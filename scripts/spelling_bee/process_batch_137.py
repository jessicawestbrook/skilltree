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
        common = ['power', 'pour', 'prayer', 'potato', 'praise', 'precious', 'potential']
        if word.lower() in common:
            return 2
            
        # Moderately common (4-6)
        moderate = ['powder', 'pottery', 'prayers', 'predator', 'preamble']
        if word.lower() in moderate:
            return 5
            
        # Specialized/rare (7-10)
        return 8
    
    def _calculate_morphological_complexity(self, word):
        """Score 1-10: Complexity of word structure"""
        complexity = 1
        
        # Add points for length
        if len(word) > 8:
            complexity += 2
        elif len(word) > 6:
            complexity += 1
            
        # Add points for prefixes/suffixes
        prefixes = ['post', 'pre', 'pot', 'pow']
        suffixes = ['ous', 'ity', 'ive', 'ment', 'tion', 'ic', 'ary']
        
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
        languages = ['latin', 'greek', 'french', 'spanish', 'italian', 'german', 'sanskrit', 'hindi']
        language_count = sum(1 for lang in languages if lang in etymology.lower())
        
        if language_count >= 2:
            complexity += 3
        elif language_count == 1:
            complexity += 1
            
        # Ancient origins add complexity
        if any(ancient in etymology.lower() for ancient in ['ancient', 'classical', 'medieval']):
            complexity += 2
            
        return min(10, complexity)

