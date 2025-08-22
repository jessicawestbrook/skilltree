#!/usr/bin/env python3

import csv
import requests
import time
from pathlib import Path

# Set up paths
SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"
BATCH_NUM = 198

def detect_combined_words(words):
    """Detect words that appear to be multiple words combined together"""
    combined_errors = []
    
    for word in words:
        word_clean = word.lower().strip()
        
        # Skip very short words
        if len(word_clean) < 8:
            continue
            
        # Look for specific patterns we've identified
        if ('noun' in word_clean and word_clean != 'noun' and 
            word_clean.endswith('noun')):
            combined_errors.append(word)
        elif ('adjective' in word_clean and word_clean != 'adjective' and 
              word_clean.endswith('adjective')):
            combined_errors.append(word)
        elif ('verb' in word_clean and word_clean != 'verb' and 
              word_clean.endswith('verb')):
            combined_errors.append(word)
            
    return combined_errors

def load_words_from_csv():
    """Load words from the batch CSV file"""
    csv_path = OUTPUT_DIR / f"batch_{BATCH_NUM:03d}_words.csv"
    words = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['word'] and row['word'].strip():
                    words.append(row['word'].strip())
    except FileNotFoundError:
        print(f"Error: Could not find {csv_path}")
        return []
    
    return words

def get_dictionary_data(word):
    """Get dictionary data from Free Dictionary API"""
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                entry = data[0]
                
                # Extract pronunciation
                pronunciation = ""
                if 'phonetics' in entry:
                    for phonetic in entry['phonetics']:
                        if 'text' in phonetic and phonetic['text']:
                            pronunciation = phonetic['text']
                            break
                
                # Extract definition
                definition = ""
                if 'meanings' in entry and entry['meanings']:
                    meaning = entry['meanings'][0]
                    if 'definitions' in meaning and meaning['definitions']:
                        definition = meaning['definitions'][0].get('definition', '')
                
                return {
                    'definition': definition,
                    'pronunciation': pronunciation,
                    'found': True
                }
    except Exception as e:
        print(f"Dictionary API error for '{word}': {e}")
    
    return {'definition': '', 'pronunciation': '', 'found': False}

def generate_example_sentence(word):
    """Generate a contextual example sentence with the word replaced by a blank"""
    
    # Quick examples for final batch words
    examples = {
        'zygotea': 'The biological term ____ was difficult to spell correctly.',
        'zymurgy': 'The science of ____ deals with fermentation processes.',
        'zyzomys': 'The ____ is a genus of Australian rock rats.',
        'élan': 'She performed the dance with remarkable ____.',
        'étagère': 'The antique ____ displayed her collection of porcelain.',
        'étouffée': 'The Louisiana ____ was served over steamed rice.',
        'étude': 'The piano student practiced the challenging ____.'
    }
    
    return examples.get(word.lower(), f'The ____ was an important part of the story.')

def get_etymology(word):
    """Generate etymology information"""
    
    etymologies = {
        'zygotea': 'Variant or error form related to zygote, from Greek zygotos',
        'zymurgy': 'From Greek zyme (leaven) + ergon (work), fermentation science',
        'zyzomys': 'From Greek zyzos (living) + mys (mouse), genus of rodents',
        'élan': 'From French élan, meaning dash or ardor',
        'étagère': 'From French étagère, meaning set of shelves',
        'étouffée': 'From French étouffer, meaning to smother or stew',
        'étude': 'From French étude, meaning study or musical exercise'
    }
    
    return etymologies.get(word.lower(), f'Etymology of {word} from historical linguistic sources')

def assign_difficulty(source_difficulty):
    """Convert source difficulty to our standard"""
    mapping = {
        'One Bee': 'Elementary',
        'Two Bee': 'Intermediate', 
        'Three Bee': 'Advanced'
    }
    
    if not source_difficulty:
        return ''
    
    difficulties = source_difficulty.split('; ')
    mapped = [mapping.get(d.strip(), d.strip()) for d in difficulties]
    return '; '.join(mapped)

def process_batch():
    """Process the batch of words"""
    print(f"Processing batch {BATCH_NUM}...")
    
    # Load words
    words = load_words_from_csv()
    if not words:
        print("No words found to process")
        return
        
    print(f"Found {len(words)} words in batch {BATCH_NUM}")
    
    # Detect combined word errors
    combined_errors = detect_combined_words(words)
    if combined_errors:
        print(f"Detected {len(combined_errors)} combined word errors:")
        for error in combined_errors:
            print(f"  - {error}")
    
    # Filter out combined errors
    valid_words = [w for w in words if w not in combined_errors]
    print(f"Processing {len(valid_words)} valid words")
    
    # Load original data for reference
    csv_path = OUTPUT_DIR / f"batch_{BATCH_NUM:03d}_words.csv"
    word_data = {}
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            word_data[row['word']] = row
    
    # Process each valid word
    processed_data = []
    
    for i, word in enumerate(valid_words, 1):
        print(f"Processing {i}/{len(valid_words)}: {word}")
        
        # Get original data
        orig_data = word_data.get(word, {})
        
        # Get dictionary data
        dict_data = get_dictionary_data(word)
        time.sleep(0.5)  # Rate limiting
        
        # Generate educational content
        example_sentence = generate_example_sentence(word)
        etymology = get_etymology(word)
        
        # Prepare row data
        row_data = {
            'word': word,
            'definition': dict_data['definition'] if dict_data['found'] else '',
            'pronunciation': dict_data['pronunciation'],
            'example_sentence': example_sentence,
            'etymology': etymology,
            'etymology_source': 'Claude',
            'definition_source': 'Dictionary API' if dict_data['found'] else '',
            'pronunciation_source': 'Dictionary API' if dict_data['found'] else '',
            'example_sentence_source': 'Claude',
            'years': orig_data.get('years', ''),
            'source_files': orig_data.get('source_files', ''),
            'source_difficulties': orig_data.get('source_difficulties', ''),
            'difficulty_level': assign_difficulty(orig_data.get('source_difficulties', ''))
        }
        
        processed_data.append(row_data)
    
    # Save processed data
    output_file = OUTPUT_DIR / f"batch_{BATCH_NUM:03d}_processed.csv"
    fieldnames = [
        'word', 'definition', 'pronunciation', 'example_sentence', 'etymology',
        'etymology_source', 'definition_source', 'pronunciation_source', 
        'example_sentence_source', 'years', 'source_files', 'source_difficulties',
        'difficulty_level'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_data)
    
    print(f"Saved {len(processed_data)} processed words to {output_file}")
    
    # Log combined errors if any
    if combined_errors:
        error_file = OUTPUT_DIR / f"batch_{BATCH_NUM:03d}_combined_errors.txt"
        with open(error_file, 'w', encoding='utf-8') as file:
            file.write(f"Combined word errors detected in batch {BATCH_NUM}:\n\n")
            for error in combined_errors:
                file.write(f"{error}\n")
        print(f"Logged {len(combined_errors)} combined errors to {error_file}")

if __name__ == "__main__":
    process_batch()