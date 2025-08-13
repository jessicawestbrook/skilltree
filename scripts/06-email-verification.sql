-- ================================================
-- EMAIL VERIFICATION SYSTEM
-- ================================================
-- Creates tables and functions for email verification flow
-- ================================================

-- Create email_verification_tokens table
CREATE TABLE IF NOT EXISTS public.email_verification_tokens (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  token VARCHAR(255) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL,
  expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
  verified_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT unique_user_token UNIQUE(user_id, token)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_email_verification_tokens_user_id ON email_verification_tokens(user_id);
CREATE INDEX IF NOT EXISTS idx_email_verification_tokens_token ON email_verification_tokens(token);
CREATE INDEX IF NOT EXISTS idx_email_verification_tokens_expires_at ON email_verification_tokens(expires_at);

-- Add email_verified column to user_profiles if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_schema = 'public' 
    AND table_name = 'user_profiles' 
    AND column_name = 'email_verified'
  ) THEN
    ALTER TABLE public.user_profiles ADD COLUMN email_verified BOOLEAN DEFAULT false;
    ALTER TABLE public.user_profiles ADD COLUMN email_verified_at TIMESTAMP WITH TIME ZONE;
  END IF;
END $$;

-- Enable RLS
ALTER TABLE email_verification_tokens ENABLE ROW LEVEL SECURITY;

-- Create policies for email_verification_tokens
CREATE POLICY "Users can view own verification tokens" ON email_verification_tokens
  FOR SELECT TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Service role can manage all tokens" ON email_verification_tokens
  FOR ALL TO service_role
  USING (true)
  WITH CHECK (true);

-- Function to generate verification token
CREATE OR REPLACE FUNCTION generate_email_verification_token(user_uuid UUID, user_email VARCHAR)
RETURNS TABLE(token VARCHAR, expires_at TIMESTAMP WITH TIME ZONE) 
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  verification_token VARCHAR;
  token_expiry TIMESTAMP WITH TIME ZONE;
BEGIN
  -- Generate a secure random token
  verification_token := encode(gen_random_bytes(32), 'hex');
  
  -- Set expiry to 24 hours from now
  token_expiry := NOW() + INTERVAL '24 hours';
  
  -- Delete any existing unexpired tokens for this user
  DELETE FROM email_verification_tokens 
  WHERE user_id = user_uuid 
  AND expires_at > NOW()
  AND verified_at IS NULL;
  
  -- Insert the new token
  INSERT INTO email_verification_tokens (user_id, token, email, expires_at)
  VALUES (user_uuid, verification_token, user_email, token_expiry);
  
  RETURN QUERY SELECT verification_token, token_expiry;
END;
$$;

-- Function to verify email with token
CREATE OR REPLACE FUNCTION verify_email_with_token(verification_token VARCHAR)
RETURNS TABLE(success BOOLEAN, message TEXT, user_id UUID) 
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  token_record RECORD;
BEGIN
  -- Find the token
  SELECT * INTO token_record
  FROM email_verification_tokens
  WHERE token = verification_token
  AND expires_at > NOW()
  AND verified_at IS NULL
  LIMIT 1;
  
  -- Check if token exists
  IF NOT FOUND THEN
    RETURN QUERY SELECT false, 'Invalid or expired verification token', NULL::UUID;
    RETURN;
  END IF;
  
  -- Mark token as verified
  UPDATE email_verification_tokens
  SET verified_at = NOW()
  WHERE id = token_record.id;
  
  -- Update user profile
  UPDATE user_profiles
  SET email_verified = true,
      email_verified_at = NOW()
  WHERE id = token_record.user_id;
  
  -- Update auth.users metadata
  UPDATE auth.users
  SET email_confirmed_at = NOW(),
      raw_user_meta_data = raw_user_meta_data || '{"email_verified": true}'::jsonb
  WHERE id = token_record.user_id;
  
  RETURN QUERY SELECT true, 'Email verified successfully', token_record.user_id;
END;
$$;

-- Function to check if user email is verified
CREATE OR REPLACE FUNCTION is_email_verified(user_uuid UUID)
RETURNS BOOLEAN 
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  is_verified BOOLEAN;
BEGIN
  SELECT email_verified INTO is_verified
  FROM user_profiles
  WHERE id = user_uuid;
  
  RETURN COALESCE(is_verified, false);
END;
$$;

-- Function to clean up expired tokens (can be run periodically)
CREATE OR REPLACE FUNCTION cleanup_expired_verification_tokens()
RETURNS INTEGER 
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  deleted_count INTEGER;
BEGIN
  DELETE FROM email_verification_tokens
  WHERE expires_at < NOW() - INTERVAL '7 days'
  OR (verified_at IS NOT NULL AND verified_at < NOW() - INTERVAL '30 days');
  
  GET DIAGNOSTICS deleted_count = ROW_COUNT;
  RETURN deleted_count;
END;
$$;

-- Create a trigger to automatically create user profile on signup
CREATE OR REPLACE FUNCTION create_profile_on_signup()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.user_profiles (id, email_verified, username, display_name)
  VALUES (
    NEW.id,
    false,
    COALESCE(NEW.raw_user_meta_data->>'username', NEW.email),
    COALESCE(NEW.raw_user_meta_data->>'username', split_part(NEW.email, '@', 1))
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger 
    WHERE tgname = 'on_auth_user_created'
  ) THEN
    CREATE TRIGGER on_auth_user_created
      AFTER INSERT ON auth.users
      FOR EACH ROW EXECUTE FUNCTION create_profile_on_signup();
  END IF;
END $$;

-- ================================================
-- Verification
-- ================================================

DO $$
BEGIN
  RAISE NOTICE 'Email verification system created successfully!';
  RAISE NOTICE 'Tables created: email_verification_tokens';
  RAISE NOTICE 'Functions created: generate_email_verification_token, verify_email_with_token, is_email_verified, cleanup_expired_verification_tokens';
  RAISE NOTICE '';
  RAISE NOTICE 'Remember to run this migration in your Supabase dashboard!';
END $$;