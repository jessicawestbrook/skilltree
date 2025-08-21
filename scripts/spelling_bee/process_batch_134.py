#!/usr/bin/env python3
"""
Process Batch 134 of Spelling Bee Words with Comprehensive Claude Data
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
            'government', 'company', 'number', 'group', 'problem', 'fact', 'pick', 'picture', 'piece', 'phone', 'physical', 'pink', 'place', 'plan', 'plant', 'play', 'please'
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

class Batch134Processor:
    """Processes Batch 134 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 134 words"""
        
        # Comprehensive data for all 50 words in Batch 134
        batch_134_data = {
            'planetarium': {
                'definition': 'A domed building or room equipped with a device that projects images of stars and planets onto the ceiling to simulate the night sky.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'plan-uh-TAIR-ee-uhm (emphasis on third syllable)',
                'etymology': 'From New Latin "planetarium", from "planeta" meaning "planet"',
                'memory_tips': 'Think "planet-aquarium" - like an aquarium but for planets',
                'alternate_spellings': '',
                'language_origin': 'New Latin',
                'example_sentence': 'The children were amazed by the star show at the _____.'
            },
            'planetesimal': {
                'definition': 'A small rocky or icy body that is thought to have formed during the early stages of planetary formation in the solar system.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'plan-uh-TES-uh-muhl (emphasis on third syllable)',
                'etymology': 'From "planet" + "-esimal" (suffix meaning "very small")',
                'memory_tips': 'Think "planet-decimal" - very small pieces that make planets',
                'alternate_spellings': '',
                'language_origin': 'Modern Scientific English',
                'example_sentence': 'Scientists believe that _____ collisions helped form the larger planets.'
            },
            'plangency': {
                'definition': 'The quality of having a deep, reverberating, and mournful sound; plaintiveness or resonant sadness.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLAN-juhn-see (emphasis on first syllable)',
                'etymology': 'From Latin "plangere" meaning "to strike, beat the breast in mourning"',
                'memory_tips': 'Think "plan-gency" - the urgency of a mournful plan',
                'alternate_spellings': 'plaintiveness, mournfulness',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ of the funeral bells echoed across the valley.'
            },
            'planisphere': {
                'definition': 'A flat map showing the celestial sphere or a star chart that can be adjusted to show which stars are visible at any given time.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLAN-uh-sfeer (emphasis on first syllable)',
                'etymology': 'From Latin "planus" meaning "flat" + Greek "sphaira" meaning "sphere"',
                'memory_tips': 'Think "plan-sphere" - planning to see the sphere of stars on a flat surface',
                'alternate_spellings': 'star chart',
                'language_origin': 'Latin and Greek',
                'example_sentence': 'The astronomy student used a _____ to identify constellations visible in winter.'
            },
            'planogram': {
                'definition': 'A diagram or model that indicates the placement of retail products on shelves in order to maximize sales.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLAN-oh-gram (emphasis on first syllable)',
                'etymology': 'From "plan" + "-gram" meaning "written record"',
                'memory_tips': 'Think "plan-oh-gram" - a gram (diagram) of your retail plan',
                'alternate_spellings': 'shelf layout diagram',
                'language_origin': 'Modern English',
                'example_sentence': 'The store manager followed the _____ to arrange products for maximum customer appeal.'
            },
            'plans': {
                'definition': 'Detailed proposals for achieving something; intentions or decisions about what to do; diagrams or drawings.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'PLANZ (emphasis on syllable)',
                'etymology': 'Plural of "plan", from Latin "planum" meaning "flat surface"',
                'memory_tips': 'Think "plans" - multiple flat layouts of your intentions',
                'alternate_spellings': 'schemes, designs',
                'language_origin': 'Latin',
                'example_sentence': 'She made detailed _____ for her summer vacation.'
            },
            'plant': {
                'definition': 'A living organism that typically grows in soil and has leaves, stems, and roots; to put a seed or young plant in the ground.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'PLANT (emphasis on syllable)',
                'etymology': 'From Latin "planta" meaning "sprout, cutting"',
                'memory_tips': 'Think "plant" - you plant plants in the ground',
                'alternate_spellings': 'vegetation, flora',
                'language_origin': 'Latin',
                'example_sentence': 'She decided to _____ tomatoes in her garden this spring.'
            },
            'plantagenet': {
                'definition': 'A member of the royal dynasty that ruled England from 1154 to 1485, including kings like Henry II and Richard the Lionheart.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'plan-TAJ-uh-net (emphasis on second syllable)',
                'etymology': 'From the nickname of Geoffrey of Anjou, who wore a sprig of broom plant (planta genista) in his hat',
                'memory_tips': 'Think "plant-a-genet" - a royal family that planted their dynasty',
                'alternate_spellings': 'Angevin dynasty',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ kings ruled England for over three centuries.'
            },
            'plantain': {
                'definition': 'A large tropical fruit similar to a banana but typically cooked before eating; also a common weed with broad leaves.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLAN-tin (emphasis on first syllable)',
                'etymology': 'From Spanish "plátano", ultimately from Latin "platanus" meaning "plane tree"',
                'memory_tips': 'Think "plant-ain" - ain\'t a banana, but a cooking plant',
                'alternate_spellings': 'cooking banana',
                'language_origin': 'Spanish via Latin',
                'example_sentence': 'She fried sliced _____ as a side dish with the Caribbean meal.'
            },
            'plantigrade': {
                'definition': 'Walking with the entire sole of the foot touching the ground, as humans and bears do.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'PLAN-tuh-grayd (emphasis on first syllable)',
                'etymology': 'From Latin "planta" meaning "sole of foot" + "gradus" meaning "step"',
                'memory_tips': 'Think "plant-grade" - planting your whole foot like getting a grade',
                'alternate_spellings': 'flat-footed',
                'language_origin': 'Latin',
                'example_sentence': 'Bears are _____ animals, walking on their entire foot like humans do.'
            },
            'plants': {
                'definition': 'Living organisms that typically grow in soil and photosynthesize; factories or industrial facilities.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'PLANTS (emphasis on syllable)',
                'etymology': 'Plural of "plant", from Latin "planta"',
                'memory_tips': 'Think "plants" - green things that grow from the ground',
                'alternate_spellings': 'vegetation, factories',
                'language_origin': 'Latin',
                'example_sentence': 'The greenhouse was filled with exotic tropical _____.'
            },
            'plaque': {
                'definition': 'A flat piece of metal, wood, or stone with writing on it; a sticky deposit on teeth; a patch of damaged tissue.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLAK (emphasis on syllable)',
                'etymology': 'From French "plaque", from Dutch "placke" meaning "disk, patch"',
                'memory_tips': 'Think "plaque" - like plague but it sticks to surfaces',
                'alternate_spellings': 'tablet, buildup',
                'language_origin': 'French via Dutch',
                'example_sentence': 'The dentist removed _____ buildup from the patient\'s teeth.'
            },
            'plastic': {
                'definition': 'A synthetic material that can be molded when soft and hardened into shape; easily shaped or molded.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'PLAS-tik (emphasis on first syllable)',
                'etymology': 'From Greek "plastikos" meaning "moldable, fit for molding"',
                'memory_tips': 'Think "plas-tick" - ticks that can be molded like plastic',
                'alternate_spellings': 'synthetic material, moldable',
                'language_origin': 'Greek',
                'example_sentence': 'The toy was made from durable _____ that could withstand rough play.'
            },
            'plastron': {
                'definition': 'The lower shell of a turtle or tortoise; a padded chest protector worn in fencing.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLAS-truhn (emphasis on first syllable)',
                'etymology': 'From French "plastron", from Italian "piastrone" meaning "breastplate"',
                'memory_tips': 'Think "plas-tron" - plastic-like protection like Tron armor',
                'alternate_spellings': 'turtle shell, chest protector',
                'language_origin': 'French via Italian',
                'example_sentence': 'The turtle\'s _____ had distinctive yellow markings.'
            },
            'plates': {
                'definition': 'Flat dishes for serving food; thin, flat sheets of material; geological sections of the Earth\'s crust.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'PLAYTS (emphasis on syllable)',
                'etymology': 'Plural of "plate", from Old French "plate" meaning "flat"',
                'memory_tips': 'Think "plates" - flat things you eat from or that move in earthquakes',
                'alternate_spellings': 'dishes, sheets',
                'language_origin': 'Old French',
                'example_sentence': 'She set the dinner _____ on the table before the guests arrived.'
            },
            'platinum': {
                'definition': 'A precious silvery-white metal that is very resistant to corrosion and tarnishing; the highest level of achievement.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'PLAT-uh-nuhm (emphasis on first syllable)',
                'etymology': 'From Spanish "platina", diminutive of "plata" meaning "silver"',
                'memory_tips': 'Think "plat-in-um" - a plat (flat piece) in your mouth worth more than silver',
                'alternate_spellings': 'precious metal',
                'language_origin': 'Spanish',
                'example_sentence': 'The jewelry was made from pure _____ and set with diamonds.'
            },
            'platitude': {
                'definition': 'A trite, meaningless, or prosaic statement, especially one expressed as if it were original or significant.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLAT-uh-tood (emphasis on first syllable)',
                'etymology': 'From French "platitude", from "plat" meaning "flat, dull"',
                'memory_tips': 'Think "plat-attitude" - a flat, dull attitude in speech',
                'alternate_spellings': 'cliché, banality',
                'language_origin': 'French',
                'example_sentence': 'His speech was filled with tired _____ instead of meaningful insights.'
            },
            'platoon': {
                'definition': 'A subdivision of a military company, typically consisting of two or more squads; a group of people working together.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pluh-TOON (emphasis on second syllable)',
                'etymology': 'From French "peloton" meaning "small ball, group"',
                'memory_tips': 'Think "plat-oon" - a flat group moving like a cartoon',
                'alternate_spellings': 'military unit, squad',
                'language_origin': 'French',
                'example_sentence': 'The sergeant led his _____ through the training exercise.'
            },
            'platypus': {
                'definition': 'A unique Australian mammal with a duck-like bill, beaver-like tail, and webbed feet that lays eggs despite being a mammal.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLAT-uh-pus (emphasis on first syllable)',
                'etymology': 'From Greek "platypous" meaning "flat-footed"',
                'memory_tips': 'Think "platy-pus" - a cat (pus sounds like puss) with flat features',
                'alternate_spellings': 'duck-billed platypus',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ is one of only two mammals that lay eggs.'
            },
            'plaudits': {
                'definition': 'Enthusiastic approval or praise, especially when expressed publicly; acclaim or commendation.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'PLAW-dits (emphasis on first syllable)',
                'etymology': 'From Latin "plaudite" meaning "applaud!", from "plaudere" meaning "to clap"',
                'memory_tips': 'Think "applaud-its" - applauding for its great performance',
                'alternate_spellings': 'applause, praise, acclaim',
                'language_origin': 'Latin',
                'example_sentence': 'The young pianist received _____ from the audience and critics alike.'
            },
            'play': {
                'definition': 'To engage in activity for enjoyment; to perform music or act in a drama; recreational activity.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'PLAY (emphasis on syllable)',
                'etymology': 'From Old English "plegan" meaning "to exercise, frolic"',
                'memory_tips': 'Think "play" - having fun and being playful',
                'alternate_spellings': 'recreation, performance',
                'language_origin': 'Old English',
                'example_sentence': 'The children love to _____ in the park after school.'
            },
            'playground': {
                'definition': 'An outdoor area provided for children to play in, typically equipped with swings, slides, and other recreational equipment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLAY-grownd (emphasis on first syllable)',
                'etymology': 'From "play" + "ground", from Old English "plegan" + "grund"',
                'memory_tips': 'Think "play-ground" - ground where you play',
                'alternate_spellings': 'play area, recreation area',
                'language_origin': 'Old English',
                'example_sentence': 'The new _____ features modern equipment and safety surfaces.'
            },
            'playlist': {
                'definition': 'A list of songs or musical recordings to be played in a particular sequence, especially on a digital music player.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLAY-list (emphasis on first syllable)',
                'etymology': 'From "play" + "list", modern compound word',
                'memory_tips': 'Think "play-list" - a list of things to play',
                'alternate_spellings': 'music queue',
                'language_origin': 'Modern English',
                'example_sentence': 'She created a _____ of her favorite songs for the road trip.'
            },
            'playwright': {
                'definition': 'A person who writes plays for the theater; a dramatist.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLAY-ryt (emphasis on first syllable)',
                'etymology': 'From "play" + "wright" (meaning "worker, maker")',
                'memory_tips': 'Think "play-wright" - someone who writes plays right',
                'alternate_spellings': 'dramatist, play author',
                'language_origin': 'English',
                'example_sentence': 'The famous _____ won a Tony Award for her latest drama.'
            },
            'plaza': {
                'definition': 'A public square or open space in a city or town; a shopping center or mall.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLAH-zuh (emphasis on first syllable)',
                'etymology': 'From Spanish "plaza", from Latin "platea" meaning "broad street"',
                'memory_tips': 'Think "plaza" - like pizza but with an open space for gathering',
                'alternate_spellings': 'town square, mall',
                'language_origin': 'Spanish via Latin',
                'example_sentence': 'The festival was held in the town\'s central _____.'
            },
            'pleasant': {
                'definition': 'Giving a sense of happy satisfaction or enjoyment; agreeable and attractive.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'PLEZ-uhnt (emphasis on first syllable)',
                'etymology': 'From Old French "plaisant", from "plaisir" meaning "to please"',
                'memory_tips': 'Think "please-ant" - like an ant that aims to please',
                'alternate_spellings': 'agreeable, enjoyable',
                'language_origin': 'Old French',
                'example_sentence': 'The weather was _____ for their outdoor picnic.'
            },
            'please': {
                'definition': 'Used as a polite request; to make someone happy or satisfied; to choose or prefer.',
                'part_of_speech': 'verb, interjection',
                'pronunciation_guide': 'PLEEZ (emphasis on syllable)',
                'etymology': 'From Old French "plaisir" meaning "to give pleasure"',
                'memory_tips': 'Think "please" - saying it with ease to please others',
                'alternate_spellings': 'satisfy, gratify',
                'language_origin': 'Old French',
                'example_sentence': '_____ pass the salt when you have a moment.'
            },
            'pleiades': {
                'definition': 'A cluster of seven stars in the constellation Taurus, also known as the Seven Sisters; in Greek mythology, seven daughters of Atlas.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'PLEE-uh-deez (emphasis on first syllable)',
                'etymology': 'From Greek "Pleiades", possibly meaning "to sail" as they were used for navigation',
                'memory_tips': 'Think "please-add-ease" - seven sisters who please and add ease to navigation',
                'alternate_spellings': 'Seven Sisters',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ are easily visible to the naked eye on clear winter nights.'
            },
            'plenipotentiary': {
                'definition': 'A person, especially a diplomat, invested with full power to transact business; having complete authority.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'plen-uh-puh-TEN-shee-er-ee (emphasis on fourth syllable)',
                'etymology': 'From Latin "plenus" meaning "full" + "potentia" meaning "power"',
                'memory_tips': 'Think "plenty-potential-iary" - plenty of potential power',
                'alternate_spellings': 'full ambassador',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ was authorized to negotiate and sign the treaty on behalf of his country.'
            },
            'plenitude': {
                'definition': 'Abundance; a large quantity of something; fullness or completeness.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLEN-uh-tood (emphasis on first syllable)',
                'etymology': 'From Latin "plenitudo", from "plenus" meaning "full"',
                'memory_tips': 'Think "plenty-tude" - an attitude of having plenty',
                'alternate_spellings': 'abundance, fullness',
                'language_origin': 'Latin',
                'example_sentence': 'The garden displayed a _____ of colorful flowers in full bloom.'
            },
            'plentiful': {
                'definition': 'Existing in large quantity; abundant; more than adequate in amount.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'PLEN-tuh-fuhl (emphasis on first syllable)',
                'etymology': 'From "plenty" + "-ful", from Latin "plenus" meaning "full"',
                'memory_tips': 'Think "plenty-full" - full of plenty',
                'alternate_spellings': 'abundant, ample',
                'language_origin': 'Latin via English',
                'example_sentence': 'The harvest was _____ this year due to favorable weather conditions.'
            },
            'plethora': {
                'definition': 'A large or excessive amount of something; an abundance that may be overwhelming.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLETH-er-uh (emphasis on first syllable)',
                'etymology': 'From Greek "plethora" meaning "fullness, abundance"',
                'memory_tips': 'Think "plenty-thorough" - thoroughly plenty of something',
                'alternate_spellings': 'abundance, excess',
                'language_origin': 'Greek',
                'example_sentence': 'The store offered a _____ of choices in their electronics department.'
            },
            'pliant': {
                'definition': 'Easily bent; flexible and supple; readily influenced or controlled.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'PLY-uhnt (emphasis on first syllable)',
                'etymology': 'From French "pliant", from "plier" meaning "to bend"',
                'memory_tips': 'Think "ply-ant" - an ant that can ply (bend) easily',
                'alternate_spellings': 'flexible, bendable',
                'language_origin': 'French',
                'example_sentence': 'The young tree branches were _____ enough to bend in the strong wind without breaking.'
            },
            'plodddded': {
                'definition': '[POTENTIAL SPELLING ERROR] This appears to be a misspelling of "plodded" with extra d\'s.',
                'part_of_speech': 'potential error',
                'pronunciation_guide': '[POSSIBLE ERROR - extra letters]',
                'etymology': '[POSSIBLE ERROR - check spelling]',
                'memory_tips': 'This may be a data error - check if this should be "plodded"',
                'alternate_spellings': 'plodded (?)',
                'language_origin': 'Uncertain - possible error',
                'example_sentence': '[NEEDS CLARIFICATION] He _____ slowly through the muddy field.'
            },
            'plodded': {
                'definition': 'Walked slowly and heavily; worked slowly and perseveringly; made steady but laborious progress.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'PLOD-id (emphasis on first syllable)',
                'etymology': 'Past tense of "plod", possibly imitative of heavy footsteps',
                'memory_tips': 'Think "plod-did" - did plod along slowly',
                'alternate_spellings': 'trudged, persevered',
                'language_origin': 'English (imitative)',
                'example_sentence': 'She _____ through the snow to reach the cabin.'
            },
            'plopped': {
                'definition': 'Fell, dropped, or sat down heavily and suddenly; made a sound like something dropping into water.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'PLOPT (emphasis on syllable)',
                'etymology': 'Past tense of "plop", imitative of the sound',
                'memory_tips': 'Think "plop-ped" - it plopped and made a ped (sound)',
                'alternate_spellings': 'dropped, fell',
                'language_origin': 'English (imitative)',
                'example_sentence': 'The frog _____ into the pond with a splash.'
            },
            'plot': {
                'definition': 'A piece of ground; the main story of a literary work; a secret plan or scheme.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'PLOT (emphasis on syllable)',
                'etymology': 'From Old English "plot" meaning "small piece of ground"',
                'memory_tips': 'Think "plot" - a spot of land or a story spot',
                'alternate_spellings': 'scheme, story, land',
                'language_origin': 'Old English',
                'example_sentence': 'The _____ of the novel kept readers guessing until the end.'
            },
            'plover': {
                'definition': 'A small shorebird with a short bill and typically running rather than walking; often found on beaches and mudflats.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLUHV-ur (emphasis on first syllable)',
                'etymology': 'From Old French "plovier", from Latin "pluvia" meaning "rain"',
                'memory_tips': 'Think "plover" - a bird that loves rain (pluvial)',
                'alternate_spellings': 'shorebird',
                'language_origin': 'Old French via Latin',
                'example_sentence': 'The _____ quickly scurried along the beach searching for small crabs.'
            },
            'pluck': {
                'definition': 'To pull or pick quickly; courage and determination; to pull feathers from a bird.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'PLUHK (emphasis on syllable)',
                'etymology': 'From Old English "pluccian" meaning "to pull"',
                'memory_tips': 'Think "pluck" - like luck but you pull it out with courage',
                'alternate_spellings': 'pull, courage',
                'language_origin': 'Old English',
                'example_sentence': 'She had the _____ to speak up for what she believed was right.'
            },
            'plucked': {
                'definition': 'Pulled or picked quickly; removed by pulling; gathered with the fingers.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'PLUHKT (emphasis on syllable)',
                'etymology': 'Past tense of "pluck", from Old English "pluccian"',
                'memory_tips': 'Think "pluck-ed" - it was plucked and now it\'s gone',
                'alternate_spellings': 'pulled, picked',
                'language_origin': 'Old English',
                'example_sentence': 'She _____ the ripe apples from the tree.'
            },
            'plumage': {
                'definition': 'The feathers of a bird, especially when considered as forming the coat or covering.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLOO-mij (emphasis on first syllable)',
                'etymology': 'From French "plumage", from "plume" meaning "feather"',
                'memory_tips': 'Think "plume-age" - the age when plumes (feathers) are most beautiful',
                'alternate_spellings': 'feathers, feather coat',
                'language_origin': 'French',
                'example_sentence': 'The peacock displayed its magnificent _____ to attract a mate.'
            },
            'plumassier': {
                'definition': 'A person who prepares, sells, or works with feathers, especially for decorative purposes in fashion or millinery.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ploo-mah-see-AY (emphasis on fourth syllable)',
                'etymology': 'From French "plumassier", from "plume" meaning "feather"',
                'memory_tips': 'Think "plume-classier" - someone who makes plumes look classier',
                'alternate_spellings': 'feather worker',
                'language_origin': 'French',
                'example_sentence': 'The _____ created elaborate feathered headdresses for the theater production.'
            },
            'plumbago': {
                'definition': 'A plant with blue, white, or red flowers native to warm climates; graphite or black lead used in pencils.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pluhm-BAY-goh (emphasis on second syllable)',
                'etymology': 'From Latin "plumbago", from "plumbum" meaning "lead"',
                'memory_tips': 'Think "plumb-a-go" - plumb a go at finding this lead-like plant',
                'alternate_spellings': 'leadwort, graphite',
                'language_origin': 'Latin',
                'example_sentence': 'The garden border was lined with beautiful blue _____ flowers.'
            },
            'plumbing': {
                'definition': 'The system of pipes, tanks, and fixtures concerned with water supply and drainage; the work of installing and maintaining such systems.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLUHM-ing (emphasis on first syllable)',
                'etymology': 'From "plumb" (lead, from Latin "plumbum") + "-ing"',
                'memory_tips': 'Think "plumb-ing" - using lead pipes for water systems',
                'alternate_spellings': 'pipes, water system',
                'language_origin': 'Latin',
                'example_sentence': 'The old house needed extensive _____ repairs before it could be occupied.'
            },
            'plume': {
                'definition': 'A large feather or arrangement of feathers; a cloud or column of smoke, steam, or other vapor.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'PLOOM (emphasis on syllable)',
                'etymology': 'From Latin "pluma" meaning "feather"',
                'memory_tips': 'Think "plume" - like fume but from a feather or fancy hat',
                'alternate_spellings': 'feather, column',
                'language_origin': 'Latin',
                'example_sentence': 'A _____ of smoke rose from the chimney into the cold air.'
            },
            'plumeria': {
                'definition': 'A tropical tree or shrub with fragrant, waxy flowers in colors like white, yellow, pink, or red; also called frangipani.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ploo-MEER-ee-uh (emphasis on second syllable)',
                'etymology': 'Named after Charles Plumier, a French botanist',
                'memory_tips': 'Think "plume-ria" - a tree with plume-like fragrant flowers',
                'alternate_spellings': 'frangipani',
                'language_origin': 'Modern Latin (from proper name)',
                'example_sentence': 'The _____ tree filled the tropical garden with its sweet fragrance.'
            },
            'plummet': {
                'definition': 'To fall or drop straight down at high speed; to decrease rapidly in value or amount.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'PLUHM-it (emphasis on first syllable)',
                'etymology': 'From Old French "plommet", diminutive of "plomb" meaning "lead weight"',
                'memory_tips': 'Think "plum-met" - a plum that met the ground fast',
                'alternate_spellings': 'fall rapidly, drop',
                'language_origin': 'Old French',
                'example_sentence': 'Stock prices _____ after the company announced unexpected losses.'
            },
            'plundered': {
                'definition': 'Robbed or pillaged, especially during war; took goods by force; looted.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'PLUHN-durd (emphasis on first syllable)',
                'etymology': 'Past tense of "plunder", from German "plündern"',
                'memory_tips': 'Think "plunder-ed" - it was plundered and now it\'s gone',
                'alternate_spellings': 'looted, pillaged',
                'language_origin': 'German',
                'example_sentence': 'The ancient tomb had been _____ by treasure hunters centuries ago.'
            },
            'plunger': {
                'definition': 'A tool with a rubber cup on a handle used to clear blocked drains; a part that moves up and down in a cylinder.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PLUHN-jur (emphasis on first syllable)',
                'etymology': 'From "plunge" + "-er", from Old French "plongier"',
                'memory_tips': 'Think "plunge-er" - something that plunges into drains',
                'alternate_spellings': 'drain clearer, piston',
                'language_origin': 'Old French',
                'example_sentence': 'He used a _____ to unclog the bathroom sink.'
            },
            'plural': {
                'definition': 'Referring to more than one person or thing; the form of a word used to denote more than one.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'PLOOR-uhl (emphasis on first syllable)',
                'etymology': 'From Latin "pluralis", from "plus" meaning "more"',
                'memory_tips': 'Think "plus-ral" - plus more than one',
                'alternate_spellings': 'multiple, more than one',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ form of "child" is "children".'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_134_data:
            return batch_134_data[word_lower]
        
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
    
    def process_batch_134(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 134 with comprehensive Claude data"""
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
    
    def save_batch_134_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 134 processed words to CSV"""
        
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
    """Process Batch 134 with comprehensive Claude data"""
    processor = Batch134Processor()
    input_csv = Path("output/batch_134_words.csv")
    output_csv = Path("output/batch_134_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 134 with comprehensive Claude data...")
    
    # Process all words in batch 134
    processed_words = processor.process_batch_134(input_csv)
    
    # Save results
    processor.save_batch_134_csv(processed_words, output_csv)
    
    logger.info(f"Batch 134 processing completed!")
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