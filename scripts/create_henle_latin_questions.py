"""
Create comprehensive questions for Henle Latin First Year course
Based on the actual Henle Latin textbook content
"""
import uuid
import json
from datetime import datetime

def generate_uuid():
    return str(uuid.uuid4())

def create_question(text, options, correct_index, explanation, difficulty="beginner", category="grammar"):
    """Create a question dictionary"""
    return {
        "id": generate_uuid(),
        "question_text": text,
        "question_type": "multiple_choice",
        "options": options,
        "correct_answer_index": correct_index,
        "explanation": explanation,
        "difficulty_level": difficulty,
        "category": category
    }

# Henle Latin First Year Questions by Module
questions_by_module = {
    "First Declension Nouns": [
        create_question(
            "What is the genitive singular ending for first declension nouns?",
            ["-a", "-ae", "-am", "-ā"],
            1,
            "First declension nouns have -ae as their genitive singular ending. This is the key identifier of first declension."
        ),
        create_question(
            "Translate 'puella' into English:",
            ["boy", "girl", "woman", "man"],
            1,
            "Puella means 'girl' in Latin. It's a common first declension noun."
        ),
        create_question(
            "Which case is 'puellārum'?",
            ["Nominative singular", "Genitive singular", "Genitive plural", "Accusative plural"],
            2,
            "The ending -ārum indicates genitive plural in the first declension."
        ),
        create_question(
            "What is the nominative plural of 'porta' (gate)?",
            ["portae", "portās", "portārum", "portīs"],
            0,
            "First declension nominative plural ends in -ae."
        ),
        create_question(
            "In 'Puella rosam habet', what case is 'rosam'?",
            ["Nominative", "Genitive", "Dative", "Accusative"],
            3,
            "Rosam ends in -am, which is the accusative singular ending for first declension. It's the direct object."
        )
    ],
    
    "Second Declension Masculine Nouns": [
        create_question(
            "What is the genitive singular ending for second declension masculine nouns?",
            ["-us", "-ī", "-um", "-ō"],
            1,
            "Second declension masculine nouns have -ī as their genitive singular ending."
        ),
        create_question(
            "What is the nominative plural of 'servus' (slave)?",
            ["servī", "servōs", "servum", "servōrum"],
            0,
            "Second declension masculine nominative plural ends in -ī."
        ),
        create_question(
            "Translate 'amīcus' into English:",
            ["enemy", "friend", "soldier", "master"],
            1,
            "Amīcus means 'friend' in Latin."
        ),
        create_question(
            "In 'Dominus servum videt', what case is 'servum'?",
            ["Nominative", "Genitive", "Accusative", "Ablative"],
            2,
            "Servum ends in -um, which is the accusative singular for second declension masculine."
        ),
        create_question(
            "Which form is the vocative singular of 'fīlius' (son)?",
            ["fīlie", "fīlī", "fīlius", "fīliī"],
            1,
            "Second declension nouns ending in -ius have vocative singular in -ī (not -ie)."
        )
    ],
    
    "Second Declension Neuter Nouns": [
        create_question(
            "What is the nominative plural ending for second declension neuter nouns?",
            ["-a", "-ī", "-um", "-ōrum"],
            0,
            "Second declension neuter nouns have -a as their nominative AND accusative plural ending."
        ),
        create_question(
            "Translate 'bellum' into English:",
            ["beautiful", "war", "good", "book"],
            1,
            "Bellum means 'war' in Latin. It's a common second declension neuter noun."
        ),
        create_question(
            "What cases are always the same in neuter nouns?",
            ["Nominative and Genitive", "Nominative and Accusative", "Genitive and Dative", "Dative and Ablative"],
            1,
            "In all neuter nouns, the nominative and accusative forms are identical."
        ),
        create_question(
            "What is the genitive plural of 'dōnum' (gift)?",
            ["dōna", "dōnī", "dōnōrum", "dōnīs"],
            2,
            "Second declension genitive plural is -ōrum for both masculine and neuter."
        ),
        create_question(
            "In 'Templa magna sunt', what case is 'templa'?",
            ["Nominative singular", "Nominative plural", "Accusative singular", "Accusative plural"],
            1,
            "Templa with -a ending is nominative plural (subject). 'Sunt' (are) confirms plural."
        )
    ],
    
    "Adjectives of First and Second Declension": [
        create_question(
            "What ending does a first/second declension adjective have in the feminine nominative singular?",
            ["-us", "-a", "-um", "-ae"],
            1,
            "Feminine forms of first/second declension adjectives follow first declension: -a in nominative singular."
        ),
        create_question(
            "How would 'bonus' (good) appear when modifying a neuter plural noun in the nominative?",
            ["bonī", "bonae", "bona", "bonōs"],
            2,
            "Neuter nominative plural of first/second declension adjectives ends in -a."
        ),
        create_question(
            "In 'puella pulchra', what must agree between noun and adjective?",
            ["Only case", "Only number", "Only gender", "Case, number, and gender"],
            3,
            "Adjectives must agree with their nouns in case, number, and gender."
        ),
        create_question(
            "What is the masculine accusative plural of 'magnus' (great)?",
            ["magnōs", "magna", "magnī", "magnārum"],
            0,
            "Masculine accusative plural of second declension adjectives ends in -ōs."
        ),
        create_question(
            "Translate 'Vir bonus est':",
            ["The good man is", "The man is good", "Good men are", "The men are good"],
            1,
            "Vir (man) bonus (good) est (is) = 'The man is good'. Predicate adjective."
        )
    ],
    
    "Present Tense of Sum": [
        create_question(
            "What is the first person singular present of 'sum' (to be)?",
            ["sum", "es", "est", "sunt"],
            0,
            "Sum means 'I am' - first person singular present."
        ),
        create_question(
            "Translate 'sunt' into English:",
            ["I am", "you are", "he/she/it is", "they are"],
            3,
            "Sunt is third person plural: 'they are'."
        ),
        create_question(
            "What is the second person singular of 'sum'?",
            ["sum", "es", "est", "sumus"],
            1,
            "Es means 'you are' (singular)."
        ),
        create_question(
            "Complete: 'Nōs ___ amīcī' (We are friends)",
            ["sum", "es", "sumus", "sunt"],
            2,
            "Sumus is first person plural: 'we are'."
        ),
        create_question(
            "In 'Puellae in hortō sunt', what does 'sunt' indicate about 'puellae'?",
            ["It's singular", "It's plural", "It's feminine", "It's accusative"],
            1,
            "Sunt (they are) confirms that puellae is plural."
        )
    ],
    
    "First Conjugation Verbs Present": [
        create_question(
            "What is the first person singular present of 'amō' (to love)?",
            ["amō", "amās", "amat", "amant"],
            0,
            "Amō means 'I love' - the first person singular keeps the -ō ending."
        ),
        create_question(
            "What is the infinitive ending for first conjugation verbs?",
            ["-ō", "-āre", "-ēre", "-ere"],
            1,
            "First conjugation infinitives end in -āre (long a)."
        ),
        create_question(
            "Translate 'laborant' into English:",
            ["I work", "you work", "he works", "they work"],
            3,
            "The -ant ending indicates third person plural: 'they work'."
        ),
        create_question(
            "What is the third person singular of 'portō' (to carry)?",
            ["portō", "portās", "portat", "portant"],
            2,
            "Third person singular of first conjugation ends in -at."
        ),
        create_question(
            "In 'Puella cantat', what person and number is 'cantat'?",
            ["1st singular", "2nd singular", "3rd singular", "3rd plural"],
            2,
            "The -at ending shows third person singular: 'she sings'."
        )
    ],
    
    "Second Conjugation Verbs Present": [
        create_question(
            "What is the infinitive ending for second conjugation verbs?",
            ["-āre", "-ēre", "-ere", "-īre"],
            1,
            "Second conjugation infinitives end in -ēre (long e)."
        ),
        create_question(
            "What is the first person singular of 'videō' (to see)?",
            ["videō", "vidēs", "videt", "vident"],
            0,
            "First person singular: videō 'I see'."
        ),
        create_question(
            "Translate 'habent' into English:",
            ["I have", "you have", "he has", "they have"],
            3,
            "The -ent ending in second conjugation indicates third person plural."
        ),
        create_question(
            "What distinguishes second conjugation from first in the present tense?",
            ["The infinitive ending", "The stem vowel", "Both A and B", "The personal endings"],
            2,
            "Second conjugation has -ēre infinitive and maintains e in the stem."
        ),
        create_question(
            "Complete: 'Ego librum ___' (I have a book) using habeō:",
            ["habeō", "habēs", "habet", "habēmus"],
            0,
            "Ego (I) requires first person singular: habeō."
        )
    ],
    
    "Questions and Interrogatives": [
        create_question(
            "What does the enclitic '-ne' indicate in Latin?",
            ["Negation", "A yes/no question", "Emphasis", "Past tense"],
            1,
            "The enclitic -ne attached to the first word creates a yes/no question."
        ),
        create_question(
            "Translate 'Quis est?':",
            ["What is it?", "Who is it?", "Where is it?", "When is it?"],
            1,
            "Quis means 'who' - asking about a person."
        ),
        create_question(
            "What is the neuter form of 'quis'?",
            ["quis", "quae", "quid", "quod"],
            2,
            "Quid is the neuter form, meaning 'what'."
        ),
        create_question(
            "How do you form 'Does the girl sing?' in Latin?",
            ["Puella cantat?", "Cantatne puella?", "Num puella cantat?", "Puella cantat"],
            1,
            "Add -ne to the first word (usually the verb) for a neutral yes/no question."
        ),
        create_question(
            "What does 'Cūr' mean?",
            ["Who", "What", "Where", "Why"],
            3,
            "Cūr means 'why' - asking for a reason."
        )
    ],
    
    "Prepositions with Ablative": [
        create_question(
            "Which case does 'in' take when it means 'in/on' (location)?",
            ["Nominative", "Accusative", "Ablative", "Genitive"],
            2,
            "In + ablative indicates location (where something is)."
        ),
        create_question(
            "Translate 'cum amīcō':",
            ["to the friend", "of the friend", "with the friend", "from the friend"],
            2,
            "Cum + ablative means 'with'."
        ),
        create_question(
            "Which preposition means 'from' or 'about'?",
            ["ad", "dē", "in", "per"],
            1,
            "Dē + ablative means 'from, about, concerning'."
        ),
        create_question(
            "In 'sine pecūniā', what case is 'pecūniā'?",
            ["Nominative", "Accusative", "Ablative", "Dative"],
            2,
            "Sine (without) always takes the ablative case."
        ),
        create_question(
            "Complete: 'in __' (in the garden) using hortus, -ī:",
            ["hortus", "hortum", "hortō", "hortī"],
            2,
            "In + ablative for location: hortō (ablative singular)."
        )
    ],
    
    "Prepositions with Accusative": [
        create_question(
            "Which case does 'in' take when it means 'into' (motion)?",
            ["Nominative", "Accusative", "Ablative", "Genitive"],
            1,
            "In + accusative indicates motion into something."
        ),
        create_question(
            "Translate 'ad urbem':",
            ["in the city", "from the city", "to the city", "with the city"],
            2,
            "Ad + accusative means 'to, toward'."
        ),
        create_question(
            "Which preposition means 'through'?",
            ["per", "post", "propter", "prō"],
            0,
            "Per + accusative means 'through'."
        ),
        create_question(
            "In 'post bellum', what does 'post' mean?",
            ["before", "after", "during", "because of"],
            1,
            "Post + accusative means 'after'."
        ),
        create_question(
            "Complete: 'trans __' (across the river) using fluvius, -ī:",
            ["fluvius", "fluviō", "fluvium", "fluviī"],
            2,
            "Trans (across) takes accusative: fluvium."
        )
    ]
}

