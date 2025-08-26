"""
Convert Spanish Anki deck to questions format for database
"""
import zipfile
import sqlite3
import json
import os
import tempfile
import shutil

def extract_anki_deck(apkg_path):
    """Extract cards from an Anki deck"""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Extract the .apkg file (which is a zip)
        with zipfile.ZipFile(apkg_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Connect to the collection.anki2 SQLite database
        db_path = os.path.join(temp_dir, 'collection.anki2')
        if not os.path.exists(db_path):
            # Try alternative path
            db_path = os.path.join(temp_dir, 'collection.anki21')
        
        if not os.path.exists(db_path):
            print(f"Database not found in extracted files:")
            for file in os.listdir(temp_dir):
                print(f"  - {file}")
            return []
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # First, let's examine the table structure
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables in database: {[t[0] for t in tables]}")
        
        # Get notes (cards)
        cursor.execute("""
            SELECT id, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data FROM notes LIMIT 10
        """)
        sample_notes = cursor.fetchall()
        
        print(f"\nSample note structure:")
        for i, note in enumerate(sample_notes[:2]):
            print(f"Note {i}: {note[:6]}...")  # Show first few fields
            print(f"  Fields content: {note[6][:200]}...")
        
        # Get all notes
        cursor.execute("""
            SELECT id, flds, tags FROM notes
        """)
        notes = cursor.fetchall()
        
        cards = []
        for note_id, fields, tags in notes:
            # Fields are separated by \x1f
            field_list = fields.split('\x1f')
            
            # Skip intro/info cards
            if len(field_list) >= 2:
                first_field = field_list[0].strip()
                # Skip UUID-like entries (these are info cards)
                if not first_field.startswith(('1a04e75e', '6ec95ca3', '15d669b8', '7766a47e', 'fa7b5373')):
                    cards.append({
                        'front': first_field,
                        'back': field_list[1].strip(),
                        'extra': field_list[2].strip() if len(field_list) > 2 else '',
                        'tags': tags
                    })
        
        conn.close()
        return cards
        
    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir)

