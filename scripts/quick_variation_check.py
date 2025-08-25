"""
Quick estimate of word variations in wordfreq
"""

import wordfreq
from collections import defaultdict

print("Quick analysis of word variations...")
print("=" * 50)

# Sample first 5000 words
sample = []
for i, word in enumerate(wordfreq.iter_wordlist('en')):
    sample.append(word)
    if i >= 5000:
        break

# Count obvious variations
variations = 0
for word in sample:
    # Common variation patterns
    if len(word) > 3 and any([
        word.endswith('s'),
        word.endswith('ed'),
        word.endswith('ing'),
        word.endswith('er'),
        word.endswith('est'),
        word.endswith('ly'),
        word.endswith('ness'),
        word.endswith('ment'),
        word.endswith('tion'),
        word.endswith('able'),
        word.endswith('ful'),
        word.endswith('less'),
        word.endswith('ize')
    ]):
        variations += 1

percent = (variations / len(sample)) * 100

print(f"\nIn sample of {len(sample):,} words:")
print(f"  Likely variations: {variations:,} ({percent:.0f}%)")
print(f"\nEstimate for all 321,180 words:")
print(f"  ~{int(321180 * percent / 100):,} are variations")
print(f"  ~{int(321180 * (100-percent) / 100):,} are unique base words")