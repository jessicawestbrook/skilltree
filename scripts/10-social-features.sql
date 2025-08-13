-- Social Features Database Schema
-- This script adds tables for friends, study groups, and activity feeds

-- Friend Requests Table
CREATE TABLE IF NOT EXISTS friend_requests (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  sender_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  receiver_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'declined', 'blocked')),
  message TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  responded_at TIMESTAMP WITH TIME ZONE,
  UNIQUE(sender_id, receiver_id),
  CHECK (sender_id != receiver_id)
);

-- Friends Table (for accepted connections)
CREATE TABLE IF NOT EXISTS friends (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  friend_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  friendship_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, friend_id),
  CHECK (user_id != friend_id)
);

-- Study Groups Table
CREATE TABLE IF NOT EXISTS study_groups (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  avatar_url TEXT,
  owner_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  max_members INTEGER DEFAULT 20,
  is_public BOOLEAN DEFAULT true,
  join_code VARCHAR(10) UNIQUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Study Group Members Table
CREATE TABLE IF NOT EXISTS study_group_members (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  group_id UUID NOT NULL REFERENCES study_groups(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  role VARCHAR(20) NOT NULL DEFAULT 'member' CHECK (role IN ('owner', 'admin', 'member')),
  joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_active TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(group_id, user_id)
);

-- Study Group Invitations
CREATE TABLE IF NOT EXISTS study_group_invitations (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  group_id UUID NOT NULL REFERENCES study_groups(id) ON DELETE CASCADE,
  inviter_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  invitee_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'declined')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  responded_at TIMESTAMP WITH TIME ZONE,
  UNIQUE(group_id, invitee_id)
);

-- Activity Feed Table
CREATE TABLE IF NOT EXISTS activity_feed (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  activity_type VARCHAR(50) NOT NULL,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  metadata JSONB DEFAULT '{}',
  visibility VARCHAR(20) DEFAULT 'friends' CHECK (visibility IN ('public', 'friends', 'group', 'private')),
  group_id UUID REFERENCES study_groups(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Study Group Messages (for group chat)
CREATE TABLE IF NOT EXISTS study_group_messages (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  group_id UUID NOT NULL REFERENCES study_groups(id) ON DELETE CASCADE,
  sender_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  message TEXT NOT NULL,
  attachments JSONB DEFAULT '[]',
  edited_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Study Group Challenges
CREATE TABLE IF NOT EXISTS study_group_challenges (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  group_id UUID NOT NULL REFERENCES study_groups(id) ON DELETE CASCADE,
  created_by UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  knowledge_node_id VARCHAR(100) REFERENCES knowledge_nodes(id),
  challenge_type VARCHAR(50) NOT NULL DEFAULT 'quiz',
  title VARCHAR(200) NOT NULL,
  description TEXT,
  start_date TIMESTAMP WITH TIME ZONE NOT NULL,
  end_date TIMESTAMP WITH TIME ZONE NOT NULL,
  min_score INTEGER DEFAULT 70,
  reward_points INTEGER DEFAULT 100,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Study Group Challenge Participants
CREATE TABLE IF NOT EXISTS study_group_challenge_participants (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  challenge_id UUID NOT NULL REFERENCES study_group_challenges(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  score INTEGER,
  completed_at TIMESTAMP WITH TIME ZONE,
  time_taken INTEGER, -- in seconds
  UNIQUE(challenge_id, user_id)
);

-- Indexes for performance
CREATE INDEX idx_friend_requests_sender ON friend_requests(sender_id);
CREATE INDEX idx_friend_requests_receiver ON friend_requests(receiver_id);
CREATE INDEX idx_friend_requests_status ON friend_requests(status);
CREATE INDEX idx_friends_user ON friends(user_id);
CREATE INDEX idx_friends_friend ON friends(friend_id);
CREATE INDEX idx_study_group_members_group ON study_group_members(group_id);
CREATE INDEX idx_study_group_members_user ON study_group_members(user_id);
CREATE INDEX idx_activity_feed_user ON activity_feed(user_id);
CREATE INDEX idx_activity_feed_created ON activity_feed(created_at DESC);
CREATE INDEX idx_activity_feed_visibility ON activity_feed(visibility);
CREATE INDEX idx_study_group_messages_group ON study_group_messages(group_id);
CREATE INDEX idx_study_group_messages_created ON study_group_messages(created_at DESC);

-- Functions and Triggers

-- Function to create bidirectional friend relationship
CREATE OR REPLACE FUNCTION create_friendship()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.status = 'accepted' THEN
    -- Insert bidirectional friendship
    INSERT INTO friends (user_id, friend_id)
    VALUES (NEW.sender_id, NEW.receiver_id), (NEW.receiver_id, NEW.sender_id)
    ON CONFLICT DO NOTHING;
    
    -- Create activity feed entries
    INSERT INTO activity_feed (user_id, activity_type, title, description, metadata)
    VALUES 
      (NEW.sender_id, 'friend_added', 'New Friend!', 'You are now friends', 
       jsonb_build_object('friend_id', NEW.receiver_id)),
      (NEW.receiver_id, 'friend_added', 'New Friend!', 'You are now friends',
       jsonb_build_object('friend_id', NEW.sender_id));
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_create_friendship
AFTER UPDATE OF status ON friend_requests
FOR EACH ROW
WHEN (NEW.status = 'accepted' AND OLD.status != 'accepted')
EXECUTE FUNCTION create_friendship();

-- Function to update group member count
CREATE OR REPLACE FUNCTION update_group_member_count()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    UPDATE study_groups 
    SET updated_at = NOW()
    WHERE id = NEW.group_id;
  ELSIF TG_OP = 'DELETE' THEN
    UPDATE study_groups 
    SET updated_at = NOW()
    WHERE id = OLD.group_id;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_group_member_count
AFTER INSERT OR DELETE ON study_group_members
FOR EACH ROW
EXECUTE FUNCTION update_group_member_count();

-- Function to generate unique join code for study groups
CREATE OR REPLACE FUNCTION generate_join_code()
RETURNS TRIGGER AS $$
DECLARE
  new_code VARCHAR(10);
  code_exists BOOLEAN;
BEGIN
  LOOP
    new_code := UPPER(SUBSTRING(MD5(RANDOM()::TEXT), 1, 8));
    SELECT EXISTS(SELECT 1 FROM study_groups WHERE join_code = new_code) INTO code_exists;
    EXIT WHEN NOT code_exists;
  END LOOP;
  NEW.join_code := new_code;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_generate_join_code
BEFORE INSERT ON study_groups
FOR EACH ROW
WHEN (NEW.join_code IS NULL)
EXECUTE FUNCTION generate_join_code();

-- View for friend suggestions (users with common groups or similar progress)
CREATE OR REPLACE VIEW friend_suggestions AS
SELECT DISTINCT
  u1.id as user_id,
  u2.id as suggested_user_id,
  COUNT(DISTINCT sgm2.group_id) as common_groups,
  COUNT(DISTINCT up2.knowledge_node_id) as common_nodes
FROM auth.users u1
CROSS JOIN auth.users u2
LEFT JOIN study_group_members sgm1 ON sgm1.user_id = u1.id
LEFT JOIN study_group_members sgm2 ON sgm2.user_id = u2.id AND sgm2.group_id = sgm1.group_id
LEFT JOIN user_progress up1 ON up1.user_id = u1.id
LEFT JOIN user_progress up2 ON up2.user_id = u2.id AND up2.knowledge_node_id = up1.knowledge_node_id
WHERE u1.id != u2.id
  AND NOT EXISTS (
    SELECT 1 FROM friends f WHERE f.user_id = u1.id AND f.friend_id = u2.id
  )
  AND NOT EXISTS (
    SELECT 1 FROM friend_requests fr 
    WHERE (fr.sender_id = u1.id AND fr.receiver_id = u2.id)
       OR (fr.sender_id = u2.id AND fr.receiver_id = u1.id)
  )
GROUP BY u1.id, u2.id
HAVING COUNT(DISTINCT sgm2.group_id) > 0 OR COUNT(DISTINCT up2.knowledge_node_id) > 5;

-- RLS Policies
ALTER TABLE friend_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE friends ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_groups ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_group_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_group_invitations ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_feed ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_group_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_group_challenges ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_group_challenge_participants ENABLE ROW LEVEL SECURITY;

-- Friend request policies
CREATE POLICY "Users can view their own friend requests"
  ON friend_requests FOR SELECT
  USING (auth.uid() = sender_id OR auth.uid() = receiver_id);

CREATE POLICY "Users can send friend requests"
  ON friend_requests FOR INSERT
  WITH CHECK (auth.uid() = sender_id);

CREATE POLICY "Users can update their received friend requests"
  ON friend_requests FOR UPDATE
  USING (auth.uid() = receiver_id);

-- Friends policies
CREATE POLICY "Users can view their own friends"
  ON friends FOR SELECT
  USING (auth.uid() = user_id);

-- Study groups policies
CREATE POLICY "Public groups are visible to all"
  ON study_groups FOR SELECT
  USING (is_public = true OR owner_id = auth.uid() OR EXISTS (
    SELECT 1 FROM study_group_members WHERE group_id = id AND user_id = auth.uid()
  ));

CREATE POLICY "Users can create study groups"
  ON study_groups FOR INSERT
  WITH CHECK (auth.uid() = owner_id);

CREATE POLICY "Group owners can update their groups"
  ON study_groups FOR UPDATE
  USING (auth.uid() = owner_id);

CREATE POLICY "Group owners can delete their groups"
  ON study_groups FOR DELETE
  USING (auth.uid() = owner_id);

-- Study group members policies
CREATE POLICY "Members can view group members"
  ON study_group_members FOR SELECT
  USING (EXISTS (
    SELECT 1 FROM study_group_members sgm 
    WHERE sgm.group_id = study_group_members.group_id 
    AND sgm.user_id = auth.uid()
  ));

-- Activity feed policies
CREATE POLICY "Users can view relevant activity"
  ON activity_feed FOR SELECT
  USING (
    visibility = 'public' OR
    user_id = auth.uid() OR
    (visibility = 'friends' AND EXISTS (
      SELECT 1 FROM friends WHERE user_id = auth.uid() AND friend_id = activity_feed.user_id
    )) OR
    (visibility = 'group' AND group_id IN (
      SELECT group_id FROM study_group_members WHERE user_id = auth.uid()
    ))
  );

CREATE POLICY "Users can create their own activities"
  ON activity_feed FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Study group messages policies
CREATE POLICY "Group members can view messages"
  ON study_group_messages FOR SELECT
  USING (EXISTS (
    SELECT 1 FROM study_group_members 
    WHERE group_id = study_group_messages.group_id 
    AND user_id = auth.uid()
  ));

CREATE POLICY "Group members can send messages"
  ON study_group_messages FOR INSERT
  WITH CHECK (
    auth.uid() = sender_id AND
    EXISTS (
      SELECT 1 FROM study_group_members 
      WHERE group_id = study_group_messages.group_id 
      AND user_id = auth.uid()
    )
  );