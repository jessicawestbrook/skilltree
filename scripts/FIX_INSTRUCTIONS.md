# Fix Instructions for Current Errors

## Issues Found:
1. **user_module_progress table missing columns** - The table doesn't have `status` or `updated_at` columns that ProfilePage expects
2. **Invalid spelling_words queries** - Flashcard IDs have prefixes like "vocab-" but the queries use them directly

## Fixes Applied:

### 1. Fixed spacedRepetitionService.ts
- Added code to strip prefixes from flashcard IDs before querying
- The IDs like "vocab-uuid" are now converted to "uuid" before database queries

### 2. Need to Execute SQL to Fix user_module_progress Table
Execute the following SQL in Supabase:

```sql
-- File: scripts/fix_user_module_progress_table.sql

-- Add status column if it doesn't exist
ALTER TABLE user_module_progress 
ADD COLUMN IF NOT EXISTS status VARCHAR(50) 
DEFAULT 'not_started' 
CHECK (status IN ('not_started', 'in_progress', 'completed'));

-- Add updated_at column if it doesn't exist
ALTER TABLE user_module_progress 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();

-- Create an update trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply the trigger
DROP TRIGGER IF EXISTS update_user_module_progress_updated_at ON user_module_progress;
CREATE TRIGGER update_user_module_progress_updated_at 
BEFORE UPDATE ON user_module_progress 
FOR EACH ROW 
EXECUTE FUNCTION update_updated_at_column();

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_module_progress_status ON user_module_progress(status);
CREATE INDEX IF NOT EXISTS idx_user_module_progress_updated_at ON user_module_progress(updated_at DESC);
```

## Steps to Complete:

1. ✅ Fixed spacedRepetitionService.ts to handle prefixed IDs
2. ⏳ Execute the SQL script above in Supabase SQL Editor to add missing columns
3. The errors should then be resolved

## What This Fixes:
- ProfilePage will be able to query user_module_progress with status and updated_at
- Spaced repetition will correctly fetch spelling_words by stripping ID prefixes
- User progress tracking will work properly