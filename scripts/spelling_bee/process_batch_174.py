import pandas as pd
import csv
import logging
from typing import Dict, Any
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DifficultyCalculator:
    def calculate_4_factor_difficulty(self, word: str, definition: str, etymology: str, frequency: float) -> Dict[str, Any]:
        phonetic_transparency = self._assess_phonetic_transparency(word)
        word_frequency_score = frequency
        morphology_score = self._assess_morphological_complexity(word, definition)
        etymology_score = self._assess_etymological_complexity(etymology)
        
        overall_score = (phonetic_transparency * 0.25 + word_frequency_score * 0.30 + 
                        morphology_score * 0.25 + etymology_score * 0.20)
        
        return {
            'phonetic_transparency_score': phonetic_transparency,
            'word_frequency_score': word_frequency_score,
            'morphology_score': morphology_score,
            'etymology_score': etymology_score,
            'overall_score': overall_score,
            'calculation_method': '4-factor weighted model'
        }
    
    def _assess_phonetic_transparency(self, word: str) -> float:
        if len(word) <= 4: return 1.0
        elif len(word) <= 6: return 1.5
        elif len(word) <= 8: return 2.0
        elif len(word) <= 10: return 2.5
        else: return 3.0
    
    def _assess_morphological_complexity(self, word: str, definition: str) -> float:
        complexity_score = 1.0
        if any(prefix in word.lower() for prefix in ['syn', 'tach', 'tachy', 'tab', 'tam']): complexity_score += 0.5
        if any(suffix in word.lower() for suffix in ['ism', 'ine', 'ous', 'tic', 'ate', 'acle']): complexity_score += 0.5
        if len(word) > 10: complexity_score += 0.5
        if 'technical' in definition.lower() or 'scientific' in definition.lower() or 'medical' in definition.lower(): complexity_score += 0.5
        return min(complexity_score, 4.0)
    
    def _assess_etymological_complexity(self, etymology: str) -> float:
        if 'Latin' in etymology: return 2.0
        elif 'Greek' in etymology: return 2.5
        elif 'French' in etymology: return 2.3
        elif 'German' in etymology: return 2.0
        elif 'Sanskrit' in etymology: return 3.0
        elif 'multiple' in etymology.lower(): return 3.0
        else: return 1.5

