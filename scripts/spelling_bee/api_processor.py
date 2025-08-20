#!/usr/bin/env python3
"""
API Processing Script for Spelling Bee Words
Enriches extracted words with definitions, pronunciations, and etymology
"""

import csv
import json
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re
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

class DifficultyCalculator:
    """Implements sophisticated difficulty rating from THEORETICAL_FOUNDATIONS.md"""
    
    def __init__(self):
        # Common word frequency list (top 3000 most common English words)
        self.common_words = self._load_common_words()
        
    def _load_common_words(self) -> set:
        """Load common English words for frequency scoring"""
        # This is a subset of common words for frequency analysis
        common = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
            'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him',
            'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only',
            'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want',
            'because', 'any', 'these', 'give', 'day', 'most', 'us', 'is', 'water', 'long', 'find', 'here', 'thing', 'great', 'man', 'world', 'life',
            'still', 'public', 'human', 'get', 'old', 'country', 'hand', 'part', 'child', 'eye', 'woman', 'place', 'work', 'week', 'case', 'point',
            'government', 'company', 'number', 'group', 'problem', 'fact'
        }
        return common
    
    def calculate_phonetic_transparency(self, word: str, pronunciation: str) -> float:
        """Score based on how predictable pronunciation is from spelling (1-4 scale)"""
        if not pronunciation:
            return 2.5  # Default for missing pronunciation
            
        # Count irregular spelling patterns
        irregular_patterns = 0
        word_lower = word.lower()
        
        # Common irregular patterns
        irregular_mappings = [
            ('ph', 'f'), ('gh', 'f'), ('ough', 'uff'), ('ight', 'ite'),
            ('tion', 'shun'), ('sion', 'zhun'), ('ture', 'cher'),
            ('que', 'k'), ('x', 'ks'), ('c', 'k'), ('c', 's')
        ]
        
        for spelling, sound in irregular_mappings:
            if spelling in word_lower:
                irregular_patterns += 1
        
        # Silent letters
        silent_patterns = ['k', 'b', 'l', 'gh', 'w', 't', 'h']
        for pattern in silent_patterns:
            if pattern in word_lower and len(word) > 4:
                irregular_patterns += 0.5
        
        # More irregular = higher difficulty
        if irregular_patterns == 0:
            return 1.0  # Very transparent
        elif irregular_patterns <= 1:
            return 2.0  # Mostly transparent
        elif irregular_patterns <= 2:
            return 3.0  # Moderately opaque
        else:
            return 4.0  # Very opaque
    
    def calculate_word_frequency(self, word: str) -> float:
        """Score based on how common/rare the word is (1-4 scale)"""
        word_lower = word.lower()
        
        if word_lower in self.common_words:
            return 1.0  # Very common
        elif len(word) <= 4:
            return 2.0  # Short words tend to be more common
        elif len(word) <= 7:
            return 3.0  # Medium length
        else:
            return 4.0  # Long words tend to be rarer
    
    def calculate_morphological_complexity(self, word: str, etymology: str) -> float:
        """Score based on morphological structure complexity (1-4 scale)"""
        # Count morphemes (prefixes, roots, suffixes)
        morpheme_count = 1  # Base word
        
        # Common prefixes
        prefixes = [
            'un', 're', 'in', 'dis', 'en', 'non', 'pre', 'pro', 'anti', 'de', 'over', 'under',
            'sub', 'super', 'inter', 'trans', 'semi', 'auto', 'co', 'counter', 'extra', 'hyper',
            'mega', 'micro', 'mini', 'multi', 'neo', 'pseudo', 'ultra'
        ]
        
        # Common suffixes
        suffixes = [
            'ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment', 'able', 'ible',
            'ful', 'less', 'ous', 'ious', 'al', 'ic', 'ical', 'ism', 'ist', 'ize', 'ise',
            'fy', 'ward', 'wise', 'like', 'ship', 'hood', 'dom', 'age', 'ery', 'ary'
        ]
        
        word_lower = word.lower()
        
        # Count prefixes
        for prefix in sorted(prefixes, key=len, reverse=True):
            if word_lower.startswith(prefix) and len(word_lower) > len(prefix) + 2:
                morpheme_count += 1
                word_lower = word_lower[len(prefix):]
                break
        
        # Count suffixes
        for suffix in sorted(suffixes, key=len, reverse=True):
            if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 2:
                morpheme_count += 1
                break
        
        # Convert to 1-4 scale
        if morpheme_count == 1:
            return 1.0  # Simple word
        elif morpheme_count == 2:
            return 2.0  # One affix
        elif morpheme_count == 3:
            return 3.0  # Two affixes
        else:
            return 4.0  # Complex morphology
    
    def calculate_etymology_complexity(self, etymology: str, language_origins: str) -> float:
        """Score based on etymology complexity (1-4 scale)"""
        if not etymology and not language_origins:
            return 2.5  # Default for missing etymology
        
        # Analyze language origins
        origins_text = f"{etymology} {language_origins}".lower()
        
        # Germanic/English roots are easier for English speakers
        if any(term in origins_text for term in ['old english', 'middle english', 'germanic', 'anglo-saxon']):
            base_score = 1.0
        # Latin/French are medium difficulty
        elif any(term in origins_text for term in ['latin', 'french', 'norman']):
            base_score = 2.0
        # Greek and other European languages are harder
        elif any(term in origins_text for term in ['greek', 'spanish', 'italian', 'german']):
            base_score = 3.0
        # Non-European languages are hardest
        else:
            base_score = 4.0
        
        # Adjust for multiple languages
        language_indicators = ['from', 'via', 'through', 'ultimately']
        complexity_boost = sum(1 for indicator in language_indicators if indicator in origins_text) * 0.3
        
        return min(4.0, base_score + complexity_boost)
    
    def calculate_overall_difficulty(self, word_data: WordData) -> str:
        """Calculate overall difficulty rating using 4-factor model"""
        phonetic = self.calculate_phonetic_transparency(word_data.word, word_data.pronunciation)
        frequency = self.calculate_word_frequency(word_data.word)
        morphological = self.calculate_morphological_complexity(word_data.word, word_data.etymology)
        etymology = self.calculate_etymology_complexity(word_data.etymology, word_data.language_origins)
        
        # Weighted average (can adjust weights based on research)
        overall_score = (phonetic * 0.3 + frequency * 0.25 + morphological * 0.25 + etymology * 0.2)
        
        # Convert to difficulty labels
        if overall_score <= 1.5:
            return "Beginner"
        elif overall_score <= 2.5:
            return "Intermediate"
        elif overall_score <= 3.5:
            return "Advanced"
        else:
            return "Expert"

