#!/usr/bin/env python3
"""
Process Batch 033 of Spelling Bee Words with Comprehensive Claude Data
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

class Batch033Processor:
    """Processes Batch 033 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 033 words"""
        
        # Comprehensive data for all 50 words in Batch 033
        batch_033_data = {
            'chastisechortle': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "chastise" (to criticize severely) + "chortle" (to laugh gleefully).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "chastise" and "chortle"',
                'alternate_spellings': 'chastise + chortle (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'chastushka': {
                'definition': 'A type of Russian folk song or poem consisting of four lines with a specific rhyme scheme, often humorous or satirical in nature, typically accompanied by accordion or balalaika.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'chah-TOOSH-kah (emphasis on second syllable)',
                'etymology': 'From Russian "chastushka", diminutive of "chast" meaning "part" or "frequent"',
                'memory_tips': 'Think "chat-rush-ka" - a quick chat in Russian song form',
                'alternate_spellings': '',
                'language_origin': 'Russian',
                'example_sentence': 'The village musician entertained the crowd with a lively _____ about local gossip.'
            },
            'chasuble': {
                'definition': 'A sleeveless outer vestment worn by the priest celebrating Mass in the Roman Catholic Church and by celebrants in some other Christian churches, typically ornately decorated.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'CHAZ-uh-buhl (emphasis on first syllable)',
                'etymology': 'From Latin "casubula" or "casula", meaning "little house" or "hooded cloak"',
                'memory_tips': 'Think "chase-able" - the priest\'s garment that flows as if chaseable',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The priest donned his embroidered _____ before beginning the Easter service.'
            },
            'chatelaine': {
                'definition': 'The mistress of a large house or castle; a decorative belt hook or clasp worn at the waist, from which keys, trinkets, or useful items are suspended.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SHAT-uh-layn (emphasis on first syllable)',
                'etymology': 'From French "châtelaine", feminine of "châtelain" (castle keeper), from "château" (castle)',
                'memory_tips': 'Think "chattel-lane" - the lane where the lady of the castle keeps her chattels',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The Victorian _____ wore an ornate silver chain with scissors and thimble attached.'
            },
            'chaucerian': {
                'definition': 'Of, relating to, or characteristic of Geoffrey Chaucer (c. 1340-1400) or his literary works, particularly his storytelling style, humor, and Middle English language.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'chaw-SEER-ee-uhn (emphasis on second syllable)',
                'etymology': 'From "Chaucer" (Geoffrey Chaucer, English poet) + "-ian" (relating to)',
                'memory_tips': 'Think "Chaucer-ian" - relating to the famous medieval English poet',
                'alternate_spellings': '',
                'language_origin': 'Modern English (from proper name)',
                'example_sentence': 'The professor noted the _____ influence in the student\'s use of medieval storytelling techniques.'
            },
            'chauffeurs': {
                'definition': 'Professional drivers employed to drive private or hired automobiles; people who operate motor vehicles for others as their occupation.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'shoh-FURZ or SHOH-furz (emphasis varies)',
                'etymology': 'From French "chauffeur", literally "stoker" (one who stokes a fire), from "chauffer" (to heat)',
                'memory_tips': 'Think "show-furs" - drivers who show off in fancy cars with fur seats',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The hotel employed several experienced _____ to transport VIP guests to the airport.'
            },
            'chauve': {
                'definition': 'French word meaning "bald" or "hairless"; in English contexts, may refer to bald animals or geographic features without vegetation.',
                'part_of_speech': 'adjective (French borrowing)',
                'pronunciation_guide': 'SHOHV (rhymes with stove)',
                'etymology': 'From French "chauve", from Latin "calvus" meaning "bald"',
                'memory_tips': 'Think "shave" - what you do to become bald like chauve',
                'alternate_spellings': '',
                'language_origin': 'French (from Latin)',
                'example_sentence': 'The mountain peak was _____, completely bare of trees or vegetation.'
            },
            'check': {
                'definition': 'To examine something to determine its accuracy, quality, or condition; to verify or confirm; a written order directing a bank to pay money; a pattern of squares.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'CHEK (emphasis on single syllable)',
                'etymology': 'From Old French "eschequier", from "eschec" (chess), ultimately from Persian "shah" (king)',
                'memory_tips': 'Think "chess-check" - examining the king\'s position to verify safety',
                'alternate_spellings': 'cheque (British spelling for bank draft)',
                'language_origin': 'Old French (from Persian)',
                'example_sentence': 'Please _____ your answers carefully before submitting the exam.'
            },
            'cheek': {
                'definition': 'Either side of the face below the eye and between the nose and ear; impudent behavior or speech; boldness or audacity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'CHEEK (emphasis on single syllable)',
                'etymology': 'From Old English "ceace", from Proto-Germanic "*kaukōn"',
                'memory_tips': 'Think of the soft, round part of your face that you can pinch',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The child\'s rosy _____ showed she had been playing outside in the cold.'
            },
            'cheer': {
                'definition': 'To shout encouragement or approval; to make or become happier; a cry of encouragement or joy; happiness or optimism.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'CHEER (emphasis on single syllable)',
                'etymology': 'From Old French "chiere" meaning "face, countenance", from Latin "cara" (face)',
                'memory_tips': 'Think of a cheerleader - someone who spreads cheer and encouragement',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'The crowd began to _____ wildly when their team scored the winning goal.'
            },
            'cheese': {
                'definition': 'A food made from the pressed curds of milk, often aged and available in many varieties; something of poor quality (slang).',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'CHEEZ (emphasis on single syllable)',
                'etymology': 'From Old English "cese", from Latin "caseus" (cheese)',
                'memory_tips': 'Think of the yellow, holey Swiss cheese that mice love to eat',
                'alternate_spellings': '',
                'language_origin': 'Old English (from Latin)',
                'example_sentence': 'The delicatessen offered over fifty varieties of imported _____.'
            },
            'cheesy': {
                'definition': 'Resembling or containing cheese; of poor quality, cheap, or lacking in good taste; overly sentimental or corny.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'CHEE-zee (emphasis on first syllable)',
                'etymology': 'From "cheese" + "-y", where "cheese" comes from Latin "caseus"',
                'memory_tips': 'Think "cheese-y" - like cheese, but also tacky or low-quality',
                'alternate_spellings': '',
                'language_origin': 'Modern English (from Latin root)',
                'example_sentence': 'The movie\'s _____ dialogue made the audience laugh at inappropriate moments.'
            },
            'chef': {
                'definition': 'A professional cook who typically manages a kitchen and creates recipes in a restaurant or other dining establishment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SHEF (emphasis on single syllable)',
                'etymology': 'From French "chef de cuisine" (head of kitchen), from "chef" meaning "head, chief"',
                'memory_tips': 'Think of a tall white hat and apron - the classic chef uniform',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The renowned _____ created a special tasting menu for the anniversary dinner.'
            },
            'chefs': {
                'definition': 'Professional cooks who typically manage kitchens and create recipes in restaurants or other dining establishments.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'SHEFS (emphasis on single syllable)',
                'etymology': 'Plural of "chef", from French "chef de cuisine"',
                'memory_tips': 'Think of multiple professionals in tall white hats cooking together',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The cooking competition featured twelve talented _____ from around the world.'
            },
            'chefuncte': {
                'definition': 'A Native American word referring to the Chefuncte River area in Louisiana; may also refer to places or features named after this geographic location.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'shuh-FUNK-tee (emphasis on second syllable)',
                'etymology': 'From Choctaw or other Native American language, meaning uncertain, possibly related to water or river',
                'memory_tips': 'Think "she-funk-tea" - a Louisiana place name with Native American origins',
                'alternate_spellings': '',
                'language_origin': 'Native American (Choctaw)',
                'example_sentence': 'The _____ River flows through scenic Louisiana wetlands before joining Lake Pontchartrain.'
            },
            'chelonia': {
                'definition': 'The taxonomic order that includes all turtles, tortoises, and terrapins; reptiles characterized by having shells and retractable heads.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kuh-LOH-nee-ah (emphasis on second syllable)',
                'etymology': 'From Greek "chelone" meaning "turtle" + "-ia" (taxonomic suffix)',
                'memory_tips': 'Think "shell-onia" - the group of animals with shells (turtles)',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The biology student studied various species within the order _____.'
            },
            'chemical': {
                'definition': 'Relating to chemistry or the interactions of substances; a substance obtained by or used in chemical processes; artificial rather than natural.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'KEM-i-kuhl (emphasis on first syllable)',
                'etymology': 'From "chemistry" + "-al", where chemistry comes from "alchemy" via Arabic "al-kīmiyā"',
                'memory_tips': 'Think "chem-ical" - relating to chemistry with an "-ical" ending',
                'alternate_spellings': '',
                'language_origin': 'Arabic (via alchemy)',
                'example_sentence': 'The laboratory stored various _____ compounds in specially labeled containers.'
            },
            'chemise': {
                'definition': 'A loose-fitting undergarment or dress worn by women; a simple, straight-hanging dress or slip, typically reaching to the hips or thighs.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'shuh-MEEZ (emphasis on second syllable)',
                'etymology': 'From French "chemise", from Late Latin "camisia" (shirt, tunic)',
                'memory_tips': 'Think "she-meez" - a loose garment that women wear with ease',
                'alternate_spellings': '',
                'language_origin': 'French (from Late Latin)',
                'example_sentence': 'The vintage _____ featured delicate lace trim around the neckline.'
            },
            'chemistry': {
                'definition': 'The scientific study of the composition, structure, properties, and reactions of matter; the complex emotional or psychological interaction between people.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KEM-is-tree (emphasis on first syllable)',
                'etymology': 'From "alchemy" via Arabic "al-kīmiyā", from Greek "khēmeia" (art of transmuting metals)',
                'memory_tips': 'Think "chem-is-tree" - the science of elements branching like a tree',
                'alternate_spellings': '',
                'language_origin': 'Arabic (from Greek)',
                'example_sentence': 'The students conducted experiments in _____ class to learn about molecular reactions.'
            },
            'chemistryquandary': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "chemistry" (science of matter) + "quandary" (state of uncertainty).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "chemistry" and "quandary"',
                'alternate_spellings': 'chemistry + quandary (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'chemotherapy': {
                'definition': 'The treatment of cancer or other diseases with chemical substances or drugs that are toxic to the causative agent, particularly the use of anticancer drugs.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kee-moh-THER-ah-pee (emphasis on third syllable)',
                'etymology': 'From "chemo-" (chemical) + "therapy" (treatment), from Greek "therapeia" (healing)',
                'memory_tips': 'Think "chemo-therapy" - chemical therapy to treat cancer',
                'alternate_spellings': '',
                'language_origin': 'Modern medical (Greek elements)',
                'example_sentence': 'The oncologist recommended a six-month course of _____ to treat the patient\'s condition.'
            },
            'cheongsam': {
                'definition': 'A close-fitting dress with a high neck and slit skirt, worn by Chinese women; also known as qipao, it became popular in the 1920s Shanghai fashion scene.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'CHUNG-sam (emphasis on first syllable)',
                'etymology': 'From Cantonese Chinese, literally "long dress" or "long shirt"',
                'memory_tips': 'Think "cheong-sam" - a long, elegant Chinese dress',
                'alternate_spellings': 'qipao',
                'language_origin': 'Cantonese Chinese',
                'example_sentence': 'She wore a silk _____ with intricate embroidered flowers to the formal dinner.'
            },
            'chernobyl': {
                'definition': 'A city in Ukraine, site of the world\'s worst nuclear power plant disaster in 1986; often used to refer to nuclear accidents or contamination.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'cher-NOH-buhl (emphasis on second syllable)',
                'etymology': 'From Ukrainian, possibly meaning "place of wormwood" or related to "chornyi" (black)',
                'memory_tips': 'Think "chair-noble" - a place where noble chairs were contaminated by radiation',
                'alternate_spellings': 'Chornobyl (Ukrainian spelling)',
                'language_origin': 'Ukrainian',
                'example_sentence': 'The documentary explored the long-term effects of the _____ nuclear disaster on surrounding communities.'
            },
            'cherubic': {
                'definition': 'Having the innocent, chubby, rosy appearance associated with cherubs; angelic and childlike in appearance; sweet and innocent-looking.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'chuh-ROO-bik (emphasis on second syllable)',
                'etymology': 'From "cherub" + "-ic", where cherub comes from Hebrew "kerub" (angel)',
                'memory_tips': 'Think "cherub-ic" - like the cute baby angels in classical paintings',
                'alternate_spellings': '',
                'language_origin': 'Hebrew',
                'example_sentence': 'The toddler\'s _____ face made everyone smile at the family gathering.'
            },
            'cheshire': {
                'definition': 'Relating to Cheshire County in England; most famous in reference to the Cheshire Cat from Alice\'s Adventures in Wonderland, known for its distinctive grin.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'CHESH-eer or CHESH-er (emphasis on first syllable)',
                'etymology': 'From Old English "Ceaster" (Roman camp) + "scir" (shire), referring to Chester',
                'memory_tips': 'Think "chess-here" - a place where they play chess with a grinning cat',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'His _____ grin reminded everyone of the mysterious cat from the famous story.'
            },
            'chess': {
                'definition': 'A strategic board game played between two players on a checkered board with specially designed pieces, each player starting with sixteen pieces.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'CHES (emphasis on single syllable)',
                'etymology': 'From Old French "esches" (plural of "eschec"), from Persian "shah" (king)',
                'memory_tips': 'Think of the checkered board with the king and queen pieces',
                'alternate_spellings': '',
                'language_origin': 'Persian (via Old French)',
                'example_sentence': 'The grandmaster taught children the fundamentals of _____ at the community center.'
            },
            'chestnut': {
                'definition': 'A glossy brown nut that is edible when cooked; the tree that produces these nuts; a reddish-brown color; an old joke or story told repeatedly.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'CHES-nuht (emphasis on first syllable)',
                'etymology': 'From "chest" + "nut", where "chest" comes from Greek "kastanon" via Latin',
                'memory_tips': 'Think "chest-nut" - a nut that comes from a tree with a thick trunk like a chest',
                'alternate_spellings': '',
                'language_origin': 'Greek (via Latin)',
                'example_sentence': 'The street vendor sold roasted _____ from his cart on the cold winter evening.'
            },
            'chevalier': {
                'definition': 'A knight, especially a member of certain honorary orders; a French nobleman of the lowest rank; a chivalrous gentleman.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'shev-uh-LEER (emphasis on third syllable)',
                'etymology': 'From French "chevalier", from "cheval" (horse), from Latin "caballus" (horse)',
                'memory_tips': 'Think "shave-a-leer" - a knight who shaves with a leer of confidence',
                'alternate_spellings': '',
                'language_origin': 'French (from Latin)',
                'example_sentence': 'The _____ was known throughout the land for his honorable conduct and bravery.'
            },
            'chevrotain': {
                'definition': 'A small, deer-like mammal found in tropical forests of Africa and Asia, also called a mouse-deer, characterized by its diminutive size and primitive features.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SHEV-roh-tayn (emphasis on first syllable)',
                'etymology': 'From French "chevrotain", diminutive of "chevrot" (young goat), from "chèvre" (goat)',
                'memory_tips': 'Think "chevro-teen" - a tiny, teenage-sized deer-like animal',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The rare _____ is one of the world\'s smallest ungulates, weighing less than five pounds.'
            },
            'chia': {
                'definition': 'A flowering plant native to Mexico, valued for its edible seeds that are rich in omega-3 fatty acids and used as a health food supplement.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'CHEE-ah (emphasis on first syllable)',
                'etymology': 'From Spanish "chia", from Nahuatl "chian" meaning "oily"',
                'memory_tips': 'Think "cheer-ah" - seeds that make you cheer because they\'re so healthy',
                'alternate_spellings': '',
                'language_origin': 'Nahuatl (via Spanish)',
                'example_sentence': 'She added _____ seeds to her smoothie for extra protein and fiber.'
            },
            'chiasmus': {
                'definition': 'A rhetorical device in which words, grammatical constructions, or concepts are repeated in reverse order in successive phrases or clauses.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ky-AZ-muhs (emphasis on second syllable)',
                'etymology': 'From Greek "chiasmos", from "chiazein" (to mark with chi), referring to the X-shape of the letter chi',
                'memory_tips': 'Think "X-asmus" - crossing words in an X pattern like the Greek letter chi',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The famous example of _____ is "Ask not what your country can do for you—ask what you can do for your country."'
            },
            'chicago': {
                'definition': 'The third-largest city in the United States, located in Illinois on the shores of Lake Michigan; known for its architecture, culture, and wind.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'shih-KAH-goh (emphasis on second syllable)',
                'etymology': 'From Miami-Illinois "shikaakwa" meaning "striped skunk" or "wild onion place"',
                'memory_tips': 'Think "she-cargo" - a windy city that ships cargo across the Great Lakes',
                'alternate_spellings': '',
                'language_origin': 'Miami-Illinois (Native American)',
                'example_sentence': 'The architecture tour of _____ showcased the city\'s famous skyscrapers and innovative designs.'
            },
            'chicana': {
                'definition': 'A female American of Mexican descent; relating to the Chicano movement that emerged in the 1960s advocating for Mexican-American civil rights.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'chee-KAH-nah (emphasis on second syllable)',
                'etymology': 'Feminine form of "Chicano", possibly from "Mexicano" or from older Spanish slang',
                'memory_tips': 'Think "chic-Ana" - a stylish woman of Mexican-American heritage named Ana',
                'alternate_spellings': '',
                'language_origin': 'Spanish-American',
                'example_sentence': 'The _____ artist\'s paintings celebrated her Mexican-American cultural identity.'
            },
            'chicanery': {
                'definition': 'The use of deception or subterfuge to achieve one\'s purpose; trickery or dishonest manipulation, especially in legal or political contexts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'shih-KAY-nuh-ree (emphasis on second syllable)',
                'etymology': 'From French "chicanerie", from "chicaner" (to quibble), possibly from "chicane" (obstacle)',
                'memory_tips': 'Think "chic-canery" - stylish trickery in a can',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The lawyer accused his opponent of using legal _____ to delay the trial unfairly.'
            },
            'chicken': {
                'definition': 'A common domestic fowl raised for eggs and meat; the meat of this bird used as food; lacking courage or bravery (colloquial).',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'CHIK-in (emphasis on first syllable)',
                'etymology': 'From Old English "cicen", from Proto-Germanic "*kiukinam" (diminutive of cock)',
                'memory_tips': 'Think of the farm bird that says "cluck cluck" and lays eggs',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The farmer counted twenty _____ in the coop before closing it for the night.'
            },
            'chicle': {
                'definition': 'A gum-like substance obtained from the sapodilla tree, traditionally used as the base for chewing gum before synthetic substitutes were developed.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'CHIK-uhl (emphasis on first syllable)',
                'etymology': 'From Spanish "chicle", from Nahuatl "tzictli" (sticky thing)',
                'memory_tips': 'Think "chick-el" - what chicks would chew if they made gum from tree sap',
                'alternate_spellings': '',
                'language_origin': 'Nahuatl (via Spanish)',
                'example_sentence': 'Before synthetic gum, _____ was harvested from trees in Central America to make chewing gum.'
            },
            'chide': {
                'definition': 'To express disapproval of or scold gently; to reprove or rebuke someone for their actions or behavior, typically in a mild manner.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'CHYD (emphasis on single syllable, rhymes with "pride")',
                'etymology': 'From Old English "cidan", meaning "to complain, dispute, or quarrel"',
                'memory_tips': 'Think "child" - what parents do when they gently scold a child',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The teacher would gently _____ students who forgot to complete their homework assignments.'
            },
            'chief': {
                'definition': 'The leader or head of an organization, tribe, or group; most important or principal; highest in rank or authority.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'CHEEF (emphasis on single syllable)',
                'etymology': 'From Old French "chief", from Latin "caput" meaning "head"',
                'memory_tips': 'Think of the "big cheese" or head person who leads the group',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'The fire _____ coordinated the emergency response to the warehouse blaze.'
            },
            'chiefly': {
                'definition': 'Mainly or mostly; for the most part; primarily or principally; above all other considerations.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'CHEEF-lee (emphasis on first syllable)',
                'etymology': 'From "chief" + "-ly", where chief comes from Latin "caput" (head)',
                'memory_tips': 'Think "chief-ly" - in the manner of a chief or leader, primarily',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'The company\'s success was _____ due to its innovative marketing strategy.'
            },
            'chiffonade': {
                'definition': 'A culinary cutting technique in which leafy green vegetables or herbs are cut into long, thin strips by stacking, rolling, and slicing.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'shif-uh-NAHD (emphasis on third syllable)',
                'etymology': 'From French "chiffonnade", from "chiffon" (rag, cloth) referring to the ribbon-like strips',
                'memory_tips': 'Think "she-fon-ade" - making strips as thin as chiffon fabric',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The chef demonstrated how to _____ the basil leaves for the pasta garnish.'
            },
            'chihuahua': {
                'definition': 'A very small breed of dog originating from Mexico, characterized by its tiny size, large eyes, and alert expression; the largest state in Mexico.',
                'part_of_speech': 'noun (proper noun for place)',
                'pronunciation_guide': 'chih-WAH-wah (emphasis on second syllable)',
                'etymology': 'From the Mexican state of Chihuahua, possibly from Tarahumara "rahui wa" meaning "dry place"',
                'memory_tips': 'Think "chee-wow-wa" - the tiny dog that makes you say "wow" at its small size',
                'alternate_spellings': '',
                'language_origin': 'Mexican Spanish (from Tarahumara)',
                'example_sentence': 'The tiny _____ trembled with excitement whenever visitors came to the door.'
            },
            'child': {
                'definition': 'A young person below the age of puberty or below the legal age of majority; a son or daughter of any age; an immature or irresponsible person.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'CHYLD (emphasis on single syllable)',
                'etymology': 'From Old English "cild", from Proto-Germanic "*kiltham" (womb, fetus)',
                'memory_tips': 'Think of a young person who needs care and protection from adults',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'Every _____ deserves access to quality education and healthcare.'
            },
            'childhood': {
                'definition': 'The state or period of being a child; the time of life when one is young, typically before reaching adolescence.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'CHYLD-hood (emphasis on first syllable)',
                'etymology': 'From "child" + "-hood" (state or condition), where child comes from Old English "cild"',
                'memory_tips': 'Think "child-hood" - the time period when you wear the hood of being a child',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'Her _____ was filled with happy memories of summer vacations at the lake.'
            },
            'chill': {
                'definition': 'An unpleasant feeling of coldness; to make or become cold; to relax or calm down; cold in temperature or manner.',
                'part_of_speech': 'verb, noun, adjective',
                'pronunciation_guide': 'CHIL (emphasis on single syllable)',
                'etymology': 'From Old English "cele" or "ciele", meaning "cold, coolness"',
                'memory_tips': 'Think of getting goosebumps when you\'re cold, or "chilling out" to relax',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The autumn morning had a _____ in the air that made everyone reach for sweaters.'
            },
            'chimaera': {
                'definition': 'Alternative spelling of chimera; a mythological creature with parts from different animals; in biology, an organism with genetically distinct cells.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ky-MEER-ah or kuh-MEER-ah (emphasis on second syllable)',
                'etymology': 'From Latin "chimaera", from Greek "khimaira" (she-goat, monster)',
                'memory_tips': 'Think "key-mera" - a key-shaped monster from Greek mythology',
                'alternate_spellings': 'chimera',
                'language_origin': 'Greek (via Latin)',
                'example_sentence': 'The ancient Greek _____ was described as having a lion\'s head, goat\'s body, and serpent\'s tail.'
            },
            'chimera': {
                'definition': 'In Greek mythology, a fire-breathing monster with a lion\'s head, goat\'s body, and serpent\'s tail; any illusory or impossible idea; in biology, an organism with genetically distinct tissues.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ky-MEER-ah or kuh-MEER-ah (emphasis on second syllable)',
                'etymology': 'From Latin "chimaera", from Greek "khimaira" (she-goat, monster)',
                'memory_tips': 'Think "key-mera" - unlocking the mystery of this mythical creature',
                'alternate_spellings': 'chimaera',
                'language_origin': 'Greek (via Latin)',
                'example_sentence': 'The scientist\'s plan to create unlimited energy was dismissed as a _____.'
            },
            'chimes': {
                'definition': 'A set of tuned bells or metal tubes that produce musical tones when struck; the sounds produced by such instruments.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'CHYMZ (emphasis on single syllable)',
                'etymology': 'From Old French "chimbe", possibly from Latin "cymbalum" (cymbal)',
                'memory_tips': 'Think of church bells or doorbell sounds that "chime" musical tones',
                'alternate_spellings': '',
                'language_origin': 'Old French (possibly from Latin)',
                'example_sentence': 'The wind _____ on the porch created gentle melodies whenever the breeze stirred.'
            },
            'chimney': {
                'definition': 'A vertical structure containing a passage for smoke and gases to escape from a fireplace, furnace, or boiler to the outside air.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'CHIM-nee (emphasis on first syllable)',
                'etymology': 'From Old French "cheminée", from Latin "caminus" (furnace, forge)',
                'memory_tips': 'Think "chim-knee" - the tall structure that bends like a knee to let smoke escape',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'Santa Claus traditionally enters houses through the _____ on Christmas Eve.'
            },
            'chin': {
                'definition': 'The protruding part of the face below the mouth; the front part of the lower jaw; to pull oneself up using arm strength.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'CHIN (emphasis on single syllable)',
                'etymology': 'From Old English "cinn", from Proto-Germanic "*kinnuz"',
                'memory_tips': 'Think of the bottom point of your face below your mouth',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'She rested her _____ on her hand while thinking deeply about the problem.'
            },
            'china': {
                'definition': 'Fine porcelain or ceramic ware, originally imported from China; dishes and decorative objects made from this material; the country in East Asia.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'CHY-nah (emphasis on first syllable)',
                'etymology': 'From Persian "chīnī" meaning "Chinese", referring to the country where porcelain originated',
                'memory_tips': 'Think of delicate, breakable dishes that your grandmother keeps in a special cabinet',
                'alternate_spellings': 'China (proper noun for country)',
                'language_origin': 'Persian',
                'example_sentence': 'The family brought out their best _____ for the holiday dinner celebration.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_033_data:
            return batch_033_data[word_lower]
        
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
    
    def process_batch_033(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 033 with comprehensive Claude data"""
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
    
    def save_batch_033_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 033 processed words to CSV"""
        
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
    """Process Batch 033 with comprehensive Claude data"""
    processor = Batch033Processor()
    input_csv = Path("output/batch_033_words.csv")
    output_csv = Path("output/batch_033_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 033 with comprehensive Claude data...")
    
    # Process all words in batch 033
    processed_words = processor.process_batch_033(input_csv)
    
    # Save results
    processor.save_batch_033_csv(processed_words, output_csv)
    
    logger.info(f"Batch 033 processing completed!")
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