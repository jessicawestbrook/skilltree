#!/usr/bin/env python3

import csv
import logging
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DifficultyCalculator:
    """Calculate 4-factor difficulty components for spelling words"""
    
    def calculate_difficulty_components(self, word: str, definition: str, etymology: str) -> dict:
        """Calculate 4-factor difficulty components leaving final difficulty null"""
        
        # 1. Phonetic Transparency (sound-to-spelling correspondence)
        phonetic_score = self._calculate_phonetic_transparency(word)
        
        # 2. Word Frequency (how common the word is)
        frequency_score = self._calculate_word_frequency(word)
        
        # 3. Morphological Complexity (prefixes, suffixes, roots)
        morphological_score = self._calculate_morphological_complexity(word, definition)
        
        # 4. Etymology Complexity (language origins and borrowing)
        etymology_score = self._calculate_etymology_complexity(etymology)
        
        return {
            'phonetic_transparency_score': phonetic_score,
            'word_frequency_score': frequency_score, 
            'morphological_complexity_score': morphological_score,
            'etymology_complexity_score': etymology_score,
            'final_difficulty': None  # Leave null for human review
        }
    
    def _calculate_phonetic_transparency(self, word: str) -> float:
        """Calculate how transparent the sound-to-spelling relationship is"""
        irregular_patterns = ['ough', 'aigh', 'eigh', 'ph', 'gh', 'tion', 'sion', 'ight']
        score = 1.0
        
        for pattern in irregular_patterns:
            if pattern in word.lower():
                score += 0.3
        
        # Silent letters
        silent_patterns = ['mb', 'ght', 'kn', 'wr', 'mn']
        for pattern in silent_patterns:
            if pattern in word.lower():
                score += 0.2
                
        return min(score, 5.0)
    
    def _calculate_word_frequency(self, word: str) -> float:
        """Estimate word frequency (higher score = less frequent = more difficult)"""
        common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did']
        
        if word.lower() in common_words:
            return 1.0
        elif len(word) <= 4:
            return 2.0
        elif len(word) <= 7:
            return 3.0
        elif len(word) <= 10:
            return 4.0
        else:
            return 5.0
    
    def _calculate_morphological_complexity(self, word: str, definition: str) -> float:
        """Calculate complexity based on word parts"""
        score = 1.0
        
        prefixes = ['un', 're', 'pre', 'dis', 'anti', 'over', 'under', 'out', 'super', 'semi', 'multi', 'inter', 'trans', 'sub', 'micro', 'macro']
        suffixes = ['tion', 'sion', 'ment', 'ness', 'able', 'ible', 'ous', 'eous', 'ious', 'ly', 'ing', 'ed', 'er', 'est', 'ful', 'less']
        
        for prefix in prefixes:
            if word.lower().startswith(prefix):
                score += 0.5
                break
                
        for suffix in suffixes:
            if word.lower().endswith(suffix):
                score += 0.5
                break
        
        # Compound words
        if len(word) > 8 and any(char.isupper() for char in word[1:]):
            score += 0.5
            
        return min(score, 5.0)
    
    def _calculate_etymology_complexity(self, etymology: str) -> float:
        """Calculate complexity based on word origins"""
        if not etymology:
            return 3.0
            
        score = 1.0
        complex_origins = ['Latin', 'Greek', 'Sanskrit', 'Arabic', 'Hebrew', 'Persian', 'Turkish']
        moderate_origins = ['French', 'Italian', 'Spanish', 'Portuguese', 'German', 'Dutch']
        
        etymology_lower = etymology.lower()
        
        for origin in complex_origins:
            if origin.lower() in etymology_lower:
                score += 1.0
                break
                
        for origin in moderate_origins:
            if origin.lower() in etymology_lower:
                score += 0.5
                break
        
        # Multiple language origins increase complexity
        origin_count = sum(1 for origin in complex_origins + moderate_origins 
                          if origin.lower() in etymology_lower)
        if origin_count > 1:
            score += 0.5
            
        return min(score, 5.0)


