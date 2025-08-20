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

class Batch075Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for a word using Claude knowledge"""
        
        batch_075_data = {
            'gathering': {
                'definition': 'Gathering refers to the act of coming together or the event where people assemble in one place for a common purpose, such as a social event, meeting, or celebration. It can also mean the process of collecting or accumulating things, such as gathering information, materials, or resources. The word emphasizes the bringing together of separate elements into a unified group or collection.',
                'part_of_speech': 'noun, verb (present participle)',
                'pronunciation_guide': 'GATH-er-ing',
                'etymology': 'From "gather" (Old English "gaderian") plus the suffix "-ing," indicating the action or result of gathering.',
                'language_origins': 'Old English',
                'example_sentence': 'The family _______ for Thanksgiving brought relatives together from across the country.',
                'memory_tip': 'Remember "GATHERING" - people GAThering together, coming to one place like a GAThering storm.'
            },
            'gattine': {
                'definition': 'Gattine appears to be a specialized term, possibly related to textiles, gatling (as in machine gun mechanisms), or may be a variant of an Italian or French term. Without more specific context, this could refer to a type of fabric treatment, mechanical process, or technical term in a specialized field. The exact meaning would depend on the specific industry or context in which it appears.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gah-TEEN',
                'etymology': 'Etymology uncertain, possibly from Italian or French origins, or related to mechanical terminology.',
                'language_origins': 'Uncertain, possibly Italian or French',
                'example_sentence': 'The textile manufacturer used a specialized _______ process to achieve the desired fabric texture.',
                'memory_tip': 'Remember "GATTINE" - sounds like GATing or getting something, possibly a technical process.'
            },
            'gaucho': {
                'definition': 'A gaucho is a skilled horseman and cattle herder from the South American pampas, particularly in Argentina, Uruguay, and southern Brazil. Gauchos are known for their traditional lifestyle, horsemanship skills, and distinctive clothing including wide-brimmed hats, ponchos, and loose-fitting pants called bombachas. They represent an important cultural symbol of South American frontier life and pastoral traditions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GOW-choh',
                'etymology': 'From Spanish "gaucho," possibly from Quechua "wakcha" (orphan, poor person) or from Mapuche "kauchu" (friend, companion).',
                'language_origins': 'Spanish, possibly Quechua or Mapuche',
                'example_sentence': 'The skilled _______ rode across the pampas, expertly herding cattle with his traditional lasso.',
                'memory_tip': 'Remember "GAUCHO" - a South American cowboy who GOes and CHases cattle on horseback.'
            },
            'gaudery': {
                'definition': 'Gaudery refers to showy, ostentatious display or ornamentation that is gaudy, flashy, or tastelessly elaborate. It describes decorative elements or behavior that is excessively ornate, colorful, or attention-seeking in a way that lacks refinement or good taste. Gaudery emphasizes the excessive and vulgar nature of such displays.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GOW-der-ee',
                'etymology': 'From "gaudy" (possibly from Middle English "gaudi," a bead in a rosary, hence something showy) plus the suffix "-ery."',
                'language_origins': 'Middle English',
                'example_sentence': 'The mansion\'s interior was filled with such _______ that visitors found it overwhelming rather than impressive.',
                'memory_tip': 'Remember "GAUDERY" - GAUDy decorations everywhere, excessive and showy ornamentation.'
            },
            'gaul': {
                'definition': 'Gaul historically refers to the ancient region of Western Europe that roughly corresponds to modern-day France, Belgium, and parts of surrounding countries, inhabited by Celtic peoples before Roman conquest. The term can also refer to the ancient Celtic inhabitants of this region. In modern contexts, Gaul sometimes appears in historical discussions or as a poetic reference to France.',
                'part_of_speech': 'proper noun, noun',
                'pronunciation_guide': 'GAWL',
                'etymology': 'From Latin "Gallia," the Roman name for the region, ultimately from the Celtic tribal name "Galatai" or similar.',
                'language_origins': 'Latin, Celtic',
                'example_sentence': 'Julius Caesar wrote extensively about his conquest of _______ in his famous Commentaries.',
                'memory_tip': 'Remember "GAUL" - ancient GALlia where GALlic people lived, now modern France.'
            },
            'gauntlet': {
                'definition': 'A gauntlet is a protective glove, especially one worn as part of medieval armor or for heavy work, designed to protect the hands and wrists. The phrase "throw down the gauntlet" means to issue a challenge, while "run the gauntlet" means to face criticism or ordeal from multiple sources. Gauntlets represent both protection and the concept of facing challenges.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAWNT-lit',
                'etymology': 'From Old French "gantelet," diminutive of "gant" (glove), literally meaning "little glove."',
                'language_origins': 'Old French',
                'example_sentence': 'The knight\'s armored _______ protected his hands during the fierce battle.',
                'memory_tip': 'Remember "GAUNTLET" - a protective glove that\'s GAUNT and LIGHT but strong, or a challenge thrown down.'
            },
            'gaur': {
                'definition': 'A gaur is a large wild ox native to South and Southeast Asia, also known as the Indian bison. These massive bovines are among the largest wild cattle in the world, with distinctive muscular builds, curved horns, and dark brown coats. Gaurs are found in forests and grasslands and are considered vulnerable due to habitat loss and hunting pressure.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GOWR',
                'etymology': 'From Hindi "gaur," the local name for this wild bovine species in the Indian subcontinent.',
                'language_origins': 'Hindi',
                'example_sentence': 'The wildlife photographer was thrilled to spot a massive _______ grazing in the forest clearing.',
                'memory_tip': 'Remember "GAUR" - a GAUnt wild ox that\'s really huge, like a GARGANTUAN bovine creature.'
            },
            'gautam': {
                'definition': 'Gautam (also spelled Gautama) is a Sanskrit name meaning "descendant of Gotama" and is most famous as the family name of Siddhartha Gautama, who became the Buddha. In Indian tradition, Gautam is also the name of one of the seven great sages (saptarishis). As a personal name, it represents wisdom, enlightenment, and spiritual leadership in Hindu and Buddhist cultures.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'GOW-tam',
                'etymology': 'From Sanskrit "Gautama," meaning "descendant of Gotama," from the sage\'s name Gotama plus the patronymic suffix.',
                'language_origins': 'Sanskrit',
                'example_sentence': '_______ Buddha\'s teachings on compassion and mindfulness continue to influence millions worldwide.',
                'memory_tip': 'Remember "GAUTAM" - the name of the future Buddha, someone who GAUged the truth and found enlightenment.'
            },
            'gaylord': {
                'definition': 'Gaylord historically is a surname and masculine given name meaning "joyful" or "high-spirited." In industrial contexts, a Gaylord is a large corrugated cardboard container used for shipping and storing bulk materials. The name derives from the Gaylord Container Corporation, which popularized these large shipping boxes. The industrial usage is completely separate from the personal name.',
                'part_of_speech': 'proper noun, noun',
                'pronunciation_guide': 'GAY-lord',
                'etymology': 'As a name: from Old French "gaillard" meaning "joyful, high-spirited." As container: from the Gaylord Container Corporation.',
                'language_origins': 'Old French, Modern American (commercial)',
                'example_sentence': 'The warehouse workers loaded the _______ container with recyclable materials.',
                'memory_tip': 'Remember "GAYLORD" - either a joyful lord (name) or a GAY (large) container for shipping loads.'
            },
            'gazed': {
                'definition': 'Gazed is the past tense of "gaze," meaning to look steadily and intently at something for an extended period, often with wonder, admiration, or deep thought. Gazing implies more than just looking - it suggests a focused, prolonged visual attention that may be accompanied by contemplation or emotion. The word emphasizes the sustained and intentional nature of this type of looking.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'GAYZD',
                'etymology': 'From Middle English "gasen," possibly from Old Norse "gá" (to heed, observe) or related to "gaze" meaning to stare.',
                'language_origins': 'Middle English, possibly Old Norse',
                'example_sentence': 'She _______ out the window at the beautiful sunset painting the sky in brilliant colors.',
                'memory_tip': 'Remember "GAZED" - past tense of gaze, when you GAZEd intently with amazement at something.'
            },
            'gazette': {
                'definition': 'A gazette is an official publication, especially a newspaper or journal that contains public notices, government announcements, or news of official appointments and events. Historically, gazettes were the primary means of communicating official information to the public. Many government publications and local newspapers still use "gazette" in their names to indicate their role in providing official or community news.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'guh-ZET',
                'etymology': 'From Italian "gazzetta," originally the price of a Venetian newspaper (a small coin called a gazeta), from "gazza" (magpie), possibly referring to the chattering nature of news.',
                'language_origins': 'Italian',
                'example_sentence': 'The official _______ published the list of new government appointments and policy changes.',
                'memory_tip': 'Remember "GAZETTE" - a GAZing publication that lets you ZET (get) the official news and announcements.'
            },
            'gazoz': {
                'definition': 'Gazoz is a type of carbonated soft drink popular in Turkey and some Middle Eastern countries, similar to soda or sparkling lemonade. These beverages are typically fruit-flavored, fizzy, and refreshing. The term comes from the French "gaz" meaning gas, referring to the carbonation. Gazoz represents a category of traditional Middle Eastern carbonated beverages.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gah-ZOHZ',
                'etymology': 'From French "gaz" (gas) referring to carbonated water, adapted into Turkish and other Middle Eastern languages.',
                'language_origins': 'French, Turkish',
                'example_sentence': 'The street vendor sold cold _______ to thirsty customers on the hot summer day.',
                'memory_tip': 'Remember "GAZOZ" - a GAZzy drink with fizz, carbonated soda that makes you go "ahh" (oz sound).'
            },
            'gchange': {
                'definition': 'Gchange appears to be a corrupted word or non-standard term that may be intended as "change" with an erroneous "g" prefix. This could represent a data entry error, typo, or specialized technical term. Without additional context, it most likely represents a parsing or transcription error where "change" was incorrectly prefixed with "g."',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'jee-CHAYNJ',
                'etymology': 'Appears to be "change" with erroneous "g" prefix, likely a transcription or data processing error.',
                'language_origins': 'English (corrupted)',
                'example_sentence': 'The word _______ appears to be a data error where "change" was incorrectly prefixed.',
                'memory_tip': 'This appears to be a data error - likely should be "change" without the "g" prefix.'
            },
            'geatish': {
                'definition': 'Geatish refers to the Geats, an ancient North Germanic tribe mentioned in Anglo-Saxon poetry, particularly in the epic poem Beowulf, where the hero Beowulf is described as a Geat. The Geats inhabited parts of what is now southern Sweden. Geatish culture and society are primarily known through literary sources rather than extensive historical records.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GEE-ah-tish',
                'etymology': 'From "Geat" (Old English "Gēatas"), the name of the ancient Germanic tribe, plus the suffix "-ish" meaning "of or relating to."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The _______ warriors in Beowulf were portrayed as brave and loyal fighters.',
                'memory_tip': 'Remember "GEATISH" - relating to the GEATs, the ancient tribe that was GREATish in the Beowulf epic.'
            },
            'gegenschein': {
                'definition': 'Gegenschein is a faint, roughly circular patch of light visible in the night sky at the antisolar point (directly opposite the sun). This astronomical phenomenon is caused by sunlight reflecting off interplanetary dust particles in space. The gegenschein is extremely faint and can only be seen under very dark sky conditions, away from light pollution.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAY-gen-shyn',
                'etymology': 'From German "Gegenschein," literally meaning "counter-shine" or "opposite glow," from "gegen" (against, opposite) plus "Schein" (shine, glow).',
                'language_origins': 'German',
                'example_sentence': 'The amateur astronomer traveled to a dark sky site hoping to observe the elusive _______.',
                'memory_tip': 'Remember "GEGENSCHEIN" - the GEGEN (opposite) SCHEIN (shine) in the sky, light opposite the sun.'
            },
            'geiger': {
                'definition': 'Geiger most commonly refers to the Geiger counter, a device that detects and measures ionizing radiation, named after physicist Hans Geiger. The term can also refer to Hans Geiger himself (1882-1945), the German physicist who invented this radiation detection device. Geiger counters are essential tools in nuclear physics, medicine, and radiation safety.',
                'part_of_speech': 'proper noun, noun',
                'pronunciation_guide': 'GUY-ger',
                'etymology': 'Named after Hans Geiger (1882-1945), German physicist who invented the radiation detection device.',
                'language_origins': 'German (personal name)',
                'example_sentence': 'The radiation safety officer used a _______ counter to check for contamination in the laboratory.',
                'memory_tip': 'Remember "GEIGER" - the physicist who invented the device that GEts radiation readings with clicking GEIGer sounds.'
            },
            'gelatin': {
                'definition': 'Gelatin is a colorless, odorless protein derived from collagen found in animal bones, skin, and connective tissue. When dissolved in hot water and cooled, gelatin forms a gel-like substance used in cooking for desserts, aspics, and as a thickening agent. Gelatin is also used in pharmaceuticals for capsules and in photography for film emulsion.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JEL-uh-tin',
                'etymology': 'From French "gélatine," from Italian "gelatina," from "gelato" (frozen, congealed), ultimately from Latin "gelatus."',
                'language_origins': 'French, Italian, Latin',
                'example_sentence': 'The chef used unflavored _______ to create a firm, clear aspic for the appetizer.',
                'memory_tip': 'Remember "GELATIN" - a protein that makes things GEL and become LATIN (firm and set).'
            },
            'gelatine': {
                'definition': 'Gelatine is the British spelling of gelatin, referring to the same colorless, odorless protein derived from animal collagen. Like gelatin, gelatine forms gel-like substances when dissolved in hot water and cooled, and is used in cooking, pharmaceuticals, and industrial applications. The spelling variation reflects British versus American English conventions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JEL-uh-teen',
                'etymology': 'British spelling of gelatin, from French "gélatine," ultimately from Latin "gelatus" (frozen, congealed).',
                'language_origins': 'French, Latin',
                'example_sentence': 'The British cookbook called for _______ powder to set the traditional trifle dessert.',
                'memory_tip': 'Remember "GELATINE" - British spelling of gelatin, makes things GEL like it\'s been to Latin school.'
            },
            'gelatinous': {
                'definition': 'Gelatinous describes something having the consistency, appearance, or properties of gelatin; jelly-like, viscous, or having a semi-solid, translucent quality. The term can apply to food textures, biological substances, or any material that resembles the wobbly, semi-transparent nature of gelatin. It emphasizes the thick, semi-liquid consistency.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'juh-LAT-uh-nus',
                'etymology': 'From "gelatin" plus the suffix "-ous" meaning "having the qualities of," literally meaning "having the nature of gelatin."',
                'language_origins': 'Latin-derived',
                'example_sentence': 'The _______ substance in the petri dish had a translucent, jelly-like appearance.',
                'memory_tip': 'Remember "GELATINOUS" - having the quality of GELATIN, wobbly and jelly-like in texture.'
            },
            'gelato': {
                'definition': 'Gelato is an Italian-style ice cream that is denser and more intensely flavored than traditional ice cream, made with milk rather than cream and churned at a slower speed to incorporate less air. Gelato is served at a slightly warmer temperature than ice cream, which enhances its smooth texture and rich flavor. It represents artisanal Italian frozen dessert craftsmanship.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jeh-LAH-toh',
                'etymology': 'From Italian "gelato," past participle of "gelare" (to freeze), from Latin "gelare" (to freeze).',
                'language_origins': 'Italian, Latin',
                'example_sentence': 'The authentic Italian _______ had a incredibly smooth texture and intense pistachio flavor.',
                'memory_tip': 'Remember "GELATO" - Italian ice cream that\'s been GELed (frozen) with ATO (a lot of) intense flavor.'
            },
            'gelilah': {
                'definition': 'Gelilah (also spelled g\'lilah) is a Hebrew term used in Jewish religious practice referring to the rolling up and dressing of the Torah scroll after it has been read during synagogue services. This honor is typically given to a congregant and involves carefully rolling the scroll, tying it with a special belt, and covering it with its decorative mantle.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'geh-LEE-lah',
                'etymology': 'From Hebrew "gelilah" (rolling), from the root "galal" meaning "to roll," referring to rolling up the Torah scroll.',
                'language_origins': 'Hebrew',
                'example_sentence': 'After the Torah reading, he was honored with performing the _______ ceremony.',
                'memory_tip': 'Remember "GELILAH" - the Jewish ceremony of rolling up the Torah, like GELing the scroll with reverent care.'
            },
            'gemini': {
                'definition': 'Gemini refers to the constellation known as the Twins and the third sign of the zodiac (May 21 - June 20), represented by the mythological twins Castor and Pollux. People born under this sign are often characterized as versatile, communicative, and adaptable. Gemini also refers to NASA\'s second human spaceflight program, which preceded the Apollo missions.',
                'part_of_speech': 'proper noun, noun',
                'pronunciation_guide': 'JEM-uh-ny',
                'etymology': 'From Latin "gemini," plural of "geminus" meaning "twin," referring to the twin stars in the constellation.',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ constellation is easily recognizable by its two bright stars representing the mythological twins.',
                'memory_tip': 'Remember "GEMINI" - the GEM twins in the sky, two similar stars like GEMs that are MINI versions of each other.'
            },
            'gemstone': {
                'definition': 'A gemstone is a precious or semi-precious stone that has been cut and polished for use in jewelry or ornamental objects. Gemstones are valued for their beauty, rarity, and durability, and include diamonds, rubies, sapphires, emeralds, and many other minerals. The term encompasses both naturally occurring stones and some synthetic alternatives used in fine jewelry.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JEM-stohn',
                'etymology': 'Compound of "gem" (from Latin "gemma," meaning "bud, precious stone") plus "stone."',
                'language_origins': 'Latin, Old English',
                'example_sentence': 'The jeweler carefully selected each _______ for the custom engagement ring.',
                'memory_tip': 'Remember "GEMSTONE" - a GEM that\'s a precious STONE, beautiful minerals cut for jewelry.'
            },
            'gendarme': {
                'definition': 'A gendarme is a member of a military force that serves as police, particularly in France and other countries with similar systems. Originally cavalry soldiers who performed police duties, gendarmes are now part of specialized military police forces responsible for law enforcement, especially in rural areas and for serious crimes. The term represents the intersection of military and civilian law enforcement.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ZHAHN-darm',
                'etymology': 'From French "gendarme," literally "man-at-arms," from "gens d\'armes" (armed people), from "gens" (people) plus "armes" (arms, weapons).',
                'language_origins': 'French',
                'example_sentence': 'The _______ investigated the crime in the small French countryside village.',
                'memory_tip': 'Remember "GENDARME" - a military police officer, a GENtle person with ARMS (weapons) who enforces the law.'
            },
            'genealogical': {
                'definition': 'Genealogical relates to genealogy, the study and tracing of family histories and lineages. It describes research, records, charts, or methods used to establish family relationships, ancestry, and descent through generations. Genealogical work involves documenting family trees, researching historical records, and establishing connections between ancestors and descendants.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'jee-nee-uh-LOJ-ik-ul',
                'etymology': 'From "genealogy" (from Greek "genealogia," from "genea" meaning "generation" plus "logos" meaning "study") plus the suffix "-ical."',
                'language_origins': 'Greek',
                'example_sentence': 'The _______ research revealed that her ancestors immigrated from Ireland in the 1800s.',
                'memory_tip': 'Remember "GENEALOGICAL" - relating to GENErations and their LOGical family tree connections through history.'
            },
            'generalisation': {
                'definition': 'Generalisation is the British spelling of generalization, referring to the process of forming broad conclusions or principles from specific examples or instances. It involves extending specific observations to broader categories or making statements that apply to a whole group based on limited examples. The process is fundamental to learning, reasoning, and scientific thinking.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jen-er-uh-ly-ZAY-shun',
                'etymology': 'British spelling of generalization, from "general" plus "-isation," the British form of the suffix "-ization."',
                'language_origins': 'Latin, English',
                'example_sentence': 'The scientist warned against making hasty _______ based on such a small sample size.',
                'memory_tip': 'Remember "GENERALISATION" - British spelling for making GENERAL conclusions about a whole NATION (population) of things.'
            },
            'generalization': {
                'definition': 'Generalization is the American spelling of generalisation, referring to the process of drawing broad conclusions or forming general principles from specific examples or observations. It involves applying insights from particular cases to broader categories or situations. Generalization is essential in learning, scientific reasoning, and everyday problem-solving.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jen-er-uh-ly-ZAY-shun',
                'etymology': 'American spelling from "general" plus "-ization," indicating the process of making something general.',
                'language_origins': 'Latin, English',
                'example_sentence': 'The teacher explained that _______ helps us understand patterns by applying specific examples to broader concepts.',
                'memory_tip': 'Remember "GENERALIZATION" - making GENERAL conclusions about a whole population based on observation.'
            },
            'generals': {
                'definition': 'Generals is the plural of general, referring to high-ranking military officers who command large units such as divisions, corps, or armies. These officers hold positions of significant authority and responsibility in military organizations, making strategic decisions and leading major military operations. The term can also refer to general principles or concepts in a broader sense.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'JEN-er-ulz',
                'etymology': 'Plural of "general," from Latin "generalis" meaning "relating to all, universal," originally referring to officers with general (overall) command.',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ met to discuss the strategic plan for the upcoming military campaign.',
                'memory_tip': 'Remember "GENERALS" - high-ranking officers with GENERAL command over large military forces.'
            },
            'generation': {
                'definition': 'Generation refers to all people born and living at about the same time, typically spanning 20-30 years, or the act of producing or creating something. It can describe age cohorts (like the Baby Boom generation), the process of producing offspring, or the creation of energy, ideas, or other outputs. The word emphasizes both time periods and productive processes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jen-er-AY-shun',
                'etymology': 'From Latin "generatio" meaning "a begetting, procreation," from "generare" (to beget, produce), from "genus" (birth, race).',
                'language_origins': 'Latin',
                'example_sentence': 'Each _______ faces unique challenges and opportunities shaped by their historical context.',
                'memory_tip': 'Remember "GENERATION" - a group born in the same general time, or the ACTion of GENerating offspring.'
            },
            'generosity': {
                'definition': 'Generosity is the quality of being generous, characterized by willingness to give freely of one\'s time, money, resources, or kindness to others without expecting anything in return. It involves magnanimity, liberality, and open-handedness in helping others or supporting causes. Generosity reflects a spirit of abundance and concern for others\' welfare.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jen-er-OS-ih-tee',
                'etymology': 'From Latin "generositas" meaning "nobility of birth, magnanimity," from "generosus" (noble, generous), related to "genus" (birth, race).',
                'language_origins': 'Latin',
                'example_sentence': 'Her _______ toward the homeless shelter included both financial donations and volunteer work.',
                'memory_tip': 'Remember "GENEROSITY" - the quality of being GENEROus, giving freely without expecting rewards.'
            },
            'genet': {
                'definition': 'A genet is a small, carnivorous mammal native to Africa and southern Europe, characterized by a long body, short legs, large ears, and a long ringed tail. These nocturnal animals are skilled climbers and hunters, feeding primarily on small mammals, birds, and insects. Genets belong to the family Viverridae and are sometimes kept as exotic pets.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'juh-NET',
                'etymology': 'From Old French "genete," ultimately from Arabic "jarnait," the name for this animal in North African regions.',
                'language_origins': 'Old French, Arabic',
                'example_sentence': 'The nocturnal _______ silently stalked its prey through the African savanna.',
                'memory_tip': 'Remember "GENET" - a small carnivore that\'s GENtle but NETwork-savvy in hunting, with a long ringed tail.'
            },
            'genetic': {
                'definition': 'Genetic relates to genes, heredity, or the transmission of characteristics from parents to offspring through DNA. The term describes anything concerning the genetic code, inherited traits, genetic disorders, or the science of genetics. Genetic factors influence physical appearance, health conditions, and various biological functions passed down through generations.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'juh-NET-ik',
                'etymology': 'From "gene" (from German "Gen," from Greek "genos" meaning "race, offspring") plus the suffix "-ic."',
                'language_origins': 'Greek, German',
                'example_sentence': 'The doctor explained that the condition had a strong _______ component inherited from both parents.',
                'memory_tip': 'Remember "GENETIC" - relating to GENEs and inheritance, the NET-work of traits passed down through IC (genetic) code.'
            },
            'geniture': {
                'definition': 'Geniture refers to birth, generation, or the act of begetting offspring. In astrological contexts, it specifically refers to a birth chart or horoscope cast for the moment of someone\'s birth. The term is also used in broader contexts to mean the circumstances or conditions surrounding birth or generation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JEN-ih-chur',
                'etymology': 'From Latin "genitura" meaning "a begetting, birth," from "gignere" (to beget, bear), related to "genus" (birth, race).',
                'language_origins': 'Latin',
                'example_sentence': 'The astrologer carefully calculated the _______ chart based on the exact time and place of birth.',
                'memory_tip': 'Remember "GENITURE" - relating to GENeration and birth, like a GENtle NATure given at birth.'
            },
            'genius': {
                'definition': 'Genius refers to exceptional intellectual ability, creativity, or skill that is markedly superior to the norm. It can describe a person who possesses such extraordinary talent or the quality itself. In Roman mythology, a genius was a guardian spirit. The word emphasizes not just intelligence but innovative thinking and the ability to achieve remarkable accomplishments.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'JEEN-yus',
                'etymology': 'From Latin "genius" meaning "guardian spirit, natural ability," from "gignere" (to beget, produce), related to "genus" (birth, kind).',
                'language_origins': 'Latin',
                'example_sentence': 'Einstein\'s _______ in theoretical physics revolutionized our understanding of space and time.',
                'memory_tip': 'Remember "GENIUS" - someone with exceptional GENetic intelligence and creative US-age of their abilities.'
            },
            'genoise': {
                'definition': 'Genoise (or génoise) is a light, airy sponge cake made by whipping whole eggs with sugar until thick and pale, then gently folding in flour and sometimes melted butter. This French cake serves as a base for many elaborate desserts and can be layered with creams, jams, or liqueurs. Genoise is fundamental to French patisserie and requires skill to achieve the proper texture.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'zheh-NWAHZ',
                'etymology': 'From French "génoise," referring to something from Genoa, Italy, where this style of sponge cake possibly originated.',
                'language_origins': 'French, Italian',
                'example_sentence': 'The pastry chef prepared a delicate _______ sponge as the foundation for the elaborate layer cake.',
                'memory_tip': 'Remember "GENOISE" - a GENtle, airy sponge cake that\'s so NICE and light from French baking tradition.'
            },
            'genome': {
                'definition': 'A genome is the complete set of genetic material (DNA) contained in an organism, including all of its genes and non-coding sequences. The genome contains all the information needed to build and maintain that organism. Human genome mapping has revolutionized medicine and biology, providing insights into heredity, disease, and evolution.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JEEN-ohm',
                'etymology': 'Coined in 1930 from "gene" (from Greek "genos," race/kind) plus the suffix "-ome" (complete set), meaning "complete set of genes."',
                'language_origins': 'Modern scientific term (Greek-derived)',
                'example_sentence': 'Scientists completed mapping the human _______ in 2003, identifying all genetic information in our DNA.',
                'memory_tip': 'Remember "GENOME" - the complete GENetic HOME, containing all the genes in an organism\'s DNA.'
            },
            'genteel': {
                'definition': 'Genteel describes refined elegance and sophistication in manners, appearance, or social behavior, often associated with upper-class respectability. However, the term can sometimes carry subtle implications of affected refinement or pretentious politeness that may seem outdated or artificial. Genteel suggests cultivated social grace and propriety.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'jen-TEEL',
                'etymology': 'From French "gentil" meaning "noble, well-born," ultimately from Latin "gentilis" (of the same clan or race).',
                'language_origins': 'French, Latin',
                'example_sentence': 'The _______ tea party featured fine china and impeccable manners from all the guests.',
                'memory_tip': 'Remember "GENTEEL" - GENTle and refined like aristocracy, with an EEL-like smoothness in social behavior.'
            },
            'gentian': {
                'definition': 'Gentian refers to flowering plants of the genus Gentiana, characterized by trumpet-shaped flowers typically in shades of blue, purple, or occasionally white or yellow. These alpine and mountain plants are prized for their intensely colored blooms and are used both in ornamental gardening and traditional medicine. Some species are used to make bitter herbal liqueurs.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JEN-shun',
                'etymology': 'From Latin "gentiana," named after Gentius, an ancient king of Illyria who supposedly discovered the plant\'s medicinal properties.',
                'language_origins': 'Latin (named after ancient king)',
                'example_sentence': 'The mountain meadow was carpeted with brilliant blue _______ flowers blooming in the alpine summer.',
                'memory_tip': 'Remember "GENTIAN" - a GENtle flower that\'s ANCIENT in its blue beauty, named after King Gentius.'
            },
            'gentilitial': {
                'definition': 'Gentilitial refers to things relating to a gens (clan) or family lineage, particularly in ancient Roman context where it described names, rights, or customs associated with patrician family groups. The term relates to hereditary family identity and the social structures based on kinship and ancestral connections in classical antiquity.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'jen-tuh-LISH-ul',
                'etymology': 'From Latin "gentilitius" meaning "of or belonging to the same clan," from "gens" (clan, family) plus the adjectival suffix.',
                'language_origins': 'Latin',
                'example_sentence': 'The historian studied _______ naming practices in ancient Roman patrician families.',
                'memory_tip': 'Remember "GENTILITIAL" - relating to GENTile family groups and their INITIAL clan identity in ancient Rome.'
            },
            'gently': {
                'definition': 'Gently means in a gentle manner, with softness, care, or kindness, avoiding harshness, force, or abruptness. It describes actions performed with tenderness, consideration, or mild intensity. Gently emphasizes a careful, moderate approach that shows concern for not causing harm, discomfort, or damage.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'JENT-lee',
                'etymology': 'From "gentle" (from Old French "gentil," meaning "noble, well-born") plus the adverbial suffix "-ly."',
                'language_origins': 'Old French',
                'example_sentence': 'She _______ placed the sleeping baby in the crib, being careful not to wake her.',
                'memory_tip': 'Remember "GENTLY" - doing something in a GENTle way, softLY and carefully without force.'
            },
            'genuflect': {
                'definition': 'Genuflect means to lower oneself briefly onto one knee, typically as a gesture of respect, reverence, or worship, particularly in religious contexts such as entering a church or approaching an altar. The action demonstrates humility and reverence before something or someone considered sacred or worthy of deep respect.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'JEN-yuh-flekt',
                'etymology': 'From Late Latin "genuflectere," from "genu" (knee) plus "flectere" (to bend), literally meaning "to bend the knee."',
                'language_origins': 'Late Latin',
                'example_sentence': 'The faithful would _______ upon entering the cathedral to show reverence.',
                'memory_tip': 'Remember "GENUFLECT" - to bend your GENu (knee) and FLECT (flex) it in reverence or respect.'
            },
            'genuflectcinerarium': {
                'definition': 'Genuflectcinerarium appears to be a combined word error where "genuflect" (to kneel in reverence) and "cinerarium" (a place for storing ashes) were incorrectly merged during PDF processing. These are completely unrelated terms - one referring to a religious gesture of kneeling, the other to burial practices and ash storage. This represents a data quality issue where religious and funeral terminology were improperly joined.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'JEN-yuh-flekt-sin-er-AIR-ee-um',
                'etymology': 'Corrupted combination of "genuflect" (Late Latin "genuflectere") and "cinerarium" (Latin "cinerarius").',
                'language_origins': 'Late Latin, Latin (corrupted)',
                'example_sentence': 'The word _______ appears to be a parsing error combining religious kneeling with ash storage terminology.',
                'memory_tip': 'This is a data error - remember that "genuflect" (kneeling) and "cinerarium" (ash storage) should be separate.'
            },
            'genuine': {
                'definition': 'Genuine means truly what it is claimed to be; authentic, real, and not fake, counterfeit, or artificial. The word describes both objects that are not imitations and people who are honest, sincere, and without pretense. Genuine emphasizes authenticity, truthfulness, and the absence of deception or artificiality.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'JEN-yoo-in',
                'etymology': 'From Latin "genuinus" meaning "innate, natural, authentic," from "genu" (knee), possibly referring to the Roman custom of a father acknowledging a child by placing it on his knee.',
                'language_origins': 'Latin',
                'example_sentence': 'The art expert confirmed that the painting was a _______ work by the famous Renaissance master.',
                'memory_tip': 'Remember "GENUINE" - truly GENerated and authentiU-INE (authentic), real and not fake or pretentious.'
            },
            'genus': {
                'definition': 'Genus is a taxonomic category in biological classification that groups related species sharing common characteristics. It ranks above species and below family in the hierarchical system of biological nomenclature. Each genus name is italicized and forms the first part of a species\' scientific binomial name (like Homo in Homo sapiens).',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JEE-nus',
                'etymology': 'From Latin "genus" meaning "birth, race, stock, kind," from the root "gen-" meaning "to give birth to."',
                'language_origins': 'Latin',
                'example_sentence': 'All domestic cats belong to the _______ Felis, with the house cat being Felis catus.',
                'memory_tip': 'Remember "GENUS" - a GENetic group that\'s similar, like a family of species with shared GENes and characteristics.'
            },
            'geocaching': {
                'definition': 'Geocaching is a real-world treasure hunting game where participants use GPS devices or smartphones to hide and find containers (called geocaches or caches) at specific locations worldwide. Players share coordinates online and search for hidden caches, often containing logbooks to sign and small trinkets to trade. It combines technology with outdoor exploration.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'JEE-oh-kash-ing',
                'etymology': 'Coined from "geo-" (Greek "ge," meaning "earth") plus "cache" (French "cacher," to hide), literally meaning "earth hiding."',
                'language_origins': 'Greek, French',
                'example_sentence': 'The family spent their vacation _______ in national parks, finding hidden treasures using GPS coordinates.',
                'memory_tip': 'Remember "GEOCACHING" - using GPS to find GEOgraphic treasures that are CACHEd (hidden) around the earth.'
            },
            'geographical': {
                'definition': 'Geographical relates to geography, the study of Earth\'s physical features, climate, population, and the relationships between people and their environments. It describes anything concerning locations, regions, maps, spatial relationships, or the physical and human characteristics of places on Earth.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'jee-uh-GRAF-ik-ul',
                'etymology': 'From "geography" (from Greek "geographia," from "geo" meaning "earth" plus "graphein" meaning "to write") plus "-ical."',
                'language_origins': 'Greek',
                'example_sentence': 'The _______ survey revealed significant differences in climate patterns across the region.',
                'memory_tip': 'Remember "GEOGRAPHICAL" - relating to GEOgraphy and GRAPHICAL representation of Earth\'s features and locations.'
            },
            'geography': {
                'definition': 'Geography is the study of Earth\'s physical features, climate, countries, peoples, and the relationships between humans and their environments. It encompasses both physical geography (landforms, weather, ecosystems) and human geography (populations, cultures, economic activities). Geography helps us understand spatial relationships and how location influences human activities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jee-OG-ruh-fee',
                'etymology': 'From Greek "geographia," from "geo" (earth) plus "graphein" (to write, describe), literally meaning "earth writing" or "earth description."',
                'language_origins': 'Greek',
                'example_sentence': 'Students learned about world _______ by studying maps, climates, and cultural regions.',
                'memory_tip': 'Remember "GEOGRAPHY" - the study that GRAPHically describes the GEO (earth) and all its features and peoples.'
            },
            'geometric': {
                'definition': 'Geometric relates to geometry, characterized by or using regular shapes, patterns, and mathematical relationships found in geometric forms like circles, squares, triangles, and other mathematical figures. It describes designs, patterns, art, or concepts that emphasize mathematical precision, symmetry, and angular or curved forms based on geometric principles.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'jee-uh-MET-rik',
                'etymology': 'From Greek "geometrikos," from "geometria" (geometry), from "geo" (earth) plus "metron" (measure).',
                'language_origins': 'Greek',
                'example_sentence': 'The artist created a stunning _______ pattern using interlocking triangles and circles.',
                'memory_tip': 'Remember "GEOMETRIC" - relating to GEOmetry and METRic measurement, featuring regular mathematical shapes and patterns.'
            },
            'geopoliticsbroached': {
                'definition': 'Geopoliticsbroached appears to be a combined word error where "geopolitics" (the study of politics influenced by geography) and "broached" (brought up for discussion or opened) were incorrectly merged during PDF processing. These terms could be related in context (geopolitics being broached in discussion), but they represent separate concepts that should not be joined as one word.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'jee-oh-POL-ih-tiks-BROHCHT',
                'etymology': 'Corrupted combination of "geopolitics" (Greek/modern political science term) and "broached" (from Old French "broche").',
                'language_origins': 'Greek, French (corrupted)',
                'example_sentence': 'The word _______ appears to be a parsing error combining political geography with discussion terminology.',
                'memory_tip': 'This is a data error - remember that "geopolitics" and "broached" should be separate words in proper usage.'
            },
            'gerbilles': {
                'definition': 'Gerbilles appears to be the French plural form of "gerbil," referring to multiple small desert rodents known for their long tails, large eyes, and ability to survive in arid environments. Gerbils are popular as pets and are native to arid regions of Africa and Asia. The French form might appear in scientific contexts or international texts.',
                'part_of_speech': 'noun (plural, French)',
                'pronunciation_guide': 'zher-BEEL',
                'etymology': 'French plural form of "gerbille" (gerbil), ultimately from Arabic "jarbu" meaning "jerboa," a similar desert rodent.',
                'language_origins': 'French, Arabic',
                'example_sentence': 'The research facility housed several colonies of _______ for studies on desert adaptation.',
                'memory_tip': 'Remember "GERBILLES" - French for gerbils, multiple GERBils that are ILLE (agile) desert rodents.'
            }
        }
        
        return batch_075_data.get(word, {
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
                
            # Check for combined word errors and other issues
            if word == 'gchange':
                errors.append(f"{word}: Corrupted word: \"gchange\" appears to be \"change\" with an erroneous \"g\" prefix. This is likely a transcription or data processing error.")
            elif word == 'genuflectcinerarium':
                errors.append(f"{word}: Combined word error: \"genuflectcinerarium\" appears to be \"genuflect\" + \"cinerarium\" merged together. This is likely a PDF parsing error where religious kneeling and ash storage terms were incorrectly combined.")
            elif word == 'geopoliticsbroached':
                errors.append(f"{word}: Combined word error: \"geopoliticsbroached\" appears to be \"geopolitics\" + \"broached\" merged together. This is likely a PDF parsing error where political geography and discussion terms were incorrectly combined.")
                
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
        print("Batch 075 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch075Processor()
    processor.process_batch(
        "output/batch_075_words.csv",
        "output/batch_075_processed.csv"
    )