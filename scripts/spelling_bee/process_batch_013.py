#!/usr/bin/env python3
import csv
import logging
from dataclasses import dataclass
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class WordData:
    word: str
    definition: str
    example_sentence: str
    source_difficulty: str
    difficulty_level: str = ""
    difficulty_name: str = ""
    ai_difficulty_level: str = ""
    ai_difficulty_name: str = ""
    phonetic_transparency_score: float = 0.0
    word_frequency_score: float = 0.0
    morphology_score: float = 0.0
    etymology_score: float = 0.0
    difficulty_calculation_method: str = ""
    part_of_speech: str = ""
    pronunciation_guide: str = ""
    etymology: str = ""
    etymology_source: str = "Claude"
    memory_tips: str = ""
    alternate_spellings: str = ""
    language_origin: str = ""
    definition_source: str = "Claude"
    source_names: str = "Scripps National Spelling Bee"
    source_difficulties: str = ""
    frequency: float = 0.0
    original_source: str = ""
    source_access_date: str = "2025-08-19"

class DifficultyCalculator:
    @staticmethod
    def calculate_phonetic_transparency(word: str) -> float:
        # Scoring based on how phonetically transparent the spelling is
        irregular_patterns = ['ough', 'augh', 'eigh', 'ph', 'gh', 'tion', 'sion', 'ious', 'eous']
        silent_letters = ['k', 'b', 'l', 'w', 'h']
        
        score = 1.0  # Start with most transparent
        
        # Check for irregular patterns
        for pattern in irregular_patterns:
            if pattern in word.lower():
                score += 1.0
        
        # Check for silent letters in common positions
        word_lower = word.lower()
        if word_lower.startswith('k') and len(word) > 1:  # knight, knee
            score += 1.0
        if 'mb' in word_lower:  # thumb, lamb
            score += 1.0
        if word_lower.endswith('l') and 'lk' in word_lower:  # walk, talk
            score += 1.0
            
        return min(score, 4.0)
    
    @staticmethod
    def calculate_word_frequency(word: str) -> float:
        # Based on common English word frequency
        common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use']
        
        word_lower = word.lower()
        if word_lower in common_words:
            return 1.0
        elif len(word) <= 4:
            return 2.0
        elif len(word) <= 7:
            return 3.0
        else:
            return 4.0
    
    @staticmethod
    def calculate_morphology_complexity(word: str) -> float:
        # Based on morphological complexity
        prefixes = ['un', 'pre', 'dis', 'mis', 're', 'over', 'under', 'out', 'up', 'non', 'anti', 'de', 'en', 'em', 'fore', 'in', 'im', 'il', 'ir', 'inter', 'mid', 'sub', 'super', 'trans', 'semi', 'auto', 'co', 'counter', 'extra', 'hyper', 'mega', 'micro', 'mini', 'multi', 'over', 'post', 'proto', 'pseudo', 'tele', 'ultra']
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment', 'able', 'ible', 'ful', 'less', 'ous', 'eous', 'ious', 'al', 'ial', 'ic', 'ive', 'ism', 'ist', 'ize', 'ise', 'age', 'ity', 'ward', 'wise']
        
        score = 1.0
        word_lower = word.lower()
        
        # Check for prefixes
        for prefix in prefixes:
            if word_lower.startswith(prefix):
                score += 0.5
                break
        
        # Check for suffixes
        for suffix in suffixes:
            if word_lower.endswith(suffix):
                score += 0.5
                break
        
        # Multiple morphemes
        if score > 2.0:
            score += 1.0
            
        return min(score, 4.0)
    
    @staticmethod
    def calculate_etymology_complexity(language_origin: str) -> float:
        # Based on language origin complexity for English speakers
        if language_origin.lower() in ['english', 'anglo-saxon', 'germanic']:
            return 1.0
        elif language_origin.lower() in ['french', 'latin']:
            return 2.0
        elif language_origin.lower() in ['greek', 'spanish', 'italian']:
            return 3.0
        else:
            return 4.0
    
    @staticmethod
    def calculate_overall_difficulty(phonetic: float, frequency: float, morphology: float, etymology: float) -> float:
        # Weighted average: phonetic (30%), frequency (25%), morphology (25%), etymology (20%)
        return (phonetic * 0.3 + frequency * 0.25 + morphology * 0.25 + etymology * 0.2)

