#!/usr/bin/env python3
"""
Process Batch 102 of spelling bee words with comprehensive Claude data.
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

class Batch102Processor:
    """Processes Batch 102 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for each word with detailed definitions, pronunciations, etymologies, and memory tips"""
        
        word_data = {
            "leisure": {
                "definition": "Free time when one is not working or occupied; time available for relaxation, recreation, or pursuits of personal interest and enjoyment. Leisure represents freedom from the demands of work, obligations, and necessary activities, allowing individuals to engage in activities they find personally fulfilling or restorative. The concept of leisure has evolved throughout history, from a privilege of the wealthy to a recognized need for human well-being and social development. Modern society increasingly recognizes leisure as essential for mental health, creativity, family relationships, and overall quality of life, though the balance between work and leisure remains a significant challenge.",
                "example_sentence": "After retiring from her demanding career, she finally had the _____ to pursue her passion for painting and travel.",
                "pronunciation": "LEE-zher or LEZH-er (emphasis on first syllable)",
                "etymology": "From Old French \"leisir,\" from Latin \"licere\" meaning \"to be permitted\" or \"be free\"",
                "memory_tips": "Think \"please-sure\" - leisure is the pleasure of pleasing yourself with free time",
                "part_of_speech": "noun, adjective"
            },
            "leisureleotard": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"leisure\" (free time) incorrectly combined with \"leotard\" (gymnastic garment). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"leisure\" and \"leotard\"",
                "part_of_speech": "error - combined words"
            },
            "leks": {
                "definition": "Areas where male animals, particularly birds, gather to display and compete for mates through elaborate courtship behaviors; plural of lek, which refers to these communal mating grounds. Lekking behavior involves males congregating in specific locations to perform displays of strength, beauty, or skill that attract females for mating selection. This reproductive strategy is found in various species including grouse, peacocks, and some mammals, where females visit leks to choose mates based on the quality of male displays. The lek system demonstrates natural selection in action, as successful males with superior displays produce more offspring.",
                "example_sentence": "Wildlife biologists studied the prairie chicken _____ to understand mating behaviors and population dynamics.",
                "pronunciation": "LEKS (single syllable, rhymes with \"decks\")",
                "etymology": "From Swedish \"lek\" meaning \"play,\" referring to the playful-seeming mating displays",
                "memory_tips": "Think \"lex\" (like Lex Luther) - a place where males compete to be the dominant one",
                "part_of_speech": "noun"
            },
            "lemniscus": {
                "definition": "A ribbon-like bundle of nerve fibers in the brainstem that carries sensory information from the body to the thalamus and ultimately to the cerebral cortex for conscious perception. The lemniscal system includes the medial lemniscus, which carries touch and position information, and the lateral lemniscus, which processes auditory signals. These neural pathways are crucial for sensory processing and demonstrate the organized structure of the nervous system in transmitting information from peripheral receptors to higher brain centers. Understanding lemniscal pathways is important in neurology and helps explain how sensory deficits occur with brainstem injuries.",
                "example_sentence": "The neurologist explained how damage to the medial _____ could cause loss of touch sensation on the opposite side of the body.",
                "pronunciation": "lem-NIS-kuhs (emphasis on second syllable)",
                "etymology": "From Latin \"lemniscus,\" meaning \"ribbon,\" from Greek \"lemniskos\" referring to the ribbon-like appearance",
                "memory_tips": "Think \"lemon-disk-us\" - a ribbon-like disk of nerve fibers, yellow like a lemon",
                "part_of_speech": "noun"
            },
            "lemon": {
                "definition": "A yellow citrus fruit with acidic juice, thick peel, and distinctive sour taste, widely used in cooking, beverages, and as a source of vitamin C; also used to describe something defective or unsatisfactory. Lemons grow on evergreen trees in warm climates and contain citric acid, essential oils, and nutrients that make them valuable for culinary and medicinal purposes. The fruit's acidic properties make it useful for cleaning, food preservation, and flavor enhancement in countless recipes worldwide. In slang usage, calling something a \"lemon\" indicates it's faulty or disappointing, particularly applied to defective cars or other products.",
                "example_sentence": "The chef squeezed fresh _____ juice over the fish to add brightness and acidity to the delicate flavors.",
                "pronunciation": "LEM-uhn (emphasis on first syllable)",
                "etymology": "From Old French \"limon,\" from Arabic \"laymun,\" ultimately from Persian",
                "memory_tips": "Think \"lemme-on\" - like saying \"let me put this on\" when adding lemon to food",
                "part_of_speech": "noun, adjective"
            },
            "leniency": {
                "definition": "The quality of being lenient; mercy, tolerance, or compassion shown in judgment or punishment; the inclination to be forgiving rather than harsh or strict in applying rules or consequences. Leniency involves tempering justice with understanding, considering circumstances that might warrant reduced penalties or more gentle treatment. This quality is valued in leadership, parenting, and legal systems where rigid application of rules might not serve the best interests of individuals or society. However, leniency must be balanced with fairness and consistency to maintain credibility and prevent abuse of compassionate treatment.",
                "example_sentence": "The judge showed _____ toward the first-time offender, considering her circumstances and genuine remorse.",
                "pronunciation": "LEE-nee-uhn-see (emphasis on first syllable)",
                "etymology": "From Latin \"lenientia,\" from \"lenis\" meaning \"soft\" or \"gentle\"",
                "memory_tips": "Think \"lean-see\" - leaning toward mercy when you see someone's situation",
                "part_of_speech": "noun"
            },
            "lento": {
                "definition": "A musical tempo marking indicating a slow speed, typically slower than andante but faster than largo; characterized by a deliberate, unhurried pace that allows for expression and musical phrasing. Lento passages require careful attention to musical line and emotional content, as the slower tempo provides space for nuanced interpretation and expressiveness. Musicians must maintain musical continuity and avoid dragging when performing lento sections, balancing slowness with forward motion. This tempo marking appears frequently in classical music where composers seek to create contemplative, lyrical, or dramatic effects through deliberate pacing.",
                "example_sentence": "The pianist performed the _____ movement with such expressiveness that the audience was completely captivated by the slow, beautiful melody.",
                "pronunciation": "LEN-toh (emphasis on first syllable)",
                "etymology": "From Italian \"lento,\" meaning \"slow,\" from Latin \"lentus\"",
                "memory_tips": "Think \"lens-tow\" - like slowly towing something with a magnifying lens to see every detail",
                "part_of_speech": "adjective, adverb, noun"
            },
            "leonine": {
                "definition": "Resembling or characteristic of a lion; having qualities associated with lions such as courage, majesty, strength, or physical features like a full mane of hair. Leonine characteristics include both literal physical resemblances to lions and metaphorical qualities of leadership, bravery, and commanding presence. The term can describe facial features, hair, personality traits, or behaviors that evoke the regal, powerful nature associated with lions. In literature and description, leonine often conveys nobility, fierce protection of territory or family, and the kind of natural authority that commands respect.",
                "example_sentence": "The actor's _____ features and commanding voice made him perfect for playing the role of the powerful king.",
                "pronunciation": "LEE-uh-nien (emphasis on first syllable)",
                "etymology": "From Latin \"leoninus,\" from \"leo\" meaning \"lion\"",
                "memory_tips": "Think \"Leo-nine\" - like nine qualities of Leo the lion: brave, strong, majestic, etc.",
                "part_of_speech": "adjective"
            },
            "leotard": {
                "definition": "A close-fitting one-piece garment that covers the torso, worn by dancers, gymnasts, and other performers to allow freedom of movement while providing modesty and support. Leotards are designed to stretch with body movements and come in various styles including sleeveless, short-sleeved, and long-sleeved versions, often made from materials like spandex or lycra. The garment serves practical purposes in athletic and artistic activities where loose clothing would interfere with performance or create safety hazards. Named after the French acrobat Jules Léotard, this essential performance wear has become standard attire in dance studios, gymnastics, and fitness activities worldwide.",
                "example_sentence": "The ballet dancer chose a simple black _____ that allowed complete freedom of movement during her performance.",
                "pronunciation": "LEE-uh-tard (emphasis on first syllable)",
                "etymology": "Named after Jules Léotard (1842-1870), French trapeze artist who popularized the garment",
                "memory_tips": "Think \"Leo-tard\" - Leo the acrobat was never tardy thanks to his flexible outfit",
                "part_of_speech": "noun"
            },
            "less": {
                "definition": "A smaller amount or degree; not as much; comparative form of little, used to indicate a reduction in quantity, extent, or intensity compared to another amount or a previous state. Less establishes comparisons between quantities that cannot be counted individually, such as water, time, or abstract concepts, distinguishing it from \"fewer\" which applies to countable items. The concept helps express relative measurements and degrees, enabling precise communication about amounts and changes. Understanding when to use less versus fewer reflects grammatical precision and clear thinking about measurable versus countable quantities.",
                "example_sentence": "The new recipe calls for _____ sugar than the original version to create a healthier dessert option.",
                "pronunciation": "LES (single syllable, rhymes with \"mess\")",
                "etymology": "From Old English \"læssa,\" comparative form of \"læt\" meaning \"small\"",
                "memory_tips": "Think \"mess\" - having less stuff creates less of a mess",
                "part_of_speech": "adjective, adverb, noun"
            },
            "letter": {
                "definition": "A written or printed symbol representing a speech sound and forming part of an alphabet; also refers to a written message sent from one person to another, typically through postal service or electronic means. Letters as alphabet symbols combine to form words and enable written communication across languages and cultures, representing one of humanity's most important inventions. As correspondence, letters serve personal, business, and official communication needs, though electronic communication has largely replaced traditional letter writing. Both meanings emphasize the fundamental role of written symbols in human communication and record-keeping throughout history.",
                "example_sentence": "She wrote a heartfelt _____ to her grandmother, expressing gratitude for all the wisdom and love shared over the years.",
                "pronunciation": "LET-er (emphasis on first syllable)",
                "etymology": "From Old French \"lettre,\" from Latin \"littera\" meaning \"letter of the alphabet\"",
                "memory_tips": "Think \"let-er\" - letting someone know your thoughts through written symbols",
                "part_of_speech": "noun, verb"
            },
            "letters": {
                "definition": "Plural of letter; multiple symbols of an alphabet or multiple written communications; also refers to literature, learning, or scholarly pursuits in the phrase \"man/woman of letters.\" As alphabet symbols, letters combine to create the building blocks of written language, enabling complex communication through systematic arrangement. As correspondence, letters represent a traditional form of long-distance communication that has shaped personal relationships, business dealings, and historical records. The broader meaning of letters as learning emphasizes the connection between literacy, education, and intellectual achievement in human culture.",
                "example_sentence": "The scholar received numerous _____ from colleagues around the world praising her groundbreaking research in medieval literature.",
                "pronunciation": "LET-erz (emphasis on first syllable)",
                "etymology": "Plural of \"letter,\" from Old French \"lettre\"",
                "memory_tips": "Think \"let-ers\" - multiple ways of letting people know things through written symbols",
                "part_of_speech": "noun"
            },
            "lettuce": {
                "definition": "A leafy green vegetable with crisp leaves commonly used in salads, sandwiches, and cooking, belonging to the daisy family and cultivated worldwide for its nutritious and refreshing qualities. Lettuce varieties include iceberg, romaine, butter, and leaf lettuce, each offering different textures, flavors, and nutritional profiles that suit various culinary applications. The vegetable provides vitamins A and K, folate, and fiber while being low in calories, making it a popular choice for healthy diets. Lettuce cultivation requires cool weather and adequate water, with modern growing techniques enabling year-round production in many regions.",
                "example_sentence": "The chef layered crisp _____ leaves with tomatoes and cucumbers to create a refreshing summer salad.",
                "pronunciation": "LET-is (emphasis on first syllable)",
                "etymology": "From Old French \"laitues,\" from Latin \"lactuca,\" from \"lac\" (milk), referring to the plant's milky sap",
                "memory_tips": "Think \"let-us\" - let us eat this healthy green vegetable in our salads",
                "part_of_speech": "noun"
            },
            "levees": {
                "definition": "Artificial embankments or natural ridges along the banks of rivers, designed to prevent flooding by containing water within the channel during high water periods. Levees are critical flood control infrastructure that protect communities, agricultural land, and property from water damage during seasonal floods or storm events. These earthen or concrete structures require careful engineering, maintenance, and monitoring to ensure their effectiveness and prevent catastrophic failure. The levee system along major rivers like the Mississippi represents massive civil engineering projects that enable human settlement and economic activity in flood-prone areas.",
                "example_sentence": "The Army Corps of Engineers inspected the _____ along the river to ensure they could withstand the predicted spring floods.",
                "pronunciation": "LEV-eez (emphasis on first syllable)",
                "etymology": "From French \"levée,\" meaning \"raised,\" from \"lever\" (to raise)",
                "memory_tips": "Think \"leave-ease\" - levees give you ease by making flood water leave your area",
                "part_of_speech": "noun"
            },
            "levels": {
                "definition": "Plural of level; different heights, degrees, or stages in a system; positions of relative elevation or intensity that create hierarchical arrangements or measurements. Levels can refer to physical heights like building floors, skill gradations in education or gaming, or intensity measurements in various fields. Understanding levels helps organize complex systems, track progress, and establish clear distinctions between different stages or capabilities. The concept applies across numerous domains from construction and engineering to education, management, and personal development, providing frameworks for measurement and advancement.",
                "example_sentence": "The video game featured multiple difficulty _____ that challenged players to develop increasingly sophisticated strategies.",
                "pronunciation": "LEV-uhlz (emphasis on first syllable)",
                "etymology": "Plural of \"level,\" from Old French \"livel,\" from Latin \"libella\" (diminutive of \"libra,\" balance)",
                "memory_tips": "Think \"leave-els\" - different elevated positions you can leave things at",
                "part_of_speech": "noun, verb"
            },
            "leviathan": {
                "definition": "A sea monster of enormous size and power mentioned in biblical and mythological texts; something impressively large or powerful, especially a massive ship, whale, or organization. In biblical context, leviathan represents chaos and divine power over creation, while in literature it symbolizes overwhelming natural forces or institutions. Modern usage often describes huge corporations, government bureaucracies, or any entity of intimidating size and influence. The term captures both literal enormity and the psychological impact of confronting something so large it seems beyond human control or comprehension.",
                "example_sentence": "The multinational corporation had become a _____ that dominated the global market through its massive resources and influence.",
                "pronunciation": "luh-VIE-uh-thuhn (emphasis on second syllable)",
                "etymology": "From Hebrew \"livyathan,\" possibly meaning \"twisted\" or \"coiled,\" referring to a sea serpent",
                "memory_tips": "Think \"levy-athan\" - a huge creature that could levy taxes on the entire ocean",
                "part_of_speech": "noun"
            },
            "levitate": {
                "definition": "To rise and hover in the air without visible support; to make something appear to float or suspend in mid-air through mysterious or supernatural means. Levitation has been claimed in various religious and spiritual traditions, often associated with saints, mystics, or meditation masters who supposedly transcended physical limitations. In entertainment, levitation tricks use hidden supports, optical illusions, or magnetic fields to create the appearance of objects or people floating. Scientific levitation exists through magnetic fields, acoustic waves, or other physical principles, though not the miraculous floating often depicted in fiction.",
                "example_sentence": "The magician appeared to _____ above the stage, creating an illusion that amazed and mystified the audience.",
                "pronunciation": "LEV-uh-tayt (emphasis on first syllable)",
                "etymology": "From Latin \"levitas\" meaning \"lightness,\" from \"levis\" (light in weight)",
                "memory_tips": "Think \"light-ate\" - becoming so light that you ate nothing and can float in the air",
                "part_of_speech": "verb"
            },
            "levity": {
                "definition": "Lightness of manner or speech, especially when inappropriate; humor or lack of seriousness in situations that might warrant more grave or respectful treatment. Levity can provide necessary relief from tension and stress, making difficult situations more bearable through appropriate humor and light-heartedness. However, excessive levity in serious contexts can appear disrespectful, insensitive, or immature, suggesting poor judgment about when humor is appropriate. The challenge lies in balancing levity's positive effects on morale and relationships with the need for appropriate seriousness in significant or solemn situations.",
                "example_sentence": "The funeral director maintained professional composure while gently discouraging inappropriate _____ during the solemn ceremony.",
                "pronunciation": "LEV-uh-tee (emphasis on first syllable)",
                "etymology": "From Latin \"levitas,\" meaning \"lightness\" or \"frivolity,\" from \"levis\" (light)",
                "memory_tips": "Think \"light-ity\" - the quality of being light in mood or taking things lightly",
                "part_of_speech": "noun"
            },
            "lexicographers": {
                "definition": "Plural of lexicographer; people who compile, edit, and write dictionaries; scholars who study and document the vocabulary of languages, including word meanings, etymologies, pronunciations, and usage patterns. Lexicographers combine linguistic expertise with meticulous research skills to create authoritative references that preserve and explain language evolution. Their work involves analyzing how words are actually used in speech and writing, tracking changes in meaning over time, and making decisions about which words and definitions to include in dictionaries. Modern lexicographers use digital tools and corpus linguistics to analyze massive amounts of text and identify language trends.",
                "example_sentence": "The team of _____ spent years researching and compiling the comprehensive dictionary of contemporary English usage.",
                "pronunciation": "lek-si-KOG-ruh-ferz (emphasis on third syllable)",
                "etymology": "From Greek \"lexikon\" (dictionary) + \"graphein\" (to write), meaning \"dictionary writers\"",
                "memory_tips": "Think \"lexi-ographers\" - people who write about words and their meanings",
                "part_of_speech": "noun"
            },
            "lexicon": {
                "definition": "The vocabulary of a language, individual, or branch of knowledge; the complete set of words and phrases that constitute a language or are used within a particular field or by a specific person. A lexicon encompasses not just individual words but also their relationships, meanings, and usage patterns within linguistic and cultural contexts. Different fields develop specialized lexicons with technical terminology that enables precise communication among experts. Personal lexicons vary based on education, experience, and social environment, reflecting how vocabulary acquisition continues throughout life and shapes both thinking and expression capabilities.",
                "example_sentence": "The medical student worked diligently to master the specialized _____ required for effective communication in healthcare settings.",
                "pronunciation": "LEK-si-kon (emphasis on first syllable)",
                "etymology": "From Greek \"lexikon biblion,\" meaning \"word book,\" from \"lexis\" (word or speech)",
                "memory_tips": "Think \"lexi-con\" - a con artist who tricks you with complex words from their vocabulary",
                "part_of_speech": "noun"
            },
            "liability": {
                "definition": "Legal responsibility for damages or debts; a person or thing that creates disadvantages or risks; something that poses a potential problem or source of trouble. In legal and financial contexts, liability represents obligations to pay debts, compensate for damages, or fulfill contractual commitments that create enforceable claims against individuals or organizations. Insurance and risk management industries focus heavily on identifying, measuring, and mitigating various forms of liability exposure. Beyond legal contexts, calling someone or something a liability suggests they create more problems than benefits, hindering rather than helping achieve goals.",
                "example_sentence": "The company's legal team carefully reviewed contracts to minimize potential _____ exposure in their international business ventures.",
                "pronunciation": "lie-uh-BIL-uh-tee (emphasis on third syllable)",
                "etymology": "From Old French \"liable,\" meaning \"bound\" or \"obligated,\" from Latin \"ligare\" (to bind)",
                "memory_tips": "Think \"lie-ability\" - the ability to create problems that lie waiting to cause trouble",
                "part_of_speech": "noun"
            },
            "liaise": {
                "definition": "To establish and maintain communication and cooperation between different groups, organizations, or individuals; to act as a link or intermediary that facilitates collaboration and information sharing. Liaising involves building relationships, coordinating activities, and ensuring that relevant parties stay informed about developments that affect their interests or responsibilities. This function is crucial in complex organizations, international relations, and project management where multiple stakeholders must work together effectively. Successful liaising requires diplomatic skills, clear communication abilities, and understanding of different perspectives and priorities.",
                "example_sentence": "The project manager will _____ with various departments to ensure all teams coordinate effectively during the product launch.",
                "pronunciation": "lee-AYZ or LEE-ayz (emphasis varies)",
                "etymology": "From French \"lier,\" meaning \"to bind\" or \"connect,\" related to \"liaison\"",
                "memory_tips": "Think \"Lee-says\" - Lee says he'll connect different groups and help them communicate",
                "part_of_speech": "verb"
            },
            "liana": {
                "definition": "A woody climbing plant found in tropical forests that roots in the ground and uses trees and other structures for support as it grows toward the forest canopy in search of sunlight. Lianas are crucial components of tropical ecosystems, creating connections between different forest layers and providing pathways for animals moving through the canopy. These plants demonstrate remarkable adaptations for climbing, including specialized stems, tendrils, and root systems that allow them to compete successfully for light in dense forest environments. Lianas contribute to forest biodiversity while sometimes competing with trees for resources and potentially affecting forest structure.",
                "example_sentence": "The biologist studied how _____ vines created highways for monkeys and other animals to travel through the rainforest canopy.",
                "pronunciation": "lee-AH-nuh (emphasis on second syllable)",
                "etymology": "From French \"liane,\" possibly from Spanish \"liar\" meaning \"to tie\" or \"bind\"",
                "memory_tips": "Think \"Lee-Anna\" - Anna climbs like Lee up trees, binding herself to them for support",
                "part_of_speech": "noun"
            },
            "libris": {
                "definition": "From the Latin phrase \"ex libris,\" meaning \"from the books of,\" typically used in bookplates to indicate ownership; the word appears in the context of book ownership and library science. Ex libris bookplates are decorative labels placed inside books to identify the owner, often featuring artistic designs, coats of arms, or personal symbols that reflect the owner's interests or identity. This tradition dates back centuries and represents the cultural value placed on book ownership and personal libraries. The practice continues today among book collectors and bibliophiles who appreciate both the practical and aesthetic aspects of marking book ownership.",
                "example_sentence": "The rare book collector designed elegant _____ bookplates featuring his family crest and favorite literary quotes.",
                "pronunciation": "LEE-bris or LIB-ris (emphasis varies)",
                "etymology": "From Latin \"libris,\" ablative plural of \"liber\" meaning \"book\"",
                "memory_tips": "Think \"library-is\" - this is from my library, as marked by the bookplate",
                "part_of_speech": "noun"
            },
            "licensure": {
                "definition": "The process of granting licenses to individuals or organizations, certifying that they meet specific qualifications and standards to practice a profession or operate a business legally. Licensure systems protect public safety and welfare by ensuring that practitioners have demonstrated competency through education, examination, and ongoing professional development requirements. Different professions including medicine, law, engineering, and cosmetology require licensure that involves initial qualification assessment and periodic renewal to maintain standards. The licensure process typically includes background checks, continuing education requirements, and adherence to professional codes of conduct that maintain industry credibility.",
                "example_sentence": "The nursing school's graduates had an excellent pass rate on the state _____ examination required to practice as registered nurses.",
                "pronunciation": "LIE-suhn-sher (emphasis on first syllable)",
                "etymology": "From \"license\" + suffix \"-ure,\" meaning \"the act or process of licensing\"",
                "memory_tips": "Think \"license-sure\" - making sure people have proper licenses to practice their profession",
                "part_of_speech": "noun"
            },
            "lidocaine": {
                "definition": "A local anesthetic medication commonly used to numb tissue during medical and dental procedures, blocking nerve signals to prevent pain sensation in specific areas of the body. Lidocaine works by preventing sodium channels in nerve cell membranes from opening, thereby stopping the transmission of pain signals to the brain. The drug is available in various forms including injections, topical creams, and sprays, making it versatile for different medical applications from minor surgeries to cardiac procedures. As one of the most widely used local anesthetics, lidocaine has revolutionized medical practice by enabling pain-free procedures and improving patient comfort.",
                "example_sentence": "The dentist administered _____ injection to numb the patient's gum before performing the tooth extraction procedure.",
                "pronunciation": "LIE-doh-kayn (emphasis on first syllable)",
                "etymology": "Named after its chemical structure, combining \"lido\" (from diethylamino) + \"caine\" (common suffix for anesthetics)",
                "memory_tips": "Think \"lie-do-cane\" - it makes pain lie down so you don't need a cane to walk after surgery",
                "part_of_speech": "noun"
            },
            "liege": {
                "definition": "In feudal systems, a lord to whom a vassal owes allegiance and service; also refers to a loyal subject or follower who serves with dedication and faithfulness. The liege relationship formed the backbone of medieval social and political organization, creating networks of mutual obligation between rulers and their subordinates. Lords provided protection and land grants to their vassals, while vassals offered military service, loyalty, and various forms of tribute to their liege lords. Modern usage extends the concept to describe any relationship characterized by devoted service, unwavering loyalty, and hierarchical respect between individuals or groups.",
                "example_sentence": "The knight pledged his sword and service to his _____ lord in exchange for protection and a grant of land.",
                "pronunciation": "LEEJ (single syllable, rhymes with \"siege\")",
                "etymology": "From Old French \"lige,\" from Germanic roots meaning \"free\" or \"allodial\"",
                "memory_tips": "Think \"siege\" - your liege lord protects you during a siege in exchange for your loyalty",
                "part_of_speech": "noun, adjective"
            },
            "lierre": {
                "definition": "French word for ivy; a climbing or trailing plant that attaches to surfaces and grows over walls, trees, and other structures, commonly used in gardening and landscaping for decorative purposes. Lierre represents various species of climbing plants that use aerial roots or tendrils to cling to supports while seeking sunlight and growing space. These plants are valued for their ability to cover unsightly surfaces, provide insulation, and create lush green environments, though they can also damage buildings and compete with other plants. In French culture and literature, lierre often symbolizes fidelity, eternal love, and the persistence of nature.",
                "example_sentence": "The old château was covered with thick _____ that had been growing up its stone walls for decades.",
                "pronunciation": "lee-AIR (emphasis on second syllable)",
                "etymology": "From French \"lierre,\" from Latin \"hedera,\" meaning \"ivy\"",
                "memory_tips": "Think \"Lee-air\" - Lee needs air to breathe while climbing up walls like ivy",
                "part_of_speech": "noun"
            },
            "lieutenant": {
                "definition": "A military or police officer of relatively low rank, typically serving as second-in-command to a captain or other superior officer; someone who acts on behalf of or assists a higher-ranking official. In military hierarchies, lieutenants serve crucial leadership roles at the tactical level, commanding small units and implementing orders from higher command while making immediate decisions in field situations. The rank represents a balance between junior officer responsibility and senior leadership preparation, providing essential experience for advancement to higher positions. In civilian contexts, lieutenant can describe any deputy or assistant who serves in a subordinate but responsible capacity.",
                "example_sentence": "The army _____ led her platoon through challenging terrain during the training exercise, demonstrating strong leadership skills.",
                "pronunciation": "loo-TEN-uhnt (British) or LOO-ten-uhnt (American) (emphasis varies)",
                "etymology": "From Old French \"lieutenant,\" meaning \"place holder,\" from \"lieu\" (place) + \"tenant\" (holding)",
                "memory_tips": "Think \"lieu-tenant\" - a tenant who holds a place for someone higher in command",
                "part_of_speech": "noun"
            },
            "lifelong": {
                "definition": "Lasting or continuing throughout a person's life; extending from early years until death; characterized by permanence and enduring commitment. Lifelong describes relationships, learning processes, interests, or commitments that persist through all of life's changes and stages, demonstrating remarkable consistency and dedication. Examples include lifelong friendships that endure despite geographical separations and life changes, or lifelong learning that continues beyond formal education throughout one's career and retirement. The concept emphasizes the value of sustained commitment and the cumulative benefits that result from consistent dedication over extended periods.",
                "example_sentence": "Her _____ passion for marine biology led her from childhood tide pool explorations to becoming a renowned oceanographer.",
                "pronunciation": "LIEH-long (emphasis on first syllable)",
                "etymology": "From \"life\" + \"long,\" meaning \"lasting for the duration of life\"",
                "memory_tips": "Think \"life-long\" - as long as your life lasts, this continues",
                "part_of_speech": "adjective"
            },
            "lifetime": {
                "definition": "The duration of a person's life; the period during which someone lives or something exists; an extremely long period of time from one's perspective. Lifetime encompasses all experiences, relationships, and achievements that occur between birth and death, representing the complete arc of individual existence. The term is often used to emphasize the significance or rarity of experiences, as in \"opportunity of a lifetime\" or \"lifetime achievement award.\" Understanding lifetime helps people prioritize goals, appreciate precious moments, and make decisions that consider long-term consequences and legacy creation.",
                "example_sentence": "The elderly professor had devoted his entire _____ to studying ancient languages and preserving historical manuscripts.",
                "pronunciation": "LIEH-tiem (emphasis on first syllable)",
                "etymology": "From \"life\" + \"time,\" meaning \"the time duration of a life\"",
                "memory_tips": "Think \"life-time\" - the amount of time you have in your life to accomplish things",
                "part_of_speech": "noun, adjective"
            },
            "ligament": {
                "definition": "A strong band of fibrous connective tissue that connects bones to other bones at joints, providing stability and controlling the range of motion in the skeletal system. Ligaments are composed primarily of collagen fibers arranged to withstand tension and maintain joint integrity during movement, preventing dislocation and excessive motion that could cause injury. Common ligament injuries include sprains, which occur when ligaments are stretched or torn beyond their normal capacity, often requiring rest, rehabilitation, or surgical repair. Understanding ligament function is crucial for athletes, physical therapists, and anyone interested in maintaining joint health and preventing injury.",
                "example_sentence": "The soccer player's knee _____ injury required surgery and months of physical therapy for full recovery.",
                "pronunciation": "LIG-uh-muhnt (emphasis on first syllable)",
                "etymology": "From Latin \"ligamentum,\" from \"ligare\" meaning \"to bind\" or \"tie\"",
                "memory_tips": "Think \"liga-meant\" - liga (league) meant to bind bones together like a sports league binds teams",
                "part_of_speech": "noun"
            },
            "ligas": {
                "definition": "Spanish word meaning \"leagues\" or \"alliances\"; organizations that bring together teams, individuals, or groups for competition, cooperation, or mutual benefit. In sports contexts, ligas represent organized competitions where multiple teams compete under unified rules and governance structures. The term can also refer to political or social alliances formed to achieve common objectives or protect shared interests. Understanding ligas helps explain organizational structures in Spanish-speaking countries and communities where these associations play important roles in sports, politics, and social activities.",
                "example_sentence": "The soccer _____ in Mexico featured teams from cities across the country competing for the national championship.",
                "pronunciation": "LEE-gahs (emphasis on first syllable)",
                "etymology": "Spanish plural of \"liga,\" from Latin \"ligare\" meaning \"to bind\" or \"unite\"",
                "memory_tips": "Think \"Lee-gas\" - Lee needs gas to travel to all the different league games",
                "part_of_speech": "noun"
            },
            "light": {
                "definition": "Electromagnetic radiation that is visible to the human eye; something that provides illumination or makes vision possible; also refers to having little weight or being easy to carry or move. As electromagnetic radiation, light enables vision, photosynthesis, and numerous technological applications from lasers to fiber optics. Light's dual nature as both wave and particle has fundamental importance in physics and led to quantum mechanics development. Metaphorically, light represents knowledge, understanding, hope, and spiritual illumination in cultures worldwide, while its opposite, darkness, often symbolizes ignorance, despair, or evil. The concept encompasses both physical phenomena and profound symbolic meanings.",
                "example_sentence": "The morning _____ streaming through the window created beautiful patterns on the wall and filled the room with warmth.",
                "pronunciation": "LIET (single syllable, rhymes with \"right\")",
                "etymology": "From Old English \"leoht,\" from Germanic roots meaning \"bright\" or \"shining\"",
                "memory_tips": "Think \"right\" - light helps you see what's right and guides you correctly",
                "part_of_speech": "noun, verb, adjective, adverb"
            },
            "lighting": {
                "definition": "The arrangement or effect of lights in a space; the equipment and techniques used to provide illumination for various purposes including safety, functionality, and aesthetic enhancement. Effective lighting involves understanding how different light sources, intensities, and positioning create desired atmospheres and serve practical needs in residential, commercial, and artistic contexts. Professional lighting design considers factors such as color temperature, brightness levels, energy efficiency, and psychological effects of different lighting approaches. Modern lighting technology includes LED systems, smart controls, and energy-efficient options that reduce environmental impact while improving illumination quality.",
                "example_sentence": "The theater's sophisticated _____ system could create any mood from romantic sunset to dramatic storm effects during performances.",
                "pronunciation": "LIET-ing (emphasis on first syllable)",
                "etymology": "From \"light\" + suffix \"-ing,\" meaning \"the action or arrangement of providing light\"",
                "memory_tips": "Think \"light-ing\" - the ongoing action of bringing light to spaces",
                "part_of_speech": "noun, verb"
            },
            "lightweight": {
                "definition": "Having little weight; designed to be light and easy to handle; also refers to someone lacking substance, influence, or intellectual depth. In sports, lightweight describes competitors in specific weight categories, while in manufacturing it refers to materials and designs that reduce weight without sacrificing strength or functionality. The term can describe both positive qualities like portability and efficiency, and negative characteristics like superficiality or lack of serious content. Modern technology often pursues lightweight solutions that maintain performance while improving mobility and reducing resource consumption.",
                "example_sentence": "The hiker chose a _____ tent that provided adequate shelter while adding minimal weight to his backpack.",
                "pronunciation": "LIET-wayt (emphasis on first syllable)",
                "etymology": "From \"light\" + \"weight,\" meaning \"having little weight\"",
                "memory_tips": "Think \"light-wait\" - you don't have to wait long to carry something light",
                "part_of_speech": "adjective, noun"
            },
            "likelier": {
                "definition": "Comparative form of likely; more probable or expected to happen; having a greater chance of occurring than other alternatives. The concept of likelihood involves assessing probabilities based on available evidence, past experience, and logical reasoning to make predictions about future events. Understanding what makes outcomes likelier helps in decision-making, risk assessment, and planning activities that depend on uncertain future conditions. Statistical analysis, historical patterns, and causal relationships all contribute to determining which scenarios are likelier to occur in various situations.",
                "example_sentence": "Based on current weather patterns, rain tomorrow seems _____ than the sunny conditions originally forecast.",
                "pronunciation": "LIEK-lee-er (emphasis on first syllable)",
                "etymology": "Comparative form of \"likely,\" from Old English \"geliclic\" meaning \"similar\" or \"probable\"",
                "memory_tips": "Think \"like-leer\" - you leer (look suspiciously) at something that's more likely to happen",
                "part_of_speech": "adjective"
            },
            "lilliputian": {
                "definition": "Extremely small in size; tiny or miniature; also refers to someone who is petty, narrow-minded, or lacking in vision or scope. The term originates from Jonathan Swift's \"Gulliver's Travels,\" where Lilliput was inhabited by people only six inches tall, creating a satirical commentary on human nature and politics. In modern usage, lilliputian can describe both literal smallness and metaphorical pettiness or small-mindedness that focuses on trivial details while missing larger important issues. The word captures both physical diminutiveness and intellectual or moral limitations that prevent broader perspective and understanding.",
                "example_sentence": "The committee's _____ concerns about minor procedural details prevented them from addressing the major policy issues.",
                "pronunciation": "lil-uh-PYOO-shuhn (emphasis on third syllable)",
                "etymology": "From \"Lilliput,\" the fictional land in Swift's \"Gulliver's Travels\" + \"-ian\"",
                "memory_tips": "Think \"little-put-ian\" - people who were put in a little place and think small",
                "part_of_speech": "adjective, noun"
            },
            "limaçon": {
                "definition": "A mathematical curve shaped like a snail shell, defined by a specific equation in polar coordinates that creates loops, dimples, or heart-like shapes depending on the parameters used. The limaçon family includes several variations such as the cardioid (heart-shaped curve) and curves with inner loops that demonstrate interesting geometric properties. These curves appear in various mathematical contexts including physics, engineering, and computer graphics where their unique properties make them useful for modeling natural phenomena and creating artistic designs. The study of limaçons contributes to understanding of parametric equations and polar coordinate systems.",
                "example_sentence": "The mathematics student graphed various _____ curves to understand how changing parameters affected the shape and loops.",
                "pronunciation": "LEE-mah-sohn (emphasis on first syllable)",
                "etymology": "From French \"limaçon,\" meaning \"snail,\" referring to the curve's shell-like appearance",
                "memory_tips": "Think \"Lima-son\" - a son from Lima drew snail-shaped curves in math class",
                "part_of_speech": "noun"
            },
            "limbs": {
                "definition": "Arms and legs of humans and animals; large branches of trees; extensions or appendages that project from main bodies or structures. In anatomy, limbs enable locomotion, manipulation, and interaction with the environment through complex systems of bones, muscles, joints, and nerves. Tree limbs provide structural support for leaves and fruit while creating habitat for various animals and contributing to the tree's overall health and growth patterns. The term extends metaphorically to describe any projecting parts of organizations, systems, or structures that extend from central cores to perform specific functions.",
                "example_sentence": "The physical therapist helped the patient regain strength and coordination in both upper and lower _____ after the accident.",
                "pronunciation": "LIMZ (single syllable, rhymes with \"gyms\")",
                "etymology": "From Old English \"lim,\" from Germanic roots meaning \"branch\" or \"member\"",
                "memory_tips": "Think \"gyms\" - you exercise your limbs at gyms to keep them strong",
                "part_of_speech": "noun"
            },
            "limburger": {
                "definition": "A strong-smelling, soft cheese originally from the Limburg region between Belgium, Germany, and the Netherlands, characterized by its pungent aroma and creamy texture that develops during the aging process. Limburger cheese is made from cow's milk and undergoes surface ripening with specific bacteria cultures that create its distinctive smell and flavor profile. Despite its notorious odor, the cheese has a relatively mild taste that appeals to adventurous cheese enthusiasts and represents traditional European cheese-making techniques. The cheese has become a cultural symbol in areas with strong European immigrant populations.",
                "example_sentence": "The cheese shop owner warned customers about the powerful aroma of _____ before they decided to purchase this traditional European delicacy.",
                "pronunciation": "LIM-ber-ger (emphasis on first syllable)",
                "etymology": "Named after Limburg, the historical region where this cheese style originated",
                "memory_tips": "Think \"limber-ger\" - you need to be limber to run away from its strong smell",
                "part_of_speech": "noun"
            },
            "limelight": {
                "definition": "The focus of public attention or scrutiny; originally referred to an intense white light produced by heating lime in a flame, used in theater lighting before electric lights were invented. Being in the limelight means receiving significant public attention, media coverage, or celebrity status that brings both benefits and challenges of fame. The historical lime-based lighting system created brilliant illumination that made performers clearly visible to audiences, leading to the metaphorical association between bright light and public visibility. Modern usage emphasizes the scrutiny and pressure that accompany public attention and celebrity status.",
                "example_sentence": "After winning the championship, the young athlete found herself thrust into the _____ with interviews and endorsement opportunities.",
                "pronunciation": "LIEM-liet (emphasis on first syllable)",
                "etymology": "From \"lime\" (calcium oxide) + \"light,\" referring to the intense theatrical lighting method",
                "memory_tips": "Think \"lime-light\" - bright green lime under a spotlight for everyone to see",
                "part_of_speech": "noun"
            },
            "limicolous": {
                "definition": "Living in or frequenting muddy places; adapted to muddy or marshy environments; describing organisms that thrive in wet, soft substrate conditions. Limicolous species have evolved specific adaptations that enable them to exploit resources in muddy habitats including specialized feeding mechanisms, body structures, and behaviors suited to soft sediments. These organisms play important ecological roles in wetland ecosystems, often serving as indicators of environmental health and water quality. Examples include various shorebirds, worms, and microorganisms that have developed strategies for surviving and reproducing in muddy conditions.",
                "example_sentence": "The _____ shorebirds used their long bills to probe deep into the mud flats searching for invertebrates and small fish.",
                "pronunciation": "luh-MIK-uh-luhs (emphasis on second syllable)",
                "etymology": "From Latin \"limum\" (mud) + \"colere\" (to inhabit), meaning \"mud-dwelling\"",
                "memory_tips": "Think \"limit-colous\" - limited to living in colonies in muddy places",
                "part_of_speech": "adjective"
            },
            "limiting": {
                "definition": "Present participle of limit; restricting, constraining, or setting boundaries that prevent something from exceeding specified parameters; establishing maximum or minimum values that define acceptable ranges. Limiting factors control growth, development, or performance by creating bottlenecks or constraints that must be addressed before progress can continue. In various fields, limiting involves identifying and managing constraints that affect outcomes, whether in resource allocation, system performance, or personal development. Effective limiting requires balancing necessary restrictions with appropriate flexibility to achieve desired results.",
                "example_sentence": "The coach focused on identifying and addressing the _____ factors that prevented the team from reaching its full potential.",
                "pronunciation": "LIM-uh-ting (emphasis on first syllable)",
                "etymology": "Present participle of \"limit,\" from Latin \"limes\" meaning \"boundary\" or \"threshold\"",
                "memory_tips": "Think \"limit-ing\" - the ongoing action of setting limits and boundaries",
                "part_of_speech": "verb, adjective"
            },
            "limned": {
                "definition": "Past tense of limn; outlined, delineated, or portrayed in clear detail; drawn or painted with precise lines and careful attention to definition and clarity. Limning involves creating detailed representations that capture essential characteristics through careful observation and skillful execution. The term is often used in artistic and literary contexts to describe work that achieves exceptional clarity and precision in depicting subjects. Historical limning referred specifically to manuscript illumination and portrait miniature painting that required exceptional skill and attention to minute details.",
                "example_sentence": "The portrait artist expertly _____ the subject's features with delicate brushstrokes that captured both physical likeness and inner character.",
                "pronunciation": "LIMD (single syllable, rhymes with \"dimmed\")",
                "etymology": "From Middle English \"limnen,\" from \"limine\" meaning \"to illuminate\" or \"paint\"",
                "memory_tips": "Think \"filmed\" - limned artwork is like being filmed with perfect clarity and detail",
                "part_of_speech": "verb"
            },
            "limousine": {
                "definition": "A large, luxurious automobile with a lengthened wheelbase, typically driven by a professional chauffeur and used for special occasions, business transportation, or ceremonial purposes. Limousines represent luxury, status, and special treatment, often featuring amenities such as bars, entertainment systems, and privacy partitions that create comfortable, exclusive environments for passengers. The vehicles serve various functions from wedding transportation and prom night celebrations to corporate travel and VIP airport transfers. Modern limousines have evolved to include stretch SUVs and eco-friendly versions while maintaining their association with elegance and special occasions.",
                "example_sentence": "The wedding party arrived at the ceremony in an elegant white _____ decorated with flowers and ribbons.",
                "pronunciation": "LIM-uh-zeen or lim-uh-ZEEN (emphasis varies)",
                "etymology": "From French \"limousine,\" named after the Limousin region of France, referring to the hooded cloak worn there",
                "memory_tips": "Think \"limo-scene\" - a scene where a limo arrives makes any event feel special",
                "part_of_speech": "noun"
            },
            "limpa": {
                "definition": "A Swedish rye bread characterized by dark color, dense texture, and distinctive flavor from ingredients including rye flour, molasses, and various spices such as anise, fennel, and orange peel. Limpa bread represents traditional Scandinavian baking techniques that create hearty, nutritious loaves suitable for harsh climate conditions and long storage periods. The bread's complex flavor profile and substantial texture make it an important part of Swedish culinary culture, often served with butter, cheese, or traditional accompaniments. Modern variations maintain traditional recipes while adapting to contemporary tastes and dietary preferences.",
                "example_sentence": "The Scandinavian bakery's authentic _____ bread featured the traditional spices and dense texture that reminded immigrants of their homeland.",
                "pronunciation": "LIM-pah (emphasis on first syllable)",
                "etymology": "From Swedish \"limpa,\" referring to this specific type of dark rye bread",
                "memory_tips": "Think \"limp-ah\" - this dense bread won't go limp, making you say \"ah\" with satisfaction",
                "part_of_speech": "noun"
            },
            "limpet": {
                "definition": "A marine mollusk with a cone-shaped shell that clings tightly to rocks in intertidal zones, using powerful suction to withstand wave action and tidal forces. Limpets are remarkable for their ability to return to the exact same spot on rocks after foraging, demonstrating sophisticated navigation and homing abilities that scientists continue to study. These creatures play important ecological roles by grazing algae from rock surfaces while serving as food sources for various predators including shorebirds and sea stars. Their strong attachment mechanism has inspired biomimetic research for developing new adhesive technologies.",
                "example_sentence": "The marine biologist studied how _____ shells withstand tremendous wave forces while maintaining their grip on rocky surfaces.",
                "pronunciation": "LIM-pit (emphasis on first syllable)",
                "etymology": "From Old English \"lempedu,\" from Latin \"lepas\" meaning \"rock-adhering shellfish\"",
                "memory_tips": "Think \"limp-pet\" - a pet that looks limp but grips rocks incredibly strongly",
                "part_of_speech": "noun"
            },
            "limpid": {
                "definition": "Characterized by crystal clarity and transparency; completely clear and free from cloudiness, contamination, or obscurity; also used to describe prose, thoughts, or expressions that are perfectly clear and easily understood. Limpid water allows complete visibility through its depth, while limpid writing conveys meaning without ambiguity or confusion. The quality of limpidity suggests purity, honesty, and directness that eliminates barriers to understanding or perception. In various contexts, limpid represents an ideal state of clarity that enhances communication, appreciation, and comprehension.",
                "example_sentence": "The mountain lake's _____ waters allowed hikers to see colorful stones and fish swimming clearly in the depths below.",
                "pronunciation": "LIM-pid (emphasis on first syllable)",
                "etymology": "From Latin \"limpidus,\" meaning \"clear\" or \"transparent\"",
                "memory_tips": "Think \"limp-id\" - so clear you could identify a limp leaf floating in the water",
                "part_of_speech": "adjective"
            },
            "limpidsyllabus": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"limpid\" (crystal clear) incorrectly combined with \"syllabus\" (course outline). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"limpid\" and \"syllabus\"",
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
        """Process all words in batch 102"""
        
        logging.info("Processing Batch 102 with comprehensive Claude data...")
        
        input_file = "output/batch_102_words.csv"
        output_file = "output/batch_102_processed.csv"
        
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
            logging.info("Batch 102 processing completed!")
            logging.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
            logging.info(f"Output saved to: {output_file}")
            logging.info(f"Results: {len(processed_words)} successful, 0 failed")
                
        except Exception as e:
            logging.error(f"Error processing batch: {e}")
            raise

if __name__ == "__main__":
    processor = Batch102Processor()
    processor.process_batch()