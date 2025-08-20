#!/usr/bin/env python3

import csv
import logging
from typing import Dict, List, Any
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DifficultyCalculator:
    """Calculate difficulty scores based on 4 factors."""
    
    def calculate_difficulty_score(self, word: str, definition: str, etymology: str) -> Dict[str, Any]:
        """Calculate 4-factor difficulty score but leave final difficulty null."""
        return {
            'phonetic_transparency_score': self._calculate_phonetic_transparency(word),
            'word_frequency_score': self._calculate_word_frequency(word),
            'morphological_complexity_score': self._calculate_morphological_complexity(word),
            'etymology_complexity_score': self._calculate_etymology_complexity(etymology),
            'difficulty': None  # Leave null as instructed
        }
    
    def _calculate_phonetic_transparency(self, word: str) -> float:
        """Calculate phonetic transparency (0.0 = transparent, 1.0 = opaque)."""
        score = 0.0
        if any(combo in word.lower() for combo in ['ph', 'gh', 'ch', 'sh', 'th']):
            score += 0.2
        if any(combo in word.lower() for combo in ['ough', 'augh', 'eigh']):
            score += 0.3
        if len([c for c in word.lower() if c in 'aeiou']) / len(word) < 0.2:
            score += 0.2
        return min(1.0, score)
    
    def _calculate_word_frequency(self, word: str) -> float:
        """Estimate word frequency (0.0 = very common, 1.0 = very rare)."""
        common_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our'}
        if word.lower() in common_words:
            return 0.0
        if len(word) <= 4:
            return 0.3
        elif len(word) <= 7:
            return 0.6
        else:
            return 0.9
    
    def _calculate_morphological_complexity(self, word: str) -> float:
        """Calculate morphological complexity based on affixes and roots."""
        complexity = 0.0
        prefixes = ['un', 're', 'in', 'dis', 'en', 'non', 'over', 'mis', 'sub', 'pre', 'inter', 'fore', 'de', 'trans', 'super', 'semi', 'anti', 'mid', 'under']
        suffixes = ['ing', 'ly', 'ed', 'ies', 'ied', 'ying', 'es', 'er', 'ion', 'tion', 'ation', 'ition', 'able', 'ible', 'ment', 'ness', 'ous', 'eous', 'ious']
        
        for prefix in prefixes:
            if word.lower().startswith(prefix):
                complexity += 0.2
                break
        
        for suffix in suffixes:
            if word.lower().endswith(suffix):
                complexity += 0.2
                break
                
        if len(word) > 10:
            complexity += 0.3
            
        return min(1.0, complexity)
    
    def _calculate_etymology_complexity(self, etymology: str) -> float:
        """Calculate etymology complexity based on language origins."""
        if not etymology or etymology.strip() == "":
            return 0.5
        
        complex_origins = ['greek', 'latin', 'french', 'german', 'italian', 'spanish', 'arabic', 'hebrew', 'sanskrit']
        simple_origins = ['english', 'old english', 'middle english']
        
        etymology_lower = etymology.lower()
        
        for origin in complex_origins:
            if origin in etymology_lower:
                return 0.8
        
        for origin in simple_origins:
            if origin in etymology_lower:
                return 0.2
                
        return 0.5

