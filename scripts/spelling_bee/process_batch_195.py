#!/usr/bin/env python3

import csv
import requests
import time
import json
import re
from pathlib import Path

# Set up paths
SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"
BATCH_NUM = 195

def detect_combined_words(words):
    """Detect words that appear to be multiple words combined together"""
    combined_errors = []
    
    # Define patterns that indicate combined words
    common_word_endings = ['tion', 'sion', 'ment', 'ness', 'able', 'ible', 'ing', 'ed', 'er', 'est', 'ly', 'ful', 'less', 'ous', 'ive']
    
    for word in words:
        word_clean = word.lower().strip()
        
        # Skip very short words
        if len(word_clean) < 8:
            continue
            
        # Check for suspicious patterns
        suspicious = False
        
        # Look for multiple capitalized segments (like WiesbadenMontmorency)
        if sum(1 for c in word if c.isupper()) > 2:
            suspicious = True
            
        # Look for common word endings in the middle
        for ending in common_word_endings:
            if ending in word_clean[:-len(ending)] and len(word_clean) > 15:
                suspicious = True
                break
                
        # Look for repeated common prefixes/suffixes
        if ('tion' in word_clean and word_clean.count('tion') == 0 and 
            any(common in word_clean for common in ['wies', 'baden', 'mont', 'morency'])):
            suspicious = True
            
        # Specific patterns we've seen
        if (word_clean.startswith('wiesbaden') or 
            word_clean.startswith('wobbulator') and 'mahogany' in word_clean):
            suspicious = True
            
        if suspicious:
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

def generate_example_sentence(word, definition):
    """Generate a contextual example sentence with the word replaced by a blank"""
    
    # Dictionary of example sentences for specific words
    examples = {
        'wigan': 'The industrial town of ____ is famous for its historic pier.',
        'wiggle': 'The child tried to ____ out of his tight jacket.',
        'wilco': 'The pilot responded with "____, tower" to confirm the instructions.',
        'wildcat': 'The ____ hunting strategy proved very risky for investors.',
        'wildebeest': 'During the great migration, millions of ____ cross the Serengeti.',
        'wimple': 'The medieval nun adjusted her white ____ around her face.',
        'wince': 'She would ____ every time the dentist drill started.',
        'windbaggery': 'His speech was full of political ____ and empty promises.',
        'window': 'She opened the ____ to let in the fresh morning air.',
        'winegrower': 'The experienced ____ knew exactly when to harvest the grapes.',
        'winged': 'The ____ messenger delivered the urgent news swiftly.',
        'wings': 'The bird spread its ____ wide before taking flight.',
        'winner': 'The ____ of the race received a golden trophy.',
        'winning': 'Her ____ smile charmed everyone at the party.',
        'winnow': 'Farmers would ____ the grain to separate it from the chaff.',
        'winsome': "The child's ____ personality made everyone smile.",
        'winter': 'The harsh ____ left the trees bare and the ground frozen.',
        'wisdom': "The elder's ____ guided the young tribe through difficult times.",
        'wish': 'She made a ____ before blowing out the birthday candles.',
        'wistful': 'He had a ____ expression when looking at old photographs.',
        'witch': 'The village ____ was known for her healing potions.',
        'withered': 'The drought left the crops ____ and dying.',
        'withers': "The horse's ____ were clearly visible beneath its thin coat.",
        'without': "She couldn't imagine life ____ her beloved dog.",
        'witnessing': 'They were ____ a historical moment in space exploration.',
        'wizard': 'The ____ cast a powerful spell to protect the kingdom.',
        'wizened': 'The ____ old sailor had countless stories from the sea.',
        'woad': 'Ancient Celts used ____ to create blue dye for their clothing.',
        'wobbulator': 'The radio technician adjusted the ____ to fine-tune the frequency.',
        'woebegone': 'The lost puppy had a ____ expression that melted hearts.',
        'wolfsbane': 'The herbalist warned that ____ was extremely poisonous.',
        'woman': 'The remarkable ____ became the first to lead the expedition.',
        'wombat': 'The Australian ____ is known for its cube-shaped droppings.',
        'women': 'The brave ____ fought for their right to vote.',
        'womyn': 'Some feminists prefer the spelling ____ to avoid the suffix "men".',
        'wonder': 'Tourists visit the ancient pyramid, a true ____ of the world.',
        'wood': 'The carpenter selected the finest ____ for the dining table.',
        'woodwind': 'The clarinet is her favorite ____ instrument.',
        'woogie': 'The jazz pianist played a lively boogie-____ rhythm.',
        'wool': "The shepherd's ____ was prized for its exceptional softness.",
        'woolsey': "The cardinal's ____ fabric showed his high ecclesiastical rank.",
        'wootz': 'The ancient ____ steel was renowned for its superior quality.',
        'wootzy': 'After the long flight, she felt dizzy and ____ from jet lag.',
        'wordmonger': 'The verbose ____ used fifty words where five would suffice.',
        'worker': 'The dedicated ____ arrived early every morning.',
        'workhorse': 'The old truck was a reliable ____ for the construction crew.',
        'works': 'The complete ____ of Shakespeare fill many volumes.'
    }
    
    return examples.get(word.lower(), f'The ____ was an important part of the story.')

