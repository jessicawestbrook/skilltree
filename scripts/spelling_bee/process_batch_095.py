#!/usr/bin/env python3
"""
Process Batch 095 of Spelling Bee Words with Comprehensive Claude Data
Generates full definitions, pronunciations, etymologies, memory tips, and examples for all 50 words
"""

import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class WordData:
    word: str
    years: str
    source_files: str
    source_difficulties: str
    definition: str = ""
    pronunciation: str = ""
    etymology: str = ""
    language_origins: str = ""
    example_sentence: str = ""
    definition_source: str = ""
    pronunciation_source: str = ""
    etymology_source: str = ""
    error_notes: str = ""
    # Claude-generated fields
    claude_definition: str = ""
    part_of_speech: str = ""
    pronunciation_guide: str = ""
    claude_etymology: str = ""
    memory_tips: str = ""
    alternate_spellings: str = ""
    claude_language_origin: str = ""

class DifficultyCalculator:
    """Implements sophisticated difficulty rating from THEORETICAL_FOUNDATIONS.md"""
    
    def __init__(self):
        # Common word frequency list (top 3000 most common English words)
        self.common_words = self._load_common_words()
        
    def _load_common_words(self) -> set:
        """Load common English words for frequency scoring"""
        common = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
            'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him',
            'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only',
            'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want',
            'because', 'any', 'these', 'give', 'day', 'most', 'us', 'is', 'water', 'long', 'find', 'here', 'thing', 'great', 'man', 'world', 'life',
            'still', 'public', 'human', 'get', 'old', 'country', 'hand', 'part', 'child', 'eye', 'woman', 'place', 'work', 'week', 'case', 'point',
            'government', 'company', 'number', 'group', 'problem', 'fact', 'actually', 'across', 'activities', 'activity', 'adding', 'addition'
        }
        return common
    
    def calculate_phonetic_transparency(self, word: str, pronunciation: str) -> float:
        """Score based on how predictable pronunciation is from spelling (1-4 scale)"""
        if not pronunciation:
            return 2.5  # Default for missing pronunciation
            
        # Count irregular spelling patterns
        irregular_patterns = 0
        word_lower = word.lower()
        
        # Common irregular patterns
        irregular_mappings = [
            ('ph', 'f'), ('gh', 'f'), ('ough', 'uff'), ('ight', 'ite'),
            ('tion', 'shun'), ('sion', 'zhun'), ('ture', 'cher'),
            ('que', 'k'), ('x', 'ks'), ('c', 'k'), ('c', 's')
        ]
        
        for spelling, sound in irregular_mappings:
            if spelling in word_lower:
                irregular_patterns += 1
        
        # Silent letters
        silent_patterns = ['k', 'b', 'l', 'gh', 'w', 't', 'h']
        for pattern in silent_patterns:
            if pattern in word_lower and len(word) > 4:
                irregular_patterns += 0.5
        
        # More irregular = higher difficulty
        if irregular_patterns == 0:
            return 1.0  # Very transparent
        elif irregular_patterns <= 1:
            return 2.0  # Mostly transparent
        elif irregular_patterns <= 2:
            return 3.0  # Moderately opaque
        else:
            return 4.0  # Very opaque
    
    def calculate_word_frequency(self, word: str) -> float:
        """Score based on how common/rare the word is (1-4 scale)"""
        word_lower = word.lower()
        
        if word_lower in self.common_words:
            return 1.0  # Very common
        elif len(word) <= 4:
            return 2.0  # Short words tend to be more common
        elif len(word) <= 7:
            return 3.0  # Medium length
        else:
            return 4.0  # Long words tend to be rarer
    
    def calculate_morphological_complexity(self, word: str, etymology: str) -> float:
        """Score based on morphological structure complexity (1-4 scale)"""
        # Count morphemes (prefixes, roots, suffixes)
        morpheme_count = 1  # Base word
        
        # Common prefixes
        prefixes = [
            'un', 're', 'in', 'dis', 'en', 'non', 'pre', 'pro', 'anti', 'de', 'over', 'under',
            'sub', 'super', 'inter', 'trans', 'semi', 'auto', 'co', 'counter', 'extra', 'hyper',
            'mega', 'micro', 'mini', 'multi', 'neo', 'pseudo', 'ultra', 'ac', 'ad', 'con'
        ]
        
        # Common suffixes
        suffixes = [
            'ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment', 'able', 'ible',
            'ful', 'less', 'ous', 'ious', 'al', 'ic', 'ical', 'ism', 'ist', 'ize', 'ise',
            'fy', 'ward', 'wise', 'like', 'ship', 'hood', 'dom', 'age', 'ery', 'ary', 'ate'
        ]
        
        word_lower = word.lower()
        
        # Count prefixes
        for prefix in sorted(prefixes, key=len, reverse=True):
            if word_lower.startswith(prefix) and len(word_lower) > len(prefix) + 2:
                morpheme_count += 1
                word_lower = word_lower[len(prefix):]
                break
        
        # Count suffixes
        for suffix in sorted(suffixes, key=len, reverse=True):
            if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 2:
                morpheme_count += 1
                break
        
        # Convert to 1-4 scale
        if morpheme_count == 1:
            return 1.0  # Simple word
        elif morpheme_count == 2:
            return 2.0  # One affix
        elif morpheme_count == 3:
            return 3.0  # Two affixes
        else:
            return 4.0  # Complex morphology
    
    def calculate_etymology_complexity(self, etymology: str, language_origins: str) -> float:
        """Score based on etymology complexity (1-4 scale)"""
        if not etymology and not language_origins:
            return 2.5  # Default for missing etymology
        
        # Analyze language origins
        origins_text = f"{etymology} {language_origins}".lower()
        
        # Germanic/English roots are easier for English speakers
        if any(term in origins_text for term in ['old english', 'middle english', 'germanic', 'anglo-saxon']):
            base_score = 1.0
        # Latin/French are medium difficulty
        elif any(term in origins_text for term in ['latin', 'french', 'norman']):
            base_score = 2.0
        # Greek and other European languages are harder
        elif any(term in origins_text for term in ['greek', 'spanish', 'italian', 'german']):
            base_score = 3.0
        # Non-European languages are hardest
        else:
            base_score = 4.0
        
        # Adjust for multiple languages
        language_indicators = ['from', 'via', 'through', 'ultimately']
        complexity_boost = sum(1 for indicator in language_indicators if indicator in origins_text) * 0.3
        
        return min(4.0, base_score + complexity_boost)

