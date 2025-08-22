#!/usr/bin/env python3
"""
Process batch 168 of spelling bee words.
Reads from batch_168_words.csv and generates comprehensive word data.
"""

import csv
import os

class DifficultyCalculator:
    @staticmethod
    def calculate_phonetic_transparency(word, pronunciation):
        # Simple heuristic: ratio of phonetic symbols to letters
        if not pronunciation:
            return 5
        
        # Count phonetic symbols that don't directly correspond to letters
        complex_phonemes = ['θ', 'ð', 'ʃ', 'ʒ', 'tʃ', 'dʒ', 'ŋ', 'j', 'w', 'ɹ', 'ə', 'ɪ', 'ʊ', 'ɛ', 'ɔ', 'æ', 'ʌ', 'ɑ']
        phonetic_complexity = sum(1 for symbol in complex_phonemes if symbol in pronunciation)
        
        return min(10, max(1, phonetic_complexity + len(word) // 3))
    
    @staticmethod
    def calculate_frequency_score(word):
        # Common words get lower scores (easier)
        common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use']
        if word.lower() in common_words:
            return 1
        elif len(word) <= 4:
            return 2
        elif len(word) <= 6:
            return 4
        elif len(word) <= 8:
            return 6
        else:
            return 8
    
    @staticmethod
    def calculate_morphological_complexity(word):
        # Count morphemes, prefixes, suffixes
        prefixes = ['pre', 'pro', 'anti', 'semi', 'multi', 'inter', 'trans', 'super', 'sub', 'un', 're', 'dis', 'mis', 'over', 'under', 'out']
        suffixes = ['tion', 'sion', 'ness', 'ment', 'able', 'ible', 'ful', 'less', 'ous', 'ious', 'eous', 'ive', 'ity', 'ty', 'ly', 'ing', 'ed', 'er', 'est']
        
        complexity = len(word) // 4  # Base complexity
        
        for prefix in prefixes:
            if word.lower().startswith(prefix):
                complexity += 2
                break
                
        for suffix in suffixes:
            if word.lower().endswith(suffix):
                complexity += 2
                break
        
        return min(10, max(1, complexity))
    
    @staticmethod
    def calculate_etymology_complexity(etymology, language_origin):
        # Rate complexity based on language origin and etymology depth
        if not etymology and not language_origin:
            return 5
            
        complex_origins = ['Sanskrit', 'Ancient Greek', 'Latin', 'Old French', 'Middle English', 'Proto-Germanic', 'Hebrew', 'Arabic']
        simple_origins = ['English', 'German', 'Spanish', 'Italian', 'Portuguese']
        
        complexity = 5  # Default
        
        if language_origin:
            if any(origin in language_origin for origin in complex_origins):
                complexity += 3
            elif any(origin in language_origin for origin in simple_origins):
                complexity += 1
        
        if etymology and len(etymology) > 100:
            complexity += 2
            
        return min(10, max(1, complexity))

def main():
    input_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_168_words.csv"
    output_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_168_processed.csv"
    
    # Comprehensive word data with educational content
    word_data = {
        "stalwart": {
            "pronunciation": "/ˈstɔlwərt/",
            "definition": "Loyal, committed, and hardworking; steadfast and unwavering in support or allegiance; physically strong and robust. Stalwart supporters remain faithful to causes, parties, or leaders through difficult times and changing circumstances. The term describes people who demonstrate consistent reliability and dedication despite challenges or opposition. Stalwart character involves moral courage, principled stands, and willingness to endure hardship for important beliefs. Political stalwarts maintain party loyalty and work tirelessly for shared goals. Stalwart allies provide dependable support during conflicts or crises. Physical stalwartness suggests robust health and strength that enables sustained effort and resilience. Organizations benefit from stalwart members who contribute consistently and can be counted on during challenging periods. The quality combines loyalty, strength, and reliability into a character trait highly valued in personal relationships and professional settings.",
            "etymology": "From Middle English, compound of 'stal' (place, position) + 'worth' (worthy), originally meaning 'worth one's place' or 'serviceable.'",
            "memory_tip": "STALWART: Someone who will STALL and stand firm, showing they're WORTH your trust",
            "example_sentence": "The _____ volunteers worked tirelessly to support the community during the crisis.",
            "language_origin": "Middle English",
            "source_difficulty": "Multiple Bee levels"
        },
        "stamina": {
            "pronunciation": "/ˈstæmənə/",
            "definition": "The ability to sustain prolonged physical or mental effort; endurance and staying power that enables continued performance despite fatigue. Physical stamina allows athletes to maintain performance through long competitions or training sessions. Mental stamina enables students, workers, and professionals to concentrate and produce quality work over extended periods. Building stamina requires gradual conditioning that progressively increases demands on physical or mental systems. Cardiovascular stamina improves through aerobic exercise that strengthens heart and lung capacity. Intellectual stamina develops through challenging mental activities that extend concentration periods. Emotional stamina helps people cope with stress, adversity, and demanding situations without breaking down. The concept emphasizes sustained capability rather than peak performance, suggesting the value of endurance over brief bursts of effort. Understanding stamina helps in planning training programs, work schedules, and personal development strategies that build long-term capacity.",
            "etymology": "From Latin 'stamina,' plural of 'stamen' meaning the warp in weaving or threads of life spun by the Fates. Extended to mean endurance or staying power.",
            "memory_tip": "STAMINA: The ability to keep going like strong threads that don't BREAK under pressure",
            "example_sentence": "Marathon runners develop exceptional _____ through months of consistent training.",
            "language_origin": "Latin",
            "source_difficulty": "Multiple Bee levels"
        },
        "stampede": {
            "pronunciation": "/stæmˈpid/",
            "definition": "A sudden rush of frightened animals, especially cattle or horses; any sudden mass movement of people driven by panic or enthusiasm; to cause such a rush or to move in such a manner. Cattle stampedes can occur when animals are startled by loud noises, predators, or sudden movements, creating dangerous situations for ranchers and livestock. Human stampedes might happen during emergencies when crowds panic and rush toward exits, sometimes causing injuries or fatalities. The word can describe any situation where groups move rapidly and chaotically due to fear, excitement, or urgency. Stock market stampedes involve rapid selling or buying based on panic or speculation rather than rational analysis. Political stampedes occur when public opinion shifts quickly in response to events or campaigns. The phenomenon emphasizes the power of group psychology and the importance of crowd control measures in preventing dangerous situations.",
            "etymology": "From Mexican Spanish 'estampida,' from 'estampar' meaning to stamp or print, referring to the stamping sound of many hooves.",
            "memory_tip": "STAMPEDE: Animals STAMP their feet as they SPEED away in panic",
            "example_sentence": "The sudden thunderclap caused a _____ as the cattle bolted across the pasture.",
            "language_origin": "Mexican Spanish",
            "source_difficulty": "Multiple Bee levels"
        },
        "stamping": {
            "pronunciation": "/ˈstæmpɪŋ/",
            "definition": "Present participle of stamp; pressing forcefully with the foot; marking with an official seal or impression; manufacturing by pressing metal into shapes. Stamping involves forceful downward pressure, whether with feet expressing emotion or with tools creating impressions. Children might stamp their feet when frustrated or excited, expressing feelings through physical action. Official stamping validates documents, passports, or certificates with authorized marks or seals. Industrial stamping shapes metal parts through hydraulic presses that force material into specific forms. Rubber stamping creates repetitive marks for addressing, dating, or marking documents. The action suggests authority, emphasis, or manufacturing precision depending on context. Stamping can express approval (rubber stamping), disapproval (stamping feet), or create permanent marks that serve identification or validation purposes. Understanding stamping helps recognize both emotional expression and manufacturing processes that rely on forceful pressure application.",
            "etymology": "Present participle of 'stamp,' from Middle English 'stampen,' from Old English 'stampian' meaning to pound or crush.",
            "memory_tip": "STAMPING: STAMPING down with force, like putting your STAMP of approval on something",
            "example_sentence": "She was _____ her feet impatiently while waiting for the bus.",
            "language_origin": "Old English",
            "source_difficulty": "Three Bee"
        },
        "stance": {
            "pronunciation": "/stæns/",
            "definition": "The way in which someone stands; a person's attitude or position on a particular issue; a physical posture adopted for a specific purpose. Physical stance affects balance, stability, and ability to move or react effectively. Athletic stances vary by sport, with tennis players adopting ready positions, golfers addressing balls with specific postures, and martial artists using combat-ready stances. Political stances represent positions on issues, policies, or candidates that guide voting and advocacy behavior. Moral stances involve principled positions on ethical questions that shape decision-making and character. Professional stances might include approaches to work, client relationships, or industry practices. The term suggests both physical positioning and ideological positioning that provides foundation for action. Understanding stance helps recognize the importance of positioning, whether physical or philosophical, in achieving effectiveness and maintaining consistency.",
            "etymology": "From Old French 'estance,' from Latin 'stantia' meaning a standing or position, from 'stare' (to stand).",
            "memory_tip": "STANCE: How you STAND physically or where you STAND on issues",
            "example_sentence": "The politician clarified her _____ on environmental protection during the debate.",
            "language_origin": "Old French, Latin",
            "source_difficulty": "Multiple Bee levels"
        },
        "stanchion": {
            "pronunciation": "/ˈstæntʃən/",
            "definition": "An upright bar, post, or frame forming a support or barrier; a device used to restrict the movement of cattle in barns. Stanchions provide structural support in buildings, ships, and other constructions where vertical posts are needed. Marine stanchions support railings and safety lines on boats and ships. Crowd control stanchions guide pedestrian traffic and form barriers at events, airports, and public spaces. Cattle stanchions in barns secure animals during feeding or milking while allowing limited head movement. The posts typically connect horizontal elements like rails, ropes, or barriers to create functional systems. Stanchions must be strong enough to withstand pressure from whatever they're supporting or restraining. Modern stanchions often feature adjustable heights, portable bases, or decorative elements that combine function with aesthetics. Understanding stanchions helps recognize the importance of vertical support elements in various structural and organizational applications.",
            "etymology": "From Old French 'estanchon,' from 'estancher' meaning to prop or support, related to 'stanch' meaning to stop flow.",
            "memory_tip": "STANCHION: A post that helps you STAND and keeps things in their proper STATION",
            "example_sentence": "The museum used velvet ropes connected to brass _____ to guide visitors through the exhibition.",
            "language_origin": "Old French",
            "source_difficulty": "Multiple Bee levels"
        },
        "stand": {
            "pronunciation": "/stænd/",
            "definition": "To be in an upright position on the feet; to be located in a particular place; to hold a particular opinion or attitude; a structure for supporting or displaying things. Standing involves maintaining vertical posture through balance and muscle control. People stand to show respect, attention, or readiness for action. Political stands represent positions on issues or principles that guide decision-making. Stands can be physical structures like music stands, fruit stands, or grandstands that support or display items. Taking a stand means adopting a firm position on controversial or important matters. Standing up for beliefs requires courage and conviction. The verb suggests stability, presence, and readiness while the noun indicates support or position. Understanding standing helps recognize both physical capabilities and moral positioning that demonstrate character and capability.",
            "etymology": "From Old English 'standan,' related to German 'stehen' and Latin 'stare,' all meaning to be in an upright position.",
            "memory_tip": "STAND: To be upright and ready, like taking a STAND for what you believe",
            "example_sentence": "She decided to _____ up for her principles despite pressure to compromise.",
            "language_origin": "Old English",
            "source_difficulty": "Multiple Bee levels"
        },
        "standard": {
            "pronunciation": "/ˈstændərd/",
            "definition": "A level of quality or attainment; a flag or banner; something established as a measure or model; typical or usual. Quality standards define minimum acceptable levels for products, services, or performance. Educational standards specify learning objectives and achievement levels for students at different grades. Professional standards guide ethical behavior and competency requirements in various fields. Standard measurements provide consistent units for comparison and commerce. Military standards include flags, emblems, and protocols that represent units and authority. Living standards reflect quality of life through income, housing, healthcare, and other factors. The word suggests both measurement criteria and typical examples that serve as references. Standards enable comparison, quality control, and coordination across different contexts and organizations. Understanding standards helps recognize the importance of consistent criteria for evaluation and excellence.",
            "etymology": "From Old French 'estandard,' possibly from Frankish 'standhard' meaning 'stand hard,' originally referring to a military flag or rallying point.",
            "memory_tip": "STANDARD: A level or flag that helps everyone STAND together under the same rules",
            "example_sentence": "The company maintained high quality _____ throughout its manufacturing process.",
            "language_origin": "Old French, Frankish",
            "source_difficulty": "Multiple Bee levels"
        },
        "standee": {
            "pronunciation": "/stænˈdi/",
            "definition": "A person who stands, especially because no seats are available; a life-sized cardboard cutout used for advertising or display. Transit standees are passengers who must stand on buses, trains, or subways when all seats are occupied. Theater standees wait for possible tickets or standing room when shows are sold out. Advertising standees are promotional displays featuring products, celebrities, or characters that attract attention in stores or events. The term emphasizes the standing position as a defining characteristic or necessity. Concert standees might enjoy better views but sacrifice comfort during long performances. Movie theater standees display upcoming films or promotional materials. Standing accommodations often cost less than seated options but require more physical endurance. Understanding standees helps recognize both transportation realities and marketing strategies that utilize vertical display formats.",
            "etymology": "From 'stand' + suffix '-ee' indicating a person who performs an action or is in a particular state.",
            "memory_tip": "STANDEE: Someone who has to STAND, or a display that STANDS up",
            "example_sentence": "The crowded subway car was filled with _____ during the morning rush hour.",
            "language_origin": "English",
            "source_difficulty": "Multiple Bee levels"
        },
        "stands": {
            "pronunciation": "/stændz/",
            "definition": "Third person singular present of stand; plural of stand; structures that support or hold things; seating areas at sports venues. Someone stands when they rise to an upright position or maintain a vertical posture. Stadium stands provide elevated seating for spectators at sporting events and concerts. Market stands offer temporary retail spaces for vendors selling goods. Music stands hold sheet music at appropriate heights for performers. The plural form can refer to multiple support structures or positions taken on various issues. Bandstands provide elevated platforms for musical performances in parks or public spaces. Grandstands offer tiered seating that improves viewing angles for large crowds. Understanding stands helps recognize both the action of standing and the structures that support people or objects in various contexts from commerce to entertainment.",
            "etymology": "Plural and third person singular form of 'stand,' from Old English 'standan.' Multiple meanings developed from the basic concept of upright position.",
            "memory_tip": "STANDS: Multiple places where people STAND, or when someone takes a position and STANDS firm",
            "example_sentence": "The baseball _____ filled with cheering fans as the home team scored.",
            "language_origin": "Old English",
            "source_difficulty": "Three Bee"
        },
        "stannum": {
            "pronunciation": "/ˈstænəm/",
            "definition": "The Latin name for tin, represented by the chemical symbol Sn in the periodic table; used in scientific and technical contexts to refer to this metallic element. Stannum (tin) is a silvery-white metal that resists corrosion and has been used by humans for thousands of years. The element forms alloys including bronze (with copper) and pewter (with lead and other metals). Tin plating protects steel from rust in food cans and other applications. Stannum compounds are used in glass manufacturing, ceramics, and various industrial processes. The metal has a low melting point and distinctive crystal structure that produces a 'tin cry' when bent. Historical importance includes tin trade routes and the Bronze Age civilization that relied on tin-copper alloys. Modern applications include electronics, where tin-based solders connect components. Understanding stannum helps recognize both historical metallurgy and contemporary industrial chemistry applications.",
            "etymology": "From Latin 'stannum' meaning tin. The chemical symbol Sn derives from this Latin name rather than the English word 'tin.'",
            "memory_tip": "STANNUM: The scientific STANDARD name for tin metal (Sn)",
            "example_sentence": "The chemistry student learned that _____ is the Latin name for the element with symbol Sn.",
            "language_origin": "Latin",
            "source_difficulty": "Multiple Bee levels"
        },
        "stanzaic": {
            "pronunciation": "/stænˈzeɪɪk/",
            "definition": "Relating to or consisting of stanzas; organized in verse form with regular groupings of lines. Stanzaic poetry uses structural divisions that organize content into manageable units with consistent patterns. Each stanza typically contains a specific number of lines with regular rhyme schemes and meter. Stanzaic structure helps poets organize ideas, create rhythm, and provide visual breaks that aid reader comprehension. Different stanzaic forms include quatrains (four lines), tercets (three lines), and couplets (two lines). Stanzaic organization can reinforce meaning through repetition, contrast, or development of themes across sections. Free verse poetry might abandon traditional stanzaic patterns in favor of organic structures. Song lyrics often use stanzaic form with verses and choruses that repeat patterns. Understanding stanzaic construction helps readers analyze poetic structure and appreciate how form contributes to meaning and aesthetic effect.",
            "etymology": "From 'stanza' (Italian 'stanza' meaning room or stopping place) + suffix '-ic' indicating relating to or characterized by.",
            "memory_tip": "STANZAIC: Poetry that STANDS in organized groups like rooms in a house",
            "example_sentence": "The _____ structure of the poem created a pleasing rhythm with four-line verses.",
            "language_origin": "Italian, English",
            "source_difficulty": "Multiple Bee levels"
        },
        "star": {
            "pronunciation": "/stɑr/",
            "definition": "A luminous celestial body composed of hot gases; a shape with radiating points; a famous performer or athlete; to feature prominently in a performance. Stars generate light and heat through nuclear fusion reactions in their cores. Star shapes appear in flags, decorations, and symbols representing excellence or guidance. Movie stars, sports stars, and other celebrities achieve fame through exceptional talent or media attention. Star performers receive top billing and major roles in productions. The North Star has historically guided navigation through its fixed position. Star ratings indicate quality levels for hotels, restaurants, and other services. Shooting stars are meteors that burn up in Earth's atmosphere. The word suggests both astronomical phenomena and human achievement that stands out from the ordinary. Understanding stars helps recognize both cosmic scale and earthly excellence.",
            "etymology": "From Old English 'steorra,' related to German 'Stern' and Latin 'stella,' all referring to celestial bodies that shine in the night sky.",
            "memory_tip": "STAR: A bright light in the sky, or someone who SHINES above others",
            "example_sentence": "The bright _____ guided the sailors across the dark ocean waters.",
            "language_origin": "Old English",
            "source_difficulty": "Multiple Bee levels"
        },
        "starboard": {
            "pronunciation": "/ˈstɑrbərd/",
            "definition": "The right side of a ship or aircraft when facing forward; the opposite of port (left side). Starboard designation helps sailors and pilots communicate direction clearly and avoid confusion during navigation and maneuvering. Ships display green lights on the starboard side and red lights on the port side to indicate direction of travel to other vessels. Starboard terminology remains constant regardless of which way a person is facing on the vessel. Harbor pilots use starboard and port directions when guiding ships through channels and docking procedures. Aviation uses the same terminology for aircraft orientation and runway approaches. Understanding starboard helps prevent navigation errors and ensures clear communication in maritime and aviation contexts. The consistent directional reference system enables safe coordination between vessels and prevents collisions through standardized terminology that all crew members understand.",
            "etymology": "From Old English 'steorbord,' compound of 'steor' (steering paddle) + 'bord' (side), referring to the side where the steering oar was traditionally placed.",
            "memory_tip": "STARBOARD: The RIGHT side where the STEERING BOARD (rudder) used to be",
            "example_sentence": "The captain ordered the ship to turn to _____ to avoid the rocky outcrop.",
            "language_origin": "Old English",
            "source_difficulty": "Two Bee"
        },
        "stared": {
            "pronunciation": "/stɛrd/",
            "definition": "Past tense of stare; looked fixedly at something for an extended period, often with wide eyes or intense concentration. Staring involves sustained visual attention that goes beyond casual glancing or observation. People stare when surprised, confused, fascinated, or trying to understand something complex. Staring can indicate concentration, admiration, rudeness, or psychological states depending on context and cultural norms. Children often stare at new or unusual sights as part of learning and exploration. Staring contests involve maintaining eye contact longer than opponents as games or challenges. The behavior can make others uncomfortable when it violates social expectations about appropriate looking duration. Medical conditions sometimes cause excessive staring or inability to control gaze direction. Understanding staring helps recognize both normal curiosity and potentially problematic social behaviors that might require intervention or accommodation.",
            "etymology": "Past tense of 'stare,' from Old English 'starian' meaning to gaze fixedly, related to German 'starren' with similar meaning.",
            "memory_tip": "STARED: Looked so intensely that you SCARED others with your gaze",
            "example_sentence": "She _____ at the painting, trying to understand the artist's hidden message.",
            "language_origin": "Old English",
            "source_difficulty": "One Bee"
        },
        "stark": {
            "pronunciation": "/stɑrk/",
            "definition": "Severe, uncompromising, or harsh in appearance or manner; complete and absolute; desolate and barren. Stark landscapes lack vegetation, comfort, or softening features that might make them more welcoming. Stark differences are clear, dramatic, and impossible to ignore. Stark realities involve harsh truths that people might prefer to avoid but cannot escape. Stark contrasts highlight differences through dramatic juxtaposition. Stark architecture emphasizes clean lines, minimal decoration, and functional design. The word suggests both physical barrenness and emotional or intellectual severity. Stark warnings convey serious messages without softening language or pleasant alternatives. Stark choices offer limited options, usually between difficult alternatives. Understanding stark helps recognize conditions or presentations that lack comfort, compromise, or gentle alternatives in favor of direct, uncompromising truth or appearance.",
            "etymology": "From Old English 'stearc' meaning stiff, strong, or severe. Related to German 'stark' meaning strong.",
            "memory_tip": "STARK: So severe and bare it's like being STRUCK by harsh reality",
            "example_sentence": "The _____ desert landscape offered no shelter from the blazing sun.",
            "language_origin": "Old English",
            "source_difficulty": "One Bee"
        },
        "start": {
            "pronunciation": "/stɑrt/",
            "definition": "To begin an action, process, or journey; to cause something to operate or function; the beginning or initial point of something. Starting involves initiation of movement, activity, or sequence of events. People start jobs, relationships, projects, and daily routines. Engines start when ignition systems activate fuel combustion. Starting positions in races determine initial placement and strategy. Fresh starts offer opportunities to begin again after setbacks or failures. Head starts provide advantages through early beginning or preparation. The word suggests both personal agency and mechanical activation. Starting procedures ensure safe and proper initiation of complex systems. Understanding starting helps recognize the importance of beginnings in determining outcomes and the various factors that enable or prevent successful initiation of activities, relationships, and processes.",
            "etymology": "From Old English 'styrtan' meaning to leap up or move suddenly, related to 'start' meaning sudden movement or shock.",
            "memory_tip": "START: To begin moving like getting a sudden JOLT that makes you DART forward",
            "example_sentence": "They decided to _____ their journey early to avoid heavy traffic.",
            "language_origin": "Old English",
            "source_difficulty": "Multiple Bee levels"
        },
        "started": {
            "pronunciation": "/ˈstɑrtəd/",
            "definition": "Past tense of start; began an action, process, or journey; caused something to begin operating. Starting involves moving from inactive to active states or initiating new activities. People started projects when they took first steps toward completion. Machines started when operators activated controls or power systems. Historical events started with specific incidents that triggered larger developments. Educational journeys started when students enrolled in programs or began studying subjects. Business ventures started with planning, investment, and initial operations. The past tense suggests completed initiation of activities that may continue beyond the starting point. Understanding starting helps recognize the importance of first steps and initial conditions in determining later success. Starting well often requires preparation, proper timing, and clear objectives that guide subsequent actions and decisions.",
            "etymology": "Past tense of 'start,' from Old English 'styrtan.' The '-ed' suffix indicates completed action in the past.",
            "memory_tip": "STARTED: Already began something, like getting your engine STARTED and running",
            "example_sentence": "She _____ learning Spanish after her trip to Mexico inspired her.",
            "language_origin": "Old English",
            "source_difficulty": "Multiple Bee levels"
        },
        "starting": {
            "pronunciation": "/ˈstɑrtɪŋ/",
            "definition": "Present participle of start; beginning or initiating an action or process; relating to the beginning phase of something. Starting involves the ongoing process of initiation rather than completed beginning. Starting positions determine initial advantages or disadvantages in competitions. Starting salaries represent entry-level compensation that may increase with experience. Starting lineups in sports show which players begin games before substitutions occur. Starting points provide reference locations for journeys, measurements, or analyses. The continuous form emphasizes the active nature of beginning processes that require sustained effort. Starting procedures ensure proper initiation of complex systems or activities. Understanding starting helps recognize that beginnings often require time, preparation, and ongoing attention rather than simple moment of initiation. Successful starting sets foundations for later achievement and progress.",
            "etymology": "Present participle of 'start,' from Old English 'styrtan' with '-ing' suffix indicating ongoing action.",
            "memory_tip": "STARTING: The ongoing action of beginning something, like STARTING your car engine",
            "example_sentence": "The team practiced their _____ formation before the championship game.",
            "language_origin": "Old English",
            "source_difficulty": "Three Bee"
        },
        "starts": {
            "pronunciation": "/stɑrts/",
            "definition": "Third person singular present of start; begins actions or processes; sudden involuntary movements; multiple beginnings. Someone starts an activity when they initiate it. Engine starts occur when ignition systems successfully activate combustion. False starts in races happen when competitors begin before official signals. Starts and stops describe irregular patterns of activity with frequent interruptions. Jump starts provide external power to activate dead batteries. Fresh starts offer new beginning opportunities after setbacks. The plural form can indicate multiple beginning points or repeated initiation attempts. Quick starts demonstrate rapid acceleration or immediate engagement. Understanding starts helps recognize both the action of beginning and the various contexts where initiation occurs, from mechanical systems to human activities and competitive events.",
            "etymology": "Third person singular and plural forms of 'start,' from Old English 'styrtan.' Multiple meanings developed from basic sense of sudden movement.",
            "memory_tip": "STARTS: When someone or something STARTS up and gets going",
            "example_sentence": "The race _____ at exactly noon with the sound of the starting gun.",
            "language_origin": "Old English",
            "source_difficulty": "Multiple Bee levels"
        },
        "starvation": {
            "pronunciation": "/stɑrˈveɪʃən/",
            "definition": "The condition of suffering or dying from lack of food; extreme hunger that threatens life and health. Starvation occurs when caloric intake falls below minimum requirements for sustaining bodily functions and life. Prolonged starvation causes weight loss, weakness, organ damage, and eventually death if not addressed. Global starvation affects millions of people in regions affected by poverty, conflict, and natural disasters. Starvation diets involve dangerous restriction of food intake that can cause serious health problems. The condition results from inability to access sufficient nutrition rather than choice or temporary hunger. Medical starvation might occur during treatment when patients cannot consume adequate nutrition. Understanding starvation helps recognize the severity of food insecurity and the importance of nutrition assistance programs. Preventing starvation requires addressing both immediate food needs and underlying causes of food insecurity including poverty and conflict.",
            "etymology": "From 'starve' (Old English 'steorfan' meaning to die, later meaning to die of hunger) + suffix '-ation' indicating process or condition.",
            "memory_tip": "STARVATION: The serious condition when people STARVE from lack of food",
            "example_sentence": "Relief organizations work to prevent _____ in drought-affected regions.",
            "language_origin": "Old English",
            "source_difficulty": "One Bee"
        },
        "states": {
            "pronunciation": "/steɪts/",
            "definition": "Plural of state; political divisions within countries; conditions or circumstances; declares or expresses clearly. United States consists of fifty individual states with their own governments and laws. States of matter include solid, liquid, gas, and plasma phases of substances. Emotional states describe psychological conditions such as happiness, anger, or confusion. Someone states facts when they declare information clearly and definitively. Physical states involve conditions of health, readiness, or capability. Nation-states are countries with defined territories and sovereign governments. Mental states affect thinking, decision-making, and behavior patterns. The word encompasses both political divisions and general conditions across various contexts. Understanding states helps recognize both governmental structures and descriptive categories that organize information about conditions, circumstances, and declarations.",
            "etymology": "Plural of 'state,' from Latin 'status' meaning condition or position, from 'stare' (to stand). Political meaning developed from idea of established condition.",
            "memory_tip": "STATES: Different PLACES or CONDITIONS where things stand",
            "example_sentence": "The agreement was signed by representatives from all fifty _____.",
            "language_origin": "Latin",
            "source_difficulty": "Multiple Bee levels"
        },
        "static": {
            "pronunciation": "/ˈstætɪk/",
            "definition": "Lacking movement, action, or change; fixed in position; electrical discharge causing interference; criticism or resistance. Static electricity builds up through friction and can create shocks or interfere with electronic devices. Static conditions remain unchanged over time without dynamic forces creating movement or development. Radio static interferes with clear signal reception through electrical noise. Static situations lack progress or improvement despite time passing. Static displays show information that doesn't change or update automatically. Water that's static doesn't flow or circulate properly. The word suggests both physical immobility and resistance to change. Static analysis examines systems without running or testing them dynamically. Understanding static helps distinguish between active, changing conditions and fixed, unchanging states that might require intervention to create movement or progress.",
            "etymology": "From Greek 'statikos' meaning causing to stand, from 'statos' (standing), related to 'stare' (to stand).",
            "memory_tip": "STATIC: So still and unchanging it's like being STUCK in one place",
            "example_sentence": "The radio reception was poor due to _____ interference from the storm.",
            "language_origin": "Greek",
            "source_difficulty": "One Bee"
        },
        "station": {
            "pronunciation": "/ˈsteɪʃən/",
            "definition": "A place or building designated for a particular activity; a radio or television channel; someone's social position or rank; to assign to a position. Train stations serve as departure and arrival points for rail transportation. Police stations house law enforcement operations and personnel. Radio stations broadcast programming on specific frequencies. Workstations provide designated areas for specific tasks or equipment. Someone's station in life refers to their social or economic position. Military personnel are stationed at bases or locations for specific duties. Gas stations provide fuel and automotive services. The word suggests both physical locations and assigned positions or roles. Understanding stations helps recognize both infrastructure for services and organizational assignments that place people or resources in specific locations for particular purposes.",
            "etymology": "From Latin 'statio' meaning a standing place or post, from 'stare' (to stand). Military and social meanings developed from basic sense of assigned position.",
            "memory_tip": "STATION: A place where you STAY in position for a specific purpose",
            "example_sentence": "The train _____ bustled with commuters during the morning rush hour.",
            "language_origin": "Latin",
            "source_difficulty": "One Bee"
        },
        "stations": {
            "pronunciation": "/ˈsteɪʃənz/",
            "definition": "Plural of station; multiple places designated for particular activities; assigns people to positions; various broadcast channels. Television stations provide programming on different channels across broadcast areas. Gas stations offer fuel and services at multiple locations throughout regions. Work stations in offices or factories provide individual spaces for specific tasks. Radio stations broadcast different types of music, news, and entertainment. Military commanders station troops at strategic locations for defense or operations. Subway stations connect underground rail networks to surface transportation. Research stations in remote areas study weather, wildlife, or other phenomena. The plural form emphasizes multiple locations or the action of positioning people in various places. Understanding stations helps recognize both infrastructure networks and organizational deployment strategies that distribute resources and personnel effectively.",
            "etymology": "Plural of 'station,' from Latin 'statio.' Multiple meanings developed from basic concept of designated standing places.",
            "memory_tip": "STATIONS: Multiple places where people STAY positioned for different purposes",
            "example_sentence": "The radio network operated twelve _____ across the metropolitan area.",
            "language_origin": "Latin",
            "source_difficulty": "Multiple Bee levels"
        },
        "statistician": {
            "pronunciation": "/ˌstætəˈstɪʃən/",
            "definition": "A person who collects, analyzes, and interprets numerical data; an expert in statistical methods and their applications. Statisticians work in diverse fields including business, government, healthcare, sports, and research to make sense of complex data sets. They design surveys and experiments to gather reliable information and use mathematical methods to identify patterns and trends. Government statisticians collect data on population, economy, and social conditions to inform policy decisions. Business statisticians analyze market research, sales data, and customer behavior to guide strategic planning. Medical statisticians evaluate treatment effectiveness and public health trends. Sports statisticians track performance metrics and develop predictive models. The profession requires strong mathematical skills, computer proficiency, and ability to communicate findings to non-technical audiences. Modern statisticians increasingly work with big data and machine learning techniques to extract insights from massive information sources.",
            "etymology": "From 'statistic' (from German 'Statistik,' from Latin 'status' meaning state) + suffix '-ian' indicating a practitioner or expert.",
            "memory_tip": "STATISTICIAN: An expert who works with STATISTICS and numerical data",
            "example_sentence": "The _____ analyzed polling data to predict election outcomes.",
            "language_origin": "German, Latin",
            "source_difficulty": "Multiple Bee levels"
        },
        "statuesque": {
            "pronunciation": "/ˌstætʃuˈɛsk/",
            "definition": "Resembling a statue in dignity, grace, or beauty; tall and elegant in bearing; having the imposing presence of classical sculpture. Statuesque people possess impressive height, graceful posture, and dignified bearing that commands attention and respect. The term often describes models, actors, or other public figures who display classical beauty and poise. Statuesque bearing suggests both physical attractiveness and inner confidence that creates commanding presence. Classical statues inspired the adjective through their idealized proportions and noble expressions. Statuesque movement appears controlled, graceful, and purposeful rather than hurried or clumsy. The quality combines physical attributes with behavioral characteristics that suggest refinement and dignity. Fashion industry values statuesque models who can display clothing with elegance and authority. Understanding statuesque helps recognize the aesthetic and behavioral qualities that create impressive, memorable presence in both personal and professional contexts.",
            "etymology": "From 'statue' (Latin 'statua' from 'statuere' to set up) + suffix '-esque' meaning in the style or manner of.",
            "memory_tip": "STATUESQUE: Beautiful and graceful like a perfect STATUE",
            "example_sentence": "Her _____ presence made her a natural choice for the leading role.",
            "language_origin": "Latin, French",
            "source_difficulty": "Multiple Bee levels"
        },
        "statuesquestatusy": {
            "pronunciation": "/ˌstætʃuˈɛsk ˈsteɪtəsi/",
            "definition": "[COMBINED WORD ERROR] This appears to be incorrectly combined as 'statuesque statusy' - combining 'statuesque' (resembling a statue in grace and dignity) with 'statusy' (concerned with social status or prestige). Statuesque refers to physical bearing and beauty that resembles classical sculpture, emphasizing grace, dignity, and imposing presence. Statusy describes behavior or possessions focused on displaying social rank, wealth, or prestige to impress others. The combination would theoretically describe someone who combines classical beauty and grace with obvious concern for social status and prestige. However, this represents a data processing error where two distinct descriptive terms were inappropriately merged. Someone might be both statuesque in appearance and statusy in behavior, but these are separate characteristics that should not be combined into a single word.",
            "etymology": "Statuesque: Latin 'statua' + French '-esque' + Statusy: Latin 'status' + English '-y'",
            "memory_tip": "Remember: STATUESQUE (statue-like grace) + STATUSY (focused on social status)",
            "example_sentence": "She was both _____ in her elegant bearing and obvious about her wealth.",
            "language_origin": "Latin, French, English (compound error)",
            "source_difficulty": "Three Bee"
        },
        "statusy": {
            "pronunciation": "/ˈsteɪtəsi/",
            "definition": "Informal adjective describing someone or something that is concerned with or indicative of social status; focused on displaying prestige, wealth, or social position. Statusy behavior involves actions, purchases, or associations designed to signal high social rank to others. Statusy possessions include luxury items, designer brands, or exclusive experiences that demonstrate wealth and taste. The term often carries slightly negative connotations, suggesting superficial concern with appearances rather than substance. Statusy neighborhoods feature expensive homes and exclusive amenities that attract wealth-conscious residents. Statusy restaurants, clubs, or events cater to clientele who value prestige and exclusivity. Social media can encourage statusy behavior through posts designed to impress followers with lifestyle achievements. The concept reflects human tendencies toward social comparison and competition for perceived rank within communities. Understanding statusy helps recognize both marketing strategies and social dynamics that focus on prestige rather than practical value.",
            "etymology": "From 'status' (Latin 'status' meaning position or condition) + suffix '-y' indicating characterized by or full of.",
            "memory_tip": "STATUSY: Focused on showing off your high STATUS to others",
            "example_sentence": "The _____ restaurant attracted customers more interested in being seen than the food quality.",
            "language_origin": "Latin, English",
            "source_difficulty": "Multiple Bee levels"
        },
        "steady": {
            "pronunciation": "/ˈstɛdi/",
            "definition": "Firmly fixed, supported, or balanced; not changing or fluctuating; regular and consistent in behavior or performance. Steady hands enable precise work such as surgery, art, or mechanical repairs. Steady progress shows consistent advancement toward goals without dramatic ups and downs. Steady relationships demonstrate reliable commitment and consistent behavior over time. Steady income provides financial security through predictable earnings. Steady winds help sailors maintain course and speed without frequent adjustments. The word suggests reliability, consistency, and resistance to sudden changes or disruptions. Steady nerves help people remain calm during stressful or dangerous situations. Steady rhythms in music provide foundation for other instruments and vocals. Understanding steady helps recognize the value of consistency and stability in achieving long-term success and maintaining effective systems, relationships, and performance.",
            "etymology": "From Middle English 'stedi,' related to 'stead' meaning place or position, suggesting something firmly in its proper place.",
            "memory_tip": "STEADY: READY to stay firm and consistent without wobbling",
            "example_sentence": "Her _____ leadership helped the company navigate through uncertain times.",
            "language_origin": "Middle English",
            "source_difficulty": "Three Bee"
        },
        "stealthily": {
            "pronunciation": "/ˈstɛlθəli/",
            "definition": "In a stealthy manner; moving quietly and secretly to avoid detection; acting with careful concealment of one's actions or presence. Stealthy movement involves deliberate techniques to minimize noise, visibility, and other signs that might alert others to one's presence. Military operations often require stealthy approaches to achieve surprise and avoid enemy detection. Wildlife photographers move stealthily to observe and capture images of animals without disturbing natural behaviors. Burglars act stealthily to avoid detection by homeowners, neighbors, or security systems. The adverb emphasizes the careful, calculated nature of concealed movement or action. Stealthy behavior can serve legitimate purposes such as wildlife observation, military operations, or surprise celebrations. Children might move stealthily when trying to avoid bedtime or sneak treats. Understanding stealthy helps recognize both legitimate tactical applications and potentially problematic secretive behaviors that might require attention or intervention.",
            "etymology": "From 'stealth' (Middle English 'stelthe' from 'stelen' meaning to steal) + adverbial suffix '-ly.'",
            "memory_tip": "STEALTHILY: Moving so quietly and secretly like a skilled THIEF",
            "example_sentence": "The cat moved _____ through the tall grass, stalking its prey.",
            "language_origin": "Middle English",
            "source_difficulty": "One Bee"
        },
        "steampunk": {
            "pronunciation": "/ˈstimpʌŋk/",
            "definition": "A subgenre of science fiction featuring steam-powered machinery and Victorian-era aesthetics; a cultural movement inspired by 19th-century industrial steam technology. Steampunk imagines alternative histories where steam power remained the dominant technology, creating elaborate mechanical devices and retro-futuristic inventions. The aesthetic combines brass, copper, and wood materials with visible gears, pipes, and mechanical components. Steampunk fashion includes Victorian clothing modified with goggles, brass accessories, and mechanical-looking embellishments. Literature in this genre often features airships, clockwork automatons, and steam-powered vehicles in historical or alternate reality settings. Steampunk art and design emphasize craftsmanship, mechanical complexity, and industrial beauty. The movement celebrates both technological innovation and nostalgic craftsmanship that contrasts with modern digital technology. Steampunk conventions showcase costumes, art, and inventions that blend historical aesthetics with imaginative engineering. Understanding steampunk helps recognize cultural fascination with alternative technological development and handcrafted aesthetics.",
            "etymology": "Coined in 1987 by science fiction author K.W. Jeter, combining 'steam' (referring to steam power) + 'punk' (from cyberpunk genre).",
            "memory_tip": "STEAMPUNK: A style mixing old STEAM technology with PUNK creativity",
            "example_sentence": "The _____ convention featured elaborate costumes with brass goggles and mechanical gadgets.",
            "language_origin": "Modern English compound",
            "source_difficulty": "Multiple Bee levels"
        },
        "steeds": {
            "pronunciation": "/stidz/",
            "definition": "Plural of steed; horses, especially those that are spirited, strong, or used for riding; noble or war horses. Steeds traditionally refer to high-quality horses valued for their strength, speed, and noble bearing. Medieval knights rode steeds into battle, relying on their mounts for mobility and cavalry charges. Literary steeds often possess almost supernatural qualities, serving heroes in epic adventures and quests. The term suggests horses of superior breeding, training, and capability compared to ordinary work animals. Racing steeds demonstrate speed and competitive spirit on tracks and in equestrian sports. Mythological steeds include winged horses, unicorns, and other magical creatures that serve legendary figures. Modern usage might refer to motorcycles or other vehicles metaphorically as mechanical steeds. Understanding steeds helps recognize the historical importance of horses in warfare, transportation, and cultural imagination as symbols of power, freedom, and nobility.",
            "etymology": "Plural of 'steed,' from Old English 'stēda' meaning stallion or war horse, related to 'stōd' (herd of horses).",
            "memory_tip": "STEEDS: Strong horses that can SPEED across battlefields",
            "example_sentence": "The cavalry's _____ thundered across the battlefield in a magnificent charge.",
            "language_origin": "Old English",
            "source_difficulty": "Three Bee"
        },
        "steel": {
            "pronunciation": "/stil/",
            "definition": "A strong metal alloy composed primarily of iron and carbon; to strengthen or harden oneself mentally or emotionally for a difficult task. Steel production involves refining iron ore and adding controlled amounts of carbon to create material stronger than pure iron. Various steel grades serve different purposes, from construction beams to precision instruments and tools. Stainless steel resists corrosion through chromium content, making it valuable for kitchen equipment and medical instruments. The verb 'steel oneself' means to prepare mentally for challenging or unpleasant experiences. Steel industries form the backbone of construction, automotive, and manufacturing sectors. Damascus steel was historically prized for its strength and distinctive patterns. Steel wool consists of fine metal fibers used for cleaning and polishing. Understanding steel helps recognize both material science principles and metaphorical applications describing mental strength and determination needed to face difficulties.",
            "etymology": "From Old English 'stēl,' related to German 'Stahl,' from Proto-Germanic root meaning to make firm or strengthen.",
            "memory_tip": "STEEL: A metal so strong it helps you STEEL yourself for tough challenges",
            "example_sentence": "The skyscraper's _____ frame could withstand hurricane-force winds.",
            "language_origin": "Old English",
            "source_difficulty": "Three Bee"
        },
        "steenkirk": {
            "pronunciation": "/ˈstinkɜrk/",
            "definition": "A type of loosely tied neckcloth or cravat worn in the late 17th and early 18th centuries; named after the Battle of Steenkerque in 1692. The steenkirk became fashionable after French officers, caught off-guard in battle, hastily tied their cravats without proper arrangement. This casual, slightly disheveled style was then adopted by fashionable society as an elegant alternative to formal neckwear. Steenkirks were typically made of fine lace or linen and worn by both men and women. The style represented a departure from rigid formal dress toward more relaxed elegance. Fashion historians study steenkirks as examples of how military events influenced civilian clothing trends. The accessory demonstrates how battlefield practicality could become aristocratic fashion. Understanding steenkirks helps recognize how historical events, even military defeats, could influence fashion and social customs across different social classes and time periods.",
            "etymology": "Named after the Battle of Steenkerque (1692), where French officers hastily tied their cravats, creating a new fashion style.",
            "memory_tip": "STEENKIRK: A loosely tied neckcloth named after a battle where soldiers were KEEN to tie their neckerchiefs quickly",
            "example_sentence": "The gentleman wore a lace _____ tied in the fashionable loose style of the period.",
            "language_origin": "French (place name)",
            "source_difficulty": "Multiple Bee levels"
        },
        "steeped": {
            "pronunciation": "/stipt/",
            "definition": "Past tense of steep; soaked or saturated in liquid; deeply immersed or saturated with knowledge, tradition, or influence. Tea leaves are steeped in hot water to extract flavor, color, and beneficial compounds. Someone steeped in tradition has been deeply influenced by cultural practices and historical knowledge. Steeped grains in brewing release sugars and flavors essential for beer production. The process requires proper temperature, timing, and liquid ratios to achieve desired results. People can be steeped in academic subjects, artistic traditions, or professional expertise through years of study and practice. Steeped herbs create medicinal teas and therapeutic preparations. The word suggests both literal soaking processes and metaphorical immersion in knowledge or culture. Understanding steeping helps recognize both cooking techniques and educational processes that require sustained exposure and absorption over time.",
            "etymology": "Past tense of 'steep,' from Old English 'stēap' meaning high or deep, later meaning to soak in liquid.",
            "memory_tip": "STEEPED: Soaked so deeply it's like taking a DEEP dive into liquid or knowledge",
            "example_sentence": "The tea leaves were _____ in boiling water for exactly five minutes.",
            "language_origin": "Old English",
            "source_difficulty": "Three Bee"
        },
        "steeplechasing": {
            "pronunciation": "/ˈstipəlˌtʃeɪsɪŋ/",
            "definition": "A horse racing sport where horses and riders navigate a course with obstacles including fences, ditches, and water jumps; also a track and field event with hurdles and water obstacles. Steeplechasing originated from cross-country races between church steeples, with riders choosing their own routes across natural terrain. Modern steeplechasing uses purpose-built courses with standardized obstacles designed to test horse and rider skills. The Grand National at Aintree is the world's most famous steeplechase, featuring challenging fences and long distance. Track steeplechasing involves runners navigating hurdles and water jumps over 3000-meter distances. Steeplechasing requires specialized training for both horses and athletes to safely navigate obstacles at speed. The sport emphasizes endurance, jumping ability, and tactical racing decisions. Understanding steeplechasing helps recognize both equestrian sport traditions and athletic events that combine running with obstacle navigation requiring specialized skills and conditioning.",
            "etymology": "From 'steeplechase' (racing from steeple to steeple across country) + present participle suffix '-ing.'",
            "memory_tip": "STEEPLECHASING: Racing across country toward church STEEPLES while CHASING over obstacles",
            "example_sentence": "The jockey specialized in _____ and had won several major cross-country races.",
            "language_origin": "English",
            "source_difficulty": "One Bee"
        },
        "steeve": {
            "pronunciation": "/stiv/",
            "definition": "To stow cargo in a ship's hold by arranging it compactly and securely; a derrick or spar used for loading cargo. Steeving involves careful placement of goods to maximize space utilization while ensuring safe transport during rough seas. Proper steeving prevents cargo from shifting, which could damage goods or affect ship stability. The technique requires understanding weight distribution, container shapes, and securing methods. Steeves (derricks) help lift heavy cargo from docks into ship holds efficiently. Historical sailing ships required expert steeving to balance load and maintain proper trim for sailing performance. Modern container ships use standardized systems that simplify steeving procedures. The process combines practical physics with seamanship knowledge to ensure safe maritime transport. Understanding steeving helps recognize the complexity of maritime cargo operations and the specialized knowledge required for efficient and safe shipping operations.",
            "etymology": "From Spanish 'estivar' meaning to stow or pack, from Latin 'stipare' meaning to press together or pack tightly.",
            "memory_tip": "STEEVE: To pack cargo so tight you LEAVE no wasted space in the ship",
            "example_sentence": "The experienced dock workers knew how to _____ the cargo for maximum efficiency.",
            "language_origin": "Spanish, Latin",
            "source_difficulty": "Three Bee"
        },
        "stegosaur": {
            "pronunciation": "/ˈstɛɡəˌsɔr/",
            "definition": "A large herbivorous dinosaur of the late Jurassic period, characterized by a double row of bony plates along its back and spikes on its tail. Stegosaurus measured up to 30 feet long and weighed several tons, using its distinctive plates for temperature regulation and possibly display. The tail spikes, called thagomizers, served as defensive weapons against predators like Allosaurus. Stegosaurs had small heads relative to body size, with beaked mouths adapted for eating low-growing plants. Fossil evidence shows these dinosaurs lived in herds and inhabited river plains and forests. The distinctive plates made stegosaurs among the most recognizable dinosaurs in popular culture. Multiple stegosaur species existed across different continents during the Mesozoic era. Scientific study of stegosaur fossils contributes to understanding dinosaur evolution, behavior, and extinction. The discovery of stegosaur remains helps paleontologists reconstruct ancient ecosystems and climate conditions.",
            "etymology": "From Greek 'stegos' (roof) + 'sauros' (lizard), referring to the bony plates that resembled roof tiles along the back.",
            "memory_tip": "STEGOSAUR: A dinosaur with bony plates like STEPS along its back",
            "example_sentence": "The museum's _____ skeleton displayed the characteristic double row of defensive plates.",
            "language_origin": "Greek",
            "source_difficulty": "Multiple Bee levels"
        },
        "steinkirk": {
            "pronunciation": "/ˈstaɪnkɜrk/",
            "definition": "An alternative spelling of steenkirk; a loosely tied neckcloth or cravat fashionable in the late 17th and early 18th centuries. The steinkirk represented a departure from formal, precisely arranged neckwear toward more casual elegance. This fashion originated from the Battle of Steenkerque where French officers, surprised by enemy attack, hastily tied their cravats without proper arrangement. The disheveled but elegant style became popular among European aristocracy and fashionable society. Steinkirks were typically made from fine materials including lace, silk, or linen. Both men and women adopted this style as an alternative to rigid formal dress codes. The accessory demonstrates how military events could influence civilian fashion trends. Fashion historians study steinkirks as examples of how practical necessities could become aesthetic choices. Understanding steinkirks helps recognize the complex relationships between military history, social customs, and fashion evolution.",
            "etymology": "Alternative spelling of 'steenkirk,' named after the Battle of Steenkerque (1692). German spelling variant of the French place name.",
            "memory_tip": "STEINKIRK: Alternative spelling of the loose neckcloth named after a battle",
            "example_sentence": "The portrait showed the nobleman wearing a silk _____ in the fashionable loose style.",
            "language_origin": "German variant of French place name",
            "source_difficulty": "Multiple Bee levels"
        },
        "stellular": {
            "pronunciation": "/ˈstɛljələr/",
            "definition": "Having the shape or form of a small star; relating to or resembling little stars; arranged in a star-like pattern. Stellular formations appear in crystalline structures, biological tissues, and architectural designs where elements radiate from central points. Stellular cells in anatomy have star-shaped morphology with projections extending in multiple directions. Stellular patterns in nature include certain flower arrangements, coral formations, and mineral crystal structures. The term describes organizational patterns that resemble stars through radial symmetry and central focus points. Stellular designs in art and architecture create visual interest through repeated star-like motifs. Scientific classification uses stellular to describe microscopic structures that display characteristic star-shaped arrangements. Understanding stellular helps recognize both natural patterns and designed elements that utilize star-like organization for functional or aesthetic purposes. The concept emphasizes radial symmetry and central organization principles found across multiple scientific and artistic disciplines.",
            "etymology": "From Latin 'stellula,' diminutive of 'stella' (star) + suffix '-ar' meaning relating to or resembling.",
            "memory_tip": "STELLULAR: Shaped like little STELLAR stars arranged in patterns",
            "example_sentence": "The microscope revealed _____ cells with star-shaped projections throughout the tissue.",
            "language_origin": "Latin",
            "source_difficulty": "Multiple Bee levels"
        },
        "stench": {
            "pronunciation": "/stɛntʃ/",
            "definition": "A strong and very unpleasant smell; an offensive odor that is difficult to tolerate. Stenches typically arise from decomposition, sewage, chemical reactions, or other sources of putrid or toxic materials. The word suggests odors that are not just unpleasant but actively repulsive and potentially harmful. Stenches can indicate dangerous conditions such as gas leaks, chemical contamination, or unsanitary environments. Some stenches serve as natural warning systems, alerting people to avoid potentially harmful substances or areas. Industrial stenches might result from manufacturing processes involving sulfur, ammonia, or other strong-smelling chemicals. Animal stenches can indicate illness, improper sanitation, or overcrowding in agricultural settings. The intensity of stenches often makes them impossible to ignore and drives people to seek relief or address underlying causes. Understanding stenches helps recognize both health hazards and environmental problems that require immediate attention and remediation.",
            "etymology": "From Old English 'stenc' meaning smell or odor, related to 'stincan' (to emit a smell). Germanic origin with cognates in other languages.",
            "memory_tip": "STENCH: A smell so bad it makes you want to CLENCH your nose shut",
            "example_sentence": "The _____ from the garbage dump was unbearable on hot summer days.",
            "language_origin": "Old English",
            "source_difficulty": "One Bee"
        },
        "stencil": {
            "pronunciation": "/ˈstɛnsəl/",
            "definition": "A thin sheet with a cut-out design used to apply paint, ink, or other materials in a specific pattern; to mark or paint using such a template. Stencils enable precise reproduction of letters, numbers, shapes, or decorative patterns across multiple surfaces. Artists use stencils for screen printing, wall murals, and repeated design elements. Military stencils mark equipment, vehicles, and supplies with identification numbers and symbols. Stenciling requires careful alignment and technique to prevent paint bleeding under edges. Home decorators use stencils for wall borders, furniture accents, and craft projects. Industrial stencils mark shipping containers, products, and safety information. The technique allows people with limited artistic skills to create professional-looking designs. Understanding stencils helps recognize both artistic techniques and practical marking systems that ensure consistency, efficiency, and clear communication across various applications from art to industry.",
            "etymology": "From Middle English 'stanselen,' from Old French 'estenceler' meaning to cover with stars or sparkles, from 'estencele' (spark).",
            "memory_tip": "STENCIL: A template that helps you make IDENTICAL patterns like a pencil guide",
            "example_sentence": "She used a flower _____ to decorate the nursery walls with repeated patterns.",
            "language_origin": "Old French",
            "source_difficulty": "Multiple Bee levels"
        },
        "stenographer": {
            "pronunciation": "/stəˈnɑɡrəfər/",
            "definition": "A person skilled in stenography; someone who takes dictation and transcribes spoken words using shorthand or specialized equipment. Stenographers work in legal settings, recording court proceedings, depositions, and legal meetings with high accuracy requirements. Business stenographers assist executives by taking dictation for correspondence, reports, and meeting minutes. Court stenographers use specialized machines that can capture speech at rates exceeding 200 words per minute. Medical stenographers transcribe physician dictation for patient records and medical reports. The profession requires excellent listening skills, typing proficiency, and knowledge of specialized terminology. Modern stenographers often use digital recording equipment and computer-assisted transcription software. Historical stenographers used shorthand writing systems that compressed spoken words into rapid written symbols. Understanding stenography helps recognize both traditional office skills and contemporary legal support services that ensure accurate record-keeping in professional settings.",
            "etymology": "From 'stenography' (Greek 'stenos' meaning narrow + 'graphein' meaning to write) + suffix '-er' indicating a person who performs an action.",
            "memory_tip": "STENOGRAPHER: Someone who writes STENO shorthand to capture speech rapidly",
            "example_sentence": "The court _____ accurately recorded every word of the witness testimony.",
            "language_origin": "Greek",
            "source_difficulty": "Multiple Bee levels"
        },
        "stentorian": {
            "pronunciation": "/stɛnˈtɔriən/",
            "definition": "Very loud and powerful; having an extremely strong voice; characterized by great volume and resonance. Stentorian voices can be heard clearly across large distances and crowded spaces without amplification. Public speakers with stentorian delivery command attention and project authority through vocal power. Opera singers often possess stentorian voices capable of filling large theaters without microphones. Military commanders traditionally needed stentorian voices to communicate orders across battlefields. The term suggests not just loudness but also clarity and carrying power that makes speech intelligible at distance. Stentorian announcers at sporting events can energize crowds and communicate information effectively. Some people naturally possess stentorian voices while others develop them through training and practice. Understanding stentorian helps recognize the value of vocal projection in leadership, performance, and communication roles that require reaching large audiences without electronic assistance.",
            "etymology": "From Stentor, a herald in Homer's Iliad whose voice was as loud as fifty men shouting together. Greek mythology reference.",
            "memory_tip": "STENTORIAN: A voice so loud it's like a STENTOR horn announcing important news",
            "example_sentence": "The coach's _____ voice could be heard across the entire football field.",
            "language_origin": "Greek (mythological)",
            "source_difficulty": "Three Bee"
        },
        "step": {
            "pronunciation": "/stɛp/",
            "definition": "To lift one foot and put it down in a different place; a single movement in walking; one of a series of actions toward achieving a goal; a flat surface for placing the foot. Steps involve coordinated movement that enables human locomotion and navigation across various terrains. Dance steps follow specific patterns and rhythms that create artistic expression. Procedural steps break complex tasks into manageable components that ensure systematic completion. Stair steps provide safe vertical circulation in buildings and structures. First steps mark important beginnings in development, relationships, or projects. Step-by-step instructions guide users through processes with clear sequential actions. The word suggests both physical movement and progressive advancement toward objectives. Understanding steps helps recognize both biomechanical processes and organizational strategies that facilitate movement and achievement through systematic progression.",
            "etymology": "From Old English 'steppan' meaning to move by lifting the foot, related to German 'stapfen' and Dutch 'stappen.'",
            "memory_tip": "STEP: To move forward by lifting your foot and taking the next STEP",
            "example_sentence": "She took a careful _____ onto the icy sidewalk.",
            "language_origin": "Old English",
            "source_difficulty": "Multiple Bee levels"
        },
        "steppe": {
            "pronunciation": "/stɛp/",
            "definition": "A large area of flat unforested grassland in southeastern Europe or Siberia; temperate grassland characterized by low rainfall and extreme temperature variations. Steppes support nomadic herding cultures that move livestock seasonally across vast grazing areas. The ecosystem features drought-resistant grasses and few trees due to limited precipitation and harsh winters. Eurasian steppes have historically served as corridors for trade, migration, and cultural exchange between East and West. Steppe climates experience hot summers and cold winters with precipitation insufficient to support forests. Wildlife includes grazing animals like horses, sheep, and various rodent species adapted to grassland environments. Agricultural development has converted many steppes to cropland for grain production. The Great Steppe of Central Asia remains one of the world's largest continuous grassland systems. Understanding steppes helps recognize both ecological principles and cultural adaptations to semi-arid grassland environments that shaped human history and continue affecting global climate patterns.",
            "etymology": "From Russian 'step' meaning lowland or plain, borrowed into English through German 'Steppe.'",
            "memory_tip": "STEPPE: A vast grassy plain where you can take giant STEPS across endless grassland",
            "example_sentence": "The Mongolian _____ stretched endlessly to the horizon under the vast sky.",
            "language_origin": "Russian",
            "source_difficulty": "Multiple Bee levels"
        },
        "stereotypical": {
            "pronunciation": "/ˌstɛriəˈtɪpɪkəl/",
            "definition": "Relating to or characterized by stereotypes; conforming to a widely held but oversimplified image or idea about a particular group or thing. Stereotypical thinking reduces complex individuals and situations to simplistic categories that ignore diversity and nuance. Stereotypical representations in media can perpetuate harmful misconceptions about different groups of people. The adjective describes behaviors, appearances, or characteristics that match common assumptions rather than individual reality. Stereotypical gender roles limit people's choices and potential by imposing narrow expectations about appropriate behavior. Educational efforts work to reduce stereotypical thinking through exposure to diverse perspectives and experiences. Stereotypical assumptions can lead to discrimination and missed opportunities for understanding and connection. Breaking away from stereotypical patterns requires conscious effort to see individuals as complex, unique people rather than representatives of groups. Understanding stereotypical helps recognize both harmful oversimplification and the importance of individual identity beyond group membership.",
            "etymology": "From 'stereotype' (Greek 'stereos' meaning solid + 'typos' meaning impression) + suffix '-ical' meaning relating to.",
            "memory_tip": "STEREOTYPICAL: Following TYPICAL patterns that create STEREO-like repeated assumptions",
            "example_sentence": "The movie avoided _____ character portrayals by showing complex, realistic personalities.",
            "language_origin": "Greek",
            "source_difficulty": "Multiple Bee levels"
        },
        "sterling": {
            "pronunciation": "/ˈstɜrlɪŋ/",
            "definition": "Excellent; of the highest quality; relating to British currency; silver that is 92.5% pure. Sterling silver contains the precise alloy ratio that provides durability while maintaining the metal's desirable properties for jewelry and decorative items. Sterling character describes people of exceptional integrity, reliability, and moral quality. British pound sterling represents the official currency of the United Kingdom and several other territories. Sterling reputation indicates consistent excellence and trustworthiness over time. Sterling work or performance exceeds normal standards and demonstrates exceptional quality. The hallmark system certifies sterling silver to ensure consumers receive genuine quality products. Sterling qualities in people include honesty, dependability, and consistent ethical behavior. Understanding sterling helps recognize both material standards for precious metals and character standards for human behavior that represent the highest levels of quality and integrity.",
            "etymology": "Possibly from Old English 'steorling' meaning little star, referring to small stars on early Norman pennies, or from 'Easterling' (traders from eastern Germany).",
            "memory_tip": "STERLING: Quality so excellent it's like pure SILVER - the highest standard",
            "example_sentence": "Her _____ reputation for honesty made her the perfect choice for treasurer.",
            "language_origin": "Old English (uncertain)",
            "source_difficulty": "Multiple Bee levels"
        },
        "sternum": {
            "pronunciation": "/ˈstɜrnəm/",
            "definition": "The breastbone; a long flat bone located in the center of the chest that connects to the ribs and protects vital organs. The sternum consists of three parts: the manubrium (top), body (middle), and xiphoid process (bottom). This bone serves as attachment point for ribs, forming the front part of the rib cage that protects the heart and lungs. The sternum provides structural support for the chest wall and assists in breathing mechanics. Medical procedures sometimes require accessing organs through the sternum, particularly in cardiac surgery. CPR training emphasizes proper hand placement on the lower sternum to provide effective chest compressions. Sternal fractures can occur in severe chest trauma and require careful medical attention. The sternum's location makes it a reference point for medical examinations and procedures. Understanding the sternum helps recognize both anatomical structure and medical procedures that affect chest cavity protection and function.",
            "etymology": "From Latin 'sternum,' from Greek 'sternon' meaning chest or breastbone. Medical terminology adopted from classical languages.",
            "memory_tip": "STERNUM: The STERN bone in your chest that protects your heart",
            "example_sentence": "The paramedic placed her hands on the patient's _____ to perform CPR.",
            "language_origin": "Greek, Latin",
            "source_difficulty": "Multiple Bee levels"
        }
    }
    
    # Combined word errors in this batch that need special handling
    combined_word_errors = [
        "statuesquestatusy"
    ]
    
    # Read input file
    print("Processing 50 words from batch 168...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        words = list(reader)
    
    # Prepare output data
    output_data = []
    combined_errors_found = []
    
    calc = DifficultyCalculator()
    
    for i, row in enumerate(words, 1):
        word = row['word'].strip()
        print(f"Processing word {i}: {word}")
        
        # Check if this is a combined word error
        is_combined_error = word in combined_word_errors
        if is_combined_error:
            combined_errors_found.append(word)
        
        # Get comprehensive word data
        if word in word_data:
            data = word_data[word]
            
            # Calculate difficulty factors
            phonetic_transparency = calc.calculate_phonetic_transparency(word, data['pronunciation'])
            frequency_score = calc.calculate_frequency_score(word)
            morphological_complexity = calc.calculate_morphological_complexity(word)
            etymology_complexity = calc.calculate_etymology_complexity(data['etymology'], data['language_origin'])
            
            output_row = {
                'word': word,
                'pronunciation': data['pronunciation'],
                'definition': data['definition'],
                'etymology': data['etymology'],
                'memory_tip': data['memory_tip'],
                'example_sentence': data['example_sentence'],
                'language_origin': data['language_origin'],
                'phonetic_transparency': phonetic_transparency,
                'frequency_score': frequency_score,
                'morphological_complexity': morphological_complexity,
                'etymology_complexity': etymology_complexity,
                'source_difficulty': data['source_difficulty'],
                'years': row['years'],
                'source_files': row['source_files'],
                'source_difficulties': row['source_difficulties'],
                'difficulty_level': '',  # Will be assigned later
                'is_combined_error': is_combined_error
            }
            
            output_data.append(output_row)
    
    # Write output file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'word', 'pronunciation', 'definition', 'etymology', 'memory_tip', 
            'example_sentence', 'language_origin', 'phonetic_transparency', 
            'frequency_score', 'morphological_complexity', 'etymology_complexity',
            'source_difficulty', 'years', 'source_files', 'source_difficulties',
            'difficulty_level', 'is_combined_error'
        ]
        
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_data)
    
    print(f"\nBatch 168 processing complete!")
    print(f"Successfully processed {len(output_data)}/50 words")
    print(f"Output saved to: {output_file}")
    print(f"\nCombined word errors detected: {len(combined_errors_found)}")
    for error in combined_errors_found:
        print(f"  - {error}")

if __name__ == "__main__":
    main()