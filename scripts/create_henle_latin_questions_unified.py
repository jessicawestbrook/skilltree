"""
Create Henle Latin questions using the unified questions table
This uses the same structure as assessment questions
"""
import uuid
import json
from datetime import datetime

def generate_uuid():
    return str(uuid.uuid4())

def create_question(text, options, correct_answer, explanation, difficulty="beginner"):
    """Create a question dictionary using the unified questions table structure"""
    return {
        "id": generate_uuid(),
        "question_text": text,
        "options": options,
        "correct_answer": correct_answer,  # This is the actual answer text, not index
        "explanation": explanation,
        "difficulty": difficulty,
        "image_url": None  # Latin questions typically don't need images
    }

# Henle Latin First Year Questions by Module
questions_by_module = {
    "First Declension Nouns": [
        create_question(
            "What is the genitive singular ending for first declension nouns?",
            ["-a", "-ae", "-am", "-ā"],
            "-ae",
            "First declension nouns have -ae as their genitive singular ending. This is the key identifier of first declension."
        ),
        create_question(
            "Translate 'puella' into English:",
            ["boy", "girl", "woman", "man"],
            "girl",
            "Puella means 'girl' in Latin. It's a common first declension noun."
        ),
        create_question(
            "Which case is 'puellārum'?",
            ["Nominative singular", "Genitive singular", "Genitive plural", "Accusative plural"],
            "Genitive plural",
            "The ending -ārum indicates genitive plural in the first declension."
        ),
        create_question(
            "What is the nominative plural of 'porta' (gate)?",
            ["portae", "portās", "portārum", "portīs"],
            "portae",
            "First declension nominative plural ends in -ae."
        ),
        create_question(
            "In 'Puella rosam habet', what case is 'rosam'?",
            ["Nominative", "Genitive", "Dative", "Accusative"],
            "Accusative",
            "Rosam ends in -am, which is the accusative singular ending for first declension. It's the direct object."
        ),
        create_question(
            "Which of these is a first declension noun?",
            ["dominus", "bellum", "aqua", "puer"],
            "aqua",
            "Aqua (water) is a first declension noun, ending in -a in the nominative."
        ),
        create_question(
            "What is the ablative singular ending for first declension?",
            ["-a", "-ae", "-ā", "-īs"],
            "-ā",
            "First declension ablative singular has a long -ā ending."
        ),
        create_question(
            "Translate 'fēminae' (genitive singular):",
            ["of the woman", "to the woman", "the women", "by the woman"],
            "of the woman",
            "Genitive case shows possession: 'of the woman'."
        )
    ],
    
    "Second Declension Masculine Nouns": [
        create_question(
            "What is the genitive singular ending for second declension masculine nouns?",
            ["-us", "-ī", "-um", "-ō"],
            "-ī",
            "Second declension masculine nouns have -ī as their genitive singular ending."
        ),
        create_question(
            "What is the nominative plural of 'servus' (slave)?",
            ["servī", "servōs", "servum", "servōrum"],
            "servī",
            "Second declension masculine nominative plural ends in -ī."
        ),
        create_question(
            "Translate 'amīcus' into English:",
            ["enemy", "friend", "soldier", "master"],
            "friend",
            "Amīcus means 'friend' in Latin."
        ),
        create_question(
            "In 'Dominus servum videt', what case is 'servum'?",
            ["Nominative", "Genitive", "Accusative", "Ablative"],
            "Accusative",
            "Servum ends in -um, which is the accusative singular for second declension masculine."
        ),
        create_question(
            "Which form is the vocative singular of 'fīlius' (son)?",
            ["fīlie", "fīlī", "fīlius", "fīliī"],
            "fīlī",
            "Second declension nouns ending in -ius have vocative singular in -ī (not -ie)."
        ),
        create_question(
            "What is the dative plural of 'deus' (god)?",
            ["deīs", "deōs", "deōrum", "deī"],
            "deīs",
            "Second declension dative/ablative plural ends in -īs."
        ),
        create_question(
            "Which ending indicates second declension masculine accusative plural?",
            ["-ōs", "-ās", "-a", "-ēs"],
            "-ōs",
            "Second declension masculine accusative plural ends in -ōs."
        ),
        create_question(
            "Translate 'equus':",
            ["foot soldier", "horse", "rider", "chariot"],
            "horse",
            "Equus means 'horse' in Latin."
        )
    ],
    
    "Second Declension Neuter Nouns": [
        create_question(
            "What is the nominative plural ending for second declension neuter nouns?",
            ["-a", "-ī", "-um", "-ōrum"],
            "-a",
            "Second declension neuter nouns have -a as their nominative AND accusative plural ending."
        ),
        create_question(
            "Translate 'bellum' into English:",
            ["beautiful", "war", "good", "book"],
            "war",
            "Bellum means 'war' in Latin. It's a common second declension neuter noun."
        ),
        create_question(
            "What cases are always the same in neuter nouns?",
            ["Nominative and Genitive", "Nominative and Accusative", "Genitive and Dative", "Dative and Ablative"],
            "Nominative and Accusative",
            "In all neuter nouns, the nominative and accusative forms are identical."
        ),
        create_question(
            "What is the genitive plural of 'dōnum' (gift)?",
            ["dōna", "dōnī", "dōnōrum", "dōnīs"],
            "dōnōrum",
            "Second declension genitive plural is -ōrum for both masculine and neuter."
        ),
        create_question(
            "In 'Templa magna sunt', what case is 'templa'?",
            ["Nominative singular", "Nominative plural", "Accusative singular", "Accusative plural"],
            "Nominative plural",
            "Templa with -a ending is nominative plural (subject). 'Sunt' (are) confirms plural."
        ),
        create_question(
            "What is the ablative singular of 'verbum' (word)?",
            ["verbō", "verbī", "verbīs", "verba"],
            "verbō",
            "Second declension neuter ablative singular ends in -ō."
        ),
        create_question(
            "Which is a neuter second declension noun?",
            ["hortus", "oppidum", "servus", "dominus"],
            "oppidum",
            "Oppidum (town) is neuter, ending in -um."
        ),
        create_question(
            "Translate 'rēgnum':",
            ["king", "queen", "kingdom", "royal"],
            "kingdom",
            "Rēgnum means 'kingdom' in Latin."
        )
    ],
    
    "Present Tense of Sum": [
        create_question(
            "What is the first person singular present of 'sum' (to be)?",
            ["sum", "es", "est", "sunt"],
            "sum",
            "Sum means 'I am' - first person singular present."
        ),
        create_question(
            "Translate 'sunt' into English:",
            ["I am", "you are", "he/she/it is", "they are"],
            "they are",
            "Sunt is third person plural: 'they are'."
        ),
        create_question(
            "What is the second person singular of 'sum'?",
            ["sum", "es", "est", "sumus"],
            "es",
            "Es means 'you are' (singular)."
        ),
        create_question(
            "Complete: 'Nōs ___ amīcī' (We are friends)",
            ["sum", "es", "sumus", "sunt"],
            "sumus",
            "Sumus is first person plural: 'we are'."
        ),
        create_question(
            "In 'Puellae in hortō sunt', what does 'sunt' indicate about 'puellae'?",
            ["It's singular", "It's plural", "It's feminine", "It's accusative"],
            "It's plural",
            "Sunt (they are) confirms that puellae is plural."
        ),
        create_question(
            "What is the second person plural of 'sum'?",
            ["estis", "sunt", "sumus", "es"],
            "estis",
            "Estis means 'you (all) are' - second person plural."
        ),
        create_question(
            "Translate 'Est bonus':",
            ["I am good", "You are good", "He is good", "They are good"],
            "He is good",
            "Est (he/she/it is) bonus (good) = 'He is good'."
        ),
        create_question(
            "Which form means 'we are'?",
            ["sum", "sumus", "sunt", "estis"],
            "sumus",
            "Sumus is first person plural: 'we are'."
        )
    ],
    
    "First Conjugation Verbs Present": [
        create_question(
            "What is the first person singular present of 'amō' (to love)?",
            ["amō", "amās", "amat", "amant"],
            "amō",
            "Amō means 'I love' - the first person singular keeps the -ō ending."
        ),
        create_question(
            "What is the infinitive ending for first conjugation verbs?",
            ["-ō", "-āre", "-ēre", "-ere"],
            "-āre",
            "First conjugation infinitives end in -āre (long a)."
        ),
        create_question(
            "Translate 'laborant' into English:",
            ["I work", "you work", "he works", "they work"],
            "they work",
            "The -ant ending indicates third person plural: 'they work'."
        ),
        create_question(
            "What is the third person singular of 'portō' (to carry)?",
            ["portō", "portās", "portat", "portant"],
            "portat",
            "Third person singular of first conjugation ends in -at."
        ),
        create_question(
            "In 'Puella cantat', what person and number is 'cantat'?",
            ["1st singular", "2nd singular", "3rd singular", "3rd plural"],
            "3rd singular",
            "The -at ending shows third person singular: 'she sings'."
        ),
        create_question(
            "What is the second person plural of 'laudō' (to praise)?",
            ["laudās", "laudat", "laudātis", "laudant"],
            "laudātis",
            "Second person plural of first conjugation ends in -ātis."
        ),
        create_question(
            "Which ending shows first person plural in first conjugation?",
            ["-āmus", "-ātis", "-ant", "-ō"],
            "-āmus",
            "First person plural ends in -āmus: 'we [verb]'."
        ),
        create_question(
            "Translate 'vocās':",
            ["I call", "you call", "he calls", "they call"],
            "you call",
            "The -ās ending is second person singular."
        )
    ]
}

