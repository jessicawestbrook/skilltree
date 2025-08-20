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

batch_041_data = {
    'container': {
        'definition': 'A receptacle for holding or storing items; an object designed to enclose, protect, or transport contents. Containers range from simple boxes and jars to complex shipping containers and storage systems. They serve essential functions in packaging, storage, transportation, and organization. Modern containers include standardized shipping containers that revolutionized global trade.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-TAY-ner (/kənˈteɪnər/)',
        'etymology': 'From Latin "continere" (to hold together) + agent suffix "-er"',
        'memory_tips': 'Think "contain + -er" - something that contains other things',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The shipping _____ traveled from China to the United States loaded with electronics.'
    },
    'contains': {
        'definition': 'Third person singular present tense of contain; includes or holds within; keeps under control or restrains. When something contains other elements, it encompasses them as components or contents. The term can refer to physical containment (a box contains books) or conceptual inclusion (a theory contains several principles).',
        'part_of_speech': 'verb (third person singular present)',
        'pronunciation_guide': 'kun-TAYNZ (/kənˈteɪnz/)',
        'etymology': 'From Latin "continere" (to hold together, restrain)',
        'memory_tips': 'Think of holding things together inside - what a container does',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'This vitamin supplement _____ essential nutrients for daily health.'
    },
    'contemporary': {
        'definition': 'Belonging to the same time period; existing or occurring in the present time; modern or current. Contemporary can describe people living at the same time, artistic styles of the current era, or issues relevant to present-day society. The term emphasizes simultaneity and current relevance.',
        'part_of_speech': 'adjective, noun',
        'pronunciation_guide': 'kun-TEM-puh-rer-ee (/kənˈtɛmpəˌrɛri/)',
        'etymology': 'From Latin "contemporarius," from "con-" (together) + "tempus" (time)',
        'memory_tips': 'Think "con- (together) + tempor (time)" - existing together in the same time',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The museum featured _____ art from living artists around the world.'
    },
    'contemptible': {
        'definition': 'Deserving contempt or scorn; morally reprehensible or despicable. Contemptible actions or people evoke strong disapproval due to their lack of moral worth, dignity, or honor. This judgment implies that something falls below acceptable standards of behavior or character.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kun-TEMP-tuh-bul (/kənˈtɛmptəbəl/)',
        'etymology': 'From Latin "contemptibilis," from "contemnere" (to despise)',
        'memory_tips': 'Think "contempt + -ible" - worthy of contempt or scorn',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'His _____ behavior toward the homeless showed his lack of compassion.'
    },
    'contemptuous': {
        'definition': 'Showing or expressing contempt, scorn, or disdain; feeling or displaying superiority and disrespect toward someone or something considered inferior. Contemptuous attitudes involve looking down on others with arrogance, dismissing them as unworthy of respect or consideration.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kun-TEMP-choo-us (/kənˈtɛmptʃuəs/)',
        'etymology': 'From Latin "contemptuosus," from "contemnere" (to despise)',
        'memory_tips': 'Think "contempt + -uous" - full of contempt or scornful feelings',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'She gave him a _____ look when he suggested the obviously flawed plan.'
    },
    'content': {
        'definition': 'Satisfied with what one has; not wanting more or different; the subject matter or material contained in something. As a noun, content refers to the information, ideas, or material within books, websites, or other media. As an adjective, it describes a state of peaceful satisfaction.',
        'part_of_speech': 'adjective, noun',
        'pronunciation_guide': 'kun-TENT (adj.), KON-tent (noun) (/kənˈtɛnt/, /ˈkɒntɛnt/)',
        'etymology': 'From Latin "contentus," meaning "satisfied, contained"',
        'memory_tips': 'Think of being satisfied with what is "contained" in your life',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'She was _____ to spend the evening reading rather than going out.'
    },
    'contents': {
        'definition': 'Plural of content; the things that are contained within something; the subjects or topics covered in a book, document, or other work. Contents can refer to physical items (contents of a box) or abstract elements (contents of a curriculum). Often appears in "table of contents."',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KON-tents (/ˈkɒntɛnts/)',
        'etymology': 'Plural of Latin "contentus" (that which is contained)',
        'memory_tips': 'Think of multiple things contained inside something',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The table of _____ showed that the book had twelve chapters.'
    },
    'contessa': {
        'definition': 'An Italian countess; a woman holding the rank of count in her own right or the wife of a count. This aristocratic title represents nobility and high social status in Italian society and other European cultures. The title carries historical significance and social prestige.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-TES-uh (/kɒnˈtɛsə/)',
        'etymology': 'Italian, feminine form of "conte" (count), from Latin "comes" (companion)',
        'memory_tips': 'Think of Italian nobility - a female count or countess',
        'alternate_spellings': 'Countess (English equivalent)',
        'language_origin': 'Italian',
        'example_sentence': 'The _____ hosted an elegant dinner party at her Tuscan villa.'
    },
    'contested': {
        'definition': 'Past tense of contest; disputed, challenged, or competed for; questioned or opposed rather than accepted. Contested issues face opposition or debate, while contested elections involve multiple candidates competing. The term implies disagreement, competition, or challenge to established positions.',
        'part_of_speech': 'verb (past tense), adjective',
        'pronunciation_guide': 'kun-TES-ted (/kənˈtɛstəd/)',
        'etymology': 'From Latin "contestari" (to call to witness) + past tense "-ed"',
        'memory_tips': 'Think of something that was challenged or competed for in a contest',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The election results were _____ by several candidates who demanded recounts.'
    },
    'conteur': {
        'definition': 'A storyteller; someone skilled in narrating tales, especially in an entertaining or captivating manner. This French term emphasizes the artistry of oral storytelling, often used to describe professional entertainers who specialize in narrative performance. Conteurs possess charisma and skill in engaging audiences through voice and gesture.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-TUR (/kɒnˈtʊr/)',
        'etymology': 'French, from "conter" (to tell, relate), from Latin "computare"',
        'memory_tips': 'Think "conte (tale) + -eur (one who does)" - one who tells tales',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The village _____ captivated children with magical folk tales every evening.'
    },
    'context': {
        'definition': 'The circumstances, background, or setting that surrounds and gives meaning to an event, statement, or idea. Context provides the framework for understanding by showing relationships, influences, and relevant factors. Without context, information can be misunderstood or lose its intended meaning.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KON-tekst (/ˈkɒntɛkst/)',
        'etymology': 'From Latin "contextus," meaning "woven together"',
        'memory_tips': 'Think "con- (together) + text (woven)" - information woven together for understanding',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'To understand the joke, you need to know the _____ of their previous conversation.'
    },
    'contexts': {
        'definition': 'Plural of context; multiple circumstances, backgrounds, or settings that provide meaning to different events, statements, or ideas. Different contexts can change interpretation and significance of the same information. Understanding various contexts helps develop comprehensive knowledge and cultural sensitivity.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KON-teksts (/ˈkɒntɛksts/)',
        'etymology': 'Plural of Latin "contextus" (woven together)',
        'memory_tips': 'Multiple settings or circumstances that provide different frameworks for understanding',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The same phrase can have different meanings in various cultural _____.'
    },
    'conticent': {
        'definition': 'Silent, quiet, or refraining from speech; choosing not to speak or express opinions. This formal term describes someone who maintains silence, whether by choice, habit, or circumstance. Conticent behavior can indicate thoughtfulness, secrecy, or simply a preference for listening rather than speaking.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KON-ti-sent (/ˈkɒntɪsənt/)',
        'etymology': 'From Latin "conticens," present participle of "conticere" (to be silent)',
        'memory_tips': 'Think "con- (completely) + ticent (silent)" - completely silent or quiet',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The usually talkative student remained _____ during the difficult discussion.'
    },
    'contiguous': {
        'definition': 'Adjacent, touching, or sharing a common border; next to and in contact with something else. Contiguous areas are connected without gaps, breaks, or interruptions between them. This term is commonly used in geography, real estate, and describing physical relationships between objects or regions.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kun-TIG-yoo-us (/kənˈtɪgjuəs/)',
        'etymology': 'From Latin "contiguus," from "contingere" (to touch)',
        'memory_tips': 'Think "con- (together) + tig (touch)" - touching together with no gaps',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The three _____ states formed a natural economic region.'
    },
    'continent': {
        'definition': 'One of the main landmasses of the Earth (Asia, Africa, North America, South America, Antarctica, Europe, Australia); showing self-restraint, especially in relation to sexual behavior. As a geographical term, continents are large continuous areas of land. As an adjective, continent describes moral self-control.',
        'part_of_speech': 'noun, adjective',
        'pronunciation_guide': 'KON-tuh-nunt (/ˈkɒntənənt/)',
        'etymology': 'From Latin "continens," meaning "holding together, continuous"',
        'memory_tips': 'Think of "continuous" land - large landmasses that hold together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Africa is the second-largest _____ by both area and population.'
    },
    'continental': {
        'definition': 'Relating to or characteristic of a continent, especially the European continent; showing refined, sophisticated manners associated with continental European culture. Continental can describe climate patterns, cuisine, or cultural practices typical of large landmasses rather than islands.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kon-tuh-NEN-tul (/ˌkɒntəˈnɛntəl/)',
        'etymology': 'From Latin "continentalis," relating to a continent',
        'memory_tips': 'Think "continent + -al" - relating to or characteristic of a continent',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The hotel served a _____ breakfast with pastries and European coffee.'
    },
    'contingent': {
        'definition': 'Dependent on circumstances or conditions; possible but not certain; a group of people representing an organization or country. As an adjective, contingent means conditional or dependent on factors. As a noun, it refers to a delegation or representative group.',
        'part_of_speech': 'adjective, noun',
        'pronunciation_guide': 'kun-TIN-junt (/kənˈtɪndʒənt/)',
        'etymology': 'From Latin "contingens," meaning "touching, happening"',
        'memory_tips': 'Think of something that "touches" or depends on other conditions',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The project\'s success is _____ upon receiving additional funding.'
    },
    'continue': {
        'definition': 'To persist in a course of action; to keep going without stopping; to resume after an interruption. Continuing implies ongoing effort, sustained activity, or unbroken progression toward a goal. The term emphasizes persistence and maintenance of direction or activity.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'kun-TIN-yoo (/kənˈtɪnju/)',
        'etymology': 'From Latin "continuare," from "continuus" (uninterrupted)',
        'memory_tips': 'Think of maintaining an uninterrupted flow or progression',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Please _____ reading the instructions until you reach the end.'
    },
    'continuous': {
        'definition': 'Uninterrupted, ongoing, or constant; forming an unbroken sequence or stream. Continuous processes have no gaps, breaks, or interruptions in their flow or progression. This term describes sustained activity, consistent patterns, or unbroken connections in time or space.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kun-TIN-yoo-us (/kənˈtɪnjuəs/)',
        'etymology': 'From Latin "continuus," meaning "uninterrupted, connected"',
        'memory_tips': 'Think of something that continues without breaks - an unbroken flow',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The machine provided _____ operation for twenty-four hours without stopping.'
    },
    'continuum': {
        'definition': 'A continuous sequence or range where adjacent elements are virtually indistinguishable from each other, but extremes are quite different. Continuums exist in physics (space-time), color (spectrum), and abstract concepts (political ideologies). The term emphasizes gradual transition rather than discrete categories.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-TIN-yoo-um (/kənˈtɪnjuəm/)',
        'etymology': 'Latin, neuter of "continuus" (continuous)',
        'memory_tips': 'Think of a continuous spectrum where everything blends together gradually',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Color exists on a _____ from red through orange to yellow.'
    },
    'contorted': {
        'definition': 'Twisted, bent, or forced into an unnatural or strained position; distorted out of normal shape. Contortion can be physical (twisted features) or metaphorical (contorted logic). The term implies departure from natural form through force, stress, or deliberate manipulation.',
        'part_of_speech': 'adjective, verb (past tense)',
        'pronunciation_guide': 'kun-TOR-ted (/kənˈtɔrtəd/)',
        'etymology': 'From Latin "contortus," from "contorquere" (to twist together)',
        'memory_tips': 'Think "con- (together) + tort (twist)" - twisted together in unnatural ways',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'His face was _____ with pain after injuring his back.'
    },
    'contraction': {
        'definition': 'The process of becoming smaller, tighter, or more compact; a shortened form of words (like "don\'t" for "do not"); the tightening of muscles, especially during childbirth. Contractions occur in various contexts: economic (market contraction), linguistic (word shortening), and physiological (muscle tightening).',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-TRAK-shun (/kənˈtrækʃən/)',
        'etymology': 'From Latin "contractio," from "contrahere" (to draw together)',
        'memory_tips': 'Think "con- (together) + tract (draw)" - drawing together or shrinking',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The economic _____ led to reduced consumer spending and job losses.'
    },
    'contradictory': {
        'definition': 'Containing elements that oppose or conflict with each other; inconsistent or mutually exclusive. Contradictory statements, ideas, or evidence cannot all be true simultaneously. This quality creates logical problems, confusion, or the need to resolve opposing claims through further investigation.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kon-truh-DIK-tuh-ree (/ˌkɒntrəˈdɪktəri/)',
        'etymology': 'From Latin "contradictorius," from "contradicere" (to speak against)',
        'memory_tips': 'Think "contra- (against) + dict (speak)" - speaking against each other',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The witness gave _____ testimony that confused the jury.'
    },
    'contrapposto': {
        'definition': 'An artistic technique in sculpture and painting where the human figure is positioned with weight shifted to one leg, creating a natural, relaxed stance. This Italian Renaissance concept shows figures in asymmetrical but balanced poses, suggesting movement and life. Contrapposto revolutionized artistic representation of the human body.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-truh-POS-toh (/ˌkɒntrəˈpɒstoʊ/)',
        'etymology': 'Italian, meaning "set against," from Latin "contra" (against) + "positus" (placed)',
        'memory_tips': 'Think "contra- (against) + posto (placed)" - placed in opposition for natural balance',
        'alternate_spellings': 'None',
        'language_origin': 'Italian',
        'example_sentence': 'Michelangelo\'s David exemplifies perfect _____ with its natural, balanced stance.'
    },
    'contraption': {
        'definition': 'A mechanical device or machine, especially one that appears strange, unnecessarily complicated, or makeshift in construction. Contraptions often seem jury-rigged or overly complex for their intended purpose. The term suggests mechanical ingenuity combined with questionable design choices.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-TRAP-shun (/kənˈtræpʃən/)',
        'etymology': 'Possibly from "contrive" + "apparatus" or related to "contrivance"',
        'memory_tips': 'Think of a complex, strange-looking machine that somehow works',
        'alternate_spellings': 'None',
        'language_origin': 'English (possibly blend)',
        'example_sentence': 'The inventor\'s bizarre _____ successfully cracked nuts using seventeen moving parts.'
    },
    'contrariwise': {
        'definition': 'On the contrary; in the opposite manner or direction; conversely. This formal adverb introduces statements that oppose or reverse previously mentioned ideas. Contrariwise signals a logical turn that presents alternative viewpoints or contradictory evidence.',
        'part_of_speech': 'adverb',
        'pronunciation_guide': 'kun-TRAIR-ee-wyze (/kənˈtrɛriwaɪz/)',
        'etymology': 'From "contrary" + suffix "-wise" (in the manner of)',
        'memory_tips': 'Think "contrary + -wise" - in a contrary or opposite manner',
        'alternate_spellings': 'None',
        'language_origin': 'English',
        'example_sentence': 'The data suggested growth; _____, actual sales declined significantly.'
    },
    'contretemps': {
        'definition': 'An unexpected and unfortunate occurrence; an awkward or embarrassing situation; a minor dispute or disagreement. This French term describes social mishaps, timing problems, or situations that create discomfort through poor timing or unfortunate circumstances.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KON-truh-tahn (/ˈkɒntrətɑ̃/)',
        'etymology': 'French, meaning "against time," from "contre" (against) + "temps" (time)',
        'memory_tips': 'Think "contre (against) + temps (time)" - something that goes against good timing',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The diplomatic _____ embarrassed both countries during the state visit.'
    },
    'contribute': {
        'definition': 'To give or provide something (money, time, effort, ideas) to help achieve a common goal; to be instrumental in bringing about a result. Contributing involves voluntary participation in shared endeavors, whether financial donations, intellectual input, or physical effort toward collective objectives.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'kun-TRIB-yoot (/kənˈtrɪbjut/)',
        'etymology': 'From Latin "contribuere," from "con-" (together) + "tribuere" (to give)',
        'memory_tips': 'Think "con- (together) + trib (give)" - giving together toward a common cause',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Volunteers _____ their time to help rebuild homes after the disaster.'
    },
    'contributors': {
        'definition': 'Plural of contributor; people who give money, time, effort, or expertise to support a cause, project, or publication. Contributors can be financial donors, authors, researchers, or anyone who provides resources toward shared goals. Their participation enables larger accomplishments than individual efforts alone.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'kun-TRIB-yoo-turz (/kənˈtrɪbjətərz/)',
        'etymology': 'Plural of Latin "contributor," from "contribuere" (to give together)',
        'memory_tips': 'Multiple people who give or contribute to something together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The magazine thanked all _____ who submitted articles for the special issue.'
    },
    'contrite': {
        'definition': 'Feeling or showing deep remorse for wrongdoing; genuinely sorry and repentant for mistakes or sins. Contrition involves sincere regret accompanied by willingness to make amends or change behavior. This emotional state reflects moral awareness and desire for redemption.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kun-TRYT (/kənˈtraɪt/) or KON-tryt (/ˈkɒntraɪt/)',
        'etymology': 'From Latin "contritus," meaning "worn down, crushed with grief"',
        'memory_tips': 'Think of being "crushed" with guilt and remorse for wrongdoing',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ student apologized sincerely for cheating on the exam.'
    },
    'contrivance': {
        'definition': 'Something cleverly or skillfully constructed; an artificial arrangement or scheme; the act of devising or creating something. Contrivances can be mechanical devices, artistic techniques, or social arrangements created through ingenuity. The term can imply either admirable cleverness or excessive artificiality.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-TRY-vuhns (/kənˈtraɪvəns/)',
        'etymology': 'From Old French "controvance," from "controver" (to find, devise)',
        'memory_tips': 'Think "contrive + -ance" - something contrived or cleverly devised',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'The plot\'s happy ending felt like an artificial _____ rather than natural resolution.'
    },
    'controlled': {
        'definition': 'Past tense of control; managed, regulated, or restrained; kept within limits or under authority. Controlled conditions are deliberately maintained for experiments or safety. Controlled behavior shows self-discipline and emotional regulation. The term implies deliberate management and restraint.',
        'part_of_speech': 'verb (past tense), adjective',
        'pronunciation_guide': 'kun-TROHLD (/kənˈtroʊld/)',
        'etymology': 'From Middle French "contrôler" + past tense "-ed"',
        'memory_tips': 'Think of keeping something under control or management',
        'alternate_spellings': 'None',
        'language_origin': 'Middle French',
        'example_sentence': 'The scientist conducted the experiment under carefully _____ laboratory conditions.'
    },
    'controversy': {
        'definition': 'Prolonged public disagreement or heated discussion about a topic that divides opinion; a dispute involving strongly opposing viewpoints. Controversies often involve moral, political, scientific, or social issues where people hold passionate but conflicting beliefs. They generate debate and sometimes social division.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KON-truh-vur-see (/ˈkɒntrəvərsi/) or kun-TROV-ur-see (/kənˈtrɒvərsi/)',
        'etymology': 'From Latin "controversia," from "controversus" (turned against)',
        'memory_tips': 'Think "contro- (against) + vers (turn)" - people turned against each other in argument',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The proposed law sparked intense _____ among lawmakers and citizens.'
    },
    'contumelious': {
        'definition': 'Expressing contempt or insult in a haughty, insolent manner; characterized by arrogant abuse or scornful reproach. Contumelious behavior involves deliberately offensive language or actions intended to humiliate or degrade others. This conduct shows extreme disrespect and superiority.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kon-too-MEE-lee-us (/ˌkɒntuˈmiliəs/)',
        'etymology': 'From Latin "contumeliosus," from "contumelia" (insult, abuse)',
        'memory_tips': 'Think of insulting behavior that shows contempt and arrogance',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'His _____ remarks about her appearance were completely inappropriate.'
    },
    'contusion': {
        'definition': 'A bruise; an injury where blood vessels under the skin are damaged by impact, causing discoloration without breaking the skin surface. Contusions result from blunt trauma that crushes small blood vessels, creating characteristic purple, blue, or yellow marks as healing progresses.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-TOO-zhun (/kənˈtuʒən/)',
        'etymology': 'From Latin "contusio," from "contundere" (to beat, bruise)',
        'memory_tips': 'Think "con- (thoroughly) + tus (beat)" - thoroughly beaten, resulting in a bruise',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The athlete suffered a painful _____ on his shoulder during the collision.'
    },
    'contusionconundrum': {
        'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "contusion" (a bruise) + "conundrum" (a puzzling problem). These should be separate words.',
        'part_of_speech': 'error - combined words',
        'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
        'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
        'memory_tips': 'This is a data error - should be separated into "contusion" and "conundrum"',
        'alternate_spellings': 'contusion + conundrum (separate words)',
        'language_origin': 'ERROR - combined words',
        'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
    },
    'conundrum': {
        'definition': 'A confusing and difficult problem or question; a puzzle that seems to have no satisfactory solution. Conundrums often involve logical paradoxes, moral dilemmas, or complex situations where all available options have significant drawbacks. They challenge conventional thinking and problem-solving approaches.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kuh-NUN-drum (/kəˈnʌndrəm/)',
        'etymology': 'Origin uncertain, possibly from Latin academic slang meaning "whim, fancy"',
        'memory_tips': 'Think of a puzzle that makes you go "hmmm" - a puzzling problem',
        'alternate_spellings': 'None',
        'language_origin': 'Uncertain (possibly Latin)',
        'example_sentence': 'The budget cuts presented a _____ : how to maintain quality while reducing costs.'
    },
    'conurbation': {
        'definition': 'An extended urban area consisting of several towns, cities, or metropolitan areas that have grown and merged together. Conurbations form when separate settlements expand until their boundaries meet, creating continuous built-up regions. These mega-cities often share infrastructure, transportation networks, and economic systems.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-ur-BAY-shun (/ˌkɒnərˈbeɪʃən/)',
        'etymology': 'From Latin "con-" (together) + "urbs" (city) + suffix "-ation"',
        'memory_tips': 'Think "con- (together) + urb (city)" - cities grown together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The northeastern _____ stretches from Boston to Washington, D.C.'
    },
    'convalesce': {
        'definition': 'To recover gradually from illness or medical treatment; to regain health and strength after being sick or injured. Convalescence is the healing period between acute illness and full recovery, typically involving rest, gradual activity increase, and careful monitoring of progress.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'kon-vuh-LES (/ˌkɒnvəˈlɛs/)',
        'etymology': 'From Latin "convalescere," from "con-" (intensive) + "valescere" (to grow strong)',
        'memory_tips': 'Think "con- (thoroughly) + vales (strong)" - growing thoroughly strong again',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'After surgery, she needed several weeks to _____ at home.'
    },
    'convention': {
        'definition': 'A large meeting or conference of people with shared interests; established practices, customs, or rules widely accepted in society; a formal agreement between countries. Conventions can be social gatherings, behavioral norms, or international treaties that govern conduct.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-VEN-shun (/kənˈvɛnʃən/)',
        'etymology': 'From Latin "conventio," from "convenire" (to come together)',
        'memory_tips': 'Think "con- (together) + ven (come)" - coming together for a meeting or agreement',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The comic book _____ attracted thousands of fans from around the country.'
    },
    'conversation': {
        'definition': 'An informal exchange of ideas, thoughts, or information between two or more people through spoken words. Conversations involve turn-taking, listening, responding, and developing topics collaboratively. They serve social, educational, and emotional functions in human relationships.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-vur-SAY-shun (/ˌkɒnvərˈseɪʃən/)',
        'etymology': 'From Latin "conversatio," meaning "living with, social interaction"',
        'memory_tips': 'Think "con- (together) + vers (turn)" - taking turns speaking together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Their _____ about travel sparked plans for a European vacation.'
    },
    'conveyance': {
        'definition': 'The action of transporting or carrying someone or something from one place to another; a vehicle or other means of transport; the legal transfer of property ownership. Conveyance can refer to physical transportation, legal documents, or the general concept of moving things.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-VAY-uhns (/kənˈveɪəns/)',
        'etymology': 'From Old French "conveyance," from "conveier" (to escort, conduct)',
        'memory_tips': 'Think "convey + -ance" - the act or means of conveying something',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'The horse-drawn carriage served as their primary _____ to town.'
    },
    'convictions': {
        'definition': 'Plural of conviction; firmly held beliefs or opinions; legal judgments that someone is guilty of a crime. Convictions can be moral principles that guide behavior or legal determinations resulting from criminal trials. Both meanings involve certainty and formal determination.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'kun-VIK-shunz (/kənˈvɪkʃənz/)',
        'etymology': 'Plural of Latin "convictio," from "convincere" (to prove guilty)',
        'memory_tips': 'Think of being "convinced" - either of beliefs or guilt in court',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Her strong _____ about environmental protection influenced her career choice.'
    },
    'convince': {
        'definition': 'To persuade someone to believe or accept something; to cause someone to be certain that something is true or wise. Convincing involves presenting evidence, arguments, or appeals that change minds or overcome doubts. Successful persuasion requires understanding audience concerns and motivations.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'kun-VINS (/kənˈvɪns/)',
        'etymology': 'From Latin "convincere," meaning "to overcome, prove wrong"',
        'memory_tips': 'Think "con- (thoroughly) + vinc (conquer)" - thoroughly conquering doubt or opposition',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'She worked hard to _____ the committee that her proposal was feasible.'
    },
    'convivium': {
        'definition': 'A feast or banquet, especially in ancient Roman culture; a social gathering centered around food and drink where people engage in conversation and entertainment. Convivia were important social and political events that strengthened relationships and conducted business in relaxed settings.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-VIV-ee-um (/kənˈvɪviəm/)',
        'etymology': 'Latin, meaning "a living together, feast," from "con-" (together) + "vivere" (to live)',
        'memory_tips': 'Think "con- (together) + viv (live)" - living together at a feast',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The Roman senator hosted an elaborate _____ for distinguished guests.'
    },
    'convocation': {
        'definition': 'A large formal assembly or meeting, especially of members of a university, religious organization, or professional group. Convocations often mark special occasions like graduations, ceremonial events, or important institutional gatherings. They emphasize solemnity and collective purpose.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-vuh-KAY-shun (/ˌkɒnvəˈkeɪʃən/)',
        'etymology': 'From Latin "convocatio," from "convocare" (to call together)',
        'memory_tips': 'Think "con- (together) + voc (call)" - calling people together for a meeting',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The university\'s annual _____ celebrated outstanding student achievements.'
    },
    'convoy': {
        'definition': 'A group of vehicles, ships, or aircraft traveling together for mutual protection or support; to escort or accompany for protection. Convoys provide security through numbers, coordinated movement, and shared defense. They\'re commonly used in military operations and dangerous territories.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KON-voy (/ˈkɒnvɔɪ/)',
        'etymology': 'From French "convoyer," meaning "to escort," from Latin "con-" (with) + "via" (way)',
        'memory_tips': 'Think "con- (with) + voy (way)" - traveling the way together with others',
        'alternate_spellings': 'None',
        'language_origin': 'French/Latin',
        'example_sentence': 'The military _____ transported supplies safely through hostile territory.'
    },
    'convulsive': {
        'definition': 'Characterized by or causing convulsions; involving sudden, violent, involuntary movements or contractions. Convulsive can describe medical conditions (seizures), emotional states (convulsive sobs), or social phenomena (convulsive changes). The term emphasizes intensity and lack of control.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kun-VUL-siv (/kənˈvʌlsɪv/)',
        'etymology': 'From Latin "convulsivus," from "convellere" (to tear away, convulse)',
        'memory_tips': 'Think "con- (thoroughly) + vuls (tear)" - thoroughly tearing or shaking movements',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The patient experienced _____ tremors during the medical episode.'
    },
    'cooked': {
        'definition': 'Past tense of cook; prepared by heating food to make it edible; altered or manipulated dishonestly (slang). Cooked food has been transformed through heat application, changing its texture, flavor, and safety. In informal usage, "cooked" can mean fabricated or falsified.',
        'part_of_speech': 'verb (past tense), adjective',
        'pronunciation_guide': 'KOOKT (/kʊkt/)',
        'etymology': 'From Old English "coc" (cook) + past tense ending "-ed"',
        'memory_tips': 'Think of food transformed by heat into edible, tasty meals',
        'alternate_spellings': 'None',
        'language_origin': 'Old English',
        'example_sentence': 'She _____ a delicious dinner with fresh vegetables from the garden.'
    },
    'cookie': {
        'definition': 'A small, sweet baked treat typically made with flour, sugar, and butter; in computing, a small piece of data stored by websites on users\' computers to remember information. Cookies range from simple sugar cookies to complex decorated varieties, while digital cookies track user preferences and activities.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KOOK-ee (/ˈkʊki/)',
        'etymology': 'From Dutch "koekje," diminutive of "koek" (cake)',
        'memory_tips': 'Think of small, sweet treats that are smaller than cakes',
        'alternate_spellings': 'None',
        'language_origin': 'Dutch',
        'example_sentence': 'The chocolate chip _____ was still warm from the oven.'
    }
}

def process_batch():
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_041_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_041_processed.csv'
    
    try:
        df = pd.read_csv(input_file)
        print(f"Processing {len(df)} words from batch 041...")
        
        processed_data = []
        combined_word_errors = []
        
        for _, row in df.iterrows():
            word = row['word'].strip()
            if word in batch_041_data:
                data = batch_041_data[word]
                
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