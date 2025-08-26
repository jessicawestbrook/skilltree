# User Module Progress Table

## Purpose
Tracks individual user progress through course modules in the Latin learning path (and any other courses).

## SQL File to Execute
**`scripts/create_user_module_progress_table.sql`**

## Features Created

### 1. Main Table: `user_module_progress`
Stores progress data for each user-module combination:
- **Unique constraint**: One record per user per module
- **Automatic timestamps**: Tracks when started, last accessed, and completed
- **Question tracking**: Records which questions answered and score
- **Content tracking**: Records which content sections viewed
- **Completion percentage**: 0-100% progress indicator

### 2. Security (RLS Policies)
- Users can only see their own progress
- Users can only modify their own records
- Fully secure with Row Level Security enabled

### 3. Automatic Features
- **Last accessed**: Updates automatically on any change
- **Completion timestamp**: Sets automatically when 100% complete
- **Indexes**: Optimized for fast queries

### 4. Summary View: `user_module_progress_summary`
Convenient view that joins:
- User information (name, username)
- Module information (title, chapter number)
- Course information (course name)
- Language information (language name)

## How It Works

### When a user starts a module:
```sql
INSERT INTO user_module_progress (user_id, module_id) 
VALUES (current_user_id, current_module_id);
```

### When a user views content:
```sql
UPDATE user_module_progress 
SET content_viewed = content_viewed || '["content_id_123"]'::jsonb
WHERE user_id = current_user_id AND module_id = current_module_id;
```

### When a user answers questions:
```sql
UPDATE user_module_progress 
SET 
    questions_answered = questions_answered || '["question_id_456"]'::jsonb,
    questions_correct = questions_correct + 1,
    questions_total = 10,
    completion_percentage = 50.00
WHERE user_id = current_user_id AND module_id = current_module_id;
```

## Benefits
1. **Progress Persistence**: Users can leave and return to exactly where they left off
2. **Achievement Tracking**: See which modules completed and when
3. **Score Tracking**: Track performance on questions
4. **Learning Analytics**: Understand how users progress through courses
5. **Motivation**: Visual progress indicators encourage completion

## To Execute
Run the SQL file in your Supabase SQL editor:
1. Copy contents of `create_user_module_progress_table.sql`
2. Paste in Supabase SQL editor
3. Click "Run"

## To Verify
After running the SQL:
```bash
python scripts/verify_module_progress_table.py
```

This will confirm the table was created successfully and is ready to use.