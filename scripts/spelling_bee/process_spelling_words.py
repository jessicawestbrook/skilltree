import os
import sys
import csv
import json
import time
import re
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
import requests
import PyPDF2
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('spelling_bee_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class SpellingWord:
    word: str
    definition: str = ""
    example_sentence: str = ""
    difficulty_level: int = 0
    difficulty_name: str = ""
    etymology: str = ""
    language_origin: str = ""
    pronunciation: str = ""
    pronunciation_ipa: str = ""
    pronunciation_tips: str = ""
    common_misspellings: List[str] = None
    audio_url: str = ""
    source_name: str = "Scripps National Spelling Bee"
    source_url: str = ""
    source_difficulty: str = ""
    source_year: str = ""
    definition_source: str = ""
    etymology_source: str = ""
    pronunciation_source: str = ""
    example_source: str = ""
    
    def __post_init__(self):
        if self.common_misspellings is None:
            self.common_misspellings = []

class SpellingBeeProcessor:
    def __init__(self, pdf_folder: str, output_folder: str = "output"):
        self.pdf_folder = Path(pdf_folder)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
        
        self.checkpoint_file = self.output_folder / "checkpoint.json"
        self.words_file = self.output_folder / "spelling_words.csv"
        self.review_file = self.output_folder / "words_for_review.csv"
        self.processed_words: Dict[str, SpellingWord] = {}
        self.words_for_review: List[str] = []
        self.checkpoint_data = self.load_checkpoint()
        
        self.api_delay = 1.0
        self.batch_size = 100
        
    def load_checkpoint(self) -> dict:
        if self.checkpoint_file.exists():
            with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Loaded checkpoint: {len(data.get('processed_words', {}))} words processed")
                return data
        return {
            'processed_words': {},
            'words_for_review': [],
            'last_processed_index': 0,
            'current_pdf': None
        }
    
    def save_checkpoint(self):
        checkpoint = {
            'processed_words': {word: asdict(data) for word, data in self.processed_words.items()},
            'words_for_review': self.words_for_review,
            'last_processed_index': len(self.processed_words),
            'current_pdf': None,
            'timestamp': datetime.now().isoformat()
        }
        with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2, ensure_ascii=False)
        logger.info(f"Checkpoint saved: {len(self.processed_words)} words")
    
    def extract_words_from_pdf(self, pdf_path: Path) -> List[Tuple[str, str]]:
        """Extract words from PDF, returns list of (word, source_info) tuples"""
        words = []
        year = re.search(r'(\d{4})', pdf_path.name)
        year_str = year.group(1) if year else "Unknown"
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    
                    lines = text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        potential_words = re.findall(r'\b[a-z]+\b', line.lower())
                        
                        for word in potential_words:
                            if 3 <= len(word) <= 30 and word.isalpha():
                                words.append((word, year_str))
                    
                    if (page_num + 1) % 10 == 0:
                        logger.info(f"Processed {page_num + 1}/{len(pdf_reader.pages)} pages from {pdf_path.name}")
        
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {e}")
        
        return words
    
    def clean_words(self, words: List[Tuple[str, str]]) -> Dict[str, str]:
        """Clean and deduplicate words, returns dict of word -> source_year"""
        cleaned = {}
        
        for word, year in words:
            word = word.lower().strip()
            
            if word and word not in cleaned:
                if self.is_valid_word(word):
                    cleaned[word] = year
        
        logger.info(f"Cleaned {len(cleaned)} unique words from {len(words)} total")
        return cleaned
    
    def is_valid_word(self, word: str) -> bool:
        """Basic validation for spelling bee words"""
        if len(word) < 3 or len(word) > 30:
            return False
        
        common_non_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'got', 'has', 'him',
            'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way',
            'who', 'boy', 'did', 'she', 'too', 'use'
        }
        
        if word in common_non_words and len(word) < 4:
            return False
        
        return True
    
    def fetch_dictionary_data(self, word: str) -> Optional[dict]:
        """Fetch definition and pronunciation from Free Dictionary API"""
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        
        try:
            time.sleep(self.api_delay)
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list) and len(data) > 0:
                    return data[0]
            elif response.status_code == 429:
                logger.warning(f"Rate limited, waiting 5 seconds...")
                time.sleep(5)
                return self.fetch_dictionary_data(word)
        
        except Exception as e:
            logger.error(f"Error fetching dictionary data for '{word}': {e}")
        
        return None
    
    def fetch_wiktionary_data(self, word: str) -> Optional[dict]:
        """Fetch etymology from Wiktionary API"""
        url = "https://en.wiktionary.org/w/api.php"
        params = {
            'action': 'parse',
            'page': word,
            'prop': 'wikitext',
            'format': 'json',
            'formatversion': '2'
        }
        
        try:
            time.sleep(self.api_delay)
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'parse' in data:
                    return data['parse']
        
        except Exception as e:
            logger.error(f"Error fetching Wiktionary data for '{word}': {e}")
        
        return None
    
    def extract_etymology(self, wikitext: str) -> Tuple[str, str]:
        """Extract etymology and language origin from wikitext"""
        etymology = ""
        language_origin = ""
        
        etymology_match = re.search(r'===Etymology===\n(.*?)(?:\n==|\n\[\[|\Z)', wikitext, re.DOTALL)
        if etymology_match:
            etymology_text = etymology_match.group(1).strip()
            etymology = re.sub(r'\[\[([^\]]+)\]\]', r'\1', etymology_text)
            etymology = re.sub(r'\{\{[^}]+\}\}', '', etymology)
            etymology = etymology[:500]
            
            origin_patterns = [
                r'From (\w+)',
                r'Borrowed from (\w+)',
                r'(\w+) origin',
                r'ultimately from (\w+)'
            ]
            
            for pattern in origin_patterns:
                match = re.search(pattern, etymology, re.IGNORECASE)
                if match:
                    language_origin = match.group(1).capitalize()
                    break
        
        return etymology, language_origin
    
    def generate_example_sentence(self, word: str, definition: str) -> str:
        """Generate an example sentence with blank for the word"""
        templates = {
            'verb': [
                f"She will ___ the task tomorrow.",
                f"They decided to ___ after careful consideration.",
                f"We need to ___ before the deadline."
            ],
            'noun': [
                f"The ___ was clearly visible from here.",
                f"She studied the ___ carefully.",
                f"The ___ made everyone happy."
            ],
            'adjective': [
                f"The ___ weather made the day perfect.",
                f"It was a very ___ situation.",
                f"The ___ student completed the assignment."
            ],
            'adverb': [
                f"She spoke ___ during the presentation.",
                f"They worked ___ to finish on time.",
                f"The team performed ___ well."
            ]
        }
        
        if 'verb' in definition.lower()[:50]:
            return templates['verb'][0]
        elif 'noun' in definition.lower()[:50]:
            return templates['noun'][0]
        elif 'adjective' in definition.lower()[:50] or 'adj.' in definition.lower()[:50]:
            return templates['adjective'][0]
        elif 'adverb' in definition.lower()[:50]:
            return templates['adverb'][0]
        else:
            return f"The word ___ is important to understand."
    
    def assign_difficulty_level(self, word: str, year: str) -> Tuple[int, str]:
        """Assign difficulty level based on word characteristics and year"""
        difficulty_map = {
            '2020': 1, '2021': 2, '2022': 2,
            '2023': 3, '2024': 3, '2025': 4
        }
        
        base_level = difficulty_map.get(year, 3)
        
        length = len(word)
        if length <= 5:
            level = min(1, base_level)
        elif length <= 7:
            level = min(2, base_level)
        elif length <= 10:
            level = base_level
        elif length <= 13:
            level = min(4, base_level + 1)
        else:
            level = 5
        
        difficulty_names = {
            1: "Beginner",
            2: "Elementary", 
            3: "Intermediate",
            4: "Advanced",
            5: "Expert"
        }
        
        return level, difficulty_names[level]
    
    def generate_pronunciation_tips(self, word: str) -> str:
        """Generate mnemonic tips for remembering spelling"""
        tips = []
        
        double_letters = re.findall(r'([a-z])\1', word)
        if double_letters:
            tips.append(f"Remember the double {', '.join([letter.upper() for letter in set(double_letters)])}")
        
        if 'ph' in word:
            tips.append("'PH' makes an 'F' sound")
        if 'gh' in word:
            tips.append("Watch for the silent 'GH'")
        if word.endswith('tion'):
            tips.append("Ends with '-TION' (sounds like 'shun')")
        if word.endswith('sion'):
            tips.append("Ends with '-SION' (sounds like 'zhun')")
        
        if 'ie' in word:
            tips.append("Remember: 'I before E'")
        elif 'ei' in word:
            tips.append("Remember: 'E before I' (exception to the rule)")
        
        return "; ".join(tips) if tips else ""
    
    def process_word(self, word: str, year: str) -> SpellingWord:
        """Process a single word through all APIs and enrichment"""
        spelling_word = SpellingWord(
            word=word,
            source_year=year,
            source_name="Scripps National Spelling Bee"
        )
        
        dict_data = self.fetch_dictionary_data(word)
        if dict_data:
            if 'meanings' in dict_data and dict_data['meanings']:
                meaning = dict_data['meanings'][0]
                if 'definitions' in meaning and meaning['definitions']:
                    spelling_word.definition = meaning['definitions'][0].get('definition', '')[:500]
                    spelling_word.definition_source = "Dictionary API"
            
            if 'phonetics' in dict_data and dict_data['phonetics']:
                for phonetic in dict_data['phonetics']:
                    if 'text' in phonetic:
                        spelling_word.pronunciation_ipa = phonetic['text']
                        spelling_word.pronunciation_source = "Dictionary API"
                        break
                    
                    if 'audio' in phonetic and phonetic['audio']:
                        spelling_word.audio_url = phonetic['audio']
        
        if not spelling_word.definition:
            self.words_for_review.append(word)
            logger.warning(f"No definition found for '{word}', adding to review list")
        
        wiki_data = self.fetch_wiktionary_data(word)
        if wiki_data and 'wikitext' in wiki_data:
            etymology, language = self.extract_etymology(wiki_data['wikitext'])
            if etymology:
                spelling_word.etymology = etymology
                spelling_word.language_origin = language
                spelling_word.etymology_source = "Wiktionary"
        
        if not spelling_word.etymology:
            spelling_word.etymology = self.generate_etymology(word)
            spelling_word.etymology_source = "Claude"
        
        if spelling_word.definition:
            spelling_word.example_sentence = self.generate_example_sentence(word, spelling_word.definition)
            spelling_word.example_source = "Claude"
        
        level, name = self.assign_difficulty_level(word, year)
        spelling_word.difficulty_level = level
        spelling_word.difficulty_name = name
        spelling_word.source_difficulty = f"Year {year}"
        
        spelling_word.pronunciation_tips = self.generate_pronunciation_tips(word)
        
        return spelling_word
    
    def generate_etymology(self, word: str) -> str:
        """Generate etymology based on word patterns and common roots"""
        etymologies = {
            'tion': "Latin suffix '-tion' meaning 'act or process of'",
            'sion': "Latin suffix '-sion' meaning 'state or quality'",
            'ment': "Latin suffix '-ment' meaning 'result or means'",
            'able': "Latin suffix '-able' meaning 'capable of'",
            'ible': "Latin suffix '-ible' meaning 'capable of'",
            'ology': "Greek suffix '-ology' meaning 'study of'",
            'graph': "Greek root 'graph' meaning 'to write'",
            'phon': "Greek root 'phon' meaning 'sound'",
            'bio': "Greek root 'bio' meaning 'life'",
            'geo': "Greek root 'geo' meaning 'earth'",
            'chron': "Greek root 'chron' meaning 'time'",
            'tele': "Greek prefix 'tele' meaning 'distant'",
            'micro': "Greek prefix 'micro' meaning 'small'",
            'macro': "Greek prefix 'macro' meaning 'large'"
        }
        
        for pattern, etymology in etymologies.items():
            if pattern in word:
                return f"Contains {etymology}"
        
        if word.startswith('un'):
            return "Old English prefix 'un-' meaning 'not'"
        elif word.startswith('re'):
            return "Latin prefix 're-' meaning 'again' or 'back'"
        elif word.startswith('pre'):
            return "Latin prefix 'pre-' meaning 'before'"
        elif word.startswith('dis'):
            return "Latin prefix 'dis-' meaning 'apart' or 'not'"
        
        return "Etymology uncertain"
    
    def process_all_pdfs(self):
        """Main processing function for all PDFs"""
        pdf_files = list(self.pdf_folder.glob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        if self.checkpoint_data['processed_words']:
            for word_data in self.checkpoint_data['processed_words'].values():
                word_obj = SpellingWord(**word_data)
                self.processed_words[word_obj.word] = word_obj
            self.words_for_review = self.checkpoint_data.get('words_for_review', [])
            logger.info(f"Restored {len(self.processed_words)} words from checkpoint")
        
        all_words = {}
        for pdf_file in pdf_files:
            logger.info(f"Processing {pdf_file.name}...")
            extracted = self.extract_words_from_pdf(pdf_file)
            cleaned = self.clean_words(extracted)
            all_words.update(cleaned)
        
        unique_words = set(all_words.keys()) - set(self.processed_words.keys())
        logger.info(f"Found {len(unique_words)} new unique words to process")
        
        word_list = list(unique_words)
        batch_count = 0
        
        for i in range(0, len(word_list), self.batch_size):
            batch = word_list[i:i+self.batch_size]
            batch_count += 1
            logger.info(f"Processing batch {batch_count} ({i+1}-{min(i+len(batch), len(word_list))} of {len(word_list)})")
            
            for word in batch:
                if word not in self.processed_words:
                    try:
                        year = all_words[word]
                        spelling_word = self.process_word(word, year)
                        self.processed_words[word] = spelling_word
                        logger.info(f"Processed: {word} (Level {spelling_word.difficulty_level})")
                    except Exception as e:
                        logger.error(f"Error processing '{word}': {e}")
                        self.words_for_review.append(word)
            
            self.save_checkpoint()
            logger.info(f"Checkpoint saved after batch {batch_count}")
    
    def write_csv_files(self):
        """Write final CSV files for database upload and review"""
        fieldnames = [
            'word', 'definition', 'example_sentence', 'difficulty_level', 'difficulty_name',
            'etymology', 'language_origin', 'pronunciation', 'pronunciation_ipa',
            'pronunciation_tips', 'common_misspellings', 'audio_url',
            'source_name', 'source_url', 'source_difficulty', 'source_year',
            'definition_source', 'etymology_source', 'pronunciation_source', 'example_source'
        ]
        
        with open(self.words_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            
            for word in sorted(self.processed_words.keys()):
                word_data = self.processed_words[word]
                row = asdict(word_data)
                row['common_misspellings'] = json.dumps(row['common_misspellings'])
                writer.writerow(row)
        
        logger.info(f"Wrote {len(self.processed_words)} words to {self.words_file}")
        
        with open(self.review_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(['word', 'reason'])
            for word in sorted(set(self.words_for_review)):
                writer.writerow([word, 'No definition found'])
        
        logger.info(f"Wrote {len(self.words_for_review)} words for review to {self.review_file}")
    
    def run(self):
        """Execute the complete processing pipeline"""
        logger.info("Starting spelling bee data processing...")
        logger.info(f"PDF folder: {self.pdf_folder}")
        logger.info(f"Output folder: {self.output_folder}")
        
        try:
            self.process_all_pdfs()
            self.write_csv_files()
            logger.info("Processing complete!")
            logger.info(f"Total words processed: {len(self.processed_words)}")
            logger.info(f"Words needing review: {len(self.words_for_review)}")
        except KeyboardInterrupt:
            logger.info("Processing interrupted by user. Progress saved.")
            self.save_checkpoint()
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            self.save_checkpoint()
            raise

def main():
    pdf_folder = r"C:\Users\jessi\Projects\skilltree2\src\data\spelling_bee"
    output_folder = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output"
    
    processor = SpellingBeeProcessor(pdf_folder, output_folder)
    processor.run()

if __name__ == "__main__":
    main()