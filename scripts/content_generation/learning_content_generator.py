#!/usr/bin/env python3
"""
Batch Learning Content and Question Generator
===========================================

This script processes skill tree nodes to generate:
1. 10-30 minutes of comprehensive learning content
2. 50-100 multiple choice questions with detailed explanations
3. Save all content to the Supabase database

Features:
- Batch processing with progress tracking
- Recovery/resume functionality for interrupted processing
- Rate limiting and error handling
- Cost estimation and progress reporting
- Database insertion with validation
"""

import os
import sys
import json
import time
import uuid
import csv
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import anthropic
from supabase import create_client, Client

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@dataclass
class SkillTreeNode:
    """Represents a skill tree node from the database."""
    id: str
    name: str
    type: str
    path: str
    learning_area: str
    has_learning_content: bool
    learning_content_ids: Optional[List[str]]
    is_menu_leaf: bool
    parent_id: Optional[str] = None
    metadata: Optional[Dict] = None

@dataclass
class GeneratedContent:
    """Represents generated learning content."""
    title: str
    content: str
    estimated_time_minutes: int
    difficulty_level: str
    images: Optional[List[str]] = None

@dataclass
class GeneratedQuestion:
    """Represents a generated question."""
    question_text: str
    options: List[str]
    correct_answer: int
    explanation: str
    difficulty: str
    image_url: Optional[str] = None

@dataclass
class ProcessingStats:
    """Tracks processing statistics."""
    total_nodes: int = 0
    processed_nodes: int = 0
    successful_content: int = 0
    successful_questions: int = 0
    failed_nodes: int = 0
    total_api_calls: int = 0
    total_cost_estimate: float = 0.0
    start_time: Optional[datetime] = None
    last_checkpoint: Optional[datetime] = None


