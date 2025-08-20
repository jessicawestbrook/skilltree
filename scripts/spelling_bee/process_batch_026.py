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
            "word": "bump",
            "definition": "A light collision; a raised area; to knock against",
            "pronunciation": "/bʌmp/",
            "etymology": "Possibly imitative, from the sound of a collision",
            "memory_tip": "BUMP: Basic Usually - Minor collision, People hit things accidentally",
            "example_sentence": "She felt a small _____ when the car hit the pothole.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bumptious",
            "definition": "Self-assertive in an unpleasant way; arrogantly presumptuous",
            "pronunciation": "/ˈbʌmpʃəs/",
            "etymology": "From bump + -tious, possibly from the idea of pushing forward aggressively",
            "memory_tip": "BUMPTIOUS: Bad Usually - Making people annoyed, Pushy Totally obnoxious behavior, Irritating Obnoxious attitude, Usually Rude behavior, Something everyone dislikes",
            "example_sentence": "His _____ attitude made him unpopular with his colleagues.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bundt",
            "definition": "A type of cake baked in a ring-shaped pan with fluted sides",
            "pronunciation": "/bʌnt/",
            "etymology": "From German Bundkuchen, literally 'tied cake'",
            "memory_tip": "BUNDT: Beautiful Usually - Nice round cake, Decorative shaped dessert, Totally delicious cake",
            "example_sentence": "She baked a lemon _____ cake for the dinner party.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bungee",
            "definition": "An elastic cord used for jumping from heights; relating to bungee jumping",
            "pronunciation": "/ˈbʌndʒi/",
            "etymology": "From rubber, referring to the elastic material used",
            "memory_tip": "BUNGEE: Bold Usually - Never scared jumping, Getting Everyone Excited about jumping",
            "example_sentence": "The _____ cord stretched perfectly as he jumped from the bridge.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bunions",
            "definition": "Painful swellings on the big toes caused by ill-fitting shoes",
            "pronunciation": "/ˈbʌnjənz/",
            "etymology": "From Old French buignon meaning 'bump on the head'",
            "memory_tip": "BUNIONS: Bad Unfortunately - Nobody wants painful feet, Including Outstanding pain, Obviously Not comfortable, Something painful on feet",
            "example_sentence": "Her tight shoes caused painful _____ that required medical attention.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bunsen",
            "definition": "A type of gas burner used in laboratories (Bunsen burner)",
            "pronunciation": "/ˈbʌnsən/",
            "etymology": "Named after Robert Bunsen, German chemist who improved the design",
            "memory_tip": "BUNSEN: Basic Usually - Laboratory equipment, Science Experiments Need this burner",
            "example_sentence": "The chemistry student lit the _____ burner to heat the solution.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bunyanesque",
            "definition": "Resembling or characteristic of Paul Bunyan; gigantic or heroic in scale",
            "pronunciation": "/ˌbʌnjənˈɛsk/",
            "etymology": "From Bunyan (legendary giant lumberjack) + -esque meaning 'in the style of'",
            "memory_tip": "BUNYANESQUE: Big Usually - Never small size, Year-round Amazing folklore character, And Never normal size, Everyone Sees giant proportions, Quite Unusual size, Everyone knows giant legends",
            "example_sentence": "The construction project required _____ effort from the entire team.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bunyanesqueexsect",
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
            "word": "buoyancy",
            "definition": "The ability to float; cheerful and optimistic quality",
            "pronunciation": "/ˈbɔɪənsi/",
            "etymology": "From buoyant + -cy, where buoyant comes from Spanish boyar 'to float'",
            "memory_tip": "BUOYANCY: Beautiful Usually - Obviously floating ability, Year-round Amazing water physics, Never sinking down, Cheerful positive attitude, Year-round optimistic feeling",
            "example_sentence": "The life jacket provided enough _____ to keep him afloat.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bureau",
            "definition": "A government department; a writing desk with drawers",
            "pronunciation": "/ˈbjʊroʊ/",
            "etymology": "From French bureau meaning 'desk', from Old French burel 'dark brown cloth'",
            "memory_tip": "BUREAU: Basic Usually - Responsible for government services, Everyone Always Using government services, Usually office work",
            "example_sentence": "She applied for a position at the _____ of statistics.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bureaucrats",
            "definition": "Government officials who work in a bureaucracy",
            "pronunciation": "/ˈbjʊrəˌkræts/",
            "etymology": "From bureaucrat + -s, where bureaucrat comes from French bureaucrate",
            "memory_tip": "BUREAUCRATS: Basic Usually - Responsible for government services, Everyone Always Using government services, Usually office work, Creating Rules And procedures, Totally involved in Systematic administration",
            "example_sentence": "The _____ processed the applications according to established procedures.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "burelage",
            "definition": "The striated or ribbed appearance of an engraved surface",
            "pronunciation": "/ˈbjʊrəlɪdʒ/",
            "etymology": "From French burelage, from bure meaning 'ribbed cloth'",
            "memory_tip": "BURELAGE: Beautiful Usually - Ribbed texture pattern, Engraving Leaving distinctive texture, And Giving Elegant appearance",
            "example_sentence": "The engraver created a fine _____ texture on the metal plate.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "burgee",
            "definition": "A triangular or swallow-tailed flag, especially of a yacht club",
            "pronunciation": "/bərˈdʒi/",
            "etymology": "Possibly from French bourgeois, referring to merchant ships",
            "memory_tip": "BURGEE: Beautiful Usually - Recognizable flag design, Getting Everyone's attention, Everyone Enjoys yacht club symbols",
            "example_sentence": "The yacht club's _____ flew proudly from the mast.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "burglarious",
            "definition": "Of or relating to burglary; involving breaking and entering",
            "pronunciation": "/bərˈɡlɛriəs/",
            "etymology": "From burglar + -ious, relating to one who commits burglary",
            "memory_tip": "BURGLARIOUS: Bad Usually - Really criminal activity, Getting everyone Locked out, And Really illegal actions, Involving Obvious criminal behavior, Usually Something criminal",
            "example_sentence": "The suspect was charged with _____ intent after being caught with lock picks.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "burgoo",
            "definition": "A thick stew or porridge, especially one served at outdoor gatherings",
            "pronunciation": "/bərˈɡu/",
            "etymology": "Possibly from Arabic burghul meaning 'crushed grain'",
            "memory_tip": "BURGOO: Basic Usually - Really thick stew, Getting everyone Organized for outdoor cooking, Obviously hearty food",
            "example_sentence": "The Kentucky _____ simmered all day over the open fire.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "burgoooccupancy",
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
            "word": "burgundy",
            "definition": "A dark red color; a type of wine from the Burgundy region of France",
            "pronunciation": "/ˈbɜrɡəndi/",
            "etymology": "From Burgundy, the French region famous for its wine",
            "memory_tip": "BURGUNDY: Beautiful Usually - Really dark red color, Getting everyone to Notice deep wine color, Definitely rich color, Year-round sophisticated color",
            "example_sentence": "She chose a _____ dress that complemented her complexion.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "burial",
            "definition": "The act of placing a dead body in the ground; interment",
            "pronunciation": "/ˈbɛriəl/",
            "etymology": "From bury + -ial, where bury comes from Old English byrgan",
            "memory_tip": "BURIAL: Basic Usually - Respectful ceremony, Important And solemn ceremony, And Last ceremony",
            "example_sentence": "The family held a private _____ service for their loved one.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "burkinabe",
            "definition": "A native or inhabitant of Burkina Faso",
            "pronunciation": "/ˌbɜrkɪnəˈbeɪ/",
            "etymology": "From Burkina Faso + -be, the local suffix for 'person from'",
            "memory_tip": "BURKINABE: Basic Usually - Referring to African nationality, Keeping Identity from Burkina Faso, And National identity, Beautiful African heritage, Everyone from specific country",
            "example_sentence": "The _____ delegation spoke about sustainable development goals.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "burlap",
            "definition": "A coarse canvas fabric made from jute or hemp",
            "pronunciation": "/ˈbɜrlæp/",
            "etymology": "Possibly from Middle English borel meaning 'coarse cloth'",
            "memory_tip": "BURLAP: Basic Usually - Rough textured fabric, Lots of practical uses, And Practical material",
            "example_sentence": "The coffee beans were shipped in large _____ sacks.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "burly",
            "definition": "Large and strong; heavily built",
            "pronunciation": "/ˈbɜrli/",
            "etymology": "From Middle English burlich meaning 'stately, imposing'",
            "memory_tip": "BURLY: Big Usually - Really strong person, Lots of muscle, Year-round strong build",
            "example_sentence": "The _____ bouncer easily handled the unruly crowd.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "burner",
            "definition": "A device that produces a flame; a heating element",
            "pronunciation": "/ˈbɜrnər/",
            "etymology": "From burn + -er, referring to something that burns",
            "memory_tip": "BURNER: Basic Usually - Responsible for heating, Never cold equipment, Everyone Recognizes stove equipment",
            "example_sentence": "She turned up the _____ to boil the water faster.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "burro",
            "definition": "A small donkey, especially one used as a pack animal",
            "pronunciation": "/ˈbʊroʊ/",
            "etymology": "From Spanish burro meaning 'donkey'",
            "memory_tip": "BURRO: Basic Usually - Reliable animal helper, Reliable Outdoor working animal",
            "example_sentence": "The _____ carried supplies up the narrow mountain trail.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "burrowing",
            "definition": "Digging holes or tunnels underground; making burrows",
            "pronunciation": "/ˈbɛroʊɪŋ/",
            "etymology": "From burrow + -ing, where burrow comes from Middle English borough",
            "memory_tip": "BURROWING: Basic Usually - Really digging underground, Rabbits Often dig holes, Working In underground spaces, Never Getting tired of digging, Getting under the ground",
            "example_sentence": "The _____ animals created an extensive tunnel system.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bursary",
            "definition": "A monetary grant given to a student; a scholarship",
            "pronunciation": "/ˈbɜrsəri/",
            "etymology": "From Medieval Latin bursaria, from bursa meaning 'purse'",
            "memory_tip": "BURSARY: Basic Usually - Regarding financial aid, Supporting Academic achievement, Really helping students, Year-round financial assistance",
            "example_sentence": "The _____ helped cover her tuition expenses for medical school.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bursting",
            "definition": "Breaking open suddenly; filled to capacity",
            "pronunciation": "/ˈbɜrstɪŋ/",
            "etymology": "From burst + -ing, where burst comes from Old English berstan",
            "memory_tip": "BURSTING: Basic Usually - Really overflowing situation, Something Too much pressure, Including pressure release, Never Getting contained, Getting explosive energy",
            "example_sentence": "The balloon was _____ with helium before it finally popped.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "busby",
            "definition": "A tall fur hat worn by certain military units",
            "pronunciation": "/ˈbʌzbi/",
            "etymology": "Possibly named after a 18th-century hat maker named Busby",
            "memory_tip": "BUSBY: Basic Usually - Special military hat, Bold Year-round uniform accessory",
            "example_sentence": "The guard's _____ was an iconic part of his ceremonial uniform.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "busbyadjective",
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
            "word": "bushel",
            "definition": "A unit of measurement for dry goods; a large quantity",
            "pronunciation": "/ˈbʊʃəl/",
            "etymology": "From Old French boissel, from Germanic origin meaning 'little box'",
            "memory_tip": "BUSHEL: Basic Usually - Standard measurement unit, Holding Everything together, Lots of grain or produce",
            "example_sentence": "The farmer harvested three _____s of wheat from the field.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "business",
            "definition": "Commercial activity; a company or organization",
            "pronunciation": "/ˈbɪznəs/",
            "etymology": "From busy + -ness, originally meaning 'state of being busy'",
            "memory_tip": "BUSINESS: Basic Usually - Something Important commercial activity, Never Easy work, Everyone Supports commerce, Something everyone needs",
            "example_sentence": "She started her own _____ selling handmade jewelry.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "businesses",
            "definition": "Commercial enterprises; companies or organizations",
            "pronunciation": "/ˈbɪznəsəz/",
            "etymology": "From business + -es, plural of business",
            "memory_tip": "BUSINESSES: Basic Usually - Something Important commercial activities, Never Easy work, Everyone Supports commerce, Something everyone needs, Every town has many commerce, Something creating jobs",
            "example_sentence": "Many small _____ struggled during the economic downturn.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bustling",
            "definition": "Full of activity; moving energetically",
            "pronunciation": "/ˈbʌsəlɪŋ/",
            "etymology": "From bustle + -ing, where bustle means 'to move energetically'",
            "memory_tip": "BUSTLING: Basic Usually - Something Totally active environment, Lots of activity, Including Never stopping movement, Getting everyone moving",
            "example_sentence": "The _____ marketplace was filled with vendors and shoppers.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "busy",
            "definition": "Having a lot to do; actively engaged in activity",
            "pronunciation": "/ˈbɪzi/",
            "etymology": "From Old English bisig meaning 'anxious, occupied'",
            "memory_tip": "BUSY: Basic Usually - Something Year-round active situation",
            "example_sentence": "She was too _____ to answer the phone during the meeting.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "butterfly",
            "definition": "A flying insect with large colorful wings; a swimming stroke",
            "pronunciation": "/ˈbʌtərˌflaɪ/",
            "etymology": "From butter + fly, possibly from the yellow color of some species",
            "memory_tip": "BUTTERFLY: Beautiful Usually - Totally colorful insect, Totally Elegant flying pattern, Really Flying beautifully, Lots of beautiful colors, Year-round garden visitors",
            "example_sentence": "The monarch _____ migrated thousands of miles to reach its destination.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "butterscotch",
            "definition": "A candy made with butter and brown sugar; the flavor of this candy",
            "pronunciation": "/ˈbʌtərˌskɑtʃ/",
            "etymology": "From butter + scotch (meaning 'to cut'), referring to the candy-making process",
            "memory_tip": "BUTTERSCOTCH: Beautiful Usually - Totally sweet candy flavor, Totally Excellent candy, Really Sweet flavor, Candy Obviously rich, Totally Creamy sweet candy, Heavenly sweet taste",
            "example_sentence": "The _____ pudding was her grandmother's favorite dessert recipe.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "buttons",
            "definition": "Small fasteners for clothing; controls on devices",
            "pronunciation": "/ˈbʌtənz/",
            "etymology": "From button + -s, where button comes from Old French boton",
            "memory_tip": "BUTTONS: Basic Usually - Totally practical fasteners, Totally Obviously needed, Never Staying without fasteners, Something everyone uses on clothing",
            "example_sentence": "The antique dress had beautiful pearl _____ down the front.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "buzzard",
            "definition": "A large bird of prey; a vulture",
            "pronunciation": "/ˈbʌzərd/",
            "etymology": "From Old French busart, from Latin buteo meaning 'hawk'",
            "memory_tip": "BUZZARD: Basic Usually - Zipping through sky, Zipping Around hunting, Really flying high, Definitely predatory bird",
            "example_sentence": "The _____ circled overhead, searching for carrion.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "buzzing",
            "definition": "Making a continuous humming sound; filled with excitement",
            "pronunciation": "/ˈbʌzɪŋ/",
            "etymology": "From buzz + -ing, where buzz is imitative of the sound",
            "memory_tip": "BUZZING: Basic Usually - Zipping sound constantly, Zipping constantly, Including Never-ending sound, Getting everyone's attention",
            "example_sentence": "The _____ of bees filled the air around the hive.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "buzzworthy",
            "definition": "Likely to generate interest or excitement; newsworthy",
            "pronunciation": "/ˈbʌzˌwɜrði/",
            "etymology": "From buzz (excitement) + worthy (deserving of)",
            "memory_tip": "BUZZWORTHY: Basic Usually - Zipping through social media, Zipping With interest, Obviously Really exciting news, Totally Highly interesting, Year-round exciting news",
            "example_sentence": "The celebrity's announcement was highly _____ on social media.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "buñuelo",
            "definition": "A fried dough pastry, popular in Spanish and Latin American cuisine",
            "pronunciation": "/buˈɲweloʊ/",
            "etymology": "From Spanish buñuelo, possibly from Arabic bunyol",
            "memory_tip": "BUÑUELO: Beautiful Usually - Ñice fried pastry, Usually Enjoyed by Everyone, Lots of sweetness, Obviously delicious treat",
            "example_sentence": "The bakery's fresh _____ were dusted with cinnamon and sugar.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "buñueloguan",
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
            "word": "bygone",
            "definition": "Belonging to an earlier time; past",
            "pronunciation": "/ˈbaɪˌɡɔn/",
            "etymology": "From by (past) + gone, literally meaning 'gone by'",
            "memory_tip": "BYGONE: Basic Yesterday - Gone away forever, Obviously Never coming back, Everyone remembers past times",
            "example_sentence": "They reminisced about the _____ days of their youth.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bypass",
            "definition": "To go around or avoid; an alternative route",
            "pronunciation": "/ˈbaɪˌpæs/",
            "etymology": "From by (around) + pass, literally meaning 'to pass by'",
            "memory_tip": "BYPASS: Basic Yesterday - Passing around obstacles, And Solving problems, Something everyone uses for shortcuts",
            "example_sentence": "The new highway will _____ the congested downtown area.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "byzantine",
            "definition": "Relating to the Byzantine Empire; excessively complex",
            "pronunciation": "/ˈbɪzənˌtin/",
            "etymology": "From Byzantium, the ancient Greek city later known as Constantinople",
            "memory_tip": "BYZANTINE: Basic Yesterday - Zestful ancient empire, And Never simple procedures, Totally Incredibly complicated systems, Never Easy procedures",
            "example_sentence": "The company's _____ bureaucracy made simple tasks unnecessarily difficult.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "béchamel",
            "definition": "A white sauce made from butter, flour, and milk",
            "pronunciation": "/ˌbeɪʃəˈmɛl/",
            "etymology": "Named after Louis de Béchamel, French courtier",
            "memory_tip": "BÉCHAMEL: Beautiful European - Creamy sauce, Having Amazing flavor, Making Everyone Love cooking, Extremely Luxurious sauce",
            "example_sentence": "The lasagna was layered with rich _____ sauce.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "bêtise",
            "definition": "A foolish act or remark; stupidity",
            "pronunciation": "/beˈtiz/",
            "etymology": "From French bêtise meaning 'foolishness', from bête 'beast'",
            "memory_tip": "BÊTISE: Bad Everyone - Totally foolish behavior, Including Stupid actions, Something Everyone avoids",
            "example_sentence": "His latest _____ cost him his job at the embassy.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cabal",
            "definition": "A secret group plotting against authority; a conspiracy",
            "pronunciation": "/kəˈbæl/",
            "etymology": "From Hebrew qabbalah meaning 'received tradition'",
            "memory_tip": "CABAL: Conspiring Against - Basic Authority, And Lots of secrecy",
            "example_sentence": "The political _____ met secretly to plan their strategy.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cabaletta",
            "definition": "A simple aria with a repetitive rhythm, often concluding an opera scene",
            "pronunciation": "/ˌkæbəˈlɛtə/",
            "etymology": "From Italian cabaletta, diminutive of cabala meaning 'intrigue'",
            "memory_tip": "CABALETTA: Captivating And - Beautiful operatic song, And Lovely singing, Elegant Totally amazing music, Totally Amazing classical music",
            "example_sentence": "The soprano's _____ brought thunderous applause from the audience.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cabaret",
            "definition": "Entertainment performed in a nightclub; a nightclub with live entertainment",
            "pronunciation": "/ˌkæbəˈreɪ/",
            "etymology": "From French cabaret meaning 'tavern'",
            "memory_tip": "CABARET: Captivating And - Beautiful entertainment, And Really Entertaining music, Excellent Talented performers",
            "example_sentence": "The intimate _____ featured jazz singers and comedians.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        },
        {
            "word": "cabbage",
            "definition": "A leafy green vegetable with dense leaves forming a round head",
            "pronunciation": "/ˈkæbɪdʒ/",
            "etymology": "From Old French caboche meaning 'head'",
            "memory_tip": "CABBAGE: Common And - Basic vegetable, Basic And Green vegetable, Everyone knows this vegetable",
            "example_sentence": "She added fresh _____ to the soup for extra nutrition.",
            "etymology_source": "Claude",
            "definition_source": "Claude",
            "example_sentence_source": "Claude",
            "audio_source": "",
            "combined_word_error": False
        }
    ]
    
    # Write to CSV file
    output_file = "C:\\Users\\jessi\\Projects\\skilltree2\\scripts\\spelling_bee\\output\\batch_026_processed.csv"
    
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
        
        print(f"Batch 026 processing complete!")
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