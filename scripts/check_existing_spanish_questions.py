"""
Check what Spanish questions already exist in the database
"""
import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

url = os.environ.get("REACT_APP_SUPABASE_URL")
key = os.environ.get("REACT_APP_SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(url, key)

# Check for Spanish questions
print("Checking for existing Spanish questions...")

# Check by category
spanish_category = supabase.table('questions').select('id, question_text', count='exact').eq('category', 'Spanish Verb Conjugations').limit(5).execute()
print(f"\nSpanish Verb Conjugations category: {spanish_category.count} questions")
if spanish_category.data:
    print("Sample questions:")
    for q in spanish_category.data[:3]:
        print(f"  - {q['question_text'][:80]}...")

# Check by language
spanish_lang = supabase.table('questions').select('id', count='exact').eq('language', 'es').execute()
print(f"\nQuestions with language='es': {spanish_lang.count} questions")

# Check for any question containing Spanish keywords
spanish_text = supabase.table('questions').select('id', count='exact').like('question_text', '%Spanish%').execute()
print(f"\nQuestions containing 'Spanish': {spanish_text.count} questions")

# Check for fill in the blank questions
fill_blank = supabase.table('questions').select('id', count='exact').like('question_text', '%Fill in the blank%').execute()
print(f"\nQuestions with 'Fill in the blank': {fill_blank.count} questions")