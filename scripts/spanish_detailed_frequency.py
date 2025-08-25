"""
Detailed Spanish word count by exact Zipf frequency value
"""

import wordfreq
from wordfreq import zipf_frequency
from collections import defaultdict

print("\nSPANISH WORDS BY EXACT ZIPF FREQUENCY")
print("=" * 60)

print("Counting Spanish words by exact frequency value...")
print("(This may take a minute...)\n")

# Dictionary to hold counts for each frequency value
freq_counts = defaultdict(int)
freq_samples = defaultdict(list)

total = 0
for word in wordfreq.iter_wordlist('es'):
    total += 1
    freq = zipf_frequency(word, 'es')
    
    # Round to 1 decimal place for grouping
    freq_rounded = round(freq, 1)
    freq_counts[freq_rounded] += 1
    
    # Keep up to 3 samples per frequency level
    if len(freq_samples[freq_rounded]) < 3:
        freq_samples[freq_rounded].append(word)
    
    if total % 50000 == 0:
        print(f"  Processed {total:,} words...")

print(f"\nTOTAL SPANISH WORDS: {total:,}")
print("=" * 60)

print("\nDetailed Frequency Distribution:")
print("-" * 60)
print("Zipf   |   Count   |    %    | Cumulative | Examples")
print("Value  |           |         |     %      |")
print("-" * 60)

cumulative = 0
cumulative_percent = 0

# Sort by frequency value (descending)
for freq in sorted(freq_counts.keys(), reverse=True):
    count = freq_counts[freq]
    percent = (count/total*100)
    cumulative += count
    cumulative_percent = (cumulative/total*100)
    
    # Get sample words
    samples = freq_samples[freq]
    sample_str = ', '.join([f"'{w}'" for w in samples[:2]])
    if len(samples) > 2:
        sample_str += "..."
    
    print(f"{freq:5.1f}  | {count:9,} | {percent:7.2f}% | {cumulative_percent:9.2f}% | {sample_str[:40]}")

print("-" * 60)

# Summary statistics
print("\n" + "=" * 60)
print("SUMMARY BY FREQUENCY RANGES:")
print("-" * 40)

ranges = [
    ("7.0+", 7.0, 8.0, "Most common words"),
    ("6.0-6.9", 6.0, 7.0, "Very common words"),
    ("5.0-5.9", 5.0, 6.0, "Common words"),
    ("4.0-4.9", 4.0, 5.0, "Moderate frequency"),
    ("3.0-3.9", 3.0, 4.0, "Uncommon words"),
    ("2.0-2.9", 2.0, 3.0, "Rare words"),
    ("1.0-1.9", 1.0, 2.0, "Very rare words"),
    ("0.0-0.9", 0.0, 1.0, "Extremely rare")
]

cumulative = 0
for label, min_freq, max_freq, description in ranges:
    count = sum(freq_counts[f] for f in freq_counts if min_freq <= f < max_freq)
    cumulative += count
    percent = (count/total*100) if total > 0 else 0
    cumulative_percent = (cumulative/total*100) if total > 0 else 0
    print(f"{label:8} {count:9,} ({percent:6.2f}%) - Cumulative: {cumulative:9,} ({cumulative_percent:6.2f}%) - {description}")

print("\n" + "=" * 60)
print("KEY MILESTONES:")
print("-" * 40)

milestones = [100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
current_cumulative = 0

for freq in sorted(freq_counts.keys(), reverse=True):
    current_cumulative += freq_counts[freq]
    for milestone in milestones[:]:
        if current_cumulative >= milestone:
            print(f"Top {milestone:,} words: frequency >= {freq:.1f}")
            milestones.remove(milestone)