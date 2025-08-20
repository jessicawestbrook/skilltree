#!/usr/bin/env python3
"""
Simple Batch Content Generation for Spanish Vocabulary Topics
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

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

def main():
    try:
        print("=== Batch Spanish Content Generation ===")
        
        # Initialize
        generator = LearningContentGenerator()
        output_dir = Path(__file__).parent / "generated_content"
        output_dir.mkdir(exist_ok=True)
        
        # Initialize Supabase for reading topics
        supabase_url = os.getenv('REACT_APP_SUPABASE_URL')
        supabase_key = os.getenv('REACT_APP_SUPABASE_ANON_KEY')
        supabase = create_client(supabase_url, supabase_key)
        
        print("\n1. Finding Spanish vocabulary topics...")
        
        # Search for Spanish topics
        search_terms = ['spanish', 'family', 'colors', 'numbers', 'food', 'vocabulary']
        candidates = []
        seen_ids = set()
        
        for term in search_terms:
            try:
                response = supabase.table('skill_tree_nodes').select('*').ilike('name', f'%{term}%').eq('type', 'skill').eq('has_learning_content', False).limit(10).execute()
                
                if response.data:
                    for node in response.data:
                        if node['id'] not in seen_ids:
                            candidates.append(node)
                            seen_ids.add(node['id'])
            except Exception as e:
                print(f"   Warning: Error searching for '{term}': {e}")
        
        print(f"Found {len(candidates)} potential topics")
        
        # Select top 5 topics
        topics = candidates[:5]
        print(f"\nSelected {len(topics)} topics:")
        for i, topic in enumerate(topics, 1):
            print(f"  {i}. {topic['name']}")
        
        print(f"\n2. Generating content...")
        results = []
        
        for i, topic_data in enumerate(topics, 1):
            try:
                print(f"\n[{i}/{len(topics)}] Processing: {topic_data['name']}")
                
                # Convert to SkillTreeNode
                node = SkillTreeNode(
                    id=topic_data['id'],
                    name=topic_data['name'],
                    type=topic_data['type'],
                    path=topic_data.get('path', ''),
                    learning_area='Spanish Vocabulary',
                    has_learning_content=False,
                    learning_content_ids=None,
                    is_menu_leaf=False
                )
                
                # Generate content
                print("   Generating learning content...")
                content = generator.generate_learning_content(node)
                
                if not content:
                    print("   ERROR: Content generation failed")
                    results.append({'topic': node.name, 'success': False, 'error': 'Content generation failed'})
                    continue
                
                print(f"   SUCCESS: Generated {len(content.content)} character content")
                
                # Generate questions
                print("   Generating questions...")
                questions = generator.generate_questions(node, content)
                
                if not questions:
                    print("   ERROR: Question generation failed")
                    results.append({'topic': node.name, 'success': False, 'error': 'Question generation failed'})
                    continue
                
                print(f"   SUCCESS: Generated {len(questions)} questions")
                
                # Save files
                topic_slug = node.name.replace(' ', '_').replace('/', '_')
                
                # Save content
                content_file = output_dir / f"content_{topic_slug}.json"
                content_data = {
                    'topic_id': node.id,
                    'topic_name': node.name,
                    'title': content.title,
                    'content': content.content,
                    'estimated_time_minutes': content.estimated_time_minutes,
                    'difficulty_level': content.difficulty_level,
                    'generated_at': datetime.now().isoformat()
                }
                
                with open(content_file, 'w', encoding='utf-8') as f:
                    json.dump(content_data, f, indent=2, ensure_ascii=False)
                
                # Save questions
                questions_file = output_dir / f"questions_{topic_slug}.json"
                questions_data = {
                    'topic_id': node.id,
                    'topic_name': node.name,
                    'questions': [
                        {
                            'question_text': q.question_text,
                            'options': q.options,
                            'correct_answer': q.correct_answer,
                            'explanation': q.explanation,
                            'difficulty': q.difficulty
                        }
                        for q in questions
                    ],
                    'generated_at': datetime.now().isoformat()
                }
                
                with open(questions_file, 'w', encoding='utf-8') as f:
                    json.dump(questions_data, f, indent=2, ensure_ascii=False)
                
                print(f"   SAVED: {content_file.name}, {questions_file.name}")
                
                results.append({
                    'topic': node.name,
                    'success': True,
                    'content_length': len(content.content),
                    'question_count': len(questions),
                    'files': [str(content_file), str(questions_file)]
                })
                
                # Rate limiting - 25s delay to respect Claude API Tier 1 limits
                print("   Rate limiting: Waiting 25s for Claude API compliance...")
                time.sleep(25)
                
            except Exception as e:
                print(f"   ERROR: {e}")
                results.append({'topic': topic_data['name'], 'success': False, 'error': str(e)})
        
        # Summary
        print(f"\n=== BATCH GENERATION COMPLETE ===")
        successful = [r for r in results if r.get('success')]
        failed = [r for r in results if not r.get('success')]
        
        print(f"Processed: {len(results)} topics")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {len(failed)}")
        
        if successful:
            print(f"\nGenerated content:")
            total_questions = sum(r.get('question_count', 0) for r in successful)
            print(f"  - {len(successful)} learning modules")
            print(f"  - {total_questions} total questions")
            print(f"  - Files saved to: {output_dir}")
        
        if failed:
            print(f"\nFailed topics:")
            for result in failed:
                print(f"  - {result['topic']}: {result.get('error', 'Unknown error')}")
        
        print(f"\nNext steps:")
        print(f"1. Review generated files in {output_dir}/")
        print(f"2. Add REACT_APP_SUPABASE_SERVICE_KEY to .env.local for database insertion")
        print(f"3. Run database insertion when ready")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()