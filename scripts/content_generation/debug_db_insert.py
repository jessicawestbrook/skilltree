#!/usr/bin/env python3
"""
Debug database insertion to understand the schema issues.
"""

import os
import sys
import uuid
from pathlib import Path
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env.local
env_file = project_root / '.env.local'
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

from supabase import create_client

def main():
    try:
        supabase_url = os.getenv('REACT_APP_SUPABASE_URL')
        supabase_key = os.getenv('REACT_APP_SUPABASE_ANON_KEY')
        supabase = create_client(supabase_url, supabase_key)
        
        print("=== Testing Database Insertions ===")
        
        # Test 1: Try to insert a simple question
        print("\n1. Testing question insertion...")
        question_id = str(uuid.uuid4())
        question_data = {
            'id': question_id,
            'question_text': 'Test question?',
            'options': ['A) Option 1', 'B) Option 2', 'C) Option 3', 'D) Option 4'],
            'correct_answer': 0,
            'explanation': 'Test explanation',
            'difficulty': 'easy',
            'image_url': None,
            'created_at': datetime.now().isoformat()
        }
        
        try:
            response = supabase.table('questions').insert(question_data).execute()
            if response.data:
                print(f"SUCCESS: Inserted question with ID: {question_id}")
            else:
                print(f"FAILED: No data returned from question insert")
                print(f"Response: {response}")
        except Exception as e:
            print(f"ERROR inserting question: {e}")
        
        # Test 2: Try to insert learning content with question_ids
        print("\n2. Testing learning content insertion...")
        content_id = str(uuid.uuid4())
        content_data = {
            'id': content_id,
            'title': 'Test Content',
            'content': 'This is test content',
            'images': [],
            'estimated_time_minutes': 15,
            'difficulty_level': 'intermediate',
            'question_ids': [question_id],  # This might be the problem
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        try:
            response = supabase.table('learning_content').insert(content_data).execute()
            if response.data:
                print(f"SUCCESS: Inserted content with ID: {content_id}")
            else:
                print(f"FAILED: No data returned from content insert")
                print(f"Response: {response}")
        except Exception as e:
            print(f"ERROR inserting content: {e}")
        
        # Test 3: Try different formats for question_ids
        print("\n3. Testing different question_ids formats...")
        
        # Try as JSON array string
        try:
            content_id2 = str(uuid.uuid4())
            content_data2 = content_data.copy()
            content_data2['id'] = content_id2
            content_data2['question_ids'] = f'["{question_id}"]'  # JSON string format
            
            response = supabase.table('learning_content').insert(content_data2).execute()
            if response.data:
                print("SUCCESS: JSON string format worked")
            else:
                print("FAILED: JSON string format failed")
        except Exception as e:
            print(f"JSON string format error: {e}")
        
        # Try without question_ids
        try:
            content_id3 = str(uuid.uuid4())
            content_data3 = content_data.copy()
            content_data3['id'] = content_id3
            del content_data3['question_ids']  # Remove the field
            
            response = supabase.table('learning_content').insert(content_data3).execute()
            if response.data:
                print("SUCCESS: Without question_ids worked")
            else:
                print("FAILED: Without question_ids failed")
        except Exception as e:
            print(f"Without question_ids error: {e}")
        
        # Cleanup - delete test records
        print("\n4. Cleaning up test records...")
        try:
            supabase.table('learning_content').delete().eq('id', content_id).execute()
            supabase.table('learning_content').delete().eq('id', content_id2).execute()
            supabase.table('learning_content').delete().eq('id', content_id3).execute()
            supabase.table('questions').delete().eq('id', question_id).execute()
            print("Cleanup completed")
        except Exception as e:
            print(f"Cleanup error: {e}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()