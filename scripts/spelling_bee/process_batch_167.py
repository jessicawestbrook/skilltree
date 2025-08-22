#!/usr/bin/env python3
"""
Process batch 167 of spelling bee words.
Reads from batch_167_words.csv and generates comprehensive word data.
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
    input_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_167_words.csv"
    output_file = r"C:\Users\jessi\Projects\skilltree2\scripts\spelling_bee\output\batch_167_processed.csv"
    
    # Comprehensive word data with educational content
    word_data = {
        "spot": {
            "pronunciation": "/spɑt/",
            "definition": "A small, round mark or stain differing in color or texture from the surface around it; a particular place or location; to notice or identify something. Spots can be natural markings like animal patterns, freckles on skin, or spots on playing cards. Physical spots might result from spills, dirt, or deliberate marking for identification purposes. Geographic spots refer to specific locations or points of interest. The verb 'to spot' means to notice or identify something, especially something small or partially hidden. Wildlife spotting involves identifying animals in their natural habitats. Spot checks are unscheduled inspections or examinations designed to ensure compliance or quality. Trouble spots identify areas of difficulty or concern requiring attention. Spot treatments address specific problems rather than broad applications. The word's versatility reflects its use across physical, geographic, and metaphorical contexts.",
            "etymology": "From Middle English 'spot,' possibly from Old Norse 'spotti' or related to Middle Dutch 'spotte' meaning speck or blot.",
            "memory_tip": "SPOT: A small mark you can easily SPOT or see",
            "example_sentence": "She found a small ink _____ on her white shirt after the meeting.",
            "language_origin": "Middle English, Old Norse",
            "source_difficulty": "Multiple Bee levels"
        },
        "spotted": {
            "pronunciation": "/ˈspɑtəd/",
            "definition": "Having spots; marked with spots or patches of different colors; noticed or identified. Spotted animals include leopards, dalmatians, and many species of birds and fish that use spots for camouflage or identification. Spotted patterns serve various functions in nature including warning signals, mating displays, and predator confusion. The verb form means to have noticed or identified something, as in 'spotted the error in the document.' Spotted reputations refer to people with checkered or questionable histories marked by both good and bad behavior. Spotted fever describes diseases characterized by spotted rashes on the skin. Spotted patterns in textiles and design create visual interest through contrasting colors and irregular arrangements. The term suggests both physical marking and the act of observation or recognition across different contexts.",
            "etymology": "Past tense and past participle of 'spot,' from Middle English 'spot' with '-ed' suffix indicating completed action or state.",
            "memory_tip": "SPOTTED: Something that has been SPOTTED with marks or that you have SPOTTED with your eyes",
            "example_sentence": "The _____ owl blended perfectly with the tree bark patterns.",
            "language_origin": "Middle English",
            "source_difficulty": "Three Bee"
        },
        "sprawl": {
            "pronunciation": "/sprɔl/",
            "definition": "To sit, lie, or fall with arms and legs spread out in an ungainly way; to spread out over a large area in an irregular or disorderly fashion. Urban sprawl describes the uncontrolled expansion of cities into surrounding areas, often creating low-density development that requires cars for transportation. People sprawl on furniture when relaxing in comfortable, unstructured positions. Plants sprawl when they grow in spreading patterns rather than upright forms. Suburban sprawl can lead to environmental problems, traffic congestion, and loss of farmland. The verb suggests lack of order or control, whether describing physical positions or geographic expansion. Sprawling cities consume more resources and create longer commutes than compact development. Sprawling handwriting appears loose and uncontrolled across the page. The concept often implies both relaxation and lack of efficiency or organization.",
            "etymology": "From Old English 'spreawlian' meaning to move convulsively, related to 'sprawl' meaning to stretch out. Connected to 'spread' and similar extending words.",
            "memory_tip": "SPRAWL: To SPREAD yourself out in a relaxed, disorganized way",
            "example_sentence": "After the long hike, he chose to _____ on the grass and rest.",
            "language_origin": "Old English",
            "source_difficulty": "One Bee"
        },
        "spread": {
            "pronunciation": "/sprɛd/",
            "definition": "To extend over a wider area; to distribute or apply something over a surface; the extent or range of something. Spreading involves expansion from a central point or distribution across available space. People spread butter on bread, spread news through communication, or spread their arms wide. Disease spread occurs when infections move from person to person or place to place. Spread can refer to the difference between two values, such as the spread between bid and ask prices in financial markets. Food spreads are substances like jam, peanut butter, or cream cheese applied to bread or crackers. Wings spread when birds prepare for flight or display territorial behavior. The word suggests both physical expansion and metaphorical distribution of ideas, influence, or effects across broader areas or populations.",
            "etymology": "From Old English 'sprǣdan' meaning to stretch out or extend. Related to German 'spreiten' and Dutch 'spreiden' with similar meanings.",
            "memory_tip": "SPREAD: To stretch and extend something out over a wider area",
            "example_sentence": "The wildfire began to _____ rapidly across the dry grassland.",
            "language_origin": "Old English",
            "source_difficulty": "Three Bee"
        },
        "spreading": {
            "pronunciation": "/ˈsprɛdɪŋ/",
            "definition": "Present participle of spread; the action of extending, distributing, or expanding something over a wider area or among more people. Spreading involves ongoing processes of expansion or distribution across space or populations. Disease spreading concerns public health officials who work to contain outbreaks and prevent epidemics. Information spreading occurs through social networks, media, and word-of-mouth communication. Spreading rumors can damage reputations and relationships if the information proves false. Fire spreading requires immediate response from firefighters to prevent property damage and protect lives. Spreading costs refers to distributing expenses over time or among multiple parties. Spreading resources means allocating limited materials or personnel across various needs. The continuous form emphasizes the active, ongoing nature of expansion or distribution processes that require monitoring and potentially intervention to control or direct effectively.",
            "etymology": "Present participle form of 'spread,' from Old English 'sprǣdan' with '-ing' suffix indicating ongoing action.",
            "memory_tip": "SPREADING: The ongoing action of something SPREADING out wider and wider",
            "example_sentence": "The news was _____ quickly through social media channels.",
            "language_origin": "Old English",
            "source_difficulty": "Three Bee"
        },
        "spreadsheet": {
            "pronunciation": "/ˈsprɛdˌʃit/",
            "definition": "A computer program or document that organizes data in rows and columns, allowing calculations, analysis, and data manipulation. Spreadsheets revolutionized business and personal data management by providing structured ways to organize, calculate, and visualize numerical information. Popular spreadsheet programs include Microsoft Excel, Google Sheets, and Apple Numbers. Users can create formulas that automatically calculate totals, averages, and complex mathematical operations. Spreadsheets support budgeting, financial planning, inventory tracking, project management, and data analysis across virtually every industry. Features include sorting, filtering, charting, and pivot tables that help users understand patterns in their data. Before computers, spreadsheets were large paper documents with rows and columns filled in by hand. Modern spreadsheets can link to databases, import real-time data, and share information across teams for collaborative analysis and decision-making.",
            "etymology": "Compound of 'spread' (extending across space) + 'sheet' (flat surface), originally referring to large paper accounting documents.",
            "memory_tip": "SPREADSHEET: A SHEET where data is SPREAD out in rows and columns",
            "example_sentence": "She used a _____ to track expenses and create the monthly budget report.",
            "language_origin": "English compound",
            "source_difficulty": "Multiple Bee levels"
        },
        "sprechstimme": {
            "pronunciation": "/ˈʃprɛxˌʃtɪmə/",
            "definition": "A vocal technique that combines speaking and singing, where the performer uses approximate pitches rather than exact musical notes; literally meaning 'speech-voice' in German. Sprechstimme was developed by Austrian composer Arnold Schoenberg in the early 20th century as part of his twelve-tone compositional technique. The technique requires performers to begin each note with the indicated pitch but immediately slide away rather than sustaining the exact tone. This creates an eerie, unsettling vocal quality that suggests both speech and song without being purely either. Schoenberg's 'Pierrot Lunaire' represents the most famous use of sprechstimme, creating dramatic, expressionistic effects that match the work's dark, psychological content. The technique influenced other composers and performers in classical, theatrical, and experimental music contexts. Modern performers still study sprechstimme for its unique expressive capabilities and historical importance in 20th-century music development.",
            "etymology": "German compound: 'sprechen' (to speak) + 'Stimme' (voice). Created by Arnold Schoenberg for his compositional technique around 1912.",
            "memory_tip": "SPRECHSTIMME: SPEECH + voice technique combining speaking and singing",
            "example_sentence": "The vocalist mastered _____ to perform Schoenberg's challenging contemporary piece.",
            "language_origin": "German",
            "source_difficulty": "Multiple Bee levels"
        },
        "spree": {
            "pronunciation": "/spri/",
            "definition": "A period of unrestrained activity or indulgence; an episode of excessive behavior, often involving spending, drinking, or other pleasurable activities. Shopping sprees involve buying many items in a short period, often beyond normal budgets or needs. Drinking sprees describe periods of excessive alcohol consumption that can lead to health and social problems. Crime sprees involve multiple criminal acts committed in succession by the same person or group. Spending sprees can result in financial difficulties if people purchase items impulsively without considering long-term consequences. Creative sprees might involve intense periods of artistic production where inspiration flows freely. The word suggests temporary abandonment of usual restraints or limitations in favor of immediate gratification or expression. While sprees can be enjoyable, they often require subsequent periods of restraint or recovery to restore balance and address any negative consequences of the excessive behavior.",
            "etymology": "Origin uncertain, possibly from Scots 'spreath' meaning cattle raid, or from 'spray' suggesting scattered, uncontrolled action.",
            "memory_tip": "SPREE: A period where you go FREE with spending or indulging",
            "example_sentence": "Her shopping _____ at the mall resulted in bags full of new clothes.",
            "language_origin": "Uncertain (possibly Scots)",
            "source_difficulty": "Three Bee"
        },
        "sprightliness": {
            "pronunciation": "/ˈspraɪtlinəs/",
            "definition": "The quality of being sprightly; liveliness, vivacity, and energetic cheerfulness; the state of being active and spirited despite advanced age or circumstances. Sprightliness suggests youthful energy and enthusiasm that defies expectations based on age or situation. Elderly people who maintain sprightliness inspire others through their continued vitality and positive outlook. Mental sprightliness involves quick wit, sharp thinking, and intellectual agility that keeps minds active and engaged. Physical sprightliness includes graceful movement, good coordination, and maintained strength that supports active lifestyles. The quality implies both physical and mental vitality that contributes to overall well-being and quality of life. Sprightliness can be cultivated through regular exercise, social engagement, intellectual challenges, and positive attitudes toward aging and change. The term suggests that energy and enthusiasm are choices that can be maintained regardless of external circumstances or chronological age.",
            "etymology": "From 'sprightly' (variant of 'spritelike,' meaning lively like a sprite) + suffix '-ness' indicating quality or state.",
            "memory_tip": "SPRIGHTLINESS: The quality of being SPRIGHTLY and full of lively energy",
            "example_sentence": "Despite her age, her _____ made her the life of every social gathering.",
            "language_origin": "English",
            "source_difficulty": "Multiple Bee levels"
        },
        "spring": {
            "pronunciation": "/sprɪŋ/",
            "definition": "The season between winter and summer when plants begin to grow; to move suddenly or rapidly; a natural source of water; a coiled elastic device. Spring season brings warmer weather, longer daylight, and renewal of plant growth after winter dormancy. Animals spring into action when startled or hunting prey. Natural springs provide fresh water from underground sources that emerge at the surface. Mechanical springs store and release energy in devices from watches to automobile suspensions. The verb 'spring' suggests sudden, energetic movement or unexpected appearance. Spring cleaning traditionally involves thorough household maintenance as winter ends. Springs in mechanisms provide force, support weight, or return components to original positions. The word connects concepts of renewal, sudden movement, water sources, and mechanical devices through shared ideas of emergence, energy, and natural cycles.",
            "etymology": "From Old English 'spring' meaning to leap or burst forth, related to German 'springen.' All meanings derive from the basic sense of sudden emergence.",
            "memory_tip": "SPRING: Things SPRING up suddenly, like plants in spring or jumping movements",
            "example_sentence": "The natural _____ provided clear, cold water for the hiking group.",
            "language_origin": "Old English",
            "source_difficulty": "Multiple Bee levels"
        },
        "sprint": {
            "pronunciation": "/sprɪnt/",
            "definition": "To run at full speed over a short distance; a short race run at maximum speed; any brief period of intense effort or activity. Sprint races in track and field typically cover distances from 50 to 400 meters, requiring explosive power and speed rather than endurance. Athletes train specifically for sprinting through techniques that develop fast-twitch muscle fibers and efficient running mechanics. Business sprints involve intense periods of focused work to complete projects quickly. Software development uses sprint methodology where teams work intensively for short periods to deliver specific features or improvements. The final sprint describes last-minute efforts to complete tasks before deadlines. Sprint swimming events test speed over shorter pool distances compared to distance events. Emergency sprints occur when people must move quickly to avoid danger or catch transportation. The concept emphasizes maximum effort over short duration rather than sustained moderate effort.",
            "etymology": "From Middle English, possibly related to Old Norse 'spretta' meaning to jump or leap. Suggests sudden, explosive movement.",
            "memory_tip": "SPRINT: To run so fast you PRINT across the ground quickly",
            "example_sentence": "She had to _____ across the platform to catch the departing train.",
            "language_origin": "Middle English, Old Norse",
            "source_difficulty": "One Bee"
        },
        "sprite": {
            "pronunciation": "/spraɪt/",
            "definition": "A mythical creature or fairy, typically depicted as small and mischievous; a lively, energetic person, especially a child; in computing, a two-dimensional image or animation. Sprites in folklore are supernatural beings associated with nature, often living in forests, streams, or other natural settings. Water sprites inhabit rivers and lakes, while wood sprites dwell in forests and groves. The term describes people, particularly children, who display elfin qualities such as quick movements, playful behavior, and bright expressions. Computer sprites are graphic objects that can move independently on screen, commonly used in video games and animations. Sprite graphics revolutionized early video game development by allowing smooth character movement and interaction. Atmospheric sprites are rare lightning phenomena that occur high above thunderstorms. The word suggests lightness, quickness, and magical or playful qualities across various contexts from mythology to technology.",
            "etymology": "From Latin 'spiritus' meaning spirit or ghost, through Old French 'esprit.' Related to 'spirit' but developed specific meaning of nature fairy.",
            "memory_tip": "SPRITE: A small, lively SPIRIT that moves quickly and playfully",
            "example_sentence": "The woodland _____ danced among the flowers in the children's fairy tale.",
            "language_origin": "Latin, Old French",
            "source_difficulty": "Multiple Bee levels"
        },
        "spritzed": {
            "pronunciation": "/sprɪtst/",
            "definition": "Past tense of spritz; sprayed lightly with liquid, typically in fine droplets; misted or atomized onto a surface. Spritzed suggests gentle application of liquid through spray bottles, atomizers, or similar devices that create fine mists rather than heavy streams. Plants are spritzed with water to increase humidity or clean leaves without overwatering. Perfume is spritzed onto skin for light, even application that doesn't overwhelm. Hair is spritzed with styling products for hold and texture. Food preparation might involve spritzing oil onto cooking surfaces or vegetables for flavor and moisture. Cleaning involves spritzing surfaces with solutions that can be wiped away easily. The gentle nature of spritzing makes it suitable for delicate applications where heavy application would be inappropriate. The technique provides controlled distribution of liquids for various practical and aesthetic purposes.",
            "etymology": "Past tense of 'spritz,' from German 'spritzen' meaning to spray or splash. Related to 'spray' and other liquid distribution words.",
            "memory_tip": "SPRITZED: Lightly SPRAYED with fine mist like a quick spritz",
            "example_sentence": "She _____ the houseplants with water to keep them fresh and clean.",
            "language_origin": "German",
            "source_difficulty": "Three Bee"
        },
        "sprocket": {
            "pronunciation": "/ˈsprɑkət/",
            "definition": "A wheel with teeth or projections designed to engage with the links of a chain, belt, or other perforated material; commonly used in bicycles, motorcycles, and machinery. Sprockets transfer power from one rotating shaft to another through chain drives, providing mechanical advantage and controlled motion. Bicycle sprockets work with chains to convert pedaling motion into wheel rotation, with different sized sprockets providing various gear ratios. Motorcycle sprockets connect engine power to the rear wheel through chain drive systems. Industrial sprockets drive conveyor belts, printing presses, and manufacturing equipment. Film sprockets engage with perforations along movie film edges to advance frames through projectors and cameras. The teeth of sprockets must be precisely shaped and spaced to mesh properly with chains and prevent slipping. Sprocket systems offer advantages including positive engagement, variable speed ratios, and ability to transmit power around corners or over distances.",
            "etymology": "Origin uncertain, possibly from 'sprig' or 'spoke' referring to tooth-like projections. First recorded in English in the 16th century.",
            "memory_tip": "SPROCKET: A SPOKE-like wheel with teeth that grabs onto chains",
            "example_sentence": "The bicycle's rear _____ needed replacement after years of chain wear.",
            "language_origin": "English (uncertain origin)",
            "source_difficulty": "Three Bee"
        },
        "sprue": {
            "pronunciation": "/spru/",
            "definition": "A channel through which molten metal or plastic is poured into a mold; a tropical disease affecting the digestive system; excess material left attached to molded or cast objects. In manufacturing, sprues provide pathways for molten materials to flow into mold cavities, ensuring complete filling and proper shape formation. After cooling, sprues must be removed from finished products through cutting, grinding, or breaking. Plastic model kits contain parts attached to sprue systems that hobbyists carefully remove and clean before assembly. Medical sprue describes malabsorption syndromes that prevent proper nutrient absorption in the intestines, leading to weight loss and nutritional deficiencies. Tropical sprue affects people in certain geographic regions and may involve bacterial infections or environmental factors. The manufacturing term relates to the tree-like appearance of metal or plastic distribution systems that branch to reach multiple mold cavities simultaneously.",
            "etymology": "From Middle English, possibly related to 'sprout' or from Old French 'esprue.' Medical sense developed separately from manufacturing usage.",
            "memory_tip": "SPRUE: Like a SPROUT that channels material into molds or affects sprouting health",
            "example_sentence": "The metal casting required careful removal of the _____ before final finishing.",
            "language_origin": "Middle English, Old French",
            "source_difficulty": "Multiple Bee levels"
        },
        "spry": {
            "pronunciation": "/spraɪ/",
            "definition": "Active, lively, and nimble, especially despite advanced age; quick and agile in movement or thought. Spry people maintain physical and mental agility that defies expectations based on their age or circumstances. Elderly individuals who remain spry inspire others through their continued vitality and independence. Spry movements suggest efficiency, grace, and energetic purpose rather than slowness or hesitation. Mental spryness involves quick thinking, sharp wit, and intellectual agility that keeps minds engaged and responsive. Physical spryness includes good coordination, balance, and strength that supports active lifestyles. The quality can be maintained through regular exercise, proper nutrition, social engagement, and positive attitudes toward aging. Spry behavior often surprises younger people who expect decreased capability from older individuals. The term emphasizes that age doesn't necessarily limit physical or mental performance when people maintain healthy habits and active lifestyles.",
            "etymology": "Origin uncertain, possibly from dialectal Swedish 'sprygg' meaning active, or related to 'spray' suggesting quick, scattered movement.",
            "memory_tip": "SPRY: So active and quick you seem to FLY around despite your age",
            "example_sentence": "The _____ grandmother could outpace her grandchildren on hiking trails.",
            "language_origin": "Uncertain (possibly Swedish)",
            "source_difficulty": "Multiple Bee levels"
        },
        "spurious": {
            "pronunciation": "/ˈspjʊriəs/",
            "definition": "False or fake; not genuine or authentic; appearing to be true but actually based on false reasoning or misleading information. Spurious claims lack legitimate evidence and often mislead people through superficial plausibility. Spurious correlations appear to show relationships between variables that are actually coincidental rather than causal. Scientific research must distinguish between genuine effects and spurious results that arise from flawed methodology or statistical anomalies. Spurious documents are forgeries designed to appear authentic for fraudulent purposes. Legal proceedings sometimes involve spurious evidence that initially seems credible but proves false under examination. Spurious arguments use logical fallacies or misleading information to create false impressions of validity. The term emphasizes deception, whether intentional or accidental, that creates false appearance of truth or authenticity. Identifying spurious information requires critical thinking skills and careful evaluation of sources and evidence.",
            "etymology": "From Latin 'spurius' meaning illegitimate or false, possibly from 'spurcus' meaning dirty or impure.",
            "memory_tip": "SPURIOUS: Claims that should be SPURRED away because they're false",
            "example_sentence": "The detective quickly identified the _____ confession as inconsistent with the evidence.",
            "language_origin": "Latin",
            "source_difficulty": "Multiple Bee levels"
        },
        "spying": {
            "pronunciation": "/ˈspaɪɪŋ/",
            "definition": "Present participle of spy; the act of secretly watching or gathering information about others; engaging in espionage activities. Spying involves covert observation and intelligence gathering for various purposes including national security, business competition, or personal information. Government spying agencies collect information about foreign nations, terrorist organizations, and security threats. Corporate spying might involve gathering competitor information about products, strategies, or financial status. Spying technology includes surveillance cameras, listening devices, and digital monitoring systems. Counter-spying efforts attempt to detect and prevent unauthorized intelligence gathering. Children playing spy games develop observation skills and imaginative scenarios. Historical spying during wars and conflicts has influenced political outcomes and military strategies. Modern spying concerns include digital privacy, cybersecurity, and protection of personal information from unauthorized surveillance. The activity raises ethical questions about privacy rights versus security needs.",
            "etymology": "Present participle of 'spy,' from Old French 'espier' meaning to watch or observe secretly. Related to 'espy' meaning to catch sight of.",
            "memory_tip": "SPYING: Using your eyes to SPY secretly on others",
            "example_sentence": "The detective spent hours _____ on the suspect from across the street.",
            "language_origin": "Old French",
            "source_difficulty": "Three Bee"
        },
        "squabble": {
            "pronunciation": "/ˈskwæbəl/",
            "definition": "To argue noisily over petty matters; a noisy quarrel about something trivial or unimportant. Squabbles typically involve minor disagreements that escalate into heated arguments disproportionate to their underlying importance. Children squabble over toys, television channels, or seating arrangements without serious long-term consequences. Family squabbles might concern household chores, schedules, or personal preferences that create temporary friction. Political squabbles can distract from important policy discussions when politicians focus on personal attacks rather than substantial issues. Workplace squabbles over procedures, resources, or recognition can damage team morale and productivity. The word suggests petty, undignified arguing that wastes time and energy on trivial matters. Effective conflict resolution helps prevent squabbles by addressing underlying concerns before they escalate. Squabbles differ from serious disputes in their trivial nature and tendency to resolve quickly once emotions cool.",
            "etymology": "Possibly imitative of the sound of arguing, or from Swedish 'sqvabbel' meaning dispute. Related to 'squab' (young bird) suggesting immature behavior.",
            "memory_tip": "SQUABBLE: A small SCRABBLE of words when people argue about petty things",
            "example_sentence": "The siblings' _____ over the remote control disrupted the entire family movie night.",
            "language_origin": "Imitative/Swedish",
            "source_difficulty": "Three Bee"
        },
        "squabblingscuba": {
            "pronunciation": "/ˈskwæbəlɪŋ ˈskubə/",
            "definition": "[COMBINED WORD ERROR] This appears to be incorrectly combined as 'squabbling scuba' - combining 'squabbling' (arguing noisily over petty matters) with 'scuba' (self-contained underwater breathing apparatus). Squabbling refers to noisy arguments over trivial issues, while scuba enables underwater breathing through portable air supplies. The combination makes no logical sense as underwater activities require cooperation and safety focus rather than petty arguments. Scuba diving demands clear communication, buddy system protocols, and attention to safety procedures that would be compromised by squabbling behavior. Professional dive teams maintain strict discipline to prevent accidents that could result from distraction or poor communication. This represents a clear data processing error where unrelated terms were inappropriately merged. Successful scuba operations require calm, focused teamwork that is incompatible with argumentative squabbling.",
            "etymology": "Squabbling: imitative of arguing sounds + Scuba: acronym from 'Self-Contained Underwater Breathing Apparatus'",
            "memory_tip": "Remember: SQUABBLING (arguing) + SCUBA (underwater breathing) - these don't go together",
            "example_sentence": "The dive team avoided _____ by maintaining clear communication protocols underwater.",
            "language_origin": "English (compound error)",
            "source_difficulty": "Two Bee"
        },
        "squadron": {
            "pronunciation": "/ˈskwɑdrən/",
            "definition": "A unit of military aircraft or naval vessels; an organized group operating together for a common purpose. Air force squadrons typically consist of 12-24 aircraft with associated personnel, equipment, and support facilities. Naval squadrons might include multiple ships organized for specific missions such as carrier operations, submarine warfare, or coastal patrol. Military squadrons maintain unit identity through distinctive markings, traditions, and command structures. Squadron leaders coordinate training, operations, and personnel management within their units. Cavalry squadrons historically consisted of mounted soldiers organized for reconnaissance and rapid movement. Police squadrons might refer to specialized units such as mounted police, motorcycle units, or tactical teams. The organizational structure provides tactical flexibility while maintaining command and control. Squadron traditions often include unique patches, call signs, and ceremonial activities that build unit cohesion and pride.",
            "etymology": "From Italian 'squadrone,' augmentative of 'squadra' meaning square formation, from Latin 'quadra' (square). Military formation in square patterns.",
            "memory_tip": "SQUADRON: A SQUAD that flies or sails together in formation",
            "example_sentence": "The fighter _____ completed their training mission and returned to base.",
            "language_origin": "Italian, Latin",
            "source_difficulty": "One Bee"
        },
        "squalid": {
            "pronunciation": "/ˈskwælɪd/",
            "definition": "Extremely dirty and unpleasant due to neglect or poverty; morally degraded or repulsive. Squalid living conditions include overcrowded, unsanitary housing that lacks basic amenities and proper maintenance. Squalid environments pose health risks through poor sanitation, contaminated water, and inadequate waste disposal. The term can describe both physical conditions and moral circumstances that are degraded or corrupt. Squalid behavior involves actions that are ethically reprehensible or socially unacceptable. Urban squalor often results from poverty, inadequate housing policies, and insufficient social services. Squalid prisons or institutions fail to meet basic human dignity standards. The word suggests both physical filth and moral degradation that demand intervention and improvement. Social workers and humanitarian organizations work to address squalid conditions through improved housing, sanitation, and support services. Understanding squalor helps recognize the connection between physical environment and human dignity.",
            "etymology": "From Latin 'squalidus' meaning rough, dirty, or neglected, from 'squalere' meaning to be dirty or rough.",
            "memory_tip": "SQUALID: So dirty it makes you SQUEAL with disgust",
            "example_sentence": "The humanitarian organization worked to improve the _____ living conditions in the refugee camp.",
            "language_origin": "Latin",
            "source_difficulty": "Multiple Bee levels"
        },
        "squall": {
            "pronunciation": "/skwɔl/",
            "definition": "A sudden violent gust of wind, often accompanied by rain or snow; a brief but intense storm; to cry or scream loudly. Weather squalls can appear suddenly and create dangerous conditions for small boats and aircraft. Snow squalls produce heavy snowfall over short periods that can reduce visibility and create hazardous driving conditions. Rain squalls bring intense precipitation that may cause localized flooding. The verb 'squall' describes loud crying or screaming, typically by infants or children. Squalls at sea require immediate response from sailors to secure equipment and adjust course. Weather forecasters issue squall warnings to help people prepare for sudden wind changes. Line squalls form along weather fronts and can produce severe weather including high winds and hail. The sudden, intense nature of squalls makes them particularly dangerous because they provide little warning time for protective action.",
            "etymology": "Possibly from Old Norse 'skvala' meaning to cry out, or imitative of wind or crying sounds. Weather and vocal meanings may share origins.",
            "memory_tip": "SQUALL: Sudden wind that makes you want to SQUEAL and call for help",
            "example_sentence": "The sailing crew quickly lowered the sails as the _____ approached with fierce winds.",
            "language_origin": "Old Norse (possibly)",
            "source_difficulty": "Multiple Bee levels"
        },
        "squander": {
            "pronunciation": "/ˈskwændər/",
            "definition": "To waste something valuable through careless or extravagant use; to spend or use resources foolishly without getting appropriate benefit. People squander money through impulse purchases, poor investments, or failure to budget effectively. Time can be squandered through procrastination, inefficient planning, or engaging in unproductive activities. Squandering opportunities means failing to take advantage of chances for advancement, learning, or improvement. Natural resources are squandered through inefficient use, pollution, or overconsumption that depletes supplies for future generations. Talents can be squandered when people fail to develop or use their abilities constructively. The term implies both waste and regret, suggesting that valuable resources deserved better treatment. Avoiding squandering requires careful planning, value assessment, and disciplined decision-making. Understanding what constitutes squandering helps people make better choices about resource allocation and priority setting.",
            "etymology": "Origin uncertain, possibly from dialect 'squatter' meaning to scatter, or related to 'wander' suggesting aimless dispersal of resources.",
            "memory_tip": "SQUANDER: To SCATTER and WANDER your resources away wastefully",
            "example_sentence": "She refused to _____ her inheritance on unnecessary luxury purchases.",
            "language_origin": "English (uncertain origin)",
            "source_difficulty": "Multiple Bee levels"
        },
        "square": {
            "pronunciation": "/skwɛr/",
            "definition": "A geometric shape with four equal sides and four right angles; a public open space in a city; to multiply a number by itself; honest or fair. Square shapes appear in architecture, art, and design as symbols of stability and order. Public squares serve as gathering places for markets, celebrations, and community events. Mathematical squares involve multiplying numbers by themselves, such as 3 squared equals 9. Square deals refer to fair, honest transactions that treat all parties equitably. Square dancing involves traditional folk dances performed in square formations. Square meals provide complete, satisfying nutrition. The phrase 'back to square one' means returning to the beginning. Square people are considered conventional or old-fashioned in slang usage. Squares provide fundamental building blocks for geometric constructions and mathematical calculations. The multiple meanings reflect the shape's associations with stability, fairness, and basic mathematical concepts.",
            "etymology": "From Old French 'esquarre,' from Latin 'quadra' meaning square or four-sided figure. Related to 'quadrate' and 'quarter.'",
            "memory_tip": "SQUARE: A shape that's perfectly SQUARED off with four equal sides",
            "example_sentence": "The town _____ filled with vendors selling fresh produce and local crafts.",
            "language_origin": "Old French, Latin",
            "source_difficulty": "Three Bee"
        },
        "squash": {
            "pronunciation": "/skwɑʃ/",
            "definition": "To crush or squeeze something so as to destroy its shape; a type of vegetable; a racquet sport played in an enclosed court. Squashing involves applying pressure to flatten or compress objects beyond their normal shape. The sport of squash requires players to hit a small rubber ball against court walls using racquets. Squash vegetables include various species like butternut, acorn, and summer squash that provide nutrition and culinary variety. People squash insects to kill them or squash rumors to prevent their spread. Emotional squashing occurs when people suppress feelings or discourage others' enthusiasm. Legal proceedings might squash charges or appeals to prevent further action. The verb suggests forceful compression that eliminates original form or function. Squash courts require specific dimensions and wall materials to ensure proper ball bouncing characteristics. Understanding squash helps recognize both physical processes and metaphorical applications of pressure and compression.",
            "etymology": "From Old French 'esquasser' meaning to crush, from Latin 'ex-' (out) + 'quassare' (to shake violently). Vegetable meaning from Native American languages.",
            "memory_tip": "SQUASH: To SQUEEZE and SMASH something flat, or the sport where you smash balls",
            "example_sentence": "He accidentally managed to _____ the delicate flower while weeding the garden.",
            "language_origin": "Old French, Latin; Native American",
            "source_difficulty": "Three Bee"
        },
        "squawk": {
            "pronunciation": "/skwɔk/",
            "definition": "To make a loud, harsh cry like a bird; to complain loudly and persistently about something. Birds squawk when alarmed, defending territory, or communicating with flocks. Parrots and other large birds produce distinctive squawking sounds as part of their natural vocalizations. People squawk when protesting decisions, policies, or treatment they consider unfair. Radio squawk refers to harsh static or interference that makes communication difficult. Squawking can indicate distress, anger, or urgent need for attention in both animals and humans. The sound is typically unpleasant and attention-getting rather than melodious or subtle. Chickens squawk when threatened or disturbed by predators or human activity. Children might squawk when frustrated or demanding attention from parents. The imitative word captures both the harsh quality of the sound and its function as an alarm or protest signal.",
            "etymology": "Imitative word that mimics the harsh cry of birds, particularly larger species like parrots, crows, and chickens.",
            "memory_tip": "SQUAWK: The harsh HAWK-like sound birds make when upset",
            "example_sentence": "The disturbed chickens began to _____ loudly when the fox approached the coop.",
            "language_origin": "Imitative/Onomatopoetic",
            "source_difficulty": "One Bee"
        },
        "squawl": {
            "pronunciation": "/skwɔl/",
            "definition": "An archaic or dialect variant of 'squall'; to cry out loudly or make harsh sounds. This spelling appears in older texts or regional dialects but is largely obsolete in modern English. The meaning parallels 'squall' in describing loud, harsh vocal sounds or crying. Historical usage might appear in literature from earlier periods when spelling was less standardized. The term captures similar concepts of sudden, loud, unpleasant sounds whether from weather phenomena or vocal expressions. Regional dialects sometimes preserve older spelling patterns that reflect historical pronunciation or linguistic development. Understanding such variants helps in reading historical documents and recognizing linguistic change over time. Modern usage would typically employ 'squall' instead of this variant spelling. The word demonstrates how language evolves and standardizes while preserving historical forms in specialized contexts.",
            "etymology": "Archaic variant of 'squall,' possibly preserving older spelling patterns or regional pronunciation differences.",
            "memory_tip": "SQUAWL: An old way to spell SQUALL - making loud harsh sounds",
            "example_sentence": "In the old text, the baby was described as beginning to _____ when hungry.",
            "language_origin": "English (archaic variant)",
            "source_difficulty": "Multiple Bee levels"
        },
        "squeak": {
            "pronunciation": "/skwik/",
            "definition": "To make a short, high-pitched sound; to barely succeed or achieve something. Squeaking sounds occur when objects rub together with insufficient lubrication, such as door hinges, floorboards, or vehicle brakes. Mice and other small animals produce characteristic squeaking vocalizations. Shoes squeak on certain floor surfaces due to friction between materials. People squeak when their voices rise to high pitches from excitement, fear, or strain. Squeaking through means barely passing tests, meeting deadlines, or achieving goals with minimal margin for error. The phrase 'the squeaky wheel gets the grease' suggests that complaints receive attention. Musical instruments can squeak when played improperly or need maintenance. Squeaking often indicates need for adjustment, lubrication, or repair. The high-pitched nature of squeaking makes it attention-getting even when sounds are quiet.",
            "etymology": "Imitative word that mimics high-pitched sounds produced by friction, small animals, or strained voices.",
            "memory_tip": "SQUEAK: A quick high SQUEAL sound like mice make",
            "example_sentence": "The old wooden stairs began to _____ under the weight of the heavy furniture.",
            "language_origin": "Imitative/Onomatopoetic",
            "source_difficulty": "One Bee"
        },
        "squeal": {
            "pronunciation": "/skwil/",
            "definition": "To make a long, high-pitched cry or sound; to inform on someone, especially to authorities. Pigs squeal when excited, frightened, or handled roughly. Children squeal with delight during play or when surprised by pleasant experiences. Car tires squeal when vehicles brake hard or take corners at high speed. Squealing on someone means providing information about their activities, often implying betrayal or cooperation with authorities. The sound indicates intense emotion, whether fear, excitement, or distress. Mechanical squealing might indicate brake problems, belt issues, or other maintenance needs in vehicles or machinery. Playground squealing typically represents joy and excitement during active play. Police informants are sometimes called 'squealers' in criminal contexts. The term captures both the quality of high-pitched sounds and the social dynamics of information sharing.",
            "etymology": "From Middle English 'squelen,' possibly imitative of high-pitched animal sounds, particularly pigs.",
            "memory_tip": "SQUEAL: A long high SQUEAK that shows strong feelings",
            "example_sentence": "The excited children began to _____ with joy when they saw the surprise party.",
            "language_origin": "Middle English (imitative)",
            "source_difficulty": "Three Bee"
        },
        "squeamish": {
            "pronunciation": "/ˈskwimɪʃ/",
            "definition": "Easily nauseated or made to feel sick; having a weak stomach; overly sensitive about matters involving blood, violence, or unpleasant topics. Squeamish people avoid medical shows, horror movies, or graphic content that might trigger nausea or discomfort. Some individuals feel squeamish about blood draws, injections, or surgical procedures. Squeamish reactions can include dizziness, nausea, or fainting when exposed to disturbing sights or sounds. The trait varies among individuals and can be overcome through gradual exposure and desensitization techniques. Medical professionals must work with squeamish patients to provide care while minimizing discomfort. Squeamish responses serve evolutionary functions by helping people avoid potentially dangerous or contaminated situations. Understanding squeamishness helps in accommodating different comfort levels and sensitivities. The condition can interfere with necessary medical care if not properly managed through supportive techniques.",
            "etymology": "Origin uncertain, possibly from 'squeem' (to feel sick) or related to 'qualm.' First recorded in English around 1400.",
            "memory_tip": "SQUEAMISH: Makes you want to SQUEEM and feel sick at unpleasant sights",
            "example_sentence": "She was too _____ to watch the medical documentary about surgical procedures.",
            "language_origin": "English (uncertain origin)",
            "source_difficulty": "Multiple Bee levels"
        },
        "squeeze": {
            "pronunciation": "/skwiz/",
            "definition": "To apply pressure to something from opposite sides; to force something into or through a tight space; financial pressure or difficulty. Squeezing involves compressing objects to extract contents, reduce size, or apply force. People squeeze toothpaste tubes, orange juice, or stress balls. Tight spaces require squeezing through doorways, crowds, or narrow passages. Financial squeezes occur when budgets become tight and expenses must be reduced. Economic squeezes affect businesses through increased costs, reduced demand, or credit restrictions. Squeezing profits means reducing expenses to maintain financial performance. Physical squeezing can show affection through hugs or create discomfort through excessive pressure. The action suggests both controlled pressure application and potential constraint or limitation. Understanding squeeze helps recognize both mechanical processes and economic pressures that affect daily life.",
            "etymology": "From Middle English 'queysen,' possibly from Old English 'cwȳsan' meaning to bruise or crush.",
            "memory_tip": "SQUEEZE: To SQUEEZE something tight like squeezing a wet sponge",
            "example_sentence": "She had to _____ through the narrow gap between the parked cars.",
            "language_origin": "Middle English, Old English",
            "source_difficulty": "Three Bee"
        },
        "squid": {
            "pronunciation": "/skwɪd/",
            "definition": "A marine cephalopod mollusk with ten arms, two of which are longer tentacles, and the ability to change color and release ink. Squids are intelligent invertebrates related to octopuses and cuttlefish, known for their rapid swimming and sophisticated hunting behaviors. Giant squids can reach enormous sizes and live in deep ocean waters, inspiring maritime legends and scientific fascination. Squids use jet propulsion by expelling water through siphons, allowing rapid movement and escape from predators. Many species can change color and pattern for camouflage, communication, or threat display. Squid ink serves as defense mechanism and culinary ingredient in various cuisines. Commercial squid fishing provides food products and bait for other fishing operations. Squid eyes are among the largest in the animal kingdom, providing excellent vision for hunting in marine environments. Scientific study of squids contributes to understanding of intelligence, evolution, and marine ecosystems.",
            "etymology": "Origin uncertain, possibly related to 'squirt' referring to ink ejection, or from dialectal words meaning something that squirts.",
            "memory_tip": "SQUID: A sea creature that can SQUIRT ink and swim quickly",
            "example_sentence": "The marine biologist studied the _____ specimen to understand its color-changing abilities.",
            "language_origin": "English (uncertain origin)",
            "source_difficulty": "One Bee"
        },
        "squiggles": {
            "pronunciation": "/ˈskwɪɡəlz/",
            "definition": "Irregular wavy or curvy lines; marks that twist and turn without clear pattern or purpose. Squiggles appear in handwriting, art, and natural patterns where lines deviate from straight or regular curves. Children's drawings often feature squiggles as they develop fine motor control and artistic expression. Artistic squiggles can create texture, movement, or decorative elements in visual compositions. Electrocardiogram readouts show squiggly lines representing heart rhythms and electrical activity. Signature squiggles sometimes develop as personal identification marks that are difficult to forge. Seismograph squiggles record earthquake vibrations and ground movements. The irregular nature of squiggles suggests spontaneity, movement, or natural variation rather than controlled precision. Decorative squiggles add visual interest to designs while maintaining informal, playful character. Understanding squiggles helps recognize both artistic techniques and natural patterns that deviate from geometric regularity.",
            "etymology": "Possibly from 'squiggle' meaning to twist or wriggle, combined with diminutive or frequentative elements suggesting small repeated movements.",
            "memory_tip": "SQUIGGLES: Little wavy lines that WIGGLE and SQUIRM around",
            "example_sentence": "The child decorated the paper with colorful _____ and cheerful drawings.",
            "language_origin": "English",
            "source_difficulty": "Two Bee"
        },
        "squinched": {
            "pronunciation": "/skwɪntʃt/",
            "definition": "Past tense of squinch; squeezed or compressed tightly; closed or narrowed eyes or facial features. Squinching typically involves contracting facial muscles to narrow eyes, wrinkle features, or create compressed expressions. People squinch their eyes in bright sunlight, when concentrating intensely, or when expressing skepticism. Facial squinching can indicate discomfort, confusion, or effort to see or understand something better. The action involves deliberate muscle tension that temporarily alters facial appearance. Squinched expressions often accompany mental effort, physical strain, or emotional reactions. Photographers sometimes ask subjects to squinch slightly to create more flattering eye expressions. The term suggests both physical compression and the effort required to produce such expressions. Understanding squinching helps recognize non-verbal communication and physical responses to environmental or emotional stimuli.",
            "etymology": "Past tense of 'squinch,' possibly from 'squint' + 'pinch,' suggesting the action of narrowing or compressing features.",
            "memory_tip": "SQUINCHED: SQUEEZED your face tight like squinting and pinching",
            "example_sentence": "She _____ her eyes against the bright sunlight reflecting off the snow.",
            "language_origin": "English",
            "source_difficulty": "Two Bee"
        },
        "squints": {
            "pronunciation": "/skwɪnts/",
            "definition": "Partially closes eyes to see better; looks with eyes partly closed; has a condition where eyes don't align properly (strabismus). Squinting helps reduce light entering eyes and can improve focus when vision is impaired or lighting is poor. People squint in bright sunlight, when reading small text, or when concentrating on distant objects. Medical squinting (strabismus) involves misalignment of eyes that can affect depth perception and visual development. Squinting can indicate vision problems that require corrective lenses or medical treatment. The action involves contracting muscles around the eyes to narrow the opening and reduce glare or improve focus. Habitual squinting might suggest need for eye examination and vision correction. Squinting expressions can convey skepticism, suspicion, or intense concentration. Understanding squinting helps recognize both vision issues and non-verbal communication signals. Protective squinting prevents eye damage from excessive light exposure.",
            "etymology": "Third person singular present of 'squint,' from Middle English, possibly related to 'asquint' meaning obliquely or sideways.",
            "memory_tip": "SQUINTS: When someone HINTS they can't see well by squeezing their eyes",
            "example_sentence": "He _____ at the fine print, trying to read the contract details.",
            "language_origin": "Middle English",
            "source_difficulty": "Two Bee"
        },
        "squire": {
            "pronunciation": "/skwaɪər/",
            "definition": "A young nobleman acting as an attendant to a knight; a country gentleman; to escort or attend someone, especially a woman. Historical squires served apprenticeships with knights, learning combat skills, chivalry, and nobility responsibilities. Medieval squires cared for knights' equipment, horses, and personal needs while training for eventual knighthood. English country squires were landowners who held local social and political influence in rural communities. The verb 'to squire' means to escort or accompany someone, particularly in formal or protective contexts. Modern usage might refer to local dignitaries or community leaders who maintain traditional roles. Squires represented intermediate social rank between common people and full knights or nobility. The position combined service, learning, and preparation for greater responsibility. Understanding squire roles helps explain historical social structures and mentorship systems that shaped medieval society and culture.",
            "etymology": "From Old French 'esquier' meaning shield-bearer, from Latin 'scutarius' (shield-bearer), from 'scutum' (shield).",
            "memory_tip": "SQUIRE: A SQUARE-dealing young man who serves a knight",
            "example_sentence": "The young _____ polished his master's armor before the tournament.",
            "language_origin": "Old French, Latin",
            "source_difficulty": "Three Bee"
        },
        "squirm": {
            "pronunciation": "/skwɜrm/",
            "definition": "To twist and writhe, especially from discomfort or embarrassment; to feel awkward or uncomfortable in a situation. Physical squirming involves restless movement when sitting or lying down for extended periods. Children squirm when bored, uncomfortable, or eager to move around. People squirm when discussing embarrassing topics, receiving criticism, or facing awkward social situations. Emotional squirming reflects internal discomfort that manifests through physical restlessness. Worms and other creatures squirm as natural locomotion through contracting and extending their bodies. Medical patients might squirm during uncomfortable procedures or examinations. The movement suggests both physical discomfort and psychological unease that seeks relief through motion. Squirming often indicates need for position change, emotional support, or escape from uncomfortable circumstances. Understanding squirming helps recognize both physical needs and emotional states that require attention or accommodation.",
            "etymology": "Possibly imitative of writhing motion, or related to Middle English 'swirmen' meaning to swarm or move restlessly.",
            "memory_tip": "SQUIRM: To SWIRL and WORM around when uncomfortable",
            "example_sentence": "The guilty child began to _____ in his chair when questioned about the broken vase.",
            "language_origin": "English (possibly imitative)",
            "source_difficulty": "Multiple Bee levels"
        },
        "sravaka": {
            "pronunciation": "/ˈʃrɑvəkə/",
            "definition": "In Buddhism, a disciple or follower who learns from hearing the Buddha's teachings; one who attains enlightenment through listening to and following the Dharma. Sravakas represent one of the main categories of Buddhist practitioners who seek individual liberation through understanding the Four Noble Truths and following the Eightfold Path. The term literally means 'one who hears' in Sanskrit, emphasizing the importance of receiving and comprehending Buddhist teachings. Sravakas pursue arhat status, achieving personal enlightenment and liberation from the cycle of rebirth. This path differs from the bodhisattva ideal, which emphasizes helping all beings achieve enlightenment. Traditional sravakas follow prescribed meditation practices, ethical conduct, and wisdom development. The classification appears in Mahayana Buddhist texts that distinguish different approaches to spiritual development. Understanding sravaka helps explain Buddhist philosophical categories and approaches to enlightenment. Modern practitioners might identify with sravaka principles while adapting ancient practices to contemporary life.",
            "etymology": "From Sanskrit 'śrāvaka' meaning 'one who hears,' from 'śru' (to hear) + agent suffix. Related to 'śruti' (that which is heard).",
            "memory_tip": "SRAVAKA: Someone who learns by HEARING the Buddha's teachings",
            "example_sentence": "The _____ meditated daily, following the Buddha's prescribed path to individual enlightenment.",
            "language_origin": "Sanskrit",
            "source_difficulty": "Multiple Bee levels"
        },
        "sreethan": {
            "pronunciation": "/ˈsrɪθən/",
            "definition": "This appears to be a proper name or possibly a transliteration from another language, though its specific meaning and origin are not clearly established in standard English dictionaries. The term might represent a personal name, place name, or concept from South Asian languages given its phonetic structure. Without clear etymological evidence, it's difficult to provide definitive meaning or usage context. Such terms often appear in spelling competitions when drawn from diverse linguistic backgrounds or specialized vocabularies. The word structure suggests possible Sanskrit, Hindi, or related language origins, though verification would require specialized linguistic sources. When encountering unfamiliar terms in spelling contexts, it's important to note pronunciation guides and potential language family connections. Understanding such words requires research into specific cultural, religious, or regional linguistic traditions that may not be widely documented in standard references.",
            "etymology": "Origin uncertain; possibly from South Asian language traditions, though specific etymology requires verification.",
            "memory_tip": "SREETHAN: Remember the unique spelling pattern with 'sree' + 'than'",
            "example_sentence": "The name _____ appeared in the cultural exchange program materials.",
            "language_origin": "Uncertain (possibly South Asian)",
            "source_difficulty": "Three Bee"
        },
        "stabilized": {
            "pronunciation": "/ˈsteɪbəˌlaɪzd/",
            "definition": "Past tense of stabilize; made stable, steady, or unchanging; restored to a stable condition after a period of instability. Stabilized systems resist change and maintain consistent performance despite external pressures or disturbances. Medical stabilization involves bringing patients' vital signs and conditions to safe, manageable levels. Economic stabilization efforts aim to control inflation, unemployment, and market volatility. Stabilized cameras reduce blur through mechanical or electronic systems that compensate for movement. Chemical stabilization prevents degradation, decomposition, or unwanted reactions in materials. Psychological stabilization helps people regain emotional equilibrium after trauma or crisis. Structural stabilization prevents buildings or equipment from shifting, settling, or failing. The process often requires intervention, support systems, or control mechanisms to maintain desired conditions. Understanding stabilization helps recognize both natural and artificial systems that resist change and maintain consistent function despite varying conditions.",
            "etymology": "From 'stabilize' (from Latin 'stabilis' meaning firm or steady) + past tense suffix '-ed.' Related to 'stable' and 'stability.'",
            "memory_tip": "STABILIZED: Made STABLE and steady, no longer wobbling or changing",
            "example_sentence": "The patient's condition was _____ after emergency surgery and intensive care.",
            "language_origin": "Latin",
            "source_difficulty": "Three Bee"
        },
        "stagecoach": {
            "pronunciation": "/ˈsteɪdʒˌkoʊtʃ/",
            "definition": "A large, horse-drawn vehicle used for carrying passengers and mail over long distances before the development of railways. Stagecoaches operated on regular routes with scheduled stops at stations where horses could be changed and passengers could rest. The vehicles typically held 6-12 passengers inside with additional seating on top for those willing to pay less for outside travel. Stagecoach travel was slow, uncomfortable, and sometimes dangerous due to rough roads, weather, and potential robberies. Famous stagecoach routes included the Overland Stage in the American West and mail coaches in England. Stagecoach companies provided essential transportation and communication services connecting distant communities. The industry declined rapidly with railroad development but remains important in transportation and communication history. Modern tourist attractions sometimes feature authentic or replica stagecoaches to demonstrate historical travel conditions. Understanding stagecoaches helps appreciate transportation challenges before modern infrastructure.",
            "etymology": "Compound of 'stage' (a regular stopping place on a journey) + 'coach' (large passenger vehicle). Stages referred to predetermined route segments.",
            "memory_tip": "STAGECOACH: A horse-drawn COACH that traveled in STAGES between towns",
            "example_sentence": "The _____ bounced along the dusty trail, carrying mail and passengers to the frontier town.",
            "language_origin": "English compound",
            "source_difficulty": "Three Bee"
        },
        "stagestruck": {
            "pronunciation": "/ˈsteɪdʒˌstrʌk/",
            "definition": "Fascinated by the theater and having a strong desire to become an actor or performer; completely captivated by theatrical performance and stage life. Stagestruck individuals often dream of careers in acting, singing, dancing, or other performing arts. The condition typically involves romantic idealization of theater life and celebrity status. Young people frequently become stagestruck after attending powerful performances or meeting charismatic performers. Stagestruck behavior might include participating in school plays, taking acting classes, or constantly discussing theater and entertainment. The term suggests both positive enthusiasm and potentially unrealistic expectations about entertainment careers. Professional theater requires dedication, training, and talent beyond initial fascination. Stagestruck individuals often benefit from realistic guidance about entertainment industry challenges while pursuing their interests. Understanding the phenomenon helps distinguish between healthy artistic interest and unrealistic career expectations that might need tempering with practical considerations.",
            "etymology": "Compound of 'stage' (theatrical performance area) + 'struck' (overwhelmed or affected), similar to 'thunderstruck' or 'lovestruck.'",
            "memory_tip": "STAGESTRUCK: So fascinated by the theater STAGE that you're STRUCK with wanting to perform",
            "example_sentence": "The _____ teenager auditioned for every school play and dreamed of Broadway stardom.",
            "language_origin": "English compound",
            "source_difficulty": "Multiple Bee levels"
        },
        "stagflation": {
            "pronunciation": "/stægˈfleɪʃən/",
            "definition": "An economic condition characterized by simultaneous inflation (rising prices) and economic stagnation (high unemployment and slow growth). Stagflation challenges traditional economic theory, which typically assumes inverse relationships between inflation and unemployment. The phenomenon gained prominence during the 1970s when oil price shocks and other factors created unprecedented economic conditions. Stagflation presents policy dilemmas because traditional remedies for inflation (reducing spending) can worsen unemployment, while measures to stimulate growth might increase inflation. Central banks struggle with stagflation because raising interest rates to combat inflation can deepen recession and unemployment. The condition often results from supply shocks, productivity declines, or structural economic changes that disrupt normal relationships. Stagflation erodes purchasing power while limiting employment opportunities, creating particular hardship for working families. Modern economists study historical stagflation episodes to understand causes and develop better policy responses for similar future situations.",
            "etymology": "Portmanteau of 'stagnation' + 'inflation,' coined in 1965 by British politician Iain Macleod to describe concurrent economic problems.",
            "memory_tip": "STAGFLATION: When the economy STAGNATES but prices still have inFLATION",
            "example_sentence": "The 1970s _____ period challenged economists' understanding of traditional inflation-unemployment relationships.",
            "language_origin": "English portmanteau",
            "source_difficulty": "Multiple Bee levels"
        },
        "staggered": {
            "pronunciation": "/ˈstæɡərd/",
            "definition": "Past tense of stagger; moved unsteadily or swayed while walking; shocked or overwhelmed; arranged in overlapping or alternating patterns. Physical staggering occurs when people lose balance due to illness, fatigue, intoxication, or injury. Emotional staggering describes overwhelming surprise, shock, or disbelief that leaves people temporarily unable to respond normally. Staggered schedules arrange work times so that not all employees start and end simultaneously, reducing crowding and extending coverage. Staggered formations place objects or people in alternating patterns rather than straight lines. Staggered payments spread large expenses over multiple installments to improve affordability. The word suggests both physical instability and temporal distribution that provides practical benefits. Staggered arrangements often improve efficiency, reduce congestion, or distribute loads more evenly. Understanding staggering helps recognize both balance problems and organizational strategies that manage resources and timing effectively.",
            "etymology": "Past tense of 'stagger,' from Old Norse 'stakra' meaning to push or stagger. Related to 'stack' and words suggesting unsteady movement.",
            "memory_tip": "STAGGERED: Moved like you're about to fall, or arranged in a zig-zag pattern",
            "example_sentence": "He _____ backward, overwhelmed by the unexpected news from his family.",
            "language_origin": "Old Norse",
            "source_difficulty": "One Bee"
        },
        "staid": {
            "pronunciation": "/steɪd/",
            "definition": "Sedate, respectable, and unadventurous; characterized by a serious, steady, and somewhat conservative demeanor. Staid people prefer conventional behavior and avoid dramatic or risky activities. Staid institutions maintain traditional practices and resist rapid change or innovation. The quality suggests reliability and respectability but might also imply resistance to excitement or novelty. Staid clothing choices favor conservative styles over fashionable or attention-getting options. Staid communities value stability, order, and established social norms. Business environments might be described as staid when they emphasize formal procedures and conservative practices. The term can carry both positive connotations of reliability and negative implications of dullness or inflexibility. Staid personalities provide stability in relationships and organizations but might struggle with creativity or adaptation. Understanding staid characteristics helps recognize the value of different personality types and approaches to life and work.",
            "etymology": "From past participle of obsolete 'stay' meaning to check or restrain, suggesting someone who restrains themselves from excess.",
            "memory_tip": "STAID: STAYED calm and serious, never getting too excited",
            "example_sentence": "The _____ professor preferred traditional teaching methods over innovative classroom techniques.",
            "language_origin": "English",
            "source_difficulty": "Multiple Bee levels"
        },
        "stairs": {
            "pronunciation": "/stɛrz/",
            "definition": "A series of steps leading from one floor or level to another in a building. Stairs provide vertical circulation in multi-story structures, allowing people to move between floors safely and efficiently. Stair design involves careful calculation of riser height, tread depth, and overall angle to ensure comfort and safety. Building codes specify minimum and maximum dimensions for stairs to prevent accidents and ensure accessibility. Stairs can be straight, curved, spiral, or arranged in various configurations to fit architectural requirements. Handrails and guardrails provide support and safety features for stair users. Emergency stairs offer alternative escape routes during fires or other building emergencies. Decorative stairs serve as architectural focal points while maintaining functional requirements. Maintenance of stairs includes cleaning, repair of worn treads, and ensuring proper lighting for safety. Understanding stairs helps appreciate both functional design requirements and architectural possibilities for vertical circulation.",
            "etymology": "From Old English 'stǣger,' related to 'to stare' in the sense of being stiff or rigid, referring to the fixed steps.",
            "memory_tip": "STAIRS: Steps that help you STARE up at higher floors",
            "example_sentence": "She climbed the narrow _____ to reach the apartment on the third floor.",
            "language_origin": "Old English",
            "source_difficulty": "Two Bee"
        },
        "stalagmite": {
            "pronunciation": "/stəˈlæɡˌmaɪt/",
            "definition": "A deposit of calcium carbonate rising from the floor of a cave, formed by the dripping of mineral-rich water over long periods. Stalagmites grow upward from cave floors as water containing dissolved limestone drips from above and deposits minerals. The formation process requires thousands of years of consistent water dripping and mineral deposition. Stalagmites often pair with stalactites hanging from cave ceilings, sometimes eventually meeting to form columns. The mineral composition typically includes calcite, though other minerals can create different colors and textures. Cave formations like stalagmites provide evidence of long-term geological processes and past climate conditions. Tourist caves often feature spectacular stalagmite formations that demonstrate natural geological artistry. Scientific study of stalagmites helps researchers understand historical climate patterns and geological change. The formations are fragile and can be damaged by touching, temperature changes, or pollution.",
            "etymology": "From Greek 'stalagma' meaning a drop, from 'stalassein' (to drip) + suffix '-ite' indicating mineral formation.",
            "memory_tip": "STALAGMITE: Mineral formations that MIGHT reach the ceiling, growing UP from the ground",
            "example_sentence": "The massive _____ in the center of the cave had taken millennia to form.",
            "language_origin": "Greek",
            "source_difficulty": "One Bee"
        },
        "stalemate": {
            "pronunciation": "/ˈsteɪlˌmeɪt/",
            "definition": "A situation in which neither side in a conflict can win or make progress; in chess, a position where a player has no legal moves but is not in check. Stalemates occur in negotiations, wars, and competitions when opposing forces reach deadlocks that prevent resolution. Chess stalemates result in draws because the player whose turn it is cannot move without putting their king in check. Political stalemates happen when legislative bodies cannot pass important legislation due to partisan gridlock. Labor stalemates involve deadlocked negotiations between workers and management that prevent contract agreements. The condition suggests frustration and the need for creative solutions or outside intervention to break impasses. Stalemates often require compromise, mediation, or changed circumstances to achieve resolution. Understanding stalemates helps recognize when situations need new approaches or perspectives to move forward. Strategic thinking about stalemates involves looking for ways to change conditions rather than continue ineffective approaches.",
            "etymology": "From 'stale' (Middle English meaning fixed position) + 'mate' (from chess term for defeated king). Originally a chess term.",
            "memory_tip": "STALEMATE: A STALE situation where neither side can make a MATE or winning move",
            "example_sentence": "The budget negotiations reached a _____ with neither party willing to compromise.",
            "language_origin": "Middle English",
            "source_difficulty": "Two Bee"
        },
        "stall": {
            "pronunciation": "/stɔl/",
            "definition": "A compartment for an animal in a stable; a booth for selling goods; to delay or prevent progress; to come to a stop suddenly. Horse stalls provide individual living spaces in barns with feeding and watering facilities. Market stalls offer temporary retail spaces for vendors selling food, crafts, or other goods. Vehicle engines stall when they stop running due to mechanical problems or operator error. Stalling tactics involve deliberately delaying actions or decisions to gain advantage or avoid unwanted outcomes. Bathroom stalls provide privacy in public restrooms through partial enclosures. Aircraft can stall when airspeed drops too low to maintain lift, requiring specific recovery procedures. Legislative stalling might involve filibusters or procedural delays to prevent votes on controversial bills. The word suggests both physical enclosure and the cessation of movement or progress. Understanding stalling helps recognize both mechanical failures and strategic behaviors that affect timing and outcomes.",
            "etymology": "From Old English 'steall' meaning a standing place or stable, related to 'stall' meaning to place or install.",
            "memory_tip": "STALL: A SMALL space for animals, or when something comes to a FULL stop",
            "example_sentence": "The car began to _____ in heavy traffic, forcing them to restart the engine.",
            "language_origin": "Old English",
            "source_difficulty": "Three Bee"
        }
    }
    
    # Combined word errors in this batch that need special handling
    combined_word_errors = [
        "squabblingscuba"
    ]
    
    # Read input file
    print("Processing 50 words from batch 167...")
    
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
    
    print(f"\nBatch 167 processing complete!")
    print(f"Successfully processed {len(output_data)}/50 words")
    print(f"Output saved to: {output_file}")
    print(f"\nCombined word errors detected: {len(combined_errors_found)}")
    for error in combined_errors_found:
        print(f"  - {error}")

if __name__ == "__main__":
    main()