#!/usr/bin/env python3
"""
Process Batch 132 of Spelling Bee Words with Comprehensive Claude Data
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
            'government', 'company', 'number', 'group', 'problem', 'fact', 'pick', 'picture', 'piece', 'phone', 'physical'
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
            'mega', 'micro', 'mini', 'multi', 'neo', 'pseudo', 'ultra', 'photo', 'phys'
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

class Batch132Processor:
    """Processes Batch 132 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 132 words"""
        
        # Comprehensive data for all 50 words in Batch 132
        batch_132_data = {
            'phlebotomy': {
                'definition': 'The medical practice of drawing blood from patients for diagnostic testing, blood donation, or therapeutic treatment; the art and science of venipuncture.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fluh-BOT-uh-mee (emphasis on second syllable)',
                'etymology': 'From Greek "phlebos" meaning "vein" + "tomia" meaning "cutting"',
                'memory_tips': 'Think "fleabotomy" - cutting into veins like a flea bites for blood',
                'alternate_spellings': 'venipuncture, bloodletting',
                'language_origin': 'Greek',
                'example_sentence': 'The nurse performed _____ to collect blood samples for laboratory analysis.'
            },
            'phlegmatic': {
                'definition': 'Having a calm, unemotional temperament; not easily excited or made angry; characterized by coolness and composure.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'fleg-MAT-ik (emphasis on second syllable)',
                'etymology': 'From Greek "phlegmatikos", from "phlegma" meaning "inflammation, mucus"',
                'memory_tips': 'Think "fleg-matic" - so calm they seem almost automatic',
                'alternate_spellings': 'calm, unemotional',
                'language_origin': 'Greek',
                'example_sentence': 'Despite the chaos around him, he remained _____ and focused on the task.'
            },
            'phloem': {
                'definition': 'The tissue in plants that transports nutrients, especially sugars produced by photosynthesis, from the leaves to other parts of the plant.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLOH-em (emphasis on first syllable)',
                'etymology': 'From Greek "phloios" meaning "bark"',
                'memory_tips': 'Think "flow-em" - nutrients flow through em (them)',
                'alternate_spellings': 'food-conducting tissue',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ carries sugar from the leaves to the roots and other plant parts.'
            },
            'phlox': {
                'definition': 'A flowering plant with clusters of colorful, often fragrant flowers, popular in gardens and native to North America.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLOKS (emphasis on first syllable)',
                'etymology': 'From Greek "phlox" meaning "flame", referring to the bright flower colors',
                'memory_tips': 'Think "flocks" - flocks of colorful flowers',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The garden was filled with pink and purple _____ blooming in the summer heat.'
            },
            'phobos': {
                'definition': 'The larger and closer of the two moons of Mars, named after the Greek god of fear; also refers to fear or panic in general.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'FOH-bohs (emphasis on first syllable)',
                'etymology': 'From Greek "Phobos", the personification of fear in Greek mythology',
                'memory_tips': 'Think "foe-boss" - a fearsome foe that is the boss of fear',
                'alternate_spellings': 'fear, panic',
                'language_origin': 'Greek',
                'example_sentence': 'The spacecraft captured detailed images of _____, the irregularly shaped moon of Mars.'
            },
            'phoenix': {
                'definition': 'A mythical bird that cyclically burns itself to death and rises from its own ashes; a symbol of renewal and rebirth.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FEE-niks (emphasis on first syllable)',
                'etymology': 'From Greek "phoinix" meaning "purple-red", referring to the bird\'s fiery colors',
                'memory_tips': 'Think "fee-nicks" - it costs a fee to see this mythical bird nick death',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Like a _____ rising from the ashes, the company rebuilt stronger after bankruptcy.'
            },
            'phone': {
                'definition': 'A device used for transmitting and receiving voice communications over distances; short for telephone.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FOHN (emphasis on syllable)',
                'etymology': 'From Greek "phone" meaning "voice, sound"',
                'memory_tips': 'Think "fone" - a device for your voice',
                'alternate_spellings': 'telephone',
                'language_origin': 'Greek',
                'example_sentence': 'She answered the _____ on the first ring.'
            },
            'phonetician': {
                'definition': 'A specialist in phonetics; someone who studies the sounds of human speech and their production, transmission, and reception.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'foh-nuh-TISH-uhn (emphasis on third syllable)',
                'etymology': 'From Greek "phone" (sound) + "technician"',
                'memory_tips': 'Think "phone-technician" - a technician who specializes in phone sounds',
                'alternate_spellings': 'speech sound specialist',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ analyzed the subtle differences in vowel pronunciation across dialects.'
            },
            'phoneticianmacular': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "phonetician" (speech sound specialist) + "macular" (relating to spots/macula).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "phonetician" and "macular"',
                'alternate_spellings': 'phonetician + macular (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'phonics': {
                'definition': 'A method of teaching reading and spelling based on the relationship between sounds and their corresponding letters or letter combinations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FON-iks (emphasis on first syllable)',
                'etymology': 'From Greek "phone" meaning "sound" + "-ics" meaning "study of"',
                'memory_tips': 'Think "fon-icks" - sounds that make you say "ick" when learning to read',
                'alternate_spellings': 'phonetic method',
                'language_origin': 'Greek',
                'example_sentence': 'The teacher used _____ to help students decode unfamiliar words.'
            },
            'phosphorescent': {
                'definition': 'Emitting light without heat after being exposed to radiation; glowing with a soft, steady light that continues after the light source is removed.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'fos-fuh-RES-uhnt (emphasis on third syllable)',
                'etymology': 'From Greek "phosphoros" meaning "light-bearing" + "-escent" meaning "becoming"',
                'memory_tips': 'Think "phosphor-essence" - the essence of light-bearing phosphor',
                'alternate_spellings': 'luminescent, glowing',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ plankton created a magical glow in the ocean waves.'
            },
            'photogenic': {
                'definition': 'Looking attractive in photographs; having features that photograph well; capable of being photographed.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'foh-tuh-JEN-ik (emphasis on third syllable)',
                'etymology': 'From Greek "photos" meaning "light" + "genes" meaning "born, produced"',
                'memory_tips': 'Think "photo-genic" - having genes that are good for photos',
                'alternate_spellings': 'camera-friendly',
                'language_origin': 'Greek',
                'example_sentence': 'The model was naturally _____ and looked stunning in every shot.'
            },
            'photosynthesis': {
                'definition': 'The process by which plants use sunlight, carbon dioxide, and water to produce glucose and oxygen; the conversion of light energy into chemical energy.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'foh-toh-SIN-thuh-sis (emphasis on third syllable)',
                'etymology': 'From Greek "photos" meaning "light" + "synthesis" meaning "putting together"',
                'memory_tips': 'Think "photo-synthesis" - photos of light being synthesized into food',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'During _____, plants convert sunlight into energy they can use for growth.'
            },
            'photovoltaic': {
                'definition': 'Relating to the production of electric current when light strikes certain materials; capable of generating electricity from light.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'foh-toh-vol-TAY-ik (emphasis on fourth syllable)',
                'etymology': 'From Greek "photos" meaning "light" + "voltaic" from Alessandro Volta',
                'memory_tips': 'Think "photo-voltaic" - photos (light) creating voltage',
                'alternate_spellings': 'solar electric',
                'language_origin': 'Greek and Modern Scientific',
                'example_sentence': 'The _____ panels on the roof generate clean electricity from sunlight.'
            },
            'phraseology': {
                'definition': 'The study of phrases and expressions; the particular way in which words and phrases are arranged and used in language.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fray-zee-OL-uh-jee (emphasis on third syllable)',
                'etymology': 'From Greek "phrasis" meaning "speech, phrase" + "-ology" meaning "study of"',
                'memory_tips': 'Think "phrase-ology" - the ology (study) of phrases',
                'alternate_spellings': 'phrasal study',
                'language_origin': 'Greek',
                'example_sentence': 'The linguist specialized in the _____ of regional dialects.'
            },
            'phulkari': {
                'definition': 'A traditional form of embroidery from the Punjab region of India and Pakistan, characterized by bright floral patterns on cotton fabric.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOOL-kah-ree (emphasis on first syllable)',
                'etymology': 'From Punjabi "phul" meaning "flower" + "kari" meaning "work"',
                'memory_tips': 'Think "full-carry" - carrying full loads of colorful flower patterns',
                'alternate_spellings': '',
                'language_origin': 'Punjabi',
                'example_sentence': 'The bride wore a beautiful _____ dupatta embroidered with vibrant flowers.'
            },
            'phycology': {
                'definition': 'The scientific study of algae; the branch of botany that deals with algae and their classification, structure, and ecology.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fy-KOL-uh-jee (emphasis on second syllable)',
                'etymology': 'From Greek "phykos" meaning "seaweed, algae" + "-ology" meaning "study of"',
                'memory_tips': 'Think "fickle-ology" - the fickle study of ever-changing algae',
                'alternate_spellings': 'algology',
                'language_origin': 'Greek',
                'example_sentence': 'Marine _____ focuses on the study of seaweed and ocean algae.'
            },
            'phylum': {
                'definition': 'A major taxonomic division of the animal or plant kingdom, ranking above class and below kingdom in biological classification.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FY-luhm (emphasis on first syllable)',
                'etymology': 'From Greek "phylon" meaning "tribe, race"',
                'memory_tips': 'Think "file-um" - filing organisms into groups',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Arthropods belong to the largest _____ in the animal kingdom.'
            },
            'phylumdifficulty': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "phylum" (taxonomic division) + "difficulty" (challenge).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "phylum" and "difficulty"',
                'alternate_spellings': 'phylum + difficulty (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'physical': {
                'definition': 'Relating to the body or material things; involving bodily contact or activity; existing in a material form that can be touched.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FIZ-i-kuhl (emphasis on first syllable)',
                'etymology': 'From Greek "physikos" meaning "natural, relating to nature"',
                'memory_tips': 'Think "fizz-ical" - things that fizz are physical and real',
                'alternate_spellings': 'bodily, material',
                'language_origin': 'Greek',
                'example_sentence': 'The doctor performed a _____ examination to check the patient\'s health.'
            },
            'physicalpunily': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "physical" (bodily) + "punily" (in a weak manner).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "physical" and "punily"',
                'alternate_spellings': 'physical + punily (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'physician': {
                'definition': 'A person qualified to practice medicine; a doctor who diagnoses and treats illnesses and injuries.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fi-ZISH-uhn (emphasis on second syllable)',
                'etymology': 'From Greek "physikos" meaning "natural" + "-ian" meaning "practitioner"',
                'memory_tips': 'Think "fizz-ician" - a magician who can fix your physical fizz',
                'alternate_spellings': 'doctor, medical doctor',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ prescribed medication to treat the patient\'s infection.'
            },
            'physicists': {
                'definition': 'Scientists who study physics; people who specialize in the science of matter, energy, and their interactions.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FIZ-uh-sists (emphasis on first syllable)',
                'etymology': 'From Greek "physikos" meaning "natural" + "-ist" meaning "specialist"',
                'memory_tips': 'Think "fizz-uh-cists" - scientists who study how things fizz and react',
                'alternate_spellings': 'physicist (singular)',
                'language_origin': 'Greek',
                'example_sentence': 'The team of _____ worked together to understand the behavior of subatomic particles.'
            },
            'phytophilous': {
                'definition': 'Having an affinity for or attraction to plants; describing organisms that prefer or depend on plant environments.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'fy-TOF-uh-lus (emphasis on second syllable)',
                'etymology': 'From Greek "phyton" meaning "plant" + "philos" meaning "loving"',
                'memory_tips': 'Think "fight-oh-fill-us" - we fight to fill ourselves with plant love',
                'alternate_spellings': 'plant-loving',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ insects were found exclusively in areas with dense vegetation.'
            },
            'pianola': {
                'definition': 'A type of player piano that automatically plays music using perforated paper rolls; a self-playing piano mechanism.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pee-uh-NOH-luh (emphasis on third syllable)',
                'etymology': 'Trademark name, from "piano" + diminutive suffix "-ola"',
                'memory_tips': 'Think "piano-la" - a little piano that plays by itself',
                'alternate_spellings': 'player piano',
                'language_origin': 'Modern trademark (Italian-influenced)',
                'example_sentence': 'The antique _____ entertained guests with its automatic melodies.'
            },
            'piatti': {
                'definition': 'Italian term for cymbals, especially orchestral cymbals used in classical music; also refers to plates or dishes in Italian.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'pee-AH-tee (emphasis on second syllable)',
                'etymology': 'From Italian "piatti" meaning "plates, cymbals"',
                'memory_tips': 'Think "pee-at-tea" - cymbals that crash when you pee at tea time',
                'alternate_spellings': 'cymbals, plates',
                'language_origin': 'Italian',
                'example_sentence': 'The orchestra\'s _____ crashed dramatically during the symphony\'s climax.'
            },
            'piccata': {
                'definition': 'An Italian cooking method where meat is sliced thin, sautéed, and served in a sauce of lemon, butter, and capers.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pi-KAH-tuh (emphasis on second syllable)',
                'etymology': 'From Italian "piccata", past participle of "piccare" meaning "to prick, season"',
                'memory_tips': 'Think "pick-at-a" - pick at a dish with lemon and capers',
                'alternate_spellings': '',
                'language_origin': 'Italian',
                'example_sentence': 'The chef prepared chicken _____ with a tangy lemon and caper sauce.'
            },
            'pick': {
                'definition': 'To select or choose from a group; to pluck or gather; a tool with a pointed end for breaking or digging.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'PIK (emphasis on syllable)',
                'etymology': 'From Middle English "pikken", possibly from Old English "pyccean"',
                'memory_tips': 'Think "pick" - like picking apples or picking a choice',
                'alternate_spellings': 'choose, select',
                'language_origin': 'Middle English',
                'example_sentence': 'Please _____ your favorite color from the palette.'
            },
            'picture': {
                'definition': 'A visual representation or image, especially a painting, drawing, or photograph; to imagine or visualize.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'PIK-cher (emphasis on first syllable)',
                'etymology': 'From Latin "pictura", from "pingere" meaning "to paint"',
                'memory_tips': 'Think "pick-ture" - you pick a moment and turn it into a picture',
                'alternate_spellings': 'image, photo',
                'language_origin': 'Latin',
                'example_sentence': 'The family hung a _____ of their vacation on the wall.'
            },
            'pictures': {
                'definition': 'Multiple visual representations or images; photographs, paintings, drawings, or other visual artworks.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'PIK-cherz (emphasis on first syllable)',
                'etymology': 'Plural of "picture", from Latin "pictura"',
                'memory_tips': 'Think "pick-tures" - picking multiple moments to capture',
                'alternate_spellings': 'images, photos',
                'language_origin': 'Latin',
                'example_sentence': 'She scrolled through hundreds of _____ on her phone.'
            },
            'piece': {
                'definition': 'A part or portion of something; an individual item or work of art; to put together or assemble.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'PEES (emphasis on syllable)',
                'etymology': 'From Old French "piece", from Vulgar Latin "pettia"',
                'memory_tips': 'Think "peace" - each piece brings peace to the whole puzzle',
                'alternate_spellings': 'part, portion',
                'language_origin': 'Old French',
                'example_sentence': 'She found the missing _____ of the jigsaw puzzle.'
            },
            'pieces': {
                'definition': 'Multiple parts or portions of something; individual items or components that form a whole.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'PEE-siz (emphasis on first syllable)',
                'etymology': 'Plural of "piece", from Old French "piece"',
                'memory_tips': 'Think "peace-iz" - peace is made of many pieces',
                'alternate_spellings': 'parts, portions',
                'language_origin': 'Old French',
                'example_sentence': 'The broken vase lay in _____ on the floor.'
            },
            'piecing': {
                'definition': 'The process of putting together parts or fragments; assembling components to form a whole.',
                'part_of_speech': 'verb (present participle), noun',
                'pronunciation_guide': 'PEES-ing (emphasis on first syllable)',
                'etymology': 'From "piece" + "-ing", from Old French "piece"',
                'memory_tips': 'Think "peace-ing" - bringing peace by putting pieces together',
                'alternate_spellings': 'assembling, putting together',
                'language_origin': 'Old French',
                'example_sentence': 'She spent hours _____ together the historical evidence.'
            },
            'piercing': {
                'definition': 'Sharp and penetrating in quality; making a hole through something; an opening made through body tissue for jewelry.',
                'part_of_speech': 'adjective, noun, verb',
                'pronunciation_guide': 'PEER-sing (emphasis on first syllable)',
                'etymology': 'From "pierce" + "-ing", from Old French "percier"',
                'memory_tips': 'Think "peer-sing" - peers singing with sharp, penetrating voices',
                'alternate_spellings': 'sharp, penetrating',
                'language_origin': 'Old French',
                'example_sentence': 'Her _____ blue eyes seemed to see right through him.'
            },
            'pierre': {
                'definition': 'French word meaning "stone" or "Peter"; also refers to a capital city (Pierre, South Dakota).',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'pee-AIR (emphasis on second syllable)',
                'etymology': 'From French "pierre" meaning "stone", from Latin "petra"',
                'memory_tips': 'Think "pee-air" - Peter is as solid as stone in the air',
                'alternate_spellings': 'Peter, stone',
                'language_origin': 'French',
                'example_sentence': '_____ is the capital city of South Dakota.'
            },
            'pierrot': {
                'definition': 'A traditional character from French pantomime, typically dressed in white with a white face and often portrayed as a sad clown.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pee-uh-ROH (emphasis on third syllable)',
                'etymology': 'From French "Pierrot", diminutive of "Pierre" (Peter)',
                'memory_tips': 'Think "peer-row" - peers in a row watching the sad white clown',
                'alternate_spellings': 'sad clown character',
                'language_origin': 'French',
                'example_sentence': 'The _____ performed a melancholy pantomime for the audience.'
            },
            'piety': {
                'definition': 'Reverence and devotion to religious beliefs and practices; dutiful respect and devotion to parents, family, or country.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PY-uh-tee (emphasis on first syllable)',
                'etymology': 'From Latin "pietas" meaning "dutifulness, devotion"',
                'memory_tips': 'Think "pie-tea" - serving pie and tea with devoted reverence',
                'alternate_spellings': 'devotion, reverence',
                'language_origin': 'Latin',
                'example_sentence': 'Her _____ was evident in her daily prayers and charitable works.'
            },
            'pigeon': {
                'definition': 'A medium-sized bird with a stout body, typically gray in color, commonly found in urban areas; a dove.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PIJ-uhn (emphasis on first syllable)',
                'etymology': 'From Old French "pijon", from Late Latin "pipio" meaning "young bird"',
                'memory_tips': 'Think "pid-gin" - a bird that speaks pidgin English',
                'alternate_spellings': 'dove',
                'language_origin': 'Old French',
                'example_sentence': 'The _____ perched on the window sill, cooing softly.'
            },
            'pigmentosa': {
                'definition': 'Relating to or characterized by abnormal pigmentation; often refers to retinitis pigmentosa, an eye condition.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'pig-men-TOH-suh (emphasis on third syllable)',
                'etymology': 'From Latin "pigmentum" meaning "pigment" + "-osa" meaning "full of"',
                'memory_tips': 'Think "pig-men-toe-sa" - pigs with pigmented toes',
                'alternate_spellings': 'pigmented',
                'language_origin': 'Latin',
                'example_sentence': 'Retinitis _____ is a genetic disorder affecting vision.'
            },
            'pigments': {
                'definition': 'Substances that give color to materials; natural or synthetic compounds that absorb certain wavelengths of light.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'PIG-muhnts (emphasis on first syllable)',
                'etymology': 'From Latin "pigmentum", from "pingere" meaning "to paint"',
                'memory_tips': 'Think "pig-ments" - pigs with colorful mental images',
                'alternate_spellings': 'pigment (singular), colorants',
                'language_origin': 'Latin',
                'example_sentence': 'The artist mixed various _____ to create the perfect shade of blue.'
            },
            'pigsty': {
                'definition': 'An enclosure where pigs are kept; a very dirty or messy place.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PIG-sty (emphasis on first syllable)',
                'etymology': 'From "pig" + "sty" (enclosure), from Old English "stig"',
                'memory_tips': 'Think "pig-sty" - where pigs stay and make it messy',
                'alternate_spellings': 'pigpen, mess',
                'language_origin': 'Old English',
                'example_sentence': 'His room was such a _____ that he couldn\'t find anything.'
            },
            'pikas': {
                'definition': 'Small, round-eared mammals related to rabbits, typically found in mountainous areas and known for their high-pitched calls.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'PEE-kuhz (emphasis on first syllable)',
                'etymology': 'From Tungusic languages, possibly from "pika" meaning "little chief hare"',
                'memory_tips': 'Think "peek-as" - small animals that peek as they hop around rocks',
                'alternate_spellings': 'pika (singular)',
                'language_origin': 'Tungusic',
                'example_sentence': 'The _____ collected plants and stored them in haypiles for winter.'
            },
            'pilaster': {
                'definition': 'A rectangular column that projects slightly from a wall, often used for decoration or structural support in architecture.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pi-LAS-tur (emphasis on second syllable)',
                'etymology': 'From French "pilastre", from Italian "pilastro", from Latin "pila" meaning "pillar"',
                'memory_tips': 'Think "pile-aster" - like a pillar but faster to build',
                'alternate_spellings': 'wall column',
                'language_origin': 'Latin via Italian and French',
                'example_sentence': 'The building\'s facade featured elegant _____ between the windows.'
            },
            'pilcrow': {
                'definition': 'A typographical symbol (¶) used to mark the beginning of a paragraph; also called a paragraph mark.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PIL-kroh (emphasis on first syllable)',
                'etymology': 'From Middle English "pylcrafte", possibly from "paragraph"',
                'memory_tips': 'Think "pill-crow" - a crow-shaped pill that marks paragraphs',
                'alternate_spellings': 'paragraph mark',
                'language_origin': 'Middle English',
                'example_sentence': 'The editor used a _____ to indicate where each new paragraph should begin.'
            },
            'pileus': {
                'definition': 'The cap or top part of a mushroom; the umbrella-shaped structure that contains the spores.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PIE-lee-us (emphasis on first syllable)',
                'etymology': 'From Latin "pileus" meaning "felt cap"',
                'memory_tips': 'Think "pile-us" - the pile of mushroom cap above us',
                'alternate_spellings': 'mushroom cap',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ of the mushroom was smooth and brown with white spots.'
            },
            'pilferer': {
                'definition': 'A person who steals small items or small amounts, typically in a sly or petty manner; a petty thief.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'PIL-fur-ur (emphasis on first syllable)',
                'etymology': 'From "pilfer" + "-er", from Old French "pelfrer" meaning "to plunder"',
                'memory_tips': 'Think "pill-ferer" - someone who steals pills and small things',
                'alternate_spellings': 'petty thief, pilferer',
                'language_origin': 'Old French',
                'example_sentence': 'The store installed cameras to catch the _____ who had been stealing candy.'
            },
            'pilgrimages': {
                'definition': 'Journeys to sacred places for religious or spiritual reasons; travels undertaken for personal growth or devotion.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'PIL-grim-ij-iz (emphasis on first syllable)',
                'etymology': 'From "pilgrim" + "-age", from Latin "peregrinus" meaning "foreigner"',
                'memory_tips': 'Think "pill-grim-ages" - grim ages requiring spiritual pills (journeys)',
                'alternate_spellings': 'pilgrimage (singular), religious journeys',
                'language_origin': 'Latin',
                'example_sentence': 'Many _____ to Santiago de Compostela follow ancient walking routes.'
            },
            'pillage': {
                'definition': 'To rob or plunder, especially during war; to steal goods from a place using violence.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'PIL-ij (emphasis on first syllable)',
                'etymology': 'From Old French "pillage", from "piller" meaning "to plunder"',
                'memory_tips': 'Think "pill-age" - taking pills from every age group',
                'alternate_spellings': 'plunder, loot',
                'language_origin': 'Old French',
                'example_sentence': 'The invading army would _____ the villages for supplies and treasures.'
            },
            'pillor': {
                'definition': '[POSSIBLE ERROR] This may be a misspelling of "pillar" (column) or refer to a specific term requiring clarification.',
                'part_of_speech': 'noun (uncertain)',
                'pronunciation_guide': 'PIL-ur (if meant as "pillar")',
                'etymology': 'Uncertain - possibly variant of "pillar" from Latin "pila"',
                'memory_tips': 'May be an error - check if this should be "pillar"',
                'alternate_spellings': 'pillar (?)',
                'language_origin': 'Uncertain',
                'example_sentence': '[NEEDS CLARIFICATION] The structure was supported by stone _____.'
            },
            'pillow': {
                'definition': 'A soft cushion used to support the head during sleep or rest; to rest one\'s head on something soft.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'PIL-oh (emphasis on first syllable)',
                'etymology': 'From Old English "pyle", from Latin "pulvinus" meaning "cushion"',
                'memory_tips': 'Think "pill-low" - a low place to rest your head like a soft pill',
                'alternate_spellings': 'cushion',
                'language_origin': 'Latin via Old English',
                'example_sentence': 'She fluffed her _____ before settling down to sleep.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_132_data:
            return batch_132_data[word_lower]
        
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
    
    def process_batch_132(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 132 with comprehensive Claude data"""
        words = []
        with open(input_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row['word']:  # Skip empty rows
                    continue
                    
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
    
    def save_batch_132_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 132 processed words to CSV"""
        
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
    """Process Batch 132 with comprehensive Claude data"""
    processor = Batch132Processor()
    input_csv = Path("output/batch_132_words.csv")
    output_csv = Path("output/batch_132_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 132 with comprehensive Claude data...")
    
    # Process all words in batch 132
    processed_words = processor.process_batch_132(input_csv)
    
    # Save results
    processor.save_batch_132_csv(processed_words, output_csv)
    
    logger.info(f"Batch 132 processing completed!")
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