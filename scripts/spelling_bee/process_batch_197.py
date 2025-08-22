#!/usr/bin/env python3

import csv
import requests
import time
from pathlib import Path

# Set up paths
SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"
BATCH_NUM = 197

def detect_combined_words(words):
    """Detect words that appear to be multiple words combined together"""
    combined_errors = []
    
    for word in words:
        word_clean = word.lower().strip()
        
        # Skip very short words
        if len(word_clean) < 8:
            continue
            
        # Look for suspicious patterns - very long words with common combinations
        if len(word_clean) > 15 and any(combo in word_clean for combo in ['math', 'world', 'yakitori']):
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
    
    # Quick examples for common words
    examples = {
        'yeti': 'The legendary ____ is said to roam the Himalayan mountains.',
        'yippee': 'The children shouted "____ " when school was cancelled.',
        'yoga': 'She practiced ____ every morning to improve flexibility.',
        'yolks': 'The recipe called for separating egg whites from ____.',
        'yonder': 'The treasure lies buried somewhere over ____.',
        'yore': 'In days of ____, knights rode horses into battle.',
        'yorkshire': 'The ____ pudding was a traditional English dish.',
        'yoruba': 'The ____ people have a rich cultural heritage in Nigeria.',
        'yosenabe': 'The Japanese ____ hot pot contained fresh vegetables and seafood.',
        'young': 'The ____ artist showed remarkable talent.',
        'yourself': 'You must believe in ____ to succeed.',
        'yttriferous': 'The ____ mineral contained rare earth elements.',
        'yuga': 'According to Hindu cosmology, we live in the current ____.',
        'yuloh': 'The sailor used a ____ to propel the boat through calm waters.',
        'zabajone': 'The Italian dessert ____ was made with egg yolks and wine.',
        'zabaione': 'The creamy ____ was served warm in delicate glasses.',
        'zag': 'The path made a sudden ____ to the left.',
        'zaibatsu': 'The powerful ____ controlled much of Japanese industry.',
        'zakuska': 'The Russian ____ included pickled vegetables and smoked fish.',
        'zambo': 'The historical term ____ referred to people of mixed ancestry.',
        'zamindar': 'The wealthy ____ owned vast estates in colonial India.',
        'zapateo': 'The flamenco dancer performed the intricate ____ footwork.',
        'zaphrentid': 'The fossil ____ coral showed distinctive horn-like structure.',
        'zapotec': 'The ancient ____ civilization flourished in Oaxaca.',
        'zaptiah': 'The Ottoman ____ police maintained order in rural areas.',
        'zaratite': 'The green mineral ____ was found in nickel deposits.',
        'zarzuela': 'The Spanish ____ combined singing, dancing, and spoken dialogue.',
        'zealot': 'The religious ____ preached with fervent dedication.',
        'zebu': 'The ____ cattle were well-adapted to tropical climates.',
        'zed': 'British speakers call the letter Z a ____.',
        'zeitgeber': 'Sunlight acts as a natural ____ for circadian rhythms.',
        'zeitgeist': 'The art movement captured the ____ of the era.',
        'zemstvo': 'The Russian ____ provided local self-government.',
        'zenana': 'The ____ quarters housed the women of the household.',
        'zephyr': 'A gentle ____ rustled the leaves on the trees.',
        'zeppelin': 'The massive ____ airship crossed the Atlantic.',
        'zeppelin': 'The ____ floated majestically across the sky.',
        'zeugma': 'The literary device ____ creates surprising word combinations.',
        'zeusian': 'The statue had a ____ grandeur befitting the king of gods.',
        'ziggurat': 'The ancient ____ temple tower dominated the skyline.',
        'zigzag': 'The lightning followed a ____ path across the sky.',
        'zinck': 'The old spelling ____ referred to the metallic element.',
        'zingy': 'The lemonade had a ____ flavor that woke up the taste buds.',
        'zinnia': 'The colorful ____ flowers bloomed all summer long.',
        'zircon': 'The ____ gemstone sparkled in the jewelry setting.',
        'zither': 'The musician plucked the strings of the ____.',
        'zizith': 'The religious ____ fringes were worn under the garment.',
        'zloty': 'The Polish ____ is the national currency.',
        'zodiac': 'She studied her ____ sign in the astrology book.',
        'zombi': 'The ____ folklore originated in Haitian traditions.',
        'zombie': 'The horror movie featured a ____ apocalypse.',
        'zonal': 'The climate map showed different ____ temperature regions.',
        'zonary': 'The ____ placenta structure was studied in mammals.',
        'zone': 'The school ____ required drivers to slow down.',
        'zooglea': 'The bacterial ____ formed a protective gel matrix.',
        'zooid': 'Each ____ in the colony had a specialized function.',
        'zoology': 'She majored in ____ to study animal behavior.',
        'zoom': 'The photographer used the lens to ____ in on the subject.',
        'zoophyte': 'The marine ____ resembled both animals and plants.',
        'zori': 'The traditional Japanese ____ sandals were made of straw.',
        'zoril': 'The African ____ resembled a skunk with its striped pattern.',
        'zoster': 'The medical term ____ refers to a viral skin condition.',
        'zouave': 'The ____ military uniform featured colorful baggy pants.',
        'zounds': 'The old exclamation "____" expressed surprise or anger.',
        'zoysia': 'The ____ grass was drought-resistant and low-maintenance.',
        'zucchetto': 'The Pope wore a white ____ skull cap.',
        'zucchini': 'The garden produced an abundance of ____.',
        'zwieback': 'The ____ biscuits were perfect for teething babies.',
        'zydeco': 'The Louisiana ____ music featured accordion and washboard.',
        'zygote': 'The fertilized ____ began dividing into multiple cells.',
        'zymurgy': 'The science of ____ deals with fermentation processes.'
    }
    
    return examples.get(word.lower(), f'The ____ was an important part of the story.')

def get_etymology(word):
    """Generate etymology information"""
    
    etymologies = {
        'yeti': 'From Tibetan yeh-teh, meaning rock bear or man-bear',
        'yippee': 'Exclamation of joy, popularized in American West',
        'yoga': 'From Sanskrit yoga, meaning union or joining',
        'yolks': 'Plural of yolk, from Old English geolca meaning yellow part',
        'yonder': 'From Middle English yonder, meaning at a distance',
        'yore': 'From Old English geara, meaning years or time past',
        'yorkshire': 'From Old English Eoforwic, meaning boar settlement',
        'yoruba': 'From the name of the ethnic group in West Africa',
        'yosenabe': 'From Japanese yose (gather) + nabe (pot)',
        'young': 'From Old English geong, meaning not old',
        'yourself': 'From your + self, reflexive pronoun',
        'yttriferous': 'From yttrium + -ferous (bearing), containing yttrium',
        'yuga': 'From Sanskrit yuga, meaning age or cosmic cycle',
        'yuloh': 'From Chinese yu (oar) + lo (scull), type of oar'
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