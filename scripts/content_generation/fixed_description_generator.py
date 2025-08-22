#!/usr/bin/env python3
"""
Fixed Description Generator for SkillTree Categories
===================================================

This script works with the actual database schema using parent_id relationships
to build hierarchy and generate descriptions for 2nd and 3rd level categories.

Database Schema:
- id: primary key
- parent_id: foreign key to parent node
- name: category name
- description: category description (can be null)
- metadata: JSON metadata
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
    parent_id: Optional[str]
    description: Optional[str]
    metadata: Optional[Dict]
    level: int
    path: List[str]
    has_learning_content: bool = False
    learning_content_ids: Optional[List[str]] = None

@dataclass
class ImprovedDescription:
    """Represents an improved category description."""
    description: str
    focus_areas: List[str]
    difficulty_level: str

class FixedDescriptionGenerator:
    """Generates improved descriptions using actual database schema."""
    
    def __init__(self, anthropic_api_key: str = None, supabase_url: str = None, supabase_key: str = None):
        """Initialize the fixed description generator with API clients."""
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
        
        # Cache for node hierarchy
        self.nodes_by_id = {}
        self.children_by_parent = {}
        
    def log_progress(self, message: str):
        """Log progress with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def load_all_nodes(self) -> bool:
        """Load all nodes and build hierarchy cache."""
        try:
            # Get total count first
            count_response = self.supabase.table('skill_tree_nodes').select('id', count='exact').execute()
            total_count = count_response.count if count_response.count else 0
            self.log_progress(f"Total nodes in database: {total_count}")
            
            # Load all nodes (Supabase has a default limit of 1000)
            all_nodes = []
            page_size = 1000
            offset = 0
            
            while True:
                response = self.supabase.table('skill_tree_nodes').select('*').range(offset, offset + page_size - 1).execute()
                
                if not response.data:
                    break
                    
                all_nodes.extend(response.data)
                
                if len(response.data) < page_size:
                    break
                    
                offset += page_size
                self.log_progress(f"Loaded {len(all_nodes)} nodes so far...")
            
            self.log_progress(f"Finished loading {len(all_nodes)} total nodes")
            
            if not all_nodes:
                self.log_progress("No nodes found in database")
                return False
            
            # Build caches
            self.nodes_by_id = {}
            self.children_by_parent = {}
            
            for row in all_nodes:
                self.nodes_by_id[row['id']] = row
                
                parent_id = row.get('parent_id')
                if parent_id:
                    if parent_id not in self.children_by_parent:
                        self.children_by_parent[parent_id] = []
                    self.children_by_parent[parent_id].append(row['id'])
            
            self.log_progress(f"Loaded {len(self.nodes_by_id)} nodes")
            return True
            
        except Exception as e:
            self.log_progress(f"Error loading nodes: {e}")
            return False

    def build_node_path(self, node_id: str) -> List[str]:
        """Build the path from root to this node."""
        path = []
        current_id = node_id
        
        # Prevent infinite loops
        visited = set()
        
        while current_id and current_id not in visited:
            visited.add(current_id)
            node = self.nodes_by_id.get(current_id)
            
            if not node:
                break
                
            path.insert(0, node['name'])
            current_id = node.get('parent_id')
        
        return path

    def get_level_and_path(self, node_id: str) -> Tuple[int, List[str]]:
        """Get the level and path for a node."""
        path = self.build_node_path(node_id)
        level = len(path) - 1  # Level 0 = root, Level 1 = top categories, etc.
        return level, path

    def get_nodes_needing_descriptions(self) -> List[SkillTreeNode]:
        """Get all nodes at levels 1, 2, and 3 that need descriptions."""
        if not self.load_all_nodes():
            return []
        
        target_nodes = []
        
        for node_id, node_data in self.nodes_by_id.items():
            level, path = self.get_level_and_path(node_id)
            
            # Target levels 1 and 2 (which display as levels 2 and 3 on UI)
            if level in [1, 2]:
                # Check if needs description
                has_description = node_data.get('description') and node_data['description'].strip()
                
                if not has_description:
                    skill_node = SkillTreeNode(
                        id=node_data['id'],
                        name=node_data['name'],
                        parent_id=node_data.get('parent_id'),
                        description=node_data.get('description'),
                        metadata=node_data.get('metadata', {}),
                        level=level,
                        path=path,
                        has_learning_content=node_data.get('has_learning_content', False),
                        learning_content_ids=node_data.get('learning_content_ids')
                    )
                    target_nodes.append(skill_node)
        
        # Sort by level then name
        target_nodes.sort(key=lambda x: (x.level, x.name))
        return target_nodes

    def determine_subject_context(self, node: SkillTreeNode) -> str:
        """Determine the subject context for better description generation."""
        if len(node.path) < 2:
            return "academic study and conceptual understanding"
        
        # Use the top-level category to determine context
        top_level = node.path[1].lower() if len(node.path) > 1 else node.path[0].lower()
        
        context_map = {
            'computer science': 'computer science concepts and programming principles',
            'natural sciences': 'scientific concepts, theories, and natural phenomena',
            'mathematics': 'mathematical concepts, theories, and problem-solving methods',
            'languages': 'language study, linguistic concepts, and communication principles',
            'humanities': 'humanities concepts, cultural understanding, and analytical thinking',
            'creative skills': 'creative concepts, artistic principles, and design theory',
            'applied sciences': 'applied concepts, theoretical frameworks, and analytical methods',
            'technical skills': 'technical concepts and practical knowledge',
            'social sciences': 'social science concepts and human behavior analysis',
            'professional skills': 'business concepts, organizational theory, and analytical frameworks',
            'life skills': 'conceptual knowledge and theoretical understanding'
        }
        
        return context_map.get(top_level, 'academic study and conceptual understanding')

    def detect_target_audience(self, node: SkillTreeNode) -> str:
        """Detect the target audience age group for a topic."""
        category = node.name.lower()
        path_str = ' > '.join(node.path).lower() if node.path else ''
        
        # Young children indicators (ages 4-8)
        young_indicators = [
            'early', 'elementary', 'beginning', 'counting', 'alphabet', 'phonics', 
            'shapes', 'colors', 'animals', 'simple', 'first', 'preschool', 'kindergarten',
            'early math', 'early reading', 'early learning'
        ]
        
        # Middle/teen indicators (ages 9-17)
        teen_indicators = [
            'middle school', 'high school', 'teen', 'adolescent', 'junior',
            'intermediate', 'advanced', 'college prep', 'sat', 'act', 'ap ',
            'honors', 'algebra', 'geometry', 'calculus', 'chemistry', 'physics'
        ]
        
        # Adult/professional indicators (ages 18+)
        adult_indicators = [
            'professional', 'business', 'career', 'certification', 'graduate', 
            'master', 'phd', 'research', 'industry', 'corporate', 'management', 
            'leadership', 'strategy', 'analysis', 'finance', 'ai', 'automation',
            'fundamentals', 'advanced', 'technical skills'
        ]
        
        # Check for young audience (be more specific)
        young_matches = [indicator for indicator in young_indicators if indicator in category or indicator in path_str]
        if young_matches:
            # Exclude if it's clearly not for young children despite matching keywords
            exclusions = ['accounting', 'cpa', 'certification', 'professional', 'languages', 'alphabet', 'characters']
            if any(adult_word in category or adult_word in path_str for adult_word in exclusions):
                pass  # Don't return young_children for foreign languages, professional topics, etc.
            elif 'languages' in path_str:
                pass  # Foreign languages are for teens/adults
            else:
                return "young_children"  # Ages 4-8
        
        # Check for adult audience  
        if any(indicator in category or indicator in path_str for indicator in adult_indicators):
            return "adults"  # Ages 18+
        
        # Check for teen audience
        if any(indicator in category or indicator in path_str for indicator in teen_indicators):
            return "teens"  # Ages 9-17
        
        # Default based on subject area
        if any(subj in path_str for subj in ['mathematics', 'science', 'computer', 'languages']):
            return "teens"  # Most math/science/languages are teen-level by default
        elif any(subj in path_str for subj in ['professional', 'business', 'applied']):
            return "adults"
        else:
            return "teens"  # Default to teens for general academic content

    def get_subject_specific_guidance(self, node: SkillTreeNode) -> str:
        """Get specific guidance for different subject areas."""
        category = node.name.lower()
        path_str = ' > '.join(node.path).lower() if node.path else ''
        audience = self.detect_target_audience(node)
        
        # Physics specific
        if 'physics' in category:
            return "Focus on physical laws, forces, energy, motion, waves, thermodynamics, electromagnetism, or quantum phenomena specific to this physics area."
        
        # Sciences
        elif any(sci in path_str for sci in ['natural sciences', 'science']):
            if 'biology' in category or 'life' in category:
                return "Focus on biological processes, cellular mechanisms, genetic principles, or ecological relationships specific to this field."
            elif 'chemistry' in category:
                return "Focus on chemical reactions, molecular structures, bonding theories, or chemical properties and behavior."
            elif 'astronomy' in category or 'space' in category:
                return "Focus on celestial objects, astronomical phenomena, space exploration concepts, or cosmological principles."
            else:
                return "Focus on scientific principles, natural phenomena, research methods, or theories specific to this scientific discipline."
        
        # Mathematics
        elif 'math' in path_str:
            return "Focus on specific mathematical concepts, equations, theorems, problem-solving methods, or mathematical relationships unique to this area."
        
        # Computer Science
        elif 'computer' in path_str:
            return "Focus on programming concepts, algorithms, data structures, software design principles, or computational methods specific to this area."
        
        # Business and Economics
        elif any(biz in path_str for biz in ['business', 'economics', 'applied sciences']):
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
        
        # Languages
        elif 'language' in path_str:
            return "Focus on grammar structures, vocabulary, pronunciation patterns, cultural context, or communication principles specific to this language."
        
        # Engineering/Technical
        elif any(tech in path_str for tech in ['engineering', 'technical']):
            return "Focus on technical concepts, design principles, engineering methods, or technological systems specific to this field."
        
        # Arts and Creative
        elif 'creative' in path_str:
            return "Focus on artistic techniques, design principles, aesthetic theories, creative processes, or stylistic elements specific to this medium."
        
        # Humanities
        elif 'humanities' in path_str:
            return "Focus on historical events, cultural movements, philosophical ideas, literary analysis, or social developments specific to this area."
        
        # Default guidance
        return "Focus on the unique concepts, theories, methods, or knowledge that makes this subject distinct from others in its field."

    def generate_improved_description(self, node: SkillTreeNode) -> Optional[ImprovedDescription]:
        """Generate an improved description for a category node."""
        subject_context = self.determine_subject_context(node)
        subject_specific_guidance = self.get_subject_specific_guidance(node)
        audience = self.detect_target_audience(node)
        
        # Audience-specific language guidance
        audience_guidance = {
            "young_children": "Use simple, fun language that a 4-8 year old can understand. Avoid technical terms. Use words like 'learn', 'discover', 'find out', 'explore'. Make it sound exciting and playful.",
            "teens": "Use clear, engaging language appropriate for ages 9-17. Explain concepts simply but don't talk down to them. Use age-appropriate vocabulary.",
            "adults": "Use professional, sophisticated language appropriate for adult learners. Technical terms are acceptable if explained clearly."
        }
        
        # Create the improved prompt
        prompt = f"""Create a concise, accurate description for the learning category: "{node.name}"

Context:
- Category Path: {' > '.join(node.path)}
- Platform: Online learning platform for academic study
- Focus: {subject_context}
- Target Audience: {audience.replace('_', ' ').title()} - {audience_guidance[audience]}

CRITICAL Requirements:
1. Write 1-3 sentences (50-150 words maximum)
2. Be HIGHLY SPECIFIC to "{node.name}" - mention concrete topics that make this subject unique
3. Use ACCESSIBLE language that beginners can understand
4. Explain technical terms or use simpler alternatives
5. Make it sound interesting and approachable, not intimidating
6. STRICTLY FORBIDDEN - DO NOT use these words/phrases:
   - "hands-on", "practical experience", "lab work", "field work", "hands-on activities"
   - "career", "professional", "job training", "industry experience"  
   - "master", "expertise", "become an expert", "develop expertise"
   - "real-world applications", "practical applications"
   - Technical jargon like "paradigms", "frameworks", "methodologies", "constructs"
   - Academic buzzwords like "analytical tools", "theoretical foundations"
   - ANY phrase suggesting physical activities or professional training

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

GOOD Examples (age-appropriate language):
Early Math (Young Children): "Learn to count things, recognize different shapes, and figure out which group has more toys or cookies!"
Physics (Teens): "Study how forces create motion, how energy transforms from one type to another, and how waves carry information through space."
Business Strategy (Adults): "Develop strategic thinking skills to analyze market dynamics, competitive positioning, and organizational performance metrics."
Biology (Teens): "Understand how DNA copies itself, how cells get energy from food, and how species change over time to survive."

BAD Examples (too jargony or formulaic):
"Examine the relationship between organizational paradigms and strategic frameworks..."
"Analyze complex theoretical constructs and methodological approaches..."
"Study advanced analytical frameworks and sophisticated modeling techniques..."
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
                self.log_progress(f"[{i+1}/{len(nodes)}] Processing: {node.name} (Level {node.level})")
                
                if dry_run:
                    # For dry run, just write original data
                    writer.writerow({
                        'id': node.id,
                        'name': node.name,
                        'level': node.level,
                        'path': ' > '.join(node.path),
                        'original_description': node.description or '[NO DESCRIPTION]',
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
                        'level': node.level,
                        'path': ' > '.join(node.path),
                        'original_description': node.description or '[NO DESCRIPTION]',
                        'new_description': description.description,
                        'focus_areas': ', '.join(description.focus_areas),
                        'difficulty_level': description.difficulty_level
                    })
                    success_count += 1
                    self.log_progress(f"Success: {node.name}")
                    self.log_progress(f"   Path: {' > '.join(node.path)}")
                    self.log_progress(f"   New: {description.description}")
                else:
                    writer.writerow({
                        'id': node.id,
                        'name': node.name,
                        'level': node.level,
                        'path': ' > '.join(node.path),
                        'original_description': node.description or '[NO DESCRIPTION]',
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
    """Main function for fixed description generation."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate improved descriptions using actual database schema')
    parser.add_argument('--dry-run', action='store_true', help='Test run without API calls')
    parser.add_argument('--limit', type=int, help='Limit number of nodes to process (for testing)')
    parser.add_argument('--update-from-csv', type=str, help='Update database from approved CSV file')
    parser.add_argument('--output', type=str, default='fixed_descriptions.csv', help='Output CSV file name')
    
    args = parser.parse_args()
    
    print("Fixed Description Generator")
    print("=" * 40)
    print("Using actual database schema with parent_id relationships")
    
    if args.update_from_csv:
        print(f"Mode: Update database from {args.update_from_csv}")
    else:
        print(f"Mode: Generate to CSV file ({args.output})")
        print(f"Dry run: {args.dry_run}")
        if args.limit:
            print(f"Limit: {args.limit} nodes")
    print()
    
    try:
        generator = FixedDescriptionGenerator()
        
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
            nodes = generator.get_nodes_needing_descriptions()
            
            if args.limit:
                nodes = nodes[:args.limit]
            
            total_nodes = len(nodes)
            
            print(f"Found {total_nodes} nodes needing descriptions")
            
            # Show breakdown by level
            levels = {}
            for node in nodes:
                if node.level not in levels:
                    levels[node.level] = []
                levels[node.level].append(node)
            
            for level in sorted(levels.keys()):
                print(f"  Level {level}: {len(levels[level])} nodes")
                if level == 1:  # Show some examples of level 1 nodes
                    examples = [node.name for node in levels[level][:5]]
                    print(f"    Examples: {', '.join(examples)}")
                    if 'Physics' in [node.name for node in levels[level]]:
                        print(f"    Physics is included!")
            
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
                print(f"\nImproved descriptions saved to {args.output}")
                print(f"Review the file and then run with --update-from-csv {args.output} to update database")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()