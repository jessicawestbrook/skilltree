import csv
import os

class DifficultyCalculator:
    def calculate_difficulty_score(self, word, pronunciation, etymology):
        phonetic_score = self._calculate_phonetic_transparency(word, pronunciation)
        frequency_score = self._calculate_word_frequency(word)
        morphological_score = self._calculate_morphological_complexity(word)
        etymology_score = self._calculate_etymology_complexity(etymology)
        
        total_score = phonetic_score + frequency_score + morphological_score + etymology_score
        return phonetic_score, frequency_score, morphological_score, etymology_score, total_score
    
    def _calculate_phonetic_transparency(self, word, pronunciation):
        if not pronunciation:
            return 1.5
        
        phonetic_irregularities = 0
        
        # Silent letters
        silent_patterns = ['gh', 'kn', 'wr', 'mb', 'bt', 'sc']
        for pattern in silent_patterns:
            if pattern in word.lower():
                phonetic_irregularities += 1
        
        # Irregular vowel patterns
        irregular_vowels = ['ough', 'augh', 'eigh', 'igh']
        for pattern in irregular_vowels:
            if pattern in word.lower():
                phonetic_irregularities += 1
        
        # Foreign phonetic patterns
        foreign_patterns = ['ch' if word.lower().startswith('ch') and 'k' in pronunciation.lower() else '',
                          'ph', 'gh', 'x' if word.lower().startswith('x') and 'z' in pronunciation.lower() else '']
        foreign_patterns = [p for p in foreign_patterns if p]
        
        for pattern in foreign_patterns:
            if pattern and pattern in word.lower():
                phonetic_irregularities += 1
        
        base_score = min(phonetic_irregularities * 0.3, 2.0)
        return base_score if base_score > 0 else 0.1
    
    def _calculate_word_frequency(self, word):
        common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'day', 'get', 'use', 'man', 'new', 'now', 'way', 'may', 'say', 'each', 'which', 'their', 'time', 'will', 'about', 'if', 'up', 'out', 'many', 'then', 'them', 'these', 'so', 'some', 'would', 'make', 'like', 'into', 'him', 'has', 'more', 'go', 'no', 'do', 'than', 'first', 'been', 'its', 'who', 'oil', 'sit', 'now', 'find', 'long', 'down', 'day', 'did', 'get', 'come', 'made', 'may', 'part']
        
        very_common_words = ['a', 'an', 'the', 'is', 'it', 'to', 'of', 'in', 'on', 'at', 'be', 'or', 'as', 'have', 'do', 'they', 'we', 'he', 'she', 'i', 'me', 'my', 'this', 'that', 'with', 'from', 'by', 'up', 'out', 'off', 'over', 'under', 'again', 'further', 'then', 'once']
        
        word_lower = word.lower()
        
        if word_lower in very_common_words:
            return 0.1
        elif word_lower in common_words:
            return 0.3
        elif len(word) <= 4:
            return 0.5
        elif len(word) <= 6:
            return 1.0
        elif len(word) <= 8:
            return 1.5
        else:
            return 2.0
    
    def _calculate_morphological_complexity(self, word):
        complexity_score = 0
        
        # Length-based complexity
        if len(word) >= 10:
            complexity_score += 1.0
        elif len(word) >= 8:
            complexity_score += 0.7
        elif len(word) >= 6:
            complexity_score += 0.4
        
        # Prefix/suffix complexity
        complex_prefixes = ['anti', 'auto', 'circum', 'counter', 'extra', 'hyper', 'inter', 'macro', 'micro', 'multi', 'over', 'post', 'pre', 'proto', 'pseudo', 'semi', 'sub', 'super', 'trans', 'ultra', 'under']
        complex_suffixes = ['tion', 'sion', 'ment', 'ness', 'ity', 'ous', 'ful', 'less', 'able', 'ible', 'ize', 'ise', 'fy', 'ward', 'wise', 'like', 'ship', 'hood', 'dom', 'acy', 'ary', 'ery', 'ory']
        
        word_lower = word.lower()
        for prefix in complex_prefixes:
            if word_lower.startswith(prefix):
                complexity_score += 0.3
                break
        
        for suffix in complex_suffixes:
            if word_lower.endswith(suffix):
                complexity_score += 0.3
                break
        
        # Consonant clusters
        consonant_clusters = ['str', 'scr', 'thr', 'shr', 'spl', 'spr', 'squ', 'chr', 'phr', 'tch', 'dge', 'nch', 'rch', 'lch']
        for cluster in consonant_clusters:
            if cluster in word_lower:
                complexity_score += 0.2
        
        return min(complexity_score, 2.0)
    
    def _calculate_etymology_complexity(self, etymology):
        if not etymology:
            return 1.0
        
        etymology_lower = etymology.lower()
        complexity_score = 0
        
        # Language origin complexity
        high_complexity_origins = ['sanskrit', 'arabic', 'chinese', 'japanese', 'hebrew', 'hungarian', 'finnish', 'nahuatl', 'quechua']
        medium_complexity_origins = ['greek', 'latin', 'german', 'dutch', 'russian', 'polish', 'czech', 'turkish', 'persian']
        
        for origin in high_complexity_origins:
            if origin in etymology_lower:
                complexity_score += 1.5
                break
        else:
            for origin in medium_complexity_origins:
                if origin in etymology_lower:
                    complexity_score += 1.0
                    break
            else:
                if any(lang in etymology_lower for lang in ['french', 'spanish', 'italian', 'portuguese']):
                    complexity_score += 0.7
                elif 'english' in etymology_lower or 'germanic' in etymology_lower:
                    complexity_score += 0.3
        
        # Multiple language origins
        language_indicators = ['from', 'via', 'through', 'borrowed', 'derived', 'ultimately']
        origin_count = sum(1 for indicator in language_indicators if indicator in etymology_lower)
        if origin_count >= 2:
            complexity_score += 0.5
        
        return min(complexity_score, 2.0)

