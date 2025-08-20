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
            "word": "brands",
            "definition": "Particular makes of products; marks made with hot iron",
            "pronunciation": "/brændz/",
            "etymology": "From brand + -s, where brand comes from Old English brand meaning 'fire'",
            "memory_tip": "BRANDS: Basic Recognition - Always Notable company marks, Distinguishing products, Something everyone recognizes",
            "example_sentence": "The store carried several popular _____ of athletic shoes.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brandywine",
            "definition": "A variety of grape; a type of brandy; a creek name",
            "pronunciation": "/ˈbrændiˌwaɪn/",
            "etymology": "From brandy + wine, referring to a distilled wine product",
            "memory_tip": "BRANDYWINE: Beautiful Rich - And smooth alcohol, Never basic drink, Distilled from grapes, Year-long aging process, Wine processed Into stronger drink, Never watered down, Everyone knows this spirit",
            "example_sentence": "The _____ grapes produced an excellent vintage that year.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brass",
            "definition": "An alloy of copper and zinc; bold confidence",
            "pronunciation": "/bræs/",
            "etymology": "From Old English bræs, from Proto-Germanic brasom",
            "memory_tip": "BRASS: Basic Really - Alloy metal, Strong and durable, Something everyone knows",
            "example_sentence": "The musician polished his _____ trumpet before the concert.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bravado",
            "definition": "A bold manner intended to impress; swaggering display of courage",
            "pronunciation": "/brəˈvɑdoʊ/",
            "etymology": "From Spanish bravada, from bravo meaning 'brave' or 'wild'",
            "memory_tip": "BRAVADO: Bold Really - Always showing off courage, Very obvious Acting, Displaying false confidence, Obviously showing off",
            "example_sentence": "His _____ masked his deep insecurity about the upcoming challenge.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brave",
            "definition": "Ready to face danger; showing courage",
            "pronunciation": "/breɪv/",
            "etymology": "From French brave, from Italian bravo meaning 'wild, savage'",
            "memory_tip": "BRAVE: Bold Really - Always Very courageous, Everyone admires courage",
            "example_sentence": "The _____ firefighter rescued the family from the burning building.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brayed",
            "definition": "Made the loud harsh cry of a donkey; spoke loudly and harshly",
            "pronunciation": "/breɪd/",
            "etymology": "From bray + -ed, where bray comes from Old French braier meaning 'to cry'",
            "memory_tip": "BRAYED: Bold Really - Annoying donkey sound, Year-long memory of harsh sound, Everyone knows donkey sound, Definitely loud noise",
            "example_sentence": "The donkey _____ loudly as the farmer approached with hay.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bread",
            "definition": "A baked food made from flour and water; basic sustenance",
            "pronunciation": "/brɛd/",
            "etymology": "From Old English bread meaning 'morsel, bit of food'",
            "memory_tip": "BREAD: Basic Really - Essential food, Always Delicious staple",
            "example_sentence": "She baked fresh _____ for the family dinner.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "breadmaking",
            "definition": "The process of baking bread; the art of bread production",
            "pronunciation": "/ˈbrɛdˌmeɪkɪŋ/",
            "etymology": "From bread + making, referring to the process of creating bread",
            "memory_tip": "BREADMAKING: Basic Really - Essential food cooking, Always Delicious Making food, And Kitchen activity, Including flour, Never Getting tired of fresh bread",
            "example_sentence": "Her _____ skills improved with years of practice in the kitchen.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "breathe",
            "definition": "To take air into the lungs and expel it; to live",
            "pronunciation": "/brið/",
            "etymology": "From Old English brēathen, from brǣth meaning 'breath'",
            "memory_tip": "BREATHE: Basic Really - Essential function, Always Taking air, Having life, Everyone needs oxygen",
            "example_sentence": "Take a moment to _____ deeply and relax your mind.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "breathtaking",
            "definition": "Extremely impressive or beautiful; astonishing",
            "pronunciation": "/ˈbrɛθˌteɪkɪŋ/",
            "etymology": "From breath + taking, literally meaning 'taking one's breath away'",
            "memory_tip": "BREATHTAKING: Beautiful Really - Everyone stunned And speechless, Taking everyone's breath away, Having Amazing visual impact, Taking people's breath away, Awe-inspiring, Keeping everyone amazed, Including stunning views, Never Getting old, Great beauty",
            "example_sentence": "The _____ view from the mountain summit left everyone speechless.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bred",
            "definition": "Raised or produced offspring; brought up in a particular way",
            "pronunciation": "/brɛd/",
            "etymology": "From breed, past tense, from Old English brēdan meaning 'to bring up'",
            "memory_tip": "BRED: Basic Really - Everyone reproduces, Developing offspring naturally",
            "example_sentence": "The horses were carefully _____ for speed and endurance.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "breed",
            "definition": "To produce offspring; a particular variety of animal",
            "pronunciation": "/brid/",
            "etymology": "From Old English brēdan meaning 'to bring up' or 'to cherish'",
            "memory_tip": "BREED: Basic Really - Everyone reproduces, Everyone Develops offspring",
            "example_sentence": "What _____ of dog is best for families with young children?",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "breeds",
            "definition": "Produces offspring; varieties of animals or plants",
            "pronunciation": "/bridz/",
            "etymology": "From breed + -s, where breed comes from Old English brēdan",
            "memory_tip": "BREEDS: Basic Really - Everyone reproduces, Everyone Develops offspring, Something animals do",
            "example_sentence": "The kennel specialized in several different _____ of hunting dogs.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brethren",
            "definition": "Brothers; fellow members of a group or organization",
            "pronunciation": "/ˈbrɛθrən/",
            "etymology": "From Old English brēthren, plural of brother",
            "memory_tip": "BRETHREN: Basic Religious - Everyone Together as brothers, Having Religious fellowship, Really close Evangelical community, Never excluding anyone",
            "example_sentence": "The _____ gathered for their weekly prayer meeting.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brevet",
            "definition": "A commission promoting a military officer without increase in pay",
            "pronunciation": "/brəˈvɛt/",
            "etymology": "From French brevet meaning 'brief' or 'short document'",
            "memory_tip": "BREVET: Basic Rank - Everyone gets promoted, Very honorable promotion, Everyone Together recognizing achievement",
            "example_sentence": "The colonel received a _____ promotion to general for his distinguished service.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "breviloquence",
            "definition": "The practice of speaking briefly and concisely",
            "pronunciation": "/ˌbrɛvɪˈloʊkwəns/",
            "etymology": "From Latin brevis 'short' + loquentia 'speaking'",
            "memory_tip": "BREVILOQUENCE: Basic Really - Everyone speaking briefly, Very Intelligent speaking style, Literally Outstanding concise speech, Outstanding Quality speaking, Using Economical words, Never Complicated Explanations",
            "example_sentence": "The professor was known for his _____, making complex topics clear in few words.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "breviloquencenoun",
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
            "word": "bribery",
            "definition": "The giving or offering of a bribe; corruption through payment",
            "pronunciation": "/ˈbraɪbəri/",
            "etymology": "From bribe + -ery, where bribe comes from Old French briber 'to beg'",
            "memory_tip": "BRIBERY: Bad Really - Illegal activity, Buying illegal favors, Everyone Recognizes corruption, Year-long consequences",
            "example_sentence": "The politician was convicted of _____ and sentenced to prison.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bric",
            "definition": "Miscellaneous small objects; knickknacks (part of bric-a-brac)",
            "pronunciation": "/brɪk/",
            "etymology": "From French bric-à-brac, possibly from à bric et à broc 'by hook or by crook'",
            "memory_tip": "BRIC: Basic Random - Items Collected everywhere",
            "example_sentence": "The antique shop was filled with curious _____-a-brac from various eras.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brick",
            "definition": "A block of fired clay used in building; a reliable person",
            "pronunciation": "/brɪk/",
            "etymology": "From Middle Dutch bricke, possibly from broken pieces of stone",
            "memory_tip": "BRICK: Basic Really - Important Construction material, Keeping buildings strong",
            "example_sentence": "The mason carefully laid each _____ to build the garden wall.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bride",
            "definition": "A woman about to be married or recently married",
            "pronunciation": "/braɪd/",
            "etymology": "From Old English brȳd, from Proto-Germanic brūdiz",
            "memory_tip": "BRIDE: Beautiful Really - Important ceremony participant, Dressed Elegantly for wedding",
            "example_sentence": "The _____ looked radiant in her grandmother's vintage wedding dress.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bridge",
            "definition": "A structure carrying a road over an obstacle; to connect",
            "pronunciation": "/brɪdʒ/",
            "etymology": "From Old English brycg, from Proto-Germanic brugjō",
            "memory_tip": "BRIDGE: Basic Really - Important connecting structure, Driving over water, Getting Everyone across safely",
            "example_sentence": "The old stone _____ had spanned the river for over two centuries.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "briefcase",
            "definition": "A flat rectangular container for carrying documents",
            "pronunciation": "/ˈbrifˌkeɪs/",
            "etymology": "From brief (documents) + case (container)",
            "memory_tip": "BRIEFCASE: Business Really - Important Equipment for carrying documents, For work Carrying important documents, And Storing Everything, Everyone knows business accessory",
            "example_sentence": "She packed her important documents in the leather _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brigadoon",
            "definition": "A mythical village that appears once every hundred years",
            "pronunciation": "/ˌbrɪɡəˈdun/",
            "etymology": "From the 1947 musical 'Brigadoon' by Lerner and Loewe",
            "memory_tip": "BRIGADOON: Beautiful Really - Imaginary Scottish village, Going Away mysteriously, And Disappearing for years, Definitely Outstanding mythology, Outstanding Opera story, Never actually exists",
            "example_sentence": "The remote village seemed like a _____, appearing and disappearing from memory.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brigand",
            "definition": "A bandit or outlaw who lives by robbery",
            "pronunciation": "/ˈbrɪɡənd/",
            "etymology": "From Old French brigand, from briguer meaning 'to fight'",
            "memory_tip": "BRIGAND: Bad Really - Illegal thief, Generally Always taking things, And Never legal behavior, Definitely criminal activity",
            "example_sentence": "The mountain pass was known to be dangerous due to _____s who robbed travelers.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bright",
            "definition": "Giving out much light; intelligent; cheerful",
            "pronunciation": "/braɪt/",
            "etymology": "From Old English beorht meaning 'shining, brilliant'",
            "memory_tip": "BRIGHT: Beautiful Really - Intelligent and smart, Great light source, Having good intelligence, Totally illuminated",
            "example_sentence": "The _____ student quickly understood the complex mathematical concept.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brilliant",
            "definition": "Very bright; exceptionally clever or talented",
            "pronunciation": "/ˈbrɪljənt/",
            "etymology": "From French brillant, from briller meaning 'to shine'",
            "memory_tip": "BRILLIANT: Beautiful Really - Incredibly smart, Literally Outstanding intelligence, Intellectual Amazing excellence, And Never Typical intelligence",
            "example_sentence": "Her _____ solution to the problem impressed everyone in the meeting.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brim",
            "definition": "The edge or rim of something; to be full to the point of overflowing",
            "pronunciation": "/brɪm/",
            "etymology": "From Middle English brimme, possibly from Old Norse barmr 'edge'",
            "memory_tip": "BRIM: Basic Really - Important edge, Making containers full to the top",
            "example_sentence": "His eyes filled to the _____ with tears of joy.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brimless",
            "definition": "Without a brim or edge; lacking a projecting rim",
            "pronunciation": "/ˈbrɪmləs/",
            "etymology": "From brim + -less, meaning 'without a brim'",
            "memory_tip": "BRIMLESS: Basic Really - Important hat style, Missing the edge, Lacking typical hat features, Everyone knows this style, Some hats have no edge, Something different design",
            "example_sentence": "The _____ cap fit snugly on his head during the swim.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bring",
            "definition": "To carry or take something to a place; to cause something to happen",
            "pronunciation": "/brɪŋ/",
            "etymology": "From Old English bringan, from Proto-Germanic brenganą",
            "memory_tip": "BRING: Basic Really - Important action, Never Going empty-handed",
            "example_sentence": "Please _____ your passport when you come to the appointment.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bringing",
            "definition": "The act of carrying or taking something to a place",
            "pronunciation": "/ˈbrɪŋɪŋ/",
            "etymology": "From bring + -ing, where bring comes from Old English bringan",
            "memory_tip": "BRINGING: Basic Really - Important action, Never Going empty-handed, Going somewhere with items, Including taking something, Never Going without items, Getting things to destination",
            "example_sentence": "She is _____ fresh flowers to brighten up the office.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "briny",
            "definition": "Of or containing salt; relating to the sea",
            "pronunciation": "/ˈbraɪni/",
            "etymology": "From brine + -y, where brine comes from Old English brȳne",
            "memory_tip": "BRINY: Basic Really - Including salt water, Never fresh water, Year-round ocean taste",
            "example_sentence": "The _____ ocean spray left salt crystals on their faces.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "briocheadumbrate",
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
            "word": "bristle",
            "definition": "A short stiff hair; to show anger or become defensive",
            "pronunciation": "/ˈbrɪsəl/",
            "etymology": "From Old English bristl, from byrst meaning 'bristle'",
            "memory_tip": "BRISTLE: Basic Really - Individual Stiff hair, Something animals have, Tough Little spiky hair, Everyone knows pig hairs",
            "example_sentence": "The dog's fur began to _____ when it sensed danger nearby.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "british",
            "definition": "Of or relating to Great Britain or its people",
            "pronunciation": "/ˈbrɪtɪʃ/",
            "etymology": "From Britain + -ish, where Britain comes from Old English Brettas 'the Britons'",
            "memory_tip": "BRITISH: Basic Really - Important country, Totally Island nation, Including Scotland and Wales, Something European, Having royal family",
            "example_sentence": "The _____ accent was easily recognizable in the international conference.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "broad",
            "definition": "Wide; covering a large area; general rather than specific",
            "pronunciation": "/brɔd/",
            "etymology": "From Old English brād meaning 'wide, spacious'",
            "memory_tip": "BROAD: Basic Really - Obviously wide, And spacious, Definitely not narrow",
            "example_sentence": "The highway took a _____ sweep around the mountain.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "broadcast",
            "definition": "To transmit radio or television programs; to spread widely",
            "pronunciation": "/ˈbrɔdˌkæst/",
            "etymology": "From broad + cast, originally meaning 'to scatter seed widely'",
            "memory_tip": "BROADCAST: Basic Really - Obviously transmitting information, And Distributing content, Definitely Communicating to everyone, And Sharing Television programs, Something Television does",
            "example_sentence": "The news station will _____ the election results live tonight.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "broadcaster",
            "definition": "A person or organization that transmits radio or television programs",
            "pronunciation": "/ˈbrɔdˌkæstər/",
            "etymology": "From broadcast + -er, referring to one who broadcasts",
            "memory_tip": "BROADCASTER: Basic Really - Obviously transmitting content, And Distributing content, Definitely Communicating And Sharing Television programs, Teaching Everyone, Really professional communicator",
            "example_sentence": "The veteran _____ had been on the air for over thirty years.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "broadcasters",
            "definition": "People or organizations that transmit radio or television programs",
            "pronunciation": "/ˈbrɔdˌkæstərz/",
            "etymology": "From broadcaster + -s, plural of broadcaster",
            "memory_tip": "BROADCASTERS: Basic Really - Obviously transmitting content, And Distributing content, Definitely Communicating And Sharing Television programs, Teaching Everyone, Really professional communicators, Something media companies employ",
            "example_sentence": "The conference brought together _____ from around the world.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brocade",
            "definition": "A rich fabric with raised designs; to weave with a raised pattern",
            "pronunciation": "/broʊˈkeɪd/",
            "etymology": "From Spanish brocado, from Italian broccato meaning 'embossed cloth'",
            "memory_tip": "BROCADE: Beautiful Rich - Obviously expensive fabric, Carefully woven, And Decorated Elegantly",
            "example_sentence": "The queen's coronation gown was made of golden _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "broccolini",
            "definition": "A hybrid vegetable combining broccoli and Chinese kale",
            "pronunciation": "/ˌbrɑkəˈlini/",
            "etymology": "From broccoli + -ini suffix, meaning 'little broccoli'",
            "memory_tip": "BROCCOLINI: Beautiful Really - Obviously green vegetable, Constantly Cooking in restaurants, Obviously Luxurious vegetable, Including healthy nutrients, Never boring Ingredient",
            "example_sentence": "The chef sautéed the _____ with garlic and olive oil.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brochure",
            "definition": "A small pamphlet or booklet containing information or advertising",
            "pronunciation": "/broʊˈʃʊr/",
            "etymology": "From French brochure, from brocher meaning 'to stitch'",
            "memory_tip": "BROCHURE: Basic Really - Obviously Containing information, Having useful details, Usually business Reasonable advertising, Everyone uses marketing materials",
            "example_sentence": "The travel _____ featured beautiful photos of tropical destinations.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brochureorganized",
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
            "word": "brockage",
            "definition": "A defective coin with a design from another coin impressed on it",
            "pronunciation": "/ˈbrɑkɪdʒ/",
            "etymology": "From French brocage, from broquer meaning 'to strike' or 'to mint'",
            "memory_tip": "BROCKAGE: Basic Really - Obviously damaged coin, Collector values, And collecting Keeping rare coins, And Gathering Everything valuable",
            "example_sentence": "The coin collector found a rare _____ with double impressions.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "brogue",
            "definition": "A strong regional accent; a type of shoe with decorative perforations",
            "pronunciation": "/broʊɡ/",
            "etymology": "From Irish bróg meaning 'shoe', later extended to accent",
            "memory_tip": "BROGUE: Basic Really - Obviously Irish accent, Getting Everyone's attention, Usually Evident pronunciation",
            "example_sentence": "His thick Irish _____ made his stories even more charming.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "broil",
            "definition": "To cook with direct heat; to be very hot",
            "pronunciation": "/brɔɪl/",
            "etymology": "From Old French bruillir meaning 'to burn' or 'to roast'",
            "memory_tip": "BROIL: Basic Really - Obviously hot cooking, Including direct heat, Literally cooking with fire",
            "example_sentence": "She decided to _____ the fish instead of frying it.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "broken",
            "definition": "Damaged and no longer working; interrupted",
            "pronunciation": "/ˈbroʊkən/",
            "etymology": "From break + -en, past participle of break, from Old English brecan",
            "memory_tip": "BROKEN: Basic Really - Obviously damaged, Keeping Everyone from using it, Everyone knows damaged things, Never working properly",
            "example_sentence": "The _____ vase lay in pieces on the kitchen floor.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bromide",
            "definition": "A chemical compound; a trite or unoriginal remark",
            "pronunciation": "/ˈbroʊmaɪd/",
            "etymology": "From bromine + -ide, referring to compounds containing bromine",
            "memory_tip": "BROMIDE: Basic Really - Obviously chemical compound, Maybe used as medicine, Including bromine element, Definitely scientific term, Everyone knows basic chemistry",
            "example_sentence": "The speaker's presentation was full of tired _____s about success.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bromidealgae",
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
            "word": "brontophobia",
            "definition": "An irrational fear of thunder and thunderstorms",
            "pronunciation": "/ˌbrɑntoʊˈfoʊbiə/",
            "etymology": "From Greek bronte 'thunder' + phobos 'fear'",
            "memory_tip": "BRONTOPHOBIA: Basic Really - Obviously fearing thunder, Never Tolerating storms, Obviously Phobic reaction, Having Outstanding anxiety, Obviously Being Incredibly Afraid",
            "example_sentence": "Her _____ made summer storms a terrifying experience.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        }
    ]
    
    # Write to CSV file
    output_file = "C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\spelling_bee\\output\\batch_024_processed.csv"
    
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
        
        print(f"Batch 024 processing complete!")
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