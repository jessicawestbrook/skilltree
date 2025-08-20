import pandas as pd
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import math

@dataclass
class WordData:
    word: str
    definition: str = ""
    part_of_speech: str = ""
    pronunciation_guide: str = ""
    etymology: str = ""
    language_origins: str = ""
    definition_source: str = "Claude"
    pronunciation_source: str = "Claude"
    etymology_source: str = "Claude"
    example_sentence: str = ""
    example_sentence_source: str = "Claude"
    memory_tip: str = ""
    memory_tip_source: str = "Claude"
    difficulty_phonetic: Optional[int] = None
    difficulty_semantic: Optional[int] = None
    difficulty_morphological: Optional[int] = None
    difficulty_etymological: Optional[int] = None
    combined_words_detected: bool = False
    incomplete_word_detected: bool = False
    parsing_errors: List[str] = field(default_factory=list)
    years: str = ""
    source_files: str = ""
    source_difficulties: str = ""

class DifficultyCalculator:
    def calculate_phonetic_score(self, word: str, pronunciation: str) -> int:
        irregular_patterns = ['ough', 'augh', 'eigh', 'ough', 'ph', 'gh', 'ch', 'sh', 'th']
        score = 1
        for pattern in irregular_patterns:
            if pattern in word.lower():
                score += 1
        return min(score, 5)
    
    def calculate_semantic_score(self, definition: str, word: str) -> int:
        if len(definition) > 300:
            return 4
        elif len(definition) > 200:
            return 3
        elif len(definition) > 100:
            return 2
        return 1
    
    def calculate_morphological_score(self, word: str) -> int:
        prefixes = ['un', 'pre', 'dis', 'in', 'im', 'ir', 'ex', 'sub', 'super', 'anti', 'auto']
        suffixes = ['tion', 'sion', 'ness', 'ment', 'able', 'ible', 'ous', 'eous', 'ious']
        score = 1
        for prefix in prefixes:
            if word.lower().startswith(prefix):
                score += 1
                break
        for suffix in suffixes:
            if word.lower().endswith(suffix):
                score += 1
                break
        if len(word) > 10:
            score += 1
        return min(score, 5)
    
    def calculate_etymological_score(self, etymology: str, language_origins: str) -> int:
        complex_origins = ['Greek', 'Latin', 'Sanskrit', 'Hebrew', 'Arabic']
        if any(origin in language_origins for origin in complex_origins):
            return 3
        elif 'French' in language_origins or 'German' in language_origins:
            return 2
        return 1

