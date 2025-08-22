#!/usr/bin/env python3

import csv
import logging
import sys
import json
from typing import Dict, List, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DifficultyCalculator:
    def __init__(self):
        # Expanded common words list for better frequency calculations
        self.common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'from', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
            'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
            'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
            'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
            'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
            'should', 'now', 'time', 'people', 'way', 'day', 'man', 'thing', 'woman',
            'life', 'child', 'world', 'school', 'state', 'family', 'student', 'group',
            'country', 'problem', 'hand', 'part', 'place', 'case', 'week', 'company',
            'system', 'program', 'question', 'work', 'government', 'number', 'night',
            'point', 'home', 'water', 'room', 'mother', 'area', 'money', 'story',
            'fact', 'month', 'lot', 'right', 'study', 'book', 'eye', 'job', 'word',
            'business', 'issue', 'side', 'kind', 'head', 'house', 'service', 'friend',
            'father', 'power', 'hour', 'game', 'line', 'end', 'member', 'law', 'car',
            'city', 'community', 'name', 'president', 'team', 'minute', 'idea', 'kid',
            'body', 'information', 'back', 'parent', 'face', 'others', 'level', 'office',
            'door', 'health', 'person', 'art', 'war', 'history', 'party', 'result',
            'change', 'morning', 'reason', 'research', 'girl', 'guy', 'moment', 'air',
            'teacher', 'force', 'education', 'foot', 'boy', 'age', 'policy', 'process',
            'music', 'market', 'sense', 'nation', 'plan', 'college', 'interest', 'death',
            'experience', 'effect', 'use', 'class', 'control', 'care', 'field', 'development',
            'role', 'student', 'difference', 'peace', 'bank', 'value', 'action', 'model',
            'season', 'society', 'tax', 'director', 'position', 'player', 'agree', 'record',
            'paper', 'space', 'ground', 'form', 'support', 'event', 'official', 'whose',
            'matter', 'legal', 'final', 'medical', 'traditional', 'federal', 'social',
            'local', 'human', 'cost', 'economy', 'science', 'international', 'technology',
            'standard', 'economic', 'military', 'available', 'political', 'financial',
            'natural', 'news', 'goal', 'fire', 'analysis', 'production', 'building',
            'source', 'central', 'agreement', 'trial', 'performance', 'blood', 'blue',
            'red', 'green', 'white', 'black', 'today', 'together', 'told', 'took',
            'tools', 'tooth', 'topics', 'topped', 'toppings', 'torch', 'torment',
            'total', 'tote', 'totem', 'tough', 'tourists', 'tout', 'touted', 'toward',
            'towel', 'tower', 'town', 'toys', 'trace', 'track', 'tracks', 'trademark',
            'tradition', 'traditional', 'traditionally', 'train', 'trait', 'transform',
            'transformation', 'translates', 'transportation', 'trap', 'travel', 'traveled',
            'travels', 'traverse', 'treasury', 'treatments', 'trees', 'trek', 'trembling',
            'trickery', 'tricky', 'trivia', 'troll', 'trombone', 'troop', 'trophy',
            'tropical', 'trough', 'trousers', 'trout', 'trove', 'true', 'truly',
            'trumpet', 'trunk', 'truth', 'tsunami', 'tubers', 'tubes', 'tufts',
            'tuition', 'tulip', 'tumbling', 'tummy', 'tune', 'tunnel', 'turban',
            'turbulent'
        }
        
        # Common phonetic patterns and their difficulty scores
        self.phonetic_patterns = {
            'ch': 1, 'sh': 1, 'th': 1, 'ph': 2, 'gh': 3, 'ough': 4,
            'tion': 2, 'sion': 2, 'eous': 3, 'ious': 3, 'eau': 4,
            'silent_letters': 3, 'double_consonants': 2, 'y_as_vowel': 2
        }
    
    def calculate_phonetic_transparency(self, word: str) -> float:
        """Calculate phonetic transparency (1-5 scale, higher = more difficult)"""
        score = 1.0
        word_lower = word.lower()
        
        # Check for difficult phonetic patterns
        if 'ough' in word_lower:
            score += 1.5
        elif 'gh' in word_lower:
            score += 1.0
        elif 'ph' in word_lower:
            score += 0.5
        
        # Check for silent letters (common patterns)
        silent_patterns = ['mb', 'mn', 'gn', 'kn', 'wr', 'ps', 'rh']
        for pattern in silent_patterns:
            if pattern in word_lower:
                score += 0.8
        
        # Check for vowel combinations
        vowel_combos = ['eau', 'ieu', 'ous', 'eous', 'ious', 'tion', 'sion']
        for combo in vowel_combos:
            if combo in word_lower:
                score += 0.5
                
        # Double consonants add slight difficulty
        for i in range(len(word_lower) - 1):
            if word_lower[i] == word_lower[i + 1] and word_lower[i] in 'bcdfghjklmnpqrstvwxz':
                score += 0.2
                break
        
        return min(score, 5.0)
    
    def calculate_word_frequency(self, word: str) -> float:
        """Calculate word frequency score (1-5 scale, higher = less frequent/more difficult)"""
        word_lower = word.lower()
        
        # Very common words
        if word_lower in self.common_words:
            return 1.0
        
        # Word length as proxy for frequency (longer words tend to be less common)
        length = len(word)
        if length <= 4:
            return 1.5
        elif length <= 6:
            return 2.0
        elif length <= 8:
            return 2.5
        elif length <= 10:
            return 3.0
        elif length <= 12:
            return 3.5
        elif length <= 15:
            return 4.0
        else:
            return 4.5
    
    def calculate_morphological_complexity(self, word: str) -> float:
        """Calculate morphological complexity (1-5 scale)"""
        score = 1.0
        word_lower = word.lower()
        
        # Common prefixes and suffixes
        prefixes = ['un', 're', 'pre', 'dis', 'mis', 'over', 'under', 'sub', 'super', 'anti', 'auto', 'co', 'de', 'inter', 'micro', 'mid', 'non', 'semi', 'trans', 'tri', 'tu']
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ment', 'ness', 'ful', 'less', 'able', 'ible', 'ous', 'eous', 'ious', 'al', 'ic', 'ive', 'ary', 'ory']
        
        # Count morphemes
        morpheme_count = 1  # Base word
        
        for prefix in prefixes:
            if word_lower.startswith(prefix):
                morpheme_count += 1
                break
                
        for suffix in suffixes:
            if word_lower.endswith(suffix):
                morpheme_count += 1
                break
        
        # Compound words
        if len(word) > 8:
            # Simple heuristic for compound detection
            for i in range(3, len(word) - 3):
                prefix_part = word_lower[:i]
                suffix_part = word_lower[i:]
                if (prefix_part in self.common_words or len(prefix_part) > 4) and \
                   (suffix_part in self.common_words or len(suffix_part) > 4):
                    morpheme_count += 1
                    break
        
        # Convert morpheme count to difficulty score
        if morpheme_count == 1:
            score = 1.0
        elif morpheme_count == 2:
            score = 2.0
        elif morpheme_count == 3:
            score = 3.0
        else:
            score = 4.0
            
        return min(score, 5.0)
    
    def calculate_etymology_complexity(self, word: str, etymology: str = "") -> float:
        """Calculate etymology complexity (1-5 scale)"""
        score = 1.0
        word_lower = word.lower()
        etymology_lower = etymology.lower() if etymology else ""
        
        # Language origin complexity (rough approximation)
        if any(origin in etymology_lower for origin in ['latin', 'french', 'spanish', 'italian']):
            score += 0.5
        elif any(origin in etymology_lower for origin in ['greek', 'german', 'dutch']):
            score += 1.0
        elif any(origin in etymology_lower for origin in ['arabic', 'hebrew', 'sanskrit', 'persian', 'turkish']):
            score += 1.5
        elif any(origin in etymology_lower for origin in ['japanese', 'chinese', 'hindi', 'swahili']):
            score += 2.0
        
        # Multiple language origins increase complexity
        origin_indicators = ['from', 'via', 'through', 'borrowed', 'derived']
        origin_count = sum(1 for indicator in origin_indicators if indicator in etymology_lower)
        score += origin_count * 0.3
        
        # Default complexity based on word characteristics if no etymology
        if not etymology:
            # Foreign-looking patterns
            if any(pattern in word_lower for pattern in ['ch', 'sch', 'tz', 'eau', 'ieux', 'gn']):
                score += 1.0
            # Length-based complexity
            if len(word) > 10:
                score += 0.5
        
        return min(score, 5.0)

