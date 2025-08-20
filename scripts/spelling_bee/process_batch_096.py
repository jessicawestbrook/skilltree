#!/usr/bin/env python3
"""
Process Batch 096 of Spelling Bee Words with Comprehensive Claude Data
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

class Batch096Processor:
    """Processes Batch 096 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive Claude data for Batch 096 words"""
        
        # Comprehensive data for all 50 words in Batch 096
        batch_096_data = {
            'joropo': {
                'definition': 'A traditional Venezuelan folk dance and musical genre, characterized by fast-paced harp music, cuatro guitar, and maracas, performed at festivals and social gatherings. This energetic dance features couples moving in intricate patterns with rapid footwork, heel-tapping, and synchronized movements reflecting rural Colombian and Venezuelan culture. The joropo encompasses different regional styles including llanero joropo from the plains and tuyero joropo from central regions. It serves as an important cultural expression representing national identity, featuring call-and-response singing with lyrics about rural life, love, and nature.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hoh-ROH-poh (emphasis on second syllable)',
                'etymology': 'From Spanish "joropo," possibly from Arabic "sharab" meaning drink, referring to festive gatherings',
                'memory_tips': 'Think "ho-rope-oh" - dancers move like they\'re jumping rope with lively "oh!" exclamations',
                'alternate_spellings': '',
                'language_origin': 'Spanish',
                'example_sentence': 'The festival featured traditional _____ dancers accompanied by harp and cuatro musicians.'
            },
            'joule': {
                'definition': 'The standard unit of energy in the International System of Units, equal to the work done when a force of one newton acts through a distance of one meter. Named after English physicist James Prescott Joule, it measures energy, work, and heat in physics and engineering. One joule equals the energy expended in applying one newton of force over one meter of distance, or the energy dissipated as heat by one ampere of electric current flowing through one ohm of resistance for one second. This fundamental unit connects mechanical, electrical, and thermal energy measurements.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JOOL (single syllable, rhymes with "pool")',
                'etymology': 'Named after James Prescott Joule (1818-1889), English physicist who studied energy relationships',
                'memory_tips': 'Think "jewel" - energy is precious like a jewel, and both sound similar',
                'alternate_spellings': '',
                'language_origin': 'English (eponym)',
                'example_sentence': 'The battery stored 3600 _____ of electrical energy for the portable device.'
            },
            'jour': {
                'definition': 'French word meaning "day," commonly used in English phrases like "soup du jour" (soup of the day) and "plat du jour" (dish of the day). In journalism and publishing, it appears in compound terms describing daily publications or current events. The word represents the concept of daily occurrence, current happenings, or things that change each day. In legal contexts, it may appear in phrases describing daily proceedings or contemporary issues.',
                'part_of_speech': 'noun (French)',
                'pronunciation_guide': 'ZHOOR (French) / ZHOOR or JOR (anglicized)',
                'etymology': 'From Latin "diurnus" meaning "of the day," through Old French "jor"',
                'memory_tips': 'Think "journey" - both start with "jour" and involve daily travel through time',
                'alternate_spellings': '',
                'language_origin': 'French via Latin',
                'example_sentence': 'The restaurant\'s soup du _____ featured locally sourced vegetables.'
            },
            'journal': {
                'definition': 'A daily record of personal experiences, thoughts, and observations; a periodical publication containing articles on specialized subjects; or an official record of proceedings. Personal journals serve as private reflections and memory preservation, while academic journals publish research findings. Business journals track transactions and financial activities. The practice of journaling promotes self-reflection, emotional processing, and historical documentation, serving both personal development and scholarly communication purposes.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'JER-nuhl (emphasis on first syllable)',
                'etymology': 'From Old French "journal" meaning "daily," from Latin "diurnalis"',
                'memory_tips': 'Think "journey-all" - recording the journey of all daily experiences',
                'alternate_spellings': '',
                'language_origin': 'Old French via Latin',
                'example_sentence': 'She wrote in her personal _____ every evening to reflect on the day\'s events.'
            },
            'journalism': {
                'definition': 'The profession of gathering, writing, editing, and presenting news and information to the public through various media including newspapers, television, radio, and digital platforms. Modern journalism encompasses investigative reporting, breaking news coverage, feature writing, and multimedia storytelling. Ethical journalism follows principles of accuracy, fairness, independence, and accountability while serving the public interest. The field has evolved with technology, adapting to social media, podcasting, and citizen journalism while maintaining core standards of verification and objectivity.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JER-nuh-lizm (emphasis on first syllable)',
                'etymology': 'From "journal" + suffix "-ism," indicating the practice or profession of daily news reporting',
                'memory_tips': 'Think "journal-ism" - the practice of keeping society\'s daily journal',
                'alternate_spellings': '',
                'language_origin': 'English formation',
                'example_sentence': 'Digital _____ has transformed how news is reported and consumed in the modern era.'
            },
            'journey': {
                'definition': 'An act of traveling from one place to another, typically over a considerable distance; a process of personal development or change over time. Physical journeys involve movement through space, while metaphorical journeys represent life experiences, learning processes, or spiritual growth. The concept encompasses both the destination and the experiences encountered along the way. Journeys can be planned expeditions, unexpected adventures, or internal transformations that shape character and perspective.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'JER-nee (emphasis on first syllable)',
                'etymology': 'From Old French "jornee" meaning "day\'s work or travel," from "jor" (day)',
                'memory_tips': 'Think "jour-ney" - originally meant a day\'s travel, like attorney means one who acts for another',
                'alternate_spellings': '',
                'language_origin': 'Old French',
                'example_sentence': 'The family\'s cross-country _____ created lasting memories and strengthened their bonds.'
            },
            'joyful': {
                'definition': 'Characterized by great happiness, delight, or pleasure; expressing or causing joy. Joyful describes both internal emotional states and external expressions of happiness, including smiles, laughter, and celebratory behavior. The word suggests more than temporary happiness, implying deep satisfaction and positive energy that radiates to others. Joyful experiences often involve accomplishments, relationships, beauty, or spiritual fulfillment that create lasting positive memories and emotional resonance.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'JOY-fuhl (emphasis on first syllable)',
                'etymology': 'From "joy" + suffix "-ful" meaning "full of," indicating abundant happiness',
                'memory_tips': 'Think "joy-full" - completely filled with joy like a full cup',
                'alternate_spellings': '',
                'language_origin': 'English',
                'example_sentence': 'The wedding ceremony was a _____ celebration filled with laughter and tears of happiness.'
            },
            'jubilant': {
                'definition': 'Extremely happy and triumphant, especially as a result of success or victory; expressing great joy and celebration. Jubilant describes the elated feeling following achievements, wins, or positive outcomes. The emotion goes beyond simple happiness to include feelings of triumph, vindication, and communal celebration. Jubilant responses often involve public expressions of joy including cheering, dancing, or other demonstrative behaviors that share happiness with others.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'JOO-buh-luhnt (emphasis on first syllable)',
                'etymology': 'From Latin "jubilant" meaning "shouting for joy," from "jubilare" (to shout)',
                'memory_tips': 'Think "jubilee-ant" - like an ant celebrating at a jubilee festival',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The team was _____ after winning the championship game in overtime.'
            },
            'jubilantdifficulty': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "jubilant" (extremely happy) + "difficulty" (challenge or problem). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing spelling bee word lists, where formatting irregularities cause adjacent words to merge without proper spacing.',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "jubilant" and "difficulty"',
                'alternate_spellings': 'jubilant + difficulty (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'judaism': {
                'definition': 'One of the world\'s oldest monotheistic religions, characterized by belief in one God, adherence to Torah teachings, and rich traditions spanning over 3,500 years. Judaism encompasses religious practices, cultural identity, and ethical teachings including the Ten Commandments and emphasis on education, social justice, and community responsibility. The religion includes various movements from Orthodox to Reform, united by shared history, texts, and covenant with God. Jewish observances include Sabbath, holidays like Passover and Yom Kippur, and life-cycle events.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JOO-day-izm (emphasis on first syllable)',
                'etymology': 'From "Judah" (biblical patriarch) + suffix "-ism," referring to the religion of the Jewish people',
                'memory_tips': 'Think "Judah-ism" - the faith tradition originating from the tribe of Judah',
                'alternate_spellings': '',
                'language_origin': 'Hebrew via Greek and Latin',
                'example_sentence': 'The study of _____ includes learning about ancient texts, modern practices, and cultural traditions.'
            },
            'judicious': {
                'definition': 'Showing good judgment and wisdom in decisions; characterized by careful consideration and sound reasoning. Judicious behavior involves weighing options thoughtfully, considering consequences, and making choices based on evidence and experience rather than emotion or impulse. The quality encompasses both practical wisdom and ethical consideration, leading to decisions that are fair, reasonable, and beneficial. Judicious people are often sought as advisors because of their balanced perspective and reliable judgment.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'joo-DISH-uhs (emphasis on second syllable)',
                'etymology': 'From Latin "judiciosus" meaning "having sound judgment," from "judicium" (judgment)',
                'memory_tips': 'Think "judge-icious" - like a wise judge making careful decisions',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Her _____ investment strategy helped preserve wealth during economic uncertainty.'
            },
            'judoka': {
                'definition': 'A person who practices judo, the Japanese martial art emphasizing throws, grappling, and submission techniques. Judoka train in physical technique, mental discipline, and philosophical principles including respect, courtesy, and continuous self-improvement. The practice involves learning to use an opponent\'s force and momentum rather than opposing it directly. Competitive judoka participate in tournaments following international rules, while recreational practitioners focus on fitness, self-defense, and personal development through this traditional martial way.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'joo-DOH-kah (emphasis on second syllable)',
                'etymology': 'From Japanese "judo" (gentle way) + "ka" (person who practices)',
                'memory_tips': 'Think "judo-ka" - a person (ka) who does judo',
                'alternate_spellings': '',
                'language_origin': 'Japanese',
                'example_sentence': 'The experienced _____ demonstrated proper throwing technique to the beginning students.'
            },
            'jugular': {
                'definition': 'Relating to the major veins in the neck that return deoxygenated blood from the head and brain to the heart; specifically the internal and external jugular veins. The jugular vein system is crucial for circulation, carrying blood from the brain, face, and neck regions. In medical contexts, jugular veins are important for assessing cardiovascular health and central venous pressure. The term is often used metaphorically to describe vulnerable points or critical weak spots in systems or arguments.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'JUG-yuh-ler (emphasis on first syllable)',
                'etymology': 'From Latin "jugularis" meaning "of the throat," from "jugulum" (throat, collarbone)',
                'memory_tips': 'Think "jug-ular" - like a jug at the throat carrying blood',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The doctor checked the _____ vein for signs of increased pressure.'
            },
            'juice': {
                'definition': 'The liquid extracted from fruits or vegetables; bodily fluids; electrical power; or influence and power in social contexts. Fruit juices provide vitamins and natural sugars, while vegetable juices offer nutrients and health benefits. In slang, "juice" can refer to electrical power, social influence, or energy. The extraction process concentrates flavors and nutrients, though it often removes beneficial fiber. Commercial juices range from pure extracts to diluted beverages with added ingredients.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'JOOS (single syllable, rhymes with "goose")',
                'etymology': 'From Old French "jus" meaning "broth, liquid," from Latin "jus"',
                'memory_tips': 'Think "juice" sounds like "Zeus" - both have power (electrical vs. divine)',
                'alternate_spellings': '',
                'language_origin': 'Old French via Latin',
                'example_sentence': 'Fresh orange _____ provided vitamin C and natural energy for breakfast.'
            },
            'julienne': {
                'definition': 'A culinary knife technique producing thin, matchstick-shaped strips of vegetables or fruits, typically 2-3 millimeters wide and 4-5 centimeters long. This French cooking method creates uniform pieces that cook evenly and provide elegant presentation in salads, soups, and garnishes. The technique requires sharp knives and consistent cutting skills to achieve professional results. Julienne cuts enhance both visual appeal and texture in dishes, allowing ingredients to integrate better while maintaining distinct flavors.',
                'part_of_speech': 'noun, verb, adjective',
                'pronunciation_guide': 'joo-lee-EN (emphasis on third syllable)',
                'etymology': 'From French "julienne," possibly named after a chef named Jules or from "juli" meaning "July"',
                'memory_tips': 'Think "Julie-Anne" cutting vegetables into thin strips for her cooking show',
                'alternate_spellings': '',
                'language_origin': 'French',
                'example_sentence': 'The chef prepared _____ vegetables as a colorful garnish for the soup.'
            },
            'julius': {
                'definition': 'A masculine given name of Roman origin, historically significant as the name of Julius Caesar and other prominent Roman figures. The name carries connotations of leadership, power, and classical heritage. In modern usage, it remains popular across many cultures with variations including Jules, Julian, and Julio. The name\'s association with July (named after Julius Caesar) connects it to summer, growth, and imperial authority in Western cultural consciousness.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'JOO-lee-uhs (emphasis on first syllable)',
                'etymology': 'From Roman family name "Julius," possibly meaning "descended from Jove" or "youthful"',
                'memory_tips': 'Think "July-us" - Julius Caesar gave his name to the month of July',
                'alternate_spellings': 'Jules, Julian, Julio',
                'language_origin': 'Latin',
                'example_sentence': '_____ Caesar crossed the Rubicon River, changing Roman history forever.'
            },
            'july': {
                'definition': 'The seventh month of the year in the Gregorian calendar, containing 31 days and named after Julius Caesar. In the Northern Hemisphere, July represents peak summer with long days, warm weather, and abundant sunshine. The month features important celebrations including Independence Day in the United States and Canada Day. Agricultural activities include harvesting summer crops and enjoying peak growing season. Cultural associations include vacations, outdoor activities, and summer festivals worldwide.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'juh-LY (emphasis on second syllable)',
                'etymology': 'Named after Julius Caesar by Mark Antony, originally called "Quinctilis" (fifth month)',
                'memory_tips': 'Think "July-us Caesar" - the month named after Julius Caesar',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Many families take vacations during _____ to enjoy the warm summer weather.'
            },
            'jumada': {
                'definition': 'The name of two months in the Islamic lunar calendar: Jumada al-Awwal (first Jumada) and Jumada al-Akhirah (second Jumada), representing the fifth and sixth months respectively. These months traditionally fell during dry seasons when water was scarce and travel was difficult. The name relates to the Arabic root meaning "dry" or "parched." Islamic calendar months are based on lunar cycles, making their relationship to Gregorian calendar months variable.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'joo-MAH-dah (emphasis on second syllable)',
                'etymology': 'From Arabic "jamada" meaning "to freeze" or "to be dry," referring to seasonal conditions',
                'memory_tips': 'Think "ju-mad-a" - sounds like "you made a" dry month',
                'alternate_spellings': 'Jamada',
                'language_origin': 'Arabic',
                'example_sentence': 'The Islamic month of _____ al-Awwal marks an important period in the lunar calendar.'
            },
            'jumbled': {
                'definition': 'Mixed up in a confused or disorderly way; tangled or muddled together without clear organization. Jumbled describes physical arrangements where items lack order, as well as mental states involving confused thoughts or unclear communication. The condition results from hasty organization, accidental mixing, or intentional scrambling. Jumbled items often require sorting, untangling, or reorganizing to restore functionality and comprehension.',
                'part_of_speech': 'adjective, verb (past tense)',
                'pronunciation_guide': 'JUM-buhld (emphasis on first syllable)',
                'etymology': 'Past tense of "jumble," possibly from Middle English "jomblen" meaning "to move confusedly"',
                'memory_tips': 'Think "jump-bled" - things that jumped around and got mixed up',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The _____ papers on his desk made it impossible to find important documents.'
            },
            'jumbo': {
                'definition': 'Extremely large in size; much bigger than usual or standard. Originally referring to a famous circus elephant named Jumbo in the 1880s, the term now describes oversized versions of products, animals, or objects. Common usage includes jumbo jets (large aircraft), jumbo shrimp (large shrimp), and jumbo-sized portions. The word suggests impressive scale that exceeds normal expectations, often implying both size and enhanced capacity or impact.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'JUM-boh (emphasis on first syllable)',
                'etymology': 'From Jumbo, a famous circus elephant (1861-1885), possibly from West African word for "elephant"',
                'memory_tips': 'Think "jump-bo" - so big it could jump over buildings like a superhero',
                'alternate_spellings': '',
                'language_origin': 'English (from African origin)',
                'example_sentence': 'The airline\'s _____ jet could carry over 400 passengers across the ocean.'
            },
            'jumping': {
                'definition': 'The action of propelling oneself upward or forward by pushing off from a surface using leg muscles; moving suddenly or energetically. Jumping serves various purposes including locomotion, exercise, sport, and play. Athletic jumping includes high jump, long jump, and pole vault, each requiring specific techniques and training. The motion involves coordinated muscle contraction, timing, and balance to achieve desired height, distance, or precision.',
                'part_of_speech': 'verb (present participle), noun, adjective',
                'pronunciation_guide': 'JUM-ping (emphasis on first syllable)',
                'etymology': 'From Middle English "jumpen," possibly from Middle Low German or imitative origin',
                'memory_tips': 'Think "jump-ing" - the continuous action of making jumps',
                'alternate_spellings': '',
                'language_origin': 'Middle English',
                'example_sentence': 'The children were _____ rope in the playground during recess.'
            },
            'juncture': {
                'definition': 'A particular point in time or development, especially one at which different possibilities arise; a place where things join or meet. Critical junctures often involve decision-making moments that influence future outcomes. The term applies to both temporal situations (moments of choice) and physical locations (joints, connections). In various contexts, junctures represent transition points, convergence zones, or pivotal moments requiring careful consideration and action.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JUNK-cher (emphasis on first syllable)',
                'etymology': 'From Latin "junctura" meaning "a joining," from "jungere" (to join)',
                'memory_tips': 'Think "junction-ure" - like a junction where paths meet at a crucial point',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'At this critical _____ in her career, she must decide between two job offers.'
            },
            'june': {
                'definition': 'The sixth month of the year in the Gregorian calendar, containing 30 days and traditionally associated with weddings, graduations, and the beginning of summer in the Northern Hemisphere. Named after the Roman goddess Juno, protector of marriage and family. June features the summer solstice (longest day) and optimal weather for outdoor activities. Cultural significance includes graduation ceremonies, wedding season, and Father\'s Day celebrations in many countries.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'JOON (single syllable, rhymes with "moon")',
                'etymology': 'Named after Juno, Roman goddess of marriage and protector of women',
                'memory_tips': 'Think "June-o" - named after Juno, goddess of marriage (hence June weddings)',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'Many couples choose _____ for their wedding because of the pleasant weather and beautiful flowers.'
            },
            'juneteenth': {
                'definition': 'A U.S. federal holiday commemorating June 19, 1865, when news of the Emancipation Proclamation finally reached enslaved people in Texas, effectively ending slavery throughout the former Confederacy. Also called Freedom Day, Jubilee Day, or Liberation Day, it celebrates African American freedom and achievement while acknowledging the historical struggles against slavery and racial inequality. The holiday combines "June" and "nineteenth" to mark this significant date in American civil rights history.',
                'part_of_speech': 'noun (proper noun)',
                'pronunciation_guide': 'JOON-teenth (emphasis on first syllable)',
                'etymology': 'Compound of "June" + "nineteenth," referring to June 19, 1865',
                'memory_tips': 'Think "June-nineteenth" - celebrating freedom on June 19th',
                'alternate_spellings': 'June 19th',
                'language_origin': 'American English',
                'example_sentence': '_____ became a federal holiday in 2021, recognizing the end of slavery in the United States.'
            },
            'jungian': {
                'definition': 'Relating to Carl Gustav Jung (1875-1961) or his theories of analytical psychology, including concepts of the collective unconscious, archetypes, psychological types, and individuation. Jungian psychology emphasizes the integration of conscious and unconscious elements of the psyche through dream analysis, active imagination, and understanding symbolic content. The approach differs from Freudian psychoanalysis by focusing on spiritual and creative aspects of human development rather than primarily sexual motivations.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'YOONG-ee-uhn (emphasis on first syllable)',
                'etymology': 'From Carl Jung + suffix "-ian" indicating relation to or following the theories of Jung',
                'memory_tips': 'Think "Young-ian" - though Jung wasn\'t young, his ideas were groundbreaking',
                'alternate_spellings': '',
                'language_origin': 'English (from German surname)',
                'example_sentence': 'The therapist used _____ dream analysis to help the patient understand recurring symbols.'
            },
            'junior': {
                'definition': 'Lower in rank, status, or age; designed for younger people; a person of lesser experience or authority. In names, "junior" indicates a son with the same name as his father. Academic contexts use junior to describe third-year students or lower-level courses. Professional settings apply the term to entry-level positions or employees with less experience. The designation implies apprenticeship, learning, or developmental stage within hierarchical systems.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'JOON-yer (emphasis on first syllable)',
                'etymology': 'From Latin "junior" meaning "younger," comparative form of "juvenis" (young)',
                'memory_tips': 'Think "June-yor" - younger version, like June is younger in the year than July',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The company hired a _____ developer to assist with software maintenance tasks.'
            },
            'jurassic': {
                'definition': 'Relating to the middle period of the Mesozoic Era (approximately 201-145 million years ago), characterized by warm climate, high sea levels, and diverse dinosaur populations. The Jurassic Period saw the evolution of many famous dinosaur species including Brontosaurus, Stegosaurus, and Allosaurus. Geologically, it featured extensive limestone deposits, mountain-building, and the breakup of the supercontinent Pangaea. The period\'s name derives from the Jura Mountains where characteristic rock formations were first studied.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'juh-RAS-ik (emphasis on second syllable)',
                'etymology': 'From Jura Mountains (France/Switzerland border) where rocks from this period were first identified',
                'memory_tips': 'Think "Jurassic Park" - the famous movie about dinosaurs from this time period',
                'alternate_spellings': '',
                'language_origin': 'French (from Celtic)',
                'example_sentence': 'The museum\'s _____ exhibit featured fossils of giant marine reptiles and early birds.'
            },
            'jurassicmyoglobin': {
                'definition': '[COMBINED WORD ERROR] This appears to be two words incorrectly joined: "jurassic" (geological period) + "myoglobin" (oxygen-carrying protein). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing spelling bee word lists, where formatting irregularities cause adjacent words to merge without proper spacing.',
                'part_of_speech': 'error - combined words',
                'pronunciation_guide': '[PRONUNCIATION ERROR - COMBINED WORDS]',
                'etymology': '[ETYMOLOGY ERROR - COMBINED WORDS]',
                'memory_tips': 'This is a data error - should be separated into "jurassic" and "myoglobin"',
                'alternate_spellings': 'jurassic + myoglobin (separate words)',
                'language_origin': 'ERROR - combined words',
                'example_sentence': '[ERROR - This combined word should not appear in spelling bee materials]'
            },
            'jurisdiction': {
                'definition': 'The official power or authority to make legal decisions and enforce laws within a particular geographic area or over specific subject matters. Legal jurisdiction determines which courts can hear cases, which laws apply, and which government agencies have regulatory authority. The concept encompasses territorial boundaries, subject-matter expertise, and hierarchical court systems. Jurisdictional questions often arise in complex legal cases involving multiple states, countries, or areas of law.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'joor-is-DIK-shuhn (emphasis on third syllable)',
                'etymology': 'From Latin "jurisdictio" meaning "administration of justice," from "jus" (law) + "dicere" (to say)',
                'memory_tips': 'Think "juris-diction" - legal dictionary authority over an area',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The federal court had _____ over the interstate commerce case.'
            },
            'justaucorps': {
                'definition': 'A form-fitting, long-sleeved garment extending from neck to knees or ankles, worn in 17th and 18th-century European fashion. Originally a military coat, it evolved into fashionable civilian wear characterized by close fit, decorative buttons, and sometimes elaborate embroidery. The justaucorps represented status and wealth through expensive fabrics and ornate decoration. Modern ballet and dance use similar fitted garments inspired by this historical clothing style.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'zhoos-toh-KOR (French pronunciation)',
                'etymology': 'From French "juste au corps" meaning "close to the body," describing the garment\'s fitted style',
                'memory_tips': 'Think "just-au-corps" - just (exactly) fitting the body (corps)',
                'alternate_spellings': 'justacorps',
                'language_origin': 'French',
                'example_sentence': 'The museum displayed an ornate 18th-century _____ decorated with gold embroidery.'
            },
            'justiciable': {
                'definition': 'Subject to trial in a court of law; capable of being decided by legal proceedings. Justiciable issues are those that courts have the authority and competence to resolve through judicial process, as opposed to political or administrative questions better handled by other branches of government. The concept involves separation of powers, determining which disputes are appropriate for judicial resolution versus legislative or executive action.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'juh-STISH-uh-buhl (emphasis on second syllable)',
                'etymology': 'From "justice" + suffix "-able," meaning "capable of being subjected to justice"',
                'memory_tips': 'Think "justice-able" - able to be resolved through justice system',
                'alternate_spellings': '',
                'language_origin': 'English (from Latin roots)',
                'example_sentence': 'The constitutional dispute was deemed _____ and proceeded to federal court.'
            },
            'justify': {
                'definition': 'To provide adequate reasons or evidence for actions, decisions, or beliefs; to prove or show to be right or reasonable. Justification involves presenting logical arguments, ethical reasoning, or factual support for positions taken. In typography, justify means aligning text to create even margins. The process of justification requires critical thinking, evidence evaluation, and clear communication to demonstrate validity or appropriateness of choices made.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'JUS-tuh-fy (emphasis on first syllable)',
                'etymology': 'From Old French "justifier," from Latin "justificare" meaning "to act justly"',
                'memory_tips': 'Think "just-ify" - to make something just or fair',
                'alternate_spellings': '',
                'language_origin': 'Old French via Latin',
                'example_sentence': 'The manager had to _____ the budget increase to the board of directors.'
            },
            'jutia': {
                'definition': 'A group of large, herbivorous rodents native to the Caribbean, particularly Cuba, with stocky bodies, short legs, and round heads. These guinea pig-like mammals inhabit trees and rocky areas, feeding on leaves, bark, and fruits. Several jutia species exist, with some being endangered due to habitat loss and hunting. They represent important elements of Caribbean island ecosystems and have cultural significance in local communities where they have been hunted for food.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hoo-TEE-ah (emphasis on second syllable)',
                'etymology': 'From Spanish "jutía," from Taíno indigenous Caribbean language',
                'memory_tips': 'Think "who-tea-ah" - like asking "who" wants "tea" with this Caribbean rodent',
                'alternate_spellings': 'hutia',
                'language_origin': 'Taíno via Spanish',
                'example_sentence': 'The Cuban _____ is one of the few large native mammals remaining on the island.'
            },
            'juvenilia': {
                'definition': 'Works produced by an author, artist, or composer during their youth, typically before achieving artistic maturity. These early creations often show developing talent, experimental techniques, and influences that shaped later mature works. Juvenilia provides insight into creative development, artistic influences, and the evolution of style over time. While sometimes dismissed as immature, juvenilia can reveal important aspects of an artist\'s development and early promise.',
                'part_of_speech': 'noun (plural)',
                'pronunciation_guide': 'joo-vuh-NIL-ee-ah (emphasis on third syllable)',
                'etymology': 'From Latin "juvenilis" meaning "youthful," with plural ending "-ia"',
                'memory_tips': 'Think "juvenile-ia" - youthful works by young artists',
                'alternate_spellings': '',
                'language_origin': 'Latin',
                'example_sentence': 'The exhibition featured Shakespeare\'s _____ including poems written during his teenage years.'
            },
            'juxtapose': {
                'definition': 'To place two or more things side by side for the purpose of comparison, contrast, or artistic effect. Juxtaposition reveals relationships, differences, or similarities that might not be apparent when items are considered separately. This technique is common in art, literature, photography, and rhetoric to create meaning, emphasis, or emotional impact through strategic placement and contrast.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'JUK-stuh-pohz (emphasis on first syllable)',
                'etymology': 'From French "juxtaposer," from Latin "juxta" (beside) + "ponere" (to place)',
                'memory_tips': 'Think "juxta-pose" - to pose things next to (juxta) each other',
                'alternate_spellings': '',
                'language_origin': 'French via Latin',
                'example_sentence': 'The photographer chose to _____ images of wealth and poverty to highlight social inequality.'
            },
            'kaddish': {
                'definition': 'A Jewish prayer recited in memory of the deceased, expressing praise for God and acceptance of divine will. The Mourner\'s Kaddish is recited during the eleven-month mourning period and on the anniversary of death. Different versions exist for various occasions including daily services, study sessions, and funerals. Written in Aramaic rather than Hebrew, the prayer affirms faith and community connection during times of loss and remembrance.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KAH-dish (emphasis on first syllable)',
                'etymology': 'From Aramaic "qaddish" meaning "holy," related to Hebrew "kadosh"',
                'memory_tips': 'Think "cad-dish" - a sacred dish of prayers served in memory',
                'alternate_spellings': 'qaddish',
                'language_origin': 'Aramaic',
                'example_sentence': 'The family gathered to recite _____ on the anniversary of their father\'s death.'
            },
            'kaffeeklatsch': {
                'definition': 'An informal social gathering for coffee and conversation, typically among women; a coffee circle or chat session combining refreshments with gossip or discussion. The tradition originated in German-speaking countries but became popular in American suburban culture during the mid-20th century. These gatherings serve important social functions including community building, information sharing, and mutual support among participants.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KAH-fee-klahch (emphasis on first syllable)',
                'etymology': 'From German "Kaffeeklatsch," literally "coffee gossip" or "coffee chat"',
                'memory_tips': 'Think "coffee-clatch" - clutching coffee cups while chatting',
                'alternate_spellings': 'coffee klatch',
                'language_origin': 'German',
                'example_sentence': 'The neighborhood _____ met every Tuesday morning to discuss local events over coffee.'
            },
            'kaftan': {
                'definition': 'A loose, flowing garment with wide sleeves, traditionally worn in many Middle Eastern, Central Asian, and African cultures. Modern kaftans serve as both traditional dress and contemporary fashion, often featuring colorful patterns, embroidery, or decorative elements. The garment adapts to various climates and occasions, providing comfort and cultural expression. Western fashion has adopted kaftan styles for resort wear and casual clothing.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KAF-tan (emphasis on first syllable)',
                'etymology': 'From Persian "qaftan," through Turkish "kaftan"',
                'memory_tips': 'Think "calf-tan" - a loose robe that covers from calf to head',
                'alternate_spellings': 'caftan',
                'language_origin': 'Persian via Turkish',
                'example_sentence': 'She wore a silk _____ decorated with traditional geometric patterns to the cultural festival.'
            },
            'kaiser': {
                'definition': 'The German and Austrian imperial title equivalent to emperor, most famously held by the German Kaiser from 1871-1918. The title derives from "Caesar" and represents supreme autocratic authority. Historical kaisers include Wilhelm I, Friedrich III, and Wilhelm II who ruled during German unification, industrial expansion, and World War I. The title ended with German defeat and the establishment of the Weimar Republic in 1918.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KY-zer (emphasis on first syllable)',
                'etymology': 'From German "Kaiser," from Latin "Caesar" (Roman imperial title)',
                'memory_tips': 'Think "Caesar" pronounced with German accent - the German emperor title',
                'alternate_spellings': '',
                'language_origin': 'German via Latin',
                'example_sentence': 'The German _____ Wilhelm II abdicated at the end of World War I in 1918.'
            },
            'kakapo': {
                'definition': 'A large, flightless, nocturnal parrot native to New Zealand, known for being the world\'s heaviest parrot species. These critically endangered birds are herbivorous, ground-dwelling, and capable of climbing trees despite their inability to fly. Kakapos have distinctive mossy-green plumage providing camouflage, and males produce unique booming calls during breeding season. Conservation efforts work to protect the remaining population of fewer than 250 individuals.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KAH-kah-poh (emphasis on first syllable)',
                'etymology': 'From Māori "kākāpō," literally meaning "night parrot"',
                'memory_tips': 'Think "kaka-po" - a parrot that says "kaka" but can\'t fly like Edgar Allan Poe\'s raven',
                'alternate_spellings': '',
                'language_origin': 'Māori',
                'example_sentence': 'The _____ is one of New Zealand\'s most endangered native species.'
            },
            'kalanchoe': {
                'definition': 'A genus of succulent flowering plants native to Madagascar and tropical Africa, popular in horticulture for their colorful blooms and easy care requirements. These plants feature thick, fleshy leaves that store water and produce clusters of small, vibrant flowers in various colors. Kalanchoe species are commonly used as houseplants, in rock gardens, and for medicinal purposes in traditional healing practices.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kal-an-KOH-ee (emphasis on third syllable)',
                'etymology': 'From Chinese "kalan chau," referring to one species of the plant',
                'memory_tips': 'Think "kalan-chow" - a colorful plant that makes you say "chow!" with delight',
                'alternate_spellings': '',
                'language_origin': 'Chinese',
                'example_sentence': 'The bright red _____ blooms provided color throughout the winter months.'
            },
            'kaleidoscope': {
                'definition': 'An optical instrument containing mirrors and colored fragments that create changing symmetrical patterns when viewed through an eyepiece and rotated. Invented in 1816, kaleidoscopes demonstrate principles of reflection and symmetry while providing artistic visual experiences. Metaphorically, the term describes rapidly changing patterns, situations, or experiences that shift continuously. The device combines entertainment with education about optics, geometry, and pattern formation.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kuh-LY-duh-skohp (emphasis on second syllable)',
                'etymology': 'From Greek "kalos" (beautiful) + "eidos" (shape) + "scope" (to see)',
                'memory_tips': 'Think "calico-scope" - scope for seeing beautiful calico-like patterns',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The child was fascinated by the shifting patterns in the _____ as she turned it slowly.'
            },
            'kalimba': {
                'definition': 'An African musical instrument consisting of a wooden board with attached metal tines of varying lengths that are plucked with the thumbs to produce melodic sounds. Also called a thumb piano or mbira, this traditional instrument creates gentle, bell-like tones and is used in both traditional African music and contemporary world music. The kalimba represents important cultural heritage and continues to influence global musical traditions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kuh-LIM-bah (emphasis on second syllable)',
                'etymology': 'From Bantu languages of Africa, related to "mbira" (thumb piano)',
                'memory_tips': 'Think "calm-ba" - a calming instrument that makes beautiful music',
                'alternate_spellings': 'kalimba',
                'language_origin': 'Bantu (African languages)',
                'example_sentence': 'The musician\'s _____ provided gentle accompaniment to the traditional African songs.'
            },
            'kalopanax': {
                'definition': 'A genus of deciduous trees native to eastern Asia, characterized by large, palmate leaves and spiny trunks. These ornamental trees, also called castor aralias, produce clusters of small white flowers followed by dark berries. Kalopanax species are valued in landscaping for their tropical appearance, shade provision, and autumn foliage. The trees adapt well to various soil conditions and climates, making them popular in botanical gardens and urban forestry.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kal-oh-PAN-aks (emphasis on third syllable)',
                'etymology': 'From Greek "kalos" (beautiful) + "panax" (all-healing), referring to medicinal properties',
                'memory_tips': 'Think "calo-panax" - beautiful (calo) pan-shaped leaves that cure all (panax)',
                'alternate_spellings': '',
                'language_origin': 'Greek',
                'example_sentence': 'The _____ tree\'s distinctive spiny trunk and large leaves made it a focal point in the garden.'
            },
            'kanban': {
                'definition': 'A lean manufacturing and project management method using visual signals to control work flow and inventory levels. Developed by Toyota, kanban systems use cards, boards, or digital tools to indicate when to produce, move, or order materials. The approach minimizes waste, reduces inventory costs, and improves efficiency through just-in-time production. Modern kanban applications extend beyond manufacturing to software development and general project management.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KAHN-bahn (emphasis on first syllable)',
                'etymology': 'From Japanese "kanban" meaning "signboard" or "visual card"',
                'memory_tips': 'Think "can-ban" - you can ban waste by using visual management boards',
                'alternate_spellings': '',
                'language_origin': 'Japanese',
                'example_sentence': 'The software team implemented a _____ board to visualize their workflow and identify bottlenecks.'
            },
            'kangaroo': {
                'definition': 'Large marsupial native to Australia, characterized by powerful hind legs for hopping, a long muscular tail for balance, and a pouch for carrying young. These herbivorous animals are iconic symbols of Australian wildlife, with various species ranging from small wallabies to large red kangaroos. Their unique locomotion method is energy-efficient for covering long distances across diverse Australian landscapes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kang-guh-ROO (emphasis on third syllable)',
                'etymology': 'From Guugu Yimidhirr (Australian Aboriginal) "gangurru," referring to a large black kangaroo',
                'memory_tips': 'Think "gang-a-roo" - a gang of bouncing animals from Australia',
                'alternate_spellings': '',
                'language_origin': 'Australian Aboriginal',
                'example_sentence': 'The mother _____ carried her joey safely in her pouch while hopping across the grassland.'
            },
            'kangri': {
                'definition': 'A traditional portable heater used in Kashmir, consisting of a clay pot filled with burning charcoal, placed in a wicker basket and carried under loose clothing for warmth. This ingenious heating device provides personal warmth during harsh Himalayan winters when conventional heating is unavailable. The kangri represents traditional adaptation to extreme cold climates and remains an important cultural artifact of Kashmiri life.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KANG-gree (emphasis on first syllable)',
                'etymology': 'From Kashmiri "kangri," referring to this traditional portable heater',
                'memory_tips': 'Think "gang-gri" - a gang of people carrying these heaters to stay warm',
                'alternate_spellings': '',
                'language_origin': 'Kashmiri',
                'example_sentence': 'During the cold Kashmir winter, she carried a _____ under her shawl for warmth.'
            },
            'kanji': {
                'definition': 'The system of Japanese writing using Chinese characters, representing concepts or words rather than individual sounds. Modern Japanese writing combines kanji with two phonetic scripts (hiragana and katakana) to create a complex but efficient written language. Each kanji character can have multiple readings depending on context, making the system challenging but highly expressive. Learning kanji is essential for Japanese literacy and cultural understanding.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'KAHN-jee (emphasis on first syllable)',
                'etymology': 'From Japanese "kanji," literally meaning "Chinese characters"',
                'memory_tips': 'Think "can-ji" - Chinese characters that Japan can use in their writing',
                'alternate_spellings': '',
                'language_origin': 'Japanese',
                'example_sentence': 'Students spend years learning to read and write the thousands of _____ characters used in Japanese texts.'
            },
            'kannada': {
                'definition': 'A Dravidian language spoken primarily in the Indian state of Karnataka by approximately 40 million people. Kannada has a rich literary tradition dating back over 1,000 years and its own distinctive script. The language has official status in Karnataka and is used in education, government, media, and literature. Kannada literature has produced notable works and authors, contributing significantly to Indian cultural heritage.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'kah-NAH-dah (emphasis on second syllable)',
                'etymology': 'From "Karnata," the ancient name for the Karnataka region',
                'memory_tips': 'Think "can-nada" - can speak nada (nothing) unless you learn this Indian language',
                'alternate_spellings': 'Canarese',
                'language_origin': 'Dravidian',
                'example_sentence': 'The _____ film industry produces hundreds of movies each year in the regional language.'
            },
            'kapparah': {
                'definition': 'A Jewish ritual of atonement performed before Yom Kippur, traditionally involving swinging a chicken overhead while reciting prayers, then donating the value to charity. This ancient custom symbolically transfers sins to the offering, though many modern practitioners substitute money or perform charitable acts instead. The ritual reflects themes of repentance, responsibility, and the desire for spiritual purification before the Day of Atonement.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'kah-pah-RAH (emphasis on third syllable)',
                'etymology': 'From Hebrew "kapparah" meaning "atonement" or "covering," from "kaper" (to cover/atone)',
                'memory_tips': 'Think "cap-para" - covering (capping) sins with atonement ritual',
                'alternate_spellings': 'kaparot',
                'language_origin': 'Hebrew',
                'example_sentence': 'Many families perform _____ as part of their preparation for the High Holy Days.'
            }
        }
        
        word_lower = word.lower()
        if word_lower in batch_096_data:
            return batch_096_data[word_lower]
        
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
    
    def process_batch_096(self, input_csv: Path) -> List[WordData]:
        """Process all words in Batch 096 with comprehensive Claude data"""
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
    
    def save_batch_096_csv(self, processed_words: List[WordData], output_file: Path):
        """Save Batch 096 processed words to CSV"""
        
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
    """Process Batch 096 with comprehensive Claude data"""
    processor = Batch096Processor()
    input_csv = Path("output/batch_096_words.csv")
    output_csv = Path("output/batch_096_processed.csv")
    
    if not input_csv.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    logger.info("Processing Batch 096 with comprehensive Claude data...")
    
    # Process all words in batch 096
    processed_words = processor.process_batch_096(input_csv)
    
    # Save results
    processor.save_batch_096_csv(processed_words, output_csv)
    
    logger.info(f"Batch 096 processing completed!")
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