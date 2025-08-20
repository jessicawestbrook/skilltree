#!/usr/bin/env python3
"""
Process Batch 002 of Spelling Bee Words with Comprehensive Claude Data
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

class Batch002Processor:
    """Processes Batch 002 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 002 words"""
        
        # Comprehensive data for all 50 words in Batch 002
        batch_002_data = {
            'acadians': {
                'definition': 'People from Acadia, a historical region in eastern Canada and Maine; French settlers and their descendants who established communities in the Maritime provinces.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'uh-KAY-dee-unz (emphasis on second syllable)',
                'etymology': 'From "Acadia", derived from Greek "Arcadia" meaning pastoral paradise, applied to the region by early explorers',
                'memory_tips': 'Think "a-cadians" - people from Acadia, the peaceful land',
                'alternate_spellings': 'Acadian (singular)',
                'language_origin': 'Greek via French',
                'example_sentence': 'The _____ maintained their French culture despite being expelled from their homeland.'
            },
            'accelerates': {
                'definition': 'Increases in speed, rate, or pace; moves faster or causes something to move faster; hastens the progress of an action or process.',
                'part_of_speech': 'verb (third person singular)',
                'pronunciation_guide': 'ak-SEL-uh-rayts (emphasis on second syllable)',
                'etymology': 'From Latin "acceleratus", from "accelerare" meaning "to quicken", from "ad" (to) + "celer" (swift)',
                'memory_tips': 'Think "ac-celery-ates" - celery accelerates your health when you eat it',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The car _____ rapidly as it merges onto the highway.'
            },
            'accent': {
                'definition': 'A distinctive way of pronouncing a language; emphasis placed on a syllable; a mark or symbol indicating stress or pronunciation.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'AK-sent (emphasis on first syllable)',
                'etymology': 'From Latin "accentus", from "ad" (to) + "cantus" (singing)',
                'memory_tips': 'Think "ac-cent" - adding a cent of emphasis to your speech',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Her British _____ made her speech sound elegant and refined.'
            },
            'accentuate': {
                'definition': 'To emphasize or make more noticeable; to stress or highlight particular features; to intensify or strengthen.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ak-SEN-choo-ayt (emphasis on second syllable)',
                'etymology': 'From Latin "accentuatus", past participle of "accentuare" meaning "to accent"',
                'memory_tips': 'Think "accent-you-ate" - you ate the accent to make it stronger',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The bright lighting will _____ the architectural details of the building.'
            },
            'accept': {
                'definition': 'To receive willingly; to agree to or approve of; to acknowledge as true or valid; to endure without protest.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ak-SEPT (emphasis on second syllable)',
                'etymology': 'From Latin "acceptare", frequentative of "accipere" meaning "to take or receive"',
                'memory_tips': 'Think "ac-cept" - you accept the concept',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She decided to _____ the job offer after careful consideration.'
            },
            'acceptable': {
                'definition': 'Satisfactory; meeting minimum standards; adequate or tolerable; capable of being accepted.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ak-SEP-tuh-buhl (emphasis on second syllable)',
                'etymology': 'From Latin "acceptabilis", from "acceptare" meaning "to accept"',
                'memory_tips': 'Think "accept-able" - able to be accepted',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The quality of the work was _____ but not exceptional.'
            },
            'acceptance': {
                'definition': 'The action of accepting; agreement to receive or undertake something; approval or recognition; willingness to tolerate a situation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ak-SEP-tunss (emphasis on second syllable)',
                'etymology': 'From Latin "acceptantia", from "acceptare" meaning "to accept"',
                'memory_tips': 'Think "accept-ance" - the dance of accepting something',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Her _____ letter from the university arrived in the mail yesterday.'
            },
            'accident': {
                'definition': 'An unexpected and unpleasant event, typically resulting in damage or injury; something happening by chance without apparent cause.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AK-si-duhnt (emphasis on first syllable)',
                'etymology': 'From Latin "accidens", present participle of "accidere" meaning "to fall upon, happen"',
                'memory_tips': 'Think "ac-cident" - when you accidentally dent something',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The traffic _____ caused delays on the highway for several hours.'
            },
            'acclaim': {
                'definition': 'Public praise and approval; enthusiastic recognition for achievement; to praise or applaud publicly.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'uh-KLAYM (emphasis on second syllable)',
                'etymology': 'From Latin "acclamare", from "ad" (to) + "clamare" (to shout)',
                'memory_tips': 'Think "ac-claim" - claiming recognition with a shout',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The novel received critical _____ for its innovative storytelling.'
            },
            'acclimate': {
                'definition': 'To adjust or adapt to a new climate, environment, or situation; to become accustomed to different conditions.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'AK-li-mayt (emphasis on first syllable)',
                'etymology': 'From "ac-" (to) + "climate", meaning to adapt to a climate',
                'memory_tips': 'Think "ac-climate" - getting used to the climate',
                'alternate_spellings': 'acclimatize',
                'language_origin': 'Modern English (French influence)',
                'example_sentence': 'It took weeks for the mountaineers to _____ to the high altitude.'
            },
            'accolade': {
                'definition': 'An expression of praise or approval; an award or honor; recognition for exceptional achievement.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AK-uh-layd (emphasis on first syllable)',
                'etymology': 'From French "accolade", from Italian "accollata" meaning "embrace around the neck"',
                'memory_tips': 'Think "ac-cola-ade" - a cola drink as a reward for achievement',
                'alternate_spellings': '',
                'language_origin': 'French via Italian',
                'example_sentence': 'The scientist received numerous _____ for her groundbreaking research.'
            },
            'accommodations': {
                'definition': 'Lodging and food provided for travelers; adjustments made to help someone with special needs; arrangements to suit particular requirements.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'uh-kom-uh-DAY-shunz (emphasis on third syllable)',
                'etymology': 'From Latin "accommodatio", from "accommodare" meaning "to fit, adapt"',
                'memory_tips': 'Think "ac-commode-ations" - comfortable arrangements like a commode',
                'alternate_spellings': 'accommodation (singular)',
                'language_origin': 'Latin',
                'example_sentence': 'The hotel provided excellent _____ for guests with disabilities.'
            },
            'accompli': {
                'definition': 'Short for "fait accompli", meaning an accomplished fact; something already done that cannot be changed.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-kom-PLEE (emphasis on third syllable)',
                'etymology': 'From French "accompli", past participle of "accomplir" meaning "to accomplish"',
                'memory_tips': 'Think "ac-comply" - already complied with, done',
                'alternate_spellings': 'fait accompli (full form)',
                'language_origin': 'French',
                'example_sentence': 'The merger was presented as an _____ to the shareholders.'
            },
            'accomplice': {
                'definition': 'A person who helps another commit a crime; a partner in wrongdoing; someone who assists in an illegal or questionable act.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-KOM-plis (emphasis on second syllable)',
                'etymology': 'From French "complice", from Latin "complex" meaning "confederate, partner"',
                'memory_tips': 'Think "ac-com-police" - working with someone against the police',
                'alternate_spellings': '',
                'language_origin': 'French via Latin',
                'example_sentence': 'The thief and his _____ were both arrested for the bank robbery.'
            },
            'accomplished': {
                'definition': 'Skilled or talented; having achieved a high level of expertise; completed successfully; highly educated or cultured.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'uh-KOM-plisht (emphasis on second syllable)',
                'etymology': 'Past participle of "accomplish", from Old French "accomplir"',
                'memory_tips': 'Think "ac-com-plished" - polished with accomplishments',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'She is an _____ pianist who has performed with major orchestras.'
            },
            'accomplishments': {
                'definition': 'Things that have been achieved successfully; skills or talents; notable achievements or completed tasks.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'uh-KOM-plish-muhnts (emphasis on second syllable)',
                'etymology': 'From "accomplish" + "-ment", from Old French "accomplir"',
                'memory_tips': 'Think "ac-com-plish-ments" - mental list of things you accomplished',
                'alternate_spellings': 'accomplishment (singular)',
                'language_origin': 'Old French',
                'example_sentence': 'His _____ in science earned him international recognition.'
            },
            'accordance': {
                'definition': 'Agreement or harmony with something; conformity to rules, wishes, or standards; the act of granting or giving.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-KOR-dunss (emphasis on second syllable)',
                'etymology': 'From Old French "accordance", from "accorder" meaning "to agree"',
                'memory_tips': 'Think "ac-cord-ance" - dancing in accord with the music',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The contract was signed in _____ with company policy.'
            },
            'accordatura': {
                'definition': 'The tuning of a stringed musical instrument; a specific system or method of tuning strings to produce desired musical intervals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ah-kor-dah-TOO-rah (emphasis on third syllable)',
                'etymology': 'From Italian "accordatura", from "accordare" meaning "to tune, accord"',
                'memory_tips': 'Think "accord-a-tura" - according the instruments together',
                'alternate_spellings': '',
                'language_origin': 'Italian',
                'example_sentence': 'The violinist adjusted the _____ to achieve the perfect pitch.'
            },
            'accouterment': {
                'definition': 'Additional items of dress or equipment; accessories worn or carried for a particular activity; military or ceremonial gear.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-KOO-ter-muhnt (emphasis on second syllable)',
                'etymology': 'From French "accoutrement", from "accoutrer" meaning "to equip"',
                'memory_tips': 'Think "ac-couture-ment" - fashionable equipment like couture',
                'alternate_spellings': 'accoutrement',
                'language_origin': 'French',
                'example_sentence': 'The soldier checked each piece of military _____ before the mission.'
            },
            'accoutrement': {
                'definition': 'Additional items of dress or equipment; accessories worn or carried for a particular activity; military or ceremonial gear.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-KOO-truh-muhnt (emphasis on second syllable)',
                'etymology': 'From French "accoutrement", from "accoutrer" meaning "to equip"',
                'memory_tips': 'Think "ac-couture-ment" - fashionable equipment like couture',
                'alternate_spellings': 'accouterment',
                'language_origin': 'French',
                'example_sentence': 'The knight\'s _____ included sword, shield, and armor.'
            },
            'accrual': {
                'definition': 'The accumulation or increase of something over time; in accounting, income or expenses recognized before payment is made.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-KROO-uhl (emphasis on second syllable)',
                'etymology': 'From "accrue" + "-al", from Old French "accreue" meaning "increase"',
                'memory_tips': 'Think "ac-crew-al" - a crew working to accumulate something',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The _____ of vacation days allowed her to take a month off.'
            },
            'accumulate': {
                'definition': 'To gather together or collect gradually; to build up over time; to amass or pile up in increasing quantities.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'uh-KYOO-myuh-layt (emphasis on second syllable)',
                'etymology': 'From Latin "accumulatus", from "ad" (to) + "cumulus" (heap)',
                'memory_tips': 'Think "ac-cumulus-ate" - like cumulus clouds gathering and growing',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Snow began to _____ on the mountain peaks during the storm.'
            },
            'accurate': {
                'definition': 'Correct and precise; free from error; exact in conformity to truth or to a standard; carefully done.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'AK-yuh-rit (emphasis on first syllable)',
                'etymology': 'From Latin "accuratus", from "ad" (to) + "cura" (care)',
                'memory_tips': 'Think "ac-cure-ate" - cured of mistakes, made accurate',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The scientist needed _____ measurements for the experiment.'
            },
            'accuse': {
                'definition': 'To charge someone with wrongdoing; to blame or claim that someone has done something illegal or wrong.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'uh-KYOOZ (emphasis on second syllable)',
                'etymology': 'From Latin "accusare", from "ad" (to) + "causa" (cause, lawsuit)',
                'memory_tips': 'Think "ac-cause" - pointing to the cause of blame',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The prosecutor will _____ the defendant of theft.'
            },
            'aceituna': {
                'definition': 'Spanish word for olive; the small oval fruit of the olive tree, used for food and oil production.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ah-say-TOO-nah (emphasis on third syllable)',
                'etymology': 'From Spanish "aceituna", from Arabic "az-zaytūna" meaning "olive"',
                'memory_tips': 'Think "ace-tuna" - an ace type of fruit like tuna is an ace fish',
                'alternate_spellings': 'olive (English)',
                'language_origin': 'Spanish from Arabic',
                'example_sentence': 'The Spanish cook used fresh _____ in the traditional recipe.'
            },
            'acequia': {
                'definition': 'An irrigation ditch or canal, especially in the southwestern United States; a community-operated waterway for agricultural use.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ah-SEH-kee-ah (emphasis on second syllable)',
                'etymology': 'From Spanish "acequia", from Arabic "as-sāqiya" meaning "water channel"',
                'memory_tips': 'Think "ace-sequence" - an ace sequence of water channels',
                'alternate_spellings': '',
                'language_origin': 'Spanish from Arabic',
                'example_sentence': 'The ancient _____ system still irrigates the New Mexican farmland.'
            },
            'acerbity': {
                'definition': 'Harshness or severity of manner, speech, or conditions; bitter or sharp quality in taste, character, or expression.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-SUR-bi-tee (emphasis on second syllable)',
                'etymology': 'From Latin "acerbitas", from "acerbus" meaning "harsh, bitter"',
                'memory_tips': 'Think "a-serb-ity" - the harsh quality of being acerbic',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The critic\'s review was marked by unusual _____ toward the performance.'
            },
            'acerola': {
                'definition': 'A small cherry-like fruit from the West Indies, extremely high in vitamin C; also called Barbados cherry.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ah-suh-ROH-lah (emphasis on third syllable)',
                'etymology': 'From Spanish "acerola", possibly from Arabic or indigenous Caribbean languages',
                'memory_tips': 'Think "ace-rola" - an ace fruit that rolls with vitamin C',
                'alternate_spellings': 'Barbados cherry',
                'language_origin': 'Spanish',
                'example_sentence': 'The _____ is prized for its exceptional vitamin C content.'
            },
            'acetaminophen': {
                'definition': 'A common over-the-counter pain reliever and fever reducer; a pharmaceutical compound used as an analgesic and antipyretic.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-see-tuh-MIN-oh-fen (emphasis on fourth syllable)',
                'etymology': 'From chemical nomenclature: "acet-" (relating to acetic acid) + "amino" + "phen" (relating to phenol)',
                'memory_tips': 'Think "ace-tam-in-oh-fen" - ace medicine for pain',
                'alternate_spellings': 'paracetamol (international)',
                'language_origin': 'Modern pharmaceutical nomenclature',
                'example_sentence': 'The doctor recommended _____ for the patient\'s headache.'
            },
            'acetone': {
                'definition': 'A colorless, flammable liquid chemical compound used as a solvent; commonly found in nail polish remover.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AS-uh-tohn (emphasis on first syllable)',
                'etymology': 'From German "Aceton", from Latin "acetum" (vinegar) + "-one" (chemical suffix)',
                'memory_tips': 'Think "ace-tone" - an ace chemical with a strong tone (smell)',
                'alternate_spellings': '',
                'language_origin': 'German from Latin',
                'example_sentence': 'She used _____ to remove the old nail polish.'
            },
            'acharya': {
                'definition': 'A Hindu or Buddhist spiritual teacher or guru; a learned person who teaches religious or philosophical principles.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ah-CHAR-yah (emphasis on second syllable)',
                'etymology': 'From Sanskrit "ācārya" meaning "teacher, guide" from "ācāra" (conduct, behavior)',
                'memory_tips': 'Think "a-charya" - a person who charges you with knowledge',
                'alternate_spellings': '',
                'language_origin': 'Sanskrit',
                'example_sentence': 'The _____ taught meditation and ancient philosophy to his students.'
            },
            'ached': {
                'definition': 'Past tense of ache; experienced a continuous dull pain; felt emotional distress or longing.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'AYKT (single syllable)',
                'etymology': 'From Old English "acan" meaning "to ache, suffer pain"',
                'memory_tips': 'Think "ache-ed" - past tense of feeling aches',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'Her muscles _____ after the long hike through the mountains.'
            },
            'achernar': {
                'definition': 'The brightest star in the constellation Eridanus; a blue giant star located in the southern sky.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'AH-ker-nar (emphasis on first syllable)',
                'etymology': 'From Arabic "ākhir an-nahr" meaning "river\'s end", referring to its position in Eridanus',
                'memory_tips': 'Think "ache-er-nar" - the star that aches to be at the river\'s end',
                'alternate_spellings': '',
                'language_origin': 'Arabic',
                'example_sentence': 'Astronomers studied _____ to understand the behavior of rapidly spinning stars.'
            },
            'achievement': {
                'definition': 'Something accomplished successfully; a notable accomplishment or attainment; the act of achieving a goal.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-CHEEV-muhnt (emphasis on second syllable)',
                'etymology': 'From "achieve" + "-ment", from Old French "achever" meaning "to complete"',
                'memory_tips': 'Think "a-chief-ment" - becoming chief through accomplishment',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'Graduating with honors was her greatest academic _____.'
            },
            'achilles': {
                'definition': 'Referring to Achilles, the Greek hero of the Trojan War; often used in "Achilles\' heel" meaning a vulnerable point.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'uh-KIL-eez (emphasis on second syllable)',
                'etymology': 'From Greek "Akhilleus", name of the legendary Greek warrior',
                'memory_tips': 'Think "a-kill-ease" - he could kill with ease except for his heel',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'His pride was his _____ heel in business negotiations.'
            },
            'achromatic': {
                'definition': 'Without color; black, white, or gray; relating to light transmission without decomposition into spectral colors.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ay-kroh-MAT-ik (emphasis on third syllable)',
                'etymology': 'From Greek "a-" (without) + "chrōma" (color) + "-ic"',
                'memory_tips': 'Think "a-chrome-atic" - without the chrome color',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The photographer preferred _____ film for artistic black and white images.'
            },
            'acicula': {
                'definition': 'A needle-like structure or appendage; a small, sharp-pointed projection found in plants, animals, or crystals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-SIK-yuh-lah (emphasis on second syllable)',
                'etymology': 'From Latin "acicula", diminutive of "acus" meaning "needle"',
                'memory_tips': 'Think "a-sick-ula" - a small needle that might make you sick',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The cactus spine is a type of _____ that protects the plant.'
            },
            'acidophilus': {
                'definition': 'A type of beneficial bacteria (Lactobacillus acidophilus) used in probiotics and yogurt production; acid-loving microorganisms.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'as-id-OH-fi-lus (emphasis on third syllable)',
                'etymology': 'From Latin "acidus" (acid) + Greek "philos" (loving)',
                'memory_tips': 'Think "acid-oh-phil-us" - organisms that love acid',
                'alternate_spellings': 'L. acidophilus (scientific)',
                'language_origin': 'Modern Latin from Greek',
                'example_sentence': 'The yogurt contained live _____ cultures for digestive health.'
            },
            'acoel': {
                'definition': 'A type of simple, flatworm-like marine animal without a body cavity; a member of the phylum Acoelomorpha.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AY-seel (emphasis on first syllable)',
                'etymology': 'From Greek "a-" (without) + "koilos" (cavity)',
                'memory_tips': 'Think "a-coil" - without the coiled body cavity',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Marine biologists studied the _____ to understand early animal evolution.'
            },
            'acorn': {
                'definition': 'The nut of an oak tree; a hard-shelled seed that serves as food for many animals and can grow into an oak tree.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AY-korn (emphasis on first syllable)',
                'etymology': 'From Old English "æcern", related to "æcer" (field, acre)',
                'memory_tips': 'Think "a-corn" - a piece of corn from a tree (though not actually corn)',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The squirrel buried the _____ to save it for winter.'
            },
            'acoustic': {
                'definition': 'Relating to sound or hearing; designed to improve sound quality; using natural sound without electronic amplification.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'uh-KOO-stik (emphasis on second syllable)',
                'etymology': 'From Greek "akoustikos", from "akouein" meaning "to hear"',
                'memory_tips': 'Think "a-cue-stick" - a cue stick that makes acoustic sounds when hitting balls',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ guitar produced beautiful natural tones without amplification.'
            },
            'acquaintance': {
                'definition': 'A person known slightly but not intimately; familiarity with someone or something; the state of knowing someone casually.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'uh-KWAYN-tunss (emphasis on second syllable)',
                'etymology': 'From Old French "acointance", from "acointer" meaning "to make known"',
                'memory_tips': 'Think "ac-quaint-ance" - a quaint dance of getting to know someone',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'She met an old _____ from college at the coffee shop.'
            },
            'acquiesce': {
                'definition': 'To accept or agree without protest; to submit or comply passively; to consent reluctantly but without resistance.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ak-wee-ESS (emphasis on third syllable)',
                'etymology': 'From Latin "acquiescere", from "ad" (to) + "quiescere" (to rest, be quiet)',
                'memory_tips': 'Think "ac-quiet-ess" - becoming quiet and accepting',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'After lengthy debate, he decided to _____ to the committee\'s decision.'
            },
            'acquit': {
                'definition': 'To declare someone not guilty of a criminal charge; to conduct oneself in a specified manner; to discharge a duty.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'uh-KWIT (emphasis on second syllable)',
                'etymology': 'From Old French "acquiter", from "a-" (to) + "quiter" (to free)',
                'memory_tips': 'Think "ac-quit" - quitting the accusation',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The jury voted to _____ the defendant of all charges.'
            },
            'acquitcapnometer': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "acquit" (to declare not guilty) + "capnometer" (device measuring CO2).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "acquit" and "capnometer"',
                'alternate_spellings': 'acquit + capnometer (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'acral': {
                'definition': 'Relating to the extremities of the body; pertaining to the hands, feet, or other terminal parts of limbs.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'AY-kruhl (emphasis on first syllable)',
                'etymology': 'From Greek "akron" meaning "extremity, tip" + "-al"',
                'memory_tips': 'Think "a-crawl" - relating to parts that crawl (hands and feet)',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The dermatologist examined the _____ regions for signs of frostbite.'
            },
            'acrid': {
                'definition': 'Having a strong, unpleasant, and sharp smell or taste; harsh or bitter in manner, speech, or temperament.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'AK-rid (emphasis on first syllable)',
                'etymology': 'From Latin "acer" meaning "sharp, keen" + "-id"',
                'memory_tips': 'Think "ac-rid" - getting rid of something because it\'s so sharp and unpleasant',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ smoke from the fire made everyone\'s eyes water.'
            },
            'acrimony': {
                'definition': 'Harsh or bitter speech, manner, or feelings; anger and resentment expressed in words; sharpness of temper or language.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AK-ruh-moh-nee (emphasis on first syllable)',
                'etymology': 'From Latin "acrimonia", from "acer" meaning "sharp, keen"',
                'memory_tips': 'Think "ac-rim-money" - sharp words about money causing bitterness',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The divorce proceedings were marked by considerable _____ between the parties.'
            },
            'acrogeria': {
                'definition': 'A rare genetic disorder causing premature aging of the skin on hands and feet; a condition affecting the extremities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ak-roh-JEE-ree-ah (emphasis on third syllable)',
                'etymology': 'From Greek "akron" (extremity) + "gēras" (old age) + "-ia"',
                'memory_tips': 'Think "acro-geria" - aging (geriatric) of the extremities (acro)',
                'alternate_spellings': '',
                'language_origin': 'Modern medical Greek',
                'example_sentence': 'The child was diagnosed with _____, a condition causing aged-looking skin on the hands.'
            },
            'acronym': {
                'definition': 'A word formed from the initial letters of other words; an abbreviation pronounced as a word rather than spelled out.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AK-ruh-nim (emphasis on first syllable)',
                'etymology': 'From Greek "akron" (tip, end) + "onyma" (name)',
                'memory_tips': 'Think "acro-nym" - name made from the tips (first letters) of words',
                'alternate_spellings': '',
                'language_origin': 'Modern Greek',
                'example_sentence': 'NASA is an _____ for National Aeronautics and Space Administration.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_002_data:
            return batch_002_data[word_lower]
        
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
    
    def process_batch_002(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 002 with comprehensive Claude data"""
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
    
    def save_batch_002_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 002 processed words to CSV"""
        
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
    """Process Batch 002 with comprehensive Claude data"""
    processor = Batch002Processor()
    input_csv = Path("output/batch_002_words.csv")
    output_csv = Path("output/batch_002_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 002 with comprehensive Claude data...")
    
    # Process all words in batch 002
    processed_words = processor.process_batch_002(input_csv)
    
    # Save results
    processor.save_batch_002_csv(processed_words, output_csv)
    
    logger.info(f"Batch 002 processing completed!")
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