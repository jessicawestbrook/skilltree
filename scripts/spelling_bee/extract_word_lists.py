#!/usr/bin/env python3
"""
Extract actual spelling bee word lists from Scripps PDFs for review
Focus on finding the real word lists, not extracting random text
"""

import os
import re
import csv
from pathlib import Path
from typing import List, Tuple, Set
import PyPDF2
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('word_extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SpellingBeeWordExtractor:
    """Extract actual spelling bee words from Scripps PDFs"""
    
    def __init__(self, pdf_folder: str, output_folder: str = "output"):
        self.pdf_folder = Path(pdf_folder)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
        
        # Output files
        self.word_list_file = self.output_folder / "extracted_words_for_review.csv"
        self.stats_file = self.output_folder / "extraction_stats.txt"
        
        logger.info(f"Initialized extractor: PDF folder={self.pdf_folder}, Output={self.output_folder}")
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract all text from PDF"""
        full_text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        text = page.extract_text()
                        full_text += text + "\n"
                    except Exception as e:
                        logger.warning(f"Error extracting page {page_num + 1} from {pdf_path.name}: {e}")
                        continue
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {e}")
        
        return full_text
    
    def find_word_list_sections(self, text: str) -> List[str]:
        """Find sections that contain actual word lists"""
        # Look for patterns that indicate word lists
        # Scripps PDFs often have words in lists, sometimes numbered
        
        # Split text into sections by common delimiters
        sections = []
        
        # Split by double newlines (paragraph breaks)
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            # Clean up the paragraph
            para = paragraph.strip()
            if not para:
                continue
            
            # Look for sections that might contain word lists
            # Check if paragraph has multiple words that look like spelling bee words
            words_in_para = self.extract_potential_words(para)
            
            if len(words_in_para) >= 3:  # At least 3 potential words
                sections.append(para)
        
        return sections
    
    def extract_potential_words(self, text: str) -> List[str]:
        """Extract potential spelling bee words from text"""
        # Look for words that could be spelling bee words
        words = []
        
        # Split text by common delimiters
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try different patterns to extract words
            # Pattern 1: Words at start of line (possibly numbered lists)
            # Remove numbers, bullets, etc.
            cleaned_line = re.sub(r'^\d+\.?\s*', '', line)  # Remove leading numbers
            cleaned_line = re.sub(r'^[•\-\*]\s*', '', cleaned_line)  # Remove bullets
            
            # Look for single words or words with simple definitions
            # Split by common separators but try to identify the main word
            potential_word = cleaned_line.split()[0] if cleaned_line.split() else ""
            
            if self.is_potential_spelling_word(potential_word):
                words.append(potential_word.lower())
            
            # Pattern 2: Look for words in the middle of lines too
            word_matches = re.findall(r'\b[a-zA-Z]{4,20}\b', line)
            for word in word_matches:
                if self.is_potential_spelling_word(word):
                    words.append(word.lower())
        
        return words
    
    def is_potential_spelling_word(self, word: str) -> bool:
        """Check if a word could be a legitimate spelling bee word"""
        if not word or not word.isalpha():
            return False
        
        # Length constraints
        if len(word) < 4 or len(word) > 20:
            return False
        
        # Skip very common words that wouldn't be in spelling bees
        common_skip = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'got', 'has', 'him',
            'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way',
            'who', 'boy', 'did', 'she', 'too', 'use', 'said', 'each', 'which', 'do',
            'will', 'about', 'many', 'then', 'them', 'these', 'some', 'would', 
            'make', 'like', 'into', 'time', 'more', 'very', 'what', 'know', 'just',
            'first', 'over', 'think', 'also', 'your', 'work', 'life', 'only', 'still',
            'should', 'after', 'being', 'made', 'before', 'here', 'through', 'when',
            'where', 'much', 'take', 'than', 'little', 'state', 'years', 'came',
            'show', 'every', 'good', 'give', 'under', 'name', 'this', 'that', 'with',
            'from', 'they', 'have', 'been', 'could', 'were', 'said', 'each', 'which',
            'their', 'time', 'will', 'about', 'there', 'would', 'other', 'after',
            'first', 'well', 'water', 'been', 'call', 'who', 'its', 'now', 'find',
            'long', 'down', 'day', 'did', 'get', 'come', 'made', 'may', 'part',
            'words', 'spelling', 'bee', 'national', 'scripps', 'champion', 'champions',
            'study', 'guide', 'word', 'list', 'page', 'grade', 'level', 'school',
            'district', 'regional', 'competition', 'contest'
        }
        
        if word.lower() in common_skip:
            return False
        
        # Skip instructional words
        instructional = {
            'instructions', 'rules', 'guidelines', 'steps', 'procedure', 'method',
            'practice', 'preparation', 'training', 'tutorial', 'lesson', 'chapter',
            'section', 'appendix', 'introduction', 'conclusion', 'summary', 'note',
            'example', 'sample', 'demonstration', 'illustration', 'explanation'
        }
        
        if word.lower() in instructional:
            return False
        
        # Skip if it's all uppercase (likely headers)
        if word.isupper() and len(word) > 3:
            return False
        
        # Skip if it contains numbers
        if re.search(r'\d', word):
            return False
        
        return True
    
    def extract_words_from_pdf(self, pdf_path: Path) -> Tuple[List[str], str]:
        """Extract words from a single PDF"""
        logger.info(f"Processing {pdf_path.name}")
        
        # Extract year from filename
        year_match = re.search(r'(\d{4})', pdf_path.name)
        year = year_match.group(1) if year_match else "Unknown"
        
        # Extract text
        full_text = self.extract_text_from_pdf(pdf_path)
        
        # Find word list sections
        word_sections = self.find_word_list_sections(full_text)
        
        # Extract words from all sections
        all_words = set()
        for section in word_sections:
            words = self.extract_potential_words(section)
            all_words.update(words)
        
        # Convert to sorted list
        word_list = sorted(list(all_words))
        
        logger.info(f"Extracted {len(word_list)} potential words from {pdf_path.name} (Year: {year})")
        
        return word_list, year
    
    def process_all_pdfs(self) -> List[Tuple[str, str, str]]:
        """Process all PDFs and return (word, year, source_file) tuples"""
        pdf_files = list(self.pdf_folder.glob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        all_word_data = []
        total_stats = {}
        
        for pdf_file in pdf_files:
            words, year = self.extract_words_from_pdf(pdf_file)
            total_stats[pdf_file.name] = {
                'year': year,
                'word_count': len(words),
                'words': words
            }
            
            # Add to master list with metadata
            for word in words:
                all_word_data.append((word, year, pdf_file.name))
        
        # Write stats
        self.write_extraction_stats(total_stats)
        
        return all_word_data
    
    def write_extraction_stats(self, stats: dict):
        """Write extraction statistics"""
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            f.write("Spelling Bee Word Extraction Statistics\n")
            f.write("=" * 50 + "\n\n")
            
            total_words = 0
            for filename, data in stats.items():
                f.write(f"File: {filename}\n")
                f.write(f"Year: {data['year']}\n")
                f.write(f"Words extracted: {data['word_count']}\n")
                f.write(f"Sample words: {', '.join(data['words'][:10])}\n")
                f.write("-" * 30 + "\n")
                total_words += data['word_count']
            
            f.write(f"\nTotal unique words across all files: {total_words}\n")
    
    def save_words_for_review(self, word_data: List[Tuple[str, str, str]]):
        """Save extracted words to CSV for manual review"""
        # Year to Scripps difficulty mapping
        year_to_difficulty = {
            "2020": "One Bee",
            "2021": "One Bee", 
            "2022": "Two Bee",
            "2023": "Two Bee",
            "2024": "Three Bee",
            "2025": "Three Bee"
        }
        
        # Remove duplicates while preserving all source info
        unique_words = {}
        for word, year, source_file in word_data:
            if word not in unique_words:
                unique_words[word] = {
                    'years': [year],
                    'source_files': [source_file],
                    'source_difficulties': [year_to_difficulty.get(year, "Two Bee")]
                }
            else:
                # Track multiple sources and their difficulties
                if source_file not in unique_words[word]['source_files']:
                    unique_words[word]['source_files'].append(source_file)
                if year not in unique_words[word]['years']:
                    unique_words[word]['years'].append(year)
                    difficulty = year_to_difficulty.get(year, "Two Bee")
                    if difficulty not in unique_words[word]['source_difficulties']:
                        unique_words[word]['source_difficulties'].append(difficulty)
        
        # Write to CSV
        with open(self.word_list_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(['word', 'years', 'source_files', 'source_difficulties'])
            
            for word in sorted(unique_words.keys()):
                data = unique_words[word]
                years_list = '; '.join(sorted(data['years']))
                source_files = '; '.join(data['source_files'])
                difficulties = '; '.join(sorted(set(data['source_difficulties'])))
                
                writer.writerow([
                    word,
                    years_list,
                    source_files,
                    difficulties
                ])
        
        logger.info(f"Saved {len(unique_words)} unique words to {self.word_list_file}")
        return len(unique_words)
    
    def run_extraction(self):
        """Run the complete word extraction process"""
        logger.info("=== STARTING WORD EXTRACTION ===")
        
        try:
            # Process all PDFs
            word_data = self.process_all_pdfs()
            
            # Save for review
            unique_count = self.save_words_for_review(word_data)
            
            logger.info("=== EXTRACTION COMPLETED ===")
            logger.info(f"Total words extracted: {len(word_data)}")
            logger.info(f"Unique words: {unique_count}")
            logger.info(f"Word list saved to: {self.word_list_file}")
            logger.info(f"Statistics saved to: {self.stats_file}")
            
            print(f"\n✅ Word extraction completed!")
            print(f"📄 Review file: {self.word_list_file}")
            print(f"📊 Stats file: {self.stats_file}")
            print(f"📝 Log file: word_extraction.log")
            print(f"\nPlease review the extracted words before proceeding with API processing.")
            
        except Exception as e:
            logger.error(f"Fatal error during extraction: {e}")
            raise

def main():
    """Main entry point"""
    pdf_folder = r"C:\Users\jessi\Projects\skilltree2\src\data\spelling_bee\input"
    output_folder = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output"
    
    extractor = SpellingBeeWordExtractor(pdf_folder, output_folder)
    extractor.run_extraction()

if __name__ == "__main__":
    main()