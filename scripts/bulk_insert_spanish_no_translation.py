"""
Bulk insert Spanish words WITHOUT translation for speed
Translations can be added later in batches
"""

import os
import sys
import uuid
from datetime import datetime
from dotenv import load_dotenv
import wordfreq
from wordfreq import zipf_frequency

# Load environment variables
load_dotenv('.env.local')

# Install required packages if needed
for package in ['supabase']:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        os.system(f"{sys.executable} -m pip install {package}")

from supabase import create_client

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

def main():
    print("Bulk inserting Spanish words (NO TRANSLATION)")
    print("="*60)
    
    # Get existing words from database
    print("Loading existing words from database...")
    response = supabase.table('language_vocabulary').select('word').eq('language', 'es').execute()
    existing_in_db = set(w['word'].lower() for w in response.data)
    print(f"Found {len(existing_in_db):,} existing words in database")
    
    # Collect all Spanish words with zipf >= 3
    print("\nCollecting Spanish words from wordfreq...")
    all_records = []
    count = 0
    
    for word in wordfreq.iter_wordlist('es'):
        # Skip if already in database
        if word.lower() in existing_in_db:
            continue
            
        freq = zipf_frequency(word, 'es')
        if freq >= 3.0:
            # Create record WITHOUT translation
            record = {
                'id': str(uuid.uuid4()),
                'language': 'es',
                'word': word,
                'zipf_frequency': freq,
                'difficulty_id': get_difficulty_id(freq),
                'english_translation': word,  # Placeholder - same as Spanish word
                'pronunciation_guide': get_phonetic_guide(word),
                'part_of_speech': get_part_of_speech(word),
                'definition_english': word,  # Placeholder
                'translation_source': 'PENDING',
                'definition_source': 'PENDING',
                'created_at': datetime.utcnow().isoformat()
            }
            
            all_records.append(record)
            count += 1
            
            if count % 1000 == 0:
                print(f"  Collected {count:,} words...")
    
    print(f"\nTotal new words to insert: {len(all_records):,}")
    
    if not all_records:
        print("No new words to add!")
        return
    
    # Insert in large batches
    batch_size = 500
    total_inserted = 0
    
    print(f"\nInserting {len(all_records):,} records in batches of {batch_size}...")
    
    for i in range(0, len(all_records), batch_size):
        batch = all_records[i:min(i+batch_size, len(all_records))]
        try:
            response = supabase.table('language_vocabulary').insert(batch).execute()
            total_inserted += len(batch)
            print(f"  Batch {i//batch_size + 1}: Inserted {len(batch)} words (total: {total_inserted:,})")
        except Exception as e:
            print(f"  Error inserting batch: {e}")
            # Try smaller batches
            for j in range(0, len(batch), 50):
                mini_batch = batch[j:min(j+50, len(batch))]
                try:
                    supabase.table('language_vocabulary').insert(mini_batch).execute()
                    total_inserted += len(mini_batch)
                except Exception as e2:
                    print(f"    Error with mini-batch: {e2}")
    
    # Final verification
    print(f"\n{'='*60}")
    print("BULK INSERTION COMPLETE")
    print(f"Successfully inserted {total_inserted:,} words")
    
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
    print(f"  Total: {sum(counts.values()):,} Spanish words")
    
    # Count how many need translation
    response = supabase.table('language_vocabulary').select('count', count='exact').eq('language', 'es').eq('translation_source', 'PENDING').execute()
    print(f"\nWords needing translation: {response.count:,}")
    print("\nNote: Translations can be added later using a separate script.")

if __name__ == "__main__":
    main()