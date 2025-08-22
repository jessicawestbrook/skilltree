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
        common = ['prepare', 'prepared', 'present', 'press', 'pressure', 'pretty', 'previous', 'pride']
        if word.lower() in common:
            return 2
            
        # Moderately common (4-6)
        moderate = ['president', 'priest', 'primitive', 'pretend', 'preferred', 'premium']
        if word.lower() in moderate:
            return 5
            
        # Specialized/rare (7-10)
        return 8
    
    def _calculate_morphological_complexity(self, word):
        """Score 1-10: Complexity of word structure"""
        complexity = 1
        
        # Add points for length
        if len(word) > 10:
            complexity += 3
        elif len(word) > 8:
            complexity += 2
        elif len(word) > 6:
            complexity += 1
            
        # Add points for prefixes/suffixes
        prefixes = ['pre', 'pri', 'pres']
        suffixes = ['ous', 'ity', 'ive', 'ment', 'tion', 'ic', 'ary', 'ence', 'ent', 'ed', 'ing']
        
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
        languages = ['latin', 'greek', 'french', 'spanish', 'italian', 'german', 'sanskrit', 'old english']
        language_count = sum(1 for lang in languages if lang in etymology.lower())
        
        if language_count >= 2:
            complexity += 3
        elif language_count == 1:
            complexity += 1
            
        # Ancient origins add complexity
        if any(ancient in etymology.lower() for ancient in ['ancient', 'classical', 'medieval']):
            complexity += 2
            
        return min(10, complexity)

