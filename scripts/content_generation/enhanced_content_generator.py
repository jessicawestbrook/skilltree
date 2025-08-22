#!/usr/bin/env python3
"""
Enhanced Learning Content Generator with Category Descriptions
============================================================

Extends the original content generator to also generate:
1. Category descriptions for skill tree nodes
2. Learning content and questions (existing functionality)
3. Save descriptions to the skill_tree_nodes table

This version generates concise, engaging descriptions for categories
that will be displayed on the category pages.
"""

import os
import sys
import json
import time
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
    description: Optional[str] = None
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
class GeneratedDescription:
    """Represents a generated category description."""
    description: str
    focus_areas: List[str]
    difficulty_level: str

class EnhancedContentGenerator:
    """Enhanced content generator with description generation."""
    
    def __init__(self, anthropic_api_key: str = None, supabase_url: str = None, supabase_key: str = None):
        """Initialize the enhanced content generator with API clients."""
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
        
        # Rate limiting configuration (Claude API Tier 1 compliance)
        self.api_delay = 25  # 25 seconds between API calls for rate limit compliance
        
        # Progress tracking
        self.processed_count = 0
        self.success_count = 0
        self.error_count = 0
        
    def log_progress(self, message: str):
        """Log progress with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
    
    def generate_category_description(self, node: SkillTreeNode) -> Optional[GeneratedDescription]:
        """Generate a concise description for a category."""
        # Skip description generation for leaf nodes (skills) - only generate for categories
        if node.type != 'category':
            return None
            
        # Create subject-specific context to make descriptions unique
        subject_hints = {
            'Algebra': 'variables, equations, functions, polynomials, linear relationships',
            'Algorithms': 'computational procedures, data processing, sorting, searching, optimization',
            'Geometry': 'shapes, spatial relationships, angles, proofs, measurements',
            'Calculus': 'derivatives, integrals, limits, rates of change, continuous functions',
            'Statistics': 'data analysis, probability, distributions, hypothesis testing',
            'Programming': 'coding languages, software development, debugging, syntax',
            'Machine Learning': 'artificial intelligence, neural networks, pattern recognition, data modeling',
            'Marketing': 'branding, customer acquisition, advertising, market research',
            'Finance': 'money management, investments, banking, financial planning',
            'Chemistry': 'elements, compounds, chemical reactions, molecular structure',
            'Physics': 'forces, energy, motion, waves, matter and its properties',
            'Biology': 'living organisms, cells, genetics, ecosystems, life processes',
            'History': 'past events, historical analysis, timelines, civilizations, cultural changes',
            'Literature': 'written works, literary analysis, genres, authors, storytelling techniques',
            'Psychology': 'human behavior, mental processes, cognitive functions, emotions',
            'Engineering': 'design, construction, technical problem-solving, systems optimization',
            'Art': 'creative expression, visual techniques, artistic movements, aesthetic principles',
            'Music': 'sound, rhythm, melody, composition, musical instruments and theory'
        }
        
        # Get specific hints for this subject
        subject_hint = ""
        for subject, hints in subject_hints.items():
            if subject.lower() in node.name.lower():
                subject_hint = f"Key concepts include: {hints}."
                break
        
        prompt = f"""Create a highly specific, engaging description for the learning category: "{node.name}"

Context:
- Learning Area: {node.learning_area}
- Category Path: {node.path}
- Target Audience: Students and lifelong learners
- Subject Focus: {subject_hint}

CRITICAL Requirements:
1. Write 1-3 sentences (50-150 words maximum)
2. Be HIGHLY SPECIFIC to "{node.name}" - avoid generic language that could apply to any subject
3. Mention concrete concepts, techniques, or applications unique to this field
4. Use precise terminology specific to this domain
5. Avoid vague words like "fundamental", "essential", "unlock", "master", "dive into"
6. Focus on what makes THIS subject distinct from others
7. Include specific examples or applications when possible

AVOID these overused phrases:
- "building blocks", "foundation", "unlock the power"
- "dive into", "explore", "master", "essential skills"
- "real-world applications", "complex problems"
- "logical thinking", "problem-solving"

Format your response as JSON:
{{
    "description": "Highly specific description with concrete details about {node.name}",
    "focus_areas": ["specific_concept1", "specific_concept2", "specific_concept3"],
    "difficulty_level": "beginner|intermediate|advanced"
}}

