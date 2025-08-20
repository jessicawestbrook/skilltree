#!/usr/bin/env python3
"""
Process Batch 049 of Spelling Bee Words with Comprehensive Claude Data
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
            'default', 'defeat', 'defense', 'defined', 'definition', 'defy', 'delivery', 'deny', 'department', 'describe', 'describes'
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

class Batch049Processor:
    """Processes Batch 049 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 049 words"""
        
        # Comprehensive data for all 50 words in Batch 049
        batch_049_data = {
            'demigod': {
                'definition': 'A being with partial divine status; a person who is greatly admired or feared.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DEM-ee-god (emphasis on first syllable)',
                'etymology': 'From "demi-" (half) + "god"',
                'memory_tips': 'Think "demi-god" - half god, half mortal',
                'alternate_spellings': 'semi-divine being',
                'language_origin': 'Greek prefix + English',
                'example_sentence': 'Hercules was considered a _____ in Greek mythology.'
            },
            'demitasse': {
                'definition': 'A small cup used for serving strong black coffee, especially espresso; the coffee itself.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DEM-ih-tas (emphasis on first syllable)',
                'etymology': 'From French "demi-tasse" meaning "half-cup"',
                'memory_tips': 'Think "demi-tasse" - half the size of a regular coffee cup',
                'alternate_spellings': 'espresso cup',
                'language_origin': 'French',
                'example_sentence': 'After dinner, she served coffee in delicate _____ cups.'
            },
            'demographics': {
                'definition': 'Statistical data relating to the population and particular groups within it.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dem-uh-GRAF-iks (emphasis on third syllable)',
                'etymology': 'From Greek "demos" (people) + "graphikos" (writing, description)',
                'memory_tips': 'Think "demo-graphics" - graphics about the demo (people)',
                'alternate_spellings': 'population statistics',
                'language_origin': 'Greek',
                'example_sentence': 'The marketing team studied the _____ of their target audience.'
            },
            'demolitiongargantuan': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "demolition" (destruction) + "gargantuan" (enormous).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "demolition" and "gargantuan"',
                'alternate_spellings': 'demolition + gargantuan (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'demonstrative': {
                'definition': 'Clearly showing the existence or truth of something; tending to show feelings openly; a word that points to something.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'dih-MON-struh-tiv (emphasis on second syllable)',
                'etymology': 'From Latin "demonstrativus", from "demonstrare" meaning "to show"',
                'memory_tips': 'Think "demon-strative" - showing like a demonstration',
                'alternate_spellings': 'illustrative, expressive',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ pronoun "this" points to a specific object.'
            },
            'demulcent': {
                'definition': 'Having a soothing effect; relieving inflammation or irritation, especially of mucous membranes.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'dih-MUHL-suhnt (emphasis on second syllable)',
                'etymology': 'From Latin "demulcens", from "demulcere" meaning "to stroke down, soothe"',
                'memory_tips': 'Think "de-mulcent" - calming down (de) the irritation',
                'alternate_spellings': 'soothing, mollifying',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ properties of honey help soothe a sore throat.'
            },
            'demure': {
                'definition': 'Reserved, modest, and shy in manner or appearance; affectedly modest.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dih-MYOOR (emphasis on second syllable)',
                'etymology': 'From Old French "demure", possibly from "de-" + "meur" (ripe, mature)',
                'memory_tips': 'Think "de-mature" - acting in a mature, modest way',
                'alternate_spellings': 'modest, reserved',
                'language_origin': 'Old French',
                'example_sentence': 'She gave a _____ smile and looked down shyly.'
            },
            'demurrage': {
                'definition': 'A charge payable to the owner of a chartered ship for failure to load or discharge the ship within the agreed time.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-MUR-ij (emphasis on second syllable)',
                'etymology': 'From Old French "demorage", from "demorer" meaning "to delay"',
                'memory_tips': 'Think "de-murrage" - a charge for delaying (de-mouring)',
                'alternate_spellings': 'delay charge',
                'language_origin': 'Old French',
                'example_sentence': 'The shipping company had to pay _____ fees for the delayed cargo.'
            },
            'dendrochronology': {
                'definition': 'The scientific method of dating tree rings to determine the age of trees and study climate patterns.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'den-droh-kruh-NOL-uh-jee (emphasis on fourth syllable)',
                'etymology': 'From Greek "dendron" (tree) + "chronos" (time) + "logos" (study)',
                'memory_tips': 'Think "dendro-chrono-logy" - tree (dendro) time (chrono) study (logy)',
                'alternate_spellings': 'tree ring dating',
                'language_origin': 'Greek',
                'example_sentence': 'Scientists used _____ to determine the age of the ancient forest.'
            },
            'dengue': {
                'definition': 'A tropical disease transmitted by mosquitoes, causing fever, headache, and joint pain.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DENG-ee or den-GAY (emphasis varies)',
                'etymology': 'From Spanish "dengue", possibly from Swahili "ki-denga"',
                'memory_tips': 'Think "den-gue" - a disease that puts you in a den (bed)',
                'alternate_spellings': 'dengue fever',
                'language_origin': 'Spanish, possibly from Swahili',
                'example_sentence': 'The tropical region had an outbreak of _____ fever.'
            },
            'denizen': {
                'definition': 'An inhabitant or occupant of a particular place; a foreigner admitted to certain rights of citizenship.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DEN-ih-zuhn (emphasis on first syllable)',
                'etymology': 'From Old French "deinzein", from "deins" meaning "within"',
                'memory_tips': 'Think "den-izen" - a citizen of the den (place)',
                'alternate_spellings': 'inhabitant, resident',
                'language_origin': 'Old French',
                'example_sentence': 'The old owl was a longtime _____ of the forest.'
            },
            'denominator': {
                'definition': 'The number below the line in a fraction; a common feature or characteristic shared by members of a group.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-NOM-uh-nay-ter (emphasis on second syllable)',
                'etymology': 'From Latin "denominare" meaning "to name" + "-ator"',
                'memory_tips': 'Think "de-nominator" - the number that names what the fraction represents',
                'alternate_spellings': 'bottom number, common factor',
                'language_origin': 'Latin',
                'example_sentence': 'In the fraction 3/4, the _____ is 4.'
            },
            'denouement': {
                'definition': 'The final outcome of the main dramatic complication in a literary work; the climax of a chain of events.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'day-noo-MAHN (emphasis on third syllable)',
                'etymology': 'From French "dénouement", from "dénouer" meaning "to untie"',
                'memory_tips': 'Think "de-nouement" - untying (de-nouer) the plot knots',
                'alternate_spellings': 'resolution, climax',
                'language_origin': 'French',
                'example_sentence': 'The _____ revealed that the butler was the murderer.'
            },
            'denouncement': {
                'definition': 'The action of publicly declaring something or someone to be wrong or evil; condemnation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-NOWNS-muhnt (emphasis on second syllable)',
                'etymology': 'From "denounce" (from Latin "denuntiare") + "-ment"',
                'memory_tips': 'Think "de-nounce-ment" - the act of denouncing',
                'alternate_spellings': 'condemnation, denunciation',
                'language_origin': 'Latin',
                'example_sentence': 'The speech was a fierce _____ of government corruption.'
            },
            'denticulate': {
                'definition': 'Having small teeth or tooth-like projections; finely toothed.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'den-TIK-yuh-lit (emphasis on second syllable)',
                'etymology': 'From Latin "denticulatus", from "denticulus" meaning "small tooth"',
                'memory_tips': 'Think "denti-culate" - having little teeth (denti)',
                'alternate_spellings': 'toothed, serrated',
                'language_origin': 'Latin',
                'example_sentence': 'The leaf had a _____ edge with tiny tooth-like projections.'
            },
            'dentifrice': {
                'definition': 'A paste or powder for cleaning the teeth; toothpaste.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DEN-tuh-fris (emphasis on first syllable)',
                'etymology': 'From Latin "dentifricium", from "dens" (tooth) + "fricare" (to rub)',
                'memory_tips': 'Think "denti-frice" - something to rub (frice) teeth (denti)',
                'alternate_spellings': 'toothpaste, tooth powder',
                'language_origin': 'Latin',
                'example_sentence': 'The ancient Romans used a primitive _____ to clean their teeth.'
            },
            'deny': {
                'definition': 'To declare untrue; to refuse to give or grant something; to disown or reject.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-NAHY (emphasis on second syllable)',
                'etymology': 'From Old French "denier", from Latin "denegare" meaning "to refuse"',
                'memory_tips': 'Think "de-ny" - to negate (ny sounds like nay)',
                'alternate_spellings': 'refuse, reject',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The suspect continued to _____ any involvement in the crime.'
            },
            'department': {
                'definition': 'A division of a large organization; a section of a store; an administrative district.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-PAHRT-muhnt (emphasis on second syllable)',
                'etymology': 'From French "département", from "départir" meaning "to divide"',
                'memory_tips': 'Think "de-part-ment" - a part that has been divided off',
                'alternate_spellings': 'division, section',
                'language_origin': 'French',
                'example_sentence': 'She works in the marketing _____ of the company.'
            },
            'dependable': {
                'definition': 'Trustworthy and reliable; able to be depended upon.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dih-PEN-duh-buhl (emphasis on second syllable)',
                'etymology': 'From "depend" (from Latin "dependere") + "-able"',
                'memory_tips': 'Think "depend-able" - able to be depended on',
                'alternate_spellings': 'reliable, trustworthy',
                'language_origin': 'Latin',
                'example_sentence': 'The old car was still _____ after twenty years.'
            },
            'depilatory': {
                'definition': 'Used to remove unwanted hair; a cream or device for hair removal.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'dih-PIL-uh-tawr-ee (emphasis on second syllable)',
                'etymology': 'From Latin "depilatorius", from "depilare" meaning "to pluck out hair"',
                'memory_tips': 'Think "de-pil-atory" - removing (de) hair (pil like pile)',
                'alternate_spellings': 'hair removal',
                'language_origin': 'Latin',
                'example_sentence': 'She used a _____ cream to remove unwanted leg hair.'
            },
            'deportment': {
                'definition': 'A person\'s behavior or manners; the way one conducts oneself.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-PAWRT-muhnt (emphasis on second syllable)',
                'etymology': 'From "deport" (from Latin "deportare") + "-ment"',
                'memory_tips': 'Think "de-port-ment" - how you port (carry) yourself',
                'alternate_spellings': 'behavior, conduct',
                'language_origin': 'Latin',
                'example_sentence': 'The finishing school taught proper _____ and etiquette.'
            },
            'depose': {
                'definition': 'To remove from office; to testify under oath; to state or assert.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-POHZ (emphasis on second syllable)',
                'etymology': 'From Old French "deposer", from Latin "deponere" meaning "to put down"',
                'memory_tips': 'Think "de-pose" - to remove from a posed position of power',
                'alternate_spellings': 'remove, testify',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The witness was asked to _____ in front of the grand jury.'
            },
            'deposited': {
                'definition': 'Placed or stored in a particular location; put money into a bank account.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'dih-POZ-ih-tid (emphasis on second syllable)',
                'etymology': 'From "deposit" (from Latin "depositum") + "-ed"',
                'memory_tips': 'Think "de-posited" - placed in a position (deposit)',
                'alternate_spellings': 'placed, stored',
                'language_origin': 'Latin',
                'example_sentence': 'She _____ the check into her savings account.'
            },
            'deposition': {
                'definition': 'The action of depositing something; testimony given under oath; the removal of someone from office.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dep-uh-ZISH-uhn (emphasis on third syllable)',
                'etymology': 'From Latin "depositio", from "deponere" meaning "to put down"',
                'memory_tips': 'Think "de-position" - removing from position or putting down testimony',
                'alternate_spellings': 'testimony, removal',
                'language_origin': 'Latin',
                'example_sentence': 'The lawyer scheduled a _____ with the key witness.'
            },
            'deposits': {
                'definition': 'Plural of deposit; sums of money placed in bank accounts; natural accumulations of minerals.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'dih-POZ-its (emphasis on second syllable)',
                'etymology': 'Plural of "deposit", from Latin "depositum"',
                'memory_tips': 'Think "de-posits" - multiple things positioned or placed',
                'alternate_spellings': 'placements, accumulations',
                'language_origin': 'Latin',
                'example_sentence': 'The geologist found rich mineral _____ in the mountain.'
            },
            'depot': {
                'definition': 'A storage facility; a railroad or bus station; a military supply base.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DEE-poh or DEP-oh (emphasis on first syllable)',
                'etymology': 'From French "dépôt", from Latin "depositum" meaning "something deposited"',
                'memory_tips': 'Think "de-pot" - a pot (container) for depositing things',
                'alternate_spellings': 'station, warehouse',
                'language_origin': 'Latin via French',
                'example_sentence': 'The old train _____ was converted into a museum.'
            },
            'depravity': {
                'definition': 'Moral corruption; wickedness; the state of being depraved.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-PRAV-ih-tee (emphasis on second syllable)',
                'etymology': 'From "deprave" (from Latin "depravare") + "-ity"',
                'memory_tips': 'Think "de-prav-ity" - the state of being depraved',
                'alternate_spellings': 'corruption, wickedness',
                'language_origin': 'Latin',
                'example_sentence': 'The novel explored the _____ of human nature.'
            },
            'depreciate': {
                'definition': 'To decrease in value over time; to belittle or disparage.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-PREE-shee-ayt (emphasis on second syllable)',
                'etymology': 'From Latin "depretiare", from "de-" + "pretium" meaning "price"',
                'memory_tips': 'Think "de-price-iate" - to reduce the price or value',
                'alternate_spellings': 'devalue, diminish',
                'language_origin': 'Latin',
                'example_sentence': 'New cars _____ rapidly in their first year.'
            },
            'depredation': {
                'definition': 'An act of attacking and robbing; plundering; destructive action.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dep-rih-DAY-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "depraedatio", from "depraedari" meaning "to plunder"',
                'memory_tips': 'Think "de-predation" - predatory behavior that destroys',
                'alternate_spellings': 'plundering, pillaging',
                'language_origin': 'Latin',
                'example_sentence': 'The Viking _____ left the coastal village in ruins.'
            },
            'deprivation': {
                'definition': 'The damaging lack of material benefits; the action of taking something away.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dep-ruh-VAY-shuhn (emphasis on third syllable)',
                'etymology': 'From "deprive" (from Latin "deprivare") + "-ation"',
                'memory_tips': 'Think "de-priv-ation" - the action of removing privileges',
                'alternate_spellings': 'lack, want',
                'language_origin': 'Latin',
                'example_sentence': 'Sleep _____ can seriously affect your health.'
            },
            'depths': {
                'definition': 'The deepest or most intense parts of something; the bottom of a body of water.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'DEPTHS (emphasis on first syllable)',
                'etymology': 'From "depth" (from Old English "deop") + "-s"',
                'memory_tips': 'Think "dep-ths" - the deepest parts',
                'alternate_spellings': 'deepest parts, bottom',
                'language_origin': 'Old English',
                'example_sentence': 'The submarine explored the ocean _____.'
            },
            'deputy': {
                'definition': 'A person appointed to act as a substitute for another; an assistant with power to act.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DEP-yuh-tee (emphasis on first syllable)',
                'etymology': 'From Old French "deputé", from Latin "deputare" meaning "to assign"',
                'memory_tips': 'Think "dep-uty" - someone deputized to help',
                'alternate_spellings': 'assistant, substitute',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The sheriff appointed a _____ to patrol the rural areas.'
            },
            'derby': {
                'definition': 'A horse race; a stiff felt hat with a rounded crown; any sporting contest.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DUR-bee (emphasis on first syllable)',
                'etymology': 'Named after the Earl of Derby, who founded the famous horse race',
                'memory_tips': 'Think "Derby" - the famous horse race and hat style',
                'alternate_spellings': 'bowler hat, race',
                'language_origin': 'English (proper name)',
                'example_sentence': 'The Kentucky _____ is known as "the most exciting two minutes in sports."'
            },
            'derecho': {
                'definition': 'A widespread, long-lived windstorm with bands of rapidly moving thunderstorms.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'duh-RAY-choh (emphasis on second syllable)',
                'etymology': 'From Spanish "derecho" meaning "straight" (referring to straight-line winds)',
                'memory_tips': 'Think "de-recho" - straight (derecho) destructive winds',
                'alternate_spellings': 'land hurricane',
                'language_origin': 'Spanish',
                'example_sentence': 'The _____ caused widespread power outages across three states.'
            },
            'derelict': {
                'definition': 'Abandoned and in poor condition; neglectful of duty; a person without a home or job.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'DER-uh-likt (emphasis on first syllable)',
                'etymology': 'From Latin "derelictus", past participle of "derelinquere" meaning "to abandon"',
                'memory_tips': 'Think "de-relict" - abandoned and wrecked',
                'alternate_spellings': 'abandoned, neglected',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ building was scheduled for demolition.'
            },
            'derelictderisive': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "derelict" (abandoned) + "derisive" (mocking).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "derelict" and "derisive"',
                'alternate_spellings': 'derelict + derisive (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'derisive': {
                'definition': 'Expressing contempt or ridicule; mocking in a scornful way.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dih-RAHY-siv (emphasis on second syllable)',
                'etymology': 'From "deride" (from Latin "deridere") + "-ive"',
                'memory_tips': 'Think "de-risive" - causing others to rise up in mockery',
                'alternate_spellings': 'mocking, scornful',
                'language_origin': 'Latin',
                'example_sentence': 'His _____ laughter made her feel embarrassed about her mistake.'
            },
            'derivative': {
                'definition': 'Something that is based on or derived from another source; lacking originality.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'dih-RIV-uh-tiv (emphasis on second syllable)',
                'etymology': 'From "derive" (from Latin "derivare") + "-ative"',
                'memory_tips': 'Think "de-riv-ative" - something that flows (riv like river) from another source',
                'alternate_spellings': 'derived, secondary',
                'language_origin': 'Latin',
                'example_sentence': 'The movie was criticized as a _____ work lacking original ideas.'
            },
            'derived': {
                'definition': 'Obtained from a specified source; developed or originated from something else.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'dih-RAHYVD (emphasis on second syllable)',
                'etymology': 'From Latin "derivatus", past participle of "derivare" meaning "to draw off"',
                'memory_tips': 'Think "de-rived" - drawn off like water from a river',
                'alternate_spellings': 'obtained, originated',
                'language_origin': 'Latin',
                'example_sentence': 'The medicine is _____ from a tropical plant extract.'
            },
            'derogatory': {
                'definition': 'Showing a critical or disrespectful attitude; disparaging.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dih-ROG-uh-tawr-ee (emphasis on second syllable)',
                'etymology': 'From Latin "derogatorius", from "derogare" meaning "to detract from"',
                'memory_tips': 'Think "de-rog-atory" - speech that rogs (diminishes) someone',
                'alternate_spellings': 'disparaging, belittling',
                'language_origin': 'Latin',
                'example_sentence': 'She was offended by his _____ comments about her work.'
            },
            'derrick': {
                'definition': 'A type of crane with a movable pivoted arm; a framework over an oil well.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DER-ik (emphasis on first syllable)',
                'etymology': 'Named after Derrick, a famous 17th-century English hangman',
                'memory_tips': 'Think of Derek the crane operator - derrick sounds like Derek',
                'alternate_spellings': 'crane, tower',
                'language_origin': 'English (proper name)',
                'example_sentence': 'The oil _____ towered over the drilling site.'
            },
            'derring': {
                'definition': 'Daring action; brave or audacious conduct (usually in "derring-do").',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DER-ing (emphasis on first syllable)',
                'etymology': 'From Middle English "derring do" meaning "daring to do"',
                'memory_tips': 'Think "derring-do" - daring deeds of courage',
                'alternate_spellings': 'daring, courage',
                'language_origin': 'Middle English',
                'example_sentence': 'The knights were famous for their tales of _____ and adventure.'
            },
            'descent': {
                'definition': 'An action of moving downward; a person\'s origin or background; a decline.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-SENT (emphasis on second syllable)',
                'etymology': 'From Old French "descente", from Latin "descendere" meaning "to climb down"',
                'memory_tips': 'Think "de-scent" - going down from a high scent (height)',
                'alternate_spellings': 'decline, ancestry',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The airplane began its _____ toward the runway.'
            },
            'describe': {
                'definition': 'To give an account in words of someone or something; to say what something is like.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-SKRAHYB (emphasis on second syllable)',
                'etymology': 'From Latin "describere", from "de-" + "scribere" meaning "to write"',
                'memory_tips': 'Think "de-scribe" - to write down details about something',
                'alternate_spellings': 'explain, detail',
                'language_origin': 'Latin',
                'example_sentence': 'Can you _____ what the suspect looked like?'
            },
            'describes': {
                'definition': 'Third person singular present of describe; gives an account of something.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-SKRAHYBZ (emphasis on second syllable)',
                'etymology': 'From "describe" (from Latin "describere") + "-s"',
                'memory_tips': 'Think "de-scribes" - writes down descriptions',
                'alternate_spellings': 'explains, details',
                'language_origin': 'Latin',
                'example_sentence': 'The witness _____ the events in great detail.'
            },
            'desecration': {
                'definition': 'The action of treating a sacred place or thing with violent disrespect.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'des-ih-KRAY-shuhn (emphasis on third syllable)',
                'etymology': 'From "desecrate" (from Latin "desacrare") + "-ion"',
                'memory_tips': 'Think "de-secr-ation" - removing (de) the sacred (secr) nature',
                'alternate_spellings': 'defilement, profanation',
                'language_origin': 'Latin',
                'example_sentence': 'The vandalism was considered a _____ of the historic monument.'
            },
            'deseret': {
                'definition': 'A name meaning "honeybee" in the Book of Mormon; the proposed name for Utah Territory.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'dez-uh-RET (emphasis on third syllable)',
                'etymology': 'From the Book of Mormon, meaning "honeybee"',
                'memory_tips': 'Think "desert-et" - like a small desert, but actually means honeybee',
                'alternate_spellings': 'honeybee (translation)',
                'language_origin': 'Book of Mormon language',
                'example_sentence': 'The early Mormon settlers wanted to name their territory _____.'
            },
            'deserter': {
                'definition': 'A person who abandons their duty, especially a member of the armed forces who leaves without permission.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-ZUR-ter (emphasis on second syllable)',
                'etymology': 'From "desert" (abandon, from Latin "deserere") + "-er"',
                'memory_tips': 'Think "de-serter" - someone who serves (sert) no more',
                'alternate_spellings': 'defector, runaway',
                'language_origin': 'Latin',
                'example_sentence': 'The military court tried the _____ for abandoning his post.'
            },
            'desertification': {
                'definition': 'The process by which fertile land becomes desert, typically due to drought or poor farming.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-zur-tuh-fi-KAY-shuhn (emphasis on fifth syllable)',
                'etymology': 'From "desert" + "-ification" (process of making)',
                'memory_tips': 'Think "desert-ification" - the process of becoming desert',
                'alternate_spellings': 'land degradation',
                'language_origin': 'Modern English compound',
                'example_sentence': 'Climate change is accelerating _____ in many regions.'
            },
            'desiccate': {
                'definition': 'To remove the moisture from something; to dry out completely.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'DES-ih-kayt (emphasis on first syllable)',
                'etymology': 'From Latin "desiccare", from "de-" + "siccus" meaning "dry"',
                'memory_tips': 'Think "de-sicc-ate" - to make completely dry (sicc)',
                'alternate_spellings': 'dehydrate, dry out',
                'language_origin': 'Latin',
                'example_sentence': 'The hot desert sun will quickly _____ any exposed organic matter.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_049_data:
            return batch_049_data[word_lower]
        
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
    
    def process_batch_049(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 049 with comprehensive Claude data"""
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
    
    def save_batch_049_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 049 processed words to CSV"""
        
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
    """Process Batch 049 with comprehensive Claude data"""
    processor = Batch049Processor()
    input_csv = Path("output/batch_049_words.csv")
    output_csv = Path("output/batch_049_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 049 with comprehensive Claude data...")
    
    # Process all words in batch 049
    processed_words = processor.process_batch_049(input_csv)
    
    # Save results
    processor.save_batch_049_csv(processed_words, output_csv)
    
    logger.info(f"Batch 049 processing completed!")
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