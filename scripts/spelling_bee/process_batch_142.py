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
        
        # Silent letters and irregular patterns
        if re.search(r'[bt](?![aeiou])|[kl](?=n)|[w](?=r)|[h](?=[^aeiou])|[p](?=s)|[pt](?=[^aeiou])|[gh]|[qu]', word.lower()):
            irregular_patterns += 1
            
        # Double letters not in pronunciation
        if re.search(r'(.)\1', word) and 'double' not in pronunciation.lower():
            irregular_patterns += 1
            
        # French/foreign patterns
        if any(pattern in word.lower() for pattern in ['ée', 'ieu', 'eau', 'oux']):
            irregular_patterns += 1
            
        # Score inversely related to irregular patterns
        return min(10, max(1, 8 - irregular_patterns * 2))
    
    def _calculate_word_frequency(self, word):
        """Score 1-10: How common the word is (lower = more common)"""
        # Common words (1-3)
        common = ['purple', 'purpose', 'purposes', 'purse', 'purchase', 'puzzle', 'puzzles', 'public', 'quality', 'quack']
        if word.lower() in common:
            return 2
            
        # Moderately common (4-6)
        moderate = ['punctuation', 'pyramid', 'python', 'pursuit', 'putty', 'qualifying', 'qualitative']
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
        prefixes = ['pul', 'pum', 'pun', 'pup', 'pur', 'pus', 'put', 'puz', 'pyl', 'pyr', 'pyt', 'pyx', 'qu', 'qua']
        suffixes = ['ous', 'ity', 'ive', 'ment', 'tion', 'ic', 'ary', 'ence', 'ent', 'ed', 'ing', 'ly', 'ism', 'ist', 'er', 'eer']
        
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
        languages = ['latin', 'greek', 'french', 'spanish', 'italian', 'german', 'sanskrit', 'old english', 'arabic', 'hebrew', 'old french']
        language_count = sum(1 for lang in languages if lang in etymology.lower())
        
        if language_count >= 2:
            complexity += 3
        elif language_count == 1:
            complexity += 1
            
        # Ancient origins add complexity
        if any(ancient in etymology.lower() for ancient in ['ancient', 'classical', 'medieval']):
            complexity += 2
            
        return min(10, complexity)

