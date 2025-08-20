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
        
        high_freq = ['edge', 'edible', 'edition', 'editorial', 'educational', 'effect', 'efficient', 'eight', 'eighth', 'either', 'elderly', 'electric', 'electrical', 'electrified', 'elegant']
        medium_freq = ['edinburgh', 'eerily', 'efface', 'effortless', 'eggplant', 'eggs', 'egyptian', 'einstein', 'electrode']
        
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
        prefixes = ['ed-', 'ef-', 'eg-', 'el-']
        suffixes = ['-ic', '-ed', '-ly', '-ing', '-tion', '-al', '-ive', '-ent', '-ary']
        
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
        elif any(word_lower.startswith(prefix) for prefix in ['ed', 'ef', 'eg', 'el']):
            return 5
        else:
            return 3

class Batch057Processor:
    def __init__(self):
        self.base_path = "/c/Users/jessi/Projects/skilltree2/scripts/spelling_bee"
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive data using Claude's knowledge"""
        
        batch_057_data = {
            'edenic': {
                'definition': 'Relating to or resembling the Garden of Eden; characterized by idyllic beauty, innocence, and perfection; paradisiacal.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'eh-DEN-ik (emphasis on second syllable)',
                'etymology': 'From "Eden" (the biblical garden) + "-ic" suffix. Religious and literary terminology.',
                'language_origins': 'Hebrew via English',
                'example_sentence': 'The tropical island had an _____ quality that made visitors feel like they had found paradise.',
                'memory_tip': 'Remember "e-DEN-ic" - relating to the "Eden" garden, perfectly beautiful and innocent like paradise.'
            },
            'edge': {
                'definition': 'The outside limit of an object, area, or surface; a slight advantage; the sharpened side of a blade.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'EJ (rhymes with "hedge")',
                'etymology': 'From Old English "ecg" meaning "corner, point." Related to Germanic words for sharp points.',
                'language_origins': 'Old English',
                'example_sentence': 'She carefully walked along the _____ of the cliff to get a better view.',
                'memory_tip': 'Simple "EDGE" rhymes with "hedge" - the sharp boundary or border of something.'
            },
            'edible': {
                'definition': 'Safe and suitable for eating; fit to be consumed as food without harm.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ED-uh-bul (emphasis on first syllable)',
                'etymology': 'From Latin "edibilis" meaning "eatable" (from edere "to eat"). Food terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The survival guide taught hikers to identify _____ plants in the wilderness.',
                'memory_tip': 'Remember "ED-ible" - something you can "eat" without getting sick, safely "edible."'
            },
            'edification': {
                'definition': 'The instruction or improvement of a person morally or intellectually; education that enlightens and uplifts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ed-uh-fi-KAY-shun (emphasis on fourth syllable)',
                'etymology': 'From Latin "aedificare" meaning "to build" (aedes "building" + facere "to make"). About building character.',
                'language_origins': 'Latin',
                'example_sentence': 'She read philosophy books for her moral and intellectual _____.',
                'memory_tip': 'Think "edifi-CATION" - "edifying" education that builds character like constructing a building.'
            },
            'edinburgh': {
                'definition': 'The capital city of Scotland, known for its historic castle, annual festivals, and cultural significance.',
                'part_of_speech': 'noun (proper)',
                'pronunciation_guide': 'ED-in-bur-uh (emphasis on first syllable)',
                'etymology': 'From Old English "Edwin\'s burh" (Edwin\'s fortress). Named after King Edwin of Northumbria.',
                'language_origins': 'Old English',
                'example_sentence': 'The annual _____ Festival attracts performers and audiences from around the world.',
                'memory_tip': 'Remember "EDIN-burgh" - like "eating burg," the Scottish capital city with its famous castle.'
            },
            'edition': {
                'definition': 'A particular version of a published text; one of a series of printings of the same book or publication.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-DISH-un (emphasis on second syllable)',
                'etymology': 'From Latin "editio" meaning "a bringing forth" (from edere "to give out"). Publishing terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The first _____ of the novel is now a valuable collector\'s item.',
                'memory_tip': 'Think "e-DITION" - a specific "addition" or version of a book that\'s been "edited" and published.'
            },
            'editorial': {
                'definition': 'An article expressing the opinion of the newspaper\'s editors; relating to editing or editors.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'ed-ih-TOR-ee-ul (emphasis on third syllable)',
                'etymology': 'From "editor" + "-ial" suffix. Journalism and publishing terminology.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'The newspaper\'s _____ strongly criticized the mayor\'s new policy.',
                'memory_tip': 'Remember "edi-TOR-ial" - an article written by the "editor" expressing the newspaper\'s opinions.'
            },
            'educand': {
                'definition': 'A person who is being educated; a student or learner receiving instruction.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ED-yoo-kand (emphasis on first syllable)',
                'etymology': 'From Latin "educandus" meaning "to be educated" (from educare "to educate"). Educational terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The teacher adapted her methods to meet the needs of each _____.',
                'memory_tip': 'Think "EDU-cand" - a "candidate" for "education," someone being taught and educated.'
            },
            'educational': {
                'definition': 'Relating to education; providing knowledge or teaching; designed to educate or inform.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ed-yoo-KAY-shun-ul (emphasis on third syllable)',
                'etymology': 'From "education" + "-al" suffix. About the process of teaching and learning.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'The museum offers many _____ programs for children and adults.',
                'memory_tip': 'Remember "edu-CATION-al" - relating to "education" and learning, designed to teach.'
            },
            'edwardian': {
                'definition': 'Relating to the reign of King Edward VII of Britain (1901-1910); characteristic of this period\'s style and culture.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ed-WOR-dee-an (emphasis on second syllable)',
                'etymology': 'From "Edward" + "-ian" suffix. Historical period terminology.',
                'language_origins': 'English (eponym)',
                'example_sentence': 'The house was decorated in elegant _____ style with period furniture.',
                'memory_tip': 'Remember "Ed-WARD-ian" - relating to King "Edward\'s" era, the period after Victorian times.'
            },
            'eerily': {
                'definition': 'In an eerie manner; mysteriously or strangely; in a way that causes unease or fear.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'EER-uh-lee (emphasis on first syllable)',
                'etymology': 'From "eerie" (possibly from Old English "earg" meaning "cowardly") + "-ly" suffix.',
                'language_origins': 'Old English',
                'example_sentence': 'The old house was _____ quiet, with no sounds except the wind.',
                'memory_tip': 'Remember "EERIE-ly" - doing things in an "eerie" (spooky) way that makes you feel uncomfortable.'
            },
            'efface': {
                'definition': 'To erase or remove completely; to make oneself appear unimportant or inconspicuous.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ih-FAYS (emphasis on second syllable)',
                'etymology': 'From French "effacer" meaning "to erase" (ex- "out" + face "face"). About removing or erasing.',
                'language_origins': 'French from Latin',
                'example_sentence': 'Time had begun to _____ the old inscription on the gravestone.',
                'memory_tip': 'Think "ef-FACE" - to erase the "face" or surface of something, making it disappear completely.'
            },
            'effect': {
                'definition': 'A result or consequence; something brought about by a cause; to bring about or cause.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'ih-FEKT (emphasis on second syllable)',
                'etymology': 'From Latin "effectus" meaning "accomplishment" (ex- "out" + facere "to make"). About results.',
                'language_origins': 'Latin',
                'example_sentence': 'The new medicine had a positive _____ on the patient\'s condition.',
                'memory_tip': 'Remember "ef-FECT" - the result or "fact" that comes after a cause, what happens as a consequence.'
            },
            'effectual': {
                'definition': 'Successful in producing a desired or intended result; effective and efficient.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-FEK-choo-ul (emphasis on second syllable)',
                'etymology': 'From "effect" + "-ual" suffix. About being successful in achieving results.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'The new treatment proved _____ in reducing the symptoms.',
                'memory_tip': 'Think "ef-FECT-ual" - actually producing the intended "effect," successful and effective.'
            },
            'effervescent': {
                'definition': 'Vivacious and enthusiastic; giving off bubbles; lively and exuberant in manner.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ef-er-VES-ent (emphasis on third syllable)',
                'etymology': 'From Latin "effervescere" meaning "to boil up" (ex- "out" + fervere "to boil"). About bubbling energy.',
                'language_origins': 'Latin',
                'example_sentence': 'Her _____ personality made her the life of every party.',
                'memory_tip': 'Remember "effer-VESCE-nt" - bubbling with energy like soda that fizzes, lively and enthusiastic.'
            },
            'effete': {
                'definition': 'Weak and ineffective; lacking vigor or strength; exhausted or worn out.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-FEET (emphasis on second syllable)',
                'etymology': 'From Latin "effetus" meaning "worn out by bearing" (ex- "out" + fetus "offspring"). About exhaustion.',
                'language_origins': 'Latin',
                'example_sentence': 'The once-powerful empire had become _____ and unable to defend itself.',
                'memory_tip': 'Think "ef-FETE" - so worn out that even your "feet" are tired, weak and ineffective.'
            },
            'efficient': {
                'definition': 'Working in a well-organized way; achieving maximum productivity with minimum wasted effort or expense.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-FISH-ent (emphasis on second syllable)',
                'etymology': 'From Latin "efficientem" meaning "working out, accomplishing" (ex- "out" + facere "to make").',
                'language_origins': 'Latin',
                'example_sentence': 'The new software made the office workflow much more _____.',
                'memory_tip': 'Remember "ef-FICI-ent" - like being "proficient," working effectively without wasting time or energy.'
            },
            'effigy': {
                'definition': 'A sculpture or model of a person, especially one created to be damaged or destroyed in protest.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EF-ih-jee (emphasis on first syllable)',
                'etymology': 'From Latin "effigies" meaning "image, likeness" (ex- "out" + fingere "to shape"). About shaped images.',
                'language_origins': 'Latin',
                'example_sentence': 'The protesters burned an _____ of the unpopular politician.',
                'memory_tip': 'Think "EF-figy" - a figure shaped "out of" materials to represent someone, often for protest.'
            },
            'effleurage': {
                'definition': 'A massage technique involving long, gliding strokes with the palms and fingers; gentle, flowing massage movements.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'ef-lur-AHZH (emphasis on third syllable)',
                'etymology': 'From French "effleurer" meaning "to skim, touch lightly" (ex- "out" + fleur "flower"). Massage terminology.',
                'language_origins': 'French',
                'example_sentence': 'The massage therapist began with gentle _____ to relax the client\'s muscles.',
                'memory_tip': 'Remember "ef-fleur-AGE" - like "flower" (fleur) movements, gentle gliding strokes in massage.'
            },
            'efflux': {
                'definition': 'The action of flowing out; something that flows out; an outflow or discharge.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EF-luks (emphasis on first syllable)',
                'etymology': 'From Latin "effluxus" meaning "a flowing out" (ex- "out" + fluere "to flow"). About outward flow.',
                'language_origins': 'Latin',
                'example_sentence': 'The _____ of water from the dam created a powerful downstream current.',
                'memory_tip': 'Think "EF-flux" - like "flux" (flow) going "ef" (out), water or substances flowing outward.'
            },
            'effluxfrugivore': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "effluxfrugivore" appears to be "efflux" + "frugivore" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'effortless': {
                'definition': 'Requiring no physical or mental exertion; achieved with ease; appearing natural and unforced.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'EF-ert-lis (emphasis on first syllable)',
                'etymology': 'From "effort" + "-less" suffix. About doing things without strain or difficulty.',
                'language_origins': 'English formation',
                'example_sentence': 'The professional dancer made the complex routine look _____.',
                'memory_tip': 'Simple "EFFORT-less" - without "effort," doing things easily and naturally without strain.'
            },
            'effortlesseighth': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "effortlesseighth" appears to be "effortless" + "eighth" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'effraction': {
                'definition': 'The act of breaking open or through; forcible entry or breaking, especially in legal contexts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-FRAK-shun (emphasis on second syllable)',
                'etymology': 'From Latin "effractio" meaning "a breaking open" (ex- "out" + frangere "to break"). Legal terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The burglar was charged with _____ for breaking into the building.',
                'memory_tip': 'Remember "ef-FRAC-tion" - like "fracture," forcibly breaking open or through something.'
            },
            'effrontery': {
                'definition': 'Insolent or impertinent behavior; shameless audacity or boldness.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-FRUN-ter-ee (emphasis on second syllable)',
                'etymology': 'From French "effronterie" from "effronté" meaning "shameless" (ex- "out" + frons "forehead").',
                'language_origins': 'French from Latin',
                'example_sentence': 'She had the _____ to ask for a raise after being late every day.',
                'memory_tip': 'Think "ef-FRONT-ery" - showing your "front" (forehead) shamelessly, bold and impudent behavior.'
            },
            'effusive': {
                'definition': 'Expressing feelings of gratitude, pleasure, or approval in an unrestrained way; gushing and enthusiastic.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-FYOO-siv (emphasis on second syllable)',
                'etymology': 'From Latin "effusus" meaning "poured out" (ex- "out" + fundere "to pour"). About pouring out emotions.',
                'language_origins': 'Latin',
                'example_sentence': 'Her _____ praise made the young artist feel very appreciated.',
                'memory_tip': 'Remember "ef-FUSIVE" - emotions "fusing" and pouring out excessively, gushing with enthusiasm.'
            },
            'effusiveprimitive': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "effusiveprimitive" appears to be "effusive" + "primitive" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'egeria': {
                'definition': 'A female advisor or counselor; a woman who guides or influences someone in authority. From Roman mythology.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'eh-JEER-ee-ah (emphasis on second syllable)',
                'etymology': 'From Latin "Egeria," a Roman nymph who advised King Numa. Mythological and political terminology.',
                'language_origins': 'Latin (mythological)',
                'example_sentence': 'The queen\'s trusted _____ provided wise counsel during the political crisis.',
                'memory_tip': 'Remember "e-GEER-ia" - like a female "gear" that helps guide and advise those in power.'
            },
            'eggcorn': {
                'definition': 'A misheard or misunderstood phrase that is substituted with words that sound similar but change the meaning.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EG-korn (emphasis on first syllable)',
                'etymology': 'From "acorn" misheard as "eggcorn." Linguistic terminology coined by linguist Geoffrey Pullum.',
                'language_origins': 'English (modern linguistic term)',
                'example_sentence': 'Saying "for all intensive purposes" instead of "for all intents and purposes" is an _____.',
                'memory_tip': 'Remember "EGG-corn" - like confusing an "acorn" with an "eggcorn," mishearing words that sound similar.'
            },
            'eggplant': {
                'definition': 'A purple, egg-shaped vegetable; also called aubergine; used in cooking worldwide, especially Mediterranean cuisine.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EG-plant (emphasis on first syllable)',
                'etymology': 'From "egg" + "plant." Originally white varieties resembled large eggs.',
                'language_origins': 'English',
                'example_sentence': 'She grilled sliced _____ with olive oil and herbs for dinner.',
                'memory_tip': 'Simple "EGG-plant" - a purple vegetable that originally looked like a large white egg on a plant.'
            },
            'eggs': {
                'definition': 'Plural of egg; oval reproductive bodies laid by female birds, reptiles, and some other animals; used as food.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EGZ (rhymes with "legs")',
                'etymology': 'From Old English "æg," plural of "egg." Basic food and biological terminology.',
                'language_origins': 'Old English',
                'example_sentence': 'She scrambled three _____ for breakfast this morning.',
                'memory_tip': 'Simple "EGGS" rhymes with "legs" - oval-shaped reproductive bodies that chickens lay.'
            },
            'egress': {
                'definition': 'The action of going out or leaving; an exit or way out of a place.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'EE-gres (emphasis on first syllable)',
                'etymology': 'From Latin "egressus" meaning "a going out" (ex- "out" + gradi "to step"). Architectural terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The fire code requires clear _____ routes in all public buildings.',
                'memory_tip': 'Think "E-GRESS" - to "exit" and "go" out, the opposite of "ingress" (going in).'
            },
            'egressgeocaching': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "egressgeocaching" appears to be "egress" + "geocaching" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'egucigalpa': {
                'definition': 'The capital and most populous city of Honduras, located in central Honduras.',
                'part_of_speech': 'noun (proper)',
                'pronunciation_guide': 'teh-goo-see-GAL-pah (emphasis on fourth syllable)',
                'etymology': 'From indigenous Lenca language, possibly meaning "silver hills." Geographic proper noun.',
                'language_origins': 'Indigenous Lenca',
                'example_sentence': '_____ serves as the political and economic center of Honduras.',
                'memory_tip': 'Remember "Tegu-ci-GAL-pa" - the capital city of Honduras with a complex indigenous name.'
            },
            'egyptian': {
                'definition': 'Relating to Egypt or its people; a native or inhabitant of Egypt; characteristic of ancient or modern Egypt.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ih-JIP-shun (emphasis on second syllable)',
                'etymology': 'From "Egypt" + "-ian" suffix. Geographic and cultural terminology.',
                'language_origins': 'English from Greek',
                'example_sentence': 'The museum displayed ancient _____ artifacts including mummies and hieroglyphics.',
                'memory_tip': 'Remember "e-GYP-tian" - relating to "Egypt," the land of pyramids and pharaohs.'
            },
            'eight': {
                'definition': 'The number 8; one more than seven and one less than nine; a numeral representing this quantity.',
                'part_of_speech': 'number, noun',
                'pronunciation_guide': 'AYT (rhymes with "late")',
                'etymology': 'From Old English "eahta" related to Germanic and Indo-European words for eight.',
                'language_origins': 'Old English',
                'example_sentence': 'She counted _____ apples in the basket.',
                'memory_tip': 'Simple "EIGHT" rhymes with "late" - the number that comes after seven, written as 8.'
            },
            'eighth': {
                'definition': 'The ordinal number corresponding to eight; one of eight equal parts; position number 8 in a sequence.',
                'part_of_speech': 'ordinal number, noun',
                'pronunciation_guide': 'AYTH (rhymes with "faith")',
                'etymology': 'From "eight" + "-th" ordinal suffix. Ordinal number formation.',
                'language_origins': 'English',
                'example_sentence': 'She finished in _____ place in the running competition.',
                'memory_tip': 'Remember "EIGHTH" rhymes with "faith" - the ordinal form of eight, 8th in order.'
            },
            'einstein': {
                'definition': 'Albert Einstein (1879-1955), German-born theoretical physicist famous for the theory of relativity; used to refer to a very intelligent person.',
                'part_of_speech': 'noun (proper)',
                'pronunciation_guide': 'EYE-n-styne (emphasis on first syllable)',
                'etymology': 'German surname meaning "one stone." Scientific and cultural eponym.',
                'language_origins': 'German',
                'example_sentence': 'The physics student admired _____ for his groundbreaking theories about space and time.',
                'memory_tip': 'Remember "EYE-n-stein" - the brilliant physicist whose name means "one stone" but whose ideas were revolutionary.'
            },
            'eisteddfod': {
                'definition': 'A Welsh festival of literature, music, and performance; a competitive cultural event celebrating Welsh arts and language.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'eye-STETH-vod (emphasis on second syllable)',
                'etymology': 'From Welsh "eisteddfod" meaning "session" (eistedd "to sit" + bod "to be"). Cultural terminology.',
                'language_origins': 'Welsh',
                'example_sentence': 'The annual _____ featured competitions in poetry, singing, and traditional Welsh music.',
                'memory_tip': 'Think "eye-STEAD-fod" - a Welsh cultural "festival" where people "sit" to watch performances.'
            },
            'either': {
                'definition': 'One or the other of two; used to indicate a choice between two alternatives; each of two.',
                'part_of_speech': 'determiner, pronoun, adverb',
                'pronunciation_guide': 'EE-ther or EYE-ther (both pronunciations acceptable)',
                'etymology': 'From Old English "ægther" meaning "each of two." Basic English determiner.',
                'language_origins': 'Old English',
                'example_sentence': 'You can choose _____ the red shirt or the blue one.',
                'memory_tip': 'Remember "EITHER" - like "each there," indicating one choice or the other of two options.'
            },
            'elaborative': {
                'definition': 'Involving or characterized by elaboration; providing additional detail or development; expansive and detailed.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-LAB-uh-ray-tiv (emphasis on second syllable)',
                'etymology': 'From "elaborate" + "-ive" suffix. About working out details thoroughly.',
                'language_origins': 'English formation from Latin roots',
                'example_sentence': 'The professor used an _____ teaching method that included many examples and details.',
                'memory_tip': 'Remember "e-LAB-orative" - like working in a "lab," carefully developing and elaborating on details.'
            },
            'elasticity': {
                'definition': 'The ability to stretch and return to original shape; flexibility and adaptability; resilience under pressure.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-las-TIS-ih-tee (emphasis on third syllable)',
                'etymology': 'From "elastic" + "-ity" suffix. Physics and general terminology about flexibility.',
                'language_origins': 'English formation from Greek roots',
                'example_sentence': 'Rubber bands demonstrate the principle of _____ by stretching and snapping back.',
                'memory_tip': 'Think "e-las-TIC-ity" - the quality of being "elastic," able to stretch like a rubber band.'
            },
            'elderly': {
                'definition': 'Old in years; advanced in age; relating to or designed for older people.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'EL-der-lee (emphasis on first syllable)',
                'etymology': 'From "elder" + "-ly" suffix. About advanced age and seniority.',
                'language_origins': 'English',
                'example_sentence': 'The community center offers special programs for _____ residents.',
                'memory_tip': 'Simple "ELDER-ly" - like an "elder," someone who is older and advanced in years.'
            },
            'elderlyamigo': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "elderlyamigo" appears to be "elderly" + "amigo" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'electric': {
                'definition': 'Relating to or powered by electricity; exciting or thrilling; having a sudden energizing effect.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-LEK-trik (emphasis on second syllable)',
                'etymology': 'From Greek "elektron" meaning "amber" (which produces static electricity when rubbed). Scientific terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'The _____ guitar produced a much louder sound than the acoustic version.',
                'memory_tip': 'Remember "e-LEK-tric" - powered by "electrons," the force that makes lights and machines work.'
            },
            'electrical': {
                'definition': 'Relating to electricity; concerned with the generation and application of electricity.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-LEK-tri-kul (emphasis on second syllable)',
                'etymology': 'From "electric" + "-al" suffix. Engineering and technical terminology.',
                'language_origins': 'English formation from Greek roots',
                'example_sentence': 'The _____ engineer designed the wiring system for the new building.',
                'memory_tip': 'Think "e-LEK-trical" - the technical field dealing with "electric" power and systems.'
            },
            'electrified': {
                'definition': 'Charged with electricity; supplied with electric power; excited or thrilled.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'ih-LEK-truh-fyed (emphasis on second syllable)',
                'etymology': 'From "electrify" + "-ed" suffix. About charging with electricity or excitement.',
                'language_origins': 'English formation from Greek roots',
                'example_sentence': 'The audience was _____ by the performer\'s amazing guitar solo.',
                'memory_tip': 'Remember "e-LEK-trified" - charged up with "electric" power or excitement, energized.'
            },
            'electrode': {
                'definition': 'A conductor through which electricity enters or leaves an object, substance, or region.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-LEK-trohd (emphasis on second syllable)',
                'etymology': 'From "electro-" (electric) + Greek "hodos" (way, path). Scientific terminology.',
                'language_origins': 'English from Greek',
                'example_sentence': 'The battery has a positive and negative _____ for conducting electric current.',
                'memory_tip': 'Think "ELECTRO-de" - the "electric" "ode" (path) where electricity travels into or out of something.'
            },
            'eleemosynary': {
                'definition': 'Relating to or supported by charity; charitable and philanthropic; given or done out of compassion.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'el-ee-MOS-uh-nair-ee (emphasis on third syllable)',
                'etymology': 'From Greek "eleemosyne" meaning "alms, charity" (eleos "mercy" + syn "with"). Charitable terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'The hospital was founded as an _____ institution to serve the poor.',
                'memory_tip': 'Remember "elee-MOS-ynary" - relating to "alms" and charity, helping those in need with mercy.'
            },
            'elegant': {
                'definition': 'Graceful and stylish in appearance or manner; pleasingly ingenious and simple; refined and tasteful.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'EL-ih-gant (emphasis on first syllable)',
                'etymology': 'From Latin "elegans" meaning "choice, fine" (from eligere "to choose"). About refined choice.',
                'language_origins': 'Latin',
                'example_sentence': 'She wore an _____ black dress to the formal dinner.',
                'memory_tip': 'Remember "ELE-gant" - so refined and graceful it\'s like an "elegant" choice, tasteful and stylish.'
            }
        }
        
        return batch_057_data.get(word.lower(), {})
    
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
    processor = Batch057Processor()
    success = processor.process_csv("batch_057_words.csv", "batch_057_processed.csv")
    
    if success:
        print("Batch 057 processing completed successfully!")
    else:
        print("Batch 057 processing failed!")

if __name__ == "__main__":
    main()