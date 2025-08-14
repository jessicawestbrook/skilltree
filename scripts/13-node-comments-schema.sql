-- Create node_comments table for user commentary on learning content
CREATE TABLE IF NOT EXISTS public.node_comments (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  node_id VARCHAR(255) NOT NULL,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  parent_id UUID REFERENCES public.node_comments(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  comment_type VARCHAR(50) DEFAULT 'comment', -- 'comment', 'note', 'insight', 'question'
  is_edited BOOLEAN DEFAULT false,
  is_deleted BOOLEAN DEFAULT false,
  upvotes INT DEFAULT 0,
  downvotes INT DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create comment votes table
CREATE TABLE IF NOT EXISTS public.comment_votes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  comment_id UUID NOT NULL REFERENCES public.node_comments(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  vote_type VARCHAR(10) NOT NULL CHECK (vote_type IN ('upvote', 'downvote')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(comment_id, user_id)
);

-- Create comment reports table for moderation
CREATE TABLE IF NOT EXISTS public.comment_reports (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  comment_id UUID NOT NULL REFERENCES public.node_comments(id) ON DELETE CASCADE,
  reporter_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  reason VARCHAR(100) NOT NULL,
  description TEXT,
  status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'reviewed', 'resolved', 'dismissed'
  reviewed_by UUID REFERENCES auth.users(id),
  reviewed_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_node_comments_node_id ON public.node_comments(node_id);
CREATE INDEX IF NOT EXISTS idx_node_comments_user_id ON public.node_comments(user_id);
CREATE INDEX IF NOT EXISTS idx_node_comments_parent_id ON public.node_comments(parent_id);
CREATE INDEX IF NOT EXISTS idx_node_comments_created_at ON public.node_comments(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_comment_votes_comment_id ON public.comment_votes(comment_id);
CREATE INDEX IF NOT EXISTS idx_comment_votes_user_id ON public.comment_votes(user_id);
CREATE INDEX IF NOT EXISTS idx_comment_reports_status ON public.comment_reports(status);

-- Enable RLS
ALTER TABLE public.node_comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.comment_votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.comment_reports ENABLE ROW LEVEL SECURITY;

-- Policies for node_comments
CREATE POLICY "Users can view all non-deleted comments" ON public.node_comments
  FOR SELECT USING (NOT is_deleted);

CREATE POLICY "Users can create their own comments" ON public.node_comments
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own comments" ON public.node_comments
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can soft delete their own comments" ON public.node_comments
  FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (is_deleted = true);

-- Policies for comment_votes
CREATE POLICY "Users can view all votes" ON public.comment_votes
  FOR SELECT USING (true);

CREATE POLICY "Users can create their own votes" ON public.comment_votes
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own votes" ON public.comment_votes
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own votes" ON public.comment_votes
  FOR DELETE USING (auth.uid() = user_id);

-- Policies for comment_reports
CREATE POLICY "Users can create reports" ON public.comment_reports
  FOR INSERT WITH CHECK (auth.uid() = reporter_id);

CREATE POLICY "Users can view their own reports" ON public.comment_reports
  FOR SELECT USING (auth.uid() = reporter_id);

-- Function to update comment vote counts
CREATE OR REPLACE FUNCTION update_comment_votes()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    IF NEW.vote_type = 'upvote' THEN
      UPDATE public.node_comments 
      SET upvotes = upvotes + 1 
      WHERE id = NEW.comment_id;
    ELSE
      UPDATE public.node_comments 
      SET downvotes = downvotes + 1 
      WHERE id = NEW.comment_id;
    END IF;
  ELSIF TG_OP = 'DELETE' THEN
    IF OLD.vote_type = 'upvote' THEN
      UPDATE public.node_comments 
      SET upvotes = GREATEST(0, upvotes - 1) 
      WHERE id = OLD.comment_id;
    ELSE
      UPDATE public.node_comments 
      SET downvotes = GREATEST(0, downvotes - 1) 
      WHERE id = OLD.comment_id;
    END IF;
  ELSIF TG_OP = 'UPDATE' THEN
    -- Handle vote type change
    IF OLD.vote_type != NEW.vote_type THEN
      IF OLD.vote_type = 'upvote' THEN
        UPDATE public.node_comments 
        SET upvotes = GREATEST(0, upvotes - 1), downvotes = downvotes + 1 
        WHERE id = NEW.comment_id;
      ELSE
        UPDATE public.node_comments 
        SET downvotes = GREATEST(0, downvotes - 1), upvotes = upvotes + 1 
        WHERE id = NEW.comment_id;
      END IF;
    END IF;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for vote count updates
DROP TRIGGER IF EXISTS trigger_update_comment_votes ON public.comment_votes;
CREATE TRIGGER trigger_update_comment_votes
  AFTER INSERT OR UPDATE OR DELETE ON public.comment_votes
  FOR EACH ROW
  EXECUTE FUNCTION update_comment_votes();

-- Function to get comments with user info
CREATE OR REPLACE FUNCTION get_node_comments_with_users(p_node_id VARCHAR(255))
RETURNS TABLE (
  id UUID,
  node_id VARCHAR(255),
  user_id UUID,
  parent_id UUID,
  content TEXT,
  comment_type VARCHAR(50),
  is_edited BOOLEAN,
  upvotes INT,
  downvotes INT,
  created_at TIMESTAMP WITH TIME ZONE,
  updated_at TIMESTAMP WITH TIME ZONE,
  username VARCHAR(255),
  avatar_url TEXT,
  user_voted VARCHAR(10),
  reply_count BIGINT
) AS $$
BEGIN
  RETURN QUERY
  WITH RECURSIVE comment_tree AS (
    -- Get root comments
    SELECT 
      nc.id,
      nc.node_id,
      nc.user_id,
      nc.parent_id,
      nc.content,
      nc.comment_type,
      nc.is_edited,
      nc.upvotes,
      nc.downvotes,
      nc.created_at,
      nc.updated_at,
      0 as level
    FROM public.node_comments nc
    WHERE nc.node_id = p_node_id 
      AND nc.parent_id IS NULL
      AND nc.is_deleted = false
    
    UNION ALL
    
    -- Get replies recursively
    SELECT 
      nc.id,
      nc.node_id,
      nc.user_id,
      nc.parent_id,
      nc.content,
      nc.comment_type,
      nc.is_edited,
      nc.upvotes,
      nc.downvotes,
      nc.created_at,
      nc.updated_at,
      ct.level + 1
    FROM public.node_comments nc
    INNER JOIN comment_tree ct ON nc.parent_id = ct.id
    WHERE nc.is_deleted = false
  ),
  reply_counts AS (
    SELECT 
      parent_id, 
      COUNT(*) as reply_count 
    FROM public.node_comments 
    WHERE is_deleted = false 
      AND parent_id IS NOT NULL
    GROUP BY parent_id
  )
  SELECT 
    ct.id,
    ct.node_id,
    ct.user_id,
    ct.parent_id,
    ct.content,
    ct.comment_type,
    ct.is_edited,
    ct.upvotes,
    ct.downvotes,
    ct.created_at,
    ct.updated_at,
    up.username,
    up.avatar_url,
    cv.vote_type as user_voted,
    COALESCE(rc.reply_count, 0) as reply_count
  FROM comment_tree ct
  LEFT JOIN public.user_profiles up ON ct.user_id = up.id
  LEFT JOIN public.comment_votes cv ON ct.id = cv.comment_id AND cv.user_id = auth.uid()
  LEFT JOIN reply_counts rc ON ct.id = rc.parent_id
  ORDER BY ct.created_at DESC;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;