class Batch095Processor:
    """Processes Batch 095 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 095 words"""
        
        # Comprehensive data for all 50 words in Batch 095
        batch_095_data = {
            'janthina': {
                'definition': 'A genus of violet sea snails, pelagic gastropod mollusks that create air-filled floats and drift on ocean surfaces. These delicate marine creatures are famous for their unique lifestyle of hanging upside down from bubble rafts they construct by secreting mucus and trapping air bubbles. Janthina species exhibit beautiful violet to purple shells and feed on surface-dwelling organisms like Portuguese man-o-war. They represent one of the few gastropod groups adapted for a completely pelagic existence, drifting across warm tropical and subtropical waters worldwide. Their reproductive strategy and feeding behavior are closely tied to their floating lifestyle, making them fascinating subjects for marine biological research.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jan-THY-nah (emphasis on second syllable)',
                'etymology': 'From Greek "ianthinos" meaning "violet-colored," referring to the characteristic purple-violet coloration of their shells',
                'memory_tips': 'Think "jan-thin-a" - thin violet shells floating like Janus (January) looking both ways on the ocean surface',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'Marine biologists collected several _____ specimens floating on their characteristic bubble rafts during the research expedition.'
            },
            'january': {
                'definition': 'The first month of the year in the Gregorian calendar, containing 31 days and named after Janus, the Roman god of beginnings, transitions, and doorways. January marks the start of the new year in most cultures, often associated with fresh starts, resolutions, and new opportunities. In the Northern Hemisphere, it is typically the coldest winter month, characterized by snow, frost, and shorter daylight hours. The month holds significant cultural importance as a time for reflection on the past year and planning for the future, influencing agricultural cycles, seasonal activities, and human behavior patterns worldwide.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JAN-yoo-air-ee (emphasis on first syllable)',
                'etymology': 'From Latin "Ianuarius" meaning "of Janus," named after the Roman god Janus who had two faces looking backward and forward, symbolizing transitions',
                'memory_tips': 'Think "Janus-uary" - the two-faced god looking back at the old year and forward to the new year',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Many people make resolutions at the beginning of _____ to start the new year with positive changes.'
            },
            'japan': {
                'definition': 'An island nation in East Asia located in the Pacific Ocean, consisting of four main islands and numerous smaller ones. Japan is renowned for its unique blend of ancient traditions and cutting-edge technology, distinctive cultural elements including samurai history, traditional arts, and modern innovations in electronics and automotive industries. The country has approximately 125 million people and features mountainous terrain including the iconic Mount Fuji. Japan has played a significant role in global economics, technology development, and cultural exchange, contributing major innovations in manufacturing, robotics, and entertainment while maintaining its rich cultural heritage.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'juh-PAN (emphasis on second syllable)',
                'etymology': 'From Chinese "Riben" via Malay "Japang," meaning "origin of the sun," reflecting its eastern position relative to China',
                'memory_tips': 'Think "ja-pan" - a cooking pan from the land of the rising sun, famous for distinctive cuisine',
                'alternate_spellings': '',
                'language_origin': 'Chinese via Malay',
                'example_sentence': 'Many tourists visit _____ to experience the unique combination of traditional culture and modern technology.'
            },
            'japanese': {
                'definition': 'Relating to Japan, its people, language, or culture; or a person from Japan or the Japanese language. As an adjective, it describes anything originating from or associated with Japan. The term encompasses the Japanese language with its three writing systems (hiragana, katakana, and kanji), cultural practices emphasizing harmony and respect, traditional arts, and social customs. The Japanese language is spoken by approximately 125 million people and features sophisticated honorific expressions and contextual communication patterns that reflect cultural values of respect and social hierarchy.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'jap-uh-NEEZ (emphasis on third syllable)',
                'etymology': 'From "Japan" + suffix "-ese" indicating nationality or language, following standard patterns for nationality words',
                'memory_tips': 'Think "Japan-ese" - the "-ese" suffix indicates people, language, or things from Japan',
                'alternate_spellings': '',
                'language_origin': 'English formation',
                'example_sentence': 'She studied _____ culture and language for four years before traveling to Tokyo.'
            },
            'jargon': {
                'definition': 'Specialized terminology, vocabulary, or expressions used by members of a particular profession, trade, hobby, or social group that may be difficult for outsiders to understand. Jargon serves as professional shorthand, allowing experts to communicate complex concepts efficiently and precisely within their field. While it enhances communication within specialized communities, it can create barriers for those unfamiliar with the terminology. Examples include medical, legal, computer, and military jargon. The appropriate use of jargon versus plain language is crucial for effective communication across different audiences.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JAR-gon (emphasis on first syllable)',
                'etymology': 'From Old French "jargon" meaning "chattering, twittering," possibly from an imitative origin suggesting confused speech',
                'memory_tips': 'Think "jar-gone" - specialized language kept in a jar, gone from common understanding',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The medical _____ made it difficult for patients to understand their diagnosis.'
            },
            'jarl': {
                'definition': 'A Scandinavian noble or chief during the Viking Age and medieval period, ranking below a king but above ordinary freemen. Jarls were powerful feudal lords who controlled territories, commanded armies, and owed allegiance to the king. They possessed significant wealth, land holdings, and political influence, often serving as military leaders during conflicts and raids. The position was typically hereditary, though exceptional warriors could be elevated through royal favor. Jarls played crucial roles in organizing expeditions, administering justice, and maintaining order, equivalent to English earls.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'YARL (single syllable, like "earl" with Y sound)',
                'etymology': 'From Old Norse "jarl" meaning "nobleman, earl," related to English "earl"',
                'memory_tips': 'Think "yarl" sounds like "earl" - both are nobleman titles of equivalent rank',
                'alternate_spellings': '',
                'language_origin': 'Old Norse',
                'example_sentence': 'The Viking _____ ruled over several coastal settlements and commanded a fleet of longships.'
            },
            'jars': {
                'definition': 'Cylindrical containers with wide mouths, typically made of glass, ceramic, or plastic, used for storing food, liquids, or other materials. Jars feature designs ideal for preservation with airtight seals and are available in various sizes for different purposes including mason jars for canning, storage jars for dry goods, and decorative containers. The wide opening allows easy filling and cleaning, making them practical for both short-term storage and long-term food preservation. Archaeological evidence shows ceramic jars have been used for thousands of years across human civilizations.',
                'part_of_speech': 'noun (plural), verb (third person singular)',
                'pronunciation_guide': 'JARZ (single syllable)',
                'etymology': 'From French "jarre" meaning "large earthen vessel," ultimately from Arabic "jarrah"',
                'memory_tips': 'Think "jars" - containers that can "jar" you if they fall and break',
                'alternate_spellings': '',
                'language_origin': 'French via Arabic',
                'example_sentence': 'The kitchen shelves were lined with glass _____ filled with colorful spices and herbs.'
            },
            'jasmone': {
                'definition': 'An organic compound with the formula C11H16O, naturally occurring in jasmine flowers and other plants, responsible for the characteristic floral fragrance of jasmine. This volatile cyclopentenone compound is important in perfumery and fragrance applications, existing in different isomeric forms with cis-jasmone being particularly significant for olfactory properties. Beyond natural flower fragrances, jasmone is studied for biological activities and used in synthetic fragrance components for cosmetics and scented products, representing plant chemistry research and artificial fragrance development.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JAS-mohn (emphasis on first syllable)',
                'etymology': 'From "jasmine" + chemical suffix "-one" indicating a ketone compound, following standard chemical nomenclature',
                'memory_tips': 'Think "jasmine-one" - the number one scent compound that makes jasmine smell sweet',
                'alternate_spellings': '',
                'language_origin': 'Modern chemical terminology',
                'example_sentence': 'Perfumers prize _____ for its sweet, floral aroma that captures the essence of jasmine blossoms.'
            },
            'jasper': {
                'definition': 'An opaque, microcrystalline variety of quartz characterized by rich colors and patterns, commonly found in red, yellow, brown, and green hues. Jasper forms through slow silica precipitation from groundwater, incorporating iron oxides and minerals that create distinctive coloration and banding. This semi-precious stone has been prized throughout history for jewelry and ceremonial purposes, with archaeological evidence from ancient civilizations worldwide. Different varieties are named for appearance or origin, exhibiting waxy to vitreous luster when polished and ranking 6.5-7 on the Mohs hardness scale.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JAS-per (emphasis on first syllable)',
                'etymology': 'From Greek "iaspis" via Latin "iasper," ultimately from a Semitic language',
                'memory_tips': 'Think "jazz-per" - a jazzy, colorful stone perfect for decoration',
                'alternate_spellings': '',
                'language_origin': 'Greek via Latin',
                'example_sentence': 'The ancient Egyptian amulet was carved from deep red _____ and inlaid with gold.'
            },
            'jaundiced': {
                'definition': 'Having yellowish discoloration of skin, eyes, or mucous membranes due to excess bilirubin from liver dysfunction, bile duct obstruction, or red blood cell breakdown. Medically, jaundice indicates underlying conditions like hepatitis, cirrhosis, or gallstones. Metaphorically, it describes cynical, bitter, or prejudiced perspectives, suggesting judgment colored by negative experiences or bias. This figurative usage draws on the visual association between yellow discoloration and seeing things through a "colored" or distorted lens.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'JAWN-dist (emphasis on first syllable)',
                'etymology': 'From "jaundice" + "-ed," where "jaundice" comes from Old French "jaunisse" meaning "yellowness"',
                'memory_tips': 'Think "jaun-diced" - "jaun" sounds like "yawn" (tired and yellow) plus "diced" (cut up by illness)',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'His _____ view of politics made him skeptical of every campaign promise.'
            },
            'javas': {
                'definition': 'Plural form of Java, referring to multiple contexts: the Indonesian island known for dense population and cultural heritage; multiple cups of coffee (slang, as Java produces coffee); or multiple instances of Java programming language applications. Geographically, it could reference multiple Java-like regions. In computing, it refers to multiple Java applications or runtime environments. The island Java hosts over half of Indonesia\'s population, includes major cities like Jakarta, and features important historical sites like Borobudur temple.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'JAH-vuhz (emphasis on first syllable)',
                'etymology': 'Plural of "Java," from Sanskrit "Yavadvipa" meaning "island of barley," referring to the Indonesian island',
                'memory_tips': 'Think "java-s" - multiple cups of Java coffee or multiple Java programs running',
                'alternate_spellings': '',
                'language_origin': 'Sanskrit via Indonesian',
                'example_sentence': 'The programmer had several cups of _____ while debugging multiple applications.'
            },
            'javelin': {
                'definition': 'A light spear designed for throwing in athletic competition or ancient warfare, consisting of a metal head, shaft (metal, carbon fiber, or fiberglass), and grip area. In track and field, athletes sprint down a runway to throw for maximum distance following strict technical rules. The javelin throw is a classic Olympic field event requiring skill, strength, and technique. Historically, javelins were hunting and warfare weapons across many cultures. Modern sporting javelins have undergone design changes for safety and fair competition with specific weight, length, and balance regulations.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JAV-lin (emphasis on first syllable)',
                'etymology': 'From Old French "javeline," diminutive of "javelot" meaning dart or spear',
                'memory_tips': 'Think "jab-elin" - jabbing with a spear like an elf (elin) would throw',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The Olympic athlete threw the _____ over 90 meters to win the gold medal.'
            },
            'jazzy': {
                'definition': 'Having characteristics of jazz music including syncopated rhythms, improvisation, and energetic qualities; or describing something flashy, showy, or stylish in attention-getting ways. In music, it suggests rhythmic complexity, spontaneous creativity, and distinctive swing feel. Broadly, it describes anything with flair, excitement, or sophisticated style in fashion, design, or behavior. The term captures jazz culture\'s influence on creativity, innovation, and dynamic energy, representing originality and verve that stands out from conventional approaches.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'JAZ-ee (emphasis on first syllable)',
                'etymology': 'From "jazz" + suffix "-y," where "jazz" possibly comes from American slang meaning energy or excitement',
                'memory_tips': 'Think "jazz-y" - having the lively, improvisational quality of jazz music',
                'alternate_spellings': '',
                'language_origin': 'American English',
                'example_sentence': 'She wore a _____ outfit with bright colors and bold patterns to the music festival.'
            },
            'jealousy': {
                'definition': 'A complex emotion characterized by insecurity, resentment, and anxiety from perceived threats to valued relationships or comparisons with others possessing desired things. It involves fear of losing someone important combined with anger toward perceived threats. Jealousy manifests in romantic relationships, friendships, family dynamics, and professional settings through cognitive thoughts, emotional feelings, and behavioral actions. While mild jealousy might indicate care, extreme jealousy becomes destructive, leading to controlling behavior and relationship breakdown. Managing it requires self-awareness, communication skills, and emotional regulation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JEL-uh-see (emphasis on first syllable)',
                'etymology': 'From Old French "jalousie," from "jalous" meaning jealous, ultimately from Late Latin "zelosus"',
                'memory_tips': 'Think "jello-ousy" - shaky like jello when envious, plus "ousy" sounds like "ouch-y" (emotionally painful)',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'Professional _____ among colleagues can create a toxic work environment.'
            },
            'jeans': {
                'definition': 'Durable casual trousers made from denim fabric, typically blue from indigo dyeing, originally designed as workwear for miners and laborers in 19th-century America. The fabric features cotton warp threads dyed indigo and white weft threads, creating characteristic blue exterior contrasting with white interior fibers. Modern jeans come in numerous styles, cuts, colors, and treatments from traditional straight-leg to skinny, distressed, and designer variations. Their global popularity represents significant cultural phenomenon, symbolizing American casual culture while being adapted worldwide.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'JEENZ (single syllable)',
                'etymology': 'From "jean," referring to fabric originally from Gênes (Genoa), Italy, with plural form becoming standard',
                'memory_tips': 'Think "Jean-s" - Jean\'s pants became "jeans" for everyone to wear',
                'alternate_spellings': '',
                'language_origin': 'Italian (place name) via French',
                'example_sentence': 'Blue _____ became popular worldwide as both work wear and casual fashion.'
            },
            'jeepney': {
                'definition': 'A distinctive Filipino public transportation vehicle evolved from U.S. military jeeps left after World War II. These colorful, elongated vehicles serve as buses throughout the Philippines, known for vibrant decorations, bright colors, chrome ornaments, religious symbols, and personalized artwork reflecting Filipino culture. They feature bench seating along sides, open-air design for tropical comfort, and unique jeep front with extended passenger compartment. Operating on fixed routes with flexible stops, jeepneys provide affordable transportation for millions daily while representing important Filipino cultural identity and ingenuity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JEEP-nee (emphasis on first syllable)',
                'etymology': 'Compound from "jeep" (military vehicle) + Filipino suffix "ney," created post-WWII from converted surplus jeeps',
                'memory_tips': 'Think "jeep-knee" - a jeep that bends at the knee to hold more passengers',
                'alternate_spellings': '',
                'language_origin': 'Filipino English',
                'example_sentence': 'The brightly painted _____ served as affordable transportation through busy Manila streets.'
            },
            'jelly': {
                'definition': 'A semi-solid, translucent food made by boiling fruit juice with sugar and pectin until gel-like consistency, smoother than jam without fruit pieces. Also refers to gelatin-based desserts, savory aspics, or any gelatinous substance. The preservation process allows fruit flavors to be enjoyed year-round and was historically important before refrigeration. Commercial and homemade varieties include traditional grape and strawberry to exotic tropical fruits. The term describes any substance with similar consistency, including biological materials and petroleum jelly for cosmetic and medical applications.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'JEL-ee (emphasis on first syllable)',
                'etymology': 'From Old French "gelée" meaning frozen or congealed, from Latin "gelare" meaning to freeze',
                'memory_tips': 'Think "gel-ly" - like gel but sweet and wobbly',
                'alternate_spellings': '',
                'language_origin': 'Old French via Latin',
                'example_sentence': 'The homemade grape _____ spread perfectly on warm toast for breakfast.'
            },
            'jeopardy': {
                'definition': 'A state of danger, risk, or uncertainty where someone faces possibility of loss, harm, or failure. In legal contexts, it refers to danger of conviction and punishment in criminal proceedings, leading to "double jeopardy" constitutional protection against being tried twice for the same crime. Generally, being in jeopardy means being in precarious situations where negative consequences are possible or likely, suggesting immediate rather than theoretical threat. Common usage includes situations where jobs, relationships, health, safety, or success are at stake.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JEP-er-dee (emphasis on first syllable)',
                'etymology': 'From Old French "jeu parti" meaning "divided game" or uncertain outcome situation',
                'memory_tips': 'Think "jeop-party" - a party where the outcome is uncertain and risky',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The company\'s financial difficulties put hundreds of jobs in _____.'
            },
            'jerboa': {
                'definition': 'A small, jumping desert rodent of family Dipodidae, characterized by extremely long hind legs, long tufted tail, and large ears adapted for arid environments. Found in African and Asian deserts, they\'ve evolved remarkable adaptations for harsh, dry conditions with limited water sources. These nocturnal animals hop at high speeds like miniature kangaroos, using oversized ears for hearing and heat regulation. They obtain water from food and have highly efficient kidneys. Sandy-colored fur provides camouflage while long tails aid balance during rapid hopping.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jer-BOH-ah (emphasis on second syllable)',
                'etymology': 'From Arabic "yarbu," the native name for these desert rodents',
                'memory_tips': 'Think "jer-boa" - sounds like "jerk-boa" but this one hops quickly instead of slithering',
                'alternate_spellings': '',
                'language_origin': 'Arabic',
                'example_sentence': 'The tiny _____ bounded across desert sand using powerful hind legs like a miniature kangaroo.'
            },
            'jerky': {
                'definition': 'Lean meat cut into strips and dried to remove moisture, creating preserved food storable without refrigeration. Traditional jerky uses salt and natural drying, while modern production includes marinades, spices, and controlled dehydration for enhanced taste and safety. Common varieties include beef, turkey, and exotic game meats. This preservation method dates back thousands of years, essential for early human survival during travel and harsh seasons. As an adjective, jerky describes sudden, irregular movements lacking smoothness or continuity.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'JER-kee (emphasis on first syllable)',
                'etymology': 'From Spanish "charqui," from Quechua "ch\'arki" meaning dried meat',
                'memory_tips': 'Think "jerk-y" - meat that makes your jaw work with jerky chewing motions',
                'alternate_spellings': '',
                'language_origin': 'Quechua via Spanish',
                'example_sentence': 'The hikers packed beef _____ as lightweight, high-protein snack for their expedition.'
            },
            'jersey': {
                'definition': 'A close-fitting pullover shirt made from knitted fabric, commonly worn as athletic wear with team uniforms featuring numbers, names, and logos. The term refers to both the garment and the knitted fabric characterized by stretch properties and comfortable fit, created using processes producing smooth surfaces and looped textures. Beyond sports, jersey material makes casual garments including t-shirts and dresses. The word also refers to Jersey cattle (dairy breed) and the British Crown dependency island where the fabric originated.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JER-zee (emphasis on first syllable)',
                'etymology': 'Named after Isle of Jersey where distinctive knitted fabric was originally produced',
                'memory_tips': 'Think "Jer-sey" - Jer from Jersey island making knitted sports clothing',
                'alternate_spellings': '',
                'language_origin': 'English (place name)',
                'example_sentence': 'The basketball player\'s _____ displayed his number prominently on front and back.'
            },
            'jesuit': {
                'definition': 'A member of the Society of Jesus, a Roman Catholic religious order founded by Saint Ignatius of Loyola in 1540, known for education, missionary work, and intellectual pursuits. Jesuits operate schools, universities, and missions worldwide, playing significant roles in Counter-Reformation, theological scholarship, and scientific research. They take vows of poverty, chastity, obedience, plus special obedience to the Pope regarding missions. Often called "the Pope\'s soldiers," they\'re renowned for academic excellence and commitment to forming students intellectually, spiritually, and ethically according to Catholic principles.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'JEZH-oo-it (emphasis on first syllable)',
                'etymology': 'From "Jesus" + suffix "-uit" meaning "of Jesus," chosen by founder Ignatius of Loyola',
                'memory_tips': 'Think "Jesus-uit" - following Jesus through education and service',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The _____ priest combined rigorous scholarship with deep spiritual commitment in teaching.'
            },
            'jettison': {
                'definition': 'To deliberately throw away, discard, or abandon something, especially in emergencies to reduce weight or eliminate burden. Originating from maritime and aviation contexts where cargo might be thrown overboard or dropped to prevent disaster, it broadly means abandoning plans, ideas, or possessions no longer useful or impeding progress. The action involves conscious sacrifice of potential value for greater benefit or necessity. Businesses might jettison unprofitable divisions; individuals might jettison outdated beliefs. It implies both urgency and calculated decision-making.',
                'part_of_speech': 'verb, noun',
                'pronunciation_guide': 'JET-i-suhn (emphasis on first syllable)',
                'etymology': 'From Old French "getaison," from Latin "jactare" meaning to throw',
                'memory_tips': 'Think "jet-is-on" - when the jet is on, throw out extra weight to survive',
                'alternate_spellings': '',
                'language_origin': 'Old French via Latin',
                'example_sentence': 'The pilot had to _____ cargo to gain altitude to clear the mountain range.'
            },
            'jewel': {
                'definition': 'A precious stone or gem, typically cut and polished for jewelry, or any ornamental object of great beauty and value. Includes gemstones like diamonds, rubies, sapphires, and emeralds prized for rarity, beauty, hardness, and brilliance. Metaphorically refers to anything precious or exceptional. In mechanics, jewels are synthetic gems used as bearings in precision instruments. The cutting and setting requires specialized skills developed into sophisticated art forms. Historically, jewels symbolized wealth, power, and status in royal regalia and ceremonial objects.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'JOO-uhl (emphasis on first syllable)',
                'etymology': 'From Old French "juel," from Latin "jocale" meaning plaything or ornament',
                'memory_tips': 'Think "jew-el" - a precious gem that makes you exclaim "Ooh!" with delight',
                'alternate_spellings': '',
                'language_origin': 'Old French via Latin',
                'example_sentence': 'The crown\'s centerpiece was a magnificent sapphire _____ that sparkled brilliantly.'
            },
            'jibboom': {
                'definition': 'A nautical spar extending forward from the bowsprit of sailing ships to support jib sails and forward sails. This essential rigging component extends the ship\'s sail-carrying capacity forward of the main mast, consisting of sections that can be extended or retracted based on wind conditions and sailing requirements. It works with the bowsprit to create platforms for triangular sails improving ability to sail close to wind. On larger ships, multiple jibbooms including flying jibbooms extend even further forward for optimal sailing performance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JIB-boom (emphasis on first syllable)',
                'etymology': 'Compound word from "jib" (triangular sail) + "boom" (spar or pole)',
                'memory_tips': 'Think "jib-boom" - the boom that holds the jib sail goes boom in the wind',
                'alternate_spellings': '',
                'language_origin': 'English nautical terminology',
                'example_sentence': 'The sailor climbed out on the _____ to secure the jib sail in rough weather.'
            },
            'jicama': {
                'definition': 'A large, turnip-shaped root vegetable native to Mexico and Central America, also known as Mexican turnip or yam bean. It has brown, fibrous exterior skin that\'s inedible, but white, crisp, mildly sweet interior flesh similar to water chestnut texture. This low-calorie vegetable is rich in vitamin C, fiber, and potassium with minimal starch. Eaten raw in salads or as crunchy snacks, often served with lime and chili in Mexican cuisine. It can be cooked but loses characteristic crispness when heated.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HEE-kah-mah (emphasis on first syllable)',
                'etymology': 'From Spanish "jícama," from Nahuatl "xicamatl," the indigenous Mexican name',
                'memory_tips': 'Think "hee-kah-ma" - mama says "hee kah!" when tasting this sweet, crispy root',
                'alternate_spellings': '',
                'language_origin': 'Nahuatl via Spanish',
                'example_sentence': 'The crisp, refreshing _____ added pleasant crunch to the summer salad.'
            },
            'jicarilla': {
                'definition': 'A federally recognized Native American tribe, a subgroup of Apache people primarily in north-central New Mexico. The Jicarilla Apache Nation covers approximately 742,000 acres and is known for traditional basket weaving, pottery, and beadwork. The name means "little basket" in Spanish, referring to their exceptional waterproof basket-making skills. Historically semi-nomadic, they followed seasonal patterns across Great Plains and Southwest regions, combining Plains and Southwestern cultural elements while maintaining cultural identity through language, ceremonies, and traditional arts.',
                'part_of_speech': 'noun, proper noun',
                'pronunciation_guide': 'hee-kah-REE-yah (emphasis on third syllable)',
                'etymology': 'From Spanish "jicarilla," diminutive of "jícara" meaning bowl or cup, from Nahuatl',
                'memory_tips': 'Think "hee-kah-rilla" - small guerrilla warriors known for making strong baskets',
                'alternate_spellings': '',
                'language_origin': 'Spanish via Nahuatl',
                'example_sentence': 'The _____ Apache Nation maintains traditional basket-making while operating modern enterprises.'
            },
            'jiggery': {
                'definition': 'Trickery, deception, or underhanded manipulation involving clever but dishonest schemes or fraudulent practices. The term suggests cunning behavior designed to mislead or cheat others through complex or elaborate methods achieving illegitimate goals. It typically implies sophistication in deceptive practices, going beyond simple lies to calculated manipulation or fraud. The word can describe mysterious or suspicious activity where the exact nature appears questionable. It emphasizes the clever or intricate nature of deception rather than crude dishonesty.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JIG-uh-ree (emphasis on first syllable)',
                'etymology': 'Possibly from "jigger" meaning to manipulate, combined with suffix "-ery" indicating action or practice',
                'memory_tips': 'Think "jig-ery" - dancing around the truth with tricky, deceptive moves',
                'alternate_spellings': '',
                'language_origin': 'English slang',
                'example_sentence': 'The magician\'s _____ made it impossible to detect how he made the coin disappear.'
            },
            'jigsaw': {
                'definition': 'A power tool with thin, reciprocating blade designed for cutting curved lines, intricate patterns, and detailed shapes in wood, metal, and plastic materials. The blade moves up and down rapidly, allowing precise control when following cutting lines or creating freehand curves, making it essential for woodworking and crafting projects. The term also refers to jigsaw puzzles - interlocking pieces forming complete pictures when assembled, ranging from simple children\'s versions to complex adult puzzles with thousands of pieces, named after the original cutting method.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JIG-saw (emphasis on first syllable)',
                'etymology': 'Compound word from "jig" (guide or template) + "saw" (cutting tool)',
                'memory_tips': 'Think "jig-saw" - a saw that can "dance" around curves and intricate cuts',
                'alternate_spellings': '',
                'language_origin': 'English compound',
                'example_sentence': 'She used a _____ to cut decorative curves in the wooden cabinet door.'
            },
            'jimberjawed': {
                'definition': 'Having a protruding or prominent jaw characterized by irregular or asymmetrical jawline extending beyond normal proportions. This descriptive term refers to facial features where the lower jaw projects forward significantly, creating distinctive appearance. The condition can result from natural bone structure variation or developmental factors. Sometimes used broadly to describe anything appearing crooked, askew, or irregularly shaped. While primarily descriptive, it can carry informal connotations about appearance, though jaw prominence is often normal human facial variation.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'JIM-ber-jawd (emphasis on first syllable)',
                'etymology': 'Compound possibly from "jimber" (crooked or askew) + "jawed" (having jaws)',
                'memory_tips': 'Think "jimber-jawed" - Jim has a jaw that juts out like crooked timber',
                'alternate_spellings': '',
                'language_origin': 'English dialect',
                'example_sentence': 'The cartoon character had an exaggerated _____ appearance to emphasize his gruff personality.'
            },
            'jingoism': {
                'definition': 'Extreme patriotism characterized by aggressive foreign policy advocacy, bellicose nationalism, and support for military action against other countries. It goes beyond healthy national pride to embrace antagonistic stances toward other nations, often involving calls for war or military intervention to assert dominance. This ideology includes belief in national superiority, suspicion of international cooperation, and support for expansionist policies. Jingoistic attitudes often emerge during international tension and can influence public opinion toward supporting conflicts when diplomatic solutions might be available.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JING-goh-izm (emphasis on first syllable)',
                'etymology': 'From "jingo" (patriotic slogan) + "-ism," from British music hall song supporting aggressive action',
                'memory_tips': 'Think "jingo-ism" - extreme belief system that goes "by jingo!" for war instead of peace',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The politician\'s _____ appealed to nationalistic feelings but worried diplomats.'
            },
            'jingoismjitney': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "jingoism" (extreme nationalism) + "jitney" (small bus). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing spelling bee word lists, where formatting irregularities cause adjacent words to merge without proper spacing.',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "jingoism" and "jitney"',
                'alternate_spellings': 'jingoism + jitney (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'jinx': {
                'definition': 'A person, thing, or circumstance believed to bring bad luck or cause unfortunate events. The concept involves superstitious beliefs about certain individuals, objects, or situations having power to influence outcomes negatively. As a verb, to jinx means casting bad luck spells or mentioning positive things in ways that might cause them to go wrong. Commonly used in sports where fans avoid saying positive things about team performance for fear of "jinxing" outcomes. While scientifically unfounded, belief in jinxes remains widespread and can influence behavior.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'JINKS (single syllable)',
                'etymology': 'Possibly from Latin "jynx" meaning wryneck bird used in magic, or from "jinks" meaning to dodge',
                'memory_tips': 'Think "jinks" - high jinks (mischief) that bring bad luck and spoil good things',
                'alternate_spellings': '',
                'language_origin': 'Greek via Latin',
                'example_sentence': 'The superstitious athlete believed his old shoes were a _____ after losing three games.'
            },
            'jitney': {
                'definition': 'A small public bus or shared taxi operating on flexible routes, typically charging low fares and providing informal transportation services. Jitneys originated in early 20th century United States as alternatives to expensive streetcars and taxis, offering affordable transportation for working-class passengers. These vehicles usually follow semi-fixed routes but can deviate to pick up and drop off passengers conveniently. The term can also refer to any small coin, particularly a nickel, which was originally the typical fare for jitney rides.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JIT-nee (emphasis on first syllable)',
                'etymology': 'From "jitney" (slang for nickel, five cents), referring to the original small fare charged',
                'memory_tips': 'Think "jit-ney" - a quick (jittery) journey for a nickel',
                'alternate_spellings': '',
                'language_origin': 'American slang',
                'example_sentence': 'The _____ provided affordable transportation between the train station and downtown hotels.'
            },
            'jitterbug': {
                'definition': 'A lively, acrobatic form of swing dance popular in the 1930s and 1940s, characterized by energetic movements, lifts, spins, and jumps performed to big band and swing music. The dance encompasses various swing styles including Lindy Hop and East Coast Swing, emphasizing improvisation and athletic partnering with rapid footwork and dramatic moves requiring significant skill and stamina. It became a cultural phenomenon during the swing era, representing youth culture and musical innovation while serving as social expression during challenging historical periods.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'JIT-er-bug (emphasis on first syllable)',
                'etymology': 'Compound from "jitter" (nervous, shaky movement) + "bug" (enthusiast or affected person)',
                'memory_tips': 'Think "jitter-bug" - a bug that jitters around while dancing energetically',
                'alternate_spellings': '',
                'language_origin': 'American English',
                'example_sentence': 'The couple impressed everyone with their energetic _____ performance to big band music.'
            },
            'jitterbugkennel': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "jitterbug" (swing dance) + "kennel" (dog house). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing spelling bee word lists, where formatting irregularities cause adjacent words to merge without proper spacing.',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "jitterbug" and "kennel"',
                'alternate_spellings': 'jitterbug + kennel (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'joaquin': {
                'definition': 'A Spanish and Portuguese masculine given name equivalent to Joachim in English, commonly used in Hispanic and Latin American cultures. The name has biblical origins, traditionally associated with Saint Joachim, believed father of Virgin Mary in Christian tradition. It carries cultural significance in Spanish-speaking communities, representing connection to Catholic religious traditions and Hispanic heritage. In geographical contexts, it may refer to features named after individuals with this name, such as San Joaquin Valley in California.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'wah-KEEN (Spanish) / joh-uh-KEEN (English)',
                'etymology': 'From Hebrew "Yehoyakim" meaning "God will establish," through Latin "Joachim" and Spanish adaptation',
                'memory_tips': 'Think "wah-keen" - sounds like "walking" but with keen sense of direction',
                'alternate_spellings': 'Joachim',
                'language_origin': 'Hebrew via Spanish',
                'example_sentence': 'The San _____ Valley is one of California\'s most important agricultural regions.'
            },
            'jocote': {
                'definition': 'A small tropical fruit native to Central America and Mexico, scientifically known as Spondias purpurea, also called red mombin, purple mombin, or hog plum. The fruit is oval-shaped with smooth, thin skin ranging from green to yellow, orange, red, or purple when ripe. The flesh is juicy and sweet-tart, surrounding a large seed with tropical flavor profile. Common throughout Central America, it\'s eaten fresh, made into beverages, or used in traditional desserts, rich in vitamin C and antioxidants.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hoh-KOH-teh (emphasis on second syllable)',
                'etymology': 'From Nahuatl "xocotl" meaning fruit, adopted into Spanish',
                'memory_tips': 'Think "ho-ko-te" - "ho, ko!" exclamation when tasting this sweet tropical fruit',
                'alternate_spellings': '',
                'language_origin': 'Nahuatl via Spanish',
                'example_sentence': 'Children in El Salvador often climb trees to pick ripe _____ fruits during summer.'
            },
            'jocularity': {
                'definition': 'The quality of being jocular; humor, jest, or playful behavior characterized by good-natured fun and lightheartedness. It involves tendency to joke, laugh, and engage in witty conversation, often creating pleasant, relaxed atmospheres in social situations. This trait encompasses both ability to appreciate humor and skill to generate amusing remarks. Jocularity differs from sarcasm or mean-spirited humor by aiming to entertain and uplift rather than mock. It can be valuable in leadership, teaching, and social contexts for maintaining morale and engagement.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'jok-yuh-LAR-i-tee (emphasis on third syllable)',
                'etymology': 'From Latin "jocularis" meaning given to jesting, from "jocus" meaning joke',
                'memory_tips': 'Think "joke-ularity" - the quality of making jokes regularly',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The teacher\'s _____ made even difficult lessons enjoyable for students.'
            },
            'jodhpurs': {
                'definition': 'Close-fitting riding pants loose through hips and thighs but tight from knee to ankle, originally designed for horseback riding. They feature distinctive flared cut above the knee narrowing dramatically to fit snugly around lower leg, allowing comfortable wear inside tall riding boots. The design originated in India, adapted by British cavalry officers, becoming standard equestrian attire. Made from stretchy, durable materials providing freedom of movement while maintaining sleek appearance, often featuring reinforced inner leg panels to prevent wear from stirrup contact.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'JOD-perz (emphasis on first syllable)',
                'etymology': 'Named after Jodhpur, a city in India where this riding breeches style originated',
                'memory_tips': 'Think "Jod-purs" - pants that purr like a cat when you ride from Jodhpur',
                'alternate_spellings': '',
                'language_origin': 'Place name (Hindi)',
                'example_sentence': 'The equestrian wore traditional _____ and tall boots for the horse show competition.'
            },
            'jody': {
                'definition': 'In military slang, a term referring to the civilian man who stays home while soldiers are deployed, often implying he might steal affections of servicemen\'s girlfriends or wives. The concept represents fears and anxieties of deployed personnel about what might happen in their absence. Jody calls or cadences are rhythmic chants used during military training and marching, serving both as motivation and ways to express deployment concerns. As a proper name, Jody is used for both masculine and feminine names in American culture.',
                'part_of_speech': 'noun, proper noun',
                'pronunciation_guide': 'JOH-dee (emphasis on first syllable)',
                'etymology': 'Origin uncertain in military context, possibly from "Joe"; as personal name, diminutive of various names',
                'memory_tips': 'Think "Jody" - the person everyone sings about while marching',
                'alternate_spellings': 'Jodie',
                'language_origin': 'American military slang',
                'example_sentence': 'The drill sergeant called out a _____ cadence to keep soldiers marching in rhythm.'
            },
            'joggled': {
                'definition': 'Past tense of joggle, meaning to shake or move with slight, irregular motions; to bump or jar gently and repeatedly. Joggling describes continuous, mild shaking or vibrating action causing something to move in jerky, unsteady manner. The motion is typically not violent but persistent enough to be noticeable and potentially disruptive. In construction, joggle can refer to specific joint types where pieces fit together with notches, and "joggled" describes something constructed with such joints.',
                'part_of_speech': 'verb (past tense)',
                'pronunciation_guide': 'JOG-uhld (emphasis on first syllable)',
                'etymology': 'Past tense of "joggle," frequentative form of "jog" meaning to shake with small repeated motions',
                'memory_tips': 'Think "jog-gled" - giggled while jogging with quick, bouncing movements',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The rough road _____ the passengers in the old bus for the entire journey.'
            },
            'john': {
                'definition': 'A common masculine given name of Hebrew origin, one of the most popular names in English-speaking cultures throughout history, with numerous variations across languages and cultures including Juan, Jean, Johann, and Giovanni. The name has biblical significance, associated with John the Baptist and John the Apostle. In colloquial usage, "john" can refer to a toilet or bathroom. Its prevalence has made it synonymous with the "common man" or "everyman" in various cultural expressions like "John Doe."',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'JON (single syllable)',
                'etymology': 'From Hebrew "Yohanan" meaning "God is gracious," through Greek, Latin, and Old French',
                'memory_tips': 'Think "John" - one of the most common names meaning "God is gracious"',
                'alternate_spellings': 'Jon',
                'language_origin': 'Hebrew',
                'example_sentence': 'The public restroom sign simply read "\_\_\_\_\_" above the men\'s door.'
            },
            'johnson': {
                'definition': 'A patronymic surname meaning "son of John," one of the most common surnames in English-speaking countries following traditional English pattern of adding "-son" to father\'s name. The name\'s ubiquity stems from popularity of the given name John, making it representative of typical American family names. Due to its frequency, Johnson often requires additional identifiers to distinguish between individuals. The surname has various spelling alternatives including Johnston and appears frequently in American history and culture through numerous notable figures.',
                'part_of_speech': 'proper noun (surname)',
                'pronunciation_guide': 'JON-suhn (emphasis on first syllable)',
                'etymology': 'Patronymic surname from "John\'s son," literally meaning "son of John"',
                'memory_tips': 'Think "John-son" - literally "John\'s son" following patronymic naming patterns',
                'alternate_spellings': 'Johnston',
                'language_origin': 'English patronymic',
                'example_sentence': 'President _____ signed the Civil Rights Act into law in 1964.'
            },
            'joie': {
                'definition': 'A French word meaning joy, happiness, or delight, commonly encountered in English through the phrase "joie de vivre" (joy of living). Joie represents more than simple happiness, conveying exuberant enjoyment and zest for existence. The concept encompasses appreciation for life\'s pleasures, optimistic outlook, and ability to find satisfaction in everyday experiences. This French cultural philosophy emphasizes living fully, appreciating beauty, savoring experiences, and maintaining positive attitude despite challenges, representing balance between responsibility and pursuit of happiness.',
                'part_of_speech': 'noun (French)',
                'pronunciation_guide': 'ZHWAH (French) / JOY (anglicized)',
                'etymology': 'From Old French "joie," from Latin "gaudia" meaning joy or gladness',
                'memory_tips': 'Think "joie" - sounds like "joy" in English, and that\'s exactly what it means in French',
                'alternate_spellings': '',
                'language_origin': 'French via Latin',
                'example_sentence': 'Her _____ de vivre was infectious, brightening everyone\'s mood at the party.'
            },
            'join': {
                'definition': 'To connect, unite, or bring together two or more things, people, or concepts into a single entity or group. Join describes physical actions like connecting materials or assembling components, and social meanings like becoming group members or participating in activities. In relationships, it suggests partnership, collaboration, or coming together for mutual benefit. The word implies conscious decision to become part of something larger or create connections where none existed, involving commitment and being fundamental to human cooperation and community building.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'JOYN (single syllable)',
                'etymology': 'From Old French "joindre," from Latin "jungere" meaning to yoke or bind together',
                'memory_tips': 'Think "join" - like linking hands to join together with others',
                'alternate_spellings': '',
                'language_origin': 'Old French via Latin',
                'example_sentence': 'Please _____ us for dinner tonight at the new restaurant downtown.'
            },
            'joinery': {
                'definition': 'The craft or trade of constructing wooden joints and assembling wooden components into furniture, buildings, or other structures without using nails, screws, or metal fasteners. Joinery relies on precisely cut interlocking joints like dovetails, mortise and tenon, and finger joints to create strong, durable connections. This traditional building technique has been practiced for thousands of years, valued for strength, beauty, and longevity. Master joiners possess deep knowledge of wood properties, joint geometry, and construction techniques for complex wooden structures.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JOYN-uh-ree (emphasis on first syllable)',
                'etymology': 'From "join" + suffix "-ery" indicating place of work or craft',
                'memory_tips': 'Think "join-ery" - the craft of joining wood pieces together expertly without nails',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The master craftsman\'s _____ skills were evident in the perfectly fitted cabinet doors.'
            },
            'joists': {
                'definition': 'Horizontal structural beams running parallel to each other that support floors, ceilings, or roofs in building construction. Typically made from wood, steel, or engineered materials, joists are designed to bear loads and transfer weight to main support beams or walls. In residential construction, floor joists create frameworks for subfloors and finish floors, while ceiling joists support ceiling materials. Proper joist installation is crucial for structural integrity and preventing sagging. Different types include solid wood joists, I-joists, and steel joists.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'JOYSTS (single syllable)',
                'etymology': 'From Old French "giste" meaning "beam on which something rests"',
                'memory_tips': 'Think "joists" - sounds like "hoists" because they hoist up and support floors',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The contractor inspected the floor _____ to ensure they could support the kitchen island weight.'
            },
            'jolly': {
                'definition': 'Cheerful, merry, and good-humored; characterized by happiness, friendliness, and upbeat disposition. A jolly person displays infectious enthusiasm, laughs easily, and spreads positive feelings to others. The word suggests not just happiness but robust, hearty cheerfulness often associated with celebration, festivity, and social enjoyment. It can describe both temporary moods and permanent personality traits, indicating someone who approaches life with optimism and finds reasons to be pleased in ordinary circumstances.',
                'part_of_speech': 'adjective, adverb',
                'pronunciation_guide': 'JOL-ee (emphasis on first syllable)',
                'etymology': 'From Old French "joli" meaning pretty or pleasant, evolving to emphasize cheerfulness over physical attractiveness',
                'memory_tips': 'Think "jolly" - so happy you jolt with laughter, like jolly old Saint Nicholas',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The _____ shopkeeper always greeted customers with warm smiles and friendly conversation.'
            },
            'jonquil': {
                'definition': 'A type of narcissus flower, specifically Narcissus jonquilla, characterized by small, fragrant, bright yellow blooms with sweet scent and narrow, rush-like leaves. These spring-flowering bulbous plants are native to Spain and Portugal but widely cultivated in temperate gardens. Flowers typically appear in clusters of 2-6 blooms per stem with six petals surrounding small central cups. Distinguished from other daffodils by distinctive fragrance, smaller size, and multiple flowers per stem, jonquils prefer well-drained soil and are valued for ornamental beauty and sweet perfume.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JON-kwil (emphasis on first syllable)',
                'etymology': 'From Spanish "junquillo," diminutive of "junco" meaning rush, referring to narrow, rush-like leaves',
                'memory_tips': 'Think "John-quill" - John\'s quill pen shaped like a narrow-leafed flower',
                'alternate_spellings': '',
                'language_origin': 'Spanish via French',
                'example_sentence': 'The garden was filled with sweet fragrance of blooming _____ flowers in early spring.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_095_data:
            return batch_095_data[word_lower]
        
        # Return empty data if word not found
        return {
            'definition': '',
            'part_of_speech': '',
            'pronunciation_guide': '',
            'etymology': '',
            'memory_tips': '',
            'alternate_spellings': '',
            'language_origin': '',
            'example_sentence': ''
        }
    
    def process_batch_095(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 095 with comprehensive Claude data"""
        words = []
        with open(input_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word_data = WordData(
                    word=row['word'],
                    years=row['years'],
                    source_files=row['source_files'],
                    source_difficulties=row['source_difficulties']
                )
                
                # Get comprehensive Claude data
                claude_data = self.get_comprehensive_claude_data(word_data.word)
                
                # Store all Claude-generated data
                word_data.claude_definition = claude_data['definition']
                word_data.part_of_speech = claude_data['part_of_speech']
                word_data.pronunciation_guide = claude_data['pronunciation_guide']
                word_data.claude_etymology = claude_data['etymology']
                word_data.memory_tips = claude_data['memory_tips']
                word_data.alternate_spellings = claude_data['alternate_spellings']
                word_data.claude_language_origin = claude_data['language_origin']
                word_data.example_sentence = claude_data['example_sentence']
                
                # Track any missing data
                errors = []
                if not word_data.claude_definition:
                    errors.append("No Claude definition available")
                if not word_data.pronunciation_guide:
                    errors.append("No pronunciation guide available")
                if not word_data.claude_etymology:
                    errors.append("No etymology available")
                
                word_data.error_notes = "; ".join(errors)
                
                words.append(word_data)
                logger.info(f"Processed word: {word_data.word}")
        
        return words
    
    def save_batch_095_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 095 processed words to CSV"""
        
        # Match actual database schema
        fieldnames = [
            'word', 'definition', 'example_sentence', 'source_difficulty', 
            'difficulty_level', 'difficulty_name', 'ai_difficulty_level', 'ai_difficulty_name',
            'phonetic_transparency_score', 'word_frequency_score', 'morphology_score', 
            'etymology_score', 'difficulty_calculation_method', 'part_of_speech',
            'pronunciation_guide', 'etymology', 'etymology_source', 'memory_tips',
            'alternate_spellings', 'language_origin', 'definition_source',
            'source_names', 'source_difficulties', 'frequency', 'original_source',
            'source_access_date'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for word_data in processed_words:
                # Calculate difficulty components (but don't assign final difficulty yet)
                calc = self.difficulty_calculator
                phonetic_score = calc.calculate_phonetic_transparency(word_data.word, word_data.pronunciation_guide)
                frequency_score = calc.calculate_word_frequency(word_data.word)
                morphology_score = calc.calculate_morphological_complexity(word_data.word, word_data.claude_etymology)
                etymology_score = calc.calculate_etymology_complexity(word_data.claude_etymology, word_data.claude_language_origin)
                
                # Calculate overall score but don't assign difficulty level yet
                overall_score = (phonetic_score * 0.3 + frequency_score * 0.25 + morphology_score * 0.25 + etymology_score * 0.2)
                
                # Create detailed original source with years
                years_list = word_data.years.replace(';', ',') if word_data.years else ''
                original_source = f"Scripps National Spelling Bee Words of the Champions ({years_list})" if years_list else 'Scripps National Spelling Bee Words of the Champions'
                
                row = {
                    'word': word_data.word,
                    'definition': word_data.claude_definition,
                    'example_sentence': word_data.example_sentence,
                    'source_difficulty': word_data.source_difficulties.split(';')[0].strip() if word_data.source_difficulties else '',
                    'difficulty_level': '',
                    'difficulty_name': '',
                    'ai_difficulty_level': '',
                    'ai_difficulty_name': '',
                    'phonetic_transparency_score': phonetic_score,
                    'word_frequency_score': frequency_score,
                    'morphology_score': morphology_score,
                    'etymology_score': etymology_score,
                    'difficulty_calculation_method': f'4-factor weighted model (overall_score: {overall_score:.2f})',
                    'part_of_speech': word_data.part_of_speech,
                    'pronunciation_guide': word_data.pronunciation_guide,
                    'etymology': word_data.claude_etymology,
                    'etymology_source': 'Claude',
                    'memory_tips': word_data.memory_tips,
                    'alternate_spellings': word_data.alternate_spellings,
                    'language_origin': word_data.claude_language_origin,
                    'definition_source': 'Claude',
                    'source_names': 'Scripps National Spelling Bee',
                    'source_difficulties': word_data.source_difficulties,
                    'frequency': frequency_score,
                    'original_source': original_source,
                    'source_access_date': '2025-08-19'
                }
                writer.writerow(row)
        
        logger.info(f"Saved {len(processed_words)} words to {output_file}")

def main():
    """Process Batch 095 with comprehensive Claude data"""
    processor = Batch095Processor()
    input_csv = Path("output/batch_095_words.csv")
    output_csv = Path("output/batch_095_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 095 with comprehensive Claude data...")
    
    # Process all words in batch 095
    processed_words = processor.process_batch_095(input_csv)
    
    # Save results
    processor.save_batch_095_csv(processed_words, output_csv)
    
    logger.info(f"Batch 095 processing completed!")
    logger.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
    logger.info(f"Output saved to: {output_csv}")
    
    # Show summary
    successful_words = [w for w in processed_words if w.claude_definition]
    failed_words = [w for w in processed_words if not w.claude_definition]
    
    logger.info(f"Results: {len(successful_words)} successful, {len(failed_words)} failed")
    
    if failed_words:
        logger.info("Words that failed processing:")
        for word in failed_words:
            logger.info(f"  - {word.word}: {word.error_notes}")

if __name__ == "__main__":
    main()