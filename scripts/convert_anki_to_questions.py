#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert Anki deck (.apkg) to language_questions format for the database
"""

import sys
import io

# Set UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import sqlite3
import zipfile
import tempfile
import os
import re
import html
import shutil
from pathlib import Path
from datetime import datetime
import uuid

def clean_html(text):
    """Remove HTML tags and clean up text"""
    if not text:
        return ""
    
    # Unescape HTML entities
    text = html.unescape(text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text.strip()

def clean_markdown(text):
    """Remove markdown formatting from text"""
    if not text:
        return ""
    
    # Remove headers (##, ###, etc.)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    
    # Remove bold/italic markers
    text = re.sub(r'\*{1,3}([^\*]+)\*{1,3}', r'\1', text)
    text = re.sub(r'_{1,3}([^_]+)_{1,3}', r'\1', text)
    
    # Remove code blocks
    text = re.sub(r'```[^`]*```', '', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    
    # Remove links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # Remove blockquotes
    text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)
    
    # Remove horizontal rules
    text = re.sub(r'^[\-\*]{3,}$', '', text, flags=re.MULTILINE)
    
    # Clean up extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = ' '.join(text.split())
    
    return text.strip()

def extract_anki_deck(apkg_path):
    """Extract and parse an Anki deck file"""
    cards_data = []
    media_files = {}
    
    # Create a temporary directory for extraction
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract the .apkg file (it's a zip file)
        with zipfile.ZipFile(apkg_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Check for media files
        media_json_path = os.path.join(temp_dir, 'media')
        if os.path.exists(media_json_path):
            with open(media_json_path, 'r', encoding='utf-8') as f:
                media_mapping = json.load(f)
                print(f"Found media mapping: {len(media_mapping)} files")
                
                # Copy media files to output directory
                media_output_dir = Path(__file__).parent / 'anki_media'
                media_output_dir.mkdir(exist_ok=True)
                
                for anki_name, real_name in media_mapping.items():
                    src_path = os.path.join(temp_dir, anki_name)
                    if os.path.exists(src_path):
                        dst_path = media_output_dir / real_name
                        shutil.copy2(src_path, dst_path)
                        media_files[real_name] = str(dst_path)
                        print(f"  Extracted media: {real_name}")
        
        # Connect to the Anki collection database
        collection_db = os.path.join(temp_dir, 'collection.anki2')
        
        if not os.path.exists(collection_db):
            print(f"Warning: collection.anki2 not found in {apkg_path}")
            return cards_data, media_files
        
        conn = sqlite3.connect(collection_db)
        cursor = conn.cursor()
        
        # Get cards and notes
        cursor.execute("""
            SELECT cards.id, notes.flds, notes.tags, cards.did
            FROM cards
            JOIN notes ON cards.nid = notes.id
        """)
        
        for row in cursor.fetchall():
            card_id, fields, tags, deck_id = row
            
            # Fields are separated by \x1f character
            field_list = fields.split('\x1f')
            
            # Store original fields with HTML for media extraction
            original_fields = field_list.copy()
            
            # Clean the fields for text
            field_list = [clean_html(field) for field in field_list]
            
            cards_data.append({
                'id': card_id,
                'fields': field_list,
                'original_fields': original_fields,
                'tags': tags,
                'deck_id': deck_id
            })
        
        conn.close()
    
    return cards_data, media_files

def extract_media_references(html_text):
    """Extract media file references from HTML text"""
    media_refs = {
        'audio': [],
        'images': []
    }
    
    if not html_text:
        return media_refs
    
    # Find audio references [sound:filename.mp3]
    audio_pattern = r'\[sound:([^\]]+)\]'
    audio_matches = re.findall(audio_pattern, html_text)
    media_refs['audio'] = audio_matches
    
    # Find image references <img src="filename">
    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
    img_matches = re.findall(img_pattern, html_text)
    media_refs['images'] = img_matches
    
    return media_refs

def parse_spanish_conjugation_card(fields, original_fields=None):
    """Parse a Spanish conjugation card into a question format"""
    if len(fields) < 2:
        return None
    
    # This deck structure:
    # Field 0: UUID (card ID)
    # Field 1: The actual Spanish sentence with cloze deletion {{c1::answer::hint}}
    # Field 2+: Additional fields (often empty)
    
    # Skip if this looks like a UUID in field 0
    if len(fields[0]) == 36 and '-' in fields[0]:
        # This is the Ultimate Spanish Conjugation deck format
        if len(fields) < 2 or not fields[1]:
            return None
        
        sentence_with_cloze = fields[1]
        
        # Extract the cloze deletion pattern {{c1::answer::hint}}
        import re
        cloze_pattern = r'\{\{c1::([^:}]+)(?:::([^}]+))?\}\}'
        match = re.search(cloze_pattern, sentence_with_cloze)
        
        if not match:
            # No cloze pattern found, skip this card
            return None
        
        answer = clean_markdown(clean_html(match.group(1).strip()))
        hint = clean_markdown(clean_html(match.group(2).strip())) if match.group(2) else None
        
        # Replace cloze with blank for the question
        question_text = re.sub(cloze_pattern, '_____', sentence_with_cloze)
        
        # Clean up the question text - remove HTML and markdown
        question_text = clean_markdown(clean_html(question_text))
        question_text = question_text.strip()
        
        # Try to extract verb from hint (format is usually "…verb…")
        verb = None
        if hint and hint.startswith('…') and hint.endswith('…'):
            verb = hint.strip('…')
        
        parsed_result = {
            'question': question_text,
            'answer': answer,
            'verb': verb,
            'original_sentence': sentence_with_cloze,
            'tense': None,
            'person': None
        }
        
        # Extract media references if original fields provided
        media_refs = {'audio': [], 'images': []}
        if original_fields and len(original_fields) >= 2:
            sentence_media = extract_media_references(original_fields[1])
            media_refs['audio'] = sentence_media['audio']
            media_refs['images'] = sentence_media['images']
        
        parsed_result['media'] = media_refs
        return parsed_result
        
    else:
        # Original parsing logic for standard format
        front = fields[0]
        back = fields[1]
        
        if not front or not back:
            return None
        
        # Try to parse the front to extract verb and conjugation info
        # Common patterns:
        # "verb - tense, person"
        # "Conjugate: verb (tense, person)"
        # "verb (tense) - person"
        
        question = None
        verb = None
        tense = None
        person = None
        
        # Pattern 1: "verb - tense, person"
        match = re.match(r'^([\w\s]+?)\s*[-–]\s*([\w\s]+?),\s*([\w\s]+)$', front)
        if match:
            verb = match.group(1).strip()
            tense = match.group(2).strip()
            person = match.group(3).strip()
        else:
            # Pattern 2: Try other patterns
            match = re.match(r'^Conjugate:\s*([\w\s]+?)\s*\(([\w\s]+?),\s*([\w\s]+)\)$', front)
            if match:
                verb = match.group(1).strip()
                tense = match.group(2).strip()
                person = match.group(3).strip()
            else:
                # Pattern 3: "verb (tense) - person"
                match = re.match(r'^([\w\s]+?)\s*\(([\w\s]+?)\)\s*[-–]\s*([\w\s]+)$', front)
                if match:
                    verb = match.group(1).strip()
                    tense = match.group(2).strip()
                    person = match.group(3).strip()
        
        # If we couldn't parse it, use the original format
        if not verb:
            question = f"Conjugate: {front}"
        else:
            # Create a more structured question
            person_map = {
                'yo': 'first person singular (yo)',
                'tú': 'second person singular informal (tú)',
                'él': 'third person singular masculine (él)',
                'ella': 'third person singular feminine (ella)',
                'usted': 'second person singular formal (usted)',
                'nosotros': 'first person plural (nosotros)',
                'vosotros': 'second person plural informal (vosotros)',
                'ellos': 'third person plural masculine (ellos)',
                'ellas': 'third person plural feminine (ellas)',
                'ustedes': 'second person plural formal (ustedes)'
            }
            
            person_full = person_map.get(person.lower(), person)
            question = f"Conjugate the Spanish verb '{verb}' in the {tense} for {person_full}:"
        
        # Extract media references if original fields provided
        media_refs = {'audio': [], 'images': []}
        if original_fields and len(original_fields) >= 2:
            front_media = extract_media_references(original_fields[0])
            back_media = extract_media_references(original_fields[1])
            media_refs['audio'] = front_media['audio'] + back_media['audio']
            media_refs['images'] = front_media['images'] + back_media['images']
        
        return {
            'question': question,
            'answer': back,
            'verb': verb,
            'tense': tense,
            'person': person,
            'media': media_refs
        }

def convert_to_language_questions(anki_cards, media_files):
    """Convert Anki cards to language_questions format"""
    questions = []
    
    for card in anki_cards:
        # Skip orientation cards
        if 'orientation' in card.get('tags', ''):
            continue
        parsed = parse_spanish_conjugation_card(
            card['fields'], 
            card.get('original_fields')
        )
        
        if not parsed:
            continue
        
        # Generate a unique ID
        question_id = str(uuid.uuid4())
        
        # Determine difficulty based on tense or tags
        difficulty = 'Intermediate'  # Default
        
        # Check tags first for better categorization
        anki_tags = card.get('tags', '')
        if anki_tags:
            if 'presente' in anki_tags or 'pretérito' in anki_tags:
                difficulty = 'Elementary'
            elif 'subjuntivo' in anki_tags or 'extreme_irregularity' in anki_tags:
                difficulty = 'Advanced'
            elif 'imperfecto' in anki_tags or 'futuro' in anki_tags or 'condicional' in anki_tags:
                difficulty = 'Intermediate'
        elif parsed.get('tense'):
            tense_lower = parsed['tense'].lower()
            if 'present' in tense_lower or 'presente' in tense_lower:
                difficulty = 'Elementary'
            elif 'preterit' in tense_lower or 'pretérito' in tense_lower:
                difficulty = 'Elementary'
            elif 'imperfect' in tense_lower or 'imperfecto' in tense_lower:
                difficulty = 'Intermediate'
            elif 'future' in tense_lower or 'futuro' in tense_lower:
                difficulty = 'Intermediate'
            elif 'conditional' in tense_lower or 'condicional' in tense_lower:
                difficulty = 'Intermediate'
            elif 'subjunctive' in tense_lower or 'subjuntivo' in tense_lower:
                difficulty = 'Advanced'
            elif 'perfect' in tense_lower or 'perfecto' in tense_lower:
                difficulty = 'Advanced'
        
        # Check for media files
        audio_url = None
        image_url = None
        
        if parsed.get('media'):
            # Check if we have audio files
            if parsed['media']['audio']:
                audio_file = parsed['media']['audio'][0]  # Take first audio
                if audio_file in media_files:
                    audio_url = media_files[audio_file]
            
            # Check if we have image files
            if parsed['media']['images']:
                image_file = parsed['media']['images'][0]  # Take first image
                if image_file in media_files:
                    image_url = media_files[image_file]
        
        # Create the question object with all available data
        question_obj = {
            'id': question_id,
            'language_id': 'es',  # Spanish
            'category_id': 'grammar-conjugation',  # Will need to be updated with actual category ID
            'question_text': parsed['question'],
            'question_type': 'fill_in_blank',
            'options': [],  # Fill-in-the-blank doesn't need options
            'correct_answer': parsed['answer'],
            'correct_answer_index': None,
            'explanation': f"The correct conjugation of '{parsed.get('verb') or 'this verb'}' in this context is '{parsed['answer']}'.",
            'difficulty_level': difficulty,
            'image_url': image_url,
            'audio_url': audio_url,
            'hint': parsed.get('verb', '') if parsed.get('verb') else "Consider the context and tense markers",
            'tags': ['conjugation', 'grammar', 'spanish', 'verb'],
            'estimated_time_seconds': 15,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'metadata': {
                'verb': parsed.get('verb'),
                'tense': parsed.get('tense'),
                'person': parsed.get('person'),
                'source': 'anki_deck',
                'anki_tags': card.get('tags', ''),
                'anki_deck_id': card.get('deck_id', ''),
                'anki_card_id': card.get('id', ''),
                'media_files': parsed.get('media', {}),
                'original_sentence': parsed.get('original_sentence', ''),
                'original_fields': card.get('original_fields', [])  # Store original HTML if needed
            }
        }
        
        questions.append(question_obj)
    
    return questions

def main():
    # Path to the Anki deck
    anki_file = Path(__file__).parent.parent / 'src' / 'data' / 'spanish' / 'Ultimate_Spanish_Conjugation.apkg'
    
    # Try absolute path if relative doesn't work
    if not anki_file.exists():
        anki_file = Path('C:/Users/jessi/Projects/skilltree2/src/data/spanish/Ultimate_Spanish_Conjugation.apkg')
    
    if not anki_file.exists():
        print(f"Error: Anki file not found at {anki_file}")
        return
    
    print(f"Processing Anki deck: {anki_file}")
    
    # Extract cards from Anki deck
    print("Extracting cards from Anki deck...")
    anki_cards, media_files = extract_anki_deck(anki_file)
    print(f"Found {len(anki_cards)} cards")
    if media_files:
        print(f"Found {len(media_files)} media files")
    
    # Show a sample of cards for debugging
    if anki_cards:
        print("\nSample of extracted cards:")
        for i, card in enumerate(anki_cards[:5]):
            print(f"\nCard {i+1}:")
            print(f"  Fields: {card['fields']}")
            print(f"  Tags: {card['tags']}")
    
    # Convert to language questions format
    print("\nConverting to language questions format...")
    questions = convert_to_language_questions(anki_cards, media_files)
    print(f"Converted {len(questions)} questions")
    
    # Save to JSON file for review
    output_file = Path(__file__).parent / 'spanish_grammar_questions.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"\nQuestions saved to: {output_file}")
    
    # Show sample questions
    if questions:
        print("\nSample questions:")
        for q in questions[:3]:
            print(f"\n- Question: {q['question_text']}")
            print(f"  Answer: {q['correct_answer']}")
            print(f"  Difficulty: {q['difficulty_level']}")
            print(f"  Explanation: {q['explanation']}")
    
    # Generate SQL insert statements
    sql_file = Path(__file__).parent / 'spanish_grammar_questions.sql'
    
    with open(sql_file, 'w', encoding='utf-8') as f:
        f.write("-- Spanish Grammar Questions from Anki Deck\n")
        f.write("-- Generated on: " + datetime.now().isoformat() + "\n\n")
        
        for q in questions:
            # Escape single quotes in text fields
            question_text = q['question_text'].replace("'", "''")
            correct_answer = q['correct_answer'].replace("'", "''")
            explanation = q['explanation'].replace("'", "''")
            hint = q['hint'].replace("'", "''") if q['hint'] else ''
            
            f.write(f"""
