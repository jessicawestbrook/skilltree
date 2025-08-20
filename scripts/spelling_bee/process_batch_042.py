import csv
import pandas as pd

class DifficultyCalculator:
    def calculate_phonetic_transparency(self, word):
        irregular_patterns = ['ough', 'augh', 'eigh', 'tion', 'sion', 'cial', 'tial', 'ph', 'gh', 'kn', 'wr', 'gn', 'mb', 'sc', 'ps']
        silent_letters = ['b', 'c', 'd', 'g', 'h', 'k', 'l', 'n', 'p', 's', 't', 'w']
        
        score = 1.0
        word_lower = word.lower()
        
        for pattern in irregular_patterns:
            if pattern in word_lower:
                score += 0.3
        
        for i, char in enumerate(word_lower):
            if char in silent_letters:
                if (char == 'b' and i > 0 and word_lower[i-1] == 'm') or \
                   (char == 'k' and i < len(word_lower)-1 and word_lower[i+1] == 'n') or \
                   (char == 'w' and i < len(word_lower)-1 and word_lower[i+1] == 'r'):
                    score += 0.2
        
        return min(score, 4.0)
    
    def calculate_frequency_score(self, word):
        common_words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their']
        
        if word.lower() in common_words:
            return 1.0
        elif len(word) <= 4:
            return 1.5
        elif len(word) <= 6:
            return 2.0
        elif len(word) <= 8:
            return 2.5
        elif len(word) <= 10:
            return 3.0
        else:
            return 3.5
    
    def calculate_morphological_complexity(self, word):
        prefixes = ['un', 're', 'in', 'dis', 'en', 'non', 'over', 'mis', 'sub', 'pre', 'inter', 'fore', 'de', 'trans', 'super', 'semi', 'anti', 'mid', 'under']
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment', 'ful', 'less', 'able', 'ible', 'ous', 'ious', 'al', 'ial', 'ic', 'ive', 'ary', 'ory']
        
        score = 1.0
        word_lower = word.lower()
        
        for prefix in prefixes:
            if word_lower.startswith(prefix):
                score += 0.5
                break
        
        for suffix in suffixes:
            if word_lower.endswith(suffix):
                score += 0.5
                break
        
        if len(word) > 10:
            score += 0.5
        if len(word) > 15:
            score += 0.5
        
        return min(score, 4.0)
    
    def calculate_etymology_complexity(self, etymology_info):
        if not etymology_info or etymology_info.lower() in ['unknown', 'english']:
            return 1.0
        
        complex_origins = ['greek', 'latin', 'sanskrit', 'arabic', 'hebrew', 'chinese', 'japanese']
        moderate_origins = ['french', 'german', 'spanish', 'italian', 'dutch', 'portuguese']
        
        etymology_lower = etymology_info.lower()
        
        for origin in complex_origins:
            if origin in etymology_lower:
                return 3.5
        
        for origin in moderate_origins:
            if origin in etymology_lower:
                return 2.5
        
        return 2.0

def calculate_difficulty_scores(word, etymology):
    calculator = DifficultyCalculator()
    
    phonetic = calculator.calculate_phonetic_transparency(word)
    frequency = calculator.calculate_frequency_score(word)
    morphological = calculator.calculate_morphological_complexity(word)
    etymology_score = calculator.calculate_etymology_complexity(etymology)
    
    return phonetic, frequency, morphological, etymology_score

