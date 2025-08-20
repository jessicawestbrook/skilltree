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

batch_038_data = {
    'colson': {
        'definition': 'A surname of English origin, historically referring to "son of Cole" or derived from the Old English personal name "Col." In educational contexts, it may also refer to Colson Whitehead, the acclaimed American novelist and journalist known for works like "The Underground Railroad" and "The Intuitionist." The name has gained prominence in American literature and cultural discourse through various notable bearers.',
        'part_of_speech': 'noun (proper name)',
        'pronunciation_guide': 'COAL-sun (/ˈkoʊlsən/)',
        'etymology': 'English surname meaning "son of Cole," from Old English personal name "Col" + patronymic suffix "-son"',
        'memory_tips': 'Remember "coal + son" - like coal\'s son, or think of author Colson Whitehead',
        'alternate_spellings': 'Coulson',
        'language_origin': 'Old English',
        'example_sentence': 'The literary critic praised _____ for his masterful storytelling in contemporary American fiction.'
    },
    'coltan': {
        'definition': 'A metallic ore consisting primarily of columbite and tantalite, essential for manufacturing electronic devices like smartphones, computers, and gaming consoles. This mineral contains tantalum and niobium, critical elements for capacitors and other electronic components. Most coltan is mined in the Democratic Republic of Congo, often under controversial conditions that have raised ethical concerns about conflict minerals in the electronics industry.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOL-tan (/ˈkɒltæn/)',
        'etymology': 'Portmanteau of "columbite" and "tantalite," the two main mineral components',
        'memory_tips': 'Think "col(umbite) + tan(talite)" - the two minerals combined to form this crucial electronic ore',
        'alternate_spellings': 'None commonly used',
        'language_origin': 'Modern English (mineralogy)',
        'example_sentence': 'The smartphone in your pocket likely contains _____ mined from Central African deposits.'
    },
    'colubrine': {
        'definition': 'Relating to or characteristic of snakes, particularly those belonging to the family Colubridae, which includes most common non-venomous snakes. This scientific term describes snake-like qualities such as serpentine movement, elongated body form, or behavioral characteristics typical of colubrids. In zoological contexts, it specifically refers to the morphological and behavioral traits of this diverse snake family.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KOL-yuh-brine (/ˈkɒljʊbraɪn/)',
        'etymology': 'From Latin "colubrinus," meaning "of or pertaining to a snake," from "coluber" (snake)',
        'memory_tips': 'Connect to "cobra" - both relate to snakes, with "colubrine" describing snake-like characteristics',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The biologist noted the _____ grace with which the garden snake moved through the grass.'
    },
    'columbia': {
        'definition': 'A poetic and historical name for the United States of America, personified as a female figure representing American ideals and liberty. Named after Christopher Columbus, Columbia became a popular patriotic symbol in American art, literature, and culture from the 18th through early 20th centuries. The name also refers to various geographical locations, institutions, and the space shuttle program, embodying American exploration and achievement.',
        'part_of_speech': 'noun (proper name)',
        'pronunciation_guide': 'kuh-LUM-bee-uh (/kəˈlʌmbiə/)',
        'etymology': 'From Christopher Columbus, Latinized as "Columba" (dove), used poetically for America',
        'memory_tips': 'Think "Columbus + -ia" - America named after Columbus, often shown as Lady Columbia',
        'alternate_spellings': 'None',
        'language_origin': 'Latin (from Italian)',
        'example_sentence': 'The patriotic song praised _____ as the embodiment of American freedom and democracy.'
    },
    'column': {
        'definition': 'A vertical structural element, typically cylindrical, that supports weight in architecture and construction. Columns transfer loads from above (such as roofs or upper floors) to the foundation below. In writing and journalism, a column refers to a regular feature or opinion piece by a specific author. Additionally, in data organization, a column represents a vertical arrangement of information in tables, spreadsheets, or databases.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOL-um (/ˈkɒləm/)',
        'etymology': 'From Latin "columna," meaning pillar or support post',
        'memory_tips': 'Visualize a tall pillar supporting a building, or think of newspaper columns arranged vertically',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The ancient Greek temple featured ornate Corinthian _____ supporting its marble roof.'
    },
    'columns': {
        'definition': 'Plural form of column, referring to multiple vertical supports in architecture or multiple sections in printed material. In classical architecture, columns often appear in rows forming colonnades or porticos. In publishing, columns divide pages into vertical sections for easier reading. In data analysis, columns represent different variables or categories of information arranged vertically in spreadsheets or databases.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KOL-ums (/ˈkɒləmz/)',
        'etymology': 'Plural of Latin "columna," meaning pillars or support posts',
        'memory_tips': 'Multiple pillars supporting a structure, or multiple vertical sections in a newspaper',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The spreadsheet organized the financial data into clearly labeled _____ for easy analysis.'
    },
    'comanchero': {
        'definition': 'A historical term for traders, primarily of Hispanic origin, who conducted commerce with Comanche Native Americans on the Great Plains during the 18th and 19th centuries. These traders operated along established trade routes, exchanging manufactured goods, weapons, and horses for buffalo hides, captives, and livestock. The comanchero trade system played a significant role in the economic and cultural interactions between different groups in the American Southwest.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'koh-man-CHEH-roh (/koʊmænˈtʃɛroʊ/)',
        'etymology': 'Spanish, meaning "one who trades with Comanches," from "Comanche" + Spanish suffix "-ero"',
        'memory_tips': 'Break down: "Comanche" (Native American tribe) + "-ero" (Spanish for "one who does") = trader with Comanches',
        'alternate_spellings': 'Comancheros (plural)',
        'language_origin': 'Spanish',
        'example_sentence': 'The _____ arrived at the trading post with horses and buffalo hides from the Comanche bands.'
    },
    'combat': {
        'definition': 'Armed fighting or conflict between opposing forces, whether in military warfare, individual duels, or competitive sports. Combat involves direct engagement with an adversary using weapons, physical force, or strategic tactics. The term extends beyond military contexts to include fighting diseases, social problems, or any vigorous struggle against opposing forces. Modern combat encompasses various forms from traditional warfare to cyber warfare.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KOM-bat (noun), kum-BAT (verb) (/ˈkɒmbæt/, /kəmˈbæt/)',
        'etymology': 'From Old French "combattre," meaning "to fight," from Latin "com-" (together) + "battuere" (to beat)',
        'memory_tips': 'Think "com- (together) + bat (beat)" - opponents beating against each other together',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'The soldiers prepared for _____ while medics worked to _____ the spread of infection.'
    },
    'combed': {
        'definition': 'Past tense of "comb," meaning to have arranged, cleaned, or searched through systematically. When referring to hair, it means having used a comb to arrange strands neatly. In textile production, combed refers to fibers that have been straightened and aligned by combing processes. The term also means to have searched thoroughly through an area or material, as in "combed the beach for shells."',
        'part_of_speech': 'verb (past tense)',
        'pronunciation_guide': 'KOHMD (/koʊmd/)',
        'etymology': 'From Old English "camb" (comb) + past tense ending "-ed"',
        'memory_tips': 'Think of running a comb through hair to make it neat and orderly',
        'alternate_spellings': 'None',
        'language_origin': 'Old English',
        'example_sentence': 'She _____ her hair carefully before the important interview.'
    },
    'combination': {
        'definition': 'The result of combining two or more elements, substances, or concepts to create something new or unified. In mathematics, a combination refers to a selection of items where order does not matter. In everyday usage, it describes things joined together for a common purpose, such as a combination lock requiring specific numbers in sequence. The term emphasizes the synergistic effect of elements working together.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kom-buh-NAY-shun (/ˌkɒmbɪˈneɪʃən/)',
        'etymology': 'From Latin "combinatio," from "combinare" (to combine), from "com-" (together) + "bini" (two by two)',
        'memory_tips': 'Think "combine + -ation" - the act or result of combining things together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The chef\'s _____ of spices created an unexpectedly delicious flavor profile.'
    },
    'combustible': {
        'definition': 'Capable of catching fire and burning readily; easily ignited by heat, sparks, or flames. This term describes materials with low ignition temperatures that pose fire hazards, such as gasoline, paper, or dry wood. In figurative usage, combustible describes volatile situations or personalities prone to explosive reactions. Safety regulations strictly control the storage and handling of combustible materials to prevent accidents.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kum-BUS-tuh-bul (/kəmˈbʌstəbəl/)',
        'etymology': 'From Latin "combustus" (burned up) + suffix "-ible" (capable of being)',
        'memory_tips': 'Connect to "combust" - if something can combust (burn), it\'s combustible',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The warehouse stored _____ materials away from heat sources to prevent fires.'
    },
    'comedienne': {
        'definition': 'A female comedian or performer who specializes in comedy, particularly in theatrical, television, or film entertainment. This term specifically designates women who make their living through humor, whether as stand-up comedians, comic actresses, or comedy writers. While "comedian" has become increasingly gender-neutral, "comedienne" maintains the tradition of acknowledging women\'s contributions to comedy and entertainment.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kuh-mee-dee-EN (/kəˌmidiˈɛn/)',
        'etymology': 'French feminine form of "comédien" (comedian), from "comédie" (comedy)',
        'memory_tips': 'Remember the French feminine ending "-enne" - like "comedian" but specifically for women',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The talented _____ brought the audience to tears of laughter with her witty observations.'
    },
    'comes': {
        'definition': 'Third person singular present tense of the verb "come," indicating movement toward the speaker or arrival at a destination. This fundamental verb expresses approach, arrival, or occurrence of events. "Comes" can also indicate origin ("comes from a good family") or future events ("comes next Tuesday"). It\'s one of the most frequently used verbs in English, essential for describing movement and temporal relationships.',
        'part_of_speech': 'verb (third person singular present)',
        'pronunciation_guide': 'KUMZ (/kʌmz/)',
        'etymology': 'From Old English "cuman," related to German "kommen" and Latin "venire"',
        'memory_tips': 'Think of someone approaching: "Here he comes!" - movement toward you',
        'alternate_spellings': 'None',
        'language_origin': 'Old English',
        'example_sentence': 'She _____ to visit every Sunday afternoon for tea with her grandmother.'
    },
    'comestibles': {
        'definition': 'Edible items; food and drink suitable for consumption. This formal term encompasses all consumable provisions, from basic groceries to gourmet delicacies. Often used in upscale culinary contexts, fine dining establishments, or food retail describing high-quality edible products. The term elevates ordinary food discussion to a more sophisticated level, commonly found in gourmet food descriptions and culinary literature.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'kuh-MES-tuh-bulz (/kəˈmɛstəbəlz/)',
        'etymology': 'From Latin "comestibilis," meaning "edible," from "comedere" (to eat up)',
        'memory_tips': 'Connect to "edible" - both mean things you can eat, but comestibles sounds more fancy',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The gourmet shop specialized in imported _____ from various European countries.'
    },
    'comfort': {
        'definition': 'A state of physical ease and freedom from pain or constraint, or the provision of such relief. Comfort includes emotional solace, reassurance during distress, and the amenities that make life pleasant and convenient. The term encompasses both physical comfort (soft furniture, warm clothing) and psychological comfort (emotional support, familiar surroundings). Modern usage extends to comfort zones and comfort food.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KUM-furt (/ˈkʌmfərt/)',
        'etymology': 'From Latin "confortare," meaning "to strengthen greatly," from "com-" (intensive) + "fortis" (strong)',
        'memory_tips': 'Think "com- (with) + fort (strength)" - providing strength and ease to someone',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The soft blanket provided _____ during the cold winter night.'
    },
    'comic': {
        'definition': 'Relating to comedy or humor; designed to amuse or provoke laughter. As a noun, comic refers to a comedian or performer specializing in humorous entertainment. Comic also describes illustrated stories or publications (comic books, comic strips) that typically combine visual art with text to tell stories, often but not exclusively humorous. The term encompasses various forms of comedic expression in entertainment and literature.',
        'part_of_speech': 'adjective, noun',
        'pronunciation_guide': 'KOM-ik (/ˈkɒmɪk/)',
        'etymology': 'From Latin "comicus," from Greek "komikos," relating to comedy',
        'memory_tips': 'Think of comic books or stand-up comics - both designed to entertain and amuse',
        'alternate_spellings': 'None',
        'language_origin': 'Greek/Latin',
        'example_sentence': 'The _____ timing of the actor made even the serious scene unexpectedly funny.'
    },
    'comics': {
        'definition': 'Sequential art combining illustrations and text to tell stories, typically published as comic books, comic strips, or graphic novels. Comics encompass various genres from superhero adventures to literary narratives, using panels, speech bubbles, and visual storytelling techniques. The medium has evolved from newspaper comic strips to sophisticated graphic literature recognized for artistic and literary merit. Comics also refers to the comedy entertainment industry.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KOM-iks (/ˈkɒmɪks/)',
        'etymology': 'Plural of "comic," from Latin "comicus," originally referring to comedic theatrical works',
        'memory_tips': 'Think of comic books with superheroes, or newspaper comic strips with funny characters',
        'alternate_spellings': 'None',
        'language_origin': 'Greek/Latin',
        'example_sentence': 'The library\'s _____ section included both classic superhero stories and modern graphic novels.'
    },
    'coming': {
        'definition': 'Present participle of "come," indicating approaching movement or future arrival. As an adjective, "coming" describes something that is approaching or about to happen in the near future. The term can refer to physical approach ("coming closer"), temporal approach ("coming year"), or developmental stages ("coming of age"). It expresses anticipation and forward movement in time or space.',
        'part_of_speech': 'verb (present participle), adjective',
        'pronunciation_guide': 'KUM-ing (/ˈkʌmɪŋ/)',
        'etymology': 'From Old English "cuman" + present participle suffix "-ing"',
        'memory_tips': 'Think of movement toward you: "She is coming here" or future events: "coming soon"',
        'alternate_spellings': 'None',
        'language_origin': 'Old English',
        'example_sentence': 'The _____ storm forced residents to prepare their homes for severe weather.'
    },
    'commandeer': {
        'definition': 'To officially take possession or control of something, typically for military or public use during emergencies. This term often involves requisitioning private property, vehicles, or resources when normal procurement methods are insufficient. Commandeering usually occurs under legal authority during wartime, natural disasters, or other urgent situations where immediate access to resources is critical for public safety or national security.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'kom-an-DEER (/ˌkɒmənˈdɪər/)',
        'etymology': 'From Afrikaans "kommandeer," from French "commander" (to command)',
        'memory_tips': 'Think "command + steer" - taking command and steering/controlling something',
        'alternate_spellings': 'None',
        'language_origin': 'Afrikaans/French',
        'example_sentence': 'During the evacuation, officials had to _____ buses to transport stranded civilians.'
    },
    'commandments': {
        'definition': 'Authoritative rules or principles, especially divine commands that must be obeyed. Most famously referring to the Ten Commandments given to Moses in Judeo-Christian tradition, these represent fundamental moral and religious laws. The term extends beyond religious contexts to describe any important rules, principles, or guidelines that should be followed, whether in ethical systems, organizational policies, or personal codes of conduct.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'kuh-MAND-muhnts (/kəˈmændmənts/)',
        'etymology': 'From Old French "commandement," from "commander" (to command) + suffix "-ment"',
        'memory_tips': 'Think "command + -ments" - commands or orders that must be followed',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'The organization\'s ethical _____ guided employee behavior in difficult situations.'
    },
    'commemoration': {
        'definition': 'The act of honoring the memory of someone or something through ceremonies, monuments, or special observances. Commemoration preserves historical events, celebrates achievements, or honors deceased individuals through formal recognition. This process helps societies remember significant moments, heroes, or tragic events through memorials, annual observances, or dedicated spaces. Commemoration serves both educational and emotional purposes in collective memory.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kuh-mem-uh-RAY-shun (/kəˌmɛməˈreɪʃən/)',
        'etymology': 'From Latin "commemoratio," from "commemorare" (to bring to remembrance)',
        'memory_tips': 'Think "com- (together) + memor (memory)" - coming together to remember',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The memorial service was a beautiful _____ of the fallen soldiers\' sacrifice.'
    },
    'commerce': {
        'definition': 'The activity of buying and selling goods and services, especially on a large scale involving transportation between different places. Commerce encompasses all aspects of trade, including wholesale and retail operations, import and export activities, and the financial systems supporting these transactions. Modern commerce includes e-commerce, digital transactions, and global supply chains that connect producers and consumers worldwide.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOM-urs (/ˈkɒmərs/)',
        'etymology': 'From Latin "commercium," from "com-" (together) + "mercari" (to trade)',
        'memory_tips': 'Think "com- (together) + merce (trade)" - people coming together to trade',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The port city thrived due to its strategic location for international _____.'
    },
    'commercial': {
        'definition': 'Related to commerce, trade, or business activities, especially those aimed at generating profit. As a noun, commercial refers to an advertisement broadcast on television, radio, or other media to promote products or services. Commercial activities contrast with non-profit, artistic, or purely academic endeavors, focusing on market viability and financial success. The term can also describe practical, business-minded approaches to various activities.',
        'part_of_speech': 'adjective, noun',
        'pronunciation_guide': 'kuh-MUR-shul (/kəˈmɜːrʃəl/)',
        'etymology': 'From Latin "commercialis," relating to commerce or trade',
        'memory_tips': 'Think of TV commercials selling products, or commercial businesses making money',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ district bustled with shops, offices, and restaurants serving business clients.'
    },
    'comminatory': {
        'definition': 'Expressing or containing threats; menacing or threatening in nature. This formal term describes language, behavior, or communications that warn of punishment or harmful consequences. Often used in legal, religious, or official contexts, comminatory statements serve as warnings intended to deter certain actions. The term implies a serious, authoritative tone designed to inspire fear or compliance through threatened consequences.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kuh-MIN-uh-tor-ee (/kəˈmɪnətɔri/)',
        'etymology': 'From Latin "comminatorius," from "comminari" (to threaten)',
        'memory_tips': 'Think "com- + minat (threaten)" - threatening or menacing in tone',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The judge\'s _____ remarks warned the defendant about consequences of future violations.'
    },
    'commiserative': {
        'definition': 'Expressing sympathy, pity, or compassion for someone\'s suffering or misfortune. This term describes language, actions, or attitudes that show understanding and shared sorrow for another\'s difficulties. Commiserative responses acknowledge pain while offering emotional support. The word implies genuine empathy rather than mere politeness, suggesting a deep understanding of another\'s situation and a desire to provide comfort.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kuh-MIZ-uh-ray-tiv (/kəˈmɪzərətɪv/)',
        'etymology': 'From Latin "commiseratus," past participle of "commiserari" (to pity)',
        'memory_tips': 'Think "com- (with) + miser (wretched)" - feeling wretched together with someone',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Her _____ words provided comfort to the family during their time of grief.'
    },
    'commissioner': {
        'definition': 'An official appointed to oversee and administer a particular department, organization, or area of public service. Commissioners typically have executive authority within their jurisdiction, such as police commissioners, health commissioners, or sports commissioners. They may lead government agencies, regulate industries, or manage public institutions. The role combines administrative expertise with policy implementation and public accountability.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kuh-MISH-uh-nur (/kəˈmɪʃənər/)',
        'etymology': 'From Latin "commissarius," from "committere" (to entrust)',
        'memory_tips': 'Think "commission + -er" - someone who has been commissioned or entrusted with authority',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The police _____ announced new reforms to improve community relations.'
    },
    'commissionergrande': {
        'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "commissioner" (an appointed official) + "grande" (Spanish/Italian for "large" or "great"). These should be separate words.',
        'part_of_speech': 'error - combined words',
        'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
        'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
        'memory_tips': 'This is a data error - should be separated into "commissioner" and "grande"',
        'alternate_spellings': 'commissioner + grande (separate words)',
        'language_origin': 'ERROR - combined words',
        'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
    },
    'commits': {
        'definition': 'Third person singular present tense of "commit," meaning to carry out, pledge, or dedicate oneself to a particular action or cause. The term can indicate performing an act (commits a crime), making a promise (commits to helping), or dedicating resources (commits funds). In various contexts, it implies determination, obligation, or the act of binding oneself to a course of action.',
        'part_of_speech': 'verb (third person singular present)',
        'pronunciation_guide': 'kuh-MITS (/kəˈmɪts/)',
        'etymology': 'From Latin "committere," meaning "to connect, entrust," from "com-" (together) + "mittere" (to send)',
        'memory_tips': 'Think "com- (together) + mit (send)" - sending oneself together with a cause or action',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'She _____ to exercising every morning before work to maintain her health.'
    },
    'committee': {
        'definition': 'A group of people appointed or elected to perform a specific function, make decisions, or manage particular tasks within a larger organization. Committees typically have defined purposes, such as planning events, reviewing policies, or overseeing projects. They operate through meetings, discussions, and collaborative decision-making processes. Committee structures are common in government, businesses, educational institutions, and community organizations.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kuh-MIT-ee (/kəˈmɪti/)',
        'etymology': 'From Latin "committere" (to entrust) + suffix "-ee" indicating recipients of action',
        'memory_tips': 'Think "commit + -tee" - a group committed to a specific task or responsibility',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The planning _____ met weekly to organize the school\'s annual fundraising event.'
    },
    'commodious': {
        'definition': 'Spacious and comfortable; having ample room for intended purposes. This term describes living spaces, vehicles, or containers that provide generous accommodation without crowding. Commodious implies both adequate size and thoughtful design that enhances comfort and usability. Often used in real estate, architecture, or descriptions of luxury accommodations, the word suggests both practical functionality and pleasant roominess.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kuh-MOH-dee-us (/kəˈmoʊdiəs/)',
        'etymology': 'From Latin "commodiosus," meaning "convenient, suitable," from "commodus" (convenient)',
        'memory_tips': 'Think "commod (convenient) + -ious" - conveniently spacious and comfortable',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ dining room easily accommodated the large family gathering.'
    },
    'commonly': {
        'definition': 'In a usual, ordinary, or frequently occurring manner; typically or generally. This adverb indicates that something happens regularly, is widely known, or represents normal practice. Commonly suggests broad acceptance, frequent occurrence, or general understanding among most people. It contrasts with rare, unusual, or specialized occurrences, emphasizing the ordinary or expected nature of events, behaviors, or knowledge.',
        'part_of_speech': 'adverb',
        'pronunciation_guide': 'KOM-un-lee (/ˈkɒmənli/)',
        'etymology': 'From "common" + adverbial suffix "-ly"',
        'memory_tips': 'Think "common + -ly" - in a common or typical way',
        'alternate_spellings': 'None',
        'language_origin': 'Middle English',
        'example_sentence': 'This error is _____ made by students learning the multiplication tables.'
    },
    'commonplace': {
        'definition': 'Ordinary, unremarkable, or frequently encountered; lacking originality or special interest. As a noun, commonplace refers to something ordinary or a collection of notable quotations, ideas, or observations. The term suggests that something has become so familiar or frequent that it no longer attracts attention or interest. In academic contexts, a commonplace book was a personal compilation of quotes and ideas.',
        'part_of_speech': 'adjective, noun',
        'pronunciation_guide': 'KOM-un-plays (/ˈkɒmənpleɪs/)',
        'etymology': 'Translation of Latin "locus communis," meaning "general theme" or "common topic"',
        'memory_tips': 'Think "common + place" - something you commonly find in any place',
        'alternate_spellings': 'None',
        'language_origin': 'Latin (via translation)',
        'example_sentence': 'Cell phones have become so _____ that few restaurants remain phone-free zones.'
    },
    'commorients': {
        'definition': 'Legal term referring to people who die simultaneously or at approximately the same time, particularly relevant in inheritance and succession law. When commorients include family members or beneficiaries, special legal provisions determine how property and assets are distributed. This concept addresses situations where the order of death cannot be determined, such as in accidents, disasters, or other tragic circumstances affecting multiple related parties.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'kuh-MOR-ee-uhnts (/kəˈmɔriənts/)',
        'etymology': 'From Latin "commorientes," present participle of "commori" (to die together)',
        'memory_tips': 'Think "com- (together) + mori (die)" - people who die together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The estate lawyer explained the laws governing _____ in cases of simultaneous death.'
    },
    'commotion': {
        'definition': 'A state of confused and noisy disturbance; tumultuous activity or agitation. Commotion suggests disorder, excitement, and disruption of normal calm or quiet. This can result from accidents, arguments, celebrations, or any event that creates sudden activity and noise. The term implies temporary chaos, confusion, or excitement that disturbs the usual peaceful state of an environment.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kuh-MOH-shun (/kəˈmoʊʃən/)',
        'etymology': 'From Latin "commotio," from "commovere" (to move violently)',
        'memory_tips': 'Think "com- (together) + motion" - lots of people in motion together creating disturbance',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The loud _____ in the hallway disrupted classes throughout the school.'
    },
    'commove': {
        'definition': 'To move emotionally; to stir up, agitate, or cause to feel strong emotion. This formal and somewhat archaic term describes the action of deeply affecting someone\'s feelings or creating emotional turbulence. Commove implies more than simple movement—it suggests profound emotional stirring that may lead to action or significant psychological impact. The word is rarely used in contemporary speech but appears in literary contexts.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'kuh-MOOV (/kəˈmuv/)',
        'etymology': 'From Latin "commovere," meaning "to move violently, stir up"',
        'memory_tips': 'Think "com- (thoroughly) + move" - to move someone thoroughly or emotionally',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The tragic story served to _____ even the most hardened audience members.'
    },
    'communication': {
        'definition': 'The process of conveying information, ideas, or feelings through speech, writing, gestures, or other means between individuals or groups. Effective communication involves both transmission and reception of messages, requiring clarity, understanding, and often feedback. Modern communication encompasses various media including digital platforms, telecommunication systems, and face-to-face interaction. Communication is fundamental to human relationships, education, business, and social organization.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kuh-myoo-nuh-KAY-shun (/kəˌmjunɪˈkeɪʃən/)',
        'etymology': 'From Latin "communicatio," from "communicare" (to share, make common)',
        'memory_tips': 'Think "common + -ication" - making ideas common or shared between people',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Clear _____ between team members improved the project\'s efficiency significantly.'
    },
    'communing': {
        'definition': 'The act of communicating intimately or sharing thoughts and feelings in close spiritual or emotional connection. Communing often implies deep, meaningful interaction that goes beyond superficial conversation. This can occur between people, with nature, or in spiritual contexts where individuals seek connection with the divine or transcendent. The term suggests peaceful, reflective communication that creates understanding and unity.',
        'part_of_speech': 'verb (present participle)',
        'pronunciation_guide': 'kuh-MYOON-ing (/kəˈmjunɪŋ/)',
        'etymology': 'From Old French "comuner," from Latin "communicare" (to share)',
        'memory_tips': 'Think "commune + -ing" - actively sharing or connecting deeply with someone or something',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'She spent the morning _____ with nature during her peaceful forest walk.'
    },
    'communiqué': {
        'definition': 'An official announcement or statement, typically issued by a government, military organization, or other authority to provide information to the public or media. Communiqués are formal communications that convey important news, policy changes, or official positions on significant matters. These statements are often carefully worded and released through official channels to ensure accurate dissemination of information.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kuh-MYOO-nuh-kay (/kəˈmjunɪkeɪ/)',
        'etymology': 'French, past participle of "communiquer" (to communicate)',
        'memory_tips': 'Think "communicate" with French accent - an official communication or announcement',
        'alternate_spellings': 'Communique (without accent)',
        'language_origin': 'French',
        'example_sentence': 'The embassy issued a _____ clarifying its position on the diplomatic negotiations.'
    },
    'communities': {
        'definition': 'Plural of community; groups of people living in the same area or sharing common interests, characteristics, or goals. Communities can be geographical (neighborhoods, towns), social (religious groups, professional associations), or virtual (online communities). These groups typically share resources, responsibilities, and mutual support systems. Modern communities may be physical or digital, united by proximity, shared values, or common purposes.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'kuh-MYOO-nuh-teez (/kəˈmjunɪtiz/)',
        'etymology': 'Plural of Latin "communitas," from "communis" (common, shared)',
        'memory_tips': 'Think "common + -ities" - groups with common interests or locations',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Online _____ provide support networks for people with shared interests worldwide.'
    },
    'commute': {
        'definition': 'To travel regularly between home and work, typically over a considerable distance. As a verb, commute can also mean to reduce a punishment or exchange one thing for another. The noun refers to the journey itself, often involving public transportation or personal vehicles. Modern commuting includes remote work arrangements and flexible schedules. Commuting patterns significantly impact urban planning, transportation systems, and quality of life.',
        'part_of_speech': 'verb, noun',
        'pronunciation_guide': 'kuh-MYOOT (/kəˈmjut/)',
        'etymology': 'From Latin "commutare," meaning "to change completely"',
        'memory_tips': 'Think "com- (completely) + mute (change)" - completely changing location regularly',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Her daily _____ takes an hour each way on the subway system.'
    },
    'companion': {
        'definition': 'A person who accompanies or associates with another; a friend, partner, or fellow traveler who provides company and often emotional support. Companions share experiences, offer mutual assistance, and maintain ongoing relationships. The term can describe human relationships, animal relationships (companion animals), or even objects that accompany people regularly. Companionship implies loyalty, shared time, and mutual benefit in the relationship.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kum-PAN-yun (/kəmˈpænjən/)',
        'etymology': 'From Latin "companio," literally "bread-fellow," from "com-" (with) + "panis" (bread)',
        'memory_tips': 'Think "com- (with) + pan (bread)" - someone you share bread with, a close friend',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The elderly woman\'s dog served as her faithful _____ during long walks.'
    },
    'company': {
        'definition': 'A commercial business organization engaged in the production or sale of goods or services. Company also refers to companionship or the presence of others, as in "enjoying good company." In military contexts, a company is a subdivision of a regiment. The term encompasses various business structures from small partnerships to large corporations, emphasizing collective effort toward commercial goals.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KUM-puh-nee (/ˈkʌmpəni/)',
        'etymology': 'From Latin "companio" (companion), extended to mean "group of companions"',
        'memory_tips': 'Think of companions working together - a company is a group working together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The technology _____ developed innovative software solutions for small businesses.'
    },
    'comparison': {
        'definition': 'The act of examining similarities and differences between two or more items, ideas, or situations to understand their relative qualities or characteristics. Comparison involves analytical thinking to identify patterns, contrasts, and relationships. This process is fundamental to learning, decision-making, and understanding. Comparisons can be objective (measurable differences) or subjective (personal preferences or interpretations).',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kum-PAIR-uh-sun (/kəmˈpɛrɪsən/)',
        'etymology': 'From Latin "comparatio," from "comparare" (to pair together)',
        'memory_tips': 'Think "compare + -ison" - the act of comparing things to find similarities and differences',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ between the two smartphones helped her choose the better option.'
    },
    'compass': {
        'definition': 'A navigational instrument that shows direction relative to magnetic north, essential for orientation and navigation. Compass also refers to the range or scope of something, as in "beyond the compass of human understanding." In drawing, a compass is a tool used to create circles and arcs. Metaphorically, compass represents guidance, direction, or moral orientation in life decisions.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KUM-pus (/ˈkʌmpəs/)',
        'etymology': 'From Latin "compassus," meaning "measured pace" or "circle"',
        'memory_tips': 'Think of a circle (compass draws circles) or finding direction (navigation compass)',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The hiker used her _____ to navigate through the unfamiliar mountain trail.'
    },
    'compatriots': {
        'definition': 'Fellow citizens of the same country; people who share the same nationality or homeland. Compatriots often share common cultural heritage, legal systems, and national identity. The term emphasizes solidarity and mutual connection based on shared citizenship, particularly relevant in discussions of patriotism, national identity, or when citizens live abroad. Compatriots may support each other in foreign countries or during national challenges.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'kum-PAY-tree-uts (/kəmˈpeɪtriəts/)',
        'etymology': 'From Latin "compatriota," from "com-" (together) + "patria" (fatherland)',
        'memory_tips': 'Think "com- (together) + patri (father/homeland)" - people sharing the same fatherland',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The ambassador welcomed his _____ to the embassy\'s cultural celebration.'
    },
    'compelling': {
        'definition': 'Forcefully persuasive, captivating, or evoking strong interest and attention. Something compelling demands notice through its powerful appeal, logical strength, or emotional impact. This can describe arguments that are convincing, stories that are engaging, or evidence that is irrefutable. Compelling suggests an almost irresistible quality that draws people in and influences their thoughts or actions.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kum-PEL-ing (/kəmˈpɛlɪŋ/)',
        'etymology': 'From Latin "compellere," meaning "to drive together, force"',
        'memory_tips': 'Think "compel + -ing" - something that compels or forces your attention',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The documentary presented _____ evidence about climate change impacts.'
    },
    'compendium': {
        'definition': 'A comprehensive collection or summary of information on a particular subject, typically presented in a concise format. Compendiums gather extensive knowledge into accessible, organized presentations, serving as reference works or educational resources. These collections can cover academic subjects, practical skills, or specialized fields, providing readers with essential information without requiring extensive research through multiple sources.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kum-PEN-dee-um (/kəmˈpɛndiəm/)',
        'etymology': 'From Latin "compendium," meaning "a saving, shortcut," from "compendere" (to weigh together)',
        'memory_tips': 'Think "com- (together) + pend (weigh)" - weighing information together in one collection',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The medical _____ contained essential information for emergency room procedures.'
    },
    'compete': {
        'definition': 'To strive against others to achieve a goal, win a prize, or demonstrate superiority in a particular activity. Competition involves effort, skill, and determination to outperform rivals in sports, academics, business, or other endeavors. Competing can drive innovation, improvement, and excellence while also creating challenges related to pressure and rivalry. Healthy competition promotes growth and achievement.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'kum-PEET (/kəmˈpit/)',
        'etymology': 'From Latin "competere," meaning "to strive together," from "com-" (together) + "petere" (to seek)',
        'memory_tips': 'Think "com- (together) + pete (seek)" - seeking the same goal together with rivals',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Athletes from around the world will _____ in the international swimming championships.'
    },
    'competing': {
        'definition': 'Present participle of compete; actively striving against others or engaging in rivalry to achieve a goal. Competing involves ongoing effort to outperform opponents in various contexts such as sports, business, or academics. The term can also describe conflicting interests or priorities that vie for attention or resources. Competing forces or ideas create tension that often leads to resolution or compromise.',
        'part_of_speech': 'verb (present participle), adjective',
        'pronunciation_guide': 'kum-PEET-ing (/kəmˈpitɪŋ/)',
        'etymology': 'From Latin "competere" + present participle suffix "-ing"',
        'memory_tips': 'Think "compete + -ing" - actively in the process of competing with others',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ restaurants offered increasingly attractive deals to win customers.'
    },
    'competitive': {
        'definition': 'Having a strong desire to win or be more successful than others; involving competition or rivalry. Competitive people seek to outperform others and often thrive in challenging situations. In business contexts, competitive refers to market conditions where multiple companies vie for customers. Competitive advantages, prices, or strategies are designed to succeed against rivals. The term can describe both positive drive and potentially problematic behavior.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kum-PET-uh-tiv (/kəmˈpɛtətɪv/)',
        'etymology': 'From Latin "competere" + suffix "-ive" (having the quality of)',
        'memory_tips': 'Think "compete + -ive" - having the quality of wanting to compete and win',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Her _____ spirit helped her excel in both academics and athletics.'
    }
}

def process_batch():
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_038_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_038_processed.csv'
    
    try:
        df = pd.read_csv(input_file)
        print(f"Processing {len(df)} words from batch 038...")
        
        processed_data = []
        combined_word_errors = []
        
        for _, row in df.iterrows():
            word = row['word'].strip()
            if word in batch_038_data:
                data = batch_038_data[word]
                
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