# Comprehensive word data for batch 138
word_data = {
    'preened': {
        'definition': 'Past tense of preen; cleaned and arranged feathers with the beak; showed self-satisfaction.',
        'pronunciation': '/priːnd/',
        'pronunciation_respelling': 'PREEND',
        'etymology': 'From Middle English "prenen," related to "prune" (to trim).',
        'memory_tip': 'Think of birds "pre" (before) + "ened" - preparing their feathers beforehand.',
        'example_sentence': 'The peacock ___ its magnificent tail feathers before displaying them.',
        'source': 'Claude'
    },
    'preferential': {
        'definition': 'Giving or showing preference; favoring one over others.',
        'pronunciation': '/ˌprɛfəˈrɛnʃəl/',
        'pronunciation_respelling': 'pref-uh-REN-shul',
        'etymology': 'From "preference" + suffix "-ial," from Latin "praeferre" (to carry before).',
        'memory_tip': 'Think "prefer" + "ential" = giving preference to someone.',
        'example_sentence': 'The company offered ___ hiring to military veterans.',
        'source': 'Claude'
    },
    'preferred': {
        'definition': 'Past tense of prefer; liked better; chose one thing over another.',
        'pronunciation': '/prɪˈfɜːrd/',
        'pronunciation_respelling': 'prih-FURD',
        'etymology': 'From Latin "praeferre," from "prae" (before) + "ferre" (to carry).',
        'memory_tip': 'Think "pre" (before) + "ferred" (carried) = carried before others.',
        'example_sentence': 'She ___ tea to coffee during her afternoon break.',
        'source': 'Claude'
    },
    'prefers': {
        'definition': 'Third person singular of prefer; likes better; chooses one over another.',
        'pronunciation': '/prɪˈfɜːrz/',
        'pronunciation_respelling': 'prih-FURZ',
        'etymology': 'From Latin "praeferre," present tense third person singular.',
        'memory_tip': 'Simple present tense - "he/she prefers" something over another.',
        'example_sentence': 'The cat ___ sleeping in sunny spots rather than shaded areas.',
        'source': 'Claude'
    },
    'prefix': {
        'definition': 'A word element placed before a root word to modify its meaning.',
        'pronunciation': '/ˈpriːfɪks/',
        'pronunciation_respelling': 'PREE-fiks',
        'etymology': 'From Latin "praefixus," from "prae" (before) + "figere" (to fasten).',
        'memory_tip': 'Think "pre" (before) + "fix" (fasten) = fastened before the root word.',
        'example_sentence': 'The ___ "un-" changes "happy" to "unhappy."',
        'source': 'Claude'
    },
    'prehensile': {
        'definition': 'Capable of grasping or holding, especially by wrapping around.',
        'pronunciation': '/prɪˈhɛnsaɪl/',
        'pronunciation_respelling': 'prih-HEN-syl',
        'etymology': 'From Latin "prehensus," from "prehendere" (to grasp).',
        'memory_tip': 'Think "pre" (before) + "hensile" (seize) = able to seize/grasp.',
        'example_sentence': 'The monkey\'s ___ tail helped it swing from branch to branch.',
        'source': 'Claude'
    },
    'prejudice': {
        'definition': 'Preconceived opinion not based on reason or experience; bias.',
        'pronunciation': '/ˈprɛdʒʊdɪs/',
        'pronunciation_respelling': 'PREJ-uh-dis',
        'etymology': 'From Latin "praejudicium," from "prae" (before) + "judicium" (judgment).',
        'memory_tip': 'Think "pre" (before) + "judice" (judge) = judging before knowing.',
        'example_sentence': 'Education helps combat ___ and promotes understanding between cultures.',
        'source': 'Claude'
    },
    'prelapsarian': {
        'definition': 'Relating to the time before the Fall of Man; innocent, unspoiled.',
        'pronunciation': '/ˌpriːlæpˈsɛəriən/',
        'pronunciation_respelling': 'pree-lap-SAIR-ee-un',
        'etymology': 'From "pre" (before) + Latin "lapsus" (fall) + "-arian."',
        'memory_tip': 'Think "pre" (before) + "lapse" (fall) + "arian" = before the fall.',
        'example_sentence': 'The garden had a ___ beauty, untouched by human corruption.',
        'source': 'Claude'
    },
    'preliminary': {
        'definition': 'Preceding the main part; introductory; preparatory.',
        'pronunciation': '/prɪˈlɪmɪnəri/',
        'pronunciation_respelling': 'prih-LIM-ih-ner-ee',
        'etymology': 'From Latin "prae" (before) + "limen" (threshold).',
        'memory_tip': 'Think "pre" (before) + "liminary" (threshold) = before crossing the threshold.',
        'example_sentence': 'The ___ results suggested the experiment was successful.',
        'source': 'Claude'
    },
    'premium': {
        'definition': 'A sum paid in addition to a basic amount; something of high quality.',
        'pronunciation': '/ˈpriːmiəm/',
        'pronunciation_respelling': 'PREE-mee-um',
        'etymology': 'From Latin "praemium," from "prae" (before) + "emere" (to take).',
        'memory_tip': 'Think "pre" (before) + "mium" (take) = something taken first/best.',
        'example_sentence': 'The insurance ___ increased after the accident claim.',
        'source': 'Claude'
    },
    'premonition': {
        'definition': 'A strong feeling that something is about to happen, especially something bad.',
        'pronunciation': '/ˌprɛməˈnɪʃən/',
        'pronunciation_respelling': 'prem-uh-NISH-un',
        'etymology': 'From Latin "praemonitio," from "prae" (before) + "monere" (to warn).',
        'memory_tip': 'Think "pre" (before) + "monition" (warning) = warning beforehand.',
        'example_sentence': 'She had a ___ that something terrible was going to happen.',
        'source': 'Claude'
    },
    'premonitionprevious': {
        'definition': '[COMBINED WORD ERROR] This appears to be "premonition" + "previous" incorrectly joined. Should be separated into two distinct words.',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "premonition" (Latin: advance warning) with "previous" (Latin: going before).',
        'memory_tip': '[ERROR] This should be split into "premonition" (foreboding) and "previous" (earlier).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "premonition" and "previous."',
        'source': 'Claude'
    },
    'prenuptial': {
        'definition': 'Existing or occurring before marriage.',
        'pronunciation': '/priːˈnʌpʃəl/',
        'pronunciation_respelling': 'pree-NUP-shul',
        'etymology': 'From "pre" (before) + Latin "nuptialis" (relating to marriage).',
        'memory_tip': 'Think "pre" (before) + "nuptial" (marriage) = before marriage.',
        'example_sentence': 'They signed a ___ agreement to protect their individual assets.',
        'source': 'Claude'
    },
    'prepare': {
        'definition': 'To make ready for use or consideration; to get ready.',
        'pronunciation': '/prɪˈpɛər/',
        'pronunciation_respelling': 'prih-PAIR',
        'etymology': 'From Latin "praeparare," from "prae" (before) + "parare" (to make ready).',
        'memory_tip': 'Think "pre" (before) + "pare" (make ready) = make ready beforehand.',
        'example_sentence': 'The chef took an hour to ___ the elaborate five-course meal.',
        'source': 'Claude'
    },
    'prepared': {
        'definition': 'Past tense of prepare; made ready; equipped for something.',
        'pronunciation': '/prɪˈpɛərd/',
        'pronunciation_respelling': 'prih-PAIRD',
        'etymology': 'Past tense of "prepare," from Latin "praeparatus."',
        'memory_tip': 'Think "pre" (before) + "pared" (made ready) = made ready beforehand.',
        'example_sentence': 'The students were well ___ for the challenging examination.',
        'source': 'Claude'
    },
    'prepares': {
        'definition': 'Third person singular of prepare; makes ready.',
        'pronunciation': '/prɪˈpɛərz/',
        'pronunciation_respelling': 'prih-PAIRZ',
        'etymology': 'Present tense third person singular of "prepare."',
        'memory_tip': 'Simple present - "he/she prepares" for something.',
        'example_sentence': 'The teacher carefully ___ each lesson plan in advance.',
        'source': 'Claude'
    },
    'preponderance': {
        'definition': 'The quality of being greater in weight, force, or importance.',
        'pronunciation': '/prɪˈpɒndərəns/',
        'pronunciation_respelling': 'prih-PON-dur-uns',
        'etymology': 'From Latin "praeponderare," from "prae" (before) + "ponderare" (to weigh).',
        'memory_tip': 'Think "pre" (before) + "ponder" (weigh) + "ance" = weighing more.',
        'example_sentence': 'The ___ of evidence supported the defendant\'s innocence.',
        'source': 'Claude'
    },
    'preposterous': {
        'definition': 'Contrary to reason or common sense; utterly absurd or ridiculous.',
        'pronunciation': '/prɪˈpɒstərəs/',
        'pronunciation_respelling': 'prih-POS-tur-us',
        'etymology': 'From Latin "praeposterus," from "prae" (before) + "posterus" (coming after).',
        'memory_tip': 'Think "pre" (before) + "posterous" (after) = backwards/absurd.',
        'example_sentence': 'The claim that the earth is flat is utterly ___.',
        'source': 'Claude'
    },
    'preprandial': {
        'definition': 'Done or taken before dinner or lunch.',
        'pronunciation': '/priːˈprændiəl/',
        'pronunciation_respelling': 'pree-PRAN-dee-ul',
        'etymology': 'From "pre" (before) + Latin "prandium" (meal).',
        'memory_tip': 'Think "pre" (before) + "prandial" (meal) = before eating.',
        'example_sentence': 'They enjoyed a ___ cocktail before the formal dinner.',
        'source': 'Claude'
    },
    'prerogative': {
        'definition': 'A right or privilege exclusive to a particular individual or class.',
        'pronunciation': '/prɪˈrɒɡətɪv/',
        'pronunciation_respelling': 'prih-ROG-uh-tiv',
        'etymology': 'From Latin "praerogativa," from "prae" (before) + "rogare" (to ask).',
        'memory_tip': 'Think "pre" (before) + "rogative" (ask) = right to be asked first.',
        'example_sentence': 'As team captain, choosing the starting lineup was her ___.',
        'source': 'Claude'
    },
    'prescient': {
        'definition': 'Having knowledge of events before they take place; prophetic.',
        'pronunciation': '/ˈprɛʃənt/',
        'pronunciation_respelling': 'PRESH-unt',
        'etymology': 'From Latin "praesciens," from "prae" (before) + "scire" (to know).',
        'memory_tip': 'Think "pre" (before) + "scient" (knowing) = knowing beforehand.',
        'example_sentence': 'The economist\'s ___ warnings about inflation proved accurate.',
        'source': 'Claude'
    },
    'presencesizzle': {
        'definition': '[COMBINED WORD ERROR] This appears to be "presence" + "sizzle" incorrectly joined. Should be separated into two distinct words.',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "presence" (Latin: being present) with "sizzle" (imitative sound).',
        'memory_tip': '[ERROR] This should be split into "presence" (being there) and "sizzle" (hissing sound).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "presence" and "sizzle."',
        'source': 'Claude'
    },
    'present': {
        'definition': 'Existing or occurring now; to give or show; a gift.',
        'pronunciation': '/ˈprɛzənt/',
        'pronunciation_respelling': 'PREZ-unt',
        'etymology': 'From Latin "praesens," from "prae" (before) + "esse" (to be).',
        'memory_tip': 'Think "pre" (before) + "sent" = being before you now.',
        'example_sentence': 'All students must be ___ for the final examination.',
        'source': 'Claude'
    },
    'presentient': {
        'definition': 'Having a feeling or perception beforehand; prescient.',
        'pronunciation': '/prɪˈzɛnʃənt/',
        'pronunciation_respelling': 'prih-ZEN-shunt',
        'etymology': 'From Latin "praesentire," from "prae" (before) + "sentire" (to feel).',
        'memory_tip': 'Think "pre" (before) + "sentient" (feeling) = feeling beforehand.',
        'example_sentence': 'Her ___ anxiety about the storm proved justified.',
        'source': 'Claude'
    },
    'preserving': {
        'definition': 'Present participle of preserve; protecting from harm or decay.',
        'pronunciation': '/prɪˈzɜːrvɪŋ/',
        'pronunciation_respelling': 'prih-ZUR-ving',
        'etymology': 'From Latin "praeservare," from "prae" (before) + "servare" (to keep).',
        'memory_tip': 'Think "pre" (before) + "serving" (keeping) = keeping safe beforehand.',
        'example_sentence': '___ historical artifacts requires careful temperature control.',
        'source': 'Claude'
    },
    'president': {
        'definition': 'The head of a republic or organization; a chief executive.',
        'pronunciation': '/ˈprɛzɪdənt/',
        'pronunciation_respelling': 'PREZ-ih-dent',
        'etymology': 'From Latin "praesidens," from "prae" (before) + "sedere" (to sit).',
        'memory_tip': 'Think "pre" (before) + "sident" (sitting) = sitting before/leading others.',
        'example_sentence': 'The ___ addressed the nation during the crisis.',
        'source': 'Claude'
    },
    'presidio': {
        'definition': 'A Spanish fortress or fortified settlement, especially in the American Southwest.',
        'pronunciation': '/prɪˈsɪdioʊ/',
        'pronunciation_respelling': 'prih-SID-ee-oh',
        'etymology': 'From Spanish "presidio," from Latin "praesidium" (protection, garrison).',
        'memory_tip': 'Think Spanish fortress - "pre" (before) + "sidio" (settlement).',
        'example_sentence': 'The old ___ in San Francisco is now a national park.',
        'source': 'Claude'
    },
    'prespinous': {
        'definition': 'Located in front of the spinous process of a vertebra.',
        'pronunciation': '/priːˈspaɪnəs/',
        'pronunciation_respelling': 'pree-SPY-nus',
        'etymology': 'From "pre" (before) + "spinous" (relating to the spine).',
        'memory_tip': 'Think "pre" (before) + "spinous" (spine) = in front of the spine.',
        'example_sentence': 'The ___ muscles help support the vertebral column.',
        'source': 'Claude'
    },
    'press': {
        'definition': 'To apply force to; to urge strongly; news media.',
        'pronunciation': '/prɛs/',
        'pronunciation_respelling': 'PRES',
        'etymology': 'From Old French "presser," from Latin "pressare" (to press).',
        'memory_tip': 'Short and strong like the pressure it describes.',
        'example_sentence': 'Please ___ the button to start the machine.',
        'source': 'Claude'
    },
    'pressed': {
        'definition': 'Past tense of press; applied force; urged strongly.',
        'pronunciation': '/prɛst/',
        'pronunciation_respelling': 'PREST',
        'etymology': 'Past tense of "press," from Latin "pressus."',
        'memory_tip': 'Think of something that has been squeezed or pushed.',
        'example_sentence': 'She ___ the flowers between the pages of her book.',
        'source': 'Claude'
    },
    'pressure': {
        'definition': 'Continuous force exerted on an object; stress or urgency.',
        'pronunciation': '/ˈprɛʃər/',
        'pronunciation_respelling': 'PRESH-ur',
        'etymology': 'From Latin "pressura," from "pressus" (pressed).',
        'memory_tip': 'Think "press" + "ure" = the state of being pressed.',
        'example_sentence': 'The deep-sea diver felt immense ___ at that depth.',
        'source': 'Claude'
    },
    'prestidigitation': {
        'definition': 'Sleight of hand; magic tricks performed with the hands.',
        'pronunciation': '/ˌprɛstɪˌdɪdʒɪˈteɪʃən/',
        'pronunciation_respelling': 'pres-ti-dij-ih-TAY-shun',
        'etymology': 'From French "prestidigitation," from "preste" (nimble) + Latin "digitus" (finger).',
        'memory_tip': 'Think "presti" (nimble) + "digitation" (finger work) = nimble finger work.',
        'example_sentence': 'The magician\'s ___ amazed the audience with impossible card tricks.',
        'source': 'Claude'
    },
    'prestigious': {
        'definition': 'Having high status or reputation; respected and admired.',
        'pronunciation': '/prɛˈstɪdʒəs/',
        'pronunciation_respelling': 'preh-STIJ-us',
        'etymology': 'From Latin "praestigiosus," from "praestigiae" (delusions, tricks).',
        'memory_tip': 'Think "prestige" + "ous" = full of prestige/honor.',
        'example_sentence': 'Harvard is one of the most ___ universities in the world.',
        'source': 'Claude'
    },
    'presumptuous': {
        'definition': 'Overstepping bounds; taking liberties; arrogantly assuming.',
        'pronunciation': '/prɪˈzʌmptʃuəs/',
        'pronunciation_respelling': 'prih-ZUMP-choo-us',
        'etymology': 'From Latin "praesumptuosus," from "praesumere" (to take beforehand).',
        'memory_tip': 'Think "pre" (before) + "sumptuous" (taking) = taking before given permission.',
        'example_sentence': 'It would be ___ to assume we\'re invited to their private party.',
        'source': 'Claude'
    },
    'pretend': {
        'definition': 'To act as if something is true when it is not; to feign.',
        'pronunciation': '/prɪˈtɛnd/',
        'pronunciation_respelling': 'prih-TEND',
        'etymology': 'From Latin "praetendere," from "prae" (before) + "tendere" (to stretch).',
        'memory_tip': 'Think "pre" (before) + "tend" (stretch) = stretch before reality.',
        'example_sentence': 'Children love to ___ they are superheroes during playtime.',
        'source': 'Claude'
    },
    'pretentious': {
        'definition': 'Attempting to impress by affecting greater importance than is actually possessed.',
        'pronunciation': '/prɪˈtɛnʃəs/',
        'pronunciation_respelling': 'prih-TEN-shus',
        'etymology': 'From French "prétentieux," from Latin "praetentus" (alleged).',
        'memory_tip': 'Think "pretend" + "tious" = acting more important than you are.',
        'example_sentence': 'The restaurant\'s ___ atmosphere made simple food seem overpriced.',
        'source': 'Claude'
    },
    'preternaturally': {
        'definition': 'In a way that is beyond what is normal or natural; extraordinarily.',
        'pronunciation': '/ˌpriːtərˈnætʃərəli/',
        'pronunciation_respelling': 'pree-tur-NACH-ur-ul-lee',
        'etymology': 'From Latin "praeter" (beyond) + "naturalis" (natural) + "-ly."',
        'memory_tip': 'Think "preter" (beyond) + "naturally" = beyond naturally.',
        'example_sentence': 'The child was ___ mature for her age.',
        'source': 'Claude'
    },
    'pretty': {
        'definition': 'Attractive in a delicate way; fairly or moderately.',
        'pronunciation': '/ˈprɪti/',
        'pronunciation_respelling': 'PRIT-ee',
        'etymology': 'From Old English "prættig," from "prætt" (trick, cunning).',
        'memory_tip': 'Common word - sounds pleasant like what it describes.',
        'example_sentence': 'The garden looked ___ with all the spring flowers blooming.',
        'source': 'Claude'
    },
    'prevenient': {
        'definition': 'Preceding and preparing the way for something; anticipatory.',
        'pronunciation': '/prɪˈviːniənt/',
        'pronunciation_respelling': 'prih-VEE-nee-unt',
        'etymology': 'From Latin "praeveniens," from "prae" (before) + "venire" (to come).',
        'memory_tip': 'Think "pre" (before) + "venient" (coming) = coming before.',
        'example_sentence': 'The theologian discussed ___ grace as God\'s preparation of the soul.',
        'source': 'Claude'
    },
    'previous': {
        'definition': 'Existing or occurring before in time or order; former.',
        'pronunciation': '/ˈpriːviəs/',
        'pronunciation_respelling': 'PREE-vee-us',
        'etymology': 'From Latin "praevius," from "prae" (before) + "via" (way).',
        'memory_tip': 'Think "pre" (before) + "vious" (way) = on the way before.',
        'example_sentence': 'Her ___ experience in teaching helped her with the new job.',
        'source': 'Claude'
    },
    'pride': {
        'definition': 'Deep satisfaction derived from achievements; self-respect.',
        'pronunciation': '/praɪd/',
        'pronunciation_respelling': 'PRYD',
        'etymology': 'From Old English "pryde," related to "proud."',
        'memory_tip': 'Short word for a big emotion - "pride" sounds strong.',
        'example_sentence': 'She felt great ___ watching her daughter graduate from college.',
        'source': 'Claude'
    },
    'priest': {
        'definition': 'A religious leader authorized to perform sacred rituals.',
        'pronunciation': '/priːst/',
        'pronunciation_respelling': 'PREEST',
        'etymology': 'From Old English "preost," from Latin "presbyter" (elder).',
        'memory_tip': 'Think "prayed" + "east" = one who prays (religious leader).',
        'example_sentence': 'The ___ performed the wedding ceremony in the old stone church.',
        'source': 'Claude'
    },
    'prima': {
        'definition': 'First in importance; chief; leading (as in prima donna).',
        'pronunciation': '/ˈpriːmə/',
        'pronunciation_respelling': 'PREE-muh',
        'etymology': 'From Latin "prima," feminine of "primus" (first).',
        'memory_tip': 'Think "primary" shortened - "prima" means first/main.',
        'example_sentence': 'The opera\'s ___ ballerina received thunderous applause.',
        'source': 'Claude'
    },
    'primaeval': {
        'definition': 'British spelling of primeval; relating to the earliest ages; ancient.',
        'pronunciation': '/praɪˈmiːvəl/',
        'pronunciation_respelling': 'pry-MEE-vul',
        'etymology': 'From Latin "primaevus," from "primus" (first) + "aevum" (age).',
        'memory_tip': 'Think "prima" (first) + "eval" (age) = first age.',
        'example_sentence': 'The ___ forest had remained unchanged for millions of years.',
        'source': 'Claude'
    },
    'primarily': {
        'definition': 'For the most part; mainly; chiefly.',
        'pronunciation': '/ˈpraɪmərəli/',
        'pronunciation_respelling': 'PRY-mer-ih-lee',
        'etymology': 'From "primary" + suffix "-ly," from Latin "primarius."',
        'memory_tip': 'Think "primary" + "ly" = in a primary/main way.',
        'example_sentence': 'The museum focuses ___ on modern art from the 20th century.',
        'source': 'Claude'
    },
    'primatologist': {
        'definition': 'A scientist who studies primates (apes, monkeys, and related species).',
        'pronunciation': '/ˌpraɪməˈtɒlədʒɪst/',
        'pronunciation_respelling': 'pry-muh-TOL-uh-jist',
        'etymology': 'From "primate" + Greek "logos" (study) + suffix "-ist."',
        'memory_tip': 'Think "primate" + "ologist" = one who studies primates.',
        'example_sentence': 'The famous ___ Jane Goodall studied chimpanzees in Africa.',
        'source': 'Claude'
    },
    'primavera': {
        'definition': 'Spring (Italian/Spanish); a type of pasta sauce with vegetables.',
        'pronunciation': '/ˌpriːməˈvɛrə/',
        'pronunciation_respelling': 'pree-muh-VER-uh',
        'etymology': 'From Italian/Spanish "primavera," from Latin "prima" (first) + "ver" (spring).',
        'memory_tip': 'Think "prima" (first) + "vera" (spring) = first season (spring).',
        'example_sentence': 'The restaurant\'s pasta ___ featured fresh seasonal vegetables.',
        'source': 'Claude'
    },
    'primeval': {
        'definition': 'Relating to the earliest ages in the history of the world; ancient.',
        'pronunciation': '/praɪˈmiːvəl/',
        'pronunciation_respelling': 'pry-MEE-vul',
        'etymology': 'From Latin "primaevus," from "primus" (first) + "aevum" (age).',
        'memory_tip': 'Think "prime" (first) + "eval" (age) = first age.',
        'example_sentence': 'The ___ rainforest contained species unchanged since prehistoric times.',
        'source': 'Claude'
    },
    'primitive': {
        'definition': 'Relating to an early stage of development; basic; rudimentary.',
        'pronunciation': '/ˈprɪmətɪv/',
        'pronunciation_respelling': 'PRIM-ih-tiv',
        'etymology': 'From Latin "primitivus," from "primus" (first).',
        'memory_tip': 'Think "prime" (first) + "itive" = from the first/earliest time.',
        'example_sentence': 'The tribe used ___ tools made from stone and wood.',
        'source': 'Claude'
    },
    'primogeniture': {
        'definition': 'The system of inheritance by the firstborn child, especially the eldest son.',
        'pronunciation': '/ˌpraɪmoʊˈdʒɛnɪtʃər/',
        'pronunciation_respelling': 'pry-moh-JEN-ih-chur',
        'etymology': 'From Latin "primogenitus," from "primus" (first) + "genitus" (born).',
        'memory_tip': 'Think "primo" (first) + "geniture" (birth) = first-born inheritance.',
        'example_sentence': 'Under ___, the eldest son inherited the entire estate.',
        'source': 'Claude'
    }
}

def process_batch_138():
    """Process batch 138 spelling bee words"""
    
    calculator = DifficultyCalculator()
    
    # Read input CSV
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_138_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_138_processed.csv'
    
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
                        'notes': 'Batch 138 processing',
                        'review_status': 'pending',
                        'batch_number': 138
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
            
            print(f"\nBatch 138 processing complete!")
            print(f"Successfully processed {len(processed_words)}/50 words")
            print(f"Output saved to: {output_file}")
            
            # Flag any combined word errors
            combined_errors = [word for word in processed_words if '[COMBINED WORD ERROR]' in word['definition']]
            if combined_errors:
                print(f"\nCombined word errors detected: {len(combined_errors)}")
                for error in combined_errors:
                    print(f"  - {error['word']}")
        
    except Exception as e:
        print(f"Error processing batch 138: {e}")
        return False
    
    return True

if __name__ == "__main__":
    process_batch_138()