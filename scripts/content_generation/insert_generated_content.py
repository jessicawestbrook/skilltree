#!/usr/bin/env python3
"""
Database Insertion Script for Generated Content
==============================================

This script reads the generated content files and inserts them into the database.
Requires REACT_APP_SUPABASE_SERVICE_KEY to be set in .env.local for RLS bypass.
"""

import os
import sys
import json
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

from supabase import create_client

class ContentInserter:
    def __init__(self):
        # Check for service key
        self.service_key = os.getenv('REACT_APP_SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_SERVICE_KEY')
        if not self.service_key:
            raise ValueError("Service key required. Add REACT_APP_SUPABASE_SERVICE_KEY to .env.local")
        
        supabase_url = os.getenv('REACT_APP_SUPABASE_URL')
        self.supabase = create_client(supabase_url, self.service_key)
        
        self.content_dir = Path(__file__).parent / "generated_content"
        
    def find_content_files(self):
        """Find all generated content and question files."""
        content_files = list(self.content_dir.glob("content_*.json"))
        questions_files = list(self.content_dir.glob("questions_*.json"))
        
        # Match content files with question files
        pairs = []
        for content_file in content_files:
            topic_name = content_file.name.replace("content_", "").replace(".json", "")
            question_file = self.content_dir / f"questions_{topic_name}.json"
            
            if question_file.exists():
                pairs.append({
                    'topic_name': topic_name,
                    'content_file': content_file,
                    'questions_file': question_file
                })
        
        return pairs
    
    def insert_content_and_questions(self, content_file, questions_file):
        """Insert content and questions for a single topic."""
        try:
            # Load content data
            with open(content_file, 'r', encoding='utf-8') as f:
                content_data = json.load(f)
            
            # Load questions data
            with open(questions_file, 'r', encoding='utf-8') as f:
                questions_data = json.load(f)
            
            print(f"  Inserting content: {content_data.get('title', 'Unknown')}")
            
            # Insert learning content (without ID - let DB auto-generate)
            content_insert_data = {
                'title': content_data['title'],
                'content': content_data['content'],
                'estimated_time_minutes': content_data['estimated_time_minutes'],
                'difficulty_level': content_data['difficulty_level'],
                'images': content_data.get('images', []),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            content_response = self.supabase.table('learning_content').insert(content_insert_data).execute()
            
            if not content_response.data or len(content_response.data) == 0:
                print(f"    ERROR: Failed to insert content")
                return False
            
            content_id = content_response.data[0]['id']
            print(f"    SUCCESS: Content inserted with ID {content_id}")
            
            # Insert questions
            question_ids = []
            questions = questions_data.get('questions', [])
            
            print(f"  Inserting {len(questions)} questions...")
            
            for i, question in enumerate(questions, 1):
                question_insert_data = {
                    'question_text': question['question_text'],
                    'options': question['options'],
                    'correct_answer': question['correct_answer'],
                    'explanation': question['explanation'],
                    'difficulty': question['difficulty'],
                    'image_url': question.get('image_url'),
                    'created_at': datetime.now().isoformat()
                }
                
                try:
                    question_response = self.supabase.table('questions').insert(question_insert_data).execute()
                    
                    if question_response.data and len(question_response.data) > 0:
                        question_id = question_response.data[0]['id']
                        question_ids.append(question_id)
                        print(f"    Q{i}: SUCCESS (ID: {question_id})")
                    else:
                        print(f"    Q{i}: ERROR - No data returned")
                        
                except Exception as e:
                    print(f"    Q{i}: ERROR - {e}")
            
            print(f"  Successfully inserted {len(question_ids)} questions")
            
            # Update learning content with question IDs
            if question_ids:
                content_update = {
                    'question_ids': question_ids,
                    'updated_at': datetime.now().isoformat()
                }
                
                update_response = self.supabase.table('learning_content').update(content_update).eq('id', content_id).execute()
                
                if update_response.data:
                    print(f"  SUCCESS: Linked {len(question_ids)} questions to content")
                else:
                    print(f"  WARNING: Failed to link questions to content")
            
            # Update skill tree node
            topic_id = content_data.get('topic_id')
            if topic_id:
                node_update = {
                    'has_learning_content': True,
                    'learning_content_ids': [str(content_id)],
                    'updated_at': datetime.now().isoformat()
                }
                
                try:
                    node_response = self.supabase.table('skill_tree_nodes').update(node_update).eq('id', topic_id).execute()
                    
                    if node_response.data:
                        print(f"  SUCCESS: Updated skill tree node")
                    else:
                        print(f"  WARNING: Failed to update skill tree node")
                        
                except Exception as e:
                    print(f"  WARNING: Error updating skill tree node: {e}")
            
            return True
            
        except Exception as e:
            print(f"  ERROR: {e}")
            return False
    
    def run_insertion(self):
        """Run the batch insertion process."""
        try:
            print("=== Database Content Insertion ===")
            
            # Find content files
            pairs = self.find_content_files()
            
            if not pairs:
                print("No content files found to insert")
                return
            
            print(f"\nFound {len(pairs)} topics to insert:")
            for pair in pairs:
                print(f"  - {pair['topic_name']}")
            
            print(f"\nStarting insertion...")
            
            successful = 0
            failed = 0
            
            for i, pair in enumerate(pairs, 1):
                print(f"\n[{i}/{len(pairs)}] Processing: {pair['topic_name']}")
                
                if self.insert_content_and_questions(pair['content_file'], pair['questions_file']):
                    successful += 1
                else:
                    failed += 1
            
            print(f"\n=== INSERTION COMPLETE ===")
            print(f"Successful: {successful}")
            print(f"Failed: {failed}")
            
            if successful > 0:
                print(f"\nContent is now available in your SkillTree application!")
                print(f"Navigate to the Spanish vocabulary sections to see the new content.")
        
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()

def main():
    try:
        # Check if service key is available
        service_key = os.getenv('REACT_APP_SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_SERVICE_KEY')
        
        if not service_key:
            print("ERROR: Service key required for database insertion")
            print("\nTo insert content into the database:")
            print("1. Get your Supabase service role key from the Supabase dashboard")
            print("2. Add it to .env.local as REACT_APP_SUPABASE_SERVICE_KEY=your_key_here")
            print("3. Run this script again")
            print("\nThe service key bypasses Row Level Security and allows content insertion.")
            return
        
        inserter = ContentInserter()
        inserter.run_insertion()
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()