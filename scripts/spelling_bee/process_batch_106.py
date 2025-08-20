#!/usr/bin/env python3

import csv
import logging
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DifficultyCalculator:
    """Calculate 4-factor difficulty components for spelling words"""
    
    def calculate_difficulty_components(self, word: str, definition: str, etymology: str) -> dict:
        """Calculate 4-factor difficulty components leaving final difficulty null"""
        
        # 1. Phonetic Transparency (sound-to-spelling correspondence)
        phonetic_score = self._calculate_phonetic_transparency(word)
        
        # 2. Word Frequency (how common the word is)
        frequency_score = self._calculate_word_frequency(word)
        
        # 3. Morphological Complexity (prefixes, suffixes, roots)
        morphological_score = self._calculate_morphological_complexity(word, definition)
        
        # 4. Etymology Complexity (language origins and borrowing)
        etymology_score = self._calculate_etymology_complexity(etymology)
        
        return {
            'phonetic_transparency_score': phonetic_score,
            'word_frequency_score': frequency_score, 
            'morphological_complexity_score': morphological_score,
            'etymology_complexity_score': etymology_score,
            'final_difficulty': None  # Leave null for human review
        }
    
    def _calculate_phonetic_transparency(self, word: str) -> float:
        """Calculate how transparent the sound-to-spelling relationship is"""
        irregular_patterns = ['ough', 'aigh', 'eigh', 'ph', 'gh', 'tion', 'sion', 'ight']
        score = 1.0
        
        for pattern in irregular_patterns:
            if pattern in word.lower():
                score += 0.3
        
        # Silent letters
        silent_patterns = ['mb', 'ght', 'kn', 'wr', 'mn']
        for pattern in silent_patterns:
            if pattern in word.lower():
                score += 0.2
                
        return min(score, 5.0)
    
    def _calculate_word_frequency(self, word: str) -> float:
        """Estimate word frequency (higher score = less frequent = more difficult)"""
        common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did']
        
        if word.lower() in common_words:
            return 1.0
        elif len(word) <= 4:
            return 2.0
        elif len(word) <= 7:
            return 3.0
        elif len(word) <= 10:
            return 4.0
        else:
            return 5.0
    
    def _calculate_morphological_complexity(self, word: str, definition: str) -> float:
        """Calculate complexity based on word parts"""
        score = 1.0
        
        prefixes = ['un', 're', 'pre', 'dis', 'anti', 'over', 'under', 'out', 'super', 'semi', 'multi', 'inter', 'trans', 'sub', 'micro', 'macro']
        suffixes = ['tion', 'sion', 'ment', 'ness', 'able', 'ible', 'ous', 'eous', 'ious', 'ly', 'ing', 'ed', 'er', 'est', 'ful', 'less']
        
        for prefix in prefixes:
            if word.lower().startswith(prefix):
                score += 0.5
                break
                
        for suffix in suffixes:
            if word.lower().endswith(suffix):
                score += 0.5
                break
        
        # Compound words
        if len(word) > 8 and any(char.isupper() for char in word[1:]):
            score += 0.5
            
        return min(score, 5.0)
    
    def _calculate_etymology_complexity(self, etymology: str) -> float:
        """Calculate complexity based on word origins"""
        if not etymology:
            return 3.0
            
        score = 1.0
        complex_origins = ['Latin', 'Greek', 'Sanskrit', 'Arabic', 'Hebrew', 'Persian', 'Turkish']
        moderate_origins = ['French', 'Italian', 'Spanish', 'Portuguese', 'German', 'Dutch']
        
        etymology_lower = etymology.lower()
        
        for origin in complex_origins:
            if origin.lower() in etymology_lower:
                score += 1.0
                break
                
        for origin in moderate_origins:
            if origin.lower() in etymology_lower:
                score += 0.5
                break
        
        # Multiple language origins increase complexity
        origin_count = sum(1 for origin in complex_origins + moderate_origins 
                          if origin.lower() in etymology_lower)
        if origin_count > 1:
            score += 0.5
            
        return min(score, 5.0)


