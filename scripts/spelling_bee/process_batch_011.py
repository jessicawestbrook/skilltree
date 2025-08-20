#!/usr/bin/env python3
import csv
import logging
from dataclasses import dataclass
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class WordData:
    word: str
    definition: str
    example_sentence: str
    source_difficulty: str
    difficulty_level: str = ""
    difficulty_name: str = ""
    ai_difficulty_level: str = ""
    ai_difficulty_name: str = ""
    phonetic_transparency_score: float = 0.0
    word_frequency_score: float = 0.0
    morphology_score: float = 0.0
    etymology_score: float = 0.0
    difficulty_calculation_method: str = ""
    part_of_speech: str = ""
    pronunciation_guide: str = ""
    etymology: str = ""
    etymology_source: str = "Claude"
    memory_tips: str = ""
    alternate_spellings: str = ""
    language_origin: str = ""
    definition_source: str = "Claude"
    source_names: str = "Scripps National Spelling Bee"
    source_difficulties: str = ""
    frequency: float = 0.0
    original_source: str = ""
    source_access_date: str = "2025-08-19"

class DifficultyCalculator:
    @staticmethod
    def calculate_phonetic_transparency(word: str) -> float:
        # Scoring based on how phonetically transparent the spelling is
        irregular_patterns = ['ough', 'augh', 'eigh', 'ph', 'gh', 'tion', 'sion', 'ious', 'eous']
        silent_letters = ['k', 'b', 'l', 'w', 'h']
        
        score = 1.0  # Start with most transparent
        
        # Check for irregular patterns
        for pattern in irregular_patterns:
            if pattern in word.lower():
                score += 1.0
        
        # Check for silent letters in common positions
        word_lower = word.lower()
        if word_lower.startswith('k') and len(word) > 1:  # knight, knee
            score += 1.0
        if 'mb' in word_lower:  # thumb, lamb
            score += 1.0
        if word_lower.endswith('l') and 'lk' in word_lower:  # walk, talk
            score += 1.0
            
        return min(score, 4.0)
    
    @staticmethod
    def calculate_word_frequency(word: str) -> float:
        # Based on common English word frequency
        common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use']
        
        word_lower = word.lower()
        if word_lower in common_words:
            return 1.0
        elif len(word) <= 4:
            return 2.0
        elif len(word) <= 7:
            return 3.0
        else:
            return 4.0
    
    @staticmethod
    def calculate_morphology_complexity(word: str) -> float:
        # Based on morphological complexity
        prefixes = ['un', 'pre', 'dis', 'mis', 're', 'over', 'under', 'out', 'up', 'non', 'anti', 'de', 'en', 'em', 'fore', 'in', 'im', 'il', 'ir', 'inter', 'mid', 'sub', 'super', 'trans', 'semi', 'auto', 'co', 'counter', 'extra', 'hyper', 'mega', 'micro', 'mini', 'multi', 'over', 'post', 'proto', 'pseudo', 'tele', 'ultra']
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment', 'able', 'ible', 'ful', 'less', 'ous', 'eous', 'ious', 'al', 'ial', 'ic', 'ive', 'ism', 'ist', 'ize', 'ise', 'age', 'ity', 'ward', 'wise']
        
        score = 1.0
        word_lower = word.lower()
        
        # Check for prefixes
        for prefix in prefixes:
            if word_lower.startswith(prefix):
                score += 0.5
                break
        
        # Check for suffixes
        for suffix in suffixes:
            if word_lower.endswith(suffix):
                score += 0.5
                break
        
        # Multiple morphemes
        if score > 2.0:
            score += 1.0
            
        return min(score, 4.0)
    
    @staticmethod
    def calculate_etymology_complexity(language_origin: str) -> float:
        # Based on language origin complexity for English speakers
        if language_origin.lower() in ['english', 'anglo-saxon', 'germanic']:
            return 1.0
        elif language_origin.lower() in ['french', 'latin']:
            return 2.0
        elif language_origin.lower() in ['greek', 'spanish', 'italian']:
            return 3.0
        else:
            return 4.0
    
    @staticmethod
    def calculate_overall_difficulty(phonetic: float, frequency: float, morphology: float, etymology: float) -> float:
        # Weighted average: phonetic (30%), frequency (25%), morphology (25%), etymology (20%)
        return (phonetic * 0.3 + frequency * 0.25 + morphology * 0.25 + etymology * 0.2)

