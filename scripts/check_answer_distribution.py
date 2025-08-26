import json

# Load the questions
with open('scripts/spanish_data/anki_spanish_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Count the distribution of correct answer positions
position_counts = {0: 0, 1: 0, 2: 0, 3: 0}

for q in data:
    correct_index = q['correct_answer']
    if correct_index in position_counts:
        position_counts[correct_index] += 1

print(f"Total questions: {len(data)}")
print(f"\nDistribution of correct answer positions:")
for pos, count in sorted(position_counts.items()):
    percentage = (count / len(data)) * 100
    print(f"  Position {pos}: {count} questions ({percentage:.1f}%)")

# Show some examples
print(f"\nSample questions showing varied answer positions:")
for i in [0, 10, 20, 30, 40]:
    q = data[i]
    correct_idx = q['correct_answer']
    correct_ans = q['options'][correct_idx]
    print(f"  Q{i+1}: Correct answer '{correct_ans}' is at position {correct_idx}")
    print(f"       Options: {q['options']}")