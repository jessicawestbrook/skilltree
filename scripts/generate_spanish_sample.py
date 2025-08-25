"""
Generate a small sample of Spanish vocabulary for testing
Only processes 10 words per difficulty level
"""

import json
import csv
import uuid
from datetime import datetime
from deep_translator import GoogleTranslator

def get_difficulty_id(zipf_freq):
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

def get_phonetic(word):
    phonetic = word.lower()
    replacements = [
        ('que', 'keh'), ('qui', 'kee'),
        ('ce', 'seh'), ('ci', 'see'),
        ('ge', 'heh'), ('gi', 'hee'),
        ('ll', 'y'), ('ñ', 'ny'),
        ('j', 'h'), ('rr', 'rr'),
        ('á', 'AH'), ('é', 'EH'), ('í', 'EE'), ('ó', 'OH'), ('ú', 'OO')
    ]
    for old, new in replacements:
        phonetic = phonetic.replace(old, new)
    return phonetic

print("Generating Spanish vocabulary sample...")
print("=" * 50)

# Load vocabulary
with open('spanish_vocabulary_selection.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

translator = GoogleTranslator(source='es', target='en')
records = []

# Process 10 words from each level
for difficulty in ['Basic', 'Elementary', 'Intermediate', 'Advanced', 'Expert']:
    words = data['vocabulary'].get(difficulty, [])[:10]
    
    print(f"\n{difficulty} ({len(words)} words):")
    
    for word_data in words:
        word = word_data['word']
        
        try:
            translation = translator.translate(word)
            
            record = {
                'id': str(uuid.uuid4()),
                'language': 'es',
                'word': word,
                'base_form': word_data.get('base_form'),
                'zipf_frequency': word_data['zipf'],
                'difficulty_id': get_difficulty_id(word_data['zipf']),
                'english_translation': translation,
                'pronunciation_guide': get_phonetic(word),
                'part_of_speech': 'noun',  # simplified
                'definition_english': translation,
                'translation_source': 'GoogleTranslator',
                'created_at': datetime.utcnow().isoformat()
            }
            
            records.append(record)
            print(f"  {word:15} -> {translation:20} [{get_phonetic(word)}]")
            
        except Exception as e:
            print(f"  Error: {word} - {e}")

# Save sample
output_file = 'spanish_vocab_sample.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    if records:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

print(f"\n" + "=" * 50)
print(f"Generated {len(records)} sample records")
print(f"Saved to {output_file}")

# Also save as SQL insert statements for review
sql_file = 'spanish_vocab_sample.sql'
with open(sql_file, 'w', encoding='utf-8') as f:
    f.write("-- Sample Spanish vocabulary inserts\n")
    f.write("-- Review before inserting into database\n\n")
    
    for r in records[:5]:  # Just first 5 for review
        f.write(f"INSERT INTO language_vocabulary (\n")
        f.write(f"  id, language, word, base_form, zipf_frequency, difficulty_id,\n")
        f.write(f"  english_translation, pronunciation_guide, part_of_speech,\n")
        f.write(f"  definition_english, translation_source, created_at\n")
        f.write(f") VALUES (\n")
        base_form_value = 'NULL' if not r.get('base_form') else f"'{r['base_form']}'"
        f.write(f"  '{r['id']}', 'es', '{r['word']}', ")
        f.write(f"{base_form_value}, ")
        f.write(f"{r['zipf_frequency']}, {r['difficulty_id']},\n")
        f.write(f"  '{r['english_translation']}', '{r['pronunciation_guide']}', '{r['part_of_speech']}',\n")
        f.write(f"  '{r['definition_english']}', '{r['translation_source']}', '{r['created_at']}'\n")
        f.write(f");\n\n")

print(f"SQL preview saved to {sql_file}")