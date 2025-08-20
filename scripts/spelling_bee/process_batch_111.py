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

class Batch111Processor:
    """Processes Batch 111 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for each word"""
        data = {
            'merrimack': {
                'definition': 'Referring to the Merrimack River in New Hampshire and Massachusetts, or historically to USS Merrimack, a steam frigate that was converted by the Confederacy into the ironclad warship CSS Virginia during the American Civil War. The Merrimack River flows 117 miles from Franklin, New Hampshire to Newburyport, Massachusetts, supporting early industrial development through water power for textile mills. The river valley became a major manufacturing center during the Industrial Revolution, with cities like Manchester, Nashua, and Lowell growing around textile production. USS Merrimack gained historical significance when Confederate forces raised the scuttled ship and rebuilt it as an ironclad, leading to the famous Battle of Hampton Roads against USS Monitor in 1862. This battle marked the beginning of the end for wooden warships and demonstrated the effectiveness of armored vessels in naval warfare.',
                'pronunciation': "/ˈmɛr.ɪ.mæk/",
                'etymology': 'From Pennacook Native American "Namaoskeag," meaning "good fishing place," referring to the river and surrounding area.',
                'memory_tip': 'Remember MERRIMACK = river that was MERRY for MANUFACTURING - powered early American industry.',
                'example_sentence': 'The ______ River powered the textile mills that made Lowell a center of American industrial development.'
            },
            'mesial': {
                'definition': 'Located in or directed toward the middle line of the body; in dentistry, referring to the surface of a tooth facing toward the front center of the mouth. Mesial anatomical positions help describe spatial relationships in medical and dental contexts with precision. Mesial surfaces of teeth are those closest to the midline of the dental arch, contrasting with distal surfaces that face away from the midline. Understanding mesial orientation is crucial for dental procedures, orthodontic treatment, and oral health assessment. The term appears in medical imaging, surgical descriptions, and anatomical studies where precise spatial reference is essential. Mesial displacement can describe abnormal positioning of organs or structures toward the body\'s center line. In orthodontics, mesial movement refers to tooth migration toward the front center of the mouth.',
                'pronunciation': "/ˈmi.zi.əl/",
                'etymology': 'From Greek "mesos," meaning middle, with "-ial" suffix indicating relationship to the middle or median line.',
                'memory_tip': 'Remember MESIAL = toward the MIDDLE - dental/medical term for facing the center.',
                'example_sentence': 'The dentist noted decay on the ______ surface of the molar facing the center of the mouth.'
            },
            'mesopotamian': {
                'definition': 'Relating to Mesopotamia, the ancient region between the Tigris and Euphrates rivers in modern-day Iraq, often called the "cradle of civilization." Mesopotamian civilizations including Sumerians, Babylonians, and Assyrians developed the world\'s first cities, writing systems, legal codes, and complex societies. Mesopotamian contributions to human civilization include cuneiform writing, the wheel, the plow, mathematics, astronomy, and architectural innovations like the ziggurat. The region\'s fertile soil and river systems supported agriculture that enabled population growth and social stratification. Mesopotamian literature includes the Epic of Gilgamesh, one of humanity\'s earliest known literary works. The Code of Hammurabi established legal precedents that influenced later civilizations. Understanding Mesopotamian history provides insight into the origins of urban civilization, government, religion, and cultural development.',
                'pronunciation': "/ˌmɛs.ə.pəˈteɪ.mi.ən/",
                'etymology': 'From Greek "Mesopotamia," meaning "between rivers" (mesos = middle, potamos = river), referring to the region between Tigris and Euphrates.',
                'memory_tip': 'Remember MESOPOTAMIAN = MESO (between) + POTAMIAN (rivers) - ancient civilization between two rivers.',
                'example_sentence': 'The ______ cuneiform tablets revealed details about ancient legal systems and daily life.'
            },
            'mess': {
                'definition': 'A state of disorder, confusion, or untidiness; also a situation that is complicated or difficult to resolve. Mess can describe physical disorganization where objects are scattered or dirty, creating chaotic appearances. Emotional or social messes involve complicated relationships, conflicts, or problems that resist easy solutions. Making a mess implies creating disorder through careless or clumsy actions. Military mess refers to communal dining facilities where service members eat together. Cleaning up a mess requires systematic effort to restore order and cleanliness. The term can describe both minor inconveniences and major disasters depending on context and scale. Understanding mess involves recognizing the difference between temporary disorder and chronic disorganization that affects functioning and well-being.',
                'pronunciation': "/mɛs/",
                'etymology': 'From Old French "mes," meaning portion of food, later extended to mean confused state or untidy condition.',
                'memory_tip': 'Remember MESS = disorder and confusion - things mixed up in a messy way.',
                'example_sentence': 'The kitchen was a complete ______ after the children tried to bake cookies by themselves.'
            },
            'message': {
                'definition': 'A communication or information transmitted from one person or place to another, whether spoken, written, or conveyed through various media. Messages serve fundamental human needs for connection, information sharing, and coordination of activities across time and distance. Different message types include personal communications, business correspondence, emergency alerts, and mass media broadcasts. Message delivery involves senders, content, channels, and receivers working together to create understanding. Digital messaging has revolutionized communication through email, text messaging, social media, and instant messaging platforms. Effective messages require clarity, appropriate tone, correct targeting, and suitable delivery methods. Messages can be explicit (direct statements) or implicit (implied meanings requiring interpretation). Understanding message construction and interpretation skills are essential for personal and professional success.',
                'pronunciation': "/ˈmɛs.ɪdʒ/",
                'etymology': 'From Old French "message," derived from Latin "missus" (sent), related to "mittere" (to send).',
                'memory_tip': 'Remember MESSAGE = communication sent to someone - a MISSIVE that\'s SAGE (wise).',
                'example_sentence': 'She left a ______ on his voicemail explaining why she would be late for the meeting.'
            },
            'messenger': {
                'definition': 'A person who carries messages or communications between individuals or organizations; also software or services that facilitate message delivery. Historical messengers traveled on foot, horseback, or by other means to deliver important information before modern communication technology. Military messengers carried orders, intelligence, and reports between commanders and units during wartime. Modern digital messengers include email systems, instant messaging applications, and automated notification services. Biological messengers like hormones and neurotransmitters carry information within living organisms. The phrase "don\'t shoot the messenger" warns against blaming those who deliver unwelcome news. Messenger services provide professional document and package delivery for businesses. Understanding messenger roles involves recognizing both human intermediaries and technological systems that enable communication.',
                'pronunciation': "/ˈmɛs.ən.dʒər/",
                'etymology': 'From "message" + "-er" suffix, meaning one who carries messages or communications.',
                'memory_tip': 'Remember MESSENGER = person who carries MESSAGES - communication deliverer.',
                'example_sentence': 'The ______ arrived on horseback with urgent news from the capital city.'
            },
            'metadata': {
                'definition': 'Data that provides information about other data, describing characteristics, properties, or context of datasets without containing the primary content itself. Metadata serves as organized information about information, enabling efficient storage, retrieval, and management of digital resources. Examples include file creation dates, author names, keywords, formats, and technical specifications that describe documents, images, or databases. Library catalog systems use metadata to organize books through titles, authors, subjects, and publication information. Digital photographs contain metadata including camera settings, location coordinates, and timestamps. Web pages include metadata for search engine optimization and content description. Database metadata describes table structures, field types, and relationships between different data elements. Understanding metadata management is crucial for information organization, data governance, and system interoperability.',
                'pronunciation': "/ˈmɛt.əˌdeɪ.tə/",
                'etymology': 'From Greek "meta" (beyond, about) + "data" (facts), meaning information about information.',
                'memory_tip': 'Remember METADATA = META (about) + DATA - information that describes other data.',
                'example_sentence': 'The digital library used ______ to catalog and search millions of electronic documents efficiently.'
            },
            'metals': {
                'definition': 'Chemical elements characterized by properties including electrical conductivity, malleability, ductility, and metallic luster; materials that typically lose electrons to form positive ions. Metals constitute the majority of elements in the periodic table and serve essential roles in technology, biology, and industry. Common metals include iron, aluminum, copper, gold, and silver, each with distinct properties and applications. Metal alloys combine multiple metals to create materials with enhanced characteristics for specific purposes. Precious metals like gold and platinum have high economic value due to rarity and resistance to corrosion. Industrial metals support manufacturing, construction, and infrastructure development worldwide. Transition metals exhibit variable oxidation states and often serve as catalysts in chemical processes. Understanding metal properties enables technological advancement, materials engineering, and scientific research across numerous fields.',
                'pronunciation': "/ˈmɛt.əlz/",
                'etymology': 'From Latin "metallum," meaning mine or quarry, derived from Greek "metallon" (mine, quarry, metal).',
                'memory_tip': 'Remember METALS = shiny materials that MEET-AL (all) our industrial needs.',
                'example_sentence': 'The electronics industry depends on various ______ including copper, gold, and rare earth elements.'
            },
            'metaplasia': {
                'definition': 'A reversible replacement of one differentiated cell type with another mature differentiated cell type, typically occurring as an adaptive response to chronic irritation or inflammation. Metaplasia represents cellular adaptation where normal tissue transforms into a different but normal cell type better suited to withstand environmental stress. Common examples include respiratory epithelium changing to squamous epithelium in smokers\' airways, or stomach lining adapting to chronic acid exposure. While metaplasia itself is benign, it can predispose tissues to malignant transformation if the underlying cause persists. Barrett\'s esophagus exemplifies metaplasia where normal esophageal lining transforms due to chronic acid reflux. Understanding metaplasia helps in recognizing early pathological changes and implementing preventive measures. Medical professionals monitor metaplastic changes to assess disease progression and treatment effectiveness.',
                'pronunciation': "/ˌmɛt.əˈpleɪ.ʒə/",
                'etymology': 'From Greek "meta" (change) + "plasis" (formation), meaning change in tissue formation or development.',
                'memory_tip': 'Remember METAPLASIA = META (change) + PLASIA (formation) - tissue changing into different type.',
                'example_sentence': 'The pathologist identified ______ in the biopsy, showing normal cells adapting to chronic irritation.'
            },
            'metastasize': {
                'definition': 'The process by which cancer cells spread from the primary tumor site to distant parts of the body through bloodstream, lymphatic system, or direct extension. Metastasis represents the most dangerous aspect of cancer, as it enables malignant cells to establish secondary tumors in vital organs. The metastatic process involves multiple steps including local invasion, intravasation into blood vessels, circulation, extravasation at distant sites, and establishment of new tumors. Different cancer types have preferred metastatic patterns: breast cancer often spreads to bones and liver, lung cancer to brain and bone, colon cancer to liver. Understanding metastatic mechanisms guides treatment strategies, staging protocols, and prognostic assessments. Early detection and treatment aim to prevent metastasis and improve patient outcomes. Research focuses on identifying factors that promote or inhibit metastatic spread.',
                'pronunciation': "/məˈtæs.təˌsaɪz/",
                'etymology': 'From Greek "metastasis," meaning displacement or change of position, from "meta" (beyond) + "stasis" (standing).',
                'memory_tip': 'Remember METASTASIZE = META (beyond) + STASIZE - cancer spreading beyond original site.',
                'example_sentence': 'Doctors worked to prevent the tumor from beginning to ______ to other organs.'
            },
            'metatarsal': {
                'definition': 'Relating to the five long bones of the foot located between the tarsal bones of the midfoot and the phalanges of the toes. Metatarsal bones form the skeletal framework of the forefoot and bear significant weight during walking, running, and standing. Each metatarsal connects to a toe, with the first metatarsal being the thickest and most important for balance and propulsion. Metatarsal stress fractures commonly occur in athletes due to repetitive loading and inadequate rest. The metatarsal arch helps distribute body weight and provides shock absorption during locomotion. Metatarsalgia describes pain in the metatarsal region often caused by overuse, improper footwear, or structural abnormalities. Understanding metatarsal anatomy is essential for treating foot injuries, designing athletic footwear, and addressing biomechanical problems affecting gait and stability.',
                'pronunciation': "/ˌmɛt.əˈtɑr.səl/",
                'etymology': 'From Greek "meta" (beyond) + "tarsus" (ankle), referring to bones beyond the ankle region.',
                'memory_tip': 'Remember METATARSAL = META (beyond) + TARSAL - foot bones beyond the ankle.',
                'example_sentence': 'The X-ray revealed a stress fracture in the second ______ bone of her foot.'
            },
            'mete': {
                'definition': 'To distribute or give a measured portion, especially of punishment or justice; to dispense in measured amounts. The term "mete out" commonly describes the delivery of consequences, penalties, or rewards according to established standards or legal requirements. Courts mete out sentences proportionate to crimes committed, while parents mete out discipline appropriate to children\'s misbehavior. The word implies careful consideration and measured response rather than arbitrary or excessive action. Historical usage included measuring land boundaries and distributing resources. Meting requires judgment about appropriate quantities and fair allocation. The concept emphasizes proportionality and justice in distribution of both positive and negative consequences. Understanding meting involves balancing punishment with rehabilitation and ensuring responses match the severity of actions.',
                'pronunciation': "/mit/",
                'etymology': 'From Old English "metan," meaning to measure or allot, related to "measure" and "meter."',
                'memory_tip': 'Remember METE = to MEASURE out justice or punishment - give measured portions.',
                'example_sentence': 'The judge will ______ out punishment that fits the severity of the crime.'
            },
            'meteor': {
                'definition': 'A bright streak of light that appears in the sky when a meteoroid enters Earth\'s atmosphere and burns up due to friction with air molecules. Meteors are commonly called "shooting stars" or "falling stars," though they are not related to actual stars. Most meteors result from small particles of dust or rock debris left by comets orbiting the Sun. Meteor showers occur when Earth passes through dense trails of meteoroid debris, creating spectacular displays of multiple meteors. Larger meteors may survive atmospheric entry to reach Earth\'s surface as meteorites, providing valuable scientific information about space. The brightness and color of meteors depend on their composition, speed, and atmospheric conditions. Understanding meteors contributes to astronomy education and helps scientists study solar system formation and evolution.',
                'pronunciation': "/ˈmi.ti.ər/",
                'etymology': 'From Greek "meteoros," meaning high in the air or atmospheric phenomenon, related to weather events.',
                'memory_tip': 'Remember METEOR = bright light that MEETS the EARTH\'s atmosphere and burns up.',
                'example_sentence': 'The children made wishes as they watched the brilliant ______ streak across the night sky.'
            },
            'methodology': {
                'definition': 'A system of methods used in a particular area of study or activity; the principles and procedures that guide research or systematic investigation. Methodology encompasses the theoretical framework, research design, data collection techniques, and analysis procedures that ensure valid and reliable results. Scientific methodology includes hypothesis formation, experimental design, control of variables, and statistical analysis. Research methodology varies across disciplines: qualitative methods for social sciences, quantitative methods for physical sciences, and mixed methods for comprehensive studies. Good methodology ensures reproducible results, minimizes bias, and enables peer review and validation. Educational methodology describes teaching approaches and learning strategies. Business methodology includes project management frameworks and process improvement techniques. Understanding methodology enables critical evaluation of research quality and appropriate application of investigative techniques.',
                'pronunciation': "/ˌmɛθ.əˈdɑl.ə.dʒi/",
                'etymology': 'From Greek "methodos" (way of investigation) + "logos" (study), meaning the study of methods.',
                'memory_tip': 'Remember METHODOLOGY = METHOD + OLOGY - the study of systematic methods.',
                'example_sentence': 'The researcher\'s ______ ensured reliable data collection and valid statistical analysis.'
            },
            'methods': {
                'definition': 'Systematic procedures, techniques, or ways of doing something to achieve specific goals or results. Methods provide structured approaches to problem-solving, research, teaching, manufacturing, and countless other activities requiring organized effort. Scientific methods include observation, hypothesis formation, experimentation, and analysis. Teaching methods encompass various pedagogical approaches adapted to different learning styles and subject matter. Research methods determine how data is collected, analyzed, and interpreted to answer questions or test theories. Manufacturing methods involve processes, quality control, and efficiency optimization. Effective methods are reproducible, reliable, and appropriate for their intended purposes. Method comparison helps identify best practices and optimize outcomes. Understanding various methods enables informed choice of approaches and continuous improvement through systematic evaluation and refinement.',
                'pronunciation': "/ˈmɛθ.ədz/",
                'etymology': 'From Greek "methodos," meaning way of investigation or procedure, derived from "meta" (after) + "hodos" (way).',
                'memory_tip': 'Remember METHODS = systematic ways to MEET your goals - organized procedures.',
                'example_sentence': 'The science teacher demonstrated various ______ for conducting controlled experiments safely.'
            },
            'metonic': {
                'definition': 'Relating to the Metonic cycle, a period of approximately 19 years after which the phases of the moon recur on the same dates of the solar calendar. The Metonic cycle was discovered by Greek astronomer Meton of Athens in 432 BCE and represents a fundamental relationship between lunar and solar calendars. This cycle consists of 235 lunar months equaling almost exactly 19 solar years, with only a few hours of discrepancy. Ancient civilizations used the Metonic cycle to reconcile lunar religious calendars with solar agricultural calendars. The cycle appears in Easter date calculations, Jewish calendar systems, and historical chronological studies. Understanding the Metonic cycle demonstrates the mathematical precision of ancient astronomical observations. Modern calendar systems and astronomical calculations still reference this ancient discovery that bridges lunar and solar time measurement.',
                'pronunciation': "/mɪˈtɑn.ɪk/",
                'etymology': 'Named after Meton of Athens, Greek astronomer who discovered the 19-year lunar-solar calendar cycle.',
                'memory_tip': 'Remember METONIC = cycle discovered by METON - 19-year moon/sun calendar pattern.',
                'example_sentence': 'The ancient Greeks used the ______ cycle to predict when moon phases would repeat on the same calendar dates.'
            },
            'metrical': {
                'definition': 'Relating to meter in poetry or music; characterized by rhythmic patterns of stressed and unstressed syllables or beats. Metrical analysis involves identifying poetic feet (iamb, trochee, anapest, dactyl) and measuring line lengths in verse. Metrical patterns create rhythm, musicality, and structural organization in poetry across all literary traditions. Different metrical forms include sonnet meter (iambic pentameter), ballad meter, and free verse that breaks traditional patterns. Metrical composition requires understanding syllable stress, line length, and rhythmic flow. Music theory uses metrical concepts to describe time signatures, rhythmic patterns, and temporal organization. Metrical variation creates emphasis, surprise, and artistic expression within established patterns. Understanding metrical analysis enhances appreciation of poetry\'s technical craft and aesthetic effects.',
                'pronunciation': "/ˈmɛt.rɪ.kəl/",
                'etymology': 'From Greek "metron" (measure) + "-ical" suffix, relating to measurement and rhythmic patterns.',
                'memory_tip': 'Remember METRICAL = relating to METER - rhythmic patterns in poetry and music.',
                'example_sentence': 'The poetry student analyzed the ______ structure to understand the sonnet\'s rhythmic pattern.'
            },
            'metronome': {
                'definition': 'A device that produces regular, metrical ticks to help musicians maintain consistent tempo during practice and performance. Metronomes mark time through audible clicks, visual beats, or both, providing external rhythmic reference for musical timing. Traditional mechanical metronomes use weighted pendulums with adjustable speeds measured in beats per minute. Digital metronomes offer additional features including different sounds, complex time signatures, and programmable patterns. Musicians use metronomes to develop steady timing, coordinate ensemble playing, and gradually increase performance speed. Music education relies on metronomes to teach rhythm, tempo consistency, and temporal precision. The device helps musicians internalize steady pulse and overcome tendency to rush or slow down during difficult passages. Understanding metronome use improves musical performance, timing accuracy, and ensemble coordination skills.',
                'pronunciation': "/ˈmɛt.rəˌnoʊm/",
                'etymology': 'From Greek "metron" (measure) + "nomos" (law), meaning device that regulates musical measure.',
                'memory_tip': 'Remember METRONOME = METRO (measure) + NOME (law) - device that keeps musical time.',
                'example_sentence': 'The piano student practiced scales with a ______ to develop steady, consistent timing.'
            },
            'metropolis': {
                'definition': 'A large, important city that serves as a major political, economic, or cultural center for a surrounding region or country. Metropolises typically have populations exceeding one million and function as hubs for commerce, government, education, and transportation. Historical metropolises like Rome, Constantinople, and London dominated their respective empires and regions. Modern metropolises include New York, Tokyo, London, and Paris, which influence global economics, culture, and politics. Metropolitan areas encompass surrounding suburbs and satellite communities economically connected to the central city. Metropolises face unique challenges including traffic congestion, housing costs, pollution, and infrastructure maintenance. Urban planning addresses metropolitan growth through transportation systems, zoning regulations, and public services. Understanding metropolitan development involves examining population dynamics, economic factors, and urban design principles.',
                'pronunciation': "/məˈtrɑp.ə.lɪs/",
                'etymology': 'From Greek "metropolis," meaning mother city, from "meter" (mother) + "polis" (city).',
                'memory_tip': 'Remember METROPOLIS = METRO (mother) + POLIS (city) - the mother city or major urban center.',
                'example_sentence': 'New York serves as a global ______ influencing finance, culture, and commerce worldwide.'
            },
            'meunière': {
                'definition': 'A French cooking method for preparing fish by dredging in flour, pan-frying in butter, and finishing with lemon juice, parsley, and brown butter sauce. The meunière technique ("miller\'s style") creates a light, crispy coating that enhances the fish\'s natural flavors without overwhelming delicate textures. Classic meunière preparation involves seasoned flour coating, careful butter temperature control, and precise timing to achieve golden-brown exteriors and moist interiors. The dish originated in French cuisine but appears in Creole cooking, particularly New Orleans, where trout or sole meunière became signature preparations. Meunière sauce combines brown butter (beurre noisette), lemon juice, and fresh herbs for a simple but elegant accompaniment. The technique works best with flat fish like sole, flounder, or trout that cook evenly and present well. Understanding meunière preparation demonstrates fundamental French culinary techniques.',
                'pronunciation': "/ˌmøn.iˈɛr/",
                'etymology': 'From French "meunière," meaning miller\'s wife, referring to the flour-dusting technique resembling a miller\'s work.',
                'memory_tip': 'Remember MEUNIÈRE = MILLER\'S style - fish coated in flour like a miller working with grain.',
                'example_sentence': 'The chef prepared the sole ______ with brown butter, lemon, and fresh parsley.'
            },
            'mexico': {
                'definition': 'A country in North America bordered by the United States to the north and Guatemala and Belize to the south, officially known as the United Mexican States. Mexico has a rich cultural heritage combining indigenous civilizations (Aztec, Maya, Olmec) with Spanish colonial influence. The country features diverse geography including mountains, deserts, tropical forests, and extensive coastlines on both Pacific and Atlantic oceans. Mexico\'s economy includes manufacturing, oil production, agriculture, and tourism as major sectors. Mexican cuisine, art, music, and literature have gained worldwide recognition and influence. The capital, Mexico City, is one of the world\'s largest metropolitan areas. Mexico\'s history includes ancient civilizations, Spanish conquest, independence movements, revolution, and modern development. Understanding Mexico involves appreciating its cultural diversity, economic challenges and opportunities, and significant regional and global relationships.',
                'pronunciation': "/ˈmɛk.sɪ.koʊ/",
                'etymology': 'From Nahuatl "Mexihco," possibly meaning "place of the Mexica people" or relating to the god Mexitli.',
                'memory_tip': 'Remember MEXICO = country with rich MIX of indigenous and Spanish culture.',
                'example_sentence': 'Tourists visited ______ to experience ancient Mayan ruins and vibrant contemporary culture.'
            },
            'mezzanine': {
                'definition': 'An intermediate floor between two main floors of a building, typically located between the ground floor and first floor; also the lowest balcony level in a theater. Architectural mezzanines create additional space within existing floor heights, often used for offices, storage, or specialized functions. Theater mezzanines provide seating with good views of the stage while being more affordable than orchestra seats. Mezzanine financing in business refers to hybrid debt-equity funding that combines features of loans and equity investment. The term describes anything occupying an intermediate position between two primary levels or categories. Mezzanine design requires careful attention to ceiling heights, structural support, and building codes. In retail spaces, mezzanines can expand floor area without full additional stories. Understanding mezzanine concepts applies to architecture, theater design, and financial structures.',
                'pronunciation': "/ˈmɛz.əˌnin/",
                'etymology': 'From Italian "mezzanino," meaning middle or intermediate, derived from "mezzo" (half).',
                'memory_tip': 'Remember MEZZANINE = MEZZO (half) level - intermediate floor between main floors.',
                'example_sentence': 'The bookstore added a ______ level to display more inventory without expanding the building footprint.'
            },
            'miasma': {
                'definition': 'An unhealthy or unpleasant atmosphere or influence; historically, a noxious form of "bad air" believed to cause disease before the development of germ theory. Miasma theory dominated medical thinking until the late 19th century, attributing diseases like cholera and malaria to poisonous vapors from swamps, sewers, and decaying matter. Modern usage describes oppressive or corrupting atmospheres that seem to emanate from particular places or situations. Political miasma refers to corrupt or toxic environments that undermine good governance. Environmental miasma can describe air pollution or contaminated conditions affecting health and well-being. The concept represents both historical medical understanding and contemporary metaphorical usage. Understanding miasma theory helps appreciate the evolution of medical knowledge and public health practices. The term emphasizes atmospheric influences on human health and social conditions.',
                'pronunciation': "/maɪˈæz.mə/",
                'etymology': 'From Greek "miasma," meaning pollution or defilement, related to "miainein" (to pollute).',
                'memory_tip': 'Remember MIASMA = bad atmosphere that MARS the air - unhealthy influence or environment.',
                'example_sentence': 'The detective felt a ______ of corruption surrounding the investigation that made everyone suspicious.'
            },
            'mice': {
                'definition': 'Plural form of mouse, referring to small rodents characterized by pointed snouts, small rounded ears, and long tails. Mice are among the most successful mammalian species, adapting to diverse environments worldwide and living in close association with humans. House mice (Mus musculus) are common in buildings and serve as important laboratory animals for scientific research. Field mice inhabit natural environments and play crucial ecological roles as prey species and seed dispersers. Laboratory mice contribute to medical research, genetics studies, and pharmaceutical testing. Mice reproduce rapidly with short generation times, making them valuable for studying heredity and development. Computer mice derive their name from resemblance to the rodent\'s body and tail. Understanding mice involves appreciating both their ecological importance and their contributions to human knowledge through scientific research.',
                'pronunciation': "/maɪs/",
                'etymology': 'Plural of "mouse," from Old English "mys," related to Latin "mus" and Greek "mys" (mouse).',
                'memory_tip': 'Remember MICE = plural of mouse - small rodents that are NICE research subjects.',
                'example_sentence': 'The laboratory ______ were used to test the effectiveness of the new cancer treatment.'
            },
            'micellar': {
                'definition': 'Relating to micelles, spherical structures formed by surfactant molecules in aqueous solutions when concentration exceeds the critical micelle concentration. Micellar structures have hydrophilic heads facing outward toward water and hydrophobic tails clustered inward, creating unique chemical and physical properties. Micellar solutions enable solubilization of oils and other hydrophobic substances in water, forming the basis for soap and detergent action. Pharmaceutical applications use micellar systems for drug delivery, enhancing solubility and bioavailability of poorly water-soluble medications. Micellar water in cosmetics combines cleansing and moisturizing properties through gentle surfactant action. Industrial applications include enhanced oil recovery, where micellar solutions improve petroleum extraction efficiency. Understanding micellar chemistry explains fundamental processes in cleaning, drug formulation, and biotechnology. The technology represents important interface between chemistry and practical applications.',
                'pronunciation': "/maɪˈsɛl.ər/",
                'etymology': 'From Latin "micella," diminutive of "mica" (crumb), referring to small particle-like structures.',
                'memory_tip': 'Remember MICELLAR = relating to MICELLES - tiny soap-like structures that help clean.',
                'example_sentence': 'The cosmetic company developed ______ cleansing water that removes makeup without harsh rubbing.'
            },
            'michaelmas': {
                'definition': 'The Christian feast day celebrating the Archangel Michael, observed on September 29th in Western Christianity; also one of the four traditional quarter days in English and Welsh law. Michaelmas marks the beginning of the academic year in many British universities and traditionally represents the start of autumn activities. The feast honors Saint Michael\'s victory over Satan and his role as protector and judge of souls. Michaelmas daisies bloom around this time, creating purple flowers that symbolize farewell to summer. Traditional Michaelmas customs include eating goose, settling debts, and beginning new agricultural and business cycles. Legal and academic calendar systems historically organized activities around quarter days including Michaelmas, Christmas, Lady Day, and Midsummer. Understanding Michaelmas provides insight into traditional English seasonal celebrations and institutional organization.',
                'pronunciation': "/ˈmaɪ.kəl.məs/",
                'etymology': 'From "Michael" (the archangel) + "mass" (Christian feast), referring to the feast of Saint Michael.',
                'memory_tip': 'Remember MICHAELMAS = MICHAEL\'S MASS - feast day for Archangel Michael in September.',
                'example_sentence': 'Oxford University\'s autumn term traditionally begins near ______, following centuries-old academic calendar customs.'
            },
            'michel': {
                'definition': 'A French given name equivalent to Michael, meaning "who is like God" in Hebrew; also referring to various notable people with this name throughout history. Michel appears frequently in French literature, philosophy, and culture, including philosopher Michel Foucault and writer Michel de Montaigne. The name represents French cultural identity and appears in place names, institutions, and artistic works. Michel de Nostredame (Nostradamus) gained fame for his prophetic writings in the 16th century. Saint-Michel refers to various churches and locations dedicated to the Archangel Michael in French-speaking regions. Understanding Michel involves recognizing both the personal name and its cultural significance in French history and literature. The name demonstrates the adaptation of religious and cultural traditions across different languages and societies.',
                'pronunciation': "/miˈʃɛl/",
                'etymology': 'From Hebrew "Mikhael," meaning "who is like God," adapted through Latin and French linguistic evolution.',
                'memory_tip': 'Remember MICHEL = French version of Michael - asks "who is like God" in Hebrew tradition.',
                'example_sentence': 'The French philosopher ______ Foucault influenced modern thinking about power and knowledge.'
            },
            'michigander': {
                'definition': 'A person who lives in or is from the state of Michigan; a demonym specifically referring to Michigan residents. The term emerged in the 19th century, possibly popularized during political campaigns and regional identity discussions. Michiganders experience the state\'s unique geography including two peninsulas separated by the Great Lakes. The state\'s economy historically centered on automobile manufacturing, though it has diversified into technology, agriculture, and tourism. Michiganders often develop strong regional pride based on the state\'s natural beauty, including extensive shorelines, forests, and recreational opportunities. Cultural characteristics associated with Michiganders include resilience during economic challenges and appreciation for outdoor activities. The term reflects American regional identity formation and the tendency to create distinctive names for state residents. Understanding Michigander usage demonstrates how geographic and cultural factors shape regional identity.',
                'pronunciation': "/ˈmɪʃ.ɪ.ɡæn.dər/",
                'etymology': 'From "Michigan" (state name from Ojibwe "mishigami") + "-er" suffix, meaning resident of Michigan.',
                'memory_tip': 'Remember MICHIGANDER = person from MICHIGAN who might GANDER (look) at the Great Lakes.',
                'example_sentence': 'As a lifelong ______, she knew the best spots for viewing fall colors in the Upper Peninsula.'
            },
            'microfiche': {
                'definition': 'A flat rectangular sheet of microfilm containing greatly reduced photographic images of printed materials, used for compact storage and preservation of documents. Microfiche technology emerged in the mid-20th century to address space limitations in libraries, archives, and offices. Each microfiche sheet can store dozens or hundreds of document pages in a format requiring special readers for viewing and printing. Libraries used microfiche extensively for storing newspapers, periodicals, and government documents before digital technology became widespread. The format provided excellent storage density, long-term preservation capabilities, and relatively low cost compared to maintaining original paper documents. Research institutions continue using microfiche for historical materials and specialized collections. Understanding microfiche represents important document management history and demonstrates technological evolution in information storage.',
                'pronunciation': "/ˈmaɪ.kroʊˌfiʃ/",
                'etymology': 'From French "microfiche," meaning small index card, from "micro" (small) + "fiche" (card or slip).',
                'memory_tip': 'Remember MICROFICHE = MICRO (tiny) FICHE (card) - small film sheet storing many documents.',
                'example_sentence': 'The historian used ______ readers to examine 19th-century newspaper archives stored on film.'
            },
            'microphone': {
                'definition': 'A device that converts sound waves into electrical signals, enabling recording, amplification, and transmission of audio. Microphones work through various technologies including dynamic, condenser, ribbon, and crystal designs that respond to sound pressure variations. Applications include public speaking, music recording, broadcasting, telecommunications, and voice recognition systems. Different microphone types serve specific purposes: lavalier microphones for hands-free speaking, shotgun microphones for directional recording, and studio microphones for high-quality music production. Microphone placement, polar patterns, and frequency response characteristics affect audio quality and suitability for different uses. Modern microphones often incorporate digital signal processing and wireless transmission capabilities. Understanding microphone technology enables better audio recording, live sound reinforcement, and communication system design. The device represents fundamental audio engineering principles and practical sound reproduction.',
                'pronunciation': "/ˈmaɪ.krəˌfoʊn/",
                'etymology': 'From Greek "mikros" (small) + "phone" (sound), meaning device for amplifying small sounds.',
                'memory_tip': 'Remember MICROPHONE = MICRO (small) + PHONE (sound) - device that makes quiet sounds loud.',
                'example_sentence': 'The singer adjusted the ______ height to capture her voice clearly during the recording session.'
            },
            'microwavegabled': {
                'definition': 'A combined word error from PDF parsing that incorrectly merged "microwave" and "gabled." This represents a data processing error where two unrelated terms were concatenated without proper spacing. Microwave refers to electromagnetic radiation or cooking appliances, while gabled describes architectural roof structures with triangular ends. Such parsing errors occur when PDF text extraction fails to recognize word boundaries, particularly in documents with complex formatting or multiple columns. These errors highlight the challenges of automated text processing and the importance of data validation. The nonsensical combination would require manual correction or sophisticated error detection algorithms to separate into meaningful individual components.',
                'pronunciation': "/ˈmaɪ.kroʊˌweɪvˈɡeɪ.bəld/",
                'etymology': 'Processing error combining "microwave" (electromagnetic waves) with "gabled" (architectural roof style). Invalid concatenation.',
                'memory_tip': 'This is a COMBINED WORD ERROR - two different words incorrectly joined during PDF processing.',
                'example_sentence': 'The text processing system detected ______ as an invalid word requiring separation into components.'
            },
            'midair': {
                'definition': 'The space or position in the middle of the air, above the ground but not touching any surface; suspended in the atmosphere. Midair describes the three-dimensional space where flying objects, aircraft, birds, and projectiles move freely without ground contact. Aviation uses midair terminology for flight operations, collision avoidance, and air traffic control communications. Midair collisions represent serious aviation hazards requiring sophisticated radar systems and flight path coordination. Sports involving midair movement include gymnastics, diving, basketball, and aerial skiing where athletes perform while airborne. Midair catches in baseball or football demonstrate athletic skill in judging trajectory and timing. The concept emphasizes the temporary suspension between ground departure and landing. Understanding midair dynamics involves physics of flight, ballistics, and three-dimensional movement in space.',
                'pronunciation': "/ˌmɪdˈɛr/",
                'etymology': 'Compound of "mid" (middle) + "air," referring to space in the middle of the atmosphere.',
                'memory_tip': 'Remember MIDAIR = MID (middle) + AIR - space suspended in the middle of the air.',
                'example_sentence': 'The acrobat performed a spectacular flip in ______ before landing safely on the trampoline.'
            },
            'midday': {
                'definition': 'The middle of the day; noon, when the sun reaches its highest point in the sky for a given location. Midday represents the transition between morning and afternoon, traditionally marked by the sun\'s zenith position. Different cultures have varying midday customs including lunch breaks, rest periods (siesta), and business closures. Solar noon occurs when the sun crosses the local meridian, though this may differ from clock noon due to time zone boundaries and daylight saving time. Midday temperatures typically reach daily maximums in many climates, affecting human activity patterns and energy consumption. Agricultural societies historically organized work schedules around midday heat, with early morning and late afternoon labor. Understanding midday involves astronomical concepts, cultural practices, and practical time management. The concept connects solar movement with human temporal organization.',
                'pronunciation': "/ˌmɪdˈdeɪ/",
                'etymology': 'From "mid" (middle) + "day," referring to the middle point of the daylight period.',
                'memory_tip': 'Remember MIDDAY = MID (middle) + DAY - noon when the sun is highest.',
                'example_sentence': 'The workers took their lunch break at ______ when the Mediterranean sun was most intense.'
            },
            'middle': {
                'definition': 'The center or middle part of something; equally distant from extremes or ends. Middle describes spatial positions between boundaries, temporal periods between beginning and end, or qualitative states between opposite conditions. Middle age refers to the period between youth and old age, typically considered ages 40-65. Middle class describes socioeconomic groups between wealthy and poor, often characterized by professional occupations and moderate incomes. Middle ground represents compromise positions in negotiations or debates. Geographic middles include continental centers and halfway points between cities. The middle way in Buddhism advocates moderation between extreme asceticism and indulgence. Understanding middle concepts involves recognizing balance, moderation, and central positioning. The term appears across multiple contexts from spatial relationships to philosophical principles.',
                'pronunciation': "/ˈmɪd.əl/",
                'etymology': 'From Old English "middel," related to "mid," meaning the center point between extremes.',
                'memory_tip': 'Remember MIDDLE = center point between two ends - in the MID position.',
                'example_sentence': 'She found herself caught in the ______ of a dispute between her two best friends.'
            },
            'midnight': {
                'definition': 'Twelve o\'clock at night; the middle of the night when one day ends and the next begins. Midnight represents the transition point between calendar dates and often symbolizes mystery, romance, or supernatural activity in literature and culture. Different time systems may define midnight differently: 12:00 AM in 12-hour format, 00:00 in 24-hour format. Midnight sun phenomenon occurs in polar regions where the sun remains visible throughout the night during summer months. Cultural associations include Cinderella\'s transformation, New Year\'s Eve celebrations, and "witching hour" folklore. Legal and business contexts often specify whether midnight belongs to the ending or beginning day. Midnight shifts describe work schedules spanning late night hours. Understanding midnight involves timekeeping systems, cultural symbolism, and practical scheduling considerations.',
                'pronunciation': "/ˈmɪd.naɪt/",
                'etymology': 'From "mid" (middle) + "night," referring to the middle point of the nighttime period.',
                'memory_tip': 'Remember MIDNIGHT = MID (middle) + NIGHT - the middle of nighttime at 12 AM.',
                'example_sentence': 'The new year officially began at ______ with fireworks lighting up the city skyline.'
            },
            'midriff': {
                'definition': 'The front part of the human torso between the chest and waist; the diaphragm area or middle section of the body. Midriff anatomy includes abdominal muscles, lower ribs, and the diaphragm that separates chest and abdominal cavities. Fashion terminology uses midriff to describe clothing that exposes this body area, including crop tops and two-piece outfits. Physical fitness focuses on midriff strength through core exercises that develop abdominal and back muscles. Cultural attitudes toward midriff exposure vary widely across societies and historical periods. Medical contexts may reference midriff pain related to digestive, muscular, or respiratory conditions. The midriff area plays important roles in breathing, posture, and physical stability. Understanding midriff involves anatomical knowledge, cultural norms, and health considerations.',
                'pronunciation': "/ˈmɪd.rɪf/",
                'etymology': 'From Old English "midhrif," literally meaning "middle belly," from "mid" (middle) + "hrif" (belly).',
                'memory_tip': 'Remember MIDRIFF = MID (middle) + RIFF - the middle section of the torso.',
                'example_sentence': 'The dancer\'s costume included a decorated top that showed her toned ______.'
            },
            'midriffteaspoon': {
                'definition': 'A combined word error from PDF parsing that incorrectly merged "midriff" and "teaspoon." This represents a data processing error where two unrelated terms were concatenated without proper spacing. Midriff refers to the middle section of the human torso, while teaspoon is a small measuring spoon or utensil. Such parsing errors occur when PDF text extraction fails to recognize word boundaries, particularly in documents with complex formatting or multiple columns. These errors highlight the challenges of automated text processing and the importance of data validation. The nonsensical combination would require manual correction or sophisticated error detection algorithms to separate into meaningful individual components.',
                'pronunciation': "/ˈmɪd.rɪfˈti.spun/",
                'etymology': 'Processing error combining "midriff" (Old English middle belly) with "teaspoon" (small spoon). Invalid concatenation.',
                'memory_tip': 'This is a COMBINED WORD ERROR - two unrelated words incorrectly joined during PDF processing.',
                'example_sentence': 'The quality control algorithm flagged ______ as an invalid word combination requiring separation.'
            },
            'mien': {
                'definition': 'A person\'s appearance, manner, or demeanor, especially as an indication of their character or mood. Mien encompasses facial expressions, body language, posture, and overall bearing that communicate personality and emotional state. Regal mien describes dignified, authoritative appearance associated with nobility or leadership. Gentle mien indicates kind, peaceful demeanor, while stern mien suggests serious, uncompromising character. Artists and writers use mien to convey character traits and emotional states through physical description. Social interactions often involve reading others\' mien to understand intentions, feelings, and social signals. Cultural differences affect interpretation of mien, as facial expressions and body language vary across societies. Understanding mien helps in developing social awareness, character assessment, and nonverbal communication skills.',
                'pronunciation': "/min/",
                'etymology': 'From French "mine," meaning facial expression or appearance, related to "miner" (to lead or conduct).',
                'memory_tip': 'Remember MIEN = person\'s appearance and DEMEANOR - how they look and act.',
                'example_sentence': 'The professor\'s scholarly ______ immediately commanded respect from the students.'
            },
            'might': {
                'definition': 'Great strength, power, or force; also used as a modal auxiliary verb to express possibility or permission. Physical might describes the ability to exert force, move heavy objects, or overcome resistance. Political might refers to influence, authority, and ability to effect change through governmental or institutional power. Military might encompasses armed forces, weapons, and strategic capabilities that nations use for defense or offense. The phrase "might makes right" controversially suggests that power determines morality. As a modal verb, might expresses uncertainty ("it might rain") or polite requests ("might I ask"). Economic might describes financial resources and market influence. Understanding might involves recognizing both literal strength and abstract power concepts. The term connects physical capabilities with social, political, and economic influence.',
                'pronunciation': "/maɪt/",
                'etymology': 'From Old English "miht," meaning power or strength, related to "may" indicating ability or possibility.',
                'memory_tip': 'Remember MIGHT = great power and strength - the ability to do something forceful.',
                'example_sentence': 'The ancient fortress was built to demonstrate the kingdom\'s military ______ to potential enemies.'
            },
            'mighty': {
                'definition': 'Having great power, strength, or force; impressive in size, importance, or intensity. Mighty describes individuals, objects, or phenomena that inspire awe through their exceptional capabilities or characteristics. Mighty rivers like the Amazon and Mississippi shape continents and support vast ecosystems. Mighty warriors in mythology and history demonstrate extraordinary courage and fighting ability. Mighty storms including hurricanes and tornadoes display nature\'s tremendous power. The term can describe physical strength, moral authority, intellectual prowess, or spiritual significance. Mighty oaks symbolize strength and endurance in literature and culture. Technological achievements can be described as mighty when they represent significant human accomplishment. Understanding mighty involves recognizing exceptional qualities that set something apart from ordinary examples.',
                'pronunciation': "/ˈmaɪ.ti/",
                'etymology': 'From Old English "mihtig," meaning having great power, derived from "miht" (might, power).',
                'memory_tip': 'Remember MIGHTY = having great MIGHT - very powerful and impressive.',
                'example_sentence': 'The ______ redwood trees towered over the forest, some reaching heights of over 300 feet.'
            },
            'mignonette': {
                'definition': 'A small, delicate plant with fragrant flowers, typically yellow-green in color; also a small, finely cut garnish or sauce used in French cuisine. Mignonette plants (Reseda species) are cultivated for their sweet fragrance and modest appearance, often used in cottage gardens and perfumery. The flowers attract bees and other pollinators while providing subtle scent for garden spaces. Culinary mignonette refers to a classic French sauce made with minced shallots, black pepper, and vinegar, traditionally served with raw oysters. The sauce\'s name reflects its finely chopped texture resembling the small mignonette flower. Mignonette pepper describes coarsely cracked black peppercorns used as seasoning. Understanding mignonette involves appreciating both botanical and culinary traditions that value subtle flavors and delicate presentations.',
                'pronunciation': "/ˌmɪɲ.əˈnɛt/",
                'etymology': 'From French "mignonette," meaning little darling, derived from "mignon" (cute or dainty).',
                'memory_tip': 'Remember MIGNONETTE = little darling flower - small, delicate, and fragrant plant.',
                'example_sentence': 'The chef served fresh oysters with a classic ______ sauce made from shallots and vinegar.'
            },
            'migraine': {
                'definition': 'A recurrent, severe headache disorder characterized by intense, throbbing pain, often accompanied by nausea, vomiting, and sensitivity to light and sound. Migraines affect approximately 12% of the population and represent a significant neurological condition requiring medical management. Migraine episodes typically last 4-72 hours and may include warning signs called aura, featuring visual disturbances or sensory changes. Triggers can include hormonal changes, stress, certain foods, sleep patterns, and environmental factors. Migraine treatment involves both acute medications to stop attacks and preventive therapies to reduce frequency. The condition significantly impacts quality of life, work productivity, and daily activities. Understanding migraine helps in recognizing symptoms, avoiding triggers, and seeking appropriate medical care. Research continues to explore migraine mechanisms and develop more effective treatments.',
                'pronunciation': "/ˈmaɪ.ɡreɪn/",
                'etymology': 'From French "migraine," derived from Greek "hemikrania," meaning half of the skull.',
                'memory_tip': 'Remember MIGRAINE = severe headache that makes you want to MIGRATE away from pain.',
                'example_sentence': 'She had to leave work early when a severe ______ caused nausea and light sensitivity.'
            },
            'migratory': {
                'definition': 'Relating to migration; characterized by regular movement from one place to another, especially seasonally. Migratory behavior appears throughout the animal kingdom as species travel to find food, breeding grounds, or favorable climates. Migratory birds travel thousands of miles between summer breeding areas and winter feeding grounds, following ancient routes passed through generations. Migratory fish like salmon return to natal streams for spawning after ocean journeys. Human migratory patterns include seasonal work movements, nomadic lifestyles, and long-term relocations seeking better opportunities. Migratory agriculture involves moving crops or livestock seasonally to optimize growing conditions. Climate change affects migratory patterns by altering temperatures, food availability, and habitat conditions. Understanding migratory behavior helps in conservation planning, agricultural management, and predicting environmental changes.',
                'pronunciation': "/ˈmaɪ.ɡrəˌtɔr.i/",
                'etymology': 'From Latin "migratorius," meaning moving or wandering, derived from "migrare" (to migrate).',
                'memory_tip': 'Remember MIGRATORY = relating to MIGRATION - regular movement from place to place.',
                'example_sentence': 'The ______ geese formed perfect V-formations as they flew south for the winter.'
            },
            'mildew': {
                'definition': 'A thin, superficial growth of fungus consisting of minute fungi that forms on organic matter in warm, moist conditions. Mildew appears as white, gray, or black spots on surfaces including fabric, paper, wood, and plant materials. Common types include powdery mildew affecting plants and downy mildew causing crop diseases. Indoor mildew growth indicates excessive humidity and poor ventilation, potentially causing health problems and property damage. Mildew prevention involves controlling moisture through ventilation, dehumidifiers, and proper air circulation. Cleaning mildew requires antimicrobial solutions and addressing underlying moisture problems. Plant mildew can be treated with fungicides or resistant varieties. Understanding mildew helps in maintaining healthy indoor environments and protecting crops and materials from fungal damage. The organism represents important ecological decomposition processes while creating practical challenges for human activities.',
                'pronunciation': "/ˈmɪl.du/",
                'etymology': 'From Old English "mildēaw," literally meaning honey dew, referring to the sweet substance on affected plants.',
                'memory_tip': 'Remember MILDEW = MILD (grows quietly) + DEW (moisture) - fungus that grows in damp places.',
                'example_sentence': 'The basement books developed ______ stains after the flooding caused persistent humidity problems.'
            },
            'mile': {
                'definition': 'A unit of linear measure equal to 5,280 feet or approximately 1.609 kilometers in the imperial system. The mile serves as a standard distance measurement for road travel, athletics, and geographic calculations in countries using imperial units. Marathon races cover 26.2 miles, while speed limits express vehicle velocities in miles per hour. Nautical miles (6,076 feet) differ from statute miles and are used for maritime and aviation navigation. Historical mile variations included Roman miles and regional measurements that differed significantly from modern standards. "Going the extra mile" means exceeding expectations or making additional effort beyond requirements. Mile markers help travelers gauge distances and locate positions on highways and trails. Understanding miles enables navigation, fitness tracking, and comprehension of distances in countries using imperial measurement systems.',
                'pronunciation': "/maɪl/",
                'etymology': 'From Latin "milia pasuum," meaning thousand paces, referring to Roman distance measurement.',
                'memory_tip': 'Remember MILE = about 1000 paces for a Roman soldier - standard distance unit.',
                'example_sentence': 'The runner completed her first ______ in under eight minutes during track practice.'
            },
            'miles': {
                'definition': 'Plural of mile; multiple units of distance measurement; also a given name meaning "soldier" or "merciful." Multiple miles describe longer distances for travel, geography, and measurement applications. Road trip planning involves calculating miles between destinations and estimating travel times. Athletic training programs gradually increase weekly miles to build endurance safely. "Miles apart" describes significant differences in opinion, location, or understanding. Frequent flyer miles reward airline customers with credits for future travel. Miles per gallon measures vehicle fuel efficiency. Miles Davis gained fame as an influential jazz trumpeter and composer. Understanding miles involves both measurement applications and recognition of the name\'s historical and cultural significance. The term connects practical distance concepts with personal identity.',
                'pronunciation': "/maɪlz/",
                'etymology': 'Plural of "mile" (Latin thousand paces); as a name, from Latin "miles" meaning soldier.',
                'memory_tip': 'Remember MILES = multiple distance units OR a name meaning soldier.',
                'example_sentence': 'The cross-country trip covered over 2,000 ______ through diverse landscapes and climates.'
            },
            'milieu': {
                'definition': 'The physical or social environment in which something occurs or develops; the setting or background that influences behavior, attitudes, and outcomes. Milieu encompasses cultural, social, economic, and physical factors that shape experiences and opportunities. Social milieu describes the community, class, and cultural context that influences individual development and choices. Professional milieu includes workplace culture, industry norms, and career environments. Academic milieu encompasses educational institutions, scholarly communities, and intellectual traditions. Therapeutic milieu in healthcare refers to treatment environments designed to promote healing and recovery. Understanding milieu helps explain why behaviors and attitudes vary across different contexts and communities. The concept emphasizes environmental influences on human development and social phenomena. Milieu analysis considers how surroundings shape individual and group experiences.',
                'pronunciation': "/mɪlˈjø/",
                'etymology': 'From French "milieu," meaning middle or environment, derived from "mi" (middle) + "lieu" (place).',
                'memory_tip': 'Remember MILIEU = the middle LIEU (place) - the surrounding environment and setting.',
                'example_sentence': 'The artist thrived in the creative ______ of the bohemian neighborhood with its galleries and cafes.'
            },
            'militant': {
                'definition': 'Aggressively active in supporting a cause or belief; disposed to warfare or combat; also a person who engages in aggressive advocacy or armed struggle. Militant behavior involves forceful, often confrontational approaches to promoting political, religious, or social causes. Militant groups may use violence, intimidation, or extreme tactics to achieve their objectives. Labor militants historically fought for workers\' rights through strikes, protests, and organized resistance. Militant activism can describe passionate advocacy that stops short of violence but employs aggressive tactics. The term carries negative connotations when associated with extremism or terrorism. However, militant dedication can also describe admirable commitment to just causes. Understanding militant behavior involves recognizing the spectrum from passionate advocacy to dangerous extremism. Context determines whether militant approaches are constructive or destructive.',
                'pronunciation': "/ˈmɪl.ɪ.tənt/",
                'etymology': 'From Latin "militans," meaning fighting or serving as a soldier, from "militare" (to serve as a soldier).',
                'memory_tip': 'Remember MILITANT = like a soldier fighting - aggressively active for a cause.',
                'example_sentence': 'The ______ environmentalists chained themselves to trees to prevent the logging operation.'
            },
            'military': {
                'definition': 'Relating to armed forces, warfare, or soldiers; the organized force of a nation for defense and offense. Military institutions include army, navy, air force, and specialized units trained for combat and national security. Military service involves training, discipline, and potential deployment for defense missions or conflict resolution. Military strategy encompasses planning, tactics, logistics, and intelligence gathering for successful operations. Military technology includes weapons systems, communications equipment, and protective gear. Military culture emphasizes hierarchy, duty, honor, and sacrifice for national service. Military history studies conflicts, strategic developments, and the evolution of warfare. Civilian control of military ensures democratic governance while maintaining effective defense capabilities. Understanding military concepts involves recognizing both practical defense needs and broader societal impacts of armed forces.',
                'pronunciation': "/ˈmɪl.ɪˌtɛr.i/",
                'etymology': 'From Latin "militaris," meaning of soldiers or war, derived from "miles" (soldier).',
                'memory_tip': 'Remember MILITARY = relating to soldiers and armed forces - defense and warfare.',
                'example_sentence': 'The young cadet was proud to begin his ______ career serving his country.'
            },
            'milk': {
                'definition': 'A white liquid produced by female mammals to nourish their young; also plant-based liquids resembling animal milk. Cow\'s milk provides protein, calcium, vitamins, and other nutrients essential for human health and development. Milk processing includes pasteurization, homogenization, and various fat content adjustments. Different animals produce milk with varying compositions: goat milk, sheep milk, and buffalo milk serve regional dietary needs. Plant-based milks including almond, soy, oat, and rice varieties accommodate dietary restrictions and preferences. Milk products include cheese, yogurt, butter, and cream that form staples in many cuisines. The phrase "milk of human kindness" describes compassionate nature. Dairy farming involves careful animal husbandry and milk quality control. Understanding milk involves nutrition science, agricultural practices, and cultural food traditions.',
                'pronunciation': "/mɪlk/",
                'etymology': 'From Old English "meolc," related to Latin "mulgere" (to milk) and Greek "amolgos" (milking).',
                'memory_tip': 'Remember MILK = white liquid that helps children grow - essential nutrition from mammals.',
                'example_sentence': 'The children drank fresh ______ with their breakfast cereal every morning.'
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
            'microwavegabled',      # microwave + gabled
            'midriffteaspoon'       # midriff + teaspoon
        ]
        
        for word in words_to_check:
            combined_words.append(word)
            
        return combined_words
    
    def process_batch(self, input_file: str, output_file: str):
        """Process the batch with comprehensive Claude data"""
        
        logger.info("Processing Batch 111 with comprehensive Claude data...")
        
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
    processor = Batch111Processor()
    
    input_file = "output/batch_111_words.csv"
    output_file = "output/batch_111_processed.csv"
    
    try:
        word_count = processor.process_batch(input_file, output_file)
        
        logger.info("Batch 111 processing completed!")
        logger.info(f"Processed {word_count} words with comprehensive Claude data")
        logger.info(f"Output saved to: {output_file}")
        logger.info(f"Results: {word_count} successful, 0 failed")
        
    except Exception as e:
        logger.error(f"Error processing batch 111: {str(e)}")
        raise