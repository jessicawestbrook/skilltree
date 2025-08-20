import pandas as pd
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import math

@dataclass
class WordData:
    word: str
    definition: str = ""
    part_of_speech: str = ""
    pronunciation_guide: str = ""
    etymology: str = ""
    language_origins: str = ""
    definition_source: str = "Claude"
    pronunciation_source: str = "Claude"
    etymology_source: str = "Claude"
    example_sentence: str = ""
    example_sentence_source: str = "Claude"
    memory_tip: str = ""
    memory_tip_source: str = "Claude"
    difficulty_phonetic: Optional[int] = None
    difficulty_semantic: Optional[int] = None
    difficulty_morphological: Optional[int] = None
    difficulty_etymological: Optional[int] = None
    combined_words_detected: bool = False
    incomplete_word_detected: bool = False
    parsing_errors: List[str] = field(default_factory=list)
    years: str = ""
    source_files: str = ""
    source_difficulties: str = ""

class DifficultyCalculator:
    def calculate_phonetic_score(self, word: str, pronunciation: str) -> int:
        irregular_patterns = ['ough', 'augh', 'eigh', 'ough', 'ph', 'gh', 'ch', 'sh', 'th']
        score = 1
        for pattern in irregular_patterns:
            if pattern in word.lower():
                score += 1
        return min(score, 5)
    
    def calculate_semantic_score(self, definition: str, word: str) -> int:
        if len(definition) > 300:
            return 4
        elif len(definition) > 200:
            return 3
        elif len(definition) > 100:
            return 2
        return 1
    
    def calculate_morphological_score(self, word: str) -> int:
        prefixes = ['un', 'pre', 'dis', 'in', 'im', 'ir', 'ex', 'sub', 'super', 'anti', 'auto']
        suffixes = ['tion', 'sion', 'ness', 'ment', 'able', 'ible', 'ous', 'eous', 'ious']
        score = 1
        for prefix in prefixes:
            if word.lower().startswith(prefix):
                score += 1
                break
        for suffix in suffixes:
            if word.lower().endswith(suffix):
                score += 1
                break
        if len(word) > 10:
            score += 1
        return min(score, 5)
    
    def calculate_etymological_score(self, etymology: str, language_origins: str) -> int:
        complex_origins = ['Greek', 'Latin', 'Sanskrit', 'Hebrew', 'Arabic']
        if any(origin in language_origins for origin in complex_origins):
            return 3
        elif 'French' in language_origins or 'German' in language_origins:
            return 2
        return 1

