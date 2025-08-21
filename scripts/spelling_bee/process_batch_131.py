#!/usr/bin/env python3
"""
Process Batch 131 of Spelling Bee Words with Comprehensive Claude Data
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

class Batch131Processor:
    """Processes Batch 131 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 131 words"""
        
        # Comprehensive data for all 50 words in Batch 131
        batch_131_data = {
            'perpendicularity': {
                'definition': 'The state or quality of being perpendicular; the condition of forming a right angle (90 degrees) with another line or surface.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pur-pen-dik-yuh-LAR-uh-tee (emphasis on fifth syllable)',
                'etymology': 'From Latin "perpendicularis" meaning "vertical, plumb" + "-ity" suffix forming nouns',
                'memory_tips': 'Think "per-pen-particular-ity" - particularly perpendicular quality',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The architect checked the _____ of the walls to ensure they met at perfect right angles.'
            },
            'perpetrate': {
                'definition': 'To carry out or commit (an illegal, harmful, or immoral act); to be responsible for bringing about something undesirable.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'PUR-puh-trayt (emphasis on first syllable)',
                'etymology': 'From Latin "perpetratus", past participle of "perpetrare" meaning "to accomplish, perform"',
                'memory_tips': 'Think "purr-pet-rate" - like a cat rating how well a crime was committed',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The detective worked to identify who would _____ such an elaborate fraud scheme.'
            },
            'perpetrator': {
                'definition': 'A person who commits a crime or other harmful act; someone who carries out an illegal or immoral deed.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PUR-puh-tray-tur (emphasis on first syllable)',
                'etymology': 'From Latin "perpetrator", agent noun from "perpetrare" meaning "to accomplish"',
                'memory_tips': 'Think "purr-pet-traitor" - a traitorous pet who commits crimes',
                'alternate_spellings': 'criminal, offender',
                'language_origin': 'Latin',
                'example_sentence': 'The security cameras helped police identify the _____ of the robbery.'
            },
            'perpetual': {
                'definition': 'Never ending or changing; continuous throughout time; occurring repeatedly without interruption.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'pur-PECH-oo-uhl (emphasis on second syllable)',
                'etymology': 'From Latin "perpetualis", from "perpetuus" meaning "continuous, universal"',
                'memory_tips': 'Think "purr-pet-you-all" - a pet that purrs for all eternity',
                'alternate_spellings': 'continuous, endless',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ motion machine was supposedly designed to run forever without external energy.'
            },
            'perplex': {
                'definition': 'To cause someone to feel completely baffled or confused; to make something difficult to understand.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'pur-PLEKS (emphasis on second syllable)',
                'etymology': 'From Latin "perplexus" meaning "confused, entangled"',
                'memory_tips': 'Think "purr-plex" - when a cat\'s behavior is so complex it confuses you',
                'alternate_spellings': 'confuse, baffle',
                'language_origin': 'Latin',
                'example_sentence': 'The mysterious disappearance continued to _____ investigators.'
            },
            'perquisite': {
                'definition': 'A special privilege, benefit, or advantage that comes with a job or position; an additional payment or benefit beyond regular salary.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PUR-kwuh-zit (emphasis on first syllable)',
                'etymology': 'From Latin "perquisitum" meaning "something sought after, acquired"',
                'memory_tips': 'Think "perk-you-sit" - perks you get when you sit in a high position',
                'alternate_spellings': 'perk, benefit',
                'language_origin': 'Latin',
                'example_sentence': 'A company car was one of the _____ that came with the executive position.'
            },
            'perseverance': {
                'definition': 'Persistence in doing something despite difficulty or delay in achieving success; steadfastness in pursuit of a goal.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pur-suh-VEER-uhns (emphasis on third syllable)',
                'etymology': 'From Latin "perseverantia", from "perseverare" meaning "to persist, continue steadfastly"',
                'memory_tips': 'Think "purr-severe-ants" - ants that purr through severe challenges',
                'alternate_spellings': 'persistence, determination',
                'language_origin': 'Latin',
                'example_sentence': 'Her _____ in studying mathematics finally paid off when she solved the difficult theorem.'
            },
            'persia': {
                'definition': 'The historical name for Iran, a country in southwestern Asia known for its ancient empire and rich cultural heritage.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'PUR-zhuh (emphasis on first syllable)',
                'etymology': 'From Greek "Persis", from Old Persian "Parsa" referring to the Persian people',
                'memory_tips': 'Think "purr-shuh" - the land where Persian cats originated',
                'alternate_spellings': 'Iran (modern name)',
                'language_origin': 'Old Persian via Greek',
                'example_sentence': 'Ancient _____ was known for its magnificent palaces and advanced road systems.'
            },
            'persian': {
                'definition': 'Relating to Persia (Iran) or its people, language, or culture; a native or inhabitant of Persia.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'PUR-zhuhn (emphasis on first syllable)',
                'etymology': 'From Latin "Persicus", from Greek "Persikos" meaning "of Persia"',
                'memory_tips': 'Think "purr-shun" - relating to the land of purring Persian cats',
                'alternate_spellings': 'Iranian (modern term)',
                'language_origin': 'Greek via Latin',
                'example_sentence': 'The _____ carpet displayed intricate patterns and vibrant colors.'
            },
            'persiflage': {
                'definition': 'Light, bantering talk; frivolous or mocking conversation characterized by wit and humor.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PUR-suh-flahzh (emphasis on first syllable)',
                'etymology': 'From French "persiflage", from "persifler" meaning "to banter, mock"',
                'memory_tips': 'Think "purr-see-flage" - cats purring while they see playful banter',
                'alternate_spellings': 'banter, raillery',
                'language_origin': 'French',
                'example_sentence': 'The dinner party was filled with witty _____ between old friends.'
            },
            'person': {
                'definition': 'An individual human being; a man, woman, or child as distinct from an animal or thing.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PUR-suhn (emphasis on first syllable)',
                'etymology': 'From Latin "persona" meaning "mask, character in a play, person"',
                'memory_tips': 'Think "purr-son" - every person can be as individual as a cat\'s purr',
                'alternate_spellings': 'individual, human being',
                'language_origin': 'Latin',
                'example_sentence': 'Each _____ has unique talents and perspectives to contribute.'
            },
            'personnel': {
                'definition': 'The people employed by an organization; the department responsible for hiring and managing employees.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pur-suh-NEL (emphasis on third syllable)',
                'etymology': 'From French "personnel", from "personne" meaning "person"',
                'memory_tips': 'Think "person-nel" - all the persons in a company',
                'alternate_spellings': 'staff, employees',
                'language_origin': 'French',
                'example_sentence': 'The _____ department handled all matters related to employee benefits.'
            },
            'persons': {
                'definition': 'The plural form of person, especially when referring to individuals in a formal or legal context.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'PUR-suhnz (emphasis on first syllable)',
                'etymology': 'Plural of "person", from Latin "persona"',
                'memory_tips': 'Think "purr-sons" - multiple individual people, each unique',
                'alternate_spellings': 'people, individuals',
                'language_origin': 'Latin',
                'example_sentence': 'The elevator was designed to carry no more than eight _____.'
            },
            'perspicacious': {
                'definition': 'Having keen insight and understanding; able to perceive things clearly and comprehend their meaning quickly.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'pur-spi-KAY-shus (emphasis on third syllable)',
                'etymology': 'From Latin "perspicax" meaning "sharp-sighted, keen"',
                'memory_tips': 'Think "purr-spick-a-cious" - spicily sharp and perceptive like a cat',
                'alternate_spellings': 'perceptive, astute',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ detective quickly noticed details that others had missed.'
            },
            'persuasible': {
                'definition': 'Capable of being persuaded or convinced; open to influence through reasoning or argument.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'pur-SWAY-zuh-buhl (emphasis on second syllable)',
                'etymology': 'From Latin "persuasus", past participle of "persuadere" meaning "to convince" + "-ible"',
                'memory_tips': 'Think "purr-sway-able" - able to be swayed like a cat can be convinced with treats',
                'alternate_spellings': 'convincible, influenceable',
                'language_origin': 'Latin',
                'example_sentence': 'She proved to be _____ when presented with compelling evidence.'
            },
            'pertinacity': {
                'definition': 'The quality of being determined to continue with a course of action despite obstacles; stubborn persistence.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pur-tn-AS-uh-tee (emphasis on third syllable)',
                'etymology': 'From Latin "pertinacia", from "pertinax" meaning "holding fast, stubborn"',
                'memory_tips': 'Think "purr-ten-a-city" - the persistence of ten cats trying to enter a city',
                'alternate_spellings': 'persistence, stubbornness',
                'language_origin': 'Latin',
                'example_sentence': 'His _____ in pursuing the research eventually led to a breakthrough discovery.'
            },
            'peru': {
                'definition': 'A country in South America known for its ancient Incan civilization, including Machu Picchu, and its diverse geography.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'puh-ROO (emphasis on second syllable)',
                'etymology': 'Possibly from Quechua "piruw" or from Spanish interpretation of indigenous place names',
                'memory_tips': 'Think "purr-oo" - a cat purring at the amazing sights in Peru',
                'alternate_spellings': 'República del Perú (official name)',
                'language_origin': 'Uncertain, possibly Quechua',
                'example_sentence': 'Tourists from around the world visit _____ to see the ancient ruins of Machu Picchu.'
            },
            'peruse': {
                'definition': 'To read or examine something carefully and thoroughly; to scrutinize or study with attention to detail.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'puh-ROOZ (emphasis on second syllable)',
                'etymology': 'From Middle English "perusen" meaning "to use up, wear out"',
                'memory_tips': 'Think "purr-use" - a cat carefully using its eyes to examine something',
                'alternate_spellings': 'examine, scrutinize',
                'language_origin': 'Middle English',
                'example_sentence': 'She took time to _____ the contract before signing it.'
            },
            'pervading': {
                'definition': 'Spreading throughout; present in every part of something; permeating completely.',
                'part_of_speech': 'verb (present participle), adjective',
                'pronunciation_guide': 'pur-VAY-ding (emphasis on second syllable)',
                'etymology': 'From Latin "pervadere" meaning "to go through, spread throughout"',
                'memory_tips': 'Think "purr-vading" - a cat\'s purr pervading the entire room',
                'alternate_spellings': 'permeating, spreading',
                'language_origin': 'Latin',
                'example_sentence': 'A sense of excitement was _____ the crowd before the concert began.'
            },
            'pervasive': {
                'definition': 'Existing in or spreading through every part of something; having a penetrating and persistent presence.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'pur-VAY-siv (emphasis on second syllable)',
                'etymology': 'From Latin "pervasivus", from "pervadere" meaning "to spread throughout"',
                'memory_tips': 'Think "purr-vase-ive" - like a cat\'s scent spreading from a vase throughout the house',
                'alternate_spellings': 'widespread, ubiquitous',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ influence of social media has changed how people communicate.'
            },
            'pesos': {
                'definition': 'The plural form of peso, which is the monetary unit used in several Latin American countries and the Philippines.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'PAY-sohs (emphasis on first syllable)',
                'etymology': 'From Spanish "peso" meaning "weight", from Latin "pensum"',
                'memory_tips': 'Think "pay-sohs" - you pay with these coins that weigh something',
                'alternate_spellings': 'peso (singular)',
                'language_origin': 'Spanish',
                'example_sentence': 'The tourist exchanged dollars for _____ before traveling to Mexico.'
            },
            'pessimum': {
                'definition': 'The worst or most unfavorable condition or state; the least favorable point in a range of possibilities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PES-uh-mum (emphasis on first syllable)',
                'etymology': 'From Latin "pessimus" meaning "worst", superlative of "malus" (bad)',
                'memory_tips': 'Think "pest-simum" - the worst possible pest situation',
                'alternate_spellings': 'worst case, minimum',
                'language_origin': 'Latin',
                'example_sentence': 'The plant growth reached its _____ during the drought conditions.'
            },
            'pestilence': {
                'definition': 'A fatal epidemic disease, especially bubonic plague; something that is considered harmful, destructive, or morally corrupting.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PES-tuh-luhns (emphasis on first syllable)',
                'etymology': 'From Latin "pestilentia", from "pestis" meaning "plague, pestilence"',
                'memory_tips': 'Think "pest-ill-ence" - when pests make everyone ill with disease',
                'alternate_spellings': 'plague, epidemic',
                'language_origin': 'Latin',
                'example_sentence': 'The medieval _____ wiped out nearly a third of Europe\'s population.'
            },
            'petal': {
                'definition': 'One of the colored parts of a flower that surrounds the reproductive organs, typically soft and delicate.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PET-uhl (emphasis on first syllable)',
                'etymology': 'From Greek "petalon" meaning "leaf, thin plate"',
                'memory_tips': 'Think "pet-all" - you could pet all the soft petals of a flower',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Each _____ of the rose was perfectly formed and velvety to the touch.'
            },
            'petechia': {
                'definition': 'A small red or purple spot on the skin caused by bleeding from broken capillary blood vessels.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'puh-TEE-kee-uh (emphasis on second syllable)',
                'etymology': 'From Italian "petecchia", from Latin "petigo" meaning "skin eruption"',
                'memory_tips': 'Think "pet-teach-ia" - teaching about pet spots on the skin',
                'alternate_spellings': 'petechiae (plural)',
                'language_origin': 'Latin via Italian',
                'example_sentence': 'The doctor noticed a _____ on the patient\'s arm and ordered blood tests.'
            },
            'petite': {
                'definition': 'Small and dainty in size or stature, especially referring to a woman\'s build; designed for small sizes.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'puh-TEET (emphasis on second syllable)',
                'etymology': 'From French "petit" meaning "small", feminine form "petite"',
                'memory_tips': 'Think "pet-eat" - a small pet that doesn\'t eat much',
                'alternate_spellings': 'small, diminutive',
                'language_origin': 'French',
                'example_sentence': 'The _____ dancer moved gracefully across the stage.'
            },
            'petrifying': {
                'definition': 'Causing someone to feel so frightened that they cannot move; turning into stone through mineral replacement.',
                'part_of_speech': 'verb (present participle), adjective',
                'pronunciation_guide': 'PET-ruh-fy-ing (emphasis on first syllable)',
                'etymology': 'From Greek "petros" meaning "stone" + Latin "facere" meaning "to make"',
                'memory_tips': 'Think "pet-rye-fying" - so scary it turns you to stone like rye bread',
                'alternate_spellings': 'terrifying, fossilizing',
                'language_origin': 'Greek and Latin',
                'example_sentence': 'The _____ roar of the lion froze the explorer in place.'
            },
            'petroglyphs': {
                'definition': 'Rock carvings or engravings, especially prehistoric ones, created by removing part of a rock surface.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'PET-roh-glifs (emphasis on first syllable)',
                'etymology': 'From Greek "petros" meaning "stone" + "glyphein" meaning "to carve"',
                'memory_tips': 'Think "pet-row-glyphs" - pets carved in rows on stone',
                'alternate_spellings': 'petroglyph (singular)',
                'language_origin': 'Greek',
                'example_sentence': 'Ancient _____ found in the canyon depicted hunting scenes and animals.'
            },
            'petroleum': {
                'definition': 'A naturally occurring liquid fuel composed of hydrocarbon deposits; crude oil used to make gasoline and other products.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'puh-TROH-lee-uhm (emphasis on second syllable)',
                'etymology': 'From Latin "petroleum", from "petra" (rock) + "oleum" (oil)',
                'memory_tips': 'Think "pet-role-eum" - the role of this substance in petrol',
                'alternate_spellings': 'crude oil, oil',
                'language_origin': 'Latin',
                'example_sentence': 'The discovery of _____ transformed the local economy.'
            },
            'petticoat': {
                'definition': 'A woman\'s undergarment worn beneath a dress or skirt, typically a slip or underskirt.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PET-ee-koht (emphasis on first syllable)',
                'etymology': 'From "petty coat", meaning a small coat or short garment',
                'memory_tips': 'Think "pet-tee-coat" - a small coat for a pet under a dress',
                'alternate_spellings': 'slip, underskirt',
                'language_origin': 'Middle English',
                'example_sentence': 'The vintage dress required a _____ to give it the proper shape.'
            },
            'pews': {
                'definition': 'Long wooden benches with backs, typically arranged in rows in churches for the congregation to sit on.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'PYOOZ (emphasis on first syllable)',
                'etymology': 'From Old French "puie" meaning "balcony, elevated place"',
                'memory_tips': 'Think "p-yews" - where people say "phew" after a long sermon',
                'alternate_spellings': 'pew (singular), benches',
                'language_origin': 'Old French',
                'example_sentence': 'The congregation filled the _____ for the Sunday morning service.'
            },
            'pgames': {
                'definition': '[POTENTIAL ERROR] This may be an incomplete word or abbreviation; could refer to Paralympic Games or a similar term.',
                'part_of_speech': 'noun (possible abbreviation)',
                'pronunciation_guide': 'PEE-gaymz (if abbreviation)',
                'etymology': 'Unclear - possibly abbreviation for "Paralympic Games" or similar',
                'memory_tips': 'May be an error or abbreviation requiring clarification',
                'alternate_spellings': 'Paralympic Games (?)',
                'language_origin': 'Uncertain',
                'example_sentence': '[NEEDS CLARIFICATION] The _____ brought together athletes from around the world.'
            },
            'phalanges': {
                'definition': 'The bones of the fingers and toes; the plural form of phalanx in anatomical terms.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'fuh-LAN-jeez (emphasis on second syllable)',
                'etymology': 'From Greek "phalanx" meaning "line of battle, finger bone"',
                'memory_tips': 'Think "fal-anges" - fallen angels with finger bones',
                'alternate_spellings': 'phalanx (singular), finger bones',
                'language_origin': 'Greek',
                'example_sentence': 'The X-ray revealed a fracture in one of the _____ of her index finger.'
            },
            'pharaoh': {
                'definition': 'A ruler of ancient Egypt, considered to be a living god and absolute monarch of the Egyptian empire.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAIR-oh (emphasis on first syllable)',
                'etymology': 'From Hebrew "par\'oh", from Egyptian "per-aa" meaning "great house"',
                'memory_tips': 'Think "fair-oh" - the fair ruler who said "oh" to all requests',
                'alternate_spellings': 'pharaoh, king of Egypt',
                'language_origin': 'Egyptian via Hebrew',
                'example_sentence': 'The _____ was buried in an elaborate tomb filled with treasures.'
            },
            'pharaohopponency': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "pharaoh" (Egyptian ruler) + "opponency" (opposition).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "pharaoh" and "opponency"',
                'alternate_spellings': 'pharaoh + opponency (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'pharmacy': {
                'definition': 'A place where medicinal drugs are prepared and dispensed; the science and practice of preparing and dispensing drugs.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAHR-muh-see (emphasis on first syllable)',
                'etymology': 'From Greek "pharmakeia" meaning "use of drugs, medicines"',
                'memory_tips': 'Think "farm-a-see" - you can see the farm where medicine is made',
                'alternate_spellings': 'drugstore, apothecary',
                'language_origin': 'Greek',
                'example_sentence': 'She picked up her prescription at the local _____.'
            },
            'pharmacyfondant': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "pharmacy" (drugstore) + "fondant" (sweet confection).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "pharmacy" and "fondant"',
                'alternate_spellings': 'pharmacy + fondant (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'pharynx': {
                'definition': 'The cavity behind the nose and mouth, connecting them to the esophagus; the throat area where breathing and swallowing pathways cross.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAIR-inks (emphasis on first syllable)',
                'etymology': 'From Greek "pharynx" meaning "throat, windpipe"',
                'memory_tips': 'Think "fair-inks" - fair inks flow through the throat like food and air',
                'alternate_spellings': 'throat',
                'language_origin': 'Greek',
                'example_sentence': 'The doctor examined her _____ for signs of infection.'
            },
            'phenom': {
                'definition': 'A person who is outstandingly talented or admired, especially for their remarkable abilities; short for phenomenon.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FEE-nom (emphasis on first syllable)',
                'etymology': 'Shortened form of "phenomenon", from Greek "phainomenon" meaning "thing appearing"',
                'memory_tips': 'Think "fee-nom" - someone so talented they command a fee',
                'alternate_spellings': 'phenomenon, prodigy',
                'language_origin': 'Greek',
                'example_sentence': 'The young athlete was considered a _____ in the world of professional tennis.'
            },
            'phenomenal': {
                'definition': 'Remarkably impressive or extraordinary; relating to phenomena or things as they appear to our experience.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'fuh-NOM-uh-nuhl (emphasis on second syllable)',
                'etymology': 'From Greek "phainomenon" meaning "thing appearing" + "-al"',
                'memory_tips': 'Think "fee-nominal" - beyond nominal, extremely impressive',
                'alternate_spellings': 'extraordinary, remarkable',
                'language_origin': 'Greek',
                'example_sentence': 'The concert was _____, exceeding all expectations.'
            },
            'phenotype': {
                'definition': 'The set of observable characteristics of an organism resulting from the interaction of its genotype with the environment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FEE-noh-typ (emphasis on first syllable)',
                'etymology': 'From Greek "phainein" meaning "to show" + "typos" meaning "type"',
                'memory_tips': 'Think "fee-no-type" - the type you can see, not hidden in genes',
                'alternate_spellings': 'observable traits',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ of the plant included its height, leaf shape, and flower color.'
            },
            'phil': {
                'definition': 'A prefix meaning "love" or "loving"; also used as a shortened form of names like Philip.',
                'part_of_speech': 'prefix, noun (name)',
                'pronunciation_guide': 'FIL (emphasis on syllable)',
                'etymology': 'From Greek "philos" meaning "loving, fond of"',
                'memory_tips': 'Think "fill" - fill your heart with love',
                'alternate_spellings': 'Philip (full name)',
                'language_origin': 'Greek',
                'example_sentence': 'The prefix _____ appears in words like "philosophy" and "philanthropy".'
            },
            'philharmonic': {
                'definition': 'Relating to a large orchestra or musical society; literally meaning "loving harmony".',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'fil-har-MON-ik (emphasis on third syllable)',
                'etymology': 'From Greek "philos" (loving) + "harmonia" (harmony)',
                'memory_tips': 'Think "fill-harmonic" - filling the air with harmonious music',
                'alternate_spellings': 'orchestra, symphony',
                'language_origin': 'Greek',
                'example_sentence': 'The city _____ performed Beethoven\'s Symphony No. 9.'
            },
            'philistine': {
                'definition': 'A person who is hostile or indifferent to culture and the arts; someone lacking in cultural appreciation.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'FIL-uh-steen (emphasis on first syllable)',
                'etymology': 'From Hebrew "Pelishtim", referring to the ancient Palestinian people',
                'memory_tips': 'Think "fill-a-steam" - filling with steam instead of appreciating fine culture',
                'alternate_spellings': 'uncultured person',
                'language_origin': 'Hebrew',
                'example_sentence': 'The art critic called him a _____ for dismissing abstract painting.'
            },
            'philology': {
                'definition': 'The study of language in written historical sources; the branch of knowledge dealing with the structure and development of language.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fi-LOL-uh-jee (emphasis on second syllable)',
                'etymology': 'From Greek "philologia", from "philos" (loving) + "logos" (word, speech)',
                'memory_tips': 'Think "fill-ology" - the ology that fills your mind with language love',
                'alternate_spellings': 'linguistics, language study',
                'language_origin': 'Greek',
                'example_sentence': 'Her degree in _____ prepared her to analyze ancient manuscripts.'
            },
            'philopatry': {
                'definition': 'The tendency of an organism to stay in or return to its birthplace or home area, especially for breeding.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FIL-oh-pay-tree (emphasis on first syllable)',
                'etymology': 'From Greek "philos" (loving) + "patria" (fatherland, homeland)',
                'memory_tips': 'Think "fill-oh-patriot" - filled with love for your homeland',
                'alternate_spellings': 'site fidelity',
                'language_origin': 'Greek',
                'example_sentence': 'Salmon demonstrate _____ by returning to their natal streams to spawn.'
            },
            'philos': {
                'definition': 'A Greek root meaning "loving" or "fond of"; used in forming compound words related to love or affinity.',
                'part_of_speech': 'prefix/root',
                'pronunciation_guide': 'FEE-lohs (emphasis on first syllable)',
                'etymology': 'From ancient Greek "philos" meaning "loving, dear, fond"',
                'memory_tips': 'Think "fee-low" - a low fee for loving something',
                'alternate_spellings': 'phil- (prefix form)',
                'language_origin': 'Ancient Greek',
                'example_sentence': 'The root _____ appears in words like "philosophy" and "Philadelphia".'
            },
            'philosophize': {
                'definition': 'To engage in philosophical reasoning or speculation; to theorize about fundamental questions of existence.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'fi-LOS-uh-fyz (emphasis on second syllable)',
                'etymology': 'From Greek "philosophos" (lover of wisdom) + "-ize"',
                'memory_tips': 'Think "fill-osoph-eyes" - filling your eyes with wisdom through thinking',
                'alternate_spellings': 'theorize, speculate',
                'language_origin': 'Greek',
                'example_sentence': 'Students gathered in the coffee shop to _____ about the meaning of life.'
            },
            'philtrum': {
                'definition': 'The vertical groove or depression between the nose and upper lip in humans and some other mammals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FIL-truhm (emphasis on first syllable)',
                'etymology': 'From Greek "philtron" meaning "love potion", from the groove\'s resemblance to a potion channel',
                'memory_tips': 'Think "filter-rum" - the groove that filters what goes to your mouth',
                'alternate_spellings': 'nasal groove',
                'language_origin': 'Greek',
                'example_sentence': 'The plastic surgeon carefully reconstructed the patient\'s _____.'
            },
            'phishing': {
                'definition': 'The fraudulent practice of sending emails or messages purporting to be from reputable companies to steal personal information.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FISH-ing (emphasis on first syllable)',
                'etymology': 'Variant spelling of "fishing", referring to "fishing" for information',
                'memory_tips': 'Think "ph-ishing" - fishing with a "ph" for personal information',
                'alternate_spellings': 'cyber fraud, email scam',
                'language_origin': 'Modern English (internet slang)',
                'example_sentence': 'The company warned employees about _____ emails requesting login credentials.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_131_data:
            return batch_131_data[word_lower]
        
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
    
    def process_batch_131(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 131 with comprehensive Claude data"""
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
    
    def save_batch_131_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 131 processed words to CSV"""
        
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
    """Process Batch 131 with comprehensive Claude data"""
    processor = Batch131Processor()
    input_csv = Path("output/batch_131_words.csv")
    output_csv = Path("output/batch_131_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 131 with comprehensive Claude data...")
    
    # Process all words in batch 131
    processed_words = processor.process_batch_131(input_csv)
    
    # Save results
    processor.save_batch_131_csv(processed_words, output_csv)
    
    logger.info(f"Batch 131 processing completed!")
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