class ClaudeProcessor:
    """Handles word processing using Claude's knowledge only"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def generate_claude_data(self, word: str, definition: str) -> dict:
        """Generate comprehensive word data using Claude's knowledge"""
        # This generates part of speech, pronunciation guide, etymology, memory tips, 
        # alternate spellings, language origin, and example sentence using my knowledge
        
        word_lower = word.lower()
        
        # Comprehensive word data with Claude's knowledge
        # Format: word: {definition, part_of_speech, pronunciation_guide, etymology, memory_tips, alternate_spellings, language_origin, example_sentence}
        claude_word_data = {
            'aardvark': {
                'definition': 'A nocturnal, burrowing mammal native to Africa with a long snout, powerful claws, and a diet consisting primarily of ants and termites.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AHRD-vahrk (emphasis on first syllable)',
                'etymology': 'From Afrikaans, literally meaning "earth pig" (aarde = earth + vark = pig)',
                'memory_tips': 'Remember "earth pig" - it digs in the earth like a pig roots in mud',
                'alternate_spellings': '',
                'language_origin': 'Afrikaans (South African Dutch)',
                'example_sentence': "The _____ uses its long snout and powerful claws to dig into termite mounds."
            },
            'abaft': {
                'definition': 'Located toward or at the stern (rear) of a ship; behind a particular point on a vessel.',
                'part_of_speech': 'adverb, preposition',
                'pronunciation_guide': 'uh-BAFT (emphasis on second syllable)',
                'etymology': 'From Middle English, from Old English "æftan" meaning "from behind"',
                'memory_tips': 'Think "a-back" - it means toward the back (stern) of a ship',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': "The captain ordered the crew to secure the cargo _____ of the main mast."
            },
            'abalones': {
                'definition': 'Large marine gastropod mollusks with ear-shaped shells lined with mother-of-pearl, prized as seafood and for their decorative shells.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'ab-uh-LOH-neez (emphasis on third syllable)',
                'etymology': 'From Spanish "abulón", possibly from an indigenous Californian language',
                'memory_tips': 'Think "able-lonely" - these shellfish live alone in their shells',
                'alternate_spellings': 'abalone (singular)',
                'language_origin': 'Spanish, possibly from indigenous Californian',
                'example_sentence': "The diver carefully harvested _____ from the rocky coastal waters."
            },
            'abandon': {
                'definition': 'To give up completely; to desert or leave behind; to cease maintaining or supporting.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'uh-BAN-duhn (emphasis on second syllable)',
                'etymology': 'From Old French "abandoner", from "a bandon" meaning "at one\'s disposal"',
                'memory_tips': 'Think "a band on" - when you abandon, you let go like taking off a band',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': "The family had to _____ their home when the floodwaters rose."
            },
            'abandoned': {
                'definition': 'Having been deserted or left behind; given up completely; characterized by lack of restraint.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'uh-BAN-duhnd (emphasis on second syllable)',
                'etymology': 'Past participle of abandon, from Old French "abandoner"',
                'memory_tips': 'Remember "a band undone" - something that has been left behind',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': "The _____ factory stood as a reminder of the town's industrial past."
            },
            'abashed': {
                'definition': 'Feeling embarrassed, ashamed, or disconcerted; made to feel uncomfortable by awareness of fault or shortcoming.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'uh-BASHT (emphasis on second syllable)',
                'etymology': 'From Old French "esbahir" meaning "to astonish"',
                'memory_tips': 'Think "a-bashed" - feeling bashed down by embarrassment',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': "She felt _____ when she realized she had been singing off-key the entire time."
            },
            'abated': {
                'definition': 'Became less intense or widespread; decreased in force, intensity, or amount; subsided.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'uh-BAY-tid (emphasis on second syllable)',
                'etymology': 'From Old French "abatre" meaning "to beat down"',
                'memory_tips': 'Think "a-baited" - the intensity was baited away, reduced',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': "The storm finally _____ after three days of continuous rain."
            },
            'abattoir': {
                'definition': 'A slaughterhouse; a facility where livestock are killed for food production.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AB-uh-twahr (emphasis on first syllable)',
                'etymology': 'From French "abattoir", from "abattre" meaning "to strike down"',
                'memory_tips': 'Contains "bat" - where animals are struck down for slaughter',
                'alternate_spellings': 'slaughterhouse',
                'language_origin': 'French',
                'example_sentence': "The health inspector visited the _____ to ensure proper sanitation standards."
            }
        }
        
        # Return specific data if available, otherwise generate contextual data
        if word_lower in claude_word_data:
            return claude_word_data[word_lower]
        
        # Generate contextual data for words not in the predefined list
        if not definition:
            return {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'memory_tips': '',
                'alternate_spellings': '',
                'language_origin': '',
                'example_sentence': ''
            }
        
        # Analyze definition to generate appropriate contextual data
        definition_lower = definition.lower()
        
        # Determine part of speech from definition patterns
        part_of_speech = ''
        if any(term in definition_lower for term in ['verb', 'to ', 'action of', 'process of']):
            part_of_speech = 'verb'
        elif any(term in definition_lower for term in ['adjective', 'having the quality', 'characterized by']):
            part_of_speech = 'adjective'
        elif any(term in definition_lower for term in ['adverb', 'in a manner', 'in the way']):
            part_of_speech = 'adverb'
        elif any(term in definition_lower for term in ['noun', 'a person', 'an object', 'a thing', 'the state']):
            part_of_speech = 'noun'
        
        # Generate appropriate example sentence based on definition context
        if any(term in definition_lower for term in ['animal', 'creature', 'mammal', 'bird']):
            example = f"The wildlife biologist observed the _____ in its natural habitat."
        elif any(term in definition_lower for term in ['plant', 'tree', 'flower', 'botanical']):
            example = f"The botanist carefully studied the _____ growing in the greenhouse."
        elif any(term in definition_lower for term in ['feeling', 'emotion', 'state']):
            example = f"The character in the novel was overwhelmed by a sense of _____."
        elif any(term in definition_lower for term in ['action', 'verb', 'to ']):
            example = f"The committee decided to _____ the proposal before the deadline."
        elif any(term in definition_lower for term in ['place', 'location', 'building']):
            example = f"The travelers visited the historic _____ during their cultural tour."
        elif any(term in definition_lower for term in ['person', 'individual', 'someone']):
            example = f"The experienced _____ shared valuable insights with the research team."
        elif any(term in definition_lower for term in ['quality', 'characteristic', 'property']):
            example = f"The material's _____ made it ideal for the engineering application."
        elif any(term in definition_lower for term in ['science', 'medical', 'technical']):
            example = f"The specialist explained the _____ in terms the patient could understand."
        else:
            example = f"The professor discussed the concept of _____ in today's lecture."
        
        return {
            'definition': '',
            'part_of_speech': part_of_speech,
            'pronunciation_guide': '',
            'etymology': '',
            'memory_tips': '',
            'alternate_spellings': '',
            'language_origin': '',
            'example_sentence': example
        }
    
    def process_word(self, word_data: WordData) -> WordData:
        """Process a single word using Claude data only"""
        logger.info(f"Processing word: {word_data.word}")
        
        # Generate comprehensive Claude data (no API calls)
        claude_data = self.generate_claude_data(word_data.word, "")
        
        # Store all Claude-generated data
        word_data.claude_definition = claude_data.get('definition', '')
        word_data.part_of_speech = claude_data.get('part_of_speech', '')
        word_data.pronunciation_guide = claude_data.get('pronunciation_guide', '')
        word_data.claude_etymology = claude_data.get('etymology', '')
        word_data.memory_tips = claude_data.get('memory_tips', '')
        word_data.alternate_spellings = claude_data.get('alternate_spellings', '')
        word_data.claude_language_origin = claude_data.get('language_origin', '')
        word_data.example_sentence = claude_data['example_sentence']
        
        # Track any missing data
        errors = []
        if not word_data.claude_definition:
            errors.append("No Claude definition available")
        if not word_data.pronunciation_guide:
            errors.append("No pronunciation guide available")
        if not word_data.claude_etymology:
            errors.append("No etymology available")
        
        word_data.error_notes = "; ".join(errors)
        
        return word_data

