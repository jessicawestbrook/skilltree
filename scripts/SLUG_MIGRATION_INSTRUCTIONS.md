# Slug Migration Instructions

## Step 1: Add Slugs to Database

1. Go to your Supabase dashboard: https://app.supabase.com
2. Navigate to **SQL Editor**
3. Copy and paste the contents of `scripts/complete_slug_migration.sql`
4. Click **Run** to execute

This will:
- Add slug columns to `learning_paths` and `language_courses` tables
- Generate slugs from existing names
- Create indexes for performance
- Show sample URLs

## Step 2: Verify Slugs Were Added

After running the SQL, you should see output like:
```
Learning Paths: 1 total, 1 with_slug
Language Courses: 5 total, 5 with_slug

Sample URLs:
/learning-paths/complete-henle-latin-program
/course/henle-latin-first-year
/course/henle-latin-second-year
```

## Step 3: Update the Application

Once the database has slugs, the application components will be updated to:
- Use slugs in URLs instead of UUIDs
- Query by slug instead of ID
- Generate proper navigation links

## Example URLs

### Before (with UUIDs):
- `/learning-paths/97765ae5-4d73-43eb-8072-6b110a8c6a8a`
- `/course/cebb7f42-e51b-4ac4-8464-29fee0894024/overview`

### After (with slugs):
- `/learning-paths/complete-henle-latin-program`
- `/course/henle-latin-first-year/overview`

Much cleaner and more user-friendly!