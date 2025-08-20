#!/usr/bin/env python3
"""
Check database schema for content generation tables.
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
        
        print("Checking database schema...")
        
        # Try to get a sample from learning_content table if it exists
        try:
            result = supabase.table('learning_content').select('*').limit(1).execute()
            if result.data:
                print("\nlearning_content table columns:")
                for col in result.data[0].keys():
                    print(f"  - {col}")
            else:
                print("\nlearning_content table exists but has no data")
        except Exception as e:
            print(f"\nlearning_content table error: {e}")
        
        # Try to get a sample from questions table if it exists
        try:
            result = supabase.table('questions').select('*').limit(1).execute()
            if result.data:
                print("\nquestions table columns:")
                for col in result.data[0].keys():
                    print(f"  - {col}")
            else:
                print("\nquestions table exists but has no data")
        except Exception as e:
            print(f"\nquestions table error: {e}")
        
        # Check skill_tree_nodes table for reference
        try:
            result = supabase.table('skill_tree_nodes').select('*').limit(1).execute()
            if result.data:
                print("\nskill_tree_nodes table columns (reference):")
                for col in result.data[0].keys():
                    print(f"  - {col}")
        except Exception as e:
            print(f"\nskill_tree_nodes table error: {e}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()