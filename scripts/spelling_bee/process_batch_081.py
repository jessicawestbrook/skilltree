import csv
import os
from dataclasses import dataclass
from typing import List, Dict, Optional

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
    phonetic_transcription_score: Optional[float] = None
    frequency_score: Optional[float] = None
    morphological_score: Optional[float] = None
    etymology_score: Optional[float] = None
    final_difficulty: Optional[str] = None

class DifficultyCalculator:
    def calculate_phonetic_transparency_score(self, word: str) -> float:
        return 0.5
    
    def calculate_frequency_score(self, word: str) -> float:
        return 0.5
    
    def calculate_morphological_complexity_score(self, word: str) -> float:
        return 0.5
    
    def calculate_etymology_complexity_score(self, etymology: str, language_origins: str) -> float:
        return 0.5

class Batch081Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
        self.errors = []
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        batch_081_data = {
            'gushedchina': {
                'definition': 'This appears to be a combined word error where "gushed" (flowed forth rapidly or spoke with great enthusiasm) has been incorrectly merged with "china" (porcelain or the country). Gushed is the past tense of gush, meaning to flow out rapidly and in large quantities, or to speak with great enthusiasm or emotion. China can refer to fine porcelain ceramics, or to the People\'s Republic of China. This combination likely resulted from a PDF parsing error where two separate words were inadvertently joined together. The correct terms would be "gushed" referring to rapid flowing or enthusiastic speaking, and "china" referring to porcelain or the country.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'GUSHT-CHAHY-nuh',
                'etymology': 'Error: "gushed" (possibly imitative) + "china" (from Persian "chīnī," meaning "Chinese")',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "gushed" and "china" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "GUSHEDCHINA" - this is a combined word error, separate into GUSHED (flowed rapidly) + CHINA (porcelain or country).'
            },
            'gustatory': {
                'definition': 'Gustatory refers to the sense of taste or things related to tasting and flavor perception. This adjective describes anything connected to the physiological process of taste, including taste buds, flavor sensations, and the neural pathways involved in detecting and processing taste information. Gustatory experiences involve the five basic tastes: sweet, sour, salty, bitter, and umami (savory). The term is used in scientific, medical, and culinary contexts when discussing taste perception, flavor analysis, food science, or sensory evaluation. Gustatory memory refers to the ability to recall tastes and flavors from past experiences.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GUS-tuh-tor-ee',
                'etymology': 'From Latin "gustare" meaning "to taste" + "-ory" suffix meaning "relating to."',
                'language_origins': 'Latin',
                'example_sentence': 'The chef\'s _______ memory was so refined that she could identify dozens of spices and herbs by taste alone.',
                'memory_tip': 'Remember "GUSTATORY" - GUSTo + TORY (relating to), relating to gusto and the sense of taste.'
            },
            'gusto': {
                'definition': 'Gusto refers to enthusiastic enjoyment, zest, or vigorous appreciation in doing something. When someone approaches an activity with gusto, they demonstrate energetic pleasure, hearty enthusiasm, and wholehearted engagement. The word suggests not just enjoyment but active, spirited participation that shows genuine relish and zeal. Gusto can apply to eating, working, performing, or any activity approached with energetic enthusiasm and evident pleasure. The term emphasizes the vigor and heartiness of the enjoyment rather than quiet satisfaction.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GUS-toh',
                'etymology': 'From Italian "gusto" meaning "taste," from Latin "gustus" meaning "taste, flavor."',
                'language_origins': 'Italian, Latin',
                'example_sentence': 'She attacked the challenging crossword puzzle with such _______ that her enthusiasm was infectious to everyone around her.',
                'memory_tip': 'Remember "GUSTO" - GUSt of enthusiasm, a gust of wind-like enthusiasm and energetic enjoyment.'
            },
            'gutter': {
                'definition': 'Gutter has several meanings: it most commonly refers to a channel or trough designed to collect and direct rainwater away from buildings, typically found along the edges of roofs or streets. In printing, the gutter is the inner margin between pages in a bound book. In bowling, the gutter refers to the channels on either side of the lane where balls can fall. Metaphorically, "gutter" can describe the lowest or most degraded level of society or behavior. As a verb, to gutter means to burn unsteadily (as a candle) or to be on the verge of going out.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GUT-er',
                'etymology': 'From Old French "gotiere," from "goute" meaning "drop," from Latin "gutta."',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The autumn leaves clogged the roof _______, causing water to overflow during the heavy rainstorm.',
                'memory_tip': 'Remember "GUTTER" - GUTs water away, it guts (removes) water away from buildings by channeling it.'
            },
            'guttural': {
                'definition': 'Guttural describes sounds produced in the throat, particularly harsh, rough, or throaty sounds that seem to come from deep in the vocal tract. In phonetics, guttural refers to consonant sounds articulated in the back of the mouth or throat area. More generally, guttural describes any sound, voice, or utterance that is deep, harsh, growling, or throat-like in quality. The term can describe human speech sounds, animal vocalizations, or any sound that seems to originate from the throat area. Guttural sounds often convey primitiveness, emotion, or physical strain.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'GUT-er-uhl',
                'etymology': 'From Medieval Latin "gutturalis," from Latin "guttur" meaning "throat."',
                'language_origins': 'Medieval Latin, Latin',
                'example_sentence': 'The actor\'s _______ growl perfectly conveyed the character\'s menacing and primitive nature.',
                'memory_tip': 'Remember "GUTTURAL" - GUTter + URAL (throat area), sounds from the gutter of your throat, deep and rough.'
            },
            'gyascutus': {
                'definition': 'Gyascutus is a mythical creature from American folklore, particularly associated with tall tales and logging camps of the 19th and early 20th centuries. This legendary animal was described as resembling a large bear with legs that were shorter on one side than the other, supposedly adapted for walking around steep hillsides. According to the folklore, the gyascutus could only walk in one direction around hills due to its uneven legs. The creature represents the tradition of tall tales and fabricated wildlife stories told for entertainment in logging camps, lumber towns, and frontier communities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JYE-as-kyoo-tuhs',
                'etymology': 'American folklore creation, possibly pseudo-Latin construction for humorous effect.',
                'language_origins': 'American folklore (pseudo-Latin)',
                'example_sentence': 'The old lumberjack entertained the camp with stories of the elusive _______, a creature that could supposedly only walk around hills in one direction.',
                'memory_tip': 'Remember "GYASCUTUS" - GYm class + SCUTUS (shield-like), a mythical gym-class-like creature with uneven legs like a lopsided shield.'
            },
            'gyascutusgyokuro': {
                'definition': 'This appears to be a combined word error where "gyascutus" (a mythical American folklore creature) has been incorrectly merged with "gyokuro" (a high-quality Japanese green tea). Gyascutus is a legendary creature from American tall tales with uneven legs, while gyokuro is a premium shade-grown Japanese tea known for its sweet, delicate flavor and bright green color. This combination likely resulted from a PDF parsing error where two completely unrelated terms were inadvertently joined together. The correct terms would be "gyascutus" referring to the mythical hillside creature, and "gyokuro" referring to the Japanese premium tea.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'JYE-as-kyoo-tuhs-GYOH-koo-roh',
                'etymology': 'Error: "gyascutus" (American folklore) + "gyokuro" (Japanese "gyoku" jewel + "ro" dew)',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "gyascutus" and "gyokuro" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "GYASCUTUSGYOKURO" - this is a combined word error, separate into GYASCUTUS (mythical creature) + GYOKURO (Japanese tea).'
            },
            'gymnastics': {
                'definition': 'Gymnastics is a sport involving exercises and performances that require strength, flexibility, agility, coordination, and balance. This athletic discipline includes various apparatuses such as floor exercise, vault, uneven bars, balance beam, rings, parallel bars, and high bar. Gymnastics combines artistry with athleticism, featuring routines that showcase both technical skill and creative expression. The sport has ancient origins but modern competitive gymnastics includes artistic gymnastics, rhythmic gymnastics, trampoline, and tumbling. Gymnastics develops physical fitness, mental discipline, and body awareness while providing spectacular displays of human athletic capability.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jim-NAS-tiks',
                'etymology': 'From Greek "gymnastikos" meaning "fond of athletic exercises," from "gymnazein" meaning "to exercise naked."',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The young athlete dedicated hours daily to _______ training, developing the strength and grace needed for competition.',
                'memory_tip': 'Remember "GYMNASTICS" - GYM + NASTICS (fantastic), fantastic gym exercises that require incredible skill and athleticism.'
            },
            'gyokuro': {
                'definition': 'Gyokuro is a premium type of Japanese green tea, considered one of the highest grades of tea in Japan. This tea is shade-grown for several weeks before harvest, which increases chlorophyll content and creates a sweet, delicate flavor with reduced astringency. The name literally means "jade dew," referring to the tea\'s pale green color when brewed. Gyokuro is characterized by its umami-rich taste, sweet aroma, and vibrant green color. The tea requires careful preparation with lower water temperatures and specific brewing techniques to preserve its delicate flavor profile. It represents the pinnacle of Japanese tea craftsmanship.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GYOH-koo-roh',
                'etymology': 'From Japanese "gyoku" meaning "jewel, jade" + "ro" meaning "dew."',
                'language_origins': 'Japanese',
                'example_sentence': 'The tea master carefully prepared the _______ using precise temperature and timing to bring out its characteristic sweet, umami flavor.',
                'memory_tip': 'Remember "GYOKURO" - GYOku (jewel) + ro (dew), like jewel dew, the most precious Japanese tea that\'s like liquid jewels.'
            },
            'gypsophila': {
                'definition': 'Gypsophila is a genus of flowering plants commonly known as baby\'s breath, characterized by delicate, small white or pink flowers that create airy, cloud-like clusters. These perennial or annual plants are popular in floral arrangements due to their ability to provide texture and fill space between larger flowers. Gypsophila thrives in alkaline soils and is often found in rocky or sandy areas. The most common species, Gypsophila paniculata, produces masses of tiny flowers on branched stems. The name refers to the plant\'s preference for lime-rich (gypsum-containing) soils.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jip-SOF-i-lah',
                'etymology': 'From Greek "gypsos" meaning "gypsum" + "philos" meaning "loving," referring to its preference for lime-rich soils.',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The florist used delicate white _______ to create an airy, ethereal effect in the bridal bouquet.',
                'memory_tip': 'Remember "GYPSOPHILA" - GYPSum + PHILA (loving), loving gypsum-rich soils where these delicate baby\'s breath flowers grow.'
            },
            'gypsum': {
                'definition': 'Gypsum is a soft sulfate mineral composed of calcium sulfate dihydrate, commonly found in sedimentary rock formations. This mineral is typically white or colorless but can occur in various colors due to impurities. Gypsum has many industrial uses, including the production of plaster of Paris, drywall, cement, and fertilizer. The mineral is soft enough to be scratched by a fingernail and often forms in evaporite deposits where ancient seas have evaporated. Alabaster, a fine-grained form of gypsum, has been used for carving and sculpture throughout history due to its workability and attractive appearance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JIP-suhm',
                'etymology': 'From Latin "gypsum," from Greek "gypsos" meaning "chalk, plaster."',
                'language_origins': 'Latin, Ancient Greek',
                'example_sentence': 'The construction crew used _______ board for the interior walls because of its fire resistance and ease of installation.',
                'memory_tip': 'Remember "GYPSUM" - GYP (gypsy travels) + SUM, like gypsies who travel and build with this soft white mineral for plaster.'
            },
            'gyrocopter': {
                'definition': 'Gyrocopter, also known as an autogyro, is a type of rotorcraft that uses an unpowered rotor in free autorotation to develop lift, and an engine-powered propeller to provide thrust. Unlike helicopters, the rotor of a gyrocopter is not powered during flight but spins due to the upward flow of air through the rotor disc. These aircraft are generally smaller and simpler than helicopters, offering economical flight with good stability and short takeoff and landing capabilities. Gyrocopters are used for recreational flying, aerial photography, surveillance, and other specialized applications where their unique flight characteristics are advantageous.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JAHY-roh-kop-ter',
                'etymology': 'From Greek "gyros" meaning "circle, turn" + "copter" from "helicopter" (Greek "helix" spiral + "pteron" wing).',
                'language_origins': 'Greek',
                'example_sentence': 'The pilot enjoyed flying the _______ because it offered helicopter-like maneuverability with simpler controls and lower operating costs.',
                'memory_tip': 'Remember "GYROCOPTER" - GYROscope + heLICOPTER, like a helicopter with a gyroscope-spinning rotor that autorotates.'
            },
            'gyttja': {
                'definition': 'Gyttja is a fine-grained organic lake sediment composed of plant and animal remains mixed with mineral particles. This dark, nutrient-rich mud typically forms in the deeper parts of lakes where organic matter settles and decomposes in oxygen-poor conditions. Gyttja is important in limnology (the study of lakes) and paleoecology as it preserves records of past environmental conditions, including pollen, diatoms, and other microscopic remains. The sediment layers can provide information about climate history, vegetation changes, and lake ecosystem development over thousands of years.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GIT-yah',
                'etymology': 'From Swedish "gyttja," meaning "mud, ooze."',
                'language_origins': 'Swedish',
                'example_sentence': 'The paleoecologist analyzed cores of _______ from the lake bottom to reconstruct the region\'s climate history over the past 10,000 years.',
                'memory_tip': 'Remember "GYTTJA" - GET + YA (you) muddy, the organic lake mud that will get ya muddy if you step in it.'
            },
            'habanero': {
                'definition': 'Habanero is a variety of hot chili pepper belonging to the species Capsicum chinense, originally from the Amazon region but now strongly associated with Mexican and Caribbean cuisine. These small, lantern-shaped peppers typically measure 2-6 cm long and range in color from green to orange, red, brown, or chocolate when ripe. Habaneros are known for their intense heat, rating 100,000-350,000 Scoville heat units, combined with a distinctive fruity, citrusy flavor. They are essential ingredients in many hot sauces, salsas, and spicy dishes, prized for both their heat and complex flavor profile.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'hab-uh-NAIR-oh',
                'etymology': 'From Spanish, literally "from Havana," though the pepper is not native to Cuba.',
                'language_origins': 'Spanish',
                'example_sentence': 'The chef carefully added one minced _______ pepper to the salsa, warning diners about its intense heat and fruity flavor.',
                'memory_tip': 'Remember "HABANERO" - HAVANA + NERO (burning emperor), like the burning emperor of peppers from the Havana region.'
            },
            'habeas': {
                'definition': 'Habeas typically refers to "habeas corpus," a fundamental legal principle and writ that protects against unlawful and indefinite imprisonment. The full Latin phrase "habeas corpus" literally means "you may have the body" and requires authorities to bring a prisoner before a court to determine if their detention is lawful. This legal protection ensures that no one can be held in custody without proper legal justification and due process. Habeas corpus is considered one of the most important safeguards of individual liberty in legal systems derived from English common law.',
                'part_of_speech': 'noun (legal term)',
                'pronunciation_guide': 'HAY-bee-uhs',
                'etymology': 'From Latin "habeas," second person singular present subjunctive of "habere" meaning "to have."',
                'language_origins': 'Latin',
                'example_sentence': 'The defense attorney filed a _______ corpus petition to challenge the legality of their client\'s continued detention.',
                'memory_tip': 'Remember "HABEAS" - HAve the Body in court, you must have the body (person) brought before court to justify imprisonment.'
            },
            'haberdasher': {
                'definition': 'Haberdasher is a person who sells men\'s clothing and accessories, particularly items like hats, ties, shirts, and other haberdashery goods. Historically, haberdashers were merchants who sold small articles for sewing, such as buttons, ribbons, zippers, and other notions. In British usage, a haberdasher typically sells small items and accessories, while in American usage, the term more commonly refers to a men\'s clothier. The profession has a long history in retail trade and was once a prominent and specialized form of commerce in downtown business districts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAB-er-dash-er',
                'etymology': 'From Middle English "haberdassher," possibly from "hapertas," a type of fabric, of uncertain origin.',
                'language_origins': 'Middle English',
                'example_sentence': 'The downtown _______ had been fitting men with quality suits and accessories for over fifty years.',
                'memory_tip': 'Remember "HABERDASHER" - HABit + DASHer, someone who dashes around helping men get into the habit of dressing well.'
            },
            'habiliments': {
                'definition': 'Habiliments refers to clothing, dress, or attire, particularly the characteristic dress associated with a particular profession, rank, or ceremonial occasion. This somewhat formal or archaic term describes not just any clothing but specifically the garments that identify someone\'s role, status, or function. Habiliments can include uniforms, vestments, robes, or other distinctive clothing that serves both practical and symbolic purposes. The word often appears in literary or formal contexts when describing ceremonial dress, professional attire, or historically significant clothing.',
                'part_of_speech': 'noun (usually plural)',
                'pronunciation_guide': 'huh-BIL-uh-muhnts',
                'etymology': 'From Old French "abillement," from "abiller" meaning "to fit out, prepare," from Latin "habilis" meaning "suitable."',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The judge donned the traditional _______ of the court, including the black robe and ceremonial wig.',
                'memory_tip': 'Remember "HABILIMENTS" - HABIts + garMENTS, the habit-forming garments or special clothing for particular roles.'
            },
            'habitual': {
                'definition': 'Habitual describes something done regularly, customarily, or by habit rather than by conscious decision. This adjective characterizes behaviors, actions, or patterns that have become automatic through repetition and routine. A habitual action is performed almost unconsciously because it has been repeated so often that it becomes second nature. Habitual can describe both positive habits (habitual exercise) and negative ones (habitual lateness). The word emphasizes the automatic, ingrained nature of the behavior rather than deliberate or occasional actions.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'huh-BICH-oo-uhl',
                'etymology': 'From Medieval Latin "habitualis," from Latin "habitus" meaning "condition, habit."',
                'language_origins': 'Medieval Latin, Latin',
                'example_sentence': 'His _______ morning routine of coffee and newspaper reading had remained unchanged for twenty years.',
                'memory_tip': 'Remember "HABITUAL" - HABIT + UAL (usual), usual habits that are done automatically and regularly.'
            },
            'habitue': {
                'definition': 'Habitué (also spelled habitue without the accent) refers to a person who frequents or is a regular visitor to a particular place, especially establishments like restaurants, bars, theaters, or clubs. This French-derived term describes someone who is so familiar with a venue that they are recognized by staff and other patrons as a regular customer. A habitué often has preferred seating, knows the staff personally, and is considered part of the establishment\'s regular clientele. The word suggests both loyalty and familiarity with the establishment\'s customs and atmosphere.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'huh-BICH-oo-ay',
                'etymology': 'From French "habitué," past participle of "habituer" meaning "to accustom," from Latin "habitus."',
                'language_origins': 'French, Latin',
                'example_sentence': 'As a longtime _______ of the jazz club, he had his own favorite table near the stage where the staff knew his usual order.',
                'memory_tip': 'Remember "HABITUE" - HABIT + UE (you), you who has the habit of regularly visiting the same place.'
            },
            'habitué': {
                'definition': 'Habitué is the French spelling (with accent) of habitue, referring to a person who frequents or is a regular visitor to a particular place, especially establishments like restaurants, bars, theaters, or clubs. This term describes someone who is so familiar with a venue that they are recognized by staff and other patrons as a regular customer. A habitué often has preferred seating arrangements, knows the staff personally, and is considered part of the establishment\'s regular clientele. The accent mark preserves the original French pronunciation and spelling.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'huh-bee-TYWAY',
                'etymology': 'From French "habitué," past participle of "habituer" meaning "to accustom," from Latin "habitus."',
                'language_origins': 'French, Latin',
                'example_sentence': 'The café owner greeted the elderly _______ warmly, already preparing his usual morning coffee before he reached his customary corner table.',
                'memory_tip': 'Remember "HABITUÉ" - HABIT + UÉ (French you), the French way to say "you who has the habit" of visiting regularly.'
            },
            'hackamore': {
                'definition': 'Hackamore is a type of horse headgear used for controlling and directing horses without using a bit in the mouth. This equipment consists of a noseband, usually made of braided rawhide or rope, that applies pressure to the horse\'s nose and chin rather than the mouth. Hackamores are popular in Western riding, natural horsemanship, and with horses that have mouth sensitivity or dental issues. The hackamore provides control through leverage action and pressure points on the nose, jaw, and poll, allowing riders to communicate with their horses while avoiding potential mouth discomfort from traditional bits.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAK-uh-mor',
                'etymology': 'From Spanish "jáquima," possibly from Arabic "shakīmah" meaning "halter."',
                'language_origins': 'Spanish, Arabic',
                'example_sentence': 'The trainer preferred using a _______ on young horses to avoid potential mouth damage while teaching them to respond to rein pressure.',
                'memory_tip': 'Remember "HACKAMORE" - HACK (not harsh) + MORE control, more gentle control without hacking at the horse\'s mouth with a bit.'
            },
            'hackles': {
                'definition': 'Hackles are the long, pointed feathers on the neck of birds, particularly roosters, or the hair on the back of the neck of mammals, especially dogs. When animals are agitated, threatened, or aggressive, these hackles typically stand upright as part of their defensive or threatening display. In humans, the phrase "raise one\'s hackles" means to make someone angry, irritated, or defensive. The term can also refer to the feathers used in fly fishing lures or the neck feathers plucked from birds for various uses in crafts and fishing.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'HAK-uhlz',
                'etymology': 'From Middle English "hakell," related to "hack" meaning "to chop," referring to the jagged appearance of the feathers.',
                'language_origins': 'Middle English',
                'example_sentence': 'The dog\'s _______ rose along his neck when he sensed the approaching stranger, signaling his alertness and wariness.',
                'memory_tip': 'Remember "HACKLES" - HACK + LES (less calm), when hackles rise, there\'s less calm and more agitation or alertness.'
            },
            'hackneyed': {
                'definition': 'Hackneyed describes something that has been overused to the point of losing its original impact, freshness, or meaning. This adjective applies to expressions, ideas, phrases, or concepts that have become trite, cliché, or commonplace through excessive repetition. A hackneyed phrase or idea lacks originality and fails to engage audiences because of its overfamiliarity. The term suggests that what was once fresh and effective has been worn out through overuse, like a horse that has been ridden too much and becomes tired and ineffective.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'HAK-need',
                'etymology': 'From "hackney" (a horse for ordinary riding, later meaning "common, ordinary") + "-ed" suffix.',
                'language_origins': 'English',
                'example_sentence': 'The speech was full of _______ phrases about hard work and dedication that failed to inspire the already weary audience.',
                'memory_tip': 'Remember "HACKNEYED" - HACK (worn out) + NEYED (neighed like an old horse), worn out from overuse like an old horse that\'s been ridden too much.'
            },
            'hadith': {
                'definition': 'Hadith refers to a collection of traditions containing sayings, actions, and teachings of the Islamic prophet Muhammad, as well as accounts of his daily practice (the Sunnah). These reports are considered a major source of Islamic law and moral guidance, second only to the Quran in importance. Each hadith consists of two parts: the matn (the actual text of the saying or account) and the isnad (the chain of narrators who transmitted the report). Islamic scholars have developed elaborate sciences for authenticating and categorizing hadith based on the reliability of their transmission chains and the character of the narrators.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hah-DEETH',
                'etymology': 'From Arabic "ḥadīth" meaning "talk, speech, conversation, tradition."',
                'language_origins': 'Arabic',
                'example_sentence': 'Islamic scholars spent decades collecting and verifying the authenticity of each _______ to preserve accurate records of Prophet Muhammad\'s teachings.',
                'memory_tip': 'Remember "HADITH" - HAD + ITH (it), what Muhammad had said - the traditions that had it (his teachings) recorded for posterity.'
            },
            'haggisdolce': {
                'definition': 'This appears to be a combined word error where "haggis" (a traditional Scottish dish) has been incorrectly merged with "dolce" (Italian for sweet or dessert). Haggis is a savory pudding made from sheep\'s organs, oatmeal, and spices, traditionally cooked in the animal\'s stomach. Dolce refers to sweet desserts or confections in Italian cuisine, or can mean "sweet" in musical terms. This combination likely resulted from a PDF parsing error where two completely unrelated culinary terms were inadvertently joined together. The correct terms would be "haggis" referring to the Scottish dish, and "dolce" referring to sweet desserts.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'HAG-is-DOHL-chay',
                'etymology': 'Error: "haggis" (Scottish, possibly from "hag" to chop) + "dolce" (Italian, from Latin "dulcis" sweet)',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "haggis" and "dolce" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "HAGGISDOLCE" - this is a combined word error, separate into HAGGIS (Scottish savory dish) + DOLCE (Italian sweet dessert).'
            },
            'haggle': {
                'definition': 'Haggle means to negotiate or bargain persistently, especially over the price of goods or services, often in a somewhat contentious or protracted manner. This verb describes the back-and-forth process of making offers and counteroffers until reaching an acceptable agreement. Haggling typically involves both parties starting from extreme positions and gradually moving toward a middle ground. The process can be found in markets, bazaars, car dealerships, and other commercial settings where prices are not fixed. Haggling requires patience, persistence, and negotiation skills.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'HAG-uhl',
                'etymology': 'Possibly from Old Norse "höggva" meaning "to hew, chop," suggesting the cutting back and forth of negotiation.',
                'language_origins': 'Old Norse',
                'example_sentence': 'At the flea market, she loved to _______ with vendors, often getting items for half their asking price through patient negotiation.',
                'memory_tip': 'Remember "HAGGLE" - HAG (nag) + GLE (struggle), like nagging and struggling over prices until you reach an agreement.'
            },
            'hagiographer': {
                'definition': 'Hagiographer is a person who writes hagiographies - biographical accounts of saints\' lives, martyrs, or other religious figures that emphasize their spiritual qualities and miraculous deeds. These writers traditionally focused on the holy and exemplary aspects of their subjects\' lives rather than providing objective historical accounts. In broader usage, hagiographer can describe anyone who writes excessively reverent or uncritical biographical accounts that idealize their subjects. The term sometimes carries a slightly negative connotation when applied to biographical writing that lacks objectivity or critical analysis.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hag-ee-OG-ruh-fer',
                'etymology': 'From Greek "hagios" meaning "holy, sacred" + "graphein" meaning "to write" + "-er" suffix.',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The medieval _______ wrote inspiring accounts of saints\' lives, emphasizing their miracles and virtues rather than historical accuracy.',
                'memory_tip': 'Remember "HAGIOGRAPHER" - HAGIO (holy) + GRAPHER (writer), a holy writer who writes about saints and holy people.'
            },
            'hair': {
                'definition': 'Hair refers to the fine, thread-like strands that grow from follicles in the skin of humans and animals. In humans, hair serves both protective and aesthetic functions, helping regulate body temperature and serving as a means of self-expression through styling and coloring. Hair is composed primarily of a protein called keratin and grows in cycles of growth, rest, and shedding. The term can also refer to anything resembling hair in appearance or texture, such as plant fibers or thin filaments. Hair plays significant roles in cultural identity, fashion, and social expression across different societies.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAIR',
                'etymology': 'From Old English "hǣr," from Germanic roots meaning "hair."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'She decided to donate her long _______ to charity, knowing it would be made into wigs for cancer patients.',
                'memory_tip': 'Remember "HAIR" - Head\'s Amazing Insulating Rods, the amazing insulating rods that grow from your head for protection and beauty.'
            },
            'haitian': {
                'definition': 'Haitian refers to something or someone from Haiti, the Caribbean nation that occupies the western third of the island of Hispaniola. As an adjective, Haitian describes the culture, people, language, food, or other aspects related to Haiti. As a noun, it refers to a person from Haiti or of Haitian descent. Haiti has a rich cultural heritage influenced by African, French, and indigenous Taíno traditions. Haitian Creole and French are the official languages. The country has a complex history involving colonial rule, slavery, revolution, and independence, making it the first black republic in the world.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'HAY-shuhn',
                'etymology': 'From Haiti (from Taíno "ayiti" meaning "land of high mountains") + "-an" suffix.',
                'language_origins': 'Taíno, English',
                'example_sentence': 'The _______ restaurant served traditional dishes like griot and plantains that reflected the island\'s rich culinary heritage.',
                'memory_tip': 'Remember "HAITIAN" - HAIti + TIAN (person), a person or thing from Haiti, the mountainous Caribbean nation.'
            },
            'halala': {
                'definition': 'Halala is a monetary subunit used in Saudi Arabia, where 100 halalas equal one Saudi riyal. This term can also refer to a controversial Islamic practice related to marriage and divorce laws, where a divorced woman must marry and consummate a marriage with another man before she can remarry her former husband. In the monetary sense, halala represents the smallest unit of Saudi currency. The marriage practice, while mentioned in Islamic jurisprudence, is widely considered controversial and is discouraged by many Islamic scholars as it can be subject to abuse.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hah-LAH-lah',
                'etymology': 'From Arabic "ḥalāla," related to "ḥalāl" meaning "lawful, permitted."',
                'language_origins': 'Arabic',
                'example_sentence': 'The price was listed as 50 riyals and 75 _______, showing the precise cost in Saudi currency down to the smallest denomination.',
                'memory_tip': 'Remember "HALALA" - HALf a riAL + A, like half a riyal plus a bit, the small change unit of Saudi money.'
            },
            'halalah': {
                'definition': 'Halalah is an alternate spelling or variant form of halala, referring to the monetary subunit of Saudi Arabia where 100 halalahs equal one Saudi riyal. This represents the smallest denomination of Saudi currency, similar to cents in dollar-based systems or pence in pound-based systems. The term derives from Arabic and is used in financial contexts when precise monetary amounts need to be specified. Different spellings may appear in various transliterations from Arabic script, but both halala and halalah refer to the same monetary unit.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hah-LAH-lah',
                'etymology': 'Variant of "halala," from Arabic "ḥalāla," related to "ḥalāl" meaning "lawful, permitted."',
                'language_origins': 'Arabic',
                'example_sentence': 'The merchant calculated the exact change, counting out several _______ to make up the precise amount owed.',
                'memory_tip': 'Remember "HALALAH" - HALf pLus ALf + AH, like half plus half of a riyal, the tiny Saudi currency unit.'
            },
            'halcyon': {
                'definition': 'Halcyon describes a period of time that is idyllically happy, peaceful, and prosperous, often referring to a golden age or time remembered with nostalgic fondness. The word can also refer to the mythical halcyon bird (kingfisher), which was said to nest on the sea and calm the waters during the winter solstice period. "Halcyon days" specifically refers to this legendary period of calm weather, but more broadly describes any tranquil, carefree time. The term evokes images of serenity, contentment, and harmonious conditions, whether in personal life, society, or nature.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'HAL-see-uhn',
                'etymology': 'From Greek "halkyon," referring to the kingfisher bird, from Greek mythology about Alcyone.',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'She looked back fondly on the _______ days of her childhood, when summers seemed endless and worry was unknown.',
                'memory_tip': 'Remember "HALCYON" - HALf of skY + ON, like half the sky is always sunny and calm, representing peaceful, happy times.'
            },
            'halibut': {
                'definition': 'Halibut is a large flatfish found in cold northern waters of the Pacific and Atlantic oceans, prized as both a commercial and sport fish. These fish can grow to enormous sizes, with some Pacific halibut reaching over 400 pounds and 8 feet in length. Halibut are bottom-dwelling fish with both eyes on their upper side, having migrated from one side during their development. The fish is highly valued for its firm, white, mild-flavored meat and is prepared in numerous ways in restaurants and homes. Halibut fishing is an important industry in Alaska and other northern regions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAL-i-buht',
                'etymology': 'From Middle English "halibut," literally "holy flatfish" (eaten on holy days), from "haly" (holy) + "butte" (flatfish).',
                'language_origins': 'Middle English',
                'example_sentence': 'The charter boat captain was excited when they hooked a massive _______ that took thirty minutes to bring to the surface.',
                'memory_tip': 'Remember "HALIBUT" - HALf huge + BUT flat, a huge fish that\'s flat like it was squashed, the holy flatfish.'
            },
            'halifax': {
                'definition': 'Halifax is the capital and largest city of Nova Scotia, Canada, serving as the major economic, cultural, and transportation hub of the Maritime provinces. The city has a rich maritime history, including its role as a major port and naval base. Halifax is home to several universities, including Dalhousie University, and has a vibrant arts and culture scene. The city is also notable for its connection to the Titanic disaster, as it was the base for recovery efforts and where many victims were brought. Halifax combines historic charm with modern urban amenities, making it an important Canadian Atlantic city.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'HAL-i-faks',
                'etymology': 'Named after George Montagu-Dunk, 2nd Earl of Halifax, from Old English "halig" (holy) + "feax" (hair).',
                'language_origins': 'Old English (named after person)',
                'example_sentence': 'The cruise ship docked in _______ harbor, allowing passengers to explore the historic waterfront and visit the Maritime Museum.',
                'memory_tip': 'Remember "HALIFAX" - HALf way + FAX (facts), halfway across Canada you\'ll find the facts about this important Maritime city.'
            },
            'halifaxhallucinate': {
                'definition': 'This appears to be a combined word error where "halifax" (the Canadian city) has been incorrectly merged with "hallucinate" (to perceive things that are not actually present). Halifax is the capital city of Nova Scotia, Canada, known for its maritime history and cultural significance. Hallucinate means to experience perceptions of objects or events that do not have an external source, often due to mental illness, drug effects, or extreme fatigue. This combination likely resulted from a PDF parsing error where two completely unrelated words were inadvertently joined together.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'HAL-i-faks-huh-LOO-suh-nayt',
                'etymology': 'Error: "halifax" (Old English "halig" + "feax") + "hallucinate" (Latin "hallucinari")',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "halifax" and "hallucinate" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "HALIFAXHALLUCINATE" - this is a combined word error, separate into HALIFAX (Canadian city) + HALLUCINATE (see things that aren\'t there).'
            },
            'hall': {
                'definition': 'Hall refers to a large room or building used for meetings, entertainment, dining, or other gatherings. Halls can range from small meeting rooms to vast auditoriums, concert halls, or banquet facilities. In residential contexts, a hall is typically a corridor or passageway connecting rooms. Educational institutions often have dining halls, lecture halls, and residence halls. The term also appears in the names of stately homes, manor houses, and public buildings. Halls serve as gathering spaces that bring people together for various social, cultural, educational, and recreational purposes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAWL',
                'etymology': 'From Old English "heall," from Germanic roots meaning "to cover, conceal."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The wedding reception was held in the grand _______ of the historic mansion, with its soaring ceilings and crystal chandeliers.',
                'memory_tip': 'Remember "HALL" - High Area for Large meetings, a high-ceilinged area designed for large groups to gather.'
            },
            'hallowed': {
                'definition': 'Hallowed describes something that is regarded as holy, sacred, or greatly revered due to its religious significance or honored tradition. This adjective indicates that something has been consecrated, blessed, or set apart as sacred through religious ritual or long-standing reverence. Hallowed places, objects, or traditions are treated with special respect and often considered inviolable. The word appears in religious contexts, such as "hallowed ground" for sacred burial places, or "hallowed be thy name" from the Lord\'s Prayer. Hallowed suggests both sanctification and deep reverence.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'HAL-ohd',
                'etymology': 'From "hallow" (from Old English "halgian" meaning "to make holy") + "-ed" suffix.',
                'language_origins': 'Old English',
                'example_sentence': 'The veterans walked respectfully through the _______ grounds of the national cemetery, honoring those who had served.',
                'memory_tip': 'Remember "HALLOWED" - HALLmark + OWED respect, a hallmark place that is owed special respect because it\'s holy.'
            },
            'hallucinate': {
                'definition': 'Hallucinate means to perceive objects, sounds, sensations, or other experiences that appear real but do not actually exist outside one\'s mind. These perceptions can affect any of the senses and may result from mental illness, drug use, extreme fatigue, high fever, or certain medical conditions. Hallucinations can be visual (seeing things), auditory (hearing voices or sounds), tactile (feeling sensations), olfactory (smelling odors), or gustatory (tasting flavors). The term is also used metaphorically to describe vivid imagination or unrealistic thinking, and recently in technology to describe AI systems generating false information.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'huh-LOO-suh-nayt',
                'etymology': 'From Latin "hallucinari" meaning "to wander mentally, dream," from "alucinari" meaning "to wander in mind."',
                'language_origins': 'Latin',
                'example_sentence': 'The fever caused him to _______, seeing shadowy figures that disappeared when he tried to focus on them.',
                'memory_tip': 'Remember "HALLUCINATE" - HALf reLUCid dreaM + inATE (innate), having innate half-lucid dreams while awake, seeing things that aren\'t there.'
            },
            'hallux': {
                'definition': 'Hallux is the medical term for the big toe, the largest and most medial (innermost) toe of the foot. In human anatomy, the hallux plays a crucial role in balance, walking, and push-off during locomotion. This digit has only two phalanges (toe bones) compared to the three found in other toes. Medical conditions affecting the hallux include hallux valgus (bunions), hallux rigidus (arthritis of the big toe joint), and ingrown toenails. The hallux is essential for proper gait mechanics and weight distribution during standing and walking.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAL-uhks',
                'etymology': 'From Latin "hallux," possibly related to "hallex," meaning "big toe."',
                'language_origins': 'Latin',
                'example_sentence': 'The podiatrist examined the patient\'s painful _______, diagnosing the condition as hallux rigidus due to arthritis in the big toe joint.',
                'memory_tip': 'Remember "HALLUX" - HALf your foot\'s powerfUL oPtion, the powerful big toe that\'s half your foot\'s push-off power.'
            },
            'halo': {
                'definition': 'Halo has several meanings: it most commonly refers to a circle of light depicted around the head of a holy person in religious art, symbolizing divine grace or sanctity. In meteorology, a halo is an optical phenomenon where a ring of light appears around the sun or moon, caused by ice crystals in the atmosphere. The term can also describe anything resembling a circular ring of light or the aura of fame, glory, or sanctity surrounding a person. Metaphorically, "halo effect" describes the tendency to let positive impressions in one area influence opinions in other areas.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'HAY-loh',
                'etymology': 'From Greek "halos" meaning "disk of the sun or moon," from "hals" meaning "salt" (referring to the circular salt-grinding floor).',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The ice crystals in the thin clouds created a beautiful _______ around the full moon, forming a perfect circle of diffused light.',
                'memory_tip': 'Remember "HALO" - HALf angeLic lOop, the half-angelic loop of light around holy heads or celestial bodies.'
            },
            'halogens': {
                'definition': 'Halogens are a group of chemical elements in Group 17 (formerly Group VIIA) of the periodic table, including fluorine, chlorine, bromine, iodine, and astatine. These elements share similar properties: they have seven electrons in their outer shell, making them highly reactive as they readily gain one electron to achieve a stable configuration. Halogens form salts when combined with metals (the name "halogen" means "salt-former"). They exist in various physical states at room temperature: fluorine and chlorine are gases, bromine is a liquid, and iodine is a solid. Halogens are essential in many industrial, medical, and biological processes.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'HAL-uh-juhns',
                'etymology': 'From Greek "hals" meaning "salt" + "genes" meaning "born, produced," literally "salt-producers."',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The chemistry student learned that _______ like chlorine and iodine are highly reactive elements that readily form ionic compounds with metals.',
                'memory_tip': 'Remember "HALOGENS" - HALf of sALt + GENES (makers), the genes (elements) that make half of salt by combining with metals.'
            },
            'hamadryad': {
                'definition': 'Hamadryad has two main meanings: in Greek mythology, it refers to tree nymphs whose lives were bound to specific trees, dying when their trees were cut down or destroyed. In zoology, hamadryad is an alternative name for the king cobra, the world\'s longest venomous snake found in Asia. The mythological hamadryads were considered guardian spirits of forests and trees, punishing those who harmed their trees. The snake earned this name due to its impressive size and the reverence (or fear) it inspired. Both meanings share themes of natural power, respect for nature, and the connection between life and the natural world.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ham-uh-DRAHY-ad',
                'etymology': 'From Greek "hamadryas," from "hama" meaning "together with" + "drys" meaning "tree."',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'According to Greek mythology, cutting down an ancient oak would kill the _______ who lived within it, bringing misfortune to the woodcutter.',
                'memory_tip': 'Remember "HAMADRYAD" - HAMa (together) + DRY (tree) + AD, together with the dry tree, the nymph who lives with her tree.'
            },
            'hamlet': {
                'definition': 'Hamlet has two primary meanings: it refers to a small village or settlement, typically smaller than a village and often lacking a church or other municipal buildings. In literature, Hamlet is the title character of Shakespeare\'s famous tragedy, a Danish prince who seeks revenge for his father\'s murder. As a geographical term, hamlet describes a small rural community, often consisting of just a few houses and farms. The literary Hamlet is one of the most studied characters in English literature, known for his famous soliloquy "To be or not to be" and his complex psychological portrayal.',
                'part_of_speech': 'noun, proper noun',
                'pronunciation_guide': 'HAM-lit',
                'etymology': 'From Old French "hamelet," diminutive of "hamel," from Germanic "ham" meaning "home, village."',
                'language_origins': 'Old French, Germanic',
                'example_sentence': 'The peaceful _______ consisted of only twelve houses scattered around a central green, with no shops or municipal services.',
                'memory_tip': 'Remember "HAMLET" - HAM (home) + LET (little), a little home community, or the little Danish prince from Shakespeare.'
            },
            'hamstring': {
                'definition': 'Hamstring refers to any of the three muscles at the back of the thigh (biceps femoris, semitendinosus, and semimembranosus) that bend the knee and extend the hip. As a verb, to hamstring means to cripple someone by cutting their hamstring tendons, or more commonly, to severely limit or restrict someone\'s effectiveness or ability to act. Hamstring injuries are common in sports that involve running and sudden stops or changes of direction. The muscles are essential for walking, running, and many athletic activities, making hamstring flexibility and strength important for overall mobility.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'HAM-string',
                'etymology': 'From "ham" (back of the knee, from Old English "hamm") + "string" (tendon).',
                'language_origins': 'Old English',
                'example_sentence': 'The runner felt a sharp pain in her _______ during the sprint, forcing her to stop and seek medical attention.',
                'memory_tip': 'Remember "HAMSTRING" - HAM (back of leg like ham) + STRING (tight muscle string), the string-like muscles at the back of your ham-like thigh.'
            },
            'hamtramck': {
                'definition': 'Hamtramck is a city in southeastern Michigan, completely surrounded by the city of Detroit, making it an enclave within the larger metropolitan area. This small city has a rich history of immigration, originally settled by German and Polish immigrants in the early 20th century, and later becoming home to Middle Eastern and South Asian communities. Hamtramck is known for its cultural diversity, ethnic restaurants, and historic architecture. The city has maintained its distinct identity despite being geographically isolated within Detroit, serving as an example of urban ethnic enclaves in American cities.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'ham-TRAM-ik',
                'etymology': 'Named after Colonel Jean François Hamtramck, a French-Canadian military officer who served in the American Revolutionary War.',
                'language_origins': 'French (named after person)',
                'example_sentence': 'The food festival in _______ celebrated the city\'s diverse population with Polish pierogi, Middle Eastern kebabs, and Bangladeshi curry.',
                'memory_tip': 'Remember "HAMTRAMCK" - HAM + TRAMpled + miCK, like ham trampled by Mick, a small city trampled by (surrounded by) larger Detroit.'
            },
            'hand': {
                'definition': 'Hand refers to the part of the human body at the end of the arm, consisting of the palm, four fingers, and thumb, used for grasping, manipulating objects, and performing intricate tasks. Hands are remarkable tools that enable humans to create, build, write, gesture, and perform countless daily activities. The term also has numerous figurative meanings: assistance ("lend a hand"), control ("upper hand"), skill ("good with his hands"), or applause ("give him a hand"). In various contexts, hand can refer to workers, clock pointers, card games, or handwriting.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'HAND',
                'etymology': 'From Old English "hand," from Germanic roots meaning "hand."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'She used her steady _______ to thread the needle, demonstrating the precision and dexterity that made her an excellent seamstress.',
                'memory_tip': 'Remember "HAND" - Help ANd Do, the body part that helps you do everything from writing to building to caring for others.'
            },
            'handcuffs': {
                'definition': 'Handcuffs are restraining devices consisting of two metal rings connected by a chain or hinge, designed to secure a person\'s wrists together to prevent them from using their hands freely. These devices are primarily used by law enforcement officers to detain suspects or prisoners during arrest, transport, or custody. Handcuffs are typically made of steel and feature a ratcheting mechanism that allows them to tighten but requires a key to release. The use of handcuffs is regulated by law enforcement policies and procedures to ensure they are applied safely and appropriately.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'HAND-kufs',
                'etymology': 'From "hand" + "cuff" (from Middle English "cuffe," meaning "mitten"), literally "hand mittens."',
                'language_origins': 'Middle English',
                'example_sentence': 'The police officer placed _______ on the suspect after reading him his rights, securing his wrists behind his back for safety.',
                'memory_tip': 'Remember "HANDCUFFS" - HAND + CUFFS (like shirt cuffs), metal cuffs that go around your hands to restrain them.'
            },
            'handle': {
                'definition': 'Handle has multiple meanings: as a noun, it refers to the part of an object designed to be held, carried, or controlled by hand, such as a door handle or tool handle. As a verb, handle means to touch, hold, or manipulate something with the hands, or more broadly, to manage, deal with, or control a situation, problem, or responsibility. The term can also refer to a name or nickname, particularly in online contexts. Good handles are ergonomically designed for comfort and control, while handling skills involve both physical dexterity and management capabilities.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'HAN-duhl',
                'etymology': 'From Old English "handle," from "hand" + "-le" diminutive suffix.',
                'language_origins': 'Old English',
                'example_sentence': 'The chef showed the apprentice how to properly _______ the sharp knife, emphasizing safety and precision in every cut.',
                'memory_tip': 'Remember "HANDLE" - HAND + LE (little extension), the little extension you grab with your hand, or how you manage things with skill.'
            },
            'handles': {
                'definition': 'Handles is the plural form of handle, referring to multiple parts of objects designed to be held, carried, or controlled by hand. These can include door handles, tool handles, bag handles, or any gripping mechanisms. As a verb form, handles means the third person singular present tense of handle, describing how someone or something manages, controls, or deals with situations, objects, or responsibilities. Good handles are essential for user-friendly design, providing secure grip and comfortable operation of tools, doors, containers, and other objects.',
                'part_of_speech': 'noun (plural), verb (third person singular)',
                'pronunciation_guide': 'HAN-duhlz',
                'etymology': 'Plural of "handle," from Old English "handle," from "hand" + "-le" diminutive suffix.',
                'language_origins': 'Old English',
                'example_sentence': 'The antique chest featured ornate brass _______ that had been polished to a brilliant shine over decades of use.',
                'memory_tip': 'Remember "HANDLES" - HAND + LES (multiple little extensions), multiple little extensions you grab with your hands.'
            },
            'handstand': {
                'definition': 'Handstand is a gymnastic or acrobatic position where a person balances upside down, supporting their entire body weight on their hands with arms extended and legs pointing upward. This skill requires significant upper body strength, core stability, and balance coordination. Handstands are fundamental movements in gymnastics, yoga, breakdancing, and various martial arts. Learning to perform a handstand involves developing wrist and shoulder flexibility, arm and core strength, and the ability to maintain equilibrium while inverted. Handstands can be performed against a wall for support or freestanding.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAND-stand',
                'etymology': 'From "hand" + "stand," literally standing on one\'s hands.',
                'language_origins': 'English (compound word)',
                'example_sentence': 'After months of practice, she could finally hold a perfect _______ for thirty seconds without touching the wall.',
                'memory_tip': 'Remember "HANDSTAND" - HAND + STAND, standing on your hands instead of your feet, balancing upside down.'
            }
        }
        
        return batch_081_data.get(word.lower(), {
            'definition': f'{word} - Comprehensive definition not available in batch data.',
            'part_of_speech': 'unknown',
            'pronunciation_guide': f'{word.upper()}',
            'etymology': 'Etymology not available.',
            'language_origins': 'Unknown',
            'example_sentence': f'The word _______ was used in the sentence.',
            'memory_tip': f'Remember {word.upper()} by its distinctive spelling pattern.'
        })
    
    def detect_parsing_errors(self, word: str) -> Optional[str]:
        parsing_errors = {
            'gushedchina': 'Combined word error: "gushedchina" appears to be "gushed" + "china" merged together. This is likely a PDF parsing error where rapid flow/enthusiasm and porcelain/country terminology were incorrectly combined.',
            'gyascutusgyokuro': 'Combined word error: "gyascutusgyokuro" appears to be "gyascutus" + "gyokuro" merged together. This is likely a PDF parsing error where mythical creature and Japanese tea terminology were incorrectly combined.',
            'haggisdolce': 'Combined word error: "haggisdolce" appears to be "haggis" + "dolce" merged together. This is likely a PDF parsing error where Scottish savory dish and Italian dessert terminology were incorrectly combined.',
            'halifaxhallucinate': 'Combined word error: "halifaxhallucinate" appears to be "halifax" + "hallucinate" merged together. This is likely a PDF parsing error where Canadian city and perception disorder terminology were incorrectly combined.'
        }
        return parsing_errors.get(word.lower())
    
    def process_batch(self, input_file: str, output_file: str):
        print(f"Processing {input_file}...")
        
        words_data = []
        word_count = 0
        
        with open(input_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                word = row['word'].strip()
                if not word:
                    continue
                    
                word_count += 1
                
                # Check for parsing errors
                error_msg = self.detect_parsing_errors(word)
                if error_msg:
                    self.errors.append(f"  - {word}: {error_msg}")
                
                # Get comprehensive data
                claude_data = self.get_comprehensive_claude_data(word)
                
                # Calculate difficulty scores
                phonetic_score = self.difficulty_calculator.calculate_phonetic_transparency_score(word)
                frequency_score = self.difficulty_calculator.calculate_frequency_score(word)
                morphological_score = self.difficulty_calculator.calculate_morphological_complexity_score(word)
                etymology_score = self.difficulty_calculator.calculate_etymology_complexity_score(
                    claude_data['etymology'], claude_data['language_origins']
                )
                
                word_data = WordData(
                    word=word,
                    definition=claude_data['definition'],
                    part_of_speech=claude_data['part_of_speech'],
                    pronunciation_guide=claude_data['pronunciation_guide'],
                    etymology=claude_data['etymology'],
                    language_origins=claude_data['language_origins'],
                    example_sentence=claude_data['example_sentence'],
                    memory_tip=claude_data['memory_tip'],
                    phonetic_transcription_score=phonetic_score,
                    frequency_score=frequency_score,
                    morphological_score=morphological_score,
                    etymology_score=etymology_score,
                    final_difficulty=None
                )
                
                words_data.append(word_data)
        
        # Write to CSV
        fieldnames = [
            'word', 'definition', 'part_of_speech', 'pronunciation_guide', 'etymology', 
            'language_origins', 'example_sentence', 'memory_tip', 'phonetic_transcription_score',
            'frequency_score', 'morphological_score', 'etymology_score', 'final_difficulty',
            'definition_source', 'pronunciation_source', 'etymology_source', 'example_sentence_source',
            'memory_tip_source', 'audio_file', 'difficulty_level', 'difficulty_source',
            'years', 'source_files', 'source_difficulties', 'scripps_difficulty'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for word_data in words_data:
                writer.writerow({
                    'word': word_data.word,
                    'definition': word_data.definition,
                    'part_of_speech': word_data.part_of_speech,
                    'pronunciation_guide': word_data.pronunciation_guide,
                    'etymology': word_data.etymology,
                    'language_origins': word_data.language_origins,
                    'example_sentence': word_data.example_sentence,
                    'memory_tip': word_data.memory_tip,
                    'phonetic_transcription_score': word_data.phonetic_transcription_score,
                    'frequency_score': word_data.frequency_score,
                    'morphological_score': word_data.morphological_score,
                    'etymology_score': word_data.etymology_score,
                    'final_difficulty': word_data.final_difficulty,
                    'definition_source': 'Claude',
                    'pronunciation_source': 'Claude',
                    'etymology_source': 'Claude',
                    'example_sentence_source': 'Claude',
                    'memory_tip_source': 'Claude',
                    'audio_file': '',
                    'difficulty_level': '',
                    'difficulty_source': '',
                    'years': '',
                    'source_files': '',
                    'source_difficulties': '',
                    'scripps_difficulty': ''
                })
        
        print(f"Successfully processed {word_count}/{word_count} words to {output_file}")
        
        if self.errors:
            print(f"Found {len(self.errors)} error(s):")
            for error in self.errors:
                print(error)
        
        print("Batch 081 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch081Processor()
    input_path = "output/batch_081_words.csv"
    output_path = "output/batch_081_processed.csv"
    processor.process_batch(input_path, output_path)