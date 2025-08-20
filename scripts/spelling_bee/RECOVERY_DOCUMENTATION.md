# Spelling Bee Data Processing - Recovery Documentation

## Overview
This document explains how to recover and restart the spelling bee data processing if it fails or is interrupted.

## Prerequisites
Before running the script, ensure you have the following Python packages installed:
```bash
pip install PyPDF2 requests
```

## Running the Script

### Initial Run
```bash
cd C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee
python process_spelling_words.py
```

### Resuming After Interruption
The script automatically saves progress every 100 words. To resume:
1. Simply run the same command again: `python process_spelling_words.py`
2. The script will automatically load the checkpoint and continue from where it left off

## Checkpoint System

### Checkpoint File Location
- **File**: `output/checkpoint.json`
- **Contents**: 
  - `processed_words`: Dictionary of all successfully processed words
  - `words_for_review`: List of words that couldn't be processed
  - `last_processed_index`: Number of words processed so far
  - `timestamp`: Last checkpoint save time

### Manual Checkpoint Inspection
To check progress:
```python
import json
with open('output/checkpoint.json', 'r') as f:
    data = json.load(f)
    print(f"Words processed: {len(data['processed_words'])}")
    print(f"Words for review: {len(data['words_for_review'])}")
```

## Output Files

### Main Output
- **File**: `output/spelling_words.csv`
- **Description**: Contains all successfully processed words with complete data
- **Format**: CSV with quoted fields, UTF-8 encoding

### Review File
- **File**: `output/words_for_review.csv`
- **Description**: Words that need manual review (no definition found)
- **Format**: CSV with word and reason for review

## Common Issues and Solutions

### Issue 1: API Rate Limiting
**Symptom**: Script pauses frequently with "Rate limited" messages
**Solution**: 
- The script automatically handles rate limiting with delays
- If persistent, increase `api_delay` in the script (default: 1.0 seconds)

### Issue 2: Network Connection Lost
**Symptom**: Script fails with connection error
**Solution**: 
- Check internet connection
- Run the script again - it will resume from checkpoint

### Issue 3: PDF Reading Errors
**Symptom**: "Error processing PDF" messages
**Solution**:
- Check if PDF files are corrupted
- The script will continue with other PDFs
- Note which PDFs failed for manual review

### Issue 4: Memory Issues
**Symptom**: Script crashes with memory error
**Solution**:
- Reduce `batch_size` in the script (default: 100)
- Close other applications to free memory

## Manual Recovery Steps

If the checkpoint is corrupted or you need to start fresh:

1. **Backup existing data**:
   ```bash
   copy output\checkpoint.json output\checkpoint_backup.json
   copy output\spelling_words.csv output\spelling_words_backup.csv
   ```

2. **Clear checkpoint** (to start over):
   ```bash
   del output\checkpoint.json
   ```

3. **Partial recovery** (keep some processed words):
   - Edit `checkpoint.json`
   - Remove corrupted entries from `processed_words`
   - Update `last_processed_index`
   - Run script again

## Database Upload Preparation

After successful completion:

1. **Review the output CSV**:
   - Check `output/spelling_words.csv` for completeness
   - Review `output/words_for_review.csv` for words needing attention

2. **Prepare for database upload**:
   - The CSV is formatted to match the `spelling_words` table structure
   - Fields are properly quoted and UTF-8 encoded
   - Common misspellings are JSON-encoded in the CSV

3. **Validate before upload**:
   ```python
   import csv
   with open('output/spelling_words.csv', 'r', encoding='utf-8') as f:
       reader = csv.DictReader(f)
       words = list(reader)
       print(f"Total words ready for upload: {len(words)}")
       print(f"Difficulty distribution:")
       for level in range(1, 6):
           count = sum(1 for w in words if w['difficulty_level'] == str(level))
           print(f"  Level {level}: {count} words")
   ```

## Monitoring Progress

The script logs to both console and `spelling_bee_processing.log`. Monitor progress by:
- Watching console output for real-time updates
- Checking log file for detailed history
- Reviewing checkpoint file for exact count

## Performance Expectations

- **Processing rate**: ~60 words per minute (with API calls)
- **Total time estimate**: For 5000 words, expect ~1.5-2 hours
- **Checkpoint frequency**: Every 100 words (configurable)
- **API delays**: 1 second between calls (configurable)

## Contact for Issues
If you encounter issues not covered here, check the log file for detailed error messages and ensure all dependencies are correctly installed.