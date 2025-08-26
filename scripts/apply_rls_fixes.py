"""
Apply RLS policy fixes for user_module_progress table
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Initialize Supabase client with service role key
url = os.environ.get("REACT_APP_SUPABASE_URL")
service_key = os.environ.get("REACT_APP_SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, service_key)

# Read the SQL file
with open('scripts/fix_module_progress_rls.sql', 'r') as f:
    sql_content = f.read()

# Split into individual statements (Supabase SDK doesn't handle multiple statements well)
statements = [s.strip() for s in sql_content.split(';') if s.strip() and not s.strip().startswith('--')]

print("Applying RLS policy fixes...")
print("=" * 50)

for i, statement in enumerate(statements, 1):
    # Skip SELECT statements for now (verification queries)
    if statement.upper().startswith('SELECT'):
        print(f"Skipping verification query {i}")
        continue
        
    try:
        # Add semicolon back
        statement = statement + ';'
        print(f"\nExecuting statement {i}:")
        print(statement[:100] + "..." if len(statement) > 100 else statement)
        
        # Execute via RPC (raw SQL)
        result = supabase.rpc('exec_sql', {'sql': statement}).execute()
        print(f"✓ Success")
    except Exception as e:
        if 'exec_sql' in str(e):
            print(f"! Cannot execute raw SQL via SDK, statement {i} needs manual execution")
        else:
            print(f"✗ Error: {e}")

print("\n" + "=" * 50)
print("IMPORTANT: The RLS policies need to be applied manually in Supabase SQL Editor")
print("=" * 50)
print("\nTo apply the fixes:")
print("1. Go to your Supabase dashboard: https://app.supabase.com")
print("2. Navigate to SQL Editor")
print("3. Copy and paste the contents of scripts/fix_module_progress_rls.sql")
print("4. Click 'Run' to execute")
print("\nThis will:")
print("- Drop all existing RLS policies on user_module_progress")
print("- Create new, more permissive policies")
print("- Allow authenticated users to read/write their own progress")