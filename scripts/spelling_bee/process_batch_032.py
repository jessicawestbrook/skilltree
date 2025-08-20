import pandas as pd
import csv
import random

class DifficultyCalculator:
    def __init__(self):
        self.phonetic_patterns = {
            'silent_letters': ['b', 'k', 'l', 'w', 'h'],
            'double_consonants': ['ss', 'tt', 'nn', 'mm', 'll', 'dd', 'cc'],
            'irregular_vowels': ['ough', 'augh', 'eigh', 'ieu']
        }
        
    def calculate_difficulty(self, word, definition="", etymology=""):
        phonetic_score = self._calculate_phonetic_transparency(word)
        frequency_score = self._estimate_word_frequency(word)
        morphology_score = self._analyze_morphological_complexity(word, definition)
        etymology_score = self._analyze_etymological_complexity(etymology)
        
        raw_score = (phonetic_score + frequency_score + morphology_score + etymology_score) / 4
        
        if raw_score <= 2:
            return "Beginning"
        elif raw_score <= 4:
            return "Intermediate"
        elif raw_score <= 6:
            return "Advanced"
        else:
            return "Expert"
    
    def _calculate_phonetic_transparency(self, word):
        score = 1
        word_lower = word.lower()
        
        for pattern in self.phonetic_patterns['silent_letters']:
            if pattern in word_lower and not self._is_pronounced(word_lower, pattern):
                score += 1
                
        for pattern in self.phonetic_patterns['double_consonants']:
            if pattern in word_lower:
                score += 0.5
                
        for pattern in self.phonetic_patterns['irregular_vowels']:
            if pattern in word_lower:
                score += 1.5
                
        return min(score, 8)
    
    def _is_pronounced(self, word, letter):
        silent_contexts = {
            'b': ['mb', 'bt'],
            'k': ['kn'],
            'l': ['lf', 'lk', 'lm'],
            'w': ['wr', 'wh'],
            'h': ['rh', 'gh']
        }
        
        if letter in silent_contexts:
            for context in silent_contexts[letter]:
                if context in word:
                    return False
        return True
    
    def _estimate_word_frequency(self, word):
        length = len(word)
        if length <= 4:
            return 1
        elif length <= 6:
            return 2
        elif length <= 8:
            return 3
        elif length <= 10:
            return 4
        else:
            return 5
    
    def _analyze_morphological_complexity(self, word, definition):
        score = 1
        
        prefixes = ['pre', 'post', 'anti', 'semi', 'multi', 'inter', 'super', 'sub', 'trans', 'over', 'under']
        suffixes = ['tion', 'sion', 'ment', 'ness', 'able', 'ible', 'ous', 'ful', 'less', 'ing', 'ed']
        
        for prefix in prefixes:
            if word.lower().startswith(prefix):
                score += 0.5
                
        for suffix in suffixes:
            if word.lower().endswith(suffix):
                score += 0.5
                
        if any(char.isupper() for char in word[1:]):
            score += 1
            
        return min(score, 6)
    
    def _analyze_etymological_complexity(self, etymology):
        if not etymology:
            return 2
            
        etymology_lower = etymology.lower()
        complex_origins = ['greek', 'latin', 'sanskrit', 'arabic', 'hebrew', 'chinese', 'japanese']
        
        score = 1
        for origin in complex_origins:
            if origin in etymology_lower:
                score += 1
                
        return min(score, 6)