Example of GOOD specificity:
{{
    "description": "Study quadratic equations, polynomial factoring, and linear systems to model relationships between variables and solve for unknown values in mathematical expressions.",
    "focus_areas": ["quadratic equations", "polynomial factoring", "linear systems"],
    "difficulty_level": "intermediate"
}}

Example of BAD (too generic):
{{
    "description": "Learn the fundamental concepts that unlock mathematical thinking and problem-solving skills for real-world applications.",
    "focus_areas": ["problem solving", "logical thinking", "applications"],
    "difficulty_level": "intermediate"
}}"""

        try:
            self.log_progress(f"Generating description for category: {node.name}")
            
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
                
                return GeneratedDescription(
                    description=description_data.get('description', ''),
                    focus_areas=description_data.get('focus_areas', []),
                    difficulty_level=description_data.get('difficulty_level', 'intermediate')
                )
            except json.JSONDecodeError:
                # If JSON parsing fails, extract description from raw response
                # Try to find a reasonable description in the text
                lines = description_text.strip().split('\n')
                for line in lines:
                    if len(line.strip()) > 20 and not line.startswith('{'):
                        return GeneratedDescription(
                            description=line.strip(),
                            focus_areas=[],
                            difficulty_level='intermediate'
                        )
                return None
                
        except Exception as e:
            self.log_progress(f"Error generating description for {node.name}: {e}")
            return None
    
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
        """Generate questions based on the learning content."""
        prompt = f"""Based on the learning content for "{node.name}", create 10 multiple choice questions.

Learning Content Summary:
Title: {content.title}
Content: {content.content[:1000]}...

Requirements for Questions:
1. Create exactly 10 multiple choice questions
2. Each question should have exactly 4 options (A, B, C, D)
3. Questions should test understanding of the content, not memorization
4. Include a mix of difficulty levels (easy, medium, hard)
5. Provide detailed explanations for correct answers
6. Make questions conceptual rather than calculation-heavy
7. Ensure each question has only one clearly correct answer

