"""
Update database constraint from 'average' to 'medium' for difficulty field
"""
import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

url = os.environ.get("REACT_APP_SUPABASE_URL")
key = os.environ.get("REACT_APP_SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(url, key)


print("="*50)
print("UPDATING DIFFICULTY CONSTRAINT FROM 'average' TO 'medium'")
print("="*50)

# Step 1: Count current distribution
print("\n1. Current difficulty distribution:")
for diff in ['easy', 'average', 'medium', 'hard']:
    count = supabase.table('questions').select('id', count='exact').eq('difficulty', diff).execute()
    print(f"   {diff}: {count.count} questions")

# Step 2: Create backup (using Supabase client)
print("\n2. Creating backup of current data...")
all_questions = []
limit = 1000
offset = 0

while True:
    batch = supabase.table('questions').select('*').range(offset, offset + limit - 1).execute()
    if not batch.data:
        break
    all_questions.extend(batch.data)
    offset += limit
    print(f"   Backed up {len(all_questions)} questions...")

print(f"   Total questions backed up in memory: {len(all_questions)}")

# Step 3: Update all 'average' to 'medium' 
print("\n3. Updating all 'average' difficulty to 'medium'...")
try:
    # Get all IDs with 'average' difficulty
    average_questions = supabase.table('questions').select('id').eq('difficulty', 'average').execute()
    
    if average_questions.data:
        # Update in batches
        batch_size = 100
        total_ids = [q['id'] for q in average_questions.data]
        
        for i in range(0, len(total_ids), batch_size):
            batch_ids = total_ids[i:i+batch_size]
            
            # First, we need to temporarily remove the constraint by using a different value
            # Try updating to 'easy' first, then to 'medium'
            try:
                # Try direct update to medium (in case constraint allows it)
                result = supabase.table('questions').update({'difficulty': 'medium'}).in_('id', batch_ids).execute()
                print(f"   Updated batch {i//batch_size + 1}: {len(batch_ids)} questions")
            except Exception as e:
                if "violates check constraint" in str(e):
                    # Constraint doesn't allow 'medium' yet
                    # We'll need to drop and recreate the constraint
                    print(f"   Cannot update to 'medium' - constraint needs to be modified")
                    print(f"   Error: {str(e)[:100]}...")
                    
                    print("\n   NOTE: The constraint needs to be updated at the database level.")
                    print("   Please run the following SQL in Supabase SQL Editor:")
                    print("")
                    print("   -- Drop the existing constraint")
                    print("   ALTER TABLE questions DROP CONSTRAINT questions_difficulty_check;")
                    print("")
                    print("   -- Add the new constraint with 'medium' instead of 'average'")
                    print("   ALTER TABLE questions ADD CONSTRAINT questions_difficulty_check")
                    print("   CHECK (difficulty IN ('easy', 'medium', 'hard'));")
                    print("")
                    print("   Then run this script again to update the data.")
                    break
                else:
                    raise e
        
        print(f"\n   Total questions to update: {len(total_ids)}")
    else:
        print("   No questions found with 'average' difficulty")

except Exception as e:
    print(f"\nError during update: {str(e)}")
    print("\nTo complete this update, you need to:")
    print("1. Go to Supabase SQL Editor")
    print("2. Run the SQL commands in scripts/update_difficulty_constraint.sql")
    print("3. Run this script again if needed")

# Step 4: Verify final distribution
print("\n4. Final difficulty distribution:")
for diff in ['easy', 'average', 'medium', 'hard']:
    count = supabase.table('questions').select('id', count='exact').eq('difficulty', diff).execute()
    if count.count > 0:
        print(f"   {diff}: {count.count} questions")

print("\n" + "="*50)
print("COMPLETE")
print("="*50)