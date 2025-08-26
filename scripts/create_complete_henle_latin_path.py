import uuid
import json
from datetime import datetime

# Generate UUIDs for consistency
latin_language_id = '84acf185-0b8c-4c2a-99f3-c5056be86d23'  # Already exists in DB
learning_path_id = str(uuid.uuid4())

# Course IDs for all 5 Henle books
course_ids = {
    'first_year': 'cebb7f42-e51b-4ac4-8464-29fee0894024',  # Already exists
    'second_year': str(uuid.uuid4()),
    'third_year': str(uuid.uuid4()),
    'fourth_year': str(uuid.uuid4()),
    'grammar': str(uuid.uuid4())
}

# Category IDs (reuse existing ones)
category_ids = {
    'vocabulary': '1b922f3b-71da-490a-a6de-2637b2313c95',
    'grammar': 'a60bffbc-ef33-4fbb-835c-ad35985335e5',
    'translation': '0f38bc09-00e2-4f65-b57e-1df712c10c1f',
    'reading_comprehension': '69e5fb77-d3ac-4e91-88f0-0e1a4f732848',
    'declensions': '22660823-a19f-40d7-8c34-adcd0acd7d7d',
    'conjugations': 'fdab6231-4268-4518-be85-a4c746e36b6a'
}

def create_course_structure(course_name, chapters, level, estimated_hours, course_description):
    """Create the structure for a Henle Latin course"""
    return {
        'name': course_name,
        'description': course_description,
        'level': level,
        'estimated_hours': estimated_hours,
        'chapters': chapters
    }

