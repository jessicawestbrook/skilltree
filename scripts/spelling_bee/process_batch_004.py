#!/usr/bin/env python3
"""
Process Batch 004 of Spelling Bee Words with Comprehensive Claude Data
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
            'advantage', 'advertisement', 'adviser', 'aerobics', 'aesthetic', 'afar', 'affable', 'affiliate', 'affluent', 'afraid', 'africa', 'again', 'against'
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
            'mega', 'micro', 'mini', 'multi', 'neo', 'pseudo', 'ultra', 'ac', 'ad', 'con', 'af'
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

class Batch004Processor:
    """Processes Batch 004 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 004 words"""
        
        # Comprehensive data for all 50 words in Batch 004
        batch_004_data = {
            'adulation': {
                'definition': 'Excessive admiration or praise; obsequious flattery; worship or devotion that goes beyond what is appropriate or deserved.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'aj-uh-LAY-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "adulatio", from "adulari" meaning "to flatter like a dog"',
                'memory_tips': 'Think "adult-ulation" - adults giving excessive praise like howling',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The celebrity was uncomfortable with the _____ of overzealous fans.'
            },
            'advancing': {
                'definition': 'Moving forward in space or time; making progress; promoting to a higher position; developing or improving.',
                'part_of_speech': 'verb (present participle)',
                'pronunciation_guide': 'ad-VAN-sing (emphasis on second syllable)',
                'etymology': 'From Old French "avancier", from Latin "ab ante" meaning "from before"',
                'memory_tips': 'Think "ad-van-sing" - singing while moving forward in a van',
                'alternate_spellings': '',
                'language_origin': 'Old French via Latin',
                'example_sentence': 'The army was _____ slowly through the difficult terrain.'
            },
            'advantage': {
                'definition': 'A condition or circumstance that puts one in a favorable position; a benefit or gain from a particular situation.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'ad-VAN-tij (emphasis on second syllable)',
                'etymology': 'From Old French "avantage", from "avant" meaning "before"',
                'memory_tips': 'Think "ad-van-tag" - tagging along with a van gives you an advantage',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'Her fluency in three languages gave her a significant _____ in the job market.'
            },
            'advection': {
                'definition': 'The horizontal transfer of heat, moisture, or other atmospheric properties by the movement of air masses.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ad-VEK-shuhn (emphasis on second syllable)',
                'etymology': 'From Latin "advectio", from "advectus" meaning "carried to"',
                'memory_tips': 'Think "ad-vector" - adding vectors to carry atmospheric properties',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The meteorologist explained how _____ brings warm air from the south.'
            },
            'adverb': {
                'definition': 'A word that modifies a verb, adjective, or other adverb, typically ending in -ly and expressing manner, time, or degree.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AD-vurb (emphasis on first syllable)',
                'etymology': 'From Latin "adverbium", from "ad" (to) + "verbum" (word)',
                'memory_tips': 'Think "add-verb" - adding meaning to a verb',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The word "quickly" is an _____ that describes how something is done.'
            },
            'adversaria': {
                'definition': 'Miscellaneous notes or observations; a commonplace book containing random thoughts and remarks.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'ad-vur-SAIR-ee-uh (emphasis on third syllable)',
                'etymology': 'From Latin "adversaria", meaning "things written on the opposite page"',
                'memory_tips': 'Think "adverse-aria" - notes about adverse or opposing ideas',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The scholar\'s _____ contained insights from decades of reading and research.'
            },
            'adversity': {
                'definition': 'Difficult or unpleasant circumstances; hardship, misfortune, or affliction that tests one\'s strength and resilience.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ad-VUR-si-tee (emphasis on second syllable)',
                'etymology': 'From Latin "adversitas", from "adversus" meaning "turned against"',
                'memory_tips': 'Think "adverse-ity" - the quality of things being adverse or against you',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She showed remarkable strength in overcoming the _____ of her childhood.'
            },
            'advertisement': {
                'definition': 'A public notice or announcement promoting a product, service, or event; a paid promotional message in media.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ad-VUR-tiz-muhnt (emphasis on second syllable)',
                'etymology': 'From French "avertissement", from "avertir" meaning "to warn, inform"',
                'memory_tips': 'Think "ad-vert-ise-ment" - turning minds toward a mental announcement',
                'alternate_spellings': 'advert (British)',
                'language_origin': 'French',
                'example_sentence': 'The _____ for the new smartphone appeared on every major website.'
            },
            'advertizement': {
                'definition': 'An archaic or alternative spelling of advertisement; a public notice or promotional announcement.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ad-VUR-tahyz-muhnt (emphasis on second syllable)',
                'etymology': 'Alternative spelling of "advertisement", from French "avertissement"',
                'memory_tips': 'Think "advertize-ment" - older spelling with "z" instead of "s"',
                'alternate_spellings': 'advertisement (modern standard)',
                'language_origin': 'French',
                'example_sentence': 'The old newspaper contained an _____ for patent medicine.'
            },
            'adviser': {
                'definition': 'A person who gives advice or counsel; someone who provides guidance or recommendations, especially in official capacity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ad-VY-zur (emphasis on second syllable)',
                'etymology': 'From "advise" + "-er", from Old French "aviser" meaning "to consider"',
                'memory_tips': 'Think "ad-vise-er" - one who adds wisdom by giving advice',
                'alternate_spellings': 'advisor',
                'language_origin': 'Old French',
                'example_sentence': 'The financial _____ helped the couple plan for their retirement.'
            },
            'advocatory': {
                'definition': 'Having the nature of advocacy; characterized by supporting or recommending a particular cause or policy.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'AD-vuh-kuh-tor-ee (emphasis on first syllable)',
                'etymology': 'From Latin "advocatus" meaning "called to aid" + "-ory"',
                'memory_tips': 'Think "advocate-ory" - relating to the work of an advocate',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The organization took an _____ stance on environmental protection.'
            },
            'advocatoryaerobics': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "advocatory" (supporting) + "aerobics" (exercise).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "advocatory" and "aerobics"',
                'alternate_spellings': 'advocatory + aerobics (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'adzuki': {
                'definition': 'A small reddish-brown bean commonly used in East Asian cuisine; also called azuki bean or red bean.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ad-ZOO-kee (emphasis on second syllable)',
                'etymology': 'From Japanese "azuki" meaning "small bean"',
                'memory_tips': 'Think "ad-zoo-key" - a key to the zoo of small beans',
                'alternate_spellings': 'azuki, aduki',
                'language_origin': 'Japanese',
                'example_sentence': 'The bakery specialized in sweet pastries filled with _____ bean paste.'
            },
            'adélie': {
                'definition': 'A species of penguin found in Antarctica, characterized by a white ring around the eyes and distinctive markings.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'uh-DEL-ee (emphasis on second syllable)',
                'etymology': 'Named after Adélie Land in Antarctica, which was named after Adèle, wife of French explorer Dumont d\'Urville',
                'memory_tips': 'Think "a-Delia" - a penguin named after a French woman named Adèle',
                'alternate_spellings': 'Adelie',
                'language_origin': 'French (proper name)',
                'example_sentence': 'The _____ penguins gathered in large colonies on the Antarctic ice.'
            },
            'aegilops': {
                'definition': 'A genus of grass closely related to wheat; also called goatgrass, important in the evolution and breeding of wheat.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EE-ji-lops (emphasis on first syllable)',
                'etymology': 'From Greek "aegilops", from "aigios" (goat) + "ops" (eye, face)',
                'memory_tips': 'Think "eagle-ops" - eagle operations in grass fields',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Botanists study _____ to understand the genetic diversity of wheat ancestors.'
            },
            'aegrotat': {
                'definition': 'A medical certificate stating that a student is too ill to attend an examination; a degree awarded on such grounds.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EE-groh-tat (emphasis on first syllable)',
                'etymology': 'From Latin "aegrotat" meaning "he is ill"',
                'memory_tips': 'Think "ego-rotat" - your ego rotates when you\'re too sick for exams',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The university granted her an _____ due to her hospitalization during finals.'
            },
            'aerobics': {
                'definition': 'Physical exercises designed to strengthen the cardiovascular system through sustained vigorous activity that increases oxygen consumption.',
                'part_of_speech': 'noun (plural, treated as singular)',
                'pronunciation_guide': 'air-OH-biks (emphasis on second syllable)',
                'etymology': 'From Greek "aer" (air) + "bios" (life) + "-ics"',
                'memory_tips': 'Think "aero-bics" - air-breathing exercise for life',
                'alternate_spellings': '',
                'language_origin': 'Modern Greek',
                'example_sentence': 'She attended _____ classes three times a week to improve her fitness.'
            },
            'aerocele': {
                'definition': 'A medical condition involving an abnormal air-filled swelling or cavity, often in the neck area.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AIR-oh-seel (emphasis on first syllable)',
                'etymology': 'From Greek "aer" (air) + "kele" (tumor, swelling)',
                'memory_tips': 'Think "aero-cell" - air-filled cellular swelling',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The patient developed an _____ following the tracheotomy procedure.'
            },
            'aerophilatelic': {
                'definition': 'Relating to the collection and study of airmail stamps and postal history; concerning aviation postal services.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'air-oh-fil-uh-TEL-ik (emphasis on fourth syllable)',
                'etymology': 'From Greek "aer" (air) + "philos" (loving) + "ateleia" (exemption from tax) + "-ic"',
                'memory_tips': 'Think "aero-philatelic" - loving air mail stamps',
                'alternate_spellings': '',
                'language_origin': 'Modern Greek compound',
                'example_sentence': 'The _____ exhibition featured rare stamps from early aviation postal routes.'
            },
            'aerosol': {
                'definition': 'A substance dispensed from a pressurized container as a fine spray; fine particles suspended in gas.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AIR-uh-sol (emphasis on first syllable)',
                'etymology': 'From Greek "aer" (air) + Latin "solutio" (solution)',
                'memory_tips': 'Think "aero-sol" - air solution in a spray can',
                'alternate_spellings': '',
                'language_origin': 'Greek and Latin combination',
                'example_sentence': 'The _____ spray provided even coverage over the entire surface.'
            },
            'aesir': {
                'definition': 'In Norse mythology, the principal group of gods including Odin, Thor, and Frigg who dwell in Asgard.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'AY-zeer (emphasis on first syllable)',
                'etymology': 'From Old Norse "æsir", plural of "áss" meaning "god"',
                'memory_tips': 'Think "A-seer" - the "A" grade seers or gods of Norse mythology',
                'alternate_spellings': '',
                'language_origin': 'Old Norse',
                'example_sentence': 'In Norse cosmology, the _____ were the primary deities who ruled from Asgard.'
            },
            'aesopian': {
                'definition': 'Relating to Aesop or his fables; characterized by moral instruction through allegory; conveying hidden meaning.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ee-SOP-ee-uhn (emphasis on second syllable)',
                'etymology': 'From Aesop, the ancient Greek fabulist, + "-ian"',
                'memory_tips': 'Think "Aesop-ian" - relating to Aesop\'s moral fables',
                'alternate_spellings': '',
                'language_origin': 'Greek (from proper name)',
                'example_sentence': 'The novel\'s _____ quality made readers search for deeper meanings in simple stories.'
            },
            'aesthetic': {
                'definition': 'Concerned with beauty or the appreciation of beauty; relating to the philosophy of art and taste; pleasing in appearance.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'es-THET-ik (emphasis on second syllable)',
                'etymology': 'From Greek "aisthesis" meaning "sensation, perception"',
                'memory_tips': 'Think "a-thetic" - appreciating beauty is athletic for the mind',
                'alternate_spellings': 'esthetic (alternative)',
                'language_origin': 'Greek',
                'example_sentence': 'The modern building\'s _____ appeal divided critics and the public.'
            },
            'aestival': {
                'definition': 'Relating to or occurring in summer; characteristic of the summer season.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ES-ti-vuhl (emphasis on first syllable)',
                'etymology': 'From Latin "aestivalis", from "aestas" meaning "summer"',
                'memory_tips': 'Think "festival" - summer festivals are aestival celebrations',
                'alternate_spellings': 'estival',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ migration patterns of birds change during the hottest months.'
            },
            'aeterno': {
                'definition': 'Latin phrase meaning "forever" or "for eternity"; used in formal or ceremonial contexts.',
                'part_of_speech': 'adverb (Latin)',
                'pronunciation_guide': 'ay-TUR-noh (emphasis on second syllable)',
                'etymology': 'From Latin "aeternalis", from "aeternus" meaning "eternal"',
                'memory_tips': 'Think "eternal-o" - adding emphasis to eternal',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The inscription promised that their love would last "_____."'
            },
            'aethalium': {
                'definition': 'A large, cushion-like mass of spores formed by certain slime molds; a fruiting body in myxomycetes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ee-THAL-ee-um (emphasis on second syllable)',
                'etymology': 'From Greek "aithalos" meaning "soot, black" + "-ium"',
                'memory_tips': 'Think "eternal-ium" - a structure that seems to last forever',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The biologist photographed the dark _____ growing on the decaying log.'
            },
            'aethaliumaffiche': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "aethalium" (slime mold structure) + "affiche" (poster).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "aethalium" and "affiche"',
                'alternate_spellings': 'aethalium + affiche (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'afar': {
                'definition': 'At or to a great distance; far away in space or time; from a remote location.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'uh-FAHR (emphasis on second syllable)',
                'etymology': 'From Middle English, from "a-" (on) + "far"',
                'memory_tips': 'Think "a-far" - at a distance that is far',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The mountain peaks were visible from _____.'
            },
            'affable': {
                'definition': 'Easy to approach and talk to; friendly, good-natured, and easy to get along with; showing warmth and friendliness.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'AF-uh-buhl (emphasis on first syllable)',
                'etymology': 'From Latin "affabilis", from "affari" meaning "to speak to"',
                'memory_tips': 'Think "af-fab-le" - fabulously friendly and able to chat',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Despite his fame, the actor remained _____ and approachable to fans.'
            },
            'affectionately': {
                'definition': 'In a manner showing fondness or tenderness; with warmth, love, or gentle care; lovingly.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'uh-FEK-shuhn-it-lee (emphasis on second syllable)',
                'etymology': 'From "affection" + "-ate" + "-ly", from Latin "affectio" meaning "disposition"',
                'memory_tips': 'Think "affection-ate-ly" - in a way that shows you ate affection',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She spoke _____ about her grandmother\'s cooking.'
            },
            'affeer': {
                'definition': 'To assess or fix the amount of a fine or penalty; to determine the price or value of something officially.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'uh-FEER (emphasis on second syllable)',
                'etymology': 'From Anglo-French "afferer", from Latin "ad" (to) + "forum" (market)',
                'memory_tips': 'Think "a-fear" - fearing the assessment of a fine',
                'alternate_spellings': '',
                'language_origin': 'Anglo-French via Latin',
                'example_sentence': 'The court will _____ the damages based on the evidence presented.'
            },
            'affenpinscher': {
                'definition': 'A small breed of dog with a monkey-like face, wiry coat, and terrier-like personality; originally from Germany.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AH-fuhn-pin-sher (emphasis on first syllable)',
                'etymology': 'From German "Affe" (monkey) + "Pinscher" (terrier)',
                'memory_tips': 'Think "ape-pin-cher" - a dog that looks like an ape and pinches',
                'alternate_spellings': '',
                'language_origin': 'German',
                'example_sentence': 'The _____ is known for its distinctive mustache and beard-like facial hair.'
            },
            'affianced': {
                'definition': 'Engaged to be married; bound by a promise of marriage; betrothed to another person.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'uh-FY-uhnst (emphasis on second syllable)',
                'etymology': 'From Old French "afiancier", from "afiance" meaning "trust, confidence"',
                'memory_tips': 'Think "a-fiance-ed" - having acquired a fiancé',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The young couple became _____ after a romantic proposal on the beach.'
            },
            'affiche': {
                'definition': 'A poster or public notice, especially one announcing an event; a placard or advertisement displayed publicly.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ah-FEESH (emphasis on second syllable)',
                'etymology': 'From French "affiche", from "afficher" meaning "to post up"',
                'memory_tips': 'Think "a-fish" - a poster fishing for attention',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The vintage _____ advertising the circus was found in an antique shop.'
            },
            'afficionado': {
                'definition': 'A misspelling of "aficionado"; should refer to a person who is very knowledgeable and enthusiastic about an activity or subject.',
                'part_of_speech': 'noun (misspelled)',
                'pronunciation_guide': 'uh-fish-uh-NAH-doh (emphasis on fourth syllable)',
                'etymology': 'Misspelling of Spanish "aficionado", from "afición" meaning "affection, enthusiasm"',
                'memory_tips': 'Think "af-fish-ionado" - but remember the correct spelling has no double "f"',
                'alternate_spellings': 'aficionado (correct spelling)',
                'language_origin': 'Spanish (misspelled)',
                'example_sentence': '[Note: This is a misspelling - the correct word is "aficionado"]'
            },
            'affiliate': {
                'definition': 'To associate or connect with an organization; a person or organization officially connected to a larger group.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'uh-FIL-ee-ayt (emphasis on second syllable)',
                'etymology': 'From Latin "affiliatus", from "ad" (to) + "filius" (son)',
                'memory_tips': 'Think "af-fill-iate" - filling up with connections',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The local station decided to _____ with the national broadcasting network.'
            },
            'affiliateaffluent': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "affiliate" (associate) + "affluent" (wealthy).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "affiliate" and "affluent"',
                'alternate_spellings': 'affiliate + affluent (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'affluent': {
                'definition': 'Having a great deal of money; wealthy and prosperous; abundant or plentiful in supply.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'AF-loo-uhnt (emphasis on first syllable)',
                'etymology': 'From Latin "affluens", from "ad" (to) + "fluere" (to flow)',
                'memory_tips': 'Think "af-fluent" - flowing with wealth and abundance',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ neighborhood featured mansions with manicured gardens.'
            },
            'affogato': {
                'definition': 'An Italian dessert consisting of a scoop of vanilla ice cream or gelato "drowned" in a shot of hot espresso.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ah-foh-GAH-toh (emphasis on third syllable)',
                'etymology': 'From Italian "affogato" meaning "drowned"',
                'memory_tips': 'Think "af-fog-ato" - ice cream fogged and drowned in coffee',
                'alternate_spellings': '',
                'language_origin': 'Italian',
                'example_sentence': 'The restaurant\'s _____ was the perfect end to the Italian meal.'
            },
            'affront': {
                'definition': 'An action or remark that causes outrage or offense; to insult or offend someone deliberately.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'uh-FRUHNT (emphasis on second syllable)',
                'etymology': 'From Old French "afronter", from "a" (to) + "front" (forehead, face)',
                'memory_tips': 'Think "a-front" - facing someone with an insult',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'His rude behavior was an _____ to everyone at the dinner party.'
            },
            'afghan': {
                'definition': 'A knitted or crocheted blanket; a person from Afghanistan; relating to Afghanistan or its people.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'AF-gan (emphasis on first syllable)',
                'etymology': 'From "Afghanistan", from Persian "afghān"',
                'memory_tips': 'Think "af-ghan" - a blanket from the Afghan region',
                'alternate_spellings': '',
                'language_origin': 'Persian',
                'example_sentence': 'Grandmother\'s hand-knitted _____ kept the family warm during winter.'
            },
            'afghanistan': {
                'definition': 'A landlocked country in Central Asia, bordered by Pakistan, Iran, Turkmenistan, Uzbekistan, Tajikistan, and China.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'af-GAN-i-stan (emphasis on second syllable)',
                'etymology': 'From Persian "afghān" (Afghan people) + "stān" (place, land)',
                'memory_tips': 'Think "Afghan-istan" - the land of the Afghan people',
                'alternate_spellings': '',
                'language_origin': 'Persian',
                'example_sentence': 'The ancient Silk Road passed through what is now _____.'
            },
            'aficionado': {
                'definition': 'A person who is very knowledgeable and enthusiastic about an activity, subject, or pastime; a devoted fan or expert.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-fish-uh-NAH-doh (emphasis on fourth syllable)',
                'etymology': 'From Spanish "aficionado", from "afición" meaning "affection, enthusiasm"',
                'memory_tips': 'Think "a-fish-ionado" - someone who has a passion like fishing',
                'alternate_spellings': '',
                'language_origin': 'Spanish',
                'example_sentence': 'As a wine _____, she could identify the vintage and region of any bottle.'
            },
            'aforesaid': {
                'definition': 'Mentioned before; stated or named previously in a document or speech; aforementioned.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'uh-FOR-sed (emphasis on second syllable)',
                'etymology': 'From Middle English "aforeseid", from "afore" (before) + "said"',
                'memory_tips': 'Think "a-fore-said" - said before, previously mentioned',
                'alternate_spellings': 'aforementioned',
                'language_origin': 'Middle English',
                'example_sentence': 'The _____ conditions must be met before the contract is valid.'
            },
            'afraid': {
                'definition': 'Feeling fear or anxiety; worried about possible harm or trouble; reluctant or unwilling due to concern.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'uh-FRAYD (emphasis on second syllable)',
                'etymology': 'From Middle English "affrayed", past participle of "affray" meaning "to frighten"',
                'memory_tips': 'Think "a-frayed" - like frayed nerves from fear',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The child was _____ of the dark and asked for a nightlight.'
            },
            'africa': {
                'definition': 'The second-largest continent in the world, located south of Europe and southwest of Asia, known for its diverse cultures and wildlife.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'AF-ri-kuh (emphasis on first syllable)',
                'etymology': 'From Latin "Africa", possibly from Phoenician "afar" meaning "dust"',
                'memory_tips': 'Think "Af-rica" - a rich continent with diverse cultures',
                'alternate_spellings': '',
                'language_origin': 'Latin, possibly from Phoenician',
                'example_sentence': 'The safari took them across the vast savannas of _____.'
            },
            'afrobeat': {
                'definition': 'A music genre combining jazz, funk, and traditional African music, developed by Nigerian musician Fela Kuti in the 1960s.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AF-roh-beet (emphasis on first syllable)',
                'etymology': 'From "Afro" (African) + "beat" (rhythm)',
                'memory_tips': 'Think "Afro-beat" - African rhythmic beats',
                'alternate_spellings': '',
                'language_origin': 'Modern English compound',
                'example_sentence': 'The festival featured several _____ bands from West Africa.'
            },
            'afroth': {
                'definition': 'Covered with froth or foam; in a frothy state; agitated or excited.',
                'part_of_speech': 'adjective, adverb',
                'pronunciation_guide': 'uh-FROTH (emphasis on second syllable)',
                'etymology': 'From "a-" (in a state of) + "froth"',
                'memory_tips': 'Think "a-froth" - in a state of being frothy',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The rapids left the river _____ with white foam.'
            },
            'again': {
                'definition': 'Once more; another time; in addition; used to indicate repetition of an action or state.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'uh-GEN (emphasis on second syllable)',
                'etymology': 'From Old English "ongeagn", from "on" (on) + "geagn" (against, toward)',
                'memory_tips': 'Think "a-gain" - gaining something once more',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She read the book _____ because she enjoyed it so much.'
            },
            'against': {
                'definition': 'In opposition to; contrary to; in contact with or supported by; in preparation for.',
                'part_of_speech': 'preposition, adverb',
                'pronunciation_guide': 'uh-GENST (emphasis on second syllable)',
                'etymology': 'From Middle English "agenst", from Old English "ongeagn"',
                'memory_tips': 'Think "a-gain-st" - standing again-st something',
                'alternate_spellings': '',
                'language_origin': 'Old English via Middle English',
                'example_sentence': 'The boat struggled _____ the strong current.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_004_data:
            return batch_004_data[word_lower]
        
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
    
    def process_batch_004(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 004 with comprehensive Claude data"""
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
    
    def save_batch_004_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 004 processed words to CSV"""
        
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
    """Process Batch 004 with comprehensive Claude data"""
    processor = Batch004Processor()
    input_csv = Path("output/batch_004_words.csv")
    output_csv = Path("output/batch_004_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 004 with comprehensive Claude data...")
    
    # Process all words in batch 004
    processed_words = processor.process_batch_004(input_csv)
    
    # Save results
    processor.save_batch_004_csv(processed_words, output_csv)
    
    logger.info(f"Batch 004 processing completed!")
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