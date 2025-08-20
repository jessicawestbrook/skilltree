#!/usr/bin/env python3
"""
Process Batch 046 of Spelling Bee Words with Comprehensive Claude Data
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

class Batch046Processor:
    """Processes Batch 046 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 046 words"""
        
        # Comprehensive data for all 50 words in Batch 046
        batch_046_data = {
            'cushion': {
                'definition': 'A soft bag filled with air, feathers, foam, or other material, used to make something more comfortable or to protect against impacts.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'KOOSH-uhn (emphasis on first syllable)',
                'etymology': 'From Old French "coissin", from Latin "culcita" meaning "mattress, pillow"',
                'memory_tips': 'Think "cozy-shin" - something cozy to rest your shin on',
                'alternate_spellings': 'pillow, pad',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'She placed a _____ behind her back for extra comfort while reading.'
            },
            'custard': {
                'definition': 'A sweet dessert made from milk, eggs, and sugar, typically thickened by cooking and often flavored with vanilla.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KUHS-terd (emphasis on first syllable)',
                'etymology': 'From Middle English "crustade", meaning a tart with a crust, later applied to the filling',
                'memory_tips': 'Think "crust-ard" - originally a custard in a crust',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The creamy _____ was the perfect ending to the elegant dinner.'
            },
            'customer': {
                'definition': 'A person who purchases goods or services from a business; a client or patron.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KUHS-tuh-mer (emphasis on first syllable)',
                'etymology': 'From Middle English "custumer", from "custom" meaning habit, usage',
                'memory_tips': 'Think "custom-er" - someone who follows the custom of buying',
                'alternate_spellings': 'client, patron',
                'language_origin': 'Middle English',
                'example_sentence': 'The _____ was pleased with the excellent service at the restaurant.'
            },
            'cutaneous': {
                'definition': 'Relating to or affecting the skin; having to do with the outer layer of the body.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'kyoo-TAY-nee-us (emphasis on second syllable)',
                'etymology': 'From Latin "cutaneus", from "cutis" meaning "skin"',
                'memory_tips': 'Think "cut-aneous" - related to what you can cut (the skin)',
                'alternate_spellings': 'dermal, skin-related',
                'language_origin': 'Latin',
                'example_sentence': 'The doctor examined the patient for any _____ abnormalities.'
            },
            'cute': {
                'definition': 'Attractive in a pretty or endearing way; appealing, especially in a small or delicate manner.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'KYOOT (emphasis on first syllable)',
                'etymology': 'Originally short for "acute", meaning clever or shrewd, later meaning attractive',
                'memory_tips': 'Think of "acute" angle - sharp and appealing',
                'alternate_spellings': 'adorable, sweet',
                'language_origin': 'Latin via Middle English',
                'example_sentence': 'The puppy was so _____ that everyone wanted to pet it.'
            },
            'cutis': {
                'definition': 'The skin, especially the deeper layer (dermis) beneath the epidermis; used in medical terminology.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KYOO-tis (emphasis on first syllable)',
                'etymology': 'From Latin "cutis" meaning "skin"',
                'memory_tips': 'Think "cut-is" - what you cut is the skin',
                'alternate_spellings': 'dermis, skin',
                'language_origin': 'Latin',
                'example_sentence': 'The dermatologist studied the structure of the _____ in detail.'
            },
            'cutiscyanosis': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "cutis" (skin) + "cyanosis" (bluish discoloration).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "cutis" and "cyanosis"',
                'alternate_spellings': 'cutis + cyanosis (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'cutlery': {
                'definition': 'Sharp cutting implements, especially knives, forks, and spoons used for eating; collectively, eating utensils.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KUHT-luh-ree (emphasis on first syllable)',
                'etymology': 'From Old French "coutelier", from "coutel" meaning "knife"',
                'memory_tips': 'Think "cut-lery" - tools used for cutting and eating',
                'alternate_spellings': 'silverware, utensils',
                'language_origin': 'Old French',
                'example_sentence': 'The formal dinner table was set with the finest silver _____.'
            },
            'cutter': {
                'definition': 'A person or tool that cuts; a type of small, fast sailing vessel; a small boat used by larger ships.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KUHT-er (emphasis on first syllable)',
                'etymology': 'From "cut" + "-er" (agent suffix)',
                'memory_tips': 'Think "cut-ter" - one who cuts',
                'alternate_spellings': 'blade, slicer',
                'language_origin': 'English',
                'example_sentence': 'The paper _____ made precise slices through the thick cardboard.'
            },
            'cutting': {
                'definition': 'The action of using a sharp tool to divide or slice; a piece cut from a plant for propagation; harsh or hurtful in speech.',
                'part_of_speech': 'noun, adjective, verb (present participle)',
                'pronunciation_guide': 'KUHT-ing (emphasis on first syllable)',
                'etymology': 'From "cut" + "-ing" (present participle suffix)',
                'memory_tips': 'Think "cut-ting" - the ongoing action of cutting',
                'alternate_spellings': 'slicing, sharp',
                'language_origin': 'English',
                'example_sentence': 'The gardener took a _____ from the rose bush to grow a new plant.'
            },
            'cyanosis': {
                'definition': 'A bluish discoloration of the skin and mucous membranes due to insufficient oxygen in the blood.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'sahy-uh-NOH-sis (emphasis on third syllable)',
                'etymology': 'From Greek "kyanos" meaning "blue" + "-osis" meaning "condition"',
                'memory_tips': 'Think "cyan-osis" - cyan blue skin condition',
                'alternate_spellings': 'blue skin syndrome',
                'language_origin': 'Greek',
                'example_sentence': 'The patient showed signs of _____ around the lips and fingertips.'
            },
            'cyanosisregurgitate': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "cyanosis" (blue skin condition) + "regurgitate" (to bring back up).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "cyanosis" and "regurgitate"',
                'alternate_spellings': 'cyanosis + regurgitate (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'cybernetics': {
                'definition': 'The science of communication and control in machines and living beings; the study of automatic control systems.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'sahy-ber-NET-iks (emphasis on third syllable)',
                'etymology': 'From Greek "kybernetes" meaning "helmsman, governor" + "-ics"',
                'memory_tips': 'Think "cyber-net-ics" - the science of cyber networks',
                'alternate_spellings': 'automation science',
                'language_origin': 'Greek',
                'example_sentence': 'The field of _____ studies how machines and humans process information.'
            },
            'cyberneticsgarniture': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "cybernetics" (automation science) + "garniture" (decoration, garnish).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "cybernetics" and "garniture"',
                'alternate_spellings': 'cybernetics + garniture (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'cycle': {
                'definition': 'A series of events that repeat in a regular sequence; a complete rotation or revolution; to ride a bicycle.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'SAHY-kuhl (emphasis on first syllable)',
                'etymology': 'From Greek "kyklos" meaning "circle, wheel"',
                'memory_tips': 'Think "circle" - a cycle goes in a circular pattern',
                'alternate_spellings': 'loop, sequence',
                'language_origin': 'Greek',
                'example_sentence': 'The water _____ includes evaporation, condensation, and precipitation.'
            },
            'cyclone': {
                'definition': 'A violent rotating windstorm; a system of winds rotating around a center of low atmospheric pressure.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SAHY-klohn (emphasis on first syllable)',
                'etymology': 'From Greek "kyklon", present participle of "kykloun" meaning "to rotate"',
                'memory_tips': 'Think "cycle-own" - wind that cycles and owns the area',
                'alternate_spellings': 'hurricane, typhoon',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ caused widespread damage as it moved across the coast.'
            },
            'cyclops': {
                'definition': 'In Greek mythology, a member of a race of giants with a single eye in the center of the forehead.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SAHY-klops (emphasis on first syllable)',
                'etymology': 'From Greek "Kyklops", from "kyklos" (circle) + "ops" (eye)',
                'memory_tips': 'Think "cycle-ops" - one circular eye operation',
                'alternate_spellings': 'one-eyed giant',
                'language_origin': 'Greek',
                'example_sentence': 'Odysseus cleverly escaped from the cave of the _____ Polyphemus.'
            },
            'cygnet': {
                'definition': 'A young swan, especially one that has not yet developed its adult plumage.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIG-nit (emphasis on first syllable)',
                'etymology': 'From Old French "cigne", from Latin "cygnus" meaning "swan"',
                'memory_tips': 'Think "signet" ring - a young swan is like a precious signet',
                'alternate_spellings': 'young swan',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The _____ followed its mother closely as they glided across the lake.'
            },
            'cylindrical': {
                'definition': 'Having the shape of a cylinder; round with straight parallel sides and circular ends.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'suh-LIN-dri-kuhl (emphasis on second syllable)',
                'etymology': 'From Greek "kylindros" meaning "roller" + "-ical"',
                'memory_tips': 'Think "cylinder-ical" - having the characteristics of a cylinder',
                'alternate_spellings': 'tube-shaped, round',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ container rolled easily down the inclined ramp.'
            },
            'cymbals': {
                'definition': 'A pair of musical instruments consisting of slightly concave round brass plates that are struck together or with drumsticks.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'SIM-buhlz (emphasis on first syllable)',
                'etymology': 'From Greek "kymbalon", from "kymbe" meaning "bowl"',
                'memory_tips': 'Think "symbol-s" - symbols of music that clash together',
                'alternate_spellings': 'crash cymbals',
                'language_origin': 'Greek',
                'example_sentence': 'The drummer crashed the _____ together at the climax of the song.'
            },
            'cynicism': {
                'definition': 'An attitude of scornful or jaded negativity; the belief that people are motivated purely by self-interest.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIN-uh-sizm (emphasis on first syllable)',
                'etymology': 'From Greek "kynikos" meaning "dog-like", from the Cynic philosophers who lived simply',
                'memory_tips': 'Think "sin-icism" - the belief that everyone sins (acts selfishly)',
                'alternate_spellings': 'skepticism, pessimism',
                'language_origin': 'Greek',
                'example_sentence': 'His years in politics had filled him with _____ about human nature.'
            },
            'cynocephali': {
                'definition': 'Mythical creatures with human bodies and dog heads; in medieval lore, a race of dog-headed people.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'sahy-nuh-SEF-uh-lahy (emphasis on third syllable)',
                'etymology': 'From Greek "kynokephalos", from "kyon" (dog) + "kephale" (head)',
                'memory_tips': 'Think "cyno-cephali" - "cyno" means dog, "cephali" means heads',
                'alternate_spellings': 'dog-headed people',
                'language_origin': 'Greek',
                'example_sentence': 'Medieval maps often depicted the _____ living in distant, unexplored lands.'
            },
            'cytoplasm': {
                'definition': 'The jelly-like substance that fills a cell, surrounding the nucleus and containing various organelles.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SAHY-tuh-plazm (emphasis on first syllable)',
                'etymology': 'From Greek "kytos" meaning "cell" + "plasma" meaning "something formed"',
                'memory_tips': 'Think "cyto-plasm" - the plasm (substance) inside the cyto (cell)',
                'alternate_spellings': 'cell fluid',
                'language_origin': 'Greek',
                'example_sentence': 'The organelles floated freely in the cell\'s _____.'
            },
            'dactylic': {
                'definition': 'Relating to or written in dactyls, a metrical foot in poetry consisting of one stressed syllable followed by two unstressed syllables.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dak-TIL-ik (emphasis on second syllable)',
                'etymology': 'From Greek "daktylikos", from "daktylos" meaning "finger" (referring to the three joints)',
                'memory_tips': 'Think "dactyl-ic" - like a finger with three parts (one stressed, two unstressed)',
                'alternate_spellings': 'dactylic meter',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ meter gave the poem a distinctive rhythmic pattern.'
            },
            'daft': {
                'definition': 'Silly or foolish; lacking good sense or judgment; mildly eccentric.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DAFT (emphasis on first syllable)',
                'etymology': 'From Middle English "dafte" meaning "mild, gentle", later "silly"',
                'memory_tips': 'Think "draft" without the "r" - silly like a rough draft',
                'alternate_spellings': 'silly, foolish',
                'language_origin': 'Middle English',
                'example_sentence': 'That\'s a _____ idea - it will never work in practice.'
            },
            'daguerreotype': {
                'definition': 'An early photographic process using silver-plated copper sheets; a photograph made by this process.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'duh-GAIR-uh-tahyp (emphasis on second syllable)',
                'etymology': 'Named after Louis Daguerre, the French inventor of the process',
                'memory_tips': 'Think "da-Guerre-type" - the type of photo invented by Daguerre',
                'alternate_spellings': 'early photograph',
                'language_origin': 'French (proper name)',
                'example_sentence': 'The museum displayed a rare _____ from the 1840s.'
            },
            'dainty': {
                'definition': 'Delicately small and pretty; refined or fastidious, especially in eating; a small, choice morsel of food.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'DAYN-tee (emphasis on first syllable)',
                'etymology': 'From Old French "daintie", from Latin "dignitas" meaning "worth, dignity"',
                'memory_tips': 'Think "ain\'t-y" - something that ain\'t big, but is delicate',
                'alternate_spellings': 'delicate, refined',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'She ate with _____ bites, savoring each morsel of the exquisite meal.'
            },
            'dais': {
                'definition': 'A raised platform or stage, especially one used by speakers or for ceremonies; a place of honor.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DAY-is (emphasis on first syllable)',
                'etymology': 'From Old French "deis", from Latin "discus" meaning "disk, platform"',
                'memory_tips': 'Think "days" - where important people spend their days speaking',
                'alternate_spellings': 'platform, stage',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The speaker stood on the _____ to address the large audience.'
            },
            'daisy': {
                'definition': 'A small white flower with a yellow center, commonly found in lawns and meadows; any of various composite flowers.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DAY-zee (emphasis on first syllable)',
                'etymology': 'From Old English "dæges eage" meaning "day\'s eye" (opens in daylight)',
                'memory_tips': 'Think "day\'s eye" - the flower that opens its eye to the day',
                'alternate_spellings': 'day\'s eye',
                'language_origin': 'Old English',
                'example_sentence': 'Children love to make chains from the simple _____ flowers.'
            },
            'daliesque': {
                'definition': 'Resembling or characteristic of the surrealist art style of Salvador Dalí; dreamlike and fantastical.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dah-lee-ESK (emphasis on third syllable)',
                'etymology': 'From Salvador Dalí (Spanish artist) + "-esque" (in the style of)',
                'memory_tips': 'Think "Dali-esque" - in the style of Salvador Dali\'s surreal art',
                'alternate_spellings': 'surrealistic',
                'language_origin': 'Spanish (proper name) + French suffix',
                'example_sentence': 'The melting clocks in his painting were distinctly _____.'
            },
            'dalmatian': {
                'definition': 'A breed of dog known for its white coat with black or brown spots; relating to Dalmatia, a region in Croatia.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'dal-MAY-shuhn (emphasis on second syllable)',
                'etymology': 'From Dalmatia, a coastal region of Croatia where the breed originated',
                'memory_tips': 'Think "dal-ma-tion" - the spotted dog nation',
                'alternate_spellings': 'spotted dog',
                'language_origin': 'Geographic name (Dalmatia)',
                'example_sentence': 'The _____ ran alongside the fire truck, its spots flashing in the sunlight.'
            },
            'damaged': {
                'definition': 'Having been harmed, injured, or impaired; suffering from physical or functional deterioration.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'DAM-ijd (emphasis on first syllable)',
                'etymology': 'From Old French "damage", from Latin "damnum" meaning "loss, harm"',
                'memory_tips': 'Think "dam-aged" - harmed like an old dam that has aged',
                'alternate_spellings': 'harmed, impaired',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The _____ car was towed away after the accident.'
            },
            'damascened': {
                'definition': 'Decorated with watered steel patterns; inlaid with gold or silver wire in the style of Damascus metalwork.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'DAM-uh-seend (emphasis on first syllable)',
                'etymology': 'From Damascus, the Syrian city famous for its metalworking techniques',
                'memory_tips': 'Think "Damascus-ened" - worked in the Damascus style',
                'alternate_spellings': 'inlaid, decorated',
                'language_origin': 'Arabic via geographic name',
                'example_sentence': 'The sword\'s _____ blade showed intricate patterns of gold inlay.'
            },
            'dame': {
                'definition': 'A woman of rank or authority; a title of honor for women; an elderly or mature woman.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DAYM (emphasis on first syllable)',
                'etymology': 'From Old French "dame", from Latin "domina" meaning "lady, mistress"',
                'memory_tips': 'Think "same" with "d" - a lady of the same high rank',
                'alternate_spellings': 'lady, madam',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The _____ was honored for her contributions to charity.'
            },
            'damp': {
                'definition': 'Slightly wet or moist; containing moisture; to make slightly wet or to reduce the intensity of something.',
                'part_of_speech': 'adjective, verb, noun',
                'pronunciation_guide': 'DAMP (emphasis on first syllable)',
                'etymology': 'From Middle English, possibly from Old Norse "dampi" meaning "vapor"',
                'memory_tips': 'Think "damp" like a camp that got wet',
                'alternate_spellings': 'moist, humid',
                'language_origin': 'Middle English, possibly Old Norse',
                'example_sentence': 'The basement felt _____ after the heavy rainfall.'
            },
            'damson': {
                'definition': 'A small, dark purple plum with a tart flavor, often used for making jams and preserves.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DAM-zuhn (emphasis on first syllable)',
                'etymology': 'From Latin "prunum Damascenum" meaning "plum of Damascus"',
                'memory_tips': 'Think "Damascus-on" - the plum from Damascus',
                'alternate_spellings': 'damson plum',
                'language_origin': 'Latin via geographic name',
                'example_sentence': 'She made delicious jam from the tart _____ plums.'
            },
            'dance': {
                'definition': 'To move rhythmically to music; a series of rhythmic steps and movements; a social gathering where people dance.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'DANS (emphasis on first syllable)',
                'etymology': 'From Old French "dancier", of unknown origin',
                'memory_tips': 'Think "chance" with "d" - taking a chance to move to music',
                'alternate_spellings': 'boogie, groove',
                'language_origin': 'Old French',
                'example_sentence': 'The couple learned to _____ the waltz for their wedding.'
            },
            'dancing': {
                'definition': 'The activity of moving rhythmically to music; performing dance movements.',
                'part_of_speech': 'noun, verb (present participle)',
                'pronunciation_guide': 'DAN-sing (emphasis on first syllable)',
                'etymology': 'From "dance" + "-ing"',
                'memory_tips': 'Think "dance-ing" - actively doing the dance',
                'alternate_spellings': 'choreography, movement',
                'language_origin': 'Old French + English suffix',
                'example_sentence': 'The children spent the afternoon _____ to their favorite songs.'
            },
            'dandelion': {
                'definition': 'A yellow-flowered weed with deeply notched leaves and fluffy seed heads that blow away in the wind.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DAN-duh-lahy-uhn (emphasis on first syllable)',
                'etymology': 'From French "dent de lion" meaning "lion\'s tooth" (referring to the leaf shape)',
                'memory_tips': 'Think "dandy-lion" - a dandy little lion-toothed flower',
                'alternate_spellings': 'lion\'s tooth',
                'language_origin': 'French',
                'example_sentence': 'Children love to blow the seeds off a _____ and make wishes.'
            },
            'dandle': {
                'definition': 'To move a baby or young child gently up and down on one\'s knee or in one\'s arms; to pamper or treat indulgently.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'DAN-duhl (emphasis on first syllable)',
                'etymology': 'Of uncertain origin, possibly imitative of gentle bouncing motion',
                'memory_tips': 'Think "handle" with "d" - how you handle a baby gently',
                'alternate_spellings': 'bounce, rock',
                'language_origin': 'Unknown, possibly imitative',
                'example_sentence': 'The grandfather would _____ his grandson on his knee while singing lullabies.'
            },
            'dandruff': {
                'definition': 'Small white or gray flakes of dead skin that fall from the scalp; a common scalp condition.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DAN-druhf (emphasis on first syllable)',
                'etymology': 'From "dander" (scurf) + "ruff" (rough), possibly influenced by dandriff',
                'memory_tips': 'Think "dander-rough" - rough dander falling from the head',
                'alternate_spellings': 'scalp flakes',
                'language_origin': 'English compound',
                'example_sentence': 'The special shampoo helped reduce his _____.'
            },
            'dangerous': {
                'definition': 'Likely to cause harm or injury; involving risk or peril; threatening safety.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DAYN-jer-uhs (emphasis on first syllable)',
                'etymology': 'From Old French "dangereus", from "danger" meaning "power to harm"',
                'memory_tips': 'Think "danger-ous" - full of danger',
                'alternate_spellings': 'hazardous, risky',
                'language_origin': 'Old French',
                'example_sentence': 'The _____ storm forced everyone to seek shelter indoors.'
            },
            'danseur': {
                'definition': 'A male ballet dancer; a man who performs classical dance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dan-SUR (emphasis on second syllable)',
                'etymology': 'From French "danseur", from "danser" meaning "to dance"',
                'memory_tips': 'Think "dance-sir" - a sir who dances ballet',
                'alternate_spellings': 'male dancer',
                'language_origin': 'French',
                'example_sentence': 'The skilled _____ performed a perfect grand jeté across the stage.'
            },
            'danta': {
                'definition': 'A South American tapir; a large, herbivorous mammal with a flexible snout, found in tropical forests.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DAN-tah (emphasis on first syllable)',
                'etymology': 'From Spanish "danta", from a South American indigenous language',
                'memory_tips': 'Think "Dan-ta" - Dan\'s favorite tapir animal',
                'alternate_spellings': 'tapir',
                'language_origin': 'Indigenous South American via Spanish',
                'example_sentence': 'The _____ used its flexible snout to browse among the forest vegetation.'
            },
            'daoism': {
                'definition': 'A Chinese philosophy and religion emphasizing harmony with the Tao (the Way); also called Taoism.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOW-izm (emphasis on first syllable)',
                'etymology': 'From Chinese "dao" meaning "way, path" + "-ism"',
                'memory_tips': 'Think "dao-ism" - the way-ism, the philosophy of the Way',
                'alternate_spellings': 'Taoism',
                'language_origin': 'Chinese',
                'example_sentence': 'The principles of _____ emphasize living in harmony with nature.'
            },
            'dapper': {
                'definition': 'Neat and trim in dress and appearance; stylishly dressed; smart in appearance.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DAP-er (emphasis on first syllable)',
                'etymology': 'From Middle Dutch "dapper" meaning "brave, strong"',
                'memory_tips': 'Think "dap-per" - someone who daps (steps) perfectly in style',
                'alternate_spellings': 'stylish, well-dressed',
                'language_origin': 'Middle Dutch',
                'example_sentence': 'The _____ gentleman adjusted his bow tie before entering the gala.'
            },
            'dappled': {
                'definition': 'Marked with spots or patches of different colors or shades; having a mottled appearance.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DAP-uhld (emphasis on first syllable)',
                'etymology': 'From "dapple" meaning "spotted", of uncertain origin',
                'memory_tips': 'Think "apple-d" - spotted like different colored apples',
                'alternate_spellings': 'spotted, mottled',
                'language_origin': 'Unknown origin',
                'example_sentence': 'The _____ sunlight filtered through the forest canopy.'
            },
            'daredevil': {
                'definition': 'A person who enjoys doing dangerous things; someone who takes extreme risks for excitement.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'DAIR-dev-uhl (emphasis on first syllable)',
                'etymology': 'From "dare" + "devil" (one who dares the devil)',
                'memory_tips': 'Think "dare-devil" - someone who dares to challenge even the devil',
                'alternate_spellings': 'thrill-seeker, risk-taker',
                'language_origin': 'English compound',
                'example_sentence': 'The _____ motorcyclist jumped over twelve cars in front of the amazed crowd.'
            },
            'daresay': {
                'definition': 'To venture to say; to think it likely; used to express polite assumption or mild assertion.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'DAIR-say (emphasis on first syllable)',
                'etymology': 'From "dare" + "say" (to venture to say)',
                'memory_tips': 'Think "dare-say" - to dare to say something',
                'alternate_spellings': 'venture to say',
                'language_origin': 'English compound',
                'example_sentence': 'I _____ you\'ll find the museum quite interesting.'
            },
            'darjeeling': {
                'definition': 'A type of black tea grown in the Darjeeling district of India, known for its distinctive flavor and aroma.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dahr-JEE-ling (emphasis on second syllable)',
                'etymology': 'From Darjeeling, a town in West Bengal, India where the tea is grown',
                'memory_tips': 'Think "dar-jeeling" - the dark tea that\'s feeling good',
                'alternate_spellings': 'Darjeeling tea',
                'language_origin': 'Geographic name (Indian)',
                'example_sentence': 'She savored her afternoon cup of fragrant _____ tea.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_046_data:
            return batch_046_data[word_lower]
        
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
    
    def process_batch_046(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 046 with comprehensive Claude data"""
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
    
    def save_batch_046_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 046 processed words to CSV"""
        
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
    """Process Batch 046 with comprehensive Claude data"""
    processor = Batch046Processor()
    input_csv = Path("output/batch_046_words.csv")
    output_csv = Path("output/batch_046_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 046 with comprehensive Claude data...")
    
    # Process all words in batch 046
    processed_words = processor.process_batch_046(input_csv)
    
    # Save results
    processor.save_batch_046_csv(processed_words, output_csv)
    
    logger.info(f"Batch 046 processing completed!")
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