class Batch013Processor:
    def __init__(self):
        self.word_data = {
            "asgard": {
                "definition": "In Norse mythology, the realm of the gods (Æsir), connected to Earth by the rainbow bridge Bifrost.",
                "example_sentence": "In Norse legends, warriors who died bravely would journey to _____ to feast with the gods.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AZ-gard (emphasis on first syllable)",
                "etymology": "From Old Norse 'Ásgarðr', from 'áss' (god) + 'garðr' (enclosure, yard)",
                "memory_tips": "Think 'As-gard' - the guarded realm of the gods (As/Æsir)",
                "language_origin": "Old Norse"
            },
            "asiago": {
                "definition": "A type of Italian cheese, named after the Asiago plateau, available in fresh and aged varieties.",
                "example_sentence": "The chef grated fresh _____ cheese over the warm pasta dish.",
                "part_of_speech": "noun",
                "pronunciation_guide": "ah-see-AH-go (emphasis on third syllable)",
                "etymology": "From Asiago, a town and plateau in the Veneto region of Italy",
                "memory_tips": "Think 'Asiago' - the Italian town famous for its distinctive cheese",
                "language_origin": "Italian"
            },
            "asiagoaspish": {
                "definition": "COMBINED WORD ERROR - appears to be 'asiago' + 'aspish' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "asiatic": {
                "definition": "Relating to Asia or its peoples; sometimes considered outdated, with 'Asian' being preferred.",
                "example_sentence": "The museum featured an extensive collection of _____ art and artifacts.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "ay-shee-AT-ik (emphasis on third syllable)",
                "etymology": "From Latin 'Asiaticus', from Greek 'Asiatikos'",
                "memory_tips": "Think 'Asiatic' - relating to the continent of Asia",
                "language_origin": "Latin"
            },
            "asked": {
                "definition": "Past tense of ask; requested information or made an inquiry; invited or requested.",
                "example_sentence": "She _____ the teacher to explain the difficult concept again.",
                "part_of_speech": "verb",
                "pronunciation_guide": "ASKT (single syllable)",
                "etymology": "From Old English 'ascian', related to Germanic 'aiskōną'",
                "memory_tips": "Think 'asked' - simple past form of making a request",
                "language_origin": "Old English"
            },
            "asmanian": {
                "definition": "Relating to Tasmania (informal variant); pertaining to the island state of Australia.",
                "example_sentence": "The _____ devil is a unique marsupial found only on that island.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "az-MAY-nee-un (emphasis on second syllable)",
                "etymology": "Variant of 'Tasmanian', from Tasmania (named after Abel Tasman)",
                "memory_tips": "Think 'Asmanian' - variant form relating to Tasmania",
                "language_origin": "English"
            },
            "asparagus": {
                "definition": "A green vegetable with long, tender spears; a plant cultivated for its edible shoots.",
                "example_sentence": "The dinner featured grilled _____ drizzled with lemon and olive oil.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-SPAR-uh-gus (emphasis on second syllable)",
                "etymology": "From Latin 'asparagus', from Greek 'asparagos'",
                "memory_tips": "Think 'asparagus' - the spear-like green vegetable",
                "language_origin": "Greek"
            },
            "aspersions": {
                "definition": "Harsh or unfair criticisms; attacks on someone's reputation or character.",
                "example_sentence": "The candidate refused to cast _____ on his opponent's character.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-SPUR-zhunz (emphasis on second syllable)",
                "etymology": "From Latin 'aspersio', from 'aspergere' (to sprinkle, splash)",
                "memory_tips": "Think 'aspersions' - splashing criticism like water",
                "language_origin": "Latin"
            },
            "asphyxiate": {
                "definition": "To kill or make unconscious by depriving of oxygen; to suffocate.",
                "example_sentence": "The toxic fumes could _____ anyone trapped in the sealed room.",
                "part_of_speech": "verb",
                "pronunciation_guide": "as-FIK-see-ayt (emphasis on second syllable)",
                "etymology": "From Greek 'asphyxia', from 'a-' (without) + 'sphyxis' (pulse)",
                "memory_tips": "Think 'a-sphyxiate' - without pulse, deprived of oxygen",
                "language_origin": "Greek"
            },
            "aspidistra": {
                "definition": "A hardy houseplant with broad, dark green leaves, popular in Victorian times.",
                "example_sentence": "The Victorian parlor featured a large _____ in a decorative ceramic pot.",
                "part_of_speech": "noun",
                "pronunciation_guide": "as-puh-DIS-truh (emphasis on third syllable)",
                "etymology": "From Greek 'aspidistos', from 'aspis' (shield) referring to leaf shape",
                "memory_tips": "Think 'aspidistra' - the shield-shaped (aspis) leafed plant",
                "language_origin": "Greek"
            },
            "aspirate": {
                "definition": "To breathe in; to pronounce with a breath of air; to remove fluid from the body with suction.",
                "example_sentence": "The doctor needed to _____ fluid from the patient's lungs.",
                "part_of_speech": "verb/noun",
                "pronunciation_guide": "AS-puh-rayt (emphasis on first syllable)",
                "etymology": "From Latin 'aspirare', from 'ad-' (to) + 'spirare' (to breathe)",
                "memory_tips": "Think 'aspirate' - to breathe toward or draw in air",
                "language_origin": "Latin"
            },
            "aspirin": {
                "definition": "A common pain-relieving and anti-inflammatory medication; acetylsalicylic acid.",
                "example_sentence": "She took an _____ to relieve her headache and reduce the fever.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AS-pur-in (emphasis on first syllable)",
                "etymology": "From 'a-' + 'spir' (from spiraea, meadowsweet plant) + '-in'",
                "memory_tips": "Think 'aspirin' - derived from the spiraea plant for pain relief",
                "language_origin": "Modern Latin"
            },
            "aspish": {
                "definition": "Resembling or characteristic of an asp (venomous snake); snake-like in malice or danger.",
                "example_sentence": "Her _____ glare warned others to keep their distance.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "AS-pish (emphasis on first syllable)",
                "etymology": "From 'asp' (venomous snake) + '-ish' (having the quality of)",
                "memory_tips": "Think 'asp-ish' - like a dangerous snake in character",
                "language_origin": "English"
            },
            "assailant": {
                "definition": "A person who attacks another physically or verbally; an aggressor.",
                "example_sentence": "The victim was unable to identify her _____ in the police lineup.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-SAY-lunt (emphasis on second syllable)",
                "etymology": "From French 'assaillant', from 'assaillir' (to attack)",
                "memory_tips": "Think 'assailant' - one who assails or attacks others",
                "language_origin": "French"
            },
            "assam": {
                "definition": "A state in northeastern India; a type of black tea grown in this region.",
                "example_sentence": "The afternoon tea service featured a robust _____ blend with milk and sugar.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-SAHM (emphasis on second syllable)",
                "etymology": "From Sanskrit 'asama' meaning 'unequaled, peerless'",
                "memory_tips": "Think 'Assam' - the unequaled region famous for strong tea",
                "language_origin": "Sanskrit"
            },
            "assassinate": {
                "definition": "To murder a prominent person for political or religious motives; to kill by sudden attack.",
                "example_sentence": "The conspiracy aimed to _____ the political leader during the public ceremony.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-SAS-uh-nayt (emphasis on second syllable)",
                "etymology": "From Arabic 'hashishin' (hashish users), referring to a sect of killers",
                "memory_tips": "Think 'assassinate' - from the hashish-using killers of medieval times",
                "language_origin": "Arabic"
            },
            "assemblage": {
                "definition": "A collection of things or people; an artistic work made from fragments or junk.",
                "example_sentence": "The artist's _____ combined metal scraps and found objects into stunning sculptures.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-SEM-blij (emphasis on second syllable)",
                "etymology": "From French 'assemblage', from 'assembler' (to assemble)",
                "memory_tips": "Think 'assemblage' - things assembled together into a collection",
                "language_origin": "French"
            },
            "assembly": {
                "definition": "A group of people gathered together; the action of fitting together parts of a machine.",
                "example_sentence": "The school _____ featured a presentation about environmental conservation.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-SEM-blee (emphasis on second syllable)",
                "etymology": "From Old French 'assemblee', from 'assembler' (to bring together)",
                "memory_tips": "Think 'assembly' - people assembled or brought together",
                "language_origin": "French"
            },
            "assiduous": {
                "definition": "Showing great care and perseverance; diligent and persistent in effort.",
                "example_sentence": "Her _____ study habits helped her excel in the challenging course.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "uh-SID-yoo-us (emphasis on second syllable)",
                "etymology": "From Latin 'assiduus', from 'assidere' (to sit by, attend to)",
                "memory_tips": "Think 'assiduous' - sitting by your work, constantly attending to it",
                "language_origin": "Latin"
            },
            "assiduousdiligence": {
                "definition": "COMBINED WORD ERROR - appears to be 'assiduous' + 'diligence' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "assimilation": {
                "definition": "The process of absorbing and integrating ideas, culture, or people into a larger group.",
                "example_sentence": "The _____ of immigrants into American society has been a continuous process.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-sim-uh-LAY-shun (emphasis on fourth syllable)",
                "etymology": "From Latin 'assimilare', from 'ad-' (to) + 'similis' (like, similar)",
                "memory_tips": "Think 'assimilation' - making similar to or like the existing group",
                "language_origin": "Latin"
            },
            "assistance": {
                "definition": "Help or support given to someone; aid in accomplishing a task or goal.",
                "example_sentence": "The elderly man required _____ with carrying his heavy groceries.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-SIS-tunts (emphasis on second syllable)",
                "etymology": "From Latin 'assistere', from 'ad-' (to) + 'sistere' (to stand)",
                "memory_tips": "Think 'assistance' - standing by someone to help them",
                "language_origin": "Latin"
            },
            "assizes": {
                "definition": "Historical court sessions held periodically in English counties; legal proceedings or judgments.",
                "example_sentence": "The criminal was tried at the county _____ and sentenced accordingly.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-SYZ-iz (emphasis on second syllable)",
                "etymology": "From Old French 'assise', from 'asseoir' (to sit, settle)",
                "memory_tips": "Think 'assizes' - court sessions where judges sit to hear cases",
                "language_origin": "French"
            },
            "associated": {
                "definition": "Connected or linked with something else; joined in partnership or cooperation.",
                "example_sentence": "The symptoms were _____ with the patient's underlying medical condition.",
                "part_of_speech": "adjective/verb",
                "pronunciation_guide": "uh-SOH-see-ay-tid (emphasis on third syllable)",
                "etymology": "From Latin 'associare', from 'ad-' (to) + 'socius' (companion)",
                "memory_tips": "Think 'associated' - joined with companions or partners",
                "language_origin": "Latin"
            },
            "association": {
                "definition": "An organization of people with a common purpose; a mental connection between ideas or experiences.",
                "example_sentence": "The professional _____ provided training and networking opportunities for members.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-soh-see-AY-shun (emphasis on fourth syllable)",
                "etymology": "From Latin 'associare', from 'ad-' (to) + 'socius' (companion)",
                "memory_tips": "Think 'association' - people joining together as companions",
                "language_origin": "Latin"
            },
            "assuage": {
                "definition": "To make less intense; to satisfy or relieve; to calm or pacify.",
                "example_sentence": "The mother's gentle words helped _____ her child's fears about the first day of school.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-SWAYJ (emphasis on second syllable)",
                "etymology": "From Old French 'assuagier', from Latin 'ad-' (to) + 'suavis' (sweet)",
                "memory_tips": "Think 'assuage' - making something sweet or gentle to relieve pain",
                "language_origin": "Latin"
            },
            "assumed": {
                "definition": "Supposed to be true without proof; taken on or adopted; pretended or false.",
                "example_sentence": "The detective questioned the witness's _____ identity and requested verification.",
                "part_of_speech": "adjective/verb",
                "pronunciation_guide": "uh-SOOMD (emphasis on second syllable)",
                "etymology": "From Latin 'assumere', from 'ad-' (to) + 'sumere' (to take)",
                "memory_tips": "Think 'assumed' - taken to be true without proof",
                "language_origin": "Latin"
            },
            "assumption": {
                "definition": "Something accepted as true without proof; the action of taking on responsibility or control.",
                "example_sentence": "Her _____ that everyone would attend proved to be incorrect.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-SUMP-shun (emphasis on second syllable)",
                "etymology": "From Latin 'assumptio', from 'assumere' (to take up)",
                "memory_tips": "Think 'assumption' - taking up an idea as true without proof",
                "language_origin": "Latin"
            },
            "assure": {
                "definition": "To tell someone confidently that something is true; to guarantee or make certain.",
                "example_sentence": "The doctor tried to _____ the patient that the surgery would be successful.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-SHUR (emphasis on second syllable)",
                "etymology": "From Old French 'asseurer', from Latin 'ad-' + 'securus' (secure)",
                "memory_tips": "Think 'assure' - making someone feel secure about something",
                "language_origin": "Latin"
            },
            "astaxanthin": {
                "definition": "A red pigment found in marine animals and algae, with antioxidant properties.",
                "example_sentence": "The supplement contained _____ derived from algae for its antioxidant benefits.",
                "part_of_speech": "noun",
                "pronunciation_guide": "as-tuh-ZAN-thin (emphasis on third syllable)",
                "etymology": "From Greek 'astakos' (lobster) + 'xanthin' (yellow pigment)",
                "memory_tips": "Think 'astaxanthin' - the yellow pigment from lobsters (astakos)",
                "language_origin": "Greek"
            },
            "asterion": {
                "definition": "An anatomical point on the skull where three bones meet; a cranial landmark.",
                "example_sentence": "The forensic anthropologist located the _____ to help identify the skull.",
                "part_of_speech": "noun",
                "pronunciation_guide": "as-TEER-ee-on (emphasis on second syllable)",
                "etymology": "From Greek 'asterion', from 'aster' (star)",
                "memory_tips": "Think 'asterion' - a star-like point where skull bones meet",
                "language_origin": "Greek"
            },
            "asterisk": {
                "definition": "A symbol (*) used in printing and writing to mark footnotes or indicate omissions.",
                "example_sentence": "The footnote was marked with an _____ at the bottom of the page.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AS-tuh-risk (emphasis on first syllable)",
                "etymology": "From Greek 'asteriskos', diminutive of 'aster' (star)",
                "memory_tips": "Think 'asterisk' - a little star (*) symbol",
                "language_origin": "Greek"
            },
            "asthmatic": {
                "definition": "Relating to or suffering from asthma; characterized by difficulty breathing.",
                "example_sentence": "The _____ child always carried an inhaler during physical activities.",
                "part_of_speech": "adjective/noun",
                "pronunciation_guide": "az-MAT-ik (emphasis on second syllable)",
                "etymology": "From Greek 'asthma', from 'azein' (to breathe hard)",
                "memory_tips": "Think 'asthmatic' - having trouble breathing hard",
                "language_origin": "Greek"
            },
            "astigmatism": {
                "definition": "A vision condition where the eye doesn't focus light evenly, causing blurred vision.",
                "example_sentence": "The optometrist diagnosed her _____ and prescribed corrective lenses.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-STIG-muh-tizm (emphasis on second syllable)",
                "etymology": "From Greek 'a-' (without) + 'stigma' (point, mark)",
                "memory_tips": "Think 'a-stigmatism' - without a clear focal point",
                "language_origin": "Greek"
            },
            "astilbe": {
                "definition": "A flowering plant with feathery plumes, popular in shade gardens.",
                "example_sentence": "The _____ added delicate pink and white blooms to the shaded garden border.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-STIL-bee (emphasis on second syllable)",
                "etymology": "From Greek 'a-' (not) + 'stilbe' (glittering), referring to small flowers",
                "memory_tips": "Think 'a-stilbe' - flowers that don't glitter individually but form beautiful plumes",
                "language_origin": "Greek"
            },
            "astonish": {
                "definition": "To surprise greatly; to fill with wonder; to amaze or astound.",
                "example_sentence": "The magician's final trick never failed to _____ the audience.",
                "part_of_speech": "verb",
                "pronunciation_guide": "uh-STON-ish (emphasis on second syllable)",
                "etymology": "From Old French 'estoner', from Latin 'ex-' + 'tonare' (to thunder)",
                "memory_tips": "Think 'astonish' - to strike like thunder, leaving someone amazed",
                "language_origin": "Latin"
            },
            "astonishment": {
                "definition": "Great surprise or amazement; the feeling of being astonished.",
                "example_sentence": "To everyone's _____, the quiet student gave the most eloquent speech.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-STON-ish-munt (emphasis on second syllable)",
                "etymology": "From Old French 'estoner', from Latin 'ex-' + 'tonare' (to thunder)",
                "memory_tips": "Think 'astonishment' - the state of being struck by thunder-like surprise",
                "language_origin": "Latin"
            },
            "astounding": {
                "definition": "Extremely surprising or impressive; causing amazement or wonder.",
                "example_sentence": "The athlete's _____ performance broke three world records in one day.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "uh-STOW-ding (emphasis on second syllable)",
                "etymology": "From 'astound', from 'astonish' with influence from 'confound'",
                "memory_tips": "Think 'astounding' - so amazing it leaves you astounded",
                "language_origin": "English"
            },
            "astral": {
                "definition": "Relating to stars or outer space; in some beliefs, relating to a spiritual realm.",
                "example_sentence": "The ancient astronomers studied _____ movements to predict earthly events.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "AS-trul (emphasis on first syllable)",
                "etymology": "From Latin 'astralis', from 'astrum' (star)",
                "memory_tips": "Think 'astral' - relating to stars (astrum) and celestial bodies",
                "language_origin": "Latin"
            },
            "astrayliquid": {
                "definition": "COMBINED WORD ERROR - appears to be 'astray' + 'liquid' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            },
            "astride": {
                "definition": "With one leg on each side of something; spanning or extending across.",
                "example_sentence": "The cowboy sat _____ his horse, surveying the vast prairie ahead.",
                "part_of_speech": "adverb/preposition",
                "pronunciation_guide": "uh-STRYD (emphasis on second syllable)",
                "etymology": "From 'a-' (on) + 'stride'",
                "memory_tips": "Think 'astride' - taking a stride across something, legs on each side",
                "language_origin": "English"
            },
            "astringent": {
                "definition": "Causing tissues to contract; harsh or severe in manner; a substance that tightens skin.",
                "example_sentence": "The _____ lotion helped tighten her pores and reduce oiliness.",
                "part_of_speech": "adjective/noun",
                "pronunciation_guide": "uh-STRIN-junt (emphasis on second syllable)",
                "etymology": "From Latin 'astringere', from 'ad-' (to) + 'stringere' (to bind tight)",
                "memory_tips": "Think 'astringent' - binding tight, causing contraction",
                "language_origin": "Latin"
            },
            "astrobleme": {
                "definition": "A scar on Earth's surface caused by meteorite impact; an ancient impact crater.",
                "example_sentence": "Geologists study each _____ to understand the history of meteorite impacts on Earth.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AS-troh-bleem (emphasis on first syllable)",
                "etymology": "From Greek 'astron' (star) + 'blema' (wound, throw)",
                "memory_tips": "Think 'astro-bleme' - a wound from the stars (meteorites)",
                "language_origin": "Greek"
            },
            "astrologer": {
                "definition": "A person who studies astrology and makes predictions based on celestial positions.",
                "example_sentence": "The _____ claimed to predict the future based on planetary alignments.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-STROL-uh-jur (emphasis on second syllable)",
                "etymology": "From Greek 'astron' (star) + 'logos' (study) + '-er'",
                "memory_tips": "Think 'astrologer' - one who studies the stars to make predictions",
                "language_origin": "Greek"
            },
            "astronaut": {
                "definition": "A person trained to travel and work in space; a space traveler.",
                "example_sentence": "The _____ conducted experiments during the six-month mission to the space station.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AS-truh-nawt (emphasis on first syllable)",
                "etymology": "From Greek 'astron' (star) + 'nautes' (sailor)",
                "memory_tips": "Think 'astronaut' - a sailor among the stars",
                "language_origin": "Greek"
            },
            "astur": {
                "definition": "A genus of hawks; relating to birds of prey in the hawk family.",
                "example_sentence": "The _____ goshawk is a powerful predator found in many forest regions.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AS-tur (emphasis on first syllable)",
                "etymology": "From Latin 'astur', possibly from 'accipiter' (hawk)",
                "memory_tips": "Think 'astur' - a type of swift and powerful hawk",
                "language_origin": "Latin"
            },
            "astute": {
                "definition": "Having the ability to accurately assess situations; shrewd and perceptive.",
                "example_sentence": "Her _____ business sense helped her identify profitable investment opportunities.",
                "part_of_speech": "adjective",
                "pronunciation_guide": "uh-STOOT (emphasis on second syllable)",
                "etymology": "From Latin 'astutus', from 'astus' (craft, cunning)",
                "memory_tips": "Think 'astute' - having cunning craft in understanding situations",
                "language_origin": "Latin"
            },
            "asura": {
                "definition": "In Hindu and Buddhist mythology, a class of divine beings or demons opposed to the gods.",
                "example_sentence": "The ancient texts describe battles between the gods and the powerful _____.",
                "part_of_speech": "noun",
                "pronunciation_guide": "AH-soo-rah (emphasis on first syllable)",
                "etymology": "From Sanskrit 'asura', from 'asu' (breath, life)",
                "memory_tips": "Think 'asura' - powerful beings with divine breath or life force",
                "language_origin": "Sanskrit"
            },
            "asylee": {
                "definition": "A person who has been granted asylum; someone given protection in a foreign country.",
                "example_sentence": "The _____ was grateful for the safety and opportunities in her new country.",
                "part_of_speech": "noun",
                "pronunciation_guide": "uh-SYE-lee (emphasis on third syllable)",
                "etymology": "From 'asylum' + '-ee' (one who receives)",
                "memory_tips": "Think 'asylee' - one who receives asylum or protection",
                "language_origin": "English"
            },
            "asyleeatrabilious": {
                "definition": "COMBINED WORD ERROR - appears to be 'asylee' + 'atrabilious' incorrectly joined",
                "example_sentence": "ERROR: This appears to be two words incorrectly combined.",
                "part_of_speech": "ERROR",
                "pronunciation_guide": "ERROR - combined word",
                "etymology": "ERROR - this appears to be a data extraction error",
                "memory_tips": "FLAG: This is a combined word error that needs manual review",
                "language_origin": "ERROR"
            }
        }
        
        # Combined word errors detected in this batch
        self.combined_word_errors = [
            "asiagoaspish",
            "assiduousdiligence", 
            "astrayliquid",
            "asyleeatrabilious"
        ]

    def process_batch(self, input_file: str, output_file: str):
        """Process the batch CSV file and generate comprehensive data"""
        logger.info(f"Starting processing of {input_file}")
        
        words_processed = []
        
        # Read input file
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                input_words = list(reader)
                
        except Exception as e:
            logger.error(f"Error reading input file: {e}")
            return
        
        # Process each word
        for row in input_words:
            word = row['word'].strip()
            if not word:  # Skip empty rows
                continue
                
            logger.info(f"Processing word: {word}")
            
            # Get word data
            if word in self.word_data:
                data = self.word_data[word]
                
                # Calculate difficulty scores
                calc = DifficultyCalculator()
                phonetic_score = calc.calculate_phonetic_transparency(word)
                frequency_score = calc.calculate_word_frequency(word)
                morphology_score = calc.calculate_morphology_complexity(word)
                etymology_score = calc.calculate_etymology_complexity(data['language_origin'])
                overall_score = calc.calculate_overall_difficulty(phonetic_score, frequency_score, morphology_score, etymology_score)
                
                # Create word data object
                word_obj = WordData(
                    word=word,
                    definition=data['definition'],
                    example_sentence=data['example_sentence'],
                    source_difficulty=row['source_difficulties'],
                    phonetic_transparency_score=phonetic_score,
                    word_frequency_score=frequency_score,
                    morphology_score=morphology_score,
                    etymology_score=etymology_score,
                    difficulty_calculation_method=f"4-factor weighted model (overall_score: {overall_score:.2f})",
                    part_of_speech=data['part_of_speech'],
                    pronunciation_guide=data['pronunciation_guide'],
                    etymology=data['etymology'],
                    memory_tips=data['memory_tips'],
                    language_origin=data['language_origin'],
                    source_difficulties=row['source_difficulties'],
                    frequency=len(row['years'].split('; ')) if 'years' in row else 1.0,
                    original_source=f"Scripps National Spelling Bee Words of the Champions ({row.get('years', 'Unknown')})" if 'years' in row else "Scripps National Spelling Bee"
                )
                
                words_processed.append(word_obj)
                
                # Flag combined word errors
                if word in self.combined_word_errors:
                    logger.warning(f"COMBINED WORD ERROR DETECTED: {word}")
                    
            else:
                logger.warning(f"No data found for word: {word}")
        
        # Write output file
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                if words_processed:
                    fieldnames = [
                        'word', 'definition', 'example_sentence', 'source_difficulty',
                        'difficulty_level', 'difficulty_name', 'ai_difficulty_level', 'ai_difficulty_name',
                        'phonetic_transparency_score', 'word_frequency_score', 'morphology_score', 'etymology_score',
                        'difficulty_calculation_method', 'part_of_speech', 'pronunciation_guide', 'etymology',
                        'etymology_source', 'memory_tips', 'alternate_spellings', 'language_origin',
                        'definition_source', 'source_names', 'source_difficulties', 'frequency',
                        'original_source', 'source_access_date'
                    ]
                    
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for word_obj in words_processed:
                        writer.writerow({
                            'word': word_obj.word,
                            'definition': word_obj.definition,
                            'example_sentence': word_obj.example_sentence,
                            'source_difficulty': word_obj.source_difficulty,
                            'difficulty_level': word_obj.difficulty_level,
                            'difficulty_name': word_obj.difficulty_name,
                            'ai_difficulty_level': word_obj.ai_difficulty_level,
                            'ai_difficulty_name': word_obj.ai_difficulty_name,
                            'phonetic_transparency_score': word_obj.phonetic_transparency_score,
                            'word_frequency_score': word_obj.word_frequency_score,
                            'morphology_score': word_obj.morphology_score,
                            'etymology_score': word_obj.etymology_score,
                            'difficulty_calculation_method': word_obj.difficulty_calculation_method,
                            'part_of_speech': word_obj.part_of_speech,
                            'pronunciation_guide': word_obj.pronunciation_guide,
                            'etymology': word_obj.etymology,
                            'etymology_source': word_obj.etymology_source,
                            'memory_tips': word_obj.memory_tips,
                            'alternate_spellings': word_obj.alternate_spellings,
                            'language_origin': word_obj.language_origin,
                            'definition_source': word_obj.definition_source,
                            'source_names': word_obj.source_names,
                            'source_difficulties': word_obj.source_difficulties,
                            'frequency': word_obj.frequency,
                            'original_source': word_obj.original_source,
                            'source_access_date': word_obj.source_access_date
                        })
                        
            logger.info(f"Successfully processed {len(words_processed)} words to {output_file}")
            
            # Report combined word errors
            if any(word in self.combined_word_errors for word in [w.word for w in words_processed]):
                logger.warning("COMBINED WORD ERRORS DETECTED IN THIS BATCH:")
                for error in self.combined_word_errors:
                    if any(w.word == error for w in words_processed):
                        logger.warning(f"  - {error}")
                        
        except Exception as e:
            logger.error(f"Error writing output file: {e}")

def main():
    processor = Batch013Processor()
    input_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_013_words.csv"
    output_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_013_processed.csv"
    
    processor.process_batch(input_file, output_file)
    
    print(f"\nBatch 013 Processing Complete!")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Combined word errors flagged: {len(processor.combined_word_errors)}")

if __name__ == "__main__":
    main()