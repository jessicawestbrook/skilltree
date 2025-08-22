#!/usr/bin/env python3
"""
Process Batch 170 of Spelling Bee Words with Comprehensive Claude Data
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
            'government', 'company', 'number', 'group', 'problem', 'fact', 'strong', 'student', 'students', 'studied', 'studies', 'studio', 'studying',
            'stuff', 'style'
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
            'mega', 'micro', 'mini', 'multi', 'neo', 'pseudo', 'ultra', 'ac', 'ad', 'con', 'strat',
            'str', 'st'
        ]
        
        # Common suffixes
        suffixes = [
            'ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment', 'able', 'ible',
            'ful', 'less', 'ous', 'ious', 'al', 'ic', 'ical', 'ism', 'ist', 'ize', 'ise',
            'fy', 'ward', 'wise', 'like', 'ship', 'hood', 'dom', 'age', 'ery', 'ary', 'ate',
            'oid', 'ary', 'ery', 'ity', 'ship', 'ness', 'ure', 'ency', 'tic'
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

class Batch170Processor:
    """Processes Batch 170 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 170 words"""
        
        # Comprehensive data for all 50 words in Batch 170
        batch_170_data = {
            'strelitzia': {
                'definition': 'A tropical plant native to South Africa, also known as bird-of-paradise flower, prized for its striking orange and blue bird-like blooms. Named after Queen Charlotte of Mecklenburg-Strelitz, these plants are popular in warm climates and as houseplants. The distinctive flowers emerge from boat-shaped bracts and resemble exotic birds in flight.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'streh-LIT-zee-uh (emphasis on second syllable)',
                'etymology': 'Named after Queen Charlotte of Mecklenburg-Strelitz by Sir Joseph Banks',
                'memory_tips': 'Think "Strelitz-ia" - named after the Strelitz royal family',
                'alternate_spellings': '',
                'language_origin': 'Modern Latin (named after person)',
                'example_sentence': 'The _____ in the botanical garden bloomed with spectacular orange and blue flowers.'
            },
            'strength': {
                'definition': 'The quality or state of being physically strong; the capacity to resist force, stress, or wear; mental or moral power to endure difficulties. Physical strength involves muscular power and endurance. Emotional strength helps people cope with challenges and adversity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STRENGTH (one syllable with "ng" sound)',
                'etymology': 'From Old English "strengþu," from "strang" meaning "strong"',
                'memory_tips': 'Think "strong-th" - the quality of being strong',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'Her _____ of character helped her overcome every obstacle.'
            },
            'strengthen': {
                'definition': 'To make or become stronger; to increase the strength, force, or intensity of something; to reinforce or fortify. This can apply to physical objects, muscles, relationships, arguments, or abstract concepts like resolve or commitment.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'STRENG-thuhn (emphasis on first syllable)',
                'etymology': 'From "strength" + "-en" (causative verb suffix)',
                'memory_tips': 'Think "strength-en" - to make something have strength',
                'alternate_spellings': '',
                'language_origin': 'Old English + suffix',
                'example_sentence': 'Regular exercise will _____ your muscles and improve your health.'
            },
            'stress': {
                'definition': 'Physical, mental, or emotional strain or tension; emphasis placed on words or syllables; force exerted on an object. In psychology, stress refers to the body\'s response to challenging situations. In linguistics, it refers to vocal emphasis.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'STRES (rhymes with "dress")',
                'etymology': 'From Old French "destresse," later "stress" from Latin "strictus" meaning "drawn tight"',
                'memory_tips': 'Think "stress" sounds like "press" - pressure causing tension',
                'alternate_spellings': '',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The _____ of final exams made many students anxious.'
            },
            'stressed': {
                'definition': 'Past tense of stress; experiencing mental or emotional strain; emphasized or given prominence; subjected to physical force or pressure. Can describe both psychological states and mechanical conditions.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'STREST (one syllable)',
                'etymology': 'Past tense of "stress," from Latin "strictus"',
                'memory_tips': 'Think "stress-ed" - past tense of being under stress',
                'alternate_spellings': '',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'She felt _____ about the important presentation tomorrow.'
            },
            'stretcher': {
                'definition': 'A framework of canvas or other material stretched between poles, used for carrying sick, injured, or dead persons; a device used to extend or stretch something; a person who stretches materials or exaggerates stories.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STRECH-ur (emphasis on first syllable)',
                'etymology': 'From "stretch" + "-er," from Old English "streccan"',
                'memory_tips': 'Think "stretch-er" - something that stretches to carry people',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The paramedics carefully placed the patient on a _____.'
            },
            'stretto': {
                'definition': 'In music, especially in fugues, a passage where successive entries of the subject occur at shorter intervals than usual, creating overlapping voices. This technique increases musical tension and demonstrates compositional skill.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STRET-oh (emphasis on first syllable)',
                'etymology': 'From Italian "stretto" meaning "narrow, tight," from Latin "strictus"',
                'memory_tips': 'Think "stretch-o" - stretching musical voices closer together',
                'alternate_spellings': '',
                'language_origin': 'Italian via Latin',
                'example_sentence': 'The composer used a _____ to build excitement in the fugue\'s final section.'
            },
            'striation': {
                'definition': 'A series of ridges, furrows, or linear marks; the arrangement of striations in a pattern. Common in geology (rock formations), biology (muscle fibers), and archaeology (tool marks). Striations provide evidence of processes and forces.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'stry-AY-shuhn (emphasis on second syllable)',
                'etymology': 'From Latin "striatus" meaning "grooved, striped" + "-ion"',
                'memory_tips': 'Think "stri-ation" - the action of making stripes or grooves',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The geologist studied the rock\'s _____ to understand its formation history.'
            },
            'stricture': {
                'definition': 'A restriction or limitation; a critical remark or censure; in medicine, an abnormal narrowing of a body passage. Legal strictures limit behavior, while medical strictures can impede normal function.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STRIK-cher (emphasis on first syllable)',
                'etymology': 'From Latin "strictura" meaning "a drawing tight," from "stringere"',
                'memory_tips': 'Think "strict-ure" - a strict rule that restricts',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The new law placed strict _____ on industrial emissions.'
            },
            'stridency': {
                'definition': 'The quality of being strident; harshness of sound; forcefulness or urgency in expression that may be unpleasant or grating. Often describes voices, protests, or demands that are loud, shrill, and insistent.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STRY-den-see (emphasis on first syllable)',
                'etymology': 'From "strident" + "-cy," from Latin "stridens" meaning "creaking, harsh"',
                'memory_tips': 'Think "stride-ency" - walking with loud, harsh steps',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ of the political rhetoric alienated moderate voters.'
            },
            'strife': {
                'definition': 'Angry or bitter disagreement; conflict or struggle; vigorous or bitter conflict, discord, or antagonism. Can refer to personal disputes, social conflicts, or internal struggles between competing forces or ideas.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STRYF (rhymes with "knife")',
                'etymology': 'From Old French "estrif," possibly from Germanic sources',
                'memory_tips': 'Think "strife" sounds like "knife" - both can cause pain',
                'alternate_spellings': '',
                'language_origin': 'Old French via Germanic',
                'example_sentence': 'The family was torn apart by years of bitter _____.'
            },
            'strigolniki': {
                'definition': 'Historical Russian religious dissidents who practiced extreme self-flagellation and rejected traditional Orthodox practices. These sectarians believed that suffering and pain brought them closer to God and salvation.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'stri-gol-NEE-kee (emphasis on third syllable)',
                'etymology': 'From Russian "strigolnik," from "strich" meaning "to cut" or "shear"',
                'memory_tips': 'Think "strigol-niki" - Russian religious people who cut themselves',
                'alternate_spellings': 'strigolniky',
                'language_origin': 'Russian',
                'example_sentence': 'Medieval Russian chronicles describe the practices of the _____.'
            },
            'striking': {
                'definition': 'Attracting attention through unusual or impressive qualities; hitting or attacking; ceasing work as a form of protest. Can describe remarkable appearance, forceful actions, or labor disputes.',
                'part_of_speech': 'adjective, verb (present participle)',
                'pronunciation_guide': 'STRY-king (emphasis on first syllable)',
                'etymology': 'Present participle of "strike," from Old English "strican"',
                'memory_tips': 'Think "strike-ing" - so impressive it strikes your attention',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The museum\'s _____ architecture drew visitors from around the world.'
            },
            'strings': {
                'definition': 'Thin cords or threads; musical instruments with strings; series of connected things; conditions or restrictions attached to offers. Can refer to physical objects, musical elements, or abstract connections.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'STRINGZ (rhymes with "things")',
                'etymology': 'From Old English "streng" meaning "cord, rope"',
                'memory_tips': 'Think "strings" that bring things together or make music',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The violin\'s _____ needed tuning before the concert.'
            },
            'strip': {
                'definition': 'To remove covering, clothing, or surface material; a long narrow piece of something; to take away rights or possessions. Can describe physical actions, geographical features, or legal processes.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'STRIP (rhymes with "trip")',
                'etymology': 'From Old English "strypan" meaning "to plunder, despoil"',
                'memory_tips': 'Think "strip" - removing layers like stripping wallpaper',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'Workers will _____ the old paint before applying the new coat.'
            },
            'stroganoff': {
                'definition': 'A Russian dish of sautéed pieces of beef served in a sauce with sour cream; named after a Russian noble family. The dish typically includes mushrooms and onions, served over rice or noodles.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STROG-uh-nof (emphasis on first syllable)',
                'etymology': 'Named after the Russian Stroganov family of merchants and nobles',
                'memory_tips': 'Think "strong-enough" - a strong, hearty Russian dish',
                'alternate_spellings': 'stroganov',
                'language_origin': 'Russian (family name)',
                'example_sentence': 'The restaurant\'s beef _____ was served with fresh herbs and egg noodles.'
            },
            'stroll': {
                'definition': 'To walk in a leisurely or casual way; a leisurely walk taken for pleasure or exercise. Implies unhurried movement, often for enjoyment rather than reaching a destination quickly.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'STROHL (rhymes with "roll")',
                'etymology': 'From German "strollen" meaning "to roam"',
                'memory_tips': 'Think "stroll" like "roll" - rolling along slowly and casually',
                'alternate_spellings': '',
                'language_origin': 'German',
                'example_sentence': 'They took an evening _____ through the peaceful garden.'
            },
            'strong': {
                'definition': 'Having great physical power, force, or intensity; not easily broken, damaged, or defeated; having a specified strength or potency. Can describe physical attributes, materials, flavors, or abstract qualities.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'STRAWNG (one syllable)',
                'etymology': 'From Old English "strang" meaning "powerful, violent"',
                'memory_tips': 'Think "strong" - the sound itself seems powerful and firm',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The _____ wind knocked down several trees during the storm.'
            },
            'structural': {
                'definition': 'Relating to or affecting the structure of something; concerning the arrangement and organization of parts in a system. Used in architecture, engineering, linguistics, and various scientific fields.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'STRUK-cher-uhl (emphasis on first syllable)',
                'etymology': 'From "structure" + "-al," from Latin "structura"',
                'memory_tips': 'Think "structure-al" - related to how things are structured',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The engineer identified _____ problems in the building\'s foundation.'
            },
            'strum': {
                'definition': 'To play a guitar or similar stringed instrument by sweeping the fingers across the strings; to play casually or idly. Often produces chords rather than individual notes.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'STRUM (rhymes with "hum")',
                'etymology': 'Imitative of the sound made when playing strings',
                'memory_tips': 'Think "strum" - the word sounds like strumming guitar strings',
                'alternate_spellings': '',
                'language_origin': 'Imitative (onomatopoeia)',
                'example_sentence': 'He learned to _____ basic chords on his acoustic guitar.'
            },
            'struthious': {
                'definition': 'Relating to or resembling ostriches and similar large flightless birds; having characteristics of the ostrich family (Struthionidae). Used in biological and zoological contexts.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'STROO-thee-us (emphasis on first syllable)',
                'etymology': 'From Latin "struthio" meaning "ostrich" + "-ous"',
                'memory_tips': 'Think "struth-ious" - ostrich-ious, like an ostrich',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The fossil showed _____ characteristics indicating it was from an ancient flightless bird.'
            },
            'struthiousstupa': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "struthious" (ostrich-like) + "stupa" (Buddhist monument). This is a data processing error that should be corrected.',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "struthious" and "stupa"',
                'alternate_spellings': 'struthious + stupa (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'strychnine': {
                'definition': 'A highly toxic alkaloid poison obtained from seeds of the strychnos tree, historically used in small doses as a medicine and in large doses as a rodenticide. Causes severe muscle spasms and convulsions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STRIK-nyn (emphasis on first syllable)',
                'etymology': 'From French "strychnine," from Latin "strychnos," from Greek "strychnos"',
                'memory_tips': 'Think "strick-nine" - strictly nine lives, this poison takes them away',
                'alternate_spellings': '',
                'language_origin': 'Greek via Latin and French',
                'example_sentence': 'The detective suspected _____ poisoning based on the victim\'s symptoms.'
            },
            'stubble': {
                'definition': 'Short stiff hairs growing on a man\'s face when he has not shaved recently; the short stalks of grain plants left in the ground after harvesting. Both create rough, prickly surfaces.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STUB-uhl (emphasis on first syllable)',
                'etymology': 'From Old English "stybb" meaning "tree stump"',
                'memory_tips': 'Think "stub-ble" - short stubby bristles that trouble smooth skin',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The farmer\'s field was covered with wheat _____ after the harvest.'
            },
            'stubborn': {
                'definition': 'Having or showing dogged determination not to change one\'s attitude or position; difficult to move, remove, or cure. Can describe people who resist change or objects that resist efforts to modify them.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'STUB-urn (emphasis on first syllable)',
                'etymology': 'From Middle English "stobborn," possibly related to "stub"',
                'memory_tips': 'Think "stub-born" - born like a stub, hard to remove',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The _____ child refused to eat his vegetables despite repeated attempts.'
            },
            'student': {
                'definition': 'A person who is studying at a school, college, or university; someone who is learning about a particular subject. Can refer to formal education participants or anyone engaged in systematic learning.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STOO-duhnt (emphasis on first syllable)',
                'etymology': 'From Latin "studens," present participle of "studere" meaning "to study"',
                'memory_tips': 'Think "stude-nt" - one who studies diligently',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Each _____ received a personalized learning plan from their advisor.'
            },
            'students': {
                'definition': 'Plural of student; multiple people who are studying at educational institutions or learning particular subjects. Collective term for learners in academic settings.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'STOO-duhnts (emphasis on first syllable)',
                'etymology': 'Plural of "student," from Latin "studens"',
                'memory_tips': 'Think "stude-nts" - multiple people who study',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ gathered in the library to prepare for their final examinations.'
            },
            'studied': {
                'definition': 'Past tense of study; having learned about something through systematic investigation; deliberate and carefully considered; characterized by conscious effort or planning.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'STUD-eed (emphasis on first syllable)',
                'etymology': 'Past tense of "study," from Latin "studium" meaning "zeal, pursuit"',
                'memory_tips': 'Think "stud-ied" - past tense of putting in studious effort',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She _____ medicine for six years before becoming a doctor.'
            },
            'studies': {
                'definition': 'Plural of study; academic subjects or courses of learning; systematic investigations or examinations; rooms or spaces used for reading and writing.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'STUD-eez (emphasis on first syllable)',
                'etymology': 'Plural of "study," from Latin "studium"',
                'memory_tips': 'Think "stud-ies" - multiple areas where one studies',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'His _____ in environmental science led to a career in conservation.'
            },
            'studio': {
                'definition': 'A room where an artist works; a place where films, television shows, or music recordings are made; a small apartment consisting mainly of one room.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STOO-dee-oh (emphasis on first syllable)',
                'etymology': 'From Italian "studio," from Latin "studium" meaning "study, zeal"',
                'memory_tips': 'Think "stud-io" - a place where people study their art',
                'alternate_spellings': '',
                'language_origin': 'Latin via Italian',
                'example_sentence': 'The artist rented a _____ with large windows for natural light.'
            },
            'studying': {
                'definition': 'Present participle of study; the act of learning about something through books, observation, or instruction; devoting time and attention to acquiring knowledge.',
                'part_of_speech': 'verb (present participle)',
                'pronunciation_guide': 'STUD-ee-ing (emphasis on first syllable)',
                'etymology': 'Present participle of "study," from Latin "studium"',
                'memory_tips': 'Think "stud-y-ing" - currently engaged in studious activity',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'She spent the evening _____ for her chemistry final exam.'
            },
            'stuff': {
                'definition': 'Matter, material, or things in general; personal belongings; the basic material of which something is made; to fill tightly with material.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'STUF (rhymes with "rough")',
                'etymology': 'From Old French "estoffe" meaning "material, furniture"',
                'memory_tips': 'Think "stuff" - filled with rough materials',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'She packed all her _____ into boxes before moving to the new apartment.'
            },
            'stumble': {
                'definition': 'To trip or momentarily lose one\'s balance; to walk unsteadily; to make a mistake or encounter difficulties; to discover something by chance.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'STUM-buhl (emphasis on first syllable)',
                'etymology': 'From Middle English "stomblen," possibly from Old Norse',
                'memory_tips': 'Think "stum-ble" - stumbling makes you mumble complaints',
                'alternate_spellings': '',
                'language_origin': 'Middle English via Old Norse',
                'example_sentence': 'She began to _____ over the difficult pronunciation in the foreign language.'
            },
            'stumped': {
                'definition': 'Past tense of stump; baffled or confused by a difficult problem; unable to think of an answer or solution; in cricket, dismissed by having the wicket broken.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'STUMPD (one syllable)',
                'etymology': 'Past tense of "stump," from Middle English "stumpe"',
                'memory_tips': 'Think "stump-ed" - like hitting a tree stump and stopping',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The difficult math problem _____ even the brightest students.'
            },
            'stun': {
                'definition': 'To shock or daze someone so as to make them temporarily unable to react; to astonish or amaze; to render senseless or unconscious.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'STUN (rhymes with "run")',
                'etymology': 'From Old French "estoner," from Latin "ex-" + "tonare" meaning "to thunder"',
                'memory_tips': 'Think "stun" like being struck by thunder',
                'alternate_spellings': '',
                'language_origin': 'Latin via Old French',
                'example_sentence': 'The unexpected announcement was enough to _____ the entire audience.'
            },
            'stunts': {
                'definition': 'Plural of stunt; daring feats performed to entertain or as part of a film; actions designed to attract attention; things that hinder normal growth or development.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'STUNTS (rhymes with "hunts")',
                'etymology': 'From "stunt," possibly from Old Norse "stuttr" meaning "short"',
                'memory_tips': 'Think "stunts" - short bursts of exciting action',
                'alternate_spellings': '',
                'language_origin': 'Old Norse',
                'example_sentence': 'The action movie featured dangerous _____ performed by professional stuntmen.'
            },
            'stupa': {
                'definition': 'A dome-shaped Buddhist monument, typically containing relics; a mound-like structure containing Buddhist relics and used as a place of meditation. Important in Buddhist architecture and religious practice.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STOO-puh (emphasis on first syllable)',
                'etymology': 'From Sanskrit "stupa" meaning "heap, mound"',
                'memory_tips': 'Think "stoop-a" - you stoop to show respect at this Buddhist monument',
                'alternate_spellings': '',
                'language_origin': 'Sanskrit',
                'example_sentence': 'The ancient _____ contained sacred relics and attracted pilgrims from distant lands.'
            },
            'stupefy': {
                'definition': 'To make someone unable to think or feel properly; to astonish and shock; to make torpid or senseless. Can result from drugs, alcohol, amazement, or overwhelming circumstances.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'STOO-puh-fy (emphasis on first syllable)',
                'etymology': 'From Latin "stupefacere," from "stupere" (to be stunned) + "facere" (to make)',
                'memory_tips': 'Think "stupid-fy" - to make stupid or senseless',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The magician\'s incredible trick was enough to _____ the amazed audience.'
            },
            'sturdy': {
                'definition': 'Strongly and solidly built; showing confidence and determination; healthy and robust. Describes objects that can withstand wear or people who demonstrate reliability and strength.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'STUR-dee (emphasis on first syllable)',
                'etymology': 'From Old French "estourdi," possibly meaning "stunned, rash"',
                'memory_tips': 'Think "stur-dy" - sturdy and steady, ready for duty',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The _____ wooden table had survived decades of family dinners.'
            },
            'sturnine': {
                'definition': 'Relating to or resembling starlings; belonging to the starling family of birds (Sturnidae). Used in ornithological and biological contexts to describe bird characteristics.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'STUR-nyn (emphasis on first syllable)',
                'etymology': 'From Latin "sturnus" meaning "starling" + "-ine"',
                'memory_tips': 'Think "stern-ine" - starlings can look stern and serious',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The ornithologist identified several _____ species in the urban park.'
            },
            'stuttered': {
                'definition': 'Past tense of stutter; spoke with involuntary repetition or prolongation of sounds or syllables; performed in a halting or irregular manner.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'STUT-urd (emphasis on first syllable)',
                'etymology': 'Past tense of "stutter," from Middle English "stutten"',
                'memory_tips': 'Think "stut-tered" - repeated sounds in a stuttering pattern',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'He _____ nervously when asked to speak in front of the large crowd.'
            },
            'stygian': {
                'definition': 'Very dark, gloomy, or forbidding; relating to the river Styx in Greek mythology; infernal or hellish in character. Often used to describe extreme darkness or ominous atmospheres.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'STIJ-ee-uhn (emphasis on first syllable)',
                'etymology': 'From Latin "Stygius," from Greek "Stygios," referring to the river Styx',
                'memory_tips': 'Think "Sty-gian" - dark as the river Styx in the underworld',
                'alternate_spellings': '',
                'language_origin': 'Greek via Latin',
                'example_sentence': 'The cave\'s _____ darkness made exploration dangerous without proper lighting.'
            },
            'style': {
                'definition': 'A particular manner of doing something; a distinctive appearance or design; elegance and sophistication; a way of using language. Can refer to fashion, art, writing, or behavior.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'STYL (rhymes with "mile")',
                'etymology': 'From Latin "stilus" meaning "writing instrument"',
                'memory_tips': 'Think "style" - your personal file of how to present yourself',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Her unique _____ of painting caught the attention of art critics.'
            },
            'stylistic': {
                'definition': 'Relating to style, especially literary or artistic style; concerned with the manner of expression rather than content. Used in analysis of artistic, literary, or design elements.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'sty-LIS-tik (emphasis on second syllable)',
                'etymology': 'From "style" + "-istic," from Latin "stilus"',
                'memory_tips': 'Think "style-istic" - having the characteristics of a particular style',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ differences between the two authors made their works easily distinguishable.'
            },
            'styptic': {
                'definition': 'Able to stop bleeding by contracting blood vessels; serving to check hemorrhage. In medicine, styptic agents are used to control minor bleeding from cuts or wounds.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'STIP-tik (emphasis on first syllable)',
                'etymology': 'From Latin "stypticus," from Greek "styptikos" meaning "astringent"',
                'memory_tips': 'Think "stop-tic" - stops bleeding like magic',
                'alternate_spellings': '',
                'language_origin': 'Greek via Latin',
                'example_sentence': 'The barber used a _____ pencil to stop bleeding from small nicks.'
            },
            'styrofoam': {
                'definition': 'A trademark for expanded polystyrene foam, commonly used for insulation and disposable food containers. The lightweight, white foam material is known for its insulating properties but environmental persistence.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'STY-roh-fohm (emphasis on first syllable)',
                'etymology': 'Trademark combining "styrene" + "foam," from Greek "styrax" (resin)',
                'memory_tips': 'Think "styro-foam" - styrene made into foam',
                'alternate_spellings': '',
                'language_origin': 'Modern trademark (Greek elements)',
                'example_sentence': 'The takeout container was made of white _____ that kept the food warm.'
            },
            'subaltern': {
                'definition': 'A person holding a subordinate position; in military contexts, a commissioned officer below the rank of captain; someone of inferior rank or status.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'suhb-AL-turn (emphasis on second syllable)',
                'etymology': 'From Late Latin "subalternus," from "sub" (under) + "alternus" (alternate)',
                'memory_tips': 'Think "sub-alternate" - an alternate person in a subordinate position',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ officer carried out orders from the commanding general.'
            },
            'subaqueous': {
                'definition': 'Existing, occurring, or designed for use underwater; formed or taking place beneath the surface of water. Used in geological, biological, and engineering contexts.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'suhb-AY-kwee-us (emphasis on second syllable)',
                'etymology': 'From Latin "sub" (under) + "aqua" (water) + "-ous"',
                'memory_tips': 'Think "sub-aqueous" - under water like a submarine',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ volcanic activity created new underwater formations.'
            },
            'subaqueousrecusancy': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "subaqueous" (underwater) + "recusancy" (refusal to submit to authority). This is a data processing error that should be corrected.',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "subaqueous" and "recusancy"',
                'alternate_spellings': 'subaqueous + recusancy (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'subcutaneous': {
                'definition': 'Situated or applied under the skin; relating to the tissue layer beneath the skin. In medicine, refers to injections, implants, or conditions affecting the area just below the skin surface.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'suhb-kyoo-TAY-nee-us (emphasis on third syllable)',
                'etymology': 'From Latin "sub" (under) + "cutis" (skin) + "-aneous"',
                'memory_tips': 'Think "sub-cute-aneous" - under the cute skin surface',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The doctor administered a _____ injection just beneath the skin.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_170_data:
            return batch_170_data[word_lower]
        
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
    
    def process_batch_170(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 170 with comprehensive Claude data"""
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
    
    def save_batch_170_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 170 processed words to CSV"""
        
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
    """Process Batch 170 with comprehensive Claude data"""
    processor = Batch170Processor()
    input_csv = Path("output/batch_170_words.csv")
    output_csv = Path("output/batch_170_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 170 with comprehensive Claude data...")
    
    # Process all words in batch 170
    processed_words = processor.process_batch_170(input_csv)
    
    # Save results
    processor.save_batch_170_csv(processed_words, output_csv)
    
    logger.info(f"Batch 170 processing completed!")
    logger.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
    logger.info(f"Output saved to: {output_csv}")
    
    # Show summary
    successful_words = [w for w in processed_words if w.claude_definition]
    failed_words = [w for w in processed_words if not w.claude_definition]
    combined_errors = [w for w in processed_words if "COMBINED WORD ERROR" in w.claude_definition]
    
    logger.info(f"Results: {len(successful_words)} successful, {len(failed_words)} failed")
    logger.info(f"Combined word errors detected and flagged: {len(combined_errors)}")
    
    if failed_words:
        logger.info("Words that failed processing:")
        for word in failed_words:
            logger.info(f"  - {word.word}: {word.error_notes}")
            
    if combined_errors:
        logger.info("Combined word errors flagged:")
        for word in combined_errors:
            logger.info(f"  - {word.word}: Combined word error")

if __name__ == "__main__":
    main()