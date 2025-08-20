#!/usr/bin/env python3
"""
Question Duplicate Prevention Analysis
====================================

Analyze strategies to prevent duplicate questions when expanding question banks.
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Set
import difflib

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def analyze_existing_questions():
    """Analyze existing questions to understand duplication patterns."""
    
    print("=== Question Duplicate Prevention Analysis ===")
    
    # Load existing questions
    content_dir = Path(__file__).parent / "generated_content"
    question_files = list(content_dir.glob("questions_*.json"))
    
    if not question_files:
        print("No existing question files found for analysis")
        return
    
    all_questions = []
    topics = []
    
    for file in question_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                topic_name = data.get('topic_name', file.stem)
                topics.append(topic_name)
                
                questions = data.get('questions', [])
                for q in questions:
                    all_questions.append({
                        'topic': topic_name,
                        'text': q.get('question_text', ''),
                        'options': q.get('options', []),
                        'explanation': q.get('explanation', ''),
                        'difficulty': q.get('difficulty', 'unknown')
                    })
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    print(f"Loaded {len(all_questions)} questions from {len(topics)} topics")
    print(f"Topics: {', '.join(topics)}")
    
    return all_questions

def detect_similarities(questions: List[Dict]) -> List[Dict]:
    """Detect similar questions using text similarity."""
    
    similarities = []
    
    print(f"\n=== Similarity Detection ===")
    
    for i, q1 in enumerate(questions):
        for j, q2 in enumerate(questions[i+1:], i+1):
            # Compare question text
            similarity = difflib.SequenceMatcher(None, q1['text'].lower(), q2['text'].lower()).ratio()
            
            if similarity > 0.7:  # 70% similarity threshold
                similarities.append({
                    'q1_index': i,
                    'q2_index': j,
                    'q1_topic': q1['topic'],
                    'q2_topic': q2['topic'],
                    'q1_text': q1['text'][:100] + "..." if len(q1['text']) > 100 else q1['text'],
                    'q2_text': q2['text'][:100] + "..." if len(q2['text']) > 100 else q2['text'],
                    'similarity': similarity
                })
    
    print(f"Found {len(similarities)} potential duplicates (>70% similarity)")
    
    if similarities:
        print("\nTop similar questions:")
        for sim in sorted(similarities, key=lambda x: x['similarity'], reverse=True)[:3]:
            print(f"  Similarity: {sim['similarity']:.1%}")
            print(f"    Topic 1: {sim['q1_topic']}")
            print(f"    Q1: {sim['q1_text']}")
            print(f"    Topic 2: {sim['q2_topic']}")  
            print(f"    Q2: {sim['q2_text']}")
            print()
    
    return similarities

def analyze_duplicate_prevention_strategies():
    """Analyze different strategies for preventing duplicates."""
    
    print("=== Duplicate Prevention Strategies ===")
    
    strategies = {
        "1. Prompt-Based Prevention": {
            "description": "Include existing questions in the prompt to avoid repetition",
            "pros": [
                "Simple to implement",
                "AI can directly see what to avoid",
                "Works well for small question sets"
            ],
            "cons": [
                "Increases input token usage significantly", 
                "May hit token limits with large question banks",
                "AI might focus too much on avoiding rather than creating"
            ],
            "implementation": "Include previous questions in generation prompt",
            "token_impact": "High - could double input token usage"
        },
        
        "2. Semantic Similarity Detection": {
            "description": "Use text similarity algorithms to detect and filter duplicates",
            "pros": [
                "Catches similar questions regardless of wording",
                "Can be tuned for different similarity thresholds",
                "Works post-generation to filter results"
            ],
            "cons": [
                "May miss semantically similar but differently worded questions",
                "Requires additional processing step",
                "Threshold tuning needed"
            ],
            "implementation": "Use difflib, sentence transformers, or embedding similarity",
            "token_impact": "None - post-processing only"
        },
        
        "3. Topic Aspect Targeting": {
            "description": "Generate questions targeting specific aspects/subtopics not covered",
            "pros": [
                "Ensures comprehensive coverage",
                "Natural diversity in questions",
                "Educational value through systematic coverage"
            ],
            "cons": [
                "Requires analysis of existing question coverage",
                "More complex prompt engineering",
                "May not prevent all duplicates"
            ],
            "implementation": "Analyze existing questions, target uncovered aspects",
            "token_impact": "Medium - more detailed prompts"
        },
        
        "4. Difficulty Level Progression": {
            "description": "Generate questions at different difficulty levels",
            "pros": [
                "Natural differentiation between question sets",
                "Educational progression value",
                "Reduces likelihood of exact duplicates"
            ],
            "cons": [
                "May still have duplicates within same difficulty level",
                "Requires careful difficulty level definition",
                "Some topics may not have enough depth for all levels"
            ],
            "implementation": "Sequential generation: basic → intermediate → advanced",
            "token_impact": "Low - just difficulty specification"
        },
        
        "5. Hybrid Approach": {
            "description": "Combine multiple strategies for maximum effectiveness",
            "pros": [
                "Most comprehensive prevention",
                "Catches duplicates through multiple methods",
                "Balances effectiveness with efficiency"
            ],
            "cons": [
                "More complex implementation",
                "Higher computational cost",
                "Requires tuning multiple systems"
            ],
            "implementation": "Use 2-3 strategies together",
            "token_impact": "Variable depending on combination"
        }
    }
    
    for strategy, details in strategies.items():
        print(f"\n{strategy}: {details['description']}")
        print(f"  Implementation: {details['implementation']}")
        print(f"  Token Impact: {details['token_impact']}")
        print(f"  Pros:")
        for pro in details['pros']:
            print(f"    + {pro}")
        print(f"  Cons:")
        for con in details['cons']:
            print(f"    - {con}")

def demonstrate_prevention_techniques():
    """Show practical implementation of duplicate prevention."""
    
    print(f"\n=== Practical Implementation Examples ===")
    
    # Example 1: Prompt-based prevention
    print(f"1. PROMPT-BASED PREVENTION EXAMPLE:")
    existing_questions = [
        "What does the acronym 'DELE' stand for?",
        "Which organization administers the DELE exams?",
        "What is the purpose of the DELE exams?"
    ]
    
    prompt_example = f"""
    Generate 10 new multiple choice questions about DELE Spanish Proficiency.
    
    AVOID creating questions similar to these existing ones:
    {chr(10).join(f'- {q}' for q in existing_questions)}
    
    Focus on NEW aspects such as:
    - Exam structure and format
    - Preparation strategies  
    - Score interpretation
    - Practical applications
    - Historical context
    """
    
    print("Sample prompt with existing questions:")
    print(prompt_example[:300] + "...")
    print(f"Token impact: ~{len(prompt_example.split()) * 1.3:.0f} additional input tokens")
    
    # Example 2: Aspect targeting
    print(f"\n2. ASPECT TARGETING EXAMPLE:")
    covered_aspects = ["Definition", "Administration", "Purpose"] 
    uncovered_aspects = ["Exam Format", "Scoring", "Preparation", "Levels", "Applications"]
    
    print(f"Existing questions cover: {covered_aspects}")
    print(f"Next round should target: {uncovered_aspects[:3]}")
    
    aspect_prompt = f"""
    Generate 10 questions specifically about these UNCOVERED aspects of DELE:
    1. Exam format and structure
    2. Scoring system and interpretation  
    3. Preparation strategies and timeline
    
    Do NOT create questions about: definition, administration, or general purpose.
    """
    print("Aspect-focused prompt:")
    print(aspect_prompt)

def recommend_best_approach():
    """Recommend the best approach for the SkillTree system."""
    
    print(f"\n=== RECOMMENDATION FOR SKILLTREE SYSTEM ===")
    
    print(f"RECOMMENDED HYBRID APPROACH:")
    print(f"1. PRIMARY: Topic Aspect Targeting")
    print(f"   - Analyze existing 10 questions for coverage gaps")
    print(f"   - Target specific uncovered subtopics in new rounds")
    print(f"   - Natural diversity without heavy prompt engineering")
    
    print(f"\n2. SECONDARY: Difficulty Level Progression")
    print(f"   - Round 1: Basic questions (already generated)")
    print(f"   - Round 2: Intermediate questions") 
    print(f"   - Round 3: Advanced questions")
    print(f"   - Round 4: Application/scenario questions")
    
    print(f"\n3. BACKUP: Post-Generation Similarity Check")
    print(f"   - Quick similarity scan after generation")
    print(f"   - Flag questions >80% similar for manual review")
    print(f"   - Automatic retry if too many duplicates detected")
    
    print(f"\nWHY THIS APPROACH:")
    print(f"  + Low token overhead (no existing questions in prompts)")
    print(f"  + Educational value through systematic coverage")
    print(f"  + Scales well to large question banks")
    print(f"  + Maintains generation speed and reliability")
    print(f"  + Provides safety net through similarity detection")
    
    print(f"\nIMPLEMENTATION STEPS:")
    print(f"1. Create question analysis tool to identify coverage gaps")
    print(f"2. Design targeted prompts for uncovered aspects")
    print(f"3. Implement similarity detection as quality check")
    print(f"4. Test with 1-2 topics before full deployment")

def main():
    # Analyze existing questions
    questions = analyze_existing_questions()
    
    if questions:
        # Detect any existing similarities
        similarities = detect_similarities(questions)
    
    # Analyze prevention strategies
    analyze_duplicate_prevention_strategies()
    
    # Show practical examples
    demonstrate_prevention_techniques()
    
    # Provide recommendations
    recommend_best_approach()

if __name__ == "__main__":
    main()