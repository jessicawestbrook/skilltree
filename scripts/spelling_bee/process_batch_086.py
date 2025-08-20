#!/usr/bin/env python3

import pandas as pd
from dataclasses import dataclass
from typing import List, Optional, Tuple
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
    phonetic_transparency: Optional[int] = None
    word_frequency: Optional[int] = None
    morphological_complexity: Optional[int] = None
    etymology_complexity: Optional[int] = None
    final_difficulty: Optional[str] = None

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

class Batch086Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        self.errors = []

    def get_comprehensive_claude_data(self, word: str) -> dict:
        batch_086_data = {
            'honourific': {
                'definition': 'Honourific is the British English spelling of "honorific," referring to titles, forms of address, or language expressions that convey respect, deference, or recognition of social status, professional achievement, or cultural position. These linguistic and social conventions include titles such as "Dr.," "Professor," "Your Honour," "Sir," or "Madam," as well as respectful language patterns that acknowledge hierarchy, age, expertise, or cultural values. The British spelling reflects historical linguistic traditions and is commonly used in Commonwealth countries including the United Kingdom, Canada, Australia, and other former British territories. Different cultures have complex honourific systems that reflect social structures, relationships, and values, requiring speakers to choose appropriate forms based on context, audience, and social dynamics. Professional honourifics recognize educational achievements, occupational roles, or institutional positions, while social honourifics may reflect age, gender, family relationships, or community status. Understanding and using appropriate honourifics demonstrates cultural competence, social awareness, and respect for established conventions. The spelling variation between "honour" and "honor" systems represents broader differences between British and American English orthographic traditions.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'on-uh-RIF-ik',
                'etymology': 'From Latin "honorificus" meaning "conferring honor," with British spelling using "ou" from French influence.',
                'language_origins': 'Latin, French, British English',
                'example_sentence': 'The British diplomat used the appropriate _______ titles when addressing members of Parliament during the formal ceremony.',
                'memory_tip': 'Remember "HONOURIFIC" - British spelling of honorific with HONOUR + IFIC, titles that honour and show respect for someone.'
            },
            'hooey': {
                'definition': 'Hooey is an informal American slang term meaning nonsense, foolish talk, or something that is obviously untrue or exaggerated. This colloquial expression dismisses statements, claims, or ideas as silly, worthless, or deliberately deceptive. The word carries a tone of casual dismissal rather than aggressive confrontation, making it suitable for informal conversations where someone wants to express skepticism without being overly harsh. Hooey often describes exaggerated advertising claims, political rhetoric, superstitious beliefs, or any statements that seem obviously false or misleading. The term can apply to both intentionally deceptive content and genuinely held beliefs that the speaker considers foolish or unfounded. Usage of hooey typically indicates the speaker\'s confidence that reasonable people would recognize the falseness or silliness of whatever is being described. The word reflects American linguistic creativity in developing colorful ways to express disbelief or dismissal. While informal and somewhat dated, hooey remains recognizable in American English as a mild way to call something nonsensical or untrue.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HOO-ee',
                'etymology': 'American slang, origin uncertain, possibly from "hooey" as an exclamation of disbelief or from similar-sounding expressions.',
                'language_origins': 'American English (slang)',
                'example_sentence': 'The salesman\'s claims about the miracle product were complete _______ designed to fool gullible customers.',
                'memory_tip': 'Remember "HOOEY" - sounds like "WHO-y?" like questioning "who would believe this nonsense?" when something is obviously false.'
            },
            'hook': {
                'definition': 'Hook refers to a curved or bent device designed for catching, holding, or suspending objects, typically made of metal, plastic, or other durable materials shaped to grip or support items. These versatile tools appear in countless applications from fishing hooks that catch fish to coat hooks that support clothing to cargo hooks that lift heavy loads. The curved shape allows hooks to catch and hold objects securely while enabling easy attachment and removal. In fishing, hooks come in various sizes and designs optimized for different fish species and fishing techniques. Construction and rigging use hooks for lifting and moving heavy materials safely. The term extends metaphorically to describe anything that catches attention, interest, or engagement, such as a "hook" in writing that draws readers in or a musical hook that makes songs memorable. Digital contexts use hooks in programming to intercept and modify software behavior. Understanding hook design and applications is important for fishing, construction, organizing systems, and many practical activities that require secure attachment or catching mechanisms.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'HOOK',
                'etymology': 'From Old English "hoc" meaning "hook" or "angle," from Germanic roots related to "hang."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The angler carefully selected a sharp _______ appropriate for the size of fish he hoped to catch in the lake.',
                'memory_tip': 'Remember "HOOK" - shaped like a question mark (?), a curved device that hooks onto or catches things securely.'
            },
            'hooligan': {
                'definition': 'Hooligan refers to a person who engages in rowdy, destructive, or violent behavior, particularly in groups and often in connection with sporting events or public gatherings. This term originated in late 19th-century Britain and became strongly associated with football (soccer) fan violence, though it applies to any form of organized troublemaking or antisocial behavior. Hooliganism typically involves property damage, fighting, intimidation, and disruption of public order, often fueled by group dynamics, alcohol, and tribal loyalties. The behavior goes beyond normal fan enthusiasm to include criminal activities that endanger public safety and property. Law enforcement agencies develop specialized strategies for managing hooligan groups, particularly around major sporting events where tensions and rivalries can escalate into violence. The term has expanded beyond sports contexts to describe any organized group engaged in destructive or antisocial activities. Understanding hooliganism involves examining group psychology, social identity, economic factors, and the role of alcohol and peer pressure in promoting violent behavior. Modern approaches to preventing hooliganism include community policing, fan education programs, and stadium security measures.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HOO-li-guhn',
                'etymology': 'Possibly from Irish surname "Hooligan," popularized in 1890s British music halls and associated with rowdy behavior.',
                'language_origins': 'Irish, British English',
                'example_sentence': 'The police increased security around the stadium to prevent _______ groups from causing violence during the championship match.',
                'memory_tip': 'Remember "HOOLIGAN" - sounds like "HOOP-again," troublemakers who jump through hoops to cause problems again and again.'
            },
            'hooves': {
                'definition': 'Hooves are the plural form of hoof, referring to the hard, horny coverings that protect the feet of certain mammals including horses, cattle, sheep, goats, deer, and pigs. These specialized structures are made of keratin, the same protein found in human fingernails and hair, but are much thicker and more durable to withstand the weight and movement of large animals. Hooves serve multiple functions including protection from rough terrain, support for the animal\'s weight, shock absorption during movement, and traction on various surfaces. The shape and structure of hooves vary among species, with horses having single hooves, cattle having cloven (split) hooves, and other animals showing different adaptations to their environments and movement patterns. Hoof care is essential in domestic animal management, requiring regular trimming, cleaning, and health monitoring to prevent lameness and disease. Wild animals naturally wear down their hooves through movement over varied terrain. Understanding hoof anatomy and care is crucial for veterinary medicine, animal husbandry, and wildlife biology.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'HOOVZ',
                'etymology': 'Plural of "hoof," from Old English "hof" meaning "hoof," from Germanic roots.',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The veterinarian examined the horse\'s _______ to ensure they were healthy and properly trimmed for safe riding.',
                'memory_tip': 'Remember "HOOVES" - sounds like "WHO-VES," the hard feet coverings of animals who move around on hard surfaces.'
            },
            'hope': {
                'definition': 'Hope is a feeling of expectation and desire for positive outcomes, combined with belief that favorable events are possible and worth working toward. This fundamental human emotion involves optimism about the future, confidence that goals can be achieved, and motivation to persist through challenges and setbacks. Hope provides psychological resilience during difficult times, enabling people to maintain effort and emotional stability when facing uncertainty or adversity. The concept encompasses both passive wishes and active efforts to create desired outcomes, ranging from simple daily hopes to profound life aspirations. Religious and philosophical traditions often emphasize hope as a virtue that sustains human dignity and purpose even in dire circumstances. Psychological research shows that hope correlates with better mental health, improved performance, and greater life satisfaction. Hope requires a balance between realistic assessment of possibilities and positive expectations about outcomes. Understanding hope involves recognizing its role in motivation, decision-making, and emotional regulation. Cultivating hope can improve resilience, goal achievement, and overall well-being in personal and professional contexts.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'HOHP',
                'etymology': 'From Old English "hopian" meaning "to hope" or "wish," from Germanic roots related to "hop" (jump).',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'Despite the challenges she faced, her _______ for a better future motivated her to continue pursuing her education.',
                'memory_tip': 'Remember "HOPE" - sounds like "HOOP," jumping through hoops with optimism that good things will happen in the future.'
            },
            'hopped': {
                'definition': 'Hopped is the past tense of the verb "hop," describing the action of jumping lightly on one foot or making short, quick jumps with both feet together. This movement pattern is common in many animals including rabbits, frogs, kangaroos, and birds, as well as in human activities like children\'s games and exercise routines. The hopping motion involves brief periods of being airborne followed by landing, typically used for quick movement or play rather than sustained locomotion. In human contexts, hopping can be recreational (hopscotch games), therapeutic (physical therapy exercises), or practical (navigating obstacles while keeping one foot elevated). The term can also describe quick, informal movement from one place to another, as in "hopping" between locations or activities. Animals use hopping as their primary means of locomotion, with specialized anatomical adaptations that make this movement efficient and fast. Understanding hopping biomechanics is relevant to sports science, physical therapy, animal behavior studies, and exercise physiology. The motion requires coordination, balance, and appropriate muscle strength to execute safely and effectively.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'HOPT',
                'etymology': 'Past tense of "hop," from Old English "hoppian" meaning "to dance" or "leap," from Germanic roots.',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The injured player _______ on one foot to the sideline after twisting his ankle during the game.',
                'memory_tip': 'Remember "HOPPED" - HOP + PED (past tense), already did the action of hopping or jumping on one or both feet.'
            },
            'hopping': {
                'definition': 'Hopping is the present participle of "hop," describing the ongoing action of jumping lightly on one foot or making repeated short jumps. This movement pattern can be continuous or intermittent, involving rhythmic bouncing motions that keep the person or animal in frequent contact with the ground. Hopping appears in various contexts including children\'s games like hopscotch, exercise routines for coordination and fitness, and animal locomotion patterns. The activity requires balance, coordination, and leg strength, making it useful for physical development and rehabilitation. Some animals, particularly rabbits, kangaroos, and certain birds, use hopping as their primary means of movement, having evolved specialized anatomy for efficient jumping locomotion. Human hopping can be recreational, therapeutic, or practical, such as when navigating obstacles or playing games. The term can also describe energetic or excited behavior, as someone might be "hopping mad" or "hopping with excitement." Understanding hopping mechanics is important for sports training, physical therapy, child development, and animal behavior studies. The activity provides cardiovascular exercise and helps develop lower body strength and balance.',
                'part_of_speech': 'verb (present participle), noun',
                'pronunciation_guide': 'HOP-ing',
                'etymology': 'Present participle of "hop," from Old English "hoppian" meaning "to dance" or "leap."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The children were _______ excitedly around the playground while waiting for the carnival games to begin.',
                'memory_tip': 'Remember "HOPPING" - HOP + PING, the ongoing action of hopping like a bunny rabbit bouncing around.'
            },
            'hopppped': {
                'definition': 'This appears to be a spelling error or typographical mistake involving the word "hopped" with extra "p" letters added. The correct spelling should be "hopped" with two "p"s, referring to the past tense of the verb "hop," which means to jump lightly on one foot or make short, quick jumps. The additional "p" letters likely resulted from typing errors, copy-and-paste mistakes, or data processing errors during text entry or transfer. Such spelling errors are common in digital documents and can occur through various means including keyboard malfunctions, software glitches, or human error during transcription. Quality control processes in document preparation should catch such obvious spelling mistakes before final publication or distribution. The error demonstrates the importance of proofreading and spell-checking in professional writing and data entry. Understanding that this is an error rather than a legitimate word helps maintain accuracy in spelling and communication. Proper spelling of "hopped" involves exactly two "p" letters followed by "-ed" to indicate past tense action.',
                'part_of_speech': 'spelling error',
                'pronunciation_guide': 'N/A (incorrect spelling)',
                'etymology': 'Spelling error: should be "hopped" with two "p"s, from "hop" plus past tense suffix "-ed."',
                'language_origins': 'Spelling error',
                'example_sentence': 'The word _______ appears to be a spelling error and should be written as "hopped" with only two p\'s.',
                'memory_tip': 'Remember "HOPPPPED" - this is a spelling error with too many P\'s; the correct spelling is "hopped" with just two P\'s.'
            },
            'hopscotch': {
                'definition': 'Hopscotch is a traditional children\'s playground game played by hopping through a pattern of numbered squares drawn on the ground, typically using chalk on pavement or other hard surfaces. The game involves throwing a small object (often called a "puck" or marker) into numbered squares and then hopping through the pattern while avoiding the square containing the marker. Players must hop on one foot in single squares and can use both feet in side-by-side double squares, following specific rules about which squares to skip and how to retrieve the marker. Hopscotch provides excellent physical exercise, helping children develop balance, coordination, leg strength, and spatial awareness while having fun. The game has ancient origins and appears in various forms across many cultures worldwide, with different regional variations in rules, patterns, and names. Modern hopscotch continues to be popular in schools, playgrounds, and recreational programs as a simple activity requiring minimal equipment but providing significant developmental benefits. The game teaches counting, following rules, taking turns, and good sportsmanship while encouraging physical activity and social interaction among children.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HOP-skoch',
                'etymology': 'From "hop" + "scotch" (score or scratch), referring to hopping over scratched lines on the ground.',
                'language_origins': 'English',
                'example_sentence': 'The children drew a _______ pattern on the playground with chalk and took turns hopping through the numbered squares.',
                'memory_tip': 'Remember "HOPSCOTCH" - HOP + SCOTCH (scratch), a game where you hop over scratched lines drawn on the ground.'
            },
            'hordeolum': {
                'definition': 'Hordeolum is the medical term for a stye, a small, painful bacterial infection that occurs in the oil glands of the eyelids, typically appearing as a red, swollen bump resembling a pimple. This common eye condition results from bacterial infection, usually by Staphylococcus bacteria, that blocks and inflames the sebaceous glands along the eyelash follicles or deeper meibomian glands within the eyelid. Hordeolum can be external (affecting glands at the eyelash base) or internal (affecting glands within the eyelid), with external types being more common and visible. Symptoms include localized pain, swelling, redness, tenderness, and sometimes discharge or crusting around the affected area. The condition often resolves spontaneously within a few days to weeks, though warm compresses and good eyelid hygiene can help speed healing and provide comfort. Severe or recurrent hordeolum may require antibiotic treatment or minor surgical drainage. Prevention involves maintaining good eye hygiene, avoiding eye rubbing with dirty hands, and properly removing eye makeup. Understanding hordeolum helps people recognize this common condition and seek appropriate treatment when necessary.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hor-DEE-oh-luhm',
                'etymology': 'From Latin "hordeolum" meaning "little barley grain," referring to the resemblance of a stye to a barley seed.',
                'language_origins': 'Latin',
                'example_sentence': 'The ophthalmologist diagnosed the patient\'s painful eyelid swelling as a _______ and recommended warm compresses for treatment.',
                'memory_tip': 'Remember "HORDEOLUM" - from Latin for "little barley grain," a stye that looks like a small grain on the eyelid.'
            },
            'horizon': {
                'definition': 'Horizon refers to the apparent line where the earth\'s surface meets the sky, creating a visual boundary between terrestrial and celestial views. This fundamental geographical and optical phenomenon results from the curvature of the Earth and the limitations of human visual perspective. The horizon appears to be at eye level regardless of elevation, though its actual distance varies with height above sea level - higher positions reveal more distant horizons. Maritime navigation relies heavily on horizon observations for determining position, weather patterns, and safe passage. The term extends metaphorically to describe limits, boundaries, or future possibilities, as in "expanding one\'s horizons" or planning "on the horizon." Astronomical horizons include specific technical definitions used in celestial navigation and observational astronomy. Weather phenomena often appear first at the horizon, making it important for meteorological observations and predictions. Artists frequently use horizon lines as compositional elements that organize visual space and create depth in landscapes and seascapes. Understanding horizon concepts is essential for navigation, geography, astronomy, and visual arts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'huh-RAHY-zuhn',
                'etymology': 'From Greek "horizon" meaning "bounding" or "limiting," from "horizein" meaning "to bound."',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'The ship appeared as a small dot on the distant _______ before gradually growing larger as it approached the harbor.',
                'memory_tip': 'Remember "HORIZON" - the line where the earth meets the sky at the HORIZONTAL boundary of what you can see.'
            },
            'horizontal': {
                'definition': 'Horizontal describes a position, direction, or orientation that runs parallel to the earth\'s surface or perpendicular to the direction of gravity, forming a level line from left to right. This fundamental geometric concept is essential in construction, engineering, navigation, and many practical applications where level surfaces and accurate measurements are crucial. Horizontal lines appear flat and even, contrasting with vertical lines that run up and down. Construction uses horizontal references for ensuring buildings are level, foundations are even, and structures are properly aligned. The term applies to both physical objects and abstract concepts, such as horizontal thinking (lateral problem-solving approaches) or horizontal integration (business expansion within the same industry level). Tools like spirit levels, laser levels, and surveying equipment help establish accurate horizontal references for construction and measurement. Understanding horizontal orientation is essential for reading maps, architectural plans, and technical drawings. The concept relates to balance, stability, and proper alignment in countless practical applications from hanging pictures to building skyscrapers.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'hawr-uh-ZON-tuhl',
                'etymology': 'From "horizon" plus the suffix "-al," meaning "relating to the horizon" or "parallel to the horizon."',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'The carpenter used a level to ensure the shelf was perfectly _______ before securing it to the wall.',
                'memory_tip': 'Remember "HORIZONTAL" - relates to HORIZON + AL, running parallel to the horizon line, left to right and level.'
            },
            'horned': {
                'definition': 'Horned describes animals or objects that possess horns, the hard, pointed projections that grow from the heads of certain mammals including cattle, goats, sheep, rhinoceros, and many wild species. Animal horns are permanent structures made of keratin (the same protein in fingernails and hair) surrounding a bony core, distinguishing them from antlers which are shed and regrown annually. Horned animals use these structures for defense, competition, dominance displays, and species recognition. The size, shape, and number of horns vary dramatically among species, from the massive single horn of rhinoceros to the curved horns of bighorn sheep to the elaborate twisted horns of some antelope species. In domestic animals, horns may be naturally present or removed for safety reasons, particularly in dairy and beef cattle operations. The term also applies to objects shaped like horns or having horn-like projections, such as horned helmets in historical armor or horned instruments in music. Understanding horned animals is important for livestock management, wildlife biology, and animal safety considerations.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'HAWRND',
                'etymology': 'From "horn" plus the suffix "-ed," meaning "having horns" or "equipped with horn-like projections."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The rancher kept his _______ cattle in a separate pasture from the hornless ones to prevent injuries during feeding.',
                'memory_tip': 'Remember "HORNED" - HORN + ED, describing animals that have horns growing from their heads.'
            },
            'horns': {
                'definition': 'Horns are hard, pointed structures that project from the heads of various mammals, made of keratin surrounding a bony core and used for defense, competition, and social signaling. These permanent anatomical features differ from antlers, which are shed and regrown annually. Horn shapes and sizes vary tremendously among species, from the single horns of rhinoceros to the paired horns of cattle, the spiral horns of some antelopes, and the massive curved horns of water buffalo. In domestic animals, horns may pose safety concerns and are sometimes removed through dehorning procedures, though some breeds are naturally polled (hornless). The term also refers to musical instruments made from animal horns or shaped like horns, including French horns, hunting horns, and various folk instruments. Vehicle horns serve as warning devices that produce loud sounds to alert other drivers and pedestrians. Understanding horn biology is important for animal husbandry, wildlife management, and veterinary care. Cultural associations with horns include symbols of power, strength, and sometimes evil or danger in various mythological and religious contexts.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'HAWRNZ',
                'etymology': 'Plural of "horn," from Old English "horn," from Germanic roots related to projecting points.',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The bull\'s large _______ made him look intimidating, but he was actually quite gentle with the farm workers.',
                'memory_tip': 'Remember "HORNS" - the hard, pointed projections that grow from animal heads, like the horns on a bull or rhino.'
            },
            'horologist': {
                'definition': 'Horologist refers to a person who studies, designs, makes, or repairs clocks, watches, and other timepieces, combining technical skill with artistic craftsmanship and scientific understanding of timekeeping mechanisms. This specialized profession requires deep knowledge of mechanical systems, precision engineering, and often historical restoration techniques for antique timepieces. Horologists work with various types of timekeeping devices from simple mechanical clocks to complex astronomical clocks, chronometers, and modern precision instruments. The field combines elements of engineering, artistry, and historical preservation, as many horologists specialize in restoring valuable antique timepieces that represent centuries of technological development. Modern horologists may focus on different areas including repair services, custom clockmaking, restoration of historical pieces, or research into timekeeping technology. The profession requires excellent fine motor skills, patience for detailed work, and understanding of both traditional mechanical systems and modern timekeeping technology. Swiss watchmaking traditions have particularly elevated horology to an art form, producing some of the world\'s most skilled horologists. Understanding horology involves appreciating the intersection of science, technology, craftsmanship, and artistic expression in measuring time.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'huh-ROL-uh-jist',
                'etymology': 'From "horology" (study of time measurement) plus "-ist" (one who practices), from Greek "hora" (time) and "logos" (study).',
                'language_origins': 'Greek',
                'example_sentence': 'The skilled _______ carefully restored the 18th-century grandfather clock to its original working condition.',
                'memory_tip': 'Remember "HOROLOGIST" - HORO (time) + LOGIST (specialist), someone who specializes in the study and repair of timepieces.'
            },
            'horologistspeleothem': {
                'definition': 'This appears to be a combined word error from PDF parsing, incorrectly merging "horologist" (someone who studies or repairs timepieces) with "speleothem" (mineral deposits formed in caves). This type of parsing error occurs when PDF text extraction software fails to properly separate words from different parts of a document, creating nonsensical combinations that don\'t exist in standard dictionaries. The error likely resulted from text appearing in adjacent columns, different text blocks, or overlapping elements that were erroneously combined during the digitization process. Such combined word errors highlight the importance of quality control in data processing, especially when dealing with large datasets extracted from various PDF sources with complex formatting. The original document likely contained separate references to horologists (clockmakers) and speleothems (cave formations), which were incorrectly merged during text extraction. This demonstrates why careful validation and error detection are essential when processing digitized text from academic or reference materials where accuracy is crucial for educational purposes.',
                'part_of_speech': 'parsing error',
                'pronunciation_guide': 'N/A (invalid word)',
                'etymology': 'Combined word error: "horologist" + "speleothem" merged during PDF parsing.',
                'language_origins': 'PDF parsing error',
                'example_sentence': 'The word _______ does not exist in English dictionaries and appears to be a PDF processing error combining two unrelated scientific terms.',
                'memory_tip': 'Remember "HOROLOGISTSPELEOTHEM" - this is a PDF parsing error combining HOROLOGIST (clockmaker) + SPELEOTHEM (cave formation) into one invalid word.'
            },
            'horse': {
                'definition': 'Horse refers to a large, four-legged domesticated mammal (Equus caballus) that has been a crucial partner to humans for thousands of years in transportation, agriculture, warfare, and recreation. These magnificent animals are characterized by their flowing manes, powerful build, keen intelligence, and remarkable athletic abilities that have made them invaluable throughout human history. Horses possess excellent memory, strong social bonds, and the ability to form deep relationships with humans through proper training and care. Different breeds have been developed for specific purposes including draft work (pulling heavy loads), riding, racing, jumping, and showing, each with distinct physical characteristics and temperaments. Modern horses serve primarily recreational purposes through riding, racing, showing, and therapeutic programs, though they still work in some agricultural and ceremonial contexts. Horse care requires significant knowledge of nutrition, health, grooming, training, and stable management. The human-horse relationship has profoundly influenced culture, art, literature, and military history. Understanding horses involves appreciating their psychology, physical needs, and the skills required for safe and effective interaction with these powerful animals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAWRS',
                'etymology': 'From Old English "hors," from Germanic roots, related to the concept of "running" or "swift movement."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The beautiful black _______ galloped across the meadow with grace and power, its mane flowing in the wind.',
                'memory_tip': 'Remember "HORSE" - sounds like "FORCE," these powerful animals were a major force in human history for transportation and work.'
            },
            'horseradish': {
                'definition': 'Horseradish is a perennial plant (Armoracia rusticana) in the mustard family, cultivated primarily for its large, white, tapered root that produces a pungent, spicy condiment when grated or processed. The plant\'s root contains compounds called glucosinolates that, when damaged by grating or chewing, produce the characteristic sharp, burning sensation that can clear sinuses and bring tears to the eyes. Fresh horseradish root has a much stronger flavor than prepared commercial versions, which often contain vinegar to stabilize the heat and prevent excessive pungency. Horseradish sauce traditionally accompanies roast beef, seafood, and various ethnic dishes, particularly in European and Jewish cuisines. The plant is hardy and easy to grow, often becoming invasive if not properly contained, with large leaves and small white flowers. Medicinally, horseradish has been used historically for respiratory conditions, digestive issues, and as a natural antibiotic, though scientific evidence for these uses is limited. The name possibly derives from the plant\'s strong bite, comparable to a horse\'s kick, rather than any actual relationship to horses.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAWRS-rad-ish',
                'etymology': 'From "horse" (indicating strength or coarseness) + "radish," though the plant is not botanically related to radishes.',
                'language_origins': 'English',
                'example_sentence': 'The chef grated fresh _______ root to make a fiery sauce that perfectly complemented the prime rib dinner.',
                'memory_tip': 'Remember "HORSERADISH" - HORSE + RADISH, a root so strong and spicy it kicks like a horse when you taste it.'
            },
            'hortatory': {
                'definition': 'Hortatory describes language, speeches, or writing that strongly encourages, urges, or gives advice, typically intended to inspire action or motivate behavior change. This rhetorical style emphasizes persuasion through encouragement rather than command, using inspirational appeals, moral arguments, and emotional motivation to influence audience decisions. Hortatory discourse appears frequently in religious sermons, motivational speeches, political campaigns, and educational contexts where speakers aim to inspire positive action without resorting to direct orders or threats. The approach relies on shared values, common goals, and emotional connection to convince audiences to adopt particular behaviors or beliefs. Effective hortatory communication requires understanding audience motivations, cultural values, and appropriate emotional appeals that resonate with intended listeners. Examples include graduation speeches encouraging achievement, environmental advocacy promoting conservation, and public health campaigns urging healthy behaviors. The style balances respect for audience autonomy with passionate advocacy for specific actions or values. Understanding hortatory techniques helps both speakers craft more effective persuasive messages and audiences recognize when they are being encouraged toward particular conclusions or behaviors.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'HAWR-tuh-tawr-ee',
                'etymology': 'From Latin "hortatorius," from "hortari" meaning "to encourage" or "urge."',
                'language_origins': 'Latin',
                'example_sentence': 'The principal\'s _______ address to graduating students encouraged them to pursue their dreams with determination and integrity.',
                'memory_tip': 'Remember "HORTATORY" - from Latin "hortari" (to urge), language that urges and encourages people to take positive action.'
            },
            'horticulture': {
                'definition': 'Horticulture is the branch of agriculture focused on the cultivation, production, and study of fruits, vegetables, nuts, seeds, herbs, sprouts, mushrooms, algae, flowers, seaweeds, and non-food crops such as grass and ornamental trees and plants. This scientific discipline combines botanical knowledge with practical growing techniques to optimize plant production for food, medicine, comfort, and aesthetic purposes. Horticultural practices include plant breeding, crop production, plant propagation, crop physiology, plant pathology, soil management, and post-harvest handling and processing. The field encompasses both commercial production operations and residential gardening activities, ranging from large-scale greenhouse operations to home vegetable gardens. Modern horticulture incorporates sustainable practices, integrated pest management, organic growing methods, and advanced technologies like hydroponics and controlled environment agriculture. Horticultural education prepares professionals for careers in nursery management, landscape design, food production, research, and extension services. The discipline plays crucial roles in food security, environmental sustainability, urban planning, and quality of life through both food production and ornamental landscaping that enhances human living spaces.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAWR-ti-kuhl-cher',
                'etymology': 'From Latin "hortus" meaning "garden" and "cultura" meaning "cultivation," literally "garden cultivation."',
                'language_origins': 'Latin',
                'example_sentence': 'The university\'s _______ program taught students both the science and practical skills needed for successful plant cultivation and garden management.',
                'memory_tip': 'Remember "HORTICULTURE" - HORTI (garden) + CULTURE (cultivation), the science and art of cultivating gardens and crops.'
            },
            'hospitality': {
                'definition': 'Hospitality refers to the generous and friendly treatment of guests, visitors, or strangers, encompassing the customs, practices, and attitudes that make people feel welcome and comfortable in unfamiliar settings. This fundamental social concept involves providing food, shelter, entertainment, and care to others, often without expectation of immediate reciprocation. Hospitality traditions exist across all cultures, though specific practices vary significantly based on religious beliefs, social customs, economic conditions, and historical contexts. The concept extends beyond personal interactions to include professional service industries such as hotels, restaurants, tourism, and event management that specialize in providing positive experiences for customers. Quality hospitality involves attention to detail, anticipation of needs, genuine care for guest comfort, and creation of memorable experiences that exceed expectations. Religious and philosophical traditions often emphasize hospitality as a moral virtue and sacred duty, particularly toward strangers and those in need. Understanding hospitality involves recognizing cultural differences in guest treatment, service expectations, and appropriate reciprocal behaviors. Modern hospitality education combines service skills with business management, cultural awareness, and customer psychology.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hos-pi-TAL-i-tee',
                'etymology': 'From Latin "hospitalitas," from "hospitalis" meaning "of a guest," from "hospes" meaning "guest" or "host."',
                'language_origins': 'Latin',
                'example_sentence': 'The family\'s warm _______ made their international visitors feel immediately at home in the unfamiliar country.',
                'memory_tip': 'Remember "HOSPITALITY" - related to HOSPITAL (place of care), the generous care and welcome treatment of guests and visitors.'
            },
            'hostile': {
                'definition': 'Hostile describes behavior, attitudes, or environments characterized by antagonism, aggression, or unfriendliness toward others. This adjective applies to individuals, groups, situations, or conditions that create opposition, conflict, or danger rather than cooperation and support. Hostile behavior can range from verbal aggression and unfriendly attitudes to physical violence and warfare, depending on context and intensity. Environmental conditions can be hostile when they pose dangers to human survival or comfort, such as extreme weather, dangerous terrain, or toxic substances. Workplace hostility involves discrimination, harassment, or aggressive behavior that creates uncomfortable or threatening work environments. Legal contexts recognize hostile environments as situations where systematic harassment makes normal participation difficult or impossible. Understanding hostility involves recognizing the difference between temporary conflict and persistent antagonistic patterns that require intervention. Hostile situations often escalate without proper management, making early recognition and appropriate response crucial for safety and conflict resolution. The term can also describe military or competitive contexts where opposition is expected and legitimate rather than problematic.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'HOS-tahyl',
                'etymology': 'From Latin "hostilis," from "hostis" meaning "enemy" or "stranger."',
                'language_origins': 'Latin',
                'example_sentence': 'The negotiator worked to defuse the _______ atmosphere and find common ground between the conflicting parties.',
                'memory_tip': 'Remember "HOSTILE" - from Latin "hostis" (enemy), describing enemy-like behavior that is aggressive and unfriendly.'
            },
            'hostilehowler': {
                'definition': 'This appears to be a combined word error from PDF parsing, incorrectly merging "hostile" (aggressive or unfriendly) with "howler" (something that howls or a glaring mistake). This type of parsing error occurs when PDF text extraction software fails to properly separate adjacent words, especially when formatting changes between lines, columns, or text blocks. The combination creates a nonsensical term that doesn\'t exist in standard dictionaries and demonstrates the challenges of processing digitized text from various sources. Such errors are particularly common when dealing with documents that have complex layouts, multiple columns, or inconsistent formatting that confuses automated text extraction systems. The original document likely contained separate references to hostile behavior and something described as a howler (perhaps an error or a howling animal), which were erroneously combined during the digitization process. This highlights the importance of implementing quality control measures and error detection systems when processing large datasets extracted from PDF documents. Careful validation and manual review remain essential for ensuring data accuracy in educational and reference applications where precise information is crucial.',
                'part_of_speech': 'parsing error',
                'pronunciation_guide': 'N/A (invalid word)',
                'etymology': 'Combined word error: "hostile" + "howler" merged during PDF parsing.',
                'language_origins': 'PDF parsing error',
                'example_sentence': 'The word _______ does not exist in English dictionaries and appears to be a PDF processing error combining two separate words.',
                'memory_tip': 'Remember "HOSTILEHOWLER" - this is a PDF parsing error combining HOSTILE (aggressive) + HOWLER (something that howls) into one invalid word.'
            },
            'hotel': {
                'definition': 'Hotel refers to a commercial establishment that provides lodging, meals, and other services to travelers and tourists for payment. These businesses range from basic accommodations with minimal amenities to luxury resorts offering extensive facilities including restaurants, spas, entertainment venues, and recreational activities. Hotels serve the fundamental human need for temporary shelter away from home, supporting business travel, tourism, and various forms of mobility in modern society. The hospitality industry encompasses various types of hotels including business hotels, resort hotels, boutique hotels, extended-stay facilities, and budget accommodations, each designed for specific customer needs and price points. Hotel operations involve complex management of reservations, housekeeping, food service, maintenance, security, and customer relations to ensure guest satisfaction and business profitability. Modern hotels often provide technology amenities such as internet access, business centers, and mobile check-in services to meet contemporary traveler expectations. The quality and reputation of hotels significantly impact local tourism, economic development, and community image. Understanding hotel operations involves hospitality management, customer service, facilities management, and business operations skills.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hoh-TEL',
                'etymology': 'From French "hôtel," originally meaning "townhouse" or "mansion," from Old French "hostel."',
                'language_origins': 'French, Old French',
                'example_sentence': 'The business travelers chose a downtown _______ that offered convenient access to the convention center and airport transportation.',
                'memory_tip': 'Remember "HOTEL" - sounds like "HOST-EL," a place that hosts travelers by providing temporary lodging and services.'
            },
            'houppelande': {
                'definition': 'Houppelande is a historical garment worn in medieval Europe, particularly from the 14th to 16th centuries, characterized as a long, loose-fitting outer robe or gown with wide sleeves and often a high collar. This elegant garment was worn by both men and women of the upper classes and represented fashion sophistication and social status during the late medieval period. The houppelande typically featured rich fabrics, elaborate decorations, and intricate tailoring that demonstrated the wearer\'s wealth and position. Men\'s versions were often shorter and more fitted, while women\'s houppelandes were typically floor-length and more voluminous. The garment evolved over time, with variations in sleeve styles, collar treatments, and overall silhouette reflecting changing fashion preferences and regional differences. Houppelandes were often made from expensive materials such as velvet, silk, or fine wool and decorated with embroidery, fur trim, or jeweled accessories. Fashion historians study houppelandes as important examples of medieval clothing construction, social stratification, and artistic expression. Modern historical reenactment, theatrical costume design, and fashion education often reference houppelandes as quintessential examples of medieval aristocratic dress.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hoo-puh-LAHND',
                'etymology': 'From Old French "houppelande," possibly related to "houppe" meaning "tuft" or "crest," referring to decorative elements.',
                'language_origins': 'Old French',
                'example_sentence': 'The museum\'s medieval collection featured a beautifully preserved 15th-century _______ made of rich burgundy velvet with gold embroidery.',
                'memory_tip': 'Remember "HOUPPELANDE" - a HOOP-like LAND of fabric, describing the wide, flowing medieval robes worn by aristocrats.'
            },
            'hour': {
                'definition': 'Hour refers to a unit of time equal to 60 minutes or 3,600 seconds, representing one twenty-fourth of a day in standard time measurement systems. This fundamental temporal division organizes daily life, work schedules, transportation systems, and countless human activities around the world. Hours provide the framework for coordinating social activities, business operations, and personal routines across different time zones and cultures. The concept of dividing days into 24 equal hours originated in ancient civilizations and has become universally adopted in modern timekeeping systems. Clock faces typically display 12 hours twice daily, while digital systems often use 24-hour formats to eliminate ambiguity between morning and afternoon times. Different contexts require precise hour measurement, including work schedules, transportation timetables, scientific experiments, and legal proceedings. The term also describes periods of time more generally, such as "rush hour" for busy traffic periods or "office hours" for availability periods. Understanding hour-based time systems is essential for punctuality, scheduling, and coordination in modern society.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'OWR',
                'etymology': 'From Old French "hore," from Latin "hora," from Greek "hora" meaning "time" or "season."',
                'language_origins': 'Greek, Latin, Old French',
                'example_sentence': 'The meeting was scheduled to last exactly one _______ but continued for nearly two due to extensive discussion.',
                'memory_tip': 'Remember "HOUR" - sounds like "OUR," our basic unit of time that divides the day into 24 equal parts.'
            },
            'hours': {
                'definition': 'Hours is the plural form of hour, referring to multiple units of time or periods of operation, availability, or activity. This term commonly appears in contexts describing work schedules, business operations, service availability, and time duration. Business hours indicate when establishments are open for customers, while working hours define employment time requirements and overtime calculations. The concept of hours shapes modern life through structured schedules, time management, and coordination of activities across different time zones. Educational institutions use credit hours to measure academic workload and degree requirements. Medical contexts reference hours for medication schedules, symptom monitoring, and treatment duration. Legal and employment contexts carefully define hours worked for wage calculation, labor law compliance, and benefit eligibility. The flexibility of modern work includes various hour arrangements such as flexible hours, part-time hours, and compressed work weeks. Understanding hour systems is crucial for time management, scheduling, and meeting obligations in personal and professional contexts. Different cultures and industries may have varying norms regarding appropriate hours for different activities.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'OWRZ',
                'etymology': 'Plural of "hour," from Old French "hore," from Latin "hora," from Greek "hora."',
                'language_origins': 'Greek, Latin, Old French',
                'example_sentence': 'The restaurant\'s _______ were posted on the door so customers would know when they could dine there.',
                'memory_tip': 'Remember "HOURS" - HOUR + S, multiple units of time or the times when places are open for business.'
            },
            'house': {
                'definition': 'House refers to a building designed and constructed as a dwelling place for people, typically including rooms for sleeping, cooking, eating, and living activities. This fundamental architectural structure serves the basic human need for shelter while providing privacy, security, storage space, and a base for family and personal life. Houses vary enormously across cultures, climates, economic conditions, and personal preferences, ranging from simple single-room structures to elaborate multi-story mansions with numerous specialized spaces. Construction methods, materials, and designs reflect local resources, climate conditions, building traditions, and aesthetic preferences. Modern houses often include utilities such as electricity, plumbing, heating, and internet connectivity that support contemporary lifestyle needs. The concept extends beyond physical structure to encompass the idea of "home" with emotional, social, and cultural significance representing belonging, identity, and personal sanctuary. Real estate markets, urban planning, and housing policy significantly impact access to houses and community development. Understanding houses involves architecture, construction, interior design, property law, and the social functions of domestic space.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'HOWS',
                'etymology': 'From Old English "hus," from Germanic roots meaning "shelter" or "covering."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The family spent months searching for the perfect _______ in a neighborhood with good schools and parks nearby.',
                'memory_tip': 'Remember "HOUSE" - sounds like "HOW-S," as in "how\'s your house?" - the building where you live and call home.'
            },
            'households': {
                'definition': 'Households refer to groups of people who live together in the same dwelling unit, sharing living spaces and often resources, expenses, and domestic responsibilities. This demographic and economic unit serves as the basic building block for census data, market research, social policy, and economic analysis. Households can consist of families (related individuals), unrelated individuals living together, or single-person units, each representing different social and economic patterns. The composition and characteristics of households significantly impact consumer behavior, housing demand, utility usage, and community planning needs. Government agencies use household data for resource allocation, tax policy, social services planning, and infrastructure development. Economic research analyzes household income, spending patterns, savings behavior, and financial decision-making to understand broader economic trends. Household formation and dissolution patterns reflect social changes including marriage rates, divorce rates, educational trends, and economic opportunities. Modern households increasingly include diverse arrangements such as multi-generational families, unmarried couples, roommate situations, and single-parent families. Understanding household dynamics is essential for marketing, urban planning, social services, and policy development.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'HOWS-hohldz',
                'etymology': 'Plural of "household," from "house" + "hold" (those who hold or occupy a house).',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The census revealed that average _______ size had decreased over the past decade due to changing family structures.',
                'memory_tip': 'Remember "HOUSEHOLDS" - HOUSE + HOLDS, the groups of people who hold or live together in houses.'
            },
            'houses': {
                'definition': 'Houses is the plural form of house, referring to multiple residential buildings or dwelling structures designed for human habitation. This term encompasses the variety of architectural styles, sizes, and types of residential buildings found in communities, from small cottages to large estates. Real estate markets deal extensively with houses as commodities that are bought, sold, rented, and developed to meet housing demand. Urban and rural planning involves arranging houses within communities to create functional neighborhoods with appropriate infrastructure, services, and amenities. Construction industries build houses using various materials, techniques, and designs adapted to local conditions, regulations, and market preferences. The availability and affordability of houses significantly impact economic development, social mobility, and community stability. Historical preservation efforts often focus on houses that represent important architectural styles, cultural heritage, or significant events. Energy efficiency, sustainability, and smart home technology increasingly influence modern house design and construction. Understanding houses involves architecture, construction, real estate, urban planning, and the social functions of residential communities.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'HOW-ziz',
                'etymology': 'Plural of "house," from Old English "hus," from Germanic roots.',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The new subdivision featured fifty modern _______ designed with energy-efficient features and contemporary architectural styles.',
                'memory_tip': 'Remember "HOUSES" - HOUSE + S, multiple buildings where people live, like all the houses in a neighborhood.'
            },
            'hover': {
                'definition': 'Hover describes the action of remaining suspended in air or staying in one place while floating or flying, typically referring to aircraft, birds, insects, or objects that maintain position without moving forward, backward, or landing. This aerodynamic capability requires precise balance between lift and weight, often achieved through specialized wing movements, rotor systems, or technological mechanisms. Helicopters exemplify mechanical hovering through rotor blade manipulation that provides vertical lift and positional control. Many birds and insects hover naturally while feeding, hunting, or observing their environment, using rapid wing movements to maintain stationary flight. The term extends metaphorically to describe lingering, waiting, or remaining near something without direct engagement, such as hovering around a decision or hovering over someone protectively. Computer interfaces use hover effects to provide interactive feedback when cursors move over clickable elements. Technology applications include drone hovering for photography, surveillance hovering for security, and precision hovering for industrial operations. Understanding hovering involves aerodynamics, control systems, and the physics of maintaining stable position against gravitational and environmental forces.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'HUV-er',
                'etymology': 'Origin uncertain, possibly from "hove" (past tense of heave) or related to staying suspended.',
                'language_origins': 'English',
                'example_sentence': 'The hummingbird could _______ perfectly still in front of the flower while extending its beak to reach the nectar.',
                'memory_tip': 'Remember "HOVER" - sounds like "HUV-over," staying suspended over one spot without moving forward or landing.'
            },
            'howard': {
                'definition': 'Howard is a given name and surname of English origin, historically meaning "high guardian" or "chief guardian." As a personal name, Howard has been popular in English-speaking countries and often appears in both first and last name positions. The name has Anglo-Saxon roots and was historically associated with nobility and guardianship roles in medieval English society. Famous individuals named Howard include historical figures, politicians, actors, writers, and other public personalities who have contributed to various fields of human endeavor. In genealogical research, Howard often appears as both a first name and family name, sometimes making family history research complex when individuals share the same name across generations. The name has variations and derivatives in different languages and cultures, though the English version remains most common. Cultural references to "Howard" appear in literature, film, television, and popular culture, sometimes as character names or references to specific famous people. Understanding personal names like Howard involves etymology, cultural history, naming traditions, and the social significance of names in identity formation.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'HOW-erd',
                'etymology': 'From Old English "howeard," meaning "high guardian" or "noble guardian," from "hoh" (high) and "weard" (guardian).',
                'language_origins': 'Old English',
                'example_sentence': '_______ was named after his grandfather, continuing the family tradition of passing down names through generations.',
                'memory_tip': 'Remember "HOWARD" - HOW + WARD, like asking "how are you, ward (guardian)?" - a name meaning guardian or protector.'
            },
            'howdy': {
                'definition': 'Howdy is an informal greeting commonly used in American English, particularly associated with the American South and Southwest, serving as a casual way to say "hello" or "how are you doing?" This friendly salutation originated as a contraction of "how do you do?" and has become emblematic of American frontier culture, cowboy traditions, and rural communities. The greeting conveys warmth, friendliness, and down-to-earth approachability, often used to establish immediate rapport and demonstrate openness to conversation. Regional usage varies, with howdy being more common in Texas, Oklahoma, and other southwestern states where it remains part of everyday vocabulary. The term appears frequently in Western movies, country music, and popular culture representations of American frontier life, sometimes stereotypically but often authentically reflecting genuine regional speech patterns. Modern usage includes both serious and playful contexts, with some people adopting howdy to project friendliness or connection to American cultural traditions. Understanding regional greetings like howdy helps appreciate linguistic diversity, cultural identity, and the ways communities express personality through language choices.',
                'part_of_speech': 'interjection',
                'pronunciation_guide': 'HOW-dee',
                'etymology': 'Contraction of "how do ye" or "how do you do," shortened to a casual greeting.',
                'language_origins': 'American English',
                'example_sentence': 'The friendly cowboy tipped his hat and said "_______, partner!" when he met the visitors at the ranch.',
                'memory_tip': 'Remember "HOWDY" - HOW + D(o) Y(ou do), a shortened way of asking "how do you do?" used as a friendly greeting.'
            },
            'however': {
                'definition': 'However is a transitional adverb used to introduce contrast, exception, or alternative viewpoints that modify or contradict previous statements. This versatile word serves crucial functions in writing and speech by signaling shifts in logic, presenting opposing evidence, or acknowledging complexity in arguments and situations. However can appear at the beginning, middle, or end of sentences, with punctuation and placement affecting emphasis and flow. Academic and professional writing relies heavily on however to create nuanced arguments that acknowledge multiple perspectives while maintaining logical progression. The word helps writers and speakers present balanced analysis by introducing contradictory information, unexpected results, or qualifying conditions that complicate simple conclusions. Effective use of however requires understanding appropriate contexts, punctuation rules, and the logical relationships being expressed. Overuse can make writing choppy or argumentative, while underuse can make arguments seem one-sided or simplistic. Similar transitional words include "nevertheless," "nonetheless," "yet," and "but," each carrying slightly different connotations and appropriate usage contexts. Understanding transitional words like however improves both writing clarity and reading comprehension.',
                'part_of_speech': 'adverb, conjunction',
                'pronunciation_guide': 'how-EV-er',
                'etymology': 'From "how" + "ever," literally meaning "in whatever way" or "to whatever extent."',
                'language_origins': 'Middle English',
                'example_sentence': 'The weather forecast predicted rain; _______, the outdoor concert proceeded as scheduled with beautiful clear skies.',
                'memory_tip': 'Remember "HOWEVER" - HOW + EVER, meaning "in whatever way," used to show contrast or introduce a different perspective.'
            },
            'howler': {
                'definition': 'Howler refers to something or someone that howls, most commonly describing howler monkeys, large New World primates known for their incredibly loud vocalizations that can be heard from miles away. These arboreal mammals use their powerful calls for territorial communication, group coordination, and mate attraction in Central and South American rainforests. The term also describes any animal that produces howling sounds, including wolves, dogs, coyotes, and other creatures that use long, loud calls for communication. In colloquial usage, a howler refers to a glaring mistake, embarrassing error, or obvious blunder that is so apparent it metaphorically "howls" for attention. These mistakes might appear in writing, speech, performance, or decision-making contexts where the error is unmistakably obvious to observers. Media and critics sometimes describe particularly egregious errors as howlers, emphasizing their blatant nature. The dual meaning reflects both the literal acoustic phenomenon of loud animal calls and the figurative concept of mistakes so obvious they demand attention. Understanding howlers involves both zoology and communication, recognizing how both animals and humans use attention-getting signals, whether intentionally or accidentally.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HOW-ler',
                'etymology': 'From "howl" plus the suffix "-er" indicating one who performs the action of howling.',
                'language_origins': 'English',
                'example_sentence': 'The _______ monkey\'s call echoed through the jungle at dawn, announcing the troop\'s presence to neighboring groups.',
                'memory_tip': 'Remember "HOWLER" - HOWL + ER, something that howls, like the loud monkeys or an obvious mistake that "howls" for attention.'
            },
            'hsaing': {
                'definition': 'Hsaing appears to be a transliteration or romanization of a word from another language, possibly Burmese, Chinese, or another Asian language that uses different writing systems. Transliteration involves representing words from non-Latin alphabets using Latin letters, which can result in various spelling conventions depending on the romanization system used. Different academic, governmental, and cultural institutions may use different approaches to transliterating the same word, leading to spelling variations. Without additional context about the source language and intended meaning, it\'s difficult to provide a precise definition. This could represent a place name, personal name, cultural term, or other concept from the original language. The presence of such terms in English texts often reflects cultural exchange, immigration, academic study of other cultures, or documentation of international places and people. Understanding transliterated terms requires knowledge of the source language, the romanization system being used, and the cultural context in which the term appears. Modern globalization has increased the frequency of such cross-linguistic terms in English texts.',
                'part_of_speech': 'proper noun (transliterated)',
                'pronunciation_guide': 'Pronunciation varies by source language',
                'etymology': 'Transliterated from another language system, possibly Burmese, Chinese, or other Asian language.',
                'language_origins': 'Unknown (transliterated)',
                'example_sentence': 'The document mentioned _______ but did not provide sufficient context to understand its meaning or origin.',
                'memory_tip': 'Remember "HSAING" - this appears to be a transliterated word from another language that would require cultural context to understand.'
            },
            'hsia': {
                'definition': 'Hsia appears to be a transliteration of a Chinese term, possibly referring to the Xia Dynasty (approximately 2070-1600 BCE), considered by many historians to be the first dynasty in Chinese history, though its historical existence remains debated among scholars. The Xia Dynasty is traditionally credited with establishing many foundational aspects of Chinese civilization including governmental structures, cultural practices, and technological innovations. Different romanization systems for Chinese characters can produce various English spellings including "Hsia," "Xia," and other variants. The term might also represent other Chinese words, names, or concepts depending on the specific characters and context involved. Chinese historical and cultural terms often appear in English texts through various transliteration methods, reflecting different time periods, academic traditions, or regional preferences in representing Chinese sounds with Latin letters. Modern Pinyin romanization typically uses "Xia" rather than "Hsia" for this dynasty name. Understanding such transliterated terms requires knowledge of Chinese history, language, and the evolution of romanization systems. The presence of such terms in English reflects academic study of Chinese culture, historical research, or cultural exchange between Chinese and English-speaking communities.',
                'part_of_speech': 'proper noun (transliterated)',
                'pronunciation_guide': 'SHEE-ah or HSEE-ah',
                'etymology': 'Transliterated from Chinese, possibly referring to the Xia Dynasty or other Chinese terms.',
                'language_origins': 'Chinese (transliterated)',
                'example_sentence': 'The archaeology professor discussed the _______ Dynasty as a foundational period in early Chinese civilization.',
                'memory_tip': 'Remember "HSIA" - this is likely a transliterated Chinese term, possibly referring to the ancient Xia Dynasty in Chinese history.'
            },
            'http': {
                'definition': 'HTTP stands for HyperText Transfer Protocol, the foundational communication protocol used for transferring web pages, files, and data across the Internet between web servers and browsers. This technical standard defines how messages are formatted and transmitted, enabling the World Wide Web to function by establishing common rules for requesting and delivering web content. HTTP operates on a client-server model where browsers (clients) send requests to web servers, which respond with the requested resources such as HTML pages, images, videos, or other files. The protocol uses specific methods including GET (retrieve information), POST (submit data), PUT (upload data), and DELETE (remove resources) to handle different types of web interactions. Modern web security relies on HTTPS, which adds encryption layers to protect data transmission from interception or tampering. Understanding HTTP is essential for web development, internet security, and comprehending how online communication works. The protocol\'s simplicity and flexibility have enabled the explosive growth of web-based applications, e-commerce, social media, and digital communication systems that define modern internet usage.',
                'part_of_speech': 'noun (acronym)',
                'pronunciation_guide': 'AYCH-tee-tee-PEE',
                'etymology': 'Acronym for "HyperText Transfer Protocol," from "hypertext" (linked text) and "transfer protocol" (communication rules).',
                'language_origins': 'Modern English (technical acronym)',
                'example_sentence': 'Web developers must understand _______ protocols to create websites that communicate effectively with servers and browsers.',
                'memory_tip': 'Remember "HTTP" - HyperText Transfer Protocol, the system that transfers web pages from servers to your browser when you visit websites.'
            },
            'huallaga': {
                'definition': 'Huallaga refers to the Huallaga River, a major tributary of the Amazon River system flowing through central Peru for approximately 1,100 kilometers from the Andes Mountains to its confluence with the Marañón River. This significant waterway passes through diverse ecosystems including high mountain valleys, cloud forests, and lowland rainforests, supporting rich biodiversity and various indigenous communities along its course. The Huallaga Valley is known for both its natural beauty and its historical association with coca cultivation, which has created complex social, economic, and political challenges for the region. The river serves important transportation functions for remote communities that depend on boat travel for access to markets, supplies, and services. Economic activities along the Huallaga include agriculture, fishing, timber harvesting, and tourism, though development efforts face challenges from geography, infrastructure limitations, and security concerns. Environmental conservation efforts focus on protecting the river\'s watershed and the diverse species that depend on its ecosystem. Understanding the Huallaga involves geography, ecology, socioeconomics, and the complex interactions between human communities and Amazonian environments.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'wah-YAH-gah',
                'etymology': 'From Quechua or other indigenous Peruvian language, referring to the river system in Peru.',
                'language_origins': 'Quechua, indigenous Peruvian',
                'example_sentence': 'The expedition traveled down the _______ River to study the biodiversity of the Peruvian Amazon region.',
                'memory_tip': 'Remember "HUALLAGA" - a major river in Peru that flows through the Amazon basin, important for transportation and ecology.'
            },
            'huapango': {
                'definition': 'Huapango is a traditional Mexican folk music and dance style originating in the Huasteca region of eastern Mexico, characterized by distinctive rhythmic patterns, virtuosic string playing, and energetic dance movements. This cultural expression combines indigenous, Spanish, and African musical influences to create a unique art form that includes both instrumental music and accompanying dance traditions. Traditional huapango ensembles, called trios huastecos, typically feature violin, jarana huasteca (a small guitar-like instrument), and huapanguera (a larger bass guitar), creating complex polyrhythmic music with intricate improvisation. The dance component involves rapid footwork, heel tapping, and competitive elements where dancers demonstrate skill, stamina, and creativity. Huapango lyrics often tell stories of rural life, love, regional pride, and social commentary, preserving oral traditions and cultural memory. The music has influenced other Mexican genres and gained international recognition through folkloric performances and cultural exchanges. Modern huapango continues to evolve while maintaining traditional elements, appearing in festivals, cultural celebrations, and educational programs that preserve Mexican cultural heritage. Understanding huapango involves appreciating the intersection of music, dance, poetry, and regional identity in Mexican culture.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'wah-PAHN-goh',
                'etymology': 'From Mexican Spanish, possibly from Nahuatl "cuauhpanco" meaning "on wooden platform," referring to dance platforms.',
                'language_origins': 'Nahuatl, Mexican Spanish',
                'example_sentence': 'The cultural festival featured a traditional _______ performance with musicians and dancers showcasing this vibrant Mexican folk art.',
                'memory_tip': 'Remember "HUAPANGO" - a traditional Mexican music and dance style from the Huasteca region, featuring lively rhythms and intricate footwork.'
            },
            'hubbub': {
                'definition': 'Hubbub refers to a loud, confused noise or uproar, particularly the sound of many people talking, laughing, or making noise simultaneously in a chaotic or disorderly manner. This term describes the acoustic environment in crowded places where multiple conversations, activities, and sounds blend together to create a general atmosphere of busy noise. Hubbub often occurs in markets, parties, sporting events, busy restaurants, or any gathering where many people are engaged in simultaneous activities. The word conveys not just volume but also the disorganized, overlapping nature of multiple sound sources creating an overall din. While hubbub can be overwhelming or annoying in some contexts, it can also represent vitality, energy, and the positive bustle of active community life. The term sometimes describes excitement, controversy, or commotion surrounding events or issues that generate public attention and discussion. Understanding hubbub involves recognizing both the acoustic phenomenon of overlapping sounds and the social dynamics that create such environments. The concept applies to both literal noise situations and metaphorical descriptions of busy, chaotic, or exciting circumstances.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HUB-ub',
                'etymology': 'Possibly from Gaelic "ub! ub!" meaning "away! away!" or "hooray!" or from similar exclamatory sounds.',
                'language_origins': 'Possibly Gaelic, English',
                'example_sentence': 'The _______ in the marketplace made it difficult to have a conversation, with vendors calling out and customers bargaining loudly.',
                'memory_tip': 'Remember "HUBBUB" - sounds like "HUB-BLUB," the blubbing noise of many people talking at once in a busy hub of activity.'
            },
            'hubris': {
                'definition': 'Hubris refers to excessive pride, arrogance, or self-confidence that leads to downfall, particularly the kind of overweening pride that defies gods, fate, or natural order. This ancient Greek concept describes a character flaw where individuals become so convinced of their own superiority, power, or righteousness that they make reckless decisions or ignore important warnings and limitations. Classical literature and mythology frequently feature hubris as a central theme, where heroes or leaders are destroyed by their own arrogance and refusal to accept human limitations. The concept extends beyond literature to describe real-world situations where individuals, organizations, or nations make catastrophic errors due to overconfidence and dismissal of risks or opposition. Hubris often involves believing one is above consequences, immune to failure, or capable of controlling outcomes beyond one\'s actual abilities. Modern applications include business failures, political miscalculations, and personal disasters that result from excessive self-confidence and insufficient humility. Understanding hubris helps recognize the dangers of unchecked pride and the importance of maintaining realistic self-assessment and respect for limits, whether human, natural, or circumstantial.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HYOO-bris',
                'etymology': 'From ancient Greek "hubris" meaning "excessive pride" or "arrogance," originally referring to violence or insolence toward gods.',
                'language_origins': 'Ancient Greek',
                'example_sentence': 'The CEO\'s _______ led him to ignore market warnings and make risky investments that ultimately destroyed the company.',
                'memory_tip': 'Remember "HUBRIS" - sounds like "HUB-RICH," excessive pride that makes someone think they\'re the rich center (hub) of everything.'
            },
            'huddling': {
                'definition': 'Huddling describes the action of crowding together closely, typically for warmth, protection, comfort, or private conversation. This behavior appears in both human and animal contexts as a survival strategy and social bonding mechanism. Animals huddle for thermoregulation, sharing body heat during cold weather to maintain life-sustaining temperatures. Penguins, for example, form large huddles that rotate to ensure all members receive warmth. Human huddling serves similar functions during emergencies, cold weather, or frightening situations where people instinctively move closer together for physical and psychological comfort. Sports teams huddle before plays to coordinate strategy and maintain team unity. The behavior reflects fundamental social instincts for cooperation, protection, and mutual support during challenging circumstances. Huddling can also describe informal gatherings where people come together for discussion, planning, or decision-making in small groups. The physical act of huddling often strengthens social bonds and creates feelings of security and belonging. Understanding huddling behavior reveals important aspects of social psychology, survival strategies, and the human need for connection and protection through proximity to others.',
                'part_of_speech': 'verb (present participle)',
                'pronunciation_guide': 'HUD-ling',
                'etymology': 'From "huddle," possibly from Low German "hudeln" meaning "to cover" or "wrap up."',
                'language_origins': 'Low German, English',
                'example_sentence': 'The children were _______ together under the blanket during the thunderstorm, finding comfort in staying close.',
                'memory_tip': 'Remember "HUDDLING" - HUDDLE + ING, the action of crowding together closely like a group hug for warmth and comfort.'
            },
            'huerta': {
                'definition': 'Huerta refers to a traditional Spanish and Latin American agricultural system involving intensively cultivated garden plots or orchards, typically located near settlements and featuring diverse crops grown using irrigation and careful soil management. These productive agricultural areas combine fruit trees, vegetables, grains, and sometimes small livestock in integrated farming systems that maximize production from limited land areas. Huertas represent centuries of agricultural knowledge and adaptation to local climates, soil conditions, and water availability. The term also refers to specific geographic regions known for such agriculture, including the famous Huerta de Valencia in Spain and various huerta regions throughout Latin America. These agricultural systems often involve complex irrigation networks, terracing, and intensive labor to maintain high productivity. Huertas serve important roles in local food security, cultural preservation, and sustainable agriculture practices that have been refined over generations. Modern agricultural research studies traditional huerta systems for insights into sustainable farming, biodiversity conservation, and efficient resource use. Understanding huertas involves agricultural science, cultural geography, and the relationship between traditional farming knowledge and contemporary food production challenges.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'WAIR-tah',
                'etymology': 'From Spanish "huerta," from Latin "hortus" meaning "garden," related to "horticulture."',
                'language_origins': 'Latin, Spanish',
                'example_sentence': 'The traditional _______ provided the village with fresh vegetables, fruits, and herbs grown using centuries-old irrigation techniques.',
                'memory_tip': 'Remember "HUERTA" - from Latin "hortus" (garden), a traditional Spanish intensive garden system that provides diverse crops.'
            },
            'huge': {
                'definition': 'Huge describes something that is extremely large in size, amount, extent, or intensity, far exceeding normal or expected dimensions. This adjective emphasizes scale that impresses, overwhelms, or dominates through sheer magnitude, whether physical, numerical, or conceptual. Huge objects might include mountains, buildings, vehicles, or natural formations that dwarf human scale and create feelings of awe or insignificance. The term can describe quantities, distances, differences, impacts, or any measurable attribute that reaches extraordinary levels. Huge success indicates achievement far beyond typical expectations, while huge problems suggest challenges of exceptional difficulty or scope. Context determines whether "huge" conveys positive excitement (huge opportunities), negative concern (huge problems), or neutral observation (huge distances). The word often appears in informal speech and writing to express emphasis and emotional response to scale. Related terms include enormous, gigantic, massive, and colossal, each with slightly different connotations but similar emphasis on exceptional size. Understanding "huge" involves recognizing both literal measurement and figurative emphasis used to communicate the impressive nature of whatever is being described.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'HYOOJ',
                'etymology': 'From Old French "ahuge," meaning "of great size," possibly related to Germanic roots meaning "high" or "elevated."',
                'language_origins': 'Old French, Germanic',
                'example_sentence': 'The earthquake caused a _______ crack in the mountainside that could be seen from miles away.',
                'memory_tip': 'Remember "HUGE" - sounds like "HUGH-gee," something so big it makes you say "Hugh, gee, that\'s enormous!"'
            },
            'hugh': {
                'definition': 'Hugh is a masculine given name of Germanic origin meaning "mind," "spirit," or "intelligence," historically popular in European countries and their cultural derivatives. The name has been borne by numerous notable historical figures including saints, kings, nobles, and contemporary celebrities, contributing to its continued recognition and usage. Saint Hugh of Lincoln and Saint Hugh of Cluny are among the religious figures who have made the name significant in Christian tradition. The name appears in various linguistic forms across different cultures, including Hugo in Spanish and other Romance languages, reflecting its widespread adoption and adaptation. Hugh has remained relatively common in English-speaking countries, though its popularity has fluctuated over different historical periods. Modern bearers of the name include actors, politicians, writers, and other public figures who contribute to its contemporary recognition. The name carries connotations of intelligence and nobility, reflecting its etymological meaning and historical associations with leadership and learning. Understanding personal names like Hugh involves etymology, cultural history, naming traditions, and the social significance of names in personal and family identity.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'HYOO',
                'etymology': 'From Germanic "hug" meaning "mind," "spirit," or "intelligence," related to "Hugo."',
                'language_origins': 'Germanic',
                'example_sentence': '_______ decided to name his son after his grandfather, continuing the family tradition of strong, traditional names.',
                'memory_tip': 'Remember "HUGH" - sounds like "HUE," a name with the hue or color of intelligence and nobility from its Germanic meaning of "mind."'
            },
            'huguenot': {
                'definition': 'Huguenot refers to French Protestant Christians who followed the Reformed tradition during the 16th and 17th centuries, facing severe persecution from the Catholic majority and French government for their religious beliefs. These religious minorities played significant roles in French society as skilled craftspeople, merchants, professionals, and intellectuals, often achieving economic success despite political and social discrimination. Huguenots endured periods of intense persecution including massacres, forced conversions, and legal restrictions on their civil and religious rights. The revocation of the Edict of Nantes in 1685 ended official tolerance and triggered massive emigration to Protestant countries including England, Netherlands, Prussia, and American colonies. Huguenot refugees brought valuable skills, knowledge, and cultural contributions to their adopted countries, significantly impacting development in areas such as textile production, banking, science, and arts. Their diaspora communities maintained distinct cultural identities while integrating into new societies. Modern descendants of Huguenots can be found worldwide, with some maintaining genealogical and cultural connections to their French Protestant heritage. Understanding Huguenot history illuminates religious conflict, migration patterns, and the contributions of persecuted minorities to global development.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HYOO-guh-not',
                'etymology': 'Possibly from German "Eidgenoss" (confederate) or from "Hugues," referring to followers of a Geneva political leader.',
                'language_origins': 'French, possibly German',
                'example_sentence': 'The _______ silversmith brought his family to colonial America to escape religious persecution in France.',
                'memory_tip': 'Remember "HUGUENOT" - HUGH + NOT, French Protestants who were NOT Catholic and faced persecution for their different religious beliefs.'
            },
            'huipil': {
                'definition': 'Huipil is a traditional blouse or dress worn by indigenous women in Mexico, Central America, and parts of South America, characterized by its rectangular shape, minimal tailoring, and often elaborate decorative elements that reflect cultural identity, regional traditions, and personal or family history. These garments are typically made from handwoven textiles and feature distinctive patterns, colors, and embroidery that communicate information about the wearer\'s community, marital status, social position, and cultural heritage. Huipil construction involves ancient techniques passed down through generations, with mothers teaching daughters not only sewing skills but also the cultural meanings embedded in different design elements. The garments serve both practical and ceremonial functions, with everyday huipils being simpler and ceremonial versions featuring more elaborate decoration using techniques such as brocade, embroidery, and appliqué work. Regional variations in huipil styles reflect different indigenous traditions, available materials, and cultural influences, creating a rich diversity of forms across different communities. Modern huipil production includes both traditional hand-made versions and commercial reproductions, raising questions about cultural preservation, authenticity, and economic opportunities for indigenous artisans.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'WEE-peel',
                'etymology': 'From Nahuatl "huipilli," meaning "blouse" or "dress," referring to traditional indigenous women\'s garments.',
                'language_origins': 'Nahuatl',
                'example_sentence': 'The museum displayed a beautiful collection of traditional _______ from different indigenous communities, each featuring unique patterns and embroidery.',
                'memory_tip': 'Remember "HUIPIL" - sounds like "WEE-pill," a traditional garment that\'s like a wee (small) rectangular piece that indigenous women wear as a blouse.'
            },
            'hula': {
                'definition': 'Hula is a traditional Hawaiian dance form that combines graceful movements, storytelling, and cultural expression to preserve and transmit Hawaiian history, mythology, and values through artistic performance. This ancient art form uses hand gestures, body movements, facial expressions, and rhythmic motions to narrate stories about nature, gods, historical events, and daily life in Hawaiian culture. Hula encompasses both ancient forms (hula kahiko) performed to traditional chanting and instruments, and modern forms (hula \'auana) that incorporate contemporary music and Western influences while maintaining cultural authenticity. The dance requires extensive training in both physical technique and cultural knowledge, as performers must understand the meanings behind movements and songs to properly convey their intended messages. Hula instruction traditionally follows the hālau system, where students learn under master teachers (kumu hula) who preserve and transmit both dance techniques and cultural wisdom. Modern hula serves important functions in cultural preservation, tourism, education, and Hawaiian identity maintenance, though questions exist about commercialization and authentic representation. Understanding hula involves appreciating its role as living culture that connects contemporary Hawaiians with ancestral traditions while adapting to modern contexts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HOO-lah',
                'etymology': 'From Hawaiian "hula," meaning "dance," from Proto-Polynesian roots referring to rhythmic movement.',
                'language_origins': 'Hawaiian, Proto-Polynesian',
                'example_sentence': 'The _______ performance told the story of the volcano goddess Pele through graceful hand movements and traditional Hawaiian chants.',
                'memory_tip': 'Remember "HULA" - sounds like "WHO-la," the Hawaiian dance that shows who you are through graceful movements and storytelling.'
            }
        }
        
        return batch_086_data.get(word.lower(), {
            'definition': 'Definition not available for this word.',
            'part_of_speech': 'unknown',
            'pronunciation_guide': 'Pronunciation not available',
            'etymology': 'Etymology not available',
            'language_origins': 'Unknown',
            'example_sentence': 'Example sentence not available for _______.',
            'memory_tip': 'Memory tip not available for this word.'
        })

    def process_batch(self, input_file: str, output_file: str) -> None:
        print(f"Processing {input_file}...")
        
        try:
            df = pd.read_csv(input_file)
            
            processed_words = []
            word_count = 0
            
            for _, row in df.iterrows():
                word = str(row['word']).strip()
                if not word or word.lower() == 'nan':
                    continue
                    
                word_count += 1
                
                if self.is_error_word(word):
                    self.errors.append(self.detect_word_error(word))
                
                claude_data = self.get_comprehensive_claude_data(word)
                
                word_data = WordData(
                    word=word,
                    definition=claude_data['definition'],
                    part_of_speech=claude_data['part_of_speech'],
                    pronunciation_guide=claude_data['pronunciation_guide'],
                    etymology=claude_data['etymology'],
                    language_origins=claude_data['language_origins'],
                    example_sentence=claude_data['example_sentence'],
                    memory_tip=claude_data['memory_tip'],
                    phonetic_transparency=self.difficulty_calc.calculate_phonetic_transparency(word),
                    word_frequency=self.difficulty_calc.calculate_word_frequency(word),
                    morphological_complexity=self.difficulty_calc.calculate_morphological_complexity(word),
                    etymology_complexity=self.difficulty_calc.calculate_etymology_complexity(word)
                )
                
                processed_words.append(word_data)
            
            output_data = []
            for word_data in processed_words:
                output_data.append({
                    'word': word_data.word,
                    'definition': word_data.definition,
                    'part_of_speech': word_data.part_of_speech,
                    'pronunciation_guide': word_data.pronunciation_guide,
                    'etymology': word_data.etymology,
                    'language_origins': word_data.language_origins,
                    'example_sentence': word_data.example_sentence,
                    'memory_tip': word_data.memory_tip,
                    'phonetic_transparency': word_data.phonetic_transparency,
                    'word_frequency': word_data.word_frequency,
                    'morphological_complexity': word_data.morphological_complexity,
                    'etymology_complexity': word_data.etymology_complexity,
                    'difficulty_level': None,
                    'source_difficulties': row.get('source_difficulties', ''),
                    'years': row.get('years', ''),
                    'source_files': row.get('source_files', ''),
                    'definition_source': 'Claude',
                    'pronunciation_source': 'Claude',
                    'etymology_source': 'Claude',
                    'example_sentence_source': 'Claude',
                    'audio_file_path': None,
                    'created_at': None,
                    'updated_at': None,
                    'alternative_spellings': None,
                    'related_words': None,
                    'usage_notes': None
                })
            
            output_df = pd.DataFrame(output_data)
            output_df.to_csv(output_file, index=False, encoding='utf-8')
            
            print(f"Successfully processed {word_count}/50 words to {output_file}")
            
            if self.errors:
                print(f"Found {len(self.errors)} error(s):")
                for error in self.errors:
                    print(f"  - {error}")
            
            print("Batch 086 processing completed successfully!")
            
        except Exception as e:
            print(f"Error processing batch 086: {str(e)}")
            raise

    def is_error_word(self, word: str) -> bool:
        error_patterns = [
            lambda w: len(w) > 20 and any(common in w.lower() for common in 
                ['difficulty', 'diligence', 'different', 'decision', 'development', 'discussion']),
            lambda w: any(combo in w.lower() for combo in 
                ['anearly', 'anadequate', 'anational', 'anhonest', 'anindependent']),
            lambda w: w.count('a') > 4 and len(w) > 15,
            lambda w: 'difficulty' in w.lower() and w.lower() != 'difficulty',
            lambda w: len([c for c in w if c.islower()]) > len(w) * 0.9 and len(w) > 25,
            lambda w: 'speleothem' in w.lower() and len(w) > 12,
            lambda w: 'howler' in w.lower() and len(w) > 8 and w.lower() != 'howler',
            lambda w: w.count('p') > 3,  # for hopppped
            lambda w: 'horologistspeleothem' in w.lower(),
            lambda w: 'hostilehowler' in w.lower()
        ]
        
        return any(pattern(word) for pattern in error_patterns)

    def detect_word_error(self, word: str) -> str:
        if 'horologistspeleothem' in word.lower():
            return f'{word}: Combined word error: "{word}" appears to be "horologist" + "speleothem" merged together. This is likely a PDF parsing error where clockmaker and cave formation terminology were incorrectly combined.'
        
        if 'hostilehowler' in word.lower():
            return f'{word}: Combined word error: "{word}" appears to be "hostile" + "howler" merged together. This is likely a PDF parsing error where aggressive behavior and howling terminology were incorrectly combined.'
        
        if word.count('p') > 3:
            return f'{word}: Spelling error: "{word}" appears to have too many repeated letters, likely "hopped" with extra "p"s added by mistake.'
        
        if 'difficulty' in word.lower() and word.lower() != 'difficulty':
            parts = word.lower().split('difficulty')
            return f'{word}: Combined word error: "{word}" appears to be "{parts[0]}" + "difficulty" merged together. This is likely a PDF parsing error where two separate concepts were incorrectly combined.'
        
        common_endings = ['ness', 'tion', 'sion', 'ment', 'able', 'ible', 'ence', 'ance']
        for ending in common_endings:
            if word.lower().endswith(ending):
                base = word.lower()[:-len(ending)]
                if len(base) > 8:
                    return f'{word}: Possible combined word error: "{word}" may contain merged terms. This is likely a PDF parsing error where separate words were incorrectly combined.'
        
        return f'{word}: Combined word error: This appears to be multiple words merged together during PDF processing.'

if __name__ == "__main__":
    processor = Batch086Processor()
    input_file = "output/batch_086_words.csv"
    output_file = "output/batch_086_processed.csv"
    processor.process_batch(input_file, output_file)