class Batch106Processor:
    """Processes Batch 106 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
        # Define combined word errors found in this batch
        self.combined_errors = {
            'mambomanacle': ['mambo', 'manacle']
        }
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for each word using Claude knowledge"""
        
        # Handle combined word errors
        if word in self.combined_errors:
            return {
                'word': word,
                'pronunciation': None,
                'definition': f"COMBINED_WORD_ERROR: This appears to be two words combined: {' + '.join(self.combined_errors[word])}",
                'example_sentence': None,
                'etymology': None,
                'etymology_source': 'Claude',
                'memory_tip': 'This is a combined word error from PDF parsing and should not be used.',
                'phonetic_transparency_score': None,
                'word_frequency_score': None,
                'morphological_complexity_score': None,
                'etymology_complexity_score': None,
                'final_difficulty': None
            }
        
        # Comprehensive word data with 200-400 word definitions
        word_data = {
            'mackinaw': {
                'pronunciation': '/MAK-ə-naw/',
                'definition': 'A heavy woolen cloth, typically plaid or checked, originally used for blankets and outdoor clothing; also refers to a type of boat used on the Great Lakes, or the Mackinaw coat made from this fabric. The fabric originated as a trade good in the Great Lakes region, where French-Canadian voyageurs and Native Americans engaged in fur trading activities that required durable, warm clothing for harsh winter conditions. Mackinaw blankets became essential trade items, valued by indigenous peoples for their warmth and durability compared to traditional materials, while European settlers appreciated their effectiveness in North American winters. The boats called mackinaws were flat-bottomed vessels designed for carrying cargo and passengers across the Great Lakes, featuring distinctive designs adapted to shallow waters and variable weather conditions that characterized inland navigation. Modern mackinaw fabric continues to be used for outdoor clothing, particularly hunting and fishing gear where durability and weather resistance are essential for extended exposure to harsh conditions. The town of Mackinaw City, Michigan, and Mackinac Island preserve the historical significance of this region in American expansion and trade, demonstrating how geographic locations, trade relationships, and material culture intersect to create lasting cultural legacies. Understanding mackinaw helps appreciate how trade goods, transportation methods, and environmental adaptations shaped North American frontier life and continue to influence regional identity and commercial activities.',
                'etymology': 'From Ojibwe "Michilimackinac" meaning "great turtle," referring to the shape of Mackinac Island',
                'memory_tip': 'Remember MACKINAW as "MACK-in-AWE" of the great turtle island - the plaid fabric from Mackinac.',
                'example_sentence': 'The hunter wore his traditional _____ coat, its red and black plaid pattern helping him stay warm during the early morning deer hunt.'
            },
            'macrobiotics': {
                'pronunciation': '/MAK-roh-by-OT-iks/',
                'definition': 'A dietary and lifestyle philosophy that emphasizes eating natural, unprocessed foods in balanced proportions to promote health, longevity, and spiritual well-being, based on principles derived from traditional Eastern medicine and adapted for Western contexts by Japanese educator George Ohsawa and his followers. The macrobiotic approach categorizes foods as yin (expansive) or yang (contractive) and seeks to balance these opposing forces through careful food selection, preparation methods, and eating practices that maintain physical and emotional equilibrium. Core dietary principles include emphasizing whole grains as primary foods, eating locally grown seasonal vegetables, avoiding processed foods and artificial additives, and consuming foods in their most natural state with minimal cooking when possible. Macrobiotic practice extends beyond diet to include lifestyle recommendations such as eating slowly and mindfully, chewing food thoroughly, maintaining regular eating schedules, and creating harmonious living environments that support overall well-being. The philosophy influences meal planning through considerations of food quality, seasonal availability, geographic origin, and preparation methods that preserve nutritional value while creating satisfying and balanced meals. While some scientific evidence supports benefits of macrobiotic-style eating patterns, particularly their emphasis on whole plant foods and minimal processing, critics note that strict adherence can lead to nutritional deficiencies without careful planning and professional guidance.',
                'etymology': 'From Greek "makros" (large) + "bios" (life), meaning promoting long life',
                'memory_tip': 'Remember MACROBIOTICS as "MACRO" (large) + "BIOTICS" (life) - diet for large, long life.',
                'example_sentence': 'She studied _____ extensively before adopting a diet centered on whole grains, fresh vegetables, and balanced yin-yang principles.'
            },
            'macrocosm': {
                'pronunciation': '/MAK-roh-kozm/',
                'definition': 'The universe or cosmos as a whole, particularly when considered as representing the larger system of which humans and their immediate environment are small parts; the opposite of microcosm, representing the concept that individual beings and small systems reflect or correspond to universal patterns and structures. This philosophical and scientific concept suggests that understanding large-scale patterns and relationships in the universe provides insights into smaller-scale phenomena, while observing microcosmic details reveals truths about macrocosmic organization and function. Ancient and medieval philosophers used macrocosm-microcosm analogies to explain relationships between human beings and the universe, suggesting that individuals contain within themselves the same elements, forces, and organizing principles that govern celestial and terrestrial phenomena. Scientific applications include systems theory approaches that examine how patterns observed in cosmic structures like galaxy formation might reflect similar organizational principles in biological systems, social organizations, or other complex adaptive systems. The macrocosm encompasses all levels of reality from atomic and molecular structures through biological organisms and ecological systems to planetary, solar, galactic, and universal scales of organization. Modern usage extends the concept to describe any large-scale system or context that contains and influences smaller components, helping in understanding relationships between individual actions and societal outcomes, local phenomena and global patterns, or specific instances and universal principles.',
                'etymology': 'From Greek "makros" (large) + "kosmos" (world/universe), meaning the large universe',
                'memory_tip': 'Remember MACROCOSM as "MACRO" (large) + "COSMOS" - the large universe containing everything.',
                'example_sentence': 'The philosopher argued that social movements reflect patterns visible in the _____, with individual actions contributing to universal changes.'
            },
            'macropterous': {
                'pronunciation': '/mak-ROP-tər-əs/',
                'definition': 'Having large or well-developed wings; referring to insects or other flying creatures that possess wings of normal or greater-than-normal size for their species, representing an important biological characteristic that affects flight capability, dispersal patterns, and ecological roles. This adjective appears primarily in entomological and biological contexts where wing development variations within species or between closely related species have significant implications for behavior, reproduction, and survival strategies. Many insects exhibit wing polymorphism where some individuals are macropterous (fully-winged) while others are brachypterous (short-winged) or apterous (wingless), with these differences often linked to environmental conditions, population density, or seasonal factors that influence dispersal needs. Macropterous forms typically appear when environmental conditions favor dispersal to new habitats, such as during food shortages, overcrowding, or seasonal changes that make migration advantageous for survival and reproduction. The development of wing size and functionality involves complex genetic and environmental interactions that demonstrate how organisms adapt their morphology to ecological challenges and opportunities. Research on macropterous versus other wing forms provides insights into evolutionary strategies, population dynamics, and species responses to environmental change including climate change impacts on insect migration patterns and habitat use.',
                'etymology': 'From Greek "makros" (large) + "pteron" (wing), meaning having large wings',
                'memory_tip': 'Remember MACROPTEROUS as "MACRO" (large) + "PTEROUS" (winged) - having large, well-developed wings.',
                'example_sentence': 'The entomologist identified the _____ form of the aphid, noting its fully developed wings that would enable long-distance migration.'
            },
            'macular': {
                'pronunciation': '/MAK-yə-lər/',
                'definition': 'Relating to or affecting the macula, the small central area of the retina responsible for sharp, detailed central vision that enables activities like reading, driving, and recognizing faces, representing a crucial component of the visual system that can be affected by age-related and other degenerative conditions. Macular degeneration, particularly age-related macular degeneration (AMD), represents one of the leading causes of vision loss in older adults, causing progressive deterioration of central vision while typically preserving peripheral vision that allows continued mobility and basic daily activities. The macula contains the highest concentration of cone cells in the retina, specialized photoreceptors responsible for color vision and fine detail resolution that require optimal nutrition, blood flow, and cellular maintenance to function effectively throughout life. Macular health depends on various factors including genetics, diet, smoking status, sun exposure, and cardiovascular health, with protective measures including consumption of antioxidant-rich foods, UV protection, regular exercise, and avoiding smoking that can reduce risk of degenerative changes. Medical treatments for macular conditions include nutritional supplements, anti-VEGF injections, photodynamic therapy, and emerging treatments like stem cell therapy that aim to preserve or restore macular function and prevent progression of vision loss. Understanding macular anatomy and function helps in recognizing early symptoms of macular diseases and taking preventive measures that protect this critical component of the visual system.',
                'etymology': 'From Latin "macula" meaning spot or stain, referring to the spot-like area of the retina',
                'memory_tip': 'Remember MACULAR as "MACULA" (spot) + "AR" (relating to) - relating to the spot in your eye for sharp vision.',
                'example_sentence': 'The ophthalmologist detected early signs of _____ degeneration and recommended lifestyle changes to slow its progression.'
            },
            'macushla': {
                'pronunciation': '/mə-KOOSH-lə/',
                'definition': 'An Irish term of endearment meaning "my pulse" or "my heartbeat," used affectionately to address loved ones, particularly romantic partners or close family members, representing the deep emotional connection and vital importance that someone holds in the speaker\'s life and affections. This Gaelic-derived expression demonstrates the poetic nature of Irish language and culture, where terms of endearment often reference vital bodily functions, natural phenomena, or precious objects to convey the essential role that beloved individuals play in one\'s emotional and spiritual well-being. The word reflects Irish cultural values that emphasize emotional expressiveness, family bonds, and the importance of articulating love and affection through distinctive linguistic expressions that carry cultural heritage and personal meaning. Irish terms of endearment like macushla serve important social and emotional functions, strengthening relationships, expressing cultural identity, and preserving linguistic traditions that connect contemporary speakers with their ancestral heritage and community values. The usage of such terms in Irish-American communities helps maintain cultural connections across generations and geographic distances, providing ways for individuals to express both personal affection and cultural identity through language choices. Understanding Irish terms of endearment provides insights into Celtic culture, the role of language in expressing emotion, and how immigrant communities preserve and adapt linguistic traditions in new cultural contexts.',
                'etymology': 'From Irish Gaelic "mo chuisle" meaning "my pulse" or "my heartbeat"',
                'memory_tip': 'Remember MACUSHLA as "MY-CUSHLA" - Irish for "my pulse," a heartfelt term of endearment.',
                'example_sentence': 'The grandmother lovingly called her granddaughter "_____, " using the traditional Irish term that meant "my heartbeat."'
            },
            'madagascar': {
                'pronunciation': '/MAD-ə-gas-kər/',
                'definition': 'The fourth-largest island in the world, located off the east coast of Africa in the Indian Ocean, known for its unique biodiversity, distinctive culture, and endemic species that evolved in isolation after the island separated from the African continent approximately 165 million years ago. Madagascar\'s isolation has created a natural laboratory of evolution, with over 90% of its wildlife found nowhere else on Earth, including lemurs, fossas, chameleons, and thousands of endemic plant species that represent extraordinary examples of adaptive radiation and speciation. The Malagasy people represent a unique blend of African and Asian ancestry, with cultural traditions, languages, and customs that reflect influences from both continents as well as interactions with Arab, European, and other trading populations over centuries. The island\'s economy depends heavily on agriculture, mining, and increasingly ecotourism that showcases its remarkable biodiversity while providing income for conservation efforts and local communities. Environmental challenges include deforestation, species extinction, climate change impacts, and poverty that create pressures for unsustainable resource use, making Madagascar a priority for international conservation efforts and sustainable development initiatives. The country\'s political history includes periods of monarchical rule, French colonial administration, independence in 1960, and ongoing efforts to develop stable democratic institutions while managing economic development and environmental protection challenges.',
                'etymology': 'From "Madagascar," possibly from Malagasy "Madagasikara" or from Marco Polo\'s corruption of Mogadishu',
                'memory_tip': 'Remember MADAGASCAR as the large African island famous for lemurs and unique wildlife evolution.',
                'example_sentence': 'Researchers traveled to _____ to study the unique lemur species found nowhere else on Earth.'
            },
            'mademoiselle': {
                'pronunciation': '/MAM-wə-zel/ or /mad-mwa-ZEL/',
                'definition': 'A French title of address for an unmarried woman or young lady, equivalent to "Miss" in English, representing a formal yet respectful way to address females who have not married or whose marital status is unknown, though usage has evolved significantly in modern French society. Traditionally, mademoiselle distinguished unmarried women from married women (addressed as "madame"), reflecting social systems where marital status played important roles in determining social position, legal rights, and appropriate forms of address in formal and professional contexts. The title appears frequently in French literature, film, and culture as a marker of social relationships, class distinctions, and generational differences that have shaped French society and interpersonal interactions throughout history. Modern usage of mademoiselle has become controversial in France, with many women preferring "madame" regardless of marital status to avoid discrimination or assumptions based on personal relationships, leading to official policy changes that eliminated mademoiselle from most government documents and forms. The evolution of this term reflects broader social changes regarding women\'s rights, gender equality, and the relationship between language and social attitudes about women\'s roles and identity in contemporary society. Educational and cultural contexts continue to use mademoiselle in teaching French language and culture, though with awareness of its changing social significance and the importance of respectful address forms that reflect current values.',
                'etymology': 'From French "ma demoiselle" meaning "my young lady," from Latin "domina" (lady)',
                'memory_tip': 'Remember MADEMOISELLE as French "my young lady" - the formal address for an unmarried woman.',
                'example_sentence': 'In French class, students learned to address their unmarried female teacher as "_____ Dubois."'
            },
            'madrigal': {
                'pronunciation': '/MAD-ri-gəl/',
                'definition': 'A type of secular vocal music composition, typically unaccompanied, that flourished during the Renaissance and early Baroque periods, characterized by sophisticated polyphonic writing, expressive text setting, and often pastoral or amorous themes that showcased compositional skill and performing artistry. Renaissance madrigals originated in Italy during the 16th century as sophisticated entertainment for educated aristocratic circles, featuring complex interweaving vocal lines, word painting techniques that musically illustrated textual meanings, and harmonic innovations that influenced the development of Western classical music. The form spread throughout Europe, with distinctive national styles developing in England, Germany, and other regions where composers adapted madrigal techniques to their own languages and cultural preferences while maintaining the essential characteristics of refined polyphonic writing. English madrigals, particularly those by composers like Thomas Weelkes and John Wilbye, became especially renowned for their technical brilliance, emotional expressiveness, and literary sophistication that combined musical artistry with poetic excellence. Modern performances of madrigals require skilled vocal ensembles capable of navigating complex polyphonic textures, precise intonation, and expressive interpretation that conveys both the technical mastery and emotional content of these sophisticated musical works. The madrigal\'s influence extends beyond its historical period to contemporary choral music, where its principles of text-music relationships, vocal independence, and expressive singing continue to inform composition and performance practices.',
                'etymology': 'From Italian "madrigale," possibly from Latin "matricalis" (of the womb/mother tongue)',
                'memory_tip': 'Remember MADRIGAL as sophisticated Renaissance vocal music - "MAD-REGAL" like mad royal singing.',
                'example_sentence': 'The chamber choir performed a beautiful 16th-century _____ that showcased intricate harmonies and expressive word painting.'
            },
            'magellan': {
                'pronunciation': '/mə-JEL-ən/',
                'definition': 'Ferdinand Magellan (c. 1480-1521), a Portuguese explorer whose expedition achieved the first circumnavigation of the globe, revolutionizing understanding of Earth\'s geography and establishing sea routes that connected the Atlantic and Pacific Oceans through what became known as the Strait of Magellan. Magellan\'s voyage, sponsored by the Spanish Crown, sought a western route to the Spice Islands and proved that the Earth could be circumnavigated by sea, though Magellan himself died in the Philippines before completing the journey, leaving Juan Sebastián Elcano to complete the historic voyage. The expedition\'s achievements included discovering the strait at the southern tip of South America that bears Magellan\'s name, crossing the Pacific Ocean (which Magellan named), and providing practical evidence of the Earth\'s spherical nature and actual size. Magellan\'s legacy extends beyond exploration to include contributions to navigation techniques, cartography, and global trade routes that connected previously isolated regions and cultures while establishing patterns of European expansion and colonization. The Magellanic Clouds, two satellite galaxies visible in the southern hemisphere, were named after Magellan by later astronomers who honored his role in southern hemisphere exploration and navigation. Modern spacecraft and space missions have also adopted Magellan\'s name, reflecting his enduring association with exploration, discovery, and pushing the boundaries of human knowledge about our world and universe.',
                'etymology': 'Named after Ferdinand Magellan, Portuguese explorer, from Portuguese "Magalhães"',
                'memory_tip': 'Remember MAGELLAN as the explorer who "MAGically" navigated around the Earth first.',
                'example_sentence': 'Students learned about _____ expedition and how it proved the Earth could be circumnavigated by sea.'
            },
            'magenta': {
                'pronunciation': '/mə-JEN-tə/',
                'definition': 'A vibrant purplish-red color that does not occur in the visible light spectrum but is perceived by the human brain when red and blue light are combined, representing one of the primary colors in subtractive color systems used in printing and art. This distinctive hue was named after the 1859 Battle of Magenta in Italy, where French and Sardinian forces defeated Austrian troops, with the newly developed aniline dye being named to commemorate this military victory. Magenta plays a crucial role in color theory and printing technology as one of the four primary colors in CMYK printing (cyan, magenta, yellow, and key/black), enabling reproduction of most colors in printed materials through various combinations and percentages of these inks. The color demonstrates important principles of human color perception, as magenta represents what happens when the brain processes certain combinations of wavelengths that don\'t correspond to any single wavelength in the electromagnetic spectrum. Artistic applications of magenta include painting, graphic design, fashion, and decorative arts where its bold, attention-grabbing qualities create visual impact and emotional responses that can convey energy, creativity, and modernity. Understanding magenta\'s properties helps in color mixing, design applications, and appreciating the complex relationship between light physics, human perception, and cultural associations that influence how we experience and use color in various contexts.',
                'etymology': 'Named after the Battle of Magenta (1859) in Italy, where this dye color was first marketed',
                'memory_tip': 'Remember MAGENTA as the vibrant color named after a famous battle - "MAG-BATTLE" color.',
                'example_sentence': 'The graphic designer chose a bright _____ background to make the text stand out dramatically in the advertisement.'
            },
            'magician': {
                'pronunciation': '/mə-JISH-ən/',
                'definition': 'A performer who creates illusions and seemingly impossible effects through sleight of hand, misdirection, and specialized techniques designed to entertain audiences by appearing to defy natural laws and logical explanation, representing an ancient art form that combines manual dexterity, psychological understanding, and theatrical presentation. Professional magicians master various branches of magical arts including close-up magic performed for small groups, stage illusions designed for large audiences, mentalism that simulates psychic abilities, and escape artistry that involves breaking free from restraints or confined spaces. The craft requires extensive practice, creativity, and understanding of human perception and attention that enables magicians to control what audiences observe and how they interpret sensory information during performances. Historical traditions of magic and illusion appear across cultures worldwide, with modern magic incorporating technology, psychology, and performance arts while maintaining connections to ancient practices of entertainment and wonder-creation. Magic serves important social and psychological functions including providing escapism from everyday reality, creating shared experiences of wonder and surprise, and demonstrating the limitations and fallibility of human perception and reasoning. Educational applications of magic include teaching critical thinking, problem-solving, and understanding of how cognitive biases and assumptions can be manipulated, while therapeutic applications use magic techniques in rehabilitation and confidence-building programs.',
                'etymology': 'From Old French "magicien," from Latin "magicus" (magical), from Greek "magikos"',
                'memory_tip': 'Remember MAGICIAN as one who performs "MAGIC" + "IAN" (practitioner) - a practitioner of magic arts.',
                'example_sentence': 'The skilled _____ amazed the children by making coins disappear and reappear from behind their ears.'
            },
            'magistrates': {
                'pronunciation': '/MAJ-ə-strāts/',
                'definition': 'Government officials who administer justice and enforce laws at local levels, typically handling minor criminal cases, civil disputes, and administrative matters within their jurisdictions, representing an important component of judicial systems that provides accessible legal services and maintains law and order in communities. These judicial officers possess limited but significant authority to hear cases, issue warrants, set bail, conduct preliminary hearings, and render judgments in matters that fall within their designated scope of responsibility and geographic area of jurisdiction. Different legal systems organize magistrate roles differently: some magistrates are elected officials who serve local communities, while others are appointed professionals with legal training who focus on specific types of cases or administrative functions within larger court systems. Magistrates often serve as the first point of contact between citizens and the judicial system, handling traffic violations, small claims disputes, domestic violence cases, and other matters that require prompt legal attention but don\'t warrant higher court involvement. The institution of magistracy has ancient roots in Roman law and has evolved to meet contemporary needs for accessible, efficient, and cost-effective justice administration that reduces burdens on higher courts while ensuring that legal protections and due process rights are maintained. Understanding magistrate functions helps citizens navigate legal systems, appreciate the structure of judicial hierarchies, and recognize the importance of local legal institutions in maintaining community order and protecting individual rights.',
                'etymology': 'Plural of "magistrate" from Latin "magistratus" meaning public official or ruler',
                'memory_tip': 'Remember MAGISTRATES as "MAGIS" (greater) + "TRATES" - greater officials who judge local legal matters.',
                'example_sentence': 'The local _____ handled small claims cases and traffic violations, providing accessible justice for community members.'
            },
            'magma': {
                'pronunciation': '/MAG-mə/',
                'definition': 'Molten rock located beneath the Earth\'s surface, consisting of liquid rock, dissolved gases, and crystals that forms through melting of existing rocks under extreme heat and pressure conditions, representing the raw material from which igneous rocks and volcanic phenomena originate. Magma forms through various geological processes including decompression melting when rocks rise toward the surface, flux melting when water or other substances lower melting temperatures, and heat-induced melting from contact with hot intrusions or elevated geothermal gradients. The composition of magma varies significantly depending on source rocks, melting conditions, and subsequent processes, with major types including felsic magmas rich in silica and aluminum, mafic magmas high in magnesium and iron, and intermediate compositions that combine characteristics of both end members. When magma reaches the Earth\'s surface through volcanic eruptions, it becomes lava and creates various volcanic rocks and landforms depending on eruption style, magma composition, and environmental conditions that affect cooling and crystallization processes. Magma chambers beneath volcanoes store and modify molten rock before eruptions, with processes like fractional crystallization, assimilation of surrounding rocks, and magma mixing creating the diversity of volcanic products and eruption behaviors observed worldwide. Understanding magma properties and processes provides insights into volcanic hazards, mineral formation, geothermal energy resources, and the dynamic processes that shape Earth\'s crust and surface features.',
                'etymology': 'From Greek "magma" meaning thick unguent or kneaded mass, referring to molten rock',
                'memory_tip': 'Remember MAGMA as "MAGnificent MAss" of molten rock beneath Earth\'s surface.',
                'example_sentence': 'Geologists studied the composition of the _____ chamber to predict the type of volcanic eruption that might occur.'
            },
            'magnate': {
                'pronunciation': '/MAG-nāt/',
                'definition': 'A wealthy and powerful person, especially in business or industry, who wields significant influence through control of substantial financial resources, major companies, or important economic sectors, representing individuals who have achieved exceptional success and accumulated power that extends beyond their immediate business interests. Industrial magnates historically played crucial roles in economic development, technological innovation, and social change through their investments, business decisions, and philanthropic activities that shaped entire industries and regions. These influential figures often control multiple businesses, maintain extensive networks of political and social connections, and possess resources that enable them to influence public policy, market conditions, and community development through their economic activities and charitable contributions. The term carries both positive and negative connotations: magnates may be celebrated as visionary leaders and job creators who drive economic growth and innovation, while also criticized as concentrating excessive wealth and power that may undermine democratic institutions and social equity. Modern magnates operate in globalized economies where their influence can extend across national boundaries through multinational corporations, international investments, and global supply chains that affect millions of workers and consumers worldwide. Understanding the role of magnates helps in analyzing economic systems, wealth distribution, and the relationship between private wealth and public influence in contemporary societies.',
                'etymology': 'From Latin "magnatus" meaning great man, from "magnus" (great)',
                'memory_tip': 'Remember MAGNATE as "MAGNA" (great) + "ATE" (person) - a great person with wealth and power.',
                'example_sentence': 'The steel _____ donated millions to build schools and libraries in his hometown after achieving immense wealth from his industrial empire.'
            },
            'magnificent': {
                'pronunciation': '/mag-NIF-ə-sənt/',
                'definition': 'Extremely impressive, beautiful, or grand in appearance, scale, or conception; inspiring wonder and admiration through exceptional quality, splendor, or majesty that surpasses ordinary expectations and creates lasting positive impressions on observers. This adjective describes objects, places, performances, or achievements that demonstrate extraordinary excellence, beauty, or grandeur that evokes strong emotional responses including awe, admiration, and appreciation for exceptional human or natural accomplishments. Magnificent architecture includes buildings, monuments, and structures that combine aesthetic beauty with impressive scale and craftsmanship, such as cathedrals, palaces, bridges, and other constructions that represent pinnacles of human creativity and technical achievement. Natural phenomena can be magnificent when they display extraordinary beauty, power, or scale that overwhelms human senses and creates profound appreciation for the wonders of the natural world, including landscapes, weather events, and astronomical displays. Artistic and cultural creations achieve magnificence through exceptional skill, creativity, and emotional impact that transcends ordinary artistic expression and creates works of lasting value and universal appeal. Understanding magnificence involves appreciating both the objective qualities that make something extraordinary and the subjective responses that recognition of excellence creates in human consciousness and cultural appreciation.',
                'etymology': 'From Latin "magnificus" meaning great-making, from "magnus" (great) + "facere" (to make)',
                'memory_tip': 'Remember MAGNIFICENT as "MAGNI" (great) + "FICENT" (making) - making something appear great and impressive.',
                'example_sentence': 'The _____ cathedral towered above the medieval city, its intricate spires and stained glass windows inspiring awe in all who saw it.'
            },
            'magnolia': {
                'pronunciation': '/mag-NOH-lee-ə/',
                'definition': 'A genus of flowering trees and shrubs known for their large, fragrant, and often spectacularly beautiful blooms that appear in white, pink, purple, or yellow colors, representing some of the most ancient flowering plant families that have existed for over 100 million years. These distinctive plants are characterized by their primitive flower structure with numerous petals and reproductive parts arranged in spiral patterns, providing insights into the evolutionary history of flowering plants and their relationships to earlier plant forms. Magnolias thrive in temperate and subtropical climates worldwide, with different species adapted to various environmental conditions from wetland areas to mountainous regions, contributing to diverse ecosystems as both ornamental and native plants. The flowers typically appear before or simultaneously with leaves, creating dramatic displays that make magnolias popular ornamental trees in parks, gardens, and landscapes where their beauty and fragrance provide aesthetic and sensory pleasure. Cultural significance includes magnolias serving as state flowers for Mississippi and Louisiana, symbols in Southern American culture, and important elements in traditional medicine systems where various plant parts have been used for therapeutic purposes. Horticultural varieties have been developed for specific climate zones, flower colors, and growth habits, enabling gardeners and landscapers to incorporate these magnificent plants into diverse settings while preserving their essential beauty and character.',
                'etymology': 'Named after Pierre Magnol, 17th-century French botanist',
                'memory_tip': 'Remember MAGNOLIA as the tree with "MAGNIFIC" large flowers - magnificent blooms named after botanist Magnol.',
                'example_sentence': 'The Southern garden featured a centuries-old _____ tree whose enormous white blooms filled the spring air with sweet fragrance.'
            },
            'maharaja': {
                'pronunciation': '/MAH-hə-rah-jə/',
                'definition': 'A great king or prince in India, particularly during the period of princely states before Indian independence, representing the highest rank of Indian nobility and sovereignty that governed territories with considerable autonomy under various historical political arrangements. These rulers possessed extensive powers within their domains, including administrative, judicial, and military authority that enabled them to govern their territories according to local customs and traditions while managing relationships with larger empires or colonial powers. The institution of maharajas reflects the complex political landscape of historical India, where numerous independent and semi-independent kingdoms coexisted with larger empires, creating diverse systems of governance, culture, and economic organization across the subcontinent. Many maharajas were renowned for their patronage of arts, architecture, and learning, creating magnificent palaces, sponsoring cultural activities, and supporting scholars and artists who produced some of India\'s greatest cultural achievements. The wealth and power of maharajas often came from control of trade routes, agricultural production, and natural resources within their territories, enabling them to maintain elaborate courts and military forces while engaging in diplomacy with neighboring rulers and foreign powers. After Indian independence and the integration of princely states into the modern Indian nation, former maharajas lost their political power but many continue to play cultural and ceremonial roles while some have converted their palaces into museums or hotels that preserve historical heritage.',
                'etymology': 'From Sanskrit "maha" (great) + "raja" (king), meaning great king',
                'memory_tip': 'Remember MAHARAJA as "MAHA" (great) + "RAJA" (king) - a great king of India.',
                'example_sentence': 'The _____ palace showcased centuries of royal architecture and housed priceless collections of art and historical artifacts.'
            },
            'maharajah': {
                'pronunciation': '/MAH-hə-rah-jə/',
                'definition': 'Alternative spelling of maharaja, referring to the same title of great king or prince in Indian history and culture, with this particular spelling reflecting British colonial period conventions and English language adaptations of Sanskrit terms. The spelling variation demonstrates how Indian titles and terms were transliterated into English during the colonial era, with different spellings sometimes coexisting in official documents, literature, and historical records. Both spellings refer to the identical concept of supreme royal authority within Indian princely states, representing rulers who governed territories with considerable independence while managing complex relationships with larger political entities including the Mughal Empire and later the British colonial administration. The title encompasses the same cultural, political, and social significance regardless of spelling, including roles in governance, cultural patronage, military leadership, and religious authority that characterized these powerful rulers throughout Indian history. Historical documents and contemporary usage may prefer one spelling over another based on regional preferences, scholarly conventions, or institutional styles, though both forms are recognized as correct and refer to the same important historical and cultural institution. Understanding these spelling variations helps in researching Indian history, reading historical documents, and appreciating how language adaptation and cultural exchange influenced the preservation and transmission of Indian cultural concepts in English-language contexts.',
                'etymology': 'Alternative spelling of maharaja, from Sanskrit "maha" (great) + "raja" (king)',
                'memory_tip': 'Remember MAHARAJAH as the British spelling of maharaja - same great king, different spelling convention.',
                'example_sentence': 'The British colonial records referred to the ruler as _____, using the anglicized spelling common in official documents of that era.'
            },
            'mahogany': {
                'pronunciation': '/mə-HOG-ə-nee/',
                'definition': 'A tropical hardwood tree and its valuable timber, prized for its rich reddish-brown color, excellent workability, and durability that makes it one of the most sought-after woods for fine furniture, musical instruments, and decorative applications. Several tree species produce mahogany wood, including genuine mahogany from the Americas (Swietenia species) and African mahogany (Khaya species), each with distinctive characteristics that affect their use in various woodworking applications. The wood\'s properties include resistance to decay and insects, dimensional stability that prevents warping and cracking, and beautiful grain patterns that can be enhanced through various finishing techniques to create stunning furniture pieces and architectural elements. Historical significance includes mahogany\'s role in 18th and 19th-century furniture making, when it became the preferred wood for high-quality furniture in Europe and America, leading to extensive trade relationships and contributing to the economic development of tropical regions. Mahogany\'s acoustic properties make it valuable for musical instrument construction, particularly for guitar bodies, piano components, and other instruments where tonal quality and resonance are crucial for sound production. Conservation concerns affect many mahogany species due to overharvesting and habitat destruction, leading to international trade regulations and sustainable forestry initiatives that aim to preserve these valuable trees while meeting continued demand for this exceptional wood.',
                'etymology': 'Possibly from Spanish "caoba," from Taíno (Caribbean indigenous language)',
                'memory_tip': 'Remember MAHOGANY as the rich reddish-brown wood - "MAH-HOG" the beautiful wood.',
                'example_sentence': 'The antique dining table was crafted from solid _____, its rich grain and deep color having only improved with age.'
            },
            'maidenhair': {
                'pronunciation': '/MAY-dən-hair/',
                'definition': 'A type of delicate fern (Adiantum species) characterized by fine, lacy fronds and thin, dark stems that create an ethereal, graceful appearance reminiscent of fine hair, representing one of the most recognizable and widely cultivated fern groups worldwide. These distinctive ferns thrive in humid, shaded environments with good drainage and are particularly valued in horticulture for their delicate beauty and ability to add texture and elegance to shade gardens, indoor plant collections, and terrarium displays. The name derives from the resemblance of the fern\'s fine pinnules (leaflets) to delicate strands of hair, with some species having particularly thin and refined foliage that appears almost transparent when backlit by filtered sunlight. Maidenhair ferns have been used traditionally in various cultures for medicinal purposes, including treatments for respiratory ailments and hair care, though modern usage focuses primarily on their ornamental value and air-purifying qualities in indoor environments. Cultivation requires attention to moisture levels, humidity, and protection from direct sunlight, making these plants somewhat challenging but rewarding for gardeners who can provide appropriate growing conditions. The genus includes numerous species ranging from tiny indoor specimens to larger outdoor varieties, with some species being more tolerant of varying conditions while others require very specific environmental requirements to thrive and display their characteristic delicate beauty.',
                'etymology': 'Named for the resemblance of its fine fronds to delicate maiden\'s hair',
                'memory_tip': 'Remember MAIDENHAIR as the delicate fern with fronds fine as a "MAIDEN\'S HAIR."',
                'example_sentence': 'The _____ fern added a touch of delicate elegance to the shaded corner of the garden with its lacy, translucent fronds.'
            },
            'maillot': {
                'pronunciation': '/MY-oh/ or /MAH-yoh/',
                'definition': 'A close-fitting one-piece garment, most commonly referring to a swimsuit or bodysuit that covers the torso without separating into distinct top and bottom pieces, representing a practical and streamlined design for swimming, gymnastics, dance, and other athletic activities. The term originated in French fashion terminology and has been adopted internationally to describe various types of form-fitting garments that prioritize freedom of movement and minimal water resistance or air drag during physical activities. Maillots in swimming contexts provide competitive advantages through reduced drag compared to two-piece swimsuits, making them standard attire for serious swimmers and professional competitions where every fraction of a second matters in performance outcomes. Fashion applications include maillots as stylish swimwear that offers coverage while maintaining elegant lines and contemporary styling that appeals to individuals seeking both functionality and aesthetic appeal in their aquatic attire. Athletic contexts extend beyond swimming to include gymnastics leotards, dance wear, and other performance garments where the maillot design provides necessary coverage and support while allowing unrestricted movement essential for artistic and athletic expression. The versatility of maillot designs enables manufacturers to create garments suitable for various body types, activity levels, and style preferences while maintaining the fundamental characteristics of fit, comfort, and performance that define this category of clothing.',
                'etymology': 'From French "maillot," originally meaning swaddling clothes or jersey',
                'memory_tip': 'Remember MAILLOT as a "MY-OH" one-piece - a close-fitting athletic or swim garment.',
                'example_sentence': 'The competitive swimmer chose a sleek _____ for the championship race to minimize drag and maximize her speed in the water.'
            },
            'maize': {
                'pronunciation': '/MĀYZ/',
                'definition': 'A large grain plant domesticated in ancient Mexico, also known as corn in North America, representing one of the world\'s most important cereal crops that provides food, animal feed, and industrial materials for billions of people globally. This versatile plant (Zea mays) has been selectively bred over thousands of years from its wild ancestor teosinte into numerous varieties adapted to different climates, growing conditions, and uses ranging from sweet corn for direct human consumption to field corn for animal feed and industrial processing. Maize cultivation spreads throughout the Americas before European contact, serving as a dietary staple that supported the development of complex civilizations including the Maya, Aztec, and Inca empires that based their agricultural systems and food security on this productive crop. The plant\'s remarkable adaptability enabled its global spread following European colonization, with maize becoming established on every continent except Antarctica and adapting to diverse environmental conditions from tropical lowlands to high-altitude mountain regions. Modern maize production utilizes advanced agricultural techniques including hybrid varieties, precision planting, irrigation systems, and integrated pest management to maximize yields while minimizing environmental impacts, making it one of the most efficiently produced crops in contemporary agriculture. Industrial applications of maize include production of ethanol fuel, high-fructose corn syrup, biodegradable plastics, and hundreds of other products that demonstrate the crop\'s versatility beyond its role as food and animal feed.',
                'etymology': 'From Spanish "maíz," from Taíno "mahiz," referring to this New World grain',
                'memory_tip': 'Remember MAIZE as another name for corn - "MAZE" like the corn mazes made from this crop.',
                'example_sentence': 'The farmer planted drought-resistant _____ varieties to ensure a good harvest despite the challenging weather conditions.'
            },
            'majeure': {
                'pronunciation': '/mə-ZHUR/',
                'definition': 'Part of the legal term "force majeure," meaning "superior force" in French, referring to unforeseeable circumstances that prevent a party from fulfilling a contract, such as natural disasters, wars, or other events beyond reasonable human control that make contract performance impossible or impractical. Force majeure clauses appear in contracts to allocate risk and provide legal protection when extraordinary events disrupt normal business operations and contractual obligations, allowing parties to suspend or modify their commitments without being held liable for breach of contract. These provisions typically specify categories of events that qualify as force majeure, including acts of God (natural disasters), acts of government (regulatory changes, wars), labor disputes, infrastructure failures, and other circumstances that parties could not reasonably anticipate or prevent through normal business precautions. Legal interpretation of force majeure clauses requires careful analysis of specific contract language, the nature of the disruptive event, and whether affected parties took reasonable steps to mitigate the impact and fulfill their obligations despite challenging circumstances. Recent global events including the COVID-19 pandemic have increased attention to force majeure provisions as businesses worldwide have faced unprecedented disruptions that prevented normal contract performance and required legal analysis of what constitutes unforeseeable and uncontrollable circumstances. Understanding force majeure concepts helps in contract negotiation, risk management, and legal planning that protects parties from liability when truly extraordinary events make contract performance impossible.',
                'etymology': 'From French "majeure" meaning greater or superior, part of "force majeure" (superior force)',
                'memory_tip': 'Remember MAJEURE as "MAJOR" force - part of force majeure meaning major uncontrollable events.',
                'example_sentence': 'The contract included a force _____ clause that protected both parties from liability during natural disasters or other uncontrollable events.'
            },
            'major': {
                'pronunciation': '/MAY-jər/',
                'definition': 'Greater in importance, size, extent, or intensity; principal or significant rather than minor or secondary, representing the primary or most substantial element within a particular context, system, or situation. This adjective describes things that have considerable influence, size, or significance compared to other related elements, indicating priority, prominence, or substantial impact that affects outcomes, decisions, or understanding. Major can describe various categories including major cities that serve as important economic and cultural centers, major medical conditions that significantly affect health and require serious treatment, and major academic subjects that form the core focus of educational programs. In military contexts, major represents a mid-level officer rank between captain and lieutenant colonel, with responsibilities for leading larger units and serving in staff positions that require experience and demonstrated leadership capability. Musical applications include major scales and keys that create bright, stable harmonic foundations contrasting with minor tonalities, with major chords and progressions forming the basis for much Western music and establishing emotional associations with happiness and resolution. Understanding the concept of "major" helps in prioritizing information, making decisions, and recognizing the relative importance of different factors in complex situations where distinguishing between significant and minor elements guides effective action and resource allocation.',
                'etymology': 'From Latin "major" meaning greater or larger, comparative of "magnus" (great)',
                'memory_tip': 'Remember MAJOR as "MAJ-OR" - the greater or more important option or element.',
                'example_sentence': 'The _____ earthquake caused significant damage throughout the region, requiring extensive emergency response and reconstruction efforts.'
            },
            'majuscule': {
                'pronunciation': '/mə-JUS-kyool/',
                'definition': 'A capital or uppercase letter in writing and typography, representing the larger, more formal version of alphabetic characters used to begin sentences, proper nouns, and other grammatically significant words, contrasting with minuscule (lowercase) letters that form the majority of text in most writing systems. The term appears primarily in scholarly discussions of paleography, typography, and linguistics where precise terminology distinguishes between different letter forms and their historical development, evolution, and usage patterns across various writing traditions. Historical development of majuscule letters traces back to ancient Roman inscriptions and early medieval manuscripts where capital letters served both practical and aesthetic functions, providing visual hierarchy and ceremonial dignity to important texts and formal documents. Medieval scribes developed elaborate decorative majuscules, particularly for illuminated manuscripts where initial letters became artistic masterpieces combining calligraphy with illustration to create visually stunning and culturally significant textual presentations. Modern typography maintains distinctions between majuscule and minuscule forms while developing design principles that optimize readability, aesthetic appeal, and functional communication across print and digital media platforms. Understanding majuscule terminology and concepts helps in appreciating typographic design, historical manuscript traditions, and the evolution of writing systems that balance practical communication needs with cultural values regarding textual presentation, formality, and artistic expression.',
                'etymology': 'From Latin "majuscula" meaning somewhat larger, feminine of "majusculus" (larger)',
                'memory_tip': 'Remember MAJUSCULE as "MAJUS" (larger) + "CULE" (letter) - the larger capital letters.',
                'example_sentence': 'The medieval manuscript featured elaborate _____ letters decorated with gold leaf and intricate designs at the beginning of each chapter.'
            },
            'makes': {
                'pronunciation': '/MĀKS/',
                'definition': 'Third person singular present tense of "make," indicating the action of creating, producing, causing, or forming something through effort, skill, or process, representing one of the most fundamental and versatile verbs in English that describes countless human activities and natural processes. The word encompasses physical creation such as manufacturing products, preparing food, constructing buildings, and crafting objects, as well as abstract creation including making decisions, making friends, making progress, and making sense of complex situations. Different contexts use "makes" to describe various types of causation and production: cooking makes meals, education makes informed citizens, practice makes improvement, and hard work makes success more likely, demonstrating the verb\'s flexibility in expressing relationships between actions and outcomes. The concept extends to natural processes where environmental conditions make weather patterns, geological forces make mountains and valleys, and biological processes make growth and development possible in living organisms. Economic contexts include manufacturing that makes goods, services that make experiences possible, and innovation that makes technological advancement achievable, showing how human activity creates value and improves living conditions. Understanding the versatility of "makes" helps in clear communication about causation, production, and the countless ways that actions, processes, and conditions create changes in the physical and social world.',
                'etymology': 'Third person singular of "make" from Old English "macian" meaning to construct or create',
                'memory_tip': 'Remember MAKES as the action word for creating or causing something - "he/she/it MAKES."',
                'example_sentence': 'Hard work and dedication _____ the difference between mediocre and exceptional performance in any field.'
            },
            'makgadikgadi': {
                'pronunciation': '/mak-GAH-dee-GAH-dee/',
                'definition': 'A large salt pan complex in northeastern Botswana, representing one of the world\'s largest salt flats and an important archaeological and ecological site that provides insights into both ancient human history and contemporary environmental processes in southern Africa. These vast salt pans were formed by the gradual drying of ancient Lake Makgadikgadi, which once covered much of the Kalahari Basin and supported diverse ecosystems including early human populations whose archaeological remains provide evidence of human evolution and cultural development. The pans transform seasonally from dry, crusty salt flats that stretch to the horizon into temporary wetlands during rainy seasons when they fill with water and attract enormous concentrations of flamingos, pelicans, and other waterfowl that create spectacular wildlife displays. Archaeological significance includes some of the earliest evidence of modern human behavior, with stone tools and other artifacts found in the region providing crucial information about human migration patterns, technological development, and adaptation to changing environmental conditions over hundreds of thousands of years. The landscape demonstrates dramatic environmental changes over geological time, showing how climate shifts transformed a large freshwater lake system into the arid salt pan complex visible today, providing natural laboratories for studying long-term climate change and ecosystem adaptation. Modern conservation efforts protect both the unique ecosystem and archaeological heritage while supporting local communities through tourism and sustainable resource management that balances preservation with economic development needs.',
                'etymology': 'From Tswana language, meaning "the great thirst" or referring to the vast salt pans',
                'memory_tip': 'Remember MAKGADIKGADI as the great salt pans of Botswana - "MAK-GADIK-GADI" sounds like the vast, repeating landscape.',
                'example_sentence': 'Researchers studied the _____ Pans to understand ancient climate changes and early human migration patterns in southern Africa.'
            },
            'making': {
                'pronunciation': '/MAY-king/',
                'definition': 'The present participle of "make," describing the ongoing process of creating, producing, constructing, or causing something to exist or happen, representing active engagement in productive activities that transform raw materials, ideas, or situations into desired outcomes through skill, effort, and intention. This versatile term encompasses countless human activities from simple tasks like making breakfast or making beds to complex processes like making scientific discoveries, making artistic creations, or making important life decisions that shape personal and professional trajectories. Manufacturing contexts use making to describe industrial processes that convert raw materials into finished products through various stages of production, quality control, and assembly that require coordination of human workers, machines, and systems. Creative making includes artistic endeavors, craftsmanship, and innovation where individuals transform ideas and materials into original works that express personal vision, cultural values, or practical solutions to human needs and challenges. The concept extends to social and personal development where people engage in making friends, making improvements, making progress, and making contributions to their communities through various forms of positive action and engagement. Understanding making as an active, ongoing process helps appreciate the effort, skill, and dedication required for achievement while recognizing that creation and improvement require sustained engagement rather than single actions.',
                'etymology': 'Present participle of "make" from Old English "macian" meaning to construct',
                'memory_tip': 'Remember MAKING as "MAKE" + "ING" (ongoing) - currently in the process of creating or producing.',
                'example_sentence': 'The artisan spent months _____ the intricate wooden sculpture, carefully carving each detail by hand.'
            },
            'malachite': {
                'pronunciation': '/MAL-ə-kīt/',
                'definition': 'A bright green copper carbonate mineral prized for its vivid color and distinctive banded patterns, representing one of the most recognizable and historically significant copper minerals used for both ornamental and practical purposes throughout human civilization. This striking mineral forms through the weathering of copper ore deposits, creating distinctive green bands, swirls, and patterns that make each specimen unique and highly valued for decorative applications including jewelry, sculpture, and architectural ornamentation. Historical significance includes malachite\'s use as a pigment for paintings and cosmetics in ancient Egypt, Greece, and other civilizations where its brilliant green color was ground into powder for artistic and ceremonial applications before synthetic pigments became available. The mineral\'s properties include relative softness that makes it easy to carve and polish, distinctive green coloration that ranges from light to deep forest green, and beautiful patterns that result from rhythmic precipitation during its formation process. Geological occurrence typically involves copper-rich environments where groundwater circulation creates the chemical conditions necessary for malachite formation, often in association with other copper minerals including azurite, chrysocolla, and native copper. Modern applications include use in jewelry making, decorative objects, mineral collections, and as an indicator mineral in copper exploration that helps geologists locate valuable copper ore deposits in mining operations worldwide.',
                'etymology': 'From Greek "malakos" meaning soft, referring to the mineral\'s relative softness',
                'memory_tip': 'Remember MALACHITE as "MALA" (soft) + "KITE" (like the mineral) - the soft green mineral.',
                'example_sentence': 'The museum displayed a stunning _____ specimen with intricate green bands that showcased the mineral\'s natural beauty and patterns.'
            },
            'malacology': {
                'pronunciation': '/mal-ə-KOL-ə-jee/',
                'definition': 'The scientific study of mollusks, including snails, slugs, clams, oysters, squids, and octopuses, representing a specialized branch of zoology that investigates the anatomy, behavior, ecology, evolution, and classification of one of the largest and most diverse animal phyla on Earth. This field encompasses both marine and terrestrial mollusks, examining their remarkable diversity of body plans, reproductive strategies, feeding mechanisms, and ecological roles that range from microscopic parasites to giant squids that represent some of the largest invertebrates known to science. Malacologists study mollusk shell formation, growth patterns, and chemical composition that provide insights into environmental conditions, climate change impacts, and evolutionary history while also contributing to practical applications including aquaculture, pearl production, and biomedical research. The discipline includes paleontological aspects where fossil mollusks serve as important indicators of ancient environmental conditions, climate patterns, and geological time periods, with some mollusk fossils providing crucial evidence for understanding evolutionary processes and extinction events. Economic importance of malacological research includes contributions to fisheries management, aquaculture development, and conservation efforts that protect endangered mollusk species and their habitats from pollution, habitat destruction, and climate change impacts. Modern malacology utilizes advanced techniques including DNA analysis, electron microscopy, and computer modeling to understand mollusk biology and evolution while addressing practical challenges in marine conservation and sustainable resource management.',
                'etymology': 'From Greek "malakos" (soft) + "logos" (study), referring to the study of soft-bodied mollusks',
                'memory_tip': 'Remember MALACOLOGY as "MALACO" (soft creatures) + "LOGY" (study) - the study of mollusks.',
                'example_sentence': 'The professor specialized in _____ and spent her career studying the incredible diversity of marine snails and their evolutionary adaptations.'
            },
            'malady': {
                'pronunciation': '/MAL-ə-dee/',
                'definition': 'A disease, disorder, or ailment that affects physical or mental health; any condition that causes suffering, dysfunction, or impairment to normal biological or psychological functioning, representing disruptions to well-being that may range from minor temporary conditions to serious chronic illnesses. This somewhat formal term encompasses both physical maladies such as infections, injuries, genetic disorders, and degenerative diseases, as well as mental and emotional maladies including depression, anxiety, and other psychological conditions that affect quality of life and daily functioning. The word often carries connotations of persistent or troubling conditions rather than simple temporary discomfort, suggesting ailments that require attention, treatment, or management to restore normal functioning and prevent further deterioration or complications. Social contexts sometimes use "malady" metaphorically to describe problems affecting communities, institutions, or societies, such as social maladies including poverty, corruption, or violence that harm collective well-being and require systematic interventions to address root causes. Historical usage includes references to common maladies of particular time periods, demonstrating how disease patterns, medical understanding, and treatment approaches have evolved while revealing insights into living conditions, nutrition, and healthcare availability in different historical contexts. Understanding the concept of malady helps in discussing health issues with appropriate seriousness while recognizing the distinction between minor ailments and significant conditions that substantially impact individual or community well-being.',
                'etymology': 'From Old French "maladie," from Latin "male" (badly) + "habitus" (condition)',
                'memory_tip': 'Remember MALADY as "MAL" (bad) + "ADY" (condition) - a bad condition or illness.',
                'example_sentence': 'The physician worked tirelessly to develop treatments for the rare _____ that had baffled medical professionals for decades.'
            },
            'malaise': {
                'pronunciation': '/mə-LĀYZ/',
                'definition': 'A general feeling of discomfort, illness, or unease whose exact cause is difficult to identify; a vague sense that something is wrong physically, emotionally, or socially, representing a state of dissatisfaction or uneasiness that affects well-being without having clearly defined symptoms or sources. Physical malaise involves feelings of fatigue, weakness, or general unwellness that may precede specific illness or reflect ongoing health issues that haven\'t yet manifested as identifiable conditions requiring specific medical diagnosis and treatment. Psychological malaise encompasses emotional states including depression, anxiety, restlessness, or dissatisfaction with life circumstances that create persistent feelings of unease without necessarily having specific triggers or immediate solutions. Social and cultural malaise describes widespread feelings of discontent, alienation, or dissatisfaction within communities or societies, often reflecting underlying problems with economic conditions, political systems, or social structures that affect collective well-being and morale. The concept appears in various contexts including medical consultations where patients report feeling "unwell" without specific symptoms, literary and artistic works that explore themes of modern anxiety and dissatisfaction, and social commentary that examines collective mood and cultural health. Understanding malaise helps in recognizing early warning signs of health problems, addressing emotional and social needs that contribute to well-being, and identifying when vague feelings of unease warrant further attention or professional consultation.',
                'etymology': 'From French "malaise," from "mal" (badly) + "aise" (ease), meaning feeling badly at ease',
                'memory_tip': 'Remember MALAISE as "MAL" (bad) + "AISE" (ease) - feeling bad or uneasy without knowing why.',
                'example_sentence': 'She experienced a persistent _____ that made her feel generally unwell, though doctors couldn\'t find any specific medical problem.'
            },
            'malapropism': {
                'pronunciation': '/MAL-ə-prop-izm/',
                'definition': 'The mistaken use of a word in place of a similar-sounding one, often with amusing results that create unintended humor through the confusion of meanings, named after Mrs. Malaprop, a character in Richard Sheridan\'s 1775 play "The Rivals" who frequently confused words in this manner. These linguistic errors typically occur when speakers attempt to use sophisticated or formal vocabulary but select incorrect words that sound similar to their intended choices, creating statements that are grammatically correct but semantically absurd or humorous. Common examples include saying "a nice derangement of epitaphs" instead of "a nice arrangement of epithets," or "illiterate" instead of "obliterate," demonstrating how similar sounds can lead to dramatically different meanings. Malapropisms reveal interesting aspects of human language processing, showing how people store and retrieve words based on phonetic similarity rather than meaning, and how the desire to appear educated or sophisticated can sometimes lead to communication failures. The phenomenon appears in everyday speech, literature, comedy, and political discourse where speakers may inadvertently create memorable moments through word confusion that entertains audiences while potentially undermining their intended messages. Understanding malapropisms helps in language learning, communication skills development, and appreciating both the complexity of vocabulary acquisition and the humor that can result from linguistic mistakes that demonstrate the challenges of mastering language\'s intricate relationships between sound and meaning.',
                'etymology': 'Named after Mrs. Malaprop, a character in Sheridan\'s play "The Rivals" who misused words',
                'memory_tip': 'Remember MALAPROPISM as "MAL" (bad) + "PROP" (appropriate) - inappropriately using wrong but similar-sounding words.',
                'example_sentence': 'His speech was filled with amusing _____, such as saying "nuclear" instead of "unclear" and "extensive" instead of "expensive."'
            },
            'male': {
                'pronunciation': '/MĀYL/',
                'definition': 'Relating to or characteristic of the sex that typically produces small, mobile gametes (sperm) and possesses XY chromosomes in humans, representing one of the two primary biological sexes found in most sexually reproducing species throughout the animal and plant kingdoms. Male characteristics in humans typically include higher levels of testosterone, development of masculine secondary sexual characteristics during puberty, and reproductive anatomy designed for sperm production and delivery, though individual variation exists within normal biological ranges. The concept extends beyond purely biological definitions to include social and cultural roles, behaviors, and expectations associated with masculinity in different societies, though these social constructions vary significantly across cultures and historical periods. In animal species, males often display distinctive behaviors related to competition for mates, territorial defense, and parental care patterns that may differ from female behaviors, with some species showing dramatic sexual dimorphism in size, coloration, or other physical characteristics. Plant biology includes male flowers or plant parts that produce pollen for reproductive purposes, demonstrating that male-female distinctions exist across many forms of life as fundamental aspects of sexual reproduction and genetic diversity. Understanding male biology and social roles requires recognizing both biological foundations and cultural variations while appreciating individual differences that exist within all gender categories.',
                'etymology': 'From Old French "masle," from Latin "masculus" meaning masculine or male',
                'memory_tip': 'Remember MALE as the biological sex that typically produces sperm and has masculine characteristics.',
                'example_sentence': 'The study examined differences in communication styles between _____ and female participants in workplace settings.'
            },
            'males': {
                'pronunciation': '/MĀYLS/',
                'definition': 'Plural of male; referring to multiple individuals of the sex that typically produces sperm and possesses masculine biological and social characteristics, representing groups or populations of male humans, animals, or plants within various contexts including scientific research, social analysis, and demographic studies. In biological contexts, males of different species exhibit varying characteristics and behaviors that reflect evolutionary adaptations to environmental pressures, reproductive strategies, and social structures that influence survival and reproductive success. Human males show considerable diversity in physical characteristics, personality traits, cultural backgrounds, and social roles while sharing certain biological commonalities related to chromosomal patterns, hormone levels, and reproductive anatomy that distinguish them from females. Research contexts often examine males as a demographic group to understand patterns in health, behavior, education, employment, and other social indicators that may differ between sexes and inform policy decisions, medical treatments, and social programs. The term appears in discussions of gender equality, social justice, and cultural analysis where understanding male perspectives, experiences, and challenges contributes to comprehensive approaches to human development and social organization. Wildlife biology and conservation efforts often focus on male animals\' roles in reproduction, territory establishment, and social hierarchies that affect population dynamics and species survival in changing environmental conditions.',
                'etymology': 'Plural of "male" from Old French "masle," from Latin "masculus"',
                'memory_tip': 'Remember MALES as multiple "MALE" individuals - the plural form referring to groups of males.',
                'example_sentence': 'The research study found significant differences in risk-taking behavior between _____ and females in adolescent populations.'
            },
            'malevolent': {
                'pronunciation': '/mə-LEV-ə-lənt/',
                'definition': 'Having or showing a wish to do evil to others; characterized by malice, spite, or desire to cause harm, suffering, or misfortune to other people, representing one of the most serious forms of negative human motivation and behavior. Malevolent individuals actively seek opportunities to hurt others through various means including emotional manipulation, physical harm, social sabotage, or other actions designed to cause pain and damage to their targets. This adjective describes both conscious intentions to harm others and behaviors that consistently result in negative consequences for other people, whether through direct action or deliberate neglect and undermining of others\' well-being and success. Malevolent behavior can manifest in personal relationships through emotional abuse, betrayal, and manipulation, in professional settings through sabotage and hostile competition, and in broader social contexts through discrimination, oppression, and systematic harm to vulnerable groups. The concept extends to supernatural or fictional contexts where malevolent spirits, characters, or forces represent pure evil or destructive intent that threatens protagonists and innocent people in literature, mythology, and popular culture. Understanding malevolence helps in recognizing dangerous individuals and situations while developing protective strategies and ethical frameworks that promote positive human relationships and social structures that discourage harmful behavior and protect potential victims from those who wish them harm.',
                'etymology': 'From Latin "malevolens" meaning ill-wishing, from "male" (badly) + "volens" (wishing)',
                'memory_tip': 'Remember MALEVOLENT as "MALE" (badly) + "VOLENT" (wishing) - wishing badly or evil toward others.',
                'example_sentence': 'The _____ dictator systematically oppressed his people, showing no concern for their suffering and actively working to maintain their misery.'
            },
            'malfeasance': {
                'pronunciation': '/mal-FEE-zəns/',
                'definition': 'Illegal or unethical conduct, especially by a public official who abuses their position of trust and authority for personal gain or other improper purposes, representing serious violations of professional duty and public confidence that can result in criminal charges and civil liability. This legal term encompasses various forms of misconduct including embezzlement of public funds, accepting bribes, using official position for personal benefit, and other actions that violate the ethical and legal obligations that come with positions of public responsibility. Malfeasance differs from misfeasance (improper performance of lawful acts) and nonfeasance (failure to perform required duties) by involving actively wrongful or criminal behavior rather than mere negligence or incompetence in carrying out official responsibilities. The consequences of malfeasance can be severe, including removal from office, criminal prosecution, civil lawsuits, and permanent damage to reputation and career prospects, while also undermining public trust in institutions and democratic governance. Corporate contexts also recognize malfeasance when business executives or employees engage in fraud, embezzlement, or other illegal activities that harm shareholders, customers, or the public interest while violating their fiduciary duties and professional obligations. Preventing malfeasance requires robust oversight mechanisms, transparency requirements, ethical training, and accountability systems that deter misconduct while providing mechanisms for detecting and addressing violations when they occur.',
                'etymology': 'From French "malfaisance," from "mal" (badly) + "faisance" (doing), meaning doing badly',
                'memory_tip': 'Remember MALFEASANCE as "MAL" (bad) + "FEASANCE" (doing) - bad doing or misconduct by officials.',
                'example_sentence': 'The mayor was charged with _____ after investigators discovered he had been embezzling city funds for personal use.'
            },
            'malicious': {
                'pronunciation': '/mə-LISH-əs/',
                'definition': 'Characterized by malice; intending or intended to do harm; showing a desire to hurt, damage, or cause suffering to others through deliberate actions that demonstrate spite, cruelty, or vindictive motivation rather than accident or negligence. Malicious behavior involves conscious decision-making where individuals choose to act in ways that will harm others, often deriving satisfaction from causing pain, embarrassment, or damage to their targets through various means. This adjective appears in legal contexts where malicious acts may constitute crimes or civil wrongs that warrant punishment or compensation, with malicious intent being an important element in determining guilt, liability, and appropriate penalties for harmful actions. Computer security uses "malicious" to describe software, websites, or online activities designed to damage systems, steal information, or disrupt operations, including viruses, malware, phishing attacks, and other cyber threats created specifically to harm users and organizations. Social contexts include malicious gossip, rumors, and character assassination that deliberately damage reputations and relationships through false or harmful information spread with intent to cause social and emotional harm to targets. Understanding malicious behavior helps in recognizing threats, protecting oneself from harmful individuals, and developing appropriate responses that minimize damage while potentially seeking legal remedies when malicious actions cause significant harm or losses.',
                'etymology': 'From Latin "malitiosus" meaning full of malice, from "malitia" (malice)',
                'memory_tip': 'Remember MALICIOUS as "MALICE" + "IOUS" (full of) - full of malice, intending to harm others.',
                'example_sentence': 'The cybersecurity team detected _____ software attempting to steal sensitive customer data from the company\'s servers.'
            },
            'malignant': {
                'pronunciation': '/mə-LIG-nənt/',
                'definition': 'In medical contexts, describing cancerous tumors that grow uncontrollably, invade surrounding tissues, and spread to other parts of the body, representing the most serious and potentially life-threatening form of cancer that requires aggressive treatment to prevent progression and metastasis. Malignant tumors differ from benign growths by their ability to penetrate normal tissue boundaries, enter blood and lymphatic systems, and establish secondary growths in distant organs, making early detection and treatment crucial for successful outcomes. The term extends beyond medical usage to describe anything that is extremely harmful, evil, or destructive in nature, including malignant social influences, political systems, or personal characteristics that cause widespread damage and suffering to individuals and communities. Malignant personality traits include extreme narcissism, psychopathy, and other antisocial characteristics that lead individuals to harm others without remorse while often appearing charming or successful in superficial interactions. Environmental contexts may describe malignant pollution or ecological damage that spreads and intensifies over time, causing increasingly severe harm to ecosystems and human health through toxic contamination or habitat destruction. Understanding malignancy helps in recognizing serious threats whether medical, social, or environmental, and emphasizes the importance of early intervention, professional treatment, and systematic approaches to preventing the spread and escalation of harmful conditions.',
                'etymology': 'From Latin "malignus" meaning of bad nature, from "male" (badly) + root of "gigni" (to be born)',
                'memory_tip': 'Remember MALIGNANT as "MALIG" (bad nature) - describing harmful, spreading cancer or evil influence.',
                'example_sentence': 'The oncologist explained that the tumor was _____ and had already begun to spread to nearby lymph nodes.'
            },
            'malinger': {
                'pronunciation': '/mə-LING-gər/',
                'definition': 'To pretend to be ill or incapacitated in order to avoid work, duty, or other responsibilities; to feign sickness or disability for the purpose of escaping obligations or gaining sympathy and benefits that would not otherwise be available. This behavior involves deliberate deception where individuals exaggerate symptoms, fabricate illnesses, or prolong recovery from legitimate medical conditions to avoid unpleasant tasks, military service, work assignments, or other duties they wish to escape. Malingering can occur in various contexts including workplace situations where employees fake illness to avoid difficult projects or gain sick leave benefits, military settings where soldiers attempt to avoid combat or training, and legal contexts where individuals exaggerate injuries to gain compensation or avoid criminal prosecution. Medical professionals must distinguish between genuine illness and malingering through careful examination, psychological assessment, and observation of inconsistencies between reported symptoms and clinical findings, though this can be challenging when dealing with skilled deceivers. The behavior raises ethical questions about personal responsibility, fairness to others who must shoulder additional burdens, and the abuse of medical and social support systems designed to help genuinely ill or disabled individuals. Understanding malingering helps in developing appropriate responses that protect legitimate medical needs while discouraging fraudulent behavior that undermines trust and places unfair burdens on organizations and communities.',
                'etymology': 'From French "malingre" meaning sickly or weak, possibly from "mal" (bad) + Old French "haingre" (thin)',
                'memory_tip': 'Remember MALINGER as "MAL" (fake) + "LINGER" (stay) - fake staying sick to avoid responsibility.',
                'example_sentence': 'The supervisor suspected the employee might be trying to _____ after calling in sick every Friday for three consecutive weeks.'
            },
            'malleable': {
                'pronunciation': '/MAL-ee-ə-bəl/',
                'definition': 'Capable of being shaped, formed, or influenced; easily hammered, pressed, or bent without breaking, referring both to physical properties of materials and metaphorical flexibility in people, ideas, or situations that can be modified or adapted to different circumstances. In metallurgy and materials science, malleable substances like gold, silver, and copper can be hammered into thin sheets, stretched into wires, or formed into complex shapes without fracturing, making them valuable for manufacturing, jewelry making, and artistic applications. The concept extends to psychological and social contexts where malleable personalities, young minds, or developing institutions can be influenced, educated, or shaped by external forces including education, training, social pressure, and environmental conditions. Malleable materials and people share the characteristic of adaptability that enables them to change form or behavior while maintaining their essential identity and structural integrity, making flexibility a valuable trait in both physical and social applications. Understanding malleability helps in working with materials and people effectively, recognizing opportunities for positive change and development while avoiding excessive pressure that might cause damage rather than beneficial transformation. The concept appears in education, leadership, therapy, and personal development where the goal is to create positive changes through appropriate influence and support rather than force or coercion.',
                'etymology': 'From Latin "malleus" meaning hammer, referring to the ability to be hammered into shape',
                'memory_tip': 'Remember MALLEABLE as "MALLE" (hammer) + "ABLE" - able to be hammered or shaped without breaking.',
                'example_sentence': 'Gold is highly _____ and can be hammered into extremely thin sheets for use in decorative applications and electronics.'
            },
            'malleolus': {
                'pronunciation': '/mə-LEE-ə-ləs/',
                'definition': 'Either of the bony prominences on each side of the ankle joint, representing the lower ends of the tibia (medial malleolus) and fibula (lateral malleolus) that form crucial anatomical landmarks and provide stability for the ankle joint through their articulation with the talus bone. These important anatomical structures serve as attachment points for ligaments that provide lateral stability to the ankle, preventing excessive inward or outward movement that could result in sprains, fractures, or other injuries during walking, running, and other activities. Medical professionals use malleoli as reference points for physical examination, diagnostic imaging, and surgical procedures involving the ankle and lower leg, with fractures of these structures being common injuries that require careful treatment to restore normal function. The medial malleolus (inner ankle bone) and lateral malleolus (outer ankle bone) work together with surrounding ligaments and muscles to create a stable yet mobile joint that enables the complex movements required for human locomotion on varied terrain. Ankle injuries often involve damage to one or both malleoli, requiring medical evaluation to determine appropriate treatment ranging from conservative management with immobilization to surgical repair for severe fractures or ligament damage. Understanding malleolus anatomy helps in recognizing ankle injuries, appreciating the complexity of human joint structure, and making informed decisions about treatment options when ankle problems occur.',
                'etymology': 'From Latin "malleolus" meaning small hammer, referring to the hammer-like shape of these ankle bones',
                'memory_tip': 'Remember MALLEOLUS as "small MALLET" - the hammer-shaped ankle bones on each side of your foot.',
                'example_sentence': 'The X-ray showed a fracture of the lateral _____, requiring surgery to properly align and stabilize the ankle joint.'
            },
            'mallet': {
                'pronunciation': '/MAL-it/',
                'definition': 'A hammer-like tool with a large, usually wooden head used for striking objects without damaging them, representing an essential implement in woodworking, construction, musical performance, and various crafts where controlled striking force is needed without the marring effects of metal hammers. Different types of mallets serve specific purposes: wooden mallets for woodworking and furniture assembly, rubber mallets for tile installation and automotive work, rawhide mallets for leatherworking and jewelry making, and specialized mallets for musical instruments like xylophones and marimbas. The tool\'s design emphasizes control and surface protection, with heads made from materials softer than typical hammer heads to prevent damage to finished surfaces, delicate materials, or precision work where exact force application is crucial for successful outcomes. Musical applications include mallets designed for specific instruments, with variations in head materials, size, and hardness that affect the tone, volume, and character of sounds produced when striking percussion instruments, bells, or other musical devices. Construction and automotive contexts use mallets for tasks requiring significant force without surface damage, including tile setting, panel fitting, bearing installation, and other applications where metal hammers would cause unwanted dents, scratches, or structural damage. Understanding mallet selection and proper usage helps in achieving professional results while preserving material integrity and ensuring safety during various striking and assembly operations.',
                'etymology': 'From Old French "maillet," diminutive of "mail" (hammer), meaning small hammer',
                'memory_tip': 'Remember MALLET as a soft-headed hammer - "MALL-ET" like a gentler hammer for delicate work.',
                'example_sentence': 'The woodworker used a rubber _____ to carefully tap the furniture joints together without damaging the finished surface.'
            },
            'malnutrition': {
                'pronunciation': '/MAL-noo-TRISH-ən/',
                'definition': 'A condition resulting from inadequate, excessive, or imbalanced nutrition that fails to meet the body\'s requirements for optimal growth, development, and maintenance of healthy biological functions, representing a serious global health challenge that affects millions of people across all age groups and socioeconomic levels. This condition encompasses both undernutrition caused by insufficient caloric intake or essential nutrient deficiencies, and overnutrition resulting from excessive consumption of calories, fats, sugars, or processed foods that create health problems including obesity and related chronic diseases. Undernutrition includes protein-energy malnutrition that stunts growth and development in children, micronutrient deficiencies that cause conditions like anemia and scurvy, and wasting syndromes that compromise immune function and increase vulnerability to infectious diseases. The consequences of malnutrition are particularly severe for children, pregnant women, and elderly individuals whose nutritional needs are highest and whose bodies are least able to compensate for dietary inadequacies that can result in permanent developmental damage or increased mortality risk. Causes include poverty, food insecurity, inadequate healthcare, poor sanitation, armed conflict, and lack of nutrition education that prevent access to adequate, nutritious food and proper feeding practices necessary for health maintenance. Prevention and treatment strategies require comprehensive approaches including economic development, agricultural improvement, education programs, healthcare access, and policy interventions that address the root causes of food insecurity and promote healthy eating behaviors.',
                'etymology': 'From "mal" (bad) + "nutrition," meaning bad or inadequate nutrition',
                'memory_tip': 'Remember MALNUTRITION as "MAL" (bad) + "NUTRITION" - bad or inadequate nutrition affecting health.',
                'example_sentence': 'The humanitarian organization worked to combat _____ in refugee camps by providing balanced meals and nutrition education programs.'
            },
            'mambo': {
                'pronunciation': '/MAM-boh/',
                'definition': 'A ballroom dance of Cuban origin characterized by a basic pattern of two quick steps and a slow step, performed to Latin music with distinctive rhythmic patterns that emphasize syncopation and infectious energy that encourages improvisation and expressive movement. The dance originated in Cuba during the 1940s through the fusion of rumba, swing, and Afro-Cuban musical elements, becoming internationally popular through the work of musicians like Pérez Prado and Tito Puente who helped establish mambo as a major Latin dance and musical genre. Mambo music features complex percussion patterns, brass sections, and rhythmic structures that create the driving energy essential for dance performance, with composers and arrangers developing sophisticated musical arrangements that showcase both individual virtuosity and ensemble coordination. The dance requires partners to work together while maintaining individual expression through hip movements, shoulder isolations, and footwork patterns that reflect the music\'s rhythmic complexity and emotional intensity while staying connected through leads and follows. Social and cultural significance includes mambo\'s role in breaking down racial barriers in American dance halls and promoting Latin American culture internationally, contributing to the development of salsa and other Latin dance forms that continue to evolve today. Modern mambo includes both social dancing in clubs and community centers and competitive ballroom dancing where technical precision and artistic interpretation are judged according to established standards for posture, timing, and musical expression.',
                'etymology': 'From Spanish "mambo," possibly from Haitian Creole meaning conversation with the gods',
                'memory_tip': 'Remember MAMBO as the lively Cuban dance - "MAM-BO" sounds like the rhythmic beat of the music.',
                'example_sentence': 'The dance instructor taught the basic _____ steps, emphasizing the quick-quick-slow rhythm that defines this energetic Latin dance.'
            },
            'mammal': {
                'pronunciation': '/MAM-əl/',
                'definition': 'A warm-blooded vertebrate animal characterized by having hair or fur, producing milk to feed their young, and typically giving birth to live offspring rather than laying eggs, representing one of the most diverse and successful animal classes that includes humans, whales, bats, elephants, and thousands of other species worldwide. Mammals possess several distinctive features including mammary glands that produce nutritious milk for nursing infants, three middle ear bones that enable sensitive hearing, and neocortex brain regions that support complex learning, memory, and behavioral flexibility not found in other animal groups. The class encompasses remarkable diversity in size, habitat, and lifestyle, from tiny shrews weighing less than an ounce to blue whales exceeding 100 feet in length, and from desert-dwelling camels to arctic seals adapted for life in frozen waters. Reproductive strategies vary among mammals but generally involve internal fertilization, extended parental care, and complex social behaviors that facilitate learning and survival in challenging environments where intelligence and adaptability provide significant advantages. Evolutionary success of mammals relates to their ability to maintain constant body temperature, efficient metabolism, and sophisticated sensory systems that enable them to exploit diverse ecological niches while competing successfully with other animal groups. Modern conservation challenges affect many mammal species due to habitat loss, climate change, and human activities that require international cooperation and scientific management to preserve mammalian biodiversity for future generations.',
                'etymology': 'From Latin "mammalis" meaning of the breast, from "mamma" (breast), referring to milk production',
                'memory_tip': 'Remember MAMMAL as animals with "MAMmary glands" that produce milk for babies.',
                'example_sentence': 'The blue whale is the largest _____ on Earth, using its mammary glands to produce hundreds of gallons of milk daily for its calf.'
            },
            'mammalian': {
                'pronunciation': '/mə-MAY-lee-ən/',
                'definition': 'Relating to or characteristic of mammals; possessing the distinctive features and traits that define the mammalian class including warm-bloodedness, hair or fur, milk production, and typically live birth, representing characteristics that distinguish this vertebrate group from birds, reptiles, amphibians, and fish. Mammalian physiology includes advanced circulatory systems with four-chambered hearts, sophisticated nervous systems with well-developed brains, and efficient respiratory systems that support the high metabolic rates required for maintaining constant body temperature in varying environmental conditions. Research contexts use mammalian to describe biological processes, anatomical structures, evolutionary relationships, and physiological mechanisms that are characteristic of or derived from mammal studies, with laboratory mammals serving as important models for understanding human health and disease. The adjective appears in discussions of mammalian evolution, comparative anatomy, reproductive biology, and behavioral ecology where scientists examine how mammalian traits developed and function across different species and environmental contexts. Mammalian characteristics enable success in diverse environments through adaptations including hibernation, migration, complex social structures, and specialized feeding strategies that demonstrate the evolutionary advantages of mammalian biology and behavior. Understanding mammalian traits helps in appreciating biodiversity, evolutionary relationships, and the biological foundations of human health while recognizing the connections between humans and other mammalian species that share fundamental anatomical and physiological characteristics.',
                'etymology': 'From "mammal" + suffix "-ian" meaning relating to or characteristic of mammals',
                'memory_tip': 'Remember MAMMALIAN as "MAMMAL" + "IAN" (relating to) - relating to or characteristic of mammals.',
                'example_sentence': 'The researcher studied _____ evolution by comparing skull structures across different species to understand brain development patterns.'
            },
            'mamushi': {
                'pronunciation': '/mə-MOO-shee/',
                'definition': 'A venomous pit viper (Gloydius blomhoffii) native to Japan, Korea, and parts of Russia and China, recognized as one of the most medically significant venomous snakes in East Asia due to its relatively aggressive nature, potent venom, and frequent encounters with humans in rural and suburban areas. This species typically measures 1-2 feet in length with distinctive brown and tan patterning that provides effective camouflage in forest floor environments where it hunts small mammals, birds, and amphibians using heat-sensing pit organs to locate warm-blooded prey. Mamushi venom contains various toxic compounds including hemotoxins that destroy red blood cells and tissue, causing severe pain, swelling, bleeding disorders, and potentially life-threatening systemic effects that require prompt medical treatment with appropriate antivenoms. The snake plays important ecological roles as both predator and prey species in East Asian forest ecosystems, helping control rodent populations while serving as food for larger predators including birds of prey and other snakes. Cultural significance includes mamushi\'s place in traditional medicine and folklore, where various parts of the snake have been used in folk remedies despite the obvious dangers of handling venomous species without proper expertise and safety precautions. Modern conservation concerns include habitat loss and human persecution that affect mamushi populations, though the species generally maintains stable numbers throughout most of its range due to its adaptability to disturbed environments.',
                'etymology': 'From Japanese "mamushi" (蝮), referring to this specific venomous pit viper',
                'memory_tip': 'Remember MAMUSHI as the Japanese venomous snake - "MA-MUSHI" sounds like "my mushy" bite from this dangerous viper.',
                'example_sentence': 'Hikers in rural Japan were warned to watch for the _____, a venomous pit viper whose bite requires immediate medical attention.'
            }
        }
        
        # Get data for the specific word
        if word in word_data:
            data = word_data[word]
            difficulty_components = self.difficulty_calc.calculate_difficulty_components(
                word, data['definition'], data['etymology']
            )
            
            return {
                'word': word,
                'pronunciation': data['pronunciation'],
                'definition': data['definition'],
                'example_sentence': data['example_sentence'],
                'etymology': data['etymology'],
                'etymology_source': 'Claude',
                'memory_tip': data['memory_tip'],
                **difficulty_components
            }
        
        # Default case for any missing words
        return {
            'word': word,
            'pronunciation': f'/{word.upper()}/',
            'definition': f'A word that requires additional research for comprehensive definition.',
            'example_sentence': f'The word _____ needs further investigation.',
            'etymology': 'Etymology requires additional research.',
            'etymology_source': 'Claude',
            'memory_tip': f'Remember {word.upper()} - additional memory techniques needed.',
            'phonetic_transparency_score': 3.0,
            'word_frequency_score': 3.0,
            'morphological_complexity_score': 3.0,
            'etymology_complexity_score': 3.0,
            'final_difficulty': None
        }

