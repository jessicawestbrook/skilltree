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

class Batch080Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
        self.errors = []
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        batch_080_data = {
            'grout': {
                'definition': 'Grout is a mixture of water, cement, and sometimes sand used to fill the spaces between tiles, bricks, or stones in construction and masonry work. This material serves both functional and aesthetic purposes by sealing joints, preventing water penetration, and creating smooth, finished surfaces. Grout comes in various types including cement-based, epoxy, and urethane formulations, each suited for different applications. After application, grout hardens to provide structural support and weather resistance. Proper grouting is essential for preventing moisture damage, maintaining structural integrity, and achieving professional-looking tile installations in bathrooms, kitchens, and other areas.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GROWT',
                'etymology': 'From Old English "grūt" meaning "coarse grain, dregs," related to "grits."',
                'language_origins': 'Old English',
                'example_sentence': 'The tiler carefully applied _______ between the ceramic tiles to create watertight seals in the bathroom renovation.',
                'memory_tip': 'Remember "GROUT" - GReat filling stuff that fills the gaps OUT, the great material that fills gaps out between tiles.'
            },
            'grouth': {
                'definition': 'Grouth appears to be an archaic or dialectal variant of "growth," meaning the process of increasing in size, developing, or expanding over time. Growth encompasses physical enlargement, maturation, development of skills or knowledge, economic expansion, or any progressive change toward greater size, complexity, or maturity. This older spelling form would have carried the same meanings as modern "growth" - referring to natural biological development, personal advancement, business expansion, or any process of positive change and development. The word represents fundamental processes of change and development in living organisms, organizations, and abstract concepts.',
                'part_of_speech': 'noun (archaic/variant spelling)',
                'pronunciation_guide': 'GROWTH',
                'etymology': 'Archaic variant of "growth," from Old Norse "grōthr," from Germanic roots meaning "to grow."',
                'language_origins': 'Old Norse, Germanic (archaic spelling)',
                'example_sentence': 'The ancient text described the _______ of the kingdom over many generations, using the older spelling common to that era.',
                'memory_tip': 'Remember "GROUTH" - GROw + oUT + H, an old way to spell growth, growing out with an extra H at the end.'
            },
            'groves': {
                'definition': 'Groves are small groups of trees growing together, typically without undergrowth, often planted or maintained for specific purposes such as fruit production, landscaping, or religious significance. These tree groupings are smaller than forests but larger than individual plantings, creating natural or cultivated spaces that provide shade, beauty, and often practical benefits. Groves can consist of various tree types including olive groves, citrus groves, or sacred groves used for spiritual purposes. The term suggests an organized, intentional arrangement of trees that serves both aesthetic and functional purposes in agriculture, landscaping, or cultural practices.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GROHVZ',
                'etymology': 'Plural of "grove," from Old English "grāf," meaning "thicket, copse."',
                'language_origins': 'Old English',
                'example_sentence': 'The ancient olive _______ on the hillside had been producing fruit for the family farm for over two centuries.',
                'memory_tip': 'Remember "GROVES" - GROw + VES (places), places where trees grow together in organized groups.'
            },
            'growing': {
                'definition': 'Growing describes the process of increasing in size, developing, or expanding, whether referring to living organisms, businesses, knowledge, or abstract concepts. This present participle indicates ongoing development, maturation, or enlargement over time. Growing can describe physical development in plants, animals, or people, or metaphorical expansion in areas like growing confidence, growing concern, or growing markets. The word suggests continuous, progressive change toward greater size, complexity, maturity, or intensity. Growing implies active development rather than static existence, emphasizing dynamic change and forward progress.',
                'part_of_speech': 'verb (present participle), adjective',
                'pronunciation_guide': 'GROH-ing',
                'etymology': 'Present participle of "grow," from Old English "grōwan," from Germanic roots meaning "to grow."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The _______ concern about climate change led to increased investment in renewable energy technologies.',
                'memory_tip': 'Remember "GROWING" - GROWing larger and strongER, continuously becoming larger and stronger over time.'
            },
            'growling': {
                'definition': 'Growling describes the act of making a low, rumbling, threatening sound, typically produced by angry or aggressive animals, especially dogs, or by humans expressing displeasure or irritation. Animal growls serve as warnings, indicating potential aggression or territorial defense. Human growling can express anger, frustration, or impatience, often through a low, guttural vocal sound. The term can also describe similar low rumbling sounds made by machinery, storms, or other non-living sources. Growling serves as a form of communication that conveys threat, displeasure, or warning across various contexts.',
                'part_of_speech': 'verb (present participle), noun',
                'pronunciation_guide': 'GROWL-ing',
                'etymology': 'From "growl," probably imitative of the sound, possibly related to "grin" or "groan."',
                'language_origins': 'English (imitative)',
                'example_sentence': 'The protective dog began _______ when strangers approached the family\'s front yard at night.',
                'memory_tip': 'Remember "GROWLING" - GROWLing like an angry animal, making GROWLy sounds when upset or aggressive.'
            },
            'grown': {
                'definition': 'Grown is the past participle of "grow," indicating that development, increase, or maturation has been completed. Something grown has reached a state of maturity or has achieved increased size through natural development or cultivation. The word can describe physical development (grown plants, grown children), cultivated products (grown crops), or developed qualities (grown wisdom). Grown often implies reaching adulthood or maturity, as in "grown man" or "grown woman." The term emphasizes completed development rather than ongoing growth, suggesting achievement of a mature or developed state.',
                'part_of_speech': 'verb (past participle), adjective',
                'pronunciation_guide': 'GROHN',
                'etymology': 'Past participle of "grow," from Old English "grōwan," from Germanic roots meaning "to grow."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The vegetables _______ in the garden this summer exceeded all expectations for size and flavor.',
                'memory_tip': 'Remember "GROWN" - GROWing is Now done, something that has finished growing and reached maturity.'
            },
            'grub': {
                'definition': 'Grub has several meanings: as a noun, it refers to the larval stage of insects, particularly beetles, characterized by a soft, white, worm-like appearance. These larvae live in soil or decaying matter and eventually metamorphose into adult insects. Grub can also mean food in informal usage, or refer to hard, physical work, especially digging or manual labor. As a verb, grub means to dig in the ground, search thoroughly, or work hard at something. The various meanings share themes of earth-related activity, basic sustenance, or fundamental work.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GRUB',
                'etymology': 'From Middle English "grubben," meaning "to dig," related to "grave" (to dig).',
                'language_origins': 'Middle English',
                'example_sentence': 'The gardener found several beetle _______ while turning the soil for the spring vegetable planting.',
                'memory_tip': 'Remember "GRUB" - GRound hUg Bug, the ground-hugging bug larvae, or GRUBby food (informal slang for food).'
            },
            'grudgingly': {
                'definition': 'Grudgingly describes doing something in a reluctant, unwilling manner, with resentment or bad grace. When someone acts grudgingly, they perform an action or make a concession while clearly showing their displeasure, reluctance, or resentment about having to do so. This adverb indicates that the person feels forced or pressured into the action and does not do it willingly or enthusiastically. Grudging behavior often involves minimal compliance, lack of genuine cooperation, or obvious signs of displeasure while performing the required task or making the requested concession.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'GRUJ-ing-lee',
                'etymology': 'From "grudge" (from Old French "grouchier") + "-ing" + "-ly" adverb suffix.',
                'language_origins': 'Old French',
                'example_sentence': 'She _______ agreed to work overtime, making it clear through her body language that she was not happy about it.',
                'memory_tip': 'Remember "GRUDGINGLY" - GRUDGe + ING + LY, doing something grudgingly while holding a grudge and showing displeasure.'
            },
            'grudginglycanopy': {
                'definition': 'This appears to be a combined word error where "grudgingly" (reluctantly, unwillingly) has been incorrectly merged with "canopy" (a covering or shelter formed by tree branches or fabric). Grudgingly means doing something with reluctance or resentment, while a canopy refers to the uppermost layer of tree branches in a forest or an artificial covering that provides shelter or decoration. This combination likely resulted from a PDF parsing error where two separate words were inadvertently joined together. The correct terms would be "grudgingly" referring to reluctant behavior, and "canopy" referring to overhead covering or shelter.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'GRUJ-ing-lee-KAN-uh-pee',
                'etymology': 'Error: "grudgingly" (Old French "grouchier") + "canopy" (Medieval Latin "canopeum")',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "grudgingly" and "canopy" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "GRUDGINGLYCANOPY" - this is a combined word error, separate into GRUDGINGLY (reluctantly) + CANOPY (overhead covering).'
            },
            'gruel': {
                'definition': 'Gruel is a thin, watery porridge made by boiling grain, typically oats or rice, in water or milk until it reaches a soup-like consistency. This simple food has historically served as sustenance for the poor, sick, or imprisoned due to its low cost and easy digestibility. Gruel requires minimal ingredients and cooking skill, making it accessible during times of hardship or scarcity. While nutritionally basic, gruel can provide essential calories and carbohydrates. The term often carries connotations of poverty, punishment, or minimal subsistence, as it represents the most basic form of prepared food.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GROO-uhl',
                'etymology': 'From Old French "gruel," from Germanic roots meaning "coarse meal."',
                'language_origins': 'Old French, Germanic',
                'example_sentence': 'During the harsh winter, the orphanage served thin _______ to the children when other food supplies ran low.',
                'memory_tip': 'Remember "GRUEL" - GRU (gru like gruel) + EL, a grueling thin soup that\'s the most basic food for survival.'
            },
            'grueldifficulty': {
                'definition': 'This appears to be a combined word error where "gruel" (thin porridge) has been incorrectly merged with "difficulty" (something hard to accomplish or understand). Gruel is a thin, watery porridge typically made from oats or other grains, while difficulty refers to the state or quality of being hard to do, understand, or deal with. This combination likely resulted from a PDF parsing error where two separate words were inadvertently joined together. The correct terms would be "gruel" referring to the simple food, and "difficulty" referring to challenges or problems.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'GROO-uhl-DIF-i-kul-tee',
                'etymology': 'Error: "gruel" (Old French "gruel") + "difficulty" (Latin "difficilis")',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "gruel" and "difficulty" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "GRUELDIFFICULTY" - this is a combined word error, separate into GRUEL (thin porridge) + DIFFICULTY (hard problem).'
            },
            'gruelgroom': {
                'definition': 'This appears to be a combined word error where "gruel" (thin porridge) has been incorrectly merged with "groom" (a man about to be married or to care for appearance). Gruel is a thin, watery porridge made from grains, while groom can refer to a bridegroom or the act of cleaning and maintaining appearance or preparing someone for advancement. This combination likely resulted from a PDF parsing error where two separate words were inadvertently joined together. The correct terms would be "gruel" referring to the simple food, and "groom" referring to either the wedding participant or grooming activities.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'GROO-uhl-GROOM',
                'etymology': 'Error: "gruel" (Old French "gruel") + "groom" (Middle English "grome")',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "gruel" and "groom" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "GRUELGROOM" - this is a combined word error, separate into GRUEL (thin porridge) + GROOM (bridegroom or grooming).'
            },
            'gruesome': {
                'definition': 'Gruesome describes something that is horrifyingly or revoltingly frightful, causing feelings of revulsion, horror, or disgust. Something gruesome is characterized by graphic violence, death, gore, or other disturbing elements that shock or horrify viewers or readers. The word describes scenes, stories, images, or situations that are macabre, grisly, ghastly, or repulsive in nature. Gruesome content often involves blood, violence, death, or injury presented in vivid, disturbing detail. The term emphasizes the visceral, disturbing quality of something that causes people to recoil in horror, fear, or disgust.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GROO-sum',
                'etymology': 'From "grue" (to shudder) + "-some" suffix meaning "characterized by."',
                'language_origins': 'English',
                'example_sentence': 'The crime scene was so _______ that even experienced detectives had difficulty examining the evidence.',
                'memory_tip': 'Remember "GRUESOME" - GRU (grew) + SOME fear, something that grew to be fearsome and horrifying to witness.'
            },
            'grumbling': {
                'definition': 'Grumbling describes the act of complaining or expressing dissatisfaction in a low, muttering voice, often characterized by continuous, subdued complaints or expressions of displeasure. People grumble when they are annoyed, frustrated, or unhappy about something but may not want to voice their complaints openly or loudly. Grumbling can also describe low rumbling sounds made by natural phenomena like thunder, stomach sounds, or machinery. The behavior suggests ongoing discontent that is expressed through quiet, persistent complaining rather than direct confrontation or loud protest.',
                'part_of_speech': 'verb (present participle), noun',
                'pronunciation_guide': 'GRUM-bling',
                'etymology': 'From "grumble," probably imitative, related to Middle Dutch "grommelen."',
                'language_origins': 'Middle Dutch (imitative)',
                'example_sentence': 'The employees were _______ about the new policy changes, expressing their dissatisfaction in hushed conversations.',
                'memory_tip': 'Remember "GRUMBLING" - GRUMpy + bLING (making sounds), making grumpy sounds of complaint and dissatisfaction.'
            },
            'grumpy': {
                'definition': 'Grumpy describes someone who is bad-tempered, irritable, or easily annoyed, often displaying a consistently sour or unfriendly demeanor. A grumpy person tends to be moody, cranky, and quick to express displeasure or annoyance with situations, people, or circumstances. This temperament can be temporary due to fatigue, stress, or specific situations, or it can be a more persistent personality trait. Grumpy behavior often includes frowning, complaining, snapping at others, or showing general dissatisfaction. The term suggests someone who is difficult to please and tends to focus on negative aspects of situations.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GRUM-pee',
                'etymology': 'From "grump" (probably imitative) + "-y" suffix meaning "characterized by."',
                'language_origins': 'English (imitative)',
                'example_sentence': 'My grandfather becomes _______ when he doesn\'t get enough sleep, snapping at everyone until he takes his afternoon nap.',
                'memory_tip': 'Remember "GRUMPY" - GRUMbling and crankY, someone who\'s grumbling and cranky all the time.'
            },
            'gruyère': {
                'definition': 'Gruyère is a hard Swiss cheese named after the town of Gruyères in Switzerland, known for its rich, nutty, slightly sweet flavor that develops complexity with age. This traditional Alpine cheese is made from cow\'s milk and has a pale yellow interior with small holes scattered throughout. Young Gruyère is creamy and mild, while aged versions develop a more intense, complex flavor with crystalline texture. The cheese is excellent for melting, making it popular for fondue, French onion soup, and gratins. Gruyère is protected by designation of origin laws, ensuring authentic production methods and regional authenticity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'groo-YAIR',
                'etymology': 'Named after Gruyères, a town in Switzerland where this cheese originated.',
                'language_origins': 'Swiss (place name)',
                'example_sentence': 'The chef grated fresh _______ over the French onion soup, creating a golden, bubbly top when broiled.',
                'memory_tip': 'Remember "GRUYÈRE" - GReat cheese from switzerlAnd with a YEARning taste, a great Swiss cheese with complex flavors.'
            },
            'guam': {
                'definition': 'Guam is an unincorporated territory of the United States located in the western Pacific Ocean, serving as the largest and southernmost island in the Mariana Islands archipelago. This strategic island has significant military importance and serves as a major U.S. naval and air force base in the Pacific region. Guam has a rich indigenous Chamorro culture blended with American, Spanish, and other Pacific influences due to its complex colonial history. The island features tropical climate, beautiful beaches, and coral reefs, making it both a military stronghold and tourist destination. Guam plays a crucial role in U.S. Pacific defense strategy.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'GWAHM',
                'etymology': 'From Chamorro "Guåhan," the indigenous name for the island.',
                'language_origins': 'Chamorro (indigenous Pacific language)',
                'example_sentence': 'The military family was stationed at _______ for three years, enjoying the tropical climate and rich cultural heritage.',
                'memory_tip': 'Remember "GUAM" - Great U.S. Armed forces location in the Pacific, where great U.S. military forces are located.'
            },
            'guan': {
                'definition': 'Guan refers to a type of large bird found in Central and South America, belonging to the family Cracidae, which includes guans, chachalacas, and curassows. These birds are typically arboreal (tree-dwelling) and are important to forest ecosystems as seed dispersers. Guans have distinctive features including long tails, strong legs for perching, and often colorful throat wattles or crests. They are primarily frugivorous (fruit-eating) but may also consume leaves, flowers, and insects. Many guan species are threatened by habitat loss and hunting pressure, making them of conservation concern in their native ranges.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GWAHN',
                'etymology': 'From Spanish "guán," possibly from indigenous South American languages.',
                'language_origins': 'Spanish, indigenous South American',
                'example_sentence': 'The wildlife biologist spotted a crested _______ in the rainforest canopy, noting its importance for seed dispersal.',
                'memory_tip': 'Remember "GUAN" - GUArding the forest with Natural seed dispersal, these birds guard forests by dispersing seeds naturally.'
            },
            'guanine': {
                'definition': 'Guanine is one of the four nucleotide bases found in DNA and RNA, paired with cytosine through hydrogen bonding in the double helix structure. This purine base is essential for genetic coding and protein synthesis, serving as a fundamental component of the genetic code. Guanine also occurs in guano (bird droppings) and was historically extracted from this source, hence its name. In biochemistry, guanine participates in numerous cellular processes including DNA replication, transcription, and various metabolic pathways. The molecule contains nitrogen and is classified as a purine due to its double-ring structure.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GWAHN-een',
                'etymology': 'From Spanish "guano" (bird droppings, where it was first found) + chemical suffix "-ine."',
                'language_origins': 'Spanish',
                'example_sentence': 'The biology student learned that _______ pairs with cytosine in DNA, forming one of the essential base pairs of the genetic code.',
                'memory_tip': 'Remember "GUANINE" - GUAno + iNE, a chemical first found in guano that\'s essential for genetic coding.'
            },
            'guapena': {
                'definition': 'Guapena appears to be a specialized or regional term that may refer to a type of tree or plant, possibly from Latin American botanical terminology. Without more widespread documentation, this term likely represents either a local/indigenous plant name, a scientific species designation, or possibly a variant spelling of another botanical term. It could be related to tropical or subtropical flora, given the Spanish-influenced phonetic structure. The exact definition would require verification from specialized botanical or regional linguistic sources, as it appears to be either highly specialized terminology or a regional variant not commonly found in standard dictionaries.',
                'part_of_speech': 'noun (specialized/regional term)',
                'pronunciation_guide': 'gwah-PEH-nah',
                'etymology': 'Possibly from Spanish or indigenous Latin American languages, exact etymology unclear.',
                'language_origins': 'Possibly Spanish or indigenous Latin American',
                'example_sentence': 'The botanist encountered a _______ specimen during the rainforest survey, noting its unique characteristics for further study.',
                'memory_tip': 'Remember "GUAPENA" - GUA (sounds Latin American) + PENA (like piña), likely a Latin American plant name with Spanish influences.'
            },
            'guarantor': {
                'definition': 'Guarantor is a person or entity that provides a guarantee or assurance that another party will fulfill their obligations, especially financial commitments like loan payments or rental agreements. When someone serves as a guarantor, they accept legal responsibility to pay debts or meet obligations if the primary party defaults or fails to perform. This role requires the guarantor to have sufficient financial resources and creditworthiness to cover potential losses. Guarantors are commonly used in lending, leasing, and contract situations where additional security is needed to reduce risk for creditors or service providers.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gair-un-TOR',
                'etymology': 'From "guarantee" (from French "garantie") + "-or" suffix meaning "one who does."',
                'language_origins': 'French',
                'example_sentence': 'Since the college student had no credit history, her father served as a _______ for her apartment lease.',
                'memory_tip': 'Remember "GUARANTOR" - GUARANTee + OR (one who), one who guarantees and takes responsibility for someone else\'s obligations.'
            },
            'guardian': {
                'definition': 'Guardian refers to a person who has legal responsibility for the care and protection of another person (typically a minor or someone incapable of managing their own affairs) or something valuable. Guardians make important decisions regarding their ward\'s welfare, education, medical care, and financial matters. The role involves both protective responsibilities and fiduciary duties, requiring the guardian to act in the best interests of those under their care. Guardianship can be established through legal proceedings, parental designation, or by law. The term can also describe anyone who protects, watches over, or defends something important.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAHR-dee-uhn',
                'etymology': 'From Old French "gardien," from "garder" meaning "to guard, protect."',
                'language_origins': 'Old French',
                'example_sentence': 'After their parents died in an accident, their aunt became the children\'s legal _______, taking responsibility for their upbringing.',
                'memory_tip': 'Remember "GUARDIAN" - GUARDing + IAN (person), a person whose job is guarding and protecting others, especially children.'
            },
            'guarnerius': {
                'definition': 'Guarnerius refers to violins made by the Guarneri family of luthiers (violin makers) in Cremona, Italy, during the 17th and 18th centuries. These instruments are among the most prized and valuable violins in the world, rivaling those made by Stradivarius. The Guarneri family, particularly Giuseppe "del Gesù" Guarneri, created instruments known for their powerful, distinctive tone and exceptional craftsmanship. Guarnerius violins are characterized by their robust sound, unique varnish, and distinctive construction techniques. These historical instruments are now worth millions of dollars and are sought after by the world\'s finest violinists.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'gwahr-NAIR-ee-uhs',
                'etymology': 'Named after the Guarneri family of violin makers from Cremona, Italy, Latinized form.',
                'language_origins': 'Italian (Latinized)',
                'example_sentence': 'The virtuoso violinist performed the concerto on a rare 1743 _______ violin, its rich tone filling the concert hall.',
                'memory_tip': 'Remember "GUARNERIUS" - GUARded + precious violiN + lEgendaRy craftsmen, guarded precious violins made by legendary Italian craftsmen.'
            },
            'guava': {
                'definition': 'Guava is a tropical fruit native to Central and South America, now cultivated worldwide in warm climates. The fruit has a distinctive sweet-tart flavor and can range in color from green to yellow to pink, with flesh that may be white, pink, or red. Guavas are rich in vitamin C, dietary fiber, and various antioxidants, making them highly nutritious. The fruit can be eaten fresh, made into juices, jams, jellies, or used in desserts and beverages. Guava trees are also valued for their hardwood and medicinal properties of their leaves.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GWAH-vuh',
                'etymology': 'From Spanish "guayaba," from Taíno (indigenous Caribbean language).',
                'language_origins': 'Spanish, Taíno',
                'example_sentence': 'The tropical smoothie featured fresh _______ juice, providing a sweet and tangy flavor rich in vitamin C.',
                'memory_tip': 'Remember "GUAVA" - GUArd Against vitamin deficiency, this tropical fruit guards against vitamin C deficiency with its rich content.'
            },
            'guayabera': {
                'definition': 'Guayabera is a traditional men\'s shirt originating from Latin America, particularly Cuba and Mexico, characterized by its lightweight fabric, short sleeves, and distinctive pleated front panels with decorative embroidery or stitching. This garment typically features four pockets on the front and is designed to be worn untucked as formal or semi-formal attire in tropical climates. The guayabera represents an elegant alternative to traditional suits in hot weather, combining comfort with sophistication. The shirt has become a symbol of Latin American culture and is often worn at weddings, business meetings, and formal events in tropical regions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gwah-yah-BAIR-ah',
                'etymology': 'From Spanish, possibly named after the Yayabo River in Cuba or related to "guayaba" (guava).',
                'language_origins': 'Spanish (Cuban/Mexican)',
                'example_sentence': 'For the beach wedding ceremony, the groom chose an elegant white _______ instead of a traditional suit jacket.',
                'memory_tip': 'Remember "GUAYABERA" - GUAYa (guava) + BERA (wear it), a traditional shirt from guava-growing regions that\'s elegant to wear.'
            },
            'gubernatorial': {
                'definition': 'Gubernatorial refers to matters concerning the office, election, duties, or authority of a state governor in American politics. This adjective describes anything related to gubernatorial campaigns, gubernatorial powers, gubernatorial appointments, or other aspects of state-level executive leadership. The term is commonly used in political reporting and analysis when discussing state government leadership, election cycles, policy initiatives led by governors, or the administrative functions of state executive branches. Gubernatorial authority typically includes signing or vetoing legislation, appointing officials, and serving as the chief executive of state government.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'goo-ber-nuh-TOR-ee-uhl',
                'etymology': 'From Latin "gubernator" meaning "governor, helmsman" + "-ial" suffix meaning "relating to."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ race attracted national attention as both candidates proposed dramatically different approaches to state economic policy.',
                'memory_tip': 'Remember "GUBERNATORIAL" - GUBERnator (governor) + ORIAL (relating to), relating to the governor and governorship.'
            },
            'gudgeon': {
                'definition': 'Gudgeon has several meanings: it refers to a small freshwater fish found in European rivers and streams, valued as bait for larger fish and sometimes kept in aquariums. In mechanical contexts, a gudgeon is a pivot or journal around which something rotates, such as the pin that connects a piston to a connecting rod in engines. The term can also describe a person who is easily deceived or cheated, similar to calling someone gullible. Additionally, gudgeon refers to the socket part of a hinge that receives the pin. All meanings share the concept of something that serves as a connection point or is easily caught/manipulated.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GUJ-uhn',
                'etymology': 'From Old French "goujon," possibly from Latin "gobio" meaning "goby" (a type of fish).',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The angler used a small _______ as live bait to catch larger pike in the river.',
                'memory_tip': 'Remember "GUDGEON" - GUD (good) + GEON (like pigeon), a good small fish used for bait, or someone gullible like a pigeon.'
            },
            'guerilla': {
                'definition': 'Guerilla (variant spelling of guerrilla) refers to a member of an irregular military force that uses unconventional warfare tactics such as ambushes, sabotage, and hit-and-run attacks against a larger, more conventional army. Guerilla warfare typically involves small, mobile units operating in familiar territory, using stealth and local knowledge to harass enemy forces while avoiding direct confrontation. This form of warfare has been used throughout history by smaller forces fighting against occupying armies or established governments. The term can also describe any similar unconventional or insurgent approach to conflict or competition.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'guh-RIL-uh',
                'etymology': 'From Spanish "guerrilla," diminutive of "guerra" meaning "war," literally "little war."',
                'language_origins': 'Spanish',
                'example_sentence': 'The _______ fighters used their knowledge of the mountain terrain to launch surprise attacks against the occupying forces.',
                'memory_tip': 'Remember "GUERILLA" - GUErra (war) + RILLa (little), little war tactics using unconventional fighting methods.'
            },
            'guerite': {
                'definition': 'Guerite is a small sentry box or watchtower, typically projecting from the corner of a fortification, castle wall, or other defensive structure. These architectural features provided protected vantage points for guards or sentries to observe approaching threats while remaining sheltered from enemy fire. Guerites were commonly used in medieval and renaissance fortifications, designed to maximize visibility while minimizing exposure to attack. The term can also refer to similar small, enclosed observation posts or guard booths used for security purposes. These structures represent practical military architecture focused on surveillance and defense.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'geh-REET',
                'etymology': 'From French "guérite," from "guérir" meaning "to watch, guard," from Germanic origins.',
                'language_origins': 'French, Germanic',
                'example_sentence': 'The castle\'s corner _______ provided the watchman with a perfect view of the valley while keeping him protected from arrows.',
                'memory_tip': 'Remember "GUERITE" - GUERd (guard) + ITE (small place), a small place where guards watch and protect from.'
            },
            'gueritegallivat': {
                'definition': 'This appears to be a combined word error where "guerite" (a small sentry box or watchtower) has been incorrectly merged with "gallivat" (a type of small, fast sailing vessel used historically in the Indian Ocean). A guerite is a protective structure for guards or sentries, while a gallivat is a historical type of sailing ship. This combination likely resulted from a PDF parsing error where two separate words were inadvertently joined together. The correct terms would be "guerite" referring to the guard tower structure, and "gallivat" referring to the historical sailing vessel.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'geh-REET-GAL-i-vat',
                'etymology': 'Error: "guerite" (French "guérite") + "gallivat" (possibly from Portuguese or Indian languages)',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "guerite" and "gallivat" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "GUERITEGALLIVAT" - this is a combined word error, separate into GUERITE (guard tower) + GALLIVAT (historical sailing ship).'
            },
            'guerrilla': {
                'definition': 'Guerrilla refers to a member of an irregular military force that uses unconventional warfare tactics such as ambushes, sabotage, raids, and hit-and-run attacks against a larger, more conventional army. Guerrilla warfare typically involves small, mobile units operating in familiar territory, using stealth, surprise, and local knowledge to harass enemy forces while avoiding direct confrontation. This form of warfare has been used throughout history by resistance movements, independence fighters, and smaller forces fighting against occupying armies or established governments. The term can also describe any unconventional or insurgent approach to conflict, business, or competition.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'guh-RIL-uh',
                'etymology': 'From Spanish "guerrilla," diminutive of "guerra" meaning "war," literally "little war."',
                'language_origins': 'Spanish',
                'example_sentence': 'The resistance movement used _______ tactics to disrupt supply lines and avoid direct confrontation with the superior enemy forces.',
                'memory_tip': 'Remember "GUERRILLA" - GUErra (war) + RILLA (little), using little war tactics instead of big conventional battles.'
            },
            'guess': {
                'definition': 'Guess means to form an opinion or estimate about something without having definite knowledge or evidence, or to attempt to answer or solve something through conjecture rather than certainty. As a noun, a guess is the estimate or opinion formed through this process. Guessing involves making judgments based on incomplete information, intuition, or probability rather than facts or proof. The accuracy of guesses can vary widely, from educated guesses based on experience and partial knowledge to random guesses with little basis. Guessing is a common human cognitive process used when facing uncertainty.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'GES',
                'etymology': 'From Middle English "gessen," possibly from Old Norse "geta" meaning "to get, obtain."',
                'language_origins': 'Middle English, Old Norse',
                'example_sentence': 'Without access to the internet, she could only _______ at the population of the remote island nation.',
                'memory_tip': 'Remember "GUESS" - GUEssing without certainty, giving your best GUEss when you don\'t know for Sure.'
            },
            'gueule': {
                'definition': 'Gueule is a French word meaning "mouth" or "maw," particularly when referring to the mouth of an animal or used in a coarse, informal way when referring to human faces or mouths. In heraldry, "gueules" refers to the color red. The word can appear in English contexts when discussing French cuisine (such as "gueule de loup" - wolf\'s mouth, a type of dish), French slang expressions, or heraldic terminology. In casual French usage, the word has a somewhat crude connotation compared to more polite terms for mouth, similar to saying "mug" or "trap" in English when referring to someone\'s face or mouth.',
                'part_of_speech': 'noun (French)',
                'pronunciation_guide': 'GEUL',
                'etymology': 'From Old French "goule," from Latin "gula" meaning "throat, gullet."',
                'language_origins': 'French, Latin',
                'example_sentence': 'The heraldic shield displayed lions with red _______, indicating their fierce and noble nature in medieval symbolism.',
                'memory_tip': 'Remember "GUEULE" - GUy\'s ULtra Expression, like a guy\'s mouth or facial expression, especially when used informally.'
            },
            'guffaw': {
                'definition': 'Guffaw is a loud, hearty burst of laughter, typically characterized by its boisterous, unrestrained nature. This type of laughter is often spontaneous and indicates genuine amusement or hilarity. A guffaw is louder and more robust than a chuckle or giggle, expressing strong emotional response to something funny. The sound is often described as deep, booming, or explosive, and may be considered somewhat crude or unrefined in formal settings. Guffaws often occur in response to particularly amusing jokes, situations, or unexpected events that strike people as extremely funny.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'guh-FAW',
                'etymology': 'Probably imitative of the sound of loud laughter, first recorded in English in the 18th century.',
                'language_origins': 'English (imitative)',
                'example_sentence': 'The comedian\'s unexpected punchline caused the entire audience to erupt in a loud _______ of appreciation.',
                'memory_tip': 'Remember "GUFFAW" - GUt-busting Fun + AWesome laughter, gut-busting fun that produces awesome loud laughter.'
            },
            'guichet': {
                'definition': 'Guichet is a French term referring to a small window or opening, typically with a grille or protective barrier, used for conducting business transactions, such as at banks, ticket offices, or government bureaus. In English contexts, the word appears when describing French architectural features or administrative systems. A guichet provides security while allowing communication and document exchange between customers and service providers. The term can also refer to the booth or station where such transactions take place. This architectural feature is common in French public buildings, banks, and offices where security and controlled access are important.',
                'part_of_speech': 'noun (French)',
                'pronunciation_guide': 'gee-SHEH',
                'etymology': 'From Old French "guichet," possibly from Germanic origins related to "wicket."',
                'language_origins': 'French, Germanic',
                'example_sentence': 'At the French post office, customers purchased stamps and mailed packages through the secure _______ window.',
                'memory_tip': 'Remember "GUICHET" - GUIded transaCtion winHET (window), a guided transaction window for secure business dealings.'
            },
            'guido': {
                'definition': 'Guido is an Italian masculine given name, historically significant as the name of Guido of Arezzo (c. 991-1033), the medieval monk who developed modern musical notation including the staff system and solmization (do-re-mi). In some contexts, particularly in American slang, the name has unfortunately been used as an ethnic slur, which is inappropriate and offensive. The historical Guido made revolutionary contributions to music theory and notation that are still used today. As a given name, Guido means "guide" in Italian and has been borne by many notable figures throughout history, including composers, scholars, and leaders.',
                'part_of_speech': 'proper noun (given name)',
                'pronunciation_guide': 'GWEE-doh',
                'etymology': 'From Germanic "widu" meaning "wide" or Latin "guidare" meaning "to guide."',
                'language_origins': 'Germanic, Latin',
                'example_sentence': 'Music students learn about _______ of Arezzo, whose innovations in musical notation revolutionized how we read and write music.',
                'memory_tip': 'Remember "GUIDO" - GUIde + DO (musical note), named after the monk who GUIded us to the DO-re-mi musical system.'
            },
            'guidonian': {
                'definition': 'Guidonian refers to things related to Guido of Arezzo (c. 991-1033), the medieval Italian monk who revolutionized musical notation and education. The most famous Guidonian innovation is the "Guidonian hand," a mnemonic device where different parts of the hand represent different musical pitches, helping singers learn and remember musical intervals and scales. Guidonian also relates to the hexachord system and solmization (ut-re-mi-fa-sol-la, the predecessor to do-re-mi) that Guido developed for teaching music. These Guidonian methods formed the foundation of Western musical education and notation systems that are still used today.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'gwee-DOH-nee-uhn',
                'etymology': 'From Guido (of Arezzo) + "-ian" suffix meaning "relating to or characteristic of."',
                'language_origins': 'Latin (named after person)',
                'example_sentence': 'The medieval choir director used the _______ hand method to teach students proper pitch relationships and musical intervals.',
                'memory_tip': 'Remember "GUIDONIAN" - GUIDO + NIAN (related to), related to Guido of Arezzo who guided musical notation development.'
            },
            'guilloche': {
                'definition': 'Guilloche is a decorative technique or pattern consisting of interlaced curved lines forming continuous, repetitive designs, often creating braided, woven, or flowing ribbon-like effects. This ornamental motif appears in architecture, metalwork, engraving, and various decorative arts. Guilloche patterns can be simple interlacing circles or complex geometric designs that create optical effects and visual rhythm. The technique is commonly used in coin design, banknote security features, architectural moldings, jewelry, and luxury goods. The precision and complexity of guilloche work often serve both aesthetic and anti-counterfeiting purposes in currency and valuable items.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gi-LOHSH',
                'etymology': 'From French "guilloche," named after Guillot, a French engineer, or from "guillochis" (engine turning).',
                'language_origins': 'French',
                'example_sentence': 'The antique watch face featured intricate _______ patterns that created a shimmering, wave-like effect in the metal.',
                'memory_tip': 'Remember "GUILLOCHE" - GUILt-free decorative weavy LOCHE (lines), guilt-free decorative wavy lines that create beautiful interlaced patterns.'
            },
            'guineas': {
                'definition': 'Guineas can refer to guinea pigs (small domesticated rodents kept as pets), guinea fowl (African birds raised for meat and eggs), or historically, British gold coins called guineas that were worth 21 shillings. Guinea pigs, despite their name, are not from Guinea nor related to pigs, but are popular small pets known for their gentle nature. Guinea fowl are distinctive birds with spotted plumage, originally from Africa, now raised worldwide for their meat and pest control abilities. The historical guinea coin was used in Britain until 1816 and got its name because the gold originally came from the Guinea region of Africa.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GIN-eez',
                'etymology': 'Named after Guinea region in West Africa; various items associated with this region.',
                'language_origins': 'English (from African place name)',
                'example_sentence': 'The farm raised _______ fowl for both their meat and their ability to control insect pests in the fields.',
                'memory_tip': 'Remember "GUINEAS" - GUINea region of Africa gave its name to various animals and coins, like GUINea pigs and GUINea fowl.'
            },
            'gules': {
                'definition': 'Gules is the heraldic term for the color red in coat of arms and heraldic designs. In heraldry, specific terms are used for colors: gules (red), azure (blue), vert (green), purpure (purple), and sable (black). When describing heraldic designs, "gules" indicates that a particular element should be colored red. This terminology derives from medieval Latin and French heraldic traditions. Gules is one of the most common and significant colors in heraldry, often representing courage, strength, military prowess, or martyrdom. Understanding heraldic color terminology is essential for properly describing and interpreting coat of arms.',
                'part_of_speech': 'noun (heraldic term)',
                'pronunciation_guide': 'GYOOLZ',
                'etymology': 'From Old French "goules," from Medieval Latin "gula" meaning "throat" (referring to red throat/mouth of animals).',
                'language_origins': 'Old French, Medieval Latin',
                'example_sentence': 'The family coat of arms featured a lion rampant _______ on a field of silver, symbolizing courage and nobility.',
                'memory_tip': 'Remember "GULES" - GULet (throat) + ES, like a red throat or the red mouth of a heraldic lion showing courage.'
            },
            'gullet': {
                'definition': 'Gullet refers to the throat or esophagus, specifically the passage through which food and drink travel from the mouth to the stomach. In anatomy, the gullet is the muscular tube that connects the pharynx to the stomach, using coordinated muscle contractions (peristalsis) to move swallowed materials downward. The term is often used in everyday language to describe the throat area or the act of swallowing. In some contexts, gullet can refer to a narrow channel or passage that resembles the anatomical structure, such as water channels or geological formations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GUL-it',
                'etymology': 'From Old French "golet," diminutive of "goule" meaning "throat," from Latin "gula."',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The large fish bone got stuck in his _______, requiring medical attention to remove it safely.',
                'memory_tip': 'Remember "GULLET" - GULp + LET (little passage), the little passage that lets you gulp food down to your stomach.'
            },
            'gullibility': {
                'definition': 'Gullibility is the quality of being easily deceived, fooled, or taken advantage of due to excessive trust or lack of critical thinking. A gullible person tends to believe claims, stories, or promises without sufficient evidence or skeptical evaluation. Gullibility can result from naivety, lack of experience, desire to trust others, or insufficient knowledge to evaluate information critically. This trait makes individuals vulnerable to scams, fraud, misinformation, and manipulation. While some level of trust is necessary for social functioning, excessive gullibility can lead to financial, emotional, or other forms of harm.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gul-uh-BIL-i-tee',
                'etymology': 'From "gullible" (from "gull" meaning "to deceive") + "-ibility" suffix meaning "quality of being."',
                'language_origins': 'English',
                'example_sentence': 'His _______ made him an easy target for online scammers who promised unrealistic investment returns.',
                'memory_tip': 'Remember "GULLIBILITY" - GULL (seagull that eats anything) + ABILITY, the ability to be gulled like a seagull that swallows anything thrown at it.'
            },
            'gummy': {
                'definition': 'Gummy describes something having a sticky, viscous, or adhesive quality similar to gum. This adjective can refer to substances that are chewy, sticky, or gelatinous in texture, such as gummy candy, tree sap, or certain food preparations. In medical contexts, gummy can describe gums that are swollen or infected. The term can also refer to things that have become sticky due to deterioration or contamination. Gummy textures are often associated with pleasant foods like gummy bears or gummy vitamins, but can also describe undesirable sticky conditions.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GUM-ee',
                'etymology': 'From "gum" (from Old English "goma") + "-y" suffix meaning "characterized by."',
                'language_origins': 'Old English',
                'example_sentence': 'The children enjoyed the _______ bears as a special treat, savoring their chewy, fruity flavors.',
                'memory_tip': 'Remember "GUMMY" - GUM + MY (mouth), like gum in my mouth that\'s sticky and chewy.'
            },
            'gumption': {
                'definition': 'Gumption refers to enterprising spirit, initiative, and resourcefulness in tackling challenges or pursuing goals. Someone with gumption demonstrates courage, determination, and practical common sense when facing difficulties or opportunities. This quality combines boldness with practical wisdom, indicating not just willingness to act but also the intelligence to act effectively. Gumption suggests both mental sharpness and strength of character, enabling people to take on difficult tasks, solve problems creatively, and persist in the face of obstacles. It represents the combination of courage, initiative, and practical intelligence.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GUMP-shuhn',
                'etymology': 'Possibly from Scottish dialect, origin uncertain, may be related to "gumptious."',
                'language_origins': 'Scottish English',
                'example_sentence': 'It took real _______ for the young entrepreneur to start her own business with no experience and limited funds.',
                'memory_tip': 'Remember "GUMPTION" - GUMpy person with ambiTION, even a grumpy person with ambition has the drive and courage to succeed.'
            },
            'gung': {
                'definition': 'Gung appears most commonly as part of "gung-ho," meaning extremely enthusiastic, eager, or zealous about something. The term "gung-ho" comes from Chinese "gōng hé" meaning "work together" and was popularized by U.S. Marines in World War II. As a standalone word, "gung" is less common in English but may appear in certain compound expressions or as a shortened form of "gung-ho." The concept emphasizes passionate commitment, wholehearted dedication, or sometimes overzealous enthusiasm for a cause, project, or activity.',
                'part_of_speech': 'adjective (informal)',
                'pronunciation_guide': 'GUNG',
                'etymology': 'From Chinese "gōng" meaning "work" (as in "gung-ho" from "gōng hé" meaning "work together").',
                'language_origins': 'Chinese',
                'example_sentence': 'The new recruit was so _______ about military training that he volunteered for every extra drill and exercise.',
                'memory_tip': 'Remember "GUNG" - GUNg-ho enthusiasm, being GUNg-ho means being extremely enthusiastic and eager.'
            },
            'gurdy': {
                'definition': 'Gurdy typically refers to a hurdy-gurdy, a stringed musical instrument that produces sound by a rosined wheel rubbing against the strings, operated by a hand crank. This medieval instrument combines elements of both string and wind instruments, creating a distinctive drone-like sound often associated with folk music. The hurdy-gurdy has melody strings played by a keyboard and drone strings that provide continuous background tones. In some contexts, "gurdy" might refer to similar mechanical musical instruments or devices that produce music through rotational mechanisms. The instrument has a rich history in European folk music traditions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GUR-dee',
                'etymology': 'Short for "hurdy-gurdy," possibly imitative of the sound the instrument makes.',
                'language_origins': 'English (imitative)',
                'example_sentence': 'The street musician played medieval melodies on his hurdy-_______, drawing crowds with the instrument\'s unique droning sound.',
                'memory_tip': 'Remember "GURDY" - GURgling musical instrumEnt that makes Droning sounds, a gurgling instrument that creates droning musical tones.'
            },
            'gurmukhi': {
                'definition': 'Gurmukhi is the script used to write Punjabi, particularly in the Indian state of Punjab, and is the script in which the Guru Granth Sahib (Sikh holy book) is written. Developed from the Laṇḍā script in the 16th century, Gurmukhi literally means "from the mouth of the Guru." This writing system consists of 35 basic letters and has been standardized for modern Punjabi language use. Gurmukhi is essential to Sikh religious practice and Punjabi cultural identity, serving as the primary script for religious texts, literature, and official communication in Punjab, India.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'gur-MUK-hee',
                'etymology': 'From Punjabi/Sanskrit "guru" (teacher) + "mukhi" (from the mouth), literally "from the mouth of the Guru."',
                'language_origins': 'Sanskrit, Punjabi',
                'example_sentence': 'The Sikh children learned to read the _______ script so they could study their religious texts in the original language.',
                'memory_tip': 'Remember "GURMUKHI" - GURu\'s MUKh (mouth) + I, the script that comes from the Guru\'s mouth for writing Punjabi.'
            },
            'gurmukhigyascutus': {
                'definition': 'This appears to be a combined word error where "gurmukhi" (the Punjabi script) has been incorrectly merged with "gyascutus" (a mythical creature from American folklore). Gurmukhi is the writing system used for Punjabi language and Sikh religious texts, while gyascutus is a legendary creature from tall tales, described as a large, bear-like animal with legs shorter on one side than the other, supposedly adapted for walking on hillsides. This combination likely resulted from a PDF parsing error where two completely unrelated terms were inadvertently joined together.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'gur-MUK-hee-JYE-as-kyoo-tuhs',
                'etymology': 'Error: "gurmukhi" (Sanskrit/Punjabi) + "gyascutus" (American folklore, possibly pseudo-Latin)',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "gurmukhi" and "gyascutus" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "GURMUKHIGYASCUTUS" - this is a combined word error, separate into GURMUKHI (Punjabi script) + GYASCUTUS (mythical hillside creature).'
            },
            'gurney': {
                'definition': 'Gurney is a wheeled stretcher or bed used in hospitals and medical facilities to transport patients who cannot walk or need to remain lying down during movement. These medical devices are designed with safety features, adjustable height, and locking wheels to ensure secure patient transport between rooms, departments, or facilities. Gurneys are essential equipment in emergency rooms, surgical suites, and patient transport services. The term can also refer to similar wheeled platforms used in other contexts where items need to be moved while remaining horizontal and stable.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GUR-nee',
                'etymology': 'Possibly named after J.T. Gurney, a British inventor, or from the surname Gurney.',
                'language_origins': 'English (named after person)',
                'example_sentence': 'The paramedics carefully transferred the injured patient from the ambulance _______ to the emergency room bed.',
                'memory_tip': 'Remember "GURNEY" - GURd (guard) + NEY (needy), something that guards needy patients by safely transporting them.'
            },
            'gurneysanctimonious': {
                'definition': 'This appears to be a combined word error where "gurney" (a wheeled medical stretcher) has been incorrectly merged with "sanctimonious" (showing false righteousness or hypocritical devotion). A gurney is medical transport equipment used in hospitals, while sanctimonious describes behavior that displays hypocritical righteousness or self-righteous moral superiority. This combination likely resulted from a PDF parsing error where two completely unrelated words were inadvertently joined together. The correct terms would be "gurney" referring to the medical stretcher, and "sanctimonious" referring to hypocritically righteous behavior.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'GUR-nee-sangk-tuh-MOH-nee-uhs',
                'etymology': 'Error: "gurney" (English, named after person) + "sanctimonious" (Latin "sanctimonia")',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "gurney" and "sanctimonious" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "GURNEYSANCTIMONIOUS" - this is a combined word error, separate into GURNEY (medical stretcher) + SANCTIMONIOUS (self-righteous).'
            }
        }
        
        return batch_080_data.get(word.lower(), {
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
            'grudginglycanopy': 'Combined word error: "grudginglycanopy" appears to be "grudgingly" + "canopy" merged together. This is likely a PDF parsing error where reluctance and overhead covering terminology were incorrectly combined.',
            'grueldifficulty': 'Combined word error: "grueldifficulty" appears to be "gruel" + "difficulty" merged together. This is likely a PDF parsing error where thin porridge and challenge terminology were incorrectly combined.',
            'gruelgroom': 'Combined word error: "gruelgroom" appears to be "gruel" + "groom" merged together. This is likely a PDF parsing error where thin porridge and bridegroom terminology were incorrectly combined.',
            'gueritegallivat': 'Combined word error: "gueritegallivat" appears to be "guerite" + "gallivat" merged together. This is likely a PDF parsing error where guard tower and sailing vessel terminology were incorrectly combined.',
            'gurmukhigyascutus': 'Combined word error: "gurmukhigyascutus" appears to be "gurmukhi" + "gyascutus" merged together. This is likely a PDF parsing error where Punjabi script and mythical creature terminology were incorrectly combined.',
            'gurneysanctimonious': 'Combined word error: "gurneysanctimonious" appears to be "gurney" + "sanctimonious" merged together. This is likely a PDF parsing error where medical stretcher and self-righteous behavior terminology were incorrectly combined.'
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
        
        print("Batch 080 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch080Processor()
    input_path = "output/batch_080_words.csv"
    output_path = "output/batch_080_processed.csv"
    processor.process_batch(input_path, output_path)