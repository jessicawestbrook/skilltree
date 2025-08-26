import json

# Load the questions
with open('scripts/spanish_data/anki_spanish_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total unique questions: {len(data)}")

# Analyze verbs
verbs = set()
for q in data:
    hint = q['question_text']
    if 'Hint:' in hint:
        verb = hint.split('Hint:')[1].strip().strip(')').strip()
        verbs.add(verb)

print(f"Different verbs covered: {len(verbs)}")
print(f"Sample verbs: {sorted(list(verbs))[:30]}")

# Check for exact duplicates
unique_questions = set()
duplicates = 0
for q in data:
    key = (q['question_text'], q['options'][0])  # question + correct answer
    if key in unique_questions:
        duplicates += 1
    unique_questions.add(key)

print(f"Duplicate questions found: {duplicates}")

# Sample different question types
print("\nSample questions at different positions:")
for i in [0, 100, 500, 1000, 1500, 1999]:
    if i < len(data):
        print(f"  Q{i+1}: {data[i]['question_text'][:80]}...")