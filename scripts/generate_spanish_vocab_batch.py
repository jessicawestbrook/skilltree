"""
Generate Spanish vocabulary data in batches
Processes vocabulary with translations and saves to CSV for database import
"""

import json
import csv
import time
import uuid
from datetime import datetime
from deep_translator import GoogleTranslator

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

def get_phonetic_guide(word):
    """Simple phonetic guide for Spanish"""
    phonetic = word.lower()
    replacements = [
        ('que', 'keh'), ('qui', 'kee'),
        ('ce', 'seh'), ('ci', 'see'),
        ('ge', 'heh'), ('gi', 'hee'),
        ('ll', 'y'), ('ñ', 'ny'),
        ('j', 'h'), ('v', 'b'),
        ('á', 'AH'), ('é', 'EH'), ('í', 'EE'), ('ó', 'OH'), ('ú', 'OO')
    ]
    for old, new in replacements:
        phonetic = phonetic.replace(old, new)
    return phonetic

def get_part_of_speech(word):
    """Guess part of speech"""
    if word.endswith(('ar', 'er', 'ir')):
        return 'verb'
    elif word.endswith('mente'):
        return 'adverb'
    elif word.endswith(('ción', 'sión', 'dad', 'tad', 'miento')):
        return 'noun'
    elif word.endswith(('oso', 'osa', 'able', 'ible')):
        return 'adjective'
    else:
        return 'noun'

def process_vocabulary_batch(words, translator, batch_num):
    """Process a batch of words"""
    results = []
    
    for i, word_data in enumerate(words):
        word = word_data['word']
        
        try:
            # Translate
            translation = translator.translate(word)
            
            # Skip if translation is same as original (usually means not translated)
            if translation.lower() == word.lower():
                translation = None
            
            # Generate example sentence for common words
            example = None
            if word_data['zipf'] >= 4.5:
                example_es = f"Necesito {word}." if get_part_of_speech(word) == 'verb' else f"El {word} es importante."
                try:
                    example_en = translator.translate(example_es)
                    example = f"{example_es}|{example_en}"
                except:
                    pass
            
            # Create record
            record = {
                'id': str(uuid.uuid4()),
                'language': 'es',
                'word': word,
                'base_form': word_data.get('base_form'),
                'zipf_frequency': word_data['zipf'],
                'difficulty_id': get_difficulty_id(word_data['zipf']),
                'english_translation': translation,
                'pronunciation_guide': get_phonetic_guide(word),
                'part_of_speech': get_part_of_speech(word),
                'definition_english': translation,  # Simple definition
                'example_sentence': example_es if example else None,
                'example_sentence_translation': example_en if example else None,
                'memory_tips': f"Frequency rank: top {i+1 + batch_num*100}",
                'translation_source': 'GoogleTranslator',
                'definition_source': 'GoogleTranslator',
                'created_at': datetime.utcnow().isoformat()
            }
            
            results.append(record)
            
            if (i + 1) % 10 == 0:
                print(f"  Processed {i+1}/{len(words)} words in batch {batch_num+1}")
            
            # Rate limit
            time.sleep(0.2)
            
        except Exception as e:
            print(f"  Error with {word}: {e}")
            continue
    
    return results

def main():
    print("Generating Spanish vocabulary with translations...")
    print("=" * 60)
    
    # Load vocabulary
    with open('spanish_vocabulary_selection.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Initialize translator
    translator = GoogleTranslator(source='es', target='en')
    
    # Process all words
    all_records = []
    batch_size = 50
    batch_num = 0
    
    for difficulty in ['Basic', 'Elementary', 'Intermediate', 'Advanced', 'Expert']:
        words = data['vocabulary'].get(difficulty, [])
        
        print(f"\nProcessing {difficulty} level: {len(words)} words")
        print("-" * 40)
        
        # Process in batches
        for i in range(0, len(words), batch_size):
            batch = words[i:min(i+batch_size, len(words))]
            print(f"\nBatch {batch_num+1} ({difficulty}): {len(batch)} words")
            
            batch_results = process_vocabulary_batch(batch, translator, batch_num)
            all_records.extend(batch_results)
            
            # Save progress
            with open(f'spanish_vocab_progress_{batch_num}.csv', 'w', newline='', encoding='utf-8') as f:
                if batch_results:
                    writer = csv.DictWriter(f, fieldnames=batch_results[0].keys())
                    writer.writeheader()
                    writer.writerows(batch_results)
            
            print(f"  Saved batch {batch_num+1} ({len(batch_results)} records)")
            batch_num += 1
            
            # Longer pause between batches
            if i + batch_size < len(words):
                print("  Pausing before next batch...")
                time.sleep(2)
    
    # Save all records to final CSV
    output_file = 'spanish_vocabulary_final.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        if all_records:
            writer = csv.DictWriter(f, fieldnames=all_records[0].keys())
            writer.writeheader()
            writer.writerows(all_records)
    
    print(f"\n" + "=" * 60)
    print(f"COMPLETE! Generated {len(all_records)} vocabulary records")
    print(f"Saved to {output_file}")
    
    # Show summary
    difficulty_counts = {}
    for record in all_records:
        diff_id = record['difficulty_id']
        diff_name = ['', 'Basic', 'Elementary', 'Intermediate', 'Advanced', 'Expert'][diff_id]
        difficulty_counts[diff_name] = difficulty_counts.get(diff_name, 0) + 1
    
    print("\nRecords by difficulty:")
    for diff in ['Basic', 'Elementary', 'Intermediate', 'Advanced', 'Expert']:
        if diff in difficulty_counts:
            print(f"  {diff:15} {difficulty_counts[diff]:5} words")

if __name__ == "__main__":
    main()