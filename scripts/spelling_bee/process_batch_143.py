import csv
import re

class DifficultyCalculator:
    def calculate_difficulty_score(self, word, pronunciation, etymology):
        """Calculate 4-factor difficulty score"""
        
        # Factor 1: Phonetic Transparency (1-10)
        phonetic_score = self._calculate_phonetic_transparency(word, pronunciation)
        
        # Factor 2: Word Frequency (1-10) 
        frequency_score = self._calculate_word_frequency(word)
        
        # Factor 3: Morphological Complexity (1-10)
        morphological_score = self._calculate_morphological_complexity(word)
        
        # Factor 4: Etymology Complexity (1-10)
        etymology_score = self._calculate_etymology_complexity(etymology)
        
        # Total score (4-40)
        total_score = phonetic_score + frequency_score + morphological_score + etymology_score
        
        return {
            'phonetic_transparency_score': phonetic_score,
            'word_frequency_score': frequency_score,
            'morphological_complexity_score': morphological_score,
            'etymology_complexity_score': etymology_score,
            'total_difficulty_score': total_score
        }
    
    def _calculate_phonetic_transparency(self, word, pronunciation):
        """Score 1-10: How well spelling matches pronunciation"""
        if not pronunciation:
            return 5
        
        # Count irregular patterns
        irregular_patterns = 0
        
        # Silent letters and irregular patterns
        if re.search(r'[bt](?![aeiou])|[kl](?=n)|[w](?=r)|[h](?=[^aeiou])|[p](?=s)|[pt](?=[^aeiou])|[gh]|[qu]|[ueue]', word.lower()):
            irregular_patterns += 1
            
        # Double letters not in pronunciation
        if re.search(r'(.)\1', word) and 'double' not in pronunciation.lower():
            irregular_patterns += 1
            
        # Foreign/irregular patterns
        if any(pattern in word.lower() for pattern in ['qu', 'x', 'ue', 'oi', 'eau']):
            irregular_patterns += 1
            
        # Score inversely related to irregular patterns
        return min(10, max(1, 8 - irregular_patterns * 2))
    
    def _calculate_word_frequency(self, word):
        """Score 1-10: How common the word is (lower = more common)"""
        # Common words (1-3)
        common = ['questions', 'quiet', 'quiz', 'quart', 'queue', 'quarantine', 'quarry']
        if word.lower() in common:
            return 2
            
        # Moderately common (4-6)
        moderate = ['quantity', 'quality', 'quotation', 'quotient', 'quirky', 'quicken']
        if word.lower() in moderate:
            return 5
            
        # Specialized/rare (7-10)
        return 8
    
    def _calculate_morphological_complexity(self, word):
        """Score 1-10: Complexity of word structure"""
        complexity = 1
        
        # Add points for length
        if len(word) > 15:
            complexity += 4
        elif len(word) > 12:
            complexity += 3
        elif len(word) > 8:
            complexity += 2
        elif len(word) > 6:
            complexity += 1
            
        # Add points for prefixes/suffixes
        prefixes = ['qu', 'qua', 'que', 'qui', 'quo', 'rab']
        suffixes = ['ous', 'ity', 'ive', 'ment', 'tion', 'ic', 'ary', 'ence', 'ent', 'ed', 'ing', 'ly', 'ism', 'ist', 'er', 'eer', 'ful', 'ical']
        
        for prefix in prefixes:
            if word.lower().startswith(prefix):
                complexity += 1
                break
                
        for suffix in suffixes:
            if word.lower().endswith(suffix):
                complexity += 1
                break
        
        return min(10, complexity)
    
    def _calculate_etymology_complexity(self, etymology):
        """Score 1-10: Complexity of word origins"""
        if not etymology:
            return 5
            
        complexity = 3  # Base score
        
        # Multiple language origins increase complexity
        languages = ['latin', 'greek', 'french', 'spanish', 'italian', 'german', 'sanskrit', 'old english', 'arabic', 'hebrew', 'old french', 'middle english']
        language_count = sum(1 for lang in languages if lang in etymology.lower())
        
        if language_count >= 2:
            complexity += 3
        elif language_count == 1:
            complexity += 1
            
        # Ancient origins add complexity
        if any(ancient in etymology.lower() for ancient in ['ancient', 'classical', 'medieval']):
            complexity += 2
            
        return min(10, complexity)

