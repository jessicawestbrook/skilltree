#!/usr/bin/env python3

import pandas as pd
from dataclasses import dataclass
from typing import List, Optional, Tuple
import os

@dataclass
class WordData:
    word: str
    definition: str
    part_of_speech: str
    pronunciation_guide: str
    etymology: str
    language_origins: str
    example_sentence: str
    memory_tip: str
    phonetic_transparency: Optional[int] = None
    word_frequency: Optional[int] = None
    morphological_complexity: Optional[int] = None
    etymology_complexity: Optional[int] = None
    final_difficulty: Optional[str] = None

class DifficultyCalculator:
    @staticmethod
    def calculate_phonetic_transparency(word: str) -> int:
        return 3
    
    @staticmethod
    def calculate_word_frequency(word: str) -> int:
        return 3
    
    @staticmethod
    def calculate_morphological_complexity(word: str) -> int:
        return 3
    
    @staticmethod
    def calculate_etymology_complexity(word: str) -> int:
        return 3

class Batch087Processor:
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        self.errors = []

    def get_comprehensive_claude_data(self, word: str) -> dict:
        batch_087_data = {
            'hull': {
                'definition': 'Hull refers to the main body or frame of a ship or boat, providing the watertight structure that allows the vessel to float and navigate through water. This essential component of marine vessels includes the bottom, sides, and deck framework that forms the basic shell of the watercraft. Ship hulls are designed to withstand water pressure, weather conditions, and the stresses of movement through waves while maintaining structural integrity and buoyancy. Different hull shapes serve various purposes, from the deep V-hulls of high-speed boats to the flat bottoms of barges and the rounded hulls of traditional sailing vessels. Hull construction involves specialized materials and techniques including welded steel plates, fiberglass molding, or traditional wood planking, depending on the vessel type and intended use. The term also applies to the outer covering or shell of seeds, nuts, and fruits that protects the inner contents. In broader usage, hull can describe the basic framework or body of any structure. Understanding hull design is crucial for naval architecture, boat building, and marine safety, as hull integrity directly affects vessel performance, stability, and seaworthiness.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'HUL',
                'etymology': 'From Middle English "hul," possibly from Old English "hulu" meaning "husk" or "shell," related to covering or enclosing.',
                'language_origins': 'Old English, Middle English',
                'example_sentence': 'The ship\'s _______ was carefully inspected for damage after it ran aground on the rocky coastline.',
                'memory_tip': 'Remember "HULL" - sounds like "HOLE," but it\'s the opposite - the solid shell that keeps holes (water) out of ships.'
            },
            'human': {
                'definition': 'Human refers to members of the species Homo sapiens, characterized by advanced cognitive abilities, complex language, sophisticated tool use, and intricate social structures that distinguish them from other animals. This term encompasses the biological, psychological, cultural, and social aspects of humanity, including consciousness, creativity, moral reasoning, and the capacity for abstract thought. Humans are bipedal primates with highly developed brains, opposable thumbs, and sophisticated communication abilities that enable complex cooperation and cultural transmission across generations. The human experience includes emotions, relationships, artistic expression, scientific inquiry, and spiritual exploration that create rich individual and collective identities. Human societies develop diverse cultures, languages, technologies, and belief systems that adapt to different environments and historical circumstances. Modern understanding of humans includes both biological aspects studied by anthropology and medicine, and social aspects examined by psychology, sociology, and philosophy. The concept of being human involves questions about consciousness, free will, moral responsibility, and the meaning of existence that have puzzled thinkers throughout history. Human rights, dignity, and equality are fundamental principles that recognize the inherent value and worth of all human beings.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'HYOO-muhn',
                'etymology': 'From Latin "humanus," from "homo" meaning "man" or "person," related to "humus" meaning "earth."',
                'language_origins': 'Latin',
                'example_sentence': 'The study explored what makes _______ behavior different from that of other intelligent animals.',
                'memory_tip': 'Remember "HUMAN" - from Latin "homo" (person), people who are humane and connected to the earth (humus).'
            },
            'humane': {
                'definition': 'Humane describes behavior, treatment, or policies characterized by compassion, kindness, and concern for the welfare and dignity of others, particularly those who are vulnerable, suffering, or in distress. This moral concept emphasizes treating all beings with respect, minimizing harm, and acting with empathy and understanding rather than cruelty or indifference. Humane treatment involves recognizing the inherent worth and rights of individuals, whether human or animal, and making efforts to reduce suffering while promoting well-being. The concept extends to various contexts including healthcare, criminal justice, animal welfare, education, and social services, where humane approaches prioritize dignity and compassion. Humane societies and organizations work to protect vulnerable populations, advocate for ethical treatment, and educate communities about compassionate practices. The opposite of humane is inhumane, describing cruel, callous, or degrading treatment that ignores suffering or dignity. Humane considerations influence laws, policies, and professional practices in fields such as medicine, law enforcement, and animal care. Understanding what constitutes humane treatment requires balancing practical necessities with moral obligations to minimize harm and respect the inherent value of all sentient beings.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'hyoo-MAYN',
                'etymology': 'From Latin "humanus" meaning "of humans," emphasizing the best qualities associated with humanity.',
                'language_origins': 'Latin',
                'example_sentence': 'The animal shelter\'s _______ policies ensured that all creatures received compassionate care regardless of their circumstances.',
                'memory_tip': 'Remember "HUMANE" - HUMAN + E, showing the best human qualities of kindness and compassion toward others.'
            },
            'humboldt': {
                'definition': 'Humboldt typically refers to Alexander von Humboldt (1769-1859), a Prussian polymath, naturalist, explorer, and geographer who made groundbreaking contributions to multiple scientific disciplines including geography, geology, meteorology, and biology. This influential figure is considered one of the founders of modern geography and ecology, known for his extensive scientific expeditions to South America and his holistic approach to understanding natural phenomena. Humboldt\'s work emphasized the interconnectedness of natural systems, pioneering the concept of nature as a unified whole rather than isolated components. His scientific methods combined careful observation, measurement, and documentation with artistic and literary expression to communicate scientific discoveries to broader audiences. The name appears in numerous geographic features, institutions, and species named in his honor, including the Humboldt Current, Humboldt County, and various universities worldwide. Humboldt\'s legacy includes advancing scientific education, promoting international scientific cooperation, and influencing later scientists including Charles Darwin. His approach to science integrated multiple disciplines and emphasized the importance of both rigorous methodology and passionate curiosity about the natural world.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'HUM-bohlt',
                'etymology': 'German surname, from "hum" (possibly related to "home") and "boldt" (bold), referring to Alexander von Humboldt.',
                'language_origins': 'German',
                'example_sentence': 'The oceanographic expedition studied the _______ Current, named after the famous naturalist who first described it.',
                'memory_tip': 'Remember "HUMBOLDT" - HUM + BOLD, the bold naturalist who hummed with excitement about exploring and understanding nature.'
            },
            'humbug': {
                'definition': 'Humbug refers to deceptive or false talk and behavior, particularly fraudulent claims, deliberate nonsense, or insincere pretense designed to mislead or impress others. This term describes both the act of deception and something that is recognized as fraudulent or worthless. Historical usage often applied humbug to charlatan salespeople, fake medical treatments, or exaggerated claims that exploited gullible customers. The word gained cultural prominence through Charles Dickens\' character Ebenezer Scrooge, who famously dismisses Christmas as "humbug," expressing cynicism about holiday sentiments and traditions. Humbug can describe anything from minor exaggerations and white lies to serious fraud and deliberate misinformation. The term carries connotations of irritation or dismissal, often used when someone recognizes obvious deception or pretense. Modern usage includes political rhetoric, advertising claims, or social media content that appears designed more to mislead than inform. Understanding humbug requires recognizing the difference between honest mistakes and deliberate attempts to deceive, as well as developing critical thinking skills to identify suspicious claims and evaluate information sources.',
                'part_of_speech': 'noun, interjection',
                'pronunciation_guide': 'HUM-bug',
                'etymology': 'Origin uncertain, possibly from "hum" (deceptive talk) and "bug" (something troublesome), meaning troublesome deception.',
                'language_origins': 'English (origin uncertain)',
                'example_sentence': 'The old man dismissed the politician\'s promises as complete _______, having heard similar empty pledges for decades.',
                'memory_tip': 'Remember "HUMBUG" - HUM + BUG, annoying buzzing (hum) that bugs you with false or deceptive talk.'
            },
            'humdrum': {
                'definition': 'Humdrum describes something that is lacking in variety, dull, monotonous, or boringly routine, characterized by repetitive sameness that fails to stimulate interest or excitement. This adjective applies to activities, experiences, conversations, or lifestyles that have become predictable, ordinary, and unstimulating through constant repetition or lack of novelty. Humdrum situations often involve mechanical routines, repetitive tasks, or environments where little changes from day to day, creating feelings of boredom, restlessness, or dissatisfaction. Work can become humdrum when it involves repetitive duties without creative challenges or opportunities for growth. Relationships, conversations, or social activities may be described as humdrum when they lack spontaneity, depth, or engaging content. The term suggests a desire for more excitement, variety, or meaningfulness in whatever is being described. People experiencing humdrum circumstances often seek ways to introduce novelty, challenge, or purpose into their routines. Understanding humdrum involves recognizing the human need for stimulation, variety, and engagement, as well as the importance of finding balance between stability and excitement in personal and professional life.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'HUM-drum',
                'etymology': 'Reduplication of "hum," representing monotonous droning sounds, suggesting boring repetition.',
                'language_origins': 'English',
                'example_sentence': 'After years of the same _______ routine, she decided to change careers and pursue something more challenging.',
                'memory_tip': 'Remember "HUMDRUM" - HUM + DRUM, monotonous humming and drumming that becomes boring and repetitive.'
            },
            'humerus': {
                'definition': 'Humerus is the long bone in the upper arm that extends from the shoulder to the elbow, serving as the primary structural element of the upper limb and providing attachment points for numerous muscles involved in arm movement. This largest bone of the arm articulates with the scapula (shoulder blade) at the shoulder joint and with the radius and ulna bones at the elbow joint, enabling the complex range of motion possible in human arms. The humerus features several important anatomical landmarks including the head (which fits into the shoulder socket), the shaft (main body), and various projections and depressions where muscles and ligaments attach. Common humerus injuries include fractures from falls or impacts, which require careful medical treatment due to the bone\'s proximity to important nerves and blood vessels. The bone serves crucial functions in arm movement, weight bearing, and force transmission during activities ranging from lifting objects to throwing and reaching motions. Understanding humerus anatomy is essential for medical professionals, physical therapists, and anyone studying human biomechanics or treating upper arm injuries. The bone\'s structure reflects evolutionary adaptations for tool use, manipulation, and the complex movements that distinguish human upper limb function.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HYOO-mer-uhs',
                'etymology': 'From Latin "humerus" meaning "shoulder" or "upper arm," related to "humeri" (shoulders).',
                'language_origins': 'Latin',
                'example_sentence': 'The X-ray revealed a fracture in the patient\'s _______ that would require surgery and months of physical therapy.',
                'memory_tip': 'Remember "HUMERUS" - sounds like "HUMOROUS," but it\'s not funny when you break the bone in your upper arm!'
            },
            'humidistat': {
                'definition': 'Humidistat is a device that automatically controls humidity levels in enclosed spaces by monitoring moisture content in the air and activating humidification or dehumidification systems when predetermined levels are exceeded. This instrument combines humidity sensing technology with control mechanisms to maintain optimal moisture conditions for comfort, health, equipment protection, or industrial processes. Humidistats work similarly to thermostats but respond to humidity rather than temperature, using sensors such as hair hygrometers, electronic sensors, or psychrometric measurements to detect moisture levels. When humidity rises above or falls below set points, the humidistat triggers appropriate responses such as activating dehumidifiers, humidifiers, ventilation fans, or other climate control equipment. These devices are essential in applications where humidity control is critical, including museums preserving artifacts, greenhouses maintaining plant health, data centers protecting electronic equipment, and residential spaces ensuring comfort and preventing mold growth. Modern humidistats often integrate with comprehensive HVAC systems and building automation networks to provide precise environmental control. Understanding humidistat operation is important for facilities management, HVAC technicians, and anyone responsible for maintaining optimal indoor environmental conditions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hyoo-MID-uh-stat',
                'etymology': 'From "humid" (moisture) and "stat" (from Greek "statos" meaning "standing"), a device that keeps humidity standing at set levels.',
                'language_origins': 'Latin, Greek',
                'example_sentence': 'The museum installed a sophisticated _______ to protect the ancient artifacts from damage caused by fluctuating moisture levels.',
                'memory_tip': 'Remember "HUMIDISTAT" - HUMID + STAT, a device that keeps humidity static or constant at desired levels.'
            },
            'hummingbird': {
                'definition': 'Hummingbird refers to small, brightly colored birds belonging to the family Trochilidae, renowned for their ability to hover in mid-air, fly backwards, and beat their wings at extraordinary speeds of up to 80 beats per second. These remarkable birds are found exclusively in the Americas, ranging from Alaska to southern Chile, with the greatest diversity in tropical regions. Hummingbirds have specialized anatomical features including rapid wing movements, excellent maneuverability, long bills adapted for reaching flower nectar, and high-energy metabolisms that require constant feeding. Their unique flight capabilities result from specialized wing structures and muscle arrangements that allow for precise control and sustained hovering while feeding. These birds play crucial ecological roles as pollinators for many flowering plants, with some species having co-evolved intricate relationships with specific flower types. Hummingbirds consume nectar for energy and small insects for protein, requiring visits to hundreds or thousands of flowers daily to meet their metabolic needs. Their jewel-like appearance, acrobatic flight patterns, and tiny size make them popular subjects for birdwatchers, photographers, and garden enthusiasts who provide feeders and flowering plants to attract them.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HUM-ing-burd',
                'etymology': 'From "humming" (the sound their rapidly beating wings make) and "bird," describing their characteristic wing sound.',
                'language_origins': 'English',
                'example_sentence': 'The tiny _______ hovered motionlessly at the feeder, its wings beating so fast they were just a blur.',
                'memory_tip': 'Remember "HUMMINGBIRD" - HUMMING + BIRD, birds that make a humming sound with their incredibly fast-beating wings.'
            },
            'hummock': {
                'definition': 'Hummock refers to a small mound, hillock, or raised area of ground that rises above the surrounding landscape, typically formed through natural processes such as frost action, vegetation growth, or geological activity. These minor topographical features are common in various environments including wetlands, tundra regions, grasslands, and coastal areas where they create microhabitat diversity and influence drainage patterns. Hummocks in wetlands often form when vegetation such as sedges or mosses accumulates and creates elevated areas that support different plant communities than surrounding lower areas. In permafrost regions, hummocks can result from freeze-thaw cycles that create characteristic polygonal patterns in the landscape. These small elevations provide important ecological functions by creating varied growing conditions, wildlife habitat, and drainage patterns that support biodiversity. Hummocks can also refer to small wooded areas or groves that stand slightly above surrounding terrain. Understanding hummock formation and distribution helps ecologists, landscape managers, and researchers study ecosystem dynamics, hydrology, and the effects of climate change on various environments. The presence and characteristics of hummocks often indicate specific environmental conditions and ecological processes.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HUM-uhk',
                'etymology': 'Probably from Low German "hummel" meaning "small hill" or related to "hump," referring to small raised areas.',
                'language_origins': 'Low German, English',
                'example_sentence': 'The marsh was dotted with small _______ that provided dry spots for nesting birds above the waterline.',
                'memory_tip': 'Remember "HUMMOCK" - sounds like "HUM-ock," a small hump of rock or earth that rises from the ground.'
            },
            'humor': {
                'definition': 'Humor refers to the quality of being amusing, entertaining, or comical, as well as the human ability to perceive, appreciate, and express what is funny, ironic, or absurd in various situations. This complex psychological and social phenomenon involves cognitive processes that recognize incongruities, timing, and social contexts that create amusement or laughter. Humor serves important social functions including building relationships, relieving tension, coping with stress, and communicating ideas in engaging ways that might otherwise be difficult to express. Different types of humor include wit, sarcasm, satire, puns, physical comedy, and observational comedy, each requiring different cognitive skills and social awareness. Cultural factors significantly influence what people find humorous, with jokes, references, and comedic styles varying across different societies and time periods. Psychological research shows that humor can improve mental health, enhance creativity, strengthen social bonds, and even provide physiological benefits through laughter. The development and appreciation of humor involve complex interactions between intelligence, emotional understanding, timing, and social sensitivity. Understanding humor requires recognizing both its entertainment value and its deeper roles in human communication and social interaction.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HYOO-mer',
                'etymology': 'From Latin "humor" meaning "moisture" or "liquid," originally referring to bodily fluids thought to affect temperament.',
                'language_origins': 'Latin',
                'example_sentence': 'Her quick wit and dry _______ made even the most boring meetings entertaining for her colleagues.',
                'memory_tip': 'Remember "HUMOR" - from Latin for body fluids that were thought to affect mood, now meaning what puts us in a good mood through laughter.'
            },
            'humour': {
                'definition': 'Humour is the British English spelling of "humor," referring to the quality of being amusing, entertaining, or comical, as well as the human capacity to perceive and express what is funny or absurd. This spelling reflects the British orthographic tradition of retaining the "u" in words derived from Latin, distinguishing it from the American English spelling that drops this vowel. The concept encompasses the same meanings as the American spelling, including wit, comedy, amusement, and the ability to find and create entertaining situations through clever observation, timing, and social awareness. British humour is often characterized by specific cultural traits including irony, understatement, self-deprecation, and dry wit that reflects particular social values and communication styles. The spelling difference represents broader patterns in English language development, where American English simplified many spellings while British English maintained more traditional forms. Understanding these spelling variations is important for international communication, academic writing, and recognizing different English language traditions. The content and appreciation of humour remain culturally specific, with British comedy traditions influencing global entertainment while maintaining distinctive characteristics that reflect British social attitudes and values.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HYOO-mer',
                'etymology': 'From Latin "humor," with British spelling retaining the "u" from French influence.',
                'language_origins': 'Latin, French, British English',
                'example_sentence': 'The British comedian\'s self-deprecating _______ had the audience laughing at his witty observations about everyday life.',
                'memory_tip': 'Remember "HUMOUR" - British spelling of humor with an extra U, like "colour" and other British words that keep the U.'
            },
            'hunch': {
                'definition': 'Hunch refers to an intuitive feeling, guess, or suspicion about something without concrete evidence or logical reasoning to support the conclusion. This psychological phenomenon involves subconscious processing of information, pattern recognition, and emotional responses that generate sudden insights or predictions about situations, people, or outcomes. Hunches often prove surprisingly accurate, suggesting they may result from unconscious analysis of subtle cues, past experiences, and environmental factors that conscious reasoning hasn\'t fully processed. The term can also describe the physical act of hunching, meaning to bend forward or curve the back and shoulders, typically in response to cold, defensiveness, or concentration. Having a hunch involves trusting instinctive responses even when logical analysis is incomplete or unavailable. Successful decision-makers often report relying on hunches in situations where complete information isn\'t available or time constraints prevent thorough analysis. Research in cognitive psychology suggests hunches may represent rapid processing of complex information by experienced individuals who have developed expertise in recognizing patterns. Understanding when to trust hunches versus seeking more information requires balancing intuitive insights with critical thinking and evidence-based reasoning.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'HUNCH',
                'etymology': 'Origin uncertain, possibly from Old French "hanche" meaning "haunch" or hip, referring to a bent posture.',
                'language_origins': 'Old French, English',
                'example_sentence': 'The detective had a strong _______ that the suspect was hiding something important, though he couldn\'t yet prove it.',
                'memory_tip': 'Remember "HUNCH" - sounds like "LUNCH," when you have a gut feeling (like hunger) that something is true even without proof.'
            },
            'hundred': {
                'definition': 'Hundred is the number 100, representing ten groups of ten or the cardinal number following ninety-nine and preceding one hundred one. This fundamental mathematical concept serves as a base unit in many counting and measurement systems, providing a convenient reference point for expressing large quantities, percentages, and proportional relationships. The number hundred appears frequently in currency systems, scoring systems, measurement units, and statistical expressions where it represents completeness or a standard reference point. Cultural and linguistic usage often employs "hundred" metaphorically to indicate large but finite quantities, as in "hundreds of people" or completeness as in "giving one hundred percent effort." Historical number systems have long recognized hundred as significant, with many cultures developing specific words and symbols for this quantity. In decimal mathematics, hundred serves crucial functions in place value systems, percentage calculations, and proportional reasoning. The concept extends beyond mere counting to represent benchmarks, goals, and standards in various contexts from academic grading to business metrics. Understanding hundred and its applications is fundamental to mathematical literacy, financial understanding, and quantitative reasoning in daily life.',
                'part_of_speech': 'number, noun',
                'pronunciation_guide': 'HUN-drid',
                'etymology': 'From Old English "hundred," from Germanic roots meaning "ten tens" or "great hundred."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The store celebrated its grand opening by giving away prizes to the first _______ customers who arrived.',
                'memory_tip': 'Remember "HUNDRED" - HUN + DRED, like a hundred huns being dreadful, the number 100 or ten groups of ten.'
            },
            'hungary': {
                'definition': 'Hungary is a landlocked Central European country bordered by Austria, Slovakia, Ukraine, Romania, Serbia, Croatia, and Slovenia, known for its rich history, distinctive culture, and unique Magyar language. This nation has a complex history involving the Austro-Hungarian Empire, periods of Ottoman occupation, Soviet influence, and eventual independence and European Union membership. Hungary\'s capital and largest city, Budapest, straddles the Danube River and serves as a major cultural and economic center. The country is renowned for its thermal springs, historic architecture, classical music traditions, and contributions to science and mathematics. Hungarian culture includes distinctive folk traditions, cuisine featuring dishes like goulash and paprika-based recipes, and a language that belongs to the Finno-Ugric family rather than the Indo-European languages of neighboring countries. Modern Hungary faces contemporary challenges including economic development, political reforms, and balancing national identity with European integration. The nation has produced notable figures in various fields including music, science, literature, and sports. Understanding Hungary involves appreciating its unique position in Central Europe, its complex history of foreign influences and resistance, and its ongoing efforts to maintain cultural identity while participating in modern European institutions.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'HUN-guh-ree',
                'etymology': 'From Medieval Latin "Hungaria," possibly from Turkish "on-ogur" meaning "ten arrows," referring to tribal confederations.',
                'language_origins': 'Medieval Latin, possibly Turkish',
                'example_sentence': 'The students planned to visit _______ during their European tour to experience the thermal baths and historic architecture of Budapest.',
                'memory_tip': 'Remember "HUNGARY" - sounds like "HUNGRY," a country in Central Europe where you might get hungry for delicious goulash!'
            },
            'hungrily': {
                'definition': 'Hungrily is an adverb describing actions performed with hunger, eagerness, or intense desire for food, knowledge, experience, or satisfaction. When applied to eating, hungrily describes consuming food with obvious appetite, often quickly or enthusiastically due to genuine hunger or exceptional enjoyment of the meal. The term extends beyond physical hunger to describe any behavior characterized by intense wanting, craving, or seeking after something desired. People might hungrily pursue opportunities, hungrily read books for knowledge, or hungrily seek experiences they\'ve been denied. The word conveys both the intensity of desire and often the urgency or enthusiasm with which someone approaches what they want. Hungrily can describe emotional, intellectual, or spiritual appetites as well as physical ones, emphasizing the eagerness and intensity of the person\'s approach. The adverb suggests not just wanting something but actively pursuing it with energy and determination. Understanding the use of hungrily involves recognizing both literal descriptions of eating behavior and metaphorical applications to various forms of human desire and pursuit of goals, experiences, or satisfaction.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'HUN-gruh-lee',
                'etymology': 'From "hungry" plus the adverbial suffix "-ly," meaning "in a hungry manner."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'After the long hike, the campers _______ devoured the hot meal around the campfire.',
                'memory_tip': 'Remember "HUNGRILY" - HUNGRY + LY, doing something in a hungry way, eating or wanting something with great eagerness.'
            },
            'hunky': {
                'definition': 'Hunky is an informal adjective describing a man who is physically attractive, muscular, and sexually appealing, typically emphasizing masculine physical characteristics such as strong build, handsome features, and robust appearance. This colloquial term represents subjective assessments of male physical attractiveness based on contemporary cultural standards that often emphasize fitness, strength, and conventional masculine beauty ideals. The usage of hunky reflects societal attitudes about male attractiveness and the objectification of physical appearance in both casual conversation and media representations. While generally considered a positive descriptor, the term can be superficial and reductive when it becomes the primary way someone is evaluated or described. Cultural standards for what constitutes "hunky" vary across different societies, time periods, and individual preferences, making the term inherently subjective and culturally specific. The term often appears in entertainment contexts, romance literature, and casual social discussion about physical attraction. Understanding hunky involves recognizing both its role in expressing attraction and its potential limitations when physical appearance becomes the dominant criterion for evaluating individuals. The term reflects broader social attitudes about masculinity, attractiveness, and how people express physical appreciation.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'HUN-kee',
                'etymology': 'Possibly from "hunk," meaning a sexually attractive man, origin uncertain, possibly from Dutch or German roots.',
                'language_origins': 'American English (uncertain origin)',
                'example_sentence': 'The romance novel featured a _______ hero who swept the heroine off her feet with his charm and good looks.',
                'memory_tip': 'Remember "HUNKY" - HUNK + Y, describing someone who is a hunk, physically attractive and muscular in appearance.'
            },
            'hunting': {
                'definition': 'Hunting refers to the practice of pursuing, capturing, or killing wild animals for food, sport, population control, or traditional cultural purposes. This ancient human activity involves tracking, stalking, and using various tools and techniques to capture game animals in their natural habitats. Modern hunting encompasses recreational activities, wildlife management practices, and subsistence hunting that continues to play important roles in many communities worldwide. Hunting regulations, licensing requirements, and seasonal restrictions help balance human activities with wildlife conservation, ensuring sustainable animal populations and ecosystem health. Different hunting methods include firearms, archery, falconry, and traditional techniques that have been passed down through generations. The practice requires skills in animal behavior, habitat knowledge, safety procedures, and often physical fitness and outdoor survival abilities. Ethical hunting emphasizes fair chase principles, quick and humane kills, and full utilization of harvested animals. Hunting also provides economic benefits through license fees, equipment sales, and tourism that support conservation programs and rural communities. Contemporary debates about hunting involve animal rights concerns, conservation effectiveness, safety issues, and cultural conflicts between different values regarding wildlife and land use.',
                'part_of_speech': 'noun, verb (present participle)',
                'pronunciation_guide': 'HUN-ting',
                'etymology': 'From Old English "huntian" meaning "to chase game," from Germanic roots related to "hound."',
                'language_origins': 'Old English, Germanic',
                'example_sentence': 'The wildlife biologist studied how traditional _______ practices affected deer population dynamics in the region.',
                'memory_tip': 'Remember "HUNTING" - HUNT + ING, the ongoing activity of hunting for wild animals using various skills and techniques.'
            },
            'hurdy': {
                'definition': 'Hurdy typically appears as part of "hurdy-gurdy," referring to a stringed musical instrument that produces sound by turning a crank that rotates a wheel against strings, similar to how a violin bow creates sound but using continuous circular motion instead of back-and-forth movements. This traditional folk instrument features a keyboard that presses tangents against the strings to change pitches, while drone strings provide continuous harmonic accompaniment. Hurdy-gurdies have been used in European folk music for centuries, particularly in France, where they remain popular in traditional and contemporary folk music. The instrument requires coordination between turning the crank at consistent speeds and operating the keyboard to create melodies, making it challenging to master but capable of producing distinctive and appealing sounds. Street musicians historically used hurdy-gurdies because they could be played while standing and moving, making them practical for busking and traveling performances. Modern hurdy-gurdies continue to be built and played by folk music enthusiasts, early music specialists, and contemporary musicians who appreciate their unique tonal qualities. Understanding hurdy-gurdies involves appreciating both their mechanical complexity and their important role in preserving and continuing European folk music traditions.',
                'part_of_speech': 'adjective (part of compound)',
                'pronunciation_guide': 'HUR-dee',
                'etymology': 'Part of "hurdy-gurdy," possibly imitative of the sound the instrument makes, from French traditions.',
                'language_origins': 'English, French influence',
                'example_sentence': 'The folk musician demonstrated the unique sound of his traditional _______ -gurdy at the medieval festival.',
                'memory_tip': 'Remember "HURDY" - part of "hurdy-gurdy," sounds like the hurried, whirring sound the crank-operated musical instrument makes.'
            },
            'hurricane': {
                'definition': 'Hurricane is a type of tropical cyclone characterized by sustained winds of at least 74 mph (119 km/h) that forms over warm ocean waters, typically in the Atlantic and northeastern Pacific basins. These massive rotating storm systems develop when atmospheric conditions combine warm sea surface temperatures, low wind shear, and sufficient atmospheric instability to create organized circulation patterns that can intensify into destructive weather events. Hurricanes are classified using the Saffir-Simpson scale from Category 1 (74-95 mph winds) to Category 5 (over 157 mph winds), with higher categories indicating more dangerous and destructive potential. The storm structure includes a calm eye surrounded by the eyewall containing the strongest winds, and spiral bands of thunderstorms that extend outward for hundreds of miles. Hurricane hazards include extreme winds, storm surge flooding, heavy rainfall, tornadoes, and coastal erosion that can cause catastrophic damage to infrastructure, agriculture, and human communities. Meteorologists use sophisticated forecasting models, satellite imagery, and aircraft reconnaissance to track hurricane development, movement, and intensity to provide advance warning for affected areas. Understanding hurricanes involves appreciating their role in global weather patterns, their impacts on coastal communities, and the importance of emergency preparedness and evacuation planning.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HUR-uh-kayn',
                'etymology': 'From Spanish "huracán," from Taíno "hurakán," referring to the Taíno god of storms.',
                'language_origins': 'Taíno, Spanish',
                'example_sentence': 'The coastal residents prepared for the approaching _______ by boarding up windows and evacuating to higher ground.',
                'memory_tip': 'Remember "HURRICANE" - sounds like "HURRY-CANE," storms so powerful you better hurry away from them, named after a Taíno storm god.'
            },
            'hurriedly': {
                'definition': 'Hurriedly is an adverb describing actions performed quickly, hastily, or with urgent speed, typically due to time pressure, emergency situations, or anxiety about completing tasks promptly. This word characterizes behavior that prioritizes speed over careful consideration, often resulting from external pressures or internal urgency about accomplishing goals within limited timeframes. Hurried actions may sacrifice thoroughness, accuracy, or quality in favor of rapid completion, sometimes leading to mistakes or overlooking important details. The adverb suggests both the pace of activity and often the emotional state of the person performing the actions, indicating stress, excitement, or concern about timing. Hurriedly can describe physical movements, decision-making processes, speech patterns, or any activity where speed becomes the dominant characteristic. Context determines whether hurried action is appropriate and effective or problematic and counterproductive. Emergency situations may require hurried responses to prevent harm, while other circumstances might benefit from more deliberate approaches. Understanding the use of hurriedly involves recognizing when speed is essential versus when careful consideration is more important, and the trade-offs between efficiency and accuracy in various situations.',
                'part_of_speech': 'adverb',
                'pronunciation_guide': 'HUR-eed-lee',
                'etymology': 'From "hurried" (past participle of "hurry") plus the adverbial suffix "-ly," meaning "in a hurried manner."',
                'language_origins': 'English',
                'example_sentence': 'She _______ packed her suitcase when she realized her flight departure time had been moved up by two hours.',
                'memory_tip': 'Remember "HURRIEDLY" - HURRIED + LY, doing something in a hurried way, quickly and often frantically due to time pressure.'
            },
            'hurtle': {
                'definition': 'Hurtle refers to moving with great speed and apparent lack of control, typically describing objects or people rushing forward with tremendous velocity and force. This verb emphasizes both the speed of movement and often the dangerous or reckless nature of the motion, suggesting movement that is difficult to stop or control once initiated. Hurtling objects or individuals often create impressions of power, momentum, and potential danger due to their rapid movement through space. The term frequently describes vehicles moving at high speeds, projectiles flying through the air, or people running with desperate urgency. Hurtling motion often occurs during emergencies, competitions, or situations where maximum speed is prioritized over safety or control. The word carries connotations of excitement, danger, or urgency that distinguish it from simply moving quickly. Natural phenomena such as meteorites, avalanches, or rushing water can also hurtle with destructive force. Understanding hurtle involves recognizing both the physical description of rapid movement and the emotional implications of speed that appears dangerous or uncontrolled. The term suggests movement that is thrilling, frightening, or impressive due to its combination of velocity and apparent lack of restraint.',
                'part_of_speech': 'verb',
                'pronunciation_guide': 'HUR-tuhl',
                'etymology': 'From Middle English "hurtlen," possibly from Old Norse "hurt" meaning "to collide," emphasizing forceful movement.',
                'language_origins': 'Middle English, Old Norse',
                'example_sentence': 'The race car began to _______ down the straightaway at incredible speeds toward the finish line.',
                'memory_tip': 'Remember "HURTLE" - sounds like "HURDLE," moving so fast you hurdle over obstacles, rushing forward with great speed and force.'
            },
            'husk': {
                'definition': 'Husk refers to the dry outer covering or shell of seeds, grains, or fruits that protects the inner edible or useful portions during growth and storage. These natural protective layers serve important biological functions including moisture retention, protection from pests and diseases, and seed dispersal mechanisms. Common examples include corn husks, rice husks, coconut husks, and sunflower seed hulls that must be removed to access the desired inner contents. Husks vary in thickness, texture, and durability depending on the plant species and environmental conditions, with some being papery and easily removed while others are tough and fibrous. The removal of husks, called husking or hulling, is essential in food processing and agricultural operations to prepare crops for consumption or further processing. Some husks have valuable secondary uses including animal bedding, composting material, fuel for burning, or raw materials for manufacturing products like paper or building materials. The term can also be used metaphorically to describe outer appearances that conceal inner reality or substance. Understanding husks involves recognizing their protective biological functions and their economic importance in agricultural processing and waste utilization.',
                'part_of_speech': 'noun, verb',
                'pronunciation_guide': 'HUSK',
                'etymology': 'From Middle English "husk," possibly from Middle Dutch "huuskijn" meaning "little house," referring to protective covering.',
                'language_origins': 'Middle English, Middle Dutch',
                'example_sentence': 'The farmer showed the children how to remove the _______ from corn ears to reveal the golden kernels inside.',
                'memory_tip': 'Remember "HUSK" - sounds like "HUSK-y," the husky outer shell that protects seeds and grains like a protective house.'
            },
            'hutia': {
                'definition': 'Hutia refers to large rodents belonging to the family Capromyidae that are endemic to the Caribbean islands, particularly Cuba, Jamaica, and other islands in the Greater Antilles. These mammals are among the few surviving native land mammals in the Caribbean, having evolved in isolation after the islands separated from mainland continents. Hutias are relatively large rodents, typically weighing between 1-7 kilograms, with robust bodies, short legs, and long tails, adapted for both arboreal and terrestrial lifestyles. They are primarily herbivorous, feeding on leaves, bark, fruits, and other plant materials, though some species occasionally consume small animals. Many hutia species are critically endangered or have become extinct due to habitat destruction, introduced predators such as cats and dogs, and human hunting pressure. Conservation efforts focus on protecting remaining populations through habitat preservation, predator control, and captive breeding programs. These animals play important ecological roles in their island ecosystems as seed dispersers and herbivores that influence plant community structure. Understanding hutias involves appreciating their unique evolutionary history, their vulnerability to environmental changes, and their significance as indicators of Caribbean island ecosystem health.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HOO-tee-ah',
                'etymology': 'From Taíno "jutía," the indigenous name for these Caribbean rodents.',
                'language_origins': 'Taíno',
                'example_sentence': 'The conservation biologist studied the endangered Cuban _______ to understand how habitat loss affected their feeding behavior.',
                'memory_tip': 'Remember "HUTIA" - sounds like "WHO-tea-ah," Caribbean rodents whose name makes you say "who?" because they\'re rarely seen and endangered.'
            },
            'hyacinth': {
                'definition': 'Hyacinth refers to fragrant spring-blooming flowers belonging to the genus Hyacinthus, characterized by dense clusters of tubular, waxy blooms in colors including blue, purple, pink, white, and yellow that emerge from bulbs planted in fall. These popular garden plants are native to the eastern Mediterranean region and have been cultivated for centuries for their intense fragrance and attractive appearance in spring landscapes. Hyacinths grow from bulbs that require a cold winter period to bloom properly, making them ideal for temperate climate gardens and forcing indoors for winter flowers. The flowers are arranged in dense, cylindrical spikes that rise from the center of strap-like leaves, creating spectacular displays when planted in masses. Beyond their ornamental value, hyacinths have cultural significance in Greek mythology, where the flower was said to have grown from the blood of the youth Hyacinthus, beloved by Apollo. The bulbs contain toxic compounds that can cause skin irritation and should be handled with care. Modern hyacinth varieties include both traditional outdoor types and specially prepared bulbs for indoor forcing, allowing gardeners to enjoy these fragrant flowers throughout the growing season. Understanding hyacinths involves appreciating their cultural history, horticultural requirements, and their role in spring garden design.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAHY-uh-sinth',
                'etymology': 'From Greek "hyakinthos," named after a youth in Greek mythology who was transformed into this flower.',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'The garden was filled with the sweet fragrance of purple _______ blooming in neat rows along the pathway.',
                'memory_tip': 'Remember "HYACINTH" - from Greek mythology where a youth named Hyacinthus became this fragrant spring flower.'
            },
            'hybrid': {
                'definition': 'Hybrid refers to offspring resulting from the crossbreeding of two different species, varieties, or breeds, combining genetic material from both parents to create organisms with mixed characteristics. This biological concept applies to plants, animals, and microorganisms where hybridization can occur naturally or through human intervention for specific purposes such as improving crop yields, disease resistance, or desired traits. In agriculture, hybrid crops like hybrid corn combine advantageous characteristics from different parent varieties to produce plants with superior performance, though the offspring typically cannot reproduce the same traits. Animal hybrids include examples like mules (horse-donkey crosses) and ligers (lion-tiger crosses), which often exhibit unique combinations of parental traits but may have reduced fertility. The term extends beyond biology to describe anything that combines elements from different sources, including hybrid vehicles that use both gasoline engines and electric motors, hybrid musical styles that blend different genres, or hybrid technologies that integrate multiple approaches. Hybridization represents both natural evolutionary processes and deliberate human efforts to create improved or novel combinations of existing characteristics. Understanding hybrids involves recognizing both the potential benefits of combining different traits and the complexities that can arise from mixing different biological or technological systems.',
                'part_of_speech': 'noun, adjective',
                'pronunciation_guide': 'HAHY-brid',
                'etymology': 'From Latin "hybrida," meaning "mongrel" or "mixed offspring," originally referring to mixed breeding.',
                'language_origins': 'Latin',
                'example_sentence': 'The farmer planted _______ corn varieties that combined disease resistance with high yield potential.',
                'memory_tip': 'Remember "HYBRID" - sounds like "HIGH-BRED," offspring that are highly bred from mixing two different types together.'
            },
            'hydra': {
                'definition': 'Hydra refers to a genus of small, freshwater cnidarians known for their remarkable regenerative abilities, capable of completely regrowing their entire body from small fragments. These simple multicellular animals are typically a few millimeters long, with tubular bodies topped by tentacles surrounding a mouth opening, and they reproduce both sexually and asexually through budding. Hydra demonstrate extraordinary biological properties including apparent immortality under laboratory conditions, as they continuously replace their cells and show no signs of aging. The name also refers to the mythological Lernaean Hydra, a serpentine water monster from Greek mythology that grew two heads for every one that was cut off, famously defeated by Hercules as one of his twelve labors. In broader usage, hydra describes any problem or challenge that seems to grow more complex or difficult when attempts are made to solve it, similar to the mythological creature\'s regenerating heads. Modern scientific research studies hydra as model organisms for understanding regeneration, stem cell biology, and aging processes that may have applications for human medicine. Understanding hydra involves appreciating both their remarkable biological properties and their symbolic significance in representing persistent, multiplying challenges that resist simple solutions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAHY-druh',
                'etymology': 'From Greek "hydra," meaning "water serpent," referring to both the mythological monster and the aquatic animal.',
                'language_origins': 'Greek',
                'example_sentence': 'The biology students observed how a _______ could regenerate its entire body after being cut into pieces.',
                'memory_tip': 'Remember "HYDRA" - from Greek water serpent, both a mythical multi-headed monster and a real water animal that regrows when cut.'
            },
            'hydrangea': {
                'definition': 'Hydrangea refers to flowering shrubs and climbing vines belonging to the family Hydrangeaceae, known for their large, showy flower clusters and their ability to change flower color based on soil pH conditions. These popular ornamental plants produce distinctive globular or flat-topped flower heads composed of numerous small flowers, with colors ranging from white and pink to blue and purple depending on soil acidity. Most hydrangeas prefer partial shade and consistent moisture, making them excellent choices for woodland gardens and areas with filtered sunlight. The unique pH-responsive color change occurs because aluminum availability in the soil affects flower pigmentation, with acidic soils producing blue flowers and alkaline soils producing pink flowers. Different hydrangea species offer various growth habits, bloom times, and flower forms, providing gardeners with numerous options for landscape design and seasonal interest. These plants have become garden staples in temperate regions worldwide, valued for their reliable blooming, relatively low maintenance requirements, and dramatic seasonal displays. Hydrangeas also have cultural significance in many societies and are popular as cut flowers for arrangements due to their large size and long-lasting blooms. Understanding hydrangeas involves appreciating their unique soil-color relationship, their diverse forms and cultivation requirements, and their important role in ornamental horticulture.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hahy-DRAYN-juh',
                'etymology': 'From Greek "hydor" (water) and "angeion" (vessel), referring to the cup-shaped seed capsules.',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'The gardener adjusted the soil pH to change the _______ flowers from pink to blue for the following season.',
                'memory_tip': 'Remember "HYDRANGEA" - HYDRA (water) + ANGEA (vessel), water-loving plants with vessel-like flowers that change color with soil conditions.'
            },
            'hydrant': {
                'definition': 'Hydrant refers to a connection point in water supply systems that provides access to pressurized water for firefighting, street cleaning, or other municipal purposes. Fire hydrants are the most common type, strategically placed along streets and near buildings to ensure firefighters can quickly access water supplies during emergency response operations. These devices typically consist of a valve mechanism connected to underground water mains, with outlets that can be opened using special tools to release high-pressure water flow. Hydrant design varies by region and manufacturer but generally includes color coding systems that indicate water flow capacity, operating mechanisms that control flow, and weather-resistant construction to function reliably in various environmental conditions. Proper hydrant maintenance is crucial for public safety, requiring regular inspection, testing, and repairs to ensure functionality during emergencies. Fire departments conduct routine testing of hydrants to verify adequate water pressure and flow rates needed for effective firefighting operations. The placement and spacing of hydrants in urban planning follows specific codes and standards to ensure adequate coverage for fire protection. Understanding hydrants involves appreciating their critical role in public safety infrastructure, their technical requirements for reliable operation, and their integration into broader municipal water and fire protection systems.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAHY-druhnt',
                'etymology': 'From Greek "hydor" meaning "water," referring to water access points in municipal systems.',
                'language_origins': 'Greek',
                'example_sentence': 'The fire crew quickly connected their hoses to the _______ and began attacking the building fire.',
                'memory_tip': 'Remember "HYDRANT" - HYDR (water) + ANT, like a water ant that provides access to underground water supplies for emergencies.'
            },
            'hydrargyrum': {
                'definition': 'Hydrargyrum is the Latin name for mercury, the chemical element with symbol Hg and atomic number 80, representing the only metal that remains liquid at room temperature under standard conditions. This name literally means "liquid silver" in Latin, reflecting mercury\'s distinctive silvery appearance and fluid properties that have fascinated humans throughout history. Mercury has been known since ancient times and was used in various applications including alchemy, medicine, and industrial processes, though modern understanding of its toxicity has greatly restricted its use. The element occurs naturally in cinnabar ore and can exist in various chemical forms including elemental mercury, inorganic mercury compounds, and organic mercury compounds, each with different properties and health risks. Historical uses of mercury included thermometers, barometers, dental amalgams, and various industrial processes, but environmental and health concerns have led to significant restrictions on its use and disposal. Mercury poisoning can cause serious neurological damage, making proper handling and containment essential for any remaining legitimate uses. Understanding hydrargyrum involves appreciating both its unique physical properties that made it valuable historically and the serious environmental and health challenges associated with mercury contamination. Modern science continues to study mercury\'s behavior in the environment and develop safer alternatives for applications that once relied on this liquid metal.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hahy-DRAHR-ji-rum',
                'etymology': 'From Greek "hydor" (water) and "argyros" (silver), literally meaning "liquid silver" or "water silver."',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'The old chemistry textbook referred to mercury by its Latin name _______, meaning liquid silver.',
                'memory_tip': 'Remember "HYDRARGYRUM" - HYDR (liquid) + ARGYRUM (silver), the Latin name for mercury, the liquid silver metal.'
            },
            'hydraulics': {
                'definition': 'Hydraulics refers to the branch of engineering and physics that deals with the mechanical properties and behavior of fluids, particularly liquids, and their application in machinery, systems, and structures. This field encompasses both the theoretical study of fluid mechanics and practical applications including hydraulic machinery, water supply systems, and fluid power technologies. Hydraulic systems use confined liquids, typically oil or water, to transmit power and create mechanical advantage through pressure differentials and fluid flow principles. Common applications include construction equipment like excavators and bulldozers, automotive braking and power steering systems, aircraft control systems, and industrial manufacturing equipment. The fundamental principle underlying hydraulics is Pascal\'s law, which states that pressure applied to a confined fluid is transmitted equally in all directions, allowing small forces to create much larger forces through appropriate system design. Hydraulic systems offer advantages including high power-to-weight ratios, precise control, reliable operation, and the ability to generate enormous forces using relatively compact equipment. Understanding hydraulics involves mastering fluid mechanics principles, system design considerations, and practical applications that leverage liquid properties to accomplish mechanical work. Modern hydraulic engineering continues to advance through improved materials, better system designs, and integration with electronic controls for enhanced precision and efficiency.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hahy-DRAW-liks',
                'etymology': 'From Greek "hydraulikos," from "hydor" (water) and "aulos" (pipe), referring to water conveyed through pipes.',
                'language_origins': 'Greek',
                'example_sentence': 'The construction crew used _______ to operate the powerful excavator that could lift several tons of material.',
                'memory_tip': 'Remember "HYDRAULICS" - HYDR (water) + AULICS (pipes), the science of using liquid power through pipes and systems.'
            },
            'hydriotaphia': {
                'definition': 'Hydriotaphia refers to "Hydriotaphia, Urn Burial," a philosophical and literary work written by Sir Thomas Browne in 1658, exploring themes of mortality, burial customs, and the nature of human existence through examination of ancient funeral urns discovered in Norfolk, England. This baroque prose work combines archaeological investigation with profound meditation on death, memory, and the transient nature of human life and achievements. Browne uses the discovery of Roman burial urns as a launching point for wide-ranging reflections on burial practices across different cultures and time periods, ultimately questioning what remains of human endeavors after death. The work is renowned for its elaborate, ornate prose style characteristic of 17th-century scholarly writing, featuring complex sentence structures, classical allusions, and philosophical speculation. Hydriotaphia represents both historical documentation of archaeological findings and literary art that transforms scientific observation into profound contemplation of universal human concerns. The text demonstrates Browne\'s vast learning, combining classical references, contemporary scientific knowledge, and religious contemplation in a unified artistic work. Modern readers appreciate Hydriotaphia both as a historical document reflecting 17th-century intellectual culture and as enduring literature that addresses timeless questions about mortality, memory, and the meaning of human existence.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'hahy-dree-oh-TAF-ee-ah',
                'etymology': 'From Greek "hydria" (water jar) and "taphos" (burial), referring to burial in urns or water vessels.',
                'language_origins': 'Greek',
                'example_sentence': 'The literature professor assigned _______ to demonstrate how 17th-century writers combined scientific observation with philosophical reflection.',
                'memory_tip': 'Remember "HYDRIOTAPHIA" - HYDRIO (water vessel) + TAPHIA (burial), Sir Thomas Browne\'s work about ancient burial urns and mortality.'
            },
            'hydrocortisone': {
                'definition': 'Hydrocortisone is a steroid hormone naturally produced by the adrenal glands and also manufactured synthetically for medical use as an anti-inflammatory and immunosuppressive medication. This corticosteroid hormone, also known as cortisol, plays essential roles in regulating metabolism, immune response, blood pressure, and stress reactions in the human body. Medical applications of hydrocortisone include treating inflammatory conditions such as eczema, dermatitis, allergic reactions, and various autoimmune disorders where excessive inflammation causes tissue damage and symptoms. The medication is available in various forms including topical creams and ointments for skin conditions, oral tablets for systemic treatment, and injectable forms for severe inflammatory conditions. Hydrocortisone works by mimicking natural cortisol functions, suppressing immune system activity and reducing inflammatory responses that cause swelling, redness, and pain. While effective for treating many conditions, long-term use of hydrocortisone can cause side effects including skin thinning, increased infection susceptibility, and potential systemic effects on metabolism and bone health. Understanding hydrocortisone involves appreciating both its important therapeutic benefits for inflammatory conditions and the need for careful medical supervision to balance treatment effectiveness with potential risks from prolonged corticosteroid use.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hahy-droh-KAWR-tuh-zohn',
                'etymology': 'From "hydro-" (water/hydrogen) + "cortisone" (from cortex, referring to adrenal cortex origin).',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'The doctor prescribed _______ cream to reduce the inflammation and itching caused by the allergic skin reaction.',
                'memory_tip': 'Remember "HYDROCORTISONE" - HYDRO + CORTISONE, a hormone from the adrenal cortex that helps reduce inflammation.'
            },
            'hydrophobia': {
                'definition': 'Hydrophobia literally means "fear of water" and historically referred to rabies, particularly the symptom where infected individuals develop an intense fear and inability to swallow liquids due to painful throat spasms. This term describes both the specific medical symptom of rabies where patients experience terror at the sight of water and the broader psychological condition of irrational fear of water. In rabies cases, hydrophobia results from neurological damage that makes swallowing extremely painful, causing patients to avoid water despite severe thirst, creating a tragic and distressing symptom. As a phobia, hydrophobia can describe anxiety disorders where individuals experience persistent, excessive fear of water, swimming, or aquatic environments that significantly impacts their daily functioning and quality of life. The condition may develop from traumatic experiences involving water, learned behaviors, or other psychological factors that create disproportionate fear responses to water-related situations. Treatment for hydrophobia as a phobia typically involves gradual exposure therapy, cognitive-behavioral therapy, and sometimes medication to manage anxiety symptoms. Understanding hydrophobia requires distinguishing between its historical medical usage related to rabies and its contemporary psychological usage describing water-related anxiety disorders. Modern medical terminology tends to use "rabies" rather than hydrophobia to avoid confusion with psychological conditions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hahy-druh-FOH-bee-uh',
                'etymology': 'From Greek "hydro" (water) and "phobos" (fear), literally meaning "fear of water."',
                'language_origins': 'Greek',
                'example_sentence': 'The patient\'s _______ made it difficult for medical staff to provide adequate hydration during treatment.',
                'memory_tip': 'Remember "HYDROPHOBIA" - HYDRO (water) + PHOBIA (fear), fear of water, historically associated with rabies symptoms.'
            },
            'hydroponic': {
                'definition': 'Hydroponic refers to a method of growing plants without soil, using nutrient-rich water solutions to deliver essential minerals directly to plant roots through various growing media and delivery systems. This agricultural technique allows precise control over plant nutrition, pH levels, and growing conditions, often resulting in faster growth rates, higher yields, and more efficient use of water and nutrients compared to traditional soil-based cultivation. Hydroponic systems include various designs such as deep water culture, nutrient film technique, ebb and flow systems, and drip irrigation methods, each offering different advantages for specific crops and growing situations. The controlled environment of hydroponic production enables year-round cultivation regardless of weather conditions, making it valuable for regions with poor soil, extreme climates, or limited arable land. Modern hydroponic operations range from small home garden systems to large commercial greenhouses producing vegetables, herbs, and flowers for urban markets. Environmental benefits include reduced water usage through recycling systems, elimination of soil-borne diseases and pests, and potential reduction in chemical pesticide use. Understanding hydroponics involves appreciating both the technical complexity of nutrient management and environmental control, and the potential for sustainable food production in urban and challenging environments.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'hahy-druh-PON-ik',
                'etymology': 'From Greek "hydro" (water) and "ponos" (labor), literally meaning "water working."',
                'language_origins': 'Greek',
                'example_sentence': 'The urban farm used _______ systems to grow fresh vegetables year-round without requiring soil.',
                'memory_tip': 'Remember "HYDROPONIC" - HYDRO (water) + PONIC (working), plants working with water instead of soil to grow.'
            },
            'hymnal': {
                'definition': 'Hymnal refers to a book containing religious songs, hymns, and spiritual music used in worship services, personal devotion, and community singing. These collections typically include both musical notation and lyrics, organized by liturgical seasons, themes, or alphabetical order to facilitate congregational participation in religious services. Hymnals serve important functions in preserving religious musical traditions, teaching theological concepts through song, and providing structured worship resources for religious communities. Different denominations and faiths have developed their own hymnals reflecting specific theological emphases, cultural traditions, and musical preferences that characterize their worship practices. Traditional hymnals include classic hymns that have been sung for centuries, while modern versions may incorporate contemporary worship songs, diverse musical styles, and songs from various cultural backgrounds. The compilation of hymnals involves careful selection of texts and music that support worship goals, theological education, and community participation regardless of individual musical ability. Many hymnals include additional resources such as responsive readings, liturgical elements, and indexes organized by topic, scripture reference, or first line to help worship leaders plan services. Understanding hymnals involves appreciating their role in religious education, community building, and the preservation and transmission of faith traditions through musical expression.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HIM-nuhl',
                'etymology': 'From "hymn" (religious song) plus the suffix "-al" indicating a collection or book.',
                'language_origins': 'Greek, Latin, English',
                'example_sentence': 'The choir director selected songs from the new _______ to teach the congregation contemporary worship music.',
                'memory_tip': 'Remember "HYMNAL" - HYMN + AL (collection), a collection or book of hymns used for religious worship and singing.'
            },
            'hypaethral': {
                'definition': 'Hypaethral describes architectural structures that are open to the sky, lacking a complete roof covering and designed to expose interior spaces to natural elements including sunlight, rain, and fresh air. This term applies to ancient temples, courtyards, and other buildings where deliberate openness to the heavens served religious, practical, or aesthetic purposes. Classical Greek and Roman architecture included hypaethral temples where the central sanctuary area remained unroofed, allowing direct connection between worshippers and the sky, which held spiritual significance in many ancient religions. The design concept reflects beliefs about divine presence being accessible through open sky connections, as well as practical considerations for large interior spaces where roofing technology was limited. Modern architecture occasionally incorporates hypaethral elements in buildings designed to blur boundaries between interior and exterior spaces, create dramatic lighting effects, or provide environmental benefits through natural ventilation and illumination. Hypaethral spaces require careful planning to address weather protection, structural integrity, and functional requirements while achieving desired openness to natural elements. Understanding hypaethral architecture involves appreciating both its historical religious significance and its contemporary applications in sustainable design that takes advantage of natural lighting, ventilation, and the psychological benefits of connection to outdoor environments.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'hahy-PEE-thruhl',
                'etymology': 'From Greek "hypaithros," from "hypo" (under) and "aither" (sky), literally meaning "under the open sky."',
                'language_origins': 'Greek',
                'example_sentence': 'The ancient Greek temple featured a _______ design that allowed worshippers to commune with the gods under the open sky.',
                'memory_tip': 'Remember "HYPAETHRAL" - HYPO (under) + AETHRAL (sky), architectural structures designed to be under the open sky.'
            },
            'hypallage': {
                'definition': 'Hypallage is a figure of speech in which the natural or logical relationship between two elements in a sentence is reversed or displaced, often involving the transfer of an adjective or modifier from the word it logically describes to another word in the same phrase. This rhetorical device creates emphasis, poetic effect, or memorable expression by deliberately misplacing descriptive elements in ways that are grammatically incorrect but stylistically effective. Common examples include phrases like "sleepless night" (where the person, not the night, is sleepless) or "restless sea" (where the sea\'s movement creates restlessness rather than the sea itself being restless). Latin poetry frequently employed hypallage as a sophisticated literary technique that compressed meaning while creating distinctive and memorable phrasing that demonstrated the poet\'s skill with language. The device can also appear in everyday speech where emotional intensity or poetic expression takes precedence over logical grammatical relationships. Understanding hypallage requires recognizing the difference between literal grammatical correctness and the expressive power that comes from deliberately disrupting expected word relationships. This rhetorical figure demonstrates how language can be manipulated for artistic effect, creating meaning and impact through creative misalignment of grammatical elements rather than through logical precision.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hahy-PAL-uh-jee',
                'etymology': 'From Greek "hypallage," meaning "exchange" or "interchange," referring to the exchange of grammatical relationships.',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'The poet used _______ in the phrase "guilty conscience" where the person, not the conscience, feels guilt.',
                'memory_tip': 'Remember "HYPALLAGE" - sounds like "HYP-exchange," a figure of speech that exchanges or switches the normal grammatical relationships between words.'
            },
            'hyperion': {
                'definition': 'Hyperion refers to a Titan in Greek mythology, one of the twelve Titans who were the children of Gaia (Earth) and Uranus (Sky), specifically associated with heavenly light and celestial observation. This mythological figure was the father of Helios (the Sun), Selene (the Moon), and Eos (the Dawn), making him a primordial deity connected to astronomical phenomena and the regulation of time through celestial movements. The name Hyperion means "the high one" or "he who goes above," reflecting his elevated status among the Titans and his association with celestial heights and cosmic order. In astronomy, Hyperion is also the name of one of Saturn\'s moons, discovered in 1848, which is notable for its irregular shape, chaotic rotation, and unusual surface composition. Literary references to Hyperion include John Keats\' unfinished epic poems "Hyperion" and "The Fall of Hyperion," which explore themes of divine power, artistic creation, and the relationship between gods and mortals. The name appears in various cultural contexts as a symbol of elevated status, celestial connection, or supreme authority. Understanding Hyperion involves appreciating both its mythological significance in ancient Greek cosmology and its continued cultural relevance as a symbol of transcendent power and cosmic order.',
                'part_of_speech': 'proper noun',
                'pronunciation_guide': 'hahy-PEER-ee-uhn',
                'etymology': 'From Greek "Hyperion," meaning "the high one" or "he who goes above," referring to a Titan associated with light.',
                'language_origins': 'Greek',
                'example_sentence': 'The astronomy class learned about _______, both as a Titan in Greek mythology and as one of Saturn\'s irregularly shaped moons.',
                'memory_tip': 'Remember "HYPERION" - HYPER (above/high) + ION, the mythological Titan who was "the high one" associated with celestial light.'
            },
            'hypertrophy': {
                'definition': 'Hypertrophy refers to the enlargement or overgrowth of an organ, tissue, or body part due to the increase in size of individual cells rather than an increase in their number. This biological process occurs as an adaptive response to increased functional demands, hormonal stimulation, or pathological conditions that require enhanced performance from specific tissues. Muscle hypertrophy is a common example where regular resistance training causes muscle fibers to increase in size, resulting in larger, stronger muscles that can handle greater physical demands. Cardiac hypertrophy involves thickening of heart muscle walls, which can be beneficial in athletes but problematic when caused by high blood pressure or heart disease. Pathological hypertrophy can occur in various organs including the prostate, liver, or kidney when disease processes or abnormal conditions stimulate excessive growth. The process involves increased protein synthesis, cellular metabolism, and structural development within existing cells rather than creation of new cells, which would be called hyperplasia. Understanding hypertrophy is important in medicine, exercise science, and pathology for recognizing both beneficial adaptations and problematic disease processes. Treatment approaches for pathological hypertrophy focus on addressing underlying causes while managing symptoms and preventing complications from abnormal tissue enlargement.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hahy-PUR-truh-fee',
                'etymology': 'From Greek "hyper" (excessive) and "trophe" (nourishment), referring to excessive growth or nourishment.',
                'language_origins': 'Greek',
                'example_sentence': 'The bodybuilder achieved significant muscle _______ through consistent weight training and proper nutrition.',
                'memory_tip': 'Remember "HYPERTROPHY" - HYPER (excessive) + TROPHY (growth prize), excessive growth of tissues like winning a trophy for getting bigger.'
            },
            'hypnotic': {
                'definition': 'Hypnotic describes something that induces sleep, trance-like states, or altered consciousness, particularly referring to medications, techniques, or phenomena that promote relaxation, drowsiness, or hypnotic states. In medical contexts, hypnotic drugs are sedatives specifically designed to help people fall asleep and maintain sleep, differing from other sedatives by their primary focus on sleep induction rather than general calming effects. Hypnotic medications include various classes of drugs such as benzodiazepines, non-benzodiazepine sleep aids, and other substances that act on brain neurotransmitter systems to promote sleep onset and duration. The term also describes the practice and effects of hypnosis, where specially trained practitioners guide individuals into focused, relaxed states of consciousness that may increase suggestibility and enable therapeutic interventions. Hypnotic states can occur naturally through repetitive activities, meditation, or exposure to rhythmic stimuli that induce trance-like consciousness. Beyond medical and therapeutic contexts, hypnotic can describe anything that has a mesmerizing, captivating, or entrancing quality that holds attention and creates absorption or fascination. Understanding hypnotic effects involves recognizing both their therapeutic potential for treating sleep disorders and anxiety, and the need for proper medical supervision due to potential dependency and side effects.',
                'part_of_speech': 'adjective, noun',
                'pronunciation_guide': 'hip-NOT-ik',
                'etymology': 'From Greek "hypnotikos," from "hypnos" meaning "sleep," referring to sleep-inducing properties.',
                'language_origins': 'Greek',
                'example_sentence': 'The doctor prescribed a mild _______ medication to help the patient overcome chronic insomnia.',
                'memory_tip': 'Remember "HYPNOTIC" - from Greek "hypnos" (sleep), something that puts you to sleep or in a trance-like state.'
            },
            'hypoallergenic': {
                'definition': 'Hypoallergenic describes products, materials, or substances that are less likely to cause allergic reactions in sensitive individuals, though the term does not guarantee complete prevention of allergic responses. This marketing and medical term applies to cosmetics, fabrics, pet breeds, foods, and other consumer goods that have been formulated or selected to minimize common allergens and irritating ingredients. Hypoallergenic products typically avoid known allergens such as fragrances, dyes, harsh chemicals, or specific proteins that commonly trigger sensitivities in susceptible people. The development of hypoallergenic products involves identifying and eliminating ingredients most likely to cause reactions, using gentler alternatives, and sometimes conducting testing to verify reduced allergenic potential. However, individual sensitivities vary greatly, and products labeled as hypoallergenic may still cause reactions in some people depending on their specific allergies and sensitivities. Medical professionals recommend patch testing or gradual introduction of new hypoallergenic products for people with known sensitivities to ensure individual tolerance. The term has regulatory limitations in many countries, as there is no standardized definition or testing requirement for hypoallergenic claims. Understanding hypoallergenic labeling helps consumers make informed choices while recognizing that individual testing and medical guidance remain important for managing allergies and sensitivities.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'hahy-poh-al-er-JEN-ik',
                'etymology': 'From Greek "hypo" (under/less) + "allergenic," meaning less likely to cause allergic reactions.',
                'language_origins': 'Greek, modern medical terminology',
                'example_sentence': 'The dermatologist recommended _______ skincare products to reduce the patient\'s risk of developing contact dermatitis.',
                'memory_tip': 'Remember "HYPOALLERGENIC" - HYPO (less) + ALLERGENIC, products that are less likely to cause allergic reactions.'
            },
            'hypocaust': {
                'definition': 'Hypocaust was an ancient Roman heating system that provided underfloor heating for buildings by circulating hot air through spaces beneath floors and within walls. This sophisticated engineering system worked by burning fuel in a furnace that heated air, which then flowed through raised floors supported by pillars and hollow wall spaces, providing efficient and comfortable heating for homes, baths, and public buildings. The hypocaust system demonstrated remarkable Roman engineering expertise and understanding of thermodynamics, creating comfortable indoor environments even during cold weather. Wealthy Roman homes, public bathhouses, and important buildings throughout the Roman Empire featured hypocaust heating systems that provided luxury and comfort unavailable in most other contemporary civilizations. The system required skilled construction techniques including waterproof flooring, proper ventilation, fire safety measures, and maintenance access for cleaning and repairs. Archaeological evidence shows hypocaust systems in Roman settlements throughout Europe, North Africa, and the Middle East, demonstrating the widespread adoption of this technology. Modern radiant heating systems use similar principles of circulating warm air or water beneath floors, showing the enduring validity of Roman engineering concepts. Understanding hypocaust systems provides insights into Roman technology, lifestyle, and the engineering capabilities that supported their extensive empire and urban development.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAHY-puh-kawst',
                'etymology': 'From Greek "hypokauston," from "hypo" (under) and "kauston" (burnt), referring to burning under floors.',
                'language_origins': 'Greek, Latin',
                'example_sentence': 'Archaeologists discovered the remains of a Roman _______ system that once heated the floors of the ancient villa.',
                'memory_tip': 'Remember "HYPOCAUST" - HYPO (under) + CAUST (burning), Roman heating system that burned fuel under floors.'
            },
            'hypochondria': {
                'definition': 'Hypochondria, now more commonly known as illness anxiety disorder, is a psychological condition characterized by excessive worry and preoccupation with having or developing serious medical conditions despite little or no medical evidence of actual disease. Individuals with this condition interpret normal bodily sensations, minor symptoms, or temporary discomfort as signs of severe illness, leading to persistent anxiety, frequent medical consultations, and significant disruption of daily functioning. The condition involves cognitive distortions where people catastrophically interpret physical sensations, overestimate health risks, and remain unconvinced by medical reassurance or normal test results. Hypochondria can severely impact quality of life, relationships, and work performance as individuals become consumed with health fears and medical seeking behaviors. The condition differs from malingering or factitious disorders because the anxiety and concern are genuine, not feigned or deliberately produced. Treatment typically involves cognitive-behavioral therapy to address catastrophic thinking patterns, reduce excessive health monitoring behaviors, and develop more realistic health assessment skills. Understanding hypochondria requires recognizing the genuine distress experienced by affected individuals while distinguishing between realistic health concerns and excessive anxiety that interferes with normal functioning. Modern approaches emphasize compassionate treatment that validates concerns while helping people develop healthier relationships with their physical sensations and medical care.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hahy-puh-KON-dree-uh',
                'etymology': 'From Greek "hypochondrion," referring to the area under the rib cartilage, once thought to be the seat of melancholy.',
                'language_origins': 'Greek',
                'example_sentence': 'The patient\'s _______ led her to seek multiple medical opinions for minor symptoms that were actually normal bodily sensations.',
                'memory_tip': 'Remember "HYPOCHONDRIA" - from Greek area under ribs once thought to cause excessive worry about health and imaginary illnesses.'
            },
            'hypogeous': {
                'definition': 'Hypogeous describes organisms, structures, or processes that occur underground or below the earth\'s surface, particularly in botanical contexts where it refers to seeds that germinate below ground level. This scientific term applies to various biological phenomena including hypogeous germination where seed cotyledons remain underground during sprouting, contrasting with epigeous germination where cotyledons emerge above ground. Many plant species exhibit hypogeous development as an adaptation to specific environmental conditions, providing protection from surface hazards such as frost, herbivores, or mechanical damage during early growth stages. The term also applies to fungi, bacteria, and other organisms that complete their life cycles primarily in underground environments, including various soil microorganisms essential for ecosystem functioning. Archaeological contexts use hypogeous to describe underground structures, burial chambers, or other human-made subterranean features that were deliberately constructed below ground level. Understanding hypogeous phenomena is important for botany, ecology, agriculture, and archaeology as it helps explain plant development strategies, soil ecosystem dynamics, and human construction practices. The concept relates to broader understanding of how organisms adapt to different environmental zones and utilize underground resources and protection. Modern applications include studying root development, soil biology, and underground construction techniques.',
                'part_of_speech': 'adjective',
                'pronunciation_guide': 'hahy-puh-JEE-uhs',
                'etymology': 'From Greek "hypo" (under) and "ge" (earth), literally meaning "under the earth."',
                'language_origins': 'Greek',
                'example_sentence': 'The botany students studied _______ germination in peas, where the cotyledons remain underground during sprouting.',
                'memory_tip': 'Remember "HYPOGEOUS" - HYPO (under) + GEOUS (earth), describing things that happen under the earth or underground.'
            },
            'hypotenuse': {
                'definition': 'Hypotenuse is the longest side of a right triangle, located opposite the right angle and connecting the two shorter sides (called legs) in this fundamental geometric shape. This concept is central to trigonometry and the Pythagorean theorem, which states that the square of the hypotenuse equals the sum of squares of the other two sides (a² + b² = c²). Understanding the hypotenuse is essential for solving problems involving distance, navigation, construction, engineering, and any application requiring calculation of diagonal measurements or relationships between perpendicular dimensions. The hypotenuse serves as the basis for defining trigonometric ratios including sine, cosine, and tangent that relate angles to side lengths in right triangles. Real-world applications include calculating diagonal distances across rectangular spaces, determining slope angles in construction, navigation using triangulation, and engineering problems involving force vectors and structural analysis. The concept appears in advanced mathematics including coordinate geometry where the distance formula derives from Pythagorean relationships, and in physics where vector calculations often involve right triangle relationships. Historical significance includes ancient civilizations using hypotenuse relationships for surveying, construction, and astronomical calculations. Understanding hypotenuse properties and calculations provides foundation for advanced mathematics, physics, engineering, and practical problem-solving in numerous technical fields.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'hahy-POT-uh-noos',
                'etymology': 'From Greek "hypoteinousa," meaning "stretching under," referring to the side that stretches under the right angle.',
                'language_origins': 'Greek',
                'example_sentence': 'The student used the Pythagorean theorem to calculate the length of the triangle\'s _______ given the two shorter sides.',
                'memory_tip': 'Remember "HYPOTENUSE" - sounds like "HIP-to-NOOSE," the longest side that stretches from hip to hip across the right angle.'
            },
            'hyrax': {
                'definition': 'Hyrax refers to small, furry mammals belonging to the order Hyracoidea, found primarily in Africa and the Middle East, characterized by their compact bodies, short tails, and surprising evolutionary relationship to elephants despite their rodent-like appearance. These remarkable animals are the closest living relatives to elephants and manatees, sharing common ancestors despite their dramatically different sizes and lifestyles. Hyraxes inhabit various environments including rocky outcrops, trees, and scrublands, where they live in social groups and feed primarily on vegetation including leaves, bark, fruits, and grasses. Different species include rock hyraxes that live in colonial groups on cliff faces, bush hyraxes that are more solitary and arboreal, and tree hyraxes that are nocturnal forest dwellers. Despite their small size, hyraxes have unique anatomical features including continuously growing incisors, specialized feet with rubbery pads for climbing, and complex stomach chambers for digesting plant material. These animals play important ecological roles as herbivores and prey species while serving as indicators of habitat health in their native environments. Hyrax populations face threats from habitat destruction, hunting, and climate change, making conservation efforts important for maintaining ecosystem balance. Understanding hyraxes provides insights into evolutionary relationships, adaptive radiation, and the importance of protecting diverse mammalian species.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HAHY-raks',
                'etymology': 'From Greek "hyrax" meaning "shrew mouse," though they are not related to shrews or mice.',
                'language_origins': 'Greek',
                'example_sentence': 'The wildlife biologist was excited to observe a colony of rock _______ sunbathing on the cliffs in their natural habitat.',
                'memory_tip': 'Remember "HYRAX" - sounds like "HI-RACKS," small mammals that rack up on rocks and are surprisingly related to elephants.'
            },
            'hyssop': {
                'definition': 'Hyssop refers to aromatic perennial herbs belonging to the mint family, particularly Hyssopus officinalis, known for their medicinal properties, culinary uses, and historical significance in religious and cultural traditions. This Mediterranean plant produces small blue, pink, or white flowers and has been cultivated for centuries for its essential oils, which contain compounds with antimicrobial, anti-inflammatory, and expectorant properties. Traditional medicinal uses of hyssop include treating respiratory conditions, digestive problems, and wounds, though modern medical applications require careful evaluation and professional guidance. The herb appears frequently in religious texts including the Bible, where it was used in purification rituals and ceremonial practices, giving it significant cultural and spiritual symbolism. Culinary applications include using fresh or dried hyssop leaves as seasoning for meats, vegetables, and herbal teas, providing a slightly bitter, minty flavor that complements various dishes. Garden cultivation of hyssop is relatively easy as the plant adapts to various soil conditions, attracts beneficial pollinators, and can serve both ornamental and practical purposes in herb gardens. Essential oil production from hyssop provides aromatherapy applications, though concentrated oils require careful handling and dilution for safe use. Understanding hyssop involves appreciating both its practical applications and its rich cultural history that connects contemporary herbal use with ancient traditions.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'HIS-uhp',
                'etymology': 'From Greek "hyssopos," from Hebrew "ezob," referring to this aromatic herb used in religious purification.',
                'language_origins': 'Hebrew, Greek, Latin',
                'example_sentence': 'The herbalist grew _______ in her garden for making traditional teas and natural remedies for respiratory ailments.',
                'memory_tip': 'Remember "HYSSOP" - sounds like "HIS-sop," an herb that was his (ancient people\'s) sop or remedy for various ailments.'
            },
            'hysteresis': {
                'definition': 'Hysteresis refers to the phenomenon where a system\'s output depends not only on its current input but also on its history of previous inputs, creating a lag between cause and effect that results in different behavior during loading and unloading cycles. This concept appears in various fields including physics, engineering, biology, and economics, where systems exhibit memory effects that influence their response to changing conditions. In magnetism, hysteresis describes how magnetic materials retain some magnetization even after the external magnetic field is removed, creating a characteristic loop when plotting magnetic field strength against magnetization. Engineering applications include understanding how materials respond to stress and strain cycles, where loading and unloading follow different paths due to internal friction, plastic deformation, or other irreversible processes. Economic hysteresis occurs when temporary economic shocks create permanent changes in employment levels, productivity, or other economic indicators that persist even after the original cause is removed. Biological systems exhibit hysteresis in various processes including enzyme reactions, population dynamics, and cellular responses where past conditions influence current behavior. Understanding hysteresis is crucial for designing control systems, predicting material behavior, and modeling complex systems where history matters. The concept helps explain why simply reversing conditions doesn\'t always restore original states, requiring more sophisticated approaches to system control and prediction.',
                'part_of_speech': 'noun',
                'pronunciation_guide': 'his-tuh-REE-sis',
                'etymology': 'From Greek "hysteresis" meaning "deficiency" or "lagging behind," referring to the lag between cause and effect.',
                'language_origins': 'Greek',
                'example_sentence': 'The engineer had to account for _______ in the magnetic materials to ensure the motor would perform consistently.',
                'memory_tip': 'Remember "HYSTERESIS" - sounds like "HISTORY-esis," where the history of inputs affects current system behavior, creating a lag.'
            },
            'hysteron': {
                'definition': 'Hysteron typically appears as part of "hysteron proteron," a rhetorical figure where the natural or logical order of events, ideas, or words is deliberately reversed for emphasis, dramatic effect, or artistic purpose. This Greek rhetorical term literally means "latter former," describing situations where what should come later is placed first, creating a reversal that can enhance meaning, create emphasis, or produce memorable expression. The device appears in literature when authors describe effects before causes, conclusions before premises, or later events before earlier ones to create specific impacts on readers. Examples include phrases like "let us die and rush into battle" where dying (the result) is mentioned before fighting (the cause), or "put on your shoes and socks" where the final action precedes the preliminary one. Hysteron proteron can occur intentionally as a sophisticated literary technique or unintentionally in speech when excitement, emotion, or urgency disrupts logical sequencing. Understanding this rhetorical figure requires recognizing both its deliberate artistic applications and its occasional appearance in natural speech patterns where emphasis takes precedence over logical order. The concept demonstrates how language can be manipulated for effect by violating expected temporal or logical sequences while maintaining comprehensibility and often achieving greater impact than conventional ordering would provide.',
                'part_of_speech': 'noun (part of phrase)',
                'pronunciation_guide': 'HIS-ter-on',
                'etymology': 'From Greek "hysteron" meaning "latter" or "subsequent," used in the phrase "hysteron proteron" (latter former).',
                'language_origins': 'Greek',
                'example_sentence': 'The poet used _______ proteron by describing the victory celebration before mentioning the battle itself.',
                'memory_tip': 'Remember "HYSTERON" - from Greek "latter," part of "hysteron proteron" where the latter thing is mentioned first, reversing logical order.'
            }
        }
        
        return batch_087_data.get(word.lower(), {
            'definition': 'Definition not available for this word.',
            'part_of_speech': 'unknown',
            'pronunciation_guide': 'Pronunciation not available',
            'etymology': 'Etymology not available',
            'language_origins': 'Unknown',
            'example_sentence': 'Example sentence not available for _______.',
            'memory_tip': 'Memory tip not available for this word.'
        })

    def process_batch(self, input_file: str, output_file: str) -> None:
        print(f"Processing {input_file}...")
        
        try:
            df = pd.read_csv(input_file)
            
            processed_words = []
            word_count = 0
            
            for _, row in df.iterrows():
                word = str(row['word']).strip()
                if not word or word.lower() == 'nan':
                    continue
                    
                word_count += 1
                
                if self.is_error_word(word):
                    self.errors.append(self.detect_word_error(word))
                
                claude_data = self.get_comprehensive_claude_data(word)
                
                word_data = WordData(
                    word=word,
                    definition=claude_data['definition'],
                    part_of_speech=claude_data['part_of_speech'],
                    pronunciation_guide=claude_data['pronunciation_guide'],
                    etymology=claude_data['etymology'],
                    language_origins=claude_data['language_origins'],
                    example_sentence=claude_data['example_sentence'],
                    memory_tip=claude_data['memory_tip'],
                    phonetic_transparency=self.difficulty_calc.calculate_phonetic_transparency(word),
                    word_frequency=self.difficulty_calc.calculate_word_frequency(word),
                    morphological_complexity=self.difficulty_calc.calculate_morphological_complexity(word),
                    etymology_complexity=self.difficulty_calc.calculate_etymology_complexity(word)
                )
                
                processed_words.append(word_data)
            
            output_data = []
            for word_data in processed_words:
                output_data.append({
                    'word': word_data.word,
                    'definition': word_data.definition,
                    'part_of_speech': word_data.part_of_speech,
                    'pronunciation_guide': word_data.pronunciation_guide,
                    'etymology': word_data.etymology,
                    'language_origins': word_data.language_origins,
                    'example_sentence': word_data.example_sentence,
                    'memory_tip': word_data.memory_tip,
                    'phonetic_transparency': word_data.phonetic_transparency,
                    'word_frequency': word_data.word_frequency,
                    'morphological_complexity': word_data.morphological_complexity,
                    'etymology_complexity': word_data.etymology_complexity,
                    'difficulty_level': None,
                    'source_difficulties': row.get('source_difficulties', ''),
                    'years': row.get('years', ''),
                    'source_files': row.get('source_files', ''),
                    'definition_source': 'Claude',
                    'pronunciation_source': 'Claude',
                    'etymology_source': 'Claude',
                    'example_sentence_source': 'Claude',
                    'audio_file_path': None,
                    'created_at': None,
                    'updated_at': None,
                    'alternative_spellings': None,
                    'related_words': None,
                    'usage_notes': None
                })
            
            output_df = pd.DataFrame(output_data)
            output_df.to_csv(output_file, index=False, encoding='utf-8')
            
            print(f"Successfully processed {word_count}/50 words to {output_file}")
            
            if self.errors:
                print(f"Found {len(self.errors)} error(s):")
                for error in self.errors:
                    print(f"  - {error}")
            
            print("Batch 087 processing completed successfully!")
            
        except Exception as e:
            print(f"Error processing batch 087: {str(e)}")
            raise

    def is_error_word(self, word: str) -> bool:
        error_patterns = [
            lambda w: len(w) > 20 and any(common in w.lower() for common in 
                ['difficulty', 'diligence', 'different', 'decision', 'development', 'discussion']),
            lambda w: any(combo in w.lower() for combo in 
                ['anearly', 'anadequate', 'anational', 'anhonest', 'anindependent']),
            lambda w: w.count('a') > 4 and len(w) > 15,
            lambda w: 'difficulty' in w.lower() and w.lower() != 'difficulty',
            lambda w: len([c for c in w if c.islower()]) > len(w) * 0.9 and len(w) > 25
        ]
        
        return any(pattern(word) for pattern in error_patterns)

    def detect_word_error(self, word: str) -> str:
        if 'difficulty' in word.lower() and word.lower() != 'difficulty':
            parts = word.lower().split('difficulty')
            return f'{word}: Combined word error: "{word}" appears to be "{parts[0]}" + "difficulty" merged together. This is likely a PDF parsing error where two separate concepts were incorrectly combined.'
        
        common_endings = ['ness', 'tion', 'sion', 'ment', 'able', 'ible', 'ence', 'ance']
        for ending in common_endings:
            if word.lower().endswith(ending):
                base = word.lower()[:-len(ending)]
                if len(base) > 8:
                    return f'{word}: Possible combined word error: "{word}" may contain merged terms. This is likely a PDF parsing error where separate words were incorrectly combined.'
        
        return f'{word}: Combined word error: This appears to be multiple words merged together during PDF processing.'

if __name__ == "__main__":
    processor = Batch087Processor()
    input_file = "output/batch_087_words.csv"
    output_file = "output/batch_087_processed.csv"
    processor.process_batch(input_file, output_file)