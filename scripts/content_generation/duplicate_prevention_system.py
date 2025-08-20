#!/usr/bin/env python3
"""
Question Duplicate Prevention System
==================================

Comprehensive system to prevent duplicate questions when expanding question banks.
"""

import os
import sys
import json
import difflib
from pathlib import Path
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

@dataclass
class ExistingQuestion:
    text: str
    topic: str
    difficulty: str
    concepts: List[str]  # Key concepts covered
    
class QuestionDuplicateChecker:
    def __init__(self):
        self.existing_questions: List[ExistingQuestion] = []
        self.similarity_threshold = 0.75  # 75% similarity = potential duplicate
        
    def load_existing_questions(self, content_dir: Path) -> int:
        """Load existing questions from generated files."""
        question_files = list(content_dir.glob("questions_*.json"))
        
        for file in question_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    topic_name = data.get('topic_name', file.stem)
                    
                    for q in data.get('questions', []):
                        question = ExistingQuestion(
                            text=q.get('question_text', ''),
                            topic=topic_name,
                            difficulty=q.get('difficulty', 'unknown'),
                            concepts=self._extract_concepts(q.get('question_text', ''))
                        )
                        self.existing_questions.append(question)
            except Exception as e:
                print(f"Error loading {file}: {e}")
        
        return len(self.existing_questions)
    
    def _extract_concepts(self, question_text: str) -> List[str]:
        """Extract key concepts from question text."""
        # Simple concept extraction - can be enhanced
        concepts = []
        text_lower = question_text.lower()
        
        # Common question patterns
        if "what does" in text_lower and "stand for" in text_lower:
            concepts.append("acronym_definition")
        elif "who" in text_lower and ("administers" in text_lower or "manages" in text_lower):
            concepts.append("administration")
        elif "how" in text_lower and "pronounced" in text_lower:
            concepts.append("pronunciation")
        elif "which" in text_lower and "levels" in text_lower:
            concepts.append("levels_classification")
        elif "purpose" in text_lower or "why" in text_lower:
            concepts.append("purpose_goals")
        
        return concepts
    
    def check_similarity(self, new_question: str) -> List[Tuple[float, ExistingQuestion]]:
        """Check similarity of new question against existing ones."""
        similarities = []
        
        for existing in self.existing_questions:
            similarity = difflib.SequenceMatcher(
                None, 
                new_question.lower().strip(), 
                existing.text.lower().strip()
            ).ratio()
            
            if similarity >= self.similarity_threshold:
                similarities.append((similarity, existing))
        
        return sorted(similarities, key=lambda x: x[0], reverse=True)
    
    def analyze_coverage_gaps(self, topic: str) -> Dict[str, List[str]]:
        """Analyze what aspects of a topic are not yet covered."""
        topic_questions = [q for q in self.existing_questions if q.topic == topic]
        
        # Define comprehensive coverage areas by topic
        topic_coverage_map = {
            "DELE Spanish Proficiency": [
                "acronym_definition", "administration", "purpose_goals", 
                "exam_structure", "scoring_system", "preparation_strategies",
                "difficulty_levels", "time_requirements", "cost_fees",
                "recognition_value", "comparison_other_exams", "practical_applications"
            ],
            "Spanish Alphabet": [
                "vowel_pronunciation", "consonant_pronunciation", "letter_names",
                "alphabet_size", "special_characters", "pronunciation_rules",
                "spelling_patterns", "accent_marks", "capitalization",
                "handwriting_differences", "regional_variations", "etymology"
            ],
            "Mexican Spanish": [
                "vocabulary_differences", "pronunciation_variations", "cultural_context",
                "regional_dialects", "grammar_differences", "formal_informal",
                "indigenous_influences", "historical_development", "slang_expressions",
                "comparison_spain_spanish", "learning_resources", "cultural_etiquette"
            ]
        }
        
        all_concepts = topic_coverage_map.get(topic, [])
        covered_concepts = set()
        
        for q in topic_questions:
            covered_concepts.update(q.concepts)
        
        uncovered = [concept for concept in all_concepts if concept not in covered_concepts]
        
        return {
            "covered": list(covered_concepts),
            "uncovered": uncovered,
            "total_possible": len(all_concepts),
            "coverage_percentage": len(covered_concepts) / len(all_concepts) * 100 if all_concepts else 0
        }
    
    def generate_targeted_prompt(self, topic: str, target_aspects: List[str], difficulty: str = "mixed") -> str:
        """Generate a targeted prompt to avoid duplicates."""
        
        # Get existing question texts for this topic
        topic_questions = [q.text for q in self.existing_questions if q.topic == topic]
        
        # Create aspect descriptions
        aspect_descriptions = {
            "exam_structure": "exam format, sections, time limits, question types",
            "scoring_system": "how exams are scored, grade interpretation, pass/fail criteria",
            "preparation_strategies": "study methods, timeline, resources, tips",
            "difficulty_levels": "different proficiency levels, progression, requirements",
            "pronunciation_rules": "specific pronunciation guidelines, exceptions, regional differences",
            "cultural_context": "cultural background, social usage, historical significance",
            "practical_applications": "real-world uses, career benefits, academic value"
        }
        
        aspect_details = [aspect_descriptions.get(aspect, aspect) for aspect in target_aspects]
        
        prompt = f"""Generate 10 multiple choice questions about {topic}.

IMPORTANT: Focus ONLY on these specific aspects:
{chr(10).join(f'- {detail}' for detail in aspect_details)}

AVOID creating questions similar to these patterns (we already have questions covering these):
{chr(10).join(f'- Questions about: {self._categorize_question(q)}' for q in topic_questions[:5])}

Requirements:
- Each question should test understanding of the specified aspects above
- Provide 4 multiple choice options (A, B, C, D)
- Include detailed explanations for correct answers
- Mix difficulty levels: {difficulty}
- Questions should be educationally distinct from existing ones

Return ONLY valid JSON in this format:
{{
    "questions": [
        {{
            "question_text": "Question here?",
            "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
            "correct_answer": 0,
            "explanation": "Detailed explanation here",
            "difficulty": "easy|medium|hard"
        }}
    ]
}}"""
        
        return prompt
    
    def _categorize_question(self, question_text: str) -> str:
        """Categorize what a question is about."""
        text_lower = question_text.lower()
        
        if "stand for" in text_lower or "acronym" in text_lower:
            return "acronyms/definitions"
        elif "administers" in text_lower or "organization" in text_lower:
            return "administration/management"  
        elif "pronounced" in text_lower or "pronunciation" in text_lower:
            return "pronunciation rules"
        elif "purpose" in text_lower or "why" in text_lower:
            return "purposes/goals"
        elif "levels" in text_lower or "difficulty" in text_lower:
            return "levels/classification"
        else:
            return "general concepts"
    
    def validate_new_questions(self, new_questions: List[Dict], topic: str) -> Dict:
        """Validate new questions for duplicates and quality."""
        results = {
            "total_questions": len(new_questions),
            "duplicates_found": [],
            "high_similarity": [],
            "approved_questions": [],
            "coverage_analysis": {}
        }
        
        for i, q in enumerate(new_questions):
            question_text = q.get('question_text', '')
            
            # Check for exact or near duplicates
            similarities = self.check_similarity(question_text)
            
            if similarities:
                highest_sim = similarities[0]
                if highest_sim[0] > 0.9:  # >90% similarity
                    results["duplicates_found"].append({
                        "question_index": i,
                        "question": question_text[:100] + "...",
                        "duplicate_of": highest_sim[1].text[:100] + "...",
                        "similarity": highest_sim[0]
                    })
                elif highest_sim[0] > self.similarity_threshold:  # >75% similarity
                    results["high_similarity"].append({
                        "question_index": i,
                        "question": question_text[:100] + "...",
                        "similar_to": highest_sim[1].text[:100] + "...",
                        "similarity": highest_sim[0]
                    })
                else:
                    results["approved_questions"].append(q)
            else:
                results["approved_questions"].append(q)
        
        # Analyze coverage improvement
        results["coverage_analysis"] = self.analyze_coverage_gaps(topic)
        
        return results