def generate_sql():
    """Generate SQL to insert questions into the unified questions table"""
    
    sql_statements = []
    all_questions = []
    
    # Flatten all questions
    for module_title, module_questions in questions_by_module.items():
        for q in module_questions:
            q["module"] = module_title
            all_questions.append(q)
    
    # Generate INSERT statements
    sql_statements.append("-- Insert Henle Latin First Year Questions into unified questions table")
    sql_statements.append(f"-- Total questions: {len(all_questions)}")
    sql_statements.append("-- These use the same table as assessment questions")
    sql_statements.append("")
    
    for q in all_questions:
        # Format options as PostgreSQL array
        escaped_options = []
        for opt in q["options"]:
            escaped_opt = opt.replace("'", "''")
            escaped_options.append(f"'{escaped_opt}'")
        options_array = 'ARRAY[' + ', '.join(escaped_options) + ']::text[]'
        
        # Escape text fields
        question_text = q["question_text"].replace("'", "''")
        correct_answer = q["correct_answer"].replace("'", "''")
        explanation = q["explanation"].replace("'", "''") if q["explanation"] else ""
        
        sql = f"""INSERT INTO questions (
    id, 
    question_text, 
    options, 
    correct_answer, 
    explanation, 
    difficulty,
    image_url
) VALUES (
    '{q["id"]}',
    '{question_text}',
    {options_array},
    '{correct_answer}',
    '{explanation}',
    '{q["difficulty"]}',
    NULL
) ON CONFLICT (id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    correct_answer = EXCLUDED.correct_answer,
    explanation = EXCLUDED.explanation,
    difficulty = EXCLUDED.difficulty;"""
        
        sql_statements.append(sql)
        sql_statements.append("")
    
    # Add module linking instructions
    sql_statements.append("-- Link questions to course modules")
    sql_statements.append("-- This creates the module_questions relationships")
    sql_statements.append("")
    
    for module_title in questions_by_module.keys():
        sql_statements.append(f"-- For module: {module_title}")
        sql_statements.append(f"""
-- INSERT INTO module_questions (module_id, question_id, display_order)
-- SELECT 
--     m.id as module_id,
--     q.id as question_id,
--     ROW_NUMBER() OVER (ORDER BY q.created_at) as display_order
-- FROM course_modules m
-- CROSS JOIN questions q
-- WHERE m.title = '{module_title}'
-- AND q.question_text IN (
--     /* List specific question texts for this module */
-- )
-- ON CONFLICT DO NOTHING;
""")
    
    return "\n".join(sql_statements)

