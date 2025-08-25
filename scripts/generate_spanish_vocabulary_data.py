"""
Generate Spanish vocabulary data with translations and definitions
Uses deep-translator for free batch translations
"""

import json
import time
import os
from typing import Dict, List
import sys

# Install required packages
required_packages = ['deep-translator']
for package in required_packages:
    try:
        __import__(package.replace('-', '_'))
    except ImportError:
        print(f"Installing {package}...")
        os.system(f"{sys.executable} -m pip install {package}")

from deep_translator import GoogleTranslator

def get_phonetic_spanish(word: str) -> str:
    """
    Generate a simple phonetic guide for Spanish pronunciation
    This is a basic approximation for English speakers
    """
    phonetic = word.lower()
    
    # Spanish pronunciation rules for English speakers
    replacements = [
        ('que', 'keh'),
        ('qui', 'kee'),
        ('gue', 'geh'),
        ('gui', 'gee'),
        ('ce', 'seh'),
        ('ci', 'see'),
        ('ge', 'heh'),
        ('gi', 'hee'),
        ('j', 'h'),
        ('ll', 'y'),
        ('ñ', 'ny'),
        ('rr', 'rr'),  # rolled r
        ('h', ''),  # silent h
        ('v', 'b'),  # v sounds like b
        ('z', 'th'),  # in Spain Spanish
        ('á', 'AH'),
        ('é', 'EH'),
        ('í', 'EE'),
        ('ó', 'OH'),
        ('ú', 'OO'),
    ]
    
    for old, new in replacements:
        phonetic = phonetic.replace(old, new)
    
    return phonetic

def get_part_of_speech(word: str, base_form: str = None) -> str:
    """
    Guess part of speech based on Spanish word patterns
    """
    word = word.lower()
    
    # Verb infinitives
    if word.endswith('ar') or word.endswith('er') or word.endswith('ir'):
        return 'verb'
    
    # Adverbs
    if word.endswith('mente'):
        return 'adverb'
    
    # Nouns with common endings
    if any(word.endswith(ending) for ending in ['ción', 'sión', 'dad', 'tad', 'ez', 'eza', 'ismo', 'miento']):
        return 'noun'
    
    # Adjectives with common endings
    if any(word.endswith(ending) for ending in ['oso', 'osa', 'able', 'ible', 'ivo', 'iva']):
        return 'adjective'
    
    # Gender/number variations suggest noun or adjective
    if any(word.endswith(ending) for ending in ['o', 'a', 'os', 'as', 'e', 'es']):
        return 'noun/adjective'
    
    return 'unknown'

def generate_memory_tip(word: str, translation: str) -> str:
    """
    Generate memory tips for Spanish words
    """
    tips = []
    
    # Check for cognates (similar to English)
    if len(word) > 4:
        # Simple cognate detection
        if any([
            word.startswith(translation[:3].lower()),
            translation.lower().startswith(word[:3]),
            word.replace('ción', 'tion') in translation.lower(),
            word.replace('dad', 'ty') in translation.lower(),
        ]):
            tips.append(f"Cognate: similar to English '{translation}'")
    
    # Common patterns
    if word.endswith('ción'):
        tips.append("Ends in -ción (like -tion in English)")
    elif word.endswith('mente'):
        tips.append("Ends in -mente (like -ly in English)")
    elif word.endswith('ismo'):
        tips.append("Ends in -ismo (like -ism in English)")
    
    return '; '.join(tips) if tips else None

def process_batch(words_batch: List[Dict], translator) -> List[Dict]:
    """
    Process a batch of words with translations
    """
    processed = []
    
    for word_data in words_batch:
        word = word_data['word']
        
        try:
            # Translate the word
            translation = translator.translate(word)
            
            # Generate additional data
            phonetic = get_phonetic_spanish(word)
            pos = get_part_of_speech(word, word_data.get('base_form'))
            memory_tip = generate_memory_tip(word, translation)
            
            # Create vocabulary entry
            entry = {
                'word': word,
                'base_form': word_data.get('base_form'),
                'zipf': word_data['zipf'],
                'english_translation': translation,
                'pronunciation_guide': phonetic,
                'part_of_speech': pos,
                'memory_tips': memory_tip,
                'translation_source': 'GoogleTranslator',
                'definition_source': 'GoogleTranslator'
            }
            
            processed.append(entry)
            print(f"  Processed: {word} -> {translation}")
            
            # Small delay to avoid rate limiting
            time.sleep(0.1)
            
        except Exception as e:
            print(f"  Error processing {word}: {e}")
            # Add word without translation
            processed.append({
                'word': word,
                'base_form': word_data.get('base_form'),
                'zipf': word_data['zipf'],
                'error': str(e)
            })
    
    return processed

def main():
    print("Generating Spanish vocabulary data with translations...")
    print("=" * 60)
    
    # Load the vocabulary selection
    with open('spanish_vocabulary_selection.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    vocabulary = data['vocabulary']
    
    # Initialize translator
    translator = GoogleTranslator(source='es', target='en')
    
    # Process each difficulty level
    all_processed = {}
    
    for difficulty, words in vocabulary.items():
        print(f"\nProcessing {difficulty} level ({len(words)} words)...")
        print("-" * 40)
        
        processed_words = []
        batch_size = 10
        
        # Process in small batches with progress saving
        for i in range(0, len(words), batch_size):
            batch = words[i:i+batch_size]
            print(f"\nBatch {i//batch_size + 1}/{(len(words)-1)//batch_size + 1}")
            
            batch_results = process_batch(batch, translator)
            processed_words.extend(batch_results)
            
            # Save progress every 50 words
            if (i + batch_size) % 50 == 0 or i + batch_size >= len(words):
                temp_file = f'spanish_vocab_{difficulty}_progress.json'
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(processed_words, f, ensure_ascii=False, indent=2)
                print(f"  Progress saved to {temp_file}")
        
        all_processed[difficulty] = processed_words
    
    # Save final results
    output = {
        'metadata': data['metadata'],
        'vocabulary': all_processed,
        'total_processed': sum(len(words) for words in all_processed.values())
    }
    
    output_file = 'spanish_vocabulary_with_translations.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n" + "=" * 60)
    print(f"Completed! Processed {output['total_processed']} words")
    print(f"Results saved to {output_file}")
    
    # Print sample results
    print("\n" + "=" * 60)
    print("SAMPLE RESULTS:")
    print("-" * 40)
    
    for difficulty in ["Basic", "Elementary"]:
        if difficulty in all_processed and all_processed[difficulty]:
            print(f"\n{difficulty} samples:")
            for entry in all_processed[difficulty][:3]:
                if 'english_translation' in entry:
                    print(f"  {entry['word']:15} -> {entry['english_translation']:20} [{entry['pronunciation_guide']}]")

if __name__ == "__main__":
    main()