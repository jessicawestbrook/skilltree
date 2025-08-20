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

def process_batch_030():
    # Read the batch file
    input_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_030_words.csv"
    output_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_030_processed.csv"
    
    # Read the input file
    df = pd.read_csv(input_file)
    
    # Initialize difficulty calculator
    calc = DifficultyCalculator()
    
    # Combined word errors detected
    combined_errors = ["cartoondough", "castigateveered", "cathodecatnap", "cathodecattalo"]
    
    # Create comprehensive word data
    word_data = [
        {
            "word": "carte",
            "definition": "A menu, especially in a restaurant; or a map or chart.",
            "pronunciation": "/kɑrt/",
            "pronunciation_audio_url": "",
            "example_sentence": "The waiter presented the evening's _____ featuring seasonal specialties and wine pairings.",
            "etymology": "From French carte, from Latin charta 'paper'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARTE: Classic And Restaurant Table Entertainment - menu or map.",
            "fun_fact": "The phrase 'à la carte' literally means 'according to the card' and refers to ordering individual dishes rather than a set meal.",
            "difficulty_level": calc.calculate_difficulty("carte", "A menu or map", "From French carte"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "carthusian",
            "definition": "A member of a strict Roman Catholic monastic order founded in 1084, known for their contemplative and austere lifestyle.",
            "pronunciation": "/kɑrˈθuziən/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ monks lived in silence and solitude, dedicating their lives to prayer and meditation.",
            "etymology": "From Chartreuse, the location of their first monastery in France",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARTHUSIAN: Catholic And Religious Traditional Hermits Upholding Strict Internal Ascetic Norms - monastic order.",
            "fun_fact": "Carthusian monks are famous for creating Chartreuse liqueur, one of the few remaining monastery-produced spirits.",
            "difficulty_level": calc.calculate_difficulty("carthusian", "A member of a monastic order", "From Chartreuse location"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cartilage",
            "definition": "A firm, flexible connective tissue found in various parts of the body, including joints, nose, and ears.",
            "pronunciation": "/ˈkɑrtəlɪdʒ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The surgeon explained that the damaged _____ in her knee would need to be repaired arthroscopically.",
            "etymology": "From Latin cartilago, from unknown origin",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARTILAGE: Connective And Resilient Tissue In Limbs And Generating Elasticity - flexible body tissue.",
            "fun_fact": "Shark skeletons are made entirely of cartilage rather than bone, making them lighter and more flexible for swimming.",
            "difficulty_level": calc.calculate_difficulty("cartilage", "A firm, flexible connective tissue", "From Latin cartilago"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cartoon",
            "definition": "A simple drawing showing features in a humorous or exaggerated way; or an animated film or TV show.",
            "pronunciation": "/kɑrˈtun/",
            "pronunciation_audio_url": "",
            "example_sentence": "The political _____ in the newspaper cleverly satirized the current election campaign.",
            "etymology": "From Italian cartone 'pasteboard', from carta 'paper'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARTOON: Comic And Ridiculous Theatrical Outlined Outlined Narrative - humorous drawing.",
            "fun_fact": "The first animated cartoon was created in 1906 by J. Stuart Blackton, called 'Humorous Phases of Funny Faces.'",
            "difficulty_level": calc.calculate_difficulty("cartoon", "A humorous drawing or animation", "From Italian cartone"),
            "source_difficulty": "Two Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cartouches",
            "definition": "Oval frames containing Egyptian hieroglyphic names of royalty; or ornamental scrollwork designs in architecture.",
            "pronunciation": "/kɑrˈtuʃɪz/",
            "pronunciation_audio_url": "",
            "example_sentence": "The archaeologist identified several royal _____ on the temple wall, indicating the presence of pharaonic inscriptions.",
            "etymology": "From French cartouche, from Italian cartoccio 'roll of paper'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARTOUCHES: Containing And Recording Titles Of Unique Ceremonial Hieroglyphic Egyptian Symbols - Egyptian name frames.",
            "fun_fact": "The Rosetta Stone's cartouches helped scholars decode hieroglyphics by providing known royal names in multiple scripts.",
            "difficulty_level": calc.calculate_difficulty("cartouches", "Oval frames for Egyptian royal names", "From French cartouche"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "caryatid",
            "definition": "A sculpted female figure serving as an architectural support or column, typically in classical Greek architecture.",
            "pronunciation": "/ˌkæriˈætɪd/",
            "pronunciation_audio_url": "",
            "example_sentence": "The ancient temple featured six elegant _____ figures supporting the roof with graceful poses.",
            "etymology": "From Greek karyatides, referring to maidens from Karyai",
            "etymology_source": "Claude",
            "memory_tip": "Remember CARYATID: Classical Architecture Requires Young And Talented Individual Decorative figures - female column.",
            "fun_fact": "The most famous caryatids are those from the Erechtheion on the Acropolis in Athens, dating to around 420 BCE.",
            "difficulty_level": calc.calculate_difficulty("caryatid", "A sculpted female figure as architectural support", "From Greek karyatides"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "casa",
            "definition": "Spanish and Italian word for house; used in English to refer to a dwelling, especially in southwestern United States.",
            "pronunciation": "/ˈkɑsə/",
            "pronunciation_audio_url": "",
            "example_sentence": "Their vacation _____ in Mexico featured traditional tile work and a beautiful courtyard garden.",
            "etymology": "From Spanish and Italian casa, from Latin casa 'cottage'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASA: Comfortable And Spacious Accommodation - Spanish/Italian house.",
            "fun_fact": "The word 'casa' appears in many place names in the southwestern United States, reflecting Spanish colonial history.",
            "difficulty_level": calc.calculate_difficulty("casa", "Spanish/Italian word for house", "From Latin casa"),
            "source_difficulty": "Two Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cascabel",
            "definition": "A small, round, dried chili pepper with a distinctive rattling sound when shaken; or a type of small cannon.",
            "pronunciation": "/ˌkæskəˈbɛl/",
            "pronunciation_audio_url": "",
            "example_sentence": "The chef used dried _____ peppers to add a smoky, nutty flavor to the traditional Mexican sauce.",
            "etymology": "From Spanish cascabel 'little bell', from cascabe 'rattle'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASCABEL: Chili And Spicy Capsicum Always Brings Excellent Lively flavor - rattling pepper.",
            "fun_fact": "Cascabel peppers are named for their resemblance to sleigh bells and the rattling sound their seeds make when dried.",
            "difficulty_level": calc.calculate_difficulty("cascabel", "A type of chili pepper", "From Spanish cascabel"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cascade",
            "definition": "A waterfall, especially one in a series; or something that falls, rushes, or occurs in abundance.",
            "pronunciation": "/kæsˈkeɪd/",
            "pronunciation_audio_url": "",
            "example_sentence": "The mountain stream formed a beautiful _____ as it tumbled down the rocky cliff face.",
            "etymology": "From French cascade, from Italian cascata, from cascare 'to fall'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASCADE: Constantly And Steadily Cascading And Descending Elegantly - waterfall or flowing sequence.",
            "fun_fact": "In computing, a 'cascade' refers to a series of operations where each one triggers the next, like in CSS styling.",
            "difficulty_level": calc.calculate_difficulty("cascade", "A waterfall or flowing sequence", "From French cascade"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cases",
            "definition": "Plural of case; instances, examples, or occurrences of something; containers or coverings.",
            "pronunciation": "/ˈkeɪsɪz/",
            "pronunciation_audio_url": "",
            "example_sentence": "The detective reviewed several _____ of similar crimes to identify a pattern in the suspect's behavior.",
            "etymology": "From case + -s, from Latin casus 'fall, occurrence'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASES: Circumstances And Situations Everyone Studies - instances or containers.",
            "fun_fact": "In legal terminology, landmark cases often establish precedents that influence future court decisions for decades.",
            "difficulty_level": calc.calculate_difficulty("cases", "Instances or containers", "From Latin casus"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cashier",
            "definition": "A person who handles payments and receipts in a store, bank, or other business establishment.",
            "pronunciation": "/kæˈʃɪr/",
            "pronunciation_audio_url": "",
            "example_sentence": "The friendly _____ at the grocery store helped bag the groceries and wished everyone a pleasant day.",
            "etymology": "From French caissier, from caisse 'money box'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASHIER: Customer And Store Handler In Exchange Routines - payment processor.",
            "fun_fact": "The first mechanical cash register was invented in 1879 by James Ritty to prevent employee theft in his saloon.",
            "difficulty_level": calc.calculate_difficulty("cashier", "A person who handles payments", "From French caissier"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "casimir",
            "definition": "A type of fine, lightweight wool fabric with a twilled weave, used for making high-quality garments.",
            "pronunciation": "/ˈkæzɪˌmɪr/",
            "pronunciation_audio_url": "",
            "example_sentence": "The tailor chose _____ fabric for the elegant coat, appreciating its soft texture and durability.",
            "etymology": "Named after Kashmir, the region famous for fine wool textiles",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASIMIR: Classic And Soft Material In Rich textures - fine wool fabric.",
            "fun_fact": "Casimir fabric was highly prized in 18th and 19th century Europe as a luxury material for formal wear.",
            "difficulty_level": calc.calculate_difficulty("casimir", "A type of fine wool fabric", "Named after Kashmir"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "casino",
            "definition": "A facility where gambling games are played; a building or room used for gambling and entertainment.",
            "pronunciation": "/kəˈsinoʊ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The Las Vegas _____ featured slot machines, card tables, and elaborate shows for tourist entertainment.",
            "etymology": "From Italian casino, diminutive of casa 'house'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASINO: Chances And Stakes In Numbers Operations - gambling establishment.",
            "fun_fact": "The first legal casino in America was opened in Nevada in 1931, leading to Las Vegas becoming the gambling capital.",
            "difficulty_level": calc.calculate_difficulty("casino", "A gambling establishment", "From Italian casino"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cassandra",
            "definition": "In Greek mythology, a Trojan princess cursed to prophesy truly but never be believed; someone who predicts disaster.",
            "pronunciation": "/kəˈsændrə/",
            "pronunciation_audio_url": "",
            "example_sentence": "The economist was dismissed as a _____ when she warned about the impending financial crisis.",
            "etymology": "From Greek Kassandra, a mythological figure",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASSANDRA: Correctly Anticipating Situations Seen As Negative Delivers Rejected Accurate predictions - unheeded prophet.",
            "fun_fact": "The term 'Cassandra complex' describes the psychological phenomenon of being unable to convince others of impending disaster.",
            "difficulty_level": calc.calculate_difficulty("cassandra", "A prophet whose warnings are ignored", "From Greek Kassandra"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "casserole",
            "definition": "A dish cooked slowly in an oven, typically containing meat and vegetables; or the deep dish used for cooking such meals.",
            "pronunciation": "/ˈkæsəˌroʊl/",
            "pronunciation_audio_url": "",
            "example_sentence": "Grandmother's chicken and rice _____ was a family favorite during cold winter evenings.",
            "etymology": "From French casserole, from Provençal cassa 'ladle'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASSEROLE: Cooked And Slow Simmered Excellent Recipe Over Low Eatables - baked dish.",
            "fun_fact": "Casseroles became popular in America during the Great Depression as a way to stretch ingredients and feed families economically.",
            "difficulty_level": calc.calculate_difficulty("casserole", "A slow-cooked oven dish", "From French casserole"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cassock",
            "definition": "A full-length garment worn by clergy and church officials, typically black and reaching to the feet.",
            "pronunciation": "/ˈkæsək/",
            "pronunciation_audio_url": "",
            "example_sentence": "The priest wore his traditional black _____ during the formal church ceremony.",
            "etymology": "From French casaque, possibly from Turkish kazak 'vagabond'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASSOCK: Clerical And Sacred Spiritual Official Ceremonial Kostume - religious robe.",
            "fun_fact": "The color of a cassock often indicates the wearer's rank: black for priests, purple for bishops, red for cardinals.",
            "difficulty_level": calc.calculate_difficulty("cassock", "A full-length clerical garment", "From French casaque"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cast",
            "definition": "To throw or hurl something; to shape metal or other material in a mold; or the actors in a play or movie.",
            "pronunciation": "/kæst/",
            "pronunciation_audio_url": "",
            "example_sentence": "The fisherman was able to _____ his line perfectly into the center of the quiet pond.",
            "etymology": "From Old Norse kasta 'to throw'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAST: Carefully Aimed Skillful Throw - to throw or shape.",
            "fun_fact": "In theater, the 'cast' originally referred to the act of 'casting' actors into their roles, like casting metal into a mold.",
            "difficulty_level": calc.calculate_difficulty("cast", "To throw or shape", "From Old Norse kasta"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "castalia",
            "definition": "In Greek mythology, a sacred spring on Mount Parnassus, sacred to Apollo and the Muses; source of poetic inspiration.",
            "pronunciation": "/kæˈsteɪliə/",
            "pronunciation_audio_url": "",
            "example_sentence": "The poet sought inspiration at _____, hoping the sacred waters would enhance her creative abilities.",
            "etymology": "From Greek Kastalia, the name of a mythological nymph transformed into a spring",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASTALIA: Creative And Sacred Tale About Legendary Inspiring Apollo - mythological spring.",
            "fun_fact": "Castalia was considered the source of inspiration for the Oracle at Delphi and for poets seeking divine creativity.",
            "difficulty_level": calc.calculate_difficulty("castalia", "A sacred spring in Greek mythology", "From Greek Kastalia"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "castellated",
            "definition": "Having turrets and battlements like a castle; built with defensive architectural features resembling medieval fortifications.",
            "pronunciation": "/ˈkæstəˌleɪtɪd/",
            "pronunciation_audio_url": "",
            "example_sentence": "The Victorian mansion featured a _____ roofline that gave it the appearance of a medieval fortress.",
            "etymology": "From Latin castellum 'fortress' + -ated",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASTELLATED: Castle And Structure Themed Elaborate Luxury Lofty Architecture Together Elaborate Design - castle-like.",
            "fun_fact": "Many 19th-century buildings adopted castellated architecture to evoke romantic notions of medieval chivalry and nobility.",
            "difficulty_level": calc.calculate_difficulty("castellated", "Having castle-like features", "From Latin castellum + -ated"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "castigate",
            "definition": "To reprimand or criticize someone severely; to punish or rebuke harshly for wrongdoing.",
            "pronunciation": "/ˈkæstɪˌɡeɪt/",
            "pronunciation_audio_url": "",
            "example_sentence": "The teacher chose to _____ the students privately rather than embarrass them in front of their classmates.",
            "etymology": "From Latin castigatus, from castigare 'to correct, punish'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASTIGATE: Critiquing And Severely Telling Individual Groups About Their Errors - harsh criticism.",
            "fun_fact": "The word originally implied correction and improvement, not just punishment, reflecting the educational purpose of discipline.",
            "difficulty_level": calc.calculate_difficulty("castigate", "To reprimand severely", "From Latin castigare"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "castilian",
            "definition": "Relating to Castile, a historical region of Spain; or the standard form of Spanish language originating from this region.",
            "pronunciation": "/kæˈstɪliən/",
            "pronunciation_audio_url": "",
            "example_sentence": "The language school emphasized proper _____ pronunciation to help students learn standard Spanish.",
            "etymology": "From Castile, the historical Spanish kingdom + -ian",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASTILIAN: Central And Standard Traditional Imperial Language In Authentic Notable Spanish - Spanish from Castile.",
            "fun_fact": "Castilian Spanish became the standard form of the language because the Kingdom of Castile unified much of Spain.",
            "difficulty_level": calc.calculate_difficulty("castilian", "Relating to Castile or standard Spanish", "From Castile + -ian"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "castle",
            "definition": "A large fortified building or complex of buildings, typically from medieval times; a stronghold or fortress.",
            "pronunciation": "/ˈkæsəl/",
            "pronunciation_audio_url": "",
            "example_sentence": "The ancient _____ on the hilltop had served as both a royal residence and a military fortress.",
            "etymology": "From Old English castel, from Latin castellum 'fortress'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASTLE: Commanding And Strong Tall Landmark Establishment - fortified building.",
            "fun_fact": "The largest castle in the world is Prague Castle, covering 70,000 square meters and dating back to the 9th century.",
            "difficulty_level": calc.calculate_difficulty("castle", "A fortified building", "From Latin castellum"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "castor",
            "definition": "A beaver; or castor oil, derived from castor beans and used medicinally; or a small wheel on furniture legs.",
            "pronunciation": "/ˈkæstər/",
            "pronunciation_audio_url": "",
            "example_sentence": "The old medicine cabinet contained a bottle of _____ oil, once commonly used as a home remedy.",
            "etymology": "From Latin castor 'beaver', from Greek kastor",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASTOR: Chemical And Substance Treatment Oil Resource - beaver or medicinal oil.",
            "fun_fact": "Castor oil was once so commonly used as a medicine that 'taking castor oil' became synonymous with unpleasant but necessary treatment.",
            "difficulty_level": calc.calculate_difficulty("castor", "Beaver or medicinal oil", "From Latin castor"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "casualty",
            "definition": "A person killed or injured in a war or accident; a victim of unfortunate circumstances.",
            "pronunciation": "/ˈkæʒuəlti/",
            "pronunciation_audio_url": "",
            "example_sentence": "The first _____ of the storm was the old oak tree that fell across the main road.",
            "etymology": "From Medieval Latin casualitas, from casualis 'by chance'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CASUALTY: Circumstance And Situation Usually Affects Life Through Yield - victim of misfortune.",
            "fun_fact": "The term originally referred to any accident or chance event, before becoming specifically associated with war injuries.",
            "difficulty_level": calc.calculate_difficulty("casualty", "A victim of war or accident", "From Latin casualis"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "catachresis",
            "definition": "The use of a word in a way that is not correct; misuse of language or strained metaphor in rhetoric.",
            "pronunciation": "/ˌkætəˈkrisɪs/",
            "pronunciation_audio_url": "",
            "example_sentence": "The poet's use of _____ created an intentionally jarring effect by combining incompatible metaphors.",
            "etymology": "From Greek katachresis, from katachresthai 'to misuse'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATACHRESIS: Combining And Twisting All Commonly Held Rhetorical Expressions Strangely In Speech - misuse of language.",
            "fun_fact": "Shakespeare often used catachresis deliberately to create striking poetic effects, as in 'take arms against a sea of troubles.'",
            "difficulty_level": calc.calculate_difficulty("catachresis", "Misuse of language or metaphor", "From Greek katachresis"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cataclysmic",
            "definition": "Involving or resulting in large-scale and violent upheaval; extremely disruptive or destructive.",
            "pronunciation": "/ˌkætəˈklɪzmɪk/",
            "pronunciation_audio_url": "",
            "example_sentence": "The asteroid impact had _____ effects on Earth's climate, leading to mass extinctions.",
            "etymology": "From Greek kataklysmos 'deluge' + -ic",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATACLYSMIC: Catastrophic And Totally Altering Climate Leading Yielding Serious Massive Impact Changes - extremely destructive.",
            "fun_fact": "The word originally referred to Noah's flood, but geologists now use it to describe major environmental disasters.",
            "difficulty_level": calc.calculate_difficulty("cataclysmic", "Extremely destructive", "From Greek kataklysmos + -ic"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "catadromous",
            "definition": "Describing fish that live in fresh water but migrate to the ocean to spawn, like eels.",
            "pronunciation": "/kəˈtædrəməs/",
            "pronunciation_audio_url": "",
            "example_sentence": "The American eel is a _____ species that travels thousands of miles to breed in the Sargasso Sea.",
            "etymology": "From Greek kata 'down' + dromos 'running'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATADROMOUS: Certain Aquatic Types Always Descend Rivers Ocean Migration Usually Spawning - fresh to salt water migration.",
            "fun_fact": "This is the opposite of anadromous fish like salmon, which live in salt water but spawn in fresh water.",
            "difficulty_level": calc.calculate_difficulty("catadromous", "Migrating from fresh to salt water to spawn", "From Greek kata + dromos"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "catalepsy",
            "definition": "A medical condition characterized by rigid muscles and fixed posture, often associated with psychiatric disorders.",
            "pronunciation": "/ˈkætəˌlɛpsi/",
            "pronunciation_audio_url": "",
            "example_sentence": "The patient experienced episodes of _____ where she remained motionless for hours at a time.",
            "etymology": "From Greek katalepsis, from katalambanein 'to seize'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATALEPSY: Condition And Total And Long Extended Physical Suspension - rigid muscle condition.",
            "fun_fact": "Catalepsy was once thought to be supernatural possession, but is now understood as a neurological symptom.",
            "difficulty_level": calc.calculate_difficulty("catalepsy", "A condition of rigid muscles", "From Greek katalepsis"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "catalina",
            "definition": "A type of casual women's swimsuit; or referring to Santa Catalina Island off the California coast.",
            "pronunciation": "/ˌkætəˈlinə/",
            "pronunciation_audio_url": "",
            "example_sentence": "She wore a vintage-style _____ swimsuit to the beach party, complete with a modest neckline.",
            "etymology": "Named after Saint Catherine (Santa Catalina in Spanish)",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATALINA: Coastal And Tropical Alternative Ladies In Natural Attire - swimsuit or island name.",
            "fun_fact": "Catalina Island became famous as a Hollywood filming location and vacation destination in the early 20th century.",
            "difficulty_level": calc.calculate_difficulty("catalina", "A swimsuit or island name", "Named after Saint Catherine"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "catalo",
            "definition": "A hybrid animal produced by crossing domestic cattle with American bison, combining traits of both species.",
            "pronunciation": "/ˈkætəˌloʊ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The rancher experimented with raising _____ to produce meat with lower fat content than traditional beef.",
            "etymology": "Blend of cattle + buffalo (bison)",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATALO: Cattle And Trusted Animals Living Optimally - cattle-bison hybrid.",
            "fun_fact": "Catalo breeding was promoted in the early 1900s as a way to combine the hardiness of bison with the docility of cattle.",
            "difficulty_level": calc.calculate_difficulty("catalo", "A cattle-bison hybrid", "Blend of cattle + buffalo"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "catalyst",
            "definition": "A substance that accelerates a chemical reaction without being consumed; a person or thing that precipitates change.",
            "pronunciation": "/ˈkætəlɪst/",
            "pronunciation_audio_url": "",
            "example_sentence": "The new CEO served as a _____ for organizational change, inspiring innovation throughout the company.",
            "etymology": "From Greek katalysis 'dissolution', from katalyein 'to loosen'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATALYST: Chemical And Transformative Agent Leading Yet Stays Unchanged - reaction accelerator.",
            "fun_fact": "Enzymes in living organisms are biological catalysts that speed up essential life processes by millions of times.",
            "difficulty_level": calc.calculate_difficulty("catalyst", "A substance that accelerates reactions", "From Greek katalysis"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cataphora",
            "definition": "A linguistic device where a pronoun or word refers to a later word or phrase in the text.",
            "pronunciation": "/kəˈtæfərə/",
            "pronunciation_audio_url": "",
            "example_sentence": "In the sentence 'When he arrived, John was surprised,' the pronoun 'he' is an example of _____.",
            "etymology": "From Greek kataphora, from kata 'down' + pherein 'to carry'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATAPHORA: Coming And Telling About Phrases Happening Or Referenced Ahead - forward reference.",
            "fun_fact": "Cataphora is the opposite of anaphora, where a word refers back to an earlier word in the text.",
            "difficulty_level": calc.calculate_difficulty("cataphora", "A forward reference in language", "From Greek kataphora"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "catapults",
            "definition": "Ancient siege weapons that launch projectiles; things that propel or launch something forcefully.",
            "pronunciation": "/ˈkætəˌpʌlts/",
            "pronunciation_audio_url": "",
            "example_sentence": "The medieval army used massive _____ to hurl stones at the castle walls during the siege.",
            "etymology": "From Greek katapeltes, from kata 'down' + pallein 'to hurl'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATAPULTS: Clever And Tactical Artillery Projectile Units Launch Through Strength - siege weapons.",
            "fun_fact": "Modern aircraft carriers use steam catapults to launch planes, reaching speeds of 150 mph in just 2 seconds.",
            "difficulty_level": calc.calculate_difficulty("catapults", "Ancient siege weapons", "From Greek katapeltes"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "catarrh",
            "definition": "Inflammation of mucous membranes, especially in the nose and throat, causing congestion and discharge.",
            "pronunciation": "/kəˈtɑr/",
            "pronunciation_audio_url": "",
            "example_sentence": "The doctor diagnosed her persistent cough and congestion as chronic _____.",
            "etymology": "From Greek katarrhous, from kata 'down' + rhein 'to flow'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATARRH: Congestion And Thick Accumulation Restricts Respiratory Health - mucous membrane inflammation.",
            "fun_fact": "The term was once used broadly for any condition involving excessive mucus production, from colds to consumption.",
            "difficulty_level": calc.calculate_difficulty("catarrh", "Inflammation of mucous membranes", "From Greek katarrhous"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "catastrophe",
            "definition": "A sudden disaster or extremely unfortunate event causing great damage or suffering.",
            "pronunciation": "/kəˈtæstrəfi/",
            "pronunciation_audio_url": "",
            "example_sentence": "The earthquake was a natural _____ that affected thousands of families in the region.",
            "etymology": "From Greek katastrophe, from kata 'down' + strephein 'to turn'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATASTROPHE: Calamitous And Terrible And Severe Tragic Ruinous Overwhelming Painful Event - disaster.",
            "fun_fact": "In ancient Greek drama, catastrophe referred to the final part of a tragedy where the plot was resolved.",
            "difficulty_level": calc.calculate_difficulty("catastrophe", "A sudden disaster", "From Greek katastrophe"),
            "source_difficulty": "Two Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "catch",
            "definition": "To capture or seize something in motion; to intercept; to become infected with something.",
            "pronunciation": "/kætʃ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The outfielder made a spectacular diving _____ to prevent the ball from reaching the fence.",
            "etymology": "From Old French cachier 'to hunt, chase'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATCH: Capture And Take Coordinated Hand movement - to seize or intercept.",
            "fun_fact": "The phrase 'catch-22' comes from Joseph Heller's novel, describing a paradoxical or inescapable situation.",
            "difficulty_level": calc.calculate_difficulty("catch", "To capture or seize", "From Old French cachier"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "catching",
            "definition": "Contagious or infectious; likely to spread from person to person; or the act of seizing something.",
            "pronunciation": "/ˈkætʃɪŋ/",
            "pronunciation_audio_url": "",
            "example_sentence": "Her enthusiasm for the project was _____, inspiring everyone on the team to work harder.",
            "etymology": "From catch + -ing",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATCHING: Contagious And Transmissible Characteristics Having Infectious Nature Globally - spreading or seizing.",
            "fun_fact": "Yawning is famously 'catching' - seeing someone yawn can trigger yawning in about 60% of people due to mirror neurons.",
            "difficulty_level": calc.calculate_difficulty("catching", "Contagious or seizing", "From catch + -ing"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "catechism",
            "definition": "A summary of religious doctrine in the form of questions and answers, used for instruction in Christian faith.",
            "pronunciation": "/ˈkætəˌkɪzəm/",
            "pronunciation_audio_url": "",
            "example_sentence": "The children studied the _____ to prepare for their confirmation ceremony at church.",
            "etymology": "From Greek katechismos, from katechein 'to instruct orally'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATECHISM: Church And Teaching Everyone Christian Heritage In Structured Manner - religious instruction.",
            "fun_fact": "Martin Luther's Small Catechism, written in 1529, became one of the most influential religious education texts in history.",
            "difficulty_level": calc.calculate_difficulty("catechism", "A summary of religious doctrine", "From Greek katechismos"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "categorically",
            "definition": "In an absolute or unconditional manner; without exception or qualification; unambiguously.",
            "pronunciation": "/ˌkætəˈɡɔrɪkli/",
            "pronunciation_audio_url": "",
            "example_sentence": "The senator _____ denied any involvement in the scandal, refusing to consider alternative explanations.",
            "etymology": "From categorical + -ly, from Greek kategorikos",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATEGORICALLY: Completely And Totally Explicitly Giving Obvious Responses In Clear And Logical Language Yielding - absolutely.",
            "fun_fact": "Immanuel Kant distinguished between 'categorical' and 'hypothetical' imperatives in his moral philosophy.",
            "difficulty_level": calc.calculate_difficulty("categorically", "In an absolute manner", "From Greek kategorikos + -ly"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "caterpillar",
            "definition": "The larval stage of a butterfly or moth, characterized by a segmented body and multiple legs.",
            "pronunciation": "/ˈkætərˌpɪlər/",
            "pronunciation_audio_url": "",
            "example_sentence": "The hungry _____ munched through several leaves before beginning its transformation into a chrysalis.",
            "etymology": "From Old French chatepelose, literally 'hairy cat'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATERPILLAR: Creature And Tiny Eating Room Preparing Important Larval Life And Reorganization - butterfly larva.",
            "fun_fact": "A caterpillar increases its body weight by thousands of times during its growth period before pupating.",
            "difficulty_level": calc.calculate_difficulty("caterpillar", "The larval stage of a butterfly", "From Old French chatepelose"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cathect",
            "definition": "In psychoanalysis, to invest emotional energy in a person, object, or idea; to form an emotional attachment.",
            "pronunciation": "/kəˈθɛkt/",
            "pronunciation_audio_url": "",
            "example_sentence": "The therapist explained how patients sometimes _____ their feelings onto inanimate objects during treatment.",
            "etymology": "From Greek kathexis, from kata 'down' + hexis 'holding'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATHECT: Concentrating And Thinking Heavily Emotionally Connected To - emotional investment.",
            "fun_fact": "The term was introduced by Freud's translators to explain the concept of libidinal energy attachment in psychoanalytic theory.",
            "difficulty_level": calc.calculate_difficulty("cathect", "To invest emotional energy", "From Greek kathexis"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cathedral",
            "definition": "A large and important Christian church, typically the seat of a bishop; any large or impressive building.",
            "pronunciation": "/kəˈθidrəl/",
            "pronunciation_audio_url": "",
            "example_sentence": "The Gothic _____ took over two centuries to complete, with its soaring spires visible from miles away.",
            "etymology": "From Greek kathedra 'seat', referring to the bishop's throne",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATHEDRAL: Central And Towering Holy Ecclesiastical Distinctive Religious And Liturgical building - large church.",
            "fun_fact": "Notre-Dame de Paris took 182 years to build and inspired Victor Hugo's famous novel 'The Hunchback of Notre-Dame.'",
            "difficulty_level": calc.calculate_difficulty("cathedral", "A large Christian church", "From Greek kathedra"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "catherine",
            "definition": "A feminine given name; also refers to various saints named Catherine in Christian tradition.",
            "pronunciation": "/ˈkæθərɪn/",
            "pronunciation_audio_url": "",
            "example_sentence": "_____ the Great ruled Russia for 34 years and expanded the empire significantly during her reign.",
            "etymology": "From Greek Aikaterine, possibly meaning 'pure'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATHERINE: Classic And Traditional Historical Everyone Remembers In Notable Examples - feminine name.",
            "fun_fact": "Saint Catherine of Alexandria is the patron saint of philosophers, students, and universities.",
            "difficulty_level": calc.calculate_difficulty("catherine", "A feminine given name", "From Greek Aikaterine"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cathode",
            "definition": "The negatively charged electrode in an electrical device; the electrode where reduction occurs in electrolysis.",
            "pronunciation": "/ˈkæθoʊd/",
            "pronunciation_audio_url": "",
            "example_sentence": "The electronics technician replaced the damaged _____ in the vacuum tube radio.",
            "etymology": "From Greek kathodos, from kata 'down' + hodos 'way'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATHODE: Current And Terminal Having Opposite Designation Electrically - negative electrode.",
            "fun_fact": "Cathode ray tubes (CRTs) were the technology behind old television and computer monitors before LCD screens.",
            "difficulty_level": calc.calculate_difficulty("cathode", "The negative electrode", "From Greek kathodos"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "catjang",
            "definition": "A type of cowpea or black-eyed pea, commonly grown in Asia and Africa as a food crop.",
            "pronunciation": "/ˈkætˌdʒæŋ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The farmer planted _____ beans as a protein-rich crop that could improve the soil's nitrogen content.",
            "etymology": "From Malay kacang 'bean'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATJANG: Cultivated Asian Type Just Another Nutritious Growing bean - type of cowpea.",
            "fun_fact": "Catjang beans are drought-resistant and can grow in poor soils, making them valuable in subsistence farming.",
            "difficulty_level": calc.calculate_difficulty("catjang", "A type of cowpea", "From Malay kacang"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "catnap",
            "definition": "A short sleep taken during the day; a brief nap, typically lasting 10-30 minutes.",
            "pronunciation": "/ˈkætˌnæp/",
            "pronunciation_audio_url": "",
            "example_sentence": "After lunch, she took a quick _____ at her desk to recharge for the afternoon meetings.",
            "etymology": "From cat + nap, referring to cats' habit of taking short sleeps",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATNAP: Comfortable And Therapeutic Napping And Peaceful rest - short sleep.",
            "fun_fact": "Research shows that a 20-minute catnap can improve alertness and cognitive performance without causing grogginess.",
            "difficulty_level": calc.calculate_difficulty("catnap", "A short daytime sleep", "From cat + nap"),
            "source_difficulty": "Three Bee",
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
    
    print(f"Batch 030 processing complete!")
    print(f"Processed: {len(df)}/50 words")
    print(f"Combined word errors flagged: {len(combined_word_errors)}")
    print(f"Valid spelling words: {len(output_data)}")
    
    if combined_word_errors:
        print(f"\nCombined word errors found:")
        for error in combined_word_errors:
            print(f"  - {error['word']}")

if __name__ == "__main__":
    process_batch_030()