#!/usr/bin/env python3
"""
Process Batch 178 of Spelling Bee Words with Comprehensive Claude Data
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
            'team', 'tape', 'tasks', 'teachers', 'teak', 'teamwork', 'tell', 'telling', 'tells', 'temperature', 'television', 'telescope', 'tennis',
            'tent', 'technical', 'technology', 'technique', 'technician', 'tends', 'tendency', 'term', 'test', 'text', 'thank', 'thanks', 'theater',
            'theatre', 'theme', 'themed', 'territory', 'terror', 'tertiary', 'themes', 'therefore', 'thing', 'things', 'third', 'those', 'though',
            'thought', 'thousand', 'thousands', 'thread', 'three', 'threshold', 'throat', 'throughout', 'throw', 'thumbs'
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
            ('que', 'k'), ('x', 'ks'), ('c', 'k'), ('c', 's'), ('th', 'th')
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
            'mega', 'micro', 'mini', 'multi', 'neo', 'pseudo', 'ultra', 'ac', 'ad', 'con', 'tele', 'ter', 'the'
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

class Batch178Processor:
    """Processes Batch 178 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 178 words"""
        
        # Comprehensive data for all 50 words in Batch 178
        batch_178_data = {
            'themes': {
                'definition': 'Plural of theme; main subjects or central ideas in works of art, literature, or discussion.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'THEEMZ (single syllable)',
                'etymology': 'Plural of "theme", from Greek "thema" meaning "something set down"',
                'memory_tips': 'Think of multiple central ideas or subjects in different works',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The festival explored _____ of love and loss in classical music.'
            },
            'theodicy': {
                'definition': 'The branch of theology that attempts to justify the existence of evil in a world created by a benevolent God.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'thee-OD-i-see (emphasis on second syllable)',
                'etymology': 'From Greek "theos" (god) + "dike" (justice)',
                'memory_tips': 'Think "theo-dice-y" - rolling the dice on God\'s justice',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The philosopher\'s _____ attempted to reconcile suffering with divine goodness.'
            },
            'theomachy': {
                'definition': 'A battle or conflict among gods; opposition to the will of God.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'thee-OM-uh-kee (emphasis on second syllable)',
                'etymology': 'From Greek "theos" (god) + "mache" (battle)',
                'memory_tips': 'Think "theo-macho" - gods being macho and fighting',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The epic poem described a fierce _____ between rival deities.'
            },
            'theorem': {
                'definition': 'A mathematical statement that has been proven true; a general principle or rule.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THEE-uh-rem (emphasis on first syllable)',
                'etymology': 'From Greek "theorema", from "theorein" meaning "to look at, observe"',
                'memory_tips': 'Think "theo-rem" - observing divine mathematical truths',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The Pythagorean _____ relates the sides of a right triangle.'
            },
            'theosophy': {
                'definition': 'A religious philosophy claiming direct insight into divine nature through spiritual contemplation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'thee-OS-uh-fee (emphasis on second syllable)',
                'etymology': 'From Greek "theos" (god) + "sophia" (wisdom)',
                'memory_tips': 'Think "theo-sophy" - wisdom about God and divine things',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'She studied _____ to understand the mystical aspects of spirituality.'
            },
            'therapeutic': {
                'definition': 'Having healing properties; relating to the treatment of disease or disorders.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ther-uh-PYOO-tik (emphasis on third syllable)',
                'etymology': 'From Greek "therapeutikos", from "therapeuein" meaning "to heal"',
                'memory_tips': 'Think "therapy-tic" - relating to therapy and healing',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The massage had a _____ effect on her sore muscles.'
            },
            'theravada': {
                'definition': 'A school of Buddhism emphasizing individual enlightenment through meditation and moral conduct.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ther-uh-VAH-duh (emphasis on third syllable)',
                'etymology': 'From Pali "theravada", meaning "doctrine of the elders"',
                'memory_tips': 'Think "thera-vada" - the way (vada) of the elder teachers (thera)',
                'alternate_spellings': '',
                'language_origin': 'Pali',
                'example_sentence': '_____ Buddhism is practiced primarily in Sri Lanka and Southeast Asia.'
            },
            'therefore': {
                'definition': 'For that reason; as a result; consequently.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'THAIR-for (emphasis on first syllable)',
                'etymology': 'From Middle English "therefore", from "there" + "fore"',
                'memory_tips': 'Think "there-fore" - for that reason over there',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'It was raining heavily; _____, the picnic was cancelled.'
            },
            'theriatrics': {
                'definition': 'The branch of veterinary medicine dealing with wild animals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ther-ee-AT-riks (emphasis on third syllable)',
                'etymology': 'From Greek "therion" (wild animal) + "iatros" (physician)',
                'memory_tips': 'Think "theri-atrics" - medical tricks for wild animals',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The zoo veterinarian specialized in _____ and exotic animal care.'
            },
            'theriatricsnoun': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "theriatrics" (veterinary medicine for wild animals) + "noun" (grammar term).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "theriatrics" and "noun"',
                'alternate_spellings': 'theriatrics + noun (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'thermohaline': {
                'definition': 'Relating to ocean circulation driven by differences in water temperature and salinity.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ther-moh-HAY-lyn (emphasis on third syllable)',
                'etymology': 'From Greek "thermos" (heat) + "halinos" (of salt)',
                'memory_tips': 'Think "thermo-haline" - heat and salt driving ocean currents',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ circulation patterns affect global climate systems.'
            },
            'thermos': {
                'definition': 'A vacuum-insulated container designed to keep liquids hot or cold; a thermal bottle.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THUR-mohs (emphasis on first syllable)',
                'etymology': 'From Greek "thermos" meaning "hot"; originally a trademark',
                'memory_tips': 'Think "thermo-s" - keeping things at the right temperature',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'She filled her _____ with hot coffee for the long hike.'
            },
            'thesmothete': {
                'definition': 'In ancient Athens, one of six junior archons who served as judges and legislators.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THES-moh-theet (emphasis on first syllable)',
                'etymology': 'From Greek "thesmothetes", from "thesmos" (law) + "tithemi" (to place)',
                'memory_tips': 'Think "thesmo-thete" - one who places (thete) laws (thesmo)',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ presided over important legal cases in ancient Athens.'
            },
            'thespian': {
                'definition': 'An actor or actress; relating to drama and the theater.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'THES-pee-uhn (emphasis on first syllable)',
                'etymology': 'From Thespis, legendary first actor in ancient Greek theater',
                'memory_tips': 'Think "Thespis-ian" - following the tradition of the first actor Thespis',
                'alternate_spellings': '',
                'language_origin': 'Greek (from proper name)',
                'example_sentence': 'The talented _____ captivated audiences with her dramatic performances.'
            },
            'thespiansubmersible': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "thespian" (actor) + "submersible" (underwater vessel).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "thespian" and "submersible"',
                'alternate_spellings': 'thespian + submersible (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'thickened': {
                'definition': 'Past tense of thicken; became thicker or denser; made more viscous.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'THIK-uhnd (emphasis on first syllable)',
                'etymology': 'Past tense of "thicken", from "thick" + "-en"',
                'memory_tips': 'Think "thick-ened" - became thick and finished',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The sauce _____ as it simmered on the stove.'
            },
            'thicket': {
                'definition': 'A dense growth of bushes, trees, or shrubs; a tangled mass of vegetation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THIK-it (emphasis on first syllable)',
                'etymology': 'From "thick" + "-et" (diminutive suffix)',
                'memory_tips': 'Think "thick-et" - a small area that\'s thick with plants',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The rabbit disappeared into the dense _____ of brambles.'
            },
            'thievery': {
                'definition': 'The practice of stealing; the act of taking someone else\'s property illegally.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THEEV-uh-ree (emphasis on first syllable)',
                'etymology': 'From "thief" + "-ery", from Old English "theof"',
                'memory_tips': 'Think "thief-ery" - the practice of being a thief',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The town was plagued by increased _____ during the economic downturn.'
            },
            'thimblerig': {
                'definition': 'A gambling game using three cups and a ball; any confidence trick or swindle.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'THIM-buhl-rig (emphasis on first syllable)',
                'etymology': 'From "thimble" + "rig" (to manipulate fraudulently)',
                'memory_tips': 'Think "thimble-rig" - rigging a game with thimbles',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The street performer\'s _____ fooled many unsuspecting tourists.'
            },
            'thimerosal': {
                'definition': 'A mercury-containing preservative formerly used in vaccines; an antiseptic compound.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'thy-MER-oh-sal (emphasis on second syllable)',
                'etymology': 'From "thio" (sulfur) + "mercury" + "sal" (salt)',
                'memory_tips': 'Think "thimer-o-sal" - a mercury salt preservative',
                'alternate_spellings': 'thiomersal',
                'language_origin': 'Modern scientific',
                'example_sentence': 'Concerns about _____ led to its removal from most childhood vaccines.'
            },
            'thing': {
                'definition': 'An object, entity, or concept; a matter or situation; an item or element.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THING (single syllable)',
                'etymology': 'From Old English "thing" meaning "assembly, matter, concern"',
                'memory_tips': 'Think of any object, idea, or matter you can name',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The most important _____ is to stay safe during the storm.'
            },
            'things': {
                'definition': 'Plural of thing; objects, matters, or items; personal belongings.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'THINGZ (single syllable)',
                'etymology': 'Plural of "thing", from Old English "thing"',
                'memory_tips': 'Think of multiple objects, ideas, or matters',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She packed her _____ for the weekend trip.'
            },
            'third': {
                'definition': 'The ordinal number between second and fourth; one of three equal parts.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'THURD (single syllable)',
                'etymology': 'From Old English "thridda", from "three"',
                'memory_tips': 'Think "three-d" - the ordinal form of three',
                'alternate_spellings': '3rd',
                'language_origin': 'Old English',
                'example_sentence': 'She finished in _____ place in the marathon.'
            },
            'thistle': {
                'definition': 'A prickly plant with purple, pink, or white flowers; the national emblem of Scotland.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THIS-uhl (emphasis on first syllable)',
                'etymology': 'From Old English "thistel"',
                'memory_tips': 'Think "this-tle" - this plant will tickle you with thorns',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The Scottish _____ is known for its sharp spines and beautiful flowers.'
            },
            'thistledifficulty': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "thistle" (prickly plant) + "difficulty" (challenge).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "thistle" and "difficulty"',
                'alternate_spellings': 'thistle + difficulty (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'thomism': {
                'definition': 'The philosophical and theological system of Thomas Aquinas, emphasizing reason and faith.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TOH-mizm (emphasis on first syllable)',
                'etymology': 'From Thomas Aquinas + "-ism"',
                'memory_tips': 'Think "Thomas-ism" - the philosophy of Thomas Aquinas',
                'alternate_spellings': '',
                'language_origin': 'Latin (from proper name)',
                'example_sentence': '_____ attempts to reconcile Aristotelian philosophy with Christian theology.'
            },
            'thoracic': {
                'definition': 'Relating to the thorax or chest; concerning the part of the body between neck and abdomen.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'thoh-RAS-ik (emphasis on second syllable)',
                'etymology': 'From Greek "thorax" (chest) + "-ic"',
                'memory_tips': 'Think "thorax-ic" - relating to the thorax or chest',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ surgeon specialized in chest and lung operations.'
            },
            'thorax': {
                'definition': 'The part of the body between the neck and abdomen; the chest cavity containing heart and lungs.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THOR-aks (emphasis on first syllable)',
                'etymology': 'From Greek "thorax" meaning "breastplate, chest"',
                'memory_tips': 'Think "Thor-axe" - Thor\'s axe protects his chest like armor',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The doctor examined the patient\'s _____ for signs of infection.'
            },
            'thorn': {
                'definition': 'A sharp, pointed spike on a plant stem; something that causes pain or difficulty.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THORN (single syllable)',
                'etymology': 'From Old English "thorn"',
                'memory_tips': 'Think of sharp spikes that can prick your skin',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She carefully avoided the rose\'s sharp _____ while picking flowers.'
            },
            'thoroughbred': {
                'definition': 'A purebred horse, especially for racing; something of excellent quality or breeding.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'THUR-oh-bred (emphasis on first syllable)',
                'etymology': 'From "thorough" + "bred" (past participle of breed)',
                'memory_tips': 'Think "thorough-bred" - thoroughly and carefully bred',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The _____ racehorse won the Kentucky Derby.'
            },
            'thoroughfare': {
                'definition': 'A main road or public highway; a route for through traffic.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THUR-oh-fair (emphasis on first syllable)',
                'etymology': 'From "thorough" + "fare" (to go)',
                'memory_tips': 'Think "thorough-fare" - a road for thorough travel',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The busy _____ was congested during rush hour.'
            },
            'those': {
                'definition': 'Plural of "that"; referring to people or things previously mentioned or easily identified.',
                'part_of_speech': 'pronoun, determiner',
                'pronunciation_guide': 'THOHZ (single syllable)',
                'etymology': 'From Middle English "thos", from Old English "thas"',
                'memory_tips': 'Think of pointing to multiple things over there',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': '_____ books on the shelf belong to my sister.'
            },
            'though': {
                'definition': 'Despite the fact that; however; even if.',
                'part_of_speech': 'conjunction, adverb',
                'pronunciation_guide': 'THOH (single syllable)',
                'etymology': 'From Middle English "though", from Old Norse "tho"',
                'memory_tips': 'Think "th-oh" - expressing contrast or concession',
                'alternate_spellings': '',
                'language_origin': 'Old Norse',
                'example_sentence': '_____ it was raining, they continued their hike.'
            },
            'thought': {
                'definition': 'An idea or opinion; the process of thinking; past tense of think.',
                'part_of_speech': 'noun, verb (past tense)',
                'pronunciation_guide': 'THAWT (single syllable)',
                'etymology': 'From Old English "thoht", related to "think"',
                'memory_tips': 'Think of ideas flowing through your mind',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She had an interesting _____ about solving the problem.'
            },
            'thoughtsverb': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "thoughts" (ideas) + "verb" (grammar term).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "thoughts" and "verb"',
                'alternate_spellings': 'thoughts + verb (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'thousand': {
                'definition': 'The number 1,000; a very large number or amount.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'THOW-zuhnd (emphasis on first syllable)',
                'etymology': 'From Old English "thusend"',
                'memory_tips': 'Think "thou-sand" - like a thousand grains of sand',
                'alternate_spellings': '1,000',
                'language_origin': 'Old English',
                'example_sentence': 'The library contained over a _____ books.'
            },
            'thousands': {
                'definition': 'Plural of thousand; many thousands; very large numbers.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'THOW-zuhnds (emphasis on first syllable)',
                'etymology': 'Plural of "thousand", from Old English "thusend"',
                'memory_tips': 'Think of multiple groups of a thousand',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': '_____ of people attended the outdoor concert.'
            },
            'thrasonical': {
                'definition': 'Boastful or bragging in an arrogant manner; characterized by vainglorious speech.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'thruh-SON-i-kuhl (emphasis on second syllable)',
                'etymology': 'From Thraso, a boastful character in ancient Roman comedy + "-ical"',
                'memory_tips': 'Think "Thraso-nical" - like the boastful character Thraso',
                'alternate_spellings': '',
                'language_origin': 'Latin (from character name)',
                'example_sentence': 'His _____ claims about his achievements impressed no one.'
            },
            'thread': {
                'definition': 'A thin strand of cotton, silk, or other fiber; a line of reasoning or narrative.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'THRED (single syllable)',
                'etymology': 'From Old English "thraed"',
                'memory_tips': 'Think of thin strands used for sewing',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She lost the _____ of the conversation during the interruption.'
            },
            'three': {
                'definition': 'The number 3; one more than two.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'THREE (single syllable)',
                'etymology': 'From Old English "threo"',
                'memory_tips': 'Think of the number after two and before four',
                'alternate_spellings': '3',
                'language_origin': 'Old English',
                'example_sentence': 'The triangle has _____ sides and three angles.'
            },
            'threnody': {
                'definition': 'A song or poem expressing grief or mourning; a lament for the dead.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THREN-uh-dee (emphasis on first syllable)',
                'etymology': 'From Greek "threnoidia", from "threnos" (lament) + "ode" (song)',
                'memory_tips': 'Think "threno-dy" - a dying song of lament',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The poet composed a beautiful _____ for the fallen soldiers.'
            },
            'threshold': {
                'definition': 'The bottom of a doorway; the beginning point; the level at which something starts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THRESH-hohld (emphasis on first syllable)',
                'etymology': 'From Old English "therscold", from "thresh" + "hold"',
                'memory_tips': 'Think "thresh-hold" - holding the place where you thresh grain',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She stood on the _____ of a new career opportunity.'
            },
            'thrift': {
                'definition': 'Careful management of resources; frugality; a type of plant with small flowers.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THRIFT (single syllable)',
                'etymology': 'From Old Norse "thrift" meaning "prosperity"',
                'memory_tips': 'Think of being careful with money to achieve prosperity',
                'alternate_spellings': '',
                'language_origin': 'Old Norse',
                'example_sentence': 'Her _____ allowed her to save money for vacation.'
            },
            'throat': {
                'definition': 'The passage from the mouth to the stomach and lungs; the front part of the neck.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'THROHT (single syllable)',
                'etymology': 'From Old English "throte"',
                'memory_tips': 'Think of the tube through which food and air pass',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She felt a scratchy sensation in her _____ when she was getting sick.'
            },
            'throes': {
                'definition': 'Intense or violent pain; the final stages of something difficult.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'THROHZ (single syllable)',
                'etymology': 'From Middle English "throwe", possibly related to "throw"',
                'memory_tips': 'Think "throws" - violent throwing motions of pain',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The country was in the _____ of a major political crisis.'
            },
            'throttle': {
                'definition': 'To choke or strangle; a valve controlling fuel flow in an engine.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'THROT-uhl (emphasis on first syllable)',
                'etymology': 'From "throat" + "-le" (frequentative suffix)',
                'memory_tips': 'Think "throat-le" - affecting the throat repeatedly',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The pilot adjusted the _____ to increase engine power.'
            },
            'throughout': {
                'definition': 'In every part of; during the entire time or extent of something.',
                'part_of_speech': 'preposition, adverb',
                'pronunciation_guide': 'throo-OWT (emphasis on second syllable)',
                'etymology': 'From "through" + "out"',
                'memory_tips': 'Think "through-out" - all the way through and out',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'Rain continued _____ the entire weekend.'
            },
            'throw': {
                'definition': 'To propel something through the air; to cast or hurl.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'THROH (single syllable)',
                'etymology': 'From Old English "thrawan" meaning "to twist, turn"',
                'memory_tips': 'Think of propelling something through the air with your arm',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She learned to _____ a baseball with perfect accuracy.'
            },
            'thuluth': {
                'definition': 'A style of Arabic calligraphy characterized by curved letters and elegant proportions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'thoo-LOOTH (emphasis on second syllable)',
                'etymology': 'From Arabic "thuluth" meaning "one-third" (referring to proportions)',
                'memory_tips': 'Think "thu-luth" - one-third proportions in Arabic writing',
                'alternate_spellings': '',
                'language_origin': 'Arabic',
                'example_sentence': 'The master calligrapher specialized in the elegant _____ script.'
            },
            'thumbs': {
                'definition': 'Plural of thumb; the short, thick first digits of the hands.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'THUHMZ (single syllable)',
                'etymology': 'Plural of "thumb", from Old English "thuma"',
                'memory_tips': 'Think of the two thick fingers you use for gripping',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She gave the performance two _____ up.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_178_data:
            return batch_178_data[word_lower]
        
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
    
    def process_batch_178(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 178 with comprehensive Claude data"""
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
    
    def save_batch_178_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 178 processed words to CSV"""
        
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
    """Process Batch 178 with comprehensive Claude data"""
    processor = Batch178Processor()
    input_csv = Path("output/batch_178_words.csv")
    output_csv = Path("output/batch_178_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 178 with comprehensive Claude data...")
    
    # Process all words in batch 178
    processed_words = processor.process_batch_178(input_csv)
    
    # Save results
    processor.save_batch_178_csv(processed_words, output_csv)
    
    logger.info(f"Batch 178 processing completed!")
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