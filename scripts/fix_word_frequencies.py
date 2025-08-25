"""
Fix word frequency data using wordfreq library
The current data appears to be all 1s instead of actual Zipf frequencies
"""

import os
import sys
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

def fix_frequencies():
    """Fix frequency field with correct Zipf frequencies"""
    
    print("=== FIXING WORD FREQUENCIES ===\n")
    
    # Connect to Supabase
    supabase = get_supabase_client()
    
    # Get all words
    print("Fetching all words from database...")
    response = supabase.table('spelling_words').select('id, word').execute()
    words = response.data
    
    print(f"Found {len(words)} words to update\n")
    
    # First, let's verify the problem with a sample
    print("Checking sample words to verify the issue:")
    sample_words = ['economy', 'enjoy', 'set', 'happy', 'peculiar']
    for word in sample_words[:5]:
        word_data = next((w for w in words if w['word'] == word), None)
        if word_data:
            correct_freq = zipf_frequency(word, 'en')
            print(f"  {word}: should be {correct_freq:.2f}")
    
    print("\nUpdating frequencies...")
    
    # Process in batches
    batch_size = 100
    updates = []
    
    for i, word_data in enumerate(words):
        word = word_data['word'].lower()
        word_id = word_data['id']
        
        # Get correct Zipf frequency (0-8 scale)
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
                
                if (i + 1) % 1000 == 0:
                    print(f"  Updated {i+1}/{len(words)} words...")
                updates = []
                
            except Exception as e:
                print(f"Error updating batch: {e}")
                updates = []
    
    print(f"\n✓ Updated {len(words)} words with correct frequencies!")
    
    # Verify the fix
    print("\n=== VERIFICATION ===")
    
    # Get updated data for sample words
    response = supabase.table('spelling_words').select('word, frequency').in_('word', sample_words).execute()
    
    print("\nSample words after update:")
    for word_data in response.data:
        word = word_data['word']
        db_freq = word_data['frequency']
        expected_freq = zipf_frequency(word, 'en')
        status = "✓" if abs(db_freq - expected_freq) < 0.01 else "✗"
        print(f"  {word}: {db_freq:.2f} (expected: {expected_freq:.2f}) {status}")
    
    # Show distribution
    print("\n=== FREQUENCY DISTRIBUTION ===")
    
    response = supabase.table('spelling_words').select('frequency').execute()
    frequencies = [w['frequency'] for w in response.data if w['frequency'] is not None]
    
    if frequencies:
        import statistics
        
        # Calculate distribution
        ranges = {
            '7-8 (Extremely common)': sum(1 for f in frequencies if f >= 7),
            '6-7 (Very common)': sum(1 for f in frequencies if 6 <= f < 7),
            '5-6 (Common)': sum(1 for f in frequencies if 5 <= f < 6),
            '4-5 (Moderate)': sum(1 for f in frequencies if 4 <= f < 5),
            '3-4 (Uncommon)': sum(1 for f in frequencies if 3 <= f < 4),
            '2-3 (Rare)': sum(1 for f in frequencies if 2 <= f < 3),
            '0-2 (Very rare)': sum(1 for f in frequencies if f < 2)
        }
        
        total = len(frequencies)
        for range_name, count in ranges.items():
            pct = (count / total * 100) if total > 0 else 0
            print(f"  {range_name}: {count} words ({pct:.1f}%)")
        
        print(f"\nTotal words with frequency: {total}")
        print(f"Average frequency: {statistics.mean(frequencies):.2f}")
        print(f"Median: {statistics.median(frequencies):.2f}")
        print(f"Min: {min(frequencies):.2f}, Max: {max(frequencies):.2f}")

if __name__ == "__main__":
    fix_frequencies()