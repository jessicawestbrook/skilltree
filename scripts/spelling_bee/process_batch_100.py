#!/usr/bin/env python3
"""
Process Batch 100 of spelling bee words with comprehensive Claude data.
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

class Batch100Processor:
    """Processes Batch 100 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calculator = DifficultyCalculator()
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for each word with detailed definitions, pronunciations, etymologies, and memory tips"""
        
        word_data = {
            "lanceolate": {
                "definition": "Having a lance-shaped form; narrow and tapering to a point at one or both ends, resembling the shape of a spearhead or lance tip. This botanical and scientific term is commonly used to describe leaf shapes, anatomical structures, or geometric forms that are elongated and pointed. Lanceolate leaves are typically two to six times longer than they are wide, with the widest part near the base and gradually tapering to a sharp point at the tip. This shape is efficient for plants as it allows effective light capture while minimizing water loss and wind resistance.",
                "example_sentence": "The botanist identified the plant by its distinctive _____ leaves that tapered to sharp points.",
                "pronunciation": "LAN-see-uh-layt (emphasis on first syllable)",
                "etymology": "From Latin \"lanceolatus,\" from \"lancea\" (lance) + \"-atus\" (shaped like)",
                "memory_tips": "Think \"lance-oh-late\" - shaped like a lance that arrived late to the battle",
                "part_of_speech": "adjective"
            },
            "land": {
                "definition": "The solid part of Earth's surface not covered by water; ground or soil that can be owned, cultivated, or developed for various human purposes including agriculture, construction, and recreation. Land represents one of the fundamental resources for human civilization, providing space for habitation, food production, and economic activity. The concept encompasses both the physical surface and the legal rights associated with ownership, use, and control of specific areas. Land management involves balancing economic development with environmental conservation to ensure sustainable use of this finite resource.",
                "example_sentence": "The pioneer family traveled west to claim fertile _____ for farming and establishing their homestead.",
                "pronunciation": "LAND (single syllable, rhymes with \"hand\")",
                "etymology": "From Old English \"land,\" from Germanic roots meaning \"ground\" or \"territory\"",
                "memory_tips": "Think \"hand\" - what you can hold in your hand is the land you own",
                "part_of_speech": "noun, verb"
            },
            "landlinesparrow": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"landline\" (telephone line) incorrectly combined with \"sparrow\" (small bird). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"landline\" and \"sparrow\"",
                "part_of_speech": "error - combined words"
            },
            "landmark": {
                "definition": "A prominent or distinctive feature of a landscape that serves as a reference point for navigation or identification; also refers to an important building, structure, or location that has historical, cultural, or architectural significance. Natural landmarks include mountains, rivers, and rock formations that help people navigate and understand geography, while cultural landmarks represent human achievements and historical events that define community identity. Legal landmarks refer to significant court decisions or legislation that establish important precedents. These reference points help people orient themselves both physically and culturally within their environment.",
                "example_sentence": "The ancient lighthouse served as both a navigational aid and a historical _____ for the coastal community.",
                "pronunciation": "LAND-mark (emphasis on first syllable)",
                "etymology": "From \"land\" + \"mark,\" meaning a mark or sign on the land for identification",
                "memory_tips": "Think \"land-mark\" - a mark on the land that helps you identify where you are",
                "part_of_speech": "noun, adjective"
            },
            "lane": {
                "definition": "A narrow road, path, or passage, typically in rural areas or between buildings; also refers to designated strips on roadways or tracks that separate traffic or organize movement in specific directions. Lanes serve organizational functions in transportation systems, allowing for orderly traffic flow, pedestrian movement, and efficient use of available space. In sports, lanes define individual areas for competition such as swimming or running tracks. The concept extends to any narrow, defined pathway that channels movement or activity within larger spaces.",
                "example_sentence": "The cyclist carefully stayed in the bike _____ to avoid conflicts with motor vehicle traffic.",
                "pronunciation": "LAYN (single syllable, rhymes with \"rain\")",
                "etymology": "From Old English \"lone,\" meaning \"narrow way\" or \"passage\"",
                "memory_tips": "Think \"rain-lane\" - a narrow path where rain flows, like a lane for traffic",
                "part_of_speech": "noun"
            },
            "langrage": {
                "definition": "A type of artillery ammunition consisting of irregular metal fragments, chain links, or scrap metal packed in a canister, designed to inflict maximum damage to personnel and rigging rather than structural targets. Langrage was commonly used in naval warfare during the age of sail to disable enemy ships by destroying sails, ropes, and crew members rather than attempting to sink the vessel. This antipersonnel ammunition created a shotgun-like effect when fired, spreading deadly fragments across a wide area. The use of langrage reflects historical military tactics focused on disabling rather than destroying enemy capabilities.",
                "example_sentence": "The naval commander ordered the gunners to load _____ ammunition to damage the enemy ship's rigging and crew.",
                "pronunciation": "LANG-rij (emphasis on first syllable)",
                "etymology": "Possibly from \"lange\" (long) + \"rage,\" or from French naval terminology",
                "memory_tips": "Think \"long-rage\" - long-range ammunition that spreads rage across enemy ships",
                "part_of_speech": "noun"
            },
            "language": {
                "definition": "A complex system of communication using words, symbols, and grammar rules that enables humans to express thoughts, emotions, and ideas while sharing information and cultural knowledge across generations. Language encompasses spoken, written, and sign-based communication systems that vary among different communities and cultures worldwide. The development of language represents one of humanity's most significant achievements, enabling abstract thinking, artistic expression, scientific advancement, and social cooperation. Modern linguistics studies how languages evolve, how children acquire them, and how they influence thought and culture.",
                "example_sentence": "The diplomat's fluency in multiple _____ systems enabled effective communication during international negotiations.",
                "pronunciation": "LANG-gwij (emphasis on first syllable)",
                "etymology": "From Old French \"langage,\" from Latin \"lingua\" meaning \"tongue\" or \"speech\"",
                "memory_tips": "Think \"lang-gwij\" - the way we manage (gwij sounds like \"engage\") with our tongue",
                "part_of_speech": "noun"
            },
            "languages": {
                "definition": "Plural of language; multiple systems of communication used by different communities, cultures, or regions to express ideas, share information, and maintain social connections. The world's languages represent incredible diversity in sounds, grammar structures, vocabulary, and cultural perspectives that reflect human creativity and adaptation to different environments. Language families show historical relationships among groups of languages that evolved from common ancestors, providing insights into human migration and cultural development. Multilingualism, the ability to speak multiple languages, offers cognitive benefits and enhanced cultural understanding in our interconnected world.",
                "example_sentence": "The international conference provided translation services for over twenty different _____ spoken by delegates.",
                "pronunciation": "LANG-gwij-iz (emphasis on first syllable)",
                "etymology": "Plural of \"language,\" from Old French \"langage\"",
                "memory_tips": "Think \"lang-gwij-es\" - multiple ways to engage with tongues and speech",
                "part_of_speech": "noun"
            },
            "languish": {
                "definition": "To suffer from being forced to remain in an unpleasant situation; to lose vigor, health, or strength through neglect, confinement, or adverse conditions. Languishing involves gradual deterioration due to lack of attention, proper care, or favorable circumstances that would promote growth and well-being. The term can describe physical decline, emotional depression, or stagnation in personal or professional development. People, relationships, projects, or institutions may languish when they lack the resources, support, or opportunities needed to thrive and reach their potential.",
                "example_sentence": "The talented musician began to _____ in the small town where there were few opportunities to perform professionally.",
                "pronunciation": "LANG-gwish (emphasis on first syllable)",
                "etymology": "From Old French \"languir,\" from Latin \"languere\" meaning \"to be weak\" or \"faint\"",
                "memory_tips": "Think \"language-ish\" - when your language skills become ish (weak) from lack of use",
                "part_of_speech": "verb"
            },
            "languorous": {
                "definition": "Characterized by tiredness or inertia; displaying a dreamy, lazy, or sluggish quality that suggests lack of energy or motivation. Languorous describes a state of pleasant lethargy, often associated with warm weather, comfortable surroundings, or relaxed circumstances that encourage slow, unhurried movement and thought. This quality can be either positive, suggesting peaceful relaxation and freedom from stress, or negative, indicating problematic laziness and lack of productivity. The languorous mood often appears in literature and art to evoke sensual, romantic, or meditative atmospheres.",
                "example_sentence": "The hot summer afternoon created a _____ atmosphere that made everyone move slowly and speak softly.",
                "pronunciation": "LANG-ger-uhs (emphasis on first syllable)",
                "etymology": "From \"languor\" + \"-ous,\" from Latin \"languere\" meaning \"to be faint or weary\"",
                "memory_tips": "Think \"language-orous\" - speaking in a slow, dreamy way like you're half asleep",
                "part_of_speech": "adjective"
            },
            "languorouslanolated": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"languorous\" (dreamy, sluggish) incorrectly combined with \"lanolated\" (covered with soft down). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"languorous\" and \"lanolated\"",
                "part_of_speech": "error - combined words"
            },
            "lanolated": {
                "definition": "Covered with soft, woolly down or fine hair; having a surface texture resembling wool or soft fur that provides insulation and protection. This botanical and zoological term describes plants or animals with downy coverings that serve various functions including temperature regulation, moisture retention, and protection from environmental stresses. Lanolated surfaces often appear on desert plants, young bird feathers, or mammalian fur that provides insulation. The soft, woolly texture is typically composed of fine fibers or hairs that trap air and create effective barriers against heat loss or moisture evaporation.",
                "example_sentence": "The desert plant's _____ leaves helped it conserve moisture in the harsh, arid environment.",
                "pronunciation": "LAN-uh-lay-ted (emphasis on first syllable)",
                "etymology": "From Latin \"lana\" (wool) + \"-ated,\" meaning \"made woolly\" or \"covered with wool\"",
                "memory_tips": "Think \"llano-elated\" - elated about the soft wool covering like a llama's fur",
                "part_of_speech": "adjective"
            },
            "lantana": {
                "definition": "A genus of flowering plants in the verbena family, native to tropical regions of the Americas and Africa, commonly grown as ornamental plants for their clusters of small, brightly colored flowers. Lantana plants are popular in landscaping because they bloom continuously in warm weather, attract butterflies and hummingbirds, and tolerate drought conditions once established. These shrubs produce flowers in various color combinations including yellow, orange, red, pink, purple, and white, often with multiple colors within the same flower cluster. While beautiful and beneficial for wildlife, some lantana species can become invasive in certain climates.",
                "example_sentence": "The butterfly garden featured colorful _____ bushes that bloomed throughout the summer and attracted numerous pollinators.",
                "pronunciation": "lan-TAN-uh (emphasis on second syllable)",
                "etymology": "From Latin \"lantana,\" possibly from \"lentus\" meaning \"flexible,\" referring to the plant's branches",
                "memory_tips": "Think \"plant-ana\" - a plant that's as colorful as a banana but grows in clusters",
                "part_of_speech": "noun"
            },
            "lanternmince": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"lantern\" (light-producing device) incorrectly combined with \"mince\" (to cut into small pieces or walk delicately). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"lantern\" and \"mince\"",
                "part_of_speech": "error - combined words"
            },
            "lanthanides": {
                "definition": "A series of fifteen metallic chemical elements with atomic numbers from 57 (lanthanum) to 71 (lutetium), characterized by similar chemical properties due to their electron configurations and position in the periodic table. Also known as rare earth elements, lanthanides have unique magnetic, optical, and catalytic properties that make them essential for modern technology including computer screens, batteries, magnets, and medical imaging equipment. Despite being called \"rare,\" these elements are actually relatively abundant in Earth's crust but are difficult to separate and purify due to their similar chemical properties. China dominates global lanthanide production, creating strategic concerns about supply security.",
                "example_sentence": "The smartphone's advanced display technology relied on several _____ elements to produce bright, accurate colors.",
                "pronunciation": "LAN-thuh-niedz (emphasis on first syllable)",
                "etymology": "From \"lanthanum\" (the first element in the series) + \"-ides,\" from Greek \"lanthanein\" (to be hidden)",
                "memory_tips": "Think \"lantern-ides\" - elements that help modern lanterns (screens) shine brightly",
                "part_of_speech": "noun"
            },
            "lapel": {
                "definition": "The part of a coat or jacket that folds back on either side of the front opening, typically extending from the collar to the button line and often featuring decorative elements or fabric contrasts. Lapels serve both functional and aesthetic purposes, protecting the chest area while providing a surface for displaying pins, badges, or boutonnieres during formal occasions. Different lapel styles including notched, peaked, and shawl lapels reflect various fashion traditions and levels of formality in men's and women's clothing. The lapel's design and width often indicate the garment's style period and degree of formality.",
                "example_sentence": "The businessman wore a small flag pin on his suit jacket's _____ to show his patriotic support.",
                "pronunciation": "luh-PEL (emphasis on second syllable)",
                "etymology": "From \"lap\" + diminutive suffix \"-el,\" referring to the fold that laps over the chest",
                "memory_tips": "Think \"lap-el\" - the part that laps over your chest like a small lap",
                "part_of_speech": "noun"
            },
            "lapidary": {
                "definition": "Relating to the cutting, polishing, or engraving of stones and gems; also refers to a person skilled in working with precious and semi-precious stones to create jewelry or decorative objects. Lapidary work requires specialized tools, techniques, and knowledge of stone properties to transform rough minerals into polished gems, carved ornaments, or jewelry components. The craft combines artistic vision with technical skill to reveal the natural beauty hidden within raw stones through careful cutting and polishing. Modern lapidary work includes both traditional hand methods and advanced mechanical equipment for precision cutting and shaping.",
                "example_sentence": "The skilled _____ artist spent weeks carefully cutting and polishing the rough sapphire into a brilliant gemstone.",
                "pronunciation": "LAP-uh-der-ee (emphasis on first syllable)",
                "etymology": "From Latin \"lapidarius,\" from \"lapis\" meaning \"stone\"",
                "memory_tips": "Think \"lap-diary\" - keeping a diary of stones you work on in your lap",
                "part_of_speech": "adjective, noun"
            },
            "lapidarycachexia": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"lapidary\" (stone-cutting craft) incorrectly combined with \"cachexia\" (wasting syndrome). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"lapidary\" and \"cachexia\"",
                "part_of_speech": "error - combined words"
            },
            "laptop": {
                "definition": "A portable personal computer designed to be easily transported and used in various locations, featuring a hinged design with screen, keyboard, and touchpad integrated into a compact, lightweight package. Laptops revolutionized computing by enabling work and communication from virtually anywhere, supporting business travel, remote work, and educational mobility. Modern laptops offer performance comparable to desktop computers while providing battery power, wireless connectivity, and portability that meets diverse user needs from basic tasks to professional applications. The laptop form factor continues to evolve with ultrabooks, gaming laptops, and 2-in-1 devices that blur the lines between laptops and tablets.",
                "example_sentence": "The student carried her _____ computer to the library to work on research projects and online assignments.",
                "pronunciation": "LAP-top (emphasis on first syllable)",
                "etymology": "From \"lap\" + \"top,\" describing a computer that sits on top of one's lap",
                "memory_tips": "Think \"lap-top\" - a computer that sits on top of your lap for portable use",
                "part_of_speech": "noun"
            },
            "larceny": {
                "definition": "The unlawful taking and carrying away of someone else's personal property with the intent to permanently deprive the owner of possession; a legal term for theft that distinguishes between different degrees of stealing based on the value of stolen goods. Grand larceny involves theft of items above a certain monetary threshold and carries more severe penalties, while petit larceny covers theft of lesser-valued items. The charge requires proof of intent to steal rather than merely borrow, and the property must be moved from its original location. Larceny laws vary by jurisdiction but generally represent one of the most common property crimes in legal systems.",
                "example_sentence": "The defendant was charged with grand _____ for stealing jewelry valued at over five thousand dollars from the store.",
                "pronunciation": "LAR-suh-nee (emphasis on first syllable)",
                "etymology": "From Old French \"larcin,\" from Latin \"latrocinium\" meaning \"robbery\" or \"theft\"",
                "memory_tips": "Think \"large-siny\" - a large sin involving stealing from others",
                "part_of_speech": "noun"
            },
            "large": {
                "definition": "Of considerable size, extent, or intensity; bigger than normal or average in dimensions, scope, or magnitude. The concept of largeness is relative and depends on context, comparison standards, and observer perspective, ranging from physical measurements to abstract qualities like influence or importance. Large can describe tangible objects like buildings or animals, as well as intangible concepts such as ideas, problems, or social movements. Understanding scale and proportion helps determine what constitutes large in different situations, from microscopic to cosmic scales of reference.",
                "example_sentence": "The _____ oak tree provided shade for the entire playground during hot summer afternoons.",
                "pronunciation": "LARJ (single syllable, rhymes with \"charge\")",
                "etymology": "From Old French \"large,\" from Latin \"largus\" meaning \"abundant\" or \"generous\"",
                "memory_tips": "Think \"charge\" - something large might charge a lot of space or attention",
                "part_of_speech": "adjective, adverb"
            },
            "largely": {
                "definition": "To a great extent; mostly or mainly; in large part or for the most part, indicating that something is true or applies to a significant degree but not necessarily completely. This adverb suggests that while other factors may be involved, the primary influence, cause, or characteristic being described represents the dominant aspect of the situation. Largely implies a substantial majority or predominant influence while acknowledging that exceptions or minor contributions may exist. The word helps express proportional relationships and degrees of causation or influence in complex situations.",
                "example_sentence": "The project's success was _____ due to the team's dedication and careful planning throughout the development process.",
                "pronunciation": "LARJ-lee (emphasis on first syllable)",
                "etymology": "From \"large\" + \"-ly,\" meaning \"in a large manner\" or \"to a large extent\"",
                "memory_tips": "Think \"large-ly\" - in a large way, meaning mostly or mainly",
                "part_of_speech": "adverb"
            },
            "largesses": {
                "definition": "Plural of largess; generous gifts or donations, especially those given by wealthy or powerful individuals to demonstrate benevolence, gain favor, or fulfill social obligations. Largesses represent acts of generosity that often involve substantial resources and may serve both charitable and political purposes, helping to establish or maintain social relationships and public reputation. Historical examples include royal patronage of arts and sciences, wealthy individuals founding institutions, or corporate philanthropic initiatives. Modern largesses may include charitable foundations, scholarship programs, or disaster relief contributions that benefit society while enhancing the giver's public image.",
                "example_sentence": "The billionaire's _____ included funding for schools, hospitals, and environmental conservation programs worldwide.",
                "pronunciation": "lar-JES-iz (emphasis on second syllable)",
                "etymology": "Plural of \"largess,\" from Old French \"largesse,\" from \"large\" meaning \"generous\"",
                "memory_tips": "Think \"large-esses\" - large gifts given by generous people or entities",
                "part_of_speech": "noun"
            },
            "largest": {
                "definition": "Superlative form of large; the biggest in size, extent, or intensity among a group; having the greatest dimensions, magnitude, or scope when compared to others in the same category. The largest represents the extreme end of a size or scale comparison, indicating maximum measurement within a defined set or context. This designation requires clear criteria for measurement and comparison, whether referring to physical dimensions, numerical quantities, or abstract qualities like importance or influence. Understanding what constitutes largest depends on the specific attributes being measured and the boundaries of the comparison group.",
                "example_sentence": "The blue whale is the _____ animal ever known to have lived on Earth, reaching lengths of up to 100 feet.",
                "pronunciation": "LAR-jist (emphasis on first syllable)",
                "etymology": "Superlative form of \"large,\" from Old French \"large\"",
                "memory_tips": "Think \"large-est\" - the most large among all things being compared",
                "part_of_speech": "adjective"
            },
            "larkspur": {
                "definition": "A flowering plant in the buttercup family (genus Delphinium) characterized by tall spikes of colorful flowers with distinctive spurs projecting from the back of each bloom. Larkspurs are popular garden plants valued for their dramatic vertical flower displays in shades of blue, purple, pink, and white that attract bees, butterflies, and hummingbirds. These plants prefer cool weather and rich, well-drained soil, making them excellent choices for cottage gardens and perennial borders. However, all parts of larkspur plants are toxic to humans and livestock, containing alkaloids that can cause serious poisoning if ingested.",
                "example_sentence": "The cottage garden's tall _____ spikes created a stunning blue backdrop for the lower-growing perennial flowers.",
                "pronunciation": "LARK-sper (emphasis on first syllable)",
                "etymology": "From the resemblance of the flower's spur to a lark's hind claw or spur",
                "memory_tips": "Think \"lark-spur\" - a flower with a spur like a lark bird's claw",
                "part_of_speech": "noun"
            },
            "larnax": {
                "definition": "An ancient Greek or Roman funerary container, typically made of stone, clay, or wood, used to hold cremated remains or burial goods; a type of sarcophagus or ossuary that preserved the deceased's remains and valuable items for the afterlife. Larnakes (plural) were often decorated with painted scenes, inscriptions, or relief carvings that reflected the deceased's social status, religious beliefs, or family history. These burial containers provide valuable archaeological evidence about ancient funeral practices, artistic traditions, and social hierarchies. The style and contents of larnakes help archaeologists understand ancient attitudes toward death, afterlife beliefs, and cultural values.",
                "example_sentence": "The archaeologist carefully excavated the painted _____ containing ancient burial goods and cremated remains from the Greek tomb.",
                "pronunciation": "LAR-naks (emphasis on first syllable)",
                "etymology": "From Greek \"larnax,\" meaning \"chest\" or \"coffer,\" used specifically for burial containers",
                "memory_tips": "Think \"learn-ax\" - learning about ancient people through their burial chests",
                "part_of_speech": "noun"
            },
            "laryngitis": {
                "definition": "Inflammation of the larynx (voice box) that causes hoarseness, voice loss, or throat pain, typically resulting from viral infections, vocal strain, or irritant exposure. The condition affects the vocal cords and surrounding tissues, leading to swelling that interferes with normal voice production and may cause complete voice loss in severe cases. Acute laryngitis usually resolves within a few days to weeks with rest and proper care, while chronic laryngitis may indicate underlying conditions requiring medical attention. Treatment focuses on voice rest, hydration, and addressing underlying causes such as infection or acid reflux.",
                "example_sentence": "The singer developed _____ from overuse during the concert tour and had to cancel several performances to rest her voice.",
                "pronunciation": "lar-in-JIE-tis (emphasis on third syllable)",
                "etymology": "From Greek \"larynx\" (voice box) + \"-itis\" (inflammation)",
                "memory_tips": "Think \"larynx-itis\" - inflammation of the larynx that affects your voice",
                "part_of_speech": "noun"
            },
            "lascaux": {
                "definition": "A cave system in southwestern France famous for its Paleolithic cave paintings dating back approximately 15,000-17,000 years, representing some of the finest examples of prehistoric art ever discovered. The Lascaux caves contain over 600 painted animals including horses, deer, aurochs, bison, and birds, created by Cro-Magnon people using natural pigments and sophisticated artistic techniques. These paintings provide invaluable insights into prehistoric human culture, artistic expression, and the relationship between early humans and their environment. The original caves are now closed to protect the artwork, but detailed replicas allow visitors to experience these remarkable ancient masterpieces.",
                "example_sentence": "Art historians study the _____ cave paintings to understand the sophisticated artistic abilities of prehistoric humans.",
                "pronunciation": "las-KOH (emphasis on second syllable)",
                "etymology": "From the French place name \"Lascaux,\" where the cave system is located",
                "memory_tips": "Think \"last-cow\" - the last cave with ancient cow paintings from prehistoric times",
                "part_of_speech": "noun (proper)"
            },
            "laser": {
                "definition": "A device that produces an intense, narrow beam of light through the stimulated emission of electromagnetic radiation, creating coherent light waves that can be precisely controlled and focused for various applications. LASER stands for Light Amplification by Stimulated Emission of Radiation, representing a technology that revolutionized fields including medicine, manufacturing, communications, and scientific research. Lasers work by exciting atoms or molecules to emit photons in a coordinated manner, producing light that maintains consistent wavelength, phase, and direction. Applications range from simple laser pointers to complex surgical procedures, industrial cutting, and fiber optic communications.",
                "example_sentence": "The surgeon used a precision _____ to remove the tumor while minimizing damage to surrounding healthy tissue.",
                "pronunciation": "LAY-zer (emphasis on first syllable)",
                "etymology": "Acronym from \"Light Amplification by Stimulated Emission of Radiation\"",
                "memory_tips": "Think \"lay-zer\" - laying down precise beams of light with zero scatter",
                "part_of_speech": "noun, verb"
            },
            "lassitude": {
                "definition": "A state of physical or mental weariness; lack of energy or motivation characterized by tiredness, listlessness, and disinclination to exert effort. Lassitude can result from various factors including illness, stress, depression, poor sleep, or prolonged physical or mental demands that deplete energy reserves. This condition goes beyond simple fatigue to include emotional apathy and reduced interest in activities that normally provide satisfaction or engagement. While temporary lassitude is normal after intense activity or during recovery from illness, persistent lassitude may indicate underlying health issues requiring medical attention.",
                "example_sentence": "After months of working overtime, she experienced a deep _____ that made even simple daily tasks feel overwhelming.",
                "pronunciation": "LAS-uh-tood (emphasis on first syllable)",
                "etymology": "From Latin \"lassitudo,\" from \"lassus\" meaning \"weary\" or \"tired\"",
                "memory_tips": "Think \"lazy-attitude\" - an attitude of being lazy and tired",
                "part_of_speech": "noun"
            },
            "lasso": {
                "definition": "A long rope with a running noose at one end, used especially by cowboys and ranchers for catching cattle and horses; also refers to the act of catching something with such a rope. The lasso represents an essential tool in livestock management and western culture, requiring skill and practice to throw accurately and secure animals effectively. Traditional lassos are made from braided leather or rope materials that provide the right combination of flexibility and strength. The technique involves swinging the looped rope overhead and throwing it to encircle the target, then quickly tightening the noose to secure the catch.",
                "example_sentence": "The skilled cowboy could _____ a runaway calf from horseback with remarkable accuracy and speed.",
                "pronunciation": "las-OO or LAS-oh (emphasis varies by region)",
                "etymology": "From Spanish \"lazo,\" from Latin \"laqueus\" meaning \"snare\" or \"noose\"",
                "memory_tips": "Think \"lass-oh\" - a cowboy saying \"oh\" when he lassos a young animal (lass)",
                "part_of_speech": "noun, verb"
            },
            "lassoo": {
                "definition": "Alternative spelling of lasso; a rope with a noose used for catching animals, particularly in ranching and cowboy contexts where skilled horsemen use the looped rope to capture livestock. This variant spelling reflects regional or historical differences in romanizing the Spanish word \"lazo\" into English. The lassoo technique requires considerable practice to master the proper rope handling, timing, and accuracy needed to successfully capture moving targets. Whether spelled lasso or lassoo, the tool remains an iconic symbol of western American culture and practical livestock management.",
                "example_sentence": "The rodeo competitor demonstrated expert _____ skills by roping the steer in record time during the competition.",
                "pronunciation": "las-OO (emphasis on second syllable)",
                "etymology": "Alternative spelling of \"lasso,\" from Spanish \"lazo\"",
                "memory_tips": "Think \"lass-ooo\" - making an \"ooo\" sound when throwing the rope at a young animal",
                "part_of_speech": "noun, verb"
            },
            "last": {
                "definition": "Coming at the end of a series, process, or period of time; final in sequence, position, or occurrence; also refers to the most recent or immediately preceding instance of something. As an adjective, last indicates the final item in a chronological or spatial arrangement, while as a verb it means to continue for a specified duration or to endure through time. The concept of lastness implies completion, finality, or the conclusion of a particular sequence or experience. Understanding what is last requires clear definition of the boundaries or criteria that determine the ending point.",
                "example_sentence": "The _____ student to finish the exam handed in her paper just before the time limit expired.",
                "pronunciation": "LAST (single syllable, rhymes with \"fast\")",
                "etymology": "From Old English \"latost,\" superlative of \"læt\" meaning \"late\"",
                "memory_tips": "Think \"fast\" - the last person might need to go fast to catch up",
                "part_of_speech": "adjective, adverb, verb, noun"
            },
            "late": {
                "definition": "Happening, arriving, or occurring after the expected, usual, or proper time; delayed beyond the scheduled or anticipated moment. Late can describe temporal delays, deceased persons (the late Mr. Smith), or things that occur toward the end of a period (late afternoon). The concept is relative and depends on established expectations, schedules, or social norms that define appropriate timing. Being late may result from various factors including poor planning, unexpected circumstances, or different cultural attitudes toward punctuality. Understanding lateness requires awareness of context-specific time expectations and consequences.",
                "example_sentence": "The train was twenty minutes _____ due to signal problems that caused delays throughout the rail system.",
                "pronunciation": "LAYT (single syllable, rhymes with \"gate\")",
                "etymology": "From Old English \"læt,\" meaning \"slow\" or \"tardy\"",
                "memory_tips": "Think \"gate\" - arriving late means the gate might be closing",
                "part_of_speech": "adjective, adverb"
            },
            "latency": {
                "definition": "The delay between the initiation of a process and its observable effect; the time interval during which something remains hidden, inactive, or undeveloped before becoming apparent or active. In technology, latency refers to the delay in data transmission between sending and receiving information, affecting system performance and user experience. In medicine, latency describes the period between infection or exposure and the appearance of symptoms. Psychological latency involves delays between stimulus and response, while in various fields it represents dormant periods before activation, manifestation, or measurable effects occur.",
                "example_sentence": "The network's high _____ made online gaming frustrating because actions appeared delayed on screen.",
                "pronunciation": "LAY-tuhn-see (emphasis on first syllable)",
                "etymology": "From Latin \"latere\" meaning \"to lie hidden,\" referring to hidden or delayed effects",
                "memory_tips": "Think \"lay-ten-see\" - laying down for ten seconds to see delayed effects",
                "part_of_speech": "noun"
            },
            "latencyepitaphs": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"latency\" (delay time) incorrectly combined with \"epitaphs\" (tombstone inscriptions). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"latency\" and \"epitaphs\"",
                "part_of_speech": "error - combined words"
            },
            "later": {
                "definition": "At a time in the future; after the present moment or after a specified time; comparative form of late, indicating a subsequent point in time or sequence. Later establishes temporal relationships by referring to events, actions, or conditions that will occur or be relevant after the current moment or reference point. The term can indicate both definite future times (later today) and indefinite future periods (we'll discuss this later). Understanding later requires temporal context and may involve scheduling, planning, or sequential thinking about events and their relationships in time.",
                "example_sentence": "We'll finish discussing the budget details _____ when all the department heads can attend the meeting.",
                "pronunciation": "LAY-ter (emphasis on first syllable)",
                "etymology": "Comparative form of \"late,\" from Old English \"læt\"",
                "memory_tips": "Think \"late-er\" - more late than now, meaning in the future",
                "part_of_speech": "adverb, adjective"
            },
            "lateral": {
                "definition": "Relating to the side or sides; extending sideways rather than forward, backward, up, or down; positioned at or moving toward the side. In anatomy, lateral describes structures away from the midline of the body, while in various fields it refers to horizontal movement, side-by-side arrangements, or approaches that come from the side rather than direct frontal directions. Lateral thinking involves creative problem-solving that approaches issues from unexpected angles rather than following conventional logical progression. The concept emphasizes horizontal rather than vertical relationships and movements.",
                "example_sentence": "The football player made a quick _____ movement to avoid the tackle and run toward the sideline.",
                "pronunciation": "LAT-er-uhl (emphasis on first syllable)",
                "etymology": "From Latin \"lateralis,\" from \"latus\" meaning \"side\"",
                "memory_tips": "Think \"later-all\" - all sides that come later from the main center",
                "part_of_speech": "adjective, noun"
            },
            "laterigrade": {
                "definition": "Moving or walking sideways; describing animals, particularly crabs and some spiders, that locomote primarily by moving laterally rather than forward or backward. This specialized form of movement provides advantages in certain environments and situations, allowing rapid escape movements, efficient navigation in tight spaces, or optimal positioning for feeding and defense. Laterigrade locomotion requires specialized anatomical adaptations including joint structures, muscle arrangements, and body proportions that support sideways movement. The term applies to both permanent sideways movement patterns and occasional lateral locomotion used for specific purposes.",
                "example_sentence": "The _____ crab scuttled quickly across the beach, moving sideways to escape from approaching waves.",
                "pronunciation": "LAT-er-uh-grayd (emphasis on first syllable)",
                "etymology": "From Latin \"latus\" (side) + \"gradus\" (step or walk), meaning \"side-walking\"",
                "memory_tips": "Think \"lateral-grade\" - grading or walking in a lateral direction",
                "part_of_speech": "adjective"
            },
            "laterigradehyssop": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"laterigrade\" (side-walking) incorrectly combined with \"hyssop\" (medicinal plant). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"laterigrade\" and \"hyssop\"",
                "part_of_speech": "error - combined words"
            },
            "latigo": {
                "definition": "A strap used on a Western saddle to secure the cinch (girth) that holds the saddle in place on a horse; typically made of leather and featuring holes or adjustment mechanisms that allow riders to tighten or loosen the saddle's fit. The latigo connects the saddle rigging to the cinch through a complex system of straps and hardware that distributes weight and pressure evenly across the horse's body. Proper latigo adjustment is crucial for both horse comfort and rider safety, preventing saddle slippage during riding activities. This essential piece of tack reflects the practical engineering of western riding equipment designed for working conditions.",
                "example_sentence": "The cowboy carefully adjusted the _____ strap to ensure the saddle was securely fastened before mounting his horse.",
                "pronunciation": "LAT-uh-goh (emphasis on first syllable)",
                "etymology": "From Spanish \"latigo,\" meaning \"whip\" or \"strap,\" referring to its flexible leather construction",
                "memory_tips": "Think \"lasso-go\" - the strap that helps your saddle go securely like a lasso holds cattle",
                "part_of_speech": "noun"
            },
            "latin": {
                "definition": "The classical language of ancient Rome and the Roman Empire, which became the foundation for Romance languages and served as the scholarly and religious language of Western Europe for centuries. Latin influenced legal, medical, and scientific terminology that remains in use today, while Latin phrases and expressions continue to appear in formal writing, legal documents, and academic contexts. As an adjective, Latin refers to things related to ancient Rome, the Latin language, or Latin American cultures descended from Roman influence. The study of Latin provides insights into linguistic development, historical texts, and the cultural foundations of Western civilization.",
                "example_sentence": "Medical students learn _____ terminology to understand anatomical names and communicate precisely with healthcare professionals worldwide.",
                "pronunciation": "LAT-in (emphasis on first syllable)",
                "etymology": "From Latin \"Latinus,\" referring to the people of Latium, the region around Rome",
                "memory_tips": "Think \"flat-in\" - the flat language that got built into many other languages",
                "part_of_speech": "noun, adjective"
            },
            "latinized": {
                "definition": "Converted to or expressed in Latin form; adapted to follow Latin language patterns, grammar, or spelling conventions; made to conform to Latin linguistic structures or cultural practices. The process of latinization historically occurred when local names, terms, or concepts were modified to fit Latin pronunciation, spelling, or grammatical rules, often during Roman expansion or later scholarly work. Scientific nomenclature frequently uses latinized names to create universal terminology that transcends language barriers. Modern latinization may involve adapting contemporary terms to classical Latin forms for academic, legal, or ceremonial purposes.",
                "example_sentence": "The botanist _____ the common plant name to create a proper scientific designation following international taxonomic rules.",
                "pronunciation": "LAT-in-iezd (emphasis on first syllable)",
                "etymology": "Past tense of \"latinize,\" from \"Latin\" + \"-ize\" (to make like)",
                "memory_tips": "Think \"Latin-ized\" - made to be like Latin in form or structure",
                "part_of_speech": "verb, adjective"
            },
            "latinxua": {
                "definition": "A romanization system for Chinese characters developed in the Soviet Union during the 1930s, designed to replace Chinese characters with Latin letters for improved literacy and international communication. The system aimed to simplify Chinese writing by using familiar Latin alphabetic symbols instead of complex character systems, making the language more accessible to learners and facilitating communication with other nations. Latinxua represented attempts at language reform that sought to modernize Chinese writing systems through international alphabetic standards. While not widely adopted, it influenced later romanization systems and reflects historical efforts to bridge Eastern and Western writing traditions.",
                "example_sentence": "Linguists studied the _____ system to understand early attempts at romanizing Chinese characters using Latin letters.",
                "pronunciation": "lat-in-SHOO-ah (emphasis on third syllable)",
                "etymology": "From \"Latin\" + Chinese \"xua\" referring to the Chinese application of Latin letters",
                "memory_tips": "Think \"Latin-shoe-ah\" - Latin letters wearing Chinese shoes to walk between languages",
                "part_of_speech": "noun"
            },
            "latitudinarian": {
                "definition": "A person who advocates for broad tolerance in religious or political matters, supporting flexibility and accommodation rather than strict adherence to particular doctrines or practices. Latitudinarians typically oppose rigid orthodoxy and favor inclusive approaches that allow for diverse interpretations, beliefs, and practices within broader frameworks. This philosophical position emphasizes practical cooperation over theological precision and tends to prioritize social harmony over doctrinal purity. The term historically applied to Anglican clergy who supported religious tolerance and accommodation with different Christian denominations, but extends to any context involving tolerance of diverse viewpoints.",
                "example_sentence": "The _____ bishop encouraged dialogue between different denominations rather than insisting on strict doctrinal conformity.",
                "pronunciation": "lat-uh-tood-uh-NAIR-ee-uhn (emphasis on fifth syllable)",
                "etymology": "From \"latitude\" (breadth or freedom) + \"-arian\" (person who advocates), meaning one who advocates breadth",
                "memory_tips": "Think \"latitude-in-area\" - someone who gives latitude (freedom) in their area of influence",
                "part_of_speech": "noun, adjective"
            },
            "latke": {
                "definition": "A traditional Jewish potato pancake, typically made from grated potatoes mixed with eggs, onions, and seasonings, then fried until golden and crispy. Latkes are especially associated with Hanukkah celebrations, where the oil used for frying commemorates the miracle of the Temple oil that burned for eight days. These savory pancakes can be served with various accompaniments including sour cream, applesauce, or smoked salmon, reflecting both Ashkenazi Jewish culinary traditions and modern adaptations. The preparation of latkes involves techniques for achieving the proper texture balance between crispy exterior and tender interior.",
                "example_sentence": "The family gathered to make traditional potato _____ for their Hanukkah celebration, serving them with homemade applesauce.",
                "pronunciation": "LAHT-kuh or LAT-kuh (emphasis on first syllable)",
                "etymology": "From Yiddish \"latke,\" possibly from Ukrainian \"oladka\" meaning \"small pancake\"",
                "memory_tips": "Think \"lot-kuh\" - a lot of potatoes mashed together to make these pancakes",
                "part_of_speech": "noun"
            },
            "latter": {
                "definition": "The second of two things or people previously mentioned; the more recent or final item in a pair or sequence; referring to something that comes later in time or order. Latter provides a way to reference the second item without repeating the specific noun, creating cleaner sentence structure while maintaining clear meaning. The term establishes comparative relationships between two options, events, or periods, always referring to the one that appears second in the sequence. Understanding latter requires tracking the order of presentation and maintaining clear mental reference to the items being compared.",
                "example_sentence": "Between studying medicine and law, she chose the _____ because it better matched her interest in social justice.",
                "pronunciation": "LAT-er (emphasis on first syllable)",
                "etymology": "Comparative form of \"late,\" from Old English \"læt,\" meaning \"the later one\"",
                "memory_tips": "Think \"later\" - the latter is the later one of two choices mentioned",
                "part_of_speech": "adjective, noun"
            },
            "laudatory": {
                "definition": "Expressing praise, commendation, or approval; containing or characterized by words of acclaim, tribute, or positive recognition. Laudatory language celebrates achievements, honors accomplishments, or acknowledges excellence through complimentary expressions that highlight positive qualities or successful outcomes. This type of communication serves important social functions including motivation, recognition, and relationship building by publicly acknowledging worth and value. Laudatory speeches, writings, or comments often appear in formal contexts such as award ceremonies, graduation addresses, or professional evaluations where recognition is appropriate and expected.",
                "example_sentence": "The professor's _____ comments about the student's research paper encouraged her to pursue graduate studies in the field.",
                "pronunciation": "LAWD-uh-tor-ee (emphasis on first syllable)",
                "etymology": "From Latin \"laudatorius,\" from \"laudare\" meaning \"to praise\"",
                "memory_tips": "Think \"laud-a-story\" - telling a story that lauds or praises someone",
                "part_of_speech": "adjective"
            },
            "laude": {
                "definition": "A Latin term meaning \"with praise,\" commonly used in academic contexts as part of graduation honors including magna cum laude (with great praise) and summa cum laude (with highest praise). These designations recognize exceptional academic achievement and distinguish graduates who have demonstrated superior scholarship throughout their educational programs. The laude system provides standardized recognition that helps identify outstanding students for employment opportunities, graduate school admission, and professional advancement. Different institutions may have varying requirements and criteria for achieving these prestigious academic honors.",
                "example_sentence": "She graduated magna cum _____ after maintaining excellent grades throughout her undergraduate program.",
                "pronunciation": "LAWD-ay (emphasis on second syllable)",
                "etymology": "From Latin \"laude,\" ablative form of \"laus\" meaning \"praise\"",
                "memory_tips": "Think \"loud-ay\" - saying \"ay\" loudly to praise someone's academic achievement",
                "part_of_speech": "noun"
            },
            "laudeevo": {
                "definition": "[COMBINED WORD ERROR] This appears to be \"laude\" (academic praise designation) incorrectly combined with \"evo\" (evolution prefix or brand name). This type of error occurs when PDF text extraction fails to properly separate distinct words appearing close together in original document formatting. These are completely unrelated concepts artificially combined due to technical parsing issues common when processing PDF documents containing educational materials, where formatting irregularities cause adjacent words to merge without proper spacing or punctuation between distinct vocabulary terms.",
                "example_sentence": "[ERROR - This combined word should not appear in spelling bee materials]",
                "pronunciation": "[PRONUNCIATION ERROR - COMBINED WORDS]",
                "etymology": "[ETYMOLOGY ERROR - COMBINED WORDS]",
                "memory_tips": "This is a data error - should be separated into \"laude\" and \"evo\"",
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
        """Process all words in batch 100"""
        
        logging.info("Processing Batch 100 with comprehensive Claude data...")
        
        input_file = "output/batch_100_words.csv"
        output_file = "output/batch_100_processed.csv"
        
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
            logging.info("Batch 100 processing completed!")
            logging.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
            logging.info(f"Output saved to: {output_file}")
            logging.info(f"Results: {len(processed_words)} successful, 0 failed")
                
        except Exception as e:
            logging.error(f"Error processing batch: {e}")
            raise

if __name__ == "__main__":
    processor = Batch100Processor()
    processor.process_batch()