#!/usr/bin/env python3
"""
Batch Content Generation for Spanish Vocabulary Topics
=====================================================

Generates learning content and questions for multiple Spanish vocabulary topics,
saving results to files for review before database insertion.
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict

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

class BatchSpanishGenerator:
    def __init__(self):
        self.generator = LearningContentGenerator()
        self.output_dir = Path(__file__).parent / "generated_content"
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize Supabase for reading topics
        supabase_url = os.getenv('REACT_APP_SUPABASE_URL')
        supabase_key = os.getenv('REACT_APP_SUPABASE_ANON_KEY')
        self.supabase = create_client(supabase_url, supabase_key)
        
        self.results = []
        
    def find_spanish_topics(self, limit: int = 10) -> List[Dict]:
        """Find Spanish vocabulary topics that need content."""
        try:
            print("🔍 Searching for Spanish vocabulary topics...")
            
            # Search terms that indicate Spanish vocabulary content
            search_terms = [
                'spanish', 'familia', 'colores', 'números', 'comida', 
                'family', 'colors', 'numbers', 'food', 'vocabulary',
                'casa', 'cuerpo', 'animales', 'ropa', 'tiempo',
                'house', 'body', 'animals', 'clothes', 'weather'
            ]
            
            candidates = []
            seen_ids = set()
            
            for term in search_terms:
                try:
                    response = self.supabase.table('skill_tree_nodes').select('*').ilike('name', f'%{term}%').eq('type', 'skill').eq('has_learning_content', False).limit(20).execute()
                    
                    if response.data:
                        for node in response.data:
                            if node['id'] not in seen_ids:
                                candidates.append(node)
                                seen_ids.add(node['id'])
                except Exception as e:
                    print(f"   Warning: Error searching for '{term}': {e}")
            
            # Sort by relevance (Spanish-specific terms first)
            spanish_terms = ['spanish', 'familia', 'colores', 'números', 'comida', 'casa']
            def relevance_score(node):
                name_lower = node.get('name', '').lower()
                path_lower = node.get('path', '').lower()
                score = 0
                
                # Higher score for Spanish-specific terms
                for term in spanish_terms:
                    if term in name_lower or term in path_lower:
                        score += 10
                
                # Medium score for general vocabulary terms
                vocab_terms = ['family', 'colors', 'numbers', 'food', 'vocabulary']
                for term in vocab_terms:
                    if term in name_lower or term in path_lower:
                        score += 5
                        
                return score
            
            candidates.sort(key=relevance_score, reverse=True)
            
            print(f"   Found {len(candidates)} potential Spanish topics")
            
            # Filter to most relevant ones
            selected = candidates[:limit]
            
            print(f"📋 Selected {len(selected)} topics for content generation:")
            for i, topic in enumerate(selected, 1):
                print(f"   {i:2d}. {topic['name']}")
                if topic.get('path'):
                    print(f"       Path: {topic['path']}")
            
            return selected
            
        except Exception as e:
            print(f"❌ Error finding Spanish topics: {e}")
            return []
    
    def generate_content_for_topic(self, topic_data: Dict) -> Dict:
        """Generate content and questions for a single topic."""
        try:
            # Convert to SkillTreeNode
            node = SkillTreeNode(
                id=topic_data['id'],
                name=topic_data['name'],
                type=topic_data['type'],
                path=topic_data.get('path', ''),
                learning_area=topic_data.get('learning_area', 'Spanish Vocabulary'),
                has_learning_content=topic_data.get('has_learning_content', False),
                learning_content_ids=topic_data.get('learning_content_ids'),
                is_menu_leaf=topic_data.get('is_menu_leaf', False),
                parent_id=topic_data.get('parent_id'),
                metadata=topic_data.get('metadata', {})
            )
            
            print(f"\n🎯 Generating content for: {node.name}")
            print("=" * 60)
            
            # Generate learning content
            print("   📖 Generating learning content...")
            content = self.generator.generate_learning_content(node)
            
            if not content:
                print("   ❌ Failed to generate learning content")
                return {
                    'topic': node.name,
                    'success': False,
                    'error': 'Content generation failed'
                }
            
            print(f"   ✅ Generated {len(content.content)} character content ({content.estimated_time_minutes} min)")
            
            # Generate questions
            print("   ❓ Generating questions...")
            questions = self.generator.generate_questions(node, content)
            
            if not questions:
                print("   ❌ Failed to generate questions")
                return {
                    'topic': node.name,
                    'success': False,
                    'error': 'Question generation failed'
                }
            
            print(f"   ✅ Generated {len(questions)} questions")
            
            # Save to files
            topic_slug = node.name.replace(' ', '_').replace('/', '_').replace(':', '_')
            
            # Save content
            content_file = self.output_dir / f"content_{topic_slug}.json"
            content_data = {
                'topic_id': node.id,
                'topic_name': node.name,
                'topic_path': node.path,
                'title': content.title,
                'content': content.content,
                'estimated_time_minutes': content.estimated_time_minutes,
                'difficulty_level': content.difficulty_level,
                'images': content.images,
                'generated_at': datetime.now().isoformat()
            }
            
            with open(content_file, 'w', encoding='utf-8') as f:
                json.dump(content_data, f, indent=2, ensure_ascii=False)
            
            # Save questions
            questions_file = self.output_dir / f"questions_{topic_slug}.json"
            questions_data = {
                'topic_id': node.id,
                'topic_name': node.name,
                'questions': [
                    {
                        'question_text': q.question_text,
                        'options': q.options,
                        'correct_answer': q.correct_answer,
                        'explanation': q.explanation,
                        'difficulty': q.difficulty,
                        'image_url': q.image_url
                    }
                    for q in questions
                ],
                'generated_at': datetime.now().isoformat()
            }
            
            with open(questions_file, 'w', encoding='utf-8') as f:
                json.dump(questions_data, f, indent=2, ensure_ascii=False)
            
            print(f"   💾 Saved to: {content_file.name}, {questions_file.name}")
            
            # Add rate limiting
            time.sleep(2)
            
            return {
                'topic': node.name,
                'topic_id': node.id,
                'success': True,
                'content_file': str(content_file),
                'questions_file': str(questions_file),
                'content_length': len(content.content),
                'question_count': len(questions),
                'estimated_time': content.estimated_time_minutes
            }
            
        except Exception as e:
            print(f"   ❌ Error generating content for {topic_data['name']}: {e}")
            return {
                'topic': topic_data['name'],
                'success': False,
                'error': str(e)
            }
    
    def generate_batch_summary(self) -> str:
        """Generate a summary of the batch processing results."""
        successful = [r for r in self.results if r.get('success')]
        failed = [r for r in self.results if not r.get('success')]
        
        summary = f"""
