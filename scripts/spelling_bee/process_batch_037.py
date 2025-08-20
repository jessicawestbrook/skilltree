#!/usr/bin/env python3
"""
Process Batch 037 of Spelling Bee Words with Comprehensive Claude Data
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

class Batch037Processor:
    """Processes Batch 037 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 037 words"""
        
        # Comprehensive data for all 50 words in Batch 037
        batch_037_data = {
            'cochineal': {
                'definition': 'A red dye obtained from dried female cochineal insects; the insect itself, native to Mexico and Central America, used historically to create crimson and scarlet colors.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'koh-chuh-NEEL or KOCH-uh-neel (emphasis varies)',
                'etymology': 'From Spanish "cochinilla", diminutive of "cochino" (pig), referring to the insect\'s appearance',
                'memory_tips': 'Think "coach-in-eel" - a red dye that colored coaches, slippery like an eel',
                'alternate_spellings': '',
                'language_origin': 'Spanish',
                'example_sentence': 'The vibrant red fabric was dyed with traditional _____ extract from Mexican insects.'
            },
            'cochlear': {
                'definition': 'Relating to the cochlea of the inner ear; spiral-shaped like a snail shell; pertaining to hearing and sound processing.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'KOKE-lee-er (emphasis on first syllable)',
                'etymology': 'From Latin "cochlea" (snail shell), from Greek "kokhlias" (spiral shell)',
                'memory_tips': 'Think "cock-lear" - a rooster\'s ear that hears in spirals',
                'alternate_spellings': '',
                'language_origin': 'Latin (from Greek)',
                'example_sentence': 'The _____ implant restored partial hearing to the young patient.'
            },
            'cockles': {
                'definition': 'Small, heart-shaped edible shellfish; the ventricles of the heart (in the phrase "warm the cockles of your heart").',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'KOK-uhlz (emphasis on first syllable)',
                'etymology': 'From Old French "coquille" (shell), from Latin "conchylia" (shellfish)',
                'memory_tips': 'Think "cock-els" - small shells that make your heart cockle with warmth',
                'alternate_spellings': '',
                'language_origin': 'Old French (from Latin)',
                'example_sentence': 'The story of the rescue warmed the _____ of everyone\'s heart.'
            },
            'cocoa': {
                'definition': 'A powder made from roasted and ground cacao seeds; a hot drink made from this powder; the brown color of chocolate.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'KOH-koh (emphasis on first syllable)',
                'etymology': 'From Spanish "cacao", from Nahuatl "cacahuatl" (cacao bean)',
                'memory_tips': 'Think "co-co" - like coconut but brown, the color of chocolate',
                'alternate_spellings': '',
                'language_origin': 'Spanish (from Nahuatl)',
                'example_sentence': 'She sipped hot _____ by the fireplace on the snowy winter evening.'
            },
            'cocoon': {
                'definition': 'A silky case spun by insect larvae for protection during metamorphosis; anything that envelops protectively.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'kuh-KOON (emphasis on second syllable)',
                'etymology': 'From French "cocon", from Provençal "coucoun", possibly from "coque" (shell)',
                'memory_tips': 'Think "co-coon" - a cooperative coon (raccoon) wrapping itself for protection',
                'alternate_spellings': '',
                'language_origin': 'French (from Provençal)',
                'example_sentence': 'The caterpillar spun its silky _____ before transforming into a butterfly.'
            },
            'codicil': {
                'definition': 'An addition or supplement to a will that modifies or adds to its provisions; an appendix or supplement to any document.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KOD-uh-sil (emphasis on first syllable)',
                'etymology': 'From Latin "codicillus", diminutive of "codex" (book, legal document)',
                'memory_tips': 'Think "code-icil" - a small addition to the legal code',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The lawyer drafted a _____ to add the new grandchildren to the inheritance.'
            },
            'codswallop': {
                'definition': 'British slang for nonsense or rubbish; something regarded as untrue or meaningless.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KODZ-wol-uhp (emphasis on first syllable)',
                'etymology': 'British slang, possibly from "Codd\'s wallop" (a type of beer bottle), meaning inferior drink',
                'memory_tips': 'Think "cod\'s-wallop" - what a cod fish might say (nonsense)',
                'alternate_spellings': '',
                'language_origin': 'British slang',
                'example_sentence': 'He dismissed the conspiracy theory as complete _____.'
            },
            'coercive': {
                'definition': 'Using force or threats to make someone do something; involving compulsion or constraint.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'koh-UR-siv (emphasis on second syllable)',
                'etymology': 'From "coerce" + "-ive", where coerce comes from Latin "coercere" (to restrain)',
                'memory_tips': 'Think "co-ercive" - forcing cooperation through pressure',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The dictator used _____ tactics to maintain control over the population.'
            },
            'coeval': {
                'definition': 'Of the same age or period; contemporary; existing or occurring at the same time.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'koh-EE-vuhl (emphasis on second syllable)',
                'etymology': 'From Latin "coaevus", from "co-" (together) + "aevum" (age)',
                'memory_tips': 'Think "co-evil" - people of the same age who might get into mischief together',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The artifacts were _____ with the ancient Roman settlement.'
            },
            'coffee': {
                'definition': 'A hot drink made from roasted and ground coffee beans; the brown seeds of a tropical shrub; the color of coffee.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'KOF-ee (emphasis on first syllable)',
                'etymology': 'From Turkish "kahve", from Arabic "qahwah", possibly from Ethiopian',
                'memory_tips': 'Think of the brown liquid that wakes you up in the morning',
                'alternate_spellings': '',
                'language_origin': 'Turkish (from Arabic)',
                'example_sentence': 'She needed a strong cup of _____ to start her busy workday.'
            },
            'cogently': {
                'definition': 'In a clear, logical, and convincing manner; persuasively and with compelling force.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'KOH-juhnt-lee (emphasis on first syllable)',
                'etymology': 'From "cogent" + "-ly", where cogent comes from Latin "cogere" (to drive together)',
                'memory_tips': 'Think "co-gently" - gently driving points together cooperatively',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The lawyer argued _____ for her client\'s innocence using compelling evidence.'
            },
            'cogitation': {
                'definition': 'Deep thought or meditation; the process of thinking carefully about something; contemplation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'koj-uh-TAY-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "cogitatio", from "cogitare" (to think)',
                'memory_tips': 'Think "cog-itation" - your brain\'s cogs turning during deep thought',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'After hours of _____, he finally reached a decision about his career.'
            },
            'cognisant': {
                'definition': 'British spelling of cognizant; having knowledge or awareness of something; being conscious or informed.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'KOG-ni-zuhnt (emphasis on first syllable)',
                'etymology': 'From Latin "cognoscere" (to get to know), with British "-isant" spelling',
                'memory_tips': 'Think "cog-nis-ant" - an ant whose cogs of knowledge are turning',
                'alternate_spellings': 'cognizant (American spelling)',
                'language_origin': 'Latin',
                'example_sentence': 'The manager was _____ of the potential risks involved in the project.'
            },
            'cognizant': {
                'definition': 'Having knowledge or awareness of something; being conscious, informed, or mindful.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'KOG-ni-zuhnt (emphasis on first syllable)',
                'etymology': 'From Latin "cognoscere" (to get to know), with American "-izant" spelling',
                'memory_tips': 'Think "cog-nize-ant" - an ant that recognizes and knows things',
                'alternate_spellings': 'cognisant (British spelling)',
                'language_origin': 'Latin',
                'example_sentence': 'She was fully _____ of the consequences before making her decision.'
            },
            'cohesive': {
                'definition': 'Forming a united whole; characterized by unity and solidarity; tending to stick together.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'koh-HEE-siv (emphasis on second syllable)',
                'etymology': 'From "cohere" + "-sive", where cohere comes from Latin "cohaerere" (to stick together)',
                'memory_tips': 'Think "co-he-sive" - he and others sticking together cooperatively',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The team developed a _____ strategy that unified all departments.'
            },
            'cohesiveadjectives': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "cohesive" (unified) + "adjectives" (descriptive words).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "cohesive" and "adjectives"',
                'alternate_spellings': 'cohesive + adjectives (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'cohort': {
                'definition': 'A group of people with shared characteristics; a band of warriors or soldiers; a generation or peer group.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KOH-hort (emphasis on first syllable)',
                'etymology': 'From Latin "cohors" (enclosed yard, company of soldiers)',
                'memory_tips': 'Think "co-hort" - a group that works together in cooperation',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The research study followed a _____ of students over ten years.'
            },
            'cohosh': {
                'definition': 'Any of several North American plants used in herbal medicine, particularly black cohosh, traditionally used for women\'s health issues.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KOH-hosh (emphasis on first syllable)',
                'etymology': 'From Algonquian (Native American) language, exact origin uncertain',
                'memory_tips': 'Think "co-hosh" - a plant that Native Americans said "hush" to pain',
                'alternate_spellings': '',
                'language_origin': 'Algonquian (Native American)',
                'example_sentence': 'The herbalist recommended _____ to help with menopausal symptoms.'
            },
            'coiffure': {
                'definition': 'A person\'s hairstyle, especially an elaborate one; the art or act of arranging hair; to arrange someone\'s hair.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'kwah-FYOOR (emphasis on second syllable)',
                'etymology': 'From French "coiffure", from "coiffer" (to cover the head)',
                'memory_tips': 'Think "quaff-your" - quaffing drinks while getting your hair done',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The bride\'s elaborate _____ took three hours to complete.'
            },
            'coiffurerepartee': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "coiffure" (hairstyle) + "repartee" (witty conversation).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "coiffure" and "repartee"',
                'alternate_spellings': 'coiffure + repartee (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'coincidence': {
                'definition': 'A remarkable occurrence of events at the same time by chance; the fact of corresponding in nature or time.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'koh-IN-si-duhns (emphasis on second syllable)',
                'etymology': 'From Latin "coincidere", from "co-" (together) + "incidere" (to fall)',
                'memory_tips': 'Think "co-incidence" - incidents that happen together by chance',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'It was quite a _____ that they both chose the same restaurant.'
            },
            'colcannon': {
                'definition': 'A traditional Irish dish made with mashed potatoes and kale or cabbage, often mixed with butter and milk.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kol-KAN-uhn (emphasis on second syllable)',
                'etymology': 'From Irish "cál ceannann" (white-headed cabbage)',
                'memory_tips': 'Think "coal-cannon" - a cannon that shoots coal-colored (dark green) vegetables',
                'alternate_spellings': '',
                'language_origin': 'Irish',
                'example_sentence': 'The Irish pub served traditional _____ alongside the corned beef.'
            },
            'colcannonnoun': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "colcannon" (Irish dish) + "noun" (part of speech).',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "colcannon" and "noun"',
                'alternate_spellings': 'colcannon + noun (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'cold': {
                'definition': 'Having a low temperature; lacking warmth; unfriendly or unemotional; a common viral infection of the nose and throat.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'KOHLD (emphasis on single syllable)',
                'etymology': 'From Old English "ceald", from Proto-Germanic "*kaldaz"',
                'memory_tips': 'Think of shivering in winter or having a stuffy nose',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The _____ winter wind made everyone bundle up in heavy coats.'
            },
            'coleus': {
                'definition': 'A tropical plant with colorful, ornamental leaves, popular as a houseplant and in gardens for its vibrant foliage.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KOH-lee-uhs (emphasis on first syllable)',
                'etymology': 'From Greek "koleos" (sheath), referring to the way stamens are joined',
                'memory_tips': 'Think "cool-e-us" - a cool, colorful plant that makes us happy',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The gardener planted bright red and purple _____ to add color to the shade garden.'
            },
            'colic': {
                'definition': 'Severe abdominal pain caused by intestinal gas or obstruction; in babies, prolonged crying due to digestive discomfort.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KOL-ik (emphasis on first syllable)',
                'etymology': 'From Greek "kolikos" (of the colon), from "kolon" (large intestine)',
                'memory_tips': 'Think "coal-ick" - stomach pain that makes you feel sick like eating coal',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The pediatrician assured the parents that the baby\'s _____ would improve with time.'
            },
            'collaboration': {
                'definition': 'The action of working with someone to produce or create something; cooperation between people or groups.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kuh-lab-uh-RAY-shuhn (emphasis on fourth syllable)',
                'etymology': 'From Latin "collaborare", from "co-" (together) + "laborare" (to work)',
                'memory_tips': 'Think "co-labor-ation" - working together cooperatively',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The successful project was the result of close _____ between all departments.'
            },
            'collapsar': {
                'definition': 'A collapsed star; an astronomical object formed when a massive star undergoes gravitational collapse, potentially forming a black hole.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kuh-LAP-sar (emphasis on second syllable)',
                'etymology': 'Blend of "collapse" + "star", coined in astrophysics',
                'memory_tips': 'Think "collapse-ar" - a star that has collapsed',
                'alternate_spellings': '',
                'language_origin': 'Modern scientific (blend word)',
                'example_sentence': 'The _____ was so dense that not even light could escape its gravitational pull.'
            },
            'collar': {
                'definition': 'The part of a shirt or garment around the neck; a band around an animal\'s neck; to seize or grab someone.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'KOL-er (emphasis on first syllable)',
                'etymology': 'From Latin "collare", from "collum" (neck)',
                'memory_tips': 'Think of the part of a shirt that goes around your neck',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'He straightened his shirt _____ before the important business meeting.'
            },
            'colleagues': {
                'definition': 'People who work together, especially in a profession or business; fellow workers or associates.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'KOL-eegz (emphasis on first syllable)',
                'etymology': 'From French "collègue", from Latin "collega" (partner in office)',
                'memory_tips': 'Think "coal-leagues" - people in the same league as you at work',
                'alternate_spellings': '',
                'language_origin': 'French (from Latin)',
                'example_sentence': 'She enjoyed working with her supportive _____ on the research team.'
            },
            'collect': {
                'definition': 'To bring or gather together; to accumulate items as a hobby; to pick up or fetch someone.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'kuh-LEKT (emphasis on second syllable)',
                'etymology': 'From Latin "collectus", past participle of "colligere" (to gather together)',
                'memory_tips': 'Think "co-lect" - cooperatively selecting and gathering things',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She decided to _____ vintage postcards from around the world.'
            },
            'collectanea': {
                'definition': 'A collection of miscellaneous items, especially literary passages or scholarly materials; an anthology or compilation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kol-ek-TAY-nee-ah (emphasis on third syllable)',
                'etymology': 'From Latin "collectanea", neuter plural of "collectaneus" (collected)',
                'memory_tips': 'Think "collect-an-ea" - collecting things with an "ea" sound',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The scholar\'s _____ contained fascinating excerpts from medieval manuscripts.'
            },
            'collected': {
                'definition': 'Past tense of collect; gathered together; calm and composed; assembled as a group.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'kuh-LEK-tid (emphasis on second syllable)',
                'etymology': 'Past tense of "collect", from Latin "collectus"',
                'memory_tips': 'Think "co-lected" - cooperatively selected and gathered, now finished',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She remained calm and _____ during the emergency situation.'
            },
            'collection': {
                'definition': 'A group of objects gathered and kept together; the action of collecting; money collected for charity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kuh-LEK-shuhn (emphasis on second syllable)',
                'etymology': 'From Latin "collectio", from "colligere" (to gather together)',
                'memory_tips': 'Think "co-lection" - cooperatively selecting and arranging items',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'His stamp _____ included rare specimens from every continent.'
            },
            'collegiality': {
                'definition': 'A cooperative relationship among colleagues; the spirit of friendly cooperation and mutual respect in a workplace.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kuh-lee-jee-AL-uh-tee (emphasis on fourth syllable)',
                'etymology': 'From "collegial" + "-ity", where collegial comes from Latin "collegium" (partnership)',
                'memory_tips': 'Think "college-ality" - the friendly spirit found in college partnerships',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The department was known for its spirit of _____ and mutual support.'
            },
            'collie': {
                'definition': 'A breed of dog known for intelligence and herding ability, with long hair and a pointed snout, popularized by "Lassie".',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KOL-ee (emphasis on first syllable)',
                'etymology': 'Possibly from Scottish "colley" (black-faced sheep) or "coll" (coal)',
                'memory_tips': 'Think of Lassie, the famous loyal dog who saved people',
                'alternate_spellings': '',
                'language_origin': 'Scottish',
                'example_sentence': 'The border _____ expertly herded the sheep into the pen.'
            },
            'collimate': {
                'definition': 'To make parallel; to adjust the alignment of optical elements; to focus or direct light rays in parallel lines.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'KOL-uh-mayt (emphasis on first syllable)',
                'etymology': 'From Latin "collimare", alteration of "collineare" (to align)',
                'memory_tips': 'Think "colli-mate" - making light rays like mates walking in parallel',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The technician needed to _____ the laser beam for the precision experiment.'
            },
            'collision': {
                'definition': 'An instance of one moving object striking another; a conflict between opposing ideas or parties.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kuh-LIZH-uhn (emphasis on second syllable)',
                'etymology': 'From Latin "collisio", from "collidere" (to strike together)',
                'memory_tips': 'Think "co-lision" - two things cooperatively deciding to crash together',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The traffic _____ was caused by icy road conditions.'
            },
            'colloque': {
                'definition': 'A formal academic conference or seminar; a scholarly discussion or conversation between experts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kol-OHKE or KOL-oke (emphasis varies)',
                'etymology': 'From French "colloque", from Latin "colloquium" (conversation)',
                'memory_tips': 'Think "collo-que" - a queue of people gathered to talk together',
                'alternate_spellings': '',
                'language_origin': 'French (from Latin)',
                'example_sentence': 'The international _____ brought together leading scientists from around the world.'
            },
            'colluctation': {
                'definition': 'A struggle or contest; striving or contention, especially in an intellectual or spiritual sense.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kol-uhk-TAY-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "colluctatio", from "colluctari" (to struggle together)',
                'memory_tips': 'Think "collo-uctation" - a collective action of struggling',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The philosopher described the _____ between reason and emotion in human nature.'
            },
            'collude': {
                'definition': 'To cooperate secretly for an illegal or deceitful purpose; to conspire or plot together.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'kuh-LOOD (emphasis on second syllable)',
                'etymology': 'From Latin "colludere", from "co-" (together) + "ludere" (to play)',
                'memory_tips': 'Think "co-lude" - playing together cooperatively, but secretly and wrongly',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The investigation revealed that several officials had conspired to _____ with the criminals.'
            },
            'colocate': {
                'definition': 'To place side by side or in the same location; in linguistics, to occur together frequently.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'koh-loh-KAYT (emphasis on third syllable)',
                'etymology': 'From Latin "co-" (together) + "locare" (to place)',
                'memory_tips': 'Think "co-locate" - cooperatively locating things in the same place',
                'alternate_spellings': 'co-locate (hyphenated)',
                'language_origin': 'Latin',
                'example_sentence': 'The company decided to _____ its manufacturing and research facilities.'
            },
            'colonel': {
                'definition': 'A military officer of high rank, typically commanding a regiment; the pronunciation differs significantly from the spelling.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KUR-nuhl (emphasis on first syllable, sounds like "kernel")',
                'etymology': 'From French "coronel", from Italian "colonnello" (little column commander)',
                'memory_tips': 'Remember it sounds like "kernel" - think of a kernel of corn commanding troops',
                'alternate_spellings': '',
                'language_origin': 'French (from Italian)',
                'example_sentence': 'The _____ addressed the troops before the important military exercise.'
            },
            'colonists': {
                'definition': 'People who settle in a new territory but remain subject to or connected with their parent country; settlers.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'KOL-uh-nists (emphasis on first syllable)',
                'etymology': 'From "colony" + "-ist" + "-s", where colony comes from Latin "colonia"',
                'memory_tips': 'Think "colon-ists" - people who established colonies, like the American colonists',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The early American _____ faced many hardships during their first winter.'
            },
            'color': {
                'definition': 'The property of objects that produces different sensations on the eye; hue, tint, or pigment; to give color to something.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'KUL-er (emphasis on first syllable)',
                'etymology': 'From Latin "color" (color, complexion)',
                'memory_tips': 'Think of the rainbow with all its different colors',
                'alternate_spellings': 'colour (British spelling)',
                'language_origin': 'Latin',
                'example_sentence': 'The artist mixed different paints to create the perfect shade of blue _____.'
            },
            'colossal': {
                'definition': 'Extremely large or great; gigantic in size or extent; impressively large.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'kuh-LOS-uhl (emphasis on second syllable)',
                'etymology': 'From "colossus" + "-al", where colossus comes from Greek "kolossos" (giant statue)',
                'memory_tips': 'Think of the Colossus of Rhodes, a gigantic ancient statue',
                'alternate_spellings': '',
                'language_origin': 'Greek (via Latin)',
                'example_sentence': 'The project required a _____ amount of time and resources to complete.'
            },
            'colour': {
                'definition': 'British spelling of color; the property of objects that produces different sensations on the eye; hue or pigment.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'KUL-er (emphasis on first syllable)',
                'etymology': 'From Latin "color", with British spelling retention of "ou"',
                'memory_tips': 'Think "col-our" - our collective way of seeing the spectrum',
                'alternate_spellings': 'color (American spelling)',
                'language_origin': 'Latin',
                'example_sentence': 'The British artist preferred watercolours for their translucent _____.'
            },
            'colporter': {
                'definition': 'A person who travels around selling books, newspapers, or religious tracts; an itinerant book peddler.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KOL-por-ter (emphasis on first syllable)',
                'etymology': 'From French "colporteur", from "col" (neck) + "porter" (to carry)',
                'memory_tips': 'Think "col-porter" - carrying books around your collar/neck area',
                'alternate_spellings': 'colporteur',
                'language_origin': 'French',
                'example_sentence': 'The _____ traveled from village to village selling religious books and pamphlets.'
            },
            'colporteur': {
                'definition': 'A person who distributes or sells books, newspapers, or religious literature, especially while traveling; an itinerant book seller.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kol-por-TUR (emphasis on third syllable)',
                'etymology': 'From French "colporteur", from "col" (neck) + "porter" (to carry)',
                'memory_tips': 'Think "col-port-eur" - a European who carries books around their collar',
                'alternate_spellings': 'colporter',
                'language_origin': 'French',
                'example_sentence': 'The dedicated _____ spread literacy by bringing books to remote mountain communities.'
            },
            'colquitt': {
                'definition': 'A proper noun, typically a surname; also the name of several places in the United States, particularly counties in Georgia and Texas.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'KOL-kwit (emphasis on first syllable)',
                'etymology': 'American surname, possibly from English or Scottish origins',
                'memory_tips': 'Think "coal-quit" - someone who quit working with coal',
                'alternate_spellings': '',
                'language_origin': 'English/Scottish (American usage)',
                'example_sentence': '_____ County was named after an important political figure in Georgia history.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_037_data:
            return batch_037_data[word_lower]
        
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
    
    def process_batch_037(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 037 with comprehensive Claude data"""
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
    
    def save_batch_037_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 037 processed words to CSV"""
        
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
    """Process Batch 037 with comprehensive Claude data"""
    processor = Batch037Processor()
    input_csv = Path("output/batch_037_words.csv")
    output_csv = Path("output/batch_037_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 037 with comprehensive Claude data...")
    
    # Process all words in batch 037
    processed_words = processor.process_batch_037(input_csv)
    
    # Save results
    processor.save_batch_037_csv(processed_words, output_csv)
    
    logger.info(f"Batch 037 processing completed!")
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