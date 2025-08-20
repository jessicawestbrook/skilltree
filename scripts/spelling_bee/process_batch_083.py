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

class Batch083Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
        self.errors = []
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        batch_083_data = {
            'hawsers': {
                'definition': 'Hawsers are heavy ropes or cables used on ships for mooring, towing, or anchoring vessels. These thick, strong lines are essential maritime equipment that can withstand tremendous stress and strain from wind, waves, and the weight of large ships. Hawsers are typically made from natural fibers like hemp or manila, or modern synthetic materials like nylon or polyester that offer superior strength and weather resistance. The size and construction of hawsers vary depending on the vessel size and intended use, with larger ships requiring proportionally stronger and thicker hawsers for safe operations in harbors and at sea.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'HAW-zers',
                'etymology': 'From Old French "haucier" meaning "to hoist," from Germanic roots meaning "to lift."',
                'language_origins': 'Old French, Germanic',
                'example_sentence': 'The dock workers secured the massive cargo ship to the pier using thick _______ that could handle the vessel\'s weight and the pull of the tide.',
                'memory_tip': 'Remember "HAWSERS" - HAWl + SeRS (sailors), sailors use these to haul and secure their ships with heavy ropes.'
            },
            'hazardous': {
                'definition': 'Hazardous describes something that involves danger, risk, or the potential to cause harm, injury, or damage to people, property, or the environment. This adjective applies to substances, activities, conditions, or situations that pose significant threats requiring special precautions, safety measures, or protective equipment. Hazardous materials include chemicals, radioactive substances, or biological agents that can cause illness or environmental damage. The term encompasses both immediate dangers and long-term risks that may not be immediately apparent but can cause serious consequences over time.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'HAZ-er-duhs',
                'etymology': 'From "hazard" (from Old French "hasard") + "-ous" suffix meaning "full of" or "characterized by."',
                'language_origins': 'Old French',
                'example_sentence': 'The laboratory workers wore protective suits when handling _______ chemicals that could cause serious health problems if inhaled.',
                'memory_tip': 'Remember "HAZARDOUS" - HAZARD + OUS (full of), full of hazards and dangers that require extreme caution.'
            },
            'hazelnut': {
                'definition': 'Hazelnut is the edible nut of the hazel tree (Corylus species), characterized by a hard brown shell enclosing a sweet, oily kernel. These nuts are popular in cooking, baking, and confectionery, often used in chocolates, cookies, spreads, and desserts. Hazelnuts are rich in healthy fats, protein, vitamins, and minerals, making them nutritionally valuable. They grow in temperate regions around the world and are commercially cultivated for food production. The nuts can be eaten raw, roasted, or processed into oils, flours, and other food products.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAY-zul-nuht',
                'etymology': 'From Old English "hæsel" (hazel tree) + "hnutu" (nut).',
                'language_origins': 'Old English',
                'example_sentence': 'The baker crushed roasted _______ to sprinkle over the chocolate cake, adding a rich, nutty flavor and crunchy texture.',
                'memory_tip': 'Remember "HAZELNUT" - HAZEL tree + NUT, the delicious nut that grows on hazel trees and goes great with chocolate.'
            },
            'hazmat': {
                'definition': 'Hazmat is an abbreviation for "hazardous materials," referring to substances that pose risks to health, safety, property, or the environment during transportation, handling, or storage. This term encompasses chemicals, radioactive materials, biological agents, and other dangerous substances that require special handling procedures, protective equipment, and regulatory compliance. Hazmat teams are specially trained emergency responders who deal with spills, leaks, or accidents involving dangerous materials. The classification helps ensure proper safety protocols and legal compliance when dealing with potentially harmful substances.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'HAZ-mat',
                'etymology': 'Abbreviation of "hazardous materials," from "hazard" (Old French) + "material" (Latin "materialis").',
                'language_origins': 'Modern English abbreviation',
                'example_sentence': 'The _______ team arrived in protective suits to clean up the chemical spill that had occurred during the truck accident.',
                'memory_tip': 'Remember "HAZMAT" - HAZardous MATerials, the dangerous materials that require special handling and safety equipment.'
            },
            'head': {
                'definition': 'Head has numerous meanings: anatomically, it refers to the uppermost part of the human body containing the brain, eyes, ears, nose, and mouth. As a leader, head describes the person in charge of an organization, department, or group. Head can mean the front, top, or most important part of something, such as the head of a line or head of a table. In various contexts, head refers to individual units (head of cattle), pressure in fluids, foam on beer, or the striking part of tools. The word is fundamental across many areas of language and life.',
                'part_of_speech': 'noun, verb, adjective',
                'pronunciation_guide': 'HED',
                'etymology': 'From Old English "hēafod," from Germanic roots meaning "head, top."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'She nodded her _______ in agreement before stepping forward to address the crowd as the newly appointed team leader.',
                'memory_tip': 'Remember "HEAD" - Highest part of Everything And Decision-making center, the highest part of your body where decisions are made.'
            },
            'headdress': {
                'definition': 'Headdress is an ornamental covering or decoration worn on the head, often signifying cultural identity, religious beliefs, social status, or ceremonial importance. These elaborate head coverings can include feathers, beads, shells, precious metals, fabrics, or other decorative materials arranged in culturally specific patterns. Headdresses appear in many cultures worldwide, from Native American war bonnets to African ceremonial crowns to medieval European court fashion. They serve both aesthetic and symbolic purposes, often representing spiritual beliefs, tribal membership, achievements, or social ranking within communities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HED-dres',
                'etymology': 'From "head" (Old English "hēafod") + "dress" (Old French "dresser").',
                'language_origins': 'Old English, Old French',
                'example_sentence': 'The tribal chief wore an elaborate _______ of eagle feathers and turquoise beads during the sacred ceremony.',
                'memory_tip': 'Remember "HEADDRESS" - HEAD + DRESS, a dress or decoration for your head worn for special occasions and cultural significance.'
            },
            'headlong': {
                'definition': 'Headlong describes movement or action that is hasty, reckless, or done without careful thought, literally meaning "head first" but often implying dangerous speed or impulsiveness. As an adverb, headlong describes how something is done in a rushed, precipitous manner without proper consideration of consequences. The word can describe physical movement (diving headlong into water) or abstract actions (rushing headlong into decisions). Headlong suggests both literal forward momentum with the head leading and figurative rash behavior that lacks caution or planning.',
                'part_of_speech': 'adverb, adjective',
                'pronunciation_guide': 'HED-lawng',
                'etymology': 'From "head" (Old English "hēafod") + "long" (meaning "along"), literally "head along."',
                'language_origins': 'Old English',
                'example_sentence': 'He rushed _______ into the business venture without researching the market, later regretting his impulsive decision.',
                'memory_tip': 'Remember "HEADLONG" - HEAD + LONG (along), going head-along in a rush without stopping to think carefully.'
            },
            'headquartered': {
                'definition': 'Headquartered describes an organization, company, or institution that has established its main office, administrative center, or primary base of operations in a particular location. This verb indicates where the central command, executive leadership, and primary decision-making activities of an organization are located. Being headquartered in a location often implies significant economic, legal, and operational ties to that area. The headquarters typically serves as the nerve center from which the organization\'s activities are directed and coordinated across various locations or regions.',
                'part_of_speech': 'verb (past tense/past participle), adjective',
                'pronunciation_guide': 'HED-kwar-terd',
                'etymology': 'From "headquarters" (head + quarters meaning "lodgings") + "-ed" past tense suffix.',
                'language_origins': 'English',
                'example_sentence': 'The multinational corporation is _______ in Geneva, Switzerland, though it operates offices in over fifty countries worldwide.',
                'memory_tip': 'Remember "HEADQUARTERED" - HEAD + QUARTERED, where the head office is quartered or located as the main base.'
            },
            'health': {
                'definition': 'Health refers to the state of being free from illness or injury, encompassing physical, mental, and social well-being rather than merely the absence of disease. This concept includes optimal functioning of body systems, emotional stability, cognitive clarity, and positive social relationships. Health is influenced by genetics, lifestyle choices, environment, healthcare access, and social determinants. It exists on a continuum from optimal wellness to severe illness, with most people experiencing varying degrees of health throughout their lives. Modern understanding of health emphasizes prevention, holistic care, and quality of life.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HELTH',
                'etymology': 'From Old English "hǣlth," from "hāl" meaning "whole, sound, healthy."',
                'language_origins': 'Old English',
                'example_sentence': 'Regular exercise, balanced nutrition, and adequate sleep are fundamental pillars of good _______ throughout one\'s lifetime.',
                'memory_tip': 'Remember "HEALTH" - HEaLing + THriving, the state of healing and thriving in body, mind, and spirit.'
            },
            'hear': {
                'definition': 'Hear means to perceive sounds through the auditory system, involving the ears, auditory nerves, and brain working together to process sound waves into meaningful information. Beyond physical hearing, the word can mean to listen to someone with attention, to receive news or information, or to consider someone\'s case or argument formally. Hearing involves both the mechanical process of sound detection and the cognitive process of understanding and interpreting what is heard. The ability to hear is crucial for communication, safety, learning, and social interaction.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'HEER',
                'etymology': 'From Old English "hīeran," from Germanic roots meaning "to hear, listen."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'She could _______ the distant thunder rumbling across the valley, warning of an approaching storm.',
                'memory_tip': 'Remember "HEAR" - Head Ears Always Receiving, your head\'s ears are always receiving and processing sounds from the environment.'
            },
            'heard': {
                'definition': 'Heard is the past tense and past participle of the verb "hear," indicating that the action of perceiving sound occurred in the past or has been completed. This form describes sounds that were previously detected by the auditory system, information that was received, or cases that were listened to and considered. Heard can refer to actual auditory perception, receiving news or communication, or formal consideration of arguments or evidence. The word indicates completed auditory experience or communication that took place at a previous time.',
                'part_of_speech': 'verb (past tense/past participle)',
                'pronunciation_guide': 'HURD',
                'etymology': 'Past tense of "hear," from Old English "hīerde," from Germanic roots.',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'She _______ her name called from across the crowded room and turned to see who was trying to get her attention.',
                'memory_tip': 'Remember "HEARD" - HEard in the pAst, what you heard in the past using your ears and brain.'
            },
            'heartthrob': {
                'definition': 'Heartthrob refers to a person, typically a celebrity or public figure, who is widely considered attractive and causes romantic excitement or infatuation, especially among fans or admirers. This term suggests someone whose appeal is so strong that they literally make hearts "throb" or beat faster with romantic interest. Heartthrobs often include actors, musicians, or other entertainers who become objects of widespread admiration and romantic fantasy. The term can also describe the physical sensation of a rapid or strong heartbeat caused by excitement, anxiety, or romantic attraction.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAHRT-throb',
                'etymology': 'From "heart" (Old English "heorte") + "throb" (imitative), literally "heart beating fast."',
                'language_origins': 'Old English (compound)',
                'example_sentence': 'The young actor became a teen _______ after starring in the romantic movie that broke box office records.',
                'memory_tip': 'Remember "HEARTTHROB" - HEART + THROB, someone who makes your heart throb with excitement and romantic attraction.'
            },
            'heavenly': {
                'definition': 'Heavenly describes something that relates to heaven or the divine realm, or more commonly, something that is extremely pleasant, delightful, or perfect in quality. In religious contexts, heavenly refers to celestial, spiritual, or divine attributes associated with paradise or the afterlife. In everyday usage, heavenly describes experiences, foods, sensations, or objects that are so wonderful they seem divine or perfect. The word suggests the highest degree of pleasure, beauty, or satisfaction, often used to express enthusiastic approval or amazement at something\'s exceptional quality.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'HEV-uhn-lee',
                'etymology': 'From Old English "heofenlic," from "heofon" (heaven) + "-lic" suffix meaning "like."',
                'language_origins': 'Old English',
                'example_sentence': 'The chocolate cake had such a _______ taste that everyone at the dinner party asked for the recipe.',
                'memory_tip': 'Remember "HEAVENLY" - HEAVEN + LY (like), like heaven - so perfect and delightful it seems divine.'
            },
            'heavenlyheiress': {
                'definition': 'This appears to be a combined word error where "heavenly" (divine or extremely pleasant) has been incorrectly merged with "heiress" (a female heir to wealth or property). Heavenly describes something that is divine, celestial, or extremely delightful in quality, while heiress refers to a woman who inherits or is entitled to inherit wealth, property, or a title from family members. This combination likely resulted from a PDF parsing error where two separate words were inadvertently joined together. The correct terms would be "heavenly" referring to divine or perfect qualities, and "heiress" referring to a female heir.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'HEV-uhn-lee-AIR-is',
                'etymology': 'Error: "heavenly" (Old English "heofenlic") + "heiress" (Old French "heir" + feminine suffix)',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "heavenly" and "heiress" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "HEAVENLYHEIRESS" - this is a combined word error, separate into HEAVENLY (divine/perfect) + HEIRESS (female heir).'
            },
            'heavy': {
                'definition': 'Heavy describes something that has great weight, making it difficult to lift, move, or carry due to its mass or density. The word can also describe intensity, severity, or abundance in various contexts: heavy rain, heavy traffic, or heavy responsibilities. Heavy can refer to emotional weight (heavy heart), serious or profound matters (heavy topics), or things that are oppressive or burdensome. In different contexts, heavy might describe thick consistency, strong force, or significant impact. The concept encompasses both literal physical weight and figurative emotional or situational weight.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'HEV-ee',
                'etymology': 'From Old English "hefig," from Germanic roots meaning "weight, heaviness."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The _______ suitcase required two people to lift it into the car trunk before their long vacation trip.',
                'memory_tip': 'Remember "HEAVY" - HEaVy + Y (why so hard), why so hard to lift - because it has great weight and mass.'
            },
            'hebdomadal': {
                'definition': 'Hebdomadal means occurring weekly or relating to a period of seven days. This formal, somewhat archaic adjective derives from the concept of a seven-day cycle and is used primarily in academic, religious, or formal contexts to describe regular weekly occurrences or schedules. The term appears in institutional settings like universities, where "hebdomadal councils" might meet weekly, or in religious contexts referring to weekly observances. While "weekly" is more commonly used in everyday language, hebdomadal provides a more scholarly or formal alternative for describing seven-day cycles.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'heb-DOM-uh-dl',
                'etymology': 'From Greek "hebdomas" meaning "seven" + Latin "-alis" suffix meaning "relating to."',
                'language_origins': 'Ancient Greek, Latin',
                'example_sentence': 'The university\'s _______ council met every Tuesday to discuss academic policies and administrative matters.',
                'memory_tip': 'Remember "HEBDOMADAL" - HEBdo (seven) + MAD + AL (relating to), relating to the "mad" busy cycle of seven days each week.'
            },
            'hebrides': {
                'definition': 'Hebrides refers to a group of islands off the western coast of Scotland, divided into the Inner Hebrides and Outer Hebrides. These Scottish islands are known for their rugged landscapes, Celtic culture, Gaelic language traditions, and maritime heritage. The Hebrides include well-known islands like Skye, Mull, Islay, and Lewis and Harris, each with distinct characteristics and cultural significance. The islands have played important roles in Scottish history, serving as strongholds of Gaelic culture and featuring prominently in Scottish literature, music, and folklore. They are popular destinations for tourists seeking natural beauty and Celtic heritage.',
                'part_of_speech': 'proper noun (plural)',
                'pronunciation_guide': 'HEB-ri-deez',
                'etymology': 'From Latin "Hebrides," possibly from Celtic roots meaning "islands of the edges" or similar.',
                'language_origins': 'Latin, Celtic',
                'example_sentence': 'The photographer captured stunning images of the rugged coastline and ancient castles scattered throughout the _______ during her month-long journey.',
                'memory_tip': 'Remember "HEBRIDES" - HEB (like web) + RIDES, a web of islands where you can take boat rides around the Scottish coast.'
            },
            'hedgehog': {
                'definition': 'Hedgehog is a small, spiny mammal found in Europe, Asia, and Africa, characterized by a coat of stiff spines that serve as protection from predators. These insectivorous animals can roll into a defensive ball when threatened, presenting only their sharp spines to attackers. Hedgehogs are nocturnal creatures that feed primarily on insects, worms, and other small invertebrates, making them beneficial for controlling garden pests. Some species are kept as exotic pets, though they require specialized care. The animal\'s distinctive appearance and defensive behavior have made it a popular subject in literature and folklore.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HEJ-hawg',
                'etymology': 'From "hedge" (Old English "hecg") + "hog" (Old English "hogg"), referring to its habitat and pig-like snout.',
                'language_origins': 'Old English',
                'example_sentence': 'The garden _______ emerged at dusk to hunt for insects and slugs among the flower beds.',
                'memory_tip': 'Remember "HEDGEHOG" - HEDGE + HOG, a hog-like animal that lives in hedges and rolls into a spiny ball for protection.'
            },
            'hegemony': {
                'definition': 'Hegemony refers to the dominance or leadership of one group, nation, or entity over others, particularly in political, economic, or cultural spheres. This concept describes not just power but influence that shapes how others think and act, often achieved through consent rather than force alone. Hegemony can manifest as cultural dominance where one group\'s values and practices become the accepted norm, or political hegemony where one nation exercises significant influence over international affairs. The term suggests subtle but pervasive control that extends beyond mere military or economic power to include ideological influence.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hi-JEM-uh-nee',
                'etymology': 'From Greek "hegemon" meaning "leader," from "hegeisthai" meaning "to lead."',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The cultural _______ of Hollywood films has spread American values and entertainment styles worldwide.',
                'memory_tip': 'Remember "HEGEMONY" - HEGEmon (leader) + ONY (only), when only one leader dominates and influences everyone else.'
            },
            'hegirae': {
                'definition': 'Hegirae is the plural form of hegira, referring to multiple journeys or migrations undertaken to escape danger or seek better conditions, particularly those with historical or religious significance. The original Hegira refers to Prophet Muhammad\'s migration from Mecca to Medina in 622 CE, which marks the beginning of the Islamic calendar. By extension, hegirae can describe any significant migrations or journeys made by groups seeking refuge, freedom, or new opportunities. The term emphasizes the historical importance and often desperate circumstances that prompt such mass movements of people.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'hi-JAHY-ree',
                'etymology': 'Plural of "hegira," from Arabic "hijra" meaning "emigration, departure."',
                'language_origins': 'Arabic',
                'example_sentence': 'Historical scholars studied various _______ throughout history, including religious migrations and refugee movements seeking safety.',
                'memory_tip': 'Remember "HEGIRAE" - HE (they) + GIRA (journey) + E (multiple), multiple journeys that groups of people take to escape danger.'
            },
            'hegiraeanomaliped': {
                'definition': 'This appears to be a combined word error where "hegirae" (plural of hegira, meaning migrations or journeys) has been incorrectly merged with "anomaliped" (an unusual or abnormal foot). Hegirae refers to significant migrations or journeys, particularly those with religious or historical importance like the Islamic Hegira. Anomaliped would describe a foot or walking appendage that is abnormal or unusual in structure. This combination likely resulted from a PDF parsing error where two completely unrelated terms were inadvertently joined together.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'hi-JAHY-ree-uh-NOM-uh-li-ped',
                'etymology': 'Error: "hegirae" (Arabic "hijra") + "anomaliped" (Greek "anomalos" + Latin "pes")',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "hegirae" and "anomaliped" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "HEGIRAEANOMALIPED" - this is a combined word error, separate into HEGIRAE (migrations) + ANOMALIPED (abnormal foot).'
            },
            'hegiraemoissanite': {
                'definition': 'This appears to be a combined word error where "hegirae" (plural of hegira, meaning migrations or journeys) has been incorrectly merged with "moissanite" (a silicon carbide mineral used as a diamond substitute). Hegirae refers to significant migrations or journeys with religious or historical importance, while moissanite is a rare naturally occurring mineral that is synthetically produced for use in jewelry as a diamond alternative due to its brilliance and hardness. This combination likely resulted from a PDF parsing error where two completely unrelated terms were inadvertently joined together.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'hi-JAHY-ree-MOY-suh-nahyt',
                'etymology': 'Error: "hegirae" (Arabic "hijra") + "moissanite" (named after Henri Moissan, French chemist)',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "hegirae" and "moissanite" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "HEGIRAEMOISSANITE" - this is a combined word error, separate into HEGIRAE (migrations) + MOISSANITE (diamond-like mineral).'
            },
            'heinousness': {
                'definition': 'Heinousness refers to the quality of being extremely wicked, evil, or morally reprehensible to a shocking degree. This noun describes the severity and moral depravity of actions, crimes, or behaviors that are so terrible they provoke universal condemnation and disgust. Heinousness implies not just wrongdoing but evil of such magnitude that it offends fundamental moral principles and human decency. The term is often used in legal contexts to describe aggravating factors that make crimes particularly deserving of severe punishment, or in general discourse to emphasize the extreme nature of immoral acts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAY-nuhs-nis',
                'etymology': 'From "heinous" (from Old French "haineus," from "haine" meaning "hatred") + "-ness" suffix.',
                'language_origins': 'Old French',
                'example_sentence': 'The court considered the _______ of the defendant\'s crimes when determining the appropriate sentence.',
                'memory_tip': 'Remember "HEINOUSNESS" - HAIN (hatred) + OUS (full of) + NESS (quality), the quality of being full of hatred and evil.'
            },
            'heiress': {
                'definition': 'Heiress is a female heir who inherits or is entitled to inherit wealth, property, titles, or other valuable assets from family members, typically parents or other relatives. This term specifically refers to women who receive inheritances, often substantial fortunes, that may include money, real estate, businesses, or aristocratic titles. Heiresses often hold significant social and economic status due to their inherited wealth, and historically have been important figures in marriage alliances and social hierarchies. The word emphasizes both the inheritance aspect and the female gender of the inheritor.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AIR-is',
                'etymology': 'From Old French "heir" (heir) + "-ess" feminine suffix.',
                'language_origins': 'Old French',
                'example_sentence': 'As the only _______ to the family fortune, she inherited both the vast estate and the responsibility of managing the family business.',
                'memory_tip': 'Remember "HEIRESS" - HEIR + ESS (female), a female heir who inherits wealth, property, or titles from family.'
            },
            'heirloom': {
                'definition': 'Heirloom refers to a valuable object, piece of property, or tradition that is passed down from generation to generation within a family. These items often have sentimental, historical, or monetary value and serve as tangible connections to family heritage and ancestry. Heirlooms can include jewelry, furniture, artwork, books, tools, or any other objects that families choose to preserve and transmit to their descendants. The term also applies to plant varieties that have been passed down through generations. Heirlooms represent continuity, family identity, and cultural preservation across generations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'AIR-loom',
                'etymology': 'From "heir" (Old French) + "loom" (Old English "gelōma" meaning "tool, utensil").',
                'language_origins': 'Old French, Old English',
                'example_sentence': 'The antique pocket watch was a treasured family _______ that had been passed down from great-grandfather to grandson for four generations.',
                'memory_tip': 'Remember "HEIRLOOM" - HEIR + LOOM (valuable object), valuable objects that loom large in family history and are passed to heirs.'
            },
            'heist': {
                'definition': 'Heist refers to a robbery or theft, particularly one that is carefully planned, involves significant risk, and typically targets valuable items like money, jewelry, or artwork. This term often describes elaborate criminal schemes that require coordination, specialized skills, and detailed planning to execute successfully. Heists have captured public imagination through movies and literature, often portrayed as sophisticated criminal enterprises involving teams of specialists. The word can also be used as a verb meaning to steal or rob in such a manner. Heists typically involve high stakes and dramatic circumstances.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'HAHYST',
                'etymology': 'From German "hissen" meaning "to hoist," later American slang for robbery.',
                'language_origins': 'German (via American slang)',
                'example_sentence': 'The movie depicted a dramatic bank _______ involving a team of skilled criminals and an elaborate escape plan.',
                'memory_tip': 'Remember "HEIST" - HE + IST (one who), like "he is the one who" steals valuable things in a carefully planned robbery.'
            },
            'held': {
                'definition': 'Held is the past tense and past participle of the verb "hold," indicating that someone or something was grasped, supported, contained, or maintained in a particular position or state in the past. The word can describe physical holding (held in hand), events that took place (meeting was held), beliefs or opinions that were maintained (held views), or positions that were occupied (held office). Held indicates completed action of keeping, supporting, conducting, or maintaining something that occurred at a previous time.',
                'part_of_speech': 'verb (past tense/past participle)',
                'pronunciation_guide': 'HELD',
                'etymology': 'Past tense of "hold," from Old English "healdan," from Germanic roots meaning "to keep, guard."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'She _______ the crying child gently until he calmed down and felt safe in her comforting arms.',
                'memory_tip': 'Remember "HELD" - HELped by holding, you helped by holding something or someone securely in the past.'
            },
            'heleoplankton': {
                'definition': 'Heleoplankton refers to microscopic organisms that live in freshwater wetland environments, including marshes, swamps, ponds, and other shallow aquatic habitats. These planktonic organisms include various bacteria, algae, protozoans, and small invertebrates that float or swim weakly in the water column of wetland ecosystems. Heleoplankton play crucial roles in wetland food webs, nutrient cycling, and ecosystem health. They serve as primary producers and consumers, helping to maintain water quality and supporting larger aquatic organisms. The study of heleoplankton helps scientists understand wetland ecology and environmental health.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hel-ee-oh-PLANK-tuhn',
                'etymology': 'From Greek "heleos" meaning "marsh, swamp" + "plankton" meaning "wandering."',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The biologist collected water samples to study the _______ population in the restored wetland ecosystem.',
                'memory_tip': 'Remember "HELEOPLANKTON" - HELEO (marsh) + PLANKTON (floating organisms), floating microscopic organisms in marsh and wetland waters.'
            },
            'heleoplanktonpliant': {
                'definition': 'This appears to be a combined word error where "heleoplankton" (microscopic marsh organisms) has been incorrectly merged with "pliant" (flexible or easily influenced). Heleoplankton refers to microscopic organisms living in freshwater wetland environments, while pliant describes something that is easily bent, flexible, or readily influenced and adaptable. This combination likely resulted from a PDF parsing error where two separate words were inadvertently joined together. The correct terms would be "heleoplankton" referring to wetland microorganisms, and "pliant" referring to flexibility or adaptability.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'hel-ee-oh-PLANK-tuhn-PLAHY-uhnt',
                'etymology': 'Error: "heleoplankton" (Greek "heleos" + "plankton") + "pliant" (Old French "plier")',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "heleoplankton" and "pliant" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "HELEOPLANKTONPLIANT" - this is a combined word error, separate into HELEOPLANKTON (marsh organisms) + PLIANT (flexible).'
            },
            'heliacal': {
                'definition': 'Heliacal refers to astronomical phenomena related to the sun, particularly the rising or setting of stars or other celestial bodies in relation to the sun\'s position. The most common use describes "heliacal rising," when a star becomes visible just before dawn after a period of being hidden by the sun\'s brightness. This astronomical term is important in ancient astronomy and astrology, where heliacal risings marked seasonal changes and calendar events. For example, the heliacal rising of Sirius was significant in ancient Egyptian astronomy for predicting Nile flood cycles.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'hi-LY-uh-kuhl',
                'etymology': 'From Greek "heliakos," from "helios" meaning "sun."',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'Ancient astronomers tracked the _______ rising of specific stars to create accurate calendars for agricultural and religious purposes.',
                'memory_tip': 'Remember "HELIACAL" - HELI (sun) + ACAL (like magical), magical astronomical events related to the sun and stars.'
            },
            'heliotrope': {
                'definition': 'Heliotrope has multiple meanings: it refers to a plant with fragrant purple or white flowers that turn to follow the sun throughout the day, giving it its name meaning "sun-turning." The term also describes a purple or violet color, particularly a reddish-purple hue. In mineralogy, heliotrope is another name for bloodstone, a dark green jasper with red spots. As a plant, heliotrope is popular in gardens and perfumery for its sweet fragrance. The word has been adopted to describe the distinctive purplish color associated with the flower.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'HEE-lee-uh-trohp',
                'etymology': 'From Greek "heliotropion," from "helios" (sun) + "tropos" (turn).',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The garden featured beds of fragrant _______ flowers that filled the evening air with their sweet perfume.',
                'memory_tip': 'Remember "HELIOTROPE" - HELIO (sun) + TROPE (turn), the flower that turns to follow the sun, or the purple color it represents.'
            },
            'helium': {
                'definition': 'Helium is a chemical element with the symbol He and atomic number 2, making it the second lightest and second most abundant element in the observable universe. This noble gas is colorless, odorless, tasteless, and chemically inert under standard conditions. Helium is commonly known for making voices sound high-pitched when inhaled and for its use in balloons and airships due to its low density and non-flammable properties. The element has important scientific and commercial applications, including cooling superconducting magnets in MRI machines and serving as a protective atmosphere for welding.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HEE-lee-uhm',
                'etymology': 'From Greek "helios" meaning "sun," where it was first discovered spectroscopically.',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The party balloons were filled with _______ gas, making them float safely in the air without the fire risk of hydrogen.',
                'memory_tip': 'Remember "HELIUM" - HELI (sun) + UM (element), the element first discovered in the sun that makes balloons float and voices funny.'
            },
            'hellebore': {
                'definition': 'Hellebore is a genus of perennial flowering plants in the buttercup family, known for their early blooming period and toxic properties. These plants produce distinctive flowers in winter or early spring, often called Christmas roses or Lenten roses depending on the species and blooming time. Hellebores are valued in gardening for their ability to flower in cold weather and shade tolerance. However, all parts of hellebore plants contain toxic compounds that can be poisonous to humans and animals if ingested. Historically, some species were used in traditional medicine, though this is not recommended due to toxicity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HEL-uh-bor',
                'etymology': 'From Greek "helleboros," possibly from "elein" (to injure) + "bora" (food), referring to its poisonous nature.',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The gardener planted _______ in the shaded corner where few other flowers would bloom during the winter months.',
                'memory_tip': 'Remember "HELLEBORE" - HELL + BORE, like a boring plant from hell because it\'s poisonous, but blooms beautifully in winter.'
            },
            'helmet': {
                'definition': 'Helmet is a protective covering worn on the head to prevent injury from impacts, falling objects, or other hazards. These safety devices are designed to absorb and distribute the force of blows to protect the skull and brain from trauma. Helmets come in various forms for different activities: motorcycle helmets, bicycle helmets, construction hard hats, military combat helmets, and sports helmets for football, hockey, and other activities. Modern helmets often incorporate advanced materials and design features to maximize protection while maintaining comfort and functionality.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HEL-mit',
                'etymology': 'From Old French "helmet," diminutive of "helme," from Germanic roots meaning "protection."',
                'language_origins': 'Old French, Germanic',
                'example_sentence': 'The construction worker put on his safety _______ before entering the job site where falling debris posed a constant danger.',
                'memory_tip': 'Remember "HELMET" - HELp + MET (meet danger), helps you meet danger safely by protecting your head from harm.'
            },
            'help': {
                'definition': 'Help means to assist, aid, or support someone in accomplishing a task, solving a problem, or dealing with a difficulty. As a noun, help refers to assistance provided to someone in need, or to a person who provides such assistance. Help can involve physical aid, emotional support, guidance, resources, or any form of contribution that makes someone\'s situation better or easier. The concept encompasses both formal assistance programs and informal acts of kindness. Help is fundamental to human cooperation and social functioning, representing our interconnectedness and mutual dependence.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'HELP',
                'etymology': 'From Old English "helpan," from Germanic roots meaning "to aid, assist."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'She was always willing to _______ her neighbors with grocery shopping when they were unable to get out themselves.',
                'memory_tip': 'Remember "HELP" - Hold Everyone\'s Load Properly, holding and supporting everyone\'s load when they need assistance.'
            },
            'helped': {
                'definition': 'Helped is the past tense and past participle of the verb "help," indicating that assistance, aid, or support was provided to someone in the past. This form describes completed acts of helping, whether physical assistance, emotional support, guidance, or any other form of aid that was given at a previous time. Helped can describe various types of assistance that made someone\'s situation better, easier, or more manageable. The word indicates that supportive action was taken and completed in the past.',
                'part_of_speech': 'verb (past tense/past participle)',
                'pronunciation_guide': 'HELPD',
                'etymology': 'Past tense of "help," from Old English "healp," from Germanic roots.',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The volunteers _______ rebuild the community center after the flood damaged the original building.',
                'memory_tip': 'Remember "HELPED" - HELPed Earlier Done, assistance that was provided earlier and is now done or completed.'
            },
            'helpful': {
                'definition': 'Helpful describes something or someone that provides assistance, makes tasks easier, or contributes to solving problems in a beneficial way. This adjective characterizes people who are willing and able to offer aid, or things that prove useful, convenient, or advantageous in accomplishing goals. Helpful can apply to people with supportive attitudes, tools that make work easier, information that clarifies situations, or any resource that contributes positively to desired outcomes. The word emphasizes the beneficial and constructive nature of the assistance provided.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'HELP-fuhl',
                'etymology': 'From "help" (Old English "helpan") + "-ful" suffix meaning "full of" or "characterized by."',
                'language_origins': 'Old English',
                'example_sentence': 'The librarian was extremely _______ in locating the rare books needed for the historical research project.',
                'memory_tip': 'Remember "HELPFUL" - HELP + FUL, full of help and always ready to provide useful assistance to others.'
            },
            'helvetia': {
                'definition': 'Helvetia is the Latin name for Switzerland, derived from the Helvetii, a Celtic tribe that lived in the region during ancient times. This poetic and formal name for Switzerland appears on Swiss coins, official documents, and in formal contexts where Latin terminology is preferred. Helvetia is also personified as a female allegorical figure representing Switzerland in art, literature, and national symbolism. The name connects modern Switzerland to its ancient Celtic heritage and provides a classical, dignified designation for the country that transcends its multiple modern language names (Schweiz, Suisse, Svizzera).',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'hel-VEE-shuh',
                'etymology': 'From Latin "Helvetia," from "Helvetii," the Celtic tribe that inhabited the region.',
                'language_origins': 'Latin, Celtic',
                'example_sentence': 'The Swiss franc coins bear the inscription "______," the formal Latin name for Switzerland.',
                'memory_tip': 'Remember "HELVETIA" - HELVet (help vet) + IA (land), the land that helped veterans (like the Helvetii tribe) in ancient times, now Switzerland.'
            },
            'hematology': {
                'definition': 'Hematology is the medical specialty that focuses on the study, diagnosis, and treatment of blood disorders, blood-forming organs, and diseases of the blood and bone marrow. This field encompasses conditions affecting red blood cells, white blood cells, platelets, plasma, lymph nodes, spleen, and bone marrow. Hematologists diagnose and treat various conditions including anemia, leukemia, lymphoma, hemophilia, and other blood-related disorders. The specialty combines clinical care with laboratory analysis, requiring expertise in interpreting blood tests, bone marrow biopsies, and other diagnostic procedures related to blood health.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hee-muh-TOL-uh-jee',
                'etymology': 'From Greek "haima" meaning "blood" + "logos" meaning "study."',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The patient was referred to the _______ department for specialized treatment of her unusual blood disorder.',
                'memory_tip': 'Remember "HEMATOLOGY" - HEMATO (blood) + LOGY (study), the study of blood and blood-related diseases and disorders.'
            },
            'hemorrhage': {
                'definition': 'Hemorrhage refers to severe or uncontrolled bleeding, either internal or external, that occurs when blood vessels are damaged or ruptured. This medical condition can result from injury, disease, surgical complications, or various medical conditions that affect blood clotting or vessel integrity. Hemorrhages can be life-threatening depending on their location, severity, and duration. As a verb, hemorrhage means to bleed severely or, figuratively, to lose something rapidly in large amounts (such as hemorrhaging money or support). Prompt medical intervention is often critical in managing serious hemorrhages.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'HEM-er-ij',
                'etymology': 'From Greek "haimorrhagia," from "haima" (blood) + "rhegnynai" (to break forth).',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The emergency room doctors worked quickly to stop the internal _______ caused by the car accident.',
                'memory_tip': 'Remember "HEMORRHAGE" - HEMO (blood) + RRHAGE (rage/rush), blood raging or rushing out uncontrollably from the body.'
            },
            'hennery': {
                'definition': 'Hennery is a poultry house or enclosure specifically designed for keeping hens and other domestic fowl. This structure provides shelter, nesting areas, and protection for chickens while allowing them space to move around safely. A hennery typically includes roosting bars, nesting boxes, adequate ventilation, and protection from predators and weather. The term can also refer to a poultry farm or facility where chickens are raised for egg production or meat. Henneries are essential infrastructure for both commercial poultry operations and backyard chicken keeping.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HEN-er-ee',
                'etymology': 'From "hen" (Old English "henn") + "-ery" suffix meaning "place where."',
                'language_origins': 'Old English',
                'example_sentence': 'The farmer built a new _______ with improved ventilation and predator protection for his growing flock of laying hens.',
                'memory_tip': 'Remember "HENNERY" - HEN + ERY (place for), a place for hens to live, lay eggs, and stay safe from predators.'
            },
            'hennin': {
                'definition': 'Hennin is a tall, cone-shaped headdress worn by noblewomen in medieval Europe, particularly during the 15th century. This distinctive fashion accessory was typically made of stiffened fabric or wire frame and often extended two feet or more in height, sometimes decorated with veils or other ornamental elements. The hennin was a symbol of high social status and fashion among the upper classes, particularly in Burgundy, France, and surrounding regions. The elaborate headdress required specific posture and movement, influencing how women carried themselves and interacted in social situations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HEN-in',
                'etymology': 'From Middle French "hennin," of uncertain origin, possibly related to "hen."',
                'language_origins': 'Middle French',
                'example_sentence': 'The medieval portrait showed the duchess wearing an elaborate _______ that rose nearly three feet above her head.',
                'memory_tip': 'Remember "HENNIN" - HEN + IN, like a hen in a tall cone hat, the cone-shaped medieval headdress worn by noble ladies.'
            },
            'henotheism': {
                'definition': 'Henotheism is a religious belief system that acknowledges the existence of multiple gods but focuses worship and devotion primarily on one particular deity, often considered supreme or most relevant to the worshiper\'s community. This theological concept differs from monotheism (belief in only one god) and polytheism (worship of multiple gods equally). Henotheistic traditions recognize other deities as real and powerful but maintain special loyalty to their chosen god. This religious approach appears in various ancient and modern religious traditions and represents a middle ground between strict monotheism and full polytheism.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HEN-oh-thee-izm',
                'etymology': 'From Greek "henos" meaning "one" + "theos" meaning "god" + "-ism" suffix.',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'Scholars debated whether ancient Israelite religion represented early _______ before developing into strict monotheism.',
                'memory_tip': 'Remember "HENOTHEISM" - HEN (one) + THEISM (god belief), believing in many gods but worshipping one main god above others.'
            },
            'henry': {
                'definition': 'Henry has multiple meanings: as a proper name, it\'s a common masculine given name of Germanic origin meaning "home ruler." In physics, henry (symbol H) is the SI unit of electrical inductance, named after American scientist Joseph Henry. One henry is the inductance of a closed circuit in which an electromotive force of one volt is produced when the electric current varies uniformly at one ampere per second. The unit is fundamental in electrical engineering for measuring the property of electrical conductors that opposes changes in current flow.',
                'part_of_speech': 'proper noun, noun (physics unit)',
                'pronunciation_guide': 'HEN-ree',
                'etymology': 'Name: from Germanic "Heimirich" (home ruler); Unit: named after Joseph Henry (1797-1878), American physicist.',
                'language_origins': 'Germanic (name), English (named after person)',
                'example_sentence': 'The electrical engineer calculated that the circuit\'s inductance was approximately 2.5 _______ based on the coil specifications.',
                'memory_tip': 'Remember "HENRY" - HEN (home) + RY (ruler), originally meaning home ruler, now also an electrical unit named after physicist Joseph Henry.'
            },
            'hepatectomy': {
                'definition': 'Hepatectomy is a surgical procedure involving the partial or complete removal of the liver, typically performed to treat liver cancer, severe liver disease, or to obtain liver tissue for transplantation. This complex operation requires extensive surgical expertise due to the liver\'s vital functions and rich blood supply. Partial hepatectomy removes diseased portions while preserving healthy liver tissue, taking advantage of the liver\'s remarkable ability to regenerate. The procedure carries significant risks but can be life-saving for patients with liver tumors or severe liver damage that cannot be treated through other means.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hep-uh-TEK-tuh-mee',
                'etymology': 'From Greek "hepar" meaning "liver" + "ektome" meaning "excision, removal."',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The surgical team prepared for the complex _______ to remove the cancerous portion of the patient\'s liver.',
                'memory_tip': 'Remember "HEPATECTOMY" - HEPAT (liver) + ECTOMY (removal), surgical removal of all or part of the liver.'
            },
            'heptad': {
                'definition': 'Heptad refers to a group, set, or series of seven related items, elements, or units. This term is used in various contexts to describe collections of seven things, whether in chemistry (seven-membered molecular structures), music (seven-note scales), literature (seven-part works), or other fields where seven-element groupings are significant. The concept emphasizes the specific quantity of seven and often implies some organizational or structural relationship among the elements. Heptads appear in cultural, religious, and scientific contexts where the number seven holds particular importance or meaning.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HEP-tad',
                'etymology': 'From Greek "heptas" meaning "group of seven," from "hepta" meaning "seven."',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The musical composition was structured as a _______, with seven distinct movements representing different emotional themes.',
                'memory_tip': 'Remember "HEPTAD" - HEPTA (seven) + D (group), a group of seven related things or elements.'
            },
            'heraldic': {
                'definition': 'Heraldic refers to the art, practice, or science of heraldry, which involves the design, display, and study of armorial bearings or coats of arms. This adjective describes anything related to the formal system of symbols, colors, and designs used to identify families, institutions, or territories through distinctive emblems. Heraldic designs follow specific rules and traditions developed over centuries, including the use of particular colors, patterns, and symbolic elements. The term encompasses the visual, historical, and genealogical aspects of coat-of-arms tradition, as well as ceremonial and decorative applications of heraldic symbols.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'huh-RAL-dik',
                'etymology': 'From "herald" (from Old French "herault") + "-ic" suffix meaning "relating to."',
                'language_origins': 'Old French',
                'example_sentence': 'The cathedral\'s stained glass windows featured _______ symbols representing the noble families who funded its construction.',
                'memory_tip': 'Remember "HERALDIC" - HERALD + IC (related to), related to heralds and their traditional coat-of-arms symbols and designs.'
            },
            'herb': {
                'definition': 'Herb refers to a plant valued for its medicinal, culinary, or aromatic qualities, typically having soft stems that die back seasonally rather than woody stems that persist year-round. In cooking, herbs are used to flavor, garnish, or enhance dishes with their distinctive tastes and aromas. Common culinary herbs include basil, oregano, thyme, rosemary, and parsley. Medicinal herbs have been used throughout human history for healing and health maintenance. The term can also refer more broadly to any small, non-woody plant, distinguishing herbs from shrubs and trees in botanical classification.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'URB (silent H) or HURB',
                'etymology': 'From Old French "erbe," from Latin "herba" meaning "grass, green plant."',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The chef grew a variety of fresh _______ in the restaurant garden, including basil, sage, and rosemary for seasonal dishes.',
                'memory_tip': 'Remember "HERB" - Healing Edible Refreshing Botanicals, plants that are healing, edible, and refreshing for cooking and medicine.'
            },
            'herbaceous': {
                'definition': 'Herbaceous describes plants that have soft, green, non-woody stems that typically die back to ground level at the end of each growing season. These plants lack the persistent woody stems found in shrubs and trees, instead producing new growth from their base or root system each year. Herbaceous plants include most garden flowers, vegetables, and many wild plants. They can be annuals (living one season), biennials (living two seasons), or perennials (living multiple seasons but with stems that die back annually). This botanical term helps classify plants based on their stem structure and growth patterns.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'hur-BAY-shuhs',
                'etymology': 'From Latin "herbaceus," from "herba" meaning "grass, herb" + "-aceous" suffix meaning "resembling."',
                'language_origins': 'Latin',
                'example_sentence': 'The garden designer planned _______ perennial borders that would die back in winter and return with fresh growth each spring.',
                'memory_tip': 'Remember "HERBACEOUS" - HERB + ACEOUS (like herbs), like herbs with soft green stems that die back each year.'
            },
            'herbalist': {
                'definition': 'Herbalist is a person who specializes in the use of plants for medicinal purposes, combining traditional knowledge with understanding of plant properties to promote health and treat illness. These practitioners study the therapeutic effects of various herbs, roots, flowers, and other plant materials, often drawing from traditional healing systems like Traditional Chinese Medicine, Ayurveda, or European folk medicine. Herbalists may grow, harvest, prepare, and prescribe plant-based remedies, though their practice varies widely depending on local regulations and training. They represent a connection between ancient healing wisdom and modern holistic health approaches.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'UR-buh-list or HUR-buh-list',
                'etymology': 'From "herbal" (relating to herbs) + "-ist" suffix meaning "one who practices."',
                'language_origins': 'Latin (via English formation)',
                'example_sentence': 'The experienced _______ recommended a blend of chamomile and valerian root to help with the client\'s sleep difficulties.',
                'memory_tip': 'Remember "HERBALIST" - HERB + ALIST (specialist), a specialist who uses herbs for healing and promoting health.'
            }
        }
        
        return batch_083_data.get(word.lower(), {
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
            'heavenlyheiress': 'Combined word error: "heavenlyheiress" appears to be "heavenly" + "heiress" merged together. This is likely a PDF parsing error where divine/pleasant and female heir terminology were incorrectly combined.',
            'hegiraeanomaliped': 'Combined word error: "hegiraeanomaliped" appears to be "hegirae" + "anomaliped" merged together. This is likely a PDF parsing error where religious migrations and abnormal foot terminology were incorrectly combined.',
            'hegiraemoissanite': 'Combined word error: "hegiraemoissanite" appears to be "hegirae" + "moissanite" merged together. This is likely a PDF parsing error where religious migrations and diamond-like mineral terminology were incorrectly combined.',
            'heleoplanktonpliant': 'Combined word error: "heleoplanktonpliant" appears to be "heleoplankton" + "pliant" merged together. This is likely a PDF parsing error where marsh microorganisms and flexibility terminology were incorrectly combined.'
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
        
        print("Batch 083 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch083Processor()
    input_path = "output/batch_083_words.csv"
    output_path = "output/batch_083_processed.csv"
    processor.process_batch(input_path, output_path)