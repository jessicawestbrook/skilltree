"""
Enhanced Spanish translation script that adds articles to nouns
Combines translation with article assignment
"""

import os
import sys
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv('.env.local')

# Install required packages if needed
for package in ['supabase', 'deep-translator']:
    try:
        __import__(package.replace('-', '_'))
    except ImportError:
        print(f"Installing {package}...")
        os.system(f"{sys.executable} -m pip install {package}")

from supabase import create_client
from deep_translator import GoogleTranslator

# Initialize Supabase with service role key
SUPABASE_URL = os.getenv('REACT_APP_SUPABASE_URL')
SUPABASE_KEY = os.getenv('REACT_APP_SUPABASE_SERVICE_ROLE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: Missing environment variables")
    sys.exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Common Spanish nouns with known irregular gender
IRREGULAR_GENDER = {
    # Common masculine words ending in -a
    'día': 'm', 'mapa': 'm', 'problema': 'm', 'sistema': 'm', 'tema': 'm',
    'programa': 'm', 'idioma': 'm', 'clima': 'm', 'planeta': 'm', 'poeta': 'm',
    'drama': 'm', 'poema': 'm', 'dilema': 'm', 'esquema': 'm', 'síntoma': 'm',
    
    # Common feminine words ending in -o
    'mano': 'f', 'foto': 'f', 'moto': 'f', 'radio': 'f',
    
    # Feminine words starting with stressed a/ha that use 'el'
    'agua': 'f-el', 'águila': 'f-el', 'alma': 'f-el', 'arma': 'f-el',
    'hacha': 'f-el', 'hambre': 'f-el', 'área': 'f-el', 'aula': 'f-el',
    
    # Other common irregulars
    'arte': 'm/f', 'mar': 'm/f', 'capital': 'f', 'cárcel': 'f', 'clase': 'f',
    'calle': 'f', 'leche': 'f', 'muerte': 'f', 'gente': 'f', 'mente': 'f',
    'fuente': 'f', 'puente': 'm', 'diente': 'm', 'frente': 'f',
    
    # Days of the week (all masculine)
    'lunes': 'm', 'martes': 'm', 'miércoles': 'm', 'jueves': 'm', 
    'viernes': 'm', 'sábado': 'm', 'domingo': 'm',
    
    # Months (all masculine)
    'enero': 'm', 'febrero': 'm', 'marzo': 'm', 'abril': 'm', 'mayo': 'm',
    'junio': 'm', 'julio': 'm', 'agosto': 'm', 'septiembre': 'm',
    'octubre': 'm', 'noviembre': 'm', 'diciembre': 'm',
}

def get_article(word):
    """
    Determine the appropriate Spanish article for a word
    Returns: article string (el/la/los/las)
    """
    word_lower = word.lower()
    
    # Check if plural
    is_plural = False
    singular_form = word_lower
    
    # Common plural endings
    if word_lower.endswith('es'):
        # Words ending in consonant + es
        if len(word_lower) > 3 and word_lower[-3] in 'lrndzjsxñ':
            is_plural = True
            singular_form = word_lower[:-2]
        # Words ending in stressed vowel + es (cafés, sofás)
        elif len(word_lower) > 3 and word_lower[-3] in 'áéíóú':
            is_plural = True
            singular_form = word_lower[:-2]
    elif word_lower.endswith('s') and len(word_lower) > 2:
        # Words ending in vowel + s
        if word_lower[-2] in 'aeiou':
            is_plural = True
            singular_form = word_lower[:-1]
    
    # Check irregular gender dictionary first (using singular form)
    if singular_form in IRREGULAR_GENDER:
        gender = IRREGULAR_GENDER[singular_form]
        if gender == 'm':
            return 'los' if is_plural else 'el'
        elif gender == 'f':
            return 'las' if is_plural else 'la'
        elif gender == 'f-el':  # Feminine but uses 'el'
            return 'las' if is_plural else 'el'
        elif gender == 'm/f':  # Can be either
            return 'los' if is_plural else 'el'  # Default to masculine
    
    # Apply standard rules (using singular form for gender detection)
    
    # Feminine endings (very reliable)
    if singular_form.endswith(('ción', 'sión', 'dad', 'tad', 'tud', 'umbre', 
                           'ez', 'eza', 'ncia', 'anza', 'icia', 'icie')):
        return 'las' if is_plural else 'la'
    
    # Masculine endings (very reliable)
    if singular_form.endswith(('aje', 'or', 'án', 'ambre', 'ema', 'oma', 
                           'ismo', 'ista', 'nte')):
        # Note: -ista and -nte can be both, but default to masculine
        return 'los' if is_plural else 'el'
    
    # Words ending in -ma (often from Greek, usually masculine)
    if singular_form.endswith('ma') and len(singular_form) > 4:
        return 'los' if is_plural else 'el'
    
    # Standard -o/-a endings (check singular form)
    if singular_form.endswith('o'):
        return 'los' if is_plural else 'el'
    if singular_form.endswith('a'):
        return 'las' if is_plural else 'la'
    
    # Words ending in -e (less predictable, default to masculine)
    if singular_form.endswith('e'):
        # Some common feminine -e endings
        if singular_form.endswith(('umbre', 'ie', 'ente')):
            return 'las' if is_plural else 'la'
        return 'los' if is_plural else 'el'  # Default for -e
    
    # Words ending in consonants (usually masculine)
    if singular_form[-1] in 'lrndzjsxñ':
        # Some exceptions
        if singular_form.endswith(('tud', 'ud')):
            return 'las' if is_plural else 'la'
        return 'los' if is_plural else 'el'
    
    # Default to masculine for unknown patterns
    return 'los' if is_plural else 'el'

def clean_word_for_translation(word):
    """Remove articles and clean word for translation"""
    prefixes = ['el ', 'la ', 'los ', 'las ', 'un ', 'una ', 'unos ', 'unas ']
    cleaned = word
    for prefix in prefixes:
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):]
            break
    return cleaned

