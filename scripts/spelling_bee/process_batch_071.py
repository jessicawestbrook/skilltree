import pandas as pd
from typing import Dict
from dataclasses import dataclass

@dataclass
class WordData:
    definition: str = ""
    part_of_speech: str = ""
    pronunciation_guide: str = ""
    etymology: str = ""
    language_origins: str = ""
    example_sentence: str = ""
    memory_tip: str = ""
    phonetic_complexity: float = 0.0
    frequency_complexity: float = 0.0
    morphological_complexity: float = 0.0
    etymological_complexity: float = 0.0

class DifficultyCalculator:
    @staticmethod
    def calculate_phonetic_complexity(word: str) -> float:
        score = 0.0
        silent_letters = ['gh', 'kn', 'mb', 'mn', 'ps', 'pt', 'rh']
        unusual_combos = ['eau', 'ough', 'augh', 'ious', 'eous', 'sce', 'sci']
        
        for combo in silent_letters:
            if combo in word.lower():
                score += 0.3
                
        for combo in unusual_combos:
            if combo in word.lower():
                score += 0.2
                
        double_letters = len([i for i in range(len(word)-1) if word[i] == word[i+1]])
        score += double_letters * 0.1
        
        return min(score, 1.0)
    
    @staticmethod 
    def estimate_frequency(word: str) -> float:
        common_words = {'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'it'}
        if word.lower() in common_words:
            return 0.1
        elif len(word) <= 4:
            return 0.3
        elif len(word) <= 7:
            return 0.5
        else:
            return 0.8
    
    @staticmethod
    def calculate_morphological_complexity(word: str) -> float:
        prefixes = ['un', 're', 'pre', 'dis', 'over', 'under', 'out', 'up', 'mis', 'sub', 'inter', 'fore', 'de', 'trans', 'super', 'semi', 'anti', 'mid', 'non']
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'ness', 'ment', 'ful', 'less', 'able', 'ible', 'ous', 'eous', 'ious']
        
        morphemes = 1
        word_lower = word.lower()
        
        for prefix in prefixes:
            if word_lower.startswith(prefix):
                morphemes += 1
                break
                
        for suffix in suffixes:
            if word_lower.endswith(suffix):
                morphemes += 1
                break
                
        return min((morphemes - 1) * 0.3, 1.0)
    
    @staticmethod
    def calculate_etymological_complexity(etymology: str, language_origins: str) -> float:
        if not etymology or not language_origins:
            return 0.5
            
        complex_origins = ['Greek', 'Latin', 'Sanskrit', 'Hebrew', 'Arabic']
        simple_origins = ['English', 'Germanic', 'Old English']
        
        score = 0.5
        for origin in complex_origins:
            if origin.lower() in language_origins.lower():
                score += 0.2
                
        for origin in simple_origins:
            if origin.lower() in language_origins.lower():
                score -= 0.1
                
        return max(0.0, min(score, 1.0))