# Batch Spanish Content Generation Summary

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview
- **Total Topics Processed:** {len(self.results)}
- **Successful:** {len(successful)}
- **Failed:** {len(failed)}

## Successful Generations
"""
        
        for result in successful:
            summary += f"""
### {result['topic']}
- **Content Length:** {result.get('content_length', 'N/A')} characters
- **Questions:** {result.get('question_count', 'N/A')}
- **Estimated Reading Time:** {result.get('estimated_time', 'N/A')} minutes
- **Files:** 
  - Content: `{Path(result.get('content_file', '')).name}`
  - Questions: `{Path(result.get('questions_file', '')).name}`
"""
        
        if failed:
            summary += "\n## Failed Generations\n"
            for result in failed:
                summary += f"- **{result['topic']}:** {result.get('error', 'Unknown error')}\n"
        
        summary += f"""
## Next Steps
1. Review generated content files in `{self.output_dir}/`
2. Add `REACT_APP_SUPABASE_SERVICE_KEY` to `.env.local` for database insertion
3. Run database insertion script to save content to database
4. Test content in SkillTree application

## Cost Estimate
- **API Calls:** ~{len(successful) * 2} (content + questions)
- **Estimated Cost:** ~${len(successful) * 0.11:.2f} USD
"""
        
        return summary
    
    def run_batch_generation(self, max_topics: int = 5):
        """Run batch content generation for Spanish topics."""
        try:
            print("🚀 Starting Batch Spanish Content Generation")
            print("=" * 60)
            
            # Find topics
            topics = self.find_spanish_topics(limit=max_topics)
            
            if not topics:
                print("❌ No Spanish topics found for content generation")
                return
            
            print(f"\n📝 Processing {len(topics)} topics...")
            
            # Generate content for each topic
            for i, topic in enumerate(topics, 1):
                print(f"\n[{i}/{len(topics)}] Processing: {topic['name']}")
                result = self.generate_content_for_topic(topic)
                self.results.append(result)
            
            # Generate summary
            print(f"\n📊 Generating summary...")
            summary = self.generate_batch_summary()
            
            summary_file = self.output_dir / f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary)
            
            print(f"💾 Summary saved to: {summary_file}")
            
            print("\n🎉 Batch Generation Complete!")
            print("=" * 60)
            print(f"Generated content for {len([r for r in self.results if r.get('success')])} Spanish topics")
            print(f"Review files in: {self.output_dir}/")
            
        except Exception as e:
            print(f"❌ Batch generation error: {e}")
            import traceback
            traceback.print_exc()

def main():
    try:
        batch_generator = BatchSpanishGenerator()
        
        print("Generating content for 5 Spanish vocabulary topics...")
        max_topics = 5
        
        batch_generator.run_batch_generation(max_topics=max_topics)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Generation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()