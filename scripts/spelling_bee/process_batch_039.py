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

batch_039_data = {
    'competitivelounge': {
        'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "competitive" (having a strong desire to win) + "lounge" (a comfortable room for relaxing). These should be separate words.',
        'part_of_speech': 'error - combined words',
        'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
        'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
        'memory_tips': 'This is a data error - should be separated into "competitive" and "lounge"',
        'alternate_spellings': 'competitive + lounge (separate words)',
        'language_origin': 'ERROR - combined words',
        'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
    },
    'compilation': {
        'definition': 'The process of collecting and assembling information, data, or materials from various sources into a unified work or collection. In computing, compilation refers to translating source code written in a programming language into machine code or another target language. Musical compilations gather songs from different artists or albums. Academic compilations bring together research, articles, or scholarly works on related topics.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kom-puh-LAY-shun (/ˌkɒmpəˈleɪʃən/)',
        'etymology': 'From Latin "compilatio," from "compilare" (to plunder, collect)',
        'memory_tips': 'Think "compile + -ation" - the act of compiling or gathering things together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The music _____ featured the greatest hits from the 1980s decade.'
    },
    'compiled': {
        'definition': 'Past tense of compile; gathered, collected, or assembled from various sources into a comprehensive whole. In computer programming, compiled refers to source code that has been translated into executable machine code. The term indicates that information, data, or materials have been systematically organized and brought together from different origins to create a unified resource or product.',
        'part_of_speech': 'verb (past tense)',
        'pronunciation_guide': 'kum-PAYLD (/kəmˈpaɪld/)',
        'etymology': 'From Latin "compilare" (to collect, gather together) + past tense suffix "-ed"',
        'memory_tips': 'Think of gathering scattered pieces and putting them together in an organized way',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The researcher _____ data from multiple studies to support her conclusions.'
    },
    'complacency': {
        'definition': 'A feeling of self-satisfaction or contentment, often accompanied by unawareness of potential dangers, problems, or areas needing improvement. Complacency represents a comfortable but potentially harmful state where individuals or organizations become overconfident and cease striving for progress. This attitude can lead to stagnation, missed opportunities, and vulnerability to competitors or changing circumstances.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kum-PLAY-sun-see (/kəmˈpleɪsənsi/)',
        'etymology': 'From Latin "complacentia," from "complacere" (to please greatly)',
        'memory_tips': 'Think "com- (completely) + place (pleased)" - being completely pleased and thus not improving',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The team\'s _____ after their early success led to their eventual defeat.'
    },
    'complacencykraken': {
        'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "complacency" (self-satisfied contentment) + "kraken" (legendary sea monster). These should be separate words.',
        'part_of_speech': 'error - combined words',
        'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
        'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
        'memory_tips': 'This is a data error - should be separated into "complacency" and "kraken"',
        'alternate_spellings': 'complacency + kraken (separate words)',
        'language_origin': 'ERROR - combined words',
        'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
    },
    'complaint': {
        'definition': 'A formal or informal expression of dissatisfaction, criticism, or grievance about a service, product, situation, or behavior. Complaints serve as feedback mechanisms that can lead to improvements and resolution of problems. In legal contexts, a complaint is a formal document initiating a lawsuit. Effective complaint handling is crucial for customer service, organizational improvement, and maintaining positive relationships.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kum-PLAYNT (/kəmˈpleɪnt/)',
        'etymology': 'From Old French "complainte," from Latin "complangere" (to bewail)',
        'memory_tips': 'Think "com- (together) + plain (clear)" - clearly stating what\'s wrong',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'The customer filed a _____ about the defective product with the company\'s service department.'
    },
    'complaints': {
        'definition': 'Plural form of complaint; multiple expressions of dissatisfaction or formal grievances. Complaints data helps organizations identify patterns, improve services, and address systemic issues. In customer service, tracking complaints enables companies to measure satisfaction levels and implement improvements. Legal complaints represent formal allegations in court proceedings requiring official responses.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'kum-PLAYNTS (/kəmˈpleɪnts/)',
        'etymology': 'Plural of Old French "complainte," from Latin "complangere" (to bewail)',
        'memory_tips': 'Multiple people stating what\'s wrong or what they\'re unhappy about',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'The manager reviewed all customer _____ from the previous month to identify improvement areas.'
    },
    'complementary': {
        'definition': 'Serving to complete or enhance each other when combined; mutually supplying each other\'s lack or deficiency. Complementary elements work together harmoniously to create a more effective or complete whole. In medicine, complementary therapies supplement conventional treatments. In color theory, complementary colors are opposite on the color wheel and create visual contrast. The concept emphasizes cooperation and mutual benefit.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kom-pluh-MEN-tuh-ree (/ˌkɒmpləˈmɛntəri/)',
        'etymology': 'From Latin "complementum" (that which completes) + suffix "-ary"',
        'memory_tips': 'Remember "complete" - complementary things complete each other (not "compliment")',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The two software programs had _____ features that worked perfectly together.'
    },
    'complete': {
        'definition': 'Having all necessary parts, elements, or components; finished, entire, or comprehensive. As a verb, complete means to finish or bring to an end successfully. Complete indicates wholeness, thoroughness, or the absence of missing elements. In various contexts, complete can mean total, absolute, or fully accomplished without remaining tasks or components.',
        'part_of_speech': 'adjective, verb',
        'pronunciation_guide': 'kum-PLEET (/kəmˈplit/)',
        'etymology': 'From Latin "completus," past participle of "complere" (to fill up, finish)',
        'memory_tips': 'Think "com- (completely) + plete (filled)" - completely filled or finished',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'She needed one more course to _____ her degree requirements.'
    },
    'completely': {
        'definition': 'In a total, thorough, or absolute manner; entirely without exception or reservation. This adverb emphasizes the full extent or degree of an action, state, or condition. Completely indicates that something is done wholly, utterly, or to the maximum possible extent, leaving nothing incomplete, partial, or unfinished.',
        'part_of_speech': 'adverb',
        'pronunciation_guide': 'kum-PLEET-lee (/kəmˈplitli/)',
        'etymology': 'From Latin "completus" (complete) + adverbial suffix "-ly"',
        'memory_tips': 'Think "complete + -ly" - in a complete way, thoroughly or entirely',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The renovation _____ transformed the old building into a modern workspace.'
    },
    'complicated': {
        'definition': 'Complex, intricate, or difficult to understand due to having many interconnected parts or elements. Complicated situations, problems, or systems require careful analysis and often specialized knowledge to navigate successfully. The term implies confusion, difficulty, or the presence of multiple factors that make simple solutions inadequate. Complicated matters often require step-by-step approaches to resolve.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KOM-pluh-kay-ted (/ˈkɒmpləkeɪtəd/)',
        'etymology': 'From Latin "complicatus," past participle of "complicare" (to fold together)',
        'memory_tips': 'Think "com- (together) + plic (fold)" - folded together in complex ways',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The tax regulations became increasingly _____ with each new amendment.'
    },
    'complicit': {
        'definition': 'Involved in or associated with wrongdoing, illegal activity, or unethical behavior, typically as an accomplice rather than the primary actor. Being complicit implies knowledge of and participation in activities that cause harm or violate laws or moral standards. This involvement may be through action, inaction, or silent approval that enables harmful behavior to continue.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kum-PLIS-it (/kəmˈplɪsɪt/)',
        'etymology': 'From Latin "complicitus," variant of "complicatus" (folded together, involved)',
        'memory_tips': 'Think "com- (together) + plic (folded)" - folded together in wrongdoing',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The investigation revealed that several employees were _____ in the embezzlement scheme.'
    },
    'comportment': {
        'definition': 'Manner of personal conduct; the way a person behaves, especially in terms of manners, bearing, and social conduct. Comportment encompasses posture, speech, dress, and overall demeanor in social and professional situations. Good comportment reflects self-discipline, respect for others, and awareness of social expectations. It\'s particularly important in formal settings, diplomatic relations, and leadership positions.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kum-PORT-ment (/kəmˈpɔrtmənt/)',
        'etymology': 'From French "comportement," from "comporter" (to conduct oneself)',
        'memory_tips': 'Think "com- (together) + port (carry)" - how you carry yourself together with others',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The diplomat\'s dignified _____ impressed all the foreign delegates at the summit.'
    },
    'composite': {
        'definition': 'Made up of various parts or elements combined to form a complex whole; consisting of distinct components that work together. In materials science, composites combine different materials to achieve properties superior to individual components. Composite numbers in mathematics have factors other than one and themselves. The term emphasizes the strength or effectiveness achieved through combination.',
        'part_of_speech': 'adjective, noun',
        'pronunciation_guide': 'kum-POZ-it (/kəmˈpɒzɪt/)',
        'etymology': 'From Latin "compositus," past participle of "componere" (to put together)',
        'memory_tips': 'Think "com- (together) + pos (place)" - placing different elements together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ material combined carbon fiber and resin for maximum strength.'
    },
    'composition': {
        'definition': 'The arrangement, structure, or makeup of something; the way components are combined or organized to form a whole. In art and music, composition refers to the creation and arrangement of elements to produce a work. In writing, composition involves organizing ideas and words effectively. Chemical composition describes the elements and their proportions in a substance.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kom-puh-ZISH-un (/ˌkɒmpəˈzɪʃən/)',
        'etymology': 'From Latin "compositio," from "componere" (to put together)',
        'memory_tips': 'Think "compose + -ition" - the act or result of composing or arranging',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The chemical _____ of the mineral included iron, magnesium, and silicon.'
    },
    'comprehensive': {
        'definition': 'Complete, thorough, and including everything that is relevant or important; covering all aspects of a subject or situation. Comprehensive approaches examine issues from multiple angles and consider all significant factors. In education, comprehensive schools serve all students regardless of ability. Comprehensive insurance covers a wide range of potential damages or losses.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kom-pri-HEN-siv (/ˌkɒmprɪˈhɛnsɪv/)',
        'etymology': 'From Latin "comprehensivus," from "comprehendere" (to grasp fully)',
        'memory_tips': 'Think "comprehend + -ive" - having the quality of grasping or including everything',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The report provided a _____ analysis of the environmental impact.'
    },
    'compunction': {
        'definition': 'A feeling of guilt, remorse, or uneasiness about something one has done or is considering doing; moral qualms or scruples that cause hesitation. Compunction represents the conscience\'s response to actual or potential wrongdoing. It serves as an internal moral guide, creating discomfort that encourages ethical behavior and discourages harmful actions.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kum-PUNGK-shun (/kəmˈpʌŋkʃən/)',
        'etymology': 'From Latin "compunctio," from "compungere" (to prick sharply)',
        'memory_tips': 'Think "com- (thoroughly) + punct (prick)" - being thoroughly pricked by conscience',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'She felt no _____ about reporting the unethical behavior to management.'
    },
    'compute': {
        'definition': 'To calculate, determine, or process information using mathematical operations or logical reasoning. Computing involves systematic problem-solving, often using mathematical formulas, algorithms, or computer programs. Modern computing encompasses data processing, analysis, and manipulation through electronic devices. The term can apply to both human mental calculations and machine-based computations.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'kum-PYOOT (/kəmˈpjut/)',
        'etymology': 'From Latin "computare," meaning "to calculate, reckon"',
        'memory_tips': 'Think "com- (together) + put (reckon)" - reckoning or calculating things together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The scientist used complex formulas to _____ the trajectory of the spacecraft.'
    },
    'computer': {
        'definition': 'An electronic device capable of receiving, processing, storing, and outputting data according to programmed instructions. Computers perform calculations, execute software applications, and facilitate communication and information management. Modern computers range from personal devices to powerful servers that run internet services. They have revolutionized work, education, entertainment, and communication worldwide.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kum-PYOO-tur (/kəmˈpjutər/)',
        'etymology': 'From Latin "computare" (to calculate) + agent suffix "-er"',
        'memory_tips': 'Think "compute + -er" - a machine that computes or calculates',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The new _____ processed the data analysis in just a few minutes.'
    },
    'concatenate': {
        'definition': 'To link together in a series or chain; to connect or join things in a sequential manner. In computer programming, concatenation involves combining strings, arrays, or data structures end-to-end to create a single, longer entity. The process preserves the order and content of the original elements while creating a unified sequence.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'kon-KAT-uh-nayt (/kənˈkætəneɪt/)',
        'etymology': 'From Latin "concatenatus," from "con-" (together) + "catena" (chain)',
        'memory_tips': 'Think "con- (together) + caten (chain)" - chaining things together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The programmer needed to _____ the user\'s first and last names.'
    },
    'conceit': {
        'definition': 'Excessive pride in oneself; an exaggerated opinion of one\'s own abilities, appearance, or importance. Conceit represents vanity and self-absorption that often alienates others. In literary contexts, conceit refers to an elaborate, often surprising metaphor or comparison. Conceit typically involves a disconnect between self-perception and reality, leading to arrogance and social difficulties.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-SEET (/kənˈsit/)',
        'etymology': 'From Latin "conceptus" (something conceived), later developing the sense of "opinion of oneself"',
        'memory_tips': 'Think "conceive" - conceiving too high an opinion of yourself',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'His _____ about his appearance made him insufferable at social gatherings.'
    },
    'concentrate': {
        'definition': 'To focus attention, effort, or energy on a particular task, subject, or area; to bring together into a smaller space or increase in strength or density. Concentration requires mental discipline and the ability to ignore distractions. In chemistry, to concentrate means to increase the proportion of a substance in a solution. The term emphasizes intensity and focused application.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'KON-sun-trayt (/ˈkɒnsəntreɪt/)',
        'etymology': 'From Latin "concentratus," from "con-" (together) + "centrum" (center)',
        'memory_tips': 'Think "con- (together) + center" - bringing everything together to the center',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'She had to _____ harder to solve the complex mathematical equation.'
    },
    'concepts': {
        'definition': 'Plural of concept; abstract ideas, principles, or mental constructs that represent fundamental understanding of phenomena, objects, or relationships. Concepts form the building blocks of knowledge, allowing humans to categorize, analyze, and communicate about the world. They range from simple (like "red" or "big") to complex (like "democracy" or "entropy").',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KON-septs (/ˈkɒnsɛpts/)',
        'etymology': 'Plural of Latin "conceptus," from "concipere" (to take in, conceive)',
        'memory_tips': 'Think "conceive + -pts" - things conceived or understood in the mind',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The philosophy course explored fundamental _____ of ethics and morality.'
    },
    'conch': {
        'definition': 'A large marine gastropod mollusk with a spiral shell, often used as a horn or decorative object. The conch shell has cultural significance in many societies, used in religious ceremonies, as musical instruments, and as symbols of authority. In literature, notably "Lord of the Flies," the conch represents order and democratic discourse. These shells are also valued for their beauty and acoustic properties.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KONGK (/kɒŋk/) or KONCH (/kɒntʃ/)',
        'etymology': 'From Latin "concha," from Greek "konche" (shell)',
        'memory_tips': 'Think of the shell\'s shape - like a cone with curves, used as a horn',
        'alternate_spellings': 'None',
        'language_origin': 'Greek/Latin',
        'example_sentence': 'The tribal leader blew the _____ shell to summon the village for important announcements.'
    },
    'conciliatory': {
        'definition': 'Intended to placate, soothe, or reconcile conflicting parties; aimed at making peace or resolving disputes through compromise and understanding. Conciliatory approaches emphasize diplomacy, empathy, and finding common ground rather than confrontation. This attitude seeks to reduce tensions, heal relationships, and create cooperative solutions to conflicts.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kun-SIL-ee-uh-tor-ee (/kənˈsɪliəˌtɔri/)',
        'etymology': 'From Latin "conciliatorius," from "conciliare" (to bring together)',
        'memory_tips': 'Think "conciliate + -ory" - having the quality of bringing people together peacefully',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'His _____ tone helped ease the tension during the difficult negotiation.'
    },
    'concinnate': {
        'definition': 'To arrange or compose with skill and elegance; to make neat, harmonious, or well-proportioned. This formal term refers to the artful arrangement of elements to achieve aesthetic or functional excellence. Concinnation involves careful attention to balance, proportion, and refinement in composition, whether in writing, design, or organization.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'KON-si-nayt (/ˈkɒnsɪneɪt/)',
        'etymology': 'From Latin "concinnatus," from "concinnus" (skillfully arranged, elegant)',
        'memory_tips': 'Think of creating neat, elegant arrangements - like a skilled interior designer',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The architect worked to _____ the building\'s design for maximum visual appeal.'
    },
    'concision': {
        'definition': 'The quality of being brief and clearly expressed; the skill of communicating effectively using few words. Concision values clarity and efficiency in communication, eliminating unnecessary words while preserving meaning and impact. This writing principle is highly valued in journalism, academic writing, and professional communication where time and attention are limited.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-SIZH-un (/kənˈsɪʒən/)',
        'etymology': 'From Latin "concisio," from "concidere" (to cut up, cut short)',
        'memory_tips': 'Think "con- (completely) + cis (cut)" - cutting out unnecessary words completely',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The editor praised the writer\'s _____ in conveying complex ideas simply.'
    },
    'conclave': {
        'definition': 'A private or secret meeting of a select group, especially one that involves important decision-making. Most famously, a conclave refers to the assembly of cardinals who elect a new Pope, conducted in strict secrecy. More generally, conclaves are exclusive gatherings where participants discuss confidential matters or make significant decisions away from public scrutiny.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KON-klayv (/ˈkɒnkleɪv/)',
        'etymology': 'From Latin "conclave," meaning "room that can be locked," from "con-" (together) + "clavis" (key)',
        'memory_tips': 'Think "con- (together) + clav (key)" - locked together with a key for secrecy',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The board held a secret _____ to discuss the proposed merger.'
    },
    'concoct': {
        'definition': 'To prepare or devise something, typically by combining various ingredients or elements; to create or invent, especially something unusual or elaborate. Concoct can refer to cooking, creating mixtures, or devising plans and stories. The term often implies creativity, experimentation, or sometimes deception, depending on context.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'kun-KOKT (/kənˈkɒkt/)',
        'etymology': 'From Latin "concoctus," from "concoquere" (to cook together)',
        'memory_tips': 'Think "con- (together) + coct (cook)" - cooking ingredients together to create something',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The chef decided to _____ a new sauce using exotic spices.'
    },
    'concordance': {
        'definition': 'Agreement, harmony, or correspondence between things; an alphabetical index of words used in a book or body of work, showing where each word appears. In biblical studies, concordances help locate specific passages. In statistics, concordance measures the degree of agreement between observations. The term emphasizes consistency and systematic organization.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-KOR-dans (/kənˈkɔrdəns/)',
        'etymology': 'From Latin "concordantia," from "concordare" (to agree)',
        'memory_tips': 'Think "con- (together) + cord (heart)" - hearts agreeing together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The biblical _____ helped scholars locate every occurrence of specific words.'
    },
    'concours': {
        'definition': 'A public competition or contest, especially one involving skills, knowledge, or artistic ability. From French, concours often refers to academic competitions, design contests, or exhibitions where participants demonstrate expertise. In automotive contexts, a "concours d\'elegance" is a competition judging the beauty and condition of classic cars.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-KOOR (/kɒnˈkʊr/)',
        'etymology': 'French, from Latin "concursus" (a running together, competition)',
        'memory_tips': 'Think of people "running together" in competition - a contest',
        'alternate_spellings': 'None',
        'language_origin': 'French/Latin',
        'example_sentence': 'The architecture students participated in the international design _____.'
    },
    'concrete': {
        'definition': 'A hard building material made from cement, sand, gravel, and water that hardens into a stone-like substance. As an adjective, concrete means specific, definite, and tangible rather than abstract or theoretical. Concrete examples provide clear, observable instances that help explain concepts. The term emphasizes solidity, reality, and practical application.',
        'part_of_speech': 'noun, adjective',
        'pronunciation_guide': 'KON-kreet (adj.), kon-KREET (noun) (/ˈkɒnkrit/, /kɒnˈkrit/)',
        'etymology': 'From Latin "concretus," meaning "grown together, hardened"',
        'memory_tips': 'Think of something solid and specific - not abstract but real and tangible',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The foundation was built with reinforced _____ to ensure structural stability.'
    },
    'condemn': {
        'definition': 'To express strong disapproval of something; to judge or declare something as wrong, evil, or unacceptable. In legal contexts, to condemn means to sentence someone to punishment or declare property unsuitable for use. Condemnation often involves moral judgment and can lead to social sanctions, legal penalties, or property seizure for public use.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'kun-DEM (/kənˈdɛm/)',
        'etymology': 'From Latin "condemnare," from "con-" (completely) + "damnare" (to damage, condemn)',
        'memory_tips': 'Think "con- (completely) + damn" - completely damning or rejecting something',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The international community decided to _____ the dictator\'s human rights violations.'
    },
    'condensation': {
        'definition': 'The process by which a gas or vapor changes into liquid form, typically due to cooling or increased pressure. In physics, condensation occurs when water vapor in air transforms into liquid droplets. The term also refers to the act of making something more compact or concentrated, such as condensing a long document into a summary.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-den-SAY-shun (/ˌkɒndɛnˈseɪʃən/)',
        'etymology': 'From Latin "condensatio," from "condensare" (to make dense)',
        'memory_tips': 'Think "con- (together) + dense" - bringing particles together to become dense/liquid',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Morning dew forms through _____ of water vapor on cool surfaces.'
    },
    'condescendingly': {
        'definition': 'In a manner that shows a patronizing attitude toward someone considered inferior; acting as though one is lowering oneself to interact with others. This adverb describes behavior that appears helpful but actually conveys superiority, arrogance, or disdain. Condescending communication often alienates others and damages relationships.',
        'part_of_speech': 'adverb',
        'pronunciation_guide': 'kon-duh-SEND-ing-lee (/ˌkɒndəˈsɛndɪŋli/)',
        'etymology': 'From Latin "condescendere" (to stoop, descend) + adverbial suffix "-ly"',
        'memory_tips': 'Think "con- (down) + descend" - coming down from a high position in a superior way',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'She spoke _____ to her colleagues, making them feel incompetent.'
    },
    'condign': {
        'definition': 'Well-deserved and appropriate, especially referring to punishment that fits the crime or consequence that matches the action. This formal term emphasizes justice and proportionality in responses to behavior. Condign punishment is neither too harsh nor too lenient but precisely matches the severity of the offense.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kun-DINE (/kənˈdaɪn/)',
        'etymology': 'From Latin "condignus," meaning "wholly worthy," from "con-" (completely) + "dignus" (worthy)',
        'memory_tips': 'Think "con- (completely) + dign (worthy)" - completely worthy or deserved',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The judge imposed _____ punishment that perfectly matched the severity of the crime.'
    },
    'condiments': {
        'definition': 'Substances such as sauces, spices, or seasonings added to food to enhance flavor, typically served separately and applied according to individual taste. Common condiments include ketchup, mustard, salt, pepper, and various sauces. These flavor enhancers allow diners to customize their meals and can reflect cultural preferences and regional cuisines.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KON-duh-muhnts (/ˈkɒndəmənts/)',
        'etymology': 'From Latin "condimentum," from "condire" (to season, pickle)',
        'memory_tips': 'Think "condition + -ments" - things that condition or flavor food',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The restaurant provided various _____ including hot sauce, relish, and specialty mustards.'
    },
    'condimentsconference': {
        'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "condiments" (food seasonings) + "conference" (formal meeting). These should be separate words.',
        'part_of_speech': 'error - combined words',
        'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
        'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
        'memory_tips': 'This is a data error - should be separated into "condiments" and "conference"',
        'alternate_spellings': 'condiments + conference (separate words)',
        'language_origin': 'ERROR - combined words',
        'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
    },
    'condition': {
        'definition': 'The state or circumstances in which something exists; the physical or mental state of a person, object, or situation. Conditions can refer to requirements that must be met, medical states, environmental factors, or contractual terms. The word emphasizes the current status and any factors that influence or determine that status.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'kun-DISH-un (/kənˈdɪʃən/)',
        'etymology': 'From Latin "conditio," from "condicere" (to agree upon)',
        'memory_tips': 'Think of the state something is in - its current situation or requirements',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The car was in excellent _____ despite being ten years old.'
    },
    'condominium': {
        'definition': 'A type of real estate ownership where individuals own individual units within a larger building or complex, while sharing ownership of common areas such as hallways, elevators, and recreational facilities. Condominiums combine private ownership with shared responsibilities and are governed by homeowners\' associations that manage common areas and enforce community rules.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-duh-MIN-ee-um (/ˌkɒndəˈmɪniəm/)',
        'etymology': 'From Latin "con-" (together) + "dominium" (ownership, domain)',
        'memory_tips': 'Think "con- (together) + dominium (ownership)" - shared ownership arrangement',
        'alternate_spellings': 'Condo (informal)',
        'language_origin': 'Latin',
        'example_sentence': 'They purchased a _____ overlooking the harbor with stunning ocean views.'
    },
    'conductor': {
        'definition': 'A person who directs an orchestra, choir, or other musical ensemble, guiding tempo, dynamics, and interpretation through gestures and baton movements. In transportation, a conductor collects tickets and assists passengers. In physics, a conductor is a material that allows electricity, heat, or sound to pass through easily. The term emphasizes guidance and transmission.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-DUK-tur (/kənˈdʌktər/)',
        'etymology': 'From Latin "conductor," from "conducere" (to lead together)',
        'memory_tips': 'Think "con- (together) + duct (lead)" - someone who leads people together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The orchestra _____ raised his baton to begin the symphony performance.'
    },
    'conduit': {
        'definition': 'A channel or tube for conveying water, cables, or other materials; a means of transmitting or distributing something. In electrical work, conduits protect wiring. Metaphorically, a conduit can be a person or organization that facilitates communication or transfer between parties. The term emphasizes the function of transmission and protection.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KON-doo-it (/ˈkɒnduɪt/) or KON-dit (/ˈkɒndɪt/)',
        'etymology': 'From Old French "conduit," from Latin "conductus" (led together)',
        'memory_tips': 'Think of a tube or channel that "conducts" or leads things through',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'The electrical _____ protected the wiring from moisture and damage.'
    },
    'condyles': {
        'definition': 'Rounded projections at the end of bones that form joints with other bones, particularly important in knee and jaw anatomy. Condyles allow for smooth articulation and movement between bones, acting as the contact points in joints. These anatomical structures are crucial for proper joint function and are covered with cartilage to reduce friction during movement.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KON-dylz (/ˈkɒndaɪlz/)',
        'etymology': 'Plural of Greek "kondylos," meaning "knuckle" or "joint"',
        'memory_tips': 'Think of "knuckle-like" projections on bones where joints form',
        'alternate_spellings': 'None',
        'language_origin': 'Greek',
        'example_sentence': 'The orthopedic surgeon examined the femoral _____ for signs of arthritis.'
    },
    'cone': {
        'definition': 'A three-dimensional geometric shape with a circular base that tapers evenly to a point; objects shaped like this form. In botany, cones are reproductive structures of coniferous trees containing seeds. Ice cream cones, traffic cones, and pine cones are common examples. The shape is characterized by its pointed top and circular bottom.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOHN (/koʊn/)',
        'etymology': 'From Latin "conus," from Greek "konos" (cone, pine cone)',
        'memory_tips': 'Think of ice cream cones or pine cones - pointed at one end, round at the other',
        'alternate_spellings': 'None',
        'language_origin': 'Greek/Latin',
        'example_sentence': 'The children collected pine _____ during their nature walk in the forest.'
    },
    'conestoga': {
        'definition': 'A type of large, heavy wagon with a canvas cover, used by American pioneers for transporting goods and families across the frontier in the 18th and 19th centuries. Named after the Conestoga Valley in Pennsylvania where they were first built, these wagons were essential for westward expansion and featured distinctive curved floors and white canvas tops.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-uh-STOH-guh (/ˌkɒnəˈstoʊgə/)',
        'etymology': 'Named after Conestoga Valley in Lancaster County, Pennsylvania',
        'memory_tips': 'Think of covered wagons crossing the American frontier - the classic pioneer wagon',
        'alternate_spellings': 'Conestoga wagon',
        'language_origin': 'American English (place name)',
        'example_sentence': 'The pioneer family loaded their _____ wagon for the long journey westward.'
    },
    'confabulation': {
        'definition': 'The unconscious filling in of memory gaps with fabricated, distorted, or misinterpreted information, often seen in certain neurological conditions. Unlike lying, confabulation involves the person genuinely believing their false memories. In psychology, this phenomenon helps explain how memory reconstruction can create vivid but inaccurate recollections of events.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-fab-yuh-LAY-shun (/kənˌfæbjəˈleɪʃən/)',
        'etymology': 'From Latin "confabulatio," from "confabulari" (to chat together)',
        'memory_tips': 'Think "con- (together) + fabul (story)" - making up stories together, but unconsciously',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The patient\'s _____ made it difficult to determine what actually happened.'
    },
    'conference': {
        'definition': 'A formal meeting or series of meetings where people gather to discuss specific topics, share information, or make decisions. Conferences often bring together experts, professionals, or stakeholders to exchange ideas, present research, or coordinate activities. They can range from small business meetings to large international gatherings covering academic, professional, or political subjects.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KON-fur-uhns (/ˈkɒnfərəns/)',
        'etymology': 'From Latin "conferre," meaning "to bring together"',
        'memory_tips': 'Think "con- (together) + fer (bring)" - bringing people together to discuss',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The annual medical _____ featured presentations from leading researchers worldwide.'
    },
    'confident': {
        'definition': 'Having a strong belief in one\'s abilities, qualities, or judgment; showing self-assurance and certainty. Confident people trust their skills and knowledge, approach challenges with optimism, and communicate with conviction. Healthy confidence enables effective leadership, decision-making, and interpersonal relationships while avoiding the extremes of arrogance or self-doubt.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KON-fi-duhnt (/ˈkɒnfɪdənt/)',
        'etymology': 'From Latin "confidens," present participle of "confidere" (to trust fully)',
        'memory_tips': 'Think "con- (with) + fid (trust)" - trusting fully in yourself',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'She felt _____ about her presentation after weeks of careful preparation.'
    },
    'configuration': {
        'definition': 'The arrangement, setup, or organization of parts or elements in a particular form or pattern. In computing, configuration refers to the specific settings and parameters that determine how software or hardware operates. The term emphasizes the way components are positioned relative to each other and how this arrangement affects function or appearance.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-fig-yuh-RAY-shun (/kənˌfɪgjəˈreɪʃən/)',
        'etymology': 'From Latin "configuratio," from "configurare" (to shape after)',
        'memory_tips': 'Think "con- (together) + figur (shape)" - shaping things together in a pattern',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The IT specialist adjusted the network _____ to improve connection speed.'
    },
    'confiscated': {
        'definition': 'Past tense of confiscate; seized or taken away by authority, typically as a penalty or for violating rules. Confiscation involves official seizure of property, often without compensation, usually due to illegal activity or rule violations. The term implies legitimate authority taking possession of items or assets.',
        'part_of_speech': 'verb (past tense)',
        'pronunciation_guide': 'KON-fi-skay-ted (/ˈkɒnfɪskeɪtəd/)',
        'etymology': 'From Latin "confiscatus," from "confiscare" (to seize for the public treasury)',
        'memory_tips': 'Think "con- (together) + fisc (treasury)" - seized together for the treasury/authority',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The teacher _____ the student\'s phone for using it during class.'
    }
}

def process_batch():
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_039_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_039_processed.csv'
    
    try:
        df = pd.read_csv(input_file)
        print(f"Processing {len(df)} words from batch 039...")
        
        processed_data = []
        combined_word_errors = []
        
        for _, row in df.iterrows():
            word = row['word'].strip()
            if word in batch_039_data:
                data = batch_039_data[word]
                
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