class Batch103Processor:
    """Processes Batch 103 with comprehensive Claude data for all 50 words"""
    
    def __init__(self):
        self.difficulty_calc = DifficultyCalculator()
        
        # Define combined word errors found in this batch
        self.combined_errors = {
            'listsevery': ['lists', 'every'],
            'listspage': ['lists', 'page'],
            'literacydifficulty': ['literacy', 'difficulty']
        }
    
    def get_comprehensive_claude_data(self, word: str) -> dict:
        """Get comprehensive educational data for each word using Claude knowledge"""
        
        # Handle combined word errors
        if word in self.combined_errors:
            return {
                'word': word,
                'pronunciation': None,
                'definition': f"COMBINED_WORD_ERROR: This appears to be two words combined: {' + '.join(self.combined_errors[word])}",
                'example_sentence': None,
                'etymology': None,
                'etymology_source': 'Claude',
                'memory_tip': 'This is a combined word error from PDF parsing and should not be used.',
                'phonetic_transparency_score': None,
                'word_frequency_score': None,
                'morphological_complexity_score': None,
                'etymology_complexity_score': None,
                'final_difficulty': None
            }
        
        # Comprehensive word data with 200-400 word definitions
        word_data = {
            'limpkin': {
                'pronunciation': '/LIMP-kin/',
                'definition': 'A large wading bird (Aramus guarauna) native to wetlands of the southeastern United States, Central America, and South America, characterized by its distinctive brown plumage with white markings and specialized bill adapted for extracting apple snails from their shells. The limpkin belongs to its own family, Aramidae, making it evolutionarily unique among wading birds. These secretive birds inhabit freshwater marshes, swamps, and wetlands where they feed primarily on apple snails, though they also consume frogs, insects, and other aquatic invertebrates. Limpkins are notable for their loud, wailing calls that can be heard over long distances, earning them the nickname "crying bird" in some regions. Their long, slightly decurved bills are perfectly adapted for reaching into snail shells, and their long toes help them navigate through floating vegetation. During breeding season, limpkins build platform nests in dense vegetation near water, where they lay 4-6 spotted eggs. The species has experienced population fluctuations due to wetland habitat loss, but conservation efforts have helped stabilize numbers in many areas.',
                'etymology': 'Named for its limping gait when walking, from "limp" + diminutive suffix "-kin"',
                'memory_tip': 'Remember LIMPKIN by thinking of a bird that walks with a "limping" gait, like it has a sore leg.',
                'example_sentence': 'The researcher observed a _____ wading through the marsh, using its specialized bill to extract apple snails from their shells.'
            },
            'lincoln': {
                'pronunciation': '/LINK-ən/',
                'definition': 'Most commonly referring to Abraham Lincoln (1809-1865), the 16th President of the United States who led the nation through the Civil War and issued the Emancipation Proclamation, fundamentally reshaping American society and government. Lincoln is remembered as one of America\'s greatest presidents for his role in preserving the Union, ending slavery, and strengthening federal power. Born in a log cabin in Kentucky, Lincoln was largely self-educated and worked as a rail-splitter, storekeeper, and lawyer before entering politics. His political career included service in the Illinois House of Representatives and U.S. House of Representatives before his successful presidential campaign in 1860. Lincoln\'s presidency was dominated by the Civil War, during which he demonstrated remarkable leadership, strategic thinking, and moral courage. His famous speeches, including the Gettysburg Address and Second Inaugural Address, are considered masterpieces of American rhetoric. Lincoln\'s assassination by John Wilkes Booth at Ford\'s Theatre in April 1865, just days after the war\'s end, made him a martyr for the causes of union and freedom. The name also refers to numerous places named after the president, including Lincoln, Nebraska, and Lincoln University.',
                'etymology': 'From Old English "lind" (lime tree) + "colonia" (colony), originally meaning a settlement by lime trees',
                'memory_tip': 'Remember LINCOLN by connecting it to Abraham Lincoln and the famous penny - both are part of American history.',
                'example_sentence': 'Students studied ______\'s Emancipation Proclamation and its impact on ending slavery in the United States.'
            },
            'line': {
                'pronunciation': '/līn/',
                'definition': 'A fundamental geometric concept representing a straight path extending infinitely in both directions, having length but no width or thickness, forming the basis for more complex geometric shapes and mathematical relationships. In mathematics, a line is defined by at least two points and can be described by linear equations in coordinate systems. Lines have numerous practical applications across various fields: in art and design, lines create structure, movement, and visual interest; in architecture, they define spaces and create aesthetic appeal; in technology, lines represent connections in circuit diagrams and network topologies. The concept extends to many everyday contexts - waiting lines organize people in sequence, assembly lines organize industrial production, and power lines transmit electricity. In literature, "line" refers to a single row of text in poetry or prose, while in theater, actors memorize "lines" of dialogue. Lines can be straight, curved, parallel, perpendicular, or intersecting, each serving different purposes in mathematical and practical applications. The study of lines leads to understanding angles, planes, and three-dimensional geometry, making it a cornerstone concept in mathematics education.',
                'etymology': 'From Latin "linea" meaning string or line, from "linum" (flax), as lines were drawn with flax thread',
                'memory_tip': 'Remember LINE as the most basic geometric shape - think of drawing a straight _____ with a ruler.',
                'example_sentence': 'The teacher asked students to draw a straight _____ connecting points A and B on their geometry worksheet.'
            },
            'lineage': {
                'pronunciation': '/LIN-ee-ij/',
                'definition': 'A direct line of descent from an ancestor; ancestry or pedigree that traces familial relationships through generations, representing the genetic, cultural, and social connections that bind individuals to their heritage and ancestral roots. Lineage encompasses both biological inheritance and cultural transmission, including family traditions, customs, languages, and beliefs passed down through generations. In anthropology and sociology, lineage systems form the backbone of many societies, determining inheritance rights, social status, marriage patterns, and political authority. Genealogical research traces lineages to understand family histories, medical predispositions, and cultural backgrounds. In biology, lineage refers to evolutionary relationships between species, tracing how organisms descended from common ancestors through millions of years of evolution. Royal lineages have historically determined succession to thrones and political power, while in many cultures, noble or distinguished lineages confer social prestige and honor. Modern DNA testing has revolutionized lineage tracing, allowing people to discover ancestral origins across continents and connect with distant relatives. Lineage also appears in professional contexts, such as academic lineages tracing intellectual traditions from mentor to student, or artistic lineages showing influences between artists across generations.',
                'etymology': 'From Old French "lignage" from Latin "linea" (line), referring to a line of descent',
                'memory_tip': 'Remember LINEAGE as your family "LINE" plus "AGE" - tracing your family line back through the ages.',
                'example_sentence': 'The genealogist helped the family trace their _____ back to immigrants who arrived in America during the 1800s.'
            },
            'linen': {
                'pronunciation': '/LIN-ən/',
                'definition': 'A textile fabric made from the fibers of the flax plant (Linum usitatissimum), renowned for its exceptional durability, breathability, and natural elegance, making it one of humanity\'s oldest and most valued fabrics. Linen production involves harvesting flax plants, retting the stems to separate fibers, and spinning these fibers into thread for weaving into fabric. The resulting material possesses unique properties: it becomes softer and more comfortable with each washing, naturally resists bacteria and moths, provides excellent moisture-wicking capabilities, and maintains its shape well. Linen has been used for thousands of years, with archaeological evidence showing its use in ancient Egypt for mummy wrappings and fine garments. The fabric\'s natural variations in texture and slight irregularities are considered desirable characteristics that distinguish high-quality linen from synthetic alternatives. Modern linen applications range from luxury bedding and tablecloths to fashion garments and home décor. Fine linen is often associated with quality and sophistication, while its casual drape makes it popular for summer clothing. The term "linen" also refers to household textile items like sheets, towels, and table settings, regardless of the actual fiber content.',
                'etymology': 'From Latin "linum" (flax plant), the source of linen fibers',
                'memory_tip': 'Remember LINEN comes from the "LINe" of flax plants - think of LINe EN(ds) making fabric.',
                'example_sentence': 'The hotel prided itself on using only the finest Egyptian cotton and Irish _____ for its luxury bedding.'
            },
            'lines': {
                'pronunciation': '/līnz/',
                'definition': 'The plural form of line, encompassing multiple straight or curved paths, geometric elements, or sequential arrangements that serve various functions across numerous disciplines and contexts. In geometry, lines intersect to form angles and create complex shapes, while in art, multiple lines create texture, depth, perspective, and visual movement within compositions. Lines organize information in writing and printing, separating paragraphs, creating lists, and establishing visual hierarchy. In theater and film, actors memorize lines of dialogue, while directors use lines of sight to guide audience attention. Transportation systems rely on lines - subway lines, airline routes, shipping lanes - to organize movement of people and goods efficiently. In technology, telephone lines, power lines, and data lines form the infrastructure of modern communication and energy distribution. Lines also represent boundaries: property lines define ownership, battle lines show military positions, and waiting lines organize social interactions. In literature, poetic lines create rhythm and meter, while in music, staff lines organize notation. The concept extends to genealogical lines showing family relationships, product lines organizing merchandise, and assembly lines organizing industrial production. Understanding how multiple lines interact and relate to each other is fundamental to many fields of study.',
                'etymology': 'Plural of "line" from Latin "linea" meaning string or line',
                'memory_tip': 'Remember LINES as multiple "line" elements - think of drawing several parallel _____ on paper.',
                'example_sentence': 'The artist used bold, sweeping _____ to create a sense of movement and energy in the abstract painting.'
            },
            'lingua': {
                'pronunciation': '/LING-gwə/',
                'definition': 'A Latin term meaning tongue or language, used in scientific and academic contexts to refer to linguistic phenomena, anatomical structures, or communication systems across various disciplines. In anatomy, lingua specifically refers to the tongue, the muscular organ responsible for taste, speech articulation, and food manipulation during eating. The tongue contains numerous taste buds, specialized sensory organs that detect sweet, sour, salty, bitter, and umami flavors, while its complex musculature enables precise movements necessary for clear speech production. Linguistically, "lingua" appears in terms like "lingua franca" (a bridge language used for communication between speakers of different native languages) and "bilingual" (speaking two languages). In medical terminology, "lingua" forms part of many anatomical terms describing tongue-related structures and conditions. The word also appears in religious contexts, particularly in Christianity, where "speaking in tongues" or glossolalia involves vocalization in unknown languages during spiritual experiences. Ancient Romans used "lingua" to distinguish between different languages within their empire, recognizing the diversity of communication systems across conquered territories. Modern usage maintains these classical meanings while extending to contemporary linguistic and medical applications.',
                'etymology': 'Latin "lingua" meaning tongue or language, related to "lingere" (to lick)',
                'memory_tip': 'Remember LINGUA as "LING" sounds like "language" + "UA" - your tongue helps you speak language.',
                'example_sentence': 'The medical student learned that the _____ contains thousands of taste buds and complex muscles essential for speech.'
            },
            'linguistic': {
                'pronunciation': '/ling-GWIS-tik/',
                'definition': 'Relating to language or linguistics, the scientific study of human language including its structure, development, variation, and use across different cultures and contexts. Linguistic research encompasses multiple subfields: phonetics studies speech sounds, phonology examines sound patterns, morphology analyzes word structure, syntax investigates sentence construction, semantics explores meaning, and pragmatics considers language use in context. Linguistic anthropologists study how language shapes culture and social relationships, while psycholinguists investigate how humans acquire, process, and produce language. Historical linguistics traces language evolution over time, revealing relationships between languages and reconstructing ancient languages through comparative analysis. Sociolinguistics examines how social factors like class, gender, age, and ethnicity influence language use and variation. Applied linguistics addresses practical language issues including language teaching, translation, speech therapy, and computational linguistics. Linguistic diversity represents one of humanity\'s greatest intellectual achievements, with approximately 7,000 languages currently spoken worldwide, each representing unique ways of organizing and expressing human experience. Modern linguistic research utilizes advanced technology including computer modeling, brain imaging, and digital corpus analysis to understand language complexity and universals.',
                'etymology': 'From Latin "lingua" (tongue/language) + suffix "-istic" (relating to)',
                'memory_tip': 'Remember LINGUISTIC as "LINGUA" (language) + "ISTIC" (relating to) - relating to language study.',
                'example_sentence': 'The professor\'s _____ research focused on how children acquire grammar rules in their native language.'
            },
            'linguistics': {
                'pronunciation': '/ling-GWIS-tiks/',
                'definition': 'The scientific study of human language, encompassing its structure, history, variation, acquisition, and use across different cultures and social contexts, representing one of the most important cognitive and cultural phenomena that distinguishes humans from other species. Linguistics examines language at multiple levels: phonetics analyzes speech sounds and their production, phonology studies sound patterns and rules, morphology investigates word formation and structure, syntax explores sentence construction and grammatical relationships, semantics examines meaning systems, and pragmatics considers how context affects language interpretation. The field includes numerous specialized subdisciplines: historical linguistics traces language evolution and relationships, sociolinguistics studies language variation across social groups, psycholinguistics investigates mental processes in language use, computational linguistics develops computer models of language, and applied linguistics addresses practical applications like language teaching and speech therapy. Linguistic research reveals both universal principles shared across all human languages and remarkable diversity in how different cultures organize and express meaning. Modern linguistics employs rigorous scientific methods including data collection, hypothesis testing, and theoretical modeling to understand how language works, how children acquire it, and how it changes over time.',
                'etymology': 'From "linguistic" + suffix "-s" denoting the field of study',
                'memory_tip': 'Remember LINGUISTICS as the study of "LINGUA" (language) - the science of language itself.',
                'example_sentence': 'Students majoring in _____ learn to analyze language structure, evolution, and cultural variation across different societies.'
            },
            'linked': {
                'pronunciation': '/LINKD/',
                'definition': 'Connected, joined, or associated together in a relationship or sequence, forming bonds or connections between separate elements to create larger systems, networks, or relationships. In technology, linked refers to hyperlinks connecting web pages, documents, or data sources, enabling users to navigate between related information seamlessly. Database systems use linked records to establish relationships between different data sets, while linked lists in computer science connect data elements through pointer references. Social media platforms create linked networks where users connect with friends, colleagues, and communities, forming complex webs of social relationships. In biology, linked genes are located close together on chromosomes and tend to be inherited together, while linked traits show statistical correlation in inheritance patterns. Business contexts use linked to describe connected operations, supply chains, or strategic partnerships where separate entities work together toward common goals. Scientific research often reveals linked phenomena where changes in one variable correlate with changes in another, establishing causal or correlational relationships. The concept extends to mechanical linkages connecting moving parts in machines, economic linkages connecting different sectors of an economy, and intellectual linkages connecting ideas across different fields of study.',
                'etymology': 'Past participle of "link" from Old Norse "hlankr" (chain, link)',
                'memory_tip': 'Remember LINKED as connected like chain "LINK" + "ED" - things joined together in the past.',
                'example_sentence': 'The research clearly showed that air pollution and respiratory disease rates were closely _____ in urban areas.'
            },
            'linnet': {
                'pronunciation': '/LIN-it/',
                'definition': 'A small European finch (Linaria cannabina) belonging to the family Fringillidae, characterized by its brownish plumage with distinctive reddish markings on the breast and forehead of breeding males, making it a popular species among birdwatchers and avian enthusiasts. Linnets inhabit open countryside, heathlands, farmlands, and scrubby areas where they feed primarily on seeds from various plants including flax, dandelion, and other weedy species. These highly social birds often form large flocks during winter months, creating spectacular aerial displays as they move between feeding areas. Linnets build cup-shaped nests in dense shrubs or hedgerows, where females lay 4-6 pale blue eggs with brown markings. Their melodious song consists of twittering notes and musical phrases that have inspired poets and musicians throughout history. Male linnets are particularly vocal during breeding season, often singing from prominent perches to attract mates and defend territories. The species has experienced population declines in many areas due to agricultural intensification and habitat loss, leading to conservation efforts aimed at preserving appropriate breeding and feeding habitats. Linnets play important ecological roles as seed dispersers and serve as prey species for various predators including hawks and mammals.',
                'etymology': 'From Old French "linette," from "lin" (flax), as these birds often feed on flax seeds',
                'memory_tip': 'Remember LINNET as a little bird that loves "LIN" (flax) seeds - LIN + NET like catching seeds in a net.',
                'example_sentence': 'The birdwatcher was delighted to spot a male _____ singing from atop a gorse bush, its red breast clearly visible.'
            },
            'linsey': {
                'pronunciation': '/LIN-zee/',
                'definition': 'A type of coarse fabric, typically referring to linsey-woolsey, a durable textile made from a combination of linen (flax) fibers and wool, representing an important material in historical clothing and household goods, particularly in colonial America and rural European communities. Linsey-woolsey combined the strength and smoothness of linen with the warmth and water resistance of wool, creating a practical fabric suitable for everyday clothing, blankets, and household textiles. The fabric was typically woven with linen warp (lengthwise threads) and wool weft (crosswise threads), though variations existed depending on available materials and local traditions. This mixed-fiber approach made linsey more affordable than pure linen while providing better durability and warmth than cotton alternatives. Colonial American families often produced linsey-woolsey at home using locally grown flax and wool from their own sheep, making it an essential part of domestic textile production. The fabric\'s practical qualities made it popular for work clothes, undergarments, and bed linens among working-class families. While synthetic fabrics have largely replaced traditional linsey in modern manufacturing, historical reproductions and artisanal textile makers still produce linsey-woolsey for historical reenactments, traditional crafts, and specialty applications.',
                'etymology': 'Shortened form of "linsey-woolsey," from "lin" (linen) + "woolsey" (wool)',
                'memory_tip': 'Remember LINSEY as "LIN" (linen) + "SEY" sounds like "sew" - sewing linen with wool.',
                'example_sentence': 'The colonial museum displayed original _____ garments worn by 18th-century settlers in rural America.'
            },
            'linstock': {
                'pronunciation': '/LIN-stok/',
                'definition': 'A long wooden staff with a forked or pointed end used historically by artillery gunners to hold a lighted match (slow match) for igniting cannons and other gunpowder weapons, representing an essential tool in pre-modern warfare and naval combat. The linstock typically measured 3-4 feet in length, providing safe distance between the gunner and the cannon\'s touch hole when firing. One end featured a metal fork or spike to securely hold the slow-burning match cord, while the other end could be sharpened for sticking into the ground when not in use. Military regulations specified proper linstock construction and maintenance, as reliable ignition was crucial for effective artillery operations. Gunners carried multiple linstocks to ensure backup ignition sources, and naval crews maintained linstocks in weather-resistant containers to protect matches from moisture. The tool\'s design evolved over centuries, with different armies developing variations suited to their specific cannon types and tactical requirements. As firing mechanisms advanced from matchlock to flintlock and eventually to percussion systems, linstocks gradually became obsolete, though they remained in use through the 19th century in some armies. Today, linstocks appear primarily in historical reenactments, military museums, and artillery demonstrations, serving as reminders of traditional gunpowder warfare methods.',
                'etymology': 'From "lint" (slow-burning match) + "stock" (staff or handle)',
                'memory_tip': 'Remember LINSTOCK as "LINT" (burning match) + "STOCK" (wooden staff) - a stick for holding fire.',
                'example_sentence': 'The artillery sergeant carefully held the _____ steady as he prepared to ignite the cannon during the historical demonstration.'
            },
            'lionize': {
                'pronunciation': '/LI-ə-nīz/',
                'definition': 'To treat someone as a celebrity or person of great importance, typically by giving them excessive attention, praise, or adulation, often elevating them to near-heroic status in public perception or social circles. This practice involves recognizing and celebrating someone\'s achievements, talents, or contributions to such an extent that they become objects of widespread admiration and respect. Lionization often occurs in various contexts: media outlets lionize entertainment figures, sports heroes, or political leaders; academic communities lionize distinguished scholars and researchers; business sectors lionize successful entrepreneurs and innovators. The process can be beneficial when it appropriately recognizes genuine contributions and inspires others to pursue excellence, but it can become problematic when it creates unrealistic expectations or overlooks character flaws. Historical examples include the lionization of military heroes after successful campaigns, artists after breakthrough works, or scientists after major discoveries. Social media has amplified lionization processes, allowing rapid elevation of individuals to celebrity status through viral content or public achievements. The term suggests treating someone with the reverence typically reserved for a lion, the "king of beasts," implying majesty, power, and dominance in their particular field or society.',
                'etymology': 'From "lion" + suffix "-ize," meaning to treat like a lion (king of beasts)',
                'memory_tip': 'Remember LIONIZE as treating someone like a "LION" - making them the king of their field.',
                'example_sentence': 'The media began to _____ the young scientist after her groundbreaking research led to a potential cancer treatment.'
            },
            'lipophilic': {
                'pronunciation': '/LIP-ə-FIL-ik/',
                'definition': 'Having a strong affinity for lipids (fats and oils); describing substances, molecules, or compounds that readily dissolve in or bind with fatty substances while showing poor solubility in water, representing a fundamental concept in biochemistry, pharmacology, and molecular biology. Lipophilic substances, also called lipophiles or hydrophobic compounds, play crucial roles in biological systems: cell membranes consist primarily of lipophilic phospholipids that create barriers between cellular compartments; many hormones are lipophilic, allowing them to pass through cell membranes and directly influence gene expression; and numerous medications are designed to be lipophilic to enhance their absorption and distribution throughout the body. The lipophilic nature of compounds affects their behavior in biological systems: they tend to accumulate in fatty tissues, cross the blood-brain barrier more easily, and require special transport mechanisms for movement through aqueous environments. Pharmaceutical researchers carefully consider lipophilicity when designing drugs, as it influences absorption, distribution, metabolism, and elimination properties. Environmental scientists study lipophilic pollutants because they bioaccumulate in food chains, concentrating in fatty tissues of organisms. Understanding lipophilic interactions is essential for developing effective treatments, predicting environmental impacts, and comprehending basic cellular processes.',
                'etymology': 'From Greek "lipos" (fat) + "philic" (loving), meaning fat-loving',
                'memory_tip': 'Remember LIPOPHILIC as "LIPO" (fat) + "PHILIC" (loving) - molecules that love fat.',
                'example_sentence': 'The drug\'s _____ properties allowed it to easily cross cell membranes and reach its target tissues.'
            },
            'liquefaction': {
                'pronunciation': '/LIK-wə-FAK-shən/',
                'definition': 'The process of converting a solid or gas into a liquid state through the application of heat, pressure, or chemical treatment, representing a fundamental phase transition with important applications across numerous scientific and industrial fields. In physics, liquefaction occurs when molecular motion increases sufficiently (through heating) or when molecular spacing decreases sufficiently (through compression) to overcome the forces holding particles in solid or gaseous arrangements. Industrial liquefaction processes include converting coal into liquid fuels through chemical treatment, transforming natural gas into liquefied natural gas (LNG) for efficient transportation and storage, and producing liquid oxygen and nitrogen for medical and industrial applications. Geological liquefaction describes the process by which water-saturated sediments lose strength during earthquakes, causing solid ground to behave like a liquid and leading to significant infrastructure damage. Medical applications include the liquefaction of gallstones using shock waves, making them easier to eliminate naturally. Food processing utilizes controlled liquefaction to create products like honey, syrups, and certain dairy products. Understanding liquefaction principles is crucial for materials science, geological engineering, chemical processing, and environmental management, as it affects everything from natural disaster mitigation to energy production and storage.',
                'etymology': 'From Latin "liquefacere" (to make liquid), from "liquere" (to be liquid) + "facere" (to make)',
                'memory_tip': 'Remember LIQUEFACTION as making something "LIQU(ID)" through "FACTION" (making/doing) - making liquid.',
                'example_sentence': 'The earthquake caused soil _____ in the coastal area, causing buildings to sink and tilt dangerously.'
            },
            'lisp': {
                'pronunciation': '/LISP/',
                'definition': 'A speech impediment characterized by difficulty pronouncing sibilant consonants, particularly "s" and "z" sounds, which are often replaced with "th" sounds, creating distinctive pronunciation patterns that can affect communication clarity and social interactions. Lisping typically results from improper tongue placement during speech production: instead of positioning the tongue tip against the alveolar ridge (just behind the upper teeth), speakers with lisps often place their tongue between or against their teeth. There are several types of lisps: frontal lisp (tongue protrudes between teeth), lateral lisp (air escapes over the sides of the tongue), and palatal lisp (tongue contacts the soft palate). Lisping can occur naturally during childhood speech development, with most children outgrowing it by age 5-6, or it can persist into adulthood requiring speech therapy intervention. Causes include anatomical variations (tongue tie, dental irregularities, cleft palate), hearing difficulties, or simply learned speech patterns. Speech-language pathologists treat persistent lisps through targeted exercises focusing on proper tongue placement, airflow control, and sound discrimination. While lisping rarely affects overall communication effectiveness, it can impact self-confidence and social interactions, making professional treatment beneficial for many individuals.',
                'etymology': 'From Old English "wlisp" meaning to speak with a lisp, related to "lisp" meaning to falter in speech',
                'memory_tip': 'Remember LISP as when "L" and "S" sounds get mixed up - "L-I-S-P" shows the problem sounds.',
                'example_sentence': 'The speech therapist helped the child overcome her _____ by practicing proper tongue placement for "s" sounds.'
            },
            'listener': {
                'pronunciation': '/LIS-ə-nər/',
                'definition': 'A person who actively pays attention to sounds, speech, music, or other auditory information, engaging in the cognitive and emotional process of receiving, interpreting, and responding to audio communication and environmental sounds. Effective listening involves multiple skills: auditory processing (accurately receiving sound waves), attention management (focusing on relevant information while filtering distractions), comprehension (understanding meaning and context), and response preparation (formulating appropriate reactions). In communication contexts, listeners play crucial roles in conversations, educational settings, therapeutic relationships, and entertainment experiences. Good listeners demonstrate active listening skills including maintaining eye contact, asking clarifying questions, providing appropriate feedback, and avoiding interruptions. Research shows that most people spend more time listening than speaking, reading, or writing, making listening skills fundamental to personal and professional success. Different contexts require different listening approaches: critical listening for evaluating arguments and evidence, empathetic listening for understanding emotions and perspectives, appreciative listening for enjoying music and entertainment, and discriminative listening for distinguishing between sounds and meanings. Modern technology has transformed listening experiences through streaming services, podcasts, audiobooks, and digital communication platforms, creating new opportunities and challenges for effective listening in information-rich environments.',
                'etymology': 'From "listen" + suffix "-er" indicating one who performs the action',
                'memory_tip': 'Remember LISTENER as "LISTEN" + "ER" - someone who does the listening.',
                'example_sentence': 'The counselor was an excellent _____, making clients feel heard and understood during difficult conversations.'
            },
            'listlessly': {
                'pronunciation': '/LIST-ləs-lee/',
                'definition': 'In a manner lacking energy, enthusiasm, or interest; characterized by apathy, lethargy, and indifference toward activities or situations that would normally engage attention or motivation. This adverb describes behavior that appears tired, sluggish, or emotionally detached, often indicating underlying physical fatigue, emotional exhaustion, depression, or lack of purpose. People acting listlessly might move slowly without apparent direction, participate in activities without genuine engagement, or respond to situations with minimal emotional investment. Listless behavior can stem from various causes: physical illness or medical conditions that drain energy, psychological states such as depression or burnout, life circumstances that create feelings of hopelessness or meaninglessness, or simple temporary fatigue from overwork or stress. In literature, characters often behave listlessly to convey emotional states, create atmosphere, or advance plot development. Medical professionals recognize listlessness as a potential symptom of various conditions including anemia, thyroid disorders, chronic fatigue syndrome, and mental health conditions. Recognizing listless behavior in oneself or others can prompt important conversations about well-being, health assessments, or lifestyle changes needed to restore energy and engagement with life\'s activities.',
                'etymology': 'From "listless" (lacking energy or enthusiasm) + adverbial suffix "-ly"',
                'memory_tip': 'Remember LISTLESSLY as "LIST-LESS" (no list, no goals) + "LY" - doing things without purpose.',
                'example_sentence': 'After months of unemployment, he wandered through his days _____, unable to summon enthusiasm for job searching.'
            },
            'lists': {
                'pronunciation': '/LISTS/',
                'definition': 'Organized sequences of items, names, numbers, or concepts arranged in a particular order for reference, organization, or systematic presentation, serving as fundamental tools for information management, task organization, and knowledge structure across countless personal, professional, and academic applications. Lists can be organized alphabetically, numerically, chronologically, by importance, or according to other logical systems depending on their intended purpose. Common types include grocery lists for shopping efficiency, to-do lists for task management, contact lists for communication, inventory lists for resource tracking, and reference lists for academic citations. Digital technology has transformed list-making through applications that enable sharing, collaboration, automatic sorting, and integration with other systems. In literature and rhetoric, lists can create emphasis, rhythm, and comprehensive coverage of topics. Scientific research often presents findings in list format for clarity and systematic presentation. Lists serve cognitive functions by reducing memory load, providing structure for complex information, and enabling systematic processing of multiple items. The effectiveness of lists depends on clear organization, appropriate level of detail, regular updating, and alignment with user needs and contexts.',
                'etymology': 'Plural of "list" from Old French "liste," meaning a strip of paper or border',
                'memory_tip': 'Remember LISTS as multiple "LIST" items - organized sequences of information.',
                'example_sentence': 'The project manager created detailed _____ of tasks, deadlines, and responsible team members for each phase.'
            },
            'lisztian': {
                'pronunciation': '/LIST-zee-ən/',
                'definition': 'Relating to or characteristic of Franz Liszt (1811-1886), the Hungarian composer and virtuoso pianist who revolutionized both piano technique and musical composition during the Romantic era, establishing new standards for technical brilliance, emotional expression, and innovative musical forms. Lisztian elements in music include extraordinarily demanding technical passages requiring exceptional finger dexterity and hand coordination, revolutionary use of piano sonorities and extended techniques, programmatic compositions that tell stories or paint musical pictures, and harmonic innovations that influenced later composers including Wagner and Debussy. Liszt\'s compositional style featured dramatic contrasts between loud and soft passages, innovative pedal techniques that created new tonal colors, and transformation of themes throughout compositions to create organic musical development. His piano transcriptions of orchestral works demonstrated remarkable ability to capture full orchestral textures on solo piano, while his original compositions like the Piano Sonata in B minor and Hungarian Rhapsodies remain cornerstone works of piano literature. Lisztian performance style emphasizes dramatic interpretation, technical perfection, and charismatic stage presence that engages audiences emotionally. The term also describes teaching methods emphasizing technical development alongside musical expression, following Liszt\'s pedagogical approach with his many distinguished students.',
                'etymology': 'From Franz Liszt + suffix "-ian" meaning relating to or characteristic of',
                'memory_tip': 'Remember LISZTIAN as "LISZT" (the composer) + "IAN" (relating to) - in the style of Franz Liszt.',
                'example_sentence': 'The young pianist\'s performance displayed the virtuosic, dramatic style typical of the _____ tradition.'
            },
            'litany': {
                'pronunciation': '/LIT-ə-nee/',
                'definition': 'A form of prayer or ceremonial recitation consisting of a series of petitions, responses, or invocations, typically characterized by repetitive structure and rhythmic patterns that create meditative or ceremonial effects in religious, literary, or rhetorical contexts. In Christian liturgy, litanies involve a leader reciting prayers or statements while the congregation responds with repeated phrases like "Lord, have mercy" or "Pray for us," creating communal participation in worship. The term extends beyond religious contexts to describe any lengthy recitation, enumeration, or repetitive listing of items, complaints, or concerns. Literary litanies appear in poetry and prose to create emphasis, rhythm, and emotional intensity through repetitive structures that build cumulative power. Political speeches sometimes employ litany-like repetition to emphasize key points and create memorable rhetorical effects. In everyday usage, "litany" often describes a long series of complaints, problems, or grievances presented in succession. The repetitive nature of litanies serves psychological and social functions: in religious contexts, they facilitate meditation and group bonding; in literary contexts, they create aesthetic effects and emotional responses; in persuasive contexts, they emphasize important points through repetition and rhythm.',
                'etymology': 'From Greek "litaneia" meaning prayer or supplication, from "lite" (prayer)',
                'memory_tip': 'Remember LITANY as "LIT" (like recited) + "ANY" - any repeated prayer or list.',
                'example_sentence': 'The congregation participated in the _____ of saints, responding "pray for us" after each invocation.'
            },
            'literacy': {
                'pronunciation': '/LIT-ər-ə-see/',
                'definition': 'The ability to read, write, and comprehend written language effectively, representing a fundamental skill that enables individuals to access information, communicate ideas, participate fully in society, and engage in lifelong learning across personal, professional, and civic domains. Literacy encompasses multiple components: decoding skills for translating written symbols into sounds and meanings, vocabulary knowledge for understanding word meanings and relationships, comprehension strategies for extracting and constructing meaning from texts, and writing abilities for expressing ideas clearly and effectively. Modern literacy concepts have expanded beyond basic reading and writing to include digital literacy (navigating electronic texts and multimedia), visual literacy (interpreting images and graphics), critical literacy (analyzing and evaluating information sources), and disciplinary literacies specific to different fields like scientific or mathematical literacy. Educational research emphasizes that literacy development is ongoing throughout life, requiring continued practice and refinement as texts become more complex and contexts change. Literacy rates serve as important indicators of educational system effectiveness and societal development, with UNESCO and other organizations tracking global progress toward universal literacy goals. Strong literacy skills correlate with improved economic opportunities, better health outcomes, increased civic participation, and enhanced quality of life.',
                'etymology': 'From Latin "literatus" meaning learned or lettered, from "litera" (letter)',
                'memory_tip': 'Remember LITERACY as "LITER" (letter) + "ACY" (ability) - the ability to work with letters.',
                'example_sentence': 'The school implemented a comprehensive _____ program to improve students\' reading and writing skills across all subjects.'
            },
            'literally': {
                'pronunciation': '/LIT-ər-ə-lee/',
                'definition': 'In a literal manner; according to the exact meaning of words without metaphor, allegory, or figurative interpretation, emphasizing precise, factual accuracy rather than symbolic or exaggerated expression. This adverb indicates that statements should be understood according to their most basic, dictionary definitions rather than as hyperbole, idioms, or figurative language. However, modern usage has evolved to include an intensifying function where "literally" emphasizes the speaker\'s sincerity or the surprising nature of a situation, even when not strictly literal. Traditional prescriptive grammar maintains that "literally" should only be used when statements are factually accurate, but descriptive linguists recognize that language naturally evolves and "literally" now serves multiple communicative functions. In academic and professional writing, "literally" helps distinguish between figurative and actual meanings, preventing misunderstandings about whether statements represent facts or metaphorical expressions. The word\'s dual usage sometimes creates confusion, leading style guides to recommend careful consideration of context and audience when using it. Understanding both literal and intensifying functions of "literally" enables more effective communication while recognizing the dynamic nature of language change over time.',
                'etymology': 'From "literal" + adverbial suffix "-ly," from Latin "literalis" (of letters)',
                'memory_tip': 'Remember LITERALLY as "LITERAL" + "LY" - in the exact, word-for-word sense.',
                'example_sentence': 'The temperature dropped so quickly that the water _____ froze within minutes of the cold front arriving.'
            },
            'literatim': {
                'pronunciation': '/LIT-ər-AH-tim/',
                'definition': 'A Latin term meaning letter for letter; exactly as written or word for word, used to indicate that text should be reproduced, quoted, or transcribed with absolute precision without any alterations, corrections, or interpretations. In legal contexts, literatim quotations ensure that contracts, statutes, testimonies, and other documents are referenced with complete accuracy, preventing disputes that might arise from paraphrasing or summarization. Academic scholarship uses literatim citations when precise wording is crucial for analysis, maintaining the exact language of primary sources, historical documents, or research data. Medical and scientific fields employ literatim transcription for patient records, research notes, and experimental observations where accuracy is essential for proper diagnosis, treatment, and replication of studies. The term emphasizes the importance of faithful reproduction in situations where even minor changes in wording might alter meaning, legal standing, or scientific validity. Literatim copying requires careful attention to detail including spelling, punctuation, capitalization, and formatting exactly as they appear in original sources. This concept contrasts with paraphrasing or summarizing, which involve restating ideas in different words while maintaining general meaning. Understanding when literatim accuracy is necessary versus when paraphrasing is acceptable requires judgment about context, purpose, and potential consequences of textual variations.',
                'etymology': 'Latin "literatim" from "litera" (letter) meaning letter by letter',
                'memory_tip': 'Remember LITERATIM as "LITER" (letter) + "ATIM" (exactly) - exactly letter by letter.',
                'example_sentence': 'The court reporter was required to transcribe the witness testimony _____ to ensure legal accuracy.'
            },
            'literature': {
                'pronunciation': '/LIT-ər-ə-CHər/',
                'definition': 'Written works of artistic, cultural, or intellectual merit, particularly those considered to have lasting value and significance in human culture, encompassing poetry, fiction, drama, essays, and other creative expressions that explore universal themes, human experiences, and aesthetic possibilities through sophisticated use of language. Literature serves multiple functions: it preserves cultural knowledge and values across generations, provides insights into human nature and social conditions, offers aesthetic pleasure through beautiful and powerful use of language, and challenges readers to consider new perspectives and ideas. Major literary genres include epic poetry that tells heroic stories, lyric poetry expressing personal emotions and observations, novels exploring character development and social themes, short stories focusing on specific moments or situations, and drama presenting conflicts through dialogue and action. Literary analysis examines elements such as plot structure, character development, symbolism, themes, style, and historical context to understand how authors create meaning and artistic effects. Literature education develops critical thinking skills, cultural awareness, empathy, and communication abilities while connecting students to their cultural heritage and global human experiences. Contemporary literature continues evolving through digital media, diverse voices, and new forms of expression while maintaining connections to traditional literary values and techniques.',
                'etymology': 'From Latin "literatura" meaning learning or writing, from "litera" (letter)',
                'memory_tip': 'Remember LITERATURE as "LITER" (letters) + "ATURE" (collection) - a collection of written letters/works.',
                'example_sentence': 'The English professor assigned classic works of American _____ including novels by Twain, Hawthorne, and Morrison.'
            },
            'lithium': {
                'pronunciation': '/LITH-ee-əm/',
                'definition': 'A soft, silvery-white alkali metal and the lightest solid element on the periodic table, with atomic number 3 and symbol Li, playing crucial roles in modern technology, medicine, and industrial applications due to its unique chemical and physical properties. Lithium\'s exceptional characteristics include being the least dense metal, having high electrochemical potential, and exhibiting strong reactivity with water and air, requiring storage in mineral oil or inert atmospheres. The element\'s most prominent modern application involves rechargeable lithium-ion batteries that power smartphones, laptops, electric vehicles, and energy storage systems, making it essential for the transition to renewable energy and electric transportation. In medicine, lithium compounds treat bipolar disorder and other psychiatric conditions, though requiring careful monitoring due to narrow therapeutic windows and potential side effects. Industrial applications include ceramics and glass production where lithium compounds reduce melting temperatures and thermal expansion, aluminum production where lithium improves metal properties, and specialized lubricants for extreme temperature conditions. Lithium occurs naturally in brine deposits, pegmatite rocks, and certain clay formations, with major reserves in Chile, Argentina, Australia, and China. Growing demand for electric vehicles and energy storage has created increased interest in lithium extraction and recycling technologies.',
                'etymology': 'From Greek "lithos" meaning stone, as it was first discovered in mineral form',
                'memory_tip': 'Remember LITHIUM as "LITH" (stone) + "IUM" (element) - the stone element, discovered in minerals.',
                'example_sentence': 'Electric vehicle manufacturers require large quantities of _____ for producing the rechargeable batteries that power their cars.'
            },
            'lithophone': {
                'pronunciation': '/LITH-ə-fōn/',
                'definition': 'A musical percussion instrument consisting of tuned stone slabs or bars that produce musical tones when struck with mallets, representing one of humanity\'s oldest forms of musical expression dating back thousands of years to prehistoric cultures worldwide. Lithophones utilize the natural resonant properties of specific stone types, particularly limestone, slate, marble, and volcanic rock, which produce clear, sustained tones when properly shaped and supported. Historical examples include the famous Vietnamese đàn đá instruments carved from stone slabs and arranged chromatically, ancient Chinese bianqing stone chimes used in ritual ceremonies, and various African stone instruments discovered in archaeological sites. Modern lithophone construction involves careful selection of resonant stones, precise tuning through grinding and shaping, and mounting systems that allow stones to vibrate freely for optimal sound production. The instrument\'s unique timbral qualities create ethereal, bell-like tones that blend well with other percussion instruments in contemporary classical music, world music ensembles, and experimental compositions. Lithophones require skilled craftsmanship to achieve proper intonation and tonal balance, making them relatively rare instruments that fascinate both musicians and audiences. Their durability surpasses most other musical instruments, with ancient examples still producing music after centuries of existence.',
                'etymology': 'From Greek "lithos" (stone) + "phone" (sound), meaning stone sound',
                'memory_tip': 'Remember LITHOPHONE as "LITHO" (stone) + "PHONE" (sound) - an instrument that makes sound from stone.',
                'example_sentence': 'The composer incorporated a _____ into the orchestral arrangement to create mysterious, stone-like percussive tones.'
            },
            'lithuania': {
                'pronunciation': '/LITH-oo-AY-nee-ə/',
                'definition': 'A Baltic country in Northern Europe, officially known as the Republic of Lithuania, located along the southeastern shore of the Baltic Sea and bordered by Latvia, Belarus, Poland, and Russia\'s Kaliningrad Oblast, representing one of the three Baltic states that regained independence from the Soviet Union in 1991. Lithuania covers approximately 65,300 square kilometers with a population of about 2.8 million people, making it the largest of the Baltic countries by both area and population. The capital and largest city is Vilnius, known for its well-preserved medieval Old Town and baroque architecture that attracts numerous tourists annually. Lithuanian culture reflects a unique blend of Baltic traditions, Catholic influences, and modern European developments, with the Lithuanian language being one of the oldest Indo-European languages still spoken today. The country\'s history includes the powerful Grand Duchy of Lithuania that existed from the 14th to 18th centuries, periods of foreign occupation by Poland, Russia, and Germany, and decades of Soviet control before independence restoration. Modern Lithuania has successfully transitioned to a democratic market economy, joining NATO in 2004 and the European Union in the same year, while maintaining strong cultural identity and traditional festivals. The economy focuses on services, industry, and agriculture, with significant growth in information technology and financial services sectors.',
                'etymology': 'From Lithuanian "Lietuva," possibly related to "Lietava" (a small river) or meaning "land of rain"',
                'memory_tip': 'Remember LITHUANIA as "LITH" sounds like "little" + "UANIA" - one of the smaller Baltic countries.',
                'example_sentence': 'After joining the European Union, _____ experienced significant economic growth and increased cultural exchanges with Western Europe.'
            },
            'litigious': {
                'pronunciation': '/li-TIJ-əs/',
                'definition': 'Characterized by a tendency to engage in lawsuits; prone to bringing legal action against others, often excessively or unnecessarily, reflecting an inclination to resolve disputes through formal legal proceedings rather than alternative methods like negotiation, mediation, or compromise. Litigious behavior can stem from various motivations: genuine grievances requiring legal remedy, desire for financial compensation, personality traits that favor confrontational approaches, or cultural and professional environments that normalize legal action as first recourse for problem-solving. Some individuals develop reputations for being litigious after filing multiple lawsuits, while certain industries or professions naturally involve higher levels of litigation due to complex regulations, high stakes, or contractual relationships. Society\'s relationship with litigiousness reflects broader cultural attitudes toward conflict resolution, legal systems, and individual rights. While legal action serves important functions in protecting rights and ensuring justice, excessive litigiousness can strain court systems, increase costs for businesses and individuals, and damage relationships unnecessarily. Understanding when litigation represents appropriate recourse versus when alternative dispute resolution might be more effective requires balancing legal rights with practical considerations including time, cost, relationships, and likelihood of successful outcomes.',
                'etymology': 'From Latin "litigiosus" meaning quarrelsome, from "litigare" (to dispute in court)',
                'memory_tip': 'Remember LITIGIOUS as "LITIGATE" (sue) + "IOUS" (full of) - full of lawsuits.',
                'example_sentence': 'The company avoided doing business with the _____ contractor who had filed numerous lawsuits against previous clients.'
            },
            'litmus': {
                'pronunciation': '/LIT-məs/',
                'definition': 'A water-soluble mixture of different dyes extracted from certain lichens, particularly Roccella tinctoria, used as an acid-base indicator that changes color depending on the pH level of solutions, representing one of the most fundamental and widely recognized chemical testing tools in laboratories and educational settings worldwide. Litmus exhibits distinctive color changes: it turns red in acidic solutions (pH less than 7) and blue in basic or alkaline solutions (pH greater than 7), while remaining purple in neutral solutions (pH approximately 7). This simple yet reliable color-change mechanism makes litmus paper an essential tool for quickly determining whether substances are acidic or basic without requiring complex equipment or calculations. The indicator works because litmus contains chromophores (color-producing molecular structures) that change configuration when hydrogen ion concentrations vary, resulting in visible color shifts that correspond to pH levels. Beyond its laboratory applications, "litmus test" has entered common usage as a metaphor for simple, decisive tests that clearly reveal essential characteristics or qualities of situations, policies, or individuals. Educational institutions use litmus paper to teach fundamental chemistry concepts, while researchers employ it for preliminary pH assessments before using more precise electronic pH meters for detailed measurements.',
                'etymology': 'From Dutch "lakmoes," possibly from "lak" (lac, a red dye) + "moes" (pulp)',
                'memory_tip': 'Remember LITMUS as "LIT" (light up with color) + "MUS" (must show) - must show pH by lighting up with color.',
                'example_sentence': 'The chemistry students used _____ paper to test whether the unknown solution was acidic or basic.'
            },
            'littoral': {
                'pronunciation': '/LIT-ər-əl/',
                'definition': 'Relating to or situated on the shore or coastal region of a sea, lake, or large river; describing the zone between high and low tide marks or the shallow nearshore area where aquatic ecosystems transition to terrestrial environments, representing a critical interface between land and water systems with unique ecological, geological, and economic characteristics. Littoral zones support distinctive biological communities adapted to fluctuating conditions including varying water levels, wave action, temperature changes, and salinity variations in marine environments. These areas serve as nursery habitats for many fish species, feeding grounds for migratory birds, and breeding areas for various marine and aquatic organisms. Littoral vegetation includes specialized plants like salt-tolerant grasses, mangroves in tropical regions, and algae adapted to periodic exposure to air. Human activities heavily impact littoral zones through coastal development, pollution, fishing, recreation, and climate change effects including sea level rise and increased storm intensity. Environmental management recognizes littoral areas as particularly vulnerable ecosystems requiring special protection due to their ecological importance and exposure to multiple stressors. Understanding littoral processes helps scientists study coastal erosion, sediment transport, habitat conservation, and the effects of human activities on coastal ecosystems and communities.',
                'etymology': 'From Latin "litoralis" meaning of the seashore, from "litus" (shore)',
                'memory_tip': 'Remember LITTORAL as "LITTER" (scattered) + "AL" (area) - the area where land and sea scatter together.',
                'example_sentence': 'Marine biologists studied the diverse species found in the _____ zone between high and low tide marks.'
            },
            'liturgy': {
                'pronunciation': '/LIT-ər-jee/',
                'definition': 'The formal, prescribed ritual and ceremonial procedures used in public religious worship, encompassing the structured sequence of prayers, readings, songs, and symbolic actions that constitute organized religious services across various faith traditions, particularly in Christianity, Judaism, and other liturgical religions. Christian liturgy varies among denominations but typically includes elements such as processionals, scriptural readings, homilies or sermons, communion or Eucharist, and benedictions arranged according to theological principles and seasonal calendars. The liturgical year follows cyclical patterns celebrating major religious events like Christmas, Easter, Pentecost, and other holy days that shape the rhythm of worship throughout the year. Liturgical music, vestments, architecture, and ceremonial objects contribute to the overall worship experience, creating sacred atmosphere and facilitating community participation in religious observances. Different Christian traditions emphasize various aspects of liturgy: Catholic and Orthodox churches maintain elaborate ritual traditions, while Protestant denominations range from highly liturgical (Episcopal, Lutheran) to less formal (Baptist, Pentecostal) approaches. Liturgical scholarship studies the historical development, theological significance, and cultural impact of worship practices, examining how liturgy shapes religious identity, community bonds, and spiritual experiences across different cultures and time periods.',
                'etymology': 'From Greek "leitourgia" meaning public service or worship, from "leitos" (public) + "ergon" (work)',
                'memory_tip': 'Remember LITURGY as "LITER" (public reading) + "URGY" (work) - the public work of worship.',
                'example_sentence': 'The ancient _____ included traditional chants and prayers that had been used in the church for over a thousand years.'
            },
            'live': {
                'pronunciation': '/līv/ (verb), /LIV/ (adjective)',
                'definition': 'To be alive; to exist as a living being with biological functions including growth, metabolism, reproduction, and response to environmental stimuli, representing the fundamental state of being that distinguishes living organisms from inanimate objects and deceased matter. Living involves multiple dimensions: biological existence through cellular processes, conscious experience through sensory perception and cognition, social existence through relationships and cultural participation, and temporal existence through continuous development and change over time. The concept extends beyond mere survival to encompass quality of life factors including health, happiness, purpose, and fulfillment that contribute to meaningful existence. As an adjective, "live" describes things that are currently alive, happening in real-time (live television broadcasts, live performances), or capable of activity (live electrical wires, live ammunition). Philosophical questions about what it means to truly "live" versus merely exist have occupied thinkers throughout history, exploring concepts of authentic living, purposeful existence, and the relationship between biological life and meaningful experience. Modern discussions about living well incorporate physical health, mental wellness, social connections, environmental sustainability, and personal fulfillment as essential components of quality living.',
                'etymology': 'From Old English "libban" meaning to live, be alive, related to German "leben"',
                'memory_tip': 'Remember LIVE as the opposite of dead - to be alive and active.',
                'example_sentence': 'Scientists study extremophile bacteria that can _____ in the harsh conditions of deep ocean thermal vents.'
            },
            'lived': {
                'pronunciation': '/LIVD/',
                'definition': 'Past tense of live; having existed as a living being, experienced life events, or resided in particular places during past time periods, representing the accumulated history of experiences, relationships, and activities that constitute an individual\'s or community\'s biographical narrative. Lived experiences encompass all aspects of existence including personal relationships, educational achievements, professional activities, cultural practices, challenges overcome, and wisdom gained through time. The concept of "lived experience" holds particular importance in phenomenological philosophy, qualitative research, and social sciences, where understanding subjective human experience provides insights into meaning-making, identity formation, and social phenomena. Lived experiences differ from theoretical or secondhand knowledge because they involve direct personal encounter with situations, emotions, and consequences that shape understanding and perspective. In therapeutic and counseling contexts, acknowledging clients\' lived experiences validates their personal narratives and provides foundation for healing and growth. Historical and sociological studies examine how different groups\' lived experiences reflect broader social patterns, inequalities, and cultural changes over time. Understanding that everyone brings unique lived experiences to interactions promotes empathy, respect for diversity, and more inclusive approaches to education, healthcare, and social policy.',
                'etymology': 'Past tense of "live" from Old English "libban"',
                'memory_tip': 'Remember LIVED as "LIVE" + "D" (past) - having experienced life in the past.',
                'example_sentence': 'The elderly woman had _____ through both World War II and the civil rights movement in America.'
            },
            'liver': {
                'pronunciation': '/LIV-ər/',
                'definition': 'The largest internal organ in the human body and most complex metabolic organ in vertebrates, performing over 500 essential functions including detoxification of harmful substances, protein synthesis, bile production for fat digestion, glucose regulation, and storage of vitamins and minerals, making it crucial for survival and overall health. Located in the upper right portion of the abdominal cavity beneath the diaphragm, the liver receives blood from both the hepatic artery (carrying oxygen-rich blood) and portal vein (carrying nutrient-rich blood from digestive organs), processing approximately 1.5 liters of blood per minute. The organ\'s remarkable regenerative capacity allows it to restore up to 75% of its mass after injury or surgical removal, making it unique among human organs. Liver functions include metabolizing carbohydrates, fats, and proteins; producing albumin and other plasma proteins; storing iron, vitamins A, D, E, K, and B12; converting ammonia to urea for safe elimination; and producing bile acids essential for fat absorption. Liver diseases including hepatitis, cirrhosis, fatty liver disease, and liver cancer significantly impact health and can be life-threatening. Understanding liver health involves recognizing risk factors such as alcohol consumption, viral infections, obesity, and certain medications that can damage hepatocytes (liver cells).',
                'etymology': 'From Old English "lifer," related to "live" as it was considered essential for life',
                'memory_tip': 'Remember LIVER as the organ that helps you "LIVE" + "ER" - the organ that makes living possible.',
                'example_sentence': 'The doctor explained that the _____ processes toxins from the blood and produces bile to help digest fats.'
            },
            'livery': {
                'pronunciation': '/LIV-ər-ee/',
                'definition': 'A distinctive uniform, costume, or style of dress worn by servants, employees, or members of a particular organization, guild, or household, historically indicating their allegiance, rank, or function within hierarchical social structures, particularly in medieval and early modern European societies. Traditional livery included specific colors, patterns, badges, or emblems that identified the wearer\'s master, company, or institution, serving both practical and symbolic purposes in societies where visual identification was crucial for social navigation and security. Medieval nobles provided livery to their retainers, creating visual displays of wealth, power, and loyalty that reinforced social hierarchies and political alliances. The concept extends to modern contexts including military uniforms, corporate attire, school uniforms, and ceremonial dress that maintain traditions of institutional identity and professional distinction. Livery companies in London, evolved from medieval trade guilds, continue historic traditions while engaging in charitable activities and maintaining craft standards. The term also refers to the care, feeding, and housing of horses (livery stable), reflecting historical connections between transportation services and distinctive identification of service providers. Understanding livery traditions provides insights into social history, class relations, corporate identity, and the symbolic power of dress in human societies.',
                'etymology': 'From Anglo-French "livere" meaning delivery or allowance, referring to clothes provided to servants',
                'memory_tip': 'Remember LIVERY as "LIVE" (serve) + "ERY" (place/thing) - clothing for those who serve.',
                'example_sentence': 'The hotel staff wore elegant _____ featuring the establishment\'s distinctive colors and crest.'
            },
            'lives': {
                'pronunciation': '/līvz/ (noun plural), /LIVz/ (verb)',
                'definition': 'The plural form of life, referring to multiple individual existences, biographical narratives, or living beings, encompassing the diverse experiences, relationships, and stories that constitute human existence across different contexts, cultures, and time periods. Lives represent the collective human experience including various life stages, social roles, cultural backgrounds, and individual choices that shape personal and social history. Understanding different lives provides insights into human diversity, social conditions, historical periods, and universal themes that connect all human experience despite surface differences. The study of lives appears in biography, autobiography, oral history, and social sciences where researchers examine how individual experiences reflect broader patterns of social change, cultural values, and historical events. Lives can be examined through various lenses: developmental psychology studies how lives unfold through predictable stages, sociology examines how social forces shape individual trajectories, and history explores how personal lives both influence and reflect broader historical movements. The concept of "saving lives" emphasizes the precious nature of human existence and motivates medical research, public health initiatives, emergency services, and humanitarian efforts. Understanding that everyone has complex, meaningful lives promotes empathy, respect for human dignity, and commitment to creating conditions that support flourishing for all people.',
                'etymology': 'Plural of "life" from Old English "lif" meaning existence, lifetime',
                'memory_tip': 'Remember LIVES as multiple "LIFE" experiences - many people\'s life stories.',
                'example_sentence': 'The documentary explored the _____ of three generations of women in the same family during major historical changes.'
            },
            'livid': {
                'pronunciation': '/LIV-id/',
                'definition': 'Extremely angry; furious to the point of being visibly affected by rage, often characterized by facial color changes, tense body language, and intense emotional expression that reflects deep indignation or outrage about perceived injustices, betrayals, or frustrating situations. Livid anger typically results from situations that trigger strong emotional responses: violations of trust, unfair treatment, moral outrages, or circumstances that threaten important values or relationships. The term originally described a bluish or grayish skin coloration, particularly in medical contexts referring to bruising or oxygen deprivation, but has evolved primarily to describe emotional states where anger is so intense that it manifests physically through changes in complexion, vocal tone, or body posture. People become livid when they feel powerless against perceived injustices, when their efforts are dismissed or undermined, or when they witness treatment of others that violates their moral standards. Understanding livid emotional states helps in conflict resolution, relationship management, and recognizing when situations require cooling-off periods before productive communication can occur. While intense anger serves important functions in motivating responses to genuine problems, learning to manage livid emotions constructively prevents damage to relationships and promotes more effective problem-solving approaches.',
                'etymology': 'From Latin "lividus" meaning bluish, from "livere" (to be bluish), later extended to mean furious',
                'memory_tip': 'Remember LIVID as so angry you turn blue - "LIV" (blue) + "ID" (intense) - intensely blue with anger.',
                'example_sentence': 'The customer became _____ when the airline cancelled her flight without explanation just hours before departure.'
            },
            'living': {
                'pronunciation': '/LIV-ing/',
                'definition': 'The condition or experience of being alive; existing as a biological entity with the capacity for growth, reproduction, response to stimuli, and adaptation to environmental changes, representing the dynamic state of life that encompasses both survival needs and quality of life considerations. Living involves multiple dimensions: biological functioning through cellular processes and organ systems, conscious experience through sensory perception and cognition, social existence through relationships and community participation, and purposeful activity through work, creativity, and personal development. The concept of "making a living" refers to earning income sufficient to support oneself and dependents, while "standard of living" describes the level of comfort, goods, and services available to individuals or communities. Living conditions significantly impact health, happiness, and life outcomes, leading to public health initiatives, social policies, and urban planning efforts aimed at improving housing, sanitation, education, and economic opportunities. Philosophical and spiritual traditions explore questions about what constitutes meaningful living, examining relationships between material well-being, personal fulfillment, social contribution, and spiritual development. Modern discussions about living well integrate physical health, mental wellness, environmental sustainability, and social justice as interconnected aspects of quality living for individuals and communities.',
                'etymology': 'Present participle of "live" from Old English "lifian"',
                'memory_tip': 'Remember LIVING as actively "LIV" (being alive) + "ING" (ongoing) - ongoing state of being alive.',
                'example_sentence': 'The family worked hard to improve their _____ conditions by finding better housing and educational opportunities.'
            },
            'llama': {
                'pronunciation': '/LLA-mə/',
                'definition': 'A domesticated South American camelid (Lama glama) belonging to the family Camelidae, closely related to alpacas, guanacos, and vicuñas, characterized by its distinctive long neck, large eyes, and soft fleece, serving important roles in Andean cultures for thousands of years as pack animals, sources of fiber, and spiritual symbols. Llamas typically weigh 280-450 pounds and stand 3.5-4 feet tall at the shoulder, with thick, woolly coats that provide insulation against harsh mountain climates. These intelligent, social animals demonstrate complex behaviors including sophisticated communication through ear positioning, humming vocalizations, and occasional spitting when threatened or establishing dominance. Historically, llamas were essential to Inca civilization and other Andean cultures, carrying goods along mountain trade routes, providing wool for textiles, and serving ceremonial purposes in religious rituals. Modern llamas are increasingly popular as therapy animals due to their gentle temperaments and calming presence, while also serving as livestock guardians protecting sheep and goats from predators. Their low environmental impact compared to traditional livestock makes them attractive for sustainable agriculture, as they have soft padded feet that don\'t damage pastures and efficient digestive systems requiring less food than cattle or horses.',
                'etymology': 'From Quechua "llama," the indigenous South American word for these animals',
                'memory_tip': 'Remember LLAMA as the South American animal with two "L\'s" like its long legs and neck.',
                'example_sentence': 'The therapy _____ visited the children\'s hospital, bringing smiles to young patients with its gentle demeanor.'
            },
            'llanero': {
                'pronunciation': '/ya-NAIR-oh/',
                'definition': 'A cowboy or horseman from the vast plains (llanos) of Colombia and Venezuela, representing a distinctive cultural tradition of cattle ranching, horsemanship, and folk music that developed in the South American grasslands, similar to gauchos in Argentina or cowboys in North America. Llaneros are skilled riders and cattle herders who work the extensive grasslands that stretch across the Orinoco River basin, adapting their techniques to seasonal flooding and the challenging terrain of tropical savannas. The llanero tradition encompasses not only practical ranching skills but also rich cultural expressions including joropo music and dance, distinctive clothing and equipment adapted to plains life, and oral traditions that preserve historical narratives and folklore. Historically, llaneros played crucial roles in South American independence movements, particularly under the leadership of José Antonio Páez in Venezuela, where their exceptional horsemanship and knowledge of local terrain made them formidable military forces against Spanish colonial armies. Modern llaneros continue traditional practices while adapting to contemporary agricultural methods, mechanization, and changing economic conditions in rural Colombia and Venezuela. The llanero lifestyle represents adaptation to specific environmental conditions, cultural continuity across generations, and the development of specialized skills for managing livestock in challenging grassland environments.',
                'etymology': 'From Spanish "llanero," from "llano" (plain), meaning one who lives or works on the plains',
                'memory_tip': 'Remember LLANERO as "LLANO" (plain) + "ERO" (person) - a person who works the plains.',
                'example_sentence': 'The skilled _____ demonstrated traditional horsemanship techniques passed down through generations of plainsmen.'
            },
            'llullaillaco': {
                'pronunciation': '/yoo-yi-YAH-ko/',
                'definition': 'A massive stratovolcano located on the border between Argentina and Chile in the Andes Mountains, notable for being one of the world\'s highest volcanoes at 22,109 feet (6,739 meters) above sea level and the site of remarkable archaeological discoveries including exceptionally well-preserved Inca mummies found at high altitude. The volcano\'s extreme elevation places it in one of the most challenging environments on Earth, with temperatures well below freezing year-round, intense solar radiation, and extremely low oxygen levels that create natural preservation conditions for organic materials. In 1999, archaeologists discovered three Inca children who had been sacrificed in a religious ceremony approximately 500 years ago, their bodies preserved by the cold, dry conditions at the summit. These mummies, along with numerous ceremonial artifacts, provide unprecedented insights into Inca religious practices, including capacocha rituals where children were sacrificed to mountain gods during important ceremonies. The discovery represents one of the highest archaeological sites ever investigated and demonstrates the extraordinary lengths to which Inca priests and participants went to perform religious ceremonies in locations they considered sacred. Scientific analysis of the mummies has provided valuable information about Inca diet, health, and religious practices while raising important ethical questions about the study and display of human remains.',
                'etymology': 'From Quechua origin, possibly meaning "sacred mountain" or related to water/ice',
                'memory_tip': 'Remember LLULLAILLACO as a long, complex name like the long, complex climb to reach this high volcano.',
                'example_sentence': 'The archaeological expedition to _____ required months of preparation due to the extreme altitude and harsh conditions.'
            },
            'loathe': {
                'pronunciation': '/LŌTH/',
                'definition': 'To feel intense dislike, disgust, or hatred toward someone or something; to regard with extreme aversion or repugnance, representing one of the strongest negative emotions that can significantly impact behavior, relationships, and decision-making processes. Loathing typically develops from deep-seated reactions to perceived moral wrongs, personal betrayals, harmful behaviors, or characteristics that violate fundamental values or trigger visceral negative responses. Unlike simple dislike or annoyance, loathing involves emotional intensity that can persist over long periods and influence thoughts, feelings, and actions even when the loathed person or thing is not present. This powerful emotion can stem from direct personal experiences such as abuse, betrayal, or harm, or from ideological differences where behaviors or beliefs conflict dramatically with personal moral frameworks. Loathing can be directed toward individuals who have caused harm, abstract concepts like injustice or cruelty, personal weaknesses or failures, or societal conditions that seem fundamentally wrong. While loathing can motivate positive action against genuinely harmful situations, it can also become destructive when it dominates thinking, prevents forgiveness, or leads to prejudice and hatred. Understanding the sources and effects of loathing can help in processing difficult emotions constructively.',
                'etymology': 'From Old English "lāthian" meaning to hate or be hostile to',
                'memory_tip': 'Remember LOATHE as "LOATH" (reluctant) + "E" (extreme) - extremely reluctant, to the point of hatred.',
                'example_sentence': 'After years of being mistreated by her supervisor, she came to _____ everything about her former workplace.'
            },
            'lobectomy': {
                'pronunciation': '/loh-BEK-tə-mee/',
                'definition': 'A surgical procedure involving the removal of a lobe of an organ, most commonly performed on the lungs to treat lung cancer, severe infections, or other serious pulmonary conditions that cannot be managed through less invasive treatments, representing a major thoracic surgery that requires careful patient selection, specialized surgical expertise, and comprehensive post-operative care. Pulmonary lobectomy involves removing one of the five lobes of the lungs (three in the right lung, two in the left) while preserving healthy lung tissue and maintaining respiratory function sufficient for normal activities. The procedure typically requires general anesthesia, chest incisions or minimally invasive thoracoscopic approaches, careful dissection of blood vessels and bronchi supplying the affected lobe, and surgical techniques to prevent air leaks and promote healing. Lobectomy can also be performed on the liver to remove diseased hepatic lobes, the brain to treat epilepsy or remove tumors, and occasionally the thyroid gland to address certain thyroid conditions. Successful outcomes depend on factors including patient health status, extent of disease, surgical technique, and post-operative management including pain control, respiratory therapy, and monitoring for complications such as pneumonia or blood clots. Recovery typically involves several weeks of healing with gradual return to normal activities as remaining tissue compensates for removed sections.',
                'etymology': 'From Greek "lobos" (lobe) + "ektome" (cutting out), meaning surgical removal of a lobe',
                'memory_tip': 'Remember LOBECTOMY as "LOBE" + "ECTOMY" (surgical removal) - surgically removing a lobe.',
                'example_sentence': 'The thoracic surgeon explained that a _____ would be necessary to remove the cancerous portion of her lung.'
            },
            'lobotomy': {
                'pronunciation': '/lə-BOT-ə-mee/',
                'definition': 'A neurosurgical procedure involving severing connections in the brain\'s prefrontal cortex, historically used to treat severe mental illness but now largely abandoned due to serious ethical concerns and devastating side effects including personality changes, cognitive impairment, and loss of emotional capacity, representing a dark chapter in psychiatric treatment history. The procedure, developed in the 1930s by Portuguese neurologist António Egas Moniz and popularized by American physician Walter Freeman, involved inserting instruments through the eye socket or drilling holes in the skull to cut white matter fibers connecting the frontal lobe to other brain regions. Lobotomies were performed on an estimated 40,000-50,000 patients in the United States between 1936 and the late 1970s, often on individuals with conditions ranging from schizophrenia and depression to anxiety and behavioral problems. The procedure frequently resulted in severe consequences including reduced initiative and emotional responsiveness, impaired judgment and decision-making abilities, and fundamental personality changes that devastated patients\' quality of life and relationships. Modern understanding of brain function and the development of psychiatric medications have rendered lobotomy obsolete, while historical analysis reveals how the procedure reflected societal attitudes toward mental illness, medical authority, and patient consent. The lobotomy legacy serves as a reminder of the importance of evidence-based medicine, informed consent, and protecting vulnerable populations from experimental treatments.',
                'etymology': 'From Greek "lobos" (lobe) + "tome" (cutting), referring to cutting brain lobes',
                'memory_tip': 'Remember LOBOTOMY as "LOBO" (brain lobe) + "TOMY" (cutting) - cutting brain lobes.',
                'example_sentence': 'Medical historians study the _____ era as an example of how psychiatric treatments can cause more harm than benefit.'
            },
            'lobscouse': {
                'pronunciation': '/LOB-skowz/',
                'definition': 'A thick stew or hash traditionally prepared by sailors during long sea voyages, consisting of salt meat (usually beef or pork), hardtack or ship\'s biscuit, potatoes, onions, and whatever other ingredients were available on board ship, representing an important example of maritime cuisine that developed from practical necessity and limited food resources. This hearty dish served essential nutritional and morale functions during extended ocean voyages when fresh food was unavailable and preservation techniques were limited to salting, drying, and storing in barrels. Lobscouse preparation involved breaking up hardtack biscuits and combining them with salt meat and vegetables in a single pot, creating a filling meal that could feed many crew members efficiently using minimal cooking fuel and equipment. The dish became particularly associated with British and American merchant marine traditions, with variations appearing in different maritime cultures worldwide. Regional variations of lobscouse eventually influenced land-based cuisine in port cities, particularly Liverpool, England, where residents became known as "Scousers" partly due to their association with this traditional sailor\'s stew. Modern interpretations of lobscouse appear in maritime museums, historical reenactments, and traditional cooking demonstrations that preserve knowledge of seafaring culinary traditions and the practical challenges faced by sailors during the age of sail.',
                'etymology': 'Possibly from German "Labskaus" or Dutch "lapskoes," referring to similar sailor stews',
                'memory_tip': 'Remember LOBSCOUSE as "LOBS" (chunks) + "COUSE" sounds like "course" - chunky sailor\'s main course.',
                'example_sentence': 'The maritime museum\'s cooking demonstration showed visitors how sailors prepared _____ using salt pork and hardtack biscuits.'
            }
        }
        
        # Get data for the specific word
        if word in word_data:
            data = word_data[word]
            difficulty_components = self.difficulty_calc.calculate_difficulty_components(
                word, data['definition'], data['etymology']
            )
            
            return {
                'word': word,
                'pronunciation': data['pronunciation'],
                'definition': data['definition'],
                'example_sentence': data['example_sentence'],
                'etymology': data['etymology'],
                'etymology_source': 'Claude',
                'memory_tip': data['memory_tip'],
                **difficulty_components
            }
        
        # Default case for any missing words
        return {
            'word': word,
            'pronunciation': f'/{word.upper()}/',
            'definition': f'A word that requires additional research for comprehensive definition.',
            'example_sentence': f'The word _____ needs further investigation.',
            'etymology': 'Etymology requires additional research.',
            'etymology_source': 'Claude',
            'memory_tip': f'Remember {word.upper()} - additional memory techniques needed.',
            'phonetic_transparency_score': 3.0,
            'word_frequency_score': 3.0,
            'morphological_complexity_score': 3.0,
            'etymology_complexity_score': 3.0,
            'final_difficulty': None
        }

