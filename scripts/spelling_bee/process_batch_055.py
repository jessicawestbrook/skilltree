import csv
import pandas as pd
from dataclasses import dataclass
from typing import Dict, Any, Optional
import os

@dataclass
class WordData:
    word: str
    definition: str
    part_of_speech: str
    pronunciation_guide: str
    etymology: str
    language_origins: str
    example_sentence: str
    memory_tip: str
    phonetic_transparency_score: int
    word_frequency_score: int
    morphological_complexity_score: int
    etymology_complexity_score: int
    source_difficulty: str
    years: str
    source_files: str
    definition_source: str = "Claude"
    pronunciation_source: str = "Claude"
    etymology_source: str = "Claude"
    memory_tip_source: str = "Claude"
    example_sentence_source: str = "Claude"
    difficulty: Optional[str] = None
    is_error: bool = False
    error_message: str = ""

class DifficultyCalculator:
    @staticmethod
    def calculate_phonetic_transparency(word: str) -> int:
        """Calculate phonetic transparency score (1-10, higher = more transparent)"""
        irregular_patterns = ['ough', 'augh', 'eigh', 'ph', 'gh', 'ch', 'qu', 'x']
        silent_letters = 0
        irregular_count = 0
        
        for pattern in irregular_patterns:
            if pattern in word.lower():
                irregular_count += 1
        
        common_silent = ['b', 'l', 'n', 'h', 'k', 'w']
        word_lower = word.lower()
        for i, char in enumerate(word_lower):
            if char in common_silent:
                if (char == 'b' and i > 0 and word_lower[i-1] == 'm') or \
                   (char == 'l' and i > 0 and word_lower[i-1] in 'af') or \
                   (char == 'n' and i == len(word_lower)-1 and word_lower[i-1] == 'm') or \
                   (char == 'h' and i > 0 and word_lower[i-1] in 'gkr') or \
                   (char == 'k' and i > 0 and word_lower[i-1] == 'n') or \
                   (char == 'w' and i > 0 and word_lower[i-1] in 'rs'):
                    silent_letters += 1
        
        base_score = 10 - min(irregular_count * 2 + silent_letters, 9)
        return max(1, base_score)
    
    @staticmethod
    def calculate_word_frequency(word: str) -> int:
        """Calculate word frequency score (1-10, higher = more frequent)"""
        word_lower = word.lower()
        
        high_freq = ['during', 'dropped', 'drill', 'drum', 'drift', 'dusk', 'duties', 'dunk']
        medium_freq = ['drizzle', 'drone', 'drool', 'drooped', 'drowsy', 'duckling', 'dutifully']
        
        if word_lower in high_freq:
            return 9
        elif word_lower in medium_freq:
            return 6
        elif len(word) <= 6:
            return 7
        elif len(word) <= 10:
            return 4
        else:
            return 2
    
    @staticmethod
    def calculate_morphological_complexity(word: str) -> int:
        """Calculate morphological complexity score (1-10, higher = more complex)"""
        prefixes = ['dr-', 'du-']
        suffixes = ['-ing', '-ed', '-ly', '-ous', '-ery', '-ine']
        
        prefix_count = sum(1 for prefix in prefixes if word.lower().startswith(prefix[:-1]))
        suffix_count = sum(1 for suffix in suffixes if word.lower().endswith(suffix[1:]))
        
        complexity = len(word) / 4 + prefix_count + suffix_count
        return min(10, max(1, int(complexity)))
    
    @staticmethod
    def calculate_etymology_complexity(word: str) -> int:
        """Calculate etymology complexity score (1-10, higher = more complex)"""
        word_lower = word.lower()
        
        if any(char in word_lower for char in 'θφχψω'):
            return 9
        
        greek_latin_indicators = ['ph', 'ch', 'th', 'rh', 'ps', 'pt', 'ct', 'gn']
        complex_origins = sum(1 for pattern in greek_latin_indicators if pattern in word_lower)
        
        if complex_origins >= 2:
            return 8
        elif complex_origins == 1:
            return 6
        elif any(word_lower.startswith(prefix) for prefix in ['dr', 'du']):
            return 4
        else:
            return 3

