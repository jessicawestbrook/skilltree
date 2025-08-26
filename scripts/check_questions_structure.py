"""
Check the structure of the questions table
"""
import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

url = os.environ.get("REACT_APP_SUPABASE_URL")
key = os.environ.get("REACT_APP_SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(url, key)

# Get a sample question to see the structure
print("Checking questions table structure...")

sample = supabase.table('questions').select('*').limit(1).execute()
if sample.data:
    print("\nSample question structure:")
    for key in sample.data[0].keys():
        value = sample.data[0][key]
        if value is not None:
            print(f"  {key}: {type(value).__name__} = {str(value)[:50]}...")

# Count total questions
total = supabase.table('questions').select('id', count='exact').execute()
print(f"\nTotal questions in database: {total.count}")

# Check for Spanish-related questions
spanish_text = supabase.table('questions').select('id, question_text', count='exact').like('question_text', '%Spanish%').limit(5).execute()
print(f"\nQuestions containing 'Spanish': {spanish_text.count}")
if spanish_text.data:
    print("Sample Spanish questions:")
    for q in spanish_text.data[:3]:
        print(f"  - {q['question_text'][:80]}...")

# Check for conjugation questions
conjugation = supabase.table('questions').select('id, question_text', count='exact').like('question_text', '%conjugat%').limit(5).execute()
print(f"\nQuestions containing 'conjugat': {conjugation.count}")
if conjugation.data:
    print("Sample conjugation questions:")
    for q in conjugation.data[:3]:
        print(f"  - {q['question_text'][:80]}...")