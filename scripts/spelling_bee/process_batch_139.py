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
        common = ['probably', 'problem', 'process', 'produce', 'private', 'prize', 'profit', 'professor']
        if word.lower() in common:
            return 2
            
        # Moderately common (4-6)
        moderate = ['princess', 'prior', 'privacy', 'privilege', 'production', 'professional', 'profile', 'profound']
        if word.lower() in moderate:
            return 5
            
        # Specialized/rare (7-10)
        return 8
    
    def _calculate_morphological_complexity(self, word):
        """Score 1-10: Complexity of word structure"""
        complexity = 1
        
        # Add points for length
        if len(word) > 12:
            complexity += 4
        elif len(word) > 10:
            complexity += 3
        elif len(word) > 8:
            complexity += 2
        elif len(word) > 6:
            complexity += 1
            
        # Add points for prefixes/suffixes
        prefixes = ['pri', 'pro', 'pre']
        suffixes = ['ous', 'ity', 'ive', 'ment', 'tion', 'ic', 'ary', 'ence', 'ent', 'ed', 'ing', 'ual', 'ate']
        
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
        languages = ['latin', 'greek', 'french', 'spanish', 'italian', 'german', 'sanskrit', 'old english', 'old french']
        language_count = sum(1 for lang in languages if lang in etymology.lower())
        
        if language_count >= 2:
            complexity += 3
        elif language_count == 1:
            complexity += 1
            
        # Ancient origins add complexity
        if any(ancient in etymology.lower() for ancient in ['ancient', 'classical', 'medieval']):
            complexity += 2
            
        return min(10, complexity)

