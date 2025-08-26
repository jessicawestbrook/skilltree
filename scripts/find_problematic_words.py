"""
Find and remove any remaining problematic words with special characters
"""

import os
import sys
from dotenv import load_dotenv
load_dotenv('.env.local')

from supabase import create_client

SUPABASE_URL = os.getenv('REACT_APP_SUPABASE_URL')
SUPABASE_KEY = os.getenv('REACT_APP_SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print('Finding problematic pending words...')
print('='*60)

# Get pending words
response = supabase.table('language_vocabulary') \
    .select('id, word') \
    .eq('language', 'es') \
    .eq('translation_source', 'PENDING') \
    .execute()

print(f'Total pending words: {len(response.data)}')

problematic = []
for record in response.data:
    word = record['word']
    
    # Check for any non-standard characters
    for c in word:
        # Allow Spanish letters and basic ASCII
        if ord(c) > 127 and c not in 'áéíóúñÁÉÍÓÚÑüÜ':
            problematic.append(record)
            print(f'Found problematic word ID: {record["id"]}')
            print(f'  Word (repr): {repr(word)}')
            print(f'  Problem character: U+{ord(c):04X}')
            break

if problematic:
    print(f'\nFound {len(problematic)} problematic words')
    
    response = input('\nDelete these words? (yes/no): ')
    if response.lower() == 'yes':
        ids_to_delete = [r['id'] for r in problematic]
        
        result = supabase.table('language_vocabulary') \
            .delete() \
            .in_('id', ids_to_delete) \
            .execute()
        
        print(f'Deleted {len(problematic)} problematic words')
        
        # Check remaining
        response = supabase.table('language_vocabulary') \
            .select('count', count='exact') \
            .eq('language', 'es') \
            .eq('translation_source', 'PENDING') \
            .execute()
        
        print(f'Remaining pending words: {response.count}')
else:
    print('\nNo problematic words found in pending set')