class Batch066Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def detect_parsing_errors(self, word: str) -> Tuple[bool, bool, List[str]]:
        errors = []
        combined_detected = False
        incomplete_detected = False
        
        # Check for combined words (specific to this batch)
        combined_word_patterns = {
            'feintedhumus': ['feinted', 'humus'],
            'feldenkraisbailiwick': ['feldenkrais', 'bailiwick']
        }
        
        if word.lower() in combined_word_patterns:
            combined_detected = True
            errors.append(f"Combined word error: \"{word}\" appears to be {' + '.join(combined_word_patterns[word.lower()])} merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.")
        
        return combined_detected, incomplete_detected, errors
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Generate comprehensive educational data for spelling bee words using Claude's knowledge."""
        
        batch_066_data = {
            'farouche': {
                'definition': 'Farouche describes someone who is shy, wild, or unsociable in a fierce or sullen way. The word suggests a person who is withdrawn from social contact not out of simple shyness, but with a kind of fierce independence or untamed quality. Someone who is farouche may appear unfriendly or hostile, but this behavior often stems from a deep-seated wariness or discomfort with social interaction rather than genuine malice. The term carries connotations of wildness and an uncivilized or primitive nature, as if the person has not been tamed by social conventions.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'fuh-ROOSH',
                'etymology': 'From French "farouche" meaning "wild" or "fierce," ultimately from Latin "forasticus" meaning "outside" or "foreign," related to "foris" meaning "out of doors."',
                'language_origins': 'French, Latin',
                'example_sentence': 'The _______ mountain dweller avoided visitors and rarely spoke to anyone who ventured near his remote cabin.',
                'memory_tip': 'Remember "fa-ROOSH" - someone so wild and fierce they make a RUSHING sound when they retreat from social contact.'
            },
            'farrago': {
                'definition': 'A farrago is a confused mixture or medley of things, typically a hodgepodge of different elements that creates a chaotic or disorganized whole. The word often describes a jumbled collection of ideas, styles, or objects that lack coherence or logical organization. Farrago can refer to literary works that mix various genres or themes inconsistently, or to any situation where multiple disparate elements are thrown together without careful consideration. The term emphasizes the confused and mixed-up nature of the collection rather than its diversity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fuh-RAH-goh',
                'etymology': 'From Latin "farrago" meaning "mixed fodder for cattle," derived from "far" meaning "grain." Originally referred to mixed animal feed.',
                'language_origins': 'Latin',
                'example_sentence': 'The student\'s essay was a _______ of unrelated ideas that jumped from topic to topic without any clear structure.',
                'memory_tip': 'Remember "far-RAGO" - a FAR-reaching mess of different things, like mixed animal feed that goes in all directions.'
            },
            'farsi': {
                'definition': 'Farsi is the Persian language, spoken primarily in Iran and parts of Afghanistan and Tajikistan. It is an Indo-European language that uses a modified Arabic script and has been the literary language of much of the Islamic world for centuries. Farsi has a rich literary tradition, with famous poets like Rumi, Hafez, and Omar Khayyam writing in this language. The language has influenced many other languages in the region and has contributed numerous words to English, particularly in areas of poetry, mathematics, and culture.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'FAR-see',
                'etymology': 'From Persian "fārsī," meaning "of Fars," referring to the Fars province in Iran where the language originated. Related to "Persian."',
                'language_origins': 'Persian',
                'example_sentence': 'She spent two years studying _______ to better understand the classical poetry of medieval Persia.',
                'memory_tip': 'Remember "FAR-si" - the language spoken FAR away in Persia, where you can SEE beautiful poetry and culture.'
            },
            'farthingale': {
                'definition': 'A farthingale is a hooped petticoat or framework worn under women\'s skirts in the 16th and 17th centuries to extend the skirt outward in a bell or drum shape. This undergarment was made of whalebone, wire, or wooden hoops that created the distinctive silhouette of Renaissance and Elizabethan fashion. Farthingales varied in style, with Spanish farthingales creating a cone shape and French farthingales producing a drum or wheel shape. The garment was both a fashion statement and a symbol of social status among the upper classes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAR-thing-gayl',
                'etymology': 'From Spanish "verdugado," meaning "rod-like," referring to the rods used in construction. The English term may be influenced by "farthing" (a small coin) and "gale."',
                'language_origins': 'Spanish, English',
                'example_sentence': 'The museum\'s costume exhibit featured an elaborate Renaissance dress supported by an authentic 16th-century _______.',
                'memory_tip': 'Remember "FARTHING-gale" - costs more than a FARTHING and creates a dress wide as a GALE wind, expanding the skirt.'
            },
            'fascinated': {
                'definition': 'Fascinated describes being intensely interested in or attracted to something, experiencing a powerful draw or captivation that holds one\'s attention completely. When someone is fascinated, they are so absorbed by something that they find it difficult to look away or think about anything else. This state involves both intellectual curiosity and emotional engagement, creating a sense of wonder or amazement. Fascination can be temporary or lasting, and it often leads to deeper exploration or study of the object of interest.',
                'part_of_speech': 'adjective (past participle)',
                'pronunciation_guide': 'FAS-uh-nay-tid',
                'etymology': 'From Latin "fascinatus," past participle of "fascinare" meaning "to bewitch" or "to cast a spell," related to "fascinum" meaning "spell" or "charm."',
                'language_origins': 'Latin',
                'example_sentence': 'The child remained _______ by the magician\'s performance, watching every movement with wide-eyed wonder.',
                'memory_tip': 'Remember "FASCIN-ated" - so captivated it\'s like being under a FASCIN-ating spell, unable to look away.'
            },
            'fascinating': {
                'definition': 'Fascinating describes something that is extremely interesting, captivating, or enchanting in a way that holds attention completely. When something is fascinating, it possesses qualities that draw people in and make them want to learn more or continue observing. The word suggests an almost magical ability to capture interest, often involving elements of mystery, beauty, complexity, or uniqueness. Fascinating subjects or experiences create a sense of wonder and curiosity that can be both intellectually stimulating and emotionally engaging.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FAS-uh-nay-ting',
                'etymology': 'Present participle of "fascinate," from Latin "fascinare" meaning "to bewitch," related to the idea of casting a spell that captures attention.',
                'language_origins': 'Latin',
                'example_sentence': 'The documentary about deep-sea creatures was _______, revealing species that seemed almost alien in their bizarre adaptations.',
                'memory_tip': 'Remember "FASCIN-ating" - so interesting it\'s like a FASCIN-ating spell that keeps you watching and wanting more.'
            },
            'fascinator': {
                'definition': 'A fascinator is a lightweight, decorative headpiece worn by women as an alternative to a hat, typically featuring feathers, beads, flowers, or other ornamental elements attached to a small base that sits on the head. Fascinators are commonly worn at formal events such as weddings, horse races, and garden parties, particularly in British fashion culture. The headpiece is usually secured with a headband, comb, or clip and is designed to be elegant and eye-catching without the full coverage of a traditional hat.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAS-uh-nay-ter',
                'etymology': 'From "fascinate" plus the suffix "-or," literally meaning "something that fascinates." The headpiece is designed to attract attention and fascinate onlookers.',
                'language_origins': 'Latin, English',
                'example_sentence': 'She chose an elegant _______ decorated with peacock feathers for her sister\'s wedding ceremony.',
                'memory_tip': 'Remember "FASCIN-ator" - a headpiece designed to FASCINATE others, like a decorative attractor for attention.'
            },
            'fashionista': {
                'definition': 'A fashionista is a person who is very interested in fashion and follows the latest trends closely, often someone who has an exceptional sense of style or works in the fashion industry. Fashionistas are typically early adopters of new styles and are often looked to by others for fashion advice and inspiration. The term can describe both professionals in fashion-related fields and enthusiastic consumers who make fashion a central part of their identity. Fashionistas often have extensive knowledge of designers, trends, and fashion history.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fash-uh-NEES-tah',
                'etymology': 'Blend of "fashion" and the Spanish suffix "-ista" (meaning "one who follows"), popularized in the late 20th century fashion industry.',
                'language_origins': 'English, Spanish',
                'example_sentence': 'As a dedicated _______, she spent hours each morning carefully selecting her outfit and accessories for the day.',
                'memory_tip': 'Remember "fashion-ISTA" - like a fashion artISTA (artist) who lives and breathes style trends.'
            },
            'fast': {
                'definition': 'Fast has multiple meanings depending on context. As an adjective, it means moving or happening quickly, or firmly fixed and secure. As an adverb, it describes rapid movement or action. As a verb, fast means to abstain from food, often for religious, health, or political reasons. The word can also describe something that is ahead of the correct time, as in a fast clock. In various contexts, fast emphasizes speed, security, or the deliberate avoidance of something.',
                'part_of_speech': 'adjective, adverb, verb, noun',
                'pronunciation_guide': 'FAST',
                'etymology': 'From Old English "fæst" meaning "firm" or "fixed." The "quick" meaning developed from the idea of moving firmly or steadily.',
                'language_origins': 'Old English',
                'example_sentence': 'The athlete ran _______ around the track, breaking the school record for the mile.',
                'memory_tip': 'Remember "FAST" - whether moving quickly or holding firmly, it\'s about intensity and strength in action or position.'
            },
            'fasting': {
                'definition': 'Fasting is the practice of abstaining from food, and sometimes drink, for a specified period of time. This practice can be undertaken for various reasons including religious observance, health benefits, protest, or spiritual purification. Religious fasting is common in many traditions, such as during Ramadan in Islam or Lent in Christianity. Medical fasting might be done before certain procedures or as part of dietary regimens. Fasting requires self-discipline and can have both physical and psychological effects on the person undertaking it.',
                'part_of_speech': 'noun, verb (present participle)',
                'pronunciation_guide': 'FAS-ting',
                'etymology': 'From "fast" (to abstain from food) plus the suffix "-ing." The practice has ancient roots in religious and cultural traditions.',
                'language_origins': 'Old English',
                'example_sentence': 'During the month of Ramadan, many Muslims observe _______ from sunrise to sunset as part of their religious practice.',
                'memory_tip': 'Remember "FAST-ing" - going without food FAST, abstaining quickly and completely from eating.'
            },
            'fastuous': {
                'definition': 'Fastuous describes someone who is arrogant, haughty, or disdainful, particularly someone who looks down on others with contempt or superiority. The word suggests an attitude of proud disdain combined with ostentation or showiness. A fastuous person not only feels superior to others but displays this superiority in an offensive, pompous manner. The term implies both internal arrogance and external display of that arrogance, making it particularly objectionable to those who encounter such behavior.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FAS-choo-us',
                'etymology': 'From Latin "fastuosus" meaning "haughty" or "proud," derived from "fastus" meaning "pride" or "disdain."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ nobleman treated the servants with such obvious contempt that even his peers found his behavior offensive.',
                'memory_tip': 'Remember "FAST-uous" - someone who thinks they\'re too FAST (superior) for others, acting haughty and pompous.'
            },
            'fata': {
                'definition': 'Fata is a Latin word meaning "fate" or "destiny," often used in legal and academic contexts in phrases like "fata morgana" (a type of mirage) or in discussions of classical literature and philosophy. In mythology and literature, fata can refer to the Fates, the three goddesses who controlled human destiny in Greek and Roman mythology. The word represents the concept of predetermined destiny or the inevitable course of events that cannot be changed by human action.',
                'part_of_speech': 'Latin noun used in English contexts',
                'pronunciation_guide': 'FAH-tah',
                'etymology': 'From Latin "fata," plural of "fatum" meaning "that which is spoken" or "fate," derived from "fari" meaning "to speak."',
                'language_origins': 'Latin',
                'example_sentence': 'The classical scholar discussed how ancient Romans believed in _______ as an unchangeable force governing human lives.',
                'memory_tip': 'Remember "FATA" - sounds like FATE-ah, representing the ancient concept of predetermined destiny.'
            },
            'father': {
                'definition': 'Father refers to a male parent, the man who has biological or adoptive responsibility for a child. In broader contexts, father can mean the founder or originator of something, such as "the father of modern science." The term also applies to priests in many Christian denominations, reflecting their spiritual parental role. Father represents concepts of protection, guidance, authority, and nurturing within family and social structures. The word carries deep emotional and social significance across cultures.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FAH-ther',
                'etymology': 'From Old English "fæder," related to Latin "pater" and Greek "pater," all from the Indo-European root meaning "father."',
                'language_origins': 'Old English, Indo-European',
                'example_sentence': 'The young _______ read bedtime stories to his daughter every night before she went to sleep.',
                'memory_tip': 'Remember "FATHER" - the male parent who helps you go FARther in life through guidance and support.'
            },
            'fatimid': {
                'definition': 'Fatimid refers to a medieval Islamic dynasty that ruled parts of North Africa and the Middle East from 909 to 1171 CE. The Fatimids claimed descent from Fatima, the daughter of the Prophet Muhammad, and established a caliphate that rivaled the Abbasid Caliphate in Baghdad. They founded the city of Cairo and built the famous Al-Azhar University. The Fatimid period was marked by significant cultural, architectural, and intellectual achievements, as well as religious tolerance and trade prosperity.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'FAT-uh-mid',
                'etymology': 'From Arabic "Fāṭimī," referring to Fatimah, daughter of Prophet Muhammad. The dynasty claimed descent from her lineage.',
                'language_origins': 'Arabic',
                'example_sentence': 'The museum\'s Islamic art collection includes beautiful ceramics and textiles from the _______ period.',
                'memory_tip': 'Remember "FATI-mid" - the dynasty in the MIDdle of Islamic history that claimed descent from FATIma.'
            },
            'fatshedera': {
                'definition': 'Fatshedera is a hybrid houseplant created by crossing Fatsia japonica and Hedera helix (English ivy). This evergreen plant combines characteristics of both parents, featuring large, glossy, palmate leaves similar to Fatsia but with some of the climbing tendencies of ivy. Fatshedera is popular as an indoor plant because it tolerates low light conditions and is relatively easy to care for. The plant can be grown as a bushy shrub or trained to climb, making it versatile for interior decoration.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fat-SHED-er-ah',
                'etymology': 'Botanical hybrid name combining "Fatsia" (the genus of one parent plant) and "Hedera" (the genus of the other parent plant).',
                'language_origins': 'Latin (botanical nomenclature)',
                'example_sentence': 'The office lobby featured several large _______ plants that thrived in the low-light environment.',
                'memory_tip': 'Remember "FATS-HED-era" - a plant that\'s FAT like Fatsia but climbs like ivy in the SHED, combining both traits.'
            },
            'fatuously': {
                'definition': 'Fatuously means in a foolish, silly, or pointlessly stupid manner, typically describing behavior or speech that lacks intelligence or common sense. When someone acts fatuously, they demonstrate a complacent kind of foolishness, often combined with an unawareness of their own stupidity. The word suggests not just simple ignorance but a kind of self-satisfied foolishness that prevents the person from recognizing their own lack of wisdom. Fatuous behavior often appears confident despite being fundamentally misguided.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'FACH-oo-us-lee',
                'etymology': 'From "fatuous" (from Latin "fatuus" meaning "foolish" or "silly") plus the adverb suffix "-ly."',
                'language_origins': 'Latin',
                'example_sentence': 'He smiled _______ while explaining his obviously flawed theory, completely unaware of how ridiculous he sounded.',
                'memory_tip': 'Remember "FATU-ously" - acting so foolishly that you\'re FAT with stupidity, bloated with silly confidence.'
            },
            'faucet': {
                'definition': 'A faucet is a device that controls the flow of liquid, typically water, from a pipe or container. Most commonly found in kitchens, bathrooms, and utility areas, faucets allow users to start, stop, and regulate the flow of water for various purposes such as washing, drinking, or cleaning. Modern faucets come in various styles and may include features like temperature control, spray settings, or motion sensors. The term is primarily used in American English, while "tap" is more common in British English.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FAW-sit',
                'etymology': 'From Old French "fausset" meaning "bung" (cork for a cask), derived from "faux" meaning "false," referring to the removable nature of the stopper.',
                'language_origins': 'Old French',
                'example_sentence': 'She turned the kitchen _______ handle clockwise to stop the dripping water that had been annoying her all morning.',
                'memory_tip': 'Remember "FAU-cet" - a device to PAUSE-it (stop) the flow of water when you turn the handle.'
            },
            'fauchard': {
                'definition': 'A fauchard is a type of medieval European polearm weapon, featuring a long wooden shaft topped with a curved, single-edged blade resembling a large sickle or billhook. This weapon was primarily used by infantry soldiers and was effective against cavalry and other foot soldiers. The curved blade could be used for slashing, hooking, or pulling opponents off balance. Fauchards were common from the 12th to 16th centuries and represent an important development in medieval weaponry, combining reach with cutting power.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'foh-SHAR',
                'etymology': 'From Old French "fauchard," related to "faux" meaning "scythe" or "sickle," referring to the curved blade shape.',
                'language_origins': 'Old French',
                'example_sentence': 'The museum\'s medieval weapons display included a well-preserved 14th-century _______ with intricate engravings on the blade.',
                'memory_tip': 'Remember "fau-CHARD" - a weapon that\'s HARD and looks like a FAUx (scythe), curved for slashing.'
            },
            'fault': {
                'definition': 'Fault has several meanings depending on context. As a noun, it can mean a defect, flaw, or imperfection in something, or responsibility for a mistake or problem. In geology, a fault is a fracture in rock where movement has occurred. In tennis and other sports, a fault is a rule violation. As a verb, fault means to criticize or find defects in something. The word generally relates to problems, defects, or the assignment of blame for difficulties or failures.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FAWLT',
                'etymology': 'From Old French "faute" meaning "defect" or "lacking," ultimately from Latin "fallere" meaning "to deceive" or "to fail."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The engineer couldn\'t find any _______ with the bridge\'s design after conducting a thorough safety inspection.',
                'memory_tip': 'Remember "FAULT" - when something FALLs short of perfection, there\'s a fault or flaw that needs attention.'
            },
            'faux': {
                'definition': 'Faux is a French word meaning "false" or "fake," commonly used in English to describe imitations or artificial versions of genuine materials or styles. When something is described as faux, it is designed to look like something else, typically something more expensive or luxurious. Common examples include faux leather, faux fur, or faux finishes in interior decoration. The term can also describe artificial behavior or emotions that are not genuine, such as faux sincerity or faux sophistication.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FOH',
                'etymology': 'From French "faux" meaning "false," ultimately from Latin "falsus," past participle of "fallere" meaning "to deceive."',
                'language_origins': 'French, Latin',
                'example_sentence': 'The designer chose _______ marble tiles for the bathroom because they provided the elegant look of real stone at a fraction of the cost.',
                'memory_tip': 'Remember "FAUX" - sounds like "foe," something that\'s an enemy of authenticity, pretending to be real but false.'
            },
            'favorite': {
                'definition': 'Favorite describes something or someone that is preferred above all others, regarded with special liking or affection. As a noun, favorite refers to the person or thing that is most preferred or likely to succeed. In competitions, the favorite is the competitor expected to win. The word indicates a choice based on personal preference, superior qualities, or past performance. Favorites often receive special attention, treatment, or consideration due to their preferred status.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'FAY-vur-it',
                'etymology': 'From French "favori," from Italian "favorito," past participle of "favorire" meaning "to favor," ultimately from Latin "favor."',
                'language_origins': 'Latin, Italian, French',
                'example_sentence': 'Chocolate ice cream has been her _______ dessert since childhood, and she always orders it when available.',
                'memory_tip': 'Remember "FAVOR-ite" - the thing you FAVOR most, the one you prefer above all others.'
            },
            'favourite': {
                'definition': 'Favourite is the British spelling of "favorite," describing something or someone that is preferred above all others or regarded with special liking. The word carries the same meanings as the American spelling, referring to preferred choices, expected winners in competitions, or items that receive special treatment due to their preferred status. The British spelling maintains the "u" that appears in many British English words derived from French or Latin sources.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'FAY-vur-it',
                'etymology': 'British spelling of "favorite," from French "favori," ultimately from Latin "favor" meaning "goodwill" or "support."',
                'language_origins': 'Latin, French',
                'example_sentence': 'The British author\'s _______ writing spot was a quiet corner of the local library overlooking the garden.',
                'memory_tip': 'Remember "FAVOUR-ite" - the British way to spell what you favor most, with the extra "u" for "United Kingdom."'
            },
            'fealty': {
                'definition': 'Fealty is a feudal tenant\'s or vassal\'s sworn loyalty to their lord, representing a formal allegiance that included obligations of service and support. In medieval society, fealty was a cornerstone of the feudal system, creating binding relationships between nobles and their subordinates. More broadly, fealty means faithfulness, loyalty, or allegiance to a person, cause, or principle. The concept involves both emotional commitment and formal obligation, creating bonds that were expected to endure through difficult circumstances.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FEE-ul-tee',
                'etymology': 'From Old French "feauté," from Latin "fidelitas" meaning "faithfulness," derived from "fidelis" meaning "faithful."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The knight swore _______ to his lord, promising to serve faithfully in both war and peace.',
                'memory_tip': 'Remember "FEALTY" - FEE-like loyalty, a formal commitment that\'s as valuable as paying a fee for protection.'
            },
            'fearsome': {
                'definition': 'Fearsome describes something that inspires fear or dread due to its frightening, formidable, or intimidating nature. When something is fearsome, it possesses qualities that make people afraid or apprehensive, such as size, power, appearance, or reputation. The word can apply to physical threats like fearsome predators, or to abstract concepts like fearsome responsibilities. Fearsome suggests an objective quality that naturally provokes fear rather than fear based on misunderstanding or irrationality.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FEER-sum',
                'etymology': 'From "fear" (from Old English "fǣr") plus the suffix "-some" meaning "characterized by" or "tending to cause."',
                'language_origins': 'Old English',
                'example_sentence': 'The _______ storm approached with dark clouds and lightning that made everyone seek shelter immediately.',
                'memory_tip': 'Remember "FEAR-some" - something that causes FEAR in SOME people, or makes everyone afraid.'
            },
            'feasibility': {
                'definition': 'Feasibility refers to the state or degree of being easily or conveniently done, achieved, or accomplished. When something has feasibility, it is practical and realistic to implement given available resources, time, and circumstances. Feasibility studies are common in business and project planning to determine whether proposed ventures are viable. The concept involves analyzing practical constraints, costs, benefits, and potential obstacles to determine whether a goal or project can be successfully completed.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fee-zuh-BIL-i-tee',
                'etymology': 'From "feasible" (from French "faisable" meaning "doable") plus the suffix "-ity" indicating a state or quality.',
                'language_origins': 'French, Latin',
                'example_sentence': 'The engineering team conducted a thorough _______ study before recommending the construction of the new bridge.',
                'memory_tip': 'Remember "FEASIBIL-ity" - the ability to make something feasible, the capacity to turn plans into reality.'
            },
            'feast': {
                'definition': 'A feast is a large, elaborate meal typically prepared for a special occasion or celebration, featuring an abundance of food and often multiple courses. Feasts are associated with holidays, religious observances, weddings, and other significant events where people gather to share food and companionship. As a verb, feast means to eat heartily or to enjoy something with great pleasure. The word emphasizes abundance, celebration, and communal enjoyment of food and fellowship.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FEEST',
                'etymology': 'From Old French "feste," from Latin "festa," plural of "festum" meaning "holiday" or "celebration."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The thanksgiving _______ included turkey, stuffing, cranberry sauce, and pumpkin pie, bringing the whole family together.',
                'memory_tip': 'Remember "FEAST" - a meal that\'s FIT for celebration, where everyone can eat with great pleasure and abundance.'
            },
            'featherbrained': {
                'definition': 'Featherbrained describes someone who is silly, scatterbrained, or lacking in intelligence or seriousness. The term suggests a person whose mind is as light and insubstantial as feathers, easily blown about by every passing thought or distraction. Someone who is featherbrained has difficulty focusing, makes poor decisions, or acts in foolish ways. While sometimes used affectionately, the term generally implies criticism of someone\'s mental capabilities or tendency toward frivolous behavior.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FETH-er-braynd',
                'etymology': 'Compound word combining "feather" (light, insubstantial) and "brained," suggesting a brain as light as feathers.',
                'language_origins': 'English',
                'example_sentence': 'Her _______ decision to buy a dozen pairs of shoes on sale left her unable to pay rent that month.',
                'memory_tip': 'Remember "FEATHER-brained" - a brain as light as FEATHERs, easily blown around by silly thoughts.'
            },
            'feats': {
                'definition': 'Feats are impressive or difficult achievements that require considerable skill, strength, or courage to accomplish. The word typically describes extraordinary accomplishments that stand out due to their difficulty, rarity, or the exceptional ability they demonstrate. Feats can be physical, such as athletic achievements, intellectual, such as solving complex problems, or creative, such as artistic masterpieces. The term emphasizes the remarkable nature of the accomplishment and the admiration it deserves.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FEETS',
                'etymology': 'From Old French "fait" meaning "deed" or "action," ultimately from Latin "factum" meaning "something done."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The gymnast\'s incredible _______ of strength and balance earned her a standing ovation from the amazed audience.',
                'memory_tip': 'Remember "FEATS" - impressive deeds that make people say "that\'s NEAT!" because they\'re so extraordinary.'
            },
            'featured': {
                'definition': 'Featured describes something that is prominently displayed, highlighted, or given special attention. When something is featured, it is presented as a main attraction, important element, or noteworthy component. The word can apply to products in advertisements, articles in publications, performances in shows, or any item that receives emphasis or special presentation. Featured items are typically selected for their quality, importance, or appeal to the intended audience.',
                'part_of_speech': 'adjective (past participle)',
                'pronunciation_guide': 'FEE-churd',
                'etymology': 'From "feature," ultimately from Old French "faiture" meaning "formation," from Latin "factura" meaning "making" or "formation."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The _______ artist at tonight\'s concert is known for her powerful vocals and emotional performances.',
                'memory_tip': 'Remember "FEATURED" - given special treatment like a FEATURE film, prominently displayed and highlighted.'
            },
            'features': {
                'definition': 'Features are distinctive characteristics, qualities, or parts that help define or identify something. The word can describe physical characteristics of a person\'s face, functional aspects of a product, natural formations of landscape, or special articles in publications. Features are the notable elements that make something recognizable or give it particular value. In various contexts, features represent the key attributes that distinguish one thing from another or make it useful and appealing.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'FEE-churz',
                'etymology': 'From "feature," from Old French "faiture" meaning "formation," ultimately from Latin "factura" meaning "act of making."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The new smartphone\'s best _______ include a high-resolution camera and extended battery life.',
                'memory_tip': 'Remember "FEATURES" - the special characteristics that make something stand out, like a creature\'s distinctive traits.'
            },
            'featuring': {
                'definition': 'Featuring means presenting or highlighting someone or something as a main attraction or important element. When something is featuring a particular person, product, or characteristic, it is giving that element prominence or special attention. The word is commonly used in entertainment, advertising, and media to indicate what or whom is being specially presented or emphasized. Featuring suggests intentional selection and prominent display of the highlighted element.',
                'part_of_speech': 'verb (present participle)',
                'pronunciation_guide': 'FEE-chur-ing',
                'etymology': 'Present participle of "feature," from Old French "faiture," ultimately from Latin "factura" meaning "making."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The magazine cover is _______ an interview with the famous director about her latest film project.',
                'memory_tip': 'Remember "FEATUR-ing" - actively putting something in the spotlight as a main FEATURE, showcasing it prominently.'
            },
            'feckless': {
                'definition': 'Feckless describes someone who is weak, ineffective, or irresponsible, lacking in initiative, competence, or strength of character. A feckless person typically fails to achieve goals due to poor planning, lack of determination, or inability to take effective action. The word suggests not just failure but a fundamental weakness in approach or character that prevents success. Feckless behavior often involves making poor decisions or failing to make decisions at all when action is needed.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FEK-lis',
                'etymology': 'From Scottish "feck" (effect, strength) plus "-less," literally meaning "without effect" or "without strength."',
                'language_origins': 'Scottish English',
                'example_sentence': 'His _______ approach to managing the project resulted in missed deadlines and frustrated team members.',
                'memory_tip': 'Remember "FECK-less" - without EFFECT or strength, lacking the power to accomplish anything meaningful.'
            },
            'fecund': {
                'definition': 'Fecund means fertile and capable of producing abundant growth, offspring, or results. The word can describe biological fertility, such as fecund soil that produces rich harvests or fecund animals that reproduce prolifically. Figuratively, fecund can describe minds, imaginations, or periods that generate many ideas, works of art, or innovations. The term emphasizes not just the ability to produce but the capacity for abundant, rich, and successful production.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FEE-kund',
                'etymology': 'From Latin "fecundus" meaning "fertile" or "fruitful," related to "fetus" and "feminine" concepts of productivity.',
                'language_origins': 'Latin',
                'example_sentence': 'The artist\'s _______ imagination produced dozens of paintings during her most creative period.',
                'memory_tip': 'Remember "FE-cund" - FErtile and productive, able to create or reproduce abundantly, like FEeding growth.'
            },
            'fedora': {
                'definition': 'A fedora is a soft felt hat with a creased crown and a medium-width brim, typically worn by men but also adopted by women in fashion. The hat became popular in the early 20th century and was a standard element of men\'s formal and business attire for decades. Fedoras are characterized by their distinctive shape, with a center crease running front to back and pinched sides. The hat has seen various periods of popularity and remains a classic style in fashion and popular culture.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fi-DOR-uh',
                'etymology': 'Named after the 1882 play "Fédora" by Victorien Sardou, in which the heroine wore this style of hat.',
                'language_origins': 'French (from proper name)',
                'example_sentence': 'The detective in the old movie wore a classic _______ pulled low over his eyes as he walked through the rainy streets.',
                'memory_tip': 'Remember "fe-DORA" - a hat worn by detectives and dapper gentlemen, like FEDORAS in FEDORA the play.'
            },
            'feeble': {
                'definition': 'Feeble describes something that is weak, lacking in physical strength, force, or effectiveness. When applied to people, feeble suggests physical frailty or weakness, often due to age, illness, or infirmity. The word can also describe weak attempts, arguments, or efforts that lack power or conviction. Feeble implies a significant lack of strength or capability that makes successful action difficult or impossible. The term often evokes sympathy for the weakness described.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FEE-bul',
                'etymology': 'From Old French "feble," from Latin "flebilis" meaning "lamentable" or "to be wept over," related to "flere" meaning "to weep."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The elderly man\'s _______ attempts to open the heavy door prompted a passerby to offer assistance.',
                'memory_tip': 'Remember "FEE-ble" - so weak that you FEEl BAD for them, lacking strength and needing help.'
            },
            'feedback': {
                'definition': 'Feedback is information about reactions to a product, performance, or process that is used as a basis for improvement. This information can be positive or negative and serves to help individuals or organizations understand how they are performing and what changes might be beneficial. In technical contexts, feedback refers to signals or data that are returned to the input of a system. Effective feedback is specific, timely, and actionable, providing clear guidance for improvement or adjustment.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FEED-bak',
                'etymology': 'Compound word combining "feed" and "back," originally from electronics and control systems, later adopted for general use.',
                'language_origins': 'English',
                'example_sentence': 'The teacher provided detailed _______ on each student\'s essay to help them improve their writing skills.',
                'memory_tip': 'Remember "FEED-back" - information that feeds back to you, helping you improve by showing results of your actions.'
            },
            'feeds': {
                'definition': 'Feeds can function as both a noun and a verb with different meanings. As a verb, feeds means to give food to someone or something, or to supply with necessary materials or information. As a noun, feeds can refer to animal food, particularly for livestock, or to data streams in digital contexts, such as news feeds or social media feeds. The word emphasizes the act of providing sustenance, information, or materials needed for growth, survival, or operation.',
                'part_of_speech': 'verb, noun (plural)',
                'pronunciation_guide': 'FEEDZ',
                'etymology': 'From "feed," from Old English "fēdan" meaning "to nourish" or "to supply with food."',
                'language_origins': 'Old English',
                'example_sentence': 'The farmer _______ the cattle every morning at sunrise, providing them with hay and grain.',
                'memory_tip': 'Remember "FEEDS" - provides food or information, like feeding animals or news feeds that feed your mind.'
            },
            'feel': {
                'definition': 'Feel has multiple meanings as both a verb and a noun. As a verb, it means to perceive through physical touch, to experience emotions, or to have opinions or beliefs. Feel can describe physical sensations, emotional states, or intuitive perceptions. As a noun, feel refers to the physical sensation of touching something or the general atmosphere or character of a situation. The word encompasses both tangible and intangible experiences that help us understand our environment and inner states.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'FEEL',
                'etymology': 'From Old English "fēlan" meaning "to touch" or "to perceive," related to the physical sense of touch.',
                'language_origins': 'Old English',
                'example_sentence': 'She could _______ the soft texture of the velvet fabric between her fingers.',
                'memory_tip': 'Remember "FEEL" - using your senses to understand texture, emotion, or atmosphere through direct experience.'
            },
            'feet': {
                'definition': 'Feet is the plural form of foot, referring to the terminal parts of the legs used for standing and walking. In measurement, feet refers to units of length equal to 12 inches each. Feet can also mean the bottom or base of something, such as the feet of a mountain or the feet of a page. The word encompasses both anatomical body parts essential for mobility and units of measurement commonly used in construction, real estate, and everyday measurements.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FEET',
                'etymology': 'Plural of "foot," from Old English "fōt," related to most Indo-European languages\' words for foot.',
                'language_origins': 'Old English, Indo-European',
                'example_sentence': 'After walking ten miles, her _______ were tired and sore from the long hiking trip.',
                'memory_tip': 'Remember "FEET" - the plural of foot, what you use to walk and also what you measure distance with.'
            },
            'feign': {
                'definition': 'Feign means to pretend to have or feel something, especially in order to deceive others or avoid unpleasant situations. When someone feigns an emotion, illness, or condition, they are deliberately acting as if it were real when it is not. The word implies intentional deception or simulation for personal advantage or to avoid consequences. Feigning often involves careful performance to make the pretense believable to others.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'FAYN',
                'etymology': 'From Old French "feindre" meaning "to pretend," ultimately from Latin "fingere" meaning "to shape" or "to form."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The child tried to _______ illness to avoid taking the difficult mathematics test at school.',
                'memory_tip': 'Remember "FEIGN" - to pretend, like FAINting when you\'re not really sick, putting on an act.'
            },
            'feisty': {
                'definition': 'Feisty describes someone who is lively, spirited, and showing courage or determination, especially when facing challenges or adversity. A feisty person has energy, spunk, and is willing to stand up for themselves despite being small or at a disadvantage. The word can also suggest someone who is somewhat aggressive or quarrelsome, though usually in an admirable way that shows strength of character. Feisty implies a combination of energy, courage, and spirited defiance.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FY-stee',
                'etymology': 'From "feist," a term for a small mongrel dog known for being aggressive, ultimately from Middle English "fist" meaning "to break wind."',
                'language_origins': 'Middle English',
                'example_sentence': 'Despite being the smallest player on the team, her _______ attitude and determination made her a formidable opponent.',
                'memory_tip': 'Remember "FEIST-y" - like a small dog with a big attitude, FISTy and ready to fight despite size.'
            },
            'feldenkrais': {
                'definition': 'Feldenkrais refers to a method of movement education developed by Moshe Feldenkrais that uses gentle movement and directed attention to improve movement and enhance human functioning. The Feldenkrais Method consists of two branches: Awareness Through Movement (group classes) and Functional Integration (individual sessions). This approach helps people develop greater awareness of their habitual movement patterns and discover new ways of moving that are more efficient and comfortable. The method is used for rehabilitation, performance enhancement, and general wellness.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FEL-den-krahs',
                'etymology': 'Named after Moshe Feldenkrais (1904-1984), the Israeli engineer and martial artist who developed this movement method.',
                'language_origins': 'Proper name (Hebrew origin)',
                'example_sentence': 'The physical therapist recommended _______ classes to help improve her posture and reduce chronic back pain.',
                'memory_tip': 'Remember "FELDEN-krais" - a method where you FEEL the DANCE of movement, learning to move with greater awareness.'
            },
            'feline': {
                'definition': 'Feline refers to anything relating to cats or members of the cat family, including domestic cats, lions, tigers, leopards, and other wild cats. As an adjective, feline describes characteristics typical of cats, such as grace, stealth, independence, or agility. As a noun, feline can refer to any member of the cat family. The word often evokes qualities associated with cats: elegance, mystery, independence, and predatory skill.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'FEE-lahyn',
                'etymology': 'From Latin "felinus," from "felis" meaning "cat." Related to the scientific classification of the cat family.',
                'language_origins': 'Latin',
                'example_sentence': 'With her _______ grace and silent movements, the dancer seemed to glide across the stage like a cat.',
                'memory_tip': 'Remember "FE-line" - relating to cats, like a LINE of FElines (cats) showing their graceful, cat-like qualities.'
            },
            'fellaheen': {
                'definition': 'Fellaheen is the plural form of "fellah," referring to peasants or agricultural laborers in Arab countries, particularly in Egypt and other parts of the Middle East and North Africa. Traditionally, fellaheen were farmers who worked the land, often as tenant farmers or sharecroppers. The term has historical and cultural significance in understanding rural life and agricultural systems in Arab societies. Fellaheen have played crucial roles in the agricultural economies of their regions throughout history.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'fel-uh-HEEN',
                'etymology': 'From Arabic "fallāḥīn," plural of "fallāḥ" meaning "plowman" or "tiller of the soil."',
                'language_origins': 'Arabic',
                'example_sentence': 'The documentary explored the lives of _______ in rural Egypt and their traditional farming methods.',
                'memory_tip': 'Remember "fellah-EEN" - the EEN (plural ending) of FELLAH, the farmers who FELL (work) the land in Arab countries.'
            },
            'fellahin': {
                'definition': 'Fellahin is an alternative plural form of "fellah," referring to peasant farmers or agricultural workers in Arab countries. Like fellaheen, this term describes rural agricultural laborers who traditionally worked the land in countries such as Egypt, Syria, and Palestine. The fellahin have been the backbone of agricultural production in these regions, maintaining farming traditions and techniques passed down through generations. Their role in society and economy has been central to understanding rural Arab culture.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'fel-uh-HEEN',
                'etymology': 'Alternative plural form from Arabic "fallāḥīn," referring to agricultural workers or peasants.',
                'language_origins': 'Arabic',
                'example_sentence': 'The historical study examined how the _______ adapted their farming practices during periods of social and political change.',
                'memory_tip': 'Remember "fellah-IN" - farmers who are IN the fields, working IN the agricultural tradition of Arab lands.'
            },
            'fellowship': {
                'definition': 'Fellowship refers to friendly association, companionship, or community among people who share common interests, experiences, or beliefs. The word can describe the relationship between members of a group, the spirit of friendship and mutual support within an organization, or formal associations of people with shared purposes. In academic contexts, fellowship refers to a position or grant that provides financial support for research or study. Fellowship emphasizes connection, belonging, and mutual support among individuals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FEL-oh-ship',
                'etymology': 'From "fellow" (from Old English "feolaga" meaning "partner") plus "-ship" indicating a state or condition.',
                'language_origins': 'Old English',
                'example_sentence': 'The graduate student received a prestigious _______ that would fund her research for the next two years.',
                'memory_tip': 'Remember "FELLOW-ship" - a relationship where you\'re fellows together, sharing companionship and support like passengers on a ship.'
            },
            'felonious': {
                'definition': 'Felonious describes actions, behavior, or intent that relates to or constitutes a felony, which is a serious crime typically punishable by imprisonment. When something is felonious, it involves criminal behavior of a severe nature, such as robbery, murder, or fraud. The word carries legal weight and implies serious wrongdoing that goes beyond minor infractions or misdemeanors. Felonious acts are those that violate major laws and pose significant threats to society or individuals.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'fuh-LOH-nee-us',
                'etymology': 'From "felony" (from Old French "felonie" meaning "wickedness") plus the suffix "-ous" meaning "characterized by."',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The prosecutor argued that the defendant\'s _______ assault deserved the maximum penalty under state law.',
                'memory_tip': 'Remember "FELON-ious" - behavior typical of a FELON, involving serious criminal activity that\'s FELt to be ONerous (burdensome) to society.'
            },
            'felt': {
                'definition': 'Felt has multiple meanings depending on context. As a noun, felt is a textile material made from compressed fibers, typically wool, that creates a dense, smooth fabric used for hats, crafts, and industrial applications. As the past tense of "feel," felt describes having experienced physical sensations, emotions, or perceptions in the past. The word encompasses both a specific material known for its durability and versatility, and the past experience of sensing or perceiving something.',
                'part_of_speech': 'noun, verb (past tense of feel)',
                'pronunciation_guide': 'FELT',
                'etymology': 'As a noun: from Old English "felt." As a verb: past tense of "feel" from Old English "fēlan."',
                'language_origins': 'Old English',
                'example_sentence': 'She _______ the soft texture of the wool _______ as she considered it for her craft project.',
                'memory_tip': 'Remember "FELT" - both a fabric you can feel and the past tense of feeling something with your senses.'
            }
        }
        
        if word.lower() in batch_066_data:
            return batch_066_data[word.lower()]
        else:
            # For any words not in our comprehensive data, return basic structure
            return {
                'definition': f'[Definition for {word} not available in batch data]',
                'part_of_speech': 'unknown',
                'pronunciation_guide': f'[Pronunciation for {word} not available]',
                'etymology': f'[Etymology for {word} not available]',
                'language_origins': 'unknown',
                'example_sentence': f'[Example sentence for {word} not available]',
                'memory_tip': f'[Memory tip for {word} not available]'
            }
    
    def process_batch(self, input_file: str, output_file: str):
        """Process a batch of spelling bee words with comprehensive Claude data."""
        print(f"Processing {input_file}...")
        
        # Read the input CSV
        df = pd.read_csv(input_file)
        
        processed_words = []
        error_count = 0
        
        for _, row in df.iterrows():
            word = str(row['word']).strip()
            
            # Skip empty rows
            if not word or word.lower() == 'nan':
                continue
            
            # Detect parsing errors
            combined_detected, incomplete_detected, errors = self.detect_parsing_errors(word)
            if errors:
                error_count += len(errors)
            
            # Get comprehensive data for this word
            word_data = self.get_comprehensive_claude_data(word)
            
            # Calculate difficulty scores (leaving final difficulty as null for now)
            phonetic_score = self.difficulty_calculator.calculate_phonetic_score(word, word_data['pronunciation_guide'])
            semantic_score = self.difficulty_calculator.calculate_semantic_score(word_data['definition'], word)
            morphological_score = self.difficulty_calculator.calculate_morphological_score(word)
            etymological_score = self.difficulty_calculator.calculate_etymological_score(word_data['etymology'], word_data['language_origins'])
            
            # Create WordData object
            processed_word = WordData(
                word=word,
                definition=word_data['definition'],
                part_of_speech=word_data['part_of_speech'],
                pronunciation_guide=word_data['pronunciation_guide'],
                etymology=word_data['etymology'],
                language_origins=word_data['language_origins'],
                example_sentence=word_data['example_sentence'],
                memory_tip=word_data['memory_tip'],
                difficulty_phonetic=phonetic_score,
                difficulty_semantic=semantic_score,
                difficulty_morphological=morphological_score,
                difficulty_etymological=etymological_score,
                combined_words_detected=combined_detected,
                incomplete_word_detected=incomplete_detected,
                parsing_errors=errors,
                years=str(row['years']) if 'years' in row else '',
                source_files=str(row['source_files']) if 'source_files' in row else '',
                source_difficulties=str(row['source_difficulties']) if 'source_difficulties' in row else ''
            )
            
            processed_words.append(processed_word)
        
        # Convert to DataFrame
        output_data = []
        for word_obj in processed_words:
            output_data.append({
                'word': word_obj.word,
                'definition': word_obj.definition,
                'part_of_speech': word_obj.part_of_speech,
                'pronunciation_guide': word_obj.pronunciation_guide,
                'etymology': word_obj.etymology,
                'language_origins': word_obj.language_origins,
                'definition_source': word_obj.definition_source,
                'pronunciation_source': word_obj.pronunciation_source,
                'etymology_source': word_obj.etymology_source,
                'example_sentence': word_obj.example_sentence,
                'example_sentence_source': word_obj.example_sentence_source,
                'memory_tip': word_obj.memory_tip,
                'memory_tip_source': word_obj.memory_tip_source,
                'difficulty_phonetic': word_obj.difficulty_phonetic,
                'difficulty_semantic': word_obj.difficulty_semantic,
                'difficulty_morphological': word_obj.difficulty_morphological,
                'difficulty_etymological': word_obj.difficulty_etymological,
                'difficulty': None,  # Leave null for now
                'years': word_obj.years,
                'source_files': word_obj.source_files,
                'source_difficulties': word_obj.source_difficulties,
                'combined_words_detected': word_obj.combined_words_detected,
                'incomplete_word_detected': word_obj.incomplete_word_detected,
                'parsing_errors': '; '.join(word_obj.parsing_errors) if word_obj.parsing_errors else ''
            })
        
        # Save to CSV
        output_df = pd.DataFrame(output_data)
        output_df.to_csv(output_file, index=False, quoting=1)  # quoting=1 ensures text fields are quoted
        
        # Print results
        print(f"Successfully processed {len(processed_words)}/50 words to {output_file}")
        if error_count > 0:
            print(f"Found {error_count} error(s):")
            for word_obj in processed_words:
                if word_obj.parsing_errors:
                    for error in word_obj.parsing_errors:
                        print(f"  - {word_obj.word}: {error}")
        
        print("Batch 066 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch066Processor()
    
    input_file = "output/batch_066_words.csv"
    output_file = "output/batch_066_processed.csv"
    
    processor.process_batch(input_file, output_file)