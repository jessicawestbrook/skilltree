#!/usr/bin/env python3
"""
Test script for the Learning Content Generator
============================================

This script tests the content generator functionality with a small sample
to validate that everything works before running large batches.
"""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from learning_content_generator import LearningContentGenerator, SkillTreeNode, GeneratedContent, GeneratedQuestion


def test_api_connection():
    """Test basic API connectivity."""
    print("Testing API connections...")
    
    try:
        generator = LearningContentGenerator()
        print("✅ Successfully initialized generator with API keys")
        return True
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_database_connection():
    """Test database connectivity."""
    print("Testing database connection...")
    
    try:
        generator = LearningContentGenerator()
        
        # Try to load skill tree nodes
        nodes = generator.load_skill_tree_nodes()
        print(f"✅ Successfully connected to database, found {len(nodes)} skill tree nodes")
        return True, nodes
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False, []


def test_content_generation():
    """Test learning content generation with a sample node."""
    print("Testing content generation...")
    
    try:
        generator = LearningContentGenerator()
        
        # Create a test node
        test_node = SkillTreeNode(
            id="test-node-1",
            name="Basic Algebra",
            type="leaf",
            path="/Mathematics/Algebra/Basic Algebra",
            learning_area="Mathematics",
            has_learning_content=False,
            learning_content_ids=None,
            is_menu_leaf=True
        )
        
        print(f"Generating content for test node: {test_node.name}")
        content = generator.generate_learning_content(test_node)
        
        if content:
            print("✅ Successfully generated learning content")
            print(f"   Title: {content.title}")
            print(f"   Length: {len(content.content)} characters")
            print(f"   Estimated time: {content.estimated_time_minutes} minutes")
            print(f"   Difficulty: {content.difficulty_level}")
            print(f"   Content preview: {content.content[:200]}...")
            return True, content
        else:
            print("❌ Failed to generate learning content")
            return False, None
            
    except Exception as e:
        print(f"❌ Content generation error: {e}")
        return False, None


def test_question_generation(content):
    """Test question generation with sample content."""
    print("Testing question generation...")
    
    try:
        generator = LearningContentGenerator()
        
        # Create a test node for context
        test_node = SkillTreeNode(
            id="test-node-1",
            name="Basic Algebra",
            type="leaf",
            path="/Mathematics/Algebra/Basic Algebra",
            learning_area="Mathematics",
            has_learning_content=False,
            learning_content_ids=None,
            is_menu_leaf=True
        )
        
        print(f"Generating questions for: {content.title}")
        questions = generator.generate_questions(test_node, content)
        
        if questions:
            print(f"✅ Successfully generated {len(questions)} questions")
            
            # Show sample questions
            for i, q in enumerate(questions[:3]):  # Show first 3 questions
                print(f"\n   Question {i+1}: {q.question_text}")
                print(f"   Options: {q.options}")
                print(f"   Correct: {q.correct_answer} ({q.options[q.correct_answer]})")
                print(f"   Difficulty: {q.difficulty}")
                print(f"   Explanation: {q.explanation[:100]}...")
            
            if len(questions) > 3:
                print(f"\n   ... and {len(questions) - 3} more questions")
                
            return True, questions
        else:
            print("❌ Failed to generate questions")
            return False, []
            
    except Exception as e:
        print(f"❌ Question generation error: {e}")
        return False, []


def test_database_operations():
    """Test database save operations without actually saving."""
    print("Testing database operations (dry run)...")
    
    try:
        generator = LearningContentGenerator()
        
        # Test database table access
        response = generator.supabase.table('skill_tree_nodes').select('id, name').limit(1).execute()
        if response.data:
            print("✅ Can read from skill_tree_nodes table")
        else:
            print("⚠️  skill_tree_nodes table is empty")
        
        response = generator.supabase.table('learning_content').select('id').limit(1).execute()
        print("✅ Can access learning_content table")
        
        response = generator.supabase.table('questions').select('id').limit(1).execute()
        print("✅ Can access questions table")
        
        return True
        
    except Exception as e:
        print(f"❌ Database operations error: {e}")
        return False


def test_cost_estimation():
    """Test cost estimation functionality."""
    print("Testing cost estimation...")
    
    try:
        generator = LearningContentGenerator()
        
        # Test with different node counts
        for node_count in [1, 10, 100]:
            estimate = generator.estimate_costs(node_count)
            print(f"✅ Cost estimate for {node_count} nodes:")
            print(f"   Total cost: ${estimate['total_cost']:.2f}")
            print(f"   Input tokens: {estimate['total_input_tokens']:,}")
            print(f"   Output tokens: {estimate['total_output_tokens']:,}")
        
        return True
        
    except Exception as e:
        print(f"❌ Cost estimation error: {e}")
        return False


def run_full_test():
    """Run complete test suite."""
    print("=" * 60)
    print("LEARNING CONTENT GENERATOR TEST SUITE")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: API Connection
    if test_api_connection():
        tests_passed += 1
    print()
    
    # Test 2: Database Connection
    db_success, nodes = test_database_connection()
    if db_success:
        tests_passed += 1
    print()
    
    # Test 3: Content Generation
    content_success, sample_content = test_content_generation()
    if content_success:
        tests_passed += 1
    print()
    
    # Test 4: Question Generation (only if content generation worked)
    if content_success and sample_content:
        questions_success, sample_questions = test_question_generation(sample_content)
        if questions_success:
            tests_passed += 1
    else:
        print("Skipping question generation test (content generation failed)")
        total_tests -= 1
    print()
    
    # Test 5: Database Operations
    if test_database_operations():
        tests_passed += 1
    print()
    
    # Test 6: Cost Estimation
    if test_cost_estimation():
        tests_passed += 1
    print()
    
    # Summary
    print("=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    print(f"Success rate: {tests_passed/total_tests*100:.1f}%")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The generator is ready for use.")
        
        if db_success and nodes:
            filtered_nodes = [
                node for node in nodes 
                if hasattr(node, 'is_menu_leaf') and node.get('is_menu_leaf') 
                and not node.get('has_learning_content', False)
            ]
            print(f"\nFound {len(filtered_nodes)} nodes ready for content generation.")
            
            if len(filtered_nodes) > 0:
                estimate = LearningContentGenerator().estimate_costs(len(filtered_nodes))
                print(f"Full processing would cost approximately ${estimate['total_cost']:.2f}")
                print(f"Consider starting with --max-nodes 5 for initial testing")
    else:
        print("⚠️  Some tests failed. Please fix issues before running full batch processing.")
        print("\nTroubleshooting tips:")
        print("- Verify ANTHROPIC_API_KEY is set and valid")
        print("- Check REACT_APP_SUPABASE_URL and REACT_APP_SUPABASE_ANON_KEY")
        print("- Ensure database tables exist with correct schema")
        print("- Check network connectivity")
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the learning content generator")
    parser.add_argument('--test', choices=['api', 'db', 'content', 'questions', 'cost', 'all'],
                       default='all', help="Which test to run")
    
    args = parser.parse_args()
    
    if args.test == 'all':
        run_full_test()
    elif args.test == 'api':
        test_api_connection()
    elif args.test == 'db':
        test_database_connection()
    elif args.test == 'content':
        test_content_generation()
    elif args.test == 'cost':
        test_cost_estimation()
    else:
        print(f"Running {args.test} test...")
        # Add individual test calls as needed


if __name__ == "__main__":
    main()