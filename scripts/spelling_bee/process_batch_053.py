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
        
        high_freq = ['doctor', 'does', 'doesn', 'done', 'divided', 'divine', 'diversity', 'domain', 'dome', 'domesticated']
        medium_freq = ['documentary', 'documentaries', 'disturbed', 'diverge', 'diversion', 'divulge', 'dodge', 'dolphin', 'donkeys', 'donut', 'donuts']
        
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
        prefixes = ['dis-', 'div-', 'do-']
        suffixes = ['-tion', '-ing', '-ed', '-ly', '-ary', '-ment', '-ive', '-ous', '-ity']
        
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
        elif any(word_lower.startswith(prefix) for prefix in ['dis', 'div', 'do']):
            return 5
        else:
            return 3

class Batch053Processor:
    def __init__(self):
        self.base_path = "/c/Users/jessi/Projects/skilltree2/scripts/spelling_bee"
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive data using Claude's knowledge"""
        
        batch_053_data = {
            'distraught': {
                'definition': 'Deeply upset and agitated; extremely worried, troubled, or distressed. Describes a state of emotional turmoil where someone is so disturbed they can barely think clearly or function normally.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dis-TRAWT (emphasis on second syllable)',
                'etymology': 'From Middle English, alteration of "distract" influenced by "taught." Originally meaning "pulled in different directions."',
                'language_origins': 'Middle English',
                'example_sentence': 'The mother was _____ when she couldn\'t locate her young child in the crowded mall.',
                'memory_tip': 'Think "dis-TRAUGHT" - so emotionally "wrought" up that you\'re "dis" (completely) disturbed and upset.'
            },
            'distressed': {
                'definition': 'Experiencing anxiety, sorrow, or pain; showing signs of strain or damage. Can refer to emotional suffering or physical deterioration.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'dis-TREST (emphasis on second syllable)',
                'etymology': 'From Old French "destresse" meaning "constraint, oppression" (des- "apart" + estrecier "to constrain"). Via Middle English.',
                'language_origins': 'Old French',
                'example_sentence': 'The _____ furniture had a deliberately aged appearance that was popular in rustic decor.',
                'memory_tip': 'Remember "dis-TRESSED" - under so much "stress" that you\'re in emotional or physical distress.'
            },
            'disturbancewily': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "disturbancewily" appears to be "disturbance" + "wily" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'disturbed': {
                'definition': 'Having had one\'s peace or rest interrupted; mentally or emotionally unbalanced; moved from a settled position. Can describe interruption, mental instability, or physical displacement.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'dis-TURBD (emphasis on second syllable)',
                'etymology': 'From Latin "disturbare" meaning "to throw into disorder" (dis- "completely" + turba "crowd, disorder"). Past tense of disturb.',
                'language_origins': 'Latin',
                'example_sentence': 'The patient showed signs of being emotionally _____ after the traumatic event.',
                'memory_tip': 'Think "dis-TURBED" - someone whose peace has been "turned" upside down, completely disrupted.'
            },
            'diurnal': {
                'definition': 'Relating to or occurring during the daytime; active during the day rather than at night. Opposite of nocturnal, describing animals, plants, or activities associated with daylight hours.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'die-UR-nul (emphasis on second syllable)',
                'etymology': 'From Latin "diurnalis" meaning "daily" (from dies "day"). Scientific terminology for day-related activities.',
                'language_origins': 'Latin',
                'example_sentence': 'Most birds are _____ creatures that are active during daylight hours.',
                'memory_tip': 'Remember "die-URNal" - like a "journal" you write during the day, diurnal means active in daytime.'
            },
            'diva': {
                'definition': 'A celebrated female opera singer; a person, especially a woman, regarded as temperamental or haughty. Originally positive but now often implies demanding or difficult behavior.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DEE-vah (emphasis on first syllable)',
                'etymology': 'From Italian "diva" meaning "goddess" (from Latin "diva" feminine of "divus" meaning "divine"). Opera terminology.',
                'language_origins': 'Italian from Latin',
                'example_sentence': 'The opera _____ demanded fresh flowers in her dressing room before every performance.',
                'memory_tip': 'Think "DEE-vah" - a "divine" female singer who acts like a goddess, sometimes demanding special treatment.'
            },
            'divanbadminton': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "divanbadminton" appears to be "divan" + "badminton" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'diverge': {
                'definition': 'To separate and go in different directions; to differ in opinion, character, or form. Can refer to physical paths separating or ideas/opinions moving apart.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'die-VERJ (emphasis on second syllable)',
                'etymology': 'From Latin "divergere" meaning "to incline apart" (dis- "apart" + vergere "to bend, turn"). Mathematical and general usage.',
                'language_origins': 'Latin',
                'example_sentence': 'The hiking trail will _____ at the creek, with one path leading to the lake and the other to the mountain.',
                'memory_tip': 'Think "die-VERGE" - to "verge" away from each other, paths or opinions moving apart and diverging.'
            },
            'diversified': {
                'definition': 'Made more varied or diverse; expanded into different areas or types. Often used in business to describe expanding into multiple markets or investments.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'die-VUR-suh-fyed (emphasis on second syllable)',
                'etymology': 'From "diverse" + "-ify" + "-ed." Meaning made diverse or varied in character.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'The company _____ its portfolio by investing in technology, healthcare, and renewable energy.',
                'memory_tip': 'Remember "die-VERSified" - made more "diverse," like different verses in a song, adding variety.'
            },
            'diversion': {
                'definition': 'An activity that diverts the mind from serious concerns; an alternative route for traffic. Can mean entertainment, distraction, or a detour.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'die-VUR-zhun (emphasis on second syllable)',
                'etymology': 'From Latin "divertere" meaning "to turn aside" + "-sion." About turning attention or direction away.',
                'language_origins': 'Latin',
                'example_sentence': 'Reading mystery novels was her favorite _____ after long days at work.',
                'memory_tip': 'Think "die-VERSION" - a different "version" of your path or attention, turning away from the main focus.'
            },
            'diversity': {
                'definition': 'The state of being diverse; a range of different things or people. Refers to variety in race, ethnicity, culture, ideas, or other characteristics.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'die-VUR-si-tee (emphasis on second syllable)',
                'etymology': 'From Latin "diversitas" meaning "difference, variety" (from diversus "different"). Social and general terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The university celebrated its cultural _____ with an international food festival.',
                'memory_tip': 'Remember "die-VERSity" - like different "verses" in a poem, diversity means having many different types together.'
            },
            'divestiture': {
                'definition': 'The action of selling off business interests or investments; the process of getting rid of something, especially assets or subsidiaries.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'die-VEST-i-chur (emphasis on second syllable)',
                'etymology': 'From "divest" (to strip, deprive) + "-iture" suffix. Business and legal terminology about removing investments.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'The corporation announced the _____ of its unprofitable retail division.',
                'memory_tip': 'Think "die-VESTiture" - removing your "vest" (investment), taking off what you previously wore or owned.'
            },
            'divided': {
                'definition': 'Separated into parts; having conflicting opinions or loyalties; split or partitioned. Can refer to physical separation or disagreement.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'dih-VYE-ded (emphasis on second syllable)',
                'etymology': 'From Latin "dividere" meaning "to separate" (dis- "apart" + root related to "widow"). Past tense of divide.',
                'language_origins': 'Latin',
                'example_sentence': 'The committee was _____ on whether to approve the new budget proposal.',
                'memory_tip': 'Remember "dih-VIDed" - like a "video" split into parts, something separated or disagreeing.'
            },
            'divination': {
                'definition': 'The practice of seeking knowledge of the future or unknown through supernatural means; fortune-telling or prophecy using various methods like cards, crystals, or omens.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'div-uh-NAY-shun (emphasis on third syllable)',
                'etymology': 'From Latin "divinatio" meaning "prophecy" (from divinus "divine"). Religious and mystical terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'Ancient priests practiced _____ by interpreting the flight patterns of birds.',
                'memory_tip': 'Think "div-ination" - "divine" knowledge about the future, using supernatural methods to predict what\'s coming.'
            },
            'divine': {
                'definition': 'Having the nature of a god; excellent or delightful; to discover through intuition or insight. Can mean godly, wonderful, or to figure out.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'dih-VYNE (emphasis on second syllable)',
                'etymology': 'From Latin "divinus" meaning "of or belonging to a god" (from divus "god"). Religious and general terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The chef\'s chocolate cake was absolutely _____.',
                'memory_tip': 'Remember "dih-VINE" - like a "vine" that connects to heaven, something godly or wonderfully perfect.'
            },
            'divot': {
                'definition': 'A piece of turf dug out by a golf club in making a stroke; a clump of earth and grass torn up by impact. Golf terminology for displaced grass.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIV-ut (emphasis on first syllable)',
                'etymology': 'Scottish origin, possibly related to "divide." Golf terminology that entered general English usage.',
                'language_origins': 'Scottish',
                'example_sentence': 'The golfer carefully replaced the _____ after his shot to maintain the course.',
                'memory_tip': 'Think "DIV-ot" - you "divide" the grass, creating a clump of turf that flies out when you hit the golf ball.'
            },
            'divulge': {
                'definition': 'To make known private or secret information; to reveal or disclose something that was previously hidden or confidential.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dih-VULJ (emphasis on second syllable)',
                'etymology': 'From Latin "divulgare" meaning "to publish abroad" (dis- "widely" + vulgare "to make common"). About spreading information.',
                'language_origins': 'Latin',
                'example_sentence': 'The witness refused to _____ the location where she had seen the suspect.',
                'memory_tip': 'Remember "dih-VULGE" - to make something "vulgar" (common) by sharing secrets that should stay private.'
            },
            'divvy': {
                'definition': 'To divide and distribute; to share out portions of something among several people. Informal term for splitting something up.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'DIV-ee (emphasis on first syllable)',
                'etymology': 'Short for "divide." Informal American English formation, possibly from "dividend."',
                'language_origins': 'English (informal)',
                'example_sentence': 'The children decided to _____ up the Halloween candy equally among themselves.',
                'memory_tip': 'Think "DIV-vy" - short for "divide," when you "div" (divide) things up into portions to share.'
            },
            'divvyfatuously': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "divvyfatuously" appears to be "divvy" + "fatuously" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'djibouti': {
                'definition': 'A country in the Horn of Africa, located at the southern entrance to the Red Sea. A small nation bordered by Eritrea, Ethiopia, and Somalia, with strategic importance for maritime trade.',
                'part_of_speech': 'noun (proper)',
                'pronunciation_guide': 'jih-BOO-tee (emphasis on second syllable)',
                'etymology': 'From the Afar people\'s name for the area. Geographic proper noun from indigenous African languages.',
                'language_origins': 'Afar (African language)',
                'example_sentence': 'The port city of _____ serves as an important shipping hub for the Red Sea region.',
                'memory_tip': 'Remember "jih-BOOti" - sounds like "ji-booty," the African nation at the "booty" end of the Red Sea.'
            },
            'docket': {
                'definition': 'A list of cases to be heard by a court; an agenda or schedule of business to be conducted. Legal terminology for court schedules.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DOK-it (emphasis on first syllable)',
                'etymology': 'Possibly from "dock" (to cut short) + diminutive "-et." Originally a summary or abstract of a larger document.',
                'language_origins': 'English',
                'example_sentence': 'The judge reviewed the court _____ to see which cases would be heard that day.',
                'memory_tip': 'Think "DOCKet" - like a "dock" where ships line up, a docket is where legal cases line up to be heard.'
            },
            'doctor': {
                'definition': 'A person who is qualified to treat medical conditions; someone who holds a doctoral degree; to alter or tamper with something.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DOK-ter (emphasis on first syllable)',
                'etymology': 'From Latin "doctor" meaning "teacher" (from docere "to teach"). Originally meant a learned person or teacher.',
                'language_origins': 'Latin',
                'example_sentence': 'The _____ carefully examined the patient\'s symptoms before making a diagnosis.',
                'memory_tip': 'Simple "DOCtor" - someone who has the "docs" (documents/degrees) showing they\'re qualified to heal.'
            },
            'documentaries': {
                'definition': 'Plural of documentary; factual films or television programs that document reality for instruction or historical record. Non-fiction media presentations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dok-yuh-MEN-tuh-reez (emphasis on third syllable)',
                'etymology': 'From "document" + "-ary" + plural "-ies." Films that document reality rather than fictional stories.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'She preferred watching nature _____ over fictional movies.',
                'memory_tip': 'Remember "DOCUmentaries" - films that "document" real life, showing actual events and facts.'
            },
            'documentary': {
                'definition': 'A factual film or television program that documents reality; consisting of official documents. Presents actual events, people, or conditions.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'dok-yuh-MEN-tuh-ree (emphasis on third syllable)',
                'etymology': 'From "document" + "-ary" suffix. Media that documents real events rather than fiction.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'The _____ about ocean conservation won several international film awards.',
                'memory_tip': 'Think "DOCUmentary" - a film that "documents" real life, showing actual facts and events.'
            },
            'dodecahedron': {
                'definition': 'A three-dimensional geometric shape with twelve flat pentagonal faces; a polyhedron with twelve plane surfaces. Mathematical and geometric terminology.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'doh-dek-uh-HEE-drun (emphasis on fourth syllable)',
                'etymology': 'From Greek "dodeka" (twelve) + "hedron" (face, seat). Geometric terminology for twelve-faced solid.',
                'language_origins': 'Greek',
                'example_sentence': 'The _____ is one of the five regular polyhedra studied in geometry.',
                'memory_tip': 'Remember "do-DECA-hedron" - "dodeca" (twelve) faces, like a dozen faces on a geometric shape.'
            },
            'dodeseret': {
                'definition': 'A historical phonetic alphabet created for writing English, developed in the 19th century. An alternative writing system with unique characters for English sounds.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'doh-DEZ-er-et (emphasis on second syllable)',
                'etymology': 'From "Deseret," meaning "honeybee" in the Book of Mormon. Created as part of Mormon linguistic projects.',
                'language_origins': 'English (created terminology)',
                'example_sentence': 'The _____ alphabet was an attempt to create a more phonetic writing system for English.',
                'memory_tip': 'Think "do-DESeret" - an alphabet system created to "do" better than regular letters for English sounds.'
            },
            'dodge': {
                'definition': 'To avoid something by moving quickly to one side; to evade or escape from something, especially responsibility or obligation.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'DOHJ (rhymes with "lodge")',
                'etymology': 'Origin uncertain, possibly related to "dock" (to move quickly). Meaning to move suddenly to avoid.',
                'language_origins': 'English (uncertain origin)',
                'example_sentence': 'The politician tried to _____ the reporter\'s difficult questions about the scandal.',
                'memory_tip': 'Remember "DODGE" rhymes with "lodge" - you quickly move to a safe "lodge" to avoid something coming at you.'
            },
            'dodgy': {
                'definition': 'Risky, unreliable, or dishonest; of poor quality or potentially dangerous. British informal term for something questionable or suspicious.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DOH-jee (emphasis on first syllable)',
                'etymology': 'From "dodge" + "-y" suffix. British slang meaning unreliable or suspicious.',
                'language_origins': 'English (British slang)',
                'example_sentence': 'The used car salesman seemed rather _____, so they decided to shop elsewhere.',
                'memory_tip': 'Think "DODGy" - so unreliable that you want to "dodge" it, avoid dealing with it because it\'s suspicious.'
            },
            'does': {
                'definition': 'Third person singular present tense of "do"; performs or carries out an action. Also plural of "doe" (female deer).',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'DUHZ (rhymes with "buzz")',
                'etymology': 'From Old English "dōth," third person singular of "don" (to do). Basic English auxiliary and main verb.',
                'language_origins': 'Old English',
                'example_sentence': 'She _____ her homework every evening after dinner.',
                'memory_tip': 'Simple "DOES" - what someone "does" or performs, the action they carry out.'
            },
            'doesn': {
                'definition': 'Contraction of "does not"; indicates the negative form of the third person singular present tense of "do."',
                'part_of_speech': 'verb (contraction)',
                'pronunciation_guide': 'DUHZ-unt (emphasis on first syllable)',
                'etymology': 'Contraction of "does" + "not." Standard English negative formation.',
                'language_origins': 'English',
                'example_sentence': 'He _____ understand why the meeting was cancelled.',
                'memory_tip': 'Remember "DOESn\'t" - combines "does" + "not," showing someone "does" "not" do something.'
            },
            'dogana': {
                'definition': 'An Italian customhouse or customs office; a building where customs duties are collected on imported goods. Architectural and administrative term.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'doh-GAH-nah (emphasis on second syllable)',
                'etymology': 'From Italian "dogana" from Arabic "diwan" meaning "customs house." Trade and architectural terminology.',
                'language_origins': 'Italian from Arabic',
                'example_sentence': 'The historic _____ in Venice still stands as a reminder of the city\'s maritime trading past.',
                'memory_tip': 'Think "do-GANa" - where goods "go" through customs, the Italian customs house for trade.'
            },
            'dojo': {
                'definition': 'A hall or place for immersive learning or meditation, especially for martial arts training. A training facility for Japanese martial arts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOH-joh (emphasis on first syllable)',
                'etymology': 'From Japanese "dōjō" meaning "place of the way" (dō "way" + jō "place"). Martial arts terminology.',
                'language_origins': 'Japanese',
                'example_sentence': 'The karate students gathered at the _____ for their evening training session.',
                'memory_tip': 'Remember "DOH-jo" - a place where you "do" martial arts training, following "the way."'
            },
            'doldrums': {
                'definition': 'A state of inactivity or depression; a period of listlessness or despondency. Originally a nautical term for calm ocean areas near the equator.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOHL-drumz (emphasis on first syllable)',
                'etymology': 'Possibly from "dull" + archaic "drum" (meaning slow-moving). Nautical term that became general usage.',
                'language_origins': 'English (nautical)',
                'example_sentence': 'After the exciting vacation ended, she fell into the _____ of everyday routine.',
                'memory_tip': 'Think "DOLL-drums" - feeling so "dull" that even drums can\'t wake you up from your depressed state.'
            },
            'dollbill': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "dollbill" appears to be "doll" + "bill" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'dolma': {
                'definition': 'A traditional dish consisting of vegetables, typically grape leaves, stuffed with a mixture of rice, meat, and spices. Popular in Mediterranean and Middle Eastern cuisine.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOHL-mah (emphasis on first syllable)',
                'etymology': 'From Turkish "dolma" meaning "stuffed" (from dolmak "to fill"). Culinary terminology.',
                'language_origins': 'Turkish',
                'example_sentence': 'The restaurant served delicious grape leaf _____ as an appetizer.',
                'memory_tip': 'Remember "DOLL-ma" - like a "doll" stuffed with filling, dolma is vegetables stuffed with rice and meat.'
            },
            'dolmen': {
                'definition': 'A type of ancient stone monument consisting of large flat stones laid on upright ones; a prehistoric tomb structure. Archaeological terminology.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOHL-men (emphasis on first syllable)',
                'etymology': 'From Breton "taol" (table) + "men" (stone). Archaeological term for ancient stone structures.',
                'language_origins': 'Breton (Celtic)',
                'example_sentence': 'The ancient _____ in Ireland attracts many visitors interested in prehistoric culture.',
                'memory_tip': 'Think "DOLL-men" - ancient stone structures built by early people, like stone "dolls" marking important places.'
            },
            'dolphin': {
                'definition': 'A highly intelligent marine mammal with a streamlined body and a distinctive beak-like snout; known for playful behavior and echolocation abilities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOHL-fin (emphasis on first syllable)',
                'etymology': 'From Greek "delphis" meaning "dolphin." Via Latin "delphinus" and Old French "dauphin."',
                'language_origins': 'Greek via Latin and French',
                'example_sentence': 'The _____ leaped gracefully out of the water, delighting the tourists on the boat.',
                'memory_tip': 'Remember "DOLphin" - like a "doll" that can swim, these intelligent sea mammals are playful and friendly.'
            },
            'domain': {
                'definition': 'An area of territory controlled by a ruler; a sphere of activity or knowledge; an internet address. Can refer to land, expertise, or web addresses.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'doh-MAYN (emphasis on second syllable)',
                'etymology': 'From Latin "dominium" meaning "ownership" (from dominus "lord, master"). About ownership or control.',
                'language_origins': 'Latin',
                'example_sentence': 'Computer programming was definitely outside her _____ of expertise.',
                'memory_tip': 'Think "do-MAIN" - the "main" area where you "do" things, your territory or area of control.'
            },
            'dome': {
                'definition': 'A rounded vault forming the roof of a building; any rounded, elevated structure resembling this architectural feature.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DOHM (rhymes with "home")',
                'etymology': 'From Latin "domus" meaning "house." Originally referred to a house, later specifically to rounded roofs.',
                'language_origins': 'Latin',
                'example_sentence': 'The golden _____ of the capitol building gleamed in the afternoon sunlight.',
                'memory_tip': 'Simple "DOME" rhymes with "home" - a rounded roof that covers a building like a protective home.'
            },
            'domesticated': {
                'definition': 'Tamed and kept as a pet or farm animal; adapted to life in association with humans. Describes animals bred for human use.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'duh-MES-ti-kay-ted (emphasis on second syllable)',
                'etymology': 'From Latin "domesticus" meaning "of the household" + "-ated." About animals adapted to home life.',
                'language_origins': 'Latin',
                'example_sentence': 'Cats were first _____ by ancient Egyptians thousands of years ago.',
                'memory_tip': 'Remember "do-MESTicated" - animals that live in your "mest" (nest/home), tamed for domestic life.'
            },
            'domesticity': {
                'definition': 'The quality of being domestic; home life and family relationships; the state of being devoted to home and family activities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'doh-mes-TIS-i-tee (emphasis on third syllable)',
                'etymology': 'From "domestic" + "-ity" suffix. About the quality of home and family life.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'After years of travel, she began to appreciate the peaceful _____ of staying home.',
                'memory_tip': 'Think "do-MEST-icity" - the quality of being focused on your "nest" and home life.'
            },
            'domiciled': {
                'definition': 'Residing permanently in a particular place; having one\'s legal residence established somewhere. Legal term for official residence.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'DOM-uh-syld (emphasis on first syllable)',
                'etymology': 'From Latin "domicilium" meaning "dwelling place" (domus "house" + colere "to inhabit"). Legal terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'For tax purposes, he was officially _____ in Florida despite traveling frequently.',
                'memory_tip': 'Remember "DOMiciled" - your official "dome" (home) where you\'re legally residing.'
            },
            'domineering': {
                'definition': 'Asserting one\'s will over others in an arrogant way; overbearing and controlling in behavior toward others.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dom-uh-NEER-ing (emphasis on third syllable)',
                'etymology': 'From "domineer" (to rule arrogantly) + "-ing." From Latin "dominari" meaning "to rule, govern."',
                'language_origins': 'English from Latin',
                'example_sentence': 'Her _____ personality made it difficult for others to express their opinions in meetings.',
                'memory_tip': 'Think "dom-NEER-ing" - "dominating" people by being "near" them with controlling behavior.'
            },
            'domino': {
                'definition': 'A small rectangular block used in games, marked with dots; a masquerade costume with a half-mask; one of a series of events triggered by a single cause.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOM-uh-noh (emphasis on first syllable)',
                'etymology': 'From Latin "dominus" meaning "lord, master." Originally referred to a hooded robe, later to the game pieces.',
                'language_origins': 'Latin',
                'example_sentence': 'When the first _____ fell, it triggered a chain reaction that knocked down all the others.',
                'memory_tip': 'Remember "DOM-ino" - like "dominate," when one falls it dominates the others by knocking them down.'
            },
            'donatee': {
                'definition': 'A person who receives a donation; the recipient of a charitable gift or contribution. Legal and charitable terminology.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'doh-nuh-TEE (emphasis on third syllable)',
                'etymology': 'From "donate" + "-ee" suffix (indicating recipient). Formation parallel to "trustee" or "grantee."',
                'language_origins': 'English formation',
                'example_sentence': 'The charity carefully screened each _____ to ensure the donations reached those most in need.',
                'memory_tip': 'Think "don-a-TEE" - the "tee" (person) who receives what you "donate," the recipient of gifts.'
            },
            'done': {
                'definition': 'Completed or finished; cooked sufficiently; socially acceptable or proper. Past participle of "do," indicating completion.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'DUHN (rhymes with "sun")',
                'etymology': 'From Old English "dōn," past participle of "dōn" (to do). Basic English indicating completion.',
                'language_origins': 'Old English',
                'example_sentence': 'After three hours of studying, she was finally _____ with her homework.',
                'memory_tip': 'Simple "DONE" rhymes with "won" - when you\'ve finished something, you\'ve "won" by getting it done.'
            },
            'donkeys': {
                'definition': 'Plural of donkey; domesticated animals related to horses but smaller, with long ears and a reputation for stubbornness.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DONG-keez (emphasis on first syllable)',
                'etymology': 'Origin uncertain, possibly from "dun" (grayish-brown color) + diminutive suffix. Plural of common farm animal.',
                'language_origins': 'English (uncertain origin)',
                'example_sentence': 'The _____ carried heavy loads up the mountain trail with remarkable endurance.',
                'memory_tip': 'Remember "DONKkeys" - animals that make a "donk" sound and are sometimes stubborn like certain people.'
            },
            'donna': {
                'definition': 'An Italian title for a lady; a Spanish title for a woman of rank. Also used as a female given name.',
                'part_of_speech': 'noun (title/name)',
                'pronunciation_guide': 'DON-nah (emphasis on first syllable)',
                'etymology': 'From Italian/Spanish "donna" meaning "lady" (from Latin "domina" meaning "mistress, lady").',
                'language_origins': 'Italian/Spanish from Latin',
                'example_sentence': '_____ Maria was respected throughout the village for her wisdom and kindness.',
                'memory_tip': 'Think "DON-na" - like "don" (Spanish title for men), "donna" is the title for ladies in Italian and Spanish.'
            },
            'donut': {
                'definition': 'A small, ring-shaped cake made of sweet dough and fried in fat; alternative spelling of "doughnut." Popular breakfast pastry.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOH-nut (emphasis on first syllable)',
                'etymology': 'Simplified spelling of "doughnut" (dough + nut). American English variant of the traditional spelling.',
                'language_origins': 'English (American variant)',
                'example_sentence': 'She grabbed a glazed _____ and coffee for breakfast on her way to work.',
                'memory_tip': 'Simple "DOnut" - "dough" shaped like a nut (ring), but spelled shorter and simpler.'
            },
            'donuts': {
                'definition': 'Plural of donut; multiple ring-shaped fried cakes made from sweet dough. Popular breakfast pastries often sold by the dozen.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOH-nuts (emphasis on first syllable)',
                'etymology': 'Plural of "donut," simplified spelling of "doughnuts." American English variant.',
                'language_origins': 'English (American variant)',
                'example_sentence': 'The office meeting included a box of assorted _____ for everyone to share.',
                'memory_tip': 'Remember "DONuts" - multiple pieces of "dough" shaped like "nuts" (rings), sweet breakfast treats.'
            }
        }
        
        return batch_053_data.get(word.lower(), {})
    
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
    processor = Batch053Processor()
    success = processor.process_csv("batch_053_words.csv", "batch_053_processed.csv")
    
    if success:
        print("Batch 053 processing completed successfully!")
    else:
        print("Batch 053 processing failed!")

if __name__ == "__main__":
    main()