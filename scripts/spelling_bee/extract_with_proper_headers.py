#!/usr/bin/env python3
"""
Proper PDF Header-Based Spelling Bee Extractor
Extracts words from Scripps National Spelling Bee PDFs by properly reading page headers
to determine One Bee, Two Bee, Three Bee difficulty classifications
"""

import os
import sys
import json
import re
import time
import csv
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import logging
import PyPDF2
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('proper_header_extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ExtractedWord:
    """Word with its source difficulty from PDF headers"""
    word: str
    source_difficulty: str  # "One Bee", "Two Bee", "Three Bee"
    source_year: str
    page_number: int
    source_file: str

class ProperHeaderExtractor:
    """Extracts words with correct difficulty levels based on PDF page headers"""
    
    def __init__(self):
        self.input_dir = Path("../../src/data/spelling_bee/input")
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Patterns to identify difficulty headers in PDFs
        self.header_patterns = [
            r"ONE\s+BEE",
            r"1\s+BEE", 
            r"TWO\s+BEE",
            r"2\s+BEE",
            r"THREE\s+BEE", 
            r"3\s+BEE",
            # Also look for section headers
            r"One\s+Bee\s+Words",
            r"Two\s+Bee\s+Words", 
            r"Three\s+Bee\s+Words"
        ]
        
        # Word patterns - looking for actual words, not headers
        self.word_patterns = [
            r'\b[a-zA-Z]{2,}(?:[a-zA-Z\-\']*[a-zA-Z])?\b'  # Basic word pattern
        ]
        
        # Common non-words to filter out - expanded list
        self.filter_patterns = [
            # Common English words that shouldn't be in spelling bee lists
            r'^(the|and|of|to|a|in|for|is|on|that|by|this|with|i|you|it|not|or|be|are|from|at|as|your|all|any|can|had|her|was|one|our|out|day|get|has|him|his|how|its|may|new|now|old|see|two|way|who|boy|did|its|let|put|say|she|too|use|about|after|also|an|another|before|come|could|do|even|first|give|go|good|here|just|know|last|life|look|make|man|many|most|over|own|people|place|right|same|should|since|some|still|such|take|than|them|these|they|think|three|through|time|very|want|water|well|were|what|when|where|will|work|would|year|years)$',
            # PDF/document related words
            r'^(page|pages|chapter|section|introduction|guide|study|resource|official|perfect|start|prepare|winning|school|attending|found|ve|so|greetings|champions|dream|digital|technology|measurement|services|award|winning|investigative|reporting|newsroom|longtime|steward|founded|decades|give|light)$',
            # Organization/competition related
            r'^(scripps|national|spelling|championship|bee|competition|contest)$',
            # Numbers and short words
            r'^\d+$',  # Pure numbers
            r'^[^\w\s]+$',  # Only punctuation
            r'^.{1,2}$',  # Very short words (1-2 characters)
            # Header-like patterns
            r'bee$',  # Ends with 'bee' (likely headers)
            r'words?$',  # Ends with 'word' or 'words' (likely headers)
            r'level$',  # Competition levels
            r'list$',  # Word lists
        ]
    
    def extract_year_from_filename(self, filename: str) -> str:
        """Extract year from PDF filename"""
        # Look for 4-digit year in filename
        year_match = re.search(r'20\d{2}', filename)
        if year_match:
            return year_match.group()
        return "unknown"
    
    def identify_difficulty_from_text(self, text: str) -> Optional[str]:
        """Identify difficulty level from page text/headers"""
        text_upper = text.upper()
        
        # Check for explicit difficulty markers
        if re.search(r'(ONE|1)\s+(BEE|B)', text_upper):
            return "One Bee"
        elif re.search(r'(TWO|2)\s+(BEE|B)', text_upper): 
            return "Two Bee"
        elif re.search(r'(THREE|3)\s+(BEE|B)', text_upper):
            return "Three Bee"
        
        return None
    
    def is_valid_word(self, word: str) -> bool:
        """Check if extracted text is a valid spelling bee word"""
        if not word or len(word) < 2:
            return False
            
        word_lower = word.lower()
        
        # Check against filter patterns
        for pattern in self.filter_patterns:
            if re.match(pattern, word_lower, re.IGNORECASE):
                return False
        
        # Must contain only letters, apostrophes, and hyphens
        if not re.match(r"^[a-zA-Z\-']+$", word):
            return False
            
        # Must start and end with letters
        if not (word[0].isalpha() and word[-1].isalpha()):
            return False
            
        return True
    
    def extract_words_from_pdf(self, pdf_path: Path) -> List[ExtractedWord]:
        """Extract words from a single PDF with proper difficulty classification"""
        logger.info(f"Processing PDF: {pdf_path.name}")
        
        extracted_words = []
        year = self.extract_year_from_filename(pdf_path.name)
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                current_difficulty = None  # Track current section difficulty
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        text = page.extract_text()
                        if not text:
                            continue
                            
                        # Check if this page has a difficulty header
                        page_difficulty = self.identify_difficulty_from_text(text)
                        if page_difficulty:
                            current_difficulty = page_difficulty
                            logger.info(f"  Page {page_num + 1}: Found {page_difficulty} section")
                        
                        # Only extract words if we know the current difficulty
                        if current_difficulty:
                            # Look for word lists - they often appear in specific patterns
                            # Try to find words that are isolated or in lists, not in sentences
                            lines = text.split('\n')
                            
                            for line in lines:
                                line = line.strip()
                                if not line:
                                    continue
                                
                                # Skip header lines and introductory text
                                if any(header in line.upper() for header in ['BEE', 'SCRIPPS', 'WORDS', 'LEVEL', 'COMPETITION', 'GUIDE', 'STUDY']):
                                    continue
                                
                                # Look for single words or short phrases that could be spelling bee words
                                # Skip lines that look like sentences (have multiple common words)
                                common_sentence_indicators = ['the ', ' and ', ' of ', ' to ', ' in ', ' for ', ' is ', ' are ', ' with ']
                                if any(indicator in line.lower() for indicator in common_sentence_indicators):
                                    continue
                                
                                # Extract words from this line
                                words_in_line = re.findall(r'\b[a-zA-Z][a-zA-Z\-\']*[a-zA-Z]\b', line)
                                
                                # If line has only 1-3 words, they're more likely to be spelling bee words
                                if 1 <= len(words_in_line) <= 3:
                                    for word in words_in_line:
                                        cleaned_word = word.strip().lower()
                                        
                                        if self.is_valid_word(cleaned_word) and len(cleaned_word) >= 3:
                                            extracted_words.append(ExtractedWord(
                                                word=cleaned_word,
                                                source_difficulty=current_difficulty,
                                                source_year=year,
                                                page_number=page_num + 1,
                                                source_file=pdf_path.name
                                            ))
                    
                    except Exception as e:
                        logger.warning(f"  Error processing page {page_num + 1}: {e}")
                        continue
        
        except Exception as e:
            logger.error(f"Error processing {pdf_path.name}: {e}")
            return []
        
        # Remove duplicates while preserving first occurrence
        unique_words = {}
        for word_obj in extracted_words:
            if word_obj.word not in unique_words:
                unique_words[word_obj.word] = word_obj
        
        unique_list = list(unique_words.values())
        logger.info(f"  Extracted {len(unique_list)} unique words from {pdf_path.name}")
        
        return unique_list
    
    def process_all_pdfs(self) -> Dict[str, List[ExtractedWord]]:
        """Process all PDFs in the input directory"""
        logger.info("Starting proper header-based extraction from all PDFs...")
        
        if not self.input_dir.exists():
            logger.error(f"Input directory not found: {self.input_dir}")
            return {}
        
        all_extractions = {}
        pdf_files = list(self.input_dir.glob("*.pdf"))
        
        if not pdf_files:
            logger.error("No PDF files found in input directory")
            return {}
        
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        for pdf_file in sorted(pdf_files):
            words = self.extract_words_from_pdf(pdf_file)
            all_extractions[pdf_file.name] = words
            
            # Log difficulty distribution for this file
            if words:
                difficulty_counts = {}
                for word in words:
                    difficulty_counts[word.source_difficulty] = difficulty_counts.get(word.source_difficulty, 0) + 1
                
                logger.info(f"  {pdf_file.name} difficulty distribution:")
                for diff, count in sorted(difficulty_counts.items()):
                    logger.info(f"    {diff}: {count} words")
        
        return all_extractions
    
    def save_extraction_results(self, extractions: Dict[str, List[ExtractedWord]]):
        """Save extraction results to files"""
        timestamp = int(time.time() * 1000)
        
        # Combine all words
        all_words = []
        for file_words in extractions.values():
            all_words.extend(file_words)
        
        # Create CSV for database import
        csv_file = self.output_dir / f"proper_header_extraction_{timestamp}.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['word', 'source_difficulty', 'source_year', 'page_number', 'source_file'])
            
            for word_obj in all_words:
                writer.writerow([
                    word_obj.word,
                    word_obj.source_difficulty, 
                    word_obj.source_year,
                    word_obj.page_number,
                    word_obj.source_file
                ])
        
        # Create summary JSON
        summary = {
            'total_words': len(all_words),
            'files_processed': len(extractions),
            'difficulty_distribution': {},
            'year_distribution': {},
            'extraction_timestamp': timestamp
        }
        
        for word_obj in all_words:
            # Count by difficulty
            difficulty = word_obj.source_difficulty
            summary['difficulty_distribution'][difficulty] = summary['difficulty_distribution'].get(difficulty, 0) + 1
            
            # Count by year  
            year = word_obj.source_year
            summary['year_distribution'][year] = summary['year_distribution'].get(year, 0) + 1
        
        summary_file = self.output_dir / f"proper_header_summary_{timestamp}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"\n✅ Extraction complete!")
        logger.info(f"📄 CSV file: {csv_file}")
        logger.info(f"📊 Summary file: {summary_file}")
        logger.info(f"📈 Total words extracted: {len(all_words)}")
        
        # Print overall statistics
        logger.info(f"\n📊 Overall Statistics:")
        logger.info(f"Difficulty Distribution:")
        for diff, count in sorted(summary['difficulty_distribution'].items()):
            percentage = (count / len(all_words)) * 100
            logger.info(f"  {diff}: {count} words ({percentage:.1f}%)")
        
        logger.info(f"\nYear Distribution:")
        for year, count in sorted(summary['year_distribution'].items()):
            percentage = (count / len(all_words)) * 100
            logger.info(f"  {year}: {count} words ({percentage:.1f}%)")

def main():
    """Main execution function"""
    import time
    
    extractor = ProperHeaderExtractor()
    
    # Process all PDFs
    extractions = extractor.process_all_pdfs()
    
    if extractions:
        extractor.save_extraction_results(extractions)
    else:
        logger.error("No words were extracted. Check the PDF files and extraction logic.")

if __name__ == "__main__":
    main()