class Batch055Processor:
    def __init__(self):
        self.base_path = "/c/Users/jessi/Projects/skilltree2/scripts/spelling_bee"
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive data using Claude's knowledge"""
        
        batch_055_data = {
            'drift': {
                'definition': 'To be carried slowly by a current of air or water; to move aimlessly or gradually away from an intended position or course. Can refer to physical movement or gradual change.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'DRIFT (rhymes with "lift")',
                'etymology': 'From Middle English "drift" from Old Norse "drifa" meaning "to drive." Related to driving or pushing motion.',
                'language_origins': 'Old Norse',
                'example_sentence': 'The boat began to _____ downstream when the anchor came loose.',
                'memory_tip': 'Remember "DRIFT" rhymes with "lift" - but instead of lifting up, you drift along without control.'
            },
            'drill': {
                'definition': 'A tool for making holes; repeated practice or training; to make holes or practice repeatedly. Can refer to equipment, exercise, or action.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DRIL (rhymes with "will")',
                'etymology': 'From Middle Dutch "drillen" meaning "to bore, pierce." Related to turning and piercing tools.',
                'language_origins': 'Middle Dutch',
                'example_sentence': 'The construction worker used a power _____ to make holes in the concrete wall.',
                'memory_tip': 'Simple "DRILL" rhymes with "will" - when you have the will to practice, you drill the skill.'
            },
            'drivel': {
                'definition': 'Nonsense or silly talk; to talk in a childish or foolish way. Can also mean saliva flowing from the mouth.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DRIV-ul (emphasis on first syllable)',
                'etymology': 'From Old English "dreflian" meaning "to dribble, slaver." Related to flowing saliva or meaningless speech.',
                'language_origins': 'Old English',
                'example_sentence': 'The critic dismissed the speech as meaningless _____ that said nothing important.',
                'memory_tip': 'Think "DRIVel" - nonsense talk that "drives" you crazy because it\'s so silly and meaningless.'
            },
            'driveljettison': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "driveljettison" appears to be "drivel" + "jettison" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'drizzle': {
                'definition': 'Light rain falling in very fine drops; to rain lightly; to pour liquid in a thin stream. Weather or cooking terminology.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DRIZ-ul (emphasis on first syllable)',
                'etymology': 'From Middle English "drisnen" meaning "to fall." Related to gentle falling motion.',
                'language_origins': 'Middle English',
                'example_sentence': 'The chef decided to _____ olive oil over the salad just before serving.',
                'memory_tip': 'Remember "DRIZzle" - light rain that "drips" and "sizzles" gently, barely noticeable drops.'
            },
            'droll': {
                'definition': 'Curious or unusual in a way that provokes dry amusement; having a humorous, whimsical, or odd quality.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DROHL (rhymes with "roll")',
                'etymology': 'From French "drôle" meaning "funny, amusing." Originally from Middle French meaning "buffoon."',
                'language_origins': 'French',
                'example_sentence': 'His _____ sense of humor made even serious meetings more enjoyable.',
                'memory_tip': 'Remember "DROLL" rhymes with "roll" - droll humor makes you roll with laughter in a dry, witty way.'
            },
            'dromedary': {
                'definition': 'A one-humped camel, especially the Arabian camel used for riding and as a pack animal in desert regions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DROM-uh-dair-ee (emphasis on first syllable)',
                'etymology': 'From Greek "dromas" meaning "running" + Latin "dromedarius." Named for its running ability.',
                'language_origins': 'Greek via Latin',
                'example_sentence': 'The _____ can travel long distances across the desert without water.',
                'memory_tip': 'Think "DROM-edary" - a camel that can "roam" the "arid" desert with just one hump.'
            },
            'dromic': {
                'definition': 'Relating to running or racing; pertaining to courses or tracks. From Greek terminology about running.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DROH-mik (emphasis on first syllable)',
                'etymology': 'From Greek "dromos" meaning "running, course." Related to athletic and racing terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'The ancient Greek _____ events included various types of running competitions.',
                'memory_tip': 'Remember "DROM-ic" - relating to the "drome" (course) where people run, like a hippodrome.'
            },
            'drone': {
                'definition': 'A continuous low humming sound; a male bee; an unmanned aircraft; to make a continuous low sound.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DROHN (rhymes with "stone")',
                'etymology': 'From Old English "drān" meaning "male bee." Extended to mean continuous sound and aircraft.',
                'language_origins': 'Old English',
                'example_sentence': 'The _____ of the air conditioner made it difficult to concentrate on work.',
                'memory_tip': 'Remember "DRONE" rhymes with "tone" - a continuous, monotonous tone or sound.'
            },
            'drool': {
                'definition': 'To let saliva flow from the mouth; to show excessive desire or pleasure; saliva that flows from the mouth.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'DROOL (rhymes with "pool")',
                'etymology': 'Variant of "drivel," from Old English "dreflian." About flowing saliva.',
                'language_origins': 'Old English',
                'example_sentence': 'The baby began to _____ when she saw the delicious birthday cake.',
                'memory_tip': 'Remember "DROOL" rhymes with "pool" - saliva forms a little pool when you drool.'
            },
            'drooped': {
                'definition': 'Past tense of droop; bent or hung downward; sagged from weakness, fatigue, or lack of support.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'DROOPT (rhymes with "looped")',
                'etymology': 'From "droop" (from Old Norse "drúpa" meaning "to hang the head") + "-ed" suffix.',
                'language_origins': 'Old Norse',
                'example_sentence': 'The flowers _____ in the heat because they hadn\'t been watered.',
                'memory_tip': 'Think "DROOPED" - things that drop down and loop downward from tiredness or heat.'
            },
            'dropped': {
                'definition': 'Past tense of drop; let fall; stopped or discontinued; delivered or left at a place.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'DROPT (rhymes with "stopped")',
                'etymology': 'From "drop" (from Old English "droppian") + "-ed" suffix. About falling or letting fall.',
                'language_origins': 'Old English',
                'example_sentence': 'She accidentally _____ her keys while rushing to catch the bus.',
                'memory_tip': 'Simple "DROPPED" - things that fell down because they were dropped, no longer held up.'
            },
            'dropsonde': {
                'definition': 'A weather measurement device dropped from an aircraft to collect atmospheric data as it falls through the air.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DROP-sond (emphasis on first syllable)',
                'etymology': 'From "drop" + "sonde" (French for "probe"). Meteorological instrument terminology.',
                'language_origins': 'English + French',
                'example_sentence': 'The hurricane hunters released a _____ to measure wind speed and pressure inside the storm.',
                'memory_tip': 'Remember "DROP-sonde" - a weather "sonde" (probe) that you "drop" from planes to measure storms.'
            },
            'drowsy': {
                'definition': 'Sleepy and lethargic; half asleep; causing sleepiness or inactivity.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DROW-zee (emphasis on first syllable)',
                'etymology': 'From "drowse" (related to Old English "drūsian" meaning "to be sluggish") + "-y" suffix.',
                'language_origins': 'Old English',
                'example_sentence': 'The warm afternoon sun made him feel _____ during the long lecture.',
                'memory_tip': 'Think "DROWsy" - you "drow" (almost drown) in sleepiness, feeling tired and sluggish.'
            },
            'drudgery': {
                'definition': 'Hard, menial, or dull work; tedious and monotonous labor that lacks interest or excitement.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DRUJ-er-ee (emphasis on first syllable)',
                'etymology': 'From "drudge" (from Middle English "druggen" meaning "to work hard") + "-ery" suffix.',
                'language_origins': 'Middle English',
                'example_sentence': 'Washing dishes every night felt like pure _____ to the restaurant worker.',
                'memory_tip': 'Remember "DRUDGery" - "drudge" work that\'s a drag, tedious labor that feels like drudgery.'
            },
            'druid': {
                'definition': 'A member of the ancient Celtic priesthood; a practitioner of nature-based spirituality. Historical and mythological figure.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DROO-id (emphasis on first syllable)',
                'etymology': 'From Latin "druides" from Gaulish. Celtic religious terminology.',
                'language_origins': 'Celtic via Latin',
                'example_sentence': 'The ancient _____ conducted ceremonies in sacred groves of oak trees.',
                'memory_tip': 'Think "DROO-id" - Celtic priests who "drew" power from nature and trees.'
            },
            'drum': {
                'definition': 'A percussion instrument with a stretched membrane; a cylindrical container; to play drums or make drumming sounds.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DRUM (rhymes with "come")',
                'etymology': 'From Middle Dutch "tromme" or Middle Low German "trumme." Musical terminology.',
                'language_origins': 'Germanic',
                'example_sentence': 'The marching band\'s bass _____ kept everyone in perfect rhythm.',
                'memory_tip': 'Simple "DRUM" - an instrument that makes "thrum" sounds when you beat it rhythmically.'
            },
            'drumlin': {
                'definition': 'An elongated hill formed by glacial action, typically composed of glacial sediment. Geological landform terminology.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DRUM-lin (emphasis on first syllable)',
                'etymology': 'From Irish "droim" meaning "ridge" + diminutive "-lin." Geological terminology.',
                'language_origins': 'Irish',
                'example_sentence': 'The landscape featured several _____ formations left behind by ancient glaciers.',
                'memory_tip': 'Remember "DRUM-lin" - small hills that look like little "drums" scattered across the landscape.'
            },
            'drupiferous': {
                'definition': 'Bearing stone fruits; producing drupes (fruits with a hard stone containing the seed, like cherries or peaches).',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'droo-PIF-er-us (emphasis on second syllable)',
                'etymology': 'From Latin "drupa" (overripe olive) + "ferous" (bearing). Botanical terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The orchard contained many _____ trees, including cherries, plums, and peaches.',
                'memory_tip': 'Think "drupe-IFER-ous" - trees that "bear" (ferous) "drupes" (stone fruits) like cherries.'
            },
            'dubhe': {
                'definition': 'The brightest star in the constellation Ursa Major (the Great Bear), also known as Alpha Ursae Majoris.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DUB-hee (emphasis on first syllable)',
                'etymology': 'From Arabic "dubb" meaning "bear." Astronomical terminology.',
                'language_origins': 'Arabic',
                'example_sentence': 'Astronomers use _____ as a reference point for locating other stars in the Big Dipper.',
                'memory_tip': 'Remember "DUB-he" - you can "dub" this star the brightest in the Great Bear constellation.'
            },
            'dubiously': {
                'definition': 'In a doubtful or uncertain manner; with skepticism or suspicion; questionably or unreliably.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'DOO-bee-us-lee (emphasis on first syllable)',
                'etymology': 'From Latin "dubiosus" meaning "doubtful" + "-ly" suffix. About uncertainty and doubt.',
                'language_origins': 'Latin',
                'example_sentence': 'She looked at him _____ when he claimed to have finished all his homework.',
                'memory_tip': 'Remember "DOO-biously" - when you "doubt" something, you look at it dubiously with suspicion.'
            },
            'dubitante': {
                'definition': 'A legal term meaning "doubting" or "with doubt"; used in judicial opinions to indicate uncertainty about a decision.',
                'part_of_speech': 'adjective, adverb',
                'pronunciation_guide': 'doo-bi-TAN-tay (emphasis on third syllable)',
                'etymology': 'From Latin "dubitans" meaning "doubting" (from dubitare "to doubt"). Legal terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The judge wrote a _____ opinion, expressing some uncertainty about the precedent.',
                'memory_tip': 'Think "doo-bi-TANTE" - a legal "aunt" who always doubts and questions legal decisions.'
            },
            'dubuque': {
                'definition': 'A city in Iowa, United States, located on the Mississippi River. Named after Julien Dubuque, a French-Canadian explorer.',
                'part_of_speech': 'noun (proper)',
                'pronunciation_guide': 'duh-BYOOK (emphasis on second syllable)',
                'etymology': 'Named after Julien Dubuque, French-Canadian fur trader. Geographic proper noun.',
                'language_origins': 'French (surname)',
                'example_sentence': 'The riverboat stopped at _____ during its journey down the Mississippi River.',
                'memory_tip': 'Remember "duh-BYOOK" - sounds like "the book," a city you might read about in a geography book.'
            },
            'ducats': {
                'definition': 'Historical gold or silver coins used in various European countries; valuable coins associated with trade and wealth.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DUK-ats (emphasis on first syllable)',
                'etymology': 'From Italian "ducato" from Medieval Latin "ducatus" (duchy). Historical monetary terminology.',
                'language_origins': 'Italian from Latin',
                'example_sentence': 'The merchant\'s pouch was heavy with gold _____ from his successful trading ventures.',
                'memory_tip': 'Think "DUC-ats" - "duke" coins, valuable money used by dukes and wealthy European rulers.'
            },
            'duchy': {
                'definition': 'The territory ruled by a duke or duchess; a dukedom or the rank and jurisdiction of a duke.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DUCH-ee (emphasis on first syllable)',
                'etymology': 'From Old French "duchié" from "duc" meaning "duke." Political and territorial terminology.',
                'language_origins': 'Old French',
                'example_sentence': 'The _____ of Cornwall has been held by the heir to the British throne for centuries.',
                'memory_tip': 'Remember "DUCH-y" - the land ruled by a "duchess" or duke, their royal territory.'
            },
            'duchypagoda': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "duchypagoda" appears to be "duchy" + "pagoda" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'duckling': {
                'definition': 'A young duck; a small or baby duck that has not yet reached maturity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DUK-ling (emphasis on first syllable)',
                'etymology': 'From "duck" + "-ling" (diminutive suffix). About young or small animals.',
                'language_origins': 'English',
                'example_sentence': 'The yellow _____ followed its mother closely as they swam across the pond.',
                'memory_tip': 'Simple "DUCK-ling" - a little "duck" that\'s still small and young, just learning to swim.'
            },
            'duddy': {
                'definition': 'Ragged or tattered clothing; old, worn-out garments. Archaic term for shabby clothes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DUD-ee (emphasis on first syllable)',
                'etymology': 'Origin uncertain, possibly from "dud" meaning something that fails. About worn clothing.',
                'language_origins': 'English (uncertain origin)',
                'example_sentence': 'The beggar wore only _____ and had no proper shoes on his feet.',
                'memory_tip': 'Think "DUD-dy" - clothes that are "duds," so worn out they\'re hardly clothing anymore.'
            },
            'dudgeon': {
                'definition': 'A feeling of offense or resentment; indignation or anger, especially when feeling slighted or insulted.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DUJ-un (emphasis on first syllable)',
                'etymology': 'Origin uncertain, possibly from Anglo-French. About feelings of offense and resentment.',
                'language_origins': 'English (uncertain origin)',
                'example_sentence': 'He left the meeting in high _____ after being publicly criticized.',
                'memory_tip': 'Remember "DUD-geon" - when someone treats you like a "dud," you feel dudgeon (resentment).'
            },
            'dudley': {
                'definition': 'A place name; various towns and locations, most notably Dudley in England. Also used as a given name.',
                'part_of_speech': 'noun (proper)',
                'pronunciation_guide': 'DUD-lee (emphasis on first syllable)',
                'etymology': 'From Old English "Dodda\'s leah" meaning "Dodda\'s meadow." Geographic and personal name.',
                'language_origins': 'Old English',
                'example_sentence': 'The family traced their ancestry back to _____ in the West Midlands of England.',
                'memory_tip': 'Remember "DUD-ley" - a place name that sounds like "dud" + "lee" (meadow).'
            },
            'duello': {
                'definition': 'The practice or art of dueling; the code of honor governing formal combat between two people.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'doo-EL-oh (emphasis on second syllable)',
                'etymology': 'From Italian "duello" from Latin "duellum" (combat between two). About formal fighting.',
                'language_origins': 'Italian from Latin',
                'example_sentence': 'The nobleman challenged his rival according to the strict rules of _____.',
                'memory_tip': 'Think "doo-ELLO" - a formal "duel" between two people, following the code of duello.'
            },
            'dulcet': {
                'definition': 'Sweet and soothing, especially referring to sounds; melodious and pleasant to hear.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DUL-sit (emphasis on first syllable)',
                'etymology': 'From Latin "dulcis" meaning "sweet." About pleasant, sweet sounds.',
                'language_origins': 'Latin',
                'example_sentence': 'Her _____ voice made even the most boring lecture sound interesting.',
                'memory_tip': 'Remember "DUL-cet" - sounds so sweet they\'re "dull" (calming) and "set" your mind at ease.'
            },
            'dulcinea': {
                'definition': 'An idealized beloved woman; a sweetheart or lady love, especially one who is idolized from afar.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dul-si-NEE-ah (emphasis on third syllable)',
                'etymology': 'From "Dulcinea del Toboso," Don Quixote\'s idealized beloved in Cervantes\' novel. Literary terminology.',
                'language_origins': 'Spanish (literary)',
                'example_sentence': 'He wrote poetry to his _____, though she barely knew he existed.',
                'memory_tip': 'Think "dul-ci-NEA" - like "near," an idealized woman who seems "dulce" (sweet) but far away.'
            },
            'dumbwaiter': {
                'definition': 'A small freight elevator used for carrying food, dishes, or other items between floors in a building.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DUM-way-ter (emphasis on first syllable)',
                'etymology': 'From "dumb" (silent) + "waiter." A silent servant that carries items between floors.',
                'language_origins': 'English',
                'example_sentence': 'The restaurant used a _____ to send food from the kitchen to the dining room upstairs.',
                'memory_tip': 'Remember "DUMB-waiter" - a "dumb" (silent) "waiter" that carries things without speaking.'
            },
            'dunk': {
                'definition': 'To dip or plunge something briefly into liquid; in basketball, to thrust the ball down through the hoop.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'DUNK (rhymes with "bunk")',
                'etymology': 'From Pennsylvania German "dunke" meaning "to dip." About plunging into liquid.',
                'language_origins': 'Pennsylvania German',
                'example_sentence': 'She loved to _____ her cookies in milk before eating them.',
                'memory_tip': 'Simple "DUNK" rhymes with "sunk" - you dunk things down until they\'re briefly sunk in liquid.'
            },
            'dunkin': {
                'definition': 'Present participle of "dunk" (informal); the action of dipping or plunging repeatedly. Also a brand name.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'DUN-kin (emphasis on first syllable)',
                'etymology': 'From "dunk" + "-in" suffix. Informal present participle of dipping action.',
                'language_origins': 'English',
                'example_sentence': 'He was _____ his donut in coffee when the phone rang.',
                'memory_tip': 'Remember "DUNK-in" - the action of "dunking" something "in" liquid repeatedly.'
            },
            'duodenum': {
                'definition': 'The first part of the small intestine, immediately following the stomach. Anatomical term for digestive system.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'doo-oh-DEE-num (emphasis on third syllable)',
                'etymology': 'From Latin "duodenum" meaning "twelve each" (about twelve finger-widths long). Anatomical terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The surgeon repaired a perforation in the patient\'s _____.',
                'memory_tip': 'Think "doo-oh-DENUM" - the part of intestine about "twelve" finger-widths long after the stomach.'
            },
            'duopoly': {
                'definition': 'A market dominated by two sellers; an economic situation where two companies control most of the market.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'doo-OP-oh-lee (emphasis on second syllable)',
                'etymology': 'From Greek "duo" (two) + "polein" (to sell). Economic terminology about market control.',
                'language_origins': 'Greek',
                'example_sentence': 'The airline industry was essentially a _____ with only two major carriers.',
                'memory_tip': 'Remember "DUO-poly" - a "monopoly" shared by a "duo" (two companies) instead of one.'
            },
            'duplicitous': {
                'definition': 'Deceitful and double-dealing; characterized by deliberate deceptiveness in behavior or speech.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'doo-PLIS-i-tus (emphasis on second syllable)',
                'etymology': 'From Latin "duplicitas" meaning "doubleness" + "-ous." About having two faces or being deceptive.',
                'language_origins': 'Latin',
                'example_sentence': 'His _____ behavior lost him the trust of his business partners.',
                'memory_tip': 'Think "du-PLIC-itous" - someone who "duplicates" themselves, showing two different faces deceptively.'
            },
            'durango': {
                'definition': 'A state in northwestern Mexico; also various cities named after this Mexican state, including Durango, Colorado.',
                'part_of_speech': 'noun (proper)',
                'pronunciation_guide': 'duh-RANG-goh (emphasis on second syllable)',
                'etymology': 'From Basque "urango" meaning "water place." Geographic proper noun.',
                'language_origins': 'Basque',
                'example_sentence': 'The mining town of _____ in Colorado was named after the Mexican state.',
                'memory_tip': 'Remember "duh-RANGO" - sounds like "the ranch go," places in the American West and Mexico.'
            },
            'duress': {
                'definition': 'Pressure or constraint exerted upon someone; threats or force used to compel someone to act against their will.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'duh-RES (emphasis on second syllable)',
                'etymology': 'From Old French "duresse" from Latin "duritia" meaning "hardness." Legal terminology.',
                'language_origins': 'Latin via Old French',
                'example_sentence': 'He signed the contract under _____, threatened with losing his job.',
                'memory_tip': 'Think "duh-RESS" - under such pressure and stress that you\'re in distress and duress.'
            },
            'durham': {
                'definition': 'A city and county in northeastern England; also various places in North America named after the English city.',
                'part_of_speech': 'noun (proper)',
                'pronunciation_guide': 'DUR-um (emphasis on first syllable)',
                'etymology': 'From Old English "Dunholm" meaning "hill island." Geographic proper noun.',
                'language_origins': 'Old English',
                'example_sentence': 'The university town of _____ is famous for its Norman cathedral.',
                'memory_tip': 'Remember "DUR-ham" - a "durable" place name used for cities in England and America.'
            },
            'during': {
                'definition': 'Throughout the course or continuance of a time period; at some point in the course of an event or period.',
                'part_of_speech': 'preposition',
                'pronunciation_guide': 'DUR-ing (emphasis on first syllable)',
                'etymology': 'From "dure" (to last) + "-ing" suffix. About the time something lasts or continues.',
                'language_origins': 'English',
                'example_sentence': 'She fell asleep _____ the long movie.',
                'memory_tip': 'Simple "DUR-ing" - "during" shows when something happens while something else "endures" or lasts.'
            },
            'dusk': {
                'definition': 'The time of day immediately following sunset; twilight when daylight fades into darkness.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DUSK (rhymes with "tusk")',
                'etymology': 'From Middle English "dosk" meaning "dark, shadowy." About the transition to darkness.',
                'language_origins': 'Middle English',
                'example_sentence': 'The streetlights came on automatically at _____ each evening.',
                'memory_tip': 'Remember "DUSK" rhymes with "tusk" - when elephants become hard to see in the fading light.'
            },
            'duties': {
                'definition': 'Plural of duty; moral or legal obligations; tasks required by one\'s position or role; taxes on imports.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOO-teez (emphasis on first syllable)',
                'etymology': 'From "duty" (from Anglo-French "dueté") + plural "-s." About obligations and responsibilities.',
                'language_origins': 'Anglo-French',
                'example_sentence': 'The security guard\'s _____ included checking all doors and windows.',
                'memory_tip': 'Remember "DOO-ties" - things you "do" because they\'re your duties and responsibilities.'
            },
            'dutifully': {
                'definition': 'In a dutiful manner; conscientiously fulfilling one\'s obligations; obediently and responsibly.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'DOO-ti-ful-ee (emphasis on first syllable)',
                'etymology': 'From "dutiful" (duty + "-ful") + "-ly" suffix. About performing obligations conscientiously.',
                'language_origins': 'English formation',
                'example_sentence': 'She _____ completed all her assignments before the deadline.',
                'memory_tip': 'Think "DOO-ti-fully" - doing your "duties" "fully" and conscientiously with care.'
            },
            'duvet': {
                'definition': 'A soft quilt filled with down or synthetic material, used as a bed covering; a comforter or continental quilt.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'doo-VAY (emphasis on second syllable)',
                'etymology': 'From French "duvet" meaning "down" (soft feathers). Bedding terminology.',
                'language_origins': 'French',
                'example_sentence': 'She snuggled under the warm _____ on the cold winter morning.',
                'memory_tip': 'Remember "doo-VAY" - a French word for a cozy bed covering that you "do" "weigh" down with for warmth.'
            },
            'duxelles': {
                'definition': 'A finely chopped mixture of mushrooms, onions, and herbs, sautéed until dry; used as a stuffing or garnish in cooking.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dook-SELL (emphasis on second syllable)',
                'etymology': 'Named after the Marquis d\'Uxelles, a 17th-century French nobleman. Culinary terminology.',
                'language_origins': 'French (eponym)',
                'example_sentence': 'The chef prepared a _____ to stuff inside the beef Wellington.',
                'memory_tip': 'Think "dook-SELLS" - a fancy French mushroom mixture that chefs "sell" as gourmet cooking.'
            },
            'dvandva': {
                'definition': 'A type of compound word in Sanskrit grammar where both elements are equal and joined by "and"; a coordinative compound.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DVAN-dva (emphasis on first syllable)',
                'etymology': 'From Sanskrit "dvandva" meaning "pair, couple." Linguistic and grammatical terminology.',
                'language_origins': 'Sanskrit',
                'example_sentence': 'The compound "prince-princess" is an example of a _____ formation.',
                'memory_tip': 'Remember "DVAN-dva" - a Sanskrit compound where two words are "divided" equally like a pair.'
            },
            'dvorak': {
                'definition': 'Relating to Antonín Dvořák, Czech composer; also refers to the Dvorak keyboard layout designed for typing efficiency.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'duh-VOR-zhahk (emphasis on second syllable)',
                'etymology': 'Czech surname meaning "courtier." Used for composer and keyboard layout named after him.',
                'language_origins': 'Czech',
                'example_sentence': 'Some typists prefer the _____ keyboard layout over the standard QWERTY arrangement.',
                'memory_tip': 'Think "duh-VOR-zhak" - a Czech name associated with both beautiful music and efficient typing.'
            }
        }
        
        return batch_055_data.get(word.lower(), {})
    
    def calculate_difficulty_scores(self, word: str) -> tuple:
        """Calculate the 4 difficulty component scores"""
        calc = DifficultyCalculator()
        
        phonetic_score = calc.calculate_phonetic_transparency(word)
        frequency_score = calc.calculate_word_frequency(word)
        morphological_score = calc.calculate_morphological_complexity(word)
        etymology_score = calc.calculate_etymology_complexity(word)
        
        return phonetic_score, frequency_score, morphological_score, etymology_score
    
    def process_csv(self, input_file: str, output_file: str):
        """Process the CSV file and generate comprehensive data"""
        try:
            print(f"Processing {input_file}...")
            
            # Read input CSV
            input_path = f"C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/{input_file}"
            df = pd.read_csv(input_path)
            
            processed_words = []
            
            for _, row in df.iterrows():
                word = row['word'].strip()
                
                # Get comprehensive data
                word_data = self.get_comprehensive_claude_data(word)
                
                if not word_data:
                    print(f"No data found for word: {word}")
                    continue
                
                # Handle error cases
                if word_data.get('is_error', False):
                    processed_word = WordData(
                        word=word,
                        definition="",
                        part_of_speech="",
                        pronunciation_guide="",
                        etymology="",
                        language_origins="",
                        example_sentence="",
                        memory_tip="",
                        phonetic_transparency_score=0,
                        word_frequency_score=0,
                        morphological_complexity_score=0,
                        etymology_complexity_score=0,
                        source_difficulty=row['source_difficulties'],
                        years=row['years'],
                        source_files=row['source_files'],
                        is_error=True,
                        error_message=word_data['error_message']
                    )
                else:
                    # Calculate difficulty scores
                    phonetic_score, frequency_score, morphological_score, etymology_score = self.calculate_difficulty_scores(word)
                    
                    processed_word = WordData(
                        word=word,
                        definition=word_data['definition'],
                        part_of_speech=word_data['part_of_speech'],
                        pronunciation_guide=word_data['pronunciation_guide'],
                        etymology=word_data['etymology'],
                        language_origins=word_data['language_origins'],
                        example_sentence=word_data['example_sentence'],
                        memory_tip=word_data['memory_tip'],
                        phonetic_transparency_score=phonetic_score,
                        word_frequency_score=frequency_score,
                        morphological_complexity_score=morphological_score,
                        etymology_complexity_score=etymology_score,
                        source_difficulty=row['source_difficulties'],
                        years=row['years'],
                        source_files=row['source_files']
                    )
                
                processed_words.append(processed_word)
            
            # Write output CSV
            output_path = f"C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/{output_file}"
            
            fieldnames = [
                'word', 'definition', 'part_of_speech', 'pronunciation_guide',
                'etymology', 'language_origins', 'example_sentence', 'memory_tip',
                'phonetic_transparency_score', 'word_frequency_score',
                'morphological_complexity_score', 'etymology_complexity_score',
                'difficulty', 'definition_source', 'pronunciation_source',
                'etymology_source', 'memory_tip_source', 'example_sentence_source',
                'source_difficulty', 'years', 'source_files', 'is_error', 'error_message'
            ]
            
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for word_data in processed_words:
                    row_dict = {
                        'word': word_data.word,
                        'definition': word_data.definition,
                        'part_of_speech': word_data.part_of_speech,
                        'pronunciation_guide': word_data.pronunciation_guide,
                        'etymology': word_data.etymology,
                        'language_origins': word_data.language_origins,
                        'example_sentence': word_data.example_sentence,
                        'memory_tip': word_data.memory_tip,
                        'phonetic_transparency_score': word_data.phonetic_transparency_score,
                        'word_frequency_score': word_data.word_frequency_score,
                        'morphological_complexity_score': word_data.morphological_complexity_score,
                        'etymology_complexity_score': word_data.etymology_complexity_score,
                        'difficulty': word_data.difficulty,
                        'definition_source': word_data.definition_source,
                        'pronunciation_source': word_data.pronunciation_source,
                        'etymology_source': word_data.etymology_source,
                        'memory_tip_source': word_data.memory_tip_source,
                        'example_sentence_source': word_data.example_sentence_source,
                        'source_difficulty': word_data.source_difficulty,
                        'years': word_data.years,
                        'source_files': word_data.source_files,
                        'is_error': word_data.is_error,
                        'error_message': word_data.error_message
                    }
                    writer.writerow(row_dict)
            
            print(f"Successfully processed {len(processed_words)}/50 words to {output_file}")
            
            # Report any errors found
            error_words = [w for w in processed_words if w.is_error]
            if error_words:
                print(f"Found {len(error_words)} error(s):")
                for error_word in error_words:
                    print(f"  - {error_word.word}: {error_word.error_message}")
            
            return True
            
        except Exception as e:
            print(f"Error processing CSV: {str(e)}")
            return False

def main():
    processor = Batch055Processor()
    success = processor.process_csv("batch_055_words.csv", "batch_055_processed.csv")
    
    if success:
        print("Batch 055 processing completed successfully!")
    else:
        print("Batch 055 processing failed!")

if __name__ == "__main__":
    main()