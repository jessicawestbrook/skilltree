"""
Bulk add 'the' to English noun translations
"""

import os
from dotenv import load_dotenv
load_dotenv('.env.local')

from supabase import create_client
import time

SUPABASE_URL = os.getenv('REACT_APP_SUPABASE_URL')
SUPABASE_KEY = os.getenv('REACT_APP_SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Words that shouldn't get 'the' prefix
SKIP_WORDS = {
    # Pronouns
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
    'my', 'your', 'his', 'its', 'our', 'their', 'mine', 'yours', 'hers', 'ours', 'theirs',
    'myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves', 'themselves',
    'this', 'that', 'these', 'those',
    # Question words
    'who', 'what', 'where', 'when', 'why', 'how', 'which', 'whom', 'whose',
    # Common verbs/adverbs that got miscategorized
    'do', 'does', 'did', 'go', 'goes', 'went', 'up', 'down', 'in', 'out', 'on', 'off',
    'be', 'is', 'are', 'was', 'were', 'been', 'being', 'have', 'has', 'had', 'having',
    # Conjunctions/prepositions
    'so', 'as', 'if', 'or', 'and', 'but', 'because', 'since', 'unless', 'although',
    'for', 'with', 'without', 'to', 'from', 'by', 'at', 'of', 'about', 'through',
    # Quantifiers
    'all', 'some', 'any', 'no', 'none', 'much', 'many', 'few', 'little', 'more', 'less',
    'each', 'every', 'either', 'neither', 'both', 'several', 'enough',
    # Others
    'yes', 'no', 'not', 'never', 'always', 'sometimes', 'often', 'usually',
    'very', 'quite', 'rather', 'too', 'also', 'only', 'just', 'even',
    'here', 'there', 'now', 'then', 'today', 'tomorrow', 'yesterday'
}

print("Bulk adding 'the' to English noun translations")
print("="*60)

# Get all nouns without 'the' in one query
response = supabase.table('language_vocabulary') \
    .select('id, word, english_translation') \
    .eq('language', 'es') \
    .eq('part_of_speech', 'noun') \
    .not_.ilike('english_translation', 'the %') \
    .not_.ilike('english_translation', 'a %') \
    .not_.ilike('english_translation', 'an %') \
    .execute()

all_nouns = response.data
print(f"Total nouns to process: {len(all_nouns):,}")

# Process in batches
batch_size = 500
total_updated = 0
total_skipped = 0

for i in range(0, len(all_nouns), batch_size):
    batch = all_nouns[i:min(i+batch_size, len(all_nouns))]
    batch_updates = []
    
    print(f"\nProcessing batch {i//batch_size + 1} ({i+1}-{min(i+batch_size, len(all_nouns))} of {len(all_nouns)})")
    
    for record in batch:
        translation = record.get('english_translation', '').strip()
        
        # Skip empty or very short
        if not translation or len(translation) <= 1:
            total_skipped += 1
            continue
        
        # Skip if in skip list
        if translation.lower() in SKIP_WORDS:
            total_skipped += 1
            continue
        
        # Skip if starts with number or special char
        if translation and not translation[0].isalpha():
            total_skipped += 1
            continue
        
        # Skip URLs or code-like strings
        if any(x in translation for x in ['http', 'www', '.com', '()', '[]', '{}']):
            total_skipped += 1
            continue
        
        # Skip single words that are clearly not nouns (common Spanish words left untranslated)
        spanish_verbs = ['hacer', 'estar', 'tener', 'decir', 'poder', 'querer', 'saber', 'dar', 'ver', 'pasar']
        if translation.lower() in spanish_verbs:
            total_skipped += 1
            continue
        
        # Add to batch updates
        batch_updates.append({
            'id': record['id'],
            'translation': f"the {translation.lower()}"
        })
    
    # Update this batch
    if batch_updates:
        for update in batch_updates:
            try:
                supabase.table('language_vocabulary') \
                    .update({
                        'english_translation': update['translation'],
                        'definition_english': update['translation']
                    }) \
                    .eq('id', update['id']) \
                    .execute()
                total_updated += 1
            except Exception as e:
                print(f"  Error updating: {e}")
                total_skipped += 1
        
        print(f"  Updated {len(batch_updates)} nouns in this batch")
    
    # Small delay between batches
    time.sleep(0.2)

print("\n" + "="*60)
print("COMPLETE")
print(f"Total updated: {total_updated:,}")
print(f"Total skipped: {total_skipped:,}")

# Final count
response = supabase.table('language_vocabulary') \
    .select('count', count='exact') \
    .eq('language', 'es') \
    .eq('part_of_speech', 'noun') \
    .ilike('english_translation', 'the %') \
    .execute()

with_the = response.count

response = supabase.table('language_vocabulary') \
    .select('count', count='exact') \
    .eq('language', 'es') \
    .eq('part_of_speech', 'noun') \
    .execute()

total = response.count

print(f"\nFinal status: {with_the:,} / {total:,} nouns have 'the' ({with_the/total*100:.1f}%)")

# Show examples
response = supabase.table('language_vocabulary') \
    .select('word, english_translation') \
    .eq('language', 'es') \
    .eq('part_of_speech', 'noun') \
    .ilike('english_translation', 'the %') \
    .order('zipf_frequency', desc=True) \
    .limit(15) \
    .execute()

print("\nHigh-frequency examples with 'the':")
for r in response.data[:10]:
    print(f"  {r['word']:30} -> {r['english_translation']}")