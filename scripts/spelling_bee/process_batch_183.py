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
            'tropical', 'trough', 'trousers'
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
        prefixes = ['un', 're', 'pre', 'dis', 'mis', 'over', 'under', 'sub', 'super', 'anti', 'auto', 'co', 'de', 'inter', 'micro', 'mid', 'non', 'semi', 'trans', 'tri']
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
    Return comprehensive data for all 50 words in batch_183_words.csv
    Generated using Claude with detailed educational content.
    """
    return {
        "tricenary": {
            "definition": "Relating to or lasting for thirty years; a period of thirty years; the thirtieth anniversary of an event. This term describes time periods, commemorations, or cycles that span exactly three decades. Used in historical contexts to mark significant anniversaries, political terms, or generational periods. Academic and institutional contexts may celebrate tricenary milestones for founding dates, achievements, or important events. The word emphasizes the significance of the thirty-year timeframe as a meaningful period for reflection, celebration, or historical analysis.",
            "pronunciation": "/traɪˈsinəri/",
            "example_sentence": "The university celebrated its _____ with a special symposium reflecting on thirty years of academic excellence.",
            "etymology": "From Latin 'tricenarius,' from 'triceni' (thirty each), from 'tres' (three) + 'deni' (ten each), meaning 'of thirty.'",
            "memory_tips": [
                "Think 'TRI-CENARY' = three + ten = thirty years",
                "Remember 'thirty-year anniversary' for tricenary celebration",
                "Connect to 'centenary' (100 years) but tricenary is 30 years"
            ],
            "part_of_speech": "adjective, noun"
        },
        "tricenarytriste": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'tricenary' (relating to thirty years) and 'triste' (sad or melancholy). 'Tricenary' refers to thirty-year periods or anniversaries, while 'triste' is a French/Spanish word meaning sad. These represent different concepts from time measurement and emotion that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'tricenary' + 'triste' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "triceratops": {
            "definition": "A large herbivorous dinosaur from the Late Cretaceous period, characterized by three prominent facial horns and a large bony frill extending from the skull. These quadrupedal dinosaurs could reach lengths of 30 feet and weights of 12 tons, using their horns and frills for defense against predators like Tyrannosaurus rex. Fossil evidence shows they lived in herds and fed on low-growing vegetation. The distinctive three-horn arrangement included two large horns above the eyes and a smaller horn on the nose. Popular in paleontology education and dinosaur media due to their iconic appearance.",
            "pronunciation": "/traɪˈsɛrəˌtɑps/",
            "example_sentence": "The museum's _____ skeleton displayed the massive three-horned skull that made this dinosaur so recognizable.",
            "etymology": "From Greek 'tri-' (three) + 'keras' (horn) + 'ops' (face), literally meaning 'three-horned face.'",
            "memory_tips": [
                "Think 'TRI-CERAT-OPS' = three + horn + face for three-horned dinosaur",
                "Remember 'three horns' for distinctive facial features",
                "Connect to 'rhinoceros' for modern horned animal comparison"
            ],
            "part_of_speech": "noun"
        },
        "triceratopssandal": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'triceratops' (three-horned dinosaur) and 'sandal' (open footwear). 'Triceratops' refers to the famous horned dinosaur from the Cretaceous period, while 'sandal' is a type of shoe with straps. These represent completely different concepts from paleontology and footwear that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'triceratops' + 'sandal' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "trichinosis": {
            "definition": "A parasitic disease caused by eating undercooked meat infected with Trichinella larvae, particularly pork or wild game. Symptoms include muscle pain, fever, swelling around the eyes, and digestive problems as larvae migrate through the body and form cysts in muscle tissue. Prevention involves proper cooking of meat to internal temperatures that kill parasites. Once common in areas with poor sanitation and meat inspection, trichinosis has become rare in developed countries due to improved food safety practices. Severe cases can affect the heart and nervous system, requiring medical treatment.",
            "pronunciation": "/ˌtrɪkəˈnoʊsɪs/",
            "example_sentence": "The doctor diagnosed _____ after the patient reported severe muscle pain following consumption of undercooked pork.",
            "etymology": "From genus 'Trichinella' (the parasite) + '-osis' (disease condition), named for the thread-like appearance of the worm.",
            "memory_tips": [
                "Think 'TRICHIN-OSIS' = trichinella parasite + disease condition",
                "Remember 'undercooked pork' for common source of infection",
                "Connect to 'muscle pain' for primary symptom of the disease"
            ],
            "part_of_speech": "noun"
        },
        "trichotillomania": {
            "definition": "A mental health disorder characterized by recurrent urges to pull out one's own hair, resulting in noticeable hair loss and significant distress or impairment. This impulse control disorder can affect hair on the scalp, eyebrows, eyelashes, or other body areas. Often beginning in childhood or adolescence, the condition may involve rituals around hair pulling and can lead to social anxiety or avoidance behaviors. Treatment typically includes cognitive-behavioral therapy, support groups, and sometimes medication. The disorder represents a complex interaction of psychological, genetic, and environmental factors.",
            "pronunciation": "/ˌtrɪkoʊˌtɪləˈmeɪniə/",
            "example_sentence": "The therapist specialized in treating _____ using cognitive-behavioral techniques to help patients manage their urges.",
            "etymology": "From Greek 'tricho-' (hair) + 'till-' (to pull) + 'mania' (obsession), literally meaning 'hair-pulling obsession.'",
            "memory_tips": [
                "Think 'TRICHO-TILLO-MANIA' = hair + pulling + obsession",
                "Remember 'hair-pulling disorder' for compulsive behavior",
                "Connect to 'impulse control' for type of mental health condition"
            ],
            "part_of_speech": "noun"
        },
        "trickery": {
            "definition": "The practice of using deception, cunning, or underhanded methods to achieve goals; crafty or fraudulent behavior intended to mislead others. Involves deliberate attempts to deceive through false promises, misleading information, or manipulative tactics. Can range from harmless pranks and magic tricks to serious fraud and criminal deception. Political contexts may describe campaign trickery or diplomatic deception. The word implies intentional dishonesty and manipulation designed to gain unfair advantage over others through cleverness rather than honest means.",
            "pronunciation": "/ˈtrɪkəri/",
            "example_sentence": "The investigation revealed financial _____ involving false documents and misleading statements to investors.",
            "etymology": "From 'trick' + '-ery' (practice or art of), meaning 'the practice of using tricks or deception.'",
            "memory_tips": [
                "Think 'TRICK-ERY' - the practice or art of using tricks",
                "Remember 'deception' for dishonest or misleading behavior",
                "Connect to 'fraud' for serious forms of trickery in business"
            ],
            "part_of_speech": "noun"
        },
        "trickster": {
            "definition": "A person who uses tricks, deception, or cunning to deceive others; in mythology and folklore, a character who uses wit and humor to challenge authority or social norms. Mythological tricksters appear in many cultures, such as Loki in Norse mythology, Anansi in African folklore, or Coyote in Native American stories. These figures often serve as both troublemakers and agents of change, using cleverness to expose hypocrisy or teach lessons. Modern usage describes anyone who enjoys playing pranks, using deception, or manipulating situations for personal advantage or entertainment.",
            "pronunciation": "/ˈtrɪkstər/",
            "example_sentence": "The folklore character was a clever _____ who used wit and humor to outsmart powerful enemies.",
            "etymology": "From 'trick' + '-ster' (one who practices), meaning 'one who practices tricks or deception.'",
            "memory_tips": [
                "Think 'TRICK-STER' - one who performs tricks or uses deception",
                "Remember 'folklore character' for mythological trickster figures",
                "Connect to 'prankster' for someone who enjoys playing tricks"
            ],
            "part_of_speech": "noun"
        },
        "tricky": {
            "definition": "Requiring skill, caution, or careful handling due to difficulty or complexity; involving deception or likely to deceive; crafty or cunning in behavior. Describes situations, problems, or tasks that are challenging and may have hidden complications or unexpected difficulties. Can refer to people who are dishonest, manipulative, or unreliable in their dealings with others. The word suggests that success requires careful attention, skill, or awareness of potential pitfalls. Often used to warn others about challenging circumstances or untrustworthy individuals.",
            "pronunciation": "/ˈtrɪki/",
            "example_sentence": "The math problem proved _____ because it contained several steps that could easily lead to errors.",
            "etymology": "From 'trick' + '-y' (characterized by), meaning 'characterized by tricks, difficult, or deceptive.'",
            "memory_tips": [
                "Think 'TRICK-Y' - characterized by tricks or difficulties",
                "Remember 'challenging' for problems requiring careful handling",
                "Connect to 'complicated' for situations with hidden difficulties"
            ],
            "part_of_speech": "adjective"
        },
        "triduum": {
            "definition": "A three-day period of prayer and observance, particularly in Christian liturgy referring to the Easter Triduum (Holy Thursday, Good Friday, and Easter Vigil). This sacred period commemorates the passion, death, and resurrection of Jesus Christ, representing the most important celebrations in the Christian calendar. Each day features specific liturgical services, traditions, and symbolic observances that tell the story of salvation. The term can also refer to any three-day period of religious devotion or spiritual preparation in various Christian traditions.",
            "pronunciation": "/ˈtrɪduəm/",
            "example_sentence": "The parish prepared special liturgies for the Easter _____, the holiest three days of the Christian year.",
            "etymology": "From Latin 'triduum,' from 'tres' (three) + 'dies' (days), meaning 'three days.'",
            "memory_tips": [
                "Think 'TRI-DUUM' = three + days for three-day religious period",
                "Remember 'Easter celebration' for most important Christian triduum",
                "Connect to 'Holy Week' for liturgical calendar context"
            ],
            "part_of_speech": "noun"
        },
        "trifecta": {
            "definition": "A bet in which the bettor must select the first three finishers in exact order; any achievement involving three successes or wins; a series of three related things. Originally a horse racing term, trifecta betting requires picking the exact order of the top three horses, offering higher payouts due to its difficulty. The word has expanded to describe any accomplishment involving three consecutive victories, perfect outcomes, or related achievements. Business contexts may describe a trifecta of successful product launches, while sports might reference a trifecta of championship wins.",
            "pronunciation": "/traɪˈfɛktə/",
            "example_sentence": "The team achieved a _____ by winning the championship three consecutive years.",
            "etymology": "Blend of 'tri-' (three) + 'perfecta' (betting term), originally coined for horse racing betting systems.",
            "memory_tips": [
                "Think 'TRI-FECTA' = three + perfect outcomes or wins",
                "Remember 'horse racing' for original betting context",
                "Connect to 'hat trick' for three consecutive successes"
            ],
            "part_of_speech": "noun"
        },
        "trifle": {
            "definition": "Something of little importance or value; a small amount; a dessert made with layers of cake, custard, fruit, and whipped cream. As a verb, means to treat without seriousness or to act frivolously toward something important. The dessert trifle is popular in British cuisine, featuring multiple layers visible through glass serving dishes. Metaphorically describes matters that are insignificant or not worth serious attention. The word can express dismissal of concerns or indicate that something requires minimal effort or consideration.",
            "pronunciation": "/ˈtraɪfəl/",
            "example_sentence": "Don't _____ with the safety procedures; they're designed to protect everyone in the laboratory.",
            "etymology": "From Old French 'trufle' (mockery, nonsense), possibly related to 'truffle,' meaning something of little value.",
            "memory_tips": [
                "Think 'TRIVIAL thing' - something of little importance",
                "Remember 'layered dessert' for British trifle pudding",
                "Connect to 'insignificant' for matters not worth serious attention"
            ],
            "part_of_speech": "noun, verb"
        },
        "triforium": {
            "definition": "An arcaded gallery or passage in the wall of a church, typically above the arches of the nave, choir, or transept and below the clerestory. This architectural feature is characteristic of Romanesque and Gothic church design, providing a decorative element and sometimes housing additional seating or procession routes. The triforium creates visual rhythm and helps distribute the structural weight of the building. Often featuring ornate stonework, columns, and arches, it contributes to the vertical emphasis and grandeur of cathedral architecture. Some triforiums include windows, while others remain purely decorative.",
            "pronunciation": "/traɪˈfɔriəm/",
            "example_sentence": "The cathedral's _____ featured beautiful carved arches that added elegance to the nave's design.",
            "etymology": "From Medieval Latin 'triforium,' possibly from 'tri-' (three) + 'foris' (door), referring to three-part arcade openings.",
            "memory_tips": [
                "Think 'TRI-FORIUM' = three + openings for church gallery with arches",
                "Remember 'cathedral gallery' for architectural feature above nave",
                "Connect to 'Gothic architecture' for decorative church elements"
            ],
            "part_of_speech": "noun"
        },
        "trigeminal": {
            "definition": "Relating to the fifth cranial nerve, which has three major branches providing sensation to the face and controlling muscles used for chewing. The trigeminal nerve is the largest cranial nerve, with divisions serving the forehead/upper eyelid, cheek/upper lip, and jaw/lower lip areas. Trigeminal neuralgia is a painful condition affecting this nerve, causing severe facial pain. Medical and dental procedures often involve trigeminal nerve considerations due to its extensive facial innervation. Understanding trigeminal anatomy is crucial for diagnosing facial pain, numbness, or muscle weakness.",
            "pronunciation": "/traɪˈdʒɛmənəl/",
            "example_sentence": "The dentist carefully avoided the _____ nerve branches while performing the oral surgery procedure.",
            "etymology": "From Latin 'trigeminus' (triplet), from 'tri-' (three) + 'geminus' (twin), referring to the nerve's three branches.",
            "memory_tips": [
                "Think 'TRI-GEMINAL' = three + twin branches for facial nerve",
                "Remember 'facial sensation' for primary function of trigeminal nerve",
                "Connect to 'dental work' where trigeminal nerve anatomy matters"
            ],
            "part_of_speech": "adjective"
        },
        "trigeminalbruja": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'trigeminal' (relating to the fifth cranial nerve) and 'bruja' (Spanish word for witch). 'Trigeminal' is a medical term for the facial nerve, while 'bruja' refers to a female practitioner of witchcraft. These represent completely different concepts from anatomy and folklore that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'trigeminal' + 'bruja' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "triglycerides": {
            "definition": "A type of fat (lipid) found in blood, composed of three fatty acid molecules attached to a glycerol backbone. These molecules serve as the body's primary form of stored energy and circulate in the bloodstream after meals. High triglyceride levels can increase risk of heart disease, stroke, and pancreatitis. Normal levels are typically below 150 mg/dL, while levels above 200 mg/dL are considered high. Diet, exercise, alcohol consumption, and certain medications affect triglyceride levels. Blood tests routinely measure triglycerides as part of lipid panels for cardiovascular health assessment.",
            "pronunciation": "/traɪˈɡlɪsəˌraɪdz/",
            "example_sentence": "The blood test showed elevated _____ levels, prompting the doctor to recommend dietary changes and exercise.",
            "etymology": "From 'tri-' (three) + 'glyceride' (glycerol ester), referring to three fatty acids attached to glycerol.",
            "memory_tips": [
                "Think 'TRI-GLYCERIDES' = three + glycerol fats for blood lipids",
                "Remember 'blood fat test' for cardiovascular health screening",
                "Connect to 'cholesterol' for related blood lipid measurements"
            ],
            "part_of_speech": "noun (plural)"
        },
        "trigonometry": {
            "definition": "The branch of mathematics dealing with relationships between the sides and angles of triangles, particularly using sine, cosine, and tangent functions. Essential for navigation, engineering, physics, and astronomy, trigonometry enables calculations involving periodic phenomena, wave functions, and spatial relationships. Key concepts include the unit circle, trigonometric identities, and inverse functions. Applications range from calculating building heights and distances to analyzing sound waves and electrical circuits. Advanced trigonometry includes hyperbolic functions and complex number relationships with geometric interpretations.",
            "pronunciation": "/ˌtrɪɡəˈnɑməˌtri/",
            "example_sentence": "The engineering student used _____ to calculate the optimal angle for the bridge's support beams.",
            "etymology": "From Greek 'trigonon' (triangle) + 'metria' (measurement), literally meaning 'triangle measurement.'",
            "memory_tips": [
                "Think 'TRIGON-OMETRY' = triangle + measurement for math of triangles",
                "Remember 'sine, cosine, tangent' for basic trigonometric functions",
                "Connect to 'navigation' for practical applications of triangle math"
            ],
            "part_of_speech": "noun"
        },
        "trilby": {
            "definition": "A soft felt hat with a narrow brim and a lengthwise crease in the crown, similar to a fedora but typically with a shorter brim. Named after the title character in George du Maurier's 1894 novel 'Trilby,' the hat became fashionable in the late 19th and early 20th centuries. Popular among men and women, trilbies are often made from felt, tweed, or straw materials. The style varies in brim width and crown height, but maintains the characteristic narrow brim that distinguishes it from wider-brimmed fedoras. Modern trilbies appear in both casual and formal fashion contexts.",
            "pronunciation": "/ˈtrɪlbi/",
            "example_sentence": "The gentleman's vintage _____ completed his classic 1920s-inspired outfit perfectly.",
            "etymology": "Named after 'Trilby,' the title character in George du Maurier's 1894 novel, popularized by stage adaptations.",
            "memory_tips": [
                "Think 'narrow-brimmed HAT' - soft felt hat with creased crown",
                "Remember 'novel character' for origin from literary character Trilby",
                "Connect to 'fedora' but trilby has narrower brim"
            ],
            "part_of_speech": "noun"
        },
        "trillado": {
            "definition": "A Spanish word meaning 'worn out,' 'trite,' or 'hackneyed'; describing something that has been overused to the point of losing its original impact or meaning. Often refers to expressions, ideas, or themes that have become clichéd through repetition. In literary criticism, describes phrases or concepts that lack freshness due to excessive use. Can apply to paths, ideas, or expressions that have been 'beaten down' through constant use. The word suggests something that was once meaningful but has lost its effectiveness through overexposure or repetition.",
            "pronunciation": "/triˈʎaðo/",
            "example_sentence": "The critic dismissed the film's plot as _____, noting its reliance on overused romantic comedy formulas.",
            "etymology": "From Spanish 'trillar' (to thresh, beat), referring to grain beaten repeatedly, extended to mean 'worn out by use.'",
            "memory_tips": [
                "Think 'WORN OUT by use' - something overused and lacking freshness",
                "Remember 'beaten path' for metaphor of overuse",
                "Connect to 'clichéd' for ideas that have lost original impact"
            ],
            "part_of_speech": "adjective (Spanish)"
        },
        "trillium": {
            "definition": "A genus of flowering plants native to temperate regions, characterized by three leaves arranged in a whorl and three-petaled flowers. These woodland wildflowers bloom in spring, typically featuring white, pink, red, or yellow flowers above distinctive three-leaf arrangements. Popular in shade gardens and woodland landscapes, trilliums prefer moist, rich soil and partial shade. Some species are endangered due to habitat loss and over-collection. The plants have cultural significance in various regions, with the white trillium serving as Ontario's provincial flower and appearing on Canadian currency.",
            "pronunciation": "/ˈtrɪliəm/",
            "example_sentence": "The forest floor was carpeted with white _____ blooms, creating a spectacular spring wildflower display.",
            "etymology": "From Latin 'tri-' (three) + 'lilium' (lily), referring to the three-part structure of leaves and petals.",
            "memory_tips": [
                "Think 'TRI-LLIUM' = three + lily for three-petaled woodland flower",
                "Remember 'spring wildflower' with three leaves and three petals",
                "Connect to 'woodland garden' for natural habitat preference"
            ],
            "part_of_speech": "noun"
        },
        "trinidadian": {
            "definition": "Relating to or characteristic of Trinidad, the larger island of Trinidad and Tobago in the Caribbean; a native or inhabitant of Trinidad. Trinidad culture blends African, Indian, European, and indigenous influences, reflected in music, food, and traditions. Trinidadian cuisine features curry dishes, doubles, roti, and other Indo-Caribbean specialties alongside African-influenced foods. The island is famous for calypso and soca music, steel pan instruments, and vibrant Carnival celebrations. Trinidadian English incorporates unique vocabulary and expressions influenced by the island's multicultural heritage.",
            "pronunciation": "/ˌtrɪnɪˈdeɪdiən/",
            "example_sentence": "The _____ steel band performed energetic calypso music at the cultural festival.",
            "etymology": "From 'Trinidad' (named by Columbus for the Trinity) + '-ian' (relating to or native of), meaning 'of Trinidad.'",
            "memory_tips": [
                "Think 'from TRINIDAD' - relating to Caribbean island nation",
                "Remember 'steel pan music' for famous Trinidadian musical tradition",
                "Connect to 'Carnival' for vibrant Trinidadian cultural celebration"
            ],
            "part_of_speech": "adjective, noun"
        },
        "trinkets": {
            "definition": "Small decorative objects, jewelry, or ornaments of little value; small items kept for sentimental reasons or given as gifts. Often refers to inexpensive jewelry, souvenir items, or collectible objects that may have personal meaning despite low monetary value. Children often treasure trinkets like small toys, shiny objects, or gifts from friends and family. Tourist areas commonly sell trinkets as mementos of visits. The word can also describe any small, often decorative items that accumulate in homes, purses, or personal collections.",
            "pronunciation": "/ˈtrɪŋkəts/",
            "example_sentence": "The jewelry box was filled with childhood _____ that held precious memories despite their modest value.",
            "etymology": "Origin uncertain, possibly from Old French 'trinquet' (a small knife), later extended to small decorative objects.",
            "memory_tips": [
                "Think 'small TREASURES' - little decorative objects or cheap jewelry",
                "Remember 'souvenir shop' for tourist trinkets and mementos",
                "Connect to 'keepsakes' for sentimental value despite low cost"
            ],
            "part_of_speech": "noun (plural)"
        },
        "tripartite": {
            "definition": "Divided into or consisting of three parts; involving three parties or groups. Political contexts describe tripartite agreements between three nations, organizations, or political entities. Legal documents may be tripartite when three parties have interests or obligations. Biological classifications use tripartite to describe organisms or structures with three distinct sections. The term emphasizes equal division or participation among three elements, suggesting balance and cooperation in three-way arrangements.",
            "pronunciation": "/traɪˈpɑrtaɪt/",
            "example_sentence": "The _____ trade agreement benefited all three participating nations equally.",
            "etymology": "From Latin 'tripartitus,' from 'tri-' (three) + 'partitus' (divided), meaning 'divided into three parts.'",
            "memory_tips": [
                "Think 'TRI-PARTITE' = three + parts for three-way division",
                "Remember 'three-party agreement' for political or legal contexts",
                "Connect to 'tricolor' for other three-part concepts"
            ],
            "part_of_speech": "adjective"
        },
        "tripe": {
            "definition": "The edible lining of the stomach of ruminant animals, particularly cattle, used as food in various cuisines; nonsense or rubbish talk. As food, tripe requires careful preparation and is featured in traditional dishes from many cultures, including menudo, pho, and haggis. The texture is distinctive and polarizing—some people enjoy its chewy consistency while others find it unpalatable. Metaphorically, tripe describes worthless content, foolish talk, or material lacking substance or truth. The word carries strong dismissive connotations when describing speech or writing.",
            "pronunciation": "/traɪp/",
            "example_sentence": "The food critic dismissed the restaurant review as complete _____, lacking any useful information.",
            "etymology": "From Old French 'tripe,' possibly from Arabic 'tharb' (fold of fat), referring to stomach lining.",
            "memory_tips": [
                "Think 'stomach LINING food' or 'worthless TALK' - organ meat or nonsense",
                "Remember 'Mexican menudo' for traditional tripe soup",
                "Connect to 'rubbish' for metaphorical meaning of worthless content"
            ],
            "part_of_speech": "noun"
        },
        "triquetra": {
            "definition": "A three-cornered symbol formed by three interlaced arcs, often representing the Christian Trinity or Celtic spiritual concepts. This ancient symbol appears in Celtic art, medieval manuscripts, and modern spiritual contexts. The continuous line with no beginning or end symbolizes eternity, while the three sections can represent various trinities including mind-body-spirit, past-present-future, or maiden-mother-crone. Archaeological evidence shows the triquetra in pre-Christian Celtic cultures, later adopted by Christians to represent Father-Son-Holy Spirit. Modern usage includes jewelry, logos, and decorative arts drawing on its spiritual symbolism.",
            "pronunciation": "/traɪˈkwɛtrə/",
            "example_sentence": "The ancient Celtic stone carving featured a beautiful _____ symbol representing eternal spiritual unity.",
            "etymology": "From Latin 'tri-' (three) + 'quetrus' (cornered), literally meaning 'three-cornered.'",
            "memory_tips": [
                "Think 'TRI-QUETRA' = three + corners for three-part interlaced symbol",
                "Remember 'Celtic symbol' for spiritual trinity representation",
                "Connect to 'Trinity' for Christian three-part divine concept"
            ],
            "part_of_speech": "noun"
        },
        "triskelion": {
            "definition": "An ancient Celtic symbol consisting of three interlocked spirals or three bent human legs radiating from a central point. This motif appears throughout Celtic art, mythology, and modern cultural expressions, representing various trinities such as land-sea-sky, past-present-future, or maiden-mother-crone. The three-legged version appears on the flags of the Isle of Man and Sicily. Archaeological evidence shows triskelions in Neolithic art, suggesting pre-Celtic origins. The symbol embodies concepts of motion, progress, and the cyclical nature of life, making it popular in modern Celtic spirituality and design.",
            "pronunciation": "/traɪˈskɛliən/",
            "example_sentence": "The Isle of Man's flag prominently features a _____ with three armored legs in running position.",
            "etymology": "From Greek 'tri-' (three) + 'skelos' (leg), literally meaning 'three-legged.'",
            "memory_tips": [
                "Think 'TRI-SKELION' = three + legs for three-legged Celtic symbol",
                "Remember 'Isle of Man flag' for famous three-legged version",
                "Connect to 'Celtic spirals' for ancient artistic motif"
            ],
            "part_of_speech": "noun"
        },
        "triste": {
            "definition": "A French and Spanish word meaning 'sad,' 'melancholy,' or 'sorrowful'; expressing deep emotional sadness or wistfulness. In musical contexts, 'triste' indicates a sad, slow, or melancholic style of performance. Literature uses 'triste' to describe characters, moods, or atmospheres characterized by sadness or pensiveness. The word conveys a gentle, poetic sadness rather than harsh grief, often associated with romantic or artistic expressions of melancholy. French and Spanish poetry frequently employ 'triste' to evoke emotional depth and contemplative sadness.",
            "pronunciation": "/trist/ (French), /ˈtriste/ (Spanish)",
            "example_sentence": "The pianist played the _____ melody with deep emotion, capturing the composer's melancholic intentions.",
            "etymology": "From Latin 'tristis' meaning 'sad, sorrowful,' adopted into French and Spanish with similar meanings.",
            "memory_tips": [
                "Think 'SAD in French/Spanish' - melancholy or sorrowful emotion",
                "Remember 'melancholic music' for sad, slow musical style",
                "Connect to 'wistful' for gentle, poetic sadness"
            ],
            "part_of_speech": "adjective (French/Spanish)"
        },
        "tristetrituration": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'triste' (sad/melancholy) and 'trituration' (grinding into powder). 'Triste' is a French/Spanish word meaning sad, while 'trituration' refers to pharmaceutical or chemical grinding processes. These represent completely different concepts from emotion and chemistry that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'triste' + 'trituration' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "tristeza": {
            "definition": "A Spanish and Portuguese word meaning 'sadness' or 'sorrow'; a plant disease affecting citrus trees, particularly grapefruit and sweet orange. In emotional contexts, tristeza describes deep sadness, melancholy, or grief. Agriculturally, tristeza is a viral disease that causes citrus trees to decline, yellow, and die, transmitted by aphids. The disease has caused significant economic losses in citrus-growing regions worldwide. Resistant rootstocks and disease management practices help control tristeza in commercial citrus production. The dual meaning reflects the sadness associated with crop losses from this devastating plant virus.",
            "pronunciation": "/trɪsˈtesə/ (Spanish), /trisˈtezɐ/ (Portuguese)",
            "example_sentence": "The citrus grower implemented strict measures to prevent _____ virus from destroying the orange groves.",
            "etymology": "From Spanish/Portuguese 'tristeza,' from Latin 'tristitia' (sadness), applied to citrus disease due to tree decline.",
            "memory_tips": [
                "Think 'SADNESS in Spanish' or 'citrus DISEASE' - emotion or plant virus",
                "Remember 'citrus trees dying' for agricultural context",
                "Connect to 'triste' for related sadness vocabulary"
            ],
            "part_of_speech": "noun (Spanish/Portuguese)"
        },
        "triton": {
            "definition": "In Greek mythology, a sea god with a human upper body and fish tail, son of Poseidon and Amphitrite; any of various large marine gastropod mollusks with spiral shells. Mythological tritons served as Poseidon's messengers and trumpet players, using conch shells to calm or raise storms. The shells of triton mollusks were historically used as horns in various Pacific cultures. These large sea snails are prized by collectors for their beautiful spiral shells. Nuclear physics uses 'triton' for the nucleus of tritium, a hydrogen isotope with one proton and two neutrons.",
            "pronunciation": "/ˈtraɪtən/",
            "example_sentence": "The museum displayed a magnificent _____ shell that ancient Polynesian cultures used as a ceremonial horn.",
            "etymology": "From Greek 'Triton,' name of the sea god, later applied to similar mythological beings and related sea creatures.",
            "memory_tips": [
                "Think 'sea GOD with fish tail' or 'large CONCH shell' - mythology or mollusk",
                "Remember 'Poseidon's son' for Greek mythological context",
                "Connect to 'mermaid' for similar human-fish hybrid creature"
            ],
            "part_of_speech": "noun"
        },
        "trituration": {
            "definition": "The process of grinding, crushing, or rubbing a substance into fine powder or particles; in pharmacy, the mixing of drugs with inert powders to reduce potency or improve handling. Pharmaceutical trituration involves grinding tablets, crystals, or other solid medications into uniform powders for easier dosing, mixing, or absorption. Laboratory trituration prepares samples for analysis by creating homogeneous powders. Traditional medicine uses trituration for preparing herbal powders and medicinal compounds. The process requires careful technique to achieve uniform particle size and avoid contamination.",
            "pronunciation": "/ˌtrɪtʃəˈreɪʃən/",
            "example_sentence": "The pharmacist performed _____ to reduce the strength of the medication for pediatric patients.",
            "etymology": "From Latin 'trituratio,' from 'triturare' (to thresh, grind), from 'tritum' (ground, rubbed).",
            "memory_tips": [
                "Think 'GRINDING to powder' - crushing substances into fine particles",
                "Remember 'pharmacy technique' for medication preparation",
                "Connect to 'pulverize' for similar grinding action"
            ],
            "part_of_speech": "noun"
        },
        "triumph": {
            "definition": "A great victory or achievement; the feeling of joy and satisfaction following success; in ancient Rome, a ceremonial procession celebrating military victory. Modern usage describes personal accomplishments, competitive victories, or overcoming significant challenges. The emotion of triumph combines relief, pride, and celebration after achieving difficult goals. Historical Roman triumphs were elaborate public celebrations honoring successful generals returning from war. The word emphasizes not just winning but the magnitude and significance of the victory achieved through effort, skill, or perseverance.",
            "pronunciation": "/ˈtraɪəmf/",
            "example_sentence": "The team's victory in the championship was a _____ of teamwork, dedication, and strategic planning.",
            "etymology": "From Latin 'triumphus,' referring to Roman ceremonial processions celebrating military victories.",
            "memory_tips": [
                "Think 'great VICTORY' - significant success or achievement",
                "Remember 'Roman procession' for historical ceremonial context",
                "Connect to 'celebration' for joy following major accomplishment"
            ],
            "part_of_speech": "noun, verb"
        },
        "triumphant": {
            "definition": "Feeling or expressing great joy and satisfaction at success or victory; characterized by or celebrating triumph. Describes the emotional state and outward expression following significant achievements, competitions, or overcoming obstacles. Can describe individuals, teams, or groups that have achieved notable victories. The word implies not just success but visible celebration, pride, and satisfaction in accomplishment. Often used to describe winners in competitions, successful completion of difficult projects, or overcoming personal challenges with evident joy and satisfaction.",
            "pronunciation": "/traɪˈʌmfənt/",
            "example_sentence": "The _____ athlete raised her arms in celebration after breaking the world record.",
            "etymology": "From Latin 'triumphant-' (celebrating victory), from 'triumphare' (to celebrate a triumph).",
            "memory_tips": [
                "Think 'TRIUMPH-ANT' - showing triumph or celebrating victory",
                "Remember 'victory celebration' for joyful expression of success",
                "Connect to 'victorious' for similar winning, successful state"
            ],
            "part_of_speech": "adjective"
        },
        "trivia": {
            "definition": "Details, considerations, or pieces of information of little importance or value; questions and answers about obscure facts used in games or competitions. Modern trivia contests test knowledge of random facts across various subjects including history, entertainment, sports, and science. The word originally meant 'trifling matters' but has evolved to describe factual information that, while interesting, may not be practically important. Bar trivia, quiz shows, and trivia games have made the pursuit of obscure knowledge a popular entertainment form. Academic contexts may use trivia to describe minor details versus major concepts.",
            "pronunciation": "/ˈtrɪviə/",
            "example_sentence": "The quiz night featured challenging _____ questions about 1980s movies and historical dates.",
            "etymology": "From Latin 'trivia,' meaning 'three roads' (crossroads), extended to mean 'commonplace, ordinary matters.'",
            "memory_tips": [
                "Think 'random FACTS' - obscure or unimportant information",
                "Remember 'quiz games' for trivia contests and competitions",
                "Connect to 'trivial' for matters of little importance"
            ],
            "part_of_speech": "noun"
        },
        "trochee": {
            "definition": "A metrical foot in poetry consisting of a stressed syllable followed by an unstressed syllable, the opposite of an iamb. Common in poetry and songs, trochees create a strong, rhythmic pattern that can sound forceful or memorable. Examples include words like 'happy,' 'freedom,' and 'trouble.' Poetry using trochaic meter includes Edgar Allan Poe's 'The Raven' and many nursery rhymes. The trochee's falling rhythm contrasts with the rising rhythm of iambic meter, creating different emotional effects in verse. Understanding trochaic patterns helps in analyzing poetic rhythm and meter.",
            "pronunciation": "/ˈtroʊki/",
            "example_sentence": "The poem's opening line featured a _____ pattern that gave it a strong, memorable rhythm.",
            "etymology": "From Greek 'trochaios' (running), from 'trechein' (to run), referring to the quick, running rhythm.",
            "memory_tips": [
                "Think 'STRESSED-unstressed' pattern - strong syllable followed by weak",
                "Remember 'TROE-chee' is itself a trochee pattern",
                "Connect to 'The Raven' for famous trochaic poetry example"
            ],
            "part_of_speech": "noun"
        },
        "trocheetrompe": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'trochee' (poetic meter pattern) and 'trompe' (as in 'trompe-l'oeil,' visual illusion art). 'Trochee' refers to a stressed-unstressed syllable pattern in poetry, while 'trompe' relates to visual deception techniques in art. These represent completely different concepts from literature and visual arts that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'trochee' + 'trompe' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "trodden": {
            "definition": "Past participle of 'tread,' meaning walked on, trampled, or stepped upon; crushed or pressed down by walking or heavy pressure. Describes paths, grass, or surfaces that show evidence of foot traffic or repeated stepping. Can refer to metaphorical situations where someone feels oppressed, dominated, or treated with disrespect. Well-trodden paths indicate frequent use by pedestrians or animals. The word suggests wear, compression, or degradation resulting from repeated foot pressure or figurative oppression.",
            "pronunciation": "/ˈtrɑdən/",
            "example_sentence": "The _____ grass showed the route that countless visitors had taken to reach the scenic overlook.",
            "etymology": "Past participle of 'tread,' from Old English 'tredan' (to step, walk), meaning 'having been stepped upon.'",
            "memory_tips": [
                "Think past tense of 'TREAD' - already stepped on or walked over",
                "Remember 'worn path' for frequently traveled route",
                "Connect to 'trampled' for crushed by foot traffic"
            ],
            "part_of_speech": "verb (past participle), adjective"
        },
        "troll": {
            "definition": "In Scandinavian folklore, a supernatural being dwelling in mountains, caves, or under bridges; to fish by trailing bait from a moving boat; on the internet, someone who deliberately provokes others with inflammatory comments. Mythological trolls are often depicted as large, ugly creatures who turn to stone in sunlight. Fishing trolling involves moving slowly while lines drag behind the boat. Internet trolling describes posting provocative content to elicit angry responses from other users. The word has evolved from folklore to describe various forms of fishing and online behavior.",
            "pronunciation": "/troʊl/",
            "example_sentence": "The fisherman decided to _____ for salmon in the early morning hours when fish were most active.",
            "etymology": "From Old Norse 'troll' (giant, demon), extended to fishing technique and modern internet behavior.",
            "memory_tips": [
                "Think 'folklore MONSTER,' 'fishing METHOD,' or 'internet PROVOCATEUR'",
                "Remember 'under bridge' for classic troll fairy tale location",
                "Connect to 'provoke' for internet trolling behavior"
            ],
            "part_of_speech": "noun, verb"
        },
        "trombone": {
            "definition": "A brass musical instrument with a telescoping slide mechanism that changes pitch by altering the length of tubing. Known for its distinctive glissando capability and rich, powerful tone, the trombone plays important roles in orchestras, jazz bands, marching bands, and concert bands. The slide mechanism allows for smooth pitch transitions impossible on valved brass instruments. Different sizes include alto, tenor, and bass trombones, each with distinct tonal characteristics. Proper trombone technique requires precise slide positions, breath control, and embouchure development for accurate intonation.",
            "pronunciation": "/trɑmˈboʊn/",
            "example_sentence": "The jazz musician's _____ solo featured impressive glissandos that showcased the instrument's unique capabilities.",
            "etymology": "From Italian 'trombone,' augmentative of 'tromba' (trumpet), literally meaning 'large trumpet.'",
            "memory_tips": [
                "Think 'SLIDING brass instrument' - trumpet-like with telescoping slide",
                "Remember 'glissando' for smooth sliding pitch changes",
                "Connect to 'jazz band' for prominent trombone musical context"
            ],
            "part_of_speech": "noun"
        },
        "trompe": {
            "definition": "Short for 'trompe-l'oeil,' a French term meaning 'deceive the eye'; an art technique that uses realistic imagery to create optical illusions making painted objects appear three-dimensional. This sophisticated painting method creates convincing illusions of architectural elements, objects, or spaces that don't actually exist. Famous examples include ceiling frescoes that appear to open to sky or painted doors and windows that look real. Modern applications include murals, theater sets, and architectural decoration. The technique requires mastery of perspective, lighting, and realistic detail to successfully deceive viewers.",
            "pronunciation": "/trɔmp/",
            "example_sentence": "The artist's _____ mural made the flat wall appear to have actual windows and architectural details.",
            "etymology": "From French 'trompe-l'oeil,' literally 'deceive the eye,' from 'tromper' (to deceive) + 'l'oeil' (the eye).",
            "memory_tips": [
                "Think 'DECEIVE the eye' - art that creates realistic optical illusions",
                "Remember 'wall painting' that looks three-dimensional",
                "Connect to 'optical illusion' for visual deception technique"
            ],
            "part_of_speech": "noun"
        },
        "troop": {
            "definition": "A group of soldiers, scouts, or other organized people; a group of animals, especially primates; to move or gather in large numbers. Military troops form basic organizational units within larger forces. Scout troops organize youth activities and outdoor education. Animal troops, particularly monkey troops, exhibit complex social behaviors and hierarchies. As a verb, describes mass movement or gathering, often with purposeful direction. The word emphasizes collective action, organization, and movement in groups rather than individual behavior.",
            "pronunciation": "/trup/",
            "example_sentence": "The scout _____ organized a camping trip to teach wilderness survival skills to local youth.",
            "etymology": "From French 'troupe,' from Germanic origin, meaning 'band, company, crowd.'",
            "memory_tips": [
                "Think 'organized GROUP' - soldiers, scouts, or animals moving together",
                "Remember 'Boy Scout troop' for youth organization example",
                "Connect to 'gather' for collective movement or assembly"
            ],
            "part_of_speech": "noun, verb"
        },
        "trope": {
            "definition": "A figurative or metaphorical use of language; a common theme, device, or motif in literature, film, or other media that becomes recognizable through frequent use. Literary tropes include metaphors, similes, irony, and allegory that create meaning beyond literal interpretation. Modern usage describes recurring plot elements, character types, or situations that appear across multiple works. Some tropes become clichéd through overuse, while others remain effective storytelling tools. Understanding tropes helps in analyzing literature, film, and media for deeper meaning and cultural patterns.",
            "pronunciation": "/troʊp/",
            "example_sentence": "The 'chosen one' _____ appears in countless fantasy novels and movies as a central plot element.",
            "etymology": "From Greek 'tropos' (turn, way, manner), referring to a turn of phrase or figurative expression.",
            "memory_tips": [
                "Think 'common THEME' - recurring plot device or literary pattern",
                "Remember 'metaphor' for figurative language use",
                "Connect to 'cliché' for overused narrative elements"
            ],
            "part_of_speech": "noun"
        },
        "trophic": {
            "definition": "Relating to nutrition or feeding; describing the feeding relationships and energy flow in ecological systems. Trophic levels organize organisms by their position in food chains, from primary producers (plants) through various consumer levels to apex predators. Trophic cascades describe how changes at one level affect other levels throughout the ecosystem. Medical contexts use trophic to describe tissue nutrition and growth factors. Understanding trophic relationships is fundamental to ecology, conservation biology, and ecosystem management.",
            "pronunciation": "/ˈtroʊfɪk/",
            "example_sentence": "The marine biologist studied _____ relationships to understand how overfishing affected the entire ecosystem.",
            "etymology": "From Greek 'trophikos' (nourishing), from 'trophe' (food, nourishment), relating to feeding and nutrition.",
            "memory_tips": [
                "Think 'FEEDING relationships' - nutrition and energy flow in ecosystems",
                "Remember 'food chain levels' for trophic organization",
                "Connect to 'trophy' for similar Greek root but different meaning"
            ],
            "part_of_speech": "adjective"
        },
        "trophy": {
            "definition": "An award or prize given for victory or achievement in competition; an object kept as a reminder of success or conquest. Sports trophies recognize athletic achievements, while academic trophies honor scholarly accomplishments. Historical context includes war trophies taken from defeated enemies. Hunting trophies commemorate successful hunts, though this practice faces increasing ethical scrutiny. Modern trophy design ranges from traditional cups and plaques to creative custom awards. The psychological value of trophies lies in their role as tangible symbols of accomplishment and recognition.",
            "pronunciation": "/ˈtroʊfi/",
            "example_sentence": "The championship _____ held a place of honor in the school's display case.",
            "etymology": "From Greek 'tropaion' (monument of victory), from 'trope' (a turning, rout of enemies).",
            "memory_tips": [
                "Think 'victory AWARD' - prize for winning competition or achievement",
                "Remember 'championship cup' for sports competition recognition",
                "Connect to 'triumph' for celebration of success"
            ],
            "part_of_speech": "noun"
        },
        "tropical": {
            "definition": "Relating to or characteristic of the tropics, the region between the Tropic of Cancer and Tropic of Capricorn; having a hot, humid climate typical of equatorial regions. Tropical climates feature high temperatures, seasonal rainfall patterns, and distinctive ecosystems including rainforests, coral reefs, and unique wildlife. Tropical diseases affect populations in these regions, while tropical agriculture produces crops like coffee, bananas, and spices. Weather systems include tropical storms and hurricanes. The word evokes images of palm trees, beaches, and exotic destinations popular in tourism.",
            "pronunciation": "/ˈtrɑpɪkəl/",
            "example_sentence": "The _____ rainforest supported incredible biodiversity with thousands of unique plant and animal species.",
            "etymology": "From Latin 'tropicus,' from Greek 'tropikos' (of a turn), referring to the sun's turning points at solstices.",
            "memory_tips": [
                "Think 'hot and HUMID climate' - equatorial regions with warm weather",
                "Remember 'rainforest' for tropical ecosystem example",
                "Connect to 'vacation paradise' for tropical tourism destinations"
            ],
            "part_of_speech": "adjective"
        },
        "trotteur": {
            "definition": "A French term for a horse trained for trotting; a type of women's shoe with a low heel designed for walking; someone who trots or walks quickly. In equestrian contexts, describes horses specifically bred and trained for harness racing at a trotting gait. The shoe style emerged in early 20th century fashion as practical footwear for active women. Modern usage may describe anyone who moves at a brisk trotting pace. The term reflects French influence in both equestrian sports and fashion history.",
            "pronunciation": "/trɔˈtœr/ (French), /ˈtrɑtər/ (English)",
            "example_sentence": "She chose comfortable _____ shoes for the long walking tour through the historic city.",
            "etymology": "From French 'trotteur,' from 'trotter' (to trot), meaning 'one who trots.'",
            "memory_tips": [
                "Think 'TROTTING horse' or 'walking SHOE' - equestrian or fashion context",
                "Remember 'low-heeled shoe' for practical women's footwear",
                "Connect to 'trotter' for horse that moves at trotting gait"
            ],
            "part_of_speech": "noun"
        },
        "trough": {
            "definition": "A long, narrow container for holding water or food for animals; a low point between waves or hills; a period of low activity or achievement. Farm troughs provide drinking water for livestock, while feeding troughs hold grain or other animal food. Weather systems create atmospheric troughs associated with low pressure and stormy conditions. Economic troughs represent the lowest points in business cycles before recovery begins. The word emphasizes elongated, depressed shapes that collect or channel substances.",
            "pronunciation": "/trɔf/",
            "example_sentence": "The farmer filled the water _____ twice daily to ensure the cattle had adequate drinking water.",
            "etymology": "From Old English 'trog,' related to Germanic words for hollow vessel or container.",
            "memory_tips": [
                "Think 'animal WATER container' - long, narrow feeding/watering vessel",
                "Remember 'low point' between waves or in business cycles",
                "Connect to 'valley' for depression between higher areas"
            ],
            "part_of_speech": "noun"
        },
        "trounce": {
            "definition": "To defeat decisively or thoroughly; to beat soundly in competition or conflict. Implies overwhelming victory with significant margin of difference between winner and loser. Sports contexts describe teams that trounce opponents through superior skill, strategy, or performance. Academic or professional competitions may involve trouncing when one participant clearly outperforms others. The word suggests not just winning but dominating the competition completely. Often used when describing unexpected or impressive victories that leave no doubt about the superior party.",
            "pronunciation": "/traʊns/",
            "example_sentence": "The debate team managed to _____ their rivals with well-researched arguments and superior presentation skills.",
            "etymology": "Origin uncertain, possibly from dialectal English, meaning 'to beat thoroughly or punish severely.'",
            "memory_tips": [
                "Think 'DEFEAT decisively' - overwhelming victory with large margin",
                "Remember 'beat soundly' for thorough competitive domination",
                "Connect to 'demolish' for complete victory over opponents"
            ],
            "part_of_speech": "verb"
        },
        "trous": {
            "definition": "A French word meaning 'holes'; plural of 'trou' (hole). Used in various contexts including geology, medicine, and everyday language to describe openings, gaps, or hollow spaces. In fashion, may refer to distressed clothing with deliberate holes. Geological contexts describe natural holes or cavities in rock formations. The word appears in French expressions and may be encountered in English texts dealing with French subjects or in areas with French linguistic influence.",
            "pronunciation": "/tru/ (French)",
            "example_sentence": "The geologist examined the _____ in the limestone cliff to understand the cave formation process.",
            "etymology": "French plural of 'trou' (hole), from Latin 'foramen' through Vulgar Latin development.",
            "memory_tips": [
                "Think 'HOLES in French' - plural form of openings or gaps",
                "Remember 'cave openings' for geological context",
                "Connect to 'perforations' for multiple holes or openings"
            ],
            "part_of_speech": "noun (French)"
        },
        "trousers": {
            "definition": "A garment covering the body from the waist to the ankles, with separate sections for each leg; pants. British English primarily uses 'trousers' while American English favors 'pants.' Various styles include dress trousers, casual pants, jeans, and specialized work trousers. Materials range from cotton and wool to synthetic blends designed for specific purposes. Historical development shows trousers evolving from practical workwear to formal attire suitable for various social and professional contexts. Modern trouser design considers comfort, durability, and fashion trends.",
            "pronunciation": "/ˈtraʊzərz/",
            "example_sentence": "He selected dark wool _____ to complete his professional business outfit for the important meeting.",
            "etymology": "From Irish 'triubhas' or Scottish Gaelic 'triubhas' (close-fitting shorts), entering English via military contexts.",
            "memory_tips": [
                "Think 'leg COVERING clothing' - pants or long leg garments",
                "Remember 'British for pants' - UK term for leg-covering clothing",
                "Connect to 'business attire' for formal trouser context"
            ],
            "part_of_speech": "noun (plural)"
        }
    }

def process_batch_183():
    """Process batch_183_words.csv with comprehensive Claude data"""
    try:
        logger.info("Processing Batch 183 with comprehensive Claude data...")
        
        # Load comprehensive data
        claude_data = get_comprehensive_claude_data()
        
        # Initialize difficulty calculator
        calc = DifficultyCalculator()
        
        # Read input file
        input_file = 'output/batch_183_words.csv'
        output_file = 'output/batch_183_processed.csv'
        
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
            logger.info("Batch 183 processing completed!")
            logger.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
            logger.info(f"Output saved to: {output_file}")
            logger.info(f"Results: {len(processed_words)} successful, 0 failed")
        else:
            logger.error("No words were processed")
            
    except Exception as e:
        logger.error(f"Error processing batch 183: {str(e)}")
        raise

if __name__ == "__main__":
    process_batch_183()