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
        
        # Silent letters
        if re.search(r'[bt](?![aeiou])|[kl](?=n)|[w](?=r)|[h](?=[^aeiou])', word.lower()):
            irregular_patterns += 1
            
        # Double letters not in pronunciation
        if re.search(r'(.)\1', word) and 'double' not in pronunciation.lower():
            irregular_patterns += 1
            
        # Score inversely related to irregular patterns
        return min(10, max(1, 8 - irregular_patterns * 2))
    
    def _calculate_word_frequency(self, word):
        """Score 1-10: How common the word is (lower = more common)"""
        # Common words (1-3)
        common = ['program', 'project', 'promise', 'prone', 'pronounced', 'proof', 'proper', 'proposal', 'prosecutor']
        if word.lower() in common:
            return 2
            
        # Moderately common (4-6)
        moderate = ['progression', 'prominent', 'pronounced', 'proprietary', 'propulsion', 'prosperous', 'prosthetic']
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
        prefixes = ['pro', 'prop', 'prom', 'pron']
        suffixes = ['ous', 'ity', 'ive', 'ment', 'tion', 'ic', 'ary', 'ence', 'ent', 'ed', 'ing', 'ate', 'ive']
        
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
        languages = ['latin', 'greek', 'french', 'spanish', 'italian', 'german', 'sanskrit', 'old english', 'russian']
        language_count = sum(1 for lang in languages if lang in etymology.lower())
        
        if language_count >= 2:
            complexity += 3
        elif language_count == 1:
            complexity += 1
            
        # Ancient origins add complexity
        if any(ancient in etymology.lower() for ancient in ['ancient', 'classical', 'medieval']):
            complexity += 2
            
        return min(10, complexity)

