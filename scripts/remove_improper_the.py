"""
Remove 'the' from English translations of non-nouns
"""

import os
from dotenv import load_dotenv
load_dotenv('.env.local')

from supabase import create_client

SUPABASE_URL = os.getenv('REACT_APP_SUPABASE_URL')
SUPABASE_KEY = os.getenv('REACT_APP_SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Removing 'the' from non-noun English translations")
print("="*60)

# Get all non-nouns with 'the' in translation
response = supabase.table('language_vocabulary') \
    .select('id, word, english_translation, definition_english, part_of_speech') \
    .eq('language', 'es') \
    .neq('part_of_speech', 'noun') \
    .ilike('english_translation', 'the %') \
    .execute()

words_to_fix = response.data
print(f"Found {len(words_to_fix)} non-nouns with 'the' to fix")

if words_to_fix:
    print("\nExamples to fix:")
    for r in words_to_fix[:10]:
        print(f"  {r['word']:25} -> {r['english_translation']:25} ({r['part_of_speech']})")
    
    print("\nFixing...")
    fixed = 0
    
    for record in words_to_fix:
        translation = record.get('english_translation', '')
        definition = record.get('definition_english', '')
        
        # Remove 'the ' from the beginning
        if translation.lower().startswith('the '):
            new_translation = translation[4:]  # Remove 'the '
            
            # Also update definition if it matches
            new_definition = definition
            if definition and definition.lower().startswith('the '):
                new_definition = definition[4:]
            
            try:
                supabase.table('language_vocabulary') \
                    .update({
                        'english_translation': new_translation,
                        'definition_english': new_definition
                    }) \
                    .eq('id', record['id']) \
                    .execute()
                
                fixed += 1
                if fixed <= 10:
                    print(f"  Fixed: {record['word']:25} -> {new_translation}")
                    
            except Exception as e:
                print(f"  Error fixing {record['word']}: {e}")
    
    print(f"\nFixed {fixed} translations")

# Also fix verbs that should have 'to' instead of 'the'
print("\n" + "-"*60)
print("Checking verbs that need 'to' instead of 'the'...")

response = supabase.table('language_vocabulary') \
    .select('id, word, english_translation') \
    .eq('language', 'es') \
    .eq('part_of_speech', 'verb') \
    .not_.ilike('english_translation', 'to %') \
    .not_.ilike('english_translation', 'the %') \
    .limit(100) \
    .execute()

verbs_needing_to = response.data
if verbs_needing_to:
    print(f"Found {len(verbs_needing_to)} verbs without 'to' prefix")
    fixed_verbs = 0
    
    for record in verbs_needing_to:
        translation = record.get('english_translation', '').strip()
        
        # Skip if it's a conjugated form (starts with pronouns)
        conjugated_starts = ['i ', 'you ', 'he ', 'she ', 'it ', 'we ', 'they ', "i'm", "you're", "he's", "she's", "it's", "we're", "they're"]
        if any(translation.lower().startswith(p) for p in conjugated_starts):
            continue
        
        # Skip if it's already an infinitive form or modal
        if translation.lower() in ['be', 'have', 'do', 'can', 'will', 'shall', 'may', 'might', 'could', 'would', 'should']:
            continue
        
        # Add 'to' prefix
        new_translation = f"to {translation}"
        
        try:
            supabase.table('language_vocabulary') \
                .update({
                    'english_translation': new_translation,
                    'definition_english': new_translation
                }) \
                .eq('id', record['id']) \
                .execute()
            
            fixed_verbs += 1
            if fixed_verbs <= 5:
                print(f"  Added 'to': {record['word']:25} -> {new_translation}")
                
        except Exception as e:
            print(f"  Error fixing verb {record['word']}: {e}")
    
    if fixed_verbs > 0:
        print(f"Added 'to' to {fixed_verbs} verbs")

# Final status
print("\n" + "="*60)
print("Final Status:")

# Check remaining issues
response = supabase.table('language_vocabulary') \
    .select('count', count='exact') \
    .eq('language', 'es') \
    .neq('part_of_speech', 'noun') \
    .ilike('english_translation', 'the %') \
    .execute()

print(f"Non-nouns with 'the': {response.count} (should be 0)")

response = supabase.table('language_vocabulary') \
    .select('count', count='exact') \
    .eq('language', 'es') \
    .eq('part_of_speech', 'verb') \
    .ilike('english_translation', 'to %') \
    .execute()
verbs_with_to = response.count

response = supabase.table('language_vocabulary') \
    .select('count', count='exact') \
    .eq('language', 'es') \
    .eq('part_of_speech', 'verb') \
    .execute()
total_verbs = response.count

print(f"Verbs with 'to': {verbs_with_to} / {total_verbs} ({verbs_with_to/total_verbs*100:.1f}%)")