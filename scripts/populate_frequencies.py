"""
Populate word frequency data using wordfreq library
This gives us real-world usage frequencies on the Zipf scale (0-8)
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

try:
    from wordfreq import zipf_frequency
except ImportError:
    print("Installing wordfreq...")
    os.system(f"{sys.executable} -m pip install wordfreq")
    from wordfreq import zipf_frequency

try:
    from supabase import create_client, Client
except ImportError:
    print("Installing supabase...")
    os.system(f"{sys.executable} -m pip install supabase")
    from supabase import create_client, Client

def get_supabase_client() -> Client:
    """Create Supabase client"""
    url = os.getenv('REACT_APP_SUPABASE_URL')
    key = os.getenv('REACT_APP_SUPABASE_ANON_KEY')
    
    if not url or not key:
        raise ValueError("Missing Supabase credentials in .env.local")
    
    return create_client(url, key)

def populate_frequencies():
    """Populate frequency field with Zipf frequencies"""
    
    print("=== POPULATING WORD FREQUENCIES ===\n")
    
    # Connect to Supabase
    supabase = get_supabase_client()
    
    # Get all words
    print("Fetching words from database...")
    response = supabase.table('spelling_words').select('id, word').execute()
    words = response.data
    
    print(f"Found {len(words)} words to process\n")
    
    # Process in batches
    batch_size = 100
    updates = []
    
    for i, word_data in enumerate(words):
        word = word_data['word'].lower()
        word_id = word_data['id']
        
        # Get Zipf frequency (0-8 scale)
        # Higher = more common
        # 7-8: Very common (the, be, to)
        # 5-6: Common (house, friend, happy)
        # 3-4: Moderate (peculiar, monastery)
        # 1-2: Rare (sesquipedalian, perspicacious)
        # 0-1: Very rare or not found
        
        freq = zipf_frequency(word, 'en')
        
        updates.append({
            'id': word_id,
            'frequency': freq
        })
        
        # Update in batches
        if len(updates) >= batch_size or i == len(words) - 1:
            try:
                # Update the database
                for update in updates:
                    supabase.table('spelling_words').update({
                        'frequency': update['frequency']
                    }).eq('id', update['id']).execute()
                
                print(f"Updated {i+1}/{len(words)} words...")
                updates = []
                
            except Exception as e:
                print(f"Error updating batch: {e}")
                # Continue with next batch
                updates = []
    
    print("\n✓ Frequency population complete!")
    
    # Show distribution
    print("\n=== FREQUENCY DISTRIBUTION ===")
    
    # Get updated data to verify
    response = supabase.table('spelling_words').select('frequency').execute()
    frequencies = [w['frequency'] for w in response.data if w['frequency'] is not None]
    
    if frequencies:
        import statistics
        
        print(f"Total words with frequency: {len(frequencies)}")
        print(f"Average Zipf frequency: {statistics.mean(frequencies):.2f}")
        print(f"Median: {statistics.median(frequencies):.2f}")
        print(f"Min: {min(frequencies):.2f}, Max: {max(frequencies):.2f}")
        
        # Show distribution by ranges
        ranges = {
            '0-2 (Very rare)': sum(1 for f in frequencies if f < 2),
            '2-3 (Rare)': sum(1 for f in frequencies if 2 <= f < 3),
            '3-4 (Uncommon)': sum(1 for f in frequencies if 3 <= f < 4),
            '4-5 (Moderate)': sum(1 for f in frequencies if 4 <= f < 5),
            '5-6 (Common)': sum(1 for f in frequencies if 5 <= f < 6),
            '6-7 (Very common)': sum(1 for f in frequencies if 6 <= f < 7),
            '7-8 (Extremely common)': sum(1 for f in frequencies if f >= 7)
        }
        
        print("\nDistribution by frequency range:")
        for range_name, count in ranges.items():
            pct = (count / len(frequencies)) * 100
            print(f"  {range_name}: {count} words ({pct:.1f}%)")

if __name__ == "__main__":
    populate_frequencies()