class LearningContentGenerator:
    """Main class for generating learning content and questions."""
    
    def __init__(self, anthropic_api_key: str = None, supabase_url: str = None, supabase_key: str = None):
        """Initialize the content generator with API clients."""
        # Initialize Anthropic client
        self.anthropic_api_key = anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
        
        # Initialize Supabase client
        self.supabase_url = supabase_url or os.getenv('REACT_APP_SUPABASE_URL')
        self.supabase_key = supabase_key or os.getenv('REACT_APP_SUPABASE_ANON_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase credentials are required")
            
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        
        # Processing configuration
        self.batch_size = 5  # Process nodes in batches
        self.api_delay = 25.0  # Seconds between API calls (Claude Tier 1 rate limit safe)
        self.max_retries = 3
        self.checkpoint_frequency = 10  # Save progress every N nodes
        
        # Output directories
        self.output_dir = "scripts/content_generation/output"
        self.checkpoint_file = f"{self.output_dir}/checkpoint.json"
        self.progress_file = f"{self.output_dir}/progress.log"
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.stats = ProcessingStats()
        
    def load_skill_tree_nodes(self) -> List[SkillTreeNode]:
        """Load skill tree nodes from the database."""
        print("Loading skill tree nodes from database...")
        
        try:
            response = self.supabase.table('skill_tree_nodes').select('*').execute()
            nodes_data = response.data
            
            if not nodes_data:
                print("No skill tree nodes found in database")
                return []
            
            nodes = []
            for node_data in nodes_data:
                node = SkillTreeNode(
                    id=node_data['id'],
                    name=node_data['name'],
                    type=node_data['type'],
                    path=node_data['path'],
                    learning_area=node_data['learning_area'],
                    has_learning_content=node_data.get('has_learning_content', False),
                    learning_content_ids=node_data.get('learning_content_ids'),
                    is_menu_leaf=node_data.get('is_menu_leaf', False),
                    parent_id=node_data.get('parent_id'),
                    metadata=node_data.get('metadata', {})
                )
                nodes.append(node)
            
            print(f"Loaded {len(nodes)} skill tree nodes")
            return nodes
            
        except Exception as e:
            print(f"Error loading skill tree nodes: {e}")
            raise
    
    def filter_nodes_for_processing(self, nodes: List[SkillTreeNode]) -> List[SkillTreeNode]:
        """Filter nodes that need content generation."""
        # Process leaf nodes that don't already have learning content
        filtered = [
            node for node in nodes 
            if (node.is_menu_leaf or node.type == 'leaf') 
            and not node.has_learning_content
            and not (node.learning_content_ids and len(node.learning_content_ids) > 0)
        ]
        
        print(f"Filtered to {len(filtered)} nodes needing content generation")
        return filtered
    
    def load_checkpoint(self) -> Dict[str, Any]:
        """Load processing checkpoint if exists."""
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'r') as f:
                    checkpoint = json.load(f)
                print(f"Loaded checkpoint: {checkpoint.get('processed_nodes', 0)} nodes processed")
                return checkpoint
            except Exception as e:
                print(f"Error loading checkpoint: {e}")
        
        return {'processed_nodes': 0, 'processed_node_ids': []}
    
    def save_checkpoint(self, processed_node_ids: List[str]):
        """Save processing checkpoint."""
        checkpoint = {
            'processed_nodes': len(processed_node_ids),
            'processed_node_ids': processed_node_ids,
            'timestamp': datetime.now().isoformat(),
            'stats': asdict(self.stats)
        }
        
        try:
            with open(self.checkpoint_file, 'w') as f:
                json.dump(checkpoint, f, indent=2)
            self.stats.last_checkpoint = datetime.now()
        except Exception as e:
            print(f"Error saving checkpoint: {e}")
    
    def log_progress(self, message: str):
        """Log progress to file and console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        print(log_message)
        
        try:
            with open(self.progress_file, 'a', encoding='utf-8') as f:
                f.write(log_message + "\n")
        except Exception as e:
            print(f"Error writing to progress log: {e}")
    
    def estimate_costs(self, nodes_to_process: int) -> Dict[str, float]:
        """Estimate API costs for processing."""
        # Claude-3 Sonnet pricing (approximate)
        input_cost_per_1k = 0.003  # $0.003 per 1K input tokens
        output_cost_per_1k = 0.015  # $0.015 per 1K output tokens
        
        # Estimates per node
        content_input_tokens = 500  # Prompt tokens
        content_output_tokens = 2000  # ~10-30 min content
        
        questions_input_tokens = 800  # Prompt + content tokens
        questions_output_tokens = 5000  # 50-100 questions with explanations
        
        total_input_tokens = nodes_to_process * (content_input_tokens + questions_input_tokens)
        total_output_tokens = nodes_to_process * (content_output_tokens + questions_output_tokens)
        
        input_cost = (total_input_tokens / 1000) * input_cost_per_1k
        output_cost = (total_output_tokens / 1000) * output_cost_per_1k
        total_cost = input_cost + output_cost
        
        return {
            'input_cost': input_cost,
            'output_cost': output_cost,
            'total_cost': total_cost,
            'total_input_tokens': total_input_tokens,
            'total_output_tokens': total_output_tokens
        }
    
    def generate_learning_content(self, node: SkillTreeNode) -> Optional[GeneratedContent]:
        """Generate learning content for a skill tree node."""
        prompt = f"""Create comprehensive learning content for the topic: "{node.name}"

Context:
- Learning Area: {node.learning_area}
- Topic Path: {node.path}
- Target Audience: General learners (high school to adult level)
- Content Length: 10-30 minutes of reading/study time

