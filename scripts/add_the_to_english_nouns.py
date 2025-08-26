"""
Add 'the' to English translations of Spanish nouns
"""

import os
import sys
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv('.env.local')

from supabase import create_client

SUPABASE_URL = os.getenv('REACT_APP_SUPABASE_URL')
SUPABASE_KEY = os.getenv('REACT_APP_SUPABASE_SERVICE_ROLE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: Missing environment variables")
    sys.exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def needs_the_prefix(translation):
    """Check if translation needs 'the' prefix"""
    if not translation:
        return False
    
    translation_lower = translation.lower()
    
    # Skip if already has 'the'
    if translation_lower.startswith('the '):
        return False
    
    # Skip if it's a proper noun (capitalized) or already has an article
    if translation_lower.startswith(('a ', 'an ', 'my ', 'your ', 'his ', 'her ', 'its ', 'our ', 'their ')):
        return False
    
    # Skip single letters or very short words that might be abbreviations
    if len(translation) <= 2:
        return False
    
    # Skip if it starts with a number
    if translation[0].isdigit():
        return False
    
    return True

def main():
    print("Adding 'the' to English translations of Spanish nouns")
    print("="*60)
    
    # Get count of nouns without 'the'
    response = supabase.table('language_vocabulary') \
        .select('count', count='exact') \
        .eq('language', 'es') \
        .eq('part_of_speech', 'noun') \
        .not_.ilike('english_translation', 'the %') \
        .execute()
    
    total_without_the = response.count
    print(f"Nouns without 'the' in translation: {total_without_the:,}")
    
    if total_without_the == 0:
        print("All nouns already have 'the' prefix!")
        return
    
    # Process in batches
    batch_size = 2000
    total_updated = 0
    
    while True:
        # Get batch of nouns without 'the'
        response = supabase.table('language_vocabulary') \
            .select('id, word, english_translation, definition_english') \
            .eq('language', 'es') \
            .eq('part_of_speech', 'noun') \
            .not_.ilike('english_translation', 'the %') \
            .limit(batch_size) \
            .execute()
        
        nouns_to_update = response.data
        
        if not nouns_to_update:
            break
        
        print(f"\nProcessing batch of {len(nouns_to_update)} nouns...")
        
        batch_updated = 0
        examples = []
        
        for record in nouns_to_update:
            translation = record.get('english_translation', '')
            definition = record.get('definition_english', '')
            
            if needs_the_prefix(translation):
                # Add 'the' to translation
                new_translation = f"the {translation}"
                
                # Also update definition if it matches translation
                new_definition = definition
                if definition and definition.lower() == translation.lower():
                    new_definition = f"the {definition}"
                
                try:
                    update_data = {
                        'english_translation': new_translation,
                        'definition_english': new_definition
                    }
                    
                    supabase.table('language_vocabulary') \
                        .update(update_data) \
                        .eq('id', record['id']) \
                        .execute()
                    
                    batch_updated += 1
                    
                    if len(examples) < 10:
                        examples.append(f"{record['word']} -> {translation} => {new_translation}")
                    
                except Exception as e:
                    print(f"  Error updating '{record['word']}': {e}")
        
        total_updated += batch_updated
        print(f"  Updated {batch_updated} nouns in this batch")
        
        if examples:
            print("\nExamples from this batch:")
            for ex in examples:
                print(f"  {ex}")
        
        # Small delay between batches
        time.sleep(0.5)
    
    # Final status
    print("\n" + "="*60)
    print("COMPLETE")
    print(f"Total nouns updated: {total_updated:,}")
    
    # Check remaining
    response = supabase.table('language_vocabulary') \
        .select('count', count='exact') \
        .eq('language', 'es') \
        .eq('part_of_speech', 'noun') \
        .not_.ilike('english_translation', 'the %') \
        .execute()
    
    print(f"Remaining nouns without 'the': {response.count:,}")
    
    # Show some examples of updated nouns
    response = supabase.table('language_vocabulary') \
        .select('word, english_translation') \
        .eq('language', 'es') \
        .eq('part_of_speech', 'noun') \
        .ilike('english_translation', 'the %') \
        .limit(20) \
        .execute()
    
    print("\nExample nouns with 'the' prefix:")
    for r in response.data[:10]:
        print(f"  {r['word']:30} -> {r['english_translation']}")

if __name__ == "__main__":
    main()