def generate_sql():
    """Generate SQL to insert questions into the database"""
    
    # Get Latin language ID (from our previous setup)
    latin_id = "84acf185-0b8c-4c2a-99f3-c5056be86d23"
    
    # Grammar category ID (you may need to adjust this based on your categories)
    grammar_category_id = "b5f91234-8abc-4def-9012-345678901234"
    
    sql_statements = []
    
    # First, create all questions
    all_questions = []
    question_to_module = {}  # Map question IDs to module titles
    
    for module_title, module_questions in questions_by_module.items():
        for q in module_questions:
            q["language_id"] = latin_id
            q["category_id"] = grammar_category_id
            all_questions.append(q)
            question_to_module[q["id"]] = module_title
    
    # Generate INSERT statements for questions
    sql_statements.append("-- Insert Henle Latin First Year Questions")
    sql_statements.append("-- Total questions: {}".format(len(all_questions)))
    sql_statements.append("")
    
    for q in all_questions:
        # Format options as PostgreSQL array
        escaped_options = []
        for opt in q["options"]:
            escaped_opt = opt.replace("'", "''")
            escaped_options.append(f"'{escaped_opt}'")
        options_array = 'ARRAY[' + ', '.join(escaped_options) + ']'
        
        # Escape text fields
        question_text = q["question_text"].replace("'", "''")
        explanation = q["explanation"].replace("'", "''")
        
        sql = f"""INSERT INTO language_questions (
    id, language_id, category_id, question_text, question_type,
    options, correct_answer_index, explanation, difficulty_level
) VALUES (
    '{q["id"]}',
    '{q["language_id"]}',
    '{q["category_id"]}',
    '{question_text}',
    '{q["question_type"]}',
    {options_array},
    {q["correct_answer_index"]},
    '{explanation}',
    '{q["difficulty_level"]}'
) ON CONFLICT (id) DO NOTHING;"""
        
        sql_statements.append(sql)
        sql_statements.append("")
    
    return "\n".join(sql_statements)

