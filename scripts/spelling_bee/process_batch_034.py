#!/usr/bin/env python3
"""
Process Batch 034 of Spelling Bee Words with Comprehensive Claude Data
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

class Batch034Processor:
    """Processes Batch 034 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 034 words"""
        
        # Comprehensive data for all 50 words in Batch 034
        batch_034_data = {
            'chinese': {
                'definition': 'Relating to China, its people, or their language; the family of languages spoken by the Han Chinese, including Mandarin, Cantonese, and other dialects.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'chy-NEEZ (emphasis on second syllable)',
                'etymology': 'From "China" + "-ese", where China comes from Persian "Chīn"',
                'memory_tips': 'Think "shy-knees" - people from China who might be shy about showing their knees',
                'alternate_spellings': '',
                'language_origin': 'Persian (via China)',
                'example_sentence': 'The _____ restaurant served authentic dishes from various regions of China.'
            },
            'chinook': {
                'definition': 'A warm, dry wind that blows down the eastern slopes of the Rocky Mountains; a type of Pacific salmon; a Native American people of the Columbia River region.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'shuh-NOOK or chi-NOOK (emphasis on second syllable)',
                'etymology': 'From Chinook Jargon, ultimately from the Chinook people of the Pacific Northwest',
                'memory_tips': 'Think "she-nook" - a warm wind that creates a cozy nook',
                'alternate_spellings': '',
                'language_origin': 'Chinook (Native American)',
                'example_sentence': 'The _____ wind raised temperatures by thirty degrees in just a few hours.'
            },
            'chintzy': {
                'definition': 'Cheap and of poor quality; stingy or miserly; decorated with or resembling chintz fabric.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'CHINT-zee (emphasis on first syllable)',
                'etymology': 'From "chintz" (printed cotton fabric) + "-y", where chintz comes from Hindi "chīnt"',
                'memory_tips': 'Think "chin-tee" - cheap like a T-shirt that barely covers your chin',
                'alternate_spellings': '',
                'language_origin': 'Hindi (via chintz)',
                'example_sentence': 'The hotel\'s _____ decorations made the room feel cheap and unwelcoming.'
            },
            'chips': {
                'definition': 'Small pieces broken off from something larger; thin slices of potato fried until crisp; computer microprocessors; to break into small fragments.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'CHIPS (emphasis on single syllable)',
                'etymology': 'From Middle English "chippen" meaning "to cut, chop"',
                'memory_tips': 'Think of potato chips or wood chips - small pieces broken off',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'She enjoyed munching on _____ while watching the football game.'
            },
            'chisel': {
                'definition': 'A tool with a sharp blade for cutting or shaping wood, stone, or metal; to cut or shape with such a tool; to cheat or swindle (slang).',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'CHIZ-uhl (emphasis on first syllable)',
                'etymology': 'From Old French "cisel", from Late Latin "cisorium" (cutting tool)',
                'memory_tips': 'Think "cheese-el" - a tool that could cut cheese into precise shapes',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Late Latin)',
                'example_sentence': 'The sculptor used a fine _____ to add delicate details to the marble statue.'
            },
            'chives': {
                'definition': 'A small plant related to the onion, with thin leaves used as a herb for flavoring food, particularly in cooking.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'CHYVZ (emphasis on single syllable)',
                'etymology': 'From Old French "cive", from Latin "cepa" (onion)',
                'memory_tips': 'Think "shy-vz" - thin green herbs that are shy and delicate',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'She sprinkled fresh _____ over the baked potato for added flavor.'
            },
            'chlorofluorocarbon': {
                'definition': 'A synthetic chemical compound containing chlorine, fluorine, and carbon, once widely used in refrigeration and aerosol propellants but now restricted due to ozone depletion.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'klor-oh-floor-oh-KAR-bon (emphasis on fifth syllable)',
                'etymology': 'From "chloro-" (chlorine) + "fluoro-" (fluorine) + "carbon"',
                'memory_tips': 'Think "chloro-fluoro-carbon" - three chemical elements combined in one compound',
                'alternate_spellings': 'CFC (abbreviation)',
                'language_origin': 'Modern scientific (Greek/Latin elements)',
                'example_sentence': 'The Montreal Protocol banned _____ compounds to protect the ozone layer.'
            },
            'choctaws': {
                'definition': 'Members of a Native American people originally from the southeastern United States, now primarily in Oklahoma; the Choctaw language.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'CHOK-taws (emphasis on first syllable)',
                'etymology': 'From Choctaw "Chahta", the people\'s name for themselves',
                'memory_tips': 'Think "chock-taws" - like chocking or blocking with their toes',
                'alternate_spellings': '',
                'language_origin': 'Choctaw (Native American)',
                'example_sentence': 'The _____ Nation operates several successful businesses in southeastern Oklahoma.'
            },
            'cholera': {
                'definition': 'An infectious bacterial disease causing severe diarrhea and dehydration, often fatal if untreated, typically spread through contaminated water.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KOL-er-ah (emphasis on first syllable)',
                'etymology': 'From Latin "cholera", from Greek "kholera", from "khole" (bile)',
                'memory_tips': 'Think "collar-ah" - a disease that makes you say "ah" while holding your collar',
                'alternate_spellings': '',
                'language_origin': 'Greek (via Latin)',
                'example_sentence': 'The outbreak of _____ was quickly contained through improved sanitation measures.'
            },
            'cholesterol': {
                'definition': 'A waxy substance found in blood and cells, essential for normal body function but potentially harmful in excess, linked to heart disease.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'koh-LES-ter-ol (emphasis on second syllable)',
                'etymology': 'From Greek "khole" (bile) + "stereos" (solid) + "-ol" (alcohol)',
                'memory_tips': 'Think "coal-ester-all" - like coal that clogs up all your arteries',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The doctor recommended dietary changes to lower her _____ levels.'
            },
            'choose': {
                'definition': 'To pick out or select from a number of alternatives; to prefer or decide on; to make a choice.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'CHOOZ (emphasis on single syllable, rhymes with "news")',
                'etymology': 'From Old English "ceosan", from Proto-Germanic "*keusaną"',
                'memory_tips': 'Think "chews" - you chew on your options before you choose',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'You can _____ any book from the library shelf for your report.'
            },
            'chopine': {
                'definition': 'A tall platform shoe worn by women in 15th-17th century Europe, designed to protect clothing from mud and increase height.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'CHOH-peen or choh-PEEN (emphasis varies)',
                'etymology': 'From French "chopine", possibly from Spanish "chapín"',
                'memory_tips': 'Think "chop-een" - shoes so tall you might chop your shins',
                'alternate_spellings': 'chapin',
                'language_origin': 'French (possibly from Spanish)',
                'example_sentence': 'The museum displayed ornate _____ shoes that made Renaissance women appear much taller.'
            },
            'choreographer': {
                'definition': 'A person who creates and arranges dances and dance movements, especially for ballet, theater, or film performances.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kor-ee-OG-rah-fer (emphasis on third syllable)',
                'etymology': 'From Greek "khoreia" (dance) + "graphein" (to write)',
                'memory_tips': 'Think "core-ee-og-rapher" - someone who writes the core movements of dance',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ spent months creating the complex dance sequences for the Broadway musical.'
            },
            'chores': {
                'definition': 'Routine tasks or duties, especially household tasks; unpleasant or tedious work that must be done regularly.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'CHORS (emphasis on single syllable)',
                'etymology': 'From Middle English "chore", variant of "char" (task, job)',
                'memory_tips': 'Think "ch-ores" - tasks that make you say "ch!" because they\'re tedious',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The children were assigned weekly _____ to help maintain the household.'
            },
            'chorten': {
                'definition': 'A Tibetan Buddhist stupa or shrine, typically dome-shaped and containing relics, used for meditation and commemoration.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'CHOR-ten (emphasis on first syllable)',
                'etymology': 'From Tibetan "mchod rten", meaning "support for offerings"',
                'memory_tips': 'Think "choir-ten" - a place where ten choir members might gather to meditate',
                'alternate_spellings': '',
                'language_origin': 'Tibetan',
                'example_sentence': 'The ancient _____ stood majestically against the backdrop of the Himalayan mountains.'
            },
            'chortle': {
                'definition': 'To laugh in a gleeful or chuckling way; a gleeful chuckling laugh, originally coined by Lewis Carroll.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'CHOR-tuhl (emphasis on first syllable)',
                'etymology': 'Coined by Lewis Carroll, likely blending "chuckle" + "snort"',
                'memory_tips': 'Think "chuckle-snort" - the combination that makes a chortle',
                'alternate_spellings': '',
                'language_origin': 'Modern English (Lewis Carroll coinage)',
                'example_sentence': 'The comedian\'s joke made the audience _____ with delight.'
            },
            'chose': {
                'definition': 'Past tense of choose; selected or picked from alternatives; made a decision or preference.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'CHOHZ (emphasis on single syllable)',
                'etymology': 'Past tense of "choose", from Old English "ceosan"',
                'memory_tips': 'Think "chose-rose" - like a rose that was chosen from the garden',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She _____ the blue dress for the wedding ceremony.'
            },
            'choucroute': {
                'definition': 'French term for sauerkraut; a traditional Alsatian dish of sauerkraut cooked with wine and served with sausages and other meats.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'shoo-KROOT (emphasis on second syllable)',
                'etymology': 'From French, from Alsatian German "sūrkrūt" (sauerkraut)',
                'memory_tips': 'Think "shoe-croute" - sauerkraut that\'s as French as a fashionable shoe',
                'alternate_spellings': '',
                'language_origin': 'French (from Alsatian German)',
                'example_sentence': 'The restaurant\'s _____ garnie was served with bratwurst and juniper berries.'
            },
            'chowder': {
                'definition': 'A thick soup typically containing fish or shellfish, vegetables, and milk or cream, especially popular in New England.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'CHOW-der (emphasis on first syllable)',
                'etymology': 'Possibly from French "chaudière" (cauldron) or from "jowter" (fish peddler)',
                'memory_tips': 'Think "chow-der" - hearty food (chow) that\'s thick like powder',
                'alternate_spellings': '',
                'language_origin': 'Uncertain (possibly French)',
                'example_sentence': 'The creamy clam _____ was the restaurant\'s most popular soup.'
            },
            'christopher': {
                'definition': 'A masculine given name meaning "bearer of Christ"; Saint Christopher is the patron saint of travelers.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'KRIS-toh-fer (emphasis on first syllable)',
                'etymology': 'From Greek "Khristophoros", from "Khristos" (Christ) + "pherein" (to bear)',
                'memory_tips': 'Think "Christ-o-pher" - one who carries or bears Christ',
                'alternate_spellings': 'Kristopher, Chris',
                'language_origin': 'Greek',
                'example_sentence': 'Saint _____ is often depicted carrying the Christ child across a river.'
            },
            'chromosome': {
                'definition': 'A thread-like structure in cell nuclei that carries genetic information in the form of genes; humans typically have 46 chromosomes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KROH-muh-sohm (emphasis on first syllable)',
                'etymology': 'From Greek "khroma" (color) + "soma" (body), named for their staining properties',
                'memory_tips': 'Think "chrome-some" - shiny body-like structures that contain some of your genes',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Each _____ contains hundreds of genes that determine inherited traits.'
            },
            'chronometer': {
                'definition': 'A highly accurate timepiece, especially one used for navigation at sea to determine longitude; any precise timekeeping instrument.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kroh-NOM-uh-ter (emphasis on second syllable)',
                'etymology': 'From Greek "khronos" (time) + "metron" (measure)',
                'memory_tips': 'Think "chrono-meter" - a device that measures chronological time',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The ship\'s _____ was essential for accurate navigation across the ocean.'
            },
            'chrysalis': {
                'definition': 'The hard-shelled pupa of a butterfly or moth; the protective casing formed during metamorphosis; a transitional stage.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KRIS-uh-lis (emphasis on first syllable)',
                'etymology': 'From Greek "khrusalis", from "khrusos" (gold), referring to the golden color',
                'memory_tips': 'Think "chris-alice" - like Alice transforming in a golden cocoon',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The caterpillar formed a _____ and emerged weeks later as a beautiful butterfly.'
            },
            'chrysolite': {
                'definition': 'A yellowish-green gemstone, specifically the mineral olivine when used as a gem; also called peridot.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KRIS-uh-lyt (emphasis on first syllable)',
                'etymology': 'From Greek "khrusos" (gold) + "lithos" (stone)',
                'memory_tips': 'Think "crystal-light" - a crystal that shines with golden-green light',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The ancient _____ pendant gleamed with a distinctive olive-green hue.'
            },
            'chuckle': {
                'definition': 'To laugh quietly or inwardly; a quiet or restrained laugh, typically expressing amusement or satisfaction.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'CHUK-uhl (emphasis on first syllable)',
                'etymology': 'Imitative word, possibly related to "chuck" (to make clucking sounds)',
                'memory_tips': 'Think "chuck-ul" - like chucking out a little laugh',
                'alternate_spellings': '',
                'language_origin': 'Imitative (English)',
                'example_sentence': 'She couldn\'t help but _____ at her dog\'s silly antics in the yard.'
            },
            'chugged': {
                'definition': 'Past tense of chug; moved with regular puffing sounds; drank something quickly in large gulps.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'CHUGD (emphasis on single syllable)',
                'etymology': 'Imitative word representing the sound of an engine or rapid drinking',
                'memory_tips': 'Think of a train that chugged along the tracks or someone who chugged a drink',
                'alternate_spellings': '',
                'language_origin': 'Imitative (English)',
                'example_sentence': 'The old train _____ slowly up the steep mountain grade.'
            },
            'chugggged': {
                'definition': '[SPELLING ERROR] This appears to be a misspelling of "chugged" with extra letters. The correct spelling is "chugged" (past tense of chug).',
                'part_of_speech': 'error - misspelled word',
                'pronunciation_guide': '[PRONUNCIATION ERROR - MISSPELLED WORD]',
                'etymology': '[ETYMOLOGY ERROR - MISSPELLED WORD]',
                'memory_tips': 'This is a spelling error - the correct word is "chugged" with only two "g"s',
                'alternate_spellings': 'chugged (correct spelling)',
                'language_origin': 'ERROR - misspelled word',
                'example_sentence': '[ERROR - This misspelled word should not appear in spelling bee materials]'
            },
            'chunks': {
                'definition': 'Thick pieces or lumps of something; portions or parts broken off; segments or blocks of data or information.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'CHUNKS (emphasis on single syllable)',
                'etymology': 'From "chunk", possibly from "chuck" (to throw) or imitative',
                'memory_tips': 'Think of chunky peanut butter or chunks of chocolate in cookies',
                'alternate_spellings': '',
                'language_origin': 'Uncertain (possibly imitative)',
                'example_sentence': 'She added _____ of pineapple to the fruit salad for extra texture.'
            },
            'chupacabra': {
                'definition': 'A legendary cryptid from Latin American folklore, described as a reptilian creature that allegedly attacks livestock and drains their blood.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'choo-pah-KAH-brah (emphasis on third syllable)',
                'etymology': 'From Spanish "chupar" (to suck) + "cabra" (goat), literally "goat-sucker"',
                'memory_tips': 'Think "chew-pah-cabra" - a creature that chews on goats',
                'alternate_spellings': '',
                'language_origin': 'Spanish',
                'example_sentence': 'The mysterious livestock deaths were blamed on the legendary _____.'
            },
            'chupacabraacadians': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "chupacabra" (legendary creature) + "Acadians" (French colonists).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "chupacabra" and "Acadians"',
                'alternate_spellings': 'chupacabra + Acadians (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'chupacabradifficulty': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "chupacabra" (legendary creature) + "difficulty" (hardship).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "chupacabra" and "difficulty"',
                'alternate_spellings': 'chupacabra + difficulty (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'churchianity': {
                'definition': 'A pejorative term describing formal, institutional Christianity that emphasizes church attendance and rituals over genuine faith and spiritual relationship.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'church-ee-AN-ih-tee (emphasis on third syllable)',
                'etymology': 'Blend of "church" + "Christianity", coined to distinguish institutional religion from personal faith',
                'memory_tips': 'Think "church-insanity" - focusing too much on church buildings rather than faith',
                'alternate_spellings': '',
                'language_origin': 'Modern English (blend word)',
                'example_sentence': 'The pastor warned against _____ that replaces genuine faith with mere ritual.'
            },
            'churlish': {
                'definition': 'Rude, surly, and mean-spirited; lacking courtesy or graciousness; ungraciously uncooperative.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'CHUR-lish (emphasis on first syllable)',
                'etymology': 'From "churl" (peasant, boor) + "-ish", where churl comes from Old English "ceorl"',
                'memory_tips': 'Think "churl-ish" - acting like a rude peasant or boor',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'His _____ behavior at the dinner party embarrassed his family.'
            },
            'churned': {
                'definition': 'Past tense of churn; agitated or stirred vigorously; moved in a turbulent manner; produced by churning.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'CHURND (emphasis on single syllable)',
                'etymology': 'From Old English "cyrin" meaning "to churn, turn"',
                'memory_tips': 'Think of butter being churned or waves that churned the sea',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The storm _____ the ocean waves into towering peaks of foam.'
            },
            'churros': {
                'definition': 'A Spanish and Mexican pastry made of fried dough shaped into long ridged strips, often dusted with cinnamon sugar.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'CHOOR-ohs (emphasis on first syllable)',
                'etymology': 'From Spanish "churro", possibly from the sound of frying or from shepherd\'s staff shape',
                'memory_tips': 'Think "chew-ros" - delicious fried pastries you chew with pleasure',
                'alternate_spellings': '',
                'language_origin': 'Spanish',
                'example_sentence': 'The street vendor served hot _____ dusted with cinnamon and sugar.'
            },
            'chute': {
                'definition': 'A sloping channel or slide for moving things from a higher to lower level; a parachute; a narrow passage.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SHOOT (emphasis on single syllable)',
                'etymology': 'From French "chute" (fall), from "choir" (to fall)',
                'memory_tips': 'Think "shoot" - things shoot down a chute rapidly',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The laundry _____ made it easy to send clothes from the second floor to the basement.'
            },
            'château': {
                'definition': 'A French castle or large country house; a wine estate, especially in the Bordeaux region; an imposing residence.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'sha-TOH (emphasis on second syllable)',
                'etymology': 'From French "château", from Latin "castellum" (castle)',
                'memory_tips': 'Think "chat-oh" - a fancy place where French people chat over wine',
                'alternate_spellings': 'chateau (without accent)',
                'language_origin': 'French (from Latin)',
                'example_sentence': 'The wine _____ offered tours of its historic cellars and vineyards.'
            },
            'chèvre': {
                'definition': 'French word for goat; a type of soft cheese made from goat\'s milk, popular in French cuisine.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SHEV-ruh (emphasis on first syllable)',
                'etymology': 'From French "chèvre" (goat), from Latin "capra" (goat)',
                'memory_tips': 'Think "shave-ruh" - goat cheese so smooth it feels like you shaved it',
                'alternate_spellings': 'chevre (without accent)',
                'language_origin': 'French (from Latin)',
                'example_sentence': 'The salad was topped with crumbled _____ cheese and toasted walnuts.'
            },
            'ciao': {
                'definition': 'An Italian word used as both a greeting and farewell; informally used in English to say hello or goodbye.',
                'part_of_speech': 'interjection',
                'pronunciation_guide': 'CHOW (emphasis on single syllable)',
                'etymology': 'From Italian "ciao", from Venetian "sciào", contraction of "schiavo" (slave, servant)',
                'memory_tips': 'Think "chow" - saying goodbye before going to eat chow (food)',
                'alternate_spellings': '',
                'language_origin': 'Italian (from Venetian)',
                'example_sentence': 'She waved and called out "____!" as she left the café.'
            },
            'cicada': {
                'definition': 'A large insect with transparent wings that produces a loud buzzing sound, especially during hot weather; males create the sound to attract mates.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'sih-KAY-dah (emphasis on second syllable)',
                'etymology': 'From Latin "cicada" (tree cricket), possibly imitative of their sound',
                'memory_tips': 'Think "see-kay-da" - you see and hear these noisy insects in summer',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ chorus grew louder as the afternoon temperature rose.'
            },
            'cicatrize': {
                'definition': 'To heal by forming scar tissue; to form a cicatrix (scar); the process of wound healing through scarring.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'SIK-uh-tryz (emphasis on first syllable)',
                'etymology': 'From Latin "cicatriz" (scar) + "-ize"',
                'memory_tips': 'Think "sick-a-tries" - when sick tissue tries to heal by forming scars',
                'alternate_spellings': 'cicatrise (British spelling)',
                'language_origin': 'Latin',
                'example_sentence': 'The deep wound took several months to _____ completely.'
            },
            'cicerone': {
                'definition': 'A guide who gives information about antiquities and places of interest to sightseers; any knowledgeable guide.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'sis-uh-ROH-nee or chee-che-ROH-nay (emphasis on third syllable)',
                'etymology': 'From Italian, named after the Roman orator Cicero, known for his eloquence',
                'memory_tips': 'Think "sister-own-ee" - like a sister who owns all the knowledge about tourist sites',
                'alternate_spellings': '',
                'language_origin': 'Italian (from Latin proper name)',
                'example_sentence': 'The knowledgeable _____ led the tourists through the ancient Roman ruins.'
            },
            'cidery': {
                'definition': 'Having the taste, smell, or characteristics of cider; relating to or resembling fermented apple juice.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'SY-der-ee (emphasis on first syllable)',
                'etymology': 'From "cider" + "-y", where cider comes from Old French "cidre"',
                'memory_tips': 'Think "cider-y" - having the qualities of apple cider',
                'alternate_spellings': '',
                'language_origin': 'Old French (via cider)',
                'example_sentence': 'The autumn air had a _____ scent of fermented apples.'
            },
            'cienega': {
                'definition': 'A marshy area where a stream disappears into sandy soil; a type of wetland found in arid regions of the southwestern United States.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'see-EN-eh-gah (emphasis on second syllable)',
                'etymology': 'From Spanish "ciénaga" (swamp, marsh), from "cien" (hundred) + "agua" (water)',
                'memory_tips': 'Think "see-a-new-gah" - seeing a new type of wetland in the desert',
                'alternate_spellings': 'ciénaga',
                'language_origin': 'Spanish',
                'example_sentence': 'The desert _____ provided a crucial water source for wildlife in the region.'
            },
            'ciliopathy': {
                'definition': 'A medical condition caused by defects in cellular cilia, the hair-like structures that help cells move and sense their environment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'sil-ee-OP-ah-thee (emphasis on third syllable)',
                'etymology': 'From Latin "cilium" (eyelash) + Greek "pathos" (disease)',
                'memory_tips': 'Think "silly-op-a-thee" - a disease affecting silly little hair-like parts of cells',
                'alternate_spellings': '',
                'language_origin': 'Modern medical (Latin/Greek)',
                'example_sentence': 'The researcher studied various forms of _____ to understand cellular function.'
            },
            'cincinnati': {
                'definition': 'A major city in southwestern Ohio, situated on the Ohio River; named after the Roman dictator Cincinnatus.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'sin-sin-NAT-ee (emphasis on third syllable)',
                'etymology': 'Named after the Society of Cincinnati, which honored the Roman leader Lucius Quinctius Cincinnatus',
                'memory_tips': 'Think "sin-sin-not-ee" - a city where there\'s not much sin, just friendly people',
                'alternate_spellings': '',
                'language_origin': 'Latin (from Roman name)',
                'example_sentence': 'The historic riverfront in _____ offers beautiful views of the Ohio River.'
            },
            'cinderella': {
                'definition': 'The title character of a famous fairy tale who transforms from servitude to royalty; someone or something that achieves unexpected success.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'sin-der-EL-ah (emphasis on third syllable)',
                'etymology': 'From French "Cendrillon", from "cendre" (ashes) + diminutive suffix',
                'memory_tips': 'Think "cinder-ella" - Ella who worked among the cinders and ashes',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The small college team was the _____ story of the basketball tournament.'
            },
            'cinematic': {
                'definition': 'Relating to movies or filmmaking; having qualities characteristic of films, such as visual drama or storytelling techniques.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'sin-uh-MAT-ik (emphasis on third syllable)',
                'etymology': 'From "cinema" + "-atic", where cinema comes from Greek "kinema" (movement)',
                'memory_tips': 'Think "cinema-matic" - automatically relating to cinema and movies',
                'alternate_spellings': '',
                'language_origin': 'Greek (via cinema)',
                'example_sentence': 'The sunset created a _____ backdrop for the outdoor wedding ceremony.'
            },
            'cinerariumpolemic': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "cinerarium" (urn for ashes) + "polemic" (controversial argument).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "cinerarium" and "polemic"',
                'alternate_spellings': 'cinerarium + polemic (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'cinnamon': {
                'definition': 'A sweet spice obtained from the inner bark of certain trees, commonly used in cooking and baking; the reddish-brown color of this spice.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'SIN-ah-muhn (emphasis on first syllable)',
                'etymology': 'From Greek "kinnamomon", possibly from a Semitic language',
                'memory_tips': 'Think "sin-a-man" - a spice so good it\'s sinful, loved by every man',
                'alternate_spellings': '',
                'language_origin': 'Greek (possibly from Semitic)',
                'example_sentence': 'She sprinkled _____ on top of the hot apple pie before serving.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_034_data:
            return batch_034_data[word_lower]
        
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
    
    def process_batch_034(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 034 with comprehensive Claude data"""
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
    
    def save_batch_034_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 034 processed words to CSV"""
        
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
    """Process Batch 034 with comprehensive Claude data"""
    processor = Batch034Processor()
    input_csv = Path("output/batch_034_words.csv")
    output_csv = Path("output/batch_034_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 034 with comprehensive Claude data...")
    
    # Process all words in batch 034
    processed_words = processor.process_batch_034(input_csv)
    
    # Save results
    processor.save_batch_034_csv(processed_words, output_csv)
    
    logger.info(f"Batch 034 processing completed!")
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