# Define all 5 Henle Latin textbooks
henle_courses = {
    'second_year': create_course_structure(
        'Henle Latin Second Year',
        [
            {
                'number': 1,
                'title': 'Review of First Year Grammar',
                'description': 'Comprehensive review of first year concepts',
                'sections': [
                    {'title': 'Case Review', 'type': 'grammar_rule', 'content': 'Review of all six Latin cases and their uses'},
                    {'title': 'Verb Conjugations Review', 'type': 'grammar_rule', 'content': 'Review of present, imperfect, and future tenses'},
                    {'title': 'Advanced Vocabulary', 'type': 'vocabulary', 'content': 'Extended vocabulary from first year'}
                ]
            },
            {
                'number': 2,
                'title': 'Subjunctive Mood',
                'description': 'Introduction to the subjunctive mood',
                'sections': [
                    {'title': 'Present Subjunctive', 'type': 'grammar_rule', 'content': 'Formation and uses of present subjunctive'},
                    {'title': 'Imperfect Subjunctive', 'type': 'grammar_rule', 'content': 'Formation and uses of imperfect subjunctive'},
                    {'title': 'Purpose Clauses', 'type': 'grammar_rule', 'content': 'Using ut and ne with subjunctive'}
                ]
            },
            {
                'number': 3,
                'title': 'Participles',
                'description': 'Present, perfect, and future participles',
                'sections': [
                    {'title': 'Present Active Participle', 'type': 'grammar_rule', 'content': 'Formation and use of present participles'},
                    {'title': 'Perfect Passive Participle', 'type': 'grammar_rule', 'content': 'Formation and use of perfect participles'},
                    {'title': 'Ablative Absolute', 'type': 'grammar_rule', 'content': 'Construction and translation of ablative absolute'}
                ]
            },
            {
                'number': 4,
                'title': 'Indirect Discourse',
                'description': 'Reporting speech and thoughts in Latin',
                'sections': [
                    {'title': 'Accusative with Infinitive', 'type': 'grammar_rule', 'content': 'Basic indirect statement construction'},
                    {'title': 'Sequence of Tenses', 'type': 'grammar_rule', 'content': 'Time relationships in indirect discourse'},
                    {'title': 'Caesar Readings', 'type': 'reading_comprehension', 'content': 'Selections from De Bello Gallico'}
                ]
            },
            {
                'number': 5,
                'title': 'Advanced Syntax',
                'description': 'Complex grammatical constructions',
                'sections': [
                    {'title': 'Gerunds and Gerundives', 'type': 'grammar_rule', 'content': 'Formation and uses of verbal nouns and adjectives'},
                    {'title': 'Conditional Sentences', 'type': 'grammar_rule', 'content': 'Types of conditional clauses'},
                    {'title': 'Advanced Caesar', 'type': 'reading_comprehension', 'content': 'Extended passages from Caesar'}
                ]
            }
        ],
        'Intermediate',
        80,
        'Second year Latin course focusing on subjunctive mood, participles, and Caesar readings'
    ),
    
    'third_year': create_course_structure(
        'Henle Latin Third Year',
        [
            {
                'number': 1,
                'title': 'Cicero: In Catilinam',
                'description': 'Introduction to Ciceronian prose',
                'sections': [
                    {'title': 'Historical Context', 'type': 'reading_comprehension', 'content': 'The Catiline Conspiracy'},
                    {'title': 'Ciceronian Style', 'type': 'grammar_rule', 'content': 'Periodic sentences and rhetorical devices'},
                    {'title': 'First Catiline Oration', 'type': 'translation', 'content': 'Opening passages of In Catilinam I'}
                ]
            },
            {
                'number': 2,
                'title': 'Advanced Subjunctive Uses',
                'description': 'Complex subjunctive constructions',
                'sections': [
                    {'title': 'Result Clauses', 'type': 'grammar_rule', 'content': 'Ut and ut non with subjunctive'},
                    {'title': 'Cum Clauses', 'type': 'grammar_rule', 'content': 'Temporal, causal, and concessive cum'},
                    {'title': 'Indirect Questions', 'type': 'grammar_rule', 'content': 'Question words with subjunctive'}
                ]
            },
            {
                'number': 3,
                'title': 'Virgil: Aeneid Introduction',
                'description': 'Beginning epic poetry',
                'sections': [
                    {'title': 'Dactylic Hexameter', 'type': 'grammar_rule', 'content': 'Meter and scansion basics'},
                    {'title': 'Epic Conventions', 'type': 'reading_comprehension', 'content': 'Invocation, epithets, and similes'},
                    {'title': 'Aeneid Book I Opening', 'type': 'translation', 'content': 'Arma virumque cano...'}
                ]
            },
            {
                'number': 4,
                'title': 'Advanced Prose Composition',
                'description': 'Writing Latin prose',
                'sections': [
                    {'title': 'Word Order', 'type': 'grammar_rule', 'content': 'Latin word order principles'},
                    {'title': 'Prose Rhythm', 'type': 'grammar_rule', 'content': 'Clausulae and periodic structure'},
                    {'title': 'Translation Exercises', 'type': 'translation', 'content': 'English to Latin prose'}
                ]
            },
            {
                'number': 5,
                'title': 'Livy: Ab Urbe Condita',
                'description': 'Historical narrative',
                'sections': [
                    {'title': 'Livy\'s Style', 'type': 'reading_comprehension', 'content': 'Narrative techniques'},
                    {'title': 'Hannibal Passages', 'type': 'translation', 'content': 'Selections from the Second Punic War'},
                    {'title': 'Historical Present', 'type': 'grammar_rule', 'content': 'Use of present tense in narrative'}
                ]
            }
        ],
        'Advanced',
        100,
        'Third year Latin featuring Cicero, introduction to Virgil, and advanced prose composition'
    ),
    
    'fourth_year': create_course_structure(
        'Henle Latin Fourth Year',
        [
            {
                'number': 1,
                'title': 'Virgil: Aeneid Books I-VI',
                'description': 'Extended reading of the Aeneid',
                'sections': [
                    {'title': 'Book I: Storm and Carthage', 'type': 'translation', 'content': 'Complete Book I selections'},
                    {'title': 'Book II: Fall of Troy', 'type': 'translation', 'content': 'Trojan Horse and destruction'},
                    {'title': 'Book IV: Dido and Aeneas', 'type': 'translation', 'content': 'The tragedy of Dido'}
                ]
            },
            {
                'number': 2,
                'title': 'Horace: Odes',
                'description': 'Lyric poetry',
                'sections': [
                    {'title': 'Lyric Meters', 'type': 'grammar_rule', 'content': 'Sapphic and Alcaic stanzas'},
                    {'title': 'Carpe Diem', 'type': 'translation', 'content': 'Odes I.11 and similar poems'},
                    {'title': 'Roman Values in Horace', 'type': 'reading_comprehension', 'content': 'Themes of moderation and virtue'}
                ]
            },
            {
                'number': 3,
                'title': 'Ovid: Metamorphoses',
                'description': 'Mythological epic',
                'sections': [
                    {'title': 'Creation Story', 'type': 'translation', 'content': 'Book I: Chaos to Cosmos'},
                    {'title': 'Daedalus and Icarus', 'type': 'translation', 'content': 'Book VIII: The flight'},
                    {'title': 'Pyramus and Thisbe', 'type': 'translation', 'content': 'Book IV: Tragic love'}
                ]
            },
            {
                'number': 4,
                'title': 'Tacitus: Annales',
                'description': 'Imperial historiography',
                'sections': [
                    {'title': 'Tacitean Style', 'type': 'grammar_rule', 'content': 'Brevity and variation'},
                    {'title': 'Death of Germanicus', 'type': 'translation', 'content': 'Annales II selections'},
                    {'title': 'Nero and the Fire', 'type': 'translation', 'content': 'Annales XV: Great Fire of Rome'}
                ]
            },
            {
                'number': 5,
                'title': 'Advanced Poetry Analysis',
                'description': 'Literary criticism and analysis',
                'sections': [
                    {'title': 'Figures of Speech', 'type': 'grammar_rule', 'content': 'Metaphor, metonymy, synecdoche'},
                    {'title': 'Allusion and Intertextuality', 'type': 'reading_comprehension', 'content': 'Literary references'},
                    {'title': 'Comparative Analysis', 'type': 'translation', 'content': 'Comparing authors and styles'}
                ]
            }
        ],
        'Advanced',
        120,
        'Fourth year Latin featuring extensive Virgil, Horace, Ovid, and Tacitus'
    ),
    
    'grammar': create_course_structure(
        'Henle Latin Grammar',
        [
            {
                'number': 1,
                'title': 'Complete Declension System',
                'description': 'All noun and adjective forms',
                'sections': [
                    {'title': 'All Five Declensions', 'type': 'grammar_rule', 'content': 'Complete paradigms and exceptions'},
                    {'title': 'Adjective Agreement', 'type': 'grammar_rule', 'content': 'Three-termination and two-termination adjectives'},
                    {'title': 'Comparative and Superlative', 'type': 'grammar_rule', 'content': 'Regular and irregular comparisons'}
                ]
            },
            {
                'number': 2,
                'title': 'Complete Conjugation System',
                'description': 'All verb forms and constructions',
                'sections': [
                    {'title': 'All Tenses Active', 'type': 'grammar_rule', 'content': 'Present, imperfect, future, perfect, pluperfect, future perfect'},
                    {'title': 'All Tenses Passive', 'type': 'grammar_rule', 'content': 'Complete passive system'},
                    {'title': 'Deponent Verbs', 'type': 'grammar_rule', 'content': 'Passive form, active meaning'}
                ]
            },
            {
                'number': 3,
                'title': 'Syntax Reference',
                'description': 'Complete syntax rules',
                'sections': [
                    {'title': 'Case Uses', 'type': 'grammar_rule', 'content': 'All uses of all cases'},
                    {'title': 'Clause Types', 'type': 'grammar_rule', 'content': 'All subordinate clause types'},
                    {'title': 'Sequence of Tenses', 'type': 'grammar_rule', 'content': 'Complete tense relationships'}
                ]
            },
            {
                'number': 4,
                'title': 'Irregular Forms',
                'description': 'Exceptions and irregularities',
                'sections': [
                    {'title': 'Irregular Verbs', 'type': 'grammar_rule', 'content': 'Sum, possum, fero, eo, volo, etc.'},
                    {'title': 'Irregular Nouns', 'type': 'grammar_rule', 'content': 'Vis, domus, and defective nouns'},
                    {'title': 'Greek Forms', 'type': 'grammar_rule', 'content': 'Greek declensions in Latin'}
                ]
            },
            {
                'number': 5,
                'title': 'Advanced Topics',
                'description': 'Specialized grammar topics',
                'sections': [
                    {'title': 'Supines and Gerunds', 'type': 'grammar_rule', 'content': 'Verbal nouns and their uses'},
                    {'title': 'Impersonal Verbs', 'type': 'grammar_rule', 'content': 'Licet, oportet, interest, etc.'},
                    {'title': 'Archaic and Poetic Forms', 'type': 'grammar_rule', 'content': 'Old and poetic variations'}
                ]
            }
        ],
        'Reference',
        40,
        'Complete Latin grammar reference covering all forms and constructions'
    )
}

