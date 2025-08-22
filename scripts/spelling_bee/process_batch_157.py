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
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_157_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_157_processed.csv'
    
    calculator = DifficultyCalculator()
    
    word_data = {
        'sedum': {
            'word': 'sedum',
            'definition': 'A genus of succulent plants in the family Crassulaceae, commonly known as stonecrops, characterized by thick, fleshy leaves and star-shaped flowers. Sedums are popular in xeriscaping and rock gardens due to their drought tolerance and ability to thrive in poor soil conditions. These plants store water in their leaves, making them highly adapted to arid environments and capable of surviving extended periods without irrigation. Many sedum species produce attractive clusters of small flowers in various colors including yellow, white, pink, and red. They are valued for their low maintenance requirements, ability to spread as ground cover, and use in green roof installations. Some species like Sedum spectabile (showy stonecrop) are particularly prized for their late-season blooms that attract butterflies and other pollinators.',
            'pronunciation': '/ˈsiːdəm/',
            'etymology': 'From Latin sedum meaning houseleek, from sedere meaning to sit, referring to how these plants sit on rocks.',
            'memory_tip': 'Think "SEED-UM" - succulent plants that sit and store water like seeds storing energy.',
            'example_sentence': 'The rock garden featured various _____ species that created colorful displays with minimal water requirements.',
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
        'seen': {
            'word': 'seen',
            'definition': 'Past participle of the verb "see," indicating that something has been observed, witnessed, or perceived visually at some point in the past. The word is used in perfect tenses to describe completed actions of visual perception, such as "I have seen that movie" or "She had seen the accident happen." Seen requires an auxiliary verb (have, has, had) when used as a past participle, distinguishing it from the simple past tense "saw." The term can also refer to being noticed, understood, or experienced, extending beyond just visual perception to include recognition or comprehension. In passive constructions, "seen" indicates that someone or something was observed by others. The word is fundamental to describing past experiences and observations in English.',
            'pronunciation': '/siːn/',
            'etymology': 'From Old English sewen, past participle of seon meaning to see, related to German gesehen.',
            'memory_tip': 'Think "SEEN" rhymes with "been" - both are past participles describing completed actions.',
            'example_sentence': 'The witness testified that she had _____ the suspect leaving the building at midnight.',
            'part_of_speech': 'verb (past participle)',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'seer': {
            'word': 'seer',
            'definition': 'A person believed to have the ability to perceive future events or hidden truths through supernatural insight, prophetic vision, or mystical powers. Seers have appeared throughout history in various cultures as oracles, prophets, fortune-tellers, or spiritual advisors who claim to access information beyond normal sensory perception. In religious and mythological contexts, seers often serve as intermediaries between divine realms and human society, delivering prophecies or guidance. The term can also refer to anyone with exceptional foresight, wisdom, or ability to predict outcomes based on careful observation and analysis. Modern usage sometimes applies "seer" to visionary leaders, analysts, or futurists who demonstrate remarkable insight into trends and developments. The credibility and interpretation of seers\' predictions have been subjects of debate throughout human history.',
            'pronunciation': '/sɪr/',
            'etymology': 'From see + -er suffix, literally meaning one who sees, particularly one who sees beyond the normal range.',
            'memory_tip': 'Think "SEE-ER" - someone who sees beyond what others can see, into the future.',
            'example_sentence': 'The ancient _____ predicted that the kingdom would face great challenges in the coming year.',
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
        'seethe': {
            'word': 'seethe',
            'definition': 'To be extremely angry or filled with rage, often while trying to control or suppress these intense emotions; to be in a state of inner turmoil or agitation. The word originates from the literal meaning of boiling or bubbling with heat, and this metaphor perfectly captures the image of emotions bubbling just beneath the surface. Someone who is seething may appear outwardly calm while experiencing intense internal anger or frustration. The term can also literally mean to boil vigorously or to foam and bubble, as in cooking or chemical processes. Seething anger often implies a prolonged state of fury rather than a brief outburst, suggesting that the person is struggling to contain their emotions. This controlled rage can be more intimidating than open displays of anger because it suggests potential for explosive release.',
            'pronunciation': '/siːð/',
            'etymology': 'From Old English sēothan meaning to boil or cook, related to German sieden meaning to boil.',
            'memory_tip': 'Think "SEE-THE" - you can see the anger boiling like liquid in a pot.',
            'example_sentence': 'After being passed over for promotion again, she continued to _____ with resentment.',
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
        'segmentate': {
            'word': 'segmentate',
            'definition': 'To divide into segments or distinct sections; to separate something into component parts or portions. This term is often used in biological contexts to describe the development of segmented body structures, such as the formation of body segments in insects, worms, or other arthropods during embryonic development. In technical and analytical contexts, segmentation involves breaking down complex systems, data sets, or structures into manageable, identifiable components for study or organization. Market research uses segmentation to divide consumer populations into distinct groups based on characteristics or behaviors. Image processing and computer vision employ segmentation algorithms to identify and separate different regions or objects within digital images. The process of segmentation is fundamental to understanding complex systems by examining their constituent parts.',
            'pronunciation': '/ˈsɛɡmənˌteɪt/',
            'etymology': 'From Latin segmentum meaning a piece cut off + -ate suffix meaning to make or cause.',
            'memory_tip': 'Think "SEGMENT-ATE" - to create segments by dividing something into parts.',
            'example_sentence': 'The biologist studied how embryos _____ into distinct body regions during early development.',
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
        'seiche': {
            'word': 'seiche',
            'definition': 'A standing wave oscillation in an enclosed or partially enclosed body of water, such as a lake, bay, or harbor, caused by atmospheric pressure changes, seismic activity, or wind patterns. Unlike regular waves that travel across water surfaces, seiches involve the entire water body rocking back and forth like water sloshing in a bathtub. These phenomena can cause water levels to rise and fall dramatically at different ends of the water body, sometimes creating dangerous conditions for boats and shoreline structures. Lake seiches are common in large lakes like the Great Lakes, where they can cause water level changes of several feet. The oscillation period depends on the dimensions and depth of the water body, following specific mathematical relationships. Seiches demonstrate fundamental principles of fluid dynamics and wave mechanics in confined spaces.',
            'pronunciation': '/seɪʃ/',
            'etymology': 'From French seiche, from Swiss German Säck meaning to sink or dry up, referring to water level changes.',
            'memory_tip': 'Think "SAY-SH" - like saying "shush" to calm the oscillating water in a lake.',
            'example_sentence': 'The harbor experienced a _____ that caused boats to rock violently despite the absence of storm waves.',
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
        'seine': {
            'word': 'seine',
            'definition': 'A large fishing net designed to encircle schools of fish, with floats along the top edge and weights along the bottom, allowing fishermen to surround and capture fish by drawing the net closed like a purse. Seine nets can be operated from shore (beach seining) or from boats (purse seining), depending on the fishing location and target species. This ancient fishing method is highly effective for catching schooling fish such as sardines, mackerel, tuna, and salmon. The net is deployed in a large circle around a fish school, then the bottom is closed to prevent escape, and the entire catch is hauled aboard. Seine fishing requires coordination between multiple crew members and specific techniques for different fish species and water conditions. Modern seine nets may incorporate sonar technology to locate fish schools and optimize fishing success.',
            'pronunciation': '/seɪn/',
            'etymology': 'From Old English segne, from Latin sagena, from Greek σαγήνη (sagene) meaning fishing net.',
            'memory_tip': 'Think "SANE" - a sane way to catch fish by surrounding them with a net.',
            'example_sentence': 'The fishing crew deployed their _____ net to encircle the large school of tuna.',
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
        'seismologist': {
            'word': 'seismologist',
            'definition': 'A scientist who specializes in the study of earthquakes and seismic waves, analyzing the movement and behavior of Earth\'s crust to understand geological processes and earthquake mechanisms. Seismologists use sophisticated instruments called seismometers to detect and measure ground motion, studying how seismic waves travel through different types of rock and soil. Their work involves interpreting seismic data to determine earthquake locations, magnitudes, and depths, as well as investigating the geological structures that influence seismic activity. This research is crucial for earthquake hazard assessment, building code development, and public safety planning in earthquake-prone regions. Seismologists also study volcanic tremors, landslides, and other phenomena that generate seismic signals. Their expertise contributes to early warning systems and helps communities prepare for and respond to seismic events.',
            'pronunciation': '/saɪzˈmɒlədʒɪst/',
            'etymology': 'From Greek seismos meaning earthquake + logos meaning study + -ist meaning one who practices.',
            'memory_tip': 'Think "SEISMO-LOGIST" - a scientist who studies seismic activity and earthquakes.',
            'example_sentence': 'The _____ analyzed the earthquake data to determine the exact location and magnitude of the tremor.',
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
        'seize': {
            'word': 'seize',
            'definition': 'To take hold of suddenly and forcibly; to grab, capture, or apprehend with quick, decisive action. The word implies swift, deliberate action to gain control of something or someone, often suggesting urgency or the need to act before an opportunity is lost. In legal contexts, seize refers to the official confiscation of property by authorities, such as when police seize evidence or when governments seize assets. The term can also mean to take advantage of an opportunity, as in "seizing the moment" or "seizing an opportunity." Mechanical seizure describes when moving parts become stuck due to overheating, lack of lubrication, or excessive friction. Medical seizures involve sudden, uncontrolled electrical activity in the brain. The word emphasizes the forceful, immediate nature of the action.',
            'pronunciation': '/siːz/',
            'etymology': 'From Old French seisir meaning to take possession, from Germanic roots meaning to set or place.',
            'memory_tip': 'Think "SEES" but with a "Z" - when you see an opportunity, you seize it quickly.',
            'example_sentence': 'The police moved quickly to _____ the suspect before he could escape through the back door.',
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
        'selah': {
            'word': 'selah',
            'definition': 'A Hebrew word appearing frequently in the Psalms and Habakkuk in the Bible, whose exact meaning remains uncertain but is generally believed to indicate a musical or liturgical direction. Scholars suggest it may signal a pause for reflection, an instrumental interlude, a change in musical tempo or key, or a moment for the congregation to respond. The word appears 71 times in the Psalms and 3 times in Habakkuk, always at the end of a verse or stanza. Some interpretations suggest it means "forever" or "amen," while others propose it indicates emphasis or calls attention to important passages. In modern worship and biblical study, selah is often understood as an invitation to pause and meditate on the preceding words. The mystery surrounding its precise meaning has made it a subject of ongoing theological and linguistic research.',
            'pronunciation': '/ˈsiːlə/ or /ˈseɪlə/',
            'etymology': 'From Hebrew סֶלָה (selah), possibly related to salal meaning to lift up or exalt.',
            'memory_tip': 'Think "SEE-LAH" - a moment to see and reflect on what has been said.',
            'example_sentence': 'The psalm ended with the word _____, indicating a pause for contemplation.',
            'part_of_speech': 'interjection',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'seldom': {
            'word': 'seldom',
            'definition': 'Rarely; not often; infrequently occurring or happening. This adverb indicates that something takes place only occasionally or at long intervals, emphasizing the uncommon nature of the event, action, or condition being described. Seldom suggests a frequency that is notably less than normal or expected, often implying that the occurrence is exceptional rather than routine. The word can describe both deliberate choices (such as seldom visiting a place) and natural patterns (such as rain seldom falling in desert regions). In formal or literary contexts, seldom often appears at the beginning of sentences for emphasis, as in "Seldom had she seen such beauty." The term conveys a sense of scarcity or rarity that makes the occasional occurrence more significant or noteworthy.',
            'pronunciation': '/ˈsɛldəm/',
            'etymology': 'From Old English seldan, from Germanic roots meaning strange or wonderful, implying rarity.',
            'memory_tip': 'Think "SELL-DOM" - so rarely for sale that it\'s seldom available.',
            'example_sentence': 'The reclusive author _____ made public appearances, preferring to let her work speak for itself.',
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
        'selected': {
            'word': 'selected',
            'definition': 'Chosen from a larger group based on specific criteria, preferences, or qualifications; picked out as being suitable, desirable, or meeting particular requirements. The word implies a deliberate process of evaluation and choice, where options are considered and decisions are made about which items, people, or possibilities are most appropriate for a given purpose. Selection can be based on merit, random chance, systematic criteria, or personal preference, depending on the context. The term suggests that not all available options were chosen, highlighting the exclusivity or special nature of what was selected. In various contexts, selection might involve competitive processes, careful screening, or strategic decision-making. The past tense form emphasizes that the choosing process has been completed.',
            'pronunciation': '/sɪˈlɛktɪd/',
            'etymology': 'From Latin selectus, past participle of seligere meaning to choose, from se- (apart) + legere (to choose).',
            'memory_tip': 'Think "SE-LECTED" - separated out and chosen from others through a selection process.',
            'example_sentence': 'The committee _____ five finalists from over three hundred applicants for the scholarship.',
            'part_of_speech': 'adjective/verb (past tense)',
            'source': 'Scripps National Spelling Bee',
            'source_difficulty': 'One Bee/Three Bee/Two Bee',
            'claude_difficulty': None,
            'phonetic_score': None,
            'frequency_score': None,
            'morphological_score': None,
            'etymology_score': None,
            'total_score': None
        },
        'selfie': {
            'word': 'selfie',
            'definition': 'A self-portrait photograph taken with a digital camera or smartphone, typically held at arm\'s length or using a front-facing camera. Selfies became a cultural phenomenon with the widespread adoption of smartphones equipped with front-facing cameras and social media platforms that encourage photo sharing. The practice ranges from casual personal photos to carefully composed images using various techniques, angles, and editing apps to achieve desired effects. Selfie culture has influenced social media behavior, photography trends, and even psychology research regarding self-image and social validation. The term has spawned related words like "selfie stick" (a device for extending camera reach) and "groupie" (a group selfie). While sometimes criticized for promoting narcissism, selfies also represent new forms of self-expression, documentation, and social connection in the digital age.',
            'pronunciation': '/ˈsɛlfi/',
            'etymology': 'From self + -ie diminutive suffix, first recorded in Australian slang around 2002.',
            'memory_tip': 'Think "SELF-IE" - a picture of yourself, like adding "ie" to make self cute and casual.',
            'example_sentence': 'She took a quick _____ with the famous landmark visible in the background.',
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
        'seller': {
            'word': 'seller',
            'definition': 'A person or entity that offers goods, services, or property for sale; someone engaged in the act of selling or transferring ownership in exchange for payment. Sellers can range from individual proprietors and small business owners to large corporations and online retailers. The term encompasses various types of commercial relationships, including retail sellers who sell directly to consumers, wholesale sellers who sell to other businesses, and private sellers who occasionally sell personal items. In real estate, the seller is the property owner transferring ownership to a buyer. Successful sellers typically understand their products or services, know their target market, and possess effective communication and negotiation skills. The relationship between sellers and buyers forms the foundation of commerce and economic exchange in market-based economies.',
            'pronunciation': '/ˈsɛlər/',
            'etymology': 'From sell + -er suffix, where sell comes from Old English sellan meaning to give or deliver.',
            'memory_tip': 'Think "SELL-ER" - one who sells things to others.',
            'example_sentence': 'The online _____ shipped the package within 24 hours of receiving the order.',
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
        'sells': {
            'word': 'sells',
            'definition': 'Third-person singular present tense of the verb "sell," meaning to transfer ownership of goods, services, or property to another person in exchange for money or other compensation. The word describes the ongoing action or habitual practice of offering items for purchase, whether by individuals, businesses, or organizations. Selling involves presenting products or services to potential customers, negotiating terms, and completing transactions. The term can also refer to convincing someone to accept an idea, proposal, or point of view, as in "selling an idea." In financial contexts, selling might refer to disposing of investments or assets. Effective selling requires understanding customer needs, communicating value propositions, and building trust with buyers. The success of selling activities often determines the viability and profitability of businesses.',
            'pronunciation': '/sɛlz/',
            'etymology': 'From Old English sellan meaning to give, deliver, or sell + -s third person singular suffix.',
            'memory_tip': 'Think "SELL-S" - what a person or business does when they sell things regularly.',
            'example_sentence': 'The local bakery _____ fresh bread and pastries every morning.',
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
        'semaphore': {
            'word': 'semaphore',
            'definition': 'A visual signaling system using flags, lights, or mechanical arms to communicate messages across distances, particularly used in maritime and railway communications. The most common form involves two handheld flags held in different positions to represent letters of the alphabet, allowing ships to communicate when radio silence is required or as a backup communication method. Railway semaphores use mechanical arms or colored lights to signal train operators about track conditions and movement permissions. Optical telegraph systems used semaphore towers with movable arms to relay messages across long distances before electrical telegraphy was developed. In computer science, a semaphore is a synchronization primitive used to control access to shared resources in concurrent programming. The fundamental principle involves using visible signals that can be interpreted according to established codes or protocols.',
            'pronunciation': '/ˈsɛməˌfɔr/',
            'etymology': 'From Greek sema meaning sign + phoros meaning bearing or carrying, literally meaning sign-bearer.',
            'memory_tip': 'Think "SEMA-PHORE" - carrying (phore) signs (sema) to communicate messages.',
            'example_sentence': 'The Navy cadets practiced _____ flag signals to communicate between ships during radio silence.',
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
        'semblance': {
            'word': 'semblance',
            'definition': 'An outward appearance or apparent similarity to something else, often suggesting that the resemblance may be superficial or misleading rather than representing true equivalence. A semblance indicates a degree of likeness or similarity that may mask important differences or create false impressions about the actual nature of something. The term often implies that while something appears to possess certain characteristics, it may lack the substance or genuine qualities associated with what it resembles. In social contexts, maintaining a semblance of normalcy might mean appearing calm and composed while experiencing internal turmoil. The word frequently appears in phrases like "semblance of order" or "semblance of truth," suggesting approximation rather than complete authenticity. This concept highlights the distinction between appearance and reality.',
            'pronunciation': '/ˈsɛmbləns/',
            'etymology': 'From Old French semblance, from sembler meaning to seem or appear, from Latin simulare.',
            'memory_tip': 'Think "SEM-BLANCE" - a glance that seems similar but may not be the same thing.',
            'example_sentence': 'After the crisis, the company tried to maintain a _____ of stability while reorganizing internally.',
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
        'semester': {
            'word': 'semester',
            'definition': 'An academic term lasting approximately half of a school year, typically 15-18 weeks, used to organize coursework and academic calendars in educational institutions. Most universities and colleges operate on semester systems with fall and spring semesters, often including shorter summer sessions. The semester system allows for in-depth study of subjects over extended periods while providing natural breaks for evaluation, planning, and rest. Students typically enroll in multiple courses simultaneously during each semester, accumulating credits toward degree requirements. Faculty use semesters to structure curriculum delivery, assess student progress, and plan research activities. The semester format influences academic scheduling, financial aid disbursement, and student life planning. Some institutions use quarter systems or trimester systems as alternatives, but the semester remains the most common academic calendar structure in higher education.',
            'pronunciation': '/sɪˈmɛstər/',
            'etymology': 'From Latin semestris meaning of six months, from sex (six) + mensis (month).',
            'memory_tip': 'Think "SEMI-ESTER" - semi (half) of the year, like a half-year term.',
            'example_sentence': 'The student registered for five courses during the fall _____ to complete her degree requirements.',
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
        'semicolon': {
            'word': 'semicolon',
            'definition': 'A punctuation mark (;) used to separate clauses in a sentence, particularly to join two independent clauses that are closely related in meaning but could stand alone as separate sentences. The semicolon provides a stronger pause than a comma but a weaker separation than a period, allowing writers to show relationships between ideas while maintaining sentence unity. It is commonly used before coordinating conjunctions when clauses contain internal commas, in complex lists where items contain commas, and to separate items in series when those items are lengthy or complex. Proper semicolon usage requires understanding sentence structure and the logical relationships between ideas. While some consider it formal or academic punctuation, the semicolon serves important functions in clear, sophisticated writing. Mastering semicolon usage demonstrates advanced understanding of English punctuation conventions.',
            'pronunciation': '/ˈsɛmiˌkoʊlən/',
            'etymology': 'From semi- meaning half + colon, literally meaning half-colon in terms of pause strength.',
            'memory_tip': 'Think "SEMI-COLON" - halfway between a comma and a colon in terms of the pause it creates.',
            'example_sentence': 'The writer used a _____ to connect two related thoughts in a single, flowing sentence.',
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
        'seminary': {
            'word': 'seminary',
            'definition': 'An educational institution for training religious leaders, particularly those preparing for ordination as priests, ministers, rabbis, or other clergy members. Seminaries provide theological education, spiritual formation, and practical training for religious ministry, combining academic study of religious texts, history, and doctrine with pastoral skills development. These institutions vary in their denominational affiliations, degree programs, and educational approaches, but generally focus on preparing students for leadership roles in religious communities. Seminary education typically includes courses in scripture study, theology, church history, pastoral care, preaching, and religious education. Many seminaries also emphasize spiritual development, community service, and practical ministry experience. The term can also refer to any institution of learning or training, though this broader usage is less common in modern contexts.',
            'pronunciation': '/ˈsɛməˌnɛri/',
            'etymology': 'From Latin seminarium meaning seed plot or nursery, from semen meaning seed.',
            'memory_tip': 'Think "SEMIN-ARY" - like a place where seeds (semina) of religious knowledge are planted and grow.',
            'example_sentence': 'After graduating from the _____, he was ordained as a minister in his denomination.',
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
        'senate': {
            'word': 'senate',
            'definition': 'The upper house of a bicameral legislature, typically representing regions or states within a federal system and often having equal representation regardless of population size. In the United States, the Senate consists of 100 members, with two senators from each state serving six-year terms. The Roman Senate was a governing body of appointed or elected officials who advised consuls and made important political decisions. Modern senates often have specific constitutional powers such as confirming appointments, trying impeachments, or representing territorial interests in federal legislation. The structure and powers of senates vary among different countries and governmental systems. Senate members are usually called senators and often serve longer terms than lower house representatives. The institution represents principles of federalism, deliberation, and balanced representation in democratic governance.',
            'pronunciation': '/ˈsɛnɪt/',
            'etymology': 'From Latin senatus meaning council of elders, from senex meaning old man or elder.',
            'memory_tip': 'Think "SEN-ATE" - where senators (sen) meet to debate and vote.',
            'example_sentence': 'The bill passed the House but faced strong opposition in the _____.',
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
        'senator': {
            'word': 'senator',
            'definition': 'An elected member of a senate, particularly in legislative bodies where senators represent states, provinces, or other geographic or political divisions. Senators typically serve longer terms than representatives in lower houses and often have specific constitutional responsibilities such as confirming executive appointments, conducting impeachment trials, or representing regional interests in national legislation. In the United States, senators serve six-year terms and have equal representation (two per state) regardless of state population. The role requires understanding complex legislation, building coalitions, and balancing local state interests with national concerns. Senators often serve on committees that specialize in specific policy areas such as foreign relations, judiciary, or appropriations. The position typically involves significant public visibility, media attention, and political responsibility for major policy decisions affecting their constituents and the nation.',
            'pronunciation': '/ˈsɛnətər/',
            'etymology': 'From Latin senator meaning member of the senate, from senatus meaning council of elders.',
            'memory_tip': 'Think "SENAT-OR" - one who serves in the senate, a senator.',
            'example_sentence': 'The _____ from California introduced legislation to address climate change concerns.',
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
        'senecio': {
            'word': 'senecio',
            'definition': 'A large genus of flowering plants in the daisy family (Asteraceae), commonly known as ragworts or groundsels, comprising over 1,000 species found worldwide in diverse habitats. Senecio plants are characterized by their composite flower heads, typically featuring yellow ray petals surrounding a central disc, though some species have different colors or lack ray petals entirely. Many species are considered weeds due to their aggressive growth and ability to colonize disturbed areas, while others are cultivated as ornamental plants for their attractive flowers and foliage. Some senecio species contain pyrrolizidine alkaloids that can be toxic to livestock and humans if consumed. The genus includes both annual and perennial herbs, shrubs, and even some tree forms. Several species have medicinal uses in traditional folk remedies, though their toxicity requires careful consideration.',
            'pronunciation': '/sɪˈniːʃioʊ/',
            'etymology': 'From Latin senecio meaning old man, referring to the white, fluffy seed heads that resemble gray hair.',
            'memory_tip': 'Think "SEN-ECIO" - plants with fluffy white seeds like an old man\'s (senex) hair.',
            'example_sentence': 'The botanist identified several _____ species growing wild in the abandoned field.',
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
        'senescent': {
            'word': 'senescent',
            'definition': 'In the process of aging or growing old; exhibiting the characteristics, changes, or decline associated with advancing age. In biological contexts, senescence refers to the gradual deterioration of cellular and organismal functions over time, leading to decreased vitality, reduced reproductive capacity, and increased vulnerability to disease and death. Cellular senescence involves the cessation of cell division and the accumulation of cellular damage that cannot be repaired. Plant senescence includes processes like leaf yellowing and dropping in autumn. The term can apply to individuals, populations, or even civilizations that show signs of decline or reduced vigor. Senescent changes are natural parts of life cycles but can be influenced by genetic factors, environmental conditions, and lifestyle choices. Understanding senescence is important in fields ranging from medicine and biology to sociology and economics.',
            'pronunciation': '/sɪˈnɛsənt/',
            'etymology': 'From Latin senescens, present participle of senescere meaning to grow old, from senex meaning old.',
            'memory_tip': 'Think "SEN-ESCENT" - becoming like a senior (sen), in the process of aging.',
            'example_sentence': 'The _____ leaves turned brilliant colors before falling from the trees in autumn.',
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
        'seneschal': {
            'word': 'seneschal',
            'definition': 'A high-ranking household officer in medieval European courts responsible for managing domestic arrangements, supervising servants, and sometimes serving as a regent or deputy ruler. The seneschal held significant authority over the household\'s daily operations, including food service, accommodations, and ceremonial functions. In larger courts, the position carried considerable political influence and the seneschal might represent the lord\'s interests in legal and administrative matters. The role varied by region and time period, with some seneschals serving primarily as domestic administrators while others wielded substantial political power. In feudal France, royal seneschals governed provinces and administered justice in the king\'s name. The position required diplomatic skills, administrative competence, and absolute loyalty to the lord or monarch. Modern usage of the term might refer to ceremonial officers in historical organizations or to stewards managing large estates.',
            'pronunciation': '/ˈsɛnəʃəl/',
            'etymology': 'From Old French seneschal, from Germanic siniscalc meaning senior servant, from sini (old/senior) + scalc (servant).',
            'memory_tip': 'Think "SEN-ESCHAL" - a senior (sen) officer who manages the household like an essential (eschal) administrator.',
            'example_sentence': 'The castle\'s _____ organized the elaborate feast to welcome the visiting dignitaries.',
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
        'senile': {
            'word': 'senile',
            'definition': 'Showing signs of mental decline or confusion typically associated with advanced age, particularly involving memory loss, disorientation, or diminished cognitive abilities. The term medically refers to age-related deterioration of mental faculties, though modern medical practice often uses more specific diagnoses like dementia or Alzheimer\'s disease rather than the general term "senile." Senile changes can include difficulty remembering recent events, confusion about time or place, impaired judgment, and personality changes. However, it\'s important to note that cognitive decline is not an inevitable part of normal aging, and many older adults maintain sharp mental faculties throughout their lives. The word is sometimes used more broadly to describe anything worn out or deteriorated due to age. In contemporary usage, the term can be considered insensitive when applied to people, as it may perpetuate negative stereotypes about aging.',
            'pronunciation': '/ˈsinaɪl/',
            'etymology': 'From Latin senilis meaning of old age, from senex meaning old man or elder.',
            'memory_tip': 'Think "SEN-ILE" - relating to seniors (sen) who may have age-related mental changes.',
            'example_sentence': 'The doctor explained that not all memory problems in older adults indicate _____ dementia.',
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
        'senna': {
            'word': 'senna',
            'definition': 'A genus of flowering plants in the legume family, many species of which have medicinal properties, particularly as natural laxatives. Senna leaves and pods contain compounds called sennosides that stimulate bowel movements and have been used for centuries in traditional medicine to treat constipation. The most commonly used medicinal species include Senna alexandrina (Alexandrian senna) and Senna angustifolia (Tinnevelly senna). These plants are native to tropical and subtropical regions and are cultivated commercially for pharmaceutical use. Senna is available in various forms including teas, tablets, and liquid preparations, though it should be used with caution as it can cause cramping and dependence if used long-term. The plants typically have pinnate leaves and yellow flowers that develop into distinctive pod-like fruits. Some ornamental senna species are grown for their attractive flowers and foliage.',
            'pronunciation': '/ˈsɛnə/',
            'etymology': 'From Arabic sanā, referring to the medicinal plant known for its purgative properties.',
            'memory_tip': 'Think "SEN-NA" - a plant whose name sounds like "sent-ya" running to the bathroom.',
            'example_sentence': 'The herbalist recommended _____ tea as a natural remedy for occasional constipation.',
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
        'sennanoun': {
            'word': 'sennanoun',
            'definition': '[COMBINED WORD ERROR] This appears to be two words combined: "senna" (a medicinal plant used as a laxative) and "noun" (a grammatical term for naming words). This combination likely resulted from a data processing error where two separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words with their individual meanings and contexts.',
            'pronunciation': '/ˈsɛnənaʊn/',
            'etymology': 'Error combination of Arabic sanā (senna) + Latin nomen (noun)',
            'memory_tip': 'This is a combined word error - look for the separation between senna and noun.',
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
        'senryu': {
            'word': 'senryu',
            'definition': 'A Japanese form of short poetry similar to haiku in structure (three lines with a 5-7-5 syllable pattern) but differing in subject matter and tone. While haiku traditionally focus on nature and seasonal references with a contemplative mood, senryu typically deal with human nature, emotions, relationships, and often incorporate humor, irony, or satire. Senryu poems frequently comment on human foibles, social situations, or everyday experiences with wit and insight. The form was named after Edo-period poet Karai Senryu, who popularized this style of verse. Unlike haiku, senryu don\'t require seasonal words (kigo) or cutting words (kireji) and tend to be more direct and conversational in tone. This poetic form has gained popularity in contemporary poetry for its accessibility and relevance to modern urban life experiences.',
            'pronunciation': '/sɛnˈrjuː/',
            'etymology': 'Named after Japanese poet Karai Senryu (1718-1790) who popularized this style of poetry.',
            'memory_tip': 'Think "SEN-RYU" - a type of Japanese poem named after the poet Senryu.',
            'example_sentence': 'The poetry workshop focused on writing _____ verses about modern city life.',
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
        'sensation': {
            'word': 'sensation',
            'definition': 'A physical or mental feeling or perception resulting from stimulation of the senses or from internal bodily processes. Sensations include basic sensory experiences such as touch, taste, smell, sight, and hearing, as well as more complex feelings like pain, temperature, or pressure. In psychology, sensation refers to the initial detection and encoding of stimulus energy by sensory receptors and the nervous system. The term also describes intense interest, excitement, or public attention, as when something creates a "sensation" in the media or society. Medical contexts use sensation to describe the ability to feel physical stimuli, with loss of sensation being a symptom of various neurological conditions. The word can also refer to remarkable or outstanding events, people, or phenomena that attract widespread attention and admiration.',
            'pronunciation': '/sɛnˈseɪʃən/',
            'etymology': 'From Latin sensatio meaning perception by the senses, from sentire meaning to feel or perceive.',
            'memory_tip': 'Think "SENS-ATION" - the action of sensing or feeling something through your senses.',
            'example_sentence': 'The pianist\'s debut performance was a _____ that launched her international career.',
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
        'sensei': {
            'word': 'sensei',
            'definition': 'A Japanese term meaning teacher or instructor, particularly used for martial arts teachers, but also applicable to any respected teacher or mentor in various fields of study. In Japanese culture, sensei conveys deep respect for someone who has achieved mastery in their discipline and shares knowledge with students. The relationship between sensei and student involves mutual respect, dedication, and often extends beyond mere technical instruction to include moral and philosophical guidance. In martial arts contexts, a sensei has typically achieved black belt rank and demonstrated proficiency in teaching techniques, philosophy, and traditions of their art. The term has been adopted in Western cultures, particularly in martial arts schools, but is also used more broadly to show respect for knowledgeable teachers. The role implies responsibility for student development, safety, and character formation.',
            'pronunciation': '/ˈsɛnseɪ/',
            'etymology': 'From Japanese sensei meaning teacher, from sen (before/previous) + sei (life/birth), literally meaning "born before."',
            'memory_tip': 'Think "SEN-SEI" - someone who has seen (sei) more and teaches others.',
            'example_sentence': 'The karate students bowed respectfully to their _____ before beginning class.',
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
        'sensory': {
            'word': 'sensory',
            'definition': 'Relating to or involving the physical senses (sight, hearing, touch, taste, smell) or the nervous system pathways that transmit sensory information to the brain. Sensory organs detect various types of stimuli from the environment and internal body conditions, converting physical or chemical signals into electrical impulses that the nervous system can process. Sensory processing involves complex interactions between specialized receptor cells, nerve pathways, and brain regions that interpret sensory data to create our perceptions of the world. Medical conditions can affect sensory function, leading to impairments in vision, hearing, touch sensation, or other sensory modalities. Sensory integration therapy helps individuals with processing difficulties. Educational and therapeutic applications often involve sensory experiences to enhance learning, memory, and development, particularly for children with special needs.',
            'pronunciation': '/ˈsɛnsəri/',
            'etymology': 'From Latin sensorius meaning of the senses, from sentire meaning to feel or perceive.',
            'memory_tip': 'Think "SENS-ORY" - relating to your senses or sensory organs.',
            'example_sentence': 'The child\'s _____ processing disorder affected how he responded to textures and sounds.',
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
        'sentient': {
            'word': 'sentient',
            'definition': 'Having the capacity for sensation, perception, or consciousness; able to experience feelings and awareness. Sentience involves the ability to have subjective experiences, to feel pleasure and pain, and to be aware of one\'s surroundings and internal states. In philosophy and ethics, sentience is often considered a criterion for moral consideration, with many arguing that sentient beings deserve protection from unnecessary suffering. The concept is particularly important in discussions about animal rights, artificial intelligence, and environmental ethics. Scientists study sentience in various species to understand the evolution and mechanisms of consciousness. In science fiction, sentient often describes artificial intelligences or alien species that possess consciousness comparable to humans. The degree and nature of sentience varies among different species, with ongoing research exploring consciousness in animals ranging from mammals to invertebrates.',
            'pronunciation': '/ˈsɛnʃənt/',
            'etymology': 'From Latin sentiens, present participle of sentire meaning to feel or perceive.',
            'memory_tip': 'Think "SENT-IENT" - able to sense and feel, having sent-ience or awareness.',
            'example_sentence': 'The philosopher argued that all _____ beings deserve moral consideration regardless of their species.',
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
        'sentinel': {
            'word': 'sentinel',
            'definition': 'A guard or watchperson stationed to keep watch and warn of approaching danger; someone or something that serves as a lookout or protective presence. Sentinels have historically been essential for military defense, community safety, and security operations, positioned at strategic locations to observe and report on potential threats. The role requires vigilance, reliability, and the ability to quickly communicate warnings to others. In modern contexts, sentinel can refer to automated monitoring systems, guard animals, or any person or device that serves a protective surveillance function. Medical terminology uses "sentinel" to describe symptoms, events, or anatomical structures that serve as early warning signs of disease or abnormal conditions. The word can also apply metaphorically to people or institutions that defend important principles, rights, or values within society.',
            'pronunciation': '/ˈsɛntɪnəl/',
            'etymology': 'From French sentinelle, from Italian sentinella, from sentire meaning to hear or watch.',
            'memory_tip': 'Think "SENT-IN-EL" - someone sent in to watch and guard a location.',
            'example_sentence': 'The lone _____ stood watch at the castle gate throughout the cold night.',
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
        'seperadventure': {
            'word': 'seperadventure',
            'definition': '[COMBINED WORD ERROR] This appears to be two words combined: "separ" (likely part of "separate") and "adventure" (an exciting or risky experience). This combination likely resulted from a data processing error where two separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words with their individual meanings and contexts.',
            'pronunciation': '/ˈsɛpərədˌvɛntʃər/',
            'etymology': 'Error combination of Latin separatus (separate) + Latin adventura (adventure)',
            'memory_tip': 'This is a combined word error - look for the separation between separ and adventure.',
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
        'september': {
            'word': 'september',
            'definition': 'The ninth month of the Gregorian calendar, containing 30 days and marking the transition from summer to autumn in the Northern Hemisphere. September is characterized by the autumnal equinox, when day and night hours are approximately equal, and by the beginning of the academic year in many educational systems. The month is associated with harvest seasons, changing foliage colors, and cooler temperatures in temperate climates. Many cultures celebrate harvest festivals during September, and it marks important astronomical events related to seasonal changes. In the Southern Hemisphere, September represents the beginning of spring. The month has cultural significance for education, with many schools and universities beginning their academic years. Weather patterns in September often feature crisp mornings, warm afternoons, and the first hints of winter\'s approach.',
            'pronunciation': '/sɛpˈtɛmbər/',
            'etymology': 'From Latin September, from septem meaning seven, as it was the seventh month in the original Roman calendar.',
            'memory_tip': 'Think "SEPT-EMBER" - originally the seventh (sept) month when autumn embers begin.',
            'example_sentence': 'The leaves began changing colors in early _____, signaling the arrival of autumn.',
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
        'septennial': {
            'word': 'septennial',
            'definition': 'Occurring every seven years or lasting for seven years; relating to a period or cycle of seven years. The term is used to describe events, celebrations, or administrative periods that follow seven-year intervals. In some governmental or organizational contexts, septennial elections or reviews occur on seven-year cycles. Academic sabbaticals, certain religious observances, and some agricultural practices may follow septennial patterns. The concept relates to various cultural and religious traditions that recognize seven-year cycles as significant, such as biblical sabbatical years or traditional land management practices. In historical contexts, some institutions operated on septennial terms for leadership positions or policy reviews. The seven-year cycle appears in various fields including economics, where some business cycles are observed to follow roughly septennial patterns, though this is not universally consistent.',
            'pronunciation': '/sɛpˈtɛniəl/',
            'etymology': 'From Latin septennis meaning of seven years, from septem (seven) + annus (year) + -al suffix.',
            'memory_tip': 'Think "SEPT-ENNIAL" - happening every seven (sept) years annually.',
            'example_sentence': 'The university conducted its _____ review of academic programs and policies.',
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
        'septum': {
            'word': 'septum',
            'definition': 'A wall or partition that divides a cavity or structure into separate compartments, particularly in anatomical contexts. The most commonly known septum is the nasal septum, which separates the two nostrils and consists of cartilage and bone covered by mucous membrane. In cardiology, the atrial septum separates the heart\'s two atria, while the ventricular septum separates the two ventricles. Defects in heart septa can cause serious medical conditions requiring surgical repair. Botanical structures also contain septa, such as the walls dividing seed chambers in fruits. In microbiology, septa divide fungal cells and bacterial cells during division. Medical procedures sometimes involve septoplasty to correct deviated nasal septa or repair septal defects. The integrity and proper formation of septa are crucial for normal organ function in many biological systems.',
            'pronunciation': '/ˈsɛptəm/',
            'etymology': 'From Latin septum meaning partition or enclosure, from sepire meaning to enclose.',
            'memory_tip': 'Think "SEPT-UM" - a structure that separates (sept) one space from another.',
            'example_sentence': 'The doctor explained that the deviated nasal _____ was causing breathing difficulties.',
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
        'sepulchral': {
            'word': 'sepulchral',
            'definition': 'Relating to burial, tombs, or the grave; having a gloomy, somber, or deathly character reminiscent of burial places. The term describes anything that evokes the atmosphere of a tomb or cemetery, including sounds, voices, or environments that seem ghostly, hollow, or eerily quiet. Sepulchral voices are often described as deep, echoing, and mournful, as if coming from beyond the grave. Architecture, art, or literature might be called sepulchral if they convey themes of death, mortality, or have a particularly grave and solemn quality. The word can describe physical characteristics of actual burial sites, including sepulchral monuments, inscriptions, or chambers. In broader usage, it characterizes anything that creates an atmosphere of death, mourning, or supernatural eeriness.',
            'pronunciation': '/sɪˈpʌlkrəl/',
            'etymology': 'From Latin sepulcralis meaning of burial, from sepulcrum meaning tomb or grave.',
            'memory_tip': 'Think "SEP-ULCHRAL" - relating to sepulchers (tombs), having a grave-like quality.',
            'example_sentence': 'His _____ voice echoed through the empty cathedral like a voice from the grave.',
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
        'sepulchralsangfroid': {
            'word': 'sepulchralsangfroid',
            'definition': '[COMBINED WORD ERROR] This appears to be two words combined: "sepulchral" (relating to burial or having a deathly character) and "sangfroid" (composure or coolness under pressure). This combination likely resulted from a data processing error where two separate dictionary entries were merged without proper spacing. The correct format should separate these as distinct words with their individual meanings and contexts.',
            'pronunciation': '/sɪˈpʌlkrəlˈsæŋfrwɑː/',
            'etymology': 'Error combination of Latin sepulcralis (sepulchral) + French sang-froid (cold blood)',
            'memory_tip': 'This is a combined word error - look for the separation between sepulchral and sangfroid.',
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
        'sequel': {
            'word': 'sequel',
            'definition': 'A published, broadcast, or recorded work that continues the story or develops the theme of an earlier work, typically featuring the same characters or setting at a later time. Sequels are common in literature, film, television, and video games, where successful original works generate demand for continuation of their stories. A sequel generally assumes audience familiarity with the original work and builds upon its established narrative, characters, and world-building. The quality and reception of sequels vary widely, with some surpassing their predecessors while others fail to capture the original\'s appeal. In broader usage, sequel can refer to any event or situation that follows and is connected to a previous occurrence. The term emphasizes continuity and progression from earlier events or works, whether fictional or real.',
            'pronunciation': '/ˈsiːkwəl/',
            'etymology': 'From Latin sequela meaning that which follows, from sequi meaning to follow.',
            'memory_tip': 'Think "SE-QUEL" - what follows in sequence after the original story.',
            'example_sentence': 'The movie\'s _____ was even more successful than the original film.',
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
        'sequential': {
            'word': 'sequential',
            'definition': 'Following in logical order or succession; arranged or occurring in a specific sequence where each element follows the previous one according to a particular pattern or system. Sequential processes require completion of one step before proceeding to the next, creating ordered progressions that depend on proper sequencing for successful outcomes. In education, sequential learning involves mastering concepts in a specific order where later skills build upon earlier foundations. Computer programming uses sequential execution where instructions are performed one after another in predetermined order. Manufacturing processes often follow sequential assembly lines where each station completes specific tasks before passing products to the next stage. Sequential organization is fundamental to many systems including numerical ordering, alphabetical arrangements, chronological timelines, and procedural instructions. The concept emphasizes the importance of order and dependency relationships between elements.',
            'pronunciation': '/sɪˈkwɛnʃəl/',
            'etymology': 'From sequence + -ial suffix, where sequence comes from Latin sequentia meaning following.',
            'memory_tip': 'Think "SEQU-ENTIAL" - following in sequence, one after another in order.',
            'example_sentence': 'The software required _____ installation of components in the exact order specified.',
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
        'sequester': {
            'word': 'sequester',
            'definition': 'To isolate, separate, or set apart from others, often for protection, security, or to prevent influence or contamination. In legal contexts, sequestration involves isolating juries from outside influences during deliberations or removing assets from someone\'s control pending legal resolution. Environmental sequestration refers to capturing and storing carbon dioxide or other substances to prevent their release into the atmosphere. Medical sequestration might involve isolating infected patients to prevent disease spread. The term can also mean to hide away or withdraw from society, as when someone sequesters themselves for privacy or concentration. Financial sequestration involves freezing or controlling assets. The word emphasizes the act of separation for specific purposes, whether protective, punitive, or preventative.',
            'pronunciation': '/sɪˈkwɛstər/',
            'etymology': 'From Latin sequestrare meaning to surrender for safekeeping, from sequester meaning mediator.',
            'memory_tip': 'Think "SEQU-ESTER" - to separate and keep in sequence away from others.',
            'example_sentence': 'The judge decided to _____ the jury to prevent them from being influenced by media coverage.',
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
        'sequoia': {
            'word': 'sequoia',
            'definition': 'A genus of massive coniferous trees native to the western United States, known for being among the largest and longest-living trees in the world. The giant sequoia (Sequoiadendron giganteum) and coast redwood (Sequoia sempervirens) are the two main species, both capable of reaching extraordinary heights and living for thousands of years. These trees are found primarily in California, with giant sequoias growing in the Sierra Nevada mountains and coast redwoods along the Pacific coast. Sequoias have thick, fire-resistant bark and can reach heights exceeding 300 feet with trunk diameters of over 30 feet. They play crucial ecological roles in their forest ecosystems and are protected in national and state parks. The trees have cultural significance and represent symbols of longevity, strength, and natural majesty. Their conservation is important for maintaining biodiversity and forest heritage.',
            'pronunciation': '/sɪˈkwɔɪə/',
            'etymology': 'Named after Sequoyah, the Cherokee leader who created the Cherokee writing system.',
            'memory_tip': 'Think "SE-QUOIA" - named after Sequoyah, these trees are like giant sequined giants.',
            'example_sentence': 'The massive _____ tree was estimated to be over 2,000 years old.',
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
        'seraphic': {
            'word': 'seraphic',
            'definition': 'Having the characteristics of a seraph; angelic, pure, or celestial in nature, often describing something or someone that appears blissfully innocent, sublime, or divinely beautiful. Seraphic qualities include otherworldly purity, radiant goodness, and spiritual transcendence that seem to emanate from divine sources. The term is often used to describe facial expressions, voices, or behaviors that convey exceptional innocence, peace, or spiritual elevation. In religious art and literature, seraphic figures are depicted as beings of perfect love and devotion, burning with divine fire. Music, poetry, or other artistic expressions might be called seraphic if they evoke feelings of spiritual uplift or celestial beauty. The word suggests a quality that transcends ordinary human experience and approaches the realm of divine perfection.',
            'pronunciation': '/səˈræfɪk/',
            'etymology': 'From seraph + -ic suffix, where seraph comes from Hebrew saraph meaning burning one, referring to celestial beings.',
            'memory_tip': 'Think "SERAPH-IC" - having the qualities of a seraph (angel), heavenly and pure.',
            'example_sentence': 'The child\'s _____ smile seemed to radiate pure innocence and joy.',
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
        'seraya': {
            'word': 'seraya',
            'definition': 'A type of tropical hardwood tree belonging to the genus Shorea, native to Southeast Asian rainforests, particularly valued for its timber in construction and furniture making. Seraya trees are part of the dipterocarp family and can grow to impressive heights in their natural forest habitats. The wood is prized for its strength, durability, and attractive grain patterns, making it commercially important in the timber industry. Different species of seraya produce wood with varying characteristics, from light-colored varieties to darker, denser types. These trees play important ecological roles in rainforest ecosystems, providing habitat for numerous species and contributing to forest biodiversity. Sustainable harvesting practices are crucial for seraya conservation, as deforestation pressures threaten many dipterocarp forests. The wood has been traditionally used in shipbuilding, construction, and decorative applications throughout Southeast Asia.',
            'pronunciation': '/səˈraɪə/',
            'etymology': 'From Malay seraya, referring to trees in the Shorea genus of the dipterocarp family.',
            'memory_tip': 'Think "SE-RAYA" - a Southeast Asian tree that produces ser-iously good wood.',
            'example_sentence': 'The carpenter chose _____ wood for the cabinet because of its beautiful grain and durability.',
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
        'serenade': {
            'word': 'serenade',
            'definition': 'A piece of music sung or played in the open air, typically by a man at night under the window of the woman he loves, as a romantic gesture. Serenades are traditionally performed as expressions of love, devotion, or courtship, often featuring gentle, melodic compositions that convey tender emotions. The practice has historical roots in European courtship traditions and appears in various cultural contexts worldwide. In classical music, serenades evolved into instrumental compositions for small ensembles, often performed at evening entertainment events. Famous composers like Mozart and Brahms wrote elaborate serenades for orchestras. The term can also refer to the act of performing such music or any romantic musical performance. Modern usage extends to any musical tribute or romantic gesture, whether formal or informal.',
            'pronunciation': '/ˌsɛrəˈneɪd/',
            'etymology': 'From French sérénade, from Italian serenata, from sereno meaning calm or clear, referring to clear evening air.',
            'memory_tip': 'Think "SEREN-ADE" - a serene musical aid for wooing someone romantically.',
            'example_sentence': 'The young man hired mariachi musicians to _____ his girlfriend on her birthday.',
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
        'serenity': {
            'word': 'serenity',
            'definition': 'A state of being calm, peaceful, and untroubled; tranquility of mind and spirit that remains undisturbed by external circumstances or internal conflicts. Serenity represents inner peace that comes from acceptance, wisdom, or spiritual development, often achieved through meditation, personal growth, or philosophical understanding. The concept is central to many religious and philosophical traditions that emphasize the importance of mental equilibrium and emotional balance. Serenity differs from mere quietness in that it implies a deep, stable peace that persists even in challenging situations. Natural environments like peaceful lakes, gardens, or mountains are often described as having a serene quality that promotes feelings of serenity in observers. The pursuit of serenity is a common goal in stress management, mental health therapy, and spiritual practices.',
            'pronunciation': '/səˈrɛnəti/',
            'etymology': 'From Latin serenitas meaning clearness or calmness, from serenus meaning clear or calm.',
            'memory_tip': 'Think "SEREN-ITY" - the quality of being serene, calm and peaceful.',
            'example_sentence': 'After years of meditation practice, she found a deep _____ that helped her handle life\'s challenges.',
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
        'series': {
            'word': 'series',
            'definition': 'A sequence of related or similar things, events, or items that follow one another in a particular order or are connected by a common theme. Series can refer to television programs with multiple episodes, book collections with continuing characters or themes, or any systematic arrangement of connected elements. In mathematics, a series is the sum of terms in a sequence, such as arithmetic or geometric series. Scientific research often involves conducting series of experiments to test hypotheses systematically. The term emphasizes the relationship and continuity between individual elements that together form a larger whole. Series can be finite (with a definite end) or infinite (continuing indefinitely), and they may follow specific patterns, rules, or organizing principles that govern their structure and development.',
            'pronunciation': '/ˈsɪriz/',
            'etymology': 'From Latin series meaning row or chain, from serere meaning to join or connect.',
            'memory_tip': 'Think "SER-IES" - things that are serious-ly connected in sequence.',
            'example_sentence': 'The documentary _____ explored different aspects of climate change over twelve episodes.',
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
        'serin': {
            'word': 'serin',
            'definition': 'A small songbird belonging to the finch family (Fringillidae), characterized by a compact build, seed-eating habits, and often bright yellow or greenish plumage. Serins are found primarily in Europe, Africa, and Asia, inhabiting various environments from forests and gardens to open woodlands and scrublands. These birds feed mainly on seeds, buds, and small insects, using their specialized beaks to crack open seed hulls. Many serin species are known for their melodious songs and are popular among birdwatchers and avian enthusiasts. The European serin (Serinus serinus) is one of the most widely distributed species and has adapted well to urban and suburban environments. Serins typically build cup-shaped nests in trees or shrubs and may have multiple broods during breeding season. Their bright plumage and cheerful songs make them welcome additions to gardens and parks.',
            'pronunciation': '/ˈsɛrɪn/',
            'etymology': 'From French serin, possibly from Provençal serena referring to the canary or related finch.',
            'memory_tip': 'Think "SER-IN" - a small bird that\'s serious about eating seeds in gardens.',
            'example_sentence': 'The bright yellow _____ perched on the sunflower stalk, feeding on the seeds.',
            'part_of_speech': 'noun',
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
    
    print(f"\nBatch 157 processing complete!")
    print(f"Successfully processed {len(processed_words)}/{len(words)} words")
    print(f"Output saved to: {output_file}")
    
    if combined_errors:
        print(f"\nCombined word errors detected: {len(combined_errors)}")
        for error in combined_errors:
            print(f"  - {error}")

if __name__ == "__main__":
    process_batch()