#!/usr/bin/env python3
"""
Process Batch 179 of Spelling Bee Words with Comprehensive Claude Data
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
            'theatre', 'theme', 'themed', 'territory', 'terror', 'tertiary', 'themes', 'therefore', 'thing', 'things', 'third', 'those', 'though',
            'thought', 'thousand', 'thousands', 'thread', 'three', 'threshold', 'throat', 'throughout', 'throw', 'thumbs', 'thursday', 'thus',
            'tide', 'tied', 'tiger', 'tigers', 'tightly', 'timber', 'timer', 'times', 'tiny', 'tired', 'tissue', 'title'
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
            ('que', 'k'), ('x', 'ks'), ('c', 'k'), ('c', 's'), ('th', 'th')
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
            'mega', 'micro', 'mini', 'multi', 'neo', 'pseudo', 'ultra', 'ac', 'ad', 'con', 'tele', 'ter', 'the', 'ti'
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

class Batch179Processor:
    """Processes Batch 179 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 179 words"""
        
        # Comprehensive data for all 50 words in Batch 179
        batch_179_data = {
            'thunderbolt': {
                'definition': 'A flash of lightning with its accompanying thunder; something sudden and shocking; a powerful or devastating force.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THUHN-der-bohlt (emphasis on first syllable)',
                'etymology': 'From "thunder" + "bolt", from Old English "thunor" + "bolt"',
                'memory_tips': 'Think "thunder-bolt" - a bolt of lightning that makes thunder',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The _____ struck the tree with tremendous force.'
            },
            'thurible': {
                'definition': 'A metal container suspended on chains, used for burning incense during religious ceremonies.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THOOR-uh-buhl (emphasis on first syllable)',
                'etymology': 'From Latin "thuribulum", from "thus" (incense)',
                'memory_tips': 'Think "thur-ible" - able to hold incense for ceremonies',
                'alternate_spellings': 'censer',
                'language_origin': 'Latin',
                'example_sentence': 'The priest swung the _____ as fragrant smoke filled the cathedral.'
            },
            'thursday': {
                'definition': 'The fifth day of the week, between Wednesday and Friday.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THURZ-day (emphasis on first syllable)',
                'etymology': 'From Old English "thursdæg", from Thor\'s day (Norse god of thunder)',
                'memory_tips': 'Think "Thor\'s-day" - the day named after the Norse god Thor',
                'alternate_spellings': '',
                'language_origin': 'Old English (from Norse)',
                'example_sentence': 'The meeting is scheduled for _____ afternoon.'
            },
            'thus': {
                'definition': 'In this way; therefore; as a result; to this degree or extent.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'THUHS (single syllable)',
                'etymology': 'From Old English "thus"',
                'memory_tips': 'Think "this" but with "thus" - meaning "in this way"',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The experiment failed; _____, we need to try a different approach.'
            },
            'thwartwise': {
                'definition': 'Crosswise; extending across something; in a direction that opposes or blocks.',
                'part_of_speech': 'adverb, adjective',
                'pronunciation_guide': 'THWORT-wyz (emphasis on first syllable)',
                'etymology': 'From "thwart" (across, crosswise) + "-wise"',
                'memory_tips': 'Think "thwart-wise" - wisely blocking or going across',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The beam was placed _____ to provide structural support.'
            },
            'thylacine': {
                'definition': 'An extinct carnivorous marsupial from Tasmania, also known as the Tasmanian tiger or wolf.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THY-luh-seen (emphasis on first syllable)',
                'etymology': 'From Greek "thylakos" (pouch) + Latin "-ine"',
                'memory_tips': 'Think "thy-la-cine" - thy pouch canine (marsupial dog-like animal)',
                'alternate_spellings': 'Tasmanian tiger',
                'language_origin': 'Greek and Latin',
                'example_sentence': 'The last _____ died in captivity in 1936.'
            },
            'thyme': {
                'definition': 'An aromatic herb of the mint family, used for seasoning and medicinal purposes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TYM (single syllable, rhymes with "time")',
                'etymology': 'From Greek "thymon", from "thyein" meaning "to sacrifice"',
                'memory_tips': 'Think "time" - thyme takes time to grow and adds flavor over time',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'She added fresh _____ to the roasted vegetables.'
            },
            'thyroid': {
                'definition': 'A butterfly-shaped gland in the neck that produces hormones regulating metabolism.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'THY-royd (emphasis on first syllable)',
                'etymology': 'From Greek "thyroeides", from "thyra" (door) + "-eides" (shaped like)',
                'memory_tips': 'Think "thy-roid" - thy shield-shaped gland (shaped like a door)',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The doctor ordered blood tests to check her _____ function.'
            },
            'tiara': {
                'definition': 'A decorative crown or headband, typically worn by women; a jeweled ornamental headpiece.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tee-AR-uh (emphasis on second syllable)',
                'etymology': 'From Greek "tiara", from Persian origin',
                'memory_tips': 'Think "tea-ara" - a fancy crown for tea parties',
                'alternate_spellings': '',
                'language_origin': 'Greek (from Persian)',
                'example_sentence': 'The princess wore a sparkling _____ for the coronation ceremony.'
            },
            'tibetan': {
                'definition': 'Relating to Tibet, its people, or culture; a native of Tibet or the Tibetan language.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ti-BET-uhn (emphasis on second syllable)',
                'etymology': 'From Tibet + "-an"',
                'memory_tips': 'Think "Tibet-an" - relating to Tibet',
                'alternate_spellings': '',
                'language_origin': 'English (from place name)',
                'example_sentence': 'The _____ monastery was built high in the mountains.'
            },
            'tibia': {
                'definition': 'The larger of the two bones in the lower leg; the shinbone.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TIB-ee-uh (emphasis on first syllable)',
                'etymology': 'From Latin "tibia" meaning "flute, pipe" (from its shape)',
                'memory_tips': 'Think "tib-ia" - the big bone that you can feel in your shin',
                'alternate_spellings': 'shinbone',
                'language_origin': 'Latin',
                'example_sentence': 'The soccer player fractured his _____ during the game.'
            },
            'tichodrome': {
                'definition': 'A small bird that climbs on rock faces and walls, also known as the wallcreeper.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TIK-oh-drohm (emphasis on first syllable)',
                'etymology': 'From Greek "teichos" (wall) + "dromos" (runner)',
                'memory_tips': 'Think "tick-o-drome" - a bird that ticks along walls like a metronome',
                'alternate_spellings': 'wallcreeper',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ used its curved bill to probe for insects in rock crevices.'
            },
            'tichodromesapporo': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "tichodrome" (wallcreeper bird) + "sapporo" (Japanese city).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "tichodrome" and "sapporo"',
                'alternate_spellings': 'tichodrome + sapporo (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'tickled': {
                'definition': 'Past tense of tickle; lightly touched to cause laughter; pleased or amused.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'TIK-uhld (emphasis on first syllable)',
                'etymology': 'Past tense of "tickle", from Middle English "tiklen"',
                'memory_tips': 'Think "tick-led" - led to laugh by light touches like a clock tick',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The baby _____ and giggled when his mother played with his feet.'
            },
            'tide': {
                'definition': 'The regular rise and fall of ocean water; a trend or tendency; a time or season.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TYD (single syllable)',
                'etymology': 'From Old English "tid" meaning "time, season"',
                'memory_tips': 'Think of water rising and falling with time',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The fishing boat returned with the evening _____.'
            },
            'tied': {
                'definition': 'Past tense of tie; fastened or bound with rope or string; equal in score.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'TYD (single syllable)',
                'etymology': 'Past tense of "tie", from Old English "tigan"',
                'memory_tips': 'Think "tie-d" - something has been tied up',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She _____ her shoelaces before starting the race.'
            },
            'tiff': {
                'definition': 'A minor quarrel or disagreement; a petty argument between friends or family.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TIF (single syllable)',
                'etymology': 'Of uncertain origin, possibly imitative of huffing sounds',
                'memory_tips': 'Think "tiff" - a quick, light argument that\'s over fast',
                'alternate_spellings': '',
                'language_origin': 'Uncertain origin',
                'example_sentence': 'The siblings had a small _____ over who would sit in the front seat.'
            },
            'tiffany': {
                'definition': 'A thin, transparent silk or muslin fabric; relating to the Tiffany brand of jewelry.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'TIF-uh-nee (emphasis on first syllable)',
                'etymology': 'From Old French "tifanie", from Greek "theophania" (divine appearance)',
                'memory_tips': 'Think "tiffy-any" - any fine, delicate fabric',
                'alternate_spellings': '',
                'language_origin': 'Greek (via Old French)',
                'example_sentence': 'The dress was made of delicate _____ that shimmered in the light.'
            },
            'tiffanytiffin': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "tiffany" (fine fabric) + "tiffin" (light meal).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "tiffany" and "tiffin"',
                'alternate_spellings': 'tiffany + tiffin (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'tiffin': {
                'definition': 'A light meal, especially lunch; a set of stacked containers for carrying food.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TIF-in (emphasis on first syllable)',
                'etymology': 'From Anglo-Indian, possibly from "tiffing" (sipping)',
                'memory_tips': 'Think "tiff-in" - a light meal that won\'t cause a tiff',
                'alternate_spellings': '',
                'language_origin': 'Anglo-Indian',
                'example_sentence': 'He packed his _____ in the traditional metal containers.'
            },
            'tiger': {
                'definition': 'A large wild cat with orange fur and black stripes, native to Asia.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TY-ger (emphasis on first syllable)',
                'etymology': 'From Greek "tigris", from Persian origin',
                'memory_tips': 'Think of the large orange and black striped cat',
                'alternate_spellings': '',
                'language_origin': 'Greek (from Persian)',
                'example_sentence': 'The _____ prowled silently through the jungle undergrowth.'
            },
            'tigers': {
                'definition': 'Plural of tiger; multiple large wild cats with distinctive orange and black striped coats.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'TY-gerz (emphasis on first syllable)',
                'etymology': 'Plural of "tiger", from Greek "tigris"',
                'memory_tips': 'Think of multiple big cats with stripes',
                'alternate_spellings': '',
                'language_origin': 'Greek (from Persian)',
                'example_sentence': 'The zoo\'s _____ were fed at feeding time.'
            },
            'tightly': {
                'definition': 'In a tight manner; firmly; securely; closely.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'TYT-lee (emphasis on first syllable)',
                'etymology': 'From "tight" + "-ly"',
                'memory_tips': 'Think "tight-ly" - in a tight, secure way',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'She held the rope _____ as she climbed down.'
            },
            'tiki': {
                'definition': 'A carved wooden or stone figure representing a Polynesian deity; relating to Polynesian culture.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'TEE-kee (emphasis on first syllable)',
                'etymology': 'From Maori "tiki"',
                'memory_tips': 'Think "tea-key" - a carved figure that might hold the key to island culture',
                'alternate_spellings': '',
                'language_origin': 'Maori',
                'example_sentence': 'The restaurant was decorated with authentic Polynesian _____ statues.'
            },
            'tikka': {
                'definition': 'An Indian dish of marinated meat or vegetables cooked on skewers; a style of Indian cooking.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TIK-uh (emphasis on first syllable)',
                'etymology': 'From Hindi "tikka" meaning "piece, chunk"',
                'memory_tips': 'Think "tick-a" - pieces of food that tick your taste buds',
                'alternate_spellings': '',
                'language_origin': 'Hindi',
                'example_sentence': 'The chicken _____ was marinated in yogurt and spices.'
            },
            'tikkun': {
                'definition': 'In Jewish mysticism, the process of repairing or correcting the world; a correction or amendment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ti-KOON (emphasis on second syllable)',
                'etymology': 'From Hebrew "tikkun" meaning "repair, correction"',
                'memory_tips': 'Think "tick-un" - ticking off items as you repair the world',
                'alternate_spellings': '',
                'language_origin': 'Hebrew',
                'example_sentence': 'The concept of _____ olam emphasizes humanity\'s role in perfecting the world.'
            },
            'tilapia': {
                'definition': 'A freshwater fish native to Africa and the Middle East, widely farmed for food.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ti-LAH-pee-uh (emphasis on second syllable)',
                'etymology': 'From modern Latin, possibly from a native African language',
                'memory_tips': 'Think "till-apia" - till the fish farm to grow apia fish',
                'alternate_spellings': '',
                'language_origin': 'Modern Latin (possibly African origin)',
                'example_sentence': 'The _____ was seasoned with herbs and grilled to perfection.'
            },
            'tillamook': {
                'definition': 'A type of cheese originally made by the Tillamook people; relating to this Native American tribe from Oregon.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'TIL-uh-mook (emphasis on first syllable)',
                'etymology': 'From Chinook jargon, name of a Native American people',
                'memory_tips': 'Think "till-a-mook" - till the land like a cow (moo) for cheese',
                'alternate_spellings': '',
                'language_origin': 'Chinook (Native American)',
                'example_sentence': 'The _____ cheddar was aged for several years to develop its sharp flavor.'
            },
            'tilleul': {
                'definition': 'A pale green color; the color of linden tree flowers; a light yellowish-green shade.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'ti-LUL (emphasis on second syllable)',
                'etymology': 'From French "tilleul" meaning "linden tree"',
                'memory_tips': 'Think "till-owl" - the color of leaves an owl might see',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The walls were painted in a soft _____ shade that complemented the garden view.'
            },
            'timber': {
                'definition': 'Wood prepared for use in building or carpentry; trees suitable for cutting into lumber.',
                'part_of_speech': 'noun, interjection',
                'pronunciation_guide': 'TIM-ber (emphasis on first syllable)',
                'etymology': 'From Old English "timber" meaning "building material"',
                'memory_tips': 'Think "tim-ber" - time to cut lumber from trees',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The loggers shouted "___!" as the massive tree began to fall.'
            },
            'timer': {
                'definition': 'A device that measures time intervals; a person who times events.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TY-mer (emphasis on first syllable)',
                'etymology': 'From "time" + "-er"',
                'memory_tips': 'Think "time-er" - something that measures time',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'She set the oven _____ for thirty minutes.'
            },
            'times': {
                'definition': 'Plural of time; periods or moments; occasions; multiplied by (in mathematics).',
                'part_of_speech': 'noun (plural), preposition',
                'pronunciation_guide': 'TYMZ (single syllable)',
                'etymology': 'Plural of "time", from Old English "tima"',
                'memory_tips': 'Think of multiple moments or multiplication',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'These are difficult _____ for everyone.'
            },
            'timidly': {
                'definition': 'In a timid manner; shyly; with lack of confidence or courage.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'TIM-id-lee (emphasis on first syllable)',
                'etymology': 'From "timid" + "-ly", from Latin "timidus"',
                'memory_tips': 'Think "timid-ly" - acting in a timid, shy way',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The child _____ approached the new teacher.'
            },
            'tinamou': {
                'definition': 'A ground-dwelling bird found in Central and South America, resembling a small ostrich.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TIN-uh-moo (emphasis on first syllable)',
                'etymology': 'From French "tinamou", from Galibi (Carib language)',
                'memory_tips': 'Think "tin-a-moo" - a bird that sounds like a tin cow',
                'alternate_spellings': '',
                'language_origin': 'Galibi (via French)',
                'example_sentence': 'The _____ is known for its beautiful, haunting calls.'
            },
            'tincture': {
                'definition': 'A solution of medicine in alcohol; a slight trace or hint of something; to tinge or color slightly.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TINK-cher (emphasis on first syllable)',
                'etymology': 'From Latin "tinctura", from "tingere" meaning "to dye"',
                'memory_tips': 'Think "tink-ture" - a liquid that tinkles when you add color',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The herbal _____ was taken with a few drops in water.'
            },
            'tinge': {
                'definition': 'A slight trace or touch of color; to color or flavor slightly.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TINJ (single syllable)',
                'etymology': 'From Latin "tingere" meaning "to dye, color"',
                'memory_tips': 'Think "tinge" - a tiny change in color',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The sunset had a pink _____ that reflected on the clouds.'
            },
            'tingle': {
                'definition': 'A slight prickling or stinging sensation; to feel or cause such a sensation.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TING-guhl (emphasis on first syllable)',
                'etymology': 'From Middle English "tinglen", possibly related to "tinkle"',
                'memory_tips': 'Think "ting-le" - a feeling that makes you want to wiggle',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'Her fingers began to _____ from the cold weather.'
            },
            'tinnient': {
                'definition': 'Making a ringing or tinkling sound; characterized by a metallic ringing quality.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'TIN-ee-uhnt (emphasis on first syllable)',
                'etymology': 'From Latin "tinniens", from "tinnire" meaning "to ring"',
                'memory_tips': 'Think "tin-ient" - efficient at making tin-like ringing sounds',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ sound of the bell echoed through the valley.'
            },
            'tinseltown': {
                'definition': 'A nickname for Hollywood, referring to the glamorous but artificial nature of the film industry.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TIN-suhl-town (emphasis on first syllable)',
                'etymology': 'From "tinsel" (shiny but cheap decoration) + "town"',
                'memory_tips': 'Think "tinsel-town" - a town decorated with shiny but fake glamour',
                'alternate_spellings': '',
                'language_origin': 'English (compound)',
                'example_sentence': 'Many aspiring actors move to _____ hoping to become movie stars.'
            },
            'tintinnabulary': {
                'definition': 'Relating to or characterized by the ringing of bells; having a bell-like sound.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'tin-ti-NAB-yuh-ler-ee (emphasis on third syllable)',
                'etymology': 'From Latin "tintinnabulum" (bell), from "tintinnare" (to ring)',
                'memory_tips': 'Think "tintin-nab-ulary" - vocabulary about ringing bells',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The poem\'s _____ rhythm mimicked the sound of church bells.'
            },
            'tiny': {
                'definition': 'Very small; minute; insignificant in size.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'TY-nee (emphasis on first syllable)',
                'etymology': 'From Middle English "tine" meaning "small"',
                'memory_tips': 'Think of something so small it\'s almost nothing',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The _____ ant carried a crumb twice its size.'
            },
            'tirade': {
                'definition': 'A long, angry speech criticizing someone or something; a prolonged outburst of harsh criticism.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TY-rayd (emphasis on second syllable)',
                'etymology': 'From French "tirade", from Italian "tirata" meaning "a drawing out"',
                'memory_tips': 'Think "tire-aid" - a long speech that tires everyone who hears it',
                'alternate_spellings': '',
                'language_origin': 'French (from Italian)',
                'example_sentence': 'The coach\'s _____ about teamwork lasted for twenty minutes.'
            },
            'tiramisu': {
                'definition': 'An Italian dessert made with ladyfingers, coffee, mascarpone cheese, and cocoa powder.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'teer-uh-mi-SOO (emphasis on fourth syllable)',
                'etymology': 'From Italian "tiramisù", literally "pick me up"',
                'memory_tips': 'Think "tire-me-sue" - but it actually picks you up with energy',
                'alternate_spellings': '',
                'language_origin': 'Italian',
                'example_sentence': 'The restaurant\'s _____ was the perfect end to the Italian meal.'
            },
            'tired': {
                'definition': 'Feeling in need of sleep or rest; weary; bored or fed up with something.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'TYRD (single syllable)',
                'etymology': 'Past participle of "tire", from Old English "teorian"',
                'memory_tips': 'Think of needing rest or sleep',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'After the long hike, everyone felt _____ and ready for bed.'
            },
            'tissue': {
                'definition': 'A group of similar cells in an organism; a disposable paper for wiping; delicate material.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TISH-oo (emphasis on first syllable)',
                'etymology': 'From French "tissu", from "tisser" meaning "to weave"',
                'memory_tips': 'Think "tish-ue" - soft material woven together',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The biologist examined the muscle _____ under a microscope.'
            },
            'titian': {
                'definition': 'A reddish-gold or auburn hair color; relating to the Venetian painter Titian.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'TISH-uhn (emphasis on first syllable)',
                'etymology': 'From Titian (Tiziano Vecellio), Venetian painter known for red-haired subjects',
                'memory_tips': 'Think "Titian" - the painter famous for red-gold hair colors',
                'alternate_spellings': '',
                'language_origin': 'Italian (from proper name)',
                'example_sentence': 'Her _____ hair gleamed like copper in the sunlight.'
            },
            'title': {
                'definition': 'The name of a book, movie, or other work; a word indicating rank or status; legal ownership.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TY-tuhl (emphasis on first syllable)',
                'etymology': 'From Latin "titulus" meaning "inscription, label"',
                'memory_tips': 'Think "title" - the label that tells you what something is',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ of the book immediately caught her attention.'
            },
            'titration': {
                'definition': 'A laboratory technique for determining the concentration of a solution by adding measured amounts of another solution.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ty-TRAY-shuhn (emphasis on second syllable)',
                'etymology': 'From French "titrer" meaning "to determine the title/strength"',
                'memory_tips': 'Think "titer-ation" - repeatedly measuring to determine strength',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The chemistry student performed a _____ to find the acid concentration.'
            },
            'tlingitdetainees': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "tlingit" (Native American people) + "detainees" (people held in custody).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "tlingit" and "detainees"',
                'alternate_spellings': 'tlingit + detainees (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'tmesis': {
                'definition': 'A linguistic phenomenon where a word is split by inserting another word or phrase in the middle.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tuh-MEE-sis (emphasis on second syllable)',
                'etymology': 'From Greek "tmesis" meaning "a cutting"',
                'memory_tips': 'Think "t-mesis" - cutting a word in the middle like "abso-freaking-lutely"',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The phrase "abso-bloody-lutely" is an example of _____.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_179_data:
            return batch_179_data[word_lower]
        
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
    
    def process_batch_179(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 179 with comprehensive Claude data"""
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
    
    def save_batch_179_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 179 processed words to CSV"""
        
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
    """Process Batch 179 with comprehensive Claude data"""
    processor = Batch179Processor()
    input_csv = Path("output/batch_179_words.csv")
    output_csv = Path("output/batch_179_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 179 with comprehensive Claude data...")
    
    # Process all words in batch 179
    processed_words = processor.process_batch_179(input_csv)
    
    # Save results
    processor.save_batch_179_csv(processed_words, output_csv)
    
    logger.info(f"Batch 179 processing completed!")
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