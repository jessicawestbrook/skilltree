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

class Batch068Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def detect_parsing_errors(self, word: str) -> Tuple[bool, bool, List[str]]:
        errors = []
        combined_detected = False
        incomplete_detected = False
        
        # Check for combined words (specific to this batch)
        combined_word_patterns = {
            'fineday': ['fine', 'day'],
            'flashbackquonk': ['flashback', 'quonk']
        }
        
        if word.lower() in combined_word_patterns:
            combined_detected = True
            errors.append(f"Combined word error: \"{word}\" appears to be {' + '.join(combined_word_patterns[word.lower()])} merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.")
        
        return combined_detected, incomplete_detected, errors
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Generate comprehensive educational data for spelling bee words using Claude's knowledge."""
        
        batch_068_data = {
            'finals': {
                'definition': 'Finals are the concluding examinations, competitions, or events in a series, representing the ultimate test or decisive contests that determine outcomes. In academic contexts, finals are comprehensive examinations given at the end of a term or course to assess students\' mastery of the material. In sports, finals are championship games or matches that determine winners. The word emphasizes the conclusive and decisive nature of these events, often carrying significant weight in determining success or advancement.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FY-nulz',
                'etymology': 'From "final" (from Latin "finalis" meaning "of the end") made plural, referring to concluding examinations or competitions.',
                'language_origins': 'Latin',
                'example_sentence': 'The students spent weeks preparing for _______ because these comprehensive exams would determine their semester grades.',
                'memory_tip': 'Remember "FIN-als" - the FINal tests that bring everything to an end, the ultimate academic challenge.'
            },
            'financier': {
                'definition': 'A financier is a person who engages in large-scale financial operations, particularly someone who provides capital for businesses, governments, or major projects. Financiers are experts in managing money, investments, and financial markets, often wielding significant influence in economic affairs. They may be bankers, investors, or specialists in raising and deploying capital for various enterprises. The term suggests someone with substantial financial resources and expertise who plays a key role in funding major economic activities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fin-un-SEER',
                'etymology': 'From French "financier," from "finance" (from Old French "finer" meaning "to pay"), referring to one who deals in financial matters.',
                'language_origins': 'French, Old French',
                'example_sentence': 'The successful _______ invested millions in renewable energy projects across three continents.',
                'memory_tip': 'Remember "financ-EER" - someone who steers (like an engineer) finances and money matters with expertise.'
            },
            'finch': {
                'definition': 'A finch is a small songbird belonging to the family Fringillidae, characterized by a compact body, short tail, and a conical beak adapted for eating seeds. Finches are known for their colorful plumage, pleasant songs, and social behavior. Common species include goldfinches, canaries, and house finches. These birds are popular in both wild bird watching and as cage birds due to their beautiful songs and relatively easy care. Finches play important roles in seed dispersal and pest control in their ecosystems.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FINCH',
                'etymology': 'From Old English "finc," related to similar words in other Germanic languages, referring to the small songbird.',
                'language_origins': 'Old English',
                'example_sentence': 'The bright yellow _______ visited the bird feeder every morning, delighting the children with its cheerful song.',
                'memory_tip': 'Remember "FINCH" - a small bird that you might FLINCH to see fly away because it\'s so beautiful and quick.'
            },
            'fine': {
                'definition': 'Fine has multiple meanings depending on context. As an adjective, it means high quality, excellent, thin, or satisfactory. As a noun, fine refers to a penalty payment for breaking laws or rules. As a verb, fine means to impose such a penalty. The word can describe weather (fine day), texture (fine sand), or quality (fine wine). Fine often suggests precision, excellence, or attention to detail, though it can also mean simply acceptable or adequate.',
                'part_of_speech': 'adjective, noun, verb',
                'pronunciation_guide': 'FYNE',
                'etymology': 'From Old French "fin," from Latin "finis" meaning "end" or "boundary," later developing meanings of "refined" and "excellent."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The artist used a _______ brush to paint the delicate details on the miniature portrait.',
                'memory_tip': 'Remember "FINE" - something that\'s reached the FINal level of quality, refined to the end point of excellence.'
            },
            'finial': {
                'definition': 'A finial is a decorative crowning ornament placed at the top, end, or corner of architectural structures, furniture, or decorative objects. These ornamental elements serve both aesthetic and symbolic functions, often featuring elaborate designs such as urns, flowers, or geometric patterns. Finials can be found on fence posts, curtain rods, flagpoles, furniture, and building corners. They represent the finishing touch that completes and crowns a design, adding elegance and visual interest to functional objects.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FIN-ee-ul',
                'etymology': 'From Latin "finalis" meaning "final" or "terminal," referring to the crowning or finishing ornament.',
                'language_origins': 'Latin',
                'example_sentence': 'The ornate brass _______ at the top of the stairway newel post was carved with intricate floral patterns.',
                'memory_tip': 'Remember "FIN-ial" - the FINal decorative touch, the ornament that FINishes off architectural details.'
            },
            'finicky': {
                'definition': 'Finicky describes someone who is extremely particular, fussy, or hard to please, especially about small details or minor matters. A finicky person shows excessive concern for precision, cleanliness, or exactness, often to the point of being difficult to satisfy. The word can apply to people, animals, or even machines that require very specific conditions to function properly. Finicky behavior often involves rejecting things that don\'t meet very high or specific standards.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FIN-i-kee',
                'etymology': 'Possibly from "finical," meaning overly precise, or related to "finicky," of uncertain origin but suggesting excessive attention to fine details.',
                'language_origins': 'English (uncertain origin)',
                'example_sentence': 'The _______ cat would only eat one specific brand of food served in a particular bowl.',
                'memory_tip': 'Remember "FIN-icky" - someone who\'s picky about every FINe detail, fussy to the point of being tricky to please.'
            },
            'finish': {
                'definition': 'Finish means to bring something to an end, to complete a task or activity, or to consume the last of something. As a noun, finish refers to the final appearance, texture, or surface treatment of an object, or the concluding part of something. Finish can describe the way something ends or concludes, such as a photo finish in a race. The word emphasizes completion, conclusion, and the final state or appearance of something.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'FIN-ish',
                'etymology': 'From Old French "finiss-," stem of "finir" meaning "to end," ultimately from Latin "finire" meaning "to limit" or "to end."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'She decided to _______ her homework before watching television for the evening.',
                'memory_tip': 'Remember "FIN-ish" - to reach the FIN (end) of something, to bring it to completion.'
            },
            'fipple': {
                'definition': 'A fipple is a wooden plug or block in the mouthpiece of certain wind instruments, such as recorders, penny whistles, or organ pipes, that directs the airflow to create sound. The fipple works by channeling air through a narrow slit against a sharp edge, causing vibrations that produce musical tones. This component is essential to the function of fipple flutes and similar instruments, determining both the instrument\'s playability and tonal characteristics. The design and positioning of the fipple significantly affect the instrument\'s sound quality.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FIP-ul',
                'etymology': 'Of uncertain origin, possibly from a dialectal word meaning "to play on a pipe" or related to the sound made by such instruments.',
                'language_origins': 'English (uncertain origin)',
                'example_sentence': 'The music student learned that the _______ in her recorder needed proper alignment to produce clear notes.',
                'memory_tip': 'Remember "FIP-ple" - the piece that helps wind instruments make sounds that go "FIP" when you play them.'
            },
            'firbolg': {
                'definition': 'A firbolg is a creature from Irish mythology, originally described as one of the supernatural races that inhabited Ireland before the arrival of the Celts. In ancient Irish legend, the Fir Bolg were one of the mythical peoples who ruled Ireland in succession. In modern fantasy literature and gaming, firbolgs are often portrayed as giant-like beings with connections to nature and druidic magic. They are typically depicted as peaceful, forest-dwelling creatures with strong ties to the natural world.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FEER-bolg',
                'etymology': 'From Irish "Fir Bolg," literally meaning "men of bags" or "men of the lightning," referring to a mythical race in Irish folklore.',
                'language_origins': 'Irish Gaelic',
                'example_sentence': 'In the fantasy novel, the _______ served as wise guardians of the ancient forest, protecting it from those who would harm nature.',
                'memory_tip': 'Remember "FIR-bolg" - mythical beings connected to FIR trees and forests, like gentle giants who are BOLD guardians of nature.'
            },
            'fire': {
                'definition': 'Fire is the rapid oxidation process that produces heat, light, and flame when combustible materials burn. This chemical reaction requires fuel, oxygen, and heat to sustain itself, creating one of humanity\'s most important discoveries for cooking, warmth, and protection. As a verb, fire can mean to ignite something, to dismiss someone from employment, or to shoot a weapon. Fire has deep symbolic meanings representing passion, destruction, purification, and energy across cultures.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FYR',
                'etymology': 'From Old English "fyr," related to similar words in other Germanic languages, ultimately from an Indo-European root meaning "fire."',
                'language_origins': 'Old English, Indo-European',
                'example_sentence': 'The campfire provided warmth and light as the family gathered around it on the cold evening.',
                'memory_tip': 'Remember "FIRE" - the burning force that\'s been essential to human survival, providing heat and light.'
            },
            'firefly': {
                'definition': 'A firefly is a nocturnal beetle that produces light through bioluminescence, creating a magical flickering effect in warm evening air. Also called lightning bugs, these insects generate light through a chemical reaction in their abdomens, using it primarily for mating communication. Fireflies are beloved for their enchanting displays during summer nights, often evoking childhood memories and romantic settings. Different species have distinct flashing patterns, colors, and timing that help them identify potential mates.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FYR-fly',
                'etymology': 'Compound word combining "fire" (referring to the light they produce) and "fly" (though they are actually beetles, not true flies).',
                'language_origins': 'English',
                'example_sentence': 'Children ran through the yard with mason jars, trying to catch the magical _______ that blinked like tiny lanterns.',
                'memory_tip': 'Remember "FIRE-fly" - insects that carry their own FIRE light as they FLY around on summer nights.'
            },
            'firenze': {
                'definition': 'Firenze is the Italian name for Florence, the capital city of Tuscany in central Italy, renowned for its art, architecture, and cultural heritage from the Renaissance period. The city is famous for masterpieces by Michelangelo, Leonardo da Vinci, and other great artists, as well as architectural marvels like the Duomo. Firenze was the birthplace of the Renaissance and remains a major tourist destination and cultural center. The name is used in Italian and by those who prefer the original Italian designation over the Anglicized "Florence."',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'fee-REN-zay',
                'etymology': 'From Latin "Florentia," meaning "flourishing," referring to the ancient Roman settlement that became the modern city.',
                'language_origins': 'Latin, Italian',
                'example_sentence': 'Art students from around the world travel to _______ to study Renaissance masterpieces in their original setting.',
                'memory_tip': 'Remember "Fi-REN-ze" - the Italian name for Florence, where the RENaissance flourished with amazing art and culture.'
            },
            'fires': {
                'definition': 'Fires is the plural form of fire, referring to multiple instances of combustion or burning. This can describe literal fires such as wildfires, campfires, or house fires, or metaphorical fires representing passions, conflicts, or intense situations. As a verb, fires means to ignite, shoot, or dismiss. The word encompasses both the physical phenomenon of combustion and various figurative meanings related to energy, intensity, and action.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'FYRZ',
                'etymology': 'Plural form of "fire," from Old English "fyr," or third person singular present tense of the verb "to fire."',
                'language_origins': 'Old English',
                'example_sentence': 'The drought conditions led to several dangerous _______ spreading across the mountainous regions.',
                'memory_tip': 'Remember "FIRES" - multiple flames burning, or when someone FIRES a gun or gets FIRED from a job.'
            },
            'fireworks': {
                'definition': 'Fireworks are pyrotechnic devices designed to produce spectacular displays of light, color, sound, and effects for entertainment and celebration. These devices contain various chemical compounds that create different colors, patterns, and sounds when ignited and launched into the air. Fireworks are traditionally used to celebrate holidays, festivals, and special occasions like New Year\'s Eve, Independence Day, and weddings. The displays combine artistry with chemistry to create memorable visual and auditory experiences that bring people together in celebration.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FYR-wurks',
                'etymology': 'Compound word combining "fire" and "works," referring to pyrotechnic devices that create fire-based displays.',
                'language_origins': 'English',
                'example_sentence': 'The spectacular _______ display lit up the night sky with brilliant colors during the Independence Day celebration.',
                'memory_tip': 'Remember "FIRE-works" - explosive devices that create beautiful FIRE displays that really WORK to amaze crowds.'
            },
            'firkin': {
                'definition': 'A firkin is a traditional English unit of measurement for liquids, particularly beer and ale, equal to one-fourth of a barrel or approximately 9 gallons (34 liters). This measurement was commonly used in brewing and was an important commercial standard for centuries. Firkins were also used as actual containers, typically made of wood, for storing and transporting beverages. The term remains in use today in traditional brewing contexts and historical references to liquid measurements.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FUR-kin',
                'etymology': 'From Middle English "ferdekyn," from Middle Dutch "vierdekijn," meaning "fourth part" (referring to one-fourth of a barrel).',
                'language_origins': 'Middle Dutch, Middle English',
                'example_sentence': 'The traditional brewery still measures their ale production in _______ to maintain historical accuracy.',
                'memory_tip': 'Remember "FIR-kin" - a measurement for beer, like asking "FIRst, how much is in the keg?" - about 9 gallons.'
            },
            'firmament': {
                'definition': 'Firmament refers to the heavens or sky, especially when viewed as a solid dome or vault arching over the earth. In biblical and ancient cosmology, the firmament was conceived as a solid barrier separating the waters above from the waters below. In literary and poetic contexts, firmament is used to describe the expanse of the sky, often with connotations of vastness, permanence, and divine creation. The word evokes the majesty and mystery of the celestial sphere.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FUR-muh-ment',
                'etymology': 'From Latin "firmamentum," meaning "strengthening" or "support," from "firmare" meaning "to make firm," referring to the solid sky dome in ancient cosmology.',
                'language_origins': 'Latin',
                'example_sentence': 'The ancient poet described the stars as jewels scattered across the vast _______ above.',
                'memory_tip': 'Remember "FIRM-ament" - the FIRM dome of the sky, the solid-seeming heavens that form the celestial vault.'
            },
            'firmly': {
                'definition': 'Firmly means in a strong, steady, or unwavering manner, with determination and resolve. When something is done firmly, it is executed with confidence, strength, and without hesitation or doubt. The adverb can describe physical actions performed with strength and stability, or mental and emotional states characterized by determination and conviction. Firmly suggests both physical solidity and moral or emotional steadfastness.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'FURM-lee',
                'etymology': 'From "firm" (from Latin "firmus" meaning "strong" or "solid") plus the adverb suffix "-ly."',
                'language_origins': 'Latin',
                'example_sentence': 'She _______ believed that education was the key to creating a better future for her children.',
                'memory_tip': 'Remember "FIRM-ly" - done in a FIRM manner, with solid determination and unwavering strength.'
            },
            'fiscal': {
                'definition': 'Fiscal relates to government revenue, taxation, and public expenditure, or more broadly to financial matters and budgets. Fiscal policy involves government decisions about spending and taxation to influence economic conditions. A fiscal year is a 12-month period used for accounting and budgeting purposes, which may not align with the calendar year. The term emphasizes the financial and budgetary aspects of government operations and organizational planning.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FIS-kul',
                'etymology': 'From Latin "fiscalis," from "fiscus" meaning "treasury" or "public revenue," originally referring to a woven basket used for holding money.',
                'language_origins': 'Latin',
                'example_sentence': 'The government implemented new _______ policies to reduce the national debt and stimulate economic growth.',
                'memory_tip': 'Remember "FISC-al" - relating to the FISC (treasury), about money and government financial matters.'
            },
            'fish': {
                'definition': 'Fish are aquatic vertebrates with gills, fins, and scales, living in water and breathing through gills. These animals represent one of the most diverse groups of vertebrates, ranging from tiny minnows to massive sharks. As a verb, fish means to attempt to catch fish or to search for something indirectly. Fish are crucial to aquatic ecosystems and human food systems, serving both ecological and economic functions. The word also appears in many idioms and expressions.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FISH',
                'etymology': 'From Old English "fisc," related to similar words in other Germanic languages, ultimately from an Indo-European root.',
                'language_origins': 'Old English, Indo-European',
                'example_sentence': 'The children were excited to _______ in the mountain lake during their summer camping trip.',
                'memory_tip': 'Remember "FISH" - aquatic animals that SWISH through water, or the activity of trying to catch them.'
            },
            'fission': {
                'definition': 'Fission is the process of splitting or dividing into two or more parts. In nuclear physics, fission refers to the splitting of atomic nuclei, which releases enormous amounts of energy and is the principle behind nuclear power and atomic weapons. In biology, fission describes a form of asexual reproduction where organisms divide into two or more parts, each capable of growing into a complete organism. The word emphasizes division, separation, and the creation of multiple parts from one original entity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FISH-un',
                'etymology': 'From Latin "fissio," from "fissus," past participle of "findere" meaning "to split" or "to cleave."',
                'language_origins': 'Latin',
                'example_sentence': 'Nuclear _______ reactions in the power plant generate electricity for thousands of homes in the region.',
                'memory_tip': 'Remember "FISS-ion" - the process of splitting apart, like a FISSURE that divides things into separate pieces.'
            },
            'fisticuffs': {
                'definition': 'Fisticuffs refers to fighting with the fists, particularly boxing or bare-knuckle combat. The term often carries a somewhat old-fashioned or humorous connotation, suggesting either formal boxing matches or informal scuffles settled with fists rather than weapons. Fisticuffs emphasizes physical combat using only the hands and fists, representing a direct, personal form of conflict resolution. The word evokes images of traditional boxing or gentlemanly disputes settled through physical prowess.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FIS-ti-kufs',
                'etymology': 'From "fist" plus "cuffs" (meaning blows), literally referring to fighting with fists and delivering blows.',
                'language_origins': 'English',
                'example_sentence': 'The disagreement between the two men was settled through old-fashioned _______ behind the tavern.',
                'memory_tip': 'Remember "FISTI-cuffs" - fighting with FISTS, throwing CUFFS (blows) with your hands instead of weapons.'
            },
            'fists': {
                'definition': 'Fists are hands with fingers clenched tightly together, typically used for striking or as a symbol of strength, anger, or determination. When someone makes a fist, they curl their fingers into their palm and clench them tightly, creating a compact, solid striking surface. Fists can represent aggression, power, solidarity, or resolve, and are used both in physical combat and as symbolic gestures. The word emphasizes the closed, clenched form of the hand prepared for action.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FISTS',
                'etymology': 'From Old English "fyst," related to similar words in other Germanic languages, referring to the closed hand.',
                'language_origins': 'Old English',
                'example_sentence': 'She raised her _______ in triumph after winning the championship boxing match.',
                'memory_tip': 'Remember "FISTS" - hands clenched tight, ready to TWIST and strike with force.'
            },
            'fitting': {
                'definition': 'Fitting can describe something that is appropriate, suitable, or proper for a particular situation or purpose. As a noun, fitting refers to a small part or component designed to connect, adjust, or complete something, such as plumbing fittings or clothing alterations. The word can also describe the process of adjusting something to ensure proper size, alignment, or suitability. Fitting emphasizes appropriateness, suitability, and proper adjustment.',
                'part_of_speech': 'adjective, noun, verb (present participle)',
                'pronunciation_guide': 'FIT-ing',
                'etymology': 'From "fit" (possibly from Middle English "fitten") plus the suffix "-ing," relating to suitability and adjustment.',
                'language_origins': 'Middle English',
                'example_sentence': 'It seemed _______ that the ceremony honoring teachers took place in the school\'s historic auditorium.',
                'memory_tip': 'Remember "FIT-ting" - something that FITs properly, appropriate and suitable for the situation.'
            },
            'five': {
                'definition': 'Five is the cardinal number between four and six, represented by the digit 5. This number holds significant cultural and mathematical importance, appearing in many natural phenomena like the five fingers on a human hand, five senses, and five-pointed stars. Five is considered a significant number in many cultures and belief systems. In mathematics, five is a prime number and appears in various geometric shapes and patterns. The number represents completion of one cycle and the beginning of another.',
                'part_of_speech': 'cardinal number, noun',
                'pronunciation_guide': 'FYV',
                'etymology': 'From Old English "fīf," related to similar numbers in other Indo-European languages, ultimately from a common ancestral root.',
                'language_origins': 'Old English, Indo-European',
                'example_sentence': 'She counted _______ shooting stars during the meteor shower last night.',
                'memory_tip': 'Remember "FIVE" - the number of fingers on one hand, helping you count and THRIVE in basic math.'
            },
            'fixed': {
                'definition': 'Fixed describes something that is securely attached, stationary, or unchanging. When something is fixed, it has been repaired, settled, or made stable and permanent. The word can describe physical objects that don\'t move, prices that don\'t change, or problems that have been resolved. Fixed can also describe something that has been predetermined or arranged in advance, such as a fixed schedule or fixed outcome.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'FIKST',
                'etymology': 'Past tense and past participle of "fix," from Latin "fixus," past participle of "figere" meaning "to fasten" or "to attach."',
                'language_origins': 'Latin',
                'example_sentence': 'The mechanic _______ the broken engine and the car runs perfectly now.',
                'memory_tip': 'Remember "FIXED" - something that\'s been made stable and secure, no longer broken or moving around.'
            },
            'fixity': {
                'definition': 'Fixity is the quality or state of being fixed, stable, or unchanging. This abstract noun describes the characteristic of permanence, steadiness, or lack of movement or variation. Fixity can refer to physical immobility, mental determination, or the stable nature of systems, relationships, or conditions. The word emphasizes the unchanging or permanent nature of something, suggesting reliability and consistency over time.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FIK-si-tee',
                'etymology': 'From "fix" (from Latin "figere" meaning "to fasten") plus the suffix "-ity" indicating a state or quality.',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ of his beliefs made it difficult for him to consider alternative viewpoints.',
                'memory_tip': 'Remember "FIX-ity" - the quality of being FIXed in place, stable and unchanging like concrete.'
            },
            'fjeld': {
                'definition': 'Fjeld (also spelled fjell) is a Scandinavian term referring to high, barren plateaus or mountainous areas above the tree line, characterized by rocky terrain and sparse vegetation. These elevated areas are common in Norway, Sweden, and other Nordic countries, representing distinct ecological zones where only hardy plants and animals can survive. Fjelds are important for understanding Arctic and alpine ecosystems, and they often serve as summer grazing areas for reindeer and other wildlife.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FYELD',
                'etymology': 'From Old Norse "fjall" meaning "mountain" or "fell," related to similar words in other Scandinavian languages.',
                'language_origins': 'Old Norse, Scandinavian',
                'example_sentence': 'The hikers crossed the windswept _______ where only lichens and hardy grasses could grow above the treeline.',
                'memory_tip': 'Remember "FJELD" - a FroJen (frozen) high mountain FIELD where few plants can grow in the harsh conditions.'
            },
            'flabbergast': {
                'definition': 'Flabbergast means to surprise, astonish, or overwhelm someone completely, leaving them speechless or bewildered. When someone is flabbergasted, they are so shocked or amazed that they cannot immediately respond or process what has happened. The word suggests a level of surprise that goes beyond mere astonishment to complete bewilderment or stupefaction. Flabbergast implies both the unexpectedness of the event and the profound impact it has on the person experiencing it.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'FLAB-er-gast',
                'etymology': 'Of uncertain origin, possibly combining "flabby" and "aghast," or from dialectal words meaning "to confound" or "to astound."',
                'language_origins': 'English (uncertain origin)',
                'example_sentence': 'The surprise announcement that she had won the lottery completely _______ the entire family.',
                'memory_tip': 'Remember "FLABBER-gast" - so shocked your jaw goes FLABBY and you GASP, completely overwhelmed by surprise.'
            },
            'flagellum': {
                'definition': 'A flagellum is a whip-like appendage that enables many microorganisms to move through liquid environments. These thread-like structures extend from the cell body and rotate or undulate to propel bacteria, sperm cells, and other microscopic organisms through water or other fluids. Flagella are crucial for cellular locomotion and are found in both prokaryotic and eukaryotic cells. The structure and movement of flagella represent one of nature\'s most elegant solutions for microscopic mobility.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fluh-JEL-um',
                'etymology': 'From Latin "flagellum," diminutive of "flagrum" meaning "whip" or "scourge," referring to the whip-like appearance and movement.',
                'language_origins': 'Latin',
                'example_sentence': 'Under the microscope, we could see the bacteria swimming by rapidly rotating their _______ structures.',
                'memory_tip': 'Remember "flag-ELLUM" - a tiny whip-like FLAG that helps cells ELLipse (move) through water like a propeller.'
            },
            'flagon': {
                'definition': 'A flagon is a large container, typically made of metal, ceramic, or glass, used for holding and serving beverages, particularly wine, ale, or other alcoholic drinks. Flagons usually have a narrow neck, a spout or lip for pouring, and often a handle, making them practical for serving at tables or gatherings. These vessels have been used for centuries in various cultures and are often decorative as well as functional, sometimes featuring elaborate designs or ceremonial significance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLAG-un',
                'etymology': 'From Old French "flascon," possibly from Germanic origins, related to "flask" and referring to a large bottle or container.',
                'language_origins': 'Old French, Germanic',
                'example_sentence': 'The medieval feast featured a large pewter _______ filled with spiced wine for the honored guests.',
                'memory_tip': 'Remember "FLAG-on" - a large container that you FLAG down to get more drinks, or wave like a FLAG when it needs refilling.'
            },
            'flags': {
                'definition': 'Flags are pieces of cloth or fabric, typically rectangular, bearing distinctive colors, patterns, or symbols that represent countries, organizations, or causes. Flags serve as symbols of identity, allegiance, and communication, used in ceremonies, celebrations, and official functions. As a verb, flags can mean to mark something for attention, to wave a flag, or to become weak or tired. Flags are powerful symbols that evoke patriotism, pride, and unity among groups of people.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'FLAGZ',
                'etymology': 'From Middle English "flagge," possibly from Old Norse "flaga" meaning "slab of stone," later applied to cloth banners.',
                'language_origins': 'Middle English, Old Norse',
                'example_sentence': 'The United Nations building displays _______ from all member countries in alphabetical order.',
                'memory_tip': 'Remember "FLAGS" - colorful cloth symbols that FLAP in the wind, representing nations and groups with pride.'
            },
            'flailed': {
                'definition': 'Flailed is the past tense of flail, meaning to wave, swing, or strike wildly and without control. When someone has flailed, they made energetic but uncontrolled movements, often with their arms or legs, typically in response to panic, excitement, or loss of balance. The word can also refer to beating grain with a flail (a farming tool) to separate seeds from stalks. Flailed suggests vigorous but ineffective or uncoordinated movement.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'FLAYLD',
                'etymology': 'From "flail," from Old English "flegil," from Latin "flagellum" meaning "whip," referring to the threshing tool and its motion.',
                'language_origins': 'Latin, Old English',
                'example_sentence': 'She _______ her arms wildly as she tried to regain her balance on the icy sidewalk.',
                'memory_tip': 'Remember "FLAILED" - moved arms wildly like a FLAIL tool, swinging without control or coordination.'
            },
            'flamboyant': {
                'definition': 'Flamboyant describes someone or something that is tending to attract attention through exuberant, colorful, or ostentatious behavior or appearance. When something is flamboyant, it is characterized by elaborate, showy, or dramatically expressive qualities that stand out from the ordinary. The word can describe fashion, personality, architecture, or any display that emphasizes boldness, creativity, and theatrical flair. Flamboyant suggests confidence and a willingness to be noticed.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'flam-BOY-ant',
                'etymology': 'From French "flamboyant," from "flamboyer" meaning "to flame," referring to flame-like decorative patterns in Gothic architecture.',
                'language_origins': 'French',
                'example_sentence': 'The performer\'s _______ costume featured bright feathers, sequins, and flowing ribbons that sparkled under the stage lights.',
                'memory_tip': 'Remember "FLAMBOY-ant" - like a FLAME that\'s BUOYANT, bright and showy, attracting attention with dramatic flair.'
            },
            'flambé': {
                'definition': 'Flambé is a cooking technique where alcohol is added to a dish and then ignited, creating dramatic flames that burn off the alcohol while leaving enhanced flavor. This spectacular culinary method is often performed tableside in restaurants for dramatic effect, with dishes like Bananas Foster or Cherries Jubilee. The flames typically burn for a few seconds, evaporating the alcohol content while concentrating the flavors. Flambé combines culinary skill with theatrical presentation, making dining an entertaining experience.',
                'part_of_speech': 'adjective, noun, verb',
                'pronunciation_guide': 'flam-BAY',
                'etymology': 'From French "flambé," past participle of "flamber" meaning "to flame" or "to burn," referring to the ignition process.',
                'language_origins': 'French',
                'example_sentence': 'The chef prepared Crepes Suzette _______ at our table, creating an impressive display of blue flames.',
                'memory_tip': 'Remember "flam-BAY" - a cooking technique where you set food on fire in a dramatic BLAZE, burning away alcohol.'
            },
            'flame': {
                'definition': 'Flame is the visible, gaseous part of a fire, characterized by light, heat, and often color produced during combustion. Flames result from the burning of gases released from fuel as it undergoes rapid oxidation. The word can also refer to intense passion, love, or anger, as in "old flame" (former romantic partner) or "flame of passion." Flames have symbolic meanings across cultures, representing purification, destruction, enlightenment, and spiritual energy.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FLAYM',
                'etymology': 'From Old French "flamme," from Latin "flamma," related to "flagrare" meaning "to burn" or "to blaze."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The candle\'s steady _______ cast dancing shadows on the walls of the dimly lit room.',
                'memory_tip': 'Remember "FLAME" - the bright, hot part of fire that can TAME darkness or inflame emotions.'
            },
            'flamingoes': {
                'definition': 'Flamingoes is an alternative plural form of flamingo, referring to multiple large, pink or red wading birds known for their distinctive curved beaks, long legs, and habit of standing on one leg. These tropical birds are famous for their vibrant coloring, which comes from carotenoid pigments in their diet of algae and small crustaceans. Flamingoes are highly social birds that gather in large flocks and are found in warm, shallow waters around the world.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'fluh-MING-gohz',
                'etymology': 'Alternative plural of "flamingo," from Spanish "flamenco," possibly from "flama" meaning "flame," referring to their bright coloring.',
                'language_origins': 'Spanish',
                'example_sentence': 'A flock of bright pink _______ waded through the shallow lagoon, creating a stunning natural spectacle.',
                'memory_tip': 'Remember "flaming-GOES" - bright pink birds that GO around in flaming (bright) colored flocks.'
            },
            'flamingos': {
                'definition': 'Flamingos is the standard plural form of flamingo, referring to these distinctive pink or red wading birds with long, curved necks, long legs, and specialized beaks for filter-feeding. Flamingos are known for their gregarious nature, forming large colonies that can number in the thousands. Their striking appearance and unique behaviors, such as standing on one leg and synchronized group movements, make them among the most recognizable and beloved birds worldwide.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'fluh-MING-gohz',
                'etymology': 'Plural of "flamingo," from Spanish "flamenco," possibly related to "flama" (flame) referring to their fiery coloration.',
                'language_origins': 'Spanish',
                'example_sentence': 'The wildlife photographer spent hours capturing images of the _______ as they performed their elaborate mating dances.',
                'memory_tip': 'Remember "flaming-OS" - bright birds that stand on one leg like the letter O, flaming pink in color.'
            },
            'flaneur': {
                'definition': 'A flaneur is a person who strolls leisurely through urban areas, observing city life with detached curiosity and aesthetic appreciation. The concept originated in 19th-century Paris, describing individuals who wandered the streets as a form of art, taking in the sights, sounds, and social dynamics of city life. Flaneurs are characterized by their contemplative approach to urban exploration, seeing the city as a text to be read and experienced rather than simply navigated. The term represents a particular attitude toward urban living and observation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'flah-NUR',
                'etymology': 'From French "flâneur," from "flâner" meaning "to stroll" or "to lounge," referring to leisurely urban wandering.',
                'language_origins': 'French',
                'example_sentence': 'As a true _______, he spent his afternoons wandering the city streets, observing the rhythm of urban life.',
                'memory_tip': 'Remember "fla-NEUR" - a person with NERVES calm enough to stroll and observe city life like a thoughtful urban explorer.'
            },
            'flannel': {
                'definition': 'Flannel is a soft, warm fabric typically made from wool, cotton, or synthetic fibers, characterized by a slightly napped or fuzzy surface that provides extra warmth and comfort. This versatile textile is commonly used for pajamas, sheets, shirts, and blankets due to its cozy feel and insulating properties. Flannel\'s brushed surface traps air, making it particularly suitable for cooler weather clothing and bedding. The fabric represents comfort, warmth, and casual, relaxed style.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLAN-ul',
                'etymology': 'Possibly from Welsh "gwlanen" meaning "woolen cloth," or from Old French "flane" meaning "blanket."',
                'language_origins': 'Welsh or Old French',
                'example_sentence': 'She wrapped herself in soft _______ pajamas before settling in to read by the fireplace.',
                'memory_tip': 'Remember "FLAN-nel" - fabric as soft and comforting as eating sweet FLAN, perfect for cozy clothing.'
            },
            'flapped': {
                'definition': 'Flapped is the past tense of flap, meaning to move up and down or back and forth with a quick, light motion, typically describing the movement of wings, fabric, or flexible objects in the wind. When something has flapped, it has moved in a repetitive, waving motion, often creating sound or air movement. The word can describe both natural movements like bird flight and artificial movements like flags or banners moving in the breeze.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'FLAPD',
                'etymology': 'From "flap," possibly imitative of the sound made by such movements, related to similar words in Germanic languages.',
                'language_origins': 'English (imitative origin)',
                'example_sentence': 'The bird _______ its wings vigorously as it took off from the branch.',
                'memory_tip': 'Remember "FLAPPED" - moved back and forth like something that SLAPPED the air repeatedly, creating a flapping sound.'
            },
            'flared': {
                'definition': 'Flared describes something that has widened or spread outward, typically in a gradual, smooth curve from a narrower base. The word can describe clothing styles like flared pants or skirts that widen toward the bottom, or physical phenomena like flared nostrils during intense emotion or exertion. Flared can also refer to sudden bursts of light, flame, or emotion that intensify rapidly. The term emphasizes the widening, spreading, or intensifying nature of whatever is being described.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'FLAIRD',
                'etymology': 'From "flare," possibly from Middle English "flaren," meaning to spread out or burst into flame.',
                'language_origins': 'Middle English',
                'example_sentence': 'Her _______ jeans were fashionable in the 1970s, widening dramatically from the knee downward.',
                'memory_tip': 'Remember "FLARED" - spread out wide like a FLARE that expands as it burns, widening from narrow to broad.'
            },
            'flashback': {
                'definition': 'A flashback is a narrative technique where the story temporarily shifts to an earlier time to provide background information, context, or insight into characters and events. In literature and film, flashbacks interrupt the chronological flow to reveal past experiences that illuminate present circumstances. The term can also refer to sudden, vivid memories of past events, often triggered by sensory experiences or emotional states. Flashbacks serve to deepen understanding and create connections between past and present.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLASH-bak',
                'etymology': 'Compound word combining "flash" (sudden, brief) and "back" (to the past), originally from cinematography.',
                'language_origins': 'English',
                'example_sentence': 'The movie used a _______ sequence to reveal the hero\'s traumatic childhood experiences.',
                'memory_tip': 'Remember "FLASH-back" - a sudden FLASH of memory that takes you BACK to an earlier time.'
            },
            'flask': {
                'definition': 'A flask is a narrow-necked container, typically made of glass, metal, or plastic, used for storing and transporting liquids. Flasks come in various forms, from laboratory equipment for scientific experiments to portable containers for carrying beverages. Hip flasks are small, flat containers designed to fit in pockets for discreet transport of alcoholic beverages. The narrow neck design makes flasks easy to pour from while minimizing spills and evaporation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLASK',
                'etymology': 'From Old English "flasce," related to Latin "flasco" meaning "bottle," possibly from Germanic origins.',
                'language_origins': 'Old English, Latin',
                'example_sentence': 'The hiker carried a stainless steel _______ filled with hot coffee to keep warm during the mountain trek.',
                'memory_tip': 'Remember "FLASK" - a narrow container that\'s handy to ASK for when you need to store liquids for travel.'
            },
            'flat': {
                'definition': 'Flat describes something that has a level, even surface without curves, bumps, or slopes. The word can refer to physical objects, landscapes, sounds, or abstract concepts. A flat surface is horizontal and smooth, while flat sound lacks variation in pitch. Flat can also mean lacking energy, interest, or flavor. In British English, flat refers to an apartment. The word emphasizes evenness, levelness, or lack of variation.',
                'part_of_speech': 'adjective, noun, adverb',
                'pronunciation_guide': 'FLAT',
                'etymology': 'From Old Norse "flatr" meaning "level" or "flat," related to similar words meaning "flat" in Germanic languages.',
                'language_origins': 'Old Norse',
                'example_sentence': 'The carpenter used a level to ensure the table surface was perfectly _______.',
                'memory_tip': 'Remember "FLAT" - level and even like a doormat, or like falling SPLAT on a flat surface.'
            },
            'flattery': {
                'definition': 'Flattery is excessive or insincere praise given to someone, typically with the intention of gaining favor, advantage, or manipulating their emotions. When someone engages in flattery, they offer compliments that may be exaggerated or untrue in order to please the recipient and achieve some personal goal. While flattery can sometimes be harmless social courtesy, it often carries negative connotations of deception and manipulation. The practice exploits human susceptibility to praise and ego gratification.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLAT-er-ee',
                'etymology': 'From Old French "flaterie," from "flater" meaning "to stroke" or "to caress," referring to soothing or pleasing someone.',
                'language_origins': 'Old French',
                'example_sentence': 'She could tell that his compliments were mere _______ designed to win her approval for his proposal.',
                'memory_tip': 'Remember "FLATTER-y" - insincere praise that makes people feel FLATTERED but is often empty and manipulative.'
            },
            'flauta': {
                'definition': 'A flauta is a Mexican dish consisting of a tortilla wrapped tightly around a filling (typically shredded meat or cheese) and then deep-fried until crispy. The name literally means "flute" in Spanish, referring to the rolled, tube-like shape of the prepared dish. Flautas are similar to taquitos but are traditionally made with flour tortillas and are often larger. They are commonly served with toppings such as guacamole, sour cream, salsa, and lettuce.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLAW-tah',
                'etymology': 'From Spanish "flauta" meaning "flute," referring to the cylindrical, flute-like shape of the rolled and fried tortilla.',
                'language_origins': 'Spanish',
                'example_sentence': 'The restaurant served crispy chicken _______ topped with fresh guacamole and salsa verde.',
                'memory_tip': 'Remember "FLAUTA" - a Mexican food shaped like a FLUTE, rolled tight and fried until crispy.'
            },
            'flavedo': {
                'definition': 'Flavedo is the outer, colored layer of citrus fruit peel, containing essential oils that give citrus fruits their characteristic aroma and much of their flavor. This outer layer, which includes the zest, is distinct from the white pith (albedo) underneath. The flavedo contains volatile oils, pigments, and aromatic compounds that are highly valued in cooking, perfumery, and flavoring. In citrus fruits like oranges, lemons, and limes, the flavedo provides the intense citrus essence used in culinary applications.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fluh-VEE-doh',
                'etymology': 'From Latin "flavedo," from "flavus" meaning "yellow," referring to the typically yellow or colored outer peel of citrus fruits.',
                'language_origins': 'Latin',
                'example_sentence': 'The chef carefully grated the lemon\'s _______ to add aromatic zest to the dessert without including the bitter white pith.',
                'memory_tip': 'Remember "flav-EDO" - the outer peel that gives citrus fruits their distinctive FLAVor, like the colorful EDge of the fruit.'
            },
            'flavored': {
                'definition': 'Flavored describes something that has been given a particular taste through the addition of flavoring agents, spices, extracts, or other substances that enhance or modify the original taste. When something is flavored, it has been intentionally modified to create a specific taste experience, whether sweet, savory, fruity, or any other desired flavor profile. This process is common in food and beverage production, where artificial or natural flavorings are added to create appealing taste combinations.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'FLAY-verd',
                'etymology': 'From "flavor" (from Old French "flaour," ultimately from Latin "flare" meaning "to blow") plus the suffix "-ed."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The children especially enjoyed the cherry-_______ medicine because it tasted like candy.',
                'memory_tip': 'Remember "FLAVOR-ed" - something that has been given extra FLAVOR, enhanced with taste-improving ingredients.'
            }
        }
        
        if word.lower() in batch_068_data:
            return batch_068_data[word.lower()]
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
        
        print("Batch 068 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch068Processor()
    
    input_file = "output/batch_068_words.csv"
    output_file = "output/batch_068_processed.csv"
    
    processor.process_batch(input_file, output_file)