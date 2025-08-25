"""
Check total number of English words in wordfreq library
and analyze frequency distribution
"""

import wordfreq
from wordfreq import available_languages, iter_wordlist, zipf_frequency
import sys

print("Checking wordfreq English word coverage...")
print("=" * 60)

# Check if English is available
if 'en' in available_languages():
    print("[OK] English language is available in wordfreq")
else:
    print("[ERROR] English not available")
    sys.exit(1)

print("\nCounting total English words...")

# Count total words
total_words = 0
frequency_buckets = {
    'Very Common (6+)': 0,
    'Common (5-6)': 0,
    'Moderate (4-5)': 0,
    'Uncommon (3-4)': 0,
    'Rare (2-3)': 0,
    'Very Rare (1-2)': 0,
    'Extremely Rare (0-1)': 0,
    'Zero frequency': 0
}

# Sample words at different frequencies
sample_words = {
    'Very Common (6+)': [],
    'Common (5-6)': [],
    'Moderate (4-5)': [],
    'Uncommon (3-4)': [],
    'Rare (2-3)': [],
    'Very Rare (1-2)': [],
    'Extremely Rare (0-1)': []
}

print("(This may take a minute...)")

# Iterate through all words
for word in iter_wordlist('en'):
    total_words += 1
    
    # Get frequency
    freq = zipf_frequency(word, 'en')
    
    # Categorize
    if freq >= 6:
        frequency_buckets['Very Common (6+)'] += 1
        if len(sample_words['Very Common (6+)']) < 5:
            sample_words['Very Common (6+)'].append(word)
    elif freq >= 5:
        frequency_buckets['Common (5-6)'] += 1
        if len(sample_words['Common (5-6)']) < 5:
            sample_words['Common (5-6)'].append(word)
    elif freq >= 4:
        frequency_buckets['Moderate (4-5)'] += 1
        if len(sample_words['Moderate (4-5)']) < 5:
            sample_words['Moderate (4-5)'].append(word)
    elif freq >= 3:
        frequency_buckets['Uncommon (3-4)'] += 1
        if len(sample_words['Uncommon (3-4)']) < 5:
            sample_words['Uncommon (3-4)'].append(word)
    elif freq >= 2:
        frequency_buckets['Rare (2-3)'] += 1
        if len(sample_words['Rare (2-3)']) < 5:
            sample_words['Rare (2-3)'].append(word)
    elif freq >= 1:
        frequency_buckets['Very Rare (1-2)'] += 1
        if len(sample_words['Very Rare (1-2)']) < 5:
            sample_words['Very Rare (1-2)'].append(word)
    elif freq > 0:
        frequency_buckets['Extremely Rare (0-1)'] += 1
        if len(sample_words['Extremely Rare (0-1)']) < 5:
            sample_words['Extremely Rare (0-1)'].append(word)
    else:
        frequency_buckets['Zero frequency'] += 1
    
    # Progress indicator
    if total_words % 50000 == 0:
        print(f"  Processed {total_words:,} words...")

print(f"\n{'='*60}")
print(f"TOTAL ENGLISH WORDS IN WORDFREQ: {total_words:,}")
print(f"{'='*60}\n")

print("Frequency Distribution:")
print("-" * 40)
for category, count in frequency_buckets.items():
    percentage = (count / total_words * 100) if total_words > 0 else 0
    print(f"{category:25} {count:8,} ({percentage:5.2f}%)")

print("\n" + "=" * 60)
print("Sample words by frequency category:")
print("-" * 40)
for category, words in sample_words.items():
    if words:
        print(f"\n{category}:")
        for word in words[:5]:
            freq = zipf_frequency(word, 'en')
            print(f"  '{word}' (freq: {freq:.2f})")

print("\n" + "=" * 60)
print("Vocabulary Difficulty Mapping (for our app):")
print("-" * 40)
print("Level 1 (Basic):        freq ≥ 6.0  →", frequency_buckets['Very Common (6+)'], "words")
print("Level 2 (Elementary):   freq 5-6    →", frequency_buckets['Common (5-6)'], "words")
print("Level 3 (Intermediate): freq 3-5    →", 
      frequency_buckets['Moderate (4-5)'] + frequency_buckets['Uncommon (3-4)'], "words")
print("Level 4 (Advanced):     freq 2-3    →", frequency_buckets['Rare (2-3)'], "words")
print("Level 5 (Expert):       freq 0-2    →", 
      frequency_buckets['Very Rare (1-2)'] + frequency_buckets['Extremely Rare (0-1)'] + frequency_buckets['Zero frequency'], "words")

# Additional analysis
print("\n" + "=" * 60)
print("Quick statistics:")
print("-" * 40)

# Test some specific words
test_words = ['the', 'cat', 'computer', 'algorithm', 'serendipity', 'perspicacious', 'antidisestablishmentarianism']
print("\nFrequencies of test words:")
for word in test_words:
    freq = zipf_frequency(word, 'en')
    print(f"  '{word}': {freq:.2f}")