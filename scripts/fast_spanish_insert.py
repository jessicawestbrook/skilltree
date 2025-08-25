"""
Fast batch insertion of Spanish vocabulary
Translates all words first, then inserts in large batches
"""

import json
import os
import sys
import uuid
from datetime import datetime
from dotenv import load_dotenv
import time

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
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_phonetic_guide(word):
    """Generate phonetic guide for Spanish pronunciation"""
    phonetic = word.lower()
    replacements = [
        ('que', 'keh'), ('qui', 'kee'),
        ('ce', 'seh'), ('ci', 'see'),
        ('ge', 'heh'), ('gi', 'hee'),
        ('gue', 'geh'), ('gui', 'gee'),
        ('ll', 'y'), ('ñ', 'ny'),
        ('j', 'h'), ('rr', 'rr'),
        ('ch', 'ch'), ('v', 'b'),
        ('z', 'th'),
        ('á', 'AH'), ('é', 'EH'), 
        ('í', 'EE'), ('ó', 'OH'), ('ú', 'OO'),
        ('ü', 'w'),
    ]
    for old, new in replacements:
        phonetic = phonetic.replace(old, new)
    return phonetic

def get_part_of_speech(word):
    """Determine part of speech based on word patterns"""
    word = word.lower()
    
    if word.endswith(('ar', 'er', 'ir')) and len(word) > 3:
        return 'verb'
    elif word.endswith('mente') and len(word) > 6:
        return 'adverb'
    elif word.endswith(('ción', 'sión', 'dad', 'tad', 'ez', 'eza', 'ismo', 'miento')):
        return 'noun'
    elif word.endswith(('oso', 'osa', 'able', 'ible', 'ivo', 'iva')):
        return 'adjective'
    elif len(word) <= 3:
        return 'other'
    else:
        return 'noun'

def get_difficulty_id(zipf_freq):
    """Map Zipf frequency to difficulty ID"""
    if zipf_freq >= 5.0:
        return 1  # Basic
    elif zipf_freq >= 4.5:
        return 2  # Elementary
    elif zipf_freq >= 4.0:
        return 3  # Intermediate
    elif zipf_freq >= 3.5:
        return 4  # Advanced
    else:
        return 5  # Expert

def main():
    print("Fast Spanish Vocabulary Insertion", flush=True)
    print("="*60, flush=True)
    
    # Load vocabulary selection
    with open('spanish_vocabulary_selection.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    vocabulary = data['vocabulary']
    
    # Get existing words
    print("Loading existing words...", flush=True)
    response = supabase.table('language_vocabulary').select('word').eq('language', 'es').execute()
    existing_words = set(w['word'].lower() for w in response.data)
    print(f"Found {len(existing_words)} existing words", flush=True)
    
    # Collect all words to process
    words_to_process = []
    for difficulty in vocabulary:
        for word_data in vocabulary[difficulty]:
            word = word_data['word'].lower()
            if word not in existing_words and word_data['zipf'] >= 3.0:
                words_to_process.append(word_data)
    
    print(f"Need to process {len(words_to_process)} new words", flush=True)
    
    if not words_to_process:
        print("No new words to add!")
        return
    
    # Initialize translator
    print("\nTranslating words in batches...", flush=True)
    translator = GoogleTranslator(source='es', target='en')
    
    # Process in chunks to avoid timeout
    chunk_size = 50
    all_records = []
    
    for i in range(0, len(words_to_process), chunk_size):
        chunk = words_to_process[i:min(i+chunk_size, len(words_to_process))]
        print(f"\nProcessing chunk {i//chunk_size + 1}/{(len(words_to_process)-1)//chunk_size + 1} ({len(chunk)} words)...", flush=True)
        
        for j, word_data in enumerate(chunk):
            word = word_data['word']
            zipf = word_data['zipf']
            
            if j % 10 == 0:
                print(f"  Translating word {j+1}/{len(chunk)}: {word}", flush=True)
            
            try:
                # Small delay to avoid rate limiting
                time.sleep(0.05)
                
                # Translate
                translation = translator.translate(word)
                if not translation or translation.lower() == word.lower():
                    translation = word
                
                # Create record
                record = {
                    'id': str(uuid.uuid4()),
                    'language': 'es',
                    'word': word,
                    'zipf_frequency': zipf,
                    'difficulty_id': get_difficulty_id(zipf),
                    'english_translation': translation,
                    'pronunciation_guide': get_phonetic_guide(word),
                    'part_of_speech': get_part_of_speech(word),
                    'definition_english': translation,
                    'translation_source': 'GoogleTranslator',
                    'definition_source': 'GoogleTranslator',
                    'created_at': datetime.utcnow().isoformat()
                }
                
                all_records.append(record)
                existing_words.add(word.lower())
                
            except Exception as e:
                print(f"  Error translating {word}: {e}", flush=True)
                continue
    
    # Insert all records in large batches
    print(f"\n{'='*60}", flush=True)
    print(f"Inserting {len(all_records)} records into database...", flush=True)
    
    batch_size = 100
    total_inserted = 0
    
    for i in range(0, len(all_records), batch_size):
        batch = all_records[i:min(i+batch_size, len(all_records))]
        try:
            response = supabase.table('language_vocabulary').insert(batch).execute()
            total_inserted += len(batch)
            print(f"  Inserted batch {i//batch_size + 1}: {len(batch)} words (total: {total_inserted})", flush=True)
        except Exception as e:
            print(f"  Error inserting batch: {e}", flush=True)
            # Try inserting one by one for this batch
            for record in batch:
                try:
                    supabase.table('language_vocabulary').insert(record).execute()
                    total_inserted += 1
                except:
                    pass
    
    # Final verification
    print(f"\n{'='*60}", flush=True)
    print("INSERTION COMPLETE", flush=True)
    print(f"Successfully inserted {total_inserted} words", flush=True)
    
    # Verify final counts
    response = supabase.table('language_vocabulary').select('difficulty_id').eq('language', 'es').execute()
    counts = {}
    for record in response.data:
        diff_id = record['difficulty_id']
        counts[diff_id] = counts.get(diff_id, 0) + 1
    
    print("\nFinal distribution:")
    difficulty_names = {1: 'Basic', 2: 'Elementary', 3: 'Intermediate', 4: 'Advanced', 5: 'Expert'}
    for level in sorted(counts.keys()):
        print(f"  {difficulty_names.get(level, f'Level {level}')}: {counts[level]} words")
    print(f"  Total: {sum(counts.values())} words")

if __name__ == "__main__":
    main()