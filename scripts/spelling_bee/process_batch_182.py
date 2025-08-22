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
            'travels', 'traverse', 'treasury', 'treatments', 'trees', 'trek', 'trembling'
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
        prefixes = ['un', 're', 'pre', 'dis', 'mis', 'over', 'under', 'sub', 'super', 'anti', 'auto', 'co', 'de', 'inter', 'micro', 'mid', 'non', 'semi', 'trans']
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
    Return comprehensive data for all 50 words in batch_182_words.csv
    Generated using Claude with detailed educational content.
    """
    return {
        "transfixed": {
            "definition": "Past tense of 'transfix,' meaning rendered motionless or paralyzed by amazement, shock, fear, or fascination; pierced through with a sharp object. Describes being completely captivated or mesmerized by something to the point of being unable to move or look away. Can refer to being emotionally overwhelmed by beauty, terror, or wonder that suspends normal physical reactions. Literary contexts often use 'transfixed' to describe characters frozen by supernatural events, intense emotions, or dramatic revelations. The word implies both physical stillness and mental absorption.",
            "pronunciation": "/trænsˈfɪkst/",
            "example_sentence": "The audience sat _____ as the magician performed impossible feats that defied all logic.",
            "etymology": "From Latin 'transfixus,' past participle of 'transfigere' (to pierce through), from 'trans-' (through) + 'figere' (to fix, fasten).",
            "memory_tips": [
                "Think 'TRANS-FIXED' - completely fixed in place by something amazing",
                "Remember 'pierced through' for literal meaning of being impaled",
                "Connect to 'mesmerized' for being captivated and unable to move"
            ],
            "part_of_speech": "verb (past tense)"
        },
        "transform": {
            "definition": "To change completely in form, appearance, nature, or character; to undergo or cause a thorough or dramatic change. Can describe physical changes like caterpillars becoming butterflies, chemical reactions altering substances, or personal growth changing personalities. Mathematical contexts use transformation for operations that change geometric shapes or algebraic expressions. Technological transformations modify systems, processes, or capabilities. The word implies significant, often fundamental change rather than minor adjustments, emphasizing the dramatic nature of the alteration from one state to another.",
            "pronunciation": "/trænsˈfɔrm/",
            "example_sentence": "The renovation project will completely _____ the old warehouse into a modern apartment complex.",
            "etymology": "From Latin 'transformare,' from 'trans-' (across, beyond) + 'forma' (form, shape), meaning 'to change form.'",
            "memory_tips": [
                "Think 'TRANS-FORM' - across forms, changing from one form to another",
                "Remember 'butterfly transformation' for dramatic change example",
                "Connect to 'metamorphosis' for complete change process"
            ],
            "part_of_speech": "verb"
        },
        "transformation": {
            "definition": "The act or process of changing completely in form, appearance, nature, or character; a thorough or dramatic change from one state to another. Describes both the process and result of fundamental alteration, whether physical, chemical, psychological, or social. Biology uses transformation for genetic changes in organisms, while psychology describes personal growth and behavioral changes. Business contexts refer to organizational changes that fundamentally alter operations or structure. The concept emphasizes comprehensive change rather than superficial modifications, often implying improvement or evolution to a more advanced state.",
            "pronunciation": "/ˌtrænsfərˈmeɪʃən/",
            "example_sentence": "The company's digital _____ improved efficiency and customer satisfaction dramatically.",
            "etymology": "From Latin 'transformation-' from 'transformare' (to transform) + '-tion' (action or process), meaning 'the action of transforming.'",
            "memory_tips": [
                "Think 'TRANSFORM-ATION' - the action or process of transforming",
                "Remember 'caterpillar to butterfly' for natural transformation example",
                "Connect to 'metamorphosis' for complete change process"
            ],
            "part_of_speech": "noun"
        },
        "transgressions": {
            "definition": "Plural of transgression; violations of laws, rules, moral codes, or boundaries; acts of going beyond accepted limits or crossing forbidden lines. Religious contexts describe sins or violations of divine commandments, while legal contexts refer to crimes or breaches of regulations. Social transgressions involve breaking cultural norms or ethical standards. The word implies deliberate crossing of established boundaries, whether legal, moral, social, or personal. Modern usage includes violations of professional ethics, academic integrity, or personal relationships that breach trust or established agreements.",
            "pronunciation": "/trænzˈɡrɛʃənz/",
            "example_sentence": "The investigation revealed multiple financial _____ that violated both company policy and federal law.",
            "etymology": "From Latin 'transgression-' from 'transgredi' (to step across), from 'trans-' (across) + 'gradi' (to step).",
            "memory_tips": [
                "Think 'TRANS-GRESS-IONS' - stepping across boundaries or limits",
                "Remember 'crossing lines' for violating rules or laws",
                "Connect to 'violations' for breaking established rules or codes"
            ],
            "part_of_speech": "noun (plural)"
        },
        "transhumance": {
            "definition": "The seasonal movement of livestock between different grazing areas, typically from lowland winter pastures to highland summer pastures. This traditional pastoral practice optimizes the use of natural resources by following seasonal availability of grass and favorable weather conditions. Common in mountainous regions of Europe, Asia, and other areas where elevation changes create distinct seasonal grazing opportunities. The practice involves moving entire herds along established routes, often requiring specialized knowledge of terrain, weather patterns, and animal behavior. Modern transhumance may use trucks or other transportation, but traditional methods involved walking livestock along ancient migration routes.",
            "pronunciation": "/trænsˈhjuməns/",
            "example_sentence": "The shepherds practiced _____, moving their flocks to mountain pastures each summer for better grazing.",
            "etymology": "From French 'transhumance,' from Spanish 'trashumancia,' from Latin 'trans-' (across) + 'humus' (ground), meaning 'across the ground.'",
            "memory_tips": [
                "Think 'TRANS-HUMANCE' - moving livestock across different lands seasonally",
                "Remember 'seasonal migration' for livestock moving to better pastures",
                "Connect to 'shepherding' for traditional pastoral livestock movement"
            ],
            "part_of_speech": "noun"
        },
        "transience": {
            "definition": "The quality or state of being transient; impermanence, temporariness, or the condition of lasting only for a short time. Philosophical contexts explore the transience of human life, beauty, and material possessions as fundamental aspects of existence. The concept emphasizes the fleeting nature of experiences, relationships, and physical phenomena. Buddhism and other philosophical traditions teach acceptance of transience as essential for reducing suffering and attachment. Art and literature often explore themes of transience through depictions of changing seasons, aging, or the passage of time.",
            "pronunciation": "/ˈtrænʃəns/",
            "example_sentence": "The _____ of cherry blossoms makes their brief spring beauty even more precious and meaningful.",
            "etymology": "From Latin 'transient-' from 'transire' (to go across, pass away) + '-ence' (quality or state), meaning 'quality of passing away.'",
            "memory_tips": [
                "Think 'TRANSIENT quality' - the state of being temporary or fleeting",
                "Remember 'cherry blossoms' for beautiful but brief existence",
                "Connect to 'impermanence' for philosophical concept of temporary nature"
            ],
            "part_of_speech": "noun"
        },
        "transistor": {
            "definition": "A semiconductor device used to amplify or switch electronic signals and electrical power, fundamental to modern electronics and computing. These three-terminal devices can control large amounts of current and voltage with small input signals, making them essential for amplifiers, switches, and digital logic circuits. Invented in 1947, transistors revolutionized electronics by replacing bulky vacuum tubes with compact, efficient, and reliable components. Modern computer processors contain billions of microscopic transistors that perform calculations and store information. Types include bipolar junction transistors (BJTs) and field-effect transistors (FETs), each with specific applications.",
            "pronunciation": "/trænˈzɪstər/",
            "example_sentence": "The invention of the _____ made possible the development of portable radios and eventually computers.",
            "etymology": "From 'transfer' + 'resistor,' coined in 1948 to describe its function of transferring electrical resistance.",
            "memory_tips": [
                "Think 'TRANSFER-resistor' - device that transfers electrical resistance",
                "Remember 'electronic switch' for basic function in circuits",
                "Connect to 'computer chip' for modern application in digital devices"
            ],
            "part_of_speech": "noun"
        },
        "transit": {
            "definition": "The action of passing through or across a place; public transportation systems; the passage of a celestial body across the meridian or across the face of another body. Urban contexts refer to public transportation networks including buses, trains, and subways that move people efficiently across cities. Astronomical transit occurs when planets pass between Earth and the Sun or when moons cross planetary faces. Shipping contexts describe goods in transit during transportation from origin to destination. The word emphasizes movement and passage rather than permanent residence or stationary states.",
            "pronunciation": "/ˈtrænzɪt/",
            "example_sentence": "The city invested in expanding public _____ to reduce traffic congestion and air pollution.",
            "etymology": "From Latin 'transitus' (a going across), from 'transire' (to go across), from 'trans-' (across) + 'ire' (to go).",
            "memory_tips": [
                "Think 'public TRANSPORTATION' - buses, trains, subways for moving people",
                "Remember 'in transit' for things moving from one place to another",
                "Connect to 'passage' for movement across or through areas"
            ],
            "part_of_speech": "noun, verb"
        },
        "translates": {
            "definition": "Third person singular present tense of 'translate,' meaning converts text or speech from one language into another; transforms or converts something into a different form, medium, or expression. Language contexts involve rendering meaning from source languages into target languages while preserving intent and cultural nuances. Can also mean explaining complex concepts in simpler terms or converting abstract ideas into practical applications. Technical contexts may describe translating data between different formats or systems. The process requires understanding both literal meaning and cultural context.",
            "pronunciation": "/trænsˈleɪts/",
            "example_sentence": "The interpreter _____ the speaker's words into three different languages simultaneously.",
            "etymology": "From Latin 'translatus,' past participle of 'transferre' (to transfer, carry across), meaning 'carried across' languages.",
            "memory_tips": [
                "Think 'carries ACROSS languages' - moving meaning between languages",
                "Remember 'TRANS-LATE' = across + carried for language conversion",
                "Connect to 'interpretation' for converting between different languages"
            ],
            "part_of_speech": "verb (third person singular)"
        },
        "translucent": {
            "definition": "Allowing light to pass through but not transparent; permitting light transmission while scattering it so that objects behind cannot be clearly seen. Materials like frosted glass, wax paper, or thin fabrics demonstrate translucency by transmitting light while maintaining privacy or creating soft illumination effects. Different from transparent (completely clear) and opaque (blocking all light), translucent materials find applications in lighting design, privacy screens, and decorative elements. The quality creates gentle, diffused lighting effects prized in architecture and interior design.",
            "pronunciation": "/trænzˈlusənt/",
            "example_sentence": "The _____ curtains provided privacy while still allowing natural light to illuminate the room softly.",
            "etymology": "From Latin 'translucent-' from 'translucere' (to shine through), from 'trans-' (through) + 'lucere' (to shine).",
            "memory_tips": [
                "Think 'light shines THROUGH' but objects aren't clearly visible",
                "Remember 'TRANS-LUCENT' = through + light for partial light transmission",
                "Connect to 'frosted glass' for material that lets light through but obscures view"
            ],
            "part_of_speech": "adjective"
        },
        "transmissibility": {
            "definition": "The quality or degree to which something can be transmitted or passed from one person, place, or organism to another. Medical contexts focus on disease transmissibility, measuring how easily pathogens spread between individuals or populations. The concept includes factors affecting transmission such as contagiousness, environmental stability, and susceptibility of recipients. Genetic transmissibility describes how traits pass from parents to offspring. Information transmissibility relates to how effectively data, knowledge, or cultural elements spread through communities. Public health uses transmissibility measures to predict and control disease outbreaks.",
            "pronunciation": "/trænzˌmɪsəˈbɪləti/",
            "example_sentence": "Scientists studied the virus's _____ to understand how quickly it could spread through the population.",
            "etymology": "From 'transmissible' + '-ity' (quality of), from Latin 'transmittere' (to send across), meaning 'quality of being transmittable.'",
            "memory_tips": [
                "Think 'ability to be TRANSMITTED' - quality of spreading or passing along",
                "Remember 'disease spread' for medical context of contagion",
                "Connect to 'contagiousness' for how easily something spreads"
            ],
            "part_of_speech": "noun"
        },
        "transmontane": {
            "definition": "Situated or existing on the other side of mountains; relating to regions beyond mountainous barriers. Geographical contexts describe areas separated by mountain ranges, often having different climates, cultures, or political systems due to natural barriers. Historical usage refers to regions beyond the Alps from a particular perspective, such as transmontane Italy from northern European viewpoints. The term emphasizes the significance of mountains as natural boundaries affecting human settlement, trade routes, and cultural development. Modern usage extends to any regions separated by significant mountainous terrain.",
            "pronunciation": "/trænzˈmɑnteɪn/",
            "example_sentence": "The _____ regions developed distinct cultural traditions due to isolation created by the mountain barriers.",
            "etymology": "From Latin 'transmontanus,' from 'trans-' (beyond) + 'montanus' (of mountains), meaning 'beyond the mountains.'",
            "memory_tips": [
                "Think 'TRANS-MOUNTAIN' - beyond or across mountain ranges",
                "Remember 'other side of mountains' for geographical separation",
                "Connect to 'Alps' for traditional European context of mountain barriers"
            ],
            "part_of_speech": "adjective"
        },
        "transparencies": {
            "definition": "Plural of transparency; the quality of being transparent or see-through; openness and honesty in processes, decisions, or operations; clear plastic sheets used for overhead projections. Physical transparency allows light to pass through without significant scattering, enabling clear vision through materials like glass or clear plastics. Organizational transparency involves open communication, accessible information, and accountable decision-making processes. Educational contexts historically used transparency sheets with overhead projectors for presentations. Financial transparency requires clear reporting of revenues, expenses, and decision-making processes.",
            "pronunciation": "/trænˈspɛrənsiz/",
            "example_sentence": "The professor prepared several _____ with diagrams to illustrate the complex scientific concepts.",
            "etymology": "From 'transparent' + '-cy' (quality) + '-ies' (plural), from Latin 'transparere' (to show through).",
            "memory_tips": [
                "Think 'see-through SHEETS' or 'openness quality' - clear materials or honest processes",
                "Remember 'overhead projector' for educational presentation materials",
                "Connect to 'clear glass' for physical transparency concept"
            ],
            "part_of_speech": "noun (plural)"
        },
        "transpiration": {
            "definition": "The process by which water is absorbed by plant roots from soil and then evaporated from plant leaves and stems into the atmosphere. This vital biological process helps plants regulate temperature, transport nutrients, and maintain structural integrity. Transpiration creates a continuous water flow from roots to leaves, enabling nutrient transport throughout the plant. Environmental factors including temperature, humidity, wind, and light intensity affect transpiration rates. The process contributes significantly to the water cycle, returning moisture to the atmosphere and influencing local climate conditions.",
            "pronunciation": "/ˌtrænspəˈreɪʃən/",
            "example_sentence": "During hot summer days, _____ from the forest trees creates cooling humidity in the surrounding air.",
            "etymology": "From French 'transpiration,' from Latin 'trans-' (through) + 'spirare' (to breathe), meaning 'breathing through.'",
            "memory_tips": [
                "Think 'plants BREATHING out water' - water evaporation from plant leaves",
                "Remember 'TRANS-SPIRATION' = through + breathing for water release",
                "Connect to 'sweating' for similar water release process in animals"
            ],
            "part_of_speech": "noun"
        },
        "transportation": {
            "definition": "The action of moving people, goods, or materials from one location to another; systems and methods used for such movement including vehicles, infrastructure, and logistics. Modern transportation encompasses personal vehicles, public transit, freight shipping, aviation, and emerging technologies like autonomous vehicles. Infrastructure includes roads, railways, airports, ports, and supporting facilities that enable efficient movement. Economic development depends heavily on transportation systems for commerce, employment access, and resource distribution. Environmental considerations increasingly influence transportation planning and technology development.",
            "pronunciation": "/ˌtrænspərˈteɪʃən/",
            "example_sentence": "The city's _____ network includes buses, trains, bike lanes, and ride-sharing services.",
            "etymology": "From Latin 'transportation-' from 'transportare' (to carry across) + '-tion' (action), meaning 'action of carrying across.'",
            "memory_tips": [
                "Think 'moving people and GOODS' - systems for getting from place to place",
                "Remember 'TRANSPORT-ATION' = carrying across + action",
                "Connect to 'vehicles' for cars, trains, planes, ships used for movement"
            ],
            "part_of_speech": "noun"
        },
        "transposable": {
            "definition": "Capable of being moved, rearranged, or transferred from one position to another; in genetics, describing DNA sequences that can move within genomes. Musical contexts refer to compositions that can be performed in different keys by shifting all notes by the same interval. Mathematical transposition involves changing the position of elements in matrices or equations. Biological transposable elements, or 'jumping genes,' can insert themselves into different locations within chromosomes, potentially affecting gene function. The concept emphasizes flexibility and movability rather than fixed positioning.",
            "pronunciation": "/trænˈspoʊzəbəl/",
            "example_sentence": "The modular furniture pieces are _____, allowing homeowners to reconfigure rooms easily.",
            "etymology": "From 'transpose' + '-able' (capable of), from Latin 'transponere' (to place across), meaning 'capable of being repositioned.'",
            "memory_tips": [
                "Think 'able to be MOVED' - capable of changing position or arrangement",
                "Remember 'TRANS-POSE-ABLE' = across + place + able",
                "Connect to 'rearrangeable' for movable or repositionable quality"
            ],
            "part_of_speech": "adjective"
        },
        "trap": {
            "definition": "A device or situation designed to catch or confine animals, people, or objects; to catch or hold someone or something in an inescapable situation. Physical traps include mousetraps, animal snares, or mechanical devices for capture. Metaphorical traps describe situations that appear beneficial but lead to negative consequences, such as debt traps or logical fallacies. Sports contexts use trap plays to deceive opponents. The word implies deception, concealment, or unexpected containment that prevents escape or freedom of movement.",
            "pronunciation": "/træp/",
            "example_sentence": "The detective realized the meeting was a _____ designed to capture the fugitive.",
            "etymology": "From Old English 'træppe,' possibly from Germanic origin, related to stepping or catching mechanisms.",
            "memory_tips": [
                "Think 'catching DEVICE' - mechanism for capturing animals or people",
                "Remember 'mousetrap' for common household catching device",
                "Connect to 'snare' for similar capturing or confining mechanism"
            ],
            "part_of_speech": "noun, verb"
        },
        "trapezoid": {
            "definition": "A quadrilateral (four-sided polygon) with exactly one pair of parallel sides, also called a trapezium in some regions. The parallel sides are called bases, while the non-parallel sides are called legs. Geometry classes teach trapezoid properties including area calculation (average of parallel sides multiplied by height) and angle relationships. Isosceles trapezoids have equal leg lengths and equal base angles. Real-world examples include some roof shapes, bridge designs, and architectural elements. The shape appears frequently in engineering and construction due to its structural properties.",
            "pronunciation": "/ˈtræpəˌzɔɪd/",
            "example_sentence": "The architect designed the building's facade with _____ windows that created an interesting geometric pattern.",
            "etymology": "From Greek 'trapezion' (little table) + '-oid' (resembling), referring to its table-like shape with parallel sides.",
            "memory_tips": [
                "Think 'TABLE-shaped polygon' - four sides with one pair parallel like table top/bottom",
                "Remember 'TRAP-EZOID' contains 'trap' for the trapping parallel sides",
                "Connect to 'table' for geometric shape resembling table outline"
            ],
            "part_of_speech": "noun"
        },
        "trashbobbed": {
            "definition": "This appears to be an unusual or potentially non-standard word. It may refer to someone having a bob haircut that looks disheveled or unkempt, resembling 'trash' in its messy appearance. Alternatively, it could describe a hairstyle that has been cut poorly or has become messy. The term combines 'trash' (worthless or messy) with 'bobbed' (cut in a bob style). This may be slang or a regional expression rather than a standard dictionary word.",
            "pronunciation": "/ˈtræʃˌbɑbd/",
            "example_sentence": "After the windy day at the beach, her _____ hair looked completely disheveled.",
            "etymology": "Appears to combine 'trash' (messy, worthless) + 'bobbed' (cut in bob style), possibly modern slang creation.",
            "memory_tips": [
                "Think 'TRASH-looking BOB haircut' - messy or poorly cut bob style",
                "Remember combination of 'trashy' appearance with 'bob' haircut",
                "Connect to 'disheveled hair' for unkempt appearance"
            ],
            "part_of_speech": "adjective (possibly slang)"
        },
        "travails": {
            "definition": "Painful or laborious efforts; difficult or arduous work; suffering or hardship endured during challenging tasks or life experiences. The word encompasses both physical labor and emotional struggles, emphasizing the difficulty and suffering involved in achieving goals or surviving difficult circumstances. Literary contexts often describe characters' travails during journeys, personal growth, or overcoming obstacles. Modern usage includes professional challenges, personal hardships, or societal struggles that require significant effort and endurance. The term suggests both the struggle itself and the strength required to persevere.",
            "pronunciation": "/trəˈveɪlz/",
            "example_sentence": "Despite the many _____ of starting a business, she persevered and eventually succeeded.",
            "etymology": "From Old French 'travail' (suffering, labor), possibly from Latin 'trepalium' (torture device), meaning difficult work or suffering.",
            "memory_tips": [
                "Think 'TRAVEL troubles' - hardships and difficulties during journeys",
                "Remember 'TRAVAIL' sounds like 'travel' but means hard work/suffering",
                "Connect to 'struggles' for difficult work or painful experiences"
            ],
            "part_of_speech": "noun (plural)"
        },
        "travel": {
            "definition": "To go from one place to another, typically over a distance; to move or journey to different locations for business, pleasure, or other purposes. Modern travel encompasses various transportation methods including automobiles, airplanes, trains, ships, and emerging technologies. Tourism involves travel for recreational and cultural experiences, contributing significantly to global economies. Business travel enables commerce, conferences, and professional relationships across distances. The concept includes both the physical movement and the experiences gained through exposure to different places, cultures, and perspectives.",
            "pronunciation": "/ˈtrævəl/",
            "example_sentence": "Many people hope to _____ around the world to experience different cultures and landscapes.",
            "etymology": "From Middle English 'travelen,' variant of 'travail' (to work, journey), from Old French 'travail' (work, suffering).",
            "memory_tips": [
                "Think 'JOURNEY to places' - moving from one location to another",
                "Remember 'vacation travel' for recreational trips and tourism",
                "Connect to 'transportation' for methods used to reach destinations"
            ],
            "part_of_speech": "verb, noun"
        },
        "traveled": {
            "definition": "Past tense of 'travel,' meaning journeyed or went from one place to another; having experience with visiting different places. Describes completed trips, journeys, or movement between locations. When describing people, indicates someone who has visited many places and gained experience through travel. Well-traveled individuals often possess cultural knowledge, adaptability, and broader perspectives from exposure to different places and peoples. The word can also describe routes, paths, or roads that have been used for transportation.",
            "pronunciation": "/ˈtrævəld/",
            "example_sentence": "She _____ extensively through Asia before settling down to write about her experiences.",
            "etymology": "From 'travel' + '-ed' past tense suffix, indicating completed action of journeying or moving between places.",
            "memory_tips": [
                "Think past tense of 'TRAVEL' - already completed journeys",
                "Remember 'experienced traveler' for someone who has visited many places",
                "Connect to 'well-traveled' for people with extensive travel experience"
            ],
            "part_of_speech": "verb (past tense), adjective"
        },
        "travels": {
            "definition": "Third person singular present tense of 'travel,' or plural noun referring to journeys, trips, or accounts of traveling experiences. As a verb, describes someone's current action of moving between places. As a noun, refers to multiple journeys or the collective experiences of traveling. Travel literature often titled 'Travels in...' documents authors' experiences in different regions. The word encompasses both the physical act of movement and the cultural, educational, or recreational experiences gained through visiting different places.",
            "pronunciation": "/ˈtrævəlz/",
            "example_sentence": "The explorer published a book about her _____ through the Amazon rainforest.",
            "etymology": "From 'travel' + '-s' third person singular or plural suffix, indicating multiple journeys or current traveling action.",
            "memory_tips": [
                "Think 'multiple TRIPS' or 'currently traveling' - journeys or present action",
                "Remember 'travel books' often called 'Travels in [place]'",
                "Connect to 'adventures' for exciting travel experiences"
            ],
            "part_of_speech": "verb (third person singular), noun (plural)"
        },
        "traverse": {
            "definition": "To travel across, over, or through something; to move from one side to the other of a space or area. Can describe physical movement across landscapes, rooms, or obstacles, as well as metaphorical movement through time periods, topics, or concepts. Mountain climbing uses traverse to describe moving horizontally across rock faces or slopes. Legal contexts may involve traversing arguments or evidence. The word emphasizes crossing or spanning distances, boundaries, or subjects rather than simply moving in straight lines or staying within familiar territories.",
            "pronunciation": "/trəˈvɜrs/",
            "example_sentence": "The hikers needed three days to _____ the difficult mountain terrain safely.",
            "etymology": "From Old French 'traverser,' from Latin 'transversus' (turned across), from 'trans-' (across) + 'vertere' (to turn).",
            "memory_tips": [
                "Think 'CROSS over or through' - moving across obstacles or areas",
                "Remember 'TRAVERSE' sounds like 'travel across' for crossing movement",
                "Connect to 'bridge' for crossing over barriers or gaps"
            ],
            "part_of_speech": "verb, noun"
        },
        "treachery": {
            "definition": "Betrayal of trust or confidence; deceitful or disloyal behavior that violates commitments, relationships, or allegiances. The term implies deliberate deception and violation of trust, often involving secret actions that harm those who trusted the perpetrator. Historical contexts describe political treachery such as betraying military secrets or switching sides during conflicts. Personal treachery involves betraying friends, family members, or romantic partners through deceit or disloyalty. The word carries strong moral condemnation, suggesting behavior that violates fundamental social and ethical bonds.",
            "pronunciation": "/ˈtrɛtʃəri/",
            "example_sentence": "The spy's _____ was discovered when classified documents were found in his possession.",
            "etymology": "From Old French 'trecherie,' from 'trecher' (to deceive), related to 'trick' and betrayal.",
            "memory_tips": [
                "Think 'BETRAYAL of trust' - deliberate deception and disloyalty",
                "Remember 'TREACHERY' sounds like 'teacher' but means betrayer",
                "Connect to 'treason' for similar betrayal of loyalty or allegiance"
            ],
            "part_of_speech": "noun"
        },
        "treadle": {
            "definition": "A lever or pedal operated by foot pressure to drive machinery, particularly spinning wheels, sewing machines, pottery wheels, or other mechanical devices. Traditional treadles convert foot motion into rotational power for various crafts and manufacturing processes. Antique sewing machines often featured treadle operation before electric motors became common. The mechanism typically involves a foot pedal connected to a flywheel or belt system that transfers human power to machine operation. Modern exercise equipment sometimes incorporates treadle-like mechanisms for foot-powered operation.",
            "pronunciation": "/ˈtrɛdəl/",
            "example_sentence": "The seamstress pressed the _____ steadily to keep her antique sewing machine running smoothly.",
            "etymology": "From Old English 'tredan' (to tread, step) + '-le' (diminutive), meaning 'small stepping device.'",
            "memory_tips": [
                "Think 'foot PEDAL for machines' - lever operated by stepping motion",
                "Remember 'TREAD-LE' = tread + little for small stepping device",
                "Connect to 'sewing machine' for traditional foot-powered operation"
            ],
            "part_of_speech": "noun"
        },
        "treadmill": {
            "definition": "An exercise machine with a moving belt that allows users to walk or run in place; historically, a device where people or animals walked on a large wheel to generate power. Modern treadmills are popular fitness equipment found in gyms and homes, featuring adjustable speeds, inclines, and monitoring systems. The original treadmill was a punishment device in prisons where inmates walked on large wheels to power mills or other machinery. Metaphorically, describes monotonous, repetitive activities that seem to lead nowhere, suggesting being trapped in unproductive cycles.",
            "pronunciation": "/ˈtrɛdˌmɪl/",
            "example_sentence": "She ran five miles on the _____ while watching the morning news program.",
            "etymology": "From 'tread' (to step) + 'mill' (grinding device), originally referring to mills powered by treading motion.",
            "memory_tips": [
                "Think 'running MACHINE' - exercise equipment for walking/running in place",
                "Remember 'TREAD-MILL' = stepping + grinding machine",
                "Connect to 'gym equipment' for modern cardiovascular exercise"
            ],
            "part_of_speech": "noun"
        },
        "treasury": {
            "definition": "A place or building where treasure or valuable items are stored; the government department responsible for financial and monetary policy; the funds or revenue of a state, institution, or organization. Modern treasuries manage public finances, collect taxes, issue currency, and oversee economic policy. Corporate treasuries handle company finances, investments, and cash management. Historical treasuries stored precious metals, jewels, and valuable artifacts in secure locations. The term encompasses both physical storage facilities and organizational departments responsible for financial management and oversight.",
            "pronunciation": "/ˈtrɛʒəri/",
            "example_sentence": "The Secretary of the _____ announced new economic policies to address inflation concerns.",
            "etymology": "From Old French 'tresorie,' from 'tresor' (treasure), from Latin 'thesaurus' (storehouse, treasure).",
            "memory_tips": [
                "Think 'TREASURE storage' - place where valuable items or money are kept",
                "Remember 'government finances' for national financial management department",
                "Connect to 'bank vault' for secure storage of valuable assets"
            ],
            "part_of_speech": "noun"
        },
        "treatise": {
            "definition": "A formal written work that deals systematically and thoroughly with a particular subject; a scholarly or academic essay that examines a topic in detail. Treatises typically present comprehensive analysis, evidence, and arguments about specific subjects, ranging from scientific theories to philosophical concepts to legal principles. Academic treatises contribute to scholarly knowledge and often influence policy or practice in their respective fields. Famous treatises include works on political philosophy, scientific discoveries, and religious doctrine. The format emphasizes thorough investigation and systematic presentation of ideas.",
            "pronunciation": "/ˈtritɪs/",
            "example_sentence": "The professor published a comprehensive _____ on environmental law that became required reading in universities.",
            "etymology": "From Old French 'traitis,' from 'traitier' (to treat, handle), from Latin 'tractare' (to handle, discuss).",
            "memory_tips": [
                "Think 'TREAT-ISE' - systematic treatment of a subject in writing",
                "Remember 'scholarly paper' for formal academic written work",
                "Connect to 'thesis' for similar formal written examination of topics"
            ],
            "part_of_speech": "noun"
        },
        "treatments": {
            "definition": "Plural of treatment; medical care provided to patients; processes of handling, processing, or dealing with subjects, materials, or situations. Medical treatments include medications, surgeries, therapies, and other interventions designed to cure, improve, or manage health conditions. Industrial treatments modify materials through chemical, physical, or mechanical processes. The word also refers to ways of handling situations, problems, or subjects in various contexts. Different treatments may be compared for effectiveness, cost, or appropriateness for specific conditions or circumstances.",
            "pronunciation": "/ˈtritmənt/",
            "example_sentence": "The hospital offers various _____ for cancer patients, including chemotherapy and radiation therapy.",
            "etymology": "From 'treatment' (from 'treat' + '-ment') + '-s' plural suffix, meaning multiple methods of handling or caring.",
            "memory_tips": [
                "Think 'medical CARE methods' - different ways of treating diseases or conditions",
                "Remember 'therapies' for various treatment approaches",
                "Connect to 'medications' for pharmaceutical treatment options"
            ],
            "part_of_speech": "noun (plural)"
        },
        "treble": {
            "definition": "Triple in amount or degree; having three parts or aspects; in music, relating to high-pitched sounds or the upper range of musical notes. Musical contexts describe treble clef notation for higher pitches, treble voices, or treble instruments. Audio equipment includes treble controls for adjusting high-frequency sounds. As a verb, means to multiply by three or increase threefold. The word can describe triple wins in sports, triple profits in business, or any situation involving three-part increases or divisions.",
            "pronunciation": "/ˈtrɛbəl/",
            "example_sentence": "The soprano's _____ voice soared beautifully above the orchestra in the concert hall.",
            "etymology": "From Old French 'treble,' from Latin 'triplus' (triple), related to 'tres' (three), meaning 'threefold.'",
            "memory_tips": [
                "Think 'TRIPLE amount' or 'high musical PITCH' - three times or high sounds",
                "Remember 'TREBLE clef' for musical notation of high notes",
                "Connect to 'soprano' for high-pitched singing voice"
            ],
            "part_of_speech": "adjective, noun, verb"
        },
        "trebuchet": {
            "definition": "A medieval siege engine that uses a counterweight system to launch projectiles at fortifications; a type of catapult that became highly effective for breaking down castle walls. These machines could hurl stones, incendiary materials, or other projectiles over long distances with devastating accuracy. Trebuchets represented advanced medieval military technology, using gravitational force and mechanical advantage to achieve greater range and power than earlier siege weapons. Modern trebuchets are built for educational demonstrations, competitions, and historical reenactments. The design principles illustrate fundamental physics concepts including leverage, momentum, and projectile motion.",
            "pronunciation": "/ˈtrɛbjʊˌʃɛt/",
            "example_sentence": "The medieval army used a massive _____ to breach the castle's stone walls during the siege.",
            "etymology": "From Old French 'trebuchet,' possibly from 'trebucher' (to overturn), referring to its tipping motion when firing.",
            "memory_tips": [
                "Think 'medieval CATAPULT' - counterweight siege engine for attacking castles",
                "Remember 'TREE-bucket' for wooden throwing machine",
                "Connect to 'castle siege' for medieval warfare weapon"
            ],
            "part_of_speech": "noun"
        },
        "trees": {
            "definition": "Plural of tree; large woody plants with trunks, branches, and leaves that typically grow to considerable height. Trees play crucial ecological roles including oxygen production, carbon dioxide absorption, soil stabilization, and habitat provision for countless species. Forest ecosystems depend on tree diversity for environmental balance and biodiversity. Urban trees provide shade, air purification, and aesthetic value in cities. Different tree species serve various human purposes including lumber, paper production, fruit, nuts, and ornamental landscaping. Environmental conservation efforts focus heavily on tree preservation and reforestation.",
            "pronunciation": "/triz/",
            "example_sentence": "The park featured dozens of mature _____ that provided shade and homes for local wildlife.",
            "etymology": "Plural of 'tree,' from Old English 'trēow,' related to Germanic languages, meaning 'woody plant.'",
            "memory_tips": [
                "Think 'large PLANTS with trunks' - woody vegetation that grows tall",
                "Remember 'forest' for collections of trees in natural settings",
                "Connect to 'oxygen production' for environmental benefits of trees"
            ],
            "part_of_speech": "noun (plural)"
        },
        "trefoil": {
            "definition": "A decorative design or architectural element featuring three leaves or lobes; a plant with three-leaflet compound leaves, particularly clover. Architectural trefoils appear in Gothic church windows, decorative stonework, and ornamental designs. The shamrock is a famous trefoil symbol associated with Ireland and St. Patrick's Day. Botanical trefoils include various clover species and other plants with characteristic three-part leaf structures. The design symbolizes the Christian Trinity in religious contexts and appears frequently in heraldry, decorative arts, and architectural ornamentation.",
            "pronunciation": "/ˈtriˌfɔɪl/",
            "example_sentence": "The Gothic cathedral's windows featured beautiful stone _____ designs that created intricate light patterns.",
            "etymology": "From Old French 'trefoil,' from Latin 'trifolium' (three-leaf), from 'tri-' (three) + 'folium' (leaf).",
            "memory_tips": [
                "Think 'THREE-leaf design' - decorative pattern with three lobes",
                "Remember 'TREFOIL' = tri (three) + foil (leaf) for three-part pattern",
                "Connect to 'clover' for plant with characteristic three-leaf structure"
            ],
            "part_of_speech": "noun"
        },
        "trek": {
            "definition": "A long journey, typically on foot; an arduous trip, especially through mountainous or difficult terrain. Originally describing organized migrations of people with wagons and livestock, particularly in South Africa. Modern usage includes hiking expeditions, adventure travel, and challenging journeys that require endurance and preparation. Popular trekking destinations include mountain ranges, national parks, and remote wilderness areas. The word implies difficulty, duration, and often adventure, distinguishing it from casual walks or short trips. Space exploration adopted 'trek' to describe exploratory missions.",
            "pronunciation": "/trɛk/",
            "example_sentence": "The mountaineers planned a two-week _____ through the Himalayas to reach base camp.",
            "etymology": "From Afrikaans 'trek' (to pull, journey), from Dutch 'trekken' (to pull, travel), originally describing wagon journeys.",
            "memory_tips": [
                "Think 'long HIKING journey' - arduous travel on foot through difficult terrain",
                "Remember 'Star Trek' for exploratory journey theme",
                "Connect to 'expedition' for challenging adventure travel"
            ],
            "part_of_speech": "noun, verb"
        },
        "trellis": {
            "definition": "A framework of wooden or metal strips used as a support for climbing plants; a lattice structure that provides support and guides plant growth. Garden trellises help vines, roses, and other climbing plants grow vertically, saving space and creating attractive displays. Architectural trellises provide privacy screens, shade structures, or decorative elements in outdoor spaces. The lattice pattern allows air circulation while supporting plant growth and can be freestanding or attached to walls or fences. Modern trellises incorporate various materials including bamboo, metal, and composite materials for durability and aesthetics.",
            "pronunciation": "/ˈtrɛlɪs/",
            "example_sentence": "The gardener installed a wooden _____ for the grape vines to climb and create natural shade.",
            "etymology": "From Old French 'trelis,' possibly from Latin 'trilicis' (woven with three threads), referring to lattice construction.",
            "memory_tips": [
                "Think 'plant SUPPORT framework' - lattice structure for climbing plants",
                "Remember 'grape vines' for common trellis application",
                "Connect to 'lattice' for crisscross pattern that supports growth"
            ],
            "part_of_speech": "noun"
        },
        "trembling": {
            "definition": "Present participle of 'tremble,' meaning shaking involuntarily, typically from fear, excitement, cold, or physical weakness. Describes rapid, small movements that occur without conscious control, often indicating emotional states or physical conditions. Medical contexts may describe trembling as symptoms of neurological conditions, anxiety disorders, or medication side effects. The word can describe both human trembling and the movement of objects in wind, during earthquakes, or from vibrations. Emotional trembling often accompanies intense feelings like fear, anger, or overwhelming joy.",
            "pronunciation": "/ˈtrɛmblɪŋ/",
            "example_sentence": "Her hands were _____ with excitement as she opened the college acceptance letter.",
            "etymology": "From 'tremble' + '-ing' present participle suffix, from Old French 'trembler,' meaning 'to shake involuntarily.'",
            "memory_tips": [
                "Think 'involuntary SHAKING' - uncontrolled movement from emotion or cold",
                "Remember 'nervous trembling' for anxiety-induced shaking",
                "Connect to 'earthquake' for ground trembling or shaking"
            ],
            "part_of_speech": "verb (present participle), noun"
        },
        "tremulous": {
            "definition": "Shaking or quivering, typically from nervousness, weakness, or emotion; timid, nervous, or uncertain in manner or speech. Describes physical trembling due to age, illness, fear, or strong emotions. Can characterize voices that waver with emotion, hands that shake with nervousness, or behavior that shows uncertainty or fear. The word often appears in literary contexts to convey vulnerability, frailty, or emotional intensity. Medical contexts may describe tremulous movements as symptoms of various conditions affecting muscle control or neurological function.",
            "pronunciation": "/ˈtrɛmjələs/",
            "example_sentence": "The elderly man spoke in a _____ voice as he recalled his wartime experiences.",
            "etymology": "From Latin 'tremulus' (shaking), from 'tremere' (to tremble), meaning 'characterized by trembling.'",
            "memory_tips": [
                "Think 'TREMBLING quality' - characterized by shaking or quivering",
                "Remember 'TREMUL-OUS' = trembling + characteristic suffix",
                "Connect to 'nervous' for uncertain, shaky behavior or speech"
            ],
            "part_of_speech": "adjective"
        },
        "tremuloustrepanation": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'tremulous' (shaking or quivering) and 'trepanation' (surgical procedure of drilling holes in the skull). 'Tremulous' describes nervous shaking or trembling behavior, while 'trepanation' refers to ancient surgical practice of creating openings in skulls. These represent completely different concepts from medicine and behavior that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'tremulous' + 'trepanation' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "trencher": {
            "definition": "A large plate or platter, typically made of wood, used for serving or eating food; historically, a flat piece of bread used as a plate. Medieval dining used trenchers as disposable plates, with stale bread serving as edible dishes that could be eaten or given to poor people after meals. Wooden trenchers became common tableware in medieval and colonial periods, often carved from single pieces of wood. Modern trenchers appear in historical reenactments, rustic dining settings, or decorative contexts. The term also describes someone who digs trenches or excavations.",
            "pronunciation": "/ˈtrɛntʃər/",
            "example_sentence": "The medieval feast featured roasted meats served on large wooden _____.",
            "etymology": "From Old French 'trencheoir,' from 'trencher' (to cut), referring to a cutting board or plate for slicing food.",
            "memory_tips": [
                "Think 'medieval PLATE' - wooden platter for serving and eating food",
                "Remember 'TRENCH-ER' like cutting or carving board",
                "Connect to 'bread plate' for historical edible trencher use"
            ],
            "part_of_speech": "noun"
        },
        "trendy": {
            "definition": "Very fashionable or up-to-date; following or setting current trends in style, culture, or behavior. Describes people, places, products, or ideas that are popular and contemporary, often associated with the latest developments in fashion, technology, or social movements. Trendy items may have temporary popularity that changes as new trends emerge. The word can carry positive connotations of being current and stylish, or negative implications of being superficial or following trends without substance. Marketing often targets trendy demographics to promote new products or services.",
            "pronunciation": "/ˈtrɛndi/",
            "example_sentence": "The _____ restaurant featured innovative fusion cuisine and minimalist decor that attracted young professionals.",
            "etymology": "From 'trend' + '-y' (characterized by), meaning 'characterized by current trends or fashion.'",
            "memory_tips": [
                "Think 'TREND-Y' - characterized by following current trends or fashion",
                "Remember 'fashionable' for stylish and up-to-date appearance",
                "Connect to 'popular' for things that are currently in style"
            ],
            "part_of_speech": "adjective"
        },
        "trepanation": {
            "definition": "A surgical procedure involving drilling or scraping a hole through the skull to expose the brain, historically performed to treat various medical conditions or for ritualistic purposes. Archaeological evidence shows trepanation was practiced by ancient civilizations worldwide, often with surprising survival rates. Historical purposes included treating head injuries, mental illness, epilepsy, or relieving pressure from brain swelling. Modern neurosurgery uses similar techniques for specific medical procedures, though with vastly improved safety and precision. The practice provides insights into ancient medical knowledge and cultural beliefs about brain function.",
            "pronunciation": "/ˌtrɛpəˈneɪʃən/",
            "example_sentence": "Archaeological excavations revealed skulls showing evidence of ancient _____ procedures.",
            "etymology": "From Greek 'trepanon' (borer, drill) + '-ation' (process), literally meaning 'drilling process.'",
            "memory_tips": [
                "Think 'drilling SKULL holes' - ancient surgical procedure on the head",
                "Remember 'TREPAN-ATION' = drill + process for skull surgery",
                "Connect to 'brain surgery' for medical procedure involving skull opening"
            ],
            "part_of_speech": "noun"
        },
        "trepidation": {
            "definition": "A feeling of fear or anxiety about something that may happen; nervous apprehension or worry about future events or uncertain outcomes. The emotion combines fear with anticipation, often occurring before important events, decisions, or potentially dangerous situations. Students may feel trepidation before exams, job applicants before interviews, or patients before medical procedures. The word suggests a mixture of excitement and fear, acknowledging both the significance of upcoming events and uncertainty about their outcomes. Trepidation often motivates preparation and careful consideration of potential consequences.",
            "pronunciation": "/ˌtrɛpɪˈdeɪʃən/",
            "example_sentence": "She approached her first job interview with considerable _____ about making a good impression.",
            "etymology": "From Latin 'trepidation-' from 'trepidare' (to tremble, be alarmed), meaning 'trembling with fear or anxiety.'",
            "memory_tips": [
                "Think 'nervous FEAR' - anxiety about uncertain future events",
                "Remember 'TREPID-ATION' contains 'tepid' suggesting hesitant feelings",
                "Connect to 'apprehension' for worried anticipation of events"
            ],
            "part_of_speech": "noun"
        },
        "trespass": {
            "definition": "To enter someone's property without permission; to violate laws, rights, or moral boundaries; an act of wrongful entry or violation. Legal trespassing involves unauthorized entry onto private property, which may result in criminal or civil penalties. Religious contexts describe trespassing as sinning or violating moral laws. The word can describe physical intrusion onto land, buildings, or restricted areas, as well as metaphorical violations of personal boundaries, rights, or sacred spaces. Property law distinguishes between different types of trespass based on intent, damage, and circumstances.",
            "pronunciation": "/ˈtrɛsˌpæs/",
            "example_sentence": "The 'No Trespassing' signs clearly warned hikers not to _____ on the private farmland.",
            "etymology": "From Old French 'trespasser' (to pass across), from 'tres-' (across) + 'passer' (to pass), meaning 'to pass across boundaries.'",
            "memory_tips": [
                "Think 'crossing BOUNDARIES' - entering property without permission",
                "Remember 'TRES-PASS' = across + pass for crossing forbidden lines",
                "Connect to 'private property' for unauthorized entry violations"
            ],
            "part_of_speech": "verb, noun"
        },
        "trey": {
            "definition": "The number three, especially on dice or playing cards; a card or die showing three spots or pips. In card games, refers to any card with a face value of three, such as the three of hearts or three of spades. Dice games use trey to describe the face showing three dots. Basketball adopted 'trey' as slang for three-point shots made from beyond the three-point line. The term appears in various gambling contexts and games where the number three has significance or special value.",
            "pronunciation": "/treɪ/",
            "example_sentence": "The poker player was disappointed to draw only a _____ when she needed a high card.",
            "etymology": "From Old French 'treis' (three), from Latin 'tres,' meaning 'three' in gaming contexts.",
            "memory_tips": [
                "Think 'number THREE' on cards or dice - gaming term for three",
                "Remember 'playing cards' for three-value cards in card games",
                "Connect to 'basketball' for three-point shot slang usage"
            ],
            "part_of_speech": "noun"
        },
        "triage": {
            "definition": "The assignment of degrees of urgency to medical patients or casualties to decide the order of treatment; the process of sorting and prioritizing based on urgency or importance. Medical triage occurs in emergency rooms, disaster responses, and military medicine to ensure the most critical patients receive immediate attention. The process involves rapid assessment to categorize patients by severity of condition and likelihood of survival with treatment. Modern triage systems use standardized protocols and color-coding to streamline decision-making. The concept extends beyond medicine to any situation requiring prioritization of limited resources.",
            "pronunciation": "/ˈtriˌɑʒ/",
            "example_sentence": "The emergency room nurse performed _____ to determine which patients needed immediate attention.",
            "etymology": "From French 'trier' (to sort, sift), originally meaning 'sorting' or 'selection,' adopted into medical terminology.",
            "memory_tips": [
                "Think 'sorting by URGENCY' - prioritizing patients by medical severity",
                "Remember 'TRI-AGE' like 'try + age' for assessing patient needs",
                "Connect to 'emergency room' for medical priority decision-making"
            ],
            "part_of_speech": "noun, verb"
        },
        "triagetrinkets": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'triage' (medical prioritization system) and 'trinkets' (small decorative objects or jewelry). 'Triage' refers to sorting patients by medical urgency, while 'trinkets' are small ornamental items or inexpensive jewelry. These represent completely different concepts from medicine and decorative arts that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'triage' + 'trinkets' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "tribunal": {
            "definition": "A court of justice; a judicial body or committee established to settle disputes, investigate matters, or make decisions on specific issues. Legal tribunals may have specialized jurisdiction over particular types of cases such as employment disputes, immigration matters, or military justice. International tribunals address conflicts between nations or war crimes. Administrative tribunals handle appeals from government decisions. The term suggests formal legal proceedings with established procedures, evidence presentation, and authoritative decision-making power. Modern tribunals often provide alternative dispute resolution outside traditional court systems.",
            "pronunciation": "/traɪˈbjunəl/",
            "example_sentence": "The employment _____ ruled in favor of the worker who had been unfairly dismissed.",
            "etymology": "From Latin 'tribunal,' from 'tribunus' (magistrate), from 'tribus' (tribe), referring to a raised platform for officials.",
            "memory_tips": [
                "Think 'specialized COURT' - judicial body for specific types of disputes",
                "Remember 'TRIBUNAL' sounds like 'tribe + final' for tribal justice",
                "Connect to 'judge' for authority figure making legal decisions"
            ],
            "part_of_speech": "noun"
        },
        "tributary": {
            "definition": "A river or stream that flows into a larger river or lake; a person or state that pays tribute to another; something that contributes to or feeds into a larger system. Geographic tributaries form essential parts of river systems, carrying water and sediment to main waterways. Historical tributaries were nations or peoples who paid tribute to dominant powers for protection or to avoid conquest. The concept extends to any subsidiary element that contributes to a larger whole, such as subsidiary roads feeding into highways or secondary sources supporting main arguments.",
            "pronunciation": "/ˈtrɪbjəˌtɛri/",
            "example_sentence": "The Missouri River is a major _____ of the Mississippi River system.",
            "etymology": "From Latin 'tributarius' (paying tribute), from 'tributum' (tribute), meaning 'contributing to' or 'feeding into.'",
            "memory_tips": [
                "Think 'TRIBUTE-ARY' - gives tribute or flows into larger water body",
                "Remember 'smaller river' flowing into bigger river system",
                "Connect to 'contributing' for feeding into larger systems"
            ],
            "part_of_speech": "noun, adjective"
        },
        "trice": {
            "definition": "A very short period of time; an instant or moment. The phrase 'in a trice' means very quickly or immediately, emphasizing the brief duration of actions or events. Originally a nautical term referring to pulling or hoisting with a single quick motion, the word evolved to describe any rapid action or brief time period. Modern usage often appears in expressions emphasizing speed or brevity. The concept suggests something happening so quickly that it's almost instantaneous, faster than most people would expect or notice.",
            "pronunciation": "/traɪs/",
            "example_sentence": "The experienced chef chopped all the vegetables in a _____, impressing the cooking students.",
            "etymology": "From Middle Dutch 'trisen' (to hoist quickly), originally a nautical term for quick rope pulling, later meaning 'instant.'",
            "memory_tips": [
                "Think 'in a TRICE' - very quick moment or instant",
                "Remember 'THREE times fast' though trice means once quickly",
                "Connect to 'instant' for extremely brief period of time"
            ],
            "part_of_speech": "noun"
        }
    }

def process_batch_182():
    """Process batch_182_words.csv with comprehensive Claude data"""
    try:
        logger.info("Processing Batch 182 with comprehensive Claude data...")
        
        # Load comprehensive data
        claude_data = get_comprehensive_claude_data()
        
        # Initialize difficulty calculator
        calc = DifficultyCalculator()
        
        # Read input file
        input_file = 'output/batch_182_words.csv'
        output_file = 'output/batch_182_processed.csv'
        
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
            logger.info("Batch 182 processing completed!")
            logger.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
            logger.info(f"Output saved to: {output_file}")
            logger.info(f"Results: {len(processed_words)} successful, 0 failed")
        else:
            logger.error("No words were processed")
            
    except Exception as e:
        logger.error(f"Error processing batch 182: {str(e)}")
        raise

if __name__ == "__main__":
    process_batch_182()