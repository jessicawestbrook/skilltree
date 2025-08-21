#!/usr/bin/env python3
"""
Process Batch 135 of Spelling Bee Words with Comprehensive Claude Data
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
            'government', 'company', 'number', 'group', 'problem', 'fact', 'pick', 'picture', 'piece', 'phone', 'physical', 'pink', 'place', 'plan', 
            'plant', 'play', 'please', 'plus', 'pocket', 'poem', 'poetry', 'point', 'points', 'poke', 'pole', 'police', 'policy', 'polish', 'political', 'polo'
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
            'mega', 'micro', 'mini', 'multi', 'neo', 'pseudo', 'ultra', 'photo', 'phys', 'pla', 'poly'
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

class Batch135Processor:
    """Processes Batch 135 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 135 words"""
        
        # Comprehensive data for all 50 words in Batch 135
        batch_135_data = {
            'plus': {
                'definition': 'In addition to; a positive quality or advantage; the mathematical symbol for addition (+).',
                'part_of_speech': 'preposition, noun, adjective',
                'pronunciation_guide': 'PLUHZ (emphasis on syllable)',
                'etymology': 'From Latin "plus" meaning "more"',
                'memory_tips': 'Think "plus" - adding more to what you have',
                'alternate_spellings': 'addition, positive',
                'language_origin': 'Latin',
                'example_sentence': 'The job offer came with a salary _____ benefits package.'
            },
            'plush': {
                'definition': 'Having a rich, luxurious texture; covered with long, soft pile; luxuriously comfortable.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'PLUHSH (emphasis on syllable)',
                'etymology': 'From French "peluche", from Italian "peluzzo" meaning "hairy"',
                'memory_tips': 'Think "plush" - so soft it makes you blush with pleasure',
                'alternate_spellings': 'luxurious, soft',
                'language_origin': 'French via Italian',
                'example_sentence': 'The hotel room featured _____ carpeting and velvet curtains.'
            },
            'plutonomy': {
                'definition': 'An economy that is significantly influenced or driven by the wealthy; economic dominance by the wealthy.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ploo-TON-uh-mee (emphasis on second syllable)',
                'etymology': 'From Greek "ploutos" meaning "wealth" + "-nomy" meaning "management"',
                'memory_tips': 'Think "Pluto-nomy" - economy ruled by the wealth god Pluto',
                'alternate_spellings': 'wealth-driven economy',
                'language_origin': 'Greek',
                'example_sentence': 'Critics argued that the country had become a _____ where only the rich had real influence.'
            },
            'pneumatocyst': {
                'definition': 'A gas-filled bladder found in certain marine organisms, especially siphonophores, that provides buoyancy.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'noo-MAT-oh-sist (emphasis on second syllable)',
                'etymology': 'From Greek "pneuma" meaning "air, breath" + "kystis" meaning "bladder"',
                'memory_tips': 'Think "pneumatic-cyst" - an air-filled cyst for floating',
                'alternate_spellings': 'gas bladder, float',
                'language_origin': 'Greek',
                'example_sentence': 'The jellyfish\'s _____ allowed it to control its position in the water column.'
            },
            'poblano': {
                'definition': 'A mild to medium-hot chili pepper native to Mexico, often used in cooking when fresh or dried.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'poh-BLAH-noh (emphasis on second syllable)',
                'etymology': 'From Spanish "poblano", meaning "from Puebla" (a Mexican state)',
                'memory_tips': 'Think "pop-lano" - a pepper that pops with flavor from Puebla',
                'alternate_spellings': 'poblano pepper',
                'language_origin': 'Spanish',
                'example_sentence': 'The chef stuffed the _____ peppers with cheese and rice.'
            },
            'pochoir': {
                'definition': 'A stenciling technique used in printmaking and illustration, especially popular in early 20th-century France.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'poh-SHWAHR (emphasis on second syllable)',
                'etymology': 'From French "pochoir", from "poche" meaning "pocket" (referring to the stencil)',
                'memory_tips': 'Think "poach-oir" - poaching colors through a stencil',
                'alternate_spellings': 'stencil technique',
                'language_origin': 'French',
                'example_sentence': 'The art book featured beautiful _____ illustrations with vibrant hand-applied colors.'
            },
            'pocket': {
                'definition': 'A small pouch sewn into clothing for carrying items; a small isolated area or group.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'POK-it (emphasis on first syllable)',
                'etymology': 'From Old French "poquet", diminutive of "poque" meaning "pouch"',
                'memory_tips': 'Think "pock-it" - like a small pock (spot) where you put it',
                'alternate_spellings': 'pouch, compartment',
                'language_origin': 'Old French',
                'example_sentence': 'She kept her keys in the front _____ of her jacket.'
            },
            'pocus': {
                'definition': 'A nonsense word, often used in "hocus pocus" meaning trickery or deception; magical incantation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'POH-kus (emphasis on first syllable)',
                'etymology': 'From "hocus pocus", possibly pseudo-Latin used by conjurers',
                'memory_tips': 'Think "poke-us" - magic that pokes us with wonder',
                'alternate_spellings': 'magic word, nonsense',
                'language_origin': 'Pseudo-Latin',
                'example_sentence': 'The magician said "hocus _____" before making the rabbit disappear.'
            },
            'podagra': {
                'definition': 'Gout affecting the foot, especially the big toe; a painful inflammatory condition of the joints.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'poh-DAG-ruh (emphasis on second syllable)',
                'etymology': 'From Greek "podagra", from "pous" meaning "foot" + "agra" meaning "seizure"',
                'memory_tips': 'Think "pod-agra" - foot seizure that makes you angry (agra-vated)',
                'alternate_spellings': 'foot gout',
                'language_origin': 'Greek',
                'example_sentence': 'The king suffered from _____, making it painful to walk.'
            },
            'podcast': {
                'definition': 'A digital audio program available for download or streaming, typically part of a series on a particular topic.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'POD-kast (emphasis on first syllable)',
                'etymology': 'From "iPod" + "broadcast", coined in 2004',
                'memory_tips': 'Think "pod-cast" - casting your voice into a pod (device)',
                'alternate_spellings': 'audio show',
                'language_origin': 'Modern English (portmanteau)',
                'example_sentence': 'She listened to her favorite _____ during her morning commute.'
            },
            'podium': {
                'definition': 'A small platform on which a person stands to be seen by an audience; a lectern or raised platform.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'POH-dee-uhm (emphasis on first syllable)',
                'etymology': 'From Latin "podium", from Greek "podion" meaning "little foot"',
                'memory_tips': 'Think "pod-ium" - a pod where you stand with aplomb (confidence)',
                'alternate_spellings': 'platform, dais',
                'language_origin': 'Greek via Latin',
                'example_sentence': 'The speaker stepped up to the _____ to address the crowd.'
            },
            'podotheca': {
                'definition': 'The scaly covering of a bird\'s leg and foot; the protective sheath around the lower leg of birds.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'poh-doh-THEE-kuh (emphasis on third syllable)',
                'etymology': 'From Greek "pous" meaning "foot" + "theke" meaning "case, sheath"',
                'memory_tips': 'Think "pod-oh-theca" - a case for the bird\'s pod-like foot',
                'alternate_spellings': 'leg scales, foot covering',
                'language_origin': 'Greek',
                'example_sentence': 'The ornithologist examined the bird\'s _____ for identification purposes.'
            },
            'podsnappery': {
                'definition': 'Smug, narrow-minded complacency and self-satisfaction; pompous conventionalism.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'POD-snap-uh-ree (emphasis on first syllable)',
                'etymology': 'From Mr. Podsnap, a character in Charles Dickens\' "Our Mutual Friend"',
                'memory_tips': 'Think "pod-snappery" - snapping at others from your smug pod',
                'alternate_spellings': 'complacency, smugness',
                'language_origin': 'English (literary)',
                'example_sentence': 'His _____ made him dismiss any ideas that challenged his worldview.'
            },
            'podunk': {
                'definition': 'A small, unimportant town; any small, insignificant, or isolated place.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'POH-duhngk (emphasis on first syllable)',
                'etymology': 'From Podunk, a place name of Algonquian origin meaning "swampy place"',
                'memory_tips': 'Think "pod-unk" - a place so small it\'s like an unk (unknown) pod',
                'alternate_spellings': 'small town, backwater',
                'language_origin': 'Algonquian',
                'example_sentence': 'He grew up in a _____ town where everyone knew everyone else.'
            },
            'poem': {
                'definition': 'A piece of writing in verse, typically with rhythm, rhyme, and expressive language to convey emotions or ideas.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'POH-uhm (emphasis on first syllable)',
                'etymology': 'From Greek "poema", from "poiein" meaning "to make, create"',
                'memory_tips': 'Think "po-em" - like "pro" but with emotional creation',
                'alternate_spellings': 'verse, rhyme',
                'language_origin': 'Greek',
                'example_sentence': 'She wrote a beautiful _____ about the changing seasons.'
            },
            'poems': {
                'definition': 'Multiple pieces of writing in verse; a collection of poetic works.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'POH-uhmz (emphasis on first syllable)',
                'etymology': 'Plural of "poem", from Greek "poema"',
                'memory_tips': 'Think "po-ems" - multiple emotional creations',
                'alternate_spellings': 'verses, poetry collection',
                'language_origin': 'Greek',
                'example_sentence': 'The anthology contained _____ by poets from around the world.'
            },
            'poetry': {
                'definition': 'Literary work in verse; the art of writing poems; language with rhythmic and metaphorical qualities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'POH-uh-tree (emphasis on first syllable)',
                'etymology': 'From Greek "poietria", feminine of "poietes" meaning "maker, poet"',
                'memory_tips': 'Think "poet-tree" - a tree where poets grow their creative works',
                'alternate_spellings': 'verse, poetic literature',
                'language_origin': 'Greek',
                'example_sentence': 'She studied _____ in college and learned to appreciate its beauty.'
            },
            'point': {
                'definition': 'A particular spot, place, or position; the sharp end of something; a unit of scoring.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'POINT (emphasis on syllable)',
                'etymology': 'From Old French "point", from Latin "punctum" meaning "prick, point"',
                'memory_tips': 'Think "point" - pointing to a specific spot',
                'alternate_spellings': 'spot, tip, score',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'She made an important _____ during the meeting.'
            },
            'pointelle': {
                'definition': 'A knitting technique that creates small decorative holes in fabric; fabric made with this technique.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'poin-TEL (emphasis on second syllable)',
                'etymology': 'From French "pointelle", diminutive of "point" meaning "stitch"',
                'memory_tips': 'Think "point-elle" - she points to the small decorative holes',
                'alternate_spellings': 'openwork knit',
                'language_origin': 'French',
                'example_sentence': 'The sweater featured delicate _____ detailing around the neckline.'
            },
            'points': {
                'definition': 'Multiple particular spots or positions; sharp ends; units of scoring in games or systems.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'POINTS (emphasis on syllable)',
                'etymology': 'Plural of "point", from Latin "punctum"',
                'memory_tips': 'Think "points" - multiple sharp spots you can point to',
                'alternate_spellings': 'scores, tips, locations',
                'language_origin': 'Latin',
                'example_sentence': 'The team scored enough _____ to win the championship.'
            },
            'poisonous': {
                'definition': 'Containing or producing poison; harmful or destructive; venomous or toxic.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'POI-zuhn-us (emphasis on first syllable)',
                'etymology': 'From "poison" + "-ous", from Latin "potio" meaning "drink"',
                'memory_tips': 'Think "poison-ous" - full of poison, dangerous to us',
                'alternate_spellings': 'toxic, venomous',
                'language_origin': 'Latin',
                'example_sentence': 'The hiker learned to identify _____ plants to avoid accidental contact.'
            },
            'poke': {
                'definition': 'To push or prod with a finger or pointed object; to stir up or provoke.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'POHK (emphasis on syllable)',
                'etymology': 'From Middle English "poken", possibly from Old French "poquer"',
                'memory_tips': 'Think "poke" - like poking a fire or poking someone',
                'alternate_spellings': 'prod, jab, push',
                'language_origin': 'Middle English',
                'example_sentence': 'Don\'t _____ the sleeping bear with that stick.'
            },
            'pokery': {
                'definition': 'Something small, cramped, or confined; petty or trivial matters; cramped living conditions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'POH-kuh-ree (emphasis on first syllable)',
                'etymology': 'From "poke" meaning "bag, sack" + "-ery"',
                'memory_tips': 'Think "poke-ery" - a place where you poke around in cramped spaces',
                'alternate_spellings': 'cramped space, confinement',
                'language_origin': 'English',
                'example_sentence': 'The tiny apartment was nothing but _____ compared to their previous home.'
            },
            'pokerysobersides': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "pokery" (cramped space) + "sobersides" (serious person).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "pokery" and "sobersides"',
                'alternate_spellings': 'pokery + sobersides (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'pokus': {
                'definition': 'A variant or shortened form of "hocus pocus"; magical nonsense word; trickery.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'POH-kus (emphasis on first syllable)',
                'etymology': 'Variant of "pocus" from "hocus pocus", pseudo-Latin',
                'memory_tips': 'Think "poke-us" - magic that pokes us with wonder',
                'alternate_spellings': 'pocus, magic word',
                'language_origin': 'Pseudo-Latin',
                'example_sentence': 'The children laughed when the magician said "_____" and pulled out a flower.'
            },
            'polarized': {
                'definition': 'Divided into opposing groups or opinions; restricted to vibrations in one plane (physics).',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'POH-luh-ryzd (emphasis on first syllable)',
                'etymology': 'From "polarize", from "polar" + "-ize", from Greek "polos" meaning "axis"',
                'memory_tips': 'Think "polar-ized" - divided like the polar regions (North and South)',
                'alternate_spellings': 'divided, split',
                'language_origin': 'Greek',
                'example_sentence': 'The controversial issue _____ the community into opposing camps.'
            },
            'pole': {
                'definition': 'A long, straight piece of wood or metal; either end of an axis; a point of maximum difference.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'POHL (emphasis on syllable)',
                'etymology': 'From Latin "palus" meaning "stake"',
                'memory_tips': 'Think "pole" - like a tall pole you can see from far away',
                'alternate_spellings': 'post, rod, extremity',
                'language_origin': 'Latin',
                'example_sentence': 'The flag fluttered at the top of the tall _____.'
            },
            'polemic': {
                'definition': 'A strong verbal or written attack on someone or something; controversial argument or debate.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'puh-LEM-ik (emphasis on second syllable)',
                'etymology': 'From Greek "polemikos" meaning "warlike", from "polemos" meaning "war"',
                'memory_tips': 'Think "pole-emic" - a war-like argument that divides like poles',
                'alternate_spellings': 'controversy, argument',
                'language_origin': 'Greek',
                'example_sentence': 'The article was a fierce _____ against government corruption.'
            },
            'polenta': {
                'definition': 'A cornmeal dish from Northern Italy, served as a creamy porridge or allowed to set and then sliced.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'poh-LEN-tuh (emphasis on second syllable)',
                'etymology': 'From Italian "polenta", from Latin "polenta" meaning "peeled barley"',
                'memory_tips': 'Think "pole-lenta" - a pole made of ground corn that\'s lenta (slow) cooked',
                'alternate_spellings': 'cornmeal mush',
                'language_origin': 'Italian via Latin',
                'example_sentence': 'The restaurant served creamy _____ topped with mushroom ragout.'
            },
            'police': {
                'definition': 'The civil force responsible for maintaining public order and enforcing laws; to monitor or control.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'puh-LEES (emphasis on second syllable)',
                'etymology': 'From French "police", from Greek "politeia" meaning "government, administration"',
                'memory_tips': 'Think "po-lease" - they police to keep the peace',
                'alternate_spellings': 'law enforcement, patrol',
                'language_origin': 'Greek via French',
                'example_sentence': 'The _____ arrived quickly to investigate the reported break-in.'
            },
            'policy': {
                'definition': 'A course or principle of action adopted by a government, organization, or individual; an insurance contract.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'POL-uh-see (emphasis on first syllable)',
                'etymology': 'From Greek "politeia" meaning "government, administration"',
                'memory_tips': 'Think "polite-see" - polite guidelines you can see',
                'alternate_spellings': 'procedure, plan, insurance',
                'language_origin': 'Greek',
                'example_sentence': 'The company implemented a new _____ regarding remote work.'
            },
            'polish': {
                'definition': 'To make smooth and shiny by rubbing; to refine or perfect; a substance used for polishing.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'POL-ish (emphasis on first syllable)',
                'etymology': 'From Old French "poliss-", from Latin "polire" meaning "to polish"',
                'memory_tips': 'Think "polish" - making something so smooth it\'s almost abolished (of roughness)',
                'alternate_spellings': 'shine, refine, wax',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'She used silver _____ to make the antique spoons gleam.'
            },
            'politeia': {
                'definition': 'The ancient Greek concept of the ideal state or constitution; citizenship and government.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pol-uh-TY-uh (emphasis on third syllable)',
                'etymology': 'From ancient Greek "politeia" meaning "government, constitution, citizenship"',
                'memory_tips': 'Think "polite-eia" - a polite way to organize government',
                'alternate_spellings': 'constitution, state',
                'language_origin': 'Ancient Greek',
                'example_sentence': 'Plato\'s "Republic" discusses the ideal _____ and just governance.'
            },
            'political': {
                'definition': 'Relating to government, politics, or public affairs; motivated by considerations of status or power.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'puh-LIT-uh-kuhl (emphasis on second syllable)',
                'etymology': 'From Greek "politikos" meaning "of citizens or the state"',
                'memory_tips': 'Think "polite-ical" - being politely involved in government',
                'alternate_spellings': 'governmental, civic',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ debate focused on healthcare and education policies.'
            },
            'politick': {
                'definition': 'To engage in political activity or maneuvering; to act in a shrewd or calculating way.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'POL-uh-tik (emphasis on first syllable)',
                'etymology': 'From "politic" + archaic verb ending "-k"',
                'memory_tips': 'Think "polite-ick" - getting sick of polite political maneuvering',
                'alternate_spellings': 'scheme, maneuver',
                'language_origin': 'English',
                'example_sentence': 'The senators continued to _____ behind the scenes for votes.'
            },
            'politickpollutant': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "politick" (political maneuvering) + "pollutant" (contaminating substance).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "politick" and "pollutant"',
                'alternate_spellings': 'politick + pollutant (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'polloi': {
                'definition': 'The common people; the masses (usually in "hoi polloi" meaning "the many").',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'puh-LOI (emphasis on second syllable)',
                'etymology': 'From Greek "polloi" meaning "many", plural of "polys"',
                'memory_tips': 'Think "poll-oi" - the many people you poll for opinions',
                'alternate_spellings': 'masses, common people',
                'language_origin': 'Greek',
                'example_sentence': 'The aristocrat looked down upon the hoi _____ with disdain.'
            },
            'pollutant': {
                'definition': 'A substance that contaminates or makes impure, especially harmful chemicals released into the environment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'puh-LOO-tuhnt (emphasis on second syllable)',
                'etymology': 'From Latin "pollutus", past participle of "polluere" meaning "to soil, defile"',
                'memory_tips': 'Think "pollute-ant" - an ant that pollutes everything it touches',
                'alternate_spellings': 'contaminant, toxin',
                'language_origin': 'Latin',
                'example_sentence': 'The factory was fined for releasing _____ into the nearby river.'
            },
            'polo': {
                'definition': 'A sport played on horseback with mallets and a ball; a type of shirt with a collar and buttons.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'POH-loh (emphasis on first syllable)',
                'etymology': 'From Tibetan "pulu" meaning "ball"',
                'memory_tips': 'Think "polo" - like solo but with polo ponies',
                'alternate_spellings': 'horseback sport',
                'language_origin': 'Tibetan',
                'example_sentence': 'The _____ match was exciting to watch as riders galloped across the field.'
            },
            'polonium': {
                'definition': 'A highly radioactive chemical element discovered by Marie Curie, used in nuclear applications.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'puh-LOH-nee-uhm (emphasis on second syllable)',
                'etymology': 'Named after Poland, Marie Curie\'s homeland, from Latin "Polonia"',
                'memory_tips': 'Think "Poland-ium" - an element named after Poland',
                'alternate_spellings': 'Po (chemical symbol)',
                'language_origin': 'Modern Latin (from Poland)',
                'example_sentence': 'The scientist handled _____ with extreme caution due to its radioactivity.'
            },
            'poltroon': {
                'definition': 'A person who is utterly lacking in courage; a complete coward.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pol-TROON (emphasis on second syllable)',
                'etymology': 'From French "poltron", from Italian "poltrone" meaning "lazy person"',
                'memory_tips': 'Think "poll-troon" - a cartoon character too cowardly to face polls',
                'alternate_spellings': 'coward, craven',
                'language_origin': 'French via Italian',
                'example_sentence': 'The brave knight called his enemy a _____ for refusing to fight.'
            },
            'polyandry': {
                'definition': 'A form of marriage in which a woman has more than one husband at the same time.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pol-ee-AN-dree (emphasis on third syllable)',
                'etymology': 'From Greek "polys" meaning "many" + "andros" meaning "man, husband"',
                'memory_tips': 'Think "poly-andy" - Andy and many other husbands',
                'alternate_spellings': 'plural marriage',
                'language_origin': 'Greek',
                'example_sentence': 'Anthropologists studied cultures that practiced _____ as a social system.'
            },
            'polydactyly': {
                'definition': 'A condition in which a person or animal is born with more than the normal number of fingers or toes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pol-ee-DAK-tuh-lee (emphasis on third syllable)',
                'etymology': 'From Greek "polys" meaning "many" + "daktylos" meaning "finger"',
                'memory_tips': 'Think "poly-dactyl" - many fingers like a pterodactyl has many claws',
                'alternate_spellings': 'extra digits',
                'language_origin': 'Greek',
                'example_sentence': 'The baby was born with _____, having six fingers on each hand.'
            },
            'polyester': {
                'definition': 'A synthetic polymer used to make fabrics and other materials; clothing made from this material.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pol-ee-ES-tur (emphasis on third syllable)',
                'etymology': 'From "polymer" + "ester", modern chemical compound name',
                'memory_tips': 'Think "poly-ester" - many esters joined together',
                'alternate_spellings': 'synthetic fabric',
                'language_origin': 'Modern scientific English',
                'example_sentence': 'The _____ shirt was wrinkle-resistant and easy to care for.'
            },
            'polyesteranoint': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "polyester" (synthetic fabric) + "anoint" (to apply oil or consecrate).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "polyester" and "anoint"',
                'alternate_spellings': 'polyester + anoint (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'polygenous': {
                'definition': 'Having multiple origins or sources; arising from several different causes or factors.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'pol-uh-JEN-us (emphasis on second syllable)',
                'etymology': 'From Greek "polys" meaning "many" + "genos" meaning "origin, birth"',
                'memory_tips': 'Think "poly-generous" - generously having many origins',
                'alternate_spellings': 'multi-origin',
                'language_origin': 'Greek',
                'example_sentence': 'The disease was _____, with genetic, environmental, and lifestyle factors all contributing.'
            },
            'polyglot': {
                'definition': 'A person who knows and is able to use several languages; written in multiple languages.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'POL-ee-glot (emphasis on first syllable)',
                'etymology': 'From Greek "polyglottos", from "polys" meaning "many" + "glotta" meaning "tongue"',
                'memory_tips': 'Think "poly-glot" - a person who glots (speaks) in many tongues',
                'alternate_spellings': 'multilingual person',
                'language_origin': 'Greek',
                'example_sentence': 'As a _____, she could conduct business in five different languages.'
            },
            'polymerized': {
                'definition': 'Formed into a polymer; underwent chemical reaction where small molecules combine into larger chains.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'puh-LIM-uh-ryzd (emphasis on second syllable)',
                'etymology': 'From "polymer" + "-ized", from Greek "polys" meaning "many" + "meros" meaning "part"',
                'memory_tips': 'Think "poly-memorized" - many parts memorized and joined together',
                'alternate_spellings': 'chemically linked',
                'language_origin': 'Greek',
                'example_sentence': 'The plastic had _____ into long chains of molecules.'
            },
            'polypeptide': {
                'definition': 'A chain of amino acids linked together, forming the basic structure of proteins.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pol-ee-PEP-tyd (emphasis on third syllable)',
                'etymology': 'From Greek "polys" meaning "many" + "peptide" from "peptein" meaning "to digest"',
                'memory_tips': 'Think "poly-peptide" - many peptides linked like a chain',
                'alternate_spellings': 'protein chain',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ folded into a specific shape to become a functional protein.'
            },
            'polysemy': {
                'definition': 'The existence of multiple meanings for a single word; the linguistic phenomenon of having several related meanings.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'pol-uh-SEE-mee (emphasis on third syllable)',
                'etymology': 'From Greek "polys" meaning "many" + "sema" meaning "sign, meaning"',
                'memory_tips': 'Think "poly-see-me" - you can see me in many different meanings',
                'alternate_spellings': 'multiple meanings',
                'language_origin': 'Greek',
                'example_sentence': 'The word "bank" demonstrates _____ with meanings including financial institution and riverbank.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_135_data:
            return batch_135_data[word_lower]
        
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
    
    def process_batch_135(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 135 with comprehensive Claude data"""
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
    
    def save_batch_135_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 135 processed words to CSV"""
        
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
    """Process Batch 135 with comprehensive Claude data"""
    processor = Batch135Processor()
    input_csv = Path("output/batch_135_words.csv")
    output_csv = Path("output/batch_135_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 135 with comprehensive Claude data...")
    
    # Process all words in batch 135
    processed_words = processor.process_batch_135(input_csv)
    
    # Save results
    processor.save_batch_135_csv(processed_words, output_csv)
    
    logger.info(f"Batch 135 processing completed!")
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