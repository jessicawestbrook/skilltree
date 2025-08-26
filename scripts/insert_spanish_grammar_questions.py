#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Insert Spanish grammar questions from Anki conversion into database
Handles UUID mappings for language_id and category_id
"""

import json
import sys
import io
from pathlib import Path
from datetime import datetime
import asyncio
import os
from supabase import create_client, Client

# Set UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Supabase credentials from environment
SUPABASE_URL = os.environ.get('REACT_APP_SUPABASE_URL')
SUPABASE_KEY = os.environ.get('REACT_APP_SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: Set REACT_APP_SUPABASE_URL and REACT_APP_SUPABASE_ANON_KEY environment variables")
    sys.exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_or_create_language(code='es', name='Spanish'):
    """Get or create Spanish language entry"""
    # Check if Spanish exists
    result = supabase.table('languages').select('*').eq('code', code).execute()
    
    if result.data and len(result.data) > 0:
        return result.data[0]['id']
    
    # Create Spanish language
    result = supabase.table('languages').insert({
        'code': code,
        'name': name,
        'flag_emoji': '🇪🇸'
    }).execute()
    
    return result.data[0]['id']

def get_or_create_category(language_id, category_name='Grammar - Conjugation'):
    """Get or create grammar conjugation category"""
    # Check if category exists
    result = supabase.table('language_categories').select('*')\
        .eq('language_id', language_id)\
        .eq('name', category_name).execute()
    
    if result.data and len(result.data) > 0:
        return result.data[0]['id']
    
    # Create category
    result = supabase.table('language_categories').insert({
        'language_id': language_id,
        'name': category_name,
        'description': 'Spanish verb conjugation practice',
        'display_order': 1
    }).execute()
    
    return result.data[0]['id']

def convert_difficulty(difficulty_str):
    """Convert difficulty string to integer"""
    mapping = {
        'Elementary': 2,
        'Intermediate': 3,
        'Advanced': 4
    }
    return mapping.get(difficulty_str, 3)

def prepare_question_for_insert(question, language_id, category_id):
    """Prepare question object for database insertion"""
    return {
        'id': question['id'],
        'language_id': language_id,
        'category_id': category_id,
        'question_text': question['question_text'],
        'question_type': question['question_type'],
        'options': question['options'],
        'correct_answer': question['correct_answer'],
        'correct_answer_index': question['correct_answer_index'],
        'explanation': question['explanation'],
        'difficulty_level': convert_difficulty(question['difficulty_level']),
        'image_url': question.get('image_url'),
        'audio_url': question.get('audio_url'),
        'hint': question.get('hint'),
        'tags': question.get('tags', []),
        'estimated_time_seconds': question.get('estimated_time_seconds', 15),
        'metadata': question.get('metadata', {}),
        'created_at': question['created_at'],
        'updated_at': question['updated_at']
    }

def main():
    # Load converted questions
    json_file = Path(__file__).parent / 'spanish_grammar_questions.json'
    
    if not json_file.exists():
        print(f"Error: {json_file} not found. Run convert_anki_to_questions.py first.")
        return
    
    print(f"Loading questions from {json_file}")
    with open(json_file, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"Loaded {len(questions)} questions")
    
    # Get or create language and category
    print("Setting up language and category...")
    language_id = get_or_create_language()
    print(f"Spanish language ID: {language_id}")
    
    category_id = get_or_create_category(language_id)
    print(f"Grammar category ID: {category_id}")
    
    # Prepare questions for insertion
    print("Preparing questions for insertion...")
    prepared_questions = []
    for q in questions:
        prepared = prepare_question_for_insert(q, language_id, category_id)
        prepared_questions.append(prepared)
    
    # Insert in batches to avoid timeouts
    batch_size = 100
    total_inserted = 0
    
    print(f"Inserting {len(prepared_questions)} questions in batches of {batch_size}...")
    
    for i in range(0, len(prepared_questions), batch_size):
        batch = prepared_questions[i:i+batch_size]
        try:
            result = supabase.table('language_questions').insert(batch).execute()
            total_inserted += len(batch)
            print(f"  Inserted batch {i//batch_size + 1}: {len(batch)} questions (Total: {total_inserted})")
        except Exception as e:
            print(f"  Error inserting batch {i//batch_size + 1}: {e}")
            # Continue with next batch
    
    print(f"\nCompleted! Inserted {total_inserted} questions")
    
    # Verify insertion
    result = supabase.table('language_questions')\
        .select('count', count='exact')\
        .eq('category_id', category_id).execute()
    
    print(f"Verification: {result.count} questions in database for this category")

if __name__ == "__main__":
    main()