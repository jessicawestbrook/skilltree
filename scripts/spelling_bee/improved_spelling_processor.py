#!/usr/bin/env python3
"""
Improved Spelling Bee Data Processor
Processes Scripps National Spelling Bee PDFs to create database-ready CSV files
"""

import os
import sys
import csv
import json
import time
import re
import math
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
import requests
import PyPDF2
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('improved_spelling_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

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

class DifficultyCalculator:
    """Implements the sophisticated difficulty rating system from THEORETICAL_FOUNDATIONS.md"""
    
    def __init__(self):
        self.difficulty_levels = {
            1: "Beginner",
            2: "Elementary", 
            3: "Intermediate",
            4: "Advanced",
            5: "Expert"
        }
        
        # Common word frequencies (simplified - in production would use corpus data)
        self.common_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'got', 'has', 'him',
            'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way',
            'who', 'boy', 'did', 'she', 'too', 'use', 'man', 'say', 'each', 'which'
        }
    
    def assess_phonetic_transparency(self, word: str, pronunciation_ipa: str = "") -> int:
        """Calculate phonetic transparency score (0-100)"""
        score = 85  # Base score
        
        # Silent letter patterns
        silent_patterns = [
            (r'mb$', -15), (r'bt$', -15), (r'ght', -15),
            (r'^kn', -15), (r'^wr', -15), (r'^gn', -15), (r'^ps', -15), (r'^pn', -15),
            (r'alk', -15), (r'alf', -15), (r'alm', -15), (r'ould', -15),
            (r'igh', -15), (r'eigh', -15)
        ]
        
        for pattern, penalty in silent_patterns:
            if re.search(pattern, word):
                score += penalty
        
        # Double consonants
        double_letters = len(re.findall(r'([a-z])\1', word))
        score -= double_letters * 5
        
        # Complex irregular patterns
        if re.search(r'ough|augh', word):
            score -= 20
        if re.search(r'eaux|ieux|oeuvre|aille|eille', word):
            score -= 20
        
        # Moderate irregular patterns
        if re.search(r'tion|sion|cian|ture|sure', word):
            score -= 10
        
        # Foreign vowel combinations
        if re.search(r'ae|oe|eu|eau|ieu|oeu|ui|oi', word):
            score -= 8
        
        # Greek/Latin combinations
        if re.search(r'ph|ps|ch|rh|mn', word):
            score -= 12
        
        return max(0, min(100, score))
    
    def get_word_frequency_score(self, word: str, source_difficulty: str, definition: str = "") -> int:
        """Calculate word frequency score (0-100)"""
        # Base score by source difficulty
        base_scores = {
            "One Bee": 75, "Two Bee": 45, "Three Bee": 15,
            "2020": 75, "2021": 65, "2022": 55, "2023": 35, "2024": 25, "2025": 15
        }
        
        score = base_scores.get(source_difficulty, 50)
        
        # Word length adjustments
        length = len(word)
        if length <= 4:
            score += 15
        elif length <= 6:
            score += 5
        elif length >= 10:
            score -= 10
        elif length >= 13:
            score -= 20
        
        # Definition complexity
        if definition:
            if len(definition) < 50:
                score += 10
            elif len(definition) > 150:
                score -= 10
            
            # Technical terms in definition
            technical_terms = ['technical', 'scientific', 'medical', 'botanical', 'anatomical', 'mathematical']
            if any(term in definition.lower() for term in technical_terms):
                score -= 15
        
        return max(0, min(100, score))
    
    def analyze_morphology_score(self, word: str, definition: str = "") -> int:
        """Calculate morphological complexity score (0-100)"""
        score = 80  # Base score
        
        # Length penalties
        length = len(word)
        if length > 12:
            score -= 15
        elif length > 8:
            score -= 10
        
        # Common affixes
        prefixes = ['un', 're', 'pre', 'dis', 'mis', 'over', 'under', 'out', 'sub', 'super']
        suffixes = ['ing', 'ed', 'er', 'ly', 'tion', 'sion', 'ment', 'ness', 'able', 'ible']
        
        for prefix in prefixes:
            if word.startswith(prefix):
                score -= 5
                break
        
        for suffix in suffixes:
            if word.endswith(suffix):
                score -= 5
                break
        
        # Compound word indicators
        if '-' in word:
            score -= 10
        
        # Multiple capitals (proper nouns)
        if sum(1 for c in word if c.isupper()) > 1:
            score -= 15
        
        return max(0, min(100, score))
    
    def score_etymology(self, etymology: str, language_origins: str) -> int:
        """Calculate etymology complexity score (0-100)"""
        score = 60  # Neutral base
        
        # Language origin adjustments
        if language_origins:
            lang = language_origins.lower()
            if any(origin in lang for origin in ['anglo', 'saxon', 'english', 'germanic']):
                score += 20
            elif any(origin in lang for origin in ['latin', 'greek']):
                score -= 10
            elif any(origin in lang for origin in ['french', 'italian', 'spanish']):
                score -= 15
            else:  # Non-European languages
                score -= 25
        
        # Etymology pattern recognition
        if etymology:
            etym = etymology.lower()
            if any(pattern in etym for pattern in ['anglo', 'saxon', 'old english']):
                score += 5
            elif any(pattern in etym for pattern in ['greek', 'latin', 'classical']):
                score -= 10
            elif 'french' in etym:
                score -= 15
        
        return max(0, min(100, score))
    
    def calculate_difficulty(self, word: str, source_difficulty: str = "", 
                           pronunciation_ipa: str = "", definition: str = "",
                           etymology: str = "", language_origins: str = "") -> Tuple[int, str]:
        """Calculate overall difficulty level using the 4-factor system"""
        
        phonetic_score = self.assess_phonetic_transparency(word, pronunciation_ipa)
        frequency_score = self.get_word_frequency_score(word, source_difficulty, definition)
        morphology_score = self.analyze_morphology_score(word, definition)
        etymology_score = self.score_etymology(etymology, language_origins)
        
        # Weighted average (as per THEORETICAL_FOUNDATIONS.md)
        weighted_score = (
            phonetic_score * 0.4 +
            frequency_score * 0.2 + 
            morphology_score * 0.2 +
            etymology_score * 0.2
        )
        
        # Map to 1-5 scale
        if weighted_score >= 80:
            level = 1
        elif weighted_score >= 60:
            level = 2
        elif weighted_score >= 40:
            level = 3
        elif weighted_score >= 20:
            level = 4
        else:
            level = 5
        
        return level, self.difficulty_levels[level]

