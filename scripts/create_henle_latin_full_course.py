"""
Create a full Henle Latin course with chapters, learning content, and exercises.
This creates a structured curriculum following the Henle First Year Latin textbook.
"""

import json
import csv
import uuid
from datetime import datetime
from typing import List, Dict, Any

class HenleLatinCourse:
    def __init__(self):
        self.latin_language_id = str(uuid.uuid4())
        self.course_id = str(uuid.uuid4())
        self.categories = {
            'vocabulary': str(uuid.uuid4()),
            'grammar': str(uuid.uuid4()),
            'translation': str(uuid.uuid4()),
            'reading_comprehension': str(uuid.uuid4()),
            'declension': str(uuid.uuid4()),
            'conjugation': str(uuid.uuid4()),
        }
        
        # Full course structure
        self.course_structure = []
        self.learning_content = []
        self.questions = []
        self.chapters = []
        
    def create_course_structure(self):
        """Create the full Henle Latin First Year course structure."""
        
        # Course metadata
        course_meta = {
            'id': self.course_id,
            'language_id': self.latin_language_id,
            'name': 'Henle Latin First Year',
            'description': 'A comprehensive Latin course based on Henle First Year Latin textbook',
            'level': 'Beginner to Intermediate',
            'estimated_hours': 120,
            'chapters': []
        }
        
        # Chapter 1: First Declension
        chapter1 = self.create_chapter_1()
        course_meta['chapters'].append(chapter1)
        
        # Chapter 2: Second Declension Masculine
        chapter2 = self.create_chapter_2()
        course_meta['chapters'].append(chapter2)
        
        # Chapter 3: Second Declension Neuter
        chapter3 = self.create_chapter_3()
        course_meta['chapters'].append(chapter3)
        
        # Chapter 4: Adjectives of First and Second Declension
        chapter4 = self.create_chapter_4()
        course_meta['chapters'].append(chapter4)
        
        # Chapter 5: Present Tense of Sum
        chapter5 = self.create_chapter_5()
        course_meta['chapters'].append(chapter5)
        
        return course_meta
    
    def create_chapter_1(self):
        """Chapter 1: First Declension Nouns"""
        chapter = {
            'id': str(uuid.uuid4()),
            'number': 1,
            'title': 'First Declension Nouns',
            'description': 'Introduction to Latin nouns of the first declension',
            'sections': []
        }
        
        # Section 1: Introduction to Cases
        section1 = {
            'id': str(uuid.uuid4()),
            'number': 1,
            'title': 'Introduction to Latin Cases',
            'type': 'learning_content',
            'content': {
                'text': """
# Introduction to Latin Cases

Latin is an inflected language, meaning that the endings of words change to show their function in a sentence. Nouns in Latin have six cases:

## The Six Cases

1. **Nominative** - Subject of the sentence
   - Example: *Puella* cantat. (The girl sings.)

2. **Genitive** - Possession (of, 's)
   - Example: Liber *puellae* (The girl's book)

3. **Dative** - Indirect object (to, for)
   - Example: Do librum *puellae*. (I give the book to the girl.)

4. **Accusative** - Direct object
   - Example: Video *puellam*. (I see the girl.)

5. **Ablative** - Various uses (by, with, from, in)
   - Example: Ambulo cum *puella*. (I walk with the girl.)

6. **Vocative** - Direct address
   - Example: *Puella*, veni! (Girl, come!)

## Why Cases Matter

Unlike English, which relies on word order, Latin uses these case endings to show relationships between words. This means Latin has much more flexible word order than English.
                """,
                'examples': [
                    'Puella aquam portat. (The girl carries water.)',
                    'Aquam puella portat. (The girl carries water.) - Same meaning, different emphasis'
                ],
                'key_points': [
                    'Case endings show the function of nouns in sentences',
                    'Word order in Latin is flexible',
                    'Each case has specific uses and meanings'
                ]
            }
        }
        
        # Section 2: First Declension Endings
        section2 = {
            'id': str(uuid.uuid4()),
            'number': 2,
            'title': 'First Declension Endings',
            'type': 'learning_content',
            'content': {
                'text': """
# First Declension Endings

The first declension includes mostly feminine nouns ending in -a. Here are the endings:

## Singular
- Nominative: -a
- Genitive: -ae
- Dative: -ae
- Accusative: -am
- Ablative: -ā (long a)
- Vocative: -a

## Plural
- Nominative: -ae
- Genitive: -ārum
- Dative: -īs
- Accusative: -ās
- Ablative: -īs
- Vocative: -ae

## Example: puella (girl)

### Singular
- Nom: puella (the girl - subject)
- Gen: puellae (of the girl)
- Dat: puellae (to/for the girl)
- Acc: puellam (the girl - object)
- Abl: puellā (by/with/from the girl)
- Voc: puella (O girl!)

### Plural
- Nom: puellae (the girls - subject)
- Gen: puellārum (of the girls)
- Dat: puellīs (to/for the girls)
- Acc: puellās (the girls - object)
- Abl: puellīs (by/with/from the girls)
- Voc: puellae (O girls!)
                """,
                'examples': [
                    'terra, terrae (f.) - land, earth',
                    'aqua, aquae (f.) - water',
                    'femina, feminae (f.) - woman',
                    'porta, portae (f.) - gate'
                ],
                'key_points': [
                    'Most first declension nouns are feminine',
                    'The genitive singular ending -ae identifies first declension',
                    'Some endings are the same (dative and ablative plural)'
                ]
            }
        }
        
        # Practice exercises for Chapter 1
        exercises1 = {
            'id': str(uuid.uuid4()),
            'number': 3,
            'title': 'Practice: First Declension Cases',
            'type': 'exercises',
            'question_ids': []  # Will be filled with actual question IDs
        }
        
        # Generate questions for this section
        ch1_questions = self.generate_chapter_1_questions()
        exercises1['question_ids'] = [q['id'] for q in ch1_questions[:5]]
        self.questions.extend(ch1_questions)
        
        # Vocabulary section
        vocab_section = {
            'id': str(uuid.uuid4()),
            'number': 4,
            'title': 'Chapter 1 Vocabulary',
            'type': 'learning_content',
            'content': {
                'text': """
# Chapter 1 Vocabulary

## First Declension Nouns

1. **aqua, aquae** (f.) - water
2. **femina, feminae** (f.) - woman
3. **patria, patriae** (f.) - fatherland, country
4. **porta, portae** (f.) - gate
5. **puella, puellae** (f.) - girl
6. **terra, terrae** (f.) - land, earth
7. **vita, vitae** (f.) - life

## Verbs (Preview)

1. **porto, portare** - to carry
2. **laudo, laudare** - to praise
3. **amo, amare** - to love

## Prepositions

1. **in** + ablative - in, on
2. **in** + accusative - into
3. **cum** + ablative - with
                """,
                'vocabulary_list': [
                    {'latin': 'aqua', 'english': 'water', 'gender': 'f', 'declension': '1st'},
                    {'latin': 'femina', 'english': 'woman', 'gender': 'f', 'declension': '1st'},
                    {'latin': 'patria', 'english': 'fatherland', 'gender': 'f', 'declension': '1st'},
                    {'latin': 'porta', 'english': 'gate', 'gender': 'f', 'declension': '1st'},
                    {'latin': 'puella', 'english': 'girl', 'gender': 'f', 'declension': '1st'},
                    {'latin': 'terra', 'english': 'land', 'gender': 'f', 'declension': '1st'},
                    {'latin': 'vita', 'english': 'life', 'gender': 'f', 'declension': '1st'}
                ]
            }
        }
        
        # Vocabulary practice
        vocab_practice = {
            'id': str(uuid.uuid4()),
            'number': 5,
            'title': 'Vocabulary Practice',
            'type': 'exercises',
            'question_ids': []  # Will be filled with vocabulary question IDs
        }
        
        vocab_questions = self.generate_vocabulary_questions_for_chapter(1)
        vocab_practice['question_ids'] = [q['id'] for q in vocab_questions[:5]]
        self.questions.extend(vocab_questions)
        
        chapter['sections'] = [section1, section2, exercises1, vocab_section, vocab_practice]
        return chapter
    
    def create_chapter_2(self):
        """Chapter 2: Second Declension Masculine"""
        chapter = {
            'id': str(uuid.uuid4()),
            'number': 2,
            'title': 'Second Declension Masculine Nouns',
            'description': 'Learn masculine nouns of the second declension',
            'sections': []
        }
        
        # Section 1: Second Declension Introduction
        section1 = {
            'id': str(uuid.uuid4()),
            'number': 1,
            'title': 'Second Declension Masculine',
            'type': 'learning_content',
            'content': {
                'text': """
# Second Declension Masculine Nouns

The second declension includes mostly masculine nouns ending in -us or -er.

## Endings for -us nouns

### Singular
- Nominative: -us
- Genitive: -ī
- Dative: -ō
- Accusative: -um
- Ablative: -ō
- Vocative: -e

### Plural
- Nominative: -ī
- Genitive: -ōrum
- Dative: -īs
- Accusative: -ōs
- Ablative: -īs
- Vocative: -ī

## Example: servus (slave, servant)

### Singular
- Nom: servus (the slave)
- Gen: servī (of the slave)
- Dat: servō (to/for the slave)
- Acc: servum (the slave - object)
- Abl: servō (by/with/from the slave)
- Voc: serve (O slave!)

### Plural
- Nom: servī (the slaves)
- Gen: servōrum (of the slaves)
- Dat: servīs (to/for the slaves)
- Acc: servōs (the slaves - object)
- Abl: servīs (by/with/from the slaves)
- Voc: servī (O slaves!)
                """,
                'examples': [
                    'dominus, dominī (m.) - master, lord',
                    'filius, filiī (m.) - son',
                    'amicus, amicī (m.) - friend'
                ],
                'key_points': [
                    'Second declension -us nouns are mostly masculine',
                    'The genitive singular ending -ī identifies second declension',
                    'Vocative singular has special ending -e'
                ]
            }
        }
        
        # Section 2: -er type nouns
        section2 = {
            'id': str(uuid.uuid4()),
            'number': 2,
            'title': 'Second Declension -er Nouns',
            'type': 'learning_content',
            'content': {
                'text': """
# Second Declension -er Nouns

Some second declension masculine nouns end in -er. They follow the same pattern except in the nominative and vocative singular.

## Two types of -er nouns:

1. **Those that keep the e**: puer, puerī (boy)
2. **Those that drop the e**: ager, agrī (field)

## Example: puer (boy) - keeps the e

### Singular
- Nom: puer
- Gen: puerī
- Dat: puerō
- Acc: puerum
- Abl: puerō
- Voc: puer

## Example: ager (field) - drops the e

### Singular
- Nom: ager
- Gen: agrī (note: no e!)
- Dat: agrō
- Acc: agrum
- Abl: agrō
- Voc: ager

The genitive tells you whether to keep or drop the e in other forms.
                """,
                'examples': [
                    'liber, librī (m.) - book (drops e)',
                    'magister, magistrī (m.) - teacher (drops e)',
                    'vir, virī (m.) - man (irregular)'
                ]
            }
        }
        
        # Practice exercises
        exercises = {
            'id': str(uuid.uuid4()),
            'number': 3,
            'title': 'Practice: Second Declension Masculine',
            'type': 'exercises',
            'question_ids': []
        }
        
        ch2_questions = self.generate_chapter_2_questions()
        exercises['question_ids'] = [q['id'] for q in ch2_questions[:5]]
        self.questions.extend(ch2_questions)
        
        chapter['sections'] = [section1, section2, exercises]
        return chapter
    
    def create_chapter_3(self):
        """Chapter 3: Second Declension Neuter"""
        chapter = {
            'id': str(uuid.uuid4()),
            'number': 3,
            'title': 'Second Declension Neuter Nouns',
            'description': 'Learn neuter nouns of the second declension',
            'sections': []
        }
        
        section1 = {
            'id': str(uuid.uuid4()),
            'number': 1,
            'title': 'Second Declension Neuter',
            'type': 'learning_content',
            'content': {
                'text': """
# Second Declension Neuter Nouns

Neuter nouns of the second declension end in -um. They follow a similar pattern to masculine nouns with important differences.

## Key Rule for All Neuter Nouns
**Nominative and Accusative are always the same!**
**Nominative and Accusative plural always end in -a!**

## Endings

### Singular
- Nominative: -um
- Genitive: -ī
- Dative: -ō
- Accusative: -um (same as nominative!)
- Ablative: -ō
- Vocative: -um

### Plural
- Nominative: -a
- Genitive: -ōrum
- Dative: -īs
- Accusative: -a (same as nominative!)
- Ablative: -īs
- Vocative: -a

## Example: bellum (war)

### Singular
- Nom: bellum
- Gen: bellī
- Dat: bellō
- Acc: bellum
- Abl: bellō
- Voc: bellum

### Plural
- Nom: bella
- Gen: bellōrum
- Dat: bellīs
- Acc: bella
- Abl: bellīs
- Voc: bella
                """,
                'examples': [
                    'oppidum, oppidī (n.) - town',
                    'regnum, regnī (n.) - kingdom',
                    'donum, donī (n.) - gift'
                ]
            }
        }
        
        exercises = {
            'id': str(uuid.uuid4()),
            'number': 2,
            'title': 'Practice: Neuter Nouns',
            'type': 'exercises',
            'question_ids': []
        }
        
        ch3_questions = self.generate_chapter_3_questions()
        exercises['question_ids'] = [q['id'] for q in ch3_questions[:5]]
        self.questions.extend(ch3_questions)
        
        chapter['sections'] = [section1, exercises]
        return chapter
    
    def create_chapter_4(self):
        """Chapter 4: Adjectives"""
        chapter = {
            'id': str(uuid.uuid4()),
            'number': 4,
            'title': 'Adjectives of First and Second Declension',
            'description': 'Learn how adjectives agree with nouns',
            'sections': []
        }
        
        section1 = {
            'id': str(uuid.uuid4()),
            'number': 1,
            'title': 'Adjective Agreement',
            'type': 'learning_content',
            'content': {
                'text': """
# Adjectives of First and Second Declension

Adjectives must agree with the nouns they modify in:
- **Gender** (masculine, feminine, neuter)
- **Number** (singular, plural)
- **Case** (nominative, genitive, etc.)

## Forms of bonus, bona, bonum (good)

### Masculine (2nd declension)
- Nom: bonus
- Gen: bonī
- Dat: bonō
- Acc: bonum
- Abl: bonō

### Feminine (1st declension)
- Nom: bona
- Gen: bonae
- Dat: bonae
- Acc: bonam
- Abl: bonā

### Neuter (2nd declension)
- Nom: bonum
- Gen: bonī
- Dat: bonō
- Acc: bonum
- Abl: bonō

## Examples of Agreement

- **Masculine**: servus bonus (good slave)
- **Feminine**: puella bona (good girl)
- **Neuter**: bellum bonum (good war)

The adjective changes its ending to match the noun!
                """,
                'examples': [
                    'magnus, magna, magnum - large, great',
                    'parvus, parva, parvum - small',
                    'malus, mala, malum - bad, evil'
                ]
            }
        }
        
        chapter['sections'] = [section1]
        return chapter
    
    def create_chapter_5(self):
        """Chapter 5: The Verb Sum"""
        chapter = {
            'id': str(uuid.uuid4()),
            'number': 5,
            'title': 'The Verb Sum (to be)',
            'description': 'Learn the present tense of the important irregular verb sum',
            'sections': []
        }
        
        section1 = {
            'id': str(uuid.uuid4()),
            'number': 1,
            'title': 'Present Tense of Sum',
            'type': 'learning_content',
            'content': {
                'text': """
# The Verb Sum (to be)

Sum is one of the most important and most irregular verbs in Latin.

## Present Tense

### Singular
- 1st person: **sum** (I am)
- 2nd person: **es** (you are)
- 3rd person: **est** (he/she/it is)

### Plural
- 1st person: **sumus** (we are)
- 2nd person: **estis** (you are)
- 3rd person: **sunt** (they are)

## Usage

Sum is used:
1. To show existence: *Est puella.* (There is a girl.)
2. With predicate nominatives: *Puella est bona.* (The girl is good.)
3. To show location: *In terra sunt.* (They are on the land.)

## Important: Predicate Nominatives

When sum links two nouns or a noun and adjective, both are in the nominative case:
- *Marcus est servus.* (Marcus is a slave.) - Both Marcus and servus are nominative
- *Puellae sunt bonae.* (The girls are good.) - Both match in nominative plural
                """,
                'examples': [
                    'Sum discipulus. (I am a student.)',
                    'Estis amici. (You are friends.)',
                    'Bella sunt mala. (Wars are bad.)'
                ]
            }
        }
        
        exercises = {
            'id': str(uuid.uuid4()),
            'number': 2,
            'title': 'Practice: Sum',
            'type': 'exercises',
            'question_ids': []
        }
        
        sum_questions = self.generate_sum_questions()
        exercises['question_ids'] = [q['id'] for q in sum_questions[:5]]
        self.questions.extend(sum_questions)
        
        chapter['sections'] = [section1, exercises]
        return chapter
    
    def generate_chapter_1_questions(self):
        """Generate questions for Chapter 1"""
        questions = []
        
        # Identify the case questions
        case_questions = [
            {
                'word': 'puellam',
                'correct_case': 'Accusative singular',
                'options': ['Accusative singular', 'Nominative singular', 'Genitive singular', 'Ablative singular']
            },
            {
                'word': 'puellae',
                'correct_case': 'Genitive singular',
                'options': ['Genitive singular', 'Nominative plural', 'Dative singular', 'Vocative plural'],
                'note': 'Could also be dative singular or nominative plural'
            },
            {
                'word': 'puellis',
                'correct_case': 'Dative plural',
                'options': ['Dative plural', 'Nominative plural', 'Accusative plural', 'Genitive plural'],
                'note': 'Could also be ablative plural'
            }
        ]
        
        for q in case_questions:
            question = {
                'id': str(uuid.uuid4()),
                'language_id': self.latin_language_id,
                'category_id': self.categories['declension'],
                'question_text': f"What case is '{q['word']}'?",
                'question_type': 'multiple_choice',
                'options': q['options'],
                'correct_answer_index': q['options'].index(q['correct_case']),
                'explanation': q.get('note', f"'{q['word']}' is {q['correct_case']}"),
                'difficulty_level': 1,
                'chapter': 1,
                'source_url': 'Henle First Year Latin - Chapter 1'
            }
            questions.append(question)
        
        # Declension practice
        declension_practice = [
            {'base': 'terra', 'case': 'accusative singular', 'answer': 'terram'},
            {'base': 'aqua', 'case': 'genitive plural', 'answer': 'aquarum'},
            {'base': 'femina', 'case': 'dative singular', 'answer': 'feminae'}
        ]
        
        for item in declension_practice:
            question = {
                'id': str(uuid.uuid4()),
                'language_id': self.latin_language_id,
                'category_id': self.categories['declension'],
                'question_text': f"Form the {item['case']} of '{item['base']}'",
                'question_type': 'fill_in_blank',
                'options': [item['answer']],
                'correct_answer_index': 0,
                'explanation': f"The {item['case']} of '{item['base']}' is '{item['answer']}'",
                'difficulty_level': 1,
                'chapter': 1,
                'source_url': 'Henle First Year Latin - Chapter 1'
            }
            questions.append(question)
        
        return questions
    
    def generate_chapter_2_questions(self):
        """Generate questions for Chapter 2"""
        questions = []
        
        # Second declension masculine
        declension_practice = [
            {'base': 'servus', 'case': 'genitive singular', 'answer': 'servi'},
            {'base': 'dominus', 'case': 'accusative plural', 'answer': 'dominos'},
            {'base': 'filius', 'case': 'vocative singular', 'answer': 'fili'},
            {'base': 'amicus', 'case': 'ablative singular', 'answer': 'amico'}
        ]
        
        for item in declension_practice:
            question = {
                'id': str(uuid.uuid4()),
                'language_id': self.latin_language_id,
                'category_id': self.categories['declension'],
                'question_text': f"Form the {item['case']} of '{item['base']}'",
                'question_type': 'fill_in_blank',
                'options': [item['answer']],
                'correct_answer_index': 0,
                'explanation': f"The {item['case']} of '{item['base']}' is '{item['answer']}'",
                'difficulty_level': 2,
                'chapter': 2,
                'source_url': 'Henle First Year Latin - Chapter 2'
            }
            questions.append(question)
        
        return questions
    
    def generate_chapter_3_questions(self):
        """Generate questions for Chapter 3"""
        questions = []
        
        # Neuter noun questions
        neuter_questions = [
            {
                'text': 'What is special about neuter nouns?',
                'options': [
                    'Nominative and accusative are always the same',
                    'They have no plural forms',
                    'They only use three cases',
                    'They never change endings'
                ],
                'correct': 0,
                'explanation': 'In all neuter nouns, nominative and accusative forms are identical'
            },
            {
                'text': 'What is the nominative plural ending for neuter nouns?',
                'options': ['-a', '-um', '-i', '-os'],
                'correct': 0,
                'explanation': 'All neuter nouns have -a in nominative and accusative plural'
            }
        ]
        
        for q in neuter_questions:
            question = {
                'id': str(uuid.uuid4()),
                'language_id': self.latin_language_id,
                'category_id': self.categories['grammar'],
                'question_text': q['text'],
                'question_type': 'multiple_choice',
                'options': q['options'],
                'correct_answer_index': q['correct'],
                'explanation': q['explanation'],
                'difficulty_level': 3,
                'chapter': 3,
                'source_url': 'Henle First Year Latin - Chapter 3'
            }
            questions.append(question)
        
        return questions
    
    def generate_sum_questions(self):
        """Generate questions about the verb sum"""
        questions = []
        
        conjugations = [
            {'person': 'I am', 'latin': 'sum'},
            {'person': 'you are (singular)', 'latin': 'es'},
            {'person': 'he/she/it is', 'latin': 'est'},
            {'person': 'we are', 'latin': 'sumus'},
            {'person': 'they are', 'latin': 'sunt'}
        ]
        
        for conj in conjugations:
            question = {
                'id': str(uuid.uuid4()),
                'language_id': self.latin_language_id,
                'category_id': self.categories['conjugation'],
                'question_text': f"How do you say '{conj['person']}' in Latin?",
                'question_type': 'fill_in_blank',
                'options': [conj['latin']],
                'correct_answer_index': 0,
                'explanation': f"'{conj['person']}' is '{conj['latin']}' in Latin",
                'difficulty_level': 5,
                'chapter': 5,
                'source_url': 'Henle First Year Latin - Chapter 5'
            }
            questions.append(question)
        
        return questions
    
    def generate_vocabulary_questions_for_chapter(self, chapter_num):
        """Generate vocabulary questions for a specific chapter"""
        questions = []
        
        # Chapter 1 vocabulary
        if chapter_num == 1:
            vocab = [
                {'latin': 'aqua', 'english': 'water'},
                {'latin': 'femina', 'english': 'woman'},
                {'latin': 'porta', 'english': 'gate'},
                {'latin': 'puella', 'english': 'girl'},
                {'latin': 'terra', 'english': 'land, earth'}
            ]
            
            for item in vocab:
                # Latin to English
                question = {
                    'id': str(uuid.uuid4()),
                    'language_id': self.latin_language_id,
                    'category_id': self.categories['vocabulary'],
                    'question_text': f"What does '{item['latin']}' mean?",
                    'question_type': 'multiple_choice',
                    'options': self._generate_vocab_options(item['english'], 'english'),
                    'correct_answer_index': 0,
                    'explanation': f"'{item['latin']}' means '{item['english']}'",
                    'difficulty_level': 1,
                    'chapter': 1,
                    'source_url': 'Henle First Year Latin - Chapter 1'
                }
                questions.append(question)
        
        return questions
    
    def _generate_vocab_options(self, correct, lang_type):
        """Generate vocabulary multiple choice options"""
        import random
        
        options = [correct]
        if lang_type == 'english':
            distractors = ['house', 'book', 'tree', 'road', 'friend', 'soldier', 'temple']
        else:
            distractors = ['domus', 'liber', 'arbor', 'via', 'amicus', 'miles', 'templum']
        
        random.shuffle(distractors)
        options.extend([d for d in distractors if d != correct][:3])
        random.shuffle(options)
        
        return options
    
    def save_course_structure(self, filename='henle_latin_course_structure.json'):
        """Save the complete course structure to JSON"""
        course = self.create_course_structure()
        
        output = {
            'course': course,
            'total_questions': len(self.questions),
            'total_chapters': len(course['chapters']),
            'categories': self.categories,
            'language_id': self.latin_language_id
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"Saved course structure to {filename}")
        return filename
    
    def save_questions_csv(self, filename='henle_latin_full_questions.csv'):
        """Save all questions to CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'id', 'language_id', 'category_id', 'chapter',
                'question_text', 'question_type', 'options',
                'correct_answer_index', 'explanation', 
                'difficulty_level', 'source_url'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for q in self.questions:
                row = {
                    'id': q['id'],
                    'language_id': q['language_id'],
                    'category_id': q['category_id'],
                    'chapter': q.get('chapter', ''),
                    'question_text': q['question_text'],
                    'question_type': q['question_type'],
                    'options': json.dumps(q['options']),
                    'correct_answer_index': q['correct_answer_index'],
                    'explanation': q.get('explanation', ''),
                    'difficulty_level': q['difficulty_level'],
                    'source_url': q.get('source_url', '')
                }
                writer.writerow(row)
        
        print(f"Saved {len(self.questions)} questions to {filename}")
        return filename
    
    def generate_sql_course_insert(self, filename='henle_latin_course.sql'):
        """Generate SQL to insert the course structure"""
        course = self.create_course_structure()
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Insert language
            f.write(f"""
