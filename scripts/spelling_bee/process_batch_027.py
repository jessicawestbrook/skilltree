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
            "word": "cabeza",
            "definition": "Spanish word for head; also used in English in certain contexts",
            "pronunciation": "/kəˈbeɪsə/",
            "etymology": "From Spanish cabeza meaning 'head', from Latin caput",
            "memory_tip": "CABEZA: Common And - Basic Spanish word, Everyone Zestfully uses Spanish, Always learning foreign vocabulary",
            "example_sentence": "The wine region's _____ de vaca landmark attracted many tourists.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cabin",
            "definition": "A small simple dwelling; a room on a ship or aircraft",
            "pronunciation": "/ˈkæbɪn/",
            "etymology": "From Old French cabane, from Late Latin capanna meaning 'hut'",
            "memory_tip": "CABIN: Cozy And - Basic dwelling, Including shelter, Never fancy housing",
            "example_sentence": "They spent their vacation in a rustic log _____ by the lake.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cabochon",
            "definition": "A gem that is polished but not cut into facets",
            "pronunciation": "/ˈkæbəˌʃɑn/",
            "etymology": "From French cabochon, from caboche meaning 'head'",
            "memory_tip": "CABOCHON: Captivating And - Beautiful gemstone, Obviously rounded stone, Captivating Handcrafted jewelry, Obviously Natural shape",
            "example_sentence": "The emerald _____ gleamed smoothly in the antique ring.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "caboodle",
            "definition": "The whole lot; everything (usually in 'kit and caboodle')",
            "pronunciation": "/kəˈbudəl/",
            "etymology": "Possibly from Dutch boedel meaning 'property' or 'estate'",
            "memory_tip": "CABOODLE: Complete And - Basic entire collection, Obviously everything, Definitely Lots of stuff, Everything together",
            "example_sentence": "She sold the house and moved away, taking the whole kit and _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cabotage",
            "definition": "Trade or shipping between ports of the same country",
            "pronunciation": "/ˈkæbətɪdʒ/",
            "etymology": "From French cabotage, from caboter meaning 'to sail along the coast'",
            "memory_tip": "CABOTAGE: Coastal And - Business trade, Obviously between local ports, Trading And Getting Economic benefits",
            "example_sentence": "The shipping law restricted _____ to vessels flying the national flag.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cacao",
            "definition": "The seed from which cocoa and chocolate are made",
            "pronunciation": "/kəˈkaʊ/",
            "etymology": "From Spanish cacao, from Nahuatl cacahuatl",
            "memory_tip": "CACAO: Cocoa And - Chocolate making ingredient, And Outstanding flavor, Obviously delicious treats",
            "example_sentence": "The _____ beans were carefully roasted to develop their rich flavor.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cacaxte",
            "definition": "A wooden frame carried on the back for transporting goods",
            "pronunciation": "/kəˈkækstoʊ/",
            "etymology": "From Nahuatl cacaxtli meaning 'carrying frame'",
            "memory_tip": "CACAXTE: Carrying And - Carrying heavy loads, Always eXercising strength, Transportation Equipment",
            "example_sentence": "The porter used a _____ to carry supplies up the mountain trail.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cache",
            "definition": "A hidden storage place; to store in a hidden place",
            "pronunciation": "/kæʃ/",
            "etymology": "From French cache meaning 'hiding place', from cacher 'to hide'",
            "memory_tip": "CACHE: Concealed And - Careful storage, Hidden Everything safely",
            "example_sentence": "The explorers discovered a _____ of supplies left by previous expeditions.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cachexia",
            "definition": "Wasting of the body due to severe chronic illness",
            "pronunciation": "/kəˈkɛksiə/",
            "etymology": "From Greek kakos 'bad' + hexis 'condition'",
            "memory_tip": "CACHEXIA: Concerning And - Concerning medical condition, Healthy people Experiencing serious illness, eXtremely concerning health Issue, Always serious medical diagnosis",
            "example_sentence": "The patient showed signs of _____ from the prolonged illness.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cachexiacacoëthes",
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
            "word": "cachexiaconnoisseur",
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
            "word": "cacophonous",
            "definition": "Having a harsh, discordant mixture of sounds",
            "pronunciation": "/kəˈkɑfənəs/",
            "etymology": "From Greek kakos 'bad' + phone 'sound' + -ous",
            "memory_tip": "CACOPHONOUS: Concerning And - Concerning terrible sounds, Obviously Producing Harsh sounds, Obviously Never pleasant, Obviously Unpleasant Sounds",
            "example_sentence": "The _____ noise from the construction site disturbed the neighborhood.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cacoëthes",
            "definition": "An uncontrollable urge or desire to do something",
            "pronunciation": "/ˌkækəˈiθiz/",
            "etymology": "From Greek kakoëthes meaning 'bad habit' or 'malignant disease'",
            "memory_tip": "CACOËTHES: Concerning And - Concerning irresistible urge, Obviously Extreme compulsive behavior, Obviously Terrible Habit, Everyone Struggles with compulsions",
            "example_sentence": "He had a _____ for collecting rare books despite his limited budget.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cactus",
            "definition": "A spiny succulent plant adapted to dry climates",
            "pronunciation": "/ˈkæktəs/",
            "etymology": "From Latin cactus, from Greek kaktos meaning 'cardoon'",
            "memory_tip": "CACTUS: Caring And - Conserving water efficiently, Totally Unusual plant, Something desert plants",
            "example_sentence": "The desert _____ bloomed with beautiful pink flowers each spring.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cadaverous",
            "definition": "Resembling a corpse; extremely pale and thin",
            "pronunciation": "/kəˈdævərəs/",
            "etymology": "From Latin cadaver meaning 'corpse' + -ous",
            "memory_tip": "CADAVEROUS: Concerning And - Deathly pale appearance, And Very thin look, Everyone Recognizes unhealthy appearance, Obviously Unhealthy looking, Something concerning appearance",
            "example_sentence": "His _____ complexion worried his family about his health.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cadence",
            "definition": "A rhythmic sequence or flow; the rise and fall of the voice",
            "pronunciation": "/ˈkeɪdəns/",
            "etymology": "From Latin cadentia meaning 'falling', from cadere 'to fall'",
            "memory_tip": "CADENCE: Captivating And - Delightful rhythmic pattern, Everyone Notice rhythmic flow, Completely Elegant music pattern",
            "example_sentence": "The poet's reading had a musical _____ that captivated the audience.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cadencelions",
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
            "word": "cadge",
            "definition": "To ask for or obtain by begging; to borrow persistently",
            "pronunciation": "/kædʒ/",
            "etymology": "Possibly from Middle English caggen meaning 'to catch'",
            "memory_tip": "CADGE: Constantly And - Demanding things from others, Getting Everything free",
            "example_sentence": "He tried to _____ a free meal from his generous neighbor.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "caduceus",
            "definition": "A winged staff with two snakes, symbol of medicine and commerce",
            "pronunciation": "/kəˈdusiəs/",
            "etymology": "From Latin caduceus, from Greek karykeion meaning 'herald's wand'",
            "memory_tip": "CADUCEUS: Classic And - Distinguished medical symbol, United States medical symbol, Clearly European medical history, Everyone Understanding medical symbols",
            "example_sentence": "The _____ appeared on the medical school's official emblem.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "caducity",
            "definition": "The frailty of old age; transitory nature",
            "pronunciation": "/kəˈdusɪti/",
            "etymology": "From Latin caducitas meaning 'liability to fall', from cadere 'to fall'",
            "memory_tip": "CADUCITY: Concerning And - Declining physical condition, Understanding aging process, Completely Inevitable aging, Temporary human existence, Year-round aging process",
            "example_sentence": "The _____ of human life reminds us to cherish each moment.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "caerphilly",
            "definition": "A mild white cheese originally from Wales",
            "pronunciation": "/kərˈfɪli/",
            "etymology": "Named after Caerphilly, a town in Wales where it was first made",
            "memory_tip": "CAERPHILLY: Classic And - European cheese tradition, Really Premium cheese, Popular Heritage cheese, Including Lovely flavor, Lovely Year-round favorite cheese",
            "example_sentence": "The cheese board featured a creamy wedge of _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "caesar",
            "definition": "A Roman emperor; a powerful ruler",
            "pronunciation": "/ˈsizər/",
            "etymology": "From Julius Caesar, Roman general and dictator",
            "memory_tip": "CAESAR: Classic And - Exceptional historical ruler, Strong Ancient leader, Everyone Recognizes Roman history",
            "example_sentence": "The play depicted the assassination of _____ in vivid detail.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "caesious",
            "definition": "Having a bluish-gray color",
            "pronunciation": "/ˈsiʃəs/",
            "etymology": "From Latin caesius meaning 'bluish-gray'",
            "memory_tip": "CAESIOUS: Classic And - Elegant bluish color, Something Interesting blue-gray shade, Obviously Unique color, Something distinctive color",
            "example_sentence": "The _____ hue of the storm clouds warned of approaching rain.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "caffeine",
            "definition": "A bitter compound found in coffee and tea that acts as a stimulant",
            "pronunciation": "/kæˈfin/",
            "etymology": "From German Kaffein, from Kaffee meaning 'coffee'",
            "memory_tip": "CAFFEINE: Coffee And - Feeling energized, Feeling Energy immediately, Including Natural stimulant, Everyone needs morning boost",
            "example_sentence": "She avoided _____ after 3 PM to ensure better sleep.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "caftan",
            "definition": "A long loose garment worn in the Middle East and North Africa",
            "pronunciation": "/ˈkæftæn/",
            "etymology": "From Turkish kaftan, possibly from Persian qaftān",
            "memory_tip": "CAFTAN: Comfortable And - Flowing garment, Traditionally worn, And Never tight clothing",
            "example_sentence": "She wore a silk _____ to the summer garden party.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cahiers",
            "definition": "Notebooks or exercise books; written records or reports",
            "pronunciation": "/kəˈjeɪz/",
            "etymology": "From French cahier meaning 'notebook', from Latin quaternum",
            "memory_tip": "CAHIERS: Careful And - Handwritten records, Including Educational records, Everyone Records important information, Something students use",
            "example_sentence": "The scholar studied the revolutionary _____ from 18th-century France.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cahoots",
            "definition": "Partnership or conspiracy, especially for wrongdoing",
            "pronunciation": "/kəˈhuts/",
            "etymology": "Possibly from French cahute meaning 'cabin' or 'hut'",
            "memory_tip": "CAHOOTS: Conspiring And - Harmful activities, Obviously secret partnership, Obviously Together secretly, Something people plot together",
            "example_sentence": "The investigators suspected the two companies were in _____ to fix prices.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "caique",
            "definition": "A light rowing boat used in the Bosphorus; a type of sailing vessel",
            "pronunciation": "/kaɪˈik/",
            "etymology": "From Turkish kayık meaning 'boat'",
            "memory_tip": "CAIQUE: Classic And - Important water transportation, Quite Unique boat design, Everyone uses for transportation",
            "example_sentence": "The fisherman rowed his _____ across the calm harbor.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cairn",
            "definition": "A mound of stones built as a memorial or landmark",
            "pronunciation": "/kɛrn/",
            "etymology": "From Scottish Gaelic carn meaning 'heap of stones'",
            "memory_tip": "CAIRN: Carefully And - Important memorial marker, Really Notable landmarks",
            "example_sentence": "Hikers built a _____ to mark the summit of the mountain.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "caisson",
            "definition": "A watertight chamber used in underwater construction; an ammunition wagon",
            "pronunciation": "/ˈkeɪsən/",
            "etymology": "From French caisson meaning 'large box', from caisse 'box'",
            "memory_tip": "CAISSON: Careful And - Important construction equipment, Something Serious construction work, Obviously Necessary building tool",
            "example_sentence": "Workers used a _____ to build the bridge foundations underwater.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cajole",
            "definition": "To persuade someone through flattery or gentle urging",
            "pronunciation": "/kəˈdʒoʊl/",
            "etymology": "From French cajoler meaning 'to chatter like a jay'",
            "memory_tip": "CAJOLE: Convincing And - Jokingly persuading people, Obviously Logical persuasion, Everyone knows sweet-talking",
            "example_sentence": "She tried to _____ her brother into lending her his car.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cake",
            "definition": "A sweet baked dessert; to form into a hardened mass",
            "pronunciation": "/keɪk/",
            "etymology": "From Old Norse kaka, related to cook",
            "memory_tip": "CAKE: Celebrating And - Keeping Everyone happy treats",
            "example_sentence": "The birthday _____ was decorated with colorful frosting.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calabash",
            "definition": "A large gourd used as a container; a tree bearing such gourds",
            "pronunciation": "/ˈkæləˌbæʃ/",
            "etymology": "From Spanish calabaza, possibly from Arabic qar'a yābisa 'dry gourd'",
            "memory_tip": "CALABASH: Classic And - Large natural container, And Basic storage vessel, And Sharing traditional uses, Helpful traditional tools",
            "example_sentence": "The musician played rhythms on a _____ drum.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calamari",
            "definition": "Squid prepared as food; a culinary term for squid",
            "pronunciation": "/ˌkæləˈmɑri/",
            "etymology": "From Italian calamari, plural of calamaro meaning 'squid'",
            "memory_tip": "CALAMARI: Culinary And - Lightly prepared seafood, And Many people enjoy, And Really Italian cuisine",
            "example_sentence": "The restaurant served crispy fried _____ with marinara sauce.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calamondin",
            "definition": "A small citrus fruit that is a cross between a mandarin and a kumquat",
            "pronunciation": "/ˌkæləˈmɑndɪn/",
            "etymology": "From Tagalog kalamunding, referring to the small citrus fruit",
            "memory_tip": "CALAMONDIN: Citrus And - Lightly sour fruit, And Many people grow these, Obviously Nice tasting fruit, Delicious Including small citrus, Including Natural sweet-sour taste",
            "example_sentence": "The _____ tree in the garden produced tiny, tart oranges.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calcify",
            "definition": "To harden by calcium deposit; to become rigid or set in ways",
            "pronunciation": "/ˈkælsəˌfaɪ/",
            "etymology": "From Latin calx 'lime' + -ify meaning 'to make'",
            "memory_tip": "CALCIFY: Calcium And - Limestone hardening process, Completely Inflexible becoming, Forming solid material, Year-round natural process",
            "example_sentence": "Over time, the old injury began to _____ and cause stiffness.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calculator",
            "definition": "An electronic device for performing mathematical calculations",
            "pronunciation": "/ˈkælkjəˌleɪtər/",
            "etymology": "From Latin calculatus meaning 'computed' + -or suffix",
            "memory_tip": "CALCULATOR: Computing And - Logical mathematical tool, Calculating Using numbers, Lots of mathematical functions, And Totally Outstanding results, Obviously Reliable mathematical device",
            "example_sentence": "Students were allowed to use a _____ during the algebra exam.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calculus",
            "definition": "A branch of mathematics dealing with rates of change and accumulation",
            "pronunciation": "/ˈkælkjələs/",
            "etymology": "From Latin calculus meaning 'small stone' (used for counting)",
            "memory_tip": "CALCULUS: Computing And - Learning advanced mathematics, Calculus University level mathematics, Learning University Subject",
            "example_sentence": "She struggled with _____ but eventually mastered the concepts.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "caldera",
            "definition": "A large crater formed by volcanic collapse or explosion",
            "pronunciation": "/kælˈdɛrə/",
            "etymology": "From Spanish caldera meaning 'cauldron'",
            "memory_tip": "CALDERA: Crater And - Large volcanic formation, Dramatic Earth geological feature, Really Amazing geological formation",
            "example_sentence": "The massive _____ was formed after the ancient volcano collapsed.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calefacient",
            "definition": "Having a warming or heating effect; producing warmth",
            "pronunciation": "/ˌkæləˈfeɪʃənt/",
            "etymology": "From Latin calefacere meaning 'to make warm' + -ent",
            "memory_tip": "CALEFACIENT: Creating And - Lasting heat effect, Especially For warming people, And Comfortable warmth, Including Enhanced temperature, Never Too cold feeling",
            "example_sentence": "The _____ herbs in the tea helped warm her chilled body.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calendar",
            "definition": "A system for organizing days; a chart showing days and dates",
            "pronunciation": "/ˈkæləndər/",
            "etymology": "From Latin calendarium meaning 'account book', from calendae 'first day'",
            "memory_tip": "CALENDAR: Counting And - Listing days systematically, Everyone Needs date organization, Dates And Reminders",
            "example_sentence": "She marked important appointments on her desk _____.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calendula",
            "definition": "A bright orange or yellow flower; pot marigold",
            "pronunciation": "/kəˈlɛndʒələ/",
            "etymology": "From Latin calendula, from calendae meaning 'first day of the month'",
            "memory_tip": "CALENDULA: Colorful And - Lovely bright flower, Everyone Notices bright colors, Delightful garden flower, Usually Lovely garden addition",
            "example_sentence": "The garden was brightened by cheerful _____ blooms.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calenture",
            "definition": "A tropical fever; a delirious condition caused by heat",
            "pronunciation": "/ˈkælənˌtʃʊr/",
            "etymology": "From Spanish calentura meaning 'fever', from caliente 'hot'",
            "memory_tip": "CALENTURE: Concerning And - Lasting fever condition, Extremely Nerve-racking tropical illness, Totally Uncomfortable tropical fever, Really Exhausting tropical disease",
            "example_sentence": "The sailors suffered from _____ during their voyage through tropical waters.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calibrate",
            "definition": "To adjust precisely; to check or correct measurement scales",
            "pronunciation": "/ˈkæləˌbreɪt/",
            "etymology": "From French calibrer, from calibre meaning 'diameter of a gun barrel'",
            "memory_tip": "CALIBRATE: Carefully And - Logical precise adjustment, Including Better accuracy, Really Accurate measurements, Totally Exact precision",
            "example_sentence": "The technician needed to _____ the scale before weighing the samples.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calico",
            "definition": "A type of cotton fabric; having patches of different colors",
            "pronunciation": "/ˈkælɪˌkoʊ/",
            "etymology": "From Calicut, a city in India where the fabric was originally made",
            "memory_tip": "CALICO: Colorful And - Lovely patterned fabric, Including Colorful patches, Obviously multicolored appearance",
            "example_sentence": "The _____ cat had beautiful patches of orange, black, and white.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calisthenics",
            "definition": "Exercises performed without equipment, using body weight",
            "pronunciation": "/ˌkæləsˈθɛnɪks/",
            "etymology": "From Greek kalos 'beautiful' + sthenos 'strength'",
            "memory_tip": "CALISTHENICS: Cardio And - Lots of body exercises, Including Strength Training, Healthy Exercise programs, Everyone Needs physical fitness, Including Cardiovascular fitness, Something everyone Should do",
            "example_sentence": "The fitness class focused on _____ like push-ups and jumping jacks.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "called",
            "definition": "Past tense of call; summoned or named",
            "pronunciation": "/kɔld/",
            "etymology": "From call + -ed, where call comes from Old Norse kalla",
            "memory_tip": "CALLED: Contacted And - Loudly summoned someone, Loudly Everyone responded, Definitely contacted someone",
            "example_sentence": "She _____ her grandmother every Sunday afternoon.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calligram",
            "definition": "A text or poem in which the typography forms a visual image",
            "pronunciation": "/ˈkæləˌɡræm/",
            "etymology": "From Greek kalos 'beautiful' + gramma 'letter'",
            "memory_tip": "CALLIGRAM: Creative And - Lovely artistic writing, Literally Including visual art, Graphic Reading And creativity, Making beautiful visual poetry",
            "example_sentence": "The poet created a _____ shaped like a tree to illustrate nature.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "callow",
            "definition": "Young and inexperienced; immature",
            "pronunciation": "/ˈkæloʊ/",
            "etymology": "From Old English calu meaning 'bald, bare'",
            "memory_tip": "CALLOW: Concerning And - Lacking experience, Lacking Obviously Wisdom, Obviously naive and immature",
            "example_sentence": "The _____ recruit made several mistakes during training.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "calmed",
            "definition": "Made peaceful or quiet; soothed",
            "pronunciation": "/kɑmd/",
            "etymology": "From calm + -ed, where calm comes from Greek kauma 'heat of the day'",
            "memory_tip": "CALMED: Comfortable And - Lacking stress, Made Everyone relaxed, Everyone Definitely peaceful",
            "example_sentence": "The mother's gentle voice _____ the crying baby.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        }
    ]
    
    # Write to CSV file
    output_file = "C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\spelling_bee\\output\\batch_027_processed.csv"
    
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
        
        print(f"Batch 027 processing complete!")
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