# Comprehensive word data for batch 143
word_data = {
    'quantify': {
        'definition': 'To express or measure the quantity of something; to determine, express, or measure the amount or number of something. Quantification is essential in science, mathematics, and research for making precise comparisons and drawing meaningful conclusions from data.',
        'pronunciation': '/ˈkwɑːntəˌfaɪ/',
        'pronunciation_respelling': 'KWON-tuh-fy',
        'etymology': 'From Latin "quantus" meaning "how much" + suffix "-ify" (to make).',
        'memory_tip': 'Think "quantity" + "ify" = to make into measurable quantities.',
        'example_sentence': 'Scientists worked to ___ the environmental impact of the new industrial process.',
        'source': 'Claude'
    },
    'quantifyredemption': {
        'definition': '[COMBINED WORD ERROR] This appears to be "quantify" + "redemption" incorrectly joined. Should be separated into two distinct words: "quantify" (to measure) and "redemption" (the act of redeeming or saving).',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "quantify" (Latin: how much) with "redemption" (Latin: buying back).',
        'memory_tip': '[ERROR] This should be split into "quantify" (measure) and "redemption" (saving).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "quantify" and "redemption."',
        'source': 'Claude'
    },
    'quaoar': {
        'definition': 'A large object in the Kuiper Belt beyond Neptune, classified as a dwarf planet candidate; discovered in 2002 and named after a creation deity of the Tongva people. Quaoar is one of the largest known objects in the outer solar system and provides insights into planetary formation.',
        'pronunciation': '/ˈkwɑːwɑːr/',
        'pronunciation_respelling': 'KWAH-war',
        'etymology': 'Named after Quaoar, the creation deity in Tongva mythology.',
        'memory_tip': 'Think "qua" (water) + "oar" = distant icy object you\'d need an oar to reach.',
        'example_sentence': 'Astronomers studied ___ to learn about the formation of our solar system.',
        'source': 'Claude'
    },
    'quarantine': {
        'definition': 'A period of isolation imposed on people, animals, or things that may have been exposed to a contagious disease; to isolate in such a manner. Quarantine prevents the spread of disease by restricting movement until it\'s determined whether infection has occurred.',
        'pronunciation': '/ˈkwɔːrəntiːn/',
        'pronunciation_respelling': 'KWOR-un-teen',
        'etymology': 'From Italian "quaranta" meaning "forty," referring to the 40-day isolation period.',
        'memory_tip': 'Think "quaranta" (forty) + "ine" = forty days of isolation.',
        'example_sentence': 'Travelers had to ___ for two weeks before entering the country.',
        'source': 'Claude'
    },
    'quarry': {
        'definition': 'An open excavation from which stone, sand, or minerals are extracted; the object of a hunt or pursuit; to extract from a quarry. Quarries provide essential building materials while quarry as prey refers to something being hunted or pursued.',
        'pronunciation': '/ˈkwɛri/',
        'pronunciation_respelling': 'KWER-ee',
        'etymology': 'From Old French "quarriere," from Latin "quadraria" (place where stones are squared).',
        'memory_tip': 'Think "square" stones extracted from a "quarry" pit.',
        'example_sentence': 'The limestone ___ provided materials for the cathedral\'s construction.',
        'source': 'Claude'
    },
    'quart': {
        'definition': 'A unit of liquid measure equal to one quarter of a gallon or two pints; a container holding this amount. The quart is commonly used in cooking and for measuring liquids in countries using the imperial measurement system.',
        'pronunciation': '/kwɔːrt/',
        'pronunciation_respelling': 'KWORT',
        'etymology': 'From Old French "quarte," from Latin "quartus" meaning "fourth."',
        'memory_tip': 'Think "quarter" of a gallon = quart.',
        'example_sentence': 'The recipe called for one ___ of milk and two cups of flour.',
        'source': 'Claude'
    },
    'quasar': {
        'definition': 'An extremely bright and distant celestial object powered by a supermassive black hole; among the most luminous objects in the universe. Quasars emit enormous amounts of energy and help scientists study the early universe and galaxy formation.',
        'pronunciation': '/ˈkweɪzɑːr/',
        'pronunciation_respelling': 'KWAY-zar',
        'etymology': 'Acronym from "quasi-stellar radio source," coined in the 1960s.',
        'memory_tip': 'Think "quasi" (almost) + "star" = almost like a star but much brighter.',
        'example_sentence': 'The ___ was so distant that its light had traveled billions of years to reach Earth.',
        'source': 'Claude'
    },
    'quasimodo': {
        'definition': 'The hunchbacked bell-ringer character from Victor Hugo\'s novel "The Hunchback of Notre-Dame"; used to describe someone with a hunchback. The character has become an iconic figure in literature representing both physical deformity and inner goodness.',
        'pronunciation': '/ˌkwæzɪˈmoʊdoʊ/',
        'pronunciation_respelling': 'kwaz-ih-MOH-doh',
        'etymology': 'From Latin "quasi modo," meaning "in the manner of," from the opening words of a Latin hymn.',
        'memory_tip': 'Think of the famous hunchback character from Notre-Dame cathedral.',
        'example_sentence': 'The actor\'s portrayal of ___ brought both pathos and dignity to the character.',
        'source': 'Claude'
    },
    'quatrains': {
        'definition': 'Plural of quatrain; stanzas or poems consisting of four lines, often with a specific rhyme scheme. Quatrains are fundamental building blocks of poetry, appearing in sonnets, ballads, and many other verse forms across different cultures and languages.',
        'pronunciation': '/ˈkwɑːtreɪnz/',
        'pronunciation_respelling': 'KWAH-traynz',
        'etymology': 'From French "quatrain," from "quatre" meaning "four."',
        'memory_tip': 'Think "quatre" (four) + "ains" = four-line poetry stanzas.',
        'example_sentence': 'The poem consisted of six ___ with alternating rhyme schemes.',
        'source': 'Claude'
    },
    'quatrefoil': {
        'definition': 'A decorative design consisting of four lobes or leaves arranged around a common center; common in Gothic architecture and decorative arts. Quatrefoils appear in windows, stonework, and ornamental designs, symbolizing the four evangelists or the cross.',
        'pronunciation': '/ˈkɑːtrəfɔɪl/',
        'pronunciation_respelling': 'KAH-truh-foyl',
        'etymology': 'From French "quatre" (four) + "feuille" (leaf).',
        'memory_tip': 'Think "quatre" (four) + "foil" (leaf) = four-leaf design.',
        'example_sentence': 'The cathedral window featured an elegant ___ design in stained glass.',
        'source': 'Claude'
    },
    'quattrocento': {
        'definition': 'The 15th century in Italian art and culture, particularly the early Renaissance period; literally meaning "four hundred" in Italian. The Quattrocento saw revolutionary developments in art, architecture, and humanism, with masters like Donatello and Brunelleschi.',
        'pronunciation': '/ˌkwɑːtroʊˈtʃɛntoʊ/',
        'pronunciation_respelling': 'kwah-troh-CHEN-toh',
        'etymology': 'Italian, meaning "four hundred," referring to the 1400s.',
        'memory_tip': 'Think "quattro" (four) + "cento" (hundred) = the 1400s in Italian art.',
        'example_sentence': 'Renaissance art reached new heights during the ___ period in Florence.',
        'source': 'Claude'
    },
    'quaver': {
        'definition': 'To shake or tremble in speaking, typically from nervousness or emotion; in music, an eighth note; to speak in a trembling voice. Quavering indicates instability whether in voice, emotion, or musical timing.',
        'pronunciation': '/ˈkweɪvər/',
        'pronunciation_respelling': 'KWAY-vur',
        'etymology': 'From Middle English "quaveren," possibly related to "quake."',
        'memory_tip': 'Think "quake" + "waver" = voice shaking and wavering.',
        'example_sentence': 'Her voice began to ___ as she delivered the emotional speech.',
        'source': 'Claude'
    },
    'querida': {
        'definition': 'Spanish term of endearment meaning "beloved" or "dear one," typically used for a female; can also refer to a mistress or lover. The word conveys affection and intimacy in Spanish-speaking cultures.',
        'pronunciation': '/keˈriða/',
        'pronunciation_respelling': 'keh-REE-thah',
        'etymology': 'From Spanish "querida," feminine of "querido," from "querer" (to love).',
        'memory_tip': 'Think "query" + "dear" = questioning who your dear one is.',
        'example_sentence': 'He whispered "___ mía" as he embraced his beloved wife.',
        'source': 'Claude'
    },
    'querulous': {
        'definition': 'Complaining in a petulant or whining manner; habitually faultfinding or argumentative. Querulous behavior involves persistent complaining and dissatisfaction, often about trivial matters, making interactions difficult and unpleasant.',
        'pronunciation': '/ˈkwɛrələs/',
        'pronunciation_respelling': 'KWER-uh-lus',
        'etymology': 'From Latin "querulosus," from "queri" meaning "to complain."',
        'memory_tip': 'Think "query" + "lous" (lousy) = constantly querying/complaining about lousy things.',
        'example_sentence': 'The ___ customer complained about every aspect of the service.',
        'source': 'Claude'
    },
    'questionaire': {
        'definition': 'Misspelling of questionnaire; this represents a common error where the second "n" is omitted. The correct spelling is "questionnaire" (a set of printed or written questions used for obtaining information from respondents).',
        'pronunciation': '[MISSPELLING]',
        'pronunciation_respelling': '[MISSPELLING - should be KWES-chun-air]',
        'etymology': '[MISSPELLING] Incorrect form of "questionnaire" from French.',
        'memory_tip': '[MISSPELLING] Remember: question + naire (with double n) = questionnaire.',
        'example_sentence': '[MISSPELLING] The correct spelling is "questionnaire" for a set of survey questions.',
        'source': 'Claude'
    },
    'questionnaire': {
        'definition': 'A set of printed or written questions with a choice of answers, devised for a survey or statistical study; a form containing such questions. Questionnaires are essential tools for research, market analysis, and data collection in various fields.',
        'pronunciation': '/ˌkwɛstʃəˈnɛr/',
        'pronunciation_respelling': 'kwes-chuh-NAIR',
        'etymology': 'From French "questionnaire," from "question" + suffix "-aire."',
        'memory_tip': 'Think "question" + "naire" (French ending) = list of questions.',
        'example_sentence': 'Researchers distributed a ___ to gather data about consumer preferences.',
        'source': 'Claude'
    },
    'questions': {
        'definition': 'Plural of question; sentences or phrases that seek information, clarification, or responses; matters requiring investigation or discussion. Questions drive learning, research, and communication by prompting thought and eliciting information.',
        'pronunciation': '/ˈkwɛstʃənz/',
        'pronunciation_respelling': 'KWES-chunz',
        'etymology': 'Plural of "question," from Latin "quaestio," from "quaerere" (to seek).',
        'memory_tip': 'Think "quest" + "ions" = seeking information through inquiry.',
        'example_sentence': 'The students asked thoughtful ___ about the complex scientific phenomenon.',
        'source': 'Claude'
    },
    'queue': {
        'definition': 'A line of people or vehicles waiting their turn; in computing, a data structure where items are processed in first-in, first-out order; to form or wait in a line. Queues organize waiting and processing in orderly, fair sequences.',
        'pronunciation': '/kjuː/',
        'pronunciation_respelling': 'KYOO',
        'etymology': 'From French "queue," meaning "tail," from Latin "cauda."',
        'memory_tip': 'Think of a tail-like line of people waiting = queue.',
        'example_sentence': 'Customers formed a long ___ outside the popular restaurant.',
        'source': 'Claude'
    },
    'quicken': {
        'definition': 'To make or become faster; to stimulate or accelerate; to come to life or become animated. Quickening can refer to physical speed, emotional intensity, or the first movements of a fetus felt by a pregnant woman.',
        'pronunciation': '/ˈkwɪkən/',
        'pronunciation_respelling': 'KWIK-un',
        'etymology': 'From "quick" + suffix "-en," from Old English "cwic" (alive).',
        'memory_tip': 'Think "quick" + "en" = to make something quick/alive.',
        'example_sentence': 'His pulse began to ___ as he approached the finish line.',
        'source': 'Claude'
    },
    'quid': {
        'definition': 'British slang for a pound sterling; something chewed but not swallowed, like tobacco; the essential nature of something. In different contexts, quid can refer to money, chewing material, or philosophical essence.',
        'pronunciation': '/kwɪd/',
        'pronunciation_respelling': 'KWID',
        'etymology': 'From Latin "quid," meaning "what" or "something."',
        'memory_tip': 'Think "quick" + "id" = quick money or something to chew.',
        'example_sentence': 'The souvenir cost twenty ___ at the London market.',
        'source': 'Claude'
    },
    'quiddity': {
        'definition': 'The essential nature or quality of something; a trifling distinction or quibble; the inherent nature that makes something what it is. In philosophy, quiddity refers to the essence that defines an object\'s identity.',
        'pronunciation': '/ˈkwɪdəti/',
        'pronunciation_respelling': 'KWID-ih-tee',
        'etymology': 'From Latin "quidditas," from "quid" meaning "what."',
        'memory_tip': 'Think "quid" (what) + "ity" = the what-ness or essence of things.',
        'example_sentence': 'Philosophers debated the ___ of consciousness and human identity.',
        'source': 'Claude'
    },
    'quidnunc': {
        'definition': 'A person who is eager to know the latest news and gossip; a busybody or inquisitive person. Quidnuncs are characterized by their insatiable curiosity about others\' affairs and their tendency to spread information.',
        'pronunciation': '/ˈkwɪdnʌŋk/',
        'pronunciation_respelling': 'KWID-nunk',
        'etymology': 'From Latin "quid nunc," meaning "what now?"',
        'memory_tip': 'Think "quid" (what) + "nunc" (now) = always asking "what now?" about news.',
        'example_sentence': 'The neighborhood ___ knew everyone\'s business before they did themselves.',
        'source': 'Claude'
    },
    'quiet': {
        'definition': 'Making little or no noise; peaceful and calm; not speaking much; to make or become silent. Quiet describes states of reduced sound, activity, or agitation, providing rest and contemplation.',
        'pronunciation': '/ˈkwaɪət/',
        'pronunciation_respelling': 'KWY-ut',
        'etymology': 'From Latin "quietus," meaning "at rest" or "calm."',
        'memory_tip': 'Think of peace and stillness = quiet atmosphere.',
        'example_sentence': 'The library maintained a ___ environment for studying and reading.',
        'source': 'Claude'
    },
    'quill': {
        'definition': 'A large feather from a bird\'s wing or tail, especially one used as a pen; the hollow shaft of a feather; a spine of a porcupine. Quills were essential writing instruments before modern pens and represent literary tradition.',
        'pronunciation': '/kwɪl/',
        'pronunciation_respelling': 'KWIL',
        'etymology': 'From Middle English "quille," possibly from Middle Low German.',
        'memory_tip': 'Think of a feather pen that authors would use to write = quill.',
        'example_sentence': 'The author dipped his ___ in ink to write the manuscript.',
        'source': 'Claude'
    },
    'quinary': {
        'definition': 'Based on or consisting of five; relating to a number system with five as its base; arranged in groups of five. Quinary systems appear in mathematics, biology, and ancient counting methods.',
        'pronunciation': '/ˈkwaɪnəri/',
        'pronunciation_respelling': 'KWY-nuh-ree',
        'etymology': 'From Latin "quinarius," from "quini" meaning "five each."',
        'memory_tip': 'Think "quin" (five) + "ary" = relating to groups of five.',
        'example_sentence': 'Some ancient cultures used a ___ counting system based on fingers of one hand.',
        'source': 'Claude'
    },
    'quinaryafroth': {
        'definition': '[COMBINED WORD ERROR] This appears to be "quinary" + "afroth" incorrectly joined. Should be separated into two distinct words: "quinary" (based on five) and "afroth" (foaming or frothy).',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "quinary" (Latin: five) with "afroth" (frothy).',
        'memory_tip': '[ERROR] This should be split into "quinary" (five-based) and "afroth" (foamy).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "quinary" and "afroth."',
        'source': 'Claude'
    },
    'quince': {
        'definition': 'A hard, golden-yellow fruit with a strong fragrance, used for making preserves and jellies; the tree that bears this fruit. Quinces are related to apples and pears but are too astringent to eat raw, requiring cooking to become palatable.',
        'pronunciation': '/kwɪns/',
        'pronunciation_respelling': 'KWINS',
        'etymology': 'From Middle English, from Old French "cooin," from Latin "cydonium."',
        'memory_tip': 'Think "queen" + "ce" = the queen of golden fruits for preserves.',
        'example_sentence': 'Grandmother made delicious ___ jelly from the fruit trees in her orchard.',
        'source': 'Claude'
    },
    'quintessential': {
        'definition': 'Representing the most perfect or typical example of a quality or class; being the most essential aspect of something. Quintessential describes the purest, most concentrated form that perfectly embodies the essential characteristics.',
        'pronunciation': '/ˌkwɪntəˈsɛnʃəl/',
        'pronunciation_respelling': 'kwin-tuh-SEN-shul',
        'etymology': 'From "quintessence," from Latin "quinta essentia" (fifth essence).',
        'memory_tip': 'Think "quint" (five) + "essential" = the fifth and most essential element.',
        'example_sentence': 'The cottage was the ___ English countryside home with roses and thatched roof.',
        'source': 'Claude'
    },
    'quip': {
        'definition': 'A witty remark or comment; a clever saying or joke; to make such a remark. Quips are characterized by their brevity, cleverness, and often spontaneous nature, adding humor to conversations.',
        'pronunciation': '/kwɪp/',
        'pronunciation_respelling': 'KWIP',
        'etymology': 'From Latin "quippe," meaning "indeed" or "to be sure."',
        'memory_tip': 'Think "quick" + "zip" = a quick, zippy witty comment.',
        'example_sentence': 'His clever ___ about the weather lightened the mood at the meeting.',
        'source': 'Claude'
    },
    'quirky': {
        'definition': 'Having unusual or unexpected traits; characterized by peculiar or unconventional behavior; having an appeal that comes from being unusual or different. Quirky suggests charming eccentricity rather than problematic oddness.',
        'pronunciation': '/ˈkwɜːrki/',
        'pronunciation_respelling': 'KWUR-kee',
        'etymology': 'From "quirk" + suffix "-y," from earlier "querk" meaning "twist."',
        'memory_tip': 'Think "quirk" + "y" = full of unusual but charming quirks.',
        'example_sentence': 'The café\'s ___ décor included mismatched furniture and vintage typewriters.',
        'source': 'Claude'
    },
    'quirt': {
        'definition': 'A type of riding whip with a short handle and a lash of braided leather; used by horseback riders, especially in the American West. Quirts are designed for control and communication with horses rather than punishment.',
        'pronunciation': '/kwɜːrt/',
        'pronunciation_respelling': 'KWURT',
        'etymology': 'From Spanish "cuarta," possibly from "cuarto" meaning "fourth."',
        'memory_tip': 'Think "quirk" + "t" = a quirky twisted leather riding whip.',
        'example_sentence': 'The cowboy carried a well-worn ___ attached to his saddle.',
        'source': 'Claude'
    },
    'quito': {
        'definition': 'The capital city of Ecuador, located high in the Andes mountains; one of the highest capital cities in the world at about 9,350 feet above sea level. Quito is known for its well-preserved colonial architecture and historical significance.',
        'pronunciation': '/ˈkiːtoʊ/',
        'pronunciation_respelling': 'KEE-toh',
        'etymology': 'From the indigenous Quitu people who inhabited the area.',
        'memory_tip': 'Think "key" + "toe" = the key city high up where your toes might get cold.',
        'example_sentence': '___ serves as Ecuador\'s political and cultural center in the Andes.',
        'source': 'Claude'
    },
    'quittance': {
        'definition': 'Release from a debt or obligation; a document certifying such release; recompense or repayment. Quittance represents formal acknowledgment that a debt has been satisfied or an obligation fulfilled.',
        'pronunciation': '/ˈkwɪtəns/',
        'pronunciation_respelling': 'KWIT-uns',
        'etymology': 'From Old French "quitance," from "quiter" meaning "to release."',
        'memory_tip': 'Think "quit" + "ance" = quitting/releasing from an obligation.',
        'example_sentence': 'The debtor received a ___ showing that the loan was fully repaid.',
        'source': 'Claude'
    },
    'quixotic': {
        'definition': 'Extremely idealistic and unrealistic; characterized by rash, impractical devotion to high ideals. Named after Don Quixote, the term describes noble but impractical pursuits that ignore practical limitations.',
        'pronunciation': '/kwɪkˈsɒtɪk/',
        'pronunciation_respelling': 'kwik-SOT-ik',
        'etymology': 'From Don Quixote, the idealistic knight created by Cervantes.',
        'memory_tip': 'Think of Don Quixote tilting at windmills = idealistic but impractical.',
        'example_sentence': 'His ___ plan to solve world hunger was admirable but unrealistic.',
        'source': 'Claude'
    },
    'quiz': {
        'definition': 'A brief test or examination; to question someone closely; an informal assessment of knowledge. Quizzes serve as educational tools for testing understanding and encouraging review of material.',
        'pronunciation': '/kwɪz/',
        'pronunciation_respelling': 'KWIZ',
        'etymology': 'Origin uncertain, possibly from Latin "quis" meaning "who."',
        'memory_tip': 'Think "question" shortened = quick test with questions.',
        'example_sentence': 'The teacher gave a surprise ___ on yesterday\'s reading assignment.',
        'source': 'Claude'
    },
    'quizzical': {
        'definition': 'Showing mild or amused puzzlement; indicating doubt or questioning in a teasing way; gently mocking or questioning. A quizzical expression suggests curiosity mixed with slight confusion or humor.',
        'pronunciation': '/ˈkwɪzɪkəl/',
        'pronunciation_respelling': 'KWIZ-ih-kul',
        'etymology': 'From "quiz" + suffix "-ical," meaning "of or relating to questioning."',
        'memory_tip': 'Think "quiz" + "ical" = having the nature of gentle questioning.',
        'example_sentence': 'She gave him a ___ look when he claimed he could speak fluent Mandarin.',
        'source': 'Claude'
    },
    'quoi': {
        'definition': 'French word meaning "what"; used in French phrases and expressions that have entered English usage. "Quoi" appears in expressions like "je ne sais quoi" (I don\'t know what) to indicate an indefinable quality.',
        'pronunciation': '/kwɑː/',
        'pronunciation_respelling': 'KWAH',
        'etymology': 'From French "quoi," from Latin "quid" meaning "what."',
        'memory_tip': 'Think French "what" = quoi, as in "je ne sais quoi."',
        'example_sentence': 'The restaurant had a certain je ne sais ___ that made it special.',
        'source': 'Claude'
    },
    'quoijerboa': {
        'definition': '[COMBINED WORD ERROR] This appears to be "quoi" + "jerboa" incorrectly joined. Should be separated into two distinct words: "quoi" (French for "what") and "jerboa" (a jumping desert rodent).',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "quoi" (French: what) with "jerboa" (Arabic: jumping rodent).',
        'memory_tip': '[ERROR] This should be split into "quoi" (French what) and "jerboa" (desert rodent).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "quoi" and "jerboa."',
        'source': 'Claude'
    },
    'quokka': {
        'definition': 'A small marsupial native to Australia, known for its friendly appearance and seeming smile; often called the world\'s happiest animal. Quokkas have become popular on social media due to their photogenic, cheerful expressions.',
        'pronunciation': '/ˈkwɒkə/',
        'pronunciation_respelling': 'KWOK-uh',
        'etymology': 'From Nyungar Aboriginal language "gwaga."',
        'memory_tip': 'Think "quack" + "a" = the smiling marsupial that\'s almost as happy as a duck.',
        'example_sentence': 'Tourists flocked to Rottnest Island to take selfies with the friendly ___.',
        'source': 'Claude'
    },
    'quonk': {
        'definition': 'The sound made by a Canada goose; an onomatopoeia representing the distinctive honking call of geese. Quonk captures the harsh, resonant quality of goose vocalizations during flight or communication.',
        'pronunciation': '/kwɒŋk/',
        'pronunciation_respelling': 'KWONK',
        'etymology': 'Onomatopoeia representing the sound made by geese.',
        'memory_tip': 'Think of the sound a goose makes = quonk, quonk.',
        'example_sentence': 'The geese\'s loud ___ echoed across the lake as they prepared to migrate.',
        'source': 'Claude'
    },
    'quonset': {
        'definition': 'A type of prefabricated building with a semicircular roof of corrugated metal; originally developed for military use during World War II. Quonset huts are characterized by their simple, curved design and ease of assembly.',
        'pronunciation': '/ˈkwɒnsət/',
        'pronunciation_respelling': 'KWON-sut',
        'etymology': 'Named after Quonset Point, Rhode Island, where they were first manufactured.',
        'memory_tip': 'Think "question" + "set" = questioning where to set up these curved military buildings.',
        'example_sentence': 'The military base used ___ huts for temporary housing and storage.',
        'source': 'Claude'
    },
    'quorum': {
        'definition': 'The minimum number of members required to be present for a meeting to conduct business; the necessary attendance for valid proceedings. Quorums ensure that decisions represent sufficient participation and aren\'t made by too few people.',
        'pronunciation': '/ˈkwɔːrəm/',
        'pronunciation_respelling': 'KWOR-um',
        'etymology': 'From Latin "quorum," meaning "of whom," from legal phrase "quorum vos...unum esse volumus."',
        'memory_tip': 'Think "quore" (core) + "um" = the core group needed for meetings.',
        'example_sentence': 'The committee couldn\'t vote because they lacked a ___ of five members.',
        'source': 'Claude'
    },
    'quota': {
        'definition': 'A fixed share or proportion that someone is expected to contribute or receive; a limited quantity allowed or assigned. Quotas can involve production targets, admission limits, or resource allocations.',
        'pronunciation': '/ˈkwoʊtə/',
        'pronunciation_respelling': 'KWOH-tuh',
        'etymology': 'From Latin "quota," meaning "how many" or "what part."',
        'memory_tip': 'Think "quote" + "a" = quoting a specific number or amount.',
        'example_sentence': 'The sales team exceeded their monthly ___ by twenty percent.',
        'source': 'Claude'
    },
    'quotation': {
        'definition': 'A group of words taken from a text or speech and repeated by someone other than the original author; a formal statement of the cost of goods or services; the action of quoting. Quotations preserve and transmit ideas across time and contexts.',
        'pronunciation': '/kwoʊˈteɪʃən/',
        'pronunciation_respelling': 'kwoh-TAY-shun',
        'etymology': 'From "quote" + suffix "-ation," from Latin "quotare" (to mark with numbers).',
        'memory_tip': 'Think "quote" + "ation" = the act of quoting someone\'s words.',
        'example_sentence': 'The speaker began with a famous ___ from Shakespeare\'s Hamlet.',
        'source': 'Claude'
    },
    'quotidian': {
        'definition': 'Belonging to each day; ordinary or commonplace; occurring daily. Quotidian describes the routine, everyday aspects of life that are regular and unremarkable, though not necessarily unimportant.',
        'pronunciation': '/kwoʊˈtɪdiən/',
        'pronunciation_respelling': 'kwoh-TID-ee-un',
        'etymology': 'From Latin "quotidianus," from "quotidie" meaning "daily."',
        'memory_tip': 'Think "quote" + "tidy" + "an" = tidying up the same daily routine.',
        'example_sentence': 'She found beauty in the ___ activities of cooking and gardening.',
        'source': 'Claude'
    },
    'quotient': {
        'definition': 'The result obtained by dividing one number by another; a particular degree or amount of a quality or characteristic. In mathematics, the quotient is the answer to a division problem.',
        'pronunciation': '/ˈkwoʊʃənt/',
        'pronunciation_respelling': 'KWOH-shunt',
        'etymology': 'From Latin "quotiens," meaning "how many times."',
        'memory_tip': 'Think "quote" + "ient" = the amount you get when dividing.',
        'example_sentence': 'The ___ of twenty divided by four equals five.',
        'source': 'Claude'
    },
    'quoties': {
        'definition': 'A Latin term meaning "how many times" or "as often as"; used in legal and academic contexts to indicate frequency or repetition. This formal term appears in scholarly writing and legal documents.',
        'pronunciation': '/ˈkwoʊtiəs/',
        'pronunciation_respelling': 'KWOH-tee-us',
        'etymology': 'From Latin "quoties," meaning "how many times."',
        'memory_tip': 'Think "quote" + "ties" = tying together how many times something occurs.',
        'example_sentence': 'The legal document specified "___ necessary" for court appearances.',
        'source': 'Claude'
    },
    'rabato': {
        'definition': 'A type of wide, stiff collar worn in the 16th and 17th centuries; a fashion accessory that extended around the neck and shoulders. Rabatos were elaborate status symbols made of starched lace or linen.',
        'pronunciation': '/rəˈbɑːtoʊ/',
        'pronunciation_respelling': 'ruh-BAH-toh',
        'etymology': 'From Spanish "rabato," possibly related to "rebatir" (to turn back).',
        'memory_tip': 'Think "rabbit" + "o" = a collar that sticks out like rabbit ears.',
        'example_sentence': 'The portrait showed the nobleman wearing an elaborate lace ___.',
        'source': 'Claude'
    },
    'rabbinic': {
        'definition': 'Relating to rabbis or their teachings, writings, and traditions; characteristic of Jewish rabbinical scholarship and interpretation. Rabbinic literature includes commentaries, legal discussions, and religious interpretations spanning centuries.',
        'pronunciation': '/rəˈbɪnɪk/',
        'pronunciation_respelling': 'ruh-BIN-ik',
        'etymology': 'From "rabbi" + suffix "-ic," from Hebrew "rabbi" meaning "my master."',
        'memory_tip': 'Think "rabbi" + "nic" = relating to rabbis and their teachings.',
        'example_sentence': 'The student spent years studying ___ literature and Jewish law.',
        'source': 'Claude'
    },
    'rabble': {
        'definition': 'A disorderly crowd of people; the common people regarded as lacking refinement or education; a mob. Rabble often implies a chaotic group acting without proper organization or consideration.',
        'pronunciation': '/ˈræbəl/',
        'pronunciation_respelling': 'RAB-ul',
        'etymology': 'From Middle English "rabel," possibly related to "rabble" (to speak rapidly).',
        'memory_tip': 'Think "babble" with "r" = a crowd that babbles and creates disorder.',
        'example_sentence': 'The politician dismissed the protesters as merely an unruly ___.',
        'source': 'Claude'
    }
}

