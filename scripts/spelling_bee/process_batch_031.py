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

def process_batch_031():
    # Read the batch file
    input_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_031_words.csv"
    output_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_031_processed.csv"
    
    # Read the input file
    df = pd.read_csv(input_file)
    
    # Initialize difficulty calculator
    calc = DifficultyCalculator()
    
    # Combined word errors detected
    combined_errors = ["celeryidiosyncratic", "censusstagflation", "centenarymatrimony", "centennialcertiorari"]
    
    # Create comprehensive word data
    word_data = [
        {
            "word": "cats",
            "definition": "Plural of cat; small carnivorous mammals commonly kept as pets, known for their independence and hunting abilities.",
            "pronunciation": "/kæts/",
            "pronunciation_audio_url": "",
            "example_sentence": "The neighborhood _____ gathered around the fish market, hoping for scraps from the daily catch.",
            "etymology": "From Old English catt, from Latin cattus",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATS: Cute And Talented Sleepy animals - plural of cat.",
            "fun_fact": "Cats have been companions to humans for over 9,000 years and were worshipped as gods in ancient Egypt.",
            "difficulty_level": calc.calculate_difficulty("cats", "Plural of cat", "From Old English catt"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cattail",
            "definition": "A tall marsh plant with long, flat leaves and a distinctive brown, cylindrical flower spike resembling a cat's tail.",
            "pronunciation": "/ˈkætˌteɪl/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ plants swayed gently in the breeze along the edge of the pond.",
            "etymology": "From cat + tail, descriptive of the plant's appearance",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATTAIL: Cat Tail Alike In Lakes - marsh plant resembling cat's tail.",
            "fun_fact": "Cattails are sometimes called 'nature's supermarket' because nearly every part of the plant is edible.",
            "difficulty_level": calc.calculate_difficulty("cattail", "A tall marsh plant", "From cat + tail"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cattalo",
            "definition": "A hybrid animal produced by crossing domestic cattle with American bison, combining traits of both species.",
            "pronunciation": "/ˈkætəˌloʊ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The rancher's _____ herd demonstrated the hardiness of bison with the docility of domestic cattle.",
            "etymology": "Blend of cattle + buffalo (bison)",
            "etymology_source": "Claude",
            "memory_tip": "Remember CATTALO: Cattle And Buffalo Lovely Animal Offspring - cattle-bison hybrid.",
            "fun_fact": "Cattalo breeding experiments peaked in the early 1900s but proved challenging due to reproductive difficulties in male hybrids.",
            "difficulty_level": calc.calculate_difficulty("cattalo", "A cattle-bison hybrid", "Blend of cattle + buffalo"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "caudex",
            "definition": "The woody stem or trunk of a palm, tree fern, or similar plant; the persistent base of an herbaceous perennial.",
            "pronunciation": "/ˈkɔdɛks/",
            "pronunciation_audio_url": "",
            "example_sentence": "The botanist examined the thick _____ of the ancient cycad, which had survived for centuries.",
            "etymology": "From Latin caudex 'tree trunk, wooden tablet'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAUDEX: Certain And Unique Dense Extended xylem - woody plant stem.",
            "fun_fact": "Some succulent plants develop a caudex as water storage, allowing them to survive extreme drought conditions.",
            "difficulty_level": calc.calculate_difficulty("caudex", "The woody stem of certain plants", "From Latin caudex"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "causal",
            "definition": "Relating to or acting as a cause; expressing or indicating cause and effect.",
            "pronunciation": "/ˈkɔzəl/",
            "pronunciation_audio_url": "",
            "example_sentence": "The scientist established a _____ relationship between the medication and the observed improvement in symptoms.",
            "etymology": "From Latin causalis, from causa 'cause'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAUSAL: Connecting And Understanding Situations And Linking events - relating to cause.",
            "fun_fact": "The phrase 'correlation does not imply causation' is a fundamental principle in statistics and scientific research.",
            "difficulty_level": calc.calculate_difficulty("causal", "Relating to cause and effect", "From Latin causalis"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "caustic",
            "definition": "Able to burn or corrode organic tissue by chemical action; or harshly critical in speech or manner.",
            "pronunciation": "/ˈkɔstɪk/",
            "pronunciation_audio_url": "",
            "example_sentence": "The chemistry teacher warned students about the _____ properties of the sodium hydroxide solution.",
            "etymology": "From Greek kaustikos, from kaiein 'to burn'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAUSTIC: Chemical And Usually Severe Tissue Injuring Corrosive - burning or harsh.",
            "fun_fact": "Caustic soda (sodium hydroxide) is used in soap making, where it chemically transforms fats into soap through saponification.",
            "difficulty_level": calc.calculate_difficulty("caustic", "Burning or harshly critical", "From Greek kaustikos"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cauterize",
            "definition": "To burn tissue with heat or chemicals to stop bleeding or prevent infection; to sear or destroy tissue.",
            "pronunciation": "/ˈkɔtəˌraɪz/",
            "pronunciation_audio_url": "",
            "example_sentence": "The surgeon chose to _____ the wound to prevent excessive bleeding during the procedure.",
            "etymology": "From Greek kauterion, from kaiein 'to burn'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAUTERIZE: Carefully And Using Temperature Eliminate Risky Infections Zones Effectively - burn tissue medically.",
            "fun_fact": "Ancient physicians used red-hot irons to cauterize wounds, a practice that saved many lives by preventing infection.",
            "difficulty_level": calc.calculate_difficulty("cauterize", "To burn tissue medically", "From Greek kauterion"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cautioned",
            "definition": "Past tense of caution; warned someone about a potential danger or problem; advised prudence.",
            "pronunciation": "/ˈkɔʃənd/",
            "pronunciation_audio_url": "",
            "example_sentence": "The park ranger _____ hikers about the dangerous trail conditions after the recent storms.",
            "etymology": "From caution + -ed, from Latin cautio 'care, precaution'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAUTIONED: Carefully Advised Users To Inspect Obvious Negative Emerging Dangers - warned.",
            "fun_fact": "Police officers 'caution' suspects by reading them their rights, a practice established by the Miranda v. Arizona case.",
            "difficulty_level": calc.calculate_difficulty("cautioned", "Warned about danger", "From Latin cautio + -ed"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cavalcade",
            "definition": "A procession of riders or vehicles; a series of related events or experiences.",
            "pronunciation": "/ˈkævəlˌkeɪd/",
            "pronunciation_audio_url": "",
            "example_sentence": "The royal _____ made its way through the city streets, with mounted guards and decorated carriages.",
            "etymology": "From French cavalcade, from Italian cavalcata, from cavalcare 'to ride'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAVALCADE: Ceremonial And Vehicular And Lovely Cavalry And Decorated Elegant procession - parade of riders.",
            "fun_fact": "Modern parades often called cavalcades originated from medieval military processions and royal progress tours.",
            "difficulty_level": calc.calculate_difficulty("cavalcade", "A procession of riders or vehicles", "From French cavalcade"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cavalier",
            "definition": "Showing a lack of proper concern; offhand or dismissive; or a horseman or knight.",
            "pronunciation": "/ˌkævəˈlɪr/",
            "pronunciation_audio_url": "",
            "example_sentence": "His _____ attitude toward safety regulations concerned the construction supervisor.",
            "etymology": "From French cavalier, from Italian cavaliere 'horseman'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAVALIER: Careless And Vain Attitude Lacks Intense Effort Responsibility - dismissive or horseman.",
            "fun_fact": "The Cavaliers were supporters of King Charles I during the English Civil War, named for their aristocratic cavalry origins.",
            "difficulty_level": calc.calculate_difficulty("cavalier", "Dismissive or horseman", "From French cavalier"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cavalletti",
            "definition": "Small, adjustable wooden jumps used in horse training to improve gait and jumping technique.",
            "pronunciation": "/ˌkævəˈlɛti/",
            "pronunciation_audio_url": "",
            "example_sentence": "The riding instructor set up _____ around the arena to help students practice their jumping position.",
            "etymology": "From Italian cavalletti, diminutive of cavallo 'horse'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAVALLETTI: Cavalry And Veterinary And Learning Little Equipment Training Together Improvements - horse training jumps.",
            "fun_fact": "Cavalletti training was developed by Italian cavalry officers to improve their horses' athleticism and rider balance.",
            "difficulty_level": calc.calculate_difficulty("cavalletti", "Small jumps for horse training", "From Italian cavalletti"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "caveat",
            "definition": "A warning or caution; a condition or qualification that limits an agreement or statement.",
            "pronunciation": "/ˈkæviˌæt/",
            "pronunciation_audio_url": "",
            "example_sentence": "The lawyer added a _____ to the contract regarding potential changes in tax regulations.",
            "etymology": "From Latin caveat 'let him beware', from cavere 'to beware'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAVEAT: Careful And Vigilant Examination And Thoughtful warning - caution or condition.",
            "fun_fact": "The phrase 'caveat emptor' means 'let the buyer beware' and places responsibility on purchasers to examine goods before buying.",
            "difficulty_level": calc.calculate_difficulty("caveat", "A warning or condition", "From Latin caveat"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "caveola",
            "definition": "A small invagination in the cell membrane, important for cellular transport and signaling processes.",
            "pronunciation": "/kæviˈoʊlə/",
            "pronunciation_audio_url": "",
            "example_sentence": "The cell biologist studied how proteins are transported through the _____ membrane structures.",
            "etymology": "From Latin caveola, diminutive of cavea 'hollow, cavity'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAVEOLA: Cellular And Vesicular Entry Opening Little Area - cell membrane invagination.",
            "fun_fact": "Caveolae were first observed in 1953 and are now known to play crucial roles in cardiovascular health.",
            "difficulty_level": calc.calculate_difficulty("caveola", "A cell membrane invagination", "From Latin caveola"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "caverns",
            "definition": "Large underground chambers or caves, typically formed by natural processes in rock formations.",
            "pronunciation": "/ˈkævərnz/",
            "pronunciation_audio_url": "",
            "example_sentence": "The explorers discovered vast limestone _____ filled with stalactites and underground pools.",
            "etymology": "From cavern + -s, from Latin caverna 'hollow, cave'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAVERNS: Cavernous And Vast Enormous Rock Natural Spaces - large underground chambers.",
            "fun_fact": "Mammoth Cave in Kentucky contains over 400 miles of surveyed caverns, making it the world's longest known cave system.",
            "difficulty_level": calc.calculate_difficulty("caverns", "Large underground chambers", "From Latin caverna + -s"),
            "source_difficulty": "Two Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "caves",
            "definition": "Natural underground chambers in rock formations; hollow spaces formed by erosion or geological processes.",
            "pronunciation": "/keɪvz/",
            "pronunciation_audio_url": "",
            "example_sentence": "The ancient people created beautiful paintings on the walls of _____ thousands of years ago.",
            "etymology": "From cave + -s, from Latin cavus 'hollow'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAVES: Cavernous And Vast Empty Spaces - natural underground chambers.",
            "fun_fact": "The oldest known cave paintings are in Spain and date back over 65,000 years, predating modern human arrival in Europe.",
            "difficulty_level": calc.calculate_difficulty("caves", "Natural underground chambers", "From Latin cavus + -s"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cavity",
            "definition": "A hollow space within something solid; a hole in a tooth caused by decay.",
            "pronunciation": "/ˈkævɪti/",
            "pronunciation_audio_url": "",
            "example_sentence": "The dentist discovered a small _____ during the routine examination and scheduled a filling appointment.",
            "etymology": "From Latin cavitas, from cavus 'hollow'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAVITY: Corroded And Vacant Internal Tooth Yielding problems - hollow space or tooth hole.",
            "fun_fact": "Tooth cavities are caused by bacteria that produce acid, which dissolves the tooth's mineral structure over time.",
            "difficulty_level": calc.calculate_difficulty("cavity", "A hollow space or tooth hole", "From Latin cavitas"),
            "source_difficulty": "Two Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cayenne",
            "definition": "A hot, red pepper used as a spice; or the capital city of French Guiana.",
            "pronunciation": "/kaɪˈɛn/",
            "pronunciation_audio_url": "",
            "example_sentence": "The chef added a pinch of _____ pepper to the soup for extra heat and flavor.",
            "etymology": "From Tupi kyynha, named after the Cayenne River in French Guiana",
            "etymology_source": "Claude",
            "memory_tip": "Remember CAYENNE: Culinary And Yummy Eating Nice Natural Exotic spice - hot red pepper.",
            "fun_fact": "Cayenne pepper contains capsaicin, which can help boost metabolism and has been used medicinally for centuries.",
            "difficulty_level": calc.calculate_difficulty("cayenne", "A hot red pepper", "From Tupi kyynha"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cecidium",
            "definition": "A plant gall; an abnormal growth on a plant caused by insects, mites, or other organisms.",
            "pronunciation": "/sɪˈsɪdiəm/",
            "pronunciation_audio_url": "",
            "example_sentence": "The botanist identified the round growth on the oak leaf as a _____ caused by wasp larvae.",
            "etymology": "From Greek kekidion, diminutive of kekis 'gall nut'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CECIDIUM: Certain Extraordinary Creature Induced Development In Unusual Material - plant gall.",
            "fun_fact": "Some galls are so specific to their host insects that they can be used to identify the species that created them.",
            "difficulty_level": calc.calculate_difficulty("cecidium", "A plant gall", "From Greek kekidion"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cedar",
            "definition": "An evergreen coniferous tree with aromatic wood, often used in construction and furniture making.",
            "pronunciation": "/ˈsidər/",
            "pronunciation_audio_url": "",
            "example_sentence": "The old _____ chest protected the family's winter clothes from moths with its natural oils.",
            "etymology": "From Old French cedre, from Latin cedrus, from Greek kedros",
            "etymology_source": "Claude",
            "memory_tip": "Remember CEDAR: Coniferous Evergreen Durable Aromatic Reliable tree - fragrant evergreen wood.",
            "fun_fact": "Cedar wood's natural oils make it resistant to insects and decay, which is why it's prized for storage chests and outdoor construction.",
            "difficulty_level": calc.calculate_difficulty("cedar", "An aromatic evergreen tree", "From Greek kedros"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "ceiling",
            "definition": "The upper interior surface of a room; an upper limit set on something.",
            "pronunciation": "/ˈsilɪŋ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The artist painted a beautiful mural on the cathedral's high, vaulted _____.",
            "etymology": "From Middle English celing, from Old French ciel 'sky'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CEILING: Covering Everything Inside Living Interior Naturally Generated - room's upper surface.",
            "fun_fact": "The Sistine Chapel's ceiling, painted by Michelangelo, took four years to complete and covers over 5,000 square feet.",
            "difficulty_level": calc.calculate_difficulty("ceiling", "The upper surface of a room", "From Old French ciel"),
            "source_difficulty": "Two Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "celebrates",
            "definition": "Third person singular present of celebrate; honors or commemorates something with festivities or ceremonies.",
            "pronunciation": "/ˈsɛləˌbreɪts/",
            "pronunciation_audio_url": "",
            "example_sentence": "The community _____ the harvest festival every autumn with music, dancing, and local food.",
            "etymology": "From celebrate + -s, from Latin celebratus 'honored'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CELEBRATES: Community Events Lasting Everyone Brings Rejoicing And Together Everyone Shares - honors with festivities.",
            "fun_fact": "The word 'celebrate' originally meant 'to honor' or 'to perform publicly' before evolving to include festive activities.",
            "difficulty_level": calc.calculate_difficulty("celebrates", "Honors with festivities", "From Latin celebratus + -s"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "celebrating",
            "definition": "Present participle of celebrate; honoring or commemorating with joy and festivities.",
            "pronunciation": "/ˈsɛləˌbreɪtɪŋ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The family spent the evening _____ their grandmother's 90th birthday with cake and stories.",
            "etymology": "From celebrate + -ing, from Latin celebratus",
            "etymology_source": "Claude",
            "memory_tip": "Remember CELEBRATING: Community Events Lasting Everyone Brings Rejoicing And Together In Notable Gatherings - honoring with joy.",
            "fun_fact": "Different cultures have unique ways of celebrating, from fireworks in China to piñatas in Mexico to ceremonial dances in many African traditions.",
            "difficulty_level": calc.calculate_difficulty("celebrating", "Honoring with festivities", "From Latin celebratus + -ing"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "celebratory",
            "definition": "Having the character of or serving as a celebration; expressing joy and festivity.",
            "pronunciation": "/ˈsɛləbrəˌtɔri/",
            "pronunciation_audio_url": "",
            "example_sentence": "The team's _____ dinner marked the successful completion of their three-year research project.",
            "etymology": "From celebrate + -ory, from Latin celebratus",
            "etymology_source": "Claude",
            "memory_tip": "Remember CELEBRATORY: Community Events Lasting Everyone Brings Rejoicing And Together Outstanding Remarkable Yearning - expressing celebration.",
            "fun_fact": "Celebratory traditions often include symbolic elements like toasts, which originated from the ancient practice of adding bread to wine.",
            "difficulty_level": calc.calculate_difficulty("celebratory", "Expressing celebration", "From Latin celebratus + -ory"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "celery",
            "definition": "A vegetable with long, green stalks that are eaten raw or cooked, known for its crisp texture and mild flavor.",
            "pronunciation": "/ˈsɛləri/",
            "pronunciation_audio_url": "",
            "example_sentence": "She chopped fresh _____ to add crunch and flavor to the chicken salad.",
            "etymology": "From French céleri, from Italian seleri, from Greek selinon 'parsley'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CELERY: Crisp Edible Long Eating Raw Yielding nutrition - green stalked vegetable.",
            "fun_fact": "Celery is about 95% water, making it one of the most hydrating vegetables, and it requires more energy to digest than it provides.",
            "difficulty_level": calc.calculate_difficulty("celery", "A green stalked vegetable", "From Greek selinon"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "celestial",
            "definition": "Relating to the sky or outer space; heavenly or divine in nature.",
            "pronunciation": "/səˈlɛstʃəl/",
            "pronunciation_audio_url": "",
            "example_sentence": "The astronomer studied _____ bodies through her powerful telescope every clear night.",
            "etymology": "From Latin caelestis, from caelum 'sky, heaven'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CELESTIAL: Concerning Everything Lovely Existing Starry Throughout Infinite And Limitless space - heavenly.",
            "fun_fact": "Celestial navigation, using stars and planets for direction, was essential for ocean voyages before the invention of GPS.",
            "difficulty_level": calc.calculate_difficulty("celestial", "Relating to the sky or heavenly", "From Latin caelestis"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cell",
            "definition": "The basic structural unit of living organisms; a small room or compartment.",
            "pronunciation": "/sɛl/",
            "pronunciation_audio_url": "",
            "example_sentence": "Under the microscope, each _____ displayed the characteristic nucleus and surrounding cytoplasm.",
            "etymology": "From Latin cella 'small room, chamber'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CELL: Contained Essential Living Layout - basic unit of life or small room.",
            "fun_fact": "The human body contains approximately 37 trillion cells, each performing specialized functions to maintain life.",
            "difficulty_level": calc.calculate_difficulty("cell", "Basic unit of life or small room", "From Latin cella"),
            "source_difficulty": "Two Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cello",
            "definition": "A large stringed musical instrument played with a bow, held between the knees while seated.",
            "pronunciation": "/ˈtʃɛloʊ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ player's haunting melody filled the concert hall with rich, deep tones.",
            "etymology": "Short for violoncello, from Italian violoncello, diminutive of violone",
            "etymology_source": "Claude",
            "memory_tip": "Remember CELLO: Classical Elegant Large Low Orchestra instrument - large stringed instrument.",
            "fun_fact": "The cello can play both bass and tenor ranges, making it one of the most versatile orchestral instruments.",
            "difficulty_level": calc.calculate_difficulty("cello", "A large stringed instrument", "From Italian violoncello"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cellophane",
            "definition": "A thin, transparent sheet material made from regenerated cellulose, used for packaging.",
            "pronunciation": "/ˈsɛləˌfeɪn/",
            "pronunciation_audio_url": "",
            "example_sentence": "The gift basket was wrapped in clear _____ tied with a colorful ribbon.",
            "etymology": "From cellulose + Greek phainein 'to show'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CELLOPHANE: Clear Extremely Light Layers Obviously Protecting Having And Neat Excellence - transparent wrapping material.",
            "fun_fact": "Cellophane was invented in 1908 and revolutionized food packaging by providing a clear, moisture-resistant barrier.",
            "difficulty_level": calc.calculate_difficulty("cellophane", "Transparent packaging material", "From cellulose + Greek phainein"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "celsius",
            "definition": "A temperature scale where water freezes at 0° and boils at 100°, named after Anders Celsius.",
            "pronunciation": "/ˈsɛlsiəs/",
            "pronunciation_audio_url": "",
            "example_sentence": "The weather forecast predicted temperatures reaching 35 degrees _____ by afternoon.",
            "etymology": "Named after Anders Celsius, Swedish astronomer who devised the scale",
            "etymology_source": "Claude",
            "memory_tip": "Remember CELSIUS: Centigrade Everywhere Logical Scale In Universal Science - temperature measurement scale.",
            "fun_fact": "Anders Celsius originally designed his scale with 100° for freezing and 0° for boiling, but it was later reversed.",
            "difficulty_level": calc.calculate_difficulty("celsius", "A temperature scale", "Named after Anders Celsius"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cement",
            "definition": "A powdery substance that hardens when mixed with water, used in construction; to join or bind firmly.",
            "pronunciation": "/sɪˈmɛnt/",
            "pronunciation_audio_url": "",
            "example_sentence": "The workers mixed _____ with sand and gravel to create concrete for the foundation.",
            "etymology": "From Old French ciment, from Latin caementum 'stone chips'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CEMENT: Construction Everyone Makes Effective New Together material - binding construction material.",
            "fun_fact": "The Romans developed hydraulic cement that could set underwater, enabling them to build harbors and underwater structures.",
            "difficulty_level": calc.calculate_difficulty("cement", "A binding construction material", "From Latin caementum"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cemetery",
            "definition": "A burial ground or graveyard where dead bodies are interred.",
            "pronunciation": "/ˈsɛməˌtɛri/",
            "pronunciation_audio_url": "",
            "example_sentence": "The old _____ was peaceful and well-maintained, with ancient oak trees shading the headstones.",
            "etymology": "From Greek koimeterion 'sleeping place', from koiman 'to put to sleep'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CEMETERY: Consecrated Everyone Memories Eternal Together Everyone Rest Yearning - burial ground.",
            "fun_fact": "The word 'cemetery' originally meant 'sleeping place,' reflecting the belief that death is a peaceful rest.",
            "difficulty_level": calc.calculate_difficulty("cemetery", "A burial ground", "From Greek koimeterion"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cenotaph",
            "definition": "A memorial monument erected in honor of persons buried elsewhere, especially soldiers killed in war.",
            "pronunciation": "/ˈsɛnəˌtæf/",
            "pronunciation_audio_url": "",
            "example_sentence": "The town's _____ honored local soldiers who died in foreign wars and whose bodies never returned home.",
            "etymology": "From Greek kenotaphion, from kenos 'empty' + taphos 'tomb'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CENOTAPH: Commemorating Everyone Not Otherwise Together And Present Here - empty tomb memorial.",
            "fun_fact": "The Cenotaph in London is the UK's primary war memorial, where the nation gathers each Remembrance Day.",
            "difficulty_level": calc.calculate_difficulty("cenotaph", "A memorial for those buried elsewhere", "From Greek kenotaphion"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cenote",
            "definition": "A natural pit or sinkhole filled with freshwater, especially in the Yucatan Peninsula of Mexico.",
            "pronunciation": "/sɪˈnoʊti/",
            "pronunciation_audio_url": "",
            "example_sentence": "The ancient Maya considered the _____ to be sacred gateways to the underworld.",
            "etymology": "From Spanish cenote, from Yucatec Maya ts'onot",
            "etymology_source": "Claude",
            "memory_tip": "Remember CENOTE: Central Everyone's Natural Open Together Ecosystem - natural freshwater sinkhole.",
            "fun_fact": "Cenotes were formed when limestone bedrock collapsed, exposing underground rivers, and many contain archaeological treasures.",
            "difficulty_level": calc.calculate_difficulty("cenote", "A natural freshwater sinkhole", "From Yucatec Maya ts'onot"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "census",
            "definition": "An official count or survey of a population, typically recording various details about individuals.",
            "pronunciation": "/ˈsɛnsəs/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ revealed that the city's population had grown by 15% over the past decade.",
            "etymology": "From Latin census, from censere 'to assess'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CENSUS: Counting Everyone Nationally Systematically Using Statistics - population survey.",
            "fun_fact": "The U.S. Constitution requires a census every 10 years to determine representation in the House of Representatives.",
            "difficulty_level": calc.calculate_difficulty("census", "An official population count", "From Latin census"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "centenary",
            "definition": "The hundredth anniversary of a significant event; a century or period of one hundred years.",
            "pronunciation": "/sɛnˈtinəri/",
            "pronunciation_audio_url": "",
            "example_sentence": "The university celebrated its _____ with a year-long series of special events and exhibitions.",
            "etymology": "From Latin centenarius, from centum 'hundred'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CENTENARY: Celebrating Everyone's Notable Truly Extraordinary Notable Anniversary Remarkable Year - hundredth anniversary.",
            "fun_fact": "Many institutions plan centenary celebrations for years in advance, often commissioning special commemorative items.",
            "difficulty_level": calc.calculate_difficulty("centenary", "A hundredth anniversary", "From Latin centenarius"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "centennial",
            "definition": "Relating to a hundredth anniversary; occurring once every hundred years.",
            "pronunciation": "/sɛnˈtɛniəl/",
            "pronunciation_audio_url": "",
            "example_sentence": "The town organized a _____ parade to commemorate its founding one hundred years ago.",
            "etymology": "From Latin centum 'hundred' + annus 'year' + -al",
            "etymology_source": "Claude",
            "memory_tip": "Remember CENTENNIAL: Celebrating Everyone's Notable Truly Extraordinary Notable Notable Important Anniversary Landmark - relating to hundredth anniversary.",
            "fun_fact": "The United States celebrated its centennial in 1876 with a massive exposition in Philadelphia that drew millions of visitors.",
            "difficulty_level": calc.calculate_difficulty("centennial", "Relating to hundredth anniversary", "From Latin centum + annus + -al"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "center",
            "definition": "The middle point of something; the main or most important part of something.",
            "pronunciation": "/ˈsɛntər/",
            "pronunciation_audio_url": "",
            "example_sentence": "The statue stood in the _____ of the town square, surrounded by benches and flower gardens.",
            "etymology": "From Latin centrum, from Greek kentron 'sharp point, center'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CENTER: Central Everything's Notable Together Equally Reached - middle point.",
            "fun_fact": "The concept of center varies: geometric center, center of mass, and center of gravity can all be different points.",
            "difficulty_level": calc.calculate_difficulty("center", "The middle point", "From Greek kentron"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "centipede",
            "definition": "An arthropod with a long, segmented body and many pairs of legs, typically one pair per body segment.",
            "pronunciation": "/ˈsɛntəˌpid/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ scurried across the basement floor with its many legs moving in coordinated waves.",
            "etymology": "From Latin centipeda, from centum 'hundred' + pes 'foot'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CENTIPEDE: Creature Everyone Notices Traveling Incredibly Producing Extreme Darting Everything - many-legged arthropod.",
            "fun_fact": "Despite their name meaning 'hundred feet,' centipedes actually have between 30 and 354 legs, always an odd number of pairs.",
            "difficulty_level": calc.calculate_difficulty("centipede", "A many-legged arthropod", "From Latin centipeda"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "central",
            "definition": "In the center; most important or essential; relating to a center.",
            "pronunciation": "/ˈsɛntrəl/",
            "pronunciation_audio_url": "",
            "example_sentence": "The _____ idea of her presentation was that collaboration improves team performance.",
            "etymology": "From Latin centralis, from centrum 'center'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CENTRAL: Core Everything's Notable Together Reaching All Locations - in the center or most important.",
            "fun_fact": "Central Park in New York City was designed as the 'lungs' of Manhattan, providing green space in the urban center.",
            "difficulty_level": calc.calculate_difficulty("central", "In the center or most important", "From Latin centralis"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "centrally",
            "definition": "In a central manner; from or in the center; in a way that involves central control.",
            "pronunciation": "/ˈsɛntrəli/",
            "pronunciation_audio_url": "",
            "example_sentence": "The building was _____ located, making it easily accessible from all parts of the city.",
            "etymology": "From central + -ly",
            "etymology_source": "Claude",
            "memory_tip": "Remember CENTRALLY: Core Everything's Notable Together Reaching All Locations Logically Yielding - in a central manner.",
            "fun_fact": "Centrally planned economies were a hallmark of socialist states, where the government controlled all economic decisions.",
            "difficulty_level": calc.calculate_difficulty("centrally", "In a central manner", "From central + -ly"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "centrifuge",
            "definition": "A machine that uses centrifugal force to separate substances of different densities.",
            "pronunciation": "/ˈsɛntrəˌfjudʒ/",
            "pronunciation_audio_url": "",
            "example_sentence": "The laboratory technician used a _____ to separate the blood cells from the plasma.",
            "etymology": "From Latin centrum 'center' + fugere 'to flee'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CENTRIFUGE: Center Force Utilized Generating Everything - machine using spinning force for separation.",
            "fun_fact": "Centrifuges can spin at over 100,000 rpm and generate forces millions of times stronger than gravity.",
            "difficulty_level": calc.calculate_difficulty("centrifuge", "A machine using spinning force", "From Latin centrum + fugere"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "centuries",
            "definition": "Plural of century; periods of one hundred years each.",
            "pronunciation": "/ˈsɛntʃəriz/",
            "pronunciation_audio_url": "",
            "example_sentence": "The ancient oak tree had stood in the forest for several _____, witnessing countless changes.",
            "etymology": "From century + -ies, from Latin centuria 'group of one hundred'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CENTURIES: Count Everyone's Notable Time Units Relating In Extended Spans - periods of one hundred years.",
            "fun_fact": "The concept of centuries helps historians organize long periods of time, though the first century AD actually ran from 1-100.",
            "difficulty_level": calc.calculate_difficulty("centuries", "Periods of one hundred years", "From Latin centuria + -ies"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "century",
            "definition": "A period of one hundred years; in sports, a score of one hundred points or runs.",
            "pronunciation": "/ˈsɛntʃəri/",
            "pronunciation_audio_url": "",
            "example_sentence": "The 21st _____ has been marked by rapid technological advancement and global connectivity.",
            "etymology": "From Latin centuria, from centum 'hundred'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CENTURY: Count Everyone's Notable Time Units Reaching Year - period of one hundred years.",
            "fun_fact": "In cricket, scoring a century (100 runs) is considered a significant individual achievement and is celebrated accordingly.",
            "difficulty_level": calc.calculate_difficulty("century", "A period of one hundred years", "From Latin centuria"),
            "source_difficulty": "Three Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cephalopod",
            "definition": "A marine mollusk with tentacles, such as an octopus, squid, cuttlefish, or nautilus.",
            "pronunciation": "/ˈsɛfələˌpɑd/",
            "pronunciation_audio_url": "",
            "example_sentence": "The marine biologist studied the intelligence of various _____ species, particularly their problem-solving abilities.",
            "etymology": "From Greek kephale 'head' + pous 'foot'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CEPHALOPOD: Creature Everyone Particularly Highly Advanced Likes Ocean People Observe Delightfully - head-footed marine animal.",
            "fun_fact": "Cephalopods are among the most intelligent invertebrates, capable of using tools, solving puzzles, and showing individual personalities.",
            "difficulty_level": calc.calculate_difficulty("cephalopod", "A marine mollusk with tentacles", "From Greek kephale + pous"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "ceramics",
            "definition": "Objects made from clay and hardened by heat; the art or science of making such objects.",
            "pronunciation": "/səˈræmɪks/",
            "pronunciation_audio_url": "",
            "example_sentence": "The museum's _____ collection included beautiful pottery from ancient civilizations around the world.",
            "etymology": "From Greek keramikos, from keramos 'potter's clay'",
            "etymology_source": "Claude",
            "memory_tip": "Remember CERAMICS: Clay Everyone Readily And Masterfully Invents Creative Spectacular objects - pottery and clay objects.",
            "fun_fact": "The oldest known ceramic objects are figurines dating back over 25,000 years, found in what is now the Czech Republic.",
            "difficulty_level": calc.calculate_difficulty("ceramics", "Objects made from clay", "From Greek keramikos"),
            "source_difficulty": "One Bee",
            "source": "Scripps National Spelling Bee",
            "source_url": "https://spellingbee.com"
        },
        {
            "word": "cereal",
            "definition": "A grass-like plant producing edible grains; breakfast food made from processed grains.",
            "pronunciation": "/ˈsɪriəl/",
            "pronunciation_audio_url": "",
            "example_sentence": "She poured milk over her favorite _____ and added fresh berries for extra flavor.",
            "etymology": "From Latin cerealis, from Ceres, Roman goddess of harvest",
            "etymology_source": "Claude",
            "memory_tip": "Remember CEREAL: Ceres Everyone Regularly Eats And Loves - grain-based food.",
            "fun_fact": "The first breakfast cereal was created in 1863 by James Caleb Jackson, who called it 'granula.'",
            "difficulty_level": calc.calculate_difficulty("cereal", "Grain-based breakfast food", "From Latin cerealis"),
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
    
    print(f"Batch 031 processing complete!")
    print(f"Processed: {len(df)}/50 words")
    print(f"Combined word errors flagged: {len(combined_word_errors)}")
    print(f"Valid spelling words: {len(output_data)}")
    
    if combined_word_errors:
        print(f"\nCombined word errors found:")
        for error in combined_word_errors:
            print(f"  - {error['word']}")

if __name__ == "__main__":
    process_batch_031()