# Comprehensive word data for batch 137
word_data = {
    'postdiction': {
        'definition': 'An explanation or account made after an event has occurred; retroactive prediction.',
        'pronunciation': '/poʊstˈdɪkʃən/',
        'pronunciation_respelling': 'pohst-DIK-shun',
        'etymology': 'From Latin "post" (after) + "dictio" (speaking, saying).',
        'memory_tip': 'Think "post" (after) + "diction" (saying) = saying something after it happens.',
        'example_sentence': 'The analyst\'s ___ explained market trends only after the crash had already occurred.',
        'source': 'Claude'
    },
    'posteriori': {
        'definition': 'Relating to reasoning from observed facts; empirical (as in "a posteriori").',
        'pronunciation': '/ˌpoʊstɪriˈɔːraɪ/',
        'pronunciation_respelling': 'pohst-ih-ree-OR-eye',
        'etymology': 'From Latin "a posteriori" meaning "from what comes after" (from experience).',
        'memory_tip': 'Think "post" (after) + "eriori" = knowledge that comes after experience.',
        'example_sentence': 'The scientist drew ___ conclusions based on experimental data rather than theory.',
        'source': 'Claude'
    },
    'posterity': {
        'definition': 'Future generations of people; descendants.',
        'pronunciation': '/pɒˈsterəti/',
        'pronunciation_respelling': 'pos-TER-ih-tee',
        'etymology': 'From Latin "posteritas," from "posterus" (coming after).',
        'memory_tip': 'Think "post" (after) + "erity" = those who come after us.',
        'example_sentence': 'The environmental policies were designed to protect the planet for ___.',
        'source': 'Claude'
    },
    'posterityposthumous': {
        'definition': '[COMBINED WORD ERROR] This appears to be "posterity" + "posthumous" incorrectly joined. Should be separated into two distinct words.',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "posterity" (Latin: future generations) with "posthumous" (Latin: after death).',
        'memory_tip': '[ERROR] This should be split into "posterity" (future generations) and "posthumous" (after death).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "posterity" and "posthumous."',
        'source': 'Claude'
    },
    'posthumous': {
        'definition': 'Occurring, awarded, or appearing after the death of the originator.',
        'pronunciation': '/ˈpɒstjʊməs/',
        'pronunciation_respelling': 'POST-yuh-mus',
        'etymology': 'From Latin "posthumus," meaning "last, final" (later associated with "post humus" - after burial).',
        'memory_tip': 'Think "post" (after) + "humus" (burial) = after death/burial.',
        'example_sentence': 'The author received a ___ award for the novel published after her death.',
        'source': 'Claude'
    },
    'postpone': {
        'definition': 'To delay or put off to a later time.',
        'pronunciation': '/poʊstˈpoʊn/',
        'pronunciation_respelling': 'pohst-POHN',
        'etymology': 'From Latin "postponere," from "post" (after) + "ponere" (to put).',
        'memory_tip': 'Think "post" (after) + "pone" (put) = put after/later.',
        'example_sentence': 'Due to rain, they decided to ___ the outdoor wedding until next weekend.',
        'source': 'Claude'
    },
    'postponewafer': {
        'definition': '[COMBINED WORD ERROR] This appears to be "postpone" + "wafer" incorrectly joined. Should be separated into two distinct words.',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "postpone" (Latin: put after) with "wafer" (Dutch: thin cake).',
        'memory_tip': '[ERROR] This should be split into "postpone" (delay) and "wafer" (thin cake).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "postpone" and "wafer."',
        'source': 'Claude'
    },
    'postural': {
        'definition': 'Relating to or involving bodily posture.',
        'pronunciation': '/ˈpɒstʃərəl/',
        'pronunciation_respelling': 'POSH-chur-ul',
        'etymology': 'From Latin "postura" (position) + suffix "-al" (relating to).',
        'memory_tip': 'Think "posture" + "al" = relating to body position.',
        'example_sentence': 'The physical therapist focused on ___ exercises to improve spinal alignment.',
        'source': 'Claude'
    },
    'potager': {
        'definition': 'A French-style ornamental vegetable garden.',
        'pronunciation': '/pɒtəˈʒeɪ/',
        'pronunciation_respelling': 'pot-uh-ZHAY',
        'etymology': 'From French "potager," from "potage" (soup), referring to kitchen garden vegetables.',
        'memory_tip': 'Think "pot" + "ager" = garden for pot vegetables (soup ingredients).',
        'example_sentence': 'The château\'s beautiful ___ combined vegetables and flowers in geometric patterns.',
        'source': 'Claude'
    },
    'potassium': {
        'definition': 'A chemical element, an alkali metal essential for life, symbol K.',
        'pronunciation': '/pəˈtæsiəm/',
        'pronunciation_respelling': 'puh-TAS-ee-um',
        'etymology': 'From English "potash" + suffix "-ium," from Dutch "potasch" (pot ash).',
        'memory_tip': 'Think "pot ash" + "ium" = element found in pot ash.',
        'example_sentence': 'Bananas are rich in ___, which helps maintain healthy blood pressure.',
        'source': 'Claude'
    },
    'potato': {
        'definition': 'An edible tuber from a plant native to South America.',
        'pronunciation': '/pəˈteɪtoʊ/',
        'pronunciation_respelling': 'puh-TAY-toh',
        'etymology': 'From Spanish "patata," from Taíno "batata" (sweet potato).',
        'memory_tip': 'Think of the simple, earthy vegetable - "po-ta-to" sounds like its shape.',
        'example_sentence': 'The Irish ___ famine of the 1840s caused massive emigration to America.',
        'source': 'Claude'
    },
    'potatoes': {
        'definition': 'Plural of potato; multiple edible tubers.',
        'pronunciation': '/pəˈteɪtoʊz/',
        'pronunciation_respelling': 'puh-TAY-tohz',
        'etymology': 'Plural form of "potato," from Spanish "patata."',
        'memory_tip': 'Simple plural - just add "es" to potato.',
        'example_sentence': 'The farmer harvested bushels of ___ from the fertile field.',
        'source': 'Claude'
    },
    'potentate': {
        'definition': 'A monarch or ruler with great power; a person of great authority.',
        'pronunciation': '/ˈpoʊtənteɪt/',
        'pronunciation_respelling': 'POH-ten-tayt',
        'etymology': 'From Latin "potentatus," from "potens" (powerful).',
        'memory_tip': 'Think "potent" (powerful) + "ate" = powerful ruler.',
        'example_sentence': 'The oriental ___ ruled his empire with absolute authority.',
        'source': 'Claude'
    },
    'potentatepotoroo': {
        'definition': '[COMBINED WORD ERROR] This appears to be "potentate" + "potoroo" incorrectly joined. Should be separated into two distinct words.',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "potentate" (Latin: powerful ruler) with "potoroo" (Australian: rat-kangaroo).',
        'memory_tip': '[ERROR] This should be split into "potentate" (powerful ruler) and "potoroo" (small kangaroo).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "potentate" and "potoroo."',
        'source': 'Claude'
    },
    'potential': {
        'definition': 'Having or showing the capacity to develop into something in the future.',
        'pronunciation': '/pəˈtenʃəl/',
        'pronunciation_respelling': 'puh-TEN-shul',
        'etymology': 'From Latin "potentialis," from "potentia" (power).',
        'memory_tip': 'Think "potent" (powerful) + "ial" = having the power to become.',
        'example_sentence': 'The young athlete showed great ___ for Olympic competition.',
        'source': 'Claude'
    },
    'pothos': {
        'definition': 'A popular houseplant with heart-shaped leaves, native to tropical regions.',
        'pronunciation': '/ˈpoʊθɒs/',
        'pronunciation_respelling': 'POH-thos',
        'etymology': 'From Greek "pothos" meaning "longing, desire" (the plant seems to reach for light).',
        'memory_tip': 'Think of the plant "reaching" or having "pothos" (longing) for light.',
        'example_sentence': 'The trailing ___ vine cascaded beautifully from the hanging planter.',
        'source': 'Claude'
    },
    'pothospolysyllabic': {
        'definition': '[COMBINED WORD ERROR] This appears to be "pothos" + "polysyllabic" incorrectly joined. Should be separated into two distinct words.',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "pothos" (Greek: longing plant) with "polysyllabic" (Greek: many syllables).',
        'memory_tip': '[ERROR] This should be split into "pothos" (houseplant) and "polysyllabic" (having many syllables).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "pothos" and "polysyllabic."',
        'source': 'Claude'
    },
    'potion': {
        'definition': 'A liquid mixture, especially one that is medicinal, magical, or poisonous.',
        'pronunciation': '/ˈpoʊʃən/',
        'pronunciation_respelling': 'POH-shun',
        'etymology': 'From Latin "potio," from "potare" (to drink).',
        'memory_tip': 'Think "po" (drink) + "tion" = something to drink (often magical).',
        'example_sentence': 'The witch brewed a magical ___ in her bubbling cauldron.',
        'source': 'Claude'
    },
    'potoroo': {
        'definition': 'A small marsupial resembling a rat-kangaroo, native to Australia.',
        'pronunciation': '/ˌpɒtəˈruː/',
        'pronunciation_respelling': 'pot-uh-ROO',
        'etymology': 'From an Australian Aboriginal language, likely Dharug.',
        'memory_tip': 'Think "pot" + "roo" (like kangaroo) = small pot-sized kangaroo.',
        'example_sentence': 'The endangered ___ is one of Australia\'s smallest kangaroo relatives.',
        'source': 'Claude'
    },
    'potpourri': {
        'definition': 'A mixture of dried petals and spices for fragrance; a miscellaneous mixture.',
        'pronunciation': '/ˌpoʊpʊˈriː/',
        'pronunciation_respelling': 'poh-puh-REE',
        'etymology': 'From French "pot-pourri," literally "rotten pot" (referring to fermented mixture).',
        'memory_tip': 'Think "pot" + "pourri" (French for rotten) = mixed pot of dried flowers.',
        'example_sentence': 'The ___ of rose petals and cinnamon filled the room with pleasant fragrance.',
        'source': 'Claude'
    },
    'pottery': {
        'definition': 'Clay articles, especially vessels, shaped and fired; the craft of making such articles.',
        'pronunciation': '/ˈpɒtəri/',
        'pronunciation_respelling': 'POT-ur-ee',
        'etymology': 'From "potter" + suffix "-y," from "pot" (vessel).',
        'memory_tip': 'Think "pot" + "tery" = the art of making pots.',
        'example_sentence': 'Ancient ___ fragments help archaeologists understand past civilizations.',
        'source': 'Claude'
    },
    'potwalloper': {
        'definition': 'Historically, a person qualified to vote by virtue of having a fireplace (able to boil a pot).',
        'pronunciation': '/ˈpɒtwɒləpər/',
        'pronunciation_respelling': 'POT-wol-uh-pur',
        'etymology': 'From "pot" + "wallop" (boil vigorously), referring to one who could boil a pot.',
        'memory_tip': 'Think "pot" + "walloper" (one who wallops/boils) = pot boiler/voter.',
        'example_sentence': 'In old England, a ___ gained voting rights simply by owning a hearth.',
        'source': 'Claude'
    },
    'pouched': {
        'definition': 'Having a pouch or pouches; bag-like.',
        'pronunciation': '/paʊtʃt/',
        'pronunciation_respelling': 'POWTCHT',
        'etymology': 'From "pouch" + suffix "-ed," from Old French "poche" (bag).',
        'memory_tip': 'Think of a kangaroo - "pouched" like having a pouch.',
        'example_sentence': 'Marsupials are ___ mammals that carry their young in abdominal pouches.',
        'source': 'Claude'
    },
    'poudre': {
        'definition': 'French word for powder; used in some English contexts, especially cosmetics.',
        'pronunciation': '/puːdr/',
        'pronunciation_respelling': 'POOD-ruh',
        'etymology': 'From French "poudre," from Latin "pulvis" (dust, powder).',
        'memory_tip': 'Think "powder" but with French pronunciation - "poudre."',
        'example_sentence': 'The vintage cosmetics included rouge and face ___.',
        'source': 'Claude'
    },
    'poultice': {
        'definition': 'A soft, moist mass applied to the skin to relieve soreness and inflammation.',
        'pronunciation': '/ˈpoʊltɪs/',
        'pronunciation_respelling': 'POHL-tis',
        'etymology': 'From Latin "puls" (thick porridge), referring to the paste-like consistency.',
        'memory_tip': 'Think "pulp" + "tice" = pulpy medicine applied to skin.',
        'example_sentence': 'The herbalist prepared a clay ___ to draw out the infection.',
        'source': 'Claude'
    },
    'pour': {
        'definition': 'To flow or cause to flow from a container; to rain heavily.',
        'pronunciation': '/pɔːr/',
        'pronunciation_respelling': 'POR',
        'etymology': 'From Middle English "pouren," of uncertain origin.',
        'memory_tip': 'Simple word - sounds like what it means, liquid flowing.',
        'example_sentence': 'Please ___ the tea slowly to avoid spilling.',
        'source': 'Claude'
    },
    'powder': {
        'definition': 'Fine, dry particles; to sprinkle with powder.',
        'pronunciation': '/ˈpaʊdər/',
        'pronunciation_respelling': 'POW-dur',
        'etymology': 'From Old French "poudre," from Latin "pulvis" (dust).',
        'memory_tip': 'Think "pow" (explosion) + "der" = explosive powder.',
        'example_sentence': 'She applied ___ to her face before the stage performance.',
        'source': 'Claude'
    },
    'power': {
        'definition': 'The ability to do work or cause change; strength, energy, or force.',
        'pronunciation': '/ˈpaʊər/',
        'pronunciation_respelling': 'POW-ur',
        'etymology': 'From Old French "povoir," from Latin "potere" (to be able).',
        'memory_tip': 'Think "POW!" - the sound of power/force.',
        'example_sentence': 'The storm knocked out electrical ___ throughout the city.',
        'source': 'Claude'
    },
    'powers': {
        'definition': 'Plural of power; abilities, authorities, or forces.',
        'pronunciation': '/ˈpaʊərz/',
        'pronunciation_respelling': 'POW-urz',
        'etymology': 'Plural of "power," from Old French "povoir."',
        'memory_tip': 'Think of superpowers - multiple abilities.',
        'example_sentence': 'The constitution clearly defines the ___ of each branch of government.',
        'source': 'Claude'
    },
    'powwow': {
        'definition': 'A Native American gathering; any meeting or conference.',
        'pronunciation': '/ˈpaʊwaʊ/',
        'pronunciation_respelling': 'POW-wow',
        'etymology': 'From Narragansett "powwaw" (medicine man, ceremony).',
        'memory_tip': 'Think "pow" + "wow" = exciting gathering that makes you say "wow!"',
        'example_sentence': 'The annual ___ featured traditional dancing, singing, and storytelling.',
        'source': 'Claude'
    },
    'practise': {
        'definition': 'British spelling of "practice" as a verb; to do repeatedly to improve skill.',
        'pronunciation': '/ˈpræktɪs/',
        'pronunciation_respelling': 'PRAK-tis',
        'etymology': 'From Latin "practicare," from Greek "praktikos" (concerned with action).',
        'memory_tip': 'British spelling ends in "ise" like "exercise" - both are actions.',
        'example_sentence': 'She would ___ piano scales every morning before school.',
        'source': 'Claude'
    },
    'praise': {
        'definition': 'To express approval or admiration; commendation.',
        'pronunciation': '/preɪz/',
        'pronunciation_respelling': 'PRAYZ',
        'etymology': 'From Old French "preisier," from Latin "pretiare" (to value).',
        'memory_tip': 'Think "praise" rhymes with "raise" - you raise someone\'s spirits.',
        'example_sentence': 'The teacher offered sincere ___ for the student\'s hard work.',
        'source': 'Claude'
    },
    'prajna': {
        'definition': 'In Buddhism, transcendent wisdom or insight into the nature of reality.',
        'pronunciation': '/ˈprɑːdʒnə/',
        'pronunciation_respelling': 'PRAH-jnuh',
        'etymology': 'From Sanskrit "prajñā," from "pra" (forth) + "jñā" (to know).',
        'memory_tip': 'Think "pra" (before) + "jna" (know) = knowing that comes before understanding.',
        'example_sentence': 'Buddhist meditation seeks to develop ___ or profound wisdom.',
        'source': 'Claude'
    },
    'pralltriller': {
        'definition': 'In music, a type of ornamental trill that begins on the upper note.',
        'pronunciation': '/ˈprɑːltrɪlər/',
        'pronunciation_respelling': 'PRAHL-tril-ur',
        'etymology': 'From German "pralltriller," from "prall" (bouncing) + "triller" (trill).',
        'memory_tip': 'Think "pral" (bounce) + "triller" = bouncing musical trill.',
        'example_sentence': 'The baroque piece featured several ___ ornaments in the melody.',
        'source': 'Claude'
    },
    'pralltrillerpratique': {
        'definition': '[COMBINED WORD ERROR] This appears to be "pralltriller" + "pratique" incorrectly joined. Should be separated into two distinct words.',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "pralltriller" (German: bouncing trill) with "pratique" (French: practical).',
        'memory_tip': '[ERROR] This should be split into "pralltriller" (musical ornament) and "pratique" (practical).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "pralltriller" and "pratique."',
        'source': 'Claude'
    },
    'prana': {
        'definition': 'In Hindu and yogic tradition, the life force or vital energy.',
        'pronunciation': '/ˈprɑːnə/',
        'pronunciation_respelling': 'PRAH-nuh',
        'etymology': 'From Sanskrit "prāṇa," from "pra" (forth) + "an" (to breathe).',
        'memory_tip': 'Think "pra" (forward) + "ana" (breath) = life breath/energy.',
        'example_sentence': 'Yoga breathing exercises help control and direct ___.',
        'source': 'Claude'
    },
    'pranks': {
        'definition': 'Plural of prank; mischievous tricks played on others.',
        'pronunciation': '/præŋks/',
        'pronunciation_respelling': 'PRANKS',
        'etymology': 'Plural of "prank," from Middle Low German "prank" (display, show off).',
        'memory_tip': 'Think of practical jokes - "pranks" sounds mischievous.',
        'example_sentence': 'April Fools\' Day is famous for harmless ___ and jokes.',
        'source': 'Claude'
    },
    'pratique': {
        'definition': 'Official permission for a ship to use a port after satisfying health regulations.',
        'pronunciation': '/prəˈtiːk/',
        'pronunciation_respelling': 'pruh-TEEK',
        'etymology': 'From French "pratique," from "pratiquer" (to practice, carry out).',
        'memory_tip': 'Think "practice" in French - ships practice/prove their health.',
        'example_sentence': 'The vessel received ___ after the health inspector cleared quarantine.',
        'source': 'Claude'
    },
    'praxis': {
        'definition': 'Practice as distinguished from theory; customary practice or conduct.',
        'pronunciation': '/ˈpræksɪs/',
        'pronunciation_respelling': 'PRAK-sis',
        'etymology': 'From Greek "praxis," from "prassein" (to do, act).',
        'memory_tip': 'Think "practice" shortened - "praxis" is about doing, not just thinking.',
        'example_sentence': 'The philosopher emphasized ___ over abstract theory.',
        'source': 'Claude'
    },
    'prayer': {
        'definition': 'A request for help or expression of thanks to a deity; the practice of praying.',
        'pronunciation': '/preər/',
        'pronunciation_respelling': 'PRAIR',
        'etymology': 'From Old French "preiere," from Latin "precaria" (obtained by prayer).',
        'memory_tip': 'Think "pray" + "er" = one who prays or the act of praying.',
        'example_sentence': 'The evening ___ brought comfort to the worried family.',
        'source': 'Claude'
    },
    'prayers': {
        'definition': 'Plural of prayer; multiple requests or expressions to a deity.',
        'pronunciation': '/preərz/',
        'pronunciation_respelling': 'PRAIRZ',
        'etymology': 'Plural of "prayer," from Old French "preiere."',
        'memory_tip': 'Multiple prayers - "pray" + "ers" = multiple prayer actions.',
        'example_sentence': 'The congregation offered ___ for those affected by the disaster.',
        'source': 'Claude'
    },
    'preamble': {
        'definition': 'An introductory statement; a preliminary explanation.',
        'pronunciation': '/priˈæmbəl/',
        'pronunciation_respelling': 'pree-AM-bul',
        'etymology': 'From Latin "praeambulum," from "prae" (before) + "ambulare" (to walk).',
        'memory_tip': 'Think "pre" (before) + "amble" (walk) = walking before/introduction.',
        'example_sentence': 'The Constitution\'s ___ begins with "We the People of the United States."',
        'source': 'Claude'
    },
    'precariously': {
        'definition': 'In an uncertain or unstable way; dangerously.',
        'pronunciation': '/prɪˈkeəriəsli/',
        'pronunciation_respelling': 'prih-KAIR-ee-us-lee',
        'etymology': 'From Latin "precarius" (obtained by prayer, uncertain) + "-ly."',
        'memory_tip': 'Think "pre" (before) + "care" + "iously" = needing care beforehand.',
        'example_sentence': 'The climber balanced ___ on the narrow ledge.',
        'source': 'Claude'
    },
    'precious': {
        'definition': 'Of great worth or value; much valued by someone.',
        'pronunciation': '/ˈpreʃəs/',
        'pronunciation_respelling': 'PRESH-us',
        'etymology': 'From Old French "precios," from Latin "pretiosus" (valuable).',
        'memory_tip': 'Think "price" + "ous" = having great price/value.',
        'example_sentence': 'The grandmother\'s ring was ___ to the entire family.',
        'source': 'Claude'
    },
    'precursor': {
        'definition': 'A thing that comes before and indicates the approach of another; a forerunner.',
        'pronunciation': '/prɪˈkɜːrsər/',
        'pronunciation_respelling': 'prih-KUR-sur',
        'etymology': 'From Latin "praecursor," from "prae" (before) + "currere" (to run).',
        'memory_tip': 'Think "pre" (before) + "cursor" (runner) = one who runs before.',
        'example_sentence': 'Dark clouds were a ___ to the approaching thunderstorm.',
        'source': 'Claude'
    },
    'predator': {
        'definition': 'An animal that hunts and kills other animals for food.',
        'pronunciation': '/ˈpredətər/',
        'pronunciation_respelling': 'PRED-uh-tur',
        'etymology': 'From Latin "praedator," from "praedari" (to plunder).',
        'memory_tip': 'Think "pred" (prey) + "ator" = one who takes prey.',
        'example_sentence': 'The lion is an apex ___ in the African savanna.',
        'source': 'Claude'
    },
    'predicament': {
        'definition': 'A difficult, unpleasant, or embarrassing situation.',
        'pronunciation': '/prɪˈdɪkəmənt/',
        'pronunciation_respelling': 'prih-DIK-uh-ment',
        'etymology': 'From Latin "praedicamentum," from "praedicare" (to proclaim).',
        'memory_tip': 'Think "predict" + "ament" = a situation you could have predicted would be bad.',
        'example_sentence': 'Finding himself locked out at midnight put him in quite a ___.',
        'source': 'Claude'
    },
    'predictions': {
        'definition': 'Plural of prediction; statements about what will happen in the future.',
        'pronunciation': '/prɪˈdɪkʃənz/',
        'pronunciation_respelling': 'prih-DIK-shunz',
        'etymology': 'Plural of "prediction," from Latin "praedicere" (to foretell).',
        'memory_tip': 'Think "pre" (before) + "dictions" (sayings) = saying things before they happen.',
        'example_sentence': 'The meteorologist\'s weather ___ proved remarkably accurate.',
        'source': 'Claude'
    },
    'predilection': {
        'definition': 'A preference or special liking for something; a bias in favor of something.',
        'pronunciation': '/ˌpriːdɪˈlekʃən/',
        'pronunciation_respelling': 'pree-dih-LEK-shun',
        'etymology': 'From French "prédilection," from Latin "prae" (before) + "diligere" (to choose).',
        'memory_tip': 'Think "pre" (before) + "dilection" (selection) = choosing beforehand/preference.',
        'example_sentence': 'The chef had a ___ for using fresh, local ingredients.',
        'source': 'Claude'
    },
    'preeminent': {
        'definition': 'Surpassing all others; very distinguished in some way.',
        'pronunciation': '/priˈemɪnənt/',
        'pronunciation_respelling': 'pree-EM-ih-nent',
        'etymology': 'From Latin "praeeminens," from "prae" (before) + "eminere" (to stand out).',
        'memory_tip': 'Think "pre" (before) + "eminent" (standing out) = standing out before all others.',
        'example_sentence': 'She was the ___ scholar in medieval European history.',
        'source': 'Claude'
    }
}

def process_batch_137():
    """Process batch 137 spelling bee words"""
    
    calculator = DifficultyCalculator()
    
    # Read input CSV
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_137_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_137_processed.csv'
    
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
                        'notes': 'Batch 137 processing',
                        'review_status': 'pending',
                        'batch_number': 137
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
            
            print(f"\nBatch 137 processing complete!")
            print(f"Successfully processed {len(processed_words)}/50 words")
            print(f"Output saved to: {output_file}")
            
            # Flag any combined word errors
            combined_errors = [word for word in processed_words if '[COMBINED WORD ERROR]' in word['definition']]
            if combined_errors:
                print(f"\nCombined word errors detected: {len(combined_errors)}")
                for error in combined_errors:
                    print(f"  - {error['word']}")
        
    except Exception as e:
        print(f"Error processing batch 137: {e}")
        return False
    
    return True

if __name__ == "__main__":
    process_batch_137()