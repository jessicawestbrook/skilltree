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

class Batch076Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for a word using Claude knowledge"""
        
        batch_076_data = {
            'gerbils': {
                'definition': 'Gerbils are small desert rodents with long tails, large eyes, and excellent adaptation to arid environments, commonly kept as pets due to their clean habits and friendly nature. These burrowing animals are native to Africa and Asia, known for their ability to conserve water and their social behavior in colonies. Gerbils rarely bite, produce minimal waste, and are active during both day and night.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'JER-bilz',
                'etymology': 'From French "gerbille," ultimately from Arabic "jarbu" meaning "jerboa," referring to similar small desert rodents.',
                'language_origins': 'French, Arabic',
                'example_sentence': 'The children enjoyed watching their pet _______ play in the sand-filled habitat.',
                'memory_tip': 'Remember "GERBILS" - small desert animals that are GERm-free and agILE, popular pets from arid regions.'
            },
            'geriatric': {
                'definition': 'Geriatric relates to the health care and medical treatment of elderly people, or describes something associated with old age and aging processes. As a branch of medicine, geriatrics focuses on the diagnosis, treatment, and prevention of disease and disability in older adults. The term can also refer to elderly patients or anything designed specifically for older people\'s needs.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'jer-ee-AT-rik',
                'etymology': 'From Greek "geras" (old age) plus "iatrikos" (relating to medical treatment), literally meaning "medical treatment of the elderly."',
                'language_origins': 'Greek',
                'example_sentence': 'The hospital\'s new _______ unit specialized in comprehensive care for patients over 65.',
                'memory_tip': 'Remember "GERIATRIC" - medical care for the elderly, GERonto (old age) plus iATRic (medical treatment).'
            },
            'german': {
                'definition': 'German refers to the language spoken primarily in Germany, Austria, and parts of Switzerland, or anything relating to Germany, its people, or culture. As a proper adjective, it describes characteristics, customs, products, or individuals associated with German-speaking countries. German is a major European language known for its complex grammar and compound word formations.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'JER-mun',
                'etymology': 'From Latin "Germanus," the Roman name for Germanic tribes, possibly from Celtic "gairm" (neighbor) or Germanic "ger" (spear).',
                'language_origins': 'Latin, possibly Celtic or Germanic',
                'example_sentence': 'She studied _______ language and literature to better understand European culture.',
                'memory_tip': 'Remember "GERMAN" - the language and culture of GERMany, from ancient Germanic tribes.'
            },
            'germane': {
                'definition': 'Germane means relevant, pertinent, or closely connected to the matter at hand; fitting and appropriate to the subject being discussed. Something germane is directly related and applicable to the topic or situation. The word emphasizes relevance and appropriateness rather than mere connection, suggesting that the information or comment genuinely contributes to understanding or resolving the issue.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'jer-MAYN',
                'etymology': 'From Latin "germanus" meaning "having the same parents, closely related," from "germen" (sprout, seed), suggesting close kinship or connection.',
                'language_origins': 'Latin',
                'example_sentence': 'His comments about budget constraints were _______ to the discussion about project planning.',
                'memory_tip': 'Remember "GERMANE" - relevant like a GERM that\'s connected to the MAIN issue, closely related to the topic.'
            },
            'germanenoun': {
                'definition': 'Germanenoun appears to be a combined word error where "germane" (relevant, pertinent) and "noun" (grammatical term) were incorrectly merged during PDF processing. This represents a data quality issue where an adjective meaning "relevant" was improperly joined with grammatical terminology. The intended content should be "germane" as an adjective with separate grammatical notation.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'jer-MAYN-NOWN',
                'etymology': 'Corrupted combination of "germane" (Latin "germanus") and "noun" (Latin grammatical term).',
                'language_origins': 'Latin (corrupted)',
                'example_sentence': 'The word _______ appears to be a parsing error combining relevance terminology with grammatical classification.',
                'memory_tip': 'This is a data error - remember that "germane" (relevant) and "noun" (grammar) should be separate.'
            },
            'germany': {
                'definition': 'Germany is a country in central Europe known for its rich history, cultural contributions, economic power, and influence on European and world affairs. Officially called the Federal Republic of Germany, it is famous for its contributions to philosophy, music, science, literature, and technology. Germany plays a leading role in the European Union and has a federal system of government.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'JER-muh-nee',
                'etymology': 'From Latin "Germania," the Roman name for the region inhabited by Germanic tribes, ultimately from the tribal name "Germani."',
                'language_origins': 'Latin',
                'example_sentence': 'After reunification in 1990, _______ became one of Europe\'s most influential nations.',
                'memory_tip': 'Remember "GERMANY" - the European country of the GERMAN people, land of many great thinkers and innovators.'
            },
            'gerundial': {
                'definition': 'Gerundial relates to or has the characteristics of a gerund, which is a verb form ending in "-ing" that functions as a noun. In grammar, gerundial constructions use these verb forms in noun positions within sentences. Understanding gerundial usage is important for proper English grammar, as gerunds can serve as subjects, objects, or complements while retaining some verbal characteristics.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'juh-RUN-dee-ul',
                'etymology': 'From Latin "gerundium" (gerund, from "gerere" meaning "to carry on, do") plus the adjectival suffix "-al."',
                'language_origins': 'Latin',
                'example_sentence': 'The teacher explained the _______ function of words like "swimming" in "Swimming is fun."',
                'memory_tip': 'Remember "GERUNDIAL" - relating to GERUNDs, verb forms that are RUNning as nouns in sentences.'
            },
            'gesellschaft': {
                'definition': 'Gesellschaft is a German sociological term referring to a type of social organization based on impersonal, contractual relationships, typically found in modern urban industrial societies. Contrasted with "Gemeinschaft" (community), Gesellschaft represents associations formed by rational self-interest rather than tradition or emotion. The concept was developed by sociologist Ferdinand Tönnies to analyze different forms of social organization.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'guh-ZEL-shahft',
                'etymology': 'From German "Gesellschaft" meaning "society, company, association," from "Geselle" (companion) plus "-schaft" (condition, state).',
                'language_origins': 'German',
                'example_sentence': 'Urban areas typically exhibit _______ characteristics with formal, contractual social relationships.',
                'memory_tip': 'Remember "GESELLSCHAFT" - German for society, where people are like GUESTS in a formal SHAFT of social structure.'
            },
            'gesticulate': {
                'definition': 'Gesticulate means to make gestures, especially animated or dramatic ones, while speaking or to express meaning through hand and arm movements. It involves using physical motions to emphasize points, convey emotions, or communicate ideas, often accompanying verbal communication. Gesticulation can be cultural, with different societies having varying norms about appropriate gesture use.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'jes-TIK-yuh-layt',
                'etymology': 'From Latin "gesticulari" meaning "to mimic, gesture," from "gesticulus" (gesture, mimicry), diminutive of "gestus" (bearing, gesture).',
                'language_origins': 'Latin',
                'example_sentence': 'The animated speaker began to _______ wildly when describing the exciting adventure.',
                'memory_tip': 'Remember "GESTICULATE" - to make GESTures that are arTICULATe, using hands to express yourself.'
            },
            'gesture': {
                'definition': 'A gesture is a movement of part of the body, especially hands or head, to express an idea, meaning, or feeling. Gestures can be conscious communicative acts or unconscious expressions of emotion. They include pointing, waving, nodding, or symbolic movements that convey specific meanings within cultural contexts. Gestures often accompany speech but can also communicate independently.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'JES-chur',
                'etymology': 'From Medieval Latin "gestura" meaning "mode of action," from Latin "gerere" (to bear, carry, perform).',
                'language_origins': 'Medieval Latin, Latin',
                'example_sentence': 'Her welcoming _______ immediately put the nervous visitors at ease.',
                'memory_tip': 'Remember "GESTURE" - a physical movement that shows what you want to EXPRESS, like waving or pointing.'
            },
            'getting': {
                'definition': 'Getting is the present participle of "get," meaning the process of obtaining, acquiring, receiving, or becoming something. It can refer to physical acquisition (getting an object), achievement (getting a job), or change of state (getting tired). Getting emphasizes the ongoing process or action of obtaining rather than the completed result.',
                'part_of_speech': 'verb (present participle)',
                'pronunciation_guide': 'GET-ing',
                'etymology': 'From "get" (from Old Norse "geta" meaning "to obtain, reach") plus the present participle suffix "-ing."',
                'language_origins': 'Old Norse',
                'example_sentence': 'She was _______ better at playing piano with each practice session.',
                'memory_tip': 'Remember "GETTING" - in the process of GETting something, actively acquiring or becoming.'
            },
            'ghana': {
                'definition': 'Ghana is a West African country known for its rich cultural heritage, historical significance in the slave trade, and natural resources including gold and cocoa. The modern nation takes its name from the ancient Ghana Empire, though geographically they are different. Ghana was the first African colony to gain independence from European rule in 1957 and is known for its democratic stability.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'GAH-nah',
                'etymology': 'Named after the ancient Ghana Empire, from Soninke "Ghana" meaning "warrior king," though modern Ghana is geographically distinct from the ancient empire.',
                'language_origins': 'Soninke (West African language)',
                'example_sentence': 'The delegation from _______ shared insights about sustainable cocoa farming practices.',
                'memory_tip': 'Remember "GHANA" - West African nation that GAined independence first, named after ancient empire meaning warrior king.'
            },
            'ghastly': {
                'definition': 'Ghastly describes something extremely unpleasant, horrifying, or shocking, often to the point of causing fear or revulsion. It can refer to appearances that are deathly pale or frightening, or to situations that are appalling or terrible. The word emphasizes both physical revulsion and moral shock, suggesting something that disturbs on multiple levels.',
                'part_of_speech': 'adjective, adverb',
                'pronunciation_guide': 'GAST-lee',
                'etymology': 'From "ghast" (to frighten, from Old English "gāstan") plus "-ly," originally meaning "ghost-like" or "terrifying."',
                'language_origins': 'Old English',
                'example_sentence': 'The accident scene was so _______ that many witnesses needed counseling.',
                'memory_tip': 'Remember "GHASTLY" - so frightening it makes you GASP, like seeing a GHOST, absolutely terrible.'
            },
            'ghostly': {
                'definition': 'Ghostly describes something resembling or characteristic of a ghost; spectral, eerie, or supernatural in appearance or quality. It can refer to pale, translucent appearances, mysterious sounds, or anything that seems to come from beyond the physical world. Ghostly suggests an otherworldly quality that may be beautiful, frightening, or simply mysterious.',
                'part_of_speech': 'adjective, adverb',
                'pronunciation_guide': 'GOHST-lee',
                'etymology': 'From "ghost" (from Old English "gāst" meaning "spirit, soul") plus the suffix "-ly."',
                'language_origins': 'Old English',
                'example_sentence': 'The _______ figure appeared in the moonlight and then vanished without a trace.',
                'memory_tip': 'Remember "GHOSTLY" - like a GHOST, pale and mysterious, having supernatural or spooky qualities.'
            },
            'giallolino': {
                'definition': 'Giallolino is an Italian term referring to a pale yellow color or a specific type of yellow pigment used in art and painting. In Italian, "giallo" means yellow, and "giallolino" indicates a lighter, more delicate shade of yellow. This term appears in art history and color terminology, particularly in discussions of Renaissance and classical painting techniques.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jah-loh-LEE-noh',
                'etymology': 'From Italian "giallo" (yellow) plus the diminutive suffix "-lino," meaning "little yellow" or "pale yellow."',
                'language_origins': 'Italian',
                'example_sentence': 'The Renaissance painter used _______ pigment to create subtle highlights in the portrait.',
                'memory_tip': 'Remember "GIALLOLINO" - Italian for pale yellow, like a gentle GLOW that\'s LIght and NOble in color.'
            },
            'giant': {
                'definition': 'A giant is an extremely large person, creature, or thing, often of mythological or fairy tale origin, or something of extraordinary size compared to normal examples of its kind. In literature and mythology, giants are typically portrayed as enormous humanoid beings with great strength. Metaphorically, giant describes anything remarkably large, powerful, or influential in its field.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'JY-ant',
                'etymology': 'From Old French "geant," from Latin "gigas," from Greek "gigas" meaning "giant, one of the mythological race of giants."',
                'language_origins': 'Old French, Latin, Greek',
                'example_sentence': 'The technology company grew from a startup to a _______ in the industry within just five years.',
                'memory_tip': 'Remember "GIANT" - something so big it\'s GIgantic, enormous like mythological giants in fairy tales.'
            },
            'gibbous': {
                'definition': 'Gibbous describes the moon when it appears more than half but less than fully illuminated, creating a bulging, rounded shape. This lunar phase occurs between the first quarter and full moon (waxing gibbous) or between full moon and third quarter (waning gibbous). The term can also describe anything having a hump-like or protuberant shape.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GIB-us',
                'etymology': 'From Latin "gibbosus" meaning "hump-backed," from "gibba" (hump), referring to the bulging appearance of the partially illuminated moon.',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ moon cast a bright glow over the landscape, nearly full but not quite.',
                'memory_tip': 'Remember "GIBBOUS" - the moon with a GIB (bulge), more than half full and looking like it has a hump.'
            },
            'giddily': {
                'definition': 'Giddily is an adverb meaning in a giddy manner, characterized by lightheaded excitement, dizziness, or frivolous behavior. It describes actions performed with a sense of spinning or disorientation, whether from physical causes or overwhelming excitement. Giddily suggests behavior that is carefree, excited, or slightly reckless due to joy or intoxication.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'GID-ih-lee',
                'etymology': 'From "giddy" (from Old English "gydig" meaning "possessed by a god, mad") plus the adverbial suffix "-ly."',
                'language_origins': 'Old English',
                'example_sentence': 'The children laughed _______ as they spun around on the playground merry-go-round.',
                'memory_tip': 'Remember "GIDDILY" - acting in a GIDDY way with GLEE, spinning around with excitement and joy.'
            },
            'gift': {
                'definition': 'A gift is something given voluntarily without payment in return, as a present or token of appreciation, love, or friendship. Gifts can also refer to natural talents or abilities that someone possesses. The act of giving gifts represents generosity, thoughtfulness, and social bonding, playing important roles in relationships and cultural traditions across societies.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GIFT',
                'etymology': 'From Old Norse "gift" meaning "gift, good luck," related to "gefa" (to give), ultimately from the same root as "give."',
                'language_origins': 'Old Norse',
                'example_sentence': 'Her _______ for music became apparent when she started composing songs at age five.',
                'memory_tip': 'Remember "GIFT" - something GIven FreeT (freely), either a present or natural talent you\'re born with.'
            },
            'giggle': {
                'definition': 'Giggle means to laugh in a light, silly, or nervous manner, typically with repeated short bursts of laughter that are higher in pitch than normal laughter. Giggling often indicates amusement, embarrassment, or nervous energy, and is commonly associated with children or situations involving mild awkwardness or silliness.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'GIG-ul',
                'etymology': 'Probably imitative, representing the sound of light laughter, possibly related to Middle English "giglen" or Dutch "giggelen."',
                'language_origins': 'English (imitative)',
                'example_sentence': 'The students couldn\'t help but _______ when their teacher mispronounced the foreign word.',
                'memory_tip': 'Remember "GIGGLE" - a GIGantic little laugh, light and bubbly like "gig-gig-gig" sounds.'
            },
            'gilded': {
                'definition': 'Gilded means covered with a thin layer of gold or gold leaf, or having a golden appearance. The word can also describe something made to appear more attractive or valuable than it actually is, often with deceptive intent. "Gilded" suggests superficial beauty or wealth that may hide inferior substance underneath.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'GIL-did',
                'etymology': 'Past participle of "gild," from Old English "gyldan" meaning "to cover with gold," related to "gold."',
                'language_origins': 'Old English',
                'example_sentence': 'The ornate _______ frame made the simple painting look much more valuable.',
                'memory_tip': 'Remember "GILDED" - covered with GOLD to look fancy, making something appear more valuable than it is.'
            },
            'gilgamesh': {
                'definition': 'Gilgamesh refers to the legendary king of Uruk in ancient Mesopotamia and the hero of one of the world\'s oldest known pieces of literature, the Epic of Gilgamesh. This ancient Sumerian and Babylonian epic tells the story of Gilgamesh\'s adventures and his quest for immortality. The epic is considered a foundational work of world literature, exploring themes of friendship, mortality, and the human condition.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'GIL-gah-mesh',
                'etymology': 'From Akkadian "Gilgameš," possibly meaning "the ancestor is a hero" or related to Sumerian divine names.',
                'language_origins': 'Akkadian, Sumerian',
                'example_sentence': 'Students studied the Epic of _______ to understand ancient Mesopotamian literature and culture.',
                'memory_tip': 'Remember "GILGAMESH" - the ancient king whose epic story is a GILded (golden) GAME of heroic adventures and MESH of human emotions.'
            },
            'gimbaled': {
                'definition': 'Gimbaled (or gimballed) describes something that is mounted on gimbals, which are pivoted supports that allow rotation around multiple axes, keeping an object level despite movement of its support. This system is used in ships\' compasses, cameras, gyroscopes, and spacecraft to maintain stability and orientation regardless of external motion.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GIM-buld',
                'etymology': 'From "gimbal" (from Old French "gemel" meaning "twin," referring to the paired rings) plus the past participle suffix "-ed."',
                'language_origins': 'Old French',
                'example_sentence': 'The _______ camera mount kept the shot steady even as the ship rocked in heavy seas.',
                'memory_tip': 'Remember "GIMBALED" - mounted on GYM-like BALanced rings that keep things steady despite movement.'
            },
            'gimballed': {
                'definition': 'Gimballed is the British spelling of "gimbaled," describing something mounted on gimbals - pivoted supports that allow free rotation around multiple axes to maintain stability. This mounting system is essential in navigation equipment, scientific instruments, and stabilization systems where maintaining level orientation is critical despite external movement.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GIM-buld',
                'etymology': 'British spelling of "gimbaled," from "gimbal" plus "-ed," where gimbal comes from Old French "gemel" (twin).',
                'language_origins': 'Old French',
                'example_sentence': 'The _______ gyroscope maintained its orientation perfectly despite the aircraft\'s maneuvers.',
                'memory_tip': 'Remember "GIMBALLED" - British spelling for GYM-BALanced mounting that keeps instruments level and stable.'
            },
            'ginger': {
                'definition': 'Ginger is a flowering plant whose rhizome (underground stem) is widely used as a spice and herbal medicine, known for its hot, pungent flavor and aromatic qualities. Fresh ginger root is used in cooking worldwide, while dried ginger powder is a common baking spice. Ginger has anti-inflammatory properties and is used to treat nausea and digestive issues.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'JIN-jer',
                'etymology': 'From Old English "gingifer," from Medieval Latin "gingiber," ultimately from Sanskrit "srngaveram" (horn-shaped).',
                'language_origins': 'Old English, Medieval Latin, Sanskrit',
                'example_sentence': 'The chef added fresh _______ to the stir-fry for extra flavor and heat.',
                'memory_tip': 'Remember "GINGER" - a spicy root that adds ZING to food, hot and aromatic like its reddish color suggests.'
            },
            'gingerbread': {
                'definition': 'Gingerbread is a sweet baked good flavored with ginger and other spices like cinnamon, cloves, and nutmeg, often made into cookies shaped like people or houses, especially popular during Christmas. The term also refers to elaborate decorative woodwork on Victorian buildings, called "gingerbread trim" because of its ornate, cookie-like appearance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JIN-jer-bred',
                'etymology': 'Compound of "ginger" plus "bread," from Middle English "gingerbrede," originally a preserved ginger confection.',
                'language_origins': 'Middle English',
                'example_sentence': 'The children decorated the _______ house with candy and icing for the holiday display.',
                'memory_tip': 'Remember "GINGERBREAD" - sweet bread flavored with GINGER, often shaped like little people or houses.'
            },
            'gingivitis': {
                'definition': 'Gingivitis is inflammation of the gums (gingiva) caused by bacterial plaque buildup, characterized by red, swollen, bleeding gums. This common dental condition is the mildest form of gum disease and is typically reversible with proper oral hygiene and professional cleaning. If untreated, gingivitis can progress to more severe periodontal disease.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jin-jih-VY-tis',
                'etymology': 'From Latin "gingiva" (gum) plus Greek suffix "-itis" (inflammation), literally meaning "gum inflammation."',
                'language_origins': 'Latin, Greek',
                'example_sentence': 'The dentist diagnosed _______ and recommended improved brushing and flossing habits.',
                'memory_tip': 'Remember "GINGIVITIS" - inflammation (-itis) of the GINGIVa (gums), making gums red and swollen.'
            },
            'ginglymus': {
                'definition': 'Ginglymus is an anatomical term for a hinge joint that allows movement in only one plane, like the elbow or knee joint. These joints permit flexion and extension but not rotation or side-to-side movement. The term is used in medical and anatomical contexts to describe this specific type of synovial joint structure.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GING-lih-mus',
                'etymology': 'From Greek "ginglymos" meaning "hinge," referring to the hinge-like movement of these joints.',
                'language_origins': 'Greek',
                'example_sentence': 'The knee is an example of a _______ joint, allowing bending and straightening but not rotation.',
                'memory_tip': 'Remember "GINGLYMUS" - a HINGE joint that GINGerly moves in one direction, like your elbow bending.'
            },
            'gippsland': {
                'definition': 'Gippsland is a region in southeastern Victoria, Australia, known for its diverse landscapes including forests, lakes, and agricultural areas. The region was named after Sir George Gipps, an early Governor of New South Wales. Gippsland is famous for its natural beauty, dairy farming, and tourist attractions including the Gippsland Lakes.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'GIPS-land',
                'etymology': 'Named after Sir George Gipps (1791-1847), Governor of New South Wales, plus "land."',
                'language_origins': 'English (named after British colonial governor)',
                'example_sentence': 'The tourists planned to explore the scenic lakes and forests of _______.',
                'memory_tip': 'Remember "GIPPSLAND" - Australian region named after Governor GIPPS, a LAND of lakes and agriculture.'
            },
            'giraffe': {
                'definition': 'A giraffe is the world\'s tallest mammal, native to Africa, characterized by its extremely long neck, legs, and distinctive spotted coat pattern. These herbivorous animals use their height to reach acacia leaves high in trees that other animals cannot access. Giraffes have unique cardiovascular adaptations to pump blood up their long necks to their brains.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'juh-RAF',
                'etymology': 'From French "girafe," from Arabic "zarāfah," possibly from an African language describing this distinctive animal.',
                'language_origins': 'French, Arabic',
                'example_sentence': 'The _______ gracefully stretched its neck to reach the highest branches of the acacia tree.',
                'memory_tip': 'Remember "GIRAFFE" - the tall animal with a long neck that can GRAB leaves from ABOVE, spotted and graceful.'
            },
            'giraffes': {
                'definition': 'Giraffes is the plural form of giraffe, referring to multiple of these tall African mammals known for their extraordinary height, long necks, and distinctive spotted patterns. These herbivores live in savannas and open woodlands, traveling in loose herds and using their height advantage to spot predators and access food sources unavailable to other animals.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'juh-RAFS',
                'etymology': 'Plural of "giraffe," from French "girafe," ultimately from Arabic "zarāfah."',
                'language_origins': 'French, Arabic',
                'example_sentence': 'The wildlife photographer captured stunning images of _______ silhouetted against the African sunset.',
                'memory_tip': 'Remember "GIRAFFES" - multiple tall animals that can GRAB leaves from ABOVE, a group of spotted long-necked mammals.'
            },
            'girandole': {
                'definition': 'A girandole is an ornate candlestick or candelabra with multiple branches for holding several candles, often elaborately decorated and designed as a centerpiece. These decorative lighting fixtures were particularly popular in the 17th and 18th centuries and are characterized by their artistic design combining functionality with aesthetic appeal.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JIR-un-dohl',
                'etymology': 'From French "girandole," from Italian "girandola" meaning "revolving firework," from "girare" (to turn), referring to the radiating arms.',
                'language_origins': 'French, Italian',
                'example_sentence': 'The elegant _______ held twelve candles and served as the centerpiece for the formal dining table.',
                'memory_tip': 'Remember "GIRANDOLE" - a decorative candle holder that GIRates with multiple arms, like a GRAND spinning wheel of light.'
            },
            'gist': {
                'definition': 'The gist is the main point, central idea, or essential meaning of something, particularly a speech, argument, or written work. It represents the core substance or most important elements, stripped of details and supporting information. Understanding the gist means grasping the fundamental message or primary significance of a communication.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JIST',
                'etymology': 'From Old French "gist" meaning "it lies," from "gésir" (to lie), originally a legal term meaning "the point on which an action lies."',
                'language_origins': 'Old French',
                'example_sentence': 'Although the lecture was complex, the _______ was that climate change requires immediate action.',
                'memory_tip': 'Remember "GIST" - the main point that you GET, the essential idea that really matters in any communication.'
            },
            'gistgizzard': {
                'definition': 'Gistgizzard appears to be a combined word error where "gist" (main point or essential meaning) and "gizzard" (bird\'s digestive organ) were incorrectly merged during PDF processing. These are completely unrelated terms - one referring to abstract meaning and the other to anatomy. This represents a data quality issue where linguistic and biological terminology were improperly joined.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'JIST-GIZ-ard',
                'etymology': 'Corrupted combination of "gist" (Old French "gist") and "gizzard" (Middle English "giser").',
                'language_origins': 'Old French, Middle English (corrupted)',
                'example_sentence': 'The word _______ appears to be a parsing error combining meaning terminology with bird anatomy.',
                'memory_tip': 'This is a data error - remember that "gist" (main point) and "gizzard" (bird organ) should be separate.'
            },
            'given': {
                'definition': 'Given can mean provided, granted, or assumed as a basis for argument or calculation. As an adjective, it describes something that is specified, particular, or taken as fact. Given also functions as the past participle of "give," indicating something that has been provided or bestowed. The word often introduces conditions or assumptions in logical arguments.',
                'part_of_speech': 'adjective, verb (past participle), noun',
                'pronunciation_guide': 'GIV-en',
                'etymology': 'Past participle of "give," from Old English "giefan" meaning "to give, bestow," related to Old Norse "gefa."',
                'language_origins': 'Old English',
                'example_sentence': 'Under the _______ circumstances, we had no choice but to postpone the event.',
                'memory_tip': 'Remember "GIVEN" - something that\'s already been GIVen or assumed, a fact you can count on.'
            },
            'giza': {
                'definition': 'Giza is a city in Egypt, part of Greater Cairo, famous for the Giza pyramid complex including the Great Pyramid of Giza, one of the Seven Wonders of the Ancient World. The site also features the Great Sphinx and other ancient monuments from the Old Kingdom period. Giza represents one of the most important archaeological sites in the world.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'GEE-zah',
                'etymology': 'From Arabic "al-Jīzah," possibly meaning "the sycamore" or related to ancient Egyptian place names.',
                'language_origins': 'Arabic, ancient Egyptian',
                'example_sentence': 'Tourists from around the world visit _______ to see the ancient pyramids and Sphinx.',
                'memory_tip': 'Remember "GIZA" - where the Great pyramids stand, an ancient site that makes you GAZe in wonder.'
            },
            'gizzard': {
                'definition': 'A gizzard is a muscular part of a bird\'s stomach that grinds food, particularly in birds that eat seeds and grain. This specialized digestive organ contains small stones or grit that help break down tough food materials. The gizzard is the bird\'s equivalent of teeth for mechanical digestion, essential for processing hard foods.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GIZ-ard',
                'etymology': 'From Middle English "giser," from Old French "gesier," ultimately from Latin "gigeria" (cooked entrails of poultry).',
                'language_origins': 'Middle English, Old French, Latin',
                'example_sentence': 'The chicken\'s _______ helped grind up the corn and seeds it had eaten.',
                'memory_tip': 'Remember "GIZZARD" - a bird\'s grinding organ that\'s like a GRIZzly bear for food, tough and powerful.'
            },
            'glabella': {
                'definition': 'The glabella is the smooth area of the forehead between the eyebrows, above the nose bridge. In anatomy, this region is significant as a landmark for medical procedures and anthropological measurements. The glabella can also refer to the muscle in this area that causes frowning when contracted, and is a common site for cosmetic treatments.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gluh-BEL-uh',
                'etymology': 'From Latin "glabella," diminutive of "glaber" meaning "smooth, hairless," referring to the smooth area between the eyebrows.',
                'language_origins': 'Latin',
                'example_sentence': 'The dermatologist injected the treatment directly into the _______ to reduce frown lines.',
                'memory_tip': 'Remember "GLABELLA" - the GLAB (smooth) area between eyebrows, like a small BELL-shaped smooth zone on your forehead.'
            },
            'glabrous': {
                'definition': 'Glabrous means smooth and hairless, lacking hair, down, or fuzz, typically used to describe plant parts, skin, or surfaces. In botany, glabrous leaves or stems are completely smooth without any hair-like structures. The term emphasizes the complete absence of surface texture or covering that would make something rough or fuzzy.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GLAY-brus',
                'etymology': 'From Latin "glaber" meaning "smooth, bald, hairless," related to "glabra" (smooth area).',
                'language_origins': 'Latin',
                'example_sentence': 'The botanist noted that the plant\'s _______ leaves had no fuzzy texture whatsoever.',
                'memory_tip': 'Remember "GLABROUS" - GLAd to be BaRe and smOoth, completely hairless and smooth to touch.'
            },
            'glacier': {
                'definition': 'A glacier is a large, slow-moving mass of ice formed from compressed snow that accumulates over many years, typically found in mountains or polar regions. Glaciers flow slowly downhill due to gravity, carving valleys and shaping landscapes. They serve as important water sources and climate indicators, with many glaciers currently retreating due to global warming.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GLAY-sher',
                'etymology': 'From French "glacier," from "glace" (ice), ultimately from Latin "glacies" (ice).',
                'language_origins': 'French, Latin',
                'example_sentence': 'The massive _______ had carved the mountain valley over thousands of years.',
                'memory_tip': 'Remember "GLACIER" - a GLAss-like river of ICE that moves slowly down mountains, shaping the land.'
            },
            'glacis': {
                'definition': 'A glacis is a gently sloping embankment or artificial slope, particularly one that slopes away from a fortification to provide a clear field of fire and prevent enemies from taking cover. In military architecture, the glacis is the outermost defensive element of a fort, designed to expose attackers to defensive fire while providing no protection.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GLAY-sis',
                'etymology': 'From French "glacis" meaning "slope," from "glacer" (to slip, slide), related to "glace" (ice, slippery surface).',
                'language_origins': 'French',
                'example_sentence': 'The fort\'s _______ provided a clear killing field while offering no cover to approaching enemies.',
                'memory_tip': 'Remember "GLACIS" - a GLAss-smooth slope around forts that\'s as slippery as ICE for attackers, exposing them to fire.'
            },
            'gladiatorial': {
                'definition': 'Gladiatorial relates to gladiators or the arena contests in which they fought in ancient Rome. It describes the combats, spectacles, training, or culture surrounding these professional fighters who entertained crowds by fighting each other or wild animals. Gladiatorial contests were central to Roman entertainment and represent a significant aspect of ancient Roman society.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'glad-ee-uh-TOR-ee-ul',
                'etymology': 'From Latin "gladiator" (swordsman, from "gladius" meaning "sword") plus the adjectival suffix "-ial."',
                'language_origins': 'Latin',
                'example_sentence': 'The museum\'s exhibit featured artifacts from _______ contests in the Roman Colosseum.',
                'memory_tip': 'Remember "GLADIATORIAL" - relating to GLADiators fighting in arenas, sword combat for entertainment in ancient Rome.'
            },
            'gladiolus': {
                'definition': 'A gladiolus is a flowering plant with tall spikes of colorful, funnel-shaped flowers arranged along a single stem, popular in gardens and as cut flowers. These perennial plants grow from corms (bulb-like structures) and produce sword-shaped leaves. Gladioli come in many colors and are prized for their dramatic vertical flower displays.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'glad-ee-OH-lus',
                'etymology': 'From Latin "gladiolus," diminutive of "gladius" (sword), referring to the sword-like shape of the leaves.',
                'language_origins': 'Latin',
                'example_sentence': 'The garden bed was filled with tall _______ flowers in shades of pink, red, and white.',
                'memory_tip': 'Remember "GLADIOLUS" - a flower with sword-like leaves, named after the GLADius (Roman sword) due to its shape.'
            },
            'gladness': {
                'definition': 'Gladness is a feeling of joy, happiness, or pleasure, characterized by a cheerful and contented state of mind. It represents a positive emotional condition that arises from favorable circumstances, good news, or general satisfaction with life. Gladness is often visible in facial expressions and behavior, suggesting an inner lightness and optimism.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GLAD-nis',
                'etymology': 'From "glad" (from Old English "glæd" meaning "bright, cheerful") plus the noun-forming suffix "-ness."',
                'language_origins': 'Old English',
                'example_sentence': 'Her face lit up with _______ when she received the acceptance letter from her dream college.',
                'memory_tip': 'Remember "GLADNESS" - the state of being GLAD, happiness and joy that makes you feel bright and cheerful.'
            },
            'glareous': {
                'definition': 'Glareous means gravelly or containing gravel, particularly describing soil or ground that has a high content of small stones and pebbles. This geological term is used to describe terrain or soil composition that is characterized by loose rock fragments. The term is primarily used in technical, geological, or agricultural contexts.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GLAIR-ee-us',
                'etymology': 'From Latin "glarea" meaning "gravel" plus the adjectival suffix "-ous," literally meaning "full of gravel."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ soil drained quickly but required amendments to support plant growth.',
                'memory_tip': 'Remember "GLAREOUS" - GLARE-ing with gravel, soil that\'s full of stones and rocky fragments.'
            },
            'glasses': {
                'definition': 'Glasses refers to eyeglasses or spectacles worn to correct vision problems or protect the eyes, consisting of lenses mounted in frames that sit on the nose and ears. The term can also refer to drinking vessels made of glass, or the plural of any glass objects. In the vision context, glasses help focus light properly on the retina.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GLAS-iz',
                'etymology': 'Plural of "glass," from Old English "glæs," referring to the transparent material or objects made from it.',
                'language_origins': 'Old English',
                'example_sentence': 'She put on her reading _______ to examine the fine print in the contract.',
                'memory_tip': 'Remember "GLASSES" - GLAss lenses that help you see clearly, or drinking vessels made of transparent glass.'
            },
            'glaswegian': {
                'definition': 'Glaswegian refers to a person from Glasgow, Scotland, or anything relating to Glasgow and its culture, dialect, or characteristics. Glaswegians are known for their distinctive accent and cultural identity within Scotland. The term encompasses both the people and the cultural aspects associated with Scotland\'s largest city.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'glaz-WEE-jun',
                'etymology': 'From "Glasgow" (from Scottish Gaelic "Glaschu" meaning "green hollow") plus the suffix "-ian" indicating origin or relation.',
                'language_origins': 'Scottish Gaelic, English',
                'example_sentence': 'The _______ comedian entertained the audience with stories about life in Glasgow.',
                'memory_tip': 'Remember "GLASWEGIAN" - someone from GLASgow who speaks with a distinctive Scottish dialect, a GLAd resident of the WEll-known city.'
            },
            'glaucomatous': {
                'definition': 'Glaucomatous relates to or affected by glaucoma, a group of eye diseases that damage the optic nerve and can lead to blindness if untreated. The term describes conditions, symptoms, or changes in the eye associated with increased intraocular pressure that characterizes glaucoma. Early detection and treatment are crucial for preserving vision.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'glow-KOM-uh-tus',
                'etymology': 'From "glaucoma" (from Greek "glaukoma," from "glaukos" meaning "bluish-gray," referring to the appearance of affected eyes) plus "-ous."',
                'language_origins': 'Greek',
                'example_sentence': 'The ophthalmologist detected early _______ changes during the routine eye examination.',
                'memory_tip': 'Remember "GLAUCOMATOUS" - relating to GLAUcoma, eye disease that can make vision GLAUky (gray and dim).'
            },
            'glazed': {
                'definition': 'Glazed describes something covered with a smooth, glossy coating or surface, such as pottery with a ceramic glaze, food with a shiny coating, or eyes that appear glassy and unfocused. The term can refer to the shiny finish applied to ceramics, the coating on donuts or ham, or the blank expression that suggests distraction or tiredness.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'GLAYZD',
                'etymology': 'Past participle of "glaze," from Middle English "glasen" meaning "to fit with glass," related to "glass."',
                'language_origins': 'Middle English',
                'example_sentence': 'The _______ pottery had a beautiful blue-green finish that caught the light perfectly.',
                'memory_tip': 'Remember "GLAZED" - covered with a GLAss-like coating that\'s smooth and shiny, or eyes that look glassy.'
            },
            'glazier': {
                'definition': 'A glazier is a craftsperson who cuts, installs, and replaces glass, particularly in windows, doors, and other architectural applications. Glaziers work with various types of glass and glazing systems, requiring skill in measuring, cutting, and safely handling glass materials. This trade combines technical knowledge with practical craftsmanship.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GLAY-zher',
                'etymology': 'From Middle English "glasier," from "glass" plus the agent suffix "-ier," meaning "one who works with glass."',
                'language_origins': 'Middle English',
                'example_sentence': 'The skilled _______ carefully measured and cut the replacement window glass.',
                'memory_tip': 'Remember "GLAZIER" - someone who works with GLAss, a specialist who instaLls and repairs glass windows.'
            }
        }
        
        return batch_076_data.get(word, {
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
            if word == 'germanenoun':
                errors.append(f"{word}: Combined word error: \"germanenoun\" appears to be \"germane\" + \"noun\" merged together. This is likely a PDF parsing error where relevance terminology and grammatical classification were incorrectly combined.")
            elif word == 'gistgizzard':
                errors.append(f"{word}: Combined word error: \"gistgizzard\" appears to be \"gist\" + \"gizzard\" merged together. This is likely a PDF parsing error where meaning terminology and bird anatomy were incorrectly combined.")
                
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
        print("Batch 076 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch076Processor()
    processor.process_batch(
        "output/batch_076_words.csv",
        "output/batch_076_processed.csv"
    )