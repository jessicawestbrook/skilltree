-- Create friends table
CREATE TABLE IF NOT EXISTS friends (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  friend_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  friendship_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, friend_id)
);

-- Create friend_requests table
CREATE TABLE IF NOT EXISTS friend_requests (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  sender_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  receiver_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'declined')),
  message TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(sender_id, receiver_id)
);

-- Create user_profiles table if it doesn't exist
CREATE TABLE IF NOT EXISTS user_profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  username VARCHAR(50) UNIQUE,
  avatar_url TEXT,
  bio TEXT,
  neural_level INTEGER DEFAULT 1,
  total_points INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create study_groups table
CREATE TABLE IF NOT EXISTS study_groups (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  created_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  max_members INTEGER DEFAULT 50,
  is_public BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create study_group_members table
CREATE TABLE IF NOT EXISTS study_group_members (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  group_id UUID REFERENCES study_groups(id) ON DELETE CASCADE NOT NULL,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  role VARCHAR(20) DEFAULT 'member' CHECK (role IN ('member', 'moderator', 'admin')),
  joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(group_id, user_id)
);

-- Create activity_feed table
CREATE TABLE IF NOT EXISTS activity_feed (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  activity_type VARCHAR(50) NOT NULL,
  title VARCHAR(200),
  description TEXT,
  metadata JSONB,
  visibility VARCHAR(20) DEFAULT 'public' CHECK (visibility IN ('public', 'friends', 'private')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_friends_user_id ON friends(user_id);
CREATE INDEX IF NOT EXISTS idx_friends_friend_id ON friends(friend_id);
CREATE INDEX IF NOT EXISTS idx_friend_requests_sender ON friend_requests(sender_id);
CREATE INDEX IF NOT EXISTS idx_friend_requests_receiver ON friend_requests(receiver_id);
CREATE INDEX IF NOT EXISTS idx_activity_feed_user ON activity_feed(user_id);
CREATE INDEX IF NOT EXISTS idx_study_group_members_user ON study_group_members(user_id);
CREATE INDEX IF NOT EXISTS idx_study_group_members_group ON study_group_members(group_id);

-- Enable Row Level Security
ALTER TABLE friends ENABLE ROW LEVEL SECURITY;
ALTER TABLE friend_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_groups ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_group_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_feed ENABLE ROW LEVEL SECURITY;

-- RLS Policies for friends table
CREATE POLICY "Users can view their own friendships" ON friends
  FOR SELECT USING (auth.uid() = user_id OR auth.uid() = friend_id);

CREATE POLICY "Users can create friendships" ON friends
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own friendships" ON friends
  FOR DELETE USING (auth.uid() = user_id OR auth.uid() = friend_id);

-- RLS Policies for friend_requests table
CREATE POLICY "Users can view their own friend requests" ON friend_requests
  FOR SELECT USING (auth.uid() = sender_id OR auth.uid() = receiver_id);

CREATE POLICY "Users can send friend requests" ON friend_requests
  FOR INSERT WITH CHECK (auth.uid() = sender_id);

CREATE POLICY "Users can update their own friend requests" ON friend_requests
  FOR UPDATE USING (auth.uid() = sender_id OR auth.uid() = receiver_id);

-- RLS Policies for user_profiles table
CREATE POLICY "Profiles are viewable by everyone" ON user_profiles
  FOR SELECT USING (true);

CREATE POLICY "Users can update their own profile" ON user_profiles
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert their own profile" ON user_profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

-- RLS Policies for activity_feed
CREATE POLICY "Users can view public activities" ON activity_feed
  FOR SELECT USING (
    visibility = 'public' 
    OR user_id = auth.uid()
    OR (visibility = 'friends' AND EXISTS (
      SELECT 1 FROM friends 
      WHERE (friends.user_id = auth.uid() AND friends.friend_id = activity_feed.user_id)
      OR (friends.friend_id = auth.uid() AND friends.user_id = activity_feed.user_id)
    ))
  );

CREATE POLICY "Users can create their own activities" ON activity_feed
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Create function for friend suggestions (the one we tried to create earlier)
CREATE OR REPLACE FUNCTION get_friend_suggestions(p_user_id UUID)
RETURNS TABLE (
  suggested_user_id UUID,
  username VARCHAR(50),
  neural_level INTEGER,
  total_points INTEGER,
  common_groups BIGINT,
  common_nodes BIGINT
) 
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  RETURN QUERY
  WITH user_friends AS (
    SELECT friend_id 
    FROM friends 
    WHERE user_id = p_user_id
  ),
  friend_requests_sent AS (
    SELECT receiver_id 
    FROM friend_requests 
    WHERE sender_id = p_user_id 
      AND status IN ('pending', 'accepted')
  ),
  friend_requests_received AS (
    SELECT sender_id 
    FROM friend_requests 
    WHERE receiver_id = p_user_id 
      AND status IN ('pending', 'accepted')
  ),
  excluded_users AS (
    SELECT friend_id AS user_id FROM user_friends
    UNION
    SELECT receiver_id AS user_id FROM friend_requests_sent
    UNION
    SELECT sender_id AS user_id FROM friend_requests_received
    UNION
    SELECT p_user_id AS user_id
  ),
  eligible_users AS (
    SELECT DISTINCT p.id, p.username, p.neural_level, p.total_points
    FROM user_profiles p
    WHERE p.id NOT IN (SELECT user_id FROM excluded_users)
      AND p.id IS NOT NULL
  )
  SELECT 
    eu.id AS suggested_user_id,
    eu.username,
    eu.neural_level,
    eu.total_points,
    0::BIGINT AS common_groups,
    0::BIGINT AS common_nodes
  FROM eligible_users eu
  ORDER BY 
    eu.neural_level DESC,
    eu.total_points DESC
  LIMIT 10;
END;
$$;

-- Grant execute permission
GRANT EXECUTE ON FUNCTION get_friend_suggestions(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION get_friend_suggestions(UUID) TO anon;

-- Create a trigger to automatically create a user profile when a new user signs up
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.user_profiles (id, username)
  VALUES (new.id, new.raw_user_meta_data->>'username')
  ON CONFLICT (id) DO NOTHING;
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create the trigger
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Insert profile for existing user if not exists
INSERT INTO user_profiles (id, username, neural_level, total_points)
SELECT id, COALESCE(raw_user_meta_data->>'username', email), 1, 0
FROM auth.users
WHERE id NOT IN (SELECT id FROM user_profiles)
ON CONFLICT (id) DO NOTHING;