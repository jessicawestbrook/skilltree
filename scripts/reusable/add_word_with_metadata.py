"""
Add words to spelling_words table with automatic metadata generation
Includes: frequency, difficulty predictions, definitions, examples, etc.

USAGE:
    python scripts/reusable/add_word_with_metadata.py "word1" "word2" "word3"
    python scripts/reusable/add_word_with_metadata.py --file word_list.txt
"""

import os
import sys
import json
import argparse
import uuid
from typing import List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Install required packages if needed
required_packages = ['wordfreq', 'supabase', 'anthropic', 'xgboost', 'numpy']
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        os.system(f"{sys.executable} -m pip install {package}")

from wordfreq import zipf_frequency
from supabase import create_client
from anthropic import Anthropic
import xgboost as xgb
import numpy as np

# ============================================================================
# CONFIGURATION
# ============================================================================

XGBOOST_MODEL_PATH = 'xgboost_spelling_model.json'
FEATURE_NAMES_PATH = 'feature_names.json'

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_supabase_client():
    """Create Supabase client"""
    url = os.getenv('REACT_APP_SUPABASE_URL')
    key = os.getenv('REACT_APP_SUPABASE_ANON_KEY')
    if not url or not key:
        raise ValueError("Missing Supabase credentials in .env.local")
    return create_client(url, key)

def get_anthropic_client():
    """Create Anthropic client for Claude API"""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("Missing ANTHROPIC_API_KEY in .env.local")
    return Anthropic(api_key=api_key)

def calculate_word_frequency(word: str) -> float:
    """Get Zipf frequency for a word"""
    return zipf_frequency(word.lower(), 'en')

def calculate_vocabulary_difficulty(frequency: float) -> int:
    """
    Calculate vocabulary difficulty based on frequency bins
    1 = Basic (6+), 2 = Elementary (5-6), 3 = Intermediate (3-5), 
    4 = Advanced (2-3), 5 = Expert (0-2)
    """
    if frequency >= 6:
        return 1  # Basic - very common words
    elif frequency >= 5:
        return 2  # Elementary - common words
    elif frequency >= 3:
        return 3  # Intermediate - moderate/uncommon words
    elif frequency >= 2:
        return 4  # Advanced - rare words
    else:
        return 5  # Expert - very rare words

def extract_features(word: str, freq: float = None) -> Dict[str, float]:
    """Extract features for spelling difficulty prediction"""
    w = word.lower()
    
    if freq is None:
        freq = calculate_word_frequency(w)
    
    features = {
        'zipf_frequency': freq,
        'is_very_common': 1 if freq >= 6 else 0,
        'is_common': 1 if 4 <= freq < 6 else 0,
        'is_uncommon': 1 if 2 <= freq < 4 else 0,
        'is_rare': 1 if freq < 2 else 0,
        'length': len(w),
        'length_squared': len(w) ** 2,
        'is_short': 1 if len(w) <= 4 else 0,
        'is_medium': 1 if 5 <= len(w) <= 8 else 0,
        'is_long': 1 if len(w) >= 9 else 0,
        'vowel_count': len([c for c in w if c in 'aeiou']),
        'consonant_count': len([c for c in w if c in 'bcdfghjklmnpqrstvwxyz']),
        'vowel_ratio': len([c for c in w if c in 'aeiou']) / len(w) if len(w) > 0 else 0,
        'consecutive_vowels': len([i for i in range(len(w)-1) if w[i] in 'aeiou' and w[i+1] in 'aeiou']),
        'consecutive_consonants': len([i for i in range(len(w)-2) if all(c not in 'aeiou' for c in w[i:i+3])]),
        'has_double': 1 if any(w[i] == w[i+1] for i in range(len(w)-1)) else 0,
        'double_count': sum(1 for i in range(len(w)-1) if w[i] == w[i+1]),
        'has_silent_e': 1 if w.endswith('e') and len(w) > 2 else 0,
        'has_gh': 1 if 'gh' in w else 0,
        'has_silent_letters': 1 if any(p in w for p in ['kn', 'gn', 'wr', 'mb', 'ps', 'pn']) else 0,
        'has_ough': 1 if 'ough' in w else 0,
        'has_eigh': 1 if 'eigh' in w else 0,
        'has_augh': 1 if 'augh' in w else 0,
        'has_ph': 1 if 'ph' in w else 0,
        'has_tion': 1 if 'tion' in w else 0,
        'has_sion': 1 if 'sion' in w else 0,
        'has_common_prefix': 1 if any(w.startswith(p) for p in ['un', 're', 'in', 'dis', 'pre', 'non']) else 0,
        'has_common_suffix': 1 if any(w.endswith(s) for s in ['ing', 'ed', 'er', 'est', 'ly', 'ness', 'ment']) else 0,
        'avg_letter_commonness': sum(zipf_frequency(c, 'en') for c in w) / len(w) if len(w) > 0 else 0,
        'syllable_count': max(1, len([c for c in w if c in 'aeiou']) - (1 if w.endswith('e') else 0))
    }
    
    return features

def predict_spelling_difficulty(word: str, freq: float = None) -> int:
    """Predict spelling difficulty using XGBoost model"""
    try:
        # Load model and feature names
        model = xgb.XGBClassifier()
        model.load_model(XGBOOST_MODEL_PATH)
        
        # Extract features
        features = extract_features(word, freq)
        X = np.array([list(features.values())])
        
        # Predict (model outputs 0-4, we need 1-5)
        prediction = model.predict(X)[0] + 1
        return int(prediction)
        
    except FileNotFoundError:
        print(f"Warning: XGBoost model not found at {XGBOOST_MODEL_PATH}")
        print("Using fallback difficulty calculation based on length and frequency")
        # Fallback calculation
        if freq >= 5:
            return 2  # Common words are easier
        elif freq >= 3:
            return 3  # Moderate difficulty
        elif len(word) <= 5:
            return 3  # Short rare words
        elif len(word) <= 8:
            return 4  # Medium rare words
        else:
            return 5  # Long rare words

