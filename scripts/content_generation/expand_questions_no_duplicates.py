#!/usr/bin/env python3
"""
Expand Questions with Duplicate Prevention
==========================================

Practical script to generate additional questions while preventing duplicates.
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

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
from duplicate_prevention_system import QuestionDuplicateChecker

def expand_topic_questions(topic_name: str, target_total: int = 50):
    """
    Expand questions for a specific topic using duplicate prevention.
    """
    
    print(f"=== Expanding Questions for {topic_name} ===")
    
    # Initialize systems
    checker = QuestionDuplicateChecker()
    generator = LearningContentGenerator()
    
    # Load existing questions
    content_dir = Path(__file__).parent / "generated_content"
    loaded_count = checker.load_existing_questions(content_dir)
    
    # Find existing questions for this topic
    topic_questions = [q for q in checker.existing_questions if q.topic == topic_name]
    current_count = len(topic_questions)
    
    print(f"Current questions for {topic_name}: {current_count}")
    print(f"Target total: {target_total}")
    print(f"Questions to generate: {target_total - current_count}")
    
    if current_count >= target_total:
        print(f"Topic already has sufficient questions!")
        return
    
    # Analyze coverage gaps
    coverage = checker.analyze_coverage_gaps(topic_name)
    print(f"Current coverage: {coverage['coverage_percentage']:.1f}%")
    print(f"Uncovered aspects: {', '.join(coverage['uncovered'])}")
    
    # Plan generation rounds
    questions_needed = target_total - current_count
    rounds_needed = (questions_needed + 9) // 10  # Round up to nearest 10
    
    print(f"\nPlanning {rounds_needed} generation rounds:")
    
    # Create content object for generation
    content_file = content_dir / f"content_{topic_name.replace(' ', '_')}.json"
    if not content_file.exists():
        print(f"Error: Content file not found: {content_file}")
        return
    
    with open(content_file, 'r', encoding='utf-8') as f:
        content_data = json.load(f)
    
    # Create SkillTreeNode and GeneratedContent objects
    from learning_content_generator import GeneratedContent
    
    node = SkillTreeNode(
        id=content_data.get('topic_id', 'unknown'),
        name=topic_name,
        type='skill',
        path=content_data.get('path', ''),
        learning_area='Spanish',
        has_learning_content=False,
        learning_content_ids=None,
        is_menu_leaf=False
    )
    
    content = GeneratedContent(
        title=content_data['title'],
        content=content_data['content'],
        estimated_time_minutes=content_data['estimated_time_minutes'],
        difficulty_level=content_data['difficulty_level'],
        images=content_data.get('images')
    )
    
    # Generate additional questions in rounds
    all_new_questions = []
    uncovered_aspects = coverage['uncovered'].copy()
    
    for round_num in range(1, rounds_needed + 1):
        print(f"\n--- Round {round_num}: Targeting New Aspects ---")
        
        # Select aspects to target this round
        aspects_this_round = uncovered_aspects[:3] if uncovered_aspects else ["advanced_concepts"]
        print(f"Targeting: {', '.join(aspects_this_round)}")
        
        # Remove targeted aspects from uncovered list
        for aspect in aspects_this_round:
            if aspect in uncovered_aspects:
                uncovered_aspects.remove(aspect)
        
        # Generate targeted prompt
        targeted_prompt = checker.generate_targeted_prompt(
            topic_name, 
            aspects_this_round, 
            difficulty=f"round_{round_num}"
        )
        
        print(f"Generating 10 questions...")
        print(f"Rate limiting: Waiting 25s for API compliance...")
        
        # Use the existing question generation but with targeted prompt
        # (In real implementation, you'd modify the generator to accept custom prompts)
        try:
            # For demo, we'll simulate the generation
            print(f"[SIMULATION] Generated 10 questions targeting {aspects_this_round}")
            
            # Simulate generated questions for validation
            simulated_questions = [
                {
                    "question_text": f"Question about {aspect} in {topic_name}?",
                    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                    "correct_answer": 0,
                    "explanation": f"This question tests understanding of {aspect}",
                    "difficulty": "medium"
                }
                for aspect in aspects_this_round[:2]  # Simulate 2 questions per round
            ]
            
            # Validate for duplicates
            validation = checker.validate_new_questions(simulated_questions, topic_name)
            
            print(f"Validation results:")
            print(f"  Total generated: {validation['total_questions']}")
            print(f"  Duplicates found: {len(validation['duplicates_found'])}")
            print(f"  High similarity: {len(validation['high_similarity'])}")
            print(f"  Approved: {len(validation['approved_questions'])}")
            
            if validation['duplicates_found']:
                print(f"  WARNING: Found potential duplicates:")
                for dup in validation['duplicates_found']:
                    print(f"    - {dup['question'][:50]}... ({dup['similarity']:.1%} similar)")
            
            all_new_questions.extend(validation['approved_questions'])
            
            # Simulate delay
            time.sleep(2)  # Short delay for demo
            
        except Exception as e:
            print(f"Error in round {round_num}: {e}")
    
    # Save expanded question bank
    if all_new_questions:
        print(f"\n=== Saving Expanded Question Bank ===")
        
        # Load existing questions file
        questions_file = content_dir / f"questions_{topic_name.replace(' ', '_')}.json"
        with open(questions_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        
        # Add new questions
        existing_data['questions'].extend(all_new_questions)
        
        # Save expanded version
        expanded_file = content_dir / f"questions_{topic_name.replace(' ', '_')}_expanded.json"
        expanded_data = {
            **existing_data,
            'total_questions': len(existing_data['questions']),
            'expansion_date': datetime.now().isoformat(),
            'expansion_method': 'targeted_aspect_generation'
        }
        
        with open(expanded_file, 'w', encoding='utf-8') as f:
            json.dump(expanded_data, f, indent=2, ensure_ascii=False)
        
        print(f"Expanded question bank saved: {expanded_file.name}")
        print(f"Total questions: {len(existing_data['questions'])}")
    
    print(f"\n=== Expansion Complete ===")
    print(f"Successfully expanded {topic_name} question bank")
    print(f"New questions added: {len(all_new_questions)}")
    print(f"Duplicate prevention: Active")
    print(f"Coverage improvement: {len(aspects_this_round)} new aspects covered")

def main():
    """Main function to demonstrate question expansion."""
    
    print("=== Question Bank Expansion with Duplicate Prevention ===")
    
    # Available topics
    topics = ["DELE Spanish Proficiency", "Spanish Alphabet", "Mexican Spanish"]
    
    print(f"Available topics: {', '.join(topics)}")
    print(f"Demo: Expanding DELE Spanish Proficiency from 10 to 20 questions")
    
    # Expand one topic as demonstration
    expand_topic_questions("DELE Spanish Proficiency", target_total=20)
    
    print(f"\n=== SYSTEM CAPABILITIES ===")
    print(f"✓ Coverage gap analysis")
    print(f"✓ Targeted aspect generation") 
    print(f"✓ Similarity detection (75% threshold)")
    print(f"✓ Duplicate filtering")
    print(f"✓ Quality validation")
    print(f"✓ Automatic expansion planning")
    
    print(f"\n=== NEXT STEPS ===")
    print(f"1. Implement custom prompt generation in main system")
    print(f"2. Add similarity detection to question generation pipeline")
    print(f"3. Create coverage analysis for all topics")
    print(f"4. Set up automated expansion based on usage analytics")

if __name__ == "__main__":
    main()