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
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_154_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_154_processed.csv'
    
    calculator = DifficultyCalculator()
    
    word_data = {
        'sanitized': {
            'word': 'sanitized',
            'definition': 'Made clean and hygienic by removing harmful bacteria, viruses, or other contaminants through the use of disinfectants or cleaning agents. In medical and food safety contexts, sanitization involves reducing microbial populations to safe levels according to established health standards. The process differs from sterilization, which eliminates all microorganisms, as sanitization focuses on reducing pathogens to acceptable levels. Beyond literal cleaning, the term can also refer to making something more acceptable by removing objectionable content, such as sanitizing language or media by removing profanity or controversial material. In data processing, sanitization refers to removing sensitive information to protect privacy and security.',
            'pronunciation': '/ˈsænɪˌtaɪzd/',
            'etymology': 'From sanitary + -ize + -ed. Sanitary comes from Latin sanitas meaning health, from sanus meaning healthy or sound.',
            'memory_tip': 'Think "SANE-itized" - making something sane and healthy by removing harmful elements.',
            'example_sentence': 'The restaurant kitchen was thoroughly _____ after the health inspector found violations.',
            'part_of_speech': 'adjective/verb (past tense)',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'sannyasi': {
            'word': 'sannyasi',
            'definition': 'In Hinduism, a religious ascetic who has renounced worldly life and entered the fourth and final stage of the traditional ashrama system. A sannyasi abandons material possessions, family ties, and social obligations to pursue spiritual liberation (moksha) through meditation, study of sacred texts, and devotion to the divine. They typically wear saffron-colored robes, carry minimal possessions, and often wander from place to place seeking alms. The term represents someone who has formally taken sannyasa, a sacred vow of renunciation that marks the transition from householder life to complete dedication to spiritual pursuits. Sannyasis are revered in Hindu society as having achieved a high level of spiritual development and detachment from worldly desires.',
            'pronunciation': '/sʌnˈjɑːsi/',
            'etymology': 'From Sanskrit संन्यासी (sannyāsī), from संन्यास (sannyāsa) meaning renunciation, from सम् (sam-) meaning completely + न्यास (nyāsa) meaning laying down or abandoning.',
            'memory_tip': 'Remember "SUN-yogi" - someone who has renounced everything to follow the spiritual path like a yogi under the sun.',
            'example_sentence': 'The elderly _____ walked barefoot through the village, carrying only a water pot and sacred texts.',
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
        'sanskrit': {
            'word': 'sanskrit',
            'definition': 'An ancient Indo-European language of India that serves as the liturgical language of Hinduism and Buddhism. Sanskrit is one of the oldest attested languages in the Indo-European family, with texts dating back over 3,500 years. The language exists in two main forms: Vedic Sanskrit, used in the earliest religious texts like the Rigveda, and Classical Sanskrit, systematized by the grammarian Panini around the 4th century BCE. Sanskrit literature encompasses vast religious, philosophical, scientific, and literary works including the Vedas, Upanishads, epics like the Mahabharata and Ramayana, and numerous treatises on mathematics, astronomy, and medicine. Though no longer spoken as a native language, Sanskrit continues to influence modern Indian languages and serves as a scholarly language for traditional learning.',
            'pronunciation': '/ˈsænskrɪt/',
            'etymology': 'From Sanskrit संस्कृत (saṃskṛta) meaning refined, perfect, or well-formed, from सम् (sam-) meaning together + कृत (kṛta) meaning made or done.',
            'memory_tip': 'Think "SANDS-script" - ancient writings in the sands of time that formed the foundation of Indian culture.',
            'example_sentence': 'Many yoga poses retain their traditional _____ names even in modern Western practice.',
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
        'saoshyant': {
            'word': 'saoshyant',
            'definition': 'In Zoroastrian eschatology, a future savior figure who will arrive at the end of time to resurrect the dead, judge all souls, and establish the final renovation of the world. The Saoshyant, whose name means "one who brings benefit," is prophesied to be born of a virgin impregnated by the preserved seed of Zoroaster. This messianic figure will defeat Ahriman (the destructive spirit), purify the world with molten metal that will feel like warm milk to the righteous but burn the wicked, and create a perfect world where death, disease, and evil no longer exist. The concept of the Saoshyant significantly influenced later Abrahamic religions\' concepts of messianic figures and final judgment. Three Saoshyants are prophesied to appear in succession, with the final one completing the cosmic renovation.',
            'pronunciation': '/saʊʃjɑːnt/',
            'etymology': 'From Avestan saošyant, meaning "one who brings benefit" or "savior," from the root saošya- meaning beneficial.',
            'memory_tip': 'Think "SAW-shiny-ant" - a prophesied savior who will make the world shine with perfection.',
            'example_sentence': 'Zoroastrian prophecies describe the _____ as the ultimate redeemer who will renovate the world.',
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
        'saoshyanttachyon': {
            'word': 'saoshyanttachyon',
            'definition': '[COMBINED WORD ERROR] This appears to be two unrelated words combined: "saoshyant" (a Zoroastrian messianic figure) and "tachyon" (a hypothetical faster-than-light particle in physics). This combination likely resulted from a data processing error where two separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words: "saoshyant" and "tachyon" each with their own definitions and contexts.',
            'pronunciation': '/saʊʃjɑːntˈtækiɒn/',
            'etymology': 'Error combination of Avestan saošyant (savior) + Greek tachyon (swift particle)',
            'memory_tip': 'This is a combined word error - look for the separation between saoshyant and tachyon.',
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
        'saponaceouscyrillic': {
            'word': 'saponaceouscyrillic',
            'definition': '[COMBINED WORD ERROR] This appears to be two unrelated words combined: "saponaceous" (having the qualities of soap, soapy or slippery) and "cyrillic" (relating to the alphabet used for Russian and other Slavic languages). This combination likely resulted from a data processing error where two separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words: "saponaceous" and "cyrillic" each with their own definitions and contexts.',
            'pronunciation': '/səˈpoʊneɪʃəssɪˈrɪlɪk/',
            'etymology': 'Error combination of Latin saponaceus (soapy) + Greek Cyrillicus (relating to Cyril)',
            'memory_tip': 'This is a combined word error - look for the separation between saponaceous and cyrillic.',
            'example_sentence': 'The data contained an error where _____ appeared instead of two separate words.',
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
        'sapphire': {
            'word': 'sapphire',
            'definition': 'A precious gemstone variety of the mineral corundum, composed of aluminum oxide with trace amounts of other elements that give it various colors. While sapphires can occur in many colors including yellow, pink, white, and green, the most prized are the deep blue varieties colored by titanium and iron. Sapphires rank 9 on the Mohs hardness scale, making them extremely durable and suitable for fine jewelry. The finest sapphires come from Kashmir, Burma (Myanmar), and Sri Lanka. In addition to their use in jewelry, synthetic sapphires are employed in various industrial applications including watch crystals, optical components, and semiconductor substrates. Historically, sapphires have been associated with royalty, wisdom, and divine favor.',
            'pronunciation': '/ˈsæfaɪər/',
            'etymology': 'From Old French safir, from Latin sapphirus, from Greek σάπφειρος (sappheiros), possibly from a Semitic language or Sanskrit śanipriya meaning dear to Saturn.',
            'memory_tip': 'Think "SAFE-fire" - a precious blue gem that safely holds the fire of beauty within its crystal structure.',
            'example_sentence': 'The princess wore a stunning blue _____ engagement ring that had been in the royal family for generations.',
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
        'sapporo': {
            'word': 'sapporo',
            'definition': 'The capital city of Hokkaido Prefecture and the largest city in northern Japan, known for its beer brewing industry, winter sports facilities, and annual Snow Festival. Sapporo is famous for hosting the 1972 Winter Olympics and developing into a major urban center despite being relatively young, founded in 1868 during the Meiji period. The city is renowned for Sapporo Beer, one of Japan\'s oldest beer brands, and for its distinctive urban planning with wide streets laid out in a grid pattern. The Sapporo Snow Festival, held every February, attracts millions of visitors who come to see elaborate ice and snow sculptures. The city also serves as an important agricultural center and gateway to Hokkaido\'s natural attractions.',
            'pronunciation': '/səˈpɔːroʊ/',
            'etymology': 'From Ainu sat poro pet meaning "dry great river," referring to the Toyohira River that flows through the city.',
            'memory_tip': 'Think "SAP-BORO" - a city that tapped into the "sap" of nature to grow into a major borough.',
            'example_sentence': 'The 1972 Winter Olympics put _____ on the international map as a world-class winter sports destination.',
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
        'sarcophagus': {
            'word': 'sarcophagus',
            'definition': 'A stone coffin or burial chamber, typically decorated with elaborate carvings, inscriptions, or sculptures, used in ancient civilizations for entombing the dead. Originally developed by ancient Egyptians and Greeks, sarcophagi were often made from limestone, granite, or marble and featured artistic depictions of the deceased, religious scenes, or mythological narratives. The most famous examples include Egyptian pharaonic sarcophagi with hieroglyphic inscriptions and Roman sarcophagi with detailed relief sculptures. These burial containers served both practical and symbolic purposes, protecting the body while demonstrating the wealth, status, and beliefs of the deceased. Modern archaeological discoveries of intact sarcophagi continue to provide valuable insights into ancient burial practices, artistry, and cultural beliefs about the afterlife.',
            'pronunciation': '/sɑːrˈkɒfəɡəs/',
            'etymology': 'From Greek σαρκοφάγος (sarkophagos) meaning "flesh-eating," from σάρξ (sarx) meaning flesh + φαγεῖν (phagein) meaning to eat, referring to a type of limestone believed to consume flesh.',
            'memory_tip': 'Think "SCAR-COFFEE-GAB" - ancient carved stone coffins where people would gather to tell stories about the deceased.',
            'example_sentence': 'The archaeologists carefully opened the ancient _____ to reveal a perfectly preserved mummy inside.',
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
        'sardine': {
            'word': 'sardine',
            'definition': 'A small, oily fish belonging to the herring family, typically preserved in cans with oil, water, or sauce. Sardines are nutrient-dense fish rich in omega-3 fatty acids, protein, calcium, and vitamin D, making them valuable both nutritionally and economically. Several species are called sardines, including true sardines (Sardina pilchardus) and various small herrings and anchovies that are processed similarly. These fish are often caught in large schools using purse seine nets and are important both as food for humans and as bait for larger fish. The phrase "packed like sardines" derives from how these fish are tightly arranged in cans, symbolizing cramped conditions. Sardine fishing and canning industries have been historically significant in coastal regions of Portugal, Spain, and California.',
            'pronunciation': '/sɑːrˈdiːn/',
            'etymology': 'From French sardine, from Latin sardina, named after Sardinia, the Mediterranean island where they were abundant.',
            'memory_tip': 'Think of the island of Sardinia where these small fish were first caught and canned in abundance.',
            'example_sentence': 'The picnic lunch included crackers topped with _____ and a squeeze of fresh lemon.',
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
        'sardonic': {
            'word': 'sardonic',
            'definition': 'Characterized by bitter, scornful, or mocking humor that often conveys cynicism or contempt. A sardonic attitude involves a harsh form of irony that typically ridicules or dismisses something as foolish or worthless. This type of humor is more cutting and bitter than simple sarcasm, often revealing deep-seated pessimism or disillusionment with human nature or society. Sardonic expressions frequently appear in literature to convey characters\' world-weariness or intellectual superiority. The term suggests a deliberate cruelty in the humor, as if the speaker takes pleasure in pointing out the failures or absurdities of others. Sardonic wit is often associated with sophisticated, cynical characters who view the world with detached amusement at its follies.',
            'pronunciation': '/sɑːrˈdɒnɪk/',
            'etymology': 'From French sardonique, from Latin sardonicus, from Greek σαρδόνιος (sardonios), possibly referring to a Sardinian plant that caused facial contortions resembling bitter laughter.',
            'memory_tip': 'Think "SAD-IRONIC" - humor that is sad and ironic, expressing bitter amusement at life\'s disappointments.',
            'example_sentence': 'His _____ comment about the failed project revealed his deep frustration with management.',
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
        'sarkara': {
            'word': 'sarkara',
            'definition': 'An ancient Sanskrit term referring to sugar or sweet substances, particularly crystallized sugar or sugar candy. In traditional Ayurvedic medicine and ancient Indian texts, sarkara represents various forms of sweetening agents derived from sugarcane, palm sap, or other natural sources. The term appears in classical Sanskrit literature describing both culinary preparations and medicinal formulations where sugar served as a vehicle for delivering herbal remedies. In historical contexts, sarkara was a valuable trade commodity, with ancient texts describing different grades and types of sugar crystals. The word is etymologically related to the English word "sugar" through various linguistic transformations across Persian, Arabic, and European languages, demonstrating the historical importance of sugar in global trade.',
            'pronunciation': '/sʌrˈkɑːrə/',
            'etymology': 'From Sanskrit शर्करा (śarkarā) meaning sugar, crystallized sugar, or gravel, ultimately the source of the word "sugar" through Persian and Arabic.',
            'memory_tip': 'Think "SAR-CAR-A" - ancient Sanskrit word for sugar that traveled by caravan across continents.',
            'example_sentence': 'Ancient Sanskrit texts mention _____ as both a sweetener and a medicinal ingredient.',
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
        'sarmentum': {
            'word': 'sarmentum',
            'definition': 'In botany, a long, slender, trailing or climbing stem that runs along the ground or climbs over other plants, capable of producing new plants at nodes or tips. Sarmenta (plural) are specialized vegetative structures found in plants like strawberries, grape vines, and many ground-covering species. These structures differ from true roots in that they grow above ground and contain nodes where leaves, roots, and new shoots can develop. When a sarmentum touches soil, it can form adventitious roots at the nodes, effectively creating a new plant clone. This reproductive strategy allows plants to spread horizontally and colonize new areas efficiently. In viticulture, understanding sarmentum growth patterns is crucial for proper vine training and pruning to optimize grape production.',
            'pronunciation': '/sɑːrˈmɛntəm/',
            'etymology': 'From Latin sarmentum meaning a twig or cutting, from sarpere meaning to prune or cut.',
            'memory_tip': 'Think "SAR-MEANT-UM" - the plant "meant" to spread by sending out these trailing stems.',
            'example_sentence': 'The botanist identified the strawberry plant\'s _____ as the structure responsible for creating new plants.',
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
        'sartorial': {
            'word': 'sartorial',
            'definition': 'Relating to clothing, style of dress, or the art of tailoring, particularly concerning men\'s fashion and the craft of creating well-fitted garments. Sartorial excellence refers to impeccable taste in clothing selection, attention to detail in fit and coordination, and appreciation for quality craftsmanship in garment construction. The term encompasses not only the physical aspects of clothing but also the cultural and social significance of dress choices, including how attire communicates status, personality, and aesthetic sensibility. In fashion journalism and menswear circles, sartorial discussions often focus on traditional tailoring techniques, fabric selection, and the revival of classic menswear styles. A person with refined sartorial sense demonstrates sophisticated understanding of how clothing elements work together harmoniously.',
            'pronunciation': '/sɑːrˈtɔːriəl/',
            'etymology': 'From Latin sartor meaning tailor, from sarcire meaning to mend or patch.',
            'memory_tip': 'Think "SAR-TAILOR-IAL" - relating to tailors and the art of fine clothing construction.',
            'example_sentence': 'His _____ elegance was evident in the perfectly tailored suit and carefully chosen accessories.',
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
        'sashay': {
            'word': 'sashay',
            'definition': 'To walk in a confident, stylish, or exaggerated manner, often with swaying hips or deliberate, graceful movements that draw attention. The term originated from square dancing, where "sashay" describes a specific dance step involving sliding movements. In broader usage, it describes any form of walking or moving that is particularly elegant, flamboyant, or self-assured, often with an element of showing off or making a dramatic entrance. The movement typically involves a rhythmic, flowing gait that emphasizes grace and confidence. In fashion and performance contexts, to sashay suggests moving with awareness of being observed, whether on a runway, stage, or in social situations where one wants to make an impression.',
            'pronunciation': '/sæˈʃeɪ/',
            'etymology': 'From French chassé, meaning a sliding dance step, from chasser meaning to chase or hunt.',
            'memory_tip': 'Think "SASH-AY" - walking with the confidence of someone wearing a beauty pageant sash.',
            'example_sentence': 'The model began to _____ down the runway with graceful, confident steps.',
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
        'sashaywe': {
            'word': 'sashaywe',
            'definition': '[COMBINED WORD ERROR] This appears to be two words combined: "sashay" (to walk in a confident, stylish manner) and "we" (first person plural pronoun). This combination likely resulted from a data processing error where two separate words were merged without proper spacing. The correct format should separate these as distinct words with their individual meanings and grammatical functions.',
            'pronunciation': '/sæˈʃeɪwi/',
            'etymology': 'Error combination of French chassé (sashay) + English we',
            'memory_tip': 'This is a combined word error - look for the separation between sashay and we.',
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
        'saskatoon': {
            'word': 'saskatoon',
            'definition': 'A North American berry-producing shrub (Amelanchier alnifolia) native to western and central Canada and the northern United States, also known as serviceberry, Juneberry, or shadbush. The dark purple berries are sweet and nutritious, traditionally harvested by Indigenous peoples and early settlers for food preservation and winter sustenance. Saskatoon berries are rich in antioxidants, fiber, and vitamins, with a flavor similar to blueberries but with a hint of almond from the seeds. The plant thrives in prairie and parkland environments and is valued both for its edible fruit and as an ornamental landscape plant. Commercial cultivation of saskatoons has increased in recent decades due to growing interest in native foods and their nutritional benefits.',
            'pronunciation': '/ˌsæskəˈtuːn/',
            'etymology': 'From Cree misâskwatômina, meaning "the fruit of the tree of many branches," referring to the branching pattern of the shrub.',
            'memory_tip': 'Think of Saskatchewan, the Canadian province named after the Cree word for this native berry.',
            'example_sentence': 'The Indigenous guide showed us how to identify ripe _____ berries for our wilderness survival training.',
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
        'satchel': {
            'word': 'satchel',
            'definition': 'A bag with a long shoulder strap, typically made of leather or canvas, used for carrying books, papers, or personal belongings. Traditional satchels feature a flap closure with buckles or straps and are designed for durability and practical use. Originally used by students, messengers, and travelers, satchels have evolved into both functional everyday bags and fashionable accessories. The design typically includes a main compartment with the characteristic flap that folds over the opening, often secured with metal clasps or leather straps. Modern satchels may include additional pockets, laptop compartments, and updated materials while maintaining the classic rectangular shape and cross-body carrying style that makes them practical for hands-free transport.',
            'pronunciation': '/ˈsætʃəl/',
            'etymology': 'From Old French sachel, diminutive of sac meaning bag or sack, ultimately from Latin saccus.',
            'memory_tip': 'Think "SACK-EL" - a small sack that you carry with a strap, like a diminutive of sack.',
            'example_sentence': 'The student carried her textbooks in a worn leather _____ that had belonged to her grandmother.',
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
        'satellite': {
            'word': 'satellite',
            'definition': 'An object that orbits around a larger celestial body, including both natural satellites like moons and artificial satellites launched by humans for various purposes. Natural satellites are gravitationally bound objects that circle planets, with Earth\'s moon being the most familiar example. Artificial satellites serve numerous functions including telecommunications, weather monitoring, GPS navigation, scientific research, and military surveillance. These human-made objects are placed in different orbital patterns depending on their intended use, from low Earth orbit for imaging satellites to geostationary orbit for communication satellites. The term also refers metaphorically to subordinate entities that depend on or revolve around a central authority, such as satellite nations or satellite offices of a company.',
            'pronunciation': '/ˈsætəlaɪt/',
            'etymology': 'From Latin satelles meaning attendant or guard, referring to something that accompanies or follows a principal object.',
            'memory_tip': 'Think "SAT-ELITE" - objects that sit in space as part of an elite network orbiting Earth.',
            'example_sentence': 'The weather _____ provided crucial data for predicting the hurricane\'s path.',
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
        'satiety': {
            'word': 'satiety',
            'definition': 'The state of being completely satisfied or fulfilled, especially in regard to appetite or desire, to the point where no more is wanted or needed. In nutritional and physiological contexts, satiety refers to the feeling of fullness that occurs after eating and helps regulate food intake by signaling when to stop eating. This biological mechanism involves complex interactions between the digestive system, hormones, and brain centers that control hunger and appetite. Beyond physical hunger, satiety can apply to any situation where desires or needs have been completely met, whether material, emotional, or intellectual. The concept is important in understanding eating behaviors, consumer psychology, and the point at which additional consumption provides diminishing satisfaction.',
            'pronunciation': '/səˈtaɪəti/',
            'etymology': 'From Latin satietas meaning fullness or abundance, from satis meaning enough or sufficient.',
            'memory_tip': 'Think "SATISFY-ETY" - the state of being satisfied to the point where you\'ve had enough.',
            'example_sentence': 'After the large meal, a feeling of _____ made it impossible to consider dessert.',
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
        'satisfactory': {
            'word': 'satisfactory',
            'definition': 'Meeting expectations or requirements adequately, though not necessarily excellently; acceptable or sufficient in quality, quantity, or degree. A satisfactory result fulfills the basic criteria or standards needed for approval or acceptance without being outstanding or exceptional. In educational contexts, satisfactory often represents a grade level that demonstrates competent understanding without excellence. The term implies that while improvements might be possible, the current state or performance meets minimum acceptable standards. In professional or technical contexts, satisfactory completion means that all necessary requirements have been fulfilled according to specifications, allowing a project, task, or evaluation to be considered successfully completed rather than requiring additional work or revision.',
            'pronunciation': '/ˌsætɪsˈfæktəri/',
            'etymology': 'From Latin satisfactorius, from satisfacere meaning to do enough, from satis (enough) + facere (to do or make).',
            'memory_tip': 'Think "SATISFY-FACTORY" - like a factory that produces just enough to satisfy requirements.',
            'example_sentence': 'The student\'s performance was _____ but showed room for improvement in future assignments.',
            'part_of_speech': 'adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'satsuma': {
            'word': 'satsuma',
            'definition': 'A variety of mandarin orange (Citrus unshiu) known for its sweet flavor, easy-to-peel skin, and typically seedless segments. Originally cultivated in Japan, satsumas are cold-hardy citrus fruits that can tolerate temperatures lower than most other citrus varieties, making them suitable for cultivation in temperate regions. The fruit has a distinctive loose, easily removable peel and sweet, juicy flesh with minimal acidity. Satsumas ripen earlier than most citrus fruits, typically in late fall and early winter. The name also refers to Satsuma Province in Japan (now part of Kagoshima Prefecture), where this citrus variety was first developed. These oranges are prized for their convenience as a snack fruit and their nutritional content, being rich in vitamin C and other antioxidants.',
            'pronunciation': '/sætˈsuːmə/',
            'etymology': 'Named after Satsuma Province in Japan, where this variety of mandarin orange was originally cultivated.',
            'memory_tip': 'Think "SAT-SOON-MA" - you can sit down and soon eat this sweet, easy-to-peel orange.',
            'example_sentence': 'The child preferred _____ oranges because they were easy to peel and had no seeds.',
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
        'saturday': {
            'word': 'saturday',
            'definition': 'The seventh and final day of the week in many Western cultures, traditionally a day of rest and leisure activities following the Monday-through-Friday work week. Saturday is named after the Roman god Saturn and has historically been associated with various cultural and religious observances. In Jewish tradition, Saturday corresponds to the Sabbath (Shabbat), a day of rest and spiritual reflection from Friday evening to Saturday evening. For many people, Saturday represents freedom from work obligations and an opportunity for personal activities, family time, recreational pursuits, and social gatherings. The day often serves as a transition between the structured work week and the more relaxed atmosphere of Sunday, making it a popular time for errands, entertainment, and preparation for the week ahead.',
            'pronunciation': '/ˈsætərdeɪ/',
            'etymology': 'From Old English Sæternesdæg, meaning day of Saturn, from Latin Saturni dies, named after the Roman god Saturn.',
            'memory_tip': 'Think "SAT-UR-DAY" - the day you can sit around and relax after the work week.',
            'example_sentence': 'Every _____ morning, the family enjoyed a leisurely breakfast together.',
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
        'saturn': {
            'word': 'saturn',
            'definition': 'The sixth planet from the Sun in our solar system, famous for its prominent ring system composed of ice particles and rocky debris. Saturn is a gas giant composed primarily of hydrogen and helium, with a density lower than water, making it unique among the planets. The planet has at least 146 known moons, including Titan, which has a thick atmosphere and liquid methane lakes. Saturn\'s rings, while not unique among gas giants, are the most visible and spectacular when viewed from Earth through telescopes. In Roman mythology, Saturn was the god of agriculture and time, equivalent to the Greek god Cronus. The planet takes approximately 29.5 Earth years to complete one orbit around the Sun and has been known since ancient times due to its visibility to the naked eye.',
            'pronunciation': '/ˈsætərn/',
            'etymology': 'From Latin Saturnus, the Roman god of agriculture and time, equivalent to Greek Kronos.',
            'memory_tip': 'Think of the "SAT-URN" with its beautiful rings that you can see when you sit with a telescope.',
            'example_sentence': 'Through the telescope, we could clearly see the magnificent rings surrounding _____.',
            'part_of_speech': 'noun (proper)',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'saturnine': {
            'word': 'saturnine',
            'definition': 'Having a gloomy, morose, or melancholy temperament; characterized by a slow, deliberate, and often pessimistic disposition. The term describes individuals who appear perpetually serious, reserved, and somewhat brooding in their demeanor. Saturnine personalities often exhibit introspective tendencies, preferring solitude and deep contemplation over social interaction and lighthearted activities. In historical contexts, this temperament was associated with the astrological influence of the planet Saturn, believed to produce individuals with serious, methodical, and sometimes depressed dispositions. The word can also describe situations, atmospheres, or artistic works that convey a sense of heaviness, solemnity, or subdued emotional tone. Literary characters described as saturnine often serve as contemplative figures who provide philosophical depth or represent the weight of experience and wisdom.',
            'pronunciation': '/ˈsætərnaɪn/',
            'etymology': 'From Latin saturninus, relating to the god Saturn, who was associated with melancholy and slow, deliberate characteristics in astrological tradition.',
            'memory_tip': 'Think "SATURN-INE" - like the slow, distant planet Saturn, people with this temperament are distant and slow to warm up.',
            'example_sentence': 'His _____ expression rarely changed, even during the most joyful celebrations.',
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
        'sauce': {
            'word': 'sauce',
            'definition': 'A liquid or semi-liquid mixture served with food to enhance flavor, add moisture, or provide complementary tastes and textures. Sauces range from simple preparations like melted butter or olive oil to complex reductions involving multiple ingredients, herbs, and cooking techniques. Classic sauce categories include mother sauces in French cuisine (béchamel, velouté, espagnole, hollandaise, and tomato), each serving as a base for numerous derivative sauces. The preparation and mastery of sauces is considered fundamental to culinary arts, with proper sauce-making requiring understanding of emulsification, reduction, thickening agents, and flavor balance. Beyond culinary applications, "sauce" can colloquially refer to alcohol or to something that adds excitement or interest to a situation.',
            'pronunciation': '/sɔːs/',
            'etymology': 'From Old French sauce, from Latin salsa meaning salted, from sal meaning salt.',
            'memory_tip': 'Think of "SALT-ce" - originally sauces were ways to add salt and flavor to bland foods.',
            'example_sentence': 'The chef prepared a rich mushroom _____ to accompany the grilled steak.',
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
        'saucer': {
            'word': 'saucer',
            'definition': 'A small, shallow dish designed to hold a cup, typically used for serving tea or coffee and catching any liquid that might spill or drip from the cup. Traditional saucers are round with a slight indentation in the center to cradle the cup and a raised rim to contain spills. The combination of cup and saucer forms a classic table setting element that has been standard in formal dining and tea service for centuries. Saucers also serve practical purposes such as providing a place to rest a spoon and protecting table surfaces from heat and moisture. The term can also refer to any shallow, round dish used for various purposes, or colloquially to describe flying saucers (UFOs) due to their resemblance to the round, flat shape of a traditional saucer.',
            'pronunciation': '/ˈsɔːsər/',
            'etymology': 'From Old French saussier, meaning a container for sauce, from sauce + -ier (vessel suffix).',
            'memory_tip': 'Think "SAUCE-ER" - originally a small dish for holding sauce, now paired with cups.',
            'example_sentence': 'She carefully placed the delicate china cup back on its matching _____.',
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
        'sauerkraut': {
            'word': 'sauerkraut',
            'definition': 'Fermented cabbage prepared by finely shredding fresh cabbage and fermenting it with salt, creating a tangy, sour-tasting preserved vegetable. The fermentation process involves beneficial lactic acid bacteria that naturally occur on cabbage leaves, which convert sugars into lactic acid, creating the characteristic sour flavor and preserving the cabbage. Sauerkraut is rich in probiotics, vitamin C, and fiber, making it both nutritious and beneficial for digestive health. This traditional food preservation method originated in Central and Eastern Europe and became particularly associated with German cuisine. The fermentation process can take several weeks and requires proper temperature and salinity conditions to ensure safe preservation while developing the desired flavor profile.',
            'pronunciation': '/ˈsaʊərkraʊt/',
            'etymology': 'From German Sauerkraut, literally meaning "sour cabbage," from sauer (sour) + Kraut (cabbage or herb).',
            'memory_tip': 'Think "SOUR-KRAUT" - German for sour cabbage, which describes exactly what this fermented food is.',
            'example_sentence': 'The traditional German meal included bratwurst served with a side of tangy _____.',
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
        'sauger': {
            'word': 'sauger',
            'definition': 'A freshwater fish species (Sander canadensis) belonging to the perch family, closely related to the walleye but smaller in size and distinguished by distinct markings and habitat preferences. Saugers typically have dark blotches or saddle-like markings across their backs and sides, unlike the more uniform coloration of walleyes. These fish inhabit large rivers and reservoirs throughout much of North America, preferring areas with moderate to strong currents and rocky or sandy bottoms. Saugers are valued by anglers for their fighting ability and excellent taste, though they generally don\'t grow as large as walleyes. They are important both ecologically as predators in river ecosystems and economically as a recreational and commercial fishing target. The species is sensitive to water quality and habitat changes, making it an indicator species for river health.',
            'pronunciation': '/ˈsɔːɡər/',
            'etymology': 'Origin uncertain, possibly from an American Indian language or from a French-Canadian dialect term.',
            'memory_tip': 'Think "SAW-GER" - a fish you might catch with a rod while sitting on a saw log by the river.',
            'example_sentence': 'The angler was excited to catch a _____ from the swift-flowing section of the river.',
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
        'sauna': {
            'word': 'sauna',
            'definition': 'A traditional Finnish bathing facility consisting of a heated room designed for relaxation, cleansing, and health benefits through exposure to dry or wet heat. Traditional saunas use wood-burning stoves to heat the air to temperatures between 70-100°C (158-212°F), while modern versions may use electric heaters or infrared technology. The practice involves sitting in the heated room, often on wooden benches arranged at different levels to accommodate various temperature preferences, with optional water poured over heated stones to create steam. Sauna bathing is followed by cooling off through cold showers, swimming, or rolling in snow, then repeating the cycle. This practice is believed to provide numerous health benefits including improved circulation, stress relief, muscle relaxation, and cardiovascular conditioning.',
            'pronunciation': '/ˈsaʊnə/',
            'etymology': 'From Finnish sauna, originally meaning a type of underground dwelling or earth lodge.',
            'memory_tip': 'Think "SAW-NA" - you saw people in Finland relaxing in these hot wooden rooms.',
            'example_sentence': 'After the skiing trip, we relaxed our sore muscles in the hotel\'s traditional Finnish _____.',
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
        'sausage': {
            'word': 'sausage',
            'definition': 'A cylindrical meat product made from ground meat, typically pork, beef, or poultry, mixed with seasonings and stuffed into a casing made from animal intestines or synthetic materials. Sausages come in numerous varieties reflecting different cultural traditions, spice combinations, preservation methods, and preparation techniques. They can be fresh (requiring cooking before eating), cured (preserved through smoking, drying, or salting), or cooked (ready to eat). Popular types include bratwurst, chorizo, kielbasa, salami, and breakfast sausages. The sausage-making process involves grinding meat to specific textures, mixing with spices and other ingredients, and stuffing the mixture into casings. This ancient food preservation technique allows for long-term storage while creating distinctive flavors through various curing and smoking processes.',
            'pronunciation': '/ˈsɔːsɪdʒ/',
            'etymology': 'From Old French saussiche, from Latin salsicia meaning seasoned with salt, from sal meaning salt.',
            'memory_tip': 'Think "SALT-AGE" - originally sausages were meat preserved with salt through the ages.',
            'example_sentence': 'The butcher explained how traditional Italian _____ is made using family recipes passed down for generations.',
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
        'savoir': {
            'word': 'savoir',
            'definition': 'A French term meaning "to know" in the sense of knowledge, skill, or expertise, often used in English in compound expressions like "savoir-faire" (knowing how to do things properly or tactfully) or "savoir-vivre" (knowing how to live well or proper social conduct). The word represents sophisticated knowledge that goes beyond mere facts to include practical wisdom, social skills, and cultural understanding. In French, savoir specifically refers to factual knowledge or learned information, as distinguished from connaître, which means to be familiar with or acquainted with something or someone. English speakers sometimes use "savoir" alone to suggest a refined, worldly kind of knowledge or sophistication, particularly in contexts involving French culture, cuisine, or social graces.',
            'pronunciation': '/sævˈwɑːr/',
            'etymology': 'From Latin sapere meaning to taste, to be wise, or to know, which also gives us words like sage and sapient.',
            'memory_tip': 'Think "SAV-WAR" - to save yourself from social warfare, you need this kind of sophisticated knowledge.',
            'example_sentence': 'Her elegant _____ was evident in how gracefully she handled the diplomatic crisis.',
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
        'savor': {
            'word': 'savor',
            'definition': 'To enjoy or appreciate something fully, especially food or drink, by taking time to experience its taste, smell, or other qualities completely. The act of savoring involves deliberate attention to sensory experiences, whether culinary, aesthetic, or emotional, rather than consuming or experiencing something quickly or carelessly. In culinary contexts, savoring means tasting food slowly and mindfully to appreciate its flavors, textures, and aromas. More broadly, to savor means to derive pleasure from any experience by being fully present and engaged with it. The word can also function as a noun, referring to a distinctive taste or smell, particularly one that is pleasant or appealing. Savoring represents a mindful approach to experience that emphasizes quality over quantity.',
            'pronunciation': '/ˈseɪvər/',
            'etymology': 'From Old French saveur meaning taste or flavor, from Latin sapor, from sapere meaning to taste.',
            'memory_tip': 'Think "SAVE-OR" - save the moment or save time to really taste and appreciate something.',
            'example_sentence': 'She wanted to _____ every bite of the exquisite chocolate dessert.',
            'part_of_speech': 'verb/noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'savour': {
            'word': 'savour',
            'definition': 'The British spelling of "savor," meaning to enjoy or appreciate something fully, especially food or drink, by taking time to experience its taste, smell, or other qualities completely. This spelling is standard in British English, Canadian English, and other Commonwealth varieties of English. The meaning remains identical to the American spelling: to taste or enjoy something slowly and deliberately, or to appreciate any experience by being fully present and engaged with it. As a noun, savour refers to a distinctive taste, smell, or quality that characterizes something. The British spelling reflects the tendency in British English to retain certain French-influenced spellings that American English has simplified.',
            'pronunciation': '/ˈseɪvər/',
            'etymology': 'From Old French saveur meaning taste or flavor, from Latin sapor, from sapere meaning to taste.',
            'memory_tip': 'British spelling adds "u" like "colour" and "flavour" - think of the "u" as standing for "UK".',
            'example_sentence': 'The British chef advised guests to _____ the wine slowly to appreciate its complex notes.',
            'part_of_speech': 'verb/noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'savvy': {
            'word': 'savvy',
            'definition': 'Practical knowledge, understanding, or intelligence, especially in business or political matters; the ability to understand situations quickly and make good decisions. Someone who is savvy demonstrates shrewd awareness of how things work in the real world, often in specific contexts like "tech-savvy" or "business-savvy." The term implies a combination of knowledge, experience, and intuitive understanding that enables effective navigation of complex situations. As an adjective, savvy describes someone who is knowledgeable and experienced in practical matters. The word often suggests streetwise intelligence or sophisticated understanding gained through experience rather than formal education. Savvy individuals are typically good at reading situations, understanding motives, and making strategic decisions.',
            'pronunciation': '/ˈsævi/',
            'etymology': 'From Spanish sabe meaning he knows, from saber meaning to know, ultimately from Latin sapere meaning to be wise.',
            'memory_tip': 'Think "SAV-VY" - someone who can save the day because they\'re very wise and experienced.',
            'example_sentence': 'Her political _____ helped her navigate the complex negotiations successfully.',
            'part_of_speech': 'noun/adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'sawan': {
            'word': 'sawan',
            'definition': 'The fifth month of the Hindu lunar calendar, corresponding roughly to July-August in the Gregorian calendar, considered one of the most sacred months in Hinduism. Sawan is particularly devoted to Lord Shiva worship, with many devotees observing fasts, especially on Mondays (Sawan Somwar), and making pilgrimages to Shiva temples. The month is marked by the monsoon season in India, making it symbolically associated with renewal, fertility, and spiritual cleansing. Special festivals and rituals are performed during Sawan, including Raksha Bandhan, which celebrates the bond between brothers and sisters. The month is considered highly auspicious for spiritual practices, meditation, and seeking blessings from deities. Many Hindu families observe specific dietary restrictions and engage in charitable activities during this holy period.',
            'pronunciation': '/sɑːˈwɑːn/',
            'etymology': 'From Sanskrit श्रावण (śrāvaṇa), named after the Shravana constellation, from श्रवण (śravaṇa) meaning hearing or listening.',
            'memory_tip': 'Think "SAW-ONE" - you saw the one holy month when devotees focus intensely on spiritual practices.',
            'example_sentence': 'During _____, the temple was filled with devotees offering prayers and conducting special rituals.',
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
        'sawdust': {
            'word': 'sawdust',
            'definition': 'Fine particles and small pieces of wood created as a byproduct when wood is cut, sawed, or machined. Sawdust consists of tiny wood fibers and chips that result from the friction and cutting action of saw blades, planers, sanders, and other woodworking tools. This material has numerous practical applications including use as absorbent material for spills, bedding for animals, material for particleboard manufacturing, fuel for biomass energy, and filler in various products. In workshops and lumber mills, sawdust collection is important for both cleanliness and safety, as accumulated sawdust can pose fire hazards and respiratory health risks. The texture and size of sawdust varies depending on the type of cutting tool used and the species of wood being processed.',
            'pronunciation': '/ˈsɔːdʌst/',
            'etymology': 'Compound word from saw + dust, literally meaning the dust created by sawing wood.',
            'memory_tip': 'Think "SAW-DUST" - the dusty particles left behind when you saw wood.',
            'example_sentence': 'The carpenter swept up the _____ from the workshop floor after completing the cabinet project.',
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
        'says': {
            'word': 'says',
            'definition': 'Third-person singular present tense of the verb "say," meaning to express something in words, to speak, or to state. This common verb form is used when referring to what someone else expresses, communicates, or declares in speech or writing. The word can introduce direct quotations, report someone\'s statements, or describe the act of verbal communication. In writing, "says" is frequently used in dialogue tags and reported speech to attribute statements to specific speakers. The pronunciation of "says" is irregular compared to its spelling, sounding like "sez" rather than following the pattern of words like "days" or "ways." This irregularity makes it a commonly misspelled word despite its frequent use in everyday communication.',
            'pronunciation': '/sɛz/',
            'etymology': 'From Old English secgan meaning to speak or tell, related to German sagen meaning to say.',
            'memory_tip': 'Remember it sounds like "SEZ" not "SAZE" - the pronunciation doesn\'t match the spelling pattern.',
            'example_sentence': 'The weather forecast _____ it will rain tomorrow afternoon.',
            'part_of_speech': 'verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'sbrinz': {
            'word': 'sbrinz',
            'definition': 'A traditional Swiss hard cheese made from cow\'s milk, similar to Parmesan but with its own distinctive characteristics and protected designation of origin status. Sbrinz is produced in specific regions of central Switzerland using traditional methods that have been practiced for centuries. The cheese undergoes an extensive aging process of at least 16 months, often much longer, developing a hard, granular texture and intensely savory, nutty flavor. Like Parmigiano-Reggiano, Sbrinz is excellent for grating over dishes or eating in small pieces as a table cheese. The production follows strict regulations regarding milk source, production methods, and aging requirements to maintain the authentic quality and characteristics that have made this cheese prized since medieval times. It represents one of Switzerland\'s most important traditional dairy products.',
            'pronunciation': '/sbrɪnts/',
            'etymology': 'From Swiss German, possibly related to a place name or traditional cheese-making term in central Switzerland.',
            'memory_tip': 'Think "S-BRINGS" - Switzerland brings us this ancient hard cheese similar to Parmesan.',
            'example_sentence': 'The chef grated aged _____ over the risotto to add a distinctly Swiss flavor.',
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
        'sbrinzkathakali': {
            'word': 'sbrinzkathakali',
            'definition': '[COMBINED WORD ERROR] This appears to be two unrelated words combined: "sbrinz" (a Swiss hard cheese) and "kathakali" (a traditional Indian classical dance-drama form from Kerala). This combination likely resulted from a data processing error where two separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words with their individual cultural and linguistic contexts.',
            'pronunciation': '/sbrɪntskʌθʌˈkɑːli/',
            'etymology': 'Error combination of Swiss German sbrinz (cheese) + Malayalam kathakali (classical dance)',
            'memory_tip': 'This is a combined word error - look for the separation between sbrinz and kathakali.',
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
        'scabbard': {
            'word': 'scabbard',
            'definition': 'A protective sheath or case designed to hold and cover a sword, dagger, or other bladed weapon when not in use. Scabbards serve multiple functions: protecting the blade from damage and corrosion, preventing accidental injury, and providing a convenient way to carry the weapon. They are typically made from leather, wood, metal, or combinations of these materials, often decorated according to the owner\'s status or cultural traditions. Historical scabbards were essential military equipment, designed to be worn on belts or attached to armor systems. The construction of a scabbard requires precise fitting to the specific weapon, with internal linings to prevent blade damage and external fittings for secure attachment to carrying systems. Fine scabbards were often works of art, featuring intricate metalwork, jewels, or carved decorations.',
            'pronunciation': '/ˈskæbərd/',
            'etymology': 'From Anglo-Norman escalberc, possibly from Germanic words meaning "to cut" and "to protect."',
            'memory_tip': 'Think "SCAB-BARD" - like a scab protects a wound, a scabbard protects a sword blade.',
            'example_sentence': 'The knight carefully slid his sword into its ornate leather _____.',
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
        'scaberulous': {
            'word': 'scaberulous',
            'definition': 'In botanical terminology, describing a surface that is slightly rough or minutely scabrous, having small raised points or tiny bumps that create a gritty or sandpaper-like texture when touched. This term is used specifically in plant morphology to describe leaves, stems, or other plant parts that feel slightly rough due to microscopic projections, short hairs, or small tubercles on the surface. The roughness is typically subtle, requiring close examination or touch to detect, and is less pronounced than surfaces described as simply "scabrous." Scaberulous surfaces often serve protective functions for plants, such as reducing water loss or deterring herbivores. This precise botanical descriptor helps scientists and horticulturists accurately communicate the tactile characteristics of plant specimens.',
            'pronunciation': '/skəˈbɛrʊləs/',
            'etymology': 'From Latin scaber meaning rough + -ulous (diminutive suffix), literally meaning "slightly rough."',
            'memory_tip': 'Think "SCAB-ERULOUS" - slightly rough like a small scab, but not severely rough.',
            'example_sentence': 'The botanist noted that the leaf surface was _____, feeling slightly gritty to the touch.',
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
        'scagliola': {
            'word': 'scagliola',
            'definition': 'A decorative plaster technique that imitates marble or other decorative stones through the use of finely ground gypsum, glue, and pigments applied in multiple layers and polished to achieve a marble-like appearance. This Italian art form, developed during the 17th century, allows artisans to create elaborate architectural details, columns, and decorative elements that convincingly replicate expensive natural stones at a fraction of the cost. The process involves applying successive coats of specially prepared plaster, each containing different colored materials to create veining and patterns characteristic of various types of marble. After drying, the surface is carefully polished to achieve the smooth, lustrous finish typical of natural stone. Scagliola work can be found in historic palaces, churches, and important buildings throughout Europe, representing a sophisticated craft that required considerable skill and artistic ability.',
            'pronunciation': '/skælˈjoʊlə/',
            'etymology': 'From Italian scagliola, diminutive of scaglia meaning scale or chip, referring to the scaly appearance of gypsum.',
            'memory_tip': 'Think "SCALE-IOLA" - using scales or chips of material to create fake marble.',
            'example_sentence': 'The palace columns were actually made of _____, not genuine marble, though few visitors could tell the difference.',
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
        'scale': {
            'word': 'scale',
            'definition': 'A graduated range of values, measurements, or degrees used for comparison, measurement, or classification purposes. In various contexts, scale can refer to the size or extent of something relative to other things, a system of numerical measurement, or the ratio between distances on a map and actual distances. Musical scales consist of sequences of notes arranged in ascending or descending order according to pitch relationships. In biology, scales are small, flat, overlapping plates that cover the skin of fish and reptiles for protection. Weight scales are instruments for measuring mass or weight. The concept of scale is fundamental in mathematics, science, engineering, and many practical applications where proportion, measurement, and comparison are important.',
            'pronunciation': '/skeɪl/',
            'etymology': 'From Latin scala meaning ladder or staircase, referring to graduated steps or levels.',
            'memory_tip': 'Think of climbing a "SCALE" like a ladder - each step represents a measured level or degree.',
            'example_sentence': 'The earthquake measured 7.2 on the Richter _____.',
            'part_of_speech': 'noun/verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scallion': {
            'word': 'scallion',
            'definition': 'A young onion harvested before the bulb has fully developed, characterized by long green tops and a small white or light-colored base, also known as green onions or spring onions. Scallions have a milder flavor than mature onions, with both the white base and green tops being edible and commonly used in cooking. The white portion provides a sharper onion flavor, while the green tops offer a more delicate taste similar to chives. These vegetables are popular in many cuisines, particularly Asian cooking, where they are used as garnishes, in stir-fries, soups, and salads. Scallions can be eaten raw or cooked and are valued for their ability to add onion flavor without the intensity of full-sized bulbs. They are easy to grow and can be harvested multiple times from the same plant.',
            'pronunciation': '/ˈskæljən/',
            'etymology': 'From Anglo-Norman escaloun, from Latin Ascalonia meaning "from Ashkelon," a city in ancient Palestine associated with onions.',
            'memory_tip': 'Think "SCALE-ION" - these are small-scale onions harvested before they fully develop.',
            'example_sentence': 'The chef garnished the soup with finely chopped _____ for added color and flavor.',
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
        'scalp': {
            'word': 'scalp',
            'definition': 'The skin covering the top and back of the human head, typically covered with hair, extending from the forehead to the base of the skull and from ear to ear. The scalp consists of five layers: skin, connective tissue, aponeurosis (a tough fibrous sheet), loose connective tissue, and periosteum (membrane covering the skull). This area contains numerous hair follicles, sebaceous glands, and blood vessels that nourish hair growth. In historical contexts, "scalp" also refers to the practice of removing part of the scalp as a trophy, which occurred in various cultures during warfare. In trading contexts, to scalp means to buy and quickly resell items (like tickets) at inflated prices, or in financial markets, to make small profits from rapid trades.',
            'pronunciation': '/skælp/',
            'etymology': 'From Middle English, possibly from Old Norse skálpr meaning sheath or scabbard.',
            'memory_tip': 'Think "SCALE-P" - the scalp has multiple layers like scales protecting the skull.',
            'example_sentence': 'The dermatologist examined her _____ to determine the cause of the persistent itching.',
            'part_of_speech': 'noun/verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scalpscrapple': {
            'word': 'scalpscrapple',
            'definition': '[COMBINED WORD ERROR] This appears to be two unrelated words combined: "scalp" (the skin covering the head) and "scrapple" (a Pennsylvania Dutch dish made from pork scraps and cornmeal). This combination likely resulted from a data processing error where two separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words with their individual meanings and contexts.',
            'pronunciation': '/skælpˈskræpəl/',
            'etymology': 'Error combination of Middle English scalp + scrapple (from scrap + -le)',
            'memory_tip': 'This is a combined word error - look for the separation between scalp and scrapple.',
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
        'scaly': {
            'word': 'scaly',
            'definition': 'Covered with or resembling scales, or having a surface that flakes off in small pieces. In biological contexts, scaly describes animals like fish, reptiles, and certain birds that have overlapping protective plates covering their skin. In medical contexts, scaly skin refers to conditions where the skin becomes dry and sheds in small flakes, often due to dermatological conditions, dehydration, or environmental factors. The term can also describe any surface that has scale-like patterns or textures, whether natural or artificial. Scaly surfaces often serve protective functions, such as reducing water loss, providing armor-like protection, or helping with movement through certain environments. In casual usage, scaly can refer to anything that appears flaky, rough, or covered with small overlapping pieces.',
            'pronunciation': '/ˈskeɪli/',
            'etymology': 'From scale + -y suffix, meaning having the characteristics of scales.',
            'memory_tip': 'Think "SCALE-Y" - having scales like a fish or lizard, or flaking like scales.',
            'example_sentence': 'The lizard\'s _____ skin provided excellent protection from predators and harsh weather.',
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
        'scan': {
            'word': 'scan',
            'definition': 'To examine something systematically and carefully, often by moving one\'s eyes or a device across the surface or through the contents. In medical contexts, scanning involves using technology like X-rays, MRI, or ultrasound to create images of internal body structures for diagnostic purposes. In technology, scanning refers to converting physical documents or images into digital format using optical devices. The term also applies to quickly looking through written material to locate specific information or get a general understanding of content. In poetry, to scan means to analyze the rhythmic pattern of verses by identifying stressed and unstressed syllables. Security scanning involves checking for threats, whether in computer systems or physical locations.',
            'pronunciation': '/skæn/',
            'etymology': 'From Latin scandere meaning to climb or mount, originally referring to analyzing poetry by climbing through its metrical feet.',
            'memory_tip': 'Think "S-CAN" - you can systematically examine or look through something carefully.',
            'example_sentence': 'The doctor ordered a CT _____ to get a detailed view of the patient\'s internal organs.',
            'part_of_speech': 'verb/noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scandal': {
            'word': 'scandal',
            'definition': 'An action, event, or situation that causes public outrage, shock, or moral indignation due to its perceived impropriety, illegality, or violation of accepted standards of behavior. Scandals typically involve prominent figures or institutions and often receive significant media attention, leading to damaged reputations, loss of public trust, and sometimes legal consequences. The revelation of scandals can trigger investigations, resignations, reforms, or other corrective actions. Political scandals might involve corruption, abuse of power, or personal misconduct, while corporate scandals often center on financial fraud, safety violations, or ethical breaches. The impact of a scandal depends on factors such as the severity of the wrongdoing, the prominence of those involved, and the public\'s reaction to the revelations.',
            'pronunciation': '/ˈskændəl/',
            'etymology': 'From Greek skandalon meaning trap or snare, later meaning stumbling block or cause of offense.',
            'memory_tip': 'Think "SCAN-DAL" - when people scan or examine someone\'s actions, they might discover scandalous behavior.',
            'example_sentence': 'The corruption _____ led to the resignation of several high-ranking government officials.',
            'part_of_speech': 'noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
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
    
    print(f"\nBatch 154 processing complete!")
    print(f"Successfully processed {len(processed_words)}/{len(words)} words")
    print(f"Output saved to: {output_file}")
    
    if combined_errors:
        print(f"\nCombined word errors detected: {len(combined_errors)}")
        for error in combined_errors:
            print(f"  - {error}")

if __name__ == "__main__":
    process_batch()