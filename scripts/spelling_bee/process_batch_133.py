#!/usr/bin/env python3
"""
Process Batch 133 of Spelling Bee Words with Comprehensive Claude Data
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
        # This is a subset of common words for frequency analysis
        common = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
            'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him',
            'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only',
            'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want',
            'because', 'any', 'these', 'give', 'day', 'most', 'us', 'is', 'water', 'long', 'find', 'here', 'thing', 'great', 'man', 'world', 'life',
            'still', 'public', 'human', 'get', 'old', 'country', 'hand', 'part', 'child', 'eye', 'woman', 'place', 'work', 'week', 'case', 'point',
            'government', 'company', 'number', 'group', 'problem', 'fact', 'pick', 'picture', 'piece', 'phone', 'physical', 'pink', 'place', 'plan'
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
            'mega', 'micro', 'mini', 'multi', 'neo', 'pseudo', 'ultra', 'photo', 'phys', 'pla'
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

class Batch133Processor:
    """Processes Batch 133 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 133 words"""
        
        # Comprehensive data for all 50 words in Batch 133
        batch_133_data = {
            'piloncillo': {
                'definition': 'An unrefined brown sugar commonly used in Mexican and Latin American cooking, formed into cone or cylindrical shapes; also called panela.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pee-lon-SEE-yoh (emphasis on third syllable)',
                'etymology': 'From Spanish "piloncillo", diminutive of "pilón" meaning "cone"',
                'memory_tips': 'Think "pile-on-see-yo" - pile on this sweet cone you can see',
                'alternate_spellings': 'panela, brown sugar cone',
                'language_origin': 'Spanish',
                'example_sentence': 'The traditional recipe called for _____ to sweeten the mole sauce.'
            },
            'pilosity': {
                'definition': 'The state or condition of being hairy or covered with soft hair; hairiness, especially abnormal or excessive hair growth.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'py-LOS-uh-tee (emphasis on second syllable)',
                'etymology': 'From Latin "pilosus" meaning "hairy" + "-ity" suffix',
                'memory_tips': 'Think "pilot-city" - a city where all the pilots are very hairy',
                'alternate_spellings': 'hairiness, hirsutism',
                'language_origin': 'Latin',
                'example_sentence': 'The patient showed signs of _____ as a side effect of the medication.'
            },
            'pilotage': {
                'definition': 'The act of piloting a ship or aircraft; navigation services provided by a pilot; the fee paid for piloting services.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PY-luh-tij (emphasis on first syllable)',
                'etymology': 'From French "pilotage", from "pilote" meaning "pilot"',
                'memory_tips': 'Think "pilot-age" - the age when you learn to pilot',
                'alternate_spellings': 'navigation, piloting',
                'language_origin': 'French',
                'example_sentence': 'The harbor required experienced _____ to safely guide large vessels through the narrow channel.'
            },
            'piminy': {
                'definition': 'Affectedly proper, prim, or precise in speech and manner; overly formal or delicate in behavior.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'PIM-uh-nee (emphasis on first syllable)',
                'etymology': 'Possibly from "prim" + "mini", suggesting small or delicate primness',
                'memory_tips': 'Think "prim-mini" - so prim and proper in a mini way',
                'alternate_spellings': 'prim, proper, affected',
                'language_origin': 'English (possibly compound)',
                'example_sentence': 'Her _____ manner of speaking made her seem uptight and formal.'
            },
            'pineapple': {
                'definition': 'A large tropical fruit with a tough, spiky exterior and sweet, juicy flesh; the plant that produces this fruit.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PY-nap-uhl (emphasis on first syllable)',
                'etymology': 'From "pine" (for its appearance) + "apple" (for its fruit nature)',
                'memory_tips': 'Think "pine-apple" - looks like a pine cone but tastes like fruit',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The sweet _____ was the perfect addition to the tropical fruit salad.'
            },
            'pinetum': {
                'definition': 'A botanical garden or arboretum dedicated to growing different species of pine and coniferous trees.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'py-NEE-tum (emphasis on second syllable)',
                'etymology': 'From Latin "pinetum", from "pinus" meaning "pine tree"',
                'memory_tips': 'Think "pine-tum" - your tummy feels good walking through pine trees',
                'alternate_spellings': 'conifer garden',
                'language_origin': 'Latin',
                'example_sentence': 'The university\'s _____ contained over 200 species of coniferous trees.'
            },
            'pinioned': {
                'definition': 'Having wings or arms bound; restrained by binding the wings or arms; confined or restricted in movement.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'PIN-yuhnd (emphasis on first syllable)',
                'etymology': 'From "pinion" meaning "wing tip" or "to bind", from Latin "penna" meaning "feather"',
                'memory_tips': 'Think "pin-yawned" - pinned down so tightly you yawned from boredom',
                'alternate_spellings': 'bound, restrained',
                'language_origin': 'Latin',
                'example_sentence': 'The bird was _____ and could not fly away from its captors.'
            },
            'pink': {
                'definition': 'A pale red color; a flowering plant with fragrant, often pink flowers; in perfect condition.',
                'part_of_speech': 'noun, adjective, verb',
                'pronunciation_guide': 'PINGK (emphasis on syllable)',
                'etymology': 'From Dutch "pinck" meaning "small" or from the flower name',
                'memory_tips': 'Think "p-ink" - pink ink used for writing',
                'alternate_spellings': 'rose-colored',
                'language_origin': 'Dutch',
                'example_sentence': 'She wore a beautiful _____ dress to the garden party.'
            },
            'pinkerton': {
                'definition': 'A detective or private investigator, especially one employed by the Pinkerton Detective Agency; relating to private security services.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PING-kur-tuhn (emphasis on first syllable)',
                'etymology': 'From Allan Pinkerton, founder of the Pinkerton Detective Agency in 1850',
                'memory_tips': 'Think "pink-erton" - a pink detective who turns criminals',
                'alternate_spellings': 'private detective',
                'language_origin': 'American English (proper name)',
                'example_sentence': 'The company hired a _____ to investigate the theft of industrial secrets.'
            },
            'pinnacle': {
                'definition': 'The highest point or peak of something; the most successful point of a career or achievement; a tall, pointed rock formation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PIN-uh-kuhl (emphasis on first syllable)',
                'etymology': 'From Latin "pinnaculum", diminutive of "pinna" meaning "feather, wing"',
                'memory_tips': 'Think "pin-a-call" - pin a call to the highest point',
                'alternate_spellings': 'peak, summit, apex',
                'language_origin': 'Latin',
                'example_sentence': 'Winning the championship was the _____ of her athletic career.'
            },
            'pinnate': {
                'definition': 'Having leaflets arranged on either side of a common stem, resembling a feather; feather-like in structure.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'PIN-ayt (emphasis on first syllable)',
                'etymology': 'From Latin "pinnatus" meaning "feathered", from "pinna" meaning "feather"',
                'memory_tips': 'Think "pin-ate" - leaves arranged like pins that ate the stem',
                'alternate_spellings': 'feather-like',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ leaves of the ash tree create beautiful symmetrical patterns.'
            },
            'pinniped': {
                'definition': 'A carnivorous marine mammal with flippers, including seals, sea lions, and walruses.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PIN-uh-ped (emphasis on first syllable)',
                'etymology': 'From Latin "pinna" meaning "fin" + "pes" meaning "foot"',
                'memory_tips': 'Think "pin-uh-ped" - animals with fins for feet',
                'alternate_spellings': 'seal-like mammal',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ used its powerful flippers to navigate through the icy waters.'
            },
            'pinpoint': {
                'definition': 'To locate or identify precisely; extremely small or precise; a very small point or area.',
                'part_of_speech': 'verb, adjective, noun',
                'pronunciation_guide': 'PIN-point (emphasis on first syllable)',
                'etymology': 'From "pin" + "point", referring to the sharp tip of a pin',
                'memory_tips': 'Think "pin-point" - as precise as the point of a pin',
                'alternate_spellings': 'identify precisely',
                'language_origin': 'English',
                'example_sentence': 'The detective was able to _____ the exact time of the crime.'
            },
            'pinyin': {
                'definition': 'The official romanization system for Standard Chinese, using Latin letters to represent Chinese pronunciation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PIN-yin (emphasis on first syllable)',
                'etymology': 'From Chinese "pinyin" meaning "spelled sound"',
                'memory_tips': 'Think "pin-yin" - pinning down the yin (sound) of Chinese words',
                'alternate_spellings': 'Chinese romanization',
                'language_origin': 'Chinese',
                'example_sentence': 'Students learning Mandarin often start with _____ before learning Chinese characters.'
            },
            'pinyondysfunctional': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "pinyon" (type of pine tree) + "dysfunctional" (not working properly).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "pinyon" and "dysfunctional"',
                'alternate_spellings': 'pinyon + dysfunctional (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'pioneered': {
                'definition': 'Developed or introduced something new; led the way in exploring or developing new areas of knowledge or activity.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'py-uh-NEERD (emphasis on third syllable)',
                'etymology': 'From "pioneer", from French "pionnier" meaning "foot soldier, digger"',
                'memory_tips': 'Think "pie-on-eared" - pioneers who had pie on their ears from hard work',
                'alternate_spellings': 'developed, initiated',
                'language_origin': 'French',
                'example_sentence': 'She _____ the use of computer technology in medical diagnosis.'
            },
            'pious': {
                'definition': 'Devoutly religious; showing reverence for religious beliefs; earnestly compliant in the observance of religion.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'PY-us (emphasis on first syllable)',
                'etymology': 'From Latin "pius" meaning "dutiful, devout"',
                'memory_tips': 'Think "pie-us" - sharing pie with us in a religious way',
                'alternate_spellings': 'devout, religious',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ monk spent hours each day in prayer and meditation.'
            },
            'piousadjective': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "pious" (devoutly religious) + "adjective" (grammar term).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "pious" and "adjective"',
                'alternate_spellings': 'pious + adjective (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'piperhear': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "piper" (one who plays pipes) + "hear" (to perceive sound).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "piper" and "hear"',
                'alternate_spellings': 'piper + hear (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'pipet': {
                'definition': 'A variant spelling of pipette; a laboratory instrument used to measure and transfer small volumes of liquid.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'py-PET (emphasis on second syllable)',
                'etymology': 'From French "pipette", diminutive of "pipe"',
                'memory_tips': 'Think "pipe-et" - a small pipe for measuring liquids',
                'alternate_spellings': 'pipette',
                'language_origin': 'French',
                'example_sentence': 'The scientist used a _____ to carefully measure the chemical solution.'
            },
            'pipette': {
                'definition': 'A laboratory instrument used to measure and transfer small, precise volumes of liquid.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'py-PET (emphasis on second syllable)',
                'etymology': 'From French "pipette", diminutive of "pipe" meaning "tube"',
                'memory_tips': 'Think "pipe-ette" - a little pipe for precise liquid transfer',
                'alternate_spellings': 'pipet',
                'language_origin': 'French',
                'example_sentence': 'She used a _____ to add exactly 10 microliters of the reagent.'
            },
            'piraeus': {
                'definition': 'The port city of Athens, Greece; the largest passenger port in Europe and one of the most important in the Mediterranean.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'py-REE-us (emphasis on second syllable)',
                'etymology': 'From ancient Greek "Peiraieus", possibly meaning "the place of crossing over"',
                'memory_tips': 'Think "pier-ee-us" - the pier where Greeks meet us',
                'alternate_spellings': 'Peiraieus (Greek)',
                'language_origin': 'Ancient Greek',
                'example_sentence': 'The ferry from the islands arrived at the busy port of _____.'
            },
            'piratical': {
                'definition': 'Relating to or characteristic of pirates; involving robbery or illegal violence at sea; predatory or plundering.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'py-RAT-uh-kuhl (emphasis on second syllable)',
                'etymology': 'From "pirate" + "-ical", from Latin "pirata" meaning "sea robber"',
                'memory_tips': 'Think "pie-rat-ical" - rats eating pie in a pirate-like manner',
                'alternate_spellings': 'pirate-like, predatory',
                'language_origin': 'Latin',
                'example_sentence': 'The ship was attacked by _____ raiders who stole all the cargo.'
            },
            'pirouetted': {
                'definition': 'Performed a pirouette; spun around on one foot in ballet; rotated or turned quickly.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'pir-oo-ET-id (emphasis on third syllable)',
                'etymology': 'From French "pirouette" meaning "spinning top"',
                'memory_tips': 'Think "peer-whet-ted" - peers who got whetted (excited) watching the spin',
                'alternate_spellings': 'spun, rotated',
                'language_origin': 'French',
                'example_sentence': 'The ballerina _____ gracefully across the stage.'
            },
            'pisces': {
                'definition': 'The twelfth sign of the zodiac, represented by two fish; people born under this sign (February 19 - March 20).',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'PY-seez (emphasis on first syllable)',
                'etymology': 'From Latin "pisces" meaning "fishes", plural of "piscis"',
                'memory_tips': 'Think "pie-seas" - fish swimming in seas shaped like pies',
                'alternate_spellings': 'Fishes (zodiac)',
                'language_origin': 'Latin',
                'example_sentence': 'As a _____, she was known for her intuitive and compassionate nature.'
            },
            'piscivorous': {
                'definition': 'Fish-eating; feeding primarily on fish; having a diet that consists mainly of fish.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'pis-SIV-uh-rus (emphasis on second syllable)',
                'etymology': 'From Latin "piscis" meaning "fish" + "vorare" meaning "to devour"',
                'memory_tips': 'Think "piss-see-vore-us" - animals that voraciously eat fish',
                'alternate_spellings': 'fish-eating',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ bird caught several fish during its morning hunt.'
            },
            'pisin': {
                'definition': 'A creole language based on English, spoken in Papua New Guinea; also refers to pidgin languages in general.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PEE-sin (emphasis on first syllable)',
                'etymology': 'From "pidgin", possibly from Chinese pronunciation of "business"',
                'memory_tips': 'Think "pea-sin" - simple language like counting peas without sin',
                'alternate_spellings': 'pidgin, creole',
                'language_origin': 'English pidgin',
                'example_sentence': 'The locals communicated in _____, which combined English with indigenous languages.'
            },
            'pissaladière': {
                'definition': 'A traditional French tart from Nice, typically topped with onions, anchovies, and olives on a bread-like base.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pee-sah-lah-dee-YAIR (emphasis on last syllable)',
                'etymology': 'From Provençal "pissaladiera", from "pissala" (anchovy paste) + "-ière"',
                'memory_tips': 'Think "pizza-ladyear" - a French pizza-like dish for ladies to eat',
                'alternate_spellings': 'French onion tart',
                'language_origin': 'Provençal French',
                'example_sentence': 'The café served traditional _____ with caramelized onions and black olives.'
            },
            'pistons': {
                'definition': 'Moving parts in engines that transfer force from expanding gas to the crankshaft; sliding pieces in cylinders.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'PIS-tuhnz (emphasis on first syllable)',
                'etymology': 'From French "piston", from Italian "pistone" meaning "large pestle"',
                'memory_tips': 'Think "piss-tons" - heavy parts that move up and down like tons of weight',
                'alternate_spellings': 'piston (singular)',
                'language_origin': 'French via Italian',
                'example_sentence': 'The mechanic replaced all four _____ to improve the engine\'s performance.'
            },
            'pistou': {
                'definition': 'A French sauce similar to pesto, made from basil, garlic, and olive oil, often served with vegetables or soup.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pee-STOO (emphasis on second syllable)',
                'etymology': 'From Provençal "pistou", from "pistar" meaning "to pound"',
                'memory_tips': 'Think "pea-stew" - a green sauce that goes well with pea stew',
                'alternate_spellings': 'French pesto',
                'language_origin': 'Provençal French',
                'example_sentence': 'The soup was garnished with a dollop of fresh _____.'
            },
            'pitanga': {
                'definition': 'A tropical fruit from South America, also known as Surinam cherry, with a distinctive ribbed shape and sweet-tart flavor.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pee-TAHN-gah (emphasis on second syllable)',
                'etymology': 'From Tupi (Brazilian indigenous language) "pitanga"',
                'memory_tips': 'Think "pee-tango" - a fruit so good it makes you dance the tango',
                'alternate_spellings': 'Surinam cherry',
                'language_origin': 'Tupi (Brazilian indigenous)',
                'example_sentence': 'The _____ tree in the garden produced bright red, ribbed fruits.'
            },
            'pitch': {
                'definition': 'The highness or lowness of a sound; to throw or toss; a sticky, dark substance; to set up or erect.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'PICH (emphasis on syllable)',
                'etymology': 'From Old English "pic" meaning "pointed object" or from Latin "pix" meaning "tar"',
                'memory_tips': 'Think "pitch" - throwing a ball or the pitch of your voice',
                'alternate_spellings': 'throw, tone, tar',
                'language_origin': 'Old English/Latin',
                'example_sentence': 'The singer could reach an incredibly high _____ with her voice.'
            },
            'pitiful': {
                'definition': 'Deserving or arousing pity; pathetically small or inadequate; contemptibly poor in quality.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'PIT-uh-fuhl (emphasis on first syllable)',
                'etymology': 'From "pity" + "-ful", from Latin "pietas" meaning "compassion"',
                'memory_tips': 'Think "pit-full" - so sad it fills you with pity like a deep pit',
                'alternate_spellings': 'pathetic, wretched',
                'language_origin': 'Latin via English',
                'example_sentence': 'The abandoned puppy looked _____ shivering in the rain.'
            },
            'pituitary': {
                'definition': 'A small endocrine gland at the base of the brain that produces hormones regulating growth and other bodily functions.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'pi-TOO-uh-ter-ee (emphasis on second syllable)',
                'etymology': 'From Latin "pituitarius" meaning "secreting phlegm"',
                'memory_tips': 'Think "pit-you-terry" - a pit in your head where Terry (the gland) lives',
                'alternate_spellings': 'hypophysis',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ gland is often called the "master gland" of the endocrine system.'
            },
            'pivot': {
                'definition': 'A central point on which something turns or balances; to turn on a central point; to change direction or approach.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'PIV-ut (emphasis on first syllable)',
                'etymology': 'From French "pivot", possibly from Provençal "pivo" meaning "peg"',
                'memory_tips': 'Think "give-it" - give it a turn around the central point',
                'alternate_spellings': 'fulcrum, turn',
                'language_origin': 'French',
                'example_sentence': 'The basketball player used his left foot as a _____ to spin around the defender.'
            },
            'pixels': {
                'definition': 'The smallest elements of a digital image; individual points of light that make up a digital display.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'PIK-suhls (emphasis on first syllable)',
                'etymology': 'From "picture" + "element", coined in the 1960s for computer graphics',
                'memory_tips': 'Think "pick-sells" - you pick and sell tiny picture elements',
                'alternate_spellings': 'pixel (singular), picture elements',
                'language_origin': 'Modern English (technical)',
                'example_sentence': 'The high-resolution monitor displayed millions of _____ to create sharp images.'
            },
            'piñon': {
                'definition': 'A small pine tree found in the southwestern United States and Mexico, producing edible nuts; the nuts themselves.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PEEN-yon (emphasis on first syllable)',
                'etymology': 'From Spanish "piñón", from "piña" meaning "pine cone"',
                'memory_tips': 'Think "peen-yon" - yon (over there) are pine trees with edible nuts',
                'alternate_spellings': 'pinyon, pine nut',
                'language_origin': 'Spanish',
                'example_sentence': 'The indigenous people harvested _____ nuts as an important food source.'
            },
            'placards': {
                'definition': 'Signs or notices displayed publicly, often carried in demonstrations or posted for advertisement or information.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'PLAK-ardz (emphasis on first syllable)',
                'etymology': 'From French "placard", from "plaquer" meaning "to stick on"',
                'memory_tips': 'Think "plaque-cards" - cards that stick like plaque on teeth',
                'alternate_spellings': 'placard (singular), signs',
                'language_origin': 'French',
                'example_sentence': 'The protesters carried _____ demanding better working conditions.'
            },
            'placate': {
                'definition': 'To make someone less angry or hostile; to calm or soothe someone who is upset or agitated.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'PLAY-kayt (emphasis on first syllable)',
                'etymology': 'From Latin "placare" meaning "to appease, calm"',
                'memory_tips': 'Think "place-ate" - place food to calm someone who ate too little',
                'alternate_spellings': 'appease, calm, soothe',
                'language_origin': 'Latin',
                'example_sentence': 'The manager tried to _____ the angry customers with free vouchers.'
            },
            'place': {
                'definition': 'A particular position, point, or area in space; a location; to put something in a specific position.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'PLAYS (emphasis on syllable)',
                'etymology': 'From Latin "platea" meaning "broad street, courtyard"',
                'memory_tips': 'Think "place" - where you place things or a place to be',
                'alternate_spellings': 'location, position',
                'language_origin': 'Latin',
                'example_sentence': 'She found the perfect _____ to build her new home.'
            },
            'placed': {
                'definition': 'Put in a particular position; positioned or located; finished in a specific rank in a competition.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'PLAYST (emphasis on syllable)',
                'etymology': 'Past tense of "place", from Latin "platea"',
                'memory_tips': 'Think "play-st" - past tense of placing something in play',
                'alternate_spellings': 'positioned, located',
                'language_origin': 'Latin',
                'example_sentence': 'She _____ the vase carefully on the shelf.'
            },
            'placoderm': {
                'definition': 'An extinct class of armored prehistoric fish that lived during the Devonian period, characterized by bony plates covering the head and neck.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLAK-oh-durm (emphasis on first syllable)',
                'etymology': 'From Greek "plax" meaning "plate" + "derma" meaning "skin"',
                'memory_tips': 'Think "plaque-derm" - ancient fish with plaque-like skin plates',
                'alternate_spellings': 'armored fish',
                'language_origin': 'Greek',
                'example_sentence': 'The fossil _____ showed the distinctive bony armor that protected these ancient fish.'
            },
            'placque': {
                'definition': '[POSSIBLE MISSPELLING] This may be an incorrect spelling of "plaque" (dental buildup or commemorative tablet).',
                'part_of_speech': 'noun (uncertain spelling)',
                'pronunciation_guide': 'PLAK (if meant as "plaque")',
                'etymology': 'Uncertain - possibly variant of "plaque" from French',
                'memory_tips': 'May be an error - check if this should be "plaque"',
                'alternate_spellings': 'plaque (?)',
                'language_origin': 'Uncertain',
                'example_sentence': '[NEEDS CLARIFICATION] The dentist removed the _____ from the patient\'s teeth.'
            },
            'plagiarism': {
                'definition': 'The practice of using someone else\'s work or ideas without proper acknowledgment; copying another\'s work and presenting it as one\'s own.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLAY-juh-riz-uhm (emphasis on first syllable)',
                'etymology': 'From Latin "plagiarius" meaning "kidnapper, literary thief"',
                'memory_tips': 'Think "play-jury-ism" - a jury would play (judge) this as theft',
                'alternate_spellings': 'copying, intellectual theft',
                'language_origin': 'Latin',
                'example_sentence': 'The student was expelled for committing _____ in his research paper.'
            },
            'plague': {
                'definition': 'A contagious bacterial disease; any widespread affliction or calamity; to trouble or torment persistently.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'PLAYG (emphasis on syllable)',
                'etymology': 'From Latin "plaga" meaning "blow, wound"',
                'memory_tips': 'Think "play-g" - a game where G (germs) spread disease',
                'alternate_spellings': 'pestilence, epidemic',
                'language_origin': 'Latin',
                'example_sentence': 'The medieval _____ devastated European populations.'
            },
            'plaid': {
                'definition': 'A pattern of intersecting lines in multiple colors, typically associated with Scottish tartans; fabric with this pattern.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'PLAD (emphasis on syllable)',
                'etymology': 'From Scottish Gaelic "plaide" meaning "blanket"',
                'memory_tips': 'Think "played" - patterns that played across the fabric',
                'alternate_spellings': 'tartan, checkered',
                'language_origin': 'Scottish Gaelic',
                'example_sentence': 'He wore a _____ shirt with red and green intersecting lines.'
            },
            'plaintiff': {
                'definition': 'A person who brings a legal action against another in a court of law; the party who initiates a lawsuit.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLAYN-tif (emphasis on first syllable)',
                'etymology': 'From Old French "plaintif" meaning "complaining"',
                'memory_tips': 'Think "plain-tiff" - someone who makes a plain complaint in court',
                'alternate_spellings': 'complainant, petitioner',
                'language_origin': 'Old French',
                'example_sentence': 'The _____ sued the company for damages after the accident.'
            },
            'plaiting': {
                'definition': 'The action of braiding or weaving strands together; interlacing strips of material to form a pattern.',
                'part_of_speech': 'verb (present participle), noun',
                'pronunciation_guide': 'PLAYT-ing (emphasis on first syllable)',
                'etymology': 'From "plait", from Old French "pleit" meaning "fold"',
                'memory_tips': 'Think "play-ting" - playing with strands while making a ting sound',
                'alternate_spellings': 'braiding, weaving',
                'language_origin': 'Old French',
                'example_sentence': 'She spent the afternoon _____ her daughter\'s long hair into intricate braids.'
            },
            'plan': {
                'definition': 'A detailed proposal for achieving something; an intention or decision about what to do; to design or make arrangements.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'PLAN (emphasis on syllable)',
                'etymology': 'From Latin "planum" meaning "flat surface, ground plan"',
                'memory_tips': 'Think "plan" - a flat layout of your intentions',
                'alternate_spellings': 'scheme, design, strategy',
                'language_origin': 'Latin',
                'example_sentence': 'They developed a comprehensive _____ to renovate the building.'
            },
            'plane': {
                'definition': 'A flat surface; an aircraft; a level of existence or development; a tool for smoothing wood.',
                'part_of_speech': 'noun, verb, adjective',
                'pronunciation_guide': 'PLAYN (emphasis on syllable)',
                'etymology': 'From Latin "planum" meaning "flat surface"',
                'memory_tips': 'Think "plain" - a flat, plain surface or flying plane',
                'alternate_spellings': 'aircraft, surface, level',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ took off smoothly into the clear blue sky.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_133_data:
            return batch_133_data[word_lower]
        
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
    
    def process_batch_133(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 133 with comprehensive Claude data"""
        words = []
        with open(input_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row['word']:  # Skip empty rows
                    continue
                    
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
    
    def save_batch_133_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 133 processed words to CSV"""
        
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
    """Process Batch 133 with comprehensive Claude data"""
    processor = Batch133Processor()
    input_csv = Path("output/batch_133_words.csv")
    output_csv = Path("output/batch_133_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 133 with comprehensive Claude data...")
    
    # Process all words in batch 133
    processed_words = processor.process_batch_133(input_csv)
    
    # Save results
    processor.save_batch_133_csv(processed_words, output_csv)
    
    logger.info(f"Batch 133 processing completed!")
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