class Batch064Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def detect_parsing_errors(self, word: str) -> Tuple[bool, bool, List[str]]:
        errors = []
        combined_detected = False
        incomplete_detected = False
        
        # Check for combined words (specific to this batch)
        combined_word_patterns = {
            'expatiatexerogel': ['expatiate', 'xerogel'],
            'extinctextinguish': ['extinct', 'extinguish'],
            'extrorsef': ['corrupted "extrorse"']
        }
        
        if word.lower() in combined_word_patterns:
            combined_detected = True
            errors.append(f"Combined word error: \"{word}\" appears to be {' + '.join(combined_word_patterns[word.lower()])} merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.")
        
        # Check for corrupted words
        if word.lower() == 'extrorsef':
            incomplete_detected = True
            errors.append(f"Corrupted word: \"{word}\" appears to be \"extrorse\" with an extra \"f\" added. This is likely a PDF parsing error.")
        
        return combined_detected, incomplete_detected, errors
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Generate comprehensive educational data for spelling bee words using Claude's knowledge."""
        
        batch_064_data = {
            'exorbitant': {
                'definition': 'Exorbitant describes something that is unreasonably high, excessive, or extreme, particularly in terms of price, cost, or demand. When something is exorbitant, it goes far beyond what is considered normal, fair, or reasonable. The word carries a strong negative connotation, suggesting that the excessive nature of whatever is being described is problematic or unjustifiable. Exorbitant prices, for example, are those that are so high they seem to take advantage of consumers or circumstances. The term can also apply to demands, requests, expectations, or behaviors that are considered wildly unreasonable or beyond acceptable limits.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ig-ZOR-bi-tant',
                'etymology': 'From Latin "exorbitans," present participle of "exorbitare," meaning "to go out of the track." The prefix "ex-" means "out of" and "orbita" means "track" or "rut," literally referring to a wheel going off its proper path.',
                'language_origins': 'Latin',
                'example_sentence': 'The hotel charged _______ rates during the holiday weekend, forcing many tourists to look for alternative accommodations.',
                'memory_tip': 'Think "EX-ORB-itant" - imagine something going "EX" (out of) its proper "ORB" (circular path or orbit), becoming excessive and unreasonable.'
            },
            'expand': {
                'definition': 'Expand means to increase in size, volume, scope, or extent, or to cause something to become larger or more comprehensive. This can refer to physical growth, such as a balloon expanding when filled with air, or abstract growth, such as expanding one\'s knowledge or expanding a business. The word implies a stretching out, spreading, or enlargement from a previous state. Expansion can be gradual or rapid, controlled or uncontrolled. In various contexts, expand can mean to elaborate on ideas, to extend boundaries, to grow in influence, or to develop something more fully.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ik-SPAND',
                'etymology': 'From Latin "expandere," meaning "to spread out." The prefix "ex-" means "out" and "pandere" means "to spread," literally meaning to spread outward.',
                'language_origins': 'Latin',
                'example_sentence': 'The company plans to _______ its operations to three new countries by the end of next year.',
                'memory_tip': 'Remember "ex-PAND" - think of a PANDa stretching EX-tra wide, expanding its body to appear larger.'
            },
            'expanse': {
                'definition': 'An expanse is a wide, continuous area or stretch of something, typically land, water, or sky. The word suggests vastness, openness, and breadth, often referring to natural features that extend far in all directions. An expanse creates a sense of scale and grandeur, emphasizing the impressive scope of what is being described. It can refer to physical spaces like the expanse of the ocean, the expanse of a desert, or the expanse of the night sky. The term conveys both the idea of great size and the unbroken, continuous nature of the area being described.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ik-SPANS',
                'etymology': 'From Latin "expansum," meaning "something spread out," derived from "expandere" (to spread out). Related to the concept of expansion and spreading across space.',
                'language_origins': 'Latin',
                'example_sentence': 'The travelers gazed across the vast _______ of the prairie, seeing nothing but grassland stretching to the horizon.',
                'memory_tip': 'Think "ex-PANSE" - imagine EX-tra large PANTS that SPAN a huge area, representing a vast expanse of fabric.'
            },
            'expansion': {
                'definition': 'Expansion refers to the action or process of becoming larger, more extensive, or more comprehensive. It can describe physical growth, such as the thermal expansion of metals when heated, or abstract growth, such as business expansion into new markets. Expansion implies an increase in size, scope, scale, or influence from a previous state. The process can be intentional and planned, as in urban expansion, or natural and automatic, as in the expansion of gases. Expansion can be gradual or rapid, and it often involves spreading outward or extending boundaries beyond their previous limits.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ik-SPAN-shun',
                'etymology': 'From Latin "expansio," from "expandere" meaning "to spread out." The suffix "-sion" indicates the action or result of the verb, making it the noun form of "expand."',
                'language_origins': 'Latin',
                'example_sentence': 'The rapid _______ of the technology sector has created thousands of new jobs in the region.',
                'memory_tip': 'Remember "ex-PANS-ion" - think of EX-tra PANS being added to a kitchen during renovation, representing expansion of cooking capacity.'
            },
            'expatiate': {
                'definition': 'Expatiate means to speak or write at length about a subject, often in great detail and with elaborate explanation. When someone expatiates, they elaborate extensively, providing comprehensive coverage of a topic, sometimes to the point of being lengthy or verbose. The word suggests a thorough, detailed discussion that explores various aspects of a subject. Expatiation often involves going into considerable depth, offering extensive commentary, analysis, or description. While it can indicate thoroughness and expertise, it can also suggest a tendency toward wordiness or excessive elaboration.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ik-SPAY-shee-ayt',
                'etymology': 'From Latin "expatiari," meaning "to wander outside" or "to digress." The prefix "ex-" means "out" and "spatiari" means "to walk about," originally referring to wandering off the main path in discussion.',
                'language_origins': 'Latin',
                'example_sentence': 'The professor began to _______ on the historical significance of the Renaissance, speaking for nearly an hour about its various cultural impacts.',
                'memory_tip': 'Think "ex-PATIENT" - when someone is EX-tremely PATIENT, they have time to speak at great length about topics they\'re passionate about.'
            },
            'expectorant': {
                'definition': 'An expectorant is a type of medication or substance that helps loosen and expel mucus and phlegm from the respiratory tract, particularly from the lungs and bronchi. Expectorants work by thinning the secretions in the airways, making it easier for a person to cough up and clear mucus from their respiratory system. This type of medication is commonly used to treat conditions involving congestion, such as bronchitis, colds, and other respiratory infections. Natural expectorants include certain herbs and steam inhalation, while pharmaceutical expectorants are available over-the-counter or by prescription.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ik-SPEK-tuh-rant',
                'etymology': 'From Latin "expectoratus," past participle of "expectorare," meaning "to expel from the chest." The prefix "ex-" means "out" and "pectus" means "chest" or "breast."',
                'language_origins': 'Latin',
                'example_sentence': 'The doctor recommended an _______ to help clear the persistent cough and chest congestion.',
                'memory_tip': 'Remember "ex-PECTOR-ant" - think "EX-pel from the CHEST" (pectoral area), which is exactly what this medicine helps you do.'
            },
            'expedition': {
                'definition': 'An expedition is an organized journey or voyage undertaken for a specific purpose, typically involving exploration, research, military action, or adventure. Expeditions are usually planned missions that involve traveling to distant, difficult, or dangerous places to achieve particular objectives. They often require careful preparation, specialized equipment, and skilled participants. Historical expeditions have included explorations of unknown territories, scientific research missions, military campaigns, and adventures to remote locations. Modern expeditions might involve mountain climbing, archaeological research, wildlife studies, or space exploration.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ek-spi-DISH-un',
                'etymology': 'From Latin "expeditio," from "expedire" meaning "to free up" or "to make ready." Originally referred to freeing soldiers\' feet from entanglements, then came to mean preparing for a journey.',
                'language_origins': 'Latin',
                'example_sentence': 'The scientific _______ to Antarctica will study the effects of climate change on ice formations over the next six months.',
                'memory_tip': 'Think "ex-PETITION" - like signing a petition to get EX-tra support for a challenging journey or mission.'
            },
            'experience': {
                'definition': 'Experience encompasses the knowledge, skills, and understanding that come from direct participation in events, activities, or situations over time. It can refer to a single event or occurrence, as in "having an experience," or to the accumulated wisdom and capability that develops through repeated exposure to situations. Experience is often contrasted with theoretical knowledge, representing practical, hands-on learning. It can be positive or negative, educational or entertaining, brief or extensive. Experience shapes our understanding of the world and influences our future decisions and actions.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'ik-SPEER-ee-uns',
                'etymology': 'From Latin "experientia," from "experiri" meaning "to try" or "to test." The root "per-" means "through" and relates to going through trials or tests.',
                'language_origins': 'Latin',
                'example_sentence': 'Her years of _______ in emergency medicine made her the ideal candidate to lead the hospital\'s trauma unit.',
                'memory_tip': 'Remember "ex-PEER-ience" - you gain experience by looking beyond (EX) what your PEERS know, through actual doing and learning.'
            },
            'experimenting': {
                'definition': 'Experimenting is the action of conducting tests, trials, or investigations to discover, prove, or disprove something. It involves systematically trying different approaches, methods, or variables to observe outcomes and gather information. Experimenting can be formal, as in scientific research with controlled conditions, or informal, as in trying new cooking techniques or creative approaches. The process typically involves hypothesis formation, testing, observation, and analysis of results. Experimenting is fundamental to scientific discovery, innovation, and learning.',
                'part_of_speech': 'verb (present participle)',
                'pronunciation_guide': 'ik-SPER-uh-ment-ing',
                'etymology': 'From Latin "experimentum," from "experiri" meaning "to try" or "to test." The suffix "-ing" indicates ongoing action.',
                'language_origins': 'Latin',
                'example_sentence': 'The chef spent months _______ with different spice combinations before perfecting her signature sauce.',
                'memory_tip': 'Think "ex-PERIMENT-ing" - like a PERMANENT EX-tra effort to try new things and discover what works.'
            },
            'expert': {
                'definition': 'An expert is a person who has extensive knowledge, skill, or experience in a particular field, subject, or activity. Experts have developed their expertise through years of study, practice, and application, making them authorities in their areas of specialization. They possess deep understanding that allows them to solve complex problems, make informed judgments, and provide reliable guidance to others. Expertise typically involves both theoretical knowledge and practical application. As an adjective, expert describes something done with great skill, knowledge, or proficiency.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'EK-spurt',
                'etymology': 'From Latin "expertus," past participle of "experiri" meaning "to try" or "to test." Originally meant "one who has tried" or "one who has been tested."',
                'language_origins': 'Latin',
                'example_sentence': 'The cybersecurity _______ identified the source of the data breach within hours of the attack.',
                'memory_tip': 'Remember "EX-PERT" - someone who is EX-tremely PERT (skilled and confident) in their field through extensive experience.'
            },
            'expiration': {
                'definition': 'Expiration refers to the end of a period of validity, effectiveness, or life. It commonly describes the date when something becomes invalid, unusable, or unsafe, such as food products, medications, documents, or agreements. In biological contexts, expiration can refer to the act of breathing out or exhaling air from the lungs. The term also applies to the termination of contracts, licenses, warranties, or other time-limited arrangements. When something reaches its expiration, it typically requires renewal, replacement, or disposal.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ek-spi-RAY-shun',
                'etymology': 'From Latin "expiratio," from "expirare" meaning "to breathe out" or "to die." The prefix "ex-" means "out" and "spirare" means "to breathe."',
                'language_origins': 'Latin',
                'example_sentence': 'Please check the _______ date on the medication before taking it, as expired drugs can be ineffective or dangerous.',
                'memory_tip': 'Think "ex-SPIRE-ation" - when something EX-PIRES (ends or runs out), like a subscription that needs renewal.'
            },
            'explode': {
                'definition': 'Explode means to burst or shatter violently and noisily as a result of rapid expansion or the release of internal pressure. This can describe literal explosions involving fire, chemicals, or other destructive forces, or figurative explosions such as sudden emotional outbursts or rapid population growth. When something explodes, it typically involves a sudden, dramatic release of energy that causes destruction, dispersion, or dramatic change. The word can also mean to increase rapidly in size, number, or intensity, or to react with sudden, intense emotion.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ik-SPLOHD',
                'etymology': 'From Latin "explodere," originally meaning "to drive off by clapping." The prefix "ex-" means "out" and "plaudere" means "to clap," originally referring to driving actors off stage.',
                'language_origins': 'Latin',
                'example_sentence': 'The fireworks will _______ in brilliant colors across the night sky during the grand finale of the celebration.',
                'memory_tip': 'Remember "ex-PLODE" - think of something EX-tremely LOADED with energy that suddenly bursts out.'
            },
            'exploits': {
                'definition': 'Exploits can function as both a noun and a verb with different meanings. As a noun, exploits refer to bold, daring, or heroic acts or achievements, particularly those involving adventure, courage, or skill. These are notable deeds that often become legendary or are celebrated for their remarkable nature. As a verb, exploits means to make use of something or someone, often unfairly or for personal gain. This usage typically has negative connotations, suggesting taking advantage of vulnerabilities, resources, or people without proper compensation or consideration.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'EK-sployts (noun), ik-SPLOYTS (verb)',
                'etymology': 'From Old French "esploit," meaning "accomplishment," derived from Latin "explicitus" meaning "unfolded" or "accomplished."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The documentary chronicled the daring _______ of early aviation pioneers who risked their lives to advance human flight.',
                'memory_tip': 'For the noun meaning heroic deeds, think "EX-PLOIT" - EX-traordinary acts that people like to exPLOIT (tell stories about).'
            },
            'exploration': {
                'definition': 'Exploration is the action of traveling through or investigating unfamiliar areas, subjects, or concepts to learn about them or discover new information. It involves systematic investigation, examination, or study of something that is unknown or not fully understood. Exploration can be physical, such as geographical expeditions to uncharted territories, or intellectual, such as exploring new ideas, theories, or fields of knowledge. The process typically involves curiosity, careful observation, documentation, and analysis of findings. Exploration has been fundamental to human advancement and discovery throughout history.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ek-spluh-RAY-shun',
                'etymology': 'From Latin "exploratio," from "explorare" meaning "to investigate" or "to search out." The root "plorare" means "to cry out," possibly referring to calling out while searching.',
                'language_origins': 'Latin',
                'example_sentence': 'The space agency announced a new mission for the _______ of Mars\' polar ice caps to search for signs of past water activity.',
                'memory_tip': 'Think "ex-PLORE-ation" - the process of EX-tending your knowledge by going out to EXPLORE unknown territories or subjects.'
            },
            'explore': {
                'definition': 'Explore means to investigate, examine, or travel through an area or subject systematically in order to learn about it or discover new information. When you explore, you venture into unfamiliar territory, whether physical spaces like forests or caves, or abstract concepts like ideas or possibilities. Exploration involves curiosity, careful observation, and often some degree of risk or uncertainty. The word implies a purposeful search for knowledge, understanding, or discovery. Exploring can be methodical and scientific or spontaneous and adventurous.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ik-SPLOR',
                'etymology': 'From Latin "explorare," meaning "to investigate" or "to search out." The prefix "ex-" means "out" and "plorare" means "to cry out," possibly referring to calling out while searching.',
                'language_origins': 'Latin',
                'example_sentence': 'Scientists continue to _______ the deepest parts of the ocean, discovering new species with each expedition.',
                'memory_tip': 'Remember "ex-PLORE" - think of going EX-tra far to thoroughly examine and investigate, like an explorer with a map.'
            },
            'explosive': {
                'definition': 'Explosive describes something capable of exploding or likely to explode, or characterized by sudden, violent, or dramatic action. When applied to substances, it refers to materials that can rapidly release energy through chemical reaction, causing destruction. Figuratively, explosive can describe situations, emotions, or developments that are volatile, intense, or likely to erupt suddenly. The term can also describe rapid growth or change, such as explosive population growth. As a noun, an explosive is a substance designed to explode for specific purposes.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ik-SPLOH-siv',
                'etymology': 'From Latin "explosivus," derived from "explodere" meaning "to drive out by clapping" or "to burst forth." The suffix "-ive" indicates having the quality or tendency.',
                'language_origins': 'Latin',
                'example_sentence': 'The documentary revealed the _______ growth of social media companies over the past decade.',
                'memory_tip': 'Think "ex-PLOS-ive" - something that can EX-PLODE with tremendous force, whether literally or figuratively.'
            },
            'exposition': {
                'definition': 'Exposition refers to a comprehensive description, explanation, or presentation of an idea, theory, or subject. In literature and drama, exposition is the part of a story that provides background information, setting, and context necessary for understanding the plot. In academic or formal contexts, exposition involves detailed explanation or analysis of complex topics. An exposition can also be a large-scale public exhibition or fair showcasing products, ideas, or cultural achievements. The term emphasizes clarity, thoroughness, and systematic presentation of information.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ek-spuh-ZISH-un',
                'etymology': 'From Latin "expositio," from "exponere" meaning "to set forth" or "to expose." The prefix "ex-" means "out" and "ponere" means "to place."',
                'language_origins': 'Latin',
                'example_sentence': 'The professor\'s clear _______ of quantum mechanics made the complex topic accessible to undergraduate students.',
                'memory_tip': 'Remember "ex-POSITION" - like setting out your POSITION on a topic in an EX-tended, detailed explanation.'
            },
            'expostulate': {
                'definition': 'Expostulate means to express disagreement or disapproval earnestly and in detail, often in an attempt to persuade someone to change their course of action. When someone expostulates, they present arguments, reasons, or objections in a serious, often lengthy manner, typically because they believe the other person is making a mistake or acting wrongly. The word suggests a formal, reasoned protest rather than an emotional outburst. Expostulation often involves pleading, reasoning, or attempting to convince through logical argument.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ik-SPOS-chuh-layt',
                'etymology': 'From Latin "expostulare," meaning "to demand urgently." The prefix "ex-" means "out" and "postulare" means "to demand" or "to ask."',
                'language_origins': 'Latin',
                'example_sentence': 'The environmental lawyer began to _______ with the city council about their decision to approve the controversial development project.',
                'memory_tip': 'Think "ex-POSTULATE" - like an EX-tended POSTULATION where you present detailed arguments and reasons against something.'
            },
            'exposure': {
                'definition': 'Exposure refers to the state of being subjected to or coming into contact with something, often something potentially harmful, beneficial, or influential. It can describe physical contact with elements like sunlight, chemicals, or weather conditions, or abstract contact with ideas, experiences, or situations. In photography, exposure refers to the amount of light that reaches the camera sensor. In medicine, exposure often refers to contact with pathogens or toxins. The term can also mean revealing or making something visible that was previously hidden.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ik-SPOH-zhur',
                'etymology': 'From expose + -ure suffix. "Expose" comes from Old French "exposer," from Latin "exponere" meaning "to set forth" or "to place outside."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'Prolonged _______ to loud music without hearing protection can cause permanent damage to your ears.',
                'memory_tip': 'Remember "ex-POSURE" - being EX-posed to something, like standing outside in different weather conditions.'
            },
            'exposé': {
                'definition': 'An exposé is a detailed investigation and report that reveals hidden, secret, or scandalous information about a person, organization, or situation. Exposés are typically journalistic works that uncover wrongdoing, corruption, fraud, or other unethical behavior that those involved would prefer to keep hidden. These investigative pieces often require extensive research, fact-checking, and sometimes undercover work. Exposés serve the public interest by bringing important information to light and holding powerful individuals or institutions accountable for their actions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ek-spoh-ZAY',
                'etymology': 'From French "exposé," past participle of "exposer" meaning "to expose." The accent mark indicates the French pronunciation and distinguishes it from the verb "expose."',
                'language_origins': 'French',
                'example_sentence': 'The investigative journalist spent two years researching her _______ on corporate tax avoidance schemes.',
                'memory_tip': 'Remember the French pronunciation "ex-poh-ZAY" - it\'s like saying "EX-pose, eh?" with a French accent when revealing secrets.'
            },
            'express': {
                'definition': 'Express has multiple meanings depending on context. As a verb, it means to convey thoughts, feelings, or ideas through words, actions, or artistic media. It can also mean to squeeze or press out, as in expressing juice from fruit. As an adjective, express means explicit, definite, or specifically stated, or designed for speed and efficiency. As a noun, express refers to a fast train or delivery service that makes few stops. The word generally emphasizes clarity, directness, or speed.',
                'part_of_speech': 'verb, adjective, noun',
                'pronunciation_guide': 'ik-SPRES',
                'etymology': 'From Latin "expressus," past participle of "exprimere" meaning "to press out" or "to represent." The prefix "ex-" means "out" and "premere" means "to press."',
                'language_origins': 'Latin',
                'example_sentence': 'The artist used bold colors and dramatic brushstrokes to _______ the intensity of her emotions.',
                'memory_tip': 'Think "ex-PRESS" - like EX-tra fast PRESS delivery, or like pressing OUT your thoughts and feelings.'
            },
            'expressing': {
                'definition': 'Expressing is the present participle of express, referring to the ongoing action of conveying thoughts, feelings, ideas, or information through various means such as speech, writing, art, or behavior. When someone is expressing themselves, they are actively communicating their inner experiences, opinions, or creative visions to others. Expression can be verbal, non-verbal, artistic, or behavioral. The act of expressing often involves translating internal experiences into external, observable forms that others can understand and interpret.',
                'part_of_speech': 'verb (present participle)',
                'pronunciation_guide': 'ik-SPRES-ing',
                'etymology': 'From Latin "expressus" (past participle of "exprimere") meaning "to press out," with the English suffix "-ing" indicating ongoing action.',
                'language_origins': 'Latin',
                'example_sentence': 'The therapy session focused on helping patients practice _______ their feelings in healthy, constructive ways.',
                'memory_tip': 'Remember "ex-PRESS-ing" - like continuously PRESSING OUT your thoughts and feelings, making them EX-ternal and visible.'
            },
            'expression': {
                'definition': 'Expression encompasses the action of making known one\'s thoughts, feelings, or ideas, as well as the particular way in which something is communicated or manifested. It can refer to facial expressions that convey emotions, artistic expressions that communicate creativity, or verbal expressions that share thoughts. In mathematics, an expression is a combination of symbols, numbers, and operators that represents a value. Expression also refers to the style, manner, or form in which something is presented or performed, often reflecting individual personality or cultural influences.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ik-SPRESH-un',
                'etymology': 'From Latin "expressio," from "exprimere" meaning "to press out" or "to represent." The suffix "-ion" indicates the action or result of expressing.',
                'language_origins': 'Latin',
                'example_sentence': 'The dancer\'s graceful movements were a beautiful _______ of the music\'s emotional depth and complexity.',
                'memory_tip': 'Think "ex-PRESS-ion" - the result of PRESSING OUT your inner thoughts and feelings into EX-ternal form.'
            },
            'expressway': {
                'definition': 'An expressway is a high-speed, limited-access highway designed for fast-moving traffic, typically featuring multiple lanes, controlled entrances and exits, and minimal intersections. Expressways are engineered to facilitate efficient transportation over longer distances, with features like overpasses, underpasses, and on-ramps that allow traffic to flow smoothly without frequent stops. These roadways often connect major cities or serve as bypasses around urban areas. The design of expressways prioritizes speed and traffic volume, making them essential components of modern transportation infrastructure.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ik-SPRES-way',
                'etymology': 'Compound word combining "express" (meaning fast or direct) and "way" (meaning road or path). "Express" comes from Latin "exprimere" meaning "to press out."',
                'language_origins': 'Latin, English',
                'example_sentence': 'Construction crews worked overnight to repave sections of the _______ that connects downtown to the international airport.',
                'memory_tip': 'Remember "EXPRESS-way" - a highway designed for EX-tra fast, EX-press travel without delays or stops.'
            },
            'expugnable': {
                'definition': 'Expugnable describes something that can be conquered, overcome, or successfully attacked, particularly in military contexts. The term refers to fortifications, positions, or defenses that are vulnerable to assault and can be captured or defeated through force or strategy. When something is expugnable, it lacks the strength, protection, or strategic advantage necessary to withstand attack. The word can also be applied metaphorically to arguments, positions, or situations that can be successfully challenged or refuted.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ik-SPUG-nuh-bul',
                'etymology': 'From Latin "expugnabilis," from "expugnare" meaning "to fight out" or "to conquer by assault." The prefix "ex-" means "out" and "pugnare" means "to fight."',
                'language_origins': 'Latin',
                'example_sentence': 'The ancient fortress, once considered impregnable, proved to be _______ when attackers discovered a weakness in its eastern wall.',
                'memory_tip': 'Remember "ex-PUG-nable" - think of something that can be defeated in a fight (PUG = fight), something that can be conquered (EX-pelled from its position).'
            },
            'expulsion': {
                'definition': 'Expulsion is the action of forcing someone or something to leave a place, institution, or organization, often as a punishment or consequence of unacceptable behavior. In educational contexts, expulsion typically refers to the permanent removal of a student from school due to serious misconduct. In medical contexts, expulsion can refer to the body\'s natural process of ejecting foreign substances or waste materials. The term implies a forceful, often permanent removal that results from violation of rules, standards, or natural processes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ik-SPUL-shun',
                'etymology': 'From Latin "expulsio," from "expellere" meaning "to drive out." The prefix "ex-" means "out" and "pellere" means "to drive" or "to push."',
                'language_origins': 'Latin',
                'example_sentence': 'The student\'s repeated violations of the academic honor code resulted in his _______ from the university.',
                'memory_tip': 'Think "ex-PULSE-ion" - like being EX-pelled with a strong PULSE of force, driven out powerfully.'
            },
            'expunge': {
                'definition': 'Expunge means to completely remove, erase, or eliminate something, particularly from records, memory, or existence. The word is often used in legal contexts to describe the process of officially removing criminal records or court proceedings from public access. When something is expunged, it is not merely hidden but thoroughly deleted or destroyed, as if it never existed. The term carries connotations of thorough, deliberate removal, often for the purpose of providing a fresh start or protecting privacy.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ik-SPUNJ',
                'etymology': 'From Latin "expungere," meaning "to mark off" or "to prick out." The prefix "ex-" means "out" and "pungere" means "to prick" or "to puncture."',
                'language_origins': 'Latin',
                'example_sentence': 'The judge agreed to _______ the defendant\'s juvenile record, giving him a clean slate as he entered adulthood.',
                'memory_tip': 'Remember "ex-SPUNGE" - like using a SPONGE to completely wipe away and remove all traces of something.'
            },
            'exquisite': {
                'definition': 'Exquisite describes something of exceptional beauty, elegance, or refinement, characterized by intricate detail, superior craftsmanship, or rare quality. When something is exquisite, it demonstrates extraordinary skill, taste, or perfection that sets it apart from ordinary examples. The word can apply to art, jewelry, food, experiences, or anything that exhibits remarkable beauty or quality. Exquisite can also describe intense sensations, whether pleasant or painful, that are felt with particular acuteness or sensitivity.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ik-SKWIZ-it',
                'etymology': 'From Latin "exquisitus," past participle of "exquirere" meaning "to search out carefully." The prefix "ex-" means "out" and "quaerere" means "to seek."',
                'language_origins': 'Latin',
                'example_sentence': 'The antique vase displayed _______ craftsmanship, with delicate hand-painted flowers covering its entire surface.',
                'memory_tip': 'Think "ex-QUIZ-ite" - something so beautiful it makes you want to EX-amine it closely, like taking a QUIZ about all its perfect details.'
            },
            'exsect': {
                'definition': 'Exsect is a technical term meaning to cut out or remove surgically, particularly in medical or biological contexts. The word describes the precise surgical removal of tissue, organs, or specimens for examination, treatment, or research purposes. Exsection typically involves careful, controlled cutting to extract specific portions while minimizing damage to surrounding areas. This term is primarily used in medical, veterinary, and biological research settings where precise removal procedures are necessary.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ek-SEKT',
                'etymology': 'From Latin "exsecare," meaning "to cut out." The prefix "ex-" means "out" and "secare" means "to cut."',
                'language_origins': 'Latin',
                'example_sentence': 'The surgeon will carefully _______ the tumor while preserving as much healthy tissue as possible.',
                'memory_tip': 'Remember "ex-SECT" - to cut out a specific SECTion, removing it EX-actly and precisely.'
            },
            'extant': {
                'definition': 'Extant means still existing, surviving, or remaining in existence, particularly when referring to things that might be expected to have disappeared over time. The word is often used to describe historical documents, artifacts, buildings, or species that have survived to the present day despite age, threats, or the passage of time. When something is extant, it has persisted through various challenges and continues to exist in its original or recognizable form, making it valuable for historical, scientific, or cultural study.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'EK-stant',
                'etymology': 'From Latin "extans," present participle of "extare" meaning "to stand out" or "to exist." The prefix "ex-" means "out" and "stare" means "to stand."',
                'language_origins': 'Latin',
                'example_sentence': 'Only three _______ copies of the medieval manuscript remain, making it one of the rarest books in the world.',
                'memory_tip': 'Think "ex-TANT" - something that EX-ists and is TANGIBLE, still standing and present today.'
            },
            'extemporaneous': {
                'definition': 'Extemporaneous describes something done or created spontaneously, without advance preparation or planning. When applied to speeches or performances, it refers to delivery that appears natural and unrehearsed, though it may involve some preparation or prior knowledge of the subject. Extemporaneous speaking involves thinking and responding on the spot, demonstrating quick thinking and adaptability. The term suggests skillful improvisation and the ability to communicate effectively without rigid scripts or detailed preparation.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ik-stem-puh-RAY-nee-us',
                'etymology': 'From Latin "ex tempore," meaning "out of time" or "according to the time." The phrase originally referred to something done according to the circumstances of the moment.',
                'language_origins': 'Latin',
                'example_sentence': 'Her _______ remarks at the ceremony were so eloquent that many guests assumed she had prepared them in advance.',
                'memory_tip': 'Remember "ex-TEMPO-raneous" - speaking EX-temporaneously, outside of planned TEMPO or timing, spontaneously in the moment.'
            },
            'extensive': {
                'definition': 'Extensive describes something that covers a large area, has great scope, or includes many details or aspects. When something is extensive, it is comprehensive, wide-ranging, or substantial in size, degree, or duration. The word can apply to physical spaces, knowledge, research, damage, or any situation that involves considerable breadth or depth. Extensive implies thoroughness and completeness, suggesting that something has been developed, explored, or affected in a comprehensive manner.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ik-STEN-siv',
                'etymology': 'From Latin "extensivus," from "extendere" meaning "to stretch out." The prefix "ex-" means "out" and "tendere" means "to stretch."',
                'language_origins': 'Latin',
                'example_sentence': 'The archaeologist conducted _______ research on ancient civilizations before writing her comprehensive textbook.',
                'memory_tip': 'Think "ex-TENSIVE" - EX-tremely TENSE with effort to stretch out and cover a vast area or many aspects.'
            },
            'extinct': {
                'definition': 'Extinct describes something that no longer exists, has died out completely, or has come to an end. The term is most commonly used to describe species of plants or animals that have no living members remaining anywhere on Earth. Extinct can also apply to languages that are no longer spoken, cultures that have disappeared, or practices that are no longer followed. When something becomes extinct, it represents a permanent loss, as there is no possibility of natural recovery or revival.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ik-STINGKT',
                'etymology': 'From Latin "extinctus," past participle of "extinguere" meaning "to quench" or "to put out." Originally referred to extinguishing fires.',
                'language_origins': 'Latin',
                'example_sentence': 'Paleontologists study fossils to learn about _______ species that lived millions of years ago.',
                'memory_tip': 'Remember "ex-TINCT" - completely EX-tinguished, with no TINT or trace of life remaining.'
            },
            'extinguish': {
                'definition': 'Extinguish means to put out a fire or flame completely, or to bring something to an end by eliminating or destroying it. When you extinguish a fire, you remove the conditions necessary for combustion, such as oxygen, heat, or fuel. Figuratively, the word can mean to eliminate, suppress, or destroy hopes, dreams, debt, or other abstract concepts. Extinguishing implies complete cessation rather than temporary suppression, suggesting that what is extinguished cannot easily be rekindled or revived.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ik-STING-gwish',
                'etymology': 'From Latin "extinguere," meaning "to quench" or "to put out." The prefix "ex-" means "completely" and "stinguere" means "to quench."',
                'language_origins': 'Latin',
                'example_sentence': 'The firefighters worked through the night to _______ the wildfire before it could spread to nearby homes.',
                'memory_tip': 'Think "ex-TING-wish" - you WISH to completely EX-tinguish the fire, making your wish come true by putting it out.'
            },
            'extra': {
                'definition': 'Extra means additional, beyond what is usual, expected, or necessary. As an adjective, it describes something that is supplementary, surplus, or exceeding the normal amount or standard. As a noun, extra can refer to an additional person or thing, particularly actors hired for crowd scenes in films. As an adverb, extra means to an unusually high degree, more than normal. The word generally suggests something beneficial that goes beyond basic requirements or expectations.',
                'part_of_speech': 'adjective, noun, adverb',
                'pronunciation_guide': 'EK-struh',
                'etymology': 'From Latin "extra," meaning "outside" or "beyond." Originally used as a prefix meaning "outside of" or "beyond the bounds of."',
                'language_origins': 'Latin',
                'example_sentence': 'The restaurant provided _______ bread rolls for the large party at no additional charge.',
                'memory_tip': 'Remember "EX-TRA" - EX-ceeding the usual amount, going beyond to provide TRA-ditional or expected quantities.'
            },
            'extracurricular': {
                'definition': 'Extracurricular refers to activities, programs, or pursuits that take place outside the regular academic curriculum of a school or educational institution. These activities complement formal education by providing opportunities for students to explore interests, develop skills, socialize, and engage in leadership experiences beyond classroom learning. Extracurricular activities can include sports, clubs, volunteer work, arts programs, student government, and various hobby groups. They are valuable for personal development, college applications, and building well-rounded individuals.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ek-struh-kuh-RIK-yuh-lur',
                'etymology': 'Compound word from Latin "extra" meaning "outside" and "curriculum" meaning "course of study." Literally means "outside the course of study."',
                'language_origins': 'Latin',
                'example_sentence': 'Sarah participated in numerous _______ activities including debate team, student council, and volunteer tutoring.',
                'memory_tip': 'Remember "EXTRA-curricular" - EXTRA activities beyond the regular curricular (curriculum) requirements.'
            },
            'extradition': {
                'definition': 'Extradition is the legal process by which one country surrenders a suspected or convicted criminal to another country where they are wanted for trial or to serve a sentence. This formal procedure typically involves treaties between nations and judicial proceedings to ensure the request is legitimate and meets legal requirements. Extradition serves to prevent criminals from escaping justice by fleeing to other countries. The process includes safeguards to protect individuals from unfair prosecution and ensures that extradition requests meet specific legal criteria.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ek-struh-DISH-un',
                'etymology': 'From Latin "ex" meaning "out" and "traditio" meaning "a handing over," from "tradere" meaning "to hand over" or "to deliver."',
                'language_origins': 'Latin',
                'example_sentence': 'The suspect fought the _______ order for three years before finally being returned to face charges in his home country.',
                'memory_tip': 'Think "extra-DITION" - an EXTRA formal procedure to hand over (traditio) someone across borders.'
            },
            'extraordinaire': {
                'definition': 'Extraordinaire is a term used after a noun to emphasize that someone is exceptionally skilled, remarkable, or outstanding in a particular field or activity. It suggests someone who possesses extraordinary abilities, talents, or expertise that sets them apart from others. The word is often used in a somewhat playful or grandiose manner to highlight exceptional competence or achievement. When someone is described as extraordinaire, it implies they have reached a level of excellence that is rare and noteworthy.',
                'part_of_speech': 'adjective (postpositive)',
                'pronunciation_guide': 'ik-stror-dn-AIR',
                'etymology': 'From French "extraordinaire," meaning "extraordinary" or "exceptional." The word maintains its French form and pronunciation in English usage.',
                'language_origins': 'French',
                'example_sentence': 'The chef _______ created a seven-course meal that left every guest talking about the incredible flavors for weeks.',
                'memory_tip': 'Remember the French pronunciation "extraordin-AIRE" - someone with EX-traordinary flair that\'s in the AIR, obvious to everyone.'
            },
            'extrapolate': {
                'definition': 'Extrapolate means to extend known information, data, or trends to make predictions or draw conclusions about unknown situations or future events. In mathematics and science, extrapolation involves extending a graph or data series beyond the known points to estimate values. More generally, extrapolation means taking existing knowledge or patterns and applying them to new contexts or circumstances. The process involves making educated guesses based on available evidence, though extrapolated conclusions become less reliable the further they extend from known data.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ik-STRAP-uh-layt',
                'etymology': 'From Latin "extra" meaning "outside" and "polatus" (related to "polire," meaning "to polish"). The term was originally used in mathematics to mean extending beyond known data points.',
                'language_origins': 'Latin',
                'example_sentence': 'Scientists can _______ from current climate data to predict temperature changes over the next century.',
                'memory_tip': 'Think "extra-POLATE" - taking EX-tra steps to POLISH your predictions by extending beyond known data.'
            },
            'extravagant': {
                'definition': 'Extravagant describes something that exceeds reasonable limits in terms of cost, elaborateness, or indulgence. When something is extravagant, it is characterized by excess, luxury, or wastefulness that goes beyond what is necessary or appropriate. The word can apply to spending habits, lifestyles, displays, or behaviors that are lavish, ostentatious, or immoderate. Extravagance often implies a disregard for practical constraints and a tendency toward showiness or self-indulgence.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ik-STRAV-uh-gant',
                'etymology': 'From Latin "extravagans," meaning "wandering outside" or "straying beyond bounds." The prefix "extra-" means "outside" and "vagari" means "to wander."',
                'language_origins': 'Latin',
                'example_sentence': 'The wedding featured _______ decorations including crystal chandeliers and thousands of imported roses.',
                'memory_tip': 'Remember "extra-VAGANT" - going EX-tra far in a VAGRANT (wandering) way, straying beyond reasonable limits.'
            },
            'extravasate': {
                'definition': 'Extravasate means to flow out or escape from the proper vessels or channels, particularly in medical contexts where it refers to the leakage of fluids such as blood, lymph, or medication from blood vessels or other conduits into surrounding tissues. When extravasation occurs, fluids that should remain within specific pathways instead leak into areas where they don\'t belong, potentially causing complications. The term is used in medicine, geology, and other sciences to describe the abnormal escape or overflow of contained substances.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ik-STRAV-uh-sayt',
                'etymology': 'From Latin "extra" meaning "outside" and "vas" meaning "vessel." Literally means "outside the vessel."',
                'language_origins': 'Latin',
                'example_sentence': 'The nurse monitored the IV site carefully to ensure the medication did not _______ into the surrounding tissue.',
                'memory_tip': 'Remember "extra-VAS-ate" - fluids going EX-tra outside their proper VAS (vessel), like a vase overflowing.'
            },
            'extremely': {
                'definition': 'Extremely is an adverb that means to a very high degree, in the highest possible measure, or to an exceptional extent. When something is described as extremely, it indicates that it possesses a quality or characteristic in an intense, maximum, or remarkable way. The word serves as an intensifier, emphasizing that whatever is being described goes well beyond normal or average levels. Extremely suggests the upper limits of a scale or the most intense version of a particular quality.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'ik-STREEM-lee',
                'etymology': 'From "extreme" (from Latin "extremus" meaning "outermost") plus the adverb suffix "-ly." "Extremus" comes from "exter" meaning "outside."',
                'language_origins': 'Latin',
                'example_sentence': 'The mountain climbers faced _______ cold temperatures and high winds during their ascent to the summit.',
                'memory_tip': 'Think "ex-TREME-ly" - going to the EX-treme, the most EXTREME degree possible of something.'
            },
            'extrorse': {
                'definition': 'Extrorse is a botanical term that describes anthers or other plant structures that face or open outward, away from the center of the flower. In botanical terminology, when stamens are extrorse, their anthers release pollen in a direction that faces away from the pistil and toward the outside of the flower. This is the opposite of introrse, where structures face inward. The positioning of extrorse anthers affects pollination patterns and is an important characteristic used in plant identification and classification.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'EK-strors',
                'etymology': 'From Latin "extorsus," meaning "turned outward." The prefix "ex-" means "out" and "torsus" relates to "torquere" meaning "to turn."',
                'language_origins': 'Latin',
                'example_sentence': 'The botanist noted that the lily\'s _______ anthers would facilitate cross-pollination by releasing pollen outward toward visiting insects.',
                'memory_tip': 'Remember "ex-TRORSE" - anthers that turn EX-ternally, facing outward like a TORCH pointing away from the center.'
            },
            'exuberant': {
                'definition': 'Exuberant describes someone or something characterized by high energy, enthusiasm, excitement, or abundant vitality. When a person is exuberant, they display lively, effusive, or spirited behavior that demonstrates joy, confidence, or vigorous health. The word can also describe abundant growth or profuse development, such as exuberant vegetation. Exuberance suggests an overflowing quality, whether of emotion, energy, or physical abundance, that is infectious and noticeable to others.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ig-ZOO-bur-ant',
                'etymology': 'From Latin "exuberans," present participle of "exuberare" meaning "to be abundant" or "to overflow." The prefix "ex-" means "out" and "uber" means "fertile" or "abundant."',
                'language_origins': 'Latin',
                'example_sentence': 'The children\'s _______ laughter and playful energy filled the playground with joy and excitement.',
                'memory_tip': 'Think "ex-UBER-ant" - like an UBER-charged person with EX-tra energy and enthusiasm bursting out.'
            },
            'exude': {
                'definition': 'Exude means to discharge or emit gradually, either literally by seeping or oozing out, or figuratively by displaying or radiating a quality or feeling. When substances exude, they slowly leak or flow from their source, such as sap exuding from tree bark or sweat exuding from pores. Figuratively, people can exude confidence, charm, or other personal qualities, meaning these characteristics are naturally and noticeably displayed in their behavior or presence. The word suggests a gradual, natural emission or display.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ig-ZOOD',
                'etymology': 'From Latin "exsudare," meaning "to sweat out." The prefix "ex-" means "out" and "sudare" means "to sweat."',
                'language_origins': 'Latin',
                'example_sentence': 'The confident speaker seemed to _______ charisma and expertise, captivating the entire audience.',
                'memory_tip': 'Remember "ex-UDE" - like moisture that seeps EX-ternally, or personal qualities that naturally ooze out.'
            },
            'eyelet': {
                'definition': 'An eyelet is a small hole, typically circular, that is reinforced around its edges and used for various purposes such as threading cords, laces, or ropes through fabric or other materials. Eyelets are commonly found in shoes for shoelaces, in clothing for drawstrings, in curtains for hanging rods, and in various textile applications. They can be made from metal, plastic, or other durable materials and are designed to prevent tearing or fraying of the surrounding material when items are threaded through them.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AHY-lit',
                'etymology': 'Middle English, diminutive of "eye," literally meaning "little eye." The suffix "-let" indicates a small version of something.',
                'language_origins': 'Middle English',
                'example_sentence': 'She carefully threaded the ribbon through each _______ to create an adjustable waistband on the dress.',
                'memory_tip': 'Remember "EYE-let" - a little EYE-shaped hole that lets things pass through, like threading a needle through an eye.'
            },
            'eyesore': {
                'definition': 'An eyesore is something that is visually unpleasant, ugly, or offensive to look at, particularly something that detracts from the aesthetic appeal of its surroundings. Eyesores are typically buildings, structures, or objects that are poorly maintained, inappropriately designed, or simply unattractive in their context. The term expresses strong disapproval of something\'s visual impact and suggests that it causes discomfort or annoyance to those who see it. Eyesores can affect property values and community pride.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AHY-sor',
                'etymology': 'Compound word combining "eye" and "sore," literally meaning something that makes the eyes sore or uncomfortable to look at.',
                'language_origins': 'English',
                'example_sentence': 'The abandoned factory became an _______ in the neighborhood, prompting residents to petition for its demolition.',
                'memory_tip': 'Remember "EYE-sore" - something that makes your EYES SORE from looking at something ugly or unpleasant.'
            }
        }
        
        if word.lower() in batch_064_data:
            return batch_064_data[word.lower()]
        else:
            # For any words not in our comprehensive data, return basic structure
            return {
                'definition': f'[Definition for {word} not available in batch data]',
                'part_of_speech': 'unknown',
                'pronunciation_guide': f'[Pronunciation for {word} not available]',
                'etymology': f'[Etymology for {word} not available]',
                'language_origins': 'unknown',
                'example_sentence': f'[Example sentence for {word} not available]',
                'memory_tip': f'[Memory tip for {word} not available]'
            }
    
    def process_batch(self, input_file: str, output_file: str):
        """Process a batch of spelling bee words with comprehensive Claude data."""
        print(f"Processing {input_file}...")
        
        # Read the input CSV
        df = pd.read_csv(input_file)
        
        processed_words = []
        error_count = 0
        
        for _, row in df.iterrows():
            word = str(row['word']).strip()
            
            # Skip empty rows
            if not word or word.lower() == 'nan':
                continue
            
            # Detect parsing errors
            combined_detected, incomplete_detected, errors = self.detect_parsing_errors(word)
            if errors:
                error_count += len(errors)
            
            # Get comprehensive data for this word
            word_data = self.get_comprehensive_claude_data(word)
            
            # Calculate difficulty scores (leaving final difficulty as null for now)
            phonetic_score = self.difficulty_calculator.calculate_phonetic_score(word, word_data['pronunciation_guide'])
            semantic_score = self.difficulty_calculator.calculate_semantic_score(word_data['definition'], word)
            morphological_score = self.difficulty_calculator.calculate_morphological_score(word)
            etymological_score = self.difficulty_calculator.calculate_etymological_score(word_data['etymology'], word_data['language_origins'])
            
            # Create WordData object
            processed_word = WordData(
                word=word,
                definition=word_data['definition'],
                part_of_speech=word_data['part_of_speech'],
                pronunciation_guide=word_data['pronunciation_guide'],
                etymology=word_data['etymology'],
                language_origins=word_data['language_origins'],
                example_sentence=word_data['example_sentence'],
                memory_tip=word_data['memory_tip'],
                difficulty_phonetic=phonetic_score,
                difficulty_semantic=semantic_score,
                difficulty_morphological=morphological_score,
                difficulty_etymological=etymological_score,
                combined_words_detected=combined_detected,
                incomplete_word_detected=incomplete_detected,
                parsing_errors=errors,
                years=str(row['years']) if 'years' in row else '',
                source_files=str(row['source_files']) if 'source_files' in row else '',
                source_difficulties=str(row['source_difficulties']) if 'source_difficulties' in row else ''
            )
            
            processed_words.append(processed_word)
        
        # Convert to DataFrame
        output_data = []
        for word_obj in processed_words:
            output_data.append({
                'word': word_obj.word,
                'definition': word_obj.definition,
                'part_of_speech': word_obj.part_of_speech,
                'pronunciation_guide': word_obj.pronunciation_guide,
                'etymology': word_obj.etymology,
                'language_origins': word_obj.language_origins,
                'definition_source': word_obj.definition_source,
                'pronunciation_source': word_obj.pronunciation_source,
                'etymology_source': word_obj.etymology_source,
                'example_sentence': word_obj.example_sentence,
                'example_sentence_source': word_obj.example_sentence_source,
                'memory_tip': word_obj.memory_tip,
                'memory_tip_source': word_obj.memory_tip_source,
                'difficulty_phonetic': word_obj.difficulty_phonetic,
                'difficulty_semantic': word_obj.difficulty_semantic,
                'difficulty_morphological': word_obj.difficulty_morphological,
                'difficulty_etymological': word_obj.difficulty_etymological,
                'difficulty': None,  # Leave null for now
                'years': word_obj.years,
                'source_files': word_obj.source_files,
                'source_difficulties': word_obj.source_difficulties,
                'combined_words_detected': word_obj.combined_words_detected,
                'incomplete_word_detected': word_obj.incomplete_word_detected,
                'parsing_errors': '; '.join(word_obj.parsing_errors) if word_obj.parsing_errors else ''
            })
        
        # Save to CSV
        output_df = pd.DataFrame(output_data)
        output_df.to_csv(output_file, index=False, quoting=1)  # quoting=1 ensures text fields are quoted
        
        # Print results
        print(f"Successfully processed {len(processed_words)}/50 words to {output_file}")
        if error_count > 0:
            print(f"Found {error_count} error(s):")
            for word_obj in processed_words:
                if word_obj.parsing_errors:
                    for error in word_obj.parsing_errors:
                        print(f"  - {word_obj.word}: {error}")
        
        print("Batch 064 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch064Processor()
    
    input_file = "output/batch_064_words.csv"
    output_file = "output/batch_064_processed.csv"
    
    processor.process_batch(input_file, output_file)