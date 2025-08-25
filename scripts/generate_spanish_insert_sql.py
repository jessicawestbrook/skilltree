"""
Generate SQL insert statements for Spanish vocabulary
This creates SQL that can be run directly in Supabase SQL editor
"""

import json
import uuid
from datetime import datetime
import os
import sys

# Install required packages if needed
for package in ['deep-translator']:
    try:
        __import__(package.replace('-', '_'))
    except ImportError:
        print(f"Installing {package}...")
        os.system(f"{sys.executable} -m pip install {package}")

from deep_translator import GoogleTranslator
import time

def get_phonetic_guide(word):
    """Generate phonetic guide for Spanish pronunciation"""
    phonetic = word.lower()
    replacements = [
        ('que', 'keh'), ('qui', 'kee'),
        ('ce', 'seh'), ('ci', 'see'),
        ('ge', 'heh'), ('gi', 'hee'),
        ('gue', 'geh'), ('gui', 'gee'),
        ('ll', 'y'), ('ñ', 'ny'),
        ('j', 'h'), ('rr', 'rr'),
        ('ch', 'ch'), ('v', 'b'),
        ('z', 'th'), # Spain Spanish
        ('á', 'AH'), ('é', 'EH'), 
        ('í', 'EE'), ('ó', 'OH'), ('ú', 'OO'),
        ('ü', 'w'),
    ]
    for old, new in replacements:
        phonetic = phonetic.replace(old, new)
    return phonetic

def get_part_of_speech(word):
    """Determine part of speech based on word patterns"""
    word = word.lower()
    
    # Common patterns
    if word.endswith(('ar', 'er', 'ir')) and len(word) > 3:
        return 'verb'
    elif word.endswith('mente') and len(word) > 6:
        return 'adverb'
    elif word.endswith(('ción', 'sión', 'dad', 'tad', 'ez', 'eza', 'ismo', 'miento')):
        return 'noun'
    elif word.endswith(('oso', 'osa', 'able', 'ible', 'ivo', 'iva')):
        return 'adjective'
    elif len(word) <= 3:
        return 'other'  # Articles, prepositions, etc.
    else:
        return 'noun'  # Default

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
    elif zipf_freq >= 3.0:
        return 5  # Expert

def escape_sql_string(s):
    """Escape string for SQL"""
    if s is None:
        return 'NULL'
    # Replace single quotes with two single quotes
    s = str(s).replace("'", "''")
    return f"'{s}'"

