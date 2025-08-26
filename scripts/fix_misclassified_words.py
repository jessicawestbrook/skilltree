"""
Fix misclassified Spanish words
Remove articles from verbs and reclassify them correctly
"""

import os
from dotenv import load_dotenv
load_dotenv('.env.local')

from supabase import create_client

SUPABASE_URL = os.getenv('REACT_APP_SUPABASE_URL')
SUPABASE_KEY = os.getenv('REACT_APP_SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Fixing misclassified Spanish words")
print("="*60)

# Common Spanish verb forms that shouldn't be nouns
VERB_INDICATORS = {
    # Conjugated forms
    'hago', 'haces', 'hace', 'hacemos', 'hacen', 'hacía', 'hizo', 'haré', 'haría',
    'voy', 'vas', 'va', 'vamos', 'van', 'iba', 'fue', 'iré', 'iría',
    'tengo', 'tienes', 'tiene', 'tenemos', 'tienen', 'tenía', 'tuvo', 'tendré',
    'estoy', 'estás', 'está', 'estamos', 'están', 'estaba', 'estuvo', 'estaré',
    'digo', 'dices', 'dice', 'decimos', 'dicen', 'decía', 'dijo', 'diré',
    'puedo', 'puedes', 'puede', 'podemos', 'pueden', 'podía', 'pudo', 'podré',
    'quiero', 'quieres', 'quiere', 'queremos', 'quieren', 'quería', 'quiso',
    'soy', 'eres', 'es', 'somos', 'son', 'era', 'fue', 'seré', 'sería',
    # Subjunctive forms
    'haga', 'hagas', 'hagamos', 'hagan', 'hiciera', 'hiciese',
    'vaya', 'vayas', 'vayamos', 'vayan', 'fuera', 'fuese',
    'tenga', 'tengas', 'tengamos', 'tengan', 'tuviera', 'tuviese',
    # Gerunds
    'haciendo', 'yendo', 'teniendo', 'estando', 'diciendo', 'pudiendo',
    'queriendo', 'siendo', 'viendo', 'dando', 'viniendo', 'subiendo',
    # Past participles
    'hecho', 'ido', 'tenido', 'estado', 'dicho', 'podido', 'querido',
    'sido', 'visto', 'dado', 'venido', 'levantado',
    # Infinitives with pronouns
    'hacerlo', 'hacerla', 'hacerle', 'hacerme', 'hacerte', 'hacernos',
    'irme', 'irte', 'irse', 'irnos', 'iros',
    'verlo', 'verla', 'verle', 'verme', 'verte',
}

# Words that are often pronouns/adverbs, not nouns
NON_NOUNS = {
    'como', 'cómo',  # how/as
    'entonces',  # then
    'nosotros', 'vosotros', 'ellos', 'ellas',  # pronouns
    'ahora', 'después', 'antes', 'siempre', 'nunca',  # adverbs
    'aquí', 'allí', 'ahí', 'acá', 'allá',  # adverbs of place
    'así', 'asique',  # thus/so
}

# Step 1: Find misclassified words
print("\n1. Finding misclassified words...")

# Get all Spanish "nouns" with articles
response = supabase.table('language_vocabulary') \
    .select('id, word, english_translation, part_of_speech') \
    .eq('language', 'es') \
    .eq('part_of_speech', 'noun') \
    .or_('word.like.el %,word.like.la %,word.like.los %,word.like.las %') \
    .execute()

all_nouns_with_articles = response.data
print(f"   Total nouns with articles: {len(all_nouns_with_articles):,}")

to_fix_as_verb = []
to_fix_as_other = []
suspicious_nouns = []

for record in all_nouns_with_articles:
    word = record['word']
    translation = record.get('english_translation', '').lower()
    
    # Remove article to check the base word
    base_word = word
    for article in ['el ', 'la ', 'los ', 'las ']:
        if word.startswith(article):
            base_word = word[len(article):]
            break
    
    # Check if it's a verb form
    if base_word in VERB_INDICATORS:
        to_fix_as_verb.append(record)
    # Check if it's clearly not a noun
    elif base_word in NON_NOUNS:
        to_fix_as_other.append(record)
    # Check if translation suggests it's not a noun
    elif translation in ['do', 'go', 'up', 'down', 'as', 'so', 'if', 'but', 'and', 'or', 
                         'us', 'them', 'me', 'you', 'he', 'she', 'it', 'we', 'they']:
        suspicious_nouns.append(record)
    # Check for infinitives (ending in -ar, -er, -ir, or with pronouns)
    elif base_word.endswith(('ar', 'er', 'ir')) or \
         base_word.endswith(('arme', 'arte', 'arse', 'arnos', 'aros',
                            'erme', 'erte', 'erse', 'ernos', 'eros',
                            'irme', 'irte', 'irse', 'irnos', 'iros',
                            'arlo', 'arla', 'arle', 'arlos', 'arlas', 'arles',
                            'erlo', 'erla', 'erle', 'erlos', 'erlas', 'erles',
                            'irlo', 'irla', 'irle', 'irlos', 'irlas', 'irles')):
        # Check if it's really a verb by looking at the translation
        if translation.startswith('to ') or translation in ['do', 'go', 'make', 'take', 'give', 'say', 'see']:
            to_fix_as_verb.append(record)

print(f"   Found {len(to_fix_as_verb)} verbs misclassified as nouns")
print(f"   Found {len(to_fix_as_other)} other words misclassified as nouns")
print(f"   Found {len(suspicious_nouns)} suspicious nouns")

# Step 2: Fix misclassified verbs
if to_fix_as_verb:
    print("\n2. Fixing misclassified verbs...")
    print("   Examples to fix:")
    for r in to_fix_as_verb[:10]:
        print(f"     {r['word']:30} -> {r['english_translation']}")
    
    # Auto-fix without prompting
    print("\n   Auto-fixing these verbs...")
    if True:
        fixed = 0
        for record in to_fix_as_verb:
            word = record['word']
            # Remove article
            clean_word = word
            for article in ['el ', 'la ', 'los ', 'las ']:
                if word.startswith(article):
                    clean_word = word[len(article):]
                    break
            
            try:
                # Update: remove article and change part of speech
                supabase.table('language_vocabulary') \
                    .update({
                        'word': clean_word,
                        'part_of_speech': 'verb'
                    }) \
                    .eq('id', record['id']) \
                    .execute()
                fixed += 1
            except Exception as e:
                print(f"     Error fixing {word}: {e}")
        
        print(f"   Fixed {fixed} verbs")

# Step 3: Show suspicious nouns for manual review
if suspicious_nouns:
    print("\n3. Suspicious nouns (need manual review):")
    print("   These have translations that suggest they're not nouns:")
    for r in suspicious_nouns[:20]:
        print(f"     {r['word']:30} -> {r['english_translation']:15}")
    print(f"   Total suspicious: {len(suspicious_nouns)}")

# Final summary
print("\n" + "="*60)
print("Summary:")
print(f"  Verbs to fix: {len(to_fix_as_verb)}")
print(f"  Other words to fix: {len(to_fix_as_other)}")
print(f"  Suspicious nouns: {len(suspicious_nouns)}")

# Check final status
response = supabase.table('language_vocabulary') \
    .select('count', count='exact') \
    .eq('language', 'es') \
    .eq('part_of_speech', 'noun') \
    .execute()

print(f"\nTotal Spanish nouns remaining: {response.count:,}")