batch_042_data = {
    'cooking': {
        'definition': 'The process of preparing food by applying heat through various methods such as boiling, frying, baking, or grilling. Cooking transforms raw ingredients into palatable, safe, and nutritious meals through chemical and physical changes. It involves combining ingredients, seasonings, and techniques to create diverse flavors, textures, and presentations that satisfy both nutritional needs and cultural preferences.',
        'part_of_speech': 'noun, verb (present participle)',
        'pronunciation_guide': 'KOOK-ing (/ˈkʊkɪŋ/)',
        'etymology': 'From Old English "coc" (cook) + present participle suffix "-ing"',
        'memory_tips': 'Think of the ongoing action of preparing food with heat and skill',
        'alternate_spellings': 'None',
        'language_origin': 'Old English',
        'example_sentence': 'Her _____ skills improved dramatically after taking culinary classes.'
    },
    'cool': {
        'definition': 'Having a low temperature; not warm or hot; calm and composed; fashionable or impressive in a relaxed way. Cool can describe physical temperature, emotional state, or social desirability. The term has evolved from simple temperature description to complex social and cultural meanings involving approval and admiration.',
        'part_of_speech': 'adjective, verb, noun',
        'pronunciation_guide': 'KOOL (/kul/)',
        'etymology': 'From Old English "col," related to "cold"',
        'memory_tips': 'Think of temperature, calmness, or something impressive and trendy',
        'alternate_spellings': 'None',
        'language_origin': 'Old English',
        'example_sentence': 'The evening breeze felt _____ after the hot summer day.'
    },
    'coop': {
        'definition': 'A cage or enclosure for keeping small animals, especially poultry like chickens; to confine in a restricted space. Coops provide protection, containment, and organized housing for domestic birds. The term can also metaphorically describe any cramped or confined living situation that restricts freedom of movement.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KOOP (/kup/)',
        'etymology': 'From Middle English "coupe," from Latin "cupa" (cask, tub)',
        'memory_tips': 'Think of chickens in their enclosed house - a chicken coop',
        'alternate_spellings': 'None',
        'language_origin': 'Middle English/Latin',
        'example_sentence': 'The farmer built a secure _____ to protect the chickens from predators.'
    },
    'cooperate': {
        'definition': 'To work together toward a common goal; to assist willingly and comply with requests or demands. Cooperation involves coordination, communication, and mutual support to achieve shared objectives. This collaborative behavior is essential for successful relationships, organizations, and societies.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'koh-OP-uh-rayt (/koʊˈɒpəreɪt/)',
        'etymology': 'From Latin "cooperatus," from "co-" (together) + "operari" (to work)',
        'memory_tips': 'Think "co- (together) + operate" - operating or working together',
        'alternate_spellings': 'Co-operate (hyphenated)',
        'language_origin': 'Latin',
        'example_sentence': 'The team members learned to _____ effectively to complete the project on time.'
    },
    'copenhagen': {
        'definition': 'The capital and largest city of Denmark, located on the eastern shore of Zealand island. Copenhagen is known for its historic architecture, progressive culture, cycling infrastructure, and high quality of life. The city serves as Denmark\'s political, economic, and cultural center, famous for landmarks like the Little Mermaid statue and Tivoli Gardens.',
        'part_of_speech': 'noun (proper name)',
        'pronunciation_guide': 'koh-pun-HAY-gun (/ˌkoʊpənˈheɪgən/)',
        'etymology': 'Danish "København," meaning "merchant\'s harbor," from "købmand" (merchant) + "havn" (harbor)',
        'memory_tips': 'Think of Danish merchants and harbors - a merchant\'s harbor city',
        'alternate_spellings': 'København (Danish)',
        'language_origin': 'Danish',
        'example_sentence': 'The conference was held in _____, allowing participants to explore Danish culture.'
    },
    'copernicium': {
        'definition': 'A synthetic chemical element with atomic number 112, named after astronomer Nicolaus Copernicus. This extremely radioactive element was first created in 1996 through particle accelerator experiments. Copernicium has no practical applications due to its instability and extremely short half-life, existing only for scientific research purposes.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'koh-pur-NIS-ee-um (/ˌkoʊpərˈnɪsiəm/)',
        'etymology': 'Named after Nicolaus Copernicus, Polish astronomer + Latin suffix "-ium"',
        'memory_tips': 'Think of Copernicus + -ium - an element named after the famous astronomer',
        'alternate_spellings': 'None',
        'language_origin': 'Modern Latin (from proper name)',
        'example_sentence': 'Scientists created _____ in the laboratory for only milliseconds before it decayed.'
    },
    'copious': {
        'definition': 'Abundant, plentiful, or existing in large quantities; produced or present in impressive amounts. Copious suggests generosity or richness in supply, whether referring to physical objects, abstract concepts, or natural phenomena. The term emphasizes abundance that exceeds normal expectations.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KOH-pee-us (/ˈkoʊpiəs/)',
        'etymology': 'From Latin "copiosus," meaning "plentiful," from "copia" (abundance)',
        'memory_tips': 'Think "copy" - so much that you could make many copies, abundant',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The garden produced _____ amounts of vegetables throughout the growing season.'
    },
    'copperhead': {
        'definition': 'A venomous North American snake with distinctive copper-colored markings, known for its triangular head and heat-sensing abilities. Copperheads are pit vipers that typically inhabit wooded areas and are responsible for many snakebite incidents in the United States. They are characterized by their reddish-brown coloration and hourglass-shaped crossbands.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOP-ur-hed (/ˈkɒpərˌhɛd/)',
        'etymology': 'From "copper" (reddish-brown metal) + "head" (referring to coloration)',
        'memory_tips': 'Think of a snake with a copper-colored head - distinctive reddish-brown coloring',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'Hikers should be cautious of _____ snakes in wooded areas during summer months.'
    },
    'copse': {
        'definition': 'A small group or thicket of trees, especially one that is regularly cut for wood or managed for wildlife. Copses are often maintained through traditional woodland management practices called coppicing, where trees are cut to encourage new growth. These small woodlands provide habitat for wildlife and sustainable timber resources.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOPS (/kɒps/)',
        'etymology': 'From Old French "copeiz," meaning "a cutting," from "couper" (to cut)',
        'memory_tips': 'Think of a "cop" (cut) of trees - a small group that can be cut and managed',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'The bird nested in the small _____ at the edge of the meadow.'
    },
    'coptic': {
        'definition': 'Relating to the Coptic Orthodox Church or the Coptic language, associated with Egyptian Christianity. Coptic refers to the Christian community in Egypt and the liturgical language derived from ancient Egyptian. The Coptic Church traces its origins to the apostle Mark and represents one of the oldest Christian traditions.',
        'part_of_speech': 'adjective, noun',
        'pronunciation_guide': 'KOP-tik (/ˈkɒptɪk/)',
        'etymology': 'From Arabic "qubti," from Greek "Aigyptios" (Egyptian)',
        'memory_tips': 'Think of Egyptian Christians and their ancient language and traditions',
        'alternate_spellings': 'None',
        'language_origin': 'Arabic/Greek',
        'example_sentence': 'The museum displayed ancient _____ manuscripts from Egyptian monasteries.'
    },
    'copy': {
        'definition': 'An identical or similar reproduction of something original; to make such a reproduction; to imitate or duplicate. Copying can involve physical reproduction, behavioral imitation, or digital duplication. The term encompasses both the action of replicating and the resulting duplicate product.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KOP-ee (/ˈkɒpi/)',
        'etymology': 'From Latin "copia," meaning "abundance, transcript"',
        'memory_tips': 'Think of making an identical version of something - a duplicate',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Please make a _____ of this document for the meeting.'
    },
    'coqui': {
        'definition': 'A small tree frog native to Puerto Rico, famous for its distinctive two-note call that sounds like "ko-KEE." These tiny frogs are important symbols of Puerto Rican culture and ecology. Coquí frogs are nocturnal and play crucial roles in their ecosystem, though introduced populations in other locations can become invasive.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'koh-KEE (/koʊˈki/)',
        'etymology': 'Taíno (indigenous Caribbean language), onomatopoeia of the frog\'s call',
        'memory_tips': 'Think of the sound "ko-KEE" that these Puerto Rican frogs make',
        'alternate_spellings': 'Coquí (with accent)',
        'language_origin': 'Taíno',
        'example_sentence': 'The _____ frogs filled the Puerto Rican night with their melodic calls.'
    },
    'coquiwith': {
        'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "coqui" (Puerto Rican tree frog) + "with" (preposition). These should be separate words.',
        'part_of_speech': 'error - combined words',
        'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
        'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
        'memory_tips': 'This is a data error - should be separated into "coqui" and "with"',
        'alternate_spellings': 'coqui + with (separate words)',
        'language_origin': 'ERROR - combined words',
        'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
    },
    'coracle': {
        'definition': 'A small, round boat traditionally made from a wooden frame covered with waterproof material like animal hide or canvas. Coracles are lightweight, portable vessels used for fishing and river transport, particularly in Wales and Ireland. These ancient boat designs demonstrate ingenious solutions for water navigation using available materials.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOR-uh-kul (/ˈkɒrəkəl/)',
        'etymology': 'From Welsh "corwgl," meaning "small round boat"',
        'memory_tips': 'Think of a "cor(e)" shaped like a circle - a round Welsh boat',
        'alternate_spellings': 'None',
        'language_origin': 'Welsh',
        'example_sentence': 'The fisherman paddled his traditional _____ across the calm Welsh river.'
    },
    'coralline': {
        'definition': 'Resembling, containing, or relating to coral; composed of or containing the calcium carbonate structures created by coral organisms. Coralline can describe marine algae that deposit calcium carbonate, geological formations made from ancient coral reefs, or anything having the characteristics of coral.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KOR-uh-lyn (/ˈkɒrəlaɪn/)',
        'etymology': 'From Latin "corallinus," from "corallum" (coral)',
        'memory_tips': 'Think "coral + -ine" - having the nature or characteristics of coral',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ limestone formed from ancient coral reefs millions of years ago.'
    },
    'corda': {
        'definition': 'A musical term meaning "string" in Italian, used in musical notation to indicate string instruments or specific string techniques. In organ music, "una corda" instructs to use one string (soft pedal on piano). The term appears in various musical contexts relating to stringed instruments and their performance techniques.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOR-dah (/ˈkɔrdə/)',
        'etymology': 'Italian, meaning "string," from Latin "chorda" (string, cord)',
        'memory_tips': 'Think "cord" - musical strings are cords that vibrate to make sound',
        'alternate_spellings': 'None',
        'language_origin': 'Italian/Latin',
        'example_sentence': 'The musical score indicated "una _____" for the delicate piano passage.'
    },
    'cordaunchristened': {
        'definition': '[COMBINED WORD ERROR] This appears to be multiple words incorrectly joined: "corda" (musical string) + "unchristened" (not baptized). These should be separate words.',
        'part_of_speech': 'error - combined words',
        'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
        'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
        'memory_tips': 'This is a data error - should be separated into "corda" and "unchristened"',
        'alternate_spellings': 'corda + unchristened (separate words)',
        'language_origin': 'ERROR - combined words',
        'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
    },
    'cordillera': {
        'definition': 'An extensive mountain range or system of parallel mountain chains, especially in the Americas. Cordilleras are major geological features formed by tectonic activity, creating long chains of peaks and valleys. Notable examples include the American Cordillera extending from Alaska to Chile and various cordilleras in Asia.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kor-dil-YEH-rah (/ˌkɔrdɪlˈjɛrə/)',
        'etymology': 'Spanish, meaning "mountain range," from "cordilla" (little cord) + augmentative "-era"',
        'memory_tips': 'Think "cord + hill" - mountains connected like a cord or rope',
        'alternate_spellings': 'None',
        'language_origin': 'Spanish',
        'example_sentence': 'The Andes form the longest _____ in the world, stretching along South America\'s western coast.'
    },
    'cordillerazazen': {
        'definition': '[COMBINED WORD ERROR] This appears to be words incorrectly joined: "cordillera" (mountain range) + "zazen" (Zen meditation). These should be separate words.',
        'part_of_speech': 'error - combined words',
        'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
        'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
        'memory_tips': 'This is a data error - should be separated into "cordillera" and "zazen"',
        'alternate_spellings': 'cordillera + zazen (separate words)',
        'language_origin': 'ERROR - combined words',
        'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
    },
    'corduroy': {
        'definition': 'A durable cotton fabric with a distinctive ribbed or ridged surface created by cut pile arranged in parallel lines. Corduroy is commonly used for clothing, upholstery, and other textile applications. The fabric\'s characteristic texture comes from extra weft threads that are cut to create the raised pile pattern.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOR-duh-roy (/ˈkɔrdərɔɪ/)',
        'etymology': 'Possibly from French "corde du roi" (cord of the king) or English "cord" + obsolete "duroy"',
        'memory_tips': 'Think of "cord" texture - the ribbed fabric feels like parallel cords',
        'alternate_spellings': 'None',
        'language_origin': 'French/English (uncertain)',
        'example_sentence': 'The professor wore his favorite _____ jacket with leather elbow patches.'
    },
    'core': {
        'definition': 'The central, innermost, or most essential part of something; the heart or nucleus around which other parts are assembled. Core can refer to physical centers (Earth\'s core), abstract concepts (core beliefs), or essential components (core curriculum). The term emphasizes fundamental importance and centrality.',
        'part_of_speech': 'noun, verb, adjective',
        'pronunciation_guide': 'KOHR (/kɔr/)',
        'etymology': 'From Old French "cuer," from Latin "cor" (heart)',
        'memory_tips': 'Think of the "heart" of something - the most central and important part',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'The _____ values of honesty and integrity guided her decisions.'
    },
    'corgi': {
        'definition': 'A short-legged herding dog breed originally from Wales, characterized by a long body, pointed ears, and fox-like face. Corgis were traditionally used for herding cattle and sheep. The two main varieties are Pembroke Welsh Corgi and Cardigan Welsh Corgi, both known for their intelligence and loyalty.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOR-gee (/ˈkɔrgi/)',
        'etymology': 'Welsh, possibly from "cor" (dwarf) + "ci" (dog)',
        'memory_tips': 'Think of a short dog - "cor" (dwarf) + "gi" (dog) from Welsh',
        'alternate_spellings': 'None',
        'language_origin': 'Welsh',
        'example_sentence': 'The energetic _____ herded the sheep with remarkable skill despite its short legs.'
    },
    'coriander': {
        'definition': 'An aromatic herb and spice from the cilantro plant (Coriandrum sativum), where the leaves are called cilantro and the seeds are called coriander. The seeds have a warm, nutty flavor used in cooking worldwide, while the leaves provide a fresh, citrusy taste. Both parts are essential ingredients in many cuisines.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kor-ee-AN-dur (/ˌkɔriˈændər/)',
        'etymology': 'From Old French "coriandre," from Latin "coriandrum," from Greek "koriannon"',
        'memory_tips': 'Think of the spice that comes from cilantro seeds - aromatic and flavorful',
        'alternate_spellings': 'None',
        'language_origin': 'Greek/Latin',
        'example_sentence': 'The recipe called for ground _____ seeds to add warmth to the curry.'
    },
    'corinthian': {
        'definition': 'Relating to Corinth, an ancient Greek city; describing the most ornate of the three classical orders of Greek architecture, characterized by elaborate acanthus leaf decorations on column capitals. Corinthian style represents the height of classical architectural refinement and decorative complexity.',
        'part_of_speech': 'adjective, noun',
        'pronunciation_guide': 'kuh-RIN-thee-uhn (/kəˈrɪnθiən/)',
        'etymology': 'From Latin "Corinthius," relating to the Greek city of Corinth',
        'memory_tips': 'Think of elaborate Greek columns with fancy decorative leaves at the top',
        'alternate_spellings': 'None',
        'language_origin': 'Latin/Greek',
        'example_sentence': 'The _____ columns of the courthouse featured intricate acanthus leaf carvings.'
    },
    'corkscrew': {
        'definition': 'A device for removing corks from wine bottles, typically consisting of a pointed spiral metal piece and a handle; something twisted in a spiral shape like the motion or path resembling such a tool. Corkscrews enable access to wine while preserving cork integrity.',
        'part_of_speech': 'noun, adjective, verb',
        'pronunciation_guide': 'KORK-skroo (/ˈkɔrkskru/)',
        'etymology': 'From "cork" (bottle stopper) + "screw" (spiral fastener)',
        'memory_tips': 'Think of screwing a spiral tool into a cork to remove it from a bottle',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'The sommelier used an elegant silver _____ to open the vintage wine.'
    },
    'corm': {
        'definition': 'A short, swollen underground plant stem that serves as a storage organ, similar to a bulb but solid throughout. Corms store nutrients and energy to support plant growth during dormant periods. Examples include gladiolus, crocus, and taro plants. Corms can be propagated by division to create new plants.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KORM (/kɔrm/)',
        'etymology': 'From Greek "kormos," meaning "tree trunk, log"',
        'memory_tips': 'Think of a solid plant "core" underground - like a thick tree trunk but underground',
        'alternate_spellings': 'None',
        'language_origin': 'Greek',
        'example_sentence': 'Gardeners plant gladiolus _____ in spring for beautiful summer flowers.'
    },
    'cormorant': {
        'definition': 'A large water bird with dark plumage, a long neck, and webbed feet, known for its excellent diving and fishing abilities. Cormorants have minimal waterproofing in their feathers, allowing them to sink easily while hunting fish underwater. They are found worldwide near water bodies and are sometimes used in traditional fishing practices.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOR-muh-ruhnt (/ˈkɔrmərænt/)',
        'etymology': 'From Old French "cormarant," from "corp" (raven) + "marenc" (of the sea)',
        'memory_tips': 'Think "corp (raven) + marine" - a dark sea bird like a sea raven',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'The _____ spread its wings to dry after diving for fish in the lake.'
    },
    'corn': {
        'definition': 'A cereal grain also known as maize, widely cultivated for food, animal feed, and industrial uses; in British English, any cereal grain including wheat, barley, or oats. Corn is a staple food crop that originated in Mexico and spread worldwide, becoming essential for global food security.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KORN (/kɔrn/)',
        'etymology': 'From Old English "corn," meaning "grain, seed"',
        'memory_tips': 'Think of golden kernels on a cob - the classic American corn',
        'alternate_spellings': 'Maize (scientific/British)',
        'language_origin': 'Old English',
        'example_sentence': 'Farmers harvested acres of _____ to feed livestock through the winter.'
    },
    'cornea': {
        'definition': 'The transparent front layer of the eye that covers the iris, pupil, and anterior chamber, providing much of the eye\'s focusing power. The cornea must remain clear and properly shaped for good vision. Corneal damage or irregularities can significantly impact sight, sometimes requiring transplantation or corrective surgery.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOR-nee-uh (/ˈkɔrniə/)',
        'etymology': 'From Latin "corneus," meaning "horny," referring to its horn-like transparency',
        'memory_tips': 'Think "horn-like" - the clear, protective covering of the eye',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The eye doctor examined her _____ for scratches after the accident.'
    },
    'cornel': {
        'definition': 'A type of dogwood tree (Cornus species) that produces small, edible, cherry-like fruits; the hard, dense wood from such trees. Cornel wood is prized for tool handles, walking sticks, and other applications requiring durability. The fruits are used in jams, liqueurs, and traditional medicine.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOR-nul (/ˈkɔrnəl/)',
        'etymology': 'From Old French "cornille," from Latin "cornum" (cornel cherry)',
        'memory_tips': 'Think of "corn" + "el" - a tree that produces corn-sized fruits',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'The artisan carved the _____ wood into a beautiful walking stick.'
    },
    'cornichon': {
        'definition': 'A small, tart pickle made from tiny gherkin cucumbers, typically served as an accompaniment to pâtés, charcuterie, and French cuisine. Cornichons are pickled in vinegar with herbs and spices, creating a sharp, acidic flavor that cuts through rich foods. They are a classic element of French culinary tradition.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kor-ni-SHON (/ˌkɔrnɪˈʃɒn/)',
        'etymology': 'French, diminutive of "corne" (horn), referring to the small, horn-like shape',
        'memory_tips': 'Think "corn + horn" - tiny horn-shaped pickles from France',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The charcuterie board included small _____ pickles alongside the rich pâté.'
    },
    'cornily': {
        'definition': 'In a corny manner; in a way that is overly sentimental, unsophisticated, or lacking in subtlety. This adverb describes behavior, speech, or artistic expression that is considered trite, cheesy, or embarrassingly earnest. The term often implies good intentions delivered with poor execution.',
        'part_of_speech': 'adverb',
        'pronunciation_guide': 'KOR-nuh-lee (/ˈkɔrnəli/)',
        'etymology': 'From "corny" (overly sentimental) + adverbial suffix "-ly"',
        'memory_tips': 'Think "corny + -ly" - in a cheesy, overly sentimental manner',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'He _____ declared his love with outdated romantic clichés.'
    },
    'cornilycontraction': {
        'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "cornily" (in a corny manner) + "contraction" (shortening or tightening). These should be separate words.',
        'part_of_speech': 'error - combined words',
        'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
        'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
        'memory_tips': 'This is a data error - should be separated into "cornily" and "contraction"',
        'alternate_spellings': 'cornily + contraction (separate words)',
        'language_origin': 'ERROR - combined words',
        'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
    },
    'cornucopia': {
        'definition': 'A horn-shaped container overflowing with fruits, vegetables, and flowers, symbolizing abundance and prosperity; any abundant supply or great abundance of something. Also called the "horn of plenty," this symbol appears in art, literature, and seasonal decorations, especially during harvest celebrations like Thanksgiving.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kor-nuh-KOH-pee-uh (/ˌkɔrnəˈkoʊpiə/)',
        'etymology': 'From Latin "cornu copiae," meaning "horn of plenty"',
        'memory_tips': 'Think "corn (horn) + copia (plenty)" - a horn filled with plenty of good things',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The Thanksgiving centerpiece featured a _____ overflowing with autumn harvest.'
    },
    'corollary': {
        'definition': 'A proposition that follows logically from one already proved; a natural consequence or result that accompanies or parallels a main result. In mathematics and logic, corollaries extend proven theorems. In general usage, corollaries are secondary effects or conclusions that naturally flow from primary events or decisions.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOR-uh-ler-ee (/ˈkɔrəˌlɛri/)',
        'etymology': 'From Latin "corollarium," meaning "money for a garland, gratuity"',
        'memory_tips': 'Think of a "crown" (coroll-) of additional results following from the main one',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'A _____ of increased education funding was improved test scores across the district.'
    },
    'coronation': {
        'definition': 'The ceremony of crowning a sovereign or monarch, formally investing them with regal power and authority. Coronations are elaborate state ceremonies rich with tradition, symbolism, and religious significance. They mark the official beginning of a reign and often involve oaths, religious blessings, and presentation of royal regalia.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kor-uh-NAY-shun (/ˌkɔrəˈneɪʃən/)',
        'etymology': 'From Latin "coronatio," from "coronare" (to crown)',
        'memory_tips': 'Think "crown + -ation" - the act of placing a crown on someone\'s head',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ ceremony was broadcast worldwide to millions of viewers.'
    },
    'coroner': {
        'definition': 'A public official responsible for investigating deaths that occur under unusual, suspicious, or unexplained circumstances. Coroners determine cause and manner of death, often working with medical examiners, law enforcement, and forensic specialists. They may conduct inquests and issue death certificates for legal and public health purposes.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOR-uh-nur (/ˈkɔrənər/)',
        'etymology': 'From Anglo-Norman "corouner," from "coroune" (crown), originally a crown officer',
        'memory_tips': 'Think "crown officer" - an official who works for the crown/government on deaths',
        'alternate_spellings': 'None',
        'language_origin': 'Anglo-Norman',
        'example_sentence': 'The _____ ruled that the death was accidental after examining all evidence.'
    },
    'corporate': {
        'definition': 'Relating to a business corporation; involving shared responsibility or unified action by a group. Corporate can describe business structures, culture, policies, or activities conducted by companies. The term emphasizes collective organization, formal business practices, and institutional rather than individual action.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KOR-pur-it (/ˈkɔrpərɪt/)',
        'etymology': 'From Latin "corporatus," from "corpus" (body) - formed into a body',
        'memory_tips': 'Think "corp (body) + -ate" - formed into one body or organization',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ headquarters housed over 2,000 employees across thirty floors.'
    },
    'corpulent': {
        'definition': 'Having a large, bulky body; obese or very overweight. This formal term describes excessive body weight in a clinical or literary context. Corpulent suggests not just overweight but substantially heavy, often used in medical, historical, or descriptive literary contexts rather than casual conversation.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KOR-pyuh-luhnt (/ˈkɔrpjələnt/)',
        'etymology': 'From Latin "corpulentus," from "corpus" (body)',
        'memory_tips': 'Think "corp (body) + -ulent" - having a very large or full body',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ gentleman struggled to fit into the airplane seat.'
    },
    'corpus': {
        'definition': 'A collection or body of written or spoken material; the main part or body of something; in anatomy, the main part of an organ or structure. Corpus can refer to literary works, legal documents, linguistic data, or physical body parts. The term emphasizes completeness and systematic organization.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOR-pus (/ˈkɔrpəs/)',
        'etymology': 'Latin, meaning "body"',
        'memory_tips': 'Think of a "body" of work or knowledge - a complete collection',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Researchers analyzed a large _____ of text to study language patterns.'
    },
    'corral': {
        'definition': 'An enclosure for confining livestock, especially horses or cattle; to gather together and confine or control. Corrals are typically circular or rectangular fenced areas used in ranching and farming. The verb form means to round up, gather, or bring under control.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'kuh-RAL (/kəˈræl/)',
        'etymology': 'From Spanish "corral," meaning "yard, enclosure"',
        'memory_tips': 'Think of cowboys corralling cattle - gathering them into an enclosed area',
        'alternate_spellings': 'None',
        'language_origin': 'Spanish',
        'example_sentence': 'The ranchers built a sturdy _____ to hold the wild horses.'
    },
    'correct': {
        'definition': 'Free from error; accurate, true, or right; conforming to established standards; to make right by removing errors or faults. Correct implies accordance with fact, truth, or proper procedure. As a verb, it means to fix, adjust, or point out mistakes.',
        'part_of_speech': 'adjective, verb',
        'pronunciation_guide': 'kuh-REKT (/kəˈrɛkt/)',
        'etymology': 'From Latin "correctus," from "corrigere" (to make straight)',
        'memory_tips': 'Think "co- (thoroughly) + rect (straight)" - thoroughly straightened or made right',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Please _____ any errors you find in the final draft.'
    },
    'correctly': {
        'definition': 'In a correct manner; accurately, properly, or without error. This adverb describes actions performed according to proper standards, rules, or factual accuracy. Correctly emphasizes precision, appropriateness, and conformity to established norms or truth.',
        'part_of_speech': 'adverb',
        'pronunciation_guide': 'kuh-REKT-lee (/kəˈrɛktli/)',
        'etymology': 'From Latin "correctus" + adverbial suffix "-ly"',
        'memory_tips': 'Think "correct + -ly" - in a correct or accurate manner',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'She _____ identified all the plants during the botany examination.'
    },
    'corridor': {
        'definition': 'A long passage or hallway connecting different rooms or areas within a building; a strip of land connecting two larger areas, often providing access or passage. Corridors facilitate movement and can be architectural features, transportation routes, or ecological connections between habitats.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOR-i-dor (/ˈkɔrɪˌdɔr/)',
        'etymology': 'From Italian "corridore," from "correre" (to run)',
        'memory_tips': 'Think of "running" through a hallway - a passage where people move quickly',
        'alternate_spellings': 'None',
        'language_origin': 'Italian',
        'example_sentence': 'The school _____ echoed with footsteps between classes.'
    },
    'corrigenda': {
        'definition': 'Plural of corrigendum; a list of errors and their corrections, typically found in books or published works. Corrigenda appear as errata sheets or correction notices to fix mistakes discovered after publication. This formal term is commonly used in academic and scholarly publishing.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'kor-i-JEN-duh (/ˌkɔrɪˈdʒɛndə/)',
        'etymology': 'Latin, meaning "things to be corrected," from "corrigere" (to correct)',
        'memory_tips': 'Think "corrig (correct) + -enda (things to be done)" - things that need correcting',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The publisher issued _____ to fix the numerous typographical errors.'
    },
    'corroborate': {
        'definition': 'To confirm or support with evidence; to strengthen or make more certain by providing additional proof or testimony. Corroboration involves independent verification that increases confidence in claims, statements, or findings. This process is crucial in legal proceedings, scientific research, and journalism.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'kuh-ROB-uh-rayt (/kəˈrɒbəreɪt/)',
        'etymology': 'From Latin "corroboratus," from "cor-" (thoroughly) + "roborare" (to strengthen)',
        'memory_tips': 'Think "cor- (thoroughly) + robor (strength)" - thoroughly strengthening with evidence',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Multiple witnesses were able to _____ the defendant\'s alibi.'
    },
    'corrosive': {
        'definition': 'Having the power to gradually destroy or damage by chemical action; harmful or destructive in a gradual way. Corrosive substances eat away at materials through chemical reactions. Metaphorically, corrosive describes attitudes, behaviors, or influences that gradually damage relationships, institutions, or morale.',
        'part_of_speech': 'adjective, noun',
        'pronunciation_guide': 'kuh-ROH-siv (/kəˈroʊsɪv/)',
        'etymology': 'From Latin "corrosivus," from "corrodere" (to gnaw away)',
        'memory_tips': 'Think "cor- (thoroughly) + ros (gnaw)" - thoroughly gnawing away at something',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ acid slowly ate through the metal container.'
    },
    'corsage': {
        'definition': 'A small bouquet of flowers worn on a woman\'s dress or wrist, typically for special occasions like proms, weddings, or formal events. Corsages are decorative floral arrangements designed to complement formal attire and mark celebratory occasions. They represent tradition, elegance, and special recognition.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kor-SAHZH (/kɔrˈsɑʒ/)',
        'etymology': 'French, from "cors" (body, bodice), referring to flowers worn on the bodice',
        'memory_tips': 'Think of flowers worn on the "cors" (body) - decorative flowers on formal wear',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'He presented her with an elegant orchid _____ before the dance.'
    },
    'corsair': {
        'definition': 'A pirate or privateer, especially those operating in the Mediterranean Sea; a fast sailing ship used by pirates or privateers. Corsairs were often sanctioned by governments to attack enemy ships, blurring the line between piracy and naval warfare. The term evokes maritime adventure and lawlessness.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOR-sair (/ˈkɔrˌsɛr/)',
        'etymology': 'From French "corsaire," from Italian "corsaro," from Latin "cursus" (course, raid)',
        'memory_tips': 'Think "course + air" - pirates who coursed through the air over water',
        'alternate_spellings': 'None',
        'language_origin': 'French/Italian',
        'example_sentence': 'The _____ ship flew a black flag as it approached the merchant vessel.'
    },
    'cortege': {
        'definition': 'A solemn procession, especially for a funeral; a formal procession of people accompanying someone important. Corteges are ceremonial formations that demonstrate respect, honor, or mourning. They can accompany funerals, state ceremonies, or other significant occasions requiring formal processional movement.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kor-TEZH (/kɔrˈtɛʒ/)',
        'etymology': 'French, from Italian "corteggio," from "corte" (court)',
        'memory_tips': 'Think "court + -ege" - a formal procession fit for a royal court',
        'alternate_spellings': 'Cortège (with accent)',
        'language_origin': 'French/Italian',
        'example_sentence': 'The funeral _____ slowly made its way through the city streets.'
    }
}

