#!/usr/bin/env python3
"""
Process Batch 035 of Spelling Bee Words with Comprehensive Claude Data
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

class Batch035Processor:
    """Processes Batch 035 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 035 words"""
        
        # Comprehensive data for all 50 words in Batch 035
        batch_035_data = {
            'cioppino': {
                'definition': 'A fish stew originating in San Francisco, typically containing various seafood such as clams, mussels, crab, and fish in a tomato-wine base.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'chuh-PEE-noh (emphasis on second syllable)',
                'etymology': 'From Italian "ciuppin", a Ligurian fish stew, brought to San Francisco by Italian fishermen',
                'memory_tips': 'Think "chop-ino" - chopping up seafood for an Italian stew',
                'alternate_spellings': '',
                'language_origin': 'Italian (Ligurian dialect)',
                'example_sentence': 'The fisherman\'s _____ contained fresh crab, mussels, and tender pieces of halibut.'
            },
            'circadian': {
                'definition': 'Relating to biological processes that recur naturally on a twenty-four-hour cycle, especially sleep-wake patterns and hormone production.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ser-KAY-dee-uhn (emphasis on second syllable)',
                'etymology': 'From Latin "circa" (about) + "dies" (day), literally meaning "about a day"',
                'memory_tips': 'Think "circle-adian" - biological cycles that circle around each day',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Jet lag disrupts your natural _____ rhythm, making it difficult to sleep at night.'
            },
            'circle': {
                'definition': 'A round shape with all points equidistant from the center; a group of people with shared interests; to move around something.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'SUR-kuhl (emphasis on first syllable)',
                'etymology': 'From Latin "circulus", diminutive of "circus" (ring)',
                'memory_tips': 'Think of drawing a perfect round shape with a compass',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The children sat in a _____ to listen to the storyteller.'
            },
            'circuitous': {
                'definition': 'Taking a longer route than necessary; roundabout or indirect in speech or behavior; unnecessarily complicated.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ser-KYOO-ih-tuhs (emphasis on second syllable)',
                'etymology': 'From Latin "circuitus" (a going around), from "circuire" (to go around)',
                'memory_tips': 'Think "circuit-ous" - like taking a long electrical circuit instead of a direct path',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The politician gave a _____ answer that avoided addressing the real question.'
            },
            'circuitouscircumflex': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "circuitous" (roundabout) + "circumflex" (accent mark).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "circuitous" and "circumflex"',
                'alternate_spellings': 'circuitous + circumflex (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'circuitousveracity': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "circuitous" (roundabout) + "veracity" (truthfulness).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "circuitous" and "veracity"',
                'alternate_spellings': 'circuitous + veracity (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'circumflex': {
                'definition': 'A diacritical mark (^) placed over a vowel in some languages to indicate pronunciation, length, or stress; in anatomy, curved or bending around.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'SUR-kuhm-fleks (emphasis on first syllable)',
                'etymology': 'From Latin "circumflexus", from "circum" (around) + "flectere" (to bend)',
                'memory_tips': 'Think "circum-flex" - bending around like the curved accent mark ^',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The French word "château" features a _____ accent over the "a" in the second syllable.'
            },
            'circumscribe': {
                'definition': 'To draw a line around; to restrict or limit the range or activity of something; to surround or encompass.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'SUR-kuhm-skryb (emphasis on first syllable)',
                'etymology': 'From Latin "circumscribere", from "circum" (around) + "scribere" (to write)',
                'memory_tips': 'Think "circum-scribe" - writing or drawing around something to contain it',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The new regulations will _____ the company\'s ability to expand overseas.'
            },
            'circumspectlythe': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "circumspectly" (cautiously) + "the" (definite article).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "circumspectly" and "the"',
                'alternate_spellings': 'circumspectly + the (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'circus': {
                'definition': 'A traveling entertainment show featuring acrobats, clowns, and trained animals; a situation of noisy confusion; in ancient Rome, an arena for chariot races.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SUR-kuhs (emphasis on first syllable)',
                'etymology': 'From Latin "circus" (ring, circular arena)',
                'memory_tips': 'Think of the circular ring where circus performers entertain audiences',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The traveling _____ set up its big top tent in the empty field outside town.'
            },
            'cire': {
                'definition': 'French word meaning "wax"; in English, refers to a glossy finish applied to fabrics or surfaces to give them a waxy appearance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SEER (emphasis on single syllable)',
                'etymology': 'From French "cire" (wax), from Latin "cera" (wax)',
                'memory_tips': 'Think "seer" - someone who can see the glossy, waxy finish clearly',
                'alternate_spellings': '',
                'language_origin': 'French (from Latin)',
                'example_sentence': 'The fabric had a beautiful _____ finish that made it shimmer in the light.'
            },
            'cirque': {
                'definition': 'A steep-walled amphitheater-like valley carved by glacial erosion; a circular or semicircular arena; a traveling acrobatic performance group.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SURK (emphasis on single syllable)',
                'etymology': 'From French "cirque", from Latin "circus" (circle, ring)',
                'memory_tips': 'Think "circus" without the "us" - a circular amphitheater in nature',
                'alternate_spellings': '',
                'language_origin': 'French (from Latin)',
                'example_sentence': 'The mountain _____ was carved by ancient glaciers thousands of years ago.'
            },
            'cirrhosisbangalore': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "cirrhosis" (liver disease) + "Bangalore" (city in India).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "cirrhosis" and "Bangalore"',
                'alternate_spellings': 'cirrhosis + Bangalore (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'cirri': {
                'definition': 'Plural of cirrus; thin, wispy, high-altitude clouds; slender appendages or tendrils in biology, such as those found on certain marine animals.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'SIR-eye (emphasis on first syllable)',
                'etymology': 'Plural of Latin "cirrus" (curl, lock of hair)',
                'memory_tips': 'Think "sear-eye" - thin clouds that look like curled hairs in the sky that sear your eyes',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The delicate _____ clouds streaked across the blue sky like wispy brushstrokes.'
            },
            'cistern': {
                'definition': 'A tank for storing water, especially one supplying taps or as part of a flushing toilet; an underground reservoir for rainwater.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIS-turn (emphasis on first syllable)',
                'etymology': 'From Latin "cisterna", from "cista" (box, chest)',
                'memory_tips': 'Think "sister-n" - like a sister container that stores water',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The old farmhouse relied on a large _____ to collect and store rainwater.'
            },
            'citation': {
                'definition': 'A reference to a source of information; an official summons to appear in court; recognition or praise for achievement.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'sy-TAY-shuhn (emphasis on second syllable)',
                'etymology': 'From Latin "citatio", from "citare" (to summon, call)',
                'memory_tips': 'Think "cite-ation" - the action of citing or referencing something',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The research paper included a proper _____ for every source mentioned.'
            },
            'citizen': {
                'definition': 'A legally recognized member of a country or state with rights and responsibilities; an inhabitant of a particular town or city.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIT-ih-zuhn (emphasis on first syllable)',
                'etymology': 'From Old French "citezein", from "cite" (city)',
                'memory_tips': 'Think "city-zen" - someone who lives in the city with zen-like civic responsibility',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'Every _____ has both rights and responsibilities within their community.'
            },
            'citronella': {
                'definition': 'A fragrant grass native to Asia, or oil extracted from it, commonly used as an insect repellent and in perfumes and soaps.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'sit-ruh-NEL-ah (emphasis on third syllable)',
                'etymology': 'From "citron" (citrus fruit) + "-ella" (diminutive), referring to its lemony scent',
                'memory_tips': 'Think "citrus-ella" - like Cinderella but with a citrusy smell that repels bugs',
                'alternate_spellings': '',
                'language_origin': 'Modern Latin (from citrus)',
                'example_sentence': 'The _____ candles helped keep mosquitoes away during the outdoor dinner party.'
            },
            'city': {
                'definition': 'A large town; an incorporated municipal area with defined boundaries and local government; an urban area with significant population.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIT-ee (emphasis on first syllable)',
                'etymology': 'From Old French "cite", from Latin "civitas" (citizenship, community)',
                'memory_tips': 'Think of tall buildings, busy streets, and lots of people living together',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'The _____ skyline was illuminated by thousands of lights after dark.'
            },
            'civet': {
                'definition': 'A small, carnivorous mammal native to Africa and Asia, valued for the musky secretion used in perfumes; the secretion itself.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIV-it (emphasis on first syllable)',
                'etymology': 'From French "civette", from Arabic "zabād" (civet perfume)',
                'memory_tips': 'Think "civic-cat" - a cat-like animal that contributes to the civic duty of making perfume',
                'alternate_spellings': '',
                'language_origin': 'French (from Arabic)',
                'example_sentence': 'The _____ is prized for the aromatic secretion used in expensive perfumes.'
            },
            'civics': {
                'definition': 'The study of the rights and duties of citizenship; education about government, democracy, and civic responsibilities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIV-iks (emphasis on first syllable)',
                'etymology': 'From "civic" + "-s", where civic comes from Latin "civicus" (of citizens)',
                'memory_tips': 'Think "civic-s" - the study of multiple civic duties and responsibilities',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ class taught students about voting, jury duty, and democratic processes.'
            },
            'civil': {
                'definition': 'Relating to citizens and their affairs; courteous and polite; relating to civil law rather than criminal law.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'SIV-uhl (emphasis on first syllable)',
                'etymology': 'From Latin "civilis", from "civis" (citizen)',
                'memory_tips': 'Think "civilized" - being polite and relating to citizenship',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Despite their disagreement, they maintained a _____ conversation throughout dinner.'
            },
            'cladding': {
                'definition': 'A covering or coating applied to the outside of a building or structure for protection or decoration; metal bonded to another metal.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLAD-ing (emphasis on first syllable)',
                'etymology': 'From "clad" (clothed, covered) + "-ing"',
                'memory_tips': 'Think "glad-ding" - gladly adding a protective covering to buildings',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The building\'s aluminum _____ gave it a modern, sleek appearance.'
            },
            'cladistics': {
                'definition': 'A method of biological classification based on evolutionary relationships and shared derived characteristics among species.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'klah-DIS-tiks (emphasis on second syllable)',
                'etymology': 'From Greek "klados" (branch) + "-istics", referring to branching evolutionary relationships',
                'memory_tips': 'Think "clad-is-tics" - statistics about how species are clad in evolutionary branches',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Using _____, scientists determined that birds are more closely related to dinosaurs than to mammals.'
            },
            'cladogram': {
                'definition': 'A diagram showing the evolutionary relationships between different species or groups, resembling a branching tree structure.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLAD-oh-gram (emphasis on first syllable)',
                'etymology': 'From Greek "klados" (branch) + "gramma" (drawing, written character)',
                'memory_tips': 'Think "clad-oh-gram" - a diagram that draws how species are clad in evolutionary branches',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ clearly illustrated the evolutionary connections between various mammalian species.'
            },
            'claimed': {
                'definition': 'Past tense of claim; asserted ownership or right to something; stated something to be true; demanded or requested something.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'KLAYMD (emphasis on single syllable)',
                'etymology': 'From Old French "clamer", from Latin "clamare" (to call out, shout)',
                'memory_tips': 'Think "acclaimed" without the "ac" - someone shouted out their right to something',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'She _____ that the lost wallet belonged to her grandmother.'
            },
            'clairvoyance': {
                'definition': 'The supposed ability to perceive events in the future or beyond normal sensory contact; exceptional insight or perceptiveness.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'klair-VOY-uhns (emphasis on second syllable)',
                'etymology': 'From French "clairvoyance", from "clair" (clear) + "voir" (to see)',
                'memory_tips': 'Think "clear-voyance" - clear sight beyond normal vision',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The fortune teller claimed to possess _____ and could predict future events.'
            },
            'clamorous': {
                'definition': 'Making a loud and confused noise; expressing demands or complaints loudly and insistently; characterized by uproar.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'KLAM-er-uhs (emphasis on first syllable)',
                'etymology': 'From "clamor" + "-ous", where clamor comes from Latin "clamare" (to shout)',
                'memory_tips': 'Think "clam-or-us" - either clams are noisy, or there\'s a choice between clam and noise',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ crowd outside the courthouse demanded justice for the wrongly accused.'
            },
            'clandestine': {
                'definition': 'Kept secret or done secretively, especially because it is illicit or unauthorized; surreptitious or covert.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'klan-DES-tin (emphasis on second syllable)',
                'etymology': 'From Latin "clandestinus", from "clam" (secretly)',
                'memory_tips': 'Think "clan-destined" - a clan destined to meet in secret',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The resistance fighters held _____ meetings in abandoned buildings throughout the city.'
            },
            'clarinet': {
                'definition': 'A woodwind musical instrument with a single reed mouthpiece, cylindrical bore, and flaring bell, played by covering holes and pressing keys.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'klar-uh-NET (emphasis on third syllable)',
                'etymology': 'From French "clarinette", diminutive of "clarine" (a type of bell)',
                'memory_tips': 'Think "clear-net" - an instrument that makes clear sounds through its net of keys',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The _____ solo in the jazz piece showcased the musician\'s exceptional skill.'
            },
            'clarinetcapillary': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "clarinet" (musical instrument) + "capillary" (tiny blood vessel).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "clarinet" and "capillary"',
                'alternate_spellings': 'clarinet + capillary (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'clarion': {
                'definition': 'A shrill, narrow-tubed war trumpet; a loud, clear sound; loud and clear in expression.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'KLAR-ee-uhn (emphasis on first syllable)',
                'etymology': 'From Latin "clario", from "clarus" (clear, bright)',
                'memory_tips': 'Think "clear-ion" - a clear, bright sound that carries like an ion through the air',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ call echoed across the battlefield, signaling the charge.'
            },
            'clash': {
                'definition': 'To come into violent contact; to conflict or disagree strongly; a violent collision or loud, harsh sound.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'KLASH (emphasis on single syllable)',
                'etymology': 'Imitative word, possibly from the sound of metal striking metal',
                'memory_tips': 'Think of cymbals clashing together with a loud metallic sound',
                'alternate_spellings': '',
                'language_origin': 'Imitative (English)',
                'example_sentence': 'The two armies would _____ at dawn in the valley below.'
            },
            'classical': {
                'definition': 'Relating to ancient Greek and Roman culture; representing the highest standards of traditional art, literature, or music; standard and authoritative.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'KLAS-ih-kuhl (emphasis on first syllable)',
                'etymology': 'From "classic" + "-al", where classic comes from Latin "classicus" (of the highest class)',
                'memory_tips': 'Think "class-ical" - of the highest class, like classical music or literature',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The orchestra performed a _____ symphony by Mozart to end the concert season.'
            },
            'classified': {
                'definition': 'Arranged in classes or categories; designated as officially secret; small advertisements in newspapers organized by category.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'KLAS-uh-fyd (emphasis on first syllable)',
                'etymology': 'From "classify" + "-ed", where classify comes from Latin "classis" (class)',
                'memory_tips': 'Think "class-ified" - officially placed into a class or category',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The government documents were marked as _____ and required special clearance to access.'
            },
            'classroom': {
                'definition': 'A room in which a class of students is taught; the educational setting where formal instruction takes place.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLAS-room (emphasis on first syllable)',
                'etymology': 'Compound word from "class" + "room"',
                'memory_tips': 'Think of a room where students attend class with desks, a blackboard, and a teacher',
                'alternate_spellings': '',
                'language_origin': 'Modern English (compound)',
                'example_sentence': 'The _____ was equipped with new computers and interactive whiteboards.'
            },
            'clatter': {
                'definition': 'To make a continuous rattling sound; to move or fall with such a sound; the sound itself.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'KLAT-er (emphasis on first syllable)',
                'etymology': 'Imitative word representing the sound of hard objects striking each other',
                'memory_tips': 'Think of dishes clattering in the sink or hooves clattering on pavement',
                'alternate_spellings': '',
                'language_origin': 'Imitative (English)',
                'example_sentence': 'The horse\'s hooves would _____ loudly against the cobblestone street.'
            },
            'claustrophobia': {
                'definition': 'An abnormal fear of being in enclosed or confined spaces; extreme discomfort in crowded or restricted environments.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'klaw-struh-FOH-bee-ah (emphasis on third syllable)',
                'etymology': 'From Latin "claustrum" (enclosed place) + Greek "phobos" (fear)',
                'memory_tips': 'Think "claus-tro-phobia" - fear of being closed in like Santa Claus in a chimney',
                'alternate_spellings': '',
                'language_origin': 'Latin and Greek',
                'example_sentence': 'Her _____ made it impossible for her to ride in elevators or small rooms.'
            },
            'clavichord': {
                'definition': 'A small, rectangular keyboard instrument popular from the 16th to 18th centuries, producing sound by metal blades striking strings.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLAV-ih-kord (emphasis on first syllable)',
                'etymology': 'From Latin "clavis" (key) + "chorda" (string)',
                'memory_tips': 'Think "clavi-chord" - keys that make chords by striking strings',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The delicate _____ produced a soft, intimate sound perfect for chamber music.'
            },
            'claws': {
                'definition': 'Sharp, curved nails on the toes of animals; the pincers of arthropods like crabs; to scratch or grasp with claws.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'KLAWZ (emphasis on single syllable)',
                'etymology': 'From Old English "clawu", related to German "Klaue"',
                'memory_tips': 'Think of a cat\'s sharp claws or a crab\'s pincers',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The cat extended its sharp _____ to climb up the tree trunk.'
            },
            'clear': {
                'definition': 'Easy to perceive or understand; transparent or free from obstruction; free from confusion or doubt; to remove obstructions.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'KLEER (emphasis on single syllable)',
                'etymology': 'From Old French "cler", from Latin "clarus" (bright, clear)',
                'memory_tips': 'Think of crystal-clear water or a clear blue sky',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'The instructions were _____ and easy to follow.'
            },
            'clearance': {
                'definition': 'The action of clearing or removing something; official authorization or permission; the space between two objects.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLEER-uhns (emphasis on first syllable)',
                'etymology': 'From "clear" + "-ance"',
                'memory_tips': 'Think "clear-ance" - the state of being clear or the act of clearing',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'The pilot waited for _____ from the control tower before taking off.'
            },
            'clearly': {
                'definition': 'In a clear manner; obviously or without doubt; in a way that is easy to see, hear, or understand.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'KLEER-lee (emphasis on first syllable)',
                'etymology': 'From "clear" + "-ly"',
                'memory_tips': 'Think "clear-ly" - in a clear manner, obviously',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'She spoke _____ so everyone in the audience could understand her presentation.'
            },
            'cleave': {
                'definition': 'To split or divide, especially along natural lines; paradoxically also means to stick or adhere closely; to separate by force.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'KLEEV (emphasis on single syllable)',
                'etymology': 'From Old English "cleofan" (to split) and "clifian" (to adhere)',
                'memory_tips': 'Think "cleave" - it can mean both to split apart AND to stick together (confusing but true!)',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The axe was designed to _____ through logs with a single powerful swing.'
            },
            'clematis': {
                'definition': 'A climbing plant with showy flowers, belonging to the buttercup family, popular in gardens for its ornamental value.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLEM-ah-tis or kluh-MAT-is (emphasis varies)',
                'etymology': 'From Greek "klema" (vine branch, twig)',
                'memory_tips': 'Think "climb-atis" - a climbing plant with beautiful flowers',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The purple _____ covered the entire garden trellis with cascading blooms.'
            },
            'clemency': {
                'definition': 'Mercy or leniency, especially in the punishment of offenders; mildness of weather; compassionate treatment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLEM-uhn-see (emphasis on first syllable)',
                'etymology': 'From Latin "clementia", from "clemens" (mild, gentle)',
                'memory_tips': 'Think "clem-mercy" - showing mercy and gentleness',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The governor granted _____ to the prisoner who had shown genuine remorse.'
            },
            'clerihew': {
                'definition': 'A humorous four-line biographical poem with an AABB rhyme scheme, typically about famous people, invented by Edmund Clerihew Bentley.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLER-ih-hyoo (emphasis on first syllable)',
                'etymology': 'Named after Edmund Clerihew Bentley, who invented this poetic form',
                'memory_tips': 'Think "clear-he-you" - a clear poem about he, you, or famous people',
                'alternate_spellings': '',
                'language_origin': 'Modern English (proper name)',
                'example_sentence': 'The student wrote a _____ about Shakespeare that made the entire class laugh.'
            },
            'clerisy': {
                'definition': 'The educated class or intellectual elite of a society; scholars, clergy, and learned people collectively.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KLER-ih-see (emphasis on first syllable)',
                'etymology': 'From German "Klerisei", from "Klerus" (clergy), coined by Samuel Taylor Coleridge',
                'memory_tips': 'Think "clergy-see" - the clergy and intellectuals who see and understand scholarly matters',
                'alternate_spellings': '',
                'language_origin': 'German (via English coinage)',
                'example_sentence': 'The university\'s _____ gathered to discuss the implications of the new research findings.'
            },
            'clerks': {
                'definition': 'Office workers who keep records and perform routine administrative tasks; shop assistants; junior members of the clergy.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'KLURKS (emphasis on single syllable)',
                'etymology': 'From Old French "clerc", from Latin "clericus" (clergyman, scholar)',
                'memory_tips': 'Think of office workers who clerk (work) with papers and files',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'The bank employed several _____ to handle customer transactions and paperwork.'
            },
            'clever': {
                'definition': 'Quick to understand, learn, and devise solutions; skillful or adroit; showing intelligence or ingenuity.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'KLEV-er (emphasis on first syllable)',
                'etymology': 'From Middle English, possibly from Old Norse "kleyfr" (easy to split, handy)',
                'memory_tips': 'Think "cleave-er" - someone who can cleverly cleave through problems',
                'alternate_spellings': '',
                'language_origin': 'Middle English (possibly Old Norse)',
                'example_sentence': 'Her _____ solution to the puzzle impressed everyone in the room.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_035_data:
            return batch_035_data[word_lower]
        
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
    
    def process_batch_035(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 035 with comprehensive Claude data"""
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
    
    def save_batch_035_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 035 processed words to CSV"""
        
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
    """Process Batch 035 with comprehensive Claude data"""
    processor = Batch035Processor()
    input_csv = Path("output/batch_035_words.csv")
    output_csv = Path("output/batch_035_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 035 with comprehensive Claude data...")
    
    # Process all words in batch 035
    processed_words = processor.process_batch_035(input_csv)
    
    # Save results
    processor.save_batch_035_csv(processed_words, output_csv)
    
    logger.info(f"Batch 035 processing completed!")
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