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
        
        high_freq = ['double', 'doubled', 'doubt', 'dough', 'doughnut', 'download', 'dots', 'dotted', 'drawing', 'drawn', 'draws', 'dream', 'dread']
        medium_freq = ['doomed', 'dormitories', 'dosages', 'drape', 'drastic', 'drawers', 'drawl', 'dredged', 'dribbles', 'drag']
        
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
        prefixes = ['do-', 'dr-', 'dow-']
        suffixes = ['-ed', '-ing', '-er', '-ous', '-tion', '-ary', '-ment', '-ive']
        
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
        elif any(word_lower.startswith(prefix) for prefix in ['do', 'dr']):
            return 4
        else:
            return 3

class Batch054Processor:
    def __init__(self):
        self.base_path = "/c/Users/jessi/Projects/skilltree2/scripts/spelling_bee"
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive data using Claude's knowledge"""
        
        batch_054_data = {
            'doodled': {
                'definition': 'Past tense of doodle; drew aimlessly or absentmindedly, typically while thinking about something else. Often refers to simple drawings made without conscious artistic intent.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'DOO-duhld (emphasis on first syllable)',
                'etymology': 'From "doodle" (possibly from German "dudeln" meaning "to play pipes"). Past tense of mindless drawing.',
                'language_origins': 'English, possibly from German',
                'example_sentence': 'While listening to the lecture, she _____ flowers and geometric shapes in her notebook margins.',
                'memory_tip': 'Remember "DOOdled" - you "do" little drawings mindlessly, just doodling around without thinking.'
            },
            'doomed': {
                'definition': 'Certain to meet with or cause failure, destruction, or death; destined for a terrible fate. Indicates an inevitable bad outcome.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'DOOMD (rhymes with "zoomed")',
                'etymology': 'From Old English "dom" meaning "judgment, fate." Past participle of "doom," meaning condemned to a bad fate.',
                'language_origins': 'Old English',
                'example_sentence': 'The expedition was _____ from the start due to poor planning and bad weather.',
                'memory_tip': 'Think "DOOMED" rhymes with "zoomed" - heading straight toward disaster, zoomed into a terrible fate.'
            },
            'doorjamb': {
                'definition': 'The vertical piece that forms the side of a doorway; the frame around a door opening. Architectural term for door frame components.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOOR-jam (emphasis on first syllable)',
                'etymology': 'From "door" + "jamb" (from Old French "jambe" meaning "leg"). The "leg" or side support of a doorway.',
                'language_origins': 'English + Old French',
                'example_sentence': 'He measured the _____ carefully to ensure the new door would fit properly.',
                'memory_tip': 'Remember "DOORjamb" - the "jamb" is like the "leg" that supports the door frame on each side.'
            },
            'dopamine': {
                'definition': 'A neurotransmitter chemical in the brain associated with pleasure, reward, and motivation. Important for motor control and emotional regulation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOHP-uh-meen (emphasis on first syllable)',
                'etymology': 'From "DOPA" (chemical precursor) + "amine" (chemical suffix). Scientific terminology for brain chemistry.',
                'language_origins': 'Scientific Latin',
                'example_sentence': 'Exercise naturally increases _____ levels, which can improve mood and motivation.',
                'memory_tip': 'Think "DOPamine" - the "dope" brain chemical that makes you feel good and motivated.'
            },
            'doppelgänger': {
                'definition': 'A person who looks exactly like someone else; a ghostly double or counterpart of a living person. Originally a supernatural concept, now used for look-alikes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOP-ul-gang-er (emphasis on first syllable)',
                'etymology': 'From German "Doppelgänger" meaning "double-goer" (doppel "double" + gänger "goer"). Folklore terminology.',
                'language_origins': 'German',
                'example_sentence': 'She was shocked to meet her _____ at the conference, someone who looked exactly like her.',
                'memory_tip': 'Remember "DOPpelgänger" - a "double" person who "gangs" around looking exactly like you.'
            },
            'doppler': {
                'definition': 'Relating to the Doppler effect, where the frequency of waves changes for an observer moving relative to the source. Physics principle explaining changing pitch.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'DOP-ler (emphasis on first syllable)',
                'etymology': 'Named after Christian Doppler, Austrian physicist who described the effect in 1842. Scientific eponym.',
                'language_origins': 'German (surname)',
                'example_sentence': 'The _____ radar can detect the speed of approaching vehicles by measuring frequency changes.',
                'memory_tip': 'Think "DOPpler" - named after Doppler, the scientist who explained why sounds change pitch when moving.'
            },
            'dorking': {
                'definition': 'A breed of domestic chicken known for having five toes instead of four; named after Dorking, England. Poultry terminology.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOR-king (emphasis on first syllable)',
                'etymology': 'Named after Dorking, a town in Surrey, England, where this chicken breed was developed.',
                'language_origins': 'English (place name)',
                'example_sentence': 'The farmer raised _____ chickens, prized for their unique five-toed feet and meat quality.',
                'memory_tip': 'Remember "DORking" - a chicken breed from Dorking, England, known for its extra toe.'
            },
            'dormitories': {
                'definition': 'Plural of dormitory; large sleeping rooms with multiple beds, typically in schools, colleges, or institutions. Student housing facilities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOR-mi-tor-eez (emphasis on first syllable)',
                'etymology': 'From Latin "dormitorium" meaning "sleeping place" (dormire "to sleep"). Institutional housing terminology.',
                'language_origins': 'Latin',
                'example_sentence': 'The university built new _____ to accommodate the growing number of students.',
                'memory_tip': 'Remember "DORMitories" - places where students "dorm" (sleep), multiple sleeping quarters for residents.'
            },
            'dorsiflexor': {
                'definition': 'A muscle that causes dorsiflexion, the upward bending of the foot or hand. Anatomical term for muscles that lift extremities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dor-si-FLEK-sor (emphasis on third syllable)',
                'etymology': 'From Latin "dorsum" (back) + "flexor" (bender). Anatomical term for back-bending muscles.',
                'language_origins': 'Latin',
                'example_sentence': 'The _____ muscles help lift the toes upward when walking.',
                'memory_tip': 'Think "dorsi-FLEXor" - muscles that "flex" the "dorsal" (back) side, lifting feet or hands upward.'
            },
            'dory': {
                'definition': 'A small, flat-bottomed boat with high sides and a narrow transom; a type of edible marine fish. Nautical and marine terminology.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOR-ee (emphasis on first syllable)',
                'etymology': 'From French "doré" meaning "golden" (referring to the golden color of the fish). Maritime terminology.',
                'language_origins': 'French',
                'example_sentence': 'The fishermen rowed their _____ out to the deeper waters where the fish were plentiful.',
                'memory_tip': 'Remember "DORy" - a golden-colored boat or fish, both found near water.'
            },
            'dosages': {
                'definition': 'Plural of dosage; prescribed amounts of medicine or drugs to be taken at specific intervals. Medical terminology for medication quantities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOH-si-jiz (emphasis on first syllable)',
                'etymology': 'From "dose" (from Greek "dosis" meaning "a giving") + "-age" suffix + plural "-s." Medical terminology.',
                'language_origins': 'Greek via English formation',
                'example_sentence': 'The doctor carefully calculated the appropriate _____ for each patient based on their weight.',
                'memory_tip': 'Think "DOSages" - the "doses" given to patients, specific amounts of medication prescribed.'
            },
            'dots': {
                'definition': 'Plural of dot; small round marks or spots; punctuation marks used in writing. Can refer to small circular markings.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DOTS (rhymes with "lots")',
                'etymology': 'From Old English "dott" meaning "head of a boil." Basic English term for small marks.',
                'language_origins': 'Old English',
                'example_sentence': 'The artist created a beautiful pattern using colored _____ of various sizes.',
                'memory_tip': 'Simple "DOTS" - small round marks, like the "dots" on dice or polka dot patterns.'
            },
            'dotted': {
                'definition': 'Marked with dots; scattered or distributed across an area. Can describe patterns, signatures, or geographic distribution.',
                'part_of_speech': 'adjective, verb',
                'pronunciation_guide': 'DOT-ed (emphasis on first syllable)',
                'etymology': 'From "dot" + "-ed" suffix. Past tense of putting dots on something or having dots.',
                'language_origins': 'English',
                'example_sentence': 'She signed on the _____ line to complete the legal contract.',
                'memory_tip': 'Remember "DOTted" - covered with "dots," like a dotted line you sign on documents.'
            },
            'double': {
                'definition': 'Twice as much or many; consisting of two identical or similar parts; to multiply by two or increase twofold.',
                'part_of_speech': 'adjective, verb, noun',
                'pronunciation_guide': 'DUH-bul (emphasis on first syllable)',
                'etymology': 'From Old French "doble" from Latin "duplus" meaning "twofold" (duo "two" + -plus "fold").',
                'language_origins': 'Latin via Old French',
                'example_sentence': 'The recipe calls for a _____ portion of chocolate chips to make it extra sweet.',
                'memory_tip': 'Think "DOUble" - like "duo," it means two of something, twice the amount.'
            },
            'doubled': {
                'definition': 'Past tense of double; increased to twice the amount; folded over on itself. Indicates something that became twice as much.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'DUH-buld (emphasis on first syllable)',
                'etymology': 'From "double" + "-ed" suffix. Past tense of increasing by two or folding over.',
                'language_origins': 'Latin via Old French with English suffix',
                'example_sentence': 'The company\'s profits _____ after they introduced the new product line.',
                'memory_tip': 'Remember "DOUbled" - something that was made "double," increased to twice its original size.'
            },
            'doubloons': {
                'definition': 'Historical Spanish gold coins used in colonial America and pirate stories; valuable coins associated with treasure and maritime adventure.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'duh-BLOONZ (emphasis on second syllable)',
                'etymology': 'From Spanish "doblón" meaning "double" (because worth two escudos). Historical monetary terminology.',
                'language_origins': 'Spanish',
                'example_sentence': 'The pirates buried their treasure chest filled with gold _____ on the remote island.',
                'memory_tip': 'Think "duh-BLOONS" - "double" value Spanish gold coins that pirates loved to steal and bury.'
            },
            'doubt': {
                'definition': 'A feeling of uncertainty or lack of conviction; to feel uncertain about the truth or reliability of something.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DOWT (rhymes with "out")',
                'etymology': 'From Old French "douter" from Latin "dubitare" meaning "to hesitate, waver." The "b" is silent.',
                'language_origins': 'Latin via Old French',
                'example_sentence': 'She began to _____ whether she had made the right decision about changing careers.',
                'memory_tip': 'Remember "DOUBT" sounds like "out" - when you doubt, certainty goes "out" the window.'
            },
            'dough': {
                'definition': 'A thick mixture of flour and liquid used for baking bread, pastries, or pizza; informal term for money.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOH (rhymes with "go")',
                'etymology': 'From Old English "dag" meaning "dough." Related to Germanic words for kneading and dough-making.',
                'language_origins': 'Old English',
                'example_sentence': 'She kneaded the bread _____ until it became smooth and elastic.',
                'memory_tip': 'Simple "DOUGH" rhymes with "go" - the mixture that will "go" into the oven to become bread.'
            },
            'doughnut': {
                'definition': 'A small, ring-shaped cake made of sweet dough and fried in fat; a popular breakfast pastry often glazed or filled.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOH-nut (emphasis on first syllable)',
                'etymology': 'From "dough" + "nut." Originally because the center was filled with nuts, later became the ring shape.',
                'language_origins': 'English',
                'example_sentence': 'He stopped at the bakery to buy a fresh glazed _____ with his morning coffee.',
                'memory_tip': 'Remember "DOUGHnut" - made from "dough" in the shape of a "nut" (ring), a sweet fried pastry.'
            },
            'douloureux': {
                'definition': 'A medical term meaning "painful," specifically referring to trigeminal neuralgia (tic douloureux), a severe facial nerve pain condition.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'doo-loo-RUH (emphasis on third syllable)',
                'etymology': 'From French "douloureux" meaning "painful" (from douleur "pain"). Medical terminology.',
                'language_origins': 'French',
                'example_sentence': 'The patient suffered from tic _____, experiencing sharp facial pain along the nerve.',
                'memory_tip': 'Think "doo-lou-REUX" - sounds like "do-you-rue" (regret), because this condition causes painful regret.'
            },
            'dovecote': {
                'definition': 'A structure built to house doves or pigeons; a small building or compartment designed for keeping domesticated birds.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DUV-koht (emphasis on first syllable)',
                'etymology': 'From "dove" + "cote" (from Old English "cot" meaning "small dwelling"). Agricultural terminology.',
                'language_origins': 'Old English',
                'example_sentence': 'The old farm had a charming _____ where white doves nested peacefully.',
                'memory_tip': 'Remember "DOVEcote" - a "cote" (cottage) where "doves" live, a house for birds.'
            },
            'dowager': {
                'definition': 'A widow holding property or title from her deceased husband; an elderly woman of dignified bearing, especially from aristocracy.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DOW-uh-jer (emphasis on first syllable)',
                'etymology': 'From Old French "douagiere" from "douage" (dower). Legal and social terminology for widowed nobility.',
                'language_origins': 'Old French',
                'example_sentence': 'The _____ empress maintained her royal duties even after her husband\'s death.',
                'memory_tip': 'Think "DOWager" - a widow who was "dowed" (given property) by her deceased husband.'
            },
            'dowdy': {
                'definition': 'Lacking in stylishness or smartness; unfashionable in appearance or dress. Describes someone who dresses without attention to current fashion.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DOW-dee (emphasis on first syllable)',
                'etymology': 'Origin uncertain, possibly from Middle English "doude" meaning "an unattractive woman." Fashion terminology.',
                'language_origins': 'Middle English (uncertain)',
                'example_sentence': 'She felt _____ in her old sweater compared to her fashionably dressed friends.',
                'memory_tip': 'Remember "DOWdy" - like feeling "down" about your unfashionable, outdated appearance.'
            },
            'dowdycorkscrew': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "dowdycorkscrew" appears to be "dowdy" + "corkscrew" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'downcast': {
                'definition': 'Feeling despondent or dejected; looking or directed downward. Describes both emotional state and physical direction.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DOWN-kast (emphasis on first syllable)',
                'etymology': 'From "down" + "cast" (thrown, directed). Literally meaning thrown or directed downward.',
                'language_origins': 'English',
                'example_sentence': 'His _____ expression revealed his disappointment about not getting the promotion.',
                'memory_tip': 'Think "DOWNcast" - both your eyes and mood are cast "down" when you\'re sad and dejected.'
            },
            'downcastjubilant': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "downcastjubilant" appears to be "downcast" + "jubilant" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'download': {
                'definition': 'To transfer data from a remote computer or server to a local device; the process of receiving digital files via internet connection.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'DOWN-lohd (emphasis on first syllable)',
                'etymology': 'From "down" + "load." Computer terminology from the 1970s, referring to transferring data "down" from a server.',
                'language_origins': 'English (modern technology)',
                'example_sentence': 'You can _____ the software update directly from the company\'s website.',
                'memory_tip': 'Remember "DOWNload" - data comes "down" from the internet server to "load" onto your device.'
            },
            'doxycycline': {
                'definition': 'A broad-spectrum antibiotic used to treat various bacterial infections, including acne, respiratory infections, and tick-borne diseases.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dok-si-SYE-kleen (emphasis on third syllable)',
                'etymology': 'From "doxy-" (chemical prefix) + "cycline" (tetracycline family suffix). Pharmaceutical nomenclature.',
                'language_origins': 'Scientific Latin',
                'example_sentence': 'The doctor prescribed _____ to treat the patient\'s respiratory infection.',
                'memory_tip': 'Think "doxy-CYCLine" - a "cycle" of medicine that\'s "doxy" (effective) against bacterial infections.'
            },
            'draconian': {
                'definition': 'Excessively harsh or severe, especially in laws or punishment; characterized by extreme strictness or cruelty.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'dray-KOH-nee-an (emphasis on second syllable)',
                'etymology': 'From Draco, ancient Greek lawmaker known for extremely harsh laws. His name + "-ian" suffix.',
                'language_origins': 'Greek (eponym)',
                'example_sentence': 'The school\'s _____ dress code prohibited any clothing that wasn\'t navy blue or white.',
                'memory_tip': 'Remember "dray-CONian" - like "dragon," draconian rules are fierce and harsh, named after Draco.'
            },
            'draegerman': {
                'definition': 'A mine rescue worker trained in using breathing apparatus in dangerous underground conditions; a specialist in mine emergency response.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DRAG-er-man (emphasis on first syllable)',
                'etymology': 'From "Draeger" (German breathing apparatus manufacturer) + "man." Mining safety terminology.',
                'language_origins': 'German + English',
                'example_sentence': 'The _____ quickly descended into the mine to rescue the trapped miners.',
                'memory_tip': 'Think "DRAGERman" - a rescue worker who uses "Draeger" breathing equipment to save people in mines.'
            },
            'drag': {
                'definition': 'To pull something along a surface, typically the ground; to move slowly and with effort; air resistance against a moving object.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'DRAG (rhymes with "bag")',
                'etymology': 'From Old English "dragan" meaning "to draw, pull." Related to Germanic words for drawing and pulling.',
                'language_origins': 'Old English',
                'example_sentence': 'He had to _____ the heavy suitcase up three flights of stairs.',
                'memory_tip': 'Simple "DRAG" - when something is hard to move, you have to "drag" it along the ground.'
            },
            'dragoon': {
                'definition': 'A member of a cavalry regiment; to coerce someone into doing something they are reluctant to do.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'drah-GOON (emphasis on second syllable)',
                'etymology': 'From French "dragon" (soldier with a dragon-decorated gun). Military terminology.',
                'language_origins': 'French',
                'example_sentence': 'The committee tried to _____ him into volunteering for the unpopular assignment.',
                'memory_tip': 'Think "drah-GOON" - like a "dragon," a fierce soldier who might "goon" (force) people to comply.'
            },
            'dragée': {
                'definition': 'A small, round confection covered with a hard coating; sugar-coated almonds or other candies often used in celebrations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'drah-ZHAY (emphasis on second syllable)',
                'etymology': 'From French "dragée" from Old French "dragie." Confectionery terminology.',
                'language_origins': 'French',
                'example_sentence': 'The wedding favors included elegant white _____ in small satin bags.',
                'memory_tip': 'Remember "drah-ZHAY" - French candy that sounds elegant, small sugar-coated treats for special occasions.'
            },
            'drahthaar': {
                'definition': 'A German breed of hunting dog with a wiry coat, also known as German Wirehaired Pointer; bred for versatile hunting and retrieving.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DRAHT-har (emphasis on first syllable)',
                'etymology': 'From German "Draht" (wire) + "Haar" (hair). Refers to the dog\'s distinctive wiry coat.',
                'language_origins': 'German',
                'example_sentence': 'The _____ excelled at both pointing game birds and retrieving waterfowl.',
                'memory_tip': 'Think "DRAHT-hair" - a German dog breed with "draft" (wiry) "hair" for hunting.'
            },
            'dramatization': {
                'definition': 'The adaptation of a story into a dramatic form; the process of making something seem more dramatic or exciting than it actually is.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'dram-uh-ti-ZAY-shun (emphasis on fourth syllable)',
                'etymology': 'From "drama" + "-tize" + "-ation." About making something dramatic or theatrical.',
                'language_origins': 'English formation from Greek roots',
                'example_sentence': 'The television _____ of the historical novel won several Emmy awards.',
                'memory_tip': 'Remember "drama-ti-ZATION" - the process of making something into a "drama" for theater or TV.'
            },
            'dramaturgy': {
                'definition': 'The art or technique of dramatic composition and theatrical representation; the craft of structuring and presenting dramatic works.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DRAM-uh-tur-jee (emphasis on first syllable)',
                'etymology': 'From Greek "drama" (drama) + "ergon" (work). The craft of creating dramatic works.',
                'language_origins': 'Greek',
                'example_sentence': 'Her expertise in _____ helped the theater company develop more compelling productions.',
                'memory_tip': 'Think "DRAMA-turgy" - the "urgy" (working) craft of creating and staging "drama."'
            },
            'drape': {
                'definition': 'To arrange cloth or clothing loosely on or around something; to cover or hang with cloth in graceful folds.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'DRAYP (rhymes with "cape")',
                'etymology': 'From Old French "draper" meaning "to weave, make cloth." Related to fabric and clothing terminology.',
                'language_origins': 'Old French',
                'example_sentence': 'She decided to _____ the table with her grandmother\'s vintage lace tablecloth.',
                'memory_tip': 'Remember "DRAPE" rhymes with "cape" - both involve hanging fabric gracefully over something.'
            },
            'drastic': {
                'definition': 'Extreme in effect or action; likely to have a strong or far-reaching impact; severe or radical in nature.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'DRAS-tik (emphasis on first syllable)',
                'etymology': 'From Greek "drastikos" meaning "effective, active" (from dran "to do, act"). About taking strong action.',
                'language_origins': 'Greek',
                'example_sentence': 'The company had to take _____ measures to avoid bankruptcy.',
                'memory_tip': 'Think "DRASTic" - so extreme it might "drag" you into dramatic, life-changing consequences.'
            },
            'drawers': {
                'definition': 'Sliding compartments in furniture for storage; old-fashioned term for underwear or undergarments.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DRAW-erz (emphasis on first syllable)',
                'etymology': 'From "draw" + "-er" suffix + plural "-s." Things that are drawn or pulled out.',
                'language_origins': 'English',
                'example_sentence': 'She organized all her socks and underwear in the bedroom _____ .',
                'memory_tip': 'Remember "DRAWers" - compartments you "draw" (pull) out to access stored items inside.'
            },
            'drawing': {
                'definition': 'A picture or diagram made with a pencil, pen, or crayon; the art of making pictures by hand; the action of pulling something.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DRAW-ing (emphasis on first syllable)',
                'etymology': 'From "draw" + "-ing" suffix. The action or result of drawing lines to create images.',
                'language_origins': 'English',
                'example_sentence': 'Her pencil _____ of the landscape captured every detail beautifully.',
                'memory_tip': 'Simple "DRAWing" - the act of "drawing" lines to create pictures or art.'
            },
            'drawl': {
                'definition': 'A slow, prolonged way of speaking with vowels drawn out; to speak in this manner, often associated with certain regional accents.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DRAWL (rhymes with "all")',
                'etymology': 'Probably from "draw" meaning to stretch out. About stretching out speech sounds.',
                'language_origins': 'English',
                'example_sentence': 'His Southern _____ made every word sound relaxed and unhurried.',
                'memory_tip': 'Remember "DRAWL" rhymes with "all" - you draw out "all" the vowels when you speak with a drawl.'
            },
            'drawn': {
                'definition': 'Past participle of draw; pulled, attracted, or sketched; appearing strained, tired, or tense from stress or illness.',
                'part_of_speech': 'verb, adjective',
                'pronunciation_guide': 'DRAWN (rhymes with "lawn")',
                'etymology': 'From Old English "dragan" past participle. Past tense of pulling or creating pictures.',
                'language_origins': 'Old English',
                'example_sentence': 'After the long illness, his face looked pale and _____ .',
                'memory_tip': 'Remember "DRAWN" rhymes with "worn" - when you look drawn, you appear worn out and tired.'
            },
            'draws': {
                'definition': 'Third person singular present of draw; pulls, attracts, or creates pictures; competitions that end in a tie.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'DRAWZ (rhymes with "laws")',
                'etymology': 'From "draw" + third person singular "-s." Present tense of pulling or attracting.',
                'language_origins': 'English',
                'example_sentence': 'The magnet _____ metal objects toward it with invisible force.',
                'memory_tip': 'Simple "DRAWS" - what someone does when they pull things or create pictures with a pencil.'
            },
            'dread': {
                'definition': 'Great fear or apprehension about something that might happen; to anticipate with great anxiety or fear.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DRED (rhymes with "red")',
                'etymology': 'From Old English "drædan" meaning "to fear greatly." Related to Germanic words for fear.',
                'language_origins': 'Old English',
                'example_sentence': 'She felt a sense of _____ as the final exam date approached.',
                'memory_tip': 'Remember "DREAD" rhymes with "red" - fear makes you see red with anxiety and worry.'
            },
            'dreadlocks': {
                'definition': 'A hairstyle where hair is twisted into long, rope-like strands; naturally matted or intentionally locked hair sections.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DRED-loks (emphasis on first syllable)',
                'etymology': 'From "dread" + "locks" (hair). Originally associated with Rastafarian culture.',
                'language_origins': 'English (cultural)',
                'example_sentence': 'His _____ had taken years to grow and were an important part of his cultural identity.',
                'memory_tip': 'Remember "DREADlocks" - hair "locks" that some people might "dread" (fear) to touch because they\'re tightly matted.'
            },
            'dream': {
                'definition': 'A series of thoughts, images, and sensations during sleep; a cherished aspiration, ambition, or ideal; to experience dreams while sleeping.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'DREEM (rhymes with "team")',
                'etymology': 'From Old English "dream" meaning "joy, music." Later came to mean sleep visions.',
                'language_origins': 'Old English',
                'example_sentence': 'Her _____ of becoming a doctor motivated her through years of difficult study.',
                'memory_tip': 'Simple "DREAM" rhymes with "team" - dreams bring together thoughts and images like a team in your mind.'
            },
            'dredged': {
                'definition': 'Past tense of dredge; removed sediment or objects from the bottom of a body of water; brought up something from the past.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'DREJD (rhymes with "pledged")',
                'etymology': 'From Middle English "dregge," possibly from Old English. About scooping or dragging up material.',
                'language_origins': 'Middle English',
                'example_sentence': 'The harbor was _____ to remove sand and make it deep enough for large ships.',
                'memory_tip': 'Remember "DREDGED" - like a "dredge" (machine) that drags up material from underwater.'
            },
            'dreikanter': {
                'definition': 'A three-sided stone shaped by wind erosion in desert environments; a geological formation with three distinct faces.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'DRY-kan-ter (emphasis on first syllable)',
                'etymology': 'From German "drei" (three) + "Kante" (edge). Geological terminology for three-edged wind-carved rocks.',
                'language_origins': 'German',
                'example_sentence': 'The geologist found several _____ specimens in the desert, carved by centuries of wind.',
                'memory_tip': 'Think "DRY-kanter" - "dry" desert winds create rocks with three "canted" (angled) edges.'
            },
            'drewdifficulty': {
                'definition': '',
                'part_of_speech': '',
                'pronunciation_guide': '',
                'etymology': '',
                'language_origins': '',
                'example_sentence': '',
                'memory_tip': '',
                'is_error': True,
                'error_message': 'Combined word error: "drewdifficulty" appears to be "drew" + "difficulty" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
            },
            'dribbles': {
                'definition': 'Third person singular of dribble; lets liquid fall in drops; bounces a ball repeatedly while moving. Sports and liquid terminology.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'DRIB-ulz (emphasis on first syllable)',
                'etymology': 'From "drib" (variant of "drip") + "-le" + "-s." About small amounts of liquid or ball control.',
                'language_origins': 'English',
                'example_sentence': 'The basketball player _____ skillfully down the court toward the goal.',
                'memory_tip': 'Remember "DRIBbles" - like "drips" in small amounts, or bouncing a ball in small, controlled movements.'
            }
        }
        
        return batch_054_data.get(word.lower(), {})
    
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
    processor = Batch054Processor()
    success = processor.process_csv("batch_054_words.csv", "batch_054_processed.csv")
    
    if success:
        print("Batch 054 processing completed successfully!")
    else:
        print("Batch 054 processing failed!")

if __name__ == "__main__":
    main()