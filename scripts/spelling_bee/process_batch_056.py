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
        
        high_freq = ['early', 'eagerly', 'eagle', 'earth', 'earthquake', 'ease', 'easily', 'east', 'eastern', 'eaten', 'eats', 'economic', 'economy']
        medium_freq = ['earmark', 'earnestly', 'ears', 'eavesdrop', 'echoed', 'eclipse', 'ecstatic', 'eddy']
        
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
        prefixes = ['dys-', 'dé-', 'e-', 'ec-', 'ect-']
        suffixes = ['-ed', '-ly', '-ing', '-ic', '-ia', '-ism', '-tion']
        
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
        elif any(word_lower.startswith(prefix) for prefix in ['dys', 'ec', 'ect']):
            return 6
        else:
            return 3

class Batch056Processor:
    def __init__(self):
        self.base_path = "/c/Users/jessi/Projects/skilltree2/scripts/spelling_bee"
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive data using Claude's knowledge"""
        
        batch_056_data = {
            'dwindled': {
                'definition': 'Past tense of dwindle; gradually decreased in size, amount, or strength; became smaller or fewer over time. Indicates a steady decline or reduction.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'DWIN-duhld (emphasis on first syllable)',
                'etymology': 'From "dwindle" (frequentative of "dwine" meaning "to waste away") + "-ed" suffix. About gradual decrease.',
                'language_origins': 'English',
                'example_sentence': 'The crowd _____ as the evening grew later and people went home.',
                'memory_tip': 'Remember "DWIN-dled" - things "dwindle" down until they become small, like a "twin" that shrinks.'
            },
            'dynamite': {
                'definition': 'A high explosive made from nitroglycerin; something or someone having a powerful effect; excellent or outstanding.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'DIE-nuh-mite (emphasis on first syllable)',
                'etymology': 'From Greek "dynamis" meaning "power" + suffix "-ite." Coined by Alfred Nobel for his explosive invention.',
                'language_origins': 'Greek',
                'example_sentence': 'The construction crew used _____ to blast through the solid rock.',
                'memory_tip': 'Think "DIE-na-mite" - explosive with so much "dynamic" power it can make rocks "die" and break apart.'
            },
            'dynasty': {
                'definition': 'A sequence of rulers from the same family; a powerful group or family that maintains control for generations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIE-nuh-stee (emphasis on first syllable)',
                'etymology': 'From Greek "dynasteia" meaning "lordship, dominion" (from dynastes "ruler"). Political terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'The Ming _____ ruled China for nearly three centuries.',
                'memory_tip': 'Remember "DIE-nasty" - when a ruling family "dies," the dynasty ends, passing power through generations.'
            },
            'dysgraphia': {
                'definition': 'A learning disability that affects writing abilities; difficulty with spelling, handwriting, and organizing thoughts on paper.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dis-GRAF-ee-ah (emphasis on second syllable)',
                'etymology': 'From Greek "dys-" (bad) + "graphia" (writing). Medical terminology for writing disorders.',
                'language_origins': 'Greek',
                'example_sentence': 'The student\'s _____ made it challenging to complete written assignments despite good verbal skills.',
                'memory_tip': 'Think "dys-GRAPH-ia" - "dys" (bad) "graph" (writing), difficulty with writing and spelling.'
            },
            'dyspeptic': {
                'definition': 'Suffering from or relating to indigestion; bad-tempered or irritable, especially due to stomach problems.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dis-PEP-tik (emphasis on second syllable)',
                'etymology': 'From Greek "dyspeptos" meaning "hard to digest" (dys- "bad" + peptos "digested"). Medical terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'His _____ mood was probably due to eating too much spicy food.',
                'memory_tip': 'Remember "dys-PEP-tic" - "dys" (bad) "peptic" (digestion), causing irritable mood from stomach troubles.'
            },
            'dysphasia': {
                'definition': 'Difficulty with speech and language caused by brain damage; partial loss of ability to understand or express speech.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dis-FAY-zhuh (emphasis on second syllable)',
                'etymology': 'From Greek "dys-" (bad) + "phasis" (speech). Medical terminology for speech disorders.',
                'language_origins': 'Greek',
                'example_sentence': 'After the stroke, she experienced _____ and needed speech therapy.',
                'memory_tip': 'Think "dys-PHASIA" - "dys" (bad) speech "phases," difficulty with language and speaking.'
            },
            'dysphasiae': {
                'definition': 'Plural of dysphasia; multiple cases or types of speech and language difficulties caused by brain damage.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dis-FAY-zhee-ee (emphasis on second syllable)',
                'etymology': 'From "dysphasia" + Latin plural "-ae." Medical terminology for multiple speech disorders.',
                'language_origins': 'Greek with Latin plural',
                'example_sentence': 'The neurologist studied various _____ to understand different speech disorder patterns.',
                'memory_tip': 'Remember "dys-PHAS-iae" - plural of dysphasia, multiple speech difficulties with the Latin "-ae" ending.'
            },
            'dysrhythmia': {
                'definition': 'An abnormal heart rhythm; irregular heartbeat that deviates from the normal pattern of cardiac contractions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dis-RITH-mee-ah (emphasis on second syllable)',
                'etymology': 'From Greek "dys-" (bad) + "rhythmos" (rhythm). Medical terminology for heart rhythm disorders.',
                'language_origins': 'Greek',
                'example_sentence': 'The cardiologist detected a _____ during the patient\'s routine examination.',
                'memory_tip': 'Think "dys-RHYTHM-ia" - "dys" (bad) "rhythm," when the heart doesn\'t beat in proper rhythm.'
            },
            'dystopia': {
                'definition': 'An imagined society where everything is unpleasant or bad; the opposite of utopia, characterized by suffering and oppression.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dis-TOH-pee-ah (emphasis on second syllable)',
                'etymology': 'From Greek "dys-" (bad) + "topos" (place). Literary and political terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'The novel depicted a _____ where individual freedom had been completely eliminated.',
                'memory_tip': 'Remember "dys-TOPIA" - "dys" (bad) place, the opposite of "utopia," a terrible society.'
            },
            'dystopiae': {
                'definition': 'Plural of dystopia; multiple imagined societies characterized by suffering, oppression, and unpleasant conditions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dis-TOH-pee-ee (emphasis on second syllable)',
                'etymology': 'From "dystopia" + Latin plural "-ae." Literary terminology for multiple bad societies.',
                'language_origins': 'Greek with Latin plural',
                'example_sentence': 'Science fiction literature often explores various _____ to warn about potential futures.',
                'memory_tip': 'Think "dys-TOP-iae" - plural of dystopia, multiple bad "topias" (places) with Latin "-ae" ending.'
            },
            'déjà': {
                'definition': 'Part of "déjà vu," meaning "already" in French; the feeling of having experienced something before.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'day-ZHAH (emphasis on second syllable)',
                'etymology': 'From French "déjà" meaning "already." Part of psychological terminology.',
                'language_origins': 'French',
                'example_sentence': 'She experienced a strong sense of _____ vu when visiting the old house.',
                'memory_tip': 'Remember "day-ZHAH" - French word meaning "already," like you\'ve "already" been in this "day."'
            },
            'démodé': {
                'definition': 'Out of fashion; no longer fashionable or stylish; outdated or passé.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'day-moh-DAY (emphasis on third syllable)',
                'etymology': 'From French "démodé" meaning "out of fashion" (dé- "un-" + mode "fashion"). Fashion terminology.',
                'language_origins': 'French',
                'example_sentence': 'Her grandmother\'s clothing style was considered _____ by modern standards.',
                'memory_tip': 'Think "day-mo-DAY" - fashion from "yesterday" that\'s no longer the "mode" (style) of today.'
            },
            'déné': {
                'definition': 'Referring to the Dené people, indigenous peoples of northern Canada; also called Athapaskan or Athabascan peoples.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'day-NAY (emphasis on second syllable)',
                'etymology': 'From Dené language meaning "the people." Indigenous terminology.',
                'language_origins': 'Dené (Indigenous North American)',
                'example_sentence': 'The _____ communities have lived in the northern territories for thousands of years.',
                'memory_tip': 'Remember "day-NAY" - the indigenous people who say "nay" to being called by other names, preferring "Dené."'
            },
            'eagerly': {
                'definition': 'With keen interest or enthusiasm; in an eager manner, showing excitement or impatience for something.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'EE-ger-lee (emphasis on first syllable)',
                'etymology': 'From "eager" (from Old French "aigre" meaning "keen") + "-ly" suffix.',
                'language_origins': 'Old French',
                'example_sentence': 'The children _____ awaited the arrival of the ice cream truck.',
                'memory_tip': 'Remember "EAGER-ly" - doing things with an "eager" attitude, full of enthusiasm and excitement.'
            },
            'eagle': {
                'definition': 'A large bird of prey with keen eyesight and powerful flight; a symbol of strength and freedom in many cultures.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EE-gul (emphasis on first syllable)',
                'etymology': 'From Old English "earn" related to Germanic words for eagle. Bird terminology.',
                'language_origins': 'Old English',
                'example_sentence': 'The bald _____ soared majestically above the mountain lake.',
                'memory_tip': 'Simple "EAGLE" - a powerful bird with "eager" eyes that can see prey from great distances.'
            },
            'early': {
                'definition': 'Before the usual or expected time; happening or done before others; in the first part of a period.',
                'part_of_speech': 'adjective, adverb',
                'pronunciation_guide': 'UR-lee (emphasis on first syllable)',
                'etymology': 'From Old English "ærlice" (from "ær" meaning "before" + "-lice" suffix).',
                'language_origins': 'Old English',
                'example_sentence': 'She always arrived _____ to meetings to make a good impression.',
                'memory_tip': 'Remember "EAR-ly" - happening before your "ear" expects to hear the alarm clock.'
            },
            'earmark': {
                'definition': 'To designate funds for a particular purpose; a distinctive mark on an animal\'s ear; to set aside for a specific use.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'EER-mark (emphasis on first syllable)',
                'etymology': 'From "ear" + "mark." Originally about marking animal ears, later extended to designating funds.',
                'language_origins': 'English',
                'example_sentence': 'The government decided to _____ the funds specifically for education improvements.',
                'memory_tip': 'Think "EAR-mark" - like putting a "mark" on an animal\'s "ear," you mark money for specific purposes.'
            },
            'earnestly': {
                'definition': 'In a serious and sincere manner; with genuine feeling or commitment; showing deep conviction.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'UR-nest-lee (emphasis on first syllable)',
                'etymology': 'From "earnest" (from Old English "eornost" meaning "serious") + "-ly" suffix.',
                'language_origins': 'Old English',
                'example_sentence': 'She spoke _____ about the importance of environmental conservation.',
                'memory_tip': 'Remember "EARNEST-ly" - doing things with an "earnest" (serious) attitude, genuinely caring.'
            },
            'ears': {
                'definition': 'Plural of ear; the organs of hearing; the ability to perceive or appreciate sounds, especially music.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EERZ (rhymes with "years")',
                'etymology': 'From Old English "eare," plural of "ear." Basic anatomical terminology.',
                'language_origins': 'Old English',
                'example_sentence': 'The loud music hurt her _____ at the concert.',
                'memory_tip': 'Simple "EARS" rhymes with "years" - the body parts that help you hear for many years.'
            },
            'earth': {
                'definition': 'The planet we live on; soil or ground; the world as opposed to heaven or space.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'URTH (rhymes with "worth")',
                'etymology': 'From Old English "eorþe" related to Germanic words for ground and soil.',
                'language_origins': 'Old English',
                'example_sentence': 'Astronauts could see the whole _____ from their spacecraft.',
                'memory_tip': 'Remember "EARTH" rhymes with "worth" - our planet is worth protecting and caring for.'
            },
            'earthquake': {
                'definition': 'A sudden violent shaking of the ground caused by movement of the earth\'s crust; a major upheaval or disturbance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'URTH-kwayk (emphasis on first syllable)',
                'etymology': 'From "earth" + "quake" (shake). Geological terminology for seismic events.',
                'language_origins': 'English',
                'example_sentence': 'The _____ measured 7.2 on the Richter scale and caused significant damage.',
                'memory_tip': 'Simple "EARTH-quake" - when the "earth" "quakes" (shakes) violently from underground movement.'
            },
            'ease': {
                'definition': 'Absence of difficulty or effort; comfort and lack of pain; to make less difficult or troublesome.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'EEZE (rhymes with "breeze")',
                'etymology': 'From Old French "aise" meaning "comfort, pleasure." About lack of difficulty.',
                'language_origins': 'Old French',
                'example_sentence': 'The new software was designed with _____ of use in mind.',
                'memory_tip': 'Remember "EASE" rhymes with "breeze" - both are gentle and make things feel comfortable and easy.'
            },
            'easily': {
                'definition': 'Without difficulty or effort; in a relaxed and comfortable manner; by far or without doubt.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'EE-zuh-lee (emphasis on first syllable)',
                'etymology': 'From "easy" + "-ly" suffix. About doing things without difficulty.',
                'language_origins': 'English formation',
                'example_sentence': 'She could _____ solve the math problems that stumped her classmates.',
                'memory_tip': 'Remember "EASY-ly" - doing things in an "easy" manner, without struggle or effort.'
            },
            'east': {
                'definition': 'The direction toward the sunrise; one of the four cardinal compass directions; the eastern part of a region.',
                'part_of_speech': 'noun, adjective, adverb',
                'pronunciation_guide': 'EEST (rhymes with "feast")',
                'etymology': 'From Old English "ēast" related to Germanic words for dawn and sunrise.',
                'language_origins': 'Old English',
                'example_sentence': 'The sun rises in the _____ and sets in the west.',
                'memory_tip': 'Remember "EAST" rhymes with "feast" - where the sun brings the "feast" of daylight each morning.'
            },
            'eastern': {
                'definition': 'Located in or relating to the east; coming from the east; characteristic of eastern regions or cultures.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'EE-stern (emphasis on first syllable)',
                'etymology': 'From "east" + "-ern" suffix. Directional and regional terminology.',
                'language_origins': 'English',
                'example_sentence': 'The _____ coast of the United States faces the Atlantic Ocean.',
                'memory_tip': 'Think "EAST-ern" - the "-ern" suffix shows direction, things relating to the "east" side.'
            },
            'eaten': {
                'definition': 'Past participle of eat; consumed as food; devoured or destroyed by something.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'EE-ten (emphasis on first syllable)',
                'etymology': 'From Old English "etan" past participle "eaten." Basic verb for consuming food.',
                'language_origins': 'Old English',
                'example_sentence': 'All the cookies had been _____ before the guests arrived.',
                'memory_tip': 'Remember "EAT-en" - the past participle of "eat," showing something was consumed in the past.'
            },
            'eats': {
                'definition': 'Third person singular of eat; consumes food; informal term for food itself.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'EETS (rhymes with "beats")',
                'etymology': 'From "eat" + third person singular "-s." Basic verb for consuming food.',
                'language_origins': 'English',
                'example_sentence': 'She _____ breakfast at seven o\'clock every morning.',
                'memory_tip': 'Simple "EATS" - what someone does when they consume food, or slang for food itself.'
            },
            'eavesdrop': {
                'definition': 'To secretly listen to a private conversation; to overhear without the speakers\' knowledge.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'EEVZ-drop (emphasis on first syllable)',
                'etymology': 'From "eaves" (roof edge) + "drop." Originally about listening from under the eaves of a house.',
                'language_origins': 'English',
                'example_sentence': 'It\'s rude to _____ on other people\'s private conversations.',
                'memory_tip': 'Think "EAVES-drop" - secretly listening by standing under the "eaves" where conversations "drop" down.'
            },
            'ebullience': {
                'definition': 'Cheerful and full of energy; the quality of being enthusiastic and vivacious; exuberant high spirits.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-BUL-yens (emphasis on second syllable)',
                'etymology': 'From Latin "ebullire" meaning "to bubble up" (e- "out" + bullire "to boil"). About bubbling enthusiasm.',
                'language_origins': 'Latin',
                'example_sentence': 'Her _____ was contagious, making everyone around her feel more cheerful.',
                'memory_tip': 'Think "e-BULL-ience" - enthusiasm that "bubbles" up like boiling water, full of energetic spirit.'
            },
            'eburnean': {
                'definition': 'Made of or resembling ivory; having the color or texture of ivory; white and smooth like elephant tusks.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'eh-BUR-nee-an (emphasis on second syllable)',
                'etymology': 'From Latin "eburneus" meaning "of ivory" (from ebur "ivory"). Descriptive terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The statue\'s _____ surface gleamed like polished ivory.',
                'memory_tip': 'Remember "e-BURN-ean" - like ivory that doesn\'t "burn," smooth and white like elephant tusks.'
            },
            'ecchymosis': {
                'definition': 'A medical term for bruising; discoloration of the skin due to bleeding underneath from damaged blood vessels.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ek-ih-MOH-sis (emphasis on third syllable)',
                'etymology': 'From Greek "ekchymosis" meaning "extravasation of blood" (ek- "out" + chymos "juice"). Medical terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'The doctor noted extensive _____ around the injury site.',
                'memory_tip': 'Think "ek-chy-MOSIS" - "ek" (out) blood that creates "osis" (condition) of bruising under skin.'
            },
            'ecclesiology': {
                'definition': 'The study of churches, their architecture, decoration, and furnishings; theological study of the Christian church.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'eh-klee-zee-OL-uh-jee (emphasis on fourth syllable)',
                'etymology': 'From Greek "ekklesia" (church) + "logos" (study). Religious and architectural terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'Her doctorate in _____ focused on medieval cathedral construction techniques.',
                'memory_tip': 'Remember "eccles-iology" - the "ology" (study) of "ecclesia" (churches) and their design.'
            },
            'echelon': {
                'definition': 'A level or rank in an organization or society; a formation of troops or vehicles in parallel rows.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ESH-uh-lon (emphasis on first syllable)',
                'etymology': 'From French "échelon" meaning "rung of a ladder" (from échelle "ladder"). Military and organizational terminology.',
                'language_origins': 'French',
                'example_sentence': 'She worked her way up to the highest _____ of corporate management.',
                'memory_tip': 'Think "ECHE-lon" - like "echo" levels, different ranks that echo up the organizational ladder.'
            },
            'echidna': {
                'definition': 'A spiny egg-laying mammal native to Australia and New Guinea; also called a spiny anteater.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-KID-nah (emphasis on second syllable)',
                'etymology': 'From Greek "echidna" meaning "viper" (named for its spines). Zoological terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'The _____ is one of only two types of mammals that lay eggs.',
                'memory_tip': 'Remember "e-CHID-na" - sounds like "e-KID-na," a unique mammal "kid" that\'s spiny like a porcupine.'
            },
            'echinoderm': {
                'definition': 'A marine animal with a hard, spiny skin, such as a starfish, sea urchin, or sea cucumber.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-KYE-noh-durm (emphasis on second syllable)',
                'etymology': 'From Greek "echinos" (sea urchin, hedgehog) + "derma" (skin). Zoological terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'The tide pool contained several _____ species, including starfish and sea urchins.',
                'memory_tip': 'Think "echino-DERM" - sea animals with "spiny" (echino) "skin" (derm) like sea urchins.'
            },
            'echoed': {
                'definition': 'Past tense of echo; repeated or reflected sound; imitated or repeated someone else\'s words or actions.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'EK-ohd (emphasis on first syllable)',
                'etymology': 'From "echo" (from Greek "ēchō") + "-ed" suffix. About sound reflection and repetition.',
                'language_origins': 'Greek',
                'example_sentence': 'Her words _____ through the empty hallway.',
                'memory_tip': 'Remember "ECHO-ed" - sounds that bounced back like an "echo," repeated in the past.'
            },
            'eclectic': {
                'definition': 'Selecting ideas, styles, or tastes from various sources; not following one particular style but choosing from many.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ih-KLEK-tik (emphasis on second syllable)',
                'etymology': 'From Greek "eklektikos" meaning "selective" (from eklegein "to select out"). About choosing from variety.',
                'language_origins': 'Greek',
                'example_sentence': 'Her _____ music collection included everything from classical to hip-hop.',
                'memory_tip': 'Think "e-CLEK-tic" - like "electric" variety, choosing and collecting from many different sources.'
            },
            'eclipse': {
                'definition': 'An astronomical event where one celestial body obscures another; to overshadow or surpass something.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'ih-KLIPS (emphasis on second syllable)',
                'etymology': 'From Greek "ekleipsis" meaning "abandonment, failing" (ek- "out" + leipein "to leave"). Astronomical terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'The solar _____ darkened the sky for several minutes.',
                'memory_tip': 'Remember "e-CLIPS" - when the moon "clips" the sun\'s light, creating an eclipse.'
            },
            'economic': {
                'definition': 'Relating to economics or the economy; financially profitable or cost-effective; concerned with material wealth.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ee-kuh-NOM-ik (emphasis on third syllable)',
                'etymology': 'From Greek "oikonomikos" meaning "of household management" (oikos "house" + nomos "law").',
                'language_origins': 'Greek',
                'example_sentence': 'The government implemented new _____ policies to stimulate growth.',
                'memory_tip': 'Think "eco-NOMIC" - relating to the "eco" (economy) and its "nomic" (laws/management).'
            },
            'economy': {
                'definition': 'The system of trade and industry by which the wealth of a country is made and used; careful management of resources.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-KON-uh-mee (emphasis on second syllable)',
                'etymology': 'From Greek "oikonomia" meaning "household management" (oikos "house" + nemein "to manage").',
                'language_origins': 'Greek',
                'example_sentence': 'The country\'s _____ grew stronger after the trade agreement.',
                'memory_tip': 'Remember "e-CON-omy" - the "con" (management) of money and resources in a region or country.'
            },
            'ecotourism': {
                'definition': 'Tourism directed toward natural environments to support conservation efforts and observe wildlife responsibly.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EE-koh-toor-izm (emphasis on first syllable)',
                'etymology': 'From "eco-" (ecological) + "tourism." Modern term for environmentally conscious travel.',
                'language_origins': 'English (modern formation)',
                'example_sentence': 'The national park promotes _____ to protect endangered species while educating visitors.',
                'memory_tip': 'Simple "ECO-tourism" - "eco" (environmental) "tourism" that protects nature while traveling.'
            },
            'ecstatic': {
                'definition': 'Feeling or expressing overwhelming happiness or joyful excitement; in a state of ecstasy.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ik-STAT-ik (emphasis on second syllable)',
                'etymology': 'From Greek "ekstatikos" meaning "causing to stand outside oneself" (ek- "out" + stasis "standing").',
                'language_origins': 'Greek',
                'example_sentence': 'She was _____ when she learned she had won the scholarship.',
                'memory_tip': 'Think "ek-STAT-ic" - so happy you\'re "statically" charged with joy, "ecstatic" with excitement.'
            },
            'ecstaticcinnamon': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "ecstaticcinnamon" appears to be "ecstatic" + "cinnamon" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'ection': {
                'definition': 'A suffix meaning "the action or process of"; appears in words like "selection," "protection," "infection."',
                'part_of_speech': 'suffix',
                'pronunciation_guide': 'EK-shun',
                'etymology': 'From Latin "-ectio" meaning "action, process." Grammatical suffix for forming nouns.',
                'language_origins': 'Latin',
                'example_sentence': 'The suffix _____ turns verbs into nouns showing the action or process.',
                'memory_tip': 'Remember "ECtion" - a suffix that shows "action" in words like "selection" and "protection."'
            },
            'ectoplasm': {
                'definition': 'In spiritualism, a supernatural substance supposedly exuded by mediums; in biology, the outer layer of cell cytoplasm.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EK-toh-plazm (emphasis on first syllable)',
                'etymology': 'From Greek "ektos" (outside) + "plasma" (something formed). Spiritual and biological terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'The medium claimed to produce _____ during the séance.',
                'memory_tip': 'Think "ECTO-plasm" - "ecto" (outside) "plasm" (substance), mysterious matter from outside the body.'
            },
            'ectoplasmolfactory': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "ectoplasmolfactory" appears to be "ectoplasm" + "olfactory" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'ecuador': {
                'definition': 'A country in South America, located on the equator between Colombia and Peru; named for its position on the equator.',
                'part_of_speech': 'noun (proper)',
                'pronunciation_guide': 'EK-wah-dor (emphasis on first syllable)',
                'etymology': 'From Spanish "Ecuador" meaning "equator." Geographic proper noun.',
                'language_origins': 'Spanish',
                'example_sentence': 'The Galápagos Islands belong to _____ and are famous for their unique wildlife.',
                'memory_tip': 'Remember "EQUAdor" - the country named for the "equator" line that runs through it.'
            },
            'eczema': {
                'definition': 'A skin condition causing itchy, inflamed patches; atopic dermatitis characterized by dry, red, and irritated skin.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EK-zuh-mah (emphasis on first syllable)',
                'etymology': 'From Greek "ekzema" meaning "to boil over" (ek- "out" + zein "to boil"). Medical terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'The dermatologist prescribed a cream to treat her _____.',
                'memory_tip': 'Think "EK-zema" - skin that looks like it\'s "seeping" or irritated, red and inflamed patches.'
            },
            'edamame': {
                'definition': 'Young soybeans served in the pod, typically boiled and salted; a popular Japanese appetizer and healthy snack.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'eh-dah-MAH-may (emphasis on third syllable)',
                'etymology': 'From Japanese "edamame" meaning "branch bean" (eda "branch" + mame "bean"). Culinary terminology.',
                'language_origins': 'Japanese',
                'example_sentence': 'The sushi restaurant served complimentary _____ while we waited for our order.',
                'memory_tip': 'Remember "eh-da-MAH-me" - Japanese beans you eat by saying "eh, da!" as you pop them in your mouth.'
            },
            'eddy': {
                'definition': 'A circular movement of fluid, counter to the main current; a small whirlpool or whirlwind.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'ED-ee (emphasis on first syllable)',
                'etymology': 'From Old Norse "iða" meaning "whirlpool." About circular water or air movement.',
                'language_origins': 'Old Norse',
                'example_sentence': 'Leaves swirled in the small _____ beside the creek.',
                'memory_tip': 'Simple "EDDY" - water that goes "eddy" (around in circles) instead of straight flow.'
            }
        }
        
        return batch_056_data.get(word.lower(), {})
    
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
    processor = Batch056Processor()
    success = processor.process_csv("batch_056_words.csv", "batch_056_processed.csv")
    
    if success:
        print("Batch 056 processing completed successfully!")
    else:
        print("Batch 056 processing failed!")

if __name__ == "__main__":
    main()