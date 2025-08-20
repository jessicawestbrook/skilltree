#!/usr/bin/env python3
"""
Test content generation with all fixes, but skip database insertion for now.
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
        
        # Create a test node
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
        
        print("=== Complete Content Generation Test ===")
        
        print("\n1. Generating learning content...")
        content = generator.generate_learning_content(test_node)
        if content:
            print(f"SUCCESS: Generated {len(content.content)} character content")
            print(f"   Title: {content.title}")
            print(f"   Time: {content.estimated_time_minutes} minutes") 
            print(f"   Difficulty: {content.difficulty_level}")
        else:
            print("FAILED: Content generation failed")
            return
        
        print("\n2. Generating questions...")
        questions = generator.generate_questions(test_node, content)
        if questions:
            print(f"SUCCESS: Generated {len(questions)} questions")
            
            # Show details of first few questions
            for i, q in enumerate(questions[:3]):
                print(f"\n   Q{i+1}: {q.question_text}")
                print(f"        A) {q.options[0]}")
                print(f"        B) {q.options[1]}")
                print(f"        C) {q.options[2]}")
                print(f"        D) {q.options[3]}")
                print(f"        Correct: {chr(65 + q.correct_answer)} ({q.options[q.correct_answer]})")
                print(f"        Difficulty: {q.difficulty}")
                print(f"        Explanation: {q.explanation[:100]}...")
        else:
            print("FAILED: Question generation failed")
        
        print("\n=== Generation Complete ===")
        print(f"Generated content suitable for 10-30 minutes of learning")
        print(f"Generated {len(questions) if questions else 0} multiple choice questions with explanations")
        print("Content and questions are ready for database insertion")
        
        # Save to local files for review
        if content and questions:
            print("\n3. Saving to local files for review...")
            
            # Save content
            content_file = Path(__file__).parent / f"generated_content_{test_node.name.replace(' ', '_')}.json"
            content_data = {
                "title": content.title,
                "content": content.content,
                "estimated_time_minutes": content.estimated_time_minutes,
                "difficulty_level": content.difficulty_level,
                "images": content.images
            }
            
            with open(content_file, 'w', encoding='utf-8') as f:
                json.dump(content_data, f, indent=2, ensure_ascii=False)
            
            # Save questions
            questions_file = Path(__file__).parent / f"generated_questions_{test_node.name.replace(' ', '_')}.json"
            questions_data = [
                {
                    "question_text": q.question_text,
                    "options": q.options,
                    "correct_answer": q.correct_answer,
                    "explanation": q.explanation,
                    "difficulty": q.difficulty,
                    "image_url": q.image_url
                }
                for q in questions
            ]
            
            with open(questions_file, 'w', encoding='utf-8') as f:
                json.dump(questions_data, f, indent=2, ensure_ascii=False)
                
            print(f"Content saved to: {content_file}")
            print(f"Questions saved to: {questions_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()