def process_batch_032():
    # Read the batch file
    input_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_032_words.csv"
    output_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_032_processed.csv"
    
    # Read the input file
    df = pd.read_csv(input_file)
    
    # Initialize difficulty calculator
    calc = DifficultyCalculator()
    
    # Combined word errors detected
    combined_errors = ["charismaticchâteau", "charlotteelation", "chastisechief"]
    
    # Create comprehensive word data
    word_data = [
        {
            "word": "cerebellum",
            "definition": "The part of the brain that coordinates movement, balance, and posture, located at the back of the skull beneath the cerebrum.",
            "pronunciation": "/ˌsɛrəˈbɛləm/",
            "pronunciation_audio_url": "",
            "example_sentence": "Damage to the _____ can result in problems with coordination and balance during movement.",
            "etymology": "From Latin cerebellum, diminutive of cerebrum 'brain'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CEREBELLUM: Coordinating Everyone's Reflexes Enables Balanced Excellent Locomotion Learning Using Motion - brain balance center.",
            "fun_fact": "Despite being only 10% of the brain's volume, the cerebellum contains over half of all neurons in the brain.",
            "difficulty_level": calc.calculate_difficulty("cerebellum", "Part of brain coordinating movement", "From Latin cerebellum"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cermet",
            "definition": "A composite material made of ceramic and metallic materials, combining properties of both for specialized applications.",
            "pronunciation": "/ˈsɜrmɛt/",
            "pronunciation_audio_url": "",
            "example_sentence": "The cutting tool was made from _____, which provided both hardness and toughness for industrial applications.",
            "etymology": "Blend of ceramic + metal",
            "etymology_source": "Claude",
            "memory_tip": "Remember CERMET: Ceramic Related Material Engineered Together - ceramic-metal composite.",
            "fun_fact": "Cermets are used in high-performance applications like jet engine components and cutting tools because they resist wear and heat.",
            "difficulty_level": calc.calculate_difficulty("cermet", "A ceramic-metal composite", "Blend of ceramic + metal"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "certain",
            "definition": "Known for sure; established beyond doubt; confident and assured.",
            "pronunciation": "/ˈsɜrtən/",
            "pronunciation_audio_url": "",
            "example_sentence": "She was _____ that her calculations were correct after checking them multiple times.",
            "etymology": "From Old French certain, from Latin certus 'settled, sure'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CERTAIN: Completely Established Reality That Anyone Is Notable - sure and confident.",
            "fun_fact": "The phrase 'for certain' emphasizes absolute certainty, while 'certain people' means 'some specific people.'",
            "difficulty_level": calc.calculate_difficulty("certain", "Known for sure", "From Latin certus"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "certiorari",
            "definition": "A legal writ from a higher court ordering a lower court to send up records of a case for review.",
            "pronunciation": "/ˌsɜrʃiəˈrɛri/",
            "pronunciation_audio_url": "",
            "example_sentence": "The Supreme Court granted _____ to review the controversial constitutional law case.",
            "etymology": "From Latin certiorari 'to be made more certain'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CERTIORARI: Court Examination Requiring Thorough Investigation Of Records And Related Issues - legal review writ.",
            "fun_fact": "The U.S. Supreme Court uses certiorari to choose which cases to hear, granting it in only about 1% of petitions filed.",
            "difficulty_level": calc.calculate_difficulty("certiorari", "A legal writ for case review", "From Latin certiorari"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "certitude",
            "definition": "Absolute certainty or conviction; complete confidence in one's beliefs or knowledge.",
            "pronunciation": "/ˈsɜrtɪˌtud/",
            "pronunciation_audio_url": "",
            "example_sentence": "His _____ about the success of the project inspired confidence in the entire team.",
            "etymology": "From Latin certitudo, from certus 'certain'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CERTITUDE: Complete Evidence Reveals Truth In Total Unwavering Definite Explanation - absolute certainty.",
            "fun_fact": "Philosophers distinguish between certitude (subjective confidence) and certainty (objective truth), though they're often used interchangeably.",
            "difficulty_level": calc.calculate_difficulty("certitude", "Absolute certainty", "From Latin certitudo"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cetology",
            "definition": "The branch of zoology dealing with whales, dolphins, and other cetaceans.",
            "pronunciation": "/sɪˈtɑlədʒi/",
            "pronunciation_audio_url": "",
            "example_sentence": "The marine biologist specialized in _____, studying humpback whale migration patterns.",
            "etymology": "From Greek ketos 'whale, sea monster' + -logy 'study of'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CETOLOGY: Careful Examination Teaching Our Learning Of Great Yearning whales - whale study.",
            "fun_fact": "Herman Melville helped popularize the term 'cetology' in his novel Moby-Dick, which includes detailed chapters on whale biology.",
            "difficulty_level": calc.calculate_difficulty("cetology", "The study of whales", "From Greek ketos + -logy"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chachalacas",
            "definition": "Large game birds native to the Americas, related to turkeys and known for their loud, raucous calls.",
            "pronunciation": "/ˌtʃɑtʃəˈlɑkəz/",
            "pronunciation_audio_url": "",
            "example_sentence": "The dawn chorus of _____ echoed through the tropical forest, waking the entire camp.",
            "etymology": "From Spanish chachalaca, imitative of the bird's call",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHACHALACAS: Chattering And Calling Habitually All Loud And Clamorous Active Sounds - noisy tropical birds.",
            "fun_fact": "Chachalacas are among the loudest birds in the Americas, with calls that can be heard over a mile away.",
            "difficulty_level": calc.calculate_difficulty("chachalacas", "Loud tropical birds", "From Spanish chachalaca"),
            "source_difficulty": "Two Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chai",
            "definition": "A spiced tea beverage, typically made with black tea, milk, and aromatic spices like cardamom and cinnamon.",
            "pronunciation": "/tʃaɪ/",
            "pronunciation_audio_url": "",
            "example_sentence": "She enjoyed a warm cup of _____ latte with its blend of cinnamon, cardamom, and ginger.",
            "etymology": "From Hindi chai, from Chinese cha 'tea'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHAI: Cinnamon Herbs And India beverage - spiced tea drink.",
            "fun_fact": "The word 'chai' simply means 'tea' in many languages, so 'chai tea' is technically redundant, meaning 'tea tea.'",
            "difficulty_level": calc.calculate_difficulty("chai", "A spiced tea beverage", "From Hindi chai"),
            "source_difficulty": "Two Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chain",
            "definition": "A series of connected metal links; a sequence of related things or events.",
            "pronunciation": "/tʃeɪn/",
            "pronunciation_audio_url": "",
            "example_sentence": "The heavy _____ secured the boat to the dock during the storm.",
            "etymology": "From Old French chaeine, from Latin catena 'chain'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHAIN: Connected Hardware And Interlocking Nodes - linked metal series.",
            "fun_fact": "The strongest chains are only as strong as their weakest link, which inspired the famous metaphor about team strength.",
            "difficulty_level": calc.calculate_difficulty("chain", "Series of connected links", "From Latin catena"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chalaza",
            "definition": "One of two spiral bands of thick egg white that anchor the yolk in the center of an egg.",
            "pronunciation": "/kəˈleɪzə/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ keeps the egg yolk properly positioned within the protective white.",
            "etymology": "From Greek khalaza 'hailstone, lump'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHALAZA: Connecting Harness And Linking Anchor Zonally Arranged - egg yolk anchor.",
            "fun_fact": "A prominent chalaza is actually a sign of a fresh, high-quality egg, not a defect as some people think.",
            "difficulty_level": calc.calculate_difficulty("chalaza", "Spiral band in egg white", "From Greek khalaza"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chalcolithic",
            "definition": "Relating to a prehistoric period when both stone and copper tools were used, also called the Copper Age.",
            "pronunciation": "/ˌkælkoʊˈlɪθɪk/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ period marked humanity's transition from the Stone Age to the Bronze Age.",
            "etymology": "From Greek khalkos 'copper' + lithos 'stone' + -ic",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHALCOLITHIC: Copper Hardware And Lithic Combined Old Learning In Technology Historical Innovation Culture - copper-stone age.",
            "fun_fact": "The Chalcolithic period began around 4500 BCE in some regions and represents humanity's first use of metal tools.",
            "difficulty_level": calc.calculate_difficulty("chalcolithic", "Relating to copper-stone age", "From Greek khalkos + lithos + -ic"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chalet",
            "definition": "A wooden house with overhanging eaves, typically found in mountainous regions, especially the Alps.",
            "pronunciation": "/ʃæˈleɪ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The cozy mountain _____ offered stunning views of the snow-covered peaks.",
            "etymology": "From French chalet, from Swiss French chalets 'herdsman's hut'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHALET: Charming House And Lodge Excellent Together - Alpine mountain house.",
            "fun_fact": "Traditional chalets were designed with wide, overhanging roofs to shed heavy snow loads common in Alpine regions.",
            "difficulty_level": calc.calculate_difficulty("chalet", "A wooden mountain house", "From Swiss French chalets"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chalice",
            "definition": "A ceremonial cup or goblet, especially one used in religious rituals for wine or communion.",
            "pronunciation": "/ˈtʃælɪs/",
            "pronunciation_audio_url": "",
            "example_sentence": "The ornate golden _____ was passed among the congregants during the communion service.",
            "etymology": "From Old French chalice, from Latin calix 'cup'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHALICE: Ceremonial Holy And Liturgical Important Cup Elegant - religious goblet.",
            "fun_fact": "The Holy Grail, sought by medieval knights, was said to be the chalice used at the Last Supper.",
            "difficulty_level": calc.calculate_difficulty("chalice", "A ceremonial cup", "From Latin calix"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chalk",
            "definition": "A soft white limestone used for writing on blackboards; a powdery substance used for marking.",
            "pronunciation": "/tʃɔk/",
            "pronunciation_audio_url": "",
            "example_sentence": "The teacher used white _____ to write the equations on the blackboard.",
            "etymology": "From Old English cealc, from Latin calx 'limestone'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHALK: Classroom Hardware And Learning Kit - white writing material.",
            "fun_fact": "The White Cliffs of Dover are made of chalk formed from ancient marine organisms over millions of years.",
            "difficulty_level": calc.calculate_difficulty("chalk", "White writing material", "From Latin calx"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "challenge",
            "definition": "A demanding task or situation that tests someone's abilities; to question or dispute something.",
            "pronunciation": "/ˈtʃælɪndʒ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The mountain climb presented a significant _____ that required careful preparation and skill.",
            "etymology": "From Old French chalenge, from Latin calumnia 'false accusation'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHALLENGE: Confronting Hard And Lengthy Learning Events Needing Great Effort - demanding task.",
            "fun_fact": "The word originally meant 'false accusation' but evolved to mean 'summons to a contest' and then 'difficult task.'",
            "difficulty_level": calc.calculate_difficulty("challenge", "A demanding task", "From Latin calumnia"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chamberlain",
            "definition": "A senior official in charge of managing a royal or noble household; a treasurer or steward.",
            "pronunciation": "/ˈtʃeɪmbərlɪn/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ oversaw all aspects of the castle's daily operations and royal ceremonies.",
            "etymology": "From Old French chamberlenc, from chamber + -lain (Germanic origin)",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHAMBERLAIN: Chamber Attendant Managing Household Estate Requirements Leading And In Nobility - royal household manager.",
            "fun_fact": "Neville Chamberlain, the British Prime Minister known for appeasement before WWII, came from a family of political chamberlains.",
            "difficulty_level": calc.calculate_difficulty("chamberlain", "A household steward", "From Old French chamberlenc"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chambray",
            "definition": "A lightweight fabric with colored warp threads and white filling threads, creating a mottled appearance.",
            "pronunciation": "/ˈʃæmbreɪ/",
            "pronunciation_audio_url": "",
            "example_sentence": "Her blue _____ shirt had a subtle texture that looked sophisticated yet casual.",
            "etymology": "From Cambrai, a city in France where the fabric was originally made",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHAMBRAY: Colored Haberdashery And Material Bringing Rich Authentic Yarn - textured cotton fabric.",
            "fun_fact": "Chambray is often confused with denim, but chambray uses different colored threads while denim uses the same color throughout.",
            "difficulty_level": calc.calculate_difficulty("chambray", "A lightweight cotton fabric", "From Cambrai, France"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "champignon",
            "definition": "A small edible mushroom, especially the common button mushroom used in cooking.",
            "pronunciation": "/ˌʃæmpɪˈnjɑn/",
            "pronunciation_audio_url": "",
            "example_sentence": "The chef sautéed fresh _____ mushrooms with garlic and herbs for the pasta dish.",
            "etymology": "From French champignon, from Late Latin campio 'mushroom'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHAMPIGNON: Culinary Harvested And Marvelous Prepared In Gourmet Nutrition Offering Nourishment - edible mushroom.",
            "fun_fact": "Champignon mushrooms are one of the most cultivated mushrooms worldwide and can be grown year-round indoors.",
            "difficulty_level": calc.calculate_difficulty("champignon", "An edible mushroom", "From French champignon"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "championship",
            "definition": "A competition to determine the best in a particular sport or activity; the position of being a champion.",
            "pronunciation": "/ˈtʃæmpiənˌʃɪp/",
            "pronunciation_audio_url": "",
            "example_sentence": "The team trained for months to prepare for the national _____.",
            "etymology": "From champion + -ship",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHAMPIONSHIP: Competitive Heroes And Masters Prove Individual Outstanding Notable Skills Having Incredible Performance - top competition.",
            "fun_fact": "The first modern championship format was developed for chess in the 19th century and became the model for many sports.",
            "difficulty_level": calc.calculate_difficulty("championship", "A competition to determine the best", "From champion + -ship"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "champs",
            "definition": "Short for champions; winners of a competition or contest; also means 'to bite or chew noisily.'",
            "pronunciation": "/tʃæmps/",
            "pronunciation_audio_url": "",
            "example_sentence": "The defending _____ returned to compete for another title in the annual tournament.",
            "etymology": "From champion (shortened) or from champ 'to bite'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHAMPS: Champions Holding And Maintaining Premier Status - winners or chewing action.",
            "fun_fact": "The phrase 'champing at the bit' comes from horses chewing on their bits when eager to move forward.",
            "difficulty_level": calc.calculate_difficulty("champs", "Champions or chewing action", "From champion or champ"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chancellor",
            "definition": "A senior government official; the head of a university; a high-ranking judicial officer.",
            "pronunciation": "/ˈtʃænsələr/",
            "pronunciation_audio_url": "",
            "example_sentence": "The university _____ addressed the graduating class during the commencement ceremony.",
            "etymology": "From Old French chancelier, from Late Latin cancellarius 'doorkeeper'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHANCELLOR: Chief Administrator Notably Controlling Educational Leadership Or Responsibility - high government or university official.",
            "fun_fact": "The German Chancellor is the head of government, while the British Chancellor of the Exchequer manages the nation's finances.",
            "difficulty_level": calc.calculate_difficulty("chancellor", "A high government or university official", "From Late Latin cancellarius"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chances",
            "definition": "Plural of chance; opportunities or possibilities; the likelihood of something happening.",
            "pronunciation": "/ˈtʃænsɪz/",
            "pronunciation_audio_url": "",
            "example_sentence": "There are good _____ that the weather will improve by tomorrow afternoon.",
            "etymology": "From chance + -s, from Old French cheance 'falling out'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHANCES: Circumstances Having And Naturally Creating Expected Situations - opportunities or probabilities.",
            "fun_fact": "The phrase 'taking chances' originally referred to gambling, where outcomes depend on random events.",
            "difficulty_level": calc.calculate_difficulty("chances", "Opportunities or probabilities", "From Old French cheance + -s"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chandleries",
            "definition": "Shops that sell equipment and supplies for ships; businesses dealing in candles and related goods.",
            "pronunciation": "/ˈtʃændləriz/",
            "pronunciation_audio_url": "",
            "example_sentence": "The harbor was lined with _____ selling rope, anchors, and other maritime supplies.",
            "etymology": "From chandler + -ies, from Old French chandelier 'candle maker'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHANDLERIES: Candle Hardware And Nautical Dealers Likely Equipment Retailers In Emergent Supplies - maritime supply shops.",
            "fun_fact": "Traditional chandleries evolved from candle-making shops to become essential suppliers for sailing ships and boats.",
            "difficulty_level": calc.calculate_difficulty("chandleries", "Maritime supply shops", "From Old French chandelier + -ies"),
            "source_difficulty": "Two Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "change",
            "definition": "To make or become different; to replace something with something else; coins of small denomination.",
            "pronunciation": "/tʃeɪndʒ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The company decided to _____ its marketing strategy to reach younger customers.",
            "etymology": "From Old French changier, from Latin cambiare 'to exchange'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHANGE: Converting Habits And New Growth Eventually - to alter or modify.",
            "fun_fact": "The phrase 'change of heart' dates back to biblical times and originally meant a spiritual transformation.",
            "difficulty_level": calc.calculate_difficulty("change", "To make different", "From Latin cambiare"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "changes",
            "definition": "Third person singular of change; modifications or alterations; different forms or versions.",
            "pronunciation": "/ˈtʃeɪndʒɪz/",
            "pronunciation_audio_url": "",
            "example_sentence": "The new software _____ improved the system's efficiency and user experience.",
            "etymology": "From change + -s",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHANGES: Converting Habits And New Growth Eventually Systematically - modifications or alterations.",
            "fun_fact": "David Bowie's song 'Changes' became an anthem for embracing personal transformation and growth.",
            "difficulty_level": calc.calculate_difficulty("changes", "Modifications or alterations", "From change + -s"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "changing",
            "definition": "Present participle of change; in the process of becoming different; modifying or altering.",
            "pronunciation": "/ˈtʃeɪndʒɪŋ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ seasons brought new colors to the landscape every few months.",
            "etymology": "From change + -ing",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHANGING: Converting Habits And New Growth In Natural Gradations - in process of becoming different.",
            "fun_fact": "Climate change refers to long-term shifts in global weather patterns, primarily caused by human activities.",
            "difficulty_level": calc.calculate_difficulty("changing", "Becoming different", "From change + -ing"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "channel",
            "definition": "A waterway connecting two larger bodies of water; a television or radio frequency; a means of communication.",
            "pronunciation": "/ˈtʃænəl/",
            "pronunciation_audio_url": "",
            "example_sentence": "The narrow _____ between the islands required careful navigation due to strong currents.",
            "etymology": "From Old French chanel, from Latin canalis 'pipe, groove'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHANNEL: Connecting Harbors And Natural Networks Establishing Links - waterway or communication path.",
            "fun_fact": "The English Channel is only 21 miles wide at its narrowest point between England and France.",
            "difficulty_level": calc.calculate_difficulty("channel", "A waterway or communication path", "From Latin canalis"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chanoyu",
            "definition": "The Japanese tea ceremony; a traditional ritual of preparing and serving tea with emphasis on aesthetics and mindfulness.",
            "pronunciation": "/ˈtʃɑnoʊju/",
            "pronunciation_audio_url": "",
            "example_sentence": "The master taught the subtle movements and philosophy behind the art of _____.",
            "etymology": "From Japanese chanoyu, from cha 'tea' + no 'of' + yu 'hot water'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHANOYU: Ceremonial Harmony And Natural Oriental Yielding Understanding - Japanese tea ceremony.",
            "fun_fact": "Chanoyu emphasizes four principles: harmony, respect, purity, and tranquility, reflecting Zen Buddhist philosophy.",
            "difficulty_level": calc.calculate_difficulty("chanoyu", "Japanese tea ceremony", "From Japanese cha + no + yu"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chanteuse",
            "definition": "A female singer, especially one who performs in nightclubs or cabarets with a sophisticated style.",
            "pronunciation": "/ʃænˈtuz/",
            "pronunciation_audio_url": "",
            "example_sentence": "The elegant _____ captivated the audience with her sultry voice and graceful stage presence.",
            "etymology": "From French chanteuse, feminine of chanteur 'singer'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHANTEUSE: Captivating Harmonious And Notable Talented Entertaining Unique Singer Elegant - female nightclub singer.",
            "fun_fact": "Famous chanteuses like Édith Piaf and Billie Holiday helped define the sophisticated cabaret singing style.",
            "difficulty_level": calc.calculate_difficulty("chanteuse", "A female nightclub singer", "From French chanteuse"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chantilly",
            "definition": "A type of delicate lace; whipped cream sweetened and flavored, often used in desserts.",
            "pronunciation": "/ʃænˈtɪli/",
            "pronunciation_audio_url": "",
            "example_sentence": "The wedding dress featured intricate _____ lace that had been handmade by French artisans.",
            "etymology": "Named after Chantilly, France, where the lace was originally made",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHANTILLY: Charming Harmonious And Notable Textiles In Lovely Lacy Yearning - delicate French lace.",
            "fun_fact": "Chantilly lace reached its peak popularity in the 18th and 19th centuries and was favored by European royalty.",
            "difficulty_level": calc.calculate_difficulty("chantilly", "A type of delicate lace", "Named after Chantilly, France"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chaotic",
            "definition": "In a state of complete confusion or disorder; unpredictable and uncontrolled.",
            "pronunciation": "/keɪˈɑtɪk/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ traffic during rush hour made it nearly impossible to arrive on time.",
            "etymology": "From Greek khaotikos, from khaos 'void, chasm'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHAOTIC: Completely Hectic And Obviously Totally Irregular Confusion - completely disordered.",
            "fun_fact": "Chaos theory studies how small changes in initial conditions can lead to dramatically different outcomes in complex systems.",
            "difficulty_level": calc.calculate_difficulty("chaotic", "Completely disordered", "From Greek khaotikos"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chaperonage",
            "definition": "The act or practice of chaperoning; supervision of young people by an older, responsible person.",
            "pronunciation": "/ˈʃæpəroʊnɪdʒ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The school dance required proper _____ to ensure appropriate behavior among students.",
            "etymology": "From chaperone + -age, from French chaperon 'hood'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHAPERONAGE: Careful Handling And Protection Ensuring Respectful Oversight Nurturing And Guiding Everyone - supervision of young people.",
            "fun_fact": "The term originally referred to a hood worn by women, then to an older woman who accompanied younger ones for protection.",
            "difficulty_level": calc.calculate_difficulty("chaperonage", "The act of chaperoning", "From French chaperon + -age"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chaplain",
            "definition": "A clergyman attached to a chapel, military unit, institution, or private household for religious services.",
            "pronunciation": "/ˈtʃæplɪn/",
            "pronunciation_audio_url": "",
            "example_sentence": "The military _____ provided spiritual comfort and guidance to soldiers during deployment.",
            "etymology": "From Old French chapelain, from Medieval Latin cappellanus",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHAPLAIN: Clerical Helper And Pastor Leading And Inspiring Naturally - institutional clergyman.",
            "fun_fact": "Military chaplains are non-combatants protected under the Geneva Conventions and serve soldiers of all faiths.",
            "difficulty_level": calc.calculate_difficulty("chaplain", "An institutional clergyman", "From Medieval Latin cappellanus"),
            "source_difficulty": "Two Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "characteristic",
            "definition": "A distinguishing feature or quality; typical of a particular person, place, or thing.",
            "pronunciation": "/ˌkærɪktəˈrɪstɪk/",
            "pronunciation_audio_url": "",
            "example_sentence": "Her optimistic outlook was a defining _____ that everyone admired.",
            "etymology": "From Greek kharaktēristikos, from kharaktēr 'character'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHARACTERISTIC: Common Habits And Recognizable Attributes Created Through Everyone's Routine Interactions Shaping Their Individual Character - distinguishing feature.",
            "fun_fact": "In mathematics, characteristic functions help define probability distributions and are fundamental to statistical analysis.",
            "difficulty_level": calc.calculate_difficulty("characteristic", "A distinguishing feature", "From Greek kharaktēristikos"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "characterized",
            "definition": "Past tense of characterize; described the distinctive features of; marked by particular qualities.",
            "pronunciation": "/ˈkærɪktəˌraɪzd/",
            "pronunciation_audio_url": "",
            "example_sentence": "The period was _____ by rapid technological advancement and social change.",
            "etymology": "From characterize + -d, from Greek kharaktēr",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHARACTERIZED: Common Habits And Recognizable Attributes Created Through Everyone's Routine Interactions Systematically Establishing Distinguishing features - described distinctive features.",
            "fun_fact": "Historical periods are often characterized by their dominant technologies, like the Stone Age, Bronze Age, and Information Age.",
            "difficulty_level": calc.calculate_difficulty("characterized", "Described distinctive features", "From Greek kharaktēr + -ized"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "charade",
            "definition": "A word-guessing game using gestures; an absurd pretense intended to hide the truth.",
            "pronunciation": "/ʃəˈreɪd/",
            "pronunciation_audio_url": "",
            "example_sentence": "The elaborate apology was just a _____ to avoid taking real responsibility.",
            "etymology": "From French charade, from Provençal charrado 'chat, chatter'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHARADE: Concealing Habits And Reality And Deceptive Entertainment - guessing game or pretense.",
            "fun_fact": "The party game charades became popular in 18th-century France and spread throughout Europe as salon entertainment.",
            "difficulty_level": calc.calculate_difficulty("charade", "A guessing game or pretense", "From Provençal charrado"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "charcuterie",
            "definition": "The art of preparing and preserving meat products; a shop selling such products; an assortment of cured meats.",
            "pronunciation": "/ʃɑrˈkutəri/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ board featured an elegant selection of cured meats, cheeses, and artisanal crackers.",
            "etymology": "From French charcuterie, from chair 'flesh' + cuit 'cooked'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHARCUTERIE: Carefully Handled And Refined Cuisine Using Traditional European Restaurant Including Excellence - cured meat preparation.",
            "fun_fact": "Traditional charcuterie techniques were developed before refrigeration as ways to preserve meat for long periods.",
            "difficulty_level": calc.calculate_difficulty("charcuterie", "The art of preserving meat", "From French chair + cuit"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "charge",
            "definition": "To rush forward in attack; to demand payment; to fill with electrical energy; an accusation or responsibility.",
            "pronunciation": "/tʃɑrdʒ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The cavalry prepared to _____ across the battlefield at dawn.",
            "etymology": "From Old French chargier, from Late Latin carricare 'to load'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHARGE: Cavalry Horses And Riders Galloping Everywhere - to rush forward or load with energy.",
            "fun_fact": "The famous Charge of the Light Brigade during the Crimean War became a symbol of courage in the face of overwhelming odds.",
            "difficulty_level": calc.calculate_difficulty("charge", "To rush forward or demand payment", "From Late Latin carricare"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "charioteer",
            "definition": "A person who drives a chariot, especially in ancient warfare or racing competitions.",
            "pronunciation": "/ˌtʃæriəˈtɪr/",
            "pronunciation_audio_url": "",
            "example_sentence": "The skilled _____ guided his horses through the tight turns of the Roman circus.",
            "etymology": "From chariot + -eer, from Old French chariot",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHARIOTEER: Chariot Handler And Racer In Olympic Tournaments Expertly Executing Racing - chariot driver.",
            "fun_fact": "Chariot racing was one of the most popular sports in ancient Rome, with successful charioteers becoming celebrities.",
            "difficulty_level": calc.calculate_difficulty("charioteer", "A chariot driver", "From chariot + -eer"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "charismatic",
            "definition": "Having a compelling charm that inspires devotion in others; possessing a divinely conferred power or talent.",
            "pronunciation": "/ˌkærɪzˈmætɪk/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ speaker captivated the audience with his passionate delivery and compelling message.",
            "etymology": "From Greek kharismatikos, from kharisma 'divine gift'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHARISMATIC: Compelling Harmony And Radiance Inspiring Strong Magnetic Appeal Together In Character - having compelling charm.",
            "fun_fact": "The term was popularized by sociologist Max Weber to describe leaders who inspire through personal magnetism rather than traditional authority.",
            "difficulty_level": calc.calculate_difficulty("charismatic", "Having compelling charm", "From Greek kharismatikos"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "charitable",
            "definition": "Generous in giving help to those in need; showing kindness and tolerance toward others.",
            "pronunciation": "/ˈtʃærɪtəbəl/",
            "pronunciation_audio_url": "",
            "example_sentence": "Her _____ nature led her to volunteer at the local food bank every weekend.",
            "etymology": "From charity + -able, from Latin caritas 'love, affection'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHARITABLE: Caring Habits And Regularly Inspiring Thoughtful And Benevolent Loving Everyone - generous and kind.",
            "fun_fact": "The modern concept of charitable organizations as tax-exempt entities developed in the 19th century in Britain and America.",
            "difficulty_level": calc.calculate_difficulty("charitable", "Generous and kind", "From Latin caritas + -able"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "charon",
            "definition": "In Greek mythology, the ferryman who carries souls of the dead across the river Styx to Hades.",
            "pronunciation": "/ˈkɛrən/",
            "pronunciation_audio_url": "",
            "example_sentence": "According to ancient myth, _____ required payment of a coin to transport souls to the underworld.",
            "etymology": "From Greek Kharōn, possibly meaning 'fierce brightness'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHARON: Crossing Hades And River Of No return - mythological ferryman.",
            "fun_fact": "The tradition of placing coins on the eyes of the dead comes from the practice of paying Charon for passage to the afterlife.",
            "difficulty_level": calc.calculate_difficulty("charon", "Mythological ferryman", "From Greek Kharōn"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "charred",
            "definition": "Burned or scorched to create a blackened surface; partially burned or carbonized.",
            "pronunciation": "/tʃɑrd/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ remains of the wooden beam showed how intense the fire had been.",
            "etymology": "From char + -ed, of uncertain origin, possibly from charcoal",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHARRED: Carbonized Heated And Reduced Remains Eventually Darkened - burned and blackened.",
            "fun_fact": "Charring food creates the Maillard reaction, which produces complex flavors and aromas prized in cooking.",
            "difficulty_level": calc.calculate_difficulty("charred", "Burned and blackened", "From char + -ed"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chart",
            "definition": "A map or graph showing information; to plan or map out a course of action.",
            "pronunciation": "/tʃɑrt/",
            "pronunciation_audio_url": "",
            "example_sentence": "The navigation _____ showed all the underwater hazards in the coastal waters.",
            "etymology": "From Old French charte, from Latin charta 'paper, map'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHART: Careful Helpful And Recorded Territory - map or graph.",
            "fun_fact": "Sea charts have been essential for navigation for centuries, with the oldest known chart dating back to the 13th century.",
            "difficulty_level": calc.calculate_difficulty("chart", "A map or graph", "From Latin charta"),
            "source_difficulty": "Two Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chase",
            "definition": "To pursue someone or something in order to catch them; to follow rapidly or persistently.",
            "pronunciation": "/tʃeɪs/",
            "pronunciation_audio_url": "",
            "example_sentence": "The dog began to _____ the ball across the yard as soon as it was thrown.",
            "etymology": "From Old French chacier, from Latin captare 'to catch'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHASE: Catch Hurrying And Speeding Everywhere - to pursue rapidly.",
            "fun_fact": "The phrase 'wild goose chase' comes from a 16th-century horse racing game where riders followed a lead horse in formation.",
            "difficulty_level": calc.calculate_difficulty("chase", "To pursue rapidly", "From Latin captare"),
            "source_difficulty": "Two Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chasm",
            "definition": "A deep crack or opening in the earth's surface; a profound difference between people, viewpoints, or situations.",
            "pronunciation": "/ˈkæzəm/",
            "pronunciation_audio_url": "",
            "example_sentence": "The earthquake created a wide _____ that split the road completely in half.",
            "etymology": "From Greek khasma, from khainein 'to gape, yawn'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHASM: Crack Having And Splitting Material - deep opening or gap.",
            "fun_fact": "The Grand Canyon is one of the world's most famous chasms, carved by the Colorado River over millions of years.",
            "difficulty_level": calc.calculate_difficulty("chasm", "A deep opening or gap", "From Greek khasma"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "chastise",
            "definition": "To rebuke or reprimand severely; to punish or discipline someone for wrongdoing.",
            "pronunciation": "/tʃæˈstaɪz/",
            "pronunciation_audio_url": "",
            "example_sentence": "The teacher chose to _____ the student privately rather than embarrass him in front of the class.",
            "etymology": "From Old French chastier, from Latin castigare 'to correct'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CHASTISE: Correcting Habits And Stopping Trouble In Serious Education - to rebuke severely.",
            "fun_fact": "The word originally implied correction for improvement, reflecting the educational purpose of discipline in medieval times.",
            "difficulty_level": calc.calculate_difficulty("chastise", "To rebuke severely", "From Latin castigare"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        }
    ]
    
    # Create output CSV
    output_data = []
    combined_word_errors = []
    
    for _, row in df.iterrows():
        word = row['word'].strip()
        
        # Check for combined word errors
        if word in combined_errors:
            combined_word_errors.append({
                'word': word,
                'error_type': 'combined_word',
                'reason': 'Contains multiple words joined together from PDF extraction error'
            })
            continue
            
        # Find word data
        word_info = next((item for item in word_data if item['word'] == word), None)
        if word_info:
            output_data.append(word_info)
    
    # Write to CSV
    fieldnames = [
        'word', 'definition', 'pronunciation', 'pronunciation_audio_url',
        'example_sentence', 'etymology', 'etymology_source', 'memory_tip',
        'fun_fact', 'difficulty_level', 'source_difficulty', 'source', 'source_url'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_data)
    
    print(f"Batch 032 processing complete!")
    print(f"Processed: {len(df)}/50 words")
    print(f"Combined word errors flagged: {len(combined_word_errors)}")
    print(f"Valid spelling words: {len(output_data)}")
    
    if combined_word_errors:
        print(f"\nCombined word errors found:")
        for error in combined_word_errors:
            print(f"  - {error['word']}")

if __name__ == "__main__":
    process_batch_032()