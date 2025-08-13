-- Create push subscriptions table
CREATE TABLE IF NOT EXISTS push_subscriptions (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  endpoint TEXT NOT NULL,
  p256dh TEXT NOT NULL,
  auth TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id)
);

-- Create user notification preferences table
CREATE TABLE IF NOT EXISTS user_notification_preferences (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE UNIQUE,
  daily_reminders BOOLEAN DEFAULT true,
  achievement_alerts BOOLEAN DEFAULT true,
  streak_notifications BOOLEAN DEFAULT true,
  friend_activity BOOLEAN DEFAULT true,
  new_content BOOLEAN DEFAULT true,
  reminder_time TIME DEFAULT '09:00:00',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create notification history table for tracking
CREATE TABLE IF NOT EXISTS notification_history (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  data JSONB,
  sent_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  read_at TIMESTAMP WITH TIME ZONE,
  clicked_at TIMESTAMP WITH TIME ZONE,
  dismissed_at TIMESTAMP WITH TIME ZONE
);

-- Create scheduled notifications table
CREATE TABLE IF NOT EXISTS scheduled_notifications (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  data JSONB,
  scheduled_for TIMESTAMP WITH TIME ZONE NOT NULL,
  sent BOOLEAN DEFAULT false,
  sent_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_push_subscriptions_user_id ON push_subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_notification_history_user_id ON notification_history(user_id);
CREATE INDEX IF NOT EXISTS idx_notification_history_sent_at ON notification_history(sent_at);
CREATE INDEX IF NOT EXISTS idx_scheduled_notifications_scheduled_for ON scheduled_notifications(scheduled_for);
CREATE INDEX IF NOT EXISTS idx_scheduled_notifications_sent ON scheduled_notifications(sent);

-- Enable RLS
ALTER TABLE push_subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_notification_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE notification_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE scheduled_notifications ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for push_subscriptions
CREATE POLICY "Users can view own push subscriptions"
  ON push_subscriptions FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own push subscriptions"
  ON push_subscriptions FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own push subscriptions"
  ON push_subscriptions FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own push subscriptions"
  ON push_subscriptions FOR DELETE
  USING (auth.uid() = user_id);

-- Create RLS policies for user_notification_preferences
CREATE POLICY "Users can view own notification preferences"
  ON user_notification_preferences FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own notification preferences"
  ON user_notification_preferences FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own notification preferences"
  ON user_notification_preferences FOR UPDATE
  USING (auth.uid() = user_id);

-- Create RLS policies for notification_history
CREATE POLICY "Users can view own notification history"
  ON notification_history FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Service role can insert notification history"
  ON notification_history FOR INSERT
  WITH CHECK (true);

-- Create RLS policies for scheduled_notifications
CREATE POLICY "Users can view own scheduled notifications"
  ON scheduled_notifications FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Service role can manage scheduled notifications"
  ON scheduled_notifications FOR ALL
  USING (true);

-- Create function to clean old notification history
CREATE OR REPLACE FUNCTION clean_old_notifications()
RETURNS void AS $$
BEGIN
  -- Delete notifications older than 30 days
  DELETE FROM notification_history 
  WHERE sent_at < CURRENT_TIMESTAMP - INTERVAL '30 days';
  
  -- Delete sent scheduled notifications older than 7 days
  DELETE FROM scheduled_notifications 
  WHERE sent = true AND sent_at < CURRENT_TIMESTAMP - INTERVAL '7 days';
END;
$$ LANGUAGE plpgsql;

-- Create function to schedule daily reminders
CREATE OR REPLACE FUNCTION schedule_daily_reminders()
RETURNS void AS $$
DECLARE
  user_record RECORD;
BEGIN
  -- For each user with daily reminders enabled
  FOR user_record IN 
    SELECT u.id, p.reminder_time 
    FROM auth.users u
    JOIN user_notification_preferences p ON u.id = p.user_id
    WHERE p.daily_reminders = true
  LOOP
    -- Schedule reminder for tomorrow at their preferred time
    INSERT INTO scheduled_notifications (
      user_id, 
      type, 
      title, 
      body, 
      scheduled_for
    ) VALUES (
      user_record.id,
      'reminder',
      '🧠 Time to Learn!',
      'Continue your journey in NeuroQuest and keep your streak alive!',
      (CURRENT_DATE + INTERVAL '1 day' + user_record.reminder_time)::TIMESTAMP WITH TIME ZONE
    )
    ON CONFLICT DO NOTHING;
  END LOOP;
END;
$$ LANGUAGE plpgsql;