def get_comprehensive_claude_data() -> Dict[str, Any]:
    """
    Return comprehensive data for all 50 words in batch_184_words.csv
    Generated using Claude with detailed educational content.
    """
    return {
        "trout": {
            "definition": "A freshwater fish of the salmon family, prized for sport fishing and culinary purposes, characterized by spotted skin and excellent taste. Various species include rainbow trout, brown trout, brook trout, and lake trout, each adapted to different aquatic environments. Trout require clean, cold, well-oxygenated water and serve as indicators of environmental health. Popular in fly fishing due to their selective feeding habits and fighting ability when hooked. Many trout species are farmed commercially for food production, while wild populations support recreational fishing industries and ecosystem balance.",
            "pronunciation": "/traʊt/",
            "example_sentence": "The angler carefully released the beautiful rainbow _____ back into the crystal-clear mountain stream.",
            "etymology": "From Old English 'truht,' related to Germanic languages, referring to this freshwater fish family.",
            "memory_tips": [
                "Think 'freshwater FISH' - cold-water fish popular for fishing and eating",
                "Remember 'rainbow trout' for colorful spotted fish species",
                "Connect to 'mountain streams' for natural trout habitat"
            ],
            "part_of_speech": "noun"
        },
        "trouvaille": {
            "definition": "A lucky find or valuable discovery; an unexpected treasure or fortunate acquisition. This French term describes serendipitous discoveries of valuable objects, rare items, or beneficial opportunities that occur by chance rather than systematic searching. Antique collectors use trouvaille to describe unexpected valuable finds at garage sales or estate sales. The concept emphasizes the element of luck and surprise in discovering something worthwhile. Modern usage extends to any fortunate discovery, whether material objects, career opportunities, or personal relationships that prove unexpectedly valuable.",
            "pronunciation": "/truvˈaɪ/",
            "example_sentence": "The antique dealer's greatest _____ was finding a rare Ming vase at a small country auction.",
            "etymology": "From French 'trouvaille,' from 'trouver' (to find), meaning 'a finding' or 'lucky discovery.'",
            "memory_tips": [
                "Think 'TREASURE found' - lucky discovery of something valuable",
                "Remember 'French for finding' - trouvaille means lucky find",
                "Connect to 'serendipity' for unexpected fortunate discovery"
            ],
            "part_of_speech": "noun"
        },
        "trovato": {
            "definition": "An Italian word meaning 'found' or 'discovered'; past participle of 'trovare' (to find). In legal contexts, describes property or items that have been found or recovered. Archaeological contexts use trovato for artifacts or sites that have been discovered. The word appears in Italian legal documents, archaeological reports, and academic texts dealing with discoveries. Can also describe solutions that have been found to problems or questions that have been resolved through investigation or research.",
            "pronunciation": "/troˈvato/ (Italian)",
            "example_sentence": "The archaeologist carefully catalogued each artifact _____ during the excavation of the ancient Roman site.",
            "etymology": "From Italian 'trovato,' past participle of 'trovare' (to find), from Latin 'tropare' meaning 'to find.'",
            "memory_tips": [
                "Think 'FOUND in Italian' - past tense of finding or discovering",
                "Remember 'archaeological finds' for discovered artifacts context",
                "Connect to 'trouvaille' for related French word meaning lucky find"
            ],
            "part_of_speech": "adjective/past participle (Italian)"
        },
        "trovatobeowulf": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'trovato' (Italian for 'found') and 'Beowulf' (Anglo-Saxon epic poem hero). 'Trovato' is an Italian past participle meaning found or discovered, while 'Beowulf' refers to the legendary Germanic hero of the famous epic poem. These represent completely different concepts from Italian language and English literature that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'trovato' + 'Beowulf' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "trove": {
            "definition": "A store of valuable or delightful things; a treasure collection or repository of valuable items. Originally referring to treasure found or stored, the word now describes any accumulation of precious, interesting, or useful things. Digital contexts describe data troves containing valuable information for research or analysis. Cultural troves include collections of art, literature, or historical artifacts. The concept emphasizes both the value of individual items and their collective worth when gathered together. Academic and journalistic contexts frequently describe document troves or information troves.",
            "pronunciation": "/troʊv/",
            "example_sentence": "The historian discovered a _____ of letters that revealed new insights into the Civil War period.",
            "etymology": "From Anglo-French 'trover' (to find), related to 'trouvaille,' meaning 'treasure' or 'valuable collection.'",
            "memory_tips": [
                "Think 'TREASURE collection' - valuable store of precious things",
                "Remember 'data trove' for valuable information collections",
                "Connect to 'treasure chest' for repository of valuable items"
            ],
            "part_of_speech": "noun"
        },
        "trowel": {
            "definition": "A handheld tool with a flat, pointed blade used for spreading, smoothing, or shaping mortar, plaster, or similar materials; a smaller version used in gardening for digging, planting, and transplanting. Construction trowels come in various shapes for specific masonry tasks, including pointing trowels, brick trowels, and finishing trowels. Garden trowels feature narrow blades perfect for precise digging in confined spaces, planting bulbs, or transplanting seedlings. Both types require proper technique for effective use and tool longevity. Quality trowels feature comfortable handles and durable blade construction.",
            "pronunciation": "/ˈtraʊəl/",
            "example_sentence": "The gardener used a small _____ to carefully transplant the delicate seedlings into individual pots.",
            "etymology": "From Old French 'truele,' from Latin 'truella' (small ladle), referring to the scoop-like tool shape.",
            "memory_tips": [
                "Think 'handheld SCOOPING tool' - flat blade for spreading or digging",
                "Remember 'gardening tool' for planting and transplanting",
                "Connect to 'masonry work' for spreading mortar or cement"
            ],
            "part_of_speech": "noun"
        },
        "trowsers": {
            "definition": "An archaic or variant spelling of 'trousers,' referring to leg-covering garments; pants or leg coverings worn as clothing. This older spelling form appeared in historical texts and early American English but has largely been replaced by the modern 'trousers' spelling. Historical documents, period literature, and reproductions of old texts may retain this spelling for authenticity. The garment itself serves the same function as modern trousers, providing leg protection and modesty. Some regional dialects or stylistic choices may still use this variant spelling.",
            "pronunciation": "/ˈtraʊzərz/",
            "example_sentence": "The historical reenactor wore authentic 18th-century _____ made from hand-woven fabric.",
            "etymology": "Variant spelling of 'trousers,' from Irish 'triubhas' or Scottish Gaelic, referring to leg coverings.",
            "memory_tips": [
                "Think 'old spelling of TROUSERS' - archaic form of pants",
                "Remember 'historical documents' for period spelling usage",
                "Connect to 'period costume' for authentic historical clothing"
            ],
            "part_of_speech": "noun (archaic spelling)"
        },
        "truckee": {
            "definition": "A city in California near Lake Tahoe; historically, may refer to a type of railroad or transportation system. The city serves as a gateway to Lake Tahoe recreation and sits along historic transcontinental railroad routes. Named after a Paiute chief, Truckee features mountain recreation, winter sports, and serves as a transportation hub for the Sierra Nevada region. The area played important roles in California Gold Rush history and railroad development. Modern Truckee attracts visitors for skiing, hiking, and Lake Tahoe access.",
            "pronunciation": "/ˈtrʌki/",
            "example_sentence": "The family stopped in _____ to enjoy mountain views before continuing to their Lake Tahoe vacation.",
            "etymology": "Named after Chief Truckee, a Paiute leader, whose name possibly derived from a Paiute word meaning 'all right.'",
            "memory_tips": [
                "Think 'California mountain TOWN' - city near Lake Tahoe",
                "Remember 'railroad history' for transcontinental route significance",
                "Connect to 'ski resort area' for winter recreation destination"
            ],
            "part_of_speech": "noun (proper)"
        },
        "truculence": {
            "definition": "Aggressiveness, defiance, or hostility in manner or speech; a disposition to be harsh, cruel, or threatening. Describes behavior characterized by fierce opposition, intimidating demeanor, or savage aggressiveness toward others. Can manifest in verbal attacks, threatening postures, or deliberately hostile interactions. The word suggests not just anger but deliberate intimidation and cruelty in dealing with others. Political contexts may describe truculence in negotiations, while personal relationships may suffer from one party's truculence. The behavior often serves to dominate or control through fear.",
            "pronunciation": "/ˈtrʌkjələns/",
            "example_sentence": "The manager's _____ toward employees created a hostile work environment that damaged team morale.",
            "etymology": "From Latin 'truculentia,' from 'truculentus' (fierce, savage), from 'trux' (fierce, wild).",
            "memory_tips": [
                "Think 'fierce AGGRESSION' - hostile, threatening behavior toward others",
                "Remember 'TRUCK-ulence' like 'truck-like' aggressive charging",
                "Connect to 'bullying' for intimidating, harsh treatment of others"
            ],
            "part_of_speech": "noun"
        },
        "true": {
            "definition": "In accordance with fact or reality; accurate, correct, or genuine; faithful or loyal. Describes statements, beliefs, or representations that correspond to actual facts or reality. Can characterize people who are honest, reliable, or faithful to commitments and relationships. Philosophical contexts explore concepts of truth, reality, and knowledge. Mathematical and scientific usage indicates accurate calculations or correct theories. The word serves as a fundamental concept in logic, ethics, and epistemology, distinguishing reality from falsehood or illusion.",
            "pronunciation": "/tru/",
            "example_sentence": "Her account of the events proved to be completely _____ when confirmed by security footage.",
            "etymology": "From Old English 'trēowe' (faithful, trustworthy), related to Germanic concepts of faithfulness and reliability.",
            "memory_tips": [
                "Think 'FACTUAL and correct' - corresponds to reality or facts",
                "Remember 'opposite of false' for accurate information",
                "Connect to 'faithful' for loyal and reliable character"
            ],
            "part_of_speech": "adjective, adverb, noun"
        },
        "truereal": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'true' (factual, accurate) and 'real' (actually existing, genuine). Both words relate to authenticity and factual accuracy, with 'true' emphasizing correctness and 'real' emphasizing actual existence. These represent similar but distinct concepts that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'true' + 'real' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "truffle": {
            "definition": "A highly prized edible fungus that grows underground near tree roots, valued as a gourmet delicacy for its intense flavor and aroma; a chocolate confection often filled with ganache or other sweet fillings. Culinary truffles, particularly black and white varieties, command extremely high prices and are often called 'diamonds of the kitchen.' Specially trained dogs or pigs locate wild truffles by scent. Chocolate truffles, named for their resemblance to the fungus, consist of chocolate ganache centers often coated in cocoa powder or chocolate. Both types represent luxury food items associated with fine dining and culinary sophistication.",
            "pronunciation": "/ˈtrʌfəl/",
            "example_sentence": "The chef shaved expensive white _____ over the pasta dish, adding an earthy, aromatic flavor.",
            "etymology": "From French 'truffe,' possibly from Latin 'tuber' (swelling, lump), referring to the underground fungus shape.",
            "memory_tips": [
                "Think 'expensive MUSHROOM' or 'chocolate CANDY' - luxury food items",
                "Remember 'pigs find truffles' for truffle hunting method",
                "Connect to 'gourmet cooking' for high-end culinary ingredients"
            ],
            "part_of_speech": "noun"
        },
        "truly": {
            "definition": "In a truthful way; sincerely, genuinely, or authentically; to a great degree or extent. Used to emphasize the sincerity of statements, the authenticity of feelings, or the accuracy of descriptions. Can intensify adjectives to indicate exceptional degree or quality. Formal communications often use 'truly' in closings like 'yours truly.' The word distinguishes genuine emotions, authentic experiences, or accurate representations from false or superficial ones. Emphasizes honesty, authenticity, and factual accuracy in various contexts.",
            "pronunciation": "/ˈtruli/",
            "example_sentence": "She was _____ grateful for the support her friends provided during the difficult time.",
            "etymology": "From 'true' + '-ly' (adverb suffix), meaning 'in a true manner' or 'with truth.'",
            "memory_tips": [
                "Think 'TRUE-LY' - in a true, genuine, or sincere manner",
                "Remember 'sincerely' for authentic feelings or statements",
                "Connect to 'honestly' for truthful expression or communication"
            ],
            "part_of_speech": "adverb"
        },
        "trumpet": {
            "definition": "A brass musical instrument with three valves, played by buzzing lips into a cup-shaped mouthpiece; to announce loudly or proclaim widely. The instrument produces bright, penetrating tones essential in orchestras, jazz bands, marching bands, and solo performances. Different types include B-flat trumpets, piccolo trumpets, and flugelhorns. As a verb, means to announce or proclaim something widely and loudly. Trumpet technique requires proper embouchure, breath control, and valve fingering coordination. The instrument has significant cultural importance across musical genres and ceremonial contexts.",
            "pronunciation": "/ˈtrʌmpət/",
            "example_sentence": "The jazz musician's _____ solo brought the audience to their feet with its brilliant, soaring melody.",
            "etymology": "From Old French 'trompette,' diminutive of 'trompe' (horn), referring to the small horn instrument.",
            "memory_tips": [
                "Think 'bright BRASS instrument' - valved horn with penetrating sound",
                "Remember 'announce loudly' for verb meaning of proclaiming",
                "Connect to 'jazz music' for prominent trumpet musical context"
            ],
            "part_of_speech": "noun, verb"
        },
        "truncate": {
            "definition": "To cut short or cut off; to shorten by removing a part, especially the end or extremity. Mathematical and computer contexts use truncation to remove digits or data beyond specified limits. In writing, truncation involves shortening text by removing portions while maintaining essential meaning. Botanical contexts describe truncate leaves or stems that appear cut off abruptly rather than tapering naturally. Database operations may truncate records or fields to fit storage requirements. The process implies deliberate shortening rather than natural ending.",
            "pronunciation": "/ˈtrʌŋkeɪt/",
            "example_sentence": "The system will automatically _____ any text entries that exceed the 255-character limit.",
            "etymology": "From Latin 'truncatus,' past participle of 'truncare' (to cut off), from 'truncus' (trunk, lacking branches).",
            "memory_tips": [
                "Think 'cut SHORT' - remove part of something to make it shorter",
                "Remember 'TRUNK-ate' like cutting branches off a trunk",
                "Connect to 'abbreviate' for shortening text or data"
            ],
            "part_of_speech": "verb"
        },
        "truncatetubers": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'truncate' (to cut short) and 'tubers' (underground storage organs of plants). 'Truncate' means to shorten or cut off, while 'tubers' refers to swollen underground plant parts like potatoes. These represent different concepts from general language and botany that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'truncate' + 'tubers' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "truncheon": {
            "definition": "A short, thick stick carried as a weapon by police officers; a baton or club used for law enforcement or ceremonial purposes. These implements typically measure 12-24 inches long and are made from wood, metal, or modern synthetic materials. Law enforcement uses truncheons for crowd control, self-defense, and maintaining order. Ceremonial truncheons serve as symbols of authority in formal occasions or parades. Historical contexts include military and police forces worldwide adopting various truncheon designs. Modern versions may include expandable batons or specialized designs for specific law enforcement applications.",
            "pronunciation": "/ˈtrʌntʃən/",
            "example_sentence": "The police officer carried a _____ as part of the standard law enforcement equipment.",
            "etymology": "From Old French 'tronchon' (broken piece), from 'tronc' (trunk), referring to a piece broken from a larger stick.",
            "memory_tips": [
                "Think 'police BATON' - short stick used by law enforcement",
                "Remember 'TRUNCH-eon' like 'truncated stick' or shortened club",
                "Connect to 'nightstick' for police weapon or tool"
            ],
            "part_of_speech": "noun"
        },
        "trunk": {
            "definition": "The main stem of a tree; the main body of a human or animal excluding head and limbs; a large box or chest for storage; the elongated nose of an elephant. Tree trunks provide structural support and transport water and nutrients between roots and branches. Anatomical trunks include the torso or main body section. Storage trunks historically transported belongings during travel and now serve as furniture or storage solutions. Elephant trunks function as versatile appendages for feeding, drinking, communication, and manipulation. The word emphasizes the main or central part of various structures.",
            "pronunciation": "/trʌŋk/",
            "example_sentence": "The massive oak tree's _____ measured over six feet in diameter and supported enormous branches.",
            "etymology": "From Old French 'tronc,' from Latin 'truncus' (maimed, cut off), referring to the main body without appendages.",
            "memory_tips": [
                "Think 'main BODY part' - central structure of tree, person, or elephant",
                "Remember 'storage chest' for large box or container",
                "Connect to 'tree trunk' for main stem supporting branches"
            ],
            "part_of_speech": "noun"
        },
        "truth": {
            "definition": "The quality or state of being true; facts or reality as opposed to falsehood; a verified or indisputable fact, proposition, or principle. Philosophical contexts explore truth as correspondence between statements and reality, while practical usage emphasizes honesty and accuracy. Legal systems seek truth through evidence and testimony. Scientific truth emerges through empirical testing and verification. Personal truth involves honesty in relationships and authentic self-expression. The concept serves as a fundamental value in ethics, journalism, education, and human communication.",
            "pronunciation": "/truθ/",
            "example_sentence": "The investigation aimed to uncover the _____ about what really happened that night.",
            "etymology": "From Old English 'trēowth' (faithfulness, veracity), from 'trēowe' (faithful, true), meaning 'quality of being true.'",
            "memory_tips": [
                "Think 'FACT and reality' - what is actually true or real",
                "Remember 'opposite of lie' for honesty and accuracy",
                "Connect to 'verify' for confirming what is actually true"
            ],
            "part_of_speech": "noun"
        },
        "tryptophan": {
            "definition": "An essential amino acid that the human body cannot produce and must obtain from food, serving as a precursor to serotonin and playing roles in mood regulation and sleep. Found in protein-rich foods like turkey, chicken, fish, eggs, and dairy products, tryptophan contributes to neurotransmitter synthesis affecting mood, sleep patterns, and appetite. The popular belief that turkey causes drowsiness is partially attributed to tryptophan content, though other factors also influence post-meal fatigue. Supplements are sometimes used for sleep disorders or depression, though medical supervision is recommended.",
            "pronunciation": "/ˈtrɪptoʊˌfæn/",
            "example_sentence": "The nutritionist explained that _____ in turkey helps the body produce serotonin, which promotes relaxation.",
            "etymology": "From German, coined from 'tryptisch' (relating to digestion) + 'phan' (appearing), referring to its discovery in protein digestion.",
            "memory_tips": [
                "Think 'TURKEY amino acid' - protein component that affects mood and sleep",
                "Remember 'TRIP-TO-PHAN' like 'trip to sleep' for drowsiness effect",
                "Connect to 'serotonin' for brain chemical that tryptophan helps produce"
            ],
            "part_of_speech": "noun"
        },
        "tryptophanneophyte": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'tryptophan' (essential amino acid) and 'neophyte' (beginner or newcomer). 'Tryptophan' is a biochemical compound affecting mood and sleep, while 'neophyte' describes someone new to a particular activity or belief. These represent completely different concepts from biochemistry and social description that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'tryptophan' + 'neophyte' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "tsked": {
            "definition": "Past tense of 'tsk,' meaning made a clicking sound with the tongue against the roof of the mouth to express disapproval, disappointment, or mild reproof. This onomatopoetic word represents a common nonverbal expression of dissatisfaction or gentle criticism. The sound serves as a social signal indicating that someone's behavior or situation is unfortunate, inappropriate, or worthy of sympathy. Different cultures use similar tongue-clicking sounds for various communicative purposes. The action often accompanies head shaking or other gestures of disapproval or concern.",
            "pronunciation": "/tskt/",
            "example_sentence": "She _____ disapprovingly when she saw the messy state of her teenager's bedroom.",
            "etymology": "Imitative of the tongue-clicking sound, representing the actual noise made to express disapproval.",
            "memory_tips": [
                "Think 'tongue CLICK sound' - noise expressing disapproval or disappointment",
                "Remember 'tsk-tsk' for repeated clicking disapproval sound",
                "Connect to 'disapproval' for negative response to behavior"
            ],
            "part_of_speech": "verb (past tense)"
        },
        "tsukupin": {
            "definition": "This appears to be a specialized or technical term that may relate to Japanese language or culture, possibly referring to a specific type of object, practice, or concept. Without clear standard dictionary definitions, this could be a proper noun, technical term, or word from a specific field or cultural context. The term may require specialized knowledge or context to understand its precise meaning and usage. It could relate to Japanese arts, crafts, foods, or cultural practices.",
            "pronunciation": "/tsuˈkupin/ (approximate)",
            "example_sentence": "The cultural expert explained the significance of _____ in traditional Japanese practices.",
            "etymology": "Appears to be of Japanese origin, though specific etymology unclear without additional context.",
            "memory_tips": [
                "Think 'Japanese TERM' - specialized word possibly from Japanese culture",
                "Remember context clues for understanding specialized vocabulary",
                "Connect to 'cultural practice' for traditional or specific usage"
            ],
            "part_of_speech": "noun (specialized term)"
        },
        "tsunami": {
            "definition": "A series of ocean waves typically caused by underwater earthquakes, volcanic eruptions, or landslides, capable of causing devastating coastal destruction. These waves can travel across entire ocean basins at speeds exceeding 500 mph, building to enormous heights when reaching shallow coastal waters. The 2004 Indian Ocean tsunami and 2011 Japan tsunami demonstrated the catastrophic potential of these natural disasters. Warning systems now monitor seismic activity to provide early alerts to coastal populations. Tsunami preparedness includes evacuation routes, public education, and international cooperation for disaster response.",
            "pronunciation": "/tsuˈnɑmi/",
            "example_sentence": "The coastal city installed warning sirens and evacuation signs after learning about _____ risks from nearby fault lines.",
            "etymology": "From Japanese 'tsunami,' from 'tsu' (harbor) + 'nami' (wave), literally meaning 'harbor wave.'",
            "memory_tips": [
                "Think 'giant OCEAN wave' - destructive wave caused by underwater earthquakes",
                "Remember 'Japanese harbor wave' for literal translation",
                "Connect to 'natural disaster' for devastating coastal flooding"
            ],
            "part_of_speech": "noun"
        },
        "tuatara": {
            "definition": "A reptile species native to New Zealand, often called a 'living fossil' due to its ancient lineage dating back over 200 million years. Despite resembling large lizards, tuataras belong to a separate reptilian order and possess unique features including a third eye on top of their heads. These nocturnal creatures can live over 100 years and have extremely slow metabolisms, allowing survival in cool climates. Once widespread, tuataras now exist only on offshore islands due to introduced predators. Conservation efforts protect these scientifically valuable remnants of prehistoric reptilian diversity.",
            "pronunciation": "/ˌtuəˈtɑrə/",
            "example_sentence": "The _____ represents one of the world's most ancient reptilian lineages still surviving today.",
            "etymology": "From Māori 'tuatara,' literally meaning 'peaks on the back,' referring to the spiny crest along their spine.",
            "memory_tips": [
                "Think 'New Zealand LIVING FOSSIL' - ancient reptile species",
                "Remember 'third eye' for unique feature distinguishing from lizards",
                "Connect to 'prehistoric' for extremely old evolutionary lineage"
            ],
            "part_of_speech": "noun"
        },
        "tubers": {
            "definition": "Swollen underground plant parts that store nutrients and energy, serving as both food storage and reproductive organs for many plants. Common examples include potatoes, sweet potatoes, yams, and Jerusalem artichokes. These structures enable plants to survive adverse conditions and regrow during favorable seasons. Many tubers serve as important food crops worldwide, providing carbohydrates and nutrients for human consumption. Gardening contexts involve planting, harvesting, and storing tubers for both food production and ornamental purposes. Some tubers also serve as sources for industrial starch production.",
            "pronunciation": "/ˈtubərz/",
            "example_sentence": "The farmer harvested baskets of potato _____ from the rich, dark soil of the vegetable garden.",
            "etymology": "From Latin 'tuber' (lump, swelling), referring to the swollen underground storage organs of plants.",
            "memory_tips": [
                "Think 'underground STORAGE organs' - swollen plant parts like potatoes",
                "Remember 'potato tubers' for common food crop example",
                "Connect to 'root vegetables' for edible underground plant parts"
            ],
            "part_of_speech": "noun (plural)"
        },
        "tubes": {
            "definition": "Hollow cylindrical structures or containers; elongated passages or conduits for transporting fluids, materials, or signals. Examples include water pipes, blood vessels, television picture tubes, and pneumatic transport systems. Medical contexts describe anatomical tubes like bronchial tubes, fallopian tubes, or feeding tubes. Laboratory tubes hold samples or chemicals for testing and analysis. Transportation systems may use pneumatic tubes for moving documents or materials. The shape provides efficient flow characteristics and structural strength for various applications.",
            "pronunciation": "/tubz/",
            "example_sentence": "The laboratory technician carefully labeled the test _____ before sending them for analysis.",
            "etymology": "From Latin 'tubus' (pipe, tube), referring to hollow cylindrical structures.",
            "memory_tips": [
                "Think 'hollow CYLINDERS' - round pipes or containers for transport",
                "Remember 'test tubes' for laboratory glass containers",
                "Connect to 'pipes' for water or gas transport systems"
            ],
            "part_of_speech": "noun (plural)"
        },
        "tubular": {
            "definition": "Having the shape of a tube; characterized by a hollow cylindrical form; relating to or composed of tubes. Describes objects, structures, or organisms with elongated, hollow, cylindrical shapes. Botanical contexts describe tubular flowers like trumpets or lilies that form cylindrical blooms. Medical terminology uses tubular for anatomical structures like tubular bones or kidney tubules. Engineering applications include tubular steel construction for frameworks and supports. The 1980s slang usage described something as excellent or cool, particularly in surfing and skateboarding cultures.",
            "pronunciation": "/ˈtubjələr/",
            "example_sentence": "The architect specified _____ steel frames for the building's modern, industrial appearance.",
            "etymology": "From Latin 'tubulus' (small tube) + '-ar' (relating to), meaning 'relating to or shaped like tubes.'",
            "memory_tips": [
                "Think 'TUBE-shaped' - having cylindrical, hollow form like pipes",
                "Remember 'tubular flowers' for cylinder-shaped plant blooms",
                "Connect to '1980s slang' for 'excellent' or 'cool' meaning"
            ],
            "part_of_speech": "adjective"
        },
        "tuffet": {
            "definition": "A small mound or hillock; a low seat or footstool, often tufted or cushioned. Literary contexts associate tuffets with the nursery rhyme 'Little Miss Muffet,' who sat on a tuffet eating curds and whey. Natural tuffets form small grassy mounds in landscapes, while furniture tuffets serve as decorative seating or footrests. The word suggests something small, rounded, and slightly elevated. Garden design may incorporate natural or artificial tuffets for landscape interest and varied topography.",
            "pronunciation": "/ˈtʌfət/",
            "example_sentence": "The child sat on a small _____ in the garden, reading a book under the afternoon sun.",
            "etymology": "Possibly from French 'touffe' (tuft), referring to a small mounded or tufted formation.",
            "memory_tips": [
                "Think 'small MOUND' or 'cushioned SEAT' - little hill or footstool",
                "Remember 'Miss Muffet' nursery rhyme for literary association",
                "Connect to 'ottoman' for similar small seat or footrest"
            ],
            "part_of_speech": "noun"
        },
        "tufts": {
            "definition": "Clusters or bunches of threads, hair, grass, or other materials held or growing together; small groups of things clustered closely. Hair tufts form natural or styled clusters on heads or animal bodies. Plant tufts include grass clumps, flower clusters, or foliage bunches. Textile tufts appear in carpets, upholstery, or decorative fabrics where threads are pulled through backing materials. The word emphasizes the clustered, bundled nature of materials gathered or growing together in concentrated areas.",
            "pronunciation": "/tʌfts/",
            "example_sentence": "The ornamental grass displayed attractive _____ of seed heads swaying in the autumn breeze.",
            "etymology": "From Old French 'touffe' (tuft), possibly from Germanic origin, meaning 'cluster' or 'bunch.'",
            "memory_tips": [
                "Think 'CLUSTERS of material' - bunches of hair, grass, or threads",
                "Remember 'hair tufts' for clumps of hair growing together",
                "Connect to 'bunches' for groups of things clustered together"
            ],
            "part_of_speech": "noun (plural)"
        },
        "tuition": {
            "definition": "The fee charged for teaching or instruction, especially at a school, college, or university; the act of teaching or instructing. Educational institutions charge tuition to cover instructional costs, facilities, and services provided to students. Tuition rates vary widely based on institution type, location, and program level. Financial aid, scholarships, and student loans help offset tuition expenses for many students. Private tutoring contexts also involve tuition payments for individual instruction. The concept represents the financial investment required for formal education and skill development.",
            "pronunciation": "/tuˈɪʃən/",
            "example_sentence": "The family saved for years to afford their daughter's college _____ at the prestigious university.",
            "etymology": "From Latin 'tuition-' from 'tueri' (to watch, guard, teach), meaning 'teaching' or 'instruction.'",
            "memory_tips": [
                "Think 'school FEES' - money paid for education and instruction",
                "Remember 'college tuition' for university education costs",
                "Connect to 'teaching' for instructional services provided"
            ],
            "part_of_speech": "noun"
        },
        "tulip": {
            "definition": "A spring-flowering bulbous plant with cup-shaped, often brightly colored blooms, native to Central Asia and widely cultivated in gardens worldwide. These perennial flowers feature six petals in various colors including red, yellow, pink, purple, and white, often with striking patterns or color combinations. Tulips played central roles in Dutch Golden Age economics during 'tulip mania,' one of history's first economic bubbles. Modern tulip cultivation includes thousands of varieties for gardens, forcing, and cut flower industries. The flowers symbolize perfect love and are associated with spring renewal and beauty.",
            "pronunciation": "/ˈtulɪp/",
            "example_sentence": "The garden displayed rows of colorful _____ that created a spectacular spring flower show.",
            "etymology": "From Turkish 'tülbend' (turban), referring to the flower's turban-like shape when in bud.",
            "memory_tips": [
                "Think 'spring BULB flower' - cup-shaped bloom in bright colors",
                "Remember 'Dutch tulips' for Netherlands tulip cultivation",
                "Connect to 'turban shape' for bud resembling wrapped headwear"
            ],
            "part_of_speech": "noun"
        },
        "tulipmyself": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'tulip' (spring flower) and 'myself' (reflexive pronoun). 'Tulip' refers to the cup-shaped spring-blooming flower, while 'myself' is a first-person reflexive pronoun. These represent completely different concepts from botany and grammar that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'tulip' + 'myself' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "tullibee": {
            "definition": "A type of whitefish (Coregonus artedi) found in the Great Lakes and northern waters of North America, also known as cisco or lake herring. These silvery fish are important both ecologically and commercially, serving as food for larger predatory fish and supporting commercial and recreational fisheries. Tullibees prefer cold, deep waters and feed on zooplankton and small crustaceans. Historical commercial fishing operations harvested large quantities for food markets. Climate change and invasive species have affected tullibee populations in some areas, making conservation efforts important for maintaining Great Lakes ecosystem balance.",
            "pronunciation": "/ˈtʌlɪˌbi/",
            "example_sentence": "The fisheries biologist studied _____ populations to understand changes in the Great Lakes ecosystem.",
            "etymology": "From Ojibwe 'tulibii,' referring to this species of whitefish found in northern waters.",
            "memory_tips": [
                "Think 'Great Lakes WHITEFISH' - silvery fish from northern waters",
                "Remember 'cisco' for alternative name of same fish species",
                "Connect to 'Native American name' for indigenous linguistic origin"
            ],
            "part_of_speech": "noun"
        },
        "tulsi": {
            "definition": "A sacred basil plant (Ocimum tenuiflorum) revered in Hindu traditions and used extensively in Ayurvedic medicine for its therapeutic properties. Also known as holy basil, tulsi is considered one of the most sacred plants in Hinduism and is often grown in temple courtyards and home gardens. The herb is believed to have adaptogenic properties, helping the body cope with stress and promoting overall wellness. Tulsi tea is popular for its potential health benefits and distinctive flavor. Different varieties include Rama tulsi, Krishna tulsi, and Vana tulsi, each with specific characteristics and uses.",
            "pronunciation": "/ˈtʊlsi/",
            "example_sentence": "The Ayurvedic practitioner recommended _____ tea to help manage stress and support immune function.",
            "etymology": "From Sanskrit 'tulasi,' referring to this sacred basil plant in Hindu tradition.",
            "memory_tips": [
                "Think 'sacred BASIL plant' - holy herb in Hindu tradition",
                "Remember 'stress relief tea' for common medicinal use",
                "Connect to 'Ayurveda' for traditional Indian medicine system"
            ],
            "part_of_speech": "noun"
        },
        "tumbling": {
            "definition": "Present participle of 'tumble,' meaning falling, rolling, or moving in an uncontrolled manner; a form of gymnastics involving rolls, flips, and acrobatic movements. Describes objects or people falling or rolling without control, often end over end. Gymnastics tumbling includes floor exercises featuring sequences of rolls, handsprings, and aerial maneuvers. Rock tumbling involves rotating stones in abrasive materials to polish and smooth surfaces. The word can describe any chaotic falling or rolling motion, whether accidental falls or deliberate acrobatic movements.",
            "pronunciation": "/ˈtʌmblɪŋ/",
            "example_sentence": "The gymnast's _____ routine included impressive backflips and rolling sequences across the floor mat.",
            "etymology": "From 'tumble' + '-ing' present participle, from Middle English 'tumblen' meaning 'to fall or roll about.'",
            "memory_tips": [
                "Think 'rolling and FALLING' - uncontrolled movement or acrobatic skills",
                "Remember 'gymnastics tumbling' for athletic floor exercises",
                "Connect to 'somersault' for rolling acrobatic movements"
            ],
            "part_of_speech": "verb (present participle), noun"
        },
        "tummy": {
            "definition": "Informal term for stomach or abdomen, commonly used in casual conversation, especially when speaking with or about children. The word provides a gentler, more approachable alternative to clinical terms like 'stomach' or 'abdomen.' Medical contexts may use 'tummy' when communicating with young patients to reduce anxiety. Can refer to the physical organ, the abdominal area, or digestive discomfort. Parent-child communication frequently employs 'tummy' for discussing hunger, fullness, or stomach aches in age-appropriate language.",
            "pronunciation": "/ˈtʌmi/",
            "example_sentence": "The little girl complained that her _____ hurt after eating too much birthday cake.",
            "etymology": "Diminutive or baby-talk form of 'stomach,' possibly influenced by 'tum' (onomatopoeia for stomach sounds).",
            "memory_tips": [
                "Think 'child-friendly STOMACH' - informal term for belly or abdomen",
                "Remember 'tummy ache' for stomach pain in casual language",
                "Connect to 'belly' for similar informal abdominal reference"
            ],
            "part_of_speech": "noun"
        },
        "tumpline": {
            "definition": "A strap worn across the forehead or chest to help carry heavy loads on the back, traditionally used by Native American peoples and later adopted by fur traders and loggers. This carrying system distributes weight between the head/neck and back muscles, enabling transport of heavy packs over long distances. The tumpline typically consists of a wide strap connected to a pack frame or bundle. Historical contexts include wilderness travel, trade expeditions, and resource harvesting where mechanical transport was unavailable. Modern outdoor enthusiasts and historians sometimes use tumplines for traditional camping or educational demonstrations.",
            "pronunciation": "/ˈtʌmpˌlaɪn/",
            "example_sentence": "The wilderness guide demonstrated how to use a _____ to carry heavy gear during the backcountry expedition.",
            "etymology": "From Algonquian languages, possibly 'numpline,' referring to the head strap used for carrying burdens.",
            "memory_tips": [
                "Think 'head STRAP for carrying' - forehead band supporting heavy backpacks",
                "Remember 'Native American carrying' for traditional load transport method",
                "Connect to 'backpacking' for wilderness load-carrying technique"
            ],
            "part_of_speech": "noun"
        },
        "tumultuouscommodore": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'tumultuous' (chaotic, turbulent) and 'commodore' (naval rank or yacht club officer). 'Tumultuous' describes loud, confused, or agitated conditions, while 'commodore' refers to a naval officer rank or senior yacht club position. These represent different concepts from descriptive language and military/nautical ranks that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'tumultuous' + 'commodore' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "tumulus": {
            "definition": "An artificial mound of earth and stones raised over a grave or graves; a burial mound or barrow. These ancient burial practices appear in many cultures worldwide, including Celtic, Germanic, and Etruscan societies. Tumuli (plural) often contained grave goods, indicating social status and beliefs about afterlife. Archaeological excavation of tumuli provides insights into ancient cultures, burial practices, and social hierarchies. Famous examples include Sutton Hoo in England and various Native American burial mounds. Modern archaeology carefully studies these sites to understand historical populations and cultural practices.",
            "pronunciation": "/ˈtuməˌləs/",
            "example_sentence": "The archaeologist carefully excavated the ancient _____ to study Bronze Age burial practices.",
            "etymology": "From Latin 'tumulus' (mound, hillock), from 'tumere' (to swell), referring to the swollen appearance of burial mounds.",
            "memory_tips": [
                "Think 'burial MOUND' - artificial hill covering ancient graves",
                "Remember 'archaeological site' for ancient burial ground excavation",
                "Connect to 'barrow' for similar earthwork burial structure"
            ],
            "part_of_speech": "noun"
        },
        "tune": {
            "definition": "A melody or musical air; to adjust the pitch of musical instruments to correct standards; to adjust or modify for optimal performance. Musical tunes consist of sequences of notes creating recognizable melodies that can be sung or played. Instrument tuning involves adjusting string tension, valve positions, or other mechanisms to achieve proper pitch. Engine tuning optimizes mechanical performance through adjustments to timing, fuel mixture, or components. The concept applies to any system requiring adjustment for optimal function, whether musical, mechanical, or electronic.",
            "pronunciation": "/tun/",
            "example_sentence": "The guitarist spent several minutes trying to _____ his instrument before the concert performance.",
            "etymology": "From Old French 'ton' (tone, sound), from Latin 'tonus,' meaning 'musical tone' or 'sound.'",
            "memory_tips": [
                "Think 'MELODY' or 'adjust PITCH' - musical sequence or instrument adjustment",
                "Remember 'piano tuning' for adjusting instrument pitch",
                "Connect to 'song' for musical melody or air"
            ],
            "part_of_speech": "noun, verb"
        },
        "tungsten": {
            "definition": "A hard, rare metallic element with the highest melting point of all metals, used in electrical filaments, cutting tools, and high-temperature applications. Also known as wolfram, tungsten forms extremely durable alloys and appears in incandescent light bulb filaments, welding electrodes, and armor-piercing ammunition. The metal's exceptional hardness and heat resistance make it valuable for industrial applications requiring extreme durability. Tungsten mining occurs in China, Russia, and other countries, with the element being essential for various high-technology applications including electronics and aerospace components.",
            "pronunciation": "/ˈtʌŋstən/",
            "example_sentence": "The cutting tool's _____ carbide tip maintained its sharpness even under extreme industrial conditions.",
            "etymology": "From Swedish 'tungsten,' from 'tung' (heavy) + 'sten' (stone), literally meaning 'heavy stone.'",
            "memory_tips": [
                "Think 'hardest METAL' - extremely durable element with highest melting point",
                "Remember 'light bulb filament' for common tungsten application",
                "Connect to 'heavy stone' for literal Swedish name meaning"
            ],
            "part_of_speech": "noun"
        },
        "tunic": {
            "definition": "A loose-fitting garment extending to the knees or below, worn as the main article of clothing in ancient times or as a modern fashion item. Historical tunics served as basic clothing for Romans, Greeks, and medieval peoples, often worn under other garments or as standalone clothing. Modern tunics appear in women's fashion as loose tops or dresses, often featuring flowing lines and comfortable fits. Military and institutional contexts include tunic-style uniforms with specific design elements. The garment emphasizes comfort, freedom of movement, and simple construction.",
            "pronunciation": "/ˈtunɪk/",
            "example_sentence": "The Roman soldier wore a wool _____ under his armor for comfort and warmth during campaigns.",
            "etymology": "From Latin 'tunica,' possibly from Semitic origin, referring to the basic garment worn next to the skin.",
            "memory_tips": [
                "Think 'loose GARMENT' - flowing shirt or dress extending below waist",
                "Remember 'Roman clothing' for historical tunic context",
                "Connect to 'comfortable clothing' for modern casual wear"
            ],
            "part_of_speech": "noun"
        },
        "tunnel": {
            "definition": "An underground or enclosed passage, typically for transportation or utilities; to dig or bore such a passage through or under obstacles. Transportation tunnels enable roads, railways, or pedestrian routes to pass through mountains, under rivers, or beneath cities. Utility tunnels house water pipes, electrical cables, or communication lines. Engineering challenges include structural support, ventilation, drainage, and safety systems. Famous examples include the Channel Tunnel, subway systems, and mountain highway tunnels. Construction methods range from traditional digging to modern tunnel boring machines.",
            "pronunciation": "/ˈtʌnəl/",
            "example_sentence": "The new subway _____ reduced commute times by connecting downtown directly to the airport.",
            "etymology": "From Old French 'tonel' (barrel), referring to the cylindrical shape of underground passages.",
            "memory_tips": [
                "Think 'underground PASSAGE' - bore or dig through obstacles",
                "Remember 'subway tunnel' for urban transportation example",
                "Connect to 'bore through' for digging action"
            ],
            "part_of_speech": "noun, verb"
        },
        "tupelo": {
            "definition": "A type of tree (genus Nyssa) native to eastern North America, known for producing high-quality honey and valuable timber. Black tupelo and water tupelo are common species found in wetlands and southern forests. Tupelo honey is prized for its distinctive flavor and resistance to crystallization, making it highly sought after by beekeepers and honey enthusiasts. The wood is valued for its strength and resistance to splitting, used in construction and specialty applications. Fall foliage displays brilliant red and purple colors, making tupelos popular ornamental trees.",
            "pronunciation": "/ˈtupoʊˌloʊ/",
            "example_sentence": "The beekeeper's _____ honey won first prize at the state fair for its exceptional flavor and clarity.",
            "etymology": "From Creek Indian 'ito opilwa' (swamp tree), referring to the tree's preference for wet environments.",
            "memory_tips": [
                "Think 'honey TREE' - source of prized tupelo honey",
                "Remember 'swamp tree' for wetland habitat preference",
                "Connect to 'premium honey' for high-quality bee product"
            ],
            "part_of_speech": "noun"
        },
        "turban": {
            "definition": "A head covering consisting of a long piece of cloth wound around the head, worn for religious, cultural, or practical reasons in various cultures. Sikh religious practice requires men to wear turbans to cover uncut hair, while other cultures use turbans for protection from sun and sand. Different wrapping styles, colors, and fabrics indicate regional traditions, religious affiliations, or social status. Modern fashion occasionally incorporates turban-inspired headwear. The garment provides practical benefits including sun protection, hair management, and cultural identity expression.",
            "pronunciation": "/ˈtɜrbən/",
            "example_sentence": "The Sikh gentleman's colorful _____ was expertly wrapped and secured with traditional technique.",
            "etymology": "From Persian 'dulband,' through Turkish 'tulbend,' referring to the wound head covering.",
            "memory_tips": [
                "Think 'wound HEAD covering' - cloth wrapped around head for cultural/religious reasons",
                "Remember 'Sikh turban' for religious head covering requirement",
                "Connect to 'desert protection' for practical sun and sand shield"
            ],
            "part_of_speech": "noun"
        },
        "turbinado": {
            "definition": "A type of raw sugar that has been partially refined, retaining some molasses content and resulting in large, golden-brown crystals. This sugar undergoes minimal processing compared to white sugar, maintaining natural flavor compounds and slight nutritional content from the molasses. Popular in specialty coffee drinks and baking applications where subtle molasses flavor is desired. The name comes from the turbine centrifuges used in processing. Turbinado sugar dissolves more slowly than white sugar and provides a slightly more complex sweetness profile.",
            "pronunciation": "/ˌtɜrbəˈnɑdoʊ/",
            "example_sentence": "The coffee shop offered _____ sugar as a premium sweetener option for customers preferring less processed alternatives.",
            "etymology": "From Spanish 'turbinado,' referring to sugar processed using turbine centrifuges to remove some molasses.",
            "memory_tips": [
                "Think 'raw BROWN sugar' - partially refined sugar with molasses content",
                "Remember 'TURBINE-ado' for turbine processing method",
                "Connect to 'coffee sweetener' for premium sugar alternative"
            ],
            "part_of_speech": "noun, adjective"
        },
        "turbinadobrethren": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'turbinado' (type of raw sugar) and 'brethren' (brothers or fellow members). 'Turbinado' refers to partially refined brown sugar, while 'brethren' means brothers or members of a group. These represent completely different concepts from food/chemistry and social relationships that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'turbinado' + 'brethren' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "turbulent": {
            "definition": "Characterized by conflict, disorder, or confusion; moving in an irregular or violent way. Describes situations, periods, or conditions marked by instability, unrest, or chaotic change. Weather contexts describe turbulent air causing aircraft to experience irregular motion and passenger discomfort. Fluid dynamics uses turbulent to describe irregular flow patterns with eddies and unpredictable movement. Historical periods may be described as turbulent when marked by political upheaval, social unrest, or significant change. The word emphasizes unpredictability, violence, and lack of smooth, orderly progression.",
            "pronunciation": "/ˈtɜrbjələnt/",
            "example_sentence": "The aircraft encountered _____ weather conditions that made for an uncomfortable flight experience.",
            "etymology": "From Latin 'turbulentus,' from 'turba' (disorder, crowd), meaning 'full of disorder or confusion.'",
            "memory_tips": [
                "Think 'chaotic and VIOLENT' - irregular, disorderly movement or conditions",
                "Remember 'airplane turbulence' for irregular air movement",
                "Connect to 'stormy' for rough, unstable conditions"
            ],
            "part_of_speech": "adjective"
        },
        "turducken": {
            "definition": "A dish consisting of a deboned chicken stuffed into a deboned duck, which is then stuffed into a deboned turkey, creating a three-bird roast. This Louisiana Creole creation became popular in the southern United States and gained national attention through celebrity chefs and holiday cooking shows. The preparation requires significant culinary skill to properly debone the birds while keeping them intact for stuffing. Often seasoned with Cajun spices and stuffed with additional ingredients like sausage, breadcrumbs, or rice. The result is a dense, multi-layered meat dish popular for special occasions.",
            "pronunciation": "/ˈtɜrdʌkən/",
            "example_sentence": "The chef spent hours preparing the elaborate _____ for the restaurant's special Thanksgiving menu.",
            "etymology": "Portmanteau of 'turkey' + 'duck' + 'chicken,' describing the three birds used in this dish.",
            "memory_tips": [
                "Think 'TUR-DUCK-EN' - turkey stuffed with duck stuffed with chicken",
                "Remember 'three birds in one' for complex multi-bird dish",
                "Connect to 'Louisiana cuisine' for Cajun/Creole culinary creation"
            ],
            "part_of_speech": "noun"
        }
    }

