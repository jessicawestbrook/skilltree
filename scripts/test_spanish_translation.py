"""
Test Spanish translation with a small sample
"""

import json
import sys
import os

# Install if needed
try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("Installing deep-translator...")
    os.system(f"{sys.executable} -m pip install deep-translator")
    from deep_translator import GoogleTranslator

# Load vocabulary
with open('spanish_vocabulary_selection.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Test with just 5 words
test_words = []
for difficulty, words in data['vocabulary'].items():
    if words:
        test_words.append((difficulty, words[0]))
    if len(test_words) >= 5:
        break

print("Testing Spanish to English translation...")
print("=" * 50)

translator = GoogleTranslator(source='es', target='en')

for difficulty, word_data in test_words:
    word = word_data['word']
    try:
        translation = translator.translate(word)
        print(f"{word:15} -> {translation:20} (Level: {difficulty})")
    except Exception as e:
        print(f"Error translating {word}: {e}")

print("\nTranslation test complete!")