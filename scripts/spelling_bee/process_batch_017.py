#!/usr/bin/env python3

import csv
import os

class DifficultyCalculator:
    def calculate_difficulty(self, word, definition="", etymology=""):
        phonetic_score = self._calculate_phonetic_transparency(word)
        frequency_score = self._estimate_word_frequency(word)
        morphology_score = self._analyze_morphological_complexity(word, definition)
        etymology_score = self._analyze_etymological_complexity(etymology)
        
        raw_score = (phonetic_score + frequency_score + morphology_score + etymology_score) / 4
        
        if raw_score <= 2.0:
            return "Beginner"
        elif raw_score <= 3.5:
            return "Intermediate" 
        elif raw_score <= 4.5:
            return "Advanced"
        else:
            return "Expert"
    
    def _calculate_phonetic_transparency(self, word):
        irregularities = 0
        word = word.lower()
        
        silent_patterns = ['ght', 'mb', 'kn', 'wr', 'gn', 'mn', 'bt', 'st', 'tch']
        for pattern in silent_patterns:
            if pattern in word:
                irregularities += 1
        
        vowel_digraphs = ['ea', 'ee', 'oo', 'ou', 'ie', 'ai', 'ay', 'ey', 'oy', 'aw', 'au', 'ue']
        for digraph in vowel_digraphs:
            irregularities += word.count(digraph) * 0.5
        
        if any(c in word for c in 'qxz'):
            irregularities += 1
        
        if len(word) > 10:
            irregularities += (len(word) - 10) * 0.2
        
        return min(5.0, 1.0 + irregularities)
    
    def _estimate_word_frequency(self, word):
        common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our', 'had', 'day', 'get', 'use', 'man', 'new', 'now', 'way', 'may', 'say', 'each', 'which', 'their', 'time', 'will', 'about', 'there', 'been', 'many', 'some', 'what', 'would', 'make', 'like', 'into', 'him', 'has', 'two', 'more', 'very', 'after', 'words', 'first', 'where', 'much', 'through', 'work', 'good', 'woman', 'life', 'right', 'high', 'every', 'tell', 'should', 'follow', 'around', 'think', 'help', 'turn', 'found', 'number', 'system', 'still', 'learn', 'human', 'music', 'world', 'family', 'never', 'home', 'place', 'picture', 'try', 'back', 'hand', 'why', 'while', 'here', 'take', 'question', 'thought', 'school', 'important', 'children', 'example', 'begin', 'seem', 'together', 'got']
        
        if word.lower() in common_words[:50]:
            return 1.0
        elif word.lower() in common_words:
            return 2.0
        elif len(word) <= 5:
            return 2.5
        elif len(word) <= 8:
            return 3.0
        else:
            return 4.0
    
    def _analyze_morphological_complexity(self, word, definition):
        complexity = 1.0
        
        prefixes = ['un', 're', 'pre', 'dis', 'mis', 'over', 'under', 'out', 'up', 'sub', 'inter', 'fore', 'de', 'non', 'in', 'im', 'ir', 'il', 'anti', 'auto', 'co', 'ex', 'trans', 'super', 'semi', 'multi', 'bi', 'tri', 'uni', 'mono', 'poly', 'micro', 'macro', 'pseudo', 'neo', 'proto', 'meta', 'hyper', 'hypo', 'ultra', 'contra', 'counter', 'extra', 'intra', 'intro', 'retro', 'circum', 'peri', 'para', 'epi', 'endo', 'exo']
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'ion', 'tion', 'sion', 'ness', 'ment', 'ful', 'less', 'able', 'ible', 'ous', 'eous', 'ious', 'al', 'ial', 'ic', 'tic', 'ive', 'ative', 'itive', 'ory', 'ary', 'ery', 'y', 'ify', 'ize', 'ise', 'ate', 'ite', 'ure', 'age', 'dom', 'ship', 'hood', 'ward', 'wise', 'like', 'some', 'fold', 'teen', 'ty', 'th']
        
        word_lower = word.lower()
        
        for prefix in prefixes:
            if word_lower.startswith(prefix):
                complexity += 0.5
                break
        
        for suffix in suffixes:
            if word_lower.endswith(suffix):
                complexity += 0.3
                break
        
        if any(char in definition.lower() for char in ['technical', 'medical', 'scientific', 'legal', 'archaic', 'obsolete']):
            complexity += 1.0
        
        return min(5.0, complexity)
    
    def _analyze_etymological_complexity(self, etymology):
        if not etymology:
            return 3.0
        
        etymology_lower = etymology.lower()
        
        complex_origins = ['sanskrit', 'arabic', 'hebrew', 'chinese', 'japanese', 'nahuatl', 'quechua', 'persian', 'turkish', 'finnish', 'hungarian', 'basque', 'irish', 'welsh', 'scots gaelic']
        moderate_origins = ['old norse', 'old english', 'middle english', 'anglo-norman', 'old french', 'middle french', 'medieval latin', 'vulgar latin', 'proto-germanic', 'proto-indo-european']
        simple_origins = ['latin', 'greek', 'french', 'german', 'spanish', 'italian', 'portuguese', 'dutch', 'english']
        
        for origin in complex_origins:
            if origin in etymology_lower:
                return 5.0
        
        for origin in moderate_origins:
            if origin in etymology_lower:
                return 3.5
        
        for origin in simple_origins:
            if origin in etymology_lower:
                return 2.0
        
        multiple_origins = sum(1 for origin in simple_origins + moderate_origins + complex_origins if origin in etymology_lower)
        if multiple_origins > 1:
            return min(5.0, 2.0 + multiple_origins * 0.5)
        
        return 3.0

