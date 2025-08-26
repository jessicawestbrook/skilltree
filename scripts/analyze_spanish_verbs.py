import json

# Load the questions
with open('scripts/spanish_data/anki_spanish_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total unique questions generated: {len(data)}")

# Analyze verbs
verbs = set()
for q in data:
    hint = q['question_text']
    if 'Hint:' in hint:
        verb = hint.split('Hint:')[1].strip().strip(')').strip()
        verbs.add(verb)

sorted_verbs = sorted(list(verbs))
print(f"\nTotal different verbs covered: {len(verbs)}")
print("\nComplete list of Spanish verbs included:")
for i in range(0, len(sorted_verbs), 10):
    print(f"  {', '.join(sorted_verbs[i:i+10])}")

# Count questions per verb (sample)
verb_counts = {}
for q in data:
    hint = q['question_text']
    if 'Hint:' in hint:
        verb = hint.split('Hint:')[1].strip().strip(')').strip()
        verb_counts[verb] = verb_counts.get(verb, 0) + 1

print("\nQuestions per verb (top 10):")
for verb, count in sorted(verb_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {verb}: {count} questions")