def generate_sql():
    """Generate SQL to create all courses and the learning path"""
    sql_lines = []
    
    # Add header
    sql_lines.append("-- Create complete Henle Latin learning path with all 5 textbooks")
    sql_lines.append("-- Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sql_lines.append("")
    
    # Create learning paths table first if needed
    sql_lines.append("-- Execute the create_learning_paths_tables.sql first if tables don't exist")
    sql_lines.append("")
    
    # Insert remaining 4 courses (first year already exists)
    for course_key, course_data in henle_courses.items():
        course_id = course_ids[course_key]
        
        sql_lines.append(f"-- Insert {course_data['name']}")
        sql_lines.append(f"INSERT INTO language_courses (")
        sql_lines.append("    id, language_id, name, description, level, estimated_hours, is_active, display_order")
        sql_lines.append(") VALUES (")
        sql_lines.append(f"    '{course_id}',")
        sql_lines.append(f"    '{latin_language_id}',")
        sql_lines.append(f"    '{course_data['name']}',")
        sql_lines.append(f"    '{course_data['description']}',")
        sql_lines.append(f"    '{course_data['level']}',")
        sql_lines.append(f"    {course_data['estimated_hours']},")
        sql_lines.append(f"    true,")
        sql_lines.append(f"    {list(henle_courses.keys()).index(course_key) + 2}")  # +2 because first year is 1
        sql_lines.append(") ON CONFLICT (id) DO UPDATE SET")
        sql_lines.append("    name = EXCLUDED.name,")
        sql_lines.append("    description = EXCLUDED.description;")
        sql_lines.append("")
        
        # Insert chapters as course modules
        for chapter in course_data['chapters']:
            module_id = str(uuid.uuid4())
            
            sql_lines.append(f"-- Chapter {chapter['number']}: {chapter['title']}")
            sql_lines.append(f"INSERT INTO course_modules (")
            sql_lines.append("    id, course_id, chapter_number, title, description, module_type, display_order")
            sql_lines.append(") VALUES (")
            sql_lines.append(f"    '{module_id}',")
            sql_lines.append(f"    '{course_id}',")
            sql_lines.append(f"    {chapter['number']},")
            sql_lines.append(f"    '{chapter['title']}',")
            sql_lines.append(f"    '{chapter['description']}',")
            sql_lines.append(f"    'chapter',")
            sql_lines.append(f"    {chapter['number']}")
            sql_lines.append(");")
            sql_lines.append("")
            
            # Insert module content (simplified for now)
            for idx, section in enumerate(chapter['sections'], 1):
                content_id = str(uuid.uuid4())
                content_json = json.dumps({
                    'text': section['content'],
                    'type': section['type']
                }).replace("'", "''")
                
                sql_lines.append(f"INSERT INTO module_content (")
                sql_lines.append("    id, module_id, section_number, title, content_type, content, display_order")
                sql_lines.append(") VALUES (")
                sql_lines.append(f"    '{content_id}',")
                sql_lines.append(f"    '{module_id}',")
                sql_lines.append(f"    {idx},")
                sql_lines.append(f"    '{section['title']}',")
                sql_lines.append(f"    'lesson',")
                sql_lines.append(f"    '{content_json}'::jsonb,")
                sql_lines.append(f"    {idx}")
                sql_lines.append(");")
                sql_lines.append("")
    
    # Create the learning path
    sql_lines.append("-- Create the Learn Latin learning path")
    sql_lines.append(f"INSERT INTO learning_paths (")
    sql_lines.append("    id, name, description, category, difficulty, estimated_hours,")
    sql_lines.append("    icon_name, color, language_id, is_active, display_order")
    sql_lines.append(") VALUES (")
    sql_lines.append(f"    '{learning_path_id}',")
    sql_lines.append(f"    'Complete Henle Latin Program',")
    sql_lines.append(f"    'Master Latin through the complete Henle Latin series, from basic grammar to advanced literature including Caesar, Cicero, Virgil, Horace, Ovid, and Tacitus',")
    sql_lines.append(f"    'language',")
    sql_lines.append(f"    'comprehensive',")
    sql_lines.append(f"    420,")  # Total of all courses
    sql_lines.append(f"    'AcademicCapIcon',")
    sql_lines.append(f"    'purple',")
    sql_lines.append(f"    '{latin_language_id}',")
    sql_lines.append(f"    true,")
    sql_lines.append(f"    1")
    sql_lines.append(");")
    sql_lines.append("")
    
    # Link all courses to the learning path
    course_order = ['first_year', 'second_year', 'third_year', 'fourth_year', 'grammar']
    for idx, course_key in enumerate(course_order, 1):
        course_id = course_ids[course_key]
        prev_course = course_ids[course_order[idx-2]] if idx > 1 else None
        
        sql_lines.append(f"-- Link course {idx}: {course_key}")
        sql_lines.append(f"INSERT INTO learning_path_courses (")
        sql_lines.append("    learning_path_id, course_id, sequence_number, is_required, unlock_after_course_id")
        sql_lines.append(") VALUES (")
        sql_lines.append(f"    '{learning_path_id}',")
        sql_lines.append(f"    '{course_id}',")
        sql_lines.append(f"    {idx},")
        sql_lines.append(f"    {str(course_key != 'grammar').lower()},")  # Grammar is optional/reference
        if prev_course and course_key != 'grammar':
            sql_lines.append(f"    '{prev_course}'")
        else:
            sql_lines.append(f"    NULL")
        sql_lines.append(");")
        sql_lines.append("")
    
    return '\n'.join(sql_lines)

if __name__ == "__main__":
    sql = generate_sql()
    
    # Save to file
    with open('create_complete_henle_latin_path.sql', 'w', encoding='utf-8') as f:
        f.write(sql)
    
    print("Generated SQL for complete Henle Latin learning path")
    print(f"Learning path ID: {learning_path_id}")
    print("Course IDs:")
    for name, id in course_ids.items():
        print(f"  {name}: {id}")