def process_words():
    calculator = DifficultyCalculator()
    
    words_data = [
        {
            "word": "bantamapprentice",
            "definition": "ERROR: Combined word - should be separate words",
            "pronunciation": "",
            "etymology": "",
            "memory_tip": "",
            "example_sentence": "",
            "etymology_source": "",
            "definition_source": "",
            "example_sentence_source": "",
            "audio_source": "",
            "combined_word_error": True
        },
        {
            "word": "bantlings",
            "definition": "Young children; infants or small creatures",
            "pronunciation": "/ˈbæntlɪŋz/",
            "etymology": "From Middle English bantling, possibly from German bänkling 'bastard', or from ban 'to curse' + -ling suffix",
            "memory_tip": "BANTLINGS: Babies And Newborns - Tiny Little Infants, Natural Growing offspring, Small children",
            "example_sentence": "The nursery was filled with the cheerful sounds of _____ at play.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "baptismal",
            "definition": "Relating to baptism, the Christian sacrament of initiation",
            "pronunciation": "/bæpˈtɪzməl/",
            "etymology": "From Latin baptisma meaning 'baptism', from Greek baptisma 'immersion', from baptein 'to dip, immerse'",
            "memory_tip": "BAPTISMAL: Blessed And Pure - The Important Spiritual Moment celebrating faith, Angels witness the ceremony, Life-changing sacrament",
            "example_sentence": "The family gathered around the _____ font for the baby's christening ceremony.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "barber",
            "definition": "A person who cuts and styles hair, especially men's hair",
            "pronunciation": "/ˈbɑrbər/",
            "etymology": "From Old French barbier, from Latin barba meaning 'beard'",
            "memory_tip": "BARBER: Beard And hair cutter - Really Better with razors, Everyone's hair specialist, Reliable professional",
            "example_sentence": "The skilled _____ gave him a precise haircut and traditional straight-razor shave.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "barbie",
            "definition": "Australian slang for barbecue; a popular doll brand name",
            "pronunciation": "/ˈbɑrbi/",
            "etymology": "Shortened form of barbecue, from Spanish barbacoa meaning 'framework of sticks'",
            "memory_tip": "BARBIE: Beautiful Australian - Really fun BBQ cooking, Informal Entertaining gatherings",
            "example_sentence": "The family hosted a weekend _____ in their backyard with grilled seafood.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bardolatry",
            "definition": "Excessive worship or admiration of William Shakespeare (the Bard)",
            "pronunciation": "/bɑrˈdɑlətri/",
            "etymology": "From bard (Shakespeare) + Greek latreia meaning 'worship', coined by George Bernard Shaw",
            "memory_tip": "BARDOLATRY: Bard Adoration - Obsessive Love And Total Reverence for Shakespeare, Amazing Talented writer Revered, Yes excessive devotion",
            "example_sentence": "The literary critic accused scholars of _____ instead of objective analysis of Shakespeare's works.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "barefoot",
            "definition": "With nothing on the feet; without shoes or socks",
            "pronunciation": "/ˈbɛrˌfʊt/",
            "etymology": "From Middle English bare + foot, referring to uncovered feet",
            "memory_tip": "BAREFOOT: Basic And - Really Easy, Feet touch ground naturally, Outdoor walking naturally",
            "example_sentence": "The children ran _____ through the soft grass in the summer meadow.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "barely",
            "definition": "Scarcely; only just; almost not",
            "pronunciation": "/ˈbɛrli/",
            "etymology": "From bare + -ly, meaning 'in a bare manner, just'",
            "memory_tip": "BARELY: Basic Amount - Really Everyone has Little of something, very minimal quantity, Yet somehow sufficient",
            "example_sentence": "She _____ had enough money to buy groceries for the week.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bargain",
            "definition": "An agreement between parties; something offered at a low price",
            "pronunciation": "/ˈbɑrɡɪn/",
            "etymology": "From Old French bargaignier meaning 'to haggle', possibly from Germanic origin",
            "memory_tip": "BARGAIN: Beautiful Agreement - Really Good deal And Investment, Nice purchase opportunity",
            "example_sentence": "The antique furniture was such a _____ that she bought the entire set.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bariatrics",
            "definition": "The medical specialty dealing with the treatment of obesity",
            "pronunciation": "/ˌbɛriˈætrɪks/",
            "etymology": "From Greek baros meaning 'weight' + iatros meaning 'physician' + -ics suffix",
            "memory_tip": "BARIATRICS: Body And - Really Important professional medical specialty, Addressing The weight Reduction, Intensive medical Care, Special surgical procedures",
            "example_sentence": "The hospital opened a new _____ center to help patients with weight-related health issues.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "barista",
            "definition": "A person who prepares and serves coffee drinks, especially espresso-based beverages",
            "pronunciation": "/bəˈristə/",
            "etymology": "From Italian barista meaning 'bartender', from bar + -ista suffix",
            "memory_tip": "BARISTA: Best And - Really Intelligent coffee Specialist, Talented Artist making drinks",
            "example_sentence": "The skilled _____ created beautiful latte art in the foam of my cappuccino.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "barked",
            "definition": "Past tense of bark; made a sharp sound like a dog; spoke harshly",
            "pronunciation": "/bɑrkt/",
            "etymology": "From Old English beorcan meaning 'to bark', of imitative origin",
            "memory_tip": "BARKED: Boisterous Animal - Really Keen on making noise, Everyone Definitely heard the sound",
            "example_sentence": "The sergeant _____ orders at the new recruits during morning drill.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "barnumesque",
            "definition": "Characterized by exaggerated showmanship and publicity, like P.T. Barnum",
            "pronunciation": "/ˌbɑrnəmˈɛsk/",
            "etymology": "From P.T. Barnum (famous circus showman) + -esque suffix meaning 'in the style of'",
            "memory_tip": "BARNUMESQUE: Big And - Really Noticeable, Utterly Magnificent spectacle, Entertainment Spectacular Quality, Upbeat circus-style Entertainment",
            "example_sentence": "The politician's _____ campaign rallies featured elaborate staging and dramatic speeches.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "barograph",
            "definition": "An instrument that records atmospheric pressure changes over time",
            "pronunciation": "/ˈbɛrəˌɡræf/",
            "etymology": "From Greek baros meaning 'weight, pressure' + graphein meaning 'to write'",
            "memory_tip": "BAROGRAPH: Barometric And - Recording pressure Observations, Graph Reveals weather patterns, Atmospheric Pressure History",
            "example_sentence": "The meteorologist consulted the _____ to track pressure changes before the storm.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "baronetcy",
            "definition": "The rank or dignity of a baronet; a hereditary title below a baron",
            "pronunciation": "/ˈbærənətsi/",
            "etymology": "From baronet (diminutive of baron) + -cy suffix indicating rank or status",
            "memory_tip": "BARONETCY: British Aristocratic - Really Old Noble title, Estate status, Typical heritage Class, high social status, Year-after-year inheritance",
            "example_sentence": "The family's _____ had been passed down through seven generations.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "baroque",
            "definition": "An elaborate artistic style of the 17th-18th centuries; highly ornate",
            "pronunciation": "/bəˈroʊk/",
            "etymology": "From French baroque, from Portuguese barroco meaning 'irregular pearl'",
            "memory_tip": "BAROQUE: Beautiful Art - Really Ornate, Quite elaborate decorative style, Unique period Extravagant artwork",
            "example_sentence": "The _____ cathedral featured intricate carvings and elaborate gold decorations.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "barracks",
            "definition": "Buildings used to house soldiers; military quarters",
            "pronunciation": "/ˈbærəks/",
            "etymology": "From French baraque meaning 'hut', from Italian baracca or Spanish barraca",
            "memory_tip": "BARRACKS: Basic Army - Really Austere military Residential housing, All Soldiers' Community space, lots of soldiers Kept in Same buildings",
            "example_sentence": "The new recruits were assigned to _____ near the training grounds.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "barrels",
            "definition": "Plural of barrel; cylindrical containers for storing liquids",
            "pronunciation": "/ˈbærəlz/",
            "etymology": "From Old French baril, possibly from Gaulish origin",
            "memory_tip": "BARRELS: Big And - Round, Reliable containers Excellent for Liquids, Large Storage vessels",
            "example_sentence": "The wine cellar contained hundreds of oak _____ aging vintages from different years.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "barren",
            "definition": "Incapable of producing vegetation; unproductive or sterile",
            "pronunciation": "/ˈbærən/",
            "etymology": "From Old French brahain meaning 'fallow', possibly from Celtic origin",
            "memory_tip": "BARREN: Bleak And - Really empty landscapes, Rough Environment, Nothing grows",
            "example_sentence": "The _____ desert stretched for miles without any signs of vegetation.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "barricade",
            "definition": "A temporary barrier erected to block or defend against attack",
            "pronunciation": "/ˌbærɪˈkeɪd/",
            "etymology": "From French barricade, from barrique 'barrel', originally barriers made of barrels",
            "memory_tip": "BARRICADE: Barrier And - Really Important defensive Construction, Against attack, Defense Everything",
            "example_sentence": "The protesters erected a _____ of overturned cars to block the street.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "barrier",
            "definition": "Something that blocks or prevents movement or access; an obstacle",
            "pronunciation": "/ˈbæriər/",
            "etymology": "From Old French barriere, from barre meaning 'bar, barrier'",
            "memory_tip": "BARRIER: Blocks And - Really Restricts movement, Impediments Everyone Recognizes",
            "example_sentence": "The language _____ made communication difficult between the two groups.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bartókian",
            "definition": "Relating to or characteristic of the musical style of composer Béla Bartók",
            "pronunciation": "/bɑrˈtoʊkiən/",
            "etymology": "From Béla Bartók (Hungarian composer) + -ian suffix meaning 'relating to'",
            "memory_tip": "BARTÓKIAN: Beautiful And - Revolutionary Hungarian composer's style, Tonal Order changes, Kaleidoscopic music, Innovative compositions, Advanced musical ideas, New techniques",
            "example_sentence": "The piece featured _____ rhythmic complexity and folk music influences.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "barylambda",
            "definition": "A type of subatomic particle in physics; a baryon containing a lambda particle",
            "pronunciation": "/ˌbæriˈlæmdə/",
            "etymology": "From Greek barys meaning 'heavy' + lambda (Greek letter used in particle physics nomenclature)",
            "memory_tip": "BARYLAMBDA: Big And - Really heavy particle physics, Yet scientific Lambda - Advanced Matter, Basic Diverse Atoms",
            "example_sentence": "The particle accelerator detected evidence of _____ formation during the collision experiment.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "basaltic",
            "definition": "Relating to basalt, a dark volcanic rock",
            "pronunciation": "/bəˈsɔltɪk/",
            "etymology": "From basalt (from Latin basaltes, variant of basanites 'touchstone') + -ic suffix",
            "memory_tip": "BASALTIC: Black And - Stone rock, Always Lava-formed, Tough Igneous stone, Characteristic volcanic material",
            "example_sentence": "The island's _____ cliffs were formed by ancient volcanic eruptions.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "baseball",
            "definition": "A bat-and-ball sport played between two teams of nine players",
            "pronunciation": "/ˈbeɪsˌbɔl/",
            "etymology": "From base + ball, referring to the bases players run between",
            "memory_tip": "BASEBALL: Bats And - Sports players run Between All four bases, Everyone Loves this sport, Legendary American sport",
            "example_sentence": "The _____ game went into extra innings before the home team won.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "based",
            "definition": "Having a foundation or origin in something; located or situated",
            "pronunciation": "/beɪst/",
            "etymology": "From base + -ed, where base comes from Greek basis meaning 'foundation'",
            "memory_tip": "BASED: Built And - Solid foundation, Everyone Depends on this foundation",
            "example_sentence": "The company's success was _____ on innovative technology and excellent customer service.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "basement",
            "definition": "The lowest floor of a building, typically below ground level",
            "pronunciation": "/ˈbeɪsmənt/",
            "etymology": "From base + -ment suffix, referring to the base or foundation level of a building",
            "memory_tip": "BASEMENT: Below And - Situated underground level, Everyone Makes storage space, Every building's Nether floor, Totally underground",
            "example_sentence": "They converted the _____ into a comfortable family recreation room.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "basenji",
            "definition": "A breed of hunting dog from Central Africa that doesn't bark",
            "pronunciation": "/bəˈsɛndʒi/",
            "etymology": "From Lingala basenji meaning 'natives' or 'wild thing'",
            "memory_tip": "BASENJI: Beautiful African - Silent dog breed, Everyone Notes they don't bark, Just quiet Intelligence",
            "example_sentence": "The _____ is known as the 'barkless dog' due to its unique vocalization.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "basically",
            "definition": "In the most essential respects; fundamentally",
            "pronunciation": "/ˈbeɪsɪkli/",
            "etymology": "From basic + -ally, where basic comes from Greek basis meaning 'foundation'",
            "memory_tip": "BASICALLY: Bottom And - Simple foundation, In Core, And Logical core meaning, Like fundamental Yielding the core idea",
            "example_sentence": "The plan is _____ sound, but we need to work out some minor details.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "basilica",
            "definition": "A large oblong hall or building with double colonnades and a semicircular apse",
            "pronunciation": "/bəˈzɪlɪkə/",
            "etymology": "From Latin basilica, from Greek basilike meaning 'royal hall', from basileus 'king'",
            "memory_tip": "BASILICA: Beautiful And - Sacred church architecture, Including Large Imperial royal design, Important Church Architecture",
            "example_sentence": "The ancient Roman _____ was later converted into a Christian church.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "basilisk",
            "definition": "A legendary serpent whose gaze or breath was fatal; a type of lizard",
            "pronunciation": "/ˈbæzəlɪsk/",
            "etymology": "From Latin basiliscus, from Greek basiliskos meaning 'little king', diminutive of basileus 'king'",
            "memory_tip": "BASILISK: Bad And - Sinister creature, Intense Lethal serpent, Instantly deadlye gaze, Seriously Killer legendary animal",
            "example_sentence": "In the legend, the _____ could kill with a single glance from its deadly eyes.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "basis",
            "definition": "The underlying support or foundation for an idea or argument",
            "pronunciation": "/ˈbeɪsɪs/",
            "etymology": "From Greek basis meaning 'stepping, foundation', from bainein 'to step'",
            "memory_tip": "BASIS: Bottom And - Strong foundation, Important Starting point of everything, Starting foundation",
            "example_sentence": "The research provided a solid _____ for their groundbreaking conclusions.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bask",
            "definition": "To lie exposed to warmth and light; to revel in something pleasant",
            "pronunciation": "/bæsk/",
            "etymology": "From Old Norse baðask meaning 'to bathe oneself'",
            "memory_tip": "BASK: Beach And - Sun warmth, Kinda relaxing on sunny days",
            "example_sentence": "The cat loved to _____ in the warm sunlight streaming through the window.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "basketsbonnet",
            "definition": "ERROR: Combined word - should be separate words",
            "pronunciation": "",
            "etymology": "",
            "memory_tip": "",
            "example_sentence": "",
            "etymology_source": "",
            "definition_source": "",
            "example_sentence_source": "",
            "audio_source": "",
            "combined_word_error": True
        },
        {
            "word": "bassoon",
            "definition": "A large double-reed woodwind instrument with a deep tone",
            "pronunciation": "/bəˈsun/",
            "etymology": "From French basson, augmentative of basse meaning 'bass'",
            "memory_tip": "BASSOON: Big And - Serious low-pitched musical instrument, Sweet Orchestral sounds, Outstanding Notation",
            "example_sentence": "The _____ provided the deep, resonant bass line in the orchestral piece.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bastion",
            "definition": "A stronghold or fortified position; something that protects or preserves",
            "pronunciation": "/ˈbæstiən/",
            "etymology": "From French bastion, from Italian bastione, from bastire 'to build'",
            "memory_tip": "BASTION: Built And - Strong fortress, Totally Impenetrable defensive structure, Outstanding fort, Notably secure position",
            "example_sentence": "The university remained a _____ of academic freedom during turbulent times.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "batamote",
            "definition": "A thorny shrub found in Mexico and the southwestern United States",
            "pronunciation": "/ˌbætəˈmoʊti/",
            "etymology": "From Mexican Spanish batamote, possibly from indigenous origin",
            "memory_tip": "BATAMOTE: Barbed And - Thorny mexican shrub, Amazing desert plant, Making Obstacles for walking, Tough Environment plant",
            "example_sentence": "The desert landscape was dotted with _____ bushes and prickly pear cacti.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bathos",
            "definition": "An unintentional lapse in mood from the sublime to the trivial",
            "pronunciation": "/ˈbeɪθɑs/",
            "etymology": "From Greek bathos meaning 'depth', coined by Alexander Pope in contrast to 'pathos'",
            "memory_tip": "BATHOS: Bad And - Terrible drop from elegant High level to low Ordinary banality, Silly drop in quality",
            "example_sentence": "The poem's _____ ruined the emotional impact by shifting from tragedy to comedy.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bathtub",
            "definition": "A large container for holding water for bathing",
            "pronunciation": "/ˈbæθˌtʌb/",
            "etymology": "From bath + tub, where bath comes from Old English baeth",
            "memory_tip": "BATHTUB: Bath And - Tub for washing body, Hot water relaxation, Totally comfortable, Unique Bathroom vessel",
            "example_sentence": "She filled the _____ with warm water and lavender bath salts.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "batson",
            "definition": "A nautical term for a thin strip of wood used in shipbuilding",
            "pronunciation": "/ˈbætsən/",
            "etymology": "From Old French baston meaning 'stick, staff', related to baton",
            "memory_tip": "BATSON: Boat And - Thin wood Strip used in ship construction, Organizing Nautical construction",
            "example_sentence": "The shipbuilder used _____ to reinforce the hull's framework.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "battalion",
            "definition": "A large military unit, typically consisting of several companies",
            "pronunciation": "/bəˈtæliən/",
            "etymology": "From French bataillon, from Italian battaglione, from battaglia 'battle'",
            "memory_tip": "BATTALION: Battle And - Team Together, Armies Leading fighting unit, Including Officers and soldiers, Organized large formation, New military formation",
            "example_sentence": "The _____ advanced across the battlefield in coordinated formation.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "batten",
            "definition": "A strip of wood or metal used to secure or reinforce something",
            "pronunciation": "/ˈbætən/",
            "etymology": "From Old French baton meaning 'stick', related to baton",
            "memory_tip": "BATTEN: Board And - Thin strip for reinforcement, Together Everything Needs fastening",
            "example_sentence": "The sailors had to _____ down the hatches before the storm arrived.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "batteries",
            "definition": "Plural of battery; devices that store electrical energy; military units of artillery",
            "pronunciation": "/ˈbætəriz/",
            "etymology": "From French batterie, from battre 'to beat', originally referring to artillery units",
            "memory_tip": "BATTERIES: Basic And - Technology power storage, Energy Requires these devices, Electricity Storage",
            "example_sentence": "The flashlight stopped working when the _____ ran out of power.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "battue",
            "definition": "A type of hunt where game is driven toward hunters by beaters",
            "pronunciation": "/bæˈtu/",
            "etymology": "From French battue, from battre 'to beat', referring to beating bushes to drive game",
            "memory_tip": "BATTUE: Beaters And - Teams Together driving game toward hunters, Unique European hunting method",
            "example_sentence": "The aristocrats organized a _____ to hunt pheasants on their estate.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bauble",
            "definition": "A showy ornament or trinket of little value; a jester's stick",
            "pronunciation": "/ˈbɔbəl/",
            "etymology": "From Old French baubel, possibly from reduplication of bel 'beautiful'",
            "memory_tip": "BAUBLE: Bright And - Useless trinkets, Beautiful looking Empty decorations",
            "example_sentence": "The Christmas tree was decorated with colorful _____ and twinkling lights.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "baucis",
            "definition": "In Greek mythology, an elderly woman who showed hospitality to Zeus and Hermes",
            "pronunciation": "/ˈbɔsɪs/",
            "etymology": "From Greek Baukis, the name of the mythological character",
            "memory_tip": "BAUCIS: Beautiful And - Understanding kind woman, Classic mythology story, Incredible hospitality, Sacred kindness to gods",
            "example_sentence": "The story of _____ and Philemon teaches the importance of hospitality to strangers.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bauhaus",
            "definition": "A German art school and design movement emphasizing functional simplicity",
            "pronunciation": "/ˈbaʊˌhaʊs/",
            "etymology": "From German Bauhaus, from bau 'building' + haus 'house'",
            "memory_tip": "BAUHAUS: Building And - Understanding simple design, Harmonious Architecture style, Architectural school, Useful design, Simple aesthetics",
            "example_sentence": "The _____ movement revolutionized modern architecture with its clean, functional designs.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bauxite",
            "definition": "The principal ore of aluminum, a clay-like mineral",
            "pronunciation": "/ˈbɔksaɪt/",
            "etymology": "From French bauxite, named after Les Baux, France, where it was first discovered",
            "memory_tip": "BAUXITE: Basic Aluminum - Underground resource, eXtracted for manufacturing, Important Tough mineral, Essential metal ore",
            "example_sentence": "The mining company extracted _____ to produce aluminum for the automotive industry.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bavardage",
            "definition": "Idle chatter or gossip; trivial conversation",
            "pronunciation": "/ˌbævərˈdɑʒ/",
            "etymology": "From French bavardage, from bavarder 'to chatter', from bavard 'talkative'",
            "memory_tip": "BAVARDAGE: Babbling And - Verbose chatter, Annoying Random Discussion, All Gossip Endless talk",
            "example_sentence": "The dinner party was filled with pleasant _____ among old friends.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bavarese",
            "definition": "A type of molded dessert made with custard, gelatin, and whipped cream",
            "pronunciation": "/ˌbævəˈreɪzi/",
            "etymology": "From French bavarois meaning 'Bavarian', referring to its supposed Bavarian origin",
            "memory_tip": "BAVARESE: Beautiful And - Velvet dessert, Amazing Rich custard, Elegant Smooth dessert, Everyone loves this cream treat",
            "example_sentence": "The chef prepared a delicate chocolate _____ for the elegant dinner party.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        }
    ]
    
    # Write to CSV file
    output_file = "C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\spelling_bee\\output\\batch_017_processed.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'word', 'definition', 'pronunciation', 'etymology', 'memory_tip',
            'example_sentence', 'etymology_source', 'definition_source', 
            'example_sentence_source', 'audio_source', 'difficulty_level',
            'phonetic_score', 'frequency_score', 'morphology_score', 
            'etymology_score', 'combined_word_error'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        combined_errors = 0
        processed_count = 0
        
        for word_data in words_data:
            if word_data['combined_word_error']:
                combined_errors += 1
                difficulty_level = "N/A"
                phonetic_score = 0.0
                frequency_score = 0.0
                morphology_score = 0.0
                etymology_score = 0.0
            else:
                difficulty_level = calculator.calculate_difficulty(
                    word_data['word'], 
                    word_data['definition'], 
                    word_data['etymology']
                )
                phonetic_score = calculator._calculate_phonetic_transparency(word_data['word'])
                frequency_score = calculator._estimate_word_frequency(word_data['word'])
                morphology_score = calculator._analyze_morphological_complexity(word_data['word'], word_data['definition'])
                etymology_score = calculator._analyze_etymological_complexity(word_data['etymology'])
            
            row = {
                'word': word_data['word'],
                'definition': word_data['definition'],
                'pronunciation': word_data['pronunciation'],
                'etymology': word_data['etymology'],
                'memory_tip': word_data['memory_tip'],
                'example_sentence': word_data['example_sentence'],
                'etymology_source': word_data['etymology_source'],
                'definition_source': word_data['definition_source'],
                'example_sentence_source': word_data['example_sentence_source'],
                'audio_source': word_data['audio_source'],
                'difficulty_level': difficulty_level,
                'phonetic_score': round(phonetic_score, 2),
                'frequency_score': round(frequency_score, 2),
                'morphology_score': round(morphology_score, 2),
                'etymology_score': round(etymology_score, 2),
                'combined_word_error': word_data['combined_word_error']
            }
            
            writer.writerow(row)
            processed_count += 1
        
        print(f"Batch 017 processing complete!")
        print(f"Processed: {processed_count}/50 words")
        print(f"Combined word errors flagged: {combined_errors}")
        print(f"Valid spelling words: {processed_count - combined_errors}")
        
        if combined_errors > 0:
            print(f"\nCombined word errors found:")
            for word_data in words_data:
                if word_data['combined_word_error']:
                    print(f"  - {word_data['word']}")

if __name__ == "__main__":
    process_words()