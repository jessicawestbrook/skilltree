# Spanish Vocabulary System Documentation

## Overview
Foreign language vocabulary flashcard system using Zipf frequency from the wordfreq library as the basis for difficulty levels and word selection.

## Database Schema

### Main Tables

1. **language_vocabulary_difficulties** (Foreign Key Table)
   - Stores difficulty levels based on Zipf frequency ranges
   - 5 levels: Basic, Elementary, Intermediate, Advanced, Expert

2. **language_vocabulary** (Main Vocabulary Table)
   - Stores vocabulary words for all languages
   - Fields include: word, zipf_frequency, english_translation, pronunciation_guide, etc.
   - Links to difficulty table via difficulty_id

3. **language_vocabulary_progress** (User Progress Tracking)
   - Tracks user progress with spaced repetition
   - Stores review history and next review dates

4. **language_vocabulary_study_lists** (Study Lists)
   - Pre-configured study lists for each difficulty level
   - Can be filtered by language and difficulty

## Difficulty Levels (Spanish)

Based on Zipf frequency scale (0-8, higher = more common):

| Level | Name | Zipf Range | Example Words | Word Count |
|-------|------|------------|---------------|------------|
| 1 | Basic | 5.0+ | la, que, el, con | ~900 words |
| 2 | Elementary | 4.5-5.0 | ciudad, profesor, familia | ~6,000 words |
| 3 | Intermediate | 4.0-4.5 | computadora, biblioteca | ~7,000 words |
| 4 | Advanced | 3.5-4.0 | democracia, investigación | ~14,000 words |
| 5 | Expert | 3.0-3.5 | epistemología, paradigma | ~8,000 words |

Total Spanish words available: 342,072 (from wordfreq)
Selected for initial implementation: 1,500 words (top words from each level)

## Data Sources

- **Word List**: Python wordfreq library (342,072 Spanish words with Zipf frequencies)
- **Translations**: Google Translator (via deep-translator library)
- **Pronunciation**: Phonetic respelling for English speakers
- **Difficulty**: Automatic assignment based on Zipf frequency

## Implementation Status

### Completed:
- ✅ Database schema created (`create_language_vocabulary_schema.sql`)
- ✅ Spanish word sampling and cleaning (1,500 words selected)
- ✅ Translation system tested with Google Translator
- ✅ Sample data generated (50 words with translations)
- ✅ SQL insert statements prepared

### Ready to Insert:
- `insert_spanish_vocabulary.sql` - Contains:
  - Table creation statements
  - 50 sample Spanish words with translations
  - Study lists for each difficulty level
  - Verification queries

### Next Steps:
1. Run schema creation SQL in database
2. Insert sample vocabulary data
3. Create/update Language Trainer page to use new table
4. Expand to full 1,500 word dataset
5. Add more languages (French, German, etc.)

## Files Created

### Scripts:
- `scripts/sample_spanish_vocabulary.py` - Samples and cleans word variations
- `scripts/generate_spanish_sample.py` - Generates sample with translations
- `scripts/test_spanish_translation.py` - Tests translation API

### SQL Files:
- `scripts/create_language_vocabulary_schema.sql` - Database schema
- `scripts/insert_spanish_vocabulary.sql` - Sample data insertion

### Data Files:
- `spanish_vocabulary_selection.json` - 1,500 selected Spanish words
- `spanish_vocab_sample.csv` - 50 words with translations
- `spanish_vocab_sample.sql` - SQL insert preview

## Usage in App

The Language Trainer page will:
1. Query vocabulary from `language_vocabulary` table filtered by language
2. Display flashcards with word, translation, and pronunciation
3. Track progress in `language_vocabulary_progress` table
4. Use spaced repetition for review scheduling
5. Organize words by difficulty level study lists

## Quality Notes

- Base form detection was producing incorrect results (e.g., "la" -> "ar"), so it's been disabled
- Translations are functional but may need review for context
- Pronunciation guides are simplified phonetic respellings, not IPA
- Focus is on high-frequency practical vocabulary