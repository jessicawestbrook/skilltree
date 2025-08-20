#!/usr/bin/env python3
"""
Process Batch 036 of Spelling Bee Words with Comprehensive Claude Data
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
            'government', 'company', 'number', 'group', 'problem', 'fact', 'actually', 'across', 'activities', 'activity', 'adding', 'addition'
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
            'mega', 'micro', 'mini', 'multi', 'neo', 'pseudo', 'ultra', 'ac', 'ad', 'con'
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

class Batch036Processor:
    """Processes Batch 036 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 036 words"""
        
        # Comprehensive data for all 50 words in Batch 036
        batch_036_data = {
            'click': {
                'definition': 'To make a short, sharp sound; to press and release a button on a computer mouse; to select something on a computer; to suddenly understand or work well together.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'KLIK (emphasis on single syllable)',
                'etymology': 'Imitative word representing the sound, first recorded in the 17th century',
                'memory_tips': 'Think of the sound a computer mouse makes when you press it',
                'alternate_spellings': '',
                'language_origin': 'Imitative (English)',
                'example_sentence': 'Please _____ the link to open the website in a new tab.'
            },
            'clickbait': {
                'definition': 'Internet content with sensationalized headlines designed to attract clicks and generate revenue, often misleading or of poor quality.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLIK-bayt (emphasis on first syllable)',
                'etymology': 'Compound of "click" + "bait", coined in the internet age (early 2000s)',
                'memory_tips': 'Think "click-bait" - bait to make people click on links',
                'alternate_spellings': 'click-bait (hyphenated)',
                'language_origin': 'Modern English (compound)',
                'example_sentence': 'The article was obvious _____ with its exaggerated "You Won\'t Believe What Happened Next" headline.'
            },
            'clientele': {
                'definition': 'The customers or clients of a professional person or business, considered as a group; a body of customers.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kly-uhn-TELL (emphasis on third syllable)',
                'etymology': 'From French "clientèle", from Latin "cliens" (dependent, follower)',
                'memory_tips': 'Think "client-eel" - a slippery group of clients like eels',
                'alternate_spellings': '',
                'language_origin': 'French (from Latin)',
                'example_sentence': 'The upscale restaurant catered to a wealthy _____ from the financial district.'
            },
            'cliff': {
                'definition': 'A steep rock face, especially at the edge of the sea; a vertical or near-vertical rock exposure.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLIF (emphasis on single syllable)',
                'etymology': 'From Old English "clif", from Proto-Germanic "*klibą"',
                'memory_tips': 'Think of standing at the edge of a high cliff looking down',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The lighthouse stood majestically on the rocky _____ overlooking the ocean.'
            },
            'climate': {
                'definition': 'The long-term weather conditions in a particular area; the prevailing trend of opinion or feeling; an environment or situation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLY-mit (emphasis on first syllable)',
                'etymology': 'From Greek "klima" (inclination, latitude), from "klinein" (to lean)',
                'memory_tips': 'Think "climb-ate" - how the weather climbs and changes over time',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The tropical _____ made it perfect for growing exotic fruits year-round.'
            },
            'climateyankee': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "climate" (weather conditions) + "Yankee" (Northern American).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "climate" and "Yankee"',
                'alternate_spellings': 'climate + Yankee (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'climb': {
                'definition': 'To go up or ascend, especially by using hands and feet; to move upward on or over; to rise in social position or value.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'KLYM (emphasis on single syllable)',
                'etymology': 'From Old English "climban", related to German "klimmen"',
                'memory_tips': 'Think of climbing a mountain or ladder, going up step by step',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The experienced mountaineer decided to _____ the steep rock face without ropes.'
            },
            'climbers': {
                'definition': 'People who climb mountains, rocks, or other vertical surfaces; plants that grow upward by attaching to supports.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'KLY-merz (emphasis on first syllable)',
                'etymology': 'From "climb" + "-er" + "-s", where climb comes from Old English "climban"',
                'memory_tips': 'Think of mountain climbers with ropes and gear, or ivy climbers on walls',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The experienced _____ reached the summit just as the sun began to set.'
            },
            'cling': {
                'definition': 'To hold on tightly to something; to stick closely; to remain emotionally attached; to adhere.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'KLING (emphasis on single syllable)',
                'etymology': 'From Old English "clingan", related to German "klingen"',
                'memory_tips': 'Think of how plastic wrap clings to a bowl, or how a child clings to a parent',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The wet shirt would _____ uncomfortably to his back after the rainstorm.'
            },
            'clobbered': {
                'definition': 'Past tense of clobber; hit hard; defeated decisively; criticized severely.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'KLOB-erd (emphasis on first syllable)',
                'etymology': 'From "clobber", origin uncertain, possibly imitative or from "club"',
                'memory_tips': 'Think "club-ered" - like being hit with a club',
                'alternate_spellings': '',
                'language_origin': 'Uncertain (possibly imitative)',
                'example_sentence': 'The home team got _____ by their rivals in a humiliating 45-0 defeat.'
            },
            'clock': {
                'definition': 'An instrument that measures and displays time; to time something with a stopwatch; to reach a particular speed or time.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'KLOK (emphasis on single syllable)',
                'etymology': 'From Middle Dutch "klocke" (bell), related to "clack" (sound)',
                'memory_tips': 'Think of the ticking sound and round face with hands pointing to numbers',
                'alternate_spellings': '',
                'language_origin': 'Middle Dutch',
                'example_sentence': 'The antique grandfather _____ chimed melodiously every hour on the hour.'
            },
            'clodhopper': {
                'definition': 'A clumsy person; a large, heavy shoe or boot; someone from a rural area (sometimes derogatory).',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLOD-hop-er (emphasis on first syllable)',
                'etymology': 'Compound of "clod" (lump of earth) + "hopper" (one who hops)',
                'memory_tips': 'Think "clod-hopper" - someone who hops on clods of dirt with big boots',
                'alternate_spellings': '',
                'language_origin': 'English (compound)',
                'example_sentence': 'His muddy clodhoppers left dirty prints across the clean kitchen floor.'
            },
            'cloisters': {
                'definition': 'Covered walks around a courtyard in religious buildings; monasteries or convents; secluded places.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'KLOY-sterz (emphasis on first syllable)',
                'etymology': 'From Old French "cloistre", from Latin "claustrum" (enclosed place)',
                'memory_tips': 'Think "close-ters" - closed areas where monks and nuns walk and pray',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'The medieval _____ provided a peaceful place for contemplation and prayer.'
            },
            'close': {
                'definition': 'Near in space or time; having a strong relationship; to shut; to end; to bring together.',
                'part_of_speech': 'adjective, verb, noun, adverb',
                'pronunciation_guide': 'KLOHS (as adjective) or KLOHZ (as verb)',
                'etymology': 'From Old French "clos" (enclosed), from Latin "clausus" (closed)',
                'memory_tips': 'Think of closing a door or being close to someone you love',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'Please _____ the window before the rain starts falling.'
            },
            'closed': {
                'definition': 'Past tense of close; shut; not open; ended; not accessible to the public.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'KLOHZD (emphasis on single syllable)',
                'etymology': 'Past tense of "close", from Latin "clausus"',
                'memory_tips': 'Think of a door that has been closed, or a store that is closed',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'The store was _____ for renovations throughout the entire month of July.'
            },
            'closer': {
                'definition': 'Comparative form of close; nearer; a person who completes deals; a relief pitcher who finishes games.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'KLOH-ser (emphasis on first syllable)',
                'etymology': 'Comparative form of "close" + "-er"',
                'memory_tips': 'Think "close-er" - more close than before',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'Each step brought them _____ to reaching the mountain summit.'
            },
            'closet': {
                'definition': 'A small room or cupboard for storing clothes; a state of secrecy; to shut away privately.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'KLOZ-it (emphasis on first syllable)',
                'etymology': 'From Old French "closet", diminutive of "clos" (enclosed space)',
                'memory_tips': 'Think of a small, enclosed space where you hang clothes',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'She organized her _____ by color and season to make choosing outfits easier.'
            },
            'closure': {
                'definition': 'The act of closing something; a sense of completion or resolution; the end of a debate in a legislature.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLOH-zher (emphasis on first syllable)',
                'etymology': 'From Old French "closure", from Latin "clausura" (a closing)',
                'memory_tips': 'Think "close-ure" - the state or act of closing something',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'After years of therapy, she finally found _____ regarding her father\'s death.'
            },
            'cloth': {
                'definition': 'Woven or knitted material made from threads or fibers; fabric used for making clothes or other items.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLOTH (emphasis on single syllable)',
                'etymology': 'From Old English "clāth", related to German "Kleid" (clothing)',
                'memory_tips': 'Think of soft fabric material used to make clothes',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The tailor examined the fine silk _____ before beginning to cut the pattern.'
            },
            'clothes': {
                'definition': 'Items worn to cover the body; garments such as shirts, pants, dresses, and jackets.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'KLOHZ (emphasis on single syllable)',
                'etymology': 'Plural of "cloth", from Old English "clāth"',
                'memory_tips': 'Think of all the different garments hanging in your closet',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She packed warm _____ for the winter camping trip in the mountains.'
            },
            'clothing': {
                'definition': 'Clothes collectively; garments used to cover and protect the body; the business of making or selling clothes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLOH-thing (emphasis on first syllable)',
                'etymology': 'From "clothe" + "-ing", where clothe comes from Old English "clāthian"',
                'memory_tips': 'Think "cloth-ing" - the act of putting on cloth or fabric items',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The charity collected winter _____ donations for families in need.'
            },
            'cloture': {
                'definition': 'A parliamentary procedure to end debate and force a vote; the closure of discussion in a legislative body.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'KLOH-cher (emphasis on first syllable)',
                'etymology': 'From French "clôture" (enclosure, closure), from Latin "clausura"',
                'memory_tips': 'Think "closure" - ending debate by closing off discussion',
                'alternate_spellings': '',
                'language_origin': 'French (from Latin)',
                'example_sentence': 'The senator called for _____ to end the filibuster and proceed to the vote.'
            },
            'cloud': {
                'definition': 'A visible mass of water droplets or ice crystals in the atmosphere; something that obscures; online data storage.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'KLOWD (emphasis on single syllable)',
                'etymology': 'From Old English "clūd" (rock, hill), later applied to masses in the sky',
                'memory_tips': 'Think of fluffy white shapes floating in the blue sky',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The dark _____ formation suggested that rain was approaching quickly.'
            },
            'cloudy': {
                'definition': 'Covered with clouds; not clear or transparent; confused or unclear in meaning.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'KLOW-dee (emphasis on first syllable)',
                'etymology': 'From "cloud" + "-y", where cloud comes from Old English "clūd"',
                'memory_tips': 'Think "cloud-y" - full of clouds, like a gray overcast day',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The weather forecast predicted _____ skies with a chance of afternoon showers.'
            },
            'clouting': {
                'definition': 'Present participle of clout; hitting hard; having influence or power; patching with cloth.',
                'part_of_speech': 'verb (present participle)',
                'pronunciation_guide': 'KLOW-ting (emphasis on first syllable)',
                'etymology': 'From "clout", from Old English "clūt" (patch, piece of cloth)',
                'memory_tips': 'Think "clout-ing" - using your clout or hitting with force',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The boxer was _____ his opponent with powerful uppercuts.'
            },
            'clover': {
                'definition': 'A small plant with three-lobed leaves, often grown for animal feed; a symbol of good luck when four-leafed.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLOH-ver (emphasis on first syllable)',
                'etymology': 'From Old English "clæfre", related to German "Klee"',
                'memory_tips': 'Think of lucky four-leaf clovers in a green field',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The children searched the field for a rare four-leaf _____ to bring good luck.'
            },
            'clowder': {
                'definition': 'A group or cluster of cats; the collective noun for a gathering of domestic cats.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLOW-der (emphasis on first syllable)',
                'etymology': 'From Middle English "clodder" (to clot), related to "clot"',
                'memory_tips': 'Think "cloud-er" - a cloud of cats clustered together',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'A _____ of feral cats had made their home in the abandoned warehouse.'
            },
            'cloying': {
                'definition': 'Excessively sweet or sentimental; so sweet as to be disgusting; overly flattering.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'KLOY-ing (emphasis on first syllable)',
                'etymology': 'From "cloy" (to surfeit), from Old French "encloer" (to nail up)',
                'memory_tips': 'Think "cloy-ing" - clogging your taste buds with too much sweetness',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The dessert was so _____ that she couldn\'t finish more than a few bites.'
            },
            'club': {
                'definition': 'A heavy stick used as a weapon; an organization of people with common interests; a playing card suit; to hit with a club.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'KLUB (emphasis on single syllable)',
                'etymology': 'From Old Norse "klubba" (cudgel), related to "clump"',
                'memory_tips': 'Think of a caveman\'s club or a social club where people gather',
                'alternate_spellings': '',
                'language_origin': 'Old Norse',
                'example_sentence': 'She joined the book _____ to discuss literature with other avid readers.'
            },
            'clue': {
                'definition': 'A piece of evidence or information that helps solve a problem or mystery; a hint or indication.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'KLOO (emphasis on single syllable)',
                'etymology': 'From "clew" (ball of yarn), referring to the thread that guided Theseus out of the labyrinth',
                'memory_tips': 'Think of detectives following clues to solve a mystery',
                'alternate_spellings': '',
                'language_origin': 'Middle English (from Greek myth)',
                'example_sentence': 'The detective found an important _____ that led to solving the case.'
            },
            'clutch': {
                'definition': 'To grasp tightly; a mechanism that connects or disconnects power transmission; a small bag; a critical situation.',
                'part_of_speech': 'verb, noun, adjective',
                'pronunciation_guide': 'KLUCH (emphasis on single syllable)',
                'etymology': 'From Old English "clyccan" (to bend, clench)',
                'memory_tips': 'Think of clutching something tightly in your hand, or a car\'s clutch pedal',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She had to _____ the railing tightly as she walked down the steep stairs.'
            },
            'cluttered': {
                'definition': 'Past tense of clutter; filled with scattered objects in an untidy way; messy and disorganized.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'KLUT-erd (emphasis on first syllable)',
                'etymology': 'From "clutter", possibly from "clot" or imitative of confused sounds',
                'memory_tips': 'Think "clutter-ed" - a room that has been filled with scattered clutter',
                'alternate_spellings': '',
                'language_origin': 'Uncertain (possibly from clot)',
                'example_sentence': 'Her desk was so _____ with papers that she couldn\'t find her important documents.'
            },
            'clydesdale': {
                'definition': 'A breed of large, powerful draft horses originally from Scotland, known for their strength and distinctive feathered legs.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLYDZ-dayl (emphasis on first syllable)',
                'etymology': 'Named after the River Clyde valley in Scotland where the breed was developed',
                'memory_tips': 'Think "Clyde\'s-dale" - horses from the dale (valley) of the River Clyde',
                'alternate_spellings': 'Clydesdale (capitalized as proper noun)',
                'language_origin': 'Scottish (place name)',
                'example_sentence': 'The magnificent _____ horses pulled the brewery wagon through the parade.'
            },
            'cnidarian': {
                'definition': 'A member of the phylum Cnidaria, including jellyfish, corals, and sea anemones, characterized by stinging cells.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'ny-DARE-ee-uhn (emphasis on second syllable)',
                'etymology': 'From Greek "knide" (nettle) + "-arian", referring to their stinging cells',
                'memory_tips': 'Think "needle-arian" - creatures with needle-like stinging cells',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The marine biologist studied various _____ species in the coral reef ecosystem.'
            },
            'coach': {
                'definition': 'A person who trains athletes or teaches skills; a bus for long-distance travel; a railway carriage; to train or instruct.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'KOHCH (emphasis on single syllable)',
                'etymology': 'From Hungarian "kocsi" (wagon from Kocs), via French "coche"',
                'memory_tips': 'Think of a sports coach with a whistle, or a horse-drawn coach',
                'alternate_spellings': '',
                'language_origin': 'Hungarian (via French)',
                'example_sentence': 'The basketball _____ motivated the team with an inspiring halftime speech.'
            },
            'coadjutor': {
                'definition': 'An assistant or helper, especially a bishop appointed to assist another bishop; a colleague who shares duties.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'koh-AD-juh-ter (emphasis on second syllable)',
                'etymology': 'From Latin "coadjutor", from "co-" (together) + "adjutare" (to help)',
                'memory_tips': 'Think "co-adjutor" - someone who helps adjust things together with you',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The elderly bishop relied heavily on his _____ to handle the daily administrative duties.'
            },
            'coalescence': {
                'definition': 'The process of coming together to form one mass or whole; the fusion of separate elements into a unified entity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'koh-uh-LES-uhns (emphasis on third syllable)',
                'etymology': 'From Latin "coalescere", from "co-" (together) + "alescere" (to grow up)',
                'memory_tips': 'Think "co-ales-cence" - growing together like ale fermenting into one brew',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ of the water droplets formed larger drops that rolled down the window.'
            },
            'coalition': {
                'definition': 'An alliance or union of different groups working together for a common purpose; a temporary partnership.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'koh-uh-LISH-uhn (emphasis on third syllable)',
                'etymology': 'From Latin "coalitio", from "coalescere" (to grow together)',
                'memory_tips': 'Think "co-alition" - different groups becoming allied together',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The environmental _____ brought together diverse organizations to fight climate change.'
            },
            'coarse': {
                'definition': 'Having a rough texture; lacking refinement; crude or vulgar in behavior or language.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'KORS (emphasis on single syllable)',
                'etymology': 'From Old French "cors" (ordinary, common), from Latin "cursus" (course)',
                'memory_tips': 'Think "course" - rough like a golf course, not smooth like a course meal',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'The _____ sandpaper was perfect for removing the old paint from the wooden fence.'
            },
            'coastal': {
                'definition': 'Relating to or located on the coast; near the sea or ocean; characteristic of coastal areas.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'KOHS-tuhl (emphasis on first syllable)',
                'etymology': 'From "coast" + "-al", where coast comes from Latin "costa" (rib, side)',
                'memory_tips': 'Think "coast-al" - relating to the coast where land meets sea',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ village depended on fishing and tourism for its economic survival.'
            },
            'coat': {
                'definition': 'An outer garment worn to provide warmth or protection; a layer of paint or other substance; the fur of an animal.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'KOHT (emphasis on single syllable)',
                'etymology': 'From Old French "cote" (tunic), from Frankish "*kotta"',
                'memory_tips': 'Think of putting on a warm coat in winter, or coating something with paint',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Frankish)',
                'example_sentence': 'She put on her heavy winter _____ before venturing out into the snowstorm.'
            },
            'coaxation': {
                'definition': 'The act of coaxing or persuading gently; gentle persuasion or encouragement to do something.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'koh-ak-SAY-shuhn (emphasis on third syllable)',
                'etymology': 'From "coax" + "-ation", where coax is of uncertain origin, possibly from "cokes" (fool)',
                'memory_tips': 'Think "coax-ation" - the action of coaxing someone into doing something',
                'alternate_spellings': '',
                'language_origin': 'Uncertain (possibly from obsolete "cokes")',
                'example_sentence': 'Through gentle _____, the teacher convinced the shy student to participate in the play.'
            },
            'coaxationardoise': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "coaxation" (gentle persuasion) + "ardoise" (French for slate).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "coaxation" and "ardoise"',
                'alternate_spellings': 'coaxation + ardoise (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'coaxing': {
                'definition': 'Present participle of coax; persuading gently; using gentle pressure to convince someone to do something.',
                'part_of_speech': 'verb (present participle)',
                'pronunciation_guide': 'KOHK-sing (emphasis on first syllable)',
                'etymology': 'From "coax" + "-ing", where coax is of uncertain origin',
                'memory_tips': 'Think "coax-ing" - gently coaxing like training a pet with treats',
                'alternate_spellings': '',
                'language_origin': 'Uncertain',
                'example_sentence': 'She was _____ the frightened kitten out from under the porch with soft words.'
            },
            'cobalamin': {
                'definition': 'Vitamin B12, an essential nutrient important for nerve function, red blood cell formation, and DNA synthesis.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'koh-BAL-ah-min (emphasis on second syllable)',
                'etymology': 'From "cobalt" (the metal at its center) + "amine" (organic compound)',
                'memory_tips': 'Think "cobalt-amine" - a vitamin containing cobalt that helps maintain energy',
                'alternate_spellings': '',
                'language_origin': 'Modern scientific (cobalt + amine)',
                'example_sentence': 'Vegans often need to supplement their diet with _____ since it\'s primarily found in animal products.'
            },
            'cobblestone': {
                'definition': 'A naturally rounded stone used for paving streets; a street or path paved with such stones.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KOB-uhl-stohn (emphasis on first syllable)',
                'etymology': 'From "cobble" (rounded stone) + "stone", where cobble may be from "cob" (lump)',
                'memory_tips': 'Think "cobble-stone" - stones cobbled together to make old European streets',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The horse-drawn carriage clattered loudly over the ancient _____ streets.'
            },
            'cobweb': {
                'definition': 'A spider\'s web, especially an old or dusty one; something that catches and holds like a web.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KOB-web (emphasis on first syllable)',
                'etymology': 'From Middle English "coppeweb", from "coppe" (spider) + "web"',
                'memory_tips': 'Think "cob-web" - a web made by a spider (historically called "cob")',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'She walked through the old attic, brushing away _____ that had accumulated over the years.'
            },
            'coccidiosis': {
                'definition': 'A parasitic disease caused by protozoa of the genus Coccidia, affecting the intestinal tract of animals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kok-sid-ee-OH-sis (emphasis on fourth syllable)',
                'etymology': 'From "Coccidia" (genus name) + "-osis" (diseased condition)',
                'memory_tips': 'Think "cock-seed-ee-osis" - a disease that affects chickens and other animals',
                'alternate_spellings': '',
                'language_origin': 'Modern scientific (Greek elements)',
                'example_sentence': 'The veterinarian diagnosed the chickens with _____ and prescribed appropriate medication.'
            },
            'coccygeal': {
                'definition': 'Relating to the coccyx or tailbone; pertaining to the small triangular bone at the base of the spine.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'kok-SIJ-ee-uhl (emphasis on second syllable)',
                'etymology': 'From "coccyx" + "-eal", where coccyx comes from Greek "kokkyx" (cuckoo bird)',
                'memory_tips': 'Think "cuckoo-geal" - relating to the cuckoo-shaped tailbone',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The patient complained of _____ pain after falling down the stairs.'
            },
            'cochin': {
                'definition': 'A breed of large domestic chicken known for its fluffy feathers and gentle temperament; also a city in India (Kochi).',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KOH-chin (emphasis on first syllable)',
                'etymology': 'Named after Cochin (now Kochi), India, where the chickens were thought to originate',
                'memory_tips': 'Think "coach-in" - a fluffy chicken that looks like it could ride in a coach',
                'alternate_spellings': 'Cochin (capitalized when referring to place or breed)',
                'language_origin': 'Place name (India)',
                'example_sentence': 'The farmer\'s prize _____ hen was known for laying large brown eggs regularly.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_036_data:
            return batch_036_data[word_lower]
        
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
    
    def process_batch_036(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 036 with comprehensive Claude data"""
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
    
    def save_batch_036_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 036 processed words to CSV"""
        
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
    """Process Batch 036 with comprehensive Claude data"""
    processor = Batch036Processor()
    input_csv = Path("output/batch_036_words.csv")
    output_csv = Path("output/batch_036_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 036 with comprehensive Claude data...")
    
    # Process all words in batch 036
    processed_words = processor.process_batch_036(input_csv)
    
    # Save results
    processor.save_batch_036_csv(processed_words, output_csv)
    
    logger.info(f"Batch 036 processing completed!")
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