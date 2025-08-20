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

class Batch008Processor:
    def __init__(self):
        self.word_data = {
            "amulet": {
                "definition": "A small ornament or piece of jewelry thought to give protection against evil, danger, or disease; a charm worn as protection.",
                "example_sentence": "The ancient warrior wore a protective _____ around his neck before battle.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AM-yuh-lit (emphasis on first syllable)",
                "etymology": "From Latin 'amuletum', possibly from Arabic 'hamala' meaning 'to carry'",
                "memory_tips": "Think 'am-u-let' - something that lets you be protected",
                "language_origin": "Latin"
            },
            "amuse": {
                "definition": "To cause someone to find something funny; to entertain or occupy in a light-hearted way.",
                "example_sentence": "The comedian's jokes never failed to _____ the audience.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-MYOOZ (emphasis on second syllable)",
                "etymology": "From Old French 'amuser', from 'muser' meaning 'to stare stupidly'",
                "memory_tips": "Think 'a-muse' - to inspire like a muse, but for fun",
                "language_origin": "French"
            },
            "amusedpouch": {
                "definition": "COMBINED WORD ERROR - appears to be 'amused' + 'pouch' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "amusement": {
                "definition": "The feeling of finding something funny; entertainment or enjoyment derived from something.",
                "example_sentence": "The children's laughter filled the _____ park with joy.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-MYOOZ-munt (emphasis on second syllable)",
                "etymology": "From French 'amusement', from 'amuser' meaning 'to entertain'",
                "memory_tips": "Think 'amuse-ment' - the state of being amused",
                "language_origin": "French"
            },
            "amygdala": {
                "definition": "An almond-shaped region in the brain that processes emotions, particularly fear and anxiety.",
                "example_sentence": "The _____ plays a crucial role in the brain's fear response system.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-MIG-duh-luh (emphasis on second syllable)",
                "etymology": "From Greek 'amygdale' meaning 'almond', referring to its shape",
                "memory_tips": "Think 'almond-dala' - it's almond-shaped in the brain",
                "language_origin": "Greek"
            },
            "anabathmoi": {
                "definition": "Songs of ascent; specifically, Psalms 120-134 in the Bible, traditionally sung by pilgrims ascending to Jerusalem.",
                "example_sentence": "The pilgrims chanted the _____ as they climbed toward the holy city.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-uh-BATH-moy (emphasis on third syllable)",
                "etymology": "From Greek 'anabathmos' meaning 'a going up, ascent'",
                "memory_tips": "Think 'ana-bath-moi' - ascending songs or steps upward",
                "language_origin": "Greek"
            },
            "anabolic": {
                "definition": "Relating to metabolic processes that build up organs and tissues; constructive metabolism.",
                "example_sentence": "The athlete used _____ steroids to increase muscle mass.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "an-uh-BOL-ik (emphasis on third syllable)",
                "etymology": "From Greek 'anabole' meaning 'a throwing up, mound'",
                "memory_tips": "Think 'ana-bolic' - building up (ana = up, bolic = throwing)",
                "language_origin": "Greek"
            },
            "anabolicjimberjawed": {
                "definition": "COMBINED WORD ERROR - appears to be 'anabolic' + 'jimberjawed' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "anachronism": {
                "definition": "Something belonging to a period other than that in which it exists; a chronological inconsistency.",
                "example_sentence": "The wristwatch in the medieval painting was an obvious _____.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-NAK-ruh-niz-um (emphasis on second syllable)",
                "etymology": "From Greek 'ana' (backward) + 'chronos' (time)",
                "memory_tips": "Think 'ana-chron-ism' - against time, out of place in time",
                "language_origin": "Greek"
            },
            "anaemic": {
                "definition": "British spelling of anemic; lacking in color, spirit, or vitality; suffering from anemia.",
                "example_sentence": "The patient's _____ condition required immediate medical attention.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "uh-NEE-mik (emphasis on second syllable)",
                "etymology": "From Greek 'anaimia', from 'an-' (without) + 'haima' (blood)",
                "memory_tips": "Think 'an-aemic' - without blood, lacking vitality",
                "language_origin": "Greek"
            },
            "anaglyphy": {
                "definition": "The art of carving or embossing in low relief; decorative raised work on metal or other materials.",
                "example_sentence": "The ancient coin showed beautiful _____ work around its edges.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-NAG-luh-fee (emphasis on second syllable)",
                "etymology": "From Greek 'anaglyphos' meaning 'carved in relief'",
                "memory_tips": "Think 'ana-glyph-y' - carving upward, raised carving",
                "language_origin": "Greek"
            },
            "anagrams": {
                "definition": "Words or phrases formed by rearranging the letters of another word or phrase.",
                "example_sentence": "The students enjoyed solving _____ like 'listen' and 'silent'.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AN-uh-grams (emphasis on first syllable)",
                "etymology": "From Greek 'ana' (up, back) + 'gramma' (letter)",
                "memory_tips": "Think 'ana-grams' - letters turned back or rearranged",
                "language_origin": "Greek"
            },
            "analects": {
                "definition": "A collection of short literary or philosophical extracts; specifically, the collected sayings of Confucius.",
                "example_sentence": "Students of philosophy often study the _____ of ancient wisdom.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AN-uh-lekts (emphasis on first syllable)",
                "etymology": "From Greek 'analekta' meaning 'things gathered up'",
                "memory_tips": "Think 'ana-lects' - collected selections or readings",
                "language_origin": "Greek"
            },
            "analepsis": {
                "definition": "A literary device; a flashback or return to an earlier point in a narrative.",
                "example_sentence": "The novel's _____ revealed the character's traumatic childhood.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-uh-LEP-sis (emphasis on third syllable)",
                "etymology": "From Greek 'analepsis' meaning 'a taking up again'",
                "memory_tips": "Think 'ana-lepsis' - taking up again, going back in time",
                "language_origin": "Greek"
            },
            "analepsisanalgesia": {
                "definition": "COMBINED WORD ERROR - appears to be 'analepsis' + 'analgesia' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "analgesia": {
                "definition": "The absence of the sense of pain while remaining conscious; pain relief without loss of consciousness.",
                "example_sentence": "The medication provided effective _____ during the procedure.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-ul-JEE-zhuh (emphasis on third syllable)",
                "etymology": "From Greek 'an-' (without) + 'algesis' (sense of pain)",
                "memory_tips": "Think 'an-algesia' - without pain sensation",
                "language_origin": "Greek"
            },
            "ananya": {
                "definition": "A Sanskrit name meaning 'unique' or 'incomparable'; also refers to devotion without duality in Hindu philosophy.",
                "example_sentence": "In Hindu philosophy, _____ represents undivided devotion to the divine.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-NAHN-yah (emphasis on second syllable)",
                "etymology": "From Sanskrit 'ananya' meaning 'not other, unique'",
                "memory_tips": "Think 'an-anya' - not any other, unique and incomparable",
                "language_origin": "Sanskrit"
            },
            "anaphylaxis": {
                "definition": "A severe, life-threatening allergic reaction that can occur rapidly after exposure to an allergen.",
                "example_sentence": "The bee sting triggered severe _____ requiring immediate medical intervention.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-uh-fuh-LAK-sis (emphasis on fourth syllable)",
                "etymology": "From Greek 'ana' (against) + 'phylaxis' (protection)",
                "memory_tips": "Think 'ana-phylaxis' - against protection, body turning against itself",
                "language_origin": "Greek"
            },
            "anathema": {
                "definition": "Something or someone that is detested or shunned; a formal curse or excommunication.",
                "example_sentence": "Violence was _____ to her peaceful philosophy of life.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-NATH-uh-muh (emphasis on second syllable)",
                "etymology": "From Greek 'anathema' meaning 'something devoted to evil'",
                "memory_tips": "Think 'ana-thema' - something set against, cursed or hated",
                "language_origin": "Greek"
            },
            "anatomical": {
                "definition": "Relating to the structure of living organisms; pertaining to anatomy.",
                "example_sentence": "The medical student studied _____ diagrams of the human heart.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "an-uh-TOM-ik-ul (emphasis on third syllable)",
                "etymology": "From Greek 'anatomikos', from 'anatome' (dissection)",
                "memory_tips": "Think 'anatom-ical' - relating to body structure and dissection",
                "language_origin": "Greek"
            },
            "ancho": {
                "definition": "A type of dried poblano pepper used in Mexican cuisine; dark reddish-brown with mild to moderate heat.",
                "example_sentence": "The chef added _____ peppers to give the sauce a smoky flavor.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AHN-cho (emphasis on first syllable)",
                "etymology": "From Spanish 'ancho' meaning 'wide', referring to the pepper's broad shape",
                "memory_tips": "Think 'ancho' - wide pepper, broad and flavorful",
                "language_origin": "Spanish"
            },
            "anchorage": {
                "definition": "A place where a ship can anchor safely; the action of securing something firmly.",
                "example_sentence": "The harbor provided safe _____ for ships during the storm.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ANG-kur-ij (emphasis on first syllable)",
                "etymology": "From Old French 'ancrage', from 'ancrer' (to anchor)",
                "memory_tips": "Think 'anchor-age' - place for anchoring ships",
                "language_origin": "French"
            },
            "ancien": {
                "definition": "French word meaning 'former' or 'ancient'; used in historical contexts like 'ancien régime'.",
                "example_sentence": "The _____ régime was overthrown during the French Revolution.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "ahn-see-AHN (French pronunciation)",
                "etymology": "From Latin 'ante' meaning 'before'",
                "memory_tips": "Think 'ancien' - ancient, from before current times",
                "language_origin": "French"
            },
            "ancient": {
                "definition": "Very old; belonging to the distant past; having existed for a very long time.",
                "example_sentence": "The archaeologists discovered _____ pottery shards from 3000 BCE.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "AYN-shunt (emphasis on first syllable)",
                "etymology": "From Old French 'ancien', from Latin 'ante' (before)",
                "memory_tips": "Think 'ancient' - from way before current times",
                "language_origin": "Latin"
            },
            "ancillary": {
                "definition": "Providing necessary support to the primary activities of an organization; auxiliary or supplementary.",
                "example_sentence": "The hospital's _____ services include physical therapy and nutrition counseling.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "AN-suh-ler-ee (emphasis on first syllable)",
                "etymology": "From Latin 'ancillaris', from 'ancilla' (female servant)",
                "memory_tips": "Think 'ancillary' - like a servant, supporting the main work",
                "language_origin": "Latin"
            },
            "andalusian": {
                "definition": "Relating to Andalusia, a region in southern Spain; a breed of horse originating from this region.",
                "example_sentence": "The elegant _____ horse pranced gracefully around the ring.",
                "part_of_speech": "adjective/noun",
                "pronunciation_guide": "an-duh-LOO-zhun (emphasis on third syllable)",
                "etymology": "From Arabic 'al-Andalus', the Muslim name for the Iberian Peninsula",
                "memory_tips": "Think 'Andalusian' - from Andalusia in southern Spain",
                "language_origin": "Arabic"
            },
            "andeanscrawled": {
                "definition": "COMBINED WORD ERROR - appears to be 'Andean' + 'scrawled' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "andouille": {
                "definition": "A type of smoked sausage made from pork and seasonings, popular in Cajun and Creole cuisine.",
                "example_sentence": "The chef added _____ sausage to the jambalaya for authentic flavor.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-DOO-ee or ahn-DWEE (French pronunciation)",
                "etymology": "From French 'andouille', possibly from Latin 'inductilia' (things stuffed in)",
                "memory_tips": "Think 'andouille' - a special French sausage with distinctive flavor",
                "language_origin": "French"
            },
            "andromeda": {
                "definition": "A constellation in the northern sky; also refers to a genus of flowering shrubs in the heath family.",
                "example_sentence": "The astronomer pointed out the _____ constellation in the night sky.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-DROM-uh-duh (emphasis on second syllable)",
                "etymology": "From Greek mythology, named after the princess Andromeda",
                "memory_tips": "Think 'Andromeda' - the chained princess in Greek mythology",
                "language_origin": "Greek"
            },
            "anecdotes": {
                "definition": "Short, amusing or interesting stories about real incidents or people.",
                "example_sentence": "The speaker shared humorous _____ from his travels around the world.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AN-ik-doats (emphasis on first syllable)",
                "etymology": "From Greek 'anekdotos' meaning 'unpublished'",
                "memory_tips": "Think 'anecdotes' - little stories shared informally",
                "language_origin": "Greek"
            },
            "anechoic": {
                "definition": "Having minimal echo or reverberation; designed to absorb sound waves.",
                "example_sentence": "The _____ chamber was used for precise acoustic testing.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "an-uh-KOH-ik (emphasis on third syllable)",
                "etymology": "From Greek 'an-' (without) + 'echo' + '-ic'",
                "memory_tips": "Think 'an-echoic' - without echo, sound-absorbing",
                "language_origin": "Greek"
            },
            "anemic": {
                "definition": "Suffering from anemia; lacking in color, spirit, or vitality; weak or feeble.",
                "example_sentence": "The patient appeared pale and _____ after the illness.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "uh-NEE-mik (emphasis on second syllable)",
                "etymology": "From Greek 'anaimia', from 'an-' (without) + 'haima' (blood)",
                "memory_tips": "Think 'an-emic' - without blood, lacking strength",
                "language_origin": "Greek"
            },
            "anemometers": {
                "definition": "Instruments used to measure wind speed and direction in weather monitoring.",
                "example_sentence": "The weather station's _____ recorded wind speeds of 45 mph during the storm.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-uh-MOM-uh-turz (emphasis on third syllable)",
                "etymology": "From Greek 'anemos' (wind) + 'metron' (measure)",
                "memory_tips": "Think 'anemo-meters' - devices that measure wind",
                "language_origin": "Greek"
            },
            "anemone": {
                "definition": "A colorful flowering plant in the buttercup family; also refers to sea anemones, marine animals.",
                "example_sentence": "The garden was filled with bright red _____ flowers in spring.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-NEM-uh-nee (emphasis on second syllable)",
                "etymology": "From Greek 'anemone', from 'anemos' (wind)",
                "memory_tips": "Think 'anemone' - windflower, flowers that dance in the wind",
                "language_origin": "Greek"
            },
            "anent": {
                "definition": "Concerning; with regard to; about (archaic or Scottish usage).",
                "example_sentence": "The discussion _____ the new policy lasted for hours.",
                "part_of_speech": "preposition",
                "pronunciation_guide": "uh-NENT (emphasis on second syllable)",
                "etymology": "From Old English 'on efen' meaning 'on even (ground), alongside'",
                "memory_tips": "Think 'anent' - alongside, concerning a topic",
                "language_origin": "Old English"
            },
            "angiitis": {
                "definition": "Medical term for inflammation of blood vessels; also called vasculitis.",
                "example_sentence": "The patient was diagnosed with _____ affecting the small blood vessels.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-jee-EYE-tis (emphasis on third syllable)",
                "etymology": "From Greek 'angeion' (vessel) + '-itis' (inflammation)",
                "memory_tips": "Think 'angi-itis' - inflammation of blood vessels",
                "language_origin": "Greek"
            },
            "anglophile": {
                "definition": "A person who admires England, its people, culture, and customs.",
                "example_sentence": "As an _____, she collected British antiques and studied English literature.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ANG-gluh-fyle (emphasis on first syllable)",
                "etymology": "From 'Anglo' (English) + Greek 'philos' (loving)",
                "memory_tips": "Think 'Anglo-phile' - lover of English things",
                "language_origin": "Greek/English"
            },
            "angolacontours": {
                "definition": "COMBINED WORD ERROR - appears to be 'Angola' + 'contours' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "angora": {
                "definition": "A soft fiber obtained from Angora goats or rabbits; fabric made from this fiber.",
                "example_sentence": "The luxurious _____ sweater felt incredibly soft against her skin.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ang-GOR-uh (emphasis on second syllable)",
                "etymology": "From Ankara (formerly Angora), Turkey, where the fiber originated",
                "memory_tips": "Think 'Angora' - soft fiber from Ankara, Turkey",
                "language_origin": "Turkish"
            },
            "angry": {
                "definition": "Feeling or showing strong displeasure or hostility; having a strong feeling of annoyance.",
                "example_sentence": "She became _____ when she discovered the broken vase.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "ANG-gree (emphasis on first syllable)",
                "etymology": "From Old Norse 'angr' meaning 'grief, sorrow'",
                "memory_tips": "Think 'angry' - filled with displeasure or rage",
                "language_origin": "Old Norse"
            },
            "anguish": {
                "definition": "Severe mental or physical pain or suffering; extreme distress.",
                "example_sentence": "The mother's _____ was evident as she waited for news of her child.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ANG-gwish (emphasis on first syllable)",
                "etymology": "From Old French 'angoisse', from Latin 'angustia' (tightness)",
                "memory_tips": "Think 'anguish' - tightness of heart, severe emotional pain",
                "language_origin": "Latin"
            },
            "angularconcomitant": {
                "definition": "COMBINED WORD ERROR - appears to be 'angular' + 'concomitant' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "angus": {
                "definition": "A breed of beef cattle originally from Scotland, known for high-quality meat.",
                "example_sentence": "The rancher raised _____ cattle for their excellent marbled beef.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ANG-gus (emphasis on first syllable)",
                "etymology": "From Angus, a county in Scotland where the breed originated",
                "memory_tips": "Think 'Angus' - quality beef cattle from Scotland",
                "language_origin": "Scottish"
            },
            "anhinga": {
                "definition": "A large waterbird with a long neck and pointed bill, also called a darter or snakebird.",
                "example_sentence": "The _____ spread its wings to dry after diving for fish.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-HING-guh (emphasis on second syllable)",
                "etymology": "From Tupi (Brazilian indigenous language) 'anhinga'",
                "memory_tips": "Think 'anhinga' - the snakebird with the long diving neck",
                "language_origin": "Tupi"
            },
            "anicca": {
                "definition": "A Buddhist concept meaning impermanence; the idea that all things are transitory.",
                "example_sentence": "In Buddhism, _____ teaches that nothing remains unchanged forever.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ah-NEE-cha (emphasis on second syllable)",
                "etymology": "From Pali 'anicca', from Sanskrit 'anitya' (impermanent)",
                "memory_tips": "Think 'anicca' - nothing remains constant, all is changing",
                "language_origin": "Pali/Sanskrit"
            },
            "animal": {
                "definition": "A living organism that feeds on organic matter and can move independently.",
                "example_sentence": "Every _____ in the zoo receives specialized care from trained keepers.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AN-uh-mul (emphasis on first syllable)",
                "etymology": "From Latin 'animalis', from 'anima' (breath, soul)",
                "memory_tips": "Think 'animal' - living creature with breath and soul",
                "language_origin": "Latin"
            },
            "animalier": {
                "definition": "An artist who specializes in depicting animals; pertaining to animal art.",
                "example_sentence": "The famous _____ captured the grace of wild horses in bronze sculptures.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-uh-muh-LEER (emphasis on fourth syllable)",
                "etymology": "From French 'animalier', from 'animal'",
                "memory_tips": "Think 'animal-ier' - one who creates animal art",
                "language_origin": "French"
            },
            "animals": {
                "definition": "Plural of animal; living organisms that can move and feed on other organisms.",
                "example_sentence": "The documentary showed how _____ adapt to changing environments.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AN-uh-mulz (emphasis on first syllable)",
                "etymology": "From Latin 'animalis', from 'anima' (breath, soul)",
                "memory_tips": "Think 'animals' - multiple living creatures with souls",
                "language_origin": "Latin"
            },
            "animatronics": {
                "definition": "The technology of creating lifelike robotic figures that can move and appear alive.",
                "example_sentence": "The theme park's dinosaur exhibit featured impressive _____ that amazed visitors.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-uh-muh-TRON-iks (emphasis on fourth syllable)",
                "etymology": "Blend of 'animate' + 'electronics'",
                "memory_tips": "Think 'animate-tronics' - electronic animation of figures",
                "language_origin": "Modern English"
            },
            "anime": {
                "definition": "A style of Japanese animation characterized by distinctive art and storytelling techniques.",
                "example_sentence": "The popular _____ series attracted millions of fans worldwide.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AN-uh-may (emphasis on first syllable)",
                "etymology": "From Japanese 'anime', borrowed from English 'animation'",
                "memory_tips": "Think 'anime' - Japanese animated entertainment",
                "language_origin": "Japanese"
            }
        }
        
        # Combined word errors detected in this batch
        self.combined_word_errors = [
            "amusedpouch",
            "anabolicjimberjawed", 
            "analepsisanalgesia",
            "andeanscrawled",
            "angolacontours",
            "angularconcomitant"
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
    processor = Batch008Processor()
    input_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_008_words.csv"
    output_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_008_processed.csv"
    
    processor.process_batch(input_file, output_file)
    
    print(f"\nBatch 008 Processing Complete!")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Combined word errors flagged: {len(processor.combined_word_errors)}")

if __name__ == "__main__":
    main()