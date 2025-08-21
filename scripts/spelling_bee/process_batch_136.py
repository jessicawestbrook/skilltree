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
        common = ['poor', 'popular', 'possible', 'post', 'play', 'point', 'pond']
        if word.lower() in common:
            return 2
            
        # Moderately common (4-6)
        moderate = ['portion', 'portal', 'possess', 'poncho', 'porridge', 'porter']
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
        prefixes = ['poly', 'port', 'pos', 'pom']
        suffixes = ['ous', 'ity', 'ive', 'ment', 'tion', 'ic']
        
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
        languages = ['latin', 'greek', 'french', 'spanish', 'italian', 'german', 'portuguese']
        language_count = sum(1 for lang in languages if lang in etymology.lower())
        
        if language_count >= 2:
            complexity += 3
        elif language_count == 1:
            complexity += 1
            
        # Ancient origins add complexity
        if any(ancient in etymology.lower() for ancient in ['ancient', 'classical', 'medieval']):
            complexity += 2
            
        return min(10, complexity)

# Comprehensive word data for batch 136
word_data = {
    'polysyllabic': {
        'definition': 'Having multiple syllables; consisting of more than one syllable.',
        'pronunciation': '/ˌpɒlɪsɪˈlæbɪk/',
        'pronunciation_respelling': 'pol-ee-si-LAB-ik',
        'etymology': 'From Greek "polys" (many) + "syllable" from Greek "syllabē" (taken together).',
        'memory_tip': 'Remember "poly" means many, and this word itself has many syllables - it\'s polysyllabic!',
        'example_sentence': 'The word "___" has four syllables and is therefore classified as a multisyllabic word.',
        'source': 'Claude'
    },
    'pomade': {
        'definition': 'A scented ointment or hair dressing, typically made from fat or oil.',
        'pronunciation': '/pəˈmeɪd/',
        'pronunciation_respelling': 'puh-MAYD',
        'etymology': 'From French "pommade" from Latin "pomum" (apple), originally apple-based ointments.',
        'memory_tip': 'Think of "pom" from pomegranate - both are smooth and glossy like pomade makes hair.',
        'example_sentence': 'The barber applied ___ to style the gentleman\'s hair in the 1920s fashion.',
        'source': 'Claude'
    },
    'pomato': {
        'definition': 'A hybrid plant that produces both potatoes underground and tomatoes above ground.',
        'pronunciation': '/pəˈmeɪtoʊ/',
        'pronunciation_respelling': 'puh-MAY-toh',
        'etymology': 'Blend of "potato" and "tomato," created through grafting techniques.',
        'memory_tip': 'Combine "po" from potato and "mato" from tomato to get pomato.',
        'example_sentence': 'Scientists created the ___ by grafting tomato plants onto potato rootstock.',
        'source': 'Claude'
    },
    'pomegranate': {
        'definition': 'A round red fruit with many seeds inside, native to the Middle East.',
        'pronunciation': '/ˈpɒmɪɡrænɪt/',
        'pronunciation_respelling': 'POM-ih-gran-it',
        'etymology': 'From Old French "pomegrenate," from Latin "pomum granatum" (seeded apple).',
        'memory_tip': 'Think "pome" (apple-like) + "granate" (having grains/seeds) for this seedy fruit.',
        'example_sentence': 'The ruby-red ___ burst open to reveal hundreds of jewel-like seeds.',
        'source': 'Claude'
    },
    'pomeranian': {
        'definition': 'A small breed of dog with a fluffy double coat, originally from the Pomerania region.',
        'pronunciation': '/ˌpɒməˈreɪniən/',
        'pronunciation_respelling': 'pom-uh-RAY-nee-un',
        'etymology': 'Named after Pomerania, a region in northern Europe where the breed was developed.',
        'memory_tip': 'Remember the "pom" in both pomegranate and Pomeranian - small and round!',
        'example_sentence': 'The tiny ___ weighed only three pounds but had the courage of a much larger dog.',
        'source': 'Claude'
    },
    'pomology': {
        'definition': 'The scientific study and cultivation of fruit, especially apples, pears, and stone fruits.',
        'pronunciation': '/pəˈmɒlədʒi/',
        'pronunciation_respelling': 'puh-MOL-uh-jee',
        'etymology': 'From Latin "pomum" (fruit, apple) + Greek "logos" (study).',
        'memory_tip': 'Think "pom" (apple) + "ology" (study of) = study of fruit growing.',
        'example_sentence': 'The university\'s ___ department researches new varieties of disease-resistant apples.',
        'source': 'Claude'
    },
    'pompadour': {
        'definition': 'A hairstyle where the hair is combed high up and back over the forehead.',
        'pronunciation': '/ˈpɒmpədɔːr/',
        'pronunciation_respelling': 'POM-puh-dor',
        'etymology': 'Named after Madame de Pompadour, mistress of King Louis XV of France.',
        'memory_tip': 'Think of Elvis\'s signature hair - "pomp" suggests the pompous height of the style.',
        'example_sentence': 'The 1950s rock star styled his hair in a dramatic ___ that added six inches to his height.',
        'source': 'Claude'
    },
    'pompeii': {
        'definition': 'An ancient Roman city destroyed by Mount Vesuvius in 79 AD, preserved under volcanic ash.',
        'pronunciation': '/pɒmˈpeɪi/',
        'pronunciation_respelling': 'pom-PAY-ee',
        'etymology': 'From Latin "Pompeii," possibly named after Pompey the Great or from Oscan origins.',
        'memory_tip': 'Remember "pomp" suggests grandeur, fitting for this once-grand Roman city.',
        'example_sentence': 'Archaeologists continue to uncover perfectly preserved buildings in ___.',
        'source': 'Claude'
    },
    'pompey': {
        'definition': 'Referring to Pompey the Great, a Roman general and statesman, rival of Julius Caesar.',
        'pronunciation': '/ˈpɒmpi/',
        'pronunciation_respelling': 'POM-pee',
        'etymology': 'From Latin "Pompeius," a Roman family name of uncertain origin.',
        'memory_tip': 'Connect with "pomp" - Pompey was known for his pompous, grand style.',
        'example_sentence': '___ formed the First Triumvirate with Caesar and Crassus in ancient Rome.',
        'source': 'Claude'
    },
    'pomposity': {
        'definition': 'The quality of being pompous; self-important behavior or speech.',
        'pronunciation': '/pɒmˈpɒsəti/',
        'pronunciation_respelling': 'pom-POS-ih-tee',
        'etymology': 'From Latin "pomposus" (stately, magnificent) + suffix "-ity" (quality of).',
        'memory_tip': 'Think "pomp" + "osity" = the quality of being full of pomp and ceremony.',
        'example_sentence': 'His ___ was evident in every grandiose gesture and elaborate speech.',
        'source': 'Claude'
    },
    'pompous': {
        'definition': 'Affectedly grand, solemn, or self-important in a way that seems ridiculous.',
        'pronunciation': '/ˈpɒmpəs/',
        'pronunciation_respelling': 'POM-pus',
        'etymology': 'From Latin "pomposus" meaning stately or magnificent, from "pompa" (procession).',
        'memory_tip': 'Think of excessive "pomp" and circumstance - overdone grandeur.',
        'example_sentence': 'The professor\'s ___ lecture style alienated students with its condescending tone.',
        'source': 'Claude'
    },
    'poncho': {
        'definition': 'A simple cloak made of a rectangle of cloth with a hole in the center for the head.',
        'pronunciation': '/ˈpɒntʃoʊ/',
        'pronunciation_respelling': 'PON-choh',
        'etymology': 'From Spanish "poncho," from Mapuche (Chilean indigenous language) "pontho."',
        'memory_tip': 'Think of a "poncho" as a "punch" through cloth - a hole punched for your head.',
        'example_sentence': 'The hiker wore a waterproof ___ to stay dry during the mountain rainstorm.',
        'source': 'Claude'
    },
    'pond': {
        'definition': 'A small body of still water, often artificially created.',
        'pronunciation': '/pɒnd/',
        'pronunciation_respelling': 'POND',
        'etymology': 'From Middle English "ponde," possibly from "pound" (enclosed area).',
        'memory_tip': 'Short and simple like the small body of water it describes.',
        'example_sentence': 'Lily pads floated on the surface of the garden ___.',
        'source': 'Claude'
    },
    'pongee': {
        'definition': 'A thin, soft fabric made from Chinese silk, typically left in its natural color.',
        'pronunciation': '/pɒnˈdʒiː/',
        'pronunciation_respelling': 'pon-JEE',
        'etymology': 'From Chinese "běnjī" meaning "own loom," referring to home-woven silk.',
        'memory_tip': 'Think "pong" + "gee" - like ping-pong, this silk bounces light softly.',
        'example_sentence': 'The tailor recommended ___ silk for its natural texture and subtle sheen.',
        'source': 'Claude'
    },
    'pontiff': {
        'definition': 'The Pope; a high priest or bishop, especially the head of the Roman Catholic Church.',
        'pronunciation': '/ˈpɒntɪf/',
        'pronunciation_respelling': 'PON-tif',
        'etymology': 'From Latin "pontifex" meaning "bridge-builder," from "pons" (bridge) + "facere" (to make).',
        'memory_tip': 'Think of the Pope as building "pont" (bridge) between Earth and heaven.',
        'example_sentence': 'The ___ addressed the faithful from the balcony of St. Peter\'s Basilica.',
        'source': 'Claude'
    },
    'ponytail': {
        'definition': 'A hairstyle in which hair is pulled back and secured, resembling a horse\'s tail.',
        'pronunciation': '/ˈpoʊniˌteɪl/',
        'pronunciation_respelling': 'POH-nee-tayl',
        'etymology': 'Compound of "pony" + "tail," referring to the resemblance to a pony\'s tail.',
        'memory_tip': 'Visualize a pony\'s tail - hair gathered and hanging down just like the hairstyle.',
        'example_sentence': 'She tied her long hair back in a simple ___ before starting her workout.',
        'source': 'Claude'
    },
    'ponzi': {
        'definition': 'A fraudulent investment scheme where returns to existing investors come from new investors.',
        'pronunciation': '/ˈpɒnzi/',
        'pronunciation_respelling': 'PON-zee',
        'etymology': 'Named after Charles Ponzi, who became notorious for using this technique in 1920.',
        'memory_tip': 'Remember Charles "Ponzi" - his name became synonymous with this type of fraud.',
        'example_sentence': 'Investors lost millions when the ___ scheme collapsed and new money stopped coming in.',
        'source': 'Claude'
    },
    'poor': {
        'definition': 'Having little money or few possessions; lacking in a specified quality.',
        'pronunciation': '/pʊr/',
        'pronunciation_respelling': 'POOR',
        'etymology': 'From Old French "povre," from Latin "pauper" meaning having little.',
        'memory_tip': 'The word looks as simple as the condition it describes - lacking embellishment.',
        'example_sentence': 'Despite being financially ___, the family was rich in love and happiness.',
        'source': 'Claude'
    },
    'popocatepetl': {
        'definition': 'An active volcano in Mexico, also known as "El Popo," located near Mexico City.',
        'pronunciation': '/ˌpoʊpoʊˈkætəˌpetəl/',
        'pronunciation_respelling': 'poh-poh-KAT-uh-pet-ul',
        'etymology': 'From Nahuatl "Popōcatepētl" meaning "smoking mountain."',
        'memory_tip': 'Break it down: "Popo" (smoking) + "catepetl" (mountain) = smoking mountain.',
        'example_sentence': 'The ancient volcano ___ last erupted in 2000, sending ash over Mexico City.',
        'source': 'Claude'
    },
    'popovers': {
        'definition': 'Light, hollow baked goods made from an egg batter, similar to Yorkshire pudding.',
        'pronunciation': '/ˈpoʊpˌoʊvərz/',
        'pronunciation_respelling': 'POHP-oh-vurz',
        'etymology': 'Named because the batter "pops over" the rim of the pan while baking.',
        'memory_tip': 'They literally "pop over" the edge of the muffin tin as they bake and expand.',
        'example_sentence': 'The bakery\'s fresh ___ were light as air and perfect with butter and jam.',
        'source': 'Claude'
    },
    'poppet': {
        'definition': 'A small figure of a person, often used in folk magic; also a term of endearment.',
        'pronunciation': '/ˈpɒpɪt/',
        'pronunciation_respelling': 'POP-it',
        'etymology': 'From Middle English "popet," diminutive of "pope" or puppet.',
        'memory_tip': 'Think of a small "puppet" - both are small figures representing people.',
        'example_sentence': 'The grandmother called her granddaughter "my little ___" with great affection.',
        'source': 'Claude'
    },
    'populace': {
        'definition': 'The general public; the common people of a community or nation.',
        'pronunciation': '/ˈpɒpjʊləs/',
        'pronunciation_respelling': 'POP-yuh-lus',
        'etymology': 'From French "populace," from Italian "popolaccio," from Latin "populus" (people).',
        'memory_tip': 'Think "popular" + "ace" = the people who make things popular.',
        'example_sentence': 'The new law was unpopular among the general ___ despite government support.',
        'source': 'Claude'
    },
    'popular': {
        'definition': 'Liked or admired by many people; of or for the general public.',
        'pronunciation': '/ˈpɒpjʊlər/',
        'pronunciation_respelling': 'POP-yuh-lur',
        'etymology': 'From Latin "popularis," from "populus" meaning people.',
        'memory_tip': 'Think "pop" culture - what\'s popular "pops" up everywhere.',
        'example_sentence': 'The ___ restaurant always had a long line of customers waiting outside.',
        'source': 'Claude'
    },
    'porcelain': {
        'definition': 'A white, translucent ceramic material; fine china made from this material.',
        'pronunciation': '/ˈpɔːrsəlɪn/',
        'pronunciation_respelling': 'POR-suh-lin',
        'etymology': 'From French "porcelaine," from Italian "porcellana" (cowrie shell, due to similarity).',
        'memory_tip': 'Think of "porcupine" - both are smooth and white (like porcupine quills).',
        'example_sentence': 'The antique ___ vase was so delicate it required careful handling.',
        'source': 'Claude'
    },
    'porch': {
        'definition': 'A covered entrance to a building, usually with a roof supported by columns.',
        'pronunciation': '/pɔːrtʃ/',
        'pronunciation_respelling': 'PORCH',
        'etymology': 'From Old French "porche," from Latin "porticus" (colonnade, portico).',
        'memory_tip': 'Think of a "portal" entrance - both provide passage into a building.',
        'example_sentence': 'They sat on the front ___ watching the sunset over the neighborhood.',
        'source': 'Claude'
    },
    'porcine': {
        'definition': 'Of, relating to, or resembling pigs or swine.',
        'pronunciation': '/ˈpɔːrsaɪn/',
        'pronunciation_respelling': 'POR-syn',
        'etymology': 'From Latin "porcinus," from "porcus" meaning pig.',
        'memory_tip': 'Think "pork" + "ine" = relating to pork (pig meat).',
        'example_sentence': 'The veterinarian specialized in ___ diseases affecting commercial pig farms.',
        'source': 'Claude'
    },
    'porcupine': {
        'definition': 'A large rodent covered with sharp, defensive quills or spines.',
        'pronunciation': '/ˈpɔːrkjʊpaɪn/',
        'pronunciation_respelling': 'POR-kyuh-pyn',
        'etymology': 'From Old French "porc-espin," meaning "spiny pig."',
        'memory_tip': 'Think "pork" (pig) + "pine" (needle-like) = spiny pig.',
        'example_sentence': 'The ___ raised its quills as a warning when the hiker approached too closely.',
        'source': 'Claude'
    },
    'porosity': {
        'definition': 'The quality of being porous; having tiny holes that allow liquid or air to pass through.',
        'pronunciation': '/pəˈrɒsəti/',
        'pronunciation_respelling': 'puh-ROS-ih-tee',
        'etymology': 'From Latin "porosus" (porous) + suffix "-ity" (quality of).',
        'memory_tip': 'Think "pore" + "osity" = the quality of having pores.',
        'example_sentence': 'The rock\'s high ___ allowed water to seep through it easily.',
        'source': 'Claude'
    },
    'porridge': {
        'definition': 'A breakfast dish made by boiling oats or other grains in water or milk.',
        'pronunciation': '/ˈpɒrɪdʒ/',
        'pronunciation_respelling': 'POR-ij',
        'etymology': 'Alteration of "pottage," from Old French "potage" (something from a pot).',
        'memory_tip': 'Think of Goldilocks - "por" sounds like "pour" (liquid poured from a pot).',
        'example_sentence': 'Goldilocks found the third bowl of ___ to be just right.',
        'source': 'Claude'
    },
    'portal': {
        'definition': 'A doorway, gate, or entrance, especially a grand or imposing one; an internet site providing access.',
        'pronunciation': '/ˈpɔːrtəl/',
        'pronunciation_respelling': 'POR-tul',
        'etymology': 'From Latin "porta" (gate, door) + suffix "-al."',
        'memory_tip': 'Think "port" (entrance) + "al" = an entrance or gateway.',
        'example_sentence': 'Students logged into the university ___ to access their course materials.',
        'source': 'Claude'
    },
    'portcullis': {
        'definition': 'A heavy grating that can be lowered to block the entrance to a castle.',
        'pronunciation': '/pɔːrtˈkʌlɪs/',
        'pronunciation_respelling': 'port-KUL-is',
        'etymology': 'From Old French "porte coleice" meaning "sliding door."',
        'memory_tip': 'Think "port" (gate) + "cullis" (sliding) = sliding castle gate.',
        'example_sentence': 'The medieval castle\'s ___ dropped suddenly, trapping the invaders in the courtyard.',
        'source': 'Claude'
    },
    'portentous': {
        'definition': 'Being a sign or warning of something momentous or calamitous; pompously self-important.',
        'pronunciation': '/pɔːrˈtentəs/',
        'pronunciation_respelling': 'por-TEN-tus',
        'etymology': 'From Latin "portentosus," from "portentum" (omen, sign).',
        'memory_tip': 'Think "portent" (omen) + "ous" = full of omens or signs.',
        'example_sentence': 'The dark clouds gathering on the horizon seemed ___ of the storm to come.',
        'source': 'Claude'
    },
    'porter': {
        'definition': 'A person employed to carry luggage or goods; a dark beer; a doorkeeper.',
        'pronunciation': '/ˈpɔːrtər/',
        'pronunciation_respelling': 'POR-tur',
        'etymology': 'From Old French "porteur," from Latin "portare" (to carry).',
        'memory_tip': 'Think "port" (carry) + "er" (one who) = one who carries.',
        'example_sentence': 'The hotel ___ helped guests with their luggage and provided local recommendations.',
        'source': 'Claude'
    },
    'portfolio': {
        'definition': 'A collection of investments; a case for carrying documents; a body of work.',
        'pronunciation': '/pɔːrtˈfoʊlioʊ/',
        'pronunciation_respelling': 'port-FOH-lee-oh',
        'etymology': 'From Italian "portafoglio," from "portare" (carry) + "foglio" (sheet).',
        'memory_tip': 'Think "port" (carry) + "folio" (sheets) = case for carrying papers.',
        'example_sentence': 'The artist\'s ___ showcased her best paintings from the past five years.',
        'source': 'Claude'
    },
    'portico': {
        'definition': 'A covered entrance or porch supported by columns, typically at the entrance of a building.',
        'pronunciation': '/ˈpɔːrtɪkoʊ/',
        'pronunciation_respelling': 'POR-ti-koh',
        'etymology': 'From Italian "portico," from Latin "porticus" (colonnade).',
        'memory_tip': 'Think "port" (entrance) + "ico" = entrance with columns.',
        'example_sentence': 'The grand ___ of the museum featured six towering marble columns.',
        'source': 'Claude'
    },
    'portion': {
        'definition': 'A part or share of something; an amount of food served to one person.',
        'pronunciation': '/ˈpɔːrʃən/',
        'pronunciation_respelling': 'POR-shun',
        'etymology': 'From Latin "portio," from "portare" (to carry, bear).',
        'memory_tip': 'Think of "proportion" - both relate to parts of a whole.',
        'example_sentence': 'Each dinner guest received a generous ___ of the delicious roasted turkey.',
        'source': 'Claude'
    },
    'portmanteau': {
        'definition': 'A large suitcase; a word blending sounds and meanings of two other words.',
        'pronunciation': '/pɔːrtˈmæntoʊ/',
        'pronunciation_respelling': 'port-MAN-toh',
        'etymology': 'From French "portemanteau," from "porter" (carry) + "manteau" (cloak).',
        'memory_tip': 'Think "port" (carry) + "manteau" (cloak) = carries clothing.',
        'example_sentence': 'The word "brunch" is a ___ combining "breakfast" and "lunch."',
        'source': 'Claude'
    },
    'portmanteaucoaxation': {
        'definition': '[COMBINED WORD ERROR] This appears to be "portmanteau" + "coaxation" incorrectly joined. Should be separated into two distinct words.',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "portmanteau" (French: carry + cloak) with "coaxation" (Latin: urging together).',
        'memory_tip': '[ERROR] This should be split into "portmanteau" (suitcase/word blend) and "coaxation" (act of coaxing).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "portmanteau" and "coaxation."',
        'source': 'Claude'
    },
    'portrait': {
        'definition': 'A painting, drawing, or photograph of a person, especially of the head and shoulders.',
        'pronunciation': '/ˈpɔːrtrɪt/',
        'pronunciation_respelling': 'POR-trit',
        'etymology': 'From French "portrait," from "portraire" (to portray).',
        'memory_tip': 'Think "portray" + "it" = to portray someone in art.',
        'example_sentence': 'The Renaissance ___ captured not just the subject\'s appearance but their personality.',
        'source': 'Claude'
    },
    'portraitpraise': {
        'definition': '[COMBINED WORD ERROR] This appears to be "portrait" + "praise" incorrectly joined. Should be separated into two distinct words.',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "portrait" (French: to portray) with "praise" (Latin: to value).',
        'memory_tip': '[ERROR] This should be split into "portrait" (painting of person) and "praise" (express approval).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "portrait" and "praise."',
        'source': 'Claude'
    },
    'portugais': {
        'definition': 'Relating to Portugal or the Portuguese language; a Portuguese person.',
        'pronunciation': '/ˌpɔːrtʃʊˈɡeɪz/',
        'pronunciation_respelling': 'por-chu-GAYZ',
        'etymology': 'From French "portugais," meaning "Portuguese."',
        'memory_tip': 'Think "Portugal" + "ais" (French suffix) = of or from Portugal.',
        'example_sentence': 'The ___ sailor navigated the trade routes between Lisbon and Brazil.',
        'source': 'Claude'
    },
    'porwigle': {
        'definition': 'An archaic or dialect term for a tadpole.',
        'pronunciation': '/ˈpɔːrwɪɡəl/',
        'pronunciation_respelling': 'POR-wig-ul',
        'etymology': 'From Middle English, possibly related to "pol" (head) + "wiggle."',
        'memory_tip': 'Think "poor" + "wiggle" = small creature that wiggles poorly (like a tadpole).',
        'example_sentence': 'In the old dialect, children called the pond\'s tadpoles "___."',
        'source': 'Claude'
    },
    'posada': {
        'definition': 'A Spanish inn or lodging house; a Christmas celebration in Mexican tradition.',
        'pronunciation': '/poʊˈsɑːdə/',
        'pronunciation_respelling': 'poh-SAH-dah',
        'etymology': 'From Spanish "posada," from "posar" (to lodge), from Latin "pausare."',
        'memory_tip': 'Think "pose" + "ada" = a place to pause and rest (inn).',
        'example_sentence': 'The travelers found shelter for the night at a small roadside ___.',
        'source': 'Claude'
    },
    'posh': {
        'definition': 'Elegant or luxuriously appointed; typical of or used by the upper class.',
        'pronunciation': '/pɒʃ/',
        'pronunciation_respelling': 'POSH',
        'etymology': 'Origin uncertain; possibly from "port out, starboard home" (preferred cabin sides) or Romani "posh" (half).',
        'memory_tip': 'Think of "polished" shortened - posh things are polished and refined.',
        'example_sentence': 'The ___ hotel featured marble floors, crystal chandeliers, and butler service.',
        'source': 'Claude'
    },
    'posse': {
        'definition': 'A body of men summoned by a sheriff to enforce the law; a group of people with a common purpose.',
        'pronunciation': '/ˈpɒsi/',
        'pronunciation_respelling': 'POS-ee',
        'etymology': 'From Medieval Latin "posse comitatus" (power of the county).',
        'memory_tip': 'Think "possible" shortened - a group with the power to make arrest possible.',
        'example_sentence': 'The sheriff gathered a ___ of volunteers to search for the missing hikers.',
        'source': 'Claude'
    },
    'possess': {
        'definition': 'To own or have; to be controlled or dominated by something.',
        'pronunciation': '/pəˈzes/',
        'pronunciation_respelling': 'puh-ZES',
        'etymology': 'From Latin "possidere," from "potis" (able) + "sedere" (to sit).',
        'memory_tip': 'Think "pos" (position) + "sess" (sit) = to sit in position of ownership.',
        'example_sentence': 'She worked hard to ___ the skills necessary for career advancement.',
        'source': 'Claude'
    },
    'possessive': {
        'definition': 'Showing ownership; demanding exclusive control or attention.',
        'pronunciation': '/pəˈzesɪv/',
        'pronunciation_respelling': 'puh-ZES-iv',
        'etymology': 'From Latin "possessivus," from "possidere" (to possess).',
        'memory_tip': 'Think "possess" + "ive" = tending to possess or own.',
        'example_sentence': 'The ___ pronoun "my" shows ownership in the phrase "my book."',
        'source': 'Claude'
    },
    'possibility': {
        'definition': 'The state or fact of being possible; a thing that may happen or be the case.',
        'pronunciation': '/ˌpɒsəˈbɪləti/',
        'pronunciation_respelling': 'pos-uh-BIL-ih-tee',
        'etymology': 'From Latin "possibilitas," from "possibilis" (possible).',
        'memory_tip': 'Think "possible" + "ity" = the quality of being possible.',
        'example_sentence': 'There was always the ___ that the weather would improve by afternoon.',
        'source': 'Claude'
    },
    'possible': {
        'definition': 'Able to be done or achieved; that may exist or happen.',
        'pronunciation': '/ˈpɒsəbəl/',
        'pronunciation_respelling': 'POS-uh-bul',
        'etymology': 'From Latin "possibilis," from "posse" (to be able).',
        'memory_tip': 'Think "posse" (power) + "ible" = able to be powered/done.',
        'example_sentence': 'It\'s ___ to learn a new language at any age with dedication and practice.',
        'source': 'Claude'
    },
    'post': {
        'definition': 'A position of employment; to send mail; an upright support; to publish online.',
        'pronunciation': '/poʊst/',
        'pronunciation_respelling': 'POHST',
        'etymology': 'From Latin "postis" (doorpost) or "ponere" (to place).',
        'memory_tip': 'Think of a fence post - upright, positioned, supporting something.',
        'example_sentence': 'She applied for the teaching ___ at the local elementary school.',
        'source': 'Claude'
    }
}

def process_batch_136():
    """Process batch 136 spelling bee words"""
    
    calculator = DifficultyCalculator()
    
    # Read input CSV
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_136_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_136_processed.csv'
    
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
                        'notes': 'Batch 136 processing',
                        'review_status': 'pending',
                        'batch_number': 136
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
            
            print(f"\nBatch 136 processing complete!")
            print(f"Successfully processed {len(processed_words)}/50 words")
            print(f"Output saved to: {output_file}")
            
            # Flag any combined word errors
            combined_errors = [word for word in processed_words if '[COMBINED WORD ERROR]' in word['definition']]
            if combined_errors:
                print(f"\nCombined word errors detected: {len(combined_errors)}")
                for error in combined_errors:
                    print(f"  - {error['word']}")
        
    except Exception as e:
        print(f"Error processing batch 136: {e}")
        return False
    
    return True

if __name__ == "__main__":
    process_batch_136()