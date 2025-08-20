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

class Batch069Processor:
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def detect_parsing_errors(self, word: str) -> Tuple[bool, bool, List[str]]:
        errors = []
        combined_detected = False
        incomplete_detected = False
        
        # Check for combined words (specific to this batch)
        combined_word_patterns = {
            'flaxentriplicate': ['flaxen', 'triplicate'],
            'flexibleskeleton': ['flexible', 'skeleton'],
            'floruitbunyanesque': ['floruit', 'bunyanesque'],
            'flotusfluoride': ['flotus', 'fluoride'],
            'focacciapahoehoe': ['focaccia', 'pahoehoe']
        }
        
        if word.lower() in combined_word_patterns:
            combined_detected = True
            errors.append(f"Combined word error: \"{word}\" appears to be {' + '.join(combined_word_patterns[word.lower()])} merged together. This is likely a PDF parsing error where two separate words were incorrectly combined.")
        
        return combined_detected, incomplete_detected, errors
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Generate comprehensive educational data for spelling bee words using Claude's knowledge."""
        
        batch_069_data = {
            'flea': {
                'definition': 'A flea is a small, wingless insect that feeds on the blood of mammals and birds as an external parasite. These tiny insects are known for their exceptional jumping ability, which can propel them many times their body length. Fleas have laterally compressed bodies and specialized mouthparts for piercing skin and sucking blood. They are common pests that can transmit diseases and cause irritation to their hosts. Fleas undergo complete metamorphosis and can survive for extended periods without feeding.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLEE',
                'etymology': 'From Old English "fleah," related to similar words in other Germanic languages, ultimately referring to the jumping insect.',
                'language_origins': 'Old English',
                'example_sentence': 'The veterinarian recommended a special shampoo to eliminate the _______ infestation on the dog.',
                'memory_tip': 'Remember "FLEA" - a tiny insect that makes you want to FLEE because it bites and jumps around.'
            },
            'flecked': {
                'definition': 'Flecked describes something that is marked with small spots, specks, or patches of color or texture that stand out from the main surface. When something is flecked, it has a speckled or spotted appearance, often creating visual interest through the contrast between the base color and the small markings. This can occur naturally, as in flecked granite or bird eggs, or artificially, as in flecked paint or fabric patterns.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'FLEKT',
                'etymology': 'From "fleck," possibly from Middle English "flekken," related to similar words meaning "spot" in Germanic languages.',
                'language_origins': 'Middle English, Germanic',
                'example_sentence': 'The artist\'s canvas was _______ with tiny drops of gold paint that caught the light beautifully.',
                'memory_tip': 'Remember "FLECKED" - decorated with FLECKS (tiny spots), like being CHECKED with small markings.'
            },
            'fleeciness': {
                'definition': 'Fleeciness is the quality or state of being fleecy, characterized by softness, wooliness, or a fluffy, cloud-like texture. This abstract noun describes the physical characteristic of materials that resemble sheep\'s fleece in their soft, thick, and often curly or matted appearance. Fleeciness can apply to actual wool, synthetic fabrics designed to mimic wool, clouds, or any surface that has a soft, fluffy, fleece-like quality.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLEE-see-nis',
                'etymology': 'From "fleecy" (from "fleece," from Old English "fleos") plus the suffix "-iness" indicating a quality or state.',
                'language_origins': 'Old English',
                'example_sentence': 'The _______ of the new blanket made it incredibly comfortable for cold winter nights.',
                'memory_tip': 'Remember "FLEECI-ness" - the quality of being soft and fluffy like a sheep\'s FLEECE, full of cozy comfort.'
            },
            'fleetness': {
                'definition': 'Fleetness is the quality of being fleet, meaning swiftness, speed, or rapidity of movement. This noun describes the characteristic of moving quickly and gracefully, often with an emphasis on agility and nimbleness rather than just raw speed. Fleetness can apply to runners, animals, vehicles, or even abstract concepts like the fleetness of time. The word suggests not only speed but also elegance and efficiency in movement.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLEET-nis',
                'etymology': 'From "fleet" (from Old English "fleot" meaning "swift") plus the suffix "-ness" indicating a quality or state.',
                'language_origins': 'Old English',
                'example_sentence': 'The gazelle\'s _______ allowed it to escape from predators across the African savanna.',
                'memory_tip': 'Remember "FLEET-ness" - the quality of being part of a swift FLEET, moving with speed and grace.'
            },
            'flehmen': {
                'definition': 'Flehmen is a behavioral response in which animals, particularly mammals, curl back their lips and inhale through their mouth to better detect scents through their vomeronasal organ. This distinctive facial expression allows animals to analyze chemical signals, pheromones, and other airborne substances more effectively. The flehmen response is commonly observed in horses, cats, snakes, and many other species as part of their chemosensory behavior for gathering information about their environment.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FLAY-men',
                'etymology': 'From German "flehmen" meaning "to curl the upper lip," describing the characteristic facial expression during this behavior.',
                'language_origins': 'German',
                'example_sentence': 'The stallion exhibited the _______ response, curling his lip to better analyze the mare\'s scent.',
                'memory_tip': 'Remember "FLEH-men" - when animals make a weird facial expression to SMELL better, curling their lips to analyze scents.'
            },
            'flexitarian': {
                'definition': 'A flexitarian is a person who follows a primarily vegetarian diet but occasionally eats meat or fish. This dietary approach allows for flexibility in food choices while maintaining a focus on plant-based nutrition. Flexitarians typically reduce their meat consumption for health, environmental, or ethical reasons while not completely eliminating animal products from their diet. This eating pattern represents a middle ground between vegetarianism and omnivorous diets.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'flek-si-TAIR-ee-an',
                'etymology': 'Portmanteau combining "flexible" and "vegetarian," coined in the early 2000s to describe this dietary approach.',
                'language_origins': 'English (modern coinage)',
                'example_sentence': 'As a _______, she mostly ate vegetables and grains but enjoyed fish once or twice a week.',
                'memory_tip': 'Remember "FLEXI-tarian" - someone who\'s FLEXIBLE about their vegetarian diet, bending the rules occasionally.'
            },
            'flight': {
                'definition': 'Flight refers to the action or process of flying through the air, whether by birds, aircraft, or other objects capable of aerial movement. The word can describe the physical act of moving through air, a journey by aircraft, or a series of steps or stairs. Flight can also mean a hasty departure or escape from danger. In various contexts, flight represents movement through space, escape, or elevation above the ground.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLYHT',
                'etymology': 'From Old English "flyht," related to "fly," ultimately from the Germanic root meaning "to move through air."',
                'language_origins': 'Old English',
                'example_sentence': 'The eagle\'s graceful _______ over the canyon demonstrated the majesty of natural aviation.',
                'memory_tip': 'Remember "FLIGHT" - the act of flying through air, whether by birds taking LIGHT to the sky or planes in flight.'
            },
            'flimflammer': {
                'definition': 'A flimflammer is a person who deceives others through confidence tricks, fraudulent schemes, or smooth-talking swindles. This term describes someone who uses charm, persuasion, and deceptive practices to cheat people out of their money or valuables. Flimflammers are skilled at gaining trust quickly and creating elaborate stories or scenarios to convince their victims to part with their resources. The word emphasizes the deceptive and manipulative nature of such individuals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLIM-flam-er',
                'etymology': 'From "flimflam" (meaning nonsense or deception, possibly imitative of meaningless chatter) plus the agent suffix "-er."',
                'language_origins': 'English',
                'example_sentence': 'The elderly woman was fortunately warned about the _______ who was targeting seniors in her neighborhood.',
                'memory_tip': 'Remember "FLIM-flammer" - a scammer who uses FLIMSY lies and SLAMS you with deceptive tricks to steal your money.'
            },
            'flimsy': {
                'definition': 'Flimsy describes something that is weak, fragile, or lacking in substance, strength, or credibility. When something is flimsy, it is easily damaged, broken, or seen through, whether physically or metaphorically. Flimsy can describe thin materials that tear easily, weak arguments that don\'t hold up to scrutiny, or excuses that are obviously false. The word emphasizes inadequacy, weakness, and lack of durability or believability.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FLIM-zee',
                'etymology': 'Of uncertain origin, possibly from "film" plus the diminutive suffix "-sy," suggesting something thin and weak.',
                'language_origins': 'English (uncertain origin)',
                'example_sentence': 'His _______ excuse for being late was quickly exposed when his friends saw his social media posts.',
                'memory_tip': 'Remember "FLIM-sy" - weak and thin like a FILM that\'s easy to see through, not substantial or believable.'
            },
            'flinch': {
                'definition': 'Flinch means to make a quick, nervous movement away from something threatening, painful, or unpleasant. When someone flinches, they instinctively recoil or draw back in response to anticipated pain, danger, or discomfort. This reaction can be physical, such as pulling away from a hot surface, or emotional, such as avoiding a difficult conversation. Flinching represents a natural protective response to perceived threats.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'FLINCH',
                'etymology': 'From Old French "flenchir" meaning "to bend" or "to turn aside," related to the idea of moving away from something.',
                'language_origins': 'Old French',
                'example_sentence': 'She didn\'t _______ when the nurse prepared to give her the vaccination shot.',
                'memory_tip': 'Remember "FLINCH" - to quickly move away like you got PINCHED, reacting instinctively to avoid pain.'
            },
            'flippancy': {
                'definition': 'Flippancy is a disrespectful or inappropriate lack of seriousness, especially when dealing with subjects that deserve thoughtful consideration. This noun describes an attitude characterized by casual dismissal, irreverent humor, or frivolous treatment of important matters. Flippancy often involves making light of serious situations or showing insufficient respect for the gravity of circumstances. The behavior can be offensive or hurtful when applied to sensitive topics.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLIP-an-see',
                'etymology': 'From "flippant" (possibly from "flip," meaning to toss lightly) plus the suffix "-ancy" indicating a state or quality.',
                'language_origins': 'English',
                'example_sentence': 'His _______ during the serious discussion about budget cuts angered his colleagues.',
                'memory_tip': 'Remember "FLIPP-ancy" - treating serious matters as if you can just FLIP them away, showing inappropriate casualness.'
            },
            'flipperling': {
                'definition': 'A flipperling appears to be a young seal or similar marine mammal with flippers, particularly referring to a juvenile in its early stages of development. This term would describe a small, young pinniped (seal, sea lion, or walrus) that is still dependent on its mother and learning to use its flippers for swimming and movement. The diminutive suffix suggests something small and endearing, emphasizing the young age and cute appearance of the animal.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLIP-er-ling',
                'etymology': 'From "flipper" (the limb of marine mammals) plus the diminutive suffix "-ling" indicating something young or small.',
                'language_origins': 'English',
                'example_sentence': 'The marine biologist observed the _______ learning to swim alongside its mother in the protected cove.',
                'memory_tip': 'Remember "FLIPPER-ling" - a little baby seal with tiny FLIPPERS, a small marine mammal still learning to swim.'
            },
            'flittern': {
                'definition': 'A flittern is a variant or dialectal term for a bat, referring to these nocturnal flying mammals that flit through the air hunting insects. The word emphasizes the erratic, fluttering flight pattern characteristic of bats as they navigate using echolocation. Flittern captures the quick, darting movements and unpredictable flight paths that bats display while hunting or traveling. This term may be more commonly used in certain regional dialects or historical contexts.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLIT-ern',
                'etymology': 'From "flit" (to move lightly and quickly) plus a suffix, referring to the fluttering flight of bats.',
                'language_origins': 'English (dialectal)',
                'example_sentence': 'As dusk approached, the first _______ emerged from the cave to begin its nightly hunt for insects.',
                'memory_tip': 'Remember "FLIT-tern" - a bat that FLITS around in a TERN-like (bird-like) pattern, darting through the air.'
            },
            'flitting': {
                'definition': 'Flitting describes moving lightly and quickly from one place to another, often in a brief, temporary, or restless manner. When something is flitting, it demonstrates rapid, light movement that typically doesn\'t linger in any one location for long. The word can describe the movement of birds, butterflies, thoughts, or people who move quickly and briefly from place to place. Flitting suggests graceful, effortless movement with frequent changes in position.',
                'part_of_speech': 'verb (present participle), adjective',
                'pronunciation_guide': 'FLIT-ing',
                'etymology': 'From "flit," possibly from Old Norse "flytja" meaning "to move" or "to carry," plus the participial suffix "-ing."',
                'language_origins': 'Old Norse',
                'example_sentence': 'The butterfly spent the afternoon _______ from flower to flower in the garden.',
                'memory_tip': 'Remember "FLIT-ting" - moving quickly and lightly, like something that FITs from place to place without staying long.'
            },
            'float': {
                'definition': 'Float means to rest or move on the surface of a liquid without sinking, or to move gently through air or space. As a noun, float can refer to a buoyant object that helps things stay on water\'s surface, a decorated vehicle in a parade, or a sum of money kept for making change. The word emphasizes buoyancy, lightness, and the ability to remain suspended without support from below.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'FLOHT',
                'etymology': 'From Old English "flotian," related to "fleet" and similar words meaning "to swim" or "to flow."',
                'language_origins': 'Old English',
                'example_sentence': 'The cork will _______ on top of the water because it\'s less dense than the liquid.',
                'memory_tip': 'Remember "FLOAT" - to stay on top of water like a boat, suspended without sinking down.'
            },
            'flooey': {
                'definition': 'Flooey is an informal exclamation or adjective meaning askew, awry, or not functioning properly. When something has gone flooey, it has malfunctioned, failed, or gone wrong in some way. This colloquial term is often used to describe mechanical failures, plans that don\'t work out, or situations that have become confused or chaotic. The word has a somewhat humorous or light-hearted tone despite describing problems or failures.',
                'part_of_speech': 'adjective, interjection',
                'pronunciation_guide': 'FLOO-ee',
                'etymology': 'Of uncertain origin, possibly imitative or related to similar exclamatory words expressing malfunction or failure.',
                'language_origins': 'English (uncertain origin)',
                'example_sentence': 'The computer went _______ right in the middle of her important presentation.',
                'memory_tip': 'Remember "FLOO-ey" - when things go wrong and FLU away from working properly, everything becomes screwy.'
            },
            'floor': {
                'definition': 'Floor refers to the bottom surface of a room or building that people walk on, or the bottom level of any space or structure. As a verb, floor can mean to knock someone down, to surprise someone greatly, or to press an accelerator pedal fully. Floor can also refer to the minimum level of something, such as a price floor. The word emphasizes the base, foundation, or lowest level of something.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FLOR',
                'etymology': 'From Old English "flor," related to similar words in Germanic languages meaning "floor" or "level ground."',
                'language_origins': 'Old English',
                'example_sentence': 'The hardwood _______ gleamed after being polished to a beautiful shine.',
                'memory_tip': 'Remember "FLOOR" - the bottom surface you walk on, or something that can FLOOR (amaze) you with surprise.'
            },
            'floral': {
                'definition': 'Floral relates to or consists of flowers, or describes patterns, designs, or scents that feature or resemble flowers. When something is floral, it either contains actual flowers or incorporates flower-like elements in its design, fragrance, or appearance. Floral can describe fabrics with flower patterns, perfumes with flower scents, or arrangements featuring flowers. The word emphasizes beauty, nature, and the decorative or aromatic qualities associated with flowers.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FLOR-ul',
                'etymology': 'From Latin "floralis," from "flos, floris" meaning "flower," relating to flowers or flowering.',
                'language_origins': 'Latin',
                'example_sentence': 'She chose a _______ dress with delicate rose patterns for the spring wedding.',
                'memory_tip': 'Remember "FLOR-al" - relating to FLOWERS, anything that features or resembles the beauty of blooms.'
            },
            'florentine': {
                'definition': 'Florentine refers to someone or something from Florence, Italy, or relates to the style, culture, or characteristics of that historic city. In culinary contexts, Florentine often describes dishes prepared with spinach, reflecting a traditional Florentine cooking style. The term can also refer to a type of biscuit or cookie, or to artistic styles associated with Renaissance Florence. Florentine emphasizes the rich cultural heritage and distinctive characteristics of Florence.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'FLOR-en-teen',
                'etymology': 'From Italian "fiorentino," meaning "of Florence," from "Firenze" (Florence), ultimately from Latin "Florentia."',
                'language_origins': 'Italian, Latin',
                'example_sentence': 'The restaurant served Eggs _______, featuring poached eggs on a bed of creamed spinach.',
                'memory_tip': 'Remember "FLOR-entine" - from FLORence, Italy, the city that FLORished during the Renaissance with amazing art and culture.'
            },
            'floribunda': {
                'definition': 'Floribunda is a type of rose characterized by clusters of flowers that bloom continuously throughout the growing season. These roses are known for producing abundant, repeated flowering with multiple blooms per stem, making them popular for gardens and landscaping. Floribunda roses are typically hardier and more disease-resistant than hybrid tea roses, while offering prolific flowering displays. The term literally means "abundant flowering," reflecting their most distinctive characteristic.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'flor-i-BUN-duh',
                'etymology': 'From Latin "floribundus," meaning "abounding in flowers," from "flos" (flower) and "abundus" (abundant).',
                'language_origins': 'Latin',
                'example_sentence': 'The gardener planted _______ roses along the fence because they would provide continuous color throughout the summer.',
                'memory_tip': 'Remember "FLORI-bunda" - roses with ABUNDANT FLOWERS that bloom generously, providing lots of floral beauty.'
            },
            'floridly': {
                'definition': 'Floridly means in an elaborate, ornate, or excessively decorative manner, often to the point of being overly complex or showy. When something is done floridly, it is characterized by excessive ornamentation, elaborate style, or flowery language that may be considered too ornate for the situation. The adverb can describe writing, speech, decorative styles, or behavior that is marked by excessive embellishment or dramatic flair.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'FLOR-id-lee',
                'etymology': 'From "florid" (from Latin "floridus" meaning "flowery" or "blooming") plus the adverb suffix "-ly."',
                'language_origins': 'Latin',
                'example_sentence': 'The poet wrote _______, using elaborate metaphors and ornate language that sometimes obscured his meaning.',
                'memory_tip': 'Remember "FLOR-idly" - in a flowery, elaborate way like FLORal decorations that are overly ornate and showy.'
            },
            'floruit': {
                'definition': 'Floruit is a Latin term meaning "he/she flourished," used in biographical contexts to indicate the period during which a person was most active, productive, or prominent, especially when exact birth and death dates are unknown. This scholarly term appears in historical and academic writing to denote the time when someone\'s work or influence was at its peak. Floruit provides a way to place historical figures in chronological context when precise life dates are unavailable.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLOR-oo-it',
                'etymology': 'From Latin "floruit," meaning "he/she flourished," third person singular perfect tense of "florere" (to flower, to flourish).',
                'language_origins': 'Latin',
                'example_sentence': 'The medieval scholar\'s _______ was during the 12th century, when he produced his most influential philosophical works.',
                'memory_tip': 'Remember "FLOR-uit" - the time when someone FLOURished and was most productive, like flowers in full bloom.'
            },
            'flotsam': {
                'definition': 'Flotsam refers to wreckage or debris from a ship that floats on the water\'s surface after a shipwreck. More broadly, flotsam can describe any floating refuse, debris, or discarded objects found in water. The term is often paired with "jetsam" (cargo deliberately thrown overboard) in the phrase "flotsam and jetsam," which collectively refers to miscellaneous debris or homeless and displaced people. Flotsam emphasizes objects that float rather than sink.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLOT-sam',
                'etymology': 'From Anglo-French "floteson," from "floter" meaning "to float," referring to floating wreckage.',
                'language_origins': 'Anglo-French',
                'example_sentence': 'After the storm, the beach was littered with _______ from ships that had been caught in the hurricane.',
                'memory_tip': 'Remember "FLOT-sam" - debris that FLOATs on water, the wreckage that doesn\'t sink after ships are damaged.'
            },
            'flounder': {
                'definition': 'Flounder means to struggle awkwardly or to be in serious difficulty, typically while trying to move, progress, or find solutions. When someone flounders, they move clumsily through water, mud, or snow, or they struggle unsuccessfully with problems or challenges. As a noun, flounder refers to a type of flatfish. The verb emphasizes awkward, ineffective movement or action, often suggesting confusion, lack of direction, or desperation.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'FLOWN-der',
                'etymology': 'Possibly from Dutch "flodderen" meaning "to splash" or from similar words suggesting struggling movement.',
                'language_origins': 'Dutch',
                'example_sentence': 'The new employee began to _______ when asked to explain the complex software system to clients.',
                'memory_tip': 'Remember "FLOUNDER" - to struggle and move awkwardly, like a fish out of water that flops around desperately.'
            },
            'flourish': {
                'definition': 'Flourish means to grow vigorously, thrive, or prosper in a healthy and successful way. When something flourishes, it develops excellently and achieves notable success or growth. As a noun, flourish can refer to an elaborate decorative gesture, a bold or showy display, or an ornamental embellishment in writing or music. The word emphasizes success, prosperity, vigorous growth, and often dramatic or impressive displays.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'FLUR-ish',
                'etymology': 'From Old French "florir," from Latin "florere" meaning "to flower" or "to bloom," related to "flos" (flower).',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The small business began to _______ after implementing the new marketing strategy.',
                'memory_tip': 'Remember "FLOUR-ish" - to grow and bloom like flowers, thriving with success and prosperity.'
            },
            'flout': {
                'definition': 'Flout means to openly disregard, disobey, or show contempt for rules, laws, conventions, or authority. When someone flouts something, they deliberately and conspicuously violate or ignore it, often with an attitude of defiance or disdain. Flouting suggests not just breaking rules but doing so in a way that demonstrates deliberate disrespect for the authority or principle behind those rules. The action is typically public and intentional.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'FLOWT',
                'etymology': 'Possibly from Middle Dutch "fluiten" meaning "to play the flute," later developing the sense of mocking or showing contempt.',
                'language_origins': 'Middle Dutch',
                'example_sentence': 'The company decided to _______ environmental regulations, resulting in significant fines and public criticism.',
                'memory_tip': 'Remember "FLOUT" - to openly defy rules, like giving them a dismissive POUT and ignoring authority completely.'
            },
            'flowers': {
                'definition': 'Flowers are the reproductive structures of flowering plants, typically characterized by colorful petals, fragrance, and often complex shapes designed to attract pollinators. These botanical structures serve the essential function of plant reproduction while providing beauty, fragrance, and nectar. Flowers have deep cultural significance across human societies, symbolizing love, celebration, sympathy, and various emotions. They are used for decoration, ceremonies, gifts, and in various cultural and religious practices.',
                'part_of_speech': 'noun (plural), verb',
                'pronunciation_guide': 'FLOW-erz',
                'etymology': 'From Old French "flor," from Latin "flos, floris" meaning "flower" or "blossom."',
                'language_origins': 'Latin, Old French',
                'example_sentence': 'The garden was filled with colorful _______ that attracted bees and butterflies throughout the summer.',
                'memory_tip': 'Remember "FLOWER-s" - beautiful blooms that make gardens GLOW with color, nature\'s way of showing off beauty.'
            },
            'flows': {
                'definition': 'Flows describes the movement of liquids, gases, or other substances in a continuous, smooth stream, or refers to multiple instances of such movement. The word can describe water flowing in rivers, air flowing through ventilation systems, or traffic flowing on highways. As a verb, flows indicates continuous, uninterrupted movement or progression. The concept emphasizes smooth, steady movement without obstruction or interruption.',
                'part_of_speech': 'verb, noun (plural)',
                'pronunciation_guide': 'FLOHZ',
                'etymology': 'From "flow," from Old English "flowan," related to similar words meaning "to stream" or "to move smoothly."',
                'language_origins': 'Old English',
                'example_sentence': 'The mountain stream _______ gently through the valley, providing fresh water for wildlife.',
                'memory_tip': 'Remember "FLOWS" - like water that goes smoothly in continuous streams, moving without stopping or obstruction.'
            },
            'fluctuation': {
                'definition': 'Fluctuation refers to irregular rising and falling movements or variations in level, amount, or intensity. When something experiences fluctuation, it changes repeatedly between different states, values, or conditions, often in an unpredictable or cyclical pattern. Fluctuations can occur in prices, temperatures, emotions, population levels, or any measurable quantity that varies over time. The word emphasizes instability, variability, and lack of steady state.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fluk-choo-AY-shun',
                'etymology': 'From Latin "fluctuatio," from "fluctuare" meaning "to flow" or "to wave," related to "fluctus" (wave).',
                'language_origins': 'Latin',
                'example_sentence': 'The stock market experienced significant _______ during the economic uncertainty.',
                'memory_tip': 'Remember "FLUCTU-ation" - like waves that FLUCTUate up and down, values that keep changing and varying.'
            },
            'fluency': {
                'definition': 'Fluency is the ability to express oneself easily, smoothly, and readily, particularly in speech or writing. When someone demonstrates fluency, they can communicate with natural flow, appropriate pace, and without frequent hesitation or struggle to find words. Fluency can refer to language skills, where a person can speak or write in a language with ease and accuracy, or to other skills performed with smooth competence. The word emphasizes ease, smoothness, and natural ability.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLOO-en-see',
                'etymology': 'From Latin "fluentia," from "fluens" meaning "flowing," related to "fluere" (to flow).',
                'language_origins': 'Latin',
                'example_sentence': 'Her _______ in three languages made her an ideal candidate for the international business position.',
                'memory_tip': 'Remember "FLU-ency" - the ability to let words FLOW naturally, like a fluent stream of communication.'
            },
            'fluid': {
                'definition': 'Fluid can describe a substance that flows and takes the shape of its container, such as liquids and gases, or it can describe something that is smooth, graceful, and adaptable to change. As a noun, fluid refers to any substance that flows, including water, oil, blood, or air. As an adjective, fluid describes movement that is smooth and continuous, or situations that are flexible and subject to change. The word emphasizes flow, adaptability, and lack of rigid form.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'FLOO-id',
                'etymology': 'From Latin "fluidus," from "fluere" meaning "to flow," emphasizing the flowing nature of liquids and gases.',
                'language_origins': 'Latin',
                'example_sentence': 'The dancer\'s movements were so _______ that she seemed to float across the stage.',
                'memory_tip': 'Remember "FLU-id" - something that FLOWs like water, adaptable and able to change shape smoothly.'
            },
            'fluke': {
                'definition': 'Fluke can refer to an unlikely chance occurrence, a stroke of luck, or an accidental success that happens despite low probability. As a noun, fluke can also describe the flat tail of a whale or the barbed end of an anchor. In biology, a fluke is a type of parasitic flatworm. When describing events, fluke emphasizes the unexpected, accidental, or fortunate nature of something that succeeds against the odds.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLOOK',
                'etymology': 'From Old English "floc," meaning "flatfish," later extended to other flat objects and chance occurrences.',
                'language_origins': 'Old English',
                'example_sentence': 'Winning the lottery was just a _______ - she had only bought one ticket on impulse.',
                'memory_tip': 'Remember "FLUKE" - a lucky accident, something that happened by chance like a fluke fish swimming into your net.'
            },
            'flummery': {
                'definition': 'Flummery originally referred to a sweet dessert made from oatmeal or flour, but has evolved to mean meaningless flattery, nonsense, or empty compliments designed to deceive or please. In modern usage, flummery describes talk or behavior that is insincere, pretentious, or designed to impress without substance. The word suggests hollow praise or elaborate but meaningless speech intended to manipulate or flatter someone.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLUM-er-ee',
                'etymology': 'From Welsh "llymru," a type of soft food made from oatmeal, later applied metaphorically to soft or insubstantial talk.',
                'language_origins': 'Welsh',
                'example_sentence': 'The politician\'s speech was full of _______ - lots of fancy words but no real substance or concrete plans.',
                'memory_tip': 'Remember "FLUM-mery" - like FLUMMY (soft) talk that\'s all sweetness but no real substance, empty flattery.'
            },
            'flummix': {
                'definition': 'Flummix appears to be a variant or dialect form of "flummox," meaning to confuse, perplex, or bewilder someone completely. When someone is flummixed, they are left in a state of confusion and unable to understand or proceed. This word suggests a state of mental confusion where someone feels completely stumped or unable to make sense of a situation. The term emphasizes bewilderment and the inability to comprehend or respond appropriately.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'FLUM-iks',
                'etymology': 'Variant of "flummox," of uncertain origin, possibly related to dialect words meaning "to make a mess of" or "to confuse."',
                'language_origins': 'English (dialectal variant)',
                'example_sentence': 'The complex mathematical proof completely _______ even the advanced students in the class.',
                'memory_tip': 'Remember "FLUM-mix" - to MIX someone up so much they feel FLUMMOXED and completely confused.'
            },
            'flummox': {
                'definition': 'Flummox means to confuse, perplex, or bewilder someone so thoroughly that they cannot understand or know how to respond. When someone is flummoxed, they are completely stumped, puzzled, or at a loss for what to do or think. This verb suggests a level of confusion that goes beyond simple misunderstanding to complete bewilderment. The word often implies that the confusion is caused by something complex, unexpected, or deliberately confusing.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'FLUM-uks',
                'etymology': 'Of uncertain origin, possibly from English dialect, first recorded in the 19th century meaning "to confuse" or "to perplex."',
                'language_origins': 'English (uncertain origin)',
                'example_sentence': 'The unexpected question about quantum physics completely _______ the history student.',
                'memory_tip': 'Remember "FLUM-mox" - to completely confuse someone, leaving them STUMPED and unable to think clearly.'
            },
            'flummux': {
                'definition': 'Flummux appears to be another variant spelling of "flummox," meaning to confuse, perplex, or bewilder someone completely. Like flummox, this word describes the action of causing someone to become thoroughly confused, puzzled, or unable to understand a situation. The person who is flummuxed feels completely stumped and unable to proceed or respond appropriately to whatever has confused them.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'FLUM-uks',
                'etymology': 'Another variant spelling of "flummox," sharing the same uncertain etymological origins and meaning.',
                'language_origins': 'English (variant spelling)',
                'example_sentence': 'The magician\'s impossible trick managed to _______ even the most skeptical audience members.',
                'memory_tip': 'Remember "FLUM-mux" - another way to spell flummox, meaning to thoroughly MUX up someone\'s understanding.'
            },
            'fluoride': {
                'definition': 'Fluoride is a chemical compound containing fluorine that is commonly added to drinking water and toothpaste to prevent tooth decay. This mineral helps strengthen tooth enamel and makes teeth more resistant to acid attacks from bacteria in the mouth. Fluoride can occur naturally in water sources or be artificially added as a public health measure. The use of fluoride in dental care and water treatment has been one of the most significant advances in preventing dental disease.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLOR-ide',
                'etymology': 'From "fluorine" (named for its occurrence in the mineral fluorite) plus the suffix "-ide" indicating a compound.',
                'language_origins': 'Latin, English',
                'example_sentence': 'The dentist recommended using _______ toothpaste to help prevent cavities and strengthen tooth enamel.',
                'memory_tip': 'Remember "FLUOR-ide" - a compound that helps your teeth FLOURISH by preventing decay and making them stronger.'
            },
            'flurry': {
                'definition': 'Flurry refers to a brief period of intense activity, excitement, or confusion, or a light fall of snow. When there\'s a flurry of activity, multiple things happen quickly and simultaneously, creating a sense of bustling movement or urgency. In meteorology, a snow flurry is a brief, light snowfall that typically doesn\'t accumulate significantly. The word emphasizes sudden, intense, but usually brief bursts of activity or precipitation.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FLUR-ee',
                'etymology': 'Possibly from "flutter" or related to words meaning "to scatter" or "to move quickly in confusion."',
                'language_origins': 'English',
                'example_sentence': 'There was a _______ of last-minute preparations before the important guests arrived.',
                'memory_tip': 'Remember "FLUR-ry" - a quick burst of activity that makes you move in a hurry, like snowflakes swirling rapidly.'
            },
            'flustered': {
                'definition': 'Flustered describes someone who is confused, agitated, or nervous, typically as a result of being rushed, embarrassed, or overwhelmed. When someone is flustered, they feel rattled and have difficulty thinking clearly or acting calmly. This state often results from unexpected situations, time pressure, or social embarrassment that disrupts normal composure. Flustered people may appear anxious, speak hesitantly, or make mistakes due to their agitated state.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'FLUS-terd',
                'etymology': 'From "fluster," possibly from Icelandic "flaustr" meaning "hurry" or "bustle," or related to "flutter."',
                'language_origins': 'Icelandic, English',
                'example_sentence': 'She became _______ when the interviewer asked an unexpected question she hadn\'t prepared for.',
                'memory_tip': 'Remember "FLUSTER-ed" - feeling rattled and confused, like your thoughts are all CLUSTERED together in chaos.'
            },
            'flute': {
                'definition': 'A flute is a woodwind musical instrument typically made of metal, wood, or plastic, played by blowing air across an opening while covering and uncovering holes along its length to create different pitches. The flute produces sound through the vibration of air across the embouchure hole and is known for its clear, bright, and ethereal tone. As a verb, flute can mean to play this instrument or to create decorative grooves or channels in objects like architectural columns or pie crusts.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FLOOT',
                'etymology': 'From Old French "fleute," possibly from Provençal "flaüt," ultimately of uncertain origin but related to "blow."',
                'language_origins': 'Old French, Provençal',
                'example_sentence': 'The solo _______ melody floated above the orchestra, creating a hauntingly beautiful sound.',
                'memory_tip': 'Remember "FLUTE" - a musical instrument you blow through to create FLUTING (flowing) melodies that sound light and airy.'
            },
            'flybys': {
                'definition': 'Flybys are close approaches or passes by aircraft, spacecraft, or other flying objects past a specific target or location without landing or stopping. In space exploration, flybys refer to spacecraft missions that pass close to planets, moons, or other celestial bodies to collect data without entering orbit or landing. The term can also describe military aircraft passes, aerial demonstrations, or any situation where something flies past at close range for observation or display purposes.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FLY-byz',
                'etymology': 'Compound word combining "fly" and "by," literally meaning flights that pass by a target.',
                'language_origins': 'English',
                'example_sentence': 'The space probe conducted several _______ of Jupiter\'s moons, collecting valuable scientific data.',
                'memory_tip': 'Remember "FLY-bys" - flights that FLY BY targets to observe them closely without stopping or landing.'
            },
            'flèche': {
                'definition': 'Flèche is a French architectural term referring to a slender spire, typically found on the roof of Gothic cathedrals, often positioned at the intersection of the nave and transept. These pointed, needle-like structures serve both decorative and symbolic purposes, reaching skyward as expressions of spiritual aspiration. In fencing, flèche refers to a specific attacking movement where the fencer lunges forward with a running step. The word emphasizes pointed, arrow-like structures or movements.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FLESH',
                'etymology': 'From French "flèche" meaning "arrow," referring to the arrow-like pointed shape of architectural spires.',
                'language_origins': 'French',
                'example_sentence': 'The cathedral\'s elegant _______ rose high above the roofline, pointing toward heaven.',
                'memory_tip': 'Remember "FLÈCHE" - a spire shaped like an arrow (flèche means arrow in French) pointing upward to the sky.'
            },
            'foam': {
                'definition': 'Foam is a mass of small bubbles formed in or on a liquid, typically created by agitation, fermentation, or the addition of soap or detergent. Foam can also refer to a light, spongy material made by introducing gas bubbles into a liquid that then solidifies, creating materials like foam rubber or foam insulation. The word emphasizes the light, airy, bubbly texture created by trapped air or gas within a liquid or solid medium.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FOHM',
                'etymology': 'From Old English "fām," related to similar words in Germanic languages meaning "foam" or "froth."',
                'language_origins': 'Old English',
                'example_sentence': 'The ocean waves created white _______ as they crashed against the rocky shore.',
                'memory_tip': 'Remember "FOAM" - bubbly, frothy substance that forms when air gets mixed into liquids, light as a feather in your HOME.'
            },
            'focaccia': {
                'definition': 'Focaccia is a traditional Italian flatbread similar to pizza dough, typically topped with olive oil, herbs, vegetables, or other seasonings before baking. This versatile bread is characterized by its dimpled surface created by pressing fingertips into the dough, which allows toppings to settle into the indentations. Focaccia can be served as an appetizer, side dish, or base for sandwiches, and varies regionally throughout Italy in thickness, toppings, and preparation methods.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'foh-KAH-chee-ah',
                'etymology': 'From Italian "focaccia," from Latin "focacius" meaning "baked in the fireplace," from "focus" (hearth, fireplace).',
                'language_origins': 'Italian, Latin',
                'example_sentence': 'The bakery\'s _______ was topped with rosemary, sea salt, and sun-dried tomatoes.',
                'memory_tip': 'Remember "fo-CACCIA" - Italian flatbread baked in the FIRE (foco), with dimpled surface to catch delicious toppings.'
            },
            'focus': {
                'definition': 'Focus means to concentrate attention, effort, or energy on a particular subject, activity, or goal, or to adjust something to achieve clarity or sharpness. As a noun, focus refers to the center of interest, activity, or attention, or the point at which light rays converge to form a clear image. The word emphasizes concentration, clarity, and the directing of attention or energy toward specific objectives or details.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'FOH-kus',
                'etymology': 'From Latin "focus" meaning "hearth" or "fireplace," the central point of a home, later applied to optics and concentration.',
                'language_origins': 'Latin',
                'example_sentence': 'She decided to _______ on her studies and avoid distractions during exam week.',
                'memory_tip': 'Remember "FOCUS" - to concentrate like light rays that meet at a single point, bringing clarity and sharpness to your attention.'
            }
        }
        
        if word.lower() in batch_069_data:
            return batch_069_data[word.lower()]
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
        
        print("Batch 069 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch069Processor()
    
    input_file = "output/batch_069_words.csv"
    output_file = "output/batch_069_processed.csv"
    
    processor.process_batch(input_file, output_file)