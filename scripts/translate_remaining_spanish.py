"""
Simple script to translate remaining Spanish words
Processes any words with PENDING translation status
"""

import os
import sys
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

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: Missing environment variables")
    sys.exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def clean_word_for_translation(word):
    """Remove articles and clean word for translation"""
    prefixes = ['el ', 'la ', 'los ', 'las ', 'un ', 'una ', 'unos ', 'unas ']
    cleaned = word
    for prefix in prefixes:
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):]
            break
    return cleaned

def main():
    print("Translating remaining Spanish words")
    print("="*60)
    
    # Get count of pending words
    response = supabase.table('language_vocabulary') \
        .select('count', count='exact') \
        .eq('language', 'es') \
        .eq('translation_source', 'PENDING') \
        .execute()
    
    total_pending = response.count
    print(f"Total words needing translation: {total_pending:,}")
    
    if total_pending == 0:
        print("No words need translation!")
        return
    
    # Get a batch of words to translate (prioritize by frequency)
    print("\nFetching batch of words...")
    response = supabase.table('language_vocabulary') \
        .select('id, word, part_of_speech, zipf_frequency') \
        .eq('language', 'es') \
        .eq('translation_source', 'PENDING') \
        .order('zipf_frequency', desc=True) \
        .limit(100) \
        .execute()
    
    words_to_translate = response.data
    
    if not words_to_translate:
        print("Could not fetch words to translate")
        return
    
    print(f"Processing batch of {len(words_to_translate)} words...")
    print(f"Zipf range: {words_to_translate[-1]['zipf_frequency']:.1f} - {words_to_translate[0]['zipf_frequency']:.1f}")
    
    # Initialize translator
    translator = GoogleTranslator(source='es', target='en')
    
    successful = 0
    failed = 0
    examples = []
    
    for i, record in enumerate(words_to_translate):
        word = record['word']
        cleaned = clean_word_for_translation(word)
        
        # Progress indicator
        if (i + 1) % 10 == 0:
            print(f"  Progress: {i + 1}/{len(words_to_translate)}")
        
        try:
            # Small delay to avoid rate limiting
            time.sleep(0.05)
            
            # Translate
            translation = translator.translate(cleaned)
            
            # For verbs, add "to" if needed
            if translation and record.get('part_of_speech') == 'verb':
                if not translation.lower().startswith('to '):
                    # Check if it's not a conjugated form
                    conjugated_starts = ['i ', 'you ', 'he ', 'she ', 'it ', 'we ', 'they ']
                    if not any(translation.lower().startswith(p) for p in conjugated_starts):
                        translation = f"to {translation}"
            
            # Always update if we got a translation (marks as processed)
            if translation:
                supabase.table('language_vocabulary') \
                    .update({
                        'english_translation': translation,
                        'definition_english': translation,
                        'translation_source': 'GoogleTranslator',
                        'definition_source': 'GoogleTranslator'
                    }) \
                    .eq('id', record['id']) \
                    .execute()
                
                successful += 1
                
                # Save examples
                if len(examples) < 5:
                    if translation.lower() != cleaned.lower():
                        examples.append(f"{word} -> {translation}")
                    else:
                        examples.append(f"{word} -> {translation} (same)")
            else:
                failed += 1
                print(f"  No translation for: {word}")
                
        except Exception as e:
            print(f"  Error translating '{word}': {e}")
            failed += 1
            
            # If we hit rate limit, wait longer
            if 'Too Many Requests' in str(e):
                print("  Rate limit hit, waiting 30 seconds...")
                time.sleep(30)
    
    # Summary
    print(f"\n{'='*60}")
    print("BATCH COMPLETE")
    print(f"Successfully translated: {successful}")
    print(f"Failed: {failed}")
    
    if examples:
        print("\nExample translations:")
        for ex in examples:
            print(f"  {ex}")
    
    # Check remaining
    response = supabase.table('language_vocabulary') \
        .select('count', count='exact') \
        .eq('language', 'es') \
        .eq('translation_source', 'PENDING') \
        .execute()
    
    print(f"\nRemaining words to translate: {response.count:,}")
    print("\nRun this script again to continue translating.")

if __name__ == "__main__":
    main()