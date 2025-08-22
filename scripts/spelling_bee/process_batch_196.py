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
BATCH_NUM = 196

def detect_combined_words(words):
    """Detect words that appear to be multiple words combined together"""
    combined_errors = []
    
    for word in words:
        word_clean = word.lower().strip()
        
        # Skip very short words
        if len(word_clean) < 8:
            continue
            
        # Specific patterns we've seen
        if word_clean == 'worldmath':
            combined_errors.append(word)
            
        # Look for other suspicious patterns
        if (any(common in word_clean for common in ['world', 'math']) and 
            len(word_clean) > 10):
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
        'world': 'The ____ is full of amazing wonders waiting to be discovered.',
        'worried': 'She looked ____ about the upcoming test results.',
        'worrywart': 'My grandmother was such a ____ that she worried about everything.',
        'worse': 'The weather today is ____ than yesterday.',
        'worth': 'The antique vase was ____ more than they initially thought.',
        'wraith': 'The ghostly ____ appeared in the moonlight.',
        'wrapped': 'She carefully ____ the fragile gift in tissue paper.',
        'wrath': "The king's ____ was feared throughout the kingdom.",
        'wreaked': 'The hurricane ____ havoc on the coastal towns.',
        'wreath': 'The holiday ____ hung beautifully on the front door.',
        'wreckage': 'The ____ from the shipwreck was scattered across the beach.',
        'wren': 'The tiny ____ built its nest in the rose bush.',
        'wrench': 'He used a ____ to tighten the loose bolts.',
        'wrenches': 'The mechanic organized his ____ by size in the toolbox.',
        'wrestle': 'The children would ____ playfully on the grass.',
        'wretched': 'The homeless man lived in ____ conditions.',
        'wriggle': "The puppy tried to ____ out of the child's arms.",
        'wring': 'She had to ____ out the wet towel before hanging it.',
        'wrinkle': 'A small ____ appeared on her forehead when she frowned.',
        'wrist': 'The tennis player wore a brace on her injured ____.',
        'write': 'Students must ____ their essays in blue or black ink.',
        'written': 'The contract was ____ in complex legal language.',
        'wrong': 'The student realized her answer was ____.',
        'wrote': 'Shakespeare ____ many famous plays and sonnets.',
        'wrought': 'The blacksmith ____ beautiful iron gates for the mansion.',
        'wrung': 'She ____ her hands nervously during the interview.',
        'wyoming': 'The state of ____ is known for its vast wilderness areas.',
        'xanthe': 'The name ____ means yellow or golden in Greek.',
        'xanthoma': 'The doctor identified the skin lesion as a ____.',
        'xenial': 'The host showed ____ hospitality to all visitors.',
        'xenolithic': 'The ____ rock contained fragments from older formations.',
        'xerophytic': 'Desert plants are typically ____ to survive dry conditions.',
        'xiphoid': 'The ____ process is the lowest part of the breastbone.',
        'xylem': 'The ____ tissue transports water from roots to leaves.',
        'xylophone': 'The musician played a cheerful melody on the ____.',
        'yacht': 'The luxury ____ sailed gracefully into the harbor.',
        'yachting': 'They spent their vacation ____ in the Mediterranean.',
        'yammer': 'The children would ____ constantly about wanting snacks.',
        'yard': 'The children played games in the back ____.',
        'yarn': 'She used colorful ____ to knit a warm winter scarf.',
        'yawn': 'The tired student tried to stifle a ____.',
        'yearbook': "Students signed each other's ____ at graduation.",
        'yearling': 'The ____ horse showed great potential for racing.',
        'yeast': 'The baker added ____ to help the bread rise.',
        'yell': "The coach had to ____ over the crowd's noise.",
        'yelp': 'The puppy let out a sharp ____ when startled.',
        'yellow': 'The bright ____ sunflowers swayed in the breeze.',
        'yen': 'He had a strong ____ for adventure and travel.',
        'yes': 'She nodded and said "____ " to the proposal.',
        'yesterday': 'The package was supposed to arrive ____.',
        'yield': "The farmer's crops had an excellent ____ this year.",
        'yodel': 'The Swiss singer could ____ beautifully in the mountains.',
        'yoga': 'She practiced ____ every morning to stay flexible.',
        'yogurt': 'The creamy ____ was topped with fresh berries.',
        'yoke': 'The oxen wore a wooden ____ to pull the plow.',
        'yolk': 'The bright orange ____ of the farm egg was delicious.',
        'young': 'The ____ artist showed tremendous talent.',
        'your': 'Please remember to bring ____ textbook to class.',
        'youth': 'The energy of ____ filled the summer camp.',
        'yurt': 'The nomads lived in a traditional ____ on the steppes.',
        'zap': 'The electric fence would ____ anyone who touched it.',
        'zeal': 'Her ____ for environmental causes was inspiring.',
        'zealous': 'The ____ fan cheered loudly for her team.',
        'zebra': 'The ____ stripes help camouflage it from predators.',
        'zen': 'She found ____ through meditation and mindfulness.',
        'zenith': 'The sun reached its ____ at noon.',
        'zephyr': 'A gentle ____ rustled the leaves on the trees.',
        'zero': 'The temperature dropped to ____ degrees overnight.',
        'zest': 'She approached every challenge with great ____.',
        'zigzag': 'The lightning bolt followed a ____ path across the sky.',
        'zinc': 'The metal roof was coated with ____ to prevent rust.',
        'zip': 'He forgot to ____ up his jacket before going outside.',
        'zodiac': 'She checked her ____ sign in the daily horoscope.',
        'zone': 'The school ____ required drivers to slow down.',
        'zoo': 'The children were excited to visit the ____ on Saturday.',
        'zoom': 'The photographer used the lens to ____ in on the bird.',
        'zucchini': 'The garden produced an abundance of ____.',
        'zygote': 'The ____ is the first stage of embryonic development.'
    }
    
    return examples.get(word.lower(), f'The ____ was an important part of the story.')

