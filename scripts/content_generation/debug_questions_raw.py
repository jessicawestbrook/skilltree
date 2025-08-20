#!/usr/bin/env python3
"""
Debug raw question generation output to see what the model is producing.
"""

import os
import sys
import json
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env.local
env_file = project_root / '.env.local'
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

import anthropic
from learning_content_generator import SkillTreeNode, GeneratedContent

def main():
    try:
        claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        # Create test content
        test_content = GeneratedContent(
            title="DELE Spanish Proficiency",
            content="The DELE (Diplomas de Español como Lengua Extranjera) exam...",
            estimated_time_minutes=20,
            difficulty_level="intermediate",
            images=None
        )
        
        test_node = SkillTreeNode(
            id="test-id",
            name="DELE Spanish Proficiency",
            type="skill",
            path="Learning/Languages/Spanish",
            learning_area="Spanish Language",
            has_learning_content=False,
            learning_content_ids=None,
            is_menu_leaf=False
        )
        
        prompt = f"""
Generate 5 multiple choice questions based on the following learning content about {test_node.name}.

Learning Content Title: {test_content.title}
Content: {test_content.content[:500]}...

Please create questions that test comprehension of this material. Each question should have 4 options (A, B, C, D) with one correct answer.

Return ONLY a valid JSON array in this exact format:
[
  {{
    "question": "What does DELE stand for?",
    "options": ["A) Spanish Language Diploma", "B) Diplomas de Español como Lengua Extranjera", "C) Spanish Proficiency Test", "D) Language Certification Exam"],
    "correct_answer": 1,
    "explanation": "DELE stands for Diplomas de Español como Lengua Extranjera, which means Diplomas of Spanish as a Foreign Language.",
    "difficulty": "beginner"
  }}
]

Important: Return ONLY the JSON array, no other text before or after.
"""

        print("=== Sending request to Claude ===")
        print("Prompt preview:")
        print(prompt[:500] + "...")
        
        response = claude.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=4000,
            temperature=0.8,
            messages=[{"role": "user", "content": prompt}]
        )
        
        raw_response = response.content[0].text
        print("\n=== Raw Claude Response ===")
        print(f"Response length: {len(raw_response)} characters")
        print("First 500 characters:")
        print(repr(raw_response[:500]))
        print("\nLast 500 characters:")
        print(repr(raw_response[-500:]))
        
        print("\n=== Attempting JSON Parse ===")
        try:
            questions_data = json.loads(raw_response)
            print(f"SUCCESS: Parsed {len(questions_data)} questions")
            for i, q in enumerate(questions_data[:2]):
                print(f"  Q{i+1}: {q.get('question', 'NO QUESTION FIELD')}")
                print(f"       Options: {len(q.get('options', []))}")
                print(f"       Correct: {q.get('correct_answer', 'NO ANSWER FIELD')}")
        except json.JSONDecodeError as e:
            print(f"JSON PARSE ERROR: {e}")
            print(f"Error at position: {e.pos}")
            if e.pos < len(raw_response):
                print(f"Character at error: {repr(raw_response[e.pos-10:e.pos+10])}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()