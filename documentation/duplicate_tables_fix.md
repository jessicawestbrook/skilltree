# Data Fixes Needed: Duplicate Response Tables

## Current Status
- ✅ Unified table `user_question_responses` exists and is configured
- ✅ All duplicate tables are empty (0 rows each):
  - `question_responses` 
  - `assessment_question_responses`
  - `user_test_responses` 
  - `user_question_attempts`

## Code Updates Required

### 1. RandomQuestionBox.tsx (lines 42, 110, 118)
- Change from: `user_question_attempts`
- Change to: `user_question_responses`
- Add `context_type: 'practice'` to inserts

### 2. VisualRavensTest.tsx (line 181)
- Change from: `user_test_responses`
- Change to: `user_question_responses`
- Add `context_type: 'visual_test'` to inserts

### 3. assessmentSessionAdapter.ts (lines 166, 194)
- Change from: `assessment_question_responses`
- Change to: `user_question_responses`
- Add `context_type: 'assessment'` to inserts

### 4. questionTrackingService.ts (lines 84, 93, 287)
- Change from: `user_question_attempts`
- Change to: `user_question_responses`
- Add `context_type: 'practice'` to inserts

### 5. DiagnosticPage.tsx (line 23)
- Remove `user_question_attempts` from tables list

### 6. checkTables.ts (line 21)
- Change from: `user_question_attempts`
- Change to: `user_question_responses`

### 7. adaptiveAssessmentService.ts
- Already correctly using `user_question_responses` ✅
- Just needs comment update on line 434

## Database Actions

### Step 1: Run Verification Query
```sql
SELECT 'question_responses' as table_name, COUNT(*) as row_count FROM question_responses
UNION ALL
SELECT 'assessment_question_responses', COUNT(*) FROM assessment_question_responses
UNION ALL
SELECT 'user_test_responses', COUNT(*) FROM user_test_responses
UNION ALL
SELECT 'user_question_attempts', COUNT(*) FROM user_question_attempts;
```

### Step 2: Drop Empty Tables (After Code Updates)
```sql
DROP TABLE IF EXISTS question_responses CASCADE;
DROP TABLE IF EXISTS assessment_question_responses CASCADE;
DROP TABLE IF EXISTS user_test_responses CASCADE;
DROP TABLE IF EXISTS user_question_attempts CASCADE;
```

## Implementation Order
1. Update all code references to use `user_question_responses`
2. Test the application to ensure everything works
3. Drop the empty duplicate tables from the database
4. Remove any migration scripts that reference old tables