#!/usr/bin/env python3
"""
Debug a single topic generation to see what's happening.
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

from learning_content_generator import LearningContentGenerator, SkillTreeNode

def main():
    try:
        generator = LearningContentGenerator()
        
        # Create a test node for debugging
        test_node = SkillTreeNode(
            id="test-spanish-id", 
            name="DELE Spanish Proficiency",
            type="skill",
            path="Learning/Languages/Spanish",
            learning_area="Spanish Language",
            has_learning_content=False,
            learning_content_ids=None,
            is_menu_leaf=False
        )
        
        print("=== Testing Content Generation ===")
        
        # Test content generation only
        print("\n1. Testing content generation...")
        content = generator.generate_learning_content(test_node)
        if content:
            print(f"SUCCESS: Generated content: {len(content.content)} characters")
            print(f"   Title: {content.title}")
            print(f"   Time: {content.estimated_time_minutes} minutes")
            print(f"   Difficulty: {content.difficulty_level}")
            print(f"   Content preview: {content.content[:200]}...")
        else:
            print("FAILED: Content generation failed")
            return
        
        print("\n2. Testing question generation...")
        questions = generator.generate_questions(test_node, content)
        if questions:
            print(f"SUCCESS: Generated {len(questions)} questions")
            for i, q in enumerate(questions[:3]):  # Show first 3
                print(f"   Q{i+1}: {q.question_text[:100]}...")
                print(f"        Options: {len(q.options)} choices")
                print(f"        Correct: {q.correct_answer}")
                print(f"        Difficulty: {q.difficulty}")
        else:
            print("FAILED: Question generation failed")
        
        print("\n=== Debug Complete ===")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()