def process_batch():
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_158_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_158_processed.csv'
    
    calculator = DifficultyCalculator()
    
    word_data = {
        'serious': {
            'word': 'serious',
            'definition': 'Characterized by careful consideration, gravity, or solemnity; not trivial, joking, or superficial in nature. A serious attitude involves thoughtful attention to important matters and recognition of their significance or potential consequences. People who are serious about something demonstrate commitment, dedication, and earnest engagement rather than casual or playful approaches. The term can describe situations, problems, or conditions that are severe, significant, or requiring immediate attention, such as serious injuries or serious threats. In academic or professional contexts, serious work reflects thorough research, rigorous methodology, and substantial effort. Serious can also indicate sincerity and genuineness, distinguishing authentic intentions from casual or insincere ones. The word implies depth, importance, and the absence of frivolity.',
            'pronunciation': '/ˈsɪriəs/',
            'etymology': 'From Latin serius meaning grave, earnest, or weighty.',
            'memory_tip': 'Think "SER-IOUS" - so serious it\'s like a series of important, weighty matters.',
            'example_sentence': 'The doctor explained that the patient\'s condition was _____ and required immediate surgery.',
            'part_of_speech': 'adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'serpentine': {
            'word': 'serpentine',
            'definition': 'Having a winding, twisting course like that of a snake; characterized by curves, turns, and sinuous movement patterns. Serpentine paths, roads, or rivers follow meandering routes rather than straight lines, often following natural terrain contours or designed for aesthetic purposes. In geology, serpentine refers to a group of minerals with a smooth, waxy feel and greenish color, formed through the alteration of certain rock types. These minerals were named for their snake-like appearance and texture. Serpentine can also describe behavior or movements that are subtle, cunning, or devious, drawing on the symbolic associations of snakes with deception. In dance or physical movement, serpentine describes fluid, undulating motions that mimic the graceful movement of snakes. The word emphasizes the characteristic of following a curved, winding pattern.',
            'pronunciation': '/ˈsɜːrpənˌtaɪn/',
            'etymology': 'From Latin serpentinus meaning snake-like, from serpens meaning serpent or snake.',
            'memory_tip': 'Think "SERPENT-INE" - like a serpent, winding and twisting in snake-like patterns.',
            'example_sentence': 'The _____ mountain road twisted through dozens of hairpin turns as it climbed to the summit.',
            'part_of_speech': 'adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'serrao': {
            'word': 'serrao',
            'definition': 'A Portuguese term referring to a mountainous or hilly region, particularly the highland areas of Portugal and Brazil characterized by elevated terrain, rocky landscapes, and distinct ecological zones. In geographic contexts, serrao describes areas with significant elevation changes, often featuring steep slopes, valleys, and diverse microclimates. These regions are typically important for agriculture, particularly viticulture in Portugal, where many famous wine regions are located in serrao areas. The term also appears in place names throughout Portuguese-speaking regions, indicating locations with characteristic mountainous topography. In Brazilian Portuguese, serrao can refer to specific highland regions that have unique cultural, economic, and environmental significance. The word emphasizes the geographic and topographic features that distinguish these elevated areas from surrounding lowlands.',
            'pronunciation': '/seˈrɐ̃w/',
            'etymology': 'From Portuguese serra meaning mountain range or saw, referring to the jagged appearance of mountain ridges.',
            'memory_tip': 'Think "SER-RAO" - Portuguese for mountainous areas where you see (ser) raw, rugged terrain.',
            'example_sentence': 'The wine estate was located in the _____ region, where the altitude and climate created ideal growing conditions.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'serrated': {
            'word': 'serrated',
            'definition': 'Having a notched edge with a series of sharp, tooth-like projections, similar to the cutting edge of a saw. Serrated edges are designed to improve cutting efficiency through materials that might resist smooth blades, such as bread, tomatoes, or fibrous substances. The tooth-like pattern creates multiple cutting points that grip and slice through materials more effectively than straight edges. In nature, many leaves, such as those of roses or elm trees, have serrated margins that may help with water drainage or defense against herbivores. Serrated knives are common kitchen tools, particularly bread knives and steak knives. The term can also describe any edge or border that has a jagged, tooth-like appearance, whether natural or manufactured. The serration pattern varies in size and spacing depending on the intended use.',
            'pronunciation': '/ˈsɛreɪtɪd/',
            'etymology': 'From Latin serratus meaning saw-toothed, from serra meaning saw.',
            'memory_tip': 'Think "SAW-RATED" - rated like a saw with tooth-like edges for better cutting.',
            'example_sentence': 'The _____ knife blade easily cut through the crusty sourdough bread without crushing it.',
            'part_of_speech': 'adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'serratedpoblano': {
            'word': 'serratedpoblano',
            'definition': '[COMBINED WORD ERROR] This appears to be two words combined: "serrated" (having tooth-like notches) and "poblano" (a type of mild chili pepper). This combination likely resulted from a data processing error where two separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words with their individual meanings and contexts.',
            'pronunciation': '/ˈsɛreɪtɪdpoʊˈblɑːnoʊ/',
            'etymology': 'Error combination of Latin serratus (serrated) + Spanish poblano (from Puebla)',
            'memory_tip': 'This is a combined word error - look for the separation between serrated and poblano.',
            'example_sentence': 'The data contained an error where _____ appeared instead of two separate words.',
            'part_of_speech': 'error',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'serricorn': {
            'word': 'serricorn',
            'definition': 'Having saw-toothed or serrated antennae, particularly used to describe certain beetles and other insects whose antennae feature comb-like or notched projections resembling the teeth of a saw. This term is primarily used in entomological classification to describe morphological characteristics that help identify different insect species and families. Serricorn beetles include various species where males especially may have elaborately serrated antennae used for detecting pheromones or during mating behaviors. The serrated structure increases the surface area of the antennae, enhancing their sensory capabilities. These antennae may appear feathery, comb-like, or distinctly notched depending on the species. Understanding serricorn characteristics helps entomologists classify insects and understand their behavior, ecology, and evolutionary relationships. The term represents one of many specialized descriptors used in taxonomic identification.',
            'pronunciation': '/ˈsɛrɪˌkɔrn/',
            'etymology': 'From Latin serri- meaning saw + cornu meaning horn, referring to saw-like antennae.',
            'memory_tip': 'Think "SERRI-CORN" - insects with antennae like serrated corn cobs or saw-toothed horns.',
            'example_sentence': 'The entomologist identified the beetle as _____ based on its distinctive saw-toothed antennae.',
            'part_of_speech': 'adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'serum': {
            'word': 'serum',
            'definition': 'The clear, yellowish liquid component of blood that remains after blood cells and clotting factors have been removed, containing water, proteins, electrolytes, antibodies, and other dissolved substances. Medical serum is used in diagnostic testing to measure various blood components, including cholesterol, glucose, proteins, and antibodies. Immune serum contains specific antibodies and can be used therapeutically to provide passive immunity against diseases. In cosmetics and skincare, serums are concentrated liquid treatments containing high levels of active ingredients designed to penetrate skin and address specific concerns like aging, hydration, or pigmentation. Laboratory serum serves as a crucial component in cell culture media for growing cells in research. The term can also refer to any clear liquid derived from biological sources for therapeutic or research purposes.',
            'pronunciation': '/ˈsɪrəm/',
            'etymology': 'From Latin serum meaning whey, the watery part separated from milk.',
            'memory_tip': 'Think "SEER-UM" - a clear liquid that allows medical professionals to see into your health.',
            'example_sentence': 'The blood _____ revealed elevated cholesterol levels during the annual health screening.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'serval': {
            'word': 'serval',
            'definition': 'A medium-sized African wild cat (Leptailurus serval) characterized by a lean build, extremely long legs, large ears, and a golden-yellow coat with distinctive black spots and stripes. Servals are exceptional hunters, using their oversized ears to locate prey and their powerful legs to leap up to 10 feet horizontally to catch birds in flight. They inhabit savannas, grasslands, and wetlands across sub-Saharan Africa, preferring areas with tall grass and water sources. Servals primarily hunt small mammals, birds, frogs, and insects, with an unusually high success rate for feline hunters. Their unique physical adaptations make them highly specialized for their environment and hunting style. Some servals are kept as exotic pets, though this practice is controversial and heavily regulated. Conservation status varies by region, with some populations threatened by habitat loss and hunting.',
            'pronunciation': '/ˈsɜrvəl/',
            'etymology': 'From Portuguese cerval, from Latin cervus meaning deer, though the connection is unclear.',
            'memory_tip': 'Think "SER-VAL" - a wild cat that serves as an excellent valley hunter with long legs.',
            'example_sentence': 'The _____ used its exceptional hearing to locate a rodent hidden in the tall grass.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'served': {
            'word': 'served',
            'definition': 'Past tense of serve, meaning to have provided assistance, food, or service to others; to have performed duties or functions in a particular role or capacity. The word encompasses various meanings including having worked in a position (served as president), having provided food or drinks (served dinner), having fulfilled a purpose (served its function), or having delivered legal documents (served papers). In military contexts, served indicates completion of duty or enlistment periods. In sports, it refers to having put the ball or shuttlecock into play. The term can also mean having been adequate or sufficient for a purpose, or having treated someone in a particular manner. Served emphasizes the completion of an action involving assistance, duty, or provision of something to others.',
            'pronunciation': '/sɜrvd/',
            'etymology': 'From Old French servir, from Latin servire meaning to serve or be a slave.',
            'memory_tip': 'Think "SERV-ED" - having completed the action of serving others in some capacity.',
            'example_sentence': 'She _____ as a volunteer coordinator for five years before accepting a paid position.',
            'part_of_speech': 'verb (past tense)',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'serves': {
            'word': 'serves',
            'definition': 'Third-person singular present tense of serve, meaning to provide assistance, food, or service to others; to perform duties or functions in a particular capacity. The word encompasses various meanings including working in a position, providing food or drinks, fulfilling a purpose, or delivering legal documents. In tennis and other racquet sports, serves refers to putting the ball into play to start each point. The term can indicate adequacy or sufficiency for a purpose, or describe how someone treats another person. Serves can also mean to be useful or beneficial for a particular goal or need. The word emphasizes ongoing action involving assistance, duty, or provision of something to others, whether in professional, personal, or functional contexts.',
            'pronunciation': '/sɜrvz/',
            'etymology': 'From Old French servir, from Latin servire meaning to serve + -s third person singular suffix.',
            'memory_tip': 'Think "SERV-ES" - what someone does when they serve others regularly.',
            'example_sentence': 'The community center _____ over 500 meals to homeless individuals each week.',
            'part_of_speech': 'verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'service': {
            'word': 'service',
            'definition': 'The action of helping or providing assistance to others; work performed for someone else or for a community, organization, or cause. Service encompasses a wide range of activities from professional services (medical, legal, financial) to public service (government, military, emergency response) to personal service (hospitality, retail, domestic help). The concept includes both paid employment and voluntary work performed for the benefit of others. Quality service involves meeting or exceeding customer expectations, providing value, and maintaining professional standards. In religious contexts, service refers to worship ceremonies or devotional acts. Military service involves duty to one\'s country. The term also applies to the maintenance and repair of equipment, vehicles, or systems. Service emphasizes contribution to others\' welfare and needs.',
            'pronunciation': '/ˈsɜrvɪs/',
            'etymology': 'From Old French service, from Latin servitium meaning slavery or service.',
            'memory_tip': 'Think "SERV-ICE" - serving others, whether in ice-cold professionalism or warm hospitality.',
            'example_sentence': 'The restaurant was known for its excellent food and exceptional customer _____.',
            'part_of_speech': 'noun/verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'services': {
            'word': 'services',
            'definition': 'Plural of service, referring to multiple forms of work performed for others, assistance provided, or systems that supply public needs. Services encompass various categories including professional services (healthcare, education, legal, financial), public services (utilities, transportation, emergency response), and personal services (hospitality, retail, entertainment). In economics, the service sector represents a major portion of modern economies, distinguished from goods-producing industries. Digital services include online platforms, software applications, and technological solutions. Religious services are organized worship gatherings or ceremonies. The term can also refer to maintenance and repair work performed on equipment, vehicles, or systems. Services emphasize meeting human needs through expertise, assistance, and support rather than through physical products.',
            'pronunciation': '/ˈsɜrvɪsɪz/',
            'etymology': 'Plural of service, from Old French service, from Latin servitium.',
            'memory_tip': 'Think "SERV-ICES" - multiple types of service, like different flavors of assistance.',
            'example_sentence': 'The company expanded its _____ to include consulting, training, and technical support.',
            'part_of_speech': 'noun (plural)',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'servitude': {
            'word': 'servitude',
            'definition': 'The state of being enslaved or subject to someone in a position of authority; a condition of forced or compulsory service where personal freedom is severely restricted. Servitude can take various forms, from historical slavery and indentured labor to modern forms of human trafficking and debt bondage. The term encompasses situations where individuals are compelled to work against their will, often under threat of punishment or due to coercion. Legal servitude historically included systems where people owed labor obligations in exchange for land use or protection. In property law, servitude refers to a burden placed on land for the benefit of another property. The concept represents a fundamental violation of human rights and personal autonomy, and international law prohibits all forms of involuntary servitude. Modern anti-trafficking efforts focus on identifying and eliminating contemporary forms of servitude.',
            'pronunciation': '/ˈsɜrvɪˌtud/',
            'etymology': 'From Latin servitudo meaning slavery or bondage, from servus meaning slave.',
            'memory_tip': 'Think "SERV-ITUDE" - an attitude of being forced to serve others without freedom.',
            'example_sentence': 'The 13th Amendment to the Constitution abolished slavery and involuntary _____.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'sesame': {
            'word': 'sesame',
            'definition': 'An annual flowering plant (Sesamum indicum) cultivated for its small, oil-rich seeds that are used as food and flavoring in cuisines worldwide. Sesame seeds are prized for their nutty flavor and nutritional value, containing high levels of healthy fats, protein, fiber, and minerals including calcium and magnesium. The seeds are commonly used in baking, cooking, and as garnishes, particularly in Middle Eastern, Asian, and Mediterranean cuisines. Tahini, a paste made from ground sesame seeds, is a key ingredient in hummus and other dishes. Sesame oil is valued for cooking and flavoring, particularly in Asian cuisine. The phrase "open sesame" from Arabian Nights folklore has made the word synonymous with magical access or passwords. Sesame cultivation dates back thousands of years and the plant is considered one of humanity\'s oldest oil crops.',
            'pronunciation': '/ˈsɛsəmi/',
            'etymology': 'From Latin sesamum, from Greek σήσαμον (sesamon), possibly from a Semitic language.',
            'memory_tip': 'Think "SES-A-ME" - seeds that give me (ses-a-me) great flavor in cooking.',
            'example_sentence': 'The bagel was topped with _____ seeds that added a nutty flavor and crunchy texture.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'sesquipedalian': {
            'word': 'sesquipedalian',
            'definition': 'Characterized by the use of long words; having many syllables or characterized by sesquipedality. The term ironically exemplifies what it describes - it is itself a long, multisyllabic word. Sesquipedalian language or writing style involves the use of unnecessarily long or complex words when simpler alternatives would suffice, often creating an impression of pomposity or pretentiousness. While extensive vocabulary can demonstrate education and precision, sesquipedalian tendencies may hinder clear communication by making text difficult to understand. In linguistics and rhetoric, the term describes a style that prioritizes impressive-sounding words over clarity and accessibility. Some academic and technical writing is necessarily sesquipedalian due to precise terminology requirements, but deliberate use of complex words for their own sake is generally discouraged in effective communication.',
            'pronunciation': '/ˌsɛskwɪpɪˈdeɪliən/',
            'etymology': 'From Latin sesquipedalis meaning a foot and a half long, from sesqui (one and a half) + pes (foot).',
            'memory_tip': 'Think "SESQUI-PEDALIAN" - words that are one-and-a-half feet long, like this very word!',
            'example_sentence': 'The professor\'s _____ lecture style made simple concepts unnecessarily difficult to understand.',
            'part_of_speech': 'adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'sessile': {
            'word': 'sessile',
            'definition': 'In biology, describing organisms that are permanently attached to a surface and cannot move from place to place, such as barnacles, corals, many plants, and certain marine animals. Sessile organisms have evolved various strategies to obtain food, reproduce, and survive without the ability to relocate, often developing specialized feeding mechanisms, reproductive systems, and defensive adaptations. Examples include sea anemones that filter food from water currents, barnacles that extend feathery appendages to capture plankton, and plants that rely on wind or animals for pollination and seed dispersal. In botany, sessile also describes plant parts that lack stalks or stems, such as leaves that attach directly to branches without petioles. The sessile lifestyle presents both advantages (energy conservation, stable environment) and challenges (limited resource access, vulnerability to local environmental changes).',
            'pronunciation': '/ˈsɛsaɪl/',
            'etymology': 'From Latin sessilis meaning able to sit, from sedere meaning to sit.',
            'memory_tip': 'Think "SESS-ILE" - organisms that sit in one place for their whole session of life.',
            'example_sentence': 'The _____ coral polyps could not move to escape the rising water temperatures.',
            'part_of_speech': 'adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'seton': {
            'word': 'seton',
            'definition': 'A medical device consisting of a thread, wire, or tube that is passed through tissue to create and maintain an artificial opening for drainage or healing purposes. Setons are commonly used in treating certain types of abscesses, fistulas, and anal conditions where conventional surgery might cause complications. The device allows infected material to drain while keeping the pathway open, promoting healing from the inside out. In veterinary medicine, setons may be used to treat similar conditions in animals. The placement of a seton requires surgical skill and careful monitoring to ensure proper healing and prevent complications. Historical medical texts describe various types of setons made from different materials including silk, horsehair, and metal wires. Modern setons are typically made from synthetic materials designed to be biocompatible and minimize tissue reaction.',
            'pronunciation': '/ˈsiːtən/',
            'etymology': 'From Latin seta meaning bristle or hair, referring to the thread-like device.',
            'memory_tip': 'Think "SET-ON" - a device that\'s set on or through tissue for medical drainage.',
            'example_sentence': 'The surgeon placed a _____ to allow the infected area to drain properly during healing.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'setondemerits': {
            'word': 'setondemerits',
            'definition': '[COMBINED WORD ERROR] This appears to be multiple words combined: "seton" (a medical drainage device), "de" (a preposition), and "merits" (good qualities or advantages). This combination likely resulted from a data processing error where separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words with their individual meanings and contexts.',
            'pronunciation': '/ˈsiːtəndɪˈmɛrɪts/',
            'etymology': 'Error combination of Latin seta (seton) + Latin de + merits',
            'memory_tip': 'This is a combined word error - look for the separation between seton, de, and merits.',
            'example_sentence': 'The data contained an error where _____ appeared instead of three separate words.',
            'part_of_speech': 'error',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'sets': {
            'word': 'sets',
            'definition': 'Plural of set, referring to multiple groups, collections, or arrangements of related items, people, or concepts organized together according to shared characteristics or purposes. Sets can describe physical objects (a set of dishes, tools, or books), mathematical concepts (collections of numbers or elements), or abstract groupings (sets of rules, principles, or ideas). In mathematics, sets are fundamental concepts representing collections of distinct objects considered as a whole. Theater sets are constructed environments for dramatic performances. Exercise sets involve repeated sequences of physical movements. The term emphasizes organization, completeness, and the relationship between individual elements that belong together. Sets can be finite or infinite, overlapping or distinct, depending on the context and defining criteria.',
            'pronunciation': '/sɛts/',
            'etymology': 'Plural of set, from Old English settan meaning to place or put.',
            'memory_tip': 'Think "SETS" - multiple groups that are set together for specific purposes.',
            'example_sentence': 'The mathematics student learned about different _____ of numbers including integers and rational numbers.',
            'part_of_speech': 'noun (plural)/verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'settee': {
            'word': 'settee',
            'definition': 'A piece of furniture designed for seating two or more people, similar to a sofa but typically smaller and more formal in design, often featuring upholstered seats and backs with wooden frames. Settees originated in the 17th century as elegant seating furniture for drawing rooms and parlors, representing a bridge between individual chairs and larger sofas. Traditional settees often feature distinctive styling with carved wooden legs, decorative upholstery, and proportions that accommodate intimate conversation while maintaining formal appearance. The design typically includes arms and a back, distinguishing it from benches, but remains more compact than full-sized sofas. Modern settees may serve various purposes including entryway seating, bedroom furniture, or accent pieces in living areas. The term reflects historical furniture terminology and remains popular in describing certain styles of compact, elegant seating.',
            'pronunciation': '/sɛˈti/',
            'etymology': 'Possibly a variant of settle, influenced by French furniture terminology.',
            'memory_tip': 'Think "SET-TEE" - a place where you can set down for tea with a friend.',
            'example_sentence': 'The antique _____ in the parlor was upholstered in rich velvet fabric.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'settle': {
            'word': 'settle',
            'definition': 'To establish residence in a new place; to resolve a dispute or disagreement; to become calm or stable after a period of activity or disturbance. The word encompasses various meanings including making a home in a location, reaching agreement on contested issues, paying debts or obligations, and achieving a state of rest or equilibrium. Settling can involve physical actions (settling into a chair), emotional states (settling nerves), or social processes (settling differences). In legal contexts, settling refers to resolving disputes outside of court through negotiation and agreement. Environmental settling involves particles sinking through liquids due to gravity. The term emphasizes transition from activity to stability, from conflict to resolution, or from temporary to permanent arrangements.',
            'pronunciation': '/ˈsɛtəl/',
            'etymology': 'From Old English setlan meaning to place, seat, or colonize.',
            'memory_tip': 'Think "SET-TLE" - to set something down until it\'s stable and settled.',
            'example_sentence': 'The family decided to _____ in the small town after years of traveling.',
            'part_of_speech': 'verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'seul': {
            'word': 'seul',
            'definition': 'A French word meaning "alone" or "only," used in English primarily in specific contexts such as dance (particularly ballet), literature, or when describing solitary performances or activities. In ballet terminology, "seul" may appear in combination with other French terms to describe solo movements or positions performed by a single dancer. The word emphasizes solitude, independence, or the state of being without others. In literary or artistic contexts, seul might be used to convey a sense of isolation, contemplation, or individual expression. While primarily a French word, it occasionally appears in English texts to add nuance or cultural specificity, particularly in discussions of French culture, literature, or performance arts. The usage reflects the international nature of certain artistic vocabularies.',
            'pronunciation': '/sœl/',
            'etymology': 'From French seul meaning alone, from Latin solus meaning alone or only.',
            'memory_tip': 'Think "SOUL" - when you\'re seul (alone), you\'re just with your soul.',
            'example_sentence': 'The dancer performed a beautiful _____ variation that showcased her technical skill.',
            'part_of_speech': 'adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'seven': {
            'word': 'seven',
            'definition': 'The cardinal number following six and preceding eight, represented by the numeral 7. Seven has significant cultural, religious, and symbolic importance across many civilizations, appearing in contexts such as the seven days of the week, seven deadly sins, seven wonders of the ancient world, and seven colors of the rainbow. In mathematics, seven is a prime number divisible only by one and itself. The number appears frequently in folklore, mythology, and religious texts, often associated with completeness, perfection, or spiritual significance. Psychological research suggests seven is near the limit of items that can be held in short-term memory simultaneously. The concept of "lucky seven" appears in various gambling and cultural contexts. Seven-based systems appear in music (seven notes in major scales), literature, and numerous other fields.',
            'pronunciation': '/ˈsɛvən/',
            'etymology': 'From Old English seofon, related to German sieben and Latin septem.',
            'memory_tip': 'Think "SEV-EN" - the number that comes after six and gives us seven days per week.',
            'example_sentence': 'There are _____ continents on Earth according to the most common geographic classification.',
            'part_of_speech': 'number/noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'seventh': {
            'word': 'seventh',
            'definition': 'The ordinal number corresponding to the position of seven in a sequence; coming after the sixth and before the eighth in order. Seventh can refer to one of seven equal parts of a whole, as in "one-seventh of the pie." In music, a seventh is an interval spanning seven scale degrees, creating harmonies that add complexity and color to musical compositions. The term appears in various cultural and religious contexts, such as the seventh day of the week (traditionally a day of rest), seventh heaven (a state of bliss), or seventh-grade education. Mathematical contexts use seventh to describe position, fractions, or sequence order. The word emphasizes numerical order and fractional relationships, whether in time, space, music, or abstract concepts.',
            'pronunciation': '/ˈsɛvənθ/',
            'etymology': 'From seven + -th ordinal suffix, from Old English seofoða.',
            'memory_tip': 'Think "SEVEN-TH" - the ordinal form of seven, showing position in sequence.',
            'example_sentence': 'She finished in _____ place in the marathon, just missing her goal of a top-five finish.',
            'part_of_speech': 'adjective/noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'several': {
            'word': 'several',
            'definition': 'More than two but not many; an indefinite number that is more than a few but less than many. Several indicates a quantity that is greater than "a couple" but smaller than "many," typically suggesting anywhere from three to perhaps eight or ten items, depending on context. The word provides useful approximation when exact numbers are unknown, unnecessary, or deliberately vague. Several can apply to countable objects, people, time periods, or abstract concepts. In legal contexts, "several" can mean individual or distinct, as in "several liability" where each party is responsible only for their own portion. The term offers flexibility in communication, allowing speakers to indicate meaningful quantity without precision. Usage often depends on relative context - several books might mean three to five, while several people at a concert might suggest dozens.',
            'pronunciation': '/ˈsɛvərəl/',
            'etymology': 'From Anglo-French several, from Latin separalis meaning separate or distinct.',
            'memory_tip': 'Think "SEVER-AL" - more than a few, but you could sever them into separate, countable groups.',
            'example_sentence': 'The research team conducted _____ experiments before reaching their final conclusions.',
            'part_of_speech': 'determiner/pronoun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'severance': {
            'word': 'severance',
            'definition': 'The action of ending a connection or relationship; separation or division of something that was previously joined or united. In employment contexts, severance refers to the termination of the employment relationship, often accompanied by severance pay or benefits provided to departing employees. Severance packages may include financial compensation, continued health insurance, and other benefits to help employees transition to new employment. The term can apply to cutting physical connections (severance of cables), ending relationships (severance of diplomatic ties), or legal separation (severance of joint ownership). Medical severance involves cutting or separating anatomical structures. Legal severance may divide complex cases or separate co-defendants. The concept emphasizes the deliberate act of cutting or separating what was previously connected or unified.',
            'pronunciation': '/ˈsɛvərəns/',
            'etymology': 'From sever + -ance suffix, where sever comes from Latin separare meaning to separate.',
            'memory_tip': 'Think "SEVER-ANCE" - the action of severing or separating connections.',
            'example_sentence': 'The company offered a generous _____ package to employees affected by the downsizing.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'severe': {
            'word': 'severe',
            'definition': 'Extremely serious, harsh, or demanding; characterized by great intensity, strictness, or difficulty that may cause hardship or challenge. Severe conditions, whether weather, medical, or social, require significant attention and often specialized responses due to their intensity or potential consequences. The term describes situations that are notably more serious than normal or expected, such as severe storms, severe illnesses, or severe penalties. Severe can characterize people who are strict, demanding, or uncompromising in their approach to rules, standards, or behavior. In medical contexts, severe symptoms indicate conditions requiring immediate attention or intensive treatment. The word emphasizes the gravity, intensity, or harshness of situations that may test human endurance, patience, or capability. Severe circumstances often require extraordinary measures or responses.',
            'pronunciation': '/sɪˈvɪr/',
            'etymology': 'From Latin severus meaning stern, strict, or serious.',
            'memory_tip': 'Think "SE-VERE" - so serious it\'s like a severe test of endurance.',
            'example_sentence': 'The _____ thunderstorm caused widespread power outages and flooding.',
            'part_of_speech': 'adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'sewage': {
            'word': 'sewage',
            'definition': 'Wastewater and excrement conveyed through sewers from homes, businesses, and industries to treatment facilities for processing and disposal. Sewage systems are essential infrastructure for public health, environmental protection, and urban development, removing waste materials that could otherwise contaminate water supplies and spread disease. Raw sewage contains human waste, food scraps, oils, chemicals, and other materials that require treatment to remove harmful bacteria, viruses, and pollutants before water can be safely returned to the environment. Modern sewage treatment involves physical, biological, and chemical processes to clean wastewater. Proper sewage management prevents waterborne diseases and environmental contamination. Combined sewage systems handle both wastewater and stormwater, while separate systems handle them independently. Inadequate sewage treatment remains a major global health and environmental challenge.',
            'pronunciation': '/ˈsuɪdʒ/',
            'etymology': 'From sew (meaning to drain) + -age suffix, related to sewer systems.',
            'memory_tip': 'Think "SEW-AGE" - waste that flows through sewn-together pipe systems.',
            'example_sentence': 'The city invested in upgrading its _____ treatment plant to meet new environmental standards.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'sewing': {
            'word': 'sewing',
            'definition': 'The craft or activity of joining fabrics or other materials together using stitches made with needle and thread, or with a sewing machine. Sewing encompasses a wide range of techniques from basic hand-stitching to complex machine operations, including activities such as garment construction, alterations, repairs, quilting, and decorative needlework. The practice requires understanding of fabric properties, pattern reading, measurement, cutting, and various stitching techniques. Sewing can be recreational, professional, or necessity-driven, ranging from hobby projects to fashion design and industrial textile production. Traditional sewing skills have cultural significance in many societies and are experiencing renewed interest as people seek creative outlets, sustainable fashion alternatives, and practical life skills. Modern sewing incorporates both traditional hand techniques and advanced machine technology.',
            'pronunciation': '/ˈsoʊɪŋ/',
            'etymology': 'From sew + -ing suffix, where sew comes from Old English seowian meaning to stitch.',
            'memory_tip': 'Think "SEW-ING" - the ongoing action of sewing fabric pieces together.',
            'example_sentence': 'Her _____ skills allowed her to create beautiful quilts and tailored clothing.',
            'part_of_speech': 'noun/verb (present participle)',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'sfax': {
            'word': 'sfax',
            'definition': 'A major port city in Tunisia, located on the Mediterranean coast and serving as the country\'s second-largest city and an important commercial and industrial center. Sfax is known for its olive oil production, fishing industry, and phosphate processing, contributing significantly to Tunisia\'s economy. The city features a well-preserved medina (old town) with traditional Arab architecture and has been an important trading center for centuries. Sfax serves as a gateway between Tunisia and Libya, with significant cross-border trade activities. The port handles various exports including olive oil, phosphates, and manufactured goods. The city\'s university and cultural institutions make it an important educational center in the region. Sfax represents a blend of traditional North African culture and modern industrial development.',
            'pronunciation': '/sfaks/',
            'etymology': 'From Arabic صفاقس (Safaqis), possibly from ancient Berber or Phoenician origins.',
            'memory_tip': 'Think "S-FAX" - a city that might send fax messages about olive oil and trade.',
            'example_sentence': 'The olive oil produced in _____ is considered among the finest in the Mediterranean region.',
            'part_of_speech': 'noun (proper)',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'sforzando': {
            'word': 'sforzando',
            'definition': 'A musical term indicating that a note or chord should be played with sudden, strong emphasis or accent, typically marked with the abbreviation "sf" or "sfz" in sheet music. Sforzando represents a dramatic dynamic effect where musicians must quickly increase volume and intensity for specific notes or passages, creating contrast and musical interest. The technique requires precise control and coordination among ensemble members to achieve the desired impact without disrupting overall musical flow. Sforzando differs from other dynamic markings by emphasizing suddenness and force rather than gradual changes. Composers use sforzando to highlight important musical moments, create tension, or add dramatic flair to compositions. The effect can be applied to individual notes, chords, or brief passages, and is common in classical, romantic, and contemporary classical music.',
            'pronunciation': '/sfɔrˈtsando/',
            'etymology': 'From Italian sforzando meaning forcing or straining, from sforzare meaning to force.',
            'memory_tip': 'Think "S-FORZ-ANDO" - using force in music to create sudden, strong emphasis.',
            'example_sentence': 'The orchestra executed the _____ passage with perfect timing and dramatic intensity.',
            'part_of_speech': 'adverb/adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'sget': {
            'word': 'sget',
            'definition': 'A term that appears to be either a typographical error, a technical abbreviation, or a word from a specialized context that is not widely recognized in standard English dictionaries. Without additional context, this may represent a data entry error, a specialized technical term, or an abbreviation specific to certain fields or software systems. It could potentially be related to computer programming, where abbreviated commands or function names are common, or it might be a term from another language that has been transliterated. The unusual letter combination and lack of clear etymology suggest this may not be a standard English word. Further context would be needed to provide an accurate definition and usage explanation.',
            'pronunciation': '/sɡɛt/',
            'etymology': 'Etymology unclear; may be an abbreviation, error, or specialized term.',
            'memory_tip': 'This appears to be an unclear or potentially erroneous entry requiring verification.',
            'example_sentence': 'The meaning of _____ requires additional context to understand its proper usage.',
            'part_of_speech': 'unclear',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shaanxinoun': {
            'word': 'shaanxinoun',
            'definition': '[COMBINED WORD ERROR] This appears to be multiple words combined: "shaanxi" (a province in China) and "noun" (a grammatical term for naming words). This combination likely resulted from a data processing error where two separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words with their individual meanings and contexts.',
            'pronunciation': '/ʃɑːnˈʃinaʊn/',
            'etymology': 'Error combination of Chinese Shaanxi (province name) + Latin nomen (noun)',
            'memory_tip': 'This is a combined word error - look for the separation between Shaanxi and noun.',
            'example_sentence': 'The data contained an error where _____ appeared instead of two separate words.',
            'part_of_speech': 'error',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shade': {
            'word': 'shade',
            'definition': 'Comparative darkness and coolness caused by shelter from direct sunlight, or a color variation that is darker than the pure hue. Shade provides relief from sun exposure and heat, making outdoor spaces more comfortable during warm weather. Natural shade comes from trees, buildings, and geographical features, while artificial shade can be created with umbrellas, awnings, and structures. In art and design, shade refers to darker variations of colors created by adding black or by the absence of light. The term can also mean a slight difference or variation, as in "shades of meaning." Metaphorically, shade can refer to a ghost or spirit, or to subtle criticism or disdain. Window shades are coverings that control light and privacy in buildings.',
            'pronunciation': '/ʃeɪd/',
            'etymology': 'From Old English sceadu meaning shadow or darkness.',
            'memory_tip': 'Think "SHADE" - shelter that helps you evade direct sunlight.',
            'example_sentence': 'The large oak tree provided welcome _____ during the hot summer afternoon.',
            'part_of_speech': 'noun/verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shadow': {
            'word': 'shadow',
            'definition': 'A dark area or shape produced by an object blocking light from reaching a surface; the dark image cast by something intercepting rays of light. Shadows change in size, shape, and position based on the light source angle, object shape, and distance relationships. In psychology, "shadow" refers to hidden or repressed aspects of personality. The term can mean to follow closely and secretly, as in shadowing someone for surveillance or observation. Shadow can also indicate a trace or slight suggestion of something, as in "a shadow of doubt." In politics, shadow ministers or shadow cabinets represent opposition party members who monitor government positions. Metaphorically, shadows represent mystery, hidden knowledge, or the darker aspects of life and human nature.',
            'pronunciation': '/ˈʃædoʊ/',
            'etymology': 'From Old English sceadwe, related to shade and meaning darkness or protection.',
            'memory_tip': 'Think "SHAD-OW" - the dark shape that shows where light is owed but blocked.',
            'example_sentence': 'Her _____ grew longer as the sun set lower in the western sky.',
            'part_of_speech': 'noun/verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shaggy': {
            'word': 'shaggy',
            'definition': 'Having long, thick, unkempt hair or fur; covered with rough, tangled, or coarse material that appears disheveled or unkempt. Shaggy typically describes textures that are intentionally or naturally rough and uneven, such as shaggy carpets with long pile, shaggy dogs with thick coats, or shaggy hairstyles with uneven layers. The term can apply to vegetation that grows wild and unmanaged, creating a rough, tangled appearance. In popular culture, "shaggy" often refers to the deliberately messy, casual hair style or the animated character Shaggy from Scooby-Doo. The word conveys a sense of natural disorder, casual styling, or deliberately unkempt appearance that may be either fashionable or simply ungroomed. Shaggy textures often feel soft despite their rough appearance.',
            'pronunciation': '/ˈʃæɡi/',
            'etymology': 'From shag + -y suffix, where shag refers to rough, tangled hair or material.',
            'memory_tip': 'Think "SHAG-GY" - hair that\'s shagged up and messy like a shag carpet.',
            'example_sentence': 'The _____ dog shook water from its thick, matted coat after swimming.',
            'part_of_speech': 'adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shah': {
            'word': 'shah',
            'definition': 'A Persian title for a king or emperor, historically used by rulers of Iran and other Persian-influenced regions. The shah held absolute power over the empire and was considered the supreme authority in political, military, and often religious matters. Famous shahs include Cyrus the Great of the ancient Persian Empire and Mohammad Reza Pahlavi, the last shah of Iran who was overthrown in 1979. The title carries connotations of imperial grandeur, absolute monarchy, and Persian cultural heritage. In chess, "shah" is the origin of the term "check," derived from the Persian phrase meaning "the king is attacked." The position represented divine appointment and carried enormous responsibility for the welfare of the empire. The last Iranian shah\'s regime ended with the Islamic Revolution, eliminating the position from modern Iran.',
            'pronunciation': '/ʃɑː/',
            'etymology': 'From Persian šāh meaning king or emperor.',
            'memory_tip': 'Think "SHAH" - a Persian king who says "ah" as he rules his empire.',
            'example_sentence': 'The last _____ of Iran left the country during the 1979 revolution.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shakar': {
            'word': 'shakar',
            'definition': 'A term for sugar in various South Asian languages including Hindi, Urdu, and Persian, referring to crystallized sugar or sweet substances used in cooking and confections. Shakar represents an important ingredient in traditional South Asian cuisine, used in both savory and sweet dishes, as well as in various traditional sweets and desserts. The term appears in many regional recipes and cultural contexts where sugar plays important roles in food preparation, religious offerings, and hospitality customs. Different types of shakar may include refined sugar, jaggery, or other sweetening agents depending on regional preferences and availability. In historical contexts, shakar was a valuable trade commodity that influenced economic and cultural exchanges between regions. The word reflects the linguistic and cultural connections between Persian, Arabic, and South Asian civilizations.',
            'pronunciation': '/ˈʃækər/',
            'etymology': 'From Persian shakar meaning sugar, related to Sanskrit शर्करा (sharkara).',
            'memory_tip': 'Think "SHAK-AR" - shaking sugar crystals into food for sweetness.',
            'example_sentence': 'The recipe called for _____ to sweeten the traditional milk-based dessert.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shake': {
            'word': 'shake',
            'definition': 'To move quickly back and forth or up and down with short, rapid movements; to tremble or vibrate due to emotion, cold, fear, or external forces. Shaking can be voluntary (shaking hands in greeting) or involuntary (shaking from cold or nervousness). The action can apply to objects being moved by external forces or people experiencing physical or emotional responses. Shake can also mean to disturb, upset, or unsettle someone emotionally, as in being "shaken" by news. In various contexts, shake refers to mixing beverages, removing items by vigorous movement, or expressing disapproval through head movements. The word can describe natural phenomena like earthquakes or mechanical vibrations. Cultural uses include handshakes for greetings and agreements, milkshakes as beverages, and "shake it off" as encouragement to overcome setbacks.',
            'pronunciation': '/ʃeɪk/',
            'etymology': 'From Old English sceacan meaning to move quickly back and forth.',
            'memory_tip': 'Think "SHAKE" - making something quake with quick back-and-forth movement.',
            'example_sentence': 'The earthquake caused the entire building to _____ violently for several seconds.',
            'part_of_speech': 'verb/noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shall': {
            'word': 'shall',
            'definition': 'A modal auxiliary verb expressing future tense, intention, obligation, or determination, traditionally used with first person pronouns (I, we) to indicate simple future action. In formal or legal contexts, "shall" often indicates obligation or requirement rather than mere futurity, as in contracts or legislation where "shall" means "must" or "is required to." The word can express strong determination or promise, as in "We shall overcome." British English tends to use "shall" more frequently than American English, which often prefers "will" for future tense. In questions, "shall" can propose action or seek agreement, as in "Shall we go?" The usage varies by region, formality level, and context, with "shall" maintaining stronger presence in legal, religious, and formal discourse.',
            'pronunciation': '/ʃæl/',
            'etymology': 'From Old English sceal meaning owe, ought to, or must.',
            'memory_tip': 'Think "SHALL" - a formal way to say what one will do or must do.',
            'example_sentence': 'The contract states that the contractor _____ complete the work by December 31st.',
            'part_of_speech': 'modal verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shallow': {
            'word': 'shallow',
            'definition': 'Having little depth from top to bottom; not extending far below a surface, whether in water, containers, or figurative contexts. Shallow water poses different challenges for navigation and swimming than deep water. The term can describe physical characteristics (shallow dishes, shallow graves) or intellectual and emotional qualities (shallow thinking, shallow relationships). When applied to people or ideas, shallow suggests lack of depth, substance, or serious consideration. Shallow breathing involves taking air only into the upper lungs rather than breathing deeply. In photography, shallow depth of field keeps only a narrow range in focus. The word often carries negative connotations when describing superficial attitudes, understanding, or relationships that lack meaningful depth or genuine engagement.',
            'pronunciation': '/ˈʃæloʊ/',
            'etymology': 'From Old English sceald meaning shallow, related to shoal.',
            'memory_tip': 'Think "SHALL-LOW" - shall we go low into the shallow water where it\'s not deep?',
            'example_sentence': 'The boat ran aground in the _____ water near the shore.',
            'part_of_speech': 'adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shaman': {
            'word': 'shaman',
            'definition': 'A religious or spiritual leader in certain cultures who is believed to have the ability to communicate with spirits, heal illnesses, and guide souls between the physical and spiritual worlds. Shamans traditionally serve as intermediaries between human communities and supernatural forces, using various techniques including ritualistic practices, trance states, herbal medicine, and ceremonial objects. The role encompasses healing, divination, spiritual guidance, and maintaining cultural traditions. Shamanic practices exist in many indigenous cultures worldwide, including Siberian, Native American, African, and South American traditions. Modern interest in shamanism has led to contemporary spiritual practices that draw from traditional techniques. The shaman\'s role often requires extensive training, initiation rituals, and deep knowledge of cultural beliefs, medicinal plants, and spiritual practices. Their work addresses both physical and spiritual aspects of community well-being.',
            'pronunciation': '/ˈʃɑːmən/',
            'etymology': 'From Russian шаман (shaman), from Tungusic šamān meaning religious practitioner.',
            'memory_tip': 'Think "SHAM-AN" - not a sham, but a real spiritual person who bridges worlds.',
            'example_sentence': 'The _____ performed a healing ceremony using traditional herbs and chanting.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shamanverb': {
            'word': 'shamanverb',
            'definition': '[COMBINED WORD ERROR] This appears to be two words combined: "shaman" (a spiritual leader who communicates with spirits) and "verb" (a grammatical term for action words). This combination likely resulted from a data processing error where two separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words with their individual meanings and contexts.',
            'pronunciation': '/ˈʃɑːmənvɜrb/',
            'etymology': 'Error combination of Tungusic šamān (shaman) + Latin verbum (verb)',
            'memory_tip': 'This is a combined word error - look for the separation between shaman and verb.',
            'example_sentence': 'The data contained an error where _____ appeared instead of two separate words.',
            'part_of_speech': 'error',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shambles': {
            'word': 'shambles',
            'definition': 'A state of complete disorder, confusion, or disorganization; a situation that is chaotic, messy, or falling apart. Originally, shambles referred to a slaughterhouse or meat market, but the modern meaning evolved from the bloody, disorderly appearance of such places. The word is often used to describe situations that have gone wrong, plans that have failed, or environments that are extremely disorganized. A room, event, organization, or process can be described as "in shambles" when it lacks order or proper function. The term emphasizes not just messiness but a degree of chaos that suggests things have deteriorated significantly from their intended state. Political situations, business operations, or personal circumstances might be described as shambles when they become unmanageable or dysfunctional.',
            'pronunciation': '/ˈʃæmbəlz/',
            'etymology': 'From Middle English shamble meaning bench or stall, originally referring to meat markets.',
            'memory_tip': 'Think "SHAM-BLES" - a situation so bad it\'s like a shameful scramble or mess.',
            'example_sentence': 'After the storm, the outdoor wedding venue was in complete _____.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shamrock': {
            'word': 'shamrock',
            'definition': 'A three-leafed plant, typically a clover, that serves as the national symbol of Ireland and is associated with St. Patrick and Irish culture. The shamrock traditionally represents the Holy Trinity in Christian symbolism, with each leaf representing the Father, Son, and Holy Spirit. According to legend, St. Patrick used the shamrock to explain the concept of the Trinity to the Irish people during his missionary work. The plant is commonly featured in St. Patrick\'s Day celebrations and Irish imagery worldwide. While several plant species are called shamrock, including white clover and wood sorrel, the exact species historically used by St. Patrick remains debated. The shamrock appears on Irish coins, emblems, and cultural artifacts. Finding a four-leaf clover among shamrocks is considered especially lucky in folklore.',
            'pronunciation': '/ˈʃæmrɑk/',
            'etymology': 'From Irish seamróg, diminutive of seamar meaning clover.',
            'memory_tip': 'Think "SHAM-ROCK" - not a sham rock, but a real three-leafed symbol of Ireland.',
            'example_sentence': 'She wore a _____ pin on her lapel to celebrate St. Patrick\'s Day.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shanter': {
            'word': 'shanter',
            'definition': 'A soft, round, brimless Scottish cap, typically made of wool and often featuring a pom-pom or tassel on top, also known as a tam o\'shanter or tam. The cap is traditionally associated with Scottish Highland dress and culture, though it has been adopted more broadly as casual headwear. Shanters are often worn tilted to one side and may feature clan tartans or other decorative patterns. The design allows for practical warmth while maintaining cultural identity and style. Military versions have been used by various Scottish regiments. The cap gained broader recognition through literature, particularly Robert Burns\' poem "Tam o\' Shanter," and through popular culture representations of Scottish heritage. Modern shanters serve both practical and ceremonial purposes in Scottish communities and among those celebrating Scottish culture.',
            'pronunciation': '/ˈʃæntər/',
            'etymology': 'Short for tam o\'shanter, named after the character in Robert Burns\' poem.',
            'memory_tip': 'Think "SHANT-ER" - a Scottish cap that you shan\'t forget when wearing Highland dress.',
            'example_sentence': 'The Scottish dancer adjusted her _____ before performing the traditional Highland fling.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shape': {
            'word': 'shape',
            'definition': 'The external form, contour, or appearance of something as defined by its outline or configuration; the geometric or physical characteristics that distinguish one object from another. Shape encompasses two-dimensional forms (circles, squares, triangles) and three-dimensional forms (spheres, cubes, pyramids). The term can also refer to physical condition or health status, as in being "in good shape." Shape can mean to mold, form, or influence something, such as shaping clay or shaping public opinion. In abstract contexts, shape refers to the nature or character of situations, ideas, or developments. Mathematical shapes have specific properties and relationships. The word emphasizes the defining characteristics that give objects their distinctive appearance and help us recognize and categorize them.',
            'pronunciation': '/ʃeɪp/',
            'etymology': 'From Old English sciepon meaning to create or form.',
            'memory_tip': 'Think "SHAPE" - the way something is made or formed that gives it its distinctive appearance.',
            'example_sentence': 'The artist molded the clay into the _____ of a graceful swan.',
            'part_of_speech': 'noun/verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shaped': {
            'word': 'shaped',
            'definition': 'Past tense of shape, meaning to have given form, configuration, or structure to something; molded or formed into a particular appearance or character. The word describes the completed action of creating, influencing, or determining the form of objects, ideas, or situations. Things can be physically shaped through manufacturing, crafting, or natural processes, or metaphorically shaped through experiences, education, or influences. Well-shaped objects have pleasing or functional forms, while misshapen items have irregular or undesirable configurations. Personal character and worldview can be shaped by experiences, relationships, and learning. The term emphasizes the transformative process that creates final forms or characteristics from raw materials or initial conditions.',
            'pronunciation': '/ʃeɪpt/',
            'etymology': 'From shape + -ed past tense suffix.',
            'memory_tip': 'Think "SHAP-ED" - having been shaped into a particular form or configuration.',
            'example_sentence': 'Her worldview was _____ by years of travel and exposure to different cultures.',
            'part_of_speech': 'verb (past tense)/adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'shar': {
            'word': 'shar',
            'definition': 'A term that may refer to the Shar Pei, a distinctive Chinese dog breed known for its wrinkled skin, blue-black tongue, and loyal temperament. The Chinese Shar Pei was originally bred for hunting, herding, and guarding, and is characterized by its unique loose, wrinkled skin that served as protection in dog fights. The breed nearly became extinct in the 20th century but was revived through dedicated breeding programs. Shar Peis are known for their independence, intelligence, and strong protective instincts toward their families. They require early socialization and consistent training due to their naturally reserved and sometimes stubborn nature. The breed\'s distinctive appearance includes a broad skull, small triangular ears, and a tail that curls over the back. Modern Shar Peis are primarily kept as companion dogs and show animals.',
            'pronunciation': '/ʃɑr/',
            'etymology': 'Shortened from Shar Pei, from Chinese 沙皮 meaning sand skin, referring to the coat texture.',
            'memory_tip': 'Think "SHAR" - a dog breed that shares its distinctive wrinkled appearance.',
            'example_sentence': 'The _____ Pei puppy\'s wrinkled skin made it look like it was wearing an oversized coat.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'share': {
            'word': 'share',
            'definition': 'To give a portion of something to others or to use, experience, or possess something jointly with others; to distribute or divide something among multiple people. Sharing involves willingness to allow others access to resources, experiences, information, or possessions that one could keep exclusively. The concept is fundamental to cooperation, community building, and social relationships. Financial shares represent portions of ownership in companies or investments. Information sharing facilitates communication and learning. Resource sharing promotes efficiency and sustainability. The word can also mean to tell others about experiences, thoughts, or feelings. Sharing differs from giving in that it typically implies ongoing or mutual access rather than permanent transfer. The practice reflects values of generosity, cooperation, and community spirit.',
            'pronunciation': '/ʃɛr/',
            'etymology': 'From Old English scieran meaning to cut or divide.',
            'memory_tip': 'Think "SHARE" - to give others their fair share of something you have.',
            'example_sentence': 'The siblings decided to _____ the inheritance equally among all family members.',
            'part_of_speech': 'verb/noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        }
    }
    
    combined_errors = []
    
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        words = [row['word'] for row in reader]
    
    processed_words = []
    for i, word in enumerate(words, 1):
        print(f"Processing word {i}: {word}")
        
        if word in word_data:
            data = word_data[word]
            phonetic_score, frequency_score, morphological_score, etymology_score, total_score = calculator.calculate_difficulty_score(
                data['word'], data['pronunciation'], data['etymology']
            )
            
            data.update({
                'phonetic_score': phonetic_score,
                'frequency_score': frequency_score,
                'morphological_score': morphological_score,
                'etymology_score': etymology_score,
                'total_score': total_score
            })
            
            processed_words.append(data)
            
            if 'COMBINED WORD ERROR' in data['definition']:
                combined_errors.append(word)
    
    csv_columns = ['word', 'definition', 'pronunciation', 'etymology', 'memory_tip', 'example_sentence', 
                   'part_of_speech', 'source', 'source_difficulty', 'claude_difficulty',
                   'phonetic_score', 'frequency_score', 'morphological_score', 'etymology_score', 'total_score']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(processed_words)
    
    print(f"\nBatch 158 processing complete!")
    print(f"Successfully processed {len(processed_words)}/{len(words)} words")
    print(f"Output saved to: {output_file}")
    
    if combined_errors:
        print(f"\nCombined word errors detected: {len(combined_errors)}")
        for error in combined_errors:
            print(f"  - {error}")

if __name__ == "__main__":
    process_batch()