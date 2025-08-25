"""
Calculate correct Zipf frequencies for all words and generate SQL updates
"""

import json
from wordfreq import zipf_frequency

print("=== CALCULATING CORRECT FREQUENCIES FOR ALL WORDS ===\n")

# Load all words
with open('all_words.json', 'r') as f:
    words_data = json.load(f)

print(f"Processing {len(words_data)} words...")

# Calculate frequencies and group by frequency for efficient SQL
updates = []
frequency_groups = {}

for i, word_data in enumerate(words_data):
    word = word_data['word'].lower()
    word_id = word_data['id']
    
    # Get correct Zipf frequency
    freq = zipf_frequency(word, 'en')
    
    # Round to 2 decimal places for grouping
    freq_rounded = round(freq, 2)
    
    if freq_rounded not in frequency_groups:
        frequency_groups[freq_rounded] = []
    frequency_groups[freq_rounded].append(word_id)
    
    if (i + 1) % 1000 == 0:
        print(f"  Processed {i + 1}/{len(words_data)} words...")

print(f"\nFound {len(frequency_groups)} distinct frequency values")

# Generate SQL
print("\nGenerating SQL file...")

sql = """-- Update all word frequencies with correct Zipf values from wordfreq
-- Generated from wordfreq library

-- Create backup first
CREATE TABLE IF NOT EXISTS spelling_words_bkp_freq_correct AS 
SELECT * FROM spelling_words;

-- Update frequencies in batches by frequency value
"""

# Generate UPDATE statements grouped by frequency value
for freq_value in sorted(frequency_groups.keys(), reverse=True):
    ids = frequency_groups[freq_value]
    
    # Split into batches of 500 IDs for SQL efficiency
    for i in range(0, len(ids), 500):
        batch = ids[i:i+500]
        id_list = "'" + "','".join(batch) + "'"
        sql += f"\nUPDATE spelling_words SET frequency = {freq_value} WHERE id IN ({id_list});\n"

# Add verification queries
sql += """
-- Verify the update
SELECT 
    'Frequency Distribution After Update' as analysis,
    COUNT(*) as total_words,
    ROUND(AVG(frequency)::numeric, 2) as avg_frequency,
    MIN(frequency) as min_frequency,
    MAX(frequency) as max_frequency
FROM spelling_words;

-- Show distribution by frequency bands
SELECT 
    CASE 
        WHEN frequency >= 7 THEN '7-8: Extremely common'
        WHEN frequency >= 6 THEN '6-7: Very common'  
        WHEN frequency >= 5 THEN '5-6: Common'
        WHEN frequency >= 4 THEN '4-5: Moderate'
        WHEN frequency >= 3 THEN '3-4: Uncommon'
        WHEN frequency >= 2 THEN '2-3: Rare'
        WHEN frequency >= 0 THEN '0-2: Very rare'
        ELSE 'NULL'
    END as frequency_band,
    COUNT(*) as word_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM spelling_words), 1) as percentage
FROM spelling_words
GROUP BY 
    CASE 
        WHEN frequency >= 7 THEN '7-8: Extremely common'
        WHEN frequency >= 6 THEN '6-7: Very common'  
        WHEN frequency >= 5 THEN '5-6: Common'
        WHEN frequency >= 4 THEN '4-5: Moderate'
        WHEN frequency >= 3 THEN '3-4: Uncommon'
        WHEN frequency >= 2 THEN '2-3: Rare'
        WHEN frequency >= 0 THEN '0-2: Very rare'
        ELSE 'NULL'
    END
ORDER BY MIN(frequency) DESC;

-- Check specific words that should have different frequencies
SELECT word, frequency 
FROM spelling_words 
WHERE word IN ('the', 'economy', 'enjoy', 'set', 'happy', 'peculiar', 'sesquipedalian')
ORDER BY frequency DESC;
"""

# Save SQL file
with open('update_all_frequencies.sql', 'w') as f:
    f.write(sql)

print("SQL saved to update_all_frequencies.sql")

# Show statistics
print("\n=== FREQUENCY STATISTICS ===")

# Calculate distribution
all_frequencies = []
for freq, ids in frequency_groups.items():
    all_frequencies.extend([freq] * len(ids))

ranges = {
    '7-8 (Extremely common)': sum(1 for f in all_frequencies if f >= 7),
    '6-7 (Very common)': sum(1 for f in all_frequencies if 6 <= f < 7),
    '5-6 (Common)': sum(1 for f in all_frequencies if 5 <= f < 6),
    '4-5 (Moderate)': sum(1 for f in all_frequencies if 4 <= f < 5),
    '3-4 (Uncommon)': sum(1 for f in all_frequencies if 3 <= f < 4),
    '2-3 (Rare)': sum(1 for f in all_frequencies if 2 <= f < 3),
    '0-2 (Very rare)': sum(1 for f in all_frequencies if f < 2)
}

total = len(all_frequencies)
print("\nExpected distribution after update:")
for range_name, count in ranges.items():
    pct = (count / total * 100) if total > 0 else 0
    print(f"  {range_name}: {count} words ({pct:.1f}%)")

import statistics
print(f"\nTotal words: {total}")
print(f"Average frequency: {statistics.mean(all_frequencies):.2f}")
print(f"Median: {statistics.median(all_frequencies):.2f}")
print(f"Min: {min(all_frequencies):.2f}, Max: {max(all_frequencies):.2f}")

# Show some sample words and their correct frequencies
print("\n=== SAMPLE WORD CORRECTIONS ===")
samples = ['economy', 'enjoy', 'set', 'happy', 'peculiar', 'monastery', 'perspicacious']
for word in samples:
    word_item = next((w for w in words_data if w['word'].lower() == word.lower()), None)
    if word_item:
        freq = zipf_frequency(word, 'en')
        print(f"  {word}: will be updated to {freq:.2f}")

print(f"\nSQL file size: {len(sql) / 1024 / 1024:.1f} MB")