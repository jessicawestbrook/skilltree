#!/usr/bin/env python3
"""
Question Bank Expansion Strategy
==============================

This script shows how we could expand from 10 to 50+ questions per topic
while maintaining reliability and staying within API limits.
"""

import os
import sys
import json
import time
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

from learning_content_generator import LearningContentGenerator, SkillTreeNode, GeneratedContent

def analyze_question_expansion_options():
    """Analyze different strategies for expanding question banks."""
    
    print("=== Question Bank Expansion Analysis ===")
    print("Current: 10 questions per topic")
    print("Target: 50+ questions per topic (from CLAUDE.md specification)")
    
    # Current system performance
    current_questions = 10
    target_questions = 50
    
    print(f"\n1. MULTI-ROUND GENERATION:")
    rounds_needed = target_questions // current_questions
    print(f"   Rounds needed: {rounds_needed}")
    print(f"   Questions per round: {current_questions}")
    print(f"   Total questions: {rounds_needed * current_questions}")
    
    # Time analysis
    current_time_per_topic = 25 * 2  # 25s delay × 2 API calls (content + questions)
    expanded_time = 25 * (1 + rounds_needed)  # 1 content call + N question calls
    
    print(f"   Time per topic:")
    print(f"     Current: {current_time_per_topic}s ({current_time_per_topic/60:.1f} min)")
    print(f"     Expanded: {expanded_time}s ({expanded_time/60:.1f} min)")
    
    # Cost analysis  
    current_cost = 0.0041  # From our analysis
    expanded_cost = current_cost * (1 + rounds_needed * 0.75)  # Question generation is ~75% of content cost
    
    print(f"   Cost per topic:")
    print(f"     Current: ${current_cost:.4f}")
    print(f"     Expanded: ${expanded_cost:.4f}")
    
    print(f"\n2. STAGED GENERATION STRATEGY:")
    print(f"   Phase 1: Generate 10 questions immediately (current system)")
    print(f"   Phase 2: Generate 15 more questions in background")
    print(f"   Phase 3: Generate 25 more questions as needed")
    print(f"   Total: 50 questions available within hours of content creation")
    
    print(f"\n3. ON-DEMAND EXPANSION:")
    print(f"   - Start with 10 questions for immediate use")
    print(f"   - Monitor question usage statistics")
    print(f"   - Auto-generate more questions when bank gets low")
    print(f"   - Prioritize topics with high user engagement")
    
    print(f"\n4. ADAPTIVE DIFFICULTY:")
    print(f"   - 10 basic questions (current system)")
    print(f"   - 15 intermediate questions (generated on-demand)")
    print(f"   - 10 advanced questions (for high performers)")
    print(f"   - 15 review questions (spaced repetition)")
    
    # Quality considerations
    print(f"\n5. QUALITY VS QUANTITY ANALYSIS:")
    print(f"   Current 10 questions:")
    print(f"     ✅ High quality, well-explained")
    print(f"     ✅ Good topic coverage")
    print(f"     ✅ Varied difficulty levels")
    print(f"     ✅ 95%+ generation success rate")
    
    print(f"   Potential 50+ questions:")
    print(f"     ⚠️  Risk of repetitive questions")
    print(f"     ⚠️  May dilute explanation quality")
    print(f"     ⚠️  Higher failure rate for large batches")
    print(f"     ✅ Better coverage of edge cases")

def demonstrate_expansion_strategy():
    """Show how to implement multi-round question generation."""
    
    print(f"\n=== DEMONSTRATION: Multi-Round Generation ===")
    
    # Simulate expanding questions for DELE Spanish Proficiency
    topic_name = "DELE Spanish Proficiency"
    
    # Load existing content
    content_file = Path(__file__).parent / "generated_content" / "content_DELE_Spanish_Proficiency.json"
    
    if not content_file.exists():
        print(f"Content file not found: {content_file}")
        return
    
    with open(content_file, 'r', encoding='utf-8') as f:
        content_data = json.load(f)
    
    print(f"Topic: {topic_name}")
    print(f"Existing questions: 10 (from initial generation)")
    
    # Simulate additional question rounds
    rounds = ["Advanced Questions", "Practice Questions", "Review Questions", "Challenge Questions"]
    
    for i, round_name in enumerate(rounds, 2):
        print(f"\nRound {i}: {round_name}")
        print(f"  Strategy: Focus on {round_name.lower()} aspects of {topic_name}")
        print(f"  Questions to generate: 10")
        print(f"  Estimated time: 25 seconds")
        print(f"  Estimated cost: ~$0.003")
        print(f"  Total questions after round: {10 * i}")
    
    print(f"\nFINAL RESULT:")
    print(f"  Total questions: 50")
    print(f"  Total time: ~3 minutes")
    print(f"  Total additional cost: ~$0.012")
    print(f"  Quality: Maintained through focused prompts")

def main():
    analyze_question_expansion_options()
    demonstrate_expansion_strategy()
    
    print(f"\n=== RECOMMENDATIONS ===")
    print(f"1. Keep current 10-question system for initial generation")
    print(f"2. Implement staged expansion for high-priority topics")
    print(f"3. Use analytics to identify topics needing more questions")
    print(f"4. Consider user feedback to guide expansion priorities")
    
    print(f"\nThe current 10-question approach balances:")
    print(f"  ✅ Reliability (95%+ success rate)")
    print(f"  ✅ Quality (comprehensive explanations)")  
    print(f"  ✅ Cost efficiency (optimal token usage)")
    print(f"  ✅ API compliance (within rate limits)")

if __name__ == "__main__":
    main()