INSERT INTO language_questions (
    id, language_id, category_id, question_text, question_type,
    options, correct_answer, correct_answer_index, explanation,
    difficulty_level, hint, tags, estimated_time_seconds,
    created_at, updated_at
) VALUES (
    '{q['id']}',
    '{q['language_id']}',
    '{q['category_id']}',
    '{question_text}',
    '{q['question_type']}',
    ARRAY[]::text[],
    '{correct_answer}',
    NULL,
    '{explanation}',
    '{q['difficulty_level']}',
    '{hint}',
    ARRAY{q['tags']}::text[],
    {q['estimated_time_seconds']},
    NOW(),
    NOW()
);
""")
    
    print(f"SQL file saved to: {sql_file}")
    
    # Create a CSV file for easier review
    csv_file = Path(__file__).parent / 'spanish_grammar_questions.csv'
    
    with open(csv_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write("Question,Answer,Difficulty,Type,Verb,Tense,Person,Has_Audio,Has_Image,Anki_Tags\n")
        
        # Write data
        for q in questions:
            metadata = q.get('metadata', {})
            has_audio = 'Yes' if q.get('audio_url') else 'No'
            has_image = 'Yes' if q.get('image_url') else 'No'
            anki_tags = metadata.get('anki_tags', '')
            
            f.write(f'"{q["question_text"]}",')
            f.write(f'"{q["correct_answer"]}",')
            f.write(f'"{q["difficulty_level"]}",')
            f.write(f'"{q["question_type"]}",')
            f.write(f'"{metadata.get("verb", "")}",')
            f.write(f'"{metadata.get("tense", "")}",')
            f.write(f'"{metadata.get("person", "")}",')
            f.write(f'"{has_audio}",')
            f.write(f'"{has_image}",')
            f.write(f'"{anki_tags}"\n')
    
    print(f"CSV file saved to: {csv_file}")
    
    print(f"\nTotal questions generated: {len(questions)}")
    print("Files created:")
    print(f"  - JSON: {output_file}")
    print(f"  - SQL: {sql_file}")
    print(f"  - CSV: {csv_file}")

if __name__ == "__main__":
    main()