def generate_linking_script():
    """Generate a Python script to link questions to modules"""
    
    script = '''"""
Link Henle Latin questions to their course modules
Run this after inserting the questions
"""
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv('.env.local')

url = os.environ.get("REACT_APP_SUPABASE_URL")
key = os.environ.get("REACT_APP_SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(url, key)

# Question text to module mapping
question_module_map = {
'''
    
    # Add the mapping
    for module_title, questions in questions_by_module.items():
        for q in questions:
            script += f'    "{q["question_text"][:50]}...": "{module_title}",\n'
    
    script += '''
}

# Get all course modules for Henle Latin First Year
course_id = "cebb7f42-e51b-4ac4-8464-29fee0894024"  # Henle Latin First Year
modules_result = supabase.table('course_modules').select('id, title').eq('course_id', course_id).execute()

module_map = {m['title']: m['id'] for m in modules_result.data}

# Get all questions we just inserted
questions_result = supabase.table('questions').select('id, question_text').execute()

# Link questions to modules
links_created = 0
for question in questions_result.data:
    # Find which module this question belongs to
    for q_text_start, module_title in question_module_map.items():
        if question['question_text'].startswith(q_text_start.replace("...", "")):
            if module_title in module_map:
                # Create the link
                link_data = {
                    'module_id': module_map[module_title],
                    'question_id': question['id'],
                    'display_order': links_created + 1
                }
                try:
                    supabase.table('module_questions').insert(link_data).execute()
                    links_created += 1
                    print(f"Linked question to {module_title}")
                except Exception as e:
                    print(f"Error linking: {e}")
                break

print(f"\\nCreated {links_created} question-module links")
'''
    
    return script

