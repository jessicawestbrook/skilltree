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
        
        high_freq = ['discussion', 'disease', 'display', 'distance', 'distinguish', 'distinguishing', 'dish', 'disguise', 'disorder']
        medium_freq = ['dispute', 'distinctive', 'discoveries', 'discovering', 'discarded', 'dismayed', 'dissolved', 'distracted']
        
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
        prefixes = ['dis-']
        suffixes = ['-tion', '-ing', '-ed', '-ly', '-ance', '-ment', '-ary', '-ate', '-ive']
        
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
        elif any(word_lower.startswith(prefix) for prefix in ['dis']):
            return 5
        else:
            return 3

class Batch052Processor:
    def __init__(self):
        self.base_path = "/c/Users/jessi/Projects/skilltree2/scripts/spelling_bee"
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive data using Claude's knowledge"""
        
        batch_052_data = {
            'discarded': {
                'definition': 'Rejected as worthless or unnecessary; thrown away or abandoned as no longer useful. Past tense of discard, indicating something that has been deliberately eliminated or gotten rid of because it lacks value or purpose.',
                'part_of_speech': 'verb, adjective',
                'pronunciation_guide': 'dis-KAR-ded (emphasis on second syllable)',
                'etymology': 'From prefix "dis-" (away) + "card" (from Latin "charta" meaning "paper"). Originally from card games, meaning to throw away unwanted cards.',
                'language_origins': 'Latin via French',
                'example_sentence': 'The researcher _____ the flawed data that contained obvious measurement errors.',
                'memory_tip': 'Think "dis-CARDed" - like throwing away unwanted playing cards, you discard things you don\'t want or need.'
            },
            'disciform': {
                'definition': 'Having the shape of a disc; flat and circular like a disk. Used in medical and biological contexts to describe structures that are disc-shaped, such as certain lesions, growths, or anatomical features.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DIS-ki-form (emphasis on first syllable)',
                'etymology': 'From Latin "discus" (disc, disk) + "forma" (form, shape). Medical and scientific terminology for disc-shaped structures.',
                'language_origins': 'Latin',
                'example_sentence': 'The doctor identified a _____ lesion on the patient\'s retina during the eye examination.',
                'memory_tip': 'Remember "DISC-i-form" - shaped like a "disc," having the "form" of a flat, round disk.'
            },
            'disclaimer': {
                'definition': 'A statement that denies responsibility or liability; a formal declaration that rejects legal responsibility for something. Commonly used to protect individuals or organizations from claims or lawsuits.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dis-KLAY-mer (emphasis on second syllable)',
                'etymology': 'From prefix "dis-" (not) + "claim" + "-er" suffix. Legal terminology meaning to not claim responsibility.',
                'language_origins': 'English (legal formation)',
                'example_sentence': 'The website included a _____ stating that the company was not responsible for user-generated content.',
                'memory_tip': 'Think "dis-CLAIMer" - you "disclaim" or refuse to "claim" responsibility for something.'
            },
            'discombobulate': {
                'definition': 'To confuse or disconcert someone; to upset or frustrate by causing confusion or bewilderment. A humorous, informal word that suggests being thrown into a state of mental disarray.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dis-kom-BOB-yuh-late (emphasis on third syllable)',
                'etymology': 'American slang, possibly alteration of "discompose" or "discomfit." Playful formation suggesting confusion and disorder.',
                'language_origins': 'English (American slang)',
                'example_sentence': 'The unexpected change in plans seemed to _____ everyone at the meeting.',
                'memory_tip': 'Think "dis-kom-BOBulate" - like a "bobblehead" shaking around, you feel confused and disoriented.'
            },
            'discomfiture': {
                'definition': 'A feeling of unease or embarrassment; the state of being frustrated or defeated. A formal term describing the discomfort that comes from being thwarted, confused, or put in an awkward position.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dis-KUM-fi-chur (emphasis on second syllable)',
                'etymology': 'From Old French "desconfiture" meaning "defeat" (des- "un-" + confire "to prepare"). Via Middle English.',
                'language_origins': 'Old French',
                'example_sentence': 'His _____ was evident when he realized he had been arguing the wrong side of the debate.',
                'memory_tip': 'Remember "dis-COMfiture" - the opposite of "comfort," it\'s the discomfort of being confused or defeated.'
            },
            'disconcerting': {
                'definition': 'Causing one to feel unsettled, disturbed, or worried; disturbing in a way that makes someone feel uneasy or confused. Describes situations or information that upset one\'s sense of stability or confidence.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dis-kon-SUR-ting (emphasis on third syllable)',
                'etymology': 'From prefix "dis-" + "concert" (harmony) + "-ing." Originally meaning to disturb the harmony or order of something.',
                'language_origins': 'French via English',
                'example_sentence': 'The student found the professor\'s sudden change in grading policy quite _____.',
                'memory_tip': 'Think "dis-CONCERTing" - like disrupting a concert, it disturbs your peace and makes you feel unsettled.'
            },
            'disconsolate': {
                'definition': 'Very unhappy and unable to be comforted; deeply dejected and without hope of consolation. Describes a state of profound sadness that seems beyond the reach of comfort or relief.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dis-KON-suh-lit (emphasis on second syllable)',
                'etymology': 'From Latin "disconsolatus" meaning "unconsoled" (dis- "not" + consolatus "consoled"). Emotional terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'She remained _____ for weeks after losing her beloved pet.',
                'memory_tip': 'Remember "dis-CONSOLate" - unable to be "consoled," too sad to find comfort or consolation.'
            },
            'discord': {
                'definition': 'Disagreement or lack of harmony between people or things; in music, a combination of notes that sound harsh or unpleasant together. Can refer to social conflict or musical dissonance.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DIS-kord (emphasis on first syllable)',
                'etymology': 'From Latin "discordia" meaning "disagreement" (dis- "apart" + cor "heart"). Musical and social terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The family reunion was marked by _____ over inheritance issues.',
                'memory_tip': 'Think "DIS-cord" - when hearts are "dis" (apart), there\'s no harmony, creating discord and disagreement.'
            },
            'discountenance': {
                'definition': 'To refuse to approve of or support something; to discourage or show disapproval. Can also mean to cause someone to feel embarrassed or disconcerted.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dis-KOWN-tuh-nans (emphasis on second syllable)',
                'etymology': 'From prefix "dis-" (not) + "countenance" (approval, support). Formation meaning to withhold approval.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'The principal decided to _____ any further disruptions during the assembly.',
                'memory_tip': 'Think "dis-COUNTenance" - to "discount" or refuse to "count" your approval for something.'
            },
            'discoveries': {
                'definition': 'Plural of discovery; findings of something previously unknown or the act of finding such things. Can refer to scientific breakthroughs, archaeological finds, or personal realizations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dis-KUV-er-eez (emphasis on second syllable)',
                'etymology': 'From prefix "dis-" (un-) + "cover" + "-y" suffix + plural "-ies." Meaning to uncover what was hidden.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'The archaeologist\'s _____ in the ancient tomb revolutionized understanding of the civilization.',
                'memory_tip': 'Remember "dis-COVERies" - you "discover" by "uncovering" things that were hidden, making new findings.'
            },
            'discovering': {
                'definition': 'Present participle of discover; the process of finding or learning something for the first time. The ongoing action of uncovering new information, places, or understanding.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dis-KUV-er-ing (emphasis on second syllable)',
                'etymology': 'From prefix "dis-" (un-) + "cover" + "-ing" suffix. Progressive form of finding something previously unknown.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'She spent her vacation _____ hidden gems in the small mountain town.',
                'memory_tip': 'Think "dis-COVERing" - actively "uncovering" and finding new things, removing the cover from mysteries.'
            },
            'discreetly': {
                'definition': 'In a careful and prudent manner, avoiding attention or causing offense; with tact and sensitivity. Acting in a way that shows good judgment and consideration for others.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'dis-KREET-lee (emphasis on second syllable)',
                'etymology': 'From Latin "discretus" meaning "separate, distinct" + "-ly." Via Old French "discret" meaning "wise, tactful."',
                'language_origins': 'Latin via Old French',
                'example_sentence': 'She _____ slipped the note to her friend during the meeting.',
                'memory_tip': 'Remember "dis-CREETly" - acting with "discrete" judgment, being subtle and careful not to attract attention.'
            },
            'discretionary': {
                'definition': 'Available for use at one\'s own discretion; involving the freedom to decide what should be done in particular circumstances. Often refers to funds, powers, or decisions left to individual judgment.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dis-KRESH-uh-nair-ee (emphasis on second syllable)',
                'etymology': 'From Latin "discretio" meaning "separation, distinction" + "-ary" suffix. Related to the ability to distinguish and choose.',
                'language_origins': 'Latin',
                'example_sentence': 'The judge had _____ authority to determine the length of the sentence.',
                'memory_tip': 'Think "dis-CRETionary" - like having a "secret" choice, you get to use your own judgment and discretion.'
            },
            'discriminating': {
                'definition': 'Having or showing refined taste or good judgment; able to distinguish between different things or people. Can also refer to treating people differently based on prejudice.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'dis-KRIM-uh-nay-ting (emphasis on second syllable)',
                'etymology': 'From Latin "discriminare" meaning "to divide, distinguish" + "-ing." Related to the ability to make distinctions.',
                'language_origins': 'Latin',
                'example_sentence': 'She has a _____ palate that can detect subtle differences in wine flavors.',
                'memory_tip': 'Remember "dis-CRIMinating" - making "critical" distinctions, able to distinguish between things with good judgment.'
            },
            'discussion': {
                'definition': 'The action or process of talking about something in order to reach a decision or exchange ideas; a conversation or debate about a particular topic.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dis-KUSH-un (emphasis on second syllable)',
                'etymology': 'From Latin "discussio" meaning "examination, investigation" (dis- "apart" + quatere "to shake"). Via Old French.',
                'language_origins': 'Latin via Old French',
                'example_sentence': 'The committee held a lengthy _____ about the proposed budget changes.',
                'memory_tip': 'Think "dis-CUSSion" - like "discussing" and "cussing" out ideas, talking them through thoroughly.'
            },
            'disdain': {
                'definition': 'The feeling that someone or something is unworthy of consideration or respect; contempt or scorn. A strong attitude of disrespect or dismissal.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'dis-DAYN (emphasis on second syllable)',
                'etymology': 'From Old French "desdaignier" meaning "to consider unworthy" (des- "un-" + daignier "to deign"). Via Middle English.',
                'language_origins': 'Old French',
                'example_sentence': 'She looked upon the poorly prepared presentation with obvious _____.',
                'memory_tip': 'Remember "dis-DAIN" - you "disdain" something when you don\'t "deign" it worthy of respect.'
            },
            'disease': {
                'definition': 'A disorder of structure or function in a human, animal, or plant that produces specific symptoms; an illness or sickness that affects normal functioning.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dih-ZEEZ (emphasis on second syllable)',
                'etymology': 'From Old French "desaise" meaning "lack of ease" (des- "without" + aise "ease"). Medical terminology.',
                'language_origins': 'Old French',
                'example_sentence': 'Early detection of the _____ greatly improved the patient\'s treatment options.',
                'memory_tip': 'Think "dis-EASE" - the absence of "ease," when your body is not at ease or comfortable due to illness.'
            },
            'disembark': {
                'definition': 'To get off a ship, aircraft, or other vehicle; to go ashore or leave a mode of transportation. The process of passengers or cargo leaving a vessel.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dis-em-BARK (emphasis on third syllable)',
                'etymology': 'From prefix "dis-" (off) + "embark" (to board). Meaning the opposite of embarking or boarding.',
                'language_origins': 'English formation from French roots',
                'example_sentence': 'Passengers were asked to _____ from the plane in an orderly fashion.',
                'memory_tip': 'Remember "dis-EMBARK" - the opposite of "embark," you get off the vessel instead of getting on.'
            },
            'disembodied': {
                'definition': 'Separated from or lacking a physical body; existing without bodily form. Often refers to voices, spirits, or abstract concepts that seem to lack physical presence.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dis-em-BOD-eed (emphasis on third syllable)',
                'etymology': 'From prefix "dis-" (without) + "embody" + "-ed." Meaning lacking physical embodiment.',
                'language_origins': 'English formation',
                'example_sentence': 'A _____ voice echoed through the empty hallway, startling the security guard.',
                'memory_tip': 'Think "dis-em-BODied" - without a "body," existing as spirit or voice without physical form.'
            },
            'disembogue': {
                'definition': 'To discharge or flow out, especially of a river flowing into the sea; to emerge from a confined space into a larger area. Technical term often used in geography.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dis-em-BOHG (emphasis on third syllable)',
                'etymology': 'From Spanish "desembocar" meaning "to flow out" (des- "out" + emboca "mouth"). Geographic terminology.',
                'language_origins': 'Spanish',
                'example_sentence': 'The river will _____ into the bay after winding through the mountain valley.',
                'memory_tip': 'Remember "dis-em-BOGUE" - like "bogey" flowing out, water flowing from a narrow space into open water.'
            },
            'disgorged': {
                'definition': 'Past tense of disgorge; discharged or poured forth violently or in large quantities; gave up unwillingly. Can refer to liquids, objects, or information being released.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dis-GORJD (emphasis on second syllable)',
                'etymology': 'From Old French "desgorger" meaning "to clear the throat" (des- "un-" + gorge "throat"). Originally about clearing blockages.',
                'language_origins': 'Old French',
                'example_sentence': 'The bus _____ its passengers at the busy terminal.',
                'memory_tip': 'Think "dis-GORGED" - like clearing the "gorge" (throat), forcefully expelling what was inside.'
            },
            'disgruntled': {
                'definition': 'Angry or dissatisfied; upset and annoyed due to unfair treatment or unmet expectations. Feeling displeased and resentful about a situation.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dis-GRUN-tuld (emphasis on second syllable)',
                'etymology': 'From prefix "dis-" (reverse) + "gruntled" (pleased). Ironically, "gruntled" is rarely used; "disgruntled" is the common form.',
                'language_origins': 'English',
                'example_sentence': 'The _____ employees complained about the lack of pay raises.',
                'memory_tip': 'Remember "dis-GRUNTled" - so unhappy you "grunt" with displeasure instead of being pleased.'
            },
            'disguise': {
                'definition': 'To change the appearance or character of something to conceal its identity; a means of altering one\'s appearance to avoid recognition. Can be physical or metaphorical concealment.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'dis-GYZE (emphasis on second syllable)',
                'etymology': 'From Old French "desguiser" meaning "to change costume" (des- "away" + guise "manner, fashion"). Related to disguising identity.',
                'language_origins': 'Old French',
                'example_sentence': 'The spy used a clever _____ to infiltrate the enemy organization.',
                'memory_tip': 'Think "dis-GUISE" - to change your "guise" (appearance) so people can\'t recognize you.'
            },
            'dish': {
                'definition': 'A shallow, flat-bottomed container for cooking or serving food; a particular type of prepared food; to serve or present food. Can also mean to gossip or provide information.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DISH (rhymes with "wish")',
                'etymology': 'From Old English "disc" from Latin "discus" meaning "disk, plate." Related to flat, round serving vessels.',
                'language_origins': 'Old English from Latin',
                'example_sentence': 'She prepared her grandmother\'s favorite _____ for the family dinner.',
                'memory_tip': 'Simple "DISH" - like a disk or plate, a flat container for serving food.'
            },
            'dishevel': {
                'definition': 'To make untidy or messy, especially hair or clothing; to disturb the neat arrangement of something. To cause disorder in appearance.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-SHEV-ul (emphasis on second syllable)',
                'etymology': 'From Old French "descheveler" meaning "to disarrange the hair" (des- "un-" + chevel "hair"). Originally about messy hair.',
                'language_origins': 'Old French',
                'example_sentence': 'The strong wind managed to _____ her carefully styled hair.',
                'memory_tip': 'Think "dih-SHEVel" - to "shove" your hair around until it\'s messy and disheveled.'
            },
            'disinfectant': {
                'definition': 'A chemical agent that destroys or inhibits the growth of harmful microorganisms on surfaces or objects. Used for cleaning and sterilization to prevent infection.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'dis-in-FEK-tunt (emphasis on third syllable)',
                'etymology': 'From prefix "dis-" (remove) + "infect" + "-ant" suffix. Meaning something that removes infection.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'The hospital staff used a strong _____ to clean all surfaces thoroughly.',
                'memory_tip': 'Remember "dis-INFECT-ant" - a substance that "dis" (removes) "infection" to keep things clean.'
            },
            'disintegration': {
                'definition': 'The process of breaking down or falling apart into small pieces; the destruction of unity or cohesion. Can be physical breakdown or social/organizational collapse.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dis-in-tuh-GRAY-shun (emphasis on fourth syllable)',
                'etymology': 'From prefix "dis-" (apart) + "integrate" + "-tion." Meaning the breakdown of integrated wholeness.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'The _____ of the ancient manuscript made it difficult to read the text.',
                'memory_tip': 'Think "dis-INTEGRATION" - the opposite of integration, things falling apart instead of coming together.'
            },
            'disjunct': {
                'definition': 'Lacking connection or coherence; disconnected or separate. In logic and linguistics, refers to elements that are mutually exclusive or not related.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'dis-JUNKT (emphasis on second syllable)',
                'etymology': 'From Latin "disjunctus" meaning "separated" (dis- "apart" + jungere "to join"). Logical and linguistic terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The professor\'s lecture seemed _____, jumping between unrelated topics.',
                'memory_tip': 'Remember "dis-JUNCT" - the opposite of being "joined," things are separated and disconnected.'
            },
            'dismal': {
                'definition': 'Causing a mood of gloom or depression; dreary and depressing. Describes conditions, weather, or situations that are particularly bleak or discouraging.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DIZ-mul (emphasis on first syllable)',
                'etymology': 'From Latin "dies mali" meaning "evil days." Originally referred to 24 unlucky days in the medieval calendar.',
                'language_origins': 'Latin',
                'example_sentence': 'The _____ weather matched his mood after receiving the disappointing news.',
                'memory_tip': 'Think "DISmal" - so bad it makes you feel "dismal" and gloomy, like evil days.'
            },
            'dismayed': {
                'definition': 'Feeling troubled, disappointed, or distressed by something unexpected; shocked or concerned by an unpleasant discovery or event.',
                'part_of_speech': 'verb, adjective',
                'pronunciation_guide': 'dis-MAYD (emphasis on second syllable)',
                'etymology': 'From Old French "esmayer" meaning "to trouble, disturb." Via prefix "dis-" meaning reversal of composure.',
                'language_origins': 'Old French',
                'example_sentence': 'She was _____ to discover that her favorite restaurant had closed.',
                'memory_tip': 'Remember "dis-MAYED" - your mood is "dismayed" when bad news makes you feel troubled and upset.'
            },
            'disneyfication': {
                'definition': 'The transformation of something (usually a place, story, or experience) to resemble the style of Disney theme parks; making something artificially wholesome, sanitized, or commercialized.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIZ-nee-fi-KAY-shun (emphasis on fourth syllable)',
                'etymology': 'From "Disney" (the company) + "-fication" suffix. Modern term describing the process of making things Disney-like.',
                'language_origins': 'English (modern formation)',
                'example_sentence': 'Critics argued that the _____ of the historic downtown area removed its authentic character.',
                'memory_tip': 'Think "DISNEY-fication" - transforming something to be like Disney parks: clean, commercialized, and artificially cheerful.'
            },
            'disorder': {
                'definition': 'A state of confusion or lack of organization; a medical condition that disrupts normal functioning. Can refer to physical disarray or health problems.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'dis-OR-der (emphasis on second syllable)',
                'etymology': 'From prefix "dis-" (not) + "order." Meaning the absence or disruption of proper arrangement.',
                'language_origins': 'English formation',
                'example_sentence': 'The therapist specialized in treating anxiety _____.',
                'memory_tip': 'Remember "dis-ORDER" - the absence of "order," when things are chaotic or not functioning properly.'
            },
            'disparate': {
                'definition': 'Essentially different in kind; not able to be compared because they are so different. Describes things that are fundamentally unlike each other.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DIS-par-it (emphasis on first syllable)',
                'etymology': 'From Latin "disparatus" meaning "separated" (dis- "apart" + parare "to prepare"). Meaning fundamentally different.',
                'language_origins': 'Latin',
                'example_sentence': 'The committee struggled to reconcile the _____ opinions of its members.',
                'memory_tip': 'Think "DIS-parate" - things so "disparate" they can\'t be "paired" together because they\'re fundamentally different.'
            },
            'dispensation': {
                'definition': 'Permission to be exempted from a rule or usual requirement; the distribution or giving out of something. Often refers to official exemptions or the act of dispensing.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dis-pen-SAY-shun (emphasis on third syllable)',
                'etymology': 'From Latin "dispensatio" meaning "management, distribution" (dis- "out" + pendere "to weigh"). Administrative terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The school granted a special _____ allowing the student to graduate despite missing credits.',
                'memory_tip': 'Remember "dis-PENSATION" - like a "dispensary," the official giving out or dispensing of permissions or exemptions.'
            },
            'display': {
                'definition': 'To show or exhibit something for others to see; an arrangement or presentation of objects or information. Can be a noun (the exhibition) or verb (the action).',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'dis-PLAY (emphasis on second syllable)',
                'etymology': 'From Old French "despleier" meaning "to unfold" (des- "un-" + pleier "to fold"). Originally about unfolding for viewing.',
                'language_origins': 'Old French',
                'example_sentence': 'The museum will _____ the ancient artifacts in the new Egyptian wing.',
                'memory_tip': 'Think "dis-PLAY" - to "play" something out for others to see, unfolding it for display.'
            },
            'disposition': {
                'definition': 'A person\'s inherent qualities of mind and character; the way something is arranged or organized. Can refer to temperament or the arrangement of things.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dis-puh-ZISH-un (emphasis on third syllable)',
                'etymology': 'From Latin "dispositio" meaning "arrangement" (dis- "apart" + ponere "to place"). About how things are positioned.',
                'language_origins': 'Latin',
                'example_sentence': 'Her cheerful _____ made her popular among her colleagues.',
                'memory_tip': 'Remember "dis-POSITION" - your "position" or stance in life, how you\'re naturally disposed to act.'
            },
            'disproportionate': {
                'definition': 'Too large or too small in comparison with something else; lacking proper proportion or balance. Describes something that is not appropriately sized relative to other elements.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dis-pruh-POR-shun-it (emphasis on third syllable)',
                'etymology': 'From prefix "dis-" (not) + "proportionate." Meaning lacking proper proportion or balance.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'The punishment seemed _____ to the minor offense committed.',
                'memory_tip': 'Think "dis-PROPORTIONATE" - not in proper "proportion," too big or too small compared to what\'s appropriate.'
            },
            'dispute': {
                'definition': 'A disagreement or argument, especially an official one; to question the truth or validity of something. Can be a noun (the disagreement) or verb (to argue against).',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'dis-PYOOT (emphasis on second syllable)',
                'etymology': 'From Latin "disputare" meaning "to weigh, examine" (dis- "apart" + putare "to think"). Originally about careful examination.',
                'language_origins': 'Latin',
                'example_sentence': 'The neighbors had a lengthy _____ over the property line boundaries.',
                'memory_tip': 'Remember "dis-PUTE" - to "dispute" is to "put" forward opposing arguments and disagree.'
            },
            'disrepair': {
                'definition': 'Poor condition due to neglect or age; the state of needing repairs because of deterioration or damage. Describes buildings, objects, or systems that have fallen into bad condition.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dis-rih-PAIR (emphasis on third syllable)',
                'etymology': 'From prefix "dis-" (not) + "repair." Meaning the absence of proper repair or maintenance.',
                'language_origins': 'English formation',
                'example_sentence': 'The old house had fallen into serious _____ after years of neglect.',
                'memory_tip': 'Think "dis-REPAIR" - the opposite of being in good repair, needing fixes and maintenance.'
            },
            'dissemble': {
                'definition': 'To hide one\'s true motives, feelings, or beliefs; to disguise or conceal one\'s real intentions. Often involves acting in a deceptive manner.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-SEM-bul (emphasis on second syllable)',
                'etymology': 'From Latin "dissimulare" meaning "to disguise" (dis- "apart" + simulare "to make like"). Via Old French.',
                'language_origins': 'Latin via Old French',
                'example_sentence': 'The politician tried to _____ his true feelings about the controversial policy.',
                'memory_tip': 'Remember "dih-SEMble" - like "disassemble," you take apart your true self to hide your real feelings.'
            },
            'dissipate': {
                'definition': 'To disperse or scatter; to squander or waste something, especially money or energy. Can refer to physical dispersal or wasteful spending.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'DIS-uh-payt (emphasis on first syllable)',
                'etymology': 'From Latin "dissipare" meaning "to scatter" (dis- "apart" + supare "to throw"). About scattering or spreading.',
                'language_origins': 'Latin',
                'example_sentence': 'The morning fog began to _____ as the sun rose higher.',
                'memory_tip': 'Think "DIS-sipate" - like sipping away little by little, things gradually disappear or get wasted.'
            },
            'dissolute': {
                'definition': 'Lacking moral restraint; indulging in sensual pleasures or immoral behavior. Describes someone who lives without proper moral boundaries.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DIS-uh-loot (emphasis on first syllable)',
                'etymology': 'From Latin "dissolutus" meaning "loose, unrestrained" (dis- "apart" + solvere "to loosen"). Moral terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The novel depicted the _____ lifestyle of the wealthy aristocrats.',
                'memory_tip': 'Remember "DIS-solute" - morally "dissolved," with restraints "dissolved" away, living without moral boundaries.'
            },
            'dissolved': {
                'definition': 'Past tense of dissolve; melted or mixed completely with a liquid; officially ended or terminated. Can refer to physical dissolution or organizational disbanding.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-ZOLVD (emphasis on second syllable)',
                'etymology': 'From Latin "dissolvere" meaning "to loosen apart" (dis- "apart" + solvere "to loosen"). Past tense formation.',
                'language_origins': 'Latin',
                'example_sentence': 'The sugar completely _____ in the hot tea.',
                'memory_tip': 'Think "dih-SOLVED" - something was "solved" by breaking apart and mixing completely with liquid.'
            },
            'dissonance': {
                'definition': 'A lack of harmony or agreement; in music, a combination of notes that sound harsh together. Can refer to musical discord or general conflict.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIS-uh-nans (emphasis on first syllable)',
                'etymology': 'From Latin "dissonantia" meaning "disagreement in sound" (dis- "apart" + sonare "to sound"). Musical terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The _____ between his actions and his stated beliefs was troubling.',
                'memory_tip': 'Remember "DIS-sonance" - "dis" (bad) "sonance" (sound), when things don\'t sound good together.'
            },
            'dissuade': {
                'definition': 'To persuade someone not to take a particular course of action; to advise against doing something. The opposite of persuade.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-SWAYD (emphasis on second syllable)',
                'etymology': 'From Latin "dissuadere" meaning "to advise against" (dis- "away from" + suadere "to advise"). Persuasion terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'Her parents tried to _____ her from dropping out of college.',
                'memory_tip': 'Think "dih-SUADE" - to "dis" someone from being "swayed," convincing them not to do something.'
            },
            'distance': {
                'definition': 'The length of space between two points; the state of being far apart in space or time. Can be physical measurement or emotional separation.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DIS-tans (emphasis on first syllable)',
                'etymology': 'From Latin "distantia" meaning "standing apart" (dis- "apart" + stare "to stand"). Spatial terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The _____ between the two cities is approximately 200 miles.',
                'memory_tip': 'Remember "DIS-tance" - things "distant" and apart, measured by the space between them.'
            },
            'distinctive': {
                'definition': 'Characteristic of one person or thing, and so serving to distinguish it from others; having a quality that makes something easily recognizable.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dih-STINK-tiv (emphasis on second syllable)',
                'etymology': 'From Latin "distinctivus" meaning "serving to distinguish" (dis- "apart" + stinguere "to mark"). About marking differences.',
                'language_origins': 'Latin',
                'example_sentence': 'The artist\'s _____ style was immediately recognizable in the gallery.',
                'memory_tip': 'Think "dih-STINCTive" - having "distinct" qualities that make something stand out and be recognizable.'
            },
            'distinguish': {
                'definition': 'To recognize the difference between two or more things; to make oneself notable or famous. Can mean to perceive differences or to achieve distinction.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-STING-gwish (emphasis on second syllable)',
                'etymology': 'From Latin "distinguere" meaning "to mark off" (dis- "apart" + stinguere "to prick"). About marking differences.',
                'language_origins': 'Latin',
                'example_sentence': 'She could easily _____ between the twins despite their similar appearance.',
                'memory_tip': 'Remember "dih-STINGuish" - to see what "stings" out as different, recognizing distinctions between things.'
            },
            'distinguishing': {
                'definition': 'Present participle of distinguish; serving to identify or differentiate; the action of recognizing differences or achieving distinction.',
                'part_of_speech': 'verb, adjective',
                'pronunciation_guide': 'dih-STING-gwish-ing (emphasis on second syllable)',
                'etymology': 'From "distinguish" + "-ing" suffix. Progressive form of recognizing differences or achieving distinction.',
                'language_origins': 'Latin with English suffix',
                'example_sentence': 'His _____ characteristic was his remarkable ability to remember names.',
                'memory_tip': 'Think "dih-STINGuishing" - actively making things "sting" out as different, creating distinctions.'
            },
            'distracted': {
                'definition': 'Unable to concentrate because one\'s mind is preoccupied with other thoughts; having one\'s attention diverted from the main focus.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'dih-STRAK-ted (emphasis on second syllable)',
                'etymology': 'From Latin "distractus" meaning "pulled apart" (dis- "apart" + trahere "to pull"). About attention being pulled away.',
                'language_origins': 'Latin',
                'example_sentence': 'She felt _____ during the meeting, thinking about her sick child at home.',
                'memory_tip': 'Remember "dih-STRACted" - your attention gets "tracked" away from where it should be, pulled in different directions.'
            }
        }
        
        return batch_052_data.get(word.lower(), {})
    
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
    processor = Batch052Processor()
    success = processor.process_csv("batch_052_words.csv", "batch_052_processed.csv")
    
    if success:
        print("Batch 052 processing completed successfully!")
    else:
        print("Batch 052 processing failed!")

if __name__ == "__main__":
    main()