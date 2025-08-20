#!/usr/bin/env python3
"""
Process Batch 001 of Spelling Bee Words with Comprehensive Claude Data
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

class Batch001Processor:
    """Processes Batch 001 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 001 words"""
        
        # Comprehensive data for all 50 words in Batch 001
        batch_001_data = {
            'aachen': {
                'definition': 'A city in western Germany near the borders with Belgium and the Netherlands, historically significant as the coronation site of Holy Roman Emperors.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'AH-khen (emphasis on first syllable)',
                'etymology': 'From Latin "Aquae Granni" meaning "waters of Grannus," named after the Celtic god of healing springs',
                'memory_tips': 'Remember "Aachen" sounds like "aching" - the healing waters were meant to cure aches',
                'alternate_spellings': 'Aix-la-Chapelle (French name)',
                'language_origin': 'Latin, Celtic',
                'example_sentence': 'Charlemagne was crowned Holy Roman Emperor in _____ in the year 800 CE.'
            },
            'aardvark': {
                'definition': 'A nocturnal, burrowing mammal native to Africa with a long snout, powerful claws, and a diet consisting primarily of ants and termites.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AHRD-vahrk (emphasis on first syllable)',
                'etymology': 'From Afrikaans, literally meaning "earth pig" (aarde = earth + vark = pig)',
                'memory_tips': 'Remember "earth pig" - it digs in the earth like a pig roots in mud',
                'alternate_spellings': '',
                'language_origin': 'Afrikaans (South African Dutch)',
                'example_sentence': 'The _____ uses its long snout and powerful claws to dig into termite mounds.'
            },
            'abaculus': {
                'definition': 'A small tile or piece of colored glass, stone, or ceramic material used in creating mosaics; a tessera.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-BAK-yuh-lus (emphasis on second syllable)',
                'etymology': 'From Latin "abaculus," diminutive of "abacus," meaning small counting board or tile',
                'memory_tips': 'Think "a back-you-loose" - small tiles that you might lose from the back of a mosaic',
                'alternate_spellings': 'tessera',
                'language_origin': 'Latin',
                'example_sentence': 'Each _____ was carefully placed to create the intricate mosaic pattern.'
            },
            'abaft': {
                'definition': 'Located toward or at the stern (rear) of a ship; behind a particular point on a vessel.',
                'part_of_speech': 'adverb, preposition',
                'pronunciation_guide': 'uh-BAFT (emphasis on second syllable)',
                'etymology': 'From Middle English, from Old English "æftan" meaning "from behind"',
                'memory_tips': 'Think "a-back" - it means toward the back (stern) of a ship',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The captain ordered the crew to secure the cargo _____ of the main mast.'
            },
            'abalones': {
                'definition': 'Large marine gastropod mollusks with ear-shaped shells lined with mother-of-pearl, prized as seafood and for their decorative shells.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'ab-uh-LOH-neez (emphasis on third syllable)',
                'etymology': 'From Spanish "abulón", possibly from an indigenous Californian language',
                'memory_tips': 'Think "able-lonely" - these shellfish live alone in their shells',
                'alternate_spellings': 'abalone (singular)',
                'language_origin': 'Spanish, possibly from indigenous Californian',
                'example_sentence': 'The diver carefully harvested _____ from the rocky coastal waters.'
            },
            'abandon': {
                'definition': 'To give up completely; to desert or leave behind; to cease maintaining or supporting.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'uh-BAN-duhn (emphasis on second syllable)',
                'etymology': 'From Old French "abandoner", from "a bandon" meaning "at one\'s disposal"',
                'memory_tips': 'Think "a band on" - when you abandon, you let go like taking off a band',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The family had to _____ their home when the floodwaters rose.'
            },
            'abandoned': {
                'definition': 'Having been deserted or left behind; given up completely; characterized by lack of restraint.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'uh-BAN-duhnd (emphasis on second syllable)',
                'etymology': 'Past participle of abandon, from Old French "abandoner"',
                'memory_tips': 'Remember "a band undone" - something that has been left behind',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The _____ factory stood as a reminder of the town\'s industrial past.'
            },
            'abashed': {
                'definition': 'Feeling embarrassed, ashamed, or disconcerted; made to feel uncomfortable by awareness of fault or shortcoming.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'uh-BASHT (emphasis on second syllable)',
                'etymology': 'From Old French "esbahir" meaning "to astonish"',
                'memory_tips': 'Think "a-bashed" - feeling bashed down by embarrassment',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'She felt _____ when she realized she had been singing off-key the entire time.'
            },
            'abated': {
                'definition': 'Became less intense or widespread; decreased in force, intensity, or amount; subsided.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'uh-BAY-tid (emphasis on second syllable)',
                'etymology': 'From Old French "abatre" meaning "to beat down"',
                'memory_tips': 'Think "a-baited" - the intensity was baited away, reduced',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The storm finally _____ after three days of continuous rain.'
            },
            'abattoir': {
                'definition': 'A slaughterhouse; a facility where livestock are killed for food production.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AB-uh-twahr (emphasis on first syllable)',
                'etymology': 'From French "abattoir", from "abattre" meaning "to strike down"',
                'memory_tips': 'Contains "bat" - where animals are struck down for slaughter',
                'alternate_spellings': 'slaughterhouse',
                'language_origin': 'French',
                'example_sentence': 'The health inspector visited the _____ to ensure proper sanitation standards.'
            },
            'abbreviations': {
                'definition': 'Shortened forms of words or phrases, typically created by omitting letters or using only initial letters.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'uh-bree-vee-AY-shunz (emphasis on fourth syllable)',
                'etymology': 'From Latin "abbreviatus", past participle of "abbreviare" meaning "to shorten"',
                'memory_tips': 'Think "a-brief-nation" - making words brief for the nation',
                'alternate_spellings': 'abbreviation (singular)',
                'language_origin': 'Latin',
                'example_sentence': 'The document was filled with technical _____ that made it difficult to understand.'
            },
            'abdomen': {
                'definition': 'The part of the body containing the digestive organs; the belly area between the thorax and pelvis in humans and other mammals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AB-duh-muhn (emphasis on first syllable)',
                'etymology': 'From Latin "abdomen" meaning "belly, lower part of the body"',
                'memory_tips': 'Think "ab-do-men" - the "ab" muscles are in this area',
                'alternate_spellings': 'belly, stomach area',
                'language_origin': 'Latin',
                'example_sentence': 'The doctor examined the patient\'s _____ for signs of inflammation.'
            },
            'aberration': {
                'definition': 'A departure from what is normal, usual, or expected; a deviation from the typical course or pattern.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ab-uh-RAY-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "aberratio", from "aberrare" meaning "to wander away from"',
                'memory_tips': 'Think "a-bear-ration" - a bear wandering away from its normal food ration',
                'alternate_spellings': 'deviation, anomaly',
                'language_origin': 'Latin',
                'example_sentence': 'The sudden cold snap in June was considered a weather _____.'
            },
            'abeyance': {
                'definition': 'A state of temporary suspension or inactivity; a condition of being held in check or delayed.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-BAY-uhns (emphasis on second syllable)',
                'etymology': 'From Old French "abeance" meaning "expectation, waiting"',
                'memory_tips': 'Think "a-bay-dance" - like a dance on hold at the bay',
                'alternate_spellings': 'suspension, dormancy',
                'language_origin': 'Old French',
                'example_sentence': 'The construction project was held in _____ pending environmental approval.'
            },
            'abhenry': {
                'definition': 'A unit of electrical inductance equal to one billionth (10^-9) of a henry, used in electronics and electrical engineering.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AB-hen-ree (emphasis on first syllable)',
                'etymology': 'From "ab-" (prefix meaning one billionth) + "henry" (unit named after Joseph Henry)',
                'memory_tips': 'Think "ab-Henry" - a very small amount of the henry unit',
                'alternate_spellings': 'nanohenry',
                'language_origin': 'Scientific Latin, named after Joseph Henry',
                'example_sentence': 'The circuit\'s inductance was measured in _____ due to its small scale.'
            },
            'abhijay': {
                'definition': 'A Sanskrit name meaning "victorious" or "triumphant"; often used as a personal name.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'ah-bhee-JAY (emphasis on third syllable)',
                'etymology': 'From Sanskrit "abhijaya" meaning "victory, triumph"',
                'memory_tips': 'Think "a-big-jay" - a victorious bird',
                'alternate_spellings': 'Abhijaya',
                'language_origin': 'Sanskrit',
                'example_sentence': '_____ was chosen as the baby\'s name to symbolize future success.'
            },
            'abhorrence': {
                'definition': 'A feeling of intense dislike, disgust, or hatred; extreme aversion to something.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ab-HOR-uhns (emphasis on second syllable)',
                'etymology': 'From Latin "abhorrere" meaning "to shrink back from, shudder at"',
                'memory_tips': 'Think "ab-horror-ence" - the quality of finding something horrible',
                'alternate_spellings': 'disgust, loathing',
                'language_origin': 'Latin',
                'example_sentence': 'She expressed her _____ for violence in any form.'
            },
            'abject': {
                'definition': 'Existing in a state of complete misery, degradation, or servility; utterly hopeless or wretched.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'AB-jekt (emphasis on first syllable)',
                'etymology': 'From Latin "abjectus", past participle of "abicere" meaning "to throw away"',
                'memory_tips': 'Think "ab-ject" - thrown away like a rejected object',
                'alternate_spellings': 'wretched, miserable',
                'language_origin': 'Latin',
                'example_sentence': 'The refugees lived in _____ poverty in the makeshift camps.'
            },
            'ablation': {
                'definition': 'The surgical removal of body tissue; the erosive wearing away of rock, ice, or other material.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ab-LAY-shuhn (emphasis on second syllable)',
                'etymology': 'From Latin "ablatio", from "ablatus" meaning "carried away"',
                'memory_tips': 'Think "able-ation" - the action of being able to remove something',
                'alternate_spellings': 'removal, erosion',
                'language_origin': 'Latin',
                'example_sentence': 'The glacier showed signs of _____ due to rising temperatures.'
            },
            'ablaut': {
                'definition': 'A systematic change in the vowel of a word root to indicate grammatical function, such as in "sing, sang, sung".',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AH-blout (emphasis on first syllable)',
                'etymology': 'From German "Ablaut", from "ab" (off) + "Laut" (sound)',
                'memory_tips': 'Think "able-out" - able to change the vowel sound out',
                'alternate_spellings': 'vowel gradation',
                'language_origin': 'German',
                'example_sentence': 'The _____ in English verbs creates patterns like "ring, rang, rung".'
            },
            'ablaze': {
                'definition': 'On fire; burning brightly; filled with intense emotion or excitement.',
                'part_of_speech': 'adjective, adverb',
                'pronunciation_guide': 'uh-BLAZE (emphasis on second syllable)',
                'etymology': 'From Middle English "a-" (on) + "blaze" (flame)',
                'memory_tips': 'Think "a-blaze" - in a state of blazing fire',
                'alternate_spellings': 'on fire, burning',
                'language_origin': 'Middle English',
                'example_sentence': 'The forest was _____ with autumn colors.'
            },
            'able': {
                'definition': 'Having the power, skill, means, or opportunity to do something; capable or competent.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'AY-buhl (emphasis on first syllable)',
                'etymology': 'From Old French "able", from Latin "habilis" meaning "handy, manageable"',
                'memory_tips': 'Think "a-bull" - strong like a bull and able to do things',
                'alternate_spellings': 'capable, competent',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'She was _____ to solve the complex mathematical equation.'
            },
            'abnegation': {
                'definition': 'The practice of self-denial; the giving up of one\'s own interests or desires, often for moral or religious reasons.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ab-ni-GAY-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "abnegatio", from "abnegare" meaning "to deny, refuse"',
                'memory_tips': 'Think "ab-negation" - the act of negating yourself or your desires',
                'alternate_spellings': 'self-denial, renunciation',
                'language_origin': 'Latin',
                'example_sentence': 'The monk\'s life of _____ included giving up all worldly possessions.'
            },
            'abnegationbeguile': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "abnegation" (self-denial) + "beguile" (to charm or deceive).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "abnegation" and "beguile"',
                'alternate_spellings': 'abnegation + beguile (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'abodes': {
                'definition': 'Places where people live; dwellings or residences, especially when considered as homes.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'uh-BOHDZ (emphasis on second syllable)',
                'etymology': 'From Middle English "abiden" meaning "to dwell, remain"',
                'memory_tips': 'Think "a-bodes" - places where you bide your time',
                'alternate_spellings': 'dwellings, residences',
                'language_origin': 'Middle English',
                'example_sentence': 'The mountain village contained humble _____ built from local stone.'
            },
            'abolish': {
                'definition': 'To formally end or eliminate a system, practice, or institution; to put an end to something completely.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'uh-BOL-ish (emphasis on second syllable)',
                'etymology': 'From Old French "aboliss-", from Latin "abolere" meaning "to destroy"',
                'memory_tips': 'Think "a-polish" - to polish something away completely',
                'alternate_spellings': 'eliminate, end',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The government decided to _____ the outdated tax system.'
            },
            'abomasum': {
                'definition': 'The fourth and final stomach chamber of ruminant animals like cattle, sheep, and goats, where true digestion occurs.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ab-oh-MAY-sum (emphasis on third syllable)',
                'etymology': 'From New Latin, possibly from Latin "ab" (from) + "omasum" (paunch)',
                'memory_tips': 'Think "a-bomb-awesome" - the awesome final stomach that completes digestion',
                'alternate_spellings': 'true stomach',
                'language_origin': 'New Latin',
                'example_sentence': 'The veterinarian explained how food moves from the rumen to the _____.'
            },
            'abominable': {
                'definition': 'Causing moral revulsion; extremely unpleasant or disagreeable; detestable.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'uh-BOM-uh-nuh-buhl (emphasis on second syllable)',
                'etymology': 'From Latin "abominabilis", from "abominari" meaning "to deprecate as an ill omen"',
                'memory_tips': 'Think "a-bomb-in-able" - so terrible it\'s like a bomb inside something able',
                'alternate_spellings': 'detestable, loathsome',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ conditions in the prison led to international condemnation.'
            },
            'aboriginal': {
                'definition': 'Relating to the indigenous inhabitants of a region; existing in a place from the earliest known period.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ab-uh-RIJ-uh-nuhl (emphasis on third syllable)',
                'etymology': 'From Latin "aborigines", from "ab origine" meaning "from the beginning"',
                'memory_tips': 'Think "ab-original" - from the very origin or beginning',
                'alternate_spellings': 'indigenous, native',
                'language_origin': 'Latin',
                'example_sentence': 'The museum featured exhibits about _____ cultures of Australia.'
            },
            'above': {
                'definition': 'In or to a higher place; at a higher level or position; more than a specified amount.',
                'part_of_speech': 'adverb, preposition, adjective',
                'pronunciation_guide': 'uh-BUHV (emphasis on second syllable)',
                'etymology': 'From Old English "abufan", from "a" (on) + "bufan" (over)',
                'memory_tips': 'Think "a-bove" - like a dove flying up high',
                'alternate_spellings': 'over, higher than',
                'language_origin': 'Old English',
                'example_sentence': 'The plane flew _____ the clouds during the storm.'
            },
            'abracadabra': {
                'definition': 'A word traditionally used by magicians as an incantation when performing tricks; any nonsensical or mystical word.',
                'part_of_speech': 'noun, interjection',
                'pronunciation_guide': 'ab-ruh-kuh-DAB-ruh (emphasis on fourth syllable)',
                'etymology': 'Of uncertain origin, possibly from Aramaic "avra kehdabra" meaning "I create as I speak"',
                'memory_tips': 'Think "a-bracelet-dabra" - a magical bracelet that makes things appear',
                'alternate_spellings': 'magic word',
                'language_origin': 'Uncertain, possibly Aramaic',
                'example_sentence': 'The magician waved his wand and shouted "_____!" as the rabbit appeared.'
            },
            'abraum': {
                'definition': 'Waste material or overburden removed from a mine site; worthless rock or soil that must be cleared to reach valuable minerals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AH-browm (emphasis on first syllable)',
                'etymology': 'From German "Abraum" meaning "material to be cleared away"',
                'memory_tips': 'Think "a-broom" - material that needs to be swept away like with a broom',
                'alternate_spellings': 'overburden, waste rock',
                'language_origin': 'German',
                'example_sentence': 'The mining company had to remove tons of _____ before reaching the ore deposit.'
            },
            'abrogate': {
                'definition': 'To formally revoke, cancel, or abolish a law, agreement, or custom; to put an end to something officially.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'AB-ruh-gayt (emphasis on first syllable)',
                'etymology': 'From Latin "abrogare", from "ab" (away) + "rogare" (to propose a law)',
                'memory_tips': 'Think "ab-roger-gate" - Roger opens the gate to let the law go away',
                'alternate_spellings': 'revoke, cancel',
                'language_origin': 'Latin',
                'example_sentence': 'The new administration decided to _____ the controversial trade agreement.'
            },
            'abruptly': {
                'definition': 'In a sudden and unexpected manner; without warning or preparation; sharply or steeply.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'uh-BRUHPT-lee (emphasis on second syllable)',
                'etymology': 'From Latin "abruptus" meaning "broken off, steep" + "-ly"',
                'memory_tips': 'Think "a-rupt-ly" - like an eruption that happens suddenly',
                'alternate_spellings': 'suddenly, sharply',
                'language_origin': 'Latin',
                'example_sentence': 'The meeting ended _____ when the fire alarm sounded.'
            },
            'abscess': {
                'definition': 'A localized collection of pus in body tissue, caused by infection and typically accompanied by swelling and inflammation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AB-ses (emphasis on first syllable)',
                'etymology': 'From Latin "abscessus", from "abscedere" meaning "to go away, withdraw"',
                'memory_tips': 'Think "ab-cess" - something that needs to cease and go away from the body',
                'alternate_spellings': 'infection, pustule',
                'language_origin': 'Latin',
                'example_sentence': 'The dentist drained the _____ that had formed near the infected tooth.'
            },
            'abscond': {
                'definition': 'To leave hurriedly and secretly, typically to avoid detection or arrest; to depart suddenly and hide oneself.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ab-SKOND (emphasis on second syllable)',
                'etymology': 'From Latin "abscondere", from "abs" (away) + "condere" (to hide)',
                'memory_tips': 'Think "ab-scond" - to scamper and hide away from someone',
                'alternate_spellings': 'flee, escape',
                'language_origin': 'Latin',
                'example_sentence': 'The thief tried to _____ with the stolen jewels before the police arrived.'
            },
            'absent': {
                'definition': 'Not present in a place or at an event; missing from where one is supposed to be.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'AB-suhnt (emphasis on first syllable)',
                'etymology': 'From Latin "absentem", present participle of "abesse" meaning "to be away"',
                'memory_tips': 'Think "ab-sent" - sent away from where you should be',
                'alternate_spellings': 'missing, away',
                'language_origin': 'Latin',
                'example_sentence': 'The student was _____ from class due to illness.'
            },
            'absolution': {
                'definition': 'Formal forgiveness or release from guilt, obligation, or punishment, especially in a religious context.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ab-suh-LOO-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "absolutio", from "absolvere" meaning "to set free, acquit"',
                'memory_tips': 'Think "absolute-solution" - the complete solution that frees you from guilt',
                'alternate_spellings': 'forgiveness, pardon',
                'language_origin': 'Latin',
                'example_sentence': 'The priest granted _____ to the penitent after hearing confession.'
            },
            'absorptive': {
                'definition': 'Having the quality or capacity to absorb liquids, energy, or other substances; capable of taking in and retaining.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ab-SORP-tiv (emphasis on second syllable)',
                'etymology': 'From Latin "absorptus", past participle of "absorbere" meaning "to swallow up"',
                'memory_tips': 'Think "ab-sorptive" - actively sorting and absorbing things',
                'alternate_spellings': 'absorbent, porous',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ material quickly soaked up the spilled liquid.'
            },
            'abstemious': {
                'definition': 'Practicing restraint, especially in eating and drinking; moderate in indulgence of appetites or desires.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ab-STEE-mee-us (emphasis on second syllable)',
                'etymology': 'From Latin "abstemius", from "abs" (away from) + "temetum" (intoxicating drink)',
                'memory_tips': 'Think "ab-steam-ious" - staying away from the steam of alcohol',
                'alternate_spellings': 'temperate, moderate',
                'language_origin': 'Latin',
                'example_sentence': 'The monk lived an _____ lifestyle, eating simple meals and drinking only water.'
            },
            'abstruse': {
                'definition': 'Difficult to understand; obscure or esoteric; requiring deep thought or study to comprehend.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ab-STROOS (emphasis on second syllable)',
                'etymology': 'From Latin "abstrusus", past participle of "abstrudere" meaning "to push away, conceal"',
                'memory_tips': 'Think "ab-strewn" - ideas scattered and pushed away, hard to gather',
                'alternate_spellings': 'obscure, esoteric',
                'language_origin': 'Latin',
                'example_sentence': 'The professor\'s _____ theories required extensive study to understand.'
            },
            'abstrusenephrolith': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "abstruse" (difficult to understand) + "nephrolith" (kidney stone).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "abstruse" and "nephrolith"',
                'alternate_spellings': 'abstruse + nephrolith (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'absurdly': {
                'definition': 'In a manner that is wildly unreasonable, illogical, or inappropriate; ridiculously or nonsensically.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'ab-SURD-lee (emphasis on second syllable)',
                'etymology': 'From Latin "absurdus" meaning "out of tune, unreasonable" + "-ly"',
                'memory_tips': 'Think "ab-surd-ly" - in a way that\'s surely absurd',
                'alternate_spellings': 'ridiculously, nonsensically',
                'language_origin': 'Latin',
                'example_sentence': 'The price of the concert tickets was _____ high for such a small venue.'
            },
            'abundancecalamitous': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "abundance" (large quantity) + "calamitous" (catastrophic).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "abundance" and "calamitous"',
                'alternate_spellings': 'abundance + calamitous (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'abysmal': {
                'definition': 'Extremely bad or appalling; resembling or befitting an abyss in depth or vastness.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'uh-BIZ-muhl (emphasis on second syllable)',
                'etymology': 'From "abyss" + "-al", where "abyss" comes from Greek "abyssos" meaning "bottomless"',
                'memory_tips': 'Think "a-bizz-mal" - so bad it makes you feel sick',
                'alternate_spellings': 'terrible, appalling',
                'language_origin': 'Greek via English',
                'example_sentence': 'The team\'s performance this season has been _____.'
            },
            'acacia': {
                'definition': 'A type of tree or shrub with yellow or white flowers, typically found in warm climates, known for its thorns and feathery leaves.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-KAY-shuh (emphasis on second syllable)',
                'etymology': 'From Latin "acacia", from Greek "akakia", from "ake" meaning "point, thorn"',
                'memory_tips': 'Think "a-kay-shuh" - okay, but watch out for the thorns',
                'alternate_spellings': 'wattle (in Australia)',
                'language_origin': 'Greek via Latin',
                'example_sentence': 'The _____ tree provided shade with its delicate, feathery branches.'
            },
            'acade': {
                'definition': 'An archaic or variant form referring to an academy or academic institution; a place of learning.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-KAYD (emphasis on second syllable)',
                'etymology': 'Shortened form of "academy", from Greek "akademeia"',
                'memory_tips': 'Think "a-cade" - like an arcade, but for academics',
                'alternate_spellings': 'academy',
                'language_origin': 'Greek',
                'example_sentence': 'The young scholar was excited to join the prestigious _____.'
            },
            'academese': {
                'definition': 'The jargon or specialized language used in academic writing and discourse, often criticized as unnecessarily complex or pretentious.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ak-uh-duh-MEES (emphasis on fourth syllable)',
                'etymology': 'From "academic" + "-ese" (suffix indicating a language or jargon)',
                'memory_tips': 'Think "academic-ese" - the language that academics use',
                'alternate_spellings': 'academic jargon',
                'language_origin': 'Modern English compound',
                'example_sentence': 'The professor\'s paper was so full of _____ that even other scholars found it hard to follow.'
            },
            'academic': {
                'definition': 'Relating to education and scholarship; theoretical rather than practical; associated with schools and universities.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ak-uh-DEM-ik (emphasis on third syllable)',
                'etymology': 'From Latin "academicus", from Greek "akademikos" relating to Plato\'s academy',
                'memory_tips': 'Think "a-cad-emic" - a cadet learning academics',
                'alternate_spellings': 'scholarly, educational',
                'language_origin': 'Greek via Latin',
                'example_sentence': 'Her _____ achievements earned her a scholarship to the prestigious university.'
            },
            'academy': {
                'definition': 'An institution of higher learning; a school or college for special training; a society of learned individuals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-KAD-uh-mee (emphasis on second syllable)',
                'etymology': 'From Greek "akademeia", named after the hero Akademos, where Plato taught',
                'memory_tips': 'Think "a-cad-emy" - where cadets learn to be enemies of ignorance',
                'alternate_spellings': 'school, institute',
                'language_origin': 'Greek',
                'example_sentence': 'The military _____ trained future officers in leadership and strategy.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_001_data:
            return batch_001_data[word_lower]
        
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
    
    def process_batch_001(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 001 with comprehensive Claude data"""
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
    
    def save_batch_001_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 001 processed words to CSV"""
        
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
    """Process Batch 001 with comprehensive Claude data"""
    processor = Batch001Processor()
    input_csv = Path("output/batch_001_words.csv")
    output_csv = Path("output/batch_001_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 001 with comprehensive Claude data...")
    
    # Process all words in batch 001
    processed_words = processor.process_batch_001(input_csv)
    
    # Save results
    processor.save_batch_001_csv(processed_words, output_csv)
    
    logger.info(f"Batch 001 processing completed!")
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