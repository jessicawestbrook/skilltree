#!/usr/bin/env python3
"""
Generate content for a specific Spanish vocabulary topic.
"""

import os
import sys
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
from supabase import create_client

def find_spanish_topic():
    """Find a good Spanish vocabulary topic to process."""
    try:
        supabase_url = os.getenv('REACT_APP_SUPABASE_URL')
        supabase_key = os.getenv('REACT_APP_SUPABASE_ANON_KEY')
        supabase = create_client(supabase_url, supabase_key)
        
        print("Searching for Spanish vocabulary topics...")
        
        # Search for nodes with Spanish-related terms
        search_terms = ['spanish', 'family', 'colors', 'numbers', 'food', 'vocabulary', 'palabras']
        
        candidates = []
        for term in search_terms:
            response = supabase.table('skill_tree_nodes').select('*').ilike('name', f'%{term}%').eq('type', 'skill').eq('has_learning_content', False).execute()
            if response.data:
                candidates.extend(response.data)
        
        # Remove duplicates
        unique_candidates = []
        seen_ids = set()
        for node in candidates:
            if node['id'] not in seen_ids:
                unique_candidates.append(node)
                seen_ids.add(node['id'])
        
        print(f"Found {len(unique_candidates)} potential topics:")
        for i, node in enumerate(unique_candidates[:5]):
            print(f"  {i+1}. {node.get('name')}")
        
        if unique_candidates:
            # Pick the first one that looks like vocabulary
            vocab_keywords = ['family', 'colors', 'numbers', 'food', 'spanish', 'vocabulary']
            best_candidate = None
            
            for node in unique_candidates:
                name_lower = node.get('name', '').lower()
                if any(keyword in name_lower for keyword in vocab_keywords):
                    best_candidate = node
                    break
            
            if not best_candidate:
                best_candidate = unique_candidates[0]
            
            print(f"\nSelected topic: {best_candidate.get('name')}")
            return best_candidate
        
        return None
        
    except Exception as e:
        print(f"Error finding topic: {e}")
        return None

def process_node(node_data):
    """Process a single node with the content generator."""
    try:
        generator = LearningContentGenerator()
        
        # Convert database node to SkillTreeNode object
        node = SkillTreeNode(
            id=node_data['id'],
            name=node_data['name'],
            type=node_data['type'],
            path=node_data.get('path', ''),
            learning_area=node_data.get('learning_area', ''),
            has_learning_content=node_data.get('has_learning_content', False),
            learning_content_ids=node_data.get('learning_content_ids'),
            is_menu_leaf=node_data.get('is_menu_leaf', False),
            parent_id=node_data.get('parent_id'),
            metadata=node_data.get('metadata', {})
        )
        
        print(f"\nProcessing: {node.name}")
        print("=" * 50)
        
        # Generate content
        success = generator.process_single_node(node)
        
        if success:
            print(f"\nSUCCESS! Generated content for: {node.name}")
            print("- Created comprehensive learning content (10-30 minutes)")
            print("- Generated 50-100 multiple choice questions with explanations")
            print("- Saved everything to the database")
        else:
            print(f"\nFAILED to generate content for: {node.name}")
        
        return success
        
    except Exception as e:
        print(f"Error processing node: {e}")
        return False

def main():
    try:
        # Find a Spanish vocabulary topic
        spanish_node = find_spanish_topic()
        
        if not spanish_node:
            print("No suitable Spanish vocabulary topics found.")
            return
        
        # Confirm with estimated cost
        print(f"\nReady to generate content for: {spanish_node.get('name')}")
        print("Estimated cost: ~$0.11")
        print("This will create:")
        print("  - 10-30 minutes of learning content")
        print("  - 50-100 multiple choice questions")
        print("  - Detailed explanations for all answers")
        
        # Auto-proceed since user requested to start with Spanish vocabulary
        print("\nProceeding automatically...")
        print("Starting content generation...")
        
        # Process the node
        success = process_node(spanish_node)
        
        if success:
            print("\n" + "=" * 60)
            print("CONTENT GENERATION COMPLETE!")
            print("=" * 60)
            print(f"Successfully generated learning content for: {spanish_node.get('name')}")
            print("\nYou can now:")
            print("1. View the content in your SkillTree application")
            print("2. Test the questions and learning materials") 
            print("3. Process more topics if satisfied with the quality")
        else:
            print("\nContent generation failed. Check the logs above for details.")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()