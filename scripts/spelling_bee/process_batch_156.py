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
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_156_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_156_processed.csv'
    
    calculator = DifficultyCalculator()
    
    word_data = {
        'scramblegames': {
            'word': 'scramblegames',
            'definition': '[COMBINED WORD ERROR] This appears to be two words combined: "scramble" (to move quickly over rough ground or to mix things together in disorder) and "games" (structured activities or competitions played for entertainment). This combination likely resulted from a data processing error where two separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words with their individual meanings and contexts.',
            'pronunciation': '/ˈskræmbəlɡeɪmz/',
            'etymology': 'Error combination of Dutch schrammen (scramble) + Old English gamen (games)',
            'memory_tip': 'This is a combined word error - look for the separation between scramble and games.',
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
        'scrambling': {
            'word': 'scrambling',
            'definition': 'The act of moving quickly and awkwardly over rough or steep terrain, often using both hands and feet for support and balance. In mountaineering and hiking, scrambling describes terrain that is more challenging than walking but easier than technical rock climbing, typically requiring the use of hands for balance but not specialized climbing equipment. The term also refers to mixing or jumbling things together in a disorderly fashion, or to competing eagerly with others for something limited or valuable. In communications and cryptography, scrambling involves encoding signals or information to prevent unauthorized access. Emergency scrambling describes rapid mobilization of resources or personnel in response to urgent situations. The activity requires agility, balance, and confidence in navigating uncertain terrain.',
            'pronunciation': '/ˈskræmblɪŋ/',
            'etymology': 'From scramble + -ing suffix, where scramble possibly comes from dialectal scamble meaning to struggle for something.',
            'memory_tip': 'Think "SCRAM-BLING" - moving so fast over rough ground that you almost scram (run away quickly).',
            'example_sentence': 'The hikers found themselves _____ over loose rocks to reach the mountain peak.',
            'part_of_speech': 'verb (present participle)/noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scrape': {
            'word': 'scrape',
            'definition': 'To rub or drag a hard or sharp implement across a surface so as to remove dirt, food, paint, or other unwanted matter. Scraping involves applying pressure while moving an object across a surface to achieve cleaning, smoothing, or material removal. The action can be performed with various tools including knives, scrapers, sandpaper, or fingernails. In medical contexts, scraping might refer to minor injuries where skin is abraded against rough surfaces, or to medical procedures like cervical scrapes for testing. The term can also describe barely managing to achieve something, as in "scraping by" financially, or making harsh, grating sounds. Scraping is fundamental to many maintenance, construction, and artistic processes.',
            'pronunciation': '/skreɪp/',
            'etymology': 'From Old Norse skrapa meaning to scrape or scratch, related to Dutch schrapen.',
            'memory_tip': 'Think "SCAPE" - you scrape to escape unwanted material from surfaces.',
            'example_sentence': 'She had to _____ the old paint off the window frame before applying the new coat.',
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
        'scrapple': {
            'word': 'scrapple',
            'definition': 'A traditional Pennsylvania Dutch dish made from pork scraps, cornmeal, and spices, formed into a loaf, sliced, and fried until crispy on the outside. This breakfast food originated as a way to use every part of the pig during butchering, combining leftover pork pieces with cornmeal to create a filling, economical meal. The mixture is seasoned with sage, pepper, and other spices, then cooked into a thick mush that solidifies when cooled. Scrapple is typically served sliced and pan-fried until golden brown and crispy, often accompanied by syrup, applesauce, or ketchup. While primarily associated with Pennsylvania and surrounding Mid-Atlantic regions, scrapple represents the resourceful cooking traditions of German immigrants who settled in America.',
            'pronunciation': '/ˈskræpəl/',
            'etymology': 'From scrap + -le diminutive suffix, literally meaning "little scraps" referring to leftover pork pieces.',
            'memory_tip': 'Think "SCRAP-LE" - made from little scraps of pork mixed with cornmeal.',
            'example_sentence': 'The Pennsylvania diner served traditional _____ alongside eggs and hash browns for breakfast.',
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
        'scrawny': {
            'word': 'scrawny',
            'definition': 'Extremely thin and bony, typically in an unattractive or unhealthy way; lacking sufficient flesh or muscle mass to appear robust or well-nourished. The term describes a physical appearance characterized by protruding bones, visible ribs, and an overall gaunt or emaciated look. Scrawny can apply to people, animals, or even plants that appear undernourished, underdeveloped, or weakened by poor conditions. Unlike simply being slender or lean, scrawny implies an unhealthy thinness that suggests inadequate nutrition, illness, or poor care. The word often carries negative connotations, suggesting weakness, frailty, or neglect. In some contexts, it might describe someone who is naturally very thin but appears healthy, though the term generally implies an undesirable level of thinness.',
            'pronunciation': '/ˈskrɔːni/',
            'etymology': 'Origin uncertain, possibly related to dialectal scrawn meaning to make thin, or from Scandinavian roots meaning shriveled.',
            'memory_tip': 'Think "SCRAWL-NY" - so thin that their body looks like a scrawled (thin) line drawing.',
            'example_sentence': 'The stray cat was _____ from weeks of not finding enough food to eat.',
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
        'scream': {
            'word': 'scream',
            'definition': 'A loud, piercing cry expressing intense emotion such as fear, pain, excitement, or anger, typically produced by forcing air through the vocal cords at high volume and pitch. Screaming represents one of the most primitive and universal human expressions, serving as both an alarm signal and emotional release. The physiological act involves rapid, forceful exhalation while tensing throat muscles to create the characteristic high-pitched, penetrating sound. Screams can communicate immediate danger, summon help, or express overwhelming emotions when words are inadequate. In entertainment contexts, screaming appears in horror films, concerts, and sporting events. The term can also describe anything that demands immediate attention or seems glaringly obvious, as in "screaming headlines" or colors that "scream" for attention.',
            'pronunciation': '/skriːm/',
            'etymology': 'From Middle English scremen, possibly imitative of the sound, or related to Old Norse skrækja meaning to screech.',
            'memory_tip': 'Think "SCREAM" - the word itself sounds sharp and piercing like the sound it describes.',
            'example_sentence': 'The horror movie made her _____ so loudly that the neighbors called to check on her.',
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
        'scree': {
            'word': 'scree',
            'definition': 'A mass of loose rock debris that accumulates on steep mountain slopes, typically consisting of small stones and rock fragments that have broken off from cliff faces or exposed rock formations due to weathering, frost action, and gravitational forces. Scree slopes are common in mountainous regions and present particular challenges for hikers and climbers due to their instability and tendency to shift underfoot. The loose material can range in size from small pebbles to larger boulders, and walking on scree requires special techniques to maintain balance and prevent dangerous slides. Scree formation is an important part of erosional processes that gradually break down mountain faces. The term is also used in geology to describe similar accumulations of loose rock material in various environments.',
            'pronunciation': '/skriː/',
            'etymology': 'From Old Norse skriða meaning landslide or scree, related to the verb meaning to slide or glide.',
            'memory_tip': 'Think "SCREE" sounds like "SPREE" - loose rocks on a sliding spree down the mountain.',
            'example_sentence': 'The mountain climbers carefully navigated the unstable _____ slope to avoid triggering a rockslide.',
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
        'screeno': {
            'word': 'screeno',
            'definition': 'A form of bingo played in movie theaters during the 1930s and 1940s, where audience members would receive game cards and play along with numbers called out between film showings or during intermissions. This entertainment format combined the appeal of cinema with the excitement of gambling, helping theater owners attract customers during the economically challenging Depression era. Players would mark their cards as numbers were announced, with winners receiving cash prizes or merchandise. Screeno represented an innovative way to increase theater attendance and revenue while providing additional entertainment value. The practice eventually declined as movie-going habits changed and other forms of entertainment became more popular. The name combines "screen" (referring to movie screens) with the "o" ending from "bingo."',
            'pronunciation': '/ˈskriːnoʊ/',
            'etymology': 'Combination of screen (movie screen) + -o ending from bingo, created in the 1930s for theater bingo games.',
            'memory_tip': 'Think "SCREEN-O" - bingo played at movie screens during the golden age of cinema.',
            'example_sentence': 'The old theater owner remembered when _____ nights brought packed houses during the Great Depression.',
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
        'scribbly': {
            'word': 'scribbly',
            'definition': 'Characterized by hasty, careless, or illegible handwriting; marked by scrawled marks that are difficult to read or understand. Scribbly writing typically features irregular letter formation, inconsistent spacing, and overall poor legibility resulting from speed, lack of care, or poor penmanship skills. The term can also describe drawings, notes, or marks that appear messy, hastily done, or lacking in precision. In some contexts, scribbly might refer to the natural patterns found on certain tree barks where insect larvae have created winding, maze-like tracks that resemble careless handwriting. The word suggests a lack of neatness or formality, often associated with quick note-taking, rough drafts, or casual jottings.',
            'pronunciation': '/ˈskrɪbli/',
            'etymology': 'From scribble + -y suffix, where scribble comes from Latin scribere meaning to write.',
            'memory_tip': 'Think "SCRIB-BLY" - writing that\'s so scribbly it\'s barely readable.',
            'example_sentence': 'The doctor\'s _____ handwriting on the prescription was nearly impossible for the pharmacist to decipher.',
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
        'scrimshaw': {
            'word': 'scrimshaw',
            'definition': 'The art of decorating whale bone, whale teeth, walrus tusks, or other marine ivory with intricate engravings, typically practiced by sailors and whalers during long voyages in the 18th and 19th centuries. Scrimshaw involves carving detailed designs, scenes, or pictures into the hard surface using sharp tools, then rubbing ink or other coloring materials into the grooves to make the images visible. Common subjects included whaling scenes, ships, portraits, patriotic symbols, and decorative patterns. This folk art form developed as both a way to pass time during lengthy sea voyages and as a means to create gifts or trade goods. Authentic antique scrimshaw is now highly valued by collectors, though modern artists continue the tradition using alternative materials due to restrictions on marine mammal products.',
            'pronunciation': '/ˈskrɪmʃɔː/',
            'etymology': 'Origin uncertain, possibly from Dutch schrim scham meaning to make a shift, or from the names of tools used in the process.',
            'memory_tip': 'Think "SCRIM-SHAW" - sailors would scrim (scrape) and saw into whale bone to create art.',
            'example_sentence': 'The maritime museum displayed an extensive collection of 19th-century _____ featuring detailed whaling scenes.',
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
        'scripture': {
            'word': 'scripture',
            'definition': 'Sacred writings or texts that are regarded as divinely inspired and authoritative within religious traditions, serving as fundamental sources of spiritual guidance, moral instruction, and religious doctrine. Different religions have their own scriptural texts, such as the Bible in Christianity, the Torah in Judaism, the Quran in Islam, the Vedas in Hinduism, and the Tripitaka in Buddhism. These texts are typically considered to contain divine revelation, historical accounts of religious figures and events, moral teachings, and guidelines for proper conduct and spiritual practice. Scripture study forms a central part of religious education and worship in most faiths. The interpretation and understanding of scriptural passages often require scholarly study and may involve consideration of historical, cultural, and linguistic contexts.',
            'pronunciation': '/ˈskrɪptʃər/',
            'etymology': 'From Latin scriptura meaning writing, from scribere meaning to write.',
            'memory_tip': 'Think "SCRIPT-URE" - sacred scripts that provide the foundation for religious belief and practice.',
            'example_sentence': 'The comparative religion class examined how different faiths interpret their sacred _____.',
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
        'scrivener': {
            'word': 'scrivener',
            'definition': 'A professional copyist or clerk who writes documents by hand, particularly in historical periods before the widespread use of printing and typewriting. Scriveners played crucial roles in medieval and early modern societies by preparing legal documents, contracts, letters, and official records with careful attention to legibility and accuracy. They were skilled in various forms of handwriting, legal terminology, and document formatting. Some scriveners also served as notaries public, witnessing signatures and certifying documents. The profession required literacy at a time when many people could not read or write, making scriveners important intermediaries in legal and business transactions. Famous literary scriveners include the character Bartleby in Herman Melville\'s story and various historical figures who maintained important records and correspondence.',
            'pronunciation': '/ˈskrɪvnər/',
            'etymology': 'From Latin scribere meaning to write + -ener suffix indicating one who performs an action.',
            'memory_tip': 'Think "SCRIVE-NER" - one who scribes or writes documents professionally.',
            'example_sentence': 'The medieval _____ carefully copied the important legal charter using elaborate calligraphy.',
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
        'scrofula': {
            'word': 'scrofula',
            'definition': 'A historical medical term for tuberculosis affecting the lymph nodes, particularly those in the neck, characterized by chronic swelling, inflammation, and often the formation of abscesses or open sores. Also known as the "king\'s evil" because it was once believed that royal touch could cure the condition, scrofula was a common manifestation of tuberculosis before the advent of modern antibiotics. The disease typically affects children and young adults, causing enlarged, sometimes painful lymph nodes that may eventually ulcerate and drain. Scrofula was often associated with poor nutrition, crowded living conditions, and overall poor health. Modern medicine understands scrofula as extrapulmonary tuberculosis, and it is now treatable with standard anti-tuberculosis medications when diagnosed properly.',
            'pronunciation': '/ˈskrɒfjʊlə/',
            'etymology': 'From Latin scrofulae meaning swelling of the glands, from scrofa meaning breeding sow, referring to the swollen appearance.',
            'memory_tip': 'Think "SCROF-ULA" - a disease that made lymph nodes scruffy and swollen.',
            'example_sentence': 'Medieval physicians often misdiagnosed _____ and attributed supernatural causes to the lymph node swellings.',
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
        'scroll': {
            'word': 'scroll',
            'definition': 'A roll of parchment, paper, or other material used for writing, typically consisting of a long strip that is rolled up for storage and unrolled for reading. Scrolls were the primary form of book or document before the development of the codex (bound book) format. Ancient scrolls contained literature, religious texts, legal documents, and historical records, with famous examples including the Dead Sea Scrolls and ancient Egyptian papyrus scrolls. The term also refers to decorative architectural or artistic elements that resemble rolled parchment, featuring curved or spiral designs. In computing, scrolling refers to moving through digital content that extends beyond the visible screen area. Modern ceremonial scrolls, such as diplomas or awards, continue the traditional association with important documents and formal recognition.',
            'pronunciation': '/skroʊl/',
            'etymology': 'From Old French escroe meaning strip of parchment, from Germanic roots meaning to cut.',
            'memory_tip': 'Think "S-ROLL" - a document that you roll up like a scroll for storage.',
            'example_sentence': 'The ancient _____ contained philosophical writings that had been preserved for over two thousand years.',
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
        'scrolls': {
            'word': 'scrolls',
            'definition': 'Plural of scroll, referring to multiple rolls of parchment, paper, or other materials used for writing and document storage. Historical collections of scrolls often contained entire libraries of ancient knowledge, religious texts, literature, and administrative records. Famous scroll collections include the Library of Alexandria, the Dead Sea Scrolls, and various monastery libraries that preserved classical and religious texts through medieval periods. Archaeological discoveries of scroll collections have provided invaluable insights into ancient civilizations, languages, and belief systems. In architecture and decorative arts, scrolls refer to multiple curved or spiral ornamental elements. Modern digital interfaces use the concept of scrolling through multiple documents or pages, maintaining the metaphor of unrolling written material to access content.',
            'pronunciation': '/skroʊlz/',
            'etymology': 'Plural of scroll, from Old French escroe meaning strip of parchment.',
            'memory_tip': 'Think "S-ROLLS" - multiple rolled documents, like having several rolls of paper.',
            'example_sentence': 'The monastery library contained hundreds of ancient _____ preserving medieval manuscripts.',
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
        'scrooge': {
            'word': 'scrooge',
            'definition': 'A person who is extremely stingy with money; a miser who hoards wealth and refuses to spend money even on necessities or reasonable comforts. The term derives from Ebenezer Scrooge, the miserly protagonist of Charles Dickens\' "A Christmas Carol," who epitomizes selfishness and penny-pinching behavior. A scrooge typically displays excessive frugality, reluctance to give gifts or help others, and general meanness regarding financial matters. The character has become a cultural archetype representing the dangers of prioritizing wealth accumulation over human relationships and generosity. In modern usage, calling someone a scrooge suggests they are unreasonably cheap, lacking in generosity, or unwilling to spend money on others\' happiness or well-being, particularly during gift-giving seasons or charitable opportunities.',
            'pronunciation': '/skruːdʒ/',
            'etymology': 'From the character Ebenezer Scrooge in Charles Dickens\' 1843 novella "A Christmas Carol."',
            'memory_tip': 'Think of Dickens\' character who was so stingy that his name became synonymous with miserliness.',
            'example_sentence': 'Don\'t be such a _____ - it\'s your daughter\'s birthday and she deserves a nice gift.',
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
        'scrounge': {
            'word': 'scrounge',
            'definition': 'To search for and gather items, food, or resources by rummaging through available materials, often in an opportunistic or somewhat desperate manner. Scrounging implies finding and collecting things that others might consider worthless or discarded, but which serve useful purposes for the scrounger. The activity often involves creativity and resourcefulness in repurposing materials or making do with whatever is available. During economic hardship or resource scarcity, scrounging becomes a survival strategy. The term can also mean to obtain something through persistent asking, begging, or informal requests, as in "scrounging for spare change." While sometimes viewed negatively as associated with poverty or desperation, scrounging can also represent admirable qualities of resourcefulness and waste reduction.',
            'pronunciation': '/skraʊndʒ/',
            'etymology': 'Origin uncertain, possibly related to dialectal scrunge meaning to search or hunt around.',
            'memory_tip': 'Think "SCROUNGE" rhymes with "lounge" - searching around leisurely for useful items.',
            'example_sentence': 'After the storm, residents had to _____ for building materials to repair their damaged homes.',
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
        'scrumptiously': {
            'word': 'scrumptiously',
            'definition': 'In a manner that is extremely delicious, appetizing, or pleasing to taste; with exceptional flavor and appeal that creates strong positive sensory responses. This adverb describes food or drink that is not merely good-tasting but extraordinarily delightful, often evoking expressions of pleasure and satisfaction. Scrumptiously prepared meals typically feature perfect seasoning, ideal texture, and appealing presentation that combine to create memorable dining experiences. The word can extend beyond food to describe anything that provides intense sensory pleasure or satisfaction. When something is described as scrumptiously prepared or presented, it suggests careful attention to quality, flavor balance, and overall appeal that exceeds ordinary expectations and creates genuine delight in those experiencing it.',
            'pronunciation': '/ˈskrʌmpʃəsli/',
            'etymology': 'From scrumptious + -ly suffix, where scrumptious is possibly a variant of sumptuous meaning magnificent.',
            'memory_tip': 'Think "SCRUMP-TIOUSLY" - so deliciously good that you want to scrump (grab) it eagerly.',
            'example_sentence': 'The holiday feast was _____ prepared, with each dish more delicious than the last.',
            'part_of_speech': 'adverb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scruple': {
            'word': 'scruple',
            'definition': 'A moral or ethical principle that restrains action or behavior; a feeling of doubt or hesitation with regard to the morality or propriety of a course of conduct. Scruples represent internal moral constraints that prevent someone from acting in ways they believe to be wrong, even when external consequences are unlikely. Having scruples indicates a strong moral conscience and ethical sensitivity that guides decision-making. People may experience scruples about lying, cheating, hurting others, or violating their personal values. The term also refers to a very small amount or degree, particularly in the phrase "without scruple," meaning without any moral hesitation. Historical medical and pharmaceutical contexts used scruple as a unit of weight. Strong moral scruples are generally viewed as positive character traits indicating integrity and ethical awareness.',
            'pronunciation': '/ˈskruːpəl/',
            'etymology': 'From Latin scrupulus meaning small sharp stone, anxiety, or doubt, from scrupus meaning rough stone.',
            'memory_tip': 'Think of a small stone (scruple) in your shoe that bothers you - like moral doubt that bothers your conscience.',
            'example_sentence': 'She had no _____ about reporting the safety violations to the proper authorities.',
            'part_of_speech': 'noun/verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scrutiny': {
            'word': 'scrutiny',
            'definition': 'Critical observation or examination, especially close and systematic investigation intended to discover facts, evaluate quality, or detect problems. Scrutiny involves careful, detailed analysis that goes beyond casual observation to thoroughly examine all aspects of a subject. This process often occurs in contexts where accuracy, truth, or quality are essential, such as scientific research, legal proceedings, financial auditing, or academic review. Public figures, policies, and institutions frequently come under scrutiny from media, investigators, or oversight bodies. The intensity of scrutiny can vary from routine inspection to intensive investigation prompted by suspicions or concerns. Effective scrutiny requires analytical skills, attention to detail, and often specialized knowledge of the subject being examined. The goal is typically to ensure accountability, accuracy, or proper standards.',
            'pronunciation': '/ˈskruːtəni/',
            'etymology': 'From Latin scrutinium meaning examination, from scrutari meaning to search or examine thoroughly.',
            'memory_tip': 'Think "SCRUT-INY" - examining something so closely you scrutinize every tiny detail.',
            'example_sentence': 'The candidate\'s financial records came under intense _____ during the election campaign.',
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
        'scuffle': {
            'word': 'scuffle',
            'definition': 'A short, confused fight or struggle, typically involving grappling and wrestling rather than systematic combat or organized conflict. Scuffles are usually brief physical altercations characterized by disorganized movement, grabbing, pushing, and general chaos rather than skilled fighting techniques. These conflicts often arise spontaneously from disagreements, frustrations, or competitive situations and typically involve two or more people in close physical contact. The term can also describe any confused struggle or disorderly conflict, whether physical or metaphorical. Scuffles may result in minor injuries, damaged clothing, or disrupted environments, but they generally lack the intensity or duration of serious fights. The word emphasizes the chaotic, uncoordinated nature of the conflict rather than any strategic or skilled combat.',
            'pronunciation': '/ˈskʌfəl/',
            'etymology': 'Probably from Scandinavian origin, related to Swedish skuffa meaning to push.',
            'memory_tip': 'Think "SCUFF-LE" - a fight where people scuff up their shoes from all the shuffling around.',
            'example_sentence': 'The hockey players engaged in a brief _____ after the controversial goal.',
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
        'scullery': {
            'word': 'scullery',
            'definition': 'A small room or area adjacent to a kitchen, traditionally used for washing dishes, preparing vegetables, and performing other messy or labor-intensive culinary tasks. In historical homes, particularly large houses with domestic staff, the scullery served to keep the main kitchen clean and organized by handling the dirtiest work separately. Sculleries typically contained deep sinks, storage for cleaning supplies, and sometimes additional preparation surfaces. The person working in the scullery, often called a scullery maid, held one of the lowest positions in household staff hierarchy. Modern homes sometimes include sculleries or butler\'s pantries that serve similar functions, providing additional workspace and storage while keeping food preparation mess away from main living areas. These spaces remain valuable for serious home cooking and entertaining.',
            'pronunciation': '/ˈskʌləri/',
            'etymology': 'From Old French escuelerie, from escuele meaning bowl or dish, from Latin scutella.',
            'memory_tip': 'Think "SKULL-ERY" - a place where you clean dishes until they\'re as clean as skulls (bones).',
            'example_sentence': 'The Victorian mansion featured a separate _____ where servants cleaned dishes and prepared vegetables.',
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
        'sculling': {
            'word': 'sculling',
            'definition': 'A rowing technique using two oars (called sculls), one in each hand, to propel a boat through water, as opposed to sweep rowing where each rower uses one oar with both hands. In sculling, the rower sits facing the stern and pulls both oars simultaneously in a coordinated rhythm. This technique is used in competitive rowing events, recreational boating, and traditional small boat handling. Sculling boats are typically narrower than sweep boats and require different balance and coordination skills. The term also describes a specific propulsion technique where a single oar is moved back and forth over the stern of a boat in a figure-eight pattern to generate forward motion. Sculling requires precise timing, balance, and upper body strength to maintain efficient boat speed and direction.',
            'pronunciation': '/ˈskʌlɪŋ/',
            'etymology': 'From scull (oar) + -ing suffix, where scull possibly comes from Old Norse skuld meaning obligation or debt.',
            'memory_tip': 'Think "SKULL-ING" - using both hands on oars like holding two skulls to row the boat.',
            'example_sentence': 'She spent hours practicing her _____ technique to improve her timing and boat speed.',
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
        'sculpting': {
            'word': 'sculpting',
            'definition': 'The art and process of creating three-dimensional artwork by shaping, carving, modeling, or assembling materials such as stone, wood, metal, clay, or other substances. Sculpting involves both additive techniques, where material is built up or added to create form, and subtractive techniques, where material is carved away or removed to reveal the desired shape. The process requires artistic vision, technical skill, and understanding of materials and tools. Traditional sculpting materials include marble, bronze, wood, and clay, while contemporary artists may use plastics, found objects, or digital technologies. Sculpting encompasses various styles from realistic representation to abstract expression. The activity demands spatial awareness, planning abilities, and often considerable physical effort. Finished sculptures can range from small figurines to monumental public artworks.',
            'pronunciation': '/ˈskʌlptɪŋ/',
            'etymology': 'From sculpt + -ing suffix, where sculpt comes from Latin sculpere meaning to carve or engrave.',
            'memory_tip': 'Think "SCULPT-ING" - the ongoing process of sculpting or shaping material into art.',
            'example_sentence': 'The artist spent months _____ the marble block into a lifelike representation of a dancer.',
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
        'sculpture': {
            'word': 'sculpture',
            'definition': 'The art of creating three-dimensional works of art by shaping, carving, modeling, or assembling materials, or the finished artwork itself created through this process. Sculpture as an art form encompasses a vast range of techniques, materials, and styles, from ancient stone carvings and bronze castings to contemporary installations using unconventional materials. Traditional sculptural materials include marble, bronze, wood, and clay, while modern sculptors may incorporate plastics, metals, found objects, or digital technologies. Sculptures can be representational, depicting recognizable subjects, or abstract, exploring form, texture, and spatial relationships. The medium allows artists to explore volume, mass, space, and texture in ways unique from two-dimensional art forms. Sculpture serves decorative, commemorative, religious, and artistic purposes across cultures and throughout history.',
            'pronunciation': '/ˈskʌlptʃər/',
            'etymology': 'From Latin sculptura, from sculpere meaning to carve, cut, or engrave.',
            'memory_tip': 'Think "SCULPT-URE" - the result or practice of sculpting three-dimensional art.',
            'example_sentence': 'The museum\'s modern _____ collection featured works ranging from traditional bronze to innovative mixed media installations.',
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
        'scumble': {
            'word': 'scumble',
            'definition': 'A painting technique involving the application of a thin, semi-transparent layer of paint over a dried layer beneath, creating a soft, hazy, or atmospheric effect by allowing the underlying color to show through partially. This technique is used to modify colors, create subtle transitions, soften harsh edges, or add atmospheric depth to paintings. Scumbling differs from glazing in that it typically uses opaque or semi-opaque paint rather than transparent paint, and it often involves rough or broken application rather than smooth, even coverage. Artists may scumble to age surfaces, create texture effects, or blend colors optically rather than physically mixing them on a palette. The technique has been used throughout art history by masters like Rembrandt and Turner to achieve complex color relationships and atmospheric effects.',
            'pronunciation': '/ˈskʌmbəl/',
            'etymology': 'Possibly from scum + -ble suffix, referring to the way the technique creates a scum-like surface effect.',
            'memory_tip': 'Think "SCUM-BLE" - creating a scummy, hazy layer effect by blending paint techniques.',
            'example_sentence': 'The artist used a _____ technique to create the misty atmosphere in the landscape painting.',
            'part_of_speech': 'verb/noun',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scuppers': {
            'word': 'scuppers',
            'definition': 'Drainage openings along the sides of a ship\'s deck that allow water to flow overboard, preventing accumulation that could affect the vessel\'s stability or cause damage. Scuppers are essential safety features that handle rainwater, wave splash, and deck washing by providing clear pathways for water to exit the deck area. They are typically positioned at the lowest points of the deck edge and may include valves or flaps to prevent seawater from entering during rough conditions. The term can also refer to similar drainage systems in buildings, particularly flat roofs, where scuppers direct water flow to prevent ponding and structural damage. Proper scupper maintenance is crucial for both marine and architectural applications to ensure effective water management and prevent flooding or water damage.',
            'pronunciation': '/ˈskʌpərz/',
            'etymology': 'Possibly from Old French escopir meaning to spit out, referring to the way water is expelled through these openings.',
            'memory_tip': 'Think "S-CUPPERS" - like cups that scoop water off the ship\'s deck and dump it overboard.',
            'example_sentence': 'The crew checked that all the _____ were clear of debris before the storm hit.',
            'part_of_speech': 'noun (plural)',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'scurrilous': {
            'word': 'scurrilous',
            'definition': 'Characterized by coarse, abusive language or harsh, unfair criticism; containing vulgar, insulting, or defamatory content intended to damage someone\'s reputation. Scurrilous attacks typically involve malicious gossip, crude insults, or deliberately false accusations designed to harm the target\'s character or standing. This type of communication goes beyond legitimate criticism to include personally offensive, often sexually explicit, or grossly inappropriate content. Scurrilous language may appear in political campaigns, personal disputes, or character assassination attempts. The term emphasizes the particularly low, crude nature of the attack, suggesting behavior that violates standards of decency and fair discourse. Legal contexts may consider scurrilous statements as potentially libelous or defamatory if they make false claims that damage reputation.',
            'pronunciation': '/ˈskɜːrələs/',
            'etymology': 'From Latin scurrilis meaning buffoonish or vulgar, from scurra meaning buffoon or jester.',
            'memory_tip': 'Think "SCURR-ILOUS" - scurrying around like a rat spreading vile, insulting rumors.',
            'example_sentence': 'The newspaper refused to print the _____ allegations without substantial evidence to support them.',
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
        'scuttlebutt': {
            'word': 'scuttlebutt',
            'definition': 'Informal gossip, rumors, or unofficial news, particularly within a workplace, military unit, or other close-knit community. The term originated in naval tradition, where the scuttlebutt was a water barrel or drinking fountain around which sailors would gather and exchange news, gossip, and speculation. Modern usage extends this concept to any informal communication network where information, whether accurate or not, spreads through social interaction. Scuttlebutt often includes speculation about upcoming changes, personal matters, or behind-the-scenes developments that may not be officially announced. While sometimes containing valuable insights, scuttlebutt should be treated cautiously as it frequently includes inaccurate or exaggerated information. The word captures the social aspect of information sharing and the human tendency to speculate and share news in informal settings.',
            'pronunciation': '/ˈskʌtəlbʌt/',
            'etymology': 'From scuttle (opening in a ship\'s deck) + butt (large cask), referring to a ship\'s water barrel where sailors gathered.',
            'memory_tip': 'Think "SCUTTLE-BUTT" - sailors would scuttle over to the water butt (barrel) to share gossip.',
            'example_sentence': 'The office _____ suggested that layoffs were coming, but management hadn\'t made any official announcements.',
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
        'scythe': {
            'word': 'scythe',
            'definition': 'A long-handled agricultural tool with a curved, sharp blade used for cutting grass, grain crops, or other vegetation through sweeping motions. The scythe consists of a wooden handle (called a snath or snead) attached to a curved metal blade, allowing the user to cut plants close to the ground while standing upright. This ancient farming implement was essential for harvesting grains like wheat, barley, and oats before mechanical reapers were developed. Skilled users could cut large areas efficiently with rhythmic, sweeping strokes. The scythe has symbolic associations with death (as carried by the Grim Reaper) and the passage of time, representing the cutting down of life. While largely replaced by modern machinery, scythes are still used for specialized tasks, organic farming, and maintaining areas where machines cannot operate.',
            'pronunciation': '/saɪθ/',
            'etymology': 'From Old English siðe, related to German Sense, both meaning cutting tool.',
            'memory_tip': 'Think "SIGH-THE" - you might sigh at the hard work of cutting grain with this curved blade.',
            'example_sentence': 'The farmer used a traditional _____ to harvest the wheat in the field\'s corners where the tractor couldn\'t reach.',
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
        'seafood': {
            'word': 'seafood',
            'definition': 'Edible marine life including fish, shellfish, crustaceans, mollusks, and other oceanic organisms consumed as food. Seafood encompasses a vast variety of species from different marine environments, ranging from commonly eaten fish like salmon, tuna, and cod to shellfish like shrimp, lobster, crab, and oysters. This food category is prized for its nutritional value, particularly high-quality protein, omega-3 fatty acids, vitamins, and minerals. Seafood preparation methods vary globally, including raw preparations (sushi, ceviche), grilled, fried, steamed, and baked dishes. The seafood industry involves commercial fishing, aquaculture, and processing operations that supply global markets. Sustainability concerns have led to increased focus on responsible fishing practices and aquaculture development to meet growing demand while protecting marine ecosystems.',
            'pronunciation': '/ˈsiːfuːd/',
            'etymology': 'Compound word from sea + food, literally meaning food from the sea.',
            'memory_tip': 'Think "SEA-FOOD" - food that comes from the sea, including fish and shellfish.',
            'example_sentence': 'The coastal restaurant specialized in fresh _____ caught by local fishermen that morning.',
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
        'seal': {
            'word': 'seal',
            'definition': 'A marine mammal with flippers, typically having a streamlined body adapted for swimming, including various species such as harbor seals, elephant seals, and sea lions. Seals are found in both polar and temperate waters worldwide and are known for their agility in water despite appearing clumsy on land. The term also refers to a device or substance used to close or secure something against air, water, or other materials, preventing leakage or unauthorized access. In official contexts, a seal is an emblem or stamp used to authenticate documents, showing authority or ownership. Sealing wax, stamps, and official seals have been used throughout history for document authentication. The verb form means to close securely, to make watertight or airtight, or to finalize something decisively.',
            'pronunciation': '/siːl/',
            'etymology': 'From Old English seolh meaning the marine mammal, and separately from Latin sigillum meaning small sign or seal.',
            'memory_tip': 'Think "SEAL" - both the animal that seals itself underwater and objects that seal containers closed.',
            'example_sentence': 'The harbor _____ basked in the sun on the rocky outcropping near the marina.',
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
        'search': {
            'word': 'search',
            'definition': 'The act of looking carefully and systematically for someone or something, typically involving methodical examination of multiple locations, sources, or possibilities. Searching requires strategy, persistence, and often specific techniques depending on what is being sought and where it might be found. The process can range from simple visual scanning to complex investigations involving multiple people, specialized equipment, or advanced technology. Modern digital searches use algorithms to find information in databases, websites, or other electronic repositories. Search and rescue operations involve coordinated efforts to locate missing persons. Academic and scientific research involves searching for information, evidence, or answers to questions. The effectiveness of a search depends on having clear objectives, appropriate methods, and sufficient resources to conduct thorough investigation.',
            'pronunciation': '/sɜːrtʃ/',
            'etymology': 'From Old French cerchier meaning to search or go around, from Latin circare meaning to go around.',
            'memory_tip': 'Think "SEARCH" - you make an "arch" motion with your eyes as you systematically look around.',
            'example_sentence': 'The detective began a methodical _____ of the crime scene for any overlooked evidence.',
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
        'searchpuzzles': {
            'word': 'searchpuzzles',
            'definition': '[COMBINED WORD ERROR] This appears to be two words combined: "search" (to look for something systematically) and "puzzles" (games or problems requiring solution). This combination likely resulted from a data processing error where two separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words with their individual meanings and contexts.',
            'pronunciation': '/sɜːrtʃˈpʌzəlz/',
            'etymology': 'Error combination of Old French cerchier (search) + Middle English posel (puzzles)',
            'memory_tip': 'This is a combined word error - look for the separation between search and puzzles.',
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
        'season': {
            'word': 'season',
            'definition': 'One of the four divisions of the year (spring, summer, autumn/fall, winter) characterized by particular weather conditions, temperatures, and daylight patterns resulting from Earth\'s changing position relative to the sun. Seasons affect natural cycles including plant growth, animal behavior, and agricultural activities. The term also refers to specific periods associated with particular activities, such as sports seasons, holiday seasons, or theatrical seasons. In cooking, "season" means to add salt, spices, or other flavorings to enhance taste. Legal and academic contexts may define seasons for hunting, fishing, or enrollment periods. Seasonal changes influence human activities, clothing choices, food availability, and cultural celebrations. The concept of seasons varies by geographic location, with tropical regions experiencing wet and dry seasons rather than temperature-based seasonal changes.',
            'pronunciation': '/ˈsiːzən/',
            'etymology': 'From Old French saison, from Latin satio meaning sowing or planting time.',
            'memory_tip': 'Think "SEA-SON" - like the sea\'s son that changes throughout the year with different weather.',
            'example_sentence': 'The restaurant changed its menu to reflect the fresh ingredients available each _____.',
            'part_of_speech': 'noun/verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'seats': {
            'word': 'seats',
            'definition': 'Plural of seat, referring to multiple places designed for sitting, such as chairs, benches, or designated positions in vehicles, theaters, restaurants, or other venues. Seats serve the fundamental human need for comfortable positioning during rest, work, transportation, or entertainment. The design and construction of seats vary greatly depending on their intended use, from simple stools to elaborate throne-like chairs, airplane seats, or stadium seating. In political contexts, seats refer to positions of power or representation, such as congressional seats or seats on boards of directors. Theater and event seating involves complex logistics of arrangement, pricing, and accessibility. The quality and comfort of seating significantly impact user experience in various settings, making seat design an important consideration in architecture, transportation, and furniture manufacturing.',
            'pronunciation': '/siːts/',
            'etymology': 'Plural of seat, from Old Norse sæti meaning place to sit.',
            'memory_tip': 'Think "SEATS" - places where people seat themselves, like multiple places to sit.',
            'example_sentence': 'The concert hall had over 2,000 _____ arranged in multiple tiers for optimal acoustics.',
            'part_of_speech': 'noun (plural)',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'sebaceous': {
            'word': 'sebaceous',
            'definition': 'Relating to or producing sebum, the oily substance secreted by sebaceous glands in the skin to lubricate and protect hair and skin surfaces. Sebaceous glands are microscopic structures found throughout the body, particularly concentrated on the face, scalp, and upper torso. These glands are most active during adolescence due to hormonal changes, often leading to increased oil production and potential acne development. Proper functioning sebaceous glands help maintain healthy skin by providing natural moisturization and creating a protective barrier against environmental factors. Medical conditions can affect sebaceous gland function, leading to either overproduction (resulting in oily skin and acne) or underproduction (causing dry, flaky skin). Understanding sebaceous gland function is important in dermatology and skincare treatment approaches.',
            'pronunciation': '/sɪˈbeɪʃəs/',
            'etymology': 'From Latin sebaceus, from sebum meaning tallow or grease.',
            'memory_tip': 'Think "SE-BAY-CEOUS" - glands that produce oily sebum to keep skin smooth like a bay.',
            'example_sentence': 'The dermatologist explained how _____ glands produce natural oils that can sometimes clog pores.',
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
        'secant': {
            'word': 'secant',
            'definition': 'In mathematics, a trigonometric function that is the reciprocal of the cosine function, expressed as sec(x) = 1/cos(x). The secant function is one of the six fundamental trigonometric functions and has applications in calculus, engineering, and physics. In geometry, a secant is a straight line that intersects a circle at two points, extending beyond the circle in both directions. This differs from a chord, which connects two points on a circle but doesn\'t extend beyond it, and from a tangent, which touches the circle at only one point. Secant lines are important in calculus for understanding rates of change and in the development of derivative concepts. The mathematical properties of secant functions include specific domains, ranges, and periodic behavior that are essential in advanced mathematics.',
            'pronunciation': '/ˈsiːkənt/',
            'etymology': 'From Latin secare meaning to cut, referring to a line that cuts through a circle.',
            'memory_tip': 'Think "SEC-ANT" - like an ant that cuts (secs) across a circle at two points.',
            'example_sentence': 'The geometry student drew a _____ line that intersected the circle at two distinct points.',
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
        'secession': {
            'word': 'secession',
            'definition': 'The formal withdrawal of a group from a larger political entity, such as a state leaving a federation, union, or confederation. Secession typically occurs when a region or group believes their interests are no longer served by remaining in the larger organization, or when fundamental disagreements make continued association untenable. The most famous example in American history is the secession of Southern states from the Union before the Civil War, though secession movements have occurred worldwide throughout history. The legality and legitimacy of secession are often disputed, with some constitutions explicitly forbidding it while others may provide legal mechanisms for withdrawal. Secession movements may be motivated by political, economic, cultural, or ethnic differences. The process usually involves formal declarations and may lead to the formation of new independent states.',
            'pronunciation': '/sɪˈsɛʃən/',
            'etymology': 'From Latin secessio meaning withdrawal, from secedere meaning to go apart or withdraw.',
            'memory_tip': 'Think "SE-CESSION" - a formal session where a group decides to separate and go away.',
            'example_sentence': 'The _____ of South Carolina from the Union in 1860 marked the beginning of a constitutional crisis.',
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
        'seclusion': {
            'word': 'seclusion',
            'definition': 'The state of being private and away from other people; isolation or solitude, often chosen deliberately for privacy, contemplation, or protection from external influences. Seclusion can be temporary or long-term, voluntary or involuntary, and may serve various purposes including spiritual reflection, creative work, recovery from illness, or protection from danger. Religious communities often practice seclusion through monasteries or convents where individuals withdraw from worldly concerns. Some people seek seclusion to escape stress, find peace, or focus on personal projects without interruption. In medical or psychological contexts, seclusion might be used therapeutically or as a safety measure. The degree of seclusion can range from simple privacy to complete isolation from human contact. While seclusion can provide benefits, excessive isolation may also pose mental health risks.',
            'pronunciation': '/sɪˈkluːʒən/',
            'etymology': 'From Latin seclusio meaning a shutting off, from secludere meaning to shut off or separate.',
            'memory_tip': 'Think "SE-CLUSION" - excluding yourself to be separate and alone, away from others.',
            'example_sentence': 'The writer sought _____ in a remote cabin to finish her novel without distractions.',
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
        'second': {
            'word': 'second',
            'definition': 'The ordinal number indicating the position after first in a sequence, or a unit of time equal to 1/60 of a minute. As a positional term, second denotes being next after the first in order, rank, or time. In timekeeping, a second is the base unit of time in the International System of Units, originally defined as 1/86,400 of a mean solar day but now defined by atomic frequency standards. The word also means to support or endorse someone else\'s proposal or motion, particularly in formal meetings or parliamentary procedures. As a verb, "to second" means to temporarily transfer someone to a different position or assignment. The term can also refer to items of slightly lower quality or imperfect goods sold at reduced prices, or to a person who assists another, particularly in duels or contests.',
            'pronunciation': '/ˈsɛkənd/',
            'etymology': 'From Latin secundus meaning following or next, from sequi meaning to follow.',
            'memory_tip': 'Think "SEC-OND" - the one that comes after first, in about one second.',
            'example_sentence': 'She finished in _____ place in the marathon, just twenty seconds behind the winner.',
            'part_of_speech': 'adjective/noun/verb',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'secrecy': {
            'word': 'secrecy',
            'definition': 'The practice of keeping information, actions, or intentions hidden from others; the condition of being secret or concealed. Secrecy involves deliberately withholding knowledge from certain people while potentially sharing it with others who are trusted or have legitimate need to know. This concept is fundamental in various contexts including national security, business operations, personal relationships, and legal proceedings. Government secrecy may protect sensitive information related to defense or intelligence, while corporate secrecy might involve trade secrets or competitive strategies. Personal secrecy can protect privacy or prevent harm to relationships. The level and appropriateness of secrecy often involves balancing competing interests such as security versus transparency, privacy versus accountability. Excessive secrecy can undermine trust and democratic processes, while insufficient secrecy may compromise safety or competitive advantages.',
            'pronunciation': '/ˈsiːkrəsi/',
            'etymology': 'From secret + -cy suffix, where secret comes from Latin secretus meaning separated or hidden.',
            'memory_tip': 'Think "SECRET-CY" - the quality or practice of keeping things secret.',
            'example_sentence': 'The government\'s _____ about the investigation made the public suspicious about the true circumstances.',
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
        'secret': {
            'word': 'secret',
            'definition': 'Information, knowledge, or activities that are deliberately concealed from others or known only to a limited number of people. Secrets involve conscious decisions to restrict access to certain information, often to protect individuals, organizations, or national interests. The nature of secrets varies widely, from personal confidences and family matters to classified government documents and proprietary business information. Keeping secrets requires discretion, trustworthiness, and often involves ethical considerations about when concealment is justified versus when transparency would be more appropriate. Secret information may be protected by legal frameworks, professional codes of conduct, or personal commitments. The revelation of secrets can have significant consequences, ranging from embarrassment to legal prosecution or threats to security. Psychological research shows that keeping secrets can be mentally taxing and may affect relationships and well-being.',
            'pronunciation': '/ˈsiːkrɪt/',
            'etymology': 'From Latin secretus meaning separated, hidden, or set apart, from secernere meaning to separate.',
            'memory_tip': 'Think "SE-CRET" - something that is separate and hidden from others.',
            'example_sentence': 'The spy carried state _____ that could compromise national security if discovered.',
            'part_of_speech': 'noun/adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'secreted': {
            'word': 'secreted',
            'definition': 'Past tense of secrete, which has two distinct meanings: to produce and release substances from cells, glands, or organs (as in biological secretion), or to hide or conceal something in a secret place. In biological contexts, secreted refers to substances like hormones, enzymes, or other chemicals that have been produced by specialized cells and released for specific functions within an organism. Examples include insulin secreted by pancreatic cells or saliva secreted by salivary glands. In the concealment sense, secreted means hidden away deliberately, often in a safe or secret location for protection or later retrieval. The dual meaning requires context to determine whether biological production or deliberate hiding is being described.',
            'pronunciation': '/sɪˈkriːtɪd/',
            'etymology': 'From Latin secretus meaning separated + -ed suffix, with two different etymological paths for the different meanings.',
            'memory_tip': 'Think "SE-CRETED" - either created and released by glands, or hidden away secretly.',
            'example_sentence': 'The endocrine system _____ hormones that regulate various body functions throughout the day.',
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
        'security': {
            'word': 'security',
            'definition': 'The state of being protected from danger, threats, or harm; measures taken to ensure safety and prevent unauthorized access, damage, or loss. Security encompasses physical protection of people and property, information security to protect data and communications, and financial security involving economic stability and protection of assets. Modern security involves multiple layers including personnel, technology, procedures, and policies designed to identify and mitigate risks. Cybersecurity has become increasingly important as digital systems store and process sensitive information. National security involves protecting a country\'s interests, citizens, and institutions from external and internal threats. Personal security includes measures individuals take to protect themselves, their families, and their possessions. Effective security requires ongoing assessment of threats, vulnerabilities, and the implementation of appropriate countermeasures.',
            'pronunciation': '/sɪˈkjʊrəti/',
            'etymology': 'From Latin securitas meaning freedom from care, from securus meaning free from care or danger.',
            'memory_tip': 'Think "SE-CURITY" - making sure you\'re secure and safe from threats.',
            'example_sentence': 'The airport increased _____ measures following the intelligence about potential threats.',
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
        'sedan': {
            'word': 'sedan',
            'definition': 'A passenger car with a closed body and separate trunk compartment, typically featuring four doors and seating for four or more people. Sedans are characterized by their three-box design: a distinct engine compartment, passenger cabin, and trunk area, creating a balanced and traditional automotive profile. This body style has been popular throughout automotive history due to its practicality, passenger comfort, and efficient use of space. Sedans often provide better ride quality and quieter cabins compared to other vehicle types due to their enclosed design and structural characteristics. The term historically referred to a covered chair carried by bearers, and later to enclosed horse-drawn carriages, before being applied to automobiles. Modern sedans range from compact economy models to full-size luxury vehicles, serving diverse transportation needs and preferences.',
            'pronunciation': '/sɪˈdæn/',
            'etymology': 'From French sedan, possibly from Italian sede meaning seat, or from the town of Sedan in France.',
            'memory_tip': 'Think "SE-DAN" - a car where you sit (se) down comfortably with separate compartments.',
            'example_sentence': 'The family chose a mid-size _____ for its combination of fuel efficiency and passenger comfort.',
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
        'sedentary': {
            'word': 'sedentary',
            'definition': 'Characterized by much sitting and little physical activity; involving minimal movement or exercise in daily routine. Sedentary lifestyles have become increasingly common in modern society due to desk jobs, increased screen time, and transportation that requires little physical effort. This lifestyle pattern is associated with various health risks including obesity, cardiovascular disease, diabetes, and mental health issues. The term can also describe animals that remain in one location rather than migrating, or jobs and activities that primarily involve sitting or remaining stationary. Medical professionals recommend regular movement and exercise to counteract the effects of sedentary behavior. Understanding sedentary patterns is important for developing public health initiatives and personal wellness strategies. The opposite of sedentary is an active lifestyle that includes regular physical movement and exercise.',
            'pronunciation': '/ˈsɛdənˌtɛri/',
            'etymology': 'From Latin sedentarius meaning sitting, from sedere meaning to sit.',
            'memory_tip': 'Think "SEDE-NTARY" - from sede (sit), describing a lifestyle of sitting too much.',
            'example_sentence': 'The office worker realized her _____ job was affecting her health and decided to take walking breaks.',
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
        'sedge': {
            'word': 'sedge',
            'definition': 'A grass-like plant that typically grows in wetlands, marshes, and along waterways, characterized by triangular stems and small, inconspicuous flowers arranged in clusters. Sedges belong to the family Cyperaceae and are distinguished from true grasses by their three-sided stems and different flower structures. These plants play crucial ecological roles in wetland ecosystems, providing habitat for wildlife, preventing erosion, and filtering water pollutants. Many sedge species are adapted to saturated soil conditions and can tolerate periodic flooding. They are important food sources for waterfowl and other wildlife. Some sedges have been historically used for making baskets, mats, and other woven products due to their strong, flexible stems. The phrase "sedge wren" refers to a small bird species commonly found in sedge-dominated habitats.',
            'pronunciation': '/sɛdʒ/',
            'etymology': 'From Old English secg meaning sword-like grass, referring to the sharp-edged leaves.',
            'memory_tip': 'Think "SEDGE" rhymes with "edge" - these plants have sharp edges and grow at water\'s edge.',
            'example_sentence': 'The wetland restoration project included planting native _____ species to prevent erosion along the shoreline.',
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
        'sediment': {
            'word': 'sediment',
            'definition': 'Particles of rock, soil, organic matter, or other materials that have been transported and deposited by water, wind, ice, or gravity, typically accumulating in layers on the bottom of bodies of water or on land surfaces. Sediment includes various sizes of particles from clay and silt to sand and gravel, and its composition reflects the source materials and transportation processes involved. In aquatic environments, sediment accumulation creates stratified layers that can preserve historical and environmental information, making sediment cores valuable for climate research and archaeology. Sediment transport and deposition are fundamental geological processes that shape landscapes, create fertile soils, and sometimes cause problems such as river channel filling or reservoir capacity reduction. Understanding sediment dynamics is important in environmental management, construction, and geological studies.',
            'pronunciation': '/ˈsɛdəmənt/',
            'etymology': 'From Latin sedimentum meaning settling, from sedere meaning to sit or settle.',
            'memory_tip': 'Think "SEDI-MENT" - particles that settle down (sede) to the bottom like sediment.',
            'example_sentence': 'The geologist analyzed core samples to study ancient climate patterns preserved in lake _____.',
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
        'sedulous': {
            'word': 'sedulous',
            'definition': 'Showing dedication and diligence; persevering steadily and carefully in work or effort, particularly in attention to detail and thoroughness. A sedulous person demonstrates consistent, conscientious application to tasks without being distracted or discouraged by difficulties. This quality involves patience, persistence, and methodical approaches to achieving goals or completing responsibilities. Sedulous work is characterized by careful attention to quality rather than speed, with emphasis on accuracy and completeness. The term suggests a positive work ethic that combines dedication with intelligence and skill. Sedulous individuals typically produce high-quality results because they invest appropriate time and effort in their endeavors. This characteristic is particularly valued in academic research, professional craftsmanship, and any field requiring precision and reliability.',
            'pronunciation': '/ˈsɛdʒələs/',
            'etymology': 'From Latin sedulus meaning zealous or diligent, possibly from sine dolo meaning without guile.',
            'memory_tip': 'Think "SED-ULOUS" - being so dedicated that you sit (sed) and work continuously with zealous effort.',
            'example_sentence': 'The researcher\'s _____ attention to detail ensured that the experimental data was accurate and reliable.',
            'part_of_speech': 'adjective',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Two Bee',
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
    
    print(f"\nBatch 156 processing complete!")
    print(f"Successfully processed {len(processed_words)}/{len(words)} words")
    print(f"Output saved to: {output_file}")
    
    if combined_errors:
        print(f"\nCombined word errors detected: {len(combined_errors)}")
        for error in combined_errors:
            print(f"  - {error}")

if __name__ == "__main__":
    process_batch()