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
        
        high_freq = ['element', 'elevator', 'eliminate', 'else', 'emails', 'embassy', 'emblem', 'embrace', 'emerge', 'emergence', 'emotional', 'emperor', 'emphatic']
        medium_freq = ['elongated', 'elusive', 'elves', 'embers', 'embossed', 'embryo', 'emerald', 'emigrate', 'eminent', 'emitting']
        
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
        prefixes = ['el-', 'em-', 'en-']
        suffixes = ['-ic', '-ed', '-ing', '-tion', '-al', '-ive', '-ent', '-ary', '-ment']
        
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
        elif any(word_lower.startswith(prefix) for prefix in ['el', 'em']):
            return 5
        else:
            return 3

class Batch058Processor:
    def __init__(self):
        self.base_path = "/c/Users/jessi/Projects/skilltree2/scripts/spelling_bee"
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive data using Claude's knowledge"""
        
        batch_058_data = {
            'elegiac': {
                'definition': 'Relating to or having the style of an elegy; expressing sorrow or lamentation; mournful and melancholic in tone.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'el-uh-JYE-ak (emphasis on third syllable)',
                'etymology': 'From Greek "elegeia" meaning "song of mourning" + "-ac" suffix. Literary terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'The poet\'s _____ verses captured the profound sadness of loss.',
                'memory_tip': 'Remember "ele-GY-ac" - relating to an "elegy," a sad poem, "elegiac" poetry mourns and laments.'
            },
            'element': {
                'definition': 'A basic chemical substance; a fundamental component or part; one of the basic principles of a subject.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EL-uh-ment (emphasis on first syllable)',
                'etymology': 'From Latin "elementum" meaning "first principles." Scientific and general terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'Hydrogen is the simplest _____ on the periodic table.',
                'memory_tip': 'Remember "ELE-ment" - the "elementary" building blocks of chemistry and other subjects.'
            },
            'elevator': {
                'definition': 'A moving platform in a shaft for carrying people or goods between floors; something that raises or lifts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EL-uh-vay-ter (emphasis on first syllable)',
                'etymology': 'From "elevate" + "-or" suffix. About lifting or raising up.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'The office building\'s _____ broke down, forcing everyone to use the stairs.',
                'memory_tip': 'Simple "ELE-vator" - a machine that "elevates" people up and down between floors.'
            },
            'elicitation': {
                'definition': 'The action of drawing out or bringing forth information, responses, or reactions; the process of obtaining something.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-lis-ih-TAY-shun (emphasis on fourth syllable)',
                'etymology': 'From Latin "elicere" meaning "to draw out" (e- "out" + lacere "to entice") + "-ation."',
                'language_origins': 'Latin',
                'example_sentence': 'The teacher\'s skillful _____ of student responses led to a productive discussion.',
                'memory_tip': 'Think "e-licit-ATION" - the process of making something "licit" (legal) to come out, drawing forth responses.'
            },
            'eligibility': {
                'definition': 'The state of having the right to something; qualification or suitability for a particular purpose or benefit.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'el-ih-jih-BIL-ih-tee (emphasis on fourth syllable)',
                'etymology': 'From "eligible" (from Latin "eligere" meaning "to choose") + "-ity" suffix.',
                'language_origins': 'Latin',
                'example_sentence': 'Her _____ for the scholarship was based on both academic merit and financial need.',
                'memory_tip': 'Remember "eli-gi-BIL-ity" - the ability to be "eligible," qualified to be chosen for something.'
            },
            'eliminate': {
                'definition': 'To completely remove or get rid of something; to exclude from consideration; to kill or destroy.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ih-LIM-uh-nayt (emphasis on second syllable)',
                'etymology': 'From Latin "eliminare" meaning "to turn out of doors" (e- "out" + limen "threshold").',
                'language_origins': 'Latin',
                'example_sentence': 'The new software will _____ the need for manual data entry.',
                'memory_tip': 'Think "e-LIMinate" - to push something past the "limit" and out the door, completely removing it.'
            },
            'elision': {
                'definition': 'The omission of sounds or syllables in speech; the leaving out of part of a word or phrase.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-LIZH-un (emphasis on second syllable)',
                'etymology': 'From Latin "elidere" meaning "to strike out" (e- "out" + laedere "to strike").',
                'language_origins': 'Latin',
                'example_sentence': 'The contraction "can\'t" is an example of _____ in English.',
                'memory_tip': 'Remember "e-LI-sion" - like "collision," sounds crash together and some parts get struck out.'
            },
            'ellipse': {
                'definition': 'An oval shape; a closed curve that is stretched in one direction; a geometric figure with two focal points.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-LIPS (emphasis on second syllable)',
                'etymology': 'From Greek "elleipsis" meaning "a falling short" (from elleipein "to fall short").',
                'language_origins': 'Greek',
                'example_sentence': 'The planet\'s orbit around the sun follows an _____ rather than a perfect circle.',
                'memory_tip': 'Think "e-LLIPSE" - like "lips" in an oval shape, an elongated circle that\'s stretched.'
            },
            'elocution': {
                'definition': 'The skill of clear and expressive speech; the art of effective public speaking and pronunciation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'el-uh-KYOO-shun (emphasis on third syllable)',
                'etymology': 'From Latin "elocutio" meaning "manner of speaking" (e- "out" + loqui "to speak").',
                'language_origins': 'Latin',
                'example_sentence': 'The actor studied _____ to improve her stage presence and vocal delivery.',
                'memory_tip': 'Remember "elo-CU-tion" - like "execution" of clear speech, the art of speaking "out" effectively.'
            },
            'elongated': {
                'definition': 'Made longer or extended in length; stretched out; having unusual length in proportion to width.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'ih-LONG-gay-ted (emphasis on second syllable)',
                'etymology': 'From "elongate" (from Latin "elongare" meaning "to extend") + "-ed" suffix.',
                'language_origins': 'Latin',
                'example_sentence': 'The artist painted an _____ figure that appeared to stretch toward the ceiling.',
                'memory_tip': 'Simple "e-LONG-ated" - made to be "long," stretched out and extended in length.'
            },
            'else': {
                'definition': 'In addition; besides; otherwise; if not; used to indicate an alternative.',
                'part_of_speech': 'adverb, adjective',
                'pronunciation_guide': 'ELS (rhymes with "bells")',
                'etymology': 'From Old English "elles" meaning "otherwise." Basic English adverb.',
                'language_origins': 'Old English',
                'example_sentence': 'We need to hurry, or _____ we\'ll miss the train.',
                'memory_tip': 'Simple "ELSE" rhymes with "bells" - when you hear the bells, choose something else or otherwise.'
            },
            'eluate': {
                'definition': 'The liquid that results from elution; a solution obtained by washing or extracting material from a substance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EL-yoo-ayt (emphasis on first syllable)',
                'etymology': 'From "elute" (from Latin "eluere" meaning "to wash out") + "-ate" suffix.',
                'language_origins': 'Latin',
                'example_sentence': 'The chemist collected the _____ after washing the sample through the column.',
                'memory_tip': 'Think "ELU-ate" - the liquid that "eludes" from a substance when you wash it out.'
            },
            'eluateheterophony': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "eluateheterophony" appears to be "eluate" + "heterophony" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'elucidate': {
                'definition': 'To make something clear by explaining it more fully; to clarify or shed light on a subject.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ih-LOO-sih-dayt (emphasis on second syllable)',
                'etymology': 'From Latin "elucidare" meaning "to make light" (e- "out" + lucidus "clear, bright").',
                'language_origins': 'Latin',
                'example_sentence': 'The professor asked the student to _____ her answer with more specific examples.',
                'memory_tip': 'Remember "e-LUCI-date" - to make "lucid" (clear) by bringing light to dark subjects.'
            },
            'elusive': {
                'definition': 'Difficult to find, catch, or achieve; tending to evade grasp or pursuit; hard to define or describe.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-LOO-siv (emphasis on second syllable)',
                'etymology': 'From Latin "eludere" meaning "to escape" (e- "out" + ludere "to play") + "-ive."',
                'language_origins': 'Latin',
                'example_sentence': 'The solution to the puzzle remained _____ despite hours of effort.',
                'memory_tip': 'Think "e-LU-sive" - like playing "loose," something that slips away and evades capture.'
            },
            'elves': {
                'definition': 'Plural of elf; mythical creatures typically depicted as small, magical beings with pointed ears; folklore characters.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ELVZ (rhymes with "shelves")',
                'etymology': 'From Old English "ælf," plural "ylfe." Mythological terminology.',
                'language_origins': 'Old English',
                'example_sentence': 'The children\'s story featured helpful _____ who worked in Santa\'s workshop.',
                'memory_tip': 'Remember "ELVES" rhymes with "shelves" - magical beings who might help organize shelves in workshops.'
            },
            'emails': {
                'definition': 'Plural of email; electronic messages sent and received via computer networks; digital correspondence.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'EE-maylz (emphasis on first syllable)',
                'etymology': 'From "electronic mail." Modern technology terminology.',
                'language_origins': 'English (modern formation)',
                'example_sentence': 'She checked her _____ first thing every morning.',
                'memory_tip': 'Simple "E-mails" - "electronic" "mails," digital messages sent through computers.'
            },
            'emanant': {
                'definition': 'Flowing or issuing forth; emanating or proceeding from a source; originating from something.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'EM-uh-nant (emphasis on first syllable)',
                'etymology': 'From Latin "emanare" meaning "to flow out" (e- "out" + manare "to flow") + "-ant."',
                'language_origins': 'Latin',
                'example_sentence': 'The _____ light from the lighthouse guided ships safely to harbor.',
                'memory_tip': 'Think "EM-anant" - "emanating" outward, flowing "ant-like" in all directions from a source.'
            },
            'emancipatory': {
                'definition': 'Relating to or involving emancipation; serving to free from bondage, oppression, or restraint; liberating.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-MAN-sih-pah-tor-ee (emphasis on second syllable)',
                'etymology': 'From "emancipate" (from Latin "emancipare" meaning "to set free") + "-ory" suffix.',
                'language_origins': 'Latin',
                'example_sentence': 'The civil rights movement had a powerful _____ effect on society.',
                'memory_tip': 'Remember "e-MAN-cipatory" - freeing people from bondage, giving "man" (humanity) liberty and freedom.'
            },
            'embassy': {
                'definition': 'The official residence or offices of an ambassador; a diplomatic mission representing one country in another.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EM-buh-see (emphasis on first syllable)',
                'etymology': 'From Old French "ambassée" from "ambassadeur" (ambassador). Diplomatic terminology.',
                'language_origins': 'Old French',
                'example_sentence': 'American citizens abroad can seek help at their country\'s _____.',
                'memory_tip': 'Remember "EM-bassy" - where "ambassadors" work, representing their country in foreign lands.'
            },
            'embellishes': {
                'definition': 'Third person singular of embellish; decorates or adorns; adds attractive details; exaggerates for effect.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'em-BEL-ish-iz (emphasis on second syllable)',
                'etymology': 'From "embellish" (from Old French "embellir" meaning "to beautify") + "-es."',
                'language_origins': 'Old French',
                'example_sentence': 'The storyteller always _____ his tales with colorful details.',
                'memory_tip': 'Think "em-BELL-ishes" - like adding "bells" and decorations, making things more beautiful and ornate.'
            },
            'embers': {
                'definition': 'Small pieces of burning or glowing coal or wood in a dying fire; the remains of a fire.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EM-berz (emphasis on first syllable)',
                'etymology': 'From Old English "æmerge" meaning "ashes." About the remains of fire.',
                'language_origins': 'Old English',
                'example_sentence': 'The campers carefully extinguished the glowing _____ before leaving.',
                'memory_tip': 'Remember "EM-bers" - the "embers" that remain when fire "members" (pieces) cool down but still glow.'
            },
            'embezzlement': {
                'definition': 'The theft or misappropriation of funds by someone trusted with those assets; stealing money entrusted to one\'s care.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'em-BEZ-ul-ment (emphasis on second syllable)',
                'etymology': 'From "embezzle" (from Anglo-French "embesiler" meaning "to steal") + "-ment."',
                'language_origins': 'Anglo-French',
                'example_sentence': 'The accountant was charged with _____ for stealing company funds.',
                'memory_tip': 'Think "em-BEZZ-lement" - stealing money in a "busy" way from those who trusted you.'
            },
            'emblazoned': {
                'definition': 'Decorated conspicuously; displayed prominently; adorned with heraldic designs; made glorious or famous.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'em-BLAY-zund (emphasis on second syllable)',
                'etymology': 'From "emblazon" (from "en-" + "blazon" meaning "to proclaim") + "-ed."',
                'language_origins': 'English formation',
                'example_sentence': 'The knight\'s shield was _____ with his family crest.',
                'memory_tip': 'Remember "em-BLAZ-oned" - like "ablaze" with decorations, prominently decorated and displayed.'
            },
            'emblem': {
                'definition': 'A heraldic device or symbolic object as a distinctive badge; a symbol or representation of something.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EM-blum (emphasis on first syllable)',
                'etymology': 'From Greek "emblema" meaning "something inserted" (from emballein "to insert").',
                'language_origins': 'Greek',
                'example_sentence': 'The eagle serves as the national _____ of the United States.',
                'memory_tip': 'Think "EM-blem" - a symbol that\'s "embedded" to represent something important.'
            },
            'emboldened': {
                'definition': 'Made bold or courageous; given confidence to act; encouraged to take risks.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'em-BOHL-dund (emphasis on second syllable)',
                'etymology': 'From "embolden" (from "en-" + "bold") + "-ed." About giving courage.',
                'language_origins': 'English',
                'example_sentence': 'She felt _____ by her recent success to try an even bigger challenge.',
                'memory_tip': 'Simple "em-BOLD-ened" - made more "bold," given courage and confidence to act.'
            },
            'embolus': {
                'definition': 'A blood clot or other blockage that travels through the bloodstream and blocks a blood vessel.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EM-buh-lus (emphasis on first syllable)',
                'etymology': 'From Greek "embolos" meaning "wedge, stopper" (from emballein "to insert").',
                'language_origins': 'Greek',
                'example_sentence': 'The doctor explained that an _____ in the lung could be life-threatening.',
                'memory_tip': 'Remember "EM-bolus" - like a "bolt" that blocks blood flow, a clot that travels and plugs vessels.'
            },
            'embossed': {
                'definition': 'Decorated with a raised design; having a pattern that stands out from the surface.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'em-BOST (emphasis on second syllable)',
                'etymology': 'From "emboss" (from Old French "en-" + "boce" meaning "protuberance") + "-ed."',
                'language_origins': 'Old French',
                'example_sentence': 'The wedding invitation featured _____ gold lettering.',
                'memory_tip': 'Think "em-BOSS-ed" - like a "boss" standing out, raised up from the surface in relief.'
            },
            'embouchure': {
                'definition': 'The way in which the lips, tongue, and teeth are applied to the mouthpiece of a wind instrument.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AHM-boo-shur (emphasis on first syllable)',
                'etymology': 'From French "embouchure" from "emboucher" meaning "to put to the mouth" (en- + bouche "mouth").',
                'language_origins': 'French',
                'example_sentence': 'The trumpet student practiced proper _____ to improve her tone.',
                'memory_tip': 'Remember "em-BOU-chure" - the "bouche" (mouth) position for playing wind instruments.'
            },
            'embrace': {
                'definition': 'To hold closely in one\'s arms; to accept willingly; to include or encompass.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'em-BRAYS (emphasis on second syllable)',
                'etymology': 'From Old French "embracier" meaning "to clasp in the arms" (en- "in" + brace "arms").',
                'language_origins': 'Old French',
                'example_sentence': 'She decided to _____ the opportunity to study abroad.',
                'memory_tip': 'Remember "em-BRACE" - to "brace" someone with your arms, holding them close or accepting them.'
            },
            'embroglio': {
                'definition': 'A confused or complicated situation; a state of confusion or entanglement; a misunderstanding or quarrel.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'em-BROHL-yoh (emphasis on second syllable)',
                'etymology': 'From Italian "imbroglio" meaning "confusion, tangle" (from imbrogliare "to tangle").',
                'language_origins': 'Italian',
                'example_sentence': 'The diplomatic _____ took months to resolve peacefully.',
                'memory_tip': 'Think "em-BROG-lio" - like being in a "bog," stuck in a confusing, tangled situation.'
            },
            'embroidery': {
                'definition': 'The art of decorating fabric with needle and thread; ornamental needlework; elaborate decoration.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'em-BROY-der-ee (emphasis on second syllable)',
                'etymology': 'From "embroider" (from Anglo-French "embrouder") + "-y" suffix.',
                'language_origins': 'Anglo-French',
                'example_sentence': 'Her grandmother taught her the traditional art of _____.',
                'memory_tip': 'Remember "em-BROID-ery" - decorating fabric by "braiding" threads in beautiful patterns.'
            },
            'embroiled': {
                'definition': 'Involved in conflict or difficulty; entangled in a complicated or troublesome situation.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'em-BOYLD (emphasis on second syllable)',
                'etymology': 'From "embroil" (from French "embrouiller" meaning "to confuse") + "-ed."',
                'language_origins': 'French',
                'example_sentence': 'The company became _____ in a lengthy legal dispute.',
                'memory_tip': 'Think "em-BROIL-ed" - like being "broiled" in hot conflict, caught up in heated trouble.'
            },
            'embryo': {
                'definition': 'An unborn offspring in the early stages of development; the beginning or rudimentary stage of anything.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EM-bree-oh (emphasis on first syllable)',
                'etymology': 'From Greek "embryon" meaning "young one" (en- "in" + bryein "to swell").',
                'language_origins': 'Greek',
                'example_sentence': 'The scientist studied the development of the _____ under a microscope.',
                'memory_tip': 'Remember "EM-bryo" - the early "embryonic" stage when life begins to grow and develop.'
            },
            'emerald': {
                'definition': 'A bright green precious stone; a vivid green color; something prized for its beauty and rarity.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'EM-er-uld (emphasis on first syllable)',
                'etymology': 'From Old French "esmeraude" from Greek "smaragdos." Gemstone terminology.',
                'language_origins': 'Greek via Old French',
                'example_sentence': 'The ring featured a stunning _____ surrounded by diamonds.',
                'memory_tip': 'Think "EM-erald" - a green gem that "emerges" from the earth, beautiful and valuable.'
            },
            'emerge': {
                'definition': 'To come forth into view; to become apparent or prominent; to come into existence.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ih-MURJ (emphasis on second syllable)',
                'etymology': 'From Latin "emergere" meaning "to rise out" (e- "out" + mergere "to dip").',
                'language_origins': 'Latin',
                'example_sentence': 'New leaders began to _____ during the crisis.',
                'memory_tip': 'Remember "e-MERGE" - to come out of being "merged" or hidden, rising into view.'
            },
            'emergence': {
                'definition': 'The process of coming forth or becoming apparent; the act of emerging or coming into being.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-MUR-jens (emphasis on second syllable)',
                'etymology': 'From "emerge" + "-ence" suffix. About the process of coming forth.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'The _____ of new technology changed how people communicate.',
                'memory_tip': 'Think "e-MERG-ence" - the process of "emerging," coming into existence or view.'
            },
            'emeritus': {
                'definition': 'Retired but retaining an honorary title; having retired from active professional duty but maintaining rank.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-MER-ih-tus (emphasis on second syllable)',
                'etymology': 'From Latin "emeritus" meaning "having served one\'s time" (from emerere "to serve out").',
                'language_origins': 'Latin',
                'example_sentence': 'The professor _____ continued to conduct research after retirement.',
                'memory_tip': 'Remember "e-MER-itus" - someone who has "earned merit" through service and now has honorary status.'
            },
            'emigrate': {
                'definition': 'To leave one\'s own country to settle permanently in another; to move away from one\'s homeland.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'EM-ih-grayt (emphasis on first syllable)',
                'etymology': 'From Latin "emigrare" meaning "to move away" (e- "out" + migrare "to move").',
                'language_origins': 'Latin',
                'example_sentence': 'Many families decided to _____ to America for better opportunities.',
                'memory_tip': 'Remember "EM-igrate" - to "exit" and "migrate" away from your home country to a new land.'
            },
            'eminent': {
                'definition': 'Famous and respected within a particular sphere; standing out above others; prominent and distinguished.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'EM-ih-nent (emphasis on first syllable)',
                'etymology': 'From Latin "eminere" meaning "to stand out" (e- "out" + minere "to project").',
                'language_origins': 'Latin',
                'example_sentence': 'The _____ scientist won the Nobel Prize for her groundbreaking research.',
                'memory_tip': 'Think "EM-inent" - so outstanding that your reputation "emanates" and stands out prominently.'
            },
            'eminentdemographics': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "eminentdemographics" appears to be "eminent" + "demographics" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'emissary': {
                'definition': 'A person sent on a special mission as a representative; an agent or messenger sent to represent others.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EM-ih-sair-ee (emphasis on first syllable)',
                'etymology': 'From Latin "emissarius" meaning "scout" (from emittere "to send out").',
                'language_origins': 'Latin',
                'example_sentence': 'The king sent an _____ to negotiate peace with the neighboring country.',
                'memory_tip': 'Remember "EM-issary" - someone "emitted" or sent out on a mission to represent others.'
            },
            'emitting': {
                'definition': 'Present participle of emit; giving off or releasing something, especially energy, light, or sound.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ih-MIT-ing (emphasis on second syllable)',
                'etymology': 'From "emit" (from Latin "emittere" meaning "to send out") + "-ing."',
                'language_origins': 'Latin',
                'example_sentence': 'The radioactive material was _____ dangerous levels of radiation.',
                'memory_tip': 'Remember "e-MITT-ing" - "mitt" (sending) something out, releasing or giving off energy.'
            },
            'emollient': {
                'definition': 'Having the quality of softening or soothing the skin; a substance that softens and moisturizes.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ih-MOL-yent (emphasis on second syllable)',
                'etymology': 'From Latin "emollire" meaning "to soften" (e- "out" + mollire "to soften").',
                'language_origins': 'Latin',
                'example_sentence': 'The doctor recommended an _____ cream for her dry skin condition.',
                'memory_tip': 'Think "e-MOLL-ient" - something that makes skin "mellow" and soft, soothing and moisturizing.'
            },
            'emolument': {
                'definition': 'A salary, fee, or profit from employment or office; compensation received for work or services.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-MOL-yuh-ment (emphasis on second syllable)',
                'etymology': 'From Latin "emolumentum" meaning "profit, gain" (from emolere "to grind out").',
                'language_origins': 'Latin',
                'example_sentence': 'The Constitution prohibits federal officials from receiving foreign _____.',
                'memory_tip': 'Remember "e-MOL-ument" - payment that you "mold" or work for, compensation earned through effort.'
            },
            'emotional': {
                'definition': 'Relating to emotions; arousing or characterized by intense feelings; involving the emotions rather than reason.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-MOH-shun-ul (emphasis on second syllable)',
                'etymology': 'From "emotion" (from Latin "emotio" meaning "a moving out") + "-al."',
                'language_origins': 'Latin',
                'example_sentence': 'The graduation ceremony was an _____ moment for the entire family.',
                'memory_tip': 'Simple "e-MOTION-al" - relating to "emotions" and feelings, stirring the heart.'
            },
            'emotionsword': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "emotionsword" appears to be "emotions" + "sword" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'empennage': {
                'definition': 'The tail assembly of an aircraft, including the rudder and elevators; the rear part of an airplane.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AHM-pen-ij (emphasis on first syllable)',
                'etymology': 'From French "empennage" from "empenner" meaning "to feather an arrow" (en- + penne "feather").',
                'language_origins': 'French',
                'example_sentence': 'The aircraft\'s _____ was damaged during the emergency landing.',
                'memory_tip': 'Remember "em-PENN-age" - like "pen" feathers on an arrow, the tail feathers of an airplane.'
            },
            'emperor': {
                'definition': 'The male ruler of an empire; a sovereign of the highest rank; a large butterfly or penguin species.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EM-per-er (emphasis on first syllable)',
                'etymology': 'From Latin "imperator" meaning "commander" (from imperare "to command").',
                'language_origins': 'Latin',
                'example_sentence': 'Napoleon crowned himself _____ of France in 1804.',
                'memory_tip': 'Remember "EMP-eror" - the "empire" ruler, someone with imperial power and authority.'
            },
            'emphatic': {
                'definition': 'Expressed with emphasis; forceful and clear in expression; definite and unmistakable.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'em-FAT-ik (emphasis on second syllable)',
                'etymology': 'From Greek "emphatikos" meaning "expressive" (from emphasis "significance").',
                'language_origins': 'Greek',
                'example_sentence': 'She gave an _____ "no" when asked if she would work overtime.',
                'memory_tip': 'Remember "em-PHAT-ic" - so forceful it\'s "fat" with emphasis, strong and unmistakable.'
            }
        }
        
        return batch_058_data.get(word.lower(), {})
    
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
    processor = Batch058Processor()
    success = processor.process_csv("batch_058_words.csv", "batch_058_processed.csv")
    
    if success:
        print("Batch 058 processing completed successfully!")
    else:
        print("Batch 058 processing failed!")

if __name__ == "__main__":
    main()