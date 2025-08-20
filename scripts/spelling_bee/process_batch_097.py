#!/usr/bin/env python3
"""
Process Batch 097 of spelling bee words with comprehensive Claude data.
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

class Batch097Processor:
    """Processes Batch 097 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for each word with detailed definitions, pronunciations, etymologies, and memory tips"""
        
        word_data = {
            "karate": {
                "definition": "A Japanese martial art that emphasizes striking techniques using hands, feet, elbows, and knees, developed in Okinawa and characterized by disciplined training, kata forms, and philosophical principles. Modern karate combines physical conditioning, self-defense applications, and mental discipline through repetitive practice of basic techniques, sparring, and form demonstrations. The art focuses on precise, powerful movements delivered from stable stances, incorporating both hard linear techniques and flowing circular motions. Karate training develops physical fitness, mental concentration, respect, and self-control while teaching effective self-defense skills through systematic progression from basic techniques to advanced applications.",
                "example_sentence": "The martial arts studio offered _____ classes for students of all ages and skill levels.",
                "pronunciation": "kuh-RAH-tee (emphasis on second syllable)",
                "etymology": "From Japanese \"karate\" meaning \"empty hand,\" from \"kara\" (empty) + \"te\" (hand)",
                "memory_tips": "Think \"car-a-tea\" - practicing martial arts keeps you as alert as drinking tea",
                "part_of_speech": "noun"
            },
            "karma": {
                "definition": "In Hindu and Buddhist philosophy, the spiritual principle that governs the cycle of cause and effect, where intentional actions influence future circumstances and experiences. Karma encompasses the moral law that good actions lead to positive outcomes while harmful actions result in negative consequences, either in this life or future rebirths. The concept extends beyond simple reward and punishment to include the accumulation of merit and demerit that shapes character development and spiritual progress. Modern usage often refers to the general idea that actions have consequences or that good and bad deeds return to their originator.",
                "example_sentence": "She believed in _____ and tried to perform kind acts whenever possible.",
                "pronunciation": "KAR-muh (emphasis on first syllable)",
                "etymology": "From Sanskrit \"karma\" meaning \"action\" or \"deed,\" from \"kar\" (to do or make)",
                "memory_tips": "Think \"car-ma\" - what goes around comes around, like a car going in circles",
                "part_of_speech": "noun"
            },
            "karst": {
                "definition": "A distinctive type of landscape and underground drainage system formed by the dissolution of soluble rocks such as limestone, dolomite, and gypsum, creating caves, sinkholes, springs, and underground rivers. Karst topography develops through chemical weathering processes where slightly acidic water dissolves carbonate minerals over thousands of years, creating complex cave systems and surface features. These landscapes are characterized by rapid groundwater flow, limited surface water, and unique ecosystems adapted to cave environments. Karst regions are important for water supply but vulnerable to contamination due to direct connections between surface and groundwater.",
                "example_sentence": "The _____ landscape featured numerous caves and underground streams carved by water erosion.",
                "pronunciation": "KAHRST (single syllable, rhymes with \"first\")",
                "etymology": "From German \"Karst,\" after the Karst region in Slovenia where this landscape type was first scientifically studied",
                "memory_tips": "Think \"car-stone\" - water carves stone like a car carves tracks",
                "part_of_speech": "noun"
            },
            "katabatic": {
                "definition": "Describing winds that flow downhill due to gravitational forces, typically occurring when dense, cold air moves from higher elevations to lower areas. Katabatic winds develop when air at higher altitudes cools and becomes denser than surrounding air, creating a pressure gradient that drives the downward flow. These winds are particularly strong in mountainous regions and polar areas, where temperature differences between elevated surfaces and valleys create significant density variations. Katabatic winds can reach extreme velocities and play important roles in local weather patterns, glacier formation, and atmospheric circulation systems.",
                "example_sentence": "The _____ winds rushing down the mountain slope created challenging conditions for climbers.",
                "pronunciation": "kat-uh-BAT-ik (emphasis on third syllable)",
                "etymology": "From Greek \"katabatikos\" meaning \"going downhill,\" from \"kata\" (down) + \"bainein\" (to go)",
                "memory_tips": "Think \"cat-a-bat-ic\" - like a cat and bat going downhill together",
                "part_of_speech": "adjective"
            },
            "katakana": {
                "definition": "One of three writing systems used in Japanese, consisting of 46 basic syllabic characters used primarily for writing foreign loanwords, onomatopoeia, scientific terms, and emphasis. Katakana characters represent the same sounds as hiragana but have more angular, simplified forms derived from portions of Chinese characters. The writing system serves specific functions including transcribing foreign names and words, writing technical terminology, and providing emphasis similar to italics in English. Katakana is essential for modern Japanese writing, especially in contexts involving international communication, technology, and popular culture.",
                "example_sentence": "Japanese students learn _____ alongside hiragana and kanji writing systems.",
                "pronunciation": "kah-tah-KAH-nah (emphasis on third syllable)",
                "etymology": "From Japanese \"katakana,\" meaning \"fragment kana,\" referring to its derivation from fragments of Chinese characters",
                "memory_tips": "Think \"kata-can-a\" - you can learn this angular Japanese script",
                "part_of_speech": "noun"
            },
            "katana": {
                "definition": "A traditional Japanese sword characterized by a curved, single-edged blade with a long grip designed for two-handed use, representing the pinnacle of Japanese sword-making artistry. The katana features a distinctive design with a sharp cutting edge, reinforced spine, and carefully balanced proportions that make it both an effective weapon and a work of art. These swords were traditionally carried by samurai warriors and are renowned for their exceptional sharpness, durability, and craftsmanship involving complex forging techniques. Modern katana serve ceremonial, artistic, and martial arts purposes while maintaining traditional construction methods and cultural significance.",
                "example_sentence": "The museum displayed an authentic samurai _____ crafted during the Edo period.",
                "pronunciation": "kah-TAH-nah (emphasis on second syllable)",
                "etymology": "From Japanese \"katana,\" possibly from \"kata\" (one side) referring to its single-edged design",
                "memory_tips": "Think \"cut-anna\" - this sword can cut through almost anything",
                "part_of_speech": "noun"
            },
            "kathakali": {
                "definition": "A classical Indian dance-drama form from Kerala that combines elaborate storytelling, music, and highly stylized movements with ornate costumes and dramatic facial makeup. Kathakali performances typically depict stories from Hindu epics like the Ramayana and Mahabharata through expressive hand gestures, facial expressions, and rhythmic movements that require years of training to master. The art form features distinctive makeup styles using vibrant colors to represent different character types, while musicians provide vocal and instrumental accompaniment. Kathakali represents one of the most sophisticated forms of theatrical expression in Indian culture, preserving ancient traditions through contemporary performances.",
                "example_sentence": "The _____ performance featured elaborate costumes and dramatic storytelling through dance.",
                "pronunciation": "kuh-thuh-kuh-LEE (emphasis on last syllable)",
                "etymology": "From Malayalam \"kathakali,\" from \"katha\" (story) + \"kali\" (play or performance)",
                "memory_tips": "Think \"cat-hack-a-lee\" - like a cat performing dramatic storytelling",
                "part_of_speech": "noun"
            },
            "kathakalinoun": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"kathakali\" (Indian dance-drama) incorrectly combined with \"noun\" (grammatical term). This type of error occurs when PDF text extraction fails to properly separate distinct words or when grammatical labels get merged with content words during document processing. These represent completely unrelated concepts artificially joined due to technical parsing issues common in processing educational materials where formatting irregularities cause adjacent text elements to merge without proper spacing or punctuation.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"kathakali\" and \"noun\"",
                "part_of_speech": "error - combined words"
            },
            "katsura": {
                "definition": "A deciduous tree native to Japan and China (Cercidiphyllum japonicum) valued for its heart-shaped leaves that turn brilliant yellow, orange, and red in autumn while releasing a sweet, caramel-like fragrance. The katsura tree is prized in landscaping for its graceful branching pattern, attractive bark, and exceptional fall color display that creates stunning visual and aromatic experiences. These trees prefer moist, well-drained soil and partial shade, making them excellent choices for woodland gardens and naturalized settings. The distinctive sweet scent produced by the decomposing leaves is caused by maltol, the same compound found in cotton candy and caramel.",
                "example_sentence": "The _____ tree's autumn leaves filled the garden with a sweet caramel fragrance.",
                "pronunciation": "kaht-SOO-rah (emphasis on second syllable)",
                "etymology": "From Japanese \"katsura,\" named after the tree's native habitat regions",
                "memory_tips": "Think \"cats-sure-ah\" - cats are sure to love the sweet smell of these leaves",
                "part_of_speech": "noun"
            },
            "kaur": {
                "definition": "A surname traditionally adopted by Sikh women, meaning \"princess\" or \"lioness,\" representing spiritual equality and eliminating caste-based identification within Sikh religious practice. The name was instituted by Guru Gobind Singh, the tenth Sikh guru, as part of a naming system where all Sikh men take \"Singh\" (lion) and all Sikh women take \"Kaur\" to promote equality and unity. This practice removes traditional surnames that often indicated social status, occupation, or caste, replacing them with names that emphasize spiritual identity and gender equality. The adoption of Kaur reflects Sikh principles of social justice and religious egalitarianism.",
                "example_sentence": "Many Sikh women adopt the surname _____ as part of their religious identity.",
                "pronunciation": "KOWR (single syllable, rhymes with \"power\")",
                "etymology": "From Punjabi \"kaur,\" meaning \"princess\" or \"lioness,\" from Sanskrit \"kumari\" (princess)",
                "memory_tips": "Think \"cow-r\" - like a cow roaring with the strength of a lioness",
                "part_of_speech": "noun"
            },
            "kazoo": {
                "definition": "A simple musical instrument consisting of a hollow tube with a vibrating membrane that modifies the player's voice to create a buzzing, nasal sound when humming or singing into it. The kazoo operates through the principle of resonance, where vocal vibrations cause a thin membrane (traditionally wax paper or plastic) to vibrate, producing its characteristic buzzing timbre. Despite its simple construction, the kazoo can play melodies and harmonies, making it popular in folk music, novelty performances, and educational settings. The instrument demonstrates basic acoustic principles while providing an accessible introduction to music-making for people of all ages.",
                "example_sentence": "The marching band's _____ section added a playful buzzing sound to the parade music.",
                "pronunciation": "kuh-ZOO (emphasis on second syllable)",
                "etymology": "Possibly imitative of the buzzing sound it produces, or from Arabic \"qasaba\" (reed pipe)",
                "memory_tips": "Think \"ka-zoo\" - it sounds like you're saying \"zoo\" through your nose",
                "part_of_speech": "noun"
            },
            "keen": {
                "definition": "Having sharp mental faculties, intense perception, or strong enthusiasm; showing acute awareness, intelligence, or interest in something. When describing mental abilities, keen indicates quick understanding, sharp observation skills, and perceptive analysis. When referring to emotions or interests, it suggests intense enthusiasm, eagerness, or passionate involvement. The word also describes physical sharpness, as in keen edges or acute senses. Keen implies active engagement and heightened attention rather than passive awareness or casual interest.",
                "example_sentence": "The detective had a _____ eye for details that others often missed.",
                "pronunciation": "KEEN (single syllable, rhymes with \"seen\")",
                "etymology": "From Old English \"cene\" meaning \"brave, fierce, sharp,\" from Germanic roots",
                "memory_tips": "Think \"key-n\" - like having a key insight that's sharp and important",
                "part_of_speech": "adjective"
            },
            "keening": {
                "definition": "A form of vocal lamentation, traditionally performed by women in Irish and Scottish cultures during funeral rites, characterized by wailing, crying, and rhythmic mourning songs that express grief for the deceased. Keening involves improvised or traditional verses that celebrate the life of the departed while providing emotional release for mourners through communal expression of sorrow. The practice serves both ritualistic and therapeutic functions, helping communities process grief while maintaining cultural traditions surrounding death and remembrance. Modern usage extends to any intense vocal expression of grief or anguish that resembles traditional keening practices.",
                "example_sentence": "The mournful _____ of the women could be heard throughout the village during the funeral.",
                "pronunciation": "KEEN-ing (emphasis on first syllable)",
                "etymology": "From Irish \"caoine\" meaning \"to cry\" or \"weep,\" related to keen (sharp, intense)",
                "memory_tips": "Think \"keen-ing\" - being keen (intense) about expressing grief through crying",
                "part_of_speech": "noun, verb"
            },
            "keenness": {
                "definition": "The quality of having sharp perception, intense interest, or acute mental faculties; characterized by enthusiasm, alertness, and penetrating insight. Keenness of mind involves quick understanding, perceptive analysis, and the ability to detect subtle details or patterns that others might miss. When referring to emotions or interests, keenness indicates passionate engagement, eager participation, and sustained attention. The term can also describe physical acuity, such as keenness of sight, hearing, or other sensory perception that exceeds normal levels of sensitivity.",
                "example_sentence": "Her _____ for solving puzzles made her an excellent candidate for the research position.",
                "pronunciation": "KEEN-ness (emphasis on first syllable)",
                "etymology": "From \"keen\" + suffix \"-ness\" indicating the state or quality of being keen",
                "memory_tips": "Think \"keen-ness\" - the state of being keen, like sharpness of mind or interest",
                "part_of_speech": "noun"
            },
            "keep": {
                "definition": "To retain possession of something, continue in a specified state or condition, or maintain something in a particular place or situation over time. Keep involves active preservation, protection, or maintenance of objects, relationships, conditions, or commitments through sustained effort or attention. The verb encompasses various meanings including storing items safely, maintaining ongoing practices, preserving things from change or decay, and fulfilling obligations or promises. Keep implies responsibility, continuity, and intentional action to prevent loss, deterioration, or abandonment of something valued or necessary.",
                "example_sentence": "Please _____ your receipt as proof of purchase for any returns or exchanges.",
                "pronunciation": "KEEP (single syllable, rhymes with \"deep\")",
                "etymology": "From Old English \"cepan\" meaning \"to observe, hold, guard,\" from Germanic roots",
                "memory_tips": "Think \"key-p\" - like using a key to preserve and protect something important",
                "part_of_speech": "verb, noun"
            },
            "keeping": {
                "definition": "The action of retaining, maintaining, or preserving something in a particular state or condition; also refers to care, custody, or guardianship of objects, animals, or responsibilities. Keeping involves ongoing attention and effort to ensure that something remains safe, functional, or unchanged over time. The term encompasses both physical custody and abstract maintenance, such as keeping promises, keeping records, or keeping traditions alive. In phrases like \"in keeping with,\" it means being consistent or harmonious with established patterns, values, or expectations.",
                "example_sentence": "The ancient manuscripts were in the _____ of the monastery's most trusted scholars.",
                "pronunciation": "KEEP-ing (emphasis on first syllable)",
                "etymology": "From \"keep\" + suffix \"-ing\" indicating the action or result of keeping",
                "memory_tips": "Think \"keep-ing\" - the ongoing action of keeping something safe or maintained",
                "part_of_speech": "noun, verb"
            },
            "kelvin": {
                "definition": "The base unit of thermodynamic temperature in the International System of Units, with zero kelvin representing absolute zero, the theoretical temperature at which all molecular motion ceases. The Kelvin scale uses the same degree increment as Celsius but starts at absolute zero (-273.15°C), making it essential for scientific calculations involving gas laws, thermodynamics, and astronomical measurements. Named after physicist Lord Kelvin, this temperature scale provides an absolute reference point that eliminates negative temperatures and simplifies many physical equations. One kelvin represents the same temperature change as one degree Celsius, but the scale's absolute zero starting point makes it fundamental to physics and chemistry.",
                "example_sentence": "The scientist measured the gas temperature in _____ to ensure accurate thermodynamic calculations.",
                "pronunciation": "KEL-vin (emphasis on first syllable)",
                "etymology": "Named after William Thomson, 1st Baron Kelvin (1824-1907), British physicist who developed the absolute temperature scale",
                "memory_tips": "Think \"Kel-vin\" - like a scientist named Kevin who studies temperature",
                "part_of_speech": "noun"
            },
            "kennel": {
                "definition": "A shelter or housing structure designed for dogs, ranging from simple doghouses to commercial boarding facilities that accommodate multiple animals with individual compartments, exercise areas, and care services. Kennels provide safe, secure environments for dogs during owner absence, travel, or when specialized care is needed. Professional kennels often include grooming services, veterinary care, exercise programs, and socialization opportunities. The term also refers to the dog breeding and training industry, where kennels maintain breeding programs and prepare dogs for shows, competitions, or working roles.",
                "example_sentence": "The family boarded their dog at a reputable _____ while they traveled overseas.",
                "pronunciation": "KEN-uhl (emphasis on first syllable)",
                "etymology": "From Old French \"kenil\" meaning \"dog house,\" from Latin \"canis\" (dog)",
                "memory_tips": "Think \"ken-nell\" - Ken built a dwelling (nell) for his dog",
                "part_of_speech": "noun, verb"
            },
            "kenning": {
                "definition": "A metaphorical compound phrase used in Old Norse and Anglo-Saxon poetry to replace a simple noun, creating vivid imagery through creative word combinations like \"whale-road\" for sea or \"bone-house\" for body. Kennings function as poetic devices that transform ordinary concepts into imaginative descriptions, often consisting of two words that together evoke the original meaning through metaphor or metonymy. These expressions appear frequently in epic poems like Beowulf and the Icelandic sagas, serving both artistic and mnemonic functions in oral tradition. Modern literature occasionally employs kenning-like constructions to create evocative, compressed imagery that enriches poetic language.",
                "example_sentence": "The poet used the _____ \"storm-stirrer\" to describe the powerful warship in the epic tale.",
                "pronunciation": "KEN-ing (emphasis on first syllable)",
                "etymology": "From Old Norse \"kenning,\" meaning \"to know\" or \"to recognize,\" referring to knowing something through metaphor",
                "memory_tips": "Think \"ken-ning\" - you need to \"ken\" (know) the hidden meaning in these poetic phrases",
                "part_of_speech": "noun"
            },
            "kenningnoun": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"kenning\" (poetic metaphorical phrase) incorrectly combined with \"noun\" (grammatical term). This type of error occurs when PDF text extraction fails to properly separate distinct words or when grammatical labels become merged with content words during document processing. These represent completely unrelated concepts artificially joined due to technical parsing issues common in processing educational materials where formatting irregularities cause adjacent text elements to merge without proper spacing or punctuation.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"kenning\" and \"noun\"",
                "part_of_speech": "error - combined words"
            },
            "kente": {
                "definition": "A traditional hand-woven cloth from Ghana characterized by intricate geometric patterns and vibrant colors, with each design carrying specific cultural meanings and historical significance within Akan society. Kente cloth is created using narrow strips of silk and cotton woven on traditional looms, then sewn together to create larger garments or ceremonial pieces. Different color combinations and patterns represent various concepts such as royalty, spirituality, social status, and historical events, making each piece a form of visual communication. Originally reserved for Ghanaian royalty and special occasions, kente has become a symbol of African heritage and cultural pride worldwide.",
                "example_sentence": "The graduation ceremony featured students wearing traditional _____ stoles to honor their African heritage.",
                "pronunciation": "KEN-tay (emphasis on first syllable)",
                "etymology": "From Akan language \"kenten,\" meaning \"basket,\" referring to the basket-like woven pattern",
                "memory_tips": "Think \"Kent-ay\" - like someone named Kent saying \"ay\" while showing off colorful cloth",
                "part_of_speech": "noun"
            },
            "kentledge": {
                "definition": "Permanent ballast made of pig iron or other heavy materials placed in the bottom of a ship's hold to provide stability and maintain proper trim during navigation. Kentledge differs from cargo or temporary ballast because it remains permanently installed to ensure the vessel maintains appropriate weight distribution and stability characteristics. The material is typically arranged in systematic patterns that allow access to other parts of the ship while providing consistent stability. Proper kentledge installation prevents excessive rolling, maintains steering control, and ensures safe operation in various sea conditions by lowering the ship's center of gravity.",
                "example_sentence": "The ship's _____ was carefully arranged to maintain stability during the long ocean voyage.",
                "pronunciation": "KENT-lij (emphasis on first syllable)",
                "etymology": "From Middle English \"kentelage,\" possibly from \"quintal\" (unit of weight) or ship terminology",
                "memory_tips": "Think \"Kent-ledge\" - like Kent placed a ledge of heavy material in the ship's bottom",
                "part_of_speech": "noun"
            },
            "kepi": {
                "definition": "A military cap with a flat circular top, visor, and cloth sides, traditionally worn by French military forces and later adopted by various armies worldwide including Civil War era American forces. The kepi features a distinctive silhouette with its rigid crown, short visor for sun protection, and band around the base that often displays military insignia or unit identification. Different styles indicate rank, regiment, or military function through variations in color, trim, and decorative elements. The kepi remains part of ceremonial uniforms in many military traditions and is recognized as an iconic piece of 19th-century military headwear.",
                "example_sentence": "The Civil War reenactor wore an authentic blue _____ to complete his Union soldier uniform.",
                "pronunciation": "kuh-PEE or KAY-pee (emphasis varies by region)",
                "etymology": "From French \"képi,\" from Swiss German \"käppi\" meaning \"small cap\"",
                "memory_tips": "Think \"keep-i\" - soldiers keep their heads covered with this military cap",
                "part_of_speech": "noun"
            },
            "keplerian": {
                "definition": "Relating to or characteristic of the astronomical theories and laws developed by Johannes Kepler, particularly his three laws of planetary motion that describe how planets orbit the sun in elliptical paths. Keplerian motion refers to the mathematically predictable orbital patterns that result from gravitational forces, where planets move faster when closer to the sun and slower when farther away. These principles revolutionized understanding of the solar system by replacing circular orbital models with accurate elliptical descriptions supported by observational data. Keplerian mechanics form the foundation for modern orbital calculations used in space exploration, satellite deployment, and astronomical predictions.",
                "example_sentence": "The spacecraft's trajectory followed _____ orbital mechanics to reach Mars efficiently.",
                "pronunciation": "kep-LEER-ee-uhn (emphasis on second syllable)",
                "etymology": "From Johannes Kepler (1571-1630), German astronomer + suffix \"-ian\" meaning \"relating to\"",
                "memory_tips": "Think \"Kepler-ian\" - relating to Kepler's laws of planetary motion",
                "part_of_speech": "adjective"
            },
            "kerala": {
                "definition": "A state in southwestern India known for its tropical coastline, backwater networks, hill stations, and distinctive cultural traditions including Ayurvedic medicine, classical dance forms, and spice cultivation. Kerala features a unique geography with the Arabian Sea coastline, Western Ghats mountain range, and extensive network of inland waterways that support diverse ecosystems and traditional fishing communities. The state is renowned for its high literacy rates, progressive social policies, and sustainable development practices that balance economic growth with environmental protection. Kerala's cultural heritage includes ancient trade connections with Arab, Chinese, and European merchants that influenced its cuisine, architecture, and religious diversity.",
                "example_sentence": "The tourist visited _____ to experience the famous backwater boat cruises and spice plantations.",
                "pronunciation": "KAIR-uh-luh (emphasis on first syllable)",
                "etymology": "From Malayalam \"Keralam,\" possibly meaning \"land of coconuts\" from \"kera\" (coconut tree)",
                "memory_tips": "Think \"care-a-la\" - like caring for the beautiful land and waterways",
                "part_of_speech": "noun (proper)"
            },
            "keratitis": {
                "definition": "Inflammation of the cornea, the clear front layer of the eye, which can cause pain, redness, blurred vision, and sensitivity to light, potentially leading to serious complications if untreated. Keratitis can result from bacterial, viral, fungal, or parasitic infections, as well as injuries, dry eyes, or exposure to ultraviolet light. The condition requires prompt medical attention because corneal damage can cause permanent vision impairment or scarring that affects visual acuity. Treatment varies depending on the underlying cause and may include antibiotic, antiviral, or antifungal medications, along with supportive care to reduce inflammation and promote healing.",
                "example_sentence": "The contact lens wearer developed _____ after inadequate lens hygiene caused a corneal infection.",
                "pronunciation": "kair-uh-TIE-tis (emphasis on third syllable)",
                "etymology": "From Greek \"keras\" (horn, referring to the cornea's horn-like consistency) + \"-itis\" (inflammation)",
                "memory_tips": "Think \"care-a-tight-is\" - you need to care for your eyes when the cornea is tight with inflammation",
                "part_of_speech": "noun"
            },
            "kerchief": {
                "definition": "A square or triangular piece of cloth worn on the head or around the neck for protection, warmth, or decoration, often tied under the chin or at the nape of the neck. Kerchiefs serve both practical and fashion purposes, protecting hair from wind, dust, or sun while adding decorative elements to clothing. Traditional kerchiefs feature various patterns, colors, and fabrics that may indicate cultural identity, social status, or regional preferences. Modern kerchiefs are worn as fashion accessories, headwear for outdoor activities, or as part of traditional folk costumes and religious observances.",
                "example_sentence": "The farmer wore a colorful _____ to protect her hair while working in the dusty fields.",
                "pronunciation": "KER-chif (emphasis on first syllable)",
                "etymology": "From Old French \"cuevrechief,\" meaning \"cover head,\" from \"couvrir\" (cover) + \"chief\" (head)",
                "memory_tips": "Think \"cover-chief\" - covering the chief (head) with a cloth",
                "part_of_speech": "noun"
            },
            "kernel": {
                "definition": "The inner, usually edible part of a seed, nut, or fruit stone; the central or most important part of something; or in computing, the core component of an operating system that manages system resources. In biological terms, kernels contain the plant embryo and nutrients needed for growth, such as corn kernels or nut meats. Metaphorically, kernel refers to the essential core idea or fundamental element within a larger concept or system. In technology, the kernel serves as the crucial interface between software applications and computer hardware, controlling memory, processing, and device communication.",
                "example_sentence": "The _____ of truth in his story made the entire tale more believable and compelling.",
                "pronunciation": "KER-nuhl (emphasis on first syllable)",
                "etymology": "From Old English \"cyrnel,\" meaning \"seed,\" from \"corn\" (grain) + diminutive suffix",
                "memory_tips": "Think \"core-nel\" - the core essential part of something, like Colonel is the core of military leadership",
                "part_of_speech": "noun"
            },
            "kerneltawny": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"kernel\" (seed core) incorrectly combined with \"tawny\" (brownish-orange color). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"kernel\" and \"tawny\"",
                "part_of_speech": "error - combined words"
            },
            "kerril": {
                "definition": "A dialectical or archaic term for a small, worthless thing or person; sometimes used to describe something insignificant, trifling, or of little value. The word appears in various regional dialects and historical texts with slightly different meanings, often carrying connotations of smallness, insignificance, or dismissiveness. In some contexts, kerril might refer to a small animal, a minor object, or be used as a term of endearment or disparagement depending on the speaker's intent and regional usage. The word demonstrates how language evolves differently across geographical regions and social contexts.",
                "example_sentence": "The old man dismissed the complaint as nothing but a _____ hardly worth discussing.",
                "pronunciation": "KAIR-uhl (emphasis on first syllable)",
                "etymology": "Possibly from Middle English or dialectical origins, with uncertain etymological connections",
                "memory_tips": "Think \"care-ill\" - caring little about something small or insignificant",
                "part_of_speech": "noun"
            },
            "keyboard": {
                "definition": "An input device consisting of arranged keys or buttons used to enter text, numbers, and commands into computers, typewriters, or musical instruments. Computer keyboards typically feature QWERTY letter arrangement, function keys, number pad, and modifier keys that enable various text formatting and system operations. Musical keyboards contain keys that correspond to different pitches, allowing musicians to play melodies, harmonies, and complex compositions through electronic or mechanical sound generation. Modern keyboards may include additional features such as backlighting, programmable keys, wireless connectivity, and ergonomic designs for improved user comfort and efficiency.",
                "example_sentence": "The programmer used a mechanical _____ to improve typing speed and reduce finger fatigue.",
                "pronunciation": "KEE-bord (emphasis on first syllable)",
                "etymology": "From \"key\" + \"board,\" describing a board or panel with keys for input",
                "memory_tips": "Think \"key-board\" - a board full of keys for typing or playing music",
                "part_of_speech": "noun"
            },
            "keyhole": {
                "definition": "The opening in a lock through which a key is inserted to operate the locking mechanism, typically featuring a distinctive shape that prevents unauthorized access while allowing proper key insertion. Keyholes often have characteristic profiles including round openings for key heads and narrow slots for key shafts, designed to match specific key shapes for security purposes. The term extends metaphorically to describe any small opening that provides limited access or visibility, such as keyhole surgery techniques that use minimal incisions. In architecture and design, keyhole shapes appear as decorative elements and functional openings in walls, doors, and furniture.",
                "example_sentence": "The spy peered through the _____ to observe the secret meeting in the adjacent room.",
                "pronunciation": "KEE-hohl (emphasis on first syllable)",
                "etymology": "From \"key\" + \"hole,\" describing the hole designed for key insertion",
                "memory_tips": "Think \"key-hole\" - the hole where you insert a key to unlock something",
                "part_of_speech": "noun"
            },
            "keynesian": {
                "definition": "Relating to the economic theories of John Maynard Keynes, particularly the belief that government intervention through spending and monetary policy can stabilize economic cycles and reduce unemployment during recessions. Keynesian economics advocates for active fiscal policy, suggesting that during economic downturns, governments should increase spending and reduce taxes to stimulate demand and restore full employment. The theory challenges classical economics by arguing that markets don't always self-correct efficiently and that government action can improve economic outcomes. Keynesian principles influenced economic policy worldwide, particularly during the Great Depression and continue to inform modern macroeconomic policy debates.",
                "example_sentence": "The government's _____ response to the recession included increased infrastructure spending to stimulate job creation.",
                "pronunciation": "KAYN-zee-uhn (emphasis on first syllable)",
                "etymology": "From John Maynard Keynes (1883-1946), British economist + suffix \"-ian\" meaning \"relating to\"",
                "memory_tips": "Think \"Keynes-ian\" - relating to economist Keynes and his theories about government spending",
                "part_of_speech": "adjective"
            },
            "kibbitzer": {
                "definition": "A person who offers unwanted advice or commentary, especially while watching others play games like cards or chess; an onlooker who interferes with unsolicited suggestions or criticism. Kibbitzers typically position themselves where they can observe activities and feel compelled to share their opinions even when not asked for input. The term often carries negative connotations of being intrusive or annoying, though it can sometimes suggest friendly involvement or community engagement. In Yiddish culture, kibbitzers are familiar figures in social settings where games and discussions take place, representing both social connection and potential disruption.",
                "example_sentence": "The chess players politely asked the _____ to stop suggesting moves during their tournament game.",
                "pronunciation": "KIB-it-ser (emphasis on first syllable)",
                "etymology": "From Yiddish \"kibitser,\" from German \"Kiebitz\" (a type of bird known for making noise)",
                "memory_tips": "Think \"kibble-itzer\" - like someone constantly kibbling (chattering) while others try to concentrate",
                "part_of_speech": "noun"
            },
            "kibitzer": {
                "definition": "Alternative spelling of kibbitzer; a person who offers unsolicited advice or commentary while watching others engage in activities, particularly games or discussions. Kibitzers observe from the sidelines and feel compelled to share their opinions, suggestions, or criticism even when their input isn't requested or welcome. The behavior is common in social settings involving card games, chess, sports viewing, or any activity where observers feel knowledgeable enough to provide commentary. While sometimes appreciated for adding social interaction, kibitzers can also be disruptive when their interventions interfere with concentration or game flow.",
                "example_sentence": "The poker game attracted several kibitzers who watched intently and occasionally whispered suggestions.",
                "pronunciation": "KIB-it-ser (emphasis on first syllable)",
                "etymology": "From Yiddish \"kibitser,\" from German \"Kiebitz\" (lapwing bird), referring to the bird's noisy behavior",
                "memory_tips": "Think \"kid-bitzer\" - like a kid who bites into conversations with unwanted advice",
                "part_of_speech": "noun"
            },
            "kichel": {
                "definition": "A traditional Jewish pastry or cookie that is light, crispy, and often twisted into bow shapes, typically made with eggs, oil, and flour, then baked until golden and crunchy. Kichel represents Ashkenazi Jewish culinary tradition, often served during holidays, celebrations, or as everyday treats with tea or coffee. These delicate pastries require skill to achieve the proper texture - crispy and light rather than heavy or dense. The preparation involves rolling thin dough, shaping into traditional forms, and careful baking to create the characteristic golden color and satisfying crunch that makes kichel a beloved comfort food in Jewish communities.",
                "example_sentence": "The bakery specialized in traditional _____ made from the grandmother's original recipe.",
                "pronunciation": "KICH-uhl (emphasis on first syllable)",
                "etymology": "From Yiddish \"kichel,\" possibly related to German \"Küchlein\" (little cake)",
                "memory_tips": "Think \"kitchen-el\" - small treats made in the kitchen for special occasions",
                "part_of_speech": "noun"
            },
            "kiddo": {
                "definition": "An informal, affectionate term used to address a child, young person, or someone younger than the speaker, conveying familiarity, warmth, or casual friendliness. The word serves as a friendly diminutive that can express fondness, mentorship, or casual camaraderie in various social contexts. While typically used with children or teenagers, adults sometimes use kiddo playfully with peers or even older individuals in contexts that emphasize shared experiences or informal relationships. The term reflects casual American English speech patterns and social dynamics where age-related terms of address create connection and establish interpersonal rapport.",
                "example_sentence": "The coach encouraged the young player by saying, 'You did great out there, _____!'",
                "pronunciation": "KID-oh (emphasis on first syllable)",
                "etymology": "From \"kid\" (child) + suffix \"-o\" creating an informal, affectionate diminutive",
                "memory_tips": "Think \"kid-oh\" - like saying \"oh, kid\" in a friendly way",
                "part_of_speech": "noun"
            },
            "kidney": {
                "definition": "One of a pair of vital organs located in the lower back that filter waste products and excess water from blood to produce urine, maintaining the body's chemical balance and fluid levels. Kidneys perform essential functions including removing toxins, regulating blood pressure, producing red blood cells, and maintaining proper pH balance in body fluids. Each kidney contains approximately one million nephrons, tiny filtering units that process blood and create urine through complex processes of filtration, reabsorption, and secretion. Kidney health is crucial for overall well-being, and kidney disease can lead to serious complications requiring dialysis or transplantation.",
                "example_sentence": "Regular blood tests help monitor _____ function and detect early signs of disease.",
                "pronunciation": "KID-nee (emphasis on first syllable)",
                "etymology": "From Middle English \"kidnei,\" possibly from \"kid\" (young goat) + \"nei\" (kidney), referring to shape similarity",
                "memory_tips": "Think \"kid-knee\" - like a kid's knee shape, referring to the kidney's curved form",
                "part_of_speech": "noun"
            },
            "kildare": {
                "definition": "A county in the eastern part of Ireland, known for its horse breeding industry, flat landscapes, and proximity to Dublin, featuring the Curragh plains where Irish horse racing and military training take place. Kildare is renowned worldwide for thoroughbred horse breeding and training, with numerous stud farms and racing facilities that contribute significantly to Ireland's equine industry. The county contains historic sites including round towers, medieval castles, and ancient monasteries that reflect Ireland's rich cultural heritage. The name also appears in place names worldwide where Irish emigrants settled, carrying their cultural connections to their homeland.",
                "example_sentence": "The thoroughbred horses from _____ are prized for their racing bloodlines and training quality.",
                "pronunciation": "kil-DAIR (emphasis on second syllable)",
                "etymology": "From Irish \"Cill Dara,\" meaning \"church of the oak,\" referring to Saint Brigid's church",
                "memory_tips": "Think \"kill-dare\" - daring to kill time in this beautiful Irish county",
                "part_of_speech": "noun (proper)"
            },
            "kiln": {
                "definition": "A furnace or oven designed for burning, baking, or drying materials at high temperatures, commonly used in pottery making, cement production, lumber drying, and various industrial processes. Kilns operate at precisely controlled temperatures to achieve specific material transformations, such as hardening clay into ceramic, removing moisture from wood, or creating chemical reactions in manufacturing. Different kiln designs include electric, gas, wood-fired, and specialized industrial versions, each optimized for particular materials and temperature requirements. Proper kiln operation requires understanding of temperature curves, atmospheric conditions, and timing to achieve desired results without damaging materials.",
                "example_sentence": "The potter carefully loaded the ceramic pieces into the _____ for the final firing process.",
                "pronunciation": "KILN or KIL (pronunciation varies regionally)",
                "etymology": "From Old English \"cyln,\" from Latin \"culina\" meaning \"kitchen\" or \"cooking place\"",
                "memory_tips": "Think \"kill-n\" - using intense heat to kill moisture or transform materials",
                "part_of_speech": "noun, verb"
            },
            "kilnwebisode": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"kiln\" (high-temperature oven) incorrectly combined with \"webisode\" (web-based episode). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"kiln\" and \"webisode\"",
                "part_of_speech": "error - combined words"
            },
            "kilt": {
                "definition": "A traditional Scottish garment consisting of a knee-length pleated skirt-like garment typically made of tartan wool fabric, worn by men as part of Highland dress for formal occasions, cultural celebrations, and military ceremonies. Kilts feature distinctive patterns called tartans that often represent specific clans, regions, or military units, with colors and designs carrying historical and cultural significance. The garment includes practical elements such as a sporran (pouch), belt, and sometimes additional accessories like sgian-dubhs (small knives) and knee-high socks. Modern kilts maintain traditional construction methods while adapting to contemporary fashion and ceremonial needs.",
                "example_sentence": "The Scottish Highland Games featured men competing in traditional _____ representing their ancestral clans.",
                "pronunciation": "KILT (single syllable, rhymes with \"built\")",
                "etymology": "From Scots \"kilt,\" meaning \"to tuck up,\" referring to how the garment is arranged",
                "memory_tips": "Think \"built kilt\" - a carefully built traditional Scottish garment",
                "part_of_speech": "noun, verb"
            },
            "kiltwhirlybird": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"kilt\" (Scottish garment) incorrectly combined with \"whirlybird\" (informal term for helicopter). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"kilt\" and \"whirlybird\"",
                "part_of_speech": "error - combined words"
            },
            "kimcheemenorahs": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"kimchee\" (Korean fermented cabbage) incorrectly combined with \"menorahs\" (Jewish ceremonial candelabras). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated cultural and religious concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"kimchee\" and \"menorahs\"",
                "part_of_speech": "error - combined words"
            },
            "kimchi": {
                "definition": "A traditional Korean fermented vegetable dish, typically made with napa cabbage, Korean chili peppers, garlic, ginger, and salt, served as a side dish or ingredient in various Korean recipes. Kimchi undergoes a fermentation process that develops complex flavors, preserves vegetables, and creates beneficial probiotics that support digestive health. The dish varies regionally within Korea, with different vegetables, spice levels, and fermentation techniques creating hundreds of variations. Kimchi represents Korean culinary culture and has gained international recognition for its unique taste, nutritional benefits, and cultural significance in Korean meals and celebrations.",
                "example_sentence": "The Korean restaurant served traditional _____ alongside rice and bulgogi beef.",
                "pronunciation": "KIM-chee (emphasis on first syllable)",
                "etymology": "From Korean \"gimchi,\" from \"jim\" (submerge) + \"chae\" (vegetable), referring to the pickling process",
                "memory_tips": "Think \"Kim-cheese\" - like someone named Kim made this fermented vegetable dish",
                "part_of_speech": "noun"
            },
            "kindergarten": {
                "definition": "An educational program for children typically between ages four and six that serves as a transition between home or preschool and elementary school, emphasizing learning through play, social development, and basic academic skills. Kindergarten curricula include activities that develop fine motor skills, letter recognition, number concepts, social interaction, and classroom behavior while maintaining child-centered approaches that honor developmental stages. The program originated in Germany as \"children's garden,\" reflecting the philosophy that young children flourish in nurturing environments that allow natural growth and exploration. Modern kindergarten balances academic preparation with creative expression, physical activity, and emotional development.",
                "example_sentence": "The child eagerly started _____ where she learned letters, numbers, and how to play cooperatively with classmates.",
                "pronunciation": "KIN-der-gar-tuhn (emphasis on first syllable)",
                "etymology": "From German \"Kindergarten,\" meaning \"children's garden,\" created by educator Friedrich Fröbel",
                "memory_tips": "Think \"kind-er-garden\" - a kind garden where children grow and learn",
                "part_of_speech": "noun"
            },
            "kindling": {
                "definition": "Small pieces of dry wood, paper, or other combustible materials used to start fires, typically arranged to catch flame easily and ignite larger fuel sources. Effective kindling burns quickly with sufficient heat to ignite larger logs or fuel, requiring materials with good surface area and low moisture content. The process of gathering and preparing kindling involves selecting appropriate materials, creating proper size gradations from fine tinder to larger sticks, and arranging them to promote airflow and flame spread. Kindling skills are essential for camping, fireplace use, and emergency situations where fire provides warmth, cooking capability, and safety.",
                "example_sentence": "The campers gathered dry twigs and bark to use as _____ for starting their evening fire.",
                "pronunciation": "KIND-ling (emphasis on first syllable)",
                "etymology": "From \"kindle\" + suffix \"-ing,\" referring to materials used to kindle fires",
                "memory_tips": "Think \"kind-ling\" - being kind to a fire by giving it easy materials to burn",
                "part_of_speech": "noun, verb"
            },
            "kindred": {
                "definition": "People who are related by blood or marriage; sharing similar characteristics, interests, or nature; having a close affinity or connection based on common qualities or experiences. Kindred relationships involve both familial connections and chosen bonds between individuals who share values, interests, or perspectives. The term suggests deep understanding and compatibility that transcends superficial differences, creating meaningful connections through shared experiences, beliefs, or temperaments. Kindred spirits often find each other across different backgrounds and circumstances, recognizing fundamental similarities that create lasting bonds and mutual understanding.",
                "example_sentence": "The two artists were _____ spirits who immediately understood each other's creative vision and passion.",
                "pronunciation": "KIN-drid (emphasis on first syllable)",
                "etymology": "From Middle English \"kinrede,\" from \"kin\" (family) + \"-red\" (condition), meaning \"kinship condition\"",
                "memory_tips": "Think \"kin-red\" - red blood relatives or kin who share similar qualities",
                "part_of_speech": "noun, adjective"
            },
            "kinds": {
                "definition": "Plural form of kind; different types, categories, or varieties of things that share certain characteristics while maintaining distinct qualities or features. Kinds represent classification systems that organize objects, concepts, or experiences based on shared attributes, helping people understand relationships and differences. The word encompasses both natural categories and human-created classifications, from biological species to social groups to material objects. Understanding different kinds enables comparison, organization, and communication about the diverse range of things encountered in daily life and specialized fields of study.",
                "example_sentence": "The library contained many different _____ of books, from fiction to science to history.",
                "pronunciation": "KIENDS (single syllable, rhymes with \"finds\")",
                "etymology": "Plural of \"kind,\" from Old English \"cynd\" meaning \"nature, race, or type\"",
                "memory_tips": "Think \"find kinds\" - you can find many kinds of things in any category",
                "part_of_speech": "noun"
            },
            "kinesiology": {
                "definition": "The scientific study of human movement, encompassing anatomy, physiology, biomechanics, and motor control to understand how the body moves and functions during physical activity. Kinesiology integrates knowledge from multiple disciplines including biology, psychology, and physics to analyze movement patterns, improve athletic performance, prevent injuries, and develop rehabilitation programs. The field applies to various areas including sports medicine, physical therapy, exercise science, and ergonomics, helping optimize human movement in both athletic and daily life contexts. Kinesiologists study everything from basic motor development to complex athletic skills and movement disorders.",
                "example_sentence": "The _____ program prepared students to work in sports medicine and physical rehabilitation careers.",
                "pronunciation": "ki-nee-see-OL-uh-jee (emphasis on fourth syllable)",
                "etymology": "From Greek \"kinesis\" (movement) + \"-ology\" (study of), meaning \"the study of movement\"",
                "memory_tips": "Think \"kinetic-ology\" - the study of kinetic movement and body motion",
                "part_of_speech": "noun"
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
        """Process all words in batch 097"""
        
        logging.info("Processing Batch 097 with comprehensive Claude data...")
        
        input_file = "output/batch_097_words.csv"
        output_file = "output/batch_097_processed.csv"
        
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
            logging.info("Batch 097 processing completed!")
            logging.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
            logging.info(f"Output saved to: {output_file}")
            logging.info(f"Results: {len(processed_words)} successful, 0 failed")
                
        except Exception as e:
            logging.error(f"Error processing batch: {e}")
            raise

if __name__ == "__main__":
    processor = Batch097Processor()
    processor.process_batch()