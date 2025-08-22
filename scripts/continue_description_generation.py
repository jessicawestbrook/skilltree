#!/usr/bin/env python3
"""
Continue Description Generation for Skill Tree Nodes
==================================================

This script continues generating descriptions for all skill tree nodes 
that don't have descriptions yet, processing them in batches with 
proper rate limiting.
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import List, Optional
import anthropic
from supabase import create_client, Client

class DescriptionGenerator:
    """Generate descriptions for skill tree nodes."""
    
    def __init__(self):
        """Initialize the description generator."""
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv('.env.local')
        
        # Initialize Anthropic client
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
        
        # Initialize Supabase client
        self.supabase_url = os.getenv('REACT_APP_SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase credentials are required")
            
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        
        # Rate limiting - be conservative with API calls
        self.api_delay = 12  # 12 seconds between API calls
        
        # Progress tracking
        self.processed_count = 0
        self.success_count = 0
        self.error_count = 0
        
    def log_progress(self, message: str):
        """Log progress with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
    
    def determine_target_audience(self, node_name: str, parent_name: str = None) -> str:
        """Determine the target audience based on subject matter."""
        node_lower = node_name.lower()
        parent_lower = parent_name.lower() if parent_name else ""
        
        # Elementary/Primary subjects (younger children)
        elementary_subjects = [
            'elementary', 'primary', 'basic math', 'counting', 'addition', 'subtraction',
            'multiplication', 'division', 'fractions', 'decimals', 'shapes', 'colors',
            'alphabet', 'phonics', 'reading', 'simple', 'beginning', 'intro'
        ]
        
        # Middle school/Teen subjects  
        teen_subjects = [
            'algebra', 'geometry', 'pre-calculus', 'trigonometry', 'physics', 'chemistry',
            'biology', 'world history', 'us history', 'geography', 'literature',
            'spanish', 'french', 'german', 'foreign language', 'language', 'programming'
        ]
        
        # Adult/Professional subjects
        adult_subjects = [
            'business', 'finance', 'marketing', 'management', 'economics', 'accounting',
            'psychology', 'philosophy', 'advanced', 'graduate', 'professional', 'career',
            'investment', 'entrepreneurship', 'leadership', 'statistics', 'calculus',
            'engineering', 'computer science', 'data science', 'machine learning',
            'artificial intelligence', 'law', 'medicine', 'research'
        ]
        
        # Check for elementary subjects
        if any(elem in node_lower or elem in parent_lower for elem in elementary_subjects):
            return "younger children (ages 6-10)"
        
        # Check for adult/professional subjects
        if any(adult in node_lower or adult in parent_lower for adult in adult_subjects):
            return "adults and professionals"
        
        # Check for teen subjects or default to teens for most academic subjects
        if any(teen in node_lower or teen in parent_lower for teen in teen_subjects):
            return "teens and young adults (ages 13-18)"
        
        # Default to general learners for unclassified topics
        return "students and lifelong learners"
    
    def generate_description(self, node_name: str, parent_name: str = None) -> Optional[str]:
        """Generate a description for a skill tree node."""
        
        # Determine target audience based on subject matter
        target_audience = self.determine_target_audience(node_name, parent_name)
        
        # Create context based on parent and node name
        context_info = f"Part of: {parent_name}" if parent_name else "Top-level category"
        
        prompt = f"""Create a concise, engaging description for the learning topic: "{node_name}"

Context: {context_info}
Target Audience: {target_audience}

Requirements:
1. Write 1-3 sentences (50-150 words maximum)
2. Be specific to "{node_name}" - avoid generic language
3. Mention concrete concepts, skills, or applications unique to this topic
4. Target the language and complexity level for {target_audience}
5. Make it sound interesting and educational for this age group
6. Be accurate and factual

AVOID these overused phrases:
- "building blocks", "foundation", "unlock the power"
- "dive into", "explore", "master", "essential skills"
- "real-world applications", "complex problems"
- "logical thinking", "problem-solving"

Return ONLY the description text, no formatting or extra text."""

        try:
            self.log_progress(f"Generating description for: {node_name}")
            
            response = self.claude.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=300,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            
            description = response.content[0].text.strip()
            
            # Clean up the description - remove quotes if present
            if description.startswith('"') and description.endswith('"'):
                description = description[1:-1]
            
            return description
                
        except Exception as e:
            self.log_progress(f"Error generating description for {node_name}: {e}")
            return None
    
    def get_nodes_without_descriptions(self, limit: int = 20) -> List[dict]:
        """Get nodes that don't have descriptions yet."""
        try:
            # Get nodes without descriptions
            response = self.supabase.table('skill_tree_nodes').select('id, name, parent_id, description').is_('description', None).limit(limit).execute()
            
            nodes = response.data or []
            
            # Also get nodes with empty descriptions
            empty_response = self.supabase.table('skill_tree_nodes').select('id, name, parent_id, description').eq('description', '').limit(limit).execute()
            
            if empty_response.data:
                nodes.extend(empty_response.data)
            
            return nodes[:limit]  # Ensure we don't exceed limit
            
        except Exception as e:
            self.log_progress(f"Error fetching nodes without descriptions: {e}")
            return []
    
    def get_parent_name(self, parent_id: str) -> Optional[str]:
        """Get the name of a parent node."""
        if not parent_id:
            return None
        
        try:
            response = self.supabase.table('skill_tree_nodes').select('name').eq('id', parent_id).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]['name']
                
        except Exception as e:
            self.log_progress(f"Error getting parent name for {parent_id}: {e}")
        
        return None
    
    def save_description(self, node_id: str, description: str) -> bool:
        """Save description to the database."""
        try:
            update_data = {
                'description': description,
                'updated_at': datetime.now().isoformat()
            }
            
            response = self.supabase.table('skill_tree_nodes').update(update_data).eq('id', node_id).execute()
            
            if response.data and len(response.data) > 0:
                return True
            else:
                self.log_progress(f"Failed to save description for node {node_id}")
                return False
                
        except Exception as e:
            self.log_progress(f"Database error saving description for {node_id}: {e}")
            return False
    
    def process_batch(self, batch_size: int = 10) -> bool:
        """Process a batch of nodes without descriptions."""
        nodes = self.get_nodes_without_descriptions(limit=batch_size)
        
        if not nodes:
            self.log_progress("No more nodes found without descriptions!")
            return False
        
        self.log_progress(f"Processing batch of {len(nodes)} nodes...")
        
        batch_success = 0
        batch_errors = 0
        
        for node in nodes:
            self.processed_count += 1
            node_name = node['name']
            node_id = node['id']
            parent_id = node.get('parent_id')
            
            # Get parent name for context
            parent_name = self.get_parent_name(parent_id) if parent_id else None
            
            # Generate description
            description = self.generate_description(node_name, parent_name)
            
            if description:
                # Save to database
                if self.save_description(node_id, description):
                    self.success_count += 1
                    batch_success += 1
                    self.log_progress(f"SUCCESS {node_name}: {description[:100]}...")
                else:
                    self.error_count += 1
                    batch_errors += 1
                    self.log_progress(f"ERROR Failed to save description for {node_name}")
            else:
                self.error_count += 1
                batch_errors += 1
                self.log_progress(f"ERROR Failed to generate description for {node_name}")
            
            # Rate limiting
            if node != nodes[-1]:  # Don't wait after the last node in batch
                time.sleep(self.api_delay)
        
        self.log_progress(f"Batch complete: {batch_success} successful, {batch_errors} errors")
        return True
    
    def generate_descriptions_continuously(self, max_batches: int = 100):
        """Generate descriptions continuously until all nodes are processed."""
        self.log_progress("Starting continuous description generation...")
        
        batches_processed = 0
        
        while batches_processed < max_batches:
            batches_processed += 1
            self.log_progress(f"\nBATCH {batches_processed}")
            
            # Process a batch
            has_more = self.process_batch(batch_size=10)
            
            if not has_more:
                self.log_progress("All nodes processed!")
                break
            
            # Progress summary
            self.log_progress(f"Overall Progress: {self.success_count} successful, {self.error_count} errors")
            
            # Brief pause between batches
            if batches_processed < max_batches:
                self.log_progress("Brief pause between batches...")
                time.sleep(5)
        
        self.log_progress(f"\nFINAL SUMMARY:")
        self.log_progress(f"  Batches processed: {batches_processed}")
        self.log_progress(f"  Total nodes processed: {self.processed_count}")
        self.log_progress(f"  Successful: {self.success_count}")
        self.log_progress(f"  Errors: {self.error_count}")
        
        if self.success_count > 0:
            success_rate = (self.success_count / self.processed_count) * 100
            self.log_progress(f"  Success rate: {success_rate:.1f}%")


def main():
    """Main function."""
    print("Skill Tree Description Generator")
    print("=" * 50)
    
    try:
        generator = DescriptionGenerator()
        
        # Check how many nodes need descriptions
        nodes_without_desc = generator.get_nodes_without_descriptions(limit=1000)
        total_without = len(nodes_without_desc)
        
        print(f"\nFound {total_without} nodes without descriptions")
        
        if total_without == 0:
            print("All nodes already have descriptions!")
            return
        
        # Estimate time (conservative estimate)
        estimated_minutes = (total_without * 12) / 60  # 12 seconds per node
        print(f"Estimated time: {estimated_minutes:.1f} minutes")
        
        print("\nStarting generation process...")
        print("Press Ctrl+C to stop at any time")
        
        # Start continuous generation
        generator.generate_descriptions_continuously(max_batches=100)
        
    except KeyboardInterrupt:
        print("\nGeneration stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        print("\nPlease ensure:")
        print("1. ANTHROPIC_API_KEY is set in .env.local")
        print("2. Supabase credentials are configured in .env.local")


if __name__ == "__main__":
    main()