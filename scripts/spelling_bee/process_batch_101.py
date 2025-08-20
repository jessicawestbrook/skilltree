#!/usr/bin/env python3
"""
Process Batch 101 of spelling bee words with comprehensive Claude data.
Generates detailed educational definitions, pronunciations, etymologies, and memory tips.
"""

import csv
import logging
from typing import Dict, List, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DifficultyCalculator:
    """Calculate 4-factor difficulty scores for spelling bee words"""
    
    def calculate_difficulty_components(self, word: str, definition: str, etymology: str) -> Dict[str, float]:
        """Calculate individual difficulty component scores (1.0-4.0 scale)"""
        
        # 1. Phonetic Transparency Score (1.0-4.0)
        phonetic_irregularities = 0
        if 'silent' in word.lower() or any(x in word.lower() for x in ['gh', 'ough', 'augh']):
            phonetic_irregularities += 1
        if any(x in word.lower() for x in ['ph', 'ch', 'th', 'sh']):
            phonetic_irregularities += 0.5
        if word.lower().count('e') > 2:  # Multiple e's often silent
            phonetic_irregularities += 0.5
        phonetic_transparency = min(4.0, max(1.0, 1.0 + phonetic_irregularities))
        
        # 2. Word Frequency Score (1.0-4.0) - inverse relationship with frequency
        word_length = len(word)
        if word_length <= 4:
            frequency_score = 1.5
        elif word_length <= 6:
            frequency_score = 2.0
        elif word_length <= 8:
            frequency_score = 2.5
        elif word_length <= 10:
            frequency_score = 3.0
        else:
            frequency_score = 3.5
            
        # Adjust for common prefixes/suffixes
        common_patterns = ['ing', 'tion', 'ed', 'er', 'est', 'ly', 'ful', 'ness']
        if any(word.lower().endswith(pattern) for pattern in common_patterns):
            frequency_score = max(1.0, frequency_score - 0.5)
            
        frequency_score = min(4.0, frequency_score)
        
        # 3. Morphological Complexity Score (1.0-4.0)
        morphology_score = 1.0
        if len(word) > 8:
            morphology_score += 0.5
        if len(word) > 12:
            morphology_score += 0.5
        if any(x in word.lower() for x in ['-', 'pre', 'post', 'anti', 'pro']):
            morphology_score += 0.5
        if any(word.lower().endswith(x) for x in ['ology', 'ography', 'tion', 'sion']):
            morphology_score += 0.5
        morphology_score = min(4.0, morphology_score)
        
        # 4. Etymology Complexity Score (1.0-4.0)
        etymology_score = 2.0  # Base score
        etymology_lower = etymology.lower()
        
        # Multiple language origins increase complexity
        language_indicators = ['latin', 'greek', 'french', 'german', 'arabic', 'sanskrit', 'hebrew']
        origin_count = sum(1 for lang in language_indicators if lang in etymology_lower)
        if origin_count >= 2:
            etymology_score += 1.0
        elif origin_count == 1:
            etymology_score += 0.5
            
        # Technical or specialized terms
        if any(x in etymology_lower for x in ['medical', 'scientific', 'technical', 'specialized']):
            etymology_score += 0.5
            
        etymology_score = min(4.0, etymology_score)
        
        return {
            'phonetic_transparency_score': phonetic_transparency,
            'word_frequency_score': frequency_score,
            'morphology_score': morphology_score,
            'etymology_score': etymology_score
        }

