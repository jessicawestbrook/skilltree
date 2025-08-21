#!/usr/bin/env python3

import csv
import logging
from typing import Dict, List, Any
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DifficultyCalculator:
    def calculate_difficulty_score(self, word: str, definition: str, etymology: str) -> Dict[str, Any]:
        phonetic_score = self._calculate_phonetic_transparency(word)
        frequency_score = self._calculate_word_frequency(word)
        morphological_score = self._calculate_morphological_complexity(word)
        etymology_score = self._calculate_etymology_complexity(etymology)
        
        return {
            'phonetic_transparency_score': phonetic_score,
            'word_frequency_score': frequency_score,
            'morphological_complexity_score': morphological_score,
            'etymology_complexity_score': etymology_score,
            'difficulty': None
        }
    
    def _calculate_phonetic_transparency(self, word: str) -> float:
        word = word.lower()
        irregularities = 0
        
        patterns = [
            (r'gh', 1), (r'ough', 2), (r'ph', 1), (r'ch(?![aeiouy])', 1),
            (r'qu', 0.5), (r'x', 1), (r'tion', 0.5), (r'sion', 0.5),
            (r'eau', 2), (r'ieu', 2), (r'ée', 1), (r'silent.*e$', 1)
        ]
        
        for pattern, weight in patterns:
            irregularities += len(re.findall(pattern, word)) * weight
        
        length_factor = len(word) / 10
        return min(5.0, irregularities + length_factor)
    
    def _calculate_word_frequency(self, word: str) -> float:
        common_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}
        word_lower = word.lower()
        
        if word_lower in common_words:
            return 1.0
        elif len(word) <= 4:
            return 2.0
        elif len(word) <= 6:
            return 3.0
        elif len(word) <= 8:
            return 4.0
        else:
            return 5.0
    
    def _calculate_morphological_complexity(self, word: str) -> float:
        word = word.lower()
        
        prefixes = ['un', 're', 'pre', 'dis', 'over', 'under', 'out', 'up', 'sub', 'inter', 'fore', 'de', 'mis', 'anti', 'semi', 'super', 'trans', 'ultra', 'non']
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment', 'ful', 'less', 'able', 'ible', 'ous', 'ive', 'al', 'ic', 'ism', 'ist', 'ize', 'ise']
        
        morphemes = 1
        temp_word = word
        
        for prefix in prefixes:
            if temp_word.startswith(prefix):
                morphemes += 1
                temp_word = temp_word[len(prefix):]
                break
        
        for suffix in suffixes:
            if temp_word.endswith(suffix):
                morphemes += 1
                temp_word = temp_word[:-len(suffix)]
                break
        
        if morphemes == 1:
            return 1.0
        elif morphemes == 2:
            return 2.5
        elif morphemes == 3:
            return 4.0
        else:
            return 5.0
    
    def _calculate_etymology_complexity(self, etymology: str) -> float:
        if not etymology or etymology.lower() in ['unknown', 'uncertain']:
            return 3.0
        
        etymology_lower = etymology.lower()
        complex_origins = ['sanskrit', 'hebrew', 'arabic', 'mandarin', 'japanese', 'finnish', 'hungarian', 'czech', 'polish', 'russian', 'nahuatl', 'quechua']
        moderate_origins = ['greek', 'latin', 'old english', 'middle english', 'old french', 'german', 'dutch', 'scandinavian', 'norse']
        simple_origins = ['english', 'french', 'spanish', 'italian', 'portuguese']
        
        if any(origin in etymology_lower for origin in complex_origins):
            return 5.0
        elif any(origin in etymology_lower for origin in moderate_origins):
            return 3.0
        elif any(origin in etymology_lower for origin in simple_origins):
            return 2.0
        else:
            return 3.5

