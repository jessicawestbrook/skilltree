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
            "word": "calories",
            "definition": "Units of energy provided by food; units of heat energy",
            "pronunciation": "/ˈkæləriz/",
            "etymology": "From calorie + -s, where calorie comes from French calorie",
            "memory_tip": "CALORIES: Counting And - Lots of energy units, Obviously Responsible for energy, Including Essential nutrition, Everyone Studying nutrition",
            "example_sentence": "She counted the _____ in her meal to maintain a healthy diet.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calumet",
            "definition": "A ceremonial pipe used by Native Americans; a peace pipe",
            "pronunciation": "/ˈkæljəˌmɛt/",
            "etymology": "From French calumet, from Latin calamellus 'little reed'",
            "memory_tip": "CALUMET: Ceremonial And - Lovely traditional pipe, Understanding important ceremonies, Making Everyone Together in peace, Everyone Taking part in ceremonies",
            "example_sentence": "The chief passed the _____ as a symbol of peace and unity.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calumny",
            "definition": "False and defamatory statements; slander",
            "pronunciation": "/ˈkæləmni/",
            "etymology": "From Latin calumnia meaning 'false accusation'",
            "memory_tip": "CALUMNY: Concerning And - Lies targeting people, Usually Malicious statements, Never true accusations, Year-round harmful gossip",
            "example_sentence": "The politician sued the newspaper for publishing _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calusar",
            "definition": "A Romanian folk dance performed by men; a ritual healing dance",
            "pronunciation": "/kəˈlusər/",
            "etymology": "From Romanian căluşar, related to the ritual dancers",
            "memory_tip": "CALUSAR: Cultural And - Lovely traditional dance, Usually Sacred ritual dance, And Romanian cultural tradition",
            "example_sentence": "The _____ dancers performed the ancient healing ritual.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calvities",
            "definition": "Baldness; the condition of being bald",
            "pronunciation": "/kælˈvɪʃiz/",
            "etymology": "From Latin calvities meaning 'baldness', from calvus 'bald'",
            "memory_tip": "CALVITIES: Concerning And - Lacking hair condition, Very obvious hair loss, Including Thinning hair, Including Eventual hair loss, Something many people experience",
            "example_sentence": "His early _____ made him look older than his actual age.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calypso",
            "definition": "A type of West Indian music; a nymph in Greek mythology",
            "pronunciation": "/kəˈlɪpsoʊ/",
            "etymology": "From Greek Kalypso, name of a nymph in Homer's Odyssey",
            "memory_tip": "CALYPSO: Caribbean And - Lively musical style, Year-round Popular music, Something Outstanding musical tradition",
            "example_sentence": "The steel drum band played lively _____ music at the festival.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calzone",
            "definition": "An Italian turnover made with pizza dough and filled with cheese",
            "pronunciation": "/kælˈzoʊni/",
            "etymology": "From Italian calzone meaning 'trouser leg' or 'stocking'",
            "memory_tip": "CALZONE: Culinary And - Lightly stuffed Italian food, Zestful Italian cuisine, Obviously Notable Italian dish, Everyone enjoys Italian food",
            "example_sentence": "The _____ was stuffed with ricotta cheese and spinach.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "caló",
            "definition": "A Spanish dialect or slang; Romani language variety",
            "pronunciation": "/kəˈloʊ/",
            "etymology": "From Spanish caló, from Romani kalo meaning 'black'",
            "memory_tip": "CALÓ: Cultural And - Language variety, Obviously different dialect",
            "example_sentence": "The novel included passages written in _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "camarilla",
            "definition": "A small group of advisers to a ruler; a clique or faction",
            "pronunciation": "/ˌkæməˈrɪlə/",
            "etymology": "From Spanish camarilla, diminutive of cámara meaning 'chamber'",
            "memory_tip": "CAMARILLA: Conspiring And - Making secret decisions, And Really secret group, Including Lots of plotting, And secret political advisors",
            "example_sentence": "The king's _____ influenced his decisions behind closed doors.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "camarillanidicolous",
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
            "word": "cambio",
            "definition": "Spanish word for change or exchange; currency exchange",
            "pronunciation": "/ˈkæmbioʊ/",
            "etymology": "From Spanish cambio meaning 'change', from Latin cambium",
            "memory_tip": "CAMBIO: Currency And - Money exchange, Business International trade, Obviously for currency exchange",
            "example_sentence": "The _____ rate affected international business transactions.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cambric",
            "definition": "A fine white linen or cotton fabric",
            "pronunciation": "/ˈkeɪmbrɪk/",
            "etymology": "From Cambrai, a city in France where it was first made",
            "memory_tip": "CAMBRIC: Classic And - Mostly fine fabric, Beautiful Refined fabric, Including Cloth material",
            "example_sentence": "The handkerchief was made of delicate _____ cotton.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "camcorder",
            "definition": "A portable video camera with built-in recording capabilities",
            "pronunciation": "/ˈkæmˌkɔrdər/",
            "etymology": "From camera + recorder, a compound word describing its function",
            "memory_tip": "CAMCORDER: Camera And - Movies recording device, Capturing Outstanding video, Recording Definitely Everything, Really convenient device",
            "example_sentence": "She used her _____ to film the family reunion.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cameist",
            "definition": "One who engraves cameos; a cameo artist",
            "pronunciation": "/ˈkeɪmist/",
            "etymology": "From cameo + -ist, referring to one who works with cameos",
            "memory_tip": "CAMEIST: Craftsman And - Making artistic jewelry, Everyone Interested in detailed carving, Something artistic profession, Talented artist specialist",
            "example_sentence": "The skilled _____ carved intricate portraits in the precious stone.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "camel",
            "definition": "A large mammal with humps, adapted for desert life",
            "pronunciation": "/ˈkæməl/",
            "etymology": "From Latin camelus, from Greek kamelos",
            "memory_tip": "CAMEL: Careful And - Making desert journeys, Everyone Loves desert animals",
            "example_sentence": "The _____ carried supplies across the vast desert.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "camelot",
            "definition": "The legendary court of King Arthur; an idealized place",
            "pronunciation": "/ˈkæməˌlɑt/",
            "etymology": "From Old French Camalot, name of Arthur's legendary court",
            "memory_tip": "CAMELOT: Classic And - Mythical Arthurian place, Everyone Loves legendary stories, Obviously Timeless legendary kingdom",
            "example_sentence": "The musical _____ tells the story of King Arthur's court.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "camembert",
            "definition": "A soft French cheese with a white rind",
            "pronunciation": "/ˈkæməmˌbɛr/",
            "etymology": "Named after Camembert, a village in Normandy, France",
            "memory_tip": "CAMEMBERT: Creamy And - Mild French cheese, Everyone Meets French cuisine, Beautiful European cheese, Everyone Recognizes this cheese, Totally delicious cheese",
            "example_sentence": "The cheese board featured a ripe wheel of _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "camera",
            "definition": "A device for taking photographs or recording video",
            "pronunciation": "/ˈkæmərə/",
            "etymology": "From Latin camera meaning 'chamber' or 'room'",
            "memory_tip": "CAMERA: Capturing And - Making pictures perfectly, Everyone Records with cameras, Always taking photos",
            "example_sentence": "The photographer adjusted the _____ settings for the portrait.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "camouflaged",
            "definition": "Disguised or hidden by blending with surroundings",
            "pronunciation": "/ˈkæməˌflɑʒd/",
            "etymology": "From camouflage + -d, where camouflage comes from French camoufler 'to disguise'",
            "memory_tip": "CAMOUFLAGED: Carefully And - Making things hidden, Obviously Undetectable blending, Frequently Letting animals hide, And Getting Everyone concealed, Disguised perfectly",
            "example_sentence": "The soldiers were perfectly _____ in the dense forest.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "campaign",
            "definition": "An organized effort to achieve a goal; a military operation",
            "pronunciation": "/kæmˈpeɪn/",
            "etymology": "From French campagne meaning 'open country', from Latin campus 'field'",
            "memory_tip": "CAMPAIGN: Coordinated And - Making progress toward goals, Promoting And Important objectives, Getting Notable results",
            "example_sentence": "The political _____ focused on education reform.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "campanology",
            "definition": "The art or study of bell ringing",
            "pronunciation": "/ˌkæmpəˈnɑlədʒi/",
            "etymology": "From Latin campana 'bell' + Greek -logia 'study of'",
            "memory_tip": "CAMPANOLOGY: Classic And - Making beautiful bell music, Particularly About church bell ringing, And Notable bell music, Obviously Learning bell ringing, Obviously Great musical tradition, Year-round bell studies",
            "example_sentence": "The church tower was famous for its _____ traditions.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "campus",
            "definition": "The grounds of a university or college; an institutional area",
            "pronunciation": "/ˈkæmpəs/",
            "etymology": "From Latin campus meaning 'field' or 'open space'",
            "memory_tip": "CAMPUS: College And - Many students together, Providing University education, Usually Students everywhere",
            "example_sentence": "Students walked across the beautiful tree-lined _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "canada",
            "definition": "A country in North America; the second-largest country by area",
            "pronunciation": "/ˈkænədə/",
            "etymology": "From Huron-Iroquois kanata meaning 'village' or 'settlement'",
            "memory_tip": "CANADA: Cold And - Northern American country, And Diverse culture, Amazing natural beauty",
            "example_sentence": "The family planned a vacation to _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "canaille",
            "definition": "The rabble; the common people (often used disparagingly)",
            "pronunciation": "/kəˈnaɪ/",
            "etymology": "From French canaille meaning 'pack of dogs', from Italian canaglia",
            "memory_tip": "CANAILLE: Concerning And - Negative term for people, And Insulting term, Lots of social prejudice, Everyone dislikes this term",
            "example_sentence": "The aristocrat looked down upon the _____ with disdain.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "canaillecantatrice",
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
            "word": "canard",
            "definition": "A false or unfounded story; a deliberately misleading report",
            "pronunciation": "/kəˈnɑrd/",
            "etymology": "From French canard meaning 'duck', from the phrase 'vendre un canard à moitié' (to half-sell a duck)",
            "memory_tip": "CANARD: Concerning And - Not truthful story, And Really Deceptive information",
            "example_sentence": "The newspaper retracted the _____ about the celebrity scandal.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "canary",
            "definition": "A small yellow songbird; a bright yellow color",
            "pronunciation": "/kəˈnɛri/",
            "etymology": "From Spanish canario, from the Canary Islands",
            "memory_tip": "CANARY: Colorful And - Nice singing bird, And Really bright yellow color, Year-round beautiful singing",
            "example_sentence": "The pet _____ sang beautifully from its cage.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cancel",
            "definition": "To call off or annul; to mark for deletion",
            "pronunciation": "/ˈkænsəl/",
            "etymology": "From Latin cancellare meaning 'to make like a lattice', from cancelli 'bars'",
            "memory_tip": "CANCEL: Calling And - No longer continuing, Calling Everything off, Everyone Learns plans change",
            "example_sentence": "They had to _____ the outdoor concert due to rain.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cancion",
            "definition": "Spanish word for song; a musical composition",
            "pronunciation": "/kənˈsjoɪn/",
            "etymology": "From Spanish canción meaning 'song', from Latin cantio",
            "memory_tip": "CANCION: Classic And - Nice musical composition, Captivating Spanish song, Including Outstanding music, Never boring songs",
            "example_sentence": "The guitarist played a beautiful _____ about lost love.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "candelabrum",
            "definition": "A large branched candlestick or lamp holder",
            "pronunciation": "/ˌkændəˈlæbrəm/",
            "etymology": "From Latin candelabrum, from candela meaning 'candle'",
            "memory_tip": "CANDELABRUM: Ceremonial And - Nice decorative lighting, Definitely Elegant lighting device, Lovely And Beautiful ceremonial lighting, Really Unique ceremonial lighting, Usually Multiple candles",
            "example_sentence": "The ornate silver _____ graced the dining room table.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "candid",
            "definition": "Frank and honest; unposed or informal",
            "pronunciation": "/ˈkændɪd/",
            "etymology": "From Latin candidus meaning 'white, pure, sincere'",
            "memory_tip": "CANDID: Clear And - Never Deceptive words, Incredibly Direct communication",
            "example_sentence": "She appreciated his _____ feedback about her performance.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "candles",
            "definition": "Wax cylinders with wicks that burn to provide light",
            "pronunciation": "/ˈkændəlz/",
            "etymology": "From candle + -s, where candle comes from Latin candela",
            "memory_tip": "CANDLES: Ceremonial And - Nice light sources, Definitely Light sources, Everyone Sees romantic lighting, Something everyone uses for atmosphere",
            "example_sentence": "The birthday cake was decorated with colorful _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "canid",
            "definition": "A member of the dog family, including wolves, foxes, and domestic dogs",
            "pronunciation": "/ˈkeɪnɪd/",
            "etymology": "From Latin canis meaning 'dog' + -id suffix",
            "memory_tip": "CANID: Carnivorous And - Natural dog family, Including Dogs and relatives",
            "example_sentence": "The fox is a wild _____ that adapts well to urban environments.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cannoli",
            "definition": "Italian pastries filled with sweet ricotta cheese",
            "pronunciation": "/kəˈnoʊli/",
            "etymology": "From Italian cannoli, plural of cannolo meaning 'little tube'",
            "memory_tip": "CANNOLI: Classic And - Nice Italian dessert, Notable Outstanding dessert, Lovely Italian pastries",
            "example_sentence": "The bakery's _____ were filled with sweet ricotta and chocolate chips.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cannonade",
            "definition": "Continuous heavy gunfire; to attack with artillery",
            "pronunciation": "/ˌkænəˈneɪd/",
            "etymology": "From French canonnade, from canon meaning 'cannon'",
            "memory_tip": "CANNONADE: Continuous And - Never stopping artillery fire, Obviously Never ending bombardment, And Destructive military action, Everyone recognizes warfare",
            "example_sentence": "The fortress withstood the enemy's fierce _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "canny",
            "definition": "Having good judgment; shrewd and careful",
            "pronunciation": "/ˈkæni/",
            "etymology": "From Scottish canny meaning 'knowing, careful'",
            "memory_tip": "CANNY: Careful And - Never careless behavior, Never making mistakes, Year-round wise decisions",
            "example_sentence": "The _____ investor avoided the risky stock market bubble.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "canoe",
            "definition": "A narrow boat propelled by paddles",
            "pronunciation": "/kəˈnu/",
            "etymology": "From Spanish canoa, from Arawakan kanawa",
            "memory_tip": "CANOE: Classic And - Natural water transportation, Obviously Efficient water travel",
            "example_sentence": "They paddled the _____ across the peaceful lake.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cantankerous",
            "definition": "Bad-tempered and uncooperative; quarrelsome",
            "pronunciation": "/kænˈtæŋkərəs/",
            "etymology": "Possibly from Middle English contekour meaning 'troublemaker'",
            "memory_tip": "CANTANKEROUS: Concerning And - Never cooperative behavior, Totally And Never peaceful, Always Never kind, Everyone Really annoyed by behavior, Obviously Unpleasant behavior, Usually Stubborn attitude",
            "example_sentence": "The _____ old man complained about everything.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cantatrice",
            "definition": "A female opera singer; a prima donna",
            "pronunciation": "/ˌkæntəˈtris/",
            "etymology": "From Italian cantatrice, from cantare meaning 'to sing'",
            "memory_tip": "CANTATRICE: Classic And - Notable opera singer, Talented And Talented musical performer, Really Incredible classical singer, Exceptionally talented singer",
            "example_sentence": "The famous _____ received a standing ovation for her performance.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "canteen",
            "definition": "A water bottle; a workplace cafeteria; a military store",
            "pronunciation": "/kænˈtin/",
            "etymology": "From French cantine, from Italian cantina meaning 'cellar'",
            "memory_tip": "CANTEEN: Container And - Never without water container, Teaching Everyone to stay hydrated, Everyone Eating together, Never hungry workplace dining",
            "example_sentence": "The soldiers filled their _____ with fresh water.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "canterbury",
            "definition": "A cathedral city in England; a piece of furniture for holding music",
            "pronunciation": "/ˈkæntərˌbɛri/",
            "etymology": "From Canterbury, England, associated with the cathedral and archbishopric",
            "memory_tip": "CANTERBURY: Cathedral And - Notable religious place, Totally English historical city, Everyone Recognizes religious history, Beautiful historic University city, Really famous cathedral, Year-round pilgrimage destination",
            "example_sentence": "The pilgrims traveled to _____ in Chaucer's famous tales.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cantonese",
            "definition": "Relating to Canton (Guangzhou) or its dialect of Chinese",
            "pronunciation": "/ˌkæntəˈniz/",
            "etymology": "From Canton (Guangzhou) + -ese suffix meaning 'from' or 'relating to'",
            "memory_tip": "CANTONESE: Chinese And - Notable dialect, Traditional Outstanding language, Obviously Notable cultural heritage, Everyone Speaking in southern China, Something Everyone learns in Hong Kong",
            "example_sentence": "The restaurant served authentic _____ cuisine.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cantor",
            "definition": "A synagogue official who sings liturgical music; a church choir leader",
            "pronunciation": "/ˈkæntər/",
            "etymology": "From Latin cantor meaning 'singer', from cantare 'to sing'",
            "memory_tip": "CANTOR: Ceremonial And - Nice religious singing, Teaching Outstanding religious music, Obviously Religious musical leader",
            "example_sentence": "The _____ led the congregation in the beautiful Hebrew prayers.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "capable",
            "definition": "Having the ability or skill to do something; competent",
            "pronunciation": "/ˈkeɪpəbəl/",
            "etymology": "From Late Latin capabilis meaning 'able to hold', from capere 'to take'",
            "memory_tip": "CAPABLE: Completely And - Perfectly Able to accomplish things, Brilliantly Learning Everything",
            "example_sentence": "She proved to be _____ of handling the challenging project.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "capacity",
            "definition": "The maximum amount that can be contained; ability or capability",
            "pronunciation": "/kəˈpæsɪti/",
            "etymology": "From Latin capacitas meaning 'breadth, capacity', from capax 'spacious'",
            "memory_tip": "CAPACITY: Completely And - Perfectly Able to hold things, And Containing maximum amounts, Including Total available space, Year-round maximum potential",
            "example_sentence": "The stadium has a _____ of 50,000 spectators.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "caparisoned",
            "definition": "Decorated with ornamental coverings; adorned with rich clothing",
            "pronunciation": "/kəˈpærɪsənd/",
            "etymology": "From Spanish caparazón meaning 'saddle covering', from capa 'cloak'",
            "memory_tip": "CAPARISONED: Ceremonial And - Perfectly decorated appearance, And Really beautiful decoration, Including Splendid ornamental covering, Obviously Noble decorative attire, Everyone Decorates horses for ceremonies",
            "example_sentence": "The _____ horses paraded in the royal procession.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "capillary",
            "definition": "A very thin tube or blood vessel; relating to hair-like tubes",
            "pronunciation": "/ˈkæpəˌlɛri/",
            "etymology": "From Latin capillaris meaning 'of hair', from capillus 'hair'",
            "memory_tip": "CAPILLARY: Cardiovascular And - Perfectly thin blood vessels, Including Lots of tiny tubes, And Really tiny vessels, Year-round blood circulation",
            "example_sentence": "Blood flows through tiny _____ vessels to reach every cell.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "capillarycapnometer",
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
            "word": "capital",
            "definition": "The chief city of a country; wealth used for investment",
            "pronunciation": "/ˈkæpɪtəl/",
            "etymology": "From Latin capitalis meaning 'of the head', from caput 'head'",
            "memory_tip": "CAPITAL: Central And - Primary Important location, And Top priority, Leading city importance",
            "example_sentence": "Washington D.C. is the _____ of the United States.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "capitalist",
            "definition": "An advocate of capitalism; one who owns capital for investment",
            "pronunciation": "/ˈkæpɪtəlɪst/",
            "etymology": "From capital + -ist, referring to one who believes in or practices capitalism",
            "memory_tip": "CAPITALIST: Central And - Private ownership advocate, Investing Totally And carefully, And Lots of business ownership, Including Serious business, Totally business-focused person",
            "example_sentence": "The _____ invested in several technology startups.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        }
    ]
    
    # Write to CSV file
    output_file = "C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\spelling_bee\\output\\batch_028_processed.csv"
    
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
        
        print(f"Batch 028 processing complete!")
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