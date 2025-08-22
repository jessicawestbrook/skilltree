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
        if re.search(r'[bt](?![aeiou])|[kl](?=n)|[w](?=r)|[h](?=[^aeiou])|[p](?=s)|[pt](?=[^aeiou])', word.lower()):
            irregular_patterns += 1
            
        # Double letters not in pronunciation
        if re.search(r'(.)\1', word) and 'double' not in pronunciation.lower():
            irregular_patterns += 1
            
        # Score inversely related to irregular patterns
        return min(10, max(1, 8 - irregular_patterns * 2))
    
    def _calculate_word_frequency(self, word):
        """Score 1-10: How common the word is (lower = more common)"""
        # Common words (1-3)
        common = ['provide', 'public', 'publish', 'published', 'publishes', 'proud', 'proxy', 'pulley']
        if word.lower() in common:
            return 2
            
        # Moderately common (4-6)
        moderate = ['provincial', 'provision', 'provocation', 'prudence', 'psychiatrist', 'pulpit']
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
        prefixes = ['pro', 'prot', 'prov', 'pru', 'ps', 'pt', 'pub', 'puc', 'pud', 'pue', 'pug', 'pul']
        suffixes = ['ous', 'ity', 'ive', 'ment', 'tion', 'ic', 'ary', 'ence', 'ent', 'ed', 'ing', 'ate', 'ism', 'ist']
        
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
        languages = ['latin', 'greek', 'french', 'spanish', 'italian', 'german', 'sanskrit', 'old english', 'hebrew', 'arabic']
        language_count = sum(1 for lang in languages if lang in etymology.lower())
        
        if language_count >= 2:
            complexity += 3
        elif language_count == 1:
            complexity += 1
            
        # Ancient origins add complexity
        if any(ancient in etymology.lower() for ancient in ['ancient', 'classical', 'medieval']):
            complexity += 2
            
        return min(10, complexity)

