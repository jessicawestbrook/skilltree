"""
Insert all Spanish vocabulary from selection file into database
Processes by difficulty level and avoids duplicates
"""

import json
import os
import sys
import uuid
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
import time

# Initialize Supabase with service role key to bypass RLS
SUPABASE_URL = os.getenv('REACT_APP_SUPABASE_URL')
# Use service role key to bypass RLS
SUPABASE_KEY = os.getenv('REACT_APP_SUPABASE_SERVICE_ROLE_KEY')
if not SUPABASE_KEY:
    print("Warning: No service role key found, falling back to anon key (may encounter RLS issues)")
    SUPABASE_KEY = os.getenv('REACT_APP_SUPABASE_ANON_KEY')
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
        ('z', 'th'), # Spain Spanish
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
    
    # Common patterns
    if word.endswith(('ar', 'er', 'ir')) and len(word) > 3:
        return 'verb'
    elif word.endswith('mente') and len(word) > 6:
        return 'adverb'
    elif word.endswith(('ción', 'sión', 'dad', 'tad', 'ez', 'eza', 'ismo', 'miento')):
        return 'noun'
    elif word.endswith(('oso', 'osa', 'able', 'ible', 'ivo', 'iva')):
        return 'adjective'
    elif len(word) <= 3:
        return 'other'  # Articles, prepositions, etc.
    else:
        return 'noun'  # Default

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
    elif zipf_freq >= 3.0:
        return 5  # Expert

def load_existing_words():
    """Load existing words from database"""
    try:
        response = supabase.table('language_vocabulary').select('word').eq('language', 'es').execute()
        return set(w['word'].lower() for w in response.data)
    except Exception as e:
        print(f"Error loading existing words: {e}")
        return set()

def clean_word_list(words, existing_words):
    """Remove duplicates and variations"""
    cleaned = []
    seen_roots = set()
    
    for word_data in words:
        word = word_data['word'].lower()
        
        # Skip if already in database
        if word in existing_words:
            continue
        
        # Skip common variations
        # Skip plurals if singular exists
        if word.endswith('s') and word[:-1] in existing_words:
            continue
        if word.endswith('es') and word[:-2] in existing_words:
            continue
        
        # Skip feminine if masculine exists
        if word.endswith('a') and word[:-1] + 'o' in existing_words:
            continue
        
        # Skip conjugated verbs (keep infinitives)
        if not word.endswith(('ar', 'er', 'ir')) and len(word) > 4:
            # Check if it might be a conjugation
            possible_infinitives = [
                word + 'ar', word + 'er', word + 'ir',
                word[:-1] + 'ar', word[:-1] + 'er', word[:-1] + 'ir',
                word[:-2] + 'ar', word[:-2] + 'er', word[:-2] + 'ir'
            ]
            if any(inf in existing_words or inf in seen_roots for inf in possible_infinitives):
                continue
        
        # Track this word
        seen_roots.add(word)
        cleaned.append(word_data)
    
    return cleaned

def process_difficulty_level(difficulty_name, words, existing_words, translator):
    """Process and insert words for a specific difficulty level"""
    print(f"\n{'='*60}")
    print(f"Processing {difficulty_name} level: {len(words)} words")
    print(f"{'='*60}")
    
    # Clean the word list
    cleaned_words = clean_word_list(words, existing_words)
    print(f"After removing duplicates: {len(cleaned_words)} words to process")
    
    if not cleaned_words:
        print("No new words to add for this level")
        return 0
    
    # Process in batches
    batch_size = 10  # Reduced batch size for reliability
    total_added = 0
    
    for i in range(0, len(cleaned_words), batch_size):
        batch = cleaned_words[i:min(i+batch_size, len(cleaned_words))]
        print(f"\nBatch {i//batch_size + 1}: Processing {len(batch)} words...")
        
        records = []
        for word_data in batch:
            word = word_data['word']
            zipf = word_data['zipf']
            
            try:
                # Add small delay to avoid rate limiting
                time.sleep(0.05)  # Reduced delay since we have smaller batches
                
                # Translate
                translation = translator.translate(word)
                
                # Skip if translation is same as original
                if translation and translation.lower() == word.lower():
                    translation = word  # Keep original if no translation
                
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
                
                records.append(record)
                existing_words.add(word.lower())  # Track as added
                print(f"  [OK] {word} -> {translation}")
                
            except Exception as e:
                print(f"  [ERROR] {word}: {e}")
                continue
        
        # Insert batch into database
        if records:
            try:
                response = supabase.table('language_vocabulary').insert(records).execute()
                total_added += len(records)
                print(f"  Inserted {len(records)} words into database")
            except Exception as e:
                print(f"  Error inserting batch: {e}")
    
    return total_added

def main():
    print("Loading Spanish vocabulary selection...", flush=True)
    print("="*60, flush=True)
    
    # Load vocabulary selection
    try:
        with open('spanish_vocabulary_selection.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: spanish_vocabulary_selection.json not found")
        print("Please run sample_spanish_vocabulary.py first")
        return
    
    vocabulary = data['vocabulary']
    
    # Load existing words from database
    print("\nLoading existing words from database...")
    existing_words = load_existing_words()
    print(f"Found {len(existing_words)} existing words in database")
    
    # Initialize translator
    print("\nInitializing translator...")
    translator = GoogleTranslator(source='es', target='en')
    
    # Process each difficulty level in order
    difficulty_order = ['Basic', 'Elementary', 'Intermediate', 'Advanced', 'Expert']
    total_added = 0
    
    for difficulty in difficulty_order:
        if difficulty in vocabulary:
            words = vocabulary[difficulty]
            added = process_difficulty_level(difficulty, words, existing_words, translator)
            total_added += added
            
            # Save progress
            with open(f'spanish_insertion_progress_{difficulty}.txt', 'w') as f:
                f.write(f"Completed {difficulty}: {added} words added\n")
                f.write(f"Total so far: {total_added} words\n")
    
    # Final summary
    print("\n" + "="*60)
    print("INSERTION COMPLETE")
    print("="*60)
    print(f"Total words added: {total_added}")
    print(f"Total words now in database: {len(existing_words)}")
    
    # Verify final counts
    print("\nVerifying database counts...")
    response = supabase.table('language_vocabulary').select('difficulty_id').eq('language', 'es').execute()
    
    counts = {}
    for record in response.data:
        diff_id = record['difficulty_id']
        counts[diff_id] = counts.get(diff_id, 0) + 1
    
    print("\nFinal distribution:")
    for level in sorted(counts.keys()):
        level_name = ['', 'Basic', 'Elementary', 'Intermediate', 'Advanced', 'Expert'][level]
        print(f"  Level {level} ({level_name}): {counts[level]} words")

if __name__ == "__main__":
    main()