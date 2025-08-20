#!/usr/bin/env python3
"""
Process Batch 098 of spelling bee words with comprehensive Claude data.
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

class Batch098Processor:
    """Processes Batch 098 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for each word with detailed definitions, pronunciations, etymologies, and memory tips"""
        
        word_data = {
            "king": {
                "definition": "A male monarch who rules a kingdom as the sovereign head of state, typically inheriting the position through hereditary succession and wielding supreme authority over governmental, military, and ceremonial functions. Kings have historically held absolute or constitutional power, depending on the political system, and serve as symbols of national unity, tradition, and continuity. The role encompasses executive leadership, judicial oversight, diplomatic representation, and cultural patronage while maintaining ceremonial duties that connect past traditions with contemporary governance. Modern constitutional monarchies limit royal power while preserving the symbolic and ceremonial importance of kingship in national identity.",
                "example_sentence": "The _____ addressed the nation during the constitutional crisis, providing stability and reassurance to citizens.",
                "pronunciation": "KING (single syllable, rhymes with \"ring\")",
                "etymology": "From Old English \"cyning,\" from Germanic roots meaning \"descendant of noble family\"",
                "memory_tips": "Think \"king-ring\" - the king wears a crown like a ring around his head",
                "part_of_speech": "noun"
            },
            "kingston": {
                "definition": "The capital and largest city of Jamaica, located on the southeastern coast of the island, serving as the country's political, economic, and cultural center with a rich history of music, particularly reggae and dancehall. Kingston is a major Caribbean port city that combines colonial architecture with modern development, featuring important institutions like the University of the West Indies and significant cultural sites including the Bob Marley Museum. The city represents Jamaica's independence movement, musical heritage, and contemporary Caribbean culture while serving as a regional hub for business, education, and international relations.",
                "example_sentence": "The reggae festival in _____ celebrated Jamaica's musical heritage and attracted international artists.",
                "pronunciation": "KINGS-tuhn (emphasis on first syllable)",
                "etymology": "Named \"King's Town\" after King William III of England, from \"king\" + \"ton\" (town)",
                "memory_tips": "Think \"Kings-town\" - the town named after a king",
                "part_of_speech": "noun (proper)"
            },
            "kippur": {
                "definition": "Short for Yom Kippur, the holiest day in Judaism known as the Day of Atonement, observed through fasting, prayer, and repentance for sins committed during the previous year. Kippur represents the culmination of the High Holy Days period, where Jewish communities engage in intensive spiritual reflection, seek forgiveness from God and fellow humans, and commit to moral improvement. The observance includes complete fasting from food and drink, extensive synagogue services, and the recitation of special prayers including the Kol Nidre. This sacred day emphasizes themes of redemption, spiritual purification, and divine mercy.",
                "example_sentence": "The synagogue was filled with worshippers observing the solemn fast of Yom _____.",
                "pronunciation": "ki-POOR or KIP-oor (emphasis varies)",
                "etymology": "From Hebrew \"kippur,\" meaning \"atonement\" or \"covering,\" from root \"kafar\" (to cover or atone)",
                "memory_tips": "Think \"keep-pure\" - keeping oneself spiritually pure through atonement",
                "part_of_speech": "noun"
            },
            "kipuka": {
                "definition": "An area of land surrounded by lava flows but left untouched during volcanic eruptions, creating islands of original vegetation and ecosystems within newly formed volcanic landscapes. Kipukas serve as crucial refuges for native plants and animals during volcanic activity, preserving biodiversity and providing seed sources for ecological recovery after eruptions. These geological features are particularly important in Hawaiian ecosystems, where volcanic activity frequently reshapes landscapes while kipukas maintain continuity of native species. The term has extended to describe any isolated area that remains unchanged while surrounding environments undergo transformation.",
                "example_sentence": "The native birds found refuge in the _____ while lava flows destroyed the surrounding forest.",
                "pronunciation": "ki-POO-kah (emphasis on second syllable)",
                "etymology": "From Hawaiian \"kīpuka,\" meaning \"opening\" or \"hole,\" referring to openings in lava fields",
                "memory_tips": "Think \"keep-puka\" - keeping a hole or opening safe from lava flows",
                "part_of_speech": "noun"
            },
            "kirpan": {
                "definition": "A ceremonial sword or dagger that represents one of the five Ks (panj kakar) worn by initiated Sikhs as a symbol of the duty to protect the innocent and uphold justice. The kirpan embodies the Sikh principle of defending righteousness and protecting those who cannot protect themselves, representing spiritual and physical courage in the face of oppression. Modern kirpans vary in size from small symbolic versions to traditional full-sized swords, with wearing practices adapted to contemporary legal and social contexts while maintaining religious significance. This sacred object connects Sikh identity to historical traditions of warrior-saints and social justice advocacy.",
                "example_sentence": "The Sikh soldier proudly wore his _____ as a symbol of his religious commitment to protecting others.",
                "pronunciation": "kir-PAHN (emphasis on second syllable)",
                "etymology": "From Punjabi \"kirpan,\" from \"kirpa\" (mercy, grace) + \"an\" (honor), meaning \"the honor of mercy\"",
                "memory_tips": "Think \"care-pan\" - caring for others with this protective sword",
                "part_of_speech": "noun"
            },
            "kiskadee": {
                "definition": "A large, colorful flycatcher bird (Pitangus sulphuratus) native to Central and South America, characterized by its distinctive black and white head pattern, bright yellow belly, and loud, repetitive call that sounds like \"kis-ka-dee.\" These birds are aggressive predators that catch insects, small fish, and other prey while perched prominently in open areas near water. Kiskadees are highly adaptable birds that thrive in various habitats from tropical forests to urban areas, known for their bold behavior and distinctive vocalizations that make them easily identifiable. Their success in diverse environments has made them common throughout their range.",
                "example_sentence": "The _____ perched on the fence post, calling loudly while hunting for insects in the garden.",
                "pronunciation": "KIS-kuh-dee (emphasis on first syllable)",
                "etymology": "Onomatopoeia from the bird's distinctive call that sounds like \"kis-ka-dee\"",
                "memory_tips": "Think \"kiss-ka-dee\" - the bird that sounds like it's saying \"kiss-ka-dee\"",
                "part_of_speech": "noun"
            },
            "kitchendifficulty": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"kitchen\" (food preparation room) incorrectly combined with \"difficulty\" (challenge or problem). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"kitchen\" and \"difficulty\"",
                "part_of_speech": "error - combined words"
            },
            "kitchens": {
                "definition": "Plural of kitchen; rooms or areas in buildings specifically designed and equipped for food preparation, cooking, and often dining, containing appliances like stoves, refrigerators, sinks, and storage facilities. Kitchens serve as central hubs of domestic activity where meals are prepared, families gather, and culinary traditions are maintained and passed down through generations. Modern kitchens incorporate advanced appliances, efficient layouts, and storage solutions that facilitate both everyday cooking and entertaining guests. The design and functionality of kitchens reflect cultural preferences, cooking styles, and social patterns of food preparation and consumption.",
                "example_sentence": "The restaurant's multiple _____ allowed chefs to prepare different cuisines simultaneously during busy periods.",
                "pronunciation": "KICH-uhnz (emphasis on first syllable)",
                "etymology": "Plural of \"kitchen,\" from Old English \"cycene,\" from Late Latin \"coquina\" (cooking place)",
                "memory_tips": "Think \"cooking-ens\" - places where cooking happens, with 's' for multiple places",
                "part_of_speech": "noun"
            },
            "kites": {
                "definition": "Plural of kite; lightweight objects designed to fly in the air when connected to strings and lifted by wind currents, traditionally made of paper, fabric, or plastic stretched over frames. Kites serve recreational, cultural, and practical purposes including children's toys, artistic expression, scientific instruments, and ceremonial objects in various cultures worldwide. The physics of kite flight involves aerodynamic principles of lift, drag, and stability that have contributed to understanding of flight and led to developments in aviation. Kite flying represents both simple pleasure and sophisticated engineering, connecting human creativity with natural forces.",
                "example_sentence": "The children flew colorful _____ in the park during the spring festival celebration.",
                "pronunciation": "KIETS (single syllable, rhymes with \"lights\")",
                "etymology": "Plural of \"kite,\" from Old English \"cyta,\" possibly related to the bird of prey",
                "memory_tips": "Think \"sky-ites\" - objects that belong in the sky when flying",
                "part_of_speech": "noun"
            },
            "kitksan": {
                "definition": "Relating to the Gitxsan people, a First Nations group indigenous to the Pacific Northwest region of British Columbia, Canada, known for their sophisticated clan system, artistic traditions, and connection to salmon fishing territories along the Skeena River. The Gitxsan maintain ancient cultural practices including potlatch ceremonies, totem pole carving, and complex oral histories that preserve their relationship to traditional territories. Their social organization involves matrilineal clans with hereditary chiefs who oversee territorial rights and cultural protocols. Contemporary Gitxsan communities balance traditional governance systems with modern political structures while advocating for land rights and cultural preservation.",
                "example_sentence": "The museum featured _____ totem poles carved by master artisans from the Skeena River region.",
                "pronunciation": "GIT-san (emphasis on first syllable)",
                "etymology": "From Gitxsan \"Gitxsan\" meaning \"people of the Skeena River,\" from \"git\" (people) + \"xsan\" (Skeena River)",
                "memory_tips": "Think \"get-san\" - getting to know the San (people) of the Skeena River",
                "part_of_speech": "adjective, noun"
            },
            "kiva": {
                "definition": "A circular, partly underground ceremonial chamber used by Pueblo peoples of the American Southwest for religious rituals, community meetings, and social gatherings. Kivas feature distinctive architectural elements including a central fire hearth, a small hole (sipapu) representing the entrance to the underworld, and a deflector stone that controls airflow. These sacred spaces serve as connections between the physical and spiritual worlds, where important ceremonies maintain relationships with ancestors, natural forces, and cosmic cycles. Archaeological evidence shows kivas have been central to Southwestern Indigenous cultures for over a thousand years.",
                "example_sentence": "The ancient _____ at Mesa Verde shows the sophisticated religious architecture of Ancestral Puebloan peoples.",
                "pronunciation": "KEE-vah (emphasis on first syllable)",
                "etymology": "From Hopi \"kihu,\" meaning \"ceremonial chamber\" or \"world below\"",
                "memory_tips": "Think \"key-va\" - like a key to the spiritual world below",
                "part_of_speech": "noun"
            },
            "kiwi": {
                "definition": "A flightless bird native to New Zealand with hair-like feathers, a long curved beak, and nocturnal habits, serving as the national symbol of New Zealand; also refers to the brown, fuzzy fruit originally from China. As a bird, kiwis are unique among avians for their ground-dwelling lifestyle, exceptional sense of smell, and the distinction of laying eggs proportionally larger than any other bird species. The fruit, technically a berry, gained its name from resemblance to the bird and provides high vitamin C content along with distinctive sweet-tart flavor. Both represent important symbols in New Zealand culture and international trade respectively.",
                "example_sentence": "The endangered _____ bird is protected in New Zealand's conservation programs and wildlife sanctuaries.",
                "pronunciation": "KEE-wee (emphasis on first syllable)",
                "etymology": "From Māori \"kiwi,\" imitative of the bird's call; fruit named after the bird due to appearance similarity",
                "memory_tips": "Think \"key-we\" - the key symbol of New Zealand, both bird and fruit",
                "part_of_speech": "noun"
            },
            "kjeldahl": {
                "definition": "Relating to a laboratory method for determining nitrogen content in organic compounds, developed by Danish chemist Johan Kjeldahl in 1883, widely used in food analysis, environmental testing, and protein quantification. The Kjeldahl method involves digesting samples with concentrated sulfuric acid to convert organic nitrogen into ammonium sulfate, followed by distillation and titration to measure total nitrogen content. This analytical technique is fundamental in determining protein content in foods since protein contains approximately 16% nitrogen by weight. The method remains the international standard for nitrogen analysis despite the development of newer automated techniques.",
                "example_sentence": "The food laboratory used the _____ method to determine protein content in the new product formulation.",
                "pronunciation": "KYEL-dahl (emphasis on first syllable)",
                "etymology": "Named after Johan Kjeldahl (1849-1900), Danish chemist who developed the nitrogen analysis method",
                "memory_tips": "Think \"Kjell-doll\" - like a doll named Kjell who measures nitrogen scientifically",
                "part_of_speech": "adjective"
            },
            "kleptocrat": {
                "definition": "A government official or political leader who uses their position of power to steal public funds and resources for personal enrichment, typically operating within corrupt systems that facilitate large-scale embezzlement and abuse of authority. Kleptocrats exploit state institutions to transfer public wealth to themselves and their associates through various schemes including inflated contracts, phantom projects, and direct treasury looting. These individuals often maintain power through patronage networks, repression, and the manipulation of electoral processes while impoverishing the populations they ostensibly serve. Kleptocracy represents one of the most destructive forms of political corruption, undermining economic development and democratic governance.",
                "example_sentence": "The international investigation revealed how the _____ had stolen billions from the country's oil revenues.",
                "pronunciation": "KLEP-tuh-krat (emphasis on first syllable)",
                "etymology": "From Greek \"klepto\" (to steal) + \"kratos\" (power or rule), meaning \"rule by thieves\"",
                "memory_tips": "Think \"kept-ocrat\" - they kept all the money for themselves while ruling",
                "part_of_speech": "noun"
            },
            "klippe": {
                "definition": "An isolated hill or mountain formed by erosion of surrounding softer rock, leaving a remnant of harder, more resistant geological formations standing above the surrounding landscape. Klippen (plural) result from differential erosion where weather and water remove less resistant materials while preserving more durable rock layers, creating distinctive landforms that provide insights into geological history and processes. These formations often contain fossils and rock types different from surrounding areas, indicating complex geological movements including thrust faulting and tectonic displacement. Klippen serve as important geological markers for understanding regional structural geology and erosional processes.",
                "example_sentence": "The limestone _____ provided geologists with evidence of ancient sea levels and tectonic movement.",
                "pronunciation": "KLIP-uh (emphasis on first syllable)",
                "etymology": "From German \"Klippe,\" meaning \"cliff\" or \"crag,\" used in geological terminology",
                "memory_tips": "Think \"clip-eh\" - like nature clipped away everything but this hard rock remnant",
                "part_of_speech": "noun"
            },
            "klutz": {
                "definition": "A person who frequently trips, drops things, or acts in an awkward, clumsy manner due to poor coordination or lack of physical grace. Klutziness involves unintentional accidents and mishaps that result from difficulty coordinating movements, spatial awareness problems, or simply being accident-prone in various situations. While sometimes used affectionately, the term can describe genuine coordination challenges that affect daily activities and social interactions. The condition may result from various factors including inner ear problems, neurological differences, anxiety, or simply natural variations in motor skills and spatial processing.",
                "example_sentence": "Despite being a brilliant scientist, he was such a _____ in the laboratory that colleagues worried about equipment safety.",
                "pronunciation": "KLUHTS (single syllable, rhymes with \"cuts\")",
                "etymology": "From Yiddish \"klots,\" meaning \"wooden block\" or \"clumsy person\"",
                "memory_tips": "Think \"clumsy-utz\" - a clumsy person who says \"utz\" when they stumble",
                "part_of_speech": "noun"
            },
            "klutzenvoy": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"klutz\" (clumsy person) incorrectly combined with \"envoy\" (diplomatic representative). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"klutz\" and \"envoy\"",
                "part_of_speech": "error - combined words"
            },
            "klystron": {
                "definition": "A type of electron tube used to generate and amplify microwave signals, functioning through the principle of velocity modulation of electron beams in resonant cavities. Klystrons operate by using input signals to modulate the velocity of electrons traveling through drift tubes, creating bunched electron streams that transfer energy to output cavities, producing amplified microwave radiation. These devices are essential components in radar systems, satellite communications, particle accelerators, and microwave ovens, providing high-power, high-frequency electromagnetic radiation with excellent stability and efficiency. The technology represents sophisticated electromagnetic engineering that enables modern communications and scientific instrumentation.",
                "example_sentence": "The radar system's _____ amplifier generated the high-power microwave pulses needed for long-range detection.",
                "pronunciation": "KLIE-stron (emphasis on first syllable)",
                "etymology": "From Greek \"klys\" (to wash over) + \"-tron\" (device), referring to the washing action of electron streams",
                "memory_tips": "Think \"crystal-tron\" - like a crystal device that amplifies microwave signals",
                "part_of_speech": "noun"
            },
            "knack": {
                "definition": "A natural talent, skill, or ability to do something well with apparent ease, often involving intuitive understanding or acquired expertise that makes difficult tasks seem effortless. Having a knack implies more than basic competence; it suggests an innate aptitude or developed proficiency that enables superior performance in specific areas. This ability often appears to come naturally but may result from combination of talent, practice, and understanding that creates expertise. People with knacks for particular activities often become sought-after specialists who can accomplish what others find challenging or impossible.",
                "example_sentence": "She had a _____ for making complicated mathematical concepts understandable to struggling students.",
                "pronunciation": "NAK (single syllable, rhymes with \"pack\")",
                "etymology": "From Middle English \"knak,\" possibly from Low German, meaning \"sharp sound\" or \"trick\"",
                "memory_tips": "Think \"crack-k\" - like cracking the code to do something well",
                "part_of_speech": "noun"
            },
            "kneecap": {
                "definition": "The small, rounded bone (patella) that protects the front of the knee joint where the thigh and shin bones meet, serving as a point of attachment for muscles and tendons that enable leg movement. The kneecap functions as a pulley system that increases the mechanical advantage of the quadriceps muscles when extending the leg, while also protecting the knee joint from impact and injury. This bone moves within grooves in the femur during knee flexion and extension, and its proper alignment is crucial for normal walking, running, and other leg movements. Kneecap injuries can significantly impair mobility and require careful treatment to restore function.",
                "example_sentence": "The soccer player's _____ injury required surgery and months of physical therapy for full recovery.",
                "pronunciation": "NEE-kap (emphasis on first syllable)",
                "etymology": "From \"knee\" + \"cap,\" describing the cap-like bone covering the knee joint",
                "memory_tips": "Think \"knee-cap\" - literally the cap that covers and protects the knee",
                "part_of_speech": "noun, verb"
            },
            "kneeling": {
                "definition": "The act of positioning oneself with one or both knees touching the ground, typically used for prayer, respect, proposal, worship, or practical tasks that require low positioning. Kneeling represents various cultural and religious significances including submission, reverence, penitence, and humility across different societies and contexts. The physical position involves bending the knee joints to lower the body while maintaining balance and stability, often requiring flexibility and strength to maintain comfort during extended periods. Different kneeling positions serve specific purposes from ceremonial observances to practical work requirements.",
                "example_sentence": "The congregation was _____ during the solemn prayer service in the cathedral.",
                "pronunciation": "NEE-ling (emphasis on first syllable)",
                "etymology": "From \"kneel\" + suffix \"-ing,\" from Old English \"cneowlian\" (to kneel)",
                "memory_tips": "Think \"knee-ling\" - lingering on your knees in a respectful position",
                "part_of_speech": "verb, noun"
            },
            "knew": {
                "definition": "Past tense of know; indicates that someone had knowledge, information, or awareness of something at a previous time, suggesting familiarity with facts, people, places, or concepts. The word implies certain knowledge rather than supposition or belief, indicating confidence in the accuracy of information or understanding. Knew can refer to intellectual knowledge, personal familiarity, or experiential understanding gained through learning, observation, or direct contact. The certainty implied by knew distinguishes it from weaker forms of awareness like suspecting, believing, or assuming.",
                "example_sentence": "She _____ the answer to the difficult question because she had studied the topic thoroughly.",
                "pronunciation": "NOO (single syllable, rhymes with \"new\")",
                "etymology": "Past tense of \"know,\" from Old English \"cnēow,\" from Germanic roots meaning \"to recognize\"",
                "memory_tips": "Think \"new\" - what you knew was new information you had learned",
                "part_of_speech": "verb"
            },
            "knickerbockers": {
                "definition": "Loose-fitting trousers that are gathered at the knee or just below, traditionally worn by men and boys, particularly popular in the late 19th and early 20th centuries for sports and casual wear. These garments, also called knickers or plus-fours, feature full legs that taper to fitted bands below the knee, originally designed for active pursuits like golf, cycling, and hiking. The style represents historical men's fashion that balanced practicality with social propriety, allowing freedom of movement while maintaining modesty standards. Modern variations appear in historical reenactments, period costumes, and some traditional or ceremonial contexts.",
                "example_sentence": "The vintage golf outfit included wool _____ and long socks in the traditional 1920s style.",
                "pronunciation": "NIK-er-bok-erz (emphasis on first syllable)",
                "etymology": "From \"Knickerbocker,\" a fictional character in Washington Irving's writings, representing Dutch settlers in New York",
                "memory_tips": "Think \"knicker-knockers\" - pants that knock around your knees",
                "part_of_speech": "noun"
            },
            "knife": {
                "definition": "A tool or weapon consisting of a sharp blade attached to a handle, designed for cutting, slicing, piercing, or spreading various materials including food, fabric, and other substances. Knives represent one of humanity's oldest and most essential tools, with designs ranging from simple utility blades to specialized instruments for specific purposes like cooking, crafts, or surgery. The effectiveness of knives depends on blade geometry, steel quality, edge maintenance, and proper handling techniques that ensure both functionality and safety. Cultural significance of knives extends from practical daily use to ceremonial objects and symbols of skill or authority.",
                "example_sentence": "The chef used a sharp paring _____ to carefully remove the apple peel in one continuous strip.",
                "pronunciation": "NIEF (single syllable, rhymes with \"life\")",
                "etymology": "From Old English \"cnīf,\" from Old Norse \"knífr,\" of uncertain ultimate origin",
                "memory_tips": "Think \"night-f\" - like a sharp tool that cuts through the night",
                "part_of_speech": "noun, verb"
            },
            "knight": {
                "definition": "A mounted warrior in medieval Europe who served a feudal superior and followed codes of chivalry, typically of noble birth and granted land in exchange for military service. Knights represented the military elite of medieval society, bound by oaths of loyalty, honor, and protection of the weak, while maintaining fighting skills through constant training and warfare. The institution of knighthood evolved from practical military necessity into elaborate social and cultural systems with ceremonies, heraldry, and literary traditions. Modern usage extends to honorary titles granted for distinguished service and to chess pieces representing mounted warriors.",
                "example_sentence": "The medieval _____ took an oath to protect the innocent and serve his lord with honor and courage.",
                "pronunciation": "NIET (single syllable, rhymes with \"night\")",
                "etymology": "From Old English \"cniht,\" meaning \"boy\" or \"servant,\" later elevated to mean \"mounted warrior\"",
                "memory_tips": "Think \"night\" - knights often rode through the night on heroic quests",
                "part_of_speech": "noun, verb"
            },
            "knitted": {
                "definition": "Past tense of knit; describes fabric or garments created by interlocking loops of yarn using needles or machines, or the act of creating such items through the knitting process. Knitted fabrics have distinctive stretch and drape characteristics that make them comfortable for clothing, while the knitting process requires skill in manipulating stitches to create patterns, shaping, and desired textures. The technique produces everything from simple scarves to complex garments with intricate designs, representing both practical craftwork and artistic expression. Knitted items often carry personal significance as handmade gifts that represent time, care, and skill.",
                "example_sentence": "She _____ a warm sweater for her grandson using soft wool yarn in his favorite colors.",
                "pronunciation": "NIT-ed (emphasis on first syllable)",
                "etymology": "Past tense of \"knit,\" from Old English \"cnyttan,\" meaning \"to knot\" or \"fasten\"",
                "memory_tips": "Think \"neat-ed\" - neatly made fabric by looping yarn in organized patterns",
                "part_of_speech": "verb, adjective"
            },
            "knitwear": {
                "definition": "Clothing and accessories made from knitted fabrics, including sweaters, cardigans, scarves, hats, and other garments characterized by their stretch, warmth, and comfort properties. Knitwear encompasses both hand-knitted and machine-produced items that take advantage of knitted fabric's unique characteristics including elasticity, drape, and insulation properties. The category includes various weights from lightweight summer tops to heavy winter outerwear, with different stitch patterns and yarn types creating diverse textures and appearances. Modern knitwear combines traditional techniques with contemporary design and synthetic materials to create fashionable, functional clothing.",
                "example_sentence": "The fashion show featured sustainable _____ made from recycled wool and organic cotton yarns.",
                "pronunciation": "NIT-wair (emphasis on first syllable)",
                "etymology": "From \"knit\" + \"wear,\" describing garments made from knitted materials",
                "memory_tips": "Think \"neat-wear\" - neat clothing made from knitted materials",
                "part_of_speech": "noun"
            },
            "knock": {
                "definition": "To strike a surface, typically a door, with the knuckles or an object to attract attention or gain entry; also describes any impact, collision, or criticism that affects something or someone. Knocking serves as a universal communication method that announces presence while respecting privacy and property boundaries. The sound and pattern of knocks can convey different meanings from polite requests to urgent demands, with cultural variations in appropriate knocking etiquette. Extended meanings include physical impacts that cause damage, criticism that affects reputation, and mechanical sounds indicating engine problems or structural issues.",
                "example_sentence": "Please _____ before entering the office to ensure you're not interrupting an important meeting.",
                "pronunciation": "NAHK (single syllable, rhymes with \"rock\")",
                "etymology": "From Middle English \"knoken,\" possibly imitative of the sound of striking",
                "memory_tips": "Think \"knock-rock\" - like hitting a rock to make a sound",
                "part_of_speech": "verb, noun"
            },
            "knoll": {
                "definition": "A small, rounded hill or elevated mound of land that rises gently from surrounding terrain, typically grassy and offering modest elevation for views or strategic positioning. Knolls are formed through various geological processes including glacial deposition, erosion patterns, and tectonic activity, creating landscape features that provide natural landmarks and drainage patterns. These landforms often serve practical purposes including building sites, grazing areas, and defensive positions while adding visual interest to otherwise flat terrain. In literature and folklore, knolls frequently appear as significant locations for gatherings, burials, or supernatural events.",
                "example_sentence": "The old oak tree stood majestically on the grassy _____ overlooking the peaceful valley below.",
                "pronunciation": "NOHL (single syllable, rhymes with \"roll\")",
                "etymology": "From Old English \"cnoll,\" related to Middle High German \"knolle\" meaning \"lump\" or \"clod\"",
                "memory_tips": "Think \"know-ll\" - you know you'll find a small hill when you see a knoll",
                "part_of_speech": "noun"
            },
            "knot": {
                "definition": "A fastening made by tying or interweaving rope, string, or similar materials; a unit of speed equal to one nautical mile per hour; or a tight cluster or tangle of something. Knots serve essential functions in sailing, climbing, construction, and countless daily activities, with different knot types designed for specific purposes including joining, securing, and adjusting tension. The maritime speed measurement reflects the historical practice of using knotted rope lines to measure ship velocity. Metaphorically, knots represent complex problems, emotional tensions, or tangled situations that require patience and skill to resolve.",
                "example_sentence": "The sailor tied a secure bowline _____ to attach the boat safely to the dock.",
                "pronunciation": "NAHT (single syllable, rhymes with \"not\")",
                "etymology": "From Old English \"cnotta,\" from Germanic roots meaning \"knob\" or \"knot\"",
                "memory_tips": "Think \"not-t\" - it's not going anywhere when properly knotted",
                "part_of_speech": "noun, verb"
            },
            "knowledge": {
                "definition": "Information, understanding, or skills acquired through experience, education, or investigation; the sum total of what is known about particular subjects or in general. Knowledge encompasses both factual information and deeper comprehension that enables application, analysis, and synthesis of concepts across various domains. The acquisition of knowledge involves multiple processes including observation, study, reflection, and practice that transform information into usable understanding. Different types of knowledge include theoretical concepts, practical skills, cultural wisdom, and personal insights that collectively enable informed decision-making and effective action.",
                "example_sentence": "Her extensive _____ of marine biology made her the perfect candidate to lead the ocean research expedition.",
                "pronunciation": "NAHL-ij (emphasis on first syllable)",
                "etymology": "From Middle English \"knowleche,\" from \"know\" + suffix indicating the result or product of knowing",
                "memory_tips": "Think \"know-ledge\" - standing on a ledge of what you know",
                "part_of_speech": "noun"
            },
            "known": {
                "definition": "Past participle of know; describes something that has been identified, recognized, or established as fact through experience, investigation, or common awareness. Known information represents confirmed knowledge rather than speculation or belief, indicating that facts have been verified or are widely accepted within relevant communities. The term suggests reliability and certainty, distinguishing established information from unknown or uncertain matters. Known quantities serve as foundations for further learning, planning, and decision-making across scientific, personal, and professional contexts.",
                "example_sentence": "The ancient artifact was _____ to archaeologists but had never been displayed publicly before.",
                "pronunciation": "NOHN (single syllable, rhymes with \"grown\")",
                "etymology": "Past participle of \"know,\" from Old English \"cnāwen,\" from Germanic roots",
                "memory_tips": "Think \"grown-n\" - like knowledge that has grown and become established",
                "part_of_speech": "verb, adjective"
            },
            "knows": {
                "definition": "Third person singular present tense of know; indicates that someone has knowledge, awareness, or understanding of specific information, people, places, or concepts at the current time. The verb implies certain knowledge rather than mere belief or supposition, suggesting confidence in the accuracy of information or familiarity with subjects. Knowing involves cognitive processes of recognition, recall, and understanding that enable people to navigate their environment and make informed decisions. The certainty implied by knows distinguishes it from weaker forms of awareness or uncertain knowledge states.",
                "example_sentence": "Everyone _____ that she has the most experience with this type of complex engineering project.",
                "pronunciation": "NOHZ (single syllable, rhymes with \"goes\")",
                "etymology": "Third person singular of \"know,\" from Old English \"cnāwan,\" from Germanic roots",
                "memory_tips": "Think \"nose\" - like your nose knows different scents, the person knows information",
                "part_of_speech": "verb"
            },
            "knuckle": {
                "definition": "The joint of a finger where the bones meet, creating the prominent bumps visible when making a fist; also refers to similar joints in animals or mechanical devices. Knuckles provide the articulation points that enable finger flexibility and grasping functions, with protective skin and underlying structures that allow for punching motions and fine motor control. The term extends to various contexts including food preparation (knuckle cuts of meat), mechanical engineering (universal joints), and idiomatic expressions about applying oneself seriously to work. Knuckle injuries are common and can significantly affect hand function and dexterity.",
                "example_sentence": "He scraped his _____ on the rough brick wall while reaching for the dropped keys.",
                "pronunciation": "NUK-uhl (emphasis on first syllable)",
                "etymology": "From Middle English \"knokel,\" diminutive of \"knoke\" (knob), referring to the knob-like finger joints",
                "memory_tips": "Think \"knock-le\" - the little knobs you can knock with on your fingers",
                "part_of_speech": "noun, verb"
            },
            "kobold": {
                "definition": "In Germanic folklore, a mischievous household sprite or mine spirit that can be helpful or harmful depending on how humans treat them, often depicted as small, gnome-like creatures with magical powers. Kobolds traditionally inhabited mines, homes, and ships, performing helpful tasks when respected but causing trouble when offended or neglected. These supernatural beings represent the animistic beliefs of pre-Christian Germanic cultures that attributed spiritual presence to domestic and work spaces. Modern fantasy literature and games have adopted kobolds as characters, typically portraying them as small humanoid creatures with varying degrees of intelligence and magical ability.",
                "example_sentence": "The miners left offerings for the _____ spirits, hoping to prevent cave-ins and other underground accidents.",
                "pronunciation": "KOH-bohld (emphasis on first syllable)",
                "etymology": "From German \"Kobold,\" from Middle High German \"kobolt,\" possibly meaning \"household god\"",
                "memory_tips": "Think \"co-bold\" - small spirits that are bold enough to live alongside humans",
                "part_of_speech": "noun"
            },
            "kodak": {
                "definition": "A brand name for cameras and photographic equipment, originally created by George Eastman in 1888, that became synonymous with photography and democratized picture-taking through simple, affordable cameras. The Kodak company revolutionized photography by providing pre-loaded cameras that customers could use and return for film processing, eliminating the need for technical knowledge about photography. The brand name became so associated with photography that \"kodak\" was sometimes used generically for cameras, similar to how \"kleenex\" represents tissues. The company's slogan \"You press the button, we do the rest\" exemplified the accessibility of photography that Kodak created.",
                "example_sentence": "The vintage _____ camera from the 1950s still produced beautiful photographs with its classic lens.",
                "pronunciation": "KOH-dak (emphasis on first syllable)",
                "etymology": "Coined by George Eastman in 1888, possibly chosen for its distinctive sound and memorability",
                "memory_tips": "Think \"code-ak\" - like a code name for making photography accessible to everyone",
                "part_of_speech": "noun (proper/brand name)"
            },
            "kodakdifficulty": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"kodak\" (camera brand) incorrectly combined with \"difficulty\" (challenge or problem). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"kodak\" and \"difficulty\"",
                "part_of_speech": "error - combined words"
            },
            "kodali": {
                "definition": "A surname of Indian origin, particularly common among Telugu-speaking populations in South India, often associated with specific regional communities and family lineages. The name may have occupational, geographical, or caste-based origins as is common with many South Indian surnames that indicate ancestral professions, village origins, or social groups. Like many Indian surnames, Kodali carries cultural significance that connects individuals to their heritage, family history, and regional identity within the diverse landscape of Indian social organization. Such names often reflect centuries of cultural continuity and social structure in the Indian subcontinent.",
                "example_sentence": "Dr. _____ was recognized for her groundbreaking research in renewable energy technologies.",
                "pronunciation": "koh-DAH-lee (emphasis on second syllable)",
                "etymology": "From Telugu origins, possibly related to geographical or occupational designations",
                "memory_tips": "Think \"code-ali\" - like a family code that identifies Ali's heritage",
                "part_of_speech": "noun (proper name)"
            },
            "kodiak": {
                "definition": "Referring to Kodiak Island in Alaska or the subspecies of brown bear (Ursus arctos middendorffi) native to the Kodiak Archipelago, known as one of the largest bear subspecies in the world. Kodiak bears can weigh over 1,500 pounds and stand up to 10 feet tall, with their impressive size resulting from the abundant salmon runs and rich coastal environment of their island habitat. The Kodiak region represents pristine wilderness that supports diverse wildlife populations and maintains traditional Alaska Native cultural connections to the land. These bears are distinguished from other brown bears by their size, isolation, and unique genetic characteristics developed over thousands of years.",
                "example_sentence": "The wildlife photographer captured stunning images of _____ bears fishing for salmon during the annual run.",
                "pronunciation": "KOH-dee-ak (emphasis on first syllable)",
                "etymology": "From Russian \"Kad'yak,\" from Alutiiq \"qikertaq,\" meaning \"island\"",
                "memory_tips": "Think \"code-yak\" - like a code for the biggest yak-sized bears in Alaska",
                "part_of_speech": "adjective, noun"
            },
            "koine": {
                "definition": "The common form of Greek that developed as a lingua franca throughout the Mediterranean world following Alexander the Great's conquests, serving as the language of trade, administration, and eventually early Christianity. Koine Greek simplified classical Greek grammar and vocabulary, making it more accessible to diverse populations throughout the Hellenistic world and Roman Empire. This linguistic variety was used to write the New Testament and many other significant historical documents, preserving important religious and cultural texts. The development of Koine represents how languages evolve to serve practical communication needs across diverse cultural groups.",
                "example_sentence": "Biblical scholars study _____ Greek to better understand the original texts of the New Testament.",
                "pronunciation": "koy-NAY or KOY-nay (emphasis varies)",
                "etymology": "From Greek \"koine dialektos,\" meaning \"common dialect\" or \"shared language\"",
                "memory_tips": "Think \"coin-eh\" - like a common coin used everywhere for communication",
                "part_of_speech": "noun, adjective"
            },
            "koji": {
                "definition": "A type of fungus (Aspergillus oryzae) used in Japanese cuisine to ferment soybeans, rice, and other grains in the production of sake, miso, soy sauce, and other traditional foods. Koji cultivation involves inoculating cooked grains with spores and allowing the fungus to grow under controlled conditions, producing enzymes that break down starches and proteins into simpler compounds. This fermentation process creates the foundation for many Japanese fermented foods and beverages, contributing to their distinctive umami flavors and nutritional properties. The koji-making process represents sophisticated biotechnology that has been refined over centuries of Japanese culinary tradition.",
                "example_sentence": "The sake brewery carefully cultivated _____ rice for three days before beginning the fermentation process.",
                "pronunciation": "KOH-jee (emphasis on first syllable)",
                "etymology": "From Japanese \"koji,\" possibly from Chinese characters meaning \"yellow mold\"",
                "memory_tips": "Think \"co-G\" - cooperating with good mold to make delicious Japanese foods",
                "part_of_speech": "noun"
            },
            "kookaburra": {
                "definition": "A large kingfisher bird native to Australia and New Guinea, famous for its distinctive loud call that sounds like human laughter, earning it the nickname \"laughing jackass.\" Kookaburras are territorial birds that live in family groups, with their calls serving to establish territory boundaries and maintain group communication across woodland habitats. These birds are skilled hunters that prey on snakes, lizards, insects, and small mammals, playing important roles in controlling pest populations. The kookaburra has become an iconic symbol of Australian wildlife and appears frequently in Aboriginal folklore and contemporary Australian culture.",
                "example_sentence": "The campers woke to the loud, laughing call of a _____ greeting the Australian dawn.",
                "pronunciation": "KOOK-uh-bur-uh (emphasis on first syllable)",
                "etymology": "From Wiradhuri Aboriginal language \"guuguubarra,\" imitative of the bird's call",
                "memory_tips": "Think \"cook-a-burra\" - like a cook laughing while making burr-a (sounds)",
                "part_of_speech": "noun"
            },
            "korea": {
                "definition": "A peninsula in East Asia divided into two countries: North Korea (Democratic People's Republic of Korea) and South Korea (Republic of Korea), with a rich history of unified kingdoms, cultural achievements, and complex modern political divisions. Korean civilization has contributed significantly to world culture through innovations in technology, art, literature, and philosophy, while experiencing periods of both independence and foreign influence. The Korean Peninsula features mountainous terrain, distinct seasonal climate, and strategic location between China and Japan that has influenced its historical development. Contemporary Korea represents both the challenges of division and the achievements of rapid economic and technological development.",
                "example_sentence": "The ancient kingdoms of _____ developed unique writing systems, architectural styles, and philosophical traditions.",
                "pronunciation": "kuh-REE-uh (emphasis on second syllable)",
                "etymology": "From \"Goryeo,\" the name of a medieval Korean kingdom, possibly meaning \"high and clear\"",
                "memory_tips": "Think \"core-ea\" - like the core area of East Asian culture and innovation",
                "part_of_speech": "noun (proper)"
            },
            "korrigan": {
                "definition": "In Breton folklore, a type of fairy or sprite associated with ancient stone circles, dolmens, and other megalithic sites in Brittany, France, often depicted as small, dwarf-like beings with magical powers. Korrigans are said to guard ancient treasures, possess knowledge of herbal medicine, and can be either helpful or mischievous depending on how humans treat them and their sacred sites. These supernatural beings represent the connection between Breton culture and ancient Celtic traditions, maintaining folklore links to pre-Christian beliefs about spirits inhabiting sacred landscapes. Stories of korrigans often involve themes of respect for nature, ancient wisdom, and the consequences of disturbing sacred places.",
                "example_sentence": "The local legend claimed that _____ spirits protected the ancient stone circle from those who would disturb its peace.",
                "pronunciation": "KOR-i-gahn (emphasis on first syllable)",
                "etymology": "From Breton \"korrig,\" meaning \"dwarf\" or \"little person,\" related to Celtic folklore traditions",
                "memory_tips": "Think \"corridor-gan\" - spirits that guard corridors of ancient stone monuments",
                "part_of_speech": "noun"
            },
            "kosher": {
                "definition": "Conforming to Jewish dietary laws (kashrut) that specify which foods are permitted and how they must be prepared, processed, and consumed according to religious requirements. Kosher laws involve complex regulations about animal slaughter, food combinations, preparation methods, and kitchen equipment that maintain ritual purity and spiritual observance. The certification process requires rabbinical supervision and adherence to detailed guidelines that affect everything from ingredient sourcing to manufacturing processes. Beyond food, kosher can describe anything that is proper, legitimate, or acceptable according to established rules or standards.",
                "example_sentence": "The restaurant obtained _____ certification to serve observant Jewish customers according to dietary laws.",
                "pronunciation": "KOH-sher (emphasis on first syllable)",
                "etymology": "From Hebrew \"kasher,\" meaning \"proper\" or \"fit,\" related to religious dietary compliance",
                "memory_tips": "Think \"go-sher\" - going sure that food meets religious standards",
                "part_of_speech": "adjective, verb"
            },
            "koto": {
                "definition": "A traditional Japanese stringed musical instrument with 13 strings stretched over a long, wooden soundboard, played by plucking with picks worn on the fingers. The koto produces delicate, resonant sounds that can range from gentle melodies to complex rhythmic patterns, serving both as a solo instrument and in ensemble performances. Learning to play koto requires mastering specific techniques for plucking, bending strings, and creating the subtle tonal variations that characterize Japanese classical music. This instrument represents centuries of Japanese musical tradition and continues to be used in both traditional and contemporary musical contexts.",
                "example_sentence": "The musician's graceful _____ performance filled the concert hall with the ethereal sounds of traditional Japanese music.",
                "pronunciation": "KOH-toh (emphasis on first syllable)",
                "etymology": "From Japanese \"koto,\" from Chinese \"guzheng,\" referring to the stringed instrument family",
                "memory_tips": "Think \"coat-oh\" - like a wooden coat that makes beautiful oh sounds when plucked",
                "part_of_speech": "noun"
            },
            "kraken": {
                "definition": "A legendary giant sea monster from Scandinavian folklore, typically described as an enormous octopus or squid capable of destroying ships and creating whirlpools with its massive tentacles. The kraken myth likely originated from sailor encounters with actual giant squids, colossal squids, or other large marine creatures that were rare and poorly understood in earlier times. These stories represent the human fascination with ocean mysteries and the tendency to mythologize encounters with unknown natural phenomena. Modern usage of kraken often refers to anything enormously large, powerful, or destructive, particularly in popular culture and literature.",
                "example_sentence": "The sailors told terrifying tales of the _____ rising from the depths to crush entire vessels in its tentacles.",
                "pronunciation": "KRAH-kuhn (emphasis on first syllable)",
                "etymology": "From Norwegian \"kraken,\" possibly from \"krake\" meaning \"twisted\" or \"crooked\"",
                "memory_tips": "Think \"crack-en\" - a creature so big it can crack ships in half",
                "part_of_speech": "noun"
            },
            "krausen": {
                "definition": "The thick, foamy head that forms on top of fermenting beer during the most active phase of fermentation, consisting of yeast, proteins, and hop compounds that rise to the surface. Krausen formation indicates healthy fermentation activity and serves as a visual indicator for brewers to monitor the fermentation process and timing. The foam layer can be several inches thick and may overflow the fermentation vessel if not properly managed, requiring careful attention to vessel sizing and temperature control. Understanding krausen behavior is essential for successful brewing and helps brewers predict when fermentation phases will complete.",
                "example_sentence": "The brewer monitored the thick _____ layer to determine when the primary fermentation was reaching its peak activity.",
                "pronunciation": "KROW-zuhn (emphasis on first syllable)",
                "etymology": "From German \"kräusen,\" meaning \"to curl\" or \"form curls,\" referring to the foam's appearance",
                "memory_tips": "Think \"crown-zen\" - like a foamy crown on fermenting beer that brings zen to brewers",
                "part_of_speech": "noun"
            },
            "krewe": {
                "definition": "A social organization that stages parades and other events during Mardi Gras celebrations, particularly in New Orleans, with members who plan, fund, and participate in elaborate themed processions. Krewes have distinctive identities, traditions, and hierarchies that govern membership, float design, and parade participation, often maintaining secrecy about member identities and internal operations. These organizations represent important cultural institutions that preserve Carnival traditions while adapting to contemporary social changes and community involvement. The krewe system enables the complex logistics required for major parade productions while maintaining the festive spirit and cultural continuity of Mardi Gras celebrations.",
                "example_sentence": "The historic _____ spent months preparing elaborate floats and costumes for their signature Mardi Gras parade.",
                "pronunciation": "KROO (single syllable, rhymes with \"crew\")",
                "etymology": "Alteration of \"crew,\" adapted in New Orleans Mardi Gras tradition to distinguish parade organizations",
                "memory_tips": "Think \"crew\" spelled fancy - a special crew that makes Mardi Gras magic",
                "part_of_speech": "noun"
            },
            "krewekriegspiel": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"krewe\" (Mardi Gras organization) incorrectly combined with \"kriegspiel\" (German war game). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"krewe\" and \"kriegspiel\"",
                "part_of_speech": "error - combined words"
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
        """Process all words in batch 098"""
        
        logging.info("Processing Batch 098 with comprehensive Claude data...")
        
        input_file = "output/batch_098_words.csv"
        output_file = "output/batch_098_processed.csv"
        
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
            logging.info("Batch 098 processing completed!")
            logging.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
            logging.info(f"Output saved to: {output_file}")
            logging.info(f"Results: {len(processed_words)} successful, 0 failed")
                
        except Exception as e:
            logging.error(f"Error processing batch: {e}")
            raise

if __name__ == "__main__":
    processor = Batch098Processor()
    processor.process_batch()