def save_files():
    """Save all generated files"""
    
    # Save SQL
    sql = generate_sql()
    with open('scripts/insert_henle_latin_questions_unified.sql', 'w', encoding='utf-8') as f:
        f.write(sql)
    
    # Save linking script
    link_script = generate_linking_script()
    with open('scripts/link_henle_questions_to_modules.py', 'w', encoding='utf-8') as f:
        f.write(link_script)
    
    # Save JSON for review
    all_questions = []
    for module_title, questions in questions_by_module.items():
        for q in questions:
            q["module"] = module_title
            all_questions.append(q)
    
    with open('scripts/henle_latin_questions.json', 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, indent=2)
    
    # Save CSV for easy review
    with open('scripts/henle_latin_questions.csv', 'w', encoding='utf-8') as f:
        f.write("Module,Question,Options,Answer,Explanation,Difficulty\n")
        for q in all_questions:
            options_str = "|".join(q["options"])
            f.write(f'"{q["module"]}","{q["question_text"]}","{options_str}","{q["correct_answer"]}","{q["explanation"]}","{q["difficulty"]}"\n')

def main():
    save_files()
    
    # Print summary
    total_questions = sum(len(questions) for questions in questions_by_module.values())
    print(f"Generated {total_questions} questions for {len(questions_by_module)} modules")
    print("\nFiles created:")
    print("  - scripts/insert_henle_latin_questions_unified.sql (SQL for questions table)")
    print("  - scripts/link_henle_questions_to_modules.py (Python script to link questions)")
    print("  - scripts/henle_latin_questions.json (JSON for review)")
    print("  - scripts/henle_latin_questions.csv (CSV for easy review)")
    print("\nModules covered:")
    for module, questions in questions_by_module.items():
        print(f"  - {module}: {len(questions)} questions")
    print("\nNext steps:")
    print("1. Review the questions in henle_latin_questions.csv")
    print("2. Run the SQL: scripts/insert_henle_latin_questions_unified.sql")
    print("3. Run the linking script: python scripts/link_henle_questions_to_modules.py")

if __name__ == "__main__":
    main()