def convert_to_questions(cards):
    """Convert Anki cards to our question format"""
    questions = []
    
    # Group cards by type based on their content
    verb_conjugations = []
    
    import re
    import random
    
    for card in cards:
        front = card['front']
        back = card['back']
        
        # Skip orientation/info cards that don't have actual content
        if 'Before we begin' in back or 'Grammar words might fry' in back or 'For beginners' in back:
            continue
        
        # Remove any special characters that might cause issues
        back = back.replace('\u21ac', '->').replace('\u2192', '->').replace('\u00a0', ' ')
        
        # Check if this is a cloze deletion card (contains {{c1:: or similar)
        if '{{c' in back:
            # Extract the cloze deletion content
            cloze_pattern = r'\{\{c\d+::([^:}]+)(?:::([^}]+))?\}\}'
            matches = re.findall(cloze_pattern, back)
            
            if matches:
                for match in matches:
                    answer = match[0]  # The answer is the first group
                    hint = match[1] if len(match) > 1 and match[1] else ''  # Hint is optional
                    
                    # Clean up the sentence for the question
                    question_base = re.sub(cloze_pattern, '____', back)
                    question_base = re.sub(r'<[^>]+>', '', question_base)  # Remove HTML
                    
                    # Remove special Unicode symbols
                    question_base = question_base.replace('⊙', '').replace('⇠', '').replace('↧', '')
                    question_base = question_base.replace('〰', '').replace('↫', '').replace('→', '->')
                    question_base = question_base.replace('…', '...').replace('¡', '').replace('!', '!')
                    question_base = question_base.replace('\u2192', '->').replace('\u21ac', '->')
                    question_base = re.sub(r'\s+', ' ', question_base).strip()  # Clean up extra spaces
                    
                    # Skip if the question is too short or doesn't make sense
                    if len(question_base) < 10 or len(answer) < 1:
                        continue
                        
                    # Clean up hint as well
                    if hint:
                        hint = hint.replace('…', '...').replace('¡', '').replace('!', '!')
                        hint = re.sub(r'\s+', ' ', hint).strip()
                    
                    verb_conjugations.append({
                        'front': question_base.strip(),
                        'back': answer.strip(),
                        'hint': hint.strip(),
                        'original': back
                    })
    
    print(f"\nFound {len(verb_conjugations)} verb conjugation cards")
    
    # Show some sample cards to understand the format
    if verb_conjugations:
        print("\nSample verb cards to convert:")
        for i, conj in enumerate(verb_conjugations[:3]):
            try:
                print(f"  {i+1}. Front: {conj['front'][:80]}")
                print(f"     Back: {conj['back'][:80]}")
                if conj.get('hint'):
                    print(f"     Hint: {conj['hint'][:80]}")
            except:
                print(f"  {i+1}. [Contains special characters]")
    
    # Create fill-in-the-blank questions from conjugations
    import re
    seen_questions = set()  # Track unique questions to avoid duplicates
    
    for conj in verb_conjugations:  # Process all available conjugations
        front = conj['front']
        back = conj['back']
        hint = conj.get('hint', '')
        
        # Clean up the front text from any remaining special characters
        clean_front = front.replace('...', '').strip()
        clean_front = re.sub(r'\s+', ' ', clean_front).strip()
        
        # Create question text based on whether it's a cloze deletion or regular card
        if '____' in clean_front:
            # This is a cloze deletion - use the sentence with blank
            question_text = f"Fill in the blank: {clean_front}"
            if hint and hint.strip():
                clean_hint = hint.replace('...', '').strip()
                question_text += f" (Hint: {clean_hint})"
        else:
            # Regular card format
            question_text = f"Complete the Spanish conjugation: {clean_front}"
        
        correct_answer = back
        
        # Create a unique key for this question to avoid duplicates
        question_key = (question_text.lower(), correct_answer.lower())
        if question_key in seen_questions:
            continue  # Skip duplicate questions
        seen_questions.add(question_key)
        
        # Generate plausible wrong options based on common patterns
        options = [correct_answer]
        
        # Add variations with different endings
        if correct_answer.endswith('o'):
            options.extend([
                correct_answer[:-1] + 'a',
                correct_answer[:-1] + 'e', 
                correct_answer[:-1] + 'as'
            ])
        elif correct_answer.endswith('a'):
            options.extend([
                correct_answer[:-1] + 'o',
                correct_answer[:-1] + 'e',
                correct_answer[:-1] + 'an'
            ])
        elif correct_answer.endswith('e'):
            options.extend([
                correct_answer[:-1] + 'a',
                correct_answer[:-1] + 'o',
                correct_answer[:-1] + 'en'
            ])
        elif correct_answer.endswith('s'):
            options.extend([
                correct_answer[:-1],
                correct_answer[:-1] + 'n',
                correct_answer + 'e'
            ])
        else:
            # Generic variations
            options.extend([
                correct_answer + 's',
                correct_answer + 'n',
                correct_answer + 'mos'
            ])
        
        # Ensure we have 4 unique options
        options = list(dict.fromkeys(options))[:4]
        
        # If we don't have enough options, add some generic ones
        while len(options) < 4:
            if correct_answer.endswith('ar'):
                options.append(correct_answer[:-2] + 'ando')
            elif correct_answer.endswith('er') or correct_answer.endswith('ir'):
                options.append(correct_answer[:-2] + 'iendo')
            else:
                options.append(correct_answer + 'r')
        
        # Parse the context to create better explanations
        explanation = f"The correct answer is '{correct_answer}'"
        
        # Identify the verb and tense from the context
        if hint and 'ser' in hint.lower():
            verb_infinitive = "ser (to be)"
        elif hint and 'haber' in hint.lower():
            verb_infinitive = "haber (to have)"
        elif hint and 'estar' in hint.lower():
            verb_infinitive = "estar (to be - temporary state)"
        else:
            verb_infinitive = "the verb"
        
        # Identify the subject from the question
        if 'yo' in question_text:
            subject = "first person singular (yo)"
        elif 'tú' in question_text:
            subject = "second person singular informal (tú)"
        elif 'vos' in question_text:
            subject = "second person singular (vos - used in some regions)"
        elif 'él/ella/usted' in question_text:
            subject = "third person singular (él/ella/usted)"
        elif 'nosotros' in question_text:
            subject = "first person plural (nosotros)"
        elif 'vosotros' in question_text:
            subject = "second person plural informal (vosotros - used in Spain)"
        elif 'ellos/ellas/ustedes' in question_text:
            subject = "third person plural (ellos/ellas/ustedes)"
        else:
            subject = "this subject"
        
        # Identify the tense from context clues
        tense = "present tense"
        if 'Ahora mismo' in question_text or '⊙' in front:
            tense = "present tense"
        elif 'En esa época' in question_text or '⇠' in front:
            tense = "imperfect tense (ongoing past action)"
        elif 'En aquel momento' in question_text or '↧' in front:
            tense = "preterite tense (completed past action)"
        elif 'En el futuro' in question_text or '->' in front:
            tense = "future tense"
        elif 'Si ocurriese' in question_text or 'Si sucediera' in question_text or '…' in front:
            tense = "conditional tense"
        elif 'Resulta divertido que' in question_text or '〰' in front:
            tense = "present subjunctive"
        elif 'Fue sorprendente que' in question_text or '↫' in front:
            tense = "imperfect subjunctive"
        elif 'ha ' in question_text or 'he ' in question_text or 'has ' in question_text:
            tense = "present perfect tense"
        elif 'había' in question_text:
            tense = "past perfect tense (pluperfect)"
        elif '¡' in question_text:
            tense = "imperative mood (command)"
        
        # Create a more informative explanation
        explanation = f"'{correct_answer}' is the {tense} conjugation of {verb_infinitive} for {subject}."
        
        # Add specific conjugation patterns when relevant
        if correct_answer.endswith('mos'):
            explanation += " The -mos ending is characteristic of first person plural (nosotros) forms."
        elif correct_answer.endswith('áis') or correct_answer.endswith('éis'):
            explanation += " This ending is specific to vosotros forms used in Spain."
        elif correct_answer.endswith('n') and 'ellos' in question_text:
            explanation += " The -n ending indicates third person plural."
        
        # Take only 4 options
        final_options = options[:4]
        
        # Randomize the position of the correct answer
        import random
        random.shuffle(final_options)
        correct_index = final_options.index(correct_answer)
        
        questions.append({
            'question_text': question_text,
            'question_type': 'multiple_choice',
            'options': final_options,
            'correct_answer': correct_index,  # Index of correct answer after shuffling
            'explanation': explanation,
            'difficulty': 'medium',
            'category': 'Spanish Verb Conjugations'
        })
        
        # No limit - convert all available cards
        # if len(questions) >= 2000:
        #     break
    
    return questions