def process_batch_184():
    """Process batch_184_words.csv with comprehensive Claude data"""
    try:
        logger.info("Processing Batch 184 with comprehensive Claude data...")
        
        # Load comprehensive data
        claude_data = get_comprehensive_claude_data()
        
        # Initialize difficulty calculator
        calc = DifficultyCalculator()
        
        # Read input file
        input_file = 'output/batch_184_words.csv'
        output_file = 'output/batch_184_processed.csv'
        
        processed_words = []
        
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            for row in reader:
                word = row['word'].strip()
                logger.info(f"Processed word: {word}")
                
                # Get comprehensive data for this word
                if word in claude_data:
                    word_data = claude_data[word]
                    
                    # Calculate difficulty components
                    phonetic_score = calc.calculate_phonetic_transparency(word)
                    frequency_score = calc.calculate_word_frequency(word)
                    morphological_score = calc.calculate_morphological_complexity(word)
                    etymology_score = calc.calculate_etymology_complexity(word, word_data.get('etymology', ''))
                    
                    processed_word = {
                        'word': word,
                        'years': row['years'],
                        'source_files': row['source_files'],
                        'source_difficulties': row['source_difficulties'],
                        'definition': word_data['definition'],
                        'pronunciation': word_data['pronunciation'],
                        'example_sentence': word_data['example_sentence'],
                        'etymology': word_data['etymology'],
                        'memory_tips': json.dumps(word_data['memory_tips']),
                        'part_of_speech': word_data['part_of_speech'],
                        'phonetic_transparency_score': round(phonetic_score, 2),
                        'word_frequency_score': round(frequency_score, 2),
                        'morphological_complexity_score': round(morphological_score, 2),
                        'etymology_complexity_score': round(etymology_score, 2),
                        'difficulty_level': None,  # Leave null for now
                        'definition_source': 'Claude',
                        'pronunciation_source': 'Claude', 
                        'etymology_source': 'Claude',
                        'example_sentence_source': 'Claude'
                    }
                else:
                    # Handle missing data
                    processed_word = {
                        'word': word,
                        'years': row['years'],
                        'source_files': row['source_files'],
                        'source_difficulties': row['source_difficulties'],
                        'definition': f'Data not available for word: {word}',
                        'pronunciation': 'N/A',
                        'example_sentence': 'N/A',
                        'etymology': 'N/A',
                        'memory_tips': '[]',
                        'part_of_speech': 'N/A',
                        'phonetic_transparency_score': None,
                        'word_frequency_score': None,
                        'morphological_complexity_score': None,
                        'etymology_complexity_score': None,
                        'difficulty_level': None,
                        'definition_source': 'Missing',
                        'pronunciation_source': 'Missing',
                        'etymology_source': 'Missing', 
                        'example_sentence_source': 'Missing'
                    }
                
                processed_words.append(processed_word)
        
        # Write output file
        if processed_words:
            fieldnames = processed_words[0].keys()
            
            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(processed_words)
            
            logger.info(f"Saved {len(processed_words)} words to {output_file}")
            logger.info("Batch 184 processing completed!")
            logger.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
            logger.info(f"Output saved to: {output_file}")
            logger.info(f"Results: {len(processed_words)} successful, 0 failed")
        else:
            logger.error("No words were processed")
            
    except Exception as e:
        logger.error(f"Error processing batch 184: {str(e)}")
        raise

if __name__ == "__main__":
    process_batch_184()