class Batch071Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for a word using Claude knowledge"""
        
        batch_071_data = {
            'formation': {
                'definition': 'Formation describes the process by which something develops, takes shape, or comes into existence, whether referring to geological processes that create rock structures, military arrangements of troops, or the development of ideas and institutions. In geology, formation specifically denotes distinct layers of rock or sediment that formed during particular time periods. The word also applies to organizational structures, educational processes, and developmental stages in various fields.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'for-MAY-shun',
                'etymology': 'From Latin "formatio" meaning "a shaping, fashioning," derived from "formare" (to form) plus the suffix "-tion" (indicating action or state).',
                'language_origins': 'Latin',
                'example_sentence': 'The geological _______ revealed layers of sediment deposited over millions of years.',
                'memory_tip': 'Remember "FORM-ation" - the ACTION (-ation) of giving FORM to something, like forming clay into pottery.'
            },
            'formed': {
                'definition': 'Formed is the past tense of "form," meaning something was shaped, created, or brought into existence in the past. It indicates that a process of development, organization, or construction has been completed. The word applies to physical objects that have been molded or shaped, organizations that have been established, or ideas and plans that have been developed and structured.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'FORMD',
                'etymology': 'From "form" (from Latin "forma" meaning "shape, figure") plus the past tense ending "-ed."',
                'language_origins': 'Latin',
                'example_sentence': 'The committee was _______ last year to address environmental concerns in the community.',
                'memory_tip': 'Remember "FORM-ed" - something that has been given FORM or shape in the past, like formed clay or a formed opinion.'
            },
            'former': {
                'definition': 'Former refers to something that existed, held a position, or had a particular quality in the past but no longer does so in the present. It indicates previous status, condition, or identity. As an adjective, it describes something that came before in time or sequence. The word emphasizes the contrast between past and present states, highlighting what something or someone used to be.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FOR-mer',
                'etymology': 'From Middle English, comparative form of "form" meaning "first, foremost," ultimately from Latin "formosus" (beautiful, well-formed).',
                'language_origins': 'Latin, Middle English',
                'example_sentence': 'The _______ president still maintains an office in the city where he once governed.',
                'memory_tip': 'Remember "FORMER" - what came beFORE, like a former job or former home you no longer have.'
            },
            'formica': {
                'definition': 'Formica refers to both a genus of ants and a trademark for a durable plastic laminate material commonly used for countertops and furniture surfaces. In biology, Formica ants are known for building large mounds and their complex social structures. The laminate material, invented in the early 1900s, was originally developed as an electrical insulator and later became popular for decorative and practical surfaces due to its durability and easy maintenance.',
                'part_of_speech': 'noun (proper noun when referring to the brand)',
                'pronunciation_guide': 'for-MY-kah',
                'etymology': 'From Latin "formica" meaning "ant." The laminate brand was named after the insect, possibly due to the industrious nature associated with ants.',
                'language_origins': 'Latin',
                'example_sentence': 'The kitchen countertops were made of _______ laminate in a wood-grain pattern.',
                'memory_tip': 'Remember "FORMICA" sounds like "for MY car" - both the ant and the laminate are known for being tough and hardworking.'
            },
            'forms': {
                'definition': 'Forms can function as either a noun (plural of form) or a verb (third person singular present of form). As a noun, it refers to shapes, structures, types, or varieties of something, including documents with blank spaces to fill out. As a verb, it means creates, shapes, or establishes something. Forms are fundamental concepts in many fields, from geometry (geometric forms) to bureaucracy (application forms) to biology (life forms).',
                'part_of_speech': 'noun (plural), verb (third person singular)',
                'pronunciation_guide': 'FORMZ',
                'etymology': 'From Latin "forma" meaning "shape, figure, appearance" with the plural ending "-s" or present tense third person singular ending.',
                'language_origins': 'Latin',
                'example_sentence': 'Please complete all the required _______ before submitting your application.',
                'memory_tip': 'Remember "FORMS" - multiple FORMS like application forms, or the action of forming multiple things.'
            },
            'forsook': {
                'definition': 'Forsook is the past tense of "forsake," meaning deliberately abandoned, deserted, or gave up something or someone that was previously valued or depended upon. It implies a conscious decision to leave behind or reject what was once important. The word carries connotations of betrayal or abandonment, often used in contexts involving relationships, beliefs, principles, or responsibilities that were once held dear.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'for-SOOK',
                'etymology': 'From Old English "forsacan" meaning "to deny, refuse, or renounce," composed of "for-" (away, completely) plus "sacan" (to strive, contend).',
                'language_origins': 'Old English',
                'example_sentence': 'He _______ his comfortable life in the city to pursue his dreams in the wilderness.',
                'memory_tip': 'Remember "for-SOOK" - sounds like "for SHOOK," as in shook off or abandoned something important.'
            },
            'forsooth': {
                'definition': 'Forsooth is an archaic English word meaning "in truth" or "indeed," used to emphasize the truthfulness of a statement. It was commonly used in medieval and Renaissance English as an assertion of honesty or certainty. In modern usage, the word is sometimes employed ironically or humorously to give speech an old-fashioned, theatrical quality, often suggesting mock seriousness or affected formality.',
                'part_of_speech': 'adverb (archaic)',
                'pronunciation_guide': 'for-SOOTH',
                'etymology': 'From Middle English, literally meaning "for sooth" where "sooth" meant "truth." Composed of "for" (indeed, truly) plus "sooth" (truth).',
                'language_origins': 'Middle English, Old English',
                'example_sentence': '"_______, good sir, I speak nothing but the truth about this matter," declared the medieval knight.',
                'memory_tip': 'Remember "for-SOOTH" - "for the TRUTH" or speaking truthfully, like swearing "for the truth of it."'
            },
            'fortification': {
                'definition': 'Fortification refers to the act of strengthening or protecting something, or to defensive structures built to protect against attack. In military contexts, fortifications are walls, barriers, trenches, or other defensive works designed to provide protection during warfare. The term also applies metaphorically to strengthening anything against potential threats, such as fortifying the body with vitamins or fortifying one\'s resolve through determination.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'for-tuh-fuh-KAY-shun',
                'etymology': 'From Latin "fortificatio" meaning "a strengthening," derived from "fortificare" (to strengthen) which combines "fortis" (strong) plus "facere" (to make).',
                'language_origins': 'Latin',
                'example_sentence': 'The ancient _______ still stands as a testament to medieval engineering and military strategy.',
                'memory_tip': 'Remember "FORT-ification" - making something as strong as a FORT, like fortifying defenses or fortifying your health.'
            },
            'fortificationnoun': {
                'definition': 'This appears to be a corrupted entry where "fortification" and "noun" were incorrectly combined during PDF processing. This represents a data quality issue where the word "fortification" (meaning defensive military structures or the act of strengthening) was merged with grammatical notation indicating it is a noun. The intended word should be "fortification" referring to defensive works or strengthening processes.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'for-tuh-fuh-KAY-shun-NOUN',
                'etymology': 'Corrupted combination of "fortification" (from Latin "fortificatio") and the English word "noun."',
                'language_origins': 'Latin, English (corrupted)',
                'example_sentence': 'This word entry contains a parsing error where _______ should be separated into "fortification" and grammatical notation.',
                'memory_tip': 'This is a data error - remember that "fortification" and "noun" should be separate, not combined as "fortificationnoun."'
            },
            'fortissimo': {
                'definition': 'Fortissimo is a musical term indicating that a passage should be played or sung very loudly with maximum volume and intensity. It represents the loudest dynamic marking in music, typically abbreviated as "ff" in musical notation. The term is used by composers to instruct performers to play with great force and power. Beyond music, the word is sometimes used metaphorically to describe anything done with maximum intensity or volume.',
                'part_of_speech': 'adverb, noun (musical term)',
                'pronunciation_guide': 'for-tih-SEE-moh',
                'etymology': 'From Italian "fortissimo," the superlative form of "forte" (strong, loud), literally meaning "very strong" or "strongest."',
                'language_origins': 'Italian',
                'example_sentence': 'The orchestra played the final movement _______, filling the concert hall with thunderous sound.',
                'memory_tip': 'Remember "FORTISSIMO" - the superlative of forte (loud), meaning the STRONGEST and loudest possible in music.'
            },
            'fortuitous': {
                'definition': 'Fortuitous means happening by chance or accident, particularly in a favorable or fortunate manner. It describes events that occur unexpectedly but turn out to be beneficial or lucky. The word emphasizes the random nature of the occurrence while often implying a positive outcome. In careful usage, fortuitous specifically means "by chance" rather than simply "fortunate," though the distinction has blurred in common usage.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'for-TOO-ih-tus',
                'etymology': 'From Latin "fortuitus" meaning "happening by chance," derived from "fors" (chance, luck) related to "fortuna" (fortune).',
                'language_origins': 'Latin',
                'example_sentence': 'Their meeting was entirely _______, as neither had planned to attend the conference.',
                'memory_tip': 'Remember "FORTUITOUS" contains "fort-YOU-itous" - fortune came TO YOU by chance, not by planning.'
            },
            'fortune': {
                'definition': 'Fortune refers to chance, luck, or fate that influences human affairs, often determining success or failure in life. It can mean good luck (good fortune) or the general circumstances that befall someone. Fortune also refers to a large amount of wealth or money accumulated over time. The concept encompasses both the unpredictable nature of life\'s events and material prosperity, reflecting humanity\'s relationship with both chance and wealth.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOR-chun',
                'etymology': 'From Latin "fortuna" meaning "luck, chance, fate," derived from "fors" (chance). Related to Fortuna, the Roman goddess of fortune and luck.',
                'language_origins': 'Latin',
                'example_sentence': 'She built her _______ through wise investments and careful financial planning.',
                'memory_tip': 'Remember "FORTUNE" - what FATE brings you, whether good luck or wealth that comes your way.'
            },
            'forty': {
                'definition': 'Forty is the cardinal number equivalent to four tens, written as 40 in digits. It represents a quantity that is one more than thirty-nine and one less than forty-one. The number appears frequently in cultural and religious contexts, such as the forty days and nights of rain during the biblical flood, Jesus\'s forty days in the wilderness, or the expression "forty winks" meaning a short nap.',
                'part_of_speech': 'number, adjective, noun',
                'pronunciation_guide': 'FOR-tee',
                'etymology': 'From Old English "feowertig," literally meaning "four tens," composed of "feower" (four) plus "tig" (group of ten).',
                'language_origins': 'Old English',
                'example_sentence': 'The treasure map indicated that the gold was buried _______ paces from the old oak tree.',
                'memory_tip': 'Remember "FORTY" - note it\'s spelled without the "u" from "four," making it FOR-ty, not "four-ty."'
            },
            'forza': {
                'definition': 'Forza is an Italian word meaning "strength," "force," or "power," commonly used as an exclamation of encouragement equivalent to "come on!" or "go for it!" in English. In sports contexts, particularly soccer, fans chant "Forza" followed by their team name to show support and encouragement. The word embodies the concept of pushing forward with determination and vigor, expressing both physical strength and emotional intensity.',
                'part_of_speech': 'noun, interjection',
                'pronunciation_guide': 'FOR-tsah',
                'etymology': 'From Latin "fortia" meaning "strong things," related to "fortis" (strong, brave). Evolved through Vulgar Latin into Italian "forza."',
                'language_origins': 'Latin, Italian',
                'example_sentence': '"_______!" shouted the crowd, encouraging their team to push harder in the final minutes.',
                'memory_tip': 'Remember "FORZA" - sounds like "FORCE-ah," expressing strength and force with Italian passion and energy.'
            },
            'fossiliferous': {
                'definition': 'Fossiliferous describes rock formations, geological layers, or sedimentary deposits that contain fossils or are rich in fossilized remains of ancient organisms. This geological term is used to identify strata that yield significant fossil specimens, making them important for paleontological study and understanding Earth\'s biological history. Fossiliferous rocks provide crucial evidence for dating geological periods and reconstructing ancient ecosystems.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'foss-uh-LIF-er-us',
                'etymology': 'From Latin "fossilis" (dug up, from "fodere" to dig) plus "ferre" (to bear, carry) plus the suffix "-ous" (full of), literally meaning "fossil-bearing."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ limestone contained numerous marine fossils from the Paleozoic era.',
                'memory_tip': 'Remember "FOSSIL-IFEROUS" - rocks that are fossil-FERous (bearing fossils), like coniferous trees bear cones.'
            },
            'foster': {
                'definition': 'Foster means to encourage, promote, or help develop something positive, such as growth, learning, or relationships. It can also refer to providing temporary care for children who cannot live with their biological parents. As a verb, foster emphasizes nurturing and supportive action that enables development or improvement. The word implies active care and attention designed to help something or someone flourish.',
                'part_of_speech': 'verb, adjective',
                'pronunciation_guide': 'FOS-ter',
                'etymology': 'From Old English "fostrian" meaning "to nourish, rear, support," derived from "fostor" (food, nourishment) related to "foda" (food).',
                'language_origins': 'Old English',
                'example_sentence': 'The mentorship program was designed to _______ creativity and innovation among young entrepreneurs.',
                'memory_tip': 'Remember "FOSTER" - like a foster parent who helps a child grow and develop with care and support.'
            },
            'foudroyant': {
                'definition': 'Foudroyant describes something that is sudden, overwhelming, and striking like lightning or thunder, often used in medical contexts to describe rapidly developing and severe symptoms or conditions. The word conveys the sense of something that appears suddenly with devastating or stunning effect. It can also describe anything that is dazzling, brilliant, or impressively forceful in its impact or appearance.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'foo-DROY-ant',
                'etymology': 'From French "foudroyant," present participle of "foudroyer" (to strike with lightning), from "foudre" (lightning, thunderbolt), ultimately from Latin "fulgur."',
                'language_origins': 'French, Latin',
                'example_sentence': 'The patient developed a _______ infection that required immediate intensive care treatment.',
                'memory_tip': 'Remember "FOUDROYANT" - sounds like "FOUL-ROYANT," like being struck by foul weather or lightning suddenly and powerfully.'
            },
            'fouetté': {
                'definition': 'Fouetté is a classical ballet term describing a turning movement where the dancer whips one leg around while spinning on the other foot, creating a rapid rotational motion. The word literally means "whipped" in French, referring to the whip-like motion of the working leg. This challenging ballet technique requires exceptional balance, strength, and coordination, and is often featured in classical variations as a display of technical virtuosity.',
                'part_of_speech': 'noun (ballet term)',
                'pronunciation_guide': 'foo-eh-TAY',
                'etymology': 'From French "fouetté," past participle of "fouetter" meaning "to whip," from "fouet" (whip), ultimately from Latin "fagus" (beech tree, from which whips were made).',
                'language_origins': 'French, Latin',
                'example_sentence': 'The ballerina performed thirty-two consecutive _______ turns, demonstrating her exceptional technique.',
                'memory_tip': 'Remember "FOUETTÉ" - the leg WHIPs around like a "FOO-et-TAY" whip motion in ballet turns.'
            },
            'found': {
                'definition': 'Found serves as both the past tense of "find" (discovered or located something) and as a separate verb meaning to establish or create something new, such as an institution, organization, or settlement. When used as the past tense of find, it indicates that something previously lost or sought was discovered. As an independent verb, found means to lay the groundwork or basis for something that will continue to exist and develop.',
                'part_of_speech': 'verb (past tense of find, or present tense meaning establish)',
                'pronunciation_guide': 'FOWND',
                'etymology': 'As past tense of "find": from Old English "findan." As "establish": from Latin "fundare" meaning "to lay the bottom, establish," from "fundus" (bottom, foundation).',
                'language_origins': 'Old English, Latin',
                'example_sentence': 'She _______ the missing keys under the couch cushions where they had fallen.',
                'memory_tip': 'Remember "FOUND" - either discovered something that was lost, or established a new foundation like founding a company.'
            },
            'founded': {
                'definition': 'Founded is the past tense of "found" meaning established, created, or set up an institution, organization, city, or system. It indicates that something was brought into existence with a specific purpose and structure, typically with the intention of lasting into the future. The word implies the creation of something substantial and enduring, often involving formal establishment with rules, principles, or foundations.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'FOWN-ded',
                'etymology': 'From Latin "fundare" meaning "to lay the foundation, establish," derived from "fundus" (bottom, base) plus the past tense ending "-ed."',
                'language_origins': 'Latin',
                'example_sentence': 'The university was _______ in 1636 and has been educating students for nearly four centuries.',
                'memory_tip': 'Remember "FOUND-ed" - something that was given a solid FOUNDATION in the past, like a city or organization.'
            },
            'fountain': {
                'definition': 'A fountain is a decorative water feature that shoots or flows water upward or through designed channels, often serving both aesthetic and practical purposes. Fountains can be natural spring sources or artificial structures created for decoration, drinking water access, or cooling effects. The word also refers metaphorically to any abundant source or origin of something desirable, as in "fountain of youth" or "fountain of knowledge."',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOWN-tin',
                'etymology': 'From Old French "fontaine," from Latin "fontana" (of a spring), derived from "fons" (spring, source of water).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The ornate marble _______ in the center of the plaza provided both beauty and a place to rest.',
                'memory_tip': 'Remember "FOUNTAIN" - water that goes UP from a FOUNT (source), creating beautiful water displays or drinking spots.'
            },
            'four': {
                'definition': 'Four is the cardinal number that comes after three and before five, representing a quantity of items equal to 2+2. It is considered a stable and balanced number in many cultures, often associated with completeness (four seasons, four directions, four elements). In mathematics, four is the smallest composite number and the first perfect square greater than one (2²=4).',
                'part_of_speech': 'number, adjective, noun',
                'pronunciation_guide': 'FORE',
                'etymology': 'From Old English "feower," related to Latin "quattuor" and Greek "tessares," all derived from Proto-Indo-European "*kʷetwores."',
                'language_origins': 'Old English, Proto-Indo-European',
                'example_sentence': 'The table had _______ legs and could comfortably seat eight people.',
                'memory_tip': 'Remember "FOUR" - sounds like "FORE!" in golf, and there are four suits in playing cards.'
            },
            'fourth': {
                'definition': 'Fourth is the ordinal number corresponding to the cardinal number four, indicating position in a sequence (1st, 2nd, 3rd, 4th). It represents something that comes after the third item in order. The word is also used to describe one part of something divided into four equal portions (one-fourth or a quarter). In music, a fourth refers to an interval spanning four scale degrees.',
                'part_of_speech': 'ordinal number, adjective, noun',
                'pronunciation_guide': 'FORTH',
                'etymology': 'From Old English "feowertha," formed from "feower" (four) plus the ordinal suffix "-tha" (equivalent to modern "-th").',
                'language_origins': 'Old English',
                'example_sentence': 'She finished in _______ place in the marathon, just missing the podium.',
                'memory_tip': 'Remember "FOURTH" - the position that comes after third, like the "Fourth of July" holiday.'
            },
            'fowl': {
                'definition': 'Fowl refers to domesticated birds raised for their meat, eggs, or feathers, including chickens, ducks, geese, and turkeys. The term can also encompass wild birds, particularly game birds hunted for food. In a broader sense, fowl describes any bird, though it is most commonly used in agricultural and culinary contexts. The word emphasizes the practical relationship between humans and birds as sources of food and materials.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOWL',
                'etymology': 'From Old English "fugol" meaning "bird," related to German "Vogel" and ultimately from Proto-Germanic "*fuglaz."',
                'language_origins': 'Old English, Proto-Germanic',
                'example_sentence': 'The farm raised various types of _______ including chickens, ducks, and geese.',
                'memory_tip': 'Remember "FOWL" sounds like "FOUL" but refers to birds - think of fowl flying around the farmyard.'
            },
            'foxes': {
                'definition': 'Foxes is the plural form of fox, referring to multiple small to medium-sized carnivorous mammals known for their intelligence, cunning behavior, and distinctive bushy tails. Foxes are found worldwide and are characterized by their pointed ears, narrow snouts, and typically reddish-brown fur, though color variations exist. The word is also used metaphorically to describe clever or sly people.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FOK-siz',
                'etymology': 'From Old English "fox," related to Proto-Germanic "*fuhsaz." The plural form adds "-es" because "fox" ends in "x."',
                'language_origins': 'Old English, Proto-Germanic',
                'example_sentence': 'The wildlife photographer captured images of two red _______ playing in the forest clearing.',
                'memory_tip': 'Remember "FOXES" - multiple sly FOX animals, adding "-es" because fox ends with "x" (like boxes, mixes).'
            },
            'foyer': {
                'definition': 'A foyer is an entrance hall, lobby, or vestibule in a building, typically located near the main entrance and serving as a transitional space between the outside and interior rooms. In theaters, the foyer is the area where audiences gather before performances and during intermissions. The space often serves both practical and aesthetic functions, providing a place to remove coats and creating an impressive first impression for visitors.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FOY-er or foy-YAY',
                'etymology': 'From French "foyer" meaning "fireplace, hearth," from Latin "focarius" (of the hearth), derived from "focus" (fireplace, hearth).',
                'language_origins': 'French, Latin',
                'example_sentence': 'Guests gathered in the elegant _______ before being seated for dinner.',
                'memory_tip': 'Remember "FOYER" - the FORE-area you enter first, like the hearth (foyer) where people once gathered.'
            },
            'frabjous': {
                'definition': 'Frabjous is a whimsical, nonsense word created by Lewis Carroll in his poem "Jabberwocky" from "Through the Looking-Glass." It is used to express great joy, delight, or exuberance, suggesting a feeling of fabulous happiness. Though originally a made-up word, frabjous has entered English usage as an expression of exultant joy. Carroll\'s creation demonstrates how inventive language can convey emotion even without traditional meaning.',
                'part_of_speech': 'adjective (nonsense word)',
                'pronunciation_guide': 'FRAB-jus',
                'etymology': 'Coined by Lewis Carroll in 1871, likely a blend of "fabulous" and "joyous," though Carroll never explained its exact derivation.',
                'language_origins': 'English (invented by Lewis Carroll)',
                'example_sentence': 'The children were absolutely _______ when they discovered the surprise party waiting for them.',
                'memory_tip': 'Remember "FRABJOUS" - sounds like "FAB-joyous," meaning fabulously joyous, created by Lewis Carroll.'
            },
            'fracas': {
                'definition': 'A fracas is a noisy disturbance, quarrel, or brawl, typically involving multiple people and characterized by disorder and confusion. It suggests a chaotic situation with raised voices, commotion, and often physical altercation. The word implies a temporary but intense disruption of peace, often arising suddenly from disagreement or conflict. Fracas emphasizes the disorderly and tumultuous nature of the disturbance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FRAY-kas or frah-KAH',
                'etymology': 'From French "fracas" meaning "crash, din," from Italian "fracasso" (uproar, crash), ultimately from "fracassare" (to shatter).',
                'language_origins': 'French, Italian',
                'example_sentence': 'The political debate turned into a _______ when supporters from both sides began shouting at each other.',
                'memory_tip': 'Remember "FRACAS" - sounds like "FRACK-us," like something that could fracture or break apart in a noisy fight.'
            },
            'fractions': {
                'definition': 'Fractions are mathematical expressions representing parts of a whole, written as one number (numerator) divided by another (denominator), such as 1/2 or 3/4. They indicate portions or ratios and are fundamental concepts in arithmetic and mathematics. Fractions can represent quantities less than one, equal to one, or greater than one. The word also refers to small parts or portions of anything, emphasizing the concept of division into smaller components.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FRAK-shuns',
                'etymology': 'From Latin "fractio" meaning "a breaking," from "frangere" (to break) plus the plural suffix "-s."',
                'language_origins': 'Latin',
                'example_sentence': 'The math teacher explained how to add _______ with different denominators.',
                'memory_tip': 'Remember "FRACTIONS" - parts that are FRACTured or broken from the whole, like 1/2 or 3/4.'
            },
            'fractious': {
                'definition': 'Fractious describes someone or something that is irritable, quarrelsome, or difficult to control or manage. It characterizes a person, group, or situation that is prone to causing trouble, showing defiance, or creating dissension. The word suggests a temperament that is easily provoked to anger or rebellion, making cooperation or harmony challenging to achieve. Fractious behavior often involves stubbornness and resistance to authority.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FRAK-shus',
                'etymology': 'From Latin "fractiosus," derived from "fractio" (a breaking) from "frangere" (to break), suggesting something that tends to break apart or cause division.',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ committee members could never agree on budget allocations, leading to constant arguments.',
                'memory_tip': 'Remember "FRACTIOUS" - like causing FRACTURES or breaks in relationships through quarrelsome behavior.'
            },
            'fragile': {
                'definition': 'Fragile describes something that is easily broken, damaged, or destroyed, requiring careful handling due to its delicate nature. The word applies to physical objects that can shatter or break easily, as well as to emotional states, relationships, or situations that are vulnerable and unstable. Fragile suggests inherent weakness or sensitivity that makes something susceptible to harm from even minor stress or impact.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FRAJ-ile or fra-JEEL',
                'etymology': 'From Latin "fragilis" meaning "easily broken," derived from "frangere" (to break).',
                'language_origins': 'Latin',
                'example_sentence': 'Please handle the antique vase carefully, as it is extremely _______.',
                'memory_tip': 'Remember "FRAGILE" - sounds like it could FRACTURE easily, needing gentle handling like fine glass.'
            },
            'fragment': {
                'definition': 'A fragment is a small piece or portion broken off from something larger, incomplete by itself and representing only part of an original whole. The word applies to physical pieces (fragments of pottery), literary works (sentence fragments), or any incomplete portion of something that was once complete. Fragments often provide clues about the nature of the original whole, whether in archaeology, literature, or other fields.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FRAG-ment (noun), frag-MENT (verb)',
                'etymology': 'From Latin "fragmentum" meaning "a piece broken off," derived from "frangere" (to break).',
                'language_origins': 'Latin',
                'example_sentence': 'Archaeologists discovered a _______ of ancient pottery that revealed details about the civilization.',
                'memory_tip': 'Remember "FRAGMENT" - a piece that was FRAGmented or broken off from something larger.'
            },
            'fragrance': {
                'definition': 'Fragrance refers to a sweet, pleasant smell or scent, typically one that is delicate and appealing to the senses. The word encompasses natural aromas from flowers, foods, or other sources, as well as manufactured perfumes and scented products. Fragrance suggests a positive olfactory experience that is often associated with beauty, cleanliness, or luxury. The term implies a more refined or desirable scent than simply "smell" or "odor."',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FRAY-grance',
                'etymology': 'From Latin "fragrantia," derived from "fragrare" (to smell sweet) related to "fragrans" (sweet-smelling).',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ of jasmine filled the evening air in the garden.',
                'memory_tip': 'Remember "FRAGRANCE" - a sweet scent that is FRAG-rant and pleasant, like flowers or perfume.'
            },
            'fragrant': {
                'definition': 'Fragrant describes something that emits a sweet, pleasant, or delightful scent that is appealing to smell. The word characterizes natural or artificial sources of agreeable aromas, such as flowers, herbs, perfumes, or cooking food. Fragrant suggests not just the presence of smell, but specifically a desirable and attractive olfactory quality that draws positive attention and creates a pleasant sensory experience.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FRAY-grant',
                'etymology': 'From Latin "fragrans" meaning "sweet-smelling," present participle of "fragrare" (to smell sweet, emit a scent).',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ herbs in the garden attracted bees and butterflies throughout the summer.',
                'memory_tip': 'Remember "FRAGRANT" - something that has a pleasant scent that you want to take a FRAGRANT whiff of.'
            },
            'frailty': {
                'definition': 'Frailty refers to the condition of being weak, delicate, or vulnerable to harm, whether in physical, emotional, or moral contexts. It describes the inherent weakness or susceptibility that makes someone or something fragile and easily damaged. The word often applies to human vulnerability, particularly in old age or illness, but can also describe moral weakness or the delicate nature of systems, relationships, or objects.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FRAYL-tee',
                'etymology': 'From Old French "fraileté," derived from Latin "fragilitas" meaning "brittleness, weakness," from "fragilis" (fragile).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The patient\'s physical _______ required constant medical monitoring and gentle care.',
                'memory_tip': 'Remember "FRAILTY" - the state of being FRAIL, weak and vulnerable like delicate glass or aging bodies.'
            },
            'framboise': {
                'definition': 'Framboise is the French word for raspberry, used in English primarily in culinary contexts to describe raspberry-flavored foods, beverages, or ingredients. In the culinary world, framboise often refers to raspberry liqueur, vinegar, or other gourmet preparations that emphasize the sophisticated or authentic French approach to raspberry flavoring. The word suggests a more refined or elegant presentation than simply "raspberry."',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fram-BWAHZ',
                'etymology': 'From French "framboise" meaning "raspberry," possibly derived from a Frankish word related to "bramble."',
                'language_origins': 'French',
                'example_sentence': 'The dessert was drizzled with _______ reduction that perfectly complemented the chocolate.',
                'memory_tip': 'Remember "FRAMBOISE" - the fancy French way to say raspberry, sounds like "FRAM-bwaz" for gourmet cooking.'
            },
            'frames': {
                'definition': 'Frames can refer to structural borders or supports that enclose, support, or give shape to something, such as picture frames, door frames, or eyeglass frames. The word also describes the basic structure or skeleton of buildings, vehicles, or other constructions. Additionally, frames can mean individual images in a series (film frames) or time periods in contexts like sports or games. As a verb form, it means to construct, enclose, or present something within a framework.',
                'part_of_speech': 'noun (plural), verb (third person singular)',
                'pronunciation_guide': 'FRAYMZ',
                'etymology': 'From Old English "framian" meaning "to profit, avail," later developing the sense of "to construct, build," related to "fram" (forward, bold).',
                'language_origins': 'Old English',
                'example_sentence': 'The old wooden window _______ needed replacement after decades of weather damage.',
                'memory_tip': 'Remember "FRAMES" - structures that FRAME or border things, like picture frames or building frames.'
            },
            'franca': {
                'definition': 'Franca typically appears as part of "lingua franca," referring to a language used as a bridge between speakers of different native languages, serving as a common means of communication in trade, diplomacy, or other interactions. The term originates from a Mediterranean trade language. When used alone, franca may refer to this concept of a bridging or common language, though it is more commonly encountered as part of the full phrase "lingua franca."',
                'part_of_speech': 'noun (usually part of "lingua franca")',
                'pronunciation_guide': 'FRAN-kah',
                'etymology': 'From Italian "lingua franca" literally meaning "Frankish language," referring to the mixed language used in Mediterranean trade.',
                'language_origins': 'Italian, historically Frankish',
                'example_sentence': 'In the historical trading ports, a simple _______ developed to facilitate commerce between different cultures.',
                'memory_tip': 'Remember "FRANCA" - part of "lingua franca," the FRANK (honest, open) language that everyone could use for trade.'
            },
            'francatriforium': {
                'definition': 'Francatriforium appears to be a combined word error, likely representing a PDF parsing mistake where multiple distinct terms were incorrectly merged together. This could involve "franca" (as in lingua franca) combined with "triforium" (an architectural term for a gallery in church architecture). This represents a data quality issue where separate words or concepts were improperly joined during text extraction or processing.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'FRAN-kah-try-FOR-ee-um',
                'etymology': 'Corrupted combination likely involving "franca" and "triforium" (from Latin "triforium," an architectural term).',
                'language_origins': 'Multiple languages (corrupted)',
                'example_sentence': 'The word _______ appears to be a data processing error combining separate architectural and linguistic terms.',
                'memory_tip': 'This is a data error - remember that this should be separated into "franca" and "triforium," not combined as one word.'
            },
            'france': {
                'definition': 'France is a Western European country known for its rich culture, history, cuisine, and contributions to art, philosophy, and science. As a proper noun, it refers to the French Republic, a nation with its capital in Paris. France has played a significant role in world history, from medieval times through modern democratic movements, and is renowned for its language, literature, fashion, and culinary traditions.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'FRANS',
                'etymology': 'From Latin "Francia" meaning "land of the Franks," derived from "Franci" (the Frankish people), ultimately from a Germanic tribal name.',
                'language_origins': 'Latin, Germanic',
                'example_sentence': 'She studied abroad in _______ and fell in love with the language and culture.',
                'memory_tip': 'Remember "FRANCE" - the country of the FRANKS, known for French culture, Paris, and the Eiffel Tower.'
            },
            'franchise': {
                'definition': 'A franchise is a legal and commercial relationship between the owner of a trademark, brand, or business model (franchisor) and an individual or entity (franchisee) who operates a business using that established system. It can also refer to the right to vote in political elections, or more broadly, any special privilege or right granted by an authority. In business, franchises allow for expansion while maintaining brand consistency and operational standards.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FRAN-chyz',
                'etymology': 'From Old French "franchise" meaning "freedom, privilege," from "franc" (free) plus the suffix "-ise."',
                'language_origins': 'Old French',
                'example_sentence': 'He decided to open a fast-food _______ rather than start an independent restaurant.',
                'memory_tip': 'Remember "FRANCHISE" - the FREEDOM (franc-) to operate a business using someone else\'s proven system.'
            },
            'franciscan': {
                'definition': 'Franciscan refers to members of religious orders founded by or following the teachings of Saint Francis of Assisi, emphasizing poverty, simplicity, and service to others. The Franciscans are Catholic religious orders known for their work with the poor and their commitment to living simply. As an adjective, Franciscan describes anything related to these religious communities, their values, or their approach to spiritual life.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'fran-SIS-kan',
                'etymology': 'From Medieval Latin "Franciscanus," derived from "Franciscus" (Francis), referring to Saint Francis of Assisi.',
                'language_origins': 'Medieval Latin',
                'example_sentence': 'The _______ monks dedicated their lives to helping the poor and homeless in the community.',
                'memory_tip': 'Remember "FRANCISCAN" - followers of Saint FRANCIS of Assisi, known for simple living and helping others.'
            },
            'francophone': {
                'definition': 'Francophone describes people, communities, or regions where French is spoken as a native or primary language, or relates to French-speaking cultures and territories. The term encompasses both native French speakers and those who have adopted French as their main language of communication. Francophone can refer to individuals, countries, or cultural movements connected by the shared use of the French language.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'FRAN-koh-fohn',
                'etymology': 'From French "francophone," composed of "franco-" (French) plus "-phone" (speaker), literally meaning "French-speaking."',
                'language_origins': 'French',
                'example_sentence': 'The conference brought together delegates from various _______ nations across Africa and Europe.',
                'memory_tip': 'Remember "FRANCOPHONE" - people who speak FRENCH on the PHONE (francophone), French speakers worldwide.'
            },
            'frangipane': {
                'definition': 'Frangipane is a sweet almond cream or paste used in pastries, tarts, and desserts, made from ground almonds, butter, eggs, and sugar. It\'s a classic filling in French patisserie, providing rich flavor and smooth texture to baked goods. The term can also refer to a type of perfume originally scented with the frangipani flower. In culinary contexts, frangipane is prized for its delicate almond flavor and creamy consistency.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FRAN-jih-payn or fran-jih-PAHN',
                'etymology': 'From French "frangipane," named after Marquis Muzio Frangipani, a 16th-century Italian who created a perfume; later applied to the almond cream.',
                'language_origins': 'French, Italian',
                'example_sentence': 'The baker filled the tart shells with homemade _______ before adding fresh pears on top.',
                'memory_tip': 'Remember "FRANGIPANE" - a FRAGRANT almond PASTE used in French pastries and desserts.'
            },
            'frank': {
                'definition': 'Frank means honest, direct, and candid in expression, characterized by openness and sincerity without attempt to conceal or deceive. A frank person speaks truthfully and straightforwardly, even when the truth might be uncomfortable. The word suggests genuineness and authenticity in communication, emphasizing clarity and honesty over politeness or diplomacy. Frank can also refer to free postage privileges or, historically, to members of a Germanic tribal confederation.',
                'part_of_speech': 'adjective, noun, verb',
                'pronunciation_guide': 'FRANK',
                'etymology': 'From Old French "franc" meaning "free," from Medieval Latin "francus" (free, noble), originally referring to the Frankish people who had full rights.',
                'language_origins': 'Old French, Medieval Latin',
                'example_sentence': 'She gave a _______ assessment of the project\'s challenges, holding nothing back.',
                'memory_tip': 'Remember "FRANK" - being FREE and open with your words, honest like a FRANK discussion.'
            },
            'frankly': {
                'definition': 'Frankly is an adverb meaning in a frank, honest, or direct manner, used to introduce statements that are candid, straightforward, or potentially blunt. It signals that the speaker is about to express their genuine opinion or assessment without diplomatic softening. The word emphasizes sincerity and directness, often used when sharing difficult truths or personal viewpoints that might be considered bold or controversial.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'FRANK-lee',
                'etymology': 'From "frank" (honest, direct) plus the adverbial suffix "-ly," meaning "in a frank manner."',
                'language_origins': 'Old French, Medieval Latin',
                'example_sentence': '_______, I think the proposal needs significant revision before it can be approved.',
                'memory_tip': 'Remember "FRANKLY" - speaking in a FRANK way, honestly and directly without sugar-coating the truth.'
            },
            'frantic': {
                'definition': 'Frantic describes a state of wild excitement, anxiety, or activity characterized by desperate urgency and lack of calm control. It suggests frenzied behavior driven by fear, worry, or extreme emotion, often resulting in chaotic or ineffective actions. Frantic implies intense agitation that impairs clear thinking and measured responses, creating a sense of overwhelming pressure or panic.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FRAN-tik',
                'etymology': 'From Old French "frenetique," from Latin "phreneticus" meaning "delirious," from Greek "phrenitikos" (relating to the mind).',
                'language_origins': 'Greek, Latin, Old French',
                'example_sentence': 'She made a _______ search through her purse looking for her car keys.',
                'memory_tip': 'Remember "FRANTIC" - so worried and rushed that you\'re in a FRENZY, acting wildly and desperately.'
            },
            'frass': {
                'definition': 'Frass is the excrement or waste material produced by insects, particularly caterpillars, beetles, and other arthropods. In entomology and forestry, frass serves as evidence of insect activity and can help identify pest species and assess damage levels. The term is also used in gardening, where insect frass can serve as a natural fertilizer. Frass analysis helps scientists track insect populations and behavior patterns.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FRAS',
                'etymology': 'From German "frass" meaning "food, fodder," related to "fressen" (to eat, devour), referring to what insects consume and excrete.',
                'language_origins': 'German',
                'example_sentence': 'The forest ranger identified the tree pest by examining the _______ found beneath the damaged bark.',
                'memory_tip': 'Remember "FRASS" - what\'s left after insects FEAST, their waste that shows where they\'ve been eating.'
            },
            'fratority': {
                'definition': 'Fratority appears to be a non-standard or potentially corrupted word that might be intended to mean brotherhood, fraternal relationship, or the state of being brothers. It could be a variant or error related to "fraternity" (brotherhood organization) or concepts related to fraternal bonds. This word does not appear in standard dictionaries and may represent a data entry error or uncommon variant spelling.',
                'part_of_speech': 'noun (non-standard)',
                'pronunciation_guide': 'fra-TOR-ih-tee',
                'etymology': 'Possibly related to Latin "frater" (brother) but appears to be non-standard formation, possibly a variant of "fraternity."',
                'language_origins': 'Latin (uncertain formation)',
                'example_sentence': 'The concept of _______ among the group members strengthened their bonds of loyalty.',
                'memory_tip': 'This appears to be a non-standard word - remember that "fraternity" is the correct term for brotherhood organizations.'
            },
            'fraudulent': {
                'definition': 'Fraudulent describes something that is characterized by deceit, trickery, or dishonesty, especially actions intended to deceive others for personal gain or to avoid legal obligations. It refers to behavior, documents, schemes, or claims that are deliberately false or misleading with intent to defraud. Fraudulent activities often involve misrepresentation of facts, forgery, or other deceptive practices designed to illegally obtain money, property, or privileges.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FRAW-juh-lent',
                'etymology': 'From Latin "fraudulentus" meaning "deceitful, dishonest," derived from "fraus" (deceit, injury, fraud).',
                'language_origins': 'Latin',
                'example_sentence': 'The company was fined heavily for making _______ claims about their product\'s effectiveness.',
                'memory_tip': 'Remember "FRAUDULENT" - full of FRAUD, involving deliberate deception and dishonesty for illegal gain.'
            }
        }
        
        return batch_071_data.get(word, {
            'definition': f'Educational definition for {word} would be provided here.',
            'part_of_speech': 'unknown',
            'pronunciation_guide': f'Pronunciation guide for {word}',
            'etymology': f'Etymology information for {word}',
            'language_origins': 'Unknown origins',
            'example_sentence': f'Example sentence with _______ blank for {word}.',
            'memory_tip': f'Memory tip for remembering {word}.'
        })

    def process_batch(self, input_file: str, output_file: str):
        """Process a batch of words with comprehensive Claude data"""
        print(f"Processing {input_file}...")
        
        df = pd.read_csv(input_file)
        processed_words = []
        errors = []
        
        for _, row in df.iterrows():
            word = row['word'].strip()
            
            # Skip empty rows
            if not word:
                continue
                
            # Check for combined word errors
            if word == 'fortificationnoun':
                errors.append(f"{word}: Combined word error: \"fortificationnoun\" appears to be \"fortification\" + \"noun\" merged together. This is likely a PDF parsing error where a word and grammatical notation were incorrectly combined.")
            elif word == 'francatriforium':
                errors.append(f"{word}: Combined word error: \"francatriforium\" appears to be \"franca\" + \"triforium\" merged together. This is likely a PDF parsing error where two separate architectural/linguistic terms were incorrectly combined.")
            elif word == 'fratority':
                errors.append(f"{word}: Non-standard word: \"fratority\" appears to be a variant or error for \"fraternity.\" This may be a spelling error or non-standard formation.")
                
            # Get comprehensive Claude data
            claude_data = self.get_comprehensive_claude_data(word)
            
            # Calculate difficulty components  
            phonetic_score = self.difficulty_calc.calculate_phonetic_complexity(word)
            frequency_score = self.difficulty_calc.estimate_frequency(word)
            morphological_score = self.difficulty_calc.calculate_morphological_complexity(word)
            etymological_score = self.difficulty_calc.calculate_etymological_complexity(
                claude_data['etymology'], claude_data['language_origins']
            )
            
            processed_word = {
                'word': word,
                'years': row['years'],
                'source_files': row['source_files'],
                'source_difficulties': row['source_difficulties'],
                'definition': claude_data['definition'],
                'part_of_speech': claude_data['part_of_speech'],
                'pronunciation_guide': claude_data['pronunciation_guide'],
                'pronunciation_source': 'Claude',
                'etymology': claude_data['etymology'],
                'etymology_source': 'Claude',
                'language_origins': claude_data['language_origins'],
                'example_sentence': claude_data['example_sentence'],
                'example_sentence_source': 'Claude',
                'memory_tip': claude_data['memory_tip'],
                'phonetic_complexity': phonetic_score,
                'frequency_complexity': frequency_score,
                'morphological_complexity': morphological_score,
                'etymological_complexity': etymological_score,
                'final_difficulty_rating': None,  # Will be assigned later
                'difficulty_justification': None,  # Will be provided later
                'audio_file_path': None,  # Will be generated later
                'image_file_path': None,  # Will be added later
                'last_updated': '2024-08-20'
            }
            
            processed_words.append(processed_word)
        
        # Create output dataframe and save
        output_df = pd.DataFrame(processed_words)
        output_df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"Successfully processed {len(processed_words)}/{len(df)} words to {output_file}")
        if errors:
            print(f"Found {len(errors)} error(s):")
            for error in errors:
                print(f"  - {error}")
        print("Batch 071 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch071Processor()
    processor.process_batch(
        "output/batch_071_words.csv",
        "output/batch_071_processed.csv"
    )