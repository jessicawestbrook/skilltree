"""
Insert Spanish verb conjugation questions into the database
"""
import json
import os
from supabase import create_client
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv('.env.local')

url = os.environ.get("REACT_APP_SUPABASE_URL")
key = os.environ.get("REACT_APP_SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(url, key)

def insert_questions():
    # Load the questions
    with open('scripts/spanish_data/anki_spanish_questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"Loaded {len(questions)} Spanish verb conjugation questions")
    
    # Format questions for database insertion
    db_questions = []
    for q in questions:
        db_questions.append({
            'id': str(uuid.uuid4()),
            'question_text': q['question_text'],
            'options': q['options'],  # Array of options
            'correct_answer': q['correct_answer'],  # Integer index
            'explanation': q['explanation'],
            'difficulty': 'average',  # Use valid difficulty value (easy/average/hard)
            'image_url': None  # No images for these questions
        })
    
    # Insert in batches of 100
    batch_size = 100
    total_inserted = 0
    failed = 0
    
    for i in range(0, len(db_questions), batch_size):
        batch = db_questions[i:i+batch_size]
        try:
            result = supabase.table('questions').insert(batch).execute()
            total_inserted += len(batch)
            print(f"Inserted batch {i//batch_size + 1}: {len(batch)} questions (Total: {total_inserted}/{len(questions)})")
        except Exception as e:
            print(f"Error inserting batch {i//batch_size + 1}: {str(e)}")
            failed += len(batch)
    
    print(f"\n{'='*50}")
    print(f"INSERTION COMPLETE:")
    print(f"  Total questions: {len(questions)}")
    print(f"  Successfully inserted: {total_inserted}")
    print(f"  Failed: {failed}")
    
    # Verify insertion
    count_result = supabase.table('questions').select('id', count='exact').like('question_text', '%Fill in the blank%').execute()
    print(f"\nVerification: Found {count_result.count} fill-in-the-blank questions in database")
    
    return total_inserted

if __name__ == "__main__":
    insert_questions()