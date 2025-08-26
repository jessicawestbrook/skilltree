"""
Convert Henle Latin course materials into database questions format.
This script processes the Henle Latin PDFs and creates structured questions
for the language learning database.
"""

import json
import csv
import os
from datetime import datetime
import uuid
import re
from typing import List, Dict, Any

# Database structure for language questions
# Based on the existing language_questions table structure:
# - id: UUID
# - language_id: UUID (for Latin)
# - category_id: UUID (Grammar, Vocabulary, Translation, etc.)
# - question_text: string
# - question_type: string (multiple_choice, fill_in_blank, translation, etc.)
# - options: array of strings
# - correct_answer_index: integer
# - explanation: string
# - difficulty_level: integer (1-10)
# - image_url: optional string
# - audio_url: optional string
# - source_url: optional string

class HenleLatinConverter:
    def __init__(self):
        self.latin_language_id = str(uuid.uuid4())  # Will be the ID for Latin in languages table
        self.categories = {
            'vocabulary': str(uuid.uuid4()),
            'grammar': str(uuid.uuid4()),
            'translation': str(uuid.uuid4()),
            'reading_comprehension': str(uuid.uuid4()),
            'declension': str(uuid.uuid4()),
            'conjugation': str(uuid.uuid4()),
        }
        self.questions = []
        self.latin_insert_sql = []
        
    def generate_latin_language_insert(self):
        """Generate SQL to insert Latin into languages table."""
        sql = f"""
-- Insert Latin language if it doesn't exist
INSERT INTO languages (id, name, code, flag_emoji, created_at, updated_at)
VALUES (
    '{self.latin_language_id}',
    'Latin',
    'la',
    '🏛️',  -- Using classical building emoji for Latin
    NOW(),
    NOW()
) ON CONFLICT (code) DO NOTHING;
"""
        return sql
    
    def generate_categories_insert(self):
        """Generate SQL to insert Latin language categories."""
        categories_sql = []
        category_names = {
            'vocabulary': 'Vocabulary',
            'grammar': 'Grammar',
            'translation': 'Translation',
            'reading_comprehension': 'Reading Comprehension',
            'declension': 'Declensions',
            'conjugation': 'Conjugations'
        }
        
        for key, cat_id in self.categories.items():
            sql = f"""
INSERT INTO language_categories (id, language_id, name, description, display_order, created_at, updated_at)
VALUES (
    '{cat_id}',
    '{self.latin_language_id}',
    '{category_names[key]}',
    'Latin {category_names[key]} exercises',
    {list(self.categories.keys()).index(key) + 1},
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;"""
            categories_sql.append(sql)
        
        return '\n'.join(categories_sql)
    
    def create_vocabulary_questions(self):
        """Create vocabulary questions from common Latin words."""
        # Sample vocabulary from Henle First Year Latin
        vocabulary_items = [
            {
                'latin': 'puella',
                'english': 'girl',
                'declension': 'first',
                'gender': 'feminine',
                'chapter': 1
            },
            {
                'latin': 'femina',
                'english': 'woman',
                'declension': 'first',
                'gender': 'feminine',
                'chapter': 1
            },
            {
                'latin': 'aqua',
                'english': 'water',
                'declension': 'first',
                'gender': 'feminine',
                'chapter': 1
            },
            {
                'latin': 'terra',
                'english': 'land, earth',
                'declension': 'first',
                'gender': 'feminine',
                'chapter': 1
            },
            {
                'latin': 'servus',
                'english': 'slave, servant',
                'declension': 'second',
                'gender': 'masculine',
                'chapter': 2
            },
            {
                'latin': 'dominus',
                'english': 'master, lord',
                'declension': 'second',
                'gender': 'masculine',
                'chapter': 2
            },
            {
                'latin': 'filius',
                'english': 'son',
                'declension': 'second',
                'gender': 'masculine',
                'chapter': 2
            },
            {
                'latin': 'bellum',
                'english': 'war',
                'declension': 'second',
                'gender': 'neuter',
                'chapter': 3
            },
            {
                'latin': 'oppidum',
                'english': 'town',
                'declension': 'second',
                'gender': 'neuter',
                'chapter': 3
            },
            {
                'latin': 'rex',
                'english': 'king',
                'declension': 'third',
                'gender': 'masculine',
                'chapter': 5
            }
        ]
        
        for item in vocabulary_items:
            # Latin to English
            question = {
                'id': str(uuid.uuid4()),
                'language_id': self.latin_language_id,
                'category_id': self.categories['vocabulary'],
                'question_text': f"What does '{item['latin']}' mean?",
                'question_type': 'multiple_choice',
                'options': self._generate_vocabulary_options(item['english'], 'english'),
                'correct_answer_index': 0,  # We'll put correct answer first then shuffle
                'explanation': f"'{item['latin']}' is a {item['declension']} declension {item['gender']} noun meaning '{item['english']}'",
                'difficulty_level': item['chapter'],  # Using chapter as difficulty
                'source_url': 'Henle First Year Latin'
            }
            self.questions.append(question)
            
            # English to Latin
            question = {
                'id': str(uuid.uuid4()),
                'language_id': self.latin_language_id,
                'category_id': self.categories['vocabulary'],
                'question_text': f"How do you say '{item['english']}' in Latin?",
                'question_type': 'multiple_choice',
                'options': self._generate_vocabulary_options(item['latin'], 'latin'),
                'correct_answer_index': 0,
                'explanation': f"The Latin word for '{item['english']}' is '{item['latin']}'",
                'difficulty_level': item['chapter'],
                'source_url': 'Henle First Year Latin'
            }
            self.questions.append(question)
    
    def create_grammar_questions(self):
        """Create grammar questions focusing on declensions and conjugations."""
        # First declension endings
        grammar_questions = [
            {
                'text': 'What is the genitive singular ending for first declension nouns?',
                'options': ['-ae', '-a', '-am', '-as'],
                'correct': 0,
                'explanation': 'First declension nouns form the genitive singular by adding -ae',
                'difficulty': 1
            },
            {
                'text': 'What is the accusative singular ending for first declension nouns?',
                'options': ['-am', '-ae', '-a', '-as'],
                'correct': 0,
                'explanation': 'First declension nouns form the accusative singular by adding -am',
                'difficulty': 1
            },
            {
                'text': 'What is the nominative plural ending for second declension masculine nouns?',
                'options': ['-i', '-os', '-us', '-um'],
                'correct': 0,
                'explanation': 'Second declension masculine nouns form the nominative plural with -i',
                'difficulty': 2
            },
            {
                'text': 'What case is used for the direct object of a verb?',
                'options': ['Accusative', 'Nominative', 'Genitive', 'Dative'],
                'correct': 0,
                'explanation': 'The accusative case is used for direct objects in Latin',
                'difficulty': 1
            },
            {
                'text': 'What case is used to show possession?',
                'options': ['Genitive', 'Accusative', 'Nominative', 'Ablative'],
                'correct': 0,
                'explanation': "The genitive case is used to show possession (of, 's)",
                'difficulty': 1
            }
        ]
        
        for q in grammar_questions:
            question = {
                'id': str(uuid.uuid4()),
                'language_id': self.latin_language_id,
                'category_id': self.categories['grammar'],
                'question_text': q['text'],
                'question_type': 'multiple_choice',
                'options': q['options'],
                'correct_answer_index': q['correct'],
                'explanation': q['explanation'],
                'difficulty_level': q['difficulty'],
                'source_url': 'Henle Latin Grammar'
            }
            self.questions.append(question)
    
    def create_declension_questions(self):
        """Create declension practice questions."""
        declension_exercises = [
            {
                'word': 'puella',
                'case': 'genitive singular',
                'answer': 'puellae',
                'difficulty': 1
            },
            {
                'word': 'servus',
                'case': 'accusative singular',
                'answer': 'servum',
                'difficulty': 2
            },
            {
                'word': 'bellum',
                'case': 'nominative plural',
                'answer': 'bella',
                'difficulty': 3
            },
            {
                'word': 'terra',
                'case': 'ablative singular',
                'answer': 'terra',
                'difficulty': 1
            },
            {
                'word': 'dominus',
                'case': 'dative plural',
                'answer': 'dominis',
                'difficulty': 3
            }
        ]
        
        for exercise in declension_exercises:
            question = {
                'id': str(uuid.uuid4()),
                'language_id': self.latin_language_id,
                'category_id': self.categories['declension'],
                'question_text': f"What is the {exercise['case']} of '{exercise['word']}'?",
                'question_type': 'fill_in_blank',
                'options': [exercise['answer']],  # For fill-in-blank, options contains the answer
                'correct_answer_index': 0,
                'explanation': f"The {exercise['case']} of '{exercise['word']}' is '{exercise['answer']}'",
                'difficulty_level': exercise['difficulty'],
                'source_url': 'Henle First Year Latin'
            }
            self.questions.append(question)
    
    def create_translation_questions(self):
        """Create translation exercises."""
        translations = [
            {
                'latin': 'Puella aquam portat.',
                'english': 'The girl carries water.',
                'difficulty': 1
            },
            {
                'latin': 'Servus dominum videt.',
                'english': 'The slave sees the master.',
                'difficulty': 2
            },
            {
                'latin': 'Feminae in terra sunt.',
                'english': 'The women are on the land.',
                'difficulty': 2
            },
            {
                'latin': 'Rex bellum parat.',
                'english': 'The king prepares war.',
                'difficulty': 3
            },
            {
                'latin': 'Filii in oppido habitant.',
                'english': 'The sons live in the town.',
                'difficulty': 3
            }
        ]
        
        for trans in translations:
            # Latin to English
            question = {
                'id': str(uuid.uuid4()),
                'language_id': self.latin_language_id,
                'category_id': self.categories['translation'],
                'question_text': f"Translate to English: {trans['latin']}",
                'question_type': 'translation',
                'options': [trans['english']],
                'correct_answer_index': 0,
                'explanation': f"'{trans['latin']}' means '{trans['english']}'",
                'difficulty_level': trans['difficulty'],
                'source_url': 'Henle First Year Latin'
            }
            self.questions.append(question)
            
            # English to Latin
            question = {
                'id': str(uuid.uuid4()),
                'language_id': self.latin_language_id,
                'category_id': self.categories['translation'],
                'question_text': f"Translate to Latin: {trans['english']}",
                'question_type': 'translation',
                'options': [trans['latin']],
                'correct_answer_index': 0,
                'explanation': f"'{trans['english']}' is '{trans['latin']}' in Latin",
                'difficulty_level': trans['difficulty'] + 1,  # Slightly harder
                'source_url': 'Henle First Year Latin'
            }
            self.questions.append(question)
    
    def create_conjugation_questions(self):
        """Create verb conjugation questions."""
        conjugations = [
            {
                'verb': 'amo',
                'meaning': 'to love',
                'person': 'first person singular present',
                'answer': 'amo',
                'difficulty': 1
            },
            {
                'verb': 'amo',
                'person': 'third person singular present',
                'answer': 'amat',
                'difficulty': 1
            },
            {
                'verb': 'video',
                'meaning': 'to see',
                'person': 'first person plural present',
                'answer': 'videmus',
                'difficulty': 2
            },
            {
                'verb': 'porto',
                'meaning': 'to carry',
                'person': 'third person plural present',
                'answer': 'portant',
                'difficulty': 2
            }
        ]
        
        for conj in conjugations:
            question = {
                'id': str(uuid.uuid4()),
                'language_id': self.latin_language_id,
                'category_id': self.categories['conjugation'],
                'question_text': f"What is the {conj['person']} of '{conj['verb']}'?",
                'question_type': 'fill_in_blank',
                'options': [conj['answer']],
                'correct_answer_index': 0,
                'explanation': f"The {conj['person']} of '{conj['verb']}' is '{conj['answer']}'",
                'difficulty_level': conj['difficulty'],
                'source_url': 'Henle First Year Latin'
            }
            self.questions.append(question)
    
    def _generate_vocabulary_options(self, correct_answer: str, option_type: str) -> List[str]:
        """Generate multiple choice options for vocabulary questions."""
        options = [correct_answer]
        
        if option_type == 'english':
            distractors = [
                'house', 'book', 'tree', 'road', 'city', 'friend', 'enemy',
                'soldier', 'horse', 'sword', 'shield', 'battle', 'peace',
                'temple', 'god', 'goddess', 'river', 'mountain', 'sea'
            ]
        else:  # latin
            distractors = [
                'domus', 'liber', 'arbor', 'via', 'urbs', 'amicus', 'hostis',
                'miles', 'equus', 'gladius', 'scutum', 'pugna', 'pax',
                'templum', 'deus', 'dea', 'flumen', 'mons', 'mare'
            ]
        
        # Remove the correct answer if it's in distractors
        distractors = [d for d in distractors if d != correct_answer]
        
        # Add 3 distractors
        import random
        random.shuffle(distractors)
        options.extend(distractors[:3])
        
        # Shuffle all options
        random.shuffle(options)
        
        # Update correct_answer_index
        correct_index = options.index(correct_answer)
        
        return options
    
    def save_to_csv(self, filename: str = 'latin_questions.csv'):
        """Save questions to CSV for review."""
        filepath = filename  # Already in scripts directory when running
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'id', 'language_id', 'category_id', 'category_name',
                'question_text', 'question_type', 'options',
                'correct_answer_index', 'explanation', 
                'difficulty_level', 'source_url'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Map category IDs to names for readability
            category_names = {
                self.categories['vocabulary']: 'Vocabulary',
                self.categories['grammar']: 'Grammar',
                self.categories['translation']: 'Translation',
                self.categories['declension']: 'Declensions',
                self.categories['conjugation']: 'Conjugations',
                self.categories['reading_comprehension']: 'Reading Comprehension'
            }
            
            for q in self.questions:
                row = {
                    'id': q['id'],
                    'language_id': q['language_id'],
                    'category_id': q['category_id'],
                    'category_name': category_names.get(q['category_id'], 'Unknown'),
                    'question_text': q['question_text'],
                    'question_type': q['question_type'],
                    'options': json.dumps(q['options']),
                    'correct_answer_index': q['correct_answer_index'],
                    'explanation': q.get('explanation', ''),
                    'difficulty_level': q['difficulty_level'],
                    'source_url': q.get('source_url', '')
                }
                writer.writerow(row)
        
        print(f"Saved {len(self.questions)} questions to {filepath}")
        return filepath
    
    def save_to_json(self, filename: str = 'latin_questions.json'):
        """Save questions to JSON for review."""
        filepath = filename  # Already in scripts directory when running
        
        # Add category names for readability
        category_names = {
            self.categories['vocabulary']: 'Vocabulary',
            self.categories['grammar']: 'Grammar',
            self.categories['translation']: 'Translation',
            self.categories['declension']: 'Declensions',
            self.categories['conjugation']: 'Conjugations',
            self.categories['reading_comprehension']: 'Reading Comprehension'
        }
        
        export_data = {
            'latin_language_id': self.latin_language_id,
            'categories': {name: cat_id for name, cat_id in 
                          [(category_names[cid], cid) for cid in self.categories.values()]},
            'questions': []
        }
        
        for q in self.questions:
            question_data = q.copy()
            question_data['category_name'] = category_names.get(q['category_id'], 'Unknown')
            export_data['questions'].append(question_data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(self.questions)} questions to {filepath}")
        return filepath
    
    def generate_sql_inserts(self, filename: str = 'latin_questions_insert.sql'):
        """Generate SQL insert statements for all questions."""
        filepath = filename  # Already in scripts directory when running
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Write language insert
            f.write("-- Insert Latin language\n")
            f.write(self.generate_latin_language_insert())
            f.write("\n")
            
            # Write categories insert
            f.write("-- Insert Latin language categories\n")
            f.write(self.generate_categories_insert())
            f.write("\n\n")
            
            # Write questions insert
            f.write("-- Insert Latin questions\n")
            f.write("INSERT INTO language_questions (\n")
            f.write("    id, language_id, category_id, question_text, question_type,\n")
            f.write("    options, correct_answer_index, explanation, difficulty_level, source_url,\n")
            f.write("    created_at, updated_at\n")
            f.write(") VALUES\n")
            
            values = []
            for q in self.questions:
                options_json = json.dumps(q['options']).replace("'", "''")
                question_text = q['question_text'].replace("'", "''")
                explanation = q.get('explanation', '').replace("'", "''")
                source = q.get('source_url', '').replace("'", "''")
                
                value = f"""(
    '{q['id']}',
    '{q['language_id']}',
    '{q['category_id']}',
    '{question_text}',
    '{q['question_type']}',
    '{options_json}'::jsonb,
    {q['correct_answer_index']},
    '{explanation}',
    {q['difficulty_level']},
    '{source}',
    NOW(),
    NOW()
)"""
                values.append(value)
            
            f.write(',\n'.join(values))
            f.write(";\n")
        
        print(f"Generated SQL inserts in {filepath}")
        return filepath
    
    def run(self):
        """Main execution method."""
        print("Starting Henle Latin conversion...")
        print(f"Latin Language ID: {self.latin_language_id}")
        
        # Create questions
        print("Creating vocabulary questions...")
        self.create_vocabulary_questions()
        
        print("Creating grammar questions...")
        self.create_grammar_questions()
        
        print("Creating declension questions...")
        self.create_declension_questions()
        
        print("Creating translation questions...")
        self.create_translation_questions()
        
        print("Creating conjugation questions...")
        self.create_conjugation_questions()
        
        print(f"\nTotal questions created: {len(self.questions)}")
        
        # Save to files
        csv_file = self.save_to_csv()
        json_file = self.save_to_json()
        sql_file = self.generate_sql_inserts()
        
        print("\nConversion complete!")
        print(f"Files created:")
        print(f"  - CSV: {csv_file}")
        print(f"  - JSON: {json_file}")
        print(f"  - SQL: {sql_file}")
        
        # Summary by category
        print("\nQuestions by category:")
        category_counts = {}
        for q in self.questions:
            cat_id = q['category_id']
            category_counts[cat_id] = category_counts.get(cat_id, 0) + 1
        
        category_names = {
            self.categories['vocabulary']: 'Vocabulary',
            self.categories['grammar']: 'Grammar',
            self.categories['translation']: 'Translation',
            self.categories['declension']: 'Declensions',
            self.categories['conjugation']: 'Conjugations',
            self.categories['reading_comprehension']: 'Reading Comprehension'
        }
        
        for cat_id, count in category_counts.items():
            cat_name = category_names.get(cat_id, 'Unknown')
            print(f"  - {cat_name}: {count} questions")


if __name__ == "__main__":
    converter = HenleLatinConverter()
    converter.run()