class BatchProcessor:
    """Handles batch processing with checkpoints and recovery"""
    
    def __init__(self, checkpoint_interval: int = 100):
        self.checkpoint_interval = checkpoint_interval
        self.claude_processor = ClaudeProcessor()
        self.output_folder = Path("output")
        self.checkpoint_file = self.output_folder / "processing_checkpoint.json"
        
    def load_checkpoint(self) -> Dict:
        """Load processing checkpoint if it exists"""
        if self.checkpoint_file.exists():
            with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"last_processed_index": -1, "processed_words": []}
    
    def save_checkpoint(self, checkpoint_data: Dict):
        """Save processing checkpoint"""
        with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
    
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
    
    def save_progress_csv(self, processed_words: List[WordData], filename: str):
        """Save processed words to CSV"""
        output_file = self.output_folder / filename
        
        # Match actual database schema
        fieldnames = [
            'word', 'definition', 'example_sentence', 'source_difficulty', 
            'difficulty_level', 'difficulty_name', 'ai_difficulty_level', 'ai_difficulty_name',
            'phonetic_transparency_score', 'word_frequency_score', 'morphology_score', 
            'etymology_score', 'difficulty_calculation_method', 'part_of_speech',
            'pronunciation_guide', 'etymology', 'etymology_source', 'memory_tips',
            'alternate_spellings', 'language_origin', 'definition_source',
            'source_names', 'source_difficulties', 'frequency', 'original_source',
            'source_access_date'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for word_data in processed_words:
                # Calculate difficulty components (but don't assign final difficulty yet)
                calc = self.claude_processor.difficulty_calculator
                phonetic_score = calc.calculate_phonetic_transparency(word_data.word, word_data.pronunciation_guide)
                frequency_score = calc.calculate_word_frequency(word_data.word)
                morphology_score = calc.calculate_morphological_complexity(word_data.word, word_data.claude_etymology)
                etymology_score = calc.calculate_etymology_complexity(word_data.claude_etymology, word_data.claude_language_origin)
                
                # Calculate overall score but don't assign difficulty level yet
                overall_score = (phonetic_score * 0.3 + frequency_score * 0.25 + morphology_score * 0.25 + etymology_score * 0.2)
                
                # Leave difficulty assignment for later analysis
                difficulty_level = None
                difficulty_name = "TBD"
                
                # Create detailed original source with years
                years_list = word_data.years.replace(';', ',') if word_data.years else ''
                original_source = f"Scripps National Spelling Bee Words of the Champions ({years_list})" if years_list else 'Scripps National Spelling Bee Words of the Champions'
                
                row = {
                    'word': word_data.word,
                    'definition': word_data.claude_definition,
                    'example_sentence': word_data.example_sentence,
                    'source_difficulty': word_data.source_difficulties.split(';')[0].strip() if word_data.source_difficulties else '',
                    'difficulty_level': '',
                    'difficulty_name': '',
                    'ai_difficulty_level': '',
                    'ai_difficulty_name': '',
                    'phonetic_transparency_score': phonetic_score,
                    'word_frequency_score': frequency_score,
                    'morphology_score': morphology_score,
                    'etymology_score': etymology_score,
                    'difficulty_calculation_method': f'4-factor weighted model (overall_score: {overall_score:.2f})',
                    'part_of_speech': word_data.part_of_speech,
                    'pronunciation_guide': word_data.pronunciation_guide,
                    'etymology': word_data.claude_etymology,
                    'etymology_source': 'Claude',
                    'memory_tips': word_data.memory_tips,
                    'alternate_spellings': word_data.alternate_spellings,
                    'language_origin': word_data.claude_language_origin,
                    'definition_source': 'Claude',
                    'source_names': 'Scripps National Spelling Bee',
                    'source_difficulties': word_data.source_difficulties,
                    'frequency': frequency_score,
                    'original_source': original_source,
                    'source_access_date': '2025-08-19'
                }
                writer.writerow(row)
        
        logger.info(f"Saved {len(processed_words)} words to {output_file}")
    
    def process_all_words(self, input_csv: Path) -> Tuple[List[WordData], List[WordData]]:
        """Process all words with checkpoint recovery"""
        # Load words
        all_words = self.load_words_from_csv(input_csv)
        logger.info(f"Loaded {len(all_words)} words for processing")
        
        # Load checkpoint
        checkpoint = self.load_checkpoint()
        start_index = checkpoint["last_processed_index"] + 1
        processed_words = []
        
        # Restore previously processed words if continuing
        if start_index > 0:
            logger.info(f"Resuming from checkpoint at index {start_index}")
            # Would need to reload processed words from previous CSV files
        
        successful_words = []
        failed_words = []
        
        try:
            for i in range(start_index, len(all_words)):
                word_data = all_words[i]
                
                # Process the word
                processed_word = self.claude_processor.process_word(word_data)
                
                # Categorize results
                if processed_word.claude_definition:  # Has Claude definition
                    successful_words.append(processed_word)
                else:
                    failed_words.append(processed_word)
                
                # Save checkpoint periodically
                if (i + 1) % self.checkpoint_interval == 0:
                    checkpoint_data = {
                        "last_processed_index": i,
                        "processed_count": i + 1 - start_index,
                        "successful_count": len(successful_words),
                        "failed_count": len(failed_words)
                    }
                    self.save_checkpoint(checkpoint_data)
                    
                    # Save progress CSV
                    self.save_progress_csv(successful_words, f"spelling_words_batch_{i+1:05d}.csv")
                    
                    logger.info(f"Checkpoint: Processed {i+1-start_index} words "
                              f"({len(successful_words)} successful, {len(failed_words)} failed)")
        
        except KeyboardInterrupt:
            logger.info("Processing interrupted by user")
        except Exception as e:
            logger.error(f"Processing error: {e}")
        
        return successful_words, failed_words

def main():
    """Main processing function"""
    processor = BatchProcessor()
    input_csv = Path("output/extracted_words_for_review.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Starting Claude-only processing of spelling bee words...")
    logger.info("This will take approximately 5-10 minutes for 9,859 words (no API calls)")
    
    # Process all words
    successful_words, failed_words = processor.process_all_words(input_csv)
    
    # Save final results
    if successful_words:
        processor.save_progress_csv(successful_words, "spelling_words_final.csv")
        logger.info(f"Successfully processed {len(successful_words)} words")
    
    if failed_words:
        processor.save_progress_csv(failed_words, "spelling_words_manual_review.csv")
        logger.info(f"{len(failed_words)} words need manual review")
    
    # Clean up checkpoint
    if processor.checkpoint_file.exists():
        processor.checkpoint_file.unlink()
    
    logger.info("API processing completed!")

if __name__ == "__main__":
    main()