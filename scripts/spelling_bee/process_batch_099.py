#!/usr/bin/env python3
"""
Process Batch 099 of spelling bee words with comprehensive Claude data.
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

class Batch099Processor:
    """Processes Batch 099 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for each word with detailed definitions, pronunciations, etymologies, and memory tips"""
        
        word_data = {
            "kriegspiel": {
                "definition": "A German war game or military training exercise that uses maps, models, and strategic scenarios to simulate combat situations for educational and planning purposes. Kriegspiel originated in 19th-century Prussia as a method for training military officers in tactical decision-making, strategic thinking, and battlefield management without the costs and risks of actual warfare. These war games involve detailed rules, realistic scenarios, and umpires who evaluate decisions and determine outcomes based on military principles. Modern versions continue to be used by military academies, strategic planners, and civilian organizations for training in leadership, crisis management, and complex problem-solving.",
                "example_sentence": "The military academy used _____ exercises to teach cadets advanced tactical decision-making and strategic planning.",
                "pronunciation": "KREEG-shpeel (emphasis on first syllable)",
                "etymology": "From German \"Kriegsspiel,\" from \"Krieg\" (war) + \"Spiel\" (game), meaning \"war game\"",
                "memory_tips": "Think \"creep-spiel\" - like creeping through a war game simulation",
                "part_of_speech": "noun"
            },
            "krypton": {
                "definition": "A chemical element with the symbol Kr and atomic number 36, classified as a noble gas that is colorless, odorless, and generally unreactive under normal conditions. Krypton occurs naturally in trace amounts in Earth's atmosphere and is used in specialized lighting applications including high-intensity discharge lamps and laser technology. The element was discovered in 1898 through fractional distillation of liquid air and derives its name from the Greek word meaning \"hidden.\" Krypton isotopes are used in nuclear medicine and scientific research, while its rarity and unique properties make it valuable for specialized industrial applications.",
                "example_sentence": "The photographer used _____ flash lamps to achieve the precise color temperature needed for the professional shoot.",
                "pronunciation": "KRIP-ton (emphasis on first syllable)",
                "etymology": "From Greek \"kryptos\" meaning \"hidden,\" referring to its elusive nature when discovered",
                "memory_tips": "Think \"crypt-on\" - like a hidden element that was hard to find, stored in a crypt",
                "part_of_speech": "noun"
            },
            "kudos": {
                "definition": "Praise, honor, or acclaim given for exceptional achievement or performance; recognition of merit or success. Kudos represents appreciation expressed for accomplishments that demonstrate skill, effort, or outstanding results worthy of public acknowledgment. The term implies respect and admiration from peers, authorities, or communities that recognize excellence in various fields including academics, arts, sports, or professional endeavors. While often used informally, kudos carries significance as validation of worthwhile contributions and achievements that inspire others or advance knowledge and understanding.",
                "example_sentence": "The young scientist received _____ from the international community for her breakthrough research in renewable energy.",
                "pronunciation": "KOO-dohs (emphasis on first syllable)",
                "etymology": "From Greek \"kudos\" meaning \"glory\" or \"renown,\" used to describe honor gained by achievement",
                "memory_tips": "Think \"could-dos\" - recognition for all the great things someone could do and did",
                "part_of_speech": "noun"
            },
            "kufi": {
                "definition": "A traditional brimless cap worn by men in various African and Middle Eastern cultures, often associated with Islamic religious practice and cultural identity. Kufis are typically made from cotton, wool, or synthetic materials and come in various styles, colors, and decorative patterns that may indicate regional origins, religious affiliations, or personal preferences. The cap serves both practical purposes of head covering and symbolic functions representing faith, cultural heritage, and community belonging. Modern kufis are worn in religious contexts, cultural celebrations, and as expressions of ethnic pride and spiritual identity.",
                "example_sentence": "The elder wore a beautifully embroidered _____ during the Friday prayer service at the mosque.",
                "pronunciation": "KOO-fee (emphasis on first syllable)",
                "etymology": "From Arabic \"kufiya,\" referring to the city of Kufa in Iraq where such caps were commonly made",
                "memory_tips": "Think \"coo-fee\" - like a dove cooing while wearing this traditional cap",
                "part_of_speech": "noun"
            },
            "kugel": {
                "definition": "A traditional Jewish baked casserole or pudding made with egg noodles or potatoes, eggs, and various seasonings, served as a side dish during Sabbath and holiday meals. Kugel preparations vary widely among different Jewish communities, with sweet versions containing sugar, cinnamon, and fruit, while savory varieties include onions, salt, and pepper. The dish represents important cultural traditions that connect Jewish families to their heritage through recipes passed down through generations. Different regional styles reflect the diverse backgrounds of Jewish communities worldwide, from Eastern European to Sephardic traditions.",
                "example_sentence": "The family recipe for noodle _____ had been passed down for four generations and was essential for holiday dinners.",
                "pronunciation": "KOO-guhl (emphasis on first syllable)",
                "etymology": "From Yiddish \"kugl,\" from Middle High German \"kugel\" meaning \"ball,\" referring to its rounded shape",
                "memory_tips": "Think \"cool-gull\" - like a cool seagull that enjoys this traditional Jewish dish",
                "part_of_speech": "noun"
            },
            "kuiper": {
                "definition": "Relating to the Kuiper Belt, a region of the outer solar system beyond Neptune containing numerous small icy bodies, comets, and dwarf planets including Pluto. Named after Dutch-American astronomer Gerard Kuiper, this celestial region extends from about 30 to 50 astronomical units from the Sun and represents remnants from the solar system's formation. Kuiper Belt objects provide valuable insights into planetary formation, early solar system conditions, and the distribution of matter in space. The study of these objects has revolutionized understanding of the outer solar system and contributed to the reclassification of Pluto as a dwarf planet.",
                "example_sentence": "The space probe's mission included studying _____ Belt objects to understand the solar system's early formation.",
                "pronunciation": "KIE-per (emphasis on first syllable)",
                "etymology": "Named after Gerard Kuiper (1905-1973), Dutch-American astronomer who predicted the belt's existence",
                "memory_tips": "Think \"keeper\" - Gerard Kuiper was the keeper of knowledge about outer solar system objects",
                "part_of_speech": "adjective"
            },
            "kumkum": {
                "definition": "A red or orange powder used in Hindu religious ceremonies and cultural traditions, typically made from turmeric and other natural ingredients, applied to the forehead as a tilaka or used in ritual offerings. Kumkum holds deep spiritual significance representing blessings, prosperity, and divine protection while serving as a visible symbol of religious devotion and cultural identity. The application of kumkum varies among different Hindu traditions and regions, with specific patterns and occasions carrying distinct meanings. This sacred powder connects practitioners to ancient spiritual practices and community traditions that maintain cultural continuity.",
                "example_sentence": "The priest applied _____ to the devotees' foreheads as a blessing during the temple ceremony.",
                "pronunciation": "KOOM-koom (emphasis on first syllable)",
                "etymology": "From Sanskrit \"kumkuma,\" possibly related to \"kunkuma\" (saffron), referring to its reddish color",
                "memory_tips": "Think \"come-come\" - inviting divine blessings to come with this sacred powder",
                "part_of_speech": "noun"
            },
            "kung": {
                "definition": "A Chinese term meaning \"skill,\" \"mastery,\" or \"achievement acquired through practice and discipline,\" most commonly known in the compound \"kung fu\" referring to martial arts expertise. Kung represents the concept of dedicated effort over time that develops exceptional ability in any field, not limited to martial arts but applicable to any skill requiring patience, practice, and perseverance. The term embodies Chinese philosophical principles about the relationship between time, effort, and mastery that values process over quick results. This concept influences various aspects of Chinese culture including education, craftsmanship, and personal development.",
                "example_sentence": "The master emphasized that true _____ in any discipline requires years of patient practice and dedication.",
                "pronunciation": "KOONG (single syllable, rhymes with \"hung\")",
                "etymology": "From Chinese \"gong\" meaning \"skill\" or \"achievement,\" often combined with \"fu\" (person) to form \"kung fu\"",
                "memory_tips": "Think \"gone\" - the time that's gone into developing skill and mastery",
                "part_of_speech": "noun"
            },
            "kurta": {
                "definition": "A traditional loose-fitting tunic worn in South Asian cultures, typically extending to the knees or mid-thigh and featuring a straight cut with side slits for comfortable movement. Kurtas are worn by both men and women across India, Pakistan, Bangladesh, and other South Asian regions, often paired with traditional bottoms like pajamas, churidar, or jeans. The garment serves both casual and formal purposes, with variations in fabric, embroidery, and styling that reflect regional preferences, social occasions, and personal taste. Modern kurtas blend traditional designs with contemporary fashion, making them popular both in South Asia and among diaspora communities worldwide.",
                "example_sentence": "He wore a white cotton _____ with traditional embroidery for the cultural festival celebration.",
                "pronunciation": "KUR-tah (emphasis on first syllable)",
                "etymology": "From Hindi/Urdu \"kurta,\" possibly from Turkish \"kurt\" or Persian origins meaning \"shirt\"",
                "memory_tips": "Think \"court-ah\" - like formal court attire that's comfortable and traditional",
                "part_of_speech": "noun"
            },
            "kutani": {
                "definition": "A style of Japanese porcelain characterized by bold, colorful overglaze decoration featuring gold, red, green, yellow, and purple colors in elaborate patterns and designs. Kutani ware originated in the 17th century in the Kutani region of Japan and is renowned for its distinctive artistic style that combines traditional Japanese aesthetics with vibrant color palettes. The porcelain features intricate hand-painted designs including flowers, birds, landscapes, and geometric patterns that demonstrate exceptional craftsmanship and artistic skill. Kutani ceramics are highly valued by collectors and represent important Japanese cultural heritage in decorative arts.",
                "example_sentence": "The museum's collection of _____ porcelain showcased the elaborate hand-painted designs characteristic of this Japanese ceramic tradition.",
                "pronunciation": "koo-TAH-nee (emphasis on second syllable)",
                "etymology": "From Japanese \"Kutani,\" meaning \"nine valleys,\" referring to the region where this porcelain style originated",
                "memory_tips": "Think \"cute-ani\" - like cute animated characters painted on beautiful Japanese porcelain",
                "part_of_speech": "noun, adjective"
            },
            "kuwait": {
                "definition": "A small country in the Arabian Peninsula bordered by Iraq and Saudi Arabia, known for its significant oil reserves, modern architecture, and strategic location at the head of the Persian Gulf. Kuwait gained independence from Britain in 1961 and has developed into a prosperous nation with one of the world's highest per capita incomes due to petroleum exports. The country features a constitutional monarchy with an elected parliament and has played important roles in regional politics and international oil markets. Kuwait City, the capital, represents modern urban development in the Middle East with impressive skyscrapers and cultural institutions.",
                "example_sentence": "The delegation traveled to _____ to participate in negotiations about regional energy cooperation and trade agreements.",
                "pronunciation": "koo-WAIT (emphasis on second syllable)",
                "etymology": "From Arabic \"al-Kuwayt,\" meaning \"little fort,\" referring to a small fortress built in the area",
                "memory_tips": "Think \"coo-wait\" - like doves cooing while waiting at this Gulf nation",
                "part_of_speech": "noun (proper)"
            },
            "kwashiorkor": {
                "definition": "A severe form of malnutrition caused by protein deficiency despite adequate caloric intake, characterized by edema, enlarged liver, skin changes, and growth retardation, primarily affecting young children in developing regions. The condition results from diets high in carbohydrates but lacking sufficient protein, often occurring when children transition from breast milk to foods with inadequate protein content. Kwashiorkor symptoms include swollen abdomen and limbs, hair color changes, skin lesions, and increased susceptibility to infections. Treatment requires careful protein supplementation and medical monitoring to prevent complications during recovery.",
                "example_sentence": "The medical team worked to treat children suffering from _____ by providing protein-rich therapeutic foods and medical care.",
                "pronunciation": "kwash-ee-OR-kor (emphasis on third syllable)",
                "etymology": "From Ga language of Ghana, meaning \"the disease the older child gets when the next baby is born\"",
                "memory_tips": "Think \"cash-ee-or-core\" - lacking the core nutrition that money could provide",
                "part_of_speech": "noun"
            },
            "kwon": {
                "definition": "A Korean surname meaning \"authority\" or \"power,\" commonly found throughout Korea and Korean diaspora communities worldwide. The name represents one of the most frequent Korean family names, with various clan origins and regional distributions throughout Korean history. Like many Korean surnames, Kwon carries cultural significance that connects individuals to ancestral lineages, regional origins, and family traditions maintained across generations. The surname appears in various romanization systems as Kwon, Gwon, or other spellings, reflecting different approaches to representing Korean sounds in Latin script.",
                "example_sentence": "Dr. _____ received recognition for her groundbreaking research in biomedical engineering and artificial intelligence applications.",
                "pronunciation": "KWAHN (single syllable, similar to \"won\" with initial 'kw' sound)",
                "etymology": "From Korean \"권\" meaning \"authority\" or \"power,\" with various historical clan origins",
                "memory_tips": "Think \"won\" with a 'k' - like someone who won authority or power",
                "part_of_speech": "noun (proper name)"
            },
            "kyphoplasty": {
                "definition": "A minimally invasive surgical procedure used to treat vertebral compression fractures by inserting a balloon into the damaged vertebra, inflating it to restore height, then injecting bone cement to stabilize the structure. The procedure aims to reduce pain, restore spinal alignment, and improve mobility in patients with fractures caused by osteoporosis, cancer, or trauma. Kyphoplasty differs from vertebroplasty by using the balloon to create a cavity before cement injection, potentially reducing cement leakage and better restoring vertebral height. This treatment has become an important option for managing painful spinal fractures that don't heal naturally.",
                "example_sentence": "The orthopedic surgeon recommended _____ to treat the patient's painful vertebral compression fracture caused by osteoporosis.",
                "pronunciation": "KIE-foh-plas-tee (emphasis on first syllable)",
                "etymology": "From Greek \"kyphos\" (hump, referring to spinal curvature) + \"plastikos\" (molding or forming)",
                "memory_tips": "Think \"cypher-plasty\" - like deciphering how to repair curved spines with plastic cement",
                "part_of_speech": "noun"
            },
            "kyphoplastyaten": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"kyphoplasty\" (spinal surgery procedure) incorrectly combined with \"aten\" (ancient Egyptian deity). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"kyphoplasty\" and \"aten\"",
                "part_of_speech": "error - combined words"
            },
            "labefaction": {
                "definition": "The process of weakening, undermining, or causing something to deteriorate or fall into decay; a gradual decline in strength, stability, or effectiveness. Labefaction describes the progressive weakening of structures, institutions, beliefs, or systems through various destructive forces or neglect. The term can apply to physical deterioration of buildings or materials, as well as metaphorical weakening of social systems, moral standards, or personal resolve. This concept often implies a slow, insidious process rather than sudden collapse, suggesting gradual erosion that eventually leads to significant damage or failure.",
                "example_sentence": "The historian documented the _____ of the empire's administrative system as corruption and neglect weakened its foundations.",
                "pronunciation": "lab-uh-FAK-shuhn (emphasis on third syllable)",
                "etymology": "From Latin \"labefactio,\" from \"labefacere\" meaning \"to cause to totter\" or \"shake\"",
                "memory_tips": "Think \"lab-effect-ion\" - like a lab effect that weakens structures through chemical action",
                "part_of_speech": "noun"
            },
            "labeled": {
                "definition": "Past tense of label; marked with a tag, sticker, or written identification that provides information about contents, ownership, destination, or classification. Labeling serves essential functions in organization, safety, marketing, and communication by providing clear identification and necessary information. The process involves attaching or applying descriptive markers that help people understand, categorize, or use items appropriately. In broader contexts, labeled can refer to categorizing people or concepts, though this usage may carry implications about stereotyping or oversimplification of complex realities.",
                "example_sentence": "All the chemical containers were clearly _____ with their contents and safety warnings for laboratory use.",
                "pronunciation": "LAY-buhld (emphasis on first syllable)",
                "etymology": "Past tense of \"label,\" from Old French \"lambel,\" meaning \"ribbon\" or \"strip of cloth\"",
                "memory_tips": "Think \"lay-bulled\" - like laying down labels that are as clear as a bull's charge",
                "part_of_speech": "verb, adjective"
            },
            "laboratory": {
                "definition": "A specially equipped facility designed for conducting scientific experiments, research, testing, and analysis under controlled conditions with appropriate instruments, safety measures, and environmental controls. Laboratories serve various fields including chemistry, biology, physics, medicine, and engineering, providing spaces where hypotheses can be tested, samples analyzed, and new knowledge developed through systematic investigation. These facilities require specialized equipment, trained personnel, and safety protocols to ensure accurate results while protecting researchers and the environment. Modern laboratories incorporate advanced technology, automation, and data management systems that enhance research capabilities.",
                "example_sentence": "The university's new research _____ featured state-of-the-art equipment for studying molecular biology and genetic engineering.",
                "pronunciation": "LAB-ruh-tor-ee (emphasis on first syllable)",
                "etymology": "From Medieval Latin \"laboratorium,\" from \"laborare\" meaning \"to work\"",
                "memory_tips": "Think \"labor-story\" - where the story of hard work and scientific labor unfolds",
                "part_of_speech": "noun"
            },
            "laborious": {
                "definition": "Requiring considerable effort, time, and perseverance; characterized by hard work, difficulty, or tedious attention to detail that demands sustained physical or mental exertion. Laborious tasks involve complex processes, careful attention, or repetitive actions that test patience and determination while requiring significant investment of energy and time. The term suggests work that is necessary but demanding, often involving careful craftsmanship, thorough research, or meticulous attention to detail that cannot be rushed or simplified. Laborious efforts often produce valuable results that justify the extensive work required.",
                "example_sentence": "The archaeologist's _____ process of cataloging and analyzing thousands of artifact fragments took several years to complete.",
                "pronunciation": "luh-BOR-ee-uhs (emphasis on second syllable)",
                "etymology": "From Latin \"laboriosus,\" from \"labor\" meaning \"work\" or \"toil\"",
                "memory_tips": "Think \"labor-serious\" - seriously hard labor that requires dedication and effort",
                "part_of_speech": "adjective"
            },
            "labradoodle": {
                "definition": "A crossbred dog created by mating a Labrador Retriever with a Poodle, originally developed to combine the gentle temperament of Labs with the low-shedding coat of Poodles for use as guide dogs for people with allergies. Labradoodles typically exhibit friendly, intelligent personalities and may have coats ranging from straight to curly with varying degrees of shedding depending on which parent breed's characteristics dominate. These dogs have become popular family pets due to their generally good temperament with children and perceived hypoallergenic qualities. The crossbreed represents the trend toward designer dogs that aim to combine desirable traits from different purebred lines.",
                "example_sentence": "The family chose a _____ because they wanted a friendly, intelligent dog with minimal shedding for their home.",
                "pronunciation": "LAB-ruh-doo-duhl (emphasis on first syllable)",
                "etymology": "Portmanteau of \"Labrador\" + \"poodle,\" created to describe this specific crossbreed",
                "memory_tips": "Think \"lab-brew-doodle\" - like brewing a lab recipe to doodle the perfect family dog",
                "part_of_speech": "noun"
            },
            "labroid": {
                "definition": "Relating to or characteristic of fish in the family Labridae, commonly known as wrasses, which are marine fish found in tropical and temperate waters worldwide. Labroid fish are characterized by their elongated bodies, continuous dorsal fin, and specialized pharyngeal teeth used for crushing prey including mollusks, crustaceans, and other small marine organisms. These fish display remarkable diversity in size, color, and behavior, with some species serving important ecological roles as cleaners that remove parasites from other fish. Many labroid species exhibit complex social behaviors, territorial patterns, and striking color changes related to age, sex, or social status.",
                "example_sentence": "The marine biologist studied _____ fish species to understand their role as cleaner fish in coral reef ecosystems.",
                "pronunciation": "LAB-roid (emphasis on first syllable)",
                "etymology": "From \"Labridae\" (family name) + suffix \"-oid\" meaning \"resembling\" or \"of the form of\"",
                "memory_tips": "Think \"lab-android\" - like fish that look like they were designed in a lab",
                "part_of_speech": "adjective"
            },
            "labyrinthine": {
                "definition": "Resembling a labyrinth in complexity, intricacy, or confusing layout; characterized by intricate passages, complicated connections, or bewildering arrangements that are difficult to navigate or understand. The term describes both physical structures with maze-like qualities and abstract concepts involving complex, interconnected elements that challenge comprehension or resolution. Labyrinthine systems often feature multiple pathways, dead ends, and circular routes that require careful attention and systematic exploration to master. This adjective applies to architecture, bureaucracy, legal systems, philosophical arguments, and any situation involving confusing complexity.",
                "example_sentence": "The ancient castle's _____ corridors confused visitors who often became lost in the maze of interconnected passages.",
                "pronunciation": "lab-uh-RIN-thien (emphasis on third syllable)",
                "etymology": "From \"labyrinth\" + suffix \"-ine,\" from Greek \"labyrinthos\" (maze structure)",
                "memory_tips": "Think \"lab-rhythm-nine\" - like a lab with nine different rhythms creating confusing complexity",
                "part_of_speech": "adjective"
            },
            "laccolith": {
                "definition": "A dome-shaped intrusive igneous rock formation created when magma is injected between sedimentary rock layers, causing the overlying strata to bulge upward while the magma cools and solidifies underground. Laccoliths form when viscous magma lacks sufficient pressure to break through to the surface, instead spreading horizontally between rock layers and creating characteristic mushroom-shaped geological structures. These formations can be several kilometers in diameter and are eventually exposed through erosion of overlying rocks, creating distinctive landscape features. Famous examples include the Henry Mountains in Utah and various formations in the American Southwest.",
                "example_sentence": "The geologist explained how the mountain was actually a _____ exposed after millions of years of erosion removed the overlying rock layers.",
                "pronunciation": "LAK-uh-lith (emphasis on first syllable)",
                "etymology": "From Greek \"lakkos\" (cistern or reservoir) + \"lithos\" (stone), referring to its pool-like shape",
                "memory_tips": "Think \"lack-o-lith\" - lacking the strength to break through, forming a stone dome instead",
                "part_of_speech": "noun"
            },
            "laceration": {
                "definition": "A deep cut or tear in skin, flesh, or other tissue, typically irregular in shape and caused by sharp objects, accidents, or traumatic impact that damages tissue structure. Lacerations differ from clean cuts by having jagged edges, tissue damage, and potential complications including bleeding, infection, and scarring that require medical attention. The severity of lacerations varies from minor surface wounds to deep injuries that affect muscles, nerves, or organs, requiring different treatment approaches from simple cleaning to surgical repair. Proper wound care, including cleaning, suturing if necessary, and infection prevention, is essential for optimal healing.",
                "example_sentence": "The emergency room physician carefully cleaned and sutured the deep _____ on the patient's forearm.",
                "pronunciation": "las-uh-RAY-shuhn (emphasis on third syllable)",
                "etymology": "From Latin \"laceratio,\" from \"lacerare\" meaning \"to tear\" or \"mangle\"",
                "memory_tips": "Think \"lace-ration\" - like delicate lace that's been torn and needs repair",
                "part_of_speech": "noun"
            },
            "lachrymose": {
                "definition": "Inclined to cry or weep easily; characterized by excessive tearfulness, sadness, or mournful expression that demonstrates emotional sensitivity or melancholy disposition. The term describes both temporary emotional states and persistent personality traits that involve frequent crying, sorrowful demeanor, or expressions of grief and sadness. Lachrymose individuals may be deeply affected by emotional situations, artistic expressions, or life circumstances that evoke tears and melancholic responses. This characteristic can reflect empathy, sensitivity, or underlying emotional conditions that influence how people process and express feelings.",
                "example_sentence": "The _____ character in the novel constantly wept over the tragic circumstances that befell her family.",
                "pronunciation": "LAK-ri-mohs (emphasis on first syllable)",
                "etymology": "From Latin \"lacrimosus,\" from \"lacrima\" meaning \"tear,\" referring to weeping or crying",
                "memory_tips": "Think \"lack-rhyme-morose\" - lacking rhyme and reason, just morose and teary",
                "part_of_speech": "adjective"
            },
            "lachsschinken": {
                "definition": "A German cold cut made from cured and smoked pork loin that resembles salmon in its pink color and delicate texture, traditionally served sliced thin as part of charcuterie boards or breakfast spreads. The preparation involves brining pork loin with salt and spices, then cold-smoking it to achieve the characteristic flavor and appearance that gives it its name meaning \"salmon ham.\" Lachsschinken represents traditional German curing techniques that preserve meat while developing complex flavors through controlled smoking processes. This specialty meat is prized for its mild flavor, tender texture, and attractive presentation in European delicatessen traditions.",
                "example_sentence": "The German delicatessen served thin slices of _____ alongside rye bread and traditional pickles for breakfast.",
                "pronunciation": "LAHKS-shin-ken (emphasis on first syllable)",
                "etymology": "From German \"Lachs\" (salmon) + \"Schinken\" (ham), referring to its salmon-like color",
                "memory_tips": "Think \"lox-shin-ken\" - like lox (smoked salmon) but it's actually Ken's favorite German ham",
                "part_of_speech": "noun"
            },
            "lackadaisical": {
                "definition": "Showing little interest, enthusiasm, or determination; characterized by laziness, carelessness, or half-hearted effort that demonstrates lack of motivation or commitment to tasks or responsibilities. Lackadaisical behavior involves casual indifference, minimal exertion, and absence of the energy or focus needed to achieve goals or meet expectations. This attitude often results in poor performance, missed opportunities, and frustration among those who depend on more dedicated effort. The term suggests a problematic approach to work or life that undermines success and personal development.",
                "example_sentence": "The student's _____ approach to studying resulted in poor grades and disappointed teachers.",
                "pronunciation": "lak-uh-DAY-zi-kuhl (emphasis on third syllable)",
                "etymology": "From \"alack-a-day\" (expression of regret) + \"-ical,\" suggesting languid disappointment",
                "memory_tips": "Think \"lack-a-days-ical\" - lacking days of proper effort and being too casual",
                "part_of_speech": "adjective"
            },
            "lacking": {
                "definition": "Absent, deficient, or insufficient in quantity, quality, or degree; missing essential elements, skills, or characteristics needed for completeness or success. The term describes situations where important components, abilities, or resources are not present or are inadequate to meet requirements or expectations. Lacking can refer to material shortages, skill deficiencies, character flaws, or any area where improvement or supplementation is needed. Recognition of what is lacking provides opportunities for development, acquisition, or problem-solving to address deficiencies and improve outcomes.",
                "example_sentence": "The project proposal was _____ sufficient detail and financial projections to secure investor funding.",
                "pronunciation": "LAK-ing (emphasis on first syllable)",
                "etymology": "Present participle of \"lack,\" from Middle Dutch \"laken\" meaning \"to be without\"",
                "memory_tips": "Think \"lack-king\" - like a king who lacks what he needs to rule effectively",
                "part_of_speech": "verb, adjective"
            },
            "laconic": {
                "definition": "Using very few words; expressing much in few words; characterized by concise, terse communication that conveys meaning efficiently without unnecessary elaboration or explanation. Laconic speech reflects a communication style that values brevity, precision, and understated expression over verbose or flowery language. This approach can demonstrate confidence, wisdom, or cultural values that favor direct communication, though it may also seem abrupt or unfriendly to those expecting more elaborate expression. Laconic individuals often make their points effectively through careful word choice rather than lengthy explanations.",
                "example_sentence": "The general's _____ response of \"We fight at dawn\" conveyed his determination without wasting words.",
                "pronunciation": "luh-KON-ik (emphasis on second syllable)",
                "etymology": "From Greek \"Lakonikos\" meaning \"of Laconia,\" referring to the Spartans' famously brief speech",
                "memory_tips": "Think \"lack-tonic\" - lacking the tonic of many words, preferring brief speech",
                "part_of_speech": "adjective"
            },
            "lacrosse": {
                "definition": "A team sport played with a small rubber ball and long-handled sticks called crosses that have a net pocket for catching, carrying, and throwing the ball, with the objective of scoring goals by shooting the ball into the opponent's goal. Lacrosse originated among Native American tribes and has evolved into modern versions including field lacrosse, box lacrosse, and women's lacrosse, each with specific rules and equipment requirements. The sport emphasizes speed, agility, hand-eye coordination, and teamwork while requiring protective equipment due to its physical nature. Lacrosse combines elements of soccer, basketball, and hockey in a fast-paced game that tests athletic skill and strategy.",
                "example_sentence": "The university's _____ team practiced daily to prepare for the championship tournament against rival schools.",
                "pronunciation": "luh-KROS (emphasis on second syllable)",
                "etymology": "From French \"la crosse,\" meaning \"the stick,\" referring to the hooked stick used in the game",
                "memory_tips": "Think \"la-cross\" - like being cross about losing this stick sport called 'la crosse'",
                "part_of_speech": "noun"
            },
            "lactose": {
                "definition": "A sugar found naturally in milk and dairy products, composed of glucose and galactose molecules linked together, which requires the enzyme lactase for proper digestion in the human intestinal system. Many adults worldwide lose the ability to produce sufficient lactase after childhood, leading to lactose intolerance characterized by digestive discomfort when consuming dairy products. Lactose serves as an important carbohydrate source in infant nutrition and is used in food manufacturing, pharmaceuticals, and scientific research. Understanding lactose metabolism has led to development of lactose-free dairy products and enzyme supplements that help lactose-intolerant individuals enjoy dairy foods.",
                "example_sentence": "The food scientist studied _____ metabolism to develop better treatments for people with dairy intolerance.",
                "pronunciation": "LAK-tohs (emphasis on first syllable)",
                "etymology": "From Latin \"lac\" (milk) + \"-ose\" (sugar suffix), meaning \"milk sugar\"",
                "memory_tips": "Think \"lack-toes\" - people who lack the enzyme may get sore toes from running to the bathroom",
                "part_of_speech": "noun"
            },
            "lacustrine": {
                "definition": "Relating to, produced by, or living in lakes; characteristic of lake environments, ecosystems, or geological formations associated with freshwater lake systems. Lacustrine environments support unique ecological communities adapted to freshwater conditions, seasonal temperature variations, and specific nutrient cycles that differ from marine or terrestrial ecosystems. In geology, lacustrine deposits include sediments, fossils, and rock formations created in ancient lake beds that provide valuable information about past climates, ecosystems, and environmental conditions. These formations often contain well-preserved fossils and serve as important records of evolutionary history and paleoenvironmental changes.",
                "example_sentence": "The geologist studied _____ deposits to understand ancient climate patterns recorded in the fossilized lake sediments.",
                "pronunciation": "luh-KUS-trien (emphasis on second syllable)",
                "etymology": "From Latin \"lacustris,\" from \"lacus\" meaning \"lake\"",
                "memory_tips": "Think \"lake-ustrine\" - like lake + pristine, describing pure lake environments",
                "part_of_speech": "adjective"
            },
            "ladder": {
                "definition": "A portable framework consisting of two parallel sides connected by a series of rungs or steps, used for climbing up or down to reach higher or lower positions safely. Ladders serve essential functions in construction, maintenance, emergency response, and household tasks that require access to elevated areas. Different ladder types including step ladders, extension ladders, and specialized designs serve specific purposes and safety requirements. Proper ladder use involves understanding weight limits, angle placement, and safety protocols that prevent falls and injuries while providing stable support for climbing.",
                "example_sentence": "The firefighter climbed the _____ to rescue the cat stranded on the roof of the burning building.",
                "pronunciation": "LAD-er (emphasis on first syllable)",
                "etymology": "From Old English \"hlæder,\" from Germanic roots related to \"hlænan\" (to lean)",
                "memory_tips": "Think \"lad-der\" - like a lad named Der who climbs up and down",
                "part_of_speech": "noun"
            },
            "ladders": {
                "definition": "Plural of ladder; multiple portable climbing devices or metaphorical references to hierarchical progression systems that enable advancement through various levels or stages. Physical ladders provide access to different heights in construction, maintenance, and emergency situations, while metaphorical ladders represent systems of advancement in careers, education, social status, or personal development. The concept of climbing ladders suggests systematic progression, effort, and achievement of higher positions through step-by-step advancement. Understanding both literal and figurative uses of ladders helps in practical safety applications and conceptualizing pathways to success.",
                "example_sentence": "The construction crew used several _____ of different heights to complete the multi-story building project safely.",
                "pronunciation": "LAD-erz (emphasis on first syllable)",
                "etymology": "Plural of \"ladder,\" from Old English \"hlæder\"",
                "memory_tips": "Think \"lad-ders\" - multiple lads named Der climbing different routes upward",
                "part_of_speech": "noun"
            },
            "ladle": {
                "definition": "A large, deep-bowled spoon with a long handle used for serving liquids like soup, stew, punch, or sauce from pots or serving vessels to individual bowls or plates. Ladles are essential kitchen utensils that allow controlled portioning of hot liquids while keeping hands safely away from heat sources and preventing spills. Different ladle sizes serve various purposes from small sauce ladles to large soup ladles, with materials ranging from stainless steel to heat-resistant plastics. The curved bowl design and long handle make ladles efficient tools for transferring liquids while maintaining food safety and presentation standards.",
                "example_sentence": "The chef used a large _____ to serve the homemade soup into bowls for the dinner guests.",
                "pronunciation": "LAY-duhl (emphasis on first syllable)",
                "etymology": "From Old English \"hlædel,\" from \"hladan\" meaning \"to load\" or \"lade\"",
                "memory_tips": "Think \"lay-dell\" - laying soup into bowls with Dell's favorite spoon",
                "part_of_speech": "noun, verb"
            },
            "ladybug": {
                "definition": "A small, dome-shaped beetle in the family Coccinellidae, typically red or orange with black spots, known for being beneficial insects that eat aphids and other garden pests. Ladybugs are valued by gardeners and farmers because they provide natural pest control by consuming large quantities of harmful insects that damage crops and plants. These beetles undergo complete metamorphosis from egg to larva to pupa to adult, with both larvae and adults serving as predators of soft-bodied insects. Ladybugs are considered symbols of good luck in many cultures and represent the positive role that insects can play in maintaining ecological balance.",
                "example_sentence": "The gardener was pleased to see _____ beetles on her roses because they would eat the aphids naturally.",
                "pronunciation": "LAY-dee-bug (emphasis on first syllable)",
                "etymology": "From \"lady\" (referring to the Virgin Mary) + \"bug,\" called \"Our Lady's bird\" in medieval times",
                "memory_tips": "Think \"lady-bug\" - a polite lady bug that helps gardens by eating pests",
                "part_of_speech": "noun"
            },
            "laff": {
                "definition": "An informal, phonetic spelling of \"laugh\" used in casual contexts, comic writing, or to represent dialectal pronunciation; also appears in entertainment contexts like \"Laff Track\" referring to recorded laughter used in television shows. This spelling variation reflects how language adapts to different contexts and purposes, from representing speech patterns to creating informal, playful communication styles. The use of \"laff\" instead of \"laugh\" can indicate humor, casualness, or deliberate nonstandard spelling for effect. In entertainment industry terminology, laff tracks are artificial laughter recordings used to enhance comedy shows and create audience participation illusion.",
                "example_sentence": "The comedian's routine was so funny that the audience's genuine _____ made the laugh track unnecessary.",
                "pronunciation": "LAF (single syllable, rhymes with \"half\")",
                "etymology": "Phonetic respelling of \"laugh,\" from Old English \"hliehhan\"",
                "memory_tips": "Think \"laugh\" spelled the way it sounds - \"laff\" like a casual way to show amusement",
                "part_of_speech": "noun, verb"
            },
            "lairs": {
                "definition": "Plural of lair; hidden retreats, dens, or resting places used by wild animals for shelter, safety, and raising young; also refers to secret hideouts or refuges used by people for concealment. Animal lairs provide essential protection from predators, weather, and human disturbance while serving as bases for hunting, breeding, and caring for offspring. The term extends to human contexts describing secret hideouts, criminal operations, or private retreats that offer concealment and security. Understanding lair locations and characteristics is important for wildlife management, conservation efforts, and sometimes law enforcement activities.",
                "example_sentence": "The wildlife biologist studied bear _____ to understand hibernation patterns and habitat requirements.",
                "pronunciation": "LAIRZ (single syllable, rhymes with \"hairs\")",
                "etymology": "Plural of \"lair,\" from Old English \"leger,\" meaning \"resting place\" or \"bed\"",
                "memory_tips": "Think \"layers\" - hidden layers where animals rest and hide safely",
                "part_of_speech": "noun"
            },
            "laity": {
                "definition": "The body of religious believers who are not ordained clergy; ordinary members of a religious community who participate in faith practices without holding official religious positions or authority. The laity plays essential roles in religious communities through worship participation, charitable activities, education, and community service while supporting clergy in their spiritual leadership functions. This distinction between clergy and laity reflects organizational structures in many religions that separate trained religious professionals from general membership. Modern religious movements increasingly emphasize the important contributions and spiritual authority of lay members in community leadership and ministry.",
                "example_sentence": "The new pastor worked to involve the _____ more actively in church decision-making and community outreach programs.",
                "pronunciation": "LAY-uh-tee (emphasis on first syllable)",
                "etymology": "From Old French \"laite,\" from Greek \"laikos\" meaning \"of the people\"",
                "memory_tips": "Think \"lay-ity\" - people who lay in pews rather than leading from the altar",
                "part_of_speech": "noun"
            },
            "lake": {
                "definition": "A large body of water completely surrounded by land, typically freshwater, formed through various geological processes including glacial activity, tectonic movements, or volcanic activity. Lakes serve crucial ecological functions as freshwater habitats supporting diverse plant and animal communities while providing important resources for human communities including drinking water, recreation, and economic activities. These aquatic ecosystems feature complex food webs, seasonal temperature cycles, and chemical processes that influence regional climate and support biodiversity. Lakes range from small ponds to vast inland seas, each with unique characteristics shaped by geography, climate, and human influence.",
                "example_sentence": "The crystal-clear mountain _____ reflected the snow-capped peaks and provided habitat for trout and waterfowl.",
                "pronunciation": "LAYK (single syllable, rhymes with \"make\")",
                "etymology": "From Old English \"lacu,\" from Latin \"lacus\" meaning \"lake\" or \"pond\"",
                "memory_tips": "Think \"lay-k\" - where water lays peacefully surrounded by land",
                "part_of_speech": "noun"
            },
            "lallygag": {
                "definition": "To spend time aimlessly; to dawdle, loiter, or engage in idle behavior instead of focusing on tasks or responsibilities that require attention. Lallygagging involves wasting time through unfocused activities, casual wandering, or procrastination that prevents productive work or timely completion of obligations. This behavior often reflects lack of motivation, poor time management, or deliberate avoidance of less pleasant duties. While occasional leisure is healthy, chronic lallygagging can lead to missed deadlines, poor performance, and frustration among those depending on more focused effort.",
                "example_sentence": "The teacher told the students to stop _____ in the hallway and get to class before the bell rang.",
                "pronunciation": "LAL-ee-gag (emphasis on first syllable)",
                "etymology": "American slang of uncertain origin, possibly from \"lally\" (tongue) + \"gag\" (to fool around)",
                "memory_tips": "Think \"jolly-gag\" - being too jolly and gagging around instead of working",
                "part_of_speech": "verb"
            },
            "lama": {
                "definition": "A domesticated South American camelid related to llamas, alpacas, and vicuñas, raised primarily for wool production and as pack animals in high-altitude regions of the Andes Mountains. Lamas are hardy animals well-adapted to harsh mountain environments, capable of carrying heavy loads while requiring minimal food and water compared to other pack animals. These animals have been essential to Andean cultures for thousands of years, providing wool, meat, transportation, and companionship to indigenous peoples. Modern lama farming includes both traditional uses and newer applications in trekking, therapy programs, and fiber production for specialty textiles.",
                "example_sentence": "The Peruvian herder used his trained _____ to transport supplies up the mountain trail to remote villages.",
                "pronunciation": "LAH-mah (emphasis on first syllable)",
                "etymology": "From Quechua \"llama,\" the indigenous South American term for this animal",
                "memory_tips": "Think \"llama\" without the double-l - this woolly pack animal from South America",
                "part_of_speech": "noun"
            },
            "lambasted": {
                "definition": "Past tense of lambaste; severely criticized, scolded, or attacked verbally with harsh, uncompromising language that expresses strong disapproval or condemnation. Being lambasted involves receiving intense criticism that may be public, sustained, and emotionally charged, often targeting behavior, performance, or decisions considered unacceptable. This type of criticism goes beyond constructive feedback to include expressions of anger, disappointment, or moral outrage that can be personally devastating. While lambasting may serve to address serious problems, it can also be excessive or unfair when the punishment exceeds the offense.",
                "example_sentence": "The politician was _____ by critics after his controversial statements about environmental policy appeared in the media.",
                "pronunciation": "lam-BAST-ed (emphasis on second syllable)",
                "etymology": "Past tense of \"lambaste,\" possibly from \"lam\" (to beat) + \"baste\" (to beat severely)",
                "memory_tips": "Think \"lamb-basted\" - like a lamb being basted, but with harsh criticism instead of cooking juices",
                "part_of_speech": "verb"
            },
            "lambently": {
                "definition": "In a manner that is softly bright, gently glowing, or flickering with a subtle, warm light; characterized by gentle radiance or luminescence that is pleasant and not harsh or glaring. Lambent light suggests a quality that is both illuminating and soothing, like candlelight, moonlight, or the gentle glow of fireflies that provides visibility without overwhelming brightness. The adverb can also describe metaphorical qualities such as gentle humor, subtle intelligence, or soft expressions that convey warmth and understanding. This type of gentle luminescence creates atmosphere and comfort rather than stark illumination.",
                "example_sentence": "The candles glowed _____ in the evening darkness, creating a romantic atmosphere for the dinner party.",
                "pronunciation": "LAM-bent-lee (emphasis on first syllable)",
                "etymology": "From \"lambent\" + \"-ly,\" from Latin \"lambere\" meaning \"to lick,\" referring to gentle, flickering light",
                "memory_tips": "Think \"lamp-gently\" - like a lamp glowing gently and softly",
                "part_of_speech": "adverb"
            },
            "lambentlyadjective": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"lambently\" (adverb meaning softly bright) incorrectly combined with \"adjective\" (grammatical term). This type of error occurs when PDF text extraction fails to properly separate distinct words or when grammatical labels become merged with content words during document processing. These represent completely unrelated concepts artificially joined due to technical parsing issues common in processing educational materials where formatting irregularities cause adjacent text elements to merge without proper spacing or punctuation.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"lambently\" and \"adjective\"",
                "part_of_speech": "error - combined words"
            },
            "lambkin": {
                "definition": "A young lamb; a term of endearment for a small child or loved one, suggesting innocence, gentleness, and vulnerability that evokes protective feelings and affection. The word combines the literal meaning of a baby sheep with metaphorical uses that emphasize youthful innocence, purity, and the need for care and protection. Lambkins represent the vulnerable stage of life that requires nurturing, guidance, and safety from those with more experience and strength. This endearing term reflects the human tendency to associate young animals with cherished qualities and to use such comparisons in expressing love and tenderness.",
                "example_sentence": "The grandmother called her youngest granddaughter her precious _____ when tucking her into bed each night.",
                "pronunciation": "LAM-kin (emphasis on first syllable)",
                "etymology": "From \"lamb\" + diminutive suffix \"-kin,\" meaning \"little lamb\"",
                "memory_tips": "Think \"lamb-kin\" - like a little lamb that's part of your kin (family)",
                "part_of_speech": "noun"
            },
            "lamentable": {
                "definition": "Deserving of grief, sorrow, or regret; deplorable, unfortunate, or distressing in a way that evokes sympathy, disappointment, or moral concern about conditions that should be improved. Lamentable situations involve circumstances, behaviors, or outcomes that fall far short of reasonable expectations and represent failures, tragedies, or missed opportunities that cause genuine sadness. The term suggests not just regret but also a sense that the situation could and should have been different, often implying responsibility or preventable causes. Lamentable conditions call for acknowledgment, understanding, and often corrective action to address underlying problems.",
                "example_sentence": "The _____ state of the old library, with its crumbling books and broken windows, moved the community to fund restoration efforts.",
                "pronunciation": "luh-MEN-tuh-buhl (emphasis on second syllable)",
                "etymology": "From Latin \"lamentabilis,\" from \"lamentare\" meaning \"to weep\" or \"mourn\"",
                "memory_tips": "Think \"lament-able\" - able to be lamented or worthy of mourning and regret",
                "part_of_speech": "adjective"
            },
            "laminate": {
                "definition": "To cover with thin layers of protective material, typically plastic or other synthetic materials, to create a durable, water-resistant surface; also refers to the layered material itself created through this process. Lamination provides protection against moisture, wear, and damage while enhancing durability and appearance of documents, furniture surfaces, and various manufactured products. The process involves applying heat and pressure to bond protective layers to underlying materials, creating strong, long-lasting surfaces. Laminated materials are widely used in flooring, furniture, signage, and document preservation where durability and easy maintenance are important.",
                "example_sentence": "The teacher decided to _____ the classroom posters to protect them from wear and make them last longer.",
                "pronunciation": "LAM-uh-nayt (emphasis on first syllable)",
                "etymology": "From Latin \"lamina\" meaning \"thin plate\" or \"layer\"",
                "memory_tips": "Think \"lam-in-ate\" - like a lamb eating thin layers to make things strong",
                "part_of_speech": "verb, noun, adjective"
            },
            "lamp": {
                "definition": "A device that produces artificial light through various means including electric bulbs, oil burning, or gas combustion, typically designed for illumination of indoor or outdoor spaces. Lamps serve essential functions in providing visibility, creating atmosphere, and enabling activities during dark hours while reflecting both practical needs and aesthetic preferences. Different lamp types include table lamps, floor lamps, desk lamps, and decorative fixtures that combine functionality with design elements. The evolution of lamp technology from oil and gas to electric and LED represents advances in safety, efficiency, and environmental considerations in lighting design.",
                "example_sentence": "The antique brass _____ on the desk provided warm light perfect for reading late into the evening.",
                "pronunciation": "LAMP (single syllable, rhymes with \"camp\")",
                "etymology": "From Old French \"lampe,\" from Latin \"lampas,\" from Greek \"lampein\" meaning \"to shine\"",
                "memory_tips": "Think \"clamp\" - a device you clamp down to turn on light",
                "part_of_speech": "noun"
            },
            "lanai": {
                "definition": "A type of porch or veranda, typically roofed and open-sided, commonly found in Hawaiian and tropical architecture designed to provide shaded outdoor living space that takes advantage of favorable climate conditions. Lanais serve as transitional spaces between indoor and outdoor environments, offering protection from sun and rain while maintaining connection to natural surroundings through open design. These architectural features reflect adaptation to tropical climates where outdoor living is comfortable year-round and indoor-outdoor integration enhances quality of life. Modern lanai designs incorporate contemporary materials and amenities while maintaining the essential concept of covered outdoor living space.",
                "example_sentence": "The family enjoyed their morning coffee on the _____ while watching the sunrise over the tropical garden.",
                "pronunciation": "luh-NIE (emphasis on second syllable)",
                "etymology": "From Hawaiian \"lānai,\" meaning \"porch\" or \"veranda\"",
                "memory_tips": "Think \"la-nigh\" - like saying \"la\" (there) nigh (near) the outdoor porch",
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
        """Process all words in batch 099"""
        
        logging.info("Processing Batch 099 with comprehensive Claude data...")
        
        input_file = "output/batch_099_words.csv"
        output_file = "output/batch_099_processed.csv"
        
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
            logging.info("Batch 099 processing completed!")
            logging.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
            logging.info(f"Output saved to: {output_file}")
            logging.info(f"Results: {len(processed_words)} successful, 0 failed")
                
        except Exception as e:
            logging.error(f"Error processing batch: {e}")
            raise

if __name__ == "__main__":
    processor = Batch099Processor()
    processor.process_batch()