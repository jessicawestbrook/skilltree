#!/usr/bin/env python3
"""
Batch Processing Script for Spelling Bee Words
Processes words in small batches to allow comprehensive Claude data generation
"""

import csv
import json
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class WordData:
    word: str
    years: str
    source_files: str
    source_difficulties: str
    definition: str = ""
    pronunciation: str = ""
    etymology: str = ""
    language_origins: str = ""
    example_sentence: str = ""
    definition_source: str = ""
    pronunciation_source: str = ""
    etymology_source: str = ""
    error_notes: str = ""
    # Claude-generated fields
    claude_definition: str = ""
    part_of_speech: str = ""
    pronunciation_guide: str = ""
    claude_etymology: str = ""
    memory_tips: str = ""
    alternate_spellings: str = ""
    claude_language_origin: str = ""

class BatchProcessor:
    def __init__(self, batch_size: int = 50):
        self.batch_size = batch_size
        self.output_folder = Path("output")
        
    def load_words_from_csv(self, csv_file: Path) -> List[WordData]:
        """Load words from extracted CSV"""
        words = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word_data = WordData(
                    word=row['word'],
                    years=row['years'],
                    source_files=row['source_files'],
                    source_difficulties=row['source_difficulties']
                )
                words.append(word_data)
        return words
    
    def create_batch_files(self, input_csv: Path):
        """Split the main CSV into smaller batch files"""
        words = self.load_words_from_csv(input_csv)
        total_words = len(words)
        logger.info(f"Splitting {total_words} words into batches of {self.batch_size}")
        
        # Create batch files
        for i in range(0, total_words, self.batch_size):
            batch_num = (i // self.batch_size) + 1
            batch_words = words[i:i + self.batch_size]
            
            batch_filename = self.output_folder / f"batch_{batch_num:03d}_words.csv"
            
            # Write batch CSV
            with open(batch_filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['word', 'years', 'source_files', 'source_difficulties']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for word_data in batch_words:
                    writer.writerow({
                        'word': word_data.word,
                        'years': word_data.years,
                        'source_files': word_data.source_files,
                        'source_difficulties': word_data.source_difficulties
                    })
            
            logger.info(f"Created {batch_filename} with {len(batch_words)} words")
            
            # Create info file with the words for this batch
            info_filename = self.output_folder / f"batch_{batch_num:03d}_info.txt"
            with open(info_filename, 'w', encoding='utf-8') as f:
                f.write(f"Batch {batch_num} - Words {i+1} to {min(i+self.batch_size, total_words)}\n")
                f.write(f"Total words in batch: {len(batch_words)}\n\n")
                f.write("Words in this batch:\n")
                for word_data in batch_words:
                    f.write(f"- {word_data.word}\n")
        
        total_batches = (total_words + self.batch_size - 1) // self.batch_size
        logger.info(f"Created {total_batches} batch files")
        
        return total_batches

def main():
    """Create batch files for processing"""
    processor = BatchProcessor(batch_size=50)  # 50 words per batch for manageable Claude data generation
    input_csv = Path("output/extracted_words_for_review.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    total_batches = processor.create_batch_files(input_csv)
    
    logger.info(f"""
Batch files created successfully!

Next steps:
1. Process each batch file (batch_001_words.csv, batch_002_words.csv, etc.)
2. For each batch, provide comprehensive Claude data for all {processor.batch_size} words
3. Combine all processed batches into final result

Total batches to process: {total_batches}
Words per batch: {processor.batch_size}
""")

if __name__ == "__main__":
    main()