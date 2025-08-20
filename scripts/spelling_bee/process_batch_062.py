#!/usr/bin/env python3

import pandas as pd
import csv
from dataclasses import dataclass
from typing import Optional
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
    
class DifficultyCalculator:
    @staticmethod
    def calculate_phonetic_transparency(word: str) -> int:
        return 3
    
    @staticmethod
    def calculate_word_frequency(word: str) -> int:
        return 3
    
    @staticmethod
    def calculate_morphological_complexity(word: str) -> int:
        return 3
    
    @staticmethod
    def calculate_etymology_complexity(word: str) -> int:
        return 3

class Batch062Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        batch_062_data = {
            'espial': {
                'definition': 'Espial is the act of watching or observing secretly; espionage or surveillance conducted to gather information without the knowledge of those being observed. This formal term describes covert observation activities that may involve spying, reconnaissance, or intelligence gathering. Espial can be conducted by individuals, organizations, or governments for various purposes including national security, criminal investigation, competitive intelligence, or personal reasons. The practice requires discretion, skill, and often specialized equipment or techniques to avoid detection while obtaining desired information. Historical espial methods ranged from simple eavesdropping to elaborate spy networks, while modern espial may involve sophisticated technology including surveillance cameras, electronic monitoring, and digital intelligence gathering. Legal and ethical considerations surround espial activities, with laws governing when and how surveillance may be conducted. Understanding espial helps recognize both legitimate security activities and potential violations of privacy rights. The term appears in literature, legal documents, and discussions of intelligence operations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'es-PAHY-uhl',
                'etymology': 'From Old French "espial," from "espier" (to spy), possibly from Germanic origin related to "spy." The word evolved alongside espionage and related surveillance terms.',
                'language_origins': 'Germanic, Old French',
                'example_sentence': 'The detective\'s careful _______ of the suspect revealed important evidence for the investigation.',
                'memory_tip': 'Remember "e-SPIAL" - think "e-spy-al" meaning the action of electronic spying, or "espial" sounds like "especially-al" meaning especially watchful observation.'
            },
            'esplanade': {
                'definition': 'An esplanade is a long, open, level area, typically beside the sea or a river, designed for walking and public recreation. These broad walkways or promenades often feature paved surfaces, landscaping, and amenities such as benches, lighting, and viewing areas. Esplanades serve both practical and aesthetic purposes, providing pedestrian access along waterfront areas while creating attractive public spaces for leisure activities. Many coastal cities feature famous esplanades that become focal points for tourism, exercise, and community gatherings. The design of esplanades typically emphasizes unobstructed views of water, easy pedestrian access, and integration with surrounding urban development. Historical esplanades often reflected civic pride and urban planning ideals, demonstrating commitment to public spaces and quality of life. Modern esplanade design considers factors such as accessibility, sustainability, and resilience to sea-level rise. Understanding esplanades helps appreciate urban planning principles and the importance of public spaces in creating livable communities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ES-pluh-nayd',
                'etymology': 'From French "esplanade," from Spanish "explanada," from Latin "explanatus" (flattened out), from "explanare" (to level, flatten).',
                'language_origins': 'Latin, Spanish, French',
                'example_sentence': 'The city\'s beautiful _______ along the harbor attracted thousands of visitors each weekend.',
                'memory_tip': 'Remember "e-SPLA-nade" - think "e-splash-nade" because esplanades are often beside water where you might splash, or "esplanade" sounds like "explain-aid" meaning it explains/shows off the waterfront.'
            },
            'espousal': {
                'definition': 'Espousal refers to the act of adopting, supporting, or advocating for a particular cause, belief, or principle. This formal term describes the process of embracing ideas, policies, or positions and actively promoting them. Espousal implies more than passive agreement; it suggests active commitment and willingness to defend or advance the adopted position. Political espousal involves supporting particular ideologies or policies, while intellectual espousal might involve adopting specific theories or methodologies. Religious espousal refers to embracing particular faith traditions or spiritual practices. The term can also refer to the act of marrying or becoming engaged, though this usage is less common in contemporary English. Successful espousal often requires understanding the principles being adopted and the ability to articulate their value to others. The concept emphasizes the voluntary nature of commitment and the responsibility that comes with advocacy. Understanding espousal helps recognize how individuals and organizations align themselves with particular values or causes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-SPOW-zuhl',
                'etymology': 'From "espouse" (from Old French "espouser," from Latin "sponsare" meaning "to betroth") + "-al" (suffix indicating action or result).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The politician\'s _______ of environmental protection policies gained support from young voters.',
                'memory_tip': 'Remember "e-SPOUS-al" - think "e-spouse-al" like choosing a spouse, meaning choosing to marry yourself to an idea, or "espousal" contains "spouse" meaning to wed yourself to a cause.'
            },
            'essential': {
                'definition': 'Essential means absolutely necessary, indispensable, or forming the fundamental nature of something. This adjective describes elements that are so crucial they cannot be removed without fundamentally changing or destroying the whole. Essential components are those without which a system, process, or entity cannot function properly or maintain its identity. In biology, essential nutrients are those the body cannot produce and must obtain from food. Essential oils contain the concentrated essence of plants. Essential workers perform jobs critical to society\'s functioning. The term can describe both concrete necessities (essential supplies) and abstract concepts (essential qualities). Essential differs from merely important or useful; it indicates absolute necessity rather than high value. Understanding what is truly essential helps prioritize resources, make decisions, and focus on what matters most. The concept appears across fields from philosophy and science to business and personal development, always emphasizing fundamental importance and necessity.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ih-SEN-shuhl',
                'etymology': 'From Late Latin "essentialis," from Latin "essentia" (essence), from "esse" (to be). The word emphasizes the "being" or core nature of something.',
                'language_origins': 'Latin',
                'example_sentence': 'Clean water and adequate food are _______ for human survival and health.',
                'memory_tip': 'Remember "e-SSENT-ial" - think "essence-ial" meaning relating to the essence/core, or "essential" contains "sent" like scent which is the essence of smell.'
            },
            'establishment': {
                'definition': 'Establishment refers to the action of setting up, founding, or creating something intended to be permanent, or to an organization, business, or institution that has been established. The term can describe the process of creating new entities (establishment of a company) or existing institutions (a medical establishment). In political contexts, "the establishment" often refers to the existing power structure, influential institutions, and traditional authority figures who maintain the status quo. Establishments can be commercial (restaurants, shops), institutional (schools, hospitals), or social (clubs, organizations). The concept implies stability, official recognition, and ongoing operation rather than temporary arrangements. Legal establishment involves formal recognition and compliance with regulations. Understanding establishment helps distinguish between formal, recognized institutions and informal arrangements. The term carries implications of authority, tradition, and sometimes resistance to change, particularly when used to describe existing power structures.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-STAB-lish-muhnt',
                'etymology': 'From "establish" (from Old French "establir," from Latin "stabilire" meaning "to make stable") + "-ment" (suffix indicating result or means).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The _______ of the new research center took three years of planning and construction.',
                'memory_tip': 'Remember "e-STAB-lishment" - think "establish-ment" meaning the mental/physical result of establishing, or "establishment" contains "stable" because established things are stable.'
            },
            'estampies': {
                'definition': 'Estampies are medieval musical compositions, typically instrumental dance pieces popular in European court music during the 13th and 14th centuries. These sophisticated musical forms featured repetitive melodic patterns with variations and were often performed for dancing at noble gatherings and ceremonial occasions. Estampies are among the earliest known examples of purely instrumental music in Western classical tradition, representing an important development in medieval musical composition. The structures typically consisted of multiple sections called "puncta," each repeated with different endings (open and closed cadences). These compositions demonstrate the growing sophistication of medieval music and the development of complex rhythmic and melodic patterns. Estampies influenced later dance forms and contributed to the evolution of instrumental music. Modern performances of estampies provide insight into medieval court life and musical practices. Understanding estampies helps appreciate the historical development of Western music and the role of dance in medieval culture.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'es-STAHM-peez',
                'etymology': 'From Old French "estampie," possibly from Provençal "estampida" (stamping), referring to the rhythmic stamping associated with these dance forms.',
                'language_origins': 'Provençal, Old French',
                'example_sentence': 'The medieval music ensemble performed several _______ to demonstrate court dance music from the 14th century.',
                'memory_tip': 'Remember "e-STAMP-ies" - think "e-stamp-ies" like electronic stamps because they\'re repeated patterns, or "estampies" sounds like "he-stamp-ies" meaning he stamps rhythmically to the dance music.'
            },
            'estancia': {
                'definition': 'An estancia is a large cattle ranch or agricultural estate, particularly common in Argentina, Uruguay, and other parts of South America. These extensive properties typically focus on livestock production, especially cattle and sheep, and often encompass thousands of acres of grassland suitable for grazing. Estancias represent an important part of South American agricultural heritage and economic development, serving as centers of rural life and livestock production. Traditional estancias often include the main house (casa principal), worker housing, barns, corrals, and other facilities necessary for ranch operations. Many historic estancias have been converted into tourist destinations, offering visitors experiences of rural life, horseback riding, traditional foods, and gaucho culture. The estancia system significantly influenced the social and economic development of the Pampas region. Modern estancias may combine traditional ranching with agricultural crops, tourism, or conservation efforts. Understanding estancias helps appreciate South American rural culture and the role of large-scale agriculture in regional development.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'es-TAHN-see-ah',
                'etymology': 'From Spanish "estancia," from "estar" (to stay, be), from Latin "stare" (to stand). Originally meant "dwelling place" or "residence."',
                'language_origins': 'Latin, Spanish',
                'example_sentence': 'The historic _______ offered guests an authentic experience of traditional Argentine ranch life.',
                'memory_tip': 'Remember "e-STAN-cia" - think "e-stance-ia" like a stance on land/property, or "estancia" sounds like "he-stands-ia" meaning where he stands on his ranch land.'
            },
            'esteem': {
                'definition': 'Esteem is respect, admiration, and favorable opinion, or the act of regarding someone or something with such positive regard. As a noun, esteem describes the positive reputation and respect that someone has earned through their actions, character, or achievements. As a verb, to esteem means to hold in high regard, value highly, or consider worthy of respect. Self-esteem refers to one\'s own sense of worth and confidence in personal value and abilities. High esteem typically results from demonstrated competence, moral character, and positive contributions to others or society. Professional esteem might be based on expertise and achievements, while personal esteem could stem from character traits and relationships. The concept is fundamental to psychology, education, and social relationships, as feeling esteemed by others contributes to well-being and motivation. Understanding esteem helps recognize the importance of mutual respect and appreciation in human relationships and personal development.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'ih-STEEM',
                'etymology': 'From Old French "estimer," from Latin "aestimare" meaning "to value, estimate, judge the worth of." Related to "estimate" and "estimation."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The teacher was held in high _______ by both students and colleagues for her dedication and expertise.',
                'memory_tip': 'Remember "e-STEEM" - think "e-steam" like the steam/energy that comes from being valued, or "esteem" sounds like "he-steam" meaning the warm feeling of being valued.'
            },
            'esteemdifficulty': {
                'definition': 'This appears to be a combined word error from PDF parsing. It likely represents two separate words: "esteem" (respect and admiration) and "difficulty" (the state of being hard to accomplish). This combination does not form a valid English word.',
                'part_of_speech': 'error',
                'pronunciation_guide': 'N/A - invalid combination',
                'etymology': 'PDF parsing error - combination of unrelated terms',
                'language_origins': 'Error',
                'example_sentence': 'N/A - This is not a valid word',
                'memory_tip': 'N/A - This is a parsing error, not a real word'
            },
            'esteemknack': {
                'definition': 'This appears to be a combined word error from PDF parsing. It likely represents two separate words: "esteem" (respect and admiration) and "knack" (a skill or talent). This combination does not form a valid English word.',
                'part_of_speech': 'error',
                'pronunciation_guide': 'N/A - invalid combination',
                'etymology': 'PDF parsing error - combination of unrelated terms',
                'language_origins': 'Error',
                'example_sentence': 'N/A - This is not a valid word',
                'memory_tip': 'N/A - This is a parsing error, not a real word'
            },
            'esthetic': {
                'definition': 'Esthetic (also spelled aesthetic) relates to beauty, artistic taste, and the appreciation of art and beautiful objects. This adjective describes things that are pleasing to look at, artistically designed, or concerned with beauty rather than practical function. Esthetic considerations involve judgments about what is visually appealing, harmonious, or artistically valuable. The term can describe physical objects (esthetic design), experiences (esthetic pleasure), or philosophical approaches (esthetic theory). Esthetic values influence architecture, fashion, interior design, and various art forms. Personal esthetic preferences vary widely among individuals and cultures, reflecting different standards of beauty and artistic taste. Professional fields like medicine and dentistry use "esthetic" to describe procedures focused on improving appearance rather than just function. Understanding esthetic principles helps people make informed decisions about design, art, and beauty while appreciating diverse forms of artistic expression. The concept bridges objective design principles with subjective personal taste.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'es-THET-ik',
                'etymology': 'From Greek "aisthetikos" meaning "of or for perception," from "aisthanesthai" (to perceive). The modern sense of "beautiful" developed in the 18th century.',
                'language_origins': 'Greek',
                'example_sentence': 'The architect focused on both functional and _______ elements when designing the new museum.',
                'memory_tip': 'Remember "e-STHET-ic" - think "aesthetic" which means the same thing, or "esthetic" sounds like "he-set-tic" meaning he set artistic/beautiful standards.'
            },
            'estimate': {
                'definition': 'To estimate means to roughly calculate, judge, or determine the value, size, quantity, or extent of something without exact measurement. This process involves using available information, experience, and reasoning to make informed approximations when precise data is unavailable or impractical to obtain. Estimates are crucial in planning, budgeting, project management, and decision-making across many fields. Construction estimates predict costs and timelines, scientific estimates approximate quantities in research, and personal estimates help with everyday decisions. Good estimates require understanding relevant factors, considering uncertainties, and applying appropriate methods or formulas. The accuracy of estimates depends on the estimator\'s knowledge, available information, and the complexity of what\'s being estimated. Professional estimators develop specialized skills for their fields, while general estimation skills help everyone make better decisions. Understanding estimation helps people evaluate information, plan effectively, and make reasonable judgments when exact answers aren\'t available.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'ES-tuh-mayt (verb), ES-tuh-mit (noun)',
                'etymology': 'From Latin "aestimatus," past participle of "aestimare" meaning "to value, rate, judge." Related to "esteem" and "estimation."',
                'language_origins': 'Latin',
                'example_sentence': 'The contractor provided an _______ of $50,000 for the kitchen renovation project.',
                'memory_tip': 'Remember "e-STI-mate" - think "e-stimate" like estimating with your "esti" (estimation), or "estimate" sounds like "best-imate" meaning your best intimate guess.'
            },
            'estimated': {
                'definition': 'Estimated is the past tense of "estimate," meaning having made an approximate calculation or judgment about the value, size, quantity, or extent of something. When something is described as estimated, it indicates that the figure or assessment is based on available information and reasoning rather than exact measurement. Estimated values acknowledge uncertainty while providing useful approximations for planning and decision-making. The term appears frequently in reports, proposals, and analyses where precise data isn\'t available but reasonable approximations are needed. Estimated costs help with budgeting, estimated times aid in scheduling, and estimated quantities assist with resource planning. Professional contexts often require disclosure when figures are estimated rather than exact, maintaining transparency about the reliability of information. Understanding that values are estimated helps people interpret information appropriately and make decisions while considering potential margins of error. The term emphasizes the difference between calculated approximations and verified measurements.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'ES-tuh-may-tid',
                'etymology': 'From "estimate" (from Latin "aestimatus") + "-ed" (past tense suffix). Indicates completed action of estimating.',
                'language_origins': 'Latin',
                'example_sentence': 'The archaeologist _______ that the ancient artifact was approximately 3,000 years old.',
                'memory_tip': 'Remember "e-STI-mated" - think "estimated" is past tense of estimate, or "esti-mated" like your estimate mated/paired with reality.'
            },
            'estival': {
                'definition': 'Estival means relating to or occurring in summer; characteristic of the summer season. This adjective describes phenomena, activities, behaviors, or conditions that are associated with the warmest months of the year. Estival patterns might include animal behaviors like summer migration, plant growth cycles that peak in summer, or human activities that are seasonal. In scientific contexts, estival refers to biological or ecological processes that occur during summer months, such as estival hibernation (aestivation) in some animals that become dormant during hot, dry periods. The term provides a precise way to describe seasonal timing without using more common but less formal words. Estival conditions often involve higher temperatures, longer daylight hours, and specific weather patterns. Understanding estival helps distinguish summer-specific phenomena from year-round or other seasonal patterns. The word appears in scientific literature, academic writing, and formal descriptions of seasonal cycles.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ES-tuh-vuhl',
                'etymology': 'From Latin "aestivalis," from "aestivus" (of summer), from "aestas" (summer). Related to "estivation" (summer dormancy).',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ migration of birds to northern breeding grounds occurs each spring and summer.',
                'memory_tip': 'Remember "e-STIV-al" - think "e-stove-al" because summer is like a stove with heat, or "estival" sounds like "festival" and many festivals happen in summer.'
            },
            'estovers': {
                'definition': 'Estovers is a legal term referring to the right of a tenant or life estate holder to take necessary materials from an estate for their reasonable needs, particularly wood for fuel, repairs, and other essential purposes. This ancient property right allows individuals to use natural resources from land they occupy without owning it outright, provided the use is reasonable and necessary for basic living needs. Estovers typically include the right to cut wood for heating (house-bote), repairing buildings (hay-bote), and making tools or farm implements (plow-bote). The concept balances the rights of occupants to live reasonably on the land with the rights of landowners to preserve their property\'s long-term value. Modern applications of estovers are less common due to changed living conditions and property arrangements, but the principle still appears in some lease agreements and property law. Understanding estovers helps appreciate historical property relationships and the evolution of tenant rights. The term reflects medieval and early modern approaches to land use and resource management.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'es-TOH-verz',
                'etymology': 'From Anglo-French "estover," meaning "it is necessary," from Old French "estovoir" (to be necessary), from Latin "est opus" (it is needful).',
                'language_origins': 'Latin, Old French, Anglo-French',
                'example_sentence': 'The medieval tenant\'s _______ allowed him to cut firewood from the lord\'s forest for heating his cottage.',
                'memory_tip': 'Remember "e-STOV-ers" - think "e-stove-ers" because estovers often included the right to wood for stoves/heating, or "estovers" sounds like "he-stoves" meaning he gets wood for stoves.'
            },
            'estrepe': {
                'definition': 'Estrepe is a legal term referring to the voluntary waste or destruction of property by a tenant or other person in lawful possession, particularly when done maliciously or in anticipation of losing their right to the property. This concept applies when someone intentionally damages or destroys buildings, cuts down trees, removes fixtures, or otherwise diminishes the value of property they occupy but do not own. Estrepe typically occurs when tenants know their lease will end or when life estate holders anticipate the termination of their rights. The law generally prohibits estrepe and provides remedies for property owners whose land has been damaged by such actions. Legal consequences may include monetary damages, injunctions to prevent further destruction, or forfeiture of rights. Understanding estrepe helps property owners and tenants recognize the boundaries of acceptable property use and the legal consequences of intentional waste. The concept remains relevant in modern property law, though it\'s less commonly invoked than in historical periods.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'es-TREEP',
                'etymology': 'From Anglo-French "estreper," meaning "to strip, waste," possibly from Germanic origin related to "strip." Legal term for intentional property waste.',
                'language_origins': 'Germanic, Anglo-French',
                'example_sentence': 'The court found the departing tenant guilty of _______ for removing fixtures and damaging the property.',
                'memory_tip': 'Remember "e-STREPE" - think "e-strip" because estrepe involves stripping value from property, or "estrepe" sounds like "he-stripe" meaning he stripes/damages the property.'
            },
            'estuary': {
                'definition': 'An estuary is a coastal water body where freshwater from rivers and streams meets and mixes with salt water from the ocean, creating a unique brackish environment. These transitional ecosystems are among the most productive natural habitats on Earth, supporting diverse plant and animal communities adapted to varying salinity levels. Estuaries serve as nurseries for many marine species, including fish, crabs, and shrimp that spend part of their life cycles in these protected waters. The mixing of nutrients from both freshwater and marine sources creates rich feeding grounds that support complex food webs. Estuaries also provide important ecosystem services including storm protection, water filtration, and carbon sequestration. Human activities often concentrate around estuaries due to their protected harbors, fertile soils, and abundant resources, making these areas centers of commerce and population. Understanding estuaries helps appreciate their ecological importance and the need for conservation in the face of development pressures and climate change.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ES-choo-er-ee',
                'etymology': 'From Latin "aestuarium," from "aestus" (tide, heat, agitation), referring to the tidal movements characteristic of these water bodies.',
                'language_origins': 'Latin',
                'example_sentence': 'The Chesapeake Bay is one of the largest _______ systems in North America, supporting diverse marine life.',
                'memory_tip': 'Remember "e-STU-ary" - think "e-stew-ary" because estuaries are like stews mixing fresh and salt water, or "estuary" sounds like "best-uary" meaning the best place for marine nurseries.'
            },
            'eternity': {
                'definition': 'Eternity refers to time without beginning or end; infinite or unending duration that transcends normal temporal boundaries. This concept represents the ultimate extent of time, beyond human comprehension and experience. Religious and philosophical traditions often associate eternity with divine existence, spiritual realms, or ultimate reality that exists outside temporal constraints. In mathematics and physics, eternity relates to concepts of infinity and the theoretical limits of time. Human attempts to understand eternity often involve contemplating what existence might be like without the familiar markers of past, present, and future. The concept appears in discussions of mortality, meaning, and purpose, as people grapple with their finite existence within an apparently infinite universe. Eternity can evoke both wonder and anxiety, representing both ultimate freedom from temporal limitations and the overwhelming nature of infinite duration. Understanding different conceptions of eternity helps people explore fundamental questions about existence, time, and meaning.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-TUR-ni-tee',
                'etymology': 'From Old French "eternité," from Latin "aeternitas," from "aeternus" (eternal), from "aevum" (age, era) + "-ternus" (suffix indicating duration).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The philosopher contemplated what it would mean to experience consciousness for all _______.',
                'memory_tip': 'Remember "e-TERN-ity" - think "eternal-ity" meaning the quality of being eternal, or "eternity" sounds like "he-turn-ity" meaning time that turns forever without end.'
            },
            'ethanol': {
                'definition': 'Ethanol is a colorless, volatile alcohol (C2H5OH) that is the intoxicating ingredient in alcoholic beverages and also serves as an important industrial chemical and biofuel. This simple alcohol is produced through fermentation of sugars by yeast or through chemical synthesis from petroleum products. In beverage production, ethanol results from the fermentation of grains, fruits, or other plant materials containing sugars or starches. Industrial ethanol is used as a solvent, antiseptic, and chemical intermediate in manufacturing various products including cosmetics, pharmaceuticals, and cleaning products. As a biofuel, ethanol is blended with gasoline to reduce emissions and petroleum dependence, with common blends including E10 (10% ethanol) and E85 (85% ethanol). Ethanol is less toxic than methanol but still requires careful handling as it is flammable and can be harmful in large quantities. Understanding ethanol helps appreciate its diverse applications in industry, energy, and consumption while recognizing associated health and safety considerations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ETH-uh-nol',
                'etymology': 'From "ethane" (the hydrocarbon) + "-ol" (suffix indicating alcohol). Coined in the late 19th century as chemical nomenclature developed.',
                'language_origins': 'Modern scientific terminology',
                'example_sentence': 'The gas station offered fuel containing 10% _______ to reduce environmental impact.',
                'memory_tip': 'Remember "ETH-anol" - think "eth-an-ol" like "ethnic-an-alcohol" or remember "ethanol" sounds like "breath-anol" because you can smell it on someone\'s breath.'
            },
            'ethylene': {
                'definition': 'Ethylene is a colorless, flammable gas (C2H4) that serves as both an important industrial chemical and a natural plant hormone. As an industrial compound, ethylene is one of the most widely produced organic chemicals, serving as a raw material for manufacturing plastics (especially polyethylene), antifreeze, synthetic rubber, and various other chemicals. In agriculture and plant biology, ethylene functions as a gaseous hormone that regulates plant growth, fruit ripening, flower development, and leaf senescence. Commercial fruit producers often use ethylene gas to control ripening timing, allowing them to harvest fruit early and ripen it when needed for market. The gas is naturally produced by plants during stress responses and developmental processes. Ethylene\'s discovery as a plant hormone revolutionized understanding of plant physiology and agricultural practices. Industrial production typically involves steam cracking of petroleum products. Understanding ethylene helps appreciate both industrial chemistry and plant biology, demonstrating how the same molecule can have vastly different applications.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ETH-uh-leen',
                'etymology': 'From "ethyl" (from "ether" + "-yl") + "-ene" (suffix indicating unsaturated hydrocarbon). Named in early chemical nomenclature development.',
                'language_origins': 'Modern scientific terminology',
                'example_sentence': 'The fruit distributor used _______ gas to ripen bananas uniformly for grocery store delivery.',
                'memory_tip': 'Remember "ETHYL-ene" - think "ethyl-lean" like a lean ethyl compound, or "ethylene" contains "ethyl" (alcohol-related) + "ene" (gas) meaning a gas related to alcohol compounds.'
            },
            'ethyleneflaneur': {
                'definition': 'This appears to be a combined word error from PDF parsing. It likely represents two separate words: "ethylene" (a chemical compound and plant hormone) and "flâneur" (a person who strolls observantly through city streets). This combination does not form a valid English word.',
                'part_of_speech': 'error',
                'pronunciation_guide': 'N/A - invalid combination',
                'etymology': 'PDF parsing error - combination of unrelated terms',
                'language_origins': 'Error',
                'example_sentence': 'N/A - This is not a valid word',
                'memory_tip': 'N/A - This is a parsing error, not a real word'
            },
            'etouffee': {
                'definition': 'Étouffée is a classic Cajun and Creole dish from Louisiana featuring shellfish (typically crawfish or shrimp) cooked in a rich, thick sauce made from a roux (flour and fat), the "holy trinity" of vegetables (onions, celery, and bell peppers), garlic, and various seasonings. The name comes from the French word meaning "smothered," referring to the cooking method where ingredients are slowly simmered in their own juices and the thick sauce. Traditional étouffée is served over rice and represents the fusion of French cooking techniques with local Louisiana ingredients and flavors. The dish showcases the resourcefulness of Cajun and Creole cooks who created complex, flavorful meals from available local seafood and vegetables. Variations exist between Cajun (typically darker roux, spicier) and Creole (often includes tomatoes) versions. Understanding étouffée helps appreciate Louisiana\'s unique culinary heritage and the cultural influences that shaped Cajun and Creole cuisine.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ay-too-FAY',
                'etymology': 'From French "étouffée," past participle of "étouffer" (to smother, stifle), from Old French "estouffer," describing the smothered cooking method.',
                'language_origins': 'French',
                'example_sentence': 'The New Orleans restaurant served authentic crawfish _______ with perfectly seasoned rice.',
                'memory_tip': 'Remember "é-TOUF-fée" - think "ay-tough-ay" because it\'s tough/thick sauce, or "étouffée" sounds like "hey-toupee" but it\'s actually smothered seafood.'
            },
            'etruscan': {
                'definition': 'Etruscan refers to the ancient civilization that flourished in central Italy (primarily modern Tuscany) from approximately the 8th to 3rd centuries BCE, before being absorbed into the Roman Empire. The Etruscans developed a sophisticated society with advanced metallurgy, art, architecture, and urban planning that significantly influenced early Roman culture. Etruscan contributions to Roman civilization included religious practices, governmental structures, engineering techniques, and artistic styles. The Etruscan language remains partially understood despite extensive archaeological evidence, as it belongs to a unique language family unrelated to Indo-European languages. Etruscan art, particularly tomb paintings and bronze work, provides valuable insights into their culture, beliefs, and daily life. The civilization was organized into city-states that formed loose confederations for mutual defense and trade. Understanding Etruscan history helps appreciate the complex cultural foundations that contributed to Roman civilization and the diversity of ancient Italian peoples.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'ih-TRUHS-kuhn',
                'etymology': 'From Latin "Etruscus," from Greek "Tyrsenos," referring to the people of Etruria (ancient Tuscany). The origin of their self-designation is uncertain.',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'The museum\'s _______ collection included bronze mirrors and painted tomb decorations from ancient Italy.',
                'memory_tip': 'Remember "e-TRUSC-an" - think "e-trust-can" because you can trust Etruscan influence on Rome, or "Etruscan" sounds like "he-trust-scan" meaning scanning/studying trustworthy ancient culture.'
            },
            'etymology': {
                'definition': 'Etymology is the study of the origin, history, and development of words and their meanings, tracing how words have evolved through time and across languages. This linguistic discipline examines how words are formed, how they change in meaning and pronunciation over centuries, and how they spread from one language to another through cultural contact, conquest, or borrowing. Etymology reveals the historical relationships between languages and provides insights into the cultures, migrations, and interactions of peoples throughout history. Professional etymologists use comparative linguistics, historical records, and archaeological evidence to trace word origins and development patterns. Understanding etymology helps people recognize patterns in language, improve vocabulary, and appreciate the rich history embedded in everyday speech. Many English words have complex etymological histories, showing influences from Latin, Greek, Germanic languages, French, and many others. Etymology demonstrates that language is constantly evolving and that words carry stories of human civilization, trade, conquest, and cultural exchange.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'et-uh-MOL-uh-jee',
                'etymology': 'From Greek "etymologia," from "etymon" (true sense) + "logia" (study of), literally meaning "study of true meanings."',
                'language_origins': 'Greek',
                'example_sentence': 'The _______ of the word "salary" traces back to the Latin word for salt, which was once used as payment.',
                'memory_tip': 'Remember "etymo-LOGY" - think "etymo" (true meaning) + "logy" (study), or "etymology" sounds like "eat-him-ology" meaning the study of eating up/consuming word origins.'
            },
            'eucalyptus': {
                'definition': 'Eucalyptus refers to a large genus of flowering trees and shrubs native to Australia, characterized by their distinctive aromatic leaves, smooth bark that often sheds in strips, and rapid growth. These evergreen plants are adapted to various Australian climates and have become important worldwide for their commercial, medicinal, and ecological value. Eucalyptus oil, extracted from the leaves, contains compounds like eucalyptol that provide antiseptic and decongestant properties, making it valuable in pharmaceuticals, cosmetics, and aromatherapy. Many eucalyptus species are cultivated globally for timber, paper production, and ornamental purposes. The trees are essential to Australian ecosystems, providing habitat and food for koalas and many other native species. Some eucalyptus species have become invasive in non-native environments due to their rapid growth and high water consumption. Understanding eucalyptus helps appreciate both their ecological importance in Australia and their global economic significance, while recognizing the environmental considerations involved in their cultivation outside their native range.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'yoo-kuh-LIP-tuhs',
                'etymology': 'From Greek "eu-" (well) + "kalyptos" (covered), referring to the cap that covers the flower buds. Named by French botanist Charles Louis L\'Héritier in 1788.',
                'language_origins': 'Greek',
                'example_sentence': 'The koala spent most of its day sleeping in the _______ tree, occasionally munching on the aromatic leaves.',
                'memory_tip': 'Remember "eu-ca-LYP-tus" - think "you-ka-lips" because eucalyptus oil is good for your lips/breathing, or "eucalyptus" sounds like "you-clip-us" because you clip the leaves for oil.'
            },
            'eucrasia': {
                'definition': 'Eucrasia is a medical term referring to a normal, healthy condition or good temperament of the body, particularly in terms of the proper balance of bodily humors or physiological functions. This concept originates from ancient Greek medicine and the theory of humoral balance, where health was thought to depend on the proper mixture of four bodily humors: blood, phlegm, yellow bile, and black bile. Eucrasia represents the ideal state where these humors exist in harmonious proportion, resulting in good health and well-being. While modern medicine has moved beyond humoral theory, the concept of eucrasia still appears in discussions of homeostasis and physiological balance. The term emphasizes the importance of equilibrium in bodily functions for maintaining health. Understanding eucrasia helps appreciate historical medical concepts and the continuing relevance of balance and moderation in health and wellness. The concept reflects ancient wisdom about the importance of harmony and proportion in achieving optimal physical condition.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'yoo-KRAY-zhah',
                'etymology': 'From Greek "eukrasia," from "eu-" (good, well) + "krasis" (mixture, temperament), literally meaning "good mixture" or "proper temperament."',
                'language_origins': 'Greek',
                'example_sentence': 'Ancient physicians sought to restore _______ by balancing the patient\'s humors through diet and lifestyle changes.',
                'memory_tip': 'Remember "eu-CRAS-ia" - think "you-crash-ia" but opposite because eucrasia means you don\'t crash (good health), or "eu-crazy-ia" meaning good crazy/balanced state.'
            },
            'eudiometer': {
                'definition': 'A eudiometer is a scientific instrument used to measure the volume of gases, particularly for analyzing gas mixtures and studying combustion reactions. This glass apparatus typically consists of a graduated tube that can be filled with gas and allows for precise volume measurements under controlled conditions. Eudiometers are commonly used in chemistry laboratories to determine the composition of gas mixtures, measure gas production in reactions, and study the properties of different gases. The instrument enables chemists to conduct volumetric gas analysis by measuring how much gas is consumed or produced in chemical reactions. Historical eudiometers were crucial in early gas chemistry research, helping scientists like Antoine Lavoisier understand combustion and respiration. Modern versions may include electronic sensors and digital readouts for greater precision. Understanding eudiometers helps appreciate the tools used in gas chemistry and the historical development of techniques for studying gaseous substances. These instruments remain valuable for educational demonstrations and specialized research applications.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'yoo-dee-OM-i-ter',
                'etymology': 'From Greek "eu-" (good, well) + "dios" (Zeus, divine) + "-meter" (measure), originally meaning "good air measurer" as it was used to test air quality.',
                'language_origins': 'Greek',
                'example_sentence': 'The chemistry student used a _______ to measure the volume of hydrogen gas produced in the electrolysis experiment.',
                'memory_tip': 'Remember "eu-DIO-meter" - think "you-do-meter" because you do measuring with it, or "eudiometer" contains "meter" which tells you it measures something (gases).'
            },
            'eulogy': {
                'definition': 'A eulogy is a speech or piece of writing that praises and honors a deceased person, typically delivered at a funeral service or memorial gathering. These commemorative addresses celebrate the life, achievements, character, and positive impact of the person who has died, providing comfort to grievers while preserving the memory of the deceased. Eulogies often include personal anecdotes, significant accomplishments, character traits, and the ways the deceased influenced others\' lives. The art of writing and delivering eulogies requires sensitivity, thoughtfulness, and the ability to capture the essence of a person\'s life in meaningful ways. Cultural and religious traditions influence eulogy styles and content, with some emphasizing spiritual aspects while others focus on earthly achievements and relationships. Effective eulogies balance grief and celebration, acknowledging loss while honoring life. Understanding eulogies helps people prepare for the difficult task of honoring deceased loved ones and appreciating the importance of commemorating lives well-lived.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'YOO-luh-jee',
                'etymology': 'From Greek "eulogia," from "eu-" (good, well) + "logos" (speech, word), literally meaning "good speech" or "praise."',
                'language_origins': 'Greek',
                'example_sentence': 'The heartfelt _______ captured the essence of her grandmother\'s generous spirit and lifetime of service to others.',
                'memory_tip': 'Remember "eu-LOGY" - think "you-ology" like the study of you (someone\'s life), or "eulogy" contains "logy" (speech) meaning a good speech about someone.'
            },
            'euphonious': {
                'definition': 'Euphonious means having a pleasant, harmonious sound; pleasing to the ear with smooth, flowing, melodious qualities. This adjective describes speech, music, poetry, or other sounds that create agreeable auditory experiences through their rhythm, tone, and phonetic qualities. Euphonious language often features smooth consonant combinations, flowing vowel sequences, and rhythmic patterns that feel natural and pleasant to hear and speak. Poets and writers deliberately choose euphonious words and phrases to create beautiful sound effects and emotional responses. Musical compositions described as euphonious typically have harmonious melodies and pleasant tonal qualities. The concept contrasts with cacophonous sounds that are harsh or discordant. Different languages have varying inherent euphonious qualities based on their phonetic structures and sound patterns. Understanding euphonious helps people appreciate the aesthetic dimensions of language and music beyond just meaning and function. The pursuit of euphonious expression reflects human appreciation for beauty in auditory experiences.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'yoo-FOH-nee-uhs',
                'etymology': 'From Greek "euphonos," from "eu-" (good, well) + "phone" (sound, voice), literally meaning "good-sounding."',
                'language_origins': 'Greek',
                'example_sentence': 'The poet chose _______ words that flowed together like music when read aloud.',
                'memory_tip': 'Remember "eu-PHON-ious" - think "you-phone-ious" like you want to phone someone with a good voice, or "euphonious" contains "phone" (sound) meaning good sound.'
            },
            'euphoria': {
                'definition': 'Euphoria is an intense feeling of happiness, excitement, and well-being that exceeds normal levels of contentment or joy. This psychological state involves heightened mood, increased energy, and often an exaggerated sense of optimism or elation. Euphoria can result from various causes including personal achievements, positive life events, physical exercise, social experiences, or chemical influences. In medical contexts, euphoria may be a symptom of certain mental health conditions, medication effects, or substance use. Natural euphoria from accomplishments, relationships, or experiences is generally considered positive and healthy. The intensity of euphoric feelings typically distinguishes them from ordinary happiness or satisfaction. Athletes often experience euphoria after significant victories, while new parents might feel euphoric when meeting their babies. Understanding euphoria helps recognize both healthy emotional highs and potentially concerning mood changes that might indicate underlying issues. The experience reflects the human capacity for profound joy and the complex relationship between brain chemistry and emotional states.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'yoo-FAWR-ee-uh',
                'etymology': 'From Greek "euphoria," from "euphoros" (bearing well), from "eu-" (good, well) + "pherein" (to bear, carry).',
                'language_origins': 'Greek',
                'example_sentence': 'The team felt overwhelming _______ after winning the championship game in overtime.',
                'memory_tip': 'Remember "eu-PHOR-ia" - think "you-for-ia" like you\'re for/in favor of feeling great, or "euphoria" sounds like "you-for-ya" meaning you\'re totally for feeling amazing.'
            },
            'euphrates': {
                'definition': 'The Euphrates is one of the most historically and geographically significant rivers in the world, flowing through Turkey, Syria, and Iraq before joining with the Tigris River to form the Shatt al-Arab waterway that empties into the Persian Gulf. This major river is approximately 2,800 kilometers (1,740 miles) long and, along with the Tigris, formed the boundary of ancient Mesopotamia, often called the "cradle of civilization." The Euphrates has been crucial to human civilization for millennia, supporting the development of agriculture, cities, and empires including Sumerian, Babylonian, and Assyrian civilizations. The river provides water for irrigation, drinking, and hydroelectric power generation for millions of people across the region. Modern challenges include water management disputes between countries, climate change effects on water flow, and the environmental impact of dam construction. Understanding the Euphrates helps appreciate its role in human history and the ongoing importance of water resources in international relations and regional development.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'yoo-FRAY-teez',
                'etymology': 'From Greek "Euphrates," from Old Persian "Ufratu," possibly meaning "good to cross over" or from Akkadian "Purattu," the ancient name for the river.',
                'language_origins': 'Old Persian, Greek',
                'example_sentence': 'Ancient Babylon was built along the banks of the _______ River in modern-day Iraq.',
                'memory_tip': 'Remember "eu-PHRATES" - think "you-phrases" because many historical phrases/stories come from this river region, or "Euphrates" sounds like "you-frates" meaning you and your frates (friends) living by the historic river.'
            },
            'eurhythmics': {
                'definition': 'Eurhythmics (also spelled eurythmics) is a method of musical education that teaches rhythm, structure, and musical expression through bodily movement and physical response to music. Developed by Swiss musician and educator Émile Jaques-Dalcroze in the early 20th century, this approach emphasizes the connection between music and natural body movement to develop musical understanding and expression. Students learn to internalize musical concepts like tempo, dynamics, phrasing, and form through walking, clapping, swaying, and other physical activities that correspond to musical elements. Eurhythmics helps develop musical ear, coordination, concentration, and creative expression simultaneously. The method is particularly effective for young children but benefits learners of all ages by engaging multiple senses in musical learning. Many music education programs incorporate eurhythmic principles to make musical instruction more engaging and comprehensive. Understanding eurhythmics helps appreciate holistic approaches to music education that recognize the natural connection between musical rhythm and human movement.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'yoo-RITH-miks',
                'etymology': 'From Greek "eu-" (good, well) + "rhythmos" (rhythm), literally meaning "good rhythm." Coined by Émile Jaques-Dalcroze for his movement-based music education method.',
                'language_origins': 'Greek',
                'example_sentence': 'The music teacher used _______ to help students feel the beat by having them step and clap to different rhythms.',
                'memory_tip': 'Remember "eu-RHYTH-mics" - think "you-rhythm-mics" like you learn rhythm with your body movement, or "eurhythmics" contains "rhythm" which is what you learn through movement.'
            },
            'euripus': {
                'definition': 'A euripus is a narrow strait or channel of water, particularly one with strong, turbulent currents or rapidly changing tidal flows. The term originates from the Euripus Strait between the Greek mainland and the island of Euboea, famous for its unpredictable and frequently changing currents that puzzled ancient observers. In geographical contexts, euripus refers to similar narrow waterways characterized by complex tidal patterns, swirling currents, or rapid flow changes that can make navigation challenging. These waterways often occur between islands or where larger bodies of water are constricted into narrow passages. The turbulent nature of euripus waters has made them subjects of scientific study to understand tidal mechanics and ocean current behavior. Metaphorically, euripus can describe any situation characterized by constant change, unpredictability, or turbulent conditions. Understanding euripus helps recognize both specific geographical features and the broader concept of turbulent, changeable waterways that challenge navigation and understanding.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'yoo-RAHY-puhs',
                'etymology': 'From Greek "Euripos," the name of the strait between mainland Greece and Euboea, from "eu-" (well) + "rhipe" (rush, throw), referring to its rushing waters.',
                'language_origins': 'Greek',
                'example_sentence': 'The ancient sailors feared the _______ for its unpredictable currents that could change direction multiple times per day.',
                'memory_tip': 'Remember "eu-RIP-us" - think "you-rip-us" because the ripping currents could tear ships apart, or "euripus" sounds like "you-rip-pus" meaning the violent water movements.'
            },
            'euro': {
                'definition': 'The euro is the official currency of the Eurozone, used by 19 of the 27 European Union member countries and several non-EU territories. Introduced in 1999 for electronic transactions and in 2002 as physical coins and banknotes, the euro represents one of the world\'s major currencies and a significant achievement in European economic integration. The euro facilitates trade and travel within member countries by eliminating exchange rate fluctuations and transaction costs. The European Central Bank manages monetary policy for the eurozone, setting interest rates and controlling money supply. Euro adoption requires countries to meet specific economic criteria including inflation rates, government debt levels, and currency stability. The currency has faced various challenges including the European debt crisis, differing economic conditions among member states, and questions about fiscal policy coordination. Understanding the euro helps appreciate European integration efforts and the complexities of managing a shared currency across diverse economies.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'YOOR-oh',
                'etymology': 'From "Europe," shortened form adopted for the common European currency. Officially chosen in 1995 from several proposed names for the new currency.',
                'language_origins': 'Modern European creation',
                'example_sentence': 'Travelers appreciated using the _______ throughout their trip across multiple European countries.',
                'memory_tip': 'Remember "EU-ro" - think "EU" (European Union) + "ro" (rolling/money rolling), or "euro" is simply the European currency starting with "Euro-pe."'
            },
            'euroclydon': {
                'definition': 'Euroclydon is a violent, tempestuous wind mentioned in the New Testament (Acts 27:14) that struck the ship carrying the apostle Paul to Rome, causing a dangerous storm that lasted many days. This biblical term describes a powerful northeastern wind in the Mediterranean Sea, known for its sudden onset and destructive force. The word appears in the account of Paul\'s shipwreck during his voyage to Rome as a prisoner. Meteorologically, euroclydon likely refers to what modern weather systems would classify as a severe Mediterranean storm or cyclone with characteristics similar to a typhoon or hurricane. These storms can develop rapidly in the Mediterranean basin, particularly during autumn and winter months, creating dangerous conditions for maritime travel. The term has entered literary and theological usage to describe any sudden, violent tempest or overwhelming adversity. Understanding euroclydon helps appreciate both ancient maritime dangers and the use of weather imagery in religious and literary contexts to represent life\'s sudden challenges.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'yoo-ROK-li-don',
                'etymology': 'From Greek "Euroklydōn," possibly from "euros" (east wind) + "klydon" (wave, surge), referring to an eastern storm wind that creates violent waves.',
                'language_origins': 'Greek',
                'example_sentence': 'The biblical account describes how the ship was caught in a fierce _______ that drove them off course for days.',
                'memory_tip': 'Remember "euro-CLY-don" - think "euro-cry-don" because the European wind makes people cry, or "euroclydon" contains "cyclone" which is a similar violent storm.'
            },
            'europe': {
                'definition': 'Europe is the second-smallest continent by area but the third-most populous, located entirely in the Northern Hemisphere and mostly in the Eastern Hemisphere. Bounded by the Arctic Ocean to the north, the Atlantic Ocean to the west, and the Mediterranean Sea to the south, Europe is separated from Asia by the Ural Mountains, Ural River, Caspian Sea, Caucasus Mountains, and Black Sea. The continent has profoundly influenced world history through its role in the development of Western civilization, science, art, philosophy, and political systems. Europe comprises approximately 50 countries with diverse languages, cultures, and political systems, unified partly through organizations like the European Union and NATO. The continent has been the birthplace of major historical movements including the Renaissance, Enlightenment, Industrial Revolution, and both World Wars. Modern Europe balances national identities with increasing integration through economic, political, and cultural cooperation. Understanding Europe helps appreciate the complex interplay of unity and diversity in one of the world\'s most historically significant regions.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'YOOR-uhp',
                'etymology': 'From Greek "Europe," possibly from Akkadian "erebu" (sunset, west) or from the Greek myth of Europa, a Phoenician princess abducted by Zeus.',
                'language_origins': 'Greek, possibly Akkadian',
                'example_sentence': 'The student\'s semester abroad in _______ included visits to twelve different countries and countless historical sites.',
                'memory_tip': 'Remember "EU-rope" - think "EU" (European Union) + "rope" because Europe is tied together like a rope, or "Europe" sounds like "you-rope" meaning you rope together many countries.'
            },
            'european': {
                'definition': 'European refers to anything relating to Europe, its peoples, cultures, languages, or characteristics. As an adjective, European describes the diverse range of national identities, cultural traditions, political systems, and historical experiences found across the European continent. As a noun, a European is a person from any European country or someone who identifies with European culture or values. The concept encompasses tremendous diversity, including different language families (Indo-European branches like Germanic, Romance, Slavic, Celtic), religious traditions (Christianity in various forms, Judaism, Islam, secular traditions), and political systems (democracies, monarchies, republics). European culture has significantly influenced global art, music, literature, philosophy, science, and political thought. Modern European identity also includes the shared experience of European Union membership for many countries, though European identity extends beyond EU membership. Understanding European diversity helps appreciate how continental identity can coexist with strong national and regional cultures.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'yoor-uh-PEE-uhn',
                'etymology': 'From "Europe" + "-an" (suffix meaning "relating to" or "person from"). Developed as Europe became recognized as a distinct geographical and cultural region.',
                'language_origins': 'Greek, English suffix',
                'example_sentence': 'The _______ Parliament represents citizens from all member countries of the European Union.',
                'memory_tip': 'Remember "Euro-PEE-an" - think "Euro-pee-an" like European people, or "European" simply means "Europe-an" meaning from or relating to Europe.'
            },
            'europium': {
                'definition': 'Europium is a chemical element with the symbol Eu and atomic number 63, belonging to the lanthanide series of rare earth metals. This silvery-white metal is one of the least abundant rare earth elements and has unique properties that make it valuable for specific technological applications. Europium is highly reactive and oxidizes rapidly in air, requiring careful storage and handling. The element has two stable isotopes and several radioactive ones. Europium\'s most important commercial use is in phosphors for fluorescent lights and television screens, where it produces red and blue colors in display technologies. The element also has applications in nuclear reactor control rods due to its high neutron absorption cross-section. Europium compounds are used in anti-counterfeiting measures for currency and documents because of their unique fluorescent properties under ultraviolet light. Understanding europium helps appreciate the specialized applications of rare earth elements in modern technology and the importance of these materials in electronics and security applications.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'yoor-OH-pee-uhm',
                'etymology': 'Named after Europe by French chemist Eugène-Anatole Demarçay in 1901, following the pattern of naming elements after continents and regions.',
                'language_origins': 'Latin (from Europe)',
                'example_sentence': 'The fluorescent bulb produced its characteristic red glow thanks to _______ compounds in the phosphor coating.',
                'memory_tip': 'Remember "euro-PI-um" - think "Euro-premium" because it\'s a premium European-named element, or "europium" is simply "Europe-ium" meaning the element named after Europe.'
            },
            'eurythmics': {
                'definition': 'Eurythmics (alternative spelling of eurhythmics) is a method of musical education that teaches rhythm, structure, and musical expression through bodily movement and physical response to music. This approach, developed by Swiss educator Émile Jaques-Dalcroze, emphasizes the natural connection between musical rhythm and human movement to develop comprehensive musical understanding. Students learn musical concepts through activities like walking to different tempos, expressing dynamics through gesture, and physically representing musical phrases and forms. The method engages multiple senses simultaneously, helping students internalize musical elements more effectively than traditional theoretical approaches alone. Eurythmics is particularly beneficial for developing musical ear training, coordination, concentration, and creative expression. The approach has influenced modern music education, dance training, and therapeutic applications that use movement and music for healing and development. Understanding eurythmics helps appreciate holistic educational methods that recognize the interconnectedness of mind, body, and musical expression in learning.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'yoo-RITH-miks',
                'etymology': 'From Greek "eu-" (good, well) + "rhythmos" (rhythm), meaning "good rhythm." Alternative spelling of "eurhythmics."',
                'language_origins': 'Greek',
                'example_sentence': 'The dance school incorporated _______ into their curriculum to help students develop better musical timing and expression.',
                'memory_tip': 'Remember "eury-THMI-cs" - think "every-rhythm-ics" meaning every type of rhythm learned through movement, or "eurythmics" like the music group that combined rhythm and movement.'
            },
            'eustress': {
                'definition': 'Eustress is positive stress that motivates, energizes, and enhances performance while promoting growth and adaptation. Unlike distress (negative stress that can be harmful), eustress represents beneficial stress responses that help individuals rise to challenges, achieve goals, and develop resilience. Common sources of eustress include exciting opportunities, challenging but achievable goals, exercise, creative projects, positive life changes like marriage or new jobs, and competitive activities. Eustress activates the body\'s stress response system in ways that improve focus, energy, and performance without causing the harmful effects associated with chronic negative stress. The concept helps distinguish between stress that supports well-being and stress that undermines it. Optimal performance often occurs with moderate levels of eustress, following the Yerkes-Dodson law that relates arousal to performance. Understanding eustress helps people recognize how some stress can be beneficial and how to cultivate positive stress while managing negative stress. The concept emphasizes the importance of challenge and growth in human development.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'YOO-stres',
                'etymology': 'From Greek "eu-" (good, well) + "stress," coined by endocrinologist Hans Selye in the 1970s to distinguish positive from negative stress.',
                'language_origins': 'Greek, English',
                'example_sentence': 'The athlete experienced _______ before the competition, feeling energized and focused rather than anxious.',
                'memory_tip': 'Remember "eu-STRESS" - think "you-stress" but good stress, or "eustress" sounds like "you-stress" positively meaning stress that helps you perform better.'
            },
            'eutonic': {
                'definition': 'Eutonic refers to a state of normal or proper muscle tone, representing the healthy balance of muscle tension that allows for optimal function, posture, and movement. This medical term describes the ideal muscular condition where muscles maintain appropriate resting tension while being able to contract and relax as needed for various activities. Eutonic muscle tone supports proper posture, efficient movement patterns, and joint stability without excessive tension or laxity. The concept contrasts with hypotonic (low muscle tone) and hypertonic (high muscle tone) conditions that can impair function and cause discomfort. Eutonic conditions are maintained through regular exercise, proper nutrition, adequate rest, and healthy lifestyle habits. Physical therapy and movement education often focus on achieving and maintaining eutonic states in patients with muscle tone disorders. Understanding eutonic helps appreciate the importance of balanced muscle function in overall health and the therapeutic goals of various movement and medical interventions aimed at restoring optimal muscle tone.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'yoo-TON-ik',
                'etymology': 'From Greek "eu-" (good, well) + "tonikos" (relating to tone or tension), literally meaning "good tone" or "proper tension."',
                'language_origins': 'Greek',
                'example_sentence': 'The physical therapist worked to restore _______ muscle function after the patient\'s injury.',
                'memory_tip': 'Remember "eu-TON-ic" - think "you-tonic" like a good tonic for your muscles, or "eutonic" contains "tonic" meaning a healthy muscle tone condition.'
            },
            'evactor': {
                'definition': 'An evactor is a legal term referring to a person who wrongfully dispossesses another of their land or property, typically through illegal means such as forcible entry, fraud, or other unlawful actions. This term appears in property law and legal proceedings involving wrongful ejection or dispossession of rightful owners or lawful occupants. Evactors may be individuals who unlawfully take possession of property, refuse to leave after their right to occupy has ended, or use deceptive means to gain control of real estate. Legal remedies against evactors typically include actions for ejectment, damages for unlawful dispossession, and restoration of possession to rightful owners. The term distinguishes between lawful eviction procedures conducted by proper authorities and unlawful dispossession by individuals acting without legal authority. Understanding evactor helps recognize the legal distinctions between authorized and unauthorized property actions and the remedies available to property owners who have been wrongfully dispossessed.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-VAK-ter',
                'etymology': 'From Latin "evictus" (dispossessed) + "-or" (agent suffix), meaning "one who dispossesses." Related to "evict" and "eviction."',
                'language_origins': 'Latin',
                'example_sentence': 'The court ordered the _______ to pay damages and restore possession of the illegally seized property.',
                'memory_tip': 'Remember "e-VACT-or" - think "e-vacate-or" meaning someone who makes others evacuate wrongfully, or "evactor" sounds like "he-factor" meaning the factor/person who wrongfully evicts.'
            },
            'evacuees': {
                'definition': 'Evacuees are people who have been moved from a place of danger to a safer location, typically during emergencies such as natural disasters, military conflicts, industrial accidents, or other threatening situations. This term describes individuals who have been temporarily or permanently relocated for their safety and protection. Evacuees may leave voluntarily in response to warnings or be mandatorily removed by authorities when conditions become life-threatening. The evacuation process often involves coordination between emergency services, government agencies, and humanitarian organizations to ensure safe transportation and temporary shelter. Evacuees face numerous challenges including temporary housing, access to essential services, separation from homes and possessions, and uncertainty about when they can return. Historical examples include evacuees from World War II bombings, hurricane evacuees from coastal areas, and evacuees from nuclear accidents. Understanding evacuees helps appreciate the human impact of disasters and the importance of emergency preparedness and humanitarian response systems.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'ih-vak-yoo-EEZ',
                'etymology': 'From "evacuate" (from Latin "evacuatus," meaning "to empty out") + "-ee" (suffix indicating recipient of action) + "-s" (plural).',
                'language_origins': 'Latin',
                'example_sentence': 'The Red Cross established temporary shelters for _______ displaced by the wildfire.',
                'memory_tip': 'Remember "e-VAC-u-ees" - think "e-vacuum-ees" because people are vacuumed/sucked out of dangerous areas, or "evacuees" are simply people who evacuate.'
            },
            'evaded': {
                'definition': 'Evaded is the past tense of "evade," meaning to have successfully avoided, escaped from, or eluded something undesirable such as capture, responsibility, detection, or confrontation. When someone has evaded something, they have managed to stay away from it through skill, cleverness, luck, or deliberate action. The term can describe physical avoidance (evaded capture by hiding) or abstract avoidance (evaded responsibility by making excuses). Evaded can have neutral, positive, or negative connotations depending on context: evading a dangerous situation might be wise, while evading legal obligations could be problematic. Military contexts often describe how forces evaded enemy detection, while legal contexts might discuss how someone evaded taxes or prosecution. The word suggests active effort to avoid rather than passive absence or coincidental avoidance. Understanding evaded helps distinguish between different types of avoidance and the various motivations and methods people use to escape unwanted situations or consequences.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'ih-VAY-did',
                'etymology': 'From "evade" (from Latin "evadere," meaning "to go out, escape") + "-ed" (past tense suffix).',
                'language_origins': 'Latin',
                'example_sentence': 'The suspect _______ police for three days before finally being apprehended at the border.',
                'memory_tip': 'Remember "e-VAD-ed" - think "e-wade-ed" like wading away from something, or "evaded" sounds like "he-waved-ed" meaning he waved goodbye while escaping.'
            },
            'evaluate': {
                'definition': 'To evaluate means to assess, judge, or determine the value, quality, importance, or worth of something through careful analysis and consideration. This process involves examining evidence, comparing against standards or criteria, and forming reasoned conclusions about merit or effectiveness. Evaluation occurs across numerous contexts: teachers evaluate student performance, employers evaluate job candidates, researchers evaluate study results, and consumers evaluate products before purchasing. Effective evaluation requires clear criteria, systematic analysis, and objective consideration of relevant factors. The process often involves both quantitative measures (numbers, statistics) and qualitative assessments (opinions, observations). Evaluation helps inform decisions, improve performance, and ensure accountability in various systems. Academic evaluation might assess learning outcomes, while business evaluation could focus on profitability or efficiency. Understanding evaluation helps people make better decisions, recognize quality, and contribute to improvement processes in personal and professional contexts.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'ih-VAL-yoo-ayt',
                'etymology': 'From French "évaluer," from "é-" (out) + "value" (value), meaning "to determine the value of." Related to "value" and "evaluation."',
                'language_origins': 'French, Latin',
                'example_sentence': 'The committee will _______ all proposals before selecting the best design for the new library.',
                'memory_tip': 'Remember "e-VAL-uate" - think "e-value-ate" meaning to find/eat up the value of something, or "evaluate" contains "value" which is what you determine when evaluating.'
            },
            'evanescent': {
                'definition': 'Evanescent means quickly fading away, vanishing like vapor, or lasting only briefly before disappearing. This adjective describes things that are transient, ephemeral, or fleeting in nature, often with a quality of delicate beauty that makes their temporary nature particularly poignant. Evanescent phenomena might include morning mist that disappears with sunrise, brief moments of perfect happiness, fleeting emotions, or temporary natural displays like rainbows or shooting stars. The term often applies to experiences or sensations that are vivid but short-lived, creating a sense of preciousness due to their temporary nature. In literature and poetry, evanescent is used to capture the bittersweet quality of beautiful things that cannot last. Scientific contexts might describe evanescent waves or fields that decay rapidly over distance. Understanding evanescent helps appreciate the beauty and significance of temporary experiences while recognizing the natural cycles of appearance and disappearance in many aspects of life.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'ev-uh-NES-uhnt',
                'etymology': 'From Latin "evanescens," present participle of "evanescere" (to vanish), from "e-" (out) + "vanescere" (to vanish), from "vanus" (empty).',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ beauty of the cherry blossoms made their brief blooming season even more precious.',
                'memory_tip': 'Remember "e-VAN-escent" - think "e-vanish-escent" meaning becoming vanished, or "evanescent" sounds like "he-vanish-ent" meaning he\'s vanishing.'
            },
            'evaporation': {
                'definition': 'Evaporation is the physical process by which liquid molecules gain enough energy to transition into the gas phase, typically occurring at the surface of a liquid at temperatures below its boiling point. This fundamental process is part of the water cycle, where solar energy causes water from oceans, lakes, rivers, and other surfaces to become water vapor that rises into the atmosphere. Evaporation occurs when individual molecules at the liquid surface acquire sufficient kinetic energy to overcome intermolecular forces holding them in the liquid state. Factors affecting evaporation rate include temperature, humidity, air movement, and surface area exposed to air. The process is endothermic, meaning it absorbs heat energy from the surroundings, which is why evaporation has a cooling effect. Industrial applications of evaporation include concentrating solutions, purifying liquids, and cooling systems. Understanding evaporation helps explain weather patterns, climate processes, and various technological applications that rely on phase changes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ih-vap-uh-RAY-shuhn',
                'etymology': 'From Latin "evaporationem," from "evaporare" (to disperse in vapor), from "e-" (out) + "vapor" (steam, vapor).',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ of water from the lake was accelerated by the hot, dry winds.',
                'memory_tip': 'Remember "e-VAPOR-ation" - think "e-vapor-ation" meaning the action of becoming vapor, or "evaporation" clearly contains "vapor" which is what liquid becomes.'
            },
            'evaporationbittern': {
                'definition': 'This appears to be a combined word error from PDF parsing. It likely represents two separate words: "evaporation" (the process of liquid becoming vapor) and "bittern" (a type of wading bird or a bitter liquid residue). This combination does not form a valid English word.',
                'part_of_speech': 'error',
                'pronunciation_guide': 'N/A - invalid combination',
                'etymology': 'PDF parsing error - combination of unrelated terms',
                'language_origins': 'Error',
                'example_sentence': 'N/A - This is not a valid word',
                'memory_tip': 'N/A - This is a parsing error, not a real word'
            },
            'even': {
                'definition': 'Even has multiple meanings depending on its use as an adjective, adverb, verb, or noun. As an adjective, even means flat, level, smooth, or uniform; numerically divisible by two without remainder; or equal in degree, intensity, or amount. As an adverb, even emphasizes something surprising or extreme, as in "even the experts were puzzled." The word can express emphasis, inclusion of unexpected cases, or precise specification. As a verb, even means to make level, smooth, or equal, often used with "out" (even out differences). Even numbers include 2, 4, 6, 8, etc. The concept of evenness implies balance, fairness, uniformity, or lack of irregularity. Understanding the various uses of even helps in mathematical contexts (even numbers), descriptive contexts (even surfaces), and emphatic contexts (even more surprising). The word demonstrates how common words can have multiple, related meanings that share concepts of balance and regularity.',
                'part_of_speech': 'adjective, adverb, verb, noun',
                'pronunciation_guide': 'EE-vuhn',
                'etymology': 'From Old English "efen" meaning "level, equal, like," from Proto-Germanic "ebnaz." Related to German "eben" and Dutch "even."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The carpenter used a level to ensure the shelf was perfectly _______.',
                'memory_tip': 'Remember "E-ven" - think "equal-even" meaning equally balanced, or "even" sounds like "he-ven" (heaven) which is perfectly balanced and smooth.'
            },
            'evening': {
                'definition': 'Evening is the period of the day between afternoon and night, typically characterized by the gradual transition from daylight to darkness as the sun sets. This time period generally begins in late afternoon and extends until nightfall, though the exact timing varies by season and geographical location. Evening often represents a time of transition, rest, and social activities as people finish work or school and engage in leisure, family time, or social gatherings. Cultural traditions often associate evening with specific activities such as dinner, entertainment, reflection, or preparation for sleep. The quality of evening light, often called "golden hour" by photographers, is prized for its warm, soft illumination. Evening can also refer to the latter part or decline of something, as in "the evening of one\'s life." Understanding evening helps appreciate natural cycles, daily rhythms, and the cultural significance of different times of day in organizing human activities and experiences.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'EEV-ning',
                'etymology': 'From Old English "æfnung," from "æfen" (evening) + "-ing" (suffix). Related to German "Abend" and the concept of "even" (nightfall).',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The family enjoyed their _______ walk through the neighborhood as the streetlights began to flicker on.',
                'memory_tip': 'Remember "E-ven-ing" - think "even" (smooth/calm) + "ing" (happening), meaning the calm time happening, or "evening" is when things become "even" and settled for the day.'
            }
        }
        
        return batch_062_data.get(word, {
            'definition': f'Definition for {word} not found in batch data.',
            'part_of_speech': 'unknown',
            'pronunciation_guide': f'Pronunciation for {word} not available.',
            'etymology': f'Etymology for {word} not available.',
            'language_origins': 'Unknown',
            'example_sentence': f'Example sentence for {word} not available.',
            'memory_tip': f'Memory tip for {word} not available.'
        })
    
    def process_batch(self, input_file: str, output_file: str):
        print(f"Processing {input_file}...")
        
        # Read the input CSV
        df = pd.read_csv(f"C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/{input_file}")
        
        processed_words = []
        errors_found = []
        
        for _, row in df.iterrows():
            word = row['word'].strip()
            
            # Check for combined word errors
            is_error = False
            error_message = ""
            
            combined_words = [
                'esteemdifficulty', 'esteemknack', 'ethyleneflaneur', 'evaporationbittern'
            ]
            
            if word in combined_words:
                is_error = True
                if word == 'esteemdifficulty':
                    error_message = 'Combined word error: "esteemdifficulty" appears to be "esteem" + "difficulty" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
                elif word == 'esteemknack':
                    error_message = 'Combined word error: "esteemknack" appears to be "esteem" + "knack" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
                elif word == 'ethyleneflaneur':
                    error_message = 'Combined word error: "ethyleneflaneur" appears to be "ethylene" + "flâneur" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
                elif word == 'evaporationbittern':
                    error_message = 'Combined word error: "evaporationbittern" appears to be "evaporation" + "bittern" merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.'
                errors_found.append(f"  - {word}: {error_message}")
            
            # Get comprehensive Claude data
            claude_data = self.get_comprehensive_claude_data(word)
            
            # Calculate difficulty components
            phonetic_transparency = self.difficulty_calc.calculate_phonetic_transparency(word)
            word_frequency = self.difficulty_calc.calculate_word_frequency(word)
            morphological_complexity = self.difficulty_calc.calculate_morphological_complexity(word)
            etymology_complexity = self.difficulty_calc.calculate_etymology_complexity(word)
            
            word_data = WordData(
                word=word,
                definition=claude_data['definition'],
                part_of_speech=claude_data['part_of_speech'],
                pronunciation_guide=claude_data['pronunciation_guide'],
                etymology=claude_data['etymology'],
                language_origins=claude_data['language_origins'],
                example_sentence=claude_data['example_sentence'],
                memory_tip=claude_data['memory_tip']
            )
            
            processed_word = {
                'word': word_data.word,
                'years': row['years'],
                'source_files': row['source_files'],
                'source_difficulties': row['source_difficulties'],
                'definition': word_data.definition,
                'part_of_speech': word_data.part_of_speech,
                'pronunciation_guide': word_data.pronunciation_guide,
                'pronunciation_audio_file': '',
                'etymology': word_data.etymology,
                'etymology_source': 'Claude',
                'language_origins': word_data.language_origins,
                'example_sentence': word_data.example_sentence,
                'example_sentence_source': 'Claude',
                'memory_tip': word_data.memory_tip,
                'phonetic_transparency_score': phonetic_transparency,
                'word_frequency_score': word_frequency,
                'morphological_complexity_score': morphological_complexity,
                'etymology_complexity_score': etymology_complexity,
                'final_difficulty_rating': '',
                'final_difficulty_source': '',
                'notes': '',
                'reviewed': False,
                'needs_audio': True,
                'has_image': False,
                'image_description': '',
                'is_error': is_error,
                'error_details': error_message if is_error else ''
            }
            
            processed_words.append(processed_word)
        
        # Write the processed CSV
        output_path = f"C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/{output_file}"
        
        fieldnames = [
            'word', 'years', 'source_files', 'source_difficulties', 'definition', 
            'part_of_speech', 'pronunciation_guide', 'pronunciation_audio_file',
            'etymology', 'etymology_source', 'language_origins', 'example_sentence',
            'example_sentence_source', 'memory_tip', 'phonetic_transparency_score',
            'word_frequency_score', 'morphological_complexity_score', 'etymology_complexity_score',
            'final_difficulty_rating', 'final_difficulty_source', 'notes', 'reviewed',
            'needs_audio', 'has_image', 'image_description', 'is_error', 'error_details'
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed_words)
        
        print(f"Successfully processed {len(processed_words)}/{len(df)} words to {output_file}")
        
        if errors_found:
            print(f"Found {len(errors_found)} error(s):")
            for error in errors_found:
                print(error)
        
        print("Batch 062 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch062Processor()
    processor.process_batch("batch_062_words.csv", "batch_062_processed.csv")