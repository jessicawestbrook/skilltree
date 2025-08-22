#!/usr/bin/env python3
"""
Process Batch 175 of Spelling Bee Words with Comprehensive Claude Data
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
            'team', 'tape', 'tasks', 'teachers', 'teak', 'teamwork', 'tariff', 'tarmac', 'tartan', 'taser', 'tasers', 'tangent', 'tangents', 'tango', 'tantrum'
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

class Batch175Processor:
    """Processes Batch 175 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 175 words"""
        
        # Comprehensive data for all 50 words in Batch 175
        batch_175_data = {
            'tanagerpneumatocyst': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "tanager" (a type of colorful bird) + "pneumatocyst" (gas-filled cavity).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "tanager" and "pneumatocyst"',
                'alternate_spellings': 'tanager + pneumatocyst (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'tandoori': {
                'definition': 'A method of cooking in which food is roasted in a clay oven called a tandoor; relating to this style of Indian cuisine characterized by high heat and distinctive flavors.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'tan-DOOR-ee (emphasis on second syllable)',
                'etymology': 'From Hindi "tanduri", related to "tandoor" (clay oven)',
                'memory_tips': 'Think "tan-door-y" - food that gets a tan from the door of a hot oven',
                'alternate_spellings': '',
                'language_origin': 'Hindi/Urdu',
                'example_sentence': 'The restaurant specializes in _____ chicken cooked in a traditional clay oven.'
            },
            'tangent': {
                'definition': 'A straight line that touches a curve at exactly one point; a sudden change of direction in thought or conversation; completely different from what was being discussed.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'TAN-juhnt (emphasis on first syllable)',
                'etymology': 'From Latin "tangens" meaning "touching", from "tangere" (to touch)',
                'memory_tips': 'Think "tan-gent" - a gentleman who barely touches the conversation before going off topic',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'During the math lesson, the professor went off on a _____ about his research.'
            },
            'tangents': {
                'definition': 'Plural of tangent; multiple straight lines touching curves; several sudden changes in direction of thought or conversation.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'TAN-juhnts (emphasis on first syllable)',
                'etymology': 'Plural of "tangent", from Latin "tangens"',
                'memory_tips': 'Think "tan-gents" - multiple gentlemen going off topic',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The speaker kept going off on _____ instead of staying focused on the main topic.'
            },
            'tangerine': {
                'definition': 'A small citrus fruit with bright orange skin that peels easily; the orange-red color of this fruit.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'tan-juh-REEN (emphasis on third syllable)',
                'etymology': 'From French "tangerine", after Tangier, Morocco, where the fruit was exported',
                'memory_tips': 'Think "Tangier-ine" - a fruit from the city of Tangier',
                'alternate_spellings': '',
                'language_origin': 'French (from place name)',
                'example_sentence': 'She packed a _____ in her lunch for a healthy vitamin C boost.'
            },
            'tangible': {
                'definition': 'Able to be touched or felt; having physical substance; real and concrete rather than imaginary or theoretical.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'TAN-juh-buhl (emphasis on first syllable)',
                'etymology': 'From Latin "tangibilis", from "tangere" meaning "to touch"',
                'memory_tips': 'Think "tan-gible" - able to be touched like a tan you can see and feel',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The new policy produced _____ improvements in student performance.'
            },
            'tangiblenourish': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "tangible" (touchable) + "nourish" (to feed).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "tangible" and "nourish"',
                'alternate_spellings': 'tangible + nourish (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'tango': {
                'definition': 'A passionate ballroom dance of Argentine origin characterized by dramatic poses and intricate footwork; to perform this dance.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TAN-goh (emphasis on first syllable)',
                'etymology': 'From American Spanish "tango", possibly from African language via Spanish',
                'memory_tips': 'Think "tan-go" - go get a tan while dancing passionately',
                'alternate_spellings': '',
                'language_origin': 'Spanish (possibly from African languages)',
                'example_sentence': 'The couple performed a dramatic _____ that captivated the entire audience.'
            },
            'tannined': {
                'definition': 'Treated with tannin; having undergone the process of tanning to preserve leather; containing or treated with tannins.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'TAN-ind (emphasis on first syllable)',
                'etymology': 'Past tense of "tannin", from French "tanin", from "tan" (tanbark)',
                'memory_tips': 'Think "tan-in-ed" - leather that has been tanned and is finished',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The _____ leather was soft and durable after the long curing process.'
            },
            'tantrum': {
                'definition': 'An uncontrolled outburst of anger and frustration; a violent emotional display, especially by a child.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAN-truhm (emphasis on first syllable)',
                'etymology': 'Of uncertain origin, possibly from Latin "tantrismus" or imitative of angry sounds',
                'memory_tips': 'Think "tan-drum" - beating a tan drum when angry',
                'alternate_spellings': '',
                'language_origin': 'Uncertain (possibly Latin)',
                'example_sentence': 'The toddler threw a _____ when told it was time to leave the playground.'
            },
            'taoiseach': {
                'definition': 'The prime minister of Ireland; the head of government in the Irish political system.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEE-shuhkh (emphasis on first syllable)',
                'etymology': 'From Irish Gaelic "taoiseach" meaning "chief" or "leader"',
                'memory_tips': 'Think "tea-shock" - Irish leaders might be shocked by tea instead of coffee',
                'alternate_spellings': '',
                'language_origin': 'Irish Gaelic',
                'example_sentence': 'The _____ announced new policies during the parliamentary session.'
            },
            'taoism': {
                'definition': 'A Chinese philosophical and religious tradition emphasizing harmony with the Tao (the Way), naturalness, and balance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAO-iz-uhm (emphasis on first syllable)',
                'etymology': 'From Chinese "dao" (the Way) + "-ism"',
                'memory_tips': 'Think "Tao-ism" - following the Way in Chinese philosophy',
                'alternate_spellings': 'Daoism',
                'language_origin': 'Chinese',
                'example_sentence': 'The principles of _____ emphasize living in harmony with nature.'
            },
            'tapas': {
                'definition': 'Small Spanish dishes served as appetizers or snacks, typically eaten with drinks; the Spanish tradition of social eating.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'TAH-pahs (emphasis on first syllable)',
                'etymology': 'From Spanish "tapa" meaning "lid" or "cover" (originally food placed on glass covers)',
                'memory_tips': 'Think "tap-as" - tapping on small plates as you eat',
                'alternate_spellings': '',
                'language_origin': 'Spanish',
                'example_sentence': 'They ordered a variety of _____ to share while enjoying wine at the Spanish restaurant.'
            },
            'tape': {
                'definition': 'A narrow strip of material used for binding, fastening, or recording; to fasten or record with such material.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TAYP (single syllable)',
                'etymology': 'From Old English "tæppe" meaning "strip of cloth"',
                'memory_tips': 'Think of the sticky strip you use to stick things together',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She used _____ to secure the package before mailing it.'
            },
            'tapestry': {
                'definition': 'A heavy decorative textile with intricate designs, typically hung on walls; something resembling this in complexity or richness.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAP-uh-stree (emphasis on first syllable)',
                'etymology': 'From Old French "tapisserie", from "tapis" meaning "carpet"',
                'memory_tips': 'Think "tap-istry" - tapping on intricate woven art',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The medieval _____ depicted scenes from ancient mythology.'
            },
            'tapetum': {
                'definition': 'A reflective layer in the eyes of many nocturnal animals that causes them to shine in the dark; a layer of cells in plant anthers.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tuh-PEE-tuhm (emphasis on second syllable)',
                'etymology': 'From Latin "tapetum" meaning "carpet" or "covering"',
                'memory_tips': 'Think "tape-tum" - a reflective tape covering the back of animal eyes',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The cat\'s eyes glowed in the dark due to the reflective _____ behind the retina.'
            },
            'tapioca': {
                'definition': 'A starchy substance extracted from cassava root, used in puddings and as a thickening agent; pearls made from this starch.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tap-ee-OH-kuh (emphasis on third syllable)',
                'etymology': 'From Portuguese "tapioca", from Tupi "tipioca"',
                'memory_tips': 'Think "tap-oca" - tapping to get starch from the oca (cassava) root',
                'alternate_spellings': '',
                'language_origin': 'Tupi (via Portuguese)',
                'example_sentence': 'The dessert featured _____ pearls in sweet coconut milk.'
            },
            'tappet': {
                'definition': 'A mechanical part that transfers motion in an engine, especially in valve mechanisms; a cam follower.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAP-it (emphasis on first syllable)',
                'etymology': 'From "tap" + diminutive suffix "-et"',
                'memory_tips': 'Think "tap-pet" - a small pet that taps in the engine',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The mechanic replaced the worn _____ to fix the engine noise.'
            },
            'tapping': {
                'definition': 'The action of striking lightly; extracting liquid from trees; creating threads with a tap; making rhythmic sounds.',
                'part_of_speech': 'verb (present participle), noun',
                'pronunciation_guide': 'TAP-ing (emphasis on first syllable)',
                'etymology': 'Present participle of "tap", from Middle English "tappen"',
                'memory_tips': 'Think of lightly striking with your fingers repeatedly',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'She was _____ her fingers nervously on the desk during the interview.'
            },
            'tarantula': {
                'definition': 'A large, hairy spider found in warm regions, known for its impressive size but generally harmless to humans.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tuh-RAN-chuh-luh (emphasis on second syllable)',
                'etymology': 'From Medieval Latin, after Taranto, Italy, where the spider was first identified',
                'memory_tips': 'Think "Taranto-ula" - a big spider from the Italian city of Taranto',
                'alternate_spellings': '',
                'language_origin': 'Medieval Latin (from place name)',
                'example_sentence': 'Despite its intimidating appearance, the _____ is relatively docile.'
            },
            'tardigrade': {
                'definition': 'A microscopic water animal known for its extreme resilience and ability to survive in harsh conditions including space.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAR-di-grayd (emphasis on first syllable)',
                'etymology': 'From Latin "tardigradus", from "tardus" (slow) + "gradus" (step)',
                'memory_tips': 'Think "tardy-grade" - a slow student who walks slowly but is tough',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ can survive extreme temperatures and even the vacuum of space.'
            },
            'tariff': {
                'definition': 'A tax imposed on imported or exported goods; a list of charges or fees for services.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAR-if (emphasis on first syllable)',
                'etymology': 'From Arabic "ta\'rif" meaning "notification" or "definition"',
                'memory_tips': 'Think "tar-if" - if you import tar, you pay extra fees',
                'alternate_spellings': '',
                'language_origin': 'Arabic',
                'example_sentence': 'The new _____ on steel imports affected the construction industry.'
            },
            'tarlatan': {
                'definition': 'A thin, stiff, transparent muslin fabric used for costumes, especially in ballet and theater.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAR-luh-tan (emphasis on first syllable)',
                'etymology': 'From French "tarlatane", possibly from "Tatar" (referring to Mongol origin)',
                'memory_tips': 'Think "tar-latin" - a fabric so fine it\'s like Latin writing',
                'alternate_spellings': 'tarlatane',
                'language_origin': 'French',
                'example_sentence': 'The ballerina\'s tutu was made of layers of delicate _____.'
            },
            'tarleton': {
                'definition': 'A type of thin, semi-transparent fabric similar to muslin; historically used for clothing and decorative purposes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAR-luh-tuhn (emphasis on first syllable)',
                'etymology': 'Named after a person, possibly British General Banastre Tarleton',
                'memory_tips': 'Think "tar-let-on" - letting tar-colored fabric go on',
                'alternate_spellings': '',
                'language_origin': 'English (from proper name)',
                'example_sentence': 'The Victorian dress featured _____ sleeves that were both elegant and practical.'
            },
            'tarmac': {
                'definition': 'A paved surface, especially at an airport where aircraft park and maneuver; asphalt or similar paving material.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAR-mak (emphasis on first syllable)',
                'etymology': 'From "tar" + "macadam" (type of road surface)',
                'memory_tips': 'Think "tar-mac" - Macintosh computer made of tar for roads',
                'alternate_spellings': '',
                'language_origin': 'English (compound)',
                'example_sentence': 'The plane taxied across the _____ to its designated gate.'
            },
            'tarpaulin': {
                'definition': 'A large sheet of strong, waterproof material used as a covering to protect things from rain or moisture.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tar-PAW-lin (emphasis on second syllable)',
                'etymology': 'From "tar" + "palling" (variant of "pall", meaning covering)',
                'memory_tips': 'Think "tar-pulling" - pulling a tarred cover over something',
                'alternate_spellings': 'tarp',
                'language_origin': 'English',
                'example_sentence': 'They covered the boat with a _____ to protect it from the storm.'
            },
            'tarsier': {
                'definition': 'A small nocturnal primate with enormous eyes and long fingers, found in Southeast Asia.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAR-see-er (emphasis on first syllable)',
                'etymology': 'From French "tarsier", from "tarse" (tarsus, referring to ankle bones)',
                'memory_tips': 'Think "tar-seer" - a creature that sees with tar-black big eyes',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The _____ used its large eyes to hunt insects in the darkness.'
            },
            'tartan': {
                'definition': 'A woolen cloth with a distinctive pattern of colored stripes crossing at right angles, associated with Scottish clans.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'TAR-tuhn (emphasis on first syllable)',
                'etymology': 'From French "tiretaine", a type of cloth',
                'memory_tips': 'Think "tar-tan" - Scottish fabric that gets a tan in patterns',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'He wore a kilt made of his family\'s traditional _____ pattern.'
            },
            'tartaric': {
                'definition': 'Relating to or derived from tartar; containing tartaric acid, found in grapes and used in baking powder.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'tar-TAR-ik (emphasis on second syllable)',
                'etymology': 'From "tartar" + "-ic", from Arabic "durdi" via Medieval Latin',
                'memory_tips': 'Think "tar-tar-ic" - twice the tar, relating to acid from grapes',
                'alternate_spellings': '',
                'language_origin': 'Arabic (via Medieval Latin)',
                'example_sentence': 'The baker used _____ acid to help the cookies rise properly.'
            },
            'tase': {
                'definition': 'To use a Taser or similar electroshock weapon; to subject to electric shock for subduing.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'TAYZ (single syllable)',
                'etymology': 'Back-formation from "Taser", acronym for "Thomas A. Swift\'s Electric Rifle"',
                'memory_tips': 'Think "taze" - using electricity to daze someone',
                'alternate_spellings': 'taze',
                'language_origin': 'Modern English (from acronym)',
                'example_sentence': 'The officer was trained on when it\'s appropriate to _____ a suspect.'
            },
            'taser': {
                'definition': 'An electroshock weapon that uses electrical current to disrupt voluntary control of muscles.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TAY-zer (emphasis on first syllable)',
                'etymology': 'Acronym for "Thomas A. Swift\'s Electric Rifle", from a fictional invention',
                'memory_tips': 'Think "taze-er" - something that tazes with electricity',
                'alternate_spellings': '',
                'language_origin': 'Modern English (acronym from fiction)',
                'example_sentence': 'Police officers carry a _____ as a non-lethal way to subdue suspects.'
            },
            'tasers': {
                'definition': 'Plural of taser; multiple electroshock weapons used by law enforcement and civilians for self-defense.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'TAY-zerz (emphasis on first syllable)',
                'etymology': 'Plural of "taser", from acronym "Thomas A. Swift\'s Electric Rifle"',
                'memory_tips': 'Think "taze-ers" - multiple devices that taze with electricity',
                'alternate_spellings': '',
                'language_origin': 'Modern English (acronym)',
                'example_sentence': 'The security team was equipped with _____ for crowd control.'
            },
            'tasks': {
                'definition': 'Pieces of work to be done; jobs or duties assigned to someone; specific activities requiring effort.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'TASKS (single syllable)',
                'etymology': 'Plural of "task", from Old French "tasche", from Medieval Latin "tasca"',
                'memory_tips': 'Think of a list of jobs you need to do',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'She completed all her _____ before the deadline.'
            },
            'tasmanian': {
                'definition': 'Relating to Tasmania, an island state of Australia; native to or characteristic of Tasmania.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'taz-MAY-nee-uhn (emphasis on second syllable)',
                'etymology': 'From Tasmania + "-ian", where Tasmania is named after Abel Tasman',
                'memory_tips': 'Think "Tasman-ian" - relating to the explorer Tasman\'s island',
                'alternate_spellings': '',
                'language_origin': 'English (from Dutch explorer\'s name)',
                'example_sentence': 'The _____ devil is a carnivorous marsupial found only on that island.'
            },
            'tasteless': {
                'definition': 'Lacking flavor; showing poor judgment or insensitivity; lacking aesthetic appeal or refinement.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'TAYST-lis (emphasis on first syllable)',
                'etymology': 'From "taste" + "-less", meaning without taste',
                'memory_tips': 'Think "taste-less" - food without taste or behavior without good taste',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The joke was _____ and offended many people at the dinner party.'
            },
            'tatterdemalion': {
                'definition': 'A person wearing ragged or tattered clothing; someone who appears disheveled or unkempt.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'tat-er-duh-MAL-yuhn (emphasis on fourth syllable)',
                'etymology': 'From "tattered" + "demalion" (possibly from French "malion")',
                'memory_tips': 'Think "tattered-demolition" - clothes so torn they look demolished',
                'alternate_spellings': '',
                'language_origin': 'English (possibly with French elements)',
                'example_sentence': 'The _____ wandered the streets in clothes that had seen better days.'
            },
            'taurine': {
                'definition': 'An amino acid found in animal tissues, especially important for cardiovascular function; relating to bulls or cattle.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'TOR-een (emphasis on first syllable)',
                'etymology': 'From Latin "taurus" meaning "bull" (first isolated from ox bile)',
                'memory_tips': 'Think "bull-ine" - relating to bulls, found in bull bile',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Energy drinks often contain _____ to support heart function.'
            },
            'taurinehierurgical': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "taurine" (amino acid) + "hierurgical" (relating to sacred rites).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "taurine" and "hierurgical"',
                'alternate_spellings': 'taurine + hierurgical (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'tautology': {
                'definition': 'The unnecessary repetition of an idea in different words; a statement that is necessarily true because of its logical form.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'taw-TOL-uh-jee (emphasis on second syllable)',
                'etymology': 'From Greek "tautologia", from "tauto" (same) + "logos" (word)',
                'memory_tips': 'Think "tauto-logy" - the logic of saying the same thing',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Saying "free gift" is a _____ because gifts are always free.'
            },
            'taverna': {
                'definition': 'A small restaurant or inn, especially in Greece, serving traditional food and drink in a casual atmosphere.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tuh-VER-nuh (emphasis on second syllable)',
                'etymology': 'From Italian "taverna", from Latin "taberna" meaning "shop" or "hut"',
                'memory_tips': 'Think "tavern-a" - a tavern with Mediterranean flair',
                'alternate_spellings': '',
                'language_origin': 'Italian/Latin',
                'example_sentence': 'They enjoyed fresh seafood at a seaside _____ overlooking the Aegean Sea.'
            },
            'tawny': {
                'definition': 'Of a warm, brownish-orange color; having the color of tanned leather or autumn leaves.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'TAW-nee (emphasis on first syllable)',
                'etymology': 'From Old French "tané", past participle of "taner" meaning "to tan"',
                'memory_tips': 'Think "tan-y" - having a tan color like leather',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The owl\'s _____ feathers provided perfect camouflage in the autumn trees.'
            },
            'taxicab': {
                'definition': 'A car that carries passengers for payment, typically with a meter to calculate the fare; a taxi.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAK-see-kab (emphasis on first syllable)',
                'etymology': 'From "taxi" (short for taximeter) + "cab" (cabriolet)',
                'memory_tips': 'Think "taxi-cab" - a cab that charges based on distance (tax-meter)',
                'alternate_spellings': 'taxi',
                'language_origin': 'English (compound from French elements)',
                'example_sentence': 'She hailed a _____ to get to the airport on time.'
            },
            'taxidermy': {
                'definition': 'The art of preparing, stuffing, and mounting the skins of animals to create lifelike displays.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAK-si-der-mee (emphasis on first syllable)',
                'etymology': 'From Greek "taxis" (arrangement) + "derma" (skin)',
                'memory_tips': 'Think "taxi-dermy" - arranging skin like arranging a taxi route',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The natural history museum displayed examples of expert _____.'
            },
            'taxonomic': {
                'definition': 'Relating to taxonomy; concerning the classification of organisms into groups based on shared characteristics.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'tak-suh-NOM-ik (emphasis on third syllable)',
                'etymology': 'From "taxonomy" + "-ic", from Greek "taxis" (arrangement) + "nomos" (law)',
                'memory_tips': 'Think "taxi-nomic" - arranging organisms like organizing taxi routes',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Scientists use _____ classification to organize species into related groups.'
            },
            'tazza': {
                'definition': 'A shallow ornamental cup or bowl, typically mounted on a foot; a decorative vessel used for display.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAT-sah (emphasis on first syllable)',
                'etymology': 'From Italian "tazza" meaning "cup", from Arabic "tassah"',
                'memory_tips': 'Think "tat-za" - a decorative cup that goes "ta-za" when you tap it',
                'alternate_spellings': '',
                'language_origin': 'Italian (from Arabic)',
                'example_sentence': 'The antique _____ displayed on the mantelpiece was a family heirloom.'
            },
            'tchefuncte': {
                'definition': 'A river in Louisiana; also refers to a Native American tribe that once lived in the region.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'CHEH-funk-tee (emphasis on first syllable)',
                'etymology': 'From Choctaw, meaning "chinquapin" (a type of tree)',
                'memory_tips': 'Think "che-funk-te" - a funky river name with Native American origins',
                'alternate_spellings': '',
                'language_origin': 'Choctaw',
                'example_sentence': 'The _____ River flows through southeastern Louisiana into Lake Pontchartrain.'
            },
            'teachers': {
                'definition': 'People who instruct or educate others; individuals whose profession is teaching in schools or other educational institutions.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'TEE-cherz (emphasis on first syllable)',
                'etymology': 'Plural of "teacher", from "teach" + "-er", from Old English "tæcan"',
                'memory_tips': 'Think of people who teach students in schools',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The _____ attended a professional development workshop during summer break.'
            },
            'teak': {
                'definition': 'A tropical hardwood tree valued for its durable, water-resistant timber; the wood from this tree.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEEK (single syllable)',
                'etymology': 'From Malayalam "tekka", via Portuguese "teca"',
                'memory_tips': 'Think "teak" - a tree that\'s tough and leak-resistant',
                'alternate_spellings': '',
                'language_origin': 'Malayalam (via Portuguese)',
                'example_sentence': 'The yacht\'s deck was made of beautiful, weather-resistant _____.'
            },
            'team': {
                'definition': 'A group of people working together toward a common goal; animals harnessed together; to work collaboratively.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TEEM (single syllable)',
                'etymology': 'From Old English "team" meaning "offspring, lineage, team of draft animals"',
                'memory_tips': 'Think of people joining together like steam forming a team',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The research _____ worked together to solve the complex problem.'
            },
            'teamwork': {
                'definition': 'The combined effort of a group to achieve a common goal; collaborative work toward shared objectives.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEEM-wurk (emphasis on first syllable)',
                'etymology': 'From "team" + "work", combining collaborative effort concepts',
                'memory_tips': 'Think "team-work" - work done by a team together',
                'alternate_spellings': '',
                'language_origin': 'English (compound)',
                'example_sentence': 'Good _____ was essential for completing the project on schedule.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_175_data:
            return batch_175_data[word_lower]
        
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
    
    def process_batch_175(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 175 with comprehensive Claude data"""
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
    
    def save_batch_175_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 175 processed words to CSV"""
        
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
    """Process Batch 175 with comprehensive Claude data"""
    processor = Batch175Processor()
    input_csv = Path("output/batch_175_words.csv")
    output_csv = Path("output/batch_175_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 175 with comprehensive Claude data...")
    
    # Process all words in batch 175
    processed_words = processor.process_batch_175(input_csv)
    
    # Save results
    processor.save_batch_175_csv(processed_words, output_csv)
    
    logger.info(f"Batch 175 processing completed!")
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