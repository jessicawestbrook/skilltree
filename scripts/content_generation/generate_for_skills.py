#!/usr/bin/env python3
"""
Generate content for skill-type nodes instead of is_menu_leaf nodes.
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

from learning_content_generator import LearningContentGenerator

def main():
    try:
        generator = LearningContentGenerator()
        
        # Override the filter function to use 'skill' type nodes
        def custom_filter_nodes(nodes):
            """Filter nodes that need content generation - use 'skill' type instead of is_menu_leaf."""
            filtered = [
                node for node in nodes 
                if node.type == 'skill'  # Changed from is_menu_leaf to type == 'skill'
                and not node.has_learning_content
                and not (node.learning_content_ids and len(node.learning_content_ids) > 0)
            ]
            
            print(f"Filtered to {len(filtered)} 'skill' type nodes needing content generation")
            return filtered
        
        # Replace the method
        generator.filter_nodes_for_processing = custom_filter_nodes
        
        # Get cost estimate
        all_nodes = generator.load_skill_tree_nodes()
        nodes_to_process = generator.filter_nodes_for_processing(all_nodes)
        
        if not nodes_to_process:
            print("No skill nodes found that need content generation")
            return
        
        print(f"\nFound {len(nodes_to_process)} skill nodes that need content:")
        for i, node in enumerate(nodes_to_process[:5]):  # Show first 5
            print(f"  {i+1}. {node.name} (Path: {node.path})")
        
        if len(nodes_to_process) > 5:
            print(f"  ... and {len(nodes_to_process) - 5} more")
        
        # Get cost estimate
        cost_estimate = generator.estimate_costs(len(nodes_to_process))
        print(f"\nCost estimate for {len(nodes_to_process)} skill nodes:")
        print(f"  Total cost: ${cost_estimate['total_cost']:.2f}")
        print(f"  Input tokens: {cost_estimate['total_input_tokens']:,}")
        print(f"  Output tokens: {cost_estimate['total_output_tokens']:,}")
        
        print(f"\nTo generate content for these nodes, run:")
        print(f"python scripts/content_generation/generate_for_skills.py --process --max-nodes 5")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate content for skill-type nodes")
    parser.add_argument('--process', action='store_true', help="Actually process nodes (not just estimate)")
    parser.add_argument('--max-nodes', type=int, default=5, help="Maximum nodes to process")
    
    args = parser.parse_args()
    
    if args.process:
        try:
            generator = LearningContentGenerator()
            
            # Override the filter function
            def custom_filter_nodes(nodes):
                filtered = [
                    node for node in nodes 
                    if node.type == 'skill'
                    and not node.has_learning_content
                    and not (node.learning_content_ids and len(node.learning_content_ids) > 0)
                ]
                return filtered
            
            generator.filter_nodes_for_processing = custom_filter_nodes
            
            # Run processing
            generator.run_batch_processing(max_nodes=args.max_nodes, resume=True)
            
        except Exception as e:
            print(f"Error during processing: {e}")
    else:
        main()