# Comprehensive word data for batch 139
word_data = {
    'primordial': {
        'definition': 'Existing from the beginning of time; primeval; fundamental.',
        'pronunciation': '/praɪˈmɔːrdiəl/',
        'pronunciation_respelling': 'pry-MOR-dee-ul',
        'etymology': 'From Latin "primordialis," from "primordium" (beginning), from "primus" (first) + "ordiri" (to begin).',
        'memory_tip': 'Think "primo" (first) + "ordial" (order) = first order of existence.',
        'example_sentence': 'The ___ soup of the early Earth contained the building blocks of life.',
        'source': 'Claude'
    },
    'princely': {
        'definition': 'Of or worthy of a prince; magnificent; generous.',
        'pronunciation': '/ˈprɪnsli/',
        'pronunciation_respelling': 'PRINS-lee',
        'etymology': 'From "prince" + suffix "-ly," from Latin "princeps" (first, chief).',
        'memory_tip': 'Think "prince" + "ly" = in a manner worthy of a prince.',
        'example_sentence': 'The mansion was furnished in a ___ style with gold and marble.',
        'source': 'Claude'
    },
    'princeps': {
        'definition': 'A first edition of a book; the first or leading citizen (Roman title).',
        'pronunciation': '/ˈprɪnsɛps/',
        'pronunciation_respelling': 'PRIN-seps',
        'etymology': 'From Latin "princeps," from "primus" (first) + "capere" (to take).',
        'memory_tip': 'Think "prince" + "ceps" (takes) = first one who takes leadership.',
        'example_sentence': 'The rare ___ edition of Shakespeare was worth millions at auction.',
        'source': 'Claude'
    },
    'princepsprocurement': {
        'definition': '[COMBINED WORD ERROR] This appears to be "princeps" + "procurement" incorrectly joined. Should be separated into two distinct words.',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "princeps" (Latin: first citizen) with "procurement" (Latin: obtaining).',
        'memory_tip': '[ERROR] This should be split into "princeps" (first edition/citizen) and "procurement" (obtaining).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "princeps" and "procurement."',
        'source': 'Claude'
    },
    'princess': {
        'definition': 'A female member of a royal family; the daughter or wife of a prince.',
        'pronunciation': '/ˈprɪnsɛs/',
        'pronunciation_respelling': 'PRIN-ses',
        'etymology': 'From Old French "princesse," feminine of "prince," from Latin "princeps."',
        'memory_tip': 'Think "prince" + "ess" (female suffix) = female prince.',
        'example_sentence': 'The young ___ waved to the crowds from the castle balcony.',
        'source': 'Claude'
    },
    'principality': {
        'definition': 'A state ruled by a prince; the position or authority of a prince.',
        'pronunciation': '/ˌprɪnsɪˈpæləti/',
        'pronunciation_respelling': 'prin-sih-PAL-ih-tee',
        'etymology': 'From Latin "principalitas," from "principalis" (first in importance).',
        'memory_tip': 'Think "principal" + "ity" = territory where prince is principal ruler.',
        'example_sentence': 'Monaco is a small ___ on the French Mediterranean coast.',
        'source': 'Claude'
    },
    'prion': {
        'definition': 'An infectious protein particle that causes degenerative brain diseases.',
        'pronunciation': '/ˈpriːɒn/',
        'pronunciation_respelling': 'PREE-on',
        'etymology': 'From "proteinaceous infectious particle," coined by Stanley Prusiner.',
        'memory_tip': 'Think "PRI" (protein) + "ON" = protein particle that\'s turned on.',
        'example_sentence': 'Mad cow disease is caused by ___ proteins that fold incorrectly.',
        'source': 'Claude'
    },
    'prior': {
        'definition': 'Existing before in time, order, or importance; a monastic officer.',
        'pronunciation': '/ˈpraɪər/',
        'pronunciation_respelling': 'PRY-ur',
        'etymology': 'From Latin "prior," comparative of "prae" (before).',
        'memory_tip': 'Think "pre" + "ior" = more before/earlier than others.',
        'example_sentence': 'Due to her ___ experience, she was chosen to lead the project.',
        'source': 'Claude'
    },
    'prioress': {
        'definition': 'A woman who is head of a religious house or order.',
        'pronunciation': '/ˈpraɪərɛs/',
        'pronunciation_respelling': 'PRY-ur-es',
        'etymology': 'From "prior" + suffix "-ess" (female), from Latin "prior."',
        'memory_tip': 'Think "prior" + "ess" (female) = female prior/head of convent.',
        'example_sentence': 'The ___ led the nuns in their daily prayers and duties.',
        'source': 'Claude'
    },
    'priority': {
        'definition': 'The fact of being regarded as more important; precedence.',
        'pronunciation': '/praɪˈɒrəti/',
        'pronunciation_respelling': 'pry-OR-ih-tee',
        'etymology': 'From Latin "prioritas," from "prior" (former, earlier).',
        'memory_tip': 'Think "prior" + "ity" = the quality of being prior/first.',
        'example_sentence': 'Student safety is the school\'s top ___.',
        'source': 'Claude'
    },
    'pris': {
        'definition': 'An archaic or informal shortened form of "precise" or prissy.',
        'pronunciation': '/prɪs/',
        'pronunciation_respelling': 'PRIS',
        'etymology': 'Shortened form, possibly from "precise" or related to "prim."',
        'memory_tip': 'Short word that sounds precise and prim.',
        'example_sentence': 'She spoke in a ___ manner that annoyed her classmates.',
        'source': 'Claude'
    },
    'prism': {
        'definition': 'A transparent object that separates white light into colors; a geometric shape.',
        'pronunciation': '/ˈprɪzəm/',
        'pronunciation_respelling': 'PRIZ-um',
        'etymology': 'From Greek "prisma," from "priein" (to saw), referring to its shape.',
        'memory_tip': 'Think of light being "prized" apart into rainbow colors.',
        'example_sentence': 'The glass ___ created a beautiful rainbow on the wall.',
        'source': 'Claude'
    },
    'pristine': {
        'definition': 'In its original condition; unspoiled; clean and fresh.',
        'pronunciation': '/ˈprɪstiːn/',
        'pronunciation_respelling': 'PRIS-teen',
        'etymology': 'From Latin "pristinus," meaning "former, original."',
        'memory_tip': 'Think "pris" (precise) + "tine" = precisely clean/original.',
        'example_sentence': 'The ___ wilderness area showed no signs of human activity.',
        'source': 'Claude'
    },
    'privacy': {
        'definition': 'The state of being private and undisturbed; freedom from intrusion.',
        'pronunciation': '/ˈpraɪvəsi/',
        'pronunciation_respelling': 'PRY-vuh-see',
        'etymology': 'From "private" + suffix "-cy," from Latin "privatus" (set apart).',
        'memory_tip': 'Think "private" + "acy" = the state of being private.',
        'example_sentence': 'The new law protects citizens\' digital ___ rights.',
        'source': 'Claude'
    },
    'private': {
        'definition': 'Belonging to a particular person; not public; confidential.',
        'pronunciation': '/ˈpraɪvət/',
        'pronunciation_respelling': 'PRY-vut',
        'etymology': 'From Latin "privatus," from "privare" (to deprive, set apart).',
        'memory_tip': 'Think "priv" (deprived of public access) + "ate" = set apart.',
        'example_sentence': 'The meeting was held in a ___ room away from the press.',
        'source': 'Claude'
    },
    'privatim': {
        'definition': 'In private; privately (Latin term used in academic contexts).',
        'pronunciation': '/praɪˈveɪtɪm/',
        'pronunciation_respelling': 'pry-VAY-tim',
        'etymology': 'From Latin "privatim," adverb of "privatus" (private).',
        'memory_tip': 'Think "private" + "im" (Latin ending) = in a private manner.',
        'example_sentence': 'The professor discussed the student\'s grades ___.',
        'source': 'Claude'
    },
    'privet': {
        'definition': 'A bushy shrub with small white flowers, commonly used for hedges.',
        'pronunciation': '/ˈprɪvɪt/',
        'pronunciation_respelling': 'PRIV-it',
        'etymology': 'Origin uncertain, possibly from "private" due to its use in creating private hedges.',
        'memory_tip': 'Think "private" hedge - privet creates privacy barriers.',
        'example_sentence': 'The ___ hedge provided a natural border between the properties.',
        'source': 'Claude'
    },
    'privilege': {
        'definition': 'A special right or advantage granted to a particular person or group.',
        'pronunciation': '/ˈprɪvəlɪdʒ/',
        'pronunciation_respelling': 'PRIV-uh-lij',
        'etymology': 'From Latin "privilegium," from "privus" (individual) + "lex" (law).',
        'memory_tip': 'Think "private" + "ledge" = special private advantage.',
        'example_sentence': 'Driving is a ___, not a right, and can be revoked.',
        'source': 'Claude'
    },
    'privy': {
        'definition': 'Sharing knowledge of something secret; an outdoor toilet.',
        'pronunciation': '/ˈprɪvi/',
        'pronunciation_respelling': 'PRIV-ee',
        'etymology': 'From Old French "privé," from Latin "privatus" (private).',
        'memory_tip': 'Think "private" shortened - privy to private information.',
        'example_sentence': 'Only the board members were ___ to the merger negotiations.',
        'source': 'Claude'
    },
    'prize': {
        'definition': 'A reward given for victory or excellence; to value highly.',
        'pronunciation': '/praɪz/',
        'pronunciation_respelling': 'PRYZ',
        'etymology': 'From Old French "pris," from Latin "pretium" (price, value).',
        'memory_tip': 'Think of something so valuable you "price" it highly.',
        'example_sentence': 'She won first ___ in the science fair competition.',
        'source': 'Claude'
    },
    'probably': {
        'definition': 'Most likely; in all likelihood.',
        'pronunciation': '/ˈprɒbəbli/',
        'pronunciation_respelling': 'PROB-uh-blee',
        'etymology': 'From "probable" + suffix "-ly," from Latin "probabilis" (worthy of approval).',
        'memory_tip': 'Think "prob" (problem) + "ably" = able to solve the problem of uncertainty.',
        'example_sentence': 'It will ___ rain tomorrow according to the weather forecast.',
        'source': 'Claude'
    },
    'probation': {
        'definition': 'A system allowing offenders to remain in the community under supervision.',
        'pronunciation': '/proʊˈbeɪʃən/',
        'pronunciation_respelling': 'proh-BAY-shun',
        'etymology': 'From Latin "probatio," from "probare" (to test, prove).',
        'memory_tip': 'Think "probe" + "ation" = testing/proving period.',
        'example_sentence': 'The judge sentenced him to two years of ___ instead of jail time.',
        'source': 'Claude'
    },
    'probative': {
        'definition': 'Having the quality of testing or examining; serving to prove.',
        'pronunciation': '/ˈproʊbətɪv/',
        'pronunciation_respelling': 'PROH-buh-tiv',
        'etymology': 'From Latin "probativus," from "probare" (to prove).',
        'memory_tip': 'Think "probe" + "ative" = tending to probe/test truth.',
        'example_sentence': 'The DNA evidence was highly ___ in establishing the defendant\'s guilt.',
        'source': 'Claude'
    },
    'problem': {
        'definition': 'A matter or situation regarded as unwelcome or harmful; a puzzle.',
        'pronunciation': '/ˈprɒbləm/',
        'pronunciation_respelling': 'PROB-lum',
        'etymology': 'From Greek "problema," from "proballein" (to throw forward).',
        'memory_tip': 'Think "prob" (probe) + "lem" = something thrown forward to probe/solve.',
        'example_sentence': 'The math ___ took her an hour to solve completely.',
        'source': 'Claude'
    },
    'process': {
        'definition': 'A series of actions to achieve a result; to perform operations on.',
        'pronunciation': '/ˈproʊsɛs/',
        'pronunciation_respelling': 'PROH-ses',
        'etymology': 'From Latin "processus," from "procedere" (to go forward).',
        'memory_tip': 'Think "pro" (forward) + "cess" (go) = going forward through steps.',
        'example_sentence': 'The manufacturing ___ takes exactly six hours to complete.',
        'source': 'Claude'
    },
    'proclamation': {
        'definition': 'A public or official announcement; a formal declaration.',
        'pronunciation': '/ˌprɒkləˈmeɪʃən/',
        'pronunciation_respelling': 'prok-luh-MAY-shun',
        'etymology': 'From Latin "proclamatio," from "proclamare" (to shout out).',
        'memory_tip': 'Think "pro" (forth) + "clam" (shout) + "ation" = shouting forth.',
        'example_sentence': 'The mayor issued a ___ declaring a local state of emergency.',
        'source': 'Claude'
    },
    'procrastinate': {
        'definition': 'To delay or postpone action; to put off doing something.',
        'pronunciation': '/proʊˈkræstəˌneɪt/',
        'pronunciation_respelling': 'proh-KRAS-tuh-nayt',
        'etymology': 'From Latin "procrastinatus," from "pro" (forward) + "cras" (tomorrow).',
        'memory_tip': 'Think "pro" (for) + "cras" (tomorrow) = putting off until tomorrow.',
        'example_sentence': 'Students often ___ on big projects until the last minute.',
        'source': 'Claude'
    },
    'procrustean': {
        'definition': 'Enforcing conformity without regard to natural variation; rigidly standardized.',
        'pronunciation': '/proʊˈkrʌstiən/',
        'pronunciation_respelling': 'proh-KRUS-tee-un',
        'etymology': 'From Procrustes, a Greek mythological figure who forced travelers to fit his bed.',
        'memory_tip': 'Think of Procrustes forcing everyone to fit the same bed size.',
        'example_sentence': 'The ___ educational policy ignored individual learning differences.',
        'source': 'Claude'
    },
    'proctors': {
        'definition': 'Plural of proctor; supervisors of examinations or university officials.',
        'pronunciation': '/ˈprɒktərz/',
        'pronunciation_respelling': 'PROK-turz',
        'etymology': 'From Latin "procurator," from "procurare" (to take care of).',
        'memory_tip': 'Think "proc" (process) + "tors" = those who process/supervise exams.',
        'example_sentence': 'The ___ walked around the room during the final examination.',
        'source': 'Claude'
    },
    'procurement': {
        'definition': 'The action of obtaining or procuring something; acquisition.',
        'pronunciation': '/prəˈkjʊərmənt/',
        'pronunciation_respelling': 'pruh-KYOOR-ment',
        'etymology': 'From "procure" + suffix "-ment," from Latin "procurare" (to take care of).',
        'memory_tip': 'Think "pro" (for) + "cure" (obtain) + "ment" = obtaining for a purpose.',
        'example_sentence': 'The military\'s ___ of new equipment took several months.',
        'source': 'Claude'
    },
    'prodigious': {
        'definition': 'Remarkably or impressively great in extent, size, or intensity.',
        'pronunciation': '/prəˈdɪdʒəs/',
        'pronunciation_respelling': 'pruh-DIJ-us',
        'etymology': 'From Latin "prodigiosus," from "prodigium" (omen, monster).',
        'memory_tip': 'Think "prod" (poke) + "igious" = so big it pokes out/amazing.',
        'example_sentence': 'Mozart showed ___ musical talent from a very young age.',
        'source': 'Claude'
    },
    'prodigiousprofligacy': {
        'definition': '[COMBINED WORD ERROR] This appears to be "prodigious" + "profligacy" incorrectly joined. Should be separated into two distinct words.',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "prodigious" (Latin: wonderful) with "profligacy" (Latin: shameless).',
        'memory_tip': '[ERROR] This should be split into "prodigious" (remarkably great) and "profligacy" (wasteful excess).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "prodigious" and "profligacy."',
        'source': 'Claude'
    },
    'produce': {
        'definition': 'To make or manufacture; to bring forth; fresh fruits and vegetables.',
        'pronunciation': '/prəˈduːs/',
        'pronunciation_respelling': 'pruh-DOOS',
        'etymology': 'From Latin "producere," from "pro" (forth) + "ducere" (to lead).',
        'memory_tip': 'Think "pro" (forth) + "duce" (lead) = leading forth/creating.',
        'example_sentence': 'The factory can ___ a thousand cars per day.',
        'source': 'Claude'
    },
    'produced': {
        'definition': 'Past tense of produce; made, manufactured, or brought forth.',
        'pronunciation': '/prəˈduːst/',
        'pronunciation_respelling': 'pruh-DOOST',
        'etymology': 'Past tense of "produce," from Latin "productus."',
        'memory_tip': 'Think "pro" (forth) + "duced" (led) = was led forth/created.',
        'example_sentence': 'The company ___ its best quarterly results in five years.',
        'source': 'Claude'
    },
    'production': {
        'definition': 'The action of making or manufacturing; a play, movie, or show.',
        'pronunciation': '/prəˈdʌkʃən/',
        'pronunciation_respelling': 'pruh-DUK-shun',
        'etymology': 'From Latin "productio," from "producere" (to bring forth).',
        'memory_tip': 'Think "produce" + "tion" = the action of producing.',
        'example_sentence': 'The Broadway ___ received rave reviews from critics.',
        'source': 'Claude'
    },
    'professes': {
        'definition': 'Third person singular of profess; claims, declares, or affirms.',
        'pronunciation': '/prəˈfɛsɪz/',
        'pronunciation_respelling': 'pruh-FES-iz',
        'etymology': 'From Latin "profiteri," from "pro" (forth) + "fateri" (to acknowledge).',
        'memory_tip': 'Think "pro" (forth) + "fesses" (speaks) = speaks forth/declares.',
        'example_sentence': 'She ___ to be an expert in ancient history.',
        'source': 'Claude'
    },
    'professing': {
        'definition': 'Present participle of profess; claiming or declaring openly.',
        'pronunciation': '/prəˈfɛsɪŋ/',
        'pronunciation_respelling': 'pruh-FES-ing',
        'etymology': 'Present participle of "profess," from Latin "profiteri."',
        'memory_tip': 'Think "pro" (forth) + "fessing" (speaking) = speaking forth.',
        'example_sentence': 'While ___ innocence, his actions suggested otherwise.',
        'source': 'Claude'
    },
    'professional': {
        'definition': 'Relating to or connected with a profession; skilled and competent.',
        'pronunciation': '/prəˈfɛʃənəl/',
        'pronunciation_respelling': 'pruh-FESH-un-ul',
        'etymology': 'From "profession" + suffix "-al," from Latin "professio."',
        'memory_tip': 'Think "profess" + "ional" = relating to what one professes to do.',
        'example_sentence': 'The carpenter\'s ___ work exceeded all expectations.',
        'source': 'Claude'
    },
    'professionally': {
        'definition': 'In a professional manner; as a profession rather than hobby.',
        'pronunciation': '/prəˈfɛʃənəli/',
        'pronunciation_respelling': 'pruh-FESH-un-ul-lee',
        'etymology': 'From "professional" + suffix "-ly."',
        'memory_tip': 'Think "professional" + "ly" = in a professional way.',
        'example_sentence': 'She dances ___ with the National Ballet Company.',
        'source': 'Claude'
    },
    'professor': {
        'definition': 'A teacher of the highest rank in a college or university.',
        'pronunciation': '/prəˈfɛsər/',
        'pronunciation_respelling': 'pruh-FES-ur',
        'etymology': 'From Latin "professor," from "profiteri" (to declare publicly).',
        'memory_tip': 'Think "profess" + "or" = one who professes knowledge.',
        'example_sentence': 'The ___ published groundbreaking research in quantum physics.',
        'source': 'Claude'
    },
    'proffered': {
        'definition': 'Past tense of proffer; offered for acceptance; presented.',
        'pronunciation': '/ˈprɒfərd/',
        'pronunciation_respelling': 'PROF-urd',
        'etymology': 'From Old French "proffrir," from "pro" (forth) + "offrir" (to offer).',
        'memory_tip': 'Think "pro" (forth) + "offered" = offered forth/presented.',
        'example_sentence': 'He ___ his assistance with the difficult project.',
        'source': 'Claude'
    },
    'profile': {
        'definition': 'An outline of something in side view; a brief description of characteristics.',
        'pronunciation': '/ˈproʊfaɪl/',
        'pronunciation_respelling': 'PROH-fyl',
        'etymology': 'From Italian "profilo," from "pro" (forth) + "filare" (to draw a line).',
        'memory_tip': 'Think "pro" (forth) + "file" = drawing a line forth (outline).',
        'example_sentence': 'The detective created a psychological ___ of the suspect.',
        'source': 'Claude'
    },
    'profit': {
        'definition': 'Financial gain; benefit or advantage derived from something.',
        'pronunciation': '/ˈprɒfɪt/',
        'pronunciation_respelling': 'PROF-it',
        'etymology': 'From Latin "profectus," from "proficere" (to make progress).',
        'memory_tip': 'Think "pro" (forward) + "fit" = fitting forward/gaining.',
        'example_sentence': 'The company reported a significant ___ increase this quarter.',
        'source': 'Claude'
    },
    'profiteer': {
        'definition': 'Someone who profits from a situation, especially unethically.',
        'pronunciation': '/ˌprɒfɪˈtɪər/',
        'pronunciation_respelling': 'prof-ih-TEER',
        'etymology': 'From "profit" + suffix "-eer" (one who).',
        'memory_tip': 'Think "profit" + "eer" = one who profits (often unethically).',
        'example_sentence': 'War profiteers made fortunes selling overpriced supplies.',
        'source': 'Claude'
    },
    'profiterole': {
        'definition': 'A small round pastry filled with cream and topped with chocolate sauce.',
        'pronunciation': '/prəˈfɪtəroʊl/',
        'pronunciation_respelling': 'pruh-FIT-uh-rohl',
        'etymology': 'From French "profiterole," diminutive of "profit" (advantage, benefit).',
        'memory_tip': 'Think French pastry that provides "profit" (pleasure) in small "role" (round).',
        'example_sentence': 'For dessert, she ordered three chocolate ___ with vanilla cream.',
        'source': 'Claude'
    },
    'profligacy': {
        'definition': 'Reckless extravagance or wastefulness; licentious behavior.',
        'pronunciation': '/ˈprɒflɪɡəsi/',
        'pronunciation_respelling': 'PROF-lih-guh-see',
        'etymology': 'From Latin "profligatus," from "profligare" (to strike down, ruin).',
        'memory_tip': 'Think "prof" (forward) + "ligacy" (looseness) = forward into loose/wasteful behavior.',
        'example_sentence': 'The king\'s financial ___ led to the kingdom\'s bankruptcy.',
        'source': 'Claude'
    },
    'profound': {
        'definition': 'Very great or intense; showing deep insight or understanding.',
        'pronunciation': '/prəˈfaʊnd/',
        'pronunciation_respelling': 'pruh-FOWND',
        'etymology': 'From Latin "profundus," from "pro" (forth) + "fundus" (bottom).',
        'memory_tip': 'Think "pro" (forth) + "found" (deep) = deeply found/discovered.',
        'example_sentence': 'The philosopher\'s ___ insights changed how people viewed ethics.',
        'source': 'Claude'
    },
    'profundity': {
        'definition': 'Deep insight or understanding; intellectual depth.',
        'pronunciation': '/prəˈfʌndəti/',
        'pronunciation_respelling': 'pruh-FUN-dih-tee',
        'etymology': 'From Latin "profunditas," from "profundus" (deep).',
        'memory_tip': 'Think "profound" + "ity" = the quality of being profound.',
        'example_sentence': 'The ___ of her observations impressed the academic committee.',
        'source': 'Claude'
    },
    'profusion': {
        'definition': 'An abundance or large quantity of something.',
        'pronunciation': '/prəˈfjuːʒən/',
        'pronunciation_respelling': 'pruh-FYOO-zhun',
        'etymology': 'From Latin "profusio," from "profundere" (to pour forth).',
        'memory_tip': 'Think "pro" (forth) + "fusion" (pouring) = pouring forth abundantly.',
        'example_sentence': 'The garden displayed a ___ of colorful spring flowers.',
        'source': 'Claude'
    },
    'prognosticate': {
        'definition': 'To foretell or predict future events; to prophesy.',
        'pronunciation': '/prɒɡˈnɒstɪkeɪt/',
        'pronunciation_respelling': 'prog-NOS-tih-kayt',
        'etymology': 'From Latin "prognosticare," from Greek "prognostikos" (knowing beforehand).',
        'memory_tip': 'Think "prog" (before) + "nostic" (know) + "ate" = to know beforehand.',
        'example_sentence': 'Ancient oracles claimed they could ___ the fate of kingdoms.',
        'source': 'Claude'
    }
}

def process_batch_139():
    """Process batch 139 spelling bee words"""
    
    calculator = DifficultyCalculator()
    
    # Read input CSV
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_139_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_139_processed.csv'
    
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
                        'notes': 'Batch 139 processing',
                        'review_status': 'pending',
                        'batch_number': 139
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
            
            print(f"\nBatch 139 processing complete!")
            print(f"Successfully processed {len(processed_words)}/50 words")
            print(f"Output saved to: {output_file}")
            
            # Flag any combined word errors
            combined_errors = [word for word in processed_words if '[COMBINED WORD ERROR]' in word['definition']]
            if combined_errors:
                print(f"\nCombined word errors detected: {len(combined_errors)}")
                for error in combined_errors:
                    print(f"  - {error['word']}")
        
    except Exception as e:
        print(f"Error processing batch 139: {e}")
        return False
    
    return True

if __name__ == "__main__":
    process_batch_139()