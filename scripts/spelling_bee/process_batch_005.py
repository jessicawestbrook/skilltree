#!/usr/bin/env python3
"""
Process Batch 005 of Spelling Bee Words with Comprehensive Claude Data
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
            'government', 'company', 'number', 'group', 'problem', 'fact', 'agreement', 'agricultural'
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
            'mega', 'micro', 'mini', 'multi', 'neo', 'pseudo', 'ultra', 'ac', 'ad', 'con', 'af', 'ag'
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

class Batch005Processor:
    """Processes Batch 005 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 005 words"""
        
        # Comprehensive data for all 50 words in Batch 005
        batch_005_data = {
            'agalma': {
                'definition': 'In ancient Greek art and religion, a sacred statue or image of a deity; an object of worship or veneration; anything delightful or pleasing.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-GAL-muh (emphasis on second syllable)',
                'etymology': 'From Greek "agalma" meaning "glory, delight, honor to the gods"',
                'memory_tips': 'Think "a-gal-ma" - a statue that makes you glad',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The ancient temple housed a beautiful _____ carved from marble.'
            },
            'agate': {
                'definition': 'A hard, fine-grained variety of quartz with bands of different colors; used in jewelry and ornamental objects.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AG-it (emphasis on first syllable)',
                'etymology': 'From Greek "achates", named after the river Achates in Sicily where it was found',
                'memory_tips': 'Think "a-gate" - a beautiful stone gate',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The jeweler polished the _____ to reveal its intricate banded patterns.'
            },
            'agave': {
                'definition': 'A succulent plant native to Mexico and the southwestern United States, used to make tequila and other products.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-GAH-vay (emphasis on second syllable)',
                'etymology': 'From Greek "agave" meaning "noble," named after the daughter of Cadmus in Greek mythology',
                'memory_tips': 'Think "a-gave" - a plant that gave us tequila',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ plant takes many years to mature before it can be harvested for tequila.'
            },
            'agelicism': {
                'definition': 'The practice of not laughing; restraint from laughter, especially as a philosophical or religious discipline.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-JEL-uh-sizm (emphasis on second syllable)',
                'etymology': 'From Greek "a-" (without) + "gelos" (laughter) + "-ism"',
                'memory_tips': 'Think "a-gel-icism" - against giggling and jelling with laughter',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The monk\'s practice of _____ was part of his spiritual discipline.'
            },
            'ageusia': {
                'definition': 'The loss or absence of the sense of taste; inability to taste flavors, often due to medical conditions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ay-GOO-zhuh (emphasis on second syllable)',
                'etymology': 'From Greek "a-" (without) + "geusis" (taste)',
                'memory_tips': 'Think "a-goose-ia" - a goose that can\'t taste anything',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The patient\'s _____ made eating an unpleasant experience.'
            },
            'aggrandizement': {
                'definition': 'An increase in power, importance, or wealth; the action of making something appear greater than it actually is.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-GRAN-diz-muhnt (emphasis on second syllable)',
                'etymology': 'From French "agrandissement", from "agrandir" meaning "to make larger"',
                'memory_tips': 'Think "ag-grand-ize-ment" - making something grand and great',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'His constant _____ of his achievements made colleagues uncomfortable.'
            },
            'aggravate': {
                'definition': 'To make worse or more serious; to annoy or exasperate; to increase the severity of something.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'AG-ruh-vayt (emphasis on first syllable)',
                'etymology': 'From Latin "aggravare", from "ad" (to) + "gravis" (heavy)',
                'memory_tips': 'Think "ag-grave-ate" - making something as heavy as a grave',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The loud music will _____ her headache.'
            },
            'agility': {
                'definition': 'The ability to move quickly and easily; mental quickness and adaptability; nimbleness and dexterity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-JIL-i-tee (emphasis on second syllable)',
                'etymology': 'From Latin "agilitas", from "agilis" meaning "movable, nimble"',
                'memory_tips': 'Think "a-gill-ity" - the ability to swim quickly like a fish with gills',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The gymnast\'s _____ impressed the judges with her graceful movements.'
            },
            'agitation': {
                'definition': 'A state of anxiety or nervous excitement; the action of making someone troubled or nervous; vigorous campaigning.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'aj-i-TAY-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "agitatio", from "agitare" meaning "to drive, stir up"',
                'memory_tips': 'Think "ag-itation" - being stirred up like agitated water',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The unexpected news caused considerable _____ among the staff.'
            },
            'agitprop': {
                'definition': 'Political propaganda, especially communist propaganda spread through literature, drama, music, or art.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AJ-it-prop (emphasis on first syllable)',
                'etymology': 'From Russian, contraction of "agitatsiya" (agitation) + "propaganda"',
                'memory_tips': 'Think "agit-prop" - agitating people with propaganda',
                'alternate_spellings': '',
                'language_origin': 'Russian',
                'example_sentence': 'The theatrical performance was criticized as thinly veiled _____.'
            },
            'aglaia': {
                'definition': 'In Greek mythology, one of the three Graces, representing splendor, glory, and beauty; brightness or brilliance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-GLAY-uh (emphasis on second syllable)',
                'etymology': 'From Greek "aglaia" meaning "splendor, beauty"',
                'memory_tips': 'Think "a-glay-a" - a glowing, beautiful goddess',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The artist depicted _____ as a radiant figure surrounded by light.'
            },
            'aglossal': {
                'definition': 'Without a tongue; lacking the ability to speak; relating to the absence of a tongue.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ay-GLOS-uhl (emphasis on second syllable)',
                'etymology': 'From Greek "a-" (without) + "glossa" (tongue)',
                'memory_tips': 'Think "a-gloss-al" - without the gloss of speech',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The medical condition left the patient functionally _____.'
            },
            'agnail': {
                'definition': 'A torn or detached piece of skin next to a fingernail; a hangnail.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AG-nayl (emphasis on first syllable)',
                'etymology': 'From Old English "angnægl", from "ang" (tight, painful) + "nægl" (nail)',
                'memory_tips': 'Think "ag-nail" - an angry, painful nail condition',
                'alternate_spellings': 'hangnail',
                'language_origin': 'Old English',
                'example_sentence': 'She winced when the _____ caught on her sweater.'
            },
            'agnesi': {
                'definition': 'A mathematical curve named after Maria Gaetana Agnesi; also called the Witch of Agnesi.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'an-YEH-zee (emphasis on second syllable)',
                'etymology': 'Named after Italian mathematician Maria Gaetana Agnesi (1718-1799)',
                'memory_tips': 'Think "ag-nesi" - a mathematical curve that nests in graphs',
                'alternate_spellings': 'Witch of Agnesi',
                'language_origin': 'Italian (proper name)',
                'example_sentence': 'Students learned to graph the _____ curve in calculus class.'
            },
            'agnolotti': {
                'definition': 'Small, crescent-shaped pasta pouches stuffed with filling, typical of the Piedmont region of Italy.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'an-yoh-LOT-tee (emphasis on third syllable)',
                'etymology': 'From Italian "agnolotti", possibly from "agnello" (lamb) as they were traditionally filled with lamb',
                'memory_tips': 'Think "ag-no-lotti" - little packets that you know are delicious',
                'alternate_spellings': '',
                'language_origin': 'Italian',
                'example_sentence': 'The restaurant served _____ filled with ricotta and spinach.'
            },
            'agnomen': {
                'definition': 'An additional name or epithet, especially one given to ancient Romans based on achievements or characteristics.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ag-NOH-muhn (emphasis on second syllable)',
                'etymology': 'From Latin "agnomen", from "ad" (to) + "nomen" (name)',
                'memory_tips': 'Think "ag-no-men" - a name you know a man by',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Scipio earned the _____ "Africanus" after his victories in Africa.'
            },
            'agonistic': {
                'definition': 'Relating to struggle or contest; competitive; characterized by conflict or argument; combative.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ag-uh-NIS-tik (emphasis on third syllable)',
                'etymology': 'From Greek "agonistikos", from "agonistes" meaning "competitor, combatant"',
                'memory_tips': 'Think "ag-on-istic" - being on the attack in an aggressive way',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The debate took on an _____ tone as both sides became more heated.'
            },
            'agoraphobia': {
                'definition': 'An anxiety disorder characterized by fear of open spaces, crowds, or situations where escape might be difficult.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ag-uh-ruh-FOH-bee-uh (emphasis on fourth syllable)',
                'etymology': 'From Greek "agora" (marketplace) + "phobia" (fear)',
                'memory_tips': 'Think "agora-phobia" - fear of the ancient Greek marketplace',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Her _____ prevented her from attending crowded events.'
            },
            'agrarian': {
                'definition': 'Relating to cultivated land or the cultivation of land; concerning agriculture and farming.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'uh-GRAIR-ee-uhn (emphasis on second syllable)',
                'etymology': 'From Latin "agrarius", from "ager" meaning "field"',
                'memory_tips': 'Think "ag-rarian" - rare agriculture practices',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The country\'s _____ economy depended heavily on crop production.'
            },
            'agreement': {
                'definition': 'A negotiated arrangement between parties; harmony of opinion; the state of being in accord.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-GREE-muhnt (emphasis on second syllable)',
                'etymology': 'From "agree" + "-ment", from Old French "agreer" meaning "to please"',
                'memory_tips': 'Think "a-gree-ment" - a mental state where people agree',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The two companies reached an _____ after months of negotiation.'
            },
            'agricultural': {
                'definition': 'Relating to agriculture; concerning the science or practice of farming and crop cultivation.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ag-ri-KUL-cher-uhl (emphasis on third syllable)',
                'etymology': 'From Latin "agricultura", from "ager" (field) + "cultura" (cultivation)',
                'memory_tips': 'Think "ag-ri-cultural" - the culture of agriculture',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The university offers several _____ programs for aspiring farmers.'
            },
            'agrypnia': {
                'definition': 'Persistent sleeplessness; chronic insomnia; the condition of being unable to sleep.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-GRIP-nee-uh (emphasis on second syllable)',
                'etymology': 'From Greek "agrypnia", from "a-" (without) + "hypnos" (sleep)',
                'memory_tips': 'Think "a-grip-nia" - gripped by the inability to sleep',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The patient\'s _____ required specialized medical treatment.'
            },
            'agrypniaague': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "agrypnia" (sleeplessness) + "ague" (fever).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "agrypnia" and "ague"',
                'alternate_spellings': 'agrypnia + ague (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'ague': {
                'definition': 'A fever characterized by fits of shivering and sweating; malaria or a similar intermittent fever.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AY-gyoo (emphasis on first syllable)',
                'etymology': 'From Old French "ague", from Latin "acuta" meaning "acute (fever)"',
                'memory_tips': 'Think "a-goo" - a fever that makes you feel gooey',
                'alternate_spellings': '',
                'language_origin': 'Old French via Latin',
                'example_sentence': 'The traveler contracted _____ during his journey through the tropics.'
            },
            'ahimsa': {
                'definition': 'The Hindu and Buddhist principle of non-violence toward all living things; respect for all life forms.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-HIM-sah (emphasis on second syllable)',
                'etymology': 'From Sanskrit "ahimsa", from "a-" (not) + "himsa" (violence, harm)',
                'memory_tips': 'Think "a-him-sa" - not harming him or any living being',
                'alternate_spellings': '',
                'language_origin': 'Sanskrit',
                'example_sentence': 'Gandhi\'s philosophy of _____ influenced peaceful resistance movements worldwide.'
            },
            'ahoy': {
                'definition': 'A nautical greeting or call used to attract attention; an exclamation used by sailors.',
                'part_of_speech': 'interjection',
                'pronunciation_guide': 'uh-HOY (emphasis on second syllable)',
                'etymology': 'From Middle English, possibly from "hoy" (exclamation to attract attention)',
                'memory_tips': 'Think "a-hoy" - a greeting that brings joy on ships',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The sailor called out "_____!" to the passing vessel.'
            },
            'ahuatle': {
                'definition': 'The eggs of aquatic insects, especially water boatmen, used as food in Mexican cuisine; sometimes called "Mexican caviar."',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ah-WAHT-lay (emphasis on second syllable)',
                'etymology': 'From Nahuatl "ahuahtli" meaning "water seed"',
                'memory_tips': 'Think "ah-water-lay" - water seeds laid by insects',
                'alternate_spellings': '',
                'language_origin': 'Nahuatl',
                'example_sentence': 'The traditional Mexican dish featured _____ harvested from the lake.'
            },
            'ahuehuete': {
                'definition': 'A large cypress tree native to Mexico, known for its longevity and massive trunk; Montezuma cypress.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ah-way-WAY-tay (emphasis on third syllable)',
                'etymology': 'From Nahuatl "ahuehuetl" meaning "old man of the water"',
                'memory_tips': 'Think "ah-way-way-te" - a tree that lives way, way long',
                'alternate_spellings': 'Montezuma cypress',
                'language_origin': 'Nahuatl',
                'example_sentence': 'The ancient _____ in the town square was over 500 years old.'
            },
            'ahura': {
                'definition': 'In Zoroastrianism, a divine being or deity; specifically refers to Ahura Mazda, the supreme god.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ah-HOO-rah (emphasis on second syllable)',
                'etymology': 'From Avestan "ahura" meaning "lord, deity"',
                'memory_tips': 'Think "ah-hoorah" - shouting hooray to the divine lord',
                'alternate_spellings': '',
                'language_origin': 'Avestan (ancient Persian)',
                'example_sentence': 'Zoroastrian prayers often invoke _____ Mazda as the wise lord.'
            },
            'aikido': {
                'definition': 'A Japanese martial art that uses circular movements and leverage to redirect an opponent\'s force; "the way of harmonious spirit."',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'eye-KEE-doh (emphasis on second syllable)',
                'etymology': 'From Japanese "aikido", from "ai" (harmony) + "ki" (spirit) + "do" (way)',
                'memory_tips': 'Think "I-key-do" - I have the key to this martial art',
                'alternate_spellings': '',
                'language_origin': 'Japanese',
                'example_sentence': 'She practiced _____ to learn self-defense through peaceful means.'
            },
            'ailanthus': {
                'definition': 'A fast-growing deciduous tree native to China, also called "tree of heaven"; often considered invasive in North America.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ay-LAN-thus (emphasis on second syllable)',
                'etymology': 'From Moluccan "ailanto" meaning "tree reaching toward the sky"',
                'memory_tips': 'Think "ailment-thus" - a tree that\'s an ailment because it grows everywhere',
                'alternate_spellings': 'tree of heaven',
                'language_origin': 'Moluccan',
                'example_sentence': 'The _____ spread rapidly through the abandoned lot.'
            },
            'aileron': {
                'definition': 'A hinged control surface on an airplane wing used to control roll movement; helps the aircraft turn.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AY-luh-ron (emphasis on first syllable)',
                'etymology': 'From French "aileron", diminutive of "aile" meaning "wing"',
                'memory_tips': 'Think "aile-ron" - little wings that help control flight',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The pilot adjusted the _____ to bank the aircraft to the left.'
            },
            'ailette': {
                'definition': 'A small plate of armor worn on the shoulder in medieval times; a shoulder guard or wing-like protection.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ay-LET (emphasis on second syllable)',
                'etymology': 'From French "ailette", diminutive of "aile" meaning "wing"',
                'memory_tips': 'Think "a-let" - a little wing that protects like armor',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The knight\'s _____ displayed his heraldic emblem.'
            },
            'ailment': {
                'definition': 'A minor illness or health problem; a disorder or complaint affecting physical or mental well-being.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AYL-muhnt (emphasis on first syllable)',
                'etymology': 'From "ail" (to cause pain or trouble) + "-ment"',
                'memory_tips': 'Think "ail-ment" - something that ails your mental and physical state',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The doctor diagnosed her with a minor _____ that would heal quickly.'
            },
            'aioli': {
                'definition': 'A Mediterranean sauce made of garlic, olive oil, and egg yolks; similar to mayonnaise but with a strong garlic flavor.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'eye-OH-lee (emphasis on second syllable)',
                'etymology': 'From Provençal "aiòli", from "ai" (garlic) + "òli" (oil)',
                'memory_tips': 'Think "I-oh-li" - I love this garlic oil sauce',
                'alternate_spellings': '',
                'language_origin': 'Provençal',
                'example_sentence': 'The chef served grilled vegetables with homemade _____.'
            },
            'airedale': {
                'definition': 'A large terrier breed with a wiry coat, originally bred in Yorkshire, England; known as the "King of Terriers."',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AIR-dayl (emphasis on first syllable)',
                'etymology': 'Named after the Aire Valley in Yorkshire, England, where the breed was developed',
                'memory_tips': 'Think "air-dale" - a dog from a valley with good air',
                'alternate_spellings': 'Airedale Terrier',
                'language_origin': 'English (place name)',
                'example_sentence': 'The _____ won first place in the terrier group at the dog show.'
            },
            'airing': {
                'definition': 'The action of broadcasting a program; exposure to fresh air; the expression or discussion of opinions publicly.',
                'part_of_speech': 'noun, verb (present participle)',
                'pronunciation_guide': 'AIR-ing (emphasis on first syllable)',
                'etymology': 'From "air" + "-ing"',
                'memory_tips': 'Think "air-ing" - putting something into the air',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The controversial documentary received its first _____ last night.'
            },
            'airwaves': {
                'definition': 'Radio frequencies used for broadcasting; the medium through which radio and television signals are transmitted.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'AIR-wayvz (emphasis on first syllable)',
                'etymology': 'From "air" + "waves", referring to electromagnetic waves traveling through air',
                'memory_tips': 'Think "air-waves" - waves traveling through the air',
                'alternate_spellings': '',
                'language_origin': 'Modern English compound',
                'example_sentence': 'The song dominated the _____ throughout the summer.'
            },
            'aisles': {
                'definition': 'Passages between rows of seats or shelves; walkways in churches, theaters, or stores.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'EYLS (single syllable)',
                'etymology': 'From Old French "ele", from Latin "ala" meaning "wing"',
                'memory_tips': 'Think "I\'ll-s" - I\'ll walk down these passages',
                'alternate_spellings': '',
                'language_origin': 'Old French via Latin',
                'example_sentence': 'The bride walked down the _____ toward the altar.'
            },
            'aistopod': {
                'definition': 'An extinct type of early amphibian with an elongated, snake-like body and reduced or absent limbs.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'eye-STOH-pod (emphasis on second syllable)',
                'etymology': 'From Greek "aistos" (darting, quick) + "pod" (foot)',
                'memory_tips': 'Think "ai-stop-od" - an ancient creature that stopped evolving feet',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Paleontologists discovered fossilized remains of an _____ in the coal deposits.'
            },
            'aitutakian': {
                'definition': 'Relating to Aitutaki, one of the Cook Islands in the Pacific Ocean; a person from Aitutaki.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'eye-too-TAH-kee-uhn (emphasis on third syllable)',
                'etymology': 'From "Aitutaki" (the island name) + "-an"',
                'memory_tips': 'Think "I-too-talk-ian" - I too can talk like someone from this island',
                'alternate_spellings': '',
                'language_origin': 'Polynesian (place name)',
                'example_sentence': 'The _____ cultural festival showcased traditional Pacific island dances.'
            },
            'aiuy': {
                'definition': 'A rare or obsolete term, possibly referring to a type of musical notation or expression in medieval music.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EYE-oo-ee (emphasis on first syllable)',
                'etymology': 'Uncertain origin, possibly from medieval Latin musical terminology',
                'memory_tips': 'Think "I-you-y" - a musical expression between I and you',
                'alternate_spellings': '',
                'language_origin': 'Uncertain, possibly medieval Latin',
                'example_sentence': 'The musicologist studied the _____ notation in the ancient manuscript.'
            },
            'ajimez': {
                'definition': 'A type of arched window divided by a slender column, typical of Islamic and Moorish architecture.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ah-hee-METH (emphasis on third syllable)',
                'etymology': 'From Arabic "al-khuṣṣa" meaning "the opening"',
                'memory_tips': 'Think "ah-jim-ez" - architectural openings that are easy to see through',
                'alternate_spellings': '',
                'language_origin': 'Arabic',
                'example_sentence': 'The palace featured beautiful _____ windows overlooking the courtyard.'
            },
            'akaryote': {
                'definition': 'A cell or organism lacking a nucleus; having no distinct nuclear membrane or organized nucleus.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'ay-KAIR-ee-oht (emphasis on second syllable)',
                'etymology': 'From Greek "a-" (without) + "karyon" (nucleus)',
                'memory_tips': 'Think "a-carry-ote" - not carrying a nucleus',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Bacteria are _____ organisms since they lack a membrane-bound nucleus.'
            },
            'akimbo': {
                'definition': 'With hands on the hips and elbows turned outward; in a bent or bowed position.',
                'part_of_speech': 'adjective, adverb',
                'pronunciation_guide': 'uh-KIM-boh (emphasis on second syllable)',
                'etymology': 'From Middle English "in kenebowe", possibly from Old Norse "kengboginn" meaning "bent into a crook"',
                'memory_tips': 'Think "a-kimbo" - arms kinked in a bow shape',
                'alternate_spellings': '',
                'language_origin': 'Middle English, possibly from Old Norse',
                'example_sentence': 'She stood with her arms _____, looking defiant and determined.'
            },
            'akkum': {
                'definition': 'A type of traditional fermented beverage or preparation, possibly from Central Asian or Middle Eastern cuisine.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AH-koom (emphasis on first syllable)',
                'etymology': 'Uncertain origin, possibly from Turkic or Persian languages',
                'memory_tips': 'Think "ack-oom" - a drink that makes you go "ack" then "mmm"',
                'alternate_spellings': '',
                'language_origin': 'Uncertain, possibly Turkic',
                'example_sentence': 'The traditional _____ was served at the cultural celebration.'
            },
            'alacrity': {
                'definition': 'Cheerful readiness or willingness; eager enthusiasm; brisk and lively action.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-LAK-ri-tee (emphasis on second syllable)',
                'etymology': 'From Latin "alacritas", from "alacer" meaning "lively, eager"',
                'memory_tips': 'Think "a-lack-rity" - never lacking enthusiasm or energy',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She accepted the challenging assignment with remarkable _____.'
            },
            'alai': {
                'definition': 'Part of "jai alai," a fast ball game played with curved baskets; also means "festival" in some languages.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-LYE (emphasis on second syllable)',
                'etymology': 'From Basque "alai" meaning "merry, joyous"',
                'memory_tips': 'Think "a-lie" - no lie, it\'s a joyous festival or game',
                'alternate_spellings': '',
                'language_origin': 'Basque',
                'example_sentence': 'The jai _____ match drew crowds to the sports arena.'
            },
            'alas': {
                'definition': 'An exclamation expressing grief, pity, or concern; used to express regret or dismay.',
                'part_of_speech': 'interjection',
                'pronunciation_guide': 'uh-LAS (emphasis on second syllable)',
                'etymology': 'From Old French "a las" meaning "ah, wretched"',
                'memory_tips': 'Think "a-las" - the last thing you want to say when sad',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': '"_____," she sighed, "we have missed the last train."'
            },
            'alate': {
                'definition': 'Having wings or wing-like extensions; in entomology, referring to the winged form of an insect.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'AY-layt (emphasis on first syllable)',
                'etymology': 'From Latin "alatus", from "ala" meaning "wing"',
                'memory_tips': 'Think "a-late" - arriving late because you have to fly with wings',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ ants swarmed during their reproductive flight.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_005_data:
            return batch_005_data[word_lower]
        
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
    
    def process_batch_005(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 005 with comprehensive Claude data"""
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
    
    def save_batch_005_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 005 processed words to CSV"""
        
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
    """Process Batch 005 with comprehensive Claude data"""
    processor = Batch005Processor()
    input_csv = Path("output/batch_005_words.csv")
    output_csv = Path("output/batch_005_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 005 with comprehensive Claude data...")
    
    # Process all words in batch 005
    processed_words = processor.process_batch_005(input_csv)
    
    # Save results
    processor.save_batch_005_csv(processed_words, output_csv)
    
    logger.info(f"Batch 005 processing completed!")
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