class Batch129Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        self.combined_words = []
        
    def detect_combined_words(self) -> List[str]:
        combined_patterns = [
            'patronymicodometer',
            'patterndifficulty',
            'pauperepoch',
            'pelagialpelerine'
        ]
        return combined_patterns
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        word_data = {
            'patronymic': {
                'definition': 'A name derived from the name of a father or paternal ancestor, typically by adding a suffix meaning "son of" or "daughter of." Patronymic naming systems are found in many cultures, including Scandinavian (-son, -sen), Russian (-ovich, -ovna), and Arabic (ibn, bint). These names traditionally indicate family lineage and paternal heritage. Some societies use patronymics as middle names or surnames, while others employ them as primary identifiers. The practice reflects cultural values about family relationships and inheritance. Modern usage varies widely, with some cultures maintaining strict patronymic traditions while others have adopted fixed family names.',
                'pronunciation': '/ˌpætrəˈnɪmɪk/',
                'pronunciation_ipa': '/ˌpætrəˈnɪmɪk/',
                'etymology': 'From Greek "patronymikos," from "patronymos" meaning named after one\'s father, from "pater" (father) + "onyma" (name).',
                'memory_tip': 'PATRONYMIC = PATRO (father) + NYMIC (name). Think of names that come from your "father\'s name" - family naming traditions.',
                'example_sentence': 'In Iceland, children still receive _____ names based on their father\'s first name plus "son" or "dóttir."'
            },
            'pattern': {
                'definition': 'A repeated design or sequence; a model or template for making something; a regular and predictable form or order. Patterns appear in art, nature, behavior, and mathematics, representing organized repetition or systematic arrangement. They can be visual (textile patterns), behavioral (daily patterns), or conceptual (thought patterns). Recognizing patterns is fundamental to learning, problem-solving, and understanding complex systems. In design and manufacturing, patterns serve as templates for creating consistent products. The human brain is naturally wired to identify and create patterns as a way of organizing and understanding the world.',
                'pronunciation': '/ˈpætərn/',
                'pronunciation_ipa': '/ˈpætərn/',
                'etymology': 'From Old French "patron" meaning model or example, from Medieval Latin "patronus." Related to the concept of a protective example or template.',
                'memory_tip': 'PATTERN sounds like "PAT-TURN" - think of "patting" something and "turning" it repeatedly to create a repeating design.',
                'example_sentence': 'The quilter followed a traditional _____ that had been passed down through her family for generations.'
            },
            'paucity': {
                'definition': 'The presence of something only in small or insufficient quantities; scarcity or lack of something needed or desired. Paucity suggests not just absence but inadequacy - having some amount but not enough to meet requirements or expectations. The term is often used in formal or academic contexts to describe shortages of resources, information, evidence, or opportunities. Paucity implies that the limited quantity creates problems or limitations. Understanding paucity is important for resource management, research evaluation, and identifying areas needing improvement or investment.',
                'pronunciation': '/ˈpɔsəti/',
                'pronunciation_ipa': '/ˈpɔsəti/',
                'etymology': 'From Latin "paucitas" meaning fewness or scarcity, from "paucus" meaning few or little. Related to "pauper" (having little).',
                'memory_tip': 'PAUCITY sounds like "PAW-CITY" - think of a "paw" trying to grab things in a "city" but finding very little - scarcity.',
                'example_sentence': 'The research was limited by a _____ of reliable data on the subject.'
            },
            'pauper': {
                'definition': 'A very poor person who depends on charity or public assistance for survival; someone without material possessions or financial resources. Historically, paupers were individuals who required support from parish relief or workhouses. The term carries connotations of destitution and social vulnerability. Pauper status often affected legal rights and social standing in historical contexts. Modern social welfare systems aim to prevent pauperization and provide dignity to those needing assistance. The concept highlights issues of poverty, social support, and economic inequality in societies.',
                'pronunciation': '/ˈpɔpər/',
                'pronunciation_ipa': '/ˈpɔpər/',
                'etymology': 'From Latin "pauper" meaning poor or having little, from "paucus" (few) + "parare" (to provide). Literally means "providing little."',
                'memory_tip': 'PAUPER sounds like "PAW-PER" - think of someone with "paws" (empty hands) "per" necessity - having very little money.',
                'example_sentence': 'The Victorian novel depicted the harsh realities faced by the _____ in London\'s workhouses.'
            },
            'pavement': {
                'definition': 'A hard surface covering for roads, walkways, or other areas, typically made of concrete, asphalt, or stones; the material used to create such surfaces. Pavement provides durable, smooth surfaces for vehicle and pedestrian traffic. Different types include flexible pavement (asphalt) and rigid pavement (concrete), each with specific advantages and applications. Pavement design considers factors like traffic load, climate, and soil conditions. Maintenance involves regular inspection, crack sealing, and resurfacing. The quality of pavement infrastructure significantly affects transportation efficiency, safety, and economic development.',
                'pronunciation': '/ˈpeɪvmənt/',
                'pronunciation_ipa': '/ˈpeɪvmənt/',
                'etymology': 'From Latin "pavimentum" meaning a floor beaten or rammed down, from "pavire" meaning to beat or ram down.',
                'memory_tip': 'PAVEMENT = PAVE + MENT. Think of the hard surface that results from "paving" roads and walkways.',
                'example_sentence': 'The city repaired the cracked _____ on Main Street to improve safety for both drivers and pedestrians.'
            },
            'pavilions': {
                'definition': 'Ornamental buildings or structures, often open or lightly enclosed, used for shelter, entertainment, or ceremonies; temporary or permanent structures in gardens, parks, or event venues. Pavilions can range from simple gazebos to elaborate architectural features. They often serve as focal points in landscape design, providing shaded gathering spaces. Exhibition pavilions house displays at fairs and expositions. Sports pavilions provide covered areas for spectators or players. The design typically emphasizes openness to surroundings while providing some protection from weather.',
                'pronunciation': '/pəˈvɪljənz/',
                'pronunciation_ipa': '/pəˈvɪljənz/',
                'etymology': 'Plural of "pavilion," from Old French "paveillon," from Latin "papilio" meaning butterfly, referring to tent-like structures resembling butterfly wings.',
                'memory_tip': 'PAVILIONS = PAVILION + S. Think of multiple butterfly-like structures that spread their "wings" to shelter people in gardens.',
                'example_sentence': 'The botanical garden featured several elegant _____ where visitors could rest and enjoy the scenery.'
            },
            'pavlova': {
                'definition': 'A meringue-based dessert with a crisp exterior and soft, marshmallow-like interior, typically topped with whipped cream and fresh fruit. Named after the Russian ballerina Anna Pavlova, this dessert is claimed by both Australia and New Zealand as their national creation. The base is made from egg whites and sugar beaten to stiff peaks, then baked at low temperature. The contrast between the crispy shell and soft center creates the dessert\'s distinctive texture. Pavlova is often served at celebrations and summer gatherings, particularly in Australia and New Zealand.',
                'pronunciation': '/pævˈloʊvə/',
                'pronunciation_ipa': '/pævˈloʊvə/',
                'etymology': 'Named after Anna Pavlova (1881-1931), the famous Russian prima ballerina, supposedly created to honor her tours of Australia and New Zealand.',
                'memory_tip': 'PAVLOVA sounds like "PAV-LOVE-A" - think of "loving" the light, airy dessert named after the graceful ballerina Anna "Pav"lova.',
                'example_sentence': 'The chef prepared a stunning _____ topped with fresh berries and passion fruit for the dinner party.'
            },
            'payments': {
                'definition': 'Transfers of money or other valuable consideration made to settle debts, purchase goods or services, or fulfill obligations; amounts paid or to be paid. Payments can be made through various methods including cash, checks, credit cards, electronic transfers, or digital currencies. Payment systems are fundamental to commerce and economic activity. Modern payment processing involves complex networks of banks, clearinghouses, and technology providers. Payment security, fraud prevention, and regulatory compliance are critical concerns in financial systems. Different payment methods offer varying levels of convenience, security, and cost.',
                'pronunciation': '/ˈpeɪmənts/',
                'pronunciation_ipa': '/ˈpeɪmənts/',
                'etymology': 'Plural of "payment," from "pay" (from Latin "pacare" meaning to pacify or settle) + "-ment" suffix indicating result or process.',
                'memory_tip': 'PAYMENTS = PAY + MENTS. Think of multiple instances of "paying" money - various "ments" (methods) of transferring value.',
                'example_sentence': 'The online store accepts _____ through credit cards, digital wallets, and bank transfers.'
            },
            'peaceful': {
                'definition': 'Characterized by tranquility, calm, and absence of conflict or disturbance; promoting or inclined toward peace rather than violence or aggression. Peaceful describes environments, situations, people, or actions that embody serenity and harmony. The term applies to personal demeanor, conflict resolution approaches, and social movements that seek change through non-violent means. Peaceful settings provide rest and relaxation from stress and anxiety. The concept is valued across cultures as both a personal virtue and a social ideal for resolving disputes and maintaining community harmony.',
                'pronunciation': '/ˈpisfəl/',
                'pronunciation_ipa': '/ˈpisfəl/',
                'etymology': 'From "peace" (from Latin "pax, pacis") + "-ful" suffix meaning full of or characterized by. Literally means "full of peace."',
                'memory_tip': 'PEACEFUL = PEACE + FUL. Think of being "full" of "peace" - calm, serene, and without conflict or disturbance.',
                'example_sentence': 'The monastery garden provided a _____ retreat from the noise and stress of city life.'
            },
            'peacenik': {
                'definition': 'A person who actively opposes war and advocates for peace, often used somewhat disparagingly to describe anti-war activists or pacifists. The term gained popularity during the Vietnam War era to describe protesters who opposed military action. Peaceniks typically support non-violent conflict resolution, disarmament, and diplomatic solutions to international disputes. While sometimes used mockingly, many peaceniks have played important roles in social movements and peace advocacy. The term reflects tensions between those who support military action and those who prefer peaceful alternatives to conflict.',
                'pronunciation': '/ˈpisˌnɪk/',
                'pronunciation_ipa': '/ˈpisˌnɪk/',
                'etymology': 'Combination of "peace" + "-nik" suffix (from Yiddish/Slavic languages) meaning a person associated with or advocating for something.',
                'memory_tip': 'PEACENIK = PEACE + NIK. Think of a person who is a "nik" (advocate) for "peace" - someone who opposes war.',
                'example_sentence': 'The former soldier became a _____ after experiencing the horrors of combat firsthand.'
            },
            'peach': {
                'definition': 'A soft, round fruit with fuzzy skin and sweet, juicy flesh surrounding a hard pit; the tree that produces this fruit; a pale orange-pink color; slang for an excellent or attractive person or thing. Peaches are stone fruits native to China but now cultivated worldwide in temperate climates. They require specific growing conditions and are harvested in summer. Peaches are rich in vitamins and minerals and are enjoyed fresh, canned, or in baked goods. The color "peach" describes the fruit\'s characteristic pale orange-pink hue.',
                'pronunciation': '/pitʃ/',
                'pronunciation_ipa': '/pitʃ/',
                'etymology': 'From Old French "pesche," from Latin "persica" meaning Persian apple, as peaches were thought to come from Persia (though they originated in China).',
                'memory_tip': 'PEACH sounds like "PEACE" - think of the peaceful, sweet feeling of eating a soft, juicy peach on a summer day.',
                'example_sentence': 'She bit into the ripe _____, and the sweet juice ran down her chin.'
            },
            'peanut': {
                'definition': 'A legume that grows underground and develops in pods, despite its name suggesting it\'s a nut; also called groundnut or goober. Peanuts are not true nuts but rather seeds of plants in the pea family. They are rich in protein, healthy fats, and various nutrients. Peanuts are consumed roasted, boiled, or processed into peanut butter, oil, and other products. They are major crops in many countries and important sources of nutrition and income. Peanut allergies are common and can be severe, making peanut-free environments necessary in some settings.',
                'pronunciation': '/ˈpiˌnʌt/',
                'pronunciation_ipa': '/ˈpiˌnʌt/',
                'etymology': 'Compound of "pea" + "nut," though technically neither a pea nor a nut. The name reflects its small size and nut-like appearance.',
                'memory_tip': 'PEANUT = PEA + NUT. Think of a small "pea"-sized "nut" that grows underground, though it\'s actually a legume.',
                'example_sentence': 'The school banned _____ products from lunch boxes due to students with severe allergies.'
            },
            'pear': {
                'definition': 'A sweet, bell-shaped fruit with white or yellowish flesh and smooth skin that can be green, yellow, red, or brown; the tree that produces this fruit. Pears belong to the rose family and are cultivated in temperate regions worldwide. They ripen from the inside out and are often harvested before fully ripe. Pears are eaten fresh, dried, canned, or used in cooking and baking. Different varieties offer varying textures, flavors, and growing seasons. The fruit is rich in fiber, vitamins, and antioxidants.',
                'pronunciation': '/pɛr/',
                'pronunciation_ipa': '/pɛr/',
                'etymology': 'From Old English "pere," from Latin "pirum." The word has remained relatively stable across Indo-European languages.',
                'memory_tip': 'PEAR sounds like "PAIR" - think of the classic "pair" of sweet, bell-shaped fruits that often grow together on trees.',
                'example_sentence': 'The bartlett _____ was perfectly ripe, with tender flesh and sweet, juicy flavor.'
            },
            'pearlescent': {
                'definition': 'Having a lustrous, iridescent quality resembling mother-of-pearl; exhibiting a soft, shimmering glow with subtle color variations. Pearlescent surfaces reflect light in ways that create shifting colors and luminous effects. This quality is found naturally in pearls, abalone shells, and certain minerals. Artificial pearlescent effects are created in paints, cosmetics, and materials using special pigments or coatings. The appearance changes depending on viewing angle and lighting conditions. Pearlescent finishes are prized for their elegant, sophisticated appearance in automotive, architectural, and decorative applications.',
                'pronunciation': '/ˌpɜrləˈsɛnt/',
                'pronunciation_ipa': '/ˌpɜrləˈsɛnt/',
                'etymology': 'From "pearl" + "-escent" suffix meaning becoming or having the quality of. Literally means "becoming like a pearl."',
                'memory_tip': 'PEARLESCENT = PEARL + ESCENT. Think of something that\'s "becoming" like a "pearl" - shimmering with lustrous, changing colors.',
                'example_sentence': 'The car\'s _____ paint shifted from silver to blue as it moved through different lighting conditions.'
            },
            'peat': {
                'definition': 'Partially decomposed organic matter, primarily plant material, that accumulates in waterlogged conditions such as bogs and marshes; used as fuel and soil amendment. Peat forms over thousands of years as plant matter decomposes slowly in acidic, oxygen-poor environments. It\'s harvested for use as fuel, particularly in Ireland and Scotland, and as a soil conditioner for gardening. Peat bogs are important ecosystems that store carbon and support unique plant and animal communities. Environmental concerns about peat harvesting include habitat destruction and carbon release.',
                'pronunciation': '/pit/',
                'pronunciation_ipa': '/pit/',
                'etymology': 'From Middle English "pete," possibly from Celtic origin. Related to the material\'s use as fuel in Celtic regions.',
                'memory_tip': 'PEAT rhymes with "HEAT" - think of the "heat" energy you get from burning this decomposed plant material as fuel.',
                'example_sentence': 'The gardener mixed _____ into the soil to improve water retention and provide nutrients for the plants.'
            },
            'pebble': {
                'definition': 'A small, smooth stone worn down by water or weather action; typically rounded and polished by natural forces. Pebbles are found on beaches, riverbanks, and other areas where water action has smoothed rough stones. They range in size from about 4 to 64 millimeters in diameter, larger than gravel but smaller than cobbles. Pebbles are used in landscaping, construction, and decorative applications. Beach pebbles are popular for their smooth texture and attractive appearance. The formation process takes considerable time as stones are gradually shaped by rolling and friction.',
                'pronunciation': '/ˈpɛbəl/',
                'pronunciation_ipa': '/ˈpɛbəl/',
                'etymology': 'From Old English "papolstān" meaning pebble stone, later influenced by Latin "papula" meaning pimple or small swelling.',
                'memory_tip': 'PEBBLE sounds like "PEB-BELL" - think of small, smooth stones that make a gentle "bell"-like sound when they click together.',
                'example_sentence': 'Children collected smooth _____ from the beach to use in their art project.'
            },
            'pebbles': {
                'definition': 'Plural of pebble; multiple small, smooth stones worn down by natural forces; also refers to a textured surface or pattern resembling small stones. Beach pebbles are popular for landscaping, drainage, and decorative purposes. Pebbled surfaces appear in leather goods, glass, and other materials to create texture and visual interest. The word can also refer to small, round objects that resemble natural pebbles. Collecting pebbles is a common beach activity, and different locations produce pebbles with unique colors and compositions.',
                'pronunciation': '/ˈpɛbəlz/',
                'pronunciation_ipa': '/ˈpɛbəlz/',
                'etymology': 'Plural of "pebble," from Old English origins. The collective form emphasizes multiple small stones found together.',
                'memory_tip': 'PEBBLES = PEBBLE + S. Think of many small, smooth stones scattered along a beach or riverbank.',
                'example_sentence': 'The path was lined with colorful _____ that crunched softly underfoot as visitors walked through the garden.'
            },
            'peculate': {
                'definition': 'To steal or misappropriate money or property entrusted to one\'s care, especially public funds or property held in an official capacity; to embezzle. Peculation typically involves abuse of trusted positions to unlawfully take funds or resources. The crime often occurs in government, corporate, or institutional settings where individuals have access to finances or valuables. Legal systems treat peculation as a serious offense due to the breach of trust involved. Prevention measures include auditing, oversight, and internal controls. The term emphasizes the violation of fiduciary responsibility inherent in such theft.',
                'pronunciation': '/ˈpɛkjəˌleɪt/',
                'pronunciation_ipa': '/ˈpɛkjəˌleɪt/',
                'etymology': 'From Latin "peculatus" meaning embezzlement, from "peculari" meaning to embezzle, from "peculium" meaning private property.',
                'memory_tip': 'PECULATE sounds like "PEC-YOU-LATE" - think of someone who "pecs" (steals) from "you" when it\'s too "late" to stop them.',
                'example_sentence': 'The treasurer was found guilty of attempting to _____ funds from the charity organization.'
            },
            'peculiarities': {
                'definition': 'Distinctive or unusual characteristics, features, or behaviors that set something apart from what is normal or expected; strange or eccentric qualities. Peculiarities can be endearing quirks or problematic anomalies depending on context. Every individual, culture, or system has peculiarities that make it unique. In scientific or technical contexts, peculiarities might indicate special conditions or properties requiring investigation. Understanding peculiarities helps in recognition, diagnosis, and appreciation of diversity. The term suggests deviation from standard patterns while not necessarily implying negative judgment.',
                'pronunciation': '/pɪˌkjuliˈærətiz/',
                'pronunciation_ipa': '/pɪˌkjuliˈærətiz/',
                'etymology': 'Plural of "peculiarity," from Latin "peculiaris" meaning one\'s own or distinctive, from "peculium" meaning private property.',
                'memory_tip': 'PECULIARITIES = PECULIAR + ITIES. Think of multiple strange "qualities" that make someone or something "peculiar" or distinctive.',
                'example_sentence': 'The detective noted several _____ in the suspect\'s behavior that seemed inconsistent with his alibi.'
            },
            'pecuniary': {
                'definition': 'Relating to or involving money; financial or monetary in nature. Pecuniary matters include income, expenses, debts, investments, and other financial concerns. Legal contexts often distinguish between pecuniary damages (monetary losses) and non-pecuniary damages (pain, suffering, loss of enjoyment). The term appears frequently in formal, legal, and business writing when discussing financial aspects of situations. Pecuniary interests refer to financial stakes in outcomes. Understanding pecuniary implications helps in making informed decisions about economic matters and legal settlements.',
                'pronunciation': '/pɪˈkjuniˌɛri/',
                'pronunciation_ipa': '/pɪˈkjuniˌɛri/',
                'etymology': 'From Latin "pecuniarius" meaning of or relating to money, from "pecunia" meaning money, from "pecus" meaning cattle (early form of wealth).',
                'memory_tip': 'PECUNIARY sounds like "PEH-COON-IARY" - think of a "raccoon" who is interested in money and financial matters.',
                'example_sentence': 'The court awarded _____ damages to compensate for the plaintiff\'s lost wages and medical expenses.'
            },
            'pedantry': {
                'definition': 'Excessive concern with minor details, rules, or displaying academic knowledge; showing off one\'s learning in a tedious or arrogant manner. Pedantry involves prioritizing technical correctness over practical understanding or meaningful communication. While attention to detail can be valuable, pedantry becomes problematic when it hinders communication or focuses on trivial points while missing larger issues. The behavior often reflects insecurity or desire to demonstrate superiority rather than genuine scholarly pursuit. Effective education and communication balance accuracy with accessibility and relevance.',
                'pronunciation': '/ˈpɛdəntri/',
                'pronunciation_ipa': '/ˈpɛdəntri/',
                'etymology': 'From "pedant" (from Italian "pedante," possibly from Latin "paedagogus" meaning teacher) + "-ry" suffix indicating behavior or practice.',
                'memory_tip': 'PEDANTRY = PEDANT + RY. Think of the annoying "try" to show off knowledge that a "pedant" does - excessive focus on minor details.',
                'example_sentence': 'The professor\'s _____ made lectures tedious as he spent excessive time correcting minor pronunciation errors.'
            },
            'peddle': {
                'definition': 'To travel from place to place selling goods; to promote or advocate something persistently, often something questionable or unwanted. Traditional peddlers carried goods door-to-door or in markets. Modern usage often refers to selling ideas, influence, or illegal substances. The term can have negative connotations when describing the promotion of false information, conspiracy theories, or harmful products. Street vendors and traveling merchants engage in legitimate peddling. The activity requires mobility, persuasion skills, and often targets areas with limited access to regular retail stores.',
                'pronunciation': '/ˈpɛdəl/',
                'pronunciation_ipa': '/ˈpɛdəl/',
                'etymology': 'From Middle English "pedlen," possibly from "ped" meaning basket or pack. Related to carrying goods for sale.',
                'memory_tip': 'PEDDLE sounds like "PADDLE" - think of "paddling" around from place to place to sell things or spread ideas.',
                'example_sentence': 'The street vendor continued to _____ handmade jewelry at the weekend market.'
            },
            'pedestals': {
                'definition': 'Platforms or bases supporting statues, columns, or other structures; positions of high regard or admiration. Physical pedestals elevate objects for display, protection, or ceremonial purposes. Figurative pedestals represent positions of respect, honor, or idealization. Putting someone "on a pedestal" means viewing them as perfect or superior. Pedestals in architecture provide both functional support and aesthetic enhancement. The concept extends to any elevated platform or position of prominence. Understanding pedestals helps in design, display, and recognizing how elevation affects perception and significance.',
                'pronunciation': '/ˈpɛdəstəlz/',
                'pronunciation_ipa': '/ˈpɛdəstəlz/',
                'etymology': 'Plural of "pedestal," from Italian "piedestallo," from "piede" (foot) + "stallo" (stall or place). Literally means "foot place."',
                'memory_tip': 'PEDESTALS = PEDE (foot) + STALS (stands). Think of "foot stands" that elevate statues or put people in high positions.',
                'example_sentence': 'The museum displayed ancient artifacts on marble _____ to protect them and enhance their visibility.'
            },
            'pedestrian': {
                'definition': 'A person traveling on foot; lacking inspiration or excitement; ordinary or mundane. As a noun, pedestrian refers to walkers in contrast to vehicle occupants. Traffic laws and urban planning address pedestrian safety and movement. As an adjective, pedestrian describes things that are prosaic, unimaginative, or commonplace. The figurative usage suggests something that walks rather than soars - reliable but uninspiring. Pedestrian areas in cities provide car-free zones for walking. The dual meaning reflects the contrast between practical, ground-level movement and elevated, creative expression.',
                'pronunciation': '/pəˈdɛstriən/',
                'pronunciation_ipa': '/pəˈdɛstriən/',
                'etymology': 'From Latin "pedestris" meaning on foot, from "pes, pedis" meaning foot. Originally just meant "going on foot."',
                'memory_tip': 'PEDESTRIAN = PEDE (foot) + STRIAN. Think of someone using their "feet" to travel, or something that\'s "down to earth" and ordinary.',
                'example_sentence': 'The crosswalk signal gave _____ priority during rush hour to improve safety in the busy downtown area.'
            },
            'pedicure': {
                'definition': 'A cosmetic treatment for feet and toenails involving cleaning, trimming, shaping, and often polishing nails, plus care for the skin of the feet. Pedicures may include soaking, exfoliation, callus removal, massage, and moisturizing. Professional pedicures are performed in salons and spas, while basic versions can be done at home. The treatment promotes foot health, hygiene, and appearance. Medical pedicures address specific foot problems like ingrown nails or infections. Regular pedicures help maintain foot health and can prevent more serious problems.',
                'pronunciation': '/ˈpɛdɪˌkjʊr/',
                'pronunciation_ipa': '/ˈpɛdɪˌkjʊr/',
                'etymology': 'From Latin "pes, pedis" meaning foot + French "cure" meaning care. Literally means "foot care."',
                'memory_tip': 'PEDICURE = PEDI (foot) + CURE. Think of a "cure" or treatment for your "feet" to make them healthy and attractive.',
                'example_sentence': 'She scheduled a _____ before her beach vacation to ensure her feet looked their best in sandals.'
            },
            'pedigree': {
                'definition': 'The recorded ancestry or lineage of an animal, especially a purebred; a person\'s background or history of achievements; a genealogical chart showing ancestry. In animal breeding, pedigrees document bloodlines to maintain breed standards and predict traits. Human pedigrees trace family history for medical, genealogical, or social purposes. The term can refer to distinguished background or credentials in professional contexts. Pedigree information helps assess quality, value, and characteristics based on ancestral records. The concept emphasizes the importance of documented lineage in establishing identity and worth.',
                'pronunciation': '/ˈpɛdɪˌɡri/',
                'pronunciation_ipa': '/ˈpɛdɪˌɡri/',
                'etymology': 'From Old French "pied de grue" meaning crane\'s foot, referring to the branching lines of genealogical charts resembling bird feet.',
                'memory_tip': 'PEDIGREE = PEDI (foot) + GREE (crane). Think of a "crane\'s foot" shape - the branching family tree showing ancestry.',
                'example_sentence': 'The champion dog\'s _____ showed three generations of award-winning ancestors.'
            },
            'peekaboo': {
                'definition': 'A simple game played with babies and young children involving hiding one\'s face and then suddenly revealing it while saying "peekaboo"; used to describe something that alternately hides and reveals itself. The game helps develop object permanence in infants and provides entertainment through surprise and repetition. In fashion, peekaboo refers to garments with strategic openings that reveal glimpses of skin. The term describes any alternating pattern of concealment and revelation. The game\'s universal appeal across cultures demonstrates fundamental aspects of human development and play.',
                'pronunciation': '/ˈpikəˌbu/',
                'pronunciation_ipa': '/ˈpikəˌbu/',
                'etymology': 'Onomatopoetic combination of "peek" (to look quickly) + "boo" (exclamation used to startle). Reflects the sounds made during the game.',
                'memory_tip': 'PEEKABOO = PEEK + A + BOO. Think of "peeking" at a baby and saying "boo!" to surprise them in the classic game.',
                'example_sentence': 'The grandmother played _____ with her granddaughter, delighting in the child\'s giggles and squeals.'
            },
            'peel': {
                'definition': 'To remove the outer layer or skin from something; the outer covering of fruits or vegetables that is removed before eating; to come off in layers or strips. Peeling fruits and vegetables removes inedible or undesirable outer layers. Paint peels when it loses adhesion to surfaces. Sunburned skin peels as it heals. The process can be gradual or sudden, intentional or natural. Different tools and techniques are used for peeling various materials. Understanding when and how to peel items is important in cooking, maintenance, and health care.',
                'pronunciation': '/pil/',
                'pronunciation_ipa': '/pil/',
                'etymology': 'From Old English "pilian" meaning to strip or remove the outer layer. Related to the concept of plucking or pulling away.',
                'memory_tip': 'PEEL sounds like "PILL" - think of removing the outer layer like taking off a pill\'s coating to get to what\'s inside.',
                'example_sentence': 'She used a sharp knife to carefully _____ the apples for the homemade pie.'
            },
            'peerless': {
                'definition': 'Having no equal; unmatched or incomparable in excellence, quality, or achievement; without peer or rival. Peerless describes something or someone that stands alone at the highest level of their category. The term suggests not just superiority but the absence of any comparable competition. Peerless achievements represent pinnacles of human accomplishment in various fields. The concept implies both objective excellence and the absence of credible alternatives. Recognition as peerless typically requires sustained demonstration of exceptional quality over time.',
                'pronunciation': '/ˈpɪrləs/',
                'pronunciation_ipa': '/ˈpɪrləs/',
                'etymology': 'From "peer" (equal or match) + "-less" suffix meaning without. Literally means "without equal."',
                'memory_tip': 'PEERLESS = PEER + LESS. Think of being "less" than others in having "peers" - so excellent that no one equals you.',
                'example_sentence': 'The violinist\'s _____ technique earned her recognition as the finest performer of her generation.'
            },
            'peevish': {
                'definition': 'Easily irritated or annoyed; showing impatience or bad temper over minor matters; querulous or petulant. Peevish behavior involves expressing dissatisfaction or irritation in ways that seem disproportionate to the cause. The mood can be temporary (due to fatigue or stress) or a more permanent personality trait. Peevish responses often alienate others and create unnecessary conflict. Understanding the sources of peevishness - whether physical, emotional, or situational - can help in managing and responding to such behavior constructively.',
                'pronunciation': '/ˈpivɪʃ/',
                'pronunciation_ipa': '/ˈpivɪʃ/',
                'etymology': 'From Middle English "pevish," possibly from "peevish" meaning spiteful, of uncertain origin. May relate to expressing spite or ill humor.',
                'memory_tip': 'PEEVISH sounds like "PEE-VISH" - think of someone who gets annoyed about everything, like they need to "pee" but are being "vicious" about it.',
                'example_sentence': 'The child became _____ when tired, complaining about everything and refusing to cooperate.'
            },
            'pejerrey': {
                'definition': 'A type of silverside fish found in South American waters, particularly Argentina and Chile, highly prized for its delicate flavor and sporting qualities. Pejerrey are important both commercially and recreationally in South American fisheries. These fish inhabit coastal and inland waters and are known for their silvery appearance and elongated body shape. They are popular targets for recreational fishing due to their fighting ability and excellent taste. The name reflects the Spanish-speaking regions where these fish are most commonly found and consumed.',
                'pronunciation': '/ˌpeɪhəˈreɪ/',
                'pronunciation_ipa': '/ˌpeɪhəˈreɪ/',
                'etymology': 'From Spanish "pejerrey," meaning king fish or royal fish, reflecting the high regard for this fish in South American cuisine.',
                'memory_tip': 'PEJERREY sounds like "PAY-HER-RAY" - think of "paying" for this prized South American fish that\'s like a silvery "ray" of light.',
                'example_sentence': 'The Argentine fisherman was delighted to catch a large _____ during his morning expedition.'
            },
            'pejorate': {
                'definition': 'To make or become worse; to deteriorate in quality, value, or condition; in linguistics, to undergo semantic change where a word develops more negative connotations over time. Pejoration can occur in various contexts including health, relationships, economic conditions, or social situations. In language, words may pejorate as social attitudes change, with previously neutral terms acquiring negative meanings. Understanding pejoration helps recognize decline and potentially take corrective action. The process can be gradual or sudden, temporary or permanent, depending on underlying causes.',
                'pronunciation': '/ˈpɛdʒəˌreɪt/',
                'pronunciation_ipa': '/ˈpɛdʒəˌreɪt/',
                'etymology': 'From Latin "pejoratus," past participle of "pejorare" meaning to make worse, from "pejor" meaning worse.',
                'memory_tip': 'PEJORATE sounds like "PEJ-OR-ATE" - think of something that "ate" its way to being "worse" - deteriorating in quality.',
                'example_sentence': 'The relationship began to _____ after months of poor communication and unresolved conflicts.'
            },
            'pekoe': {
                'definition': 'A grade of black tea made from young leaves and buds, characterized by its high quality and distinctive flavor; specifically, the larger, more mature leaves used in certain tea blends. Pekoe represents a specific leaf grade in tea classification systems, particularly for Ceylon and Indian teas. The term is part of a grading system that includes Orange Pekoe, Broken Orange Pekoe, and other classifications based on leaf size and quality. Pekoe teas are prized for their balance of flavor and body. Understanding tea grades helps consumers select appropriate teas for different preferences and uses.',
                'pronunciation': '/ˈpiˌkoʊ/',
                'pronunciation_ipa': '/ˈpiˌkoʊ/',
                'etymology': 'From Chinese "bai hao" meaning white down, referring to the fine white hairs on young tea buds. Adopted into English through colonial trade.',
                'memory_tip': 'PEKOE sounds like "PEE-KOH" - think of "peeking" at the fine "ko" (high-quality) tea leaves with white down.',
                'example_sentence': 'The tea connoisseur preferred Orange _____ for its robust flavor and aromatic qualities.'
            },
            'pelagial': {
                'definition': 'Relating to or living in the open ocean, away from the shore and sea bottom; pertaining to the pelagic zone of marine environments. Pelagial organisms include fish, marine mammals, plankton, and other creatures that inhabit the water column rather than coastal or bottom areas. This zone represents the largest habitat on Earth and supports diverse marine ecosystems. Pelagial environments are characterized by limited shelter, vast distances, and varying light and pressure conditions. Understanding pelagial ecology is crucial for marine conservation, fisheries management, and climate research.',
                'pronunciation': '/pəˈleɪdʒəl/',
                'pronunciation_ipa': '/pəˈleɪdʒəl/',
                'etymology': 'From Greek "pelagios" meaning of the sea, from "pelagos" meaning open sea. The suffix "-al" indicates relating to or characterized by.',
                'memory_tip': 'PELAGIAL = PELAG (sea) + IAL (relating to). Think of things "relating to" the open "sea" - ocean-dwelling creatures.',
                'example_sentence': 'The research vessel studied _____ species that migrate vertically through different ocean depths.'
            },
            'pelerine': {
                'definition': 'A woman\'s cape or cloak, typically short and covering the shoulders; a type of fur or fabric collar attached to garments. Pelerines were popular in 18th and 19th-century women\'s fashion, providing warmth and modesty while maintaining elegance. The garment style varies from simple shoulder coverings to more elaborate capes with decorative elements. Modern fashion occasionally revives pelerine styles for formal or vintage-inspired clothing. The term also applies to similar cape-like accessories in clerical or academic dress. Understanding historical fashion terms helps in costume design and fashion history.',
                'pronunciation': '/ˌpɛlərˈin/',
                'pronunciation_ipa': '/ˌpɛlərˈin/',
                'etymology': 'From French "pèlerine," from "pèlerin" meaning pilgrim, as such capes were worn by pilgrims. Related to practical travel clothing.',
                'memory_tip': 'PELERINE sounds like "PILL-ER-REEN" - think of a "pill" of fabric that "covers" like a cape, "reining" in your shoulders.',
                'example_sentence': 'The Victorian lady wore a velvet _____ over her evening gown for warmth during the carriage ride.'
            },
            'pelf': {
                'definition': 'Money or wealth, especially when obtained dishonestly or viewed with disdain; material riches regarded as base or contemptible. The term often carries negative connotations, suggesting wealth gained through questionable means or excessive focus on material gain. Pelf emphasizes the corrupting or degrading aspects of money-seeking behavior. Literature and moral discourse use the term to critique materialism and greed. The concept reflects tensions between spiritual values and material prosperity. Understanding pelf helps recognize discussions about the proper relationship between virtue and wealth.',
                'pronunciation': '/pɛlf/',
                'pronunciation_ipa': '/pɛlf/',
                'etymology': 'From Old French "pelfre" meaning booty or spoils. Originally referred to stolen goods or ill-gotten gains.',
                'memory_tip': 'PELF sounds like "SELF" - think of money gained for "self"ish purposes, often through dishonest means.',
                'example_sentence': 'The novel\'s villain was motivated solely by _____, caring nothing for honor or human dignity.'
            },
            'pelican': {
                'definition': 'A large water bird with a distinctive pouch beneath its long bill for catching and holding fish; known for its impressive diving or surface-feeding behavior. Pelicans are found near coastal and inland waters worldwide and are recognized for their unique bill structure and feeding methods. Different species employ various fishing techniques, from spectacular diving from heights to cooperative surface feeding. Pelicans play important roles in marine ecosystems and have cultural significance in many societies. Conservation efforts have helped several pelican species recover from population declines.',
                'pronunciation': '/ˈpɛlɪkən/',
                'pronunciation_ipa': '/ˈpɛlɪkən/',
                'etymology': 'From Greek "pelekan," possibly related to "pelekys" meaning axe, referring to the bird\'s bill shape.',
                'memory_tip': 'PELICAN sounds like "PELI-CAN" - think of a bird that "can" carry fish in its "peli" (pouch) - the distinctive fishing bird.',
                'example_sentence': 'The brown _____ dove gracefully into the water and emerged with a fish in its expandable pouch.'
            },
            'pelisse': {
                'definition': 'A long cloak or coat, typically lined or trimmed with fur; historically, a woman\'s long coat or a military officer\'s ornamental jacket. Pelisses were fashionable in 18th and 19th-century European clothing, providing both warmth and style. Military pelisses often featured elaborate braiding, fur trim, and decorative elements indicating rank or regiment. The civilian version was a practical outerwear garment that could be elegant enough for formal occasions. Understanding historical clothing terms helps in period costume design, fashion history, and literature interpretation.',
                'pronunciation': '/pəˈlis/',
                'pronunciation_ipa': '/pəˈlis/',
                'etymology': 'From French "pelisse," from Medieval Latin "pellicia" meaning fur garment, from "pellis" meaning skin or hide.',
                'memory_tip': 'PELISSE sounds like "PEL-LEASE" - think of "pelts" (fur) that "lease" warmth to your body in a long coat.',
                'example_sentence': 'The military officer\'s ornate _____ distinguished him from the regular soldiers during the formal ceremony.'
            },
            'pell': {
                'definition': 'A skin or hide, especially one prepared for use; in "pell-mell," meaning in a hasty, disorderly manner. As a standalone word, pell refers to animal skins used for various purposes including parchment, clothing, or trade. The term appears most commonly in the phrase "pell-mell," describing chaotic, hurried, or confused action. Historical documents and trade records often mention pelts and pells as valuable commodities. Understanding the term helps in reading historical texts and understanding medieval commerce and craft practices.',
                'pronunciation': '/pɛl/',
                'pronunciation_ipa': '/pɛl/',
                'etymology': 'From Old French "pel," from Latin "pellis" meaning skin or hide. Related to "pelt" and other skin-related terms.',
                'memory_tip': 'PELL sounds like "PELT" - think of animal "pelts" or skins, especially when they\'re prepared for use.',
                'example_sentence': 'The medieval merchant traded in _____ and other animal products throughout the European markets.'
            },
            'pellet': {
                'definition': 'A small, rounded mass of compressed material; a small ball of food given to animals; ammunition for air guns; a small pill or medicinal tablet. Pellets are created by compression, forming materials into dense, uniform shapes for various purposes. Animal feed pellets provide concentrated nutrition in easily consumable form. Industrial pellets serve as raw materials for manufacturing processes. Medical pellets allow controlled drug release. The compact form offers advantages in storage, transport, and controlled delivery of materials or substances.',
                'pronunciation': '/ˈpɛlət/',
                'pronunciation_ipa': '/ˈpɛlət/',
                'etymology': 'From Old French "pelote" meaning small ball, from Latin "pila" meaning ball. Diminutive form emphasizing small size.',
                'memory_tip': 'PELLET sounds like "PEL-LET" - think of a small "pebble" that you "let" animals eat, or small compressed balls.',
                'example_sentence': 'The rabbit eagerly ate the nutritious _____ from the feeder in its cage.'
            },
            'pembroke': {
                'definition': 'A breed of small herding dog, specifically the Pembroke Welsh Corgi, characterized by short legs, fox-like face, and lack of tail; also refers to Pembroke County in Wales. Pembroke Welsh Corgis are intelligent, active dogs originally bred for herding cattle despite their small stature. They are known for their loyalty, trainability, and distinctive appearance. The breed has gained popularity partly due to Queen Elizabeth II\'s well-known affection for these dogs. Pembrokes differ from Cardigan Welsh Corgis primarily in tail length and slightly different body proportions.',
                'pronunciation': '/ˈpɛmˌbrʊk/',
                'pronunciation_ipa': '/ˈpɛmˌbrʊk/',
                'etymology': 'Named after Pembrokeshire, Wales, where this variety of Welsh Corgi was developed. The place name has Celtic origins.',
                'memory_tip': 'PEMBROKE sounds like "PEM-BROKE" - think of the small Welsh dog that "broke" expectations by herding cattle despite short legs.',
                'example_sentence': 'The Queen\'s favorite _____ Corgi accompanied her on many official engagements throughout her reign.'
            },
            'penchant': {
                'definition': 'A strong inclination, liking, or preference for something; a habitual tendency toward particular behavior or activity. Penchants represent more than casual interest - they indicate consistent, often irresistible attraction to specific things or activities. People may have penchants for certain foods, activities, styles, or behaviors. The term suggests an almost involuntary leaning toward something, often based on personality, experience, or natural inclination. Understanding penchants helps predict behavior and preferences in various contexts including career choices, relationships, and lifestyle decisions.',
                'pronunciation': '/ˈpɛntʃənt/',
                'pronunciation_ipa': '/ˈpɛntʃənt/',
                'etymology': 'From French "penchant," present participle of "pencher" meaning to lean or incline. Literally means "leaning toward."',
                'memory_tip': 'PENCHANT sounds like "PEN-CHANT" - think of a strong "chant" for your "pen" - an irresistible preference or inclination.',
                'example_sentence': 'She had a _____ for vintage jewelry and spent hours browsing antique shops.'
            },
            'pencil': {
                'definition': 'A writing or drawing instrument consisting of a thin rod of graphite or colored material encased in wood, plastic, or metal; to write, draw, or mark with such an instrument. Pencils are fundamental tools for education, art, and communication. Different types include graphite pencils for writing, colored pencils for art, and mechanical pencils for precision work. The graphite core can be erased, making pencils ideal for drafts and corrections. Pencil manufacturing involves precise engineering to ensure consistent performance. The tool remains essential despite digital alternatives.',
                'pronunciation': '/ˈpɛnsəl/',
                'pronunciation_ipa': '/ˈpɛnsəl/',
                'etymology': 'From Old French "pincel," from Latin "penicillus" meaning little tail or brush, diminutive of "penis" meaning tail.',
                'memory_tip': 'PENCIL sounds like "PEN-SILL" - think of a "pen" that\'s as simple as a "sill" (basic) but essential for writing.',
                'example_sentence': 'The student carefully sharpened her _____ before beginning the important exam.'
            },
            'pendeloque': {
                'definition': 'A pear-shaped gemstone or ornament, typically used in jewelry; a pendant or drop-shaped decorative element. Pendeloques are characterized by their distinctive teardrop shape, wider at the top and tapering to a point at the bottom. This cut maximizes the stone\'s brilliance and creates elegant movement in jewelry pieces. The shape is commonly used for earrings, pendants, and chandelier crystals. Different gemstones can be cut in pendeloque style, each creating unique optical effects. The term is important in jewelry design and gemology for describing specific cut shapes.',
                'pronunciation': '/ˈpɛndəˌlɔk/',
                'pronunciation_ipa': '/ˈpɛndəˌlɔk/',
                'etymology': 'From French "pendeloque," related to "pendre" meaning to hang. Refers to the hanging, pendant-like shape of the cut.',
                'memory_tip': 'PENDELOQUE sounds like "PENDEL-LOGUE" - think of a "pendant" that "logs" (hangs) beautifully in a teardrop shape.',
                'example_sentence': 'The antique earrings featured stunning diamond _____ that caught the light with every movement.'
            },
            'pendentive': {
                'definition': 'A curved triangular architectural element that enables the transition from a square or polygonal base to a circular dome above; a structural feature that transfers the weight of a dome to supporting pillars. Pendentives are essential in Byzantine and Islamic architecture, allowing domes to be placed over square spaces. They create smooth visual and structural transitions while distributing loads effectively. The curved surfaces often feature decorative elements including mosaics, paintings, or relief work. Understanding pendentives is crucial for studying historical architecture and dome construction techniques.',
                'pronunciation': '/pɛnˈdɛntɪv/',
                'pronunciation_ipa': '/pɛnˈdɛntɪv/',
                'etymology': 'From Latin "pendens" meaning hanging, referring to how these elements appear to hang from the dome structure.',
                'memory_tip': 'PENDENTIVE = PENDENT (hanging) + IVE. Think of architectural elements that appear to "hang" and support domes above.',
                'example_sentence': 'The cathedral\'s massive dome was supported by four ornately decorated _____ at each corner.'
            },
            'pending': {
                'definition': 'Awaiting a decision, settlement, or completion; remaining undecided or unsettled; in preparation; about to happen. Pending indicates a temporary state while waiting for resolution or action. Legal cases may be pending trial, applications pending approval, or decisions pending review. The term suggests active consideration rather than abandonment or delay. Pending matters often require attention, follow-up, or decision-making. Understanding pending status helps manage expectations and prioritize actions in business, legal, and personal contexts.',
                'pronunciation': '/ˈpɛndɪŋ/',
                'pronunciation_ipa': '/ˈpɛndɪŋ/',
                'etymology': 'From Latin "pendere" meaning to hang or be suspended. Suggests something hanging in the balance, awaiting resolution.',
                'memory_tip': 'PENDING sounds like "PEN-DING" - think of a "pen" that\'s "dinging" (waiting) to write the final decision that\'s still awaiting.',
                'example_sentence': 'The merger remained _____ regulatory approval from government agencies.'
            }
        }
        
        return word_data.get(word, {
            'definition': f'[Definition for {word} not found in comprehensive dataset]',
            'pronunciation': f'[Pronunciation for {word} not available]',
            'pronunciation_ipa': f'[IPA for {word} not available]',
            'etymology': f'[Etymology for {word} not available]',
            'memory_tip': f'[Memory tip for {word} not available]',
            'example_sentence': f'[Example sentence for {word} not available]'
        })

