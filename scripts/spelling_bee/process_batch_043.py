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

batch_043_data = {
    'cortex': {
        'definition': 'The outer layer of an organ or structure, especially the brain or kidney; the bark of a tree or plant. In neuroscience, the cerebral cortex is responsible for higher cognitive functions including thinking, memory, and consciousness. The term describes the outer, often functionally distinct layer that differs from the inner core or medulla.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOR-teks (/ˈkɔrtɛks/)',
        'etymology': 'Latin, meaning "bark, rind, shell"',
        'memory_tips': 'Think of "core + tex(ture)" - the textured outer layer covering the core',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The brain\'s _____ processes complex information and conscious thought.'
    },
    'corybantic': {
        'definition': 'Wild, frenzied, or ecstatic, especially in a way associated with religious or ritualistic dancing. This term refers to the frenzied worship of Cybele by her priests called Corybants in ancient Greek and Roman religion. It describes uncontrolled, passionate behavior that seems almost possessed or divinely inspired.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kor-uh-BAN-tik (/ˌkɔrəˈbæntɪk/)',
        'etymology': 'From Greek "korybantikos," relating to the Corybants (priests of Cybele)',
        'memory_tips': 'Think "cory + ban + tic" - like frenzied priests banned from normal behavior',
        'alternate_spellings': 'None',
        'language_origin': 'Greek',
        'example_sentence': 'The _____ celebration featured wild dancing and ecstatic music.'
    },
    'cost': {
        'definition': 'The amount of money required to purchase or obtain something; the sacrifice or loss involved in achieving a goal; to require a specified payment or sacrifice. Cost encompasses both financial price and non-monetary consequences like time, effort, or opportunity loss.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KOST (/kɔst/)',
        'etymology': 'From Old French "coste," from Latin "constare" (to stand together, cost)',
        'memory_tips': 'Think of what something "stands" you - what you must pay or sacrifice',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'The _____ of education continues to rise faster than inflation.'
    },
    'costume': {
        'definition': 'Clothing worn to portray a character, represent a historical period, or for theatrical performance; the distinctive dress characteristic of a particular country, period, or class. Costumes serve decorative, educational, or entertainment purposes, often involving careful attention to historical accuracy or creative interpretation.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'kos-TOOM (/kɔsˈtum/) or KOS-toom (/ˈkɔstum/)',
        'etymology': 'From French "costume," from Italian "costume" (custom, fashion)',
        'memory_tips': 'Think "custom" clothing - special dress following customs or for characters',
        'alternate_spellings': 'None',
        'language_origin': 'French/Italian',
        'example_sentence': 'Her elaborate Victorian _____ won first prize at the historical reenactment.'
    },
    'coterie': {
        'definition': 'A small, exclusive group of people with shared interests or tastes; an intimate circle of friends or associates. Coteries often form around common intellectual, artistic, or social pursuits. The term suggests exclusivity and close personal bonds among members who may influence each other\'s ideas and activities.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOH-tuh-ree (/ˈkoʊtəri/)',
        'etymology': 'French, meaning "group of tenants," from "cote" (quota, share)',
        'memory_tips': 'Think "co + tery" - a territory shared by a close group of people',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The literary _____ met weekly to discuss poetry and philosophy.'
    },
    'cotoneaster': {
        'definition': 'A genus of flowering shrubs in the rose family, commonly used in landscaping for their attractive berries, autumn colors, and hardy nature. These versatile plants range from ground-covering to tree-sized species, often featuring small white or pink flowers followed by colorful red, orange, or black berries that attract birds.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kuh-toh-nee-AS-tur (/kəˌtoʊniˈæstər/)',
        'etymology': 'Latin, meaning "quince-like," from "cotoneum" (quince) + "-aster" (resembling)',
        'memory_tips': 'Think "cotton + easter" - shrubs with cotton-like flowers around spring time',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ shrubs provided year-round interest with spring flowers and autumn berries.'
    },
    'cotta': {
        'definition': 'A short surplice worn by Catholic and Anglican clergy and choir members; a white vestment worn over other garments during religious services. This ecclesiastical garment typically reaches to the waist or hips and may be plain or decorated with lace. It represents clerical tradition and ceremonial dress.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOT-uh (/ˈkɒtə/)',
        'etymology': 'From Medieval Latin "cotta," possibly from Frankish "kotta" (coarse cloth)',
        'memory_tips': 'Think "coat + a" - a special coat worn by religious officials',
        'alternate_spellings': 'None',
        'language_origin': 'Medieval Latin',
        'example_sentence': 'The altar server wore a white _____ over his dark cassock.'
    },
    'cottage': {
        'definition': 'A small, simple house, typically in a rural or semi-rural setting; originally referring to the dwelling of a farm laborer or peasant. Modern cottages often serve as vacation homes or represent cozy, rustic architecture. The term evokes images of quaint, comfortable living in natural settings.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOT-ij (/ˈkɒtɪdʒ/)',
        'etymology': 'From Middle English "cotage," from "cot" (small house) + suffix "-age"',
        'memory_tips': 'Think "cot + age" - a small house from an earlier age',
        'alternate_spellings': 'None',
        'language_origin': 'Middle English',
        'example_sentence': 'They spent summers at a charming _____ by the lake.'
    },
    'cotton': {
        'definition': 'A soft, fluffy fiber that grows around the seeds of cotton plants; fabric made from this fiber; to take a liking to something or understand it. Cotton is one of the most important natural fibers, used extensively in textile production. The plant requires warm climates and significant water for cultivation.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KOT-n (/ˈkɒtən/)',
        'etymology': 'From Old French "coton," from Arabic "quṭun"',
        'memory_tips': 'Think of soft, white fluffy material - like cotton balls or cotton clothing',
        'alternate_spellings': 'None',
        'language_origin': 'Arabic (via Old French)',
        'example_sentence': 'The _____ shirt was comfortable and breathable in hot weather.'
    },
    'cottonwood': {
        'definition': 'A fast-growing deciduous tree of the poplar family, native to North America, known for its triangular leaves and cotton-like seeds that float on the wind. Cottonwoods typically grow near water sources and can reach impressive heights. Their seeds create distinctive white, fluffy masses that drift through the air in late spring.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOT-n-wood (/ˈkɒtənˌwʊd/)',
        'etymology': 'From "cotton" (referring to fluffy seeds) + "wood" (tree)',
        'memory_tips': 'Think of cotton-like seeds floating from wood/trees in spring',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'The _____ trees released clouds of white seeds that filled the air.'
    },
    'cotyledon': {
        'definition': 'The first leaf or leaves that appear when a seed germinates; a seed leaf that stores nutrients for the developing plant embryo. Cotyledons are often different in shape from the plant\'s mature leaves and may remain below ground or emerge above soil. They represent the plant\'s first photosynthetic structures.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kot-uh-LEE-dn (/ˌkɒtəˈlidən/)',
        'etymology': 'From Greek "kotyledon," meaning "cup-shaped cavity," from "kotyle" (cup)',
        'memory_tips': 'Think "coty (cup) + ledon (leaf)" - cup-shaped first leaves of plants',
        'alternate_spellings': 'None',
        'language_origin': 'Greek',
        'example_sentence': 'The bean\'s _____ emerged first, followed by the true leaves.'
    },
    'couch': {
        'definition': 'A long upholstered piece of furniture for seating multiple people; to express in particular words or language; to lie down. As furniture, couches provide comfortable seating for relaxation and social gatherings. As a verb, it means to phrase or formulate language carefully.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KOWCH (/kaʊtʃ/)',
        'etymology': 'From Old French "couche," from "coucher" (to lie down)',
        'memory_tips': 'Think of lying down comfortably - a place to couch or rest',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'She decided to _____ her criticism in diplomatic language.'
    },
    'cough': {
        'definition': 'A sudden, sharp expulsion of air from the lungs, often involuntary and used to clear the throat or airways; the act of making this sound. Coughs can be protective reflexes, symptoms of illness, or voluntary actions. They help remove irritants, mucus, or foreign particles from the respiratory system.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KAWF (/kɔf/)',
        'etymology': 'From Middle English "coughen," imitative of the sound',
        'memory_tips': 'Think of the sound "cough" - an onomatopoeia for throat clearing',
        'alternate_spellings': 'None',
        'language_origin': 'Middle English (imitative)',
        'example_sentence': 'His persistent _____ kept him awake throughout the night.'
    },
    'coulibiac': {
        'definition': 'A Russian fish pie traditionally made with salmon, rice, hard-boiled eggs, and herbs, all wrapped in pastry or pancakes. This elaborate dish represents classic Russian cuisine and requires considerable culinary skill to prepare properly. Coulibiac is often served at special occasions and demonstrates sophisticated cooking techniques.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'koo-lee-bee-AHK (/ˌkulɪbiˈɑk/)',
        'etymology': 'Russian "kulebyaka," a traditional fish pie',
        'memory_tips': 'Think "cool + libiac" - a cool Russian fish pie that sounds exotic',
        'alternate_spellings': 'Kulebyaka',
        'language_origin': 'Russian',
        'example_sentence': 'The chef prepared an elaborate _____ for the Russian cultural dinner.'
    },
    'coulisse': {
        'definition': 'The wings or side scenes of a theater stage; the backstage area; in French, refers to theater corridors or behind-the-scenes areas. Coulisse represents the hidden operational spaces of theatrical productions where actors prepare and technical work occurs away from audience view.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'koo-LEES (/kuˈlis/)',
        'etymology': 'French, meaning "groove, slide," from "couler" (to flow, slide)',
        'memory_tips': 'Think "cool + lees" - the cool side areas where actors slide in and out of view',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The actors waited nervously in the _____ before their entrance cue.'
    },
    'coulomb': {
        'definition': 'The standard unit of electric charge in the International System of Units, equal to the charge of approximately 6.24 × 10^18 electrons. Named after French physicist Charles-Augustin de Coulomb, this fundamental unit measures the quantity of electrical charge. One coulomb represents the amount of charge transferred by one ampere in one second.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'koo-LOHM (/kuˈloʊm/)',
        'etymology': 'Named after Charles-Augustin de Coulomb, French physicist (1736-1806)',
        'memory_tips': 'Think of "cool + ohm" - a unit related to electrical measurements',
        'alternate_spellings': 'None',
        'language_origin': 'French (proper name)',
        'example_sentence': 'The capacitor stored exactly one _____ of electrical charge.'
    },
    'coulrophobia': {
        'definition': 'An abnormal or irrational fear of clowns. This specific phobia can cause intense anxiety, panic attacks, or avoidance behavior when encountering clowns or clown-related imagery. Coulrophobia may develop from negative childhood experiences or cultural portrayals of clowns as sinister figures.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kool-ruh-FOH-bee-uh (/ˌkulrəˈfoʊbiə/)',
        'etymology': 'From Greek "kolobathron" (stilt-walker) + "phobos" (fear)',
        'memory_tips': 'Think "clown + phobia" - though it sounds like "cool + phobia," it\'s fear of clowns',
        'alternate_spellings': 'None',
        'language_origin': 'Greek',
        'example_sentence': 'Her _____ made circus visits impossible due to intense fear of performers.'
    },
    'council': {
        'definition': 'An assembly of people meeting for consultation, deliberation, or advice; a governing or advisory body elected or appointed to manage affairs of a city, organization, or group. Councils make collective decisions, provide oversight, and represent constituent interests in democratic processes.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOWN-sil (/ˈkaʊnsəl/)',
        'etymology': 'From Old French "concile," from Latin "concilium" (assembly)',
        'memory_tips': 'Think "con + cil" - people coming together to deliberate (not "counsel")',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'The city _____ voted unanimously to approve the new park development.'
    },
    'count': {
        'definition': 'To determine the number of items in a group by assigning numbers in sequence; to include or consider; a European nobleman ranking above a baron; the total number reached by counting. Count encompasses mathematical enumeration, social inclusion, and aristocratic titles.',
        'part_of_speech': 'verb, noun',
        'pronunciation_guide': 'KOWNT (/kaʊnt/)',
        'etymology': 'From Old French "conter," from Latin "computare" (to calculate)',
        'memory_tips': 'Think of calculating or computing numbers, or a noble title',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'Please _____ the votes carefully to ensure accuracy in the election.'
    },
    'countenance': {
        'definition': 'A person\'s facial expression or appearance, especially as it reflects mood or character; to accept, approve, or tolerate something. As a noun, countenance describes the face as an indicator of inner state. As a verb, it means to sanction or permit behavior.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KOWN-tuh-nuhns (/ˈkaʊntənəns/)',
        'etymology': 'From Old French "contenance," from Latin "continentia" (restraint, demeanor)',
        'memory_tips': 'Think "count +enance" - the face that counts or shows what you\'re thinking',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'His stern _____ revealed his disapproval of the proposal.'
    },
    'counterclockwise': {
        'definition': 'In the direction opposite to the movement of clock hands; from right to left when viewed from above. This directional term describes rotational movement that reverses the conventional clockwise direction. It\'s used in instructions, descriptions of mechanical operation, and spatial orientation.',
        'part_of_speech': 'adjective, adverb',
        'pronunciation_guide': 'kown-tur-KLOK-wyze (/ˈkaʊntərˌklɒkwaɪz/)',
        'etymology': 'From "counter-" (opposite) + "clockwise"',
        'memory_tips': 'Think "counter + clockwise" - the opposite direction from clock hands',
        'alternate_spellings': 'Anticlockwise (British)',
        'language_origin': 'English',
        'example_sentence': 'Turn the jar lid _____ to loosen it from the threads.'
    },
    'counterfeit': {
        'definition': 'Made in exact imitation of something valuable with intent to deceive or defraud; fake or fraudulent. As a verb, counterfeit means to forge or imitate illegally. Counterfeiting involves creating false versions of currency, documents, or branded goods to deceive others.',
        'part_of_speech': 'adjective, noun, verb',
        'pronunciation_guide': 'KOWN-tur-fit (/ˈkaʊntərfɪt/)',
        'etymology': 'From Old French "contrefait," from "contrefaire" (to imitate)',
        'memory_tips': 'Think "counter + fit" - something that fits counter to (opposite of) the real thing',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'The _____ twenty-dollar bills were detected by special ultraviolet scanners.'
    },
    'counterpart': {
        'definition': 'A person or thing that corresponds to or has the same function as another person or thing in a different place or situation; a duplicate or complement. Counterparts often exist in parallel organizations, matching roles, or equivalent positions across different contexts.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOWN-tur-part (/ˈkaʊntərˌpɑrt/)',
        'etymology': 'From "counter-" (corresponding) + "part" (portion, role)',
        'memory_tips': 'Think "counter + part" - the corresponding part on the other side',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'The American ambassador met with her British _____ to discuss trade agreements.'
    },
    'countless': {
        'definition': 'Too many to be counted; innumerable or extremely numerous. This term indicates quantity so large that enumeration becomes impractical or impossible. Countless suggests vast numbers that exceed normal counting capacity or patience.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KOWNT-lis (/ˈkaʊntlɪs/)',
        'etymology': 'From "count" + suffix "-less" (without)',
        'memory_tips': 'Think "count + -less" - so many that you can\'t count them all',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'She made _____ attempts to reach him before finally giving up.'
    },
    'country': {
        'definition': 'A nation with its own government and borders; the land outside cities and towns; rural areas characterized by farming, open spaces, and small communities. Country can refer to sovereign states, countryside landscapes, or regions with distinct cultural identities.',
        'part_of_speech': 'noun, adjective',
        'pronunciation_guide': 'KUN-tree (/ˈkʌntri/)',
        'etymology': 'From Old French "contrée," from Latin "contra" (opposite, facing)',
        'memory_tips': 'Think of land that is "against" or "opposite" to urban areas - rural territory',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'They moved from the city to the _____ to enjoy a quieter lifestyle.'
    },
    'county': {
        'definition': 'An administrative division within a state or country, typically serving as a unit of local government. Counties often contain multiple cities, towns, and rural areas under unified administration. They provide regional services like law enforcement, courts, and public health programs.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOWN-tee (/ˈkaʊnti/)',
        'etymology': 'From Old French "conté," from Latin "comitatus" (territory of a count)',
        'memory_tips': 'Think "count + -y" - territory historically ruled by a count',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'The _____ sheriff was responsible for law enforcement in rural areas.'
    },
    'coup': {
        'definition': 'A sudden, illegal seizure of government power; a brilliant, successful stroke or move; a surprising achievement. Political coups involve overthrowing established authority through force or deception. In general usage, coup describes any sudden, decisive action that achieves remarkable success.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOO (/ku/)',
        'etymology': 'French, meaning "blow, stroke," from Latin "colpus"',
        'memory_tips': 'Think of a sudden "blow" or strike - a quick, decisive action',
        'alternate_spellings': 'None',
        'language_origin': 'French/Latin',
        'example_sentence': 'The military _____ overthrew the government in a single night.'
    },
    'coupon': {
        'definition': 'A voucher entitling the holder to a discount on a particular product or service; a detachable certificate used for obtaining goods, services, or discounts. Coupons serve as marketing tools to encourage purchases and customer loyalty while providing consumers with savings opportunities.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOO-pon (/ˈkupɒn/) or KYOO-pon (/ˈkjupɒn/)',
        'etymology': 'French, meaning "piece cut off," from "couper" (to cut)',
        'memory_tips': 'Think of something "cut off" or detached - a cut-out discount certificate',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The grocery store _____ saved her three dollars on laundry detergent.'
    },
    'courage': {
        'definition': 'The ability to do something that frightens or challenges you; mental or moral strength to persevere and withstand danger, fear, or difficulty. Courage involves facing adversity with determination despite natural instincts for self-preservation. It encompasses both physical bravery and moral fortitude.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KUR-ij (/ˈkɜrɪdʒ/)',
        'etymology': 'From Old French "corage," from Latin "cor" (heart)',
        'memory_tips': 'Think "cor (heart) + age" - having heart or spirit to face challenges',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'It took tremendous _____ for her to speak out against injustice.'
    },
    'courant': {
        'definition': 'Running or flowing; current or present; a lively baroque dance in triple time. In historical contexts, courant refers to newspapers or current events publications. As a dance term, it describes a spirited court dance popular in the 17th and 18th centuries.',
        'part_of_speech': 'adjective, noun',
        'pronunciation_guide': 'koo-RAHNT (/kuˈrɑnt/)',
        'etymology': 'French, meaning "running, current," from "courir" (to run)',
        'memory_tips': 'Think "current" - something running or flowing in the present time',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The baroque suite included a spirited _____ after the sarabande.'
    },
    'courgette': {
        'definition': 'British term for zucchini; a small vegetable marrow harvested when young and tender. Courgettes are cylindrical green squashes belonging to the cucumber and melon family. They\'re versatile vegetables used in numerous culinary applications from salads to baked goods.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'koor-ZHET (/kʊrˈʒɛt/)',
        'etymology': 'French, diminutive of "courge" (gourd, squash)',
        'memory_tips': 'Think "court + ette" - a small court-sized squash (British for zucchini)',
        'alternate_spellings': 'Zucchini (American)',
        'language_origin': 'French',
        'example_sentence': 'The garden produced an abundant harvest of _____ throughout the summer.'
    },
    'courier': {
        'definition': 'A person employed to deliver messages, packages, or mail, especially over long distances; a guide who accompanies travelers. Couriers provide specialized delivery services requiring speed, security, or personal attention. They often handle urgent, valuable, or confidential materials.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KUR-ee-ur (/ˈkɜriər/) or koo-ree-AY (/ˌkʊriˈeɪ/)',
        'etymology': 'From Old French "corier," from "courir" (to run)',
        'memory_tips': 'Think "courier runs" - someone who runs or travels to deliver messages',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'The diplomatic _____ carried sensitive documents between the embassies.'
    },
    'court': {
        'definition': 'A place where legal cases are heard and decided; the residence of a sovereign; an area marked for playing certain sports; to try to win favor or affection. Courts serve judicial, royal, or recreational functions depending on context.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KORT (/kɔrt/)',
        'etymology': 'From Old French "cort," from Latin "cohors" (enclosure, retinue)',
        'memory_tips': 'Think of an enclosed area where important activities happen - legal, royal, or sports',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'The basketball _____ was resurfaced before the new season began.'
    },
    'courtiers': {
        'definition': 'People who attend or frequent the court of a monarch; individuals seeking favor through flattery or attention to those in power. Courtiers historically formed the social circle around royalty, participating in court life, ceremonies, and political intrigue.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KOR-tee-urz (/ˈkɔrtiərz/)',
        'etymology': 'From Old French "cortier," from "cort" (court)',
        'memory_tips': 'Think "court + -iers" - people who hang around the royal court',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'The king\'s _____ competed for his attention and royal favors.'
    },
    'cousin': {
        'definition': 'A child of one\'s aunt or uncle; a relative descended from a common ancestor but not directly. Cousins share grandparents but have different parents. The term extends to describe people from related ethnic groups or similar cultural backgrounds.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KUZ-in (/ˈkʌzən/)',
        'etymology': 'From Old French "cosin," from Latin "consobrinus" (mother\'s sister\'s child)',
        'memory_tips': 'Think of "co + sin" - someone related through your family line',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'Her _____ from California visited during the summer holidays.'
    },
    'couverture': {
        'definition': 'High-quality chocolate with a high percentage of cocoa butter, used by professional chocolatiers and confectioners for coating and molding. Couverture chocolate melts smoothly, has excellent flavor, and creates glossy finishes. It requires tempering for proper crystallization and optimal texture.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'koo-vur-TOOR (/ˌkuvərˈtʊr/)',
        'etymology': 'French, meaning "covering, coating," from "couvrir" (to cover)',
        'memory_tips': 'Think "cover + ture" - chocolate that covers or coats confections beautifully',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The pastry chef used Belgian _____ to create perfectly tempered chocolate truffles.'
    },
    'couverturecreances': {
        'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "couverture" (high-quality chocolate) + "creances" (French for "claims" or "debts"). These should be separate words.',
        'part_of_speech': 'error - combined words',
        'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
        'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
        'memory_tips': 'This is a data error - should be separated into "couverture" and "creances"',
        'alternate_spellings': 'couverture + creances (separate words)',
        'language_origin': 'ERROR - combined words',
        'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
    },
    'cove': {
        'definition': 'A small, sheltered bay or inlet along a coastline; a concave molding or recess. Coves provide natural harbors protected from ocean swells and weather. In architecture, coves create smooth transitions between walls and ceilings or decorative recessed areas.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOHV (/koʊv/)',
        'etymology': 'From Old English "cofa" (chamber, cave)',
        'memory_tips': 'Think of a "cave" by the water - a sheltered inlet like a water cave',
        'alternate_spellings': 'None',
        'language_origin': 'Old English',
        'example_sentence': 'The secluded _____ offered perfect conditions for swimming and snorkeling.'
    },
    'covenant': {
        'definition': 'A formal agreement or contract between parties, especially one that is solemn and binding; in religious contexts, a sacred agreement between God and humanity. Covenants establish mutual obligations, promises, and commitments that are considered inviolable and often have spiritual significance.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KUV-uh-nuhnt (/ˈkʌvənənt/)',
        'etymology': 'From Old French "covenant," from Latin "convenire" (to come together)',
        'memory_tips': 'Think "co + vent" - coming together to vent or express mutual promises',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'The marriage _____ represented their sacred commitment to each other.'
    },
    'cover': {
        'definition': 'To place something over or in front of something else to protect, hide, or enclose; a thing that lies on, over, or around something; to deal with or include a topic. Cover serves protective, concealing, or encompassing functions.',
        'part_of_speech': 'verb, noun',
        'pronunciation_guide': 'KUV-ur (/ˈkʌvər/)',
        'etymology': 'From Old French "covrir," from Latin "cooperire" (to cover completely)',
        'memory_tips': 'Think "co + over" - placing something over to protect or hide',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'Please _____ the food to keep it warm until dinner.'
    },
    'coverage': {
        'definition': 'The extent to which something is covered or dealt with; the amount of protection provided by insurance; the reporting of events by news media. Coverage indicates scope, completeness, or range of inclusion across various contexts.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KUV-ur-ij (/ˈkʌvərɪdʒ/)',
        'etymology': 'From "cover" + suffix "-age" (action, result)',
        'memory_tips': 'Think "cover + age" - the extent or amount of covering provided',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'The insurance _____ included protection against flood damage.'
    },
    'coveralls': {
        'definition': 'A one-piece garment combining shirt and trousers, worn over regular clothes to protect them during messy work. Coveralls provide full-body protection for mechanics, painters, farmers, and other workers exposed to dirt, chemicals, or hazardous materials.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KUV-ur-awlz (/ˈkʌvərˌɔlz/)',
        'etymology': 'From "cover" + "all" (everything)',
        'memory_tips': 'Think "cover + all" - one garment that covers all your regular clothes',
        'alternate_spellings': 'Overalls',
        'language_origin': 'English',
        'example_sentence': 'The mechanic put on _____ before working under the greasy car engine.'
    },
    'coverley': {
        'definition': 'A type of English country dance, also known as "Sir Roger de Coverley," typically performed at celebrations and folk gatherings. This traditional dance involves couples in long lines performing various figures and movements. It\'s particularly associated with English cultural traditions and country festivities.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KUV-ur-lee (/ˈkʌvərli/)',
        'etymology': 'From "Sir Roger de Coverley," a traditional English country dance',
        'memory_tips': 'Think "cover + ley (field)" - a dance performed in country fields or gatherings',
        'alternate_spellings': 'Sir Roger de Coverley',
        'language_origin': 'English',
        'example_sentence': 'The folk festival concluded with everyone dancing the traditional _____.'
    },
    'covetous': {
        'definition': 'Having or showing a great desire to possess something belonging to someone else; extremely envious or greedy. Covetousness involves wanting what others have, often leading to resentment, theft, or unethical behavior. This attitude conflicts with contentment and gratitude.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KUV-i-tus (/ˈkʌvɪtəs/)',
        'etymology': 'From Old French "coveitos," from Latin "cupiditas" (desire)',
        'memory_tips': 'Think "covet + -ous" - full of coveting or wanting what others have',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'His _____ eyes followed every expensive car that passed by.'
    },
    'cowlick': {
        'definition': 'A section of hair that grows in a different direction from the rest, creating a tuft or swirl that resists combing flat. Cowlicks are natural growth patterns determined by hair follicle direction and are often most noticeable on the crown or forehead. They can be challenging to style.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOW-lik (/ˈkaʊˌlɪk/)',
        'etymology': 'From the appearance of hair licked by a cow\'s rough tongue',
        'memory_tips': 'Think "cow + lick" - hair that looks like a cow licked it, making it stick up',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'No amount of gel could tame his stubborn _____ that always stuck up.'
    },
    'cozen': {
        'definition': 'To deceive or trick someone, typically in order to obtain something from them; to cheat or defraud through cunning or fraud. Cozening involves gaining someone\'s trust before exploiting them, often through smooth talking or false promises.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'KUZ-n (/ˈkʌzən/)',
        'etymology': 'Origin uncertain, possibly from Old French "cousiner" (to claim kinship)',
        'memory_tips': 'Think "cousin" - like falsely claiming to be a cousin to gain trust and deceive',
        'alternate_spellings': 'None',
        'language_origin': 'Uncertain (possibly Old French)',
        'example_sentence': 'The con artist tried to _____ elderly residents out of their savings.'
    },
    'cradle': {
        'definition': 'A small bed for a baby, typically one that rocks; the place or environment in which something begins or develops; to hold gently and protectively. Cradles provide security and comfort for infants. Metaphorically, cradles represent origins or nurturing environments.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KRAY-dl (/ˈkreɪdəl/)',
        'etymology': 'From Old English "cradol," related to "craddle" (basket)',
        'memory_tips': 'Think of gently rocking a baby - a protective bed that rocks and soothes',
        'alternate_spellings': 'None',
        'language_origin': 'Old English',
        'example_sentence': 'She gently placed the sleeping infant in the wooden _____.'
    },
    'crafty': {
        'definition': 'Skillful in achieving goals through indirect or deceitful methods; clever in a cunning or sly way; showing skill in making things by hand. Crafty can describe both negative cunning and positive creative ability, depending on context.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KRAF-tee (/ˈkræfti/)',
        'etymology': 'From "craft" (skill, cunning) + suffix "-y"',
        'memory_tips': 'Think "craft + -y" - either skilled at crafts or skilled at cunning schemes',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'The _____ fox found a way to reach the grapes despite the high fence.'
    },
    'cranium': {
        'definition': 'The skull, especially the part that encloses the brain; the bony structure forming the head in vertebrates. The cranium protects the brain and provides attachment points for muscles. It consists of multiple bones fused together in adults.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KRAY-nee-um (/ˈkreɪniəm/)',
        'etymology': 'From Medieval Latin "cranium," from Greek "kranion" (skull)',
        'memory_tips': 'Think "crane (bird) + -ium" - the bony structure like a bird\'s head',
        'alternate_spellings': 'None',
        'language_origin': 'Greek/Latin',
        'example_sentence': 'The archaeologist carefully excavated the ancient _____ from the burial site.'
    },
    'cranky': {
        'definition': 'Bad-tempered, irritable, or easily annoyed; (of machinery) unreliable or prone to malfunction. Cranky describes emotional states characterized by impatience, grumpiness, or general dissatisfaction. It can apply to people or mechanical devices.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KRANG-kee (/ˈkræŋki/)',
        'etymology': 'From "crank" (twisted, bent) + suffix "-y"',
        'memory_tips': 'Think of someone whose mood is "cranked" or twisted into irritability',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'The baby became _____ when his nap was interrupted.'
    }
}

def process_batch():
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_043_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_043_processed.csv'
    
    try:
        df = pd.read_csv(input_file)
        print(f"Processing {len(df)} words from batch 043...")
        
        processed_data = []
        combined_word_errors = []
        
        for _, row in df.iterrows():
            word = row['word'].strip()
            if word in batch_043_data:
                data = batch_043_data[word]
                
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