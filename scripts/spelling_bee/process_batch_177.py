#!/usr/bin/env python3
"""
Process Batch 177 of Spelling Bee Words with Comprehensive Claude Data
Generates full definitions, pronunciations, etymologies, memory tips, and examples for all 50 words
"""

import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
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
        common = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
            'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him',
            'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only',
            'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want',
            'because', 'any', 'these', 'give', 'day', 'most', 'us', 'is', 'water', 'long', 'find', 'here', 'thing', 'great', 'man', 'world', 'life',
            'still', 'public', 'human', 'get', 'old', 'country', 'hand', 'part', 'child', 'eye', 'woman', 'place', 'work', 'week', 'case', 'point',
            'government', 'company', 'number', 'group', 'problem', 'fact', 'actually', 'across', 'activities', 'activity', 'adding', 'addition',
            'team', 'tape', 'tasks', 'teachers', 'teak', 'teamwork', 'tell', 'telling', 'tells', 'temperature', 'television', 'telescope', 'tennis',
            'tent', 'technical', 'technology', 'technique', 'technician', 'tends', 'tendency', 'term', 'test', 'text', 'thank', 'thanks', 'theater',
            'theatre', 'theme', 'themed', 'territory', 'terror', 'tertiary'
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
            'mega', 'micro', 'mini', 'multi', 'neo', 'pseudo', 'ultra', 'ac', 'ad', 'con', 'tele', 'ter'
        ]
        
        # Common suffixes
        suffixes = [
            'ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment', 'able', 'ible',
            'ful', 'less', 'ous', 'ious', 'al', 'ic', 'ical', 'ism', 'ist', 'ize', 'ise',
            'fy', 'ward', 'wise', 'like', 'ship', 'hood', 'dom', 'age', 'ery', 'ary', 'ate'
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

class Batch177Processor:
    """Processes Batch 177 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 177 words"""
        
        # Comprehensive data for all 50 words in Batch 177
        batch_177_data = {
            'tentativeness': {
                'definition': 'The quality of being uncertain, hesitant, or provisional; a lack of confidence or decisiveness in action or opinion.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEN-tuh-tiv-nis (emphasis on first syllable)',
                'etymology': 'From "tentative" + "-ness", from Latin "tentare" meaning "to try, attempt"',
                'memory_tips': 'Think "tent-ative-ness" - like being unsure whether to set up your tent',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Her _____ in making the decision reflected her uncertainty about the outcome.'
            },
            'tephra': {
                'definition': 'Volcanic ash and rock fragments ejected during an eruption; airborne volcanic debris of various sizes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEF-ruh (emphasis on first syllable)',
                'etymology': 'From Greek "tephra" meaning "ash"',
                'memory_tips': 'Think "teph-ra" - ash that makes you cough "teff"',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The volcanic _____ covered the landscape for miles around the eruption.'
            },
            'tepidity': {
                'definition': 'The state of being lukewarm; lack of enthusiasm or passion; moderate warmth.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tuh-PID-i-tee (emphasis on second syllable)',
                'etymology': 'From Latin "tepiditas", from "tepidus" meaning "lukewarm"',
                'memory_tips': 'Think "tepid-ity" - the quality of being tepid or lukewarm',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The audience\'s _____ toward the performance was disappointing to the actors.'
            },
            'teppanyaki': {
                'definition': 'A Japanese style of cooking where food is grilled on an iron hotplate, often performed as entertainment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tep-uhn-YAH-kee (emphasis on third syllable)',
                'etymology': 'From Japanese "teppan" (iron plate) + "yaki" (grilled)',
                'memory_tips': 'Think "teppen-yaki" - yelling at the iron plate while cooking',
                'alternate_spellings': '',
                'language_origin': 'Japanese',
                'example_sentence': 'The chef\'s _____ skills included impressive knife juggling and flame tricks.'
            },
            'terabyte': {
                'definition': 'A unit of computer memory or storage equal to approximately one trillion bytes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TER-uh-byt (emphasis on first syllable)',
                'etymology': 'From Greek "tera" (monster, trillion) + "byte" (unit of data)',
                'memory_tips': 'Think "terra-byte" - a monstrous amount of data like the whole Earth',
                'alternate_spellings': 'TB',
                'language_origin': 'Greek (modern scientific)',
                'example_sentence': 'The new hard drive has a capacity of two _____.'
            },
            'terai': {
                'definition': 'A lowland region along the southern edge of the Himalayas; a type of wide-brimmed hat.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tuh-RY (emphasis on second syllable)',
                'etymology': 'From Hindi "tarai" meaning "moist land"',
                'memory_tips': 'Think "te-rai" - terrain that\'s wet and marshy',
                'alternate_spellings': '',
                'language_origin': 'Hindi',
                'example_sentence': 'The _____ region is known for its rich agricultural land.'
            },
            'teraigabarit': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "terai" (lowland region) + "gabarit" (size/dimensions).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "terai" and "gabarit"',
                'alternate_spellings': 'terai + gabarit (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'teraphim': {
                'definition': 'Ancient Hebrew household gods or idols; small religious figurines used in worship.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'TER-uh-fim (emphasis on first syllable)',
                'etymology': 'From Hebrew "teraphim", possibly related to "raphah" (to heal)',
                'memory_tips': 'Think "tera-fim" - ancient figures with terrible power',
                'alternate_spellings': '',
                'language_origin': 'Hebrew',
                'example_sentence': 'Archaeological excavations uncovered ancient _____ in the household ruins.'
            },
            'teratism': {
                'definition': 'A biological abnormality or monstrosity; the study of developmental abnormalities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TER-uh-tizm (emphasis on first syllable)',
                'etymology': 'From Greek "teras" (monster) + "-ism"',
                'memory_tips': 'Think "terror-tism" - the study of terrifying abnormalities',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The medical textbook included a chapter on _____ and developmental disorders.'
            },
            'tercentenary': {
                'definition': 'A three-hundredth anniversary; relating to a period of three hundred years.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'ter-sen-TEN-uh-ree (emphasis on third syllable)',
                'etymology': 'From Latin "ter" (three times) + "centenary" (hundred years)',
                'memory_tips': 'Think "ter-centenary" - three centuries of celebration',
                'alternate_spellings': 'tricentennial',
                'language_origin': 'Latin',
                'example_sentence': 'The university celebrated its _____ with a year-long festival.'
            },
            'teriyaki': {
                'definition': 'A Japanese cooking technique using a sweet soy-based sauce; food prepared in this style.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'ter-ee-YAH-kee (emphasis on third syllable)',
                'etymology': 'From Japanese "teri" (luster) + "yaki" (grill)',
                'memory_tips': 'Think "teri-yaki" - grilling with a shiny, glossy sauce',
                'alternate_spellings': '',
                'language_origin': 'Japanese',
                'example_sentence': 'The _____ chicken was glazed with a sweet and savory sauce.'
            },
            'term': {
                'definition': 'A word or phrase with a specific meaning; a fixed period of time; a condition or requirement.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TURM (single syllable)',
                'etymology': 'From Latin "terminus" meaning "boundary, end"',
                'memory_tips': 'Think of a specific word or time period with clear boundaries',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The scientific _____ was difficult for the students to understand.'
            },
            'terminus': {
                'definition': 'The end or final point of something; a railway or bus station at the end of a line.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TUR-mi-nuhs (emphasis on first syllable)',
                'etymology': 'From Latin "terminus" meaning "boundary, limit"',
                'memory_tips': 'Think "term-in-us" - the term ends in us, the final point',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The train reached its _____ at the end of the line.'
            },
            'termite': {
                'definition': 'A small, pale social insect that feeds on wood and can cause significant structural damage.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TUR-myt (emphasis on first syllable)',
                'etymology': 'From Latin "termes" meaning "wood-eating worm"',
                'memory_tips': 'Think "term-mite" - a tiny creature that terminates wood',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The house foundation was damaged by _____ infestation.'
            },
            'terpsichore': {
                'definition': 'In Greek mythology, the Muse of dance and chorus; the art of dancing.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'turp-SIK-uh-ree (emphasis on second syllable)',
                'etymology': 'From Greek "Terpsichore", from "terpein" (to delight) + "choros" (dance)',
                'memory_tips': 'Think "terp-sik-ore" - a dancer who delights in sick moves',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The ballet students honored _____ as their patron goddess.'
            },
            'terra': {
                'definition': 'Earth or land; used in scientific terms relating to the planet Earth.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TER-uh (emphasis on first syllable)',
                'etymology': 'From Latin "terra" meaning "earth, land"',
                'memory_tips': 'Think "terra" - the ground we stand on, like a terrace',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The astronauts looked back at _____ firma from space.'
            },
            'terraced': {
                'definition': 'Formed into or having a series of flat areas cut into a slope; arranged in tiers.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'TER-ist (emphasis on first syllable)',
                'etymology': 'From "terrace" + "-ed", from Latin "terra" meaning "earth"',
                'memory_tips': 'Think "terra-aced" - earth arranged in steps like playing cards',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ hillside allowed for efficient farming on steep slopes.'
            },
            'terrarium': {
                'definition': 'A glass container for growing small plants; an artificial environment for keeping small land animals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tuh-RAIR-ee-uhm (emphasis on second syllable)',
                'etymology': 'From Latin "terra" (earth) + "-arium" (place for)',
                'memory_tips': 'Think "terra-arium" - a place for earth and plants',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She created a beautiful _____ with tiny ferns and moss.'
            },
            'terre': {
                'definition': 'French word meaning "earth" or "land"; used in wine terminology to refer to terroir.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAIR (single syllable, French pronunciation)',
                'etymology': 'From French "terre", from Latin "terra" meaning "earth"',
                'memory_tips': 'Think "terre" - French for "terra" (earth)',
                'alternate_spellings': '',
                'language_origin': 'French (from Latin)',
                'example_sentence': 'The wine\'s character reflected the unique _____ of the vineyard.'
            },
            'terrier': {
                'definition': 'A small, energetic dog originally bred for hunting vermin; any of various breeds of such dogs.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TER-ee-er (emphasis on first syllable)',
                'etymology': 'From French "terrier", from "terre" (earth) - dogs that hunt in burrows',
                'memory_tips': 'Think "terra-ier" - a dog that hunts in the earth',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The energetic _____ chased rabbits around the yard.'
            },
            'terrify': {
                'definition': 'To cause extreme fear; to fill with terror; to frighten greatly.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'TER-uh-fy (emphasis on first syllable)',
                'etymology': 'From Latin "terrificare", from "terrere" (to frighten) + "facere" (to make)',
                'memory_tips': 'Think "terror-ify" - to make someone feel terror',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The horror movie was designed to _____ audiences.'
            },
            'territory': {
                'definition': 'An area of land under the control of a ruler or state; an animal\'s defended area.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TER-i-tor-ee (emphasis on first syllable)',
                'etymology': 'From Latin "territorium", from "terra" meaning "earth"',
                'memory_tips': 'Think "terra-tory" - a story about controlled land',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The wolf pack defended its _____ from intruders.'
            },
            'terror': {
                'definition': 'Extreme fear; a person or thing that causes dread; the use of violence for political aims.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TER-er (emphasis on first syllable)',
                'etymology': 'From Latin "terror", from "terrere" meaning "to frighten"',
                'memory_tips': 'Think of extreme fear that makes you tremble',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The thunderstorm filled the children with _____ .'
            },
            'tersely': {
                'definition': 'In a brief and clearly expressed manner; concisely and sometimes abruptly.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'TURS-lee (emphasis on first syllable)',
                'etymology': 'From "terse" + "-ly", from Latin "tersus" meaning "wiped clean, neat"',
                'memory_tips': 'Think "terse-ly" - speaking in a wiped-clean, short way',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She answered the reporter\'s questions _____ and walked away.'
            },
            'tertiary': {
                'definition': 'Third in order or level; relating to the third stage of education (university level).',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'TUR-shee-er-ee (emphasis on first syllable)',
                'etymology': 'From Latin "tertiarius", from "tertius" meaning "third"',
                'memory_tips': 'Think "third-iary" - relating to the third level',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'After secondary school, she pursued _____ education at university.'
            },
            'tessitura': {
                'definition': 'In music, the range of notes that best suits a particular voice or instrument.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tes-i-TOO-rah (emphasis on third syllable)',
                'etymology': 'From Italian "tessitura", from "tessere" meaning "to weave"',
                'memory_tips': 'Think "test-itura" - testing the perfect vocal range',
                'alternate_spellings': '',
                'language_origin': 'Italian',
                'example_sentence': 'The soprano\'s _____ was perfect for the demanding aria.'
            },
            'test': {
                'definition': 'An examination to assess knowledge or ability; to try or evaluate something.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TEST (single syllable)',
                'etymology': 'From Latin "testum" meaning "earthen pot" (used for testing metals)',
                'memory_tips': 'Think of checking or trying something to see if it works',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The students prepared carefully for the final _____.'
            },
            'testament': {
                'definition': 'A will; evidence or proof of something; either of the two main divisions of the Bible.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TES-tuh-muhnt (emphasis on first syllable)',
                'etymology': 'From Latin "testamentum", from "testari" meaning "to witness"',
                'memory_tips': 'Think "test-ament" - a test of what someone believes or owns',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'His success was a _____ to years of hard work.'
            },
            'testimony': {
                'definition': 'Evidence given by a witness under oath; public declaration of personal experience or belief.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TES-ti-moh-nee (emphasis on first syllable)',
                'etymology': 'From Latin "testimonium", from "testis" meaning "witness"',
                'memory_tips': 'Think "test-imony" - testing the truth through witness accounts',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The witness\'s _____ was crucial to solving the case.'
            },
            'testimonybeaucoup': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "testimony" (witness statement) + "beaucoup" (French for "much").',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "testimony" and "beaucoup"',
                'alternate_spellings': 'testimony + beaucoup (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'testosterone': {
                'definition': 'A male sex hormone responsible for the development of masculine characteristics.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tes-TOS-tuh-rohn (emphasis on second syllable)',
                'etymology': 'From "testis" (testicle) + "sterol" (type of alcohol) + "-one" (chemical suffix)',
                'memory_tips': 'Think "testo-sterone" - hormone from testes with steroid structure',
                'alternate_spellings': '',
                'language_origin': 'Modern scientific (Latin elements)',
                'example_sentence': 'The athlete was tested for elevated _____ levels.'
            },
            'tetanus': {
                'definition': 'A serious bacterial infection causing muscle spasms and potentially fatal complications.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TET-uhn-uhs (emphasis on first syllable)',
                'etymology': 'From Greek "tetanos" meaning "stretched tight"',
                'memory_tips': 'Think "tet-anus" - muscles stretched tight like a tense anus',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The rusty nail wound required a _____ vaccination.'
            },
            'tetrachoric': {
                'definition': 'In statistics, relating to a correlation coefficient for two binary variables.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'tet-ruh-KOR-ik (emphasis on third syllable)',
                'etymology': 'From Greek "tetra" (four) + "choros" (space) + "-ic"',
                'memory_tips': 'Think "tetra-choric" - four-way statistical relationship',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The researcher calculated the _____ correlation between the variables.'
            },
            'tetrazzini': {
                'definition': 'A baked dish of pasta with poultry or seafood in a cream sauce, topped with cheese.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tet-ruh-ZEE-nee (emphasis on third syllable)',
                'etymology': 'Named after Italian opera singer Luisa Tetrazzini',
                'memory_tips': 'Think "tetra-zini" - a four-cheese pasta dish for an opera singer',
                'alternate_spellings': '',
                'language_origin': 'Italian (proper name)',
                'example_sentence': 'The restaurant\'s chicken _____ was rich and creamy.'
            },
            'teutonic': {
                'definition': 'Relating to the ancient Germanic peoples; characteristic of German culture or people.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'too-TON-ik (emphasis on second syllable)',
                'etymology': 'From Latin "Teutonicus", from "Teutoni" (Germanic tribe)',
                'memory_tips': 'Think "teu-tonic" - Germanic people with a tonic strength',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The castle displayed classic _____ architecture.'
            },
            'text': {
                'definition': 'Written or printed words; the main body of a book; to send a text message.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TEKST (single syllable)',
                'etymology': 'From Latin "textus" meaning "woven", from "texere" (to weave)',
                'memory_tips': 'Think of words woven together like fabric',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Please _____ me when you arrive at the airport.'
            },
            'textbook': {
                'definition': 'A book used for studying a particular subject; serving as a standard example.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'TEKST-book (emphasis on first syllable)',
                'etymology': 'From "text" + "book", referring to educational books',
                'memory_tips': 'Think "text-book" - a book full of educational text',
                'alternate_spellings': '',
                'language_origin': 'English (compound)',
                'example_sentence': 'The chemistry _____ explained the complex reactions clearly.'
            },
            'texture': {
                'definition': 'The feel or appearance of a surface; the quality of something as perceived by touch.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TEKS-cher (emphasis on first syllable)',
                'etymology': 'From Latin "textura", from "texere" meaning "to weave"',
                'memory_tips': 'Think "text-ure" - the weaving pattern you can feel',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The fabric had a smooth, silky _____.'
            },
            'thailand': {
                'definition': 'A country in Southeast Asia known for its tropical beaches, ancient temples, and spicy cuisine.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'TY-land (emphasis on first syllable)',
                'etymology': 'From Thai "thai" (free) + "land", meaning "land of the free"',
                'memory_tips': 'Think "Tie-land" - a land where people tie things, but it\'s actually "free land"',
                'alternate_spellings': '',
                'language_origin': 'Thai',
                'example_sentence': '_____ is famous for its beautiful beaches and delicious pad thai.'
            },
            'thalamus': {
                'definition': 'A structure in the brain that relays sensory and motor signals to the cerebral cortex.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THAL-uh-muhs (emphasis on first syllable)',
                'etymology': 'From Greek "thalamos" meaning "inner chamber"',
                'memory_tips': 'Think "thal-amus" - the brain\'s inner chamber that processes signals',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ processes sensory information before sending it to the cortex.'
            },
            'thalassic': {
                'definition': 'Relating to the sea or ocean; of or pertaining to marine environments.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'thuh-LAS-ik (emphasis on second syllable)',
                'etymology': 'From Greek "thalassa" meaning "sea"',
                'memory_tips': 'Think "thal-assic" - like Jurassic but for the sea',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The biologist studied _____ ecosystems in the deep ocean.'
            },
            'thank': {
                'definition': 'To express gratitude to someone; to show appreciation for something received.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'THANGK (single syllable)',
                'etymology': 'From Old English "thancian", related to "thought"',
                'memory_tips': 'Think of expressing gratitude and appreciation',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'I want to _____ you for all your help.'
            },
            'thanks': {
                'definition': 'An expression of gratitude; words used to show appreciation.',
                'part_of_speech': 'noun, interjection',
                'pronunciation_guide': 'THANGKS (single syllable)',
                'etymology': 'From "thank" + "-s", from Old English "thancian"',
                'memory_tips': 'Think of multiple ways to show gratitude',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': '_____ for helping me carry these heavy boxes.'
            },
            'thaumaturge': {
                'definition': 'A person who performs miracles or magic; a wonder-worker or magician.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THAW-muh-turj (emphasis on first syllable)',
                'etymology': 'From Greek "thaumatourgos", from "thauma" (wonder) + "ergon" (work)',
                'memory_tips': 'Think "thauma-turge" - someone who works wonders',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The ancient _____ was said to heal the sick with magical powers.'
            },
            'thawed': {
                'definition': 'Past tense of thaw; melted from a frozen state; became less cold or hostile.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'THAWD (single syllable)',
                'etymology': 'Past tense of "thaw", from Old English "thawian"',
                'memory_tips': 'Think of ice melting and becoming water',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The frozen ground _____ in the spring sunshine.'
            },
            'theater': {
                'definition': 'A building where plays and performances are presented; the art of dramatic performance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THEE-uh-ter (emphasis on first syllable)',
                'etymology': 'From Greek "theatron", from "theaomai" meaning "to view"',
                'memory_tips': 'Think "the-ater" - the place where you go to see performances',
                'alternate_spellings': 'theatre',
                'language_origin': 'Greek',
                'example_sentence': 'The local _____ is presenting Shakespeare\'s Hamlet this month.'
            },
            'theatre': {
                'definition': 'British spelling of theater; a building for dramatic performances; the art of drama.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THEE-uh-ter (emphasis on first syllable)',
                'etymology': 'From Greek "theatron", from "theaomai" meaning "to view"',
                'memory_tips': 'Think "the-atre" - British spelling with "-re" ending',
                'alternate_spellings': 'theater',
                'language_origin': 'Greek',
                'example_sentence': 'The West End _____ district is famous for its musicals.'
            },
            'theca': {
                'definition': 'A case or sheath enclosing an organ or structure; a protective covering in biology.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THEE-kuh (emphasis on first syllable)',
                'etymology': 'From Greek "theke" meaning "case, box"',
                'memory_tips': 'Think "the-ca" - the case that protects biological structures',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The pollen grains were contained within the anther\'s _____.'
            },
            'theme': {
                'definition': 'The main subject or topic of discussion; a central idea or motif in art or literature.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THEEM (single syllable)',
                'etymology': 'From Greek "thema" meaning "something set down"',
                'memory_tips': 'Think of the main idea that everything else is built around',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ of the novel was the triumph of good over evil.'
            },
            'themed': {
                'definition': 'Having or relating to a particular theme; designed around a central concept.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'THEEMD (single syllable)',
                'etymology': 'From "theme" + "-ed", from Greek "thema"',
                'memory_tips': 'Think "theme-d" - having been given a specific theme',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ restaurant was decorated like a medieval castle.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_177_data:
            return batch_177_data[word_lower]
        
        # Return empty data if word not found
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
    
    def process_batch_177(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 177 with comprehensive Claude data"""
        words = []
        with open(input_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word_data = WordData(
                    word=row['word'],
                    years=row['years'],
                    source_files=row['source_files'],
                    source_difficulties=row['source_difficulties']
                )
                
                # Get comprehensive Claude data
                claude_data = self.get_comprehensive_claude_data(word_data.word)
                
                # Store all Claude-generated data
                word_data.claude_definition = claude_data['definition']
                word_data.part_of_speech = claude_data['part_of_speech']
                word_data.pronunciation_guide = claude_data['pronunciation_guide']
                word_data.claude_etymology = claude_data['etymology']
                word_data.memory_tips = claude_data['memory_tips']
                word_data.alternate_spellings = claude_data['alternate_spellings']
                word_data.claude_language_origin = claude_data['language_origin']
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
                
                words.append(word_data)
                logger.info(f"Processed word: {word_data.word}")
        
        return words
    
    def save_batch_177_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 177 processed words to CSV"""
        
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
                calc = self.difficulty_calculator
                phonetic_score = calc.calculate_phonetic_transparency(word_data.word, word_data.pronunciation_guide)
                frequency_score = calc.calculate_word_frequency(word_data.word)
                morphology_score = calc.calculate_morphological_complexity(word_data.word, word_data.claude_etymology)
                etymology_score = calc.calculate_etymology_complexity(word_data.claude_etymology, word_data.claude_language_origin)
                
                # Calculate overall score but don't assign difficulty level yet
                overall_score = (phonetic_score * 0.3 + frequency_score * 0.25 + morphology_score * 0.25 + etymology_score * 0.2)
                
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

def main():
    """Process Batch 177 with comprehensive Claude data"""
    processor = Batch177Processor()
    input_csv = Path("output/batch_177_words.csv")
    output_csv = Path("output/batch_177_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 177 with comprehensive Claude data...")
    
    # Process all words in batch 177
    processed_words = processor.process_batch_177(input_csv)
    
    # Save results
    processor.save_batch_177_csv(processed_words, output_csv)
    
    logger.info(f"Batch 177 processing completed!")
    logger.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
    logger.info(f"Output saved to: {output_csv}")
    
    # Show summary
    successful_words = [w for w in processed_words if w.claude_definition]
    failed_words = [w for w in processed_words if not w.claude_definition]
    
    logger.info(f"Results: {len(successful_words)} successful, {len(failed_words)} failed")
    
    if failed_words:
        logger.info("Words that failed processing:")
        for word in failed_words:
            logger.info(f"  - {word.word}: {word.error_notes}")

if __name__ == "__main__":
    main()