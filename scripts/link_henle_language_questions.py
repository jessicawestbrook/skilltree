"""
Link Henle Latin questions from language_questions table to course modules
"""
import os
from supabase import create_client
from dotenv import load_dotenv
import uuid

load_dotenv('.env.local')

url = os.environ.get("REACT_APP_SUPABASE_URL")
key = os.environ.get("REACT_APP_SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(url, key)

# Mapping of question text patterns to module titles
question_module_mapping = {
    "First Declension Nouns": [
        "genitive singular ending for first declension",
        "Translate 'puella'",
        "case is 'puellārum'",
        "nominative plural of 'porta'",
        "Puella rosam habet",
        "first declension noun",
        "ablative singular ending for first declension",
        "Translate 'fēminae'"
    ],
    "Second Declension Masculine Nouns": [
        "genitive singular ending for second declension masculine",
        "nominative plural of 'servus'",
        "Translate 'amīcus'",
        "Dominus servum videt",
        "vocative singular of 'fīlius'",
        "dative plural of 'deus'",
        "second declension masculine accusative plural",
        "Translate 'equus'"
    ],
    "Second Declension Neuter Nouns": [
        "nominative plural ending for second declension neuter",
        "Translate 'bellum'",
        "cases are always the same in neuter",
        "genitive plural of 'dōnum'",
        "Templa magna sunt",
        "ablative singular of 'verbum'",
        "neuter second declension noun",
        "Translate 'rēgnum'"
    ],
    "The Verb Sum (to be)": [  # Note: adjusted module name
        "first person singular present of 'sum'",
        "Translate 'sunt'",
        "second person singular of 'sum'",
        "Nōs ___ amīcī",
        "Puellae in hortō sunt",
        "second person plural of 'sum'",
        "Est bonus",
        "form means 'we are'"
    ],
    "First Conjugation Present Active": [  # Note: adjusted module name
        "first person singular present of 'amō'",
        "infinitive ending for first conjugation",
        "Translate 'laborant'",
        "third person singular of 'portō'",
        "Puella cantat",
        "second person plural of 'laudō'",
        "first person plural in first conjugation",
        "Translate 'vocās'"
    ]
}

def main():
    print("Linking Henle Latin questions to course modules...\n")
    
    # Get Henle Latin First Year course
    course_result = supabase.table('language_courses').select('id').eq('slug', 'henle-latin-first-year').single().execute()
    if not course_result.data:
        print("ERROR: Henle Latin First Year course not found!")
        return
    
    course_id = course_result.data['id']
    print(f"Found Henle Latin First Year course: {course_id}\n")
    
    # Get all course modules
    modules_result = supabase.table('course_modules').select('id, title').eq('course_id', course_id).execute()
    module_map = {m['title']: m['id'] for m in modules_result.data}
    
    print(f"Found {len(module_map)} modules:")
    for title in module_map:
        print(f"  - {title}")
    print()
    
    # Get Latin questions from language_questions table
    latin_id = '84acf185-0b8c-4c2a-99f3-c5056be86d23'
    questions_result = supabase.table('language_questions').select('id, question_text').eq('language_id', latin_id).execute()
    
    print(f"Found {len(questions_result.data)} Latin questions in language_questions table\n")
    
    # Link questions to modules
    links_created = 0
    links_failed = 0
    links_skipped = 0
    
    for module_title, question_patterns in question_module_mapping.items():
        # Try to find the module (might have slightly different name)
        module_id = None
        for actual_title, mid in module_map.items():
            if module_title.lower() in actual_title.lower() or actual_title.lower() in module_title.lower():
                module_id = mid
                module_title = actual_title  # Use the actual title
                break
        
        if not module_id:
            print(f"WARNING: Module '{module_title}' not found in database")
            continue
            
        print(f"Linking questions to module: {module_title}")
        
        for pattern in question_patterns:
            # Find questions matching this pattern
            matching_questions = [
                q for q in questions_result.data 
                if pattern.lower() in q['question_text'].lower()
            ]
            
            for question in matching_questions:
                # Create the link
                link_data = {
                    'id': str(uuid.uuid4()),
                    'module_id': module_id,
                    'question_id': question['id'],
                    'display_order': links_created + 1
                }
                
                try:
                    # Check if link already exists
                    existing = supabase.table('module_questions').select('id').eq('module_id', module_id).eq('question_id', question['id']).execute()
                    
                    if not existing.data:
                        supabase.table('module_questions').insert(link_data).execute()
                        print(f"  + Linked: {question['question_text'][:50]}...")
                        links_created += 1
                    else:
                        links_skipped += 1
                except Exception as e:
                    print(f"  X Error linking: {str(e)[:50]}...")
                    links_failed += 1
    
    print("\n" + "="*50)
    print(f"SUMMARY:")
    print(f"  Links created: {links_created}")
    print(f"  Links skipped (already exist): {links_skipped}")
    print(f"  Links failed: {links_failed}")
    print(f"  Total modules processed: {len(question_module_mapping)}")
    
    # Verify the links
    print("\nVerifying questions per module:")
    for title in module_map.keys():
        module_id = module_map[title]
        result = supabase.table('module_questions').select('question_id').eq('module_id', module_id).execute()
        if len(result.data) > 0:
            print(f"  {title}: {len(result.data)} questions")

if __name__ == "__main__":
    main()