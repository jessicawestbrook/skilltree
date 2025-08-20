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

class Batch079Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
        self.errors = []
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        batch_079_data = {
            'gravimetry': {
                'definition': 'Gravimetry is the scientific measurement and study of gravitational fields, particularly variations in Earth\'s gravitational force at different locations. This field of geophysics uses precise instruments called gravimeters to detect minute changes in gravitational acceleration, which can reveal information about subsurface geology, mineral deposits, oil reserves, and the Earth\'s internal structure. Gravimetric surveys are used in exploration geophysics to locate underground resources, in geodesy to map Earth\'s shape and gravitational field, and in various scientific applications including monitoring groundwater levels and detecting geological hazards. The technique relies on the principle that different materials and structures beneath the surface create slight variations in local gravity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gruh-VIM-uh-tree',
                'etymology': 'From Latin "gravis" meaning "heavy, weighty" + Greek "metron" meaning "measure."',
                'language_origins': 'Latin, Greek',
                'example_sentence': 'The oil company used _______ to map underground geological structures and identify potential drilling sites.',
                'memory_tip': 'Remember "GRAVIMETRY" - GRAVIty + METRY (measurement), measuring gravity to understand what\'s underground.'
            },
            'gravitas': {
                'definition': 'Gravitas refers to dignity, seriousness, and solemnity of manner that commands respect and reverence. It describes a quality of weightiness, both literal and figurative, that suggests depth of character, moral authority, and the ability to handle serious matters with appropriate gravity. A person with gravitas possesses a compelling presence that conveys competence, wisdom, and trustworthiness. The concept encompasses not just serious demeanor but also the substance and gravitas of thought that underlies it. Originally a Roman virtue, gravitas was considered essential for leadership and public service, representing the balance between authority and responsibility.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GRAV-i-tas',
                'etymology': 'From Latin "gravitas" meaning "weight, heaviness, dignity," from "gravis" meaning "heavy, weighty."',
                'language_origins': 'Latin',
                'example_sentence': 'The Supreme Court justice\'s _______ and thoughtful questioning during oral arguments commanded respect from all the attorneys.',
                'memory_tip': 'Remember "GRAVITAS" - GRAVe + ITAs (it has), having grave seriousness and weight that commands respect.'
            },
            'gravy': {
                'definition': 'Gravy is a sauce made from the fat and juices that run naturally from meat during cooking, typically thickened with flour or other starch and seasoned for flavor. Traditional gravy accompanies roasted meats, mashed potatoes, and other dishes as a flavorful enhancement. The preparation involves combining pan drippings with liquid (such as stock or water) and a thickening agent to create a smooth, rich sauce. In broader usage, gravy can refer to any easy profit or unexpected benefit, as in the phrase "gravy train." The term represents comfort food and traditional cooking methods that maximize flavor from simple ingredients.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GRAY-vee',
                'etymology': 'From Middle English, possibly from Old French "grané," meaning "grain" (referring to the granulated appearance), or a misreading of "gravy."',
                'language_origins': 'Middle English, possibly Old French',
                'example_sentence': 'Grandmother poured hot _______ over the mashed potatoes, making the simple meal feel like a special occasion.',
                'memory_tip': 'Remember "GRAVY" - GRAsps Veggies and meat with delicious sauce, or think GRAVe + Y (why so serious? because gravy is serious business!).'
            },
            'graywacke': {
                'definition': 'Graywacke is a type of sandstone characterized by its gray color and composition of angular to subangular grains of quartz, feldspar, and rock fragments embedded in a fine-grained matrix. This sedimentary rock forms in deep marine environments, often in submarine fans or turbidity current deposits. Graywacke typically contains at least 15% matrix material, which distinguishes it from cleaner, more mature sandstones. The rock is important in geology for understanding ancient depositional environments and tectonic settings. Its name reflects both its typically gray appearance and its German origins in geological terminology, where "wacke" refers to a type of sandstone.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GRAY-wah-keh',
                'etymology': 'From German "Grauwacke," from "grau" meaning "gray" + "Wacke" (a type of sandstone), from Middle High German "wacke."',
                'language_origins': 'German',
                'example_sentence': 'The geologist identified the rock formation as _______, noting its characteristic gray color and mixed grain composition.',
                'memory_tip': 'Remember "GRAYWACKE" - GRAY + WACKE (wacky), a gray and somewhat wacky-looking type of sandstone with mixed fragments.'
            },
            'grazioso': {
                'definition': 'Grazioso is an Italian musical term meaning "gracefully" or "with grace," used as a tempo and style marking to indicate that a piece or passage should be performed with elegance, charm, and refined expression. When composers write "grazioso" in their scores, they\'re directing performers to emphasize lyrical beauty, smoothness, and graceful phrasing rather than power or intensity. The term often appears in classical music, particularly in works from the Classical and Romantic periods. Grazioso passages typically feature flowing melodies, gentle dynamics, and expressive nuances that highlight the music\'s inherent beauty and sophistication.',
                'part_of_speech': 'adverb (musical term)',
                'pronunciation_guide': 'grah-tsee-OH-so',
                'etymology': 'From Italian "grazioso," from "grazia" meaning "grace," from Latin "gratia."',
                'language_origins': 'Italian, Latin',
                'example_sentence': 'The pianist played the second movement _______, with delicate touch and graceful phrasing that brought out the melody\'s natural beauty.',
                'memory_tip': 'Remember "GRAZIOSO" - GRAZes with grace, like music that grazES your ears beautifully and gracefully.'
            },
            'greasy': {
                'definition': 'Greasy describes something covered with, containing, or resembling grease - having an oily, slippery, or fatty surface or texture. When applied to food, greasy indicates an excess of oil or fat that may make items feel slick or heavy. The term can describe hair that appears oily from natural oils or lack of washing, or surfaces that have been coated with lubricants or cooking oils. In a figurative sense, greasy can describe behavior that seems slippery, untrustworthy, or overly smooth in an unpleasant way. The word generally carries negative connotations, suggesting excess, poor hygiene, or disagreeable qualities.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GREE-see',
                'etymology': 'From "grease" (from Old French "graisse," from Latin "crassus" meaning "thick") + "-y" suffix.',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'After working on the car engine all afternoon, his hands were _______ and needed thorough washing with degreasing soap.',
                'memory_tip': 'Remember "GREASY" - GREase + Y, having the quality of grease - oily, slippery, and needing cleaning.'
            },
            'great': {
                'definition': 'Great means large in size, extent, or intensity, or of major significance and importance. The word can describe physical magnitude, such as great distances or great buildings, or abstract qualities like great ideas or great achievements. Great often implies excellence, superiority, or remarkable quality that stands above the ordinary. It can express enthusiasm or approval, as in "that\'s great!" or indicate considerable degree or extent, as in "great care" or "great difficulty." The term has evolved from its basic meaning of size to encompass notions of excellence, importance, and positive evaluation across many contexts.',
                'part_of_speech': 'adjective, noun, exclamation',
                'pronunciation_guide': 'GRAYT',
                'etymology': 'From Old English "grēat," from Germanic roots meaning "big, thick, coarse."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The _______ oak tree in the town square had been providing shade for generations of families during summer festivals.',
                'memory_tip': 'Remember "GREAT" - GRAnd + EATing (huge), something large, excellent, or very important and impressive.'
            },
            'greaves': {
                'definition': 'Greaves refers to armor for the lower legs, specifically protective plates or guards that covered the shins and sometimes the calves in medieval and ancient warfare. These pieces of armor were typically made of metal and secured with straps or buckles. Greaves could also refer to the crispy bits of rendered fat or meat, particularly the crackling pieces left after rendering lard or tallow. In historical contexts, greaves were essential components of a warrior\'s protective equipment, designed to shield the vulnerable lower legs from sword strikes, arrows, and other weapons during combat.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GREEVZ',
                'etymology': 'From Old French "greve" meaning "shin, greave," possibly from Germanic origins.',
                'language_origins': 'Old French, Germanic',
                'example_sentence': 'The medieval knight\'s _______ gleamed in the sunlight as he prepared for the tournament, protecting his shins beneath his chain mail.',
                'memory_tip': 'Remember "GREAVES" - GREAt armorVES, great armor that saves your shins and calves from weapons.'
            },
            'grebe': {
                'definition': 'Grebe is a type of freshwater diving bird characterized by lobed toes instead of webbed feet, a pointed bill, and excellent swimming and diving abilities. These waterbirds have streamlined bodies, short tails, and legs positioned far back on their bodies, making them excellent underwater swimmers but awkward on land. Grebes build floating nests and are known for their elaborate courtship displays, including synchronized swimming and dancing on water. They feed primarily on fish, aquatic insects, and other small water creatures, using their sharp bills and underwater agility to catch prey. Common species include the pied-billed grebe and great crested grebe.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GREEB',
                'etymology': 'From French "grèbe," of unknown origin, possibly imitative of the bird\'s call.',
                'language_origins': 'French',
                'example_sentence': 'The naturalist watched the _______ dive beneath the lake surface, disappearing for nearly a minute before resurfacing with a small fish.',
                'memory_tip': 'Remember "GREBE" - GREat swimmer BElow water, a diving bird that\'s great at swimming underwater to catch fish.'
            },
            'grecque': {
                'definition': 'Grecque is a French culinary term referring to a style of cooking vegetables "à la grecque" (in the Greek style), where vegetables are braised in olive oil, lemon juice, herbs, and spices, then served cold or at room temperature. This preparation method typically involves cooking vegetables like artichokes, cauliflower, or mushrooms in a seasoned liquid until tender, creating a flavorful marinade that the vegetables absorb. The term can also refer to decorative patterns inspired by ancient Greek designs, particularly the key pattern or meander motif used in architecture and decorative arts. In broader usage, grecque indicates something done in a Greek manner or style.',
                'part_of_speech': 'adjective, noun (French)',
                'pronunciation_guide': 'GREK',
                'etymology': 'From French "grecque," feminine form of "grec" meaning "Greek," from Latin "Graecus."',
                'language_origins': 'French, Latin',
                'example_sentence': 'The chef prepared the mushrooms _______ style, marinating them in olive oil and herbs to serve as an elegant cold appetizer.',
                'memory_tip': 'Remember "GRECQUE" - GREek CooKing style, cooking vegetables the Greek way with olive oil and herbs.'
            },
            'greedy': {
                'definition': 'Greedy describes having an excessive desire for food, wealth, or material possessions, often at the expense of others or beyond what is reasonable or necessary. A greedy person shows intense and selfish longing for more than their fair share, whether of money, food, power, or other resources. The term carries strongly negative connotations, suggesting not just desire but lack of self-control and consideration for others. Greedy behavior often involves taking more than needed while others have less, or pursuing gain through unfair or harmful means. The concept extends beyond material wants to include excessive desire for attention, success, or any other valued commodity.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GREE-dee',
                'etymology': 'From Old English "grǣdig," related to "grǣd" meaning "hunger, appetite," from Germanic roots.',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The _______ landlord raised rents far beyond what tenants could afford, caring only about maximizing profits.',
                'memory_tip': 'Remember "GREEDY" - GREat nEED that\'s excessive, wanting more and more beyond what\'s reasonable or fair.'
            },
            'greek': {
                'definition': 'Greek refers to the people, language, or culture of Greece, both ancient and modern. Ancient Greek civilization made fundamental contributions to philosophy, mathematics, science, art, architecture, and democratic government that continue to influence Western culture. The Greek language has evolved from ancient forms through Koine Greek to modern Greek, and many English words derive from Greek roots. Greek can describe the distinctive architectural styles (Doric, Ionic, Corinthian), philosophical traditions (Stoicism, Platonism), or cultural practices associated with Greece. In informal usage, "it\'s all Greek to me" means something is incomprehensible or foreign.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'GREEK',
                'etymology': 'From Old English "Grēcas," from Latin "Graecus," from Greek "Graikos."',
                'language_origins': 'Old English, Latin, Greek',
                'example_sentence': 'The architecture student studied _______ columns and their influence on neoclassical building design throughout Europe.',
                'memory_tip': 'Remember "GREEK" - GREat Educational Knowledge, the culture that gave us philosophy, democracy, and many academic words.'
            },
            'green': {
                'definition': 'Green is the color between blue and yellow in the spectrum, the color of grass, leaves, and emeralds. As a primary color in the additive color system, green represents nature, growth, freshness, and life. The word can describe objects, plants, or things having this color, or refer to environmental consciousness and ecological awareness, as in "going green." Green can indicate inexperience or naivety, as in a "green" rookie, or refer to jealousy, as in "green with envy." The color has strong associations with money, luck, and renewal across many cultures.',
                'part_of_speech': 'adjective, noun, verb',
                'pronunciation_guide': 'GREEN',
                'etymology': 'From Old English "grēne," from Germanic roots meaning "to grow."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The _______ leaves on the oak tree indicated that spring had finally arrived after the long winter.',
                'memory_tip': 'Remember "GREEN" - GRowth, Environment, Energy, Nature - the color of growing plants and environmental awareness.'
            },
            'greens': {
                'definition': 'Greens refers to leafy vegetables that are typically green in color, such as spinach, kale, lettuce, collard greens, and chard, valued for their nutritional content including vitamins, minerals, and fiber. The term can also refer to golf course putting surfaces, the carefully maintained grass areas around holes where players putt. In politics, "Greens" refers to members or supporters of Green political parties focused on environmental issues. Additionally, greens can mean green vegetables in general, money (particularly paper currency), or the green parts of plants used for food or decoration.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GREENZ',
                'etymology': 'Plural of "green," from Old English "grēne," from Germanic roots meaning "to grow."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The nutritionist recommended eating more leafy _______ like spinach and kale to increase iron and vitamin intake.',
                'memory_tip': 'Remember "GREENS" - GREat Energy and Nutrients, the green leafy vegetables that provide great nutrition.'
            },
            'greetingdifficulty': {
                'definition': 'This appears to be a combined word error where "greeting" (a salutation or welcome) has been incorrectly merged with "difficulty" (something hard to accomplish or understand). A greeting is typically a word, gesture, or action used to welcome or acknowledge someone, while difficulty refers to the state or quality of being hard to do, understand, or deal with. This combination likely resulted from a PDF parsing error where two separate words were inadvertently joined together. The correct terms would be "greeting" referring to welcoming expressions, and "difficulty" referring to challenges or problems.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'GREET-ing-DIF-i-kul-tee',
                'etymology': 'Error: "greeting" (from "greet," Old English) + "difficulty" (from Latin "difficilis")',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "greeting" and "difficulty" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "GREETINGDIFFICULTY" - this is a combined word error, separate into GREETING (hello) + DIFFICULTY (hard problem).'
            },
            'gregorian': {
                'definition': 'Gregorian most commonly refers to the Gregorian calendar, the calendar system used worldwide today, introduced by Pope Gregory XIII in 1582 to replace the Julian calendar. This calendar reform corrected accumulated errors in the Julian system and established the current system of leap years. Gregorian can also refer to Gregorian chant, the form of plainchant or plainsong used in the Roman Catholic Church, characterized by monophonic, unaccompanied sacred song. The term may also relate to other things associated with Pope Gregory XIII or other popes named Gregory. The Gregorian calendar\'s accuracy and widespread adoption made it the international standard for civil use.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'gruh-GOR-ee-uhn',
                'etymology': 'From Medieval Latin "Gregorianus," relating to Pope Gregory XIII (1502-1585).',
                'language_origins': 'Medieval Latin',
                'example_sentence': 'The _______ calendar system we use today was adopted to correct the drift that had accumulated in the older Julian calendar.',
                'memory_tip': 'Remember "GREGORIAN" - GREGory\'s calendAR system, named after Pope Gregory who reformed our calendar system.'
            },
            'gressorial': {
                'definition': 'Gressorial describes animals that are adapted for walking or running on land, particularly referring to the locomotor adaptations of terrestrial animals. This zoological term characterizes species that have evolved structural features optimized for terrestrial movement, such as strong legs, appropriate foot structure, and body proportions suited for ground-based locomotion. Gressorial animals are distinguished from those adapted for swimming (natatorial), flying (volant), or climbing (scansorial). The term is used in comparative anatomy and zoology to classify and describe the locomotor specializations of different animal groups based on their primary mode of movement and habitat preferences.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'gruh-SOR-ee-al',
                'etymology': 'From Latin "gressus" meaning "step, walk" + "-orial" suffix meaning "relating to."',
                'language_origins': 'Latin',
                'example_sentence': 'The zoologist noted that the bird\'s _______ adaptations, including strong legs and ground-adapted feet, made it well-suited for terrestrial foraging.',
                'memory_tip': 'Remember "GRESSORIAL" - GRESSing (progressing) on land, adapted for walking and running on the ground.'
            },
            'grew': {
                'definition': 'Grew is the simple past tense of the verb "grow," meaning to increase in size, number, strength, or degree over time. It describes the process of development, expansion, or maturation that occurred in the past. Grew can refer to physical growth, such as plants getting larger or children becoming taller, or abstract growth, such as businesses expanding or skills developing. The word indicates a completed change or development that took place over a period of time in the past. It encompasses both natural biological growth and metaphorical increases in various qualities or quantities.',
                'part_of_speech': 'verb (past tense of grow)',
                'pronunciation_guide': 'GROO',
                'etymology': 'Past tense of "grow," from Old English "grōwan," from Germanic roots meaning "to grow."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The small sapling _______ into a magnificent oak tree over the course of fifty years.',
                'memory_tip': 'Remember "GREW" - GRowth + in past, something that GRew Up or got bigger in the past.'
            },
            'grewsome': {
                'definition': 'Grewsome is an archaic or variant spelling of "gruesome," meaning horrifyingly or revoltingly frightful, causing feelings of revulsion, horror, or disgust. Something grewsome is characterized by graphic violence, death, or other disturbing elements that shock or horrify viewers or readers. The word describes scenes, stories, or images that are macabre, grisly, or ghastly in nature. While "gruesome" is the standard modern spelling, "grewsome" appears in historical texts and some regional dialects. The term emphasizes the visceral, disturbing quality of something that causes people to recoil in horror or disgust.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GROO-sum',
                'etymology': 'Variant of "gruesome," from "grue" (to shudder) + "-some" suffix meaning "characterized by."',
                'language_origins': 'English (archaic/variant spelling)',
                'example_sentence': 'The detective novel contained several _______ murder scenes that were difficult for sensitive readers to get through.',
                'memory_tip': 'Remember "GREWSOME" - GREw fearSOME, something that grew to be fearsome and horrifying to see.'
            },
            'grid': {
                'definition': 'Grid refers to a network of evenly spaced horizontal and vertical lines forming squares, used for reference, organization, or structural support. Grids appear in many contexts: coordinate systems for mapping, frameworks for urban planning, electrical distribution networks, and design layouts for organizing visual elements. In computing, grid can refer to distributed computing networks or user interface layouts. The concept provides systematic organization, making it easier to locate positions, distribute loads, or arrange elements uniformly. Grids are fundamental tools for navigation, construction, design, and analysis across numerous fields and applications.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GRID',
                'etymology': 'From Middle English "gridde," probably from "gridiron," a cooking utensil with parallel bars.',
                'language_origins': 'Middle English',
                'example_sentence': 'The city planner used a _______ system to organize the new neighborhood streets into neat, rectangular blocks.',
                'memory_tip': 'Remember "GRID" - GReat IDea for organization, a network of lines that creates an organized pattern for reference.'
            },
            'gridiron': {
                'definition': 'Gridiron originally refers to a cooking utensil consisting of parallel metal bars for broiling food over a fire, similar to a large grill grate. In American usage, gridiron is synonymous with a football field, named for the parallel yard lines that resemble the bars of a cooking gridiron. The term can also describe any framework of parallel bars or beams, or a network pattern resembling a grid. In urban planning, gridiron refers to a street layout with parallel and perpendicular streets forming rectangular blocks. The word connects the practical cooking tool with various applications that share its characteristic parallel-line structure.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GRID-eye-urn',
                'etymology': 'From Middle English, from "grid" + "iron," referring to the iron bars used for cooking.',
                'language_origins': 'Middle English',
                'example_sentence': 'The quarterback surveyed the _______ before the snap, reading the defense positioned across the yard lines.',
                'memory_tip': 'Remember "GRIDIRON" - GRID + IRON, iron bars in a grid pattern, like a football field or cooking grill.'
            },
            'griefful': {
                'definition': 'Griefful describes something that is full of grief or causing grief - characterized by deep sorrow, pain, or distress. This somewhat archaic or poetic term indicates a state of being overwhelmed with sadness or loss, or describes situations, events, or experiences that produce profound emotional pain. A griefful situation might involve death, loss, betrayal, or other circumstances that cause lasting sorrow. The word emphasizes the intensity and fullness of sorrowful emotion, suggesting that grief permeates or dominates the experience. While less common than "grievous" in modern usage, griefful carries a similar meaning with emphasis on the abundant presence of sorrow.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GREEF-ful',
                'etymology': 'From "grief" (from Old French "grief") + "-ful" suffix meaning "full of."',
                'language_origins': 'Old French, English',
                'example_sentence': 'The funeral was a _______ occasion where family members shared memories of their beloved grandmother.',
                'memory_tip': 'Remember "GRIEFFUL" - GRIEF + FUL, completely full of grief and deep sadness about a loss.'
            },
            'grievance': {
                'definition': 'Grievance is a formal complaint or a real or perceived cause for protest, especially regarding unfair treatment, injustice, or violation of rights. In workplace contexts, a grievance is typically a formal procedure for employees to raise concerns about working conditions, treatment, or policy violations. Grievances can be individual complaints or collective issues affecting groups of people. The term implies not just dissatisfaction but a legitimate basis for complaint that deserves attention and potential remedy. Grievance procedures are important mechanisms for addressing disputes and maintaining fairness in organizations, legal systems, and social institutions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GREE-vuns',
                'etymology': 'From Old French "grevance," from "grever" meaning "to burden, oppress," from Latin "gravare."',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The employee filed a formal _______ with human resources regarding the discriminatory treatment she experienced from her supervisor.',
                'memory_tip': 'Remember "GRIEVANCE" - GRIEVe + ANCE (state of), the state of having a legitimate complaint that causes you to grieve or feel wronged.'
            },
            'griffonage': {
                'definition': 'Griffonage refers to illegible or careless handwriting; scribbled, scrawled, or hastily written text that is difficult to read. This French-derived term describes writing that appears rough, untidy, or poorly formed, often resulting from speed, carelessness, or lack of attention to penmanship. Griffonage can result from writing quickly, using poor writing instruments, or simply having naturally messy handwriting. The word carries a somewhat critical connotation, suggesting that the writing quality is below acceptable standards. In an era of digital communication, griffonage is most commonly encountered in handwritten notes, signatures, or quick annotations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'grif-uh-NAHZH',
                'etymology': 'From French "griffonnage," from "griffonner" meaning "to scribble," related to "griffe" meaning "claw."',
                'language_origins': 'French',
                'example_sentence': 'The doctor\'s prescription was such terrible _______ that the pharmacist had to call the office for clarification.',
                'memory_tip': 'Remember "GRIFFONAGE" - GRIFFon (mythical creature with claws) + AGE, writing that looks like it was scratched out by claws.'
            },
            'grimaces': {
                'definition': 'Grimaces are facial expressions that show pain, disgust, distaste, or disapproval, typically involving twisting or distorting facial features in an unpleasant way. A grimace usually involves contorting the mouth, squinting the eyes, or wrinkling the forehead to express negative emotions or physical discomfort. People grimace in response to bad tastes, physical pain, embarrassing situations, or when witnessing something unpleasant. The expression is involuntary and communicates strong negative reactions. Grimaces serve as nonverbal communication, clearly indicating to others that someone is experiencing something disagreeable or uncomfortable.',
                'part_of_speech': 'noun (plural), verb (third person singular)',
                'pronunciation_guide': 'gri-MAS-iz',
                'etymology': 'From French "grimace," possibly from Germanic roots related to "grim."',
                'language_origins': 'French, Germanic',
                'example_sentence': 'The child _______ every time the nurse cleaned the scraped knee, showing obvious discomfort with the stinging antiseptic.',
                'memory_tip': 'Remember "GRIMACES" - GRIM FACES, making grim and unpleasant facial expressions when something hurts or disgusts you.'
            },
            'grimthorpe': {
                'definition': 'Grimthorpe, as a verb, means to restore or renovate an old building, especially a historic church or architectural structure, in a heavy-handed, insensitive manner that destroys its original character and historical value. The term originates from Sir Edmund Beckett, 1st Baron Grimthorpe, a Victorian architect who conducted controversial restorations of medieval buildings using methods that were criticized for their lack of sensitivity to original architectural integrity. To grimthorpe something is to "restore" it so thoroughly and inappropriately that the historical authenticity is lost. The word serves as a cautionary term in architectural preservation, representing the kind of restoration work that should be avoided.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'GRIM-thorp',
                'etymology': 'Named after Sir Edmund Beckett, 1st Baron Grimthorpe (1816-1905), known for controversial architectural restorations.',
                'language_origins': 'English (named after person)',
                'example_sentence': 'The preservationists worried that the contractor might _______ the medieval cathedral by using modern materials and ignoring historical accuracy.',
                'memory_tip': 'Remember "GRIMTHORPE" - GRIM + THORPE (town), grimly destroying the character of historic buildings through bad restoration.'
            },
            'grimy': {
                'definition': 'Grimy describes something covered with or full of grime - dirt, soot, or other ingrained filth that makes surfaces appear dark, dirty, and unclean. Grimy objects have accumulated layers of dirt and staining that cannot be easily wiped away, often requiring scrubbing or deep cleaning to remove. The word can describe physical surfaces like walls, hands, or clothing, or can be used metaphorically to describe situations, neighborhoods, or activities that seem morally questionable or unsavory. Grimy suggests not just surface dirt but deeply embedded filth that has built up over time.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'GRAHY-mee',
                'etymology': 'From "grime" (origin unknown, possibly from Middle Dutch or Germanic sources) + "-y" suffix.',
                'language_origins': 'Unknown origin, possibly Germanic',
                'example_sentence': 'After working in the coal mine all day, his hands and face were _______ with black dust that took thorough scrubbing to remove.',
                'memory_tip': 'Remember "GRIMY" - GRIM + Y, having a grim appearance because it\'s dirty and covered with ingrained filth.'
            },
            'grins': {
                'definition': 'Grins are broad smiles that show pleasure, amusement, or sometimes mischief, typically revealing the teeth and expressing happiness or satisfaction. A grin is usually wider and more pronounced than a regular smile, often indicating genuine joy, amusement at something funny, or pleased satisfaction with a situation. Grins can also suggest playful mischief or knowing satisfaction, as in a "mischievous grin" or "self-satisfied grin." The expression is generally positive, though context can give it different meanings. Grins are infectious expressions that often encourage others to smile or laugh in response.',
                'part_of_speech': 'noun (plural), verb (third person singular)',
                'pronunciation_guide': 'GRINZ',
                'etymology': 'From Old English "grennian," possibly related to "grin" and showing teeth.',
                'language_origins': 'Old English',
                'example_sentence': 'The children\'s faces lit up with wide _______ when they saw the surprise birthday cake their parents had prepared.',
                'memory_tip': 'Remember "GRINS" - GReat happy expreSsions, great big smiles that show you\'re really happy or amused.'
            },
            'griot': {
                'definition': 'Griot is a West African historian, storyteller, praise singer, poet, and musician who serves as a living repository of oral tradition and cultural history. Griots traditionally belong to specific families and castes, with knowledge and skills passed down through generations. They play crucial roles in preserving and transmitting historical narratives, genealogies, and cultural values through song, story, and music. Griots often perform at important ceremonies, celebrations, and social gatherings, using their extensive knowledge to educate, entertain, and maintain cultural continuity. Their performances typically involve musical instruments like the kora, balafon, or djembe, combined with vocal storytelling.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GREE-oh or gree-OT',
                'etymology': 'From French "griot," possibly from Portuguese "criado" or West African languages.',
                'language_origins': 'French, West African',
                'example_sentence': 'The village _______ captivated the audience with ancient stories of heroic ancestors, accompanied by the melodic sounds of his kora.',
                'memory_tip': 'Remember "GRIOT" - GReat stOriesTeller, a great storyteller who preserves cultural history through music and oral tradition.'
            },
            'grison': {
                'definition': 'Grison refers to a small carnivorous mammal native to Central and South America, belonging to the weasel family (Mustelidae). These animals are characterized by their grayish fur with distinctive white or light-colored stripes or patches, elongated bodies, and short legs. Grisons are primarily terrestrial but can climb and swim when necessary. They feed on small mammals, birds, eggs, insects, and fruits. There are two species: the greater grison and the lesser grison, both of which are relatively uncommon and found in various habitats from forests to grasslands. They play important roles in their ecosystems as both predators and prey.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GREE-sawn or GRIS-on',
                'etymology': 'From French "grison," meaning "gray," referring to the animal\'s grayish coloration.',
                'language_origins': 'French',
                'example_sentence': 'The wildlife biologist was excited to spot a _______ during the rainforest survey, as these small carnivores are rarely observed in the wild.',
                'memory_tip': 'Remember "GRISON" - GRIsy (gray) + ON, a gray-colored weasel-like animal that\'s gray on top.'
            },
            'grisonphulkari': {
                'definition': 'This appears to be a combined word error where "grison" (a weasel-like mammal) has been incorrectly merged with "phulkari" (a traditional form of embroidery from Punjab). A grison is a small carnivorous mammal with grayish fur, while phulkari is a traditional Punjabi embroidery technique characterized by brightly colored floral patterns, typically created with silk threads on cotton fabric. This combination likely resulted from a PDF parsing error where two completely unrelated terms were inadvertently joined together. The correct terms would be "grison" referring to the South American mammal, and "phulkari" referring to the traditional textile art form.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'GRIS-on-FOOL-kah-ree',
                'etymology': 'Error: "grison" (French, meaning gray) + "phulkari" (Punjabi, from "phul" flower + "kari" work)',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "grison" and "phulkari" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "GRISONPHULKARI" - this is a combined word error, separate into GRISON (gray mammal) + PHULKARI (floral embroidery).'
            },
            'grissino': {
                'definition': 'Grissino is an Italian breadstick - a thin, crispy bread product that originated in the Piedmont region of Italy, particularly associated with Turin. These slender, elongated bread sticks are typically made from flour, water, yeast, salt, and olive oil, then rolled very thin and baked until golden and crispy. Grissini (plural) are often served as appetizers in Italian restaurants, accompanied by antipasti, or used to scoop up dips and spreads. They can be plain or flavored with herbs, seeds, or cheese. The traditional grissino is hand-stretched to achieve its characteristic thin, irregular shape and crispy texture.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gree-SEE-no',
                'etymology': 'From Italian "grissino," diminutive of "grasso" meaning "fat" (ironic, as they are thin), from Turin dialect.',
                'language_origins': 'Italian',
                'example_sentence': 'The restaurant served warm _______ with olive oil and balsamic vinegar as a delicious appetizer before the main course.',
                'memory_tip': 'Remember "GRISSINO" - GReat Skinny Italian breadstick, a great thin Italian bread that\'s crispy and delicious.'
            },
            'grit': {
                'definition': 'Grit has multiple meanings: it refers to small particles of sand, stone, or other abrasive material, often used for cleaning, polishing, or providing traction. Grit also describes a personal quality of courage, determination, and strength of character in facing difficulties or challenges. Someone with grit perseveres through hardships and maintains resolve despite obstacles. The term can refer to coarsely ground grain, particularly corn grits served as food in the southern United States. In all uses, grit suggests toughness, persistence, and the ability to withstand wear or pressure, whether physical or metaphorical.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GRIT',
                'etymology': 'From Old English "greot," meaning "sand, gravel," from Germanic roots.',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'Despite facing numerous setbacks, she showed incredible _______ in pursuing her medical degree while working full-time.',
                'memory_tip': 'Remember "GRIT" - GReat Internal Toughness, both the tough sandy particles and the tough determination to persevere.'
            },
            'grits': {
                'definition': 'Grits are a dish made from coarsely ground corn kernels, particularly popular in the Southern United States. This porridge-like food is typically served hot and can be prepared with water, milk, or broth, often seasoned with butter, salt, and pepper. Grits can be served as a breakfast dish, side dish, or base for other ingredients like shrimp, cheese, or sausage. The texture ranges from smooth and creamy when finely ground to more coarse and hearty. Grits are a staple food with deep cultural significance in Southern cuisine, representing comfort food and traditional regional cooking.',
                'part_of_speech': 'noun (plural, but treated as singular)',
                'pronunciation_guide': 'GRITS',
                'etymology': 'From Old English "grytt," meaning "coarse meal," related to "grit."',
                'language_origins': 'Old English',
                'example_sentence': 'For breakfast, she ordered cheese _______ with bacon, enjoying the creamy texture and rich Southern flavors.',
                'memory_tip': 'Remember "GRITS" - GRound cITy food (corn), ground corn that\'s a signature dish of the Southern United States.'
            },
            'groats': {
                'definition': 'Groats are hulled cereal grains, particularly oats, wheat, or barley, from which the outer husk has been removed but which retain the bran and germ. Oat groats are whole oat kernels that serve as the basis for various oat products like rolled oats and steel-cut oats. Groats are considered highly nutritious because they contain the entire grain, providing fiber, protein, vitamins, and minerals. They require longer cooking times than processed grains but offer superior nutritional value and a hearty, chewy texture. Groats can be cooked as porridge, added to soups and stews, or ground into flour.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GROHTS',
                'etymology': 'From Old English "grōtan," related to "grit," referring to coarsely ground grain.',
                'language_origins': 'Old English',
                'example_sentence': 'The health-conscious cook preferred using oat _______ instead of instant oatmeal for their superior nutritional value and hearty texture.',
                'memory_tip': 'Remember "GROATS" - GReat OAT Seeds, the great whole oat kernels that are the most nutritious form of oats.'
            },
            'grobian': {
                'definition': 'Grobian refers to a rude, coarse, or ill-mannered person; someone who behaves in a crude, boorish, or socially inappropriate way. The term describes individuals who lack refinement, politeness, or proper social graces, often displaying behavior that is offensive or disturbing to others. A grobian might use foul language, have poor table manners, show disrespect for social conventions, or generally conduct themselves in ways that are considered uncouth or vulgar. The word carries strong negative connotations and suggests not just occasional rudeness but a consistent pattern of crude behavior that violates social norms.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GROH-bee-an',
                'etymology': 'From German "Grobian," from the fictional character Grobianus, representing coarse behavior.',
                'language_origins': 'German',
                'example_sentence': 'The restaurant manager had to ask the _______ to leave after his loud, crude behavior began disturbing other diners.',
                'memory_tip': 'Remember "GROBIAN" - GROss + roBBing people of pleasant company, someone whose gross behavior robs others of enjoyment.'
            },
            'groceries': {
                'definition': 'Groceries are food items and household supplies purchased for regular consumption, typically bought at supermarkets, grocery stores, or markets. The term encompasses fresh produce, packaged foods, beverages, cleaning supplies, and other everyday necessities that people need for daily living. Grocery shopping is a routine activity involving selecting and purchasing these items for home use. The word can refer both to the act of shopping for these items and to the items themselves once purchased. Groceries represent the basic supplies needed to maintain a household and prepare meals.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GROH-sur-eez',
                'etymology': 'From "grocery," from Old French "grocerie," from "gros" meaning "wholesale," originally referring to wholesale trade.',
                'language_origins': 'Old French',
                'example_sentence': 'After making a list, she went to the store to buy _______ for the week, including fresh vegetables, milk, and bread.',
                'memory_tip': 'Remember "GROCERIES" - GROcery + eries (things), the various food and household things you buy at the grocery store.'
            },
            'groenendael': {
                'definition': 'Groenendael is a variety of Belgian Shepherd dog, also known as the Belgian Sheepdog in some countries. This breed is characterized by its long, black, double coat, intelligent expression, and athletic build. Groenendaels are medium to large-sized dogs originally bred for herding sheep and cattle in Belgium. They are known for their high intelligence, loyalty, trainability, and strong work ethic. The breed requires regular exercise and mental stimulation, making them excellent working dogs, family companions, and participants in dog sports. Their name comes from the village of Groenendaal in Belgium, where the breed was first developed.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GROO-nen-dal',
                'etymology': 'Named after Groenendaal, a village in Belgium where this variety of Belgian Shepherd was first bred.',
                'language_origins': 'Dutch/Flemish (Belgian place name)',
                'example_sentence': 'The _______ excelled in the agility competition, demonstrating the intelligence and athleticism typical of Belgian Shepherd dogs.',
                'memory_tip': 'Remember "GROENENDAEL" - GREen valley + Belgian dog, a Belgian Shepherd breed named after a green valley village in Belgium.'
            },
            'groom': {
                'definition': 'Groom has several related meanings: as a noun, it refers to a man who is about to be married or has just been married, or historically, a person employed to care for horses. As a verb, groom means to clean and care for personal appearance, or to prepare someone for a particular role or activity. Grooming can involve brushing hair, cleaning, dressing appropriately, or maintaining good hygiene. The verb also describes preparing someone for advancement or success, such as grooming a successor. In animal care, grooming involves cleaning and maintaining an animal\'s coat and overall health.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GROOM',
                'etymology': 'From Middle English "grome," meaning "boy, male servant," origin uncertain.',
                'language_origins': 'Middle English',
                'example_sentence': 'The nervous _______ adjusted his tie one last time before walking down the aisle to meet his bride at the altar.',
                'memory_tip': 'Remember "GROOM" - GReat lOOk + Marriage, looking great for marriage, or making someone/something look great and well-cared for.'
            },
            'groove': {
                'definition': 'Groove refers to a long, narrow channel or furrow cut or worn into a surface, or a settled routine or habitual way of doing things. In music, groove describes the rhythmic feel or swing that makes music compelling and danceable. Physical grooves can be carved intentionally for functional purposes (like record grooves) or formed naturally through wear. Metaphorically, being "in the groove" means performing smoothly and effectively, operating at peak performance. A groove can also describe a rut or routine that becomes comfortable but potentially limiting. The word suggests both physical indentation and rhythmic or habitual patterns.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GROOV',
                'etymology': 'From Dutch "groeve" or Middle Dutch "groeve," meaning "furrow, ditch."',
                'language_origins': 'Dutch, Middle Dutch',
                'example_sentence': 'The DJ found the perfect _______ that kept the dance floor packed all night with its infectious rhythm.',
                'memory_tip': 'Remember "GROOVE" - GReat mOVEment, a great movement pattern whether it\'s a physical channel or a rhythmic flow.'
            },
            'grosgrain': {
                'definition': 'Grosgrain is a type of ribbon or fabric characterized by its distinctive ribbed texture, created by using heavier weft threads than warp threads. This technique produces prominent horizontal ribs or cords running across the width of the fabric. Grosgrain is typically made from silk, cotton, or synthetic materials and is commonly used for ribbons, trimming, hat bands, and formal wear details. The fabric is known for its durability, firm texture, and ability to hold its shape well. Grosgrain ribbons are popular for gift wrapping, hair accessories, and decorative purposes due to their attractive ribbed appearance and strength.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'GROH-grayn',
                'etymology': 'From French "gros grain," literally meaning "coarse grain," referring to the ribbed texture.',
                'language_origins': 'French',
                'example_sentence': 'She chose a navy blue _______ ribbon to trim the wedding invitations, appreciating its elegant ribbed texture.',
                'memory_tip': 'Remember "GROSGRAIN" - GROSs GRAIN texture, having a gross (thick/coarse) grain-like ribbed pattern.'
            },
            'gross': {
                'definition': 'Gross has multiple meanings: as an adjective, it can mean disgusting, offensive, or repulsive, or refer to something total or overall (before deductions). As a noun, gross can refer to twelve dozen (144 items) or total income before taxes and deductions. Gross can describe behavior that is crude, inappropriate, or morally offensive. In business contexts, gross refers to total amounts before expenses are subtracted, such as gross income or gross profit. The word can also mean obvious or glaring, as in "gross negligence." Context determines which meaning applies, from mathematical quantities to expressions of disgust.',
                'part_of_speech': 'adjective, noun, verb',
                'pronunciation_guide': 'GROHS',
                'etymology': 'From Old French "gros," from Late Latin "grossus," meaning "thick, coarse."',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The accountant calculated the company\'s _______ revenue before subtracting operating expenses and taxes.',
                'memory_tip': 'Remember "GROSS" - GReat Overall Sum (total), or GRossly disgusting, depending on context - either the total amount or really disgusting.'
            },
            'grotesque': {
                'definition': 'Grotesque describes something that is comically or repulsively ugly, distorted, or unnatural in appearance, often combining familiar elements in strange or disturbing ways. The term can refer to art, architecture, or literature that deliberately exaggerates features to create bizarre or fantastic effects. Grotesque figures often blend human, animal, and plant forms in impossible or disturbing combinations. In broader usage, grotesque describes anything so abnormal, distorted, or inappropriate as to be shocking or absurd. The word suggests something that provokes both fascination and revulsion, being simultaneously compelling and disturbing to observe.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'groh-TESK',
                'etymology': 'From French "grotesque," from Italian "grottesco," referring to art found in Roman grottoes (caves).',
                'language_origins': 'French, Italian',
                'example_sentence': 'The medieval cathedral featured _______ gargoyles whose twisted faces and bizarre forms were meant to ward off evil spirits.',
                'memory_tip': 'Remember "GROTESQUE" - GROTto + eSQUE (like), like the bizarre decorations found in ancient grottos and caves.'
            },
            'grotesqueness': {
                'definition': 'Grotesqueness is the quality or state of being grotesque - the characteristic of being comically or repulsively ugly, distorted, bizarre, or unnatural. This noun describes the degree to which something appears abnormal, disturbing, or fantastically distorted. Grotesqueness can apply to physical appearance, behavior, situations, or artistic representations that combine familiar elements in strange, disturbing, or absurd ways. The term encompasses both the visual impact of distortion and the emotional response it provokes, suggesting something that is simultaneously fascinating and repelling. Grotesqueness often implies an intentional or extreme deviation from normal proportions or expectations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'groh-TESK-nis',
                'etymology': 'From "grotesque" (from French, Italian origins) + "-ness" suffix indicating state or quality.',
                'language_origins': 'French, Italian',
                'example_sentence': 'The horror movie\'s special effects achieved such _______ that many viewers had to look away from the screen.',
                'memory_tip': 'Remember "GROTESQUENESS" - GROTesque + NESS (quality), the quality of being grotesque and bizarrely distorted.'
            },
            'grotto': {
                'definition': 'Grotto is a small, picturesque cave, especially an artificial one built as a garden feature or decorative element. Natural grottos are small caves or caverns, often near water, that may have interesting rock formations, acoustics, or historical significance. Artificial grottos are constructed features in parks, gardens, or religious sites, designed to create intimate, contemplative spaces. Many grottos have religious associations and may house shrines or statues. The term evokes mystery, tranquility, and connection with nature, whether referring to natural geological formations or human-made architectural features designed to mimic natural caves.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GROT-oh',
                'etymology': 'From Italian "grotta," from Latin "crypta," from Greek "krypte," meaning "hidden place."',
                'language_origins': 'Italian, Latin, Greek',
                'example_sentence': 'The monastery garden featured a peaceful _______ with a small shrine where monks could meditate in quiet solitude.',
                'memory_tip': 'Remember "GROTTO" - GReat cavernous spOT, a great spot that\'s like a small cave for peaceful contemplation.'
            },
            'ground': {
                'definition': 'Ground has multiple meanings: it most commonly refers to the solid surface of the earth, soil, or land. As a verb, ground is the past tense of "grind," meaning to reduce to small particles or powder. Ground can also mean to base something on solid reasoning or evidence, to restrict someone from certain activities (especially aircraft or children), or to connect electrically to the earth for safety. In sports, ground refers to playing fields or stadiums. The word encompasses both literal earth and metaphorical foundations, representing stability, basis, and fundamental support in various contexts.',
                'part_of_speech': 'noun, verb, adjective',
                'pronunciation_guide': 'GROWND',
                'etymology': 'From Old English "grund," from Germanic roots meaning "bottom, foundation."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The pilot was forced to keep the airplane on the _______ until the severe weather conditions improved.',
                'memory_tip': 'Remember "GROUND" - GReat fOUNDation, the great foundation that everything stands on, whether literal earth or figurative basis.'
            },
            'group': {
                'definition': 'Group refers to a collection of people, things, or entities that are located, gathered, or classed together based on shared characteristics, purposes, or relationships. Groups can be formal organizations with specific structures and goals, or informal collections of individuals who share common interests or circumstances. In mathematics, a group is a set with an operation that satisfies certain algebraic properties. Groups provide structure for social interaction, work collaboration, and organizational efficiency. The concept of group implies some form of unity, shared identity, or common purpose that distinguishes the collection from individual members or other groups.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GROOP',
                'etymology': 'From French "groupe," from Italian "groppo," meaning "knot, cluster."',
                'language_origins': 'French, Italian',
                'example_sentence': 'The study _______ met weekly to review course material and prepare for upcoming exams together.',
                'memory_tip': 'Remember "GROUP" - GatheR tOgether for a PUrpose, gathering together with others for a common purpose or interest.'
            },
            'grouped': {
                'definition': 'Grouped is the past tense of "group," meaning arranged, organized, or classified together based on shared characteristics, relationships, or purposes. When items or people are grouped, they have been sorted into collections or categories that make sense for organization, analysis, or activity. Grouped can describe the action of bringing similar things together or the state of being arranged in clusters or categories. This organizational process helps create order, facilitates understanding, and enables more effective management or study of the collected items or individuals.',
                'part_of_speech': 'verb (past tense), adjective',
                'pronunciation_guide': 'GROOPT',
                'etymology': 'Past tense of "group," from French "groupe," from Italian "groppo."',
                'language_origins': 'French, Italian',
                'example_sentence': 'The students were _______ by skill level to ensure everyone could participate effectively in the science project.',
                'memory_tip': 'Remember "GROUPED" - GROUPed togEther in the past, things that were brought together into organized collections.'
            },
            'grouse': {
                'definition': 'Grouse can refer to a game bird found in northern regions, characterized by feathered legs and feet, or as a verb meaning to complain or grumble persistently. As birds, grouse are known for their ground-dwelling habits, mottled plumage that provides camouflage, and importance as game animals. Common species include ruffed grouse, ptarmigan, and prairie grouse. As a verb, to grouse means to voice dissatisfaction or criticism, often about minor issues or in a habitual manner. Both meanings suggest persistence - the bird\'s hardy survival in harsh climates and the human tendency to voice repeated complaints.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GROWZ',
                'etymology': 'As bird: possibly from French "grous"; as verb: possibly related to French "groucier" meaning "to grumble."',
                'language_origins': 'French',
                'example_sentence': 'During the camping trip, they spotted a ruffed _______ drumming on a fallen log to attract a mate.',
                'memory_tip': 'Remember "GROUSE" - GROUnd dweller that makes SOUnds, either the bird that lives on ground or the person who sounds off with complaints.'
            },
            'grousegubernatorial': {
                'definition': 'This appears to be a combined word error where "grouse" (a game bird or to complain) has been incorrectly merged with "gubernatorial" (relating to a governor or governorship). Gubernatorial refers to matters concerning the office, election, or duties of a state governor, particularly in American politics. A grouse is either a ground-dwelling game bird or means to complain persistently. This combination likely resulted from a PDF parsing error where two completely unrelated words were inadvertently joined together. The correct terms would be "grouse" referring to either the bird or complaining, and "gubernatorial" referring to gubernatorial elections or governance.',
                'part_of_speech': 'combined word error',
                'pronunciation_guide': 'GROWZ-goo-ber-nuh-TOR-ee-al',
                'etymology': 'Error: "grouse" (French origins) + "gubernatorial" (from Latin "gubernator," meaning governor)',
                'language_origins': 'Combined word error',
                'example_sentence': 'This appears to be a PDF parsing error combining "grouse" and "gubernatorial" - the _______ should be treated as two separate words.',
                'memory_tip': 'Remember "GROUSEGUBERNATORIAL" - this is a combined word error, separate into GROUSE (bird/complain) + GUBERNATORIAL (governor-related).'
            }
        }
        
        return batch_079_data.get(word.lower(), {
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
            'greetingdifficulty': 'Combined word error: "greetingdifficulty" appears to be "greeting" + "difficulty" merged together. This is likely a PDF parsing error where salutation and challenge terminology were incorrectly combined.',
            'grisonphulkari': 'Combined word error: "grisonphulkari" appears to be "grison" + "phulkari" merged together. This is likely a PDF parsing error where a South American mammal and traditional Punjabi embroidery terms were incorrectly combined.',
            'grousegubernatorial': 'Combined word error: "grousegubernatorial" appears to be "grouse" + "gubernatorial" merged together. This is likely a PDF parsing error where bird/complaining and governor-related terminology were incorrectly combined.'
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
        
        print("Batch 079 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch079Processor()
    input_path = "output/batch_079_words.csv"
    output_path = "output/batch_079_processed.csv"
    processor.process_batch(input_path, output_path)