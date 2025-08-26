"""
Create Henle Latin questions using the correct questions table structure
correct_answer is an integer index, not the answer text
"""
import uuid
import json
from datetime import datetime

def generate_uuid():
    return str(uuid.uuid4())

def create_question(text, options, correct_index, explanation, difficulty="easy"):
    """Create a question dictionary using the correct structure"""
    return {
        "id": generate_uuid(),
        "question_text": text,
        "options": options,
        "correct_answer": correct_index,  # Integer index (0-based)
        "explanation": explanation,
        "difficulty": difficulty,
        "image_url": None
    }

# Henle Latin First Year Questions by Module
questions_by_module = {
    "First Declension Nouns": [
        create_question(
            "What is the genitive singular ending for first declension nouns?",
            ["-a", "-ae", "-am", "-ā"],
            1,  # Index 1 = "-ae"
            "First declension nouns have -ae as their genitive singular ending. This is the key identifier of first declension."
        ),
        create_question(
            "Translate 'puella' into English:",
            ["boy", "girl", "woman", "man"],
            1,  # Index 1 = "girl"
            "Puella means 'girl' in Latin. It's a common first declension noun."
        ),
        create_question(
            "Which case is 'puellārum'?",
            ["Nominative singular", "Genitive singular", "Genitive plural", "Accusative plural"],
            2,  # Index 2 = "Genitive plural"
            "The ending -ārum indicates genitive plural in the first declension."
        ),
        create_question(
            "What is the nominative plural of 'porta' (gate)?",
            ["portae", "portās", "portārum", "portīs"],
            0,  # Index 0 = "portae"
            "First declension nominative plural ends in -ae."
        ),
        create_question(
            "In 'Puella rosam habet', what case is 'rosam'?",
            ["Nominative", "Genitive", "Dative", "Accusative"],
            3,  # Index 3 = "Accusative"
            "Rosam ends in -am, which is the accusative singular ending for first declension. It's the direct object."
        ),
        create_question(
            "Which of these is a first declension noun?",
            ["dominus", "bellum", "aqua", "puer"],
            2,  # Index 2 = "aqua"
            "Aqua (water) is a first declension noun, ending in -a in the nominative."
        ),
        create_question(
            "What is the ablative singular ending for first declension?",
            ["-a", "-ae", "-ā", "-īs"],
            2,  # Index 2 = "-ā"
            "First declension ablative singular has a long -ā ending."
        ),
        create_question(
            "Translate 'fēminae' (genitive singular):",
            ["of the woman", "to the woman", "the women", "by the woman"],
            0,  # Index 0 = "of the woman"
            "Genitive case shows possession: 'of the woman'."
        )
    ],
    
    "Second Declension Masculine Nouns": [
        create_question(
            "What is the genitive singular ending for second declension masculine nouns?",
            ["-us", "-ī", "-um", "-ō"],
            1,  # Index 1 = "-ī"
            "Second declension masculine nouns have -ī as their genitive singular ending."
        ),
        create_question(
            "What is the nominative plural of 'servus' (slave)?",
            ["servī", "servōs", "servum", "servōrum"],
            0,  # Index 0 = "servī"
            "Second declension masculine nominative plural ends in -ī."
        ),
        create_question(
            "Translate 'amīcus' into English:",
            ["enemy", "friend", "soldier", "master"],
            1,  # Index 1 = "friend"
            "Amīcus means 'friend' in Latin."
        ),
        create_question(
            "In 'Dominus servum videt', what case is 'servum'?",
            ["Nominative", "Genitive", "Accusative", "Ablative"],
            2,  # Index 2 = "Accusative"
            "Servum ends in -um, which is the accusative singular for second declension masculine."
        ),
        create_question(
            "Which form is the vocative singular of 'fīlius' (son)?",
            ["fīlie", "fīlī", "fīlius", "fīliī"],
            1,  # Index 1 = "fīlī"
            "Second declension nouns ending in -ius have vocative singular in -ī (not -ie)."
        ),
        create_question(
            "What is the dative plural of 'deus' (god)?",
            ["deīs", "deōs", "deōrum", "deī"],
            0,  # Index 0 = "deīs"
            "Second declension dative/ablative plural ends in -īs."
        ),
        create_question(
            "Which ending indicates second declension masculine accusative plural?",
            ["-ōs", "-ās", "-a", "-ēs"],
            0,  # Index 0 = "-ōs"
            "Second declension masculine accusative plural ends in -ōs."
        ),
        create_question(
            "Translate 'equus':",
            ["foot soldier", "horse", "rider", "chariot"],
            1,  # Index 1 = "horse"
            "Equus means 'horse' in Latin."
        )
    ],
    
    "Second Declension Neuter Nouns": [
        create_question(
            "What is the nominative plural ending for second declension neuter nouns?",
            ["-a", "-ī", "-um", "-ōrum"],
            0,  # Index 0 = "-a"
            "Second declension neuter nouns have -a as their nominative AND accusative plural ending."
        ),
        create_question(
            "Translate 'bellum' into English:",
            ["beautiful", "war", "good", "book"],
            1,  # Index 1 = "war"
            "Bellum means 'war' in Latin. It's a common second declension neuter noun."
        ),
        create_question(
            "What cases are always the same in neuter nouns?",
            ["Nominative and Genitive", "Nominative and Accusative", "Genitive and Dative", "Dative and Ablative"],
            1,  # Index 1 = "Nominative and Accusative"
            "In all neuter nouns, the nominative and accusative forms are identical."
        ),
        create_question(
            "What is the genitive plural of 'dōnum' (gift)?",
            ["dōna", "dōnī", "dōnōrum", "dōnīs"],
            2,  # Index 2 = "dōnōrum"
            "Second declension genitive plural is -ōrum for both masculine and neuter."
        ),
        create_question(
            "In 'Templa magna sunt', what case is 'templa'?",
            ["Nominative singular", "Nominative plural", "Accusative singular", "Accusative plural"],
            1,  # Index 1 = "Nominative plural"
            "Templa with -a ending is nominative plural (subject). 'Sunt' (are) confirms plural."
        ),
        create_question(
            "What is the ablative singular of 'verbum' (word)?",
            ["verbō", "verbī", "verbīs", "verba"],
            0,  # Index 0 = "verbō"
            "Second declension neuter ablative singular ends in -ō."
        ),
        create_question(
            "Which is a neuter second declension noun?",
            ["hortus", "oppidum", "servus", "dominus"],
            1,  # Index 1 = "oppidum"
            "Oppidum (town) is neuter, ending in -um."
        ),
        create_question(
            "Translate 'rēgnum':",
            ["king", "queen", "kingdom", "royal"],
            2,  # Index 2 = "kingdom"
            "Rēgnum means 'kingdom' in Latin."
        )
    ],
    
    "Present Tense of Sum": [
        create_question(
            "What is the first person singular present of 'sum' (to be)?",
            ["sum", "es", "est", "sunt"],
            0,  # Index 0 = "sum"
            "Sum means 'I am' - first person singular present."
        ),
        create_question(
            "Translate 'sunt' into English:",
            ["I am", "you are", "he/she/it is", "they are"],
            3,  # Index 3 = "they are"
            "Sunt is third person plural: 'they are'."
        ),
        create_question(
            "What is the second person singular of 'sum'?",
            ["sum", "es", "est", "sumus"],
            1,  # Index 1 = "es"
            "Es means 'you are' (singular)."
        ),
        create_question(
            "Complete: 'Nōs ___ amīcī' (We are friends)",
            ["sum", "es", "sumus", "sunt"],
            2,  # Index 2 = "sumus"
            "Sumus is first person plural: 'we are'."
        ),
        create_question(
            "In 'Puellae in hortō sunt', what does 'sunt' indicate about 'puellae'?",
            ["It's singular", "It's plural", "It's feminine", "It's accusative"],
            1,  # Index 1 = "It's plural"
            "Sunt (they are) confirms that puellae is plural."
        ),
        create_question(
            "What is the second person plural of 'sum'?",
            ["estis", "sunt", "sumus", "es"],
            0,  # Index 0 = "estis"
            "Estis means 'you (all) are' - second person plural."
        ),
        create_question(
            "Translate 'Est bonus':",
            ["I am good", "You are good", "He is good", "They are good"],
            2,  # Index 2 = "He is good"
            "Est (he/she/it is) bonus (good) = 'He is good'."
        ),
        create_question(
            "Which form means 'we are'?",
            ["sum", "sumus", "sunt", "estis"],
            1,  # Index 1 = "sumus"
            "Sumus is first person plural: 'we are'."
        )
    ],
    
    "First Conjugation Verbs Present": [
        create_question(
            "What is the first person singular present of 'amō' (to love)?",
            ["amō", "amās", "amat", "amant"],
            0,  # Index 0 = "amō"
            "Amō means 'I love' - the first person singular keeps the -ō ending."
        ),
        create_question(
            "What is the infinitive ending for first conjugation verbs?",
            ["-ō", "-āre", "-ēre", "-ere"],
            1,  # Index 1 = "-āre"
            "First conjugation infinitives end in -āre (long a)."
        ),
        create_question(
            "Translate 'laborant' into English:",
            ["I work", "you work", "he works", "they work"],
            3,  # Index 3 = "they work"
            "The -ant ending indicates third person plural: 'they work'."
        ),
        create_question(
            "What is the third person singular of 'portō' (to carry)?",
            ["portō", "portās", "portat", "portant"],
            2,  # Index 2 = "portat"
            "Third person singular of first conjugation ends in -at."
        ),
        create_question(
            "In 'Puella cantat', what person and number is 'cantat'?",
            ["1st singular", "2nd singular", "3rd singular", "3rd plural"],
            2,  # Index 2 = "3rd singular"
            "The -at ending shows third person singular: 'she sings'."
        ),
        create_question(
            "What is the second person plural of 'laudō' (to praise)?",
            ["laudās", "laudat", "laudātis", "laudant"],
            2,  # Index 2 = "laudātis"
            "Second person plural of first conjugation ends in -ātis."
        ),
        create_question(
            "Which ending shows first person plural in first conjugation?",
            ["-āmus", "-ātis", "-ant", "-ō"],
            0,  # Index 0 = "-āmus"
            "First person plural ends in -āmus: 'we [verb]'."
        ),
        create_question(
            "Translate 'vocās':",
            ["I call", "you call", "he calls", "they call"],
            1,  # Index 1 = "you call"
            "The -ās ending is second person singular."
        )
    ]
}

