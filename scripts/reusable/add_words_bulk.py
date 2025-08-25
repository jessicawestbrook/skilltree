"""
Bulk add words to spelling_words table with frequency and difficulty predictions
This version doesn't use Claude API - for faster bulk additions

USAGE:
    python scripts/reusable/add_words_bulk.py --file word_list.txt
    python scripts/reusable/add_words_bulk.py word1 word2 word3
"""

import os
import sys
import json
import argparse
import uuid
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Install required packages if needed
for package in ['wordfreq', 'supabase', 'xgboost', 'numpy']:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        os.system(f"{sys.executable} -m pip install {package}")

from wordfreq import zipf_frequency
from supabase import create_client
import xgboost as xgb
import numpy as np

def get_supabase_client():
    """Create Supabase client"""
    url = os.getenv('REACT_APP_SUPABASE_URL')
    key = os.getenv('REACT_APP_SUPABASE_ANON_KEY')
    return create_client(url, key)

def calculate_vocabulary_difficulty(frequency: float) -> int:
    """Calculate vocabulary difficulty based on frequency bins"""
    if frequency >= 6:
        return 1  # Basic
    elif frequency >= 5:
        return 2  # Elementary
    elif frequency >= 3:
        return 3  # Intermediate
    elif frequency >= 2:
        return 4  # Advanced
    else:
        return 5  # Expert

def extract_features(word: str, freq: float) -> List[float]:
    """Extract features for spelling difficulty prediction"""
    w = word.lower()
    
    features = [
        freq,  # zipf_frequency
        1 if freq >= 6 else 0,  # is_very_common
        1 if 4 <= freq < 6 else 0,  # is_common
        1 if 2 <= freq < 4 else 0,  # is_uncommon
        1 if freq < 2 else 0,  # is_rare
        len(w),  # length
        len(w) ** 2,  # length_squared
        1 if len(w) <= 4 else 0,  # is_short
        1 if 5 <= len(w) <= 8 else 0,  # is_medium
        1 if len(w) >= 9 else 0,  # is_long
        len([c for c in w if c in 'aeiou']),  # vowel_count
        len([c for c in w if c in 'bcdfghjklmnpqrstvwxyz']),  # consonant_count
        len([c for c in w if c in 'aeiou']) / len(w) if len(w) > 0 else 0,  # vowel_ratio
        len([i for i in range(len(w)-1) if w[i] in 'aeiou' and w[i+1] in 'aeiou']),  # consecutive_vowels
        len([i for i in range(len(w)-2) if all(c not in 'aeiou' for c in w[i:i+3])]),  # consecutive_consonants
        1 if any(w[i] == w[i+1] for i in range(len(w)-1)) else 0,  # has_double
        sum(1 for i in range(len(w)-1) if w[i] == w[i+1]),  # double_count
        1 if w.endswith('e') and len(w) > 2 else 0,  # has_silent_e
        1 if 'gh' in w else 0,  # has_gh
        1 if any(p in w for p in ['kn', 'gn', 'wr', 'mb', 'ps', 'pn']) else 0,  # has_silent_letters
        1 if 'ough' in w else 0,  # has_ough
        1 if 'eigh' in w else 0,  # has_eigh
        1 if 'augh' in w else 0,  # has_augh
        1 if 'ph' in w else 0,  # has_ph
        1 if 'tion' in w else 0,  # has_tion
        1 if 'sion' in w else 0,  # has_sion
        1 if any(w.startswith(p) for p in ['un', 're', 'in', 'dis', 'pre', 'non']) else 0,  # has_common_prefix
        1 if any(w.endswith(s) for s in ['ing', 'ed', 'er', 'est', 'ly', 'ness', 'ment']) else 0,  # has_common_suffix
        sum(zipf_frequency(c, 'en') for c in w) / len(w) if len(w) > 0 else 0,  # avg_letter_commonness
        max(1, len([c for c in w if c in 'aeiou']) - (1 if w.endswith('e') else 0))  # syllable_count
    ]
    
    return features

def predict_spelling_difficulty(word: str, freq: float) -> int:
    """Predict spelling difficulty using XGBoost model or fallback"""
    try:
        model = xgb.XGBClassifier()
        model.load_model('xgboost_spelling_model.json')
        
        features = extract_features(word, freq)
        X = np.array([features])
        prediction = model.predict(X)[0] + 1
        return int(prediction)
        
    except:
        # Fallback calculation
        if freq >= 5:
            return 2
        elif freq >= 3:
            return 3
        elif len(word) <= 5:
            return 3
        elif len(word) <= 8:
            return 4
        else:
            return 5

def process_words_batch(words: List[str], supabase_client):
    """Process a batch of words"""
    
    # Get existing words to avoid duplicates
    existing = supabase_client.table('spelling_words').select('word').execute()
    existing_words = {w['word'].lower() for w in existing.data}
    
    # Process new words
    new_words = []
    skipped = 0
    
    for word in words:
        word = word.strip().lower()
        
        if not word or word in existing_words:
            skipped += 1
            continue
        
        # Calculate metadata
        freq = zipf_frequency(word, 'en')
        vocab_diff = calculate_vocabulary_difficulty(freq)
        spell_diff = predict_spelling_difficulty(word, freq)
        
        new_words.append({
            'id': str(uuid.uuid4()),
            'word': word,
            'frequency': freq,
            'vocabulary_difficulty_level': vocab_diff,
            'spelling_difficulty_level': spell_diff,
            'spelling_difficulty_calculation_method': 'XGBoost ML model v2025.01, 52% accuracy',
            'vocabulary_difficulty_calculation_method': 'Zipf frequency bins: 6+,5-6,3-5,2-3,0-2',
            'source': 'bulk_import',
            'created_at': datetime.utcnow().isoformat()
        })
        
        existing_words.add(word)  # Prevent duplicates in this batch
    
    # Insert in batches
    if new_words:
        batch_size = 100
        for i in range(0, len(new_words), batch_size):
            batch = new_words[i:i+batch_size]
            try:
                supabase_client.table('spelling_words').insert(batch).execute()
                print(f"  Inserted batch {i//batch_size + 1}: {len(batch)} words")
            except Exception as e:
                print(f"  Error inserting batch: {e}")
    
    return len(new_words), skipped

def main():
    parser = argparse.ArgumentParser(description='Bulk add words with automatic difficulty calculation')
    parser.add_argument('words', nargs='*', help='Words to add')
    parser.add_argument('--file', '-f', help='File with words (one per line)')
    
    args = parser.parse_args()
    
    # Collect words
    words_to_add = []
    
    if args.file:
        with open(args.file, 'r') as f:
            words_to_add.extend([line.strip() for line in f if line.strip()])
    
    if args.words:
        words_to_add.extend(args.words)
    
    if not words_to_add:
        print("No words provided.")
        sys.exit(1)
    
    print(f"Processing {len(words_to_add)} words...")
    
    # Process
    supabase = get_supabase_client()
    added, skipped = process_words_batch(words_to_add, supabase)
    
    print(f"\nSummary:")
    print(f"  Added: {added} words")
    print(f"  Skipped (duplicates): {skipped} words")
    
    # Save record
    if added > 0:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f'bulk_add_log_{timestamp}.txt'
        with open(log_file, 'w') as f:
            f.write(f"Added {added} words on {datetime.now()}\n")
            f.write(f"Skipped {skipped} duplicates\n")
        print(f"Log saved to: {log_file}")

if __name__ == "__main__":
    main()