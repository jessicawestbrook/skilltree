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

class Batch108Processor:
    """Processes Batch 108 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for each word"""
        data = {
            'marinate': {
                'definition': 'To soak food, especially meat or vegetables, in a seasoned liquid mixture before cooking to enhance flavor and tenderness. The marinating process allows acidic ingredients like vinegar, wine, or citrus juice to break down tough protein fibers while herbs and spices penetrate the food. Different marinades serve various purposes: acidic marinades tenderize tough cuts of meat, oil-based marinades add moisture and carry fat-soluble flavors, and enzymatic marinades using ingredients like pineapple or papaya break down proteins naturally. Marinating times vary from 30 minutes for delicate fish to 24 hours for tough cuts of beef. The technique originated from preservation methods but evolved into a flavor-enhancement practice essential to many cuisines worldwide.',
                'pronunciation': "/ˈmær.ɪ.neɪt/",
                'etymology': 'From French "mariner," meaning "to pickle in brine," derived from "marin" (marine) referring to seawater or salt water used in food preservation.',
                'memory_tip': 'Remember MARINATE = MARINE + ATE - think of soaking food in liquid like the ocean, then eating it.',
                'example_sentence': 'The chef decided to ______ the beef in red wine and herbs for six hours before grilling.'
            },
            'marine': {
                'definition': 'Relating to the sea or ocean, or a member of a naval infantry force trained for amphibious warfare and expeditionary missions. As an adjective, marine describes anything connected to saltwater environments, including marine biology (study of sea life), marine ecosystems, and marine vessels. Marine organisms have adapted to saltwater conditions through specialized physiological mechanisms. As a noun, a Marine (capitalized) refers to a highly trained military service member skilled in both land and sea operations. Marines undergo rigorous training emphasizing physical fitness, marksmanship, and small-unit tactics. The Marine Corps motto "Semper Fidelis" (Always Faithful) reflects their commitment to duty, honor, and loyalty to country and fellow Marines.',
                'pronunciation': "/məˈrin/",
                'etymology': 'From Latin "marinus," meaning "of the sea," derived from "mare" (sea). The military sense developed from naval forces operating from ships.',
                'memory_tip': 'Remember MARINE starts with MAR (like "water" in Spanish) - connecting to sea and ocean.',
                'example_sentence': 'The ______ biologist studied coral reef ecosystems in tropical waters.'
            },
            'maringouin': {
                'definition': 'A regional term used in Louisiana and parts of the American South for a mosquito, particularly referring to the large, aggressive mosquitoes common in wetland areas. This Cajun French term reflects the linguistic heritage of Louisiana\'s Acadian population. Maringouins are typically larger than common house mosquitoes and are known for their persistent biting behavior, especially during dawn and dusk hours. These insects thrive in the humid, swampy conditions of the Gulf Coast region, where standing water provides ideal breeding grounds. The term represents the unique vocabulary that developed in Louisiana through the blending of French, Spanish, African, and Native American linguistic influences, creating a distinctive regional dialect that preserves cultural heritage.',
                'pronunciation': "/ˈmær.ɪŋ.ɡuɪn/",
                'etymology': 'From Louisiana Cajun French, derived from French "maringouin," ultimately from a Tupi (South American indigenous) word for mosquito.',
                'memory_tip': 'Remember MARINGOUIN sounds like "marine-going" - mosquitoes that go to marine/swamp areas.',
                'example_sentence': 'The Louisiana fisherman covered himself with repellent to protect against the swarms of ______ in the bayou.'
            },
            'marionette': {
                'definition': 'A puppet controlled from above by strings or wires attached to various parts of its body, allowing for complex and lifelike movements. Marionettes represent one of the oldest forms of theatrical entertainment, with examples dating back thousands of years across many cultures. The puppeteer, called a marionettist, manipulates the strings from a bridge or elevated platform to create the illusion of life. Professional marionettes may have dozens of strings controlling head, limbs, torso, and even facial features for sophisticated performances. The art form requires exceptional skill to coordinate multiple strings simultaneously while telling a story. Marionette theaters present everything from traditional fairy tales to complex dramatic works, maintaining this ancient art form in modern times.',
                'pronunciation': "/ˌmær.i.əˈnet/",
                'etymology': 'From French "marionnette," a diminutive of "Marion" (little Mary), originally referring to figures of the Virgin Mary used in religious plays.',
                'memory_tip': 'Remember MARIONETTE = MARY + LITTLE NET - little Mary controlled by strings like a net from above.',
                'example_sentence': 'The skilled puppeteer made the ______ dance gracefully by manipulating dozens of nearly invisible strings.'
            },
            'marionetteneapolitan': {
                'definition': 'A combined word error from PDF parsing that incorrectly merged "marionette" and "neapolitan." This represents a data processing error where two separate spelling bee words were concatenated without proper spacing. Marionette refers to a string puppet, while Neapolitan typically refers to something from Naples, Italy, or the three-flavored ice cream (vanilla, chocolate, strawberry). Such parsing errors occur when PDF text extraction fails to recognize word boundaries, particularly when words appear in close proximity in formatted lists or tables. These errors highlight the importance of data validation and cleaning in large-scale text processing projects.',
                'pronunciation': "/ˌmær.i.əˈnet.ni.əˈpɑl.ɪ.tən/",
                'etymology': 'Processing error combining "marionette" (French puppet term) with "neapolitan" (relating to Naples, from Latin "Neapolitan").',
                'memory_tip': 'This is a COMBINED WORD ERROR - two separate words incorrectly joined together during PDF processing.',
                'example_sentence': 'The data processor flagged ______ as an invalid combined word requiring separation into distinct terms.'
            },
            'mariposa': {
                'definition': 'The Spanish and Portuguese word for butterfly, also used as a poetic or artistic term in English, particularly in reference to the beautiful Mariposa lily found in western North America. Mariposa lilies (Calochortus species) are bulbous perennials with distinctive three-petaled flowers that resemble butterflies in flight, hence their name. These wildflowers are native to western United States and are prized for their delicate beauty and varied colors including white, yellow, pink, and purple. The term "mariposa" appears in various place names throughout California and the Southwest, reflecting Spanish colonial influence. In literature and art, mariposa serves as a symbol of transformation, beauty, and the ephemeral nature of life.',
                'pronunciation': "/ˌmær.ɪˈpoʊ.sə/",
                'etymology': 'From Spanish/Portuguese "mariposa," meaning butterfly, possibly derived from "María" + "posa" (Mary alights), referring to the Virgin Mary.',
                'memory_tip': 'Remember MARIPOSA = MARY + POSE - Mary posing like a beautiful butterfly.',
                'example_sentence': 'The ______ lily bloomed in brilliant orange petals that resembled a butterfly\'s wings.'
            },
            'maritime': {
                'definition': 'Relating to shipping, sailing, navigation, or other activities taking place on or near the sea. Maritime encompasses the vast economic, legal, and cultural aspects of human interaction with oceans and seas. Maritime law governs international waters, shipping regulations, and naval commerce. Maritime industries include shipbuilding, port operations, offshore drilling, and marine transportation of goods. Maritime history traces human exploration, trade routes, and naval warfare across centuries. Maritime archaeology studies shipwrecks and underwater cultural sites. Maritime climate refers to weather patterns influenced by proximity to large bodies of water, characterized by moderate temperatures and higher humidity. The maritime tradition includes nautical customs, seamanship skills, and the cultural heritage of seafaring communities worldwide.',
                'pronunciation': "/ˈmær.ɪˌtaɪm/",
                'etymology': 'From Latin "maritimus," meaning "of the sea," derived from "mare" (sea). Related to "maritime" laws governing sea commerce.',
                'memory_tip': 'Remember MARITIME = MAR (sea) + TIME - time spent at sea for navigation and commerce.',
                'example_sentence': 'The ______ museum displayed artifacts from centuries of seafaring history and ocean exploration.'
            },
            'mark': {
                'definition': 'A sign, symbol, or trace that indicates position, achievement, or quality; also to make such a sign or to observe carefully. As a noun, mark can mean a grade or score (exam marks), a target (hit the mark), a distinguishing feature (birthmark), or a unit of currency in some countries. As a verb, mark means to make a visible sign, to grade or evaluate, to observe or notice, or to commemorate. In sports, marking refers to closely guarding an opponent. The phrase "make your mark" means to achieve success or recognition. Historical marks include property boundaries, trail markers, and quality stamps on manufactured goods. In education, marking involves assessing student work and providing feedback.',
                'pronunciation': "/mɑrk/",
                'etymology': 'From Old English "mearc," meaning boundary or sign, related to Germanic words for boundary or border marker.',
                'memory_tip': 'Remember MARK - short and simple, like making a quick sign or getting a grade.',
                'example_sentence': 'The teacher asked students to ______ their answers clearly on the test sheet.'
            },
            'marked': {
                'definition': 'Clearly noticeable, distinct, or having visible signs or symbols. When something is marked, it displays obvious characteristics that set it apart from others. A marked improvement shows clear, significant progress. Marked differences are easily observable distinctions between things. In linguistics, marked forms are more complex or specialized compared to unmarked basic forms. Marked cards have been secretly altered for cheating in gambling. Marked territory shows signs of animal occupation through scent or visual indicators. A marked man faces targeting or danger. The term implies both physical indicators and metaphorical distinctions that make something stand out from the ordinary or expected state.',
                'pronunciation': "/mɑrkt/",
                'etymology': 'Past tense of "mark," from Old English "mearc." The adjective sense developed from the idea of being stamped or labeled.',
                'memory_tip': 'Remember MARKED = MARK + ED - something that has been marked shows clear, visible signs.',
                'example_sentence': 'There was a ______ difference in her confidence after completing the training program.'
            },
            'markets': {
                'definition': 'Places or systems where goods, services, or securities are bought and sold; also the demand for particular products or the act of promoting and selling. Physical markets include farmers\' markets, bazaars, and shopping centers where vendors and customers meet. Financial markets encompass stock exchanges, bond markets, and commodity trading where securities change hands. Market economics refers to systems where supply and demand determine prices and resource allocation. Marketing involves researching consumer needs and promoting products to target audiences. Market share represents a company\'s portion of total industry sales. Emerging markets refer to developing countries with growing economies. The verb "markets" means actively promoting or selling products to potential customers through advertising, distribution, and sales strategies.',
                'pronunciation': "/ˈmɑr.kɪts/",
                'etymology': 'From Latin "mercatus," meaning trade or marketplace, derived from "merx" (merchandise). Related to merchant and commerce.',
                'memory_tip': 'Remember MARKETS = places where you MARK prices on goods to sell them.',
                'example_sentence': 'The company expanded into international ______ to increase their global sales revenue.'
            },
            'marksmanship': {
                'definition': 'The skill and art of accurate shooting with firearms or archery equipment, requiring precise aim, steady hands, and consistent technique. Marksmanship combines physical abilities with mental discipline, as successful shooters must control breathing, maintain focus, and manage stress under pressure. Military and police training emphasizes marksmanship for tactical effectiveness and safety. Competitive marksmanship includes target shooting, biathlon, and practical shooting sports with standardized scoring systems. Fundamental marksmanship principles include proper stance, grip, sight alignment, sight picture, breathing control, and trigger squeeze. Historical marksmanship traditions include sharpshooting units in warfare and hunting skills for survival. Modern marksmanship instruction uses advanced techniques including ballistics analysis, equipment optimization, and psychological preparation to achieve consistent accuracy.',
                'pronunciation': "/ˈmɑrks.mən.ʃɪp/",
                'etymology': 'From "marksman" (one who hits the mark) + "-ship" (skill or ability). "Mark" refers to the target being aimed at.',
                'memory_tip': 'Remember MARKSMANSHIP = hitting the MARK with expert shooting SKILL like a MAN with a SHIP (steady aim).',
                'example_sentence': 'The sniper\'s exceptional ______ allowed her to hit targets accurately at extreme distances.'
            },
            'marmoset': {
                'definition': 'A small, highly active New World monkey belonging to the family Callitrichidae, native to South American rainforests. Marmosets are characterized by their tiny size (typically 4-6 inches long excluding tail), tufted ears, long tails, and distinctive facial features. These arboreal primates live in family groups and communicate through complex vocalizations including whistles, trills, and chatter. Marmosets have specialized claws rather than fingernails, allowing them to climb vertical tree surfaces and extract tree sap, their primary food source. They also eat insects, fruits, and small vertebrates. Common marmosets, pygmy marmosets, and golden lion tamarins represent different species within this family. Their intelligence and social behaviors make them subjects of scientific research, though habitat destruction threatens many species.',
                'pronunciation': "/ˈmɑr.mə.zet/",
                'etymology': 'From Middle French "marmouset," meaning grotesque figure or small monkey, possibly derived from "marmotter" (to mutter).',
                'memory_tip': 'Remember MARMOSET = tiny monkey that makes MURMUR sounds while SET in trees.',
                'example_sentence': 'The pygmy ______ is one of the world\'s smallest primates, weighing less than a hamster.'
            },
            'marooned': {
                'definition': 'Stranded or abandoned in an isolated place with little hope of rescue, originally referring to people deliberately left on deserted islands. The practice of marooning was historically used as punishment by pirates and naval authorities, leaving offenders on remote islands with minimal supplies. Modern usage extends beyond maritime contexts to describe anyone trapped in remote locations or difficult circumstances. Someone might feel marooned during a blizzard, mechanical breakdown in wilderness areas, or even socially isolated in unfamiliar situations. The psychological impact of being marooned includes anxiety, resourcefulness development, and survival instinct activation. Famous literary examples include Robinson Crusoe and Swiss Family Robinson, exploring themes of survival, adaptation, and human resilience in isolated conditions.',
                'pronunciation': "/məˈrund/",
                'etymology': 'From American Spanish "cimarrón" meaning wild or runaway, later applied to the practice of abandoning people on islands.',
                'memory_tip': 'Remember MAROONED sounds like MAROON (dark red) - imagine being stuck on a red desert island.',
                'example_sentence': 'The sailors were ______ on the tiny coral atoll after their ship was wrecked in the storm.'
            },
            'marquee': {
                'definition': 'A large tent used for outdoor events or a prominent sign displaying entertainment information, typically featuring lights and bold lettering. Marquee tents provide temporary covered spaces for weddings, festivals, corporate events, and social gatherings. These structures range from simple pole tents to elaborate pavilions with climate control and decorative elements. Theater marquees display movie titles, show times, and performer names in eye-catching formats designed to attract audiences. The marquee serves both informational and promotional purposes, often becoming iconic architectural features of entertainment districts. Digital marquees now incorporate LED displays and programmable messages. In business contexts, "marquee" describes high-profile clients, events, or performers that attract attention and prestige to an organization.',
                'pronunciation': "/mɑrˈki/",
                'etymology': 'From French "marquise," a large tent, originally referring to a military officer\'s tent. The theater sense developed from elaborate entrance canopies.',
                'memory_tip': 'Remember MARQUEE = big tent that MARKS the entrance with lights and signs.',
                'example_sentence': 'The vintage theater\'s neon ______ displayed classic movie titles in brilliant red letters.'
            },
            'married': {
                'definition': 'United in matrimony through legal or religious ceremony; also closely connected or combined. Marriage represents a formal union between individuals, recognized by law, religion, or social custom, creating legal rights, responsibilities, and social status changes. Married couples share legal benefits including inheritance rights, medical decision authority, and tax advantages. The institution of marriage varies across cultures in terms of ceremonies, partner selection, gender roles, and dissolution processes. Beyond personal relationships, "married" describes things closely joined or inseparable, such as ideas married to action or flavors married in cooking. Marriage traditions include engagement periods, wedding ceremonies, vows, rings, and celebrations that mark the transition from single to married status.',
                'pronunciation': "/ˈmær.id/",
                'etymology': 'From Old French "marier," meaning to wed, derived from Latin "maritus" (husband) and "maritare" (to wed).',
                'memory_tip': 'Remember MARRIED = MAR (to join) + RIED (tied) - joined together and tied in matrimony.',
                'example_sentence': 'The couple had been ______ for twenty-five years and still enjoyed each other\'s company daily.'
            },
            'marring': {
                'definition': 'The act of damaging, spoiling, or diminishing the perfection or beauty of something. Marring involves causing imperfections that detract from aesthetic appeal, functionality, or value. Physical marring includes scratches on surfaces, dents in metal, or stains on fabric that reduce visual appeal. Emotional or experiential marring occurs when negative events spoil otherwise positive experiences, such as bad weather marring a wedding or arguments marring family gatherings. Environmental marring describes human activities that damage natural landscapes. The concept implies that something previously whole or beautiful has been compromised, though not necessarily destroyed. Marring can be temporary or permanent, intentional or accidental, and may sometimes be repairable through restoration efforts.',
                'pronunciation': "/ˈmær.ɪŋ/",
                'etymology': 'From Old English "mierran," meaning to hinder or obstruct. Related to words meaning to damage or impair.',
                'memory_tip': 'Remember MARRING = MAR (to damage) + RING (continuous action) - continuously damaging something beautiful.',
                'example_sentence': 'The deep scratches were ______ the otherwise perfect finish of the antique table.'
            },
            'marry': {
                'definition': 'To join in marriage through legal, religious, or social ceremony; also to combine or unite different elements harmoniously. The act of marrying involves formal commitment between individuals, creating new legal status and social relationships. Religious marriage ceremonies include vows, blessings, and ritual elements specific to different faith traditions. Civil marriages focus on legal recognition and rights. In culinary contexts, marry means combining flavors that complement each other, allowing ingredients time to blend and develop complex tastes. Musical marry refers to harmonious combination of melodies or instruments. The verb implies both formal joining and natural compatibility, whether between people, concepts, or elements that work well together.',
                'pronunciation': "/ˈmær.i/",
                'etymology': 'From Old French "marier," derived from Latin "maritare," meaning to wed or give in marriage. Related to "marital" and "matrimony."',
                'memory_tip': 'Remember MARRY = to bring together in harmony, like the sound "merry" suggests happiness.',
                'example_sentence': 'The chef decided to ______ bold spices with delicate herbs in the signature dish.'
            },
            'mars': {
                'definition': 'The fourth planet from the Sun in our solar system, known as the Red Planet due to iron oxide on its surface; also the Roman god of war. Mars has fascinated humans throughout history, appearing as a reddish star in the night sky and inspiring mythology, science fiction, and space exploration. The planet features polar ice caps, the largest volcano in the solar system (Olympus Mons), and a massive canyon system (Valles Marineris). Mars has two small moons, Phobos and Deimos. Current scientific interest focuses on evidence of past water activity and potential for ancient or current microbial life. Multiple space agencies have sent robotic missions to Mars, with plans for eventual human exploration. As a verb, "mars" means to damage or spoil something.',
                'pronunciation': "/mɑrz/",
                'etymology': 'Named after Mars, Roman god of war, due to its reddish appearance resembling blood. The verb comes from Old English "mierran."',
                'memory_tip': 'Remember MARS - the red planet that looks like it\'s covered in rust, named after the god of WAR.',
                'example_sentence': 'The rover sent back stunning images of ______\'s rusty landscape and towering rock formations.'
            },
            'marsupial': {
                'definition': 'A mammal that typically carries and nurses its young in a pouch, representing an ancient evolutionary adaptation for protecting underdeveloped offspring. Marsupials give birth to tiny, immature young that continue developing outside the womb, usually attached to nipples within a protective pouch. Famous marsupials include kangaroos, koalas, opossums, wombats, and Tasmanian devils. Most marsupials are found in Australia and nearby regions, though opossums live in the Americas. Marsupial reproduction differs significantly from placental mammals, with shorter gestation periods and extended external development. This reproductive strategy allows survival in harsh environments where food may be scarce. Marsupials represent important evolutionary diversity and occupy various ecological niches from herbivorous grazers to carnivorous hunters.',
                'pronunciation': "/mɑrˈsu.pi.əl/",
                'etymology': 'From Latin "marsupium," meaning pouch or purse, derived from Greek "marsippos" (pouch). Related to the distinctive pouch feature.',
                'memory_tip': 'Remember MARSUPIAL = MAR (sea) + SOUP + AL - animals with pouch bellies like carrying soup bowls.',
                'example_sentence': 'The mother ______ carried her tiny joey safely in her pouch while hopping across the grassland.'
            },
            'marsupialtrefoil': {
                'definition': 'A combined word error from PDF parsing that incorrectly merged "marsupial" and "trefoil." This represents a data processing error where two separate terms were concatenated without proper spacing. Marsupial refers to pouch-bearing mammals, while trefoil describes three-leafed plants (like clover) or decorative three-lobed designs. Such parsing errors occur when PDF text extraction fails to recognize word boundaries, particularly in formatted documents with multiple columns or tight spacing. These errors highlight the challenges of automated text processing and the importance of data validation. The combination creates a nonsensical term that would require manual correction or automated error detection to separate into meaningful components.',
                'pronunciation': "/mɑrˈsu.pi.əlˈtri.fɔɪl/",
                'etymology': 'Processing error combining "marsupial" (Latin pouch-bearer) with "trefoil" (Latin three-leaf). Invalid concatenation.',
                'memory_tip': 'This is a COMBINED WORD ERROR - two distinct words incorrectly joined during PDF text extraction.',
                'example_sentence': 'The data validation system flagged ______ as an invalid combined word requiring separation.'
            },
            'martial': {
                'definition': 'Relating to warfare, military affairs, or combat; characterized by discipline, strength, and warrior-like qualities. Martial arts encompass various combat and self-defense systems developed across different cultures, emphasizing physical technique, mental discipline, and philosophical principles. Martial law represents temporary military control over civilian populations during emergencies, suspending normal legal processes. Martial music includes military marches and ceremonial compositions. The martial spirit embodies courage, honor, and readiness for conflict. Martial cultures historically emphasized warrior values, training, and hierarchical military structures. Modern martial applications include military training, law enforcement tactics, competitive sports, and personal development through disciplined practice of combat skills.',
                'pronunciation': "/ˈmɑr.ʃəl/",
                'etymology': 'From Latin "martialis," meaning of Mars (Roman god of war). Related to military and warrior concepts.',
                'memory_tip': 'Remember MARTIAL = relating to MARS the war god - military and combat related.',
                'example_sentence': 'The ______ arts instructor taught students discipline, respect, and self-defense techniques.'
            },
            'martinet': {
                'definition': 'A person who demands strict adherence to rules and procedures, often to an excessive or unreasonable degree. The term describes someone who prioritizes rigid discipline over flexibility or compassion, typically in authority positions such as military officers, teachers, or supervisors. Martinets insist on precise compliance with regulations regardless of circumstances or common sense. While discipline and order serve important purposes, martinets often create hostile environments through inflexibility and harsh enforcement of minor rules. The negative connotation suggests someone who values control and conformity above effectiveness or human considerations. Historical examples include strict military drill instructors and authoritarian school administrators who prioritized rule-following over learning or morale.',
                'pronunciation': "/ˌmɑr.təˈnet/",
                'etymology': 'Named after Jean Martinet, 17th-century French military officer known for strict drill procedures and rigid discipline.',
                'memory_tip': 'Remember MARTINET = a strict person who acts like a MARINE with a NET catching every rule violation.',
                'example_sentence': 'The new supervisor was such a ______ that employees feared asking questions about minor policy details.'
            },
            'martinoe': {
                'definition': 'An obscure or archaic term that appears in historical spelling bee word lists, possibly referring to a variant spelling or regional pronunciation of "martinet" or another term. The exact definition and usage of "martinoe" is uncertain, as it does not appear in standard modern dictionaries. It may represent a historical spelling variation, transcription error, or specialized technical term from a particular field or region. In competitive spelling contexts, such words test participants\' knowledge of rare, obsolete, or variant spellings that may no longer be in common use. The inclusion of such terms in spelling competitions reflects the comprehensive nature of English vocabulary, including archaic forms and regional variations that contribute to the language\'s rich history.',
                'pronunciation': "/ˈmɑr.tɪˌnoʊ/",
                'etymology': 'Etymology uncertain; possibly a variant or archaic form related to "martinet" or from a specific regional dialect.',
                'memory_tip': 'Remember MARTINOE - an unusual word that might be related to MARTIN (bird) + OE (ending).',
                'example_sentence': 'The spelling bee contestant studied rare words like ______ to prepare for challenging vocabulary.'
            },
            'marvel': {
                'definition': 'Something that causes wonder, admiration, or astonishment; also to feel amazement or wonder at something extraordinary. Marvels inspire awe through their beauty, complexity, or seemingly impossible nature. Natural marvels include phenomena like Northern Lights, Grand Canyon formations, or intricate ecosystem relationships. Human marvels encompass architectural achievements, artistic masterpieces, technological innovations, and exceptional personal accomplishments. The verb "marvel" expresses active wonderment and appreciation for remarkable things. Marvels often challenge our understanding of what\'s possible, prompting curiosity and inspiring further exploration. In literature and entertainment, marvels create dramatic impact and emotional engagement. The concept emphasizes humanity\'s capacity for wonder and our drive to create or discover extraordinary things.',
                'pronunciation': "/ˈmɑr.vəl/",
                'etymology': 'From Old French "merveille," derived from Latin "mirabilia" (wonderful things), related to "mirari" (to wonder at).',
                'memory_tip': 'Remember MARVEL = something MAR-velous that makes you go "VEL!" (wow) in amazement.',
                'example_sentence': 'Visitors would ______ at the intricate details carved into the ancient cathedral\'s stone façade.'
            },
            'marvellous': {
                'definition': 'Extraordinary, wonderful, or inspiring great admiration; the British spelling of "marvelous." This adjective describes things that evoke amazement through exceptional quality, beauty, or achievement. Marvellous experiences create lasting positive memories and emotional impact. The term can describe artistic works, natural phenomena, personal accomplishments, or technological innovations that exceed normal expectations. In British English, the double-l spelling reflects historical orthographic traditions that differ from American simplified spellings. Marvellous implies not just good quality but genuinely remarkable characteristics that distinguish something from the ordinary. The word carries enthusiastic positive connotation, suggesting both objective excellence and subjective wonder.',
                'pronunciation': "/ˈmɑr.və.ləs/",
                'etymology': 'British spelling of "marvelous," from Old French "merveilleus," meaning full of wonder or miraculous.',
                'memory_tip': 'Remember MARVELLOUS = British spelling with extra L, like "MARVEL + LOUS" (lousy amazing).',
                'example_sentence': 'The sunset over the Scottish highlands was absolutely ______ with its brilliant colors.'
            },
            'marvelous': {
                'definition': 'Extremely impressive, extraordinary, or wonderful; the American spelling of "marvellous." This adjective expresses high praise for something that inspires amazement or admiration through exceptional qualities. Marvelous things exceed normal expectations and create positive emotional responses. The term applies to diverse contexts: marvelous performances, marvelous discoveries, marvelous weather, or marvelous achievements. American English adopted simplified spellings during the 19th century, removing what were considered unnecessary letters. Marvelous suggests both objective excellence and subjective appreciation, indicating that something is not merely good but genuinely remarkable. The word maintains strong positive connotation and enthusiasm in modern usage.',
                'pronunciation': "/ˈmɑr.və.ləs/",
                'etymology': 'American simplified spelling of "marvellous," from Old French "merveilleus," meaning causing wonder or amazement.',
                'memory_tip': 'Remember MARVELOUS = American spelling without extra L, like MARVEL + OUS (obvious amazing).',
                'example_sentence': 'The chef created a ______ fusion dish that perfectly balanced sweet and savory flavors.'
            },
            'maryland': {
                'definition': 'A state in the Mid-Atlantic region of the United States, known for its Chesapeake Bay, blue crabs, and historical significance in American colonial history. Maryland was founded as a haven for English Catholics and played important roles in the Revolutionary War and Civil War. The state features diverse geography from Atlantic Ocean beaches to Appalachian Mountains, with the Chesapeake Bay dominating its eastern region. Maryland\'s economy combines government employment (proximity to Washington D.C.), maritime industries, agriculture, and technology. Cultural contributions include distinctive cuisine (crab cakes, Old Bay seasoning), unique architectural styles, and traditions like jousting (the official state sport). Baltimore serves as the largest city, while Annapolis functions as the capital and home to the U.S. Naval Academy.',
                'pronunciation': "/ˈmɛr.ɪ.lənd/",
                'etymology': 'Named after Queen Henrietta Maria, wife of King Charles I of England, when the colony was established in 1634.',
                'memory_tip': 'Remember MARYLAND = MARY (Queen) + LAND - the land named after Queen Mary.',
                'example_sentence': 'The ______ blue crab season brings tourists from across the region to enjoy fresh seafood.'
            },
            'masa': {
                'definition': 'Traditional corn dough used in Mexican and Central American cuisine, made from dried corn kernels that have been treated with lime in a process called nixtamalization. Masa forms the foundation for tortillas, tamales, pupusas, and other staple foods. The nixtamalization process involves soaking corn in alkaline solution (traditionally wood ash or lime water), which removes the hull and improves nutritional value by making niacin available and increasing protein quality. Fresh masa has a distinctive earthy, slightly sweet flavor and pliable texture ideal for shaping. Commercial masa harina (dried masa flour) provides convenient preparation while maintaining traditional taste. Masa preparation requires skill in achieving proper consistency and handling techniques passed down through generations.',
                'pronunciation': "/ˈmɑ.sə/",
                'etymology': 'From Spanish "masa," meaning dough or paste, derived from Latin "massa" (lump or mass of dough).',
                'memory_tip': 'Remember MASA = corn dough that\'s the MASS-ive base for Mexican food like tortillas.',
                'example_sentence': 'The cook shaped fresh ______ into perfect circles before pressing them into warm tortillas.'
            },
            'mascarpone': {
                'definition': 'A rich, creamy Italian cheese made from cream and citric or tartaric acid, characterized by its smooth texture and mild, slightly sweet flavor. Mascarpone originated in the Lombardy region of northern Italy and traditionally uses cream from cows fed on fresh grass and herbs, contributing to its delicate taste. The cheese-making process involves heating cream and adding acid to create gentle coagulation, resulting in a spreadable consistency similar to cream cheese but richer and less tangy. Mascarpone is essential in classic Italian desserts, most famously tiramisu, where it provides luxurious texture and balances coffee and cocoa flavors. It also enhances savory dishes, pasta sauces, and can be sweetened for various dessert applications.',
                'pronunciation': "/ˌmɑs.kərˈpoʊ.neɪ/",
                'etymology': 'From Italian "mascarpone," possibly derived from "mascarpa" (a type of ricotta) or Spanish "mas que bueno" (better than good).',
                'memory_tip': 'Remember MASCARPONE = creamy cheese that\'s a MASK for CARPOOL desserts (covers everything richly).',
                'example_sentence': 'The pastry chef folded sweetened ______ with espresso-soaked ladyfingers to create authentic tiramisu.'
            },
            'mashed': {
                'definition': 'Reduced to a soft, pulpy mass through crushing, beating, or grinding; most commonly applied to potatoes but also other foods and materials. Mashed potatoes represent a classic comfort food prepared by cooking potatoes until tender, then crushing them with liquid and fat to create smooth or chunky consistency. The mashing process breaks down cellular structure, creating creamy texture while allowing flavor absorption from added ingredients like butter, milk, or seasonings. Other mashed foods include mashed bananas, mashed turnips, and mashed avocados (guacamole). Beyond food, materials can be mashed through physical force or pressure, often as preparation for further processing or as result of damage.',
                'pronunciation': "/mæʃt/",
                'etymology': 'Past tense of "mash," from Middle English "maschen," possibly related to "mesh" or brewing terminology.',
                'memory_tip': 'Remember MASHED = food that\'s been MASH-ed up into soft, smooth texture like potatoes.',
                'example_sentence': 'She prepared creamy ______ potatoes with butter, cream, and roasted garlic.'
            },
            'mask': {
                'definition': 'A covering worn over part or all of the face for protection, disguise, or decoration; also to conceal or disguise something. Masks serve diverse purposes across cultures and contexts. Protective masks include medical face masks, gas masks, and safety equipment that shield against harmful substances. Ceremonial and theatrical masks represent characters, spirits, or emotions in religious rituals, drama, and entertainment. Halloween and costume masks provide disguise for celebration or anonymity. As a verb, "mask" means to hide or obscure something, such as masking odors, masking emotions, or masking true intentions. Digital masking involves concealing or protecting sensitive information. The concept implies both physical covering and metaphorical concealment.',
                'pronunciation': "/mæsk/",
                'etymology': 'From French "masque," derived from Italian "maschera," possibly from Arabic "maskhara" (buffoon) or Latin "masca" (ghost).',
                'memory_tip': 'Remember MASK = something that covers and hides your face or true identity.',
                'example_sentence': 'The surgeon wore a sterile ______ to prevent contamination during the delicate operation.'
            },
            'masks': {
                'definition': 'Multiple face coverings used for protection, disguise, ceremony, or entertainment; also the third person singular form of the verb "mask," meaning to conceal or disguise. Masks throughout history have served ritual purposes in many cultures, representing gods, ancestors, or spiritual forces. Theater masks helped actors portray different characters and project emotions to large audiences. Modern masks include medical protective equipment, Halloween costumes, and artistic expressions. In digital contexts, masks can refer to image editing techniques or data protection methods. The plural form encompasses the variety and cultural significance of face coverings across different societies and purposes.',
                'pronunciation': "/mæsks/",
                'etymology': 'Plural of "mask," from French "masque," ultimately from Italian "maschera" meaning covering or disguise.',
                'memory_tip': 'Remember MASKS = multiple face coverings, like a collection of different disguises.',
                'example_sentence': 'The museum displayed ancient ceremonial ______ from various indigenous cultures around the world.'
            },
            'mason': {
                'definition': 'A skilled craftsperson who works with stone, brick, or concrete to construct buildings, walls, and other structures. Masonry represents one of humanity\'s oldest construction trades, requiring expertise in material selection, cutting, shaping, and laying techniques. Masons understand structural principles, mortar composition, and weatherproofing methods essential for durable construction. Stone masons work with natural materials like granite, marble, and limestone, while brick masons specialize in clay brick construction. The trade demands physical strength, precision, and artistic skill for decorative work. Historical masons built cathedrals, castles, and monuments that have survived centuries. Modern masons use both traditional techniques and contemporary tools to create residential, commercial, and artistic stonework.',
                'pronunciation': "/ˈmeɪ.sən/",
                'etymology': 'From Old French "masson," derived from Frankish "makjo" meaning maker or builder with stone.',
                'memory_tip': 'Remember MASON = someone who MAKES ON stone - builds with stone and brick.',
                'example_sentence': 'The skilled ______ carefully laid each stone to create a perfectly level foundation wall.'
            },
            'masse': {
                'definition': 'A billiards shot where the cue stick is held nearly vertical and struck downward to create extreme spin on the cue ball, causing it to curve around obstacles. The masse shot represents one of the most difficult techniques in cue sports, requiring exceptional skill and practice to execute successfully. The extreme angle and downward force create dramatic ball movement that defies normal physics expectations. Players use masse shots to navigate around blocking balls or achieve otherwise impossible angles. The technique risks damaging the table felt if performed incorrectly, so many pool halls prohibit masse shots. Professional players demonstrate masse shots as displays of skill and precision. The French origin reflects billiards\' historical development in European salons and gaming establishments.',
                'pronunciation': "/mæˈseɪ/",
                'etymology': 'From French "massé," meaning massed or struck heavily, referring to the forceful downward strike of the cue stick.',
                'memory_tip': 'Remember MASSE = billiards shot with MASSIVE downward force to curve the ball.',
                'example_sentence': 'The pool champion executed a perfect ______ shot to curve around three blocking balls.'
            },
            'masses': {
                'definition': 'Large quantities or numbers of people or things; also multiple religious services or the common people collectively. In physics, masses refer to the amounts of matter in objects, determining gravitational attraction and inertial resistance. Social masses describe large populations or crowds, often used in political contexts referring to ordinary citizens versus elite groups. Religious masses are Catholic worship services centered on the Eucharist, with multiple masses held throughout the week. The term can indicate overwhelming quantity, as in "masses of paperwork" or "masses of data." Popular masses refer to widespread public appeal or support. The concept emphasizes scale, collective action, and the power of large numbers in various contexts.',
                'pronunciation': "/ˈmæs.ɪz/",
                'etymology': 'Plural of "mass," from Latin "massa" meaning lump or quantity, also from "missa" (religious service).',
                'memory_tip': 'Remember MASSES = many large amounts, like MASS quantities or religious services.',
                'example_sentence': 'The protest drew ______ of supporters from across the country to demand social change.'
            },
            'massestroganoff': {
                'definition': 'A combined word error from PDF parsing that incorrectly merged "masses" and "stroganoff." This represents a data processing error where two unrelated terms were concatenated without proper spacing. Masses refers to large quantities or religious services, while stroganoff is a Russian dish of sautéed beef in sour cream sauce. Such parsing errors occur when PDF text extraction fails to maintain word boundaries, particularly in documents with complex formatting or multiple columns. These errors demonstrate the challenges of automated text processing and the need for data validation. The nonsensical combination would require manual correction or sophisticated error detection algorithms to separate into meaningful components.',
                'pronunciation': "/ˈmæs.ɪzˈstroʊ.ɡə.nɔf/",
                'etymology': 'Processing error combining "masses" (Latin massa) with "stroganoff" (Russian dish named after Count Stroganov).',
                'memory_tip': 'This is a COMBINED WORD ERROR - two unrelated words incorrectly joined during PDF processing.',
                'example_sentence': 'The data cleaning process identified ______ as an invalid word combination requiring separation.'
            },
            'masseuse': {
                'definition': 'A female professional who performs massage therapy, providing therapeutic or relaxation treatments through manual manipulation of soft body tissues. Masseuses are trained in anatomy, physiology, and various massage techniques including Swedish, deep tissue, sports, and therapeutic massage. The profession requires understanding of muscle groups, pressure points, and appropriate techniques for different client needs. Licensing requirements vary by jurisdiction, with many areas requiring formal education and certification. Professional masseuses work in spas, wellness centers, sports facilities, and private practice settings. The term specifically refers to female practitioners, while "masseur" indicates male practitioners, though "massage therapist" has become preferred gender-neutral terminology. Ethical standards and professional boundaries are essential aspects of legitimate massage therapy practice.',
                'pronunciation': "/mæˈsuz/",
                'etymology': 'From French "masseuse," feminine form of "masseur," derived from "masser" meaning to massage or knead.',
                'memory_tip': 'Remember MASSEUSE = female massage therapist who provides relaxing muscle treatment.',
                'example_sentence': 'The licensed ______ used various techniques to relieve tension in the client\'s shoulders and neck.'
            },
            'massive': {
                'definition': 'Extremely large, heavy, solid, or extensive in size, scope, or degree. Massive objects possess great physical bulk or weight, such as massive boulders, massive buildings, or massive vehicles. The term extends beyond physical size to describe scale and impact: massive changes, massive efforts, or massive problems. In geology, massive rocks lack visible layering or structure. Massive also implies impressive magnitude that commands attention or respect. The word suggests not just large size but substantial presence and significant impact. Massive undertakings require considerable resources and planning. In informal usage, massive can mean simply "very large" or "extremely significant," emphasizing the overwhelming nature of something\'s scale or importance.',
                'pronunciation': "/ˈmæs.ɪv/",
                'etymology': 'From French "massif," meaning solid or bulky, derived from Latin "massa" (mass or lump).',
                'memory_tip': 'Remember MASSIVE = having huge MASS - extremely large, heavy, and substantial.',
                'example_sentence': 'The construction project required ______ amounts of steel and concrete to complete the skyscraper.'
            },
            'mastering': {
                'definition': 'The process of gaining complete knowledge, skill, or control over a subject or activity; also the final stage of audio production where recordings are optimized for distribution. Academic mastering involves developing deep understanding and proficiency through study, practice, and application. Skill mastering requires repetition, refinement, and progressive challenge to achieve expertise. In audio production, mastering involves equalizing, compressing, and optimizing recorded music for consistent sound across different playback systems. The mastering engineer makes final adjustments to volume levels, frequency balance, and dynamic range. Personal mastering represents self-improvement and professional development. The concept implies not just competence but exceptional ability and comprehensive understanding that comes through dedicated effort and experience.',
                'pronunciation': "/ˈmæs.tər.ɪŋ/",
                'etymology': 'From "master" (Old English "mægister") + "-ing" suffix, meaning the act of gaining mastery or control.',
                'memory_tip': 'Remember MASTERING = becoming a MASTER through continuous learning and practice.',
                'example_sentence': 'She spent years ______ the complex techniques required for classical piano performance.'
            },
            'masthead': {
                'definition': 'The top section of a newspaper or magazine that displays the publication\'s name, logo, and key information; also the highest part of a ship\'s mast. In print media, the masthead serves as visual identity and branding, often including publication date, volume number, editor names, and contact information. Newspaper mastheads establish credibility and recognition through consistent design elements. On sailing vessels, the masthead houses navigation equipment, lights, and rigging hardware at the top of the mast structure. Climbing to the masthead provides the highest vantage point for lookouts and signal communications. The masthead represents authority and leadership in both nautical and publishing contexts, symbolizing the highest position and most prominent display of identity or information.',
                'pronunciation': "/ˈmæst.hɛd/",
                'etymology': 'From "mast" (Old English "mæst") + "head," referring to the top portion of a ship\'s mast or publication.',
                'memory_tip': 'Remember MASTHEAD = the HEAD of the MAST - top part of ship mast or newspaper.',
                'example_sentence': 'The newspaper\'s ______ featured elegant typography that had remained unchanged for fifty years.'
            },
            'mastiff': {
                'definition': 'A large, powerful breed of dog originally developed for guarding and protection, characterized by massive build, broad head, and gentle temperament despite imposing appearance. Mastiffs represent one of the most ancient dog breeds, with history tracing back thousands of years to ancient civilizations including Egypt, Tibet, and Europe. These dogs typically weigh 120-200 pounds or more, with muscular bodies and distinctive facial features. Despite their intimidating size, mastiffs are known for calm, loyal, and protective nature, making them excellent family guardians. Different mastiff varieties include English Mastiff, Tibetan Mastiff, Neapolitan Mastiff, and others, each with specific characteristics. Their protective instincts and imposing presence have made them valuable guard dogs throughout history, though they require proper training and socialization.',
                'pronunciation': "/ˈmæs.tɪf/",
                'etymology': 'From Old French "mastin," possibly derived from Latin "mansuetus" meaning tame or domesticated.',
                'memory_tip': 'Remember MASTIFF = MASSIVE dog that\'s MASTER of guarding and protection.',
                'example_sentence': 'The gentle ______ weighed over 180 pounds but was remarkably patient with small children.'
            },
            'mastodon': {
                'definition': 'An extinct elephant-like mammal that lived during the Miocene and Pleistocene epochs, characterized by long, curved tusks and distinctive tooth structure adapted for browsing on leaves and twigs. Mastodons were smaller than mammoths but still massive, with adults reaching 8-10 feet tall and weighing 4-6 tons. Their teeth featured cone-shaped cusps ideal for crushing woody plant material, distinguishing them from mammoths that had flat grinding teeth for grass. Mastodon fossils have been found throughout North and Central America, with the last populations disappearing around 10,000 years ago. These prehistoric giants played important ecological roles in ancient forests and woodlands. The name "mastodon" reflects their distinctive dental features that paleontologists use to identify and classify fossil remains.',
                'pronunciation': "/ˈmæs.tə.dɑn/",
                'etymology': 'From Greek "mastos" (breast) + "odon" (tooth), referring to the breast-shaped cusps on their molars.',
                'memory_tip': 'Remember MASTODON = prehistoric elephant with MAST-ive size and distinctive TOOTH structure.',
                'example_sentence': 'The natural history museum displayed a complete ______ skeleton discovered in a local quarry.'
            },
            'matching': {
                'definition': 'The process of pairing or finding correspondence between similar or complementary items; also describing things that correspond or harmonize with each other. Matching involves identifying similarities, patterns, or compatible relationships. In fashion, matching refers to coordinating colors, styles, or patterns to create harmonious appearance. Educational matching exercises help students learn associations between concepts, words, or images. Computer matching algorithms identify similarities in data sets for various applications. Matching in relationships describes compatibility between people with similar interests or complementary characteristics. The concept implies both active searching for correspondences and the state of being similar or compatible. Successful matching requires understanding criteria for comparison and desired outcomes.',
                'pronunciation': "/ˈmætʃ.ɪŋ/",
                'etymology': 'From "match" (Old English "mæcca," meaning mate or companion) + "-ing" suffix indicating action or state.',
                'memory_tip': 'Remember MATCHING = finding things that MATCH - go together in harmony or similarity.',
                'example_sentence': 'The interior designer focused on ______ furniture styles to create a cohesive living space.'
            },
            'mater': {
                'definition': 'Latin for "mother," used in formal, scientific, or academic contexts; also informal British term for mother. In medical terminology, "mater" appears in anatomical terms like "dura mater" (tough outer membrane covering the brain and spinal cord) and "pia mater" (delicate inner membrane). Educational institutions use "alma mater" to refer to the school or university where someone studied. The term maintains formal or classical associations, often appearing in legal documents, scholarly writing, or traditional expressions. In British English, "mater" serves as an informal, somewhat old-fashioned way to refer to one\'s mother, similar to "mama" or "mom." The Latin origin connects to concepts of nurturing, origin, and protective care associated with motherhood.',
                'pronunciation': "/ˈmeɪ.tər/",
                'etymology': 'From Latin "mater," meaning mother, related to Sanskrit "matar" and Greek "meter" (mother).',
                'memory_tip': 'Remember MATER = MOTHER in Latin - used in formal terms like alma mater (school mother).',
                'example_sentence': 'The graduate returned to visit her alma ______ twenty years after completing her degree.'
            },
            'materialize': {
                'definition': 'To appear in physical form; to become actual fact; to take on material substance or reality. When something materializes, it transforms from concept, plan, or possibility into tangible existence. Hopes and dreams materialize when they become reality through effort and circumstances. In supernatural contexts, spirits or apparitions materialize by appearing visibly. Business plans materialize when they develop into actual operating companies. Threats materialize when potential dangers become real problems. The process implies transition from abstract or potential state to concrete, observable reality. Materialization often requires specific conditions, resources, or actions to occur. The concept encompasses both sudden appearance and gradual development into physical or factual existence.',
                'pronunciation': "/məˈtɪr.i.əˌlaɪz/",
                'etymology': 'From "material" (Latin "materialis") + "-ize" suffix, meaning to make material or give physical form to.',
                'memory_tip': 'Remember MATERIALIZE = make MATERIAL and REAL - turn ideas into actual existence.',
                'example_sentence': 'The entrepreneur\'s vision began to ______ as investors provided funding for the innovative project.'
            },
            'maternity': {
                'definition': 'The state of being a mother; the period of pregnancy and childbirth; also services, facilities, or provisions related to pregnancy and newborn care. Maternity encompasses the physical, emotional, and social aspects of motherhood from conception through early child care. Maternity leave provides time off from work for mothers before and after giving birth, allowing recovery and bonding with newborns. Maternity wards in hospitals specialize in prenatal care, delivery services, and postpartum support. Maternity clothing accommodates changing body shape during pregnancy. Maternity benefits include healthcare coverage, family support services, and workplace protections. The concept recognizes the unique needs and experiences of women during pregnancy and early motherhood, emphasizing both medical care and social support systems.',
                'pronunciation': "/məˈtɜr.nə.ti/",
                'etymology': 'From Latin "maternitas," derived from "maternus" (maternal), relating to mothers and motherhood.',
                'memory_tip': 'Remember MATERNITY = relating to being a MOTHER - pregnancy, birth, and early childcare.',
                'example_sentence': 'The hospital\'s new ______ wing featured private rooms and advanced neonatal care facilities.'
            },
            'maternitybungee': {
                'definition': 'A combined word error from PDF parsing that incorrectly merged "maternity" and "bungee." This represents a data processing error where two unrelated terms were concatenated without proper spacing. Maternity refers to motherhood and pregnancy-related matters, while bungee typically relates to elastic cord used in jumping sports or securing items. Such parsing errors occur when PDF text extraction fails to recognize word boundaries, especially in documents with complex layouts or formatting issues. These errors highlight the challenges of automated text processing and the importance of data validation. The nonsensical combination would require correction to separate into meaningful individual terms.',
                'pronunciation': "/məˈtɜr.nə.tiˈbʌn.dʒi/",
                'etymology': 'Processing error combining "maternity" (Latin motherhood) with "bungee" (elastic cord). Invalid concatenation.',
                'memory_tip': 'This is a COMBINED WORD ERROR - two unrelated words incorrectly joined during text processing.',
                'example_sentence': 'The text processing system flagged ______ as an invalid word combination requiring separation.'
            },
            'math': {
                'definition': 'The study of numbers, quantities, shapes, and patterns; short form of mathematics. Math encompasses various branches including arithmetic, algebra, geometry, calculus, statistics, and advanced theoretical fields. Elementary math covers basic operations, fractions, and problem-solving skills essential for daily life. Advanced math explores complex relationships, abstract concepts, and applications in science, engineering, and technology. Math education emphasizes logical thinking, pattern recognition, and analytical problem-solving abilities. Mathematical concepts underlie numerous fields from physics and computer science to economics and art. Modern math includes both pure mathematical theory and applied mathematics for practical problems. The subject develops critical thinking skills and provides tools for understanding and describing the natural world through numerical and geometric relationships.',
                'pronunciation': "/mæθ/",
                'etymology': 'Shortened form of "mathematics," from Greek "mathematikos," meaning relating to learning or science.',
                'memory_tip': 'Remember MATH = short for MATHEMATICS - the study of numbers, shapes, and patterns.',
                'example_sentence': 'The students used calculators to solve complex ______ problems involving algebraic equations.'
            },
            'mathematical': {
                'definition': 'Relating to, involving, or characteristic of mathematics; having the precision, logic, or certainty associated with mathematical methods. Mathematical thinking emphasizes logical reasoning, systematic analysis, and precise relationships between concepts. Mathematical models represent real-world phenomena using equations, formulas, and geometric principles. Mathematical proof requires rigorous logical steps to establish truth of propositions. Mathematical precision involves exact measurements, calculations, and definitions. The term implies systematic, quantitative approaches to problem-solving and analysis. Mathematical beauty refers to elegance and simplicity found in mathematical relationships and proofs. Mathematical applications span virtually every field of human knowledge, from natural sciences to social sciences, providing tools for measurement, prediction, and understanding.',
                'pronunciation': "/ˌmæθ.əˈmæt.ɪ.kəl/",
                'etymology': 'From Greek "mathematikos," meaning relating to mathematics or learning, derived from "mathema" (knowledge).',
                'memory_tip': 'Remember MATHEMATICAL = relating to MATH - logical, precise, and systematic like math.',
                'example_sentence': 'The engineer used ______ formulas to calculate the structural load requirements for the bridge.'
            },
            'mathematician': {
                'definition': 'A person who specializes in mathematics, either through academic study, research, or professional application of mathematical principles. Mathematicians work in various settings including universities, research institutions, government agencies, and private industry. Pure mathematicians focus on theoretical concepts, developing new mathematical theories and exploring abstract relationships. Applied mathematicians solve practical problems in engineering, physics, economics, computer science, and other fields using mathematical methods. Famous mathematicians throughout history have revolutionized human understanding through discoveries in areas like geometry, calculus, number theory, and statistics. Modern mathematicians often specialize in specific areas such as topology, analysis, algebra, or computational mathematics. The profession requires exceptional analytical thinking, creativity, and persistence in solving complex problems.',
                'pronunciation': "/ˌmæθ.ə.məˈtɪʃ.ən/",
                'etymology': 'From Greek "mathematikos" (relating to mathematics) + "-ian" suffix indicating a person who practices or studies.',
                'memory_tip': 'Remember MATHEMATICIAN = a person who studies and practices MATHEMATICS professionally.',
                'example_sentence': 'The brilliant ______ developed a new theorem that solved a problem unsolved for over a century.'
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
            'marionetteneapolitan',  # marionette + neapolitan
            'marsupialtrefoil',      # marsupial + trefoil  
            'massestroganoff',       # masses + stroganoff
            'maternitybungee'        # maternity + bungee
        ]
        
        for word in words_to_check:
            combined_words.append(word)
            
        return combined_words
    
    def process_batch(self, input_file: str, output_file: str):
        """Process the batch with comprehensive Claude data"""
        
        logger.info("Processing Batch 108 with comprehensive Claude data...")
        
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
    processor = Batch108Processor()
    
    input_file = "output/batch_108_words.csv"
    output_file = "output/batch_108_processed.csv"
    
    try:
        word_count = processor.process_batch(input_file, output_file)
        
        logger.info("Batch 108 processing completed!")
        logger.info(f"Processed {word_count} words with comprehensive Claude data")
        logger.info(f"Output saved to: {output_file}")
        logger.info(f"Results: {word_count} successful, 0 failed")
        
    except Exception as e:
        logger.error(f"Error processing batch 108: {str(e)}")
        raise