def process_batch_129():
    processor = Batch129Processor()
    
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_129_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_129_processed.csv'
    
    combined_words = processor.detect_combined_words()
    if combined_words:
        logging.warning(f"Detected combined words that need manual review: {combined_words}")
    
    processed_data = []
    successful_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            word = row['word'].strip()
            if not word:
                continue
                
            try:
                claude_data = processor.get_comprehensive_claude_data(word)
                
                if claude_data['definition'] != f'[Definition for {word} not found in comprehensive dataset]':
                    difficulty_scores = processor.difficulty_calc.calculate_difficulty_score(
                        word, claude_data['definition'], claude_data['etymology']
                    )
                    
                    processed_row = {
                        'word': word,
                        'years': row['years'],
                        'source_files': row['source_files'],
                        'source_difficulties': row['source_difficulties'],
                        'definition': claude_data['definition'],
                        'pronunciation': claude_data['pronunciation'],
                        'pronunciation_ipa': claude_data['pronunciation_ipa'],
                        'etymology': claude_data['etymology'],
                        'memory_tip': claude_data['memory_tip'],
                        'example_sentence': claude_data['example_sentence'],
                        'phonetic_transparency_score': difficulty_scores['phonetic_transparency_score'],
                        'word_frequency_score': difficulty_scores['word_frequency_score'],
                        'morphological_complexity_score': difficulty_scores['morphological_complexity_score'],
                        'etymology_complexity_score': difficulty_scores['etymology_complexity_score'],
                        'difficulty': difficulty_scores['difficulty'],
                        'combined_word_error': word in combined_words,
                        'source': 'Claude'
                    }
                    
                    processed_data.append(processed_row)
                    successful_count += 1
                    logging.info(f"Successfully processed word {successful_count}: {word}")
                else:
                    logging.error(f"No data found for word: {word}")
                    
            except Exception as e:
                logging.error(f"Error processing word '{word}': {str(e)}")
    
    fieldnames = [
        'word', 'years', 'source_files', 'source_difficulties', 'definition',
        'pronunciation', 'pronunciation_ipa', 'etymology', 'memory_tip', 'example_sentence',
        'phonetic_transparency_score', 'word_frequency_score', 'morphological_complexity_score',
        'etymology_complexity_score', 'difficulty', 'combined_word_error', 'source'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_data)
    
    logging.info(f"Batch 129 processing complete. Processed {successful_count}/50 words.")
    logging.info(f"Output saved to: {output_file}")
    
    if combined_words:
        logging.warning(f"Combined word errors detected: {combined_words}")
    
    return successful_count

if __name__ == "__main__":
    process_batch_129()