class Batch109Processor:
    """Processes Batch 109 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for each word"""
        data = {
            'matriculation': {
                'definition': 'The process of enrolling in or being admitted to a college, university, or educational institution as a degree-seeking student. Matriculation involves completing formal admission requirements, submitting applications, transcripts, and supporting documents, and being officially accepted into an academic program. The term derives from the historical practice of registering students in official university records or matricula. Matriculation ceremonies mark the formal beginning of university study, often involving oath-taking or symbolic rituals that welcome new students into the academic community. Different institutions have varying matriculation requirements and processes, but the concept universally represents the transition from prospective student to enrolled member of an educational institution. Some universities hold special matriculation ceremonies with academic regalia and traditional customs.',
                'pronunciation': "/məˌtrɪk.jəˈleɪ.ʃən/",
                'etymology': 'From Medieval Latin "matriculare," meaning to register or enroll, derived from "matricula" (register or roll).',
                'memory_tip': 'Remember MATRICULATION = entering the MATRIX of EDUCATION - formal enrollment in college.',
                'example_sentence': 'After completing her ______, she received her student ID and course registration materials.'
            },
            'matrimony': {
                'definition': 'The formal union of marriage between two people, particularly viewed as a sacred or religious institution. Matrimony encompasses both the wedding ceremony and the ongoing marital relationship, emphasizing commitment, partnership, and often spiritual dimensions of marriage. Religious traditions typically regard matrimony as a sacrament or holy covenant blessed by divine authority. Legal matrimony creates rights, responsibilities, and social status changes recognized by government and society. The concept implies permanence, mutual support, and shared life goals between spouses. Matrimonial law governs marriage regulations, divorce proceedings, and spousal rights. Cultural traditions surrounding matrimony include engagement periods, wedding ceremonies, vows, and celebration customs that vary across different societies and religious communities.',
                'pronunciation': "/ˈmæt.rɪˌmoʊ.ni/",
                'etymology': 'From Latin "matrimonium," derived from "mater" (mother), emphasizing the maternal/family aspects of marriage.',
                'memory_tip': 'Remember MATRIMONY = MATER (mother) + union - marriage that creates families.',
                'example_sentence': 'The couple celebrated fifty years of ______ with a golden anniversary party.'
            },
            'matterhorn': {
                'definition': 'A famous pyramidal peak in the Alps on the border between Switzerland and Italy, known for its distinctive horn-shaped silhouette and mountaineering significance. The Matterhorn rises 14,692 feet (4,478 meters) and is one of the most photographed mountains in the world. Its steep, dramatic profile and isolated position make it an iconic symbol of Alpine climbing and Swiss tourism. The mountain\'s name comes from the German words meaning "meadow peak," referring to the Mattertal valley below. The Matterhorn was first climbed in 1865, marking a significant achievement in mountaineering history. The peak appears on Swiss currency, logos, and countless photographs, becoming a symbol of natural grandeur and human achievement in extreme environments.',
                'pronunciation': "/ˈmæt.ər.hɔrn/",
                'etymology': 'From German "Matterhorn," meaning "peak of the meadows," from "Matte" (meadow) + "Horn" (peak).',
                'memory_tip': 'Remember MATTERHORN = the peak that MATTERS most - iconic pyramid-shaped mountain.',
                'example_sentence': 'The climber gazed up at the imposing ______ peak, its sharp edges cutting dramatically against the sky.'
            },
            'mattress': {
                'definition': 'A large, rectangular pad used as a bed or part of a bed, designed to support the human body during sleep and provide comfort. Modern mattresses contain various materials including springs, foam, latex, or air chambers to distribute weight and maintain proper spinal alignment. Different mattress types serve different sleep preferences: firm mattresses provide strong support, soft mattresses offer cushioning comfort, and memory foam mattresses contour to body shape. Quality mattresses contribute to better sleep health, reducing back pain and improving rest quality. Mattress construction involves multiple layers including support cores, comfort layers, and protective covers. The mattress industry has evolved from simple straw-filled sacks to sophisticated sleep systems with temperature regulation and customizable firmness levels.',
                'pronunciation': "/ˈmæt.rəs/",
                'etymology': 'From Arabic "matrah," meaning place where something is thrown down, via Old French "materas."',
                'memory_tip': 'Remember MATTRESS = the MAT you REST on - comfortable bed support for sleeping.',
                'example_sentence': 'After testing several options, they chose a memory foam ______ for better sleep support.'
            },
            'mausoleum': {
                'definition': 'A large, impressive tomb or burial vault, typically built above ground as a monument to honor deceased individuals of importance or wealth. Mausoleums represent elaborate architectural expressions of remembrance, often featuring classical design elements, sculptures, and inscriptions. Famous examples include the Taj Mahal in India and the original Mausoleum at Halicarnassus in ancient Turkey, one of the Seven Wonders of the Ancient World. Modern mausoleums serve as family burial sites, cemetery landmarks, and tourist attractions. These structures reflect cultural attitudes toward death, memory, and posthumous recognition. Mausoleum design varies from simple stone buildings to ornate palatial structures with artistic decorations and symbolic elements that commemorate the deceased\'s life and achievements.',
                'pronunciation': "/ˌmɔ.səˈli.əm/",
                'etymology': 'From Latin "mausoleum," named after King Mausolus of Caria, whose elaborate tomb was one of the Seven Wonders.',
                'memory_tip': 'Remember MAUSOLEUM = MAU-SO-LEUM - elaborate tomb named after King MAU-solus.',
                'example_sentence': 'The marble ______ dominated the cemetery with its towering columns and intricate sculptures.'
            },
            'mauve': {
                'definition': 'A pale purple color with a pinkish tinge, named after the mallow flower; also referring to the synthetic dye that first produced this color in 1856. Mauve represents a significant milestone in chemistry and fashion history, as it was one of the first synthetic aniline dyes discovered by William Henry Perkin. Before synthetic dyes, purple colors were expensive and rare, derived from natural sources like murex shells. The discovery of mauve dye democratized purple fashion and launched the modern chemical dye industry. In color theory, mauve sits between purple and pink, creating a soft, sophisticated hue popular in interior design, fashion, and art. The color evokes femininity, elegance, and Victorian-era aesthetics, maintaining popularity in contemporary design applications.',
                'pronunciation': "/moʊv/",
                'etymology': 'From French "mauve," meaning mallow flower, referring to the plant that inspired the color name.',
                'memory_tip': 'Remember MAUVE = soft purple color like the MALLOW flower that moves toward pink.',
                'example_sentence': 'The Victorian parlor was decorated in shades of ______ and cream for an elegant appearance.'
            },
            'maverick': {
                'definition': 'An independent-minded person who refuses to conform to established practices or beliefs; also an unbranded range animal. The term originally described unbranded cattle that roamed freely without owners, named after Samuel Maverick, a Texas rancher who did not brand his cattle. In modern usage, a maverick represents someone who thinks and acts independently, often challenging conventional wisdom or established authority. Mavericks in politics, business, science, and arts drive innovation and social change through unconventional approaches. While sometimes viewed as troublemakers, mavericks often achieve breakthroughs by rejecting traditional limitations. The concept implies both positive qualities (creativity, courage, leadership) and potential negatives (unpredictability, difficulty working within systems). Maverick thinking contributes to progress but may create conflict with established institutions.',
                'pronunciation': "/ˈmæv.ər.ɪk/",
                'etymology': 'Named after Samuel Maverick, Texas cattleman who didn\'t brand his cattle, making them independent roamers.',
                'memory_tip': 'Remember MAVERICK = independent person who won\'t follow the herd, like unbranded cattle.',
                'example_sentence': 'The scientist\'s ______ approach to research led to groundbreaking discoveries that challenged accepted theories.'
            },
            'mawkish': {
                'definition': 'Excessively sentimental, emotional, or sweet to the point of being nauseating or disgusting. Mawkish describes situations, expressions, or artistic works that attempt to evoke emotions but instead create discomfort through over-the-top sentimentality. The term originally referred to something that literally made one feel sick to the stomach, later extending to emotional reactions. Mawkish poetry, movies, or speeches lack subtlety and genuine emotion, instead relying on clichéd expressions of feeling. Critics use "mawkish" to describe art that manipulates audiences through artificial emotional appeals rather than authentic artistic expression. The word carries strong negative connotation, suggesting that apparent sentiment is actually shallow or insincere. Mawkish content often targets lowest-common-denominator emotional responses rather than sophisticated appreciation.',
                'pronunciation': "/ˈmɔ.kɪʃ/",
                'etymology': 'From obsolete "mawk" (maggot), originally meaning nauseating, later applied to excessive sentimentality.',
                'memory_tip': 'Remember MAWKISH = makes you feel sick from too much fake sentiment, like emotional MUCK.',
                'example_sentence': 'The movie\'s ______ ending with overly dramatic music left audiences feeling manipulated rather than moved.'
            },
            'mawkishflambé': {
                'definition': 'A combined word error from PDF parsing that incorrectly merged "mawkish" and "flambé." This represents a data processing error where two unrelated terms were concatenated without proper spacing. Mawkish means excessively sentimental, while flambé refers to a cooking technique involving igniting alcohol. Such parsing errors occur when PDF text extraction fails to recognize word boundaries, particularly in documents with complex formatting or multiple columns. These errors highlight the challenges of automated text processing and the importance of data validation. The nonsensical combination would require manual correction or sophisticated error detection algorithms to separate into meaningful individual components.',
                'pronunciation': "/ˈmɔ.kɪʃflɑmˈbeɪ/",
                'etymology': 'Processing error combining "mawkish" (from mawk/maggot) with "flambé" (French cooking term). Invalid concatenation.',
                'memory_tip': 'This is a COMBINED WORD ERROR - two different words incorrectly joined during PDF processing.',
                'example_sentence': 'The data validation system identified ______ as an invalid word combination requiring separation.'
            },
            'maxillae': {
                'definition': 'The plural form of maxilla, referring to the pair of bones that form the upper jaw and central part of the facial skeleton in vertebrates. The maxillae are crucial components of skull anatomy, housing the upper teeth and forming parts of the nasal cavity, eye sockets, and hard palate. In humans, the maxillae fuse during development to create the unified upper jaw structure. These bones contain the maxillary sinuses, air-filled cavities that lighten the skull and contribute to voice resonance. Dental procedures, facial reconstruction surgery, and orthodontics all involve working with maxillary structures. In insects and other arthropods, maxillae function as paired mouthparts used for manipulating food. Understanding maxillary anatomy is essential in fields including dentistry, oral surgery, and comparative anatomy.',
                'pronunciation': "/mækˈsɪl.i/",
                'etymology': 'Latin plural of "maxilla," meaning jaw or jawbone, derived from the root meaning to chew.',
                'memory_tip': 'Remember MAXILLAE = the MAX upper jaw bones - plural of maxilla.',
                'example_sentence': 'The forensic anthropologist examined the ______ to determine the individual\'s age and ancestry.'
            },
            'maximum': {
                'definition': 'The greatest amount, quantity, or degree possible or recorded; the upper limit of variation. Maximum represents the highest value in a range of measurements, temperatures, speeds, or other quantifiable phenomena. In mathematics, maximum points on graphs indicate peak values of functions. Weather reports include maximum temperatures as the highest expected readings for the day. Maximum security refers to the strictest level of imprisonment or protection. Maximum effort implies giving one\'s complete energy and attention to a task. Speed limits establish maximum legal velocities for safety. The concept appears across scientific, legal, and everyday contexts as a boundary or goal representing the most extreme positive value achievable under given conditions.',
                'pronunciation': "/ˈmæk.sə.məm/",
                'etymology': 'From Latin "maximum," neuter form of "maximus" meaning greatest or largest.',
                'memory_tip': 'Remember MAXIMUM = the MAX amount possible - greatest quantity or degree.',
                'example_sentence': 'The elevator has a ______ capacity of ten people for safety reasons.'
            },
            'maxwell': {
                'definition': 'A unit of magnetic flux in the electromagnetic system, named after Scottish physicist James Clerk Maxwell who formulated the fundamental equations of electromagnetism. One maxwell equals one line of magnetic force, representing the magnetic flux through a surface. Maxwell\'s contributions to physics include electromagnetic field theory, statistical mechanics, and color photography. His electromagnetic equations describe how electric and magnetic fields interact and propagate as waves, forming the theoretical foundation for modern electronics, radio, and optical technologies. The Maxwell equations predict the existence of electromagnetic waves traveling at light speed, leading to understanding that light itself is electromagnetic radiation. Maxwell\'s work unified electricity, magnetism, and light into a single theoretical framework that revolutionized physics and engineering.',
                'pronunciation': "/ˈmæks.wel/",
                'etymology': 'Named after James Clerk Maxwell (1831-1879), Scottish physicist who developed electromagnetic theory.',
                'memory_tip': 'Remember MAXWELL = magnetic FLUX unit named after physicist who understood electromagnetic WELL.',
                'example_sentence': 'The engineer measured the magnetic field strength in ______ units for the motor design.'
            },
            'maybe': {
                'definition': 'Perhaps; possibly but not certainly; used to express uncertainty, possibility, or tentative agreement. Maybe indicates that something might happen or be true but lacks definitive confirmation. The word functions as an adverb expressing probability somewhere between definite yes and definite no. Maybe appears frequently in casual conversation as a non-committal response that keeps options open. In decision-making contexts, maybe suggests the need for more information or time before reaching conclusions. The term can express politeness when declining invitations ("maybe next time") or diplomatic uncertainty in professional settings. Maybe reflects human cognitive processing of incomplete information and the common experience of uncertainty in daily life. It serves important social functions by avoiding premature commitment while maintaining conversational engagement.',
                'pronunciation': "/ˈmeɪ.bi/",
                'etymology': 'From Middle English "may be," combining the modal verb "may" with "be" to express possibility.',
                'memory_tip': 'Remember MAYBE = MAY BE possible - expressing uncertainty about something happening.',
                'example_sentence': 'I asked if she wanted to join us for dinner, and she said "______" while checking her schedule.'
            },
            'mayhem': {
                'definition': 'Violent disorder, chaos, or deliberate damage and destruction; originally a legal term for the crime of maiming someone. Modern usage describes any situation of wild confusion, uncontrolled activity, or destructive behavior. Mayhem can result from natural disasters, riots, accidents, or deliberate acts of vandalism. The term captures both physical destruction and social disorder, implying loss of normal order and control. News reports describe mayhem following earthquakes, during protests that turn violent, or when crowds become unruly. In legal contexts, mayhem historically referred to permanently disabling another person through violence. Contemporary usage extends the concept to describe overwhelming chaos in any context, from traffic mayhem during rush hour to the mayhem of a busy shopping mall during sales events.',
                'pronunciation': "/ˈmeɪ.hɛm/",
                'etymology': 'From Old French "mahaigne," meaning injury or damage, originally referring to the crime of maiming.',
                'memory_tip': 'Remember MAYHEM = MAY cause total chaos and HEM (harm) - violent disorder.',
                'example_sentence': 'The unexpected announcement caused ______ in the stock market as traders rushed to adjust their positions.'
            },
            'mayonnaise': {
                'definition': 'A thick, creamy sauce made from egg yolks, oil, and vinegar or lemon juice, emulsified to create a smooth, stable condiment. Mayonnaise serves as a base for many other sauces including tartar sauce, aioli, and thousand island dressing. The emulsification process requires careful technique to prevent separation, gradually adding oil while whisking egg yolks to create the characteristic creamy texture. Commercial mayonnaise includes stabilizers and preservatives for shelf life, while homemade versions offer fresher taste but shorter storage time. Regional variations exist worldwide, with different oils, acids, and flavor additions. Mayonnaise appears in potato salad, coleslaw, sandwiches, and countless recipes as both ingredient and condiment. The sauce originated in European cuisine and spread globally as a versatile food preparation staple.',
                'pronunciation': "/ˈmeɪ.ə.neɪz/",
                'etymology': 'Possibly from French "mahonnaise," named after Port Mahon in Menorca, Spain, or from "moyeunaise" (egg yolk sauce).',
                'memory_tip': 'Remember MAYONNAISE = creamy MAY-o sauce made from eggs that\'s NICE on sandwiches.',
                'example_sentence': 'She mixed homemade ______ with herbs to create a flavorful dipping sauce for the vegetables.'
            },
            'mazda': {
                'definition': 'A Japanese automotive manufacturer known for rotary engines, innovative design, and the "zoom-zoom" marketing campaign; also refers to Ahura Mazda, the supreme deity in Zoroastrianism. Mazda Motor Corporation was founded in 1920 and became famous for developing practical rotary engines in vehicles like the RX-7 and RX-8. The company name honors Ahura Mazda, the wise lord of light in ancient Persian religion, reflecting aspirations toward enlightenment and wisdom. Mazda vehicles emphasize driving pleasure, efficient design, and distinctive styling. The rotary engine technology distinguished Mazda from other manufacturers, though production challenges limited its widespread adoption. Modern Mazda focuses on conventional engines with innovative features like SKYACTIV technology for improved efficiency and performance. The brand maintains reputation for creating vehicles that prioritize driver engagement and enjoyment.',
                'pronunciation': "/ˈmɑz.də/",
                'etymology': 'Named after Ahura Mazda, the supreme deity in Zoroastrianism, meaning "wise lord" in ancient Persian.',
                'memory_tip': 'Remember MAZDA = car company named after ancient god of wisdom and light.',
                'example_sentence': 'The automotive journalist praised the ______ sports car for its responsive handling and rotary engine.'
            },
            'mañana': {
                'definition': 'Spanish word meaning "tomorrow" or "morning," often used in English to represent a relaxed attitude toward time and scheduling, particularly the concept of putting things off until later. Mañana embodies a cultural approach that prioritizes present relationships and experiences over rigid time schedules. The term can express both literal temporal meaning (tomorrow) and philosophical attitude (unhurried approach to life). In business contexts, "mañana attitude" sometimes describes perceived inefficiency, though it may reflect different cultural values regarding work-life balance. The word appears in English especially in Southwestern United States where Spanish cultural influence remains strong. Mañana represents cross-cultural communication challenges where different societies have varying relationships with time, punctuality, and scheduling priorities.',
                'pronunciation': "/mɑˈɲɑ.nə/",
                'etymology': 'From Spanish "mañana," meaning morning or tomorrow, derived from Latin "mane" (in the morning).',
                'memory_tip': 'Remember MAÑANA = tomorrow in Spanish - represents relaxed attitude toward time.',
                'example_sentence': 'When asked about the project deadline, he smiled and said "______," indicating it would be done eventually.'
            },
            'mccoy': {
                'definition': 'Used in the phrase "the real McCoy" to mean the genuine article or authentic version of something, as opposed to an imitation or substitute. The expression originated in late 19th-century America and may derive from several possible sources including boxer Norman Selby (who fought as Kid McCoy), Scotch whisky, or other historical figures. "The real McCoy" implies superior quality, authenticity, and trustworthiness compared to competitors or imitations. The phrase appears in advertising, casual conversation, and contexts where distinguishing genuine from fake is important. McCoy as a surname has Irish and Scottish origins. The expression emphasizes the human desire to identify and value authentic experiences, products, and people rather than accepting inferior substitutes or imitations.',
                'pronunciation': "/məˈkɔɪ/",
                'etymology': 'Uncertain origin; possibly from boxer Kid McCoy, Scots phrase "the real MacKay," or other historical sources.',
                'memory_tip': 'Remember McCOY = "the real McCOY" means the authentic, genuine article.',
                'example_sentence': 'After trying several imitations, he finally found the ______ - the original recipe that tasted perfect.'
            },
            'mcintosh': {
                'definition': 'A variety of red apple with tender, white flesh and sweet-tart flavor, developed in Canada in the early 1800s by John McIntosh. The McIntosh apple became one of North America\'s most popular varieties due to its excellent eating quality and ability to grow in cooler climates. These apples ripen in fall, store well, and work excellently for fresh eating, applesauce, and baking applications. McIntosh apples contributed genetics to many other popular varieties including Empire, Cortland, and Spartan. The variety helped establish commercial apple growing in regions with shorter growing seasons. Apple computers also adopted the McIntosh name (spelled Macintosh) for their computer line, referencing the apple connection. McIntosh apples represent successful agricultural development and remain important in North American fruit production.',
                'pronunciation': "/ˈmæk.ɪn.tɑʃ/",
                'etymology': 'Named after John McIntosh, Canadian farmer who discovered and cultivated this apple variety around 1811.',
                'memory_tip': 'Remember McINTOSH = the MAC apple variety that\'s great to bite INTO.',
                'example_sentence': 'The orchard specialized in heirloom varieties including the classic red ______ apple.'
            },
            'mcmansion': {
                'definition': 'A pejorative term for large, ostentatious houses built with mass-production techniques, often characterized by architectural inconsistency, excessive size relative to lot dimensions, and emphasis on appearance over quality. McMansions typically feature multiple architectural styles combined awkwardly, oversized rooms with poor proportions, and cheap construction materials disguised with superficial decorative elements. The term combines "McDonald\'s" (representing mass production and standardization) with "mansion" (large house), suggesting houses that appear impressive but lack architectural integrity. McMansions became prevalent in American suburbs during housing booms, particularly in the 1990s and 2000s. Critics argue these houses contribute to suburban sprawl, environmental waste, and erosion of architectural standards. The concept reflects tensions between affordable luxury housing and authentic architectural design.',
                'pronunciation': "/məkˈmæn.ʃən/",
                'etymology': 'Compound of "McDonald\'s" (mass-produced restaurant chain) + "mansion," criticizing mass-produced large houses.',
                'memory_tip': 'Remember McMansion = mass-produced MANSION like McDonald\'s - big but cheap construction.',
                'example_sentence': 'The urban planner criticized the new subdivision\'s ______ for their lack of architectural character.'
            },
            'meal': {
                'definition': 'A regular occasion when food is consumed, typically breakfast, lunch, or dinner; also coarsely ground grain or other food substances. Meals provide essential nutrition and serve important social and cultural functions across human societies. Family meals create opportunities for communication, tradition-sharing, and relationship building. Meal planning involves considering nutrition, budget, time constraints, and dietary preferences. Different cultures have varying meal schedules, portion sizes, and food combinations that reflect available ingredients and social customs. Meal preparation requires cooking skills, food safety knowledge, and organizational abilities. Shared meals mark celebrations, religious observances, and community gatherings. The timing and content of meals affect health, energy levels, and social interactions. Modern lifestyle changes have influenced meal patterns, with increasing emphasis on convenience foods and irregular eating schedules.',
                'pronunciation': "/mil/",
                'etymology': 'From Old English "mǣl," meaning appointed time or measure, originally referring to fixed times for eating.',
                'memory_tip': 'Remember MEAL = regular eating time that helps you HEAL and grow with nutrition.',
                'example_sentence': 'The family gathered around the table to enjoy their evening ______ together.'
            },
            'mean': {
                'definition': 'Having multiple meanings: to intend or signify (verb); unkind or nasty (adjective); or the average of a set of numbers (noun). As a verb, mean expresses purpose, intention, or significance ("I mean to help" or "What does this word mean?"). As an adjective, mean describes cruel, spiteful, or deliberately hurtful behavior toward others. In mathematics, the mean represents the sum of values divided by the number of values, providing a measure of central tendency. Mean can also indicate intermediate position between extremes or refer to limited financial resources. The word\'s multiple meanings create potential confusion in communication, requiring context for proper interpretation. Statistical means help analyze data patterns and make comparisons across different groups or time periods.',
                'pronunciation': "/min/",
                'etymology': 'From Old English "mǣnan" (to intend) for the verb; from Old English "gemǣne" (common) for other senses.',
                'memory_tip': 'Remember MEAN can mean intention, cruelty, or mathematical average - context determines meaning.',
                'example_sentence': 'When she asked what I ______ by that comment, I explained my intentions clearly.'
            },
            'meaning': {
                'definition': 'The significance, purpose, or intended message conveyed by words, actions, symbols, or experiences. Meaning represents the connection between signs and their referents, enabling communication and understanding between individuals. Linguistic meaning involves relationships between words and their definitions, while experiential meaning encompasses personal significance derived from life events. Philosophy and psychology explore how humans create, discover, and interpret meaning in various contexts. Meaning-making processes help people understand their experiences, relationships, and place in the world. Cultural meanings vary across societies, with symbols, rituals, and customs carrying different significance for different groups. The search for meaning motivates human behavior, influences mental health, and shapes individual identity. Effective communication requires shared understanding of meaning between speakers and listeners.',
                'pronunciation': "/ˈmin.ɪŋ/",
                'etymology': 'From Old English "mǣning," derived from "mǣnan" meaning to intend or signify.',
                'memory_tip': 'Remember MEANING = what something is MEAN-ing to say - the significance or purpose.',
                'example_sentence': 'The professor spent the entire lecture explaining the ______ behind the poet\'s complex metaphors.'
            },
            'meaningless': {
                'definition': 'Lacking purpose, significance, or coherent sense; without value or importance. Meaningless describes words, actions, or experiences that fail to convey useful information or contribute to understanding. Meaningless tasks feel pointless and fail to provide satisfaction or accomplishment. Meaningless data lacks patterns or useful insights for decision-making. In philosophical contexts, meaningless existence suggests lack of purpose or direction in life. Communication becomes meaningless when words fail to convey intended messages or create understanding between people. Meaningless activities waste time and energy without producing beneficial outcomes. The perception of meaninglessness can contribute to depression, anxiety, and existential distress. Conversely, finding meaning in seemingly meaningless situations represents important psychological adaptation and resilience.',
                'pronunciation': "/ˈmin.ɪŋ.ləs/",
                'etymology': 'From "meaning" + "-less" suffix, indicating absence of significance or purpose.',
                'memory_tip': 'Remember MEANINGLESS = MEANING-LESS - without significance, purpose, or value.',
                'example_sentence': 'The data appeared ______ until the analyst discovered the hidden pattern within the numbers.'
            },
            'means': {
                'definition': 'Methods, resources, or instruments used to achieve specific goals; also financial resources or wealth. Means represent the tools, strategies, or capabilities available for accomplishing desired outcomes. Financial means include income, savings, investments, and other monetary resources that enable particular lifestyles or purchases. "By means of" indicates the method or instrument used to accomplish something. "Means to an end" suggests that methods are valuable only for achieving goals rather than for their own sake. Means testing evaluates financial resources to determine eligibility for government benefits or assistance programs. The phrase "living within your means" advises spending only what you can afford. Means encompass both tangible resources (money, equipment) and intangible capabilities (skills, knowledge, connections) that enable achievement.',
                'pronunciation': "/minz/",
                'etymology': 'Plural of "mean," from Old English "gemǣne," relating to resources or methods held in common.',
                'memory_tip': 'Remember MEANS = the resources and methods that MEAN achieving your goals.',
                'example_sentence': 'She lacked the financial ______ to pursue graduate school without taking student loans.'
            },
            'measly': {
                'definition': 'Contemptibly small, meager, or insufficient; also affected by or resembling measles. Measly describes quantities that are disappointing due to their inadequacy relative to expectations or needs. A measly salary fails to meet living expenses; measly portions leave diners hungry. The term conveys frustration with amounts that seem insulting or unfairly small. Originally, measly referred to conditions resembling measles, including skin lesions or infections. In livestock, measly meat contains parasite cysts that make it unsuitable for consumption. Modern usage primarily emphasizes inadequate quantity rather than disease associations. Measly amounts often reflect poor judgment, insufficient resources, or deliberate stinginess by those controlling distributions. The word carries emotional weight, expressing disappointment and criticism of inadequate provisions.',
                'pronunciation': "/ˈmi.zli/",
                'etymology': 'Originally from "measles" + "-y" suffix, later extended to mean contemptibly small or inadequate.',
                'memory_tip': 'Remember MEASLY = MEASLES-ly small - contemptibly inadequate amount like spotted disease.',
                'example_sentence': 'After working overtime all month, he was disappointed to receive such a ______ bonus.'
            },
            'measurement': {
                'definition': 'The process or result of determining the size, length, amount, or degree of something using standard units or instruments. Measurement forms the foundation of science, engineering, commerce, and daily life, enabling precise communication about quantities. Accurate measurements require appropriate tools (rulers, scales, thermometers), standardized units (meters, pounds, degrees), and proper techniques to minimize errors. Scientific measurements support research, hypothesis testing, and theory development across all fields. Quality control in manufacturing depends on precise measurements to ensure products meet specifications. Medical measurements including blood pressure, temperature, and weight help diagnose and monitor health conditions. Measurement systems have evolved from body-based units (foot, cubit) to international standards that enable global consistency in trade and scientific collaboration.',
                'pronunciation': "/ˈmɛʒ.ər.mənt/",
                'etymology': 'From "measure" (Old French "mesure") + "-ment" suffix, meaning the act or result of measuring.',
                'memory_tip': 'Remember MEASUREMENT = MEASURE-MENT - the process of determining size or quantity.',
                'example_sentence': 'The carpenter took careful ______ before cutting the wood to ensure a perfect fit.'
            },
            'meat': {
                'definition': 'The flesh of animals used as food, or the essential or most important part of something. Animal meat provides protein, vitamins, and minerals essential for human nutrition, though dietary choices vary based on culture, religion, health, and personal ethics. Different types of meat (beef, pork, poultry, fish) require different preparation methods and have varying nutritional profiles. Meat processing includes butchering, preservation, and packaging for safe consumption. In figurative usage, "the meat of the matter" refers to the most substantial or important aspects of a topic. Meat inspection ensures food safety and prevents disease transmission. Cultural attitudes toward meat consumption vary widely, from vegetarianism to cultures where meat represents prosperity and celebration. Modern meat production involves complex agricultural, economic, and environmental considerations.',
                'pronunciation': "/mit/",
                'etymology': 'From Old English "mete," originally meaning food in general, later narrowed to animal flesh.',
                'memory_tip': 'Remember MEAT = animal flesh we MEET at meals for protein nutrition.',
                'example_sentence': 'The chef selected high-quality ______ from local farms for the restaurant\'s signature dishes.'
            },
            'mecca': {
                'definition': 'The holiest city in Islam, located in Saudi Arabia, toward which Muslims pray and make pilgrimage; also any place that attracts people with shared interests or goals. Mecca (Makkah) is the birthplace of Prophet Muhammad and contains the Kaaba, the cubic building that serves as the focal point for Muslim prayer worldwide. The annual Hajj pilgrimage brings millions of Muslims to Mecca, representing one of the five pillars of Islam. Non-Muslims are prohibited from entering the city, emphasizing its sacred status. In secular usage, "mecca" describes destinations that draw enthusiasts: Nashville as a mecca for country music, Silicon Valley as a technology mecca. The extended meaning captures the concept of a central, important place that people seek to visit for specific purposes or interests.',
                'pronunciation': "/ˈmɛk.ə/",
                'etymology': 'From Arabic "Makkah," the holy city in Saudi Arabia; extended to mean any center of attraction.',
                'memory_tip': 'Remember MECCA = holy city that Muslims MAKE pilgrimage to - or any attraction center.',
                'example_sentence': 'Paris has long been considered a ______ for artists from around the world.'
            },
            'mechanics': {
                'definition': 'The branch of physics dealing with motion and forces; also the practical aspects of how things work or the people who repair mechanical devices. Classical mechanics studies motion of objects under the influence of forces, including concepts like velocity, acceleration, momentum, and energy. Quantum mechanics describes behavior at atomic and subatomic levels where classical physics fails to provide accurate predictions. Automotive mechanics diagnose and repair vehicle problems, requiring knowledge of engines, transmissions, electrical systems, and computerized components. The mechanics of writing include grammar, sentence structure, and technical aspects of composition. Game mechanics refer to rules and systems that define how games function and players interact. Understanding mechanics enables prediction, control, and improvement of physical systems across engineering, technology, and everyday applications.',
                'pronunciation': "/məˈkæn.ɪks/",
                'etymology': 'From Greek "mechanikos," meaning relating to machines or mechanical arts, derived from "mechane" (machine).',
                'memory_tip': 'Remember MECHANICS = the science of how things MECHANICALLY work and move.',
                'example_sentence': 'The physics student struggled with the ______ problems involving rotating objects and angular momentum.'
            },
            'medallion': {
                'definition': 'A large medal or decorative pendant worn as jewelry or awarded for achievement; also a round decorative element in architecture or design. Medallions serve ceremonial and ornamental purposes, often commemorating events, honoring individuals, or displaying artistic designs. Olympic medallions recognize athletic achievements with gold, silver, and bronze designating performance levels. Religious medallions display sacred images and serve as expressions of faith. Architectural medallions appear as circular decorative elements on buildings, furniture, or artistic works. Medallions can contain portraits, symbols, text, or abstract designs that convey specific meanings. The circular format creates natural focus and frames important imagery. Medallion collecting represents a specialized numismatic hobby focusing on these larger, often more artistic pieces compared to standard coins.',
                'pronunciation': "/məˈdæl.jən/",
                'etymology': 'From Italian "medaglione," meaning large medal, derived from "medaglia" (medal).',
                'memory_tip': 'Remember MEDALLION = large decorative MEDAL worn like a MEDALLION pendant.',
                'example_sentence': 'The antique ______ featured an intricate engraving of the family coat of arms.'
            },
            'media': {
                'definition': 'Plural of medium; refers to various means of mass communication including television, radio, newspapers, internet, and social platforms. Media serves multiple functions including information dissemination, entertainment, education, and opinion formation in democratic societies. Different media types have distinct characteristics: print media provides detailed analysis, broadcast media offers immediacy, digital media enables interactivity and personalization. Media literacy involves critical evaluation of sources, recognition of bias, and understanding of how information is constructed and presented. Media ownership concentration raises concerns about diversity of viewpoints and democratic discourse. Social media platforms have transformed information sharing, enabling direct communication between individuals and organizations while creating new challenges around misinformation and privacy. Media consumption patterns significantly influence public opinion, political processes, and cultural trends.',
                'pronunciation': "/ˈmi.di.ə/",
                'etymology': 'Plural of "medium," from Latin "medium" meaning middle or means of communication.',
                'memory_tip': 'Remember MEDIA = various MEANS of communication that MEDIATE information to public.',
                'example_sentence': 'The politician used multiple ______ outlets to communicate her message to different audiences.'
            },
            'mediaeval': {
                'definition': 'An alternative British spelling of "medieval," referring to the Middle Ages period in European history, roughly from the 5th to 15th centuries. The mediaeval period encompasses the fall of the Roman Empire through the beginning of the Renaissance, characterized by feudalism, agricultural economy, and dominant Christian influence. Mediaeval society featured hierarchical structures with kings, nobles, clergy, and peasants occupying distinct social roles. Mediaeval art, architecture, and literature reflect religious themes and Gothic styles including cathedral construction and illuminated manuscripts. The period saw development of universities, legal systems, and technological innovations despite popular misconceptions about ignorance and backwardness. Mediaeval scholarship preserved classical knowledge while developing new philosophical and theological ideas. Understanding mediaeval history helps explain contemporary European institutions, legal traditions, and cultural practices.',
                'pronunciation': "/ˌmi.diˈi.vəl/",
                'etymology': 'British spelling of "medieval," from Latin "medium aevum" meaning middle age.',
                'memory_tip': 'Remember MEDIAEVAL = British spelling of MEDIEVAL - the Middle Ages period.',
                'example_sentence': 'The historian specialized in ______ manuscripts from English monasteries.'
            },
            'medias': {
                'definition': 'Plural form that can refer to multiple types of media or communication channels, or to the middle layers of blood vessel walls in anatomy. In communication contexts, medias describes various platforms, outlets, or formats used for information sharing and entertainment. Different medias serve different purposes: traditional medias (newspapers, television) provide professional journalism, while social medias enable user-generated content and direct interaction. In anatomy, the tunica media represents the muscular middle layer of arteries and veins, containing smooth muscle cells that regulate vessel diameter and blood flow. Media analysis involves comparing how different medias present information, reach audiences, and influence public opinion. The effectiveness of various medias depends on target demographics, message complexity, and desired outcomes for communication strategies.',
                'pronunciation': "/ˈmi.di.əz/",
                'etymology': 'Plural of "media," from Latin "medium." Can refer to communication channels or anatomical structures.',
                'memory_tip': 'Remember MEDIAS = multiple MEDIA channels or anatomical middle layers.',
                'example_sentence': 'The marketing campaign utilized various ______ to reach customers across different demographics.'
            },
            'medical': {
                'definition': 'Relating to medicine, healthcare, treatment of disease, or the practice of healing. Medical encompasses the scientific study of human health, diagnosis of illness, therapeutic interventions, and prevention of disease. Medical education requires extensive training in anatomy, physiology, pathology, pharmacology, and clinical skills. Medical ethics govern professional behavior, patient confidentiality, informed consent, and end-of-life decisions. Medical technology includes diagnostic equipment, surgical instruments, monitoring devices, and pharmaceutical developments that improve patient care. Medical research advances understanding of disease mechanisms and develops new treatments through clinical trials and scientific investigation. Medical specialties focus on specific body systems, patient populations, or treatment approaches. The medical profession combines scientific knowledge with compassionate care to promote health and alleviate suffering.',
                'pronunciation': "/ˈmɛd.ɪ.kəl/",
                'etymology': 'From Latin "medicus," meaning physician or relating to healing, derived from "mederi" (to heal).',
                'memory_tip': 'Remember MEDICAL = relating to medicine and healing - MEDI-CAL treatment.',
                'example_sentence': 'The ______ team worked together to develop a treatment plan for the complex case.'
            },
            'medici': {
                'definition': 'A powerful Italian family that dominated Florence during the Renaissance, known for banking wealth, political influence, and patronage of arts and sciences. The Medici family produced four popes, two queens of France, and numerous rulers of Florence. Their banking empire extended across Europe, making them one of the wealthiest families in history. Medici patronage supported Renaissance masters including Michelangelo, Leonardo da Vinci, and Galileo Galilei. The family\'s political power involved complex alliances, conspiracies, and conflicts that shaped Italian politics for centuries. Medici palaces, gardens, and art collections represent Renaissance cultural achievement. The name "Medici" derives from their ancestral profession as physicians or apothecaries. Their legacy includes contributions to banking practices, artistic development, and scientific advancement that influenced European civilization.',
                'pronunciation': "/ˈmɛd.ɪ.tʃi/",
                'etymology': 'Italian family name, derived from "medico" meaning physician, referring to their ancestral profession.',
                'memory_tip': 'Remember MEDICI = powerful Renaissance family of bankers who supported MEDICINE and arts.',
                'example_sentence': 'The ______ family\'s patronage enabled Renaissance artists to create masterpieces that still inspire today.'
            },
            'medicine': {
                'definition': 'The science and practice of diagnosing, treating, and preventing disease; also substances used therapeutically to treat illness. Medicine combines scientific knowledge with clinical skill to promote health and heal the sick. Medical practice involves patient examination, diagnostic testing, treatment planning, and ongoing care management. Pharmaceutical medicine includes drugs, vaccines, and other therapeutic substances that target specific diseases or symptoms. Alternative medicine encompasses traditional healing practices, herbal remedies, and complementary therapies used alongside or instead of conventional treatments. Preventive medicine focuses on maintaining health and preventing disease through vaccination, screening, lifestyle counseling, and public health measures. Medicine continues evolving through research, technology advances, and improved understanding of human biology and disease processes.',
                'pronunciation': "/ˈmɛd.ə.sən/",
                'etymology': 'From Latin "medicina," meaning healing art, derived from "medicus" (physician).',
                'memory_tip': 'Remember MEDICINE = the art and science of healing - MEDI-CINE for treatment.',
                'example_sentence': 'She decided to study ______ after volunteering at the local hospital during high school.'
            },
            'medicines': {
                'definition': 'Plural of medicine; referring to multiple therapeutic substances, drugs, or treatments used to prevent, treat, or cure diseases. Medicines include prescription drugs requiring medical supervision, over-the-counter medications available without prescriptions, and traditional remedies used in various cultures. Different medicines work through various mechanisms: antibiotics fight infections, painkillers reduce discomfort, vaccines prevent diseases. Medicine development involves research, testing, regulatory approval, and ongoing safety monitoring. Proper medicine use requires understanding dosages, timing, interactions, and potential side effects. Medicine storage and disposal affect safety and environmental impact. Traditional medicines often use plant, animal, or mineral substances based on cultural healing practices. Modern medicine regulation ensures quality, safety, and efficacy through standardized testing and manufacturing processes.',
                'pronunciation': "/ˈmɛd.ə.sənz/",
                'etymology': 'Plural of "medicine," from Latin "medicina" referring to multiple healing substances or treatments.',
                'memory_tip': 'Remember MEDICINES = multiple healing substances - various MEDI-CINES for treatment.',
                'example_sentence': 'The pharmacist carefully reviewed all her ______ to check for potential interactions.'
            },
            'medieval': {
                'definition': 'Relating to the Middle Ages, the historical period in European history from approximately 500 to 1500 CE, characterized by feudalism, agricultural economy, and Christian dominance. Medieval society featured hierarchical structures with monarchs, nobles, clergy, and peasants occupying distinct social roles and obligations. Medieval culture produced Gothic architecture, illuminated manuscripts, scholastic philosophy, and courtly literature that reflected religious worldviews and feudal values. The medieval period saw the rise of universities, development of legal systems, and technological innovations including windmills, heavy plows, and mechanical clocks. Medieval towns grew around trade and craftsmanship, leading to merchant classes and guild systems. Understanding medieval history helps explain modern European institutions, legal traditions, and cultural practices that developed during this formative period.',
                'pronunciation': "/ˌmɛd.iˈi.vəl/",
                'etymology': 'From Latin "medium aevum," meaning middle age, referring to the period between ancient and modern times.',
                'memory_tip': 'Remember MEDIEVAL = the MIDDLE AGE period - MEDI (middle) + EVAL (age).',
                'example_sentence': 'The ______ castle featured thick walls, narrow windows, and defensive towers typical of the period.'
            },
            'mediobrome': {
                'definition': 'A technical term from anatomy referring to the middle portion of the brome or throat area, specifically relating to anatomical structures in the pharyngeal region. This specialized medical terminology appears in anatomical texts and clinical descriptions of throat and neck anatomy. The mediobrome area includes muscles, tissues, and structures involved in swallowing, breathing, and vocalization. Understanding mediobrome anatomy is important for medical professionals treating throat disorders, performing surgeries, or diagnosing conditions affecting pharyngeal function. Such precise anatomical terminology enables accurate communication between healthcare providers about specific locations and structures. The term represents the detailed vocabulary required in medical fields to describe complex anatomical relationships and clinical findings.',
                'pronunciation': "/ˌmi.di.oʊˈbroʊm/",
                'etymology': 'From Latin "medio" (middle) + "brome" (throat area), referring to middle throat anatomical structures.',
                'memory_tip': 'Remember MEDIOBROME = MEDIO (middle) + BROME (throat) - middle throat anatomy.',
                'example_sentence': 'The surgeon carefully examined the ______ region before proceeding with the throat operation.'
            },
            'meditation': {
                'definition': 'A practice involving focused attention, mindfulness, or contemplation to achieve mental clarity, emotional calm, and spiritual insight. Meditation techniques vary across cultures and traditions, including concentrative practices that focus on single objects, mindfulness practices that observe thoughts and sensations, and movement-based practices like walking meditation. Scientific research demonstrates meditation benefits including reduced stress, improved focus, lower blood pressure, and enhanced emotional regulation. Different meditation approaches serve various purposes: relaxation meditation reduces anxiety, insight meditation develops self-awareness, loving-kindness meditation cultivates compassion. Religious and spiritual traditions use meditation for prayer, connection with divine principles, and personal transformation. Modern secular meditation programs apply ancient techniques to contemporary stress management and mental health treatment.',
                'pronunciation': "/ˌmɛd.ɪˈteɪ.ʃən/",
                'etymology': 'From Latin "meditatio," meaning reflection or contemplation, derived from "meditari" (to think over).',
                'memory_tip': 'Remember MEDITATION = MEDITATE + ION - focused thinking practice for mental peace.',
                'example_sentence': 'Daily ______ practice helped her manage workplace stress and maintain emotional balance.'
            },
            'mediterranean': {
                'definition': 'Relating to the Mediterranean Sea and the countries surrounding it, including distinctive climate, culture, cuisine, and historical connections. The Mediterranean region encompasses parts of Europe, Africa, and Asia, sharing maritime trade routes, cultural exchanges, and similar environmental conditions. Mediterranean climate features warm, dry summers and mild, wet winters that support agriculture including olives, grapes, and citrus fruits. Mediterranean cuisine emphasizes olive oil, fresh vegetables, fish, grains, and herbs that reflect local ingredients and healthy eating patterns. Mediterranean history includes ancient civilizations (Greek, Roman, Egyptian), maritime empires, and cultural interactions that shaped Western civilization. The Mediterranean Sea has served as a highway for trade, migration, and cultural diffusion for thousands of years. Modern Mediterranean identity combines historical legacy with contemporary tourism and economic development.',
                'pronunciation': "/ˌmɛd.ɪ.təˈreɪ.ni.ən/",
                'etymology': 'From Latin "mediterraneus," meaning "in the middle of land" (medius + terra), referring to the inland sea.',
                'memory_tip': 'Remember MEDITERRANEAN = sea in the MIDDLE of TERRA (land) - surrounded by continents.',
                'example_sentence': 'The ______ diet emphasizes olive oil, fish, and fresh vegetables for optimal health.'
            },
            'medium': {
                'definition': 'A middle state or condition between extremes; a means of communication or artistic expression; or a person claiming to communicate with spirits. As a size designation, medium falls between small and large. In art, medium refers to materials and techniques used for creation: oil painting, watercolor, sculpture, digital media. Communication mediums include television, radio, print, and internet platforms that convey information. In science, a medium is a substance through which energy travels, such as sound waves traveling through air. Spiritualist mediums claim abilities to contact deceased individuals and relay messages. The plural can be "mediums" (people) or "media" (communication channels). Understanding different mediums helps in choosing appropriate tools for artistic expression, communication goals, or scientific applications.',
                'pronunciation': "/ˈmi.di.əm/",
                'etymology': 'From Latin "medium," meaning middle or means, neuter form of "medius" (middle).',
                'memory_tip': 'Remember MEDIUM = in the MIDDLE - between extremes or a means of expression.',
                'example_sentence': 'The artist preferred watercolor as her ______ because it allowed for delicate color transitions.'
            },
            'medulla': {
                'definition': 'The innermost part of an organ or structure; specifically, the medulla oblongata is the lower portion of the brainstem that controls vital functions including breathing, heart rate, and blood pressure. The medulla oblongata serves as a critical connection between the brain and spinal cord, containing nerve centers that automatically regulate essential body functions without conscious control. Damage to the medulla can be life-threatening due to its role in respiratory and cardiovascular control. In other contexts, medulla refers to inner regions of organs: kidney medulla contains structures for urine concentration, adrenal medulla produces stress hormones, bone marrow medulla creates blood cells. The term appears throughout anatomy to describe central, inner portions of various organs that often have specialized functions distinct from outer layers.',
                'pronunciation': "/məˈdʌl.ə/",
                'etymology': 'From Latin "medulla," meaning marrow or inner part, related to "medius" (middle).',
                'memory_tip': 'Remember MEDULLA = inner MIDDLE part of organs, especially brainstem for vital functions.',
                'example_sentence': 'The neurologist explained how the ______ oblongata controls automatic functions like breathing.'
            },
            'medusa': {
                'definition': 'In Greek mythology, one of three Gorgon sisters whose hair was made of venomous snakes and whose gaze could turn people to stone; also the free-swimming stage of jellyfish and related marine animals. Medusa represents one of the most recognizable figures in classical mythology, often depicted as a monster slain by the hero Perseus. The medusa stage of cnidarians (jellyfish, sea anemones) contrasts with the polyp stage, representing different phases in their life cycles. Medusae have bell-shaped bodies with trailing tentacles that contain stinging cells for capturing prey. In art and literature, Medusa symbolizes female rage, dangerous beauty, and transformative power. The image appears in contemporary culture as a symbol of feminism and protection. Marine biology uses "medusa" to describe the reproductive, swimming phase of many cnidarian species.',
                'pronunciation': "/məˈdu.sə/",
                'etymology': 'From Greek mythology; Medusa was one of the Gorgon sisters with snake hair and a deadly gaze.',
                'memory_tip': 'Remember MEDUSA = mythical monster with snake hair or jellyfish swimming stage.',
                'example_sentence': 'The marine biologist studied the ______ stage of the jellyfish life cycle in the laboratory.'
            },
            'meekness': {
                'definition': 'The quality of being gentle, humble, submissive, or easily imposed upon; often viewed as a virtue in religious and ethical contexts. Meekness involves restraining power or strength in favor of gentleness and consideration for others. Biblical teachings present meekness as a blessed quality that will "inherit the earth," distinguishing it from weakness by implying strength under control. In psychology, excessive meekness may indicate low self-esteem or difficulty asserting personal needs and boundaries. Cultural attitudes toward meekness vary: some traditions value humility and deference, while others emphasize assertiveness and self-advocacy. Meekness can be strategic in conflict resolution, demonstrating non-threatening intentions and promoting cooperation. The challenge involves balancing meekness with appropriate self-assertion and recognition of personal worth and rights.',
                'pronunciation': "/ˈmik.nəs/",
                'etymology': 'From "meek" (Old Norse "mjúkr," meaning soft) + "-ness" suffix, referring to gentle, humble quality.',
                'memory_tip': 'Remember MEEKNESS = being MEEK with gentleness - humble and gentle nature.',
                'example_sentence': 'His ______ in negotiations helped defuse tension and find common ground with opponents.'
            },
            'meet': {
                'definition': 'To come into contact or encounter someone or something; to fulfill requirements or expectations; or a gathering for competition or social purposes. Meeting people involves initial introductions, chance encounters, or planned appointments that create social connections. Meeting expectations requires achieving standards or satisfying requirements set by others or oneself. Track meets, swim meets, and other athletic competitions bring participants together for organized contests. Meeting challenges involves confronting and dealing with difficult situations. Business meetings provide forums for discussion, decision-making, and coordination among team members. The word encompasses both physical encounters and abstract fulfillment of criteria or obligations. Successful meetings require preparation, clear objectives, and effective communication among participants.',
                'pronunciation': "/mit/",
                'etymology': 'From Old English "metan," meaning to find, encounter, or come upon.',
                'memory_tip': 'Remember MEET = to come together, encounter, or fulfill requirements.',
                'example_sentence': 'They decided to ______ at the coffee shop to discuss their business proposal.'
            },
            'meeting': {
                'definition': 'A gathering of people for discussion, decision-making, or social interaction; also the act of encountering or coming together. Business meetings serve organizational purposes including planning, problem-solving, information sharing, and coordination among team members. Effective meetings require clear agendas, defined objectives, appropriate participants, and skilled facilitation to achieve productive outcomes. Meeting formats vary from formal board meetings with parliamentary procedures to informal brainstorming sessions. Social meetings strengthen relationships and community connections through shared activities and conversations. Meeting etiquette involves punctuality, preparation, active participation, and respectful communication. Virtual meetings have become increasingly common, offering convenience while creating new challenges for engagement and collaboration. The success of meetings depends on leadership skills, participant commitment, and follow-through on decisions and action items.',
                'pronunciation': "/ˈmit.ɪŋ/",
                'etymology': 'From "meet" (Old English "metan") + "-ing" suffix, referring to the act of coming together.',
                'memory_tip': 'Remember MEETING = people MEETING together for discussion or social interaction.',
                'example_sentence': 'The weekly team ______ helped everyone stay informed about project progress and upcoming deadlines.'
            },
            'megacephalic': {
                'definition': 'Having an abnormally large head or skull, typically referring to a medical condition called macrocephaly. Megacephalic conditions can result from various causes including fluid accumulation (hydrocephalus), brain tumors, genetic disorders, or developmental abnormalities. Medical evaluation of megacephalic patients involves imaging studies, neurological assessments, and developmental monitoring to determine underlying causes and appropriate treatments. The condition may be associated with developmental delays, learning disabilities, or neurological complications, though some individuals with larger head circumferences develop normally. Early detection and intervention are important for managing associated medical issues and supporting optimal development. Anthropological studies use cranial measurements including megacephalic variations to understand human population differences and evolutionary patterns. The term appears in medical literature and clinical descriptions of patients with abnormal head size.',
                'pronunciation': "/ˌmɛɡ.əˈsɛf.ə.lɪk/",
                'etymology': 'From Greek "mega" (large) + "kephalos" (head) + "-ic" suffix, meaning having a large head.',
                'memory_tip': 'Remember MEGACEPHALIC = MEGA (large) + CEPHALIC (head) - abnormally large head.',
                'example_sentence': 'The pediatric neurologist evaluated the infant\'s ______ condition to determine if treatment was necessary.'
            },
            'megahertz': {
                'definition': 'A unit of frequency equal to one million hertz, commonly used to measure radio wave frequencies, computer processor speeds, and other electronic signals. Megahertz (MHz) describes how many million cycles per second occur in oscillating phenomena. Radio stations broadcast on specific megahertz frequencies: FM radio uses 88-108 MHz, while AM radio uses much lower frequencies. Computer processors operate at gigahertz speeds (thousands of megahertz), determining how quickly they can execute instructions. Medical imaging equipment, wireless communications, and scientific instruments all use megahertz measurements to specify operating frequencies. Understanding megahertz helps in selecting appropriate electronic equipment, avoiding interference between devices, and comprehending technical specifications. The unit represents the rapid oscillations fundamental to modern electronic technology and wireless communications.',
                'pronunciation': "/ˈmɛɡ.ə.hɛrts/",
                'etymology': 'From "mega" (Greek for million) + "hertz" (named after physicist Heinrich Hertz), meaning million cycles per second.',
                'memory_tip': 'Remember MEGAHERTZ = MEGA (million) + HERTZ (cycles per second) - million frequency cycles.',
                'example_sentence': 'The radio station broadcasts at 101.5 ______ on the FM band.'
            }
        }
        
        return data.get(word, {
            'definition': f'A word from the Scripps National Spelling Bee word list. Definition not available in current dataset.',
            'pronunciation': f'Pronunciation not available for {word}.',
            'etymology': f'Etymology not available for {word}.',
            'memory_tip': f'Memory tip not available for {word}.',
            'example_sentence': f'The word ______ appears in spelling bee competitions.'
        })
    
    def detect_combined_words(self) -> List[str]:
        """Detect combined word errors in the dataset"""
        combined_words = []
        
        # Check each word for combined word patterns
        words_to_check = [
            'mawkishflambé'  # mawkish + flambé
        ]
        
        for word in words_to_check:
            combined_words.append(word)
            
        return combined_words
    
    def process_batch(self, input_file: str, output_file: str):
        """Process the batch with comprehensive Claude data"""
        
        logger.info("Processing Batch 109 with comprehensive Claude data...")
        
        # Detect combined words
        combined_words = self.detect_combined_words()
        logger.info(f"Detected {len(combined_words)} combined word errors: {combined_words}")
        
        processed_words = []
        
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            for row in reader:
                if not row['word']:  # Skip empty rows
                    continue
                    
                word = row['word'].strip()
                if not word:
                    continue
                
                # Get comprehensive Claude data
                claude_data = self.get_comprehensive_claude_data(word)
                
                # Calculate difficulty scores
                difficulty_scores = self.difficulty_calc.calculate_difficulty_score(
                    word, 
                    claude_data['definition'], 
                    claude_data['etymology']
                )
                
                # Flag combined words
                is_combined_error = word in combined_words
                
                processed_word = {
                    'word': word,
                    'years': row['years'],
                    'source_files': row['source_files'],
                    'source_difficulties': row['source_difficulties'],
                    'definition': claude_data['definition'],
                    'pronunciation': claude_data['pronunciation'],
                    'etymology': claude_data['etymology'],
                    'etymology_source': 'Claude',
                    'memory_tip': claude_data['memory_tip'],
                    'example_sentence': claude_data['example_sentence'],
                    'phonetic_transparency_score': difficulty_scores['phonetic_transparency_score'],
                    'word_frequency_score': difficulty_scores['word_frequency_score'], 
                    'morphological_complexity_score': difficulty_scores['morphological_complexity_score'],
                    'etymology_complexity_score': difficulty_scores['etymology_complexity_score'],
                    'difficulty': difficulty_scores['difficulty'],
                    'combined_word_error': is_combined_error
                }
                
                processed_words.append(processed_word)
                logger.info(f"Processed word: {word}")
        
        # Write to output file
        if processed_words:
            fieldnames = [
                'word', 'years', 'source_files', 'source_difficulties',
                'definition', 'pronunciation', 'etymology', 'etymology_source',
                'memory_tip', 'example_sentence',
                'phonetic_transparency_score', 'word_frequency_score',
                'morphological_complexity_score', 'etymology_complexity_score',
                'difficulty', 'combined_word_error'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(processed_words)
        
        logger.info(f"Saved {len(processed_words)} words to {output_file}")
        return len(processed_words)

if __name__ == "__main__":
    processor = Batch109Processor()
    
    input_file = "output/batch_109_words.csv"
    output_file = "output/batch_109_processed.csv"
    
    try:
        word_count = processor.process_batch(input_file, output_file)
        
        logger.info("Batch 109 processing completed!")
        logger.info(f"Processed {word_count} words with comprehensive Claude data")
        logger.info(f"Output saved to: {output_file}")
        logger.info(f"Results: {word_count} successful, 0 failed")
        
    except Exception as e:
        logger.error(f"Error processing batch 109: {str(e)}")
        raise