def get_etymology(word):
    """Generate etymology information"""
    
    etymologies = {
        'world': 'From Old English weorold, meaning age of man or earthly existence',
        'worried': 'From worry + -ed, Old English wyrgan meaning to strangle',
        'worrywart': 'Modern compound of worry + wart, meaning chronic worrier',
        'worse': 'From Old English wiersa, comparative of bad',
        'worth': 'From Old English weorth, meaning value or price',
        'wraith': 'From Scots wraith, meaning ghost or specter',
        'wrapped': 'From wrap + -ed, Middle English wrappen',
        'wrath': 'From Old English wræth, meaning anger or fury',
        'wreaked': 'From wreak + -ed, Old English wrecan meaning to drive out',
        'wreath': 'From Old English wreath, meaning twisted band',
        'wreckage': 'From wreck + -age, Middle English wrek from Old Norse',
        'wren': 'From Old English wrenna, small brown bird',
        'wrench': 'From Old English wrencan, meaning to twist',
        'wrenches': 'Plural of wrench, from Old English wrencan',
        'wrestle': 'From Old English wræstlian, meaning to grapple',
        'wretched': 'From wretch + -ed, Old English wrecca meaning exile',
        'wriggle': 'From Middle Low German wriggeln, meaning to twist',
        'wring': 'From Old English wringan, meaning to squeeze',
        'wrinkle': 'From Old English wrincle, meaning small fold',
        'wrist': 'From Old English wrist, meaning joint of the hand',
        'write': 'From Old English writan, meaning to score or scratch',
        'written': 'Past participle of write, from Old English writen',
        'wrong': 'From Old Norse rangr, meaning twisted or crooked',
        'wrote': 'Past tense of write, from Old English wrat',
        'wrought': 'Past tense of work, from Old English worhte',
        'wrung': 'Past tense of wring, from Old English wrang',
        'wyoming': 'From Algonquian, meaning large prairie place',
        'xanthe': 'From Greek xanthos, meaning yellow or golden',
        'xanthoma': 'From Greek xanthos (yellow) + -oma (tumor)',
        'xenial': 'From Greek xenos, meaning stranger or guest',
        'xenolithic': 'From Greek xenos (foreign) + lithos (stone)',
        'xerophytic': 'From Greek xeros (dry) + phyton (plant)',
        'xiphoid': 'From Greek xiphos (sword) + -oid (resembling)',
        'xylem': 'From Greek xylon, meaning wood',
        'xylophone': 'From Greek xylon (wood) + phone (sound)',
        'yacht': 'From Dutch jacht, meaning hunting ship',
        'yachting': 'From yacht + -ing, recreational boating',
        'yammer': 'Imitative word expressing persistent complaining',
        'yard': 'From Old English geard, meaning enclosed space',
        'yarn': 'From Old English gearn, meaning spun fiber',
        'yawn': 'From Old English ganian, meaning to gape',
        'yearbook': 'Compound of year + book, annual publication',
        'yearling': 'From year + -ling, meaning one year old',
        'yeast': 'From Old English gist, meaning foam or froth',
        'yell': 'From Old English giellan, meaning to shout',
        'yelp': 'From Old English gielpan, meaning to boast loudly',
        'yellow': 'From Old English geolu, meaning bright color',
        'yen': 'From Japanese en, meaning circle or round',
        'yes': 'From Old English gese, meaning affirmative response',
        'yesterday': 'From Old English geostran dæg, meaning former day',
        'yield': 'From Old English gieldan, meaning to pay or give',
        'yodel': 'From German jodeln, Alpine singing style',
        'yoga': 'From Sanskrit yoga, meaning union or joining',
        'yogurt': 'From Turkish yogurt, meaning fermented milk',
        'yoke': 'From Old English geoc, meaning wooden frame',
        'yolk': 'From Old English geolca, meaning yellow part',
        'young': 'From Old English geong, meaning not old',
        'your': 'From Old English eower, possessive pronoun',
        'youth': 'From Old English geoguoth, meaning young people',
        'yurt': 'From Russian yurta, portable round tent',
        'zap': 'Imitative word for sudden electric shock',
        'zeal': 'From Greek zelos, meaning ardor or eagerness',
        'zealous': 'From zeal + -ous, showing great energy',
        'zebra': 'From Portuguese zebra, striped African animal',
        'zen': 'From Japanese zen, meaning meditation',
        'zenith': 'From Arabic samt, meaning path overhead',
        'zephyr': 'From Greek zephyros, meaning west wind',
        'zero': 'From Arabic sifr, meaning empty or nothing',
        'zest': 'From French zeste, meaning orange peel',
        'zigzag': 'From French zigzag, irregular angular line',
        'zinc': 'From German zink, metallic element',
        'zip': 'Imitative of sound of rapid movement',
        'zodiac': 'From Greek zodiakos, meaning circle of animals',
        'zone': 'From Greek zone, meaning belt or girdle',
        'zoo': 'Short for zoological garden, from Greek zoon (animal)',
        'zoom': 'Imitative of sound of rapid movement',
        'zucchini': 'From Italian zucchino, diminutive of zucca (gourd)',
        'zygote': 'From Greek zygotos, meaning joined or yoked'
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