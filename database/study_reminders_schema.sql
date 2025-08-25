-- Study Reminders Database Schema
-- Extends the existing notification system with study-specific reminders

-- 1. Create study_reminders table for scheduled study sessions
CREATE TABLE IF NOT EXISTS study_reminders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  
  -- What to study
  reminder_type TEXT NOT NULL CHECK (reminder_type IN ('flashcard_review', 'skill_practice', 'custom')),
  content_type TEXT, -- 'vocabulary', 'spelling', 'language', 'skill_node', etc.
  content_ids UUID[], -- Array of specific flashcard/skill IDs to review
  
  -- When to remind
  scheduled_for TIMESTAMP WITH TIME ZONE NOT NULL,
  reminder_sent BOOLEAN DEFAULT false,
  reminder_sent_at TIMESTAMP WITH TIME ZONE,
  
  -- Study session details
  study_duration_minutes INTEGER DEFAULT 15,
  priority TEXT CHECK (priority IN ('low', 'medium', 'high')) DEFAULT 'medium',
  
  -- Metadata
  title TEXT,
  description TEXT,
  metadata JSONB DEFAULT '{}',
  
  -- Tracking
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  completed_at TIMESTAMP WITH TIME ZONE,
  dismissed_at TIMESTAMP WITH TIME ZONE,
  
  -- Recurrence settings (optional)
  is_recurring BOOLEAN DEFAULT false,
  recurrence_pattern TEXT CHECK (recurrence_pattern IN ('daily', 'weekly', 'custom')),
  recurrence_days INTEGER[], -- For weekly: 0=Sunday, 6=Saturday
  recurrence_end_date TIMESTAMP WITH TIME ZONE
);

-- 2. Create study_schedules table for user's preferred study times
CREATE TABLE IF NOT EXISTS study_schedules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  
  -- Schedule details
  schedule_name TEXT NOT NULL,
  is_active BOOLEAN DEFAULT true,
  
  -- Time preferences
  preferred_days INTEGER[], -- 0=Sunday, 6=Saturday
  preferred_time TIME NOT NULL, -- Local time for the reminder
  timezone TEXT DEFAULT 'America/New_York',
  
  -- What to study
  content_types TEXT[], -- Types of content to include
  difficulty_levels TEXT[], -- Difficulty levels to focus on
  
  -- Session settings
  session_duration_minutes INTEGER DEFAULT 15,
  cards_per_session INTEGER DEFAULT 20,
  
  -- Auto-scheduling based on spaced repetition
  auto_schedule_reviews BOOLEAN DEFAULT true,
  include_overdue BOOLEAN DEFAULT true,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Create notification_queue table for processing scheduled notifications
CREATE TABLE IF NOT EXISTS notification_queue (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  notification_id UUID REFERENCES notifications(id) ON DELETE CASCADE,
  reminder_id UUID REFERENCES study_reminders(id) ON DELETE CASCADE,
  
  scheduled_for TIMESTAMP WITH TIME ZONE NOT NULL,
  status TEXT CHECK (status IN ('pending', 'sent', 'failed', 'cancelled')) DEFAULT 'pending',
  
  attempts INTEGER DEFAULT 0,
  last_attempt_at TIMESTAMP WITH TIME ZONE,
  sent_at TIMESTAMP WITH TIME ZONE,
  error_message TEXT,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Create indexes for performance
CREATE INDEX IF NOT EXISTS study_reminders_user_id_idx ON study_reminders(user_id);
CREATE INDEX IF NOT EXISTS study_reminders_scheduled_for_idx ON study_reminders(scheduled_for);
CREATE INDEX IF NOT EXISTS study_reminders_reminder_sent_idx ON study_reminders(reminder_sent);
CREATE INDEX IF NOT EXISTS study_schedules_user_id_idx ON study_schedules(user_id);
CREATE INDEX IF NOT EXISTS study_schedules_is_active_idx ON study_schedules(is_active);
CREATE INDEX IF NOT EXISTS notification_queue_scheduled_for_idx ON notification_queue(scheduled_for);
CREATE INDEX IF NOT EXISTS notification_queue_status_idx ON notification_queue(status);

-- 5. Enable RLS
ALTER TABLE study_reminders ENABLE ROW LEVEL SECURITY;
ALTER TABLE study_schedules ENABLE ROW LEVEL SECURITY;
ALTER TABLE notification_queue ENABLE ROW LEVEL SECURITY;

-- 6. Create RLS policies
-- Study reminders policies
CREATE POLICY "Users can view their own study reminders" ON study_reminders
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own study reminders" ON study_reminders
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own study reminders" ON study_reminders
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own study reminders" ON study_reminders
  FOR DELETE USING (auth.uid() = user_id);

-- Study schedules policies
CREATE POLICY "Users can view their own study schedules" ON study_schedules
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own study schedules" ON study_schedules
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own study schedules" ON study_schedules
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own study schedules" ON study_schedules
  FOR DELETE USING (auth.uid() = user_id);

-- Notification queue policies (admin/system only for now)
CREATE POLICY "System can manage notification queue" ON notification_queue
  FOR ALL USING (true);

-- 7. Create function to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_study_reminders_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_study_schedules_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 8. Create triggers for updated_at
DROP TRIGGER IF EXISTS update_study_reminders_updated_at_trigger ON study_reminders;
CREATE TRIGGER update_study_reminders_updated_at_trigger
  BEFORE UPDATE ON study_reminders
  FOR EACH ROW
  EXECUTE FUNCTION update_study_reminders_updated_at();

DROP TRIGGER IF EXISTS update_study_schedules_updated_at_trigger ON study_schedules;
CREATE TRIGGER update_study_schedules_updated_at_trigger
  BEFORE UPDATE ON study_schedules
  FOR EACH ROW
  EXECUTE FUNCTION update_study_schedules_updated_at();

-- 9. Function to create next reminder based on spaced repetition
CREATE OR REPLACE FUNCTION create_next_study_reminder(
  p_user_id UUID,
  p_content_type TEXT,
  p_content_ids UUID[],
  p_interval_days INTEGER
)
RETURNS UUID AS $$
DECLARE
  v_reminder_id UUID;
  v_scheduled_time TIMESTAMP WITH TIME ZONE;
BEGIN
  -- Calculate next review time (default to same time tomorrow if no schedule exists)
  SELECT 
    CURRENT_TIMESTAMP + (p_interval_days || ' days')::INTERVAL
  INTO v_scheduled_time;
  
  -- Try to use user's preferred study time if available
  SELECT 
    date_trunc('day', CURRENT_TIMESTAMP + (p_interval_days || ' days')::INTERVAL) + preferred_time
  INTO v_scheduled_time
  FROM study_schedules
  WHERE user_id = p_user_id 
    AND is_active = true
  LIMIT 1;
  
  -- Create the reminder
  INSERT INTO study_reminders (
    user_id,
    reminder_type,
    content_type,
    content_ids,
    scheduled_for,
    title,
    description
  ) VALUES (
    p_user_id,
    'flashcard_review',
    p_content_type,
    p_content_ids,
    COALESCE(v_scheduled_time, CURRENT_TIMESTAMP + (p_interval_days || ' days')::INTERVAL),
    'Time to review your ' || p_content_type || ' flashcards!',
    'You have ' || array_length(p_content_ids, 1) || ' cards due for review'
  )
  RETURNING id INTO v_reminder_id;
  
  RETURN v_reminder_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;