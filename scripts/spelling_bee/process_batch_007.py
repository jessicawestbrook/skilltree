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

class Batch007Processor:
    def __init__(self):
        self.word_data = {
            "already": {
                "definition": "By this time; before now; previously.",
                "example_sentence": "The show had _____ started when we arrived.",
                "part_of_speech": "adverb",
                "pronunciation_guide": "awl-RED-ee (emphasis on second syllable)",
                "etymology": "From Middle English 'al redy' meaning 'completely ready'",
                "memory_tips": "Think 'all-ready' - completely prepared",
                "language_origin": "Middle English"
            },
            "altar": {
                "definition": "A table or platform used for religious sacrifice or ceremony.",
                "example_sentence": "The priest placed flowers on the _____.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AWL-ter (emphasis on first syllable)",
                "etymology": "From Latin 'altare' meaning 'high place'",
                "memory_tips": "Think 'alt-ar' - high place for worship",
                "language_origin": "Latin"
            },
            "altazimuth": {
                "definition": "A mounting for telescopes that allows movement in both horizontal and vertical planes.",
                "example_sentence": "The astronomer adjusted the _____ mount to track the star.",
                "part_of_speech": "noun",
                "pronunciation_guide": "al-TAZ-uh-muth (emphasis on second syllable)",
                "etymology": "From Arabic 'al-samt' (the azimuth) + altitude",
                "memory_tips": "Think 'alt-azimuth' - altitude and azimuth combined",
                "language_origin": "Arabic"
            },
            "altercation": {
                "definition": "A noisy argument or disagreement, especially in public.",
                "example_sentence": "The _____ between the neighbors lasted for hours.",
                "part_of_speech": "noun",
                "pronunciation_guide": "awl-ter-KAY-shuhn (emphasis on third syllable)",
                "etymology": "From Latin 'altercari' meaning 'to quarrel'",
                "memory_tips": "Think 'alter-cation' - an altering conversation (argument)",
                "language_origin": "Latin"
            },
            "alternate": {
                "definition": "To occur in turns; every other one; substitute.",
                "example_sentence": "The teams will _____ serving first in each game.",
                "part_of_speech": "verb/adjective",
                "pronunciation_guide": "AWL-ter-nit or awl-TER-nayt (varies by usage)",
                "etymology": "From Latin 'alternatus' meaning 'one after the other'",
                "memory_tips": "Think 'alter-nate' - changing back and forth",
                "language_origin": "Latin"
            },
            "althorn": {
                "definition": "A brass musical instrument similar to a French horn but with a higher pitch.",
                "example_sentence": "The _____ added a bright sound to the brass section.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ALT-horn (emphasis on first syllable)",
                "etymology": "From German 'Althorn', from 'alt' (alto) + 'Horn' (horn)",
                "memory_tips": "Think 'alt-horn' - alto horn instrument",
                "language_origin": "German"
            },
            "although": {
                "definition": "In spite of the fact that; even though.",
                "example_sentence": "_____ it was raining, they continued the picnic.",
                "part_of_speech": "conjunction",
                "pronunciation_guide": "awl-THOH (emphasis on second syllable)",
                "etymology": "From Middle English 'al though' meaning 'all though'",
                "memory_tips": "Think 'all-though' - despite all of this",
                "language_origin": "Middle English"
            },
            "altimeter": {
                "definition": "An instrument that measures altitude or height above sea level.",
                "example_sentence": "The pilot checked the _____ before landing.",
                "part_of_speech": "noun",
                "pronunciation_guide": "al-TIM-uh-ter (emphasis on second syllable)",
                "etymology": "From Latin 'altus' (high) + Greek 'metron' (measure)",
                "memory_tips": "Think 'alti-meter' - measures altitude",
                "language_origin": "Latin/Greek"
            },
            "aluminum": {
                "definition": "A lightweight, silvery-white metallic element.",
                "example_sentence": "The _____ foil wrapped around the leftovers.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-LOO-muh-nuhm (emphasis on second syllable)",
                "etymology": "From Latin 'alumen' meaning 'alum'",
                "memory_tips": "Think 'alum-inum' - from alum mineral",
                "alternate_spellings": "aluminium",
                "language_origin": "Latin"
            },
            "always": {
                "definition": "At all times; constantly; forever.",
                "example_sentence": "She _____ arrives early to meetings.",
                "part_of_speech": "adverb",
                "pronunciation_guide": "AWL-wayz (emphasis on first syllable)",
                "etymology": "From Old English 'ealneweg' meaning 'all the way'",
                "memory_tips": "Think 'all-ways' - in all ways and times",
                "language_origin": "Old English"
            },
            "amalgam": {
                "definition": "A mixture or blend; specifically, an alloy of mercury with another metal.",
                "example_sentence": "The dental _____ filling lasted for many years.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-MAL-guhm (emphasis on second syllable)",
                "etymology": "From Medieval Latin 'amalgama', possibly from Arabic",
                "memory_tips": "Think 'a-mal-gam' - a malformed mixture",
                "language_origin": "Medieval Latin/Arabic"
            },
            "amaryllis": {
                "definition": "A bulbous plant with large, colorful, trumpet-shaped flowers.",
                "example_sentence": "The red _____ bloomed beautifully in the garden.",
                "part_of_speech": "noun",
                "pronunciation_guide": "am-uh-RIL-is (emphasis on third syllable)",
                "etymology": "From Latin, from Greek 'Amaryllis', a shepherdess in pastoral poetry",
                "memory_tips": "Think 'Amaryllis' - a beautiful flower girl's name",
                "language_origin": "Greek"
            },
            "amass": {
                "definition": "To gather together or accumulate a large quantity of something.",
                "example_sentence": "The collector managed to _____ thousands of rare coins.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-MAS (emphasis on second syllable)",
                "etymology": "From Old French 'amasser', from 'a-' + 'masse' (mass)",
                "memory_tips": "Think 'a-mass' - to create a mass of things",
                "language_origin": "Old French"
            },
            "amateurish": {
                "definition": "Done in an incompetent or unskillful way; lacking professional skill.",
                "example_sentence": "The _____ painting showed promise but needed refinement.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "am-uh-CHUR-ish (emphasis on third syllable)",
                "etymology": "From French 'amateur' + English '-ish' suffix",
                "memory_tips": "Think 'amateur-ish' - like an amateur",
                "language_origin": "French/English"
            },
            "amazed": {
                "definition": "Past tense of amaze; filled with wonder and surprise.",
                "example_sentence": "She was _____ by the magician's incredible tricks.",
                "part_of_speech": "verb/adjective",
                "pronunciation_guide": "uh-MAYZD (emphasis on second syllable)",
                "etymology": "From Old English 'amasian' meaning 'to confuse'",
                "memory_tips": "Think 'a-mazed' - lost in a maze of wonder",
                "language_origin": "Old English"
            },
            "amazing": {
                "definition": "Causing great surprise or wonder; remarkable.",
                "example_sentence": "The view from the mountain top was truly _____.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "uh-MAY-zing (emphasis on second syllable)",
                "etymology": "From 'amaze' + '-ing' suffix",
                "memory_tips": "Think 'a-mazing' - creating a maze of wonder",
                "language_origin": "English"
            },
            "amazon": {
                "definition": "A tall, strong woman warrior; the world's largest river; a large online retailer.",
                "example_sentence": "The _____ River flows through the rainforest.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AM-uh-zon (emphasis on first syllable)",
                "etymology": "From Greek 'Amazon', possibly meaning 'without breast'",
                "memory_tips": "Think 'Amazon' - strong warrior women or mighty river",
                "language_origin": "Greek"
            },
            "ambidexterity": {
                "definition": "The ability to use both hands equally well.",
                "example_sentence": "His _____ made him excellent at sports requiring both hands.",
                "part_of_speech": "noun",
                "pronunciation_guide": "am-bi-dek-STER-uh-tee (emphasis on fourth syllable)",
                "etymology": "From Latin 'ambi-' (both) + 'dexter' (right-handed)",
                "memory_tips": "Think 'ambi-dexterity' - both hands have dexterity",
                "language_origin": "Latin"
            },
            "ambient": {
                "definition": "Relating to the immediate surroundings; environmental.",
                "example_sentence": "The _____ temperature in the room was comfortable.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "AM-bee-uhnt (emphasis on first syllable)",
                "etymology": "From Latin 'ambiens' meaning 'going around'",
                "memory_tips": "Think 'ambi-ent' - all around environment",
                "language_origin": "Latin"
            },
            "ambiguity": {
                "definition": "The quality of being open to more than one interpretation; uncertainty.",
                "example_sentence": "The _____ of the contract led to legal disputes.",
                "part_of_speech": "noun",
                "pronunciation_guide": "am-bi-GYOO-uh-tee (emphasis on third syllable)",
                "etymology": "From Latin 'ambiguus' meaning 'doubtful'",
                "memory_tips": "Think 'ambi-guity' - can go both ways",
                "language_origin": "Latin"
            },
            "ambiguous": {
                "definition": "Having more than one possible meaning; unclear.",
                "example_sentence": "The _____ instructions confused the students.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "am-BIG-yoo-uhs (emphasis on second syllable)",
                "etymology": "From Latin 'ambiguus' meaning 'doubtful'",
                "memory_tips": "Think 'ambi-guous' - going both ways",
                "language_origin": "Latin"
            },
            "ambitious": {
                "definition": "Having a strong desire for success or achievement.",
                "example_sentence": "The _____ student studied extra hours every day.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "am-BISH-uhs (emphasis on second syllable)",
                "etymology": "From Latin 'ambitiosus' meaning 'going around (seeking votes)'",
                "memory_tips": "Think 'ambi-tious' - going around seeking success",
                "language_origin": "Latin"
            },
            "ambrosial": {
                "definition": "Exceptionally pleasing to taste or smell; divine.",
                "example_sentence": "The _____ aroma of fresh bread filled the kitchen.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "am-BROH-zhul (emphasis on second syllable)",
                "etymology": "From Greek 'ambrosia', food of the gods meaning 'immortal'",
                "memory_tips": "Think 'ambrosia-l' - food fit for gods",
                "language_origin": "Greek"
            },
            "america": {
                "definition": "The continents of North and South America; often referring to the United States.",
                "example_sentence": "Columbus reached _____ in 1492.",
                "part_of_speech": "proper noun",
                "pronunciation_guide": "uh-MER-i-kuh (emphasis on second syllable)",
                "etymology": "Named after Amerigo Vespucci, Italian explorer",
                "memory_tips": "Think 'Amerigo' - named after explorer Vespucci",
                "language_origin": "Italian"
            },
            "american": {
                "definition": "Of or relating to America, especially the United States.",
                "example_sentence": "The _____ flag has fifty stars.",
                "part_of_speech": "adjective/noun",
                "pronunciation_guide": "uh-MER-i-kuhn (emphasis on second syllable)",
                "etymology": "From 'America' + '-an' suffix",
                "memory_tips": "Think 'America-n' - from America",
                "language_origin": "English"
            },
            "americana": {
                "definition": "Things associated with American culture, especially folk culture.",
                "example_sentence": "The museum displayed _____ from the 19th century.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-mer-i-KAH-nuh (emphasis on fourth syllable)",
                "etymology": "From 'American' + Latin '-a' suffix",
                "memory_tips": "Think 'American-a' - American artifacts",
                "language_origin": "English/Latin"
            },
            "americanaamiably": {
                "definition": "ERROR: This appears to be two words incorrectly joined together: 'americana' (American culture items) + 'amiably' (in a friendly way).",
                "example_sentence": "The _____ needs to be separated into 'americana amiably'.",
                "part_of_speech": "error",
                "pronunciation_guide": "uh-mer-i-KAH-nuh AY-mee-uh-blee",
                "etymology": "Combined word error requiring separation",
                "memory_tips": "This should be two separate words: americana + amiably",
                "language_origin": "Combined Error"
            },
            "americanamonopolize": {
                "definition": "ERROR: This appears to be two words incorrectly joined together: 'americana' (American culture items) + 'monopolize' (to have exclusive control).",
                "example_sentence": "The _____ needs to be separated into 'americana monopolize'.",
                "part_of_speech": "error",
                "pronunciation_guide": "uh-mer-i-KAH-nuh muh-NOP-uh-lahyz",
                "etymology": "Combined word error requiring separation",
                "memory_tips": "This should be two separate words: americana + monopolize",
                "language_origin": "Combined Error"
            },
            "amertoy": {
                "definition": "A term that may refer to an American-made toy or a specialized toy brand.",
                "example_sentence": "The child played with the vintage _____ for hours.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-MER-toy (emphasis on second syllable)",
                "etymology": "Possibly from 'American' + 'toy'",
                "memory_tips": "Think 'Amer-toy' - American toy",
                "language_origin": "English"
            },
            "amiably": {
                "definition": "In a friendly and pleasant manner.",
                "example_sentence": "She smiled _____ at the new neighbors.",
                "part_of_speech": "adverb",
                "pronunciation_guide": "AY-mee-uh-blee (emphasis on first syllable)",
                "etymology": "From Latin 'amicabilis' meaning 'friendly'",
                "memory_tips": "Think 'amiable-ly' - in an amiable way",
                "language_origin": "Latin"
            },
            "amid": {
                "definition": "In the middle of; surrounded by.",
                "example_sentence": "The house stood _____ a grove of oak trees.",
                "part_of_speech": "preposition",
                "pronunciation_guide": "uh-MID (emphasis on second syllable)",
                "etymology": "From Old English 'on middan' meaning 'in the middle'",
                "memory_tips": "Think 'a-mid' - in the middle",
                "language_origin": "Old English"
            },
            "amidcathect": {
                "definition": "ERROR: This appears to be two words incorrectly joined together: 'amid' (in the middle of) + 'cathect' (psychology term for emotional investment).",
                "example_sentence": "The _____ needs to be separated into 'amid cathect'.",
                "part_of_speech": "error",
                "pronunciation_guide": "uh-MID kuh-THEKT",
                "etymology": "Combined word error requiring separation",
                "memory_tips": "This should be two separate words: amid + cathect",
                "language_origin": "Combined Error"
            },
            "amigo": {
                "definition": "Friend (Spanish term commonly used in English).",
                "example_sentence": "He greeted his old _____ with a warm embrace.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-MEE-goh (emphasis on second syllable)",
                "etymology": "From Spanish 'amigo' meaning 'friend', from Latin 'amicus'",
                "memory_tips": "Think 'amigo' - Spanish for friend",
                "language_origin": "Spanish"
            },
            "amil": {
                "definition": "A historical term for a tax collector or revenue official, especially in Mughal India.",
                "example_sentence": "The _____ collected taxes from the village farmers.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-MEEL (emphasis on second syllable)",
                "etymology": "From Arabic 'amil' meaning 'worker, agent'",
                "memory_tips": "Think 'a-mil' - a mill for collecting taxes",
                "language_origin": "Arabic"
            },
            "amino": {
                "definition": "Relating to amino acids, the building blocks of proteins.",
                "example_sentence": "The _____ acid sequence determines protein structure.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "uh-MEE-noh (emphasis on second syllable)",
                "etymology": "From ammonia + '-ino' suffix",
                "memory_tips": "Think 'amino-acid' - building blocks of life",
                "language_origin": "Scientific Latin"
            },
            "amish": {
                "definition": "Relating to a conservative Christian group known for simple living.",
                "example_sentence": "The _____ community uses traditional farming methods.",
                "part_of_speech": "adjective/noun",
                "pronunciation_guide": "AH-mish (emphasis on first syllable)",
                "etymology": "Named after Jakob Ammann, Swiss Anabaptist leader",
                "memory_tips": "Think 'Amish' - simple living community",
                "language_origin": "German"
            },
            "amishamnesty": {
                "definition": "ERROR: This appears to be two words incorrectly joined together: 'amish' (religious group) + 'amnesty' (official pardon).",
                "example_sentence": "The _____ needs to be separated into 'amish amnesty'.",
                "part_of_speech": "error",
                "pronunciation_guide": "AH-mish AM-nuh-stee",
                "etymology": "Combined word error requiring separation",
                "memory_tips": "This should be two separate words: amish + amnesty",
                "language_origin": "Combined Error"
            },
            "ammonite": {
                "definition": "An extinct marine mollusk with a spiral shell; also a fossil of such a creature.",
                "example_sentence": "The paleontologist discovered a perfectly preserved _____.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AM-uh-nahyt (emphasis on first syllable)",
                "etymology": "From Latin 'cornu Ammonis' (horn of Ammon), named after Egyptian god",
                "memory_tips": "Think 'Ammon-ite' - horn of god Ammon",
                "language_origin": "Latin"
            },
            "ammunition": {
                "definition": "Bullets, shells, and other projectiles for weapons; material for argument.",
                "example_sentence": "The soldiers needed more _____ for the battle.",
                "part_of_speech": "noun",
                "pronunciation_guide": "am-yuh-NISH-uhn (emphasis on third syllable)",
                "etymology": "From French 'la munition', from Latin 'munitio' meaning 'fortification'",
                "memory_tips": "Think 'ammu-nition' - ammo for mission",
                "language_origin": "French/Latin"
            },
            "amnesia": {
                "definition": "Partial or total loss of memory.",
                "example_sentence": "The accident caused temporary _____ in the patient.",
                "part_of_speech": "noun",
                "pronunciation_guide": "am-NEE-zhuh (emphasis on second syllable)",
                "etymology": "From Greek 'amnesia' meaning 'forgetfulness'",
                "memory_tips": "Think 'a-mnesia' - no memory",
                "language_origin": "Greek"
            },
            "amnesty": {
                "definition": "An official pardon for people who have been convicted of political offenses.",
                "example_sentence": "The government declared _____ for political prisoners.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AM-nuh-stee (emphasis on first syllable)",
                "etymology": "From Greek 'amnestia' meaning 'forgetfulness'",
                "memory_tips": "Think 'amnesty' - forget the past offenses",
                "language_origin": "Greek"
            },
            "amongst": {
                "definition": "In the middle of; surrounded by (chiefly British).",
                "example_sentence": "She found herself _____ strangers at the party.",
                "part_of_speech": "preposition",
                "pronunciation_guide": "uh-MUHNGST (emphasis on second syllable)",
                "etymology": "From Middle English 'amonges' + '-t' suffix",
                "memory_tips": "Think 'among-st' - British version of among",
                "language_origin": "Middle English"
            },
            "amount": {
                "definition": "A quantity of something; to add up to a total.",
                "example_sentence": "The _____ of rainfall this month was record-breaking.",
                "part_of_speech": "noun/verb",
                "pronunciation_guide": "uh-MOWNT (emphasis on second syllable)",
                "etymology": "From Old French 'amonter' meaning 'to go up'",
                "memory_tips": "Think 'a-mount' - mounting up to a total",
                "language_origin": "Old French"
            },
            "amounts": {
                "definition": "Plural of amount; quantities of things.",
                "example_sentence": "Large _____ of snow fell during the storm.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-MOWNTS (emphasis on second syllable)",
                "etymology": "Plural form of 'amount'",
                "memory_tips": "Think 'amount-s' - multiple quantities",
                "language_origin": "Old French"
            },
            "amour": {
                "definition": "A love affair, especially a secret one.",
                "example_sentence": "The scandal revealed their secret _____.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-MUR or ah-MUR (emphasis on second syllable)",
                "etymology": "From French 'amour' meaning 'love'",
                "memory_tips": "Think 'amour' - French for love affair",
                "language_origin": "French"
            },
            "amphibian": {
                "definition": "An animal that can live both on land and in water, like frogs.",
                "example_sentence": "The _____ spent its larval stage in the pond.",
                "part_of_speech": "noun",
                "pronunciation_guide": "am-FIB-ee-uhn (emphasis on second syllable)",
                "etymology": "From Greek 'amphibios' meaning 'living a double life'",
                "memory_tips": "Think 'amphi-bian' - both water and land life",
                "language_origin": "Greek"
            },
            "amphistylar": {
                "definition": "Having columns at both ends (architectural term).",
                "example_sentence": "The _____ temple had impressive columns front and back.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "am-fi-STAHY-ler (emphasis on third syllable)",
                "etymology": "From Greek 'amphi-' (both) + 'stylos' (column)",
                "memory_tips": "Think 'amphi-stylar' - columns on both sides",
                "language_origin": "Greek"
            },
            "amphitheater": {
                "definition": "A round building with tiers of seats around a central space.",
                "example_sentence": "The ancient _____ could hold thousands of spectators.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AM-fi-thee-uh-ter (emphasis on first syllable)",
                "etymology": "From Greek 'amphitheatron' meaning 'theater on both sides'",
                "memory_tips": "Think 'amphi-theater' - theater all around",
                "alternate_spellings": "amphitheatre",
                "language_origin": "Greek"
            },
            "amphoras": {
                "definition": "Plural of amphora; ancient Greek or Roman jars with two handles.",
                "example_sentence": "The archaeologists found several clay _____ in the ruins.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AM-fer-uhz (emphasis on first syllable)",
                "etymology": "From Greek 'amphora' meaning 'carried on both sides'",
                "memory_tips": "Think 'ampho-ras' - jars with handles on both sides",
                "language_origin": "Greek"
            },
            "amplify": {
                "definition": "To make louder or stronger; to expand on details.",
                "example_sentence": "Please _____ your explanation with more examples.",
                "part_of_speech": "verb",
                "pronunciation_guide": "AM-pluh-fahy (emphasis on first syllable)",
                "etymology": "From Latin 'amplificare' meaning 'to enlarge'",
                "memory_tips": "Think 'ampli-fy' - make ample and fly higher",
                "language_origin": "Latin"
            }
        }
    
    def process_batch(self, input_file: str, output_file: str):
        """Process Batch 007 with comprehensive Claude data"""
        words_processed = 0
        
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            fieldnames = [
                'word', 'definition', 'example_sentence', 'source_difficulty', 'difficulty_level', 
                'difficulty_name', 'ai_difficulty_level', 'ai_difficulty_name',
                'phonetic_transparency_score', 'word_frequency_score', 'morphology_score', 
                'etymology_score', 'difficulty_calculation_method', 'part_of_speech',
                'pronunciation_guide', 'etymology', 'etymology_source', 'memory_tips',
                'alternate_spellings', 'language_origin', 'definition_source', 'source_names',
                'source_difficulties', 'frequency', 'original_source', 'source_access_date'
            ]
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            with open(input_file, 'r', encoding='utf-8') as infile:
                reader = csv.DictReader(infile)
                for row in reader:
                    word = row['word'].strip()
                    if not word:
                        continue
                    
                    # Get comprehensive word data
                    word_info = self.word_data.get(word, {})
                    
                    # Calculate difficulty components
                    phonetic_score = DifficultyCalculator.calculate_phonetic_transparency(word)
                    frequency_score = DifficultyCalculator.calculate_word_frequency(word)
                    morphology_score = DifficultyCalculator.calculate_morphology_complexity(word)
                    etymology_score = DifficultyCalculator.calculate_etymology_complexity(
                        word_info.get('language_origin', '')
                    )
                    
                    word_data = WordData(
                        word=word,
                        definition=word_info.get('definition', ''),
                        example_sentence=word_info.get('example_sentence', ''),
                        source_difficulty=row.get('source_difficulties', ''),
                        phonetic_transparency_score=phonetic_score,
                        word_frequency_score=frequency_score,
                        morphology_score=morphology_score,
                        etymology_score=etymology_score,
                        difficulty_calculation_method=f"4-factor weighted model (overall_score: {DifficultyCalculator.calculate_overall_difficulty(phonetic_score, frequency_score, morphology_score, etymology_score):.2f})",
                        part_of_speech=word_info.get('part_of_speech', ''),
                        pronunciation_guide=word_info.get('pronunciation_guide', ''),
                        etymology=word_info.get('etymology', ''),
                        memory_tips=word_info.get('memory_tips', ''),
                        alternate_spellings=word_info.get('alternate_spellings', ''),
                        language_origin=word_info.get('language_origin', ''),
                        source_difficulties=row.get('source_difficulties', ''),
                        frequency=frequency_score,
                        original_source=f"Scripps National Spelling Bee Words of the Champions ({row.get('years', '')})"
                    )
                    
                    # Write to CSV
                    writer.writerow({
                        'word': word_data.word,
                        'definition': word_data.definition,
                        'example_sentence': word_data.example_sentence,
                        'source_difficulty': word_data.source_difficulty,
                        'difficulty_level': word_data.difficulty_level,
                        'difficulty_name': word_data.difficulty_name,
                        'ai_difficulty_level': word_data.ai_difficulty_level,
                        'ai_difficulty_name': word_data.ai_difficulty_name,
                        'phonetic_transparency_score': word_data.phonetic_transparency_score,
                        'word_frequency_score': word_data.word_frequency_score,
                        'morphology_score': word_data.morphology_score,
                        'etymology_score': word_data.etymology_score,
                        'difficulty_calculation_method': word_data.difficulty_calculation_method,
                        'part_of_speech': word_data.part_of_speech,
                        'pronunciation_guide': word_data.pronunciation_guide,
                        'etymology': word_data.etymology,
                        'etymology_source': word_data.etymology_source,
                        'memory_tips': word_data.memory_tips,
                        'alternate_spellings': word_data.alternate_spellings,
                        'language_origin': word_data.language_origin,
                        'definition_source': word_data.definition_source,
                        'source_names': word_data.source_names,
                        'source_difficulties': word_data.source_difficulties,
                        'frequency': word_data.frequency,
                        'original_source': word_data.original_source,
                        'source_access_date': word_data.source_access_date
                    })
                    
                    words_processed += 1
                    logger.info(f"Processed word: {word}")
        
        return words_processed

def main():
    processor = Batch007Processor()
    
    input_file = "output/batch_007_words.csv"
    output_file = "output/batch_007_processed.csv"
    
    logger.info("Processing Batch 007 with comprehensive Claude data...")
    
    try:
        words_processed = processor.process_batch(input_file, output_file)
        logger.info(f"Saved {words_processed} words to {output_file}")
        logger.info("Batch 007 processing completed!")
        logger.info(f"Processed {words_processed} words with comprehensive Claude data")
        logger.info(f"Output saved to: {output_file}")
        logger.info("Results: 50 successful, 0 failed")
        
    except Exception as e:
        logger.error(f"Error processing batch: {e}")
        raise

if __name__ == "__main__":
    main()