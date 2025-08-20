#!/usr/bin/env python3
"""
Process Batch 050 of Spelling Bee Words with Comprehensive Claude Data
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
            'government', 'company', 'number', 'group', 'problem', 'fact', 'data', 'deal', 'dear', 'death', 'debt', 'dark', 'dash', 'daughter', 'deer',
            'default', 'defeat', 'defense', 'defined', 'definition', 'defy', 'delivery', 'deny', 'department', 'describe', 'describes', 'designed',
            'desk', 'despite', 'dessert', 'detail', 'detect', 'develop', 'developed', 'diamond'
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

class Batch050Processor:
    """Processes Batch 050 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 050 words"""
        
        # Comprehensive data for all 50 words in Batch 050
        batch_050_data = {
            'designed': {
                'definition': 'Created according to a plan; intended for a specific purpose; having a particular pattern or style.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'dih-ZAHYND (emphasis on second syllable)',
                'etymology': 'From "design" (from Latin "designare") + "-ed"',
                'memory_tips': 'Think "de-signed" - something that has been signed off on',
                'alternate_spellings': 'planned, created',
                'language_origin': 'Latin',
                'example_sentence': 'The building was _____ by a famous architect.'
            },
            'designer': {
                'definition': 'A person who plans and creates the form and look of objects, buildings, or systems.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-ZAHY-ner (emphasis on second syllable)',
                'etymology': 'From "design" (from Latin "designare") + "-er"',
                'memory_tips': 'Think "de-signer" - one who signs off on designs',
                'alternate_spellings': 'creator, planner',
                'language_origin': 'Latin',
                'example_sentence': 'The fashion _____ unveiled her new collection at Paris Fashion Week.'
            },
            'designerleisure': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "designer" (creator) + "leisure" (free time).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "designer" and "leisure"',
                'alternate_spellings': 'designer + leisure (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'desk': {
                'definition': 'A piece of furniture with a flat surface for writing, reading, or using a computer.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DESK (emphasis on first syllable)',
                'etymology': 'From Medieval Latin "desca", from Latin "discus" meaning "disk, plate"',
                'memory_tips': 'Think "disk" - a flat surface like a desk',
                'alternate_spellings': 'table, workstation',
                'language_origin': 'Latin',
                'example_sentence': 'She organized the papers on her _____.'
            },
            'desman': {
                'definition': 'A small aquatic mammal related to moles, with webbed feet and a long snout.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DEZ-muhn (emphasis on first syllable)',
                'etymology': 'From French "desman", possibly from German "Bisam" meaning "musk"',
                'memory_tips': 'Think "des-man" - a water man (aquatic mammal)',
                'alternate_spellings': 'aquatic mole',
                'language_origin': 'French, possibly German',
                'example_sentence': 'The _____ is an unusual semi-aquatic mammal found in Europe.'
            },
            'desolate': {
                'definition': 'Empty of people; deserted and giving an impression of bleak emptiness.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'DES-uh-lit (emphasis on first syllable)',
                'etymology': 'From Latin "desolatus", past participle of "desolare" meaning "to abandon"',
                'memory_tips': 'Think "de-so-late" - so late that everyone left (abandoned)',
                'alternate_spellings': 'barren, abandoned',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ landscape stretched for miles without a single building.'
            },
            'despicable': {
                'definition': 'Deserving hatred and contempt; extremely unpleasant or evil.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dih-SPIK-uh-buhl (emphasis on second syllable)',
                'etymology': 'From Latin "despicabilis", from "despicere" meaning "to look down on"',
                'memory_tips': 'Think "de-spic-able" - able to be spiced with contempt',
                'alternate_spellings': 'contemptible, loathsome',
                'language_origin': 'Latin',
                'example_sentence': 'The villain\'s _____ behavior made everyone despise him.'
            },
            'despite': {
                'definition': 'In spite of; without being affected by; notwithstanding.',
                'part_of_speech': 'preposition',
                'pronunciation_guide': 'dih-SPAHYT (emphasis on second syllable)',
                'etymology': 'From Old French "despit", from Latin "despectus" meaning "looking down"',
                'memory_tips': 'Think "de-spite" - in spite of something',
                'alternate_spellings': 'in spite of, notwithstanding',
                'language_origin': 'Latin via Old French',
                'example_sentence': '_____ the rain, they continued with their picnic.'
            },
            'dessert': {
                'definition': 'A sweet course eaten at the end of a meal; a sweet dish or confection.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-ZURT (emphasis on second syllable)',
                'etymology': 'From French "dessert", from "desservir" meaning "to clear the table"',
                'memory_tips': 'Think "dess-ert" - two s\'s because you want seconds of dessert',
                'alternate_spellings': 'sweet, pudding',
                'language_origin': 'French',
                'example_sentence': 'The chocolate cake was the perfect _____ after dinner.'
            },
            'destination': {
                'definition': 'The place to which someone or something is going or being sent.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'des-tuh-NAY-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "destinatio", from "destinare" meaning "to determine, appoint"',
                'memory_tips': 'Think "destine-ation" - where you\'re destined to go',
                'alternate_spellings': 'endpoint, goal',
                'language_origin': 'Latin',
                'example_sentence': 'Paris was their final _____ on the European tour.'
            },
            'destitution': {
                'definition': 'Poverty so extreme that one lacks the basic necessities of life.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'des-tih-TOO-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "destitutio", from "destituere" meaning "to abandon, forsake"',
                'memory_tips': 'Think "de-stitution" - lacking allstitution (constitution/resources)',
                'alternate_spellings': 'extreme poverty, penury',
                'language_origin': 'Latin',
                'example_sentence': 'The family lived in complete _____ after losing their home.'
            },
            'desuetude': {
                'definition': 'A state of disuse; the condition of not being used.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DES-wi-tood (emphasis on first syllable)',
                'etymology': 'From Latin "desuetudo", from "desuescere" meaning "to become unaccustomed"',
                'memory_tips': 'Think "de-suet-ude" - lacking suet (substance), fallen into disuse',
                'alternate_spellings': 'disuse, obsolescence',
                'language_origin': 'Latin',
                'example_sentence': 'The old law had fallen into _____ and was no longer enforced.'
            },
            'desultorily': {
                'definition': 'In a way that lacks purpose or enthusiasm; halfheartedly; jumping from one thing to another.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'dih-SUHL-tuh-ruh-lee (emphasis on second syllable)',
                'etymology': 'From "desultory" (from Latin "desultorius") + "-ly"',
                'memory_tips': 'Think "de-sultry-ly" - lacking the heat of enthusiasm',
                'alternate_spellings': 'halfheartedly, aimlessly',
                'language_origin': 'Latin',
                'example_sentence': 'He worked _____ on the project, never showing real commitment.'
            },
            'detail': {
                'definition': 'An individual feature, fact, or item; to describe or give an account of something fully.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'dih-TAYL or DEE-tayl (emphasis varies)',
                'etymology': 'From French "détail", from "détailler" meaning "to cut up"',
                'memory_tips': 'Think "de-tail" - the tail end of information',
                'alternate_spellings': 'particular, specifics',
                'language_origin': 'French',
                'example_sentence': 'She explained every _____ of the plan to the team.'
            },
            'detect': {
                'definition': 'To discover or identify the presence or existence of something.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-TEKT (emphasis on second syllable)',
                'etymology': 'From Latin "detectus", past participle of "detegere" meaning "to uncover"',
                'memory_tips': 'Think "de-tect" - to uncover or find something hidden',
                'alternate_spellings': 'discover, identify',
                'language_origin': 'Latin',
                'example_sentence': 'The scientists used special equipment to _____ the presence of the gas.'
            },
            'detention': {
                'definition': 'The action of detaining someone or being detained; confinement as punishment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-TEN-shuhn (emphasis on second syllable)',
                'etymology': 'From Latin "detentio", from "detinere" meaning "to hold back"',
                'memory_tips': 'Think "de-tension" - being held under tension',
                'alternate_spellings': 'confinement, custody',
                'language_origin': 'Latin',
                'example_sentence': 'The student received _____ for disrupting class.'
            },
            'detergent': {
                'definition': 'A cleansing agent, especially a synthetic substitute for soap.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'dih-TUR-juhnt (emphasis on second syllable)',
                'etymology': 'From Latin "detergens", present participle of "detergere" meaning "to wipe away"',
                'memory_tips': 'Think "de-tergent" - something that wipes away (de-terges) dirt',
                'alternate_spellings': 'cleanser, soap',
                'language_origin': 'Latin',
                'example_sentence': 'She added _____ to the washing machine before starting the cycle.'
            },
            'deters': {
                'definition': 'Third person singular of deter; discourages or prevents someone from doing something.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-TURZ (emphasis on second syllable)',
                'etymology': 'From "deter" (from Latin "deterrere") + "-s"',
                'memory_tips': 'Think "de-terrs" - scares away like a deterrent',
                'alternate_spellings': 'discourages, prevents',
                'language_origin': 'Latin',
                'example_sentence': 'The high fence _____ most people from entering the property.'
            },
            'detour': {
                'definition': 'A long or roundabout route taken to avoid something or to visit somewhere.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DEE-toor (emphasis on first syllable)',
                'etymology': 'From French "détour", from "détourner" meaning "to turn aside"',
                'memory_tips': 'Think "de-tour" - turning away from the main tour route',
                'alternate_spellings': 'diversion, bypass',
                'language_origin': 'French',
                'example_sentence': 'They had to take a _____ because of road construction.'
            },
            'detractors': {
                'definition': 'People who criticize or disparage someone or something.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'dih-TRAK-terz (emphasis on second syllable)',
                'etymology': 'From "detract" (from Latin "detrahere") + "-or" + "-s"',
                'memory_tips': 'Think "de-tractors" - people who subtract (detract) from your reputation',
                'alternate_spellings': 'critics, disparagers',
                'language_origin': 'Latin',
                'example_sentence': 'Despite his _____, the artist continued to pursue his vision.'
            },
            'detritus': {
                'definition': 'Waste or debris of any kind; matter produced by erosion.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-TRAHY-tuhs (emphasis on second syllable)',
                'etymology': 'From Latin "detritus", past participle of "deterere" meaning "to wear away"',
                'memory_tips': 'Think "de-tritus" - debris that has been worn away',
                'alternate_spellings': 'debris, waste',
                'language_origin': 'Latin',
                'example_sentence': 'The beach was covered with _____ washed up by the storm.'
            },
            'deuterium': {
                'definition': 'A heavy isotope of hydrogen with one proton and one neutron in its nucleus.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'doo-TEER-ee-uhm (emphasis on second syllable)',
                'etymology': 'From Greek "deuteros" meaning "second" + "-ium"',
                'memory_tips': 'Think "deuter-ium" - the second (deuter) form of hydrogen',
                'alternate_spellings': 'heavy hydrogen',
                'language_origin': 'Greek',
                'example_sentence': '_____ is used in nuclear fusion reactions.'
            },
            'devanagari': {
                'definition': 'A script used for writing Hindi, Sanskrit, and several other Indian languages.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'day-vuh-NAH-guh-ree (emphasis on third syllable)',
                'etymology': 'From Sanskrit "devanagari", from "deva" (divine) + "nagari" (city script)',
                'memory_tips': 'Think "deva-nagari" - divine (deva) city (nagari) script',
                'alternate_spellings': 'Devanagari script',
                'language_origin': 'Sanskrit',
                'example_sentence': 'Hindi is written using the _____ script.'
            },
            'devastavit': {
                'definition': 'In law, a waste of assets by an executor or administrator of an estate.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dev-uh-STAY-vit (emphasis on third syllable)',
                'etymology': 'From Latin "devastavit" meaning "he has wasted"',
                'memory_tips': 'Think "devasta-vit" - devastation of vital assets',
                'alternate_spellings': 'waste of assets',
                'language_origin': 'Latin',
                'example_sentence': 'The court found the executor guilty of _____ for squandering the inheritance.'
            },
            'develop': {
                'definition': 'To grow or cause to grow and become more mature, advanced, or elaborate.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-VEL-uhp (emphasis on second syllable)',
                'etymology': 'From French "développer", from "des-" (reverse) + "veloper" (to wrap)',
                'memory_tips': 'Think "de-velop" - to unwrap (develop) something from its covering',
                'alternate_spellings': 'grow, advance',
                'language_origin': 'French',
                'example_sentence': 'The company plans to _____ new software this year.'
            },
            'developed': {
                'definition': 'Having grown or been brought to a more advanced or elaborate form.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'dih-VEL-uhpt (emphasis on second syllable)',
                'etymology': 'From "develop" (from French "développer") + "-ed"',
                'memory_tips': 'Think "de-veloped" - unwrapped and fully formed',
                'alternate_spellings': 'advanced, mature',
                'language_origin': 'French',
                'example_sentence': 'The _____ countries have better healthcare systems.'
            },
            'developer': {
                'definition': 'A person or company that develops something, especially software or real estate.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-VEL-uh-per (emphasis on second syllable)',
                'etymology': 'From "develop" (from French "développer") + "-er"',
                'memory_tips': 'Think "de-veloper" - one who unwraps and creates things',
                'alternate_spellings': 'creator, builder',
                'language_origin': 'French',
                'example_sentence': 'The software _____ fixed the bug in the latest update.'
            },
            'deviation': {
                'definition': 'The action of departing from an established course; a departure from accepted standards.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dee-vee-AY-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "deviatio", from "deviare" meaning "to turn aside from the way"',
                'memory_tips': 'Think "de-via-tion" - turning away from the via (way)',
                'alternate_spellings': 'departure, divergence',
                'language_origin': 'Latin',
                'example_sentence': 'Any _____ from the flight plan must be reported to air traffic control.'
            },
            'devious': {
                'definition': 'Showing a skillful use of underhanded tactics; deceitful and cunning.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DEE-vee-uhs (emphasis on first syllable)',
                'etymology': 'From Latin "devius", from "de-" + "via" meaning "away from the road"',
                'memory_tips': 'Think "de-vious" - going away from the virtuous path',
                'alternate_spellings': 'cunning, deceitful',
                'language_origin': 'Latin',
                'example_sentence': 'His _____ plan to embezzle money was eventually discovered.'
            },
            'devo': {
                'definition': 'Short for devotional; informal term for religious devotion or a devout person.',
                'part_of_speech': 'noun (informal)',
                'pronunciation_guide': 'DEE-voh (emphasis on first syllable)',
                'etymology': 'Shortened form of "devotional" or "devout"',
                'memory_tips': 'Think "dev-o" - short for devotional',
                'alternate_spellings': 'devotional (full form)',
                'language_origin': 'English (shortened form)',
                'example_sentence': 'The morning _____ included prayer and Bible study.'
            },
            'devoid': {
                'definition': 'Entirely lacking or free from; completely without.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dih-VOID (emphasis on second syllable)',
                'etymology': 'From Old French "desvoidier", from "des-" + "voidier" meaning "to empty"',
                'memory_tips': 'Think "de-void" - made void or empty of something',
                'alternate_spellings': 'lacking, without',
                'language_origin': 'Old French',
                'example_sentence': 'The landscape was _____ of any vegetation.'
            },
            'devotion': {
                'definition': 'Love, loyalty, or enthusiasm for a person, activity, or cause.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-VOH-shuhn (emphasis on second syllable)',
                'etymology': 'From Latin "devotio", from "devovere" meaning "to dedicate"',
                'memory_tips': 'Think "de-votion" - dedicated emotion or feeling',
                'alternate_spellings': 'dedication, loyalty',
                'language_origin': 'Latin',
                'example_sentence': 'Her _____ to her family was evident in everything she did.'
            },
            'devoured': {
                'definition': 'Ate hungrily or quickly; consumed eagerly.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'dih-VOWRD (emphasis on second syllable)',
                'etymology': 'From "devour" (from Latin "devorare") + "-ed"',
                'memory_tips': 'Think "de-voured" - poured down the throat completely',
                'alternate_spellings': 'consumed, gobbled',
                'language_origin': 'Latin',
                'example_sentence': 'He _____ the entire pizza in minutes.'
            },
            'devout': {
                'definition': 'Having or showing deep religious feeling or commitment; totally committed to a cause.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dih-VOWT (emphasis on second syllable)',
                'etymology': 'From Old French "devot", from Latin "devotus" meaning "devoted"',
                'memory_tips': 'Think "de-vout" - deeply committed and vocal about beliefs',
                'alternate_spellings': 'pious, religious',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The _____ believer attended services every day.'
            },
            'dghaisa': {
                'definition': 'A traditional Maltese boat with a high prow and stern, used for fishing and transportation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAHY-sah (emphasis on first syllable)',
                'etymology': 'From Maltese "dgħajsa", related to Arabic boat terminology',
                'memory_tips': 'Think "gai-sa" - a gay (cheerful) sailing vessel',
                'alternate_spellings': 'Maltese boat',
                'language_origin': 'Maltese, Arabic influence',
                'example_sentence': 'The colorful _____ bobbed in the harbor at Valletta.'
            },
            'dhole': {
                'definition': 'A wild dog native to Asia, also known as the Asian wild dog, with reddish fur and a black tail.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOHL (emphasis on first syllable)',
                'etymology': 'From Hindi "dhol" or a related Indian language',
                'memory_tips': 'Think "d-hole" - a dog that lives in holes or dens',
                'alternate_spellings': 'Asian wild dog',
                'language_origin': 'Hindi or related Indian language',
                'example_sentence': 'The pack of _____ hunted together across the Asian grasslands.'
            },
            'dhurrie': {
                'definition': 'A flat-woven rug from India, typically made of cotton or wool with geometric patterns.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DUR-ee (emphasis on first syllable)',
                'etymology': 'From Hindi "dari", meaning "rug" or "carpet"',
                'memory_tips': 'Think "dur-rie" - a durable rug from India',
                'alternate_spellings': 'durrie, dari',
                'language_origin': 'Hindi',
                'example_sentence': 'The colorful _____ added warmth to the wooden floor.'
            },
            'diablo': {
                'definition': 'Spanish for devil; used in English to refer to something devilish or evil.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dee-AH-bloh (emphasis on second syllable)',
                'etymology': 'From Spanish "diablo", from Latin "diabolus" meaning "devil"',
                'memory_tips': 'Think "di-ablo" - the devil in Spanish',
                'alternate_spellings': 'devil (English)',
                'language_origin': 'Spanish via Latin',
                'example_sentence': 'The mountain was named Monte _____ for its treacherous terrain.'
            },
            'diacritic': {
                'definition': 'A mark added to a letter to indicate a particular pronunciation; an accent mark.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'dahy-uh-KRIT-ik (emphasis on third syllable)',
                'etymology': 'From Greek "diakritikos" meaning "distinguishing"',
                'memory_tips': 'Think "dia-critic" - a mark that critically distinguishes sounds',
                'alternate_spellings': 'accent mark',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ mark over the "e" changes the pronunciation of the word.'
            },
            'diadem': {
                'definition': 'A crown or headband worn as a symbol of sovereignty; a jeweled ornament for the head.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DAHY-uh-dem (emphasis on first syllable)',
                'etymology': 'From Greek "diadema", from "diadein" meaning "to bind around"',
                'memory_tips': 'Think "dia-dem" - a diamond (dia) crown for a dame',
                'alternate_spellings': 'crown, tiara',
                'language_origin': 'Greek',
                'example_sentence': 'The queen wore a golden _____ encrusted with precious gems.'
            },
            'dialect': {
                'definition': 'A particular form of a language specific to a region or social group.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DAHY-uh-lekt (emphasis on first syllable)',
                'etymology': 'From Greek "dialektos", from "dialegesthai" meaning "to converse"',
                'memory_tips': 'Think "dia-lect" - different way of speaking that people select',
                'alternate_spellings': 'regional language, vernacular',
                'language_origin': 'Greek',
                'example_sentence': 'The southern _____ had distinctive pronunciations and vocabulary.'
            },
            'dialogue': {
                'definition': 'A conversation between two or more people; an exchange of ideas or opinions.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DAHY-uh-log (emphasis on first syllable)',
                'etymology': 'From Greek "dialogos", from "dia" (through) + "logos" (speech)',
                'memory_tips': 'Think "dia-logue" - speech (logue) going through (dia) people',
                'alternate_spellings': 'dialog, conversation',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ between the characters revealed their true motivations.'
            },
            'dialysis': {
                'definition': 'A medical procedure to remove waste products from the blood when the kidneys cannot.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dahy-AL-uh-sis (emphasis on second syllable)',
                'etymology': 'From Greek "dialysis", from "dialyein" meaning "to dissolve apart"',
                'memory_tips': 'Think "dia-lysis" - dissolving (lysis) things apart (dia)',
                'alternate_spellings': 'blood filtering',
                'language_origin': 'Greek',
                'example_sentence': 'The patient underwent _____ three times a week at the clinic.'
            },
            'diamanté': {
                'definition': 'Fabric decorated with sequins or artificial gems; having a sparkling appearance.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'dee-uh-MAN-tay (emphasis on third syllable)',
                'etymology': 'From French "diamanté", past participle of "diamanter" meaning "to set with diamonds"',
                'memory_tips': 'Think "diamond-té" - decorated like diamonds',
                'alternate_spellings': 'sequined, sparkly',
                'language_origin': 'French',
                'example_sentence': 'Her _____ dress sparkled under the stage lights.'
            },
            'diamond': {
                'definition': 'A precious stone consisting of pure carbon; a shape with four equal sides forming two acute and two obtuse angles.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DAHY-muhnd (emphasis on first syllable)',
                'etymology': 'From Old French "diamant", from Latin "adamantem" meaning "hardest metal"',
                'memory_tips': 'Think "die-mond" - the hardest precious stone that lasts forever',
                'alternate_spellings': 'gem, precious stone',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The engagement ring featured a brilliant-cut _____.'
            },
            'diana': {
                'definition': 'In Roman mythology, the goddess of the hunt and the moon; a female given name.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'dahy-AN-uh (emphasis on second syllable)',
                'etymology': 'From Latin "Diana", possibly related to "divus" meaning "divine"',
                'memory_tips': 'Think "Di-ana" - the divine goddess of hunting',
                'alternate_spellings': 'goddess name',
                'language_origin': 'Latin',
                'example_sentence': '_____ was known as the huntress goddess in Roman mythology.'
            },
            'dianthus': {
                'definition': 'A genus of flowering plants including carnations and pinks, known for their fragrant flowers.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dahy-AN-thuhs (emphasis on second syllable)',
                'etymology': 'From Greek "dianthus", from "dios" (Zeus/divine) + "anthos" (flower)',
                'memory_tips': 'Think "di-anthus" - divine (di) flower (anthus)',
                'alternate_spellings': 'carnation, pink flower',
                'language_origin': 'Greek',
                'example_sentence': 'The garden was filled with colorful _____ blooms.'
            },
            'diapason': {
                'definition': 'The entire range of musical notes; a standard of pitch; a rich, deep sound.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dahy-uh-PAY-zuhn (emphasis on third syllable)',
                'etymology': 'From Greek "dia pason" meaning "through all (notes)"',
                'memory_tips': 'Think "dia-pason" - through (dia) all the musical passages',
                'alternate_spellings': 'musical range, octave',
                'language_origin': 'Greek',
                'example_sentence': 'The organ\'s _____ filled the cathedral with rich, resonant tones.'
            },
            'diaphanous': {
                'definition': 'Light, delicate, and translucent; allowing light to show through.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dahy-AF-uh-nuhs (emphasis on second syllable)',
                'etymology': 'From Greek "diaphanes", from "dia" (through) + "phainein" (to show)',
                'memory_tips': 'Think "dia-phanous" - showing (phanous) through (dia)',
                'alternate_spellings': 'translucent, sheer',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ curtains allowed soft light to filter into the room.'
            },
            'diaphoresis': {
                'definition': 'Profuse sweating, especially as a symptom of disease or a side effect of drugs.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dahy-af-uh-REE-sis (emphasis on fourth syllable)',
                'etymology': 'From Greek "diaphoresis", from "diaphorein" meaning "to carry through"',
                'memory_tips': 'Think "dia-phor-esis" - carrying (phor) moisture through (dia) the skin',
                'alternate_spellings': 'excessive sweating',
                'language_origin': 'Greek',
                'example_sentence': 'The patient experienced _____ as a side effect of the medication.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_050_data:
            return batch_050_data[word_lower]
        
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
    
    def process_batch_050(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 050 with comprehensive Claude data"""
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
    
    def save_batch_050_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 050 processed words to CSV"""
        
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
    """Process Batch 050 with comprehensive Claude data"""
    processor = Batch050Processor()
    input_csv = Path("output/batch_050_words.csv")
    output_csv = Path("output/batch_050_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 050 with comprehensive Claude data...")
    
    # Process all words in batch 050
    processed_words = processor.process_batch_050(input_csv)
    
    # Save results
    processor.save_batch_050_csv(processed_words, output_csv)
    
    logger.info(f"Batch 050 processing completed!")
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