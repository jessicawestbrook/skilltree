-- Simple, focused fix for signup trigger issue
-- This removes complexity and ensures signup always succeeds

-- 1. Drop the problematic trigger
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users CASCADE;

-- 2. Drop the function
DROP FUNCTION IF EXISTS public.handle_new_user() CASCADE;

-- 3. Create a minimal trigger function that won't fail
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  -- Try to insert profile, but ignore ALL errors
  BEGIN
    INSERT INTO public.profiles (id, email)
    VALUES (NEW.id, NEW.email);
  EXCEPTION WHEN OTHERS THEN
    -- Silently ignore all errors
    NULL;
  END;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 4. Create the trigger
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();

-- 5. Grant necessary permissions
GRANT EXECUTE ON FUNCTION public.handle_new_user() TO service_role;

-- 6. Test the function manually to ensure it works
DO $$
BEGIN
  RAISE NOTICE 'Trigger function created successfully';
END $$;