def demonstrate_duplicate_prevention():
    """Demonstrate the duplicate prevention system."""
    
    print("=== Question Duplicate Prevention System Demo ===")
    
    # Initialize checker
    checker = QuestionDuplicateChecker()
    
    # Load existing questions
    content_dir = Path(__file__).parent / "generated_content"
    loaded_count = checker.load_existing_questions(content_dir)
    print(f"Loaded {loaded_count} existing questions")
    
    # Analyze coverage for each topic
    topics = ["DELE Spanish Proficiency", "Spanish Alphabet", "Mexican Spanish"]
    
    for topic in topics:
        print(f"\n--- {topic} Coverage Analysis ---")
        coverage = checker.analyze_coverage_gaps(topic)
        
        print(f"Coverage: {coverage['coverage_percentage']:.1f}%")
        print(f"Covered aspects: {', '.join(coverage['covered'])}")
        print(f"Uncovered aspects: {', '.join(coverage['uncovered'][:3])}...")
        
        # Generate targeted prompt
        if coverage['uncovered']:
            target_aspects = coverage['uncovered'][:3]  # Target top 3 uncovered
            prompt = checker.generate_targeted_prompt(topic, target_aspects)
            print(f"Next generation should target: {', '.join(target_aspects)}")
    
    # Test similarity detection
    print(f"\n--- Similarity Detection Test ---")
    test_questions = [
        "What does DELE stand for in Spanish language testing?",  # Very similar to existing
        "How many difficulty levels are there in DELE exams?",    # New aspect
        "What is the cost structure for DELE examinations?"       # Completely new
    ]
    
    for test_q in test_questions:
        similarities = checker.check_similarity(test_q)
        if similarities:
            highest = similarities[0]
            print(f"Question: '{test_q[:50]}...'")
            print(f"  Similarity: {highest[0]:.1%} to existing question")
            print(f"  Status: {'DUPLICATE' if highest[0] > 0.9 else 'SIMILAR' if highest[0] > 0.75 else 'UNIQUE'}")
        else:
            print(f"Question: '{test_q[:50]}...'")
            print(f"  Status: UNIQUE")
    
    print(f"\n=== RECOMMENDATION ===")
    print(f"1. Use coverage gap analysis to target uncovered aspects")
    print(f"2. Generate questions with targeted prompts focusing on new aspects") 
    print(f"3. Run similarity detection on generated questions")
    print(f"4. Filter out questions >75% similar to existing ones")
    print(f"5. Manual review for questions 75-90% similar")

if __name__ == "__main__":
    demonstrate_duplicate_prevention()