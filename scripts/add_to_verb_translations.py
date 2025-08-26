"""
Add 'to' prefix to English translations of Spanish verbs
For example: "hacer" -> "to make" instead of just "make"
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
if not SUPABASE_KEY:
    print("Error: Service role key not found!")
    sys.exit(1)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def needs_to_prefix(translation):
    """Check if translation needs 'to' prefix"""
    if not translation:
        return False
    
    translation_lower = translation.lower().strip()
    
    # Skip if already has 'to'
    if translation_lower.startswith('to '):
        return False
    
    # Skip if it's just a placeholder or same as Spanish
    if translation_lower in ['pending', 'n/a', '']:
        return False
    
    # Skip if it starts with a pronoun (conjugated form)
    pronouns = ['i ', 'you ', 'he ', 'she ', 'it ', 'we ', 'they ', 
                'i\'m ', 'you\'re ', 'he\'s ', 'she\'s ', 'it\'s ', 'we\'re ', 'they\'re ',
                'i\'ve ', 'you\'ve ', 'he\'s ', 'she\'s ', 'we\'ve ', 'they\'ve ']
    for pronoun in pronouns:
        if translation_lower.startswith(pronoun):
            return False
    
    # Skip if it's a gerund or past participle
    if translation_lower.endswith('ing') or translation_lower.endswith('ed'):
        return False
    
    return True

def main():
    print("Adding 'to' prefix to Spanish verb translations")
    print("="*60)
    
    # Get all Spanish verbs
    print("\nFetching Spanish verbs...")
    response = supabase.table('language_vocabulary') \
        .select('id, word, english_translation, definition_english, part_of_speech') \
        .eq('language', 'es') \
        .eq('part_of_speech', 'verb') \
        .execute()
    
    verbs = response.data
    print(f"Found {len(verbs):,} Spanish verbs")
    
    # Process verbs
    updates_needed = []
    examples = []
    
    for verb in verbs:
        translation = verb.get('english_translation', '')
        definition = verb.get('definition_english', '')
        
        # Check if translation needs 'to' prefix
        if needs_to_prefix(translation):
            new_translation = f"to {translation}"
            new_definition = f"to {definition}" if definition and needs_to_prefix(definition) else new_translation
            
            updates_needed.append({
                'id': verb['id'],
                'word': verb['word'],
                'old_translation': translation,
                'new_translation': new_translation,
                'new_definition': new_definition
            })
            
            if len(examples) < 10:
                examples.append((verb['word'], translation, new_translation))
    
    print(f"\nFound {len(updates_needed)} verbs that need 'to' prefix")
    
    if not updates_needed:
        print("No verbs need updating!")
        return
    
    # Show examples
    if examples:
        print("\nExample updates:")
        for word, old, new in examples:
            print(f"  {word}: '{old}' -> '{new}'")
    
    # Update database
    print(f"\nUpdating {len(updates_needed)} verbs...")
    
    successful = 0
    failed = 0
    
    for i, update in enumerate(updates_needed):
        try:
            # Update both translation and definition
            supabase.table('language_vocabulary') \
                .update({
                    'english_translation': update['new_translation'],
                    'definition_english': update['new_definition']
                }) \
                .eq('id', update['id']) \
                .execute()
            
            successful += 1
            
            # Progress indicator
            if (i + 1) % 100 == 0:
                print(f"  Progress: {i + 1}/{len(updates_needed)} verbs updated...")
                
        except Exception as e:
            print(f"  Error updating {update['word']}: {e}")
            failed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("UPDATE COMPLETE")
    print(f"Successfully updated: {successful:,} verbs")
    if failed > 0:
        print(f"Failed: {failed} verbs")
    
    # Verify some results
    print("\nVerifying updates (sample of 5):")
    response = supabase.table('language_vocabulary') \
        .select('word, english_translation') \
        .eq('language', 'es') \
        .eq('part_of_speech', 'verb') \
        .like('english_translation', 'to %') \
        .limit(5) \
        .execute()
    
    for verb in response.data:
        print(f"  {verb['word']}: {verb['english_translation']}")

if __name__ == "__main__":
    main()