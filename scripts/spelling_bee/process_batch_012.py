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

class Batch012Processor:
    def __init__(self):
        self.word_data = {
            "aretalogy": {
                "definition": "A form of ancient biography that praises the virtues and miraculous deeds of gods, heroes, or distinguished persons.",
                "example_sentence": "The scholar specialized in studying ancient _____ texts that celebrated heroic achievements.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ar-uh-TAL-uh-jee (emphasis on third syllable)",
                "etymology": "From Greek 'arete' (virtue, excellence) + 'logos' (word, study)",
                "memory_tips": "Think 'arete-logy' - the study of virtue and excellence",
                "language_origin": "Greek"
            },
            "argot": {
                "definition": "The specialized vocabulary and idioms of a particular group, especially those used by criminals or other subcultures.",
                "example_sentence": "The detective had to learn the street _____ to understand the suspects' conversations.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-got (emphasis on first syllable)",
                "etymology": "From French 'argot', possibly from 'ergot' (cockspur), referring to claws",
                "memory_tips": "Think 'argot' - the special code language of particular groups",
                "language_origin": "French"
            },
            "argue": {
                "definition": "To give reasons for or against something; to quarrel or disagree; to maintain in reasoning.",
                "example_sentence": "The lawyers will _____ their case before the jury next week.",
                "part_of_speech": "verb",
                "pronunciation_guide": "AR-gyoo (emphasis on first syllable)",
                "etymology": "From Latin 'arguere' meaning 'to make clear, prove'",
                "memory_tips": "Think 'argue' - making your point clear through reasoning",
                "language_origin": "Latin"
            },
            "argument": {
                "definition": "A reason given for or against a matter; a disagreement or quarrel; a discussion involving differing points of view.",
                "example_sentence": "Her _____ for increasing the budget was very persuasive.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-gyuh-munt (emphasis on first syllable)",
                "etymology": "From Latin 'argumentum', from 'arguere' (to make clear)",
                "memory_tips": "Think 'argument' - making your reasoning clear",
                "language_origin": "Latin"
            },
            "argumentative": {
                "definition": "Given to arguing; characterized by systematic reasoning; inclined to disagree or debate.",
                "example_sentence": "The _____ student questioned every point the teacher made.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "ar-gyuh-MEN-tuh-tiv (emphasis on third syllable)",
                "etymology": "From Latin 'argumentum' + '-ative' (tending to)",
                "memory_tips": "Think 'argument-ative' - tending to argue or debate",
                "language_origin": "Latin"
            },
            "argyria": {
                "definition": "A medical condition caused by excessive exposure to silver, resulting in blue-gray discoloration of the skin.",
                "example_sentence": "The jeweler developed _____ after years of working with silver compounds.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ar-JIR-ee-uh (emphasis on second syllable)",
                "etymology": "From Greek 'argyros' meaning 'silver'",
                "memory_tips": "Think 'argyria' - silver (argyros) poisoning turning skin gray",
                "language_origin": "Greek"
            },
            "arid": {
                "definition": "Very dry, especially having insufficient rainfall to support vegetation; lacking in interest or excitement.",
                "example_sentence": "The _____ desert landscape stretched endlessly under the blazing sun.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "AR-id (emphasis on first syllable)",
                "etymology": "From Latin 'aridus', from 'arere' (to be dry)",
                "memory_tips": "Think 'arid' - air that's dried out, lacking moisture",
                "language_origin": "Latin"
            },
            "arietta": {
                "definition": "A short aria; a brief solo vocal piece, typically in an opera or oratorio.",
                "example_sentence": "The soprano performed a beautiful _____ that captivated the entire audience.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ar-ee-ET-tuh (emphasis on third syllable)",
                "etymology": "From Italian 'arietta', diminutive of 'aria'",
                "memory_tips": "Think 'arietta' - a little aria, a short solo song",
                "language_origin": "Italian"
            },
            "aristoi": {
                "definition": "The best or most excellent people; the aristocracy or nobility in ancient Greek society.",
                "example_sentence": "Plato believed that the _____ should rule society through their wisdom and virtue.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ah-RIS-toy (emphasis on second syllable)",
                "etymology": "From Greek 'aristos' meaning 'best, most excellent'",
                "memory_tips": "Think 'aristoi' - the best (aristos) people in society",
                "language_origin": "Greek"
            },
            "arithmetic": {
                "definition": "The branch of mathematics dealing with basic operations like addition, subtraction, multiplication, and division.",
                "example_sentence": "The students practiced mental _____ to improve their calculation speed.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-RITH-muh-tik (emphasis on second syllable)",
                "etymology": "From Greek 'arithmetikos', from 'arithmos' (number)",
                "memory_tips": "Think 'arith-metic' - the art of numbers (arithmos)",
                "language_origin": "Greek"
            },
            "armadillo": {
                "definition": "A small mammal with a leathery armor shell, native to South and Central America.",
                "example_sentence": "The _____ rolled into a ball when threatened by the approaching predator.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ar-muh-DIL-oh (emphasis on third syllable)",
                "etymology": "From Spanish 'armadillo', diminutive of 'armado' (armed)",
                "memory_tips": "Think 'armadillo' - the little armored animal",
                "language_origin": "Spanish"
            },
            "armaments": {
                "definition": "Military weapons and equipment; the process of equipping for war.",
                "example_sentence": "The treaty called for reducing nuclear _____ worldwide.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-muh-munts (emphasis on first syllable)",
                "etymology": "From Latin 'armamenta', from 'armare' (to arm)",
                "memory_tips": "Think 'armaments' - equipment for arming and warfare",
                "language_origin": "Latin"
            },
            "armature": {
                "definition": "The rotating part of an electric motor or generator; a framework used to support something being sculpted.",
                "example_sentence": "The sculptor built a wire _____ before adding the clay to create the statue.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-muh-chur (emphasis on first syllable)",
                "etymology": "From Latin 'armatura', from 'armare' (to arm, equip)",
                "memory_tips": "Think 'armature' - the framework that arms or supports something",
                "language_origin": "Latin"
            },
            "armies": {
                "definition": "Large organized groups of soldiers; forces prepared for war; large numbers of people or things.",
                "example_sentence": "The opposing _____ faced each other across the battlefield.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-meez (emphasis on first syllable)",
                "etymology": "From Old French 'armee', from Latin 'armata' (armed force)",
                "memory_tips": "Think 'armies' - groups of armed forces",
                "language_origin": "Latin"
            },
            "armistice": {
                "definition": "An agreement to stop fighting; a truce, especially one ending a war.",
                "example_sentence": "The _____ was signed on November 11, 1918, ending World War I.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-muh-stis (emphasis on first syllable)",
                "etymology": "From Latin 'armistitium', from 'arma' (arms) + 'sistere' (to stop)",
                "memory_tips": "Think 'armi-stice' - stopping the arms or weapons",
                "language_origin": "Latin"
            },
            "arms": {
                "definition": "Weapons; the upper limbs of the human body; branches of a tree; sections of an organization.",
                "example_sentence": "The peace treaty required both nations to reduce their stockpile of _____.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ARMZ (single syllable)",
                "etymology": "From Old English 'earm' and Latin 'arma' (weapons)",
                "memory_tips": "Think 'arms' - both body parts and weapons for fighting",
                "language_origin": "Old English/Latin"
            },
            "army": {
                "definition": "A large organized force of soldiers for fighting on land; a large number of people or things.",
                "example_sentence": "The _____ marched through the capital in a victory parade.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-mee (emphasis on first syllable)",
                "etymology": "From Old French 'armee', from Latin 'armata' (armed)",
                "memory_tips": "Think 'army' - an armed group organized for war",
                "language_origin": "Latin"
            },
            "aromatherapy": {
                "definition": "The use of essential oils and aromatic compounds for psychological and physical well-being.",
                "example_sentence": "The spa offered _____ treatments using lavender and eucalyptus oils.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-roh-muh-THER-uh-pee (emphasis on fourth syllable)",
                "etymology": "From Greek 'aroma' (spice) + 'therapeia' (healing)",
                "memory_tips": "Think 'aroma-therapy' - healing through pleasant scents",
                "language_origin": "Greek"
            },
            "around": {
                "definition": "On all sides; in a circle; approximately; in the vicinity of.",
                "example_sentence": "The children gathered _____ the storyteller to hear the tale.",
                "part_of_speech": "adverb/preposition",
                "pronunciation_guide": "uh-ROWND (emphasis on second syllable)",
                "etymology": "From 'a-' + 'round'",
                "memory_tips": "Think 'around' - in a round circle or surrounding",
                "language_origin": "English"
            },
            "arpeggio": {
                "definition": "A musical technique where notes in a chord are played in succession rather than simultaneously.",
                "example_sentence": "The pianist's graceful _____ added elegance to the classical piece.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ar-PEJ-ee-oh (emphasis on second syllable)",
                "etymology": "From Italian 'arpeggiare' meaning 'to play the harp'",
                "memory_tips": "Think 'arpeggio' - playing notes like plucking a harp (arpa)",
                "language_origin": "Italian"
            },
            "arpeggiolupine": {
                "definition": "COMBINED WORD ERROR - appears to be 'arpeggio' + 'lupine' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "arraign": {
                "definition": "To call before a court to answer charges; to accuse or criticize severely.",
                "example_sentence": "The suspect will be arraigned in court tomorrow morning.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-RAYN (emphasis on second syllable)",
                "etymology": "From Old French 'araisnier', from Latin 'ad' + 'ratio' (account)",
                "memory_tips": "Think 'arraign' - calling to account for charges",
                "language_origin": "French"
            },
            "arrange": {
                "definition": "To put in order; to organize or plan; to adapt music for particular instruments or voices.",
                "example_sentence": "Please _____ the chairs in a circle for the meeting.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-RAYNJ (emphasis on second syllable)",
                "etymology": "From Old French 'arangier', from 'a-' + 'rangier' (to put in a row)",
                "memory_tips": "Think 'arrange' - putting things in range or order",
                "language_origin": "French"
            },
            "arrayed": {
                "definition": "Arranged in order; dressed or clothed, especially in fine attire; displayed impressively.",
                "example_sentence": "The soldiers were _____ in perfect formation for the inspection.",
                "part_of_speech": "verb/adjective",
                "pronunciation_guide": "uh-RAYD (emphasis on second syllable)",
                "etymology": "From Old French 'arayer', from 'a-' + Germanic 'raid' (ready)",
                "memory_tips": "Think 'arrayed' - made ready and arranged in order",
                "language_origin": "French"
            },
            "arrearage": {
                "definition": "The state of being behind in payments; overdue debts or unpaid obligations.",
                "example_sentence": "The tenant faced eviction due to several months of rent _____.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-REER-ij (emphasis on second syllable)",
                "etymology": "From Old French 'arerage', from 'arere' (behind)",
                "memory_tips": "Think 'arrear-age' - the condition of being in arrears",
                "language_origin": "French"
            },
            "arrested": {
                "definition": "Seized by legal authority; stopped or halted; captured and held.",
                "example_sentence": "The suspect was _____ after a brief chase through the neighborhood.",
                "part_of_speech": "verb/adjective",
                "pronunciation_guide": "uh-REST-id (emphasis on second syllable)",
                "etymology": "From Old French 'arester', from Latin 'ad' + 'restare' (to remain)",
                "memory_tips": "Think 'arrested' - made to remain or stop in place",
                "language_origin": "Latin"
            },
            "arret": {
                "definition": "A decision or decree by a court; a judgment, especially in French legal systems.",
                "example_sentence": "The court's _____ established an important legal precedent.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ah-RAY (French pronunciation)",
                "etymology": "From French 'arrêt', from 'arrêter' (to stop, arrest)",
                "memory_tips": "Think 'arret' - a court's decision that stops or settles a matter",
                "language_origin": "French"
            },
            "arrieros": {
                "definition": "Spanish term for muleteers; people who drive or tend pack mules.",
                "example_sentence": "The _____ guided their mules along the mountain trail carrying supplies.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ah-ree-EH-rohs (Spanish pronunciation)",
                "etymology": "From Spanish 'arriero', from 'arria' (drove of beasts)",
                "memory_tips": "Think 'arrieros' - those who drive animals in a drove (arria)",
                "language_origin": "Spanish"
            },
            "arrive": {
                "definition": "To reach a destination; to come to a place; to achieve success or recognition.",
                "example_sentence": "The train is scheduled to _____ at the station at 3:15 PM.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-RYVE (emphasis on second syllable)",
                "etymology": "From Old French 'ariver', from Latin 'ad' + 'ripa' (shore)",
                "memory_tips": "Think 'arrive' - reaching the shore or destination",
                "language_origin": "Latin"
            },
            "arrogant": {
                "definition": "Having an exaggerated sense of one's importance; behaving in a superior manner toward others.",
                "example_sentence": "His _____ attitude made it difficult for others to work with him.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "AR-uh-gunt (emphasis on first syllable)",
                "etymology": "From Latin 'arrogans', from 'arrogare' (to claim for oneself)",
                "memory_tips": "Think 'arrogant' - claiming more for yourself than deserved",
                "language_origin": "Latin"
            },
            "arrondissement": {
                "definition": "An administrative district in France, especially a subdivision of a department or large city.",
                "example_sentence": "They lived in the fashionable 16th _____ of Paris.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ah-ron-DEES-mahn (French pronunciation)",
                "etymology": "From French 'arrondissement', from 'arrondir' (to make round)",
                "memory_tips": "Think 'arrondissement' - a rounded administrative district",
                "language_origin": "French"
            },
            "arrows": {
                "definition": "Projectiles shot from bows; symbols indicating direction; pointed shapes used for guidance.",
                "example_sentence": "The archer's _____ hit the target with remarkable accuracy.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-ohz (emphasis on first syllable)",
                "etymology": "From Old English 'arewe', from Old Norse 'or'",
                "memory_tips": "Think 'arrows' - pointed projectiles that fly straight to targets",
                "language_origin": "Old English"
            },
            "arsenic": {
                "definition": "A highly toxic chemical element used historically as a poison; a metalloid with various industrial uses.",
                "example_sentence": "The detective found traces of _____ in the victim's tea cup.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-suh-nik (emphasis on first syllable)",
                "etymology": "From Greek 'arsenikon', from Persian 'zarnik' (yellow orpiment)",
                "memory_tips": "Think 'arsenic' - the deadly element from ancient Greek knowledge",
                "language_origin": "Greek"
            },
            "artery": {
                "definition": "A blood vessel that carries blood away from the heart; a main road or transportation route.",
                "example_sentence": "The blocked _____ required immediate surgical intervention.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-tur-ee (emphasis on first syllable)",
                "etymology": "From Latin 'arteria', from Greek 'arteria' (windpipe, artery)",
                "memory_tips": "Think 'artery' - the vital tubes that carry life-giving blood",
                "language_origin": "Greek"
            },
            "arteryornithology": {
                "definition": "COMBINED WORD ERROR - appears to be 'artery' + 'ornithology' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "artesian": {
                "definition": "Relating to a type of well that taps into confined groundwater under pressure, causing water to rise naturally.",
                "example_sentence": "The _____ well provided fresh water without the need for pumping.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "ar-TEE-zhun (emphasis on second syllable)",
                "etymology": "From Artois, a region in France where such wells were first drilled",
                "memory_tips": "Think 'artesian' - wells from Artois that naturally flow upward",
                "language_origin": "French"
            },
            "arthralgia": {
                "definition": "Joint pain; aching or pain in one or more joints without inflammation.",
                "example_sentence": "The patient complained of _____ in her knees after the long hike.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ar-THRAL-jee-uh (emphasis on second syllable)",
                "etymology": "From Greek 'arthron' (joint) + 'algos' (pain)",
                "memory_tips": "Think 'arthr-algia' - pain (algia) in the joints (arthron)",
                "language_origin": "Greek"
            },
            "arthurian": {
                "definition": "Relating to King Arthur and the legends associated with him and his knights.",
                "example_sentence": "The professor specialized in _____ literature and medieval romance.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "ar-THUR-ee-un (emphasis on second syllable)",
                "etymology": "From King Arthur, legendary British king",
                "memory_tips": "Think 'Arthurian' - relating to King Arthur's legendary realm",
                "language_origin": "English"
            },
            "artifice": {
                "definition": "Clever skill; cunning or deceitful behavior; an artful stratagem or trick.",
                "example_sentence": "The magician's performance relied on skillful _____ to create illusions.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AR-tuh-fis (emphasis on first syllable)",
                "etymology": "From Latin 'artificium', from 'artifex' (craftsman)",
                "memory_tips": "Think 'artifice' - the craft (art) of skilled deception",
                "language_origin": "Latin"
            },
            "artificial": {
                "definition": "Made by humans rather than nature; synthetic; not genuine or natural.",
                "example_sentence": "The _____ flowers looked so realistic that many people thought they were real.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "ar-tuh-FISH-ul (emphasis on third syllable)",
                "etymology": "From Latin 'artificialis', from 'artificium' (craft)",
                "memory_tips": "Think 'artificial' - made by human craft rather than nature",
                "language_origin": "Latin"
            },
            "artillery": {
                "definition": "Large guns and rocket launchers used in warfare; the branch of an army that uses such weapons.",
                "example_sentence": "The _____ bombardment could be heard for miles around the battlefield.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ar-TIL-ur-ee (emphasis on second syllable)",
                "etymology": "From Old French 'artillerie', from 'artillier' (to arm)",
                "memory_tips": "Think 'artillery' - the art of using large weapons in warfare",
                "language_origin": "French"
            },
            "artilleryquotient": {
                "definition": "COMBINED WORD ERROR - appears to be 'artillery' + 'quotient' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "artistic": {
                "definition": "Having creative skill or ability; relating to art; showing imagination and skill.",
                "example_sentence": "Her _____ talents were evident in the beautiful paintings she created.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "ar-TIS-tik (emphasis on second syllable)",
                "etymology": "From Latin 'artisticus', from 'ars' (art)",
                "memory_tips": "Think 'artistic' - having the qualities of art and creativity",
                "language_origin": "Latin"
            },
            "arts": {
                "definition": "Creative activities such as painting, music, literature, and dance; subjects of study other than sciences.",
                "example_sentence": "The university had an excellent _____ program with renowned professors.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ARTS (single syllable)",
                "etymology": "From Latin 'ars' meaning 'skill, craft'",
                "memory_tips": "Think 'arts' - the various skills and crafts of creative expression",
                "language_origin": "Latin"
            },
            "asado": {
                "definition": "A South American barbecue tradition, especially popular in Argentina; grilled or roasted meat.",
                "example_sentence": "The family gathered for a traditional _____ featuring grilled beef and chorizo.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ah-SAH-doh (Spanish pronunciation)",
                "etymology": "From Spanish 'asado', from 'asar' (to roast)",
                "memory_tips": "Think 'asado' - roasted meat in South American style",
                "language_origin": "Spanish"
            },
            "ascension": {
                "definition": "The act of rising or moving upward; a spiritual rising; specifically, Christ's rising to heaven.",
                "example_sentence": "The balloon's _____ into the clouds was graceful and steady.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-SEN-shun (emphasis on second syllable)",
                "etymology": "From Latin 'ascensio', from 'ascendere' (to climb up)",
                "memory_tips": "Think 'ascension' - ascending or climbing upward",
                "language_origin": "Latin"
            },
            "ascertain": {
                "definition": "To discover or determine with certainty; to find out for sure; to establish as fact.",
                "example_sentence": "The detective worked to _____ the exact time of the incident.",
                "part_of_speech": "verb",
                "pronunciation_guide": "as-ur-TAYN (emphasis on third syllable)",
                "etymology": "From Old French 'acertener', from 'certain'",
                "memory_tips": "Think 'ascertain' - to make certain or sure about something",
                "language_origin": "French"
            },
            "ascetic": {
                "definition": "Practicing severe self-discipline; relating to a lifestyle of strict simplicity; one who practices such discipline.",
                "example_sentence": "The monk lived an _____ life, owning only the bare necessities.",
                "part_of_speech": "adjective/noun",
                "pronunciation_guide": "uh-SET-ik (emphasis on second syllable)",
                "etymology": "From Greek 'asketikos', from 'askein' (to exercise, train)",
                "memory_tips": "Think 'ascetic' - exercising strict self-discipline and simplicity",
                "language_origin": "Greek"
            },
            "ascites": {
                "definition": "A medical condition involving the accumulation of fluid in the abdomen; abdominal swelling due to fluid buildup.",
                "example_sentence": "The patient's _____ was caused by liver disease and required immediate treatment.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-SYE-teez (emphasis on second syllable)",
                "etymology": "From Greek 'askites', from 'askos' (wineskin, bag)",
                "memory_tips": "Think 'ascites' - abdomen swollen like a bag (askos) with fluid",
                "language_origin": "Greek"
            },
            "ascribe": {
                "definition": "To attribute or credit to a particular cause, source, or origin; to assign as belonging to.",
                "example_sentence": "Historians _____ the fall of the empire to economic and political factors.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-SKRYB (emphasis on second syllable)",
                "etymology": "From Latin 'ascribere', from 'ad' (to) + 'scribere' (to write)",
                "memory_tips": "Think 'ascribe' - writing something down as belonging to a source",
                "language_origin": "Latin"
            }
        }
        
        # Combined word errors detected in this batch
        self.combined_word_errors = [
            "arpeggiolupine",
            "arteryornithology", 
            "artilleryquotient"
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
    processor = Batch012Processor()
    input_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_012_words.csv"
    output_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_012_processed.csv"
    
    processor.process_batch(input_file, output_file)
    
    print(f"\nBatch 012 Processing Complete!")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Combined word errors flagged: {len(processor.combined_word_errors)}")

if __name__ == "__main__":
    main()