# Comprehensive word data for batch 140
word_data = {
    'program': {
        'definition': 'A set of related measures or activities with a particular long-term aim; a series of coded instructions for a computer; a planned series of activities or performances. In education, a program refers to a structured course of study or curriculum designed to achieve specific learning objectives. Programs can range from simple software applications that execute basic commands to complex educational frameworks that guide students through comprehensive learning experiences over months or years.',
        'pronunciation': '/ˈproʊɡræm/',
        'pronunciation_respelling': 'PROH-gram',
        'etymology': 'From Greek "programma," meaning "a written public notice," from "pro" (forth) + "graphein" (to write).',
        'memory_tip': 'Think "pro" (forward) + "gram" (write) = writing out plans forward in advance.',
        'example_sentence': 'The school\'s new mathematics ___ helped students improve their problem-solving skills.',
        'source': 'Claude'
    },
    'progression': {
        'definition': 'The process of developing or moving gradually towards a more advanced state; a succession of numbers or musical chords following a particular pattern. In mathematics, a progression is a sequence where each term is derived from the previous one according to a specific rule. In music, chord progressions create harmonic movement that guides the emotional flow of a composition.',
        'pronunciation': '/prəˈɡrɛʃən/',
        'pronunciation_respelling': 'pruh-GRESH-un',
        'etymology': 'From Latin "progressio," from "progredi" meaning "to go forward," from "pro" (forward) + "gradi" (to step).',
        'memory_tip': 'Think "pro" (forward) + "gression" (stepping) = stepping forward in sequence.',
        'example_sentence': 'The student showed steady ___ in reading comprehension throughout the semester.',
        'source': 'Claude'
    },
    'project': {
        'definition': 'An individual or collaborative enterprise carefully planned to achieve a particular aim; to extend outward or forward; to present an image or idea to others. Educational projects engage students in hands-on learning experiences that develop critical thinking, research, and presentation skills while exploring real-world applications of academic concepts.',
        'pronunciation': '/ˈprɑːdʒɛkt/',
        'pronunciation_respelling': 'PRAH-jekt',
        'etymology': 'From Latin "projectus," from "proicere" meaning "to throw forth," from "pro" (forth) + "iacere" (to throw).',
        'memory_tip': 'Think "pro" (forward) + "ject" (throw) = throwing ideas forward into reality.',
        'example_sentence': 'The science fair ___ required students to design and conduct their own experiments.',
        'source': 'Claude'
    },
    'projects': {
        'definition': 'Plural of project; multiple individual or collaborative enterprises planned to achieve particular aims; third person singular of the verb project, meaning to extend outward or present an image. In education, projects serve as comprehensive assessment tools that allow students to demonstrate mastery across multiple subjects and skills.',
        'pronunciation': '/ˈprɑːdʒɛkts/',
        'pronunciation_respelling': 'PRAH-jekts',
        'etymology': 'Plural form of "project," from Latin "projectus."',
        'memory_tip': 'Simply "project" with an "s" added for multiple planned enterprises.',
        'example_sentence': 'The teacher assigned three different ___ to help students explore various aspects of ancient civilizations.',
        'source': 'Claude'
    },
    'proletarian': {
        'definition': 'Relating to the proletariat, the working class who sell their labor for wages; a member of the working class. In Marxist theory, proletarians are distinguished from the bourgeoisie (capital owners) as they possess only their labor power. The term encompasses industrial workers, service employees, and others who work for wages rather than owning productive property.',
        'pronunciation': '/ˌproʊlɪˈtɛəriən/',
        'pronunciation_respelling': 'proh-lih-TAIR-ee-un',
        'etymology': 'From Latin "proletarius," meaning "producing offspring," referring to citizens whose only contribution to the state was having children.',
        'memory_tip': 'Think "pro" (for) + "letarian" (people) = for the working people.',
        'example_sentence': 'The novel depicted the struggles of ___ families during the Industrial Revolution.',
        'source': 'Claude'
    },
    'proliferate': {
        'definition': 'To increase rapidly in numbers; to multiply or spread abundantly; to reproduce by forming new parts or offspring. In biology, proliferation refers to rapid cell division and growth. In general usage, it describes the fast expansion of ideas, technologies, or populations across various environments or contexts.',
        'pronunciation': '/prəˈlɪfəreɪt/',
        'pronunciation_respelling': 'pruh-LIF-uh-rayt',
        'etymology': 'From Latin "proliferare," from "proles" (offspring) + "ferre" (to bear or carry).',
        'memory_tip': 'Think "pro" (much) + "liferate" (life) = producing much life/growth.',
        'example_sentence': 'Social media platforms began to ___ rapidly in the early 2000s.',
        'source': 'Claude'
    },
    'prolix': {
        'definition': 'Using too many words; tediously lengthy in speech or writing; characterized by unnecessary verbosity. A prolix speaker or writer tends to elaborate excessively, often obscuring their main points with excessive detail. This trait is generally considered a flaw in effective communication, as brevity and clarity are typically more persuasive and engaging.',
        'pronunciation': '/ˈproʊlɪks/',
        'pronunciation_respelling': 'PROH-liks',
        'etymology': 'From Latin "prolixus," meaning "extended" or "poured forth," from "pro" (forth) + "liquere" (to flow).',
        'memory_tip': 'Think "pro" (much) + "lix" (liquid/flowing) = words flowing too much.',
        'example_sentence': 'The professor\'s ___ lectures often lost students\' attention despite containing valuable information.',
        'source': 'Claude'
    },
    'prolusory': {
        'definition': 'Serving as a prelude or introduction; preliminary in nature; acting as a trial or preface to something more substantial. This term is often used in academic and literary contexts to describe introductory remarks, preliminary studies, or opening movements that prepare the audience for the main content that follows.',
        'pronunciation': '/prəˈluːsəri/',
        'pronunciation_respelling': 'pruh-LOO-suh-ree',
        'etymology': 'From Latin "prolusio," meaning "a prelude" or "preliminary exercise," from "pro" (before) + "ludere" (to play).',
        'memory_tip': 'Think "pro" (before) + "lusory" (play) = playing before the main performance.',
        'example_sentence': 'The composer wrote several ___ pieces before beginning work on his masterpiece symphony.',
        'source': 'Claude'
    },
    'promethean': {
        'definition': 'Relating to Prometheus; characterized by creative daring and originality; boldly defiant of authority; involving great creativity or innovation, often at personal risk. Named after the Greek Titan who stole fire from the gods to give to humanity, this term describes individuals who challenge established norms to bring knowledge or progress to others.',
        'pronunciation': '/prəˈmiːθiən/',
        'pronunciation_respelling': 'pruh-MEE-thee-un',
        'etymology': 'From Prometheus, the Greek Titan who stole fire from the gods, from Greek "promethes" meaning "forethinking."',
        'memory_tip': 'Think of Prometheus bringing fire (knowledge) to humans = bold, creative innovation.',
        'example_sentence': 'The scientist\'s ___ research challenged conventional theories and opened new fields of study.',
        'source': 'Claude'
    },
    'prominent': {
        'definition': 'Important and well-known; projecting out from a surface; easily noticed or conspicuous. In social contexts, prominent individuals are recognized for their achievements, influence, or status. In physical contexts, prominent features are those that stand out visually, such as a prominent nose or a prominent building on a skyline.',
        'pronunciation': '/ˈprɑːmɪnənt/',
        'pronunciation_respelling': 'PRAH-mih-nunt',
        'etymology': 'From Latin "prominens," from "prominere" meaning "to jut out," from "pro" (forward) + "minere" (to project).',
        'memory_tip': 'Think "pro" (forward) + "minent" (sticking out) = sticking out forward/notable.',
        'example_sentence': 'The ___ scientist received international recognition for her groundbreaking research.',
        'source': 'Claude'
    },
    'promise': {
        'definition': 'A declaration or assurance that one will do something or that a particular thing will happen; potential for success or good results; to give one\'s word or commitment. Promises form the foundation of trust in relationships and societies, creating expectations and obligations that bind individuals to future actions.',
        'pronunciation': '/ˈprɑːmɪs/',
        'pronunciation_respelling': 'PRAH-mis',
        'etymology': 'From Latin "promissum," from "promittere" meaning "to send forth" or "to promise," from "pro" (forth) + "mittere" (to send).',
        'memory_tip': 'Think "pro" (forward) + "mise" (send) = sending your word forward into the future.',
        'example_sentence': 'She made a ___ to her parents that she would study harder next semester.',
        'source': 'Claude'
    },
    'promontory': {
        'definition': 'A high point of land or rock projecting into a body of water; a headland or cliff that extends into the sea. Promontories are significant geological features that often serve as landmarks for navigation and can create unique ecosystems due to their exposure to wind and waves. They frequently house lighthouses or other navigational aids.',
        'pronunciation': '/ˈprɑːməntɔːri/',
        'pronunciation_respelling': 'PRAH-mun-tor-ee',
        'etymology': 'From Latin "promontorium," from "prominere" meaning "to jut out," from "pro" (forward) + "mons" (mountain).',
        'memory_tip': 'Think "pro" (forward) + "montory" (mountain) = mountain jutting forward into water.',
        'example_sentence': 'The lighthouse stood majestically on the rocky ___ overlooking the turbulent sea.',
        'source': 'Claude'
    },
    'promulgate': {
        'definition': 'To make known publicly; to announce or proclaim officially; to put a law or decree into effect by formal declaration. In legal contexts, promulgation is the official publication of new laws or regulations. In academic settings, it refers to the widespread dissemination of ideas, theories, or research findings.',
        'pronunciation': '/ˈprɑːməlɡeɪt/',
        'pronunciation_respelling': 'PRAH-mul-gayt',
        'etymology': 'From Latin "promulgatus," from "promulgare" meaning "to make publicly known," from "pro" (forth) + "mulgere" (related to publishing).',
        'memory_tip': 'Think "pro" (forth) + "mulgate" (make known) = making known to the public.',
        'example_sentence': 'The university decided to ___ new academic policies at the beginning of the semester.',
        'source': 'Claude'
    },
    'promyshlennik': {
        'definition': 'A Russian fur trader or hunter, especially one who operated in Siberia and Alaska during the 18th and 19th centuries. These individuals were crucial to Russia\'s expansion and economic development, establishing trading posts and collecting furs for the lucrative European market. They played a significant role in the exploration and colonization of Alaska.',
        'pronunciation': '/prəˈmɪʃlənɪk/',
        'pronunciation_respelling': 'pruh-MISH-luh-nik',
        'etymology': 'From Russian "promyshlennik," from "promysel" meaning "trade" or "industry," related to pursuing commercial activities.',
        'memory_tip': 'Think Russian fur trader - "prom" (fur) + "yshlennik" (trader/worker).',
        'example_sentence': 'The ___ established trading relationships with indigenous peoples throughout the Aleutian Islands.',
        'source': 'Claude'
    },
    'pronaoscraquelure': {
        'definition': '[COMBINED WORD ERROR] This appears to be "pronaos" + "craquelure" incorrectly joined. Should be separated into two distinct terms: "pronaos" (the inner area of an ancient Greek temple) and "craquelure" (a network of fine cracks in paint or varnish).',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "pronaos" (Greek: before the temple) with "craquelure" (French: crackling pattern).',
        'memory_tip': '[ERROR] This should be split into "pronaos" (temple area) and "craquelure" (crack pattern).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "pronaos" and "craquelure."',
        'source': 'Claude'
    },
    'prone': {
        'definition': 'Lying face downward; having a tendency or inclination toward something, especially something undesirable; susceptible to or likely to suffer from. In medical contexts, prone position refers to lying on one\'s stomach. When describing behavior or characteristics, it indicates a natural tendency or predisposition.',
        'pronunciation': '/proʊn/',
        'pronunciation_respelling': 'PROHN',
        'etymology': 'From Latin "pronus," meaning "leaning forward" or "inclined," from "pro" (forward).',
        'memory_tip': 'Think "pro" (forward) + "ne" = leaning forward/downward or toward something.',
        'example_sentence': 'Students who skip breakfast are ___ to difficulty concentrating during morning classes.',
        'source': 'Claude'
    },
    'proneselfie': {
        'definition': '[COMBINED WORD ERROR] This appears to be "prone" + "selfie" incorrectly joined. Should be separated into two distinct words: "prone" (lying face down or inclined toward) and "selfie" (a self-portrait photograph).',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "prone" (Latin: leaning forward) with "selfie" (modern English: self-photograph).',
        'memory_tip': '[ERROR] This should be split into "prone" (lying down/inclined) and "selfie" (self-photo).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "prone" and "selfie."',
        'source': 'Claude'
    },
    'pronounced': {
        'definition': 'Past tense of pronounce; spoken or articulated clearly; very noticeable or marked; strongly evident or conspicuous. When something is pronounced, it stands out clearly from its surroundings or context. This term can refer to both verbal articulation and the degree to which a characteristic or feature is evident.',
        'pronunciation': '/prəˈnaʊnst/',
        'pronunciation_respelling': 'pruh-NOWNST',
        'etymology': 'From Latin "pronuntiatus," from "pronuntiare" meaning "to proclaim," from "pro" (forth) + "nuntiare" (to announce).',
        'memory_tip': 'Think "pro" (forth) + "nounced" (announced) = clearly announced or noticeable.',
        'example_sentence': 'The teacher noticed a ___ improvement in the student\'s writing after intensive practice.',
        'source': 'Claude'
    },
    'pronouncer': {
        'definition': 'A person who pronounces words, especially one who announces words in spelling bees or language competitions; someone who speaks or articulates words in a particular way. In spelling bee competitions, the pronouncer plays a crucial role by clearly stating each word and providing additional information such as definitions and etymology.',
        'pronunciation': '/prəˈnaʊnsər/',
        'pronunciation_respelling': 'pruh-NOWN-sur',
        'etymology': 'From "pronounce" + suffix "-er," meaning one who pronounces, from Latin "pronuntiare."',
        'memory_tip': 'Think "pronounce" + "er" = one who speaks words clearly for others.',
        'example_sentence': 'The spelling bee ___ carefully articulated each word and provided helpful etymology information.',
        'source': 'Claude'
    },
    'pronunciations': {
        'definition': 'Plural of pronunciation; the ways in which words are spoken or articulated; the particular ways different people or regions say words. Pronunciations can vary significantly based on regional dialects, social groups, and individual speech patterns, making language dynamic and diverse across different communities.',
        'pronunciation': '/prəˌnʌnsiˈeɪʃənz/',
        'pronunciation_respelling': 'pruh-nun-see-AY-shunz',
        'etymology': 'Plural of "pronunciation," from Latin "pronuntiatio," meaning "a speaking forth" or "declaration."',
        'memory_tip': 'Think "pronunciation" + "s" = multiple ways of speaking the same words.',
        'example_sentence': 'The dictionary included multiple ___ for words that vary between American and British English.',
        'source': 'Claude'
    },
    'proof': {
        'definition': 'Evidence or argument establishing or helping to establish a fact or the truth of a statement; a test or trial of something; in mathematics, a logical argument demonstrating the truth of a theorem. Proof serves as the foundation of knowledge in mathematics, science, and logic, providing certainty through rigorous reasoning.',
        'pronunciation': '/pruːf/',
        'pronunciation_respelling': 'PROOF',
        'etymology': 'From Old French "prove," from Latin "probare" meaning "to test" or "to prove," from "probus" (good, honest).',
        'memory_tip': 'Think of the word itself as solid evidence = proof is evidence that something is true.',
        'example_sentence': 'The mathematician spent months developing a complete ___ for the challenging theorem.',
        'source': 'Claude'
    },
    'propaganda': {
        'definition': 'Information or ideas systematically spread to promote a particular political cause or point of view; biased or misleading publicity intended to influence public opinion. While often associated with negative manipulation, propaganda can also refer to any organized effort to spread particular beliefs or ideologies.',
        'pronunciation': '/ˌprɑːpəˈɡændə/',
        'pronunciation_respelling': 'prah-puh-GAN-duh',
        'etymology': 'From Latin "propaganda," meaning "things to be spread," from "propagare" (to propagate), originally from Catholic Church usage.',
        'memory_tip': 'Think "prop" (support) + "ganda" (spread) = spreading ideas to support a cause.',
        'example_sentence': 'Students learned to identify ___ techniques used in political advertisements and wartime posters.',
        'source': 'Claude'
    },
    'propane': {
        'definition': 'A colorless, flammable gas used as fuel for heating, cooking, and powering vehicles; a hydrocarbon with the chemical formula C₃H₈. Propane is commonly stored in pressurized tanks and is popular for portable applications such as camping stoves, grills, and heating systems in areas without natural gas infrastructure.',
        'pronunciation': '/ˈproʊpeɪn/',
        'pronunciation_respelling': 'PROH-payn',
        'etymology': 'From "prop-" (indicating three carbon atoms) + "-ane" (suffix for alkane hydrocarbons), coined in organic chemistry nomenclature.',
        'memory_tip': 'Think "pro" (three) + "pane" (glass-like clear) = clear gas with three carbons.',
        'example_sentence': 'The camping trip required several ___ canisters to fuel the portable cooking stove.',
        'source': 'Claude'
    },
    'propensity': {
        'definition': 'An inclination or natural tendency to behave in a particular way; a predisposition toward certain actions or outcomes. Propensities can be positive or negative traits that influence how individuals respond to situations, make decisions, or develop habits over time.',
        'pronunciation': '/prəˈpɛnsəti/',
        'pronunciation_respelling': 'pruh-PEN-sih-tee',
        'etymology': 'From Latin "propensitas," from "propensus" meaning "inclined" or "disposed," from "pro" (forward) + "pendere" (to hang).',
        'memory_tip': 'Think "pro" (toward) + "pensity" (hanging) = hanging toward a particular behavior.',
        'example_sentence': 'The child showed a strong ___ for artistic activities from an early age.',
        'source': 'Claude'
    },
    'proper': {
        'definition': 'Correct according to social conventions or accepted standards; belonging exclusively to a particular person or thing; genuine or actual. Proper behavior follows established rules and expectations, while proper nouns identify specific individuals, places, or things with unique characteristics.',
        'pronunciation': '/ˈprɑːpər/',
        'pronunciation_respelling': 'PRAH-pur',
        'etymology': 'From Old French "propre," from Latin "proprius" meaning "one\'s own" or "particular."',
        'memory_tip': 'Think of "property" - proper means belonging correctly or appropriately.',
        'example_sentence': 'Students must use ___ citation format when referencing sources in their research papers.',
        'source': 'Claude'
    },
    'properties': {
        'definition': 'Plural of property; characteristics or qualities that define something; possessions or real estate owned by someone; in science, the measurable or observable attributes of substances or systems. Mathematical properties include characteristics like commutativity and associativity that describe how operations behave.',
        'pronunciation': '/ˈprɑːpərtiz/',
        'pronunciation_respelling': 'PRAH-pur-teez',
        'etymology': 'Plural of "property," from Old French "proprieté," from Latin "proprietas" meaning "ownership" or "characteristic quality."',
        'memory_tip': 'Think "proper" + "ties" = things that properly belong to or characterize something.',
        'example_sentence': 'The chemistry students investigated the ___ of various acids and bases through laboratory experiments.',
        'source': 'Claude'
    },
    'prophecies': {
        'definition': 'Plural of prophecy; predictions or declarations of future events, especially those believed to be divinely inspired; statements about what will happen in the future. Throughout history, prophecies have played important roles in religious traditions, literature, and cultural beliefs about destiny and divine intervention.',
        'pronunciation': '/ˈprɑːfəsiz/',
        'pronunciation_respelling': 'PRAH-fuh-seez',
        'etymology': 'Plural of "prophecy," from Greek "propheteia," from "prophetes" meaning "interpreter" or "spokesperson for a god."',
        'memory_tip': 'Think "prophet" + "cies" = multiple statements from prophets about the future.',
        'example_sentence': 'Ancient texts contained numerous ___ about the rise and fall of great civilizations.',
        'source': 'Claude'
    },
    'prophet': {
        'definition': 'A person regarded as an inspired teacher or proclaimer of the will of God; someone who predicts future events; an advocate or pioneer of a particular cause or idea. Prophets have been central figures in many religious traditions, serving as intermediaries between the divine and human communities.',
        'pronunciation': '/ˈprɑːfɪt/',
        'pronunciation_respelling': 'PRAH-fit',
        'etymology': 'From Greek "prophetes," meaning "interpreter" or "spokesperson," from "pro" (before) + "phanai" (to speak).',
        'memory_tip': 'Think "pro" (before) + "phet" (speak) = one who speaks before events happen.',
        'example_sentence': 'The ancient ___ warned the people about the consequences of their actions.',
        'source': 'Claude'
    },
    'prophetically': {
        'definition': 'In a manner that predicts or foretells future events; with prophetic insight or foresight; as if inspired by divine revelation. This adverb describes actions or statements that demonstrate unusual ability to anticipate future developments or understand hidden truths.',
        'pronunciation': '/prəˈfɛtɪkli/',
        'pronunciation_respelling': 'pruh-FET-ik-lee',
        'etymology': 'From "prophetic" + suffix "-ally," from Greek "prophetikos" meaning "of or pertaining to a prophet."',
        'memory_tip': 'Think "prophetic" + "ally" = in the manner of a prophet, with foresight.',
        'example_sentence': 'The scientist ___ warned about climate change decades before it became widely accepted.',
        'source': 'Claude'
    },
    'propinquity': {
        'definition': 'Nearness in place or time; physical or temporal proximity; similarity or kinship in nature or character. In psychology, the propinquity effect describes how people are more likely to form relationships with those who are geographically close to them. The term encompasses both physical closeness and figurative similarity.',
        'pronunciation': '/prəˈpɪŋkwəti/',
        'pronunciation_respelling': 'pruh-PING-kwih-tee',
        'etymology': 'From Latin "propinquitas," from "propinquus" meaning "near" or "neighboring," from "prope" (near).',
        'memory_tip': 'Think "prop" (close) + "pinquity" (nearness) = being close in space or nature.',
        'example_sentence': 'The ___ of their apartments led to a lasting friendship between the neighbors.',
        'source': 'Claude'
    },
    'propinquityepidermis': {
        'definition': '[COMBINED WORD ERROR] This appears to be "propinquity" + "epidermis" incorrectly joined. Should be separated into two distinct terms: "propinquity" (nearness or proximity) and "epidermis" (the outer layer of skin).',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "propinquity" (Latin: nearness) with "epidermis" (Greek: outer skin).',
        'memory_tip': '[ERROR] This should be split into "propinquity" (closeness) and "epidermis" (skin layer).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "propinquity" and "epidermis."',
        'source': 'Claude'
    },
    'propitiousellipsis': {
        'definition': '[COMBINED WORD ERROR] This appears to be "propitious" + "ellipsis" incorrectly joined. Should be separated into two distinct terms: "propitious" (favorable or advantageous) and "ellipsis" (a series of dots indicating omitted text).',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "propitious" (Latin: favorable) with "ellipsis" (Greek: omission).',
        'memory_tip': '[ERROR] This should be split into "propitious" (favorable) and "ellipsis" (omission marks).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "propitious" and "ellipsis."',
        'source': 'Claude'
    },
    'proportional': {
        'definition': 'Corresponding in size, degree, or intensity; having the same or a constant ratio; maintaining proper or equal relationships between parts. In mathematics, proportional relationships describe how one quantity changes in relation to another, maintaining a consistent ratio throughout the relationship.',
        'pronunciation': '/prəˈpɔːrʃənəl/',
        'pronunciation_respelling': 'pruh-POR-shun-ul',
        'etymology': 'From "proportion" + suffix "-al," from Latin "proportio" meaning "comparative relation," from "pro" (according to) + "portio" (share).',
        'memory_tip': 'Think "pro" (according to) + "portional" (portions) = according to proper portions.',
        'example_sentence': 'The recipe required ingredients in ___ amounts based on the number of guests.',
        'source': 'Claude'
    },
    'proportionate': {
        'definition': 'Corresponding in size or amount to something else; properly balanced or adjusted according to some standard or principle. When something is proportionate, it maintains appropriate relationships with other elements, avoiding excess or deficiency in comparison to what is expected or needed.',
        'pronunciation': '/prəˈpɔːrʃənət/',
        'pronunciation_respelling': 'pruh-POR-shun-ut',
        'etymology': 'From Latin "proportionatus," past participle of "proportionare" meaning "to make proportional."',
        'memory_tip': 'Think "proportion" + "ate" = made to be in proper proportion.',
        'example_sentence': 'The punishment should be ___ to the severity of the offense committed.',
        'source': 'Claude'
    },
    'proposal': {
        'definition': 'A plan or suggestion put forward for consideration or discussion; an offer of marriage; a formal document outlining a proposed course of action. Proposals serve as structured ways to present ideas, request approval, or initiate important life changes, requiring careful thought and clear communication.',
        'pronunciation': '/prəˈpoʊzəl/',
        'pronunciation_respelling': 'pruh-POH-zul',
        'etymology': 'From "propose" + suffix "-al," from Old French "proposer," from Latin "proponere" meaning "to set forth."',
        'memory_tip': 'Think "propose" + "al" = the act or document of proposing something.',
        'example_sentence': 'The student council submitted a detailed ___ for improving campus recycling programs.',
        'source': 'Claude'
    },
    'propound': {
        'definition': 'To put forward for consideration; to offer or suggest an idea, theory, or argument for discussion; to present or propose formally. In academic and intellectual contexts, propounding involves introducing complex ideas or theories that require careful examination and debate among knowledgeable individuals.',
        'pronunciation': '/prəˈpaʊnd/',
        'pronunciation_respelling': 'pruh-POWND',
        'etymology': 'From Latin "proponere," meaning "to set forth" or "to propose," from "pro" (forth) + "ponere" (to place).',
        'memory_tip': 'Think "pro" (forth) + "pound" (place firmly) = placing ideas forth firmly.',
        'example_sentence': 'The philosopher decided to ___ a new theory about the nature of consciousness.',
        'source': 'Claude'
    },
    'propre': {
        'definition': 'French word meaning "own," "proper," or "clean"; used in French grammar to distinguish proper nouns from common nouns; characteristic of something belonging exclusively to a particular person or thing. In linguistics, "nom propre" refers to proper nouns that identify specific individuals, places, or entities.',
        'pronunciation': '/prɔpr/',
        'pronunciation_respelling': 'PROPR (French)',
        'etymology': 'From Old French "propre," from Latin "proprius" meaning "one\'s own" or "particular to oneself."',
        'memory_tip': 'Think French for "proper" or "own" - similar to English "proper" but French pronunciation.',
        'example_sentence': 'In French class, students learned to distinguish between "nom commun" and "nom ___."',
        'source': 'Claude'
    },
    'propreamphistylar': {
        'definition': '[COMBINED WORD ERROR] This appears to be "propre" + "amphistylar" incorrectly joined. Should be separated into two distinct terms: "propre" (French for proper/own) and "amphistylar" (architectural term for a building with columns on both ends).',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "propre" (French: own/proper) with "amphistylar" (Greek: columns on both sides).',
        'memory_tip': '[ERROR] This should be split into "propre" (French: own) and "amphistylar" (architectural columns).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "propre" and "amphistylar."',
        'source': 'Claude'
    },
    'proprietary': {
        'definition': 'Relating to ownership; belonging exclusively to a particular person or company; protected by trademark or patent; characterized by ownership rights. Proprietary products, information, or methods are controlled by specific entities and cannot be used freely by others without permission.',
        'pronunciation': '/prəˈpraɪəteri/',
        'pronunciation_respelling': 'pruh-PRY-uh-ter-ee',
        'etymology': 'From Latin "proprietarius," from "proprietas" meaning "ownership" or "property," from "proprius" (one\'s own).',
        'memory_tip': 'Think "property" + "ary" = relating to property ownership.',
        'example_sentence': 'The company closely guarded its ___ software technology from competitors.',
        'source': 'Claude'
    },
    'proprioceptive': {
        'definition': 'Relating to proprioception, the sense of body position and movement in space; involving awareness of the position and movement of body parts without relying on vision. Proprioceptive feedback helps maintain balance, coordinate movements, and perform activities requiring spatial awareness and motor control.',
        'pronunciation': '/ˌproʊpriəˈsɛptɪv/',
        'pronunciation_respelling': 'proh-pree-uh-SEP-tiv',
        'etymology': 'From Latin "proprius" (one\'s own) + "capere" (to take) + suffix "-ive," referring to self-perception of body position.',
        'memory_tip': 'Think "proprio" (own) + "ceptive" (receiving) = receiving information about your own body.',
        'example_sentence': 'Physical therapy included ___ exercises to improve the patient\'s balance and coordination.',
        'source': 'Claude'
    },
    'propulsion': {
        'definition': 'The action of driving or pushing forward; the force that moves something ahead, especially in rockets, aircraft, or ships. Propulsion systems convert energy into thrust, enabling vehicles to overcome resistance and achieve motion. Different types include jet propulsion, rocket propulsion, and propeller-driven systems.',
        'pronunciation': '/prəˈpʌlʃən/',
        'pronunciation_respelling': 'pruh-PUL-shun',
        'etymology': 'From Latin "propulsio," from "propellere" meaning "to drive forward," from "pro" (forward) + "pellere" (to drive).',
        'memory_tip': 'Think "pro" (forward) + "pulsion" (pushing) = pushing forward movement.',
        'example_sentence': 'The spacecraft used ion ___ to efficiently travel through the solar system.',
        'source': 'Claude'
    },
    'prorogue': {
        'definition': 'To discontinue or suspend the meetings of a legislative body without dissolving it; to defer or postpone; to extend or prolong. In parliamentary systems, prorogation ends a session of parliament while keeping the same parliament in existence, allowing for a fresh start when sessions resume.',
        'pronunciation': '/prəˈroʊɡ/',
        'pronunciation_respelling': 'pruh-ROHG',
        'etymology': 'From Latin "prorogare," meaning "to extend" or "to prolong," from "pro" (forth) + "rogare" (to ask or propose).',
        'memory_tip': 'Think "pro" (forth) + "rogue" (extend) = extending the time period forth.',
        'example_sentence': 'The prime minister decided to ___ parliament until after the summer recess.',
        'source': 'Claude'
    },
    'prosceniumpolitesse': {
        'definition': '[COMBINED WORD ERROR] This appears to be "proscenium" + "politesse" incorrectly joined. Should be separated into two distinct terms: "proscenium" (the area of a theater stage in front of the curtain) and "politesse" (formal politeness or courtesy).',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "proscenium" (Greek: before the stage) with "politesse" (French: politeness).',
        'memory_tip': '[ERROR] This should be split into "proscenium" (theater stage) and "politesse" (courtesy).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "proscenium" and "politesse."',
        'source': 'Claude'
    },
    'proscribed': {
        'definition': 'Past tense of proscribe; forbidden or prohibited, especially by law; condemned or denounced as dangerous; officially banned or outlawed. When something is proscribed, it is explicitly prohibited by authority and carries consequences for violation. This differs from "prescribed," which means recommended or required.',
        'pronunciation': '/proʊˈskraɪbd/',
        'pronunciation_respelling': 'proh-SKRYBD',
        'etymology': 'From Latin "proscribere," meaning "to publish" or "to outlaw," from "pro" (forth) + "scribere" (to write).',
        'memory_tip': 'Think "pro" (forth) + "scribed" (written) = written forth as forbidden.',
        'example_sentence': 'The use of certain performance-enhancing drugs is strictly ___ in professional sports.',
        'source': 'Claude'
    },
    'prosecutor': {
        'definition': 'A lawyer who conducts criminal proceedings on behalf of the state or government; someone who initiates and carries forward legal action against an accused person. Prosecutors play a crucial role in the justice system by presenting evidence and arguments to prove criminal cases in court.',
        'pronunciation': '/ˈprɑːsɪkjuːtər/',
        'pronunciation_respelling': 'PRAH-sih-kyoo-tur',
        'etymology': 'From Latin "prosecutor," from "prosequi" meaning "to follow after" or "to pursue," from "pro" (forward) + "sequi" (to follow).',
        'memory_tip': 'Think "pro" (forward) + "secutor" (pursuer) = one who pursues justice forward.',
        'example_sentence': 'The ___ presented compelling evidence that convinced the jury of the defendant\'s guilt.',
        'source': 'Claude'
    },
    'proselytiser': {
        'definition': 'British spelling of proselytizer; a person who attempts to convert others to a particular religion, belief, or opinion; someone who tries to recruit others to join their cause or faith. Proselytising involves active efforts to persuade others to adopt specific beliefs or practices.',
        'pronunciation': '/ˈprɑːsəlaɪtaɪzər/',
        'pronunciation_respelling': 'PRAH-suh-ly-ty-zur',
        'etymology': 'From "proselytize" + suffix "-er," from Greek "proselutos" meaning "one who has come to" or "convert."',
        'memory_tip': 'Think "proselyte" (convert) + "iser" (one who makes) = one who makes converts.',
        'example_sentence': 'The religious ___ traveled from village to village sharing his faith with anyone willing to listen.',
        'source': 'Claude'
    },
    'proselytizer': {
        'definition': 'American spelling of proselytiser; a person who attempts to convert others to a particular religion, belief, or opinion; someone who actively recruits others to join their cause or adopt their viewpoint. Proselytizing can be religious, political, or ideological in nature.',
        'pronunciation': '/ˈprɑːsəlaɪtaɪzər/',
        'pronunciation_respelling': 'PRAH-suh-ly-ty-zur',
        'etymology': 'From "proselytize" + suffix "-er," from Greek "proselutos" meaning "stranger" or "convert to Judaism."',
        'memory_tip': 'Think "proselyte" (convert) + "izer" (one who makes) = one who makes converts.',
        'example_sentence': 'The enthusiastic ___ spent hours discussing the benefits of renewable energy with neighbors.',
        'source': 'Claude'
    },
    'prosody': {
        'definition': 'The patterns of rhythm and sound used in poetry; the study of versification including meter, rhyme, and stanza forms; in linguistics, the rhythm, stress, and intonation of speech. Prosody encompasses the musical qualities of language that contribute to meaning and emotional impact in both poetry and everyday speech.',
        'pronunciation': '/ˈprɑːsədi/',
        'pronunciation_respelling': 'PRAH-suh-dee',
        'etymology': 'From Greek "prosodia," meaning "song sung to music" or "accent," from "pros" (toward) + "ode" (song).',
        'memory_tip': 'Think "pros" (toward) + "ody" (song) = the song-like qualities of speech.',
        'example_sentence': 'The poetry class focused on analyzing the ___ of Shakespeare\'s sonnets.',
        'source': 'Claude'
    },
    'prosperous': {
        'definition': 'Successful in material terms; flourishing financially; bringing wealth or success; characterized by economic well-being and growth. Prosperity involves not just individual wealth but often indicates broader economic health and opportunities for advancement and security.',
        'pronunciation': '/ˈprɑːspərəs/',
        'pronunciation_respelling': 'PRAH-spur-us',
        'etymology': 'From Latin "prosperus," meaning "favorable" or "successful," from "pro" (according to) + "spes" (hope).',
        'memory_tip': 'Think "pro" (for) + "sperous" (hope) = having hope fulfilled with success.',
        'example_sentence': 'The ___ merchant family donated generously to local schools and hospitals.',
        'source': 'Claude'
    },
    'prosthetic': {
        'definition': 'Relating to artificial devices that replace missing body parts; denoting an artificial substitute for a part of the body. Prosthetic devices range from simple cosmetic replacements to sophisticated mechanical devices that can be controlled by neural signals, dramatically improving quality of life for amputees and those with congenital limb differences.',
        'pronunciation': '/prɑːsˈθɛtɪk/',
        'pronunciation_respelling': 'prah-STHET-ik',
        'etymology': 'From Greek "prosthetikos," meaning "adding to" or "putting on," from "pros" (toward) + "tithenai" (to place).',
        'memory_tip': 'Think "pros" (toward) + "thetic" (placing) = placing artificial parts toward the body.',
        'example_sentence': 'The advanced ___ leg allowed the athlete to return to competitive running.',
        'source': 'Claude'
    }
}

def process_batch_140():
    """Process batch 140 spelling bee words"""
    
    calculator = DifficultyCalculator()
    
    # Read input CSV
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_140_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_140_processed.csv'
    
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
                        'notes': 'Batch 140 processing',
                        'review_status': 'pending',
                        'batch_number': 140
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
            
            print(f"\nBatch 140 processing complete!")
            print(f"Successfully processed {len(processed_words)}/50 words")
            print(f"Output saved to: {output_file}")
            
            # Flag any combined word errors
            combined_errors = [word for word in processed_words if '[COMBINED WORD ERROR]' in word['definition']]
            if combined_errors:
                print(f"\nCombined word errors detected: {len(combined_errors)}")
                for error in combined_errors:
                    print(f"  - {error['word']}")
        
    except Exception as e:
        print(f"Error processing batch 140: {e}")
        return False
    
    return True

if __name__ == "__main__":
    process_batch_140()