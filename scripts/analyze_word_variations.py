"""
Analyze how many words in wordfreq are variations of the same root word
"""

import wordfreq
from wordfreq import zipf_frequency
from collections import defaultdict
import re

print("Analyzing word variations in wordfreq...")
print("=" * 60)

# Sample analysis - full analysis would take too long
print("\nSampling first 10,000 words to analyze patterns...")

word_families = defaultdict(list)
total_words = 0
sample_size = 10000

# Common suffixes that indicate word variations
common_suffixes = [
    'ing', 'ed', 's', 'es', 'er', 'est', 'ly', 'ness', 'ment', 
    'tion', 'sion', 'ity', 'ous', 'ive', 'able', 'ible', 'ful',
    'less', 'ize', 'ise', 'ate', 'en', 'ify', 'wise', 'ward'
]

# Track different types of variations
variation_types = {
    'plural_s': 0,
    'plural_es': 0,
    'past_ed': 0,
    'present_ing': 0,
    'comparative_er': 0,
    'superlative_est': 0,
    'adverb_ly': 0,
    'noun_ness': 0,
    'noun_ment': 0,
    'noun_tion': 0,
    'other_variations': 0
}

# Collect sample words
sample_words = []
for word in wordfreq.iter_wordlist('en'):
    sample_words.append(word)
    total_words += 1
    if total_words >= sample_size:
        break

print(f"Analyzing {len(sample_words)} words...")

# Group potential word families by common roots
for word in sample_words:
    # Skip very short words
    if len(word) < 3:
        continue
    
    # Try to identify base form
    base = word
    
    # Check for common variations
    if word.endswith('s') and len(word) > 2:
        potential_base = word[:-1]
        if potential_base in sample_words:
            word_families[potential_base].append(word)
            variation_types['plural_s'] += 1
            continue
    
    if word.endswith('es') and len(word) > 3:
        potential_base = word[:-2]
        if potential_base in sample_words:
            word_families[potential_base].append(word)
            variation_types['plural_es'] += 1
            continue
    
    if word.endswith('ed') and len(word) > 3:
        potential_base = word[:-2]
        if potential_base in sample_words:
            word_families[potential_base].append(word)
            variation_types['past_ed'] += 1
            continue
        # Try with -e (like "moved" from "move")
        potential_base = word[:-1]
        if potential_base in sample_words:
            word_families[potential_base].append(word)
            variation_types['past_ed'] += 1
            continue
    
    if word.endswith('ing') and len(word) > 4:
        potential_base = word[:-3]
        if potential_base in sample_words:
            word_families[potential_base].append(word)
            variation_types['present_ing'] += 1
            continue
        # Try with -e (like "moving" from "move")
        potential_base = word[:-3] + 'e'
        if potential_base in sample_words:
            word_families[potential_base].append(word)
            variation_types['present_ing'] += 1
            continue
    
    if word.endswith('er') and len(word) > 3:
        potential_base = word[:-2]
        if potential_base in sample_words:
            word_families[potential_base].append(word)
            variation_types['comparative_er'] += 1
            continue
    
    if word.endswith('est') and len(word) > 4:
        potential_base = word[:-3]
        if potential_base in sample_words:
            word_families[potential_base].append(word)
            variation_types['superlative_est'] += 1
            continue
    
    if word.endswith('ly') and len(word) > 3:
        potential_base = word[:-2]
        if potential_base in sample_words:
            word_families[potential_base].append(word)
            variation_types['adverb_ly'] += 1
            continue
    
    if word.endswith('ness') and len(word) > 5:
        potential_base = word[:-4]
        if potential_base in sample_words:
            word_families[potential_base].append(word)
            variation_types['noun_ness'] += 1
            continue
    
    if word.endswith('ment') and len(word) > 5:
        potential_base = word[:-4]
        if potential_base in sample_words:
            word_families[potential_base].append(word)
            variation_types['noun_ment'] += 1
            continue
    
    if word.endswith('tion') and len(word) > 5:
        # Try various transformations
        for suffix in ['te', 't', '']:
            potential_base = word[:-4] + suffix
            if potential_base in sample_words:
                word_families[potential_base].append(word)
                variation_types['noun_tion'] += 1
                break

# Calculate statistics
total_variations = sum(len(variations) for variations in word_families.values())
base_words_with_variations = len(word_families)

print("\n" + "=" * 60)
print("RESULTS FROM SAMPLE:")
print("-" * 40)
print(f"Sample size: {sample_size:,} words")
print(f"Base words with variations: {base_words_with_variations:,}")
print(f"Total variations found: {total_variations:,}")
print(f"Percentage that are variations: {(total_variations/sample_size)*100:.1f}%")

print("\n" + "=" * 60)
print("VARIATION TYPES FOUND:")
print("-" * 40)
for var_type, count in sorted(variation_types.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        print(f"{var_type:20} {count:5} ({(count/total_variations)*100:.1f}%)")

print("\n" + "=" * 60)
print("EXAMPLE WORD FAMILIES:")
print("-" * 40)

# Show some examples
examples_shown = 0
for base, variations in sorted(word_families.items(), key=lambda x: len(x[1]), reverse=True):
    if examples_shown >= 10:
        break
    if len(variations) >= 2:
        print(f"\n'{base}' family ({len(variations)} variations):")
        all_words = [base] + variations
        for w in all_words[:8]:  # Limit display
            freq = zipf_frequency(w, 'en')
            print(f"  - {w:20} (freq: {freq:.2f})")
        if len(all_words) > 8:
            print(f"  ... and {len(all_words)-8} more")
        examples_shown += 1

# Now let's check some specific common words to see all their variations
print("\n" + "=" * 60)
print("CHECKING SPECIFIC COMMON WORDS FOR ALL VARIATIONS:")
print("-" * 40)

test_roots = ['run', 'walk', 'talk', 'play', 'work', 'think']

for root in test_roots:
    print(f"\nVariations of '{root}':")
    variations_found = []
    
    # Check common variations
    possible_variations = [
        root,
        root + 's',
        root + 'ed',
        root + 'ing',
        root + 'er',
        root + 'ers',
        root + 'able',
        root[:-1] + 'ied' if root.endswith('y') else None,
        root[:-1] + 'ies' if root.endswith('y') else None,
        root[:-1] + 'ing' if root.endswith('e') else None,
    ]
    
    for variant in possible_variations:
        if variant and variant in sample_words:
            freq = zipf_frequency(variant, 'en')
            variations_found.append((variant, freq))
    
    # Sort by frequency
    variations_found.sort(key=lambda x: x[1], reverse=True)
    for word, freq in variations_found:
        print(f"  {word:15} freq: {freq:.2f}")
    
    if not variations_found:
        print("  (none found in sample)")

print("\n" + "=" * 60)
print("ESTIMATED TOTAL (extrapolating from sample):")
print("-" * 40)
estimated_total_variations = int((total_variations / sample_size) * 321180)
estimated_base_words = 321180 - estimated_total_variations
print(f"Estimated variations in full dataset: ~{estimated_total_variations:,}")
print(f"Estimated unique base words: ~{estimated_base_words:,}")
print(f"Estimated % that are variations: ~{(estimated_total_variations/321180)*100:.0f}%")