import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables
load_dotenv('.env.local')

# Initialize Supabase client
url = os.environ.get("REACT_APP_SUPABASE_URL")
key = os.environ.get("REACT_APP_SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

print("Checking Latin language and course in database...\n")

# Check if Latin exists in languages table
latin_response = supabase.table('languages').select('*').eq('name', 'Latin').execute()
if latin_response.data:
    latin_lang = latin_response.data[0]
    print(f"[OK] Latin language found: ID = {latin_lang['id']}")
    
    # Check for Latin course
    course_response = supabase.table('language_courses').select('*').eq('language_id', latin_lang['id']).execute()
    if course_response.data:
        course = course_response.data[0]
        print(f"[OK] Latin course found: '{course['name']}'")
        print(f"  - Course ID: {course['id']}")
        print(f"  - Description: {course['description'][:100]}...")
        
        # Check course modules
        modules_response = supabase.table('course_modules').select('*').eq('course_id', course['id']).order('chapter_number').execute()
        print(f"  - Modules: {len(modules_response.data)} chapters found")
        
        # Check questions linked to course
        if modules_response.data:
            first_module = modules_response.data[0]
            questions_response = supabase.table('module_questions').select('*').eq('module_id', first_module['id']).execute()
            print(f"  - Questions in Chapter 1: {len(questions_response.data)}")
    else:
        print("[X] No Latin course found")
else:
    print("[X] Latin language not found in database")

# Check skill tree nodes for Latin
print("\nChecking skill tree nodes for Latin category...")
latin_nodes = supabase.table('skill_tree_nodes').select('*').ilike('name', '%Latin%').execute()
if latin_nodes.data:
    print(f"[OK] Found {len(latin_nodes.data)} Latin-related nodes in skill tree")
    for node in latin_nodes.data[:3]:
        print(f"  - {node['name']} (ID: {node['id']})")
else:
    print("[X] No Latin nodes found in skill tree")