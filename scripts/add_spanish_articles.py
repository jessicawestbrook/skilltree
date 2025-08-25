"""
Add Spanish articles to nouns using linguistic rules and patterns
While not 100% accurate, this covers most common cases
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

def get_article(word, part_of_speech='noun'):
    """
    Determine the appropriate Spanish article for a word
    Returns: (article, gender) tuple
    """
    word_lower = word.lower()
    
    # Skip if not a noun
    if part_of_speech not in ['noun', 'n', '']:
        return ('', '')
    
    # Check irregular gender dictionary first
    if word_lower in IRREGULAR_GENDER:
        gender = IRREGULAR_GENDER[word_lower]
        if gender == 'm':
            return ('el', 'm')
        elif gender == 'f':
            return ('la', 'f')
        elif gender == 'f-el':  # Feminine but uses 'el'
            return ('el', 'f')
        elif gender == 'm/f':  # Can be either
            return ('el/la', 'm/f')
    
    # Apply standard rules
    
    # Feminine endings (very reliable)
    if word_lower.endswith(('ción', 'sión', 'dad', 'tad', 'tud', 'umbre', 
                           'ez', 'eza', 'ncia', 'anza', 'icia', 'icie')):
        return ('la', 'f')
    
    # Masculine endings (very reliable)
    if word_lower.endswith(('aje', 'or', 'án', 'ambre', 'ema', 'oma', 
                           'ismo', 'ista', 'nte')):
        # Note: -ista and -nte can be both, but default to masculine
        return ('el', 'm')
    
    # Words ending in -ma (often from Greek, usually masculine)
    if word_lower.endswith('ma') and len(word_lower) > 4:
        return ('el', 'm')
    
    # Standard -o/-a endings
    if word_lower.endswith('o'):
        return ('el', 'm')
    if word_lower.endswith('a'):
        return ('la', 'f')
    
    # Words ending in -e (less predictable, default to masculine)
    if word_lower.endswith('e'):
        # Some common feminine -e endings
        if word_lower.endswith(('umbre', 'ie', 'ente')):
            return ('la', 'f')
        return ('el', 'm')  # Default for -e
    
    # Words ending in consonants (usually masculine)
    if word_lower[-1] in 'lrndzjsxñ':
        # Some exceptions
        if word_lower.endswith(('tud', 'ud')):
            return ('la', 'f')
        return ('el', 'm')
    
    # Default to masculine for unknown patterns
    return ('el', 'm')

def update_spanish_words_with_articles():
    """Update Spanish nouns in database with articles"""
    
    print("Fetching Spanish nouns from database...")
    
    # Get all Spanish nouns that don't already have articles
    response = supabase.table('language_vocabulary') \
        .select('id, word, part_of_speech') \
        .eq('language', 'es') \
        .in_('part_of_speech', ['noun', 'n']) \
        .execute()
    
    # Filter out words that already have articles
    nouns = [r for r in response.data if not r['word'].startswith(('el ', 'la ', 'los ', 'las '))]
    print(f"Found {len(nouns):,} Spanish nouns to process")
    
    if not nouns:
        print("No nouns to process!")
        return
    
    # Process in batches
    batch_size = 100
    updates_made = 0
    examples = []
    
    for i in range(0, len(nouns), batch_size):
        batch = nouns[i:min(i+batch_size, len(nouns))]
        
        for record in batch:
            word = record['word']
            article, gender = get_article(word, record.get('part_of_speech', 'noun'))
            
            if article and '/' not in article:  # Skip ambiguous articles
                # Create word with article
                word_with_article = f"{article} {word}"
                
                try:
                    # Update the word field directly
                    supabase.table('language_vocabulary') \
                        .update({'word': word_with_article}) \
                        .eq('id', record['id']) \
                        .execute()
                    updates_made += 1
                    
                    # Save examples
                    if len(examples) < 20:
                        examples.append((word, word_with_article, gender))
                    
                except Exception as e:
                    print(f"Error updating {word}: {e}")
        
        if updates_made > 0 and updates_made % 500 == 0:
            print(f"  Progress: Updated {updates_made} words...")
    
    print(f"\nCompleted! Added articles to {updates_made:,} Spanish nouns")
    
    # Show examples
    if examples:
        print("\nExample words with articles added:")
        for original, with_article, gender in examples:
            print(f"  {original} → {with_article} ({gender})")

def main():
    print("Adding Spanish articles to nouns")
    print("="*60)
    
    # Update words with articles
    update_spanish_words_with_articles()

if __name__ == "__main__":
    main()