def process_batch_143():
    """Process batch 143 spelling bee words"""
    
    calculator = DifficultyCalculator()
    
    # Read input CSV
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_143_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_143_processed.csv'
    
    processed_words = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            for i, row in enumerate(reader, 1):
                if i > 50:  # Limit to 50 words per batch
                    break
                    
                word = row['word'].strip().lower()
                years = row['years']
                source_files = row['source_files'] 
                source_difficulties = row['source_difficulties']
                
                print(f"Processing word {i}: {word}")
                
                # Get word data
                if word in word_data:
                    data = word_data[word]
                    
                    # Calculate difficulty scores
                    scores = calculator.calculate_difficulty_score(
                        word, 
                        data['pronunciation'], 
                        data['etymology']
                    )
                    
                    processed_word = {
                        'word': word,
                        'definition': data['definition'],
                        'pronunciation': data['pronunciation'],
                        'pronunciation_respelling': data['pronunciation_respelling'],
                        'etymology': data['etymology'],
                        'etymology_source': data['source'],
                        'memory_tip': data['memory_tip'],
                        'example_sentence': data['example_sentence'],
                        'example_sentence_source': data['source'],
                        'years': years,
                        'source_files': source_files,
                        'source_difficulties': source_difficulties,
                        'definition_source': data['source'],
                        'pronunciation_source': data['source'],
                        'phonetic_transparency_score': scores['phonetic_transparency_score'],
                        'word_frequency_score': scores['word_frequency_score'],
                        'morphological_complexity_score': scores['morphological_complexity_score'],
                        'etymology_complexity_score': scores['etymology_complexity_score'],
                        'total_difficulty_score': scores['total_difficulty_score'],
                        'assigned_difficulty': None,  # To be assigned later
                        'audio_file_path': None,
                        'created_at': '2025-01-01',
                        'updated_at': '2025-01-01',
                        'notes': 'Batch 143 processing',
                        'review_status': 'pending',
                        'batch_number': 143
                    }
                    
                    processed_words.append(processed_word)
                else:
                    print(f"Warning: No data found for word '{word}'")
        
        # Write output CSV
        if processed_words:
            fieldnames = [
                'word', 'definition', 'pronunciation', 'pronunciation_respelling', 
                'etymology', 'etymology_source', 'memory_tip', 'example_sentence',
                'example_sentence_source', 'years', 'source_files', 'source_difficulties',
                'definition_source', 'pronunciation_source', 'phonetic_transparency_score',
                'word_frequency_score', 'morphological_complexity_score', 
                'etymology_complexity_score', 'total_difficulty_score', 'assigned_difficulty',
                'audio_file_path', 'created_at', 'updated_at', 'notes', 'review_status', 'batch_number'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(processed_words)
            
            print(f"\nBatch 143 processing complete!")
            print(f"Successfully processed {len(processed_words)}/50 words")
            print(f"Output saved to: {output_file}")
            
            # Flag any combined word errors
            combined_errors = [word for word in processed_words if '[COMBINED WORD ERROR]' in word['definition']]
            if combined_errors:
                print(f"\nCombined word errors detected: {len(combined_errors)}")
                for error in combined_errors:
                    print(f"  - {error['word']}")
        
    except Exception as e:
        print(f"Error processing batch 143: {e}")
        return False
    
    return True

if __name__ == "__main__":
    process_batch_143()