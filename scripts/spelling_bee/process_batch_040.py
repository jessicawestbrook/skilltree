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

batch_040_data = {
    'confused': {
        'definition': 'Uncertain, bewildered, or unable to think clearly; lacking clarity or understanding about a situation, concept, or instruction. Confusion can result from complex information, contradictory signals, or overwhelming circumstances. When confused, individuals may struggle to make decisions, follow directions, or comprehend what is happening around them. This mental state often requires clarification or additional information to resolve.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kun-FYOOZD (/kənˈfjuzd/)',
        'etymology': 'From Latin "confusus," past participle of "confundere" (to pour together, mix up)',
        'memory_tips': 'Think "con- (together) + fus (pour)" - ideas poured together in a mixed-up way',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The student looked _____ after hearing the complex mathematical explanation.'
    },
    'confusion': {
        'definition': 'A state of being uncertain, perplexed, or lacking clear understanding; a situation where things are mixed up or unclear. Confusion can arise from ambiguous information, conflicting instructions, or overwhelming complexity. It represents a temporary inability to distinguish between options or understand relationships between concepts. Resolving confusion typically requires clarification, organization, or additional learning.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-FYOO-zhun (/kənˈfjuʒən/)',
        'etymology': 'From Latin "confusio," from "confundere" (to pour together, disorder)',
        'memory_tips': 'Think of ideas being "fused together" in a disordered way, creating confusion',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ about the meeting time led several people to arrive late.'
    },
    'congealing': {
        'definition': 'Present participle of congeal; the process of changing from liquid to semi-solid or solid state, typically due to cooling or chemical action. Congealing occurs when substances like blood, fat, or certain liquids thicken and solidify. The term can also describe ideas or plans that are beginning to take definite shape or form after a period of development.',
        'part_of_speech': 'verb (present participle)',
        'pronunciation_guide': 'kun-JEEL-ing (/kənˈdʒilɪŋ/)',
        'etymology': 'From Latin "congelare" (to freeze together), from "con-" (together) + "gelare" (to freeze)',
        'memory_tips': 'Think "con- (together) + gel" - coming together to form a gel-like substance',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The sauce was _____ as it cooled, making it difficult to pour.'
    },
    'congeniality': {
        'definition': 'The quality of being pleasant, friendly, and sociable; a warm and agreeable disposition that makes others feel comfortable. Congeniality involves genuine interest in others, easy conversation, and the ability to create harmonious social interactions. People with congeniality are often well-liked and effective at building positive relationships in both personal and professional settings.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-jee-nee-AL-i-tee (/kənˌdʒiniˈæləti/)',
        'etymology': 'From Latin "congenialis," meaning "of the same nature," from "con-" (together) + "genius" (nature)',
        'memory_tips': 'Think "con- (together) + genial" - having a nature that brings people together pleasantly',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Her natural _____ made her the perfect choice for the customer service position.'
    },
    'conglomerate': {
        'definition': 'A large corporation formed by merging or acquiring many different companies, often in unrelated industries; in geology, a rock composed of rounded fragments cemented together. Business conglomerates diversify risk by operating in multiple sectors. The term emphasizes the combination of diverse elements into a unified whole, whether in business structure or geological formation.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'kun-GLOM-ur-it (/kənˈglɒmərɪt/)',
        'etymology': 'From Latin "conglomeratus," from "con-" (together) + "glomerare" (to wind into a ball)',
        'memory_tips': 'Think "con- (together) + glomerate (gather in a ball)" - gathering different things together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The media _____ owned newspapers, television stations, and radio networks worldwide.'
    },
    'conglutinant': {
        'definition': 'Having the property of gluing or sticking together; serving to unite or bind separate parts. This medical and scientific term describes substances that promote healing by bringing tissue edges together, or materials that have adhesive properties. Conglutinant agents help in wound healing by facilitating the natural binding process of damaged tissues.',
        'part_of_speech': 'adjective, noun',
        'pronunciation_guide': 'kun-GLOO-tn-uhnt (/kənˈglutənənt/)',
        'etymology': 'From Latin "conglutinans," from "conglutinare" (to glue together)',
        'memory_tips': 'Think "con- (together) + glutin (glue)" - gluing things together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The surgeon applied a _____ substance to help the wound edges heal properly.'
    },
    'congo': {
        'definition': 'Referring to the Democratic Republic of the Congo or Republic of the Congo, countries in Central Africa named after the Congo River. The name can also refer to the Congo Basin, a vast rainforest region, or historically to the ancient Kingdom of Kongo. In various contexts, Congo represents African geography, culture, and history, particularly relating to the Congo River system.',
        'part_of_speech': 'noun (proper name)',
        'pronunciation_guide': 'KONG-goh (/ˈkɒŋgoʊ/)',
        'etymology': 'From the Kingdom of Kongo, possibly from Kikongo "nkongo" (hunter)',
        'memory_tips': 'Think of the great Congo River and the African countries named after it',
        'alternate_spellings': 'None',
        'language_origin': 'Kikongo (African)',
        'example_sentence': 'The explorers studied the biodiversity of the _____ rainforest ecosystem.'
    },
    'congratulate': {
        'definition': 'To express pleasure, approval, or admiration for someone\'s achievement, success, or good fortune; to offer praise and good wishes for accomplishments. Congratulations acknowledge effort, celebrate milestones, and strengthen social bonds by showing appreciation for others\' successes. This social ritual demonstrates support and shared joy in achievements.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'kun-GRACH-uh-layt (/kənˈgrætʃəleɪt/)',
        'etymology': 'From Latin "congratulari," from "con-" (together) + "gratulari" (to show joy)',
        'memory_tips': 'Think "con- (together) + gratulate (show joy)" - showing joy together with someone',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The family gathered to _____ the graduate on her academic achievement.'
    },
    'congregation': {
        'definition': 'A group of people assembled for religious worship; any gathering or assembly of people with a common purpose. In religious contexts, congregations form the community of believers who worship together regularly. The term can also apply to any organized group that meets for shared activities, discussions, or ceremonies.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kong-gri-GAY-shun (/ˌkɒŋgrɪˈgeɪʃən/)',
        'etymology': 'From Latin "congregatio," from "congregare" (to gather together)',
        'memory_tips': 'Think "con- (together) + greg (flock)" - a flock gathered together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ sang hymns together during the Sunday morning service.'
    },
    'conical': {
        'definition': 'Having the shape of a cone; tapering to a point from a circular base. Conical objects are characterized by their geometric form that narrows consistently from a wide bottom to a narrow top. This shape appears in nature (pine trees, volcano peaks) and human-made objects (ice cream cones, traffic cones, funnels).',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'KON-i-kul (/ˈkɒnɪkəl/)',
        'etymology': 'From Greek "konikos," from "konos" (cone)',
        'memory_tips': 'Think "cone + -ical" - having the characteristics of a cone shape',
        'alternate_spellings': 'None',
        'language_origin': 'Greek',
        'example_sentence': 'The _____ mountain peak was visible from miles away.'
    },
    'conifers': {
        'definition': 'Evergreen trees and shrubs that produce cones and typically have needle-like or scale-like leaves. Conifers include pines, spruces, firs, cedars, and redwoods. These plants are adapted to various climates and are important for lumber, paper production, and ecological systems. Most conifers retain their foliage year-round and reproduce through cone structures containing seeds.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KOH-nuh-furz (/ˈkoʊnəfərz/)',
        'etymology': 'From Latin "conifer," meaning "cone-bearing," from "conus" (cone) + "ferre" (to bear)',
        'memory_tips': 'Think "cone + -ifer (bearing)" - trees that bear cones',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The forest was dominated by tall _____ that stayed green throughout winter.'
    },
    'conjugate': {
        'definition': 'In grammar, to change the form of a verb to indicate tense, person, number, mood, or voice; in chemistry, to join or link molecules together; in mathematics, to change the sign of the imaginary part of a complex number. Conjugation creates systematic patterns that convey different meanings or relationships.',
        'part_of_speech': 'verb, adjective, noun',
        'pronunciation_guide': 'KON-juh-gayt (verb), KON-juh-git (adj/noun) (/ˈkɒndʒəgeɪt/, /ˈkɒndʒəgɪt/)',
        'etymology': 'From Latin "conjugatus," from "con-" (together) + "jugare" (to yoke)',
        'memory_tips': 'Think "con- (together) + jug (yoke)" - yoking or joining things together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Students must learn to _____ irregular verbs in multiple tenses.'
    },
    'conjugated': {
        'definition': 'Past tense of conjugate; changed in form to show grammatical relationships, or chemically joined with other molecules. In language learning, conjugated verbs show tense, person, and number. In chemistry, conjugated systems involve alternating single and double bonds. In biology, conjugated proteins are combined with non-protein groups.',
        'part_of_speech': 'verb (past tense), adjective',
        'pronunciation_guide': 'KON-juh-gay-ted (/ˈkɒndʒəgeɪtəd/)',
        'etymology': 'From Latin "conjugatus" + past tense ending "-ed"',
        'memory_tips': 'Think of verbs that have been "yoked together" with different endings',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The teacher checked whether students had correctly _____ the French verbs.'
    },
    'conjunto': {
        'definition': 'A style of Mexican-American music and the ensemble that performs it, typically featuring accordion, guitar, bass, and drums. Conjunto originated in South Texas and Northern Mexico, blending German, Mexican, and American musical influences. This genre is central to Tejano culture and represents the multicultural heritage of the border region.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-HOON-toh (/kɒnˈhuntoʊ/)',
        'etymology': 'Spanish, meaning "ensemble" or "group," from "con-" (together) + "junto" (joined)',
        'memory_tips': 'Think of musicians "joined together" in a group - a musical ensemble',
        'alternate_spellings': 'None',
        'language_origin': 'Spanish',
        'example_sentence': 'The _____ band played traditional polkas at the cultural festival.'
    },
    'conjure': {
        'definition': 'To summon or call forth, especially through supernatural means; to bring to mind or imagination; to perform magic tricks or illusions. Conjuring can refer to magical practices, creative imagination, or skillful manipulation that seems magical. The term emphasizes the seemingly impossible act of bringing something into being.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'KUN-jur (/ˈkʌndʒər/) or kun-JOOR (/kənˈdʒʊr/)',
        'etymology': 'From Old French "conjurer," from Latin "conjurare" (to swear together)',
        'memory_tips': 'Think of magicians conjuring rabbits from hats - making things appear mysteriously',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'The magician could _____ doves from thin air during his performance.'
    },
    'conkers': {
        'definition': 'A British children\'s game played with horse chestnuts (also called conkers) strung on strings, where players try to break their opponent\'s conker. The term also refers to the shiny brown seeds themselves. This traditional playground game involves strategy and luck, and has cultural significance in British childhood experiences.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KONG-kurz (/ˈkɒŋkərz/)',
        'etymology': 'Possibly from "conch" (shell) or related to "conquer" due to the competitive nature',
        'memory_tips': 'Think of "conquer" - trying to conquer opponent\'s chestnuts in the game',
        'alternate_spellings': 'None',
        'language_origin': 'British English',
        'example_sentence': 'The children spent recess playing _____ under the horse chestnut tree.'
    },
    'connect': {
        'definition': 'To join, link, or fasten together; to establish communication or relationship between people, places, or things. Connection can be physical (plugging in a cable), social (meeting people), or conceptual (linking ideas). The term emphasizes bringing separate elements into contact or relationship with each other.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'kuh-NEKT (/kəˈnɛkt/)',
        'etymology': 'From Latin "connectere," from "con-" (together) + "nectere" (to bind)',
        'memory_tips': 'Think "con- (together) + nect (bind)" - binding things together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Please _____ the printer cable to the computer before printing the document.'
    },
    'connection': {
        'definition': 'A relationship, link, or association between two or more things; the act of connecting or state of being connected. Connections can be physical (electrical connections), social (personal relationships), or conceptual (ideas that relate to each other). Strong connections often enable communication, understanding, or functionality.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kuh-NEK-shun (/kəˈnɛkʃən/)',
        'etymology': 'From Latin "connexio," from "connectere" (to join together)',
        'memory_tips': 'Think of the act of connecting - the relationship or link that results',
        'alternate_spellings': 'Connexion (archaic)',
        'language_origin': 'Latin',
        'example_sentence': 'The wireless internet _____ was too weak to stream the video.'
    },
    'connemara': {
        'definition': 'A region in western Ireland known for its rugged landscape, traditional culture, and Irish-speaking communities; also refers to a hardy breed of pony native to this region. Connemara ponies are renowned for their intelligence, sure-footedness, and jumping ability. The area represents Irish heritage, natural beauty, and traditional ways of life.',
        'part_of_speech': 'noun (proper name)',
        'pronunciation_guide': 'kon-uh-MAR-uh (/ˌkɒnəˈmɑrə/)',
        'etymology': 'Irish "Conamara," meaning "inlets of the sea"',
        'memory_tips': 'Think of Irish coastal inlets and the famous ponies from this region',
        'alternate_spellings': 'None',
        'language_origin': 'Irish Gaelic',
        'example_sentence': 'The _____ pony effortlessly navigated the rocky Irish terrain.'
    },
    'connivery': {
        'definition': 'The practice of secretly cooperating with others to do something wrong or illegal; conspiracy or collusion for improper purposes. Connivery involves deliberate participation in deceptive or harmful activities, often requiring coordination between multiple parties. This behavior violates trust and ethical standards.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kuh-NYE-vur-ee (/kəˈnaɪvəri/)',
        'etymology': 'From Latin "connivere" (to close the eyes, wink at) + suffix "-ery"',
        'memory_tips': 'Think "con- (together) + niv (wink)" - winking together in secret cooperation',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The investigation revealed extensive _____ between the officials and contractors.'
    },
    'connoisseur': {
        'definition': 'An expert judge in matters of taste, especially in art, food, wine, or other areas requiring refined appreciation and knowledge. Connoisseurs have developed sophisticated understanding through study and experience, enabling them to distinguish quality, authenticity, and subtle differences that others might miss. Their expertise is highly valued in specialized fields.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-uh-SUR (/ˌkɒnəˈsɜr/)',
        'etymology': 'French, from Old French "conoistre" (to know), from Latin "cognoscere"',
        'memory_tips': 'Think of someone who "knows" deeply - an expert in recognizing quality',
        'alternate_spellings': 'None',
        'language_origin': 'French',
        'example_sentence': 'The wine _____ could identify the vineyard and year from a single sip.'
    },
    'conquests': {
        'definition': 'Plural of conquest; military victories resulting in control over territories, peoples, or enemies; achievements or successes in overcoming challenges. Conquests can be military (capturing lands), personal (overcoming fears), or metaphorical (winning someone\'s heart). The term implies struggle, victory, and gaining control or dominance.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KON-kwests (/ˈkɒŋkwɛsts/)',
        'etymology': 'Plural of Old French "conqueste," from Latin "conquirere" (to seek together)',
        'memory_tips': 'Think "con- (together) + quest" - seeking victory together through struggle',
        'alternate_spellings': 'None',
        'language_origin': 'Old French/Latin',
        'example_sentence': 'The historian studied the Roman _____ throughout the Mediterranean region.'
    },
    'consanguine': {
        'definition': 'Related by blood; sharing common ancestry through genetic inheritance rather than marriage. Consanguine relationships include parents and children, siblings, cousins, and other blood relatives. In legal and medical contexts, consanguinity affects inheritance rights, marriage laws, and genetic risk assessments. The term emphasizes biological rather than social family connections.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kon-SANG-gwin (/kɒnˈsæŋgwɪn/)',
        'etymology': 'From Latin "consanguineus," from "con-" (together) + "sanguis" (blood)',
        'memory_tips': 'Think "con- (together) + sanguin (blood)" - sharing blood together',
        'alternate_spellings': 'Consanguineous',
        'language_origin': 'Latin',
        'example_sentence': 'The genealogist traced the _____ relationships between family members.'
    },
    'consecrate': {
        'definition': 'To dedicate formally to a sacred purpose; to make or declare sacred through religious ceremony or ritual. Consecration sets apart people, objects, or places for holy use, often involving blessings, prayers, or ceremonial acts. The term can also mean to devote earnestly to a cause or purpose.',
        'part_of_speech': 'verb',
        'pronunciation_guide': 'KON-si-krayt (/ˈkɒnsəkreɪt/)',
        'etymology': 'From Latin "consecratus," from "con-" (completely) + "sacrare" (to make sacred)',
        'memory_tips': 'Think "con- (completely) + sacr (sacred)" - making completely sacred',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The bishop will _____ the new church in a special ceremony.'
    },
    'consecrateadjective': {
        'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "consecrate" (to make sacred) + "adjective" (a grammatical term). These should be separate words.',
        'part_of_speech': 'error - combined words',
        'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
        'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
        'memory_tips': 'This is a data error - should be separated into "consecrate" and "adjective"',
        'alternate_spellings': 'consecrate + adjective (separate words)',
        'language_origin': 'ERROR - combined words',
        'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
    },
    'consecutive': {
        'definition': 'Following continuously in unbroken sequence; succeeding one after another without interruption. Consecutive events, numbers, or periods occur in order without gaps or breaks between them. This pattern suggests regularity, progression, and uninterrupted continuity in time or arrangement.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kun-SEK-yuh-tiv (/kənˈsɛkjətɪv/)',
        'etymology': 'From Latin "consecutus," from "con-" (together) + "sequi" (to follow)',
        'memory_tips': 'Think "con- (together) + secut (follow)" - following together in sequence',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The team won five _____ games to secure the championship.'
    },
    'consensus': {
        'definition': 'General agreement or accord reached by a group; collective opinion or judgment shared by most or all members of a group. Consensus emerges through discussion, compromise, and finding common ground among different viewpoints. It represents unity of opinion and collaborative decision-making rather than simple majority rule.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-SEN-sus (/kənˈsɛnsəs/)',
        'etymology': 'Latin, meaning "agreement," from "consentire" (to feel together)',
        'memory_tips': 'Think "con- (together) + sens (feel)" - feeling or thinking together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The committee reached _____ on the new policy after lengthy discussions.'
    },
    'consequences': {
        'definition': 'Plural of consequence; results or effects that follow from actions, decisions, or events. Consequences can be positive (rewards) or negative (punishments), intended or unintended. Understanding consequences helps people make informed decisions and take responsibility for their actions. They represent the cause-and-effect relationships in life.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KON-si-kwen-siz (/ˈkɒnsəkwənsɪz/)',
        'etymology': 'Plural of Latin "consequentia," from "consequi" (to follow closely)',
        'memory_tips': 'Think of results that "follow closely" after actions or decisions',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'She carefully considered the _____ before making her important decision.'
    },
    'consequent': {
        'definition': 'Following as a result or effect; logically following from premises or previous events. As a noun, consequent refers to the result part of a conditional statement. The term emphasizes logical sequence and the inevitable nature of results that flow from specific causes or conditions.',
        'part_of_speech': 'adjective, noun',
        'pronunciation_guide': 'KON-si-kwent (/ˈkɒnsəkwənt/)',
        'etymology': 'From Latin "consequens," present participle of "consequi" (to follow closely)',
        'memory_tips': 'Think of something that "follows consequently" - a logical result',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ flooding damaged many homes after the heavy rainfall.'
    },
    'considerable': {
        'definition': 'Large in amount, extent, or degree; worthy of consideration or attention due to its significance. Considerable suggests something substantial enough to be noteworthy, whether referring to time, money, effort, or impact. The term implies more than average or expected magnitude.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kun-SID-ur-uh-bul (/kənˈsɪdərəbəl/)',
        'etymology': 'From Latin "considerabilis," meaning "worthy of consideration"',
        'memory_tips': 'Think "consider + -able" - worthy of being considered because it\'s significant',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The project required _____ time and resources to complete successfully.'
    },
    'consideration': {
        'definition': 'Careful thought about something before making a decision; thoughtful regard for others\' feelings or circumstances; something given or done in return for something else. Consideration involves weighing options, showing empathy, or providing compensation. It represents thoughtfulness in decision-making and interpersonal relationships.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-sid-uh-RAY-shun (/kənˌsɪdəˈreɪʃən/)',
        'etymology': 'From Latin "consideratio," from "considerare" (to examine carefully)',
        'memory_tips': 'Think "consider + -ation" - the act of considering carefully',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Please give serious _____ to all the options before deciding.'
    },
    'consigliere': {
        'definition': 'An advisor or counselor, especially in organized crime families; a trusted adviser who provides guidance on important matters. From Italian-American usage, particularly associated with Mafia organizations where the consigliere serves as a neutral counselor to the family boss. The term emphasizes wisdom, trust, and advisory roles.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-sil-ee-EH-ray (/kɒnˌsɪliˈɛreɪ/)',
        'etymology': 'Italian, meaning "counselor," from Latin "consilium" (advice, counsel)',
        'memory_tips': 'Think "counsel + -iere" - someone who provides counsel or advice',
        'alternate_spellings': 'None',
        'language_origin': 'Italian',
        'example_sentence': 'The crime boss relied on his trusted _____ for strategic advice.'
    },
    'consisting': {
        'definition': 'Present participle of consist; being composed or made up of specified elements or parts. When something consists of particular components, those elements form its essential nature or structure. The term describes the composition or makeup of objects, groups, or concepts.',
        'part_of_speech': 'verb (present participle)',
        'pronunciation_guide': 'kun-SIS-ting (/kənˈsɪstɪŋ/)',
        'etymology': 'From Latin "consistere" (to stand together) + present participle "-ing"',
        'memory_tips': 'Think "con- (together) + sist (stand)" - standing together as component parts',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The meal was _____ of three courses: appetizer, main dish, and dessert.'
    },
    'consists': {
        'definition': 'Third person singular present tense of consist; is composed or made up of specified parts or elements. When something consists of certain components, those parts form its essential structure or composition. The verb describes the fundamental makeup or composition of things.',
        'part_of_speech': 'verb (third person singular present)',
        'pronunciation_guide': 'kun-SISTS (/kənˈsɪsts/)',
        'etymology': 'From Latin "consistere" (to stand firm, be composed of)',
        'memory_tips': 'Think of parts that "stand together" to form a whole',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The recipe _____ of flour, sugar, eggs, and butter mixed together.'
    },
    'consomme': {
        'definition': 'A clear soup made from rich stock that has been clarified, typically served as an elegant appetizer in fine dining. Consommé requires careful preparation to achieve perfect clarity and concentrated flavor. This classic French culinary technique demonstrates skill in removing impurities while preserving intense taste.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-suh-MAY (/ˌkɒnsəˈmeɪ/)',
        'etymology': 'French, past participle of "consommer" (to consume, complete)',
        'memory_tips': 'Think of "consumed" or "completed" - a soup that has been perfected through clarification',
        'alternate_spellings': 'Consommé (with accent)',
        'language_origin': 'French',
        'example_sentence': 'The chef served an elegant mushroom _____ as the first course.'
    },
    'consommé': {
        'definition': 'A clear, refined soup made from rich stock that has been carefully clarified to remove all impurities, resulting in a transparent but flavorful broth. This classic French culinary preparation requires advanced technique and is often served in fine dining establishments as an elegant appetizer. The accent mark distinguishes it as the authentic French spelling.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-suh-MAY (/ˌkɒnsəˈmeɪ/)',
        'etymology': 'French, past participle of "consommer" (to consume, bring to completion)',
        'memory_tips': 'Think of soup brought to "completion" - perfectly clarified and refined',
        'alternate_spellings': 'Consomme (without accent)',
        'language_origin': 'French',
        'example_sentence': 'The restaurant\'s signature _____ was crystal clear yet full of rich flavor.'
    },
    'consonant': {
        'definition': 'A speech sound produced by obstructing airflow in the vocal tract, contrasting with vowels; in agreement or harmony with something. Consonants include sounds like /b/, /k/, /s/, and /r/ that require specific tongue, lip, or throat positions. In music, consonant intervals create harmony and stability.',
        'part_of_speech': 'noun, adjective',
        'pronunciation_guide': 'KON-suh-nuhnt (/ˈkɒnsənənt/)',
        'etymology': 'From Latin "consonans," meaning "sounding together"',
        'memory_tips': 'Think "con- (together) + son (sound)" - sounds that work together with vowels',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The word "strength" contains several _____ sounds clustered together.'
    },
    'consonants': {
        'definition': 'Plural of consonant; speech sounds produced by restricting or blocking airflow, including sounds like /p/, /t/, /k/, /m/, /n/, and /s/. Consonants combine with vowels to form syllables and words. In written language, consonant letters represent these sounds, forming the structural framework of words alongside vowels.',
        'part_of_speech': 'noun (plural)',
        'pronunciation_guide': 'KON-suh-nuhnts (/ˈkɒnsənənts/)',
        'etymology': 'Plural of Latin "consonans" (sounding together)',
        'memory_tips': 'Multiple sounds that work together with vowels to form words',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'English has more _____ than vowels in its sound system.'
    },
    'consortium': {
        'definition': 'An association or partnership of multiple organizations, companies, or institutions working together toward common goals. Consortiums pool resources, expertise, and capabilities to undertake projects too large or complex for individual organizations. These collaborative arrangements are common in research, business ventures, and educational initiatives.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-SOR-tee-um (/kənˈsɔrtiəm/)',
        'etymology': 'Latin, meaning "partnership, fellowship," from "consors" (sharing in common)',
        'memory_tips': 'Think "con- (together) + sort" - sorting or grouping together for partnership',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The research _____ included universities from five different countries.'
    },
    'conspiratorial': {
        'definition': 'Relating to or suggesting conspiracy; involving secret planning with others to do something harmful or illegal. Conspiratorial behavior includes secretive communication, hidden agendas, and coordinated deception. The term can describe actual conspiracies or merely the appearance of secretive, suspicious activity.',
        'part_of_speech': 'adjective',
        'pronunciation_guide': 'kun-spir-uh-TOR-ee-ul (/kənˌspɪrəˈtɔriəl/)',
        'etymology': 'From Latin "conspirare" (to breathe together, plot) + suffix "-ial"',
        'memory_tips': 'Think "con- (together) + spir (breathe)" - breathing together secretly in plots',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The group exchanged _____ glances during the secret meeting.'
    },
    'constabulary': {
        'definition': 'The police force of a particular area or country; the organized body of law enforcement officers responsible for maintaining public order and safety. Constabularies have specific jurisdictions and authority to enforce laws, investigate crimes, and protect citizens. The term emphasizes the official, organized nature of police forces.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-STAB-yuh-ler-ee (/kənˈstæbjəlɛri/)',
        'etymology': 'From Old French "conestable" (chief officer) + suffix "-ary"',
        'memory_tips': 'Think "constable + -ary" - the organization or body of constables',
        'alternate_spellings': 'None',
        'language_origin': 'Old French',
        'example_sentence': 'The local _____ increased patrols in response to recent break-ins.'
    },
    'constantbalm': {
        'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "constant" (unchanging, continuous) + "balm" (soothing ointment or influence). These should be separate words.',
        'part_of_speech': 'error - combined words',
        'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
        'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
        'memory_tips': 'This is a data error - should be separated into "constant" and "balm"',
        'alternate_spellings': 'constant + balm (separate words)',
        'language_origin': 'ERROR - combined words',
        'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
    },
    'constellation': {
        'definition': 'A group of stars forming a recognizable pattern in the night sky, traditionally named after mythological figures, animals, or objects. Constellations serve as celestial navigation aids and cultural symbols across different civilizations. Modern astronomy recognizes 88 official constellations that divide the entire sky into distinct regions.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-stuh-LAY-shun (/ˌkɒnstəˈleɪʃən/)',
        'etymology': 'From Latin "constellatio," from "con-" (together) + "stella" (star)',
        'memory_tips': 'Think "con- (together) + stell (star)" - stars grouped together in patterns',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The Big Dipper is part of the _____ Ursa Major.'
    },
    'consternation': {
        'definition': 'Feelings of anxiety, dismay, or confusion caused by something unexpected or shocking; a state of alarmed bewilderment. Consternation represents emotional disturbance that disrupts normal composure and thinking. This response often occurs when facing surprising setbacks, disturbing news, or overwhelming situations.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kon-stur-NAY-shun (/ˌkɒnstərˈneɪʃən/)',
        'etymology': 'From Latin "consternatio," from "consternare" (to alarm, confuse)',
        'memory_tips': 'Think of being "stunned" or "confused" - emotional alarm and bewilderment',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The sudden announcement caused _____ among the employees.'
    },
    'constituent': {
        'definition': 'A component part of something larger; a person who lives and votes in an area represented by an elected official. Constituents can be physical parts of a system or political supporters of a representative. The term emphasizes the relationship between parts and wholes, whether in chemistry, politics, or other contexts.',
        'part_of_speech': 'noun, adjective',
        'pronunciation_guide': 'kun-STICH-oo-uhnt (/kənˈstɪtʃuənt/)',
        'etymology': 'From Latin "constituens," present participle of "constituere" (to set up)',
        'memory_tips': 'Think "constitute + -ent" - parts that constitute or make up something',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The senator met with _____ groups to discuss the proposed legislation.'
    },
    'constricting': {
        'definition': 'Present participle of constrict; tightening, narrowing, or compressing something; making smaller or more limited. Constricting can be physical (blood vessels narrowing) or metaphorical (restrictive rules). The action involves applying pressure or limitation that reduces size, flow, or freedom.',
        'part_of_speech': 'verb (present participle), adjective',
        'pronunciation_guide': 'kun-STRIK-ting (/kənˈstrɪktɪŋ/)',
        'etymology': 'From Latin "constrictus," from "con-" (together) + "stringere" (to bind tight)',
        'memory_tips': 'Think "con- (together) + strict (tight)" - binding tightly together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The _____ clothing made it difficult for him to move freely.'
    },
    'constructed': {
        'definition': 'Past tense of construct; built, assembled, or created by putting parts together systematically. Construction involves planning, organizing materials, and assembling components according to design specifications. The term applies to physical building, abstract concepts, or logical arguments that are deliberately created.',
        'part_of_speech': 'verb (past tense)',
        'pronunciation_guide': 'kun-STRUK-ted (/kənˈstrʌktəd/)',
        'etymology': 'From Latin "constructus," from "con-" (together) + "struere" (to build)',
        'memory_tips': 'Think "con- (together) + struct (build)" - built together systematically',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The bridge was _____ using the latest engineering techniques.'
    },
    'consul': {
        'definition': 'An official appointed by a government to live in a foreign city and protect the interests of citizens from their home country; in ancient Rome, one of the two chief magistrates. Modern consuls provide services like issuing visas, assisting travelers, and facilitating trade relationships between nations.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'KON-sul (/ˈkɒnsəl/)',
        'etymology': 'From Latin "consul," possibly from "consulere" (to consult, take counsel)',
        'memory_tips': 'Think of someone you "consult" - a government official who provides advice and assistance',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The American _____ helped the stranded tourists obtain new passports.'
    },
    'contact': {
        'definition': 'The state of physical touching; communication or connection between people or organizations; a person known to someone who may be useful professionally or socially. Contact can be physical, communicative, or relational, representing various forms of connection between entities.',
        'part_of_speech': 'noun, verb',
        'pronunciation_guide': 'KON-takt (/ˈkɒntækt/)',
        'etymology': 'From Latin "contactus," from "con-" (together) + "tangere" (to touch)',
        'memory_tips': 'Think "con- (together) + tact (touch)" - touching together or connecting',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'Please _____ the customer service department for assistance with your order.'
    },
    'contagion': {
        'definition': 'The spread of disease through direct or indirect contact; the transmission of ideas, emotions, or behaviors from person to person. Contagion can be biological (infectious diseases) or social (emotional contagion, viral marketing). The term emphasizes how things spread rapidly through populations or groups.',
        'part_of_speech': 'noun',
        'pronunciation_guide': 'kun-TAY-jun (/kənˈteɪdʒən/)',
        'etymology': 'From Latin "contagio," from "con-" (together) + "tangere" (to touch)',
        'memory_tips': 'Think "con- (together) + tag (touch)" - spreading by touching together',
        'alternate_spellings': 'None',
        'language_origin': 'Latin',
        'example_sentence': 'The health officials worked to prevent the _____ from spreading further.'
    }
}

def process_batch():
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_040_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_040_processed.csv'
    
    try:
        df = pd.read_csv(input_file)
        print(f"Processing {len(df)} words from batch 040...")
        
        processed_data = []
        combined_word_errors = []
        
        for _, row in df.iterrows():
            word = row['word'].strip()
            if word in batch_040_data:
                data = batch_040_data[word]
                
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