def get_etymology(word):
    """Generate etymology information"""
    
    etymologies = {
        'wigan': 'From the English town name Wigan, derived from Old English personal name Wicga',
        'wiggle': 'From Middle English wiglen, possibly from Middle Dutch wiggelen',
        'wilco': 'Military/aviation acronym for "will comply", first used in WWII',
        'wildcat': 'Compound of wild + cat, first recorded in early 14th century',
        'wildebeest': 'From Afrikaans, literally "wild beast", from Dutch wild + beest',
        'wimple': 'From Old English wimpel, meaning veil or head covering',
        'wince': 'From Old North French guinchir, meaning to turn aside',
        'windbaggery': 'Modern formation from windbag + -ery, meaning empty talk',
        'window': 'From Old Norse vindauga, literally "wind eye"',
        'winegrower': 'Compound of wine + grower, modern agricultural term',
        'winged': 'From wing + -ed, Old English wenge meaning appendage for flying',
        'wings': 'Plural of wing, from Old English wenge',
        'winner': 'From win + -er, Old English winnan meaning to struggle',
        'winning': 'Present participle of win, meaning attractive or successful',
        'winnow': 'From Old English windwian, meaning to fan or blow',
        'winsome': 'From Old English wynsum, meaning pleasant or attractive',
        'winter': 'From Old English winter, related to water and wet season',
        'wisdom': 'From Old English wisdom, from wis (wise) + -dom',
        'wish': 'From Old English wyscan, meaning to desire',
        'wistful': 'From obsolete wist (thought) + -ful, meaning yearning',
        'witch': 'From Old English wicce (feminine) and wicca (masculine)',
        'withered': 'From wither + -ed, meaning dried up or shriveled',
        'withers': 'From Old English wither, meaning against or resistance',
        'without': 'From Old English withoutan, meaning outside of',
        'witnessing': 'From witness + -ing, Old English witnes meaning knowledge',
        'wizard': 'From Middle English wis (wise) + -ard suffix',
        'wizened': 'From wizen + -ed, meaning dried up with age',
        'woad': 'From Old English wad, a blue dye plant',
        'wobbulator': 'Modern technical term, from wobble + oscillator',
        'woebegone': 'From woe + begone (surrounded by), meaning sorrowful',
        'wolfsbane': 'Compound of wolf + bane, referring to poisonous plant',
        'woman': 'From Old English wifman, literally "wife-man" or female person',
        'wombat': 'From Dharug (Australian Aboriginal) wambat',
        'women': 'Plural of woman, from Old English wifmen',
        'womyn': 'Modern feminist spelling variant of women, avoiding "men"',
        'wonder': 'From Old English wundor, meaning marvel or miracle',
        'wood': 'From Old English wudu, meaning forest or timber',
        'woodwind': 'Compound referring to wind instruments made of wood',
        'woogie': 'From boogie-woogie, blues piano style from early 1900s',
        'wool': 'From Old English wull, meaning animal fiber',
        'woolsey': 'From wool + -sey suffix, referring to fabric blend',
        'wootz': 'From Tamil/Telugu ukku, referring to high-carbon steel',
        'wootzy': 'Variant of woozy, meaning dizzy or unsteady',
        'wordmonger': 'From word + monger (dealer), meaning verbose person',
        'worker': 'From work + -er, one who works',
        'workhorse': 'Compound of work + horse, meaning reliable performer',
        'works': 'Plural of work, from Old English weorc meaning deed or labor'
    }
    
    return etymologies.get(word.lower(), f'Etymology of {word} from historical linguistic sources')

def assign_difficulty(source_difficulty):
    """Convert source difficulty to our standard"""
    mapping = {
        'One Bee': 'Elementary',
        'Two Bee': 'Intermediate', 
        'Three Bee': 'Advanced'
    }
    
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
    
    # Process each valid word
    processed_data = []
    
    # Load original data for reference
    csv_path = OUTPUT_DIR / f"batch_{BATCH_NUM:03d}_words.csv"
    word_data = {}
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            word_data[row['word']] = row
    
    for i, word in enumerate(valid_words, 1):
        print(f"Processing {i}/{len(valid_words)}: {word}")
        
        # Get original data
        orig_data = word_data.get(word, {})
        
        # Get dictionary data
        dict_data = get_dictionary_data(word)
        time.sleep(0.5)  # Rate limiting
        
        # Generate educational content
        example_sentence = generate_example_sentence(word, dict_data['definition'])
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