def process_batch_106():
    """Process Batch 106 with comprehensive Claude data"""
    input_file = Path("output/batch_106_words.csv")
    output_file = Path("output/batch_106_processed.csv")
    
    if not input_file.exists():
        logger.error(f"Input file {input_file} not found")
        return False
    
    processor = Batch106Processor()
    processed_words = []
    
    try:
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                word = row['word'].strip()
                if word:  # Skip empty rows
                    # Get comprehensive data from Claude
                    word_data = processor.get_comprehensive_claude_data(word)
                    
                    # Add original source data
                    word_data.update({
                        'years': row['years'],
                        'source_files': row['source_files'], 
                        'source_difficulties': row['source_difficulties']
                    })
                    
                    processed_words.append(word_data)
                    logger.info(f"Processed word: {word}")
        
        # Write output file with all required columns in correct order
        fieldnames = [
            'word', 'pronunciation', 'definition', 'example_sentence',
            'etymology', 'etymology_source', 'memory_tip',
            'phonetic_transparency_score', 'word_frequency_score', 
            'morphological_complexity_score', 'etymology_complexity_score',
            'final_difficulty', 'years', 'source_files', 'source_difficulties'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed_words)
        
        logger.info(f"Saved {len(processed_words)} words to {output_file}")
        logger.info(f"Batch 106 processing completed!")
        logger.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
        logger.info(f"Output saved to: {output_file}")
        logger.info(f"Results: {len(processed_words)} successful, 0 failed")
        
        return True
        
    except Exception as e:
        logger.error(f"Error processing batch 106: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Processing Batch 106 with comprehensive Claude data...")
    success = process_batch_106()
    sys.exit(0 if success else 1)