def process_batch():
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_042_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_042_processed.csv'
    
    try:
        df = pd.read_csv(input_file)
        print(f"Processing {len(df)} words from batch 042...")
        
        processed_data = []
        combined_word_errors = []
        
        for _, row in df.iterrows():
            word = row['word'].strip()
            if word in batch_042_data:
                data = batch_042_data[word]
                
                if data['part_of_speech'] == 'error - combined words':
                    combined_word_errors.append(word)
                
                phonetic, frequency, morphological, etymology_score = calculate_difficulty_scores(word, data['etymology'])
                
                processed_data.append({
                    'word': word,
                    'definition': data['definition'],
                    'part_of_speech': data['part_of_speech'],
                    'pronunciation_guide': data['pronunciation_guide'],
                    'etymology': data['etymology'],
                    'memory_tips': data['memory_tips'],
                    'alternate_spellings': data['alternate_spellings'],
                    'language_origin': data['language_origin'],
                    'example_sentence': data['example_sentence'],
                    'years': row['years'],
                    'source_files': row['source_files'],
                    'source_difficulties': row['source_difficulties'],
                    'difficulty_phonetic': round(phonetic, 2),
                    'difficulty_frequency': round(frequency, 2),
                    'difficulty_morphological': round(morphological, 2),
                    'difficulty_etymology': round(etymology_score, 2),
                    'difficulty_final': None,
                    'etymology_source': 'Claude',
                    'definition_source': 'Claude',
                    'pronunciation_source': 'Claude',
                    'example_sentence_source': 'Claude'
                })
        
        output_df = pd.DataFrame(processed_data)
        output_df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"Successfully processed {len(processed_data)}/50 words")
        print(f"Output saved to: {output_file}")
        
        if combined_word_errors:
            print(f"Found {len(combined_word_errors)} combined word errors:")
            for error in combined_word_errors:
                print(f"   - {error}")
        else:
            print("No combined word errors found")
            
        return True
        
    except Exception as e:
        print(f"Error processing batch: {str(e)}")
        return False

if __name__ == "__main__":
    process_batch()