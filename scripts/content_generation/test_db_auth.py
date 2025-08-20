#!/usr/bin/env python3
"""
Test database authentication and permissions for content insertion.
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

def test_with_service_key():
    """Test with service role key if available."""
    service_key = os.getenv('REACT_APP_SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_SERVICE_KEY')
    if not service_key:
        print("No service key found in environment")
        return False
    
    try:
        supabase_url = os.getenv('REACT_APP_SUPABASE_URL')
        supabase = create_client(supabase_url, service_key)
        
        print("Testing with service key...")
        
        # Try to insert test content
        test_content = {
            'title': 'Test Content for Auth',
            'content': 'This is a test to check authentication permissions',
            'estimated_time_minutes': 5,
            'difficulty_level': 'easy',
            'images': []
        }
        
        response = supabase.table('learning_content').insert(test_content).execute()
        
        if response.data:
            content_id = response.data[0]['id']
            print(f"SUCCESS: Service key can insert content (ID: {content_id})")
            
            # Clean up
            supabase.table('learning_content').delete().eq('id', content_id).execute()
            print("Test record cleaned up")
            return True
        else:
            print("FAILED: Service key insert returned no data")
            return False
            
    except Exception as e:
        print(f"Service key test error: {e}")
        return False

def test_with_anon_key():
    """Test with anonymous key (current method)."""
    try:
        supabase_url = os.getenv('REACT_APP_SUPABASE_URL')
        anon_key = os.getenv('REACT_APP_SUPABASE_ANON_KEY')
        supabase = create_client(supabase_url, anon_key)
        
        print("Testing with anon key...")
        
        # Check what we can read
        response = supabase.table('learning_content').select('id').limit(1).execute()
        print(f"Anon key can read learning_content: {len(response.data) if response.data else 0} records")
        
        # Try to insert (will likely fail)
        test_content = {
            'title': 'Test Content for Anon Auth',
            'content': 'This is a test with anon key',
            'estimated_time_minutes': 5,
            'difficulty_level': 'easy',
            'images': []
        }
        
        try:
            response = supabase.table('learning_content').insert(test_content).execute()
            if response.data:
                print("SUCCESS: Anon key can insert content")
                return True
            else:
                print("FAILED: Anon key insert returned no data")
                return False
        except Exception as e:
            print(f"Anon key insert error: {e}")
            return False
            
    except Exception as e:
        print(f"Anon key test error: {e}")
        return False

def check_auth_status():
    """Check current authentication status."""
    try:
        supabase_url = os.getenv('REACT_APP_SUPABASE_URL')
        anon_key = os.getenv('REACT_APP_SUPABASE_ANON_KEY')
        supabase = create_client(supabase_url, anon_key)
        
        # Try to get current user/session
        user = supabase.auth.get_user()
        print(f"Current user: {user}")
        
    except Exception as e:
        print(f"Auth status check error: {e}")

def main():
    print("=== Database Authentication Test ===")
    
    print("\n1. Checking available keys...")
    supabase_url = os.getenv('REACT_APP_SUPABASE_URL')
    anon_key = os.getenv('REACT_APP_SUPABASE_ANON_KEY')
    service_key = os.getenv('REACT_APP_SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_SERVICE_KEY')
    
    print(f"URL: {'YES' if supabase_url else 'NO'}")
    print(f"Anon Key: {'YES' if anon_key else 'NO'}")
    print(f"Service Key: {'YES' if service_key else 'NO'}")
    
    print("\n2. Testing authentication methods...")
    
    # Check current auth status
    check_auth_status()
    
    # Test with service key first (if available)
    service_success = test_with_service_key()
    
    # Test with anon key
    anon_success = test_with_anon_key()
    
    print("\n=== Results ===")
    print(f"Service key works: {'YES' if service_success else 'NO'}")
    print(f"Anon key works: {'YES' if anon_success else 'NO'}")
    
    if service_success:
        print("\nRECOMMENDATION: Use service key for content generation")
    elif anon_success:
        print("\nRECOMMENDATION: Anon key is sufficient")
    else:
        print("\nRECOMMENDATION: Need to set up proper authentication")
        print("Options:")
        print("1. Add REACT_APP_SUPABASE_SERVICE_KEY to .env.local")
        print("2. Modify RLS policies to allow anon insertions")
        print("3. Authenticate as a user before inserting")

if __name__ == "__main__":
    main()