def main():
    apkg_path = 'src/data/spanish/Ultimate_Spanish_Conjugation.apkg'
    
    if not os.path.exists(apkg_path):
        print(f"Error: File not found: {apkg_path}")
        return
    
    print(f"Extracting Anki deck from {apkg_path}...")
    cards = extract_anki_deck(apkg_path)
    
    print(f"Found {len(cards)} cards in the deck")
    
    if cards:
        # Show sample cards
        print("\nSample cards:")
        for i, card in enumerate(cards[:5]):
            print(f"\nCard {i+1}:")
            try:
                print(f"  Front: {card['front'][:100]}...")
                print(f"  Back: {card['back'][:100]}...")
                if card.get('extra'):
                    print(f"  Extra: {card['extra'][:100]}...")
            except UnicodeEncodeError:
                print(f"  Front: [Contains special characters]")
                print(f"  Back: [Contains special characters]")
    
    print("\nConverting to question format...")
    questions = convert_to_questions(cards)
    
    print(f"Generated {len(questions)} questions")
    
    # Save to JSON for review
    output_file = 'scripts/spanish_data/anki_spanish_questions.json'
    os.makedirs('scripts/spanish_data', exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"\nQuestions saved to {output_file}")
    
    # Show sample questions
    if questions:
        print("\nSample questions:")
        for i, q in enumerate(questions[:3]):
            print(f"\nQuestion {i+1}:")
            print(f"  Text: {q['question_text']}")
            print(f"  Options: {q['options']}")
            print(f"  Correct: {q['options'][q['correct_answer']]}")

if __name__ == "__main__":
    main()