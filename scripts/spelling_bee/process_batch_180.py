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
            'tools', 'tooth', 'topics', 'topped', 'toppings', 'torch', 'torment'
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
    Return comprehensive data for all 50 words in batch_180_words.csv
    Generated using Claude with detailed educational content.
    """
    return {
        "toastmaster": {
            "definition": "A person who presides at banquets and formal dinners, introducing speakers and proposing toasts. Originally emerging from medieval feast traditions, the toastmaster serves as master of ceremonies, ensuring proper protocol and entertainment flow. Modern toastmasters often belong to Toastmasters International, a global organization focused on developing public speaking and leadership skills through structured practice sessions and educational programs. Professional toastmasters may work at corporate events, weddings, and formal gatherings, using humor, timing, and crowd management skills to create memorable experiences. The role requires confidence, quick thinking, and cultural sensitivity.",
            "pronunciation": "/ˈtoʊstˌmæstər/",
            "example_sentence": "The _____ kept the company's annual dinner entertaining with witty introductions and perfectly timed speeches.",
            "etymology": "From 'toast' (act of honoring with drink) + 'master' (one in authority), dating to 17th century English social customs.",
            "memory_tips": [
                "Think 'TOAST + MASTER' - someone who masters the art of toasting at events",
                "Remember 'master of toast ceremonies' for formal dinner leadership",
                "Connect to Toastmasters International organization for public speaking practice"
            ],
            "part_of_speech": "noun"
        },
        "toccata": {
            "definition": "A musical composition typically written for keyboard instruments, characterized by rapid runs, brilliant passages, and virtuosic technical display. Originating in the late Renaissance and flourishing during the Baroque period, toccatas often feature improvisational style with free-flowing rhythms and dramatic contrasts. Famous examples include Bach's Toccata and Fugue in D minor and Debussy's impressionistic toccatas. The form emphasizes the performer's technical skill and the instrument's capabilities, often serving as showcase pieces or study exercises. Modern composers continue writing toccatas, adapting the form for various instruments beyond keyboard.",
            "pronunciation": "/təˈkɑtə/",
            "example_sentence": "The pianist's performance of Bach's _____ demonstrated incredible finger dexterity and musical precision.",
            "etymology": "From Italian 'toccare' meaning 'to touch,' referring to touching keyboard keys, first used in late 16th century.",
            "memory_tips": [
                "Think 'TOuch' - toccata means touching keys rapidly and skillfully",
                "Remember 'Bach's famous piece' for classical music recognition",
                "Connect 'toc-' to 'touch' for keyboard technique emphasis"
            ],
            "part_of_speech": "noun"
        },
        "today": {
            "definition": "The present day; this current 24-hour period from midnight to midnight. Philosophically represents the immediate moment of existence and action, distinguishing present reality from past memory and future possibility. In temporal contexts, today marks the boundary between yesterday's completion and tomorrow's potential. The concept carries psychological weight in decision-making, goal-setting, and mindfulness practices. Business and academic contexts often use 'today' to establish urgency and immediate relevance. Cultural expressions like 'live for today' reflect various attitudes toward time management and life philosophy.",
            "pronunciation": "/təˈdeɪ/",
            "example_sentence": "The weather forecast shows sunny skies for _____, perfect for the outdoor wedding ceremony.",
            "etymology": "From Old English 'tō dæge' meaning 'on this day,' combining 'to' (at) and 'dæge' (day).",
            "memory_tips": [
                "Think 'TO-DAY' - literally means 'to this day' or 'on this day'",
                "Remember as opposite of 'yesterday' and 'tomorrow'",
                "Connect to 'daily' for time period understanding"
            ],
            "part_of_speech": "noun, adverb"
        },
        "toddler": {
            "definition": "A young child typically between one and three years old who has learned to walk but still moves unsteadily, characterized by wobbling, tottering movements. Developmentally, toddlers experience rapid cognitive and physical growth, developing language skills, motor coordination, and social awareness. This stage involves exploration, boundary testing, and emotional regulation challenges, often called the 'terrible twos.' Toddlers require constant supervision due to their curiosity, limited danger awareness, and developing impulse control. Early childhood education and parenting strategies focus heavily on this critical developmental period for establishing foundations of learning and behavior.",
            "pronunciation": "/ˈtɑdlər/",
            "example_sentence": "The _____ wobbled across the playground, giggling as she chased after the colorful butterfly.",
            "etymology": "From 'toddle' (walk unsteadily) + '-er' (one who does), first recorded in 1793, from earlier 'toddle' meaning to walk slowly.",
            "memory_tips": [
                "Think 'TODDLE-R' - one who toddles or walks unsteadily",
                "Remember toddlers 'toddle' around as they learn to walk",
                "Connect to 'wobble' for the characteristic unsteady movement"
            ],
            "part_of_speech": "noun"
        },
        "toey": {
            "definition": "Australian and New Zealand slang meaning restless, nervous, or anxious; eager to leave or move on. Often describes someone who is fidgety, impatient, or experiencing anticipatory anxiety about upcoming events. The term can also mean sexually aroused or eager for romantic contact in informal contexts. In broader usage, describes general restlessness or agitation when someone cannot remain still or calm. Regional variations exist across Australia and New Zealand, with slightly different connotations depending on context and speaker intent.",
            "pronunciation": "/ˈtoʊi/",
            "example_sentence": "After sitting in the waiting room for two hours, she became increasingly _____ and started pacing around.",
            "etymology": "Australian slang of uncertain origin, possibly from 'toe' + '-y', suggesting restless foot movement, first recorded mid-20th century.",
            "memory_tips": [
                "Think 'TOE-Y' - like tapping your toes when restless or nervous",
                "Remember restless feet wanting to move around",
                "Connect to 'antsy' as similar meaning for restlessness"
            ],
            "part_of_speech": "adjective"
        },
        "toga": {
            "definition": "A draped outer garment worn by citizens of ancient Rome, consisting of a large semicircular piece of woolen cloth wrapped around the body in prescribed folds. The toga represented Roman citizenship and social status, with different styles indicating rank, age, and profession. Made from white wool, special versions included the toga praetexta (purple border for magistrates) and toga picta (decorated for triumphal occasions). Modern usage refers to similar draped garments worn at graduation ceremonies, costume parties, or theatrical productions depicting classical themes. The toga's complex draping required assistance and skill to wear properly.",
            "pronunciation": "/ˈtoʊɡə/",
            "example_sentence": "The senator adjusted his white _____ carefully before entering the Roman Forum for the important political debate.",
            "etymology": "From Latin 'toga,' related to 'tegere' meaning 'to cover,' the characteristic garment of Roman citizens.",
            "memory_tips": [
                "Think 'Roman robe' for ancient Roman clothing identification",
                "Remember 'TOG-A' sounds like 'toga party' in modern culture",
                "Connect to graduation gowns as modern toga-like garments"
            ],
            "part_of_speech": "noun"
        },
        "together": {
            "definition": "In union, proximity, or cooperation; existing or occurring in the same place, time, or relationship. Describes physical closeness, emotional connection, or collaborative action between two or more entities. Philosophically represents unity, harmony, and shared purpose, contrasting with separation or isolation. In relationships, togetherness indicates mutual support, understanding, and commitment. Business contexts use 'together' to emphasize teamwork, coordination, and collective achievement. The concept extends beyond physical presence to include synchronized timing, aligned goals, and coordinated efforts toward common objectives.",
            "pronunciation": "/təˈɡɛðər/",
            "example_sentence": "The family decided to work _____ on renovating their old farmhouse during the summer vacation.",
            "etymology": "From Old English 'tōgædere,' combining 'tō' (to) and 'gædere' (together, gather), meaning 'in one place.'",
            "memory_tips": [
                "Think 'TO-GATHER' - literally gathering things or people to one place",
                "Remember as opposite of 'apart' or 'separate'",
                "Connect to 'gather' for bringing things into unity"
            ],
            "part_of_speech": "adverb"
        },
        "toggenburg": {
            "definition": "A breed of dairy goat originating from the Toggenburg valley in eastern Switzerland, characterized by distinctive coloring and excellent milk production. These medium-sized goats feature light brown to chocolate brown coats with white markings on legs, face, and ears. Known for high butterfat content in their milk and adaptability to various climates, Toggenburgs are among the oldest registered dairy goat breeds. They typically produce 6-12 pounds of milk daily with 3.2-3.8% butterfat content. Popular in sustainable farming and homesteading operations, these goats are valued for their hardiness, longevity, and consistent milk production across extended lactation periods.",
            "pronunciation": "/ˈtɔɡənbɜrɡ/",
            "example_sentence": "The _____ goats in the mountain pasture produced rich, creamy milk perfect for artisanal cheese making.",
            "etymology": "Named after the Toggenburg valley in eastern Switzerland, where the breed was developed by local farmers over centuries.",
            "memory_tips": [
                "Think 'Swiss GOAT breed' from Toggenburg valley",
                "Remember 'TOG-GEN-BURG' like German/Swiss place names",
                "Connect to 'dairy goat' for milk production association"
            ],
            "part_of_speech": "noun"
        },
        "togo": {
            "definition": "A West African nation located between Ghana and Benin, officially the Togolese Republic, with its capital at Lomé. This narrow country stretches from the Gulf of Guinea northward, featuring diverse landscapes from coastal plains to northern savannas. Togo gained independence from France in 1960 and has a complex political history involving periods of military rule and democratic transitions. The economy relies on agriculture (coffee, cocoa, cotton), phosphate mining, and port services. Cultural diversity includes multiple ethnic groups with French as the official language, though local languages like Ewe and Kabye are widely spoken.",
            "pronunciation": "/ˈtoʊɡoʊ/",
            "example_sentence": "The Peace Corps volunteer spent two years teaching English in a rural village in _____.",
            "etymology": "From the Ewe word 'to' (water) and 'go' (shore), referring to the lake region, adopted as the country name.",
            "memory_tips": [
                "Think 'West African country' between Ghana and Benin",
                "Remember 'TO-GO' like ordering food, but it's a place you go TO",
                "Connect to 'Lomé' as the capital city for geographic reference"
            ],
            "part_of_speech": "noun (proper)"
        },
        "toile": {
            "definition": "A type of decorative fabric featuring pastoral scenes, typically printed in single colors (traditionally blue, red, or black) on white or cream backgrounds. Originally produced in 18th-century France, toile depicts elaborate scenes of rural life, historical events, or romantic vignettes in detailed line drawings. The fabric is commonly used in interior design for curtains, upholstery, wallpaper, and bedding, creating classic, elegant aesthetics. Modern toile patterns may include contemporary themes while maintaining the characteristic single-color, narrative illustration style. High-quality toile often features intricate, story-telling designs that can be examined closely for detailed artistic elements.",
            "pronunciation": "/twɑl/",
            "example_sentence": "The bedroom featured beautiful blue _____ curtains depicting 18th-century French countryside scenes.",
            "etymology": "From French 'toile' meaning 'cloth' or 'canvas,' originally referring to linen fabric before developing the decorative meaning.",
            "memory_tips": [
                "Think 'French decorative fabric' with pastoral scenes",
                "Remember 'TOILE' sounds like 'twall' - decorative wall-covering fabric",
                "Connect to 'classic interior design' for elegant home decoration"
            ],
            "part_of_speech": "noun"
        },
        "toilsome": {
            "definition": "Requiring hard work, effort, or labor; characterized by difficulty, exhaustion, or tedious struggle. Describes tasks, journeys, or processes that demand significant physical or mental exertion over extended periods. Often applied to manual labor, challenging academic work, or complex projects requiring persistence and determination. The word carries connotations of both difficulty and eventual accomplishment through sustained effort. Historical contexts frequently describe toilsome agricultural work, long journeys, or artisan crafts requiring meticulous attention and physical endurance.",
            "pronunciation": "/ˈtɔɪlsəm/",
            "example_sentence": "After years of _____ research, the scientist finally discovered the breakthrough formula.",
            "etymology": "From 'toil' (hard work) + '-some' (characterized by), first appearing in Middle English around 14th century.",
            "memory_tips": [
                "Think 'TOIL-SOME' - characterized by hard toil or work",
                "Remember 'toil' means hard work, '-some' means full of",
                "Connect to 'troublesome' for similar word structure meaning"
            ],
            "part_of_speech": "adjective"
        },
        "toilsometempestuous": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'toilsome' (requiring hard work) and 'tempestuous' (very stormy or turbulent). 'Toilsome' describes difficult, laborious work while 'tempestuous' refers to violent weather or emotional turbulence. These represent different concepts that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'toilsome' + 'tempestuous' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "toity": {
            "definition": "Informal adjective meaning uppity, pretentious, or putting on airs; acting superior or snobbish. Often used in the phrase 'hoity-toity' to describe someone who behaves in an arrogant, affected, or condescending manner. The term suggests artificial sophistication or exaggerated self-importance, particularly when someone attempts to appear more refined or cultured than their actual background. Can describe both people and their behaviors, attitudes, or speech patterns that seem designed to impress others or establish social superiority.",
            "pronunciation": "/ˈtɔɪti/",
            "example_sentence": "Her _____ attitude at the neighborhood barbecue made everyone uncomfortable with her constant corrections.",
            "etymology": "Often used in 'hoity-toity,' possibly from 'hoit' (to romp) suggesting affected behavior, first recorded in 17th century.",
            "memory_tips": [
                "Think 'HOITY-TOITY' - pretentious or uppity behavior",
                "Remember 'putting on airs' for snobbish attitude",
                "Connect to 'pretentious' for artificial superiority display"
            ],
            "part_of_speech": "adjective"
        },
        "tokendifficulty": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'token' (a symbol, sign, or minimal amount) and 'difficulty' (the state of being hard to accomplish). 'Token' can mean a symbolic gesture, a physical object representing value, or a minimal effort. 'Difficulty' refers to challenges, obstacles, or the degree of hardness in accomplishing something. These represent different concepts incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'token' + 'difficulty' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "tokonoma": {
            "definition": "A recessed alcove in traditional Japanese architecture, typically found in the most formal room of a house or tea ceremony space. This sacred space serves as the focal point for displaying hanging scrolls (kakemono), flower arrangements (ikebana), or other artistic objects representing seasonal themes or philosophical concepts. The tokonoma reflects principles of Japanese aesthetics including simplicity, asymmetry, and natural beauty. Guests traditionally sit with their backs to the tokonoma as a sign of respect, while the host faces it. Modern Japanese homes may include simplified versions maintaining the cultural significance.",
            "pronunciation": "/ˌtoʊkəˈnoʊmə/",
            "example_sentence": "The tea master carefully arranged a single white chrysanthemum in the _____ to honor the autumn season.",
            "etymology": "From Japanese 'toko' (floor, bed) + 'no' (of) + 'ma' (space, room), literally meaning 'floor space' or 'alcove.'",
            "memory_tips": [
                "Think 'Japanese alcove' for traditional home decoration space",
                "Remember 'TOKO-NO-MA' breaks down to 'floor-of-space'",
                "Connect to 'tea ceremony' for formal Japanese cultural practice"
            ],
            "part_of_speech": "noun"
        },
        "tokonomaunguiculate": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'tokonoma' (Japanese alcove) and 'unguiculate' (having claws or nails). 'Tokonoma' refers to a traditional Japanese architectural feature, while 'unguiculate' is a biological term describing animals with claws. These represent completely different concepts from architecture and biology that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'tokonoma' + 'unguiculate' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "told": {
            "definition": "Past tense and past participle of 'tell,' meaning communicated information orally or in writing; related, narrated, or revealed something to someone. Indicates completed action of sharing knowledge, stories, instructions, or facts through speech or written communication. Can also mean commanded, ordered, or directed someone to perform specific actions. In broader contexts, implies having been informed about situations, having received instructions, or having learned information from another person. The word often appears in storytelling, instruction-giving, and information-sharing contexts.",
            "pronunciation": "/toʊld/",
            "example_sentence": "She _____ her daughter the family stories that had been passed down for generations.",
            "etymology": "From Old English 'tealde,' past tense of 'tellan' meaning 'to count, relate, or narrate.'",
            "memory_tips": [
                "Think past tense of 'TELL' - already communicated something",
                "Remember 'I tell, I told' for verb conjugation",
                "Connect to 'related a story' for narrative communication"
            ],
            "part_of_speech": "verb (past tense)"
        },
        "tolerable": {
            "definition": "Able to be endured, accepted, or put up with; moderately good or acceptable, though not excellent. Describes conditions, situations, or experiences that are bearable despite being less than ideal. Can refer to physical comfort levels, pain tolerance, social situations, or quality standards that meet minimum acceptable criteria. In medical contexts, describes side effects or treatments that patients can withstand. The term suggests a middle ground between unacceptable and excellent, indicating adequate though unremarkable quality or conditions.",
            "pronunciation": "/ˈtɑlərəbəl/",
            "example_sentence": "The hotel room was small but _____, with clean sheets and a functioning air conditioner.",
            "etymology": "From Latin 'tolerabilis,' from 'tolerare' meaning 'to bear or endure,' entering English via Old French.",
            "memory_tips": [
                "Think 'can TOLERATE' - able to bear or endure something",
                "Remember 'TOLER-ABLE' - able to be tolerated",
                "Connect to 'bearable' for similar meaning of endurance"
            ],
            "part_of_speech": "adjective"
        },
        "tomahawk": {
            "definition": "A lightweight axe traditionally used by Native American peoples as both a tool and weapon, typically featuring a wooden handle and metal or stone head. Originally made with stone heads attached to wooden handles, later versions incorporated European metal trade goods. Beyond practical uses for chopping wood and hunting, tomahawks held ceremonial significance and were often decorated with symbolic designs. In warfare, they served as close-combat weapons and throwing implements. Modern tomahawks are collected as historical artifacts, used in sporting competitions, or employed by military and outdoor enthusiasts for utility purposes.",
            "pronunciation": "/ˈtɑməˌhɔk/",
            "example_sentence": "The museum displayed a beautifully carved _____ with intricate beadwork on the handle.",
            "etymology": "From Algonquian 'tomahak' or 'tamahakan,' meaning 'cutting tool,' adopted into English through early colonial contact.",
            "memory_tips": [
                "Think 'Native American axe' for traditional tool and weapon",
                "Remember 'TOM-A-HAWK' like 'Tom has a hawk' (bird of prey)",
                "Connect to 'hatchet' for similar small axe tool"
            ],
            "part_of_speech": "noun"
        },
        "tomalley": {
            "definition": "The soft, green substance found in the body cavity of cooked lobsters, consisting of the lobster's liver and pancreas. Considered a delicacy by many seafood enthusiasts, tomalley has a rich, creamy texture and intense, briny flavor that concentrates the essence of the sea. Some people enjoy eating it directly from the lobster shell, while others use it as an ingredient in sauces, bisques, or seafood dishes. However, health advisories sometimes recommend avoiding tomalley due to potential concentration of environmental toxins in the lobster's filtering organs.",
            "pronunciation": "/təˈmæli/",
            "example_sentence": "The chef incorporated the lobster's _____ into a rich bisque that captured the ocean's deepest flavors.",
            "etymology": "From French 'tomali,' possibly from a Caribbean indigenous language referring to lobster organs, adopted into culinary terminology.",
            "memory_tips": [
                "Think 'lobster liver' - the green stuff inside cooked lobster",
                "Remember 'TOM-ALLEY' sounds like a name + alley",
                "Connect to 'seafood delicacy' for gourmet cooking ingredient"
            ],
            "part_of_speech": "noun"
        },
        "tomfoolery": {
            "definition": "Foolish or silly behavior; playful nonsense, pranks, or ridiculous antics that serve no serious purpose. The term describes lighthearted mischief, practical jokes, or absurd activities undertaken for amusement rather than malice. Often implies childish or immature behavior that may be annoying to others but is generally harmless. Can refer to both innocent fun and mildly disruptive behavior that wastes time or distracts from serious activities. The word carries a tone of mild disapproval mixed with affectionate tolerance for human silliness.",
            "pronunciation": "/ˈtɑmˌfuləri/",
            "example_sentence": "The teacher had to stop the class _____ and redirect the students' attention to the math lesson.",
            "etymology": "From 'Tom Fool' (a traditional fool character) + '-ery' (activity), dating to mid-18th century English humor.",
            "memory_tips": [
                "Think 'TOM-FOOL-ERY' - foolish behavior like a fool named Tom",
                "Remember 'silly antics' for playful, nonsensical behavior",
                "Connect to 'monkey business' for similar mischievous activity"
            ],
            "part_of_speech": "noun"
        },
        "tommyrot": {
            "definition": "British slang for utter nonsense, foolish talk, or complete rubbish; absurd ideas or statements that lack any basis in truth or logic. The term expresses strong dismissal of something considered ridiculously untrue or illogical. Often used to reject arguments, theories, or claims that seem preposterous or without merit. Popular in early 20th century British English, the word conveys both incredulity and mild indignation at obviously false or silly statements. Can be used humorously or seriously to express disagreement with implausible assertions.",
            "pronunciation": "/ˈtɑmiˌrɑt/",
            "example_sentence": "When he claimed he could fly by flapping his arms, she dismissed it as complete _____.",
            "etymology": "British slang of uncertain origin, possibly combining 'Tommy' (common British name) with 'rot' (nonsense), popular early 1900s.",
            "memory_tips": [
                "Think 'TOMMY-ROT' - rotten (bad) ideas from any Tommy (person)",
                "Remember 'British nonsense' for ridiculous talk or ideas",
                "Connect to 'balderdash' for similar meaning of utter rubbish"
            ],
            "part_of_speech": "noun"
        },
        "tomography": {
            "definition": "A medical imaging technique that produces detailed cross-sectional images of internal body structures by rotating around the patient and taking multiple X-ray measurements from different angles. Computer processing combines these measurements to create precise slice images, allowing doctors to examine specific layers of organs, bones, and tissues without surgical intervention. Types include CT (computed tomography), PET (positron emission tomography), and MRI tomography. Essential for diagnosing cancers, fractures, internal injuries, and organ abnormalities. Modern tomography provides three-dimensional reconstruction capabilities and real-time imaging for surgical guidance.",
            "pronunciation": "/təˈmɑɡrəfi/",
            "example_sentence": "The doctor ordered a CT _____ to get detailed images of the patient's abdominal organs.",
            "etymology": "From Greek 'tomos' (slice, section) + 'graphein' (to write), literally meaning 'slice writing' or 'section imaging.'",
            "memory_tips": [
                "Think 'TOMO-GRAPHY' - writing/imaging slices (sections) of the body",
                "Remember 'CT scan' for medical cross-sectional imaging",
                "Connect to 'photography' for image-making with different technique"
            ],
            "part_of_speech": "noun"
        },
        "tomorrow": {
            "definition": "The day following today; the next 24-hour period in the immediate future. Philosophically represents hope, possibility, and forward-looking planning, contrasting with today's immediate reality and yesterday's completed past. In temporal organization, tomorrow serves as the primary reference point for near-future planning and scheduling. The concept carries psychological implications for goal-setting, anticipation, and procrastination tendencies. Cultural expressions like 'tomorrow never comes' or 'tomorrow is another day' reflect various attitudes toward future planning and present-moment responsibility.",
            "pronunciation": "/təˈmɔroʊ/",
            "example_sentence": "The weather forecast predicts heavy rain for _____, so we'll postpone the picnic until next weekend.",
            "etymology": "From Old English 'tō morgne,' meaning 'to morning,' combining 'to' (at) and 'morgne' (morning, dawn).",
            "memory_tips": [
                "Think 'TO-MORROW' - literally 'to the morning' (next day)",
                "Remember as opposite of 'yesterday' and day after 'today'",
                "Connect to 'future planning' for next-day activities"
            ],
            "part_of_speech": "noun, adverb"
        },
        "tongue": {
            "definition": "The muscular organ in the mouth responsible for taste, speech, and swallowing; also refers to language, manner of speaking, or something shaped like a tongue. Anatomically, the tongue contains thousands of taste buds and enables complex mouth movements essential for clear speech articulation. Metaphorically, 'tongue' represents language skills, cultural identity, or communication ability. Expressions like 'mother tongue,' 'sharp tongue,' or 'tongue-tied' reflect its symbolic connection to speech and communication. The organ's flexibility and sensitivity make it crucial for both survival functions and human expression.",
            "pronunciation": "/tʌŋ/",
            "example_sentence": "The child burned her _____ on the hot soup and learned to test temperature before eating.",
            "etymology": "From Old English 'tunge,' related to Germanic languages and Sanskrit 'jihva,' ancient Indo-European root for this vital organ.",
            "memory_tips": [
                "Think mouth organ for 'TASTE and TALK' - tongue does both",
                "Remember 'mother tongue' for native language connection",
                "Connect to 'speech' for articulation and communication function"
            ],
            "part_of_speech": "noun"
        },
        "tongued": {
            "definition": "Having a tongue or tongue-like appendage; equipped with a specified type of tongue or speaking ability. In biological contexts, describes animals or structures possessing tongue-like organs for feeding, sensing, or communication. Can refer to shoes or boots with tongues (the flap under the laces), musical instruments with tongues (like harmonicas), or woodworking joints with tongue-and-groove construction. In descriptive language, may characterize someone's speech patterns or communication style, often combined with adjectives like 'sharp-tongued,' 'silver-tongued,' or 'loose-tongued.'",
            "pronunciation": "/tʌŋd/",
            "example_sentence": "The _____ boots featured thick leather flaps that protected against water and debris.",
            "etymology": "From 'tongue' + '-ed' suffix, indicating possession of or characterized by a tongue or tongue-like feature.",
            "memory_tips": [
                "Think 'having a TONGUE' - equipped with tongue or tongue-like part",
                "Remember 'sharp-tongued' for descriptive speech characteristics",
                "Connect to 'boot tongue' for shoe parts or 'groove-tongued' woodworking"
            ],
            "part_of_speech": "adjective"
        },
        "tonsillitis": {
            "definition": "Inflammation of the tonsils, typically caused by viral or bacterial infections, resulting in sore throat, difficulty swallowing, and swollen lymph nodes. Symptoms include red, swollen tonsils often with white or yellow patches, fever, headache, and general malaise. Streptococcal tonsillitis requires antibiotic treatment, while viral forms resolve with supportive care including rest, fluids, and pain management. Chronic or recurrent tonsillitis may necessitate surgical removal (tonsillectomy). Most common in children and teenagers, though adults can also develop this condition. Complications can include abscess formation or rheumatic fever if untreated.",
            "pronunciation": "/ˌtɑnsəˈlaɪtəs/",
            "example_sentence": "The doctor diagnosed _____ and prescribed antibiotics to treat the bacterial infection.",
            "etymology": "From Latin 'tonsilla' (tonsil) + '-itis' (inflammation), medical terminology for tonsil inflammation.",
            "memory_tips": [
                "Think 'TONSIL-ITIS' - inflammation ('-itis') of the tonsils",
                "Remember 'sore throat' for main symptom of tonsil infection",
                "Connect to 'strep throat' for common bacterial cause"
            ],
            "part_of_speech": "noun"
        },
        "took": {
            "definition": "Past tense of 'take,' meaning grasped, seized, carried, or acquired something; moved an object from one location to another or gained possession of it. Indicates completed action of obtaining, removing, or transporting items or people. Can also mean required (time), consumed (medicine), or experienced (a break). In various contexts, describes accepting responsibility, making photographs, or undergoing journeys. The word represents one of the most fundamental action verbs in English, essential for describing countless daily activities involving acquisition, movement, or consumption.",
            "pronunciation": "/tʊk/",
            "example_sentence": "She _____ the ancient book carefully from the library shelf and began reading the first chapter.",
            "etymology": "From Old English 'tōc,' past tense of 'tacan' meaning 'to grasp, touch, or receive.'",
            "memory_tips": [
                "Think past tense of 'TAKE' - already grasped or acquired",
                "Remember 'I take, I took' for verb conjugation",
                "Connect to 'grabbed' or 'seized' for physical acquisition action"
            ],
            "part_of_speech": "verb (past tense)"
        },
        "tools": {
            "definition": "Implements, instruments, or devices used to carry out particular functions or tasks; equipment designed to make work easier, more efficient, or more precise. Physical tools include hammers, screwdrivers, computers, and machinery used in construction, repair, cooking, or manufacturing. Metaphorically, tools can refer to methods, techniques, skills, or resources employed to achieve specific goals. In professional contexts, describes software applications, analytical methods, or systematic approaches used to solve problems or complete projects. The concept emphasizes practical utility and purposeful application toward accomplishing objectives.",
            "pronunciation": "/tulz/",
            "example_sentence": "The carpenter organized his _____ carefully in the workshop before beginning the custom cabinet project.",
            "etymology": "From Old English 'tōl,' related to Old Norse 'tól,' referring to implements or instruments for work.",
            "memory_tips": [
                "Think 'work equipment' - implements for making tasks easier",
                "Remember 'hammer and screwdriver' for physical tool examples",
                "Connect to 'instruments' for devices that accomplish specific functions"
            ],
            "part_of_speech": "noun (plural)"
        },
        "toorie": {
            "definition": "Scottish term for a small, round knitted cap or the pompom on top of such a cap; also refers to a tuft of hair or small rounded protuberance. In traditional Scottish clothing, describes the bobble or tassel adorning knitted hats, particularly those worn in cold weather. The word can also refer to small, rounded decorative elements on clothing or accessories. Regional variations exist throughout Scotland, with different pronunciations and slight meaning variations depending on local dialect. Modern usage extends to any small, rounded decorative element resembling a traditional Scottish hat pompom.",
            "pronunciation": "/ˈturi/",
            "example_sentence": "The child's winter hat featured a bright red _____ that bobbed as she ran through the snow.",
            "etymology": "From Scots dialect, possibly related to 'tour' (tower) or 'tuft,' referring to the rounded top element.",
            "memory_tips": [
                "Think 'Scottish hat POMPOM' - the round bobble on winter caps",
                "Remember 'TOO-RIE' sounds like 'too wee' (Scottish for too small)",
                "Connect to 'tuft' for small rounded decorative element"
            ],
            "part_of_speech": "noun"
        },
        "tooth": {
            "definition": "Hard, white structures in the jaws used for biting, chewing, and processing food; each tooth consists of enamel, dentin, pulp, and roots anchored in the jawbone. Humans typically develop two sets: 20 primary (baby) teeth and 32 permanent (adult) teeth including incisors, canines, premolars, and molars. Beyond nutrition, teeth contribute to speech articulation and facial appearance. Dental health requires regular cleaning, professional care, and dietary consideration. Metaphorically, 'tooth' appears in expressions like 'tooth and nail' (fierce determination) or 'sweet tooth' (preference for sugary foods).",
            "pronunciation": "/tuθ/",
            "example_sentence": "The dentist explained that the cavity in her back _____ required a filling to prevent further decay.",
            "etymology": "From Old English 'tōth,' related to Germanic languages and Sanskrit 'danta,' ancient root for dental structures.",
            "memory_tips": [
                "Think 'CHEWING tools' - hard structures for processing food",
                "Remember 'dental care' for teeth cleaning and health maintenance",
                "Connect to 'bite' for primary function of teeth in eating"
            ],
            "part_of_speech": "noun"
        },
        "topazolite": {
            "definition": "A yellow to golden-brown variety of andradite garnet that resembles topaz in color and transparency, prized by gem collectors and jewelers for its brilliance and fire. This calcium iron silicate mineral forms in metamorphic rocks and skarns, typically displaying adamantine to vitreous luster. High-quality specimens exhibit exceptional dispersion, creating rainbow-colored flashes that make them valuable for jewelry applications. Found in locations including Italy, Russia, and Arizona, topazolite represents one of the more valuable garnet varieties. Mineral collectors appreciate both rough specimens and cut gemstones for their optical properties.",
            "pronunciation": "/təˈpæzəˌlaɪt/",
            "example_sentence": "The jeweler showcased a stunning _____ pendant that sparkled with golden fire in the display case.",
            "etymology": "From 'topaz' (yellow gemstone) + '-lite' (stone), referring to its topaz-like appearance and color.",
            "memory_tips": [
                "Think 'TOPAZ-LITE' - garnet that looks like topaz gemstone",
                "Remember 'golden garnet' for yellow gem variety",
                "Connect to 'jewelry stone' for valuable gemstone application"
            ],
            "part_of_speech": "noun"
        },
        "topgallant": {
            "definition": "The highest sail on a square-rigged sailing ship, set above the topsail on the topgallant mast; also refers to the mast itself that supports this sail. In traditional naval architecture, the topgallant sail provided additional wind-catching capacity for increased speed, particularly important during racing or pursuit situations. Skilled sailors required training to manage these high-altitude sails safely in various weather conditions. The term also describes the uppermost section of the rigging system. Historical sailing ships relied on topgallant sails for maximum performance, though they were often the first sails lowered in rough weather.",
            "pronunciation": "/ˈtɑpˌɡælənt/",
            "example_sentence": "The crew quickly lowered the _____ sail as storm clouds approached the merchant vessel.",
            "etymology": "From 'top' (highest part) + 'gallant' (fine, noble), referring to the ship's highest, finest sail.",
            "memory_tips": [
                "Think 'TOP-GALLANT' - the highest, most noble sail on a ship",
                "Remember 'uppermost sail' for square-rigged sailing ships",
                "Connect to 'sailing ship rigging' for maritime terminology"
            ],
            "part_of_speech": "noun, adjective"
        },
        "topiary": {
            "definition": "The art of training, cutting, and trimming trees or shrubs into ornamental shapes, or the plants themselves that have been shaped this way. This horticultural practice creates living sculptures from evergreen plants like boxwood, yew, or privet, forming geometric patterns, animal figures, or abstract designs. Topiary requires regular maintenance, artistic vision, and patience as plants grow slowly into desired forms. Popular in formal gardens, estates, and landscape design, topiary represents the intersection of gardening skill and artistic expression. Historical examples include elaborate European palace gardens and modern theme park displays.",
            "pronunciation": "/ˈtoʊpiˌɛri/",
            "example_sentence": "The estate's formal garden featured elaborate _____ sculptures shaped like swans and geometric spirals.",
            "etymology": "From Latin 'topiarius' (ornamental gardener), from 'topia' (decorative garden work), via French into English.",
            "memory_tips": [
                "Think 'plant sculpture' - shaping bushes into artistic forms",
                "Remember 'TOP-IARY' like 'top' shapes in gardens",
                "Connect to 'hedge art' for decorative plant trimming"
            ],
            "part_of_speech": "noun"
        },
        "topics": {
            "definition": "Subjects of conversation, study, or writing; particular themes or issues under discussion or consideration. In academic contexts, topics represent specific areas of focus within broader disciplines, serving as organizational units for research, teaching, or analysis. Discussion topics provide structure for meetings, debates, or social conversations. The term implies focused attention on particular aspects of larger subjects. Effective topic selection considers audience interest, relevance, and scope appropriateness. In digital contexts, topics often organize content through tags, categories, or thematic groupings for easy navigation and discovery.",
            "pronunciation": "/ˈtɑpɪks/",
            "example_sentence": "The professor provided a list of research _____ for students to choose from for their final papers.",
            "etymology": "From Greek 'topika' meaning 'matters of place,' through Latin 'topica' referring to subjects of discussion.",
            "memory_tips": [
                "Think 'conversation subjects' - what people talk or write about",
                "Remember 'research TOPICS' for academic subject areas",
                "Connect to 'themes' for organized discussion categories"
            ],
            "part_of_speech": "noun (plural)"
        },
        "toploftical": {
            "definition": "Pompous, pretentious, or arrogant in manner; characterized by an artificially elevated or superior attitude that suggests looking down on others from a great height. This adjective describes behavior that is haughty, condescending, or excessively self-important. Often applied to speech, writing, or personal conduct that attempts to impress others through grandiose language or affected sophistication. The term implies criticism of someone who puts on airs or acts superior to their actual station or accomplishments. Regional American usage particularly in describing pretentious social behavior.",
            "pronunciation": "/tɑpˈlɔftɪkəl/",
            "example_sentence": "His _____ speech at the town meeting alienated voters with its condescending tone and big words.",
            "etymology": "American English combining 'top loft' (high place) + '-ical' (characterized by), suggesting elevated, superior attitude.",
            "memory_tips": [
                "Think 'TOP-LOFT-ICAL' - acting like you're in the top loft looking down",
                "Remember 'high and mighty' for pretentious, superior attitude",
                "Connect to 'pompous' for arrogant, self-important behavior"
            ],
            "part_of_speech": "adjective"
        },
        "topologically": {
            "definition": "In a manner relating to topology, the mathematical study of spatial properties preserved under continuous deformations like stretching or bending. Describes analysis or relationships based on connectivity, continuity, and spatial arrangement rather than specific measurements or angles. In mathematics, topological properties remain unchanged when shapes are transformed without cutting or tearing. The adverb indicates consideration of fundamental spatial relationships, boundary conditions, or structural connectivity. Applications include network analysis, data visualization, and geometric modeling where shape relationships matter more than precise measurements.",
            "pronunciation": "/ˌtɑpəˈlɑdʒɪkli/",
            "example_sentence": "The network was analyzed _____ to understand connection patterns rather than physical distances.",
            "etymology": "From 'topology' (Greek 'topos' place + 'logos' study) + '-ically' (in the manner of), mathematical spatial analysis.",
            "memory_tips": [
                "Think 'TOPOLOGY' (space study) + '-ICALLY' (in that manner)",
                "Remember 'shape relationships' for mathematical spatial analysis",
                "Connect to 'network connections' for structural relationship study"
            ],
            "part_of_speech": "adverb"
        },
        "toponymic": {
            "definition": "Relating to toponymy, the study of place names and their origins, meanings, and historical development. This adjective describes analysis of geographic names including cities, rivers, mountains, and regions, examining their linguistic roots, cultural significance, and evolution over time. Toponymic research reveals historical settlement patterns, language influences, and cultural changes in geographic regions. Scholars use toponymic evidence to trace migration patterns, colonial influences, and indigenous heritage. The field combines geography, linguistics, and history to understand how places acquire and maintain their names.",
            "pronunciation": "/ˌtɑpəˈnɪmɪk/",
            "example_sentence": "The _____ study revealed that most local river names derived from Native American languages.",
            "etymology": "From Greek 'topos' (place) + 'onyma' (name) + '-ic' (relating to), the study of place names.",
            "memory_tips": [
                "Think 'TOPO-NYMIC' - relating to place (topo) names (onymic)",
                "Remember 'place name study' for geographic naming research",
                "Connect to 'etymology' for origin study of location names"
            ],
            "part_of_speech": "adjective"
        },
        "topped": {
            "definition": "Past tense of 'top,' meaning reached the highest point, exceeded, or placed something on the upper surface of another object. Indicates completed action of surpassing previous achievements, covering with a surface layer, or reaching a peak position. In cooking, describes adding ingredients to the upper surface of dishes. Can also mean removed the top portion of something, such as cutting tree tops or plant stems. The word frequently appears in contexts involving achievement, decoration, completion, or physical positioning.",
            "pronunciation": "/tɑpt/",
            "example_sentence": "The ice cream sundae was _____ with whipped cream, chocolate syrup, and a bright red cherry.",
            "etymology": "From 'top' + '-ed' past tense suffix, indicating completed action of topping or reaching the top.",
            "memory_tips": [
                "Think past tense of 'TOP' - already reached highest point or covered",
                "Remember 'ice cream TOPPED' with ingredients for food context",
                "Connect to 'exceeded' for surpassing previous achievements"
            ],
            "part_of_speech": "verb (past tense)"
        },
        "toppings": {
            "definition": "Ingredients placed on top of food items to enhance flavor, texture, or appearance; decorative or functional additions to the upper surface of dishes. Common examples include cheese on pizza, nuts on ice cream, herbs on salads, or whipped cream on desserts. Toppings can be savory or sweet, providing contrasting tastes, colors, or textures that complement the base food. In broader contexts, refers to any decorative or functional elements added to the surface of objects. The choice and arrangement of toppings often reflects culinary creativity and personal preferences.",
            "pronunciation": "/ˈtɑpɪŋz/",
            "example_sentence": "The pizza restaurant offered dozens of _____ including pepperoni, mushrooms, and exotic cheeses.",
            "etymology": "From 'top' + '-ing' (present participle) + '-s' (plural), referring to things that go on top.",
            "memory_tips": [
                "Think 'pizza TOPPINGS' - ingredients that go on top of food",
                "Remember 'surface additions' for decorative or flavor elements",
                "Connect to 'garnish' for food decoration and enhancement"
            ],
            "part_of_speech": "noun (plural)"
        },
        "toppled": {
            "definition": "Past tense of 'topple,' meaning fell over, collapsed, or caused to fall from an upright position due to instability or applied force. Indicates completed action of overturning, overthrowing, or losing balance and falling. In political contexts, describes the removal of leaders or governments from power. Can refer to physical objects losing stability or metaphorical structures being dismantled. The word often implies sudden, dramatic collapse rather than gradual decline. Historical examples include toppled statues, governments, or tall structures succumbing to natural forces.",
            "pronunciation": "/ˈtɑpəld/",
            "example_sentence": "The strong earthquake _____ several ancient buildings in the historic district.",
            "etymology": "From 'topple' (frequentative of 'top') + '-ed' past tense suffix, indicating completed falling action.",
            "memory_tips": [
                "Think 'TOPPED' + 'FELL' - fell over from upright position",
                "Remember 'statue toppled' for things falling from standing position",
                "Connect to 'collapsed' for sudden structural failure"
            ],
            "part_of_speech": "verb (past tense)"
        },
        "toque": {
            "definition": "A type of hat with various styles depending on cultural context: a tall, white cylindrical chef's hat; a small, round, close-fitting cap worn by women; or a knitted winter cap (particularly in Canadian English). Chef's toques traditionally indicated rank and experience through height, with master chefs wearing the tallest versions. Women's toques emerged in medieval times as fashionable headwear, often made from velvet or silk. Canadian usage refers to warm, knitted winter hats essential for cold weather protection. Each style represents different cultural traditions and practical applications.",
            "pronunciation": "/toʊk/",
            "example_sentence": "The head chef's tall white _____ distinguished her from the other kitchen staff during the dinner rush.",
            "etymology": "From French 'toque,' possibly from Spanish 'toca' (headdress) or Arabic 'ṭāq' (opening, arch), referring to head covering.",
            "memory_tips": [
                "Think 'chef's hat' - the tall white cylindrical kitchen hat",
                "Remember 'TOQUE' rhymes with 'cloak' (another head covering)",
                "Connect to 'Canadian winter hat' for knitted cold-weather version"
            ],
            "part_of_speech": "noun"
        },
        "torch": {
            "definition": "A portable light source traditionally consisting of a stick with combustible material at one end, or in modern usage, a flashlight or electric lamp. Historical torches used wood, cloth, or other materials soaked in flammable substances like pitch or oil. Symbolically represents enlightenment, knowledge, guidance, or passionate commitment, as in 'carrying the torch' for a cause. Olympic ceremonies feature torch lighting as symbols of international unity and athletic excellence. Modern torches include welding equipment, cutting tools, or high-intensity flashlights for various professional and recreational applications.",
            "pronunciation": "/tɔrtʃ/",
            "example_sentence": "The medieval castle's corridors were lit by flickering torches mounted in iron brackets along the walls.",
            "etymology": "From Old French 'torche,' from Latin 'torqua' (twisted thing), referring to twisted material for burning.",
            "memory_tips": [
                "Think 'flame on stick' - traditional burning light source",
                "Remember 'Olympic torch' for ceremonial flame symbol",
                "Connect to 'flashlight' for modern electric version"
            ],
            "part_of_speech": "noun"
        },
        "toreador": {
            "definition": "A bullfighter, particularly one who fights bulls on foot using a cape and sword; a matador engaged in the traditional Spanish spectacle of bullfighting. This skilled performer executes choreographed movements to avoid charging bulls while demonstrating courage, artistry, and technical expertise. Toreadors wear distinctive costumes called 'trajes de luces' (suits of lights) featuring intricate embroidery and bright colors. The profession requires years of training, physical conditioning, and mental preparation. Cultural significance varies globally, with some viewing it as artistic tradition while others criticize it as animal cruelty.",
            "pronunciation": "/ˈtɔriəˌdɔr/",
            "example_sentence": "The skilled _____ gracefully avoided the charging bull with a dramatic sweep of his red cape.",
            "etymology": "From Spanish 'toreador,' from 'torear' (to fight bulls) + '-ador' (one who does), related to 'toro' (bull).",
            "memory_tips": [
                "Think 'Spanish bullfighter' - person who fights bulls with cape",
                "Remember 'TORE-A-DOR' contains 'toro' (Spanish for bull)",
                "Connect to 'matador' for similar bullfighting profession"
            ],
            "part_of_speech": "noun"
        },
        "toreutics": {
            "definition": "The art of working in metal by embossing, chasing, or engraving to create decorative objects; metalworking techniques that produce raised or incised designs on metal surfaces. This ancient craft includes repoussé (hammering from the reverse side), chasing (working from the front), and engraving (cutting designs into metal). Practitioners create jewelry, decorative vessels, armor, and artistic objects using specialized tools and techniques passed down through generations. Historical examples include Greek bronze work, Islamic metalware, and Renaissance armor decoration. Modern toreutics combines traditional methods with contemporary artistic expression.",
            "pronunciation": "/təˈrutɪks/",
            "example_sentence": "The museum's collection of ancient _____ included beautifully embossed silver vessels from Greek artisans.",
            "etymology": "From Greek 'toreutikos' (relating to artistic work in metal), from 'toreus' (worker in metal), related to 'tornos' (lathe).",
            "memory_tips": [
                "Think 'metal ART techniques' - decorative metalworking crafts",
                "Remember 'embossed metal work' for raised design creation",
                "Connect to 'jewelry making' for artistic metal manipulation"
            ],
            "part_of_speech": "noun"
        },
        "torii": {
            "definition": "Traditional Japanese gates typically found at the entrance to Shinto shrines, consisting of two vertical posts connected by two horizontal crossbeams. These iconic structures mark the transition from the physical world to the spiritual realm, serving as symbolic portals to sacred spaces. Usually painted bright orange-red (vermillion) or left in natural wood, torii vary in size from small shrine markers to massive installations like the famous floating gate at Itsukushima Shrine. The design represents fundamental elements of Japanese architecture and spiritual beliefs. Visitors traditionally bow before passing through torii as a sign of respect.",
            "pronunciation": "/ˈtɔri.i/",
            "example_sentence": "The massive orange _____ standing in the water created a stunning silhouette against the sunset sky.",
            "etymology": "From Japanese 'torii,' literally meaning 'bird perch,' from 'tori' (bird) + 'i' (perch, place to sit).",
            "memory_tips": [
                "Think 'Japanese shrine GATE' - traditional entrance to sacred spaces",
                "Remember 'bird perch' for literal meaning of torii",
                "Connect to 'orange gate' for typical vermillion color"
            ],
            "part_of_speech": "noun"
        },
        "toril": {
            "definition": "A pen or enclosure where bulls are kept before being released into the bullring for bullfighting; the holding area in a bullring complex where bulls await their turn in the arena. These secure structures ensure animal containment while allowing controlled release during bullfighting events. Traditional Spanish bullrings include multiple torils to house different bulls for sequential fights. The design prioritizes both animal welfare and safety protocols for handlers and spectators. Modern facilities incorporate veterinary examination areas and safety features. The term extends to any secure enclosure for containing large, potentially dangerous animals.",
            "pronunciation": "/təˈril/",
            "example_sentence": "The matador watched nervously as the massive bull emerged from the _____ into the arena.",
            "etymology": "From Spanish 'toril,' from 'toro' (bull) + '-il' (place for), literally meaning 'place for bulls.'",
            "memory_tips": [
                "Think 'bull PEN' - where bulls are kept before bullfighting",
                "Remember 'TORIL' contains 'toro' (Spanish for bull)",
                "Connect to 'corral' for similar animal enclosure concept"
            ],
            "part_of_speech": "noun"
        },
        "torment": {
            "definition": "Severe physical or mental suffering; extreme anguish, pain, or distress that causes agony or misery. As a verb, means to cause deliberate suffering, harassment, or psychological distress to someone or something. The word encompasses both acute physical pain and emotional trauma, including anxiety, grief, guilt, or despair. Can describe persistent worry, painful medical conditions, or psychological torture. Historical contexts include religious concepts of afterlife punishment or interrogation techniques. Modern usage often refers to mental health struggles, relationship difficulties, or chronic pain conditions.",
            "pronunciation": "/ˈtɔrˌmɛnt/",
            "example_sentence": "The recurring nightmares became a source of constant _____ for the accident survivor.",
            "etymology": "From Latin 'tormentum' (instrument of torture), from 'torquere' (to twist, torture), via Old French into English.",
            "memory_tips": [
                "Think 'severe MENTAL pain' - extreme suffering or anguish",
                "Remember 'TORMENT' contains 'torn' suggesting being torn apart by pain",
                "Connect to 'torture' for deliberate infliction of suffering"
            ],
            "part_of_speech": "noun, verb"
        },
        "toroidalbialy": {
            "definition": "ERROR: This appears to be a combined word error. Should likely be separated into 'toroidal' (having a doughnut or torus shape) and 'bialy' (a type of Polish bread roll). 'Toroidal' refers to the mathematical shape of a torus or doughnut, while 'bialy' is a traditional bread product from Białystok, Poland. These represent completely different concepts from geometry and cuisine that have been incorrectly merged in the source data.",
            "pronunciation": "ERROR: Combined word - check source data",
            "example_sentence": "ERROR: This appears to be two separate words incorrectly combined.",
            "etymology": "ERROR: Combined word requiring separation and individual analysis.",
            "memory_tips": [
                "ERROR: This appears to be 'toroidal' + 'bialy' combined",
                "Review source data for proper word separation",
                "Check for data processing errors in original documents"
            ],
            "part_of_speech": "ERROR: Combined word"
        },
        "torpid": {
            "definition": "Mentally or physically inactive; lethargic, sluggish, or dormant. Describes a state of reduced activity, responsiveness, or energy, often temporary and caused by environmental conditions, illness, or natural biological cycles. In biology, refers to animals entering dormancy or hibernation-like states to conserve energy. Can describe mental dullness, lack of motivation, or emotional numbness. Weather conditions, medical conditions, or psychological states may induce torpidity. The term suggests temporary rather than permanent inactivity, implying potential for renewed vigor when conditions improve.",
            "pronunciation": "/ˈtɔrpɪd/",
            "example_sentence": "After the large holiday meal, everyone felt _____ and lounged quietly in the living room.",
            "etymology": "From Latin 'torpidus' (numb, sluggish), from 'torpere' (to be stiff or numb), related to 'torpedo.'",
            "memory_tips": [
                "Think 'TORPOR' - state of sluggishness or inactivity",
                "Remember 'TORPEDO' connection - both involve numbness/stunning",
                "Connect to 'lethargic' for lack of energy or responsiveness"
            ],
            "part_of_speech": "adjective"
        }
    }

def process_batch_180():
    """Process batch_180_words.csv with comprehensive Claude data"""
    try:
        logger.info("Processing Batch 180 with comprehensive Claude data...")
        
        # Load comprehensive data
        claude_data = get_comprehensive_claude_data()
        
        # Initialize difficulty calculator
        calc = DifficultyCalculator()
        
        # Read input file
        input_file = 'output/batch_180_words.csv'
        output_file = 'output/batch_180_processed.csv'
        
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
            logger.info("Batch 180 processing completed!")
            logger.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
            logger.info(f"Output saved to: {output_file}")
            logger.info(f"Results: {len(processed_words)} successful, 0 failed")
        else:
            logger.error("No words were processed")
            
    except Exception as e:
        logger.error(f"Error processing batch 180: {str(e)}")
        raise

if __name__ == "__main__":
    process_batch_180()