def generate_sql():
    """Generate SQL to insert questions into the questions table"""
    
    sql_statements = []
    all_questions = []
    
    # Flatten all questions
    for module_title, module_questions in questions_by_module.items():
        for q in module_questions:
            q["module"] = module_title
            all_questions.append(q)
    
    # Generate INSERT statements
    sql_statements.append("-- Insert Henle Latin First Year Questions")
    sql_statements.append(f"-- Total questions: {len(all_questions)}")
    sql_statements.append("-- Using correct_answer as integer index (0-based)")
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
    {q["correct_answer"]},
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
    
    return "\n".join(sql_statements)

def save_files():
    """Save all generated files"""
    
    # Save SQL
    sql = generate_sql()
    with open('scripts/insert_henle_latin_questions_correct.sql', 'w', encoding='utf-8') as f:
        f.write(sql)
    
    # Save JSON for review
    all_questions = []
    for module_title, questions in questions_by_module.items():
        for q in questions:
            q["module"] = module_title
            all_questions.append(q)
    
    with open('scripts/henle_latin_questions_correct.json', 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, indent=2)
    
    # Save CSV for easy review
    with open('scripts/henle_latin_questions_correct.csv', 'w', encoding='utf-8') as f:
        f.write("Module,Question,Options,CorrectIndex,CorrectAnswer,Explanation,Difficulty\n")
        for q in all_questions:
            options_str = "|".join(q["options"])
            correct_answer_text = q["options"][q["correct_answer"]]
            f.write(f'"{q["module"]}","{q["question_text"]}","{options_str}",{q["correct_answer"]},"{correct_answer_text}","{q["explanation"]}","{q["difficulty"]}"\n')

def main():
    save_files()
    
    # Print summary
    total_questions = sum(len(questions) for questions in questions_by_module.values())
    print(f"Generated {total_questions} questions for {len(questions_by_module)} modules")
    print("\nFiles created:")
    print("  - scripts/insert_henle_latin_questions_correct.sql (Ready to run)")
    print("  - scripts/henle_latin_questions_correct.json (JSON format)")
    print("  - scripts/henle_latin_questions_correct.csv (For review)")
    print("\nModules covered:")
    for module, questions in questions_by_module.items():
        print(f"  - {module}: {len(questions)} questions")
    print("\n✅ SQL is ready to run with correct integer indices for correct_answer")

if __name__ == "__main__":
    main()