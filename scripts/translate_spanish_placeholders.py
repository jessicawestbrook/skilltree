"""
Translate Spanish words that currently have placeholder translations
Processes in batches with progress tracking and recovery
"""

import os
import sys
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Install required packages if needed
for package in ['supabase', 'deep-translator']:
    try:
        __import__(package.replace('-', '_'))
    except ImportError:
        print(f"Installing {package}...")
        os.system(f"{sys.executable} -m pip install {package}")

from supabase import create_client
from deep_translator import GoogleTranslator

# Initialize Supabase with service role key
SUPABASE_URL = os.getenv('REACT_APP_SUPABASE_URL')
SUPABASE_KEY = os.getenv('REACT_APP_SUPABASE_SERVICE_ROLE_KEY')
if not SUPABASE_KEY:
    print("Error: Service role key not found!")
    sys.exit(1)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def clean_word_for_translation(word):
    """Remove articles and clean word for translation"""
    # Remove Spanish articles
    prefixes = ['el ', 'la ', 'los ', 'las ', 'un ', 'una ', 'unos ', 'unas ']
    cleaned = word
    for prefix in prefixes:
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):]
            break
    return cleaned

def save_progress(progress_file, progress_data):
    """Save progress to file"""
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f)

def load_progress(progress_file):
    """Load progress from file"""
    if os.path.exists(progress_file):
        with open(progress_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'last_id': None, 'translated_count': 0, 'failed_ids': []}

def translate_batch(words_batch, translator):
    """Translate a batch of words"""
    translations = []
    
    for record in words_batch:
        word = record['word']
        cleaned_word = clean_word_for_translation(word)
        
        try:
            # Small delay to avoid rate limiting
            time.sleep(0.05)
            
            # Translate
            translation = translator.translate(cleaned_word)
            
            # Accept any translation (even if same as original)
            # This marks it as processed rather than PENDING
            if translation:
                translations.append({
                    'id': record['id'],
                    'original': word,
                    'cleaned': cleaned_word,
                    'translation': translation
                })
            else:
                # Only skip if translation completely failed
                translations.append({
                    'id': record['id'],
                    'original': word,
                    'cleaned': cleaned_word,
                    'translation': None
                })
        except Exception as e:
            print(f"    Translation error for '{cleaned_word}': {e}")
            translations.append({
                'id': record['id'],
                'original': word,
                'cleaned': cleaned_word,
                'translation': None,
                'error': str(e)
            })
    
    return translations

def main():
    print("Translating Spanish placeholder words")
    print("="*60)
    
    progress_file = 'spanish_translation_progress.json'
    progress = load_progress(progress_file)
    
    print(f"Progress from previous run: {progress['translated_count']} words translated")
    
    # Get words that need translation
    print("\nFetching words with placeholder translations...")
    
    # Build query
    query = supabase.table('language_vocabulary') \
        .select('id, word') \
        .eq('language', 'es') \
        .eq('translation_source', 'PENDING') \
        .order('zipf_frequency', desc=True) \
        .limit(1000)  # Process 1000 at a time
    
    # Continue from last position if resuming
    if progress['last_id']:
        query = query.gt('id', progress['last_id'])
    
    response = query.execute()
    words_to_translate = response.data
    
    if not words_to_translate:
        print("No more words to translate!")
        return
    
    print(f"Found {len(words_to_translate)} words to translate in this batch")
    
    # Initialize translator
    print("\nInitializing translator...")
    translator = GoogleTranslator(source='es', target='en')
    
    # Process in smaller chunks
    chunk_size = 50
    total_translated = 0
    total_failed = 0
    
    for i in range(0, len(words_to_translate), chunk_size):
        chunk = words_to_translate[i:min(i+chunk_size, len(words_to_translate))]
        chunk_num = i//chunk_size + 1
        total_chunks = (len(words_to_translate)-1)//chunk_size + 1
        
        print(f"\nChunk {chunk_num}/{total_chunks} ({len(chunk)} words)")
        
        # Translate chunk
        translations = translate_batch(chunk, translator)
        
        # Update database
        updates_in_chunk = 0
        fails_in_chunk = 0
        
        for trans in translations:
            if trans.get('translation'):
                try:
                    # Update with translation
                    supabase.table('language_vocabulary') \
                        .update({
                            'english_translation': trans['translation'],
                            'definition_english': trans['translation'],
                            'translation_source': 'GoogleTranslator',
                            'definition_source': 'GoogleTranslator'
                        }) \
                        .eq('id', trans['id']) \
                        .execute()
                    
                    updates_in_chunk += 1
                    total_translated += 1
                    
                    # Show example
                    if updates_in_chunk <= 3:
                        print(f"  OK: {trans['original']} -> {trans['translation']}")
                    
                except Exception as e:
                    print(f"  ERROR: Failed to update {trans['original']}: {e}")
                    fails_in_chunk += 1
                    progress['failed_ids'].append(trans['id'])
            else:
                fails_in_chunk += 1
                if trans.get('error'):
                    progress['failed_ids'].append(trans['id'])
        
        total_failed += fails_in_chunk
        
        print(f"  Chunk results: {updates_in_chunk} translated, {fails_in_chunk} failed")
        
        # Update progress
        progress['last_id'] = chunk[-1]['id']
        progress['translated_count'] += updates_in_chunk
        save_progress(progress_file, progress)
    
    # Final summary
    print(f"\n{'='*60}")
    print("TRANSLATION BATCH COMPLETE")
    print(f"This batch: {total_translated} words translated, {total_failed} failed")
    print(f"Total progress: {progress['translated_count']} words translated")
    
    # Check remaining
    response = supabase.table('language_vocabulary') \
        .select('count', count='exact') \
        .eq('language', 'es') \
        .eq('translation_source', 'PENDING') \
        .execute()
    
    remaining = response.count
    print(f"Remaining placeholders: {remaining:,}")
    
    if remaining > 0:
        print(f"\nRun this script again to continue translating the next batch.")
    else:
        print("\nAll placeholder translations have been updated!")
        # Clean up progress file
        if os.path.exists(progress_file):
            os.remove(progress_file)
            print("Progress file cleaned up.")

if __name__ == "__main__":
    main()