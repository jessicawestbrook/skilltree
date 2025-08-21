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

class Batch128Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        self.combined_words = []
        
    def detect_combined_words(self) -> List[str]:
        combined_patterns = [
            'parsleydifficulty',
            'pashminautilitarian'
        ]
        return combined_patterns
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        word_data = {
            'parsec': {
                'definition': 'A unit of astronomical distance equal to approximately 3.26 light-years or 206,265 astronomical units. The parsec is defined as the distance at which one astronomical unit subtends an angle of one arcsecond. This measurement is fundamental in astronomy for expressing distances to stars and galaxies. The term combines "parallax" and "arcsecond," reflecting its basis in stellar parallax measurements. Parsecs are preferred over light-years in professional astronomy because they relate directly to observational measurements. Understanding parsecs is essential for comprehending the vast scales of the universe.',
                'pronunciation': '/ˈpɑrsɛk/',
                'pronunciation_ipa': '/ˈpɑrsɛk/',
                'etymology': 'Coined from "parallax" + "arcsecond," referring to the astronomical measurement technique used to determine this distance unit.',
                'memory_tip': 'PARSEC = PARallax + arcSECond. Think of "parsing" space into "seconds" - a way to measure vast astronomical distances.',
                'example_sentence': 'The nearest star to our solar system, Proxima Centauri, is located approximately 1.3 _____ away.'
            },
            'parsimony': {
                'definition': 'Extreme frugality; stinginess; the quality of being unwilling to spend money or resources. In scientific contexts, parsimony refers to the principle of choosing the simplest explanation that accounts for all observations, also known as Occam\'s razor. The concept suggests that simpler theories are generally preferable to more complex ones when both explain the same phenomena equally well. Parsimony can be both a virtue (careful resource management) and a fault (excessive cheapness). The principle appears in philosophy, science, and economics as a guide for decision-making and theory selection.',
                'pronunciation': '/ˈpɑrsəˌmoʊni/',
                'pronunciation_ipa': '/ˈpɑrsəˌmoʊni/',
                'etymology': 'From Latin "parsimonia" meaning frugality or economy, from "parcere" meaning to spare or be frugal. Related to "parse" and "spare."',
                'memory_tip': 'PARSIMONY sounds like "PARSE-MONEY" - think of carefully "parsing" (analyzing) how you spend "money" - extreme frugality.',
                'example_sentence': 'The scientist applied the principle of _____ to choose the theory that explained the data with the fewest assumptions.'
            },
            'parsnips': {
                'definition': 'Root vegetables related to carrots and parsley, characterized by their cream-colored, tapered shape and sweet, nutty flavor. Parsnips are typically harvested in fall and winter when cold weather converts their starches to sugars, enhancing their taste. These vegetables are rich in vitamins, minerals, and fiber, making them nutritious additions to various dishes. Parsnips can be roasted, mashed, or used in soups and stews. They have been cultivated in Europe since ancient times and were a dietary staple before potatoes became common. Modern cuisine values parsnips for their unique flavor and versatility.',
                'pronunciation': '/ˈpɑrsnɪps/',
                'pronunciation_ipa': '/ˈpɑrsnɪps/',
                'etymology': 'From Middle English "pasnepe," from Old French "pasnaise," from Latin "pastinaca." The name evolved through various linguistic influences.',
                'memory_tip': 'PARSNIPS sounds like "PARSE-NIPS" - think of "parsing" (peeling) these root vegetables that "nip" at your taste buds with sweetness.',
                'example_sentence': 'The chef roasted _____ with carrots and potatoes, creating a colorful and flavorful side dish.'
            },
            'parterre': {
                'definition': 'A formal garden design featuring intricate patterns created with low hedges, flowers, and colored gravel or sand; the main floor of a theater containing the orchestra and front seating sections. In garden design, parterres originated in 16th-century France and became characteristic of formal European gardens. These elaborate patterns are best viewed from elevated positions like terraces or upper-story windows. Theater parterres refer to the ground-level seating area, typically the most expensive section closest to the stage. Both meanings emphasize organized, decorative arrangements designed for optimal viewing and aesthetic impact.',
                'pronunciation': '/pɑrˈtɛr/',
                'pronunciation_ipa': '/pɑrˈtɛr/',
                'etymology': 'From French "parterre," from "par" (on) + "terre" (ground). Literally means "on the ground," referring to ground-level gardens or theater seating.',
                'memory_tip': 'PARTERRE = PAR (on) + TERRE (ground). Think of elaborate patterns "on the ground" in formal gardens or ground-level theater seating.',
                'example_sentence': 'The palace garden featured an elaborate _____ with geometric patterns of boxwood hedges and colorful flowers.'
            },
            'parti': {
                'definition': 'In architecture, a basic design concept or organizing idea that guides the overall layout and form of a building; the fundamental design approach or strategy. The parti represents the essential organizing principle that determines how spaces relate to each other and how the building responds to its site and program. Architectural education emphasizes developing strong parti concepts as the foundation for successful designs. A clear parti helps ensure coherent, purposeful architecture rather than arbitrary arrangements. The concept can be expressed through diagrams, sketches, or simple statements that capture the design\'s core idea.',
                'pronunciation': '/pɑrˈti/',
                'pronunciation_ipa': '/pɑrˈti/',
                'etymology': 'From French "parti" meaning decision or choice, from "partir" meaning to divide or depart. In architecture, refers to the fundamental design decision.',
                'memory_tip': 'PARTI sounds like "PARTY" - think of the main organizing idea for a "party" that determines how everything else is arranged.',
                'example_sentence': 'The architect\'s _____ for the library emphasized bringing natural light into reading areas through a central atrium.'
            },
            'partiality': {
                'definition': 'Unfair bias or favoritism toward particular people, groups, or ideas; a special fondness or preference for something. Partiality involves making judgments or decisions based on personal preferences rather than objective criteria. In legal and professional contexts, partiality is considered problematic because it undermines fairness and impartiality. However, having partialities or preferences is natural in personal relationships and aesthetic choices. The term can describe both inappropriate bias in formal situations and legitimate personal preferences in informal contexts. Understanding partiality is important for maintaining ethical standards in decision-making roles.',
                'pronunciation': '/ˌpɑrʃiˈæləti/',
                'pronunciation_ipa': '/ˌpɑrʃiˈæləti/',
                'etymology': 'From "partial" (from Latin "partialis" meaning of or relating to a part) + "-ity" suffix indicating quality or state.',
                'memory_tip': 'PARTIALITY = PARTIAL + ITY. Think of the "quality" of being "partial" - showing unfair bias or special preference.',
                'example_sentence': 'The judge recused herself from the case due to her _____ toward one of the defendants.'
            },
            'participants': {
                'definition': 'People who take part in an activity, event, study, or process; individuals who actively engage in something rather than merely observing. Participants can be volunteers, subjects, competitors, attendees, or contributors depending on the context. In research, participants provide data through surveys, interviews, or experiments. In events, participants engage actively rather than serving as passive audience members. The term emphasizes active involvement and contribution to whatever activity is taking place. Legal and ethical considerations often govern how participants are recruited, treated, and compensated.',
                'pronunciation': '/pɑrˈtɪsəpənts/',
                'pronunciation_ipa': '/pɑrˈtɪsəpənts/',
                'etymology': 'From "participate" (from Latin "participatus," past participle of "participare" meaning to share in) + "-ant" suffix meaning one who does.',
                'memory_tip': 'PARTICIPANTS = PARTICIPATE + ANTS. Think of busy "ants" who actively "participate" in group activities.',
                'example_sentence': 'The research study recruited 200 _____ to test the effectiveness of the new medication.'
            },
            'participate': {
                'definition': 'To take part in an activity or event; to have a share or role in something; to join with others in doing something. Participation involves active engagement rather than passive observation. The level of participation can vary from minimal involvement to full engagement depending on the situation and individual choice. Effective participation often requires preparation, commitment, and willingness to contribute. In democratic societies, citizen participation in government and community activities is considered essential for healthy civic life. Schools and organizations often encourage participation to foster learning, teamwork, and community building.',
                'pronunciation': '/pɑrˈtɪsəˌpeɪt/',
                'pronunciation_ipa': '/pɑrˈtɪsəˌpeɪt/',
                'etymology': 'From Latin "participare" meaning to share in, from "particeps" meaning sharing, from "pars" (part) + "capere" (to take).',
                'memory_tip': 'PARTICIPATE = PARTI (part) + CIPATE (take). Think of "taking part" in activities - actively engaging rather than just watching.',
                'example_sentence': 'Students are encouraged to _____ in extracurricular activities to develop leadership skills.'
            },
            'participated': {
                'definition': 'Past tense of participate; took part in an activity, event, or process; engaged actively in something that has already occurred. The word indicates completed involvement in activities ranging from casual events to formal programs. Participated suggests the person was an active contributor rather than a passive observer. In academic and professional contexts, having participated in certain activities may indicate experience, skills, or qualifications. Documentation of participation often serves as evidence of engagement, learning, or achievement in various settings.',
                'pronunciation': '/pɑrˈtɪsəˌpeɪtəd/',
                'pronunciation_ipa': '/pɑrˈtɪsəˌpeɪtəd/',
                'etymology': 'Past tense of "participate," from Latin "participatus." The "-ed" suffix indicates completed action in the past.',
                'memory_tip': 'PARTICIPATED = PARTICIPATE + ED. Think of having already "taken part" in something - completed active involvement.',
                'example_sentence': 'She _____ in the marathon last year and plans to run again this year.'
            },
            'particular': {
                'definition': 'Specific or individual rather than general; distinctive or notable; especially concerned with details or precision; having strong preferences or being hard to please. The word emphasizes specificity and distinctiveness from general categories. Particular people pay careful attention to details and may have exacting standards. In logic and language, particular statements refer to specific cases rather than universal claims. The term can describe both positive traits (attention to detail) and potentially negative ones (being overly fussy). Understanding the particular versus the general is fundamental to clear thinking and communication.',
                'pronunciation': '/pərˈtɪkjələr/',
                'pronunciation_ipa': '/pərˈtɪkjələr/',
                'etymology': 'From Latin "particularis" meaning of or concerning a part, from "particula" meaning small part. Related to "particle" and "part."',
                'memory_tip': 'PARTICULAR = PARTI (part) + CULAR. Think of focusing on a specific "part" rather than the whole - being precise about details.',
                'example_sentence': 'The chef was _____ about the quality of ingredients used in his signature dishes.'
            },
            'particulate': {
                'definition': 'Relating to or consisting of separate particles; existing as or containing small, discrete particles suspended in air or liquid. Particulate matter is a major air pollution concern, consisting of tiny solid or liquid particles that can be harmful when inhaled. These particles come from various sources including vehicle emissions, industrial processes, and natural phenomena like dust storms. Environmental regulations often specify limits for particulate concentrations to protect public health. The size of particulate matter affects its behavior and health impacts, with smaller particles generally being more dangerous.',
                'pronunciation': '/pɑrˈtɪkjələt/',
                'pronunciation_ipa': '/pɑrˈtɪkjələt/',
                'etymology': 'From "particle" (from Latin "particula" meaning small part) + "-ate" suffix meaning characterized by or having.',
                'memory_tip': 'PARTICULATE = PARTICLE + ATE. Think of matter that\'s made up of tiny "particles" - small bits suspended in air or water.',
                'example_sentence': 'The air quality monitor detected high levels of _____ matter during the wildfire season.'
            },
            'partner': {
                'definition': 'A person who shares in an activity, business, or relationship with another; one of two or more people who work together or are associated in some enterprise. Partners can be business associates, romantic companions, dance partners, or collaborators in various endeavors. The relationship typically involves shared responsibilities, risks, benefits, and decision-making. Legal partnerships have specific rights and obligations defined by law or contract. Successful partnerships require communication, trust, complementary skills, and aligned goals. The concept extends from personal relationships to business arrangements and professional collaborations.',
                'pronunciation': '/ˈpɑrtnər/',
                'pronunciation_ipa': '/ˈpɑrtnər/',
                'etymology': 'From Middle English "parcener," from Anglo-French, from "parçon" meaning share or part. Related to "partition" and sharing.',
                'memory_tip': 'PARTNER = PART + NER. Think of someone who shares "part" of your life or business - a person who takes part with you.',
                'example_sentence': 'The law firm promoted her to _____ after she demonstrated exceptional legal expertise and client development skills.'
            },
            'partridge': {
                'definition': 'A medium-sized ground-dwelling game bird related to quail and pheasant, known for its plump body, short tail, and tendency to run rather than fly when threatened. Partridges are found across Europe, Asia, and Africa, with some species introduced to North America. These birds prefer grasslands, farmlands, and scrublands where they feed on seeds, insects, and vegetation. Partridges are popular game birds and appear frequently in literature and folklore. They typically nest on the ground and are known for their distinctive calls. Some species are raised commercially for hunting and food.',
                'pronunciation': '/ˈpɑrtrɪdʒ/',
                'pronunciation_ipa': '/ˈpɑrtrɪdʒ/',
                'etymology': 'From Old French "pertriz," from Latin "perdix," from Greek "perdix." The name has remained relatively stable across languages.',
                'memory_tip': 'PARTRIDGE sounds like "PART-RIDGE" - think of a bird that\'s "part" of the "ridge" or hillside where it lives and nests.',
                'example_sentence': 'The hunters spotted a covey of _____ feeding in the wheat field at dawn.'
            },
            'parts': {
                'definition': 'Portions or pieces of a whole; components that make up a larger entity; sections or divisions of something; roles in a play or performance. Parts can be physical components of machines, sections of documents, or abstract divisions of concepts. In theater, parts refer to the roles that actors play. In mechanics, parts are the individual components that work together to make machines function. Understanding how parts relate to wholes is fundamental to analysis, repair, construction, and comprehension across many fields.',
                'pronunciation': '/pɑrts/',
                'pronunciation_ipa': '/pɑrts/',
                'etymology': 'Plural of "part," from Old French "part," from Latin "pars, partis" meaning portion or share. Basic concept of division and sharing.',
                'memory_tip': 'PARTS is simply the plural of PART - think of multiple pieces that make up a whole, like car parts or parts of a story.',
                'example_sentence': 'The mechanic ordered replacement _____ for the engine repair from the manufacturer.'
            },
            'parturient': {
                'definition': 'Relating to or in the process of giving birth; about to give birth or in labor. The term is primarily used in medical and veterinary contexts to describe the condition of females during the birthing process. Parturient animals or humans require special care and attention due to the physical demands and potential complications of labor and delivery. Understanding parturient physiology is crucial for healthcare providers, veterinarians, and livestock managers. The word emphasizes the active process of birth rather than just pregnancy.',
                'pronunciation': '/pɑrˈtʊriənt/',
                'pronunciation_ipa': '/pɑrˈtʊriənt/',
                'etymology': 'From Latin "parturient-" meaning being in labor, from "parturire" meaning to be in labor, from "parere" meaning to give birth.',
                'memory_tip': 'PARTURIENT sounds like "PART-YOUR-ENT" - think of the birthing process as "parting" or opening to bring forth new life.',
                'example_sentence': 'The veterinarian monitored the _____ mare carefully throughout the difficult delivery.'
            },
            'party': {
                'definition': 'A social gathering for celebration or entertainment; a political organization; a group of people involved in a particular activity; one of the sides in a legal agreement or dispute. Social parties bring people together for enjoyment, celebration, or socialization. Political parties organize people with similar ideologies to seek political power. In legal contexts, parties are the individuals or entities involved in contracts or lawsuits. The word emphasizes group participation and shared purpose, whether for fun, politics, or formal business.',
                'pronunciation': '/ˈpɑrti/',
                'pronunciation_ipa': '/ˈpɑrti/',
                'etymology': 'From Old French "partie," from "partir" meaning to divide or share. Originally meant a part or portion of something.',
                'memory_tip': 'PARTY comes from "part" - think of being "part" of a group, whether for celebration, politics, or legal matters.',
                'example_sentence': 'The surprise _____ brought together friends and family to celebrate her graduation.'
            },
            'parvo': {
                'definition': 'Short for parvovirus, a highly contagious viral infection affecting dogs, particularly puppies, causing severe gastrointestinal symptoms and potentially death. Parvovirus attacks rapidly dividing cells, particularly in the intestinal tract and bone marrow. The disease spreads through contact with infected fecal matter and contaminated environments. Vaccination is the primary prevention method, typically starting in puppyhood with booster shots. Treatment involves supportive care including fluid therapy and anti-nausea medications. The virus is extremely hardy and can survive in the environment for long periods.',
                'pronunciation': '/ˈpɑrvoʊ/',
                'pronunciation_ipa': '/ˈpɑrvoʊ/',
                'etymology': 'Shortened from "parvovirus," from Latin "parvus" meaning small + "virus." Named for the small size of the virus particles.',
                'memory_tip': 'PARVO sounds like "PAR-VOW" - think of making a "vow" to keep puppies safe from this serious viral disease.',
                'example_sentence': 'The veterinarian recommended immediate vaccination to protect the puppy from _____ and other dangerous diseases.'
            },
            'paschal': {
                'definition': 'Relating to Passover or Easter; associated with the springtime religious celebrations of Judaism and Christianity. Paschal refers to the commemoration of liberation and redemption central to both faiths. In Judaism, paschal relates to Passover, celebrating the Israelites\' exodus from Egypt. In Christianity, paschal refers to Easter, celebrating the resurrection of Jesus Christ. The term encompasses liturgical seasons, special foods, customs, and theological themes of sacrifice, deliverance, and new life. Paschal celebrations typically occur in spring, symbolizing renewal and spiritual rebirth.',
                'pronunciation': '/ˈpæskəl/',
                'pronunciation_ipa': '/ˈpæskəl/',
                'etymology': 'From Late Latin "paschalis," from "pascha" meaning Passover or Easter, from Greek "pascha," from Hebrew "pesach" meaning Passover.',
                'memory_tip': 'PASCHAL sounds like "PASS-CAL" - think of "passing" over to celebrate the religious "call" of Easter or Passover.',
                'example_sentence': 'The church prepared for the _____ season with special liturgies celebrating the resurrection.'
            },
            'pashmina': {
                'definition': 'A fine type of cashmere wool and fabric made from the soft undercoat of the changthangi goat; a shawl or scarf made from this material. Authentic pashmina comes from goats living in the high altitudes of the Himalayas, where extreme temperatures produce exceptionally soft, warm undercoat fibers. The finest pashmina is hand-woven and prized for its lightness, warmth, and luxurious texture. The term is sometimes used more broadly for any soft, lightweight shawl, though true pashmina specifically refers to this particular type of cashmere. These accessories are valued for both their practical warmth and elegant appearance.',
                'pronunciation': '/pæʃˈminə/',
                'pronunciation_ipa': '/pæʃˈminə/',
                'etymology': 'From Persian "pashmina," from "pashm" meaning wool. The word refers to the fine wool of the Himalayan goat.',
                'memory_tip': 'PASHMINA sounds like "PASH-MINA" - think of having a "passion" for "mina" (a soft, luxurious shawl made from fine goat wool).',
                'example_sentence': 'She wrapped the delicate _____ around her shoulders to ward off the evening chill.'
            },
            'pasilla': {
                'definition': 'A variety of chili pepper used in Mexican cuisine, particularly when dried; the dried form of the chilaca pepper, characterized by a dark, wrinkled appearance and mild to moderate heat level. Pasilla peppers have a rich, complex flavor with earthy, fruity notes and mild spice. They are essential ingredients in many traditional Mexican dishes, including mole sauces and various stews. The name "pasilla" means "little raisin" in Spanish, referring to the pepper\'s dark, wrinkled appearance when dried. These peppers are often ground into powder or rehydrated for use in cooking.',
                'pronunciation': '/pəˈsilə/',
                'pronunciation_ipa': '/pəˈsilə/',
                'etymology': 'From Spanish "pasilla," diminutive of "pasa" meaning raisin, referring to the pepper\'s dark, wrinkled appearance when dried.',
                'memory_tip': 'PASILLA sounds like "PASS-ILL-A" - think of "passing" around these "little" peppers that look like dark raisins.',
                'example_sentence': 'The chef soaked the _____ peppers in hot water before blending them into the traditional mole sauce.'
            },
            'pasquinade': {
                'definition': 'A satirical composition, typically anonymous, that ridicules a public figure; a lampoon or satirical writing that mocks political figures or social issues. Pasquinades were historically posted in public places to spread political criticism or social commentary through humor and satire. The form allowed people to express dissent or criticism anonymously, often during periods when direct political opposition was dangerous. These satirical works used wit, irony, and ridicule to expose perceived corruption, incompetence, or hypocrisy. Modern equivalents might include political cartoons, satirical websites, or anonymous social media critiques.',
                'pronunciation': '/ˌpæskwəˈneɪd/',
                'pronunciation_ipa': '/ˌpæskwəˈneɪd/',
                'etymology': 'From French "pasquinade," from Italian "pasquinata," named after Pasquino, a statue in Rome where satirical writings were posted.',
                'memory_tip': 'PASQUINADE sounds like "PASS-QUEEN-AID" - think of "passing" satirical "aid" to criticize the "queen" or other public figures.',
                'example_sentence': 'The political _____ circulated through the city, cleverly mocking the mayor\'s recent policy decisions.'
            },
            'passage': {
                'definition': 'A section of text, music, or other work; a corridor or pathway for movement; the process of moving from one place or state to another; the enactment of legislation. Literary passages are excerpts from books, articles, or speeches used for study or reference. Physical passages include hallways, channels, or routes for travel. The passage of time refers to temporal progression. Legislative passage involves the formal approval of laws. The concept encompasses both physical movement through space and abstract transitions between states or conditions.',
                'pronunciation': '/ˈpæsɪdʒ/',
                'pronunciation_ipa': '/ˈpæsɪdʒ/',
                'etymology': 'From Old French "passage," from "passer" meaning to pass. Related to movement and transition from one place to another.',
                'memory_tip': 'PASSAGE = PASS + AGE. Think of "passing" through different "ages" or stages, or text that "passes" information across time.',
                'example_sentence': 'The students analyzed a difficult _____ from Shakespeare to understand the poet\'s use of metaphor.'
            },
            'passed': {
                'definition': 'Past tense of pass; moved beyond or through something; succeeded in a test or examination; transferred from one person to another; came to an end or elapsed. The word indicates completed action involving movement, achievement, or transition. People pass tests by meeting required standards. Time passes as it moves forward. Objects pass from one location to another. The word emphasizes the completion of movement, transition, or achievement that has already occurred.',
                'pronunciation': '/pæst/',
                'pronunciation_ipa': '/pæst/',
                'etymology': 'Past tense of "pass," from Old French "passer," possibly from Latin "passus" meaning step or pace.',
                'memory_tip': 'PASSED sounds like "PAST" - think of something that has moved into the "past" - completed movement or achievement.',
                'example_sentence': 'She _____ the driving test on her second attempt and received her license immediately.'
            },
            'passersby': {
                'definition': 'People who happen to be walking past a particular place; individuals who are traveling through an area without stopping or having specific business there. Passersby are often casual observers of events, accidents, or activities occurring in public spaces. They may become witnesses to incidents or potential helpers in emergencies. Street performers, vendors, and businesses often depend on attracting the attention of passersby. The term emphasizes the temporary, incidental nature of their presence rather than intentional destination or purpose.',
                'pronunciation': '/ˈpæsərzˌbaɪ/',
                'pronunciation_ipa': '/ˈpæsərzˌbaɪ/',
                'etymology': 'Compound of "passers" (those who pass) + "by" (past). Refers to people who pass by a location.',
                'memory_tip': 'PASSERSBY = PASSERS + BY. Think of people who "pass" "by" a location - casual pedestrians walking past.',
                'example_sentence': 'The street musician attracted the attention of _____ with his energetic performance.'
            },
            'pasta': {
                'definition': 'A food made from unleavened dough of wheat flour mixed with water or eggs, typically formed into various shapes and cooked by boiling. Pasta originated in Italy and has become a staple food worldwide. Common types include spaghetti, penne, linguine, and ravioli, each suited to different sauces and preparations. Pasta can be fresh (made and cooked immediately) or dried (stored for later use). The cooking process involves boiling in salted water until "al dente" (firm to the bite). Pasta serves as the foundation for countless dishes across many cultures.',
                'pronunciation': '/ˈpɑstə/',
                'pronunciation_ipa': '/ˈpɑstə/',
                'etymology': 'From Italian "pasta," from Late Latin "pasta" meaning dough or paste, from Greek "pasta" meaning barley porridge.',
                'memory_tip': 'PASTA sounds like "PAST-A" - think of "past" traditions of making dough "a" certain way to create delicious noodles.',
                'example_sentence': 'The restaurant specialized in fresh _____ made daily with traditional Italian techniques.'
            },
            'pastel': {
                'definition': 'A soft, pale color; an artistic medium consisting of powdered pigment formed into sticks; artwork created using this medium. Pastel colors are light, delicate tints that create gentle, soothing visual effects. As an art medium, pastels allow for soft blending and subtle color gradations. Artists use pastels for portraits, landscapes, and other subjects requiring delicate color work. The medium combines aspects of drawing and painting, allowing for both linear work and broad color areas. Pastel artworks are often displayed under glass to protect the delicate surface.',
                'pronunciation': '/pæˈstɛl/',
                'pronunciation_ipa': '/pæˈstɛl/',
                'etymology': 'From French "pastel," from Italian "pastello," from "pasta" meaning paste. Refers to the paste-like consistency of the medium.',
                'memory_tip': 'PASTEL sounds like "PASTE-L" - think of "paste"-like art medium that creates light, soft colors like delicate pastries.',
                'example_sentence': 'The artist used soft _____ colors to create a gentle, dreamy landscape painting.'
            },
            'pastiche': {
                'definition': 'An artistic work that deliberately imitates the style of another artist, period, or work; a composition made up of selections from different sources. Pastiche can be homage, parody, or creative exercise that demonstrates understanding of artistic styles. Unlike forgery, pastiche openly acknowledges its imitative nature. The technique appears in literature, music, visual arts, and film. Pastiche allows artists to explore different styles, pay tribute to influences, or create new works that blend various traditions. The approach requires deep understanding of the styles being imitated.',
                'pronunciation': '/pæˈstiʃ/',
                'pronunciation_ipa': '/pæˈstiʃ/',
                'etymology': 'From French "pastiche," from Italian "pasticcio" meaning pie or pastry made of various ingredients. Refers to mixing different elements.',
                'memory_tip': 'PASTICHE sounds like "PAST-ICHE" - think of an artistic "itch" to imitate styles from the "past" - mixing different influences.',
                'example_sentence': 'The film was a clever _____ of 1940s film noir, complete with shadowy cinematography and hard-boiled dialogue.'
            },
            'pastime': {
                'definition': 'An activity that someone does regularly for enjoyment during leisure time; a hobby or recreational pursuit that helps pass time pleasantly. Pastimes provide relaxation, entertainment, and personal satisfaction outside of work or other obligations. They can be solitary activities like reading or gardening, or social activities like sports or games. Pastimes often reflect personal interests, skills, and values. Having engaging pastimes contributes to mental health, stress reduction, and overall quality of life. The choice of pastimes varies widely based on individual preferences, available time, and resources.',
                'pronunciation': '/ˈpæsˌtaɪm/',
                'pronunciation_ipa': '/ˈpæsˌtaɪm/',
                'etymology': 'Compound of "pass" + "time," literally meaning something that helps time pass. Originally referred to activities that make time go by quickly.',
                'memory_tip': 'PASTIME = PASS + TIME. Think of enjoyable activities that help "time" "pass" quickly - hobbies and recreational pursuits.',
                'example_sentence': 'Reading mystery novels became her favorite _____ during retirement.'
            },
            'pastitsio': {
                'definition': 'A traditional Greek baked pasta dish consisting of layers of pasta, meat sauce, and béchamel sauce, similar to lasagna but typically made with tubular pasta like penne or bucatini. The dish features a rich meat sauce seasoned with herbs and spices, layered between pasta and topped with a creamy white sauce before baking. Pastitsio is considered one of the signature dishes of Greek cuisine and is often served at special occasions and family gatherings. The preparation requires time and skill to properly layer the components and achieve the characteristic golden-brown top.',
                'pronunciation': '/ˌpɑstiˈtsioʊ/',
                'pronunciation_ipa': '/ˌpɑstiˈtsioʊ/',
                'etymology': 'From Greek "παστίτσιο," possibly related to "pasta" through Italian influence. The dish shows the blend of Mediterranean culinary traditions.',
                'memory_tip': 'PASTITSIO sounds like "PASTA-TSIO" - think of Greek "pasta" with a special "tsio" (ending) that makes it distinctly Greek-style.',
                'example_sentence': 'The family recipe for _____ had been passed down for generations, featuring a secret blend of spices in the meat sauce.'
            },
            'pastrami': {
                'definition': 'A type of cured and smoked meat, typically made from beef brisket that has been brined, seasoned with spices, and then smoked and steamed. Pastrami is strongly associated with Jewish delicatessen cuisine and New York-style sandwiches. The preparation process involves curing the meat in a spiced brine, coating it with additional spices (often including black pepper and coriander), then smoking and steaming until tender. The result is flavorful, tender meat that is typically sliced thin and served on rye bread with mustard. Pastrami has become an iconic American deli food.',
                'pronunciation': '/pəˈstrɑmi/',
                'pronunciation_ipa': '/pəˈstrɑmi/',
                'etymology': 'From Yiddish "pastrome," possibly from Romanian "pastramă," related to methods of preserving and preparing meat.',
                'memory_tip': 'PASTRAMI sounds like "PAST-RAMI" - think of meat from the "past" that\'s been cured and spiced, like a "ram" preserved for eating.',
                'example_sentence': 'The deli was famous for its _____ sandwich, piled high with tender, spiced meat on fresh rye bread.'
            },
            'pastry': {
                'definition': 'Dough made from flour, fat, and water that is used as a base for various baked goods; baked goods made with such dough, including pies, tarts, croissants, and sweet confections. Pastry dough can be sweet or savory and varies in texture from flaky to tender depending on the preparation method and intended use. The art of pastry making requires skill in handling dough, controlling temperature, and understanding how ingredients interact. Professional pastry chefs specialize in creating both simple and elaborate baked goods. Pastries are enjoyed worldwide in various cultural traditions.',
                'pronunciation': '/ˈpeɪstri/',
                'pronunciation_ipa': '/ˈpeɪstri/',
                'etymology': 'From Middle English "pastrie," from "paste" meaning dough or paste. Related to the paste-like consistency of the dough.',
                'memory_tip': 'PASTRY sounds like "PASTE-TRY" - think of "trying" to make delicious baked goods from "paste"-like dough.',
                'example_sentence': 'The French _____ chef created delicate croissants and elegant tarts for the bakery\'s morning display.'
            },
            'patagonia': {
                'definition': 'A geographical region in South America shared by Argentina and Chile, characterized by vast plains, mountains, and dramatic landscapes; also the name of an outdoor clothing company. The region is known for its natural beauty, including glaciers, mountains, and unique wildlife. Patagonia has become synonymous with adventure travel, conservation, and pristine wilderness. The area includes famous destinations like Torres del Paine and the Fitz Roy mountain range. The name has been adopted by the clothing company to evoke images of outdoor adventure and environmental consciousness.',
                'pronunciation': '/ˌpætəˈɡoʊniə/',
                'pronunciation_ipa': '/ˌpætəˈɡoʊniə/',
                'etymology': 'Named by Spanish explorer Magellan, possibly from "Patagón," referring to the large feet of indigenous people, from Spanish "pata" meaning paw or foot.',
                'memory_tip': 'PATAGONIA sounds like "PAT-A-GO-NIA" - think of wanting to "pat" and "go" to this beautiful region for adventure.',
                'example_sentence': 'The photographers traveled to _____ to capture images of the region\'s stunning glaciers and mountain landscapes.'
            },
            'patches': {
                'definition': 'Small pieces of material used to mend or cover holes; software updates designed to fix bugs or security vulnerabilities; small areas that differ from their surroundings; pieces of cloth worn as decorations or badges. Physical patches repair clothing, equipment, or surfaces. Software patches update programs to fix problems or add features. Natural patches might be areas of different vegetation or coloration. Decorative patches can indicate membership, achievement, or personal style. The concept involves covering, fixing, or marking specific areas.',
                'pronunciation': '/ˈpætʃəz/',
                'pronunciation_ipa': '/ˈpætʃəz/',
                'etymology': 'Plural of "patch," possibly from Middle English "pacche," of uncertain origin. Related to covering or mending small areas.',
                'memory_tip': 'PATCHES sounds like "PAT-CHES" - think of "patting" small pieces onto clothing or giving gentle "patches" to fix things.',
                'example_sentence': 'The software developer released security _____ to fix vulnerabilities discovered in the previous version.'
            },
            'patella': {
                'definition': 'The kneecap; a small, flat, triangular bone that sits at the front of the knee joint, protecting the knee and providing attachment points for muscles and tendons. The patella is the largest sesamoid bone in the human body, embedded within the quadriceps tendon. It plays a crucial role in knee function by increasing the leverage of the quadriceps muscle and protecting the knee joint from injury. Patella problems can include dislocation, fractures, or conditions like patellofemoral pain syndrome. Understanding patella anatomy is important for treating knee injuries and disorders.',
                'pronunciation': '/pəˈtɛlə/',
                'pronunciation_ipa': '/pəˈtɛlə/',
                'etymology': 'From Latin "patella," diminutive of "patera" meaning shallow dish or pan, referring to the bone\'s shallow, dish-like shape.',
                'memory_tip': 'PATELLA sounds like "PAT-ELLA" - think of "patting" your "ella" (knee) where the kneecap bone protects the joint.',
                'example_sentence': 'The MRI showed a small fracture in the _____ that would require several weeks of rest to heal properly.'
            },
            'patent': {
                'definition': 'A government-granted exclusive right to make, use, or sell an invention for a specific period; clearly evident or obvious; open to public inspection. Legal patents protect inventors\' rights and encourage innovation by providing temporary monopolies on new inventions. The patent system requires detailed disclosure of inventions in exchange for protection. Patent law is complex, involving requirements for novelty, usefulness, and non-obviousness. The adjective "patent" means clearly visible or obvious to everyone. Patent rights are essential for protecting intellectual property and fostering technological advancement.',
                'pronunciation': '/ˈpætənt/',
                'pronunciation_ipa': '/ˈpætənt/',
                'etymology': 'From Latin "patens" meaning open or accessible, from "patere" meaning to lie open. Originally referred to open letters or documents.',
                'memory_tip': 'PATENT = PAT + ENT. Think of "patting" an "entity" (invention) to protect it, or something that\'s "patently" (clearly) obvious.',
                'example_sentence': 'The inventor filed a _____ application to protect her revolutionary new solar panel design.'
            },
            'path': {
                'definition': 'A track or route for walking or traveling; a course of action or way of achieving something; the route that something takes through space or time. Physical paths include trails, walkways, and roads that facilitate movement between locations. Metaphorical paths represent life directions, career choices, or problem-solving approaches. In computing, paths specify the location of files or directories. The concept emphasizes direction, progression, and purposeful movement toward destinations or goals. Choosing the right path often involves consideration of efficiency, safety, and desired outcomes.',
                'pronunciation': '/pæθ/',
                'pronunciation_ipa': '/pæθ/',
                'etymology': 'From Old English "pæth," related to finding or treading a way. Basic concept of a route or way forward.',
                'memory_tip': 'PATH rhymes with "math" - think of calculating the best "path" to reach your destination, like solving a problem.',
                'example_sentence': 'The hiking _____ wound through the forest and led to a beautiful waterfall.'
            },
            'pathogen': {
                'definition': 'A microorganism that causes disease in plants, animals, or humans; any biological agent that can produce illness or infection. Pathogens include bacteria, viruses, fungi, parasites, and other disease-causing organisms. Understanding pathogens is crucial for medicine, public health, and disease prevention. Different pathogens cause different types of infections and require different treatment approaches. The study of pathogens involves understanding how they spread, how they cause disease, and how to prevent or treat the infections they cause. Modern medicine focuses heavily on identifying and controlling pathogenic organisms.',
                'pronunciation': '/ˈpæθədʒən/',
                'pronunciation_ipa': '/ˈpæθədʒən/',
                'etymology': 'From Greek "pathos" meaning disease or suffering + "genes" meaning producing or causing. Literally means "disease-producing."',
                'memory_tip': 'PATHOGEN = PATHO (disease) + GEN (generate). Think of organisms that "generate" "disease" - microbes that make you sick.',
                'example_sentence': 'The laboratory identified the _____ responsible for the food poisoning outbreak.'
            },
            'pathos': {
                'definition': 'An appeal to emotion; a quality that evokes pity, sadness, or compassion; one of the three modes of persuasion in rhetoric, along with ethos and logos. Pathos involves using emotional arguments to influence audience attitudes and decisions. Effective speakers and writers use pathos to connect with their audience\'s feelings and values. The concept is fundamental to understanding persuasive communication, literature, and artistic expression. Pathos can involve various emotions including sympathy, fear, anger, or hope. Balancing pathos with logical arguments and credibility creates powerful, persuasive communication.',
                'pronunciation': '/ˈpeɪθɔs/',
                'pronunciation_ipa': '/ˈpeɪθɔs/',
                'etymology': 'From Greek "pathos" meaning experience, emotion, or suffering. One of Aristotle\'s three modes of persuasion.',
                'memory_tip': 'PATHOS sounds like "PATH-OSS" - think of the emotional "path" that speakers use to reach their audience\'s hearts.',
                'example_sentence': 'The speaker\'s use of _____ in describing the refugees\' plight moved the audience to donate generously.'
            },
            'pathways': {
                'definition': 'Routes or tracks that provide passage from one place to another; sequences of actions or steps that lead to particular outcomes; biological or chemical routes through which substances move or reactions occur. Physical pathways include roads, trails, and corridors for movement. Metabolic pathways describe sequences of chemical reactions in living organisms. Neural pathways are connections in the nervous system. Career pathways outline steps for professional development. The concept emphasizes planned routes, systematic progression, and purposeful direction toward specific destinations or goals.',
                'pronunciation': '/ˈpæθˌweɪz/',
                'pronunciation_ipa': '/ˈpæθˌweɪz/',
                'etymology': 'Compound of "path" + "ways," emphasizing routes or methods of passage. Plural form indicates multiple possible routes.',
                'memory_tip': 'PATHWAYS = PATH + WAYS. Think of multiple "ways" to follow different "paths" - various routes to reach destinations.',
                'example_sentence': 'The university offered multiple career _____ for students interested in environmental science.'
            },
            'patience': {
                'definition': 'The ability to wait calmly without becoming annoyed or anxious; tolerance and understanding when dealing with difficult people or situations; the capacity to persevere through challenges without giving up. Patience is considered a virtue in many cultures and philosophical traditions. It involves emotional regulation, self-control, and the ability to delay gratification. Patience is essential for learning, relationship building, and achieving long-term goals. Developing patience often requires practice and mindfulness. The quality helps people cope with stress, uncertainty, and frustration more effectively.',
                'pronunciation': '/ˈpeɪʃəns/',
                'pronunciation_ipa': '/ˈpeɪʃəns/',
                'etymology': 'From Latin "patientia" meaning endurance or suffering, from "pati" meaning to suffer or endure. Related to accepting difficult situations.',
                'memory_tip': 'PATIENCE sounds like "PAY-SHENCE" - think of "paying" attention with "sense" to wait calmly without rushing.',
                'example_sentence': 'Teaching young children requires enormous _____ and the ability to explain concepts multiple times.'
            },
            'patio': {
                'definition': 'A paved outdoor area adjoining a house, typically used for dining or recreation; an open courtyard or terrace. Patios extend living space outdoors and provide areas for relaxation, entertainment, and dining. They can be constructed from various materials including concrete, stone, brick, or pavers. Patios often feature outdoor furniture, plants, and sometimes cooking facilities like grills or outdoor kitchens. The design and placement of patios consider factors like privacy, sun exposure, and accessibility. Well-designed patios enhance property value and quality of life.',
                'pronunciation': '/ˈpætiˌoʊ/',
                'pronunciation_ipa': '/ˈpætiˌoʊ/',
                'etymology': 'From Spanish "patio" meaning courtyard or yard, from Latin "patere" meaning to lie open. Refers to open outdoor spaces.',
                'memory_tip': 'PATIO sounds like "PAT-IO" - think of "patting" people on outdoor "I/O" (input/output) spaces for relaxation.',
                'example_sentence': 'They installed a stone _____ with comfortable seating for summer barbecues and evening gatherings.'
            },
            'patissier': {
                'definition': 'A professional pastry chef; someone skilled in making pastries, desserts, and other baked confections. Patissiers specialize in the art and science of pastry making, including cakes, tarts, chocolates, and elaborate desserts. The profession requires technical skill, creativity, and understanding of ingredients and techniques. French culinary tradition particularly values patissiers, who often complete extensive training and apprenticeships. Modern patissiers may work in restaurants, hotels, bakeries, or as independent cake designers. The role combines artistry with precise technical execution.',
                'pronunciation': '/pəˈtɪsiər/',
                'pronunciation_ipa': '/pəˈtɪsiər/',
                'etymology': 'From French "pâtissier," from "pâtisserie" meaning pastry shop, from "pâte" meaning paste or dough.',
                'memory_tip': 'PATISSIER sounds like "PAT-TISSIER" - think of someone who "pats" and shapes dough into beautiful pastries.',
                'example_sentence': 'The renowned _____ created an elaborate wedding cake featuring intricate sugar work and delicate flavors.'
            },
            'patois': {
                'definition': 'A regional dialect or language that differs significantly from the standard language; informal or colloquial speech patterns specific to a particular group or region. Patois often develops in isolated communities or among specific social groups, incorporating unique vocabulary, pronunciation, and grammar. Examples include Jamaican Patois and various French regional dialects. These language varieties carry cultural identity and historical significance. Linguists study patois to understand language evolution, social dynamics, and cultural preservation. Modern globalization both threatens and helps preserve various patois through increased documentation and cultural awareness.',
                'pronunciation': '/ˈpætwɑ/',
                'pronunciation_ipa': '/ˈpætwɑ/',
                'etymology': 'From French "patois," possibly from "patoyer" meaning to handle clumsily, or from "patte" meaning paw, suggesting rough speech.',
                'memory_tip': 'PATOIS sounds like "PAT-WAS" - think of how language "was" shaped by "patting" together local words and expressions.',
                'example_sentence': 'The author skillfully incorporated local _____ into the dialogue to authentic represent the character\'s regional background.'
            },
            'patrician': {
                'definition': 'A member of the aristocracy; relating to or characteristic of the upper class; in ancient Rome, a member of the noble class that originally held political power. Patricians typically possess wealth, education, refined manners, and social prestige. The term can describe both actual aristocrats and those who adopt aristocratic attitudes or behaviors. In Roman history, patricians formed the ruling class and controlled religious and political institutions. Modern usage extends to anyone with aristocratic bearing, exclusive social position, or inherited privilege. The concept often implies both privilege and responsibility.',
                'pronunciation': '/pəˈtrɪʃən/',
                'pronunciation_ipa': '/pəˈtrɪʃən/',
                'etymology': 'From Latin "patricius," from "pater" meaning father. Originally referred to descendants of the founding fathers of Rome.',
                'memory_tip': 'PATRICIAN = PATRI (father) + CIAN. Think of people from "father" (founding) families - the aristocratic upper class.',
                'example_sentence': 'The _____ family had lived in the mansion for generations, maintaining their position in high society.'
            },
            'patripassianism': {
                'definition': 'A Christian theological doctrine, considered heretical by orthodox Christianity, which holds that God the Father suffered and died along with Jesus Christ during the crucifixion. This belief contradicts the orthodox understanding that only the Son (Jesus) experienced suffering and death while the Father remained impassible (unable to suffer). Patripassianism was rejected by early church councils because it was seen as confusing the distinct persons of the Trinity. The doctrine arose in early Christianity but was declared heretical because it suggested that the divine nature itself could suffer and die.',
                'pronunciation': '/ˌpeɪtrɪpəˈseɪʃəˌnɪzəm/',
                'pronunciation_ipa': '/ˌpeɪtrɪpəˈseɪʃəˌnɪzəm/',
                'etymology': 'From Latin "patripassianismus," from "pater" (father) + "passio" (suffering) + "-ism." Literally means "father-suffering doctrine."',
                'memory_tip': 'PATRIPASSIANISM = PATRI (father) + PASSI (suffering) + ANISM. Think of the belief that the "father" (God) "suffered" with Christ.',
                'example_sentence': 'Early church theologians rejected _____ as incompatible with orthodox understanding of the Trinity.'
            },
            'patrol': {
                'definition': 'To move regularly around an area to monitor, guard, or maintain security; a group of people or vehicles engaged in such monitoring activity. Patrols serve protective, investigative, and deterrent functions in military, police, and security operations. The activity involves systematic observation and response to potential threats or problems. Patrol routes are typically planned to provide comprehensive coverage of assigned areas. Modern patrols may use various technologies including vehicles, aircraft, and surveillance equipment. Effective patrolling requires training, vigilance, and appropriate response protocols.',
                'pronunciation': '/pəˈtroʊl/',
                'pronunciation_ipa': '/pəˈtroʊl/',
                'etymology': 'From French "patrouiller" meaning to paddle or patrol, possibly from "patte" meaning paw, suggesting movement on foot.',
                'memory_tip': 'PATROL sounds like "PAT-ROLL" - think of "patting" the ground as you "roll" around an area to keep it secure.',
                'example_sentence': 'Security guards _____ the parking lot every hour to ensure the safety of employees and their vehicles.'
            },
            'patronise': {
                'definition': 'British spelling of patronize; to treat someone in a condescending manner; to be a regular customer of a business; to support or sponsor someone or something. The condescending meaning involves talking down to someone as if they were inferior or less intelligent. Commercial patronage involves regularly buying goods or services from particular businesses. Cultural patronage involves providing financial or other support to artists, institutions, or causes. The word can have both negative connotations (condescension) and positive ones (support and loyalty).',
                'pronunciation': '/ˈpeɪtrəˌnaɪz/',
                'pronunciation_ipa': '/ˈpeɪtrəˌnaɪz/',
                'etymology': 'British spelling of "patronize," from Latin "patronus" meaning protector or supporter, from "pater" meaning father.',
                'memory_tip': 'PATRONISE = PATRON + ISE. Think of being a "patron" who "ises" (supports) businesses, or unfortunately talks down to others.',
                'example_sentence': 'She decided not to _____ the restaurant anymore after the waiter spoke to her in a condescending manner.'
            },
            'patronize': {
                'definition': 'American spelling of patronise; to treat someone condescendingly; to be a regular customer of a business; to provide support or sponsorship. The condescending usage involves speaking to someone as if they lack understanding or intelligence. Business patronage means regularly purchasing from particular establishments. Artistic or cultural patronage involves providing financial support to creators or institutions. The dual meanings can create confusion, as the word can indicate both positive support and negative condescension depending on context.',
                'pronunciation': '/ˈpeɪtrəˌnaɪz/',
                'pronunciation_ipa': '/ˈpeɪtrəˌnaɪz/',
                'etymology': 'American spelling of "patronize," from Latin "patronus" meaning protector or supporter, from "pater" meaning father.',
                'memory_tip': 'PATRONIZE = PATRON + IZE. Think of being a "patron" who "izes" (supports) businesses, or unfortunately talks down like a stern father.',
                'example_sentence': 'The wealthy businessman continued to _____ local artists by purchasing their work and funding exhibitions.'
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

def process_batch_128():
    processor = Batch128Processor()
    
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_128_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_128_processed.csv'
    
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
    
    logging.info(f"Batch 128 processing complete. Processed {successful_count}/50 words.")
    logging.info(f"Output saved to: {output_file}")
    
    if combined_words:
        logging.warning(f"Combined word errors detected: {combined_words}")
    
    return successful_count

if __name__ == "__main__":
    process_batch_128()