"""
Batch update remaining Spanish verbs to add 'to' prefix
Uses SQL-like batch operations for speed
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Install required packages if needed
for package in ['supabase']:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        os.system(f"{sys.executable} -m pip install {package}")

from supabase import create_client

# Initialize Supabase with service role key
SUPABASE_URL = os.getenv('REACT_APP_SUPABASE_URL')
SUPABASE_KEY = os.getenv('REACT_APP_SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def main():
    print("Batch updating Spanish verb translations with 'to' prefix")
    print("="*60)
    
    # Get verbs that need updating
    print("\nFetching verbs without 'to' prefix...")
    
    # Get all verbs that don't start with 'to ' and aren't conjugated forms
    response = supabase.table('language_vocabulary') \
        .select('id, word, english_translation') \
        .eq('language', 'es') \
        .eq('part_of_speech', 'verb') \
        .not_.like('english_translation', 'to %') \
        .not_.like('english_translation', 'I %') \
        .not_.like('english_translation', 'You %') \
        .not_.like('english_translation', 'He %') \
        .not_.like('english_translation', 'She %') \
        .not_.like('english_translation', 'It %') \
        .not_.like('english_translation', 'We %') \
        .not_.like('english_translation', 'They %') \
        .not_.eq('english_translation', 'PENDING') \
        .execute()
    
    verbs_to_update = response.data
    print(f"Found {len(verbs_to_update)} verbs to update")
    
    if not verbs_to_update:
        print("No verbs need updating!")
        return
    
    # Show sample
    print("\nSample verbs to update:")
    for verb in verbs_to_update[:5]:
        print(f"  {verb['word']}: '{verb['english_translation']}' -> 'to {verb['english_translation']}'")
    
    # Batch update
    print(f"\nUpdating {len(verbs_to_update)} verbs in batches...")
    
    batch_size = 50
    successful = 0
    
    for i in range(0, len(verbs_to_update), batch_size):
        batch = verbs_to_update[i:min(i+batch_size, len(verbs_to_update))]
        
        # Update each in batch
        for verb in batch:
            try:
                new_translation = f"to {verb['english_translation']}"
                
                supabase.table('language_vocabulary') \
                    .update({
                        'english_translation': new_translation,
                        'definition_english': new_translation
                    }) \
                    .eq('id', verb['id']) \
                    .execute()
                
                successful += 1
                
            except Exception as e:
                print(f"  Error updating {verb['word']}: {e}")
        
        print(f"  Batch {i//batch_size + 1}: Updated {len(batch)} verbs (total: {successful})")
    
    # Final summary
    print(f"\n{'='*60}")
    print("BATCH UPDATE COMPLETE")
    print(f"Successfully updated: {successful} verbs")
    
    # Verify final state
    response = supabase.table('language_vocabulary') \
        .select('count', count='exact') \
        .eq('language', 'es') \
        .eq('part_of_speech', 'verb') \
        .like('english_translation', 'to %') \
        .execute()
    
    response2 = supabase.table('language_vocabulary') \
        .select('count', count='exact') \
        .eq('language', 'es') \
        .eq('part_of_speech', 'verb') \
        .execute()
    
    print(f"\nFinal status:")
    print(f"  Total Spanish verbs: {response2.count:,}")
    print(f"  Verbs with 'to' prefix: {response.count:,}")
    print(f"  Percentage with 'to': {response.count*100/response2.count:.1f}%")

if __name__ == "__main__":
    main()