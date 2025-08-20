#!/usr/bin/env python3
"""
Generate CSV files from existing checkpoint data
"""

import json
import csv
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class SpellingWord:
    """Data structure matching the database schema exactly"""
    word: str
    definition: Optional[str] = None
    pronunciation: Optional[str] = None  
    etymology: Optional[str] = None
    language_origins: Optional[str] = None
    example_sentence: Optional[str] = None
    difficulty: Optional[str] = None  # User-friendly difficulty name
    source_difficulty: Optional[str] = None  # Original source difficulty
    source: Optional[str] = None
    source_url: Optional[str] = None
    definition_source: Optional[str] = None
    pronunciation_source: Optional[str] = None
    etymology_source: Optional[str] = None

def load_checkpoint_and_generate_csvs():
    """Load checkpoint data and generate CSV files"""
    output_folder = Path("output")
    checkpoint_file = output_folder / "improved_checkpoint.json"
    words_file = output_folder / "spelling_words_final.csv"
    review_file = output_folder / "words_for_review.csv"
    
    # Load checkpoint
    with open(checkpoint_file, 'r', encoding='utf-8') as f:
        checkpoint_data = json.load(f)
    
    processed_words = {}
    for word, word_data in checkpoint_data.get('processed_words', {}).items():
        processed_words[word] = SpellingWord(**word_data)
    
    words_for_review = checkpoint_data.get('words_for_review', [])
    
    # Database schema field names (from setupSpellingBeeTables.ts)
    fieldnames = [
        'word', 'definition', 'pronunciation', 'etymology', 'language_origins',
        'example_sentence', 'difficulty', 'source_difficulty', 'source',
        'source_url', 'definition_source', 'pronunciation_source', 'etymology_source'
    ]
    
    # Write main words file
    print(f"Writing {len(processed_words)} words to {words_file}")
    with open(words_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        
        for word in sorted(processed_words.keys()):
            word_data = processed_words[word]
            row = {
                'word': word_data.word,
                'definition': word_data.definition or "",
                'pronunciation': word_data.pronunciation or "",
                'etymology': word_data.etymology or "",
                'language_origins': word_data.language_origins or "",
                'example_sentence': word_data.example_sentence or "",
                'difficulty': word_data.difficulty or "",
                'source_difficulty': word_data.source_difficulty or "",
                'source': word_data.source or "",
                'source_url': word_data.source_url or "",
                'definition_source': word_data.definition_source or "",
                'pronunciation_source': word_data.pronunciation_source or "",
                'etymology_source': word_data.etymology_source or ""
            }
            writer.writerow(row)
    
    # Write review file
    print(f"Writing {len(words_for_review)} review words to {review_file}")
    with open(review_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['word', 'reason'])
        for word_reason in words_for_review:
            if isinstance(word_reason, list) and len(word_reason) == 2:
                writer.writerow(word_reason)
            else:
                writer.writerow([str(word_reason), "Unknown reason"])
    
    print("CSV files generated successfully!")
    print(f"✅ Main file: {words_file}")
    print(f"🔍 Review file: {review_file}")

if __name__ == "__main__":
    load_checkpoint_and_generate_csvs()