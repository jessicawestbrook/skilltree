"""
Insert ALL Spanish words with zipf >= 3 (approximately 35,000 words)
Processes in batches with progress tracking
"""

import os
import sys
import uuid
from datetime import datetime
from dotenv import load_dotenv
import time
import wordfreq
from wordfreq import zipf_frequency
import json

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

def save_progress(progress_file, processed_words):
    """Save progress to file"""
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump({'processed': list(processed_words)}, f)

def load_progress(progress_file):
    """Load progress from file"""
    if os.path.exists(progress_file):
        with open(progress_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return set(data.get('processed', []))
    return set()

def main():
    print("Extracting ALL Spanish words with zipf >= 3.0")
    print("="*60)
    
    progress_file = 'spanish_35k_progress.json'
    
    # Get existing words from database
    print("Loading existing words from database...")
    response = supabase.table('language_vocabulary').select('word').eq('language', 'es').execute()
    existing_in_db = set(w['word'].lower() for w in response.data)
    print(f"Found {len(existing_in_db)} existing words in database")
    
    # Load progress
    processed_words = load_progress(progress_file)
    if processed_words:
        print(f"Resuming from previous run: {len(processed_words)} words already processed")
    
    # Collect all Spanish words with zipf >= 3
    print("\nCollecting Spanish words from wordfreq...")
    words_to_process = []
    
    for word in wordfreq.iter_wordlist('es'):
        # Skip if already in database or already processed
        if word.lower() in existing_in_db or word.lower() in processed_words:
            continue
            
        freq = zipf_frequency(word, 'es')
        if freq >= 3.0:
            words_to_process.append({
                'word': word,
                'zipf': freq
            })
    
    print(f"Found {len(words_to_process)} new words to process")
    
    if not words_to_process:
        print("No new words to add!")
        return
    
    # Sort by frequency (highest first)
    words_to_process.sort(key=lambda x: x['zipf'], reverse=True)
    
    # Initialize translator
    print("\nInitializing translator...")
    translator = GoogleTranslator(source='es', target='en')
    
    # Process in chunks
    chunk_size = 100
    batch_size = 50  # Database insert batch size
    total_inserted = 0
    all_records = []
    
    print(f"\nProcessing {len(words_to_process)} words...")
    print("This will take some time. Progress is saved automatically.")
    print("-" * 60)
    
    for i in range(0, len(words_to_process), chunk_size):
        chunk = words_to_process[i:min(i+chunk_size, len(words_to_process))]
        chunk_num = i//chunk_size + 1
        total_chunks = (len(words_to_process)-1)//chunk_size + 1
        
        print(f"\nChunk {chunk_num}/{total_chunks} ({len(chunk)} words)")
        
        chunk_records = []
        for j, word_data in enumerate(chunk):
            word = word_data['word']
            zipf = word_data['zipf']
            
            # Progress indicator every 10 words
            if j % 10 == 0:
                print(f"  Processing {j+1}/{len(chunk)}: {word} (zipf={zipf:.1f})")
            
            try:
                # Rate limiting
                time.sleep(0.03)
                
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
                
                chunk_records.append(record)
                processed_words.add(word.lower())
                
            except Exception as e:
                print(f"    Error processing {word}: {e}")
                continue
        
        # Insert chunk into database in batches
        for k in range(0, len(chunk_records), batch_size):
            batch = chunk_records[k:min(k+batch_size, len(chunk_records))]
            try:
                response = supabase.table('language_vocabulary').insert(batch).execute()
                total_inserted += len(batch)
                print(f"    Inserted batch: {len(batch)} words (total: {total_inserted})")
            except Exception as e:
                print(f"    Error inserting batch: {e}")
                # Try one by one
                for record in batch:
                    try:
                        supabase.table('language_vocabulary').insert(record).execute()
                        total_inserted += 1
                    except:
                        pass
        
        # Save progress after each chunk
        save_progress(progress_file, processed_words)
        print(f"  Progress saved. Total processed: {len(processed_words)}")
    
    # Final verification
    print(f"\n{'='*60}")
    print("INSERTION COMPLETE")
    print(f"Successfully inserted {total_inserted} new words")
    
    # Get final counts
    response = supabase.table('language_vocabulary').select('difficulty_id').eq('language', 'es').execute()
    counts = {}
    for record in response.data:
        diff_id = record['difficulty_id']
        counts[diff_id] = counts.get(diff_id, 0) + 1
    
    print("\nFinal distribution in database:")
    difficulty_names = {1: 'Basic', 2: 'Elementary', 3: 'Intermediate', 4: 'Advanced', 5: 'Expert'}
    for level in sorted(counts.keys()):
        print(f"  {difficulty_names.get(level, f'Level {level}')}: {counts[level]:,} words")
    print(f"  Total: {sum(counts.values()):,} words")
    
    # Clean up progress file
    if os.path.exists(progress_file):
        os.remove(progress_file)
        print("\nProgress file cleaned up.")

if __name__ == "__main__":
    main()