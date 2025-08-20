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

class Batch009Processor:
    def __init__(self):
        self.word_data = {
            "animus": {
                "definition": "A feeling of strong dislike, ill will, or resentment; hostility or antagonism; also refers to the spirit or motivating force behind an action.",
                "example_sentence": "There was clear _____ between the two rival teams after the controversial game.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AN-uh-mus (emphasis on first syllable)",
                "etymology": "From Latin 'animus' meaning 'mind, spirit, soul'",
                "memory_tips": "Think 'animosity' - animus is the hostile spirit or mind",
                "language_origin": "Latin"
            },
            "animustrillium": {
                "definition": "COMBINED WORD ERROR - appears to be 'animus' + 'trillium' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "anionic": {
                "definition": "Relating to or containing anions; having a negative electrical charge in chemical compounds.",
                "example_sentence": "The _____ surfactant helped reduce the surface tension of the solution.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "an-eye-ON-ik (emphasis on third syllable)",
                "etymology": "From Greek 'anion' (going up) + '-ic' suffix",
                "memory_tips": "Think 'an-ionic' - relating to negative ions",
                "language_origin": "Greek"
            },
            "anise": {
                "definition": "An aromatic plant with seeds that have a licorice-like flavor, used in cooking and medicine.",
                "example_sentence": "The chef added _____ seeds to give the bread a distinctive licorice flavor.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AN-is (emphasis on first syllable)",
                "etymology": "From Greek 'anison', possibly from Egyptian origins",
                "memory_tips": "Think 'anise' - the spice that tastes like licorice",
                "language_origin": "Greek"
            },
            "aniseikonia": {
                "definition": "A visual condition where the two eyes perceive images of different sizes, causing depth perception problems.",
                "example_sentence": "The patient's _____ made it difficult to judge distances accurately.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-eye-sy-KOH-nee-uh (emphasis on fourth syllable)",
                "etymology": "From Greek 'anisos' (unequal) + 'eikon' (image)",
                "memory_tips": "Think 'anise-icon-ia' - unequal images seen by the eyes",
                "language_origin": "Greek"
            },
            "anjou": {
                "definition": "A variety of pear with a sweet, buttery flavor; also refers to a historical region in France.",
                "example_sentence": "The _____ pears were perfectly ripe and ready for harvest.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AHN-zhoo (French pronunciation)",
                "etymology": "From Anjou, a region in western France where the pear variety originated",
                "memory_tips": "Think 'Anjou' - the French region famous for sweet pears",
                "language_origin": "French"
            },
            "ankh": {
                "definition": "An ancient Egyptian hieroglyphic symbol shaped like a cross with a loop at the top, representing life.",
                "example_sentence": "The archaeologist discovered an _____ carved into the tomb wall.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AHNK (rhymes with 'honk')",
                "etymology": "From ancient Egyptian, meaning 'life' or 'breath of life'",
                "memory_tips": "Think 'ankh' - the Egyptian symbol of eternal life",
                "language_origin": "Egyptian"
            },
            "anklet": {
                "definition": "A piece of jewelry worn around the ankle; a short sock that reaches just above the ankle.",
                "example_sentence": "She wore a delicate silver _____ that jingled softly as she walked.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AHNK-lit (emphasis on first syllable)",
                "etymology": "From 'ankle' + diminutive suffix '-let'",
                "memory_tips": "Think 'ankle-let' - little jewelry for the ankle",
                "language_origin": "English"
            },
            "anne": {
                "definition": "A feminine given name; also refers to Queen Anne style architecture and furniture.",
                "example_sentence": "The _____ style chair featured elegant curved legs and upholstered seats.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AN (single syllable)",
                "etymology": "From Hebrew 'Hannah' meaning 'grace' or 'favor'",
                "memory_tips": "Think 'Anne' - a classic name meaning grace",
                "language_origin": "Hebrew"
            },
            "anneal": {
                "definition": "To heat and then cool metal or glass to reduce brittleness and internal stress; to strengthen through heat treatment.",
                "example_sentence": "The blacksmith had to _____ the steel blade to make it more durable.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-NEEL (emphasis on second syllable)",
                "etymology": "From Old English 'onaelan' meaning 'to set on fire'",
                "memory_tips": "Think 'an-neal' - to heal metal through controlled heating",
                "language_origin": "Old English"
            },
            "annexation": {
                "definition": "The action of adding or incorporating territory into an existing political unit such as a country or state.",
                "example_sentence": "The _____ of the territory sparked international controversy.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-ik-SAY-shun (emphasis on third syllable)",
                "etymology": "From Latin 'annexare' meaning 'to bind to'",
                "memory_tips": "Think 'annex-ation' - the act of adding territory by binding it",
                "language_origin": "Latin"
            },
            "annihilate": {
                "definition": "To destroy completely; to reduce to nothing; to defeat decisively.",
                "example_sentence": "The meteor impact threatened to _____ all life on the planet.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-NYE-uh-layt (emphasis on second syllable)",
                "etymology": "From Latin 'annihilare' meaning 'to reduce to nothing'",
                "memory_tips": "Think 'a-nihil-ate' - to make nothing (nihil = nothing)",
                "language_origin": "Latin"
            },
            "anniversary": {
                "definition": "The yearly recurrence of the date of a past event; a celebration commemorating such a date.",
                "example_sentence": "They celebrated their golden wedding _____ with a grand party.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-uh-VUR-suh-ree (emphasis on third syllable)",
                "etymology": "From Latin 'anniversarius' meaning 'returning yearly'",
                "memory_tips": "Think 'anni-versary' - yearly turning/returning",
                "language_origin": "Latin"
            },
            "anno": {
                "definition": "Latin word meaning 'in the year of'; commonly used in 'Anno Domini' (AD) to mark years.",
                "example_sentence": "The manuscript was dated _____ Domini 1453.",
                "part_of_speech": "adverb",
                "pronunciation_guide": "AN-oh (emphasis on first syllable)",
                "etymology": "From Latin 'annus' meaning 'year'",
                "memory_tips": "Think 'anno' - relating to the year, as in Anno Domini",
                "language_origin": "Latin"
            },
            "annotate": {
                "definition": "To add notes or comments to a text or diagram to explain or comment upon it.",
                "example_sentence": "Students were asked to _____ the poem with their interpretations.",
                "part_of_speech": "verb",
                "pronunciation_guide": "AN-uh-tayt (emphasis on first syllable)",
                "etymology": "From Latin 'annotare' meaning 'to mark'",
                "memory_tips": "Think 'anno-tate' - to note or mark with comments",
                "language_origin": "Latin"
            },
            "annual": {
                "definition": "Happening once every year; calculated over or covering a period of a year.",
                "example_sentence": "The company's _____ report showed significant growth in profits.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "AN-yoo-ul (emphasis on first syllable)",
                "etymology": "From Latin 'annualis', from 'annus' (year)",
                "memory_tips": "Think 'annu-al' - relating to one year",
                "language_origin": "Latin"
            },
            "annuity": {
                "definition": "A fixed sum of money paid to someone each year, typically as a pension or investment return.",
                "example_sentence": "The retirement _____ provided steady income throughout his golden years.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-NOO-uh-tee (emphasis on second syllable)",
                "etymology": "From Latin 'annuitas', from 'annus' (year)",
                "memory_tips": "Think 'annu-ity' - yearly payment or income",
                "language_origin": "Latin"
            },
            "annulment": {
                "definition": "The legal procedure of declaring a marriage null and void, as if it never happened.",
                "example_sentence": "The court granted an _____ based on evidence of fraud.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-NUL-munt (emphasis on second syllable)",
                "etymology": "From Latin 'annullare' meaning 'to make void'",
                "memory_tips": "Think 'annul-ment' - making something null and void",
                "language_origin": "Latin"
            },
            "annulmentorganized": {
                "definition": "COMBINED WORD ERROR - appears to be 'annulment' + 'organized' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "anodyne": {
                "definition": "A medicine that relieves pain; something that soothes or comforts; inoffensive or bland.",
                "example_sentence": "The doctor prescribed an _____ to ease the patient's chronic pain.",
                "part_of_speech": "noun/adjective",
                "pronunciation_guide": "AN-uh-dyne (emphasis on first syllable)",
                "etymology": "From Greek 'anodynos' meaning 'free from pain'",
                "memory_tips": "Think 'an-odyne' - without pain, pain-relieving",
                "language_origin": "Greek"
            },
            "anoint": {
                "definition": "To smear or rub with oil, especially as part of a religious ceremony; to choose or designate.",
                "example_sentence": "The priest will _____ the new king with sacred oil during the coronation.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-NOYNT (emphasis on second syllable)",
                "etymology": "From Old French 'enoindre', from Latin 'inungere' (to smear)",
                "memory_tips": "Think 'anoint' - to ceremonially oil or designate",
                "language_origin": "Latin"
            },
            "anole": {
                "definition": "A small tropical lizard that can change color, commonly kept as a pet; also called a chameleon.",
                "example_sentence": "The green _____ blended perfectly with the leaves in the terrarium.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-NOHL (emphasis on second syllable)",
                "etymology": "From Carib (indigenous Caribbean) language",
                "memory_tips": "Think 'anole' - the color-changing lizard from the Caribbean",
                "language_origin": "Carib"
            },
            "anoli": {
                "definition": "Plural or variant form of anole; small tropical lizards capable of color change.",
                "example_sentence": "The pet store had several _____ of different species for sale.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-NOH-lee (emphasis on second syllable)",
                "etymology": "From Carib (indigenous Caribbean) language, plural form",
                "memory_tips": "Think 'anoli' - multiple color-changing lizards",
                "language_origin": "Carib"
            },
            "anomaliped": {
                "definition": "Having irregularly formed feet; refers to birds with webbed or partially webbed toes.",
                "example_sentence": "The _____ waterfowl had partially webbed feet adapted for swimming.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "uh-NOM-uh-luh-ped (emphasis on second syllable)",
                "etymology": "From Greek 'anomalos' (irregular) + Latin 'pes' (foot)",
                "memory_tips": "Think 'anomali-ped' - irregular or unusual feet",
                "language_origin": "Greek/Latin"
            },
            "anomaly": {
                "definition": "Something that deviates from what is standard, normal, or expected; an irregularity.",
                "example_sentence": "The scientist noticed an _____ in the data that required further investigation.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-NOM-uh-lee (emphasis on second syllable)",
                "etymology": "From Greek 'anomalia' meaning 'irregularity'",
                "memory_tips": "Think 'anomaly' - something abnormal or irregular",
                "language_origin": "Greek"
            },
            "anonymity": {
                "definition": "The condition of being anonymous; having one's identity unknown or concealed.",
                "example_sentence": "The witness requested _____ for protection from potential retaliation.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-uh-NIM-uh-tee (emphasis on third syllable)",
                "etymology": "From Greek 'anonymos' meaning 'nameless'",
                "memory_tips": "Think 'anonym-ity' - the state of being nameless",
                "language_origin": "Greek"
            },
            "anorak": {
                "definition": "A waterproof jacket with a hood, designed for outdoor activities; originally an Inuit garment.",
                "example_sentence": "She wore her bright red _____ to stay dry during the hiking trip.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AN-uh-rak (emphasis on first syllable)",
                "etymology": "From Inuit (Greenlandic) 'annoraaq'",
                "memory_tips": "Think 'anorak' - Arctic-style hooded jacket from the Inuit",
                "language_origin": "Inuit"
            },
            "anosognosia": {
                "definition": "A neurological condition where a person is unaware of their own disability or illness.",
                "example_sentence": "The stroke patient's _____ prevented him from recognizing his paralysis.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-oh-sog-NOH-see-uh (emphasis on fourth syllable)",
                "etymology": "From Greek 'a-' (without) + 'nosos' (disease) + 'gnosis' (knowledge)",
                "memory_tips": "Think 'a-nosog-nosia' - without knowledge of one's illness",
                "language_origin": "Greek"
            },
            "another": {
                "definition": "One more; a different or additional person or thing of the same type.",
                "example_sentence": "Would you like _____ piece of cake with your coffee?",
                "part_of_speech": "determiner/pronoun",
                "pronunciation_guide": "uh-NUTH-ur (emphasis on second syllable)",
                "etymology": "From Middle English 'an other' meaning 'one other'",
                "memory_tips": "Think 'an-other' - one more or a different one",
                "language_origin": "Middle English"
            },
            "anserine": {
                "definition": "Relating to or resembling geese; goose-like; also refers to a chemical compound found in muscle tissue.",
                "example_sentence": "The bird's _____ characteristics made it easy to identify as a waterfowl.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "AN-suh-reen (emphasis on first syllable)",
                "etymology": "From Latin 'anserinus', from 'anser' (goose)",
                "memory_tips": "Think 'anser-ine' - relating to geese (anser = goose)",
                "language_origin": "Latin"
            },
            "answer": {
                "definition": "A response to a question; a solution to a problem; to respond or reply.",
                "example_sentence": "The student raised her hand to give the correct _____ to the math problem.",
                "part_of_speech": "noun/verb",
                "pronunciation_guide": "AN-sur (emphasis on first syllable)",
                "etymology": "From Old English 'andswaru', from 'and-' (against) + 'swerian' (to swear)",
                "memory_tips": "Think 'answer' - a response given against or in reply to a question",
                "language_origin": "Old English"
            },
            "antacid": {
                "definition": "A medicine that neutralizes stomach acid to relieve indigestion and heartburn.",
                "example_sentence": "She took an _____ tablet to relieve the burning sensation in her stomach.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ant-AS-id (emphasis on second syllable)",
                "etymology": "From 'anti-' (against) + 'acid'",
                "memory_tips": "Think 'ant-acid' - against acid, neutralizing stomach acid",
                "language_origin": "Modern English"
            },
            "antagonistic": {
                "definition": "Showing opposition or hostility; actively opposing or competing; unfriendly or hostile.",
                "example_sentence": "The two political parties maintained an _____ relationship throughout the debate.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "an-tag-uh-NIS-tik (emphasis on fourth syllable)",
                "etymology": "From Greek 'antagonistikos', from 'antagonistes' (opponent)",
                "memory_tips": "Think 'antagon-istic' - opposing like an antagonist",
                "language_origin": "Greek"
            },
            "antagonisticaffront": {
                "definition": "COMBINED WORD ERROR - appears to be 'antagonistic' + 'affront' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "antarctic": {
                "definition": "Relating to the south polar region; pertaining to Antarctica and its surrounding areas.",
                "example_sentence": "The _____ expedition required specialized equipment for extreme cold conditions.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "ant-ARK-tik (emphasis on second syllable)",
                "etymology": "From Greek 'antarktikos' meaning 'opposite to the north'",
                "memory_tips": "Think 'ant-arctic' - opposite to the Arctic, the southern polar region",
                "language_origin": "Greek"
            },
            "ante": {
                "definition": "A stake put up in poker before dealing; an amount paid in advance; to pay or put up as an ante.",
                "example_sentence": "Each player had to put up a five-dollar _____ before the cards were dealt.",
                "part_of_speech": "noun/verb",
                "pronunciation_guide": "AN-tee (emphasis on first syllable)",
                "etymology": "From Latin 'ante' meaning 'before'",
                "memory_tips": "Think 'ante' - what you put up before (ante) the game begins",
                "language_origin": "Latin"
            },
            "antechamber": {
                "definition": "A small room leading to a main room; a waiting room or anteroom.",
                "example_sentence": "Visitors waited in the elegant _____ before meeting with the ambassador.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AN-tee-chaym-bur (emphasis on first syllable)",
                "etymology": "From French 'antichambre', from 'anti-' (before) + 'chambre' (room)",
                "memory_tips": "Think 'ante-chamber' - the room that comes before the main chamber",
                "language_origin": "French"
            },
            "antelope": {
                "definition": "A swift-running, horn-bearing mammal found in Africa and Asia, related to goats and sheep.",
                "example_sentence": "The graceful _____ bounded across the African savanna with remarkable speed.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AN-tuh-lohp (emphasis on first syllable)",
                "etymology": "From Old French 'antelop', from Medieval Latin 'anthalopus'",
                "memory_tips": "Think 'antelope' - the swift-running horned animal of the plains",
                "language_origin": "Greek"
            },
            "antenatus": {
                "definition": "Relating to the period before birth; prenatal; occurring during pregnancy.",
                "example_sentence": "The _____ care program provided excellent support for expectant mothers.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "an-tee-NAY-tus (emphasis on third syllable)",
                "etymology": "From Latin 'ante' (before) + 'natus' (born)",
                "memory_tips": "Think 'ante-natus' - before birth, prenatal care",
                "language_origin": "Latin"
            },
            "antennas": {
                "definition": "Plural of antenna; sensory appendages on insects; devices for receiving radio or television signals.",
                "example_sentence": "The insect's sensitive _____ helped it detect chemical signals in the air.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-TEN-uhz (emphasis on second syllable)",
                "etymology": "From Latin 'antenna' meaning 'sail yard'",
                "memory_tips": "Think 'antennas' - like ship's sail yards, they extend out to receive signals",
                "language_origin": "Latin"
            },
            "anthropology": {
                "definition": "The study of human societies, cultures, and their development throughout history.",
                "example_sentence": "Her degree in _____ helped her understand diverse cultural practices around the world.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-thruh-POL-uh-jee (emphasis on third syllable)",
                "etymology": "From Greek 'anthropos' (human) + 'logos' (study)",
                "memory_tips": "Think 'anthropo-logy' - the study (logos) of humans (anthropos)",
                "language_origin": "Greek"
            },
            "anthropomorphic": {
                "definition": "Having human characteristics or form; attributing human traits to non-human entities.",
                "example_sentence": "The children's book featured _____ animals that walked and talked like people.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "an-thruh-puh-MOR-fik (emphasis on fourth syllable)",
                "etymology": "From Greek 'anthropos' (human) + 'morphe' (form)",
                "memory_tips": "Think 'anthropo-morphic' - having human (anthropo) form (morphic)",
                "language_origin": "Greek"
            },
            "anticipatory": {
                "definition": "Happening or performed in advance; showing expectation or preparation for future events.",
                "example_sentence": "The market showed _____ excitement before the product launch announcement.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "an-TIS-uh-puh-tor-ee (emphasis on second syllable)",
                "etymology": "From Latin 'anticipare' meaning 'to take beforehand'",
                "memory_tips": "Think 'anticip-atory' - showing anticipation or expectation",
                "language_origin": "Latin"
            },
            "anticoagulant": {
                "definition": "A medicine that prevents blood from clotting; a substance that inhibits coagulation.",
                "example_sentence": "The patient took daily _____ medication to prevent dangerous blood clots.",
                "part_of_speech": "noun/adjective",
                "pronunciation_guide": "an-tee-koh-AG-yuh-lunt (emphasis on fourth syllable)",
                "etymology": "From 'anti-' (against) + 'coagulant' (clotting agent)",
                "memory_tips": "Think 'anti-coagulant' - against blood coagulation/clotting",
                "language_origin": "Modern English"
            },
            "antidote": {
                "definition": "A medicine taken to counteract poison; something that counteracts harmful effects.",
                "example_sentence": "The doctor quickly administered the _____ to neutralize the snake's venom.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AN-tuh-doht (emphasis on first syllable)",
                "etymology": "From Greek 'antidoton' meaning 'given against'",
                "memory_tips": "Think 'anti-dote' - given against poison or harm",
                "language_origin": "Greek"
            },
            "antigua": {
                "definition": "An island nation in the Caribbean; also refers to the historic city in Guatemala.",
                "example_sentence": "The tourists enjoyed the beautiful beaches and warm climate of _____.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-TEE-guh (emphasis on second syllable)",
                "etymology": "From Spanish 'antigua' meaning 'ancient' or 'old'",
                "memory_tips": "Think 'Antigua' - the ancient or old island in the Caribbean",
                "language_origin": "Spanish"
            },
            "antimony": {
                "definition": "A brittle, silvery-white metallic chemical element used in alloys and flame retardants.",
                "example_sentence": "The chemist extracted _____ from the ore for use in the special alloy.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AN-tuh-moh-nee (emphasis on first syllable)",
                "etymology": "From Medieval Latin 'antimonium', possibly from Arabic 'al-ithmid'",
                "memory_tips": "Think 'antimony' - the metallic element with anti-bacterial properties",
                "language_origin": "Arabic"
            },
            "antipathy": {
                "definition": "A strong feeling of dislike or aversion; natural opposition or hostility.",
                "example_sentence": "There was mutual _____ between the two rival companies from the start.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-TIP-uh-thee (emphasis on second syllable)",
                "etymology": "From Greek 'antipatheia', from 'anti-' (against) + 'pathos' (feeling)",
                "memory_tips": "Think 'anti-pathy' - feeling against, opposite of sympathy",
                "language_origin": "Greek"
            },
            "antiquarian": {
                "definition": "A person who studies or collects old and rare books, artifacts, or antiques; relating to antiquities.",
                "example_sentence": "The _____ discovered a rare manuscript in the estate sale collection.",
                "part_of_speech": "noun/adjective",
                "pronunciation_guide": "an-tuh-KWAIR-ee-un (emphasis on third syllable)",
                "etymology": "From Latin 'antiquarius', from 'antiquus' (ancient)",
                "memory_tips": "Think 'antiqu-arian' - one who deals with antique or ancient items",
                "language_origin": "Latin"
            },
            "antiquity": {
                "definition": "The ancient past, especially the period before the Middle Ages; great age or oldness.",
                "example_sentence": "The museum's collection spanned from _____ to the modern era.",
                "part_of_speech": "noun",
                "pronunciation_guide": "an-TIK-wuh-tee (emphasis on second syllable)",
                "etymology": "From Latin 'antiquitas', from 'antiquus' (ancient)",
                "memory_tips": "Think 'antiqu-ity' - the quality of being ancient or very old",
                "language_origin": "Latin"
            }
        }
        
        # Combined word errors detected in this batch
        self.combined_word_errors = [
            "animustrillium",
            "annulmentorganized", 
            "antagonisticaffront"
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
    processor = Batch009Processor()
    input_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_009_words.csv"
    output_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_009_processed.csv"
    
    processor.process_batch(input_file, output_file)
    
    print(f"\nBatch 009 Processing Complete!")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Combined word errors flagged: {len(processor.combined_word_errors)}")

if __name__ == "__main__":
    main()