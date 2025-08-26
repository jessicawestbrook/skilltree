"""
Remove emoji and special character entries from Spanish vocabulary
"""

import os
from dotenv import load_dotenv
load_dotenv('.env.local')

from supabase import create_client
import re

SUPABASE_URL = os.getenv('REACT_APP_SUPABASE_URL')
SUPABASE_KEY = os.getenv('REACT_APP_SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print('Finding and removing emoji/special character entries...')
print('='*60)

# Get all Spanish words
print('Fetching Spanish vocabulary entries...')
response = supabase.table('language_vocabulary') \
    .select('id, word') \
    .eq('language', 'es') \
    .execute()

entries_to_delete = []
problematic_entries = []

for record in response.data:
    word = record['word']
    
    # Check for replacement character
    if '�' in word:
        problematic_entries.append(record)
        continue
    
    # Skip articles at the beginning
    test_word = word
    for prefix in ['el ', 'la ', 'los ', 'las ']:
        if word.startswith(prefix):
            test_word = word[len(prefix):]
            break
    
    # Check if it's just punctuation or numbers
    if test_word and not any(c.isalpha() for c in test_word):
        entries_to_delete.append(record)
        continue
    
    # Check for single character non-letters
    if len(test_word) == 1 and not test_word.isalpha():
        entries_to_delete.append(record)
        continue
    
    # Check for emoji patterns (using unicode ranges)
    if any(ord(char) > 127 and not char in 'áéíóúñÁÉÍÓÚÑüÜ' for char in test_word):
        # Might be emoji or special unicode
        if not any(c.isalpha() for c in test_word):
            entries_to_delete.append(record)

print(f'\nFound {len(problematic_entries)} entries with replacement character')
if problematic_entries:
    print('Sample entries with replacement character:')
    for e in problematic_entries[:10]:
        print(f'  "{e["word"]}" (id: {e["id"]})')

print(f'\nFound {len(entries_to_delete)} non-word entries to delete')
if entries_to_delete:
    print('Sample entries to delete:')
    for e in entries_to_delete[:10]:
        print(f'  "{e["word"]}" (id: {e["id"]})')

# Delete problematic entries
if problematic_entries or entries_to_delete:
    response = input('\nDo you want to delete these entries? (yes/no): ')
    
    if response.lower() == 'yes':
        all_to_delete = problematic_entries + entries_to_delete
        
        print(f'\nDeleting {len(all_to_delete)} entries...')
        
        # Delete in batches
        batch_size = 50
        deleted_count = 0
        
        for i in range(0, len(all_to_delete), batch_size):
            batch = all_to_delete[i:min(i+batch_size, len(all_to_delete))]
            ids_to_delete = [record['id'] for record in batch]
            
            try:
                response = supabase.table('language_vocabulary') \
                    .delete() \
                    .in_('id', ids_to_delete) \
                    .execute()
                
                deleted_count += len(batch)
                print(f'  Deleted batch {i//batch_size + 1}: {len(batch)} entries')
                
            except Exception as e:
                print(f'  Error deleting batch: {e}')
        
        print(f'\nSuccessfully deleted {deleted_count} entries')
        
        # Verify
        response = supabase.table('language_vocabulary') \
            .select('count', count='exact') \
            .eq('language', 'es') \
            .execute()
        
        print(f'Remaining Spanish words: {response.count:,}')
    else:
        print('Deletion cancelled')
else:
    print('\nNo problematic entries found!')