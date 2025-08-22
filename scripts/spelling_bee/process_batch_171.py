#!/usr/bin/env python3
"""
Process Batch 171 of Spelling Bee Words with Comprehensive Claude Data
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
            'government', 'company', 'number', 'group', 'problem', 'fact', 'such', 'sudden', 'suffer', 'suffering', 'sugar', 'successful'
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
            'mega', 'micro', 'mini', 'multi', 'neo', 'pseudo', 'ultra', 'ac', 'ad', 'con', 'strat',
            'str', 'st', 'succ', 'suc', 'suf'
        ]
        
        # Common suffixes
        suffixes = [
            'ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment', 'able', 'ible',
            'ful', 'less', 'ous', 'ious', 'al', 'ic', 'ical', 'ism', 'ist', 'ize', 'ise',
            'fy', 'ward', 'wise', 'like', 'ship', 'hood', 'dom', 'age', 'ery', 'ary', 'ate',
            'oid', 'ary', 'ery', 'ity', 'ship', 'ness', 'ure', 'ency', 'tic', 'ive', 'ent',
            'ance', 'ence', 'ade', 'inct', 'ulent', 'umb', 'usion', 'ès', 'ation'
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

class Batch171Processor:
    """Processes Batch 171 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 171 words"""
        
        # Comprehensive data for all 50 words in Batch 171
        batch_171_data = {
            'subdued': {
                'definition': 'Quiet and rather reflective or depressed; lacking in energy or vitality; (of color, sound, lighting) soft and restrained. Can describe emotional states, physical behavior, or sensory qualities that are muted rather than intense or vibrant.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'suhb-DOOD (emphasis on second syllable)',
                'etymology': 'Past participle of "subdue," from Latin "subducere" meaning "to withdraw, remove"',
                'memory_tips': 'Think "sub-dued" - under control, not showing excitement',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The normally energetic child seemed _____ after the disappointing news.'
            },
            'subjugate': {
                'definition': 'To bring under domination or control, especially by conquest; to make subservient; to defeat and bring under complete control. Often used in contexts of military conquest, political oppression, or psychological domination.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'SUB-juh-gayt (emphasis on first syllable)',
                'etymology': 'From Latin "subjugatus," past participle of "subjugare," from "sub" (under) + "jugum" (yoke)',
                'memory_tips': 'Think "sub-jug-ate" - to put someone under the yoke like oxen',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The empire sought to _____ all neighboring territories through military force.'
            },
            'subliminal': {
                'definition': 'Below the threshold of conscious perception; influencing the mind without being consciously noticed. Refers to stimuli that affect behavior or emotions without the person being aware of the influence.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'suhb-LIM-uh-nuhl (emphasis on second syllable)',
                'etymology': 'From Latin "sub" (below) + "limen" (threshold) + "-al"',
                'memory_tips': 'Think "sub-liminal" - below the limit of conscious awareness',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The advertisement contained _____ messages designed to influence purchasing decisions.'
            },
            'subliminalsubluxated': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "subliminal" (below conscious perception) + "subluxated" (partially dislocated). This is a data processing error that should be corrected.',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "subliminal" and "subluxated"',
                'alternate_spellings': 'subliminal + subluxated (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'subluxated': {
                'definition': 'Partially dislocated; having undergone subluxation, which is an incomplete or partial dislocation of a joint. In chiropractic terminology, refers to a misalignment of vertebrae that may interfere with nervous system function.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'suhb-LUHK-say-ted (emphasis on second syllable)',
                'etymology': 'From "subluxation," from Latin "sub" (partially) + "luxatus" (dislocated)',
                'memory_tips': 'Think "sub-luxated" - partially out of place, not fully dislocated',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The chiropractor identified several _____ vertebrae in the patient\'s spine.'
            },
            'submerged': {
                'definition': 'Completely covered by water or another liquid; hidden or concealed beneath the surface; overwhelmed or absorbed completely in an activity or state of mind.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'suhb-MURJD (emphasis on second syllable)',
                'etymology': 'Past participle of "submerge," from Latin "submergere," from "sub" (under) + "mergere" (to plunge)',
                'memory_tips': 'Think "sub-merged" - merged completely under water',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The ancient ruins remained _____ beneath the lake for centuries.'
            },
            'submersible': {
                'definition': 'Capable of being submerged; a vessel designed to operate underwater, typically smaller and less complex than a submarine. Used for deep-sea research, exploration, and underwater construction work.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'suhb-MUR-suh-buhl (emphasis on second syllable)',
                'etymology': 'From "submerse" + "-ible," from Latin "submersus"',
                'memory_tips': 'Think "sub-mersible" - able to be submerged under water',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The research team used a deep-sea _____ to explore the ocean trench.'
            },
            'submitted': {
                'definition': 'Past tense of submit; presented for consideration or approval; yielded to authority or control; gave in to pressure or force.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'suhb-MIT-ed (emphasis on second syllable)',
                'etymology': 'Past tense of "submit," from Latin "submittere," from "sub" (under) + "mittere" (to send)',
                'memory_tips': 'Think "sub-mitted" - sent under someone else\'s authority',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She _____ her research proposal to the academic committee for review.'
            },
            'subrident': {
                'definition': 'Smiling in a subtle or restrained manner; having a faint or suppressed smile. This rare word describes a gentle, understated expression of amusement or pleasure.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'suhb-RY-dent (emphasis on second syllable)',
                'etymology': 'From Latin "sub" (under, slightly) + "ridens" (smiling), from "ridere" (to laugh)',
                'memory_tips': 'Think "sub-rident" - smiling subtly, not fully grinning',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Her _____ expression suggested she knew something amusing that others didn\'t.'
            },
            'subridentethylene': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "subrident" (smiling subtly) + "ethylene" (a chemical compound). This is a data processing error that should be corrected.',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "subrident" and "ethylene"',
                'alternate_spellings': 'subrident + ethylene (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'subsequent': {
                'definition': 'Coming after something in time; following in time or order; occurring or existing later or after something else.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'SUHB-si-kwuhnt (emphasis on first syllable)',
                'etymology': 'From Latin "subsequens," from "sub" (close to) + "sequi" (to follow)',
                'memory_tips': 'Think "sub-sequent" - following in sequence',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The initial meeting went well, and _____ negotiations proceeded smoothly.'
            },
            'subservient': {
                'definition': 'Prepared to obey others unquestioningly; servile; less important than something else; subordinate. Often implies excessive willingness to please or comply with others\' wishes.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'suhb-SUR-vee-uhnt (emphasis on second syllable)',
                'etymology': 'From Latin "subserviens," from "sub" (under) + "servire" (to serve)',
                'memory_tips': 'Think "sub-servient" - serving under someone else\'s authority',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The dictator demanded that all citizens remain completely _____ to his authority.'
            },
            'subsidence': {
                'definition': 'The gradual caving in or sinking of an area of land; the process of becoming less intense, active, or severe. Can refer to geological phenomena or the abating of conditions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'suhb-SY-duhnts (emphasis on second syllable)',
                'etymology': 'From Latin "subsidere," from "sub" (down) + "sidere" (to settle)',
                'memory_tips': 'Think "sub-sidence" - sinking down below the surface',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Mining activities caused significant _____ in the surrounding neighborhood.'
            },
            'subsistence': {
                'definition': 'The action or fact of maintaining or supporting oneself at a minimum level; the means of securing the necessities of life. Often refers to basic survival rather than comfortable living.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'suhb-SIS-tuhnts (emphasis on second syllable)',
                'etymology': 'From Latin "subsistentia," from "subsistere," meaning "to stand firm, exist"',
                'memory_tips': 'Think "sub-sistence" - existing at the most basic level',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The farmer practiced _____ agriculture, growing just enough food for his family.'
            },
            'substance': {
                'definition': 'A particular kind of matter with uniform properties; the real physical matter of which a thing consists; the essential nature or most important quality of something.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUHB-stuhnts (emphasis on first syllable)',
                'etymology': 'From Latin "substantia," from "substare," meaning "to stand under, exist"',
                'memory_tips': 'Think "sub-stance" - what stands under or supports something',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The scientist analyzed the chemical composition of the unknown _____.'
            },
            'substantial': {
                'definition': 'Of considerable importance, size, or worth; strongly built or made; having substance rather than being superficial. Implies significance, solidity, or meaningful content.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'suhb-STAN-shuhl (emphasis on second syllable)',
                'etymology': 'From Latin "substantialis," from "substantia" (substance)',
                'memory_tips': 'Think "sub-stantial" - having real substance, not superficial',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The charity received a _____ donation that would fund programs for years.'
            },
            'substitute': {
                'definition': 'A person or thing acting or serving in place of another; to put or use something in place of another. Can be temporary or permanent replacement.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'SUHB-sti-toot (emphasis on first syllable)',
                'etymology': 'From Latin "substitutus," from "sub" (in place of) + "statuere" (to set up)',
                'memory_tips': 'Think "sub-stitute" - someone who stands in substitution',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ teacher did an excellent job covering the regular instructor\'s classes.'
            },
            'substrate': {
                'definition': 'An underlying substance or layer; the surface or material on which an organism lives or grows; in biochemistry, a molecule upon which an enzyme acts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUHB-strayt (emphasis on first syllable)',
                'etymology': 'From Latin "substratus," from "sub" (under) + "sternere" (to spread)',
                'memory_tips': 'Think "sub-strate" - the layer that lies under something else',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The enzyme broke down the _____ into simpler molecular components.'
            },
            'subterranean': {
                'definition': 'Existing, occurring, or done under the earth\'s surface; secret or hidden. Can describe underground spaces, covert activities, or concealed aspects of society.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'suhb-tuh-RAY-nee-uhn (emphasis on third syllable)',
                'etymology': 'From Latin "subterraneus," from "sub" (under) + "terra" (earth)',
                'memory_tips': 'Think "sub-terranean" - under the terrain or earth',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The ancient city featured an extensive network of _____ tunnels and chambers.'
            },
            'subtitles': {
                'definition': 'Captions displayed at the bottom of a movie or television screen that translate or transcribe the dialogue; secondary or explanatory titles of books or other works.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'SUHB-ty-tuhlz (emphasis on first syllable)',
                'etymology': 'From "sub" (under) + "titles," indicating text that appears under the main content',
                'memory_tips': 'Think "sub-titles" - titles that appear under the main action',
                'alternate_spellings': '',
                'language_origin': 'English (compound)',
                'example_sentence': 'The foreign film had English _____ so viewers could understand the dialogue.'
            },
            'subtlety': {
                'definition': 'The quality of being subtle; delicacy and exactness of perception, discrimination, or expression; something that is subtle, especially a fine distinction in meaning or expression.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUHT-uhl-tee (emphasis on first syllable)',
                'etymology': 'From "subtle" + "-ty," from Latin "subtilis" meaning "fine, delicate"',
                'memory_tips': 'Think "subtle-ty" - the quality of being subtle and refined',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The artist\'s _____ in using color created a painting of remarkable depth and beauty.'
            },
            'subversive': {
                'definition': 'Seeking or intended to subvert an established system or institution; tending to overthrow or undermine. Often describes ideas, actions, or people that challenge authority.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'suhb-VUR-siv (emphasis on second syllable)',
                'etymology': 'From Latin "subversus," from "sub" (under) + "vertere" (to turn)',
                'memory_tips': 'Think "sub-versive" - turning things upside down from underneath',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The government considered his political writings to be dangerously _____.'
            },
            'subway': {
                'definition': 'An underground electric railroad; an underground tunnel or passage, especially for pedestrians. In American usage, typically refers to urban rapid transit systems.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUHB-way (emphasis on first syllable)',
                'etymology': 'From "sub" (under) + "way," indicating an underground passage',
                'memory_tips': 'Think "sub-way" - a way that goes under the ground',
                'alternate_spellings': '',
                'language_origin': 'English (compound)',
                'example_sentence': 'She took the _____ downtown to avoid the heavy surface traffic.'
            },
            'succade': {
                'definition': 'Fruit preserved in sugar; candied fruit, especially candied citrus peel. A traditional confection made by cooking fruit in heavy sugar syrup until it crystallizes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'suh-KAYD (emphasis on second syllable)',
                'etymology': 'From French "succade," from Italian "succata," from "succo" (juice)',
                'memory_tips': 'Think "suc-cade" - sweet juice preserved in sugar',
                'alternate_spellings': '',
                'language_origin': 'French via Italian',
                'example_sentence': 'The traditional recipe called for _____ made from orange and lemon peels.'
            },
            'successful': {
                'definition': 'Accomplishing an aim or purpose; having achieved fame, wealth, or social status; resulting in or having achieved success.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'suhk-SES-fuhl (emphasis on second syllable)',
                'etymology': 'From "success" + "-ful," from Latin "successus" (a good result)',
                'memory_tips': 'Think "success-ful" - full of success and achievement',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ entrepreneur built a business empire from humble beginnings.'
            },
            'successive': {
                'definition': 'Following each other in uninterrupted succession or order; consecutive; characterized by regular sequence without interruption.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'suhk-SES-iv (emphasis on second syllable)',
                'etymology': 'From Latin "successivus," from "succedere" (to come after)',
                'memory_tips': 'Think "success-ive" - following in successful sequence',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The team won five _____ championships, setting a new league record.'
            },
            'succinct': {
                'definition': 'Briefly and clearly expressed; characterized by brevity and clarity; concise without being incomplete.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'suhk-SINGKT (emphasis on second syllable)',
                'etymology': 'From Latin "succinctus," from "sub" (up) + "cingere" (to gird)',
                'memory_tips': 'Think "suc-cinct" - success in being concise and clear',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Her _____ presentation covered all the key points in just ten minutes.'
            },
            'succorance': {
                'definition': 'Assistance in time of distress; aid or relief given to someone in need. A formal or archaic term for help provided during difficult circumstances.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUHK-er-uhnts (emphasis on first syllable)',
                'etymology': 'From Old French "socours," from Latin "succurrere," meaning "to run to help"',
                'memory_tips': 'Think "succo-rance" - assistance that runs to help inrance (France)',
                'alternate_spellings': 'succour (British), succourance',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The refugees received _____ from humanitarian organizations during the crisis.'
            },
            'succourance': {
                'definition': 'Alternative spelling of succorance; assistance in time of distress; aid or relief given to someone in need. This variant spelling emphasizes the act of providing help.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUHK-er-uhnts (emphasis on first syllable)',
                'etymology': 'Variant of "succorance," from Latin "succurrere" (to run to help)',
                'memory_tips': 'Think "succourance" - assistance that encourages and helps',
                'alternate_spellings': 'succorance, succour',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The charity provided _____ to families affected by the natural disaster.'
            },
            'succulent': {
                'definition': 'Tender, juicy, and tasty; (of plants) having thick fleshy leaves or stems adapted to storing water; rich and satisfying.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'SUHK-yuh-luhnt (emphasis on first syllable)',
                'etymology': 'From Latin "succulentus," from "succus" meaning "juice"',
                'memory_tips': 'Think "succ-ulent" - full of juice and success in taste',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ roast beef was perfectly cooked and incredibly flavorful.'
            },
            'succumb': {
                'definition': 'To fail to resist pressure, temptation, or some other negative force; to die from the effect of a disease or injury; to yield or give way.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'suh-KUHM (emphasis on second syllable)',
                'etymology': 'From Latin "succumbere," from "sub" (under) + "cubare" (to lie down)',
                'memory_tips': 'Think "suc-cumb" - to lie down under pressure and give up',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Despite her strong resistance, she finally began to _____ to the illness.'
            },
            'succussion': {
                'definition': 'A shaking or jolting motion; in medicine, a method of detecting fluid in body cavities by shaking the patient and listening for sounds.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'suh-KUHSH-uhn (emphasis on second syllable)',
                'etymology': 'From Latin "succussio," from "succutere," meaning "to shake up"',
                'memory_tips': 'Think "suc-cussion" - shaking like a concussion',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The doctor used _____ to detect the presence of fluid in the patient\'s chest cavity.'
            },
            'succès': {
                'definition': 'French word meaning success; triumph or achievement. Sometimes used in English in phrases like "succès d\'estime" (critical success) or "succès de scandale" (success due to controversy).',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'sük-SEH (French pronunciation with silent "s")',
                'etymology': 'French word from Latin "successus" meaning "a good result"',
                'memory_tips': 'Think "succès" - French for success with an accent',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The controversial novel was a _____ de scandale, selling millions of copies.'
            },
            'such': {
                'definition': 'Of the type previously mentioned; of the same class, type, or degree; used to emphasize the extent or degree of something.',
                'part_of_speech': 'determiner, pronoun, adverb',
                'pronunciation_guide': 'SUHCH (rhymes with "much")',
                'etymology': 'From Old English "swylc," from "swa" (so) + "lic" (like)',
                'memory_tips': 'Think "such" - sounds like "much," both express degree',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'I have never seen _____ a beautiful sunset in all my years of travel.'
            },
            'sudation': {
                'definition': 'The process of sweating; perspiration; the act of producing and secreting sweat through the pores of the skin.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'soo-DAY-shuhn (emphasis on second syllable)',
                'etymology': 'From Latin "sudatio," from "sudare" meaning "to sweat"',
                'memory_tips': 'Think "sud-ation" - the process of producing sweat suds',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The intense heat caused excessive _____ among the marathon runners.'
            },
            'sudden': {
                'definition': 'Occurring or done quickly and unexpectedly; abrupt; happening without warning or preparation.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'SUHD-uhn (emphasis on first syllable)',
                'etymology': 'From Latin "subitaneus," from "subitus" meaning "unexpected"',
                'memory_tips': 'Think "sud-den" - happening so fast you\'re suddenly in a den of surprise',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ thunderstorm caught the hikers completely unprepared.'
            },
            'sudoku': {
                'definition': 'A number puzzle consisting of a 9×9 grid partially filled with digits, where the player must complete the grid so each row, column, and 3×3 section contains all digits 1-9.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'suh-DOH-koo (emphasis on second syllable)',
                'etymology': 'From Japanese "sudoku," short for "suji wa dokushin ni kagiru" (numbers must be single/bachelor)',
                'memory_tips': 'Think "su-doku" - a single (su) number goes in each spot',
                'alternate_spellings': '',
                'language_origin': 'Japanese',
                'example_sentence': 'She enjoyed solving the daily _____ puzzle in the newspaper during breakfast.'
            },
            'sudsy': {
                'definition': 'Full of or covered with suds; foamy with soap bubbles; frothy with detergent foam.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'SUHD-zee (emphasis on first syllable)',
                'etymology': 'From "suds" (soap foam) + "-y" suffix',
                'memory_tips': 'Think "suds-y" - having the quality of sudsy soap bubbles',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The children laughed as they played in the _____ bath water.'
            },
            'suet': {
                'definition': 'Hard fat around the kidneys and loins in beef and mutton, used in cooking and for feeding birds; a solid fat used in traditional cooking and baking.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SOO-it (emphasis on first syllable)',
                'etymology': 'From Old French "sieu," from Latin "sebum" meaning "tallow, grease"',
                'memory_tips': 'Think "su-et" - a sweet fat used in cooking',
                'alternate_spellings': '',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The traditional Christmas pudding recipe called for chopped _____ and dried fruits.'
            },
            'suffer': {
                'definition': 'To experience or be subjected to something bad or unpleasant; to undergo pain, distress, or hardship; to tolerate or allow.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'SUHF-ur (emphasis on first syllable)',
                'etymology': 'From Latin "sufferre," from "sub" (under) + "ferre" (to bear)',
                'memory_tips': 'Think "suf-fer" - to bear suffering under difficult circumstances',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The patient continued to _____ from chronic pain despite various treatments.'
            },
            'suffering': {
                'definition': 'The state of undergoing pain, distress, or hardship; an instance or period of pain or distress.',
                'part_of_speech': 'noun, verb (present participle)',
                'pronunciation_guide': 'SUHF-ur-ing (emphasis on first syllable)',
                'etymology': 'Present participle of "suffer," from Latin "sufferre"',
                'memory_tips': 'Think "suffer-ing" - currently experiencing suffering',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The humanitarian organization worked to alleviate human _____ around the world.'
            },
            'suffice': {
                'definition': 'To be enough or adequate; to meet the needs of a situation or proposed end; to satisfy requirements.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'suh-FYSS (emphasis on second syllable)',
                'etymology': 'From Latin "sufficere," from "sub" (under) + "facere" (to make)',
                'memory_tips': 'Think "suf-fice" - sufficient to make do',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'A simple apology will not _____ for such a serious mistake.'
            },
            'sufficiency': {
                'definition': 'The condition of being sufficient; an adequate amount or supply; the quality of being enough to meet needs or requirements.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'suh-FISH-uhn-see (emphasis on second syllable)',
                'etymology': 'From Latin "sufficientia," from "sufficere" (to be enough)',
                'memory_tips': 'Think "suffici-ency" - the state of being sufficient',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The food bank strived to achieve _____ in their emergency relief supplies.'
            },
            'suffix': {
                'definition': 'A morpheme added at the end of a word to form a derivative; an addition or appendage to the end of something.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'SUHF-iks (emphasis on first syllable)',
                'etymology': 'From Latin "suffixus," from "sub" (under) + "figere" (to fasten)',
                'memory_tips': 'Think "suf-fix" - something fixed at the end (suf-ter)',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Adding the _____ "-ly" to "quick" creates the adverb "quickly."'
            },
            'suffocate': {
                'definition': 'To kill or be killed by depriving of air or preventing breathing; to feel trapped and restricted; to suppress or constrain.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'SUHF-uh-kayt (emphasis on first syllable)',
                'etymology': 'From Latin "suffocare," from "sub" (under) + "fauces" (throat)',
                'memory_tips': 'Think "suf-focate" - to choke off air from under the throat',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The thick smoke began to _____ the firefighters trapped in the building.'
            },
            'suffrage': {
                'definition': 'The right to vote in political elections; the exercise of such a right; a vote given in deciding a disputed question.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUHF-rij (emphasis on first syllable)',
                'etymology': 'From Latin "suffragium," from "suffragari" (to vote for, support)',
                'memory_tips': 'Think "suf-frage" - the right to cast votes and support candidates',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The women\'s _____ movement fought for decades to secure voting rights for women.'
            },
            'suffused': {
                'definition': 'Gradually spread through or over; permeated or saturated with something, especially light, color, or feeling.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'suh-FYOOZD (emphasis on second syllable)',
                'etymology': 'Past participle of "suffuse," from Latin "suffusus," from "sub" (under) + "fundere" (to pour)',
                'memory_tips': 'Think "suf-fused" - poured over and fused throughout',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The room was _____ with golden light from the setting sun.'
            },
            'sufi': {
                'definition': 'A Muslim ascetic and mystic; a practitioner of Sufism, the mystical dimension of Islam that seeks direct personal experience of God through spiritual practices.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SOO-fee (emphasis on first syllable)',
                'etymology': 'From Arabic "sufi," possibly from "suf" (wool, referring to rough garments)',
                'memory_tips': 'Think "sufi" - a spiritual seeker who is "so free" from worldly concerns',
                'alternate_spellings': '',
                'language_origin': 'Arabic',
                'example_sentence': 'The _____ poet Rumi wrote beautiful verses about divine love and spiritual unity.'
            },
            'sugar': {
                'definition': 'A sweet crystalline substance obtained from various plants, especially sugar cane and sugar beet; any of various sweet carbohydrates used as food.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'SHOOG-ur (emphasis on first syllable)',
                'etymology': 'From Old French "sucre," from Arabic "as-sukkar," from Persian "shakar"',
                'memory_tips': 'Think "sugar" - it\'s sure good and makes things sweet',
                'alternate_spellings': '',
                'language_origin': 'Persian via Arabic and French',
                'example_sentence': 'She added two teaspoons of _____ to her morning coffee.'
            },
            'sugarcane': {
                'definition': 'A tropical grass with tall stout jointed stems from which sugar is extracted; the plant Saccharum officinarum, grown commercially for sugar production.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SHOOG-ur-kayn (emphasis on first syllable)',
                'etymology': 'Compound of "sugar" + "cane," referring to the cane-like plant that produces sugar',
                'memory_tips': 'Think "sugar-cane" - a cane plant that produces sugar',
                'alternate_spellings': 'sugar cane',
                'language_origin': 'English (compound)',
                'example_sentence': 'The plantation workers harvested acres of _____ during the busy harvest season.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_171_data:
            return batch_171_data[word_lower]
        
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
    
    def process_batch_171(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 171 with comprehensive Claude data"""
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
    
    def save_batch_171_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 171 processed words to CSV"""
        
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
    """Process Batch 171 with comprehensive Claude data"""
    processor = Batch171Processor()
    input_csv = Path("output/batch_171_words.csv")
    output_csv = Path("output/batch_171_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 171 with comprehensive Claude data...")
    
    # Process all words in batch 171
    processed_words = processor.process_batch_171(input_csv)
    
    # Save results
    processor.save_batch_171_csv(processed_words, output_csv)
    
    logger.info(f"Batch 171 processing completed!")
    logger.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
    logger.info(f"Output saved to: {output_csv}")
    
    # Show summary
    successful_words = [w for w in processed_words if w.claude_definition]
    failed_words = [w for w in processed_words if not w.claude_definition]
    combined_errors = [w for w in processed_words if "COMBINED WORD ERROR" in w.claude_definition]
    
    logger.info(f"Results: {len(successful_words)} successful, {len(failed_words)} failed")
    logger.info(f"Combined word errors detected and flagged: {len(combined_errors)}")
    
    if failed_words:
        logger.info("Words that failed processing:")
        for word in failed_words:
            logger.info(f"  - {word.word}: {word.error_notes}")
            
    if combined_errors:
        logger.info("Combined word errors flagged:")
        for word in combined_errors:
            logger.info(f"  - {word.word}: Combined word error")

if __name__ == "__main__":
    main()