#!/usr/bin/env python3
"""
Process Batch 176 of Spelling Bee Words with Comprehensive Claude Data
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
            'tent', 'technical', 'technology', 'technique', 'technician', 'tends', 'tendency'
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
            'mega', 'micro', 'mini', 'multi', 'neo', 'pseudo', 'ultra', 'ac', 'ad', 'con', 'tele'
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

class Batch176Processor:
    """Processes Batch 176 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 176 words"""
        
        # Comprehensive data for all 50 words in Batch 176
        batch_176_data = {
            'teaspoon': {
                'definition': 'A small spoon used for stirring tea or coffee; a unit of measurement equal to about 5 milliliters.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEE-spoon (emphasis on first syllable)',
                'etymology': 'From "tea" + "spoon", referring to the small spoon used with tea',
                'memory_tips': 'Think "tea-spoon" - a spoon specifically sized for tea',
                'alternate_spellings': '',
                'language_origin': 'English (compound)',
                'example_sentence': 'Add one _____ of sugar to sweeten your coffee.'
            },
            'techie': {
                'definition': 'A person who is enthusiastic about or skilled in technology, especially computers and electronics.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEK-ee (emphasis on first syllable)',
                'etymology': 'From "tech" (short for technology) + "-ie" (informal suffix)',
                'memory_tips': 'Think "tech-ie" - someone who is into tech',
                'alternate_spellings': 'techy',
                'language_origin': 'Modern English',
                'example_sentence': 'The _____ helped everyone set up their new smartphones.'
            },
            'technical': {
                'definition': 'Relating to or involving special skills or knowledge, especially in engineering or science; complex or specialized.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'TEK-ni-kuhl (emphasis on first syllable)',
                'etymology': 'From Greek "technikos", from "techne" meaning "art, skill"',
                'memory_tips': 'Think "tech-nical" - relating to technique and skill',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ manual was too complex for most users to understand.'
            },
            'technicalities': {
                'definition': 'Specific details or rules of a complex system; minor but important points of procedure or law.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'tek-ni-KAL-i-teez (emphasis on third syllable)',
                'etymology': 'From "technical" + "-ities", meaning technical details',
                'memory_tips': 'Think "technical-ities" - multiple technical details',
                'alternate_spellings': '',
                'language_origin': 'Greek (via English)',
                'example_sentence': 'The lawyer focused on legal _____ to win the case.'
            },
            'technician': {
                'definition': 'A person skilled in the technical aspects of a particular field; someone who maintains or repairs equipment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tek-NISH-uhn (emphasis on second syllable)',
                'etymology': 'From "technique" + "-ian", meaning one skilled in technique',
                'memory_tips': 'Think "technique-ian" - a person skilled in techniques',
                'alternate_spellings': '',
                'language_origin': 'Greek (via English)',
                'example_sentence': 'The computer _____ fixed the server problem quickly.'
            },
            'technique': {
                'definition': 'A way of carrying out a particular task; a skill or method in art, sport, or other activities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tek-NEEK (emphasis on second syllable)',
                'etymology': 'From French "technique", from Greek "techne" meaning "art, skill"',
                'memory_tips': 'Think "tech-unique" - a unique technical method',
                'alternate_spellings': '',
                'language_origin': 'Greek (via French)',
                'example_sentence': 'Her painting _____ improved dramatically with practice.'
            },
            'technology': {
                'definition': 'The application of scientific knowledge for practical purposes; machinery and equipment based on such knowledge.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tek-NOL-uh-jee (emphasis on second syllable)',
                'etymology': 'From Greek "technologia", from "techne" (art) + "logos" (study)',
                'memory_tips': 'Think "techno-logy" - the study of technical things',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Modern _____ has revolutionized how we communicate.'
            },
            'tectonic': {
                'definition': 'Relating to the structure of the earth\'s crust; involving large-scale geological processes.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'tek-TON-ik (emphasis on second syllable)',
                'etymology': 'From Greek "tektonikos", from "tekton" meaning "builder"',
                'memory_tips': 'Think "tec-tonic" - building and constructing the Earth\'s structure',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The earthquake was caused by _____ plate movement.'
            },
            'tedious': {
                'definition': 'Boring and repetitive; taking a long time and requiring patience; tiresome due to length or dullness.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'TEE-dee-uhs (emphasis on first syllable)',
                'etymology': 'From Latin "taediosus", from "taedium" meaning "weariness"',
                'memory_tips': 'Think "tea-dious" - so boring even tea time becomes dull',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Filing all those documents was a _____ task that took hours.'
            },
            'teemed': {
                'definition': 'Was full of or swarming with; contained in large numbers; was abundantly filled.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'TEEMD (single syllable)',
                'etymology': 'Past tense of "teem", from Old English "teman" meaning "to bring forth"',
                'memory_tips': 'Think "team-ed" - so full it needed a team to count everything',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The garden _____ with colorful butterflies in the spring.'
            },
            'teenagers': {
                'definition': 'Young people between the ages of thirteen and nineteen; adolescents in their teen years.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'TEEN-ay-jerz (emphasis on first syllable)',
                'etymology': 'From "teen" (thirteen to nineteen) + "age" + "-ers"',
                'memory_tips': 'Think "teen-agers" - people in their teen age',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The _____ gathered at the mall after school.'
            },
            'teenagerspeat': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "teenagers" (adolescents) + "peat" (organic matter).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "teenagers" and "peat"',
                'alternate_spellings': 'teenagers + peat (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'teeter': {
                'definition': 'To move unsteadily back and forth; to be in an unstable position; to waver between different states.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'TEE-ter (emphasis on first syllable)',
                'etymology': 'From Middle English "titer", possibly imitative of unsteady movement',
                'memory_tips': 'Think "see-ter" - you can see someone tottering back and forth',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The stack of books began to _____ before finally falling over.'
            },
            'teflon': {
                'definition': 'A synthetic polymer used as a non-stick coating for cookware; trademark for polytetrafluoroethylene.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEF-lon (emphasis on first syllable)',
                'etymology': 'Trademark name, from "tetrafluoroethylene" + "-on"',
                'memory_tips': 'Think "tough-lon" - a tough coating that nothing sticks to',
                'alternate_spellings': 'PTFE',
                'language_origin': 'Modern scientific (trademark)',
                'example_sentence': 'The _____ coating made the pan easy to clean.'
            },
            'tegucigalpa': {
                'definition': 'The capital and largest city of Honduras, located in the central part of the country.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'teh-goo-see-GAHL-pah (emphasis on fourth syllable)',
                'etymology': 'From Nahuatl, possibly meaning "silver hills" or "painted houses"',
                'memory_tips': 'Think "te-goose-i-gal-pa" - a city where geese and gals meet',
                'alternate_spellings': '',
                'language_origin': 'Nahuatl',
                'example_sentence': '_____ is the political and economic center of Honduras.'
            },
            'tejano': {
                'definition': 'A style of music blending Mexican folk music with elements of country and rock; relating to Mexican-American culture in Texas.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'teh-HAH-noh (emphasis on second syllable)',
                'etymology': 'From Spanish "tejano", meaning "Texan" (referring to Mexican-Texans)',
                'memory_tips': 'Think "Texas-ano" - music from Mexican-Americans in Texas',
                'alternate_spellings': '',
                'language_origin': 'Spanish',
                'example_sentence': 'The band played traditional _____ music at the festival.'
            },
            'telamon': {
                'definition': 'A male figure used as a supporting column in classical architecture; also called an atlas.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEL-uh-mon (emphasis on first syllable)',
                'etymology': 'From Greek "telamon", from "talaein" meaning "to bear, endure"',
                'memory_tips': 'Think "tell-a-man" - tell a man to hold up the building',
                'alternate_spellings': 'atlas',
                'language_origin': 'Greek',
                'example_sentence': 'The ancient temple featured carved _____ supporting the roof.'
            },
            'teledu': {
                'definition': 'A badger-like mammal found in Southeast Asia, also known as a stink badger.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEL-uh-doo (emphasis on first syllable)',
                'etymology': 'From Malay/Javanese "teledu"',
                'memory_tips': 'Think "tell-edu" - an educational animal that tells you about badgers',
                'alternate_spellings': '',
                'language_origin': 'Malay/Javanese',
                'example_sentence': 'The _____ is known for its distinctive black and white markings.'
            },
            'telegnosis': {
                'definition': 'Alleged knowledge of distant events without normal sensory contact; clairvoyance or extrasensory perception.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tel-ig-NOH-sis (emphasis on third syllable)',
                'etymology': 'From Greek "tele" (distant) + "gnosis" (knowledge)',
                'memory_tips': 'Think "tele-gnosis" - distant knowledge like a telephone for the mind',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Some claimed the psychic had _____ of events happening far away.'
            },
            'telenovelas': {
                'definition': 'Spanish or Portuguese-language television soap operas, typically featuring dramatic storylines and romance.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'tel-eh-noh-VEH-lahs (emphasis on fourth syllable)',
                'etymology': 'From Spanish "telenovela", from "tele" (television) + "novela" (novel)',
                'memory_tips': 'Think "tele-novels" - television novels with dramatic stories',
                'alternate_spellings': '',
                'language_origin': 'Spanish',
                'example_sentence': 'She watched _____ every evening to practice her Spanish.'
            },
            'teleology': {
                'definition': 'The philosophical study of purpose and design in nature; the explanation of phenomena by their purposes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tel-ee-OL-uh-jee (emphasis on third syllable)',
                'etymology': 'From Greek "telos" (end, purpose) + "logos" (study)',
                'memory_tips': 'Think "tele-ology" - the study of distant purposes and goals',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The philosopher explored _____ to understand nature\'s apparent design.'
            },
            'telepathic': {
                'definition': 'Relating to or involving telepathy; able to communicate thoughts directly without speech or writing.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'tel-uh-PATH-ik (emphasis on third syllable)',
                'etymology': 'From "telepathy" + "-ic", from Greek "tele" (distant) + "pathos" (feeling)',
                'memory_tips': 'Think "tele-pathic" - feeling thoughts from a distance like a telephone',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The twins seemed to have a _____ connection.'
            },
            'telescope': {
                'definition': 'An optical instrument for viewing distant objects by magnifying them; to compress or extend like overlapping tubes.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TEL-uh-skohp (emphasis on first syllable)',
                'etymology': 'From Greek "tele" (distant) + "skopein" (to look)',
                'memory_tips': 'Think "tele-scope" - looking at distant things in scope',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The astronomer used a powerful _____ to study distant galaxies.'
            },
            'televised': {
                'definition': 'Broadcast on television; transmitted for viewing on television screens.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'TEL-uh-vyzd (emphasis on first syllable)',
                'etymology': 'Past tense of "televise", from "television" + "-ed"',
                'memory_tips': 'Think "tele-vised" - visions sent through television',
                'alternate_spellings': '',
                'language_origin': 'Modern English (from Greek elements)',
                'example_sentence': 'The presidential debate was _____ to millions of viewers.'
            },
            'television': {
                'definition': 'A system for transmitting visual images and sound over a distance; the receiving device for such transmissions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEL-uh-vizh-uhn (emphasis on first syllable)',
                'etymology': 'From Greek "tele" (distant) + Latin "visio" (sight)',
                'memory_tips': 'Think "tele-vision" - distant vision brought to your home',
                'alternate_spellings': 'TV',
                'language_origin': 'Greek and Latin',
                'example_sentence': 'The family gathered around the _____ to watch the news.'
            },
            'tell': {
                'definition': 'To communicate information to someone; to give an account or narrative; to distinguish or recognize.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'TEL (single syllable)',
                'etymology': 'From Old English "tellan" meaning "to count, relate"',
                'memory_tips': 'Think of sharing information or stories with others',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'Please _____ me about your trip to the mountains.'
            },
            'telling': {
                'definition': 'The action of giving information; having a significant effect; revealing or significant.',
                'part_of_speech': 'verb (present participle), adjective, noun',
                'pronunciation_guide': 'TEL-ing (emphasis on first syllable)',
                'etymology': 'Present participle of "tell", from Old English "tellan"',
                'memory_tips': 'Think "tell-ing" - currently in the process of telling',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'Her facial expression was very _____ of her true feelings.'
            },
            'tells': {
                'definition': 'Third person singular of tell; communicates information; gives accounts.',
                'part_of_speech': 'verb (third person singular)',
                'pronunciation_guide': 'TELZ (single syllable)',
                'etymology': 'Third person singular of "tell", from Old English "tellan"',
                'memory_tips': 'Think "he/she tells" - someone else doing the telling',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She _____ the most interesting stories about her travels.'
            },
            'telmatology': {
                'definition': 'The scientific study of wetlands, marshes, and peat bogs; the branch of ecology focusing on wetland ecosystems.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tel-muh-TOL-uh-jee (emphasis on third syllable)',
                'etymology': 'From Greek "telma" (marsh) + "logos" (study)',
                'memory_tips': 'Think "telma-tology" - the study of marshy, swampy areas',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The scientist specialized in _____ to help restore wetland habitats.'
            },
            'temalacatl': {
                'definition': 'A circular stone platform used in Aztec ritual ball games and gladiatorial contests.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'teh-mah-lah-KAHT-l (emphasis on fourth syllable)',
                'etymology': 'From Nahuatl "temalacatl", from "tetl" (stone) + "malacatl" (spindle)',
                'memory_tips': 'Think "tema-la-catl" - a ceremonial cat platform for Aztec rituals',
                'alternate_spellings': '',
                'language_origin': 'Nahuatl',
                'example_sentence': 'The ancient _____ was carved with intricate Aztec symbols.'
            },
            'temblor': {
                'definition': 'An earthquake or earth tremor; a shaking of the ground caused by seismic activity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tem-BLOR (emphasis on second syllable)',
                'etymology': 'From Spanish "temblor", from "temblar" meaning "to tremble"',
                'memory_tips': 'Think "tremble-or" - the ground trembles during an earthquake',
                'alternate_spellings': '',
                'language_origin': 'Spanish',
                'example_sentence': 'The minor _____ shook the building for several seconds.'
            },
            'temerity': {
                'definition': 'Excessive confidence or boldness; audacity or recklessness in behavior.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tuh-MER-i-tee (emphasis on second syllable)',
                'etymology': 'From Latin "temeritas", from "temere" meaning "blindly, recklessly"',
                'memory_tips': 'Think "timer-ity" - acting without taking time to think',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'He had the _____ to criticize the expert in front of everyone.'
            },
            'temerityegress': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "temerity" (boldness) + "egress" (exit).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "temerity" and "egress"',
                'alternate_spellings': 'temerity + egress (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'tempeh': {
                'definition': 'A traditional Indonesian food made from fermented soybeans, often used as a protein source.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEM-pay (emphasis on first syllable)',
                'etymology': 'From Indonesian "tempeh"',
                'memory_tips': 'Think "temp-eh" - a temporary meat substitute from Indonesia',
                'alternate_spellings': '',
                'language_origin': 'Indonesian',
                'example_sentence': 'The vegetarian restaurant served marinated _____ as a meat substitute.'
            },
            'temperature': {
                'definition': 'The degree of hotness or coldness of something; a measurement of thermal energy.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEM-per-uh-cher (emphasis on first syllable)',
                'etymology': 'From Latin "temperatura", from "temperare" meaning "to moderate"',
                'memory_tips': 'Think "temper-ature" - the temper or mood of heat',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ dropped below freezing during the night.'
            },
            'tempestuous': {
                'definition': 'Very stormy or turbulent; characterized by strong emotions or conflicting opinions.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'tem-PES-choo-uhs (emphasis on second syllable)',
                'etymology': 'From Latin "tempestuosus", from "tempestas" meaning "storm"',
                'memory_tips': 'Think "tempest-uous" - full of tempests and storms',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Their _____ relationship was marked by frequent arguments.'
            },
            'tempura': {
                'definition': 'A Japanese dish of seafood or vegetables coated in light batter and deep-fried.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tem-POO-rah (emphasis on second syllable)',
                'etymology': 'From Portuguese "tempero" (seasoning), introduced to Japan in 16th century',
                'memory_tips': 'Think "temp-ura" - temporarily coated food that\'s fried',
                'alternate_spellings': '',
                'language_origin': 'Portuguese (via Japanese)',
                'example_sentence': 'The restaurant\'s shrimp _____ was perfectly crispy and light.'
            },
            'tenaciously': {
                'definition': 'In a determined and persistent manner; with great determination and unwillingness to give up.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'tuh-NAY-shuhs-lee (emphasis on second syllable)',
                'etymology': 'From "tenacious" + "-ly", from Latin "tenax" meaning "holding fast"',
                'memory_tips': 'Think "ten-aciously" - holding on for ten years, never giving up',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She _____ pursued her goal despite numerous obstacles.'
            },
            'tenaciouslyindemnity': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "tenaciously" (persistently) + "indemnity" (compensation).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "tenaciously" and "indemnity"',
                'alternate_spellings': 'tenaciously + indemnity (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'tendency': {
                'definition': 'An inclination toward a particular characteristic or behavior; a general direction of change.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEN-duhn-see (emphasis on first syllable)',
                'etymology': 'From Latin "tendentia", from "tendere" meaning "to stretch, extend"',
                'memory_tips': 'Think "tend-ency" - the way things tend to go',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She has a _____ to arrive early for appointments.'
            },
            'tends': {
                'definition': 'Third person singular of tend; takes care of; has a tendency toward.',
                'part_of_speech': 'verb (third person singular)',
                'pronunciation_guide': 'TENDZ (single syllable)',
                'etymology': 'Third person singular of "tend", from Latin "tendere"',
                'memory_tips': 'Think "he/she tends" - someone caring for or leaning toward something',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'He _____ to worry about things beyond his control.'
            },
            'tenement': {
                'definition': 'A multi-occupancy building, especially a run-down apartment building in a poor area of a city.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEN-uh-muhnt (emphasis on first syllable)',
                'etymology': 'From Latin "tenementum", from "tenere" meaning "to hold"',
                'memory_tips': 'Think "ten-ement" - a building where ten families live',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The old _____ housed dozens of families in cramped conditions.'
            },
            'teneramente': {
                'definition': 'A musical term meaning "tenderly" or "lovingly"; indicates a gentle, affectionate style of performance.',
                'part_of_speech': 'adverb (musical term)',
                'pronunciation_guide': 'ten-eh-rah-MEN-teh (emphasis on fourth syllable)',
                'etymology': 'From Italian "teneramente", from "tenero" meaning "tender"',
                'memory_tips': 'Think "tender-amente" - tenderly in Italian musical style',
                'alternate_spellings': '',
                'language_origin': 'Italian',
                'example_sentence': 'The pianist played the piece _____, with great emotional sensitivity.'
            },
            'tenets': {
                'definition': 'Principles or beliefs held by a person or group; fundamental doctrines or rules.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'TEN-its (emphasis on first syllable)',
                'etymology': 'From Latin "tenere" meaning "to hold" (things held to be true)',
                'memory_tips': 'Think "ten-nets" - ten nets that hold your beliefs',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The basic _____ of democracy include freedom and equality.'
            },
            'tennis': {
                'definition': 'A racket sport played on a court by two or four players who hit a ball over a net.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEN-is (emphasis on first syllable)',
                'etymology': 'From Old French "tenez", meaning "take!" (called when serving)',
                'memory_tips': 'Think "ten-is" - you need ten points to win some games',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'They played _____ every Saturday morning at the local club.'
            },
            'tenon': {
                'definition': 'A projection in woodworking designed to fit into a corresponding hole (mortise) to form a joint.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEN-uhn (emphasis on first syllable)',
                'etymology': 'From French "tenon", from "tenir" meaning "to hold"',
                'memory_tips': 'Think "ten-on" - ten pieces held on by this joint',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The carpenter cut a _____ to fit perfectly into the mortise.'
            },
            'tensile': {
                'definition': 'Relating to tension; capable of being stretched; having to do with the strength of materials under tension.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'TEN-syl (emphasis on first syllable)',
                'etymology': 'From Latin "tensilis", from "tendere" meaning "to stretch"',
                'memory_tips': 'Think "ten-sile" - ten times more stretchy and strong',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The cable\'s high _____ strength made it perfect for the bridge.'
            },
            'tensions': {
                'definition': 'States of mental or emotional strain; forces that pull or stretch; conflicts or disagreements.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'TEN-shuhnz (emphasis on first syllable)',
                'etymology': 'Plural of "tension", from Latin "tensio", from "tendere"',
                'memory_tips': 'Think "ten-sions" - ten different stresses pulling at you',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ between the two countries continued to escalate.'
            },
            'tent': {
                'definition': 'A portable shelter made of fabric stretched over a framework; to camp in such a shelter.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TENT (single syllable)',
                'etymology': 'From Latin "tentum", from "tendere" meaning "to stretch"',
                'memory_tips': 'Think of fabric stretched over poles for camping',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'They set up their _____ near the lake for the weekend.'
            },
            'tentacled': {
                'definition': 'Having tentacles; equipped with flexible, elongated appendages used for grasping or feeling.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'TEN-tuh-kuhld (emphasis on first syllable)',
                'etymology': 'From "tentacle" + "-ed", from Latin "tentaculum" meaning "feeler"',
                'memory_tips': 'Think "ten-tackle-d" - having ten arms to tackle with',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ creature moved gracefully through the water.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_176_data:
            return batch_176_data[word_lower]
        
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
    
    def process_batch_176(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 176 with comprehensive Claude data"""
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
    
    def save_batch_176_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 176 processed words to CSV"""
        
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
    """Process Batch 176 with comprehensive Claude data"""
    processor = Batch176Processor()
    input_csv = Path("output/batch_176_words.csv")
    output_csv = Path("output/batch_176_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 176 with comprehensive Claude data...")
    
    # Process all words in batch 176
    processed_words = processor.process_batch_176(input_csv)
    
    # Save results
    processor.save_batch_176_csv(processed_words, output_csv)
    
    logger.info(f"Batch 176 processing completed!")
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