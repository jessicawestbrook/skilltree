# Quiz Questions Database Migration

## Overview
This document explains how to migrate quiz questions from the local file system to your Supabase database.

## Prerequisites
1. Supabase project set up
2. Environment variables configured in `.env.local`:
   ```
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

## Database Schema
Create the following table in your Supabase database:

```sql
CREATE TABLE quiz_questions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  node_id VARCHAR(255) NOT NULL,
  question TEXT NOT NULL,
  options JSONB NOT NULL,
  correct_answer INTEGER NOT NULL,
  explanation TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE,
  
  -- Index for faster queries
  INDEX idx_quiz_questions_node_id (node_id)
);
```

## Running the Migration

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   Create a `.env.local` file with your Supabase credentials.

3. **Run the migration script:**
   ```bash
   npm run migrate:questions
   ```

   This will:
   - Connect to your Supabase database
   - Insert all quiz questions from the local data
   - Show progress and any errors
   - Display a summary at the end

## Features Added

### 1. Quiz Service (`src/services/quizService.ts`)
- `getQuestionsForNode(nodeId)` - Fetch questions for a specific node
- `getAllQuestions()` - Fetch all questions
- `addQuestion()` - Add new questions
- `updateQuestion()` - Update existing questions
- `deleteQuestion()` - Delete questions
- Automatic fallback to local questions if database is unavailable

### 2. React Hook (`src/hooks/useQuizQuestions.ts`)
- `useQuizQuestions(nodeId)` - Hook to fetch questions for a node
- `useAllQuizQuestions()` - Hook to fetch all questions
- Handles loading states and errors
- Automatic refetch on node change

### 3. App Integration
The main app (`src/app/page.tsx`) now:
- Fetches questions from Supabase in real-time
- Shows loading state while fetching
- Handles cases where no questions are available
- Falls back gracefully on errors

## Adding New Questions

To add new questions to the database:

1. **Via Supabase Dashboard:**
   - Go to your Supabase project
   - Navigate to the Table Editor
   - Select `quiz_questions` table
   - Click "Insert row" and add your question

2. **Via Code:**
   ```javascript
   import { QuizService } from '@/services/quizService';
   
   await QuizService.addQuestion('node-id', {
     question: 'Your question here?',
     options: ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
     correct: 0, // Index of correct answer
     explanation: 'Explanation of the answer'
   });
   ```

## Troubleshooting

1. **Migration fails with connection error:**
   - Check your Supabase URL and API key
   - Ensure your Supabase project is active
   - Check network connectivity

2. **Questions not showing in app:**
   - Check browser console for errors
   - Verify questions exist in database
   - Check that node IDs match between app and database

3. **Fallback questions appearing:**
   - This means the database query failed
   - Check Supabase logs for errors
   - Verify table permissions (should allow SELECT for anon users)

## Security Notes
- The anon key is safe to use in client-side code
- Set up Row Level Security (RLS) policies for production
- Consider adding authentication for write operations