Format your response as JSON with this structure:
{{
    "questions": [
        {{
            "question_text": "Clear, specific question",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": 0,
            "explanation": "Detailed explanation of why this answer is correct",
            "difficulty": "easy|medium|hard"
        }}
    ]
}}"""

        try:
            response = self.claude.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=4000,
                temperature=0.7,
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
    
    def save_description_to_database(self, node: SkillTreeNode, description: GeneratedDescription) -> bool:
        """Save category description to the skill_tree_nodes table."""
        try:
            update_data = {
                'description': description.description,
                'updated_at': datetime.now().isoformat()
            }
            
            response = self.supabase.table('skill_tree_nodes').update(update_data).eq('id', node.id).execute()
            
            if response.data and len(response.data) > 0:
                self.log_progress(f"Saved description for {node.name}")
                return True
            else:
                self.log_progress(f"Failed to save description for {node.name}")
                return False
                
        except Exception as e:
            self.log_progress(f"Database error saving description for {node.name}: {e}")
            return False
    
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
                generated_id = response.data[0]['id']
                self.log_progress(f"Saved learning content for {node.name}")
                return str(generated_id)
            else:
                self.log_progress(f"Failed to save content for {node.name}")
                return None
                
        except Exception as e:
            self.log_progress(f"Database error saving content for {node.name}: {e}")
            return None
    
    def save_questions_to_database(self, questions: List[GeneratedQuestion]) -> List[str]:
        """Save questions to the database."""
        question_ids = []
        
        for question in questions:
            try:
                question_data = {
                    'question_text': question.question_text,
                    'options': question.options,
                    'correct_answer': question.correct_answer,
                    'explanation': question.explanation,
                    'difficulty': question.difficulty,
                    'image_url': question.image_url,
                    'created_at': datetime.now().isoformat()
                }
                
                response = self.supabase.table('questions').insert(question_data).execute()
                
                if response.data and len(response.data) > 0:
                    question_ids.append(str(response.data[0]['id']))
                else:
                    self.log_progress(f"Failed to insert question: {question.question_text[:50]}...")
                    
            except Exception as e:
                self.log_progress(f"Database error saving question: {e}")
        
        return question_ids
    
    def update_skill_node(self, node: SkillTreeNode, content_id: str = None, question_ids: List[str] = None):
        """Update skill tree node with generated content and question IDs."""
        try:
            update_data = {
                'updated_at': datetime.now().isoformat()
            }
            
            if content_id:
                update_data['has_learning_content'] = True
                update_data['learning_content_ids'] = [content_id]
            
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
    
    def process_single_node(self, node: SkillTreeNode, generate_description: bool = True, generate_content: bool = True) -> bool:
        """Process a single skill tree node - generate description, content, and questions."""
        self.log_progress(f"\nProcessing node: {node.name} (Type: {node.type}, Path: {node.path})")
        self.processed_count += 1
        
        try:
            description_saved = False
            content_id = None
            question_ids = []
            
            # Generate and save category description (for categories only)
            if generate_description and node.type == 'category':
                self.log_progress(f"Generating description for category: {node.name}")
                description = self.generate_category_description(node)
                
                if description:
                    description_saved = self.save_description_to_database(node, description)
                    time.sleep(self.api_delay)  # Rate limiting
                else:
                    self.log_progress(f"Failed to generate description for: {node.name}")
            
            # Generate learning content (for skills or content-enabled categories)
            if generate_content and (node.type == 'skill' or node.has_learning_content):
                self.log_progress(f"Generating learning content for: {node.name}")
                content = self.generate_learning_content(node)
                
                if content:
                    time.sleep(self.api_delay)  # Rate limiting
                    
                    # Generate questions
                    self.log_progress(f"Generating questions for: {node.name}")
                    questions = self.generate_questions(node, content)
                    self.log_progress(f"Generated {len(questions)} questions for: {node.name}")
                    
                    time.sleep(self.api_delay)  # Rate limiting
                    
                    # Save to database
                    content_id = self.save_content_to_database(node, content)
                    
                    if content_id and questions:
                        question_ids = self.save_questions_to_database(questions)
                        self.log_progress(f"Saved {len(question_ids)} questions for: {node.name}")
                else:
                    self.log_progress(f"Failed to generate content for: {node.name}")
            
            # Update skill tree node
            if content_id or description_saved:
                self.update_skill_node(node, content_id, question_ids)
                self.success_count += 1
                self.log_progress(f"Successfully processed: {node.name}")
                return True
            else:
                self.log_progress(f"No content generated for: {node.name}")
                return False
                
        except Exception as e:
            self.log_progress(f"Error processing node {node.name}: {e}")
            self.error_count += 1
            return False
    
    def get_categories_without_descriptions(self, limit: int = 10) -> List[SkillTreeNode]:
        """Get categories that don't have descriptions yet."""
        try:
            # Try to query for categories without descriptions
            response = self.supabase.table('skill_tree_nodes').select('*').eq('type', 'category').is_('description', None).limit(limit).execute()
            
            nodes = []
            if response.data:
                for row in response.data:
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
                    nodes.append(node)
            
            return nodes
            
        except Exception as e:
            self.log_progress(f"Error fetching categories without descriptions: {e}")
            # Fallback: get all categories
            try:
                response = self.supabase.table('skill_tree_nodes').select('*').eq('type', 'category').limit(limit).execute()
                
                nodes = []
                if response.data:
                    for row in response.data:
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
                        nodes.append(node)
                
                return nodes
                
            except Exception as e2:
                self.log_progress(f"Error in fallback query: {e2}")
                return []


def main():
    """Main function for testing the enhanced generator."""
    print("🚀 Enhanced Content Generator with Category Descriptions")
    print("=" * 60)
    
    try:
        generator = EnhancedContentGenerator()
        
        # Get a few categories without descriptions for testing
        categories = generator.get_categories_without_descriptions(limit=3)
        
        if not categories:
            print("No categories found or all categories already have descriptions.")
            return
        
        print(f"\nFound {len(categories)} categories to process:")
        for cat in categories:
            print(f"  - {cat.name} ({cat.path})")
        
        print("\nStarting description generation...")
        
        for category in categories:
            success = generator.process_single_node(
                category, 
                generate_description=True, 
                generate_content=False  # Only generate descriptions for testing
            )
            
            if not success:
                print(f"Failed to process {category.name}")
        
        print(f"\n📊 Processing Summary:")
        print(f"  Total processed: {generator.processed_count}")
        print(f"  Successful: {generator.success_count}")
        print(f"  Errors: {generator.error_count}")
        
    except Exception as e:
        print(f"❌ Error initializing generator: {e}")
        print("\nPlease ensure:")
        print("1. ANTHROPIC_API_KEY is set in your environment")
        print("2. Supabase credentials are configured in .env.local")
        print("3. Description column has been added to skill_tree_nodes table")


if __name__ == "__main__":
    main()