#!/usr/bin/env python3
"""
Analyze the actual database schema to understand data types.
"""

import os
import sys
from pathlib import Path

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
        
        print("=== Analyzing Database Schema ===")
        
        # Check if there are any existing learning_content records
        try:
            response = supabase.table('learning_content').select('*').limit(3).execute()
            if response.data:
                print(f"\nFound {len(response.data)} existing learning_content records:")
                for i, record in enumerate(response.data):
                    print(f"  Record {i+1}:")
                    for key, value in record.items():
                        print(f"    {key}: {type(value).__name__} = {str(value)[:100]}")
            else:
                print("\nNo existing learning_content records found")
        except Exception as e:
            print(f"Error reading learning_content: {e}")
        
        # Check if there are any existing questions
        try:
            response = supabase.table('questions').select('*').limit(3).execute()
            if response.data:
                print(f"\nFound {len(response.data)} existing questions records:")
                for i, record in enumerate(response.data):
                    print(f"  Record {i+1}:")
                    for key, value in record.items():
                        print(f"    {key}: {type(value).__name__} = {str(value)[:100]}")
            else:
                print("\nNo existing questions records found")
        except Exception as e:
            print(f"Error reading questions: {e}")
        
        # Check RLS policies on questions table
        try:
            response = supabase.rpc('get_rls_policies', {'table_name': 'questions'}).execute()
            print(f"\nRLS policies result: {response}")
        except Exception as e:
            print(f"Error checking RLS policies: {e}")
        
        # Try a simple select to understand what's accessible
        print("\n=== Testing Table Access ===")
        tables_to_test = ['learning_content', 'questions', 'skill_tree_nodes']
        
        for table in tables_to_test:
            try:
                response = supabase.table(table).select('id').limit(1).execute()
                print(f"{table}: Accessible (found {len(response.data) if response.data else 0} records)")
                if response.data and len(response.data) > 0:
                    print(f"  Sample ID type: {type(response.data[0]['id'])} = {response.data[0]['id']}")
            except Exception as e:
                print(f"{table}: Error - {e}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()