-- Insert Latin language if not exists
INSERT INTO languages (id, name, code, flag_emoji, created_at, updated_at)
VALUES (
    '{self.latin_language_id}',
    'Latin',
    'la',
    '🏛️',
    NOW(),
    NOW()
) ON CONFLICT (code) DO NOTHING;

-- Insert language categories
""")
            
            # Insert categories
            category_names = {
                'vocabulary': 'Vocabulary',
                'grammar': 'Grammar', 
                'translation': 'Translation',
                'reading_comprehension': 'Reading Comprehension',
                'declension': 'Declensions',
                'conjugation': 'Conjugations'
            }
            
            for key, cat_id in self.categories.items():
                f.write(f"""
INSERT INTO language_categories (id, language_id, name, description, display_order, created_at, updated_at)
VALUES (
    '{cat_id}',
    '{self.latin_language_id}',
    '{category_names[key]}',
    'Latin {category_names[key]} exercises',
    {list(self.categories.keys()).index(key) + 1},
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;
""")
            
            # Insert course
            f.write(f"""
-- Insert Henle Latin course
INSERT INTO language_courses (
    id, language_id, name, description, level, 
    estimated_hours, created_at, updated_at
) VALUES (
    '{self.course_id}',
    '{self.latin_language_id}',
    'Henle Latin First Year',
    'A comprehensive Latin course based on Henle First Year Latin textbook',
    'Beginner to Intermediate',
    120,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;
""")
            
            # Insert questions FIRST (before linking them to modules)
            f.write("\n-- Insert Latin questions\n")
            f.write("INSERT INTO language_questions (\n")
            f.write("    id, language_id, category_id, question_text, question_type,\n")
            f.write("    options, correct_answer_index, explanation, difficulty_level,\n")
            f.write("    source_url, created_at, updated_at\n")
            f.write(") VALUES\n")
            
            values = []
            for q in self.questions:
                # Format options as PostgreSQL array literal
                escaped_options = []
                for opt in q['options']:
                    escaped_opt = opt.replace("'", "''")
                    escaped_options.append(f"'{escaped_opt}'")
                options_array = 'ARRAY[' + ', '.join(escaped_options) + ']'
                
                question_text = q['question_text'].replace("'", "''")
                explanation = q.get('explanation', '').replace("'", "''")
                source = q.get('source_url', '').replace("'", "''")
                
                value = f"""(
    '{q['id']}',
    '{q['language_id']}',
    '{q['category_id']}',
    '{question_text}',
    '{q['question_type']}',
    {options_array},
    {q['correct_answer_index']},
    '{explanation}',
    {q['difficulty_level']},
    '{source}',
    NOW(),
    NOW()
)"""
                values.append(value)
            
            f.write(',\n'.join(values))
            f.write("\nON CONFLICT DO NOTHING;\n")
            
            # NOW insert chapters as course modules
            f.write("\n-- Insert course chapters/modules\n")
            for chapter in course['chapters']:
                f.write(f"""
INSERT INTO course_modules (
    id, course_id, chapter_number, title, description,
    created_at, updated_at
) VALUES (
    '{chapter['id']}',
    '{self.course_id}',
    {chapter['number']},
    '{chapter['title']}',
    '{chapter['description']}',
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;
""")
                
                # Insert sections as learning content
                for section in chapter['sections']:
                    if section['type'] == 'learning_content':
                        content_json = json.dumps(section['content']).replace("'", "''")
                        f.write(f"""
INSERT INTO module_content (
    id, module_id, section_number, title, content_type,
    content, created_at, updated_at
) VALUES (
    '{section['id']}',
    '{chapter['id']}',
    {section['number']},
    '{section['title']}',
    'lesson',
    '{content_json}'::jsonb,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;
""")
                    elif section['type'] == 'exercises':
                        # Link questions to this section
                        f.write(f"""
-- Link questions to section: {section['title']}
""")
                        for q_id in section.get('question_ids', []):
                            f.write(f"""
INSERT INTO module_questions (module_id, question_id, display_order)
VALUES ('{chapter['id']}', '{q_id}', {section['question_ids'].index(q_id) + 1})
ON CONFLICT DO NOTHING;
""")
        
        print(f"Generated SQL course insert in {filename}")
        return filename
    
    def run(self):
        """Main execution"""
        print("Creating Henle Latin Full Course...")
        print(f"Course ID: {self.course_id}")
        print(f"Language ID: {self.latin_language_id}")
        
        # Create and save course structure
        structure_file = self.save_course_structure()
        
        # Save questions
        csv_file = self.save_questions_csv()
        
        # Generate SQL
        sql_file = self.generate_sql_course_insert()
        
        print("\nCourse creation complete!")
        print(f"Files created:")
        print(f"  - Course structure: {structure_file}")
        print(f"  - Questions CSV: {csv_file}")
        print(f"  - SQL inserts: {sql_file}")
        
        # Summary
        course = self.create_course_structure()
        print(f"\nCourse summary:")
        print(f"  - Chapters: {len(course['chapters'])}")
        print(f"  - Total questions: {len(self.questions)}")
        print(f"  - Categories: {len(self.categories)}")
        
        # Questions per chapter
        chapter_counts = {}
        for q in self.questions:
            ch = q.get('chapter', 'Other')
            chapter_counts[ch] = chapter_counts.get(ch, 0) + 1
        
        print("\nQuestions per chapter:")
        for ch in sorted(chapter_counts.keys()):
            print(f"  - Chapter {ch}: {chapter_counts[ch]} questions")


if __name__ == "__main__":
    course_creator = HenleLatinCourse()
    course_creator.run()