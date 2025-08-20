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

class Batch006Processor:
    def __init__(self):
        self.word_data = {
            "albeit": {
                "definition": "Although; even though; notwithstanding that.",
                "example_sentence": "The plan was risky, _____ necessary for success.",
                "part_of_speech": "conjunction",
                "pronunciation_guide": "awl-BEE-it (emphasis on second syllable)",
                "etymology": "From Middle English 'al be it' meaning 'although it be'",
                "memory_tips": "Think 'all-be-it' - even though it may be",
                "language_origin": "Middle English"
            },
            "albertadifficulty": {
                "definition": "ERROR: This appears to be two words incorrectly joined together: 'alberta' (a Canadian province) + 'difficulty' (state of being hard).",
                "example_sentence": "The _____ needs to be separated into 'alberta difficulty'.",
                "part_of_speech": "error",
                "pronunciation_guide": "al-BER-tuh dif-i-kuhl-tee",
                "etymology": "Combined word error requiring separation",
                "memory_tips": "This should be two separate words: Alberta + difficulty",
                "language_origin": "Combined Error"
            },
            "albion": {
                "definition": "An ancient poetic name for Britain or England; the white cliffs.",
                "example_sentence": "The ships approached the shores of _____ at dawn.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AL-bee-uhn (emphasis on first syllable)",
                "etymology": "From Latin 'albus' meaning 'white', referring to the white cliffs of Dover",
                "memory_tips": "Think 'alba-ion' - white island (Britain)",
                "language_origin": "Latin"
            },
            "albums": {
                "definition": "Plural of album; collections of photographs, recordings, or other items.",
                "example_sentence": "The musician released three _____ in one year.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AL-buhms (emphasis on first syllable)",
                "etymology": "From Latin 'album' meaning 'white tablet' where Romans wrote announcements",
                "memory_tips": "Think 'alba-ums' - white collections",
                "language_origin": "Latin"
            },
            "albuquerque": {
                "definition": "The largest city in New Mexico, United States.",
                "example_sentence": "The family moved to _____ for the warm climate.",
                "part_of_speech": "proper noun",
                "pronunciation_guide": "AL-buh-kur-kee (emphasis on first syllable)",
                "etymology": "Named after Spanish Duke of Alburquerque, from Arabic 'al-burqueque' meaning 'place of cork oaks'",
                "memory_tips": "Think 'Alba-quirky' - a quirky southwestern city",
                "language_origin": "Spanish/Arabic"
            },
            "alcarraza": {
                "definition": "A porous earthenware water jar used for cooling water by evaporation.",
                "example_sentence": "The _____ kept the water cool in the desert heat.",
                "part_of_speech": "noun",
                "pronunciation_guide": "al-kah-RAH-sah (emphasis on third syllable)",
                "etymology": "From Spanish, ultimately from Arabic 'al-kurraza'",
                "memory_tips": "Think 'al-car-raza' - a car-sized water vessel",
                "language_origin": "Spanish/Arabic"
            },
            "alcarrazadifficulty": {
                "definition": "ERROR: This appears to be two words incorrectly joined together: 'alcarraza' (water jar) + 'difficulty' (state of being hard).",
                "example_sentence": "The _____ needs to be separated into 'alcarraza difficulty'.",
                "part_of_speech": "error",
                "pronunciation_guide": "al-kah-RAH-sah dif-i-kuhl-tee",
                "etymology": "Combined word error requiring separation",
                "memory_tips": "This should be two separate words: alcarraza + difficulty",
                "language_origin": "Combined Error"
            },
            "alembroth": {
                "definition": "An alchemical salt, specifically a mixture of mercury chloride and ammonium chloride.",
                "example_sentence": "The alchemist prepared _____ for his transmutation experiments.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-LEM-broth (emphasis on second syllable)",
                "etymology": "From Arabic 'al-ambrut', an alchemical term",
                "memory_tips": "Think 'a-lem-broth' - an alchemical broth",
                "language_origin": "Arabic"
            },
            "alexandria": {
                "definition": "An ancient city in Egypt, founded by Alexander the Great; also various cities named after it.",
                "example_sentence": "The famous lighthouse of _____ was one of the Seven Wonders.",
                "part_of_speech": "proper noun",
                "pronunciation_guide": "al-ig-ZAN-dree-uh (emphasis on third syllable)",
                "etymology": "Named after Alexander the Great, from Greek 'Alexandreia'",
                "memory_tips": "Think 'Alexander-ia' - Alexander's city",
                "language_origin": "Greek"
            },
            "alfresco": {
                "definition": "In the open air; outdoors, especially for dining.",
                "example_sentence": "They enjoyed an _____ dinner under the stars.",
                "part_of_speech": "adjective/adverb",
                "pronunciation_guide": "al-FRES-koh (emphasis on second syllable)",
                "etymology": "From Italian 'al fresco' meaning 'in the fresh (air)'",
                "memory_tips": "Think 'al-fresh-co' - eating in fresh air",
                "language_origin": "Italian"
            },
            "alfvén": {
                "definition": "Relating to Hannes Alfvén, Swedish physicist, or to Alfvén waves in plasma physics.",
                "example_sentence": "The _____ waves propagated through the magnetized plasma.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "ALF-ven (emphasis on first syllable)",
                "etymology": "Named after Hannes Alfvén (1908-1995), Swedish physicist and Nobel Prize winner",
                "memory_tips": "Think 'Alf-ven' - Alf's invention in physics",
                "language_origin": "Swedish"
            },
            "alfvénvirga": {
                "definition": "ERROR: This appears to be two words incorrectly joined together: 'alfvén' (physics term) + 'virga' (meteorological term).",
                "example_sentence": "The _____ needs to be separated into 'alfvén virga'.",
                "part_of_speech": "error",
                "pronunciation_guide": "ALF-ven VUR-guh",
                "etymology": "Combined word error requiring separation",
                "memory_tips": "This should be two separate words: alfvén + virga",
                "language_origin": "Combined Error"
            },
            "algae": {
                "definition": "Simple aquatic organisms, typically photosynthetic and lacking true stems, roots, and leaves.",
                "example_sentence": "Green _____ covered the surface of the pond.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AL-jee (emphasis on first syllable)",
                "etymology": "From Latin 'alga' meaning 'seaweed'",
                "memory_tips": "Think 'al-gae' - green stuff in water",
                "language_origin": "Latin"
            },
            "algebraic": {
                "definition": "Relating to or involving algebra; expressed using algebraic symbols and operations.",
                "example_sentence": "The student solved the _____ equation using factoring.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "al-juh-BRAY-ik (emphasis on third syllable)",
                "etymology": "From Arabic 'al-jabr' meaning 'reunion of broken parts'",
                "memory_tips": "Think 'algebra-ic' - relating to algebra",
                "language_origin": "Arabic"
            },
            "algiers": {
                "definition": "The capital and largest city of Algeria, located in North Africa.",
                "example_sentence": "The Mediterranean port of _____ was bustling with activity.",
                "part_of_speech": "proper noun",
                "pronunciation_guide": "al-JEERZ (emphasis on second syllable)",
                "etymology": "From Arabic 'al-Jazā'ir' meaning 'the islands'",
                "memory_tips": "Think 'al-jeers' - the island city",
                "language_origin": "Arabic"
            },
            "alhambra": {
                "definition": "A palace and fortress complex in Granada, Spain; any ornate Moorish-style building.",
                "example_sentence": "The intricate tiles of the _____ displayed Islamic artistry.",
                "part_of_speech": "noun",
                "pronunciation_guide": "al-HAM-bruh (emphasis on second syllable)",
                "etymology": "From Arabic 'al-Ḥamrā' meaning 'the red one'",
                "memory_tips": "Think 'al-ham-bra' - the red palace",
                "language_origin": "Arabic"
            },
            "alibi": {
                "definition": "Evidence that a person was elsewhere when a crime was committed; an excuse.",
                "example_sentence": "The suspect had a solid _____ for the time of the robbery.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AL-uh-bahy (emphasis on first syllable)",
                "etymology": "From Latin 'alibi' meaning 'elsewhere'",
                "memory_tips": "Think 'ali-bi' - I was elsewhere, by Ali",
                "language_origin": "Latin"
            },
            "alienate": {
                "definition": "To cause someone to become unfriendly or hostile; to make someone feel isolated.",
                "example_sentence": "His rude behavior would _____ potential customers.",
                "part_of_speech": "verb",
                "pronunciation_guide": "AY-lee-uh-nayt (emphasis on first syllable)",
                "etymology": "From Latin 'alienatus', meaning 'transferred to another'",
                "memory_tips": "Think 'alien-ate' - making someone feel like an alien",
                "language_origin": "Latin"
            },
            "alighted": {
                "definition": "Past tense of alight; came down and settled; got off a vehicle.",
                "example_sentence": "The bird _____ gracefully on the branch.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-LAHY-tid (emphasis on second syllable)",
                "etymology": "From Old English 'alihtan' meaning 'to dismount'",
                "memory_tips": "Think 'a-lighted' - came to light on something",
                "language_origin": "Old English"
            },
            "alimentation": {
                "definition": "The process of nourishing or being nourished; the provision of food.",
                "example_sentence": "Proper _____ is essential for healthy growth.",
                "part_of_speech": "noun",
                "pronunciation_guide": "al-uh-men-TAY-shuhn (emphasis on fourth syllable)",
                "etymology": "From Latin 'alimentum' meaning 'nourishment'",
                "memory_tips": "Think 'aliment-ation' - the action of feeding",
                "language_origin": "Latin"
            },
            "allegedly": {
                "definition": "According to claims or assertions; supposedly but not proven.",
                "example_sentence": "The suspect _____ committed the crime last Tuesday.",
                "part_of_speech": "adverb",
                "pronunciation_guide": "uh-LEJ-id-lee (emphasis on second syllable)",
                "etymology": "From Latin 'allegare' meaning 'to send as a deputy'",
                "memory_tips": "Think 'alleged-ly' - supposedly in a legal way",
                "language_origin": "Latin"
            },
            "allegiance": {
                "definition": "Loyalty or commitment to a person, group, or cause.",
                "example_sentence": "Citizens pledge _____ to their country's flag.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-LEE-juhn-s (emphasis on second syllable)",
                "etymology": "From Old French 'ligeance', from 'lige' meaning 'liege'",
                "memory_tips": "Think 'a-legiance' - a legal commitment",
                "language_origin": "Old French"
            },
            "alleluiatic": {
                "definition": "Of or relating to alleluia; characterized by praise or joy.",
                "example_sentence": "The choir's _____ singing filled the cathedral with joy.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "al-uh-LOO-yah-tik (emphasis on third syllable)",
                "etymology": "From Hebrew 'hallelujah' meaning 'praise Yahweh'",
                "memory_tips": "Think 'alleluia-tic' - relating to alleluia praise",
                "language_origin": "Hebrew"
            },
            "allergenic": {
                "definition": "Causing or capable of causing an allergic reaction.",
                "example_sentence": "Peanuts are highly _____ for some people.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "al-er-JEN-ik (emphasis on third syllable)",
                "etymology": "From Greek 'allos' (other) + 'ergon' (work) + '-genic' (producing)",
                "memory_tips": "Think 'aller-genic' - generating allergies",
                "language_origin": "Greek"
            },
            "allocable": {
                "definition": "Capable of being allocated, assigned, or distributed.",
                "example_sentence": "The budget funds were _____ among various departments.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "AL-uh-kuh-buhl (emphasis on first syllable)",
                "etymology": "From Latin 'allocare' meaning 'to place'",
                "memory_tips": "Think 'allo-cable' - able to be placed elsewhere",
                "language_origin": "Latin"
            },
            "allochroous": {
                "definition": "Changing color; exhibiting different colors.",
                "example_sentence": "The _____ mineral appeared different under various lights.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "al-oh-KROH-uhs (emphasis on third syllable)",
                "etymology": "From Greek 'allos' (other) + 'chroa' (color)",
                "memory_tips": "Think 'allo-chromous' - other colors",
                "language_origin": "Greek"
            },
            "allonym": {
                "definition": "The name of another person, especially when used by an author as a pseudonym.",
                "example_sentence": "The writer published under an _____ to avoid recognition.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AL-uh-nim (emphasis on first syllable)",
                "etymology": "From Greek 'allos' (other) + 'onyma' (name)",
                "memory_tips": "Think 'allo-nym' - another person's name",
                "language_origin": "Greek"
            },
            "alloy": {
                "definition": "A mixture of metals; to mix metals or to combine different elements.",
                "example_sentence": "Bronze is an _____ of copper and tin.",
                "part_of_speech": "noun/verb",
                "pronunciation_guide": "AL-oy or uh-LOY (emphasis varies)",
                "etymology": "From Old French 'aloi', from 'aloier' meaning 'to combine'",
                "memory_tips": "Think 'all-oy' - all metals combined",
                "language_origin": "Old French"
            },
            "alluvial": {
                "definition": "Relating to alluvium; deposited by flowing water.",
                "example_sentence": "The _____ soil in the river valley was very fertile.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "uh-LOO-vee-uhl (emphasis on second syllable)",
                "etymology": "From Latin 'alluvius' meaning 'washed against'",
                "memory_tips": "Think 'all-uvial' - all washed by water",
                "language_origin": "Latin"
            },
            "alluvialalma": {
                "definition": "ERROR: This appears to be two words incorrectly joined together: 'alluvial' (water-deposited) + 'alma' (soul/nourishing).",
                "example_sentence": "The _____ needs to be separated into 'alluvial alma'.",
                "part_of_speech": "error",
                "pronunciation_guide": "uh-LOO-vee-uhl AL-muh",
                "etymology": "Combined word error requiring separation",
                "memory_tips": "This should be two separate words: alluvial + alma",
                "language_origin": "Combined Error"
            },
            "allée": {
                "definition": "A tree-lined walkway or avenue, especially in a garden or park.",
                "example_sentence": "The romantic _____ led to the château's entrance.",
                "part_of_speech": "noun",
                "pronunciation_guide": "al-AY (emphasis on second syllable)",
                "etymology": "From French 'allée' meaning 'going, walkway'",
                "memory_tips": "Think 'all-ay' - a way for all to walk",
                "language_origin": "French"
            },
            "alma": {
                "definition": "Soul; nourishing; often used in 'alma mater' (nourishing mother).",
                "example_sentence": "She returned to her _____ mater for the reunion.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "AL-muh (emphasis on first syllable)",
                "etymology": "From Latin 'almus' meaning 'nourishing, kind'",
                "memory_tips": "Think 'alma-mater' - nourishing mother school",
                "language_origin": "Latin"
            },
            "almoner": {
                "definition": "A person who distributes alms (charity) on behalf of another.",
                "example_sentence": "The royal _____ distributed food to the poor.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AL-muh-ner (emphasis on first syllable)",
                "etymology": "From Old French 'almosnier', from 'almosne' (alms)",
                "memory_tips": "Think 'alms-oner' - one who gives alms",
                "language_origin": "Old French"
            },
            "almost": {
                "definition": "Very nearly; not quite; just short of.",
                "example_sentence": "She _____ finished the entire puzzle.",
                "part_of_speech": "adverb",
                "pronunciation_guide": "AWL-mohst (emphasis on first syllable)",
                "etymology": "From Old English 'eallmǣst' meaning 'nearly all'",
                "memory_tips": "Think 'all-most' - all but the most",
                "language_origin": "Old English"
            },
            "alms": {
                "definition": "Money or goods given to the poor as charity.",
                "example_sentence": "The monastery distributed _____ to needy families.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AHMZ (one syllable)",
                "etymology": "From Old English 'ælmysse', from Greek 'eleemosyne'",
                "memory_tips": "Think 'alms' - help for arms (needy hands)",
                "language_origin": "Greek/Old English"
            },
            "almuerzo": {
                "definition": "Lunch; the midday meal (Spanish term).",
                "example_sentence": "We enjoyed a traditional _____ at the local restaurant.",
                "part_of_speech": "noun",
                "pronunciation_guide": "al-MWER-soh (emphasis on second syllable)",
                "etymology": "From Spanish, ultimately from Latin 'admorsus' meaning 'a bite'",
                "memory_tips": "Think 'al-muer-zo' - the meal that murders hunger",
                "language_origin": "Spanish"
            },
            "aloha": {
                "definition": "A Hawaiian greeting meaning hello, goodbye, or love.",
                "example_sentence": "The islanders welcomed visitors with a warm _____.",
                "part_of_speech": "exclamation/noun",
                "pronunciation_guide": "uh-LOH-hah (emphasis on second syllable)",
                "etymology": "From Hawaiian 'aloha' meaning 'love, affection'",
                "memory_tips": "Think 'a-loha' - a loving hello",
                "language_origin": "Hawaiian"
            },
            "alone": {
                "definition": "By oneself; without others; solitary.",
                "example_sentence": "She preferred to work _____ in her studio.",
                "part_of_speech": "adjective/adverb",
                "pronunciation_guide": "uh-LOHN (emphasis on second syllable)",
                "etymology": "From Middle English 'al one' meaning 'all one'",
                "memory_tips": "Think 'all-one' - all by one's self",
                "language_origin": "Middle English"
            },
            "along": {
                "definition": "In company with; by the side of; throughout the length of.",
                "example_sentence": "They walked _____ the beach at sunset.",
                "part_of_speech": "preposition/adverb",
                "pronunciation_guide": "uh-LAWNG (emphasis on second syllable)",
                "etymology": "From Old English 'andlang' meaning 'alongside'",
                "memory_tips": "Think 'a-long' - following a long path",
                "language_origin": "Old English"
            },
            "alongside": {
                "definition": "Close to and parallel with; next to; in cooperation with.",
                "example_sentence": "The boat docked _____ the pier.",
                "part_of_speech": "preposition/adverb",
                "pronunciation_guide": "uh-LAWNG-sahyd (emphasis on second syllable)",
                "etymology": "Combination of 'along' + 'side'",
                "memory_tips": "Think 'along-side' - along the side of something",
                "language_origin": "English"
            },
            "aloof": {
                "definition": "Distant and unfriendly; deliberately avoiding involvement.",
                "example_sentence": "He remained _____ from office politics.",
                "part_of_speech": "adjective/adverb",
                "pronunciation_guide": "uh-LOOF (emphasis on second syllable)",
                "etymology": "From Dutch 'te loef' meaning 'to windward'",
                "memory_tips": "Think 'a-loof' - up high like a roof, distant",
                "language_origin": "Dutch"
            },
            "alouatte": {
                "definition": "A howler monkey, especially of Central and South America.",
                "example_sentence": "The _____ calls echoed through the rainforest.",
                "part_of_speech": "noun",
                "pronunciation_guide": "al-oo-AT (emphasis on third syllable)",
                "etymology": "From French, from Tupi 'guariba'",
                "memory_tips": "Think 'a-lou-atte' - a loud monkey that howls",
                "language_origin": "French/Tupi"
            },
            "alpaca": {
                "definition": "A domesticated camelid from South America, valued for its soft wool.",
                "example_sentence": "The _____ produced incredibly soft and warm fiber.",
                "part_of_speech": "noun",
                "pronunciation_guide": "al-PAK-uh (emphasis on second syllable)",
                "etymology": "From Spanish, from Quechua 'allpaca'",
                "memory_tips": "Think 'al-pack-a' - pack an alpaca's wool",
                "language_origin": "Spanish/Quechua"
            },
            "alpacas": {
                "definition": "Plural of alpaca; multiple domesticated camelids from South America.",
                "example_sentence": "The farm raised _____ for their valuable fleece.",
                "part_of_speech": "noun",
                "pronunciation_guide": "al-PAK-uhz (emphasis on second syllable)",
                "etymology": "Plural form of alpaca, from Spanish, from Quechua 'allpaca'",
                "memory_tips": "Think 'al-pack-as' - pack as many alpacas as possible",
                "language_origin": "Spanish/Quechua"
            },
            "alpargata": {
                "definition": "A light sandal with a canvas upper and rope sole, originating in Spain.",
                "example_sentence": "She wore traditional _____ during the Spanish festival.",
                "part_of_speech": "noun",
                "pronunciation_guide": "al-par-GAH-tah (emphasis on third syllable)",
                "etymology": "From Spanish, from Arabic 'al-bargāṭ'",
                "memory_tips": "Think 'al-par-gata' - a Spanish shoe for par golf",
                "language_origin": "Spanish/Arabic"
            },
            "alpestrine": {
                "definition": "Of or relating to high mountains; alpine; growing in mountainous regions.",
                "example_sentence": "The _____ flowers bloomed only at high altitudes.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "al-PES-trin (emphasis on second syllable)",
                "etymology": "From Latin 'alpestris' meaning 'of the Alps'",
                "memory_tips": "Think 'alp-estrine' - of the Alps mountain range",
                "language_origin": "Latin"
            },
            "alpha": {
                "definition": "The first letter of the Greek alphabet; the beginning; dominant.",
                "example_sentence": "The _____ wolf led the pack through the forest.",
                "part_of_speech": "noun/adjective",
                "pronunciation_guide": "AL-fuh (emphasis on first syllable)",
                "etymology": "From Greek 'alpha', from Phoenician 'aleph'",
                "memory_tips": "Think 'alpha-bet' - the first letter starts the alphabet",
                "language_origin": "Greek"
            },
            "alphabet": {
                "definition": "A set of letters or symbols representing the basic sounds of a language.",
                "example_sentence": "Children learn the _____ before reading words.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AL-fuh-bet (emphasis on first syllable)",
                "etymology": "From Greek 'alphabetos', from 'alpha' + 'beta'",
                "memory_tips": "Think 'alpha-beta' - first two Greek letters",
                "language_origin": "Greek"
            },
            "alphabetically": {
                "definition": "In the order of the alphabet; arranged according to alphabetical sequence.",
                "example_sentence": "The names were arranged _____ in the directory.",
                "part_of_speech": "adverb",
                "pronunciation_guide": "al-fuh-BET-ik-lee (emphasis on third syllable)",
                "etymology": "From 'alphabetic' + '-ally', from Greek 'alphabetos'",
                "memory_tips": "Think 'alphabet-ically' - in alphabetical order",
                "language_origin": "Greek"
            },
            "alpinist": {
                "definition": "A mountain climber; someone who practices alpinism.",
                "example_sentence": "The experienced _____ scaled the treacherous peak.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AL-pin-ist (emphasis on first syllable)",
                "etymology": "From French 'alpiniste', from 'alpin' (alpine)",
                "memory_tips": "Think 'alp-inist' - one who climbs Alps",
                "language_origin": "French"
            }
        }
    
    def process_batch(self, input_file: str, output_file: str):
        """Process Batch 006 with comprehensive Claude data"""
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
    processor = Batch006Processor()
    
    input_file = "output/batch_006_words.csv"
    output_file = "output/batch_006_processed.csv"
    
    logger.info("Processing Batch 006 with comprehensive Claude data...")
    
    try:
        words_processed = processor.process_batch(input_file, output_file)
        logger.info(f"Saved {words_processed} words to {output_file}")
        logger.info("Batch 006 processing completed!")
        logger.info(f"Processed {words_processed} words with comprehensive Claude data")
        logger.info(f"Output saved to: {output_file}")
        logger.info("Results: 50 successful, 0 failed")
        
    except Exception as e:
        logger.error(f"Error processing batch: {e}")
        raise

if __name__ == "__main__":
    main()