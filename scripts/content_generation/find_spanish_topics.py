#!/usr/bin/env python3
"""
Find Spanish vocabulary topics in the skill tree.
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

from supabase import create_client

def main():
    try:
        supabase_url = os.getenv('REACT_APP_SUPABASE_URL')
        supabase_key = os.getenv('REACT_APP_SUPABASE_ANON_KEY')
        
        supabase = create_client(supabase_url, supabase_key)
        
        print("Searching for Spanish-related topics...")
        
        # Search for Spanish topics in skill nodes
        response = supabase.table('skill_tree_nodes').select('*').ilike('name', '%spanish%').execute()
        spanish_nodes = response.data or []
        
        print(f"\nFound {len(spanish_nodes)} Spanish-related nodes:")
        for i, node in enumerate(spanish_nodes):
            status = "✅ Has content" if node.get('has_learning_content') else "❌ Needs content"
            print(f"  {i+1}. {node.get('name')} - Type: {node.get('type')} - {status}")
            if node.get('path'):
                print(f"      Path: {node.get('path')}")
        
        # Also search for vocabulary-related terms
        print(f"\nSearching for vocabulary-related topics...")
        vocab_terms = ['vocabulary', 'vocab', 'palabras', 'words', 'family', 'colors', 'numbers', 'food']
        
        vocab_nodes = []
        for term in vocab_terms:
            response = supabase.table('skill_tree_nodes').select('*').ilike('name', f'%{term}%').execute()
            if response.data:
                vocab_nodes.extend(response.data)
        
        # Remove duplicates and filter for skill type
        unique_vocab = []
        seen_ids = set()
        for node in vocab_nodes:
            if node['id'] not in seen_ids and node.get('type') == 'skill' and not node.get('has_learning_content'):
                unique_vocab.append(node)
                seen_ids.add(node['id'])
        
        print(f"\nFound {len(unique_vocab)} vocabulary-related skill nodes that need content:")
        for i, node in enumerate(unique_vocab[:10]):  # Show first 10
            print(f"  {i+1}. {node.get('name')}")
            if node.get('path'):
                print(f"      Path: {node.get('path')}")
        
        if len(unique_vocab) > 10:
            print(f"  ... and {len(unique_vocab) - 10} more")
        
        # Find the best Spanish vocabulary candidate
        spanish_vocab_candidates = [
            node for node in unique_vocab 
            if any(term in node.get('name', '').lower() for term in ['spanish', 'familia', 'colores', 'números'])
        ]
        
        if not spanish_vocab_candidates:
            # If no specifically Spanish ones, look for generic vocabulary that could be Spanish
            spanish_vocab_candidates = [
                node for node in unique_vocab 
                if any(term in node.get('name', '').lower() for term in ['family', 'colors', 'numbers', 'food', 'vocabulary'])
            ][:3]  # Take first 3
        
        if spanish_vocab_candidates:
            print(f"\n🎯 Recommended Spanish vocabulary topics to generate content for:")
            for i, node in enumerate(spanish_vocab_candidates[:3]):
                print(f"  {i+1}. {node.get('name')} (ID: {node.get('id')})")
                if node.get('path'):
                    print(f"      Path: {node.get('path')}")
            
            # Return the first candidate for processing
            return spanish_vocab_candidates[0]
        else:
            print("\n❌ No suitable Spanish vocabulary topics found")
            return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    main()