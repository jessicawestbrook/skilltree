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
        
        high_freq = ['different', 'difficult', 'difficulty', 'digital', 'direct', 'directly', 'dinner', 'dictionary', 'dimension', 'dice']
        medium_freq = ['disaster', 'dilemma', 'diaspora', 'diastole', 'diploma', 'dinosaur', 'diligence', 'dire', 'diocese']
        
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
        prefixes = ['di-', 'dis-', 'dia-']
        suffixes = ['-ism', '-tion', '-tic', '-ous', '-ent', '-ary', '-ity', '-ed', '-ing', '-er', '-ly']
        
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
        elif any(word_lower.startswith(prefix) for prefix in ['di', 'dia', 'dis']):
            return 5
        else:
            return 3

class Batch051Processor:
    def __init__(self):
        self.base_path = "/c/Users/jessi/Projects/skilltree2/scripts/spelling_bee"
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive data using Claude's knowledge"""
        
        batch_051_data = {
            'diaspora': {
                'definition': 'The dispersion or spread of a people from their original homeland. Originally referred to the Jewish communities scattered outside of Israel, but now broadly describes any ethnic or cultural population living outside their traditional homeland. The term encompasses both forced displacement and voluntary migration, along with the ongoing cultural and social connections maintained between dispersed communities and their homeland.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'die-ASS-poh-rah (emphasis on second syllable)',
                'etymology': 'From Greek "diaspeirein" meaning "to scatter" (dia- "across" + speirein "to sow"). First used in the Septuagint (Greek translation of Hebrew Bible) to describe Jewish communities outside Palestine.',
                'language_origins': 'Greek',
                'example_sentence': 'The Irish _____ spread throughout the world during the 19th century famine, establishing communities that maintained strong cultural ties to their homeland.',
                'memory_tip': 'Remember "die-ASS-poh-rah" - think of people "dying to scatter" from their homeland, spreading like seeds ("spore" sound) across the earth.'
            },
            'diastole': {
                'definition': 'The phase of the cardiac cycle during which the heart muscle relaxes and the chambers fill with blood. This is the lower number in blood pressure readings, representing the pressure in arteries when the heart is at rest between beats. Diastole is crucial for coronary artery filling and proper heart function.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'die-ASS-toh-lee (emphasis on second syllable)',
                'etymology': 'From Greek "diastole" meaning "a drawing apart" (dia- "apart" + stellein "to place, arrange"). Medical term adopted in the 17th century.',
                'language_origins': 'Greek',
                'example_sentence': 'During _____, the heart chambers expand to fill with blood before the next contraction.',
                'memory_tip': 'Think "die-ASS-tole" - during this phase, the heart "takes a toll" to relax and fill with blood between beats.'
            },
            'diathermy': {
                'definition': 'A medical treatment using high-frequency electric current to generate deep heat within tissues. Commonly used for therapeutic purposes to relieve pain, reduce muscle spasms, and promote healing. Also employed in surgery for cutting tissues and controlling bleeding through controlled heat application.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIE-ah-ther-mee (emphasis on first syllable)',
                'etymology': 'From Greek "dia" (through) + "therme" (heat). Coined in early 20th century as medical technology developed.',
                'language_origins': 'Greek',
                'example_sentence': 'The physical therapist used _____ to apply deep heat therapy to the patient\'s injured muscle.',
                'memory_tip': 'Remember "DIE-athermy" - medical treatment that uses heat "through" (dia) the body for healing.'
            },
            'diatonic': {
                'definition': 'Relating to a musical scale consisting of seven different pitches within an octave, following the pattern of whole and half steps found in major and minor scales. This is the fundamental scale system in Western music, as opposed to chromatic scales that include all twelve possible pitches.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'die-ah-TON-ik (emphasis on third syllable)',
                'etymology': 'From Greek "diatonikos" meaning "through tones" (dia- "through" + tonos "tone"). Musical term from ancient Greek music theory.',
                'language_origins': 'Greek',
                'example_sentence': 'The melody was composed using a simple _____ scale, making it easy for beginners to play.',
                'memory_tip': 'Think "die-ah-TONIC" - like a musical "tonic" that goes "through" (dia) the seven notes of a standard scale.'
            },
            'diatonicwith': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "diatonicwith" appears to be "diatonic" + "with" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'diatribe': {
                'definition': 'A forceful and bitter verbal attack or criticism; a lengthy speech or piece of writing that harshly condemns something or someone. Typically characterized by angry, passionate language and sustained criticism. Often used to describe political speeches, editorials, or personal attacks that are particularly vehement.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIE-ah-tribe (emphasis on first syllable)',
                'etymology': 'From Greek "diatribe" meaning "a wearing away, discourse" (dia- "through" + tribein "to rub, wear"). Originally meant philosophical discourse but evolved to mean harsh criticism.',
                'language_origins': 'Greek',
                'example_sentence': 'The politician launched into a lengthy _____ against his opponent\'s policies during the debate.',
                'memory_tip': 'Remember "DIE-atribe" - an angry speech that could make someone "die" from the harsh criticism of the "tribe."'
            },
            'diaulos': {
                'definition': 'An ancient Greek double-flute musical instrument consisting of two reed pipes played simultaneously. The performer would play both pipes at once, often using a mouth-band to support the instruments. This was a popular instrument in ancient Greek music and religious ceremonies.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'die-OW-lohs (emphasis on second syllable)',
                'etymology': 'From Greek "diaulos" meaning "double flute" (dia- "double" + aulos "flute"). Ancient Greek musical terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'The ancient musician played a haunting melody on the _____, using both pipes to create harmonious sounds.',
                'memory_tip': 'Think "die-OWL-os" - like an owl with two pipes, the ancient Greek double flute makes music with both sides.'
            },
            'dice': {
                'definition': 'Small cubes marked with dots (pips) on each face, typically numbered one through six, used in games of chance and gambling. Can also refer to the act of cutting food into small cube-shaped pieces. The singular form is "die," though "dice" is commonly used for both singular and plural.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DICE (rhymes with "nice")',
                'etymology': 'From Old French "dé" from Latin "datum" meaning "something given." Related to gambling where outcomes are "given" by chance.',
                'language_origins': 'Latin via Old French',
                'example_sentence': 'The chef instructed his students to _____ the vegetables into small, uniform cubes.',
                'memory_tip': 'Remember "DICE" rhymes with "nice" - whether rolling for games or cutting food, you want nice, even cubes.'
            },
            'dicey': {
                'definition': 'Risky, uncertain, or potentially dangerous; unpredictable in outcome. Derived from the unpredictable nature of dice games, where outcomes depend entirely on chance. Often used to describe situations where success or safety cannot be guaranteed.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DIE-see (emphasis on first syllable)',
                'etymology': 'From "dice" + "-y" suffix. Modern slang term from mid-20th century, relating to the uncertain outcomes of dice games.',
                'language_origins': 'English (modern formation)',
                'example_sentence': 'The weather forecast looks _____ for our outdoor wedding this weekend.',
                'memory_tip': 'Think "DIE-cey" - like rolling dice, the situation could "die" (fail) or succeed, making it risky and uncertain.'
            },
            'dictionary': {
                'definition': 'A reference book or digital resource that lists words alphabetically along with their meanings, pronunciations, etymologies, and usage examples. Modern dictionaries may also include synonyms, antonyms, and grammatical information. Essential tool for language learning and understanding word definitions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIK-shun-air-ee (emphasis on first syllable)',
                'etymology': 'From Medieval Latin "dictionarium" from Latin "dictio" meaning "word, saying" (from dicere "to say"). First English dictionaries appeared in the 16th century.',
                'language_origins': 'Latin',
                'example_sentence': 'Students are encouraged to use a _____ to look up unfamiliar words while reading.',
                'memory_tip': 'Remember "DICtionary" - a book of "diction" (words) where you can find what any word means.'
            },
            'dictum': {
                'definition': 'An authoritative pronouncement or formal statement; a judge\'s expression of opinion on a legal matter. In broader usage, any dogmatic or authoritative statement of principle. Often refers to judicial opinions that, while not legally binding, carry significant weight.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIK-tum (emphasis on first syllable)',
                'etymology': 'From Latin "dictum" meaning "something said" (from dicere "to say"). Legal and scholarly term adopted directly from Latin.',
                'language_origins': 'Latin',
                'example_sentence': 'The judge\'s _____ on constitutional interpretation became widely cited in legal scholarship.',
                'memory_tip': 'Think "DICtum" - related to "dictate," an authoritative statement that someone powerful has "dictated" or proclaimed.'
            },
            'dietetic': {
                'definition': 'Relating to diet and nutrition; concerned with the regulation of food intake for health purposes. Often refers to foods specially prepared for people with specific dietary requirements, such as low-sodium or diabetic diets. Associated with the science of nutrition and therapeutic dietary planning.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'die-eh-TET-ik (emphasis on third syllable)',
                'etymology': 'From Greek "diaitētikos" meaning "of diet" (from diaita "mode of life"). Medical and nutritional terminology from ancient Greek.',
                'language_origins': 'Greek',
                'example_sentence': 'The hospital\'s _____ department creates specialized meal plans for patients with various medical conditions.',
                'memory_tip': 'Remember "die-eTETic" - sounds like "diabetic," both relating to special diets and nutrition management.'
            },
            'differed': {
                'definition': 'Past tense of differ; was unlike or distinct from something else in nature, form, or characteristics. Can also mean held a different opinion or disagreed with someone. Indicates a state of being dissimilar or having contrasting views.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'DIF-erd (emphasis on first syllable)',
                'etymology': 'From Latin "differre" meaning "to carry apart, differ" (dis- "apart" + ferre "to carry"). Past tense formation with English "-ed" suffix.',
                'language_origins': 'Latin',
                'example_sentence': 'The two scientists _____ significantly in their interpretation of the experimental results.',
                'memory_tip': 'Think "DIFFered" - they were "different" in the past, so they "differed" in their opinions or characteristics.'
            },
            'different': {
                'definition': 'Not the same as another; distinct in nature, form, or quality. Unlike or dissimilar in character or appearance. One of the most common adjectives used to indicate contrast or distinction between two or more things.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DIF-er-ent (emphasis on first syllable)',
                'etymology': 'From Latin "differentem" meaning "differing" (from differre "to differ"). Via Old French "different."',
                'language_origins': 'Latin via Old French',
                'example_sentence': 'Each snowflake has a _____ pattern, making every one unique.',
                'memory_tip': 'Remember "DIFFerent" - the "DIFF" reminds you that things are not the same, they have differences.'
            },
            'difficult': {
                'definition': 'Hard to accomplish, deal with, or understand; requiring much effort, skill, or planning to succeed. Can describe tasks, problems, people, or situations that present challenges or obstacles. Often implies the need for special effort or expertise.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DIF-i-kult (emphasis on first syllable)',
                'etymology': 'From Latin "difficilis" meaning "hard to do" (dis- "not" + facilis "easy"). Via Old French "difficile."',
                'language_origins': 'Latin via Old French',
                'example_sentence': 'Learning a new language can be _____ but very rewarding with consistent practice.',
                'memory_tip': 'Think "DIFFicult" - when something is "different" from easy, it becomes difficult and challenging.'
            },
            'difficulty': {
                'definition': 'The state or condition of being hard to accomplish or deal with; a thing that is hard to accomplish or understand. Can refer to problems, challenges, or obstacles that make progress slow or complicated. Often measured in degrees or levels.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIF-i-kul-tee (emphasis on first syllable)',
                'etymology': 'From Latin "difficultas" meaning "hardness, trouble" (from difficilis "difficult"). Noun formation from the adjective "difficult."',
                'language_origins': 'Latin',
                'example_sentence': 'The main _____ in solving this math problem is understanding the complex formula.',
                'memory_tip': 'Remember "DIFFiculty" - when you face a "difficulty," you need different strategies to overcome the challenge.'
            },
            'digerati': {
                'definition': 'A social elite of people knowledgeable about computers and technology; the digital equivalent of literati. Refers to influential figures in the technology industry, including programmers, entrepreneurs, and thought leaders who shape digital culture and innovation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dij-eh-RAH-tee (emphasis on third syllable)',
                'etymology': 'Blend of "digital" and "literati" (learned people). Coined in the 1990s during the rise of internet culture.',
                'language_origins': 'English (modern blend)',
                'example_sentence': 'The conference attracted many members of the _____ who discussed the future of artificial intelligence.',
                'memory_tip': 'Think "DIGital + literATI" = "digerati" - the learned elite of the digital world.'
            },
            'digital': {
                'definition': 'Relating to or using digital technology, especially computers and the internet. Can also refer to information stored as numerical data in binary code. In anatomy, refers to fingers or toes. Describes the modern era of electronic communication and data processing.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DIJ-i-tal (emphasis on first syllable)',
                'etymology': 'From Latin "digitalis" meaning "of or belonging to a finger" (from digitus "finger"). Extended to mean "numerical" because of counting on fingers.',
                'language_origins': 'Latin',
                'example_sentence': 'The company transformed from analog to _____ operations, improving efficiency and data management.',
                'memory_tip': 'Remember "DIGItal" - like your "digits" (fingers), digital technology counts in numbers (binary digits).'
            },
            'dignify': {
                'definition': 'To give distinction or honor to something; to make something seem worthy of respect or serious consideration. Often used when elevating the status of something that might otherwise be considered unimportant or beneath notice.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'DIG-ni-fy (emphasis on first syllable)',
                'etymology': 'From Latin "dignificare" meaning "to deem worthy" (dignus "worthy" + facere "to make"). Via Old French "dignifier."',
                'language_origins': 'Latin via Old French',
                'example_sentence': 'The author refused to _____ the critic\'s unfair attacks with a response.',
                'memory_tip': 'Think "DIGNify" - to give "dignity" to something, making it worthy of respect and honor.'
            },
            'digression': {
                'definition': 'A departure from the main subject in speech or writing; a temporary excursion away from the primary topic. Often used in literature, speeches, and academic writing to provide background information or explore related ideas before returning to the main point.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'die-GRESH-un (emphasis on second syllable)',
                'etymology': 'From Latin "digressio" meaning "a going aside" (di- "aside" + gradi "to step"). Literary and rhetorical term.',
                'language_origins': 'Latin',
                'example_sentence': 'After a brief _____ about his childhood, the speaker returned to discussing current economic policies.',
                'memory_tip': 'Think "die-GRESSION" - like "aggression," but instead of attacking, you\'re "going aside" from your main topic.'
            },
            'dihedral': {
                'definition': 'Having or formed by two plane surfaces; relating to the angle formed where two planes intersect. In geometry, refers to angles between two intersecting planes. In aviation, describes the upward or downward angle of aircraft wings relative to horizontal.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'die-HEE-dral (emphasis on second syllable)',
                'etymology': 'From Greek "di" (two) + "hedra" (face, seat). Geometric term combining Greek elements to describe two-faced angles.',
                'language_origins': 'Greek',
                'example_sentence': 'The aircraft\'s positive _____ angle helps provide stability during flight.',
                'memory_tip': 'Remember "die-HEDRal" - "di" (two) + "hedral" (faces), describing angles where two flat surfaces meet.'
            },
            'diktat': {
                'definition': 'An order or decree imposed by someone in power without popular consent; a harsh settlement or terms imposed on a defeated party. Often refers to authoritarian commands or unfair agreements forced upon those without the power to resist.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIK-tat (emphasis on first syllable)',
                'etymology': 'From German "Diktat" meaning "dictated thing" (from Latin dictare "to dictate"). Political term often associated with harsh peace treaties.',
                'language_origins': 'German from Latin',
                'example_sentence': 'The peace treaty was seen as a _____ imposed by the victorious powers on the defeated nation.',
                'memory_tip': 'Think "DIKtat" like "dictate" - an authoritarian command that is dictated to those who must obey.'
            },
            'dilapidated': {
                'definition': 'Falling apart or decaying from age and neglect; in a state of disrepair or ruin. Describes buildings, structures, or objects that have deteriorated due to lack of maintenance or the passage of time.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'die-LAP-i-day-ted (emphasis on second syllable)',
                'etymology': 'From Latin "dilapidatus" meaning "torn apart stone by stone" (dis- "apart" + lapis "stone"). Originally referred to stone buildings falling apart.',
                'language_origins': 'Latin',
                'example_sentence': 'The _____ barn had missing boards and a sagging roof that needed immediate repair.',
                'memory_tip': 'Remember "die-LAPidated" - like stones "lapping" away from a building, falling apart piece by piece.'
            },
            'dilemma': {
                'definition': 'A situation requiring a choice between equally undesirable alternatives; a difficult problem with no clear or easy solution. In logic, refers to an argument that presents two or more equally conclusive possibilities, all leading to the same conclusion.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'die-LEM-ah (emphasis on second syllable)',
                'etymology': 'From Greek "dilemma" meaning "double proposition" (di- "two" + lemma "premise"). Logical and philosophical term.',
                'language_origins': 'Greek',
                'example_sentence': 'She faced a moral _____ between telling the truth and protecting her friend\'s feelings.',
                'memory_tip': 'Think "die-LEMMA" - "di" (two) difficult choices that create a "lemma" (problem) you must solve.'
            },
            'diligence': {
                'definition': 'Careful and persistent work or effort; steady application and attention to a task or responsibility. Characterized by thoroughness, consistency, and dedication to completing work properly and completely.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIL-i-jens (emphasis on first syllable)',
                'etymology': 'From Latin "diligentia" meaning "carefulness, attentiveness" (from diligere "to choose carefully"). Via Old French "diligence."',
                'language_origins': 'Latin via Old French',
                'example_sentence': 'Her _____ in studying every night led to excellent grades and deep understanding of the subject.',
                'memory_tip': 'Remember "DILigence" - "dil" sounds like "deal," and diligent people "deal" carefully and thoroughly with their work.'
            },
            'dillydally': {
                'definition': 'To waste time by being slow or hesitant; to procrastinate or dawdle instead of taking action. Informal term describing inefficient use of time through indecision or lack of urgency.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'DIL-ee-dal-ee (emphasis on first syllable)',
                'etymology': 'Reduplication of "dally" (to waste time). Folk etymology suggesting hesitation through repetitive, playful word formation.',
                'language_origins': 'English (reduplication)',
                'example_sentence': 'Stop trying to _____ and make a decision about which restaurant you want to visit.',
                'memory_tip': 'Think "DILLY-dally" - the repeated "dilly" and "dally" sounds show someone going back and forth, wasting time.'
            },
            'diluent': {
                'definition': 'A substance used to dilute or thin another substance; an agent that reduces concentration by adding volume. Commonly used in chemistry, medicine, and manufacturing to achieve desired concentrations or consistency.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'DIL-yoo-ent (emphasis on first syllable)',
                'etymology': 'From Latin "diluere" meaning "to wash away, dilute" (dis- "away" + luere "to wash"). Scientific terminology from Latin.',
                'language_origins': 'Latin',
                'example_sentence': 'Water served as the _____ to reduce the acid concentration to safe levels.',
                'memory_tip': 'Remember "DILuent" - it "DILutes" by adding liquid to make solutions weaker or thinner.'
            },
            'dilute': {
                'definition': 'To make a liquid thinner or weaker by adding water or another solvent; to reduce the strength, force, or purity of something. Can apply to physical substances or abstract concepts like diluting someone\'s argument.',
                'part_of_speech': 'verb, adjective',
                'pronunciation_guide': 'die-LOOT (emphasis on second syllable)',
                'etymology': 'From Latin "dilutus" meaning "washed away" (dis- "away" + luere "to wash"). Chemical and general term.',
                'language_origins': 'Latin',
                'example_sentence': 'The chemist needed to _____ the solution before it could be safely handled.',
                'memory_tip': 'Think "die-LUTE" - you "loot" the strength away from something by adding liquid to make it weaker.'
            },
            'dimension': {
                'definition': 'A measurable extent of some kind, especially length, width, height, or depth; an aspect or feature of a situation or problem. In mathematics and physics, refers to the number of coordinates needed to specify a point in space.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'die-MEN-shun (emphasis on second syllable)',
                'etymology': 'From Latin "dimensio" meaning "a measuring" (from dimetiri "to measure out"). Mathematical and spatial terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The architect carefully calculated each _____ of the building to ensure it would fit the lot.',
                'memory_tip': 'Think "die-MENTION" - dimensions are the measurements you "mention" when describing size and space.'
            },
            'diminished': {
                'definition': 'Made smaller or less in size, extent, importance, or intensity; reduced or lessened. Past tense of diminish, indicating something that has been decreased or weakened from its previous state.',
                'part_of_speech': 'verb, adjective',
                'pronunciation_guide': 'die-MIN-isht (emphasis on second syllable)',
                'etymology': 'From Latin "diminuere" meaning "to lessen" (de- "down" + minuere "to make small"). Via Old French "diminuer."',
                'language_origins': 'Latin via Old French',
                'example_sentence': 'His influence in the company _____ after the failed project.',
                'memory_tip': 'Remember "die-MINished" - something became "mini" or smaller, its importance died down to a minimal level.'
            },
            'dimorphism': {
                'definition': 'The occurrence of two distinct forms of the same species, especially differences between males and females. In biology, refers to sexual dimorphism (size/appearance differences) or seasonal dimorphism (changes across seasons).',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'die-MOR-fism (emphasis on second syllable)',
                'etymology': 'From Greek "di" (two) + "morphe" (form) + "-ism." Scientific term describing dual forms in biology.',
                'language_origins': 'Greek',
                'example_sentence': 'Sexual _____ in peacocks is evident in the dramatic difference between male and female plumage.',
                'memory_tip': 'Think "die-MORphism" - "di" (two) different "morph" (forms) of the same species, like two shapes.'
            },
            'dimple': {
                'definition': 'A small natural indentation in the skin, especially on the cheek or chin; a slight depression in any surface. Often considered an attractive facial feature formed by underlying facial muscle structure.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DIM-pul (emphasis on first syllable)',
                'etymology': 'Middle English, possibly from Old English "dympel." Related to "dip" and other words suggesting small depressions.',
                'language_origins': 'Germanic',
                'example_sentence': 'Her smile revealed a charming _____ on her left cheek.',
                'memory_tip': 'Think "DIMple" - a "dim" little dip or depression that makes a "dimple" in the skin.'
            },
            'dinero': {
                'definition': 'Spanish word for money or cash; used informally in English to refer to money, especially in regions with significant Spanish-speaking populations. Originally referred to silver coins but now means money generally.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dee-NAIR-oh (emphasis on second syllable)',
                'etymology': 'From Spanish "dinero" from Latin "denarius" (Roman silver coin). Related to "denier" and other currency terms.',
                'language_origins': 'Spanish from Latin',
                'example_sentence': 'He spent all his _____ on a fancy dinner at the new restaurant.',
                'memory_tip': 'Remember "dee-NAIR-oh" - Spanish word for money that sounds like "diner-o," money for eating at a diner.'
            },
            'dingoes': {
                'definition': 'Plural of dingo; wild dogs native to Australia, typically yellowish-brown with pointed ears and a bushy tail. Descended from domestic dogs brought to Australia thousands of years ago, they are now considered a distinct subspecies.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DING-ohs (emphasis on first syllable)',
                'etymology': 'From an Australian Aboriginal language, possibly Dharuk "din-go." Adopted into English from indigenous Australian languages.',
                'language_origins': 'Australian Aboriginal',
                'example_sentence': 'The researchers studied the behavior of _____ in their natural habitat across the Australian outback.',
                'memory_tip': 'Think "DING-ohs" - wild Australian dogs that might "ding" or damage things, plural "ohs" for multiple dogs.'
            },
            'dinner': {
                'definition': 'The main meal of the day, typically eaten in the evening; a formal meal or banquet. Can refer to the largest meal regardless of timing, though commonly associated with evening dining in modern usage.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIN-er (emphasis on first syllable)',
                'etymology': 'From Old French "disner" meaning "to dine" (from Latin "disjejunare" meaning "to break one\'s fast"). Originally referred to the main meal.',
                'language_origins': 'Old French from Latin',
                'example_sentence': 'The family gathered every Sunday for a traditional _____ of roast beef and vegetables.',
                'memory_tip': 'Remember "DINner" - the main meal where people "din" (make noise) around the table, sharing food and conversation.'
            },
            'dinosaur': {
                'definition': 'An extinct reptile that lived millions of years ago, ranging from small bird-like creatures to massive long-necked giants; informally, something or someone considered outdated or old-fashioned. Dinosaurs dominated Earth during the Mesozoic Era.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIE-no-sore (emphasis on first syllable)',
                'etymology': 'From Greek "deinos" (terrible) + "saurus" (lizard). Coined by paleontologist Richard Owen in 1842 to describe fossil reptiles.',
                'language_origins': 'Greek (modern scientific coinage)',
                'example_sentence': 'The museum\'s _____ exhibit featured a complete Tyrannosaurus rex skeleton.',
                'memory_tip': 'Think "DIE-no-sore" - ancient "terrible lizards" that died out long ago, making them "sore" losers in evolution.'
            },
            'diocese': {
                'definition': 'A district under the pastoral care of a bishop in the Christian church; the territorial jurisdiction of a bishop. Represents both the geographic area and the community of churches administered by episcopal authority.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIE-oh-sees (emphasis on first syllable)',
                'etymology': 'From Greek "dioikesis" meaning "administration, province" (dia- "through" + oikein "to manage"). Ecclesiastical administrative term.',
                'language_origins': 'Greek',
                'example_sentence': 'The new bishop was assigned to oversee the largest _____ in the state.',
                'memory_tip': 'Think "DIE-ocese" - a church district that a bishop "sees" over and administers spiritually.'
            },
            'diode': {
                'definition': 'An electronic component that allows electric current to flow in only one direction; a two-terminal semiconductor device. Essential in electronic circuits for converting alternating current to direct current and preventing reverse current flow.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIE-ohd (emphasis on first syllable)',
                'etymology': 'From Greek "di" (two) + "hodos" (way). Coined in electronics to describe a two-terminal device with directional current flow.',
                'language_origins': 'Greek (modern scientific coinage)',
                'example_sentence': 'The LED light contains a _____ that converts electricity into visible light.',
                'memory_tip': 'Remember "DIE-ode" - "di" (two) terminals, but current can only take one "ode" (path) through it.'
            },
            'diphtheria': {
                'definition': 'A serious bacterial infection affecting the mucous membranes of the throat and nose; characterized by the formation of a thick gray membrane that can block breathing. Now prevented by vaccination in most developed countries.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dif-THEER-ee-ah (emphasis on second syllable)',
                'etymology': 'From Greek "diphthera" meaning "leather" (referring to the leathery membrane formed in the throat). Medical terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'Before vaccines, _____ was a leading cause of childhood death due to breathing difficulties.',
                'memory_tip': 'Think "dif-THER-ia" - a disease that creates a "leather-like" membrane in the "throat" (ther).'
            },
            'diplodocus': {
                'definition': 'A large, long-necked dinosaur from the Late Jurassic period, characterized by its extremely long tail and neck. One of the longest dinosaurs known, reaching lengths of up to 90 feet, with a relatively small head compared to its massive body.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dip-LOD-oh-kus (emphasis on second syllable)',
                'etymology': 'From Greek "diplos" (double) + "dokos" (beam), referring to the double-beamed chevron bones in its tail. Paleontological naming.',
                'language_origins': 'Greek (scientific nomenclature)',
                'example_sentence': 'The _____ used its long neck to reach vegetation that other dinosaurs couldn\'t access.',
                'memory_tip': 'Think "dip-LODocus" - a dinosaur that could "dip" its long neck down to "load" up on plants with its massive size.'
            },
            'diploma': {
                'definition': 'An official document certifying the successful completion of a course of study or training; a certificate awarded by an educational institution. Represents academic achievement and qualifies holders for advanced study or professional opportunities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dip-LOH-mah (emphasis on second syllable)',
                'etymology': 'From Greek "diploma" meaning "folded paper" (from diploun "to fold double"). Originally referred to official documents folded for authenticity.',
                'language_origins': 'Greek',
                'example_sentence': 'After four years of hard work, she finally received her college _____.',
                'memory_tip': 'Think "dip-LOMA" - you "dip" your head to receive your diploma, a document that shows you completed your educational "loma" (load).'
            },
            'diptych': {
                'definition': 'A work of art consisting of two panels or sections, typically hinged together; originally referring to ancient writing tablets. Common in religious art, where two panels might show related scenes or complementary subjects.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIP-tik (emphasis on first syllable)',
                'etymology': 'From Greek "diptychos" meaning "folded in two" (di- "two" + ptychē "fold"). Art and literary terminology.',
                'language_origins': 'Greek',
                'example_sentence': 'The medieval _____ depicted scenes from the life of Christ on two connected wooden panels.',
                'memory_tip': 'Remember "DIP-tych" - "dip" (two) panels that you can "tick" (touch) together, folded art in two parts.'
            },
            'dire': {
                'definition': 'Extremely serious or urgent; warning of or threatening disaster or misfortune. Describes situations that are desperate, critical, or foreboding, often requiring immediate attention or action.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DIRE (rhymes with "fire")',
                'etymology': 'From Latin "dirus" meaning "fearful, awful." Via Old French "dire." Related to "dirge" and other words suggesting doom.',
                'language_origins': 'Latin via Old French',
                'example_sentence': 'The economic forecast painted a _____ picture of unemployment and recession.',
                'memory_tip': 'Remember "DIRE" rhymes with "fire" - both represent dangerous, threatening situations that demand immediate attention.'
            },
            'direct': {
                'definition': 'Proceeding in a straight line or by the shortest course; straightforward and honest in manner or speech. Can mean to guide, manage, or control something toward a particular end or in a particular direction.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'die-REKT or DIE-rekt (emphasis varies)',
                'etymology': 'From Latin "directus" meaning "straight" (from dirigere "to guide straight"). Via Old French "direct."',
                'language_origins': 'Latin via Old French',
                'example_sentence': 'She gave him _____ instructions on how to reach the downtown office.',
                'memory_tip': 'Think "die-RECT" - to "correct" something by making it straight and "direct," without detours or confusion.'
            },
            'directly': {
                'definition': 'In a straight line or by the shortest route; immediately or at once; in a frank and honest manner. Indicates both spatial and temporal immediacy, as well as communication style.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'die-REKT-lee (emphasis on second syllable)',
                'etymology': 'From "direct" + "-ly" adverbial suffix. Formation following standard English adverb patterns.',
                'language_origins': 'Latin via Old French with English suffix',
                'example_sentence': 'Please speak _____ to the manager about your concerns regarding the service.',
                'memory_tip': 'Remember "die-RECTly" - doing something "directly" means doing it in a "correct" and straight manner immediately.'
            },
            'dirigible': {
                'definition': 'A large balloon or airship that can be steered and propelled through the air; a lighter-than-air aircraft with its own power source. Distinguished from balloons by having engines and steering capabilities.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'DIR-i-ji-bul (emphasis on first syllable)',
                'etymology': 'From Latin "dirigere" meaning "to direct, guide." Aeronautical term for steerable aircraft.',
                'language_origins': 'Latin',
                'example_sentence': 'The vintage _____ floated majestically over the city during the air show.',
                'memory_tip': 'Think "DIRigible" - an aircraft you can "direct" and guide through the sky, unlike a balloon that just drifts.'
            },
            'dirndl': {
                'definition': 'A traditional dress worn in Germany, Austria, and Switzerland, consisting of a bodice, blouse, full skirt, and apron. Commonly associated with Bavarian and Alpine culture, often worn during festivals like Oktoberfest.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DIRN-dul (emphasis on first syllable)',
                'etymology': 'From German/Austrian dialect "Dirndl," diminutive of "Dirne" meaning "girl." Traditional clothing terminology.',
                'language_origins': 'German/Austrian',
                'example_sentence': 'She wore a beautiful traditional _____ to the Oktoberfest celebration.',
                'memory_tip': 'Think "DIRN-dl" - a traditional German dress that "turns" girls into the classic Alpine look with its distinctive style.'
            },
            'disaster': {
                'definition': 'A sudden event causing great damage, destruction, or distress; a complete failure or fiasco. Can refer to natural catastrophes like earthquakes or human-caused events like accidents.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'die-ZAS-ter (emphasis on second syllable)',
                'etymology': 'From Italian "disastro" from Greek "dis-" (bad) + "astron" (star). Originally referred to unfavorable astrological influences.',
                'language_origins': 'Italian from Greek',
                'example_sentence': 'The earthquake was a natural _____ that required international humanitarian aid.',
                'memory_tip': 'Think "die-ZASter" - like a "zap" from bad stars that brings destruction and makes things "die" or fail completely.'
            },
            'disasternoun': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "disasternoun" appears to be "disaster" + "noun" merged together. This is likely a PDF parsing error where the word "disaster" was incorrectly combined with grammatical notation.'
            },
            'disband': {
                'definition': 'To break up or dissolve an organized group; to dismiss members of an organization and cease operations. Often refers to military units, clubs, bands, or other formal groups ending their association.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'dis-BAND (emphasis on second syllable)',
                'etymology': 'From prefix "dis-" (apart) + "band" (group). Formation indicating the breaking apart of a bound group.',
                'language_origins': 'English (prefix + word combination)',
                'example_sentence': 'After the scandal, the board decided to _____ the committee permanently.',
                'memory_tip': 'Think "dis-BAND" - to "dis" (dismiss) a "band" or group, breaking it apart and scattering the members.'
            }
        }
        
        return batch_051_data.get(word.lower(), {})
    
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
    processor = Batch051Processor()
    success = processor.process_csv("batch_051_words.csv", "batch_051_processed.csv")
    
    if success:
        print("Batch 051 processing completed successfully!")
    else:
        print("Batch 051 processing failed!")

if __name__ == "__main__":
    main()