class SpellingBeeProcessor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        batch_174_data = {
            'syndactylism': {
                'definition': 'A medical condition characterized by the fusion or webbing of fingers or toes; the presence of syndactyly, where digits are joined together by skin, bone, or both.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'sin-DAK-tuh-lizm (emphasis on second syllable)',
                'etymology': 'From Greek "syn" (together) + "daktylos" (finger) + "-ism" (condition)',
                'memory_tips': 'Think "syn-dactyl-ism" - fingers stuck together condition',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The surgeon specialized in correcting _____ in newborn patients.'
            },
            'syndactylismt': {
                'definition': '[POTENTIAL ERROR] This appears to be "syndactylism" with an extra "t" at the end. This may be a typographical error in the source material.',
                'part_of_speech': 'error/variant',
                'pronunciation_guide': 'sin-DAK-tuh-lizm-t (if pronounced as written)',
                'etymology': 'Possible error of "syndactylism" (Greek origin)',
                'memory_tips': 'This appears to be a spelling error - check if it should be "syndactylism"',
                'alternate_spellings': 'syndactylism',
                'language_origin': 'Greek (with error)',
                'example_sentence': 'The word _____ may be a typographical error that needs verification.'
            },
            'syndicate': {
                'definition': 'A group of individuals or businesses combined to promote a common interest; an association of people or firms formed to undertake an enterprise; to combine into a syndicate.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'SIN-di-kit (noun), SIN-di-kayt (verb)',
                'etymology': 'From French "syndicat," from Greek "syndikos" meaning "advocate"',
                'memory_tips': 'Think "syn-dicate" - coming together to dictate or control',
                'alternate_spellings': '',
                'language_origin': 'Greek via French',
                'example_sentence': 'The newspaper _____ distributed the comic strip to hundreds of papers.'
            },
            'synecdoche': {
                'definition': 'A figure of speech in which a part is made to represent the whole or vice versa; a rhetorical device where a portion stands for the entirety.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'si-NEK-duh-kee (emphasis on second syllable)',
                'etymology': 'From Greek "synekdoche," from "syn" (together) + "ekdoche" (interpretation)',
                'memory_tips': 'Think "syn-ecdoche" - taking parts together to mean the whole',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Using "all hands on deck" is an example of _____ where hands represent people.'
            },
            'synesthesia': {
                'definition': 'A neurological phenomenon where stimulation of one sensory pathway leads to automatic experiences in a second sensory pathway; experiencing joined senses.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'sin-uhs-THEE-zhuh (emphasis on third syllable)',
                'etymology': 'From Greek "syn" (together) + "aisthesis" (sensation)',
                'memory_tips': 'Think "syn-esthesia" - senses working together',
                'alternate_spellings': 'synaesthesia',
                'language_origin': 'Greek',
                'example_sentence': 'Her _____ caused her to see colors whenever she heard music.'
            },
            'synod': {
                'definition': 'An ecclesiastical council; an assembly of clergy or church officials to discuss and decide matters of doctrine, administration, or discipline.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIN-uhd (emphasis on first syllable)',
                'etymology': 'From Greek "synodos," from "syn" (together) + "hodos" (way, path)',
                'memory_tips': 'Think "syn-od" - coming together on the same path',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The church _____ met to discuss changes to religious doctrine.'
            },
            'synonymous': {
                'definition': 'Having the same or nearly the same meaning as another word; equivalent in meaning; closely associated with or suggestive of something.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'si-NON-uh-muhs (emphasis on second syllable)',
                'etymology': 'From Greek "synonymos," from "syn" (together) + "onyma" (name)',
                'memory_tips': 'Think "syn-onymous" - same name or meaning together',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The words "happy" and "joyful" are _____ in most contexts.'
            },
            'synthetic': {
                'definition': 'Made by chemical synthesis, especially to imitate a natural product; artificial; not genuine; relating to or involving synthesis.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'sin-THET-ik (emphasis on second syllable)',
                'etymology': 'From Greek "synthetikos," from "syn" (together) + "tithenai" (to place)',
                'memory_tips': 'Think "syn-thetic" - putting elements together artificially',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ fabric was designed to mimic the properties of natural silk.'
            },
            'syntonize': {
                'definition': 'To tune to the same frequency; to bring into tune or harmony; in radio, to adjust circuits to the same frequency for optimal reception.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'SIN-tuh-nahyz (emphasis on first syllable)',
                'etymology': 'From Greek "syntonos" meaning "in tune," from "syn" (together) + "tonos" (tone)',
                'memory_tips': 'Think "syn-tonize" - bringing tones together in harmony',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The engineer had to _____ the radio frequencies to eliminate interference.'
            },
            'syntrophism': {
                'definition': 'A symbiotic relationship between different organisms where they mutually benefit from each other\'s metabolic processes; cooperative metabolism.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIN-troh-fizm (emphasis on first syllable)',
                'etymology': 'From Greek "syn" (together) + "trophe" (nourishment) + "-ism"',
                'memory_tips': 'Think "syn-troph-ism" - feeding together cooperatively',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The bacteria demonstrated _____ by sharing nutrients in their ecosystem.'
            },
            'syringe': {
                'definition': 'A medical instrument consisting of a tube and plunger for injecting or withdrawing fluids; to clean or treat with a syringe.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'suh-RINJ (emphasis on second syllable)',
                'etymology': 'From Greek "syrinx" meaning "pipe" or "tube"',
                'memory_tips': 'Think of a pipe-like tube for medical injections',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The nurse used a _____ to administer the vaccination.'
            },
            'system': {
                'definition': 'A set of connected things forming a complex whole; an organized procedure or method; a set of principles or procedures according to which something is done.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIS-tuhm (emphasis on first syllable)',
                'etymology': 'From Greek "systema," from "syn" (together) + "histanai" (to set up)',
                'memory_tips': 'Think "sys-tem" - things systematically set up together',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The school implemented a new grading _____ this semester.'
            },
            'systemt': {
                'definition': '[POTENTIAL ERROR] This appears to be "system" with an extra "t" at the end. This may be a typographical error in the source material.',
                'part_of_speech': 'error/variant',
                'pronunciation_guide': 'SIS-tuhm-t (if pronounced as written)',
                'etymology': 'Possible error of "system" (Greek origin)',
                'memory_tips': 'This appears to be a spelling error - check if it should be "system"',
                'alternate_spellings': 'system',
                'language_origin': 'Greek (with error)',
                'example_sentence': 'The word _____ may be a typographical error that needs verification.'
            },
            'syzygy': {
                'definition': 'A straight-line configuration of three celestial bodies; the alignment of three astronomical objects; in poetry, the combination of two metrical feet.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SIZ-uh-jee (emphasis on first syllable)',
                'etymology': 'From Greek "syzygia," from "syn" (together) + "zygon" (yoke)',
                'memory_tips': 'Think "syz-ygy" - celestial bodies yoked together in a line',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The solar eclipse occurred during the _____ of the sun, moon, and Earth.'
            },
            'séance': {
                'definition': 'A meeting at which people attempt to make contact with the spirits of the dead; a spiritualist gathering for communication with deceased persons.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'SAY-ahns (emphasis on first syllable)',
                'etymology': 'From French "séance," from "seoir" meaning "to sit"',
                'memory_tips': 'Think "séance" - sitting together to contact spirits',
                'alternate_spellings': 'seance',
                'language_origin': 'French',
                'example_sentence': 'The medium conducted a _____ to help the family communicate with their ancestor.'
            },
            'taal': {
                'definition': 'An Afrikaans word meaning "language"; also refers to a rhythmic pattern in Indian classical music; in South Africa, refers to language or speech.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAHL (rhymes with "hall")',
                'etymology': 'From Afrikaans "taal" meaning "language," from Dutch "taal"',
                'memory_tips': 'Think "taal" - the language people "talk" in',
                'alternate_spellings': '',
                'language_origin': 'Afrikaans/Dutch',
                'example_sentence': 'The students learned about the history of Afrikaans _____ in South Africa.'
            },
            'tabasco': {
                'definition': 'A very hot sauce made from tabasco peppers; a type of chili pepper; a pungent condiment used to add heat to food.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tuh-BAS-koh (emphasis on second syllable)',
                'etymology': 'From Tabasco, a state in Mexico where the peppers originated',
                'memory_tips': 'Think of the hot sauce that adds spice to tacos',
                'alternate_spellings': '',
                'language_origin': 'Spanish (place name)',
                'example_sentence': 'She added a few drops of _____ sauce to spice up her scrambled eggs.'
            },
            'tabernacle': {
                'definition': 'A place of worship; in Jewish history, the portable sanctuary used during the Exodus; a receptacle for the consecrated bread and wine; a temporary dwelling.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAB-er-nak-uhl (emphasis on first syllable)',
                'etymology': 'From Latin "tabernaculum," diminutive of "taberna" meaning "hut"',
                'memory_tips': 'Think "tab-ernacle" - a holy tabular structure for worship',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The ancient Israelites carried the _____ with them through the desert.'
            },
            'tabernacledifficulty': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "tabernacle" (place of worship) + "difficulty" (challenge). This is a data processing error.',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "tabernacle" and "difficulty"',
                'alternate_spellings': 'tabernacle + difficulty (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'table': {
                'definition': 'A piece of furniture with a flat top and legs; a set of facts or figures systematically displayed; to present for discussion; to postpone consideration of.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TAY-buhl (emphasis on first syllable)',
                'etymology': 'From Latin "tabula" meaning "board" or "plank"',
                'memory_tips': 'Think of a flat surface with legs for eating or working',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The family gathered around the dining _____ for their holiday meal.'
            },
            'tableau': {
                'definition': 'A group of models or motionless figures representing a scene from a story or history; a vivid or graphic description; a striking scene or picture.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAB-loh (emphasis on first syllable)',
                'etymology': 'From French "tableau," diminutive of "table"',
                'memory_tips': 'Think "table-au" - a picture arranged on a table-like scene',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The students created a _____ depicting the signing of the Declaration of Independence.'
            },
            'tablets': {
                'definition': 'Plural of tablet; flat pieces of stone, clay, or other material with writing on them; small round pieces of medicine; portable computing devices.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'TAB-lits (emphasis on first syllable)',
                'etymology': 'From Latin "tabula" (board) + "-et" diminutive suffix',
                'memory_tips': 'Think of small flat objects like medicine pills or stone tablets',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The archaeologist discovered ancient clay _____ with cuneiform writing.'
            },
            'tabulate': {
                'definition': 'To arrange data in a table or systematic form; to count or record systematically; to organize information in columns and rows.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'TAB-yuh-layt (emphasis on first syllable)',
                'etymology': 'From Latin "tabula" (table) + "-ate" suffix meaning "to make"',
                'memory_tips': 'Think "tabu-late" - to make a table of data',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The researchers needed to _____ the survey results before analyzing them.'
            },
            'tachycardia': {
                'definition': 'A medical condition characterized by a rapid heart rate, typically over 100 beats per minute; abnormally fast heartbeat.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tak-i-KAHR-dee-uh (emphasis on third syllable)',
                'etymology': 'From Greek "tachys" (fast) + "kardia" (heart)',
                'memory_tips': 'Think "tachy-cardia" - fast heart condition',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The patient was diagnosed with _____ after experiencing episodes of rapid heartbeat.'
            },
            'tachyon': {
                'definition': 'A hypothetical particle that travels faster than the speed of light; a theoretical subatomic particle with imaginary mass.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAK-ee-on (emphasis on first syllable)',
                'etymology': 'From Greek "tachys" (fast) + "-on" particle suffix',
                'memory_tips': 'Think "tachy-on" - a fast particle, faster than light',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Scientists theorize that a _____ could theoretically travel backwards in time.'
            },
            'taciturn': {
                'definition': 'Reserved or uncommunicative in speech; saying little; habitually silent; not inclined to talk.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'TAS-i-tern (emphasis on first syllable)',
                'etymology': 'From Latin "taciturnus," from "tacere" meaning "to be silent"',
                'memory_tips': 'Think "tacit-urn" - keeping quiet, not talking much',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ professor rarely spoke unless directly asked a question.'
            },
            'taco': {
                'definition': 'A Mexican dish consisting of a folded or rolled tortilla filled with various ingredients such as meat, beans, cheese, and vegetables.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAH-koh (emphasis on first syllable)',
                'etymology': 'From Mexican Spanish "taco," possibly from Nahuatl "tlahco" meaning "half"',
                'memory_tips': 'Think of a folded tortilla filled with delicious ingredients',
                'alternate_spellings': '',
                'language_origin': 'Spanish/Nahuatl',
                'example_sentence': 'She ordered a fish _____ with cabbage slaw and lime.'
            },
            'tactics': {
                'definition': 'The methods or strategies used to achieve a goal; in military contexts, the art of arranging and maneuvering forces; planned actions.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'TAK-tiks (emphasis on first syllable)',
                'etymology': 'From Greek "taktikos," from "tassein" meaning "to arrange"',
                'memory_tips': 'Think "tac-tics" - arranged techniques for achieving goals',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The coach developed new _____ to help the team win the championship.'
            },
            'tadpole': {
                'definition': 'The aquatic larval stage of a frog or toad, characterized by a tail and gills; an immature amphibian that lives in water.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAD-pohl (emphasis on first syllable)',
                'etymology': 'From Middle English "taddepol," from "tadde" (toad) + "pol" (head)',
                'memory_tips': 'Think "tad-pole" - a tiny toad with a pole-like tail',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The children watched the _____ swim around the pond before it developed legs.'
            },
            'taedium': {
                'definition': 'Weariness or boredom; tedium; the state of being tired or disgusted with something; ennui.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TEE-dee-uhm (emphasis on first syllable)',
                'etymology': 'From Latin "taedium," from "taedere" meaning "to weary"',
                'memory_tips': 'Think "tae-dium" - feeling tired and bored, similar to tedium',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The long lecture filled the students with _____ and several fell asleep.'
            },
            'tail': {
                'definition': 'The hindmost part of an animal; something resembling an animal\'s tail; to follow someone secretly; the rear part of something.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'TAYL (rhymes with "scale")',
                'etymology': 'From Old English "tægel," related to Old Norse "tagl"',
                'memory_tips': 'Think of an animal\'s rear appendage that wags or swishes',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The dog wagged its _____ excitedly when its owner came home.'
            },
            'taillight': {
                'definition': 'A red light at the rear of a vehicle; a rear lamp on a car, truck, or other vehicle used for visibility and signaling.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAYL-lahyt (emphasis on first syllable)',
                'etymology': 'Compound word: "tail" (rear part) + "light" (illumination)',
                'memory_tips': 'Compound word: tail + light - the light at the tail end of a vehicle',
                'alternate_spellings': 'tail light',
                'language_origin': 'English',
                'example_sentence': 'The broken _____ made the car unsafe to drive at night.'
            },
            'taking': {
                'definition': 'Present participle of take; the action of grasping, capturing, or accepting something; seizing or removing.',
                'part_of_speech': 'verb (present participle), noun',
                'pronunciation_guide': 'TAY-king (emphasis on first syllable)',
                'etymology': 'From Old English "tacan," from Old Norse "taka"',
                'memory_tips': 'Think of the ongoing action of grasping or accepting something',
                'alternate_spellings': '',
                'language_origin': 'Old Norse via Old English',
                'example_sentence': 'She was _____ notes during the important lecture.'
            },
            'talent': {
                'definition': 'Natural aptitude or skill; a special ability or gift; a person or people with exceptional ability; an ancient unit of weight and currency.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAL-uhnt (emphasis on first syllable)',
                'etymology': 'From Latin "talentum," from Greek "talanton" (unit of weight)',
                'memory_tips': 'Think of natural ability that makes someone talented',
                'alternate_spellings': '',
                'language_origin': 'Greek via Latin',
                'example_sentence': 'Her _____ for music was evident from a very young age.'
            },
            'tales': {
                'definition': 'Plural of tale; stories, especially those that are imaginative or fictitious; narratives or accounts of events.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'TAYLZ (rhymes with "scales")',
                'etymology': 'From Old English "talu," related to "tellan" (to tell)',
                'memory_tips': 'Think of stories being told, multiple tales',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'Grandmother entertained the children with _____ of her childhood adventures.'
            },
            'talisman': {
                'definition': 'An object believed to bring good luck or protection; a charm or amulet; something thought to have magical powers.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAL-is-muhn (emphasis on first syllable)',
                'etymology': 'From Arabic "tilasm," from Greek "telesma" meaning "religious rite"',
                'memory_tips': 'Think "talis-man" - a man who carries a magical charm',
                'alternate_spellings': '',
                'language_origin': 'Arabic via Greek',
                'example_sentence': 'The ancient _____ was believed to protect warriors in battle.'
            },
            'talk': {
                'definition': 'To speak; to communicate by speaking; to have a conversation; a speech or lecture; the action of speaking.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'TAWK (rhymes with "walk")',
                'etymology': 'From Middle English "talken," possibly related to "tale"',
                'memory_tips': 'Think of speaking words to communicate with others',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The teacher asked the students to _____ quietly during group work.'
            },
            'talking': {
                'definition': 'Present participle of talk; the action of speaking or conversing; engaged in speech or conversation.',
                'part_of_speech': 'verb (present participle), adjective',
                'pronunciation_guide': 'TAWK-ing (emphasis on first syllable)',
                'etymology': 'From "talk" + "-ing" suffix',
                'memory_tips': 'Think "talk-ing" - the ongoing action of speaking',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The children were _____ excitedly about their upcoming field trip.'
            },
            'tall': {
                'definition': 'Having great height; of above average height; extending high upward; having a specified height.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'TAWL (rhymes with "fall")',
                'etymology': 'From Old English "getæl," related to "swift" or "quick"',
                'memory_tips': 'Think of something that reaches high up, like a tall tree',
                'alternate_spellings': '',
                'language_origin': 'Old English',
                'example_sentence': 'The _____ basketball player could easily reach the top shelf.'
            },
            'tallyho': {
                'definition': 'An exclamation used in fox hunting when the fox is sighted; a hunting cry; used to express excitement or to get attention.',
                'part_of_speech': 'interjection, noun',
                'pronunciation_guide': 'tal-ee-HOH (emphasis on third syllable)',
                'etymology': 'From French "taïaut," a hunting cry',
                'memory_tips': 'Think "tally-ho" - a cry to tally or count the fox when spotted',
                'alternate_spellings': 'tally-ho',
                'language_origin': 'French',
                'example_sentence': 'The hunters shouted "____!" when they spotted the fox running across the field.'
            },
            'talons': {
                'definition': 'Plural of talon; the sharp claws of a bird of prey; claws of predatory birds used for grasping and killing prey.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'TAL-uhnz (emphasis on first syllable)',
                'etymology': 'From Old French "talon," from Latin "talus" meaning "heel"',
                'memory_tips': 'Think of sharp claws that birds use to grab their prey',
                'alternate_spellings': '',
                'language_origin': 'Latin via French',
                'example_sentence': 'The eagle\'s powerful _____ allowed it to catch fish from the lake.'
            },
            'tamarack': {
                'definition': 'A deciduous conifer tree native to northern regions; also called American larch; a tree that loses its needles in winter.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAM-uh-rak (emphasis on first syllable)',
                'etymology': 'From Algonquian, possibly Abnaki "akemantak"',
                'memory_tips': 'Think "tama-rack" - a tree you might see on a hiking rack or trail',
                'alternate_spellings': '',
                'language_origin': 'Algonquian',
                'example_sentence': 'The _____ trees turned golden yellow before losing their needles in autumn.'
            },
            'tamari': {
                'definition': 'A type of soy sauce made without wheat; a Japanese condiment similar to soy sauce but with a richer, smoother flavor.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tuh-MAH-ree (emphasis on second syllable)',
                'etymology': 'From Japanese "tamari," from "tamaru" meaning "to accumulate"',
                'memory_tips': 'Think "tama-ri" - a Japanese sauce that accumulates rich flavor',
                'alternate_spellings': '',
                'language_origin': 'Japanese',
                'example_sentence': 'The chef used _____ instead of regular soy sauce for its deeper flavor.'
            },
            'tamarisk': {
                'definition': 'A shrub or small tree with tiny scale-like leaves and clusters of small pink flowers; a plant that grows in salt marshes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAM-uh-risk (emphasis on first syllable)',
                'etymology': 'From Latin "tamariscus," possibly from a Semitic language',
                'memory_tips': 'Think "tamar-isk" - a plant that might grow at risk near salt water',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ bushes created a natural windbreak along the sandy coastline.'
            },
            'tambour': {
                'definition': 'A small drum; a circular frame for holding fabric taut during embroidery; the wall of a circular building.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAM-boor (emphasis on first syllable)',
                'etymology': 'From French "tambour," from Arabic "tanbur" (drum)',
                'memory_tips': 'Think "tam-bour" - a drum that makes a "boom" sound',
                'alternate_spellings': '',
                'language_origin': 'Arabic via French',
                'example_sentence': 'The embroiderer stretched the fabric tightly across the _____ frame.'
            },
            'tambourine': {
                'definition': 'A percussion instrument consisting of a shallow circular frame with metal discs around the edge; a handheld drum with jingles.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'tam-buh-REEN (emphasis on third syllable)',
                'etymology': 'From French "tambourin," diminutive of "tambour" (drum)',
                'memory_tips': 'Think "tambour-ine" - a small drum with jingles',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'She shook the _____ to add rhythm to the folk song.'
            },
            'tamid': {
                'definition': 'In Judaism, referring to the perpetual or continual sacrifice; something that is constant or ongoing; eternal or continuous.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'tah-MEED (emphasis on second syllable)',
                'etymology': 'From Hebrew "tamid" meaning "continual" or "perpetual"',
                'memory_tips': 'Think "ta-mid" - something that continues in the middle of everything',
                'alternate_spellings': '',
                'language_origin': 'Hebrew',
                'example_sentence': 'The _____ offering was performed twice daily in the ancient Temple.'
            },
            'tampered': {
                'definition': 'Past tense of tamper; interfered with something in order to damage or make unauthorized changes; meddled with.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'TAM-perd (emphasis on first syllable)',
                'etymology': 'From "tamper," possibly from "temper" meaning "to mix"',
                'memory_tips': 'Think "tamp-ered" - someone pressed down and messed with something',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The evidence showed that someone had _____ with the lock.'
            },
            'tamworth': {
                'definition': 'A breed of domestic pig; a reddish-brown pig originally from Tamworth, England; also refers to the English town.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAM-werth (emphasis on first syllable)',
                'etymology': 'Named after Tamworth, a town in Staffordshire, England',
                'memory_tips': 'Think "Tam-worth" - a pig breed worth its weight from the town of Tam',
                'alternate_spellings': '',
                'language_origin': 'English (place name)',
                'example_sentence': 'The farmer raised _____ pigs known for their excellent bacon quality.'
            },
            'tanager': {
                'definition': 'A brightly colored songbird found in the Americas; a bird known for its vibrant plumage, especially the males.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'TAN-uh-jer (emphasis on first syllable)',
                'etymology': 'From Tupi "tangara," a South American bird name',
                'memory_tips': 'Think "tan-ager" - a bird that might have tan colors as it ages',
                'alternate_spellings': '',
                'language_origin': 'Tupi (South American indigenous)',
                'example_sentence': 'The bright red _____ perched on the branch was a beautiful sight.'
            }
        }
        
        return batch_174_data.get(word, {
            'definition': f'[WORD NOT FOUND: {word}] This word was not found in the comprehensive data set.',
            'part_of_speech': 'unknown',
            'pronunciation_guide': f'[PRONUNCIATION NOT AVAILABLE FOR {word.upper()}]',
            'etymology': f'[ETYMOLOGY NOT AVAILABLE FOR {word}]',
            'memory_tips': f'[MEMORY TIPS NOT AVAILABLE FOR {word}]',
            'alternate_spellings': '',
            'language_origin': 'unknown',
            'example_sentence': f'The word _____ requires further research for proper definition.'
        })

    def detect_combined_words(self, word: str) -> bool:
        combined_word_indicators = [
            len(word) > 15,  # Unusually long
            word.count('tion') > 1,  # Multiple common endings
            word.count('ing') > 1,
            word.count('ed') > 1,
        ]
        
        known_combined_errors = [
            'syndactylismt',  # syndactylism + t
            'systemt',  # system + t
            'tabernacledifficulty'  # tabernacle + difficulty
        ]
        
        return any(combined_word_indicators) or word in known_combined_errors

    def process_batch_174(self):
        input_file = 'output/batch_174_words.csv'
        output_file = 'output/batch_174_processed.csv'
        
        logging.info("Processing Batch 174 with comprehensive Claude data...")
        
        # Read input CSV
        df = pd.read_csv(input_file)
        processed_words = []
        successful_count = 0
        failed_count = 0
        combined_errors = []
        
        for _, row in df.iterrows():
            word = row['word']
            
            try:
                # Get comprehensive Claude data
                claude_data = self.get_comprehensive_claude_data(word)
                
                # Detect combined word errors
                is_combined = self.detect_combined_words(word)
                if is_combined:
                    combined_errors.append(f"{word}: Combined word error")
                
                # Extract source information
                source_difficulties = row['source_difficulties']
                years = row['years']
                
                # Map source difficulty to frequency score
                frequency_map = {"One Bee": 1.0, "Two Bee": 2.0, "Three Bee": 3.0}
                frequency_scores = [frequency_map.get(diff.strip(), 2.0) for diff in source_difficulties.split(';')]
                avg_frequency = sum(frequency_scores) / len(frequency_scores)
                
                # Calculate 4-factor difficulty but leave final difficulty assignments null
                difficulty_data = self.difficulty_calc.calculate_4_factor_difficulty(
                    word, claude_data['definition'], claude_data['etymology'], avg_frequency
                )
                
                processed_word = {
                    'word': word,
                    'definition': claude_data['definition'],
                    'example_sentence': claude_data['example_sentence'],
                    'source_difficulty': source_difficulties,
                    'difficulty_level': '',  # Leave null as requested
                    'difficulty_name': '',   # Leave null as requested
                    'ai_difficulty_level': '',  # Leave null as requested
                    'ai_difficulty_name': '',   # Leave null as requested
                    'phonetic_transparency_score': difficulty_data['phonetic_transparency_score'],
                    'word_frequency_score': difficulty_data['word_frequency_score'],
                    'morphology_score': difficulty_data['morphology_score'],
                    'etymology_score': difficulty_data['etymology_score'],
                    'difficulty_calculation_method': f"{difficulty_data['calculation_method']} (overall_score: {difficulty_data['overall_score']:.2f})",
                    'part_of_speech': claude_data['part_of_speech'],
                    'pronunciation_guide': claude_data['pronunciation_guide'],
                    'etymology': claude_data['etymology'],
                    'etymology_source': 'Claude',
                    'memory_tips': claude_data['memory_tips'],
                    'alternate_spellings': claude_data['alternate_spellings'],
                    'language_origin': claude_data['language_origin'],
                    'definition_source': 'Claude',
                    'source_names': 'Scripps National Spelling Bee',
                    'source_difficulties': source_difficulties,
                    'frequency': avg_frequency,
                    'original_source': f'Scripps National Spelling Bee Words of the Champions ({years})',
                    'source_access_date': '2025-08-19'
                }
                
                processed_words.append(processed_word)
                successful_count += 1
                logging.info(f"Processed word: {word}")
                
            except Exception as e:
                logging.error(f"Error processing word '{word}': {str(e)}")
                failed_count += 1
        
        # Save to CSV
        output_df = pd.DataFrame(processed_words)
        output_df.to_csv(output_file, index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)
        
        logging.info(f"Saved {len(processed_words)} words to {output_file}")
        logging.info("Batch 174 processing completed!")
        logging.info(f"Processed {successful_count} words with comprehensive Claude data")
        logging.info(f"Output saved to: {output_file}")
        logging.info(f"Results: {successful_count} successful, {failed_count} failed")
        logging.info(f"Combined word errors detected and flagged: {len(combined_errors)}")
        
        if combined_errors:
            logging.info("Combined word errors flagged:")
            for error in combined_errors:
                logging.info(f"  - {error}")

if __name__ == "__main__":
    processor = SpellingBeeProcessor()
    processor.process_batch_174()