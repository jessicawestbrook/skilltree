#!/usr/bin/env python3
"""
Process Batch 047 of Spelling Bee Words with Comprehensive Claude Data
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
            'government', 'company', 'number', 'group', 'problem', 'fact', 'data', 'deal', 'dear', 'death', 'debt', 'dark', 'dash', 'daughter'
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

class Batch047Processor:
    """Processes Batch 047 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 047 words"""
        
        # Comprehensive data for all 50 words in Batch 047
        batch_047_data = {
            'darjeelingrecusancy': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "darjeeling" (a type of tea) + "recusancy" (refusal to accept religious authority).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "darjeeling" and "recusancy"',
                'alternate_spellings': 'darjeeling + recusancy (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'dark': {
                'definition': 'Having little or no light; of a deep or somber color; hidden or mysterious; evil or sinister.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'DAHRK (emphasis on first syllable)',
                'etymology': 'From Old English "deorc" meaning "dark, gloomy"',
                'memory_tips': 'Think "D-ark" - the letter D looks like darkness',
                'alternate_spellings': 'murky, dim',
                'language_origin': 'Old English',
                'example_sentence': 'The _____ forest was difficult to navigate without a flashlight.'
            },
            'darmstadtium': {
                'definition': 'A synthetic chemical element with symbol Ds and atomic number 110; a very heavy, radioactive metal.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dahrm-SHTAHT-ee-uhm (emphasis on second syllable)',
                'etymology': 'Named after Darmstadt, Germany, where it was first synthesized',
                'memory_tips': 'Think "Darmstadt-ium" - the element from Darmstadt',
                'alternate_spellings': 'element 110',
                'language_origin': 'German (place name)',
                'example_sentence': 'The scientists created _____ in their particle accelerator laboratory.'
            },
            'darnel': {
                'definition': 'A type of poisonous grass that resembles wheat; a weed that grows among grain crops.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DAHR-nuhl (emphasis on first syllable)',
                'etymology': 'From Old French "darnelle", possibly from a Celtic language',
                'memory_tips': 'Think "darn-ell" - darn that weed that looks like grain',
                'alternate_spellings': 'tare, ryegrass',
                'language_origin': 'Celtic via Old French',
                'example_sentence': 'The farmer had to remove the _____ from his wheat field.'
            },
            'darted': {
                'definition': 'Moved quickly and suddenly in a particular direction; threw a dart or pointed object.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'DAHR-tid (emphasis on first syllable)',
                'etymology': 'From "dart" + "-ed", where "dart" comes from Old French "dart"',
                'memory_tips': 'Think "dart-ed" - moved like a thrown dart',
                'alternate_spellings': 'rushed, shot',
                'language_origin': 'Old French',
                'example_sentence': 'The rabbit _____ across the field when it saw the fox.'
            },
            'darts': {
                'definition': 'A game played by throwing small pointed missiles at a circular target; the missiles themselves.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'DAHRTS (emphasis on first syllable)',
                'etymology': 'From Old French "dart" meaning "spear, javelin"',
                'memory_tips': 'Think "darts" - sharp points that dart through the air',
                'alternate_spellings': 'arrows, projectiles',
                'language_origin': 'Old French',
                'example_sentence': 'The pub had a _____ board where customers could play games.'
            },
            'darwinism': {
                'definition': 'The theory of evolution by natural selection, as proposed by Charles Darwin.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DAHR-wi-nizm (emphasis on first syllable)',
                'etymology': 'Named after Charles Darwin + "-ism"',
                'memory_tips': 'Think "Darwin-ism" - the beliefs and theories of Darwin',
                'alternate_spellings': 'evolutionary theory',
                'language_origin': 'English (proper name)',
                'example_sentence': 'The biology class studied _____ and natural selection.'
            },
            'dash': {
                'definition': 'To run quickly; to strike or throw with force; a small amount; a punctuation mark.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'DASH (emphasis on first syllable)',
                'etymology': 'From Middle English, possibly imitative of the sound of striking',
                'memory_tips': 'Think of the sound "dash" - quick movement or striking',
                'alternate_spellings': 'rush, hurry',
                'language_origin': 'Middle English',
                'example_sentence': 'She had to _____ to catch the departing train.'
            },
            'dashiki': {
                'definition': 'A colorful traditional African shirt, typically worn by men, with elaborate patterns and designs.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dah-SHEE-kee (emphasis on second syllable)',
                'etymology': 'From Yoruba "danshiki" or "dàǹṣíkí"',
                'memory_tips': 'Think "dash-iki" - a shirt with dashing African patterns',
                'alternate_spellings': 'African shirt',
                'language_origin': 'Yoruba (West African)',
                'example_sentence': 'He wore a bright _____ to celebrate African Heritage Day.'
            },
            'data': {
                'definition': 'Facts, figures, and information, especially when examined and used to make decisions; computer information.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DAY-tah or DAT-ah (emphasis on first syllable)',
                'etymology': 'From Latin "data", plural of "datum" meaning "something given"',
                'memory_tips': 'Think "date-a" - dating facts and information',
                'alternate_spellings': 'information, facts',
                'language_origin': 'Latin',
                'example_sentence': 'The scientists collected _____ from their experiments.'
            },
            'daubster': {
                'definition': 'A poor or unskilled painter; someone who daubs paint clumsily rather than creating art.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DAWB-ster (emphasis on first syllable)',
                'etymology': 'From "daub" (to smear paint) + "-ster" (agent suffix)',
                'memory_tips': 'Think "daub-ster" - someone who daubs paint messily',
                'alternate_spellings': 'poor painter, amateur artist',
                'language_origin': 'English compound',
                'example_sentence': 'The art critic dismissed him as a mere _____ rather than a true artist.'
            },
            'daughter': {
                'definition': 'A female offspring; a woman or girl in relation to her parents.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DAW-ter (emphasis on first syllable)',
                'etymology': 'From Old English "dohtor", related to Germanic roots',
                'memory_tips': 'Think "daw-ter" - sounds like "water" but starts with "d"',
                'alternate_spellings': 'female child',
                'language_origin': 'Old English, Germanic',
                'example_sentence': 'The proud father walked his _____ down the aisle.'
            },
            'dauntlessly': {
                'definition': 'In a fearless and determined manner; showing courage and persistence despite difficulties.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'DAWNT-lis-lee (emphasis on first syllable)',
                'etymology': 'From "dauntless" (fearless) + "-ly", where "daunt" comes from Old French',
                'memory_tips': 'Think "daunt-less-ly" - acting without being daunted',
                'alternate_spellings': 'fearlessly, boldly',
                'language_origin': 'Old French',
                'example_sentence': 'The explorer _____ continued through the dangerous terrain.'
            },
            'davenport': {
                'definition': 'A large sofa or couch; a type of writing desk with drawers and compartments.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DAV-uhn-pawrt (emphasis on first syllable)',
                'etymology': 'Named after Captain Davenport, who first commissioned this style of furniture',
                'memory_tips': 'Think "Dave-n-port" - Dave\'s furniture at the port',
                'alternate_spellings': 'sofa, couch',
                'language_origin': 'English (proper name)',
                'example_sentence': 'The antique _____ was the centerpiece of the living room.'
            },
            'dawdle': {
                'definition': 'To waste time; to move slowly and aimlessly; to delay unnecessarily.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'DAW-duhl (emphasis on first syllable)',
                'etymology': 'Of uncertain origin, possibly related to "daddle" (to walk unsteadily)',
                'memory_tips': 'Think "dawdle" rhymes with "waddle" - moving slowly',
                'alternate_spellings': 'delay, procrastinate',
                'language_origin': 'Unknown origin',
                'example_sentence': 'Don\'t _____ on your way to school or you\'ll be late.'
            },
            'dazzle': {
                'definition': 'To blind temporarily with bright light; to impress deeply; to amaze or astonish.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'DAZ-uhl (emphasis on first syllable)',
                'etymology': 'From Middle English "dasen" meaning "to daze"',
                'memory_tips': 'Think "daze-le" - to put someone in a daze with brightness',
                'alternate_spellings': 'amaze, blind',
                'language_origin': 'Middle English',
                'example_sentence': 'The diamond necklace would _____ everyone at the gala.'
            },
            'deadpan': {
                'definition': 'Having or showing no emotion; delivered in an expressionless manner.',
                'part_of_speech': 'adjective, adverb, noun',
                'pronunciation_guide': 'DED-pan (emphasis on first syllable)',
                'etymology': 'From "dead" + "pan" (face), meaning a face without expression',
                'memory_tips': 'Think "dead-pan" - a face as lifeless as a dead pan',
                'alternate_spellings': 'expressionless, stoic',
                'language_origin': 'English compound',
                'example_sentence': 'The comedian delivered his jokes with perfect _____ timing.'
            },
            'deal': {
                'definition': 'To distribute; to trade or conduct business; an agreement or bargain; a large amount.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'DEEL (emphasis on first syllable)',
                'etymology': 'From Old English "dǣlan" meaning "to divide, share"',
                'memory_tips': 'Think "deal" - dividing up cards or making agreements',
                'alternate_spellings': 'bargain, agreement',
                'language_origin': 'Old English',
                'example_sentence': 'The business partners shook hands to seal the _____.'
            },
            'dean': {
                'definition': 'A senior official in a college or university; the head of a faculty or academic department.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DEEN (emphasis on first syllable)',
                'etymology': 'From Old French "deien", from Latin "decanus" meaning "chief of ten"',
                'memory_tips': 'Think "dean" rhymes with "seen" - the authority figure who is seen',
                'alternate_spellings': 'academic head, administrator',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The _____ of students addressed the graduation ceremony.'
            },
            'dear': {
                'definition': 'Much loved; precious; expensive; used as a term of endearment.',
                'part_of_speech': 'adjective, noun, interjection',
                'pronunciation_guide': 'DEER (emphasis on first syllable)',
                'etymology': 'From Old English "deore" meaning "precious, valuable"',
                'memory_tips': 'Think "dear" like a deer - precious and beloved',
                'alternate_spellings': 'beloved, precious',
                'language_origin': 'Old English',
                'example_sentence': 'The grandmother held her _____ grandchild close.'
            },
            'death': {
                'definition': 'The permanent ending of all life functions; the state of being dead; the end of something.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DETH (emphasis on first syllable)',
                'etymology': 'From Old English "deað", related to "dead"',
                'memory_tips': 'Think "death" - the final breath',
                'alternate_spellings': 'demise, end',
                'language_origin': 'Old English',
                'example_sentence': 'The _____ of the old oak tree saddened the entire neighborhood.'
            },
            'deathin': {
                'definition': '[INCOMPLETE/CORRUPTED WORD] This appears to be an incomplete or corrupted word, possibly a data extraction error.',
                'part_of_speech': 'error - incomplete word',
                'pronunciation_guide': '[PRONUNCIATION ERROR - INCOMPLETE WORD]',
                'etymology': '[ETYMOLOGY ERROR - INCOMPLETE WORD]',
                'memory_tips': 'This appears to be a data error - possibly incomplete extraction',
                'alternate_spellings': 'ERROR - incomplete word',
                'language_origin': 'ERROR - incomplete word',
                'example_sentence': '[ERROR - This incomplete word should not appear in spelling bee materials]'
            },
            'debilitate': {
                'definition': 'To make weak or feeble; to impair the strength or energy of someone or something.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-BIL-uh-tayt (emphasis on second syllable)',
                'etymology': 'From Latin "debilitatus", past participle of "debilitare" meaning "to weaken"',
                'memory_tips': 'Think "de-bil-itate" - to remove (de) ability (bil)',
                'alternate_spellings': 'weaken, enfeeble',
                'language_origin': 'Latin',
                'example_sentence': 'The long illness would _____ his immune system.'
            },
            'debit': {
                'definition': 'An entry recording money owed or withdrawn from an account; to remove money from an account.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DEB-it (emphasis on first syllable)',
                'etymology': 'From Latin "debitum" meaning "debt, what is owed"',
                'memory_tips': 'Think "debt-it" - it creates debt when money is withdrawn',
                'alternate_spellings': 'withdrawal, charge',
                'language_origin': 'Latin',
                'example_sentence': 'The bank will _____ your account for the monthly fee.'
            },
            'debita': {
                'definition': 'Latin plural of "debitum" meaning debts or things owed; used in legal or financial contexts.',
                'part_of_speech': 'noun (Latin plural)',
                'pronunciation_guide': 'DEB-ih-tah (emphasis on first syllable)',
                'etymology': 'From Latin "debita", plural of "debitum" meaning "debt"',
                'memory_tips': 'Think "debt-a" - multiple debts in Latin',
                'alternate_spellings': 'debts (English)',
                'language_origin': 'Latin',
                'example_sentence': 'The legal document listed all the _____ owed by the estate.'
            },
            'debitum': {
                'definition': 'Latin term meaning debt or obligation; what is owed; used in legal and financial terminology.',
                'part_of_speech': 'noun (Latin)',
                'pronunciation_guide': 'DEB-ih-tuhm (emphasis on first syllable)',
                'etymology': 'From Latin "debitum", past participle of "debere" meaning "to owe"',
                'memory_tips': 'Think "debt-um" - the Latin word for debt',
                'alternate_spellings': 'debt (English)',
                'language_origin': 'Latin',
                'example_sentence': 'The contract specified the _____ to be paid within thirty days.'
            },
            'debris': {
                'definition': 'Scattered fragments or remains; rubble from something destroyed; scattered waste material.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'duh-BREE (emphasis on second syllable)',
                'etymology': 'From French "débris", from "débriser" meaning "to break apart"',
                'memory_tips': 'Think "de-bris" - broken pieces (bris means to break)',
                'alternate_spellings': 'rubble, wreckage',
                'language_origin': 'French',
                'example_sentence': 'The tornado left _____ scattered across the entire neighborhood.'
            },
            'debt': {
                'definition': 'Money owed to another person or organization; an obligation or liability.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DET (emphasis on first syllable, silent "b")',
                'etymology': 'From Old French "dete", from Latin "debitum" meaning "thing owed"',
                'memory_tips': 'Remember the silent "b" - "debt" sounds like "det"',
                'alternate_spellings': 'obligation, liability',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'She worked hard to pay off her student loan _____.'
            },
            'debunk': {
                'definition': 'To expose the falseness or hollowness of something; to discredit or disprove.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-BUHNGK (emphasis on second syllable)',
                'etymology': 'From "de-" (reverse) + "bunk" (nonsense), coined in the 1920s',
                'memory_tips': 'Think "de-bunk" - to remove the bunk (nonsense)',
                'alternate_spellings': 'disprove, discredit',
                'language_origin': 'Modern English compound',
                'example_sentence': 'The scientist worked to _____ the popular myth.'
            },
            'debutante': {
                'definition': 'A young woman making her formal entrance into society; a young woman having her debut.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DEB-yoo-tahnt (emphasis on first syllable)',
                'etymology': 'From French "débutante", feminine of "débutant" meaning "beginner"',
                'memory_tips': 'Think "debut-ante" - a young woman (ante means woman) making her debut',
                'alternate_spellings': 'deb',
                'language_origin': 'French',
                'example_sentence': 'The _____ wore a beautiful white gown to the cotillion ball.'
            },
            'decade': {
                'definition': 'A period of ten years; any group or series of ten.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DEK-ayd (emphasis on first syllable)',
                'etymology': 'From Latin "decas", from Greek "dekas" meaning "group of ten"',
                'memory_tips': 'Think "deca-de" - "deca" means ten',
                'alternate_spellings': 'ten-year period',
                'language_origin': 'Greek via Latin',
                'example_sentence': 'The 1980s was a _____ known for distinctive music and fashion.'
            },
            'decades': {
                'definition': 'Plural of decade; multiple periods of ten years.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'DEK-aydz (emphasis on first syllable)',
                'etymology': 'Plural of "decade", from Greek "dekas" meaning "group of ten"',
                'memory_tips': 'Think "deca-des" - multiple groups of ten years',
                'alternate_spellings': 'ten-year periods',
                'language_origin': 'Greek via Latin',
                'example_sentence': 'It took _____ for the forest to recover from the fire.'
            },
            'decastich': {
                'definition': 'A poem or stanza consisting of ten lines; a literary composition of ten verses.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DEK-uh-stik (emphasis on first syllable)',
                'etymology': 'From Greek "deka" (ten) + "stichos" (line, verse)',
                'memory_tips': 'Think "deca-stich" - ten (deca) lines (stich) of poetry',
                'alternate_spellings': 'ten-line poem',
                'language_origin': 'Greek',
                'example_sentence': 'The poet composed a beautiful _____ for the anniversary celebration.'
            },
            'deceitful': {
                'definition': 'Dishonest and fraudulent; intended to deceive; characterized by deception.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dih-SEET-fuhl (emphasis on second syllable)',
                'etymology': 'From "deceit" (from Latin "deceptus") + "-ful" (full of)',
                'memory_tips': 'Think "deceit-ful" - full of deceit',
                'alternate_spellings': 'dishonest, fraudulent',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ salesman misled customers about the product\'s quality.'
            },
            'deceitfulcinderella': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "deceitful" (dishonest) + "cinderella" (fairy tale character).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "deceitful" and "cinderella"',
                'alternate_spellings': 'deceitful + cinderella (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'deceleron': {
                'definition': 'An aircraft control surface that functions as both an aileron and a speed brake; used to reduce speed.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dee-SEL-uh-ron (emphasis on second syllable)',
                'etymology': 'From "decelerate" + "aileron" (aircraft control surface)',
                'memory_tips': 'Think "decel-eron" - an aileron that decelerates the aircraft',
                'alternate_spellings': 'speed brake',
                'language_origin': 'Modern English compound',
                'example_sentence': 'The pilot deployed the _____ to slow the aircraft for landing.'
            },
            'december': {
                'definition': 'The twelfth and final month of the year in the Gregorian calendar.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-SEM-ber (emphasis on second syllable)',
                'etymology': 'From Latin "december", from "decem" meaning "ten" (originally the 10th month)',
                'memory_tips': 'Think "decem-ber" - originally the tenth (decem) month',
                'alternate_spellings': 'Dec.',
                'language_origin': 'Latin',
                'example_sentence': 'The family always gathered for the holidays in _____.'
            },
            'decennial': {
                'definition': 'Occurring every ten years; relating to a ten-year period; lasting for ten years.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'dih-SEN-ee-uhl (emphasis on second syllable)',
                'etymology': 'From Latin "decennium", from "decem" (ten) + "annus" (year)',
                'memory_tips': 'Think "decem-nial" - ten (decem) years (annual)',
                'alternate_spellings': 'ten-year, decadal',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ census provides important demographic information.'
            },
            'deceptively': {
                'definition': 'In a way that gives a false or misleading impression; contrary to appearance.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'dih-SEP-tiv-lee (emphasis on second syllable)',
                'etymology': 'From "deceptive" (from Latin "deceptus") + "-ly"',
                'memory_tips': 'Think "deception-ly" - in a manner involving deception',
                'alternate_spellings': 'misleadingly',
                'language_origin': 'Latin',
                'example_sentence': 'The task looked _____ simple but was actually quite complex.'
            },
            'dechlorinate': {
                'definition': 'To remove chlorine from water or other substances; to eliminate chlorine compounds.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dee-KLAWR-uh-nayt (emphasis on second syllable)',
                'etymology': 'From "de-" (remove) + "chlorinate" (add chlorine)',
                'memory_tips': 'Think "de-chlorinate" - to remove (de) chlorine',
                'alternate_spellings': 'remove chlorine',
                'language_origin': 'Modern English compound',
                'example_sentence': 'The water treatment plant will _____ the tap water before distribution.'
            },
            'decibels': {
                'definition': 'Units of measurement for the intensity of sound; a logarithmic scale for sound levels.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'DES-uh-belz (emphasis on first syllable)',
                'etymology': 'Named after Alexander Graham Bell + "deci-" (one-tenth)',
                'memory_tips': 'Think "deci-bells" - one-tenth of a bell unit of sound',
                'alternate_spellings': 'dB',
                'language_origin': 'Named after Alexander Graham Bell',
                'example_sentence': 'The concert reached dangerous levels of over 120 _____.'
            },
            'decide': {
                'definition': 'To make a choice or reach a conclusion; to settle a question or dispute.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-SAHYD (emphasis on second syllable)',
                'etymology': 'From Latin "decidere", from "de-" (off) + "caedere" (to cut)',
                'memory_tips': 'Think "de-cide" - to cut (cide) away options',
                'alternate_spellings': 'choose, determine',
                'language_origin': 'Latin',
                'example_sentence': 'It\'s time to _____ which college to attend.'
            },
            'decided': {
                'definition': 'Having made a firm decision; clear and definite; determined.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'dih-SAHY-did (emphasis on second syllable)',
                'etymology': 'Past tense of "decide", from Latin "decidere"',
                'memory_tips': 'Think "de-cided" - already cut away the other options',
                'alternate_spellings': 'determined, resolved',
                'language_origin': 'Latin',
                'example_sentence': 'She had a _____ advantage in the competition.'
            },
            'deciduous': {
                'definition': 'Shedding leaves annually; falling off at maturity; temporary rather than permanent.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dih-SID-yoo-uhs (emphasis on second syllable)',
                'etymology': 'From Latin "deciduus", from "decidere" meaning "to fall off"',
                'memory_tips': 'Think "de-cide-uous" - trees that decide to drop their leaves',
                'alternate_spellings': 'leaf-shedding',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ trees created a colorful carpet of fallen leaves.'
            },
            'decimal': {
                'definition': 'Relating to or based on the number ten; expressed in the scale of tens.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'DES-uh-muhl (emphasis on first syllable)',
                'etymology': 'From Latin "decimalis", from "decimus" meaning "tenth"',
                'memory_tips': 'Think "deci-mal" - relating to tenths (deci)',
                'alternate_spellings': 'base-ten',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ system uses ten as its base number.'
            },
            'decimation': {
                'definition': 'The killing of a large proportion of a group; severe reduction in numbers; widespread destruction.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'des-uh-MAY-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "decimatio", originally meaning killing every tenth soldier',
                'memory_tips': 'Think "decim-ation" - originally killing every tenth (decim) person',
                'alternate_spellings': 'destruction, slaughter',
                'language_origin': 'Latin',
                'example_sentence': 'The disease caused the _____ of the bird population.'
            },
            'decision': {
                'definition': 'A conclusion or resolution reached after consideration; the action of deciding.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-SIZH-uhn (emphasis on second syllable)',
                'etymology': 'From Latin "decisio", from "decidere" meaning "to decide"',
                'memory_tips': 'Think "de-cision" - the result of cutting (cision) away options',
                'alternate_spellings': 'choice, determination',
                'language_origin': 'Latin',
                'example_sentence': 'The committee reached a unanimous _____ on the proposal.'
            },
            'decisions': {
                'definition': 'Plural of decision; multiple conclusions or choices made after consideration.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'dih-SIZH-uhnz (emphasis on second syllable)',
                'etymology': 'Plural of "decision", from Latin "decisio"',
                'memory_tips': 'Think "de-cisions" - multiple choices that cut away options',
                'alternate_spellings': 'choices, determinations',
                'language_origin': 'Latin',
                'example_sentence': 'The manager had to make several important _____ today.'
            },
            'declamatory': {
                'definition': 'Characterized by rhetorical speech; having the style of formal public speaking; pompous in expression.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dih-KLAM-uh-tawr-ee (emphasis on second syllable)',
                'etymology': 'From Latin "declamatorius", from "declamare" meaning "to speak rhetorically"',
                'memory_tips': 'Think "de-claim-atory" - claiming something in a dramatic way',
                'alternate_spellings': 'rhetorical, oratorical',
                'language_origin': 'Latin',
                'example_sentence': 'The politician\'s _____ speech stirred the crowd\'s emotions.'
            },
            'declaration': {
                'definition': 'A formal or explicit statement; an announcement or proclamation; a document stating facts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dek-luh-RAY-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "declaratio", from "declarare" meaning "to make clear"',
                'memory_tips': 'Think "de-clare-ation" - the act of making something clear',
                'alternate_spellings': 'statement, proclamation',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ of Independence was signed in 1776.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_047_data:
            return batch_047_data[word_lower]
        
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
    
    def process_batch_047(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 047 with comprehensive Claude data"""
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
    
    def save_batch_047_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 047 processed words to CSV"""
        
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
    """Process Batch 047 with comprehensive Claude data"""
    processor = Batch047Processor()
    input_csv = Path("output/batch_047_words.csv")
    output_csv = Path("output/batch_047_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 047 with comprehensive Claude data...")
    
    # Process all words in batch 047
    processed_words = processor.process_batch_047(input_csv)
    
    # Save results
    processor.save_batch_047_csv(processed_words, output_csv)
    
    logger.info(f"Batch 047 processing completed!")
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