# Comprehensive word data for batch 142
word_data = {
    'pulvillus': {
        'definition': 'A small, cushion-like pad or structure; in biology, specifically referring to the adhesive pad found on the feet of many insects that allows them to walk on smooth surfaces. The pulvillus contains tiny hairs and sticky secretions that provide grip, enabling insects like flies to walk upside down on ceilings and glass.',
        'pronunciation': '/pʌlˈvɪləs/',
        'pronunciation_respelling': 'pul-VIL-us',
        'etymology': 'From Latin "pulvillus," diminutive of "pulvinus" meaning "cushion" or "pillow."',
        'memory_tip': 'Think "pulv" (soft) + "illus" (small) = small soft cushion-like pad.',
        'example_sentence': 'The fly\'s ___ allowed it to grip the smooth glass surface effortlessly.',
        'source': 'Claude'
    },
    'pumice': {
        'definition': 'A light, porous volcanic rock formed when gas-filled lava is ejected from a volcano and cools rapidly; used as an abrasive for polishing and in lightweight concrete. Pumice is so light it can float on water, making it unique among rocks. It\'s commonly used in personal care products and construction materials.',
        'pronunciation': '/ˈpʌmɪs/',
        'pronunciation_respelling': 'PUM-is',
        'etymology': 'From Latin "pumex," meaning "foam" or "froth," related to its light, airy structure.',
        'memory_tip': 'Think "pump" + "ice" = rock so light it pumps up like ice on water.',
        'example_sentence': 'The spa used ___ stones to gently exfoliate rough skin on feet.',
        'source': 'Claude'
    },
    'puncheon': {
        'definition': 'A large cask or barrel for holding liquids, typically wine or beer; a short, upright timber post used in construction; a tool for perforating or stamping. In winemaking, puncheons are smaller than standard barrels and are prized for aging wine with subtle wood flavors.',
        'pronunciation': '/ˈpʌntʃən/',
        'pronunciation_respelling': 'PUN-chun',
        'etymology': 'From Old French "ponçon," meaning "awl" or "pointed tool," later applied to barrels.',
        'memory_tip': 'Think "punch" + "eon" = a big container that could take a punch.',
        'example_sentence': 'The vintner aged the premium wine in French oak ___ for eighteen months.',
        'source': 'Claude'
    },
    'punctually': {
        'definition': 'In a punctual manner; exactly on time; with precise attention to scheduled times or deadlines. Being punctual demonstrates respect for others\' time and is considered an important social and professional courtesy in most cultures.',
        'pronunciation': '/ˈpʌŋktʃuəli/',
        'pronunciation_respelling': 'PUNK-choo-ul-lee',
        'etymology': 'From "punctual" + suffix "-ly," from Latin "punctualis" meaning "of a point in time."',
        'memory_tip': 'Think "punctual" + "ly" = in a timely, point-precise manner.',
        'example_sentence': 'The train arrived ___ at 3:15 PM, just as the schedule promised.',
        'source': 'Claude'
    },
    'punctuation': {
        'definition': 'The system of marks used in writing to separate sentences and their elements and to clarify meaning; the practice of inserting standardized marks in written text. Punctuation includes periods, commas, question marks, and other symbols that guide readers through the structure and meaning of written language.',
        'pronunciation': '/ˌpʌŋktʃuˈeɪʃən/',
        'pronunciation_respelling': 'punk-choo-AY-shun',
        'etymology': 'From Latin "punctuationem," from "punctuare" meaning "to prick" or "to mark with points."',
        'memory_tip': 'Think "punctual" + "ation" = marking precise points in writing.',
        'example_sentence': 'Proper ___ makes writing clearer and easier to understand.',
        'source': 'Claude'
    },
    'pungent': {
        'definition': 'Having a sharply strong taste or smell; penetrating and intense in sensory impact; having a sharp or pointed quality in argument or wit. Pungent describes sensations that are immediate and forceful, often referring to spices, odors, or sharp commentary.',
        'pronunciation': '/ˈpʌndʒənt/',
        'pronunciation_respelling': 'PUN-junt',
        'etymology': 'From Latin "pungens," from "pungere" meaning "to prick" or "to sting."',
        'memory_tip': 'Think "pun" + "gent" (gentle) = ironically not gentle, but sharp and strong.',
        'example_sentence': 'The ___ aroma of garlic filled the kitchen during cooking.',
        'source': 'Claude'
    },
    'punily': {
        'definition': 'In a puny manner; weakly, feebly, or inadequately; with insufficient strength or size. This adverb describes actions or conditions characterized by lack of vigor, power, or substantial presence.',
        'pronunciation': '/ˈpjuːnəli/',
        'pronunciation_respelling': 'PYOO-nuh-lee',
        'etymology': 'From "puny" + suffix "-ly," from Old French "puisne" meaning "younger" or "inferior."',
        'memory_tip': 'Think "puny" + "ly" = in a small, weak manner.',
        'example_sentence': 'The seedling grew ___ in the shaded corner of the garden.',
        'source': 'Claude'
    },
    'puniness': {
        'definition': 'The quality or state of being puny; weakness, frailty, or inadequate size; lack of strength or substance. Puniness describes the condition of being physically small, weak, or generally inadequate for a particular purpose or expectation.',
        'pronunciation': '/ˈpjuːnɪnəs/',
        'pronunciation_respelling': 'PYOO-nee-nus',
        'etymology': 'From "puny" + suffix "-ness," indicating the state of being puny.',
        'memory_tip': 'Think "puny" + "ness" = the state of being small and weak.',
        'example_sentence': 'The athlete was motivated by others\' comments about his ___ to build strength.',
        'source': 'Claude'
    },
    'punting': {
        'definition': 'Present participle of punt; propelling a boat with a long pole; kicking a football before it touches the ground; making risky financial bets. In each context, punting involves skillful technique to achieve forward movement or strategic advantage.',
        'pronunciation': '/ˈpʌntɪŋ/',
        'pronunciation_respelling': 'PUN-ting',
        'etymology': 'From "punt" + suffix "-ing," from Latin "ponto" meaning "bridge" or "ferry."',
        'memory_tip': 'Think "punt" + "ing" = the action of pushing forward with a pole or foot.',
        'example_sentence': '___ down the river, they enjoyed the peaceful countryside scenery.',
        'source': 'Claude'
    },
    'puppeteer': {
        'definition': 'A person who operates puppets in a performance; someone who manipulates puppet figures to create entertainment or tell stories. Puppeteers require skill in coordination, voice acting, and storytelling to bring inanimate figures to life for audiences.',
        'pronunciation': '/ˌpʌpəˈtɪr/',
        'pronunciation_respelling': 'pup-uh-TEER',
        'etymology': 'From "puppet" + suffix "-eer," from Old French "poupette" (little doll).',
        'memory_tip': 'Think "puppet" + "eer" (like engineer) = one who engineers puppet movements.',
        'example_sentence': 'The skilled ___ made the marionette dance with lifelike grace.',
        'source': 'Claude'
    },
    'puppets': {
        'definition': 'Plural of puppet; movable figures operated by strings, rods, or hands for entertainment; people who are controlled or manipulated by others. Puppets can be simple hand puppets or complex marionettes, serving both as entertainment tools and metaphors for manipulation.',
        'pronunciation': '/ˈpʌpɪts/',
        'pronunciation_respelling': 'PUP-its',
        'etymology': 'Plural of "puppet," from Old French "poupette," diminutive of "poupée" (doll).',
        'memory_tip': 'Think "pup" (small) + "pets" = small figures you can pet or control.',
        'example_sentence': 'The children\'s theater featured colorful ___ that told fairy tales.',
        'source': 'Claude'
    },
    'purchase': {
        'definition': 'To buy something; to acquire goods or services in exchange for payment; the act of buying; a firm grip or hold on something. Purchase implies a deliberate transaction where value is exchanged, whether monetary payment for goods or gaining a secure physical hold.',
        'pronunciation': '/ˈpɜːrtʃəs/',
        'pronunciation_respelling': 'PUR-chus',
        'etymology': 'From Old French "purchaser," meaning "to pursue" or "to acquire."',
        'memory_tip': 'Think "pur" (pursue) + "chase" = pursuing something to acquire it.',
        'example_sentence': 'She decided to ___ the textbook online for a better price.',
        'source': 'Claude'
    },
    'puree': {
        'definition': 'A smooth, creamy substance made by crushing or blending food; to make such a smooth mixture. Purees are common in cooking for soups, baby food, and sauces, created by removing lumps and achieving uniform texture through blending or straining.',
        'pronunciation': '/pjʊˈreɪ/',
        'pronunciation_respelling': 'pyoo-RAY',
        'etymology': 'From French "purée," from "purer" meaning "to purify" or "to strain."',
        'memory_tip': 'Think "pure" + "ay" = making food purely smooth.',
        'example_sentence': 'The chef made a smooth tomato ___ for the soup base.',
        'source': 'Claude'
    },
    'purification': {
        'definition': 'The process of removing contaminants, impurities, or unwanted elements; making something clean, pure, or sacred. Purification can be physical (cleaning water), chemical (refining metals), spiritual (religious rituals), or metaphorical (moral cleansing).',
        'pronunciation': '/ˌpjʊrəfəˈkeɪʃən/',
        'pronunciation_respelling': 'pyoor-ih-fih-KAY-shun',
        'etymology': 'From Latin "purificatio," from "purificare" meaning "to make pure."',
        'memory_tip': 'Think "pure" + "fication" = the process of making something pure.',
        'example_sentence': 'The water treatment plant\'s ___ system removed harmful bacteria.',
        'source': 'Claude'
    },
    'purificationplantain': {
        'definition': '[COMBINED WORD ERROR] This appears to be "purification" + "plantain" incorrectly joined. Should be separated into two distinct words: "purification" (the process of making something pure) and "plantain" (a type of banana-like fruit).',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "purification" (Latin: making pure) with "plantain" (Latin: flat plant).',
        'memory_tip': '[ERROR] This should be split into "purification" (cleaning process) and "plantain" (fruit).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "purification" and "plantain."',
        'source': 'Claude'
    },
    'puritan': {
        'definition': 'A member of a Protestant group in 16th and 17th century England and America that sought to purify the Church of England; a person with strict moral or religious principles. Puritans emphasized personal piety, hard work, and simple living while opposing elaborate religious ceremonies.',
        'pronunciation': '/ˈpjʊrətən/',
        'pronunciation_respelling': 'PYOOR-ih-tun',
        'etymology': 'From "purify" + suffix "-an," referring to their desire to purify religious practices.',
        'memory_tip': 'Think "pure" + "itan" (like titan) = powerful advocates for purity.',
        'example_sentence': 'The ___ settlers established communities based on strict religious principles.',
        'source': 'Claude'
    },
    'purple': {
        'definition': 'A color intermediate between red and blue; cloth or clothing of this color, especially as worn by royalty; having a purple color. Purple has historically been associated with royalty, luxury, and nobility due to the expense of purple dyes in ancient times.',
        'pronunciation': '/ˈpɜːrpəl/',
        'pronunciation_respelling': 'PUR-pul',
        'etymology': 'From Latin "purpura," from Greek "porphyra," referring to a purple shellfish dye.',
        'memory_tip': 'Think of "purple" as "pur" (pure) + "ple" = purely beautiful royal color.',
        'example_sentence': 'The princess wore a beautiful ___ gown to the royal ball.',
        'source': 'Claude'
    },
    'purpose': {
        'definition': 'The reason for which something is done or created; an intended or desired result; intention or determination. Purpose provides direction and meaning, whether in individual actions, organizational goals, or the design of objects and systems.',
        'pronunciation': '/ˈpɜːrpəs/',
        'pronunciation_respelling': 'PUR-pus',
        'etymology': 'From Old French "porpos," from "proposer" meaning "to put forth" or "to propose."',
        'memory_tip': 'Think "pur" (pursue) + "pose" = pursuing a specific goal or intention.',
        'example_sentence': 'The ___ of education is to develop knowledge and critical thinking skills.',
        'source': 'Claude'
    },
    'purposes': {
        'definition': 'Plural of purpose; multiple reasons or intentions; various goals or objectives. Having multiple purposes indicates versatility and the ability to serve different functions or meet various needs simultaneously.',
        'pronunciation': '/ˈpɜːrpəsɪz/',
        'pronunciation_respelling': 'PUR-pus-iz',
        'etymology': 'Plural form of "purpose," from Old French "porpos."',
        'memory_tip': 'Think "purpose" + "s" = multiple goals or intentions.',
        'example_sentence': 'The community center serves many ___, including education and recreation.',
        'source': 'Claude'
    },
    'purse': {
        'definition': 'A small bag for carrying money and personal items; financial resources; to draw together tightly, as in pursing lips. Purses serve practical functions for carrying essentials while often reflecting personal style and social status.',
        'pronunciation': '/pɜːrs/',
        'pronunciation_respelling': 'PURS',
        'etymology': 'From Old French "borse," from Greek "byrsa" meaning "hide" or "leather."',
        'memory_tip': 'Think of a "pure" bag for keeping money and essentials safe.',
        'example_sentence': 'She reached into her ___ to find exact change for the bus fare.',
        'source': 'Claude'
    },
    'pursuit': {
        'definition': 'The action of pursuing someone or something; a recreational activity or hobby; the act of striving to achieve or obtain something. Pursuit implies active effort and persistence in seeking goals, whether tangible objectives or abstract ideals.',
        'pronunciation': '/pərˈsuːt/',
        'pronunciation_respelling': 'pur-SOOT',
        'etymology': 'From Old French "poursuivre," meaning "to follow after" or "to chase."',
        'memory_tip': 'Think "pursue" + "it" = actively going after something.',
        'example_sentence': 'His ___ of knowledge led him to read voraciously throughout his life.',
        'source': 'Claude'
    },
    'purvey': {
        'definition': 'To supply or provide goods or services; to spread or promote ideas or information; to act as a purveyor. Purveying involves being a source or supplier, whether of physical goods, services, or information.',
        'pronunciation': '/pərˈveɪ/',
        'pronunciation_respelling': 'pur-VAY',
        'etymology': 'From Old French "pourveoir," meaning "to provide" or "to supply."',
        'memory_tip': 'Think "pur" (for) + "vey" (convey) = conveying goods for others.',
        'example_sentence': 'The local bakery continues to ___ fresh bread to the community.',
        'source': 'Claude'
    },
    'pusillanimous': {
        'definition': 'Showing a lack of courage or determination; timid, cowardly, or faint-hearted. Pusillanimous behavior is characterized by avoiding challenges or conflicts due to fear or lack of moral courage.',
        'pronunciation': '/ˌpjuːsəˈlænəməs/',
        'pronunciation_respelling': 'pyoo-suh-LAN-uh-mus',
        'etymology': 'From Latin "pusillanimis," from "pusillus" (very small) + "animus" (spirit).',
        'memory_tip': 'Think "puny" + "animal" + "us" = having the spirit of a small, timid animal.',
        'example_sentence': 'The ___ politician avoided taking any controversial stances.',
        'source': 'Claude'
    },
    'putrescent': {
        'definition': 'In the process of rotting or decay; becoming putrid; characterized by decomposition. Putrescent describes organic matter that is actively breaking down, often accompanied by unpleasant odors and changes in texture and appearance.',
        'pronunciation': '/pjuːˈtrɛsənt/',
        'pronunciation_respelling': 'pyoo-TRES-unt',
        'etymology': 'From Latin "putrescens," from "putrescere" meaning "to grow rotten."',
        'memory_tip': 'Think "putrid" + "escent" (becoming) = becoming rotten or putrid.',
        'example_sentence': 'The ___ fruit attracted flies in the compost bin.',
        'source': 'Claude'
    },
    'putrid': {
        'definition': 'Decomposed and foul-smelling; morally corrupt or extremely unpleasant; characterized by decay. Putrid describes the advanced stage of organic decomposition where offensive odors and harmful bacteria are present.',
        'pronunciation': '/ˈpjuːtrɪd/',
        'pronunciation_respelling': 'PYOO-trid',
        'etymology': 'From Latin "putridus," from "putrere" meaning "to rot."',
        'memory_tip': 'Think "put" + "rid" = something you want to put away and get rid of.',
        'example_sentence': 'The ___ smell from the garbage indicated it needed immediate disposal.',
        'source': 'Claude'
    },
    'putsch': {
        'definition': 'A violent attempt to overthrow a government; a coup or revolt, especially one that is sudden and poorly planned. The term is often associated with failed political takeovers and originated from descriptions of specific historical events in German-speaking countries.',
        'pronunciation': '/pʊtʃ/',
        'pronunciation_respelling': 'POOCH',
        'etymology': 'From German "Putsch," meaning "thrust" or "blow," originally from Swiss German.',
        'memory_tip': 'Think "push" with German pronunciation = a forceful political push for power.',
        'example_sentence': 'The military ___ failed when soldiers refused to support the rebels.',
        'source': 'Claude'
    },
    'puttering': {
        'definition': 'Present participle of putter; working in a desultory but pleasant way; occupying oneself with minor tasks; moving or acting aimlessly. Puttering describes leisurely, unfocused activity that is often therapeutic and satisfying despite lacking specific goals.',
        'pronunciation': '/ˈpʌtərɪŋ/',
        'pronunciation_respelling': 'PUT-ur-ing',
        'etymology': 'From "putter" + suffix "-ing," possibly imitative of gentle, repetitive sounds.',
        'memory_tip': 'Think "put" + "tering" = putting things here and there without urgency.',
        'example_sentence': 'He spent the afternoon ___ in his workshop, organizing tools.',
        'source': 'Claude'
    },
    'putty': {
        'definition': 'A soft, malleable substance used for sealing glass in window frames and filling holes in wood; any similar moldable material. Putty hardens when exposed to air, making it useful for repairs and construction where flexible sealing is needed.',
        'pronunciation': '/ˈpʌti/',
        'pronunciation_respelling': 'PUT-ee',
        'etymology': 'From French "potée," meaning "potful," referring to a paste-like consistency.',
        'memory_tip': 'Think "put" + "ty" = something you put on to seal or fill.',
        'example_sentence': 'The glazier used ___ to secure the new window pane.',
        'source': 'Claude'
    },
    'puzzle': {
        'definition': 'A game, problem, or toy designed to test mental skills or knowledge; something that is difficult to understand or explain; to cause someone to feel confused. Puzzles challenge cognitive abilities and provide entertainment through problem-solving.',
        'pronunciation': '/ˈpʌzəl/',
        'pronunciation_respelling': 'PUZ-ul',
        'etymology': 'Origin uncertain, possibly from "pose" meaning "to perplex" or from obsolete "pusle."',
        'memory_tip': 'Think "puz" (puzzling) + "le" = something that makes you think puzzlingly.',
        'example_sentence': 'The thousand-piece jigsaw ___ kept the family busy all weekend.',
        'source': 'Claude'
    },
    'puzzles': {
        'definition': 'Plural of puzzle; multiple games or problems designed to challenge mental skills; things that confuse or perplex; third person singular of puzzle, meaning to confuse. Puzzles come in many forms and serve both entertainment and educational purposes.',
        'pronunciation': '/ˈpʌzəlz/',
        'pronunciation_respelling': 'PUZ-ulz',
        'etymology': 'Plural form of "puzzle," of uncertain origin.',
        'memory_tip': 'Think "puzzle" + "s" = multiple brain teasers or confusing things.',
        'example_sentence': 'The book contained word ___ and crosswords for different skill levels.',
        'source': 'Claude'
    },
    'puzzlespage': {
        'definition': '[COMBINED WORD ERROR] This appears to be "puzzles" + "page" incorrectly joined. Should be separated into two distinct words: "puzzles" (brain teasers or games) and "page" (a sheet of paper or web page).',
        'pronunciation': '[ERROR - COMBINED WORDS]',
        'pronunciation_respelling': '[ERROR - COMBINED WORDS]',
        'etymology': '[ERROR - COMBINED WORDS] This combines "puzzles" (uncertain origin) with "page" (Latin: sheet).',
        'memory_tip': '[ERROR] This should be split into "puzzles" (games) and "page" (sheet).',
        'example_sentence': '[ERROR] This combined word should be corrected to separate "puzzles" and "page."',
        'source': 'Claude'
    },
    'pylorus': {
        'definition': 'The opening from the stomach to the duodenum (first part of the small intestine); the region surrounding this opening. The pylorus regulates the passage of partially digested food from the stomach to the small intestine through muscular contractions.',
        'pronunciation': '/paɪˈlɔːrəs/',
        'pronunciation_respelling': 'py-LOR-us',
        'etymology': 'From Greek "pyloros," meaning "gatekeeper," from "pyle" (gate) + "ouros" (guard).',
        'memory_tip': 'Think "py" (pipe) + "lorus" (gatekeeper) = the gate between stomach and intestine.',
        'example_sentence': 'The surgeon repaired the damaged ___ to restore normal digestion.',
        'source': 'Claude'
    },
    'pyramid': {
        'definition': 'A monumental structure with a triangular or square base and sloping sides meeting at a point; any structure or object of similar shape; a system or organization structured in hierarchical levels. Pyramids are found in various cultures and serve both architectural and symbolic purposes.',
        'pronunciation': '/ˈpɪrəmɪd/',
        'pronunciation_respelling': 'PEER-uh-mid',
        'etymology': 'From Greek "pyramis," possibly from Egyptian origin.',
        'memory_tip': 'Think "pyr" (fire) + "amid" = fire pointing up amid the desert.',
        'example_sentence': 'The ancient Egyptian ___ at Giza remains one of the world\'s wonders.',
        'source': 'Claude'
    },
    'pyrite': {
        'definition': 'A brassy yellow mineral composed of iron sulfide; also called fool\'s gold because of its resemblance to gold. Pyrite is common in sedimentary rocks and has been used historically in making fire and producing sulfur dioxide for various industrial processes.',
        'pronunciation': '/ˈpaɪraɪt/',
        'pronunciation_respelling': 'PY-ryt',
        'etymology': 'From Greek "pyrites," meaning "of fire," because it produces sparks when struck.',
        'memory_tip': 'Think "pyr" (fire) + "ite" (mineral) = the fire-making mineral.',
        'example_sentence': 'The prospector was disappointed to discover ___ instead of real gold.',
        'source': 'Claude'
    },
    'pyrotechnics': {
        'definition': 'The art or science of making fireworks; a spectacular display of fireworks; any brilliant or sensational display. Pyrotechnics combines chemistry and artistry to create controlled explosions that produce light, color, and sound effects for entertainment.',
        'pronunciation': '/ˌpaɪroʊˈtɛknɪks/',
        'pronunciation_respelling': 'py-roh-TEK-niks',
        'etymology': 'From Greek "pyr" (fire) + "tekhnikos" (of art or skill).',
        'memory_tip': 'Think "pyro" (fire) + "technics" (technology) = fire technology.',
        'example_sentence': 'The Fourth of July ___ display illuminated the night sky magnificently.',
        'source': 'Claude'
    },
    'pythagorean': {
        'definition': 'Relating to Pythagoras or his mathematical and philosophical teachings; following the principles or methods associated with the ancient Greek mathematician. Pythagorean concepts include the famous theorem about right triangles and beliefs about mathematical harmony in nature.',
        'pronunciation': '/pɪθæɡəˈriən/',
        'pronunciation_respelling': 'pih-thag-uh-REE-un',
        'etymology': 'From Pythagoras, ancient Greek mathematician and philosopher, + suffix "-ean."',
        'memory_tip': 'Think of Pythagoras + "ean" = relating to the famous mathematician.',
        'example_sentence': 'Students learned the ___ theorem: a² + b² = c² for right triangles.',
        'source': 'Claude'
    },
    'python': {
        'definition': 'A large, non-venomous snake that kills prey by constriction; a programming language known for its simplicity and readability. Pythons are found in tropical regions and are among the largest snakes in the world, while Python programming language is popular for its versatility.',
        'pronunciation': '/ˈpaɪθən/',
        'pronunciation_respelling': 'PY-thun',
        'etymology': 'From Greek "Python," a serpent killed by Apollo, from "pythein" (to rot).',
        'memory_tip': 'Think of the legendary Greek serpent that gives its name to both snake and programming language.',
        'example_sentence': 'The zoo\'s Burmese ___ measured over fifteen feet in length.',
        'source': 'Claude'
    },
    'pyxis': {
        'definition': 'A small box or container, especially one used for holding medicines or cosmetics; in botany, a type of seed capsule that opens with a lid. Pyxis containers have been used since ancient times for storing valuable or delicate substances.',
        'pronunciation': '/ˈpɪksɪs/',
        'pronunciation_respelling': 'PIK-sis',
        'etymology': 'From Greek "pyxis," meaning "box," from "pyxos" (boxwood tree).',
        'memory_tip': 'Think "picks" + "is" = what picks or holds small precious items.',
        'example_sentence': 'The ancient ___ contained healing ointments used by Greek physicians.',
        'source': 'Claude'
    },
    'pâtissier': {
        'definition': 'A pastry chef; a person skilled in making pastries, cakes, and other baked desserts. Pâtissiers undergo specialized training in the art of pastry making, combining technical skill with artistic creativity to produce elaborate and delicious confections.',
        'pronunciation': '/pəˈtɪsiˌeɪ/',
        'pronunciation_respelling': 'pah-tis-ee-AY',
        'etymology': 'From French "pâtissier," from "pâtisserie" (pastry shop), from "pâte" (paste, dough).',
        'memory_tip': 'Think French "pastry" + "sier" (maker) = one who makes fancy pastries.',
        'example_sentence': 'The renowned ___ created an elaborate wedding cake with delicate sugar flowers.',
        'source': 'Claude'
    },
    'qiyas': {
        'definition': 'In Islamic jurisprudence, analogical reasoning used to derive legal rulings for new situations by comparing them to established precedents in the Quran and Sunnah. Qiyas is one of the four primary sources of Islamic law and requires careful scholarly analysis.',
        'pronunciation': '/ˈkiːjæs/',
        'pronunciation_respelling': 'KEE-yas',
        'etymology': 'From Arabic "qiyas," meaning "measurement" or "analogy."',
        'memory_tip': 'Think "key" + "yas" = key method of reasoning in Islamic law.',
        'example_sentence': 'The scholar used ___ to determine the ruling on the modern financial instrument.',
        'source': 'Claude'
    },
    'quack': {
        'definition': 'The characteristic harsh sound made by a duck; a person who dishonestly claims to have medical knowledge; to make the sound of a duck; to practice medicine fraudulently. The term implies both the natural animal sound and deceptive human behavior.',
        'pronunciation': '/kwæk/',
        'pronunciation_respelling': 'KWAK',
        'etymology': 'Imitative of duck sounds; fraudulent doctor sense from "quacksalver" (boastful salesman).',
        'memory_tip': 'Think of the duck sound that also describes someone whose medical claims are just noise.',
        'example_sentence': 'The duck\'s loud ___ echoed across the peaceful pond.',
        'source': 'Claude'
    },
    'quadriceps': {
        'definition': 'The large muscle group at the front of the thigh consisting of four parts; crucial for leg extension and knee stability. The quadriceps are essential for walking, running, jumping, and standing, making them among the most important muscles for daily mobility.',
        'pronunciation': '/ˈkwɑːdrɪsɛps/',
        'pronunciation_respelling': 'KWOD-rih-seps',
        'etymology': 'From Latin "quadriceps," meaning "four-headed," from "quattuor" (four) + "caput" (head).',
        'memory_tip': 'Think "quad" (four) + "riceps" (like biceps) = four-part thigh muscle.',
        'example_sentence': 'The athlete strengthened her ___ muscles to improve her jumping ability.',
        'source': 'Claude'
    },
    'quadrilateral': {
        'definition': 'A polygon with four sides and four angles; any four-sided geometric figure. Quadrilaterals include squares, rectangles, parallelograms, trapezoids, and rhombuses, each with specific properties regarding side lengths, angles, and symmetry.',
        'pronunciation': '/ˌkwɑːdrəˈlætərəl/',
        'pronunciation_respelling': 'kwod-ruh-LAT-ur-ul',
        'etymology': 'From Latin "quadrilaterus," from "quattuor" (four) + "latus" (side).',
        'memory_tip': 'Think "quad" (four) + "lateral" (sides) = four-sided figure.',
        'example_sentence': 'The geometry student identified the ___ as a parallelogram.',
        'source': 'Claude'
    },
    'quadrillion': {
        'definition': 'The number 1,000,000,000,000,000 (one thousand trillion) in the American system; an extremely large number. Quadrillions are used in contexts involving vast quantities such as national debts, astronomical distances, or molecular counts in chemistry.',
        'pronunciation': '/kwɑːˈdrɪljən/',
        'pronunciation_respelling': 'kwod-RIL-yun',
        'etymology': 'From "quadri-" (four) + "million," following the pattern of numerical naming.',
        'memory_tip': 'Think "quad" (four) + "rillion" = the fourth power of a thousand after million.',
        'example_sentence': 'The national debt exceeded one ___ dollars for the first time.',
        'source': 'Claude'
    },
    'quagmire': {
        'definition': 'An area of soft, boggy ground that gives way underfoot; a complex or precarious situation from which it is difficult to escape. Quagmires represent both physical terrain hazards and metaphorical traps that become increasingly difficult to resolve.',
        'pronunciation': '/ˈkwæɡmaɪər/',
        'pronunciation_respelling': 'KWAG-myr',
        'etymology': 'From "quag" (marshy ground) + "mire" (swampy ground).',
        'memory_tip': 'Think "quag" (shaky) + "mire" (mud) = shaky muddy trap.',
        'example_sentence': 'The peace negotiations became a political ___ with no clear resolution.',
        'source': 'Claude'
    },
    'qualifying': {
        'definition': 'Present participle of qualify; meeting necessary requirements or standards; limiting or modifying the meaning of something; earning the right to participate. Qualifying implies achieving competency or eligibility through demonstrated ability or completion of requirements.',
        'pronunciation': '/ˈkwɑːləˌfaɪɪŋ/',
        'pronunciation_respelling': 'KWOL-uh-fy-ing',
        'etymology': 'From "qualify" + suffix "-ing," from Latin "qualificare" (to describe the quality of).',
        'memory_tip': 'Think "quality" + "fying" = proving you have the quality needed.',
        'example_sentence': 'After ___ for the state tournament, the team celebrated their achievement.',
        'source': 'Claude'
    },
    'qualitative': {
        'definition': 'Relating to or measured by quality rather than quantity; concerned with characteristics or attributes rather than numerical values. Qualitative research focuses on understanding experiences, behaviors, and motivations through observation and interpretation rather than statistical analysis.',
        'pronunciation': '/ˈkwɑːləˌteɪtɪv/',
        'pronunciation_respelling': 'KWOL-uh-tay-tiv',
        'etymology': 'From "quality" + suffix "-ative," from Latin "qualitas" (quality).',
        'memory_tip': 'Think "quality" + "ative" = relating to the quality/nature of things.',
        'example_sentence': 'The researcher conducted ___ interviews to understand patient experiences.',
        'source': 'Claude'
    },
    'quality': {
        'definition': 'The standard of something as measured against other things; a distinctive characteristic or attribute; the degree of excellence. Quality encompasses both measurable standards and subjective judgments about worth, value, or desirability.',
        'pronunciation': '/ˈkwɑːləti/',
        'pronunciation_respelling': 'KWOL-uh-tee',
        'etymology': 'From Latin "qualitas," from "qualis" meaning "of what kind."',
        'memory_tip': 'Think "what" + "ality" = what-ness or the nature of something.',
        'example_sentence': 'The ___ of education improved significantly with the new curriculum.',
        'source': 'Claude'
    },
    'qualms': {
        'definition': 'Feelings of doubt, uneasiness, or apprehension about the rightness of an action; scruples or misgivings. Qualms represent internal moral conflicts that arise when contemplating actions that may be questionable or potentially harmful.',
        'pronunciation': '/kwɑːmz/',
        'pronunciation_respelling': 'KWOMZ',
        'etymology': 'Possibly from Old English "cwealm" meaning "death" or "plague," later meaning uneasiness.',
        'memory_tip': 'Think "qualm" sounds like "calm" disrupted = disturbed peace of mind.',
        'example_sentence': 'She had serious ___ about accepting the job offer from the controversial company.',
        'source': 'Claude'
    },
    'quandary': {
        'definition': 'A state of perplexity or uncertainty; a difficult situation where a choice must be made between alternatives that are equally unfavorable or uncertain. Quandaries present dilemmas where all available options have significant drawbacks or risks.',
        'pronunciation': '/ˈkwɑːndəri/',
        'pronunciation_respelling': 'KWON-duh-ree',
        'etymology': 'Origin uncertain, possibly from Latin "quando" meaning "when."',
        'memory_tip': 'Think "quan" (question) + "dary" (dairy) = questioning which milk to choose from many options.',
        'example_sentence': 'The family faced a ___ about whether to move for better jobs or stay near relatives.',
        'source': 'Claude'
    }
}

def process_batch_142():
    """Process batch 142 spelling bee words"""
    
    calculator = DifficultyCalculator()
    
    # Read input CSV
    input_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_142_words.csv'
    output_file = 'C:/Users/jessi/Projects/skilltree2/scripts/spelling_bee/output/batch_142_processed.csv'
    
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
                        'notes': 'Batch 142 processing',
                        'review_status': 'pending',
                        'batch_number': 142
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
            
            print(f"\nBatch 142 processing complete!")
            print(f"Successfully processed {len(processed_words)}/50 words")
            print(f"Output saved to: {output_file}")
            
            # Flag any combined word errors
            combined_errors = [word for word in processed_words if '[COMBINED WORD ERROR]' in word['definition']]
            if combined_errors:
                print(f"\nCombined word errors detected: {len(combined_errors)}")
                for error in combined_errors:
                    print(f"  - {error['word']}")
        
    except Exception as e:
        print(f"Error processing batch 142: {e}")
        return False
    
    return True

if __name__ == "__main__":
    process_batch_142()