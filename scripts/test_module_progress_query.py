"""
Test the exact query that's causing 406 errors
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Initialize Supabase client with different keys to test
url = os.environ.get("REACT_APP_SUPABASE_URL")

print("Testing user_module_progress queries...\n")

# Test 1: With service role key (bypasses RLS)
print("1. Testing with SERVICE ROLE key (bypasses RLS):")
service_key = os.environ.get("REACT_APP_SUPABASE_SERVICE_ROLE_KEY")
if service_key:
    supabase_service = create_client(url, service_key)
    try:
        result = supabase_service.table('user_module_progress').select('*').limit(1).execute()
        print(f"   SUCCESS: Query worked. Found {len(result.data)} records")
    except Exception as e:
        print(f"   ERROR: {e}")
else:
    print("   SKIPPED: No service role key found")

print("\n2. Testing with ANON key (uses RLS):")
anon_key = os.environ.get("REACT_APP_SUPABASE_ANON_KEY")
if anon_key:
    supabase_anon = create_client(url, anon_key)
    try:
        # Test basic select
        result = supabase_anon.table('user_module_progress').select('*').limit(1).execute()
        print(f"   SUCCESS: Basic query worked. Found {len(result.data)} records")
    except Exception as e:
        print(f"   ERROR on basic query: {e}")
    
    try:
        # Test the exact failing query pattern
        test_user_id = "5876bd4e-5e68-4b4d-be15-8f0171bfae93"
        test_module_id = "89108174-0344-4571-8d2e-2d0a885d2463"
        
        result = supabase_anon.table('user_module_progress')\
            .select('*')\
            .eq('user_id', test_user_id)\
            .eq('module_id', test_module_id)\
            .execute()
        print(f"   SUCCESS: Specific query worked. Found {len(result.data)} records")
    except Exception as e:
        print(f"   ERROR on specific query: {e}")
        if '406' in str(e):
            print("   >>> This is the 406 error! RLS policies are blocking the query.")
else:
    print("   SKIPPED: No anon key found")

print("\n3. Checking table existence and structure:")
if service_key:
    supabase_service = create_client(url, service_key)
    try:
        # Get one row to see structure
        result = supabase_service.table('user_module_progress').select('*').limit(1).execute()
        if result.data and len(result.data) > 0:
            print("   Table structure (from sample row):")
            for key in result.data[0].keys():
                print(f"     - {key}")
        else:
            print("   Table exists but is empty")
            # Try to check structure with a dummy insert
            try:
                test_insert = supabase_service.table('user_module_progress').insert({
                    'user_id': '00000000-0000-0000-0000-000000000000',
                    'module_id': '00000000-0000-0000-0000-000000000000'
                }).execute()
                print("   ERROR: Test insert should have failed on foreign key")
            except Exception as e:
                if 'violates foreign key' in str(e):
                    print("   Table structure is correct (foreign keys working)")
                else:
                    print(f"   Unexpected error: {e}")
    except Exception as e:
        print(f"   ERROR: {e}")

print("\n" + "="*50)
print("DIAGNOSIS:")
print("="*50)
print("\nIf you see 406 errors with the ANON key but not SERVICE ROLE key,")
print("it means RLS policies are blocking access.")
print("\nTo fix:")
print("1. Run the SQL script: fix_module_progress_rls.sql")
print("2. This will create more permissive RLS policies")
print("3. Test again with this script")
print("\nThe 406 error specifically means 'Not Acceptable' which in Supabase")
print("usually indicates that RLS is enabled but no policy allows the query.")