def main():
    print("Translating Spanish words and adding articles to nouns")
    print("="*60)
    
    # Get count of pending words
    response = supabase.table('language_vocabulary') \
        .select('count', count='exact') \
        .eq('language', 'es') \
        .eq('translation_source', 'PENDING') \
        .execute()
    
    total_pending = response.count
    print(f"Total words needing translation: {total_pending:,}")
    
    # Also check for nouns without articles
    response = supabase.table('language_vocabulary') \
        .select('count', count='exact') \
        .eq('language', 'es') \
        .eq('part_of_speech', 'noun') \
        .not_.ilike('word', 'el %') \
        .not_.ilike('word', 'la %') \
        .not_.ilike('word', 'los %') \
        .not_.ilike('word', 'las %') \
        .execute()
    
    nouns_without_articles = response.count
    print(f"Nouns without articles: {nouns_without_articles:,}")
    
    if total_pending == 0 and nouns_without_articles == 0:
        print("No words need translation or article updates!")
        return
    
    # Process pending translations first
    if total_pending > 0:
        print("\n--- Processing translations ---")
        response = supabase.table('language_vocabulary') \
            .select('id, word, part_of_speech, zipf_frequency') \
            .eq('language', 'es') \
            .eq('translation_source', 'PENDING') \
            .order('zipf_frequency', desc=True) \
            .limit(100) \
            .execute()
        
        words_to_translate = response.data
        print(f"Processing batch of {len(words_to_translate)} words...")
        
        translator = GoogleTranslator(source='es', target='en')
        successful = 0
        
        for i, record in enumerate(words_to_translate):
            word = record['word']
            cleaned = clean_word_for_translation(word)
            
            if (i + 1) % 10 == 0:
                print(f"  Progress: {i + 1}/{len(words_to_translate)}")
            
            try:
                time.sleep(0.05)  # Rate limiting
                
                # Translate
                translation = translator.translate(cleaned)
                
                # For verbs, add "to" if needed
                if translation and record.get('part_of_speech') == 'verb':
                    if not translation.lower().startswith('to '):
                        conjugated_starts = ['i ', 'you ', 'he ', 'she ', 'it ', 'we ', 'they ']
                        if not any(translation.lower().startswith(p) for p in conjugated_starts):
                            translation = f"to {translation}"
                
                # For nouns, add article if not present
                updated_word = word
                if record.get('part_of_speech') == 'noun':
                    if not any(word.startswith(p) for p in ['el ', 'la ', 'los ', 'las ']):
                        article = get_article(cleaned)
                        updated_word = f"{article} {cleaned}"
                        print(f"    Added article: {cleaned} -> {updated_word}")
                
                # Update database
                if translation:
                    update_data = {
                        'english_translation': translation,
                        'definition_english': translation,
                        'translation_source': 'GoogleTranslator',
                        'definition_source': 'GoogleTranslator'
                    }
                    
                    # Update word with article if changed
                    if updated_word != word:
                        update_data['word'] = updated_word
                    
                    supabase.table('language_vocabulary') \
                        .update(update_data) \
                        .eq('id', record['id']) \
                        .execute()
                    
                    successful += 1
                    
            except Exception as e:
                print(f"  Error processing '{word}': {e}")
                if 'Too Many Requests' in str(e):
                    print("  Rate limit hit, waiting 30 seconds...")
                    time.sleep(30)
        
        print(f"\nTranslated {successful} words")
    
    # Now process nouns that need articles
    if nouns_without_articles > 0:
        print("\n--- Adding articles to nouns ---")
        response = supabase.table('language_vocabulary') \
            .select('id, word, part_of_speech') \
            .eq('language', 'es') \
            .eq('part_of_speech', 'noun') \
            .not_.ilike('word', 'el %') \
            .not_.ilike('word', 'la %') \
            .not_.ilike('word', 'los %') \
            .not_.ilike('word', 'las %') \
            .limit(2000) \
            .execute()
        
        nouns_to_update = response.data
        print(f"Processing {len(nouns_to_update)} nouns...")
        
        updated = 0
        examples = []
        
        for record in nouns_to_update:
            word = record['word']
            article = get_article(word)
            updated_word = f"{article} {word}"
            
            try:
                supabase.table('language_vocabulary') \
                    .update({'word': updated_word}) \
                    .eq('id', record['id']) \
                    .execute()
                
                updated += 1
                if len(examples) < 10:
                    examples.append(f"{word} -> {updated_word}")
                    
            except Exception as e:
                print(f"  Error updating '{word}': {e}")
        
        print(f"\nUpdated {updated} nouns with articles")
        if examples:
            print("\nExamples:")
            for ex in examples:
                print(f"  {ex}")
    
    # Final status
    print("\n" + "="*60)
    print("COMPLETE")
    
    # Check remaining work
    response = supabase.table('language_vocabulary') \
        .select('count', count='exact') \
        .eq('language', 'es') \
        .eq('translation_source', 'PENDING') \
        .execute()
    print(f"Remaining words to translate: {response.count:,}")
    
    response = supabase.table('language_vocabulary') \
        .select('count', count='exact') \
        .eq('language', 'es') \
        .eq('part_of_speech', 'noun') \
        .not_.ilike('word', 'el %') \
        .not_.ilike('word', 'la %') \
        .execute()
    print(f"Remaining nouns without articles: {response.count:,}")

if __name__ == "__main__":
    main()