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

class Batch124Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        self.combined_words = []
        
    def detect_combined_words(self) -> List[str]:
        combined_patterns = [
            'ostensiblyosteopath',
            'otherbedroom'
        ]
        return combined_patterns
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        word_data = {
            'organic': {
                'definition': 'Relating to or derived from living organisms, or denoting a method of farming that avoids synthetic chemical fertilizers and pesticides. In chemistry, organic compounds contain carbon atoms bonded to hydrogen. The term emphasizes natural processes and materials, distinguishing them from synthetic or artificial alternatives. In agriculture, organic practices focus on soil health, biodiversity, and ecological balance. The word has expanded to describe anything perceived as natural, wholesome, or authentic, from food products to marketing approaches that emphasize genuine development.',
                'pronunciation': '/ɔrˈɡænɪk/',
                'pronunciation_ipa': '/ɔrˈɡænɪk/',
                'etymology': 'From Greek "organikos" meaning "of or pertaining to an organ or instrument," from "organon" meaning tool or instrument. The term evolved to describe anything relating to living organisms and their natural processes.',
                'memory_tip': 'Remember ORGANIC = ORGANs + IC. Think of organs being natural parts of living things, just like organic materials come from living sources.',
                'example_sentence': 'The farmer decided to convert his entire operation to _____ farming methods to produce healthier vegetables.'
            },
            'organist': {
                'definition': 'A person who plays the organ, particularly in churches, concert halls, or other venues where pipe organs or electronic organs are used. Organists often accompany religious services, weddings, funerals, and concerts. The role requires advanced musical training, as organ playing involves complex coordination of hands and feet across multiple keyboards and pedals. Many organists also serve as music directors, choir directors, or composers. The profession has a rich history spanning centuries, with organists playing crucial roles in both sacred and secular musical traditions.',
                'pronunciation': '/ˈɔrɡənɪst/',
                'pronunciation_ipa': '/ˈɔrɡənɪst/',
                'etymology': 'From "organ" (the musical instrument) plus the suffix "-ist" (one who practices or specializes in). The word "organ" comes from Latin "organum," from Greek "organon" meaning tool or instrument.',
                'memory_tip': 'Remember ORGANIST = ORGAN + IST. The suffix "-ist" means "one who does" - so an organist is one who plays the organ.',
                'example_sentence': 'The church _____ played beautiful hymns during the wedding ceremony.'
            },
            'organized': {
                'definition': 'Arranged in a systematic way; having a formal organizational structure; methodically planned and coordinated. In a personal context, it describes someone who manages their time, space, and activities efficiently. In business or social contexts, it refers to groups that have established structures, rules, and procedures. The term can also describe crime syndicates or labor movements that operate with formal hierarchies and systems. Being organized typically leads to increased efficiency, reduced stress, and better outcomes in various endeavors.',
                'pronunciation': '/ˈɔrɡəˌnaɪzd/',
                'pronunciation_ipa': '/ˈɔrɡəˌnaɪzd/',
                'etymology': 'From "organize" (from French "organiser," ultimately from Greek "organon" meaning tool or instrument) plus the past participle suffix "-ed." The concept relates to arranging things like parts of an organism or instrument.',
                'memory_tip': 'Think of an ORGANization - when things are ORGANIZED, they work together like organs in a body, each having a specific function and place.',
                'example_sentence': 'The students were much more successful after they _____ their study materials and created a schedule.'
            },
            'organizes': {
                'definition': 'Third person singular present tense of organize; arranges systematically; coordinates and structures activities, objects, or people. The action involves creating order from chaos, establishing systems, and implementing efficient procedures. In social contexts, it can mean bringing people together for a common purpose, such as organizing events, protests, or community activities. In personal productivity, it refers to arranging one\'s schedule, workspace, or thoughts in a logical manner. Effective organization is a key skill in management, education, and daily life.',
                'pronunciation': '/ˈɔrɡəˌnaɪzɪz/',
                'pronunciation_ipa': '/ˈɔrɡəˌnaɪzɪz/',
                'etymology': 'From "organize" (from French "organiser," ultimately from Greek "organon" meaning tool or instrument) plus the third person singular present tense suffix "-s."',
                'memory_tip': 'Remember that when someone ORGANIZES, they create an ORGANization - putting things in systematic order like organs in a body.',
                'example_sentence': 'Every week, she _____ her desk and files to maintain an efficient workspace.'
            },
            'organza': {
                'definition': 'A thin, stiff, transparent fabric made of silk or synthetic fiber, characterized by its crisp texture and lustrous appearance. Organza is commonly used in formal wear, wedding dresses, evening gowns, and decorative applications like curtains or table overlays. The fabric\'s distinctive properties come from its tight weave and the way the fibers are twisted. It holds its shape well, making it ideal for creating volume in garments through ruffles, pleats, and structured designs. Organza can be plain or embellished with embroidery, beading, or metallic threads.',
                'pronunciation': '/ɔrˈɡænzə/',
                'pronunciation_ipa': '/ɔrˈɡænzə/',
                'etymology': 'From French "organzin," possibly derived from "Urgench," a city in Uzbekistan where this type of silk fabric may have originated. The word entered English through the textile trade.',
                'memory_tip': 'Think of ORGANZA as ORGANic + ZA (like pizza). Just as pizza has a crisp base, organza is a crisp, elegant fabric.',
                'example_sentence': 'The bride chose a beautiful _____ overlay for her wedding dress to add volume and elegance.'
            },
            'oriel': {
                'definition': 'A type of bay window that projects from the upper floor of a building, typically supported by brackets or corbels rather than extending to the ground. Oriel windows are architectural features that provide additional light and space to interior rooms while creating visual interest on building exteriors. They are commonly found in medieval and Tudor architecture, as well as in Gothic Revival buildings. The projecting design allows for panoramic views and increased natural lighting. Oriels often feature decorative stonework, mullions, and sometimes stained glass panels.',
                'pronunciation': '/ˈɔriəl/',
                'pronunciation_ipa': '/ˈɔriəl/',
                'etymology': 'From Old French "oriol," meaning a gallery or portico, possibly related to Latin "aureolus" meaning golden, referring to the way these windows catch and reflect light.',
                'memory_tip': 'Think of ORIEL as OR-I-EL (or I will). "Or I will look out this special projecting window" - oriels are distinctive windows that stick out from buildings.',
                'example_sentence': 'The medieval castle featured a beautiful _____ window that allowed the lord to observe the courtyard below.'
            },
            'orientation': {
                'definition': 'The determination of the relative position of something, or the process of familiarizing someone with a new situation or environment. In education and employment, orientation programs introduce newcomers to policies, procedures, and culture. In psychology, it refers to awareness of time, place, and identity. In navigation and geography, it means determining direction relative to cardinal points. Sexual orientation describes patterns of romantic or sexual attraction. The term also applies to the positioning of objects, buildings, or devices relative to their surroundings or intended function.',
                'pronunciation': '/ˌɔriənˈteɪʃən/',
                'pronunciation_ipa': '/ˌɔriənˈteɪʃən/',
                'etymology': 'From French "orientation," from "orienter" meaning to orientate or face east, ultimately from Latin "oriens" meaning rising (sun), east. Originally referred to positioning buildings to face east.',
                'memory_tip': 'ORIENTATION starts with ORIENT - think of getting your bearings, like using a compass to find which way is east (the Orient).',
                'example_sentence': 'New employees must attend a week-long _____ program to learn about company policies and procedures.'
            },
            'origin': {
                'definition': 'The point or place where something begins, arises, or is derived; the source or cause of something. In history and anthropology, it refers to the earliest known existence or development of peoples, customs, or ideas. In mathematics, the origin is the point where coordinate axes intersect. In biology, it describes the beginning of evolutionary development or the attachment point of muscles. The concept of origin is fundamental to understanding causation, development, and identity across various fields of study.',
                'pronunciation': '/ˈɔrɪdʒɪn/',
                'pronunciation_ipa': '/ˈɔrɪdʒɪn/',
                'etymology': 'From Latin "origo, originis" meaning beginning, source, birth, or lineage, from "oriri" meaning to rise or be born. Related to "orient" (east, where the sun rises).',
                'memory_tip': 'ORIGIN sounds like "ORIGInal" - the origin is where something originally came from, its very first beginning.',
                'example_sentence': 'Scientists continue to study the _____ of the universe through observations of distant galaxies.'
            },
            'original': {
                'definition': 'Present or existing from the beginning; first or earliest; not a copy, reproduction, or imitation. In creative contexts, it describes work that is novel, innovative, or unique. An original can be the authentic version from which copies are made, such as an original painting or document. The term also describes people who think independently and creatively. In legal contexts, original jurisdiction refers to the authority to hear a case first. Being original is highly valued in art, literature, invention, and intellectual pursuits.',
                'pronunciation': '/əˈrɪdʒənəl/',
                'pronunciation_ipa': '/əˈrɪdʒənəl/',
                'etymology': 'From Latin "originalis" meaning of or pertaining to an origin, from "origo" meaning beginning or source. The sense of "novel, innovative" developed later in English.',
                'memory_tip': 'ORIGINAL contains ORIGIN - an original thing goes back to its very origin, it\'s not a copy but the first or authentic version.',
                'example_sentence': 'The museum acquired the _____ manuscript of the famous author\'s first novel.'
            },
            'originally': {
                'definition': 'At first; in the beginning; from the start; as originally conceived or intended. The adverb describes the initial state, plan, or condition of something before changes, modifications, or developments occurred. It can refer to temporal sequence (what happened first) or to authentic, fundamental characteristics. In academic and historical contexts, it helps distinguish between initial conditions and subsequent developments. The word often introduces explanations of how something began versus how it evolved.',
                'pronunciation': '/əˈrɪdʒənəli/',
                'pronunciation_ipa': '/əˈrɪdʒənəli/',
                'etymology': 'From "original" plus the adverb suffix "-ly." Traces back to Latin "originalis" from "origo" meaning beginning or source.',
                'memory_tip': 'ORIGINALLY = ORIGINAL + LY. Think "in the original way" - how something was at its very beginning.',
                'example_sentence': 'The building was _____ designed as a warehouse but was later converted into luxury apartments.'
            },
            'originate': {
                'definition': 'To create, initiate, or bring into being; to have one\'s beginning in a particular place, time, or situation. The verb describes the process of something coming into existence for the first time or being invented. In business, it can refer to creating new products, services, or ideas. In geography and science, it describes where natural phenomena or processes begin. The word implies being the source or cause of something new, rather than merely transmitting or modifying existing elements.',
                'pronunciation': '/əˈrɪdʒəˌneɪt/',
                'pronunciation_ipa': '/əˈrɪdʒəˌneɪt/',
                'etymology': 'From Latin "originatus," past participle of "originari" meaning to begin or rise, from "origo" meaning beginning or source. The verb form entered English in the 17th century.',
                'memory_tip': 'ORIGINATE = ORIGIN + ATE. To originate is to create something at its origin, to be the starting point where it begins.',
                'example_sentence': 'Many of our modern customs _____ from ancient religious and cultural traditions.'
            },
            'originates': {
                'definition': 'Third person singular present tense of originate; begins, starts, or has its source in a particular place, time, or cause. The verb describes the process by which something comes into being or the point from which it derives. In scientific contexts, it often refers to natural phenomena and their sources. In business and innovation, it describes the creation of new ideas, products, or services. The word emphasizes the act of being the first or primary source of something.',
                'pronunciation': '/əˈrɪdʒəˌneɪts/',
                'pronunciation_ipa': '/əˈrɪdʒəˌneɪts/',
                'etymology': 'From "originate" plus the third person singular present tense suffix "-s." Derives from Latin "originari" meaning to begin or arise.',
                'memory_tip': 'ORIGINATES = ORIGIN + ATES. When something originates, it starts at its origin point - where it first begins to exist.',
                'example_sentence': 'The Amazon River _____ in the Peruvian Andes and flows east across South America.'
            },
            'orinoco': {
                'definition': 'One of the longest rivers in South America, flowing through Venezuela and Colombia. The Orinoco River spans approximately 1,330 miles (2,140 kilometers) and is a crucial waterway for transportation, agriculture, and hydroelectric power generation. It forms part of the border between Venezuela and Colombia and empties into the Atlantic Ocean through a vast delta. The river basin supports diverse ecosystems and indigenous communities. The Orinoco is economically important for oil deposits in its basin and serves as a major transportation route for the region.',
                'pronunciation': '/ˌɔrɪˈnoʊkoʊ/',
                'pronunciation_ipa': '/ˌɔrɪˈnoʊkoʊ/',
                'etymology': 'From Spanish "Orinoco," possibly derived from local indigenous languages. The exact etymology is uncertain, but it may relate to indigenous words for "river" or refer to geographical features of the region.',
                'memory_tip': 'Remember ORINOCO as "O-RIN-O-CO" - think of it flowing like a ring (RIN) of water across two countries (CO for Colombia and Venezuela).',
                'example_sentence': 'The _____ River serves as an important transportation route connecting inland Venezuela with the Atlantic Ocean.'
            },
            'oriole': {
                'definition': 'A brightly colored songbird belonging to the family Icteridae (New World orioles) or Oriolidae (Old World orioles). Orioles are known for their vibrant yellow, orange, and black plumage and their melodious songs. They are often found in woodlands, gardens, and parks, where they feed on insects, nectar, and fruit. Many species are migratory, traveling long distances between breeding and wintering grounds. Orioles are skilled nest builders, creating hanging, pouch-like structures woven from plant fibers. They are popular among birdwatchers and often visit backyard feeders.',
                'pronunciation': '/ˈɔriˌoʊl/',
                'pronunciation_ipa': '/ˈɔriˌoʊl/',
                'etymology': 'From Old French "oriol," from Latin "aureolus" meaning golden, referring to the bird\'s bright golden-yellow coloring. The name reflects the distinctive golden plumage of many oriole species.',
                'memory_tip': 'ORIOLE sounds like "AUR-I-OLE" (golden). Remember aureolus means golden - orioles are the golden, bright-colored birds.',
                'example_sentence': 'The Baltimore _____ is Maryland\'s state bird, known for its brilliant orange and black feathers.'
            },
            'orion': {
                'definition': 'A prominent constellation visible in both hemispheres, named after the hunter in Greek mythology. Orion is easily recognizable by its distinctive pattern of bright stars, including the three stars of Orion\'s Belt and the bright stars Betelgeuse and Rigel. The constellation contains several notable deep-sky objects, including the Orion Nebula, a star-forming region visible to the naked eye. In mythology, Orion was a great hunter who was placed among the stars. The constellation serves as a guide for finding other stars and constellations in winter skies.',
                'pronunciation': '/əˈraɪən/',
                'pronunciation_ipa': '/əˈraɪən/',
                'etymology': 'From Greek "Ōrion," the name of a hunter in Greek mythology. The name may be related to Greek words meaning "boundary" or "limit," possibly referring to the constellation\'s position in the sky.',
                'memory_tip': 'ORION the hunter has three stars in his belt - just like "O-RI-ON" has three syllables. Picture the hunter with his distinctive belt of stars.',
                'example_sentence': 'During winter nights, the constellation _____ is easily visible in the southern sky, marked by its famous three-star belt.'
            },
            'ormolu': {
                'definition': 'A decorative technique using gilt bronze or brass to create ornamental mountings, typically for furniture, clocks, and luxury objects. Ormolu involves applying a thin layer of gold to bronze through fire-gilding or electroplating, creating a lustrous, durable finish that resists tarnishing. The technique reached its peak during the 18th century in France, where skilled craftsmen created elaborate decorative elements for royal furniture and architectural details. Ormolu pieces are highly valued by collectors and museums for their artistic merit and historical significance. The process requires great skill to achieve the characteristic warm, golden appearance.',
                'pronunciation': '/ˈɔrməˌlu/',
                'pronunciation_ipa': '/ˈɔrməˌlu/',
                'etymology': 'From French "or moulu" meaning "ground gold," referring to the powdered gold used in the gilding process. The term reflects the technique of applying gold to bronze surfaces.',
                'memory_tip': 'ORMOLU = OR (gold in French) + MOULU (ground). Think of "OR-MORE-GOLD" - ormolu adds more gold decoration to bronze objects.',
                'example_sentence': 'The antique French clock featured intricate _____ decorations that gleamed with their original golden finish.'
            },
            'ornament': {
                'definition': 'A decorative object or detail used to enhance the appearance or beauty of something; to decorate or adorn with ornamental features. Ornaments can be functional or purely aesthetic, ranging from jewelry and artwork to architectural details and holiday decorations. In music, ornaments are embellishments that decorate the basic melody. The concept of ornamentation spans cultures and time periods, reflecting aesthetic values and craftsmanship. Personal ornaments like jewelry often carry cultural, religious, or sentimental significance beyond their decorative function.',
                'pronunciation': '/ˈɔrnəmənt/',
                'pronunciation_ipa': '/ˈɔrnəmənt/',
                'etymology': 'From Latin "ornamentum" meaning equipment, decoration, or embellishment, from "ornare" meaning to equip, furnish, or decorate. The word emphasizes the enhancing function of decorative elements.',
                'memory_tip': 'ORNAMENT sounds like "ORNate + MENT" - ornate things are decorated with ornaments that add beauty and detail.',
                'example_sentence': 'The Christmas tree was decorated with colorful glass _____ that had been in the family for generations.'
            },
            'ornithology': {
                'definition': 'The scientific study of birds, including their behavior, ecology, evolution, physiology, and classification. Ornithologists study bird migration patterns, breeding behaviors, habitat requirements, and conservation needs. The field combines fieldwork, laboratory research, and data analysis to understand avian biology and ecology. Ornithology contributes to conservation efforts, environmental monitoring, and our understanding of evolution and biodiversity. Professional ornithologists work in universities, museums, government agencies, and conservation organizations. Citizen science projects often involve amateur birdwatchers contributing valuable data to ornithological research.',
                'pronunciation': '/ˌɔrnɪˈθɑlədʒi/',
                'pronunciation_ipa': '/ˌɔrnɪˈθɑlədʒi/',
                'etymology': 'From Greek "ornis, ornithos" meaning bird + "logos" meaning study or science. The term was coined in the 17th century as the scientific study of birds developed.',
                'memory_tip': 'ORNITHOLOGY = ORNITHO (bird in Greek) + LOGY (study). Think "OR-NITH-OLOGY" - the study of birds and their behavior.',
                'example_sentence': 'Her graduate studies in _____ focused on the migration patterns of Arctic terns.'
            },
            'orogeny': {
                'definition': 'The process of mountain formation through tectonic plate movements, folding, faulting, and volcanic activity. Orogeny occurs when Earth\'s crustal plates collide, causing the land to buckle, fold, and rise into mountain ranges. The process can take millions of years and involves complex geological forces including compression, uplift, and metamorphism. Different types of orogeny create different mountain characteristics, from volcanic chains to folded sedimentary ranges. Understanding orogeny helps geologists interpret Earth\'s history and predict geological hazards like earthquakes and landslides.',
                'pronunciation': '/ɔˈrɑdʒəni/',
                'pronunciation_ipa': '/ɔˈrɑdʒəni/',
                'etymology': 'From Greek "oros" meaning mountain + "genesis" meaning birth or origin. The term describes the birth or formation of mountains through geological processes.',
                'memory_tip': 'OROGENY = ORO (mountain) + GENY (genesis/birth). Think of the "origin of mountains" - how mountains are born through geological forces.',
                'example_sentence': 'The Appalachian Mountains were formed through ancient _____ that occurred millions of years ago.'
            },
            'orphéon': {
                'definition': 'A type of male choral society that originated in 19th-century France, typically consisting of amateur singers from working-class backgrounds. Orphéons were cultural institutions that promoted musical education and social cohesion in industrial communities. These choirs performed secular music, often with patriotic or social themes, and participated in competitive festivals. The movement spread throughout France and influenced similar choral traditions in other countries. Orphéons played important roles in community life, providing entertainment, education, and social organization. Many were associated with factories, neighborhoods, or political movements.',
                'pronunciation': '/ɔrˈfeɪɔn/',
                'pronunciation_ipa': '/ɔrˈfeɪɔn/',
                'etymology': 'From French "orphéon," named after Orpheus, the legendary musician and poet of Greek mythology. The name reflects the musical nature of these choral societies.',
                'memory_tip': 'ORPHÉON comes from ORPHEUS, the legendary musician. Think of Orpheus leading a choir - orphéons were choral societies for community singing.',
                'example_sentence': 'The local _____ performed traditional French songs at the community festival.'
            },
            'orsay': {
                'definition': 'A town in the Essonne department in the Île-de-France region of north-central France, known for its university and scientific research facilities. Orsay is home to the Université Paris-Sud (now part of Université Paris-Saclay), one of France\'s leading universities for science and technology. The town has evolved from a rural agricultural area to an important center for higher education and research. It houses numerous laboratories and research institutes, making it a significant part of the greater Paris scientific community. The name is also associated with the famous Musée d\'Orsay in Paris.',
                'pronunciation': '/ɔrˈseɪ/',
                'pronunciation_ipa': '/ɔrˈseɪ/',
                'etymology': 'From the French place name, possibly derived from a Gallo-Roman personal name "Orcius" plus the suffix "-acum" indicating possession or location.',
                'memory_tip': 'ORSAY sounds like "OR-SAY" - you might say "or say we go to Orsay" when discussing this French university town.',
                'example_sentence': 'The physics department at _____ University is renowned for its research in quantum mechanics.'
            },
            'orthogonal': {
                'definition': 'At right angles; perpendicular; in mathematics, describing lines, planes, or vectors that intersect at 90-degree angles. In broader contexts, orthogonal means independent or unrelated, with no correlation or mutual influence. In engineering and design, orthogonal approaches involve separating different aspects or functions to avoid interference. In statistics, orthogonal variables are uncorrelated. The concept is fundamental in geometry, linear algebra, computer science, and various technical fields where independence and perpendicularity are important principles.',
                'pronunciation': '/ɔrˈθɑɡənəl/',
                'pronunciation_ipa': '/ɔrˈθɑɡənəl/',
                'etymology': 'From Greek "orthos" meaning straight or right + "gonia" meaning angle. The term literally means "right-angled" and extends to describe independence in various contexts.',
                'memory_tip': 'ORTHOGONAL = ORTHO (straight/right) + GONAL (angle). Think of a right angle - orthogonal lines meet at perfect 90-degree angles.',
                'example_sentence': 'The two research approaches were completely _____, allowing the team to pursue both without any conflict or overlap.'
            },
            'orwellian': {
                'definition': 'Characteristic of the dystopian society depicted in George Orwell\'s novels, particularly "1984," involving totalitarian control, surveillance, propaganda, and manipulation of truth. Orwellian describes situations where government or authority uses deceptive language, constant monitoring, or thought control to maintain power. The term is applied to real-world situations involving censorship, propaganda, privacy invasion, or authoritarian overreach. It encompasses concepts like "doublethink," "newspeak," and "Big Brother" that have become part of political discourse about freedom and government control.',
                'pronunciation': '/ɔrˈwɛliən/',
                'pronunciation_ipa': '/ɔrˈwɛliən/',
                'etymology': 'Named after George Orwell (Eric Blair, 1903-1950), the British author who wrote dystopian novels "1984" and "Animal Farm." The adjective was coined to describe the totalitarian society he depicted.',
                'memory_tip': 'ORWELLIAN comes from George ORWELL, who wrote "1984." Think of Big Brother watching you - Orwellian means totalitarian surveillance and control.',
                'example_sentence': 'The government\'s new surveillance program struck many citizens as deeply _____ in its scope and intrusiveness.'
            },
            'oryx': {
                'definition': 'A genus of large antelope native to Africa and Arabia, characterized by long, straight horns and adaptation to arid environments. Oryx species include the Arabian oryx, scimitar oryx, and gemsbok, all known for their striking appearance and remarkable survival abilities in desert conditions. These animals can survive without drinking water for long periods, obtaining moisture from their food. Oryx have cultural significance in Middle Eastern and African societies and appear in art and mythology. Several species have faced extinction due to hunting and habitat loss, leading to conservation efforts including captive breeding programs.',
                'pronunciation': '/ˈɔrɪks/',
                'pronunciation_ipa': '/ˈɔrɪks/',
                'etymology': 'From Greek "oryx" meaning pickaxe or gazelle, referring to the animal\'s straight, pointed horns that resemble the tool. The name reflects the distinctive horn shape.',
                'memory_tip': 'ORYX sounds like "OR-PICKS" - think of their straight horns that look like pickaxes or picks pointing forward.',
                'example_sentence': 'The Arabian _____ was successfully reintroduced to the wild after being extinct in nature for several decades.'
            },
            'oscillation': {
                'definition': 'Repetitive variation or movement between two points, positions, or states; a regular back-and-forth motion around a central point or equilibrium. In physics, oscillation describes phenomena like pendulum swings, vibrating strings, or wave motions. In electronics, it refers to alternating current or signal generation. In broader contexts, oscillation can describe fluctuations in markets, opinions, or decision-making. The concept is fundamental to understanding waves, sound, light, and many natural and technological phenomena. Mathematical analysis of oscillation helps predict and control various systems.',
                'pronunciation': '/ˌɑsəˈleɪʃən/',
                'pronunciation_ipa': '/ˌɑsəˈleɪʃən/',
                'etymology': 'From Latin "oscillatio" from "oscillare" meaning to swing, possibly from "oscillum" (a small mask hung in trees that swayed in the wind). The root suggests swinging or swaying motion.',
                'memory_tip': 'OSCILLATION sounds like "OSCILLating FAN" - think of a fan moving back and forth, that\'s oscillation - regular back-and-forth movement.',
                'example_sentence': 'The engineer studied the _____ patterns of the suspension bridge to ensure it could withstand wind forces.'
            },
            'oscitation': {
                'definition': 'The act of yawning or gaping; drowsiness or sluggishness. In medical and biological contexts, oscitation refers to the physiological response of yawning, which can indicate tiredness, boredom, or changes in oxygen levels. Yawning is contagious among humans and some animals, serving possible social and physiological functions. The term can also describe a state of mental dullness or lack of attention. In literature, oscitation might be used metaphorically to describe lethargy or indifference in broader contexts beyond the physical act of yawning.',
                'pronunciation': '/ˌɑsɪˈteɪʃən/',
                'pronunciation_ipa': '/ˌɑsɪˈteɪʃən/',
                'etymology': 'From Latin "oscitatio" from "oscitare" meaning to yawn or gape, from "os" (mouth) + "citare" (to move or rouse). The word literally refers to mouth movement.',
                'memory_tip': 'OSCITATION sounds like "OSCILLating + SITUATION" - when you\'re in a boring situation, you start oscillating between awake and tired, leading to yawning.',
                'example_sentence': 'The professor noticed the students\' frequent _____ during the lengthy afternoon lecture.'
            },
            'osculatory': {
                'definition': 'Relating to kissing or embracing; pertaining to the act of kissing. In religious contexts, osculatory refers to objects used in ceremonies involving ritual kissing, such as the pax (peace tablet) kissed during Mass. The term can describe behaviors, customs, or artifacts associated with kissing in various cultural or ceremonial contexts. In biology, it might refer to organisms or structures that come into close contact. The word is rarely used in modern English but appears in historical, religious, or scientific literature describing contact behaviors.',
                'pronunciation': '/ˈɑskjələˌtɔri/',
                'pronunciation_ipa': '/ˈɑskjələˌtɔri/',
                'etymology': 'From Latin "osculatorius" from "osculari" meaning to kiss, from "osculum" meaning little mouth or kiss. The root "os" means mouth in Latin.',
                'memory_tip': 'OSCULATORY contains "OSCUL" which sounds like "OSCular" (mouth-related). Think of "OSCULating" as mouth-to-mouth contact - kissing.',
                'example_sentence': 'The medieval manuscript described the _____ customs practiced during religious ceremonies.'
            },
            'osloite': {
                'definition': 'A rare mineral composed primarily of magnesium, iron, and titanium oxide, first discovered in the Oslo region of Norway. Osloite belongs to the magnetite group and forms in alkaline igneous rocks, particularly those associated with the Oslo Graben geological formation. The mineral appears as dark, metallic crystals and is of interest to mineralogists and geologists studying igneous petrology. Its occurrence is limited to specific geological conditions, making it valuable for understanding the formation processes of alkaline rock complexes. Osloite specimens are prized by mineral collectors for their rarity and type locality significance.',
                'pronunciation': '/ˈɑsloʊaɪt/',
                'pronunciation_ipa': '/ˈɑsloʊaɪt/',
                'etymology': 'Named after Oslo, Norway, where it was first discovered, plus the mineral suffix "-ite." The name follows the convention of naming minerals after their type locality.',
                'memory_tip': 'OSLOITE = OSLO + ITE. Like many minerals, it\'s named after the place where it was first found - Oslo, Norway.',
                'example_sentence': 'The geologist identified _____ crystals in the alkaline rock samples from the Norwegian locality.'
            },
            'osmosis': {
                'definition': 'The movement of water molecules through a semipermeable membrane from an area of lower solute concentration to an area of higher solute concentration. This passive transport process is fundamental to cellular biology, maintaining water balance in living organisms. Osmosis occurs in plant cells, animal cells, and many industrial processes. The process can be reversed under pressure (reverse osmosis) for water purification. In figurative use, osmosis describes the gradual absorption of knowledge or ideas through exposure rather than conscious effort, as in "learning by osmosis."',
                'pronunciation': '/ɑzˈmoʊsɪs/',
                'pronunciation_ipa': '/ɑzˈmoʊsɪs/',
                'etymology': 'From Greek "osmos" meaning push or impulse + "-osis" meaning condition or process. Coined in the 19th century to describe the newly understood biological process.',
                'memory_tip': 'OSMOSIS = OS-MO-SIS. Think "OS" (operating system) getting updates - osmosis is like water automatically updating cells by moving through membranes.',
                'example_sentence': 'Plant roots absorb water from the soil through the process of _____, maintaining the plant\'s hydration.'
            },
            'osprey': {
                'definition': 'A large fish-eating bird of prey found on every continent except Antarctica, also known as the fish hawk or sea hawk. Ospreys are distinguished by their distinctive fishing behavior, diving feet-first into water to catch fish with their specially adapted talons. They build large stick nests on tall structures near water bodies. Ospreys were endangered in the mid-20th century due to DDT pesticide use but have made a remarkable recovery through conservation efforts. These birds are migratory, traveling thousands of miles between breeding and wintering grounds. Their success story represents one of conservation\'s greatest achievements.',
                'pronunciation': '/ˈɑspri/',
                'pronunciation_ipa': '/ˈɑspri/',
                'etymology': 'From Latin "ossifraga" meaning bone-breaker, possibly from confusion with other large birds of prey. The name may have evolved through Old French "ospriet."',
                'memory_tip': 'OSPREY sounds like "OS-PREY" - think of it as "the fish\'s prey becomes the osprey\'s prey" since these birds are expert fish hunters.',
                'example_sentence': 'The _____ dove into the lake with remarkable precision and emerged with a large fish clutched in its talons.'
            },
            'ossicle': {
                'definition': 'A small bone, particularly referring to the three tiny bones in the middle ear (malleus, incus, and stapes) that transmit sound vibrations from the eardrum to the inner ear. These are the smallest bones in the human body and are crucial for hearing. The term can also refer to small bones in other animals or any small, bone-like structure. In marine biology, ossicles are calcium carbonate plates that form the skeletons of echinoderms like starfish and sea urchins. The medical study of ossicles is important for understanding hearing disorders and surgical treatments.',
                'pronunciation': '/ˈɑsɪkəl/',
                'pronunciation_ipa': '/ˈɑsɪkəl/',
                'etymology': 'From Latin "ossiculum," diminutive of "os, ossis" meaning bone. The suffix "-cle" indicates smallness, so ossicle means "little bone."',
                'memory_tip': 'OSSICLE = OSS (bone) + ICLE (little). Think of "little bones" - ossicles are the tiny bones in your ear that help you hear.',
                'example_sentence': 'The audiologist explained how damage to the tiny _____ in the middle ear can cause hearing loss.'
            },
            'ossuary': {
                'definition': 'A container or room for the bones of the dead, typically used when cemetery space is limited or for religious purposes. Ossuaries range from small bone boxes to elaborate underground chambers lined with human skulls and bones. They are found in various cultures and religions, serving both practical and spiritual functions. Famous examples include the Catacombs of Paris and the Sedlec Ossuary in the Czech Republic. The practice reflects beliefs about death, remembrance, and the afterlife. Archaeological ossuaries provide valuable information about ancient burial practices and population demographics.',
                'pronunciation': '/ˈɑʃuˌɛri/',
                'pronunciation_ipa': '/ˈɑʃuˌɛri/',
                'etymology': 'From Latin "ossuarium" from "os, ossis" meaning bone. The suffix "-ary" indicates a place for storing, so ossuary means "place for bones."',
                'memory_tip': 'OSSUARY = OSS (bone) + UARY (place). Think of it as a "bone library" - a place where bones are stored and organized.',
                'example_sentence': 'The medieval _____ beneath the church contained the remains of thousands of parishioners from centuries past.'
            },
            'ostensibly': {
                'definition': 'Apparently or purportedly, but perhaps not actually; seemingly or on the surface. The adverb suggests that something appears to be true or is claimed to be true, but there may be hidden motives, alternative explanations, or deceptive appearances. It implies skepticism about whether the apparent reason or situation is the real one. In writing and speech, "ostensibly" often introduces doubt about stated intentions or visible circumstances. The word is commonly used in journalism, analysis, and academic writing to indicate surface appearances versus underlying realities.',
                'pronunciation': '/ɑˈstɛnsəbli/',
                'pronunciation_ipa': '/ɑˈstɛnsəbli/',
                'etymology': 'From Latin "ostensibilis" meaning that can be shown, from "ostendere" meaning to show or display. The word suggests something shown on the surface but potentially hiding deeper truth.',
                'memory_tip': 'OSTENSIBLY sounds like "OH-TEN-SIB-LY" - think "Oh, ten times they SAID this, but..." implying doubt about what\'s claimed versus what\'s real.',
                'example_sentence': 'The meeting was _____ about budget planning, but everyone knew it was really about discussing layoffs.'
            },
            'osteopath': {
                'definition': 'A healthcare practitioner who specializes in osteopathic medicine, emphasizing the musculoskeletal system and the body\'s ability to heal itself. Osteopaths use manual techniques including stretching, massage, and manipulation to treat various conditions. In the United States, Doctors of Osteopathic Medicine (DOs) receive full medical training equivalent to MDs and can prescribe medication and perform surgery. In other countries, osteopaths may focus primarily on manual therapy. The profession emphasizes treating the whole person rather than just symptoms, considering how different body systems interact to maintain health.',
                'pronunciation': '/ˈɑstiəˌpæθ/',
                'pronunciation_ipa': '/ˈɑstiəˌpæθ/',
                'etymology': 'From Greek "osteon" meaning bone + "pathos" meaning suffering or disease. Coined by Andrew Taylor Still, who founded osteopathic medicine in the 19th century.',
                'memory_tip': 'OSTEOPATH = OSTEO (bone) + PATH (disease/treatment). Think of a bone doctor who treats diseases through bone and muscle manipulation.',
                'example_sentence': 'The _____ used gentle manipulation techniques to relieve the patient\'s chronic back pain.'
            },
            'osteson': {
                'definition': 'A rare or archaic term with limited documentation in standard dictionaries. Based on available linguistic evidence, it may refer to a type of bone-related structure or formation, possibly related to ossification or bone development processes. The term appears in specialized medical or anatomical contexts but is not commonly used in modern English. It may be a variant spelling or historical term for bone-related phenomena. Without more definitive sources, the exact meaning remains somewhat uncertain, suggesting it may be a highly technical or obsolete terminology.',
                'pronunciation': '/ˈɑstəsən/',
                'pronunciation_ipa': '/ˈɑstəsən/',
                'etymology': 'Possibly from Greek "osteon" meaning bone, with an uncertain suffix. The exact etymological development is unclear due to limited documented usage.',
                'memory_tip': 'OSTESON contains "OSTE" (bone) like "osteopath" - likely relates to bone structures or bone-related medical terminology.',
                'example_sentence': 'The medical text mentioned _____ as part of the bone formation process, though the term is rarely used in modern anatomy.'
            },
            'ostium': {
                'definition': 'An opening or mouth-like aperture in anatomy, particularly referring to openings in the heart, blood vessels, or other organs. In cardiology, ostia (plural) are the openings where coronary arteries branch from the aorta. In reproductive anatomy, the ostium is the opening of the fallopian tube near the ovary. The term is used in various medical contexts to describe natural openings or passages in the body. Understanding ostial anatomy is crucial for medical procedures like cardiac catheterization and surgical interventions involving these openings.',
                'pronunciation': '/ˈɑstiəm/',
                'pronunciation_ipa': '/ˈɑstiəm/',
                'etymology': 'From Latin "ostium" meaning door, entrance, or mouth, from "os" meaning mouth. The term describes anatomical openings that serve as entrances or exits.',
                'memory_tip': 'OSTIUM sounds like "OS-TEE-UM" - think of "OS" (mouth) - an ostium is a mouth-like opening in the body.',
                'example_sentence': 'The cardiologist carefully examined the coronary _____ during the angiogram to check for blockages.'
            },
            'ostracism': {
                'definition': 'The practice of excluding someone from a society or group; social rejection or banishment. In ancient Athens, ostracism was a political procedure where citizens could vote to exile a prominent politician for ten years without trial. In modern contexts, ostracism refers to social exclusion, shunning, or deliberately ignoring someone as punishment or rejection. The practice can occur in various settings from schools and workplaces to entire communities. Psychological research shows that ostracism can have severe emotional and mental health effects on those excluded.',
                'pronunciation': '/ˈɑstrəˌsɪzəm/',
                'pronunciation_ipa': '/ˈɑstrəˌsɪzəm/',
                'etymology': 'From Greek "ostrakismos" from "ostrakon" meaning pottery shard. In Athens, citizens wrote names on broken pottery pieces to vote for exile.',
                'memory_tip': 'OSTRACISM comes from broken pottery (ostrakon) used for voting. Think "OSTRA-CAST-OUT" - casting someone out through community rejection.',
                'example_sentence': 'The whistleblower faced _____ from colleagues who disagreed with his decision to report the company\'s illegal activities.'
            },
            'ostriches': {
                'definition': 'Large, flightless birds native to Africa, the world\'s largest living bird species. Ostriches can reach heights of up to 9 feet and weights of over 300 pounds. Despite being unable to fly, they are exceptional runners, capable of reaching speeds up to 45 mph. They have distinctive long necks, powerful legs, and small heads relative to their body size. Ostriches are omnivores, eating plants, insects, and small animals. They are farmed for their meat, eggs, leather, and feathers. The myth that ostriches bury their heads in sand when frightened is false.',
                'pronunciation': '/ˈɔstrɪtʃəz/',
                'pronunciation_ipa': '/ˈɔstrɪtʃəz/',
                'etymology': 'From Old French "ostruche," from Latin "avis struthio" meaning sparrow-bird (ironically, given their size). The name evolved through various languages.',
                'memory_tip': 'OSTRICHES are "OSTRICH + ES" (plural). Remember they\'re the opposite of sparrows - huge birds that can\'t fly but run very fast.',
                'example_sentence': 'The safari group watched in amazement as a flock of _____ ran across the African savanna at incredible speed.'
            },
            'otacoustic': {
                'definition': 'Relating to or involving sounds produced by the ear itself, particularly referring to otoacoustic emissions - sounds generated by the inner ear as a response to acoustic stimuli or spontaneously. These emissions are used in medical testing to assess inner ear function and hearing health. Otoacoustic emissions can be measured with sensitive microphones placed in the ear canal and are important diagnostic tools for detecting hearing problems, especially in newborns and young children. The phenomenon demonstrates that the ear is not just a passive receiver but an active generator of sound.',
                'pronunciation': '/ˌoʊtəˈkuːstɪk/',
                'pronunciation_ipa': '/ˌoʊtəˈkuːstɪk/',
                'etymology': 'From Greek "oto" meaning ear + "acoustic" from "akoustikos" meaning related to hearing. The term describes ear-generated sounds.',
                'memory_tip': 'OTACOUSTIC = OTO (ear) + ACOUSTIC (sound). Think of ears making their own sounds - otacoustic refers to sounds the ear produces.',
                'example_sentence': 'The audiologist used _____ emission testing to evaluate the infant\'s inner ear function.'
            },
            'others': {
                'definition': 'People or things that are different from or additional to those already mentioned or known; the remaining members of a group. "Others" serves as a pronoun referring to additional individuals or objects not specifically identified. In philosophical and social contexts, "others" can refer to people outside one\'s immediate group or those perceived as different. The concept of "otherness" is important in psychology, sociology, and anthropology for understanding identity, prejudice, and social dynamics. The word emphasizes distinction and separation between known and unknown entities.',
                'pronunciation': '/ˈʌðərz/',
                'pronunciation_ipa': '/ˈʌðərz/',
                'etymology': 'From Old English "othre," the plural of "other," from Germanic roots meaning different or alternative. The word has maintained its basic meaning throughout English history.',
                'memory_tip': 'OTHERS = OTHER + S (plural). Think of "the OTHER people" - others are all the different people besides the ones you\'ve already mentioned.',
                'example_sentence': 'Some students preferred online learning, while _____ found in-person classes more effective.'
            },
            'otiose': {
                'definition': 'Serving no practical purpose; functionally useless; lacking effectiveness or being superfluous. In formal writing, otiose describes things that are redundant, idle, or without productive value. The term can apply to arguments, actions, objects, or people that contribute nothing meaningful to a situation. In legal contexts, otiose clauses are provisions that have no legal effect. The word carries a tone of criticism, suggesting that something should be eliminated or reformed because it serves no useful function.',
                'pronunciation': '/ˈoʊʃiˌoʊs/',
                'pronunciation_ipa': '/ˈoʊʃiˌoʊs/',
                'etymology': 'From Latin "otiosus" meaning at leisure, idle, or unemployed, from "otium" meaning leisure or free time. The word evolved to mean useless rather than simply leisurely.',
                'memory_tip': 'OTIOSE sounds like "OH-SHE-OSE" (oh, she owes). Think "oh, she owes nothing useful" - otiose means serving no useful purpose.',
                'example_sentence': 'The committee decided the lengthy approval process had become _____ and voted to streamline it significantly.'
            },
            'ottoman': {
                'definition': 'A low upholstered seat or footstool without arms or back, typically used for resting feet or as extra seating. Ottomans can be round, square, or rectangular and often include storage space inside. The furniture piece originated from the Ottoman Empire, where low, cushioned seating was common. Modern ottomans serve multiple functions in interior design, providing comfort, storage, and flexibility in room arrangements. They can complement sofas and chairs or stand alone as decorative and functional elements. Some ottomans are designed to match specific furniture sets.',
                'pronunciation': '/ˈɑtəmən/',
                'pronunciation_ipa': '/ˈɑtəmən/',
                'etymology': 'Named after the Ottoman Empire, where this style of low, cushioned seating was traditional. The furniture reflects the empire\'s seating customs and design preferences.',
                'memory_tip': 'OTTOMAN furniture comes from the OTTOMAN Empire. Think of Turkish-style low seating - ottomans are low, cushioned furniture pieces.',
                'example_sentence': 'She placed her feet on the velvet _____ while reading her book in the comfortable armchair.'
            },
            'ouagadougou': {
                'definition': 'The capital and largest city of Burkina Faso, located in the central part of West Africa. Ouagadougou serves as the country\'s political, economic, and cultural center, with a population of over two million people. The city is known for its vibrant arts scene, including the biennial FESPACO film festival, one of Africa\'s most important cinema events. It features a mix of traditional African architecture and modern buildings. The city faces challenges common to rapidly growing African urban centers, including infrastructure development and poverty, but remains a crucial hub for the Sahel region.',
                'pronunciation': '/ˌwɑɡəˈduɡu/',
                'pronunciation_ipa': '/ˌwɑɡəˈduɡu/',
                'etymology': 'From the Mooré language, possibly meaning "where people get honor and respect" or related to the historical ruling dynasty. The name reflects local linguistic and cultural traditions.',
                'memory_tip': 'OUAGADOUGOU sounds like "WAH-GA-DOO-GOO" - think of it as the "wahoo" city of Burkina Faso, known for its film festival celebrations.',
                'example_sentence': 'The international film festival in _____ attracts directors and cinema enthusiasts from across Africa and beyond.'
            },
            'oubliette': {
                'definition': 'A secret dungeon with an opening only at the top, used for imprisoning people who were then forgotten. Oubliettes were typically found in medieval castles and fortifications, designed to hold prisoners in solitary confinement with minimal chance of escape or rescue. The word comes from the French verb "oublier" meaning "to forget," reflecting the intention that prisoners would be forgotten and left to die. These dungeons represent some of the most brutal aspects of medieval justice and punishment. Today, the term is sometimes used metaphorically for any place of confinement or neglect.',
                'pronunciation': '/ˌublɪˈɛt/',
                'pronunciation_ipa': '/ˌublɪˈɛt/',
                'etymology': 'From French "oubliette," from "oublier" meaning to forget. The name literally means "little place of forgetting," emphasizing the fate of prisoners.',
                'memory_tip': 'OUBLIETTE comes from "OUBLIER" (to forget). Think "OH-BLEE-ETTE" - a place where prisoners were forgotten, dropped through the top and left.',
                'example_sentence': 'The castle tour guide pointed out the narrow opening that led to the medieval _____, a grim reminder of harsh justice.'
            },
            'ounce': {
                'definition': 'A unit of weight equal to one-sixteenth of a pound in the avoirdupois system (approximately 28.35 grams) or one-twelfth of a pound in the troy system (approximately 31.1 grams). The ounce is commonly used for measuring small quantities of food, precious metals, and other materials. In cooking, fluid ounces measure volume, while weight ounces measure mass. The ounce has historical significance in trade and commerce, particularly for valuable commodities like gold and silver. The term is also used in the phrase "an ounce of prevention is worth a pound of cure," emphasizing the value of preventive measures.',
                'pronunciation': '/aʊns/',
                'pronunciation_ipa': '/aʊns/',
                'etymology': 'From Latin "uncia" meaning one-twelfth (originally of a Roman pound), through Old French "unce." The word reflects ancient systems of measurement and trade.',
                'memory_tip': 'OUNCE sounds like "OWNS" - think of what you own in small amounts, like an ounce of gold or an ounce of prevention.',
                'example_sentence': 'The recipe called for exactly one _____ of vanilla extract to achieve the perfect flavor balance.'
            },
            'ourselves': {
                'definition': 'The reflexive or emphatic form of "we" and "us," used when the subject and object of a sentence refer to the same group of people that includes the speaker. "Ourselves" emphasizes that the action is performed by and affects the same group. It can also be used for emphasis, meaning "we personally" or "we alone." The word is essential for indicating self-directed actions or distinguishing between what "we" do versus what others do. In philosophical contexts, it can refer to our essential nature or identity as a group.',
                'pronunciation': '/ɑrˈsɛlvz/',
                'pronunciation_ipa': '/ɑrˈsɛlvz/',
                'etymology': 'Compound of "our" + "selves," following the pattern of other reflexive pronouns. "Self" comes from Old English, originally meaning one\'s own person.',
                'memory_tip': 'OURSELVES = OUR + SELVES. Think "we did it to OUR own SELVES" - it refers back to the same group of people speaking.',
                'example_sentence': 'We need to challenge _____ to think more creatively about solving this complex problem.'
            },
            'ouster': {
                'definition': 'The act of removing someone from a position of power or authority; forcible ejection or displacement. In legal contexts, ouster refers to wrongfully depriving someone of their legal rights to property or position. In business and politics, ouster describes the process of forcing executives, leaders, or officials from their roles, often through votes of no confidence, impeachment, or board decisions. The term implies forcible removal rather than voluntary resignation. Ousters often occur during crises, scandals, or when performance is deemed inadequate by those with authority to make such decisions.',
                'pronunciation': '/ˈaʊstər/',
                'pronunciation_ipa': '/ˈaʊstər/',
                'etymology': 'From "oust" (from Anglo-French "ouster," meaning to take away or remove) plus the suffix "-er" indicating action or result. Related to the legal concept of dispossession.',
                'memory_tip': 'OUSTER sounds like "OUT-STER" - think of forcing someone OUT of their position, making them an "out-ster" instead of an "in-ster."',
                'example_sentence': 'The board of directors voted for the CEO\'s _____ following the company\'s poor financial performance.'
            },
            'outcome': {
                'definition': 'The result or consequence of an action, process, or event; the final product or end state of a situation. Outcomes can be positive, negative, or neutral, and may be intended or unintended. In research and evaluation, outcomes are measured to assess the effectiveness of interventions, programs, or policies. In medicine, patient outcomes determine the success of treatments. In education, learning outcomes define what students should achieve. The concept of outcome is fundamental to planning, decision-making, and evaluation across virtually all fields of human activity.',
                'pronunciation': '/ˈaʊtˌkʌm/',
                'pronunciation_ipa': '/ˈaʊtˌkʌm/',
                'etymology': 'Compound of "out" + "come," literally meaning what comes out or results from something. The word follows the pattern of other result-oriented compound words.',
                'memory_tip': 'OUTCOME = OUT + COME. Think of what COMES OUT of a situation - the outcome is the result that comes out of actions or events.',
                'example_sentence': 'The _____ of the negotiations exceeded everyone\'s expectations, resulting in a comprehensive peace agreement.'
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

def process_batch_124():
    processor = Batch124Processor()
    
    input_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_124_words.csv'
    output_file = r'C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_124_processed.csv'
    
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
    
    logging.info(f"Batch 124 processing complete. Processed {successful_count}/50 words.")
    logging.info(f"Output saved to: {output_file}")
    
    if combined_words:
        logging.warning(f"Combined word errors detected: {combined_words}")
    
    return successful_count

if __name__ == "__main__":
    process_batch_124()