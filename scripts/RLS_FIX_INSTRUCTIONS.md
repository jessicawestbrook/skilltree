# Fixing 406 Errors for user_module_progress Table

## Issue
The CourseViewer component is getting 406 "Not Acceptable" errors when trying to access the `user_module_progress` table. This is caused by Row Level Security (RLS) policies that are too restrictive.

## Solution

### Step 1: Apply RLS Policy Fix
1. Go to your Supabase dashboard: https://app.supabase.com
2. Navigate to **SQL Editor**
3. Copy and paste the contents of `scripts/simple_rls_fix.sql`
4. Click **Run** to execute

This will:
- Enable RLS on the table (if not already enabled)
- Drop all existing policies
- Create a single, simple policy that allows users to manage their own progress

### Step 2: Verify the Fix
Run the test script to verify the policies are working:
```bash
python scripts/test_module_progress_query.py
```

You should see:
- SUCCESS for both service role and anon key queries
- No 406 errors

### Step 3: Test in the Application
1. Navigate to a course (e.g., http://localhost:3000/learning-paths)
2. Click on "Learn Latin" 
3. Click "Start Path"
4. Navigate through course content
5. Answer questions
6. Check browser console - there should be no 406 errors

## Code Changes Made

### CourseViewer.tsx Updates:
1. Changed `.single()` to `.maybeSingle()` to handle cases where no record exists
2. Added automatic creation of initial progress record when user starts a module
3. Updated upsert to use explicit conflict resolution
4. Improved error handling to continue working even if progress can't be saved

## Alternative Manual Fix (if SQL script doesn't work)

If the SQL script doesn't work, you can manually fix it in Supabase dashboard:

1. Go to **Authentication > Policies**
2. Find the `user_module_progress` table
3. Delete all existing policies
4. Create a new policy:
   - Name: "Users manage own progress"
   - Policy: `FOR ALL`
   - Check expression: `auth.uid() = user_id`
   - Using expression: `auth.uid() = user_id`

## Files Created/Modified
- `scripts/simple_rls_fix.sql` - Simple RLS policy fix
- `scripts/fix_module_progress_rls.sql` - Comprehensive RLS fix (alternative)
- `scripts/test_module_progress_query.py` - Test script to verify policies
- `scripts/apply_rls_fixes.py` - Python script to apply fixes (requires manual SQL execution)
- `src/components/CourseViewer.tsx` - Updated to handle missing records gracefully