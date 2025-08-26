"""
Simple script to add 'the' to English noun translations
"""

import os
from dotenv import load_dotenv
load_dotenv('.env.local')

from supabase import create_client

SUPABASE_URL = os.getenv('REACT_APP_SUPABASE_URL')
SUPABASE_KEY = os.getenv('REACT_APP_SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Adding 'the' to English noun translations")
print("="*60)

# Get nouns without 'the' that look like real nouns
response = supabase.table('language_vocabulary') \
    .select('id, word, english_translation') \
    .eq('language', 'es') \
    .eq('part_of_speech', 'noun') \
    .not_.ilike('english_translation', 'the %') \
    .not_.ilike('english_translation', 'a %') \
    .not_.ilike('english_translation', 'an %') \
    .not_.ilike('english_translation', 'to %') \
    .limit(1000) \
    .execute()

nouns = response.data
print(f"Processing {len(nouns)} nouns...")

updated = 0
skipped = 0
examples = []

for record in nouns:
    translation = record.get('english_translation', '').strip()
    
    # Skip if empty or too short
    if not translation or len(translation) <= 2:
        skipped += 1
        continue
    
    # Skip if it's a pronoun or common word that shouldn't have 'the'
    skip_words = ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
                  'my', 'your', 'his', 'its', 'our', 'their', 'this', 'that', 'these', 'those',
                  'who', 'what', 'where', 'when', 'why', 'how', 'all', 'some', 'any', 'no', 'none',
                  'do', 'go', 'up', 'down', 'in', 'out', 'on', 'off', 'so', 'as', 'if', 'or', 'and', 'but']
    
    if translation.lower() in skip_words:
        skipped += 1
        continue
    
    # Skip if it starts with a number or special character
    if not translation[0].isalpha():
        skipped += 1
        continue
    
    # Skip proper nouns (capitalized, not at sentence start)
    if translation[0].isupper() and len(translation) > 1 and translation[1:].islower():
        # Could be a proper noun, skip it
        skipped += 1
        continue
    
    # Add 'the'
    new_translation = f"the {translation.lower()}"
    
    try:
        supabase.table('language_vocabulary') \
            .update({
                'english_translation': new_translation,
                'definition_english': new_translation
            }) \
            .eq('id', record['id']) \
            .execute()
        
        updated += 1
        
        if len(examples) < 10:
            examples.append(f"{record['word']:30} -> {translation:20} => {new_translation}")
            
    except Exception as e:
        print(f"Error updating {record['word']}: {e}")
        skipped += 1

print(f"\nUpdated: {updated}")
print(f"Skipped: {skipped}")

if examples:
    print("\nExamples:")
    for ex in examples:
        print(f"  {ex}")

# Final count
response = supabase.table('language_vocabulary') \
    .select('count', count='exact') \
    .eq('language', 'es') \
    .eq('part_of_speech', 'noun') \
    .ilike('english_translation', 'the %') \
    .execute()

print(f"\nTotal nouns with 'the': {response.count:,}")