def generate_module_links_sql():
    """Generate SQL to link questions to modules"""
    
    # This would need the actual module IDs from the database
    # For now, we'll create a template
    
    sql = """
-- After inserting questions, link them to modules
-- You'll need to run this after getting the actual module IDs

-- Example for linking questions to modules:
-- INSERT INTO module_questions (module_id, question_id, display_order)
-- SELECT 
--     m.id as module_id,
--     q.id as question_id,
--     ROW_NUMBER() OVER (PARTITION BY m.id ORDER BY q.created_at) as display_order
-- FROM course_modules m
-- CROSS JOIN language_questions q
-- WHERE m.title = 'First Declension Nouns'
-- AND q.question_text LIKE '%first declension%'
-- ON CONFLICT DO NOTHING;
"""
    return sql

def save_questions_json():
    """Save questions as JSON for review"""
    with open('scripts/henle_latin_questions.json', 'w') as f:
        json.dump(questions_by_module, f, indent=2)
    print("Questions saved to scripts/henle_latin_questions.json")

def main():
    # Generate SQL
    sql = generate_sql()
    
    # Save to file
    with open('scripts/insert_henle_latin_questions.sql', 'w') as f:
        f.write(sql)
        f.write("\n\n")
        f.write(generate_module_links_sql())
    
    # Save JSON for review
    save_questions_json()
    
    # Print summary
    total_questions = sum(len(questions) for questions in questions_by_module.values())
    print(f"Generated {total_questions} questions for {len(questions_by_module)} modules")
    print("SQL saved to: scripts/insert_henle_latin_questions.sql")
    print("JSON saved to: scripts/henle_latin_questions.json")
    print("\nModules covered:")
    for module in questions_by_module.keys():
        print(f"  - {module}: {len(questions_by_module[module])} questions")

if __name__ == "__main__":
    main()