#!/usr/bin/env python3
"""
Batch Description Generator
==========================

This script generates descriptions for categories in the skill tree database.
It focuses only on description generation and saves them to the database.

Usage:
    python batch_generate_descriptions.py --limit 10 --dry-run
    python batch_generate_descriptions.py --limit 20 --category "Finance"
"""

import os
import sys
import argparse
from enhanced_content_generator import EnhancedContentGenerator

# Load environment variables from .env.local
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env.local'))
except ImportError:
    print("Warning: python-dotenv not available. Please ensure environment variables are set manually.")

def main():
    """Main function for batch description generation."""
    parser = argparse.ArgumentParser(description='Generate descriptions for skill tree categories')
    parser.add_argument('--limit', type=int, default=5, help='Number of categories to process (default: 5)')
    parser.add_argument('--dry-run', action='store_true', help='Test run without saving to database')
    parser.add_argument('--category', type=str, help='Specific category name to process')
    
    args = parser.parse_args()
    
    print("Batch Description Generator")
    print("=" * 50)
    print(f"Limit: {args.limit}")
    print(f"Dry run: {args.dry_run}")
    if args.category:
        print(f"Specific category: {args.category}")
    print()
    
    try:
        generator = EnhancedContentGenerator()
        
        if args.category:
            # Process specific category
            print(f"Searching for category: {args.category}")
            
            # Search for the specific category
            response = generator.supabase.table('skill_tree_nodes').select('*').eq('type', 'category').ilike('name', f'%{args.category}%').execute()
            
            if not response.data:
                print(f"No category found matching: {args.category}")
                return
            
            categories = []
            for row in response.data:
                from enhanced_content_generator import SkillTreeNode
                node = SkillTreeNode(
                    id=row['id'],
                    name=row['name'],
                    type=row['type'],
                    path=row['path'],
                    learning_area=row['learning_area'],
                    has_learning_content=row['has_learning_content'],
                    learning_content_ids=row['learning_content_ids'],
                    is_menu_leaf=row['is_menu_leaf'],
                    description=row.get('description'),
                    parent_id=row['parent_id'],
                    metadata=row['metadata']
                )
                categories.append(node)
        else:
            # Get categories without descriptions
            categories = generator.get_categories_without_descriptions(limit=args.limit)
        
        if not categories:
            print("No categories found to process.")
            if not args.category:
                print("All categories may already have descriptions.")
            return
        
        print(f"Found {len(categories)} categories to process:")
        for i, cat in enumerate(categories, 1):
            existing_desc = "[Has description]" if cat.description else "[No description]"
            print(f"  {i}. {cat.name} {existing_desc}")
            print(f"     Path: {cat.path}")
        
        if args.dry_run:
            print("\n*** DRY RUN MODE - No database changes will be made ***")
        
        print(f"\nStarting description generation...")
        print("Note: 25-second delays between API calls for rate limiting compliance")
        print()
        
        success_count = 0
        for i, category in enumerate(categories, 1):
            print(f"\n[{i}/{len(categories)}] Processing: {category.name}")
            
            if args.dry_run:
                # Generate description but don't save
                description = generator.generate_category_description(category)
                if description:
                    print(f"SUCCESS - Generated description: {description.description}")
                    print(f"Focus areas: {', '.join(description.focus_areas)}")
                    success_count += 1
                else:
                    print("FAILED - Could not generate description")
            else:
                # Full processing with database save
                success = generator.process_single_node(
                    category, 
                    generate_description=True, 
                    generate_content=False  # Only descriptions
                )
                
                if success:
                    success_count += 1
        
        print(f"\n{'='*50}")
        print(f"Processing Summary:")
        print(f"  Total processed: {len(categories)}")
        print(f"  Successful: {success_count}")
        print(f"  Failed: {len(categories) - success_count}")
        
        if args.dry_run:
            print(f"\n*** Dry run completed - no database changes made ***")
        else:
            print(f"\n*** Processing completed - descriptions saved to database ***")
        
    except Exception as e:
        print(f"ERROR - Failed to initialize generator: {e}")
        print("\nPlease ensure:")
        print("1. ANTHROPIC_API_KEY is set in your environment")
        print("2. Supabase credentials are configured in .env.local")
        print("3. Description column has been added to skill_tree_nodes table")
        
        if "description" in str(e).lower():
            print("\nTo add the description column, please execute this SQL in your Supabase dashboard:")
            print("ALTER TABLE skill_tree_nodes ADD COLUMN description TEXT;")

if __name__ == "__main__":
    main()