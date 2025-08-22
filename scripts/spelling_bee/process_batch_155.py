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
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_155_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_155_processed.csv'
    
    calculator = DifficultyCalculator()
    
    word_data = {
        'scandinavia': {
            'word': 'scandinavia',
            'definition': 'A cultural and historical region in northern Europe comprising Denmark, Norway, and Sweden, characterized by shared linguistic, cultural, and historical heritage. These countries share similar languages (North Germanic), traditional customs, and political systems, often cooperating through the Nordic Council. The region is known for its distinctive geography including fjords, forests, and a long coastline along the North Sea, Baltic Sea, and Arctic Ocean. Historically, the Scandinavian peoples were seafaring Vikings who explored and settled throughout Europe and beyond. Modern Scandinavia is recognized for high living standards, progressive social policies, and strong democratic institutions. The term sometimes includes Finland and Iceland in broader Nordic discussions, though linguistically and culturally these countries have different origins.',
            'pronunciation': '/ˌskændɪˈneɪviə/',
            'etymology': 'From Latin Scandinavia, possibly from Germanic skadin meaning harmful + -avia meaning island, or from Scania, the southern region of Sweden.',
            'memory_tip': 'Think "SCAN-DINAVIA" - you can scan the northern European countries of Denmark, Norway, and Sweden.',
            'example_sentence': 'The study abroad program offered courses in _____ to explore the rich cultural heritage of Denmark, Norway, and Sweden.',
            'part_of_speech': 'noun (proper)',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scandium': {
            'word': 'scandium',
            'definition': 'A silvery-white metallic chemical element with the symbol Sc and atomic number 21, belonging to the group of rare earth elements and transition metals. Scandium is one of the lightest metals and has properties that make it valuable in aerospace applications, particularly in aluminum alloys where small amounts significantly improve strength and heat resistance. Despite being more abundant than lead in the Earth\'s crust, scandium is considered rare because it rarely concentrates in economically extractable quantities. The element was predicted by Dmitri Mendeleev before its discovery in 1879, and it filled a gap in his periodic table. Scandium compounds have specialized uses in high-intensity lighting and in some electronic applications, though its high cost limits widespread commercial use.',
            'pronunciation': '/ˈskændiəm/',
            'etymology': 'Named after Scandinavia, where it was first discovered in minerals from Scandinavian ores.',
            'memory_tip': 'Remember "SCAND-ium" - the element named after Scandinavia where it was discovered.',
            'example_sentence': 'The aerospace engineer explained how adding _____ to aluminum creates stronger, lighter alloys for aircraft construction.',
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
        'scanner': {
            'word': 'scanner',
            'definition': 'A device that captures and converts physical documents, images, or objects into digital format by using optical sensors to detect light patterns and translate them into electronic data. Computer scanners typically use charge-coupled devices (CCDs) or contact image sensors to create digital copies of photographs, documents, or artwork. The technology allows for digitization, storage, and electronic manipulation of physical materials. Scanners come in various types including flatbed scanners for documents and photos, handheld scanners for portability, and specialized scanners for film negatives or three-dimensional objects. In broader contexts, scanner can refer to any device that systematically examines or searches through data, such as security scanners, medical imaging scanners, or radio scanners that monitor communication frequencies.',
            'pronunciation': '/ˈskænər/',
            'etymology': 'From scan + -er suffix, meaning a device that performs scanning action.',
            'memory_tip': 'Think "SCAN-ER" - a device that scans documents to convert them to digital format.',
            'example_sentence': 'The office _____ converted the old paper files into digital documents for easier storage.',
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
        'scanty': {
            'word': 'scanty',
            'definition': 'Insufficient in quantity, size, or extent; barely adequate or meager in amount. Something described as scanty falls short of what is needed, expected, or desired, whether referring to physical quantities, coverage, or provision. In clothing contexts, scanty describes garments that provide minimal coverage or are revealing. The term can apply to resources, supplies, information, or any measurable quantity that is notably lacking or sparse. Scanty often implies a problematic insufficiency rather than a deliberate minimalism, suggesting that more would be beneficial or necessary. The word carries connotations of inadequacy and can describe everything from scanty rainfall during a drought to scanty evidence in a legal case.',
            'pronunciation': '/ˈskænti/',
            'etymology': 'From scant + -y suffix, where scant comes from Old Norse skamt meaning short or brief.',
            'memory_tip': 'Think "SCANT-Y" - so scant (little) that it\'s insufficient or barely adequate.',
            'example_sentence': 'The desert region received only _____ rainfall this year, causing concern about water shortages.',
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
        'scarab': {
            'word': 'scarab',
            'definition': 'A beetle belonging to the family Scarabaeidae, particularly the sacred scarab beetle (Scarabaeus sacer) revered in ancient Egyptian culture as a symbol of rebirth, transformation, and the sun god Ra. These beetles are known for their behavior of rolling balls of dung across the ground, which ancient Egyptians associated with the sun\'s movement across the sky. Scarab amulets and jewelry were common in ancient Egypt, often placed with mummies to ensure safe passage to the afterlife. The broader scarab family includes many species worldwide, including dung beetles, rhinoceros beetles, and June beetles. In archaeological contexts, scarab artifacts provide valuable insights into ancient Egyptian religious beliefs, artistic styles, and daily life practices.',
            'pronunciation': '/ˈskærəb/',
            'etymology': 'From Latin scarabaeus, from Greek σκάραβος (skarabos) meaning beetle.',
            'memory_tip': 'Think "SCAR-AB" - the sacred beetle with markings like scars that ancient Egyptians worshipped.',
            'example_sentence': 'The archaeologist discovered a gold _____ amulet in the ancient Egyptian tomb.',
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
        'scarcely': {
            'word': 'scarcely',
            'definition': 'Hardly; barely; only just; almost not at all. Used to indicate that something exists, happens, or is true to only a very small degree or extent. Scarcely emphasizes the minimal nature of an action, condition, or amount, often suggesting insufficiency or near absence. The word frequently appears in constructions like "scarcely had I arrived when..." to indicate events happening in quick succession. In formal or literary contexts, scarcely can express disbelief or skepticism about a statement. The adverb implies that something is so limited or minimal that it might as well not exist, creating emphasis through understatement.',
            'pronunciation': '/ˈskɛrsli/',
            'etymology': 'From scarce + -ly suffix, where scarce comes from Old French escars meaning restricted or limited.',
            'memory_tip': 'Think "SCARCE-LY" - so scarce that it barely exists or happens.',
            'example_sentence': 'She had _____ finished her presentation when the fire alarm interrupted the meeting.',
            'part_of_speech': 'adverb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scared': {
            'word': 'scared',
            'definition': 'Feeling fear, anxiety, or apprehension about something perceived as dangerous, threatening, or uncertain. The emotional state of being scared involves physiological responses such as increased heart rate, heightened alertness, and sometimes flight-or-fight reactions. Fear can be rational, based on genuine threats or dangers, or irrational, stemming from phobias or anxiety disorders. Being scared serves evolutionary purposes by motivating protective behaviors and heightened awareness of potential threats. The intensity of feeling scared can range from mild uneasiness to overwhelming terror, depending on the perceived severity of the threat and individual psychological factors. Common sources of fear include physical danger, social situations, unknown outcomes, or traumatic memories.',
            'pronunciation': '/skɛrd/',
            'etymology': 'Past tense of scare, from Middle English skerre, possibly from Old Norse skirra meaning to frighten.',
            'memory_tip': 'Think "SCARE-D" - having been frightened or feeling fear about something.',
            'example_sentence': 'The child was _____ of the dark and always slept with a nightlight on.',
            'part_of_speech': 'adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scarf': {
            'word': 'scarf',
            'definition': 'A piece of fabric worn around the neck, head, or shoulders for warmth, protection, or fashion purposes. Scarves come in various materials including wool, silk, cotton, and synthetic fibers, and can serve different functions depending on climate and style preferences. In cold weather, thick scarves provide insulation and protection from wind and cold air. Fashion scarves add color, texture, and style to outfits while sometimes serving practical purposes. Religious or cultural scarves may have special significance, such as hijabs, prayer shawls, or ceremonial wraps. The verb form means to wrap oneself with a scarf or, informally, to consume food quickly and eagerly. Scarves have been worn throughout history across many cultures as both functional and decorative accessories.',
            'pronunciation': '/skɑːrf/',
            'etymology': 'From Old French escharpe meaning pilgrim\'s pouch, later applied to cloth worn over the shoulder.',
            'memory_tip': 'Think "S-CARF" - a piece of cloth that you wrap around yourself, like carving a protective layer.',
            'example_sentence': 'She wrapped her wool _____ tightly around her neck before stepping out into the cold wind.',
            'part_of_speech': 'noun/verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scarlatina': {
            'word': 'scarlatina',
            'definition': 'A bacterial infection caused by group A Streptococcus bacteria, also known as scarlet fever, characterized by a distinctive red rash, high fever, and sore throat. The disease primarily affects children and is highly contagious, spreading through respiratory droplets from coughing or sneezing. Symptoms include a bright red rash that feels like sandpaper, strawberry tongue (red and bumpy), fever, headache, and swollen lymph nodes. Before the advent of antibiotics, scarlatina was a serious childhood disease with potentially fatal complications including rheumatic fever and kidney problems. Modern treatment with antibiotics like penicillin is highly effective when started early. The disease was more common and severe in past centuries, inspiring fear in communities and influencing public health measures for infectious disease control.',
            'pronunciation': '/ˌskɑːrlɑːˈtiːnə/',
            'etymology': 'From New Latin scarlatina, from Italian scarlatto meaning scarlet, referring to the characteristic red rash.',
            'memory_tip': 'Think "SCARLET-INA" - a disease that causes a scarlet (bright red) rash on the skin.',
            'example_sentence': 'The pediatrician diagnosed _____ based on the child\'s distinctive red rash and high fever.',
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
        'scars': {
            'word': 'scars',
            'definition': 'Permanent marks or areas of damaged tissue that remain after wounds, injuries, or surgical incisions have healed. Scars form as part of the natural healing process when collagen fibers repair damaged skin, often creating tissue with different texture, color, or thickness than surrounding healthy skin. The appearance of scars varies depending on factors such as the depth and size of the original wound, individual healing capacity, age, and skin type. Some scars fade over time and become barely visible, while others remain prominent. Beyond physical marks, "scars" can metaphorically refer to lasting emotional or psychological effects from traumatic experiences. Medical treatments for scars include topical treatments, laser therapy, surgical revision, and other interventions to improve appearance.',
            'pronunciation': '/skɑːrz/',
            'etymology': 'Plural of scar, from Old French escare, from Greek εσχάρα (eskhara) meaning fireplace or scab.',
            'memory_tip': 'Think "S-CARS" - permanent marks left behind like cars leave tire tracks.',
            'example_sentence': 'The surgeon explained that the _____ from the operation would fade significantly over the next year.',
            'part_of_speech': 'noun (plural)',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scattering': {
            'word': 'scattering',
            'definition': 'The process of spreading, dispersing, or distributing things widely over an area or in different directions. In physics, scattering refers to the deflection of waves, particles, or radiation when they encounter obstacles, irregularities, or interactions with matter. Examples include light scattering by atmospheric particles (causing blue skies), sound scattering by objects, or particle scattering in nuclear physics experiments. In everyday contexts, scattering describes the random distribution of objects across a space, such as seeds scattered by wind or people scattering after an event ends. The process can be intentional, like scattering ashes in a memorial service, or unintentional, like papers scattering in the wind. Mathematically, scattering patterns help scientists understand the properties of materials and fundamental particles.',
            'pronunciation': '/ˈskætərɪŋ/',
            'etymology': 'From scatter + -ing suffix, where scatter comes from Middle English scateren meaning to disperse.',
            'memory_tip': 'Think "SCATTER-ING" - the ongoing action of things spreading out or dispersing widely.',
            'example_sentence': 'The _____ of light by water droplets in the air creates the beautiful colors of a rainbow.',
            'part_of_speech': 'noun/verb (present participle)',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scenographer': {
            'word': 'scenographer',
            'definition': 'A professional who designs and creates the visual environment for theatrical productions, films, television shows, or other performance media, encompassing set design, lighting design, and sometimes costume design. Scenographers combine artistic vision with technical expertise to create spaces that support storytelling, establish mood and atmosphere, and enhance the audience\'s experience. Their work involves understanding scripts, collaborating with directors and other creative team members, and translating conceptual ideas into practical, buildable designs. The role requires knowledge of architecture, art history, color theory, materials, construction techniques, and theatrical technology. Scenographers must balance aesthetic considerations with practical constraints such as budget limitations, safety requirements, and the need for sets to function during live performances.',
            'pronunciation': '/siːˈnɒɡrəfər/',
            'etymology': 'From Greek σκηνή (skene) meaning stage + γράφω (grapho) meaning to write or draw + -er suffix.',
            'memory_tip': 'Think "SCENE-GRAPHER" - someone who graphs or designs scenes for theatrical productions.',
            'example_sentence': 'The _____ created an elaborate medieval castle set that transformed throughout the play.',
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
        'scentpuzzles': {
            'word': 'scentpuzzles',
            'definition': '[COMBINED WORD ERROR] This appears to be two words combined: "scent" (a distinctive smell or fragrance) and "puzzles" (problems or games requiring solution). This combination likely resulted from a data processing error where two separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words with their individual meanings and contexts.',
            'pronunciation': '/sɛntˈpʌzəlz/',
            'etymology': 'Error combination of Latin sentire (scent) + Middle English posel (puzzles)',
            'memory_tip': 'This is a combined word error - look for the separation between scent and puzzles.',
            'example_sentence': 'The data contained an error where _____ appeared instead of two separate words.',
            'part_of_speech': 'error',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scentscholarship': {
            'word': 'scentscholarship',
            'definition': '[COMBINED WORD ERROR] This appears to be two words combined: "scent" (a distinctive smell or fragrance) and "scholarship" (academic study or financial aid for education). This combination likely resulted from a data processing error where two separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words with their individual meanings and contexts.',
            'pronunciation': '/sɛntˈskɒlərʃɪp/',
            'etymology': 'Error combination of Latin sentire (scent) + scholar + -ship',
            'memory_tip': 'This is a combined word error - look for the separation between scent and scholarship.',
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
        'scentverb': {
            'word': 'scentverb',
            'definition': '[COMBINED WORD ERROR] This appears to be two words combined: "scent" (a distinctive smell or fragrance) and "verb" (a word denoting action or state). This combination likely resulted from a data processing error where two separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words with their individual meanings and contexts.',
            'pronunciation': '/sɛntˈvɜːrb/',
            'etymology': 'Error combination of Latin sentire (scent) + Latin verbum (verb)',
            'memory_tip': 'This is a combined word error - look for the separation between scent and verb.',
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
        'scepter': {
            'word': 'scepter',
            'definition': 'A ceremonial staff or rod carried by rulers as a symbol of authority, sovereignty, and power, typically ornately decorated with precious metals, gems, or religious symbols. Scepters have been used throughout history by monarchs, emperors, and other high-ranking officials during coronations, court ceremonies, and state functions. The design and ornamentation of scepters often reflect the cultural, religious, and artistic traditions of their respective civilizations. Famous examples include the royal scepters held in the British Crown Jewels and various ancient Egyptian and Mesopotamian ceremonial staffs. Beyond their symbolic function, scepters represent the divine right to rule and serve as tangible manifestations of royal power and legitimacy. The word can also be used metaphorically to represent any symbol of authority or control.',
            'pronunciation': '/ˈsɛptər/',
            'etymology': 'From Latin sceptrum, from Greek σκῆπτρον (skeptron) meaning staff or walking stick.',
            'memory_tip': 'Think "SEPT-ER" - a royal staff that separates the ruler from ordinary people.',
            'example_sentence': 'The queen held her jeweled _____ during the coronation ceremony as a symbol of royal authority.',
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
        'sceptical': {
            'word': 'sceptical',
            'definition': 'The British spelling of "skeptical," meaning having an attitude of doubt or questioning toward knowledge, facts, or opinions that are accepted by others. A sceptical person tends to question claims, seek evidence before believing, and maintain a critical attitude toward information presented without proof. This intellectual position involves carefully examining ideas rather than accepting them at face value. Sceptical thinking is fundamental to scientific inquiry, encouraging hypothesis testing and evidence-based conclusions. The spelling with "sc" rather than "sk" is standard in British English and other Commonwealth varieties, while American English typically uses "skeptical." Healthy scepticism helps distinguish between reliable and unreliable information, making it a valuable cognitive tool.',
            'pronunciation': '/ˈskɛptɪkəl/',
            'etymology': 'From Greek σκεπτικός (skeptikos) meaning inquiring or thoughtful, from σκέπτομαι (skeptomai) meaning to look or examine.',
            'memory_tip': 'British spelling with "SC" - remember "SC" for "Skeptical in Commonwealth" countries.',
            'example_sentence': 'The scientist remained _____ about the new theory until more research could verify the claims.',
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
        'sceptre': {
            'word': 'sceptre',
            'definition': 'The British spelling of "scepter," referring to a ceremonial staff or rod carried by rulers as a symbol of authority, sovereignty, and power. Like its American counterpart, a sceptre is typically ornately decorated with precious metals, gems, or religious symbols and used during coronations, court ceremonies, and state functions. The British spelling reflects the tendency in British English to retain certain French-influenced spellings. Sceptres have been important symbols of royal power throughout history, representing the divine right to rule and serving as tangible manifestations of authority. The British Crown Jewels include several historic sceptres that continue to be used in modern ceremonial functions.',
            'pronunciation': '/ˈsɛptər/',
            'etymology': 'From Old French sceptre, from Latin sceptrum, from Greek σκῆπτρον (skeptron) meaning staff.',
            'memory_tip': 'British spelling ends in "-tre" like "centre" and "theatre" - think "Royal English."',
            'example_sentence': 'The British monarch\'s golden _____ is displayed alongside the crown jewels in the Tower of London.',
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
        'schedar': {
            'word': 'schedar',
            'definition': 'The brightest star in the constellation Cassiopeia, also known as Alpha Cassiopeiae, located approximately 228 light-years from Earth. Schedar is an orange giant star with a magnitude that varies slightly, making it a variable star. The name comes from Arabic and means "breast," referring to its position in the constellation which represents the mythological queen Cassiopeia. This star is part of the distinctive W-shaped asterism that makes Cassiopeia easily recognizable in the northern sky. Schedar serves as an important navigation star and is visible year-round from northern latitudes. In astronomical observations, it helps locate other celestial objects and serves as a reference point for star charts and celestial navigation.',
            'pronunciation': '/ˈʃɛdɑːr/',
            'etymology': 'From Arabic صدر (sadr) meaning breast or chest, referring to its position in the constellation Cassiopeia.',
            'memory_tip': 'Think "SHED-AR" - the bright star that sheds light like a beacon in the Cassiopeia constellation.',
            'example_sentence': 'Amateur astronomers often use _____ as a starting point to locate other stars in the constellation Cassiopeia.',
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
        'schedule': {
            'word': 'schedule',
            'definition': 'A planned sequence of activities, events, or tasks arranged according to specific times, dates, or order of priority. Schedules serve organizational purposes in personal, academic, and professional contexts, helping coordinate activities and manage time efficiently. They can range from daily routines and weekly calendars to complex project timelines and transportation timetables. Effective scheduling involves balancing multiple commitments, allowing appropriate time for each activity, and building in flexibility for unexpected changes. Modern scheduling often involves digital tools and software that can automatically coordinate multiple participants and send reminders. The verb form means to arrange or plan activities for specific times, making scheduling a fundamental skill for productivity and time management.',
            'pronunciation': '/ˈʃɛdjuːl/ (British) or /ˈskɛdʒuːl/ (American)',
            'etymology': 'From Latin schedula meaning small piece of paper, diminutive of scheda meaning strip of papyrus.',
            'memory_tip': 'Think "SHED-ULE" - like shedding tasks into organized time slots, or "SKED-ULE" in American pronunciation.',
            'example_sentence': 'The conference _____ included presentations from speakers in three different time zones.',
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
        'schefflera': {
            'word': 'schefflera',
            'definition': 'A genus of tropical and subtropical plants in the family Araliaceae, commonly known as umbrella trees or octopus trees due to their distinctive leaf arrangement. Schefflera plants feature palmate leaves arranged in clusters that radiate from central points like umbrella spokes. Popular as houseplants, they are valued for their attractive foliage, tolerance of indoor conditions, and relatively easy care requirements. The most common indoor variety is Schefflera actinophylla, which can grow quite large if not pruned. These plants prefer bright, indirect light and moderate watering, making them suitable for office and home environments. In their native tropical habitats, scheffleras can grow as large trees or shrubs, producing small flowers and fruit. The genus was named after German botanist Jacob Christian Scheffler.',
            'pronunciation': '/ʃɛˈflɛrə/',
            'etymology': 'Named after German botanist Jacob Christian Scheffler (1698-1742), with the Latinized suffix -a.',
            'memory_tip': 'Think "SHEF-LERA" - like a chef named Lera who arranges leaves like ingredients in umbrella patterns.',
            'example_sentence': 'The office _____ had grown so tall that it needed pruning to prevent it from touching the ceiling.',
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
        'scheme': {
            'word': 'scheme',
            'definition': 'A systematic plan, design, or program of action designed to achieve a particular goal or purpose. Schemes can be legitimate organizational strategies, such as educational curricula, business plans, or architectural designs. However, the word often carries negative connotations when referring to deceptive or manipulative plots intended to gain advantage through dishonest means. In graphic design and art, a color scheme refers to the selection and arrangement of colors used in a composition. Mathematical and scientific schemes describe systematic approaches to solving problems or organizing information. The complexity of schemes can range from simple personal plans to elaborate multi-stage operations involving multiple participants and resources.',
            'pronunciation': '/skiːm/',
            'etymology': 'From Latin schema, from Greek σχῆμα (schema) meaning form, figure, or plan.',
            'memory_tip': 'Think "SCHEME" rhymes with "dream" - both involve planning something in your mind.',
            'example_sentence': 'The urban planning _____ proposed converting the old industrial area into a mixed-use residential district.',
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
        'scherzo': {
            'word': 'scherzo',
            'definition': 'A lively, playful musical composition or movement, typically in triple meter with a fast tempo and humorous or whimsical character. Originally developed during the Classical period as a replacement for the minuet in symphonies and chamber music, the scherzo became a standard movement in four-movement works. The term literally means "joke" in Italian, reflecting its light-hearted and sometimes surprising musical character. Scherzos often feature unexpected rhythmic accents, sudden dynamic changes, and playful melodic themes that create a sense of musical humor. Famous examples include movements from Beethoven\'s symphonies and Chopin\'s standalone piano scherzos. The form typically includes a contrasting middle section called a trio, after which the main scherzo theme returns.',
            'pronunciation': '/ˈskɛrtsoʊ/',
            'etymology': 'From Italian scherzo meaning joke or jest, from scherzare meaning to joke or play.',
            'memory_tip': 'Think "SCARE-TSO" - a musical joke that might playfully scare you with unexpected twists.',
            'example_sentence': 'The orchestra performed Beethoven\'s _____ with infectious energy that had the audience smiling.',
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
        'scherzoschnecken': {
            'word': 'scherzoschnecken',
            'definition': '[COMBINED WORD ERROR] This appears to be two words combined: "scherzo" (a playful musical composition) and "schnecken" (German for snails or a type of pastry). This combination likely resulted from a data processing error where two separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words with their individual meanings and contexts.',
            'pronunciation': '/ˈskɛrtsoʊˈʃnɛkən/',
            'etymology': 'Error combination of Italian scherzo (musical joke) + German schnecken (snails/pastries)',
            'memory_tip': 'This is a combined word error - look for the separation between scherzo and schnecken.',
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
        'schism': {
            'word': 'schism',
            'definition': 'A formal division or split within a religious organization, political party, or other group, typically resulting from differences in doctrine, leadership, or fundamental beliefs. Religious schisms have historically created separate denominations or sects, such as the Great Schism of 1054 that divided Eastern Orthodox and Roman Catholic churches. Political schisms can fracture parties or movements when factions develop irreconcilable differences. The term implies a serious, often permanent separation that goes beyond temporary disagreements to create lasting institutional divisions. Schisms usually involve competing claims to legitimacy and authority, with each side believing they represent the true or correct position. Such divisions can have profound historical consequences, affecting millions of followers and shaping cultural and political landscapes.',
            'pronunciation': '/ˈskɪzəm/ or /ˈsɪzəm/',
            'etymology': 'From Greek σχίσμα (schisma) meaning split or division, from σχίζω (schizo) meaning to split.',
            'memory_tip': 'Think "SCHISM" sounds like "PRISM" - both involve splitting, one splits groups, the other splits light.',
            'example_sentence': 'The theological disagreement led to a permanent _____ that created two separate religious denominations.',
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
        'schnecken': {
            'word': 'schnecken',
            'definition': 'A German term meaning "snails," but in culinary contexts refers to a type of sweet yeast pastry shaped like a snail shell, similar to cinnamon rolls or sticky buns. These pastries are typically made with enriched yeast dough, filled with cinnamon, sugar, and sometimes nuts or raisins, then rolled into a spiral shape that resembles a snail\'s shell. Schnecken are popular in German and Austrian baking traditions and have been adopted into American bakery culture, especially in areas with German heritage. The pastries are often glazed with icing or topped with sticky caramel sauce. In some regions, variations include different fillings such as poppy seeds, nuts, or fruit preserves. The spiral shape gives them their distinctive appearance and name.',
            'pronunciation': '/ˈʃnɛkən/',
            'etymology': 'German word meaning snails, from Old High German snecko meaning snail or slug.',
            'memory_tip': 'Think "SHNECK-EN" - pastries shaped like snails (schnecke) with the German plural ending.',
            'example_sentence': 'The German bakery featured fresh _____ every morning, their spiral shape glistening with sweet glaze.',
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
        'schnell': {
            'word': 'schnell',
            'definition': 'A German word meaning "fast," "quick," or "rapid," commonly used in musical terminology to indicate a fast tempo or quick execution of a passage. In German-speaking contexts, schnell can be used as an adverb meaning quickly or as an adjective meaning fast. The word appears in various compound terms and expressions in German culture and has been adopted into English in certain specialized contexts, particularly in music and sometimes in military or emergency situations where German terminology persists. In musical scores, "schnell" might appear as a tempo marking to instruct performers to play at a rapid pace. The word reflects the direct, efficient character often associated with German language and culture.',
            'pronunciation': '/ʃnɛl/',
            'etymology': 'From Old High German snel meaning quick, nimble, or brave.',
            'memory_tip': 'Think "SCHNELL" sounds sharp and quick like the word itself means - quick and snappy.',
            'example_sentence': 'The conductor marked the passage "_____ " to indicate it should be played at a very fast tempo.',
            'part_of_speech': 'adjective/adverb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'schnitzel': {
            'word': 'schnitzel',
            'definition': 'A traditional German and Austrian dish consisting of a thin, breaded cutlet of meat, typically veal, pork, or chicken, that is coated in breadcrumbs and pan-fried until golden brown. The most famous variety is Wiener Schnitzel, which traditionally uses veal and is served with lemon wedges. The preparation involves pounding the meat thin, dredging it in flour, dipping in beaten egg, coating with fine breadcrumbs, and frying in oil or butter. Schnitzel has become popular worldwide and spawned many variations, including chicken schnitzel, pork schnitzel, and vegetarian versions using alternative proteins. The dish is often served with potatoes, Austrian potato salad, or spaetzle, and represents comfort food in German-speaking countries. Proper schnitzel should have a crispy, golden exterior and tender interior.',
            'pronunciation': '/ˈʃnɪtsəl/',
            'etymology': 'From German Schnitzel, diminutive of Schnitz meaning slice or cut.',
            'memory_tip': 'Think "SCHNIT-ZEL" - a thin slice (schnitt) of meat that\'s been cut and breaded.',
            'example_sentence': 'The restaurant\'s authentic Wiener _____ was served with a traditional cucumber salad and lemon wedge.',
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
        'scholarship': {
            'word': 'scholarship',
            'definition': 'Financial aid awarded to students based on academic merit, athletic ability, special talents, or financial need to help cover educational expenses such as tuition, books, and living costs. Scholarships are typically grants that do not require repayment, distinguishing them from student loans. They can be funded by educational institutions, private organizations, government programs, or individual donors. The term also refers to serious academic study and research, particularly the systematic investigation and advancement of knowledge in specific fields. Scholarly work involves rigorous research methodologies, peer review, and contribution to the academic literature. Quality scholarship demonstrates thorough understanding of existing knowledge, original thinking, and adherence to academic standards. Both meanings emphasize excellence and dedication to learning.',
            'pronunciation': '/ˈskɒlərʃɪp/',
            'etymology': 'From scholar + -ship suffix, where scholar comes from Latin scholaris meaning of or belonging to school.',
            'memory_tip': 'Think "SCHOLAR-SHIP" - like a ship that carries scholars on their educational journey.',
            'example_sentence': 'Her outstanding academic performance earned her a full _____ to study engineering at the university.',
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
        'schools': {
            'word': 'schools',
            'definition': 'Educational institutions where students receive instruction in various subjects, typically organized by age groups and academic levels. Schools can range from elementary and secondary institutions to specialized training facilities, vocational colleges, and universities. The structure and curriculum of schools vary by country, culture, and educational philosophy, but most share the common goal of transmitting knowledge, skills, and cultural values to students. Modern schools often incorporate technology, diverse teaching methods, and extracurricular activities to provide comprehensive education. The term can also refer to groups of fish swimming together, or to philosophical or artistic movements characterized by shared principles or styles. As a verb, "schools" means to educate or train someone, often implying disciplined instruction.',
            'pronunciation': '/skuːlz/',
            'etymology': 'From Latin schola, from Greek σχολή (schole) meaning leisure time devoted to learning.',
            'memory_tip': 'Think "SCHOOLS" - places where students learn in groups, like schools of fish swimming together.',
            'example_sentence': 'The district invested in new technology for all elementary _____ to improve digital literacy education.',
            'part_of_speech': 'noun (plural)/verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'schooner': {
            'word': 'schooner',
            'definition': 'A type of sailing vessel characterized by having two or more masts with fore-and-aft rigged sails, where the foremast is shorter than the mainmast. Schooners were particularly popular during the 18th and 19th centuries for coastal trading, fishing, and private sailing due to their speed, maneuverability, and efficiency with smaller crews. The design originated in colonial America and became iconic in New England\'s maritime culture. Famous schooners include racing vessels like America (winner of the first America\'s Cup) and working boats used in the Grand Banks fishing industry. Modern schooners are primarily used for recreational sailing, sailing education, and tourism. The term can also refer to a large beer glass, particularly in Australia, though the size varies by region.',
            'pronunciation': '/ˈskuːnər/',
            'etymology': 'Origin uncertain, possibly from Scottish scoon meaning to skip stones on water, referring to the vessel\'s smooth sailing.',
            'memory_tip': 'Think "SCOON-ER" - a boat that scoots or skims smoothly across the water with its efficient sail design.',
            'example_sentence': 'The historic _____ offered sunset sailing tours around the harbor during the summer months.',
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
        'schwa': {
            'word': 'schwa',
            'definition': 'The most common vowel sound in English, represented by the symbol /ə/ in phonetic transcription, characterized by a neutral, unstressed pronunciation typically found in unaccented syllables. The schwa sound is neither distinctly front nor back, high nor low, and represents the natural resting position of the tongue and jaw when producing vowels. It appears in many common English words, such as the "a" in "about," the "e" in "taken," and the "o" in "lemon." Understanding schwa is crucial for English pronunciation and spelling because many vowel letters in unstressed positions reduce to this neutral sound. The concept helps explain why spelling certain words can be challenging, as the actual pronunciation may not clearly indicate which vowel letter to use.',
            'pronunciation': '/ʃwɑː/',
            'etymology': 'From Hebrew שְׁוָא (shəwā), originally referring to a diacritic mark indicating the absence of a vowel sound.',
            'memory_tip': 'Think "SHWA" - the "uh" sound that\'s so common it needs its own special name and symbol.',
            'example_sentence': 'The linguistics professor explained how the _____ sound appears in most unstressed syllables in English.',
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
        'schwegel': {
            'word': 'schwegel',
            'definition': 'A historic woodwind instrument from the Renaissance and Baroque periods, similar to a small recorder or fife, typically made of wood and used in military and folk music contexts. The schwegel was particularly associated with German and Austrian musical traditions and was often used alongside drums in military bands. These instruments were usually simple, cylindrical tubes with finger holes and produced a bright, piercing sound suitable for outdoor performances and signaling. The schwegel represents an important part of early woodwind instrument development and provides insight into historical musical practices. While largely obsolete today, similar instruments survive in folk music traditions and are studied by early music specialists and instrument makers interested in authentic historical performance practices.',
            'pronunciation': '/ˈʃveɪɡəl/',
            'etymology': 'From German schwegel, related to Middle High German swegel meaning pipe or fife.',
            'memory_tip': 'Think "SHWAY-GEL" - a small German flute that sways with its bright, piercing music.',
            'example_sentence': 'The early music ensemble included a _____ to recreate the authentic sound of 16th-century military music.',
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
        'sciatica': {
            'word': 'sciatica',
            'definition': 'A medical condition characterized by pain that radiates along the path of the sciatic nerve, which runs from the lower back through the hips and buttocks and down each leg. Typically, sciatica affects only one side of the body and can range from mild discomfort to severe, debilitating pain that interferes with daily activities. The condition is usually caused by compression or irritation of the sciatic nerve due to herniated discs, bone spurs, spinal stenosis, or piriformis syndrome. Symptoms may include sharp, burning, or shooting pain, numbness, tingling, or muscle weakness in the affected leg. Treatment options range from conservative approaches like physical therapy, medications, and lifestyle modifications to more intensive interventions such as steroid injections or surgery in severe cases.',
            'pronunciation': '/saɪˈætɪkə/',
            'etymology': 'From Latin sciaticus, from Greek ἰσχιαδικός (iskhiadikos) meaning of the hip, from ἰσχίον (iskhion) meaning hip joint.',
            'memory_tip': 'Think "SCI-ATTIC-A" - pain that travels down from the lower back like going down from an attic.',
            'example_sentence': 'The office worker developed _____ from prolonged sitting and poor posture at her desk.',
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
        'science': {
            'word': 'science',
            'definition': 'The systematic study of the natural world through observation, experimentation, and the formulation of theories and laws that explain phenomena. Science encompasses multiple disciplines including physics, chemistry, biology, geology, astronomy, and others, each focused on understanding specific aspects of the universe. The scientific method provides a structured approach to inquiry involving hypothesis formation, controlled experimentation, data collection, analysis, and peer review. Science aims to build reliable, verifiable knowledge that can predict natural phenomena and inform technological applications. Modern science has revolutionized human understanding of everything from subatomic particles to cosmic structures, leading to countless innovations that improve quality of life and expand human capabilities.',
            'pronunciation': '/ˈsaɪəns/',
            'etymology': 'From Latin scientia meaning knowledge, from scire meaning to know.',
            'memory_tip': 'Think "SCI-ENCE" - the "essence" of knowledge gained through systematic study.',
            'example_sentence': 'The Nobel Prize recognizes outstanding contributions to _____ that advance human understanding of the natural world.',
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
        'scientific': {
            'word': 'scientific',
            'definition': 'Relating to or characterized by the methods, principles, and objectives of science; based on systematic observation, experimentation, and empirical evidence rather than opinion or speculation. Scientific approaches emphasize objectivity, reproducibility, and rigorous testing of hypotheses through controlled experiments. Scientific knowledge is subject to peer review and must be verifiable by independent researchers. The term describes research methodologies, instruments, theories, and discoveries that adhere to established standards of scientific inquiry. Scientific thinking involves critical analysis, logical reasoning, and the willingness to revise conclusions when new evidence emerges. This approach has proven highly effective for understanding natural phenomena and developing reliable technologies and medical treatments.',
            'pronunciation': '/ˌsaɪənˈtɪfɪk/',
            'etymology': 'From Latin scientificus, from scientia (knowledge) + facere (to make or do).',
            'memory_tip': 'Think "SCIENCE-TIFIC" - something that makes or produces knowledge through scientific methods.',
            'example_sentence': 'The researchers followed strict _____ protocols to ensure their climate change study would be credible.',
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
        'scintillation': {
            'word': 'scintillation',
            'definition': 'The process of emitting brief flashes of light, particularly the twinkling effect observed when light passes through a medium with varying optical properties. In astronomy, scintillation refers to the twinkling of stars caused by atmospheric turbulence that bends and distorts starlight as it travels through air masses of different temperatures and densities. In physics and medical imaging, scintillation describes the phenomenon where certain materials emit light when struck by ionizing radiation, making them useful in radiation detectors and medical scanners. The term can also refer metaphorically to sparkling wit, brilliant conversation, or any display of intellectual brilliance that captures attention. Scintillation detectors are crucial tools in nuclear physics, medical imaging, and space exploration.',
            'pronunciation': '/ˌsɪntɪˈleɪʃən/',
            'etymology': 'From Latin scintillare meaning to sparkle or glitter, from scintilla meaning spark.',
            'memory_tip': 'Think "SCINTILLA-TION" - the action of creating tiny sparks or flashes of light.',
            'example_sentence': 'The _____ of the stars was particularly noticeable on the humid summer night.',
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
        'sciolistic': {
            'word': 'sciolistic',
            'definition': 'Characterized by superficial knowledge or learning; pretending to knowledge without having genuine understanding or depth of study. A sciolistic person displays shallow learning while appearing knowledgeable, often using technical terms or references incorrectly or without true comprehension. This adjective describes intellectual pretension that lacks substance, where someone has acquired enough surface knowledge to seem informed but lacks the deep understanding that comes from serious study. Sciolistic behavior often involves name-dropping, using jargon inappropriately, or making confident statements about subjects beyond one\'s actual expertise. The term implies a kind of intellectual dishonesty or self-deception where appearance of knowledge substitutes for genuine learning.',
            'pronunciation': '/saɪəˈlɪstɪk/',
            'etymology': 'From Latin sciolus meaning having superficial knowledge + -istic suffix, from scire meaning to know.',
            'memory_tip': 'Think "SCI-OL-ISTIC" - someone who knows a little science (sci) but acts like they know it all.',
            'example_sentence': 'His _____ commentary on the research revealed he had only read the abstract, not the full study.',
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
        'sclaff': {
            'word': 'sclaff',
            'definition': 'In golf, to strike the ground with the club before hitting the ball, resulting in a mishit shot that typically travels a shorter distance and with less accuracy than intended. This common golf error occurs when the club head contacts the turf behind the ball, often caused by poor weight transfer, incorrect posture, or improper swing plane. A sclaff can also refer to the sound made when this happens - a dull thud as the club digs into the earth. The term is primarily used in British golf terminology and represents one of the frustrating mistakes that golfers at all skill levels occasionally experience. Proper instruction and practice can help minimize sclaffing by improving swing mechanics and consistency.',
            'pronunciation': '/sklæf/',
            'etymology': 'Possibly from Scottish dialect, imitative of the sound made when a golf club hits the ground.',
            'memory_tip': 'Think "SC-LAUGH" - other golfers might laugh when you hit the ground before the ball.',
            'example_sentence': 'The amateur golfer began to _____ several shots when he became nervous during the tournament.',
            'part_of_speech': 'verb/noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'sclerosis': {
            'word': 'sclerosis',
            'definition': 'A pathological hardening or thickening of body tissues, typically involving the replacement of normal tissue with fibrous connective tissue, leading to loss of normal function. In medical contexts, sclerosis can affect various organs and systems, with multiple sclerosis being the most widely known form, where the protective covering of nerve fibers becomes damaged. Atherosclerosis involves hardening of arteries due to plaque buildup, while liver sclerosis (cirrhosis) involves scarring that impairs liver function. The condition represents the body\'s response to chronic inflammation or injury, but the resulting tissue changes often worsen rather than improve function. Treatment approaches vary depending on the type and location of sclerosis, ranging from medications to slow progression to therapies that manage symptoms.',
            'pronunciation': '/skləˈroʊsɪs/',
            'etymology': 'From Greek σκλήρωσις (sklerosis) meaning hardening, from σκληρός (skleros) meaning hard.',
            'memory_tip': 'Think "SCLER-OSIS" - a medical condition where tissues become hard like a "sclera" (the hard white part of the eye).',
            'example_sentence': 'The neurologist explained how multiple _____ affects the central nervous system by damaging nerve coverings.',
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
        'scobiform': {
            'word': 'scobiform',
            'definition': 'Having the appearance or consistency of sawdust; resembling fine shavings or small particles typically produced by filing, scraping, or sawing. This technical term is used in various scientific and medical contexts to describe materials, substances, or tissue formations that have a granular, powdery, or sawdust-like texture. In pathology, scobiform might describe certain types of tissue degeneration or abnormal formations. In materials science, it could refer to the physical appearance of processed materials or waste products. The term provides a precise descriptive tool for professionals who need to communicate specific textural characteristics in technical documentation, research papers, or diagnostic reports.',
            'pronunciation': '/ˈskoʊbɪfɔːrm/',
            'etymology': 'From Latin scobis meaning sawdust or filings + forma meaning shape or form.',
            'memory_tip': 'Think "SCOB-I-FORM" - shaped like or having the form of sawdust particles.',
            'example_sentence': 'The pathologist noted the _____ appearance of the tissue sample under microscopic examination.',
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
        'scoff': {
            'word': 'scoff',
            'definition': 'To express contempt, mockery, or derision toward someone or something, typically through sarcastic remarks, dismissive laughter, or sneering comments. Scoffing involves showing disbelief or scorn for ideas, suggestions, or claims that one considers foolish, unrealistic, or unworthy of serious consideration. The behavior often includes verbal expressions of ridicule or disdain, sometimes accompanied by facial expressions or gestures that convey disrespect. Scoffing can be directed at people, ideas, proposals, or beliefs that the scoffer deems inferior or absurd. While sometimes justified as critical thinking, habitual scoffing can become a negative trait that prevents open-minded consideration of new or different perspectives.',
            'pronunciation': '/skɔːf/',
            'etymology': 'Possibly from Middle English scof meaning mockery, or from Old Norse skop meaning mocking poetry.',
            'memory_tip': 'Think "SCOFF" rhymes with "cough" - both involve making dismissive sounds with your mouth.',
            'example_sentence': 'The critics began to _____ at the young inventor\'s ambitious claims about clean energy.',
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
        'scold': {
            'word': 'scold',
            'definition': 'To rebuke, criticize, or reprimand someone angrily or severely, typically for wrongdoing, mistakes, or unacceptable behavior. Scolding involves verbal correction that expresses disapproval and often includes raised voice, stern tone, and specific mention of what the person did wrong. This form of discipline is common in parent-child relationships, teacher-student interactions, and supervisory situations where authority figures need to address behavioral issues. Effective scolding focuses on specific behaviors rather than personal attacks and aims to correct future actions. However, excessive or harsh scolding can damage relationships and self-esteem. The noun form refers to a person, historically often a woman, who habitually nags or criticizes others.',
            'pronunciation': '/skoʊld/',
            'etymology': 'From Old Norse skald meaning poet, later meaning one who uses harsh language.',
            'memory_tip': 'Think "SCOLD" sounds like "COLD" - scolding gives someone the cold treatment with harsh words.',
            'example_sentence': 'The teacher had to _____ the students for talking during the important safety presentation.',
            'part_of_speech': 'verb/noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'sconce': {
            'word': 'sconce',
            'definition': 'A wall-mounted light fixture, typically decorative, that holds candles or electric bulbs and often includes a reflective backing to direct light into a room. Sconces have been used throughout history to provide ambient lighting while saving table and floor space. Traditional sconces featured ornate metalwork, mirrors, or decorative elements that complemented interior design styles. Modern sconces come in various designs from minimalist contemporary styles to elaborate period reproductions. The term can also refer to a small fort or earthwork, particularly in military historical contexts. In some regions, sconce informally means head or skull. Architectural sconces serve both functional and aesthetic purposes, contributing to a room\'s lighting scheme and decorative character.',
            'pronunciation': '/skɒns/',
            'etymology': 'From Old French esconse meaning hiding place, from Latin abscondere meaning to hide.',
            'memory_tip': 'Think "S-CONS" - wall fixtures that conserve (cons) space while providing light.',
            'example_sentence': 'The hallway was illuminated by elegant brass _____ that cast warm light on the artwork.',
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
        'scoop': {
            'word': 'scoop',
            'definition': 'A utensil with a deep bowl shape and handle, used for lifting and moving loose materials such as flour, ice cream, or soil. The design allows for measuring and transferring specific quantities of substances efficiently. In journalism, a scoop refers to an exclusive news story obtained before competitors, representing a significant professional achievement. The verb form means to lift, gather, or hollow out using a scooping motion. Ice cream scoops are specialized tools designed to create uniform portions, while larger scoops serve industrial or agricultural purposes. Metaphorically, "scoop" can mean to gather up or collect something quickly, as in "scooping up bargains" at a sale. The term emphasizes the curved, gathering motion characteristic of the tool.',
            'pronunciation': '/skuːp/',
            'etymology': 'From Middle Dutch schoepe meaning bucket or scoop, related to schoppen meaning to shovel.',
            'memory_tip': 'Think "SCOOP" like the sound of gathering something up in one swooping motion.',
            'example_sentence': 'The ice cream parlor used a special heated _____ to create perfect spherical servings.',
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
        'scooter': {
            'word': 'scooter',
            'definition': 'A lightweight vehicle with two wheels, a platform for standing, and a steering handle, propelled by pushing off the ground with one foot while the other remains on the platform. Traditional kick scooters are popular among children and adults for recreation and short-distance transportation. Motor scooters feature small engines and are widely used for urban commuting, particularly in crowded cities where their maneuverability and fuel efficiency provide advantages over larger vehicles. Electric scooters have gained popularity as eco-friendly transportation options and are often available through ride-sharing programs. The term can also refer to mobility scooters designed for people with disabilities or mobility limitations. Modern scooters range from simple toys to sophisticated transportation devices with advanced features.',
            'pronunciation': '/ˈskuːtər/',
            'etymology': 'From scoot + -er suffix, where scoot means to move quickly or suddenly.',
            'memory_tip': 'Think "SCOOT-ER" - a device that helps you scoot along quickly on wheels.',
            'example_sentence': 'The city introduced electric _____ sharing to reduce traffic congestion and pollution.',
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
        'scornfully': {
            'word': 'scornfully',
            'definition': 'In a manner expressing extreme contempt, disdain, or derision; with an attitude that shows someone or something is considered beneath consideration or unworthy of respect. Scornful behavior typically involves dismissive gestures, sneering expressions, or condescending language that demonstrates superiority and rejection. Acting scornfully often reflects deep disapproval or disgust with another person\'s actions, ideas, or character. The adverb describes the way someone might respond to suggestions they find ridiculous, proposals they consider insulting, or people they regard as inferior. While scornful responses can sometimes be justified reactions to genuinely problematic behavior, habitual scornfulness often reveals arrogance or inability to consider alternative perspectives.',
            'pronunciation': '/ˈskɔːrnfʊli/',
            'etymology': 'From scorn + -ful + -ly, where scorn comes from Old French escarn meaning mockery.',
            'memory_tip': 'Think "SCORN-FULLY" - being full of scorn and expressing it completely.',
            'example_sentence': 'She looked _____ at the suggestion that she had made an error in her calculations.',
            'part_of_speech': 'adverb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scorpion': {
            'word': 'scorpion',
            'definition': 'An arachnid arthropod characterized by eight legs, a pair of grasping pincers, and a segmented tail ending in a venomous stinger. Scorpions are found in warm climates worldwide and are primarily nocturnal predators that hunt insects, spiders, and other small prey. Their venom varies in potency among species, with some causing only mild discomfort while others can be potentially fatal to humans. Scorpions have existed for over 400 million years and have adapted to various environments from deserts to tropical forests. They use their pincers to capture prey and their stingers for defense and subduing larger victims. Many species glow under ultraviolet light due to fluorescent compounds in their exoskeletons, making them popular subjects for nature photography.',
            'pronunciation': '/ˈskɔːrpiən/',
            'etymology': 'From Latin scorpio, from Greek σκορπίος (skorpios), possibly related to the root meaning to cut.',
            'memory_tip': 'Think "SCOR-PION" - an animal that can score you with its painful stinger.',
            'example_sentence': 'The desert hiker carefully checked his boots for _____ before putting them on each morning.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scoundrel': {
            'word': 'scoundrel',
            'definition': 'A dishonest, unscrupulous person who engages in deceitful or villainous behavior; someone who lacks moral principles and takes advantage of others for personal gain. Scoundrels typically display patterns of lying, cheating, stealing, or manipulating others without remorse or consideration for the harm they cause. The term carries strong negative connotations and implies deliberate wrongdoing rather than mere mistakes or poor judgment. Historical literature often features scoundrels as antagonists who create conflict through their selfish and harmful actions. While sometimes used playfully or affectionately for minor mischief, the word generally describes serious character flaws and unethical behavior that damages trust and relationships.',
            'pronunciation': '/ˈskaʊndrəl/',
            'etymology': 'Origin uncertain, possibly from Anglo-Norman escoundre meaning to hide or skulk.',
            'memory_tip': 'Think "SOUND-REL" - someone whose reputation sounds terrible because of their bad behavior.',
            'example_sentence': 'The townspeople finally realized that the charming newcomer was actually a _____ who had swindled several families.',
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
        'scourge': {
            'word': 'scourge',
            'definition': 'A cause of widespread suffering, destruction, or trouble; something that inflicts severe punishment or serves as a source of persistent problems. Historically, scourges included diseases like plague, natural disasters, or military invasions that devastated populations. In modern contexts, drugs, poverty, violence, or environmental problems might be described as scourges affecting communities. The term can also refer to a whip or instrument of punishment, particularly in historical or religious contexts where physical discipline was common. As a verb, to scourge means to cause suffering or to punish severely. The word emphasizes the severity and widespread nature of the problem, suggesting something that requires urgent attention and coordinated response to address.',
            'pronunciation': '/skɜːrdʒ/',
            'etymology': 'From Old French escorge meaning whip, from Latin excoriare meaning to flay or strip skin.',
            'memory_tip': 'Think "SCOURGE" like "SURGE" - a harmful surge that sweeps through and damages everything.',
            'example_sentence': 'Drug addiction became a _____ that affected families across all economic levels in the community.',
            'part_of_speech': 'noun/verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
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
    
    print(f"\nBatch 155 processing complete!")
    print(f"Successfully processed {len(processed_words)}/{len(words)} words")
    print(f"Output saved to: {output_file}")
    
    if combined_errors:
        print(f"\nCombined word errors detected: {len(combined_errors)}")
        for error in combined_errors:
            print(f"  - {error}")

if __name__ == "__main__":
    process_batch()