def generate_word_content(word: str, anthropic_client) -> Dict[str, Any]:
    """Generate definition, examples, and other content using Claude API"""
    
    prompt = f"""For the word "{word}", provide the following in JSON format:
    
    {{
        "definition": "a clear, concise definition suitable for learners",
        "part_of_speech": "noun/verb/adjective/adverb/etc",
        "example_sentence": "a simple example sentence using the word",
        "etymology": "brief origin of the word (1-2 sentences)",
        "synonyms": ["list", "of", "3-5", "synonyms"],
        "difficulty_notes": "any notes about why this word might be difficult to spell",
        "mnemonic": "a memory aid for spelling this word correctly"
    }}
    
    Provide ONLY valid JSON, no additional text."""
    
    try:
        response = anthropic_client.messages.create(
            model="claude-3-haiku-20240307",  # Using Haiku for efficiency
            max_tokens=500,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text.strip()
        # Parse JSON response
        return json.loads(content)
        
    except Exception as e:
        print(f"Warning: Could not generate content for '{word}': {e}")
        # Return default structure
        return {
            "definition": None,
            "part_of_speech": None,
            "example_sentence": None,
            "etymology": None,
            "synonyms": [],
            "difficulty_notes": None,
            "mnemonic": None
        }

def check_word_exists(word: str, supabase_client) -> bool:
    """Check if word already exists in database"""
    response = supabase_client.table('spelling_words').select('id').eq('word', word).execute()
    return len(response.data) > 0

def add_word_to_database(word_data: Dict[str, Any], supabase_client) -> bool:
    """Add word with all metadata to database"""
    try:
        response = supabase_client.table('spelling_words').insert(word_data).execute()
        return True
    except Exception as e:
        print(f"Error adding word '{word_data['word']}': {e}")
        return False

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def process_word(word: str, supabase_client, anthropic_client, skip_existing: bool = True) -> Dict[str, Any]:
    """Process a single word and add to database"""
    
    word = word.strip().lower()
    
    # Check if word already exists
    if skip_existing and check_word_exists(word, supabase_client):
        print(f"⚠️  Word '{word}' already exists in database, skipping...")
        return None
    
    print(f"Processing word: '{word}'")
    
    # Calculate frequency
    frequency = calculate_word_frequency(word)
    print(f"  Frequency: {frequency:.2f}")
    
    # Calculate difficulties
    vocab_difficulty = calculate_vocabulary_difficulty(frequency)
    spelling_difficulty = predict_spelling_difficulty(word, frequency)
    print(f"  Vocabulary difficulty: {vocab_difficulty}")
    print(f"  Spelling difficulty: {spelling_difficulty}")
    
    # Generate content with Claude
    print("  Generating content with Claude API...")
    content = generate_word_content(word, anthropic_client)
    
    # Prepare database record
    word_data = {
        'id': str(uuid.uuid4()),
        'word': word,
        'frequency': frequency,
        'vocabulary_difficulty_level': vocab_difficulty,
        'spelling_difficulty_level': spelling_difficulty,
        'spelling_difficulty_calculation_method': 'XGBoost ML model v2025.01, 52% accuracy',
        'vocabulary_difficulty_calculation_method': 'Zipf frequency bins: 6+,5-6,3-5,2-3,0-2',
        'definition': content.get('definition'),
        'part_of_speech': content.get('part_of_speech'),
        'example_sentence': content.get('example_sentence'),
        'etymology': content.get('etymology'),
        'synonyms': content.get('synonyms', []),
        'difficulty_notes': content.get('difficulty_notes'),
        'mnemonic_device': content.get('mnemonic'),
        'created_at': datetime.utcnow().isoformat(),
        'source': 'auto_generated',
        'source_difficulty': None  # Will be NULL for auto-added words
    }
    
    # Add to database
    if add_word_to_database(word_data, supabase_client):
        print(f"✅ Successfully added '{word}' to database")
    else:
        print(f"❌ Failed to add '{word}' to database")
    
    return word_data

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Add words to spelling_words with automatic metadata')
    parser.add_argument('words', nargs='*', help='Words to add (space-separated)')
    parser.add_argument('--file', '-f', help='File containing words (one per line)')
    parser.add_argument('--skip-existing', default=True, action='store_true', 
                       help='Skip words that already exist (default: True)')
    parser.add_argument('--force', action='store_true', 
                       help='Add words even if they already exist')
    
    args = parser.parse_args()
    
    # Collect words to process
    words_to_add = []
    
    if args.file:
        with open(args.file, 'r') as f:
            words_to_add.extend([line.strip() for line in f if line.strip()])
    
    if args.words:
        words_to_add.extend(args.words)
    
    if not words_to_add:
        print("No words provided. Use word arguments or --file option.")
        sys.exit(1)
    
    # Initialize clients
    print("Initializing connections...")
    supabase = get_supabase_client()
    anthropic = get_anthropic_client()
    
    # Process words
    print(f"\nProcessing {len(words_to_add)} words...")
    print("=" * 60)
    
    skip_existing = not args.force
    results = []
    
    for i, word in enumerate(words_to_add, 1):
        print(f"\n[{i}/{len(words_to_add)}] ", end="")
        result = process_word(word, supabase, anthropic, skip_existing)
        if result:
            results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print(f"SUMMARY: Added {len(results)} words to database")
    
    # Save results to file
    if results:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'added_words_{timestamp}.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Results saved to: {output_file}")

if __name__ == "__main__":
    main()