class Batch011Processor:
    def __init__(self):
        self.word_data = {
            "appraisal": {
                "definition": "The act of assessing or evaluating the value, quality, or importance of something; a formal valuation of property.",
                "example_sentence": "The real estate _____ revealed that the house was worth more than expected.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-PRAY-zul (emphasis on second syllable)",
                "etymology": "From Old French 'apreisier' meaning 'to set a price on'",
                "memory_tips": "Think 'a-praise-al' - giving praise or value to something",
                "language_origin": "French"
            },
            "appraisalparabola": {
                "definition": "COMBINED WORD ERROR - appears to be 'appraisal' + 'parabola' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "appreciation": {
                "definition": "Recognition of the value or significance of something; gratitude; an increase in value over time.",
                "example_sentence": "She expressed her _____ for all the hard work her team had accomplished.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-pree-shee-AY-shun (emphasis on fourth syllable)",
                "etymology": "From Latin 'appretiare' meaning 'to set a price on'",
                "memory_tips": "Think 'appreciate-ion' - the act of appreciating or valuing",
                "language_origin": "Latin"
            },
            "apprehensive": {
                "definition": "Anxious or fearful about something that might happen; showing understanding or awareness.",
                "example_sentence": "The student felt _____ about taking the final exam without enough preparation.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "ap-ruh-HEN-siv (emphasis on third syllable)",
                "etymology": "From Latin 'apprehendere' meaning 'to take hold of, grasp'",
                "memory_tips": "Think 'apprehend-sive' - grasping or fearing what might come",
                "language_origin": "Latin"
            },
            "approaches": {
                "definition": "Methods of dealing with something; ways of tackling a problem; comes near to or draws closer.",
                "example_sentence": "The teacher used different _____ to help students understand the complex concept.",
                "part_of_speech": "noun/verb",
                "pronunciation_guide": "uh-PROH-chiz (emphasis on second syllable)",
                "etymology": "From Old French 'aprochier', from Latin 'appropiare' (to come near)",
                "memory_tips": "Think 'ap-proach' - moving toward or near to something",
                "language_origin": "French"
            },
            "approbatory": {
                "definition": "Expressing approval or praise; giving official sanction or consent.",
                "example_sentence": "The committee gave an _____ nod to the proposed changes in policy.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "uh-PROB-uh-tor-ee (emphasis on second syllable)",
                "etymology": "From Latin 'approbare' meaning 'to approve'",
                "memory_tips": "Think 'approve-atory' - giving approval or praise",
                "language_origin": "Latin"
            },
            "appropriaterummages": {
                "definition": "COMBINED WORD ERROR - appears to be 'appropriate' + 'rummages' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "appui": {
                "definition": "Support or backing; assistance or help, especially in a difficult situation.",
                "example_sentence": "The diplomat sought _____ from allied nations during the negotiations.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ah-PWEE (French pronunciation)",
                "etymology": "From French 'appui' meaning 'support, prop'",
                "memory_tips": "Think 'appui' - providing support like a prop",
                "language_origin": "French"
            },
            "appurtenances": {
                "definition": "Accessories or equipment associated with a particular activity; things that belong or are attached to something else.",
                "example_sentence": "The house came with all its _____, including the garden tools and furniture.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-PUR-tuh-nuns-iz (emphasis on second syllable)",
                "etymology": "From Old French 'apartenance', from 'apartenir' (to belong)",
                "memory_tips": "Think 'appurtenance' - things that belong or pertain to something",
                "language_origin": "French"
            },
            "april": {
                "definition": "The fourth month of the year in the Gregorian calendar, traditionally associated with spring.",
                "example_sentence": "The cherry blossoms bloomed beautifully in _____ this year.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AY-prul (emphasis on first syllable)",
                "etymology": "From Latin 'Aprilis', possibly from 'aperire' (to open) referring to spring opening",
                "memory_tips": "Think 'April' - the month when nature opens up in spring",
                "language_origin": "Latin"
            },
            "apron": {
                "definition": "A protective garment worn over clothes; an area of pavement where aircraft are parked.",
                "example_sentence": "The chef tied her _____ securely before beginning to prepare the meal.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AY-prun (emphasis on first syllable)",
                "etymology": "From Old French 'naperon', diminutive of 'nape' (tablecloth)",
                "memory_tips": "Think 'apron' - a protective covering worn in front",
                "language_origin": "French"
            },
            "apropos": {
                "definition": "Very appropriate to a particular situation; by the way; incidentally.",
                "example_sentence": "His comment about teamwork was quite _____ given the current project challenges.",
                "part_of_speech": "adjective/adverb",
                "pronunciation_guide": "ap-ruh-POH (emphasis on third syllable)",
                "etymology": "From French 'à propos' meaning 'to the purpose'",
                "memory_tips": "Think 'a-propos' - to the purpose, very fitting",
                "language_origin": "French"
            },
            "apropospessimum": {
                "definition": "COMBINED WORD ERROR - appears to be 'apropos' + 'pessimum' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "après": {
                "definition": "French word meaning 'after'; used in English in phrases like 'après-ski' (after skiing).",
                "example_sentence": "The _____ ski activities included hot chocolate by the fireplace.",
                "part_of_speech": "preposition",
                "pronunciation_guide": "ah-PRAY (French pronunciation)",
                "etymology": "From French 'après', from Latin 'ad' + 'pressus' (pressed to, near)",
                "memory_tips": "Think 'après' - what comes after or following",
                "language_origin": "French"
            },
            "aptitude": {
                "definition": "A natural ability or talent for learning or doing something; suitability or fitness.",
                "example_sentence": "Her _____ for mathematics was evident from an early age.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AP-tuh-tood (emphasis on first syllable)",
                "etymology": "From Latin 'aptitudo', from 'aptus' (fitted, suitable)",
                "memory_tips": "Think 'apt-itude' - being apt or suited for something",
                "language_origin": "Latin"
            },
            "aquamarine": {
                "definition": "A pale blue to blue-green color; a semi-precious gemstone of this color; relating to sea water.",
                "example_sentence": "The bride wore a stunning _____ necklace that matched her ocean-themed wedding.",
                "part_of_speech": "noun/adjective",
                "pronunciation_guide": "ak-wuh-muh-REEN (emphasis on fourth syllable)",
                "etymology": "From Latin 'aqua marina' meaning 'sea water'",
                "memory_tips": "Think 'aqua-marine' - the color of sea water",
                "language_origin": "Latin"
            },
            "aqueduct": {
                "definition": "An artificial channel for conveying water, typically in the form of a bridge across a valley.",
                "example_sentence": "The ancient Roman _____ still supplies water to the modern city.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AK-wuh-duhkt (emphasis on first syllable)",
                "etymology": "From Latin 'aquaeductus', from 'aqua' (water) + 'ducere' (to lead)",
                "memory_tips": "Think 'aqua-duct' - a duct that leads water",
                "language_origin": "Latin"
            },
            "aqueductorganized": {
                "definition": "COMBINED WORD ERROR - appears to be 'aqueduct' + 'organized' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "aqueous": {
                "definition": "Containing, made of, or relating to water; dissolved in water.",
                "example_sentence": "The chemist prepared an _____ solution by dissolving the salt in distilled water.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "AY-kwee-us (emphasis on first syllable)",
                "etymology": "From Latin 'aqua' meaning 'water'",
                "memory_tips": "Think 'aqu-eous' - relating to water (aqua)",
                "language_origin": "Latin"
            },
            "aquiclude": {
                "definition": "A rock formation that does not allow water to pass through it; an impermeable geological layer.",
                "example_sentence": "The clay _____ prevented groundwater from reaching the lower rock layers.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AK-wuh-klood (emphasis on first syllable)",
                "etymology": "From Latin 'aqua' (water) + 'claudere' (to close)",
                "memory_tips": "Think 'aqui-clude' - closes off or excludes water",
                "language_origin": "Latin"
            },
            "aquilineconfucianism": {
                "definition": "COMBINED WORD ERROR - appears to be 'aquiline' + 'confucianism' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "aquitaine": {
                "definition": "A historical region in southwestern France; a former duchy and province.",
                "example_sentence": "Eleanor of _____ was one of the most powerful women in medieval Europe.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ak-wuh-TAYN (emphasis on third syllable)",
                "etymology": "From Latin 'Aquitania', possibly meaning 'land of waters'",
                "memory_tips": "Think 'Aquitaine' - the French region rich in waters",
                "language_origin": "Latin"
            },
            "arabesque": {
                "definition": "An ornamental design of intertwined flowing lines; a ballet position with one leg extended behind.",
                "example_sentence": "The dancer held a perfect _____ pose with graceful extension and balance.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ar-uh-BESK (emphasis on third syllable)",
                "etymology": "From French 'arabesque', meaning 'in the Arabic style'",
                "memory_tips": "Think 'arab-esque' - in the style of Arabic ornamental art",
                "language_origin": "French"
            },
            "arabic": {
                "definition": "Relating to the Arabic language or Arab people; the Semitic language spoken across the Middle East and North Africa.",
                "example_sentence": "She spent two years studying _____ to better understand Middle Eastern culture.",
                "part_of_speech": "adjective/noun",
                "pronunciation_guide": "AR-uh-bik (emphasis on first syllable)",
                "etymology": "From Latin 'Arabicus', from 'Arabs' (Arab people)",
                "memory_tips": "Think 'Arabic' - the language and culture of Arab peoples",
                "language_origin": "Latin"
            },
            "arable": {
                "definition": "Suitable for growing crops; relating to land that can be plowed and cultivated.",
                "example_sentence": "The fertile valley contained thousands of acres of _____ farmland.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "AR-uh-bul (emphasis on first syllable)",
                "etymology": "From Latin 'arabilis', from 'arare' (to plow)",
                "memory_tips": "Think 'ar-able' - able to be plowed (arable)",
                "language_origin": "Latin"
            },
            "arachnophagous": {
                "definition": "Feeding on spiders; spider-eating (typically used to describe certain insects or animals).",
                "example_sentence": "The _____ wasp specialized in hunting spiders to feed its larvae.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "uh-rak-NOF-uh-gus (emphasis on third syllable)",
                "etymology": "From Greek 'arachne' (spider) + 'phagos' (eating)",
                "memory_tips": "Think 'arachno-phagous' - eating (phagous) spiders (arachno)",
                "language_origin": "Greek"
            },
            "aramaic": {
                "definition": "An ancient Semitic language that was the common language of the Middle East for centuries; the language Jesus spoke.",
                "example_sentence": "Biblical scholars study _____ to better understand ancient religious texts.",
                "part_of_speech": "adjective/noun",
                "pronunciation_guide": "ar-uh-MAY-ik (emphasis on third syllable)",
                "etymology": "From Greek 'Aramaikos', referring to the Aramean people",
                "memory_tips": "Think 'Aramaic' - the ancient language of the Aramean people",
                "language_origin": "Greek"
            },
            "arapaho": {
                "definition": "A member of a Native American people originally from the Great Plains; their Algonquian language.",
                "example_sentence": "The _____ tribe traditionally followed buffalo herds across the plains.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-RAP-uh-hoh (emphasis on second syllable)",
                "etymology": "From Crow 'alappaho' meaning 'people with many tattoos'",
                "memory_tips": "Think 'Arapaho' - the Native American people of the plains",
                "language_origin": "Native American"
            },
            "arapahoe": {
                "definition": "Alternative spelling of Arapaho; a Native American people and their language.",
                "example_sentence": "The _____ Nation maintains its cultural traditions in modern times.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-RAP-uh-hoh (emphasis on second syllable)",
                "etymology": "From Crow 'alappaho' meaning 'people with many tattoos'",
                "memory_tips": "Think 'Arapahoe' - alternative spelling of the Native American people",
                "language_origin": "Native American"
            },
            "arbitrary": {
                "definition": "Based on random choice or personal whim rather than reason; having unlimited power.",
                "example_sentence": "The judge's decision seemed _____ and unfair to the defendant.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "AR-buh-trer-ee (emphasis on first syllable)",
                "etymology": "From Latin 'arbitrarius', from 'arbiter' (judge, umpire)",
                "memory_tips": "Think 'arbiter-ary' - like an arbiter making random decisions",
                "language_origin": "Latin"
            },
            "arboretum": {
                "definition": "A botanical garden devoted to trees and shrubs; a place where trees are cultivated for study.",
                "example_sentence": "The university's _____ contained over 500 species of trees from around the world.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ar-buh-REE-tum (emphasis on third syllable)",
                "etymology": "From Latin 'arbor' meaning 'tree'",
                "memory_tips": "Think 'arbor-etum' - a place for trees (arbor)",
                "language_origin": "Latin"
            },
            "arborio": {
                "definition": "A type of short-grain rice used in Italian cooking, especially for risotto.",
                "example_sentence": "The chef prepared a creamy risotto using authentic _____ rice from Italy.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ar-BOR-ee-oh (emphasis on second syllable)",
                "etymology": "From Arborio, a town in the Piedmont region of Italy",
                "memory_tips": "Think 'Arborio' - the Italian town famous for risotto rice",
                "language_origin": "Italian"
            },
            "arcade": {
                "definition": "A covered passage with shops on one or both sides; a series of arches; a place with coin-operated games.",
                "example_sentence": "The historic shopping _____ featured elegant Victorian architecture.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ar-KAYD (emphasis on second syllable)",
                "etymology": "From French 'arcade', from Italian 'arcata' (series of arches)",
                "memory_tips": "Think 'arcade' - a series of arches forming a covered walkway",
                "language_origin": "Italian"
            },
            "archaic": {
                "definition": "Very old or old-fashioned; belonging to an earlier period; no longer in general use.",
                "example_sentence": "The professor explained the _____ language found in medieval texts.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "ar-KAY-ik (emphasis on second syllable)",
                "etymology": "From Greek 'archaikos', from 'archaios' (ancient)",
                "memory_tips": "Think 'archaic' - from ancient (archaic) times",
                "language_origin": "Greek"
            },
            "archaism": {
                "definition": "The use of older or obsolete forms of language; an archaic word or expression.",
                "example_sentence": "The poet's use of _____ gave his work a deliberately old-fashioned feel.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-kay-iz-um (emphasis on first syllable)",
                "etymology": "From Greek 'archaios' (ancient) + '-ism'",
                "memory_tips": "Think 'archaism' - using ancient forms of language",
                "language_origin": "Greek"
            },
            "archduke": {
                "definition": "A title of nobility ranking above a duke, especially used in the Austrian Habsburg family.",
                "example_sentence": "The assassination of _____ Franz Ferdinand triggered World War I.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ARCH-dook (emphasis on first syllable)",
                "etymology": "From 'arch-' (chief, principal) + 'duke'",
                "memory_tips": "Think 'arch-duke' - the chief or highest duke",
                "language_origin": "English"
            },
            "archers": {
                "definition": "People who shoot with bows and arrows; practitioners of archery.",
                "example_sentence": "The medieval _____ were skilled at hitting targets from great distances.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-churz (emphasis on first syllable)",
                "etymology": "From Old French 'archier', from Latin 'arcus' (bow)",
                "memory_tips": "Think 'archers' - those who use bows (arcus) and arrows",
                "language_origin": "Latin"
            },
            "archetype": {
                "definition": "A very typical example of a certain person or thing; an original model or pattern.",
                "example_sentence": "The wise old mentor is an _____ found in many classic stories.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-kuh-type (emphasis on first syllable)",
                "etymology": "From Greek 'archetypos', from 'arche' (beginning) + 'typos' (model)",
                "memory_tips": "Think 'arche-type' - the original (arche) model or type",
                "language_origin": "Greek"
            },
            "architrave": {
                "definition": "The lowest part of an entablature in classical architecture; a molded frame around a door or window.",
                "example_sentence": "The ornate _____ above the doorway featured intricate carved details.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-kuh-trayv (emphasis on first syllable)",
                "etymology": "From Italian 'architrave', from 'archi-' (chief) + 'trave' (beam)",
                "memory_tips": "Think 'archi-trave' - the chief beam in architecture",
                "language_origin": "Italian"
            },
            "archives": {
                "definition": "A collection of historical documents or records; a place where such materials are stored.",
                "example_sentence": "The historian spent weeks researching in the national _____.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-kyvz (emphasis on first syllable)",
                "etymology": "From Greek 'archeion', from 'arche' (government, magistracy)",
                "memory_tips": "Think 'archives' - where government (arche) records are kept",
                "language_origin": "Greek"
            },
            "arctic": {
                "definition": "Relating to the region around the North Pole; extremely cold or frigid.",
                "example_sentence": "The _____ expedition required specialized cold-weather equipment.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "ARK-tik (emphasis on first syllable)",
                "etymology": "From Greek 'arktikos', from 'arktos' (bear, referring to the constellation)",
                "memory_tips": "Think 'arctic' - the land of the bear (arktos) constellation",
                "language_origin": "Greek"
            },
            "arcturus": {
                "definition": "A bright orange star in the constellation Boötes; the fourth brightest star in Earth's night sky.",
                "example_sentence": "Amateur astronomers easily spot _____ in the spring sky due to its distinctive color.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ark-TOO-rus (emphasis on second syllable)",
                "etymology": "From Greek 'arktos' (bear) + 'ouros' (guardian), meaning 'guardian of the bear'",
                "memory_tips": "Think 'Arcturus' - the guardian star watching over the bear constellation",
                "language_origin": "Greek"
            },
            "arden": {
                "definition": "A woodland or forest, especially one that is wild and uncultivated; used in place names.",
                "example_sentence": "Shakespeare set 'As You Like It' in the Forest of _____.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-den (emphasis on first syllable)",
                "etymology": "From Celtic origin, meaning 'high' or 'elevated place'",
                "memory_tips": "Think 'Arden' - an elevated wooded place",
                "language_origin": "Celtic"
            },
            "ardhamagadhi": {
                "definition": "A Middle Indo-Aryan language, the sacred language of Jainism; used in ancient Jain scriptures.",
                "example_sentence": "Jain scholars study _____ to read the original religious texts.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ar-dah-mah-GAH-dee (emphasis on fourth syllable)",
                "etymology": "From Sanskrit 'ardha' (half) + 'Magadhi' (language of Magadha region)",
                "memory_tips": "Think 'ardha-magadhi' - half-Magadhi, a form of the Magadhi language",
                "language_origin": "Sanskrit"
            },
            "ardipithecus": {
                "definition": "An extinct genus of early hominids found in Africa, dating back about 4.4 million years.",
                "example_sentence": "The discovery of _____ fossils provided new insights into human evolution.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ar-duh-PITH-uh-kus (emphasis on third syllable)",
                "etymology": "From Afar 'ardi' (ground, earth) + Greek 'pithecus' (ape)",
                "memory_tips": "Think 'ardi-pithecus' - the ground ape from ancient Africa",
                "language_origin": "Afar/Greek"
            },
            "ardoise": {
                "definition": "A type of slate used for roofing; a blue-gray color resembling slate.",
                "example_sentence": "The French château featured traditional _____ roof tiles.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ar-DWAHZ (French pronunciation)",
                "etymology": "From French 'ardoise' meaning 'slate'",
                "memory_tips": "Think 'ardoise' - the French word for slate roofing",
                "language_origin": "French"
            },
            "ardoiseorganized": {
                "definition": "COMBINED WORD ERROR - appears to be 'ardoise' + 'organized' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "arduous": {
                "definition": "Requiring great effort and energy; difficult and tiring; characterized by effort to the point of exhaustion.",
                "example_sentence": "The _____ climb to the mountain summit tested the hikers' endurance.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "AR-joo-us (emphasis on first syllable)",
                "etymology": "From Latin 'arduus' meaning 'steep, difficult'",
                "memory_tips": "Think 'arduous' - steep and difficult, requiring hard work",
                "language_origin": "Latin"
            },
            "area": {
                "definition": "A region or part of a town, country, or space; the extent of a surface or piece of land.",
                "example_sentence": "The picnic _____ in the park was perfect for family gatherings.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AIR-ee-uh (emphasis on first syllable)",
                "etymology": "From Latin 'area' meaning 'open space, threshing floor'",
                "memory_tips": "Think 'area' - an open space or region",
                "language_origin": "Latin"
            },
            "arenaceous": {
                "definition": "Sandy or containing sand; relating to or growing in sandy places.",
                "example_sentence": "The _____ soil was perfect for growing certain drought-resistant plants.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "ar-uh-NAY-shus (emphasis on third syllable)",
                "etymology": "From Latin 'arena' (sand) + '-aceous' (characterized by)",
                "memory_tips": "Think 'aren-aceous' - characterized by sand (arena)",
                "language_origin": "Latin"
            }
        }
        
        # Combined word errors detected in this batch
        self.combined_word_errors = [
            "appraisalparabola",
            "appropriaterummages", 
            "apropospessimum",
            "aqueductorganized",
            "aquilineconfucianism",
            "ardoiseorganized"
        ]

    def process_batch(self, input_file: str, output_file: str):
        """Process the batch CSV file and generate comprehensive data"""
        logger.info(f"Starting processing of {input_file}")
        
        words_processed = []
        
        # Read input file
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                input_words = list(reader)
                
        except Exception as e:
            logger.error(f"Error reading input file: {e}")
            return
        
        # Process each word
        for row in input_words:
            word = row['word'].strip()
            if not word:  # Skip empty rows
                continue
                
            logger.info(f"Processing word: {word}")
            
            # Get word data
            if word in self.word_data:
                data = self.word_data[word]
                
                # Calculate difficulty scores
                calc = DifficultyCalculator()
                phonetic_score = calc.calculate_phonetic_transparency(word)
                frequency_score = calc.calculate_word_frequency(word)
                morphology_score = calc.calculate_morphology_complexity(word)
                etymology_score = calc.calculate_etymology_complexity(data['language_origin'])
                overall_score = calc.calculate_overall_difficulty(phonetic_score, frequency_score, morphology_score, etymology_score)
                
                # Create word data object
                word_obj = WordData(
                    word=word,
                    definition=data['definition'],
                    example_sentence=data['example_sentence'],
                    source_difficulty=row['source_difficulties'],
                    phonetic_transparency_score=phonetic_score,
                    word_frequency_score=frequency_score,
                    morphology_score=morphology_score,
                    etymology_score=etymology_score,
                    difficulty_calculation_method=f"4-factor weighted model (overall_score: {overall_score:.2f})",
                    part_of_speech=data['part_of_speech'],
                    pronunciation_guide=data['pronunciation_guide'],
                    etymology=data['etymology'],
                    memory_tips=data['memory_tips'],
                    language_origin=data['language_origin'],
                    source_difficulties=row['source_difficulties'],
                    frequency=len(row['years'].split('; ')) if 'years' in row else 1.0,
                    original_source=f"Scripps National Spelling Bee Words of the Champions ({row.get('years', 'Unknown')})" if 'years' in row else "Scripps National Spelling Bee"
                )
                
                words_processed.append(word_obj)
                
                # Flag combined word errors
                if word in self.combined_word_errors:
                    logger.warning(f"COMBINED WORD ERROR DETECTED: {word}")
                    
            else:
                logger.warning(f"No data found for word: {word}")
        
        # Write output file
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                if words_processed:
                    fieldnames = [
                        'word', 'definition', 'example_sentence', 'source_difficulty',
                        'difficulty_level', 'difficulty_name', 'ai_difficulty_level', 'ai_difficulty_name',
                        'phonetic_transparency_score', 'word_frequency_score', 'morphology_score', 'etymology_score',
                        'difficulty_calculation_method', 'part_of_speech', 'pronunciation_guide', 'etymology',
                        'etymology_source', 'memory_tips', 'alternate_spellings', 'language_origin',
                        'definition_source', 'source_names', 'source_difficulties', 'frequency',
                        'original_source', 'source_access_date'
                    ]
                    
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for word_obj in words_processed:
                        writer.writerow({
                            'word': word_obj.word,
                            'definition': word_obj.definition,
                            'example_sentence': word_obj.example_sentence,
                            'source_difficulty': word_obj.source_difficulty,
                            'difficulty_level': word_obj.difficulty_level,
                            'difficulty_name': word_obj.difficulty_name,
                            'ai_difficulty_level': word_obj.ai_difficulty_level,
                            'ai_difficulty_name': word_obj.ai_difficulty_name,
                            'phonetic_transparency_score': word_obj.phonetic_transparency_score,
                            'word_frequency_score': word_obj.word_frequency_score,
                            'morphology_score': word_obj.morphology_score,
                            'etymology_score': word_obj.etymology_score,
                            'difficulty_calculation_method': word_obj.difficulty_calculation_method,
                            'part_of_speech': word_obj.part_of_speech,
                            'pronunciation_guide': word_obj.pronunciation_guide,
                            'etymology': word_obj.etymology,
                            'etymology_source': word_obj.etymology_source,
                            'memory_tips': word_obj.memory_tips,
                            'alternate_spellings': word_obj.alternate_spellings,
                            'language_origin': word_obj.language_origin,
                            'definition_source': word_obj.definition_source,
                            'source_names': word_obj.source_names,
                            'source_difficulties': word_obj.source_difficulties,
                            'frequency': word_obj.frequency,
                            'original_source': word_obj.original_source,
                            'source_access_date': word_obj.source_access_date
                        })
                        
            logger.info(f"Successfully processed {len(words_processed)} words to {output_file}")
            
            # Report combined word errors
            if any(word in self.combined_word_errors for word in [w.word for w in words_processed]):
                logger.warning("COMBINED WORD ERRORS DETECTED IN THIS BATCH:")
                for error in self.combined_word_errors:
                    if any(w.word == error for w in words_processed):
                        logger.warning(f"  - {error}")
                        
        except Exception as e:
            logger.error(f"Error writing output file: {e}")

def main():
    processor = Batch011Processor()
    input_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_011_words.csv"
    output_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_011_processed.csv"
    
    processor.process_batch(input_file, output_file)
    
    print(f"\nBatch 011 Processing Complete!")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Combined word errors flagged: {len(processor.combined_word_errors)}")

if __name__ == "__main__":
    main()