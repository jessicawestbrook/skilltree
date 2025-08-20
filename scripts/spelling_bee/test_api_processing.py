#!/usr/bin/env python3
"""
Test API processing with a small batch
"""

import csv
import sys
from pathlib import Path
from api_processor import BatchProcessor, WordData

def test_processing():
    """Test API processing with first 10 words"""
    processor = BatchProcessor()
    input_csv = Path("output/extracted_words_for_review.csv")
    
    if not input_csv.exists():
        print(f"Error: {input_csv} not found")
        return
    
    # Load first 10 words for testing
    test_words = []
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= 10:
                break
            word_data = WordData(
                word=row['word'],
                years=row['years'],
                source_files=row['source_files'],
                source_difficulties=row['source_difficulties']
            )
            test_words.append(word_data)
    
    print(f"Testing API processing with {len(test_words)} words...")
    print("Words to test:", [w.word for w in test_words])
    
    # Process test words
    successful = []
    failed = []
    
    for i, word_data in enumerate(test_words):
        print(f"\nProcessing {i+1}/{len(test_words)}: {word_data.word}")
        processed = processor.claude_processor.process_word(word_data)
        
        if processed.claude_definition:
            successful.append(processed)
            print(f"  SUCCESS - Got Claude definition and data")
        else:
            failed.append(processed)
            print(f"  FAILED - {processed.error_notes}")
    
    # Save test results
    if successful:
        processor.save_progress_csv(successful, "test_successful_words.csv")
        print(f"\nSaved {len(successful)} successful words to test_successful_words.csv")
    
    if failed:
        processor.save_progress_csv(failed, "test_failed_words.csv")
        print(f"Saved {len(failed)} failed words to test_failed_words.csv")
    
    # Print summary
    print(f"\nTest Results:")
    print(f"  Successful: {len(successful)}/{len(test_words)}")
    print(f"  Failed: {len(failed)}/{len(test_words)}")
    print(f"  Success rate: {len(successful)/len(test_words)*100:.1f}%")
    
    # Show sample successful result
    if successful:
        sample = successful[0]
        print(f"\nSample successful result for '{sample.word}':")
        print(f"  Definition: {sample.claude_definition[:200]}...")
        print(f"  Pronunciation: {sample.pronunciation_guide}")
        print(f"  Example: {sample.example_sentence}")
        print(f"  Difficulty: {processor.claude_processor.difficulty_calculator.calculate_overall_difficulty(sample)}")

if __name__ == "__main__":
    test_processing()