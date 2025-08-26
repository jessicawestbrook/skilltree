#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Preview Spanish grammar questions before database insertion
Shows sample questions and statistics
"""

import json
import sys
import io
from pathlib import Path
from collections import Counter

# Set UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    # Load converted questions
    json_file = Path(__file__).parent / 'spanish_grammar_questions.json'
    
    if not json_file.exists():
        print(f"Error: {json_file} not found")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print("=" * 80)
    print("SPANISH GRAMMAR QUESTIONS PREVIEW")
    print("=" * 80)
    
    print(f"\nTotal Questions: {len(questions)}")
    
    # Statistics
    print("\n## Statistics ##")
    
    # Difficulty distribution
    difficulties = Counter(q['difficulty_level'] for q in questions)
    print("\nDifficulty Distribution:")
    for diff, count in sorted(difficulties.items()):
        print(f"  {diff}: {count} questions ({count*100//len(questions)}%)")
    
    # Extract verbs from metadata
    verbs = set()
    tenses = set()
    persons = set()
    
    for q in questions:
        metadata = q.get('metadata', {})
        if metadata.get('verb'):
            verbs.add(metadata['verb'])
        
        # Extract tense from tags
        tags = metadata.get('anki_tags', '').split()
        for tag in tags:
            if tag in ['presente', 'pretérito', 'imperfecto', 'futuro', 'condicional', 
                      'presente_subjuntivo', 'imperfecto_subjuntivo', 'imperativo',
                      'gerundio', 'participio', 'infinitivo']:
                tenses.add(tag)
            if tag in ['yo', 'tú', 'vos', 'él_ella_usted', 'nosotros', 'vosotros', 'ellos_ellas_ustedes']:
                persons.add(tag)
    
    print(f"\nUnique Verbs: {len(verbs)}")
    if verbs:
        print(f"  Sample verbs: {', '.join(list(verbs)[:10])}")
    
    print(f"\nTenses Covered: {len(tenses)}")
    if tenses:
        print(f"  {', '.join(sorted(tenses))}")
    
    print(f"\nPersons/Subjects: {len(persons)}")
    if persons:
        print(f"  {', '.join(sorted(persons))}")
    
    # Show sample questions
    print("\n## Sample Questions ##")
    
    # Show different types of questions
    samples = [
        ("Present tense", lambda q: 'presente' in q.get('metadata', {}).get('anki_tags', '')),
        ("Past tense", lambda q: 'pretérito' in q.get('metadata', {}).get('anki_tags', '')),
        ("Subjunctive", lambda q: 'subjuntivo' in q.get('metadata', {}).get('anki_tags', '')),
        ("Irregular verbs", lambda q: 'irregular_verb' in q.get('metadata', {}).get('anki_tags', ''))
    ]
    
    for sample_name, filter_func in samples:
        matching = [q for q in questions if filter_func(q)]
        if matching:
            q = matching[0]
            print(f"\n### {sample_name} Example ###")
            print(f"Question: {q['question_text'][:100]}...")
            print(f"Answer: {q['correct_answer']}")
            print(f"Difficulty: {q['difficulty_level']}")
            print(f"Hint: {q.get('hint', 'None')}")
            print(f"Tags: {', '.join(q.get('tags', []))}")
    
    # Show questions with special characters
    print("\n## Special Characters Check ##")
    special_chars = ['⊙', '⇠', '↧', '→', '↬']
    for char in special_chars:
        matching = [q for q in questions if char in q['question_text']]
        if matching:
            print(f"{char} symbol: Found in {len(matching)} questions")
    
    # Data quality check
    print("\n## Data Quality ##")
    
    missing_verb = sum(1 for q in questions if not q.get('metadata', {}).get('verb'))
    missing_hint = sum(1 for q in questions if not q.get('hint'))
    has_media = sum(1 for q in questions if q.get('audio_url') or q.get('image_url'))
    
    print(f"Questions without verb metadata: {missing_verb}")
    print(f"Questions without hints: {missing_hint}")
    print(f"Questions with media (audio/image): {has_media}")
    
    # Save a smaller sample for manual review
    sample_file = Path(__file__).parent / 'spanish_questions_sample.json'
    sample_questions = questions[:20]  # First 20 questions
    
    with open(sample_file, 'w', encoding='utf-8') as f:
        json.dump(sample_questions, f, ensure_ascii=False, indent=2)
    
    print(f"\n## Files Generated ##")
    print(f"Sample file (first 20 questions): {sample_file}")
    print("\nReview the sample file to verify question quality before insertion.")
    
    print("\n## Next Steps ##")
    print("1. Review the sample questions in spanish_questions_sample.json")
    print("2. Run add_language_questions_fields.sql to add missing database fields")
    print("3. Run insert_spanish_grammar_questions.py to insert all questions")

if __name__ == "__main__":
    main()