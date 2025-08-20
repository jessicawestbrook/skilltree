#!/usr/bin/env python3
"""
Process Batch 003 of Spelling Bee Words with Comprehensive Claude Data
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

class Batch003Processor:
    """Processes Batch 003 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 003 words"""
        
        # Comprehensive data for all 50 words in Batch 003
        batch_003_data = {
            'acropachy': {
                'definition': 'A condition characterized by clubbing of the fingers and toes; abnormal enlargement of the terminal digits often associated with certain diseases.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ak-ROP-uh-kee (emphasis on second syllable)',
                'etymology': 'From Greek "akron" (extremity) + "pachys" (thick)',
                'memory_tips': 'Think "acro-pack-y" - thick packing at the extremities',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The physician noted signs of _____ in the patient\'s fingertips.'
            },
            'across': {
                'definition': 'From one side to the other; on the opposite side; throughout the extent of something.',
                'part_of_speech': 'preposition, adverb',
                'pronunciation_guide': 'uh-KROS (emphasis on second syllable)',
                'etymology': 'From Middle English, from "a-" (on) + "cross"',
                'memory_tips': 'Think "a-cross" - using a cross to get from one side to another',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The bridge stretches _____ the wide river.'
            },
            'acrostic': {
                'definition': 'A poem or puzzle in which the first letters of each line form a word or phrase when read vertically.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'uh-KROS-tik (emphasis on second syllable)',
                'etymology': 'From Greek "akrostichis", from "akron" (end) + "stichos" (line of verse)',
                'memory_tips': 'Think "acro-stick" - sticking letters at the end (beginning) of lines',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The children wrote an _____ poem spelling out "SPRING" with the first letters.'
            },
            'acrylics': {
                'definition': 'Synthetic polymers used in paints, plastics, and textiles; acrylic paints or fibers made from these materials.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'uh-KRIL-iks (emphasis on second syllable)',
                'etymology': 'From "acrylic acid" + "-s", where acrylic comes from Latin "acer" (sharp) + Greek suffix',
                'memory_tips': 'Think "a-cry-licks" - paint that makes you cry (from fumes) but licks on smoothly',
                'alternate_spellings': '',
                'language_origin': 'Modern scientific (Latin/Greek elements)',
                'example_sentence': 'The artist preferred _____ for their vibrant colors and quick drying time.'
            },
            'activists': {
                'definition': 'People who campaign vigorously for political or social change; individuals who take action to promote causes.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'AK-ti-vists (emphasis on first syllable)',
                'etymology': 'From "active" + "-ist", from Latin "activus" meaning "doing, driving"',
                'memory_tips': 'Think "active-ists" - people who are actively involved in causes',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Environmental _____ organized a protest to protect the local forest.'
            },
            'activities': {
                'definition': 'Things that people do; actions or tasks, especially for enjoyment, education, or exercise.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'ak-TIV-i-teez (emphasis on second syllable)',
                'etymology': 'From Latin "activitas", from "activus" meaning "doing, driving"',
                'memory_tips': 'Think "active-cities" - cities full of active things to do',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The summer camp offered many outdoor _____ for the children.'
            },
            'activity': {
                'definition': 'The state of being active; a specific deed, action, or function; energetic movement or operation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ak-TIV-i-tee (emphasis on second syllable)',
                'etymology': 'From Latin "activitas", from "activus" meaning "doing, driving"',
                'memory_tips': 'Think "active-ity" - the quality of being active',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The volcanic _____ increased dramatically over the past month.'
            },
            'actually': {
                'definition': 'In fact; really; used to emphasize truth or reality, often contrary to what might be expected.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'AK-choo-uh-lee (emphasis on first syllable)',
                'etymology': 'From "actual" + "-ly", from Latin "actualis" meaning "relating to action"',
                'memory_tips': 'Think "act-you-ally" - you are actually acting as an ally to truth',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'I thought the movie would be boring, but it was _____ quite entertaining.'
            },
            'acuity': {
                'definition': 'Sharpness of thought, vision, or hearing; keenness of perception or insight; mental or sensory clarity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-KYOO-i-tee (emphasis on second syllable)',
                'etymology': 'From Latin "acuitas", from "acutus" meaning "sharp, pointed"',
                'memory_tips': 'Think "a-cute-ity" - the quality of being cute and sharp',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The pilot\'s visual _____ was tested annually to ensure flight safety.'
            },
            'acumen': {
                'definition': 'The ability to make good judgments and quick decisions; shrewdness, especially in business or practical matters.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-KYOO-muhn (emphasis on second syllable)',
                'etymology': 'From Latin "acumen" meaning "sharpness, point"',
                'memory_tips': 'Think "a-cue-men" - men who are sharp enough to take cues',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Her business _____ helped her build a successful company from scratch.'
            },
            'acupuncture': {
                'definition': 'A traditional Chinese medical practice involving the insertion of thin needles into specific points on the body.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AK-yoo-pungk-cher (emphasis on first syllable)',
                'etymology': 'From Latin "acus" (needle) + "punctura" (pricking)',
                'memory_tips': 'Think "acu-puncture" - puncturing with acute precision',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Many people find _____ helpful for managing chronic pain.'
            },
            'acutely': {
                'definition': 'In an intense or sharp manner; with keen perception or severe intensity; extremely or seriously.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'uh-KYOOT-lee (emphasis on second syllable)',
                'etymology': 'From Latin "acutus" (sharp) + "-ly"',
                'memory_tips': 'Think "a-cute-ly" - in a way that is cute and sharp',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She was _____ aware of the tension in the room.'
            },
            'adage': {
                'definition': 'A traditional saying expressing a common experience or observation; a proverb or wise saying.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AD-ij (emphasis on first syllable)',
                'etymology': 'From Latin "adagium", from "ad" (to) + "aio" (I say)',
                'memory_tips': 'Think "add-age" - adding age-old wisdom',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The old _____ "practice makes perfect" proved true in her music studies.'
            },
            'adaptable': {
                'definition': 'Able to adjust to new conditions; flexible and capable of change; easily modified for different uses.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'uh-DAP-tuh-buhl (emphasis on second syllable)',
                'etymology': 'From "adapt" + "-able", from Latin "adaptare" meaning "to fit to"',
                'memory_tips': 'Think "ad-apt-able" - able to be aptly suited to situations',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The new software is highly _____ to different operating systems.'
            },
            'adapted': {
                'definition': 'Changed or modified to suit new conditions; adjusted to fit different circumstances or requirements.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'uh-DAP-tid (emphasis on second syllable)',
                'etymology': 'Past tense of "adapt", from Latin "adaptare" meaning "to fit to"',
                'memory_tips': 'Think "ad-apt-ed" - aptly suited and finished',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The novel was _____ into a successful television series.'
            },
            'added': {
                'definition': 'Put together with something else; included as an extra or additional element; combined or joined.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'AD-id (emphasis on first syllable)',
                'etymology': 'Past tense of "add", from Latin "addere" meaning "to give to"',
                'memory_tips': 'Think "add-ed" - past tense of adding something',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She _____ extra spices to enhance the flavor of the soup.'
            },
            'addendum': {
                'definition': 'An additional item or supplement added to a book, document, or statement; an appendix or attachment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-DEN-dum (emphasis on second syllable)',
                'etymology': 'From Latin "addendum" meaning "something to be added"',
                'memory_tips': 'Think "add-end-um" - something to add at the end',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The contract included an _____ specifying new terms and conditions.'
            },
            'adding': {
                'definition': 'The act of putting together or combining; including something extra; performing mathematical addition.',
                'part_of_speech': 'verb (present participle)',
                'pronunciation_guide': 'AD-ing (emphasis on first syllable)',
                'etymology': 'Present participle of "add", from Latin "addere" meaning "to give to"',
                'memory_tips': 'Think "add-ing" - currently in the process of adding',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She is _____ more vegetables to make the salad healthier.'
            },
            'addition': {
                'definition': 'The action of adding something; a mathematical operation; something that has been added.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-DISH-uhn (emphasis on second syllable)',
                'etymology': 'From Latin "additio", from "addere" meaning "to give to"',
                'memory_tips': 'Think "add-ition" - the condition of being added',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The new wing was a welcome _____ to the hospital.'
            },
            'addle': {
                'definition': 'To make confused or muddled; to become rotten or spoiled (especially of eggs); to muddle one\'s thinking.',
                'part_of_speech': 'verb, adjective',
                'pronunciation_guide': 'AD-uhl (emphasis on first syllable)',
                'etymology': 'From Old English "adela" meaning "liquid filth, urine"',
                'memory_tips': 'Think "add-el" - adding confusion until your brain feels like liquid',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The complicated instructions began to _____ his brain.'
            },
            'addledifficulty': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "addled" (confused) + "difficulty" (problem).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "addled" and "difficulty"',
                'alternate_spellings': 'addled + difficulty (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'adduced': {
                'definition': 'Cited as evidence or proof; brought forward as an example or argument; presented to support a case.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'uh-DOOST (emphasis on second syllable)',
                'etymology': 'From Latin "adducere", from "ad" (to) + "ducere" (to lead)',
                'memory_tips': 'Think "ad-duced" - leading to proof by adding evidence',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The lawyer _____ several precedents to support her argument.'
            },
            'adelaide': {
                'definition': 'A city in southern Australia; also a feminine given name meaning "noble natured" or "nobility".',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'AD-uh-layd (emphasis on first syllable)',
                'etymology': 'From Germanic "adalheid", from "adal" (noble) + "heid" (kind, sort)',
                'memory_tips': 'Think "add-a-lady" - adding a noble lady\'s name',
                'alternate_spellings': '',
                'language_origin': 'Germanic',
                'example_sentence': 'The city of _____ is known for its wine regions and cultural festivals.'
            },
            'adhesion': {
                'definition': 'The action of sticking to something; the tendency of surfaces to cling together; attachment or loyalty.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ad-HEE-zhuhn (emphasis on second syllable)',
                'etymology': 'From Latin "adhaesio", from "adhaerere" meaning "to stick to"',
                'memory_tips': 'Think "ad-he-sion" - he is sticking to something',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The gecko\'s _____ to walls comes from tiny hairs on its feet.'
            },
            'adiabatic': {
                'definition': 'Relating to a process that occurs without transfer of heat or matter; thermodynamically isolated.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ay-dee-uh-BAT-ik (emphasis on third syllable)',
                'etymology': 'From Greek "a-" (not) + "diabatos" (passable)',
                'memory_tips': 'Think "a-dia-bat-ic" - not allowing heat to pass like a bat in a cave',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ expansion of gas caused the temperature to drop rapidly.'
            },
            'adieu': {
                'definition': 'A farewell; goodbye (used as an interjection or noun); a parting salutation.',
                'part_of_speech': 'noun, interjection',
                'pronunciation_guide': 'uh-DYOO (emphasis on second syllable)',
                'etymology': 'From French "à Dieu" meaning "to God" (commending someone to God\'s care)',
                'memory_tips': 'Think "a-due" - saying goodbye is due when parting',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'With a final _____, she departed for her long journey abroad.'
            },
            'adipose': {
                'definition': 'Relating to or consisting of fat; fatty tissue that stores energy and provides insulation.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'AD-i-pohs (emphasis on first syllable)',
                'etymology': 'From Latin "adiposus", from "adeps" meaning "fat"',
                'memory_tips': 'Think "add-i-pose" - adding poses makes you lose fat',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The surgeon removed excess _____ tissue during the procedure.'
            },
            'adirondack': {
                'definition': 'Relating to a mountain region in upstate New York; a type of rustic outdoor chair with slanted back and wide armrests.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ad-i-RON-dak (emphasis on third syllable)',
                'etymology': 'From Mohawk "ratirontaks" meaning "tree-eaters" (bark-eaters)',
                'memory_tips': 'Think "add-iron-dack" - adding iron to make a strong deck chair',
                'alternate_spellings': '',
                'language_origin': 'Mohawk (Native American)',
                'example_sentence': 'They relaxed in _____ chairs while watching the sunset over the lake.'
            },
            'adjective': {
                'definition': 'A word that describes or modifies a noun or pronoun; a part of speech expressing quality, characteristic, or attribute.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AJ-ik-tiv (emphasis on first syllable)',
                'etymology': 'From Latin "adjectivum", from "adicere" meaning "to add to"',
                'memory_tips': 'Think "add-jective" - adding descriptive words to objects',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The word "beautiful" is an _____ that describes the noun "sunset".'
            },
            'adjectives': {
                'definition': 'Words that describe or modify nouns or pronouns; multiple descriptive terms expressing qualities or characteristics.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'AJ-ik-tivz (emphasis on first syllable)',
                'etymology': 'Plural of "adjective", from Latin "adjectivum"',
                'memory_tips': 'Think "add-jectives" - adding multiple descriptive words',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The poet used colorful _____ to create vivid imagery in the poem.'
            },
            'adjudicate': {
                'definition': 'To make a formal judgment on a disputed matter; to act as a judge in a competition or legal case.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'uh-JOO-di-kayt (emphasis on second syllable)',
                'etymology': 'From Latin "adjudicare", from "ad" (to) + "judicare" (to judge)',
                'memory_tips': 'Think "ad-judi-cate" - adding judicial wisdom to settle disputes',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The panel will _____ the dispute between the two companies.'
            },
            'adjudicatecaricature': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "adjudicate" (to judge) + "caricature" (exaggerated portrait).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "adjudicate" and "caricature"',
                'alternate_spellings': 'adjudicate + caricature (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'adjugate': {
                'definition': 'In mathematics, the transpose of the cofactor matrix; used in calculating matrix inverses.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'AJ-oo-gayt (emphasis on first syllable)',
                'etymology': 'From Latin "adjugatus", past participle of "adjugare" meaning "to yoke to"',
                'memory_tips': 'Think "add-you-gate" - adding you to the mathematical gate',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Students learned to calculate the _____ matrix in linear algebra class.'
            },
            'adjure': {
                'definition': 'To urge or request earnestly; to command solemnly as if under oath; to entreat or implore.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'uh-JOOR (emphasis on second syllable)',
                'etymology': 'From Latin "adjurare", from "ad" (to) + "jurare" (to swear)',
                'memory_tips': 'Think "ad-jure" - adding a sworn oath to your request',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The witness was adjured to tell nothing but the truth.'
            },
            'adjusted': {
                'definition': 'Changed or modified to achieve a desired fit, appearance, or result; adapted to new conditions.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'uh-JUS-tid (emphasis on second syllable)',
                'etymology': 'From Latin "adjustare", from "ad" (to) + "justus" (just, proper)',
                'memory_tips': 'Think "ad-just-ed" - made just right and finished',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She _____ the mirror to get a better view of the road.'
            },
            'adjutant': {
                'definition': 'A military officer who assists a commanding officer; a large stork found in Asia; an assistant or aide.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AJ-uh-tuhnt (emphasis on first syllable)',
                'etymology': 'From Latin "adjutare" meaning "to help" (frequentative of "adjuvare")',
                'memory_tips': 'Think "add-jute-ant" - an ant that helps add support like jute fiber',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The colonel\'s _____ organized the daily briefing for the troops.'
            },
            'administered': {
                'definition': 'Managed or supervised the execution of something; gave or applied (medicine, treatment, or test).',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'ad-MIN-i-sterd (emphasis on second syllable)',
                'etymology': 'From Latin "administrare", from "ad" (to) + "ministrare" (to serve)',
                'memory_tips': 'Think "ad-minister-ed" - a minister added his service and finished',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The nurse _____ the medication according to the doctor\'s instructions.'
            },
            'admiration': {
                'definition': 'A feeling of respect and approval; the act of regarding with wonder, pleasure, or approval.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ad-muh-RAY-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "admiratio", from "admirari" meaning "to wonder at"',
                'memory_tips': 'Think "ad-mire-ation" - the state of admiring something',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She gazed at the painting with obvious _____ for the artist\'s skill.'
            },
            'admirer': {
                'definition': 'A person who regards someone or something with respect, approval, or romantic interest.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ad-MY-rer (emphasis on second syllable)',
                'etymology': 'From "admire" + "-er", from Latin "admirari" meaning "to wonder at"',
                'memory_tips': 'Think "ad-mire-er" - one who adds wonder and respect',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The famous actor had many fans but few genuine _____ of his charitable work.'
            },
            'admit': {
                'definition': 'To confess to be true; to allow someone to enter; to acknowledge or accept as valid.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ad-MIT (emphasis on second syllable)',
                'etymology': 'From Latin "admittere", from "ad" (to) + "mittere" (to send)',
                'memory_tips': 'Think "ad-mit" - adding permission to send someone in',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She was reluctant to _____ that she had made a mistake.'
            },
            'admitted': {
                'definition': 'Confessed or acknowledged as true; allowed to enter; accepted into an institution or group.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'ad-MIT-id (emphasis on second syllable)',
                'etymology': 'Past tense of "admit", from Latin "admittere"',
                'memory_tips': 'Think "ad-mitt-ed" - permission was added and completed',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'He _____ to feeling nervous before the important presentation.'
            },
            'admonition': {
                'definition': 'A gentle or friendly reproof; advice or warning given to someone about their behavior.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ad-muh-NISH-uhn (emphasis on third syllable)',
                'etymology': 'From Latin "admonitio", from "admonere" meaning "to warn"',
                'memory_tips': 'Think "ad-monitor-tion" - adding monitoring with a warning',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The teacher\'s gentle _____ helped the student improve his behavior.'
            },
            'adnate': {
                'definition': 'In botany, grown together or attached to another part (as stamens to petals); congenitally attached.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'AD-nayt (emphasis on first syllable)',
                'etymology': 'From Latin "adnatus", from "ad" (to) + "natus" (born)',
                'memory_tips': 'Think "add-nate" - born attached to something additional',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The botanist noted that the stamens were _____ to the petals in this flower species.'
            },
            'adolescence': {
                'definition': 'The period of development between childhood and adulthood; the teenage years characterized by physical and emotional changes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ad-uh-LES-uhns (emphasis on third syllable)',
                'etymology': 'From Latin "adolescentia", from "adolescere" meaning "to grow up"',
                'memory_tips': 'Think "add-olesence" - adding the essence of growing up',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'During _____, teenagers experience significant physical and emotional changes.'
            },
            'adorable': {
                'definition': 'Inspiring affection or warm approval; charming and delightful; lovable and cute.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'uh-DOR-uh-buhl (emphasis on second syllable)',
                'etymology': 'From "adore" + "-able", from Latin "adorare" meaning "to worship"',
                'memory_tips': 'Think "a-door-able" - so cute you want to open the door to let it in',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The puppy was so _____ that everyone wanted to pet it.'
            },
            'adorned': {
                'definition': 'Decorated or made more beautiful with ornaments; embellished or enhanced with attractive items.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'uh-DORND (emphasis on second syllable)',
                'etymology': 'From Latin "adornare", from "ad" (to) + "ornare" (to equip, decorate)',
                'memory_tips': 'Think "a-dorned" - decorated like a door with ornaments',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The Christmas tree was _____ with colorful lights and ornaments.'
            },
            'adrenergic': {
                'definition': 'Relating to nerve cells that release adrenaline or noradrenaline; activated by or involving adrenaline.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ad-ruh-NUR-jik (emphasis on third syllable)',
                'etymology': 'From "adrenaline" + Greek "ergon" (work) + "-ic"',
                'memory_tips': 'Think "adrenaline-ergic" - working with adrenaline energy',
                'alternate_spellings': '',
                'language_origin': 'Modern scientific (Greek elements)',
                'example_sentence': 'The doctor prescribed medication to block _____ receptors in the heart.'
            },
            'adrift': {
                'definition': 'Floating without being steered or anchored; lacking direction or purpose; in a state of uncertainty.',
                'part_of_speech': 'adjective, adverb',
                'pronunciation_guide': 'uh-DRIFT (emphasis on second syllable)',
                'etymology': 'From "a-" (on) + "drift", from Old Norse "drift" meaning "snowdrift"',
                'memory_tips': 'Think "a-drift" - in a state of drifting',
                'alternate_spellings': '',
                'language_origin': 'Old Norse via Middle English',
                'example_sentence': 'The small boat was _____ in the calm sea after its engine failed.'
            },
            'adscititious': {
                'definition': 'Added from outside; supplemental; derived from external sources rather than inherent.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ad-si-TISH-us (emphasis on third syllable)',
                'etymology': 'From Latin "adscititius", from "adsciscere" meaning "to take to oneself"',
                'memory_tips': 'Think "add-sit-itious" - sitting down to add external elements',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The philosopher argued that moral values were _____ rather than innate.'
            },
            'adsum': {
                'definition': 'Latin phrase meaning "I am present" or "here"; used to indicate attendance or availability.',
                'part_of_speech': 'interjection',
                'pronunciation_guide': 'AD-sum (emphasis on first syllable)',
                'etymology': 'From Latin "adsum", from "ad" (to, at) + "sum" (I am)',
                'memory_tips': 'Think "add-sum" - adding your presence to the sum total',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'When the teacher called roll, each student responded "_____" to indicate their presence.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_003_data:
            return batch_003_data[word_lower]
        
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
    
    def process_batch_003(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 003 with comprehensive Claude data"""
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
    
    def save_batch_003_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 003 processed words to CSV"""
        
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
    """Process Batch 003 with comprehensive Claude data"""
    processor = Batch003Processor()
    input_csv = Path("output/batch_003_words.csv")
    output_csv = Path("output/batch_003_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 003 with comprehensive Claude data...")
    
    # Process all words in batch 003
    processed_words = processor.process_batch_003(input_csv)
    
    # Save results
    processor.save_batch_003_csv(processed_words, output_csv)
    
    logger.info(f"Batch 003 processing completed!")
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