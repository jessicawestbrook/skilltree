#!/usr/bin/env python3
"""
Process Batch 048 of Spelling Bee Words with Comprehensive Claude Data
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
            'default', 'defeat', 'defense', 'defined', 'definition', 'defy', 'delivery'
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

class Batch048Processor:
    """Processes Batch 048 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 048 words"""
        
        # Comprehensive data for all 50 words in Batch 048
        batch_048_data = {
            'declared': {
                'definition': 'Stated clearly and formally; announced publicly; made known officially.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'dih-KLAIRD (emphasis on second syllable)',
                'etymology': 'From Latin "declaratus", past participle of "declarare" meaning "to make clear"',
                'memory_tips': 'Think "de-clared" - made clear to everyone',
                'alternate_spellings': 'announced, stated',
                'language_origin': 'Latin',
                'example_sentence': 'The president _____ his intention to run for reelection.'
            },
            'declension': {
                'definition': 'In grammar, the variation in the form of a noun, pronoun, or adjective to show case, number, and gender; a decline or deterioration.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-KLEN-shuhn (emphasis on second syllable)',
                'etymology': 'From Latin "declinatio", from "declinare" meaning "to bend away, decline"',
                'memory_tips': 'Think "de-clension" - bending away from the original form',
                'alternate_spellings': 'inflection',
                'language_origin': 'Latin',
                'example_sentence': 'Students learned the _____ of Latin nouns in their grammar class.'
            },
            'declination': {
                'definition': 'A formal refusal; the angular distance of a celestial object from the celestial equator; a downward slope.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dek-luh-NAY-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "declinatio", from "declinare" meaning "to bend away"',
                'memory_tips': 'Think "decline-ation" - the action of declining or bending away',
                'alternate_spellings': 'refusal, slope',
                'language_origin': 'Latin',
                'example_sentence': 'The astronomer measured the star\'s _____ from the celestial equator.'
            },
            'decor': {
                'definition': 'The style of decoration of a room or building; furnishings and ornaments.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-KAWR (emphasis on second syllable)',
                'etymology': 'From French "décor", from Latin "decor" meaning "beauty, grace"',
                'memory_tips': 'Think "deck-or" - decorating the deck or room',
                'alternate_spellings': 'decoration, ornamentation',
                'language_origin': 'Latin via French',
                'example_sentence': 'The interior designer changed the _____ to create a more modern look.'
            },
            'decorative': {
                'definition': 'Serving to make something look more attractive; ornamental rather than functional.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DEK-uh-ray-tiv (emphasis on first syllable)',
                'etymology': 'From "decorate" (from Latin "decorare") + "-ive"',
                'memory_tips': 'Think "decor-ative" - having the quality of decor',
                'alternate_spellings': 'ornamental, aesthetic',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ vase added beauty but served no practical purpose.'
            },
            'decrepitude': {
                'definition': 'The state of being old and in poor condition; physical deterioration due to age.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-KREP-ih-tood (emphasis on second syllable)',
                'etymology': 'From Latin "decrepitus" meaning "worn out, aged"',
                'memory_tips': 'Think "de-crepit-ude" - the condition of being decrepit',
                'alternate_spellings': 'deterioration, decline',
                'language_origin': 'Latin',
                'example_sentence': 'The old building showed signs of _____ after decades of neglect.'
            },
            'decumbiture': {
                'definition': 'In astrology, a chart cast for the moment when someone takes to bed due to illness; the act of lying down.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-KUHM-bi-cher (emphasis on second syllable)',
                'etymology': 'From Latin "decumbere" meaning "to lie down" + "-ture"',
                'memory_tips': 'Think "de-cumber" - lying down to rest',
                'alternate_spellings': 'lying down',
                'language_origin': 'Latin',
                'example_sentence': 'The astrologer cast a _____ chart when the patient fell ill.'
            },
            'decurion': {
                'definition': 'In ancient Rome, a cavalry officer commanding ten men; a member of a town council.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-KYOOR-ee-uhn (emphasis on second syllable)',
                'etymology': 'From Latin "decurio", from "decem" meaning "ten"',
                'memory_tips': 'Think "decu-rion" - an officer of ten (decu = ten)',
                'alternate_spellings': 'Roman officer',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ led his squadron of ten horsemen into battle.'
            },
            'dedicated': {
                'definition': 'Committed to a task or purpose; devoted exclusively to a particular activity or cause.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'DED-ih-kay-tid (emphasis on first syllable)',
                'etymology': 'From Latin "dedicatus", past participle of "dedicare" meaning "to devote"',
                'memory_tips': 'Think "dedic-ated" - having acted to dedicate oneself',
                'alternate_spellings': 'devoted, committed',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ teacher spent extra hours helping struggling students.'
            },
            'deer': {
                'definition': 'A hoofed grazing mammal with branched antlers (in males), found in many parts of the world.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DEER (emphasis on first syllable)',
                'etymology': 'From Old English "deor" meaning "animal, beast"',
                'memory_tips': 'Think "dear" but spelled differently - a beloved forest animal',
                'alternate_spellings': 'stag (male), doe (female)',
                'language_origin': 'Old English',
                'example_sentence': 'The _____ gracefully leaped across the forest clearing.'
            },
            'default': {
                'definition': 'A failure to fulfill an obligation; a preselected option that takes effect without action; to fail to pay a debt.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'dih-FAWLT (emphasis on second syllable)',
                'etymology': 'From Old French "defaute", from "defaillir" meaning "to fail"',
                'memory_tips': 'Think "de-fault" - a fault or failure in doing something',
                'alternate_spellings': 'failure, preset',
                'language_origin': 'Old French',
                'example_sentence': 'The computer will use the _____ settings if no changes are made.'
            },
            'defeat': {
                'definition': 'To win a victory over; to overcome or frustrate; the act of being beaten.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'dih-FEET (emphasis on second syllable)',
                'etymology': 'From Old French "desfait", past participle of "desfaire" meaning "to undo"',
                'memory_tips': 'Think "de-feat" - to undo someone\'s feat or achievement',
                'alternate_spellings': 'overcome, conquer',
                'language_origin': 'Old French',
                'example_sentence': 'The underdog team managed to _____ the defending champions.'
            },
            'defector': {
                'definition': 'A person who abandons their country or cause in favor of an opposing one; a deserter.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-FEK-ter (emphasis on second syllable)',
                'etymology': 'From Latin "defectus" (past participle of "deficere") + "-or"',
                'memory_tips': 'Think "de-fector" - someone who defects from their faction',
                'alternate_spellings': 'deserter, turncoat',
                'language_origin': 'Latin',
                'example_sentence': 'The Cold War _____ revealed important state secrets.'
            },
            'defense': {
                'definition': 'The action of defending from or resisting attack; protection against harm or danger.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-FENS (emphasis on second syllable)',
                'etymology': 'From Old French "defense", from Latin "defensus"',
                'memory_tips': 'Think "de-fense" - putting up a fence to protect',
                'alternate_spellings': 'defence (British)',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The castle\'s strong walls provided an excellent _____.'
            },
            'deference': {
                'definition': 'Respectful submission or yielding to the judgment or wishes of another; courteous regard.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DEF-er-uhns (emphasis on first syllable)',
                'etymology': 'From "defer" (from Latin "deferre") + "-ence"',
                'memory_tips': 'Think "defer-ence" - the quality of deferring to others',
                'alternate_spellings': 'respect, submission',
                'language_origin': 'Latin',
                'example_sentence': 'She showed _____ to her elderly professor\'s expertise.'
            },
            'defiant': {
                'definition': 'Boldly resistant or challenging; openly disobedient; showing contempt for authority.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dih-FAHY-uhnt (emphasis on second syllable)',
                'etymology': 'From "defy" (from Old French "desfier") + "-ant"',
                'memory_tips': 'Think "defy-ant" - acting like an ant that defies authority',
                'alternate_spellings': 'rebellious, resistant',
                'language_origin': 'Old French',
                'example_sentence': 'The _____ teenager refused to follow the curfew rules.'
            },
            'defibrillator': {
                'definition': 'A medical device that delivers an electric shock to the heart to restore normal rhythm during cardiac arrest.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dee-FIB-ruh-lay-ter (emphasis on second syllable)',
                'etymology': 'From "de-" (reverse) + "fibrillation" (irregular heart rhythm) + "-or"',
                'memory_tips': 'Think "de-fibrillator" - removes (de) fibrillation from the heart',
                'alternate_spellings': 'cardiac defibrillator',
                'language_origin': 'Modern medical Latin',
                'example_sentence': 'The paramedic used a _____ to restart the patient\'s heart.'
            },
            'defined': {
                'definition': 'Having exact and clearly stated meaning; clearly outlined or determined.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'dih-FAHYND (emphasis on second syllable)',
                'etymology': 'From Latin "definitus", past participle of "definire" meaning "to limit, determine"',
                'memory_tips': 'Think "de-fined" - having fine, clear boundaries',
                'alternate_spellings': 'specified, determined',
                'language_origin': 'Latin',
                'example_sentence': 'The contract had clearly _____ terms and conditions.'
            },
            'definiendum': {
                'definition': 'In logic and lexicography, the word or phrase that is being defined.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-fin-ee-EN-duhm (emphasis on fourth syllable)',
                'etymology': 'From Latin "definiendum" meaning "that which is to be defined"',
                'memory_tips': 'Think "define-endum" - the thing that needs to be defined',
                'alternate_spellings': 'term being defined',
                'language_origin': 'Latin',
                'example_sentence': 'In the dictionary entry, "cat" is the _____ and the explanation is the definition.'
            },
            'definitely': {
                'definition': 'Without doubt; certainly; in a clearly defined manner.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'DEF-uh-nit-lee (emphasis on first syllable)',
                'etymology': 'From "definite" (from Latin "definitus") + "-ly"',
                'memory_tips': 'Think "definite-ly" - in a definite manner',
                'alternate_spellings': 'certainly, surely',
                'language_origin': 'Latin',
                'example_sentence': 'She will _____ attend the graduation ceremony.'
            },
            'definition': {
                'definition': 'A statement of the exact meaning of a word or phrase; the degree of distinctness in an image or sound.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'def-uh-NISH-uhn (emphasis on third syllable)',
                'etymology': 'From Latin "definitio", from "definire" meaning "to define"',
                'memory_tips': 'Think "define-ition" - the result of defining something',
                'alternate_spellings': 'meaning, explanation',
                'language_origin': 'Latin',
                'example_sentence': 'The dictionary provided a clear _____ of the complex term.'
            },
            'definitions': {
                'definition': 'Plural of definition; multiple explanations of the meanings of words or concepts.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'def-uh-NISH-uhnz (emphasis on third syllable)',
                'etymology': 'Plural of "definition", from Latin "definitio"',
                'memory_tips': 'Think "define-itions" - multiple results of defining things',
                'alternate_spellings': 'meanings, explanations',
                'language_origin': 'Latin',
                'example_sentence': 'The glossary contained _____ for all the technical terms.'
            },
            'defoliant': {
                'definition': 'A chemical agent used to remove leaves from trees and plants; a substance that causes defoliation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-FOH-lee-uhnt (emphasis on second syllable)',
                'etymology': 'From "defoliate" (from Latin "de-" + "folium" meaning leaf) + "-ant"',
                'memory_tips': 'Think "de-foli-ant" - an agent that removes foliage',
                'alternate_spellings': 'leaf-removing agent',
                'language_origin': 'Latin',
                'example_sentence': 'The military used _____ to clear vegetation from the jungle.'
            },
            'defunct': {
                'definition': 'No longer existing or functioning; dead or obsolete.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dih-FUHNGKT (emphasis on second syllable)',
                'etymology': 'From Latin "defunctus", past participle of "defungi" meaning "to finish, die"',
                'memory_tips': 'Think "de-funct" - no longer functional',
                'alternate_spellings': 'obsolete, dead',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ factory stood empty after the company closed.'
            },
            'defy': {
                'definition': 'To openly resist or refuse to obey; to challenge someone to do something believed impossible.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-FAHY (emphasis on second syllable)',
                'etymology': 'From Old French "desfier" meaning "to challenge, distrust"',
                'memory_tips': 'Think "de-fy" - to fly against or oppose',
                'alternate_spellings': 'resist, challenge',
                'language_origin': 'Old French',
                'example_sentence': 'The protesters decided to _____ the government\'s ban on assembly.'
            },
            'degauss': {
                'definition': 'To remove or neutralize the magnetic field of something; to demagnetize.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dee-GOWS (emphasis on second syllable)',
                'etymology': 'From "de-" (reverse) + "gauss" (unit of magnetic field, named after Carl Gauss)',
                'memory_tips': 'Think "de-gauss" - to remove the gauss (magnetism)',
                'alternate_spellings': 'demagnetize',
                'language_origin': 'Named after Carl Friedrich Gauss',
                'example_sentence': 'Technicians _____ the computer monitor to fix the color distortion.'
            },
            'deglaciation': {
                'definition': 'The retreat or melting of glaciers and ice sheets; the process of losing glacial ice.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dee-glay-see-AY-shuhn (emphasis on fourth syllable)',
                'etymology': 'From "de-" (reverse) + "glaciation" (formation of glaciers)',
                'memory_tips': 'Think "de-glaciation" - the reverse of glaciation',
                'alternate_spellings': 'glacier retreat',
                'language_origin': 'Modern scientific term',
                'example_sentence': 'Climate change has accelerated _____ in polar regions.'
            },
            'deglaciationrecruit': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "deglaciation" (glacier retreat) + "recruit" (new member).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "deglaciation" and "recruit"',
                'alternate_spellings': 'deglaciation + recruit (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'deign': {
                'definition': 'To do something that one considers beneath one\'s dignity; to condescend.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'DAYN (emphasis on first syllable)',
                'etymology': 'From Old French "daigner", from Latin "dignari" meaning "to deem worthy"',
                'memory_tips': 'Think "dane" (like a Great Dane) - a noble dog that might deign to notice you',
                'alternate_spellings': 'condescend',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The celebrity would not _____ to sign autographs for fans.'
            },
            'deimos': {
                'definition': 'The smaller and outermost moon of Mars; in Greek mythology, the personification of fear.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'DAHY-mohs (emphasis on first syllable)',
                'etymology': 'From Greek "Deimos" meaning "fear, dread"',
                'memory_tips': 'Think "day-most" - the moon that\'s most fearsome',
                'alternate_spellings': 'Mars moon',
                'language_origin': 'Greek',
                'example_sentence': 'The spacecraft photographed _____ as it orbited Mars.'
            },
            'deities': {
                'definition': 'Plural of deity; gods or goddesses; divine beings worshipped in religions.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'DEE-ih-teez (emphasis on first syllable)',
                'etymology': 'From Latin "deitas" meaning "divine nature", from "deus" meaning "god"',
                'memory_tips': 'Think "dee-ities" - divine entities',
                'alternate_spellings': 'gods, divine beings',
                'language_origin': 'Latin',
                'example_sentence': 'Ancient civilizations worshipped many different _____.'
            },
            'delectable': {
                'definition': 'Extremely pleasing to taste; delightful and enjoyable.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dih-LEK-tuh-buhl (emphasis on second syllable)',
                'etymology': 'From Latin "delectabilis", from "delectare" meaning "to delight"',
                'memory_tips': 'Think "de-lectable" - able to be delighted in',
                'alternate_spellings': 'delicious, delightful',
                'language_origin': 'Latin',
                'example_sentence': 'The chef prepared a _____ feast for the wedding celebration.'
            },
            'delegation': {
                'definition': 'A group of representatives; the action of assigning responsibility to another person.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'del-ih-GAY-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "delegatio", from "delegare" meaning "to send as representative"',
                'memory_tips': 'Think "dele-gation" - a group that has been delegated',
                'alternate_spellings': 'representatives, assignment',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ from France arrived at the international conference.'
            },
            'deleterious': {
                'definition': 'Causing harm or damage; having a harmful effect.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'del-ih-TEER-ee-uhs (emphasis on third syllable)',
                'etymology': 'From Greek "deleterios" meaning "destructive", from "delein" meaning "to hurt"',
                'memory_tips': 'Think "delete-erious" - like deleting something, it causes harm',
                'alternate_spellings': 'harmful, damaging',
                'language_origin': 'Greek',
                'example_sentence': 'Smoking has _____ effects on lung health.'
            },
            'deliberately': {
                'definition': 'On purpose; intentionally; with careful consideration.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'dih-LIB-er-it-lee (emphasis on second syllable)',
                'etymology': 'From "deliberate" (from Latin "deliberatus") + "-ly"',
                'memory_tips': 'Think "deliberate-ly" - in a deliberate manner',
                'alternate_spellings': 'intentionally, purposefully',
                'language_origin': 'Latin',
                'example_sentence': 'She _____ chose to take the more challenging course.'
            },
            'delicacy': {
                'definition': 'The quality of being delicate; a choice or expensive food; something requiring careful handling.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DEL-ih-kuh-see (emphasis on first syllable)',
                'etymology': 'From Latin "delicatus" meaning "delightful, tender"',
                'memory_tips': 'Think "delicate-cy" - the quality of being delicate',
                'alternate_spellings': 'fineness, specialty food',
                'language_origin': 'Latin',
                'example_sentence': 'Caviar is considered a _____ in fine dining.'
            },
            'delicate': {
                'definition': 'Fragile and easily broken; requiring careful handling; subtle or refined.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DEL-ih-kit (emphasis on first syllable)',
                'etymology': 'From Latin "delicatus" meaning "delightful, tender, luxurious"',
                'memory_tips': 'Think "deli-cat" - as gentle as a cat from the deli',
                'alternate_spellings': 'fragile, refined',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ china required special care when washing.'
            },
            'delicious': {
                'definition': 'Having a very pleasant taste; highly enjoyable.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dih-LISH-uhs (emphasis on second syllable)',
                'etymology': 'From Latin "deliciosus", from "delicia" meaning "delight, pleasure"',
                'memory_tips': 'Think "de-licious" - bringing delight to your taste',
                'alternate_spellings': 'tasty, delectable',
                'language_origin': 'Latin',
                'example_sentence': 'The homemade apple pie was absolutely _____.'
            },
            'delight': {
                'definition': 'A feeling of great pleasure; something that gives joy; to please greatly.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'dih-LAHYT (emphasis on second syllable)',
                'etymology': 'From Old French "delit", from Latin "delectare" meaning "to charm"',
                'memory_tips': 'Think "de-light" - bringing light and joy',
                'alternate_spellings': 'joy, pleasure',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The children squealed with _____ when they saw the presents.'
            },
            'delinquent': {
                'definition': 'Failing in duty; overdue in payment; a young person who regularly breaks the law.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'dih-LING-kwuhnt (emphasis on second syllable)',
                'etymology': 'From Latin "delinquens", present participle of "delinquere" meaning "to fail"',
                'memory_tips': 'Think "de-linquent" - failing to stay in line',
                'alternate_spellings': 'defaulting, wayward',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ teenager was sentenced to community service.'
            },
            'deliquesce': {
                'definition': 'To become liquid by absorbing moisture from the air; to melt away gradually.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'del-ih-KWES (emphasis on third syllable)',
                'etymology': 'From Latin "deliquescere", from "de-" + "liquescere" meaning "to become liquid"',
                'memory_tips': 'Think "de-liquesce" - to become liquid (liquesce)',
                'alternate_spellings': 'dissolve, melt',
                'language_origin': 'Latin',
                'example_sentence': 'Salt crystals _____ in humid air.'
            },
            'delivery': {
                'definition': 'The action of bringing goods or mail to a destination; the process of giving birth; manner of speaking.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-LIV-uh-ree (emphasis on second syllable)',
                'etymology': 'From "deliver" (from Old French "delivrer") + "-y"',
                'memory_tips': 'Think "de-liver-y" - taking something from liver to destination',
                'alternate_spellings': 'transport, birth',
                'language_origin': 'Old French',
                'example_sentence': 'The _____ truck arrived with the furniture at noon.'
            },
            'delmarva': {
                'definition': 'A peninsula on the East Coast of the United States, comprising parts of Delaware, Maryland, and Virginia.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'del-MAHR-vah (emphasis on second syllable)',
                'etymology': 'Portmanteau of Delaware, Maryland, and Virginia',
                'memory_tips': 'Think "Del-Mar-Va" - Delaware + Maryland + Virginia',
                'alternate_spellings': 'Delmarva Peninsula',
                'language_origin': 'Modern English portmanteau',
                'example_sentence': 'The _____ Peninsula is known for its seafood industry.'
            },
            'delphinium': {
                'definition': 'A tall garden plant with spikes of blue, pink, or white flowers; larkspur.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'del-FIN-ee-uhm (emphasis on second syllable)',
                'etymology': 'From Greek "delphinium", from "delphis" meaning "dolphin" (shape of flower bud)',
                'memory_tips': 'Think "delphin-ium" - dolphin-shaped flower',
                'alternate_spellings': 'larkspur',
                'language_origin': 'Greek',
                'example_sentence': 'The blue _____ flowers added height to the garden border.'
            },
            'delta': {
                'definition': 'The fourth letter of the Greek alphabet; a triangular area of land at a river mouth; a change or difference.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DEL-tah (emphasis on first syllable)',
                'etymology': 'From Greek "delta", named after the triangular shape of the letter Δ',
                'memory_tips': 'Think of the triangle shape Δ - like land at a river mouth',
                'alternate_spellings': 'river mouth, triangle',
                'language_origin': 'Greek',
                'example_sentence': 'The Nile _____ is a fertile region in Egypt.'
            },
            'deltoidal': {
                'definition': 'Having a triangular shape; resembling the Greek letter delta (Δ).',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'del-TOY-duhl (emphasis on second syllable)',
                'etymology': 'From "delta" (Greek letter) + "-oidal" (having the form of)',
                'memory_tips': 'Think "delta-oidal" - having the form of delta (triangle)',
                'alternate_spellings': 'triangular, delta-shaped',
                'language_origin': 'Greek',
                'example_sentence': 'The muscle has a _____ shape similar to an inverted triangle.'
            },
            'demeanor': {
                'definition': 'A person\'s outward behavior or bearing; the way someone conducts themselves.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-MEE-ner (emphasis on second syllable)',
                'etymology': 'From "demean" (from Old French "demener") + "-or"',
                'memory_tips': 'Think "de-mean-or" - how someone means to present themselves',
                'alternate_spellings': 'behavior, bearing',
                'language_origin': 'Old French',
                'example_sentence': 'His calm _____ helped diffuse the tense situation.'
            },
            'demeanour': {
                'definition': 'British spelling of demeanor; a person\'s outward behavior or bearing.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-MEE-ner (emphasis on second syllable)',
                'etymology': 'British spelling of "demeanor", from Old French "demener"',
                'memory_tips': 'Think "de-mean-our" - how we mean to present ourselves',
                'alternate_spellings': 'demeanor (American)',
                'language_origin': 'Old French',
                'example_sentence': 'Her professional _____ impressed the interview panel.'
            },
            'dementia': {
                'definition': 'A chronic disorder of mental processes caused by brain disease; severe loss of cognitive function.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-MEN-shuh (emphasis on second syllable)',
                'etymology': 'From Latin "dementia", from "demens" meaning "out of one\'s mind"',
                'memory_tips': 'Think "de-mentis" - away from normal mental state',
                'alternate_spellings': 'cognitive decline',
                'language_origin': 'Latin',
                'example_sentence': 'The elderly man was diagnosed with early-stage _____.'
            },
            'demerits': {
                'definition': 'Faults or disadvantages; points deducted for poor performance or behavior.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'dih-MER-its (emphasis on second syllable)',
                'etymology': 'From "de-" (negative) + "merits" (good points)',
                'memory_tips': 'Think "de-merits" - the opposite of merits',
                'alternate_spellings': 'faults, disadvantages',
                'language_origin': 'Latin prefix + English',
                'example_sentence': 'The student received _____ for arriving late to class repeatedly.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_048_data:
            return batch_048_data[word_lower]
        
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
    
    def process_batch_048(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 048 with comprehensive Claude data"""
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
    
    def save_batch_048_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 048 processed words to CSV"""
        
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
    """Process Batch 048 with comprehensive Claude data"""
    processor = Batch048Processor()
    input_csv = Path("output/batch_048_words.csv")
    output_csv = Path("output/batch_048_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 048 with comprehensive Claude data...")
    
    # Process all words in batch 048
    processed_words = processor.process_batch_048(input_csv)
    
    # Save results
    processor.save_batch_048_csv(processed_words, output_csv)
    
    logger.info(f"Batch 048 processing completed!")
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