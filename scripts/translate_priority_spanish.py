"""
Translate only the most common Spanish words (highest zipf frequency)
These are the words users are most likely to encounter
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
    print("Translating high-priority Spanish words")
    print("="*60)
    
    # Get the most common words that need translation
    print("\nFetching most common words with placeholders...")
    
    # Get words with zipf >= 4.0 (most common ~7,000 words)
    response = supabase.table('language_vocabulary') \
        .select('id, word, zipf_frequency') \
        .eq('language', 'es') \
        .eq('translation_source', 'PENDING') \
        .gte('zipf_frequency', 4.0) \
        .order('zipf_frequency', desc=True) \
        .limit(500) \
        .execute()
    
    high_priority_words = response.data
    
    if not high_priority_words:
        print("No high-priority words need translation!")
        
        # Check lower priority
        response = supabase.table('language_vocabulary') \
            .select('id, word, zipf_frequency') \
            .eq('language', 'es') \
            .eq('translation_source', 'PENDING') \
            .gte('zipf_frequency', 3.5) \
            .order('zipf_frequency', desc=True) \
            .limit(500) \
            .execute()
        
        high_priority_words = response.data
        
        if not high_priority_words:
            print("All common words have been translated!")
            return
    
    print(f"Found {len(high_priority_words)} high-priority words to translate")
    print(f"Zipf range: {high_priority_words[-1]['zipf_frequency']:.1f} - {high_priority_words[0]['zipf_frequency']:.1f}")
    
    # Initialize translator
    print("\nInitializing translator...")
    translator = GoogleTranslator(source='es', target='en')
    
    # Process words
    successful = 0
    failed = 0
    examples = []
    
    print("\nTranslating...")
    for i, record in enumerate(high_priority_words):
        word = record['word']
        cleaned = clean_word_for_translation(word)
        
        # Progress indicator
        if i % 50 == 0 and i > 0:
            print(f"  Progress: {i}/{len(high_priority_words)} words processed...")
        
        try:
            # Rate limiting
            time.sleep(0.03)
            
            # Translate
            translation = translator.translate(cleaned)
            
            # Always update if we got a translation (even if it's the same)
            # This marks it as processed rather than PENDING
            if translation:
                # Update database
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
                if len(examples) < 10:
                    if translation.lower() != cleaned.lower():
                        examples.append((word, translation, record['zipf_frequency']))
                    else:
                        examples.append((word, f"{translation} (same)", record['zipf_frequency']))
            else:
                failed += 1
                
        except Exception as e:
            if 'Too Many Requests' in str(e):
                print(f"\nRate limit hit after {successful} translations. Waiting 10 seconds...")
                time.sleep(10)
            else:
                print(f"\nError translating '{cleaned}': {e}")
            failed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("PRIORITY TRANSLATION COMPLETE")
    print(f"Successfully translated: {successful} words")
    print(f"Failed: {failed} words")
    
    if examples:
        print("\nExample translations:")
        for word, trans, zipf in examples:
            print(f"  {word} -> {trans} (zipf: {zipf:.1f})")
    
    # Check remaining high-priority words
    response = supabase.table('language_vocabulary') \
        .select('count', count='exact') \
        .eq('language', 'es') \
        .eq('translation_source', 'PENDING') \
        .gte('zipf_frequency', 4.0) \
        .execute()
    
    print(f"\nRemaining high-priority words (zipf >= 4.0): {response.count:,}")
    
    response2 = supabase.table('language_vocabulary') \
        .select('count', count='exact') \
        .eq('language', 'es') \
        .eq('translation_source', 'PENDING') \
        .execute()
    
    print(f"Total remaining placeholders: {response2.count:,}")

if __name__ == "__main__":
    main()