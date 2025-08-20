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

class Batch073Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for a word using Claude knowledge"""
        
        batch_073_data = {
            'fugue': {
                'definition': 'A fugue is a complex musical composition technique where a main theme (subject) is introduced by one voice and then imitated by other voices in succession, creating intricate counterpoint. In psychology, fugue refers to a dissociative disorder characterized by sudden, unexpected travel away from home with inability to recall one\'s past. Both meanings share the concept of departure and complex, interwoven patterns - musical voices weaving together or consciousness departing from normal patterns.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FYOOG',
                'etymology': 'From Latin "fuga" meaning "flight," from "fugere" (to flee), referring to the musical voices "fleeing" or following each other in succession.',
                'language_origins': 'Latin',
                'example_sentence': 'Bach\'s intricate _______ demonstrated masterful counterpoint with multiple voices weaving the same theme.',
                'memory_tip': 'Remember "FUGUE" - musical voices that FLEW from each other, following the same theme in flight.'
            },
            'fulcrum': {
                'definition': 'A fulcrum is the pivot point or support on which a lever rests and rotates, enabling mechanical advantage by allowing a small force to move a larger load. Metaphorically, a fulcrum represents any central point of support, balance, or crucial element around which other things turn or depend. The concept emphasizes the strategic importance of positioning and leverage in both physical and abstract systems.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FUL-krum',
                'etymology': 'From Latin "fulcrum" meaning "bedpost, support," from "fulcire" (to prop up, support).',
                'language_origins': 'Latin',
                'example_sentence': 'The negotiations reached a _______ point where one decision would determine the entire outcome.',
                'memory_tip': 'Remember "FULCRUM" - the FUL point where you can CRUsh heavy loads with leverage, the crucial support point.'
            },
            'fulfillment': {
                'definition': 'Fulfillment means the achievement of something desired, promised, or predicted; the satisfaction derived from fully developing one\'s abilities and realizing one\'s potential. It encompasses both the completion of goals or obligations and the deep personal satisfaction that comes from meaningful accomplishment. Fulfillment suggests not just completion but the emotional and spiritual satisfaction that accompanies achieving one\'s purpose or reaching important milestones.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'ful-FIL-ment',
                'etymology': 'From "fulfill" (from Old English "fullfyllan" meaning "to fill up completely") plus the suffix "-ment" indicating the result of action.',
                'language_origins': 'Old English',
                'example_sentence': 'She found deep _______ in her career as a teacher, knowing she made a difference.',
                'memory_tip': 'Remember "FULFILLMENT" - when you FILL your life FULL of meaningful accomplishments and satisfaction.'
            },
            'fulgent': {
                'definition': 'Fulgent means shining brightly, radiant, or dazzling with brilliant light. It describes something that gleams or glows with intense luminosity, often suggesting divine or supernatural brightness. The word conveys not just light but specifically brilliant, impressive illumination that commands attention and suggests power or significance. Fulgent emphasizes the impressive and almost overwhelming quality of bright light.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FUL-jent',
                'etymology': 'From Latin "fulgens" meaning "shining, gleaming," present participle of "fulgere" (to shine, flash, gleam).',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ sunrise painted the mountain peaks with brilliant golden light.',
                'memory_tip': 'Remember "FULGENT" - so FULL of brilliant light it\'s like lightning (fulgor), blazing and gleaming.'
            },
            'full': {
                'definition': 'Full means containing as much as possible, complete in extent or degree, or having all necessary parts or elements. It describes a state of maximum capacity, completeness, or satisfaction. Full can refer to physical containers, emotional states, time periods, or abstract concepts. The word emphasizes totality, abundance, and the absence of lack or deficiency.',
                'part_of_speech': 'adjective, adverb, noun, verb',
                'pronunciation_guide': 'FUL',
                'etymology': 'From Old English "full" meaning "full, filled, complete," related to German "voll" and ultimately from Proto-Indo-European "*plh₁nós."',
                'language_origins': 'Old English, Proto-Indo-European',
                'example_sentence': 'The glass was _______ of fresh water, ready to quench her thirst.',
                'memory_tip': 'Remember "FULL" - when something is FILLED to capacity, completely stuffed or complete.'
            },
            'fulminate': {
                'definition': 'Fulminate means to express vehement protest, criticism, or condemnation; to speak angrily and forcefully against something. In chemistry, fulminate refers to explosive compounds that detonate upon impact. Both meanings share the concept of sudden, violent reaction - whether verbal explosion of anger or chemical explosion. The word suggests intense, volatile reaction that can be triggered easily and produces dramatic results.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'FUL-muh-nayt',
                'etymology': 'From Latin "fulminare" meaning "to lighten, strike with lightning," from "fulmen" (lightning, thunderbolt).',
                'language_origins': 'Latin',
                'example_sentence': 'The senator began to _______ against the proposed legislation during the heated debate.',
                'memory_tip': 'Remember "FULMINATE" - to explode with anger like lightning (fulmen), striking out with thunderous criticism.'
            },
            'fumatorium': {
                'definition': 'A fumatorium is a chamber or facility designed for fumigation, the process of disinfecting or purifying through exposure to chemical fumes or smoke. These specialized rooms were historically used for treating diseases, disinfecting objects, or therapeutic purposes. Fumatoriums might also refer to places where medicinal vapors or therapeutic smoke treatments were administered, combining medical treatment with controlled exposure to beneficial fumes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fyoo-muh-TOR-ee-um',
                'etymology': 'From Latin "fumatorium," derived from "fumare" (to smoke, emit fumes) plus the suffix "-orium" (place for).',
                'language_origins': 'Latin',
                'example_sentence': 'The historical hospital included a _______ for disinfecting medical equipment with medicinal vapors.',
                'memory_tip': 'Remember "FUMATORIUM" - a place (-orium) for FUME treatment, like an auditorium for fumes and fumigation.'
            },
            'fumble': {
                'definition': 'Fumble means to handle something clumsily or awkwardly, to grope about uncertainly, or to fail to catch, hold, or handle something properly. In sports, particularly football, a fumble is losing control of the ball. The word suggests uncertain, clumsy actions often resulting from nervousness, haste, or lack of skill. Fumbling implies a lack of dexterity or confidence in handling objects or situations.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'FUM-bul',
                'etymology': 'From Middle English "fomblen," possibly related to "fum" meaning "to grope," of uncertain origin but possibly imitative.',
                'language_origins': 'Middle English',
                'example_sentence': 'She began to _______ with her keys in the dark, struggling to find the right one.',
                'memory_tip': 'Remember "FUMBLE" - to handle things in a FUMBLY way, dropping or mishandling due to clumsiness.'
            },
            'funambulist': {
                'definition': 'A funambulist is a tightrope walker or acrobat who performs on a rope or wire suspended high above the ground. The term emphasizes the artistic and skilled nature of this performance, requiring exceptional balance, courage, and concentration. Funambulists are entertainers who combine athletic ability with theatrical presentation, often performing daring feats while maintaining grace and control on their precarious perch.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fyoo-NAM-byuh-list',
                'etymology': 'From Latin "funambulus" meaning "rope walker," composed of "funis" (rope) plus "ambulare" (to walk).',
                'language_origins': 'Latin',
                'example_sentence': 'The skilled _______ captivated the circus audience by walking gracefully across the high wire.',
                'memory_tip': 'Remember "FUNAMBULIST" - someone who can walk FUNNY on ROPE, a FUN AMBULating (walking) performer on tightropes.'
            },
            'functionary': {
                'definition': 'A functionary is a person who holds an official position or performs administrative duties within an organization, government, or bureaucracy, typically following established procedures rather than making independent decisions. The term often implies someone who carries out routine tasks within a larger system, emphasizing their role as part of institutional machinery rather than as an individual leader or innovator.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FUNK-shuh-ner-ee',
                'etymology': 'From "function" (from Latin "functio," meaning "performance, execution") plus the suffix "-ary" indicating a person associated with.',
                'language_origins': 'Latin',
                'example_sentence': 'The government _______ processed the applications according to established bureaucratic procedures.',
                'memory_tip': 'Remember "FUNCTIONARY" - a person whose job is to FUNCTION in a specific role, performing routine duties.'
            },
            'fundamental': {
                'definition': 'Fundamental refers to something that is basic, essential, or foundational; forming the necessary base or core from which other things develop. It describes principles, concepts, or elements that are indispensable and serve as the underlying foundation for more complex structures or ideas. Fundamental suggests not just importance but absolute necessity - without these elements, the whole system would not function.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'fun-duh-MEN-tul',
                'etymology': 'From Latin "fundamentalis," derived from "fundamentum" (foundation) from "fundare" (to found, lay the bottom).',
                'language_origins': 'Latin',
                'example_sentence': 'Learning to read is _______ to all other educational achievements.',
                'memory_tip': 'Remember "FUNDAMENTAL" - the FOUNDATION that\'s MENTAL, the basic building blocks of understanding.'
            },
            'fungible': {
                'definition': 'Fungible describes goods, commodities, or assets that are interchangeable with other identical items because each unit is equivalent in value and function. In economics and law, fungible items can be substituted for one another without loss of value - such as money, oil, or grain. The concept is crucial in commerce, contracts, and finance, where the ability to replace one item with an identical equivalent is essential for trade.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FUN-jih-bul',
                'etymology': 'From Medieval Latin "fungibilis" meaning "that may serve in place of," from Latin "fungi" (to perform, execute).',
                'language_origins': 'Medieval Latin, Latin',
                'example_sentence': 'Gold is a _______ commodity because one ounce can be exchanged for any other ounce of equal purity.',
                'memory_tip': 'Remember "FUNGIBLE" - items that can be FLUNG around and substituted, because they FUNCTION the same way.'
            },
            'funky': {
                'definition': 'Funky originally described a strong, musty, or earthy smell, but has evolved to mean having a strong, distinctive style, especially in music characterized by syncopated rhythm and prominent bass lines. In contemporary usage, funky means stylish in an unconventional or offbeat way, or having an unpleasant smell. The word suggests something with character, soul, or distinctive personality that stands out from the ordinary.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FUNK-ee',
                'etymology': 'Possibly from "funk" meaning "musty smell," which may derive from French "funkière" (smoke), or from African American slang meaning "earthy, soulful."',
                'language_origins': 'English, possibly French or African American',
                'example_sentence': 'The band played _______ music with a driving bass line that made everyone dance.',
                'memory_tip': 'Remember "FUNKY" - music with FUNK and soul, or something with a distinctive (sometimes smelly) character.'
            },
            'funnel': {
                'definition': 'A funnel is a cone-shaped utensil with a wide mouth tapering to a narrow tube, used for guiding liquid or powder into a small opening. As a verb, funnel means to channel or direct something through a restricted passage, or to move through a narrow space. Metaphorically, funnel describes any process that narrows or concentrates flow, whether of materials, information, money, or people.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FUN-ul',
                'etymology': 'From Old French "founel," ultimately from Latin "infundibulum" meaning "funnel," from "infundere" (to pour in).',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'She used a _______ to pour the oil into the narrow opening of the engine.',
                'memory_tip': 'Remember "FUNNEL" - a FUN way to chanNEL liquids from wide to narrow, avoiding spills.'
            },
            'funori': {
                'definition': 'Funori is a seaweed-based adhesive traditionally used in Japanese art, particularly for mounting paintings and in bookbinding. This natural glue is extracted from certain species of red algae and is prized for its archival qualities, flexibility, and reversibility. Funori is also used in textile arts and conservation work because it doesn\'t become brittle over time and can be removed if necessary.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'foo-NOR-ee',
                'etymology': 'From Japanese "funori" (布海苔), literally meaning "cloth seaweed," referring to its traditional use in textile and paper arts.',
                'language_origins': 'Japanese',
                'example_sentence': 'The art conservator used traditional _______ to repair the antique Japanese scroll.',
                'memory_tip': 'Remember "FUNORI" - a FUN seaweed-based glue from Japan, perfect for NORmal art conservation work.'
            },
            'furan': {
                'definition': 'Furan is an organic chemical compound consisting of a five-membered aromatic ring containing four carbon atoms and one oxygen atom. It is an important building block in organic chemistry and occurs naturally in many plants. Furan derivatives are used in the production of various chemicals, pharmaceuticals, and materials. The compound has a distinctive smell and plays roles in both industrial chemistry and natural biological processes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FYOOR-an',
                'etymology': 'From Latin "furfur" meaning "bran," because furan was first isolated from furfural, which was derived from agricultural waste like bran.',
                'language_origins': 'Latin',
                'example_sentence': 'The chemist synthesized new compounds using _______ as the base aromatic ring structure.',
                'memory_tip': 'Remember "FURAN" - an organic compound that sounds like FURY, with one oxygen atom causing chemical excitement.'
            },
            'furanmanu': {
                'definition': 'Furanmanu appears to be a combined word error where "furan" (an organic chemical compound) and possibly "manu" (Latin for "hand" or a name) were incorrectly merged during PDF processing. This represents a data quality issue where a chemistry term was improperly joined with another term. The intended words should likely be separated as "furan" and whatever term was combined with it.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'FYOOR-an-MAH-noo',
                'etymology': 'Corrupted combination of "furan" (from Latin "furfur") and possibly "manu" (Latin for "hand") or another term.',
                'language_origins': 'Latin (corrupted)',
                'example_sentence': 'The word _______ appears to be a parsing error combining chemical and other terminology.',
                'memory_tip': 'This is a data error - remember that "furan" should be separated from whatever term was incorrectly combined with it.'
            },
            'furcula': {
                'definition': 'A furcula is the wishbone or forked bone found in birds and some dinosaurs, formed by the fusion of the two clavicles (collarbones). This Y-shaped bone serves as a spring mechanism during flight, storing and releasing energy with each wingbeat to make flight more efficient. In paleontology, the presence of a furcula in dinosaur fossils provides evidence of the evolutionary link between dinosaurs and birds.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FUR-kyuh-luh',
                'etymology': 'From Latin "furcula" meaning "little fork," diminutive of "furca" (fork, pitchfork).',
                'language_origins': 'Latin',
                'example_sentence': 'The bird\'s _______ acts as a spring during flight, making each wingbeat more efficient.',
                'memory_tip': 'Remember "FURCULA" - the FORK-like bone (furca) that\'s little (-cula), the bird\'s wishbone fork.'
            },
            'furious': {
                'definition': 'Furious means extremely angry, filled with rage, or characterized by intense, violent emotion. It describes a state of anger so intense that it may impair judgment and lead to aggressive behavior. The word can also describe actions, weather, or activities that are intense, violent, or carried out with great energy and speed. Furious suggests anger or intensity that is barely controlled and potentially destructive.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FYOOR-ee-us',
                'etymology': 'From Latin "furiosus" meaning "full of rage, mad," from "furia" (rage, fury), related to "furere" (to rage, be mad).',
                'language_origins': 'Latin',
                'example_sentence': 'She was _______ when she discovered someone had stolen her bicycle.',
                'memory_tip': 'Remember "FURIOUS" - so full of FURY that you\'re raging, burning with intense anger.'
            },
            'furnace': {
                'definition': 'A furnace is an enclosed chamber or structure designed for heating materials to very high temperatures, used for purposes such as heating buildings, melting metals, or conducting industrial processes. Furnaces burn fuel or use electricity to generate intense heat, often reaching temperatures of hundreds or thousands of degrees. The word also refers metaphorically to any situation involving intense heat, pressure, or difficulty.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FUR-nis',
                'etymology': 'From Old French "fornaise," from Latin "fornax" meaning "oven, furnace," related to "fornus" (oven).',
                'language_origins': 'Old French, Latin',
                'example_sentence': 'The steel mill\'s massive _______ heated iron ore to over 2000 degrees Fahrenheit.',
                'memory_tip': 'Remember "FURNACE" - a hot chamber that can BURN with furious heat, like a BURNING place for heating.'
            },
            'furneaux': {
                'definition': 'Furneaux typically refers to the Furneaux Group, a collection of islands in Bass Strait between mainland Australia and Tasmania, or may reference places named after French explorer Tobias Furneaux. In spelling bee contexts, it represents knowledge of geographical terminology and French surnames. The word demonstrates the intersection of exploration history, geography, and the French language influence on English place names.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'fur-NOH',
                'etymology': 'French surname, ultimately from a place name possibly meaning "furnaces" (plural of Old French "fornel," furnace).',
                'language_origins': 'French',
                'example_sentence': 'The _______ Group consists of over 50 islands in the waters between Australia and Tasmania.',
                'memory_tip': 'Remember "FURNEAUX" - sounds like "FUR-no" (French for oven), named after French explorer Furneaux.'
            },
            'furniture': {
                'definition': 'Furniture refers to movable objects designed to support various human activities such as seating, eating, sleeping, and storage. These functional items include chairs, tables, beds, cabinets, and other pieces that equip homes, offices, and other spaces for practical use and comfort. Furniture combines utility with design, serving both practical needs and aesthetic preferences in interior spaces.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FUR-ni-chur',
                'etymology': 'From French "fourniture" meaning "a furnishing, supply," from "fournir" (to furnish, supply).',
                'language_origins': 'French',
                'example_sentence': 'They carefully selected _______ that was both functional and stylish for their new apartment.',
                'memory_tip': 'Remember "FURNITURE" - items that FURNISH and equip rooms, making spaces functional and comfortable.'
            },
            'furnitureambush': {
                'definition': 'Furnitureambush appears to be a combined word error where "furniture" (movable household items) and "ambush" (a surprise attack) were incorrectly merged during PDF processing. These are completely unrelated concepts - one refers to household objects and the other to military tactics. This represents a data quality issue where two distinct terms from different domains were improperly joined together.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'FUR-ni-chur-AM-bush',
                'etymology': 'Corrupted combination of "furniture" (from French "fourniture") and "ambush" (from Old French "embusche").',
                'language_origins': 'French, Old French (corrupted)',
                'example_sentence': 'The word _______ appears to be a parsing error combining household items with military terminology.',
                'memory_tip': 'This is a data error - remember that "furniture" and "ambush" should be separate words, not combined.'
            },
            'furrow': {
                'definition': 'A furrow is a long, narrow trench or groove made in the ground, especially by a plow during farming to prepare soil for planting seeds. The word also describes similar grooves or wrinkles in other contexts, such as furrows in a person\'s brow from concentration or worry. As a verb, furrow means to create these grooves or to show lines of concentration or concern in one\'s face.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FUR-oh',
                'etymology': 'From Old English "furh" meaning "furrow, trench," related to Latin "porca" (ridge between furrows) and ultimately from a root meaning "to dig."',
                'language_origins': 'Old English',
                'example_sentence': 'The farmer plowed neat _______ across the field in preparation for spring planting.',
                'memory_tip': 'Remember "FURROW" - a groove that FOLLOWS the plow, creating rows for farming (sounds like "follow").'
            },
            'furthermore': {
                'definition': 'Furthermore is an adverb used to introduce additional information or arguments that support or extend a previous point. It serves as a transitional word meaning "in addition to what has been said" or "moreover." Furthermore strengthens discourse by building upon earlier statements, helping to develop arguments or explanations in a logical, progressive manner.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'FUR-ther-mor',
                'etymology': 'Compound of "further" (from Old English "furthor," comparative of "forth") plus "more," literally meaning "more in addition."',
                'language_origins': 'Old English',
                'example_sentence': '_______, the research shows that regular exercise improves both physical and mental health.',
                'memory_tip': 'Remember "FURTHERMORE" - going FURTHER with MORE information, adding additional points to your argument.'
            },
            'furtive': {
                'definition': 'Furtive describes behavior that is stealthy, secretive, or characterized by an attempt to avoid notice or detection. It suggests actions done in a sneaky, surreptitious manner, often because the person feels guilty, ashamed, or is trying to hide something. Furtive behavior typically involves quick, careful movements and avoidance of direct eye contact or attention.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FUR-tiv',
                'etymology': 'From Latin "furtivus" meaning "stolen, secret," from "furtum" (theft) related to "fur" (thief).',
                'language_origins': 'Latin',
                'example_sentence': 'She cast a _______ glance around the room before quietly slipping the note into her pocket.',
                'memory_tip': 'Remember "FURTIVE" - sneaky like a FUR thief, stealing secretly and trying not to be caught.'
            },
            'furuncle': {
                'definition': 'A furuncle is a painful, pus-filled bump on the skin caused by bacterial infection of a hair follicle, commonly known as a boil. These skin infections typically develop when bacteria, usually Staphylococcus aureus, enters through small cuts or hair follicles. Furuncles appear as red, swollen, tender nodules that eventually form a head of pus and may require medical treatment or drainage.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FYOOR-unk-ul',
                'etymology': 'From Latin "furunculus" meaning "petty thief," diminutive of "fur" (thief), metaphorically referring to how the infection "steals" health.',
                'language_origins': 'Latin',
                'example_sentence': 'The doctor drained the painful _______ and prescribed antibiotics to treat the bacterial infection.',
                'memory_tip': 'Remember "FURUNCLE" - a skin infection like a little FURY on your skin, an angry boil that steals comfort.'
            },
            'fury': {
                'definition': 'Fury refers to intense, violent anger or rage that is often uncontrolled and overwhelming. It describes an extreme emotional state characterized by fierce passion, wrath, or indignation that may lead to aggressive behavior. In mythology, the Furies were goddesses of vengeance. Fury can also describe intense force or violence in nature, such as the fury of a storm.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FYOOR-ee',
                'etymology': 'From Latin "furia" meaning "rage, passion, fury," related to "furere" (to rage, be mad), from an Indo-European root meaning "to rage."',
                'language_origins': 'Latin',
                'example_sentence': 'His _______ at the injustice was so intense that he could barely speak coherently.',
                'memory_tip': 'Remember "FURY" - extreme anger that makes you feel like you\'re on FIRE with rage, burning with fierce emotion.'
            },
            'fuselage': {
                'definition': 'A fuselage is the main body or central structure of an aircraft, containing the cockpit, passenger cabin, and cargo areas. This streamlined, tube-like section connects the wings, tail, and other components while providing the primary structure that houses crew, passengers, and equipment. The fuselage is designed for aerodynamic efficiency and structural integrity to withstand the stresses of flight.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FYOO-suh-lahzh',
                'etymology': 'From French "fuselage," derived from "fuseau" (spindle) due to the spindle-like shape of early aircraft bodies.',
                'language_origins': 'French',
                'example_sentence': 'The aircraft\'s _______ was painted with the airline\'s distinctive colors and logo.',
                'memory_tip': 'Remember "FUSELAGE" - the main body of a plane, shaped like a FUSE that holds everything together in flight.'
            },
            'fusiform': {
                'definition': 'Fusiform means having a spindle shape that is wider in the middle and tapers toward both ends, resembling the shape of a spindle or cigar. This term is commonly used in biology and anatomy to describe structures like certain muscles, cells, or organisms that have this characteristic elongated, tapering form. The fusiform shape is often aerodynamic or hydrodynamic, providing efficiency in movement through fluids.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'FYOO-zi-form',
                'etymology': 'From Latin "fusus" (spindle) plus "forma" (shape), literally meaning "spindle-shaped."',
                'language_origins': 'Latin',
                'example_sentence': 'The _______ bacteria had the characteristic cigar-like shape that tapered at both ends.',
                'memory_tip': 'Remember "FUSIFORM" - shaped like a FUSE, wider in the middle and tapering at both ends like a spindle.'
            },
            'fussbudget': {
                'definition': 'A fussbudget is a person who worries excessively about minor details, is overly particular about small matters, or gets upset about trivial things. This term describes someone who is fussy, nitpicky, and tends to make a big deal out of small problems or imperfections. Fussbudgets are often seen as unnecessarily anxious or demanding about things that others consider unimportant.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'FUSS-buj-it',
                'etymology': 'Compound of "fuss" (from Germanic roots meaning "to be eager") plus "budget" used colloquially to mean "person," literally "a person who fusses."',
                'language_origins': 'Germanic, English',
                'example_sentence': 'Don\'t be such a _______ about the decorations - they look perfectly fine as they are.',
                'memory_tip': 'Remember "FUSSBUDGET" - someone who makes a FUSS about every little thing, budgeting their worry on tiny details.'
            },
            'futility': {
                'definition': 'Futility refers to the quality of being pointless, useless, or incapable of producing any useful result. It describes the condition of actions, efforts, or endeavors that are doomed to failure or that serve no meaningful purpose. Futility suggests not just failure but the inherent impossibility of success, making continued effort seem wasteful or hopeless.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'fyoo-TIL-ih-tee',
                'etymology': 'From Latin "futilis" meaning "leaky, untrustworthy, vain," possibly related to "fundere" (to pour), suggesting something that cannot hold anything valuable.',
                'language_origins': 'Latin',
                'example_sentence': 'He recognized the _______ of arguing with someone who refused to listen to reason.',
                'memory_tip': 'Remember "FUTILITY" - efforts that are so FUTile they leak away like water, achieving nothing useful.'
            },
            'future': {
                'definition': 'Future refers to the time that is yet to come, events that will happen after the present moment, or potential developments and possibilities that await. As an adjective, future describes things that will exist, happen, or be relevant in coming times. The concept encompasses both predictable developments and unknown possibilities, representing humanity\'s forward-looking perspective and planning capabilities.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'FYOO-chur',
                'etymology': 'From Latin "futurus" meaning "about to be," future participle of "esse" (to be).',
                'language_origins': 'Latin',
                'example_sentence': 'She planned carefully for her _______, saving money and developing valuable skills.',
                'memory_tip': 'Remember "FUTURE" - what\'s coming in the FUTURE, the time that will BE (futurus) after now.'
            },
            'fêng': {
                'definition': 'Fêng appears in the context of "feng shui," the Chinese practice of arranging spaces to promote harmony and positive energy flow. "Feng" (風) means "wind" in Chinese, while "shui" (水) means "water." In spelling bee contexts, this represents knowledge of Chinese philosophical concepts that have entered English usage. The practice involves positioning objects and structures to optimize the flow of life energy (qi).',
                'part_of_speech': 'noun (Chinese concept)',
                'pronunciation_guide': 'FUNG',
                'etymology': 'From Chinese "風" (feng) meaning "wind," an element in the geomantic practice of feng shui.',
                'language_origins': 'Chinese',
                'example_sentence': 'The interior designer considered _______ shui principles when arranging the office furniture.',
                'memory_tip': 'Remember "FÊNG" - the wind (feng) element in feng shui, helping energy flow like wind through spaces.'
            },
            'fête': {
                'definition': 'A fête is an elaborate festival, celebration, or party, typically featuring entertainment, food, and festivities. The word suggests a joyous public celebration or elaborate social gathering with special activities and attractions. Fêtes often commemorate special occasions, holidays, or community events, emphasizing collective enjoyment and festive atmosphere. The term implies something more elaborate and special than an ordinary party.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'FAYT',
                'etymology': 'From French "fête" meaning "feast, festival," from Latin "festa" (neuter plural of "festus," meaning "festive").',
                'language_origins': 'French, Latin',
                'example_sentence': 'The village _______ featured live music, traditional dancing, and local artisan crafts.',
                'memory_tip': 'Remember "FÊTE" - a FESTIVE celebration, like a fancy French party with the circumflex accent (fête).'
            },
            'gabarit': {
                'definition': 'Gabarit refers to a template, pattern, or gauge used as a guide for shaping or measuring objects, particularly in construction, engineering, or manufacturing. It can also mean the maximum dimensions or clearance limits for vehicles, structures, or equipment. In French usage, gabarit describes the overall size, build, or physical dimensions of something, including a person\'s stature or build.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gah-bah-REE',
                'etymology': 'From French "gabarit," possibly from Provençal "gabarit," ultimately from Arabic "al-qālib" (the mold, template).',
                'language_origins': 'French, Arabic',
                'example_sentence': 'The carpenter used a wooden _______ to ensure all the pieces were cut to identical specifications.',
                'memory_tip': 'Remember "GABARIT" - a pattern or GAUGE that helps you get the right size, like a measuring template.'
            },
            'gabbro': {
                'definition': 'Gabbro is a coarse-grained, dark-colored igneous rock composed primarily of plagioclase feldspar and pyroxene minerals, formed when magma cools slowly beneath the Earth\'s surface. This intrusive rock is the plutonic equivalent of basalt and is important in both geology and construction. Gabbro is often used as a building stone and in road construction due to its durability and attractive appearance when polished.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAB-roh',
                'etymology': 'From Italian "gabbro," the name of a town in Tuscany, Italy, where this type of rock was first identified and described.',
                'language_origins': 'Italian',
                'example_sentence': 'The geologist identified the dark, coarse-grained rock sample as _______.',
                'memory_tip': 'Remember "GABBRO" - a dark rock that\'s good for GABbing about geology, named after an Italian town.'
            },
            'gabbroplural': {
                'definition': 'Gabbroplural appears to be a combined word error where "gabbro" (a type of igneous rock) and "plural" (grammatical term indicating more than one) were incorrectly merged during PDF processing. This represents a data quality issue where a geological term was improperly joined with grammatical notation. The intended content should be "gabbro" as a geological term with separate grammatical information.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'GAB-roh-PLOOR-ul',
                'etymology': 'Corrupted combination of "gabbro" (Italian rock name) and "plural" (Latin grammatical term).',
                'language_origins': 'Italian, Latin (corrupted)',
                'example_sentence': 'The word _______ appears to be a parsing error combining geological and grammatical terminology.',
                'memory_tip': 'This is a data error - remember that "gabbro" (rock type) and "plural" (grammar) should be separate.'
            },
            'gabdifficulty': {
                'definition': 'Gabdifficulty appears to be a combined word error where "gab" (informal talk or chatter) and "difficulty" were incorrectly merged during PDF processing. This represents a data quality issue where a casual term for talking was improperly joined with a word meaning challenge or problem. These terms should be separated as they represent different concepts.',
                'part_of_speech': 'corrupted entry',
                'pronunciation_guide': 'GAB-DIF-ih-kul-tee',
                'etymology': 'Corrupted combination of "gab" (possibly from "gabble") and "difficulty" (from Latin "difficultas").',
                'language_origins': 'English, Latin (corrupted)',
                'example_sentence': 'The word _______ appears to be a parsing error combining casual speech with complexity terminology.',
                'memory_tip': 'This is a data error - remember that "gab" (talk) and "difficulty" (challenge) should be separate words.'
            },
            'gadgets': {
                'definition': 'Gadgets are small mechanical or electronic devices designed for specific practical purposes, often featuring innovative or clever design. These tools are typically portable, useful, and sometimes incorporate new technology to solve everyday problems or provide entertainment. Gadgets range from simple mechanical tools to complex electronic devices, characterized by their ingenuity, compactness, and specialized function.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GAJ-its',
                'etymology': 'Origin uncertain, possibly from French "gâchette" (trigger, catch) or from nautical slang for a tool or device whose name is forgotten.',
                'language_origins': 'English (uncertain origin)',
                'example_sentence': 'The kitchen was filled with modern _______ that made cooking more efficient and enjoyable.',
                'memory_tip': 'Remember "GADGETS" - clever little devices that help you GET things done, useful tools and gizmos.'
            },
            'gaels': {
                'definition': 'Gaels refers to the Celtic people of Scotland, Ireland, and the Isle of Man, or more broadly, speakers of Goidelic languages including Scottish Gaelic, Irish Gaelic, and Manx. The term encompasses both the historical Celtic peoples who settled in these regions and their modern descendants. Gaels share cultural traditions, languages, and heritage rooted in ancient Celtic civilization.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'GAYLZ',
                'etymology': 'From Scottish Gaelic "Gàidheal" and Irish "Gael," ultimately from Old Irish "Goídel," meaning "Celt."',
                'language_origins': 'Scottish Gaelic, Irish',
                'example_sentence': 'The _______ maintained their distinct cultural traditions and language despite centuries of external influence.',
                'memory_tip': 'Remember "GAELS" - the Celtic people who speak GAELIC languages in Scotland and Ireland.'
            },
            'gaetana': {
                'definition': 'Gaetana appears to be an Italian feminine name or possibly refers to something or someone from Gaeta, a coastal city in Italy. In spelling bee contexts, this likely represents proper noun knowledge of Italian names or geographical references. The name has Italian origins and would follow Italian naming conventions and pronunciation patterns.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'gah-eh-TAH-nah',
                'etymology': 'Italian feminine name, possibly related to Gaeta, a city in Italy, or from Latin "Caietanus" (from Caieta/Gaeta).',
                'language_origins': 'Italian, Latin',
                'example_sentence': 'The character _______ in the Italian novel represented the strength of women from southern Italy.',
                'memory_tip': 'Remember "GAETANA" - an Italian feminine name, like someone named after the Italian city of Gaeta.'
            },
            'gaff': {
                'definition': 'A gaff is a pole with a hook used for landing large fish, or a spar extending from a mast to support the upper edge of a fore-and-aft sail. In slang, gaff can mean harsh treatment or criticism, or one\'s home or place. The word also refers to a steel spike worn by gamecocks in cockfighting. Each meaning involves something pointed or sharp used for a specific purpose.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'GAF',
                'etymology': 'From French "gaffe" meaning "boat hook," possibly from Provençal "gaf" (hook), ultimately from a Celtic source.',
                'language_origins': 'French, Celtic',
                'example_sentence': 'The fisherman used a _______ to safely bring the large salmon into the boat.',
                'memory_tip': 'Remember "GAFF" - a hook that GAFFs (grabs) fish, or gives someone a rough time (slang).'
            },
            'gaffe': {
                'definition': 'A gaffe is an unintentional act or remark causing embarrassment to its originator; a blunder or social mistake that reveals ignorance or insensitivity. Gaffes often occur in public settings and can damage reputations or relationships. The term suggests an error that is particularly awkward or inappropriate given the circumstances, often highlighting poor judgment or lack of awareness.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAF',
                'etymology': 'From French "gaffe" meaning "blunder," originally meaning "boat hook," extended to mean "social blunder" through the idea of "catching" or "hooking" onto mistakes.',
                'language_origins': 'French',
                'example_sentence': 'The politician\'s _______ during the interview became front-page news the next morning.',
                'memory_tip': 'Remember "GAFFE" - a social mistake that makes you want to GAG from embarrassment, a blundering error.'
            },
            'gaffer': {
                'definition': 'A gaffer is the chief electrician on a film or television production, responsible for lighting design and electrical equipment. In British usage, gaffer can mean an elderly man, boss, or foreman. The term also refers to the head of a work crew or someone in charge of a particular area of production. The word emphasizes leadership and technical expertise in specialized fields.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAF-er',
                'etymology': 'From "gaff" (hook) plus "-er," originally meaning "old man" (from "godfather"), later extended to mean "foreman" and then specialized for film lighting.',
                'language_origins': 'English',
                'example_sentence': 'The _______ worked closely with the director to create the perfect lighting for each scene.',
                'memory_tip': 'Remember "GAFFER" - the lighting chief who GAFFs (manages) all the electrical equipment on film sets.'
            },
            'gagaku': {
                'definition': 'Gagaku is a form of traditional Japanese court music that has been performed for over a thousand years, characterized by its slow, stately tempo and use of traditional Japanese instruments. This ancient musical art form includes both instrumental music and accompanying dance, representing one of the world\'s oldest continuous musical traditions. Gagaku is performed at Japanese imperial ceremonies and cultural events.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gah-GAH-koo',
                'etymology': 'From Japanese "雅楽" (gagaku), literally meaning "elegant music" or "graceful music," composed of "ga" (elegant) and "gaku" (music).',
                'language_origins': 'Japanese',
                'example_sentence': 'The imperial ceremony featured a performance of ancient _______ music with traditional court dancers.',
                'memory_tip': 'Remember "GAGAKU" - GAining GAins through ancient Japanese court music, elegant and graceful sounds.'
            },
            'gaggle': {
                'definition': 'A gaggle is a flock of geese, particularly when they are on the ground rather than flying (when they form a skein). The word also refers informally to any noisy, disorderly group of people, especially when they are chattering or moving together without much organization. The term emphasizes both the number of individuals and their tendency to make noise together.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'GAG-ul',
                'etymology': 'From Middle English "gagelen" meaning "to cackle," imitative of the sound geese make, related to the noise of geese gathering together.',
                'language_origins': 'Middle English (imitative)',
                'example_sentence': 'A _______ of tourists followed the guide through the museum, chattering excitedly about the exhibits.',
                'memory_tip': 'Remember "GAGGLE" - geese that GAG and babble together, making noise like they\'re GAGging on conversation.'
            },
            'gaia': {
                'definition': 'Gaia refers to the ancient Greek goddess of Earth, representing the planet as a living, nurturing mother. In modern contexts, Gaia often appears in the Gaia hypothesis, which views Earth as a self-regulating system where living and non-living components interact to maintain conditions suitable for life. The name symbolizes Earth\'s interconnected nature and the concept of the planet as a unified, living organism.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'GUY-ah or GAY-ah',
                'etymology': 'From Greek "Γαῖα" (Gaia), meaning "earth, land," the personification of Earth in Greek mythology.',
                'language_origins': 'Greek',
                'example_sentence': 'Environmental scientists often reference the _______ hypothesis when discussing Earth\'s self-regulating systems.',
                'memory_tip': 'Remember "GAIA" - the Earth goddess who GAvE us the planet, representing Earth as a living mother.'
            },
            'gaillardia': {
                'definition': 'Gaillardia is a genus of flowering plants in the sunflower family, commonly known as blanket flowers, native to North and South America. These hardy perennial flowers are characterized by their vibrant, daisy-like blooms in shades of red, orange, and yellow, often with contrasting centers. Gaillardia plants are popular in gardens for their drought tolerance, long blooming period, and ability to attract butterflies and other pollinators.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'gay-LAR-dee-ah',
                'etymology': 'Named after Antoine René Gaillard de Charentonneau (1720-1791), a French magistrate and botanist who was a patron of botany.',
                'language_origins': 'Modern Latin (named after French botanist)',
                'example_sentence': 'The drought-resistant _______ flowers bloomed brilliantly throughout the hot summer months.',
                'memory_tip': 'Remember "GAILLARDIA" - GAY, colorful flowers that are HARDY like a sturdy guard (Gaillard was a French name).'
            },
            'gajula': {
                'definition': 'Gajula appears to be a proper name of Indian origin, possibly Telugu or another South Indian language, where it may be a surname or place name. In spelling bee contexts, this represents knowledge of Indian names and linguistic diversity. The term would follow Telugu or related language pronunciation patterns and naming conventions.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'gah-JOO-lah',
                'etymology': 'Likely from Telugu or another South Indian language, possibly meaning related to "gaju" or similar roots in regional languages.',
                'language_origins': 'Telugu or South Indian languages',
                'example_sentence': 'The family name _______ traces its origins to the Telugu-speaking regions of southern India.',
                'memory_tip': 'Remember "GAJULA" - an Indian name that sounds like "GAH-ju-la," representing South Indian linguistic heritage.'
            }
        }
        
        return batch_073_data.get(word, {
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
            if word == 'furanmanu':
                errors.append(f"{word}: Combined word error: \"furanmanu\" appears to be \"furan\" + \"manu\" merged together. This is likely a PDF parsing error where chemical and other terms were incorrectly combined.")
            elif word == 'furnitureambush':
                errors.append(f"{word}: Combined word error: \"furnitureambush\" appears to be \"furniture\" + \"ambush\" merged together. This is likely a PDF parsing error where household and military terms were incorrectly combined.")
            elif word == 'gabbroplural':
                errors.append(f"{word}: Combined word error: \"gabbroplural\" appears to be \"gabbro\" + \"plural\" merged together. This is likely a PDF parsing error where geological and grammatical terms were incorrectly combined.")
            elif word == 'gabdifficulty':
                errors.append(f"{word}: Combined word error: \"gabdifficulty\" appears to be \"gab\" + \"difficulty\" merged together. This is likely a PDF parsing error where speech and complexity terms were incorrectly combined.")
                
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
        print("Batch 073 processing completed successfully!")

if __name__ == "__main__":
    processor = Batch073Processor()
    processor.process_batch(
        "output/batch_073_words.csv",
        "output/batch_073_processed.csv"
    )