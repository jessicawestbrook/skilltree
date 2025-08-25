"""
Analyze Spanish words in wordfreq library
"""

import wordfreq
from wordfreq import zipf_frequency, available_languages

print("\nSPANISH WORDFREQ STATISTICS")
print("=" * 60)

# Check if Spanish is available
if 'es' not in available_languages():
    print("Spanish not available in wordfreq")
    exit(1)

print("Counting Spanish words by frequency...")
print("(This may take a minute...)\n")

# Count by frequency bins
frequency_bins = {
    'Very Common (6+)': 0,
    'Common (5-6)': 0,
    'Moderate (4-5)': 0,
    'Uncommon (3-4)': 0,
    'Rare (2-3)': 0,
    'Very Rare (1-2)': 0,
    'Extremely Rare (<1)': 0
}

# Sample words for each category
samples = {
    'Very Common (6+)': [],
    'Common (5-6)': [],
    'Moderate (4-5)': [],
    'Uncommon (3-4)': [],
    'Rare (2-3)': [],
    'Very Rare (1-2)': []
}

total = 0
for word in wordfreq.iter_wordlist('es'):
    total += 1
    freq = zipf_frequency(word, 'es')
    
    # Categorize
    if freq >= 6:
        frequency_bins['Very Common (6+)'] += 1
        if len(samples['Very Common (6+)']) < 5:
            samples['Very Common (6+)'].append(word)
    elif freq >= 5:
        frequency_bins['Common (5-6)'] += 1
        if len(samples['Common (5-6)']) < 5:
            samples['Common (5-6)'].append(word)
    elif freq >= 4:
        frequency_bins['Moderate (4-5)'] += 1
        if len(samples['Moderate (4-5)']) < 5:
            samples['Moderate (4-5)'].append(word)
    elif freq >= 3:
        frequency_bins['Uncommon (3-4)'] += 1
        if len(samples['Uncommon (3-4)']) < 5:
            samples['Uncommon (3-4)'].append(word)
    elif freq >= 2:
        frequency_bins['Rare (2-3)'] += 1
        if len(samples['Rare (2-3)']) < 5:
            samples['Rare (2-3)'].append(word)
    elif freq >= 1:
        frequency_bins['Very Rare (1-2)'] += 1
        if len(samples['Very Rare (1-2)']) < 5:
            samples['Very Rare (1-2)'].append(word)
    else:
        frequency_bins['Extremely Rare (<1)'] += 1
    
    if total % 50000 == 0:
        print(f"  Processed {total:,} words...")

print(f"\nTOTAL SPANISH WORDS: {total:,}")
print("=" * 60)

print("\nFrequency Distribution:")
print("-" * 40)
for category, count in frequency_bins.items():
    percent = (count/total*100) if total > 0 else 0
    print(f"{category:20} {count:8,} ({percent:5.1f}%)")

print("\n" + "=" * 60)
print("Sample words by frequency:")
print("-" * 40)
for category, words in samples.items():
    if words:
        print(f"\n{category}:")
        for word in words:
            freq = zipf_frequency(word, 'es')
            print(f"  '{word}' (freq: {freq:.2f})")

print("\n" + "=" * 60)
print("VOCABULARY LEVELS FOR SPANISH LEARNING:")
print("-" * 40)
print(f"Level 1 (Basic):        freq >= 6     ({frequency_bins['Very Common (6+)']:,} words)")
print(f"Level 2 (Elementary):   freq 5-6      ({frequency_bins['Common (5-6)']:,} words)")
print(f"Level 3 (Intermediate): freq 3-5      ({frequency_bins['Moderate (4-5)'] + frequency_bins['Uncommon (3-4)']:,} words)")
print(f"Level 4 (Advanced):     freq 2-3      ({frequency_bins['Rare (2-3)']:,} words)")
print(f"Level 5 (Expert):       freq <2       ({frequency_bins['Very Rare (1-2)'] + frequency_bins['Extremely Rare (<1)']:,} words)")

# Test common Spanish words
print("\n" + "=" * 60)
print("Common Spanish word frequencies:")
print("-" * 40)
test_words = [
    'el', 'la', 'de', 'que', 'y', 'a', 'en',  # Most common
    'hola', 'casa', 'perro', 'gato',  # Basic nouns
    'comer', 'hablar', 'vivir',  # Common verbs
    'ordenador', 'algoritmo',  # Technical
    'serendipia', 'perspicaz'  # Rare
]

for word in test_words:
    freq = zipf_frequency(word, 'es')
    print(f"  '{word:15}' freq: {freq:.2f}")