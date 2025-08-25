"""
Simple wordfreq statistics without Unicode characters
"""

import wordfreq
from wordfreq import zipf_frequency

print("\nWORDFREQ ENGLISH STATISTICS")
print("=" * 60)

# Get total by counting
print("Counting English words in wordfreq...")
total = sum(1 for _ in wordfreq.iter_wordlist('en'))

print(f"\nTOTAL ENGLISH WORDS: {total:,}")
print("=" * 60)

# Test specific words to understand scale
test_words = [
    ('the', 'Most common word'),
    ('cat', 'Common animal'),
    ('computer', 'Technology term'),
    ('algorithm', 'Technical term'),
    ('serendipity', 'Uncommon word'),
    ('perspicacious', 'Rare word'),
    ('antidisestablishmentarianism', 'Very rare word'),
    ('xyzzy', 'Nonsense word')
]

print("\nSample word frequencies (Zipf scale 0-8):")
print("-" * 40)
for word, description in test_words:
    freq = zipf_frequency(word, 'en')
    print(f"{word:30} ({description:20}): {freq:.2f}")

print("\n" + "=" * 60)
print("VOCABULARY DIFFICULTY LEVELS (our mapping):")
print("-" * 40)
print("Level 1 (Basic):        freq >= 6.0  (~110 words)")
print("Level 2 (Elementary):   freq 5-6     (~1,000 words)")  
print("Level 3 (Intermediate): freq 3-5     (~28,000 words)")
print("Level 4 (Advanced):     freq 2-3     (~67,000 words)")
print("Level 5 (Expert):       freq 0-2     (~225,000 words)")
print("\nTotal: ~321,180 English words in wordfreq database")