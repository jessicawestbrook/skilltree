# Reusable Scripts for Word Management

This folder contains production-ready scripts for managing words in the spelling_words table. These scripts automatically calculate frequencies, predict difficulties, and optionally generate content.

## 📁 Scripts

### 1. `add_word_with_metadata.py` - Full-Featured Word Addition
Adds words with complete metadata including Claude API-generated definitions and examples.

**Features:**
- Calculates Zipf frequency from wordfreq library
- Predicts spelling difficulty (1-5) using XGBoost model
- Calculates vocabulary difficulty (1-5) based on frequency bins
- Generates definitions, examples, etymology, mnemonics via Claude API
- Checks for duplicates
- Saves results to JSON

**Usage:**
```bash
# Add individual words
python scripts/reusable/add_word_with_metadata.py perspicacious ubiquitous serendipity

# Add from file
python scripts/reusable/add_word_with_metadata.py --file new_words.txt

# Force add even if exists
python scripts/reusable/add_word_with_metadata.py --force word1 word2
```

### 2. `add_words_bulk.py` - Fast Bulk Addition
Adds words quickly without Claude API calls. Best for large word lists.

**Features:**
- Calculates Zipf frequency
- Predicts both difficulty levels
- Batch inserts for efficiency
- Duplicate checking
- No API calls (faster)

**Usage:**
```bash
# Add from file
python scripts/reusable/add_words_bulk.py --file word_list.txt

# Add individual words
python scripts/reusable/add_words_bulk.py cat dog elephant
```

### 3. `update_vocabulary_difficulty_by_frequency.sql` - Update Vocabulary Difficulties
SQL script to update all vocabulary difficulty levels based on frequency bins.

**Frequency to Difficulty Mapping:**
| Frequency (Zipf) | Vocabulary Level | Description |
|-----------------|------------------|-------------|
| 6+ | 1 | Basic (very common) |
| 5-6 | 2 | Elementary (common) |
| 3-5 | 3 | Intermediate (moderate/uncommon) |
| 2-3 | 4 | Advanced (rare) |
| 0-2 | 5 | Expert (very rare) |

**Usage:**
```sql
-- Run in SQL editor or psql
\i scripts/reusable/update_vocabulary_difficulty_by_frequency.sql
```

## 🔧 Requirements

### Environment Variables (.env.local)
```
REACT_APP_SUPABASE_URL=your_supabase_url
REACT_APP_SUPABASE_ANON_KEY=your_supabase_key
ANTHROPIC_API_KEY=your_claude_api_key  # Only for add_word_with_metadata.py
```

### Python Packages
- wordfreq - For Zipf frequency calculations
- supabase - Database connection
- anthropic - Claude API (only for full metadata script)
- xgboost - Spelling difficulty prediction
- numpy - Array operations

### Model Files
- `xgboost_spelling_model.json` - Trained XGBoost model for spelling difficulty
- `feature_names.json` - Feature names for the model

## 📊 Difficulty Calculations

### Spelling Difficulty (1-5)
Predicted using XGBoost model trained on ~10,000 words with bee ratings. Features include:
- Word frequency (most important - 33% importance)
- Word length (22% importance)
- Orthographic patterns (silent letters, double letters, etc.)
- Morphological features (prefixes, suffixes)

### Vocabulary Difficulty (1-5)
Based purely on word frequency bins:
- Level 1: Words everyone knows (the, have, good)
- Level 2: Common words (happy, friend, school)
- Level 3: Moderate vocabulary (economy, substantial)
- Level 4: Advanced words (perspicacious, ubiquitous)
- Level 5: Expert/rare words (sesquipedalian, antidisestablishmentarianism)

## 📝 Database Schema

Words are added with these fields:
```sql
id                          -- UUID
word                        -- The word itself
frequency                   -- Zipf frequency (0-8, higher = more common)
spelling_difficulty_level   -- 1-5 (1 = easiest)
vocabulary_difficulty_level -- 1-5 (1 = most common)
definition                  -- From Claude API (optional)
part_of_speech             -- From Claude API (optional)
example_sentence           -- From Claude API (optional)
etymology                  -- From Claude API (optional)
synonyms                   -- Array from Claude API (optional)
difficulty_notes           -- From Claude API (optional)
mnemonic_device           -- From Claude API (optional)
source                    -- 'auto_generated' or 'bulk_import'
created_at                -- Timestamp
```

## 🚀 Best Practices

1. **For small additions (< 50 words)**: Use `add_word_with_metadata.py` for rich content
2. **For large imports (> 50 words)**: Use `add_words_bulk.py` for speed
3. **Always check for duplicates**: Both scripts do this automatically
4. **Backup before bulk operations**: Scripts create backups automatically
5. **Monitor API usage**: Claude API calls cost money, use bulk script for large lists

## 📈 Typical Workflow

1. **Initial bulk import:**
   ```bash
   python scripts/reusable/add_words_bulk.py --file spelling_bee_words.txt
   ```

2. **Update vocabulary difficulties:**
   ```sql
   -- Run the SQL to set vocabulary levels based on frequency
   ```

3. **Add individual words with full content:**
   ```bash
   python scripts/reusable/add_word_with_metadata.py "challenging" "word"
   ```

## 🔍 Troubleshooting

- **"XGBoost model not found"**: The script will fall back to a simple algorithm
- **"Missing API key"**: Add ANTHROPIC_API_KEY to .env.local for full metadata
- **Duplicate errors**: Use --force flag or bulk script handles automatically
- **Slow performance**: Use bulk script instead of metadata script for large lists

## 📊 Statistics

After adding words, you can check the distribution:
```sql
-- Check difficulty distributions
SELECT 
    spelling_difficulty_level,
    vocabulary_difficulty_level,
    COUNT(*) as count,
    AVG(frequency) as avg_freq
FROM spelling_words
GROUP BY spelling_difficulty_level, vocabulary_difficulty_level
ORDER BY spelling_difficulty_level, vocabulary_difficulty_level;
```