class ImprovedSpellingProcessor:
    """Enhanced spelling bee processor with sophisticated algorithms"""
    
    def __init__(self, pdf_folder: str, output_folder: str = "output"):
        self.pdf_folder = Path(pdf_folder)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
        
        # File paths
        self.checkpoint_file = self.output_folder / "improved_checkpoint.json"
        self.words_file = self.output_folder / "spelling_words_final.csv"
        self.review_file = self.output_folder / "words_for_review.csv"
        self.log_file = self.output_folder / "processing_log.txt"
        
        # Processing state
        self.processed_words: Dict[str, SpellingWord] = {}
        self.words_for_review: List[Tuple[str, str]] = []  # (word, reason)
        self.checkpoint_data = self.load_checkpoint()
        
        # API settings
        self.api_delay = 1.2  # Slightly slower to be safe
        self.batch_size = 50  # Smaller batches for testing
        self.max_retries = 3
        
        # Initialize difficulty calculator
        self.difficulty_calc = DifficultyCalculator()
        
        logger.info(f"Initialized processor: PDF folder={self.pdf_folder}, Output={self.output_folder}")
    
    def load_checkpoint(self) -> dict:
        """Load processing checkpoint if it exists"""
        if self.checkpoint_file.exists():
            try:
                with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"Loaded checkpoint: {len(data.get('processed_words', {}))} words processed")
                    return data
            except Exception as e:
                logger.error(f"Error loading checkpoint: {e}")
        
        return {
            'processed_words': {},
            'words_for_review': [],
            'last_processed_index': 0,
            'processing_stats': {'total_words': 0, 'successful': 0, 'failed': 0}
        }
    
    def save_checkpoint(self):
        """Save current processing state"""
        try:
            checkpoint = {
                'processed_words': {word: asdict(data) for word, data in self.processed_words.items()},
                'words_for_review': self.words_for_review,
                'last_processed_index': len(self.processed_words),
                'processing_stats': {
                    'total_words': len(self.processed_words) + len(self.words_for_review),
                    'successful': len(self.processed_words),
                    'failed': len(self.words_for_review)
                },
                'timestamp': datetime.now().isoformat()
            }
            
            with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(checkpoint, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Checkpoint saved: {len(self.processed_words)} words processed")
        except Exception as e:
            logger.error(f"Error saving checkpoint: {e}")
    
    def extract_words_from_pdf(self, pdf_path: Path) -> List[Tuple[str, str]]:
        """Extract words from Scripps PDF with improved parsing"""
        words = []
        year_match = re.search(r'(\d{4})', pdf_path.name)
        year = year_match.group(1) if year_match else "Unknown"
        
        logger.info(f"Processing PDF: {pdf_path.name} (Year: {year})")
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        text = page.extract_text()
                        page_words = self.parse_spelling_bee_page(text, year)
                        words.extend(page_words)
                        
                        if (page_num + 1) % 5 == 0 or page_num == total_pages - 1:
                            logger.info(f"Processed {page_num + 1}/{total_pages} pages, found {len(words)} words so far")
                    
                    except Exception as e:
                        logger.warning(f"Error processing page {page_num + 1} of {pdf_path.name}: {e}")
                        continue
        
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {e}")
        
        logger.info(f"Extracted {len(words)} total words from {pdf_path.name}")
        return words
    
    def parse_spelling_bee_page(self, text: str, year: str) -> List[Tuple[str, str]]:
        """Parse a page of Scripps spelling bee text to extract words"""
        words = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for spelling bee word patterns
            # Scripps typically lists words in specific formats
            
            # Pattern 1: Words followed by pronunciation/definition
            word_matches = re.findall(r'\b([a-zA-Z]+)\b(?:\s+\[.*?\])?(?:\s+\(.*?\))?', line)
            
            for match in word_matches:
                word = match.lower().strip()
                if self.is_valid_spelling_word(word):
                    words.append((word, year))
        
        return words
    
    def is_valid_spelling_word(self, word: str) -> bool:
        """Enhanced validation for spelling bee words"""
        if not word or not word.isalpha():
            return False
        
        if len(word) < 3 or len(word) > 25:
            return False
        
        # Skip very common words that wouldn't be in spelling bees
        common_skip = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'got', 'has', 'him',
            'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way',
            'who', 'boy', 'did', 'she', 'too', 'use', 'said', 'each', 'which', 'do',
            'will', 'up', 'other', 'about', 'out', 'many', 'then', 'them', 'these',
            'so', 'some', 'her', 'would', 'make', 'like', 'into', 'him', 'time',
            'has', 'two', 'more', 'very', 'what', 'know', 'just', 'first', 'get',
            'over', 'think', 'also', 'your', 'work', 'life', 'only', 'can', 'still',
            'should', 'after', 'being', 'now', 'made', 'before', 'here', 'through',
            'when', 'where', 'much', 'take', 'than', 'only', 'little', 'state',
            'years', 'came', 'show', 'every', 'good', 'give', 'our', 'under', 'name'
        }
        
        if word in common_skip:
            return False
        
        # Skip obvious non-words (numbers, abbreviations, etc.)
        if re.search(r'\d', word) or len(word) < 4 and word.isupper():
            return False
        
        return True
    
    def clean_and_dedupe_words(self, words: List[Tuple[str, str]]) -> Dict[str, str]:
        """Clean and deduplicate words with enhanced logic"""
        cleaned = {}
        
        for word, year in words:
            word = word.lower().strip()
            
            # Skip if already processed or invalid
            if not word or word in cleaned:
                continue
            
            # Additional cleaning
            word = re.sub(r'[^a-z]', '', word)  # Remove any non-letters
            
            if self.is_valid_spelling_word(word):
                # Prefer more recent year if duplicate
                if word not in cleaned or year > cleaned[word]:
                    cleaned[word] = year
        
        logger.info(f"Cleaned to {len(cleaned)} unique valid words")
        return cleaned

    def fetch_dictionary_data(self, word: str) -> Optional[dict]:
        """Fetch definition and pronunciation from Free Dictionary API with retry logic"""
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        
        for attempt in range(self.max_retries):
            try:
                time.sleep(self.api_delay)
                response = requests.get(url, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    if data and isinstance(data, list) and len(data) > 0:
                        return data[0]  # Return first entry
                
                elif response.status_code == 429:  # Rate limited
                    wait_time = 5 * (attempt + 1)
                    logger.warning(f"Rate limited for '{word}', waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                
                elif response.status_code == 404:
                    logger.debug(f"No dictionary entry found for '{word}'")
                    return None
                
                else:
                    logger.warning(f"Dictionary API returned {response.status_code} for '{word}'")
                    return None
            
            except requests.exceptions.RequestException as e:
                logger.warning(f"Dictionary API request failed for '{word}' (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 * (attempt + 1))
            
            except Exception as e:
                logger.error(f"Unexpected error fetching dictionary data for '{word}': {e}")
                return None
        
        logger.warning(f"Failed to fetch dictionary data for '{word}' after {self.max_retries} attempts")
        return None
    
    def fetch_wiktionary_data(self, word: str) -> Optional[dict]:
        """Fetch etymology from Wiktionary API with enhanced parsing"""
        url = "https://en.wiktionary.org/w/api.php"
        params = {
            'action': 'parse',
            'page': word,
            'prop': 'wikitext',
            'format': 'json',
            'formatversion': '2'
        }
        
        for attempt in range(self.max_retries):
            try:
                time.sleep(self.api_delay)
                response = requests.get(url, params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'parse' in data and 'wikitext' in data['parse']:
                        return data['parse']
                
                elif response.status_code == 429:
                    wait_time = 3 * (attempt + 1)
                    logger.warning(f"Wiktionary rate limited for '{word}', waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                
                else:
                    logger.debug(f"Wiktionary returned {response.status_code} for '{word}'")
                    return None
            
            except requests.exceptions.RequestException as e:
                logger.warning(f"Wiktionary API request failed for '{word}' (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 * (attempt + 1))
            
            except Exception as e:
                logger.error(f"Unexpected error fetching Wiktionary data for '{word}': {e}")
                return None
        
        return None
    
    def extract_etymology_from_wikitext(self, wikitext: str) -> Tuple[str, str]:
        """Extract etymology and language origins from Wiktionary wikitext"""
        etymology = ""
        language_origins = ""
        
        try:
            # Look for Etymology sections
            etymology_patterns = [
                r'===Etymology===\s*\n(.*?)(?:\n===|\n\[\[|\Z)',
                r'==Etymology==\s*\n(.*?)(?:\n==|\n\[\[|\Z)',
                r'Etymology:\s*(.*?)(?:\n|$)'
            ]
            
            for pattern in etymology_patterns:
                match = re.search(pattern, wikitext, re.DOTALL | re.IGNORECASE)
                if match:
                    etymology_text = match.group(1).strip()
                    
                    # Clean up wiki formatting
                    etymology_text = re.sub(r'\[\[([^\]|]+)(\|[^\]]+)?\]\]', r'\1', etymology_text)
                    etymology_text = re.sub(r'\{\{[^}]+\}\}', '', etymology_text)
                    etymology_text = re.sub(r'<[^>]+>', '', etymology_text)
                    etymology_text = ' '.join(etymology_text.split())  # Normalize whitespace
                    
                    if len(etymology_text) > 10:  # Only use if substantial
                        etymology = etymology_text[:500]  # Limit length
                        break
            
            # Extract language origins
            if etymology:
                origin_patterns = [
                    r'From\s+(\w+(?:\s+\w+)?)',
                    r'Borrowed from\s+(\w+(?:\s+\w+)?)',
                    r'(\w+(?:\s+\w+)?)\s+origin',
                    r'ultimately from\s+(\w+(?:\s+\w+)?)',
                    r'derives? from\s+(\w+(?:\s+\w+)?)'
                ]
                
                for pattern in origin_patterns:
                    match = re.search(pattern, etymology, re.IGNORECASE)
                    if match:
                        language_origins = match.group(1).strip().title()
                        break
        
        except Exception as e:
            logger.warning(f"Error parsing etymology: {e}")
        
        return etymology, language_origins
    
    def generate_quality_example_sentence(self, word: str, definition: str, etymology: str = "") -> str:
        """Generate contextual example sentences with word blanked out"""
        if not definition:
            return f"The ___ was discussed in class."
        
        # Analyze definition to determine word type and context
        definition_lower = definition.lower()
        
        # Try to create contextual sentences based on definition content
        if 'verb' in definition_lower or 'to ' in definition_lower[:30]:
            contexts = [
                f"She decided to ___ before making the final decision.",
                f"The team will ___ their strategy for the upcoming project.",
                f"It's important to ___ carefully in this situation."
            ]
        elif 'noun' in definition_lower or 'a ' in definition_lower[:10]:
            if 'person' in definition_lower or 'people' in definition_lower:
                contexts = [
                    f"The experienced ___ guided them through the process.",
                    f"Every ___ in the community contributed to the effort.",
                    f"She became a respected ___ in her field."
                ]
            elif 'place' in definition_lower or 'location' in definition_lower:
                contexts = [
                    f"The ancient ___ attracted visitors from around the world.",
                    f"They discovered the hidden ___ after hours of searching.",
                    f"The ___ served as a meeting point for travelers."
                ]
            elif 'thing' in definition_lower or 'object' in definition_lower:
                contexts = [
                    f"The mysterious ___ puzzled the researchers.",
                    f"She carefully examined the intricate ___.",
                    f"The ___ played a crucial role in the ceremony."
                ]
            else:
                contexts = [
                    f"The ___ was clearly visible from the observation deck.",
                    f"Understanding the ___ required careful study.",
                    f"The ___ impressed everyone who saw it."
                ]
        elif 'adjective' in definition_lower or 'adj.' in definition_lower:
            contexts = [
                f"The weather remained ___ throughout the entire week.",
                f"His ___ approach to the problem impressed his colleagues.",
                f"The ___ design won the architectural competition."
            ]
        elif 'adverb' in definition_lower:
            contexts = [
                f"She spoke ___ during the important presentation.",
                f"The team worked ___ to meet the challenging deadline.",
                f"He ___ completed the complex assignment."
            ]
        else:
            # Create context based on definition content
            if any(term in definition_lower for term in ['medical', 'disease', 'condition', 'symptom']):
                contexts = [
                    f"The doctor diagnosed the patient with ___.",
                    f"The ___ required immediate medical attention.",
                    f"Researchers are studying the causes of ___."
                ]
            elif any(term in definition_lower for term in ['art', 'music', 'literature', 'creative']):
                contexts = [
                    f"The artist's use of ___ transformed the entire piece.",
                    f"Students learned about ___ in their humanities class.",
                    f"The ___ influenced generations of creators."
                ]
            elif any(term in definition_lower for term in ['science', 'scientific', 'research', 'study']):
                contexts = [
                    f"The scientists discovered a new type of ___.",
                    f"The ___ played a key role in the experiment.",
                    f"Understanding ___ is essential for this field of study."
                ]
            elif any(term in definition_lower for term in ['food', 'cooking', 'cuisine', 'dish']):
                contexts = [
                    f"The chef prepared a delicious ___.",
                    f"The traditional ___ has been enjoyed for centuries.",
                    f"She learned to make ___ from her grandmother."
                ]
            else:
                contexts = [
                    f"The concept of ___ is fundamental to understanding this topic.",
                    f"Everyone was fascinated by the remarkable ___.",
                    f"The ___ demonstrates the complexity of the subject."
                ]
        
        # Select a context that fits well
        import random
        selected_context = random.choice(contexts)
        
        # Ensure the sentence makes sense (basic validation)
        if len(selected_context.split()) < 5:
            return f"The ___ is an important concept to understand."
        
        return selected_context
    
    def process_single_word(self, word: str, year: str) -> Optional[SpellingWord]:
        """Process a single word through all enrichment steps"""
        logger.debug(f"Processing word: {word}")
        
        # Initialize spelling word with known data
        # Map year to Scripps difficulty levels
        year_to_difficulty = {
            "2020": "One Bee",
            "2021": "One Bee", 
            "2022": "Two Bee",
            "2023": "Two Bee",
            "2024": "Three Bee",
            "2025": "Three Bee"
        }
        
        spelling_word = SpellingWord(
            word=word,
            source=f"Scripps National Spelling Bee {year}",
            source_url="https://spellingbee.com/",
            source_difficulty=year_to_difficulty.get(year, "Two Bee")
        )
        
        # Fetch dictionary data
        dict_data = self.fetch_dictionary_data(word)
        if dict_data:
            # Extract definition
            if 'meanings' in dict_data and dict_data['meanings']:
                meanings = dict_data['meanings']
                if meanings and 'definitions' in meanings[0] and meanings[0]['definitions']:
                    definition = meanings[0]['definitions'][0].get('definition', '')
                    if definition:
                        spelling_word.definition = definition[:500]  # Limit length
                        spelling_word.definition_source = "Dictionary API"
            
            # Extract pronunciation
            if 'phonetics' in dict_data and dict_data['phonetics']:
                for phonetic in dict_data['phonetics']:
                    if 'text' in phonetic and phonetic['text']:
                        spelling_word.pronunciation = phonetic['text']
                        spelling_word.pronunciation_source = "Dictionary API"
                        break
        
        # If no definition found, add to review list
        if not spelling_word.definition:
            self.words_for_review.append((word, "No definition found in Dictionary API"))
            logger.warning(f"No definition found for '{word}', adding to review list")
            return None
        
        # Fetch Wiktionary data for etymology
        wiki_data = self.fetch_wiktionary_data(word)
        if wiki_data and 'wikitext' in wiki_data:
            etymology, language_origins = self.extract_etymology_from_wikitext(wiki_data['wikitext'])
            if etymology:
                spelling_word.etymology = etymology
                spelling_word.language_origins = language_origins
                spelling_word.etymology_source = "Wiktionary"
        
        # Generate etymology if not found
        if not spelling_word.etymology:
            spelling_word.etymology = self.generate_etymology_from_patterns(word)
            spelling_word.etymology_source = "Claude"
        
        # Generate example sentence
        if spelling_word.definition:
            spelling_word.example_sentence = self.generate_quality_example_sentence(
                word, spelling_word.definition, spelling_word.etymology or ""
            )
        
        # Calculate difficulty using sophisticated algorithm
        difficulty_level, difficulty_name = self.difficulty_calc.calculate_difficulty(
            word=word,
            source_difficulty=spelling_word.source_difficulty or "Two Bee",
            pronunciation_ipa=spelling_word.pronunciation or "",
            definition=spelling_word.definition or "",
            etymology=spelling_word.etymology or "",
            language_origins=spelling_word.language_origins or ""
        )
        
        spelling_word.difficulty = difficulty_name
        
        logger.info(f"Successfully processed: {word} (Level: {difficulty_name})")
        return spelling_word
    
    def generate_etymology_from_patterns(self, word: str) -> str:
        """Generate etymology based on linguistic patterns when API data unavailable"""
        # Common etymological patterns
        patterns = {
            'tion': "From Latin suffix '-tion', meaning 'the act or process of'",
            'sion': "From Latin suffix '-sion', meaning 'state or quality of'", 
            'ment': "From Latin suffix '-ment', meaning 'result or means of'",
            'able': "From Latin suffix '-able', meaning 'capable of being'",
            'ible': "From Latin suffix '-ible', meaning 'capable of being'",
            'ology': "From Greek '-ology', meaning 'the study of'",
            'graph': "Contains Greek root 'graph', meaning 'to write'",
            'phon': "Contains Greek root 'phon', meaning 'sound'",
            'bio': "Contains Greek root 'bio', meaning 'life'",
            'geo': "Contains Greek root 'geo', meaning 'earth'",
            'chron': "Contains Greek root 'chron', meaning 'time'",
            'phil': "Contains Greek root 'phil', meaning 'love'",
            'phob': "Contains Greek root 'phob', meaning 'fear'",
            'micro': "From Greek prefix 'micro-', meaning 'small'",
            'macro': "From Greek prefix 'macro-', meaning 'large'",
            'tele': "From Greek prefix 'tele-', meaning 'distant'",
            'auto': "From Greek prefix 'auto-', meaning 'self'"
        }
        
        # Check for patterns
        for pattern, etymology in patterns.items():
            if pattern in word:
                return etymology
        
        # Check for common prefixes
        if word.startswith('un'):
            return "Old English prefix 'un-', meaning 'not' or 'reverse of'"
        elif word.startswith('re'):
            return "Latin prefix 're-', meaning 'again' or 'back'"
        elif word.startswith('pre'):
            return "Latin prefix 'pre-', meaning 'before'"
        elif word.startswith('dis'):
            return "Latin prefix 'dis-', meaning 'apart' or 'not'"
        elif word.startswith('mis'):
            return "Old English prefix 'mis-', meaning 'badly' or 'wrongly'"
        elif word.startswith('over'):
            return "Old English prefix 'over-', meaning 'above' or 'excessive'"
        elif word.startswith('under'):
            return "Old English prefix 'under-', meaning 'below' or 'insufficient'"
        
        # Default
        return "Etymology uncertain; may derive from multiple linguistic sources"
    
    def process_test_batch(self, max_words: int = 50) -> bool:
        """Process a small test batch to validate the approach"""
        logger.info(f"Starting test batch processing (max {max_words} words)")
        
        # Get all PDFs and extract words
        pdf_files = list(self.pdf_folder.glob("*.pdf"))
        all_words = {}
        
        for pdf_file in pdf_files[:2]:  # Test with first 2 PDFs only
            logger.info(f"Extracting words from {pdf_file.name}")
            extracted = self.extract_words_from_pdf(pdf_file)
            cleaned = self.clean_and_dedupe_words(extracted)
            all_words.update(cleaned)
            
            if len(all_words) >= max_words:
                break
        
        # Take only the first max_words for testing
        test_words = dict(list(all_words.items())[:max_words])
        logger.info(f"Testing with {len(test_words)} words")
        
        # Process each word
        successful = 0
        for word, year in test_words.items():
            try:
                result = self.process_single_word(word, year)
                if result:
                    self.processed_words[word] = result
                    successful += 1
                
                # Save checkpoint every 10 words
                if len(self.processed_words) % 10 == 0:
                    self.save_checkpoint()
                    
            except Exception as e:
                logger.error(f"Error processing '{word}': {e}")
                self.words_for_review.append((word, f"Processing error: {str(e)[:100]}"))
        
        logger.info(f"Test batch complete: {successful}/{len(test_words)} successful")
        self.save_checkpoint()
        return successful > 0
    
    def write_final_csv_files(self):
        """Write final CSV files matching database schema exactly"""
        # Database schema field names (from setupSpellingBeeTables.ts)
        fieldnames = [
            'word', 'definition', 'pronunciation', 'etymology', 'language_origins',
            'example_sentence', 'difficulty', 'source_difficulty', 'source',
            'source_url', 'definition_source', 'pronunciation_source', 'etymology_source'
        ]
        
        # Write main words file
        logger.info(f"Writing {len(self.processed_words)} words to {self.words_file}")
        with open(self.words_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            
            for word in sorted(self.processed_words.keys()):
                word_data = self.processed_words[word]
                row = asdict(word_data)
                
                # Ensure all fields are present and properly formatted
                for field in fieldnames:
                    if field not in row or row[field] is None:
                        row[field] = ""
                
                writer.writerow({field: row[field] for field in fieldnames})
        
        # Write review file
        logger.info(f"Writing {len(self.words_for_review)} review words to {self.review_file}")
        with open(self.review_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(['word', 'reason'])
            for word, reason in sorted(set(self.words_for_review)):
                writer.writerow([word, reason])
        
        logger.info("CSV files written successfully")
    
    def run_test(self):
        """Run a small test to validate the approach"""
        logger.info("=== STARTING TEST RUN ===")
        logger.info(f"PDF folder: {self.pdf_folder}")
        logger.info(f"Output folder: {self.output_folder}")
        
        try:
            success = self.process_test_batch(50)  # Test with 50 words
            if success:
                self.write_final_csv_files()
                logger.info("=== TEST RUN COMPLETED SUCCESSFULLY ===")
                logger.info(f"Processed: {len(self.processed_words)} words")
                logger.info(f"For review: {len(self.words_for_review)} words")
                return True
            else:
                logger.error("=== TEST RUN FAILED ===")
                return False
                
        except KeyboardInterrupt:
            logger.info("Test interrupted by user. Progress saved.")
            self.save_checkpoint()
            return False
        except Exception as e:
            logger.error(f"Fatal error during test: {e}")
            self.save_checkpoint()
            raise

def main():
    """Main entry point for testing"""
    # Use the data folder structure
    pdf_folder = r"C:\Users\jessi\Projects\skilltree2\src\data\spelling_bee\input"
    output_folder = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output"
    
    processor = ImprovedSpellingProcessor(pdf_folder, output_folder)
    success = processor.run_test()
    
    if success:
        print(f"\n✅ Test completed successfully!")
        print(f"📄 Results saved to: {processor.words_file}")
        print(f"🔍 Review file: {processor.review_file}")
        print(f"💾 Checkpoint: {processor.checkpoint_file}")
    else:
        print(f"\n❌ Test failed. Check logs for details.")

if __name__ == "__main__":
    main()