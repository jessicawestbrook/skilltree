-- Create the learning_sessions table if it doesn't exist
CREATE TABLE IF NOT EXISTS learning_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  session_start TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  session_end TIMESTAMP WITH TIME ZONE,
  total_duration_seconds INTEGER,
  user_agent TEXT,
  device_type VARCHAR(50),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_learning_sessions_user_id ON learning_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_sessions_dates ON learning_sessions(session_start, session_end);

-- Function to start a learning session
CREATE OR REPLACE FUNCTION start_learning_session(
  p_user_id UUID,
  p_user_agent TEXT DEFAULT NULL,
  p_device_type VARCHAR(50) DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
  v_session_id UUID;
BEGIN
  INSERT INTO learning_sessions (user_id, user_agent, device_type)
  VALUES (p_user_id, p_user_agent, p_device_type)
  RETURNING id INTO v_session_id;
  
  RETURN v_session_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to end a learning session
CREATE OR REPLACE FUNCTION end_learning_session(
  p_session_id UUID,
  p_total_duration_seconds INTEGER DEFAULT NULL
)
RETURNS void AS $$
BEGIN
  UPDATE learning_sessions
  SET 
    session_end = CURRENT_TIMESTAMP,
    total_duration_seconds = COALESCE(p_total_duration_seconds, 
      EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - session_start))::INTEGER)
  WHERE id = p_session_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant permissions
GRANT EXECUTE ON FUNCTION start_learning_session TO authenticated;
GRANT EXECUTE ON FUNCTION end_learning_session TO authenticated;
GRANT SELECT, INSERT, UPDATE ON learning_sessions TO authenticated;

-- Enable RLS
ALTER TABLE learning_sessions ENABLE ROW LEVEL SECURITY;

-- Create RLS policy
CREATE POLICY "Users can manage their own sessions" ON learning_sessions
  FOR ALL 
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);