# Comprehensive word data for batch 141
word_data = {
    'protectorate': {
        'definition': 'A state that is controlled and protected by another more powerful state; a territory or jurisdiction under the protection and partial control of a stronger nation. Protectorates maintain some degree of internal autonomy while relying on the protecting power for defense and foreign relations. This relationship has been common throughout history as a form of political arrangement between unequal powers.',
        'pronunciation': '/prəˈtɛktərət/',
        'pronunciation_respelling': 'pruh-TEK-tur-ut',
        'etymology': 'From "protector" + suffix "-ate," from Latin "protegere" meaning "to cover in front" or "to protect."',
        'memory_tip': 'Think "protect" + "orate" (like senate) = a protected state or territory.',
        'example_sentence': 'The small island nation became a ___ of the larger maritime power for security.',
        'source': 'Claude'
    },
    'proteron': {
        'definition': 'A figure of speech in which the natural or logical order of words or ideas is reversed; putting first what should logically come second. In rhetoric and grammar, proteron refers to a reversal of chronological or logical sequence, often used for emphasis or stylistic effect in literature and speech.',
        'pronunciation': '/ˈproʊtərɒn/',
        'pronunciation_respelling': 'PROH-tur-on',
        'etymology': 'From Greek "proteron," meaning "former" or "earlier," from "protos" (first).',
        'memory_tip': 'Think "proto" (first) + "ron" = putting the first thing in the wrong place.',
        'example_sentence': 'The phrase "put on your shoes and socks" is an example of ___.',
        'source': 'Claude'
    },
    'protruding': {
        'definition': 'Present participle of protrude; sticking out beyond the surrounding surface; extending outward in a noticeable way. Something that is protruding projects beyond the normal boundary or edge, making it conspicuous or potentially problematic for movement or aesthetics.',
        'pronunciation': '/prəˈtruːdɪŋ/',
        'pronunciation_respelling': 'pruh-TROO-ding',
        'etymology': 'From Latin "protrudere," meaning "to thrust forward," from "pro" (forward) + "trudere" (to thrust).',
        'memory_tip': 'Think "pro" (forward) + "truding" (thrusting) = thrusting forward/sticking out.',
        'example_sentence': 'The ___ nail in the floorboard caught everyone\'s attention.',
        'source': 'Claude'
    },
    'protuberant': {
        'definition': 'Bulging out; swelling beyond the surrounding surface; prominently protruding. This term is often used in medical contexts to describe abnormal swellings or in general description to indicate something that extends noticeably beyond its normal boundaries or the surrounding area.',
        'pronunciation': '/prəˈtuːbərənt/',
        'pronunciation_respelling': 'pruh-TOO-bur-unt',
        'etymology': 'From Latin "protuberans," from "protuberare" meaning "to swell out," from "pro" (forth) + "tuber" (swelling).',
        'memory_tip': 'Think "pro" (forth) + "tuberant" (tube-like swelling) = swelling forth.',
        'example_sentence': 'The doctor examined the patient\'s ___ abdomen for signs of illness.',
        'source': 'Claude'
    },
    'proud': {
        'definition': 'Feeling deep satisfaction derived from one\'s own achievements or those of someone close; having self-respect and dignity; showing a high or excessively high opinion of oneself. Pride can be a positive emotion reflecting legitimate accomplishment or a negative trait when it becomes arrogance or vanity.',
        'pronunciation': '/praʊd/',
        'pronunciation_respelling': 'PROWD',
        'etymology': 'From Old English "prūd," from Old French "prou," meaning "brave" or "valiant."',
        'memory_tip': 'Think of standing tall with satisfaction - "proud" sounds strong and confident.',
        'example_sentence': 'The parents felt ___ watching their daughter graduate with honors.',
        'source': 'Claude'
    },
    'provenance': {
        'definition': 'The chronology of ownership, custody, or location of an artwork or artifact; the origin or source of something. In art and antiquities, provenance establishes authenticity and legal ownership. More broadly, it refers to the history or origin of anything, particularly when establishing credibility or value.',
        'pronunciation': '/ˈprɒvənəns/',
        'pronunciation_respelling': 'PRAH-vuh-nuns',
        'etymology': 'From French "provenance," from "provenir" meaning "to come forth," from Latin "provenire."',
        'memory_tip': 'Think "prove" + "nance" = proving where something comes from.',
        'example_sentence': 'The museum carefully documented the ___ of each artifact in its collection.',
        'source': 'Claude'
    },
    'proverb': {
        'definition': 'A short saying that expresses a general truth or piece of advice; a traditional maxim or adage passed down through generations. Proverbs distill wisdom into memorable phrases that convey cultural values, practical knowledge, or moral guidance through metaphor and concise language.',
        'pronunciation': '/ˈprɒvɜːrb/',
        'pronunciation_respelling': 'PRAH-vurb',
        'etymology': 'From Old French "proverbe," from Latin "proverbium," from "pro" (forth) + "verbum" (word).',
        'memory_tip': 'Think "pro" (forth) + "verb" (word) = words spoken forth as wisdom.',
        'example_sentence': 'The ancient ___ "A stitch in time saves nine" teaches the value of preventive action.',
        'source': 'Claude'
    },
    'proviant': {
        'definition': 'Provisions or supplies, especially food for a journey or military campaign; victuals or sustenance carried for future use. This term, while less common in modern English, refers to the essential supplies needed to sustain people during travel or in situations where regular food sources are unavailable.',
        'pronunciation': '/ˈproʊviənt/',
        'pronunciation_respelling': 'PROH-vee-unt',
        'etymology': 'From German "Proviant," from French "provende," ultimately from Latin "providere" (to provide).',
        'memory_tip': 'Think "provide" + "ant" (like servant) = something that provides sustenance.',
        'example_sentence': 'The expedition team carefully calculated their ___ needs for the month-long journey.',
        'source': 'Claude'
    },
    'provide': {
        'definition': 'To make available for use; to supply or furnish something needed; to prepare for future use or application; to stipulate as a condition. Providing involves anticipating needs and ensuring that necessary resources, information, or support are accessible when required.',
        'pronunciation': '/prəˈvaɪd/',
        'pronunciation_respelling': 'pruh-VYD',
        'etymology': 'From Latin "providere," meaning "to foresee" or "to prepare," from "pro" (before) + "videre" (to see).',
        'memory_tip': 'Think "pro" (before) + "vide" (see) = seeing beforehand to supply what\'s needed.',
        'example_sentence': 'The school will ___ all necessary textbooks for the new semester.',
        'source': 'Claude'
    },
    'provincial': {
        'definition': 'Relating to a province or the regions outside the capital; having a narrow or unsophisticated outlook; characteristic of rural or outlying areas. Provincial can describe both geographic regions and attitudes that are considered limited in scope or parochial in perspective compared to metropolitan standards.',
        'pronunciation': '/prəˈvɪnʃəl/',
        'pronunciation_respelling': 'pruh-VIN-shul',
        'etymology': 'From Latin "provincialis," from "provincia" meaning "administrative district" or "sphere of duty."',
        'memory_tip': 'Think "province" + "ial" = relating to provinces/rural areas.',
        'example_sentence': 'The cosmopolitan writer sometimes felt constrained by her ___ upbringing.',
        'source': 'Claude'
    },
    'provision': {
        'definition': 'The action of providing or supplying something; a supply of food and other necessities; a clause in a legal document or agreement. Provisions ensure that needs are met, whether material requirements for survival or legal stipulations that govern behavior and obligations.',
        'pronunciation': '/prəˈvɪʒən/',
        'pronunciation_respelling': 'pruh-VIZH-un',
        'etymology': 'From Latin "provisio," from "providere" meaning "to foresee" or "to provide."',
        'memory_tip': 'Think "provide" + "sion" = the act of providing supplies or conditions.',
        'example_sentence': 'The contract included a ___ for annual salary increases based on performance.',
        'source': 'Claude'
    },
    'proviso': {
        'definition': 'A condition attached to an agreement or statement; a stipulation or qualification that limits or modifies the main provision. A proviso introduces an exception or additional requirement that must be met for the primary agreement to remain valid or effective.',
        'pronunciation': '/prəˈvaɪzoʊ/',
        'pronunciation_respelling': 'pruh-VY-zoh',
        'etymology': 'From Latin "proviso," meaning "it being provided," from "providere" (to provide or foresee).',
        'memory_tip': 'Think "provide" + "so" = providing a condition that must be so.',
        'example_sentence': 'The scholarship was awarded with the ___ that the student maintain a 3.5 GPA.',
        'source': 'Claude'
    },
    'provocation': {
        'definition': 'Action or speech that deliberately angers or annoys someone; something that incites anger, resentment, or strong reaction. Provocation can be intentional attempts to elicit responses or unintentional actions that nonetheless trigger emotional or behavioral reactions in others.',
        'pronunciation': '/ˌprɒvəˈkeɪʃən/',
        'pronunciation_respelling': 'prah-vuh-KAY-shun',
        'etymology': 'From Latin "provocatio," from "provocare" meaning "to call forth" or "to challenge."',
        'memory_tip': 'Think "provoke" + "ation" = the act of provoking or causing reaction.',
        'example_sentence': 'Despite the ___, she remained calm and refused to respond angrily.',
        'source': 'Claude'
    },
    'prowess': {
        'definition': 'Skill or expertise in a particular activity or field; bravery in battle or conflict; exceptional ability or competence. Prowess implies not just competence but mastery that distinguishes someone from others in their field, whether in combat, sports, academics, or professional endeavors.',
        'pronunciation': '/ˈpraʊəs/',
        'pronunciation_respelling': 'PROW-us',
        'etymology': 'From Old French "proesse," from "prou" meaning "brave" or "valiant."',
        'memory_tip': 'Think "pro" (expert) + "wess" (prowess) = expert-level skill and bravery.',
        'example_sentence': 'The athlete\'s ___ on the basketball court earned her a college scholarship.',
        'source': 'Claude'
    },
    'proximo': {
        'definition': 'Of or relating to next month; used in business correspondence to indicate the following month. This term appears in formal and commercial writing, particularly in scheduling, invoicing, and correspondence where precise temporal references are important for business operations.',
        'pronunciation': '/ˈprɒksɪmoʊ/',
        'pronunciation_respelling': 'PROK-sih-moh',
        'etymology': 'From Latin "proximo," meaning "in the next" or "nearest," from "proximus" (nearest).',
        'memory_tip': 'Think "proximity" shortened = the next closest month coming up.',
        'example_sentence': 'The invoice is due on the 15th ___, meaning next month.',
        'source': 'Claude'
    },
    'proxy': {
        'definition': 'The authority to represent someone else, especially in voting; a person authorized to act for another; a substitute or replacement. In technology, a proxy server acts as an intermediary between users and other servers, while in governance, proxy voting allows representation when direct participation is impossible.',
        'pronunciation': '/ˈprɑːksi/',
        'pronunciation_respelling': 'PROK-see',
        'etymology': 'From Latin "procuratio," shortened to "proc.," meaning "management of another\'s affairs."',
        'memory_tip': 'Think "approximate" shortened = someone acting approximately as you would.',
        'example_sentence': 'She voted by ___ since she couldn\'t attend the shareholders\' meeting.',
        'source': 'Claude'
    },
    'prudence': {
        'definition': 'The quality of being prudent; careful judgment in practical affairs; discretion in the management of one\'s actions and resources. Prudence involves thinking before acting, considering consequences, and making decisions based on wisdom rather than impulse or emotion.',
        'pronunciation': '/ˈpruːdəns/',
        'pronunciation_respelling': 'PROO-dunse',
        'etymology': 'From Latin "prudentia," from "prudens" meaning "foreseeing" or "wise," from "pro" (before) + "videre" (to see).',
        'memory_tip': 'Think "prude" (careful) + "ence" = being careful and wise in decisions.',
        'example_sentence': 'Financial ___ required them to save money rather than spend impulsively.',
        'source': 'Claude'
    },
    'pruners': {
        'definition': 'Plural of pruner; tools used for cutting and trimming plants, bushes, and small tree branches; people who prune or trim vegetation. Garden pruners come in various sizes and designs, from small hand pruners for delicate work to long-handled loppers for thicker branches.',
        'pronunciation': '/ˈpruːnərz/',
        'pronunciation_respelling': 'PROO-nurz',
        'etymology': 'From "prune" + suffix "-er" + plural "-s," from Old French "proignier" (to prune).',
        'memory_tip': 'Think "prune" + "ers" = tools or people that prune/cut plants.',
        'example_sentence': 'The gardener used sharp ___ to trim the rosebushes before winter.',
        'source': 'Claude'
    },
    'pruritus': {
        'definition': 'Severe itching of the skin; the medical term for persistent, uncomfortable itching that may lead to scratching and potential skin damage. Pruritus can result from various causes including allergic reactions, skin conditions, systemic diseases, or medication side effects, requiring medical evaluation for proper treatment.',
        'pronunciation': '/prʊˈraɪtəs/',
        'pronunciation_respelling': 'pruh-RY-tus',
        'etymology': 'From Latin "pruritus," from "prurire" meaning "to itch."',
        'memory_tip': 'Think "purr" (like scratching) + "itus" (medical condition) = itching condition.',
        'example_sentence': 'The dermatologist prescribed medication to relieve the patient\'s chronic ___.',
        'source': 'Claude'
    },
    'psalmody': {
        'definition': 'The practice of singing psalms or other religious songs; the art of composing or arranging psalm music. Psalmody has been central to Christian worship traditions, involving both the musical setting of biblical psalms and the congregational singing that accompanies religious services.',
        'pronunciation': '/ˈsælmədi/',
        'pronunciation_respelling': 'SAL-muh-dee',
        'etymology': 'From Greek "psalmodia," from "psalmos" (psalm) + "ode" (song).',
        'memory_tip': 'Think "psalm" + "ody" (like melody) = singing psalms melodically.',
        'example_sentence': 'The church choir specialized in traditional ___ dating back centuries.',
        'source': 'Claude'
    },
    'psamm': {
        'definition': 'A geological term referring to sand or sandy sediment; used in scientific contexts to describe sandy formations or deposits. In geology and ecology, psamm describes granular materials that form specific habitats and geological structures, particularly in coastal and desert environments.',
        'pronunciation': '/sæm/',
        'pronunciation_respelling': 'SAM',
        'etymology': 'From Greek "psammos," meaning "sand."',
        'memory_tip': 'Think "psalm" without the "l" = relates to sand/sandy materials.',
        'example_sentence': 'The coastal ___ provided habitat for specialized plant species.',
        'source': 'Claude'
    },
    'psammophile': {
        'definition': 'An organism that thrives in sandy environments; a plant or animal adapted to live in sand or sandy soils. Psammophiles have evolved specific adaptations to survive in the unique conditions of sandy habitats, including water conservation and specialized root or movement systems.',
        'pronunciation': '/ˈsæməfaɪl/',
        'pronunciation_respelling': 'SAM-uh-fyl',
        'etymology': 'From Greek "psammos" (sand) + "philos" (loving).',
        'memory_tip': 'Think "psalm" + "file" = filing/organizing in sand = loving sandy places.',
        'example_sentence': 'Desert succulents are excellent examples of ___ plants.',
        'source': 'Claude'
    },
    'pschent': {
        'definition': 'The double crown of ancient Egypt, combining the white crown of Upper Egypt and the red crown of Lower Egypt; a symbol of unified rule over both regions. The pschent represented the pharaoh\'s authority over the entire kingdom and was one of the most important regalia in ancient Egyptian royal iconography.',
        'pronunciation': '/ˈʃɛnt/',
        'pronunciation_respelling': 'SHENT',
        'etymology': 'From ancient Egyptian, possibly related to "sekhemty" meaning "the two powerful ones."',
        'memory_tip': 'Think "sent" with "p" = the crown sent/given to unified Egyptian rulers.',
        'example_sentence': 'Pharaoh\'s ___ symbolized his rule over both Upper and Lower Egypt.',
        'source': 'Claude'
    },
    'pseudonymous': {
        'definition': 'Using or characterized by the use of a false name or pseudonym; written or published under an assumed name. Authors, artists, and writers often publish pseudonymous works to protect their identity, explore different genres, or separate their personal and professional lives.',
        'pronunciation': '/suːˈdɒnɪməs/',
        'pronunciation_respelling': 'soo-DON-ih-mus',
        'etymology': 'From Greek "pseudonumos," from "pseudes" (false) + "onoma" (name).',
        'memory_tip': 'Think "pseudo" (false) + "nymous" (name) = using a false name.',
        'example_sentence': 'The ___ author\'s true identity remained a mystery for decades.',
        'source': 'Claude'
    },
    'psoriasis': {
        'definition': 'A chronic autoimmune skin condition characterized by red, scaly patches that appear on various parts of the body. Psoriasis occurs when the immune system causes skin cells to grow too quickly, resulting in thick, silvery scales and itchy, dry, red patches that can be painful and aesthetically concerning.',
        'pronunciation': '/səˈraɪəsɪs/',
        'pronunciation_respelling': 'suh-RY-uh-sis',
        'etymology': 'From Greek "psoriasis," from "psora" meaning "itch" or "mange."',
        'memory_tip': 'Think "sore" in the middle = a skin condition that can be sore and itchy.',
        'example_sentence': 'The dermatologist recommended a new treatment for the patient\'s ___.',
        'source': 'Claude'
    },
    'psychiatrist': {
        'definition': 'A medical doctor who specializes in diagnosing and treating mental health disorders; a physician trained in psychiatry who can prescribe medications and provide therapy. Psychiatrists combine medical knowledge with psychological understanding to treat conditions ranging from depression and anxiety to severe mental illnesses.',
        'pronunciation': '/saɪˈkaɪətrɪst/',
        'pronunciation_respelling': 'sy-KY-uh-trist',
        'etymology': 'From "psychiatry" + suffix "-ist," from Greek "psyche" (mind) + "iatros" (physician).',
        'memory_tip': 'Think "psyche" (mind) + "iatrist" (doctor) = doctor of the mind.',
        'example_sentence': 'The ___ prescribed medication to help manage the patient\'s anxiety disorder.',
        'source': 'Claude'
    },
    'psychoanalysis': {
        'definition': 'A method of treating mental disorders developed by Freud, involving analysis of unconscious thoughts and feelings; a theory of personality emphasizing unconscious psychological processes. Psychoanalysis explores how early experiences and repressed memories influence current behavior and emotional patterns.',
        'pronunciation': '/ˌsaɪkoʊəˈnæləsɪs/',
        'pronunciation_respelling': 'sy-koh-uh-NAL-uh-sis',
        'etymology': 'From Greek "psyche" (mind) + "analysis" (breaking down).',
        'memory_tip': 'Think "psycho" (mind) + "analysis" = analyzing the mind deeply.',
        'example_sentence': 'Freud\'s development of ___ revolutionized understanding of human psychology.',
        'source': 'Claude'
    },
    'psychometry': {
        'definition': 'The measurement of mental capabilities and processes; the statistical analysis of psychological test results; in parapsychology, the alleged ability to discover information about objects by touching them. In psychology, psychometry involves standardized testing and measurement of cognitive abilities, personality traits, and behavioral patterns.',
        'pronunciation': '/saɪˈkɒmətri/',
        'pronunciation_respelling': 'sy-KOM-uh-tree',
        'etymology': 'From Greek "psyche" (mind) + "metron" (measure).',
        'memory_tip': 'Think "psycho" (mind) + "metry" (measuring) = measuring mental abilities.',
        'example_sentence': 'The educational ___ exam helped identify students\' learning strengths and weaknesses.',
        'source': 'Claude'
    },
    'pterodactyl': {
        'definition': 'An extinct flying reptile from the Mesozoic era; a pterosaur with a long crest and large wingspan. Pterodactyls were not dinosaurs but flying reptiles that lived alongside dinosaurs, featuring wing membranes stretched between elongated finger bones and specialized adaptations for flight.',
        'pronunciation': '/ˌtɛrəˈdæktəl/',
        'pronunciation_respelling': 'ter-uh-DAK-til',
        'etymology': 'From Greek "pteron" (wing) + "daktylos" (finger).',
        'memory_tip': 'Think "wing" + "finger" = wings supported by long finger bones.',
        'example_sentence': 'The museum\'s ___ fossil showed the creature\'s impressive wingspan.',
        'source': 'Claude'
    },
    'ptosis': {
        'definition': 'The drooping or falling of an upper eyelid; a medical condition where the eyelid partially covers the eye. Ptosis can be congenital or acquired, affecting one or both eyes, and may interfere with vision if severe. Treatment options range from surgery to special eyeglasses depending on the cause and severity.',
        'pronunciation': '/ˈtoʊsɪs/',
        'pronunciation_respelling': 'TOH-sis',
        'etymology': 'From Greek "ptosis," meaning "a falling."',
        'memory_tip': 'Think "toe" + "sis" = like a drooping eyelid falling like a toe.',
        'example_sentence': 'The elderly patient\'s ___ made it difficult to see clearly.',
        'source': 'Claude'
    },
    'ptyxis': {
        'definition': 'The arrangement or folding of leaves in a flower bud before it opens; the pattern of how young leaves are folded or rolled in buds. Ptyxis is an important characteristic in botany for plant identification and classification, as different species have distinctive patterns of leaf arrangement in their developing buds.',
        'pronunciation': '/ˈtɪksɪs/',
        'pronunciation_respelling': 'TIK-sis',
        'etymology': 'From Greek "ptyxis," meaning "a folding."',
        'memory_tip': 'Think "ticks" = like how leaves tick/fold into tight arrangements.',
        'example_sentence': 'The botanist studied the ___ pattern to identify the plant species.',
        'source': 'Claude'
    },
    'public': {
        'definition': 'Open to or concerning the people as a whole; accessible to or shared by all members of a community; not private or secret. Public resources, spaces, and institutions serve the collective good and are funded by or accountable to the community they serve.',
        'pronunciation': '/ˈpʌblɪk/',
        'pronunciation_respelling': 'PUB-lik',
        'etymology': 'From Latin "publicus," from "populus" meaning "people."',
        'memory_tip': 'Think "pub" (where people gather) + "lic" = relating to all people.',
        'example_sentence': 'The ___ library provides free access to books and internet for everyone.',
        'source': 'Claude'
    },
    'publish': {
        'definition': 'To prepare and issue material for public sale or distribution; to make information known publicly; to print and distribute books, articles, or other written works. Publishing involves editorial processes, production, and distribution systems that bring written works to readers.',
        'pronunciation': '/ˈpʌblɪʃ/',
        'pronunciation_respelling': 'PUB-lish',
        'etymology': 'From Latin "publicare," meaning "to make public," from "publicus" (public).',
        'memory_tip': 'Think "public" + "ish" = making something public-ish/available to all.',
        'example_sentence': 'The scientist hopes to ___ her research findings in a prestigious journal.',
        'source': 'Claude'
    },
    'published': {
        'definition': 'Past tense of publish; having been prepared and issued for public distribution; made available to the public through print or digital media. Published works have undergone editorial review and production processes to reach their intended audiences.',
        'pronunciation': '/ˈpʌblɪʃt/',
        'pronunciation_respelling': 'PUB-lisht',
        'etymology': 'Past tense of "publish," from Latin "publicare."',
        'memory_tip': 'Think "publish" + "ed" = already made public in the past.',
        'example_sentence': 'The novel was ___ last year and became a bestseller.',
        'source': 'Claude'
    },
    'publishes': {
        'definition': 'Third person singular present tense of publish; makes material available to the public; issues books, articles, or other works for distribution. This form indicates ongoing or habitual publishing activity by an individual or organization.',
        'pronunciation': '/ˈpʌblɪʃɪz/',
        'pronunciation_respelling': 'PUB-lish-iz',
        'etymology': 'Present tense third person singular of "publish."',
        'memory_tip': 'Think "publish" + "es" = he/she/it publishes regularly.',
        'example_sentence': 'The university press ___ academic books on various subjects.',
        'source': 'Claude'
    },
    'puchero': {
        'definition': 'A traditional Spanish and Latin American stew containing meat, vegetables, and legumes; a hearty one-pot meal common in Spanish-speaking countries. Puchero varies by region but typically includes beef, pork, chicken, chickpeas, and seasonal vegetables, simmered together to create a nutritious and flavorful dish.',
        'pronunciation': '/puˈtʃɛroʊ/',
        'pronunciation_respelling': 'poo-CHER-oh',
        'etymology': 'From Spanish "puchero," meaning "pot" or "stewpot."',
        'memory_tip': 'Think "pouch" + "hero" = a hero-sized pouch of stew ingredients.',
        'example_sentence': 'The family gathered every Sunday to enjoy grandmother\'s traditional ___.',
        'source': 'Claude'
    },
    'puckish': {
        'definition': 'Playfully mischievous; impish or roguish in a lighthearted way; resembling Puck, the mischievous sprite from Shakespeare\'s "A Midsummer Night\'s Dream." Puckish behavior involves harmless pranks, witty remarks, or playful troublemaking that amuses rather than harms.',
        'pronunciation': '/ˈpʌkɪʃ/',
        'pronunciation_respelling': 'PUK-ish',
        'etymology': 'From "Puck" (the mischievous fairy) + suffix "-ish."',
        'memory_tip': 'Think "Puck" (the mischievous fairy) + "ish" = somewhat like Puck, playfully naughty.',
        'example_sentence': 'The child\'s ___ grin suggested he was planning some harmless mischief.',
        'source': 'Claude'
    },
    'pudibund': {
        'definition': 'Bashful; easily embarrassed; characterized by modesty or prudishness. This somewhat archaic term describes individuals who are excessively modest or who blush easily when confronted with situations they find embarrassing or inappropriate.',
        'pronunciation': '/ˈpjuːdɪbʌnd/',
        'pronunciation_respelling': 'PYOO-dih-bund',
        'etymology': 'From Latin "pudibundus," from "pudere" meaning "to be ashamed."',
        'memory_tip': 'Think "prude" + "bound" = bound to be prudish and easily embarrassed.',
        'example_sentence': 'The ___ teenager turned red whenever anyone mentioned dating.',
        'source': 'Claude'
    },
    'puerilely': {
        'definition': 'In a childish or immature manner; with lack of adult sophistication or seriousness; exhibiting behavior characteristic of children when adult behavior is expected. This adverb describes actions or attitudes that seem inappropriately juvenile for the situation or person\'s age.',
        'pronunciation': '/ˈpjʊərəlli/',
        'pronunciation_respelling': 'PYOOR-uh-lee',
        'etymology': 'From Latin "puerilis," meaning "childish," from "puer" (boy) + suffix "-ly."',
        'memory_tip': 'Think "pure" + "ly" = purely childish behavior.',
        'example_sentence': 'The executive ___ refused to participate when his proposal was rejected.',
        'source': 'Claude'
    },
    'puerto': {
        'definition': 'Spanish word meaning "port" or "harbor"; a place where ships dock to load or unload cargo and passengers. In geography and place names, puerto indicates a coastal location with facilities for maritime activities, often forming the foundation for cities and trade centers.',
        'pronunciation': '/ˈpwɛrtoʊ/',
        'pronunciation_respelling': 'PWER-toh',
        'etymology': 'From Latin "portus," meaning "harbor" or "port."',
        'memory_tip': 'Think "port" with Spanish pronunciation = harbor or port in Spanish.',
        'example_sentence': 'The cruise ship docked at the busy ___ to allow passengers to explore the city.',
        'source': 'Claude'
    },
    'pugilist': {
        'definition': 'A professional boxer; someone who fights with their fists as a sport or profession. Pugilists train extensively in technique, strategy, and physical conditioning to compete in organized boxing matches under established rules and regulations.',
        'pronunciation': '/ˈpjuːdʒəlɪst/',
        'pronunciation_respelling': 'PYOO-juh-list',
        'etymology': 'From Latin "pugil," meaning "boxer," from "pugnus" (fist) + suffix "-ist."',
        'memory_tip': 'Think "pugs" (fighting dogs) + "list" = someone on the list of fighters.',
        'example_sentence': 'The experienced ___ won the championship after years of dedicated training.',
        'source': 'Claude'
    },
    'pugilistpugnacious': {
        'definition': '[COMBINED WORD ERROR] This appears to be "pugilist" + "pugnacious" incorrectly joined. Should be separated into two distinct words: "pugilist" (a boxer) and "pugnacious" (combative or aggressive in nature).',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "pugilist" (Latin: boxer) with "pugnacious" (Latin: fighting).',
        'memory_tip': '[ERROR] This should be split into "pugilist" (boxer) and "pugnacious" (aggressive).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "pugilist" and "pugnacious."',
        'source': 'Claude'
    },
    'pugnacious': {
        'definition': 'Eager or quick to argue, quarrel, or fight; combative or aggressive in nature; having a belligerent disposition. Pugnacious individuals tend to seek confrontation and may be difficult to work with due to their argumentative tendencies and readiness to engage in conflict.',
        'pronunciation': '/pʌɡˈneɪʃəs/',
        'pronunciation_respelling': 'pug-NAY-shus',
        'etymology': 'From Latin "pugnax," meaning "fond of fighting," from "pugna" (fight).',
        'memory_tip': 'Think "pug" (fighting dog) + "nacious" = having a fighting nature like a pug.',
        'example_sentence': 'The ___ debater never backed down from an argument, even on minor points.',
        'source': 'Claude'
    },
    'pulchritude': {
        'definition': 'Physical beauty; attractiveness or comeliness, especially of a woman. This formal and somewhat archaic term refers to aesthetic appeal and physical loveliness, though its unusual sound often creates ironic contrast with its meaning of beauty.',
        'pronunciation': '/ˈpʌlkrɪtuːd/',
        'pronunciation_respelling': 'PUL-krih-tood',
        'etymology': 'From Latin "pulchritudo," from "pulcher" meaning "beautiful."',
        'memory_tip': 'Think "pull" + "attitude" = beauty that pulls/attracts with good attitude.',
        'example_sentence': 'The portrait captured the subject\'s remarkable ___ and grace.',
        'source': 'Claude'
    },
    'pulitzer': {
        'definition': 'Relating to the Pulitzer Prizes, prestigious annual awards for achievements in journalism, literature, and musical composition in the United States. Named after Joseph Pulitzer, these awards recognize excellence and have become the gold standard for recognizing outstanding work in their respective fields.',
        'pronunciation': '/ˈpʊlɪtsər/',
        'pronunciation_respelling': 'PUL-it-sur',
        'etymology': 'Named after Joseph Pulitzer, Hungarian-American newspaper publisher.',
        'memory_tip': 'Think "pull" + "itzer" = pulling the best work to receive the top prize.',
        'example_sentence': 'The journalist\'s investigative series earned her a ___ Prize for Public Service.',
        'source': 'Claude'
    },
    'pullets': {
        'definition': 'Young female chickens, typically under one year old and not yet laying eggs regularly; immature hens. Pullets are raised on farms and in backyard coops until they mature into productive laying hens, representing an important stage in poultry development.',
        'pronunciation': '/ˈpʊlɪts/',
        'pronunciation_respelling': 'PUL-its',
        'etymology': 'From Old French "polet," diminutive of "poule" (hen).',
        'memory_tip': 'Think "pull" + "ets" = small chickens you might pull from the coop.',
        'example_sentence': 'The farmer separated the ___ from the mature hens in the chicken coop.',
        'source': 'Claude'
    },
    'pulley': {
        'definition': 'A simple machine consisting of a wheel with a grooved rim around which a rope or chain passes, used to lift heavy objects or change the direction of force. Pulleys reduce the effort required to move loads by distributing weight and providing mechanical advantage.',
        'pronunciation': '/ˈpʊli/',
        'pronunciation_respelling': 'PUL-ee',
        'etymology': 'From Old French "polie," ultimately from Greek "polos" (axis).',
        'memory_tip': 'Think "pull" + "ey" = a device that helps you pull things more easily.',
        'example_sentence': 'The construction workers used a ___ system to lift materials to the upper floors.',
        'source': 'Claude'
    },
    'pulpit': {
        'definition': 'An elevated platform or enclosure in a church from which the preacher delivers sermons; a position of religious or moral authority from which opinions are expressed. The pulpit serves both as a physical structure and a metaphor for religious or moral leadership.',
        'pronunciation': '/ˈpʊlpɪt/',
        'pronunciation_respelling': 'PUL-pit',
        'etymology': 'From Latin "pulpitum," meaning "platform" or "stage."',
        'memory_tip': 'Think "pull" + "pit" = a raised place that pulls attention from the pit/floor.',
        'example_sentence': 'The minister stepped up to the ___ to deliver his Sunday sermon.',
        'source': 'Claude'
    },
    'pulverised': {
        'definition': 'British spelling of pulverized; reduced to fine particles or powder; completely crushed or ground up; thoroughly defeated or destroyed. This term applies both to physical processes of grinding materials and metaphorical destruction of opponents or obstacles.',
        'pronunciation': '/ˈpʌlvəraɪzd/',
        'pronunciation_respelling': 'PUL-vur-yzd',
        'etymology': 'From Latin "pulverizare," from "pulvis" (dust, powder).',
        'memory_tip': 'Think "pulv" (powder) + "erised" (made into) = made into powder.',
        'example_sentence': 'The machine ___ the limestone into fine powder for cement production.',
        'source': 'Claude'
    },
    'pulverized': {
        'definition': 'American spelling of pulverised; reduced to fine particles or powder; completely crushed or ground into dust; thoroughly defeated. The term describes both mechanical processes that break materials into tiny pieces and complete defeats in competition or conflict.',
        'pronunciation': '/ˈpʌlvəraɪzd/',
        'pronunciation_respelling': 'PUL-vur-yzd',
        'etymology': 'From Latin "pulverizare," from "pulvis" (dust, powder).',
        'memory_tip': 'Think "pulv" (powder) + "erized" (made into) = made into powder.',
        'example_sentence': 'The spice grinder ___ the peppercorns into a fine dust.',
        'source': 'Claude'
    }
}

def process_batch_141():
    """Process batch 141 spelling bee words"""
    
    calculator = DifficultyCalculator()
    
    # Read input CSV
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_141_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_141_processed.csv'
    
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
                        'notes': 'Batch 141 processing',
                        'review_status': 'pending',
                        'batch_number': 141
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
            
            print(f"\nBatch 141 processing complete!")
            print(f"Successfully processed {len(processed_words)}/50 words")
            print(f"Output saved to: {output_file}")
            
            # Flag any combined word errors
            combined_errors = [word for word in processed_words if '[COMBINED WORD ERROR]' in word['definition']]
            if combined_errors:
                print(f"\nCombined word errors detected: {len(combined_errors)}")
                for error in combined_errors:
                    print(f"  - {error['word']}")
        
    except Exception as e:
        print(f"Error processing batch 141: {e}")
        return False
    
    return True

if __name__ == "__main__":
    process_batch_141()