Requirements:
1. Create engaging, educational content (approximately 800-2000 words)
2. Include clear explanations with examples
3. Structure with headers and subheadings
4. Make content self-contained (don't reference external materials)
5. Include practical applications where relevant
6. Use a tone that's educational but engaging

Format your response as JSON with these fields:
{{
    "title": "Engaging title for the content",
    "content": "Full learning content with markdown formatting",
    "estimated_time_minutes": 15,
    "difficulty_level": "beginner|intermediate|advanced"
}}

Focus on making the content comprehensive enough that a learner could understand the topic from this material alone."""

        try:
            self.stats.total_api_calls += 1
            
            response = self.claude.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=3000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content_text = response.content[0].text
            
            # Parse JSON response
            try:
                content_data = json.loads(content_text)
                
                return GeneratedContent(
                    title=content_data.get('title', node.name),
                    content=content_data.get('content', ''),
                    estimated_time_minutes=content_data.get('estimated_time_minutes', 15),
                    difficulty_level=content_data.get('difficulty_level', 'intermediate'),
                )
            except json.JSONDecodeError:
                # If JSON parsing fails, create content from raw response
                return GeneratedContent(
                    title=node.name,
                    content=content_text,
                    estimated_time_minutes=20,
                    difficulty_level='intermediate',
                )
                
        except Exception as e:
            self.log_progress(f"Error generating content for {node.name}: {e}")
            return None
    
    def generate_questions(self, node: SkillTreeNode, content: GeneratedContent) -> List[GeneratedQuestion]:
        """Generate questions for the learning content."""
        prompt = f"""Based on the following learning content about "{content.title}", create exactly 10 multiple choice questions.

Learning Content:
{content.content[:1500]}...

Requirements:
1. Create diverse questions that test different aspects of the content
2. Mix difficulty levels (30% easy, 50% medium, 20% hard)
3. Each question should have 4 multiple choice options
4. Only one correct answer per question
5. Provide detailed explanations for why each answer is correct/incorrect
6. Questions should be answerable based solely on the provided content
7. Avoid overly complex calculations - focus on conceptual understanding

Format your response as JSON with this structure:
{{
    "questions": [
        {{
            "question_text": "Question text here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": 0,
            "explanation": "Detailed explanation covering why the correct answer is right and why other options are wrong",
            "difficulty": "easy|medium|hard"
        }}
    ]
}}

Create exactly 10 high-quality questions with good variety. 

CRITICAL: Return only valid JSON. Do not include any explanatory text before or after the JSON."""

        try:
            self.stats.total_api_calls += 1
            
            response = self.claude.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=4000,
                temperature=0.8,
                messages=[{"role": "user", "content": prompt}]
            )
            
            questions_text = response.content[0].text
            
            # Parse JSON response
            try:
                questions_data = json.loads(questions_text)
                questions_list = questions_data.get('questions', [])
                
                generated_questions = []
                for q_data in questions_list:
                    if all(key in q_data for key in ['question_text', 'options', 'correct_answer', 'explanation']):
                        question = GeneratedQuestion(
                            question_text=q_data['question_text'],
                            options=q_data['options'],
                            correct_answer=int(q_data['correct_answer']),
                            explanation=q_data['explanation'],
                            difficulty=q_data.get('difficulty', 'medium'),
                        )
                        generated_questions.append(question)
                
                return generated_questions
                
            except (json.JSONDecodeError, KeyError) as e:
                self.log_progress(f"Error parsing questions JSON for {node.name}: {e}")
                return []
                
        except Exception as e:
            self.log_progress(f"Error generating questions for {node.name}: {e}")
            return []
    
    def save_content_to_database(self, node: SkillTreeNode, content: GeneratedContent) -> Optional[str]:
        """Save learning content to the database."""
        try:
            content_data = {
                'title': content.title,
                'content': content.content,
                'estimated_time_minutes': content.estimated_time_minutes,
                'difficulty_level': content.difficulty_level,
                'images': content.images,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            response = self.supabase.table('learning_content').insert(content_data).execute()
            
            if response.data and len(response.data) > 0:
                generated_id = response.data[0]['id']  # Get the auto-generated integer ID
                self.stats.successful_content += 1
                return str(generated_id)  # Return as string for consistency
            else:
                self.log_progress(f"Failed to insert content for {node.name}")
                return None
                
        except Exception as e:
            self.log_progress(f"Database error saving content for {node.name}: {e}")
            return None
    
    def save_questions_to_database(self, questions: List[GeneratedQuestion]) -> List[str]:
        """Save questions to the database."""
        question_ids = []
        
        for question in questions:
            try:
                question_id = str(uuid.uuid4())
                
                question_data = {
                    'id': question_id,
                    'question_text': question.question_text,
                    'options': question.options,
                    'correct_answer': question.correct_answer,
                    'explanation': question.explanation,
                    'difficulty': question.difficulty,
                    'image_url': question.image_url,
                    'created_at': datetime.now().isoformat()
                }
                
                response = self.supabase.table('questions').insert(question_data).execute()
                
                if response.data:
                    question_ids.append(question_id)
                    self.stats.successful_questions += 1
                else:
                    self.log_progress(f"Failed to insert question: {question.question_text[:50]}...")
                    
            except Exception as e:
                self.log_progress(f"Database error saving question: {e}")
        
        return question_ids
    
    def update_skill_node(self, node: SkillTreeNode, content_id: str, question_ids: List[str]):
        """Update skill tree node with generated content and question IDs."""
        try:
            update_data = {
                'has_learning_content': True,
                'learning_content_ids': [content_id] if content_id else [],
                'updated_at': datetime.now().isoformat()
            }
            
            response = self.supabase.table('skill_tree_nodes').update(update_data).eq('id', node.id).execute()
            
            if not response.data:
                self.log_progress(f"Failed to update skill tree node {node.name}")
                return False
            
            # Also link questions to learning content
            if content_id and question_ids:
                content_update = {
                    'question_ids': question_ids,
                    'updated_at': datetime.now().isoformat()
                }
                
                self.supabase.table('learning_content').update(content_update).eq('id', content_id).execute()
            
            return True
            
        except Exception as e:
            self.log_progress(f"Error updating skill tree node {node.name}: {e}")
            return False
    
    def process_single_node(self, node: SkillTreeNode) -> bool:
        """Process a single skill tree node - generate content and questions."""
        self.log_progress(f"Processing node: {node.name} (Path: {node.path})")
        
        try:
            # Generate learning content
            self.log_progress(f"Generating learning content for: {node.name}")
            content = self.generate_learning_content(node)
            
            if not content:
                self.log_progress(f"Failed to generate content for: {node.name}")
                return False
            
            # Add delay between API calls
            time.sleep(self.api_delay)
            
            # Generate questions
            self.log_progress(f"Generating questions for: {node.name}")
            questions = self.generate_questions(node, content)
            
            if not questions:
                self.log_progress(f"Failed to generate questions for: {node.name}")
                # Still save content even if questions fail
            
            self.log_progress(f"Generated {len(questions)} questions for: {node.name}")
            
            # Add delay between API calls
            time.sleep(self.api_delay)
            
            # Save to database
            content_id = self.save_content_to_database(node, content)
            
            if not content_id:
                self.log_progress(f"Failed to save content for: {node.name}")
                return False
            
            question_ids = []
            if questions:
                question_ids = self.save_questions_to_database(questions)
            
            # Update skill tree node
            if self.update_skill_node(node, content_id, question_ids):
                self.log_progress(f"Successfully processed: {node.name} (Content: {content_id}, Questions: {len(question_ids)})")
                return True
            else:
                self.log_progress(f"Failed to update skill tree node: {node.name}")
                return False
                
        except Exception as e:
            self.log_progress(f"Error processing node {node.name}: {e}")
            return False
    
    def run_batch_processing(self, max_nodes: Optional[int] = None, resume: bool = True):
        """Run the batch processing for all skill tree nodes."""
        self.stats.start_time = datetime.now()
        self.log_progress("Starting batch learning content generation")
        
        # Load skill tree nodes
        all_nodes = self.load_skill_tree_nodes()
        nodes_to_process = self.filter_nodes_for_processing(all_nodes)
        
        if not nodes_to_process:
            self.log_progress("No nodes found that need content generation")
            return
        
        # Load checkpoint if resuming
        checkpoint = {}
        processed_node_ids = []
        
        if resume:
            checkpoint = self.load_checkpoint()
            processed_node_ids = checkpoint.get('processed_node_ids', [])
        
        # Filter out already processed nodes
        remaining_nodes = [node for node in nodes_to_process if node.id not in processed_node_ids]
        
        # Apply max_nodes limit if specified
        if max_nodes:
            remaining_nodes = remaining_nodes[:max_nodes]
        
        self.stats.total_nodes = len(remaining_nodes)
        
        if not remaining_nodes:
            self.log_progress("All nodes have already been processed")
            return
        
        # Cost estimation
        cost_estimate = self.estimate_costs(len(remaining_nodes))
        self.log_progress(f"Processing {len(remaining_nodes)} nodes")
        self.log_progress(f"Estimated cost: ${cost_estimate['total_cost']:.2f}")
        self.log_progress(f"Estimated tokens: {cost_estimate['total_input_tokens']:,} input, {cost_estimate['total_output_tokens']:,} output")
        
        # Confirm before proceeding
        if len(remaining_nodes) > 10:
            user_input = input(f"Process {len(remaining_nodes)} nodes with estimated cost ${cost_estimate['total_cost']:.2f}? (y/n): ")
            if user_input.lower() != 'y':
                self.log_progress("Processing cancelled by user")
                return
        
        # Process nodes in batches
        success_count = 0
        
        for i, node in enumerate(remaining_nodes):
            try:
                self.stats.processed_nodes = i + 1
                success = self.process_single_node(node)
                
                if success:
                    success_count += 1
                    processed_node_ids.append(node.id)
                else:
                    self.stats.failed_nodes += 1
                
                # Save checkpoint periodically
                if (i + 1) % self.checkpoint_frequency == 0:
                    self.save_checkpoint(processed_node_ids)
                    self.log_progress(f"Checkpoint saved. Progress: {i + 1}/{len(remaining_nodes)} nodes")
                
                # Progress update
                if (i + 1) % 5 == 0:
                    elapsed_time = datetime.now() - self.stats.start_time
                    rate = (i + 1) / elapsed_time.total_seconds() * 3600  # nodes per hour
                    eta = (len(remaining_nodes) - i - 1) / rate * 3600 if rate > 0 else 0
                    
                    self.log_progress(f"Progress: {i + 1}/{len(remaining_nodes)} ({(i + 1)/len(remaining_nodes)*100:.1f}%)")
                    self.log_progress(f"Success rate: {success_count}/{i + 1} ({success_count/(i + 1)*100:.1f}%)")
                    self.log_progress(f"Processing rate: {rate:.1f} nodes/hour, ETA: {eta/3600:.1f} hours")
                
            except KeyboardInterrupt:
                self.log_progress("Processing interrupted by user")
                self.save_checkpoint(processed_node_ids)
                break
            except Exception as e:
                self.log_progress(f"Unexpected error processing node {node.name}: {e}")
                self.stats.failed_nodes += 1
        
        # Final checkpoint and summary
        self.save_checkpoint(processed_node_ids)
        
        total_time = datetime.now() - self.stats.start_time
        self.log_progress("=" * 50)
        self.log_progress("BATCH PROCESSING COMPLETE")
        self.log_progress(f"Total time: {total_time}")
        self.log_progress(f"Nodes processed: {success_count}/{len(remaining_nodes)}")
        self.log_progress(f"Success rate: {success_count/len(remaining_nodes)*100:.1f}%")
        self.log_progress(f"API calls made: {self.stats.total_api_calls}")
        self.log_progress(f"Content generated: {self.stats.successful_content}")
        self.log_progress(f"Questions generated: {self.stats.successful_questions}")
        self.log_progress(f"Failed nodes: {self.stats.failed_nodes}")


def main():
    """Main function to run the content generator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate learning content and questions for skill tree")
    parser.add_argument('--max-nodes', type=int, help="Maximum number of nodes to process (for testing)")
    parser.add_argument('--no-resume', action='store_true', help="Start from beginning, ignore checkpoint")
    parser.add_argument('--estimate-only', action='store_true', help="Only show cost estimate, don't process")
    
    args = parser.parse_args()
    
    try:
        generator = LearningContentGenerator()
        
        if args.estimate_only:
            # Load and filter nodes for cost estimation
            all_nodes = generator.load_skill_tree_nodes()
            nodes_to_process = generator.filter_nodes_for_processing(all_nodes)
            
            if args.max_nodes:
                nodes_to_process = nodes_to_process[:args.max_nodes]
            
            cost_estimate = generator.estimate_costs(len(nodes_to_process))
            print(f"Cost estimate for {len(nodes_to_process)} nodes:")
            print(f"  Input cost: ${cost_estimate['input_cost']:.2f}")
            print(f"  Output cost: ${cost_estimate['output_cost']:.2f}")
            print(f"  Total cost: ${cost_estimate['total_cost']:.2f}")
            print(f"  Input tokens: {cost_estimate['total_input_tokens']:,}")
            print(f"  Output tokens: {cost_estimate['total_output_tokens']:,}")
        else:
            generator.run_batch_processing(
                max_nodes=args.max_nodes,
                resume=not args.no_resume
            )
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please ensure ANTHROPIC_API_KEY and Supabase credentials are set")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()