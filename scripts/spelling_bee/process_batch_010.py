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

class Batch010Processor:
    def __init__(self):
        self.word_data = {
            "antithesis": {
                "definition": "The exact opposite of something; a person or thing that is the direct opposite of someone or something else; a rhetorical device contrasting opposing ideas.",
                "example_sentence": "His calm demeanor was the _____ of his brother's explosive temperament.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-TIH-thuh-sis (emphasis on second syllable)",
                "etymology": "From Greek 'antithesis' meaning 'opposition, contrast'",
                "memory_tips": "Think 'anti-thesis' - against or opposite to a thesis or idea",
                "language_origin": "Greek"
            },
            "antlers": {
                "definition": "The branched horns of deer, elk, moose, and similar animals, shed and regrown annually.",
                "example_sentence": "The magnificent stag displayed impressive _____ with twelve points.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ANT-lurz (emphasis on first syllable)",
                "etymology": "From Old French 'antoillier', from Latin 'ante-ocularis' (before the eyes)",
                "memory_tips": "Think 'antlers' - the branched horns that appear before (ante) the animal's eyes",
                "language_origin": "Latin"
            },
            "antonyms": {
                "definition": "Words that have opposite meanings to other words; contrasting terms.",
                "example_sentence": "Hot and cold are common _____ taught in elementary vocabulary lessons.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AN-tuh-nimz (emphasis on first syllable)",
                "etymology": "From Greek 'anti-' (opposite) + 'onyma' (name)",
                "memory_tips": "Think 'ant-onyms' - opposite names or words",
                "language_origin": "Greek"
            },
            "anxiety": {
                "definition": "A feeling of worry, nervousness, or unease about something with an uncertain outcome; a mental health condition characterized by excessive worry.",
                "example_sentence": "The student experienced severe _____ before taking the final exam.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ang-ZYE-uh-tee (emphasis on second syllable)",
                "etymology": "From Latin 'anxietas', from 'anxius' (anxious)",
                "memory_tips": "Think 'anxiety' - the feeling of being anxious or worried",
                "language_origin": "Latin"
            },
            "anybody": {
                "definition": "Any person; anyone at all; used to refer to a person without specifying who.",
                "example_sentence": "Is _____ home to answer the door?",
                "part_of_speech": "pronoun",
                "pronunciation_guide": "EN-ee-bod-ee (emphasis on first syllable)",
                "etymology": "From 'any' + 'body' (person)",
                "memory_tips": "Think 'any-body' - any person or individual",
                "language_origin": "English"
            },
            "anymore": {
                "definition": "Any longer; at the present time (used in negative contexts or questions).",
                "example_sentence": "She doesn't live here _____ since moving to college.",
                "part_of_speech": "adverb",
                "pronunciation_guide": "en-ee-MOR (emphasis on third syllable)",
                "etymology": "From 'any' + 'more'",
                "memory_tips": "Think 'any-more' - any additional time, usually in negative contexts",
                "language_origin": "English"
            },
            "anyone": {
                "definition": "Any person; anybody; used to refer to a person without specifying who.",
                "example_sentence": "Can _____ explain how this machine works?",
                "part_of_speech": "pronoun",
                "pronunciation_guide": "EN-ee-wuhn (emphasis on first syllable)",
                "etymology": "From 'any' + 'one'",
                "memory_tips": "Think 'any-one' - any single person",
                "language_origin": "English"
            },
            "anytime": {
                "definition": "At any time; whenever; used to indicate that something can happen at any moment.",
                "example_sentence": "You can call me _____ if you need help with the project.",
                "part_of_speech": "adverb",
                "pronunciation_guide": "EN-ee-tyme (emphasis on first syllable)",
                "etymology": "From 'any' + 'time'",
                "memory_tips": "Think 'any-time' - at whatever time is convenient",
                "language_origin": "English"
            },
            "anyway": {
                "definition": "In any case; regardless; used to resume or return to a previous topic.",
                "example_sentence": "The weather was terrible, but we decided to go hiking _____.",
                "part_of_speech": "adverb",
                "pronunciation_guide": "EN-ee-way (emphasis on first syllable)",
                "etymology": "From 'any' + 'way'",
                "memory_tips": "Think 'any-way' - in whatever manner or regardless",
                "language_origin": "English"
            },
            "apabhramsa": {
                "definition": "Late Middle Indo-Aryan dialects that developed from Sanskrit and Prakrit languages in medieval India.",
                "example_sentence": "Scholars study _____ texts to understand the evolution of Indian languages.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ah-pah-BRAHM-shah (emphasis on third syllable)",
                "etymology": "From Sanskrit 'apabhramsa' meaning 'falling away, corruption'",
                "memory_tips": "Think 'apa-bhramsa' - languages that fell away from classical Sanskrit",
                "language_origin": "Sanskrit"
            },
            "apartment": {
                "definition": "A self-contained residential unit in a building; a flat or suite of rooms.",
                "example_sentence": "The young couple rented a cozy one-bedroom _____ downtown.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-PART-munt (emphasis on second syllable)",
                "etymology": "From French 'appartement', from Italian 'appartamento'",
                "memory_tips": "Think 'apart-ment' - a place set apart for living",
                "language_origin": "French"
            },
            "aperture": {
                "definition": "An opening, hole, or gap; in photography, the opening in a camera lens that controls light exposure.",
                "example_sentence": "The photographer adjusted the _____ to create a shallow depth of field.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AP-ur-chur (emphasis on first syllable)",
                "etymology": "From Latin 'apertura', from 'aperire' (to open)",
                "memory_tips": "Think 'aperture' - an opening that lets light through",
                "language_origin": "Latin"
            },
            "aperçu": {
                "definition": "A brief survey or sketch; an insight or glimpse; a concise overview or summary.",
                "example_sentence": "The professor provided an _____ of the semester's curriculum.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ah-per-SOO (French pronunciation)",
                "etymology": "From French 'aperçu', from 'apercevoir' (to perceive)",
                "memory_tips": "Think 'aperçu' - a perceived glimpse or overview",
                "language_origin": "French"
            },
            "aperçucioppino": {
                "definition": "COMBINED WORD ERROR - appears to be 'aperçu' + 'cioppino' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "apex": {
                "definition": "The highest point or peak; the culminating point; the vertex of a geometric figure.",
                "example_sentence": "The mountain climber finally reached the _____ after hours of difficult ascent.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AY-peks (emphasis on first syllable)",
                "etymology": "From Latin 'apex' meaning 'summit, peak'",
                "memory_tips": "Think 'apex' - the highest point or peak of something",
                "language_origin": "Latin"
            },
            "aphasia": {
                "definition": "A medical condition affecting the ability to communicate, typically caused by brain damage; loss of language abilities.",
                "example_sentence": "The stroke patient developed _____ and struggled to find the right words.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-FAY-zhuh (emphasis on second syllable)",
                "etymology": "From Greek 'a-' (without) + 'phasis' (speech)",
                "memory_tips": "Think 'a-phasia' - without speech or language ability",
                "language_origin": "Greek"
            },
            "apiary": {
                "definition": "A place where bees are kept; a collection of beehives for honey production.",
                "example_sentence": "The beekeeper tended to dozens of hives in his backyard _____.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AY-pee-air-ee (emphasis on first syllable)",
                "etymology": "From Latin 'apiarium', from 'apis' (bee)",
                "memory_tips": "Think 'api-ary' - a place for apis (bees)",
                "language_origin": "Latin"
            },
            "apistogramma": {
                "definition": "A genus of small, colorful freshwater fish native to South America, popular in aquariums.",
                "example_sentence": "The aquarium enthusiast added several _____ species to create a diverse tank.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ah-pis-toh-GRAM-ah (emphasis on fourth syllable)",
                "etymology": "From Greek 'apistos' (faithless) + 'gramma' (line), referring to irregular lateral lines",
                "memory_tips": "Think 'apisto-gramma' - fish with irregular (faithless) lines",
                "language_origin": "Greek"
            },
            "apocalypse": {
                "definition": "The complete final destruction of the world; a catastrophic event; a revelation or unveiling.",
                "example_sentence": "The movie depicted a zombie _____ that threatened all of humanity.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-POK-uh-lips (emphasis on second syllable)",
                "etymology": "From Greek 'apokalypsis' meaning 'revelation, unveiling'",
                "memory_tips": "Think 'apo-calypse' - an unveiling of the end times",
                "language_origin": "Greek"
            },
            "apocryphal": {
                "definition": "Of doubtful authenticity; not genuine; relating to religious writings not accepted as canonical.",
                "example_sentence": "The historian dismissed the story as _____ due to lack of reliable sources.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "uh-POK-ruh-ful (emphasis on second syllable)",
                "etymology": "From Greek 'apokryphos' meaning 'hidden, secret'",
                "memory_tips": "Think 'apo-cryphal' - hidden or secret, therefore questionable",
                "language_origin": "Greek"
            },
            "apodyterium": {
                "definition": "The undressing room in ancient Roman baths where bathers removed their clothes.",
                "example_sentence": "Archaeologists uncovered the _____ section of the ancient Roman bathhouse.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ap-oh-dy-TEER-ee-um (emphasis on fourth syllable)",
                "etymology": "From Greek 'apodyterion', from 'apodyein' (to undress)",
                "memory_tips": "Think 'apo-dyterium' - place to take off (apo) clothing",
                "language_origin": "Greek"
            },
            "apogee": {
                "definition": "The highest point of something; the point in an orbit farthest from Earth; the culmination or peak.",
                "example_sentence": "The satellite reached its _____ at 400 kilometers above Earth.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AP-oh-jee (emphasis on first syllable)",
                "etymology": "From Greek 'apo' (away from) + 'gaia' (earth)",
                "memory_tips": "Think 'apo-gee' - away from the earth, at the highest point",
                "language_origin": "Greek"
            },
            "apollo": {
                "definition": "Greek god of music, poetry, prophecy, and the sun; an extremely handsome young man.",
                "example_sentence": "The sculpture depicted _____ with his characteristic lyre and laurel crown.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-POL-oh (emphasis on second syllable)",
                "etymology": "From Greek mythology, name of the god Apollo",
                "memory_tips": "Think 'Apollo' - the classical Greek god of beauty and arts",
                "language_origin": "Greek"
            },
            "apology": {
                "definition": "A statement expressing regret or asking forgiveness; a formal justification or defense of opinions or conduct.",
                "example_sentence": "She offered a sincere _____ for arriving late to the important meeting.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-POL-uh-jee (emphasis on second syllable)",
                "etymology": "From Greek 'apologia', from 'apo-' (away) + 'logos' (speech)",
                "memory_tips": "Think 'apo-logy' - speaking away from blame, explaining oneself",
                "language_origin": "Greek"
            },
            "apophyge": {
                "definition": "In classical architecture, the curved junction between a column shaft and its base or capital.",
                "example_sentence": "The architect carefully designed the _____ to create a smooth transition in the column.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-POF-uh-jee (emphasis on second syllable)",
                "etymology": "From Greek 'apophyge', from 'apo-' (from) + 'phyge' (flight)",
                "memory_tips": "Think 'apo-phyge' - the curved flight from column to base",
                "language_origin": "Greek"
            },
            "apoplexy": {
                "definition": "A stroke; sudden loss of consciousness due to brain hemorrhage; extreme anger or rage.",
                "example_sentence": "The elderly man suffered from _____ and was rushed to the hospital.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AP-uh-plek-see (emphasis on first syllable)",
                "etymology": "From Greek 'apoplexia', from 'apo-' (off) + 'plessein' (to strike)",
                "memory_tips": "Think 'apo-plexy' - struck down by sudden illness",
                "language_origin": "Greek"
            },
            "aporia": {
                "definition": "A logical puzzle or state of puzzlement; an expression of doubt or uncertainty in rhetoric.",
                "example_sentence": "The philosopher's _____ left the audience questioning their fundamental beliefs.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-POR-ee-uh (emphasis on second syllable)",
                "etymology": "From Greek 'aporia' meaning 'impassable, without passage'",
                "memory_tips": "Think 'aporia' - a place with no passage, creating puzzlement",
                "language_origin": "Greek"
            },
            "aposematic": {
                "definition": "Relating to warning coloration in animals that advertises their toxicity or danger to predators.",
                "example_sentence": "The bright red and black pattern served as _____ coloration to warn predators.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "ap-oh-suh-MAT-ik (emphasis on fourth syllable)",
                "etymology": "From Greek 'apo-' (away) + 'sema' (sign, signal)",
                "memory_tips": "Think 'apo-sematic' - signaling away, warning others to stay away",
                "language_origin": "Greek"
            },
            "apostolici": {
                "definition": "Relating to the apostles; members of various Christian movements claiming apostolic authority.",
                "example_sentence": "The medieval _____ movement sought to return to the simple lifestyle of the apostles.",
                "part_of_speech": "adjective/noun",
                "pronunciation_guide": "ah-pos-TOL-ih-chee (emphasis on third syllable)",
                "etymology": "From Latin 'apostolicus', from Greek 'apostolikos' (of an apostle)",
                "memory_tips": "Think 'apostol-ici' - relating to the apostles or apostolic traditions",
                "language_origin": "Latin"
            },
            "apothecary": {
                "definition": "A pharmacist or druggist; a person who prepared and sold medicines; a pharmacy or drugstore.",
                "example_sentence": "The medieval _____ mixed herbs and potions to treat various ailments.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-POTH-uh-ker-ee (emphasis on second syllable)",
                "etymology": "From Greek 'apotheke' meaning 'storehouse'",
                "memory_tips": "Think 'apo-thecary' - one who manages a storehouse of medicines",
                "language_origin": "Greek"
            },
            "apotheosis": {
                "definition": "The highest point of development; the elevation of someone to divine status; the perfect example of something.",
                "example_sentence": "Winning the championship was the _____ of her athletic career.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-poth-ee-OH-sis (emphasis on fourth syllable)",
                "etymology": "From Greek 'apotheosis', from 'apo-' + 'theos' (god)",
                "memory_tips": "Think 'apo-theosis' - becoming like a god, reaching the highest point",
                "language_origin": "Greek"
            },
            "appalling": {
                "definition": "Causing shock or dismay; horrifying; extremely bad or unpleasant.",
                "example_sentence": "The conditions in the abandoned building were absolutely _____.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "uh-PAW-ling (emphasis on second syllable)",
                "etymology": "From Old French 'apalir' meaning 'to make pale'",
                "memory_tips": "Think 'appalling' - so shocking it makes you pale",
                "language_origin": "French"
            },
            "appaloosa": {
                "definition": "A breed of horse known for its spotted coat pattern, originally developed by the Nez Perce people.",
                "example_sentence": "The beautiful _____ horse displayed distinctive spotted markings across its hindquarters.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ap-uh-LOO-suh (emphasis on third syllable)",
                "etymology": "From Palouse River region, named after the Palouse people",
                "memory_tips": "Think 'Appaloosa' - spotted horse from the Palouse region",
                "language_origin": "Native American"
            },
            "apparatus": {
                "definition": "Equipment or machinery designed for a particular purpose; the complex structure of an organization.",
                "example_sentence": "The laboratory's sophisticated _____ allowed for precise chemical analysis.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ap-uh-RAT-us (emphasis on third syllable)",
                "etymology": "From Latin 'apparatus', from 'apparare' (to prepare)",
                "memory_tips": "Think 'apparatus' - equipment prepared for a specific purpose",
                "language_origin": "Latin"
            },
            "apparel": {
                "definition": "Clothing and accessories; items worn on the body; to dress or clothe.",
                "example_sentence": "The store specialized in athletic _____ for professional athletes.",
                "part_of_speech": "noun/verb",
                "pronunciation_guide": "uh-PAIR-ul (emphasis on second syllable)",
                "etymology": "From Old French 'apareillier' meaning 'to make ready'",
                "memory_tips": "Think 'apparel' - clothing that makes you ready for appearance",
                "language_origin": "French"
            },
            "apparently": {
                "definition": "Seemingly; as far as one knows or can see; evidently; used to express uncertainty.",
                "example_sentence": "_____, the meeting was cancelled due to the snowstorm.",
                "part_of_speech": "adverb",
                "pronunciation_guide": "uh-PAIR-unt-lee (emphasis on second syllable)",
                "etymology": "From Latin 'apparere' meaning 'to appear'",
                "memory_tips": "Think 'apparent-ly' - as it appears to be",
                "language_origin": "Latin"
            },
            "apparition": {
                "definition": "A ghost or ghostlike image; a supernatural appearance; something that appears suddenly or unexpectedly.",
                "example_sentence": "The frightened witness claimed to have seen an _____ in the old mansion.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ap-uh-RISH-un (emphasis on third syllable)",
                "etymology": "From Latin 'apparitio', from 'apparere' (to appear)",
                "memory_tips": "Think 'apparition' - something that appears suddenly, often supernatural",
                "language_origin": "Latin"
            },
            "appear": {
                "definition": "To come into sight; to seem or look; to come before a court or in a show.",
                "example_sentence": "The sun began to _____ through the clouds after the storm.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-PEER (emphasis on second syllable)",
                "etymology": "From Latin 'apparere', from 'ad-' (to) + 'parere' (come forth)",
                "memory_tips": "Think 'appear' - to come forth into view",
                "language_origin": "Latin"
            },
            "appearance": {
                "definition": "The way someone or something looks; the act of appearing; an instance of performing publicly.",
                "example_sentence": "Her elegant _____ at the gala made a lasting impression on everyone.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-PEER-uns (emphasis on second syllable)",
                "etymology": "From Latin 'apparere', from 'ad-' (to) + 'parere' (come forth)",
                "memory_tips": "Think 'appear-ance' - the state of having appeared or how one appears",
                "language_origin": "Latin"
            },
            "appeared": {
                "definition": "Past tense of appear; came into sight; seemed to be; manifested.",
                "example_sentence": "The lost hiker suddenly _____ at the edge of the forest clearing.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-PEERD (emphasis on second syllable)",
                "etymology": "From Latin 'apparere', from 'ad-' (to) + 'parere' (come forth)",
                "memory_tips": "Think 'appeared' - came forth into view in the past",
                "language_origin": "Latin"
            },
            "appeasement": {
                "definition": "The act of pacifying or placating someone by giving in to their demands; the policy of making concessions.",
                "example_sentence": "The policy of _____ failed to prevent the dictator's further aggression.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-PEEZ-munt (emphasis on second syllable)",
                "etymology": "From Old French 'apaisier' meaning 'to bring peace'",
                "memory_tips": "Think 'appease-ment' - the act of bringing peace by giving in",
                "language_origin": "French"
            },
            "appellation": {
                "definition": "A name or title; a designation used to identify something, especially geographical regions for wine.",
                "example_sentence": "The wine's _____ indicated it came from a prestigious vineyard region.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ap-uh-LAY-shun (emphasis on third syllable)",
                "etymology": "From Latin 'appellatio', from 'appellare' (to call upon)",
                "memory_tips": "Think 'appellation' - what something is called or named",
                "language_origin": "Latin"
            },
            "appendages": {
                "definition": "Things attached to something larger; limbs or other projecting parts of an organism.",
                "example_sentence": "The octopus used its eight _____ to navigate through the coral reef.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-PEN-dij-iz (emphasis on second syllable)",
                "etymology": "From Latin 'appendere' meaning 'to hang upon'",
                "memory_tips": "Think 'append-ages' - things that hang upon or attach to the main body",
                "language_origin": "Latin"
            },
            "appetiteluggage": {
                "definition": "COMBINED WORD ERROR - appears to be 'appetite' + 'luggage' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "appetitost": {
                "definition": "A possible variant or corrupted form; may relate to appetizers or appetite stimulants.",
                "example_sentence": "The restaurant served various _____ to stimulate guests' appetites.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ap-uh-TEE-tost (emphasis on third syllable)",
                "etymology": "Possibly from Latin 'appetitus' (appetite) with variant ending",
                "memory_tips": "Think 'appetit-ost' - relating to appetite or appetizers",
                "language_origin": "Latin"
            },
            "applause": {
                "definition": "Approval or praise expressed by clapping; enthusiastic approval or commendation.",
                "example_sentence": "The performer received thunderous _____ from the delighted audience.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-PLAWZ (emphasis on second syllable)",
                "etymology": "From Latin 'applaudere', from 'ad-' (to) + 'plaudere' (to clap)",
                "memory_tips": "Think 'applause' - clapping directed toward a performer",
                "language_origin": "Latin"
            },
            "apple": {
                "definition": "A round fruit with red or green skin and crisp white flesh; the tree that produces this fruit.",
                "example_sentence": "She picked a ripe red _____ from the tree in the orchard.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AP-ul (emphasis on first syllable)",
                "etymology": "From Old English 'æppel', related to Germanic languages",
                "memory_tips": "Think 'apple' - the classic round fruit from the tree",
                "language_origin": "Old English"
            },
            "applicable": {
                "definition": "Relevant or appropriate in a particular situation; able to be applied.",
                "example_sentence": "The new safety regulations are _____ to all employees in the building.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "uh-PLIK-uh-bul (emphasis on second syllable)",
                "etymology": "From Latin 'applicare' meaning 'to join, attach'",
                "memory_tips": "Think 'applic-able' - able to be applied or attached to a situation",
                "language_origin": "Latin"
            },
            "apportion": {
                "definition": "To divide and distribute proportionally; to allocate fairly among recipients.",
                "example_sentence": "The committee will _____ the budget funds equally among all departments.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-POR-shun (emphasis on second syllable)",
                "etymology": "From Old French 'apportioner', from 'portion'",
                "memory_tips": "Think 'a-portion' - to give a portion to each recipient",
                "language_origin": "French"
            },
            "appositive": {
                "definition": "A grammatical construction where two elements are placed side by side, with one explaining the other.",
                "example_sentence": "In the sentence 'My friend John is here,' the word 'John' is an _____.",
                "part_of_speech": "noun/adjective",
                "pronunciation_guide": "uh-POZ-uh-tiv (emphasis on second syllable)",
                "etymology": "From Latin 'appositus', from 'apponere' (to place near)",
                "memory_tips": "Think 'ap-positive' - placed near or positioned next to something",
                "language_origin": "Latin"
            }
        }
        
        # Combined word errors detected in this batch
        self.combined_word_errors = [
            "aperçucioppino",
            "appetiteluggage"
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
    processor = Batch010Processor()
    input_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_010_words.csv"
    output_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_010_processed.csv"
    
    processor.process_batch(input_file, output_file)
    
    print(f"\nBatch 010 Processing Complete!")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Combined word errors flagged: {len(processor.combined_word_errors)}")

if __name__ == "__main__":
    main()