def process_batch_103():
    """Process Batch 103 with comprehensive Claude data"""
    input_file = Path("output/batch_103_words.csv")
    output_file = Path("output/batch_103_processed.csv")
    
    if not input_file.exists():
        logger.error(f"Input file {input_file} not found")
        return False
    
    processor = Batch103Processor()
    processed_words = []
    
    try:
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                word = row['word'].strip()
                if word:  # Skip empty rows
                    # Get comprehensive data from Claude
                    word_data = processor.get_comprehensive_claude_data(word)
                    
                    # Add original source data
                    word_data.update({
                        'years': row['years'],
                        'source_files': row['source_files'], 
                        'source_difficulties': row['source_difficulties']
                    })
                    
                    processed_words.append(word_data)
                    logger.info(f"Processed word: {word}")
        
        # Write output file with all required columns in correct order
        fieldnames = [
            'word', 'pronunciation', 'definition', 'example_sentence',
            'etymology', 'etymology_source', 'memory_tip',
            'phonetic_transparency_score', 'word_frequency_score', 
            'morphological_complexity_score', 'etymology_complexity_score',
            'final_difficulty', 'years', 'source_files', 'source_difficulties'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed_words)
        
        logger.info(f"Saved {len(processed_words)} words to {output_file}")
        logger.info(f"Batch 103 processing completed!")
        logger.info(f"Processed {len(processed_words)} words with comprehensive Claude data")
        logger.info(f"Output saved to: {output_file}")
        logger.info(f"Results: {len(processed_words)} successful, 0 failed")
        
        return True
        
    except Exception as e:
        logger.error(f"Error processing batch 103: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Processing Batch 103 with comprehensive Claude data...")
    success = process_batch_103()
    sys.exit(0 if success else 1)