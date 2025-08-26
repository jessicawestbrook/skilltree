# Henle Latin Questions

## Overview
40 comprehensive Latin grammar questions for the Henle Latin First Year course have been generated and are ready to be added to the database.

## Files Created

### Ready to Use
- **`insert_henle_latin_questions_correct.sql`** - SQL script ready to run in Supabase
  - Uses the `questions` table (same as assessment questions)
  - `correct_answer` is an integer index (0-based)
  - Includes ON CONFLICT clause to handle duplicates

### For Review
- **`henle_latin_questions_correct.csv`** - Spreadsheet format for easy review
- **`henle_latin_questions_correct.json`** - JSON format for programmatic review

## Question Coverage

| Module | Questions | Topics |
|--------|-----------|---------|
| First Declension Nouns | 8 | Cases, endings, translations |
| Second Declension Masculine | 8 | Cases, endings, vocative forms |
| Second Declension Neuter | 8 | Neuter rules, plural forms |
| Present Tense of Sum | 8 | All persons and numbers of "to be" |
| First Conjugation Verbs | 8 | Present tense conjugations |

**Total: 40 questions**

## How to Add to Database

1. **Review the questions** (optional)
   - Open `henle_latin_questions_correct.csv` in Excel/Google Sheets
   - Verify content and answers are correct

2. **Run the SQL in Supabase**
   ```sql
   -- Go to Supabase SQL Editor
   -- Copy contents of insert_henle_latin_questions_correct.sql
   -- Paste and click "Run"
   ```

3. **Link to Course Modules** (after adding questions)
   - Questions need to be linked to their respective course modules
   - This can be done through the module_questions table

## Question Format

Each question includes:
- **question_text**: The question prompt
- **options**: Array of 4 multiple choice options
- **correct_answer**: Integer index (0-3) of the correct option
- **explanation**: Detailed explanation of the answer
- **difficulty**: Set to "beginner" for First Year content
- **image_url**: NULL (Latin grammar doesn't need images)

## Example Question

```json
{
  "question_text": "What is the genitive singular ending for first declension nouns?",
  "options": ["-a", "-ae", "-am", "-ā"],
  "correct_answer": 1,
  "explanation": "First declension nouns have -ae as their genitive singular ending.",
  "difficulty": "beginner"
}
```

The correct answer is index 1, which corresponds to "-ae" in the options array.

## Next Steps

1. Run `insert_henle_latin_questions_correct.sql` in Supabase
2. Questions will be available in the same assessment system
3. Can be linked to course modules for structured learning
4. Can be used in language trainer and flashcard components