def main():
    print("Loading Spanish vocabulary selection...")
    print("="*60)
    
    # Load vocabulary selection
    try:
        with open('spanish_vocabulary_selection.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: spanish_vocabulary_selection.json not found")
        return
    
    vocabulary = data['vocabulary']
    
    # Initialize translator
    print("\nInitializing translator...")
    translator = GoogleTranslator(source='es', target='en')
    
    # Open output file
    output_file = 'insert_spanish_vocabulary.sql'
    
    # Keep track of processed words to avoid duplicates
    processed_words = set()
    
    # Read existing words (we'll check these in SQL)
    print("\nGenerating SQL statements...")
    
    with open(output_file, 'w', encoding='utf-8') as sql_file:
        # Write header
        sql_file.write("-- Spanish Vocabulary Insert Script\n")
        sql_file.write("-- Generated: " + datetime.utcnow().isoformat() + "\n")
        sql_file.write("-- This script inserts Spanish vocabulary with zipf >= 3.0\n\n")
        
        # Create a temporary table to track what we're inserting
        sql_file.write("-- Create temporary table for new words\n")
        sql_file.write("CREATE TEMP TABLE new_spanish_words AS\n")
        sql_file.write("WITH words_to_insert AS (\n")
        sql_file.write("  VALUES\n")
        
        # Process each difficulty level
        difficulty_order = ['Basic', 'Elementary', 'Intermediate', 'Advanced', 'Expert']
        all_values = []
        total_words = 0
        
        for difficulty in difficulty_order:
            if difficulty not in vocabulary:
                continue
                
            words = vocabulary[difficulty]
            print(f"\nProcessing {difficulty} level: {len(words)} words")
            
            for i, word_data in enumerate(words):
                word = word_data['word'].lower()
                zipf = word_data['zipf']
                
                # Skip if already processed
                if word in processed_words:
                    continue
                
                # Skip if zipf < 3 (shouldn't happen but just in case)
                if zipf < 3.0:
                    continue
                
                try:
                    # Add delay to avoid rate limiting
                    if i % 10 == 0 and i > 0:
                        time.sleep(0.5)
                    
                    # Translate
                    translation = translator.translate(word)
                    if not translation or translation.lower() == word.lower():
                        translation = word  # Keep original if no translation
                    
                    # Generate values
                    values = (
                        escape_sql_string(str(uuid.uuid4())),
                        escape_sql_string('es'),
                        escape_sql_string(word),
                        str(zipf),
                        str(get_difficulty_id(zipf)),
                        escape_sql_string(translation),
                        escape_sql_string(get_phonetic_guide(word)),
                        escape_sql_string(get_part_of_speech(word)),
                        escape_sql_string(translation),
                        escape_sql_string('GoogleTranslator'),
                        escape_sql_string('GoogleTranslator')
                    )
                    
                    all_values.append(f"    ({','.join(values)})")
                    processed_words.add(word)
                    total_words += 1
                    
                    if total_words % 50 == 0:
                        print(f"  Processed {total_words} words...")
                    
                except Exception as e:
                    print(f"  Error processing {word}: {e}")
                    continue
        
        # Write all values
        sql_file.write(",\n".join(all_values))
        sql_file.write("\n) AS t(id, language, word, zipf_frequency, difficulty_id, english_translation, pronunciation_guide, part_of_speech, definition_english, translation_source, definition_source)\n")
        sql_file.write("SELECT * FROM words_to_insert;\n\n")
        
        # Insert only words that don't already exist
        sql_file.write("-- Insert only new words (skip existing)\n")
        sql_file.write("INSERT INTO language_vocabulary (\n")
        sql_file.write("  id, language, word, zipf_frequency, difficulty_id, \n")
        sql_file.write("  english_translation, pronunciation_guide, part_of_speech,\n")
        sql_file.write("  definition_english, translation_source, definition_source,\n")
        sql_file.write("  created_at\n")
        sql_file.write(")\n")
        sql_file.write("SELECT \n")
        sql_file.write("  n.id::uuid, n.language, n.word, n.zipf_frequency::numeric, n.difficulty_id::integer,\n")
        sql_file.write("  n.english_translation, n.pronunciation_guide, n.part_of_speech,\n")
        sql_file.write("  n.definition_english, n.translation_source, n.definition_source,\n")
        sql_file.write("  NOW()\n")
        sql_file.write("FROM new_spanish_words n\n")
        sql_file.write("WHERE NOT EXISTS (\n")
        sql_file.write("  SELECT 1 FROM language_vocabulary lv\n")
        sql_file.write("  WHERE lv.language = 'es' AND LOWER(lv.word) = LOWER(n.word)\n")
        sql_file.write(");\n\n")
        
        # Add verification query
        sql_file.write("-- Verification: Show how many words were inserted\n")
        sql_file.write("SELECT \n")
        sql_file.write("  COUNT(*) AS total_spanish_words,\n")
        sql_file.write("  COUNT(CASE WHEN difficulty_id = 1 THEN 1 END) AS basic,\n")
        sql_file.write("  COUNT(CASE WHEN difficulty_id = 2 THEN 1 END) AS elementary,\n")
        sql_file.write("  COUNT(CASE WHEN difficulty_id = 3 THEN 1 END) AS intermediate,\n")
        sql_file.write("  COUNT(CASE WHEN difficulty_id = 4 THEN 1 END) AS advanced,\n")
        sql_file.write("  COUNT(CASE WHEN difficulty_id = 5 THEN 1 END) AS expert\n")
        sql_file.write("FROM language_vocabulary\n")
        sql_file.write("WHERE language = 'es';\n")
    
    print(f"\n{'='*60}")
    print(f"Generated SQL file: {output_file}")
    print(f"Total words processed: {total_words}")
    print("\nTo insert the words:")
    print("1. Open your Supabase project dashboard")
    print("2. Go to SQL Editor")
    print("3. Copy and paste the contents of insert_spanish_vocabulary.sql")
    print("4. Run the query")
    print("\nThe script will automatically skip any words that already exist.")

if __name__ == "__main__":
    main()