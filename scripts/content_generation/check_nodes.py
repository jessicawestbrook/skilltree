#!/usr/bin/env python3
"""
Quick check of skill tree nodes to understand the data structure.
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
        
        print("Analyzing skill tree nodes...")
        
        # Get overall stats
        response = supabase.table('skill_tree_nodes').select('*', count='exact').execute()
        total_nodes = response.count
        print(f"Total nodes: {total_nodes}")
        
        # Check node types
        response = supabase.table('skill_tree_nodes').select('type').execute()
        types = {}
        for node in response.data:
            node_type = node.get('type', 'unknown')
            types[node_type] = types.get(node_type, 0) + 1
        
        print(f"\nNode types:")
        for type_name, count in types.items():
            print(f"  {type_name}: {count}")
        
        # Check leaf nodes
        response = supabase.table('skill_tree_nodes').select('*').eq('is_menu_leaf', True).execute()
        leaf_nodes = len(response.data) if response.data else 0
        print(f"\nLeaf nodes (is_menu_leaf=true): {leaf_nodes}")
        
        # Check nodes with content
        response = supabase.table('skill_tree_nodes').select('*').eq('has_learning_content', True).execute()
        nodes_with_content = len(response.data) if response.data else 0
        print(f"Nodes with learning content: {nodes_with_content}")
        
        # Check nodes that need content
        response = supabase.table('skill_tree_nodes').select('*').eq('is_menu_leaf', True).eq('has_learning_content', False).execute()
        nodes_needing_content = len(response.data) if response.data else 0
        print(f"Leaf nodes needing content: {nodes_needing_content}")
        
        # Show some example nodes that need content
        if response.data and len(response.data) > 0:
            print(f"\nFirst 5 nodes that need content:")
            for i, node in enumerate(response.data[:5]):
                print(f"  {i+1}. {node.get('name')} (Path: {node.get('path')})")
        
        # Alternative: check nodes by type 'leaf'
        response = supabase.table('skill_tree_nodes').select('*').eq('type', 'leaf').eq('has_learning_content', False).execute()
        type_leaf_nodes = len(response.data) if response.data else 0
        print(f"\nType 'leaf' nodes needing content: {type_leaf_nodes}")
        
        if response.data and len(response.data) > 0:
            print(f"\nFirst 5 'leaf' type nodes that need content:")
            for i, node in enumerate(response.data[:5]):
                print(f"  {i+1}. {node.get('name')} (Path: {node.get('path')})")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()