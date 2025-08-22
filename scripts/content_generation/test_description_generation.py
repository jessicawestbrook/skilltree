#!/usr/bin/env python3
"""
Test Script for Description Generation
=====================================

This script tests the description generation functionality
before running it on the full database.
"""

import os
import sys
from enhanced_content_generator import EnhancedContentGenerator, SkillTreeNode

# Load environment variables from .env.local
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env.local'))
except ImportError:
    print("Warning: python-dotenv not available. Please ensure environment variables are set manually.")

def test_description_generation():
    """Test description generation with sample data."""
    print("Testing Description Generation")
    print("=" * 40)
    
    try:
        generator = EnhancedContentGenerator()
        
        # Create test nodes
        test_nodes = [
            SkillTreeNode(
                id="test-1",
                name="Finance",
                type="category",
                path="Applied Sciences/Business/Finance",
                learning_area="Business",
                has_learning_content=True,
                learning_content_ids=None,
                is_menu_leaf=False
            ),
            SkillTreeNode(
                id="test-2", 
                name="Mathematics",
                type="category",
                path="Formal Sciences/Mathematics",
                learning_area="Formal Sciences",
                has_learning_content=True,
                learning_content_ids=None,
                is_menu_leaf=False
            ),
            SkillTreeNode(
                id="test-3",
                name="Spanish Language",
                type="category", 
                path="Languages/Romance Languages/Spanish",
                learning_area="Languages",
                has_learning_content=True,
                learning_content_ids=None,
                is_menu_leaf=False
            )
        ]
        
        print(f"Testing description generation for {len(test_nodes)} categories...\n")
        
        for i, node in enumerate(test_nodes, 1):
            print(f"Test {i}: {node.name}")
            print(f"Path: {node.path}")
            print("-" * 30)
            
            # Generate description
            description = generator.generate_category_description(node)
            
            if description:
                print(f"SUCCESS - Description: {description.description}")
                print(f"Focus Areas: {', '.join(description.focus_areas)}")
                print(f"Difficulty: {description.difficulty_level}")
            else:
                print("FAILED - Failed to generate description")
            
            print("\n" + "="*50 + "\n")
        
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"ERROR - Test failed: {e}")
        print("\nPlease ensure:")
        print("1. ANTHROPIC_API_KEY is set in your environment")
        print("2. You have internet connectivity")

if __name__ == "__main__":
    test_description_generation()