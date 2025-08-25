"""
Sample Spanish words from wordfreq and clean variations
Groups word families together to avoid duplicate translations
"""

import wordfreq
from wordfreq import zipf_frequency
from collections import defaultdict
import json
import re

print("Sampling Spanish vocabulary from wordfreq...")
print("=" * 60)

# Define our difficulty ranges
difficulty_ranges = [
    ("Basic", 5.0, 10.0),
    ("Elementary", 4.5, 5.0),
    ("Intermediate", 4.0, 4.5),
    ("Advanced", 3.5, 4.0),
    ("Expert", 3.0, 3.5)
]

# Common Spanish verb endings to identify infinitives
verb_endings = ['ar', 'er', 'ir']
verb_conjugation_endings = [
    'o', 'as', 'a', 'amos', 'áis', 'an',  # present
    'é', 'aste', 'ó', 'amos', 'asteis', 'aron',  # preterite
    'aba', 'abas', 'ábamos', 'abais', 'aban',  # imperfect -ar
    'ía', 'ías', 'íamos', 'íais', 'ían',  # imperfect -er/-ir
    'aré', 'arás', 'ará', 'aremos', 'aréis', 'arán',  # future
    'ando', 'iendo', 'ado', 'ido',  # participles
]

# Common noun/adjective variations
noun_adj_endings = [
    ('o', 'a', 'os', 'as'),  # gender/number variations
    ('e', 'es'),  # plural
    ('z', 'ces'),  # z->ces plural
    ('ción', 'ciones'),  # -ción words
    ('dad', 'dades'),  # -dad words
    ('mente',),  # adverbs from adjectives
]

def identify_base_form(word, word_list_set):
    """Try to identify the base form of a word"""
    
    # Check if it's already an infinitive verb
    if len(word) > 2 and word[-2:] in verb_endings:
        return word, 'verb'
    
    # Check for verb conjugations
    for ending in verb_endings:
        # Try common verb stems
        possible_infinitives = [
            word + ending,  # just add ending
            word[:-1] + ending,  # remove last letter and add
            word[:-2] + ending,  # remove last 2 letters and add
            re.sub(r'([^aeiou])$', r'\1' + ending, word),  # consonant + ending
        ]
        
        for infinitive in possible_infinitives:
            if infinitive in word_list_set and infinitive != word:
                return infinitive, 'verb'
    
    # Check for plural nouns/adjectives
    if word.endswith('s') and len(word) > 2:
        singular = word[:-1]
        if singular in word_list_set:
            return singular, 'noun/adj'
    
    if word.endswith('es') and len(word) > 3:
        singular = word[:-2]
        if singular in word_list_set:
            return singular, 'noun/adj'
    
    if word.endswith('ces') and len(word) > 4:
        singular = word[:-3] + 'z'
        if singular in word_list_set:
            return singular, 'noun/adj'
    
    # Check for feminine forms
    if word.endswith('a') and len(word) > 2:
        masculine = word[:-1] + 'o'
        if masculine in word_list_set:
            return masculine, 'noun/adj'
    
    # Check for adverbs from adjectives
    if word.endswith('mente') and len(word) > 6:
        # Try to find the adjective
        adj_stem = word[:-5]  # remove 'mente'
        possible_adjs = [adj_stem, adj_stem + 'o', adj_stem + 'a']
        for adj in possible_adjs:
            if adj in word_list_set:
                return adj, 'adverb_from_adj'
    
    return word, 'base'

# Collect words by difficulty level
words_by_difficulty = defaultdict(list)
word_families = defaultdict(set)

print("\nCollecting Spanish words by difficulty...")

# First pass: collect all words
all_words = []
word_set = set()
for word in wordfreq.iter_wordlist('es'):
    freq = zipf_frequency(word, 'es')
    if freq >= 3.0:  # Only words with freq >= 3.0
        all_words.append((word, freq))
        word_set.add(word)

print(f"Found {len(all_words)} words with frequency >= 3.0")

# Second pass: identify base forms and group families
print("\nIdentifying word families...")
for word, freq in all_words:
    base_form, word_type = identify_base_form(word, word_set)
    
    # Add to word family
    word_families[base_form].add(word)
    
    # Categorize by difficulty
    for diff_name, min_freq, max_freq in difficulty_ranges:
        if min_freq <= freq < max_freq:
            words_by_difficulty[diff_name].append({
                'word': word,
                'base_form': base_form if base_form != word else None,
                'zipf': round(freq, 1),
                'word_type': word_type
            })
            break

# Select representative words (prefer base forms)
print("\nSelecting representative words from families...")
selected_words = defaultdict(list)

for diff_name in words_by_difficulty:
    # Group by base form
    base_form_groups = defaultdict(list)
    for word_data in words_by_difficulty[diff_name]:
        base = word_data['base_form'] or word_data['word']
        base_form_groups[base].append(word_data)
    
    # Select one representative from each family
    for base, family in base_form_groups.items():
        # Prefer the base form if it exists in the family
        representative = None
        for member in family:
            if member['word'] == base or member['base_form'] is None:
                representative = member
                break
        
        if not representative:
            # Take the highest frequency one
            representative = max(family, key=lambda x: x['zipf'])
        
        selected_words[diff_name].append(representative)

# Limit words per difficulty for initial implementation
max_words_per_level = {
    "Basic": 100,
    "Elementary": 200,
    "Intermediate": 300,
    "Advanced": 400,
    "Expert": 500
}

# Sort by frequency and limit
final_selection = {}
for diff_name in selected_words:
    sorted_words = sorted(selected_words[diff_name], key=lambda x: x['zipf'], reverse=True)
    limit = max_words_per_level.get(diff_name, 500)
    final_selection[diff_name] = sorted_words[:limit]

# Print summary
print("\n" + "=" * 60)
print("VOCABULARY SELECTION SUMMARY:")
print("-" * 40)
total = 0
for diff_name in ["Basic", "Elementary", "Intermediate", "Advanced", "Expert"]:
    count = len(final_selection.get(diff_name, []))
    total += count
    print(f"{diff_name:15} {count:5} words")
print(f"{'TOTAL':15} {total:5} words")

# Show samples
print("\n" + "=" * 60)
print("SAMPLE WORDS BY DIFFICULTY:")
print("-" * 40)

for diff_name in ["Basic", "Elementary", "Intermediate", "Advanced", "Expert"]:
    words = final_selection.get(diff_name, [])
    if words:
        print(f"\n{diff_name}:")
        for word_data in words[:5]:
            word = word_data['word']
            base = word_data['base_form']
            freq = word_data['zipf']
            if base and base != word:
                print(f"  {word:20} (base: {base:15}) zipf: {freq}")
            else:
                print(f"  {word:20} {'':23} zipf: {freq}")

# Save to JSON file
output = {
    'metadata': {
        'language': 'es',
        'total_words': total,
        'source': 'wordfreq',
        'difficulty_ranges': {
            'Basic': '5.0+',
            'Elementary': '4.5-5.0',
            'Intermediate': '4.0-4.5',
            'Advanced': '3.5-4.0',
            'Expert': '3.0-3.5'
        }
    },
    'vocabulary': final_selection
}

output_file = 'spanish_vocabulary_selection.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n" + "=" * 60)
print(f"Saved {total} words to {output_file}")
print("Ready for translation and definition generation!")