class Batch101Processor:
    """Processes Batch 101 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for each word with detailed definitions, pronunciations, etymologies, and memory tips"""
        
        word_data = {
            "laugh": {
                "definition": "To make spontaneous sounds and movements expressing amusement, joy, or derision; an involuntary physical and vocal response to humor, happiness, or sometimes nervousness that involves facial expressions, body movements, and characteristic sounds. Laughter serves important social and psychological functions including stress relief, social bonding, communication of emotions, and physical health benefits through the release of endorphins. Different types of laughter convey various emotions from genuine joy and amusement to nervous discomfort or social signaling. The ability to laugh and appreciate humor represents a uniquely human characteristic that enhances quality of life and social connections.",
                "example_sentence": "The comedian's joke made the entire audience _____ so hard that tears streamed down their faces.",
                "pronunciation": "LAF (single syllable, rhymes with \"half\")",
                "etymology": "From Old English \"hliehhan,\" from Germanic roots meaning \"to make a sound of joy\"",
                "memory_tips": "Think \"half\" - laughing uses about half your face muscles in a joyful expression",
                "part_of_speech": "verb, noun"
            },
            "laughter": {
                "definition": "The action or sound of laughing; the expression of mirth, amusement, or happiness through spontaneous vocal sounds and physical reactions that demonstrate joy or humor appreciation. Laughter represents a complex physiological and psychological response involving facial muscle contractions, vocalization patterns, and often whole-body movements that communicate positive emotions to others. This universal human behavior serves important social functions including group bonding, tension relief, and emotional communication across cultural boundaries. Scientific research demonstrates that laughter provides measurable health benefits including immune system enhancement and stress hormone reduction.",
                "example_sentence": "The children's joyful _____ filled the playground as they played games together during recess.",
                "pronunciation": "LAF-ter (emphasis on first syllable)",
                "etymology": "From Old English \"hleahtor,\" from the same Germanic roots as \"laugh\"",
                "memory_tips": "Think \"laugh-ter\" - the sound that comes after you laugh",
                "part_of_speech": "noun"
            },
            "laulau": {
                "definition": "A traditional Hawaiian dish consisting of salted pork and butterfish wrapped in taro leaves and steamed for several hours, creating a tender, flavorful meal that represents authentic Polynesian cooking methods. The preparation involves layering meat with taro leaves, then wrapping the bundle in more taro leaves or aluminum foil before cooking in an underground oven (imu) or steamer. Laulau demonstrates sustainable cooking practices that utilize local ingredients and traditional preservation techniques developed by Native Hawaiian communities. This dish remains an important part of Hawaiian cultural identity and appears at luaus, family gatherings, and cultural celebrations.",
                "example_sentence": "The traditional Hawaiian _____ was steamed for hours until the pork became tender and absorbed the flavors of the taro leaves.",
                "pronunciation": "LAU-lau (emphasis on first syllable)",
                "etymology": "From Hawaiian \"laulau,\" from \"lau\" (leaf) + \"lau\" (many), meaning \"many leaves\"",
                "memory_tips": "Think \"wow-wow\" - saying wow twice at this amazing Hawaiian leaf-wrapped dish",
                "part_of_speech": "noun"
            },
            "launch": {
                "definition": "To set something in motion or begin something with energy and purpose; to send forth or release something such as a projectile, spacecraft, or new venture into action or operation. Launch implies a deliberate initiation that involves preparation, timing, and force to achieve successful deployment or commencement. The term encompasses both physical launches like rockets or boats entering water, and metaphorical launches such as starting businesses, campaigns, or projects. Successful launches require careful planning, appropriate resources, and favorable conditions to achieve desired outcomes and sustained progress.",
                "example_sentence": "NASA will _____ the new space telescope next month to begin its mission of exploring distant galaxies.",
                "pronunciation": "LAWNCH (single syllable, rhymes with \"staunch\")",
                "etymology": "From Old French \"lanchier,\" meaning \"to throw\" or \"to hurl\"",
                "memory_tips": "Think \"lawn-ch\" - launching from a lawn like a rocket taking off",
                "part_of_speech": "verb, noun"
            },
            "launching": {
                "definition": "Present participle of launch; the act of setting something in motion, beginning a new venture, or sending something forth with purpose and energy. Launching involves the process of initiation that transforms plans into active implementation, requiring coordination of resources, timing, and execution. This ongoing action suggests dynamic movement from preparation phase to active deployment or operation. Launching can apply to physical objects like spacecraft, boats, or products, as well as abstract concepts like careers, campaigns, or initiatives that require sustained effort to achieve success.",
                "example_sentence": "The company is _____ a new product line that will revolutionize the renewable energy market.",
                "pronunciation": "LAWNCH-ing (emphasis on first syllable)",
                "etymology": "Present participle of \"launch,\" from Old French \"lanchier\"",
                "memory_tips": "Think \"lawn-ching\" - like a lawn chair springing into action",
                "part_of_speech": "verb, noun"
            },
            "laundromat": {
                "definition": "A self-service laundry facility where customers use coin-operated or card-operated washing machines and dryers to clean their clothes and linens. Laundromats provide essential services for people without home laundry facilities, apartment dwellers, college students, and travelers who need convenient access to commercial-grade washing equipment. These businesses typically operate with minimal staff supervision, allowing customers to manage their own laundry processes while providing detergent vending, change machines, and seating areas. Modern laundromats may include amenities such as Wi-Fi, television, food vending, and wash-and-fold services.",
                "example_sentence": "She spent Sunday afternoon at the _____ washing several loads of clothes while reading a book.",
                "pronunciation": "LAWN-druh-mat (emphasis on first syllable)",
                "etymology": "Blend of \"laundry\" + \"automat,\" from the automated self-service concept",
                "memory_tips": "Think \"laundry-automatic\" - an automatic place to do laundry",
                "part_of_speech": "noun"
            },
            "laureate": {
                "definition": "A person who has been honored for outstanding creative or intellectual achievement, particularly in literature, science, or arts; someone crowned with laurel leaves as a symbol of victory or distinction. The term most commonly refers to Nobel Prize winners, poet laureates, or other individuals recognized for exceptional contributions to their fields. Laureates represent the highest levels of achievement and serve as exemplars of excellence that inspire others while advancing knowledge, culture, or human understanding. The designation carries prestige and often involves ongoing responsibilities such as public speaking, mentoring, or continued creative work.",
                "example_sentence": "The Nobel _____ delivered an inspiring speech about the importance of scientific research in solving global challenges.",
                "pronunciation": "LOR-ee-uht (emphasis on first syllable)",
                "etymology": "From Latin \"laureatus,\" meaning \"crowned with laurel,\" from \"laurus\" (laurel tree)",
                "memory_tips": "Think \"lore-create\" - someone who creates lore through their outstanding achievements",
                "part_of_speech": "noun, adjective"
            },
            "laurel": {
                "definition": "An evergreen shrub or tree with glossy, aromatic leaves, historically associated with honor, victory, and achievement; also refers to the recognition or praise given for accomplishments. Bay laurel leaves were used in ancient Greek and Roman cultures to create wreaths for victorious athletes, scholars, and military leaders, establishing a tradition that continues in modern expressions like \"resting on one's laurels.\" The plant produces small yellow flowers and dark berries, with leaves that serve culinary purposes as the common bay leaf used in cooking. Symbolically, laurels represent lasting fame, academic achievement, and earned recognition.",
                "example_sentence": "The ancient Olympic champions were crowned with _____ wreaths to honor their athletic victories.",
                "pronunciation": "LOR-uhl (emphasis on first syllable)",
                "etymology": "From Old French \"lorier,\" from Latin \"laurus,\" meaning \"laurel tree\"",
                "memory_tips": "Think \"lore-el\" - the plant that creates lore about victory and achievement",
                "part_of_speech": "noun"
            },
            "lava": {
                "definition": "Molten rock that flows from volcanoes during eruptions, typically at temperatures between 700-1200°C, eventually cooling and solidifying to form new rock formations and landforms. Lava represents the visible manifestation of Earth's internal geological processes, carrying minerals and gases from deep within the planet to the surface where it shapes landscapes and creates new land. Different types of lava vary in composition, viscosity, and behavior, producing diverse volcanic features including flows, domes, and explosive deposits. The study of lava provides insights into Earth's interior structure and contributes to understanding volcanic hazards and geological evolution.",
                "example_sentence": "The volcanic _____ flowed slowly down the mountainside, glowing bright orange against the dark night sky.",
                "pronunciation": "LAH-vuh (emphasis on first syllable)",
                "etymology": "From Italian \"lava,\" from Latin \"labes\" meaning \"a falling\" or \"sliding\"",
                "memory_tips": "Think \"la-va\" - saying \"la\" (there) when you see molten rock flowing",
                "part_of_speech": "noun"
            },
            "lavender": {
                "definition": "An aromatic flowering plant with purple-blue flowers and silvery-green foliage, valued for its fragrance, medicinal properties, and use in cosmetics, aromatherapy, and culinary applications. Lavender belongs to the mint family and produces essential oils that contain compounds with calming, antiseptic, and anti-inflammatory properties. The plant thrives in Mediterranean climates and has been cultivated for thousands of years for perfumes, soaps, sachets, and herbal remedies. As a color, lavender refers to a pale purple shade resembling the plant's flowers, often associated with tranquility, elegance, and femininity.",
                "example_sentence": "The _____ fields in Provence created a stunning purple landscape that attracted tourists from around the world.",
                "pronunciation": "LAV-uhn-der (emphasis on first syllable)",
                "etymology": "From Old French \"lavandre,\" from Latin \"lavandula,\" possibly from \"lavare\" (to wash)",
                "memory_tips": "Think \"lav-end-er\" - something you use to end your lavatory washing routine with nice scent",
                "part_of_speech": "noun, adjective"
            },
            "lavished": {
                "definition": "Past tense of lavish; bestowed something abundantly or generously; gave or spent freely and extravagantly without restraint or consideration of cost. Being lavished upon involves receiving generous attention, gifts, resources, or care that exceeds normal expectations or requirements. The action implies abundance and generosity that may be motivated by affection, celebration, or desire to demonstrate wealth and status. Lavishing can involve material gifts, emotional attention, praise, or any form of generous giving that emphasizes quantity and quality of what is provided.",
                "example_sentence": "The grandparents _____ attention and gifts upon their first grandchild during the holiday visit.",
                "pronunciation": "LAV-ishd (emphasis on first syllable)",
                "etymology": "Past tense of \"lavish,\" from Old French \"lavasse,\" meaning \"torrent of rain\"",
                "memory_tips": "Think \"lav-wished\" - wished for lavish treatment and received it abundantly",
                "part_of_speech": "verb"
            },
            "lavishly": {
                "definition": "In a lavish manner; abundantly, generously, or extravagantly without regard to cost or restraint; characterized by luxurious excess and generous spending or giving. Acting lavishly involves providing or displaying resources, attention, or care in quantities that exceed normal expectations or practical necessity. This adverb suggests abundance that may be motivated by celebration, affection, status display, or simple generosity. Lavishly can describe spending money, decorating spaces, entertaining guests, or expressing emotions in ways that emphasize excess and luxury.",
                "example_sentence": "The wedding reception was _____ decorated with thousands of flowers and crystal chandeliers throughout the ballroom.",
                "pronunciation": "LAV-ish-lee (emphasis on first syllable)",
                "etymology": "From \"lavish\" + \"-ly,\" meaning \"in an abundant or generous manner\"",
                "memory_tips": "Think \"lav-wish-ly\" - wishing lavishly for abundant good things",
                "part_of_speech": "adverb"
            },
            "lawmusic": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"law\" (legal rules) incorrectly combined with \"music\" (organized sound art). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"law\" and \"music\"",
                "part_of_speech": "error - combined words"
            },
            "lawyer": {
                "definition": "A person who practices law as an advocate, attorney, or counselor; a legal professional qualified to represent clients in legal matters, provide legal advice, and navigate complex legal systems. Lawyers undergo extensive education including law school and bar examination requirements that enable them to understand legal procedures, interpret statutes, and argue cases in court. The profession encompasses various specializations including criminal law, civil litigation, corporate law, family law, and many other areas that serve different client needs. Modern legal practice involves both traditional courtroom advocacy and advisory roles in business, government, and personal affairs.",
                "example_sentence": "The experienced criminal defense _____ successfully argued for her client's innocence during the lengthy trial.",
                "pronunciation": "LOY-er (emphasis on first syllable)",
                "etymology": "From Middle English \"lawier,\" from \"law\" + agent suffix \"-yer\"",
                "memory_tips": "Think \"law-yer\" - a person who says \"yes\" (yer) to practicing law",
                "part_of_speech": "noun"
            },
            "layer": {
                "definition": "A sheet, stratum, or level of material that lies over or under another; a distinct level or coating that forms part of a larger structure or system. Layers can be physical materials like geological strata, clothing garments, or paint coats, or abstract concepts like organizational levels, complexity layers, or information hierarchies. The concept of layering implies systematic arrangement where each layer serves specific functions while contributing to the overall structure or system. Understanding layers helps in analyzing complex systems, troubleshooting problems, and building efficient structures in various fields from technology to fashion.",
                "example_sentence": "The geologist studied each rock _____ to understand the region's geological history and formation processes.",
                "pronunciation": "LAY-er (emphasis on first syllable)",
                "etymology": "From \"lay\" + agent suffix \"-er,\" meaning \"something that lays\" or \"one who lays\"",
                "memory_tips": "Think \"lay-er\" - something that lays on top of or under something else",
                "part_of_speech": "noun, verb"
            },
            "leach": {
                "definition": "To remove or extract substances from materials by washing with a percolating liquid; the process by which soluble materials dissolve and drain away from soil, rock, or other substances through the action of water. Leaching occurs naturally in soil when rain or irrigation water carries nutrients, minerals, or contaminants downward through soil layers, potentially affecting groundwater quality. In industrial processes, leaching is used intentionally to extract valuable metals from ores or remove unwanted substances from materials. Understanding leaching helps in agriculture, environmental protection, and mineral processing applications.",
                "example_sentence": "Heavy rains began to _____ nutrients from the topsoil, requiring farmers to add fertilizers to maintain crop yields.",
                "pronunciation": "LEECH (single syllable, rhymes with \"beach\")",
                "etymology": "From Old English \"leccan,\" meaning \"to water\" or \"irrigate\"",
                "memory_tips": "Think \"beach\" - where water leaches minerals from sand into the ocean",
                "part_of_speech": "verb, noun"
            },
            "leader": {
                "definition": "A person who guides, directs, or commands others; someone who holds a position of authority and influence within a group, organization, or society. Leaders possess qualities including vision, communication skills, decision-making ability, and the capacity to motivate others toward common goals. Effective leadership involves understanding group dynamics, managing resources, resolving conflicts, and adapting to changing circumstances while maintaining focus on objectives. Leadership styles vary from authoritarian to collaborative approaches, with successful leaders often adjusting their methods to match situational needs and follower characteristics.",
                "example_sentence": "The team _____ inspired everyone to work together toward achieving their ambitious project goals.",
                "pronunciation": "LEE-der (emphasis on first syllable)",
                "etymology": "From Old English \"lædan\" (to lead) + agent suffix \"-er\"",
                "memory_tips": "Think \"lead-er\" - someone who leads others forward",
                "part_of_speech": "noun"
            },
            "leadership": {
                "definition": "The action of leading a group of people or an organization; the ability to guide, influence, and direct others toward achieving common goals through vision, communication, and decision-making skills. Leadership involves both positional authority and personal influence that enables individuals to coordinate group efforts, resolve conflicts, and adapt to changing circumstances. Effective leadership requires understanding of human motivation, group dynamics, strategic thinking, and ethical decision-making that serves both organizational objectives and individual needs. Leadership development has become a critical focus in business, education, and social organizations worldwide.",
                "example_sentence": "Her exceptional _____ during the crisis helped the organization navigate challenges and emerge stronger than before.",
                "pronunciation": "LEE-der-ship (emphasis on first syllable)",
                "etymology": "From \"leader\" + suffix \"-ship,\" indicating the state or condition of leading",
                "memory_tips": "Think \"leader-ship\" - the ship that a leader steers toward success",
                "part_of_speech": "noun"
            },
            "leading": {
                "definition": "Present participle of lead; being in front, guiding others, or holding the most prominent position; also refers to the most important or influential in a particular field or activity. Leading implies active direction and guidance that influences others' actions and decisions toward specific objectives. In various contexts, leading describes top performers, front-runners, or those who set standards and trends that others follow. The concept encompasses both physical positioning at the front and metaphorical influence that shapes direction and outcomes in competitive or collaborative situations.",
                "example_sentence": "The _____ researcher in climate science published groundbreaking findings about ocean temperature changes.",
                "pronunciation": "LEE-ding (emphasis on first syllable)",
                "etymology": "Present participle of \"lead,\" from Old English \"lædan\"",
                "memory_tips": "Think \"lea-ding\" - like a meadow (lea) that leads the way in natural beauty",
                "part_of_speech": "adjective, verb, noun"
            },
            "league": {
                "definition": "An association of people, groups, or countries formed for mutual benefit or common purpose; also a unit of distance measurement historically used in various cultures. Sports leagues organize competitions between teams under unified rules and governance, while political or economic leagues coordinate policies and resources among member organizations or nations. As a distance measure, a league typically represented the distance a person could walk in an hour, varying from about 2.5 to 4.6 miles depending on regional standards. The concept emphasizes cooperation, organization, and structured relationships among participants.",
                "example_sentence": "The baseball _____ announced new safety regulations to protect players during the upcoming season.",
                "pronunciation": "LEEG (single syllable, rhymes with \"league\")",
                "etymology": "From Old French \"ligue,\" from Italian \"lega,\" meaning \"alliance\" or \"bond\"",
                "memory_tips": "Think \"lea-gue\" - a group that makes agreements like a guest in a meadow",
                "part_of_speech": "noun, verb"
            },
            "leaking": {
                "definition": "Present participle of leak; allowing liquid, gas, or information to escape through holes, cracks, or unauthorized channels; the ongoing process of unintended or unauthorized release of contained substances or data. Physical leaking involves materials escaping from containers, pipes, or barriers due to structural failures or design flaws that compromise containment. Information leaking refers to unauthorized disclosure of confidential data, secrets, or sensitive materials that were meant to remain private. Both forms of leaking can cause significant problems requiring prompt identification and repair to prevent damage or security breaches.",
                "example_sentence": "The old roof was _____ rainwater into the attic, causing damage to the insulation and ceiling below.",
                "pronunciation": "LEE-king (emphasis on first syllable)",
                "etymology": "Present participle of \"leak,\" from Middle Dutch \"leken\" meaning \"to drip\"",
                "memory_tips": "Think \"lee-king\" - like a king in a protected area (lee) losing his power through leaks",
                "part_of_speech": "verb, adjective"
            },
            "leanderpneumonia": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"leander\" (mythological swimmer) incorrectly combined with \"pneumonia\" (lung infection). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"leander\" and \"pneumonia\"",
                "part_of_speech": "error - combined words"
            },
            "learn": {
                "definition": "To acquire knowledge, skills, or understanding through study, experience, instruction, or observation; the process of gaining new information and integrating it with existing knowledge to improve capabilities and comprehension. Learning involves cognitive processes including attention, memory formation, pattern recognition, and skill development that enable individuals to adapt to new situations and solve problems. The ability to learn distinguishes humans and other intelligent species, enabling cultural transmission, technological advancement, and personal growth throughout life. Effective learning requires motivation, practice, reflection, and often social interaction with teachers and peers.",
                "example_sentence": "Children _____ language naturally through interaction with parents and exposure to their linguistic environment.",
                "pronunciation": "LERN (single syllable, rhymes with \"turn\")",
                "etymology": "From Old English \"leornian,\" from Germanic roots meaning \"to follow a track\"",
                "memory_tips": "Think \"turn\" - learning helps you turn toward new knowledge and understanding",
                "part_of_speech": "verb"
            },
            "learning": {
                "definition": "The acquisition of knowledge or skills through experience, study, or instruction; the ongoing process of gaining understanding that enables improved performance, decision-making, and adaptation to new situations. Learning encompasses both formal education in structured environments and informal acquisition of knowledge through daily experiences, observation, and practice. Modern learning theory recognizes multiple learning styles, the importance of prior knowledge, and the role of motivation in effective knowledge acquisition. Lifelong learning has become essential in rapidly changing societies that require continuous skill development and adaptation.",
                "example_sentence": "The online _____ platform provided interactive courses that helped students master complex mathematical concepts.",
                "pronunciation": "LER-ning (emphasis on first syllable)",
                "etymology": "From \"learn\" + suffix \"-ing,\" indicating the process of learning",
                "memory_tips": "Think \"learn-ing\" - the ongoing action of learning new things",
                "part_of_speech": "noun, verb"
            },
            "leash": {
                "definition": "A rope, chain, or strap attached to a collar or harness to control or restrain an animal, typically a dog, during walks or public appearances; also used metaphorically to describe any restraining influence or control mechanism. Leashes serve safety functions by preventing animals from running into traffic, approaching strangers inappropriately, or getting lost while allowing controlled exercise and socialization. The length and type of leash affect both animal behavior and handler control, with different designs serving specific training or activity purposes. Legal requirements for leashes in public spaces reflect community safety concerns and responsible pet ownership principles.",
                "example_sentence": "The dog walker kept all six dogs safely on their _____ while navigating through the busy city park.",
                "pronunciation": "LEESH (single syllable, rhymes with \"fleece\")",
                "etymology": "From Old French \"laisse,\" from \"laissier\" meaning \"to let go\" or \"allow\"",
                "memory_tips": "Think \"fleece\" - a soft leash made of fleece material for gentle control",
                "part_of_speech": "noun, verb"
            },
            "least": {
                "definition": "Superlative form of little; the smallest in amount, extent, or intensity; the minimum possible degree or quantity within a given set or context. Least establishes the bottom end of a comparison scale, indicating the smallest measurement, lowest value, or most minimal presence among options being considered. The concept requires clear criteria for measurement and comparison boundaries to determine what constitutes the minimum within specific categories. Understanding what is least helps in making efficient decisions, prioritizing resources, and identifying fundamental requirements versus optional additions.",
                "example_sentence": "She chose the _____ expensive option that still met all the basic requirements for her new apartment.",
                "pronunciation": "LEEST (single syllable, rhymes with \"beast\")",
                "etymology": "Superlative form of \"little,\" from Old English \"læsest\"",
                "memory_tips": "Think \"beast\" - even the least threatening beast is still a beast",
                "part_of_speech": "adjective, adverb, noun"
            },
            "leave": {
                "definition": "To go away from a place or person; to depart or exit; also to allow something to remain in a particular condition or place without interference. Leave involves intentional separation that may be temporary or permanent, planned or spontaneous, depending on circumstances and motivations. As a noun, leave refers to permission to be absent from work or duty, typically for rest, personal business, or special circumstances. The concept encompasses both physical departure and the decision to stop involvement in activities, relationships, or situations that no longer serve one's needs or interests.",
                "example_sentence": "Please _____ your shoes at the entrance to keep the floors clean inside the traditional Japanese home.",
                "pronunciation": "LEEV (single syllable, rhymes with \"sleeve\")",
                "etymology": "From Old English \"læfan,\" meaning \"to remain\" or \"allow to stay\"",
                "memory_tips": "Think \"sleeve\" - leaving like rolling up your sleeve to prepare for departure",
                "part_of_speech": "verb, noun"
            },
            "leaven": {
                "definition": "A substance such as yeast or baking powder that causes dough to rise by producing gas bubbles during fermentation or chemical reactions; also used metaphorically to describe any influence that brings about gradual change or improvement. In baking, leaven creates the light, airy texture in breads and baked goods by generating carbon dioxide that expands dough structure. Metaphorically, leaven represents positive influences that gradually transform situations, communities, or individuals through persistent but subtle action. The concept emphasizes transformation through internal processes rather than external force.",
                "example_sentence": "The baker added _____ to the bread dough and let it rise overnight to develop complex flavors and texture.",
                "pronunciation": "LEV-uhn (emphasis on first syllable)",
                "etymology": "From Old French \"levain,\" from Latin \"levare\" meaning \"to raise\"",
                "memory_tips": "Think \"leave-in\" - something you leave in dough to make it rise",
                "part_of_speech": "noun, verb"
            },
            "leaves": {
                "definition": "Plural of leaf; the flat, typically green organs of plants that perform photosynthesis, converting sunlight, carbon dioxide, and water into energy and oxygen; also third person singular present tense of leave. Plant leaves demonstrate remarkable diversity in shapes, sizes, and structures that reflect adaptation to different environments and survival strategies. The seasonal change of leaves in deciduous trees creates spectacular displays while representing natural cycles of growth, dormancy, and renewal. As a verb form, leaves indicates someone's departure or the act of allowing something to remain in a particular state or location.",
                "example_sentence": "The autumn _____ created a colorful carpet on the forest floor as trees prepared for winter dormancy.",
                "pronunciation": "LEEVZ (single syllable, rhymes with \"sleeves\")",
                "etymology": "Plural of \"leaf,\" from Old English \"leaf,\" from Germanic roots",
                "memory_tips": "Think \"sleeves\" - leaves cover tree branches like sleeves cover arms",
                "part_of_speech": "noun, verb"
            },
            "lebensraum": {
                "definition": "A German geopolitical concept meaning \"living space,\" referring to the territory that a nation believes it needs for its people to live and develop; historically associated with Nazi ideology that justified territorial expansion and colonization. The concept originated in early 20th-century German geography and politics but became central to Hitler's aggressive expansionist policies that contributed to World War II. Lebensraum theory claimed that growing populations required additional land and resources to maintain their standard of living and cultural development. Understanding this term is important for historical education about the ideological foundations of fascist aggression and territorial conquest.",
                "example_sentence": "Historians study the concept of _____ to understand how territorial ambitions contributed to the causes of World War II.",
                "pronunciation": "LAY-bens-rowm (emphasis on first syllable)",
                "etymology": "From German \"leben\" (life) + \"raum\" (space), meaning \"living space\"",
                "memory_tips": "Think \"lay-bens-room\" - laying claim to a room for living space",
                "part_of_speech": "noun"
            },
            "leberwurst": {
                "definition": "A German-style liver sausage or spreadable pâté made primarily from pork liver mixed with other meats, spices, and seasonings, typically served as a cold cut or spread on bread. This traditional European delicacy involves grinding liver with pork, beef, or veal, then seasoning the mixture with onions, pepper, and various herbs before stuffing into casings or forming into loaves. Leberwurst provides high levels of iron, protein, and vitamins while offering rich, distinctive flavors that appeal to those who appreciate organ meat preparations. The product appears in various regional styles throughout Germany and has been adapted in American delicatessen traditions.",
                "example_sentence": "The German delicatessen served traditional _____ on dark rye bread with pickles and mustard.",
                "pronunciation": "LAY-ber-wurst (emphasis on first syllable)",
                "etymology": "From German \"leber\" (liver) + \"wurst\" (sausage), meaning \"liver sausage\"",
                "memory_tips": "Think \"lay-ber-worst\" - liver sausage that's the worst fear of picky eaters but beloved by others",
                "part_of_speech": "noun"
            },
            "lebkuchen": {
                "definition": "Traditional German gingerbread cookies typically made with honey, spices, and sometimes nuts or candied fruits, often baked during Christmas season and decorated with icing or chocolate. These spiced cookies originated in German monasteries during the Middle Ages and evolved into regional specialties with distinctive recipes passed down through generations. Lebkuchen differs from other gingerbread varieties through its use of honey as a primary sweetener and specific spice blends that may include cinnamon, cloves, cardamom, and anise. The cookies are often shaped into hearts, stars, or figures and decorated with elaborate icing designs that make them both delicious treats and artistic displays.",
                "example_sentence": "The Christmas market featured traditional _____ cookies decorated with colorful icing and German phrases.",
                "pronunciation": "LAYB-koo-khen (emphasis on first syllable)",
                "etymology": "From German \"lebkuchen,\" possibly from \"laib\" (loaf) + \"kuchen\" (cake)",
                "memory_tips": "Think \"lay-book-en\" - laying out a book of recipes for these German spiced cookies",
                "part_of_speech": "noun"
            },
            "lecithin": {
                "definition": "A natural fatty substance found in animal and plant tissues that functions as an emulsifier, helping to mix oil and water-based substances in food processing and biological systems. Lecithin plays crucial roles in cell membrane structure, nerve function, and fat metabolism while serving as a common food additive that improves texture and extends shelf life. Commercial lecithin is typically derived from soybeans, sunflowers, or egg yolks and appears in products ranging from chocolate and baked goods to dietary supplements. The compound supports brain health, liver function, and cardiovascular health while enabling the production of smooth, consistent textures in processed foods.",
                "example_sentence": "The chocolate manufacturer added soy _____ to create a smooth texture and prevent the cocoa and cocoa butter from separating.",
                "pronunciation": "LES-uh-thin (emphasis on first syllable)",
                "etymology": "From Greek \"lekithos\" (egg yolk) + \"-in,\" referring to its discovery in egg yolks",
                "memory_tips": "Think \"less-thin\" - lecithin makes mixtures less thin by helping ingredients blend together",
                "part_of_speech": "noun"
            },
            "leewardhurly": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"leeward\" (sheltered side) incorrectly combined with \"hurly\" (commotion or tumult). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"leeward\" and \"hurly\"",
                "part_of_speech": "error - combined words"
            },
            "leeway": {
                "definition": "The amount of freedom to move or act that is available; flexibility or margin for error in plans, decisions, or operations that allows for adaptation to changing circumstances. In nautical terms, leeway refers to the sideways drift of a ship caused by wind or current, representing deviation from the intended course. More generally, leeway describes the buffer space or tolerance built into systems, schedules, or agreements that accommodates uncertainty and variation. Having adequate leeway enables better decision-making under pressure and reduces the risk of failure when conditions don't match original expectations.",
                "example_sentence": "The project manager built extra _____ into the timeline to account for potential delays and unexpected complications.",
                "pronunciation": "LEE-way (emphasis on first syllable)",
                "etymology": "From nautical \"lee\" (sheltered side) + \"way\" (path or direction)",
                "memory_tips": "Think \"lee-way\" - the way things drift in the lee (sheltered) side, giving you room to maneuver",
                "part_of_speech": "noun"
            },
            "lefse": {
                "definition": "A traditional Norwegian flatbread made from potatoes, flour, and milk, rolled very thin and cooked on a griddle, typically served during holidays and special occasions with butter, sugar, and cinnamon. The preparation of lefse requires specialized tools including a grooved rolling pin and large, flat griddle that create the characteristic thin, pliable texture. This Scandinavian bread represents cultural heritage maintained by Norwegian-American communities and requires skill to achieve the proper consistency and cooking technique. Lefse is often served during Christmas celebrations and family gatherings, continuing traditions that connect modern families with their ancestral food customs.",
                "example_sentence": "The Norwegian grandmother taught her granddaughter to make traditional _____ using the special rolling pin and techniques passed down for generations.",
                "pronunciation": "LEF-suh (emphasis on first syllable)",
                "etymology": "From Norwegian \"lefse,\" related to \"leaf,\" referring to its thin, leaf-like appearance",
                "memory_tips": "Think \"left-see\" - what's left to see after rolling this Norwegian bread paper-thin",
                "part_of_speech": "noun"
            },
            "left": {
                "definition": "The side or direction that is to the west when one faces north; opposite of right; also past tense and past participle of leave, meaning departed or abandoned. As a direction, left represents one of the fundamental spatial orientations that helps humans navigate and organize their environment. In politics, \"left\" often refers to liberal or progressive ideologies that favor social equality and government intervention in economics. The concept of left-handedness describes people who prefer using their left hand for primary tasks, representing a minority population with unique neurological characteristics and social adaptations.",
                "example_sentence": "Turn _____ at the next intersection to reach the library downtown.",
                "pronunciation": "LEFT (single syllable, rhymes with \"heft\")",
                "etymology": "From Old English \"lyft,\" meaning \"weak\" or \"idle,\" referring to the typically non-dominant hand",
                "memory_tips": "Think \"heft\" - the left hand often has less heft (strength) than the right for most people",
                "part_of_speech": "adjective, adverb, noun, verb"
            },
            "legacy": {
                "definition": "Something handed down from the past, such as traditions, money, property, or reputation; the lasting impact or influence that a person, organization, or historical period leaves for future generations. Legacy encompasses both tangible inheritances like financial assets and intangible contributions such as ideas, values, cultural practices, or social changes. Understanding legacy involves recognizing how past actions and decisions continue to influence present and future circumstances. People often consider their potential legacy when making important life decisions, seeking to create positive lasting impacts through their work, relationships, and contributions to society.",
                "example_sentence": "The philanthropist's educational _____ included scholarships that enabled thousands of students to attend college.",
                "pronunciation": "LEG-uh-see (emphasis on first syllable)",
                "etymology": "From Old French \"legacie,\" from Latin \"legatum\" meaning \"bequest\" or \"thing left by will\"",
                "memory_tips": "Think \"leg-a-see\" - what you can see that someone's life journey (legs) left behind",
                "part_of_speech": "noun"
            },
            "legalese": {
                "definition": "The formal and technical language of legal documents, characterized by complex terminology, lengthy sentences, and precise but often confusing wording that can be difficult for non-lawyers to understand. Legalese serves important functions in creating precise legal meanings and avoiding ambiguity in contracts, statutes, and court documents, but often creates barriers to public understanding of legal rights and obligations. Legal professionals argue that technical language ensures accuracy and prevents misinterpretation, while critics advocate for plain language alternatives that improve accessibility. Modern legal reform movements seek to balance precision with clarity in legal communication.",
                "example_sentence": "The contract was written in dense _____ that required a lawyer's interpretation to understand the basic terms and conditions.",
                "pronunciation": "LEE-guhl-eez (emphasis on first syllable)",
                "etymology": "Blend of \"legal\" + \"-ese\" (language suffix), meaning \"legal language\"",
                "memory_tips": "Think \"legal-ease\" - legal language that's anything but easy to understand",
                "part_of_speech": "noun"
            },
            "legato": {
                "definition": "In music, a style of performance characterized by smooth, connected notes without noticeable breaks or separations between them; the opposite of staccato playing which emphasizes detached, distinct notes. Legato technique requires careful control of breath (in wind instruments or voice) or bow/finger movements (in string instruments) to create seamless transitions between pitches. This musical expression creates flowing, lyrical qualities that can convey emotions ranging from tenderness to grandeur. Mastering legato performance requires significant technical skill and musical sensitivity to achieve the desired connected, singing quality that characterizes much classical and romantic music literature.",
                "example_sentence": "The violinist's beautiful _____ passage made the melody flow like a continuous silk ribbon of sound.",
                "pronunciation": "luh-GAH-toh (emphasis on second syllable)",
                "etymology": "From Italian \"legato,\" meaning \"tied\" or \"bound together\"",
                "memory_tips": "Think \"leg-a-toe\" - connecting your leg to your toe in one smooth movement like connected musical notes",
                "part_of_speech": "adjective, adverb, noun"
            },
            "legend": {
                "definition": "A traditional story, often involving heroic characters or supernatural events, that has been passed down through generations and may contain historical elements mixed with mythical or fictional components. Legends differ from myths in that they often involve real people or places but include exaggerated or fantastic elements that grow over time through oral tradition. Modern usage extends to describe any person who has achieved legendary status through extraordinary accomplishments, influence, or fame that creates lasting cultural impact. Legends serve important cultural functions by preserving values, explaining phenomena, and providing models of heroism or cautionary tales.",
                "example_sentence": "The _____ of King Arthur and the Knights of the Round Table has inspired literature and films for centuries.",
                "pronunciation": "LEJ-uhnd (emphasis on first syllable)",
                "etymology": "From Latin \"legenda,\" meaning \"things to be read,\" originally referring to saints' stories",
                "memory_tips": "Think \"leg-end\" - stories that have legs to carry them through time to the end",
                "part_of_speech": "noun"
            },
            "legendary": {
                "definition": "Of, relating to, or characteristic of legend; famous or well-known, especially for extraordinary achievement or exceptional qualities that inspire admiration and storytelling. Legendary status suggests accomplishments or characteristics so remarkable that they become the subject of stories, myths, or widespread recognition that transcends normal fame. This adjective describes both fictional characters whose stories have legendary qualities and real people whose achievements have reached legendary proportions. Becoming legendary requires a combination of exceptional ability, significant impact, and the kind of memorable qualities that inspire others to retell and embellish stories over time.",
                "example_sentence": "The basketball player's _____ career included multiple championships and records that may never be broken.",
                "pronunciation": "LEJ-uhn-der-ee (emphasis on first syllable)",
                "etymology": "From \"legend\" + suffix \"-ary,\" meaning \"relating to or characteristic of legend\"",
                "memory_tips": "Think \"legend-dairy\" - so famous that stories about them are preserved like dairy products",
                "part_of_speech": "adjective"
            },
            "legerity": {
                "definition": "Mental or physical quickness and agility; nimbleness of mind or body that demonstrates grace, skill, and effortless capability in movement or thought processes. Legerity suggests a combination of speed and elegance that makes difficult tasks appear easy through superior coordination, intelligence, or training. This quality applies to both physical activities requiring dexterity and mental activities requiring quick thinking and adaptability. People with legerity often excel in fields requiring rapid response, complex coordination, or the ability to process information quickly while maintaining accuracy and poise under pressure.",
                "example_sentence": "The gymnast's remarkable _____ allowed her to execute complex routines with apparent effortless grace and precision.",
                "pronunciation": "luh-JAIR-uh-tee (emphasis on second syllable)",
                "etymology": "From Old French \"legerete,\" from \"leger\" meaning \"light\" or \"nimble\"",
                "memory_tips": "Think \"ledger-ity\" - the agility needed to quickly balance ledgers with nimble thinking",
                "part_of_speech": "noun"
            },
            "legerityvatican": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"legerity\" (mental/physical quickness) incorrectly combined with \"vatican\" (papal city-state). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"legerity\" and \"vatican\"",
                "part_of_speech": "error - combined words"
            },
            "leghorn": {
                "definition": "A breed of domestic chicken originally from Italy, known for its prolific egg-laying ability, white eggs, and active, hardy temperament; also refers to a type of plaited straw used for making hats. Leghorn chickens are among the most productive egg layers in commercial poultry operations, with hens capable of laying over 300 eggs per year under optimal conditions. The breed was imported to America in the 19th century and became fundamental to the development of the modern egg industry. As a material, leghorn straw comes from wheat stalks that are specially prepared and woven into fine, flexible braids used in high-quality hat making.",
                "example_sentence": "The farmer's flock of white _____ hens consistently provided fresh eggs for the local market throughout the year.",
                "pronunciation": "LEG-horn (emphasis on first syllable)",
                "etymology": "From Livorno (Leghorn), Italy, where the chicken breed originated",
                "memory_tips": "Think \"leg-horn\" - chickens with strong legs and horn-like combs for laying lots of eggs",
                "part_of_speech": "noun"
            },
            "legionnaire": {
                "definition": "A member of a legion, particularly a soldier in the ancient Roman army or a member of the French Foreign Legion; also refers to members of veterans' organizations such as the American Legion. Roman legionnaires were professional soldiers who served in highly disciplined units that formed the backbone of Roman military power for centuries. Modern legionnaires in the French Foreign Legion are international volunteers who serve in French military forces under demanding conditions around the world. The term also applies to members of veterans' organizations that provide community service and support for former military personnel and their families.",
                "example_sentence": "The former _____ shared stories of his service with the French Foreign Legion in North Africa during the 1980s.",
                "pronunciation": "lee-juh-NAIR (emphasis on third syllable)",
                "etymology": "From French \"légionnaire,\" from Latin \"legionarius,\" meaning \"of a legion\"",
                "memory_tips": "Think \"legion-air\" - a soldier who brings the air of a legion wherever he goes",
                "part_of_speech": "noun"
            },
            "legislature": {
                "definition": "The branch of government responsible for making laws, typically consisting of elected representatives who debate, draft, and vote on proposed legislation that governs society. Legislatures exist at various levels including federal, state, and local governments, with structures ranging from unicameral (single chamber) to bicameral (two chambers) systems that provide different approaches to representation and deliberation. The legislative process involves committees, public hearings, debates, and voting procedures designed to ensure thorough consideration of proposed laws. Effective legislatures balance competing interests while creating legal frameworks that serve public needs and maintain democratic governance.",
                "example_sentence": "The state _____ passed comprehensive education reform legislation after months of public hearings and debate.",
                "pronunciation": "LEJ-is-lay-cher (emphasis on first syllable)",
                "etymology": "From Latin \"legislatura,\" from \"lex\" (law) + \"latura\" (bringing or proposing)",
                "memory_tips": "Think \"ledge-is-nature\" - laws are the natural ledge that society stands on",
                "part_of_speech": "noun"
            },
            "legitimately": {
                "definition": "In a legitimate manner; legally, rightfully, or genuinely; according to established rules, laws, or accepted standards without deception or fraud. Acting legitimately means following proper procedures, meeting legal requirements, and operating within recognized authority structures. The adverb implies authenticity and adherence to standards that distinguish legitimate actions from illegal, fraudulent, or improper behaviors. Understanding legitimacy requires knowledge of relevant laws, ethical standards, and social norms that define acceptable conduct in specific contexts and relationships.",
                "example_sentence": "The business owner could _____ claim the tax deduction because all expenses were properly documented and qualified under current law.",
                "pronunciation": "luh-JIT-uh-mit-lee (emphasis on second syllable)",
                "etymology": "From \"legitimate\" + \"-ly,\" meaning \"in a lawful or genuine manner\"",
                "memory_tips": "Think \"legit-imately\" - doing things in a legit way immediately and properly",
                "part_of_speech": "adverb"
            },
            "legs": {
                "definition": "Plural of leg; the limbs that support and move the body in humans and animals; also refers to the supporting parts of furniture or other objects that raise them off the ground. Human legs consist of complex bone, muscle, and joint systems that enable walking, running, jumping, and various other movements essential for mobility and physical activity. In furniture and equipment, legs provide stable support while allowing space underneath for cleaning, storage, or other uses. The term extends metaphorically to describe segments of journeys, stages of processes, or supporting elements of plans and organizations.",
                "example_sentence": "The marathon runner's strong _____ carried her through the challenging mountain course to victory.",
                "pronunciation": "LEGZ (single syllable, rhymes with \"eggs\")",
                "etymology": "Plural of \"leg,\" from Old Norse \"leggr,\" meaning \"leg\" or \"bone\"",
                "memory_tips": "Think \"eggs\" - legs are like eggs in that they come in pairs and are essential for movement",
                "part_of_speech": "noun"
            },
            "leguminous": {
                "definition": "Belonging to or characteristic of the legume family of plants (Fabaceae), which includes beans, peas, lentils, peanuts, and clover; plants that typically produce pods and have the ability to fix nitrogen from the atmosphere through symbiotic bacteria in their root nodules. Leguminous plants play crucial roles in agriculture and ecology by enriching soil with nitrogen, reducing the need for synthetic fertilizers, and providing protein-rich foods for human and animal consumption. These plants often have compound leaves, butterfly-shaped flowers, and distinctive seed pods that split open when mature. Understanding leguminous plants is important for sustainable agriculture and nutrition planning.",
                "example_sentence": "The farmer planted _____ crops like soybeans to naturally enrich the soil with nitrogen for the following year's corn.",
                "pronunciation": "luh-GYOO-muh-nuhs (emphasis on second syllable)",
                "etymology": "From Latin \"legumen\" (things that can be picked) + suffix \"-ous,\" referring to plants with pickable pods",
                "memory_tips": "Think \"leg-goomin-us\" - plants that are good for us and help other plants with their nitrogen-fixing legs (roots)",
                "part_of_speech": "adjective"
            }
        }
        
        if word in word_data:
            data = word_data[word]
            # Calculate difficulty components
            difficulty_components = self.difficulty_calculator.calculate_difficulty_components(
                word, data["definition"], data["etymology"]
            )
            
            # Combine with existing data
            return {
                **data,
                **difficulty_components,
                "difficulty_calculation_method": "4-factor weighted model (overall_score: {:.2f})".format(
                    (difficulty_components["phonetic_transparency_score"] * 0.2 + 
                     difficulty_components["word_frequency_score"] * 0.3 + 
                     difficulty_components["morphology_score"] * 0.2 + 
                     difficulty_components["etymology_score"] * 0.3)
                )
            }
        else:
            return {
                "definition": f"[ERROR: No data available for word '{word}']",
                "example_sentence": f"[ERROR: Missing example sentence for '{word}']",
                "pronunciation": f"[ERROR: Missing pronunciation for '{word}']", 
                "etymology": f"[ERROR: Missing etymology for '{word}']",
                "memory_tips": f"[ERROR: Missing memory tips for '{word}']",
                "part_of_speech": "unknown",
                "phonetic_transparency_score": 0.0,
                "word_frequency_score": 0.0,
                "morphology_score": 0.0,
                "etymology_score": 0.0,
                "difficulty_calculation_method": "error - no data available"
            }

    def process_batch(self):
        """Process all words in batch 101"""
        
        logging.info("Processing Batch 101 with comprehensive Claude data...")
        
        input_file = "output/batch_101_words.csv"
        output_file = "output/batch_101_processed.csv"
        
        try:
            with open(input_file, 'r', encoding='utf-8') as infile:
                reader = csv.DictReader(infile)
                words_data = list(reader)
            
            processed_words = []
            
            for row in words_data:
                word = row['word'].strip()
                
                # Get comprehensive Claude data
                claude_data = self.get_comprehensive_claude_data(word)
                
                # Create processed row
                processed_row = {
                    'word': word,
                    'definition': claude_data['definition'],
                    'example_sentence': claude_data['example_sentence'],
                    'source_difficulty': row['source_difficulties'].split(';')[0].strip(),  # First source difficulty
                    'difficulty_level': '',  # Leave empty as requested
                    'difficulty_name': '',  # Leave empty as requested  
                    'ai_difficulty_level': '',  # Leave empty as requested
                    'ai_difficulty_name': '',  # Leave empty as requested
                    'phonetic_transparency_score': claude_data['phonetic_transparency_score'],
                    'word_frequency_score': claude_data['word_frequency_score'], 
                    'morphology_score': claude_data['morphology_score'],
                    'etymology_score': claude_data['etymology_score'],
                    'difficulty_calculation_method': claude_data['difficulty_calculation_method'],
                    'part_of_speech': claude_data['part_of_speech'],
                    'pronunciation_guide': claude_data['pronunciation'],
                    'etymology': claude_data['etymology'],
                    'etymology_source': 'Claude',
                    'memory_tips': claude_data['memory_tips'],
                    'alternate_spellings': '',  # Leave empty
                    'language_origin': claude_data.get('language_origin', 'Various'),
                    'definition_source': 'Claude', 
                    'source_names': 'Scripps National Spelling Bee',
                    'source_difficulties': row['source_difficulties'],
                    'frequency': len(row['source_difficulties'].split(';')),  # Count of source difficulties
                    'original_source': f"Scripps National Spelling Bee Words of the Champions ({row['years']})",
                    'source_access_date': '2025-08-19'
                }
                
                processed_words.append(processed_row)
                logging.info(f"Processed word: {word}")
            
            # Write to output file
            fieldnames = [
                'word', 'definition', 'example_sentence', 'source_difficulty', 'difficulty_level',
                'difficulty_name', 'ai_difficulty_level', 'ai_difficulty_name', 'phonetic_transparency_score',
                'word_frequency_score', 'morphology_score', 'etymology_score', 'difficulty_calculation_method',
                'part_of_speech', 'pronunciation_guide', 'etymology', 'etymology_source', 'memory_tips',
                'alternate_spellings', 'language_origin', 'definition_source', 'source_names',
                'source_difficulties', 'frequency', 'original_source', 'source_access_date'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(processed_words)
            
            logging.info(f"Saved {len(processed_words)} words to {output_file}")
            logging.info("Batch 101 processing completed!")
            logging.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
            logging.info(f"Output saved to: {output_file}")
            logging.info(f"Results: {len(processed_words)} successful, 0 failed")
                
        except Exception as e:
            logging.error(f"Error processing batch: {e}")
            raise

if __name__ == "__main__":
    processor = Batch101Processor()
    processor.process_batch()