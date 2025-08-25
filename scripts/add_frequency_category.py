"""
Add frequency_category field to spelling_words table based on Zipf frequency bands
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

try:
    from supabase import create_client
except ImportError:
    print("Installing supabase...")
    os.system(f"{sys.executable} -m pip install supabase")
    from supabase import create_client

def get_supabase_client():
    """Create Supabase client"""
    url = os.getenv('REACT_APP_SUPABASE_URL')
    key = os.getenv('REACT_APP_SUPABASE_ANON_KEY')
    return create_client(url, key)

def categorize_frequency(freq):
    """
    Categorize Zipf frequency into meaningful bands
    
    Zipf scale: 0-8 where higher = more common
    7-8: Extremely common (the, be, to) - almost never in spelling bees
    6-7: Very common (have, make, time)
    5-6: Common (house, friend, happy)
    4-5: Moderate (special, important, garden)
    3-4: Uncommon (peculiar, monastery, gymnasium)
    2-3: Rare (perspicacious, ubiquitous)
    0-2: Very rare (sesquipedalian, antidisestablishmentarianism)
    """
    if freq is None:
        return None
    elif freq >= 7:
        return 'extremely_common'
    elif freq >= 6:
        return 'very_common'
    elif freq >= 5:
        return 'common'
    elif freq >= 4:
        return 'moderate'
    elif freq >= 3:
        return 'uncommon'
    elif freq >= 2:
        return 'rare'
    else:
        return 'very_rare'

def generate_add_column_sql():
    """Generate SQL to add frequency_category column"""
    
    sql = """-- Add frequency_category field to spelling_words table
-- This categorizes the Zipf frequency (0-8 scale) into meaningful bands

-- First, create backup
CREATE TABLE IF NOT EXISTS spelling_words_bkp_freq_category AS 
SELECT * FROM spelling_words;

-- Add the new column
ALTER TABLE spelling_words 
ADD COLUMN IF NOT EXISTS frequency_category VARCHAR(20);

-- Add comment to document the field
COMMENT ON COLUMN spelling_words.frequency_category IS 
'Word frequency category based on Zipf scale: extremely_common (7+), very_common (6-7), common (5-6), moderate (4-5), uncommon (3-4), rare (2-3), very_rare (0-2)';

"""
    return sql

def generate_update_sql():
    """Generate SQL to update frequency_category based on frequency values"""
    
    print("=== GENERATING FREQUENCY CATEGORY UPDATES ===\n")
    
    supabase = get_supabase_client()
    
    # Get all words with frequency data
    print("Fetching words with frequency data...")
    response = supabase.table('spelling_words').select('id, word, frequency').execute()
    words = response.data
    
    print(f"Processing {len(words)} words...\n")
    
    # Categorize and group by category
    categories = {}
    stats = {
        'extremely_common': 0,
        'very_common': 0,
        'common': 0,
        'moderate': 0,
        'uncommon': 0,
        'rare': 0,
        'very_rare': 0,
        'null': 0
    }
    
    for word_data in words:
        freq = word_data.get('frequency')
        category = categorize_frequency(freq)
        
        if category:
            if category not in categories:
                categories[category] = []
            categories[category].append(word_data['id'])
            stats[category] += 1
        else:
            stats['null'] += 1
    
    # Generate SQL updates
    sql = "\n-- Update frequency_category based on Zipf frequency bands\n"
    
    for category in ['extremely_common', 'very_common', 'common', 'moderate', 'uncommon', 'rare', 'very_rare']:
        if category in categories:
            ids = categories[category]
            # Split into batches of 500 for efficiency
            for i in range(0, len(ids), 500):
                batch = ids[i:i+500]
                id_list = "'" + "','".join(batch) + "'"
                sql += f"\nUPDATE spelling_words SET frequency_category = '{category}' WHERE id IN ({id_list});\n"
    
    # Show statistics
    print("=== FREQUENCY CATEGORY DISTRIBUTION ===\n")
    print(f"{'Category':<20} {'Count':>8} {'Percentage':>10}")
    print("-" * 40)
    
    total = len(words)
    for category in ['extremely_common', 'very_common', 'common', 'moderate', 'uncommon', 'rare', 'very_rare']:
        count = stats[category]
        pct = (count / total * 100) if total > 0 else 0
        print(f"{category:<20} {count:>8} {pct:>9.1f}%")
    
    if stats['null'] > 0:
        pct = (stats['null'] / total * 100)
        print(f"{'NULL frequency':<20} {stats['null']:>8} {pct:>9.1f}%")
    
    print("\n" + "=" * 40)
    print(f"Total words: {total}")
    
    # Add example words for each category
    print("\n=== EXAMPLE WORDS BY CATEGORY ===\n")
    
    # Get some example words for each category
    for category in ['extremely_common', 'very_common', 'common', 'moderate', 'uncommon', 'rare', 'very_rare']:
        if category in categories and len(categories[category]) > 0:
            # Get first 5 word IDs for this category
            example_ids = categories[category][:5]
            examples = []
            for word_data in words:
                if word_data['id'] in example_ids:
                    examples.append(f"{word_data['word']} ({word_data['frequency']:.1f})")
            
            if examples:
                print(f"{category}: {', '.join(examples)}")
    
    return sql

def main():
    """Main function"""
    
    # Generate SQL to add column
    add_column_sql = generate_add_column_sql()
    
    # Generate SQL to update categories
    update_sql = generate_update_sql()
    
    # Combine and save
    full_sql = add_column_sql + update_sql
    
    output_file = 'add_frequency_category.sql'
    with open(output_file, 'w') as f:
        f.write(full_sql)
    
    print(f"\nSQL saved to {output_file}")
    print("\nTo apply these changes to the database:")
    print(f"1. Review the SQL file: {output_file}")
    print("2. Execute the SQL in your database")
    print("\nThe frequency_category field will help with:")
    print("- Better understanding of word commonality")
    print("- Filtering words by usage frequency")
    print("- Adaptive difficulty algorithms")
    print("- Curriculum planning by frequency bands")

if __name__ == "__main__":
    main()