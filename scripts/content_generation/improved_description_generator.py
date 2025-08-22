#!/usr/bin/env python3
"""
Improved Description Generator for SkillTree Categories
======================================================

This script regenerates descriptions for all 2nd and 3rd level categories
with improved prompts that avoid false assumptions about:
- Hands-on learning (this is an online platform)
- Professional career outcomes (users won't become professionals from this site)
- Physical activities or materials
- Direct application to careers

Instead focuses on:
- Knowledge and understanding
- Conceptual learning
- Theoretical foundations
- Academic study
"""

import os
import sys
import json
import time
import csv
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import anthropic
from supabase import create_client, Client

# Load environment variables
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env.local'))
except ImportError:
    print("Warning: python-dotenv not available. Please ensure environment variables are set manually.")

@dataclass
class SkillTreeNode:
    """Represents a skill tree node from the database."""
    id: str
    name: str
    type: str
    path: List[str]
    learning_area: str
    has_learning_content: bool
    learning_content_ids: Optional[List[str]]
    is_menu_leaf: bool
    description: Optional[str] = None
    parent_id: Optional[str] = None
    metadata: Optional[Dict] = None

@dataclass
class ImprovedDescription:
    """Represents an improved category description."""
    description: str
    focus_areas: List[str]
    difficulty_level: str

class ImprovedDescriptionGenerator:
    """Generates improved descriptions avoiding false assumptions."""
    
    def __init__(self, anthropic_api_key: str = None, supabase_url: str = None, supabase_key: str = None):
        """Initialize the improved description generator with API clients."""
        # Initialize Anthropic client
        self.anthropic_api_key = anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
        
        # Initialize Supabase client
        self.supabase_url = supabase_url or os.getenv('REACT_APP_SUPABASE_URL')
        self.supabase_key = supabase_key or os.getenv('SUPABASE_SERVICE_ROLE_KEY') or os.getenv('REACT_APP_SUPABASE_ANON_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase credentials are required")
            
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        
        # Rate limiting configuration
        self.api_delay = 25  # 25 seconds between API calls for rate limit compliance
        
        # Progress tracking
        self.processed_count = 0
        self.success_count = 0
        self.error_count = 0
        
    def log_progress(self, message: str):
        """Log progress with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def determine_subject_context(self, node: SkillTreeNode) -> str:
        """Determine the subject context for better description generation."""
        if not node.path or len(node.path) < 2:
            return "academic study and conceptual understanding"
        
        # Use the top-level category to determine context
        top_level = node.path[0].lower()
        
        context_map = {
            'academic disciplines': 'academic study and theoretical understanding',
            'sciences': 'scientific concepts, theories, and principles',
            'mathematics': 'mathematical concepts, theories, and problem-solving methods',
            'languages': 'language study, linguistic concepts, and communication principles',
            'humanities': 'humanities concepts, cultural understanding, and analytical thinking',
            'creative skills': 'creative concepts, artistic principles, and design theory',
            'professional skills': 'business concepts, organizational theory, and analytical frameworks',
            'test preparation': 'test concepts, academic skills, and analytical methods',
            'life skills': 'conceptual knowledge and theoretical understanding',
            'technology': 'technological concepts, digital principles, and computational thinking',
            'applied sciences': 'applied concepts, theoretical frameworks, and analytical methods'
        }
        
        return context_map.get(top_level, 'academic study and conceptual understanding')

    def get_subject_specific_guidance(self, node: SkillTreeNode) -> str:
        """Get specific guidance for different subject areas."""
        if not node.path or len(node.path) < 1:
            return "Focus on the unique concepts and knowledge specific to this subject area."
        
        category = node.name.lower()
        path_str = ' > '.join(node.path).lower()
        
        # Business and Economics
        if 'business' in path_str or 'economics' in path_str:
            if 'finance' in category:
                return "Focus on financial concepts like investment analysis, risk assessment, portfolio theory, market dynamics, and capital management principles."
            elif 'marketing' in category:
                return "Focus on consumer behavior analysis, market segmentation, brand positioning, pricing strategies, and promotional methods."
            elif 'operations' in category:
                return "Focus on supply chain principles, process optimization, quality management systems, inventory control, and production planning."
            elif 'entrepreneur' in category:
                return "Focus on business model development, startup financing, market opportunity analysis, and venture creation processes."
            else:
                return "Focus on specific business concepts, economic theories, organizational behavior, or management principles unique to this area."
        
        # Sciences
        elif 'science' in path_str:
            if 'biology' in category or 'life' in category:
                return "Focus on biological processes, cellular mechanisms, genetic principles, or ecological relationships specific to this field."
            elif 'chemistry' in category:
                return "Focus on chemical reactions, molecular structures, bonding theories, or chemical properties and behavior."
            elif 'physics' in category:
                return "Focus on physical laws, forces, energy principles, wave behavior, or atomic/quantum phenomena."
            else:
                return "Focus on scientific principles, natural phenomena, research methods, or theories specific to this scientific discipline."
        
        # Mathematics
        elif 'math' in path_str:
            return "Focus on specific mathematical concepts, equations, theorems, problem-solving methods, or mathematical relationships unique to this area."
        
        # Languages
        elif 'language' in path_str:
            return "Focus on grammar structures, vocabulary, pronunciation patterns, cultural context, or communication principles specific to this language."
        
        # Technology/Engineering
        elif 'technology' in path_str or 'engineering' in path_str:
            return "Focus on technical concepts, design principles, algorithms, systems architecture, or technological methods specific to this field."
        
        # Arts and Creative
        elif 'art' in path_str or 'creative' in path_str:
            return "Focus on artistic techniques, design principles, aesthetic theories, creative processes, or stylistic elements specific to this medium."
        
        # Humanities
        elif 'humanities' in path_str or 'history' in path_str:
            return "Focus on historical events, cultural movements, philosophical ideas, literary analysis, or social developments specific to this area."
        
        # Default guidance
        return "Focus on the unique concepts, theories, methods, or knowledge that makes this subject distinct from others in its field."

    def generate_improved_description(self, node: SkillTreeNode) -> Optional[ImprovedDescription]:
        """Generate an improved description for a category node."""
        subject_context = self.determine_subject_context(node)
        
        # Create the improved prompt with specific subject guidance
        subject_specific_guidance = self.get_subject_specific_guidance(node)
        
        prompt = f"""Create a concise, accurate description for the learning category: "{node.name}"

Context:
- Learning Area: {node.learning_area}
- Category Path: {node.path}
- Platform: Online learning platform for academic study
- Focus: {subject_context}

CRITICAL Requirements:
1. Write 1-3 sentences (50-150 words maximum)
2. Be HIGHLY SPECIFIC to "{node.name}" - mention concrete topics that make this subject unique
3. Use ACCESSIBLE language that beginners can understand
4. Explain technical terms or use simpler alternatives
5. Make it sound interesting and approachable, not intimidating
6. STRICTLY FORBIDDEN - DO NOT use these words/phrases:
   - "hands-on", "practical experience", "lab work", "field work"
   - "career", "professional", "job training", "industry experience"  
   - "master", "expertise", "become an expert"
   - "real-world applications", "practical applications"
   - Technical jargon like "paradigms", "frameworks", "methodologies", "constructs"
   - Academic buzzwords like "analytical tools", "theoretical foundations"

SUBJECT-SPECIFIC GUIDANCE:
{subject_specific_guidance}

CRITICAL: Create COMPLETELY DIFFERENT descriptions with NO formulaic patterns:
- Each description must start DIFFERENTLY and use unique phrasing
- BANNED phrases: "examine the relationship", "discover the mechanisms", "analyze the patterns"
- Use natural, varied language that focuses on what makes this subject unique
- Make it sound like a human wrote each one separately, not using a template

Format your response as JSON:
{{
    "description": "Specific description highlighting what makes {node.name} unique and distinct",
    "focus_areas": ["specific_concept1", "specific_concept2", "specific_concept3"],
    "difficulty_level": "beginner|intermediate|advanced"
}}

GOOD Examples (accessible and specific):
Finance: "Learn how to evaluate investments, spread risk across different assets, and understand what makes stock prices go up and down."
Marketing: "Study how companies figure out what customers want, create appealing brands, and reach the right audience with their products."
Biology: "Understand how DNA copies itself, how cells get energy from food, and how species change over time to survive."
Cooking: "Learn different cutting techniques, which flavors work well together, and cooking methods from various cultures around the world."
History: "Explore what caused major wars and revolutions, how political movements shaped society, and how cultures have changed over time."

BAD Examples (too jargony or formulaic):
"Examine the relationship between organizational paradigms and strategic frameworks..."
"Analyze complex theoretical constructs and methodological approaches..."
"Study advanced analytical frameworks and sophisticated modeling techniques..."
"Learn the core principles, theories, and methods..." (too generic)
"""

        try:
            self.log_progress(f"Generating improved description for: {node.name}")
            
            response = self.claude.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=500,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            
            description_text = response.content[0].text
            
            # Parse JSON response
            try:
                description_data = json.loads(description_text)
                
                return ImprovedDescription(
                    description=description_data.get('description', ''),
                    focus_areas=description_data.get('focus_areas', []),
                    difficulty_level=description_data.get('difficulty_level', 'intermediate')
                )
            except json.JSONDecodeError:
                # If JSON parsing fails, extract description from raw response
                lines = description_text.strip().split('\n')
                for line in lines:
                    if len(line.strip()) > 20 and not line.startswith('{'):
                        return ImprovedDescription(
                            description=line.strip(),
                            focus_areas=[],
                            difficulty_level='intermediate'
                        )
                return None
                
        except Exception as e:
            self.log_progress(f"Error generating description for {node.name}: {e}")
            return None

    def get_all_nodes_with_descriptions(self) -> List[SkillTreeNode]:
        """Get all nodes at level 2 and 3 that have descriptions."""
        try:
            response = self.supabase.table('skill_tree_nodes').select('*').neq('description', None).order('path').execute()
            
            if not response.data:
                return []
            
            nodes = []
            for row in response.data:
                if row.get('path') and isinstance(row['path'], list) and len(row['path']) in [1, 2, 3]:
                    node = SkillTreeNode(
                        id=row['id'],
                        name=row['name'],
                        type='category',
                        path=row['path'],
                        learning_area=row['learning_area'],
                        has_learning_content=row['has_learning_content'],
                        learning_content_ids=row['learning_content_ids'],
                        is_menu_leaf=row['is_menu_leaf'],
                        description=row.get('description'),
                        parent_id=row['parent_id'],
                        metadata=row['metadata']
                    )
                    nodes.append(node)
            
            return nodes
            
        except Exception as e:
            self.log_progress(f"Error fetching nodes: {e}")
            return []

    def generate_descriptions_to_csv(self, nodes: List[SkillTreeNode], output_file: str, dry_run: bool = False, limit: int = None) -> Tuple[int, int]:
        """Generate improved descriptions and save to CSV for review."""
        if limit:
            nodes = nodes[:limit]
        
        self.log_progress(f"Processing {len(nodes)} nodes to CSV: {output_file}")
        
        success_count = 0
        error_count = 0
        
        # Prepare CSV file
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name', 'level', 'path', 'original_description', 'new_description', 'focus_areas', 'difficulty_level']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for i, node in enumerate(nodes):
                self.log_progress(f"[{i+1}/{len(nodes)}] Processing: {node.name}")
                
                if dry_run:
                    # For dry run, just write original data
                    writer.writerow({
                        'id': node.id,
                        'name': node.name,
                        'level': len(node.path) if node.path else 0,
                        'path': ' > '.join(node.path) if node.path else '',
                        'original_description': node.description,
                        'new_description': '[DRY RUN] Would generate improved description',
                        'focus_areas': '[DRY RUN]',
                        'difficulty_level': 'intermediate'
                    })
                    success_count += 1
                    time.sleep(1)  # Simulate processing time
                    continue
                
                # Generate improved description
                description = self.generate_improved_description(node)
                
                if description:
                    writer.writerow({
                        'id': node.id,
                        'name': node.name,
                        'level': len(node.path) if node.path else 0,
                        'path': ' > '.join(node.path) if node.path else '',
                        'original_description': node.description,
                        'new_description': description.description,
                        'focus_areas': ', '.join(description.focus_areas),
                        'difficulty_level': description.difficulty_level
                    })
                    success_count += 1
                    self.log_progress(f"Success: {node.name}")
                    self.log_progress(f"   Original: {node.description[:100]}...")
                    self.log_progress(f"   New: {description.description}")
                else:
                    writer.writerow({
                        'id': node.id,
                        'name': node.name,
                        'level': len(node.path) if node.path else 0,
                        'path': ' > '.join(node.path) if node.path else '',
                        'original_description': node.description,
                        'new_description': '[ERROR] Failed to generate',
                        'focus_areas': '',
                        'difficulty_level': ''
                    })
                    error_count += 1
                    self.log_progress(f"Failed: {node.name}")
                
                # Rate limiting delay
                if not dry_run and i < len(nodes) - 1:
                    self.log_progress(f"Waiting {self.api_delay} seconds for rate limiting...")
                    time.sleep(self.api_delay)
        
        return success_count, error_count

    def update_descriptions_from_csv(self, csv_file: str) -> Tuple[int, int]:
        """Update database descriptions from approved CSV file."""
        success_count = 0
        error_count = 0
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    if row['new_description'] and not row['new_description'].startswith('['):
                        try:
                            response = self.supabase.table('skill_tree_nodes').update({
                                'description': row['new_description']
                            }).eq('id', row['id']).execute()
                            
                            if response.data:
                                success_count += 1
                                self.log_progress(f"Updated: {row['name']}")
                            else:
                                error_count += 1
                                self.log_progress(f"Failed to update: {row['name']}")
                                
                        except Exception as e:
                            error_count += 1
                            self.log_progress(f"Error updating {row['name']}: {e}")
                    
        except Exception as e:
            self.log_progress(f"Error reading CSV file: {e}")
            return 0, 1
        
        return success_count, error_count

def main():
    """Main function for improved description generation."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate improved descriptions avoiding false assumptions')
    parser.add_argument('--dry-run', action='store_true', help='Test run without API calls')
    parser.add_argument('--limit', type=int, help='Limit number of nodes to process (for testing)')
    parser.add_argument('--update-from-csv', type=str, help='Update database from approved CSV file')
    parser.add_argument('--output', type=str, default='improved_descriptions.csv', help='Output CSV file name')
    
    args = parser.parse_args()
    
    print("Improved Description Generator")
    print("=" * 40)
    print("Focus: Avoiding false assumptions about hands-on learning and professional outcomes")
    
    if args.update_from_csv:
        print(f"Mode: Update database from {args.update_from_csv}")
    else:
        print(f"Mode: Generate to CSV file ({args.output})")
        print(f"Dry run: {args.dry_run}")
        if args.limit:
            print(f"Limit: {args.limit} nodes")
    print()
    
    try:
        generator = ImprovedDescriptionGenerator()
        
        if args.update_from_csv:
            # Update database from CSV
            print(f"Updating database from {args.update_from_csv}...")
            success, errors = generator.update_descriptions_from_csv(args.update_from_csv)
            
            print(f"\nUpdate Results:")
            print(f"  Successful: {success}")
            print(f"  Errors: {errors}")
            print(f"  Success rate: {success/(success+errors)*100:.1f}%" if (success+errors) > 0 else "No items processed")
        
        else:
            # Generate descriptions to CSV
            nodes = generator.get_all_nodes_with_descriptions()
            
            if args.limit:
                nodes = nodes[:args.limit]
            
            total_nodes = len(nodes)
            
            print(f"Found {total_nodes} nodes with descriptions to improve")
            
            if total_nodes == 0:
                print("No nodes to process!")
                return
            
            # Calculate estimates
            time_per_node = 1 if args.dry_run else 30  # seconds
            total_time_minutes = (total_nodes * time_per_node) / 60
            cost_per_node = 0 if args.dry_run else 0.02
            total_cost = total_nodes * cost_per_node
            
            print(f"\nEstimates:")
            print(f"  Time: {total_time_minutes:.1f} minutes ({total_time_minutes/60:.1f} hours)")
            print(f"  Cost: ${total_cost:.2f}")
            
            if not args.dry_run and not args.limit:
                confirm = input(f"\nProcess {total_nodes} nodes? (y/N): ")
                if confirm.lower() != 'y':
                    print("Cancelled.")
                    return
            
            print(f"\nStarting description generation to {args.output}...")
            if not args.dry_run:
                print("Note: 25-second delays between API calls for rate limiting")
            print()
            
            success, errors = generator.generate_descriptions_to_csv(nodes, args.output, args.dry_run, args.limit)
            
            print(f"\nGeneration Results:")
            print(f"  Successful: {success}")
            print(f"  Errors: {errors}")
            print(f"  Success rate: {success/(success+errors)*100:.1f}%" if (success+errors) > 0 else "No items processed")
            
            if args.dry_run:
                print(f"\n[DRY RUN] Sample data saved to {args.output}")
            else:
                print(f"\n✅ Improved descriptions saved to {args.output}")
                print(f"Review the file and then run with --update-from-csv {args.output} to update database")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()