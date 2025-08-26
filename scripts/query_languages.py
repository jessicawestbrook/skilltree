#!/usr/bin/env python3
"""
Query the languages table to see what languages exist.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
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

def query_languages():
    """Query the languages table."""
    try:
        supabase_url = os.getenv('REACT_APP_SUPABASE_URL')
        anon_key = os.getenv('REACT_APP_SUPABASE_ANON_KEY')
        
        if not supabase_url or not anon_key:
            print("Missing Supabase environment variables!")
            return
        
        supabase = create_client(supabase_url, anon_key)
        
        print("Querying languages table...")
        response = supabase.table('languages').select('*').execute()
        
        if response.data:
            print(f"Found {len(response.data)} languages:")
            print("-" * 50)
            for i, language in enumerate(response.data, 1):
                # Handle encoding safely
                try:
                    print(f"{i}. {language}")
                except UnicodeEncodeError:
                    # Print with safe encoding
                    lang_str = str(language).encode('ascii', 'replace').decode('ascii')
                    print(f"{i}. {lang_str}")
                print()
        else:
            print("No languages found or table is empty")
            
    except Exception as e:
        print(f"Error querying languages table: {e}")

if __name__ == "__main__":
    query_languages()