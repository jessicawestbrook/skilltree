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

class Batch072Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for a word using Claude knowledge"""
        
        batch_072_data = {
            'fraught': {
                'definition': 'Fraught means filled with, laden with, or characterized by something undesirable, typically stress, tension, difficulty, or danger. It describes situations, relationships, or conditions that are heavy with problems, anxiety, or potential complications. The word suggests not just the presence of difficulties but an overwhelming abundance of them, creating a sense of being weighed down or burdened by challenging circumstances.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FRAWT',
                'etymology': 'From Middle Dutch "vracht" meaning "freight, cargo," originally referring to a ship loaded with cargo, later extended to mean "loaded with" or "full of."',
                'language_origins': 'Middle Dutch',
                'example_sentence': 'The peace negotiations were _______ with tension as both sides struggled to reach agreement.',
                'memory_tip': 'Remember "FRAUGHT" - a situation so FRAUGHT with problems it feels like carrying heavy FREIGHT or cargo.'
            },
            'frazil': {
                'definition': 'Frazil refers to fine ice crystals that form in supercooled, turbulent water, typically in rivers and streams during extremely cold weather. These delicate ice formations appear as floating needles or platelets and can accumulate to form ice jams. Frazil ice is important in hydrology and can affect water flow, navigation, and the formation of anchor ice on riverbeds.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FRAY-zil',
                'etymology': 'From French Canadian "frasil" meaning "cinders, embers," referring to the appearance of the ice crystals floating like ash or cinders in water.',
                'language_origins': 'French Canadian',
                'example_sentence': 'The river was filled with _______ ice crystals that sparkled in the winter sunlight.',
                'memory_tip': 'Remember "FRAZIL" - FRAZZLED ice crystals that look like floating embers or ash in cold water.'
            },
            'freckle': {
                'definition': 'A freckle is a small, brownish spot on the skin caused by an increase in melanin production, typically triggered by sun exposure. Freckles are most common on fair-skinned individuals and appear primarily on sun-exposed areas like the face, shoulders, and arms. As a verb, freckle means to mark or become marked with these small spots. Freckles are generally harmless and often considered a distinctive feature of natural beauty.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FRECK-ul',
                'etymology': 'From Middle English "frekel," related to Old Norse "freknur" (freckles), possibly from a root meaning "to sprinkle."',
                'language_origins': 'Middle English, Old Norse',
                'example_sentence': 'Her face was dotted with golden _______ that appeared every summer in the sun.',
                'memory_tip': 'Remember "FRECKLE" - small spots that look like they were FREquently speCKLEd across the skin.'
            },
            'free': {
                'definition': 'Free means not under the control or domination of another, having liberty or independence to act, speak, or think without external constraint. It can also mean provided without charge, not bound by rules or obligations, or released from captivity or restriction. The concept encompasses both political liberty and personal autonomy, as well as the absence of cost or obligation.',
                'part_of_speech': 'adjective, adverb, verb',
                'pronunciation_guide': 'FREE',
                'etymology': 'From Old English "freo" meaning "free, not in bondage," related to Sanskrit "priya" (dear, beloved), suggesting the original meaning was "beloved" or "dear one."',
                'language_origins': 'Old English, Proto-Indo-European',
                'example_sentence': 'The birds flew _______ across the open sky, unrestrained by any barriers.',
                'memory_tip': 'Remember "FREE" - able to FLY and ROAM without any restrictions or chains holding you back.'
            },
            'freedom': {
                'definition': 'Freedom is the state of being free from oppression, coercion, or restraint, encompassing both political liberty and personal autonomy. It represents the power to act, speak, or think without external control or interference. Freedom includes various dimensions: political freedom (democratic rights), personal freedom (individual choices), economic freedom (property rights), and philosophical freedom (free will). The concept is fundamental to human dignity and democratic societies.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FREE-dum',
                'etymology': 'From Old English "freodom," composed of "freo" (free) plus "-dom" (state, condition), literally meaning "the state of being free."',
                'language_origins': 'Old English',
                'example_sentence': 'The constitution guarantees citizens the _______ to practice their religion without government interference.',
                'memory_tip': 'Remember "FREEDOM" - the DOM(ain) where you are FREE to make your own choices without oppression.'
            },
            'freegan': {
                'definition': 'A freegan is a person who adopts a lifestyle that attempts to minimize consumption and waste, particularly by recovering and eating discarded food that is still safe to consume. Freegans practice this as a form of protest against perceived waste and excess in consumer society. The movement combines environmental activism with anticonsumerist philosophy, seeking to reduce participation in the conventional economy while addressing food waste.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'FREE-gun',
                'etymology': 'A portmanteau word combining "free" (as in free food) and "vegan," coined in the 1990s by activists who extended vegan principles to include anticonsumerism.',
                'language_origins': 'Modern English (portmanteau)',
                'example_sentence': 'The _______ activist rescued perfectly good vegetables from the grocery store dumpster.',
                'memory_tip': 'Remember "FREEGAN" - FREE food + veGAN ethics, getting free food to reduce waste and consumption.'
            },
            'freesia': {
                'definition': 'Freesia is a genus of fragrant flowering plants native to South Africa, widely cultivated for their delicate, tubular flowers and sweet scent. These bulbous perennials produce colorful blooms in white, yellow, pink, red, and purple, making them popular in gardens and as cut flowers. Freesias are prized for their intense fragrance and are commonly used in perfumes, bouquets, and ornamental plantings.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FREE-zhuh',
                'etymology': 'Named after Friedrich Heinrich Theodor Freese (1795-1876), a German botanist and physician, with the suffix "-ia" indicating a genus name.',
                'language_origins': 'Modern Latin (named after German botanist)',
                'example_sentence': 'The garden was filled with the sweet scent of blooming _______ flowers.',
                'memory_tip': 'Remember "FREESIA" - named after botanist FREESe, these flowers smell so good they seem FREE of any unpleasant odor.'
            },
            'freezescorch': {
                'definition': 'Freezescorch appears to be a combined word error where "freeze" and "scorch" were incorrectly merged during PDF processing. These are opposite concepts: freeze means to become solid due to cold temperatures, while scorch means to burn or char due to excessive heat. This represents a data quality issue where two distinct weather-related terms with opposite meanings were improperly joined together.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'FREEZE-skorch',
                'etymology': 'Corrupted combination of "freeze" (from Old English "freosan") and "scorch" (from Old Norse "skorpna").',
                'language_origins': 'Old English, Old Norse (corrupted)',
                'example_sentence': 'The word _______ represents a parsing error combining two opposite temperature effects.',
                'memory_tip': 'This is a data error - remember that "freeze" and "scorch" are opposites that should not be combined.'
            },
            'freight': {
                'definition': 'Freight refers to goods or cargo transported by ship, aircraft, truck, or train, especially as a commercial enterprise. It encompasses both the merchandise being shipped and the transportation service itself. Freight can also mean the cost of transporting goods or the act of loading cargo. The term emphasizes commercial transportation of bulk goods rather than passenger travel, representing a crucial component of global commerce and supply chains.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FRAYT',
                'etymology': 'From Middle Dutch "vrecht" meaning "freight, cargo," related to "vrachten" (to load a ship), ultimately from a root meaning "to carry."',
                'language_origins': 'Middle Dutch',
                'example_sentence': 'The _______ train carried containers of goods across the country to distribution centers.',
                'memory_tip': 'Remember "FREIGHT" - heavy cargo that creates WEIGHT during transport, like freight trains carrying loads.'
            },
            'french': {
                'definition': 'French refers to anything relating to France, its people, language, or culture. As an adjective, it describes characteristics, customs, products, or styles originating from France. French also denotes the Romance language spoken primarily in France and other francophone countries, known for its sophisticated literature, diplomacy, cuisine, and cultural influence. The term encompasses both the national identity and the broad cultural contributions of French civilization.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'FRENCH',
                'etymology': 'From Old English "frencisc," derived from "Franca" (the Franks), the Germanic tribe that conquered Gaul and gave France its name.',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'She studied _______ cuisine and learned to prepare classic dishes like coq au vin.',
                'memory_tip': 'Remember "FRENCH" - the language and culture of the FRANKS who conquered France long ago.'
            },
            'freneticism': {
                'definition': 'Freneticism refers to a state of frenzied, excited, or frantic activity characterized by wild enthusiasm, desperate urgency, or manic energy. It describes behavior or situations marked by intense, often chaotic activity that lacks calm control or measured pace. Freneticism suggests not just high energy but specifically agitated, desperate, or wildly enthusiastic activity that may be counterproductive or overwhelming.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'freh-NET-ih-sizm',
                'etymology': 'From "frenetic" (from Latin "phreneticus," meaning "delirious") plus the suffix "-ism" indicating a state or condition.',
                'language_origins': 'Latin, Greek',
                'example_sentence': 'The _______ of the stock trading floor created an atmosphere of barely controlled chaos.',
                'memory_tip': 'Remember "FRENETICISM" - a condition of FRENETIC activity, like being caught in a frenzy of wild activity.'
            },
            'frequently': {
                'definition': 'Frequently means occurring often, happening at short intervals, or taking place many times within a given period. It describes the regular or repeated occurrence of events, actions, or situations. The word indicates a high rate of occurrence or repetition, suggesting that something happens more often than occasionally but may not be constant or continuous.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'FREE-kwent-lee',
                'etymology': 'From Latin "frequens" meaning "crowded, repeated, frequent" plus the adverbial suffix "-ly."',
                'language_origins': 'Latin',
                'example_sentence': 'She _______ visited the library to research her dissertation topic.',
                'memory_tip': 'Remember "FREQUENTLY" - happening with great FREQuency, like frequent visits or frequent occurrences.'
            },
            'fresh': {
                'definition': 'Fresh describes something that is new, recently made, obtained, or experienced, often implying vitality, purity, or lack of staleness. It can refer to food that is newly harvested or prepared, air that is clean and invigorating, or ideas that are original and innovative. Fresh suggests absence of deterioration, contamination, or wear, emphasizing newness, cleanliness, or renewed energy.',
                'part_of_speech': 'adjective, adverb',
                'pronunciation_guide': 'FRESH',
                'etymology': 'From Old English "fersc" meaning "fresh, pure, sweet" (of water), related to Old High German "frisc" (fresh).',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The _______ mountain air invigorated the hikers after the long climb.',
                'memory_tip': 'Remember "FRESH" - so new and clean it feels like a FRESH breeze or fresh morning dew.'
            },
            'freudian': {
                'definition': 'Freudian refers to theories, concepts, or interpretations related to Sigmund Freud, the Austrian neurologist who founded psychoanalysis. It describes psychological approaches emphasizing the unconscious mind, repressed memories, sexual drives, and early childhood experiences in shaping adult behavior. A "Freudian slip" is an unintentional error revealing unconscious thoughts. Freudian analysis focuses on hidden meanings, defense mechanisms, and the influence of unconscious desires on conscious behavior.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FROY-dee-an',
                'etymology': 'From Sigmund Freud (1856-1939), Austrian psychoanalyst, plus the suffix "-ian" meaning "relating to" or "characteristic of."',
                'language_origins': 'Modern English (named after Sigmund Freud)',
                'example_sentence': 'The therapist offered a _______ interpretation of the patient\'s recurring dreams.',
                'memory_tip': 'Remember "FREUDIAN" - relating to FREUD\'s theories about the unconscious mind and psychological analysis.'
            },
            'fribble': {
                'definition': 'Fribble means to act in a frivolous, trifling, or foolishly playful manner, or to waste time on unimportant matters. As a noun, it refers to a frivolous person or something trivial and unimportant. The word suggests behavior that is silly, superficial, or lacking in seriousness or purpose. Fribble implies a lighthearted but potentially wasteful approach to activities or responsibilities.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'FRIB-ul',
                'etymology': 'Possibly from "fribble-frabble," a reduplicative formation suggesting nonsensical or trivial talk, related to "fribble" meaning "to trifle."',
                'language_origins': 'English (possibly imitative)',
                'example_sentence': 'Instead of focusing on important work, he chose to _______ away the afternoon on meaningless tasks.',
                'memory_tip': 'Remember "FRIBBLE" - to FIDDLE around with trivial things, like fribbling with frivolous activities.'
            },
            'fribourg': {
                'definition': 'Fribourg is the name of several European cities and regions, most notably Fribourg, Switzerland, and Fribourg-en-Brisgau, Germany. The Swiss Fribourg is a bilingual canton and city known for its medieval architecture, university, and cultural heritage. These place names typically derive from Germanic roots meaning "free town" or "fortified town." The term may appear in spelling competitions as an example of European geographical knowledge.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'FREE-bourg or fri-BOOR',
                'etymology': 'From Germanic "frei" (free) plus "burg" (fortress, town), literally meaning "free town" or "free fortress."',
                'language_origins': 'Germanic',
                'example_sentence': 'The medieval architecture of _______, Switzerland, attracts tourists from around the world.',
                'memory_tip': 'Remember "FRIBOURG" - a FREE BURG (fortress town) in Switzerland, combining "free" and "burg."'
            },
            'friend': {
                'definition': 'A friend is a person with whom one has a bond of mutual affection, trust, and support, typically outside family relationships. Friends share common interests, provide emotional support, and enjoy each other\'s company. The concept encompasses various levels of closeness, from casual acquaintances to intimate confidants. Friendship involves loyalty, understanding, and genuine care for another person\'s well-being and happiness.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FREND',
                'etymology': 'From Old English "freond" meaning "friend, lover," from the present participle of "freogan" (to love, favor), related to "freo" (free).',
                'language_origins': 'Old English',
                'example_sentence': 'She considered him her closest _______ and confidant throughout their college years.',
                'memory_tip': 'Remember "FRIEND" - someone who is FREe to END loneliness and shares genuine affection with you.'
            },
            'frigate': {
                'definition': 'A frigate is a type of warship, historically a fast, medium-sized sailing ship with good maneuverability, used for patrolling, escorting, and reconnaissance. In modern naval terminology, frigates are escort vessels designed for anti-submarine warfare and fleet protection. The term also applies to frigate birds, large seabirds known for their impressive wingspan and soaring ability. The word emphasizes speed, agility, and specialized naval or aerial capabilities.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FRIG-it',
                'etymology': 'From French "frégate," possibly from Italian "fregata," of uncertain origin but possibly related to Latin "fabricatus" (manufactured, built).',
                'language_origins': 'French, possibly Italian',
                'example_sentence': 'The naval _______ patrolled the coastline, protecting merchant vessels from potential threats.',
                'memory_tip': 'Remember "FRIGATE" - a FAST warship that can FRIG-around (move quickly) in naval battles.'
            },
            'frijoles': {
                'definition': 'Frijoles is the Spanish word for beans, commonly used in English when referring to beans in Mexican, Latin American, or Southwestern American cuisine. The term typically refers to various preparations of beans, including refried beans, black beans, or pinto beans served as a staple food. Frijoles are fundamental to Latin American diets and appear in numerous traditional dishes as a protein and fiber source.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'free-HO-lays',
                'etymology': 'From Spanish "frijoles" (beans), ultimately from Latin "phaseolus" meaning "kidney bean," from Greek "phasiolos."',
                'language_origins': 'Spanish, Latin, Greek',
                'example_sentence': 'The traditional Mexican dinner included rice, _______, and freshly made tortillas.',
                'memory_tip': 'Remember "FRIJOLES" - Spanish for beans, sounds like "FREE-ho-lays" when you get free beans at restaurants.'
            },
            'frisbee': {
                'definition': 'A Frisbee is a disc-shaped flying toy made of plastic, designed to glide through the air when thrown with a spinning motion. Originally trademarked by Wham-O, the term has become genericized to describe any flying disc. Frisbees are used for recreational games, competitive disc sports, and casual outdoor activities. The aerodynamic design allows for stable flight and predictable catching, making it popular for parks, beaches, and organized sports.',
                'part_of_speech': 'noun (trademark)',
                'pronunciation_guide': 'FRIZ-bee',
                'etymology': 'From the Frisbie Pie Company, whose pie tins were thrown as toys by college students; later adapted and trademarked as "Frisbee" by Wham-O in 1958.',
                'language_origins': 'American English (company name)',
                'example_sentence': 'They spent the afternoon throwing a _______ back and forth in the park.',
                'memory_tip': 'Remember "FRISBEE" - originally FRISBIE pie tins that college students threw around for fun, now a flying disc toy.'
            },
            'frisket': {
                'definition': 'A frisket is a masking device used in printing and graphic arts to protect areas of paper or other surfaces from receiving ink, paint, or other materials during the printing process. In letterpress printing, frisket refers to the hinged cover that holds the paper in place. In modern graphics and painting, frisket film serves as a temporary mask that can be cut and removed to create sharp, clean edges in artwork.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FRISK-it',
                'etymology': 'From French "frisquette," possibly related to "frisquer" (to frisk, move quickly), referring to the quick, precise masking action.',
                'language_origins': 'French',
                'example_sentence': 'The artist applied _______ film to protect areas of the watercolor painting while adding background washes.',
                'memory_tip': 'Remember "FRISKET" - it FRISKS around to protect parts of artwork, like a protective mask that moves quickly on and off.'
            },
            'frison': {
                'definition': 'Frison appears to be a variant or error related to "frisson," which means a sudden, brief moment of excitement, pleasure, or fear; a thrill or shudder of emotion. If "frison" is intended as a separate word, it may refer to a curl or wave in hair (from French "friser" meaning to curl), but this usage would be quite specialized. The word is most likely meant to be "frisson," the emotional thrill.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'free-SOHN',
                'etymology': 'Possibly a variant of "frisson" (from French "frisson" meaning "shiver, thrill") or related to "friser" (to curl).',
                'language_origins': 'French',
                'example_sentence': 'She felt a _______ of excitement when she heard her favorite song begin.',
                'memory_tip': 'Remember "FRISON" - likely meant to be "frisson," a FREEZING thrill of excitement that gives you shivers.'
            },
            'frisson': {
                'definition': 'A frisson is a sudden brief moment of excitement, pleasure, fear, or emotional thrill that often manifests as a physical sensation like a shiver or tingling feeling. It describes the emotional and physical response to something particularly moving, thrilling, or beautiful, such as music, art, or an exciting moment. The word captures both the emotional impact and the accompanying physical sensation of being deeply moved or excited.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'free-SOHN',
                'etymology': 'From French "frisson" meaning "a shiver, shudder," from "frissonner" (to shiver), ultimately from Latin "frigere" (to be cold).',
                'language_origins': 'French, Latin',
                'example_sentence': 'The powerful symphony gave her a _______ of pure emotional excitement.',
                'memory_tip': 'Remember "FRISSON" - a FREEZING thrill, like when something exciting gives you shivers of delight.'
            },
            'fritillary': {
                'definition': 'Fritillary refers to either a genus of flowering plants with distinctive checkered or spotted petals, or a group of butterflies with similar spotted wing patterns. The plants, also called crown imperial or snake\'s head fritillary, produce drooping bell-shaped flowers often marked with checkerboard patterns. Fritillary butterflies are medium to large orange butterflies with black spots and markings. Both share the characteristic of distinctive spotted or checkered patterns.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FRIT-uh-lair-ee',
                'etymology': 'From Latin "fritillus" meaning "dice box," referring to the checkered pattern on the petals resembling markings on dice.',
                'language_origins': 'Latin',
                'example_sentence': 'The garden featured purple _______ flowers with their distinctive checkered petals.',
                'memory_tip': 'Remember "FRITILLARY" - flowers and butterflies with patterns like dice in a FRITILLUS (dice box).'
            },
            'frittata': {
                'definition': 'A frittata is an Italian egg dish similar to an omelet but thicker and cooked slowly, typically starting on the stovetop and finishing in the oven. Unlike omelets, frittatas are not folded and often contain vegetables, cheese, or meat mixed throughout rather than used as filling. The dish is served in wedges like a pie and can be eaten hot or at room temperature, making it popular for brunches, picnics, and light meals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'frih-TAH-tah',
                'etymology': 'From Italian "frittata," past participle of "friggere" meaning "to fry," from Latin "frigere" (to fry, roast).',
                'language_origins': 'Italian, Latin',
                'example_sentence': 'She prepared a delicious vegetable _______ with spinach, tomatoes, and goat cheese.',
                'memory_tip': 'Remember "FRITTATA" - an Italian egg dish that\'s FRIED and FLAT like a thick omelet pie.'
            },
            'frivolous': {
                'definition': 'Frivolous describes something that lacks seriousness, importance, or substance, characterized by being trivial, silly, or unnecessarily playful when gravity is called for. It refers to behavior, attitudes, or things that are lightweight, superficial, or concerned with unimportant matters. Frivolous can apply to legal cases without merit, spending on unnecessary luxuries, or behavior that seems inappropriate given the circumstances.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FRIV-uh-lus',
                'etymology': 'From Latin "frivolus" meaning "silly, trifling," possibly related to "friare" (to rub, crumble), suggesting something that crumbles under examination.',
                'language_origins': 'Latin',
                'example_sentence': 'The judge dismissed the _______ lawsuit as having no merit or legal foundation.',
                'memory_tip': 'Remember "FRIVOLOUS" - so FRISKY and playful it lacks seriousness, like frivolous fun when you should be working.'
            },
            'frock': {
                'definition': 'A frock is a dress, particularly a woman\'s or girl\'s garment, or historically a loose outer garment worn by men such as a monk\'s habit or a smock. In modern usage, frock typically refers to a dress, especially one that is simple, casual, or traditional in style. The word can also describe clerical garments or work clothing designed to protect other clothes. Historical usage included various types of loose, comfortable outer wear.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FROK',
                'etymology': 'From Old French "froc" meaning "monk\'s habit," possibly from Frankish or another Germanic source meaning "garment."',
                'language_origins': 'Old French, possibly Germanic',
                'example_sentence': 'The little girl wore a beautiful blue _______ to the summer wedding.',
                'memory_tip': 'Remember "FROCK" - a type of garment, sounds like FROCK rhymes with "smock," another type of loose clothing.'
            },
            'frockcamcorder': {
                'definition': 'Frockcamcorder appears to be a combined word error where "frock" (a dress or garment) and "camcorder" (a portable video recording device) were incorrectly merged during PDF processing. These are completely unrelated items - one is clothing and the other is electronic equipment for recording video. This represents a data quality issue where two distinct, unrelated terms were improperly joined together.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'FROK-kam-kor-der',
                'etymology': 'Corrupted combination of "frock" (from Old French "froc") and "camcorder" (from "camera" + "recorder").',
                'language_origins': 'Old French, Modern English (corrupted)',
                'example_sentence': 'The term _______ represents a parsing error combining clothing and video equipment terminology.',
                'memory_tip': 'This is a data error - remember that "frock" (dress) and "camcorder" (video device) should be separate words.'
            },
            'frog': {
                'definition': 'A frog is an amphibian characterized by smooth, moist skin, powerful hind legs adapted for jumping, and the ability to live both in water and on land. Frogs undergo metamorphosis from tadpoles to adults, typically have bulging eyes, and most species can swim, jump, and catch insects with their sticky tongues. They play important ecological roles as both predators and prey, and many species are indicators of environmental health.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FROG',
                'etymology': 'From Old English "frogga," related to Old Norse "fraukr" and other Germanic words, possibly imitative of the croaking sound frogs make.',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The _______ sat motionless on the lily pad until a fly came within striking distance.',
                'memory_tip': 'Remember "FROG" - an amphibian that can FROG-leap with powerful legs and goes "ribbit" by the pond.'
            },
            'fronds': {
                'definition': 'Fronds are large, typically divided leaves, especially those of palm trees, ferns, or cycads. These leaves are usually compound or deeply lobed, creating a feathery or fan-like appearance. Fronds are characteristic of tropical and subtropical plants and often serve as both photosynthetic organs and distinctive visual features. In palms, fronds may be pinnate (feather-like) or palmate (fan-like), while fern fronds are usually intricately divided.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FRONDZ',
                'etymology': 'From Latin "frons" meaning "leafy branch, foliage," related to "frondescere" (to come into leaf).',
                'language_origins': 'Latin',
                'example_sentence': 'The palm tree\'s large _______ swayed gracefully in the tropical breeze.',
                'memory_tip': 'Remember "FRONDS" - the FRONDY leaves of ferns and palms that look like feathers or fans.'
            },
            'front': {
                'definition': 'Front refers to the forward-facing part, side, or surface of something, or the position ahead of others in sequence or location. It can describe the foremost area of a building, the leading edge of a weather system, or the forward position in a line or formation. As a verb, front means to face toward something or to serve as the front of something. The word emphasizes position, direction, or the most visible or prominent aspect.',
                'part_of_speech': 'noun, verb, adjective',
                'pronunciation_guide': 'FRUNT',
                'etymology': 'From Latin "frons" meaning "forehead, front, face," referring to the forward-facing part.',
                'language_origins': 'Latin',
                'example_sentence': 'The hotel room had a beautiful view of the ocean from the _______ windows.',
                'memory_tip': 'Remember "FRONT" - the FORward poinT, like your forehead is the front of your face.'
            },
            'frontier': {
                'definition': 'A frontier is a boundary or border between settled and unsettled regions, particularly the edge of developed territory that borders wilderness or unexplored areas. Historically, it refers to the advancing edge of settlement in countries like the American West. Metaphorically, frontier describes the edge of knowledge or the limits of current understanding in science, technology, or other fields, representing areas ripe for exploration and discovery.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'frun-TEER',
                'etymology': 'From Old French "frontiere" meaning "boundary, border," from "front" (forehead, front) plus the suffix "-iere."',
                'language_origins': 'Old French',
                'example_sentence': 'The space program represents humanity\'s exploration of the final _______.',
                'memory_tip': 'Remember "FRONTIER" - the FRONT TIER of exploration, the front line between known and unknown territory.'
            },
            'frosty': {
                'definition': 'Frosty describes something covered with frost, characterized by freezing temperatures, or having a cold, unfriendly demeanor. It refers to conditions where ice crystals form on surfaces due to cold temperatures, creating a white, crystalline coating. Figuratively, frosty describes relationships or interactions that are cold, distant, or lacking warmth and friendliness. The word emphasizes both literal coldness and metaphorical emotional distance.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FROS-tee',
                'etymology': 'From "frost" (from Old English "frost," meaning "freezing weather") plus the suffix "-y," meaning "characterized by frost."',
                'language_origins': 'Old English',
                'example_sentence': 'The _______ morning air made their breath visible as they walked to school.',
                'memory_tip': 'Remember "FROSTY" - covered with FROST, so cold it creates ice crystals like Frosty the Snowman.'
            },
            'froufrou': {
                'definition': 'Froufrou describes elaborate, fussy, or overly ornate decoration, especially in clothing or interior design, characterized by excessive frills, ruffles, or showy ornamentation. The word suggests decoration that is more style than substance, emphasizing appearance over function or practicality. It can also refer to pretentious or affected behavior. Froufrou implies a certain frivolity or superficiality in design or manner.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'FROO-froo',
                'etymology': 'From French "froufrou," an imitative word representing the rustling sound of silk fabric, especially elaborate dresses.',
                'language_origins': 'French (onomatopoeia)',
                'example_sentence': 'The Victorian parlor was decorated with excessive _______ that made it feel cluttered and overwhelming.',
                'memory_tip': 'Remember "FROUFROU" - the sound fancy fabric makes when it rustles, like "froo-froo" with lots of frilly decorations.'
            },
            'froufroudifficulty': {
                'definition': 'Froufroudifficulty appears to be a combined word error where "froufrou" (elaborate, fussy decoration) and "difficulty" were incorrectly merged during PDF processing. This represents a data quality issue where a descriptive term for ornate decoration was improperly joined with a word indicating complexity or challenge. These concepts could be related in the context of describing overly complex or fussy design challenges.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'FROO-froo-DIF-ih-kul-tee',
                'etymology': 'Corrupted combination of "froufrou" (French onomatopoeia) and "difficulty" (from Latin "difficultas").',
                'language_origins': 'French, Latin (corrupted)',
                'example_sentence': 'The word _______ appears to be a parsing error combining ornate decoration with complexity concepts.',
                'memory_tip': 'This is a data error - remember that "froufrou" and "difficulty" should be separate words, not combined.'
            },
            'froward': {
                'definition': 'Froward describes someone who is willfully contrary, difficult to deal with, or stubbornly disobedient. It characterizes a person who habitually opposes others or acts against what is reasonable or expected. Froward behavior involves perverse resistance to authority, guidance, or cooperation, often seeming to choose the opposite path out of defiance or obstinacy. The word suggests deliberate contrariness rather than innocent disagreement.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FROH-werd',
                'etymology': 'From Middle English "froward," literally meaning "turning away from," composed of "fro" (away from) plus "-ward" (direction).',
                'language_origins': 'Middle English',
                'example_sentence': 'The _______ child consistently refused to follow even simple instructions.',
                'memory_tip': 'Remember "FROWARD" - turning AWAY FROM being cooperative, going in the opposite direction like "fro-ward."'
            },
            'frozen': {
                'definition': 'Frozen describes something that has been turned into ice or become solid due to cold temperatures, or something that has been preserved by freezing. It can refer to water that has solidified, food that has been preserved through freezing, or metaphorically to emotions, expressions, or situations that have become rigid, immobilized, or unable to change. Frozen suggests a state of being fixed, immobile, or temporarily suspended.',
                'part_of_speech': 'adjective, verb (past participle)',
                'pronunciation_guide': 'FROH-zen',
                'etymology': 'Past participle of "freeze," from Old English "freosan" meaning "to freeze, turn to ice."',
                'language_origins': 'Old English',
                'example_sentence': 'The pond was completely _______ over, creating a perfect surface for ice skating.',
                'memory_tip': 'Remember "FROZEN" - turned to ice by FROsty weather, like frozen water becoming solid ice.'
            },
            'fructiferous': {
                'definition': 'Fructiferous means bearing or producing fruit, particularly used in botanical contexts to describe plants, trees, or branches that yield edible or reproductive fruits. The word emphasizes the productive or fertile nature of fruit-bearing plants. It can also be used metaphorically to describe anything that produces beneficial results, outcomes, or "fruits" of labor. The term highlights the generative and productive capacity of organisms or systems.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'fruk-TIF-er-us',
                'etymology': 'From Latin "fructifer" meaning "fruit-bearing," composed of "fructus" (fruit) plus "ferre" (to bear, carry).',
                'language_origins': 'Latin',
                'example_sentence': 'The orchard\'s _______ trees provided abundant apples for the local community.',
                'memory_tip': 'Remember "FRUCTIFEROUS" - FRUIT-FER-ous, like bearing or FERrying FRUIT, productive of fruit.'
            },
            'fructose': {
                'definition': 'Fructose is a simple sugar (monosaccharide) found naturally in fruits, vegetables, and honey, also known as fruit sugar. It is one of the most common naturally occurring sugars and is sweeter than glucose or sucrose. Fructose is metabolized differently from other sugars, being processed primarily by the liver. It is used commercially in food production and is a component of high-fructose corn syrup, though excessive consumption has been linked to health concerns.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FRUK-tohs',
                'etymology': 'From Latin "fructus" (fruit) plus the chemical suffix "-ose" indicating a sugar, literally meaning "fruit sugar."',
                'language_origins': 'Latin, Modern scientific terminology',
                'example_sentence': 'The apple\'s natural sweetness comes primarily from _______ and other fruit sugars.',
                'memory_tip': 'Remember "FRUCTOSE" - the sugar found in FRUITS, FRUCT-ose is fruit sugar that makes fruits sweet.'
            },
            'frugal': {
                'definition': 'Frugal describes a lifestyle, attitude, or behavior characterized by careful spending, avoiding waste, and making economical use of resources. It suggests wisdom in financial matters, preferring value over luxury, and finding satisfaction in simplicity rather than excess. Frugal living involves mindful consumption, resourcefulness, and the ability to distinguish between wants and needs. The word implies virtue in moderation and careful stewardship of resources.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FROO-gul',
                'etymology': 'From Latin "frugalis" meaning "economical, thrifty," from "frux" (fruit, produce, value), referring to getting value from resources.',
                'language_origins': 'Latin',
                'example_sentence': 'Her _______ lifestyle allowed her to save money while still enjoying life\'s simple pleasures.',
                'memory_tip': 'Remember "FRUGAL" - being careful with money to get FRUIT (value) from your resources, avoiding waste.'
            },
            'frugivore': {
                'definition': 'A frugivore is an animal that primarily feeds on fruit, playing important ecological roles as seed dispersers for plants. These animals have evolved specialized adaptations for locating, consuming, and digesting fruits, including enhanced color vision for spotting ripe fruit and digestive systems that process sugary plant matter. Examples include many primates, birds, and bats. Frugivores are crucial for forest ecosystems because they spread seeds to new locations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FROO-jih-vor',
                'etymology': 'From Latin "frux" (fruit) plus "vorare" (to devour), literally meaning "fruit-eater."',
                'language_origins': 'Latin',
                'example_sentence': 'The toucan is a _______ that helps spread seeds throughout the rainforest canopy.',
                'memory_tip': 'Remember "FRUGIVORE" - an animal that VORes (devours) FRUIT, like a fruit-eating specialist.'
            },
            'fruit': {
                'definition': 'Fruit refers to the mature, seed-bearing structure of flowering plants, typically sweet and edible, developed from the flower after pollination. In botanical terms, fruit includes many items not commonly thought of as fruits, such as tomatoes and nuts. In culinary usage, fruit generally refers to sweet, fleshy structures eaten as food. Metaphorically, fruit represents the results or outcomes of effort, as in "fruits of one\'s labor."',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FROOT',
                'etymology': 'From Latin "fructus" meaning "enjoyment, produce, fruit," from "frui" (to enjoy, have the benefit of).',
                'language_origins': 'Latin',
                'example_sentence': 'The orchard produced abundant _______ that was harvested and sold at local markets.',
                'memory_tip': 'Remember "FRUIT" - the sweet produce that plants make, giving us the FRUITS of nature\'s labor.'
            },
            'fruition': {
                'definition': 'Fruition means the realization or fulfillment of a plan, project, or desire; the point at which something comes to completion or bears results. It describes the successful achievement of goals after effort and time, like fruit coming to ripeness on a tree. Fruition implies not just completion but the satisfaction of seeing efforts rewarded with positive outcomes or the materialization of hopes and dreams.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'froo-ISH-un',
                'etymology': 'From Latin "fruitio" meaning "enjoyment," from "frui" (to enjoy), related to "fructus" (fruit, produce).',
                'language_origins': 'Latin',
                'example_sentence': 'After years of planning and work, the community garden project finally came to _______.',
                'memory_tip': 'Remember "FRUITION" - when plans bear FRUIT, like projects reaching their fruitful completion and success.'
            },
            'fruits': {
                'definition': 'Fruits is the plural form of fruit, referring to multiple seed-bearing structures of plants that are typically sweet and edible. The word encompasses the variety of natural produce including apples, oranges, berries, and tropical fruits that provide nutrition, flavor, and enjoyment. Metaphorically, fruits refers to multiple positive results or benefits arising from effort, work, or investment, as in enjoying the fruits of one\'s labor.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'FROOTS',
                'etymology': 'Plural of "fruit," from Latin "fructus" meaning "produce, results."',
                'language_origins': 'Latin',
                'example_sentence': 'The tropical market offered exotic _______ from around the world.',
                'memory_tip': 'Remember "FRUITS" - multiple FRUIT varieties, like different fruits of nature or fruits of your efforts.'
            },
            'frutti': {
                'definition': 'Frutti is an Italian word meaning "fruits" (plural), commonly encountered in English through culinary terms like "tutti frutti" (all fruits), describing mixed fruit flavors in ice cream, candy, or other foods. In English usage, frutti typically appears in food contexts, particularly describing fruit-flavored items or dishes containing mixed fruits. The word emphasizes the Italian culinary tradition of using multiple fruit varieties together.',
                'part_of_speech': 'noun (Italian)',
                'pronunciation_guide': 'FROO-tee',
                'etymology': 'From Italian "frutti," plural of "frutto" (fruit), ultimately from Latin "fructus."',
                'language_origins': 'Italian, Latin',
                'example_sentence': 'The gelato shop served delicious tutti _______ ice cream with mixed fruit flavors.',
                'memory_tip': 'Remember "FRUTTI" - Italian for fruits, like "FRUITY" flavors in Italian gelato and desserts.'
            },
            'frutticantor': {
                'definition': 'Frutticantor appears to be a combined word error where "frutti" (Italian for fruits) and "cantor" (a singer or church official) were incorrectly merged during PDF processing. These are unrelated concepts - one refers to fruits in Italian cuisine and the other to religious or musical leadership. This represents a data quality issue where two distinct terms from different domains were improperly joined together.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'FROO-tee-KAN-tor',
                'etymology': 'Corrupted combination of Italian "frutti" (fruits) and Latin "cantor" (singer).',
                'language_origins': 'Italian, Latin (corrupted)',
                'example_sentence': 'The word _______ appears to be a parsing error combining Italian fruit terminology with religious music terms.',
                'memory_tip': 'This is a data error - remember that "frutti" (fruits) and "cantor" (singer) should be separate words.'
            },
            'fucoid': {
                'definition': 'Fucoid refers to seaweeds or algae belonging to the order Fucales, which includes brown algae commonly found in marine environments, particularly in tidal zones. These algae are characterized by their leathery texture and branching structure. The term can also describe fossil traces or structures that resemble seaweed. Fucoid algae play important ecological roles in marine ecosystems, providing habitat and food for various marine organisms.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'FYOO-koid',
                'etymology': 'From Latin "fucus" meaning "seaweed" (from Greek "phykos") plus the suffix "-oid" meaning "resembling."',
                'language_origins': 'Latin, Greek',
                'example_sentence': 'The rocky coastline was covered with _______ algae that provided habitat for small marine creatures.',
                'memory_tip': 'Remember "FUCOID" - seaweed that looks like FOCUS-oid, focused on growing in marine environments.'
            },
            'fuddy': {
                'definition': 'Fuddy, typically found in the phrase "fuddy-duddy," describes a person who is old-fashioned, stuffy, or overly conservative in their attitudes and behavior. A fuddy-duddy is someone who resists change, clings to traditional ways, and often criticizes modern trends or innovations. The term suggests someone who is out of touch with current times and overly concerned with propriety or conventional behavior.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'FUD-ee',
                'etymology': 'Origin uncertain, possibly from "fud" (buttocks) implying someone who sits around, combined with reduplication to create "fuddy-duddy."',
                'language_origins': 'English (uncertain origin)',
                'example_sentence': 'The old professor was considered a _______ because he refused to use modern technology in his lectures.',
                'memory_tip': 'Remember "FUDDY" - part of "fuddy-duddy," someone so old-fashioned they seem to FUD around with outdated ideas.'
            },
            'fudge': {
                'definition': 'Fudge is a soft, rich confectionery made from sugar, butter, milk, and flavorings, typically chocolate, cooked to a specific temperature to achieve a smooth, creamy texture. As a verb, fudge means to avoid giving a direct answer, to present information in a misleading way, or to adjust figures or facts dishonestly. The word can also express mild frustration as a euphemistic exclamation. In both senses, fudge suggests something sweet but potentially deceptive.',
                'part_of_speech': 'noun, verb, exclamation',
                'pronunciation_guide': 'FUJ',
                'etymology': 'Origin uncertain, possibly from "fadge" (to fit), or from sailors\' slang meaning "nonsense." The candy meaning may be from the sense of "fitting together" ingredients.',
                'language_origins': 'English (uncertain origin)',
                'example_sentence': 'She made delicious chocolate _______ for the holiday gift boxes.',
                'memory_tip': 'Remember "FUDGE" - sweet candy that can also mean to FUDGE the truth, both involving mixing things together.'
            },
            'fuel': {
                'definition': 'Fuel is any substance that can be burned or otherwise consumed to produce energy, heat, or power, including gasoline, coal, wood, or natural gas. The word also refers to anything that sustains, encourages, or intensifies an activity or process, such as "fuel for thought" or emotional fuel for motivation. As a verb, fuel means to supply with energy or to stimulate and intensify something like anger or enthusiasm.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FYOOL',
                'etymology': 'From Old French "fueille" meaning "fuel, firewood," from Latin "focale" (relating to the hearth), from "focus" (fireplace, hearth).',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The car needed _______ before they could continue their long journey.',
                'memory_tip': 'Remember "FUEL" - what feeds the fire to create power, like FOOD for engines and machines.'
            }
        }
        
        return batch_072_data.get(word, {
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
            if word == 'freezescorch':
                errors.append(f"{word}: Combined word error: \"freezescorch\" appears to be \"freeze\" + \"scorch\" merged together. This is likely a PDF parsing error where two opposite weather terms were incorrectly combined.")
            elif word == 'frockcamcorder':
                errors.append(f"{word}: Combined word error: \"frockcamcorder\" appears to be \"frock\" + \"camcorder\" merged together. This is likely a PDF parsing error where clothing and electronics terms were incorrectly combined.")
            elif word == 'froufroudifficulty':
                errors.append(f"{word}: Combined word error: \"froufroudifficulty\" appears to be \"froufrou\" + \"difficulty\" merged together. This is likely a PDF parsing error where two separate terms were incorrectly combined.")
            elif word == 'frutticantor':
                errors.append(f"{word}: Combined word error: \"frutticantor\" appears to be \"frutti\" + \"cantor\" merged together. This is likely a PDF parsing error where Italian fruit terms and musical terms were incorrectly combined.")
            elif word == 'frison':
                errors.append(f"{word}: Possible variant: \"frison\" may be a variant or error for \"frisson\" (emotional thrill). This could be a spelling variant or transcription error.")
                
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
        print("Batch 